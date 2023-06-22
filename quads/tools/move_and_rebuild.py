#!/usr/bin/env python3
import asyncio
import logging
import os
from datetime import datetime
from time import sleep

from quads.config import Config
from quads.helpers import is_supported, get_vlan
from quads.quads_api import QuadsApi
from quads.tools.external.badfish import badfish_factory, BadfishException
from quads.tools.external.foreman import Foreman
from quads.tools.external.juniper import Juniper
from quads.tools.external.ssh_helper import SSHHelper, SSHHelperException

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
quads = QuadsApi(Config)


def switch_config(host, old_cloud, new_cloud):
    _host_obj = quads.get_host(host)
    _old_cloud_obj = quads.get_cloud(old_cloud)
    _new_cloud_obj = quads.get_cloud(new_cloud)
    if not _host_obj.interfaces:
        logger.error("Host has no interfaces defined.")
        return False
    logger.debug("Connecting to switch on: %s" % _host_obj.interfaces[0].switch_ip)
    switch_ip = None
    ssh_helper = None
    interfaces = sorted(_host_obj.interfaces, key=lambda k: k["name"])
    for i, interface in enumerate(interfaces):
        last_nic = i == len(_host_obj.interfaces) - 1
        if not switch_ip:
            switch_ip = interface.switch_ip
            try:
                ssh_helper = SSHHelper(switch_ip, Config["junos_username"])
            except SSHHelperException:
                logger.error(f"Failed to connect to switch: {switch_ip}")
                return False
        else:
            if switch_ip != interface.switch_ip:
                ssh_helper.disconnect()
                switch_ip = interface.switch_ip
                ssh_helper = SSHHelper(switch_ip, Config["junos_username"])
        result, old_vlan_out = ssh_helper.run_cmd(
            "show configuration interfaces %s" % interface.switch_port
        )
        old_vlan = None
        if result and old_vlan_out:
            old_vlan = old_vlan_out[0].split(";")[0].split()[1][7:]
        if not old_vlan:
            if not _new_cloud_obj.vlan and not last_nic:
                logger.warning(
                    "Warning: Could not determine the previous VLAN for %s on %s, switch %s, switchport %s"
                    % (
                        host,
                        interface.name,
                        interface.switch_ip,
                        interface.switch_port,
                    )
                )
            old_vlan = get_vlan(_old_cloud_obj, i)

        new_vlan = get_vlan(_new_cloud_obj, i)

        if _new_cloud_obj.vlan and last_nic:
            if int(old_vlan) != int(_new_cloud_obj.vlan.vlan_id):
                logger.info("Setting last interface to public vlan %s." % new_vlan)

                juniper = Juniper(
                    interface.switch_ip,
                    interface.switch_port,
                    old_vlan,
                    _new_cloud_obj.vlan.vlan_id,
                )
                success = juniper.convert_port_public()

                if success:
                    logger.info("Successfully updated switch settings.")
                else:
                    logger.error(
                        "There was something wrong updating switch for %s:%s"
                        % (host, interface.name)
                    )
                    if ssh_helper:
                        ssh_helper.disconnect()
                    return False
        else:
            if int(old_vlan) != int(new_vlan):
                juniper = Juniper(
                    interface.switch_ip, interface.switch_port, old_vlan, new_vlan
                )
                success = juniper.set_port()

                if success:
                    logger.info("Successfully updated switch settings.")
                else:
                    logger.error(
                        "There was something wrong updating switch for %s:%s"
                        % (host, interface.name)
                    )
                    if ssh_helper:
                        ssh_helper.disconnect()
                    return False

    if ssh_helper:
        ssh_helper.disconnect()

    return True


async def execute_ipmi(host, arguments, semaphore):
    ipmi_cmd = [
        "/usr/bin/ipmitool",
        "-I",
        "lanplus",
        "-H",
        "mgmt-%s" % host,
        "-U",
        Config["ipmi_username"],
        "-P",
        Config["ipmi_password"],
    ]
    logger.debug("Executing IPMI with argmuents: %s" % arguments)
    cmd = ipmi_cmd + arguments
    async with semaphore:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        logger.debug(f"{stdout.decode().strip()}")


async def ipmi_reset(host, semaphore):
    ipmi_off = [
        "chassis",
        "power",
        "off",
    ]
    await execute_ipmi(host, ipmi_off, semaphore)
    sleep(Config["ipmi_reset_sleep"])
    ipmi_on = [
        "chassis",
        "power",
        "on",
    ]
    await execute_ipmi(host, ipmi_on, semaphore)


