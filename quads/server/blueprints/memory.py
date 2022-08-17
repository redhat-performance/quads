from flask import Blueprint, jsonify, request

from quads.server.blueprints import check_access
from quads.server.models import Host, db, Memory

memory_bp = Blueprint("memory", __name__)


@memory_bp.route("/<hostname>")
def get_memory(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_memory.as_dict() for _memory in _host.memory])


@memory_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_memory(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Host not found: {hostname}",
                }
            ),
            400,
        )

    data = request.get_json()

    handle = data.get("handle")
    size_gb = data.get("size_gb")

    _memory_obj = Memory(handle=handle, size_gb=size_gb, host_id=_host.id)
    db.session.add(_memory_obj)
    db.session.commit()
    return jsonify(_memory_obj.as_dict()), 201


@memory_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_memory(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Host not found: {hostname}",
                }
            ),
            400,
        )

    data = request.get_json()

    memory_id = data.get("id")
    _memory_obj = db.session.query(Memory).filter(Memory.id == memory_id).first()

    db.session.delete(_memory_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Memory deleted",
            }
        ),
        201,
    )
