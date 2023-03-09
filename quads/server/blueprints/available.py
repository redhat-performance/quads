from datetime import datetime

from flask import Blueprint, jsonify, request, Response

from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao

available_bp = Blueprint("available", __name__)


@available_bp.route("/", methods=["POST"])
def get_available() -> Response:
    data = request.get_json()
    _start = _end = datetime.now()
    if data.get("start"):
        _start = datetime.strptime(data.get("start"), "%Y-%m-%d %H:%M")
    if data.get("end"):
        _end = datetime.strptime(data.get("end"), "%Y-%m-%d %H:%M")

    available = []
    all_hosts = HostDao.get_hosts()

    for host in all_hosts:
        if ScheduleDao.is_host_available(host.name, _start, _end):
            available.append(host.name)
    return jsonify(available)
