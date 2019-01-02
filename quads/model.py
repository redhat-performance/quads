from datetime import datetime
from mongoengine import (
    connect,
    Document,
    StringField,
    BooleanField,
    ListField,
    ReferenceField,
    DateTimeField,
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
    name = StringField()
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
    name = StringField()
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


class Schedule(Document):
    cloud = ReferenceField(Cloud)
    host = ReferenceField(Host)
    start = DateTimeField()
    end = DateTimeField()
    meta = {'strict': False}

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['cloud', 'host'])

        return result, data

