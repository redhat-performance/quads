import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.disk import DiskDao
from quads.server.dao.host import HostDao
from quads.server.models import Disk, db, Host

disk_bp = Blueprint("disks", __name__)


@disk_bp.route("/<hostname>")
def get_disks(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)
    return jsonify([_disks.as_dict() for _disks in _host.disks])


@disk_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_disks(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)
    data = request.get_json()

    disk_type = data.get("disk_type")
    size_gb = data.get("size_gb")
    count = data.get("count")

    if not disk_type:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: disk_type",
        }
        return Response(response=json.dumps(response), status=400)

    if not size_gb:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: size_gb",
        }
        return Response(response=json.dumps(response), status=400)

    if not count:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: count",
        }
        return Response(response=json.dumps(response), status=400)

    if not count > 0:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Argument can't be negative or zero: count",
        }
        return Response(response=json.dumps(response), status=400)

    if size_gb <= 0:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Argument can't be negative or zero: size_gb",
        }
        return Response(response=json.dumps(response), status=400)

    _disk_obj = Disk(
        disk_type=disk_type, size_gb=size_gb, count=count, host_id=_host.id
    )
    db.session.add(_disk_obj)
    db.session.commit()
    return jsonify(_disk_obj.as_dict())


@disk_bp.route("/<hostname>", methods=["PATCH"])
@check_access("admin")
def update_disk(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)
    data = request.get_json()
    disk_id = data.get("disk_id")
    _disk = DiskDao.get_disk(disk_id)
    if not _disk:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Disk not found for {hostname}: {disk_id}",
        }
        return Response(response=json.dumps(response), status=400)
    fields = ["disk_type", "size_gb", "count"]
    for field in fields:
        value = data.get(field)
        if value:
            _disk[field] = value

    db.session.commit()
    return jsonify(_disk.as_dict())


@disk_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_disk(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    data = request.get_json()

    disk_id = data.get("id")
    _disk_obj = DiskDao.get_disk(disk_id)
    if not _disk_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Disk not found: {disk_id}",
        }
        return Response(response=json.dumps(response), status=400)

    db.session.delete(_disk_obj)
    db.session.commit()
    response = {
        "status_code": 200,
        "message": f"Disk deleted",
    }
    return Response(response=json.dumps(response), status=200)
