from flask import Blueprint, jsonify, request, Response, make_response
from quads.server.dao.schedule import ScheduleDao

from quads.config import Config

from quads.server.blueprints import check_access
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import EntryNotFound, InvalidArgument, BaseDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import Assignment
from sqlalchemy import inspect

assignment_bp = Blueprint("assignments", __name__)


@assignment_bp.route("/")
def get_assignments() -> Response:
    """
    Returns a list of all assignments in the database.
        ---
        tags:
          - Assignment API

    :return: A list of all assignments in the database
    """
    if request.args:
        try:
            _assignments = AssignmentDao.filter_assignments(request.args)
        except (EntryNotFound, InvalidArgument) as ex:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": str(ex),
            }
            return make_response(jsonify(response), 400)

    else:
        _assignments = AssignmentDao.get_assignments()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@assignment_bp.route("/<assignment_id>/")
def get_assignment(assignment_id: str) -> Response:
    """
    Used to retrieve a single assignment from the database.
        It takes in an assignment_id as a parameter and returns the corresponding Assignment object.
        If no such Assignment exists, it will return a 400 Bad Request error.
        ---
        tags:
          - Assignment API

    :param assignment_id: Get the assignment from the database
    :return: The assignment as a json object
    """
    _assignment = AssignmentDao.get_assignment(int(assignment_id))
    if not _assignment:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Assignment not found: {assignment_id}",
        }
        return make_response(jsonify(response), 400)
    return jsonify(_assignment.as_dict())


@assignment_bp.route("/active/<cloud_name>/")
def get_active_cloud_assignment(cloud_name: str) -> Response:
    """
    Returns the active assignment for a given cloud.
        ---
        tags:
          - Assignment API

    :param cloud_name: Find the cloud in the database
    :return: The active assignment for the cloud
    """
    _cloud = CloudDao.get_cloud(cloud_name)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud not found: {cloud_name}",
        }
        return make_response(jsonify(response), 400)
    _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
    response = {}
    if _assignment:
        response = _assignment.as_dict()
    return jsonify(response)


@assignment_bp.route("/active/")
def get_active_assignments() -> Response:
    """
    Returns all active assignments.
        ---
        tags:
          - Assignment API

    :return: A list of all active assignments
    """
    _assignments = AssignmentDao.get_active_assignments()
    response = []
    if _assignments:
        for _ass in _assignments:
            response.append(_ass.as_dict())
    return jsonify(response)


@assignment_bp.route("/", methods=["POST"])
@check_access(["admin"])
def create_assignment() -> Response:
    """
    Creates a new assignment in the database.
        ---
        tags:
          - API

    :return: The created object as a json
    """
    data = request.get_json()

    _cloud = None
    _vlan = None
    cloud_name = data.get("cloud")
    vlan = data.get("vlan")
    description = data.get("description")
    owner = data.get("owner")
    ticket = data.get("ticket")
    qinq = data.get("qinq")
    wipe = data.get("wipe")
    cc_user = data.get("cc_user")

    required_fields = [
        "description",
        "owner",
        "ticket",
        "cloud",
    ]
    for field in required_fields:
        if not data.get(field):
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {field}",
            }
            return make_response(jsonify(response), 400)

    if cc_user:
        cc_user = cc_user.split(",")

    if cloud_name:
        _cloud = CloudDao.get_cloud(cloud_name)
        if not _cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud not found: {cloud_name}",
            }
            return make_response(jsonify(response), 400)
        _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
        if _assignment:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"There is an already active assignment for {cloud_name}",
            }
            return make_response(jsonify(response), 400)

    if vlan:
        _vlan = VlanDao.get_vlan(int(vlan))
        if not _vlan:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan not found: {vlan}",
            }
            return make_response(jsonify(response), 400)

    kwargs = {
        "description": description,
        "owner": owner,
        "ticket": ticket,
        "qinq": qinq,
        "wipe": wipe,
        "ccuser": cc_user,
        "cloud": cloud_name,
    }
    if _vlan:
        kwargs["vlan_id"] = int(vlan)
    _assignment_obj = AssignmentDao.create_assignment(**kwargs)
    return jsonify(_assignment_obj.as_dict())


