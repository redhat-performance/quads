import os
import requests

from datetime import datetime
from quads.tools.foreman import Foreman
from quads.tools.csv_to_instack import csv_to_instack
from quads.config import conf
from tempfile import NamedTemporaryFile


API = 'v2'
API_URL = os.path.join(conf['quads_base_url'], 'api', API)

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
    tickets = cloud["ticket"]
    if tickets:
        foreman_password = tickets[0].get(cloud, None)
    else:
        foreman_password = conf["ipmi_password"]

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
            ntp.write("%s\n" % line)
        ntp.seek(0)
        content = csv_to_instack(ntp.name)
        json_file = os.path.join(conf["json_web_path"], "%s_instackenv.json" % cloud)
        now = datetime.now()
        os.rename(json_file, "%s_%s" % (json_file, now.strftime("%Y-%m-%d_%H:%M:%S")))
        with open(json_file, "w+") as _json_file:
            _json_file.seek(0)
            _json_file.write(content)
        os.chmod(json_file, 644)
