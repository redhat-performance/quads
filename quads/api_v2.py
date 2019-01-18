import cherrypy
import datetime
import json
import logging
import os
import sys
import time

from quads import model
from quads.helpers import quads_load_config

logger = logging.getLogger('api_v2')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)


class MethodHandlerBase(object):
    def __init__(self, _model, name, _property=None):
        self.model = _model
        self.name = name
        self.property = _property

    def _get_obj(self, obj):
        """

        :rtype: object
        """
        q = {'name': obj}
        obj = self.model.objects(**q).first()
        return obj


@cherrypy.expose
class MovesMethodHandler(MethodHandlerBase):
    def POST(self, **data):
        if self.name == "moves":
            try:
                result = []
                # statedir, datearg
                if 'date' not in data:
                    data['date'] = [time.strftime("%Y-%m-%d %H:%M")]
                else:
                    if len(data['date']) == 0:
                        result.append("Could not parse date parameter")
                if 'statedir' not in data:
                    result.append("Missing required parameter: statedir")
                else:
                    if len(data['statedir']) == 0:
                        result.append("Could not parse statedir parameter")
                if len(result) > 0:
                    return json.dumps({'result': result})

                return json.dumps({'result': result})
            except Exception:
                logger.info("%s - %s - %s %s" % (self.client_address[0],
                                                 self.command,
                                                 self.path,
                                                 "400 Bad Request"))
                cherrypy.response.status = "400 Bad Request"
                return json.dumps({'result': ['400 Bad Request']})


@cherrypy.expose
class DocumentMethodHandler(MethodHandlerBase):
    def GET(self, **data):
        args = {}
        _cloud = None
        _host = None
        if 'cloudonly' in data:
            _cloud = model.Cloud.objects(cloud=data['cloudonly'])
            if not _cloud:
                cherrypy.response.status = "404 Not Found"
                return json.dumps({'result': 'Cloud %s Not Found' % data['cloudonly']})
            else:
                return _cloud.to_json()
        if self.name == "host":
            if 'id' in data:
                _host = model.Host.objects(id=data["id"]).first()
            elif 'name' in data:
                _host = model.Host.objects(name=data["name"]).first()
            elif 'cloud' in data:
                _host = model.Host.objects(cloud=data["cloud"])
            else:
                _host = model.Host.objects()
            if not _host:
                return json.dumps({'result': ["Nothing to do."]})
            return _host.to_json()
        if self.name == "cloud":
            if 'id' in data:
                _cloud = model.Cloud.objects(id=data["id"]).first()
            elif 'name' in data:
                _cloud = model.Cloud.objects(name=data["name"]).first()
            elif 'owner' in data:
                _cloud = model.Cloud.to_json(owner=data["owner"]).first()
            if _cloud:
                return _cloud.to_json()
        objs = self.model.objects(**args)
        if objs:
            return objs.to_json()
        else:
            return json.dumps({'result': ["No results."]})

    # post data comes in **data
    def POST(self, **data):
        # handle force

        force = data.get('force', False) == 'True'
        if 'force' in data:
            del data['force']

        # make sure post data passed in is ready to pass to mongo engine
        result, data = self.model.prep_data(data)

        # Check if there were data validation errors
        if result:
            result = ['Data validation failed: %s' % ', '.join(result)]
            cherrypy.response.status = "400 Bad Request"
        else:
            # check if object already exists
            obj_name = data['name']
            obj = self._get_obj(obj_name)
            if obj and not force:
                result.append(
                    '%s %s already exists' % (self.name, obj_name)
                )
                cherrypy.response.status = "409 Conflict"
            else:
                # Create/update Operation
                try:
                    # if force and found object do an update
                    if force and obj:
                        # TODO: DEFAULTS OVERWRITE EXISTING VALUES
                        obj.update(**data)
                        result.append(
                            'Updated %s %s' % (self.name, obj_name)
                        )
                    # otherwise create it
                    else:
                        self.model(**data).save()
                        cherrypy.response.status = "201 Resource Created"
                        result.append(
                            'Created %s %s' % (self.name, obj_name)
                        )
                    if self.name == "cloud":
                        history_result, history_data = model.CloudHistory.prep_data(data)
                        if history_result:
                            result.append('Data validation failed: %s' % ', '.join(history_result))
                            cherrypy.response.status = "400 Bad Request"
                        else:
                            model.CloudHistory(**history_data).save()
                except Exception as e:
                    # TODO: make sure when this is thrown the output
                    #       points back to here and gives the end user
                    #       enough information to fix the issue
                    cherrypy.response.status = "500 Internal Server Error"
                    result.append('Error: %s' % e)
        print(result)
        return json.dumps({'result': result})

    def PUT(self, **data):
        # update operations are done through POST
        # using PUT would duplicate most of POST
        return self.POST(**data)

    def DELETE(self, obj_name):
        obj = self._get_obj(obj_name)
        if obj:
            obj.delete()
            cherrypy.response.status = "204 No Content"
            result = ['deleted %s %s' % (self.name, obj_name)]
        else:
            cherrypy.response.status = "404 Not Found"
            result = ['%s %s Not Found' % (self.name, obj_name)]
        return json.dumps({'result': result})


