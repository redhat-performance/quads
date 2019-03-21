#!/usr/bin/env python3

import os
import pathlib
import re
from datetime import datetime

import requests

from quads.config import conf, API_URL
from quads.model import Host, Schedule, Cloud
from quads.tools.foreman import Foreman

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
        "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    ]
    return lines


def print_summary():
    _summary = []
    _headers = ["**NAME**", "**SUMMARY**", "**OWNER**", "**REQUEST**", "**INSTACKENV**"]
    if conf["gather_ansible_facts"]:
        _headers.append("**HWFACTS**")
    if conf["gather_dell_configs"]:
        _headers.append("**DELLCFG**")

    _summary.append("| %s |\n" % " | ".join(_headers))
    _summary.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))

    _cloud_response = requests.get(os.path.join(API_URL, "summary"))
    _cloud_summary = []
    if _cloud_response.status_code == 200:
        _cloud_summary = _cloud_response.json()

    for cloud in [cloud for cloud in _cloud_summary if cloud["count"] > 0]:
        cloud_name = cloud["name"]
        desc = cloud["description"]
        owner = cloud["owner"]
        ticket = cloud["ticket"]
        link = "<a href=%s?id=%s target=_blank>%s</a>" % (conf["rt_url"], ticket, ticket)
        cloud_specific_tag = "%s_%s_%s" % (cloud_name, owner, ticket)

        style_tag_end = "</span>"
        if cloud["released"] or cloud_name == "cloud01":
            style_tag_start = '<span style="color:green">'
            instack_link = os.path.join(conf["quads_url"], "cloud", "%s_instackenv.json" % cloud_name)
            instack_text = "download"
        else:
            style_tag_start = '<span style="color:red">'
            instack_link = os.path.join(conf["quads_url"], "underconstruction")
            instack_text = "validating"

        _data = ["[%s%s%s](#%s)" % (style_tag_start, cloud_name, style_tag_end, cloud_name), desc, owner, link]

        if conf["gather_ansible_facts"]:
            factstyle_tag_end = "</span>"
            if os.path.exists(
                os.path.join(conf["ansible_facts_web_path"], "ansible_facts", "%s_overview.html" % cloud_specific_tag)
            ):
                factstyle_tag_start = '<span style="color:green">'
                ansible_facts_link = os.path.join(
                    conf["quads_url"], "ansible_facts", "%s_overview.html" % cloud_specific_tag
                )
            else:
                factstyle_tag_start = '<span style="color:red">'
                ansible_facts_link = os.path.join(conf["quads_url"], "underconstruction")
            if cloud_name == "cloud01":
                _data.append("")
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>"
                    % (instack_link, style_tag_start, instack_text, style_tag_end)
                )
                _data.append(
                    "<a href=%s target=_blank>%sinventory%s</a>"
                    % (ansible_facts_link, factstyle_tag_start, factstyle_tag_end)
                )
        else:
            if cloud_name == "cloud01":
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>"
                    % (instack_link, style_tag_start, instack_text, style_tag_end)
                )

        if conf["gather_dell_configs"]:
            dellstyle_tag_end = "</span>"
            dell_config_path = os.path.join(
                conf["json_web_path"],
                "%s-%s-%s-dellconfig.html" % (cloud_name, owner, ticket)
            )
            if os.path.exists(dell_config_path):
                dellstyle_tag_start = '<span style="color:green">'
                dellconfig_link = os.path.join(
                    conf["quads_url"], "cloud", "%s-%s-%s-dellconfig.html" % (cloud_name, owner, ticket)
                )
                dellconfig_text = "view"
            else:
                dellstyle_tag_start = '<span style="color:red">'
                dellconfig_link = os.path.join(conf["quads_url"], "underconstruction")
                dellconfig_text = "unavailable"

            if cloud_name == "cloud01":
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>"
                    % (dellconfig_link, dellstyle_tag_start, dellconfig_text, dellstyle_tag_end)
                )
        _summary.append("| %s |\n" % " | ".join(_data))

    _host_response = requests.get(os.path.join(API_URL, "host"))
    _hosts = []
    if _host_response.status_code == 200:
        _hosts = _host_response.json()

    _host_count = len(_hosts)
    _summary.append("| Total | %s |\n" % _host_count)
    _summary.append("\n")
    _summary.append("[Unmanaged Hosts](#unmanaged)\n")
    _summary.append("\n")
    _summary.append("[Faulty Hosts](#faulty)\n")

    return _summary


