from datetime import datetime

from flask import Blueprint, jsonify, abort, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao


moves_bp = Blueprint("moves", __name__)


# TODO: complete this
@moves_bp.route("/")
# @check_access("admin")
def get_moves() -> Response:
    result = []
    try:
        _hosts = HostDao.get_hosts()
        for host in _hosts:
            _current_schedule = ScheduleDao.get_current_schedule(host=host)
            _schedule_cloud = (
                _current_schedule[0].assignment.cloud
                if _current_schedule
                else host.default_cloud
            )
            try:
                if _schedule_cloud != host.cloud:
                    result.append(
                        {
                            "host": host.name,
                            "new": _schedule_cloud.name,
                            "current": host.cloud.name,
                        }
                    )
            except Exception:
                # TODO: check exceptions
                abort(400)
    except Exception:
        abort(400)

    return jsonify(result)


@moves_bp.route("/<date>/")
@check_access("admin")
def get_moves_on_date(date: str) -> Response:
    """
    Returns a list of hosts that need to be moved from one cloud to another.
        The function takes in a date parameter, which is used to determine the current schedule for each host.
        If no date is provided, the current time will be used instead.

    :param date: str: Specify the date for which we want to get the moves
    :return: A list of dictionaries, each dictionary containing the following keys:
    """
    now = datetime.now()
    result = []
    if date:
        date = datetime.strptime(date, "%Y-%m-%dt%H:%M:%S")
    else:
        date = now
    try:
        _hosts = HostDao.get_hosts()
        for host in _hosts:
            _schedule_cloud = host.default_cloud
            _host_defined_cloud = host.cloud
            _current_schedule = ScheduleDao.get_current_schedule(host=host, date=date)
            try:
                if _current_schedule:
                    _schedule_cloud = _current_schedule[0].assignment.cloud
                if _schedule_cloud != _host_defined_cloud:
                    result.append(
                        {
                            "host": host.name,
                            "new": _schedule_cloud.name,
                            "current": _host_defined_cloud.name,
                        }
                    )
            except Exception:
                # TODO: check exceptions
                continue
    except Exception:
        abort(400)

    return jsonify(result)
