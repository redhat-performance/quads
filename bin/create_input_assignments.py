#!/usr/bin/env python

import os
import re
from datetime import datetime, timedelta
from quads.helpers import quads_load_config
from quads.foreman import Foreman
from quads.quads import Quads
from quads.util import get_cloud_summary, get_owners, get_tickets

conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)

HEADERS = [
    "SystemHostname",
    "OutOfBand",
    "DateStartAssignment",
    "DateEndAssignment",
    "TotalDuration",
    "TimeRemaining",
    "Graph",
]


def print_header():
    lines = ["|%s|" % "|".join(HEADERS), "|%s|\n" % "|".join(["---" for _ in range(len(HEADERS))])]
    return lines


def environment_released(_quads, _owner, _env):
    ticket = get_tickets(_quads, _env)
    release_dir = os.path.join(conf["data_dir"], "release")
    release_file = os.path.join(release_dir, "%s-%s-%s" % (_env, _owner, ticket))
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    if os.path.exists(release_file):
        return True

    return False


def print_summary(_quads, _host_count):
    _summary = []
    _headers = ["**SUMMARY**", "**OWNER**", "**REQUEST**", "**INSTACKENV**"]
    if conf["gather_ansible_facts"]:
        _headers.append("**HWFACTS**")
    if conf["gather_dell_configs"]:
        _headers.append("**DELLCFG**")

    _summary.append("|%s|\n" % "|".join(_headers))
    _summary.append("|%s|\n" % "|".join(["---" for _ in range(len(_headers))]))

    _cloud_summary = get_cloud_summary(_quads, None, True)

    for line in _cloud_summary:
        name = line.split()[0]
        desc = line.split("(")[1][:-1]
        owner = get_owners(_quads, name)
        ticket = get_tickets(_quads, name)
        cloud_specific_tag = "%s_%s_%s" % (name, owner, ticket)
        link = ""
        if ticket:
            link = "<a href=%s?id=$rt target=_blank>%s</a>" % (conf["rt_url"], ticket)

        style_tag_end = "</span>"
        if environment_released(_quads, None, None) or name == "cloud01":
            style_tag_start = '<span style="color:green">'
            instack_link = os.path.join(conf["quads_url"], "cloud", "%s_instackenv.json" % name)
            instack_text = "download"
        else:
            style_tag_start = '<span style="color:red">'
            instack_link = os.path.join(conf["quads_url"], "underconstruction")
            instack_text = "validating"

        _data = ["[%s%s%s](#%s)" % (style_tag_start, name, style_tag_end, name), desc, owner, link]

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
            if name == "cloud01":
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
            if name == "cloud01":
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>"
                    % (instack_link, style_tag_start, instack_text, style_tag_end)
                )

        if conf["gather_dell_configs"]:
            dellstyle_tag_end = "</span>"
            if os.path.exists(conf["json_web_path"], "%s-%s-%s-dellconfig.html" % (name, owner, ticket)):
                dellstyle_tag_start = '<span style="color:green">'
                dellconfig_link = os.path.join(
                    conf["quads_url"], "cloud", "%s-%s-%s-dellconfig.html" % (name, owner, ticket)
                )
                dellconfig_text = "view"
            else:
                dellstyle_tag_start = '<span style="color:red">'
                dellconfig_link = os.path.join(conf["quads_url"], "underconstruction")
                dellconfig_text = "unavailable"

            if name == "cloud01":
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>"
                    % (dellconfig_link, dellstyle_tag_start, dellconfig_text, dellstyle_tag_end)
                )
        _summary.append("|".join(_data))
        _summary.append("| Total | %s |" % _host_count)
        _summary.append("")
        _summary.append("[Unmanaged Hosts](#unmanaged)")
        _summary.append("")
        _summary.append("[Faulty Hosts](#faulty)")

        return _summary


def print_unmanaged(quads, mgmt_hosts, broken_hosts):
    lines = ["", '### <a name="unmanaged"></a>Unmanaged systems ###', ""]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("|%s|" % "|".join(_headers))
    lines.append("|%s|" % "|".join(["---" for _ in len(_headers)]))
    for host, properties in mgmt_hosts.items():
        node_name = host[5:]
        if broken_hosts.get(node_name, True):
            short_host = host.split(".")[0]
            if quads.query_host_cloud(short_host):
                lines.append("| %s | <a href=http://%s/ target=_blank>console</a> |" % (short_host, host))
    return lines


