#! /usr/bin/env python3
import argparse
import logging
import os
import time

from quads.config import API_URL, OFFSETS, conf
from quads.model import Cloud, Host
from quads.quads import Api
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)


def verify(_cloud_name, change=False):
    _cloud_obj = Cloud.objects(name=_cloud_name).first()
    quads = Api(API_URL)

    hosts = quads.get_cloud_hosts(_cloud_name)

    for _host in hosts:
        _host_obj = Host.objects(name=_host["name"]).first()
        if _host_obj.interfaces:

            ssh_helper = SSHHelper(_host_obj.interfaces[0].ip_address, conf["junos_username"])
            for interface in _host_obj.interfaces:

                cloud_offset = int(_cloud_name[5:]) * 10
                base_vlan = 1090 + cloud_offset
                if _cloud_obj.qinq:
                    vlan = base_vlan + OFFSETS["em1"]
                else:
                    vlan = base_vlan + OFFSETS[interface.name]

                # TODO: check output
                qinq_setting = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
                vlan_member = ssh_helper.run_cmd("show vlans interfaces %s.0" % interface.switch_port)
                time.sleep(2)

                if qinq_setting != vlan:
                    logger.warning("WARNING: interface %s not using QinQ_vl%s", interface.switch_port, vlan)
                if vlan_member != vlan:
                    logger.warning("WARNING: interface %s appears to be a member of VLAN $s, should be %s",
                          interface.switch_port, vlan_member, vlan)

                if change:
                    logger.info('=== INFO: change requested')
                    scripts_dir = os.path.join(conf["install_dir"], "scripts")
                    expect_script = os.path.join(scripts_dir, "juniper-set-port.exp")

                    os.subprocess.call(
                        [expect_script,
                         interface.ip_address,
                         interface.switch_port,
                         vlan_member,
                         vlan]
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query current cloud for a given host')
    parser.add_argument('--cloud', dest='cloud', type=str, default=None,
                        help='Cloud name to verify switch configuration for.')
    parser.add_argument('--change', dest='change', action='store_true', help='Commit changes on switch.')

    args = parser.parse_args()
    verify(args.cloud, args.change)
