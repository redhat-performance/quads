import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.dao.processor import ProcessorDao
from quads.server.models import db, Processor

processor_bp = Blueprint("processor", __name__)


@processor_bp.route("/<hostname>")
def get_processors(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host {hostname} does not exists",
        }
        return Response(response=json.dumps(response), status=400)

    return jsonify([_processor.as_dict() for _processor in _host.processors])


@processor_bp.route("/<hostname>", methods=["POST"])
@check_access("admin")
def create_processor(hostname: str) -> Response:
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
    vendor = data.get("vendor")
    product = data.get("product")
    cores = data.get("cores")
    threads = data.get("threads")
    required_fields = [
        "handle",
        "vendor",
        "product",
        "cores",
        "threads",
    ]
    for field in required_fields:
        if not data.get(field):
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {field}",
            }
            return Response(response=json.dumps(response), status=400)

    _processor_obj = Processor(
        handle=handle,
        vendor=vendor,
        product=product,
        cores=cores,
        threads=threads,
        host_id=_host.id,
    )
    db.session.add(_processor_obj)
    db.session.commit()
    return jsonify(_processor_obj.as_dict())


@processor_bp.route("/<hostname>", methods=["DELETE"])
@check_access("admin")
def delete_processor(hostname: str) -> Response:
    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return Response(response=json.dumps(response), status=400)

    data = request.get_json()

    processor_id = data.get("id")
    _processor_obj = ProcessorDao.get_processor(processor_id)
    if not _processor_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Processor not found: {processor_id}",
        }
        return Response(response=json.dumps(response), status=400)

    db.session.delete(_processor_obj)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": "Processor deleted",
        }
    )
