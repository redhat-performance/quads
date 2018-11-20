import os

from datetime import datetime
from tools.foreman import Foreman
from tools.csv_to_instack import csv_to_instack
from helpers import quads_load_config
from quads.quads import Quads
from tempfile import NamedTemporaryFile
from util import get_cloud_hosts

conf_file = os.path.join(os.path.dirname(__file__), "../../conf/quads.yml")
conf = quads_load_config(conf_file)

config_dir = os.path.join(conf["data_dir"], "ports")

default_config = conf["data_dir"] + "/schedule.yaml"
default_state_dir = conf["data_dir"] + "/state"
default_move_command = "/bin/echo"
quads = Quads(
    default_config,
    default_state_dir,
    default_move_command,
    None, False, False, False
)
foreman = Foreman(
    conf["foreman_api_url"],
    conf["foreman_username"],
    conf["foreman_password"]
)

cloud_list = quads.get_clouds()

if not os.path.exists(conf["json_web_path"]):
    os.makedirs(conf["json_web_path"])

old_jsons = [file for file in os.listdir(conf["json_web_path"]) if ".json" in file]
for file in old_jsons:
    os.remove(os.path.join(conf["json_web_path"], file))

over_cloud = foreman.get_parametrized(conf["foreman_director_parameter"], "true")

columns = ["macaddress", "ipmi url", "ipmi user", "ipmi password", "ipmi tool"]
lines = []
for cloud in cloud_list:
    lines.append(",".join(columns))
    tickets = quads.get_tickets(cloud)
    if tickets:
        foreman_password = tickets[0].get(cloud, None)
    else:
        foreman_password = conf["ipmi_password"]

    host_list = get_cloud_hosts(quads, None, cloud)

    for host in host_list:
        is_overcloud = host in over_cloud.keys()
        if is_overcloud:
            mac = over_cloud[host]["mac"]
            ipmi_url = "mgmt-%s" % host
            ipmi_username = conf["ipmi_cloud_username"]
            ipmi_tool = "pxe_ipmitool"
            line = ",".join([mac,ipmi_url,ipmi_username,foreman_password,ipmi_tool])
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
