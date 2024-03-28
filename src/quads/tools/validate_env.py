#!/usr/bin/env python3
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
from quads.exceptions import CliException
from quads.helpers import is_supported
from quads.quads_api import QuadsApi, APIServerException, APIBadRequest
from quads.tools.external.badfish import BadfishException, badfish_factory
from quads.tools.external.foreman import Foreman
from quads.tools.helpers import get_running_loop
from quads.tools.move_and_rebuild import switch_config
from quads.tools.external.netcat import Netcat
from quads.tools.external.postman import Postman
from quads.tools.external.ssh_helper import SSHHelper, SSHHelperException


logger = logging.getLogger(__name__)
quads = QuadsApi(Config)


class Validator(object):  # pragma: no cover
    def __init__(self, cloud, assignment, _args, _loop=None):
        self.cloud = cloud
        self.assignment = assignment
        self.report = ""
        self.args = _args
        self.hosts = quads.filter_hosts({"cloud": self.cloud, "validated": False})
        self.hosts = [
            host
            for host in self.hosts
            if quads.get_current_schedules({"host": host.name})
        ]
        if self.args.skip_hosts:
            self.hosts = [
                host for host in self.hosts if host.name not in self.args.skip_hosts
            ]
        self.loop = _loop if _loop else get_running_loop()

    def notify_failure(self):
        template_file = "validation_failed"
        with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        parameters = {
            "cloud": self.cloud,
            "owner": self.assignment.owner,
            "ticket": self.assignment.ticket,
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
            "cloud": self.cloud,
            "owner": self.assignment.owner,
            "ticket": self.assignment.ticket,
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
            "cloud": self.cloud,
        }
        schedules = quads.get_current_schedules(data)
        if schedules:
            time_delta = now - schedules[0].start
            if time_delta.total_seconds() // 60 > Config["validation_grace_period"]:
                return True
            logger.warning(
                "You're still within the configurable validation grace period. Skipping validation for %s."
                % self.cloud
            )
        return False

    async def post_system_test(self):
        password = f"{Config['infra_location']}@{self.assignment.ticket}"
        foreman = Foreman(
            Config["foreman_api_url"],
            self.cloud,
            password,
            loop=self.loop,
        )

        valid_creds = await foreman.verify_credentials()
        if not valid_creds:
            logger.error("Unable to query Foreman for cloud: %s" % self.cloud)
            logger.error("Verify Foreman password is correct: %s" % password)
            self.report = (
                self.report + "Unable to query Foreman for cloud: %s\n" % self.cloud
            )
            self.report = (
                self.report + "Verify Foreman password is correct: %s\n" % password
            )
            return False

        build_hosts = await foreman.get_build_hosts()

        pending = []
        data = {"cloud": self.cloud}
        schedules = quads.get_current_schedules(data)
        if schedules:
            for schedule in schedules:
                if schedule.host and schedule.host.name in build_hosts:
                    pending.append(schedule.host.name)

            if self.args.skip_hosts:
                pending = [host for host in pending if host not in self.args.skip_hosts]

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
            failed = await self.verify_badfish_creds(host, password)

        return not failed

    @staticmethod
    async def verify_badfish_creds(host, password):
        try:
            badfish = await badfish_factory(
                "mgmt-" + host.name,
                str(Config["ipmi_cloud_username"]),
                password,
            )
        except BadfishException:
            logger.info(f"Could not verify badfish credentials for: {host.name}")
            return True
        return False

    async def post_network_test(self):
        test_host = self.hosts[0]
        hosts_down = []
        switch_config_missing = []
        for host in self.hosts:
            if not host.switch_config_applied:
                data = {"host": host.name, "cloud": host.cloud.name}
                current_schedule = quads.get_current_schedules(data)[0]
                previous_cloud = host.default_cloud.name
                data = {
                    "host": host.name,
                    "end": current_schedule.start.strftime("%Y-%m-%dT%H:%M"),
                }
                previous_schedule = quads.get_schedules(data=data)
                if previous_schedule:
                    previous_cloud = previous_schedule[0].cloud.name
                result = switch_config(host.name, previous_cloud, host.cloud.name)
                if result:
                    try:
                        quads.update_host(host.name, {"switch_config_applied": True})
                    except (APIServerException, APIBadRequest) as ex:
                        logger.debug(str(ex))
                        logger.error("Could not update host: %s." % host.name)
                        self.report = (
                            self.report + "Could not update host: %s.\n" % host.name
                        )
                        return False
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

        if hosts_down:
            logger.error(
                "The following hosts appear to be down or with no ssh connection:"
            )
            for i in hosts_down:
                logger.error(i)
            return False

        if switch_config_missing:
            logger.error("The following hosts are missing switch configuration:")
            for i in switch_config_missing:
                logger.error(i)
            return False

        failed_ssh = False
        try:
            ssh_helper = SSHHelper(test_host.name)
        except (
            SSHHelperException,
            SSHException,
            NoValidConnectionsError,
            socket.timeout,
        ) as ex:
            logger.debug(str(ex))
            logger.error(
                "Could not establish connection with host: %s." % test_host.name
            )
            self.report = (
                self.report
                + "Could not establish connection with host: %s.\n" % test_host.name
            )
            failed_ssh = True

        if failed_ssh:
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
                if last_nic and self.assignment.vlan:
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
        logger.info(f"Validating {self.cloud}")
        failed = False
        assignment = quads.get_active_cloud_assignment(self.cloud)

        if self.env_allocation_time_exceeded():
            if self.hosts:
                if not self.args.skip_system:
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
                if not assignment.notification.success:
                    self.notify_success()
                    try:
                        quads.update_notification(
                            assignment.notification.id, {"success": True, "fail": False}
                        )
                    except (APIServerException, APIBadRequest) as ex:
                        logger.debug(str(ex))
                        logger.error(
                            "Could not update notification: %s."
                            % assignment.notification.id
                        )
                        self.report = (
                            self.report
                            + "Could not update notification: %s.\n"
                            % assignment.notification.id
                        )
                        failed = True

                for host in self.hosts:
                    try:
                        quads.update_host(host.name, {"validated": True})
                    except (APIServerException, APIBadRequest) as ex:
                        logger.debug(str(ex))
                        logger.error("Could not update host: %s." % host.name)
                        self.report = (
                            self.report + "Could not update host: %s.\n" % host.name
                        )
                        failed = True
                try:
                    quads.update_assignment(self.assignment.id, {"validated": True})
                except (APIServerException, APIBadRequest) as ex:
                    logger.debug(str(ex))
                    logger.error(
                        "Could not update assignment: %s." % self.assignment.id
                    )
                    self.report = (
                        self.report
                        + "Could not update assignment: %s.\n" % self.assignment.id
                    )
                    failed = True

        if failed and not assignment.notification.fail:
            self.notify_failure()
            try:
                quads.update_notification(assignment.notification.id, {"fail": True})
            except (APIServerException, APIBadRequest) as ex:
                logger.debug(str(ex))
                logger.error(
                    "Could not update notification: %s." % assignment.notification.id
                )
                self.report = (
                    self.report
                    + "Could not update notification: %s.\n"
                    % assignment.notification.id
                )

        return


