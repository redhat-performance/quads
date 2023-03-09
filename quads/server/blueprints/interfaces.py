import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.models import Interface, Host, db

interface_bp = Blueprint("interfaces", __name__)


@interface_bp.route("/<hostname>")
def get_interfaces(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    return jsonify([_interface.as_dict() for _interface in _host.interfaces])


@interface_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_interface(hostname: str) -> Response:
    data = request.get_json()

    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    name = data.get("name")
    bios_id = data.get("bios_id")
    mac_address = data.get("mac_address")
    switch_ip = data.get("switch_ip")
    switch_port = data.get("switch_port")
    speed = data.get("speed")
    vendor = data.get("vendor")
    pxe_boot = data.get("pxe_boot")
    maintenance = data.get("maintenance")

    required = [
        "name",
        "bios_id",
        "mac_address",
        "switch_ip",
        "switch_port",
        "speed",
        "vendor",
    ]
    for key in required:
        if not data.get(key):
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {key}",
            }
            return Response(response=json.dumps(response), status=400)

    if not speed > 0:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Argument can't be negative or zero: speed",
        }
        return Response(response=json.dumps(response), status=400)

    _interface_obj = Interface(
        name=name,
        bios_id=bios_id,
        mac_address=mac_address,
        switch_ip=switch_ip,
        switch_port=switch_port,
        speed=speed,
        vendor=vendor,
        pxe_boot=pxe_boot,
        maintenance=maintenance,
        host_id=_host.id,
    )
    db.session.add(_interface_obj)
    db.session.commit()
    return jsonify(_interface_obj.as_dict())


@interface_bp.route("/<hostname>", methods=["PATCH"])
@check_access("admin")
def update_interface(hostname: str) -> Response:
    data = request.get_json()

    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    interface_id = data.get("id")
    if not interface_id:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: id",
        }
        return Response(response=json.dumps(response), status=400)

    interface_obj = InterfaceDao.get_interface(interface_id)
    if not interface_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Interface not found: {interface_id}",
        }
        return Response(response=json.dumps(response), status=400)

    keys = [
        "name",
        "bios_id",
        "mac_address",
        "switch_ip",
        "switch_port",
        "speed",
        "vendor",
        "pxe_boot",
        "maintenance",
    ]
    update_fields = {}
    for key in keys:
        value = data.get(key)
        if value:
            if type(value) == str:
                if value.lower() in ["true", "false"]:
                    value = eval(value.lower().capitalize())
            update_fields[key] = value

    speed = update_fields.get("speed")
    if speed and not speed > 0:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Argument can't be negative or zero: speed",
        }
        return Response(response=json.dumps(response), status=400)

    for key, value in update_fields.items():
        setattr(interface_obj, key, value)
    db.session.commit()
    return jsonify(interface_obj.as_dict())


@interface_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_interface(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    data = request.get_json()

    interface_id = data.get("id")
    if not interface_id:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: id",
        }
        return Response(response=json.dumps(response), status=400)

    _interface_obj = InterfaceDao.get_interface(interface_id)
    if not _interface_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Interface not found: {interface_id}",
        }
        return Response(response=json.dumps(response), status=400)

    db.session.delete(_interface_obj)
    db.session.commit()
    response = {
        "status_code": 201,
        "message": "Interface deleted",
    }
    return Response(response=json.dumps(response), status=201)
