#!/usr/bin/env python3

import os
import pathlib

import requests

from datetime import datetime
from quads.tools.foreman import Foreman
from quads.tools.csv_to_instack import csv_to_instack
from quads.config import conf, API_URL
from tempfile import NamedTemporaryFile


def main():
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"]
    )

    _cloud_response = requests.get(os.path.join(API_URL, "cloud"))
    cloud_list = []
    if _cloud_response.status_code == 200:
        cloud_list = _cloud_response.json()

    _host_response = requests.get(os.path.join(API_URL, "host"))
    host_list = []
    if _host_response.status_code == 200:
        host_list = _host_response.json()

    if not os.path.exists(conf["json_web_path"]):
        os.makedirs(conf["json_web_path"])

    old_jsons = [file for file in os.listdir(conf["json_web_path"]) if ".json" in file]
    for file in old_jsons:
        os.remove(os.path.join(conf["json_web_path"], file))

    over_cloud = foreman.get_parametrized("params.%s" % conf["foreman_director_parameter"], "true")

    columns = ["macaddress", "ipmi url", "ipmi user", "ipmi password", "ipmi tool"]
    lines = []
    for cloud in cloud_list:
        lines.append(",".join(columns))
        foreman_password = conf["ipmi_password"]
        if cloud["ticket"]:
            foreman_password = cloud["ticket"]

        for host in host_list:
            is_overcloud = host["name"] in over_cloud.keys()
            if is_overcloud:
                mac = over_cloud[host]["mac"]
                ipmi_url = "mgmt-%s" % host["name"]
                ipmi_username = conf["ipmi_cloud_username"]
                ipmi_tool = "pxe_ipmitool"
                line = ",".join([mac, ipmi_url, ipmi_username, foreman_password, ipmi_tool])
                lines.append(line)

        with NamedTemporaryFile() as ntp:
            for line in lines:
                new_line = "%s\n" % line
                ntp.write(bytes(new_line.encode("utf-8")))
            ntp.seek(0)
            content = csv_to_instack(ntp.name)

            if not os.path.exists(conf["json_web_path"]):
                pathlib.Path(conf["json_web_path"]).mkdir(parents=True, exist_ok=True)

            json_file = os.path.join(conf["json_web_path"], "%s_instackenv.json" % cloud['name'])
            now = datetime.now()
            if os.path.exists(json_file):
                os.rename(json_file, "%s_%s" % (json_file, now.strftime("%Y-%m-%d_%H:%M:%S")))
            with open(json_file, "w+") as _json_file:
                _json_file.seek(0)
                _json_file.write(content)
            os.chmod(json_file, 644)


if __name__ == "__main__":
    main()
