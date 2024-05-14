import asyncio
import os
import re
from datetime import datetime, time

from flask import Flask
from flask import render_template, request, jsonify

from quads.config import Config
from quads.quads_api import QuadsApi as Quads, APIServerException, APIBadRequest
from quads.tools.external.foreman import Foreman
from quads.web.forms import ModelSearchForm

flask_app = Flask(__name__)
flask_app.url_map.strict_slashes = False
flask_app.secret_key = "flask rocks!"

quads = Quads(Config)
loop = asyncio.new_event_loop()
foreman = Foreman(Config["foreman_api_url"],
                  Config["foreman_username"],
                  Config["foreman_password"], loop=loop)


@flask_app.route("/", methods=["GET", "POST"])
def index():
    search = ModelSearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    return render_template("index.html", form=search, available_hosts=[])


@flask_app.route("/results")
def search_results(search):
    available_hosts = available(search)
    return render_template("index.html", form=search, available_hosts=available_hosts)


@flask_app.route("/available")
def available(search):
    models = search.data["model"]
    try:
        start, end = [datetime.strptime(date, "%Y-%m-%d").date() for date in search.data["date_range"].split(" - ")]
        start = datetime.combine(start, time(hour=22)).strftime("%Y-%m-%dT%H:%M")
        end = datetime.combine(end, time(hour=22)).strftime("%Y-%m-%dT%H:%M")
    except ValueError:
        return jsonify([])

    try:
        hosts = quads.filter_available(data={"start": start, "end": end})
        if models:
            models = [model.upper() for model in models]
            hosts = [host for host in hosts if host.model in models]

        available_hosts = []
        currently_scheduled = [schedule.host_id for schedule in quads.get_current_schedules()]
        for host in hosts:
            current = True if host.id in currently_scheduled else False
            host_dict = {
                "name": host.name,
                "cloud": host.cloud.name,
                "model": host.model,
                "current": current,
                "disks": [{
                    "disk_type": disk.disk_type,
                    "disk_size": disk.size_gb,
                    "disk_count": disk.count} for disk in host.disks],
            }
            available_hosts.append(host_dict)
    except (APIBadRequest, APIServerException):
        return jsonify({})

    return jsonify(available_hosts)


@flask_app.route("/wiki")
def create_inventory():
    all_hosts = loop.run_until_complete(foreman.get_all_hosts())
    blacklist = re.compile("|".join([re.escape(word) for word in Config["exclude_hosts"].split("|")]))
    hosts = {}
    for host, properties in all_hosts.items():
        if not blacklist.search(host):
            if properties.get("sp_name", False):
                properties["host_ip"] = properties["ip"]
                properties["host_mac"] = properties["mac"]
                properties["ip"] = properties.get("sp_ip")
                properties["mac"] = properties.get("sp_mac")
                svctag_file = os.path.join(Config["data_dir"], "ipmi", host, "svctag")
                svctag = ""
                if os.path.exists(svctag_file):
                    with open(svctag_file) as _file:
                        svctag = _file.read()
                properties["svctag"] = svctag.strip()
                hosts[host] = properties
    all_hosts = {}
    headers = [
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
    for rack in Config["racks"].split():
        for host, properties in hosts.items():
            if rack in host:
                host_obj = quads.get_host(host)
                if host_obj and not host_obj.retired:
                    assignment = quads.get_active_cloud_assignment(host_obj.cloud.name)
                    owner = assignment.owner if assignment else "QUADS"
                    all_hosts.setdefault(rack, []).append({
                        "U": host_obj.name.split("-")[1][1:],
                        "ServerHostnamePublic": host_obj.name.split(".")[0],
                        "Serial": properties.get("svctag", ""),
                        "MAC": properties.get("host_mac", ""),
                        "IP": properties.get("host_ip", ""),
                        "IPMIADDR": properties.get("ip", ""),
                        "IPMIURL": host_obj.name,
                        "IPMIMAC": properties.get("mac", ""),
                        "Workload": host_obj.cloud.name,
                        "Owner": owner,
                    })
    return render_template("wiki.html", headers=headers, all_hosts=all_hosts)


if __name__ == "__main__":
    flask_app.debug = False
    flask_app.run(host="0.0.0.0", port=5001)
