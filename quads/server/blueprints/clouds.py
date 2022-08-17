from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.cloud import CloudDao
from quads.server.models import Cloud, db


cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud):
    _cloud = CloudDao.get_cloud(cloud)
    return jsonify(_cloud.as_dict())


@cloud_bp.route("/")
def get_clouds():
    _clouds = CloudDao.get_clouds()
    return jsonify([_cloud.as_dict() for _cloud in _clouds])


@cloud_bp.route("/", methods=["POST"])
@check_access("admin")
def create_cloud() -> Response:
    data = request.get_json()
    cloud_name = data.get("name")
    if not cloud_name:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: name",
            }
        )

    _cloud = db.session.query(Cloud).filter(Cloud.name == cloud_name).first()
    if _cloud:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud {cloud_name} already exists",
            }
        )

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
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": "Missing argument: name",
            }
        )

    _cloud = db.session.query(Cloud).filter(Cloud.name == cloud_name).first()
    if not _cloud:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud {cloud_name} not found",
            }
        )

    db.session.delete(_cloud)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Cloud {cloud_name} deleted",
        }
    )
