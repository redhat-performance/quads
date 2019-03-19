#!/usr/bin/env python3
import cherrypy
import datetime
import json
import logging
import time

from quads import model
from mongoengine.errors import DoesNotExist
from quads.config import conf
from quads.tools.foreman import Foreman
from quads.tools.regenerate_vlans_wiki import regenerate_vlans_wiki

logger = logging.getLogger()


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
    def GET(self, **data):
        if self.name == "moves":
            try:
                result = []
                if 'date' not in data:
                    data['date'] = [time.strftime("%Y-%m-%d %H:%M")]
                else:
                    if len(data['date']) == 0:
                        result.append("Could not parse date parameter")
                        return json.dumps({'result': result})

                _hosts = model.Host.objects()

                result = []
                for _host in _hosts:

                    _scheduled_cloud = "cloud01"
                    _host_defined_cloud = _host.cloud.name
                    _current_schedule = self.model.current_schedule(host=_host).first()
                    _schedule = self.model.current_schedule(host=_host, date=data['date']).first()
                    try:
                        if _current_schedule:
                            _scheduled_cloud = _current_schedule.cloud.name
                        if _schedule:
                            _host_defined_cloud = _schedule.cloud.name
                        if _scheduled_cloud != _host_defined_cloud:
                            result.append(
                                {
                                    "host": _host.name,
                                    "new": _scheduled_cloud,
                                    "current": _host_defined_cloud
                                })
                    except DoesNotExist:
                        continue

                return json.dumps({'result': result})
            except Exception as ex:
                logger.debug(ex)
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
                _cloud = model.Cloud.objects(name=data["cloud"]).first()
                _host = model.Host.objects(cloud=_cloud)
            else:
                _host = model.Host.objects()
            if not _host:
                return json.dumps({'result': ["Nothing to do."]})
            return _host.to_json()
        if self.name == "ccuser":
            _clouds = model.Cloud.objects().all()
            clouds_summary = []
            for cloud in _clouds:
                count = self.model.current_schedule(cloud=cloud).count()
                clouds_summary.append(
                    {
                        "name": cloud.name,
                        "count": count,
                        "description": cloud.description,
                        "owner": cloud.owner,
                        "ticket": cloud.ticket,
                        "ccuser": cloud.ccuser,
                        "released": cloud.released
                    })

            return json.dumps(clouds_summary)
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
                _start = datetime.datetime.strptime(data["start"], '%Y-%m-%d %H:%M:%S')

            if "end" in data:
                _end = datetime.datetime.strptime(data["end"], '%Y-%m-%d %H:%M:%S')

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
                        "name": cloud.name,
                        "count": count,
                        "description": cloud.description,
                        "owner": cloud.owner,
                        "ticket": cloud.ticket,
                        "ccuser": cloud.ccuser,
                        "released": cloud.released,
                        "validated": cloud.validated,
                        "notified": cloud.notified
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
            date = datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M")
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

        # check for broken hosts from foreman
        # to enable checking foreman host health before scheduling
        # set foreman_check_host_health: true in conf/quads.yml
        if conf["foreman_check_host_health"]:
            foreman = Foreman(
                conf["foreman_api_url"],
                conf["foreman_username"],
                conf["foreman_password"]
            )
            broken_hosts = foreman.get_broken_hosts()
            if broken_hosts.get(data['host'], False):
                result.append("Host %s is in broken state" % data['host'])

        # Check if there were data validation errors
        if result:
            result = ['Data validation failed: %s' % ', '.join(result)]
            cherrypy.response.status = "400 Bad Request"
            return json.dumps({'result': result})

        cloud_obj = None
        if "cloud" in data:
            cloud_obj = model.Cloud.objects(name=data["cloud"]).first()
            if not cloud_obj:
                result.append("Provided cloud does not exist")
                cherrypy.response.status = "400 Bad Request"
                return json.dumps({'result': result})

        _host = data["host"]
        _host_obj = model.Host.objects(name=_host).first()

        if "index" in data:
            data["host"] = _host_obj
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
                if model.Schedule.is_host_available(host=_host, start=_start, end=_end):
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
