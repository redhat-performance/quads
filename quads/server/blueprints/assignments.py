from flask import Blueprint, jsonify, request
from quads.models import Assignment, Notification, Cloud, Vlan
from quads.server.app import db_session

assignment_bp = Blueprint("assignments", __name__)


@assignment_bp.route("/")
def get_assignments():
    _assignments = db_session.query(Assignment).all()
    return jsonify([_assignment.as_dict() for _assignment in _assignments])


@assignment_bp.route("/<assignment_id>/")
def get_assignment(assignment_id):
    _assignment = (
        db_session.query(Assignment).filter(Assignment.id == assignment_id).first()
    )
    return jsonify(_assignment.as_dict())


@assignment_bp.route("/", methods=["POST"])
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
        _cloud = db_session.query(Cloud).filter(Cloud.name == cloud_name).first()
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
        _vlan = db_session.query(Vlan).filter(Vlan.vlan_id == vlan).first()
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
    db_session.add(_assignment_obj)
    db_session.commit()
    return jsonify(_assignment_obj.as_dict()), 201
