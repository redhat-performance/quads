from flask import Blueprint, jsonify, request

from quads.server.blueprints import check_access
from quads.server.models import Assignment, Notification, Cloud, Vlan, db

assignment_bp = Blueprint("assignments", __name__)


@assignment_bp.route("/")
def get_assignments():
    _assignments = db.session.query(Assignment).all()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@assignment_bp.route("/<assignment_id>/")
def get_assignment(assignment_id):
    _assignment = (
        db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
    )
    return jsonify(_assignment.as_dict())


@assignment_bp.route("/", methods=["POST"])
@check_access("admin")
def create_assignment():
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

    if cloud_name:
        _cloud = db.session.query(Cloud).filter(Cloud.name == cloud_name).first()
        if not _cloud:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Cloud not found: {cloud_name}",
                    }
                ),
                400,
            )

    if vlan:
        _vlan = db.session.query(Vlan).filter(Vlan.vlan_id == vlan).first()
        if not _vlan:
            return (
                jsonify(
                    {
                        "error": "Bad Request",
                        "message": f"Vlan not found: {vlan}",
                    }
                ),
                400,
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
    return jsonify(_assignment_obj.as_dict()), 201


@assignment_bp.route("/", methods=["DELETE"])
@check_access("admin")
def delete_assignment():
    data = request.get_json()
    assignment_id = data.get("id")

    _assignment_obj = (
        db.session.query(Assignment).filter(Assignment.id == assignment_id).first()
    )
    if not _assignment_obj:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Assignment {assignment_id} not found",
                }
            ),
            400,
        )

    db.session.delete(_assignment_obj)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Assignment {assignment_id} deleted",
            }
        ),
        201,
    )
