from flask import Blueprint, jsonify
from quads.models import Host
from quads.server.app import db_session

disk_bp = Blueprint("disks", __name__)


@disk_bp.route("/<hostname>")
def get_disks(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_disks.as_dict() for _disks in _host.disks])
