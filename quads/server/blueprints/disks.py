from flask import Blueprint, jsonify, request
from quads.server.models import Host, db, Disk

# from quads.server import app

disk_bp = Blueprint("disks", __name__)


@disk_bp.route("/<hostname>")
def get_disks(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_disks.as_dict() for _disks in _host.disks])


@disk_bp.route("/<hostname>", methods=["POST"])
def create_disks(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Host not found: {hostname}",
                }
            ),
            400,
        )

    data = request.get_json()

    disk_type = data.get("disk_type")
    size_gb = data.get("size_gb")
    count = data.get("count")

    _disk_obj = Disk(
        disk_type=disk_type, size_gb=size_gb, count=count, host_id=_host.id
    )
    db.session.add(_disk_obj)
    db.session.commit()
    return jsonify(_disk_obj.as_dict()), 201


@disk_bp.route("/<hostname>", methods=["DELETE"])
def delete_disks(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Host not found: {hostname}",
                }
            ),
            400,
        )

    data = request.get_json()

    disk_id = data.get("id")
    _disk_obj = db.session.query(Disk).filter(Disk.id == disk_id).first()

    db.session.delete(_disk_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Disk deleted",
            }
        ),
        201,
    )
