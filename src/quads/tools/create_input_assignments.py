#!/usr/bin/env python3
import asyncio
import os
import pathlib
import re
import requests

from datetime import datetime
from quads.config import Config
from quads.quads_api import QuadsApi, APIBadRequest, APIServerException
from quads.tools.external.foreman import Foreman

quads = QuadsApi(Config)

HEADERS = [
    "ServerHostnamePublic",
    "OutOfBand",
    "DateStartAssignment",
    "DateEndAssignment",
    "TotalDuration",
    "TimeRemaining",
]


def print_header():
    lines = [
        "| %s |\n" % " | ".join(HEADERS),
        "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))]),
    ]
    return lines


def print_summary():
    _summary = []
    _headers = [
        "**NAME**",
        "**SUMMARY**",
        "**OWNER**",
        "**REQUEST**",
        '<span id="status">**STATUS**</span>',
    ]
    if Config["openstack_management"]:
        _headers.append("**OSPENV**")
    if Config["openshift_management"]:
        _headers.append("**OCPINV**")

    _summary.append("| %s |\n" % " | ".join(_headers))
    _summary.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))

    _cloud_response = requests.get(os.path.join(Config.API_URL, "clouds/summary"))
    _cloud_summary = []
    if _cloud_response.status_code == 200:
        _cloud_summary = _cloud_response.json()

    for cloud in [cloud for cloud in _cloud_summary if cloud["count"] > 0]:
        cloud_name = cloud["name"]
        cloud_description = cloud["description"] if cloud["description"] else Config["spare_pool_description"]
        desc = f"{cloud_description} ({cloud['count']})"
        owner = cloud["owner"] if cloud["owner"] else Config["spare_pool_owner"]
        ticket = cloud["ticket"]
        ticket_link = "<a href=%s/%s-%s target=_blank>%s</a>" % (
            Config["ticket_url"],
            Config["ticket_queue"],
            ticket,
            ticket,
        )

        style_tag_end = "</span>"

        is_valid = cloud["validated"] or cloud_name == "cloud01"

        percent = 100
        if not is_valid:
            cloud_obj = quads.get_cloud(cloud_name)
            scheduled_hosts = len(quads.get_current_schedules({"cloud": cloud_obj.name}))
            moved_hosts = len(quads.filter_hosts({"cloud": cloud_obj.name}))
            percent = moved_hosts / scheduled_hosts * 100
        style_color = "green" if is_valid else "red"
        style_tag_start = f'<span style="color:{style_color}">'

        _data = [
            "[%s%s%s](#%s)" % (style_tag_start, cloud_name, style_tag_end, cloud_name),
            desc,
            owner,
            ticket_link,
        ]
        dangerous = percent < 15
        danger_class = "danger" if dangerous else "warning"

        classes = ["progress-bar"]
        if not is_valid or percent != 100:
            classes.append("progress-bar-striped")
            classes.append(f"progress-bar-{danger_class}")
            classes.append("active")

        status = (
            '<span class="progress" style="margin-bottom:0px"><span role="progressbar" '
            'aria-valuenow="%.0f" aria-valuemin="0" aria-valuemax="100" style="width:%.0f%%" '
            'class="%s">%.0f%%</span></span>' % (percent, percent, " ".join(classes), percent)
        )

        _data.append(status)
        if Config["openstack_management"]:
            filename = f"{cloud_name}_instackenv.json"
            json_link = get_json_link(cloud_name, filename, is_valid, style_tag_start, style_tag_end)
            _data.append(json_link)
        if Config["openshift_management"]:
            filename = f"{cloud_name}_ocpinventory.json"
            json_link = get_json_link(cloud_name, filename, is_valid, style_tag_start, style_tag_end)
            _data.append(json_link)

        _summary.append("| %s |\n" % " | ".join(_data))

    _host_count = len(quads.filter_hosts({"broken": False, "retired": False}))
    _schedules = len(quads.get_current_schedules())
    _daily_percentage = _schedules * 100 // _host_count
    _summary.append(f"| Total | {_host_count} |\n")
    _summary.append("\n")
    _summary.append(f"Daily Utilization: {_daily_percentage}% \n")
    _summary.append("\n")
    _summary.append("[Unmanaged Hosts](#unmanaged)\n")
    _summary.append("\n")
    _summary.append("[Faulty Hosts](#faulty)\n")

    return _summary


def get_json_link(cloud_name, filename, is_valid, style_tag_start, style_tag_end):
    if cloud_name == "cloud01":
        return ""
    _link = os.path.join(Config["quads_url"], "instack", filename) if is_valid else "#"
    _text = "download" if is_valid else "validating"
    return "<a href=%s target=_blank>%s%s%s</a>" % (_link, style_tag_start, _text, style_tag_end)


