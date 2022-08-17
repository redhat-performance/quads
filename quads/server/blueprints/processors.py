from flask import Blueprint, jsonify
from quads.models import Host
from quads.server.app import db_session

processor_bp = Blueprint("processor", __name__)


@processor_bp.route("/<hostname>")
def get_processors(hostname):
    _host = db_session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_processor.as_dict() for _processor in _host.processors])
