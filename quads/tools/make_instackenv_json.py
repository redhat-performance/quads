#!/usr/bin/env python3
import json
import os
import pathlib
from collections import defaultdict
from distutils.util import strtobool

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

        for cloud in cloud_list:
            host_list = Host.objects(cloud=cloud).order_by("name")

            foreman_password = conf["ipmi_password"]
            if cloud.ticket:
                foreman_password = cloud.ticket

            json_data = defaultdict(list)
            for host in host_list[1:]:
                overcloud = foreman.get_host_param(host.name, "overcloud")
                if not overcloud:
                    overcloud = {"result": "true"}

                if "result" in overcloud and strtobool(overcloud["result"]):
                    host_data = foreman.get_idrac_host_with_details(host.name)
                    json_data['nodes'].append({
                        'pm_password': foreman_password,
                        'pm_type': "pxe_ipmitool",
                        'mac': [host_data["mac"]],
                        'cpu': "2",
                        'memory': "1024",
                        'disk': "20",
                        'arch': "x86_64",
                        'pm_user': conf["ipmi_cloud_username"],
                        'pm_addr': "mgmt-%s" % host.name})

            content = json.dumps(json_data, indent=4, sort_keys=True)

            if not os.path.exists(conf["json_web_path"]):
                pathlib.Path(conf["json_web_path"]).mkdir(parents=True, exist_ok=True)

            json_file = os.path.join(conf["json_web_path"], "%s_instackenv.json" % cloud.name)
            with open(json_file, "w+") as _json_file:
                _json_file.seek(0)
                _json_file.write(content)
            os.chmod(json_file, 644)


if __name__ == "__main__":
    main()
