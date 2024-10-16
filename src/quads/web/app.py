import asyncio
import os
import re

from datetime import datetime, time

from flask import Flask, g, jsonify, redirect, render_template, request, url_for

from quads.config import Config
from quads.quads_api import APIBadRequest, APIServerException
from quads.quads_api import QuadsApi as Quads
from quads.tools.external.foreman import Foreman
from quads.web.blueprints.dynamic_content import dynamic_content_bp
from quads.web.blueprints.instack import instack_bp
from quads.web.blueprints.visual import visual_bp
from quads.web.controller.CloudOperations import CloudOperations
from quads.web.forms import ModelSearchForm

flask_app = Flask(__name__)
flask_app.url_map.strict_slashes = False
flask_app.secret_key = "flask rocks!"
flask_app.register_blueprint(dynamic_content_bp)
flask_app.register_blueprint(visual_bp, url_prefix="/visual")
flask_app.register_blueprint(instack_bp, url_prefix="/instack")

quads = Quads(Config)
loop = asyncio.new_event_loop()
foreman = Foreman(
    Config["foreman_api_url"],
    Config["foreman_username"],
    Config["foreman_password"],
    loop=loop,
)
WEB_CONTENT_PATH = Config.get("web_content_path")
EXCLUDE_DIRS = Config.get("web_exclude_dirs")


@flask_app.before_request
def before_request():
    g.dynamic_navigation = get_dynamic_navigation()


def get_dynamic_navigation():
    dynamic_navigation = {}
    links = []
    menus = {}

    files = [d.name for d in os.scandir(WEB_CONTENT_PATH) if d.is_file()]
    for file in files:
        link = {}
        if file.endswith(".html"):
            link["href"] = url_for("content.dynamic_content", page=f"{file.replace('.html','')}")
            link["text"] = file.replace(".html", "").replace("_", " ")
            links.append(link)
        else:
            with open(os.path.join(WEB_CONTENT_PATH, file)) as f:
                link["href"] = f.readline().strip()
            link["text"] = file.replace("_", " ")
            links.append(link)

    numbered_links = []
    unnumbered_links = []
    for link in links:
        ln = link["text"]
        try:
            int(ln.split()[0])
            numbered_links.append(link)
        except:
            unnumbered_links.append(link)

    sorted_numbered_links = sorted(numbered_links, key=lambda x: x["text"])
    sorted_unnumbered_links = sorted(unnumbered_links, key=lambda x: x["text"])
    stripped_numbered_links = []

    for link in sorted_numbered_links:
        link["text"] = " ".join(link["text"].split()[1:])
        stripped_numbered_links.append(link)

    links = stripped_numbered_links + sorted_unnumbered_links

    dynamic_navigation["links"] = links

    submenus = [d.name for d in os.scandir(WEB_CONTENT_PATH) if d.is_dir() and d.name not in EXCLUDE_DIRS]
    numbered_submenus = []
    unnumbered_submenus = []
    for sm in submenus:
        try:
            int(sm.split("_")[0])
            numbered_submenus.append(sm)
        except:
            unnumbered_submenus.append(sm)

    sorted_numbered_submenus = sorted(numbered_submenus, key=lambda x: x)
    sorted_unnumbered_submenus = sorted(unnumbered_submenus, key=lambda x: x)
    stripped_numbered_submenus = []
    stripped_unnumbered_submenus = []

    for sm in sorted_numbered_submenus:
        sm_dir = sm
        sm = "_".join(sm.split("_")[1:])
        stripped_numbered_submenus.append({"dir": sm_dir, "name": sm})

    for sm in sorted_unnumbered_submenus:
        sm_dir = sm
        stripped_unnumbered_submenus.append({"dir": sm_dir, "name": sm})

    submenus = stripped_numbered_submenus + stripped_unnumbered_submenus

    for sub in submenus:
        sub_links = []
        sub_path = os.path.join(WEB_CONTENT_PATH, sub["dir"])
        sub_files = [d.name for d in os.scandir(sub_path) if not d.is_dir() and d.name not in EXCLUDE_DIRS]
        html_links = [file for file in sub_files if file.endswith(".html")]
        for hl in html_links:
            href = url_for(
                "content.dynamic_content_sub",
                directory=sub["dir"],
                page=hl.replace(".html", ""),
            )
            link = {"href": href, "text": hl.replace(".html", "").replace("_", " ")}
            sub_links.append(link)

        direct_links = [file for file in sub_files if not file.endswith(".html") and not file in EXCLUDE_DIRS]
        for dl in direct_links:
            link = {}
            with open(os.path.join(WEB_CONTENT_PATH, sub["dir"], dl)) as f:
                link["href"] = f.readline().strip()
            link["text"] = dl.replace("_", " ")
            sub_links.append(link)

        numbered_sub_links = []
        unnumbered_sub_links = []
        stripped_numbered_sub_links = []

        for sl in sub_links:
            sl_name = sl["text"]
            try:
                int(sl_name.split()[0])
                numbered_sub_links.append(sl)
            except:
                unnumbered_sub_links.append(sl)

        sorted_numbered_sub_links = sorted(numbered_sub_links, key=lambda x: x["text"])
        sorted_unnumbered_sub_links = sorted(unnumbered_sub_links, key=lambda x: x["text"])

        for sl in sorted_numbered_sub_links:
            sl["text"] = " ".join(sl["text"].split()[1:])
            stripped_numbered_sub_links.append(sl)

        sub_links = stripped_numbered_sub_links + sorted_unnumbered_sub_links
        menus[sub["name"]] = sub_links
    dynamic_navigation["menus"] = menus

    return dynamic_navigation


