import json

from flask import Blueprint, jsonify, request, Response, make_response
from quads.server.blueprints import check_access
from quads.server.dao.baseDao import EntryNotFound, InvalidArgument
from quads.server.dao.cloud import CloudDao

cloud_bp = Blueprint("clouds", __name__)


@cloud_bp.route("/<cloud>/")
def get_cloud(cloud: str) -> Response:
    """
    GET request that returns the cloud with the given name.
        ---
        tags:
          - API

    :param cloud: str: Specify the cloud name
    :return: A response object that contains the json representation of the cloud
    """
    _cloud = CloudDao.get_cloud(cloud)
    return jsonify(_cloud.as_dict() if _cloud else {})


@cloud_bp.route("/")
def get_clouds() -> Response:
    """
    Returns a list of all clouds in the database.
        ---
        tags:
          - API

    :return: The list of clouds
    """
    if request.args:
        try:
            _clouds = CloudDao.filter_clouds_dict(request.args)
        except (EntryNotFound, InvalidArgument) as ex:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": ex,
            }
            return make_response(jsonify(response), 400)

    else:
        _clouds = CloudDao.get_clouds()
    return jsonify([_cloud.as_dict() for _cloud in _clouds] if _clouds else {})


@cloud_bp.route("/", methods=["POST"])
@check_access("admin")
def create_cloud() -> Response:
    """
    Creates a new cloud in the database.
        ---
        tags:
          - API

    :return: A response object with the created cloud
    """
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

    _cloud_obj = CloudDao.create_cloud(cloud_name)
    return jsonify(_cloud_obj.as_dict())


@cloud_bp.route("/<cloud>/", methods=["DELETE"])
@check_access("admin")
def delete_cloud(cloud: str) -> Response:
    """
    Deletes a cloud from the database.
        Args:
            cloud (str): The name of the cloud to delete.

    :param cloud: str: Specify the name of the cloud to be deleted
    :return: A response object with a 204 status code
    """

    _cloud = CloudDao.get_cloud(cloud)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud not found: {cloud}",
        }
        return make_response(jsonify(response), 400)
    CloudDao.remove_cloud(cloud)
    response = {
        "status_code": 200,
        "message": f"Cloud {cloud} deleted",
    }
    return jsonify(response)
