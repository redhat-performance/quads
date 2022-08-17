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
    _assignments = db.session.query(Assignment).all()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@assignment_bp.route("/<assignment_id>/")
def get_assignment(assignment_id) -> Response:
    _assignment = (
        db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
    )
    if not _assignment:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Assignment {_assignment} does not exists",
            }
        )
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
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Missing argument: {field}",
                }
            )

    if cc_user:
        cc_user = cc_user.split(",")

    if cloud_name:
        _cloud = CloudDao.get_cloud(cloud_name)
        if not _cloud:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Cloud not found: {cloud_name}",
                }
            )
        _assignment = AssignmentDao.get_active_cloud_assignment(cloud_name)
        if _assignment:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"There is an already active assignment for {cloud_name}",
                }
            )

    if vlan:
        _vlan = VlanDao.get_vlan(vlan)
        if not _vlan:
            return jsonify(
                {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"Vlan not found: {vlan}",
                }
            )

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


@assignment_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_assignment() -> Response:
    data = request.get_json()
    assignment_id = data.get("id")

    try:
        AssignmentDao.delete_assignment(assignment_id)
    except EntryNotFound:
        return jsonify(
            {
                "status_code": 401,
                "message": f"Assignment {assignment_id} not found",
            }
        )
    return jsonify(
        {
            "status_code": 201,
            "message": f"Assignment {assignment_id} deleted",
        }
    )