async def move_and_rebuild(host, new_cloud, semaphore, rebuild=False, loop=None):
    build_start = datetime.now()
    logger.debug("Moving and rebuilding host: %s" % host)

    untouchable_hosts = Config["untouchable_hosts"]
    logger.debug("Untouchable hosts: %s" % untouchable_hosts)
    _host_obj = quads.get_host(host)

    if host in untouchable_hosts:
        logger.error("No way...")
        return False

    _target_cloud = quads.get_cloud(new_cloud)

    ipmi_new_pass = (
        f"{Config['infra_location']}@{_target_cloud.ticket}"
        if _target_cloud.ticket
        else Config["ipmi_password"]
    )

    ipmi_set_pass = [
        "user",
        "set",
        "password",
        str(Config["ipmi_cloud_username_id"]),
        ipmi_new_pass,
    ]

    new_semaphore = asyncio.Semaphore(20)
    await execute_ipmi(host, arguments=ipmi_set_pass, semaphore=new_semaphore)

    ipmi_set_operator = ["user", "priv", str(Config["ipmi_cloud_username_id"]), "0x4"]
    await execute_ipmi(host, arguments=ipmi_set_operator, semaphore=new_semaphore)

    badfish = None
    if rebuild and _target_cloud.name != _host_obj.default_cloud.name:
        if Config.pdu_management:
            # TODO: pdu management
            pass

        try:
            badfish = await badfish_factory(
                "mgmt-%s" % host,
                Config["ipmi_username"],
                Config["ipmi_password"],
                propagate=True,
            )
        except BadfishException:
            logger.error(
                f"Could not initialize Badfish. Verify ipmi credentials for mgmt-{host}."
            )
            return False

        if is_supported(host):
            try:
                interfaces_path = os.path.join(
                    os.path.dirname(__file__), "../../conf/idrac_interfaces.yml"
                )
                await badfish.change_boot("director", interfaces_path)

                # wait 10 minutes for the boot order job to complete
                await asyncio.sleep(600)
            except BadfishException:
                logger.error(f"Could not set boot order via Badfish for mgmt-{host}.")
                return False

        try:
            await badfish.set_power_state("on")
        except BadfishException:
            logger.error(f"Failed to power on {host}")
            return False
        foreman_results = []
        params = [
            {
                "name": "operatingsystems",
                "value": Config["foreman_default_os"],
                "identifier": "title",
            },
            {"name": "ptables", "value": Config["foreman_default_ptable"]},
            {"name": "media", "value": Config["foreman_default_medium"]},
        ]

        foreman = Foreman(
            Config["foreman_api_url"],
            Config["foreman_username"],
            Config["foreman_password"],
            semaphore=semaphore,
            loop=loop,
        )

        set_result = await foreman.set_host_parameter(host, "overcloud", "true")
        foreman_results.append(set_result)

        put_result = await foreman.put_parameter(host, "build", 1)
        foreman_results.append(put_result)

        put_param_result = await foreman.put_parameters_by_name(host, params)
        foreman_results.append(put_param_result)

        owner_id = await foreman.get_user_id(new_cloud)
        host_id = await foreman.get_host_id(host)
        put_result = await foreman.put_element("hosts", host_id, "owner_id", owner_id)
        foreman_results.append(put_result)

        for result in foreman_results:
            if isinstance(result, Exception) or not result:
                logger.error(
                    "There was something wrong setting Foreman host parameters."
                )
                return False
        if is_supported(host):
            try:
                await badfish.boot_to_type(
                    "foreman",
                    os.path.join(
                        os.path.dirname(__file__), "../../conf/idrac_interfaces.yml"
                    ),
                )
                await badfish.reboot_server(graceful=False)
            except BadfishException:
                logger.error(f"Error setting PXE boot via Badfish on {host}.")
                await badfish.reboot_server(graceful=False)
                return False
        else:
            try:
                asyncio.run_coroutine_threadsafe(
                    badfish.unmount_virtual_media(),
                    loop,
                )
            except BadfishException:
                logger.warning(f"Could not unmount virtual media for mgmt-{host}.")

            try:
                ipmi_pxe_persistent = [
                    "chassis",
                    "bootdev",
                    "pxe",
                    "options=persistent",
                ]
                await execute_ipmi(
                    host, arguments=ipmi_pxe_persistent, semaphore=new_semaphore
                )
                await ipmi_reset(host, new_semaphore)
            except Exception as ex:
                logger.debug(ex)
                logger.error(
                    f"There was something wrong setting PXE flag or resetting IPMI on {host}."
                )

    if _target_cloud.name == _host_obj.default_cloud.name:
        if not badfish:
            try:
                badfish = await badfish_factory(
                    "mgmt-%s" % host,
                    Config["ipmi_username"],
                    Config["ipmi_password"],
                    propagate=True,
                )
            except BadfishException:
                logger.error(
                    f"Could not initialize Badfish. Verify ipmi credentials for mgmt-{host}."
                )
                return False

        await badfish.set_power_state("off")
        data = {"cloud": _host_obj.cloud.name}
        source_cloud_schedule = quads.get_current_schedules(data)
        if not source_cloud_schedule:
            _old_ass_cloud_obj = quads.get_active_cloud_assignment(_host_obj.cloud)
            data = {"active": False, "vlan": None}
            quads.update_assignment(_old_ass_cloud_obj.id, data)

    data = {"host": _host_obj.name, "cloud": _target_cloud.name}
    schedule = quads.get_current_schedules(data)
    if schedule:
        data = {
            "build_start": build_start,
            "build_end": datetime.now(),
        }
        quads.update_schedule(schedule.id, data)
    logger.debug("Updating host: %s")
    data = {
        "cloud": _target_cloud.name,
        "build": False,
        "last_build": datetime.now(),
        "validated": False,
    }
    quads.update_host(_host_obj.name, data)
    return True
