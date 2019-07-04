#!/usr/bin/env python3

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


def main():
    if conf["openstack_management"]:
        foreman = Foreman(
            conf["foreman_api_url"],
            conf["foreman_username"],
            conf["foreman_password"]
        )

        cloud_list = Cloud.objects()

        if not os.path.exists(conf["json_web_path"]):
            os.makedirs(conf["json_web_path"])

        now = time.time()
        old_jsons = [file for file in os.listdir(conf["json_web_path"]) if ":" in file]
        for file in old_jsons:
            if os.stat(os.path.join(conf["json_web_path"], file)).st_mtime < now - conf["json_retention_days"] * 86400:
                os.remove(os.path.join(conf["json_web_path"], file))

        for cloud in cloud_list:
            foreman_password = conf["ipmi_password"]
            if cloud.ticket:
                foreman_password = cloud.ticket

            json_data = defaultdict(list)
            if conf["foreman_unavailable"]:
                overcloud = {"result": "true"}
            else:
                overcloud = foreman.get_host_param(host.name, "overcloud")
            if not overcloud:
                overcloud = {"result": "true"}
            if "result" in overcloud and strtobool(overcloud["result"]):
                mac = "00:00:00:00:00:00"
                if len(host.interfaces) > 1:
                    mac = host.interfaces[1].mac_address
                json_data['nodes'].append({
                    'pm_password': foreman_password,
                    'pm_type': "pxe_ipmitool",
                    'mac': [mac],
                    'cpu': "2",
                    'memory': "1024",
                    'disk': "20",
                    'arch': "x86_64",
                    'pm_user': conf["ipmi_cloud_username"],
                    'pm_addr': "mgmt-%s" % host.name})

            content = json.dumps(json_data, indent=4, sort_keys=True)

            if not os.path.exists(conf["json_web_path"]):
                pathlib.Path(conf["json_web_path"]).mkdir(parents=True, exist_ok=True)

            now = datetime.now()
            new_json_file = os.path.join(
                conf["json_web_path"],
                "%s_instackenv.json_%s" % (cloud.name, now.strftime("%Y-%m-%d_%H:%M:%S"))
            )
            json_file = os.path.join(conf["json_web_path"], "%s_instackenv.json" % cloud.name)
            with open(new_json_file, "w+") as _json_file:
                _json_file.seek(0)
                _json_file.write(content)
            os.chmod(new_json_file, 0o644)
            copyfile(new_json_file, json_file)


if __name__ == "__main__":
    main()
