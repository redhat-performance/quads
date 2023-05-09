import json

from flask import Blueprint, jsonify, request, Response
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.sql.sqltypes import Boolean

from quads.config import Config
from quads.server.blueprints import check_access
from quads.server.dao.baseDao import MAP_MODEL, OPERATORS
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.models import Host, db


host_bp = Blueprint("hosts", __name__)


@host_bp.route("/")
def get_hosts() -> Response:
    if request.args:
        _hosts = HostDao.filter_hosts_dict(request.args)
    else:
        _hosts = HostDao.get_hosts()
    return jsonify([_host.as_dict() for _host in _hosts])


@host_bp.route("/<hostname>")
def get_host(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)
    return jsonify(_host.as_dict())


@host_bp.route("/<hostname>", methods=["PATCH"])
@check_access("admin")
def update_host(hostname: str) -> Response:
    data = request.get_json()
    cloud_name = data.get("cloud")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not default_cloud:
        default_cloud = Config["spare_pool_name"]

    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    if default_cloud:
        _default_cloud = CloudDao.get_cloud(default_cloud)
        if not _default_cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Default Cloud not found: {default_cloud}",
            }
            return Response(response=json.dumps(response), status=400)

        else:
            _host.default_cloud = _default_cloud

    if cloud_name:
        _cloud = CloudDao.get_cloud(cloud_name)
        if not _cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud not found: {cloud_name}",
            }
            return Response(response=json.dumps(response), status=400)
        else:
            _host.cloud = _cloud

    if host_type:
        _host.host_type = host_type

    db.session.commit()

    return jsonify(_host.as_dict())


@host_bp.route("/", methods=["POST"])
@check_access("admin")
def create_host() -> Response:
    data = request.get_json()
    hostname = data.get("name")
    model = data.get("model")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not model:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: model",
        }
        return Response(response=json.dumps(response), status=400)
    else:
        if model.upper() not in Config["models"]:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Model {model} does not seem to be part of the defined models on quads.yml",
            }
            return Response(response=json.dumps(response), status=400)

    if not default_cloud:
        default_cloud = Config["spare_pool_name"]

    if not hostname:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: name",
        }
        return Response(response=json.dumps(response), status=400)

    _host = HostDao.get_host(hostname)
    if _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host {hostname} already exists",
        }
        return Response(response=json.dumps(response), status=400)

    if not host_type:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: host_type",
        }
        return Response(response=json.dumps(response), status=400)

    if default_cloud:
        _default_cloud = CloudDao.get_cloud(default_cloud)
        if not _default_cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Default Cloud not found: {default_cloud}",
            }
            return Response(response=json.dumps(response), status=400)

    else:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: default_cloud",
        }
        return Response(response=json.dumps(response), status=400)

    _host_obj = Host(
        name=hostname,
        model=model.upper(),
        host_type=host_type,
        default_cloud=_default_cloud,
    )
    db.session.add(_host_obj)
    db.session.commit()
    return jsonify(_host_obj.as_dict())


@host_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_host(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    HostDao.remove_host(_host)
    response = {
        "status_code": 204,
        "message": "Host deleted",
    }
    return Response(response=json.dumps(response), status=204)
