import json

from flask import Blueprint, jsonify, request, Response

from quads.server.blueprints import check_access
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import EntryNotFound
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import Assignment, Notification, Cloud, Vlan, db

assignment_bp = Blueprint("assignments", __name__)


@assignment_bp.route("/")
def get_assignments() -> Response:
    _assignments = AssignmentDao.get_assignments()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@assignment_bp.route("/<assignment_id>/")
def get_assignment(assignment_id) -> Response:
    _assignment = AssignmentDao.get_assignment(assignment_id)
    if not _assignment:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Assignment {assignment_id} does not exists",
        }
        return Response(response=json.dumps(response), status=400)
    return jsonify(_assignment.as_dict())


@assignment_bp.route("/<cloud_name>/")
def get_active_cloud_assignment(cloud_name) -> Response:
    _cloud = CloudDao.get_cloud(cloud_name)
    _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
    return jsonify(_assignment.as_dict())


@assignment_bp.route("/", methods=["POST"])
@check_access("admin")
def create_assignment() -> Response:
    data = request.get_json()

    notification = Notification()
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
    ]
    for field in required_fields:
        if not data.get(field):
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Missing argument: {field}",
            }
            return Response(response=json.dumps(response), status=400)

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
            return Response(response=json.dumps(response), status=400)
        _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
        if _assignment:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"There is an already active assignment for {cloud_name}",
            }
            return Response(response=json.dumps(response), status=400)

    if vlan:
        _vlan = VlanDao.get_vlan(vlan)
        if not _vlan:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Vlan not found: {vlan}",
            }
            return Response(response=json.dumps(response), status=400)

    _assignment_obj = Assignment(
        description=description,
        owner=owner,
        ticket=ticket,
        qinq=qinq,
        wipe=wipe,
        ccuser=cc_user,
        vlan=_vlan,
        cloud=_cloud,
        notification=notification,
    )
    db.session.add(_assignment_obj)
    db.session.commit()
    return jsonify(_assignment_obj.as_dict())


@assignment_bp.route("/<assignment_id>", methods=["PATCH"])
@check_access("admin")
def update_assignment(assignment_id: str) -> Response:
    data = request.get_json()
    assignment_obj = AssignmentDao.get_assignment(assignment_id)
    keys = [
        "cloud",
        "vlan",
        "description",
        "owner",
        "ticket",
        "qinq",
        "wipe",
        "cc_user",
    ]
    update_fields = {}
    for key in keys:
        value = data.get(key)
        if value:
            if key == "cc_user":
                value = value.split(",")
            if key == "cloud":
                _cloud = CloudDao.get_cloud(value)
                if not _cloud:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Cloud not found: {value}",
                    }
                    return Response(response=json.dumps(response), status=400)
                value = _cloud
            if key == "vlan":
                _vlan = VlanDao.get_vlan(value)
                if not _vlan:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Vlan not found: {value}",
                    }
                    return Response(response=json.dumps(response), status=400)
                value = _vlan
            if type(value) == str:
                if value.lower() in ["true", "false"]:
                    value = eval(value.lower().capitalize())
            update_fields[key] = value
    for key, value in update_fields.items():
        setattr(assignment_obj, key, value)

    db.session.commit()
    return jsonify(assignment_obj.as_dict())


@assignment_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_assignment() -> Response:
    data = request.get_json()
    assignment_id = data.get("id")

    try:
        AssignmentDao.delete_assignment(assignment_id)
    except EntryNotFound:
        response = {
            "status_code": 401,
            "message": f"Assignment {assignment_id} not found",
        }
        return Response(response=json.dumps(response), status=401)
    return jsonify(
        {
            "message": f"Assignment {assignment_id} deleted",
        }
    )
