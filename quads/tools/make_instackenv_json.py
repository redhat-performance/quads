#!/usr/bin/env python3
import json
import os
import pathlib
from collections import defaultdict
from datetime import datetime
from quads.model import Cloud, Host
from quads.tools.foreman import Foreman
from quads.config import conf


def main():
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"]
    )

    cloud_list = Cloud.objects()

    if not os.path.exists(conf["json_web_path"]):
        os.makedirs(conf["json_web_path"])

    old_jsons = [file for file in os.listdir(conf["json_web_path"]) if ".json" in file]
    for file in old_jsons:
        os.remove(os.path.join(conf["json_web_path"], file))

    for cloud in cloud_list:
        host_list = Host.objects(cloud=cloud)

        foreman_password = conf["ipmi_password"]
        if cloud.ticket:
            foreman_password = cloud.ticket

        json_data = defaultdict(list)
        for host in host_list:
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
        now = datetime.now()
        if os.path.exists(json_file):
            os.rename(json_file, "%s_%s" % (json_file, now.strftime("%Y-%m-%d_%H:%M:%S")))
        with open(json_file, "w+") as _json_file:
            _json_file.seek(0)
            _json_file.write(content)
        os.chmod(json_file, 644)


if __name__ == "__main__":
    main()
