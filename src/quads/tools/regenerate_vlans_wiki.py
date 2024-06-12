#!/usr/bin/env python3
import logging

from xmlrpc.client import ProtocolError

from quads.quads_api import QuadsApi
from quads.tools.external.wordpress import Wordpress
from quads.config import Config
from tempfile import NamedTemporaryFile

quads = QuadsApi(Config)


HEADERS = [
    "VLANID",
    "IPRange",
    "NetMask",
    "Gateway",
    "IPFree",
    "Owner",
    "Ticket",
    "Cloud",
]

logger = logging.getLogger(__name__)


def render_header(markdown):
    header = "| %s |\n" % " | ".join(HEADERS)
    separator = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    markdown.write(header)
    markdown.write(separator)


def render_vlans(markdown):
    lines = []
    vlans = quads.get_vlans()
    for vlan in vlans:
        assignment_obj = quads.filter_assignments({"vlan_id": vlan.vlan_id})
        assignment_obj = assignment_obj[0] if assignment_obj else None
        cloud_current_count = 0
        cloud_obj = None
        if assignment_obj:
            cloud_obj = quads.filter_clouds({"name": assignment_obj.cloud.name})
            if cloud_obj:
                cloud_obj = cloud_obj[0]
                cloud_current_count = len(quads.get_current_schedules({"cloud": cloud_obj.name}))

        vlan_id = vlan.vlan_id
        ip_range = vlan.ip_range
        netmask = vlan.netmask
        gateway = vlan.gateway
        ip_free = vlan.ip_free
        if assignment_obj and cloud_current_count > 0 and cloud_obj:
            owner = assignment_obj.owner
            ticket = assignment_obj.ticket
            cloud_name = cloud_obj.name
        else:
            owner = "nobody"
            ticket = ""
            cloud_name = ""

        columns = [
            vlan_id,
            ip_range.strip(","),
            netmask,
            gateway,
            ip_free,
            owner,
            ticket,
            cloud_name,
        ]

        lines.append(columns)

    for line in sorted(lines, key=lambda _line: _line[1]):
        entry = "| %s |\n" % " | ".join([str(col) for col in line])
        markdown.write(entry)


def regenerate_vlans_wiki():
    wp_url = Config["wp_wiki"]
    wp_username = Config["wp_username"]
    wp_password = Config["wp_password"]
    page_title = Config["wp_wiki_vlans_title"]
    page_id = Config["wp_wiki_vlans_page_id"]
    with NamedTemporaryFile(mode="w+t") as _markdown:
        render_header(_markdown)
        render_vlans(_markdown)
        _markdown.seek(0)
        try:
            wiki = Wordpress(wp_url, wp_username, wp_password)
            wiki.update_page(page_title, page_id, _markdown.name)
        except ProtocolError as ex:
            logger.error(ex.errmsg)


if __name__ == "__main__":
    regenerate_vlans_wiki()
