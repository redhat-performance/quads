from flask import Blueprint, jsonify, request
from quads.models import Host, Cloud
from quads.server.app import check_access
from quads.server import app

host_bp = Blueprint("hosts", __name__)


@host_bp.route("/")
def get_hosts():
    _hosts = app.session.query(Host).all()
    return jsonify([_host.as_dict() for _host in _hosts])


@host_bp.route("/<hostname>/")
@check_access("admin")
def get_host(hostname):
    _host = app.session.query(Host).filter(Host.name == hostname).first()
    return jsonify(_host.as_dict())


@host_bp.route("/", methods=["PUT"])
def update_host():
    data = request.get_json()
    cloud_name = data.get("cloud")
    hostname = data.get("name")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _host = app.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify({"error": "Bad Request", "message": f"Host {hostname} not found"}),
            400,
        )

    if default_cloud:
        _default_cloud = (
            app.session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Default Cloud not found: {default_cloud}",
                    }
                ),
                400,
            )
        else:
            _host.default_cloud = _default_cloud
    else:
        return (
            jsonify(
                {"error": "Bad Request", "message": "Missing argument: default_cloud"}
            ),
            400,
        )

    if cloud_name:
        _cloud = app.session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )
        else:
            _host.cloud = _cloud

    if host_type:
        _host.host_type = host_type

    app.session.commit()

    return jsonify(_host.as_dict()), 200


@host_bp.route("/", methods=["POST"])
def create_host():
    data = request.get_json()
    cloud_name = data.get("cloud")
    hostname = data.get("name")
    default_cloud = data.get("default_cloud")
    host_type = data.get("host_type")

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _host = app.session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
        )

    if not host_type:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: host_type"}),
            400,
        )

    if default_cloud:
        _default_cloud = (
            app.session.query(Cloud).filter(Cloud.name == default_cloud).first()
        )
        if not _default_cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Default Cloud not found: {default_cloud}",
                    }
                ),
                400,
            )
    else:
        return (
            jsonify(
                {"error": "Bad Request", "message": "Missing argument: default_cloud"}
            ),
            400,
        )

    _cloud = _default_cloud

    if cloud_name:
        _cloud = app.session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )

    _host_obj = Host(
        name=hostname, host_type=host_type, cloud=_cloud, default_cloud=_default_cloud
    )
    app.session.add(_host_obj)
    app.session.commit()
    return jsonify(_host_obj.as_dict()), 201
