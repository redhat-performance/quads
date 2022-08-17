#!/usr/bin/python3
import argparse
import asyncio
import logging
import os
import re
import socket

from datetime import datetime
from jinja2 import Template
from paramiko import SSHException
from paramiko.ssh_exception import NoValidConnectionsError

from quads.config import Config
from quads.helpers import is_supported
from quads.model import Cloud, Schedule, Host, Notification
from quads.quads_api import QuadsApi
from quads.tools.badfish import BadfishException, badfish_factory
from quads.tools.foreman import Foreman
from quads.tools.helpers import get_running_loop
from quads.tools.move_and_rebuild_hosts import switch_config
from quads.tools.netcat import Netcat
from quads.tools.postman import Postman
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)
quads = QuadsApi(Config)


class Validator(object):
    def __init__(self, cloud, _args, _loop=None):
        self.cloud = cloud
        self.report = ""
        self.args = _args
        self.hosts = quads.filter_hosts({"cloud": self.cloud.name, "validated": False})
        self.hosts = [
            host
            for host in self.hosts
            if quads.get_current_schedules({"host": host.name})
        ]
        self.loop = _loop if _loop else get_running_loop()

    def notify_failure(self):
        template_file = "validation_failed"
        with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        parameters = {
            "cloud": self.cloud.name,
            "owner": self.cloud.owner,
            "ticket": self.cloud.ticket,
            "report": self.report,
        }
        content = template.render(**parameters)

        subject = "Validation check failed for {cloud} / {owner} / {ticket}".format(
            **parameters
        )
        _cc_users = Config["report_cc"].split(",")
        postman = Postman(subject, "dev-null", _cc_users, content)
        postman.send_email()

    def notify_success(self):
        template_file = "validation_succeeded"
        with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        parameters = {
            "cloud": self.cloud.name,
            "owner": self.cloud.owner,
            "ticket": self.cloud.ticket,
        }
        content = template.render(**parameters)

        subject = "Validation check succeeded for {cloud} / {owner} / {ticket}".format(
            **parameters
        )
        _cc_users = Config["report_cc"].split(",")
        postman = Postman(subject, "dev-null", _cc_users, content)
        postman.send_email()

    def env_allocation_time_exceeded(self):
        now = datetime.now()
        data = {
            "cloud": self.cloud.name,
        }
        # TODO: Check return from get below
        schedules = quads.get_current_schedules(data)
        if schedules:
            time_delta = now - schedules[0].start
            if time_delta.seconds // 60 > Config["validation_grace_period"]:
                return True
            logger.warning(
                "You're still within the configurable validation grace period. Skipping validation for %s."
                % self.cloud.name
            )
        return False

    async def post_system_test(self):
        password = f"{Config['infra_location']}@{self.cloud.ticket}"
        foreman = Foreman(
            Config["foreman_api_url"],
            self.cloud.name,
            password,
            loop=self.loop,
        )

        valid_creds = await foreman.verify_credentials()
        if not valid_creds:
            logger.error("Unable to query Foreman for cloud: %s" % self.cloud.name)
            logger.error("Verify Foreman password is correct: %s" % password)
            self.report = (
                self.report
                + "Unable to query Foreman for cloud: %s\n" % self.cloud.name
            )
            self.report = (
                self.report + "Verify Foreman password is correct: %s\n" % password
            )
            return False

        build_hosts = await foreman.get_build_hosts()

        pending = []
        data = {"cloud": self.cloud.name}
        schedules = quads.get_current_schedules(data)
        if schedules:
            for schedule in schedules:
                if schedule.host and schedule.host.name in build_hosts:
                    pending.append(schedule.host.name)

            if pending:
                logger.info(
                    "The following hosts are marked for build and will now be rebooted:"
                )
                self.report = (
                    self.report + "The following hosts are marked for build:\n"
                )
                for host in pending:
                    logger.info(host)
                    try:
                        nc = Netcat(host)
                        healthy = await nc.health_check()
                    except OSError:
                        healthy = False
                    if not healthy:
                        logger.warning(
                            "Host %s didn't pass the health check. "
                            "Potential provisioning in process. SKIPPING." % host
                        )
                        continue
                    badfish = None
                    try:
                        badfish = await badfish_factory(
                            "mgmt-" + host,
                            str(Config["ipmi_username"]),
                            str(Config["ipmi_password"]),
                        )
                        if is_supported(host):
                            await badfish.boot_to_type(
                                "foreman",
                                os.path.join(
                                    os.path.dirname(__file__),
                                    "../../conf/idrac_interfaces.yml",
                                ),
                            )
                        else:
                            await badfish.set_next_boot_pxe()
                        await badfish.reboot_server()
                    except BadfishException as ಥ﹏ಥ:
                        logger.debug(ಥ﹏ಥ)
                        if badfish:
                            logger.warning(
                                f"There was something wrong trying to boot from Foreman interface for: {host}"
                            )
                            await badfish.reboot_server()
                        else:
                            logger.error(
                                f"Could not initiate Badfish instance for: {host}"
                            )

                    self.report = self.report + "%s\n" % host
                return False

        failed = False
        for host in self.hosts:
            try:
                badfish = await badfish_factory(
                    "mgmt-" + host.name,
                    str(Config["ipmi_cloud_username"]),
                    password,
                )
                await badfish.validate_credentials()
            except BadfishException:
                logger.info(f"Could not verify badfish credentials for: {host.name}")
                failed = True

        return not failed

    async def post_network_test(self):
        test_host = self.hosts[0]
        hosts_down = []
        switch_config_missing = []
        for host in self.hosts:
            if not host.switch_config_applied:
                data = {"host": host.name, "cloud": host.cloud.name}
                current_schedule = quads.get_current_schedules(data)
                previous_cloud = host.default_cloud.name
                previous_schedule = Schedule.objects(
                    host=host.name, end=current_schedule.start
                ).first()
                if previous_schedule:
                    previous_cloud = previous_schedule.cloud.name
                result = switch_config(host, previous_cloud, host.cloud.name)
                if result:
                    host.update(switch_config_applied=True)
                else:
                    switch_config_missing.append(host.name)
            try:
                nc = Netcat(host.name)
                healthy = await nc.health_check()
            except OSError:
                healthy = False
            if not healthy:
                hosts_down.append(host.name)
            if len(host.interfaces) > len(test_host.interfaces):
                test_host = host

        error = False
        if hosts_down:
            logger.error(
                "The following hosts appear to be down or with no ssh connection:"
            )
            for i in hosts_down:
                logger.error(i)
            error = True
        if switch_config_missing:
            logger.error("The following hosts are missing switch configuration:")
            for i in switch_config_missing:
                logger.error(i)
            error = True
        if error:
            return False

        try:
            ssh_helper = SSHHelper(test_host.name)
        except (SSHException, NoValidConnectionsError, socket.timeout) as ex:
            logger.debug(ex)
            logger.error(
                "Could not establish connection with host: %s." % test_host.name
            )
            self.report = (
                self.report
                + "Could not establish connection with host: %s.\n" % test_host.name
            )
            return False
        host_list = " ".join([host.name for host in self.hosts])

        result, output = ssh_helper.run_cmd(
            f"fping -t {Config.FPING_TIMEOUT} -B 1 -u {host_list}"
        )
        if not result:
            return False

        for i, interface in enumerate(Config.INTERFACES.keys()):
            new_ips = []
            host_ips = [
                {"ip": socket.gethostbyname(host.name), "host": host}
                for host in self.hosts
                if interface in [_interface.name for _interface in host.interfaces]
            ]
            for host in host_ips:
                _host_obj = host["host"]
                _interfaces = Config.INTERFACES[interface]
                last_nic = i == len(_host_obj.interfaces) - 1
                if last_nic and self.cloud.vlan:
                    continue
                for value in _interfaces:
                    ip_apart = host["ip"].split(".")
                    octets = value.split(".")
                    ip_apart[0] = octets[0]
                    ip_apart[1] = octets[1]
                    new_ips.append(".".join(ip_apart))

            if new_ips:
                all_ips = " ".join(new_ips)
                result, output = ssh_helper.run_cmd(
                    f"fping -t {Config.FPING_TIMEOUT} -B 1 -u {all_ips}"
                )
                if not result:
                    pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
                    hosts = []
                    for error in output:
                        ip = pattern.search(error.split()[-1])[0]
                        if ip:
                            hosts.append(ip)
                    hosts_set = set(hosts)
                    logger.warning("The following IPs are not responsive:")
                    for host in hosts_set:
                        logger.warning(host)
                    return False

        ssh_helper.disconnect()

        return True

    async def validate_env(self):
        logger.info(f"Validating {self.cloud.name}")
        notification_obj = Notification.objects(
            cloud=self.cloud, ticket=self.cloud.ticket
        ).first()
        if not notification_obj:
            notification_obj = Notification(cloud=self.cloud, ticket=self.ticket)
            notification_obj.save()
        failed = False

        if self.env_allocation_time_exceeded():
            if self.hosts:
                result_pst = await self.post_system_test()
                if not result_pst:
                    failed = True

                if not self.args.skip_network:
                    result_pnt = await self.post_network_test()
                    if not failed and not result_pnt:
                        failed = True

            # TODO: gather ansible-cmdb facts

            # TODO: quads dell config report

            if not failed:
                if not notification_obj.success:
                    self.notify_success()
                    notification_obj.update(success=True, fail=False)

                for host in self.hosts:
                    host.update(validated=True)
                self.cloud.update(validated=True)

        if failed and not notification_obj.fail:
            self.notify_failure()
            notification_obj.update(fail=True)

        return


def main(_args, _loop):
    clouds = Cloud.objects(validated=False, provisioned=True, name__ne="cloud01")
    if _args.cloud:
        clouds = [cloud for cloud in clouds if cloud.name == _args.cloud]
        if len(clouds) == 0:
            logger.error("No cloud with this name.")
    for _cloud in clouds:
        _schedule_count = Schedule.current_schedule(cloud=_cloud).count()
        if _schedule_count and _cloud.wipe:
            validator = Validator(_cloud, _args, _loop=_loop)
            try:
                _loop.run_until_complete(validator.validate_env())
            except Exception as ex:
                logger.debug(ex)
                logger.info("Failed validation for %s" % _cloud.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Quads assignments")
    parser.add_argument(
        "--skip-network",
        action="store_true",
        default=False,
        help="Skip network tests.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Show debugging information.",
    )
    parser.add_argument(
        "--cloud",
        nargs=1,
        default="",
        help="Run validation only on specified cloud."
    )
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(message)s")

    loop_main = asyncio.get_event_loop()
    asyncio.set_event_loop(loop_main)

    main(args, loop_main)
