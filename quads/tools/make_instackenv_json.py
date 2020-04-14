#!/usr/bin/env python3
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


def main():
    if conf["openstack_management"] or conf["openshift_management"]:
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
            if os.stat(os.path.join(conf["json_web_path"], file)).st_mtime < now - conf["json_retention_days"] * 86400:
                os.remove(os.path.join(conf["json_web_path"], file))

        for cloud in cloud_list:
            host_list = Host.objects(cloud=cloud).order_by("name")

            foreman_password = conf["ipmi_password"]
            if cloud.ticket:
                foreman_password = f"{conf['infra_location']}@{cloud.ticket}"

            osp_data = defaultdict(list)
            ocp_data = defaultdict(list)
            for host in host_list:
                if conf["foreman_unavailable"]:
                    overcloud = {"result": "true"}
                else:
                    overcloud = loop.run_until_complete(foreman.get_host_param(host.name, "overcloud"))
                if not overcloud:
                    overcloud = {"result": "true"}

                if type(overcloud["result"]) != bool:
                    _overcloud_result = strtobool(overcloud["result"])
                else:
                    _overcloud_result = overcloud["result"]

                if "result" in overcloud and _overcloud_result:
                    if conf["openstack_management"]:
                        mac = "00:00:00:00:00:00"
                        if len(host.interfaces) > 1:
                            mac = host.interfaces[1].mac_address
                        osp_data['nodes'].append({
                            'pm_password': foreman_password,
                            'pm_type': "pxe_ipmitool",
                            'mac': [mac],
                            'cpu': "2",
                            'memory': "1024",
                            'disk': "20",
                            'arch': "x86_64",
                            'pm_user': conf["ipmi_cloud_username"],
                            'pm_addr': "mgmt-%s" % host.name})
                    if conf["openshift_management"]:
                        mac = []
                        if len(host.interfaces) > 1:
                            for i in range(0, 2):
                                mac.append(host.interfaces[i].mac_address)
                        ocp_data['nodes'].append({
                            'pm_password': foreman_password,
                            'pm_type': "pxe_ipmitool",
                            'mac': mac,
                            'cpu': "2",
                            'memory': "1024",
                            'disk': "20",
                            'arch': "x86_64",
                            'pm_user': conf["ipmi_cloud_username"],
                            'pm_addr': "mgmt-%s" % host.name})

            osp_content = json.dumps(osp_data, indent=4, sort_keys=True)
            ocp_content = json.dumps(ocp_data, indent=4, sort_keys=True)

            if not os.path.exists(conf["json_web_path"]):
                pathlib.Path(conf["json_web_path"]).mkdir(parents=True, exist_ok=True)

            now = datetime.now()
            osp_new_json_file = os.path.join(
                conf["json_web_path"],
                "%s_instackenv.json_%s" % (cloud.name, now.strftime("%Y-%m-%d_%H:%M:%S"))
            )
            ocp_new_json_file = os.path.join(
                conf["json_web_path"],
                "%s_ocpinventory.json_%s" % (cloud.name, now.strftime("%Y-%m-%d_%H:%M:%S"))
            )
            osp_json_file = os.path.join(conf["json_web_path"], "%s_instackenv.json" % cloud.name)
            ocp_json_file = os.path.join(conf["json_web_path"], "%s_ocpinventory.json" % cloud.name)
            with open(osp_new_json_file, "w+") as _osp_json_file, (ocp_new_json_file, "w+") as _ocp_json_file:
                _osp_json_file.seek(0)
                _osp_json_file.write(osp_content)
                _ocp_json_file.seek(0)
                _ocp_json_file.write(ocp_content)
            os.chmod(osp_new_json_file, 0o644)
            copyfile(osp_new_json_file, osp_json_file)
            os.chmod(ocp_new_json_file, 0o644)
            copyfile(ocp_new_json_file, ocp_json_file)


if __name__ == "__main__":
    main()
