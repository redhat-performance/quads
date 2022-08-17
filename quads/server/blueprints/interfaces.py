from flask import Blueprint, jsonify, request
from quads.server.models import Interface, Host, db

interface_bp = Blueprint("interfaces", __name__)


@interface_bp.route("/<hostname>")
def get_interfaces(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_interface.as_dict() for _interface in _host.interfaces])


@interface_bp.route("/<hostname>", methods=["POST"])
def create_interface(hostname):
    data = request.get_json()

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
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
    )
    _host.interfaces.append(_interface_obj)
    db.session.add(_host)
    db.session.commit()
    return jsonify(_interface_obj.as_dict()), 201


@interface_bp.route("/<hostname>", methods=["DELETE"])
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

    interface_id = data.get("id")
    _interface_obj = (
        db.session.query(Interface).filter(Interface.id == interface_id).first()
    )

    db.session.delete(_interface_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Interface deleted",
            }
        ),
        201,
    )