@assignment_bp.route("/self/", methods=["POST"])
@check_access(["user"])
def create_self_assignment() -> Response:
    """
    Creates a new self assignment in the database.
        ---
        tags:
          - API

    :return: The created object as a json
    """
    data = request.get_json()

    _cloud = None
    _vlan = None
    cloud_name = data.get("cloud")
    vlan = data.get("vlan")
    description = data.get("description")
    owner = data.get("owner")
    ticket = data.get("ticket")
    qinq = data.get("qinq")
    wipe = data.get("wipe")
    cc_user = data.get("cc_user")

    required_fields = [
        "description",
        "owner",
    ]

    for field in required_fields:
        if not data.get(field):
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {field}",
            }
            return make_response(jsonify(response), 400)

    if cc_user:
        cc_user = cc_user.split(",")

    if cloud_name:
        _cloud = CloudDao.get_cloud(cloud_name)
        if not _cloud:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Cloud not found: {cloud_name}",
            }
            return make_response(jsonify(response), 400)
        _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
        if _assignment:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"There is an already active assignment for {cloud_name}",
            }
            return make_response(jsonify(response), 400)
    else:

        _clouds = CloudDao.get_clouds()
        _clouds = [_c for _c in _clouds if _c.name != Config["spare_pool_name"]]
        _free_clouds = []
        for cloud in _clouds:
            _future_sched = ScheduleDao.get_future_schedules(cloud=cloud)
            _active_ass = AssignmentDao.get_active_cloud_assignment(cloud)
            if len(_future_sched) or _active_ass:
                continue
            else:
                _free_clouds.append(cloud)

        if not _free_clouds:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": "No free clouds available",
            }
            return make_response(jsonify(response), 400)
        _cloud = _free_clouds[0]

    if vlan:
        _vlan = VlanDao.get_vlan(int(vlan))
        if not _vlan:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan not found: {vlan}",
            }
            return make_response(jsonify(response), 400)

    kwargs = {
        "description": description,
        "owner": owner,
        "ticket": ticket,
        "qinq": qinq,
        "wipe": wipe,
        "ccuser": cc_user,
        "is_self_schedule": True,
        "cloud": _cloud.name,
    }
    if _vlan:
        kwargs["vlan_id"] = int(vlan)
    _assignment_obj = AssignmentDao.create_assignment(**kwargs)
    return jsonify(_assignment_obj.as_dict())


@assignment_bp.route("/<assignment_id>/", methods=["PATCH"])
@check_access(["admin"])
def update_assignment(assignment_id: str) -> Response:
    """
    Updates an existing assignment.
        ---
        tags: API
        parameters:
          - in: path
            name: assignment_id  # The id of the assignment to update. This is a required parameter.
                It must be passed as part of the URL path, not as a query string or request body parameter.
                Example usage would be /api/v3/assignments/&lt;assignment_id&gt; where &lt;assignment_id&gt;
                is replaced with the actual value for that field (e.g., /api/v3/assignments/12345). Note that

    :param assignment_id: str: Identify which assignment to update
    :return: A json object containing the updated assignment
    """
    data = request.get_json()
    assignment_obj = AssignmentDao.get_assignment(int(assignment_id))
    if not assignment_obj:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Assignment not found: {assignment_id}",
        }
        return make_response(jsonify(response), 400)

    obj_attrs = inspect(Assignment).mapper.attrs
    update_fields = {}
    for attr in obj_attrs:
        value = data.get(attr.key)
        if value is not None:
            if attr.key == "ccuser":
                value = value.split(",")
                value = [user.strip() for user in value]
            if attr.key == "cloud":
                _cloud = CloudDao.get_cloud(value)
                if not _cloud:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Cloud not found: {value}",
                    }
                    return make_response(jsonify(response), 400)
                value = _cloud
            if attr.key == "vlan":
                _vlan = VlanDao.get_vlan(value)
                if not _vlan:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Vlan not found: {value}",
                    }
                    return make_response(jsonify(response), 400)
                value = _vlan
            if type(value) is str:
                if value.lower() in ["true", "false"]:
                    value = eval(value.lower().capitalize())
            update_fields[attr.key] = value
    for key, value in update_fields.items():
        setattr(assignment_obj, key, value)

    BaseDao.safe_commit()
    return jsonify(assignment_obj.as_dict())


@assignment_bp.route("/", methods=["DELETE"])
@check_access(["admin"])
def delete_assignment() -> Response:
    """
    Used to delete an assignment from the database.
    It takes in a JSON object with one key, &quot;id&quot;, which corresponds to the id of the assignment that
    will be deleted.
    If no such assignment exists, it returns a 400 error code and message explaining that there was no such entry
    found.
    Otherwise, it deletes the entry and returns a 204 status code.

    :return: A response with a status code of 204
    """
    data = request.get_json()
    assignment_id = data.get("id")
    if not assignment_id:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: id",
        }
        return make_response(jsonify(response), 400)

    try:
        AssignmentDao.delete_assignment(assignment_id)
    except EntryNotFound:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Assignment not found: {assignment_id}",
        }
        return make_response(jsonify(response), 400)
    response = {
        "status_code": 200,
        "message": "Assignment deleted",
    }
    return jsonify(response)