def print_unmanaged(hosts):
    lines = ["\n", '### <a name="unmanaged"></a>Unmanaged systems ###\n', "\n"]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("| %s |\n" % " | ".join(_headers))
    lines.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))
    for host, properties in hosts.items():
        real_host = host[5:]
        try:
            host_obj = quads.get_host(real_host)
        except (APIBadRequest, APIServerException):
            host_obj = None

        if not host_obj:
            short_host = real_host.split(".")[0]
            lines.append("| %s | <a href=http://%s/ target=_blank>console</a> |\n" % (short_host, host))
    return lines


def print_faulty(broken_hosts):
    lines = ["\n", '### <a name="faulty"></a>Faulty systems ###\n', "\n"]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("| %s |\n" % " | ".join(_headers))
    lines.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))
    for host in broken_hosts:
        short_host = host.name.split(".")[0]
        lines.append("| %s | <a href=http://mgmt-%s/ target=_blank>console</a> |\n" % (short_host, host.name))
    return lines


def add_row(host):
    lines = []
    short_host = host.name.split(".")[0]

    _schedule_obj = None
    _schedules = quads.get_current_schedules({"host": host.name})
    if _schedules:
        _schedule_obj = _schedules[0]

    if not _schedule_obj:
        _date_start = "∞"
        _date_end = "∞"
        total_time = "∞"
        total_time_left = "∞"
    else:
        _date_now = datetime.now()
        _date_start = _schedule_obj.start
        _date_end = _schedule_obj.end
        total_sec_left = (_date_end - _date_now).total_seconds()
        total_days = (_date_end - _date_start).days
        total_days_left = total_sec_left // 86400
        total_hours_left = ((total_sec_left / 86400) - total_days_left) * 24
        total_time = "%0d day(s)" % total_days
        total_time_left = "%0d day(s)" % total_days_left
        if total_hours_left > 1:
            total_time_left = "%s, %0d hour(s)" % (total_time_left, total_hours_left)
        _date_start = _date_start.strftime("%Y-%m-%d")
        _date_end = _date_end.strftime("%Y-%m-%d")
    _columns = [
        short_host,
        "<a href=http://mgmt-%s/ target=_blank>console</a>" % host.name,
        _date_start,
        _date_end,
        total_time,
        total_time_left,
    ]
    lines.append("| %s |\n" % " | ".join(_columns))
    return lines


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    foreman = Foreman(
        Config["foreman_api_url"],
        Config["foreman_username"],
        Config["foreman_password"],
        loop=loop,
    )

    lines = []
    all_hosts = loop.run_until_complete(foreman.get_all_hosts())
    blacklist = re.compile("|".join([re.escape(word) for word in Config["exclude_hosts"].split("|")]))

    broken_hosts = quads.filter_hosts({"broken": False})
    domain_broken_hosts = [host for host in broken_hosts if Config["domain"] in host.name]

    mgmt_hosts = {}
    for host, properties in all_hosts.items():
        if not blacklist.search(host):
            if properties.get("sp_name", False):
                properties["host_ip"] = all_hosts.get(host, {"ip": None})["ip"]
                properties["host_mac"] = all_hosts.get(host, {"mac": None})["mac"]
                properties["ip"] = properties.get("sp_ip")
                properties["mac"] = properties.get("sp_mac")
                mgmt_hosts[properties.get("sp_name")] = properties

    lines.append("### **SUMMARY**\n")
    _summary = print_summary()
    lines.extend(_summary)
    details_header = ["\n", "### **DETAILS**\n", "\n"]
    lines.extend(details_header)
    summary_response = requests.get(os.path.join(Config.API_URL, "clouds/summary"))
    _cloud_summary = []
    if summary_response.status_code == 200:
        _cloud_summary = summary_response.json()
    for cloud in [cloud for cloud in _cloud_summary if cloud["count"] > 0]:
        name = cloud["name"]
        owner = cloud["owner"] if cloud["owner"] else Config["spare_pool_owner"]
        cloud_description = cloud["description"] if cloud["description"] else Config["spare_pool_description"]
        desc = f"{cloud_description} ({cloud['count']})"
        lines.append("### <a name=%s></a>\n" % name.strip())
        lines.append(f"### **{name.strip()} : {desc} -- {owner}**\n\n")
        lines.extend(print_header())
        _cloud_obj = quads.get_cloud(name)
        _hosts = sorted(
            quads.filter_hosts({"cloud": _cloud_obj.name, "retired": False, "broken": False}),
            key=lambda x: x.name,
        )
        for host in _hosts:
            lines.extend(add_row(host))
        lines.append("\n")

    lines.extend(print_unmanaged(mgmt_hosts))
    lines.extend(print_faulty(domain_broken_hosts))

    _full_path = os.path.join(Config["wp_wiki_git_repo_path"], "assignments.md")

    if not os.path.exists(Config["wp_wiki_git_repo_path"]):
        pathlib.Path(Config["wp_wiki_git_repo_path"]).mkdir(parents=True, exist_ok=True)

    with open(_full_path, "w+") as _f:
        _f.seek(0)
        for cloud in lines:
            _line = cloud if cloud else ""
            _f.write(_line)

        _f.truncate()


if __name__ == "__main__":
    main()
