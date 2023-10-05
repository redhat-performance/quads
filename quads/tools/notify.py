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
                message = "%s QUADS: %s is now active, choo choo! - %s/assignments/#%s -  %s %s" % (
                    irc_bot_channel,
                    cloud_info,
                    Config["wp_wiki"],
                    cloud,
                    real_owner,
                    Config["report_cc"],
                )
                await nc.write(bytes(message.encode("utf-8")))
        except (TypeError, BrokenPipeError) as ex:
            logger.debug(ex)
            logger.error("Beep boop netcat can't communicate with your IRC.")

    if Config["webhook_notify"]:
        try:
            message = "QUADS: %s is now active, choo choo! - %s/assignments/#%s -  %s %s" % (
                cloud_info,
                Config["wp_wiki"],
                cloud,
                real_owner,
                Config["report_cc"],
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
    _assignments = AssignmentDao.filter_assignments({"active": True, "validated": True})

    for ass in _assignments:
        current_hosts = ScheduleDao.get_current_schedule(cloud=ass.cloud)
        cloud_info = "%s: %s (%s)" % (
            ass.cloud.name,
            len(current_hosts),
            ass.description,
        )
        if not ass.notification.initial:
            logger.info("=============== Initial Message")
            loop.run_until_complete(
                create_initial_message(
                    ass.owner,
                    ass.cloud.name,
                    cloud_info,
                    ass.ticket,
                    ass.ccuser,
                )
            )
            ass.notification.initial = True
            BaseDao.safe_commit()

        for day in Days:
            future = datetime.now() + timedelta(days=day.value)
            future_date = "%4d-%.2d-%.2d 22:00" % (
                future.year,
                future.month,
                future.day,
            )
            future_hosts = ScheduleDao.get_current_schedule(
                cloud=ass.cloud, date=datetime.strptime(future_date, "%Y-%m-%d %H:%M")
            )

            diff = set(current_hosts) - set(future_hosts)
            if diff and future > current_hosts[0].end:
                if not getattr(ass.notification, day.name.lower()) and Config["email_notify"]:
                    logger.info("=============== Additional Message")
                    host_list = [schedule.host.name for schedule in diff]
                    create_message(
                        ass.cloud,
                        ass.notification,
                        day.value,
                        cloud_info,
                        host_list,
                    )
                    setattr(ass.notification, day.name.lower(), True)
                    BaseDao.safe_commit()
                    break

    for cloud in _all_clouds:
        ass = AssignmentDao.get_active_cloud_assignment(cloud)
        if not ass:
            continue
        if cloud.name != Config["spare_pool_name"] and ass.owner not in ["quads", None]:
            current_hosts = ScheduleDao.get_current_schedule(cloud=cloud)
            cloud_info = "%s: %s (%s)" % (
                cloud.name,
                len(current_hosts),
                ass.description,
            )

            if not ass.notification.pre_initial and Config["email_notify"]:
                logger.info("=============== Future Initial Message")
                create_future_initial_message(
                    cloud,
                    ass,
                    cloud_info,
                )
                setattr(ass.notification, "pre_initial", True)
                BaseDao.safe_commit()

            for day in Days:
                if not ass.notification.pre and ass.validated:
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
                                ass,
                                day,
                                cloud_info,
                                host_list,
                            )
                            setattr(ass.notification, "pre", True)
                            BaseDao.safe_commit()
                            break


if __name__ == "__main__":
    main()
