import calendar

from datetime import timedelta, datetime
from quads.config import Config


def param_check(data, params, defaults=None):
    if not defaults:
        defaults = {}
    result = []
    # set defaults
    for k, v in defaults.items():
        data.setdefault(k, v)

    if data:
        # check for missing params
        for param in params:
            if param not in data:
                result.append("Missing required parameter: %s" % param)
            elif not data[param]:
                result.append("Could not parse %s parameter" % param)
            elif data[param] == "None":
                data[param] = None

    return result, data


def is_supported(_host_name):
    for host_type in Config.SUPPORTED:
        if host_type in _host_name:
            return True
    return False


def get_vlan(ass_obj, index, last_nic=False):
    if ass_obj and ass_obj.vlan and last_nic:
        return int(ass_obj.vlan.vlan_id)
    else:
        if ass_obj:
            return calculate_vlan(ass_obj.cloud.id, ass_obj.qinq, index)
        else:
            return calculate_vlan(1, 0, index)


def calculate_vlan(cloud_id, qinq, index):
    vlan_first = int(Config.sw_vlan_first) - 10
    cloud_offset = cloud_id * 10
    base_vlan = vlan_first + cloud_offset
    if qinq == 1:
        index = 0
    vlan = base_vlan + list(Config.OFFSETS.values())[index]
    return vlan


def date_span(start, end, delta=timedelta(days=1)):
    current = start
    while current < end:
        yield current
        current += delta


def month_delta_past(date, months):
    month = date.month - 1 - months
    year = date.year + month // 12
    month = month % 12 + 1
    _, last_day = calendar.monthrange(year, month)
    return datetime(year, month, last_day)


def last_day_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def first_day_month(date):
    return date - timedelta(days=date.day - 1)
