#!/usr/bin/env python3

import logging
import os
import subprocess
from datetime import datetime
from time import sleep

from quads.config import conf
from quads.helpers import is_supported, is_supermicro, get_vlan
from quads.model import Host, Cloud
from quads.tools.badfish import Badfish
from quads.tools.foreman import Foreman
from quads.tools.juniper_convert_port_public import juniper_convert_port_public
from quads.tools.juniper_set_port import juniper_set_port
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def execute_ipmi(host, arguments):
    ipmi_cmd = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
    ]
    logger.debug("Executing IPMI with argmuents: %s" % arguments)
    subprocess.call(ipmi_cmd + arguments)


def ipmi_reset(host):
    ipmi_off = [
        "chassis", "power", "off",
    ]
    execute_ipmi(host, ipmi_off)
    sleep(conf["ipmi_reset_sleep"])
    ipmi_on = [
        "chassis", "power", "on",
    ]
    execute_ipmi(host, ipmi_on)


def move_and_rebuild(host, old_cloud, new_cloud, rebuild=False):
    logger.debug("Moving and rebuilding host: %s" % host)

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

    logger.debug("Connecting to switch on: %s" % _host_obj.interfaces[0].ip_address)
    for i, interface in enumerate(_host_obj.interfaces):
        ssh_helper = SSHHelper(interface.ip_address, conf["junos_username"])
        old_vlan_out = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
        old_vlan = None
        if old_vlan_out:
            old_vlan = old_vlan_out[0].split(";")[0].split()[1][7:]
        if not old_vlan:
            logger.warning(
                "Warning: Could not determine the previous VLAN for %s on %s, switch %s, switchport %s"
                % (host, interface.name, interface.ip_address, interface.switch_port)
            )
            old_vlan = get_vlan(_old_cloud_obj, i)

        new_vlan = get_vlan(_new_cloud_obj, i)

        if _new_cloud_obj.vlan and i == len(_host_obj.interfaces) - 1:
            logger.info("Setting last interface to public vlan %s." % new_vlan)

            if int(old_vlan) != int(_new_cloud_obj.vlan.vlan_id):
                success = juniper_convert_port_public(
                    interface.ip_address,
                    interface.switch_port,
                    str(old_vlan),
                    str(_new_cloud_obj.vlan.vlan_id)
                )
                if success:
                    logger.info("Successfully updated switch settings.")
                else:
                    logger.error("There was something wrong updating switch for %s:%s" % (host, interface.name))
                    return False
        else:

            if int(old_vlan) != int(new_vlan):
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
                    return False

        ssh_helper.disconnect()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
    )
    foreman.remove_role(_old_cloud_obj.name, _host_obj.name)
    foreman.add_role(_new_cloud_obj.name, _host_obj.name)
    foreman.update_user_password(_new_cloud_obj.name, ipmi_new_pass)

    ipmi_set_pass = [
        "user", "set", "password",
        str(conf["ipmi_cloud_username_id"]), ipmi_new_pass
    ]
    execute_ipmi(host, arguments=ipmi_set_pass)

    ipmi_set_operator = [
        "user", "priv", str(conf["ipmi_cloud_username_id"]), "0x4"
    ]
    execute_ipmi(host, arguments=ipmi_set_operator)

    if rebuild and _new_cloud_obj.name != _host_obj.default_cloud.name:
        if "pdu_management" in conf and conf["pdu_management"]:
            # TODO: pdu management
            pass

        if is_supermicro(host):
            ipmi_pxe_persistent = [
                "chassis", "bootdev", "pxe",
                "options", "=", "persistent"
            ]
            execute_ipmi(host, arguments=ipmi_pxe_persistent)

        if is_supported(host):
            try:
                badfish = Badfish("mgmt-%s" % host, conf["ipmi_username"], conf["ipmi_password"])
            except SystemExit:
                logger.exception("Could not initialize Badfish. Verify ipmi credentials.")
                return False
            try:
                badfish.change_boot(
                    "director",
                    os.path.join(
                        os.path.dirname(__file__),
                        "../../conf/idrac_interfaces.yml"
                    )
                )
            except SystemExit:
                logger.exception("Could not set boot order via Badfish.")
                badfish.reboot_server()
                return False

        foreman_success = foreman.set_host_parameter(host, "overcloud", "true")
        foreman_success = foreman.put_parameter(host, "build", 1) and foreman_success
        foreman_success = foreman.put_parameter_by_name(
            host, "operatingsystems", conf["foreman_default_os"], "title"
        ) and foreman_success
        foreman_success = foreman.put_parameter_by_name(
            host, "ptables", conf["foreman_default_ptable"]
        ) and foreman_success
        foreman_success = foreman.put_parameter_by_name(
            host, "media", conf["foreman_default_medium"]
        ) and foreman_success
        if not foreman_success:
            logger.error("There was something wrong setting Foreman host parameters.")

        if is_supported(host):
            try:
                badfish.boot_to_type(
                    "foreman",
                    os.path.join(
                        os.path.dirname(__file__),
                        "../../conf/idrac_interfaces.yml"
                    )
                )
                badfish.reboot_server(graceful=False)
            except SystemExit:
                logger.exception("Error setting PXE boot via Badfish on: %s." % host)
                return False
        else:
            if is_supermicro(host):
                ipmi_reset(host)

        logger.debug("Updating host: %s")
        _host_obj.update(cloud=_new_cloud_obj, build=False, last_build=datetime.now())
    else:

        logger.debug("Updating host: %s")
        _host_obj.update(cloud=_new_cloud_obj, build=False, last_build=datetime.now())
    return True
