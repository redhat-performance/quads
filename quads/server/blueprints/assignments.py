import json

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import Boolean
from sqlalchemy.orm import RelationshipProperty

from quads.server.blueprints import check_access
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import EntryNotFound, OPERATORS, MAP_MODEL
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import Assignment, Notification, Cloud, Vlan, db

assignment_bp = Blueprint("assignments", __name__)


@assignment_bp.route("/")
def get_assignments() -> Response:
    # TODO: Add filter for child objects
    filter_tuples = []
    operator = "=="
    for k, value in request.args.items():
        fields = k.split(".")
        if len(fields) > 2:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Too many arguments: {fields}",
            }
            return Response(response=json.dumps(response), status=400)

        first_field = fields[0]
        field_name = fields[-1]
        if "__" in k:
            for op in OPERATORS.keys():
                if op in field_name:
                    field_name = field_name[: field_name.index(op)]
                    operator = OPERATORS[op]
                    break

        field = Assignment.__mapper__.attrs.get(first_field)
        if not field:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"{k} is not a valid field.",
            }
            return Response(response=json.dumps(response), status=400)
        if (
            type(field) != RelationshipProperty
            and type(field.columns[0].type) == Boolean
        ):
            value = value.lower() in ["true", "y", 1, "yes"]
        else:
            if first_field in ["cloud", "default_cloud"]:
                cloud = CloudDao.get_cloud(value)
                if not cloud:
                    response = {
                        "status_code": 400,
                        "error": "Bad Request",
                        "message": f"Cloud {value} does not exist.",
                    }
                    return Response(response=json.dumps(response), status=400)
                value = cloud
            if first_field.lower() in MAP_MODEL.keys():
                if len(fields) > 1:
                    field_name = f"{first_field.lower()}.{field_name.lower()}"
        filter_tuples.append(
            (
                field_name,
                operator,
                value,
            )
        )
    if filter_tuples:
        _assignments = AssignmentDao.create_query_select(
            Assignment, filters=filter_tuples
        )
    else:
        _assignments = AssignmentDao.get_assignments()


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


@assignment_bp.route("/active/<cloud_name>/")
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
