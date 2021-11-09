import json
from datetime import datetime

from flask import request, jsonify
from flask_restful import Resource
from mongoengine import DoesNotExist
from werkzeug.exceptions import BadRequest

from quads.model import Host

# example flask_restful use of Resource
# these are a bit different compared to flask's MethodView
# flask_restful is often used to create clean CRUD (json) api's
# it's less useful once you need to start doing RPC-like stuff
# (ex. /movehost, /schedule)

class MovesEndpoint(Resource):
    def get(self):
        data = dict(request.args)

        if "date" in data:
            date = datetime.strptime(data["date"], "%Y-%m-%dt%H:%M:%S")
        else:
            date = datetime.now()

        try:
            _hosts = Host.objects()

            result = []
            for _host in _hosts:

                _scheduled_cloud = _host.default_cloud.name
                _host_defined_cloud = _host.cloud.name
                _current_schedule = self.model.current_schedule(
                    host=_host, date=date
                ).first()
                try:
                    if _current_schedule:
                        _scheduled_cloud = _current_schedule.cloud.name
                    if _scheduled_cloud != _host_defined_cloud:
                        result.append(
                            {
                                "host": _host.name,
                                "new": _scheduled_cloud,
                                "current": _host_defined_cloud,
                            }
                        )
                except DoesNotExist:
                    continue

            return jsonify({"result": result})
        except Exception as ex:
            # logger.exception(ex, exc_info=ex)
            raise BadRequest(json.dumps({"result": "Bad Request"})) from ex