def print_unmanaged(hosts, broken_hosts):
    lines = ["\n", '### <a name="unmanaged"></a>Unmanaged systems ###\n', "\n"]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("| %s |\n" % " | ".join(_headers))
    lines.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))
    for host, properties in hosts.items():
        if not broken_hosts.get(host, False):
            real_host = host[5:]
            short_host = real_host.split(".")[0]

            _host_response = requests.get(os.path.join(API_URL, "host?name=%s" % real_host))
            _host = {}
            if _host_response.status_code == 200:
                _host = _host_response.json()

            if not _host or "name" not in _host:
                lines.append(
                    "| %s | <a href=http://%s/ target=_blank>console</a> |\n" % (short_host, host)
                )
    return lines


def print_faulty(broken_hosts):
    lines = ["\n", '### <a name="faulty"></a>Faulty systems ###\n', "\n"]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("| %s |\n" % " | ".join(_headers))
    lines.append("| %s |\n" % " | ".join(["---" for _ in range(len(_headers))]))
    for host, properties in broken_hosts.items():
        short_host = host.split(".")[0]
        lines.append("| %s | <a href=http://mgmt-%s/ target=_blank>console</a> |\n" % (short_host, host))
    return lines


def add_row(host):
    lines = []
    short_host = host.name.split(".")[0]

    _schedule_obj = Schedule.current_schedule(host=host).first()

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
    _columns = [
        short_host,
        "<a href=http://mgmt-%s/ target=_blank>console</a>" % host.name,
        _date_start.strftime("%Y-%m-%d"),
        _date_end.strftime("%Y-%m-%d"),
        total_time,
        total_time_left,
    ]
    lines.append("| %s |\n" % " | ".join(_columns))
    return lines


def main():
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"]
    )

    lines = []
    all_hosts = foreman.get_all_hosts()
    blacklist = re.compile("|".join([re.escape(word) for word in conf["exclude_hosts"].split("|")]))

    broken_hosts = foreman.get_broken_hosts()
    domain_broken_hosts = {
        host: properties
        for host, properties in broken_hosts.items()
        if conf["domain"] in host
    }

    mgmt_hosts = {}
    for host, properties in all_hosts.items():
        if not blacklist.search(host):
            mgmt_host = foreman.get_idrac_host_with_details(host)
            if mgmt_host:
                properties["host_ip"] = all_hosts.get(host, {"ip": None})["ip"]
                properties["host_mac"] = all_hosts.get(host, {"mac": None})["mac"]
                properties["ip"] = mgmt_host["ip"]
                properties["mac"] = mgmt_host["mac"]
                mgmt_hosts[mgmt_host["name"]] = properties

    lines.append("### **SUMMARY**\n")
    _summary = print_summary()
    lines.extend(_summary)
    details_header = ["\n", "### **DETAILS**\n", "\n"]
    lines.extend(details_header)
    summary_response = requests.get(os.path.join(API_URL, "summary"))
    _cloud_summary = []
    if summary_response.status_code == 200:
        _cloud_summary = summary_response.json()
    _cloud_hosts = []
    for cloud in [cloud for cloud in _cloud_summary if cloud["count"] > 0]:
        name = cloud["name"]
        owner = cloud["owner"]
        lines.append("### <a name=%s></a>\n" % name.strip())
        lines.append("### **%s -- %s**\n\n" % (name.strip(), owner))
        lines.extend(print_header())
        _cloud_hosts = requests.get(os.path.join(API_URL, "host?cloud=%s" % name))
        _cloud_obj = Cloud.objects(name=name).first()
        _hosts = Host.objects(cloud=_cloud_obj)
        for host in _hosts:
            lines.extend(add_row(host))
        lines.append("\n")

    lines.extend(print_unmanaged(mgmt_hosts, domain_broken_hosts))
    lines.extend(print_faulty(domain_broken_hosts))

    _full_path = os.path.join(conf["wp_wiki_git_repo_path"], "assignments.md")

    if not os.path.exists(conf["wp_wiki_git_repo_path"]):
        pathlib.Path(conf["wp_wiki_git_repo_path"]).mkdir(parents=True, exist_ok=True)

    with open(_full_path, "w+") as _f:
        _f.seek(0)
        for cloud in lines:
            _line = cloud if cloud else ""
            _f.write(_line)

        _f.truncate()


if __name__ == "__main__":
    main()
