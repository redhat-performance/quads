from datetime import datetime
from mongoengine import (
    connect,
    Document,
    EmbeddedDocument,
    queryset_manager,
    Q,
    StringField,
    BooleanField,
    ListField,
    ReferenceField,
    DateTimeField,
    SequenceField,
    IntField,
    LongField,
    EmbeddedDocumentField,
)
from quads.helpers import param_check

import os

connect(
    'quads',
    host=os.environ.get('MONGODB_IP', '127.0.0.1')
)


class CloudHistory(Document):
    name = StringField()
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = BooleanField()
    wipe = BooleanField()
    ccuser = ListField()
    meta = {
        'indexes': [
            {
                'fields': ['$name']
            }
        ],
        'strict': False
    }

    @staticmethod
    def prep_data(data):
        defaults = {
            'owner': 'quads',
            'ccuser': [],
            'ticket': '000000',
            'qinq': False,
            'wipe': True,
        }
        for flag in ['provisioned', 'validated']:
            if flag in data:
                data.pop(flag)

        params = ['name', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Cloud(Document):
    name = StringField(unique=True)
    description = StringField()
    owner = StringField(default='quads')
    ticket = StringField(default='000000')
    qinq = BooleanField(default=False)
    wipe = BooleanField(default=True)
    ccuser = ListField()
    provisioned = BooleanField(default=False)
    # TODO: Remove 'released' field after 451493_accommodate.py execution
    released = BooleanField()
    validated = BooleanField(default=False)
    meta = {
        'indexes': [
            {
                'fields': ['$name']
            }
        ],
        'strict': False
    }

    @staticmethod
    def prep_data(data):
        if 'vlan' in data:
            data.pop('vlan')
        if 'ccuser' in data:
            data['ccuser'] = data['ccuser'].split()
        if 'qinq' in data:
            data['qinq'] = bool(data['qinq'])

        params = ['name', 'description', 'owner']
        result, data = param_check(data, params)

        return result, data


class Notification(Document):
    cloud = ReferenceField(Cloud)
    ticket = StringField()
    fail = BooleanField(default=False)
    success = BooleanField(default=False)
    initial = BooleanField(default=False)
    pre_initial = BooleanField(default=False)
    pre = BooleanField(default=False)
    one_day = BooleanField(default=False)
    three_days = BooleanField(default=False)
    five_days = BooleanField(default=False)
    seven_days = BooleanField(default=False)


class Vlan(Document):
    gateway = StringField()
    ip_free = IntField()
    ip_range = StringField()
    netmask = StringField()
    owner = StringField()
    ticket = StringField()
    vlan_id = LongField()
    cloud = ReferenceField(Cloud)
    meta = {
        'indexes': [
            {
                'fields': ['$vlan_id']
            }
        ],
        'strict': False
    }

    @staticmethod
    def prep_data(data):
        _fields = [
            'gateway',
            'ip_free',
            'ip_range',
            'netmask',
            'owner',
            'vlan_id',
        ]
        if 'ipfree' in data:
            data['ip_free'] = data.pop('ipfree')
        if 'iprange' in data:
            data['ip_range'] = data.pop('iprange')
        if 'vlanid' in data:
            data['vlan_id'] = data.pop('vlanid')
        result, data = param_check(data, _fields)

        return result, data


class Interface(EmbeddedDocument):
    name = StringField()
    mac_address = StringField()
    ip_address = StringField()
    switch_port = StringField()

    @staticmethod
    def prep_data(data):
        _fields = ['name', 'mac_address', 'ip_address', 'switch_port']
        result, data = param_check(data, _fields)

        return result, data


class Host(Document):
    name = StringField(unique=True)
    cloud = ReferenceField(Cloud)
    host_type = StringField()
    interfaces = ListField(EmbeddedDocumentField(Interface))
    nullos = BooleanField(default=True)
    build = BooleanField(default=False)
    last_build = DateTimeField()
    meta = {
        'indexes': [
            {
                'fields': ['$name']
            }
        ],
        'strict': False
    }

    @staticmethod
    def prep_data(data):
        if 'cloud' in data:
            _cloud_obj = Cloud.objects(name=data['cloud']).first()
            if _cloud_obj:
                data['cloud'] = _cloud_obj
            else:
                return ['Cloud %s does not exist.' % data['cloud']], {}

        result, data = param_check(data, ['name', 'cloud', 'host_type'])

        return result, data


class Counters(Document):
    _id = StringField()
    seq = SequenceField()


class Schedule(Document):
    cloud = ReferenceField(Cloud, required=True)
    host = ReferenceField(Host, required=True)
    start = DateTimeField()
    end = DateTimeField()
    index = IntField()
    meta = {'strict': False}

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['host'])

        return result, data

    @staticmethod
    def get_next_sequence(name):
        Counters.objects(_id=name).update_one(upsert=True, inc__seq=1)
        return Counters.objects(_id=name).first()['seq']

    def insert_schedule(self, cloud, host, start, end):
        if host:
            self.index = self.get_next_sequence(host)
            self.host = Host.objects(name=host).first()
        if cloud:
            if type(cloud) == Cloud:
                self.cloud = cloud
            else:
                self.cloud = Cloud.objects(name=cloud).first()
        self.start = start
        self.end = end
        return self.save()

    @queryset_manager
    def is_host_available(self, queryset, host, start, end, exclude=None):
        _host = Host.objects(name=host).first()
        _query = Q(host=_host)
        if exclude:
            _query = _query & Q(index__ne=exclude)
        results = queryset.filter(_query)
        for result in results:
            if result['start'] <= start < result['end']:
                return False
            if result['start'] < end <= result['end']:
                return False
            if start < result['start'] and end > result['end']:
                return False
        return True

    @queryset_manager
    def current_schedule(self, queryset, date=None, host=None, cloud=None):
        if not date:
            date = datetime.now()
        _query = Q(start__lte=date) & Q(end__gte=date)
        if host:
            _query = _query & Q(host=host)
        if cloud:
            _query = _query & Q(cloud=cloud)
        return queryset.no_cache().filter(_query)
