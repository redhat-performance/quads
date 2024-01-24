import json
from datetime import datetime

from flask import Blueprint, jsonify, request, Response, make_response
from quads.server.blueprints import check_access
from quads.server.dao.baseDao import EntryNotFound, InvalidArgument
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao

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
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud not found: {cloud}",
        }
        return make_response(jsonify(response), 400)
    return jsonify(_cloud.as_dict())


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
                "message": str(ex),
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
    cloud_name = data.get("cloud")
    if not cloud_name:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: cloud",
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


@cloud_bp.route("/summary/")
def get_summary() -> Response:
    """
    Gets a cloud summary.

    :param date: str: A date in the past for a time-bound summary
    :return: A response object with a 200 status code
    """

    data = request.args.to_dict()
    _date = data.get("date")
    clouds_summary = []
    total_count = 0
    _clouds = CloudDao.get_clouds()
    schedules = None
    for _cloud in _clouds:
        if _cloud.name == "cloud01":
            hosts = HostDao.filter_hosts(cloud=_cloud, retired=False, broken=False)
            count = len(hosts)
        else:
            date = datetime.strptime(_date, "%Y-%m-%dT%H:%M") if _date else datetime.now()
            schedules = ScheduleDao.get_current_schedule(cloud=_cloud, date=date)
            count = len(schedules)
            total_count += count

        clouds_summary.append(
            {
                "name": _cloud.name,
                "count": count,
                "description": schedules[0].assignment.description if schedules else "",
                "owner": schedules[0].assignment.owner if schedules else "",
                "ticket": schedules[0].assignment.ticket if schedules else "",
                "ccuser": schedules[0].assignment.ccuser if schedules else "",
                "provisioned": schedules[0].assignment.provisioned if schedules else False,
                "validated": schedules[0].assignment.validated if schedules else False,
            }
        )

    return jsonify(clouds_summary)
