#!/usr/bin/env python3

import asyncio
import json
from collections import defaultdict
from distutils.util import strtobool

from quads.quads_api import QuadsApi
from quads.tools.external.foreman import Foreman
from quads.config import Config

quads = QuadsApi(Config)


async def make_env_json(filename, cloud):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ass = quads.get_active_cloud_assignment(cloud)
    if ass:
        infra_pass = f"{Config['infra_location']}@{ass.ticket}"

        foreman_cloud_user = Foreman(
            Config["foreman_api_url"],
            cloud.name,
            infra_pass,
            loop=loop,
        )

        cloud_hosts = loop.run_until_complete(foreman_cloud_user.get_all_hosts())
    else:
        return {}

    data = defaultdict(list)
    for host, properties in cloud_hosts:
        # TODO: check properties return
        params = properties.get('params')
        overcloud = params.get('overcloud')

        if not overcloud:
            overcloud = {"result": "true"}

        if type(overcloud["result"]) != bool:
            try:
                _overcloud_result = strtobool(overcloud["result"])
            except ValueError:
                print(f"WARN: {host} overcloud value is not set correctly.")
                _overcloud_result = 1
        else:
            _overcloud_result = overcloud["result"]

        if "result" in overcloud and _overcloud_result:
            mac = []
            if filename == "instackenv":
                # TODO: check interfaces return
                interfaces = properties.get("interfaces")
                for interface in sorted(interfaces, key=lambda k: k.name):
                    if interface.get("pxeboot"):
                        mac.append(interface.get("mac_address"))
            if filename == "ocpinventory":
                mac = [interface.get("mac_address") for interface in sorted(interfaces, key=lambda k: k["name"])]
            data["nodes"].append(
                {
                    "name": host,
                    "pm_password": infra_pass,
                    "pm_type": "pxe_ipmitool",
                    "mac": mac,
                    "cpu": "2",
                    "memory": "1024",
                    "disk": "20",
                    "arch": "x86_64",
                    "pm_user": Config["ipmi_cloud_username"],
                    "pm_addr": "mgmt-%s" % host,
                }
            )

        content = json.dumps(data, indent=4, sort_keys=True)
        return content
