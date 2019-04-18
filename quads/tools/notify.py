#!/usr/bin/env python3

import logging
import os

from datetime import datetime, timedelta
from jinja2 import Template
from pathlib import Path
from quads.config import conf, TEMPLATES_PATH
from quads.tools.netcat import Netcat
from quads.tools.postman import Postman
from quads.model import Cloud, Schedule, Notification, EventTypeEnum

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_initial_message(real_owner, cloud, cloud_info, ticket, cc):
    _cloud_obj = Cloud.objects(name=cloud).first()
    template_file = "initial_message"
    irc_bot_ip = conf["ircbot_ipaddr"]
    irc_bot_port = conf["ircbot_port"]
    irc_bot_channel = conf["ircbot_channel"]
    cc_users = conf["report_cc"].split(",")
    content = ""
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if conf["email_notify"]:
        with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
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
    return content


def create_message(
        real_owner,
        day,
        cloud,
        cloud_info,
        cc,
        host_list_expire,
):
    template_file = "message"
    cc_users = conf["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        days_to_report=day,
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
        cloud=cloud,
        hosts=host_list_expire,
    )
    postman = Postman("QUADS upcoming expiration notification", real_owner, cc_users, content)
    postman.send_email()
    return content


def create_future_initial_message(real_owner, cloud_info, cc):
    template_file = "future_initial_message"
    cc_users = conf["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
    )
    postman = Postman("New QUADS Assignment Allocated", real_owner, cc_users, content)
    postman.send_email()
    return content


def create_future_message(
        real_owner,
        future_days,
        cloud,
        cloud_info,
        cc,
        host_list_expire,
):
    cc_users = conf["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    template_file = "future_message"
    with open(os.path.join(TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        days_to_report=future_days,
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
        cloud=cloud,
        hosts=host_list_expire,
    )
    postman = Postman("QUADS upcoming assignment notification", real_owner, cc_users, content)
    postman.send_email()
    return content


def main():
    days = [EventTypeEnum.ONE_DAY, EventTypeEnum.THREE_DAYS, EventTypeEnum.FIVE_DAYS, EventTypeEnum.SEVEN_DAYS]
    future_days = 7

    _all_clouds = Cloud.objects()
    _active_clouds = [
        _cloud for _cloud in _all_clouds
        if Schedule.current_schedule(cloud=_cloud).count() > 0
    ]
    _validated_clouds = [_cloud for _cloud in _active_clouds if _cloud.validated]

    if not os.path.exists(os.path.join(conf["data_dir"], "report")):
        Path(os.path.join(conf["data_dir"], "report")).mkdir(parents=True, exist_ok=True)

    for cloud in _validated_clouds:
        current_hosts = Schedule.current_schedule(cloud=cloud)
        cloud_info = "%s: %s (%s)" % (
            cloud.name,
            current_hosts.count(),
            cloud.description
        )
        initial_notification = Notification.objects(
            event_type=EventTypeEnum.INITIAL,
            cloud=cloud,
            ticket=cloud.ticket
        ).first()
        if not initial_notification.notified:
            logger.info('=============== Initial Message')
            content = create_initial_message(
                cloud.owner,
                cloud.name,
                cloud_info,
                cloud.ticket,
                cloud.ccuser,
            )
            initial_notification.update(notified=True, content=content)

        for day in days:
            future = datetime.now() + timedelta(days=day.value)
            future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
            future_hosts = Schedule.current_schedule(cloud=cloud, date=future_date)

            diff = set(current_hosts) - set(future_hosts)
            if diff and future < current_hosts[0].end:
                day_notification = Notification.objects(event_type=day, cloud=cloud, ticket=cloud.ticket).first()
                if not day_notification.notified and conf["email_notify"]:
                    logger.info('=============== Additional Message')
                    host_list = [schedule.host.name for schedule in diff]
                    content = create_message(
                        cloud.owner,
                        day.value,
                        cloud.name,
                        cloud_info,
                        cloud.ccuser,
                        host_list,
                    )
                    day_notification.update(notified=True, content=content)
                    break

    for cloud in _all_clouds:
        if cloud.name != "cloud01" and cloud.owner not in ["quads", None]:
            current_hosts = Schedule.current_schedule(cloud=cloud)
            cloud_info = "%s: %s (%s)" % (
                cloud.name,
                current_hosts.count(),
                cloud.description
            )

            pre_initial_notification = Notification.objects(
                event_type=EventTypeEnum.PRE_INITIAL,
                cloud=cloud,
                ticket=cloud.ticket
            ).first()
            if not pre_initial_notification.notified and conf["email_notify"]:
                logger.info('=============== Future Initial Message')
                content = create_future_initial_message(
                    cloud.owner,
                    cloud_info,
                    cloud.ccuser,
                )
                pre_initial_notification.update(notified=True, content=content)

            pre_notification = Notification.objects(
                event_type=EventTypeEnum.PRE,
                cloud=cloud,
                ticket=cloud.ticket
            ).first()
            if not pre_notification.notified and cloud.validated:
                future = datetime.now() + timedelta(days=future_days)
                future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
                future_hosts = Schedule.current_schedule(cloud=cloud, date=future_date)

                diff = set(current_hosts) - set(future_hosts)
                host_list = [schedule.host.name for schedule in diff]
                if diff:
                    logger.info('=============== Additional Message')
                    content = create_future_message(
                        cloud.owner,
                        future_days,
                        cloud.name,
                        cloud_info,
                        cloud.ccuser,
                        host_list,
                    )
                    pre_notification.update(notified=True, content=content)


if __name__ == "__main__":
    main()
