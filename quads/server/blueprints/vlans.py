import json

from flask import Blueprint, jsonify, request, Response, make_response

from quads.server.blueprints import check_access
from quads.server.dao.vlan import VlanDao
from quads.server.models import Vlan, db

vlan_bp = Blueprint("vlans", __name__)


@vlan_bp.route("/<vlan_id>")
def get_vlan(vlan_id: str) -> Response:
    _vlan = VlanDao.get_vlan(vlan_id)
    if not _vlan:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Vlan not found: {vlan_id}",
        }
        return make_response(jsonify(response), 400)

    return jsonify(_vlan.as_dict())


@vlan_bp.route("/")
def get_vlans() -> Response:
    _vlans = VlanDao.get_vlans()
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
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {field}",
            }
            return make_response(jsonify(response), 400)

    _vlan = VlanDao.get_vlan(vlan_id)
    if _vlan:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Vlan {vlan_id} already exists",
        }
        return make_response(jsonify(response), 400)

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
    if not vlan_id:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Missing argument: id",
        }
        return make_response(jsonify(response), 400)

    _vlan_obj = VlanDao.get_vlan(vlan_id)
    if not _vlan_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Vlan not found: {vlan_id}",
        }
        return make_response(jsonify(response), 400)

    db.session.delete(_vlan_obj)
    db.session.commit()
    response = {
        "status_code": 200,
        "message": "Vlan deleted",
    }
    return jsonify(response)
