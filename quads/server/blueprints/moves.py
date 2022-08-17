from datetime import datetime

from flask import Blueprint, jsonify, request, abort, Response

from quads.server.blueprints import check_access
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao


moves_bp = Blueprint("moves", __name__)


# TODO: complete this
@moves_bp.route("/", methods=["POST"])
@check_access("admin")
def get_moves() -> Response:
    data = request.get_json()
    date = data.get("date")
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
                    _schedule_cloud = _current_schedule[0].cloud.name
                if _schedule_cloud != _host_defined_cloud:
                    result.append(
                        {
                            "host": host.name,
                            "new": _schedule_cloud,
                            "current": _host_defined_cloud,
                        }
                    )
            except Exception:
                # TODO: check exceptions
                continue
    except Exception as ex:
        abort(400)

    return jsonify(result)
