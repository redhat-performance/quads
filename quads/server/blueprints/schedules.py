from datetime import datetime
from flask import Blueprint, jsonify, request, Response, make_response
from sqlalchemy.exc import DataError

from quads.server.blueprints import check_access
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import EntryNotFound, InvalidArgument
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.models import Schedule, db

schedule_bp = Blueprint("schedules", __name__)


@schedule_bp.route("/")
def get_schedules() -> Response:
    if request.args:
        try:
            _schedules = ScheduleDao.filter_schedules(**request.args)
        except (EntryNotFound, InvalidArgument) as ex:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": str(ex),
            }
            return make_response(jsonify(response), 400)

    else:
        _schedules = ScheduleDao.get_schedules()
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/<schedule_id>")
def get_schedule(schedule_id: int) -> Response:
    _schedule = ScheduleDao.get_schedule(schedule_id)
    if not _schedule:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Schedule not found: {schedule_id}",
        }
        return make_response(jsonify(response), 400)
    return jsonify(_schedule.as_dict())


@schedule_bp.route("/current")
def get_current_schedule() -> Response:
    data = request.args.to_dict()
    date = data.get("date")
    hostname = data.get("host")
    cloud_name = data.get("cloud")
    host = HostDao.get_host(hostname)
    cloud = CloudDao.get_cloud(cloud_name)
    _schedules = ScheduleDao.get_current_schedule(date, host, cloud)
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/future")
def get_future_schedule() -> Response:
    data = request.args.to_dict()
    hostname = data.get("host")
    cloud_name = data.get("cloud")
    host = HostDao.get_host(hostname)
    cloud = CloudDao.get_cloud(cloud_name)
    _schedules = ScheduleDao.get_future_schedules(host, cloud)
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/", methods=["POST"])
@check_access("admin")
def create_schedule() -> Response:
    data = request.get_json()
    hostname = data.get("hostname")
    cloud = data.get("cloud")
    if not cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: cloud",
        }
        return make_response(jsonify(response), 400)

    _cloud = CloudDao.get_cloud(cloud)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Cloud not found: {cloud}",
        }
        return make_response(jsonify(response), 400)
    _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
    if not _assignment:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"No active assignment for cloud: {cloud}",
        }
        return make_response(jsonify(response), 400)

    if not hostname:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: hostname",
        }
        return make_response(jsonify(response), 400)

    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host not found: {hostname}",
        }
        return make_response(jsonify(response), 400)

    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: start or end",
        }
        return make_response(jsonify(response), 400)

    try:
        _start = datetime.strptime(start, "%Y-%m-%d %H:%M")
        _end = datetime.strptime(end, "%Y-%m-%d %H:%M")
    except ValueError:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date format for start or end, correct format: 'YYYY-MM-DD HH:MM'",
        }
        return make_response(jsonify(response), 400)

    if _start > _end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date range for start or end, start must be before end",
        }
        return make_response(jsonify(response), 400)

    _schedule_obj = Schedule(start=_start, end=_end, assignment=_assignment, host=_host)
    db.session.add(_schedule_obj)
    db.session.commit()

    return jsonify(_schedule_obj.as_dict())


@schedule_bp.route("/<schedule_id>", methods=["PATCH"])
@check_access("admin")
def update_schedule(schedule_id: str) -> Response:
    data = request.get_json()
    dates = {
        "start": data.get("start"),
        "end": data.get("end"),
        "build_start": data.get("build_start"),
        "build_end": data.get("build_end"),
    }
    objects = [("hostname", HostDao.get_host), ("cloud", CloudDao.get_cloud)]

    schedule = ScheduleDao.get_schedule(schedule_id)
    if not schedule:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Schedule not found: {schedule_id}",
        }
        return make_response(jsonify(response), 400)

    for key, method in objects:
        value = data.get(key)
        if value:
            model_obj = method(value)
            if not model_obj:
                response = {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"{key} not found: {value}",
                }
                return make_response(jsonify(response), 400)
            else:
                if key == "hostname":
                    key = "host"
                schedule[key] = model_obj

    if not any(dates.values()):
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: start, end, build_start or build_end (specify at least one)",
        }
        return make_response(jsonify(response), 400)

    for key, value in [(k, v) for k, v in dates.items() if v]:
        try:
            dates[key] = datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            response = {
                "status_code": 400,
                "error": "Bad Request",
                "message": f"Invalid date format for '{key}', correct format: 'YYYY-MM-DD HH:MM'",
            }
            return make_response(jsonify(response), 400)

    _start = dates.get("start") if dates.get("start") else schedule.start
    _end = dates.get("end") if dates.get("end") else schedule.end
    _build_start = (
        dates.get("build_start") if dates.get("build_start") else schedule.build_start
    )
    _build_end = (
        dates.get("build_end") if dates.get("build_end") else schedule.build_end
    )

    if _start > _end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date range for 'start' or 'end', 'start' must be before 'end'",
        }
        return make_response(jsonify(response), 400)
    if _build_end and _build_start and _build_start > _build_end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date range for 'build_start' or 'build_end', 'build_start' must be before 'build_end'",
        }
        return make_response(jsonify(response), 400)
    if _build_start and _start > _build_start:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date range for 'start' or 'build_start', 'start' must be before 'build_start'",
        }
        return make_response(jsonify(response), 400)
    if _build_end and _build_end > _end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Invalid date range for 'end' or 'build_end', 'build_end' must be before 'end'",
        }
        return make_response(jsonify(response), 400)

    schedule.start = _start
    schedule.end = _end
    schedule.build_start = _build_start
    schedule.build_end = _build_end
    db.session.commit()
    return jsonify(schedule.as_dict())


@schedule_bp.route("/<schedule_id>", methods=["DELETE"])
@check_access("admin")
def delete_schedule(schedule_id: int) -> Response:
    _schedule = ScheduleDao.get_schedule(schedule_id)
    if not _schedule:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Schedule not found: {schedule_id}",
        }
        return make_response(jsonify(response), 400)

    db.session.delete(_schedule)
    db.session.commit()
    response = {
        "status_code": 200,
        "message": "Schedule deleted",
    }
    return jsonify(response)
