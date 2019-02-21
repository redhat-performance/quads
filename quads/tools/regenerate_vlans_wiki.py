from quads.tools.racks_wiki import update_wiki
from quads.config import conf as quads_config
from quads.model import Vlan, Cloud
from tempfile import NamedTemporaryFile
from mongoengine.errors import DoesNotExist


HEADERS = [
    'VLANID',
    'IPRange',
    'NetMask',
    'Gateway',
    'IPFree',
    'Owner',
    'RTTicket',
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
        vlan_id = vlan.vlan_id
        ip_range = vlan.ip_range
        netmask = vlan.netmask
        gateway = vlan.gateway
        ip_free = vlan.ip_free
        owner = vlan.owner
        rt_ticket = vlan.ticket
        cloud_name = ""
        try:
            if vlan.cloud:
                cloud_name = Cloud.objects(id=vlan.cloud.id).first().name
        except DoesNotExist:
            pass

        columns = [
            vlan_id,
            ip_range.strip(","),
            netmask,
            gateway,
            ip_free,
            owner,
            rt_ticket,
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
