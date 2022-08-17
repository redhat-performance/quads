from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.models import Host, db, Disk


disk_bp = Blueprint("disks", __name__)


@disk_bp.route("/<hostname>")
def get_disks(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host {hostname} does not exists",
            }
        )
    return jsonify([_disks.as_dict() for _disks in _host.disks])


@disk_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_disks(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host not found: {hostname}",
            }
        )

    data = request.get_json()

    disk_type = data.get("disk_type")
    size_gb = data.get("size_gb")
    count = data.get("count")

    if not disk_type:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: disk_type",
            }
        )

    if not size_gb:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: size_gb",
            }
        )

    if not count:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: count",
            }
        )

    _disk_obj = Disk(
        disk_type=disk_type, size_gb=size_gb, count=count, host_id=_host.id
    )
    db.session.add(_disk_obj)
    db.session.commit()
    return jsonify(_disk_obj.as_dict())


@disk_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_disks(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host not found: {hostname}",
            }
        )

    data = request.get_json()

    disk_id = data.get("id")
    _disk_obj = db.session.query(Disk).filter(Disk.id == disk_id).first()

    db.session.delete(_disk_obj)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Disk deleted",
        }
    )