@flask_app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("assignments"))


@flask_app.route("/assignments", methods=["GET", "POST"])
def assignments():
    headers = ["NAME", "SUMMARY", "OWNER", "REQUEST", "STATUS", "OSPENV", "OCPINV"]
    host_headers = [
        "ServerHostnamePublic",
        "OutOfBand",
        "DateStartAssignment",
        "DateEndAssignment",
        "TotalDuration",
        "TimeRemaining",
    ]
    cloud_operation = CloudOperations(quads_api=quads, foreman=foreman, loop=loop)
    clouds_summary = cloud_operation.get_cloud_summary_report()
    daily_utilization = cloud_operation.get_daily_utilization()
    managed_nodes = cloud_operation.get_managed_nodes()
    domain_broken_hosts = cloud_operation.get_domain_broken_hosts(domain=Config["domain"])
    unmanaged_hosts = cloud_operation.get_unmanaged_hosts(exclude_hosts=Config["exclude_hosts"])
    return render_template(
        "wiki/assignments.html",
        headers=headers,
        clouds_summary=clouds_summary,
        ticket_url=Config.get("ticket_url"),
        ticket_queue=Config.get("ticket_queue"),
        quads_url=Config.get("quads_url"),
        openshift_management=Config["openshift_management"],
        daily_utilization=daily_utilization,
        domain_broken_hosts=domain_broken_hosts,
        host_headers=host_headers,
        managed_nodes=managed_nodes,
        unmanaged_hosts=unmanaged_hosts,
    )


@flask_app.route("/available", methods=["GET", "POST"])
def available():
    search = ModelSearchForm(request.form)
    if request.method == "POST":
        return search_results(search)

    return render_template("wiki/available.html", form=search, available_hosts=[])


@flask_app.route("/results")
def search_results(search):
    available_hosts_list = available_hosts(search)
    return render_template("wiki/available.html", form=search, available_hosts=available_hosts_list)


@flask_app.route("/available_hosts")
def available_hosts(search):
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
                "disks": [
                    {
                        "disk_type": disk.disk_type,
                        "disk_size": disk.size_gb,
                        "disk_count": disk.count,
                    }
                    for disk in host.disks
                ],
            }
            available_hosts.append(host_dict)
    except (APIBadRequest, APIServerException):
        return jsonify({})

    return jsonify(available_hosts)


@flask_app.route("/dashboard")
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
                svctag = ""
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
                    all_hosts.setdefault(rack, []).append(
                        {
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
                        }
                    )
    return render_template("wiki/inventory.html", headers=headers, all_hosts=all_hosts)


@flask_app.route("/vlans")
def create_vlans():
    cloud_operation = CloudOperations(quads_api=quads, foreman=foreman, loop=loop)
    vlans = cloud_operation.get_vlans_list()
    return render_template("wiki/vlans.html", vlans=vlans)


if __name__ == "__main__":
    flask_app.debug = True
    flask_app.run(host="0.0.0.0", port=5001)
