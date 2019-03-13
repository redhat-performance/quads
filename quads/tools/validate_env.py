#!/usr/bin/env python3
import logging
import os
import socket

from datetime import datetime
from requests import RequestException

from jinja2 import Template
from quads.config import conf, TEMPLATES_PATH, TOLERANCE, API_URL, INTERFACES
from quads.quads import Api
from quads.model import Cloud, Schedule
from quads.tools.foreman import Foreman
from quads.tools.postman import Postman
from quads.tools.ssh_helper import SSHHelper

logger = logging.getLogger(__name__)


def notify_failure(_cloud):
    template_file = "validation_failed"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check failed for {cloud} / {owner} / {ticket}".format(**parameters)
    _cc_users = ["%s@%s" % (cc, conf["domain"]) for cc in _cloud.ccuser]
    postman = Postman(subject, _cloud.owner, _cc_users, content)
    postman.send_email()


def notify_success(_cloud):
    template_file = "validation_succeded"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check succeeded for {cloud} / {owner} / {ticket}".format(**parameters)
    _cc_users = ["%s@%s" % (cc, conf["domain"]) for cc in _cloud.cc_users]
    postman = Postman(subject, _cloud.owner, _cc_users, content)
    postman.send_email()


def env_allocation_time_exceeded(_cloud):
    now = datetime.now()
    schedule = Schedule.objects(cloud=_cloud, start__lt=now).first()
    if now - schedule.start > TOLERANCE:
        return True
    return False


def post_system_test(_cloud):
    foreman = Foreman(
        conf["foreman_api_url"],
        _cloud.name,
        _cloud.ticket
    )

    quads = Api(API_URL)
    try:
        build_hosts = foreman.get_build_hosts()
    except RequestException:
        logger.error("Unable to query Foreman for cloud: %s" % _cloud.name)
        logger.error("Verify Foreman password is correct: %s" % _cloud.ticket)
        return False

    pending = []
    schedules = quads.get_current_schedule(cloud=_cloud.name)
    if "result" not in schedules:
        for schedule in schedules:
            host = quads.get_hosts(id=schedule["host"]["$oid"])
            if host and host['name'] in build_hosts:
                pending.append(host["name"])

        if pending:
            logger.info("The following hosts are marked for build:")
            for host in pending:
                logger.info(host)
            return False

    return True


def post_network_test(_cloud):

    quads = Api(API_URL)

    hosts = [host["name"] for host in quads.get_cloud_hosts(_cloud.name)]

    test_host = hosts[0]
    try:
        ssh_helper = SSHHelper(test_host)
    except Exception:
        logger.exception("Could not establish connection with host: %s." % test_host)
        return False
    host_list = " ".join(hosts)
    if type(ssh_helper.run_cmd("fping -u %s" % host_list)) != list:
        return False
    for interface, values in INTERFACES.items():
        for value in values:
            host_ips = [socket.gethostbyname(host) for host in host_list.split()]
            new_ips = []
            for ip in host_ips:
                ip_apart = ip.split(".")
                octets = value.split(".")
                ip_apart[0] = octets[0]
                ip_apart[1] = octets[1]
                new_ips.append(".".join(ip_apart))

            if type(ssh_helper.run_cmd("fping -u %s" % " ".join(new_ips))) != list:
                return False

    return True


def validate_env(_cloud):
    if not post_system_test(_cloud):
        if env_allocation_time_exceeded(_cloud):
            notify_failure(_cloud)
            return

    if not post_network_test(_cloud):
        if env_allocation_time_exceeded(_cloud):
            notify_failure(_cloud)
            return

    # TODO: gather ansible-cmdb facts

    # TODO: quads dell config report

    notify_success(_cloud)
    _cloud.update(validated=True)
    return


if __name__ == "__main__":
    clouds = Cloud.objects(released=True, validated=False)
    for cloud in clouds:
        validate_env(cloud)
