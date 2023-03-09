import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.cloud import CloudDao
from quads.server.models import Cloud, db


cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud: str) -> Response:
    _cloud = CloudDao.get_cloud(cloud)
    return jsonify(_cloud.as_dict() if _cloud else {})


@cloud_bp.route("/")
def get_clouds() -> Response:
    _clouds = CloudDao.get_clouds()
    return jsonify([_cloud.as_dict() for _cloud in _clouds] if _clouds else {})


@cloud_bp.route("/", methods=["POST"])
@check_access("admin")
def create_cloud() -> Response:
    data = request.get_json()
    cloud_name = data.get("name")
    if not cloud_name:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: name",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud = CloudDao.get_cloud(cloud_name)
    if _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud {cloud_name} already exists",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud_obj = Cloud(name=cloud_name)
    db.session.add(_cloud_obj)
    db.session.commit()
    return jsonify(_cloud_obj.as_dict())


@cloud_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_cloud() -> Response:
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: name",
        }
        return Response(response=json.dumps(response), status=400)

    _cloud = CloudDao.get_cloud(cloud_name)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud not found: {cloud_name}",
        }
        return Response(response=json.dumps(response), status=400)
    db.session.delete(_cloud)
    db.session.commit()
    response = {
        "status_code": 201,
        "message": f"Cloud {cloud_name} deleted",
    }
    return Response(response=json.dumps(response), status=201)
