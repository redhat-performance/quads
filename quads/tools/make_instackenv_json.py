#!/usr/bin/python3

import asyncio
import json
import os
import time
import pathlib
from collections import defaultdict
from distutils.util import strtobool
from datetime import datetime
from shutil import copyfile
from quads.model import Cloud, Host
from quads.tools.foreman import Foreman
from quads.config import conf


def make_env_json(filename):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )

    cloud_list = Cloud.objects()

    if not os.path.exists(conf["json_web_path"]):
        os.makedirs(conf["json_web_path"])

    now = time.time()
    old_jsons = [file for file in os.listdir(conf["json_web_path"]) if ":" in file]
    for file in old_jsons:
        if (
            os.stat(os.path.join(conf["json_web_path"], file)).st_mtime
            < now - conf["json_retention_days"] * 86400
        ):
            os.remove(os.path.join(conf["json_web_path"], file))

    for cloud in cloud_list:
        host_list = Host.objects(cloud=cloud).order_by("name")

        foreman_password = conf["ipmi_password"]
        if cloud.ticket:
            foreman_password = f"{conf['infra_location']}@{cloud.ticket}"

        data = defaultdict(list)
        for host in host_list:
            if conf["foreman_unavailable"]:
                overcloud = {"result": "true"}
            else:
                overcloud = loop.run_until_complete(
                    foreman.get_host_param(host.name, "overcloud")
                )

            if not overcloud:
                overcloud = {"result": "true"}

            if type(overcloud["result"]) != bool:
                try:
                    _overcloud_result = strtobool(overcloud["result"])
                except ValueError:
                    print(f"WARN: {host.name} overcloud value is not set correctly.")
                    _overcloud_result = 1
            else:
                _overcloud_result = overcloud["result"]

            if "result" in overcloud and _overcloud_result:
                mac = []
                if filename == "instackenv":
                    for interface in host.interfaces:
                        if interface.pxe_boot:
                            mac.append(interface.mac_address)
                if filename == "ocpinventory":
                    mac = [interface.mac_address for interface in host.interfaces]
                data["nodes"].append(
                    {
                        "pm_password": foreman_password,
                        "pm_type": "pxe_ipmitool",
                        "mac": mac,
                        "cpu": "2",
                        "memory": "1024",
                        "disk": "20",
                        "arch": "x86_64",
                        "pm_user": conf["ipmi_cloud_username"],
                        "pm_addr": "mgmt-%s" % host.name,
                    }
                )

        content = json.dumps(data, indent=4, sort_keys=True)

        if not os.path.exists(conf["json_web_path"]):
            pathlib.Path(conf["json_web_path"]).mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        new_json_file = os.path.join(
            conf["json_web_path"],
            "%s_%s.json_%s" % (cloud.name, filename, now.strftime("%Y-%m-%d_%H:%M:%S")),
        )
        json_file = os.path.join(
            conf["json_web_path"], "%s_%s.json" % (cloud.name, filename)
        )
        with open(new_json_file, "w+") as _json_file:
            _json_file.seek(0)
            _json_file.write(content)
        os.chmod(new_json_file, 0o644)
        copyfile(new_json_file, json_file)


def main():
    if conf["openstack_management"]:
        make_env_json("instackenv")
    if conf["openshift_management"]:
        make_env_json("ocpinventory")


if __name__ == "__main__":
    main()
