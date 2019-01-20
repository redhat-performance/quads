from datetime import datetime
from mongoengine import (
    connect,
    Document,
    StringField,
    BooleanField,
    ListField,
    ReferenceField,
    DateTimeField,
    queryset_manager,
    Q,
    SequenceField,
    IntField)
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

        params = ['name', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Host(Document):
    name = StringField(unique=True)
    cloud = ReferenceField(Cloud)
    host_type = StringField()
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
        result, data = param_check(data, ['name', 'cloud', 'host_type'])

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
