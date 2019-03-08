#!/usr/bin/env python3

import logging
import os

from datetime import datetime, timedelta
from jinja2 import Template
from pathlib import Path
from quads.config import conf, TEMPLATES_PATH, API_URL
from quads.quads import Api as QuadsApi
from quads.tools.netcat import Netcat
from quads.tools.postman import Postman
from quads.model import Cloud

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_initial_message(real_owner, cloud, cloud_info, ticket, cc, released):
    _cloud_obj = Cloud.objects(name=cloud).first()
    template_file = "initial_message"
    irc_bot_ip = conf["ircbot_ipaddr"]
    irc_bot_port = conf["ircbot_port"]
    irc_bot_channel = conf["ircbot_channel"]
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if released:
        if conf["email_notify"]:
            with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                template = Template(_file.read)
            content = template.render(
                cloud_info=cloud_info,
                wp_wiki=conf["wp_wiki"],
                cloud=cloud,
                quads_url=conf["quads_url"],
                real_owner=real_owner,
                ticket=ticket,
                foreman_url=conf["foreman_url"],
            )

            postman = Postman("New QUADS Assignment Allocated", real_owner, cc_users, content)
            postman.send_email()
        if conf["irc_notify"]:
            try:
                with Netcat(irc_bot_ip, irc_bot_port) as nc:
                    message = "%s QUADS: %s is now active, choo choo! - http://%s/assignments/#%s" % (
                        irc_bot_channel,
                        cloud_info,
                        conf["wp_wiki"],
                        cloud
                    )
                    nc.write(bytes(message.encode("utf-8")))
            except (TypeError, BrokenPipeError) as ex:
                logger.debug(ex)
                logger.error("Beep boop netcat can't communicate with your IRC.")
        _cloud_obj.update(notified=True)
    return


def create_message(
        real_owner,
        day,
        cloud,
        cloud_info,
        ticket,
        cc,
        released,
        current_hosts,
        future_hosts
):
    template_file = "message"
    report_file = "%s-%s-%s-%s" % (cloud, real_owner, day, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        if released:
            host_list_expire = set(current_hosts) - set(future_hosts)
            if host_list_expire:
                Path(report_file).touch()
                if conf["email_notify"]:
                    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                        template = Template(_file.read)
                    content = template.render(
                        days_to_report=day,
                        cloud_info=cloud_info,
                        wp_wiki=conf["wp_wiki"],
                        cloud=cloud,
                        hosts=host_list_expire,
                    )
                    postman = Postman("QUADS upcoming expiration notification", real_owner, cc_users, content)
                    postman.send_email()

    return


def create_future_initial_message(real_owner, cloud, cloud_info, ticket, cc):
    template_file = "future_initial_message"
    report_file = "%s-%s-pre-initial-%s" % (cloud, real_owner, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        Path(report_file).touch()
        if conf["email_notify"]:
            with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                template = Template(_file.read)
            content = template.render(
                cloud_info=cloud_info,
                wp_wiki=conf["wp_wiki"],
            )
            postman = Postman("New QUADS Assignment Allocated", real_owner, cc_users, content)
            postman.send_email()

    return


def create_future_message(
        real_owner,
        future_days,
        cloud,
        cloud_info,
        ticket,
        cc,
        released,
        current_hosts,
        future_hosts
):
    template_file = "future_message"
    report_file = "%s-%s-pre-%s" % (cloud, real_owner, ticket)
    cc_users = [conf["report_cc"]]
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if not os.path.exists(os.path.join(conf["data_dir"], "report", report_file)):
        if released:
            Path(report_file).touch()
            if conf["email_notify"]:
                host_list_expire = set(current_hosts) - set(future_hosts)
                with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
                    template = Template(_file.read)
                content = template.render(
                    days_to_report=future_days,
                    cloud_info=cloud_info,
                    wp_wiki=conf["wp_wiki"],
                    cloud=cloud,
                    hosts=host_list_expire,
                )
                postman = Postman("QUADS upcoming assignment notification", real_owner, cc_users, content)
                postman.send_email()

    return


def main():
    days = [1, 3, 5, 7]
    future_days = 7

    quads = QuadsApi(API_URL)

    _clouds = quads.get_summary()

    for cloud in [_cloud for _cloud in _clouds if int(_cloud["count"]) > 0]:
        cloud_info = "%s: %s (%s)" % (cloud["name"], cloud["count"], cloud["description"])
        logger.info('=============== Initial Message')
        if not cloud["notified"]:
            create_initial_message(
                cloud["owner"],
                cloud["name"],
                cloud_info,
                cloud["ticket"],
                cloud["ccuser"],
                cloud["released"]
            )
        for day in days:
            future = datetime.now() + timedelta(days=day)
            future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
            current_hosts = quads.get_current_schedule(cloud=cloud["name"])
            future_hosts = quads.get_current_schedule(cloud=cloud["name"], date=future_date)

            if "result" in current_hosts:
                current_hosts = []
            else:
                current_host_ids = [host["host"] for host in current_hosts]
                current_hosts = [quads.get_hosts(**{"id": host["$oid"]}) for host in current_host_ids]

            if "result" in future_hosts:
                future_hosts = []
            else:
                future_host_ids = [host["host"] for host in future_hosts]
                future_hosts = [quads.get_hosts(**{"id": host["$oid"]}) for host in future_host_ids]

            diff = set(current_hosts) - set(future_hosts)
            if diff:
                logger.info('=============== Additional Message')
                create_message(
                    cloud["owner"],
                    day,
                    cloud["name"],
                    cloud_info,
                    cloud["ticket"],
                    cloud["ccuser"],
                    cloud["released"],
                    current_hosts,
                    future_hosts
                )
                continue

    _clouds_full = quads.get_summary()

    for cloud in _clouds_full:
        if cloud not in _clouds:
            cloud_info = "%s: %s (%s)" % (cloud["name"], cloud["count"], cloud["description"])
            logger.info('=============== Future Initial Message')
            create_future_initial_message(cloud["owner"], cloud["name"], cloud_info, cloud["ticket"], cloud["ccuser"])
            future = datetime.now() + timedelta(days=future_days)
            future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
            current_hosts = quads.get_current_schedule(cloud=cloud["name"])
            future_hosts = quads.get_current_schedule(cloud=cloud["name"], date=future_date)

            if "result" in current_hosts:
                current_hosts = []
            else:
                current_host_ids = [host["host"] for host in current_hosts]
                current_hosts = [quads.get_hosts(**{"id": host["$oid"]}) for host in current_host_ids]

            if "result" in future_hosts:
                future_hosts = []
            else:
                future_host_ids = [host["host"] for host in future_hosts]
                future_hosts = [quads.get_hosts(**{"id": host["$oid"]}) for host in future_host_ids]

            diff = set(current_hosts) - set(future_hosts)
            if diff:
                logger.info('=============== Additional Message')
                create_future_message(
                    cloud["owner"],
                    future_days,
                    cloud["name"],
                    cloud_info,
                    cloud["ticket"],
                    cloud["ccuser"],
                    cloud["released"],
                    current_hosts,
                    future_hosts,
                )


if __name__ == "__main__":
    main()
