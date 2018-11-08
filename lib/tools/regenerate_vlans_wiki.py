from racks_wiki import update_page
from tempfile import NamedTemporaryFile

import os
import yaml

HEADERS = [
    'VLAN',
    'VLANID',
    'IPRange',
    'NetMask',
    'Gateway',
    'IPFree',
    'Owner',
    'RTTicket',
    'Cloud',
]


# Load QUADS yaml config
def quads_load_config(_quads_config):
    try:
        with open(_quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError:
                print "quads: Invalid YAML config: " + _quads_config
                exit(1)
    except Exception as ex:
        print ex
        exit(1)
    return quads_config_yaml


quads_config_file = os.path.dirname(__file__) + "/../../conf/quads.yml"
quads_config = quads_load_config(quads_config_file)


def render_header(markdown):
    header = "| %s |\n" % " | ".join(HEADERS)
    separator = "| %s |\n" % " | ".join(["---" for _ in range(len(HEADERS))])
    markdown.write(header)
    markdown.write(separator)


def render_vlans(markdown):
    vlans_conf = os.path.dirname(__file__) + "/../../conf/vlans.yml"
    lines = []
    try:
        with open(vlans_conf, "r") as vlans_read:
            vlans = yaml.safe_load(vlans_read)
    except yaml.YAMLError:
        print "quads: Invalid YAML config: " + vlans_conf
        exit(1)
    for vlan, properties in vlans.iteritems():
        name = vlan
        vlan_id = properties["id"]
        ip_range = properties["iprange"]
        netmask = properties["netmask"]
        gateway = properties["gateway"]
        ip_free = properties["ipfree"]
        owner = properties["owner"]
        rt_ticket = properties["ticket"]
        cloud = "cloud%.2d" % int(properties["cloud"])

        columns = [
            name,
            vlan_id,
            ip_range.strip(","),
            netmask,
            gateway,
            ip_free,
            owner,
            rt_ticket,
            cloud,
        ]

        lines.append(columns)

    for line in sorted(lines, key=lambda _line: _line[1]):
        entry = "| %s |\n" % " | ".join([str(col) for col in line])
        markdown.write(entry)


def regenerate_vlans_wiki():
    wp_url = quads_config["wp_wiki"]
    wp_username = quads_config["wp_username"]
    wp_password = quads_config["wp_password"]
    page_title = quads_config["wp_wiki_vlans_title"]
    page_id = quads_config["wp_wiki_vlans_page_id"]
    with NamedTemporaryFile(mode="w+t") as _markdown:
        render_header(_markdown)
        render_vlans(_markdown)
        _markdown.seek(0)
        update_page(wp_url, wp_username, wp_password, _markdown.name, page_title, page_id)


if __name__ == "__main__":
    regenerate_vlans_wiki()
