#!/usr/bin/python3
import asyncio
import logging
import os
import requests

from datetime import datetime, timedelta
from enum import Enum

from jinja2 import Template
from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.schedule import ScheduleDao
from quads.tools.external.netcat import Netcat
from quads.tools.external.postman import Postman

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Days(Enum):
    ONE_DAY = 1
    THREE_DAYS = 3
    FIVE_DAYS = 5
    SEVEN_DAYS = 7


async def create_initial_message(real_owner, cloud, cloud_info, ticket, cc):
    template_file = "initial_message"
    irc_bot_ip = Config["ircbot_ipaddr"]
    irc_bot_port = Config["ircbot_port"]
    irc_bot_channel = Config["ircbot_channel"]
    webhook_url = Config["webhook_url"]
    infra_location = Config["infra_location"]
    cc_users = Config["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, Config["domain"]))

    if Config["email_notify"]:
        with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
            template = Template(_file.read())
        content = template.render(
            cloud_info=cloud_info,
            wp_wiki=Config["wp_wiki"],
            cloud=cloud,
            quads_url=Config["quads_url"],
            real_owner=real_owner,
            password=f"{infra_location}@{ticket}",
            foreman_url=Config["foreman_url"],
        )

        postman = Postman(
            "New QUADS Assignment Allocated - %s %s" % (cloud, ticket),
            real_owner,
            cc_users,
            content,
        )
        postman.send_email()

    if Config["irc_notify"]:
        try:
            async with Netcat(irc_bot_ip, irc_bot_port) as nc:
                message = (
                    "%s QUADS: %s is now active, choo choo! - %s/assignments/#%s -  %s %s"
                    % (
                        irc_bot_channel,
                        cloud_info,
                        Config["wp_wiki"],
                        cloud,
                        real_owner,
                        Config["report_cc"],
                    )
                )
                await nc.write(bytes(message.encode("utf-8")))
        except (TypeError, BrokenPipeError) as ex:
            logger.debug(ex)
            logger.error("Beep boop netcat can't communicate with your IRC.")

    if Config["webhook_notify"]:
        try:
            message = (
                "QUADS: %s is now active, choo choo! - %s/assignments/#%s -  %s %s"
                % (
                    cloud_info,
                    Config["wp_wiki"],
                    cloud,
                    real_owner,
                    Config["report_cc"],
                )
            )
            requests.post(
                webhook_url,
                json={"text": message},
                headers={"Content-Type": "application/json"},
            )
        except Exception as ex:
            logger.debug(ex)
            logger.error("Beep boop we can't communicate with your webhook.")


def create_message(
    cloud_obj,
    assignment_obj,
    day,
    cloud_info,
    host_list_expire,
):
    template_file = "message"
    cloud = cloud_obj.name
    real_owner = assignment_obj.owner
    ticket = assignment_obj.ticket
    cc = assignment_obj.ccuser

    cc_users = Config["report_cc"].split(",")
    for user in cc:
        cc_users.append("%s@%s" % (user, Config["domain"]))
    with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    quads_request_url = Config.quads_request_url
    content = template.render(
        days_to_report=day,
        cloud_info=cloud_info,
        wp_wiki=Config["wp_wiki"],
        quads_request_url=quads_request_url,
        quads_request_deadline_day=Config["quads_request_deadline_day"],
        quads_notify_until_extended=Config["quads_notify_until_extended"],
        cloud=cloud,
        hosts=host_list_expire,
    )
    postman = Postman(
        "QUADS upcoming expiration for %s - %s" % (cloud, ticket),
        real_owner,
        cc_users,
        content,
    )
    postman.send_email()


def create_future_initial_message(cloud_obj, assignment_obj, cloud_info):
    template_file = "future_initial_message"
    cloud = cloud_obj.name
    ticket = assignment_obj.ticket
    cc_users = Config["report_cc"].split(",")
    for user in assignment_obj.ccuser:
        cc_users.append("%s@%s" % (user, Config["domain"]))
    with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        cloud_info=cloud_info,
        wp_wiki=Config["wp_wiki"],
    )
    postman = Postman(
        "New QUADS Assignment Defined for the Future: %s - %s" % (cloud, ticket),
        assignment_obj.owner,
        cc_users,
        content,
    )
    postman.send_email()


def create_future_message(
    cloud_obj,
    assignment_obj,
    future_days,
    cloud_info,
    host_list_expire,
):
    cc_users = Config["report_cc"].split(",")
    ticket = assignment_obj.ticket
    for user in assignment_obj.ccuser:
        cc_users.append("%s@%s" % (user, Config["domain"]))
    template_file = "future_message"
    with open(os.path.join(Config.TEMPLATES_PATH, template_file)) as _file:
        template = Template(_file.read())
    content = template.render(
        days_to_report=future_days,
        cloud_info=cloud_info,
        wp_wiki=Config["wp_wiki"],
        cloud=cloud_obj.name,
        hosts=host_list_expire,
    )
    postman = Postman(
        "QUADS upcoming assignment notification - %s - %s" % (cloud_obj.name, ticket),
        assignment_obj.owner,
        cc_users,
        content,
    )
    postman.send_email()


