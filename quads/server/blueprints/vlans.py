from flask import Blueprint, jsonify, request
from quads.server.models import Vlan, db

vlan_bp = Blueprint("vlans", __name__)


@vlan_bp.route("/")
def get_vlans():
    _vlans = db.session.query(Vlan).all()
    return jsonify([_vlan.as_dict() for _vlan in _vlans])


@vlan_bp.route("/", methods=["POST"])
# @check_access("admin")
def create_vlan():
    data = request.get_json()
    gateway = data.get("gateway")
    ip_free = data.get("ip_free")
    ip_range = data.get("ip_range")
    netmask = data.get("netmask")
    vlan_id = data.get("vlan_id")

    _vlan = db.session.query(Vlan).filter(Vlan.vlan_id == vlan_id).first()
    if _vlan:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Vlan {vlan_id} already exists",
                }
            ),
            400,
        )

    _vlan_obj = Vlan(
        gateway=gateway,
        ip_free=ip_free,
        ip_range=ip_range,
        netmask=netmask,
        vlan_id=vlan_id,
    )
    db.session.add(_vlan_obj)
    db.session.commit()
    return jsonify(_vlan_obj.as_dict()), 201


@vlan_bp.route("/", methods=["DELETE"])
def delete_vlan():
    data = request.get_json()

    vlan_id = data.get("id")
    _vlan_obj = db.session.query(Vlan).filter(Vlan.id == vlan_id).first()
    if not _vlan_obj:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Vlan not found: {vlan_id}",
                }
            ),
            400,
        )
    db.session.delete(_vlan_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Vlan deleted",
            }
        ),
        201,
    )
