from flask import Blueprint, jsonify
from quads.models import Vlan
from quads.server.app import db_session

vlan_bp = Blueprint("vlans", __name__)


@vlan_bp.route("/")
def get_vlans():
    _vlans = db_session.query(Vlan).all()
    return jsonify([_vlan.as_dict() for _vlan in _vlans])
