from flask import Blueprint, jsonify
from quads.models import Host
from quads.server import app

processor_bp = Blueprint("processor", __name__)


@processor_bp.route("/<hostname>")
def get_processors(hostname):
    _host = app.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_processor.as_dict() for _processor in _host.processors])
