#!/usr/bin/python3

import logging
import os
import socket

from datetime import datetime, timedelta
from jinja2 import Template
from quads.config import conf, TEMPLATES_PATH, API_URL, INTERFACES
from quads.quads import Api
from quads.model import Cloud, Schedule, Host, Notification
from quads.tools.foreman import Foreman
from quads.tools.postman import Postman
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Validator(object):
    def __init__(self, cloud):
        self.cloud = cloud
        self.report = ""

    def notify_failure(self):
        template_file = "validation_failed"
        with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        parameters = {
            "cloud": self.cloud.name,
            "owner": self.cloud.owner,
            "ticket": self.cloud.ticket,
            "report": self.report,
        }
        content = template.render(**parameters)

        subject = "Validation check failed for {cloud} / {owner} / {ticket}".format(**parameters)
        _cc_users = conf["report_cc"].split(",")
        postman = Postman(subject, "dev-null", _cc_users, content)
        postman.send_email()

    def notify_success(self):
        template_file = "validation_succeded"
        with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        parameters = {
            "cloud": self.cloud.name,
            "owner": self.cloud.owner,
            "ticket": self.cloud.ticket,
        }
        content = template.render(**parameters)

        subject = "Validation check succeeded for {cloud} / {owner} / {ticket}".format(**parameters)
        _cc_users = conf["report_cc"].split(",")
        postman = Postman(subject, "dev-null", _cc_users, content)
        postman.send_email()

    def env_allocation_time_exceeded(self):
        now = datetime.now()
        schedule = Schedule.objects(cloud=self.cloud, start__lt=now, end__gt=now).first()
        time_delta = now - schedule.start
        if time_delta.seconds//60 > conf["validation_grace_period"]:
            return True
        return False

    def post_system_test(self):
        foreman = Foreman(
            conf["foreman_api_url"],
            self.cloud.name,
            self.cloud.ticket
        )

        quads = Api(API_URL)

        if not foreman.verify_credentials():
            logger.error("Unable to query Foreman for cloud: %s" % self.cloud.name)
            logger.error("Verify Foreman password is correct: %s" % self.cloud.ticket)
            self.report = self.report + "Unable to query Foreman for cloud: %s\n" % self.cloud.name
            self.report = self.report + "Verify Foreman password is correct: %s\n" % self.cloud.ticket
            return False

        build_hosts = foreman.get_build_hosts()

        pending = []
        schedules = quads.get_current_schedule(cloud=self.cloud.name)
        if "result" not in schedules:
            for schedule in schedules:
                host = quads.get_hosts(id=schedule["host"]["$oid"])
                if host and host['name'] in build_hosts:
                    pending.append(host["name"])

            if pending:
                logger.info("The following hosts are marked for build:")
                self.report = self.report + "The following hosts are marked for build:\n"
                for host in pending:
                    logger.info(host)
                    self.report = self.report + "%s\n" % host
                return False

        return True

    def post_network_test(self):
        _hosts = Host.objects(cloud=self.cloud)

        test_host = _hosts[0]
        try:
            ssh_helper = SSHHelper(test_host.name)
        except Exception:
            logger.exception("Could not establish connection with host: %s." % test_host.name)
            self.report = self.report + "Could not establish connection with host: %s.\n" % test_host.name
            return False
        host_list = " ".join([host.name for host in _hosts])

        if type(ssh_helper.run_cmd("fping -u %s" % host_list)) != list:
            return False

        for interface in test_host.interfaces:
            new_ips = []
            host_ips = [
                socket.gethostbyname(host.name) for host in _hosts
                if interface.name in [_interface.name for _interface in host.interfaces]
            ]
            for ip in host_ips:
                for value in INTERFACES[interface.name]:
                    ip_apart = ip.split(".")
                    octets = value.split(".")
                    ip_apart[0] = octets[0]
                    ip_apart[1] = octets[1]
                    new_ips.append(".".join(ip_apart))

            if type(ssh_helper.run_cmd("fping -u %s" % " ".join(new_ips))) != list:
                return False

        ssh_helper.disconnect()

        return True

    def validate_env(self):
        notification_obj = Notification.objects(
            cloud=self.cloud,
            ticket=self.cloud.ticket
        ).first()
        failed = False

        if self.env_allocation_time_exceeded():
            if not self.post_system_test():
                failed = True

            if not self.post_network_test():
                failed = True

            # TODO: gather ansible-cmdb facts

            # TODO: quads dell config report

            if not failed and not notification_obj.sucess:
                self.notify_success()
                notification_obj.update(success=True, fail=False)

                self.cloud.update(validated=True)

        if failed and not notification_obj.fail:
            self.notify_failure()
            notification_obj.update(fail=True)

        return


if __name__ == "__main__":
    clouds = Cloud.objects(validated=False, name__ne="cloud01")
    for _cloud in clouds:
        _hosts_total = Host.objects(cloud=_cloud).count()
        _schedule_count = Schedule.current_schedule(cloud=_cloud).count()
        if _schedule_count:
            validator = Validator(_cloud)
            validator.validate_env()
