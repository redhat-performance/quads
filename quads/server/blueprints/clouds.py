from flask import Blueprint, jsonify, request
from quads.models import Cloud
from quads.server import app

cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud):
    _cloud = app.session.query(Cloud).filter(Cloud.name == cloud).first()
    return jsonify(_cloud.as_dict())


@cloud_bp.route("/")
def get_clouds():
    _clouds = db_session.query(Cloud).all()
    return jsonify([_cloud.as_dict() for _cloud in _clouds])


@cloud_bp.route("/", methods=["POST"])
def create_cloud():
    data = request.get_json()
    cloud_name = data.get("name")

    if not cloud_name:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: name"}),
            400,
        )

    _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
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
    db_session.add(_cloud_obj)
    db_session.commit()
    return jsonify(_cloud_obj.as_dict()), 201
