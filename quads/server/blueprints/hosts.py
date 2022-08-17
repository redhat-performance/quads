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
    # TODO: Add filter for child objects
    filter_tuples = []
    operator = "=="
    for k, value in request.args.items():
        fields = k.split(".")
        if len(fields) > 2:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Too many arguments: {fields}",
            }
            return Response(response=json.dumps(response), status=400)

        first_field = fields[0]
        field_name = fields[-1]
        if "__" in k:
            for op in OPERATORS.keys():
                if op in field_name:
                    field_name = field_name[: field_name.index(op)]
                    operator = OPERATORS[op]
                    break

        field = Host.__mapper__.attrs.get(first_field)
        if not field:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"{k} is not a valid field.",
            }
            return Response(response=json.dumps(response), status=400)
        if (
            type(field) != RelationshipProperty
            and type(field.columns[0].type) == Boolean
        ):
            value = value.lower() in ["true", "y", 1, "yes"]
        else:
            if first_field in ["cloud", "default_cloud"]:
                cloud = CloudDao.get_cloud(value)
                if not cloud:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Cloud {value} does not exist.",
                    }
                    return Response(response=json.dumps(response), status=400)
                value = cloud
            if first_field.lower() in MAP_MODEL.keys():
                _field = getattr(Host, first_field)
                if len(fields) > 1:
                    field_name = f"{first_field.lower()}.{field_name.lower()}"
        filter_tuples.append(
            (
                field_name,
                operator,
                value,
            )
        )
    if filter_tuples:
        _hosts = HostDao.create_query_select(Host, filters=filter_tuples)
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
            "message": f"Host {hostname} does not exists",
        }
        return Response(response=json.dumps(response), status=400)
    return jsonify(_host.as_dict())


@host_bp.route("/<hostname>", methods=["PUT"])
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
            "message": f"Host {hostname} not found",
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
    cloud_name = data.get("cloud")
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

    _cloud = _default_cloud

    if cloud_name:
        _cloud = CloudDao.get_cloud(cloud_name)
        if not _cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud not found: {cloud_name}",
            }
            return Response(response=json.dumps(response), status=400)

    _host_obj = Host(
        name=hostname,
        model=model.upper(),
        host_type=host_type,
        cloud=_cloud,
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

    db.session.delete(_host)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Host deleted",
        }
    )
