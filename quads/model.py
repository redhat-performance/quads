from datetime import datetime
from mongoengine import (
    connect,
    Document,
    StringField,
    BooleanField,
    ListField,
    ReferenceField,
    DictField,
    DateTimeField
)
from quads.helpers import param_check

import os


connect(
    'quads',
    host=os.environ.get("MONGODB_IP", "127.0.0.1")
)


class CloudHistory(Document):
    cloud = StringField()
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
                'fields': ['$cloud']
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
        data['cloud'] = data['_id']
        data.pop('_id')

        params = ['cloud', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Cloud(Document):
    _id = StringField()
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = BooleanField()
    wipe = BooleanField()
    post_config = ListField()
    ccuser = ListField()

    @staticmethod
    def prep_data(data):
        defaults = {
            'owner': 'nobody',
            'ccuser': [],
            'ticket': '000000',
            'qinq': False,
            'wipe': True
        }

        params = ['_id', 'description', 'owner', 'ticket', 'wipe']
        result, data = param_check(data, params, defaults)

        return result, data


class Schedule(Document):
    start = DateTimeField()
    end = DateTimeField()
    meta = {'strict': False}

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['start', 'end'])

        return result, data


class Host(Document):
    host = StringField()
    cloud = StringField()
    interfaces = DictField()
    schedule = ReferenceField(Schedule)
    type = StringField()
    meta = {
        'indexes': [
            {
                'fields': ['$host']
            }
        ],
        'strict': False
    }

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['host', 'cloud', 'type'])

        return result, data

    @staticmethod
    def prep_interfaces_data(data):
        result, data = param_check(data, ['host', 'interface', 'mac',
                                          'vendor_type', 'port'])
        host = None
        if not result:
            host = Host.objects(host=data['host']).first()
            if not host:
                result.append('Host %s not found' % data['host'])
            else:
                del data['host']
            interface = data['interface']
            del data['interface']
            data = {'set__interfaces__%s' % interface: data}

        return result, host, data
