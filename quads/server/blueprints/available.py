from datetime import datetime

from flask import Blueprint, jsonify, request, Response

from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao

available_bp = Blueprint("available", __name__)


@available_bp.route("/")
def get_available() -> Response:
    """
    Used to return a list of hosts that are available for the given time period.
        ---
        tags:
          - Hosts

    :return: A list of hosts that are available for the given start and end time
    """
    _params = request.args.to_dict()
    _start = _end = datetime.now()
    _cloud = None
    if _params.get("start"):
        _start = datetime.fromisoformat(_params.pop("start"))
    if _params.get("end"):
        _end = datetime.fromisoformat(_params.pop("end"))
    if _params.get("cloud"):
        _cloud = CloudDao.get_cloud(_params.pop("cloud"))

    available = []

    if _params:
        all_hosts = HostDao.filter_hosts_dict(_params)
    else:
        all_hosts = HostDao.get_hosts()

    for host in all_hosts:
        if ScheduleDao.is_host_available(host.name, _start, _end):
            if _cloud and host.cloud.name == _cloud.name:
                available.append(host.name)
    return jsonify(available)


@available_bp.route("/<hostname>", methods=["POST"])
def is_available(hostname) -> Response:
    """
    Used to determine if a host is available for a given time period.
        The function takes in the following parameters:
            - hostname (string): The name of the host that you want to check availability for.
            - start (datetime): A datetime object representing when you would like your reservation to begin.
            If no value is provided, it will default to now().
            - end (datetime): A datetime object representing when you would like your reservation to end.
            If no value is provided, it will default to now().

    :param hostname: Specify the hostname of the device
    :return: A boolean value
    """
    data = request.get_json()
    _start = _end = datetime.now()
    if data.get("start"):
        _start = datetime.strptime(data.get("start"), "%Y-%m-%d %H:%M")
    if data.get("end"):
        _end = datetime.strptime(data.get("end"), "%Y-%m-%d %H:%M")

    available = ScheduleDao.is_host_available(hostname, _start, _end)

    return jsonify({hostname: available})
