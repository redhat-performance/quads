#!/usr/bin/python3

from quads.tools.racks_wiki import update_wiki
from quads.config import conf as quads_config
from quads.model import Vlan, Cloud, Schedule
from tempfile import NamedTemporaryFile


HEADERS = [
    'VLANID',
    'IPRange',
    'NetMask',
    'Gateway',
    'IPFree',
    'Owner',
    'Ticket',
    'Cloud',
]


def render_header(markdown):
    header = "| %s |\n" % " | ".join(HEADERS)
    separator = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    markdown.write(header)
    markdown.write(separator)


def render_vlans(markdown):
    lines = []
    vlans = Vlan.objects().all()
    for vlan in vlans:
        cloud_obj = Cloud.objects(vlan=vlan).first()
        vlan_id = vlan.vlan_id
        ip_range = vlan.ip_range
        netmask = vlan.netmask
        gateway = vlan.gateway
        ip_free = vlan.ip_free
        cloud_current_count = Schedule.current_schedule(cloud=cloud_obj).count()
        if cloud_obj and cloud_current_count > 0:
            owner = cloud_obj.owner
            ticket = cloud_obj.ticket
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
    wp_url = "http://%s/xmlrpc.php" % quads_config["wp_wiki"]
    wp_username = quads_config["wp_username"]
    wp_password = quads_config["wp_password"]
    page_title = quads_config["wp_wiki_vlans_title"]
    page_id = quads_config["wp_wiki_vlans_page_id"]
    with NamedTemporaryFile(mode="w+t") as _markdown:
        render_header(_markdown)
        render_vlans(_markdown)
        _markdown.seek(0)
        update_wiki(wp_url, wp_username, wp_password, page_title, page_id, _markdown.name)


if __name__ == "__main__":
    regenerate_vlans_wiki()
