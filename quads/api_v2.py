import cherrypy
import datetime
import json
import logging
import os
import sys
import time

from quads import model
from quads.helpers import quads_load_config
from mongoengine.errors import DoesNotExist

from quads.tools.regenerate_vlans_wiki import regenerate_vlans_wiki

logger = logging.getLogger('api_v2')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)


class MethodHandlerBase(object):
    def __init__(self, _model, name=None, _property=None):
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
                if len(result) > 0:
                    return json.dumps({'result': result})
                _hosts = model.Host.objects()

                result = []
                for _host in _hosts:

                    _current = "cloud01"
                    _new = _current
                    _current_schedule = self.model.current_schedule(host=_host)
                    _schedule = self.model.current_schedule(host=_host, date=data['date'])
                    try:
                        if _current_schedule:
                            _current = _current_schedule["cloud"]["name"]
                        if _schedule:
                            _new = _schedule[0]["cloud"]["name"]
                        if _current != _new:
                            result.append(
                                {
                                    "host": _host["name"],
                                    "current": _current,
                                    "new": _new
                                })
                    except DoesNotExist:
                        continue

                return json.dumps({'result': result})
            except Exception:
                logger.info("400 Bad Request")
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
        if self.name == "available":

            _start = _end = datetime.datetime.now()
            if "start" in data:
                _start = datetime.datetime.strptime(data["start"], '%Y-%m-%dT%H:%M:%S')

            if "end" in data:
                _end = datetime.datetime.strptime(data["end"], '%Y-%m-%dT%H:%M:%S')

            available = []
            all_hosts = model.Host.objects().all()
            for host in all_hosts:
                if model.Schedule.is_host_available(host=host["name"], start=_start, end=_end):
                    available.append(host["name"])
            return json.dumps(available)

        if self.name == "summary":
            _clouds = model.Cloud.objects().all()
            clouds_summary = []
            for cloud in _clouds:
                count = self.model.current_schedule(cloud=cloud).count()
                clouds_summary.append(
                    {
                        "name": cloud["name"],
                        "count": count,
                        "description": cloud["description"],
                        "owner": cloud["owner"]
                    })

            return json.dumps(clouds_summary)
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

        _vlan = None
        if 'vlan' in data:
            _vlan = data.pop("vlan")
        # make sure post data passed in is ready to pass to mongo engine
        result, obj_data = self.model.prep_data(data)

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
                    '%s %s already exists.' % (self.name.capitalize(), obj_name)
                )
                cherrypy.response.status = "409 Conflict"
            else:
                # Create/update Operation
                try:
                    # if force and found object do an update
                    if force and obj:
                        # TODO: DEFAULTS OVERWRITE EXISTING VALUES
                        obj.update(**obj_data)
                        result.append(
                            'Updated %s %s' % (self.name, obj_name)
                        )
                    # otherwise create it
                    else:
                        self.model(**obj_data).save()
                        cherrypy.response.status = "201 Resource Created"
                        result.append(
                            'Created %s %s' % (self.name, obj_name)
                        )
                    if self.name == "cloud":

                        if _vlan:
                            update_data = {}
                            vlan_obj = model.Vlan.objects(vlan_id=_vlan).first()
                            update_data["cloud"] = self.model.objects(name=data["name"]).first()
                            if "owner" in data:
                                update_data["owner"] = data["owner"]
                            if "ticket" in data:
                                update_data["ticket"] = data["ticket"]
                            if vlan_obj:
                                vlan_obj.update(**update_data)
                                regenerate_vlans_wiki()
                            else:
                                result.append("WARN: No VLAN reference for that ID")

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
        # make sure post data passed in is ready to pass to mongo engine
        result, data = model.Schedule.prep_data(data)

        _start = None
        _end = None

        if "start" in data:
            _start = datetime.datetime.strptime(data["start"], '%Y-%m-%d %H:%M')

        if "end" in data:
            _end = datetime.datetime.strptime(data["end"], '%Y-%m-%d %H:%M')

        # Check if there were data validation errors
        if result:
            result = ['Data validation failed: %s' % ', '.join(result)]
            cherrypy.response.status = "400 Bad Request"
            return json.dumps({'result': result})

        if "cloud" in data:
            cloud_obj = model.Cloud.objects(name=data["cloud"]).first()
            if not cloud_obj:
                result.append("Provided cloud does not exist")
                cherrypy.response.status = "400 Bad Request"
                return json.dumps({'result': result})

        if "index" in data:
            _host = data["host"]
            data["host"] = model.Host.objects(name=_host).first()
            schedule = self.model.objects(index=data["index"], host=data["host"]).first()
            if schedule:
                if not _start:
                    _start = schedule["start"]
                if not _end:
                    _end = schedule["end"]
                if model.Schedule.is_host_available(host=_host, start=_start, end=_end, exclude=schedule["index"]):
                    data["cloud"] = cloud_obj
                    schedule.update(**data)
                    result.append(
                        'Updated %s %s' % (self.name, schedule["index"])
                    )
                else:
                    result.append("Host is not available during that time frame")

        else:
            try:
                schedule = model.Schedule()
                if model.Schedule.is_host_available(host=data["host"], start=_start, end=_end):
                    data["cloud"] = cloud_obj
                    schedule.insert_schedule(**data)
                    cherrypy.response.status = "201 Resource Created"
                    result.append('Added schedule for %s on %s' % (data["host"], cloud_obj.name))
                else:
                    result.append("Host is not available during that time frame")

            except Exception as e:
                # TODO: make sure when this is thrown the output
                #       points back to here and gives the end user
                #       enough information to fix the issue
                cherrypy.response.status = "500 Internal Server Error"
                result.append('Error: %s' % e)
        return json.dumps({'result': result})

    def PUT(self, **data):
        # update operations are done through POST
        # using PUT would duplicate most of POST
        return self.POST(**data)

    def DELETE(self, **data):
        _host = model.Host.objects(name=data["host"]).first()
        if _host:
            schedule = self.model.objects(host=_host, index=data["index"])
            if schedule:
                schedule.delete()
                cherrypy.response.status = "204 No Content"
                result = ['deleted %s ' % self.name]
            else:
                cherrypy.response.status = "404 Not Found"
                result = ['%s Not Found' % self.name]
        return json.dumps({'result': result})


