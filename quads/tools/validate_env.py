#! /usr/bin/env python

import os
import socket

from datetime import datetime

from requests import RequestException

from config import conf
from quads.quads import Api
from quads.model import Cloud, Schedule
from jinja2 import Template

from tools.foreman import Foreman
from tools.postman import Postman
from tools.ssh_helper import SSHHelper

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "../templates")
TOLERANCE = 14400
API = 'v2'

INTERFACES = {
    "nic1": ["172.16", "172.20"],
    "nic2": ["172.17", "172.21"],
    "nic3": ["172.18", "172.22"],
    "nic4": ["172.19", "172.23"],
}


def notify_failure(_cloud):
    template_file = "validation_failed"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read)
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check failed for {cloud} / {owner} / {ticket}".format(**parameters)
    postman = Postman(subject, _cloud.owner, _cloud.cc_users, content)
    postman.send_email()


def notify_success(_cloud):
    template_file = "validation_succeded"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read)
    parameters = {
        "cloud": _cloud.name,
        "owner": _cloud.owner,
        "ticket": _cloud.ticket,
    }
    content = template.render(**parameters)

    subject = "Validation check succeeded for {cloud} / {owner} / {ticket}".format(**parameters)
    postman = Postman(subject, _cloud.owner, _cloud.cc_users, content)
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

    api_url = os.path.join(conf['quads_base_url'], 'api', API)
    quads = Api(api_url)
    try:
        build_hosts = foreman.get_build_hosts()
    except RequestException:
        print("Unable to query Foreman for cloud: %s" % _cloud.name)
        print("Verify Foreman password is correct: %s" % _cloud.ticket)
        return False

    pending = []
    schedules = quads.get_current_schedule(cloud=_cloud.name)
    if "result" not in schedules:
        for schedule in schedules:
            host = quads.get_hosts(id=schedule["host"]["$oid"])
            if host and host['name'] in build_hosts:
                pending.append(host["name"])

        if pending:
            print("The following hosts are marked for build:")
            for host in pending:
                print(host)
            return False

    return True


def post_network_test(_cloud):

    api_url = os.path.join(conf['quads_base_url'], 'api', API)
    quads = Api(api_url)

    hosts = quads.get_cloud_hosts(_cloud)

    test_host = hosts[0]
    if not test_connection(test_host):
        return False

    ssh_helper = SSHHelper(test_host)
    host_list = " ".join(hosts)
    if not ssh_helper.run_cmd("fping -u %s" % host_list):
        return False
    for interface, values in INTERFACES.items():
        for value in values:
            host_ips = [socket.gethostbyname(host) for host in host_list]
            new_ips = []
            for ip in host_ips:
                ip_apart = ip.split(".")
                octets = value.split(".")
                ip_apart[0] = octets[0]
                ip_apart[1] = octets[1]
                new_ips.append(ip_apart)

            if not ssh_helper.run_cmd("fping -u %s" % new_ips):
                return False

    return True


def test_connection(_host, _port=53, _get_ip=False):
    if _get_ip:
        _host = socket.gethostbyname(_host)
    try:
        socket.setdefaulttimeout(3)
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect(_host, _port)
        return True
    except OSError as ex:
        print(ex)
        print("Host %s does not seem to be accessible." % _host)
    return False


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
    _cloud.update(validated=True, notified=True)
    return


if __name__ == "__main__":
    clouds = Cloud.objects(released=True, validated=False, notified=False)
    for cloud in clouds:
        validate_env(cloud)
