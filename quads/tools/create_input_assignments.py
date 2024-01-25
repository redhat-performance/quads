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
    if Config["gather_ansible_facts"]:
        _headers.append("**HWFACTS**")

    _summary.append("| %s |\n" % " | ".join(_headers))
    _summary.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))

    _cloud_response = requests.get(os.path.join(Config.API_URL, "clouds/summary"))
    _cloud_summary = []
    if _cloud_response.status_code == 200:
        _cloud_summary = _cloud_response.json()

    for cloud in [cloud for cloud in _cloud_summary if cloud["count"] > 0]:
        cloud_name = cloud["name"]
        desc = "%s (%s)" % (cloud["count"], cloud["description"])
        owner = cloud["owner"]
        ticket = cloud["ticket"]
        link = "<a href=%s/%s-%s target=_blank>%s</a>" % (
            Config["ticket_url"],
            Config["ticket_queue"],
            ticket,
            ticket,
        )
        cloud_specific_tag = "%s_%s_%s" % (cloud_name, owner, ticket)

        style_tag_end = "</span>"
        if cloud["validated"] or cloud_name == "cloud01":
            style_tag_start = '<span style="color:green">'
            instack_link = os.path.join(Config["quads_url"], "cloud", "%s_instackenv.json" % cloud_name)
            instack_text = "download"
            ocpinv_link = os.path.join(Config["quads_url"], "cloud", "%s_ocpinventory.json" % cloud_name)
            ocpinv_text = "download"
            status = (
                '<span class="progress" style="margin-bottom:0px"><span role="progressbar" aria-valuenow="100" '
                'aria-valuemin="0" aria-valuemax="100" style="width:100%" class="progress-bar">100%</span></span> '
            )
        else:
            cloud_obj = quads.get_cloud(cloud_name)
            scheduled_hosts = len(quads.get_current_schedules({"cloud": cloud_obj.name}))
            moved_hosts = len(quads.filter_hosts({"cloud": cloud_obj.name}))
            percent = moved_hosts / scheduled_hosts * 100
            style_tag_start = '<span style="color:red">'
            instack_link = "#"
            instack_text = "validating"
            ocpinv_link = "#"
            ocpinv_text = "validating"
            if percent < 15:
                classes = [
                    "progress-bar",
                    "progress-bar-striped",
                    "progress-bar-danger",
                    "active",
                ]
                status = (
                    '<span class="progress" style="margin-bottom:0px"><span role="progressbar" '
                    'aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%%" '
                    'class="%s">%.0f%%</span></span>' % (" ".join(classes), percent)
                )
            else:
                classes = [
                    "progress-bar",
                    "progress-bar-striped",
                    "progress-bar-warning",
                    "active",
                ]
                status = (
                    '<span class="progress" style="margin-bottom:0px"><span role="progressbar" '
                    'aria-valuenow="%.0f" aria-valuemin="0" aria-valuemax="100" style="width:%.0f%%" '
                    'class="%s">%.0f%%</span></span>' % (percent, percent, " ".join(classes), percent)
                )

        _data = [
            "[%s%s%s](#%s)" % (style_tag_start, cloud_name, style_tag_end, cloud_name),
            desc,
            owner,
            link,
        ]

        if Config["gather_ansible_facts"]:
            factstyle_tag_end = "</span>"
            if os.path.exists(
                os.path.join(
                    Config["ansible_facts_web_path"],
                    "ansible_facts",
                    "%s_overview.html" % cloud_specific_tag,
                )
            ):
                factstyle_tag_start = '<span style="color:green">'
                ansible_facts_link = os.path.join(
                    Config["quads_url"],
                    "ansible_facts",
                    "%s_overview.html" % cloud_specific_tag,
                )
            else:
                factstyle_tag_start = '<span style="color:red">'
                ansible_facts_link = os.path.join(Config["quads_url"], "underconstruction")
            if cloud_name == "cloud01":
                _data.append("")
                _data.append("")
                _data.append(status)
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>" % (instack_link, style_tag_start, instack_text, style_tag_end)
                )
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>" % (ocpinv_link, style_tag_start, ocpinv_text, style_tag_end)
                )
                _data.append(status)
                _data.append(
                    "<a href=%s target=_blank>%sinventory%s</a>"
                    % (ansible_facts_link, factstyle_tag_start, factstyle_tag_end)
                )
        else:
            _data.append(status)
            if cloud_name == "cloud01":
                if Config["openstack_management"]:
                    _data.append("")
                if Config["openshift_management"]:
                    _data.append("")
            else:
                if Config["openstack_management"]:
                    _data.append(
                        "<a href=%s target=_blank>%s%s%s</a>"
                        % (instack_link, style_tag_start, instack_text, style_tag_end)
                    )
                if Config["openshift_management"]:
                    _data.append(
                        "<a href=%s target=_blank>%s%s%s</a>"
                        % (ocpinv_link, style_tag_start, ocpinv_text, style_tag_end)
                    )

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
    _schedules = quads.get_current_schedules({"host": host})
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
        owner = cloud["owner"]
        lines.append("### <a name=%s></a>\n" % name.strip())
        lines.append("### **%s : %s (%s) -- %s**\n\n" % (name.strip(), cloud["count"], cloud["description"], owner))
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
