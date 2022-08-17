import json
from datetime import datetime

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import and_

from quads.server.blueprints import check_access
from quads.server.dao.cloud import CloudDao
from quads.server.models import Assignment, Schedule, Host, db, Cloud

schedule_bp = Blueprint("schedules", __name__)


@schedule_bp.route("/")
def get_schedules() -> Response:
    _schedules = db.session.query(Schedule).all()
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/<schedule_id>")
def get_schedule(schedule_id) -> Response:
    _schedule = db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not _schedule:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Schedule {schedule_id} does not exists",
            }
        )
    return jsonify(_schedule.as_dict())


@schedule_bp.route("/", methods=["POST"])
@check_access("admin")
def create_schedule() -> Response:
    data = request.get_json()
    hostname = data.get("hostname")
    cloud = data.get("cloud")
    if not cloud:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Missing argument: cloud",
        }
        response = Response(response=json.dumps(data), status=400)
        return response

    _cloud = CloudDao.get_cloud(cloud)
    if not _cloud:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"{cloud} not found.",
        }
        response = Response(response=json.dumps(data), status=400)
        return response
    _assignment = (
        db.session.query(Assignment)
        .filter(and_(Assignment.cloud == _cloud, Assignment.active == True))
        .first()
    )
    if not _assignment:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"No active assignment for cloud: {cloud}",
        }
        response = Response(response=json.dumps(data), status=400)
        return response

    if not hostname:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: hostname",
        }
        response = Response(response=json.dumps(data), status=400)
        return response

    _host = db.session.query(Host).filter(Host.name == hostname).first()
    if not _host:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host {hostname} not found",
        }
        response = Response(response=json.dumps(data), status=400)
        return response

    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        data = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: start or end",
        }
        response = Response(response=json.dumps(data), status=400)
        return response

    _start = datetime.strptime(start, "%Y-%m-%d %H:%M")
    _end = datetime.strptime(end, "%Y-%m-%d %H:%M")
    _schedule_obj = Schedule(start=_start, end=_end, assignment=_assignment, host=_host)
    db.session.add(_schedule_obj)
    db.session.commit()

    return jsonify(_schedule_obj.as_dict())


@schedule_bp.route("/<schedule_id>", methods=["DELETE"])
@check_access("admin")
def delete_schedule(schedule_id) -> Response:
    _schedule = db.session.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not _schedule:
        return jsonify(
            {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Schedule not found: {schedule_id}",
            }
        )

    db.session.delete(_schedule)
    db.session.commit()
    return jsonify(
        {
            "status_code": 201,
            "message": f"Schedule deleted",
        }
    )
