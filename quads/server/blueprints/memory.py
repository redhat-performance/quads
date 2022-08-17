from flask import Blueprint, jsonify
from quads.models import Host
from quads.server import app

memory_bp = Blueprint("memory", __name__)


@memory_bp.route("/memory/<hostname>")
def get_memory(hostname):
    _host = app.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_memory.as_dict() for _memory in _host.memory])
