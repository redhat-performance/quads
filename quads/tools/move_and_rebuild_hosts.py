#!/usr/bin/env python3
import asyncio
import logging
import os
from datetime import datetime
from time import sleep

from quads.config import conf
from quads.helpers import is_supported, is_supermicro, get_vlan
from quads.model import Host, Cloud, Schedule
from quads.tools.badfish import badfish_factory, BadfishException
from quads.tools.foreman import Foreman
from quads.tools.juniper_convert_port_public import juniper_convert_port_public
from quads.tools.juniper_set_port import juniper_set_port
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def switch_config(host, old_cloud, new_cloud):
    _host_obj = Host.objects(name=host).first()
    _old_cloud_obj = Cloud.objects(name=old_cloud).first()
    _new_cloud_obj = Cloud.objects(name=new_cloud).first()
    if not _host_obj.interfaces:
        logger.error("Host has no interfaces defined.")
        return False
    logger.debug("Connecting to switch on: %s" % _host_obj.interfaces[0].ip_address)
    switch_ip = None
    ssh_helper = None
    for i, interface in enumerate(_host_obj.interfaces):
        if not switch_ip:
            switch_ip = interface.ip_address
            ssh_helper = SSHHelper(switch_ip, conf["junos_username"])
        else:
            if switch_ip != interface.ip_address:
                ssh_helper.disconnect()
                switch_ip = interface.ip_address
                ssh_helper = SSHHelper(switch_ip, conf["junos_username"])
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
                    old_vlan,
                    _new_cloud_obj.vlan.vlan_id
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
                    old_vlan,
                    new_vlan
                )
                if success:
                    logger.info("Successfully updated switch settings.")
                else:
                    logger.error("There was something wrong updating switch for %s:%s" % (host, interface.name))
                    return False

    if ssh_helper:
        ssh_helper.disconnect()


async def execute_ipmi(host, arguments, semaphore):
    ipmi_cmd = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
    ]
    logger.debug("Executing IPMI with argmuents: %s" % arguments)
    cmd = ipmi_cmd + arguments
    async with semaphore:
        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        logger.debug(f"{stdout.decode().strip()}")


async def ipmi_reset(host, semaphore):
    ipmi_off = [
        "chassis", "power", "off",
    ]
    await execute_ipmi(host, ipmi_off, semaphore)
    sleep(conf["ipmi_reset_sleep"])
    ipmi_on = [
        "chassis", "power", "on",
    ]
    await execute_ipmi(host, ipmi_on, semaphore)


async def move_and_rebuild(host, old_cloud, new_cloud, semaphore, rebuild=False, loop=None):
    build_start = datetime.now()
    logger.debug("Moving and rebuilding host: %s" % host)

    untouchable_hosts = conf["untouchable_hosts"]
    logger.debug("Untouchable hosts: %s" % untouchable_hosts)
    _host_obj = Host.objects(name=host).first()

    if host in untouchable_hosts:
        logger.error("No way...")
        return False

    _old_cloud_obj = Cloud.objects(name=old_cloud).first()
    _new_cloud_obj = Cloud.objects(name=new_cloud).first()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        semaphore=semaphore,
        loop=loop,
    )

    foreman_results = []

    remove_result = await foreman.remove_role(_old_cloud_obj.name, _host_obj.name)
    foreman_results.append(remove_result)

    add_result = await foreman.add_role(_new_cloud_obj.name, _host_obj.name)
    foreman_results.append(add_result)

    update_result = await foreman.update_user_password(_new_cloud_obj.name, ipmi_new_pass)
    foreman_results.append(update_result)

    for result in foreman_results:
        if isinstance(result, Exception) or not result:
            logger.error("There was something wrong setting Foreman host parameters.")
            return False

    ipmi_set_pass = [
        "user", "set", "password",
        str(conf["ipmi_cloud_username_id"]), ipmi_new_pass
    ]

    new_semaphore = asyncio.Semaphore(20)
    await execute_ipmi(host, arguments=ipmi_set_pass, semaphore=new_semaphore)

    ipmi_set_operator = [
        "user", "priv", str(conf["ipmi_cloud_username_id"]), "0x4"
    ]
    await execute_ipmi(host, arguments=ipmi_set_operator, semaphore=new_semaphore)

    if rebuild and _new_cloud_obj.name != _host_obj.default_cloud.name:
        if "pdu_management" in conf and conf["pdu_management"]:
            # TODO: pdu management
            pass

        if is_supermicro(host):
            ipmi_pxe_persistent = [
                "chassis", "bootdev", "pxe",
                "options", "=", "persistent"
            ]
            await execute_ipmi(host, arguments=ipmi_pxe_persistent, semaphore=new_semaphore)

        if is_supported(host):
            try:
                badfish = await badfish_factory("mgmt-%s" % host, conf["ipmi_username"], conf["ipmi_password"])
            except BadfishException:
                logger.error(f"Could not initialize Badfish. Verify ipmi credentials for mgmt-{host}.")
                return False
            try:
                asyncio.run_coroutine_threadsafe(badfish.change_boot(
                    "director",
                    os.path.join(
                        os.path.dirname(__file__),
                        "../../conf/idrac_interfaces.yml"
                    )
                ), loop)
            except BadfishException:
                logger.error(f"Could not set boot order via Badfish for mgmt-{host}.")
                return False

        foreman_results = []
        params = [
            {"name": "operatingsystems", "value": conf["foreman_default_os"], "identifier": "title"},
            {"name": "ptables", "value": conf["foreman_default_ptable"]},
            {"name": "media", "value": conf["foreman_default_medium"]},
        ]

        set_result = await foreman.set_host_parameter(host, "overcloud", "true")
        foreman_results.append(set_result)

        put_result = await foreman.put_parameter(host, "build", 1)
        foreman_results.append(put_result)

        put_param_result = await foreman.put_parameters_by_name(host, params)
        foreman_results.append(put_param_result)

        for result in foreman_results:
            if isinstance(result, Exception) or not result:
                logger.error("There was something wrong setting Foreman host parameters.")
                return False

        if is_supported(host):
            try:
                await badfish.boot_to_type(
                    "foreman",
                    os.path.join(
                        os.path.dirname(__file__),
                        "../../conf/idrac_interfaces.yml"
                    )
                )
                await badfish.reboot_server(graceful=False)
            except BadfishException:
                logger.error(f"Error setting PXE boot via Badfish on {host}.")
                return False
        else:
            if is_supermicro(host):
                try:
                    await ipmi_reset(host, new_semaphore)
                except Exception as ex:
                    logger.debug(ex)
                    logger.error(f"There was something wrong resetting IPMI on {host}.")

    build_delta = datetime.now() - build_start
    schedule = Schedule.current_schedule(cloud=_new_cloud_obj, host=_host_obj).first()
    if schedule:
        schedule.update(build_delta=build_delta)
        schedule.save()

    logger.debug("Updating host: %s")
    _host_obj.update(cloud=_new_cloud_obj, build=False, last_build=datetime.now())
    return True
