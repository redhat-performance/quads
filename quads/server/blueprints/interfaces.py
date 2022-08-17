from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.models import Interface, Host, db

interface_bp = Blueprint("interfaces", __name__)


@interface_bp.route("/<hostname>")
def get_interfaces(hostname) -> Response:
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host {hostname} does not exists",
            }
        )
    return jsonify([_interface.as_dict() for _interface in _host.interfaces])


@interface_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_interface(hostname) -> Response:
    data = request.get_json()

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Host {hostname} does not exists",
            }
        )

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
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Missing argument: {key}",
                }
            )

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


@interface_bp.route("/<hostname>", methods=["DELETE"])
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

    interface_id = data.get("id")
    _interface_obj = (
        db.session.query(Interface).filter(Interface.id == interface_id).first()
    )

    db.session.delete(_interface_obj)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Interface deleted",
        }
    )
