from flask import Blueprint, jsonify, request

from quads.server.blueprints import check_access
from quads.server.models import Assignment, Schedule, Host, db

schedule_bp = Blueprint("schedules", __name__)


@schedule_bp.route("/")
def get_schedules():
    _schedules = db.session.query(Schedule).all()
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/<schedule_id>")
def get_schedule(schedule_id):
    _schedule = db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
    return jsonify(_schedule.as_dict())


@schedule_bp.route("/", methods=["POST"])
@check_access("admin")
def create_schedule():
    data = request.get_json()

    hostname = data.get("hostname")
    cloud = data.get("cloud")
    _assignment = (
        db.session.query(Assignment)
        .filter(Assignment.cloud.name == cloud, Assignment.active == True)
        .first()
    )
    if not _assignment:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"No active assignment for cloud: {cloud}",
                }
            ),
            400,
        )

    if not hostname:
        return (
            jsonify({"error": "Bad Request", "message": "Missing argument: hostname"}),
            400,
        )

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if _host:
        return (
            jsonify(
                {"error": "Bad Request", "message": f"Host {hostname} already exists"}
            ),
            400,
        )

    start = data.get("start")
    end = data.get("end")

    _schedule_obj = Schedule(start=start, end=end, assignment=_assignment, host=_host)
    db.session.add(_schedule_obj)
    db.session.commit()

    return jsonify(_schedule_obj.as_dict()), 201


@schedule_bp.route("/<schedule_id>", methods=["DELETE"])
@check_access("admin")
def delete_schedule(schedule_id):
    _schedule = db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not _schedule:
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": f"Schedule not found: {schedule_id}",
                }
            ),
            400,
        )

    db.session.delete(_schedule)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Schedule deleted",
            }
        ),
        201,
    )