def main(_args, _loop, _logger=None):  # pragma: no cover
    global logger
    if _logger:
        logger = _logger

    _filter = {"validated": False, "provisioned": True, "cloud__ne": "cloud01"}
    assignments = quads.filter_assignments(_filter)

    if type(_args) is dict:
        # Hack for tests to work
        _args = argparse.Namespace(**_args)

    if _args.cloud:
        try:
            cloud = quads.get_cloud(_args.cloud)
        except (APIServerException, APIBadRequest) as ex:
            raise CliException(ex)

    if _args.skip_hosts:
        hosts = []
        for hostname in _args.skip_hosts:
            try:
                host = quads.get_host(hostname)
            except (APIServerException, APIBadRequest) as ex:
                raise CliException(ex)
            hosts.append(host)

    for ass in assignments:
        _schedules = quads.get_current_schedules(data={"cloud": ass.cloud.name})
        _schedule_count = len(_schedules)

        _assignment = quads.get_active_cloud_assignment(ass.cloud.name)
        if _schedule_count and _assignment.wipe:
            validator = Validator(ass.cloud.name, _assignment, _args, _loop=_loop)
            try:
                _loop.run_until_complete(validator.validate_env())
            except Exception as ex:
                logger.debug(ex)
                logger.info("Failed validation for %s" % ass.cloud.name)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Validate Quads assignments")
    parser.add_argument(
        "--skip-system",
        action="store_true",
        default=False,
        help="Skip system tests.",
    )
    parser.add_argument(
        "--skip-network",
        action="store_true",
        default=False,
        help="Skip network tests.",
    )
    parser.add_argument(
        "--skip-hosts",
        action="append",
        nargs="*",
        help="Skip specific hosts.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Show debugging information.",
    )
    parser.add_argument(
        "--cloud", default="", help="Run validation only on specified cloud."
    )
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(message)s")

    loop_main = asyncio.get_event_loop()
    asyncio.set_event_loop(loop_main)

    main(args, loop_main)
