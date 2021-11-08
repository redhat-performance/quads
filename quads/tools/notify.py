#!/usr/bin/python3
import asyncio
import logging
import os

from datetime import datetime, timedelta
from enum import Enum

from jinja2 import Template
from pathlib import Path
from quads.config import Config as conf
from quads.tools.netcat import Netcat
from quads.tools.postman import Postman
from quads.model import Cloud, Schedule, Notification

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Days(Enum):
    ONE_DAY = 1
    THREE_DAYS = 3
    FIVE_DAYS = 5
    SEVEN_DAYS = 7


async def create_initial_message(real_owner, cloud, cloud_info, ticket, cc):
    template_file = "initial_message"
    irc_bot_ip = conf["ircbot_ipaddr"]
    irc_bot_port = conf["ircbot_port"]
    irc_bot_channel = conf["ircbot_channel"]
    infra_location = conf["infra_location"]
    cc_users = conf["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    if conf["email_notify"]:
        with open(os.path.join(conf.TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        content = template.render(
            cloud_info=cloud_info,
            wp_wiki=conf["wp_wiki"],
            cloud=cloud,
            quads_url=conf["quads_url"],
            real_owner=real_owner,
            password=f"{infra_location}@{ticket}",
            foreman_url=conf["foreman_url"],
        )

        postman = Postman("New QUADS Assignment Allocated - %s %s" % (
            cloud,
            ticket
        ), real_owner, cc_users, content)
        postman.send_email()
    if conf["irc_notify"]:
        try:
            async with Netcat(irc_bot_ip, irc_bot_port) as nc:
                message = "%s QUADS: %s is now active, choo choo! - http://%s/assignments/#%s -  %s %s" % (
                    irc_bot_channel,
                    cloud_info,
                    conf["wp_wiki"],
                    cloud,
                    real_owner,
                    conf["report_cc"],
                )
                await nc.write(bytes(message.encode("utf-8")))
        except (TypeError, BrokenPipeError) as ex:
            logger.debug(ex)
            logger.error("Beep boop netcat can't communicate with your IRC.")


def create_message(
        cloud_obj,
        day,
        cloud_info,
        host_list_expire,
):
    template_file = "message"
    cloud = cloud_obj.name
    real_owner = cloud_obj.owner
    ticket = cloud_obj.ticket
    cc = cloud_obj.ccuser

    cc_users = conf["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    with open(os.path.join(conf.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    quads_request_url = conf.get("quads_request_url")
    content = template.render(
        days_to_report=day,
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
        quads_request_url=quads_request_url,
        quads_request_deadline_day=conf["quads_request_deadline_day"],
        quads_notify_until_extended=conf["quads_notify_until_extended"],
        cloud=cloud,
        hosts=host_list_expire,
    )
    postman = Postman("QUADS upcoming expiration for %s - %s" % (
        cloud,
        ticket
    ), real_owner, cc_users, content)
    postman.send_email()


def create_future_initial_message(cloud_obj, cloud_info):
    template_file = "future_initial_message"
    cloud = cloud_obj.name
    ticket = cloud_obj.ticket
    cc_users = conf["report_cc"].split(",")
    for user in cloud_obj.ccuser:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    with open(os.path.join(conf.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
    )
    postman = Postman("New QUADS Assignment Defined for the Future: %s - %s" % (
        cloud,
        ticket
    ), cloud_obj.owner, cc_users, content)
    postman.send_email()


def create_future_message(
        cloud_obj,
        future_days,
        cloud_info,
        host_list_expire,
):
    cc_users = conf["report_cc"].split(",")
    ticket = cloud_obj.ticket
    for user in cloud_obj.ccuser:
        cc_users.append("%s@%s" % (user, conf["domain"]))
    template_file = "future_message"
    with open(os.path.join(conf.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        days_to_report=future_days,
        cloud_info=cloud_info,
        wp_wiki=conf["wp_wiki"],
        cloud=cloud_obj.name,
        hosts=host_list_expire,
    )
    postman = Postman("QUADS upcoming assignment notification - %s - %s" % (
        cloud_obj.name,
        ticket
    ), cloud_obj.owner, cc_users, content)
    postman.send_email()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
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
        notification_obj = Notification.objects(
            cloud=cloud,
            ticket=cloud.ticket
        ).first()
        current_hosts = Schedule.current_schedule(cloud=cloud)
        cloud_info = "%s: %s (%s)" % (
            cloud.name,
            current_hosts.count(),
            cloud.description
        )
        if not notification_obj.initial:
            logger.info('=============== Initial Message')
            loop.run_until_complete(
                create_initial_message(
                    cloud.owner,
                    cloud.name,
                    cloud_info,
                    cloud.ticket,
                    cloud.ccuser,
                )
            )
            notification_obj.update(initial=True)

        for day in Days:
            future = datetime.now() + timedelta(days=day.value)
            future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
            future_hosts = Schedule.current_schedule(cloud=cloud, date=future_date)

            diff = set(current_hosts) - set(future_hosts)
            if diff and future > current_hosts[0].end:
                if not notification_obj[day.name.lower()] and conf["email_notify"]:
                    logger.info('=============== Additional Message')
                    host_list = [schedule.host.name for schedule in diff]
                    create_message(
                        cloud,
                        day.value,
                        cloud_info,
                        host_list,
                    )
                    kwargs = {day.name.lower(): True}
                    notification_obj.update(**kwargs)
                    break

    for cloud in _all_clouds:
        notification_obj = Notification.objects(
            cloud=cloud,
            ticket=cloud.ticket
        ).first()
        if cloud.name != "cloud01" and cloud.owner not in ["quads", None]:
            current_hosts = Schedule.current_schedule(cloud=cloud)
            cloud_info = "%s: %s (%s)" % (
                cloud.name,
                current_hosts.count(),
                cloud.description
            )

            if not notification_obj.pre_initial and conf["email_notify"]:
                logger.info('=============== Future Initial Message')
                create_future_initial_message(
                    cloud,
                    cloud_info,
                )
                notification_obj.update(pre_initial=True)

            for day in range(1, future_days + 1):
                if not notification_obj.pre and cloud.validated:
                    future = datetime.now() + timedelta(days=day)
                    future_date = "%4d-%.2d-%.2d 22:00" % (future.year, future.month, future.day)
                    future_hosts = Schedule.current_schedule(cloud=cloud, date=future_date)

                    if future_hosts.count() > 0:
                        diff = set(current_hosts) - set(future_hosts)
                        host_list = [schedule.host.name for schedule in diff]
                        if diff:
                            logger.info('=============== Additional Message')
                            create_future_message(
                                cloud,
                                day,
                                cloud_info,
                                host_list,
                            )
                            notification_obj.update(pre=True)
                            break


if __name__ == "__main__":
    main()
