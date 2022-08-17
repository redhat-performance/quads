from flask import Blueprint, jsonify, request
from quads.models import Cloud
from quads.server import app
from quads.server.app import check_access

cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud):
    _cloud = app.session.query(Cloud).filter(Cloud.name == cloud).first()
    return jsonify(_cloud.as_dict())


@cloud_bp.route("/")
def get_clouds():
    _clouds = app.session.query(Cloud).all()
    return jsonify([_cloud.as_dict() for _cloud in _clouds])


@cloud_bp.route("/", methods=["POST"])
@check_access("admin")
def create_cloud():
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _cloud = app.session.query(Cloud).filter(Cloud.name == cloud_name).first()
    if _cloud:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Cloud {cloud_name} already exists",
                }
            ),
            400,
        )

    _cloud_obj = Cloud(name=cloud_name)
    app.session.add(_cloud_obj)
    app.session.commit()
    return jsonify(_cloud_obj.as_dict()), 201


@cloud_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_cloud():
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _cloud = app.session.query(Cloud).filter(Cloud.name == cloud_name).first()
    if not _cloud:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Cloud {cloud_name} not found",
                }
            ),
            400,
        )

    app.session.delete(_cloud)
    app.session.commit()
    return (
        jsonify(
            {
                "message": f"Cloud {cloud_name} deleted",
            }
        ),
        201,
    )
