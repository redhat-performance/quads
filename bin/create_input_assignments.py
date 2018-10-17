#!/usr/bin/env python

import os
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
    "Graph"
]


def render_header():
    h1 = "|%s|" % "|".join(HEADERS)
    h2 = "|%s|\n" % "|".join(["---" for _ in range(len(HEADERS))])
    return "\n".join([h1, h2])


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

        style_tag_end = '</span>'
        if environment_released(_quads, None, None) or name == "cloud01":
            style_tag_start = '<span style="color:green">'
            instack_link = os.path.join(conf["quads_url"], "cloud", "%s_instackenv.json" % name)
            instack_text = "download"
        else:
            style_tag_start = '<span style="color:red">'
            instack_link = os.path.join(conf["quads_url"], "underconstruction")
            instack_text = "validating"

        _data = [
            "[%s%s%s](#%s)" % (style_tag_start, name, style_tag_end, name),
            desc,
            owner,
            link,
        ]

        if conf["gather_ansible_facts"]:
            factstyle_tag_end = '</span>'
            if os.path.exists(os.path.join(conf["ansible_facts_web_path"], "ansible_facts",
                                           "%s_overview.html" % cloud_specific_tag)):
                factstyle_tag_start = '<span style="color:green">'
                ansible_facts_link = os.path.join(conf["quads_url"], "ansible_facts",
                                                  "%s_overview.html" % cloud_specific_tag)
            else:
                factstyle_tag_start = '<span style="color:red">'
                ansible_facts_link = os.path.join(conf["quads_url"], "underconstruction")
            if name == "cloud01":
                _data.append("")
                _data.append("")
            else:
                _data.append("<a href=%s target=_blank>%s%s%s</a>" % (
                    instack_link, style_tag_start, instack_text, style_tag_end))
                _data.append("<a href=%s target=_blank>%sinventory%s</a>" % (
                    ansible_facts_link, factstyle_tag_start, factstyle_tag_end))
        else:
            if name == "cloud01":
                _data.append("")
            else:
                _data.append("<a href=%s target=_blank>%s%s%s</a>" % (
                    instack_link, style_tag_start, instack_text, style_tag_end))

        if conf["gather_dell_configs"]:
            dellstyle_tag_end = '</span>'
            if os.path.exists(conf["json_web_path"], "%s-%s-%s-dellconfig.html" % (name, owner, ticket)):
                dellstyle_tag_start = '<span style="color:green">'
                dellconfig_link = os.path.join(
                    conf["quads_url"], "cloud", "%s-%s-%s-dellconfig.html" % (name, owner, ticket))
                dellconfig_text = "view"
            else:
                dellstyle_tag_start = '<span style="color:red">'
                dellconfig_link = os.path.join(conf["quads_url"], "underconstruction")
                dellconfig_text = "unavailable"

            if name == "cloud01":
                _data.append("")
            else:
                _data.append(
                    "<a href=%s target=_blank>%s%s%s</a>" % (
                        dellconfig_link, dellstyle_tag_start, dellconfig_text, dellstyle_tag_end)
                )
        _summary.append("|".join(_data))
        _summary.append("| Total | %s |" % _host_count)
        _summary.append("")
        _summary.append("[Unmanaged Hosts](#unmanaged)")
        _summary.append("")
        _summary.append("[Faulty Hosts](#faulty)")

        return _summary


def main():
    default_config = conf["data_dir"] + "/schedule.yaml"
    default_state_dir = conf["data_dir"] + "/state"
    default_move_command = "/bin/echo"
    quads = Quads(
        default_config,
        default_state_dir,
        default_move_command,
        None, False, False, False,
    )
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["ipmi_username"],
        conf["ipmi_password"],
    )
    domain = conf["domain"]
    all_hosts = foreman.get_hosts()
    domain_hosts = {(host, properties) for host, properties in all_hosts.items() if domain in host}
    mgmt_hosts = {(host, properties) for host, properties in all_hosts.items() if host.startwith("mgmt-")}
    broken_hosts = foreman.get_broken_hosts()
    # TODO: WIP

    lines = []
    for host, properties in domain_hosts.items():
        lines.append("| %s | <a href=http://mgmt-%s/ target=_blank>console</a> |\n" % (host.split(".")[0], host))

    lines.append('### **SUMMARY**')
    _summary = print_summary(quads, len(all_hosts))
    lines.extend(_summary)


if __name__ == "__main__":
    main()