@cherrypy.expose
class InterfaceMethodHandler(MethodHandlerBase):
    def GET(self, **data):
        _args = {}
        if "host" in data:
            host = model.Host.objects(name=data["host"]).first()
            if host:
                result = []
                for i in host.interfaces:
                    result.append(i.to_json())
                return json.dumps({'result': result})
        return json.dumps({'result': "No host provided"})

    # post data comes in **data
    def POST(self, **data):
        # handle force
        force = data.get('force', False) == 'True'
        if 'force' in data:
            del data['force']

        _host_name = data.pop("host")

        # make sure post data passed in is ready to pass to mongo engine
        result, data = self.model.prep_data(data)

        # Check if there were data validation errors
        if result:
            result = ['Data validation failed: %s' % ', '.join(result)]
            cherrypy.response.status = "400 Bad Request"
        else:
            _host = model.Host.objects(name=_host_name, interfaces__name=data["name"]).first()
            if _host and not force:
                result.append(
                    '%s %s already exists.' % (self.name.capitalize(), data["name"])
                )
                cherrypy.response.status = "409 Conflict"
            else:
                try:
                    interface = self.model(**data)
                    if force and _host:
                        updated = model.Host.objects(
                            name=_host_name,
                            interfaces__name=data["name"]
                        ).update_one(set__interfaces__S=interface)
                        if updated:
                            cherrypy.response.status = "201 Resource Created"
                            result.append('Updated %s %s' % (self.name, data["name"]))
                        else:
                            cherrypy.response.status = "400 Bad Request"
                            result.append('Host %s not found.' % _host_name)
                    else:
                        updated = model.Host.objects(name=_host_name).update_one(push__interfaces=interface)
                        if updated:
                            cherrypy.response.status = "201 Resource Created"
                            result.append('Created %s %s' % (self.name, data["name"]))
                        else:
                            cherrypy.response.status = "400 Bad Request"
                            result.append('Host %s not found.' % _host_name)
                except Exception as e:
                    # TODO: make sure when this is thrown the output
                    #       points back to here and gives the end user
                    #       enough information to fix the issue
                    cherrypy.response.status = "500 Internal Server Error"
                    result.append('Error: %s' % e)
        return json.dumps({'result': result})

    def PUT(self, **data):
        # update operations are done through POST
        # using PUT would duplicate most of POST
        return self.POST(**data)

    def DELETE(self, **data):
        _host = model.Host.objects(name=data["host"], interfaces__name=data["name"]).first()
        result = []
        if _host:
            try:
                model.Host.objects(
                    name=data["host"],
                    interfaces__name=data["name"]
                ).update_one(pull__interfaces__name=data["name"])
                cherrypy.response.status = "204 No Content"
                result.append('Removed %s.' % data["name"])
            except Exception as e:
                cherrypy.response.status = "500 Internal Server Error"
                result.append('Error: %s' % e)

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
        self.available = DocumentMethodHandler(model.Schedule, 'available')
        self.summary = DocumentMethodHandler(model.Schedule, 'summary')
        self.interfaces = InterfaceMethodHandler(model.Interface, 'interface')
        self.moves = MovesMethodHandler(model.Schedule, 'moves')
