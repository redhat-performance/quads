import json
from datetime import datetime
from mongoengine.base import BaseDocument
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
    EmbeddedDocumentField
)
from quads.helpers import param_check

import os

connect(
    'quads',
    host=os.environ.get("MONGODB_IP", "127.0.0.1")
)


class CloudHistory(Document):
    name = StringField()
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = BooleanField()
    wipe = BooleanField()
    post_config = ListField()
    ccuser = ListField()
    date = DateTimeField()
    meta = {
        'indexes': [
            {
                'fields': ['$name']
            }
        ]
    }

    @staticmethod
    def prep_data(data):
        defaults = {
            'owner': 'nobody',
            'ccuser': [],
            'ticket': '000000',
            'qinq': False,
            'wipe': True,
            'date': datetime.now()
        }

        params = ['name', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Cloud(Document):
    name = StringField(unique=True)
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = BooleanField()
    wipe = BooleanField()
    post_config = ListField()
    ccuser = ListField()
    meta = {
        'indexes': [
            {
                'fields': ['$name']
            }
        ]
    }

    @staticmethod
    def prep_data(data):
        defaults = {
            'owner': 'nobody',
            'ccuser': [],
            'ticket': '000000',
            'qinq': False,
            'wipe': True
        }

        if "vlan" in data:
            data.pop("vlan")
        params = ['name', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Vlan(Document):
    gateway = StringField()
    ip_free = IntField()
    ip_range = StringField()
    netmask = StringField()
    owner = StringField()
    ticket = LongField()
    vlan_id = LongField()
    cloud = ReferenceField(Cloud)
    meta = {
        'indexes': [
            {
                'fields': ['$vlan_id']
            }
        ]
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
        if "ipfree" in data:
            data["ip_free"] = data.pop("ipfree")
        if "iprange" in data:
            data["ip_range"] = data.pop("iprange")
        if "vlanid" in data:
            data["vlan_id"] = data.pop("vlanid")
        result, data = param_check(data, _fields)

        return result, data


class Interface(EmbeddedDocument):
    name = StringField()
    mac_address = StringField()
    ip_address = StringField()
    vlan = StringField()
    switch_port = StringField()

    @staticmethod
    def prep_data(data):
        _fields = ['name', 'mac_address', 'ip_address', 'vlan', 'switch_port']
        result, data = param_check(data, _fields)

        return result, data


class Host(Document):
    name = StringField(unique=True)
    default_cloud = ReferenceField(Cloud)
    host_type = StringField()
    interfaces = ListField(EmbeddedDocumentField(Interface))
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
        result, data = param_check(data, ['name', 'default_cloud', 'host_type'])

        return result, data


class Counters(Document):
    _id = StringField()
    seq = SequenceField()


class Schedule(Document):
    cloud = ReferenceField(Cloud)
    host = ReferenceField(Host)
    start = DateTimeField()
    end = DateTimeField()
    index = IntField()
    meta = {'strict': False}

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['cloud', 'host'])

        return result, data

    @staticmethod
    def get_next_sequence(name):
        Counters.objects(_id=name).update_one(upsert=True, inc__seq=1)
        return Counters.objects(_id=name).first()["seq"]

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
            if result["start"] <= start <= result["end"]:
                return False
            if result["start"] <= end <= result["end"]:
                return False
            if start < result["start"] and end > result["end"]:
                return False
        return True

    @queryset_manager
    def current_schedule(self, queryset, date=datetime.now(), host=None, cloud=None):
        _query = Q(start__lte=date) & Q(end__gte=date)
        if host:
            _query = _query & Q(host=host)
        if cloud:
            _query = _query & Q(cloud=cloud)
        return queryset.filter(_query)
