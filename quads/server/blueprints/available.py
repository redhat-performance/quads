from datetime import datetime

from flask import Blueprint, jsonify, request, Response

from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao

available_bp = Blueprint("available", __name__)


@available_bp.route("/")
def get_available() -> Response:
    _params = request.args.to_dict()
    _start = _end = datetime.now()
    if _params.get("start"):
        _start = datetime.fromisoformat(_params.pop("start"))
    if _params.get("end"):
        _end = datetime.fromisoformat(_params.pop("end"))
    if _params.get("cloud"):
        # TODO: fix cloud filter
        _cloud = CloudDao.get_cloud(_params.pop("cloud"))

    available = []

    if _params:
        all_hosts = HostDao.filter_hosts_dict(_params)
    else:
        all_hosts = HostDao.get_hosts()

    for host in all_hosts:
        if ScheduleDao.is_host_available(host.name, _start, _end):
            available.append(host.name)
    return jsonify(available)


@available_bp.route("/<hostname>", methods=["POST"])
def is_available(hostname) -> Response:
    data = request.get_json()
    _start = _end = datetime.now()
    if data.get("start"):
        _start = datetime.strptime(data.get("start"), "%Y-%m-%d %H:%M")
    if data.get("end"):
        _end = datetime.strptime(data.get("end"), "%Y-%m-%d %H:%M")

    available = ScheduleDao.is_host_available(hostname, _start, _end)

    return jsonify({hostname: available})
