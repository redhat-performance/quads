from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.models import Vlan, db

vlan_bp = Blueprint("vlans", __name__)


@vlan_bp.route("/<vlan_id>")
def get_vlan(vlan_id) -> Response:
    _vlan = db.session.query(Vlan).filter(Vlan.vlan_id == vlan_id).first()
    if not _vlan:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan {vlan_id} does not exists",
            }
        )
    return jsonify(_vlan.as_dict())


@vlan_bp.route("/")
def get_vlans() -> Response:
    _vlans = db.session.query(Vlan).all()
    return jsonify([_vlan.as_dict() for _vlan in _vlans])


@vlan_bp.route("/", methods=["POST"])
@check_access("admin")
def create_vlan() -> Response:
    data = request.get_json()
    gateway = data.get("gateway")
    ip_free = data.get("ip_free")
    ip_range = data.get("ip_range")
    netmask = data.get("netmask")
    vlan_id = data.get("vlan_id")

    required_fields = [
        "gateway",
        "ip_free",
        "ip_range",
        "netmask",
        "vlan_id",
    ]
    for field in required_fields:
        if not data.get(field):
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Missing argument: {field}",
                }
            )

    _vlan = db.session.query(Vlan).filter(Vlan.vlan_id == vlan_id).first()
    if _vlan:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan {vlan_id} already exists",
            }
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
    return jsonify(_vlan_obj.as_dict())


@vlan_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_vlan() -> Response:
    data = request.get_json()

    vlan_id = data.get("id")
    _vlan_obj = db.session.query(Vlan).filter(Vlan.id == vlan_id).first()
    if not _vlan_obj:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan not found: {vlan_id}",
            }
        )

    db.session.delete(_vlan_obj)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Vlan deleted",
        }
    )