@cherrypy.expose
class ScheduleMethodHandler(MethodHandlerBase):
    def GET(self, **data):
        _args = {}
        if "date" in data:
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%dT%H:%M:%S")
            _args["date"] = date
        if "host" in data:
            host = model.Host.objects(name=data["host"]).first()
            if host:
                _args["host"] = host
        if "cloud" in data:
            cloud = model.Cloud.objects(name=data["cloud"]).first()
            if cloud:
                _args["cloud"] = cloud
        if self.name == "current_schedule":
            _schedule = self.model.current_schedule(**_args)
            if _schedule:
                return _schedule.to_json()
            else:
                return json.dumps({'result': ["No results."]})
        return self.model.objects(**_args).to_json()

    # post data comes in **data
    def POST(self, **data):
        import ipdb;ipdb.set_trace()
        # make sure post data passed in is ready to pass to mongo engine
        result, data = model.Schedule.prep_data(data)

        # Check if there were data validation errors
        if result:
            result = ['Data validation failed: %s' % ', '.join(result)]
            cherrypy.response.status = "400 Bad Request"
        else:
            try:
                h_query = {'name': data['host']}
                h_obj = model.Host.objects(**h_query).first()
                data['host'] = h_obj

                c_query = {'name': data["cloud"]}
                c_obj = model.Cloud.objects(**c_query).first()
                data['cloud'] = c_obj

                model.Schedule(**data).save()

                cherrypy.response.status = "201 Resource Created"
                result.append('Added %s %s' % (self.property, data))
            except Exception as e:
                # TODO: make sure when this is thrown the output
                #       points back to here and gives the end user
                #       enough information to fix the issue
                cherrypy.response.status = "500 Internal Server Error"
                result.append('Error: %s' % e)
        print(result)
        return json.dumps({'result': result})

    def PUT(self, **data):
        # update operations are done through POST
        # using PUT would duplicate most of POST
        return self.POST(**data)

    def DELETE(self, item, obj_name):
        obj = self._get_obj(obj_name)
        if obj:
            data = {'unset__%s__%s' % (self.property, item): True}
            obj.update(**data)
            result = ['deleted %s from %s' % (self.property, obj_name)]
        else:
            cherrypy.response.status = "404 Not Found"
            result = ['%s Not Found for %s %s' % (self.property, self.name, obj_name)]
        return json.dumps({'result': result})


@cherrypy.expose
class QuadsServerApiV2(object):
    def __init__(self):
        self.cloud = DocumentMethodHandler(model.Cloud, 'cloud')
        self.owner = DocumentMethodHandler(model.Cloud, 'owner')
        self.ccuser = DocumentMethodHandler(model.Cloud, 'ccuser')
        self.ticket = DocumentMethodHandler(model.Cloud, 'ticket')
        self.qinq = DocumentMethodHandler(model.Cloud, 'qinq')
        self.wipe = DocumentMethodHandler(model.Cloud, 'wipe')
        self.host = DocumentMethodHandler(model.Host, 'host')
        self.schedule = ScheduleMethodHandler(model.Schedule, 'schedule')
        self.current_schedule = ScheduleMethodHandler(model.Schedule, 'current_schedule')
        self.moves = MovesMethodHandler('moves', 'moves')
