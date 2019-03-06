#! /usr/bin/env python

import logging
import os
import subprocess
from datetime import datetime

from requests import RequestException

from quads.config import conf, OFFSETS
from quads.helpers import is_supported
from quads.model import Host, Cloud
from quads.tools import make_instackenv_json
from quads.tools.badfish import Badfish
from quads.tools.foreman import Foreman
from quads.tools.juniper_set_port import juniper_set_port
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)


def move_and_rebuild(host, old_cloud, new_cloud, rebuild=False):
    logger.debug("Moving and rebuilding host: %s" % host)
    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
    )
    untouchable_hosts = conf["untouchable_hosts"]
    logger.debug("Untouchable hosts: %s" % untouchable_hosts)
    _host_obj = Host.objects(name=host).first()
    if not _host_obj.interfaces:
        logger.error("Host has no interfaces defined.")
        return False

    if host in untouchable_hosts:
        logger.error("No way...")
        return False

    _old_cloud_obj = Cloud.objects(name=old_cloud).first()
    _new_cloud_obj = Cloud.objects(name=new_cloud).first()
    _old_qinq = _old_cloud_obj.qinq

    for interface in _host_obj.interfaces:
        logger.debug("Connecting to switch on: %s" % interface.ip_address)
        ssh_helper = SSHHelper(interface.ip_address, conf["junos_username"])
        old_vlan_out = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
        old_vlan = old_vlan_out[0].split(";")[0].split()[1][7:]
        if not old_vlan:
            logger.warning(
                "Warning: Could not determine the previous VLAN for %s on %s, switch %s, switchport %s"
                % host, interface.name, interface.ip_address, interface.switch_port
            )
        else:
            old_cloud_offset = int(old_cloud[5:]) * 10
            old_base_vlan = 1090 + old_cloud_offset
            if _old_qinq:
                old_vlan = old_base_vlan + OFFSETS["em1"]
            else:
                old_vlan = old_base_vlan + OFFSETS[interface.name]

        cloud_offset = int(new_cloud[5:]) * 10
        base_vlan = 1090 + cloud_offset
        if _old_qinq:
            new_vlan = base_vlan + OFFSETS["em1"]
        else:
            new_vlan = base_vlan + OFFSETS[interface.name]

        if old_vlan != new_vlan:
            success = juniper_set_port(
                interface.ip_address,
                interface.switch_port,
                str(old_vlan),
                str(new_vlan)
            )
            if success:
                logger.info("Successfully update switch settings.")
            else:
                logger.error("There was something wrong updating switch for %s:%s" % (host, interface.name))

    make_instackenv_json.main()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    # TODO: Add user update to Foreman API Wrapper
    # hammer user update --login $new_cloud --password $foreman_user_password

    ipmi_set_pass = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "set", "password", str(conf["ipmi_cloud_username_id"]), ipmi_new_pass
    ]
    logger.debug("ipmi_set_pass: %s" % ipmi_set_pass)
    subprocess.call(ipmi_set_pass)

    ipmi_set_operator = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "priv", str(conf["ipmi_cloud_username_id"]), "0x4"
    ]
    logger.debug("ipmi_set_operator: %s" % ipmi_set_operator)
    subprocess.call(ipmi_set_operator)
    if rebuild and _new_cloud_obj.name != "cloud01":
        badfish = Badfish("mgmt-%s" % host, conf["ipmi_username"], conf["ipmi_password"])

        if "pdu_management" in conf and conf["pdu_management"]:
            # TODO: pdu management
            pass

        if is_supported(host):
            try:
                badfish.change_boot(
                    "director",
                    os.path.join(
                        os.path.dirname(__file__),
                        "../../conf/idrac_interfaces.yml"
                    )
                )
            except SystemExit as ex:
                logger.debug(ex)
                logger.error("Could not set boot order via Badfish.")
                return False

        try:
            foreman.remove_extraneous_interfaces(host)

            foreman.put_host_parameter(host, "rhel73", "false")
            foreman.put_host_parameter(host, "rhel75", "false")
            foreman.put_parameter(host, "build", 1)
            foreman.put_parameter_by_name(host, "operatingsystems", conf["foreman_default_os"])
            foreman.put_parameter_by_name(host, "ptables", conf["foreman_default_ptable"])
            foreman.put_parameter_by_name(host, "media", conf["foreman_default_medium"])
        except RequestException as ex:
            logger.debug(ex)
            logger.error("There was something wrong communicating with Foreman.")
            return False

        try:
            badfish.set_next_boot_pxe()

            badfish.reboot_server()
        except SystemExit as ex:
            logger.debug(ex)
            logger.error("There was something wrong setting next PXE boot via Badfish.")
            return False

        _host_obj.update(cloud=_new_cloud_obj, last_build=datetime.now())
        _new_cloud_obj.update(released=True)
        _old_cloud_obj.update(released=False, validated=False, notified=False)
