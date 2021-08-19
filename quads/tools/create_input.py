#!/usr/bin/env python3
import asyncio
import os
import pathlib
import re
import requests
from quads.managers.foreman import Foreman
from quads.config import conf, API_URL

HEADERS = [
    "U",
    "ServerHostnamePublic",
    "Serial",
    "MAC",
    "IP",
    "IPMIADDR",
    "IPMIURL",
    "IPMIMAC",
    "Workload",
    "Owner"
]


def consolidate_ipmi_data(_host, _path, _value):
    ipmi_path = os.path.join(conf["data_dir"], "ipmi")
    host_path = os.path.join(ipmi_path, _host)
    _file_path = os.path.join(host_path, _path)
    try:
        with open(_file_path, "r+") as _ipmi_file:
            mac = _ipmi_file.read()
            if not mac and _value:
                _ipmi_file.seek(0)
                _ipmi_file.write(_value)
                _ipmi_file.truncate()
    except IOError:
        if not os.path.exists(host_path):
            pathlib.Path(host_path).mkdir(parents=True, exist_ok=True)
        with open(_file_path, "w") as _ipmi_file:
            value = _value if _value else ""
            _ipmi_file.write(value)


def render_header(_rack):
    h = "**Rack %s**" % _rack.upper()
    h1 = "| %s |" % " | ".join(HEADERS)
    h2 = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    return "\n".join([h, "", h1, h2])


def render_row(_host, _properties):
    u_loc = _host.split("-")[1][1:]
    node = _host
    owner = ""
    cloud = ""
    host_url = os.path.join(API_URL, "host?name=%s" % node)
    _response = requests.get(host_url)
    if _response.status_code == 200:
        host_data = _response.json()
        if "cloud" in host_data:
            cloud_url = os.path.join(API_URL, "cloud?id=%s" % host_data["cloud"]["$oid"])
            _cloud_response = requests.get(cloud_url)
            if _cloud_response.status_code == 200:
                cloud_data = _cloud_response.json()
                if "owner" in cloud_data:
                    owner = cloud_data["owner"]
                cloud = "[%s](/assignments/#%s)" % (cloud_data["name"], cloud_data["name"])

    row = [
        u_loc,
        node.split(".")[0],
        str(_properties["svctag"]),
        str(_properties["host_mac"]),
        str(_properties["host_ip"]),
        str(_properties["ip"]),
        "<a href=http://mgmt-%s/ target=_blank>console</a>" % _host,
        str(_properties["mac"]),
        cloud,
        owner,
    ]
    return "| %s |\n" % " | ".join(row)


def rack_has_hosts(rack, hosts):
    for host, _ in hosts.items():
        if rack in host:
            return True
    return False


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )
    all_hosts = loop.run_until_complete(foreman.get_all_hosts())

    blacklist = re.compile("|".join([re.escape(word) for word in conf["exclude_hosts"].split("|")]))
    hosts = {}
    for host, properties in all_hosts.items():
        if not blacklist.search(host):
            if properties.get("sp_name", False):
                properties["host_ip"] = properties["ip"]
                properties["host_mac"] = properties["mac"]
                properties["ip"] = properties.get("sp_ip")
                properties["mac"] = properties.get("sp_mac")
                consolidate_ipmi_data(host, "macaddr", properties["host_mac"])
                consolidate_ipmi_data(host, "oobmacaddr", properties.get("sp_mac"))
                svctag_file = os.path.join(conf["data_dir"], "ipmi", host, "svctag")
                svctag = ""
                if os.path.exists(svctag_file):
                    with open(svctag_file) as _file:
                        svctag = _file.read()
                properties["svctag"] = svctag.strip()
                hosts[host] = properties

    _full_path = os.path.join(conf["wp_wiki_git_repo_path"], "main.md")

    if not os.path.exists(conf["wp_wiki_git_repo_path"]):
        pathlib.Path(conf["wp_wiki_git_repo_path"]).mkdir(parents=True, exist_ok=True)

    with open(_full_path, "w") as _f:
        _f.seek(0)
        for rack in conf["racks"].split():
            if rack_has_hosts(rack, hosts):
                _f.write(render_header(rack))

                for host, properties in hosts.items():
                    if rack in host:
                        _f.write(render_row(host, properties))
                _f.write("\n")

        _f.truncate()


if __name__ == "__main__":
    main()
