from flask import Blueprint, jsonify
from quads.models import Vlan
from quads.server import app

vlan_bp = Blueprint("vlans", __name__)


@vlan_bp.route("/")
def get_vlans():
    _vlans = app.session.query(Vlan).all()
    return jsonify([_vlan.as_dict() for _vlan in _vlans])
