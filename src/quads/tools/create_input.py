#!/usr/bin/env python3
import asyncio
import os
import pathlib
import re

from quads.quads_api import QuadsApi
from quads.tools.external.foreman import Foreman
from quads.config import Config

quads = QuadsApi(Config)

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
    "Owner",
]


def render_header(_rack):
    h = "**Rack %s**" % _rack.upper()
    h1 = "| %s |" % " | ".join(HEADERS)
    h2 = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    return "\n".join([h, "", h1, h2])


def render_row(host_obj, _properties):
    u_loc = host_obj.name.split("-")[1][1:]
    cloud = "[%s](/assignments/#%s)" % (
        host_obj.cloud.name,
        host_obj.cloud.name,
    )
    assignment = quads.get_active_cloud_assignment(host_obj.cloud.name)
    owner = assignment.owner if assignment else "QUADS"
    row = [
        u_loc,
        host_obj.name.split(".")[0],
        str(_properties["svctag"]),
        str(_properties["host_mac"]),
        str(_properties["host_ip"]),
        str(_properties["ip"]),
        "<a href=http://mgmt-%s/ target=_blank>console</a>" % host_obj.name,
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
        Config["foreman_api_url"],
        Config["foreman_username"],
        Config["foreman_password"],
        loop=loop,
    )
    all_hosts = loop.run_until_complete(foreman.get_all_hosts())

    blacklist = re.compile(
        "|".join([re.escape(word) for word in Config["exclude_hosts"].split("|")])
    )
    hosts = {}
    for host, properties in all_hosts.items():
        if not blacklist.search(host):
            if properties.get("sp_name", False):
                properties["host_ip"] = properties["ip"]
                properties["host_mac"] = properties["mac"]
                properties["ip"] = properties.get("sp_ip")
                properties["mac"] = properties.get("sp_mac")
                properties["svctag"] = ""
                hosts[host] = properties

    _full_path = os.path.join(Config["wp_wiki_git_repo_path"], "main.md")

    if not os.path.exists(Config["wp_wiki_git_repo_path"]):
        pathlib.Path(Config["wp_wiki_git_repo_path"]).mkdir(parents=True, exist_ok=True)

    with open(_full_path, "w") as _f:
        _f.seek(0)
        for rack in Config["racks"].split():
            if rack_has_hosts(rack, hosts):

                _f.write(render_header(rack))

                for host, properties in hosts.items():
                    if rack in host:
                        host_obj = quads.get_host(host)
                        if host_obj and not host_obj.retired:
                            _f.write(render_row(host_obj, properties))
                _f.write("\n")

        _f.truncate()


if __name__ == "__main__":
    main()