def main(_logger=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    global logger
    if _logger:
        logger = _logger

    _all_clouds = CloudDao.get_clouds()
    _active_clouds = [
        _cloud
        for _cloud in _all_clouds
        if len(ScheduleDao.get_current_schedule(cloud=_cloud)) > 0
    ]
    _validated_clouds = []
    for _cloud in _active_clouds:
        assignment_obj = AssignmentDao.filter_assignments({"cloud_id": _cloud.id})
        assignment_obj = assignment_obj[0] if assignment_obj else None
        if assignment_obj.validated:
            _validated_clouds.append(_cloud)

    for cloud in _validated_clouds:
        assignment_obj = AssignmentDao.filter_assignments({"cloud_id": cloud.id})
        assignment_obj = assignment_obj[0] if assignment_obj else None
        if assignment_obj is None:
            continue
        current_hosts = ScheduleDao.get_current_schedule(cloud=cloud)
        cloud_info = "%s: %s (%s)" % (
            cloud.name,
            len(current_hosts),
            assignment_obj.description,
        )
        notification_obj = current_hosts[0].assignment.notification if current_hosts else None
        if notification_obj is None:
            continue
        if not notification_obj.initial:
            logger.info("=============== Initial Message")
            loop.run_until_complete(
                create_initial_message(
                    assignment_obj.owner,
                    cloud.name,
                    cloud_info,
                    assignment_obj.ticket,
                    assignment_obj.ccuser,
                )
            )
            setattr(notification_obj, "initial", True)
            BaseDao.safe_commit()

        for day in Days:
            future = datetime.now() + timedelta(days=day.value)
            future_date = "%4d-%.2d-%.2d 22:00" % (
                future.year,
                future.month,
                future.day,
            )
            future_hosts = ScheduleDao.get_current_schedule(
                cloud=cloud, date=datetime.strptime(future_date, "%Y-%m-%d %H:%M")
            )

            diff = set(current_hosts) - set(future_hosts)
            if diff and future > current_hosts[0].end:
                if not getattr(notification_obj, day.name.lower()) and Config["email_notify"]:
                    logger.info("=============== Additional Message")
                    host_list = [schedule.host.name for schedule in diff]
                    create_message(
                        cloud,
                        assignment_obj,
                        day.value,
                        cloud_info,
                        host_list,
                    )
                    setattr(notification_obj, day.name.lower(), True)
                    BaseDao.safe_commit()
                    break

    for cloud in _all_clouds:
        assignment_obj = AssignmentDao.filter_assignments({"cloud_id": cloud.id})
        assignment_obj = assignment_obj[0] if assignment_obj else None
        if assignment_obj is None:
            continue
        if cloud.name != "cloud01" and assignment_obj.owner not in ["quads", None]:
            current_hosts = ScheduleDao.get_current_schedule(cloud=cloud)
            notification_obj = current_hosts[0].assignment.notification if current_hosts else None
            if notification_obj is None:
                continue
            cloud_info = "%s: %s (%s)" % (
                cloud.name,
                len(current_hosts),
                assignment_obj.description,
            )

            if not notification_obj.pre_initial and Config["email_notify"]:
                logger.info("=============== Future Initial Message")
                create_future_initial_message(
                    cloud,
                    assignment_obj,
                    cloud_info,
                )
                setattr(notification_obj, "pre_initial", True)
                BaseDao.safe_commit()

            for day in Days:
                if not notification_obj.pre and assignment_obj.validated:
                    future = datetime.now() + timedelta(days=day.value)
                    future_date = "%4d-%.2d-%.2d 22:00" % (
                        future.year,
                        future.month,
                        future.day,
                    )
                    future_hosts = ScheduleDao.get_current_schedule(
                        cloud=cloud,
                        date=datetime.strptime(future_date, "%Y-%m-%d %H:%M"),
                    )

                    if len(future_hosts) > 0:
                        diff = set(current_hosts) - set(future_hosts)
                        host_list = [schedule.host.name for schedule in diff]
                        if diff:
                            logger.info("=============== Additional Message")
                            create_future_message(
                                cloud,
                                assignment_obj,
                                day,
                                cloud_info,
                                host_list,
                            )
                            setattr(notification_obj, "pre", True)
                            BaseDao.safe_commit()
                            break


if __name__ == "__main__":
    main()
