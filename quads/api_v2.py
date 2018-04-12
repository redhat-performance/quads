import cherrypy
import json
import urllib

from quads import model as m

@cherrypy.expose
class MethodHandler(object):
    def __init__(self, model, name):
        self.m = model
        self.name = name

    def _get_obj(self, obj):
        q = {self.name: obj}
        obj = self.m.objects(**q).first()
        return obj

    def GET(self, **data):
        args = {}
        if 'cloudonly' in data:
            c = Cloud.objects(cloud=data['cloudonly']).first()
            if not c:
                raise cherrypy.HTTPError(404,
                        'Cloud %s Not Found' % data['cloudonly'])
            else:
                args.update({'cloud': c})
        return self.m.objects(**args).to_json()

    # post data comes in **data
    def POST(self, **data):
        # handle force
        force = True if data.get('force', False) == 'True' else False
        if 'force' in data:
            del data['force']

        # make sure post data passed in is ready to pass to mongo engine
        result, data = self.m.prep_data(data)

        # Check if there were data validation errors
        if not result:
            # check if object already exists
            obj = self._get_obj(data[self.name])
            if obj and not force:
                result.append('%s %s already exists' % (
                                self.name,
                                data[self.name]))
            else:
                # Create/update Operation
                try:
                    # if force and found object do an update
                    if force and obj:
                        obj.update(**data)
                        result.append('Updated %s %s' % (self.name,
                                                         data[self.name]))
                    # otherwise create it
                    else:
                        obj = self.m(**data).save()
                        result.append('Created %s %s' % (self.name,
                                                         data[self.name]))
                except Exception, e:
                    result.append(e)

        return json.dumps({'result': result})

    def PUT(self, **data):
        # update operations are done through POST
        # using PUT would duplicate most of POST
        return self.POST(**data)

    def DELETE(self, obj_name):
        obj = self._get_obj(obj_name)
        if obj:
            obj.delete()
            # TODO: better msg please!
            result = ['deleted %s %s' % (self.name, obj_name)]
        else:
            raise cherrypy.HTTPError(404, '%s %s Not Found' % (
                                     self.name, obj))
        return json.dumps({'result': result})

@cherrypy.expose
class QuadsServerApiV2(object):
    def __init__(self):
        self.host = MethodHandler(m.Host, 'host')
        self.cloud = MethodHandler(m.Cloud, 'cloud')
        self.owner = MethodHandler(m.Cloud, 'owner')
        self.ccuser = MethodHandler(m.Cloud, 'ccuser')
        self.ticket = MethodHandler(m.Cloud, 'ticket')
        self.qinq = MethodHandler(m.Cloud, 'qinq')
        self.wipe = MethodHandler(m.Cloud, 'wipe')
