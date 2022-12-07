import json

from datetime import datetime
from flask import Blueprint, jsonify, request, Response
from sqlalchemy import Boolean
from sqlalchemy.orm import RelationshipProperty

from quads.server.blueprints import check_access
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import OPERATORS, MAP_MODEL
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.models import Schedule, db

schedule_bp = Blueprint("schedules", __name__)


# @schedule_bp.route("/")
# def get_schedules() -> Response:
#     _schedules = ScheduleDao.get_schedules()
#     return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/")
def get_schedules() -> Response:
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

        field = Schedule.__mapper__.attrs.get(first_field)
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
        _schedules = ScheduleDao.create_query_select(Schedule, filters=filter_tuples)
    else:
        _schedules = ScheduleDao.get_schedules()
    return jsonify([_assignment.as_dict() for _assignment in _schedules])


@schedule_bp.route("/<schedule_id>")
def get_schedule(schedule_id: int) -> Response:
    _schedule = ScheduleDao.get_schedule(schedule_id)
    if not _schedule:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Schedule {schedule_id} does not exists",
        }
        return Response(response=json.dumps(response), status=400)
    return jsonify(_schedule.as_dict())


@schedule_bp.route("/current", methods=["POST"])
def get_current_schedule() -> Response:
    data = request.get_json()
    date = data.get("date")
    hostname = data.get("host")
    cloud_name = data.get("cloud")
    host = HostDao.get_host(hostname)
    cloud = CloudDao.get_cloud(cloud_name)
    _schedules = ScheduleDao.get_current_schedule(date, host, cloud)
    return jsonify([_schedule.as_dict() for _schedule in _schedules])


@schedule_bp.route("/future", methods=["POST"])
def get_future_schedule() -> Response:
    data = request.get_json()
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
        return Response(response=json.dumps(response), status=400)

    _cloud = CloudDao.get_cloud(cloud)
    if not _cloud:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"{cloud} not found.",
        }
        return Response(response=json.dumps(response), status=400)
    _assignment = AssignmentDao.get_active_cloud_assignment(_cloud)
    if not _assignment:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"No active assignment for cloud: {cloud}",
        }
        return Response(response=json.dumps(response), status=400)

    if not hostname:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: hostname",
        }
        return Response(response=json.dumps(response), status=400)

    _host = HostDao.get_host(hostname)
    if not _host:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Host {hostname} not found",
        }
        return Response(response=json.dumps(response), status=400)

    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": "Missing argument: start or end",
        }
        return Response(response=json.dumps(response), status=400)

    _start = datetime.strptime(start, "%Y-%m-%d %H:%M")
    _end = datetime.strptime(end, "%Y-%m-%d %H:%M")
    _schedule_obj = Schedule(start=_start, end=_end, assignment=_assignment, host=_host)
    db.session.add(_schedule_obj)
    db.session.commit()

    return jsonify(_schedule_obj.as_dict())


@schedule_bp.route("/<schedule_id>", methods=["POST"])
@check_access("admin")
def update_schedule(schedule_id: str) -> Response:
    data = request.get_json()
    dates = [
        "start",
        "end",
        "build_start",
        "build_end",
    ]
    objects = [("hostname", HostDao.get_host), ("cloud", CloudDao.get_cloud)]

    schedule = ScheduleDao.get_schedule(schedule_id)
    if not schedule:
        response = {
            "status_code": 400,
            "error": "Bad Request",
            "message": f"Schedule {schedule_id} not found.",
        }
        return Response(response=json.dumps(response), status=400)

    for key, method in objects:
        value = data.get(key)
        if value:
            model_obj = method(value)
            if not model_obj:
                response = {
                    "status_code": 400,
                    "error": "Bad Request",
                    "message": f"{key} {value} not found.",
                }
                return Response(response=json.dumps(response), status=400)
            else:
                if key == "hostname":
                    key = "host"
                schedule[key] = model_obj

    for date in dates:
        _date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        schedule[date] = _date

    db.session.commit()

    return jsonify(schedule.as_dict())


@schedule_bp.route("/<schedule_id>", methods=["DELETE"])
@check_access("admin")
def delete_schedule(schedule_id: int) -> Response:
    _schedule = ScheduleDao.get_schedule(schedule_id)
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
            "message": "Schedule deleted",
        }
    )
