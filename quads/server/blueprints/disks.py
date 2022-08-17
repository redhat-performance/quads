from flask import Blueprint, jsonify
from quads.models import Host
from quads.server import app

disk_bp = Blueprint("disks", __name__)


@disk_bp.route("/<hostname>")
def get_disks(hostname):
    _host = app.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_disks.as_dict() for _disks in _host.disks])
