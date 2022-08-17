from flask import Blueprint, jsonify, request
from quads.server.models import Host, db, Processor

processor_bp = Blueprint("processor", __name__)


@processor_bp.route("/<hostname>")
def get_processors(hostname):
    _host = db.session.query(Host).filter(Host.name == hostname).first()
    return jsonify([_processor.as_dict() for _processor in _host.processors])


@processor_bp.route("/<hostname>", methods=["POST"])
def create_processor(hostname):
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
    vendor = data.get("vendor")
    product = data.get("product")
    cores = data.get("cores")
    threads = data.get("threads")

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
    return jsonify(_processor_obj.as_dict()), 201


@processor_bp.route("/<hostname>", methods=["DELETE"])
def delete_processor(hostname):
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

    processor_id = data.get("id")
    _processor_obj = (
        db.session.query(Processor).filter(Processor.id == processor_id).first()
    )

    db.session.delete(_processor_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Processor deleted",
            }
        ),
        201,
    )
