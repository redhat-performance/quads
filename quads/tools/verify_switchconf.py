#!/usr/bin/python3

import argparse
import logging

from quads.config import conf
from quads.helpers import get_vlan
from quads.model import Cloud, Host
from quads.tools.juniper_convert_port_public import juniper_convert_port_public
from quads.tools.juniper_set_port import juniper_set_port
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


def verify(_cloud_name, _host_name, change=False):
    if _host_name:
        _host_obj = Host.objects(name=_host_name).first()
    _cloud_obj = Cloud.objects(name=_cloud_name).first()

    if _host_obj:
        hosts = [_host_obj]
    else:
        hosts = Host.objects(cloud=_cloud_obj)

    for _host_obj in hosts:
        logger.info(f"Host: {_host_obj.name}")
        if _host_obj.interfaces:
            interfaces = sorted(_host_obj.interfaces, key=lambda k: k["name"])
            for i, interface in enumerate(interfaces):
                ssh_helper = SSHHelper(interface.ip_address, conf["junos_username"])
                last_nic = i == len(_host_obj.interfaces) - 1
                vlan = get_vlan(_cloud_obj, i, last_nic)

                try:
                    _, old_vlan_out = ssh_helper.run_cmd(
                        "show configuration interfaces %s" % interface.switch_port
                    )
                    old_vlan = old_vlan_out[0].split(";")[0].split()[1]
                    if old_vlan.startswith("QinQ"):
                        old_vlan = old_vlan[7:]
                except IndexError:
                    old_vlan = 0

                try:
                    _, vlan_member_out = ssh_helper.run_cmd(
                        "show configuration vlans | display set | match %s.0"
                        % interface.switch_port
                    )
                    vlan_member = vlan_member_out[0].split()[2][4:].strip(",")
                except IndexError:
                    if not _cloud_obj.vlan and not last_nic:
                        logger.warning(
                            "Could not determine the previous VLAN member for %s, switch %s, switch port %s "
                            % (
                                interface.name,
                                interface.ip_address,
                                interface.switch_port,
                            )
                        )
                    vlan_member = 0

                ssh_helper.disconnect()

                if int(old_vlan) != int(vlan):
                    logger.warning(
                        "Interface %s not using QinQ_vl%s", interface.switch_port, vlan
                    )

                if int(vlan_member) != int(vlan):
                    logger.warning(
                        "Interface %s appears to be a member of VLAN %s, should be %s",
                        interface.switch_port,
                        vlan_member,
                        vlan,
                    )

                    if change:
                        if _cloud_obj.vlan and last_nic:
                            if int(_cloud_obj.vlan.vlan_id) != int(old_vlan):

                                logger.info(f"Change requested for {interface.name}")
                                logger.info(
                                    "Setting last interface to public vlan %s."
                                    % _cloud_obj.vlan.vlan_id
                                )

                                success = juniper_convert_port_public(
                                    interface.ip_address,
                                    interface.switch_port,
                                    old_vlan,
                                    vlan,
                                )
                            else:
                                logger.info(f"No changes required for {interface.name}")
                                continue
                        else:
                            logger.info(f"Change requested for {interface.name}")
                            success = juniper_set_port(
                                interface.ip_address,
                                interface.switch_port,
                                vlan_member,
                                vlan,
                            )

                        if success:
                            logger.info("Successfully updated switch settings.")
                        else:
                            logger.error(
                                f"There was something wrong updating switch for {interface.name}"
                            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify switch configs for a cloud or host")
    parser.add_argument(
        "--cloud",
        dest="cloud",
        type=str,
        default=None,
        required=True,
        help="Cloud name to verify switch configuration for.",
    )
    parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default=None,
        help="Host name to verify switch configuration for.",
    )
    parser.add_argument(
        "--change", dest="change", action="store_true", help="Commit changes on switch."
    )

    args = parser.parse_args()
    verify(args.cloud, args.host, args.change)
