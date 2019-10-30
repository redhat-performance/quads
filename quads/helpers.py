from mongoengine import ObjectIdField

from quads.config import SUPPORTED, SUPERMICRO, OFFSETS, conf


def param_check(data, params, defaults={}):
    result = []
    # set defaults
    for k, v in defaults.items():
        data.setdefault(k, v)

    if data:
        # check for missing params
        for p in params:
            if p not in data:
                result.append("Missing required parameter: %s" % p)
            elif not (data[p] or data[p] is None):
                result.append("Could not parse %s parameter" % p)
            elif data[p] == 'None':
                data[p] = None
            if p == "_id":
                data["_id"] = ObjectIdField(data[p])

    return result, data


def is_supported(_host_name):
    for host_type in SUPPORTED:
        if host_type in _host_name:
            return True
    return False


def is_supermicro(_host_name):
    for host_type in SUPERMICRO:
        if host_type in _host_name:
            return True
    return False


def get_vlan(cloud_obj, index, last_nic=False):
    if cloud_obj.vlan and last_nic:
        return int(cloud_obj.vlan.vlan_id)
    else:
        if 'sw_vlan_first' in conf:
            vlan_first = int(conf["sw_vlan_first"]) - 10
        else:
            vlan_first = 1090
        cloud_offset = int(cloud_obj.name[5:]) * 10
        base_vlan = vlan_first + cloud_offset
        vlan = base_vlan + list(OFFSETS.values())[index * int(cloud_obj.qinq)]
        return vlan