def print_faulty(broken_hosts):
    lines = ["", '### <a name="faulty"></a>Faulty systems ###', ""]
    _headers = ["**SystemHostname**", "**OutOfBand**"]
    lines.append("|%s|" % "|".join(_headers))
    lines.append("|%s|" % "|".join(["---" for _ in len(_headers)]))
    for host, properties in broken_hosts.items():
        if host.startswith("mgmt-"):
            node_name = host[5:]
            short_host = node_name.split(".")[0]
            lines.append("| %s | <a href=http://mgmt-%s/ target=_blank>console</a> |" % (short_host, node_name))
    return lines


def add_row(quads, host):
    lines = []
    short_host = host.split(".")[0]
    default_cloud, current_cloud, current_schedule, full_schedule = quads.query_host_schedule(host, None)
    if not current_schedule:
        date_start = "∞"
        date_end = "∞"
        total_time = "∞"
        total_time_left = "∞"
    else:
        for item in full_schedule:
            for override, schedule in item.items():
                if override == current_schedule:
                    for schedkey, schedval in schedule.items():
                        if schedkey == "start":
                            date_start = schedval
                        if schedkey == "end":
                            date_end = schedval
        _date_now = datetime.now()
        _date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M")
        _date_end = datetime.strptime(date_end, "%Y-%m-%d %H:%M")
        total_sec = (_date_end - _date_start).seconds()
        total_sec_left = (_date_end - _date_now).seconds()
        total_days = total_sec / 86400
        total_days_left = total_sec_left / 86400
        total_hours = (datetime(1970, 1, 1) + timedelta(seconds=total_sec)).time().hour
        total_hours_left = (datetime(1970, 1, 1) + timedelta(seconds=total_sec_left)).time().hour
        total_time = "%s day(s)" % total_days
        total_time_left = "%s day(s)" % total_days_left
        if total_hours > 0:
            total_time = "%s, %s hour(s)" % (total_time, total_hours)
        if total_hours_left > 0:
            total_time_left = "%s, %s hour(s)" % (total_time_left, total_hours_left)
    _columns = [
        short_host,
        "<a href=http://mgmt-%s/ target=_blank>console</a>" % host,
        date_start,
        date_end,
        total_time,
        total_time_left,
        "",
    ]
    lines.append("|%s|" % "|".join(_columns))
    return lines


def main():
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

    lines = []
    all_hosts = foreman.get_hosts()
    blacklist = re.compile(conf["exclude_hosts"])

    broken_hosts = foreman.get_broken_hosts()
    domain_broken_hosts = {(host, properties) for host, properties in broken_hosts.items() if conf["domain"] in host}

    mgmt_hosts = {}
    for host, properties in all_hosts.items():
        if "mgmt" in host and not blacklist.search(host):
            properties["host_ip"] = all_hosts.get(host[5:], {"ip": None})["ip"]
            properties["host_mac"] = all_hosts.get(host[5:], {"mac": None})["mac"]
            mgmt_hosts[host] = properties

    lines.append("### **SUMMARY**")
    _summary = print_summary(quads, len(all_hosts))
    lines.extend(_summary)
    details_header = ["", "### **DETAILS**", ""]
    lines.extend(details_header)
    # TODO: call this only once
    _cloud_summary = get_cloud_summary(quads, None, True)
    _cloud_hosts = quads.query_cloud_hosts(None)
    for line in _cloud_summary:
        cloud = line.split()[0]
        owner = get_owners(quads, cloud)
        lines.append("### <a name='%s'></a>" % cloud)
        lines.append("### **'%s -- %s'**" % (line, owner))
        lines.extend(print_header())
        for host in _cloud_hosts[cloud]:
            lines.append(add_row(quads, host))
        lines.append("")

    lines.extend(print_unmanaged(quads, mgmt_hosts, domain_broken_hosts))
    lines.extend(print_faulty(domain_broken_hosts))

    _full_path = os.path.join(conf["wp_wiki_git_repo_path"], "assignments.md")

    with open(_full_path, "w") as _f:
        _f.seek(0)
        for line in lines:
            _f.write(line)

        _f.truncate()


if __name__ == "__main__":
    main()
