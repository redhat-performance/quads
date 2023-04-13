import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.dao.memory import MemoryDao
from quads.server.models import db, Memory

memory_bp = Blueprint("memory", __name__)


@memory_bp.route("/")
def get_all_memory() -> Response:
    _memories = MemoryDao.get_memories()
    return jsonify([_memory.as_dict() for _memory in _memories])


@memory_bp.route("/<hostname>")
def get_memory(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    return jsonify([_memory.as_dict() for _memory in _host.memory])


@memory_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_memory(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    data = request.get_json()

    handle = data.get("handle")
    size_gb = data.get("size_gb")

    if not handle:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: handle",
        }
        return Response(response=json.dumps(response), status=400)

    memories = MemoryDao.get_memory_for_host(_host.id)
    if any(memory.handle == handle for memory in memories):
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Memory with this handle ({handle}) already exists for this host.",
        }
        return Response(response=json.dumps(response), status=400)

    if not size_gb:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: size_gb",
        }
        return Response(response=json.dumps(response), status=400)

    if size_gb <= 0:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Argument can't be negative or zero: size_gb",
        }
        return Response(response=json.dumps(response), status=400)

    _memory_obj = Memory(handle=handle, size_gb=size_gb, host_id=_host.id)
    db.session.add(_memory_obj)
    db.session.commit()
    return jsonify(_memory_obj.as_dict())


@memory_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_memory(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    data = request.get_json()

    memory_id = data.get("id")
    if not memory_id:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: id",
        }
        return Response(response=json.dumps(response), status=400)

    _memory_obj = MemoryDao.get_memory(memory_id)
    if not _memory_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Memory not found: {memory_id}",
        }
        return Response(response=json.dumps(response), status=400)

    db.session.delete(_memory_obj)
    db.session.commit()
    response = {
        "status_code": 204,
        "message": "Memory deleted",
    }
    return Response(response=json.dumps(response), status=204)
