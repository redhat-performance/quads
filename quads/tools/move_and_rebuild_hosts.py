#!/usr/bin/env python3

import logging
import os
import subprocess
from datetime import datetime

from quads.config import conf, OFFSETS
from quads.helpers import is_supported
from quads.model import Host, Cloud, Vlan
from quads.tools import make_instackenv_json
from quads.tools.badfish import Badfish
from quads.tools.foreman import Foreman
from quads.tools.juniper_convert_port_public import juniper_convert_port_public
from quads.tools.juniper_set_port import juniper_set_port
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)


def get_vlan(cloud_obj, index):
    cloud_offset = int(cloud_obj.name[5:]) * 10
    base_vlan = 1090 + cloud_offset
    vlan = base_vlan + list(OFFSETS.values())[index * int(cloud_obj.qinq)]
    return vlan


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
    ssh_helper = SSHHelper(_host_obj.interfaces[0].ip_address, conf["junos_username"])
    _public_vlan_obj = Vlan.objects(cloud=_new_cloud_obj).first()
    for i, interface in enumerate(_host_obj.interfaces):
        old_vlan_out = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
        old_vlan = old_vlan_out[0].split(";")[0].split()[1][7:]
        if not old_vlan:
            logger.warning(
                "Warning: Could not determine the previous VLAN for %s on %s, switch %s, switchport %s"
                % (host, interface.name, interface.ip_address, interface.switch_port)
            )
            old_vlan = get_vlan(_old_cloud_obj, i)

        if _public_vlan_obj and i == len(_host_obj.interfaces) - 1:
            logger.info("Setting last interface to public vlan %s." % new_vlan)

            if old_vlan != _public_vlan_obj.vlan_id:
                success = juniper_convert_port_public(
                    interface.ip_address,
                    interface.switch_port,
                    str(old_vlan),
                    str(new_vlan),
                    str(_public_vlan_obj.vlan_id)
                )
                if success:
                    logger.info("Successfully update switch settings.")
                else:
                    logger.error("There was something wrong updating switch for %s:%s" % (host, interface.name))
                    return False
        else:
            new_vlan = get_vlan(_new_cloud_obj, i)

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

        if i == len(_host_obj.interfaces) - 1:
            _old_vlan_obj = Vlan.objects(cloud=_old_cloud_obj).first()
            if _old_vlan_obj:
                _old_vlan_obj.update(cloud=None)

    make_instackenv_json.main()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
    )
    foreman.update_user_password(_new_cloud_obj.name, ipmi_new_pass)

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

        foreman_success = foreman.remove_extraneous_interfaces(host)

        foreman_success = foreman_success and foreman.put_host_parameter(host, "rhel73", "false")
        foreman_success = foreman_success and foreman.put_host_parameter(host, "rhel75", "false")
        foreman_success = foreman_success and foreman.put_parameter(host, "build", 1)
        foreman_success = foreman_success and foreman.put_parameter_by_name(host, "operatingsystems", conf["foreman_default_os"])
        foreman_success = foreman_success and foreman.put_parameter_by_name(host, "ptables", conf["foreman_default_ptable"])
        foreman_success = foreman_success and foreman.put_parameter_by_name(host, "media", conf["foreman_default_medium"])
        if not foreman_success:
            logger.error("There was something wrong setting Foreman host parameters.")

        try:
            badfish.set_next_boot_pxe()
            badfish.reboot_server()
        except SystemExit as ex:
            logger.debug(ex)
            logger.error("There was something wrong setting next PXE boot via Badfish.")
            return False

        logger.debug("Updating host: %s")
        _host_obj.update(cloud=_new_cloud_obj, last_build=datetime.now())
        _new_cloud_obj.update(released=True)
        _old_cloud_obj.update(released=False, validated=False, notified=False)
