#!/usr/bin/env python

import os
import re
from helpers import quads_load_config
from foreman import Foreman
from quads import Quads

conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)

HEADERS = [
    "U",
    "ServerHostname",
    "Serial",
    "MAC",
    "IP",
    "IPMIADDR",
    "IPMIURL",
    "IPMIMAC",
    "Workload",
    "Owner",
    "Graph"
]


def consolidate_ipmi_data(_host, _path, _value):
    _file_path = os.path.join(conf["data_dir"], "ipmi", _host, _path)
    try:
        with open(_file_path, "r+") as _ipmi_file:
            mac = _ipmi_file.read()
            if not mac:
                _ipmi_file.seek(0)
                _ipmi_file.write(_value)
                _ipmi_file.truncate()
    except IOError:
        with open(_file_path, "w") as _ipmi_file:
            _ipmi_file.write(_value)


def render_header(_rack):
    h = "**Rack %s**" % _rack.upper()
    h1 = "| %s |" % " | ".join(HEADERS)
    h2 = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    return "\n".join([h, "", h1, h2])


def render_row(_quads, _host, _properties):
    u_loc = _host.split("-")[2][1:]
    node = _host[5:]
    owner = ""
    cloud = ""
    workload = _quads.query_host_cloud(node, None)
    if workload:
        cloud_owner = _quads.get_owners(workload)
        owner = cloud_owner[0][workload]
        cloud = "[%s](/assignments/#%s)" % (workload, workload)

    # TODO: figure out what to put on grafana field
    grafana = ""
    row = [
        u_loc,
        node.split(".")[0],
        _properties["svctag"],
        _properties["host_mac"],
        _properties["host_ip"],
        _properties["ip"],
        "<a href=http://%s/ target=_blank>console</a>" % _host,
        _properties["mac"],
        cloud,
        owner,
        grafana,
    ]
    return "| %s |" % " | ".join(row)


def rack_has_hosts(rack, hosts):
    for host, _ in hosts.items():
        if rack in host:
            return True
    return False


def main():
    default_config = conf["data_dir"] + "/schedule.yaml"
    default_state_dir = conf["data_dir"] + "/state"
    default_move_command = "/bin/echo"

    quads = Quads(
        default_config,
        default_state_dir,
        default_move_command,
        None, False, False, False,
    )
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
    )

    all_hosts = foreman.get_all_hosts()
    blacklist = re.compile(conf["exclude_hosts"])
    hosts = {}
    for host, properties in all_hosts.items():
        if "mgmt" in host and not blacklist.search(host):
            properties["host_ip"] = all_hosts.get(host[5:], {"ip": None})["ip"]
            properties["host_mac"] = all_hosts.get(host[5:], {"mac": None})["mac"]
            consolidate_ipmi_data(host[5:], "macaddr", properties["host_mac"])
            consolidate_ipmi_data(host[5:], "oobmacaddr", properties["mac"])
            svctag_file = os.path.join(conf["data_dir"], "ipmi", host[5:], "svctag")
            svctag = ""
            if os.path.exists(svctag_file):
                with open(svctag_file) as _file:
                    svctag = _file.read()
            properties["svctag"] = svctag.strip()
            hosts[host] = properties

    _full_path = os.path.join(conf["wp_wiki_git_repo_path"], "main.md")

    with open(_full_path, "w") as _f:
        _f.seek(0)
        for rack in conf["racks"].split():
            if rack_has_hosts(rack, hosts):
                _f.write(render_header(rack))

                for host, properties in hosts.items():
                    if rack in host:
                        _f.write(render_row(quads, host, properties))
                _f.write("\n")

        _f.truncate()


if __name__ == "__main__":
    main()
