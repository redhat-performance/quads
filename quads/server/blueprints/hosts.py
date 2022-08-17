from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.models import Host, Cloud, db


host_bp = Blueprint("hosts", __name__)


@host_bp.route("/")
def get_hosts() -> Response:
    _hosts = HostDao.get_hosts()
    return jsonify([_host.as_dict() for _host in _hosts])


@host_bp.route("/<hostname>/")
@check_access("admin")
def get_host(hostname) -> Response:
    _host = HostDao.get_host(hostname)
    return jsonify(_host.as_dict())


@host_bp.route("/", methods=["PUT"])
@check_access("admin")
def update_host() -> Response:
    data = request.get_json()
    cloud_name = data.get("cloud")
    hostname = data.get("name")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: name",
            }
        )

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host {hostname} not found",
            }
        )

    if default_cloud:
        _default_cloud = (
            db.session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Default Cloud not found: {default_cloud}",
                }
            )
        else:
            _host.default_cloud = _default_cloud
    else:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: default_cloud",
            }
        )

    if cloud_name:
        _cloud = db.session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Cloud not found: {cloud_name}",
                }
            )
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
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: name",
            }
        )

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host {hostname} already exists",
            }
        )

    if not host_type:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: host_type",
            }
        )

    if default_cloud:
        _default_cloud = (
            db.session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Default Cloud not found: {default_cloud}",
                }
            )
    else:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: default_cloud",
            }
        )

    _cloud = _default_cloud

    if cloud_name:
        _cloud = db.session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Cloud not found: {cloud_name}",
                }
            )

    _host_obj = Host(
        name=hostname, host_type=host_type, cloud=_cloud, default_cloud=_default_cloud
    )
    db.session.add(_host_obj)
    db.session.commit()
    return jsonify(_host_obj.as_dict())


@host_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_host(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host not found: {hostname}",
            }
        )

    db.session.delete(_host)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Host deleted",
        }
    )
