from mongoengine import *

connect('quads')

# TODO: Put this some where else
def param_check(data, params, defaults={}):
    result = []
    # set defaults
    for k, v in defaults.items():
        data.setdefault(k, v)

    if data:
        # check for missing params
        for p in params:
            if p not in data:
                result.append("Missing required parameter: %s" % p)
            elif str == type(data[p]) and not data[p]:
                result.append("Could not parse %s parameter" % p)
            elif data[p] == 'None':
                data[p] = None
    return result, data

class Cloud(Document):
    #name = 'cloud'
    cloud = StringField()
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qinq = BooleanField()
    wipe = BooleanField()
    post_config = ListField()
    ccuser = ListField()

    @staticmethod
    def prep_data(data):
        # hard coded for cloud
        defaults = {'owner': 'nobody',
                    'ccuser': [],
                    'ticket': '000000',
                    'qinq': False,
                    'wipe': True}

        result, data = param_check(data,
                                   ['cloud', 'description', 'owner', 'ccuser',
                                    'ticket', 'qinq', 'wipe'],
                                   defaults)

        return result, data


class Host(Document):
    #name = 'host'
    host = StringField()
    cloud = ReferenceField(Cloud, required=True)
    interfaces = DictField()
    schedule = DictField()
    type = StringField()

    @staticmethod
    def prep_data(data):
        result, data = param_check(data, ['host', 'cloud', 'type'])
        if not result:
            cloud = Cloud.objects(cloud=data['cloud']).first()
            if not cloud:
               result.append('Cloud %s not found')
            else:
               data['cloud'] = cloud
        
        return result, data


class History(Document):
    pass

class CloudHistory(Document):
    cloud = ReferenceField(Cloud, required=True)
    dt_stamp = DateTimeField()
    name = StringField()
    description = StringField()
    owner = StringField()
    ticket = StringField()
    qing = BooleanField()
    wipe = BooleanField()
    post_config = ListField()
    ccusers = ListField()
