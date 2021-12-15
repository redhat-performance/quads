#!/usr/bin/env python3
import asyncio
import logging
import sys

from datetime import timedelta
from quads.config import conf
from quads.model import Cloud, Schedule
from quads.tools.jira import Jira, JiraException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


async def main(_loop):
    no_extend_label = "CANNOT_EXTEND"
    extend_label = "CAN_EXTEND"

    try:
        jira = Jira(
            conf["jira_url"],
            loop=_loop,
        )
    except JiraException as ex:
        logger.error(ex)
        return 1

    tickets = await jira.get_pending_tickets()
    for ticket in tickets["issues"]:
        ticket_key = ticket.get("key").split("-")[-1]
        fields = ticket.get("fields")
        if fields:
            description = fields.get("description")
            try:
                cloud_field = description.split("\n")[1]
                cloud = cloud_field.split()[-1]
            except IndexError:
                logger.warning(
                    f"Could not retrieve cloud name from ticket {ticket_key}"
                )

            cloud_obj = Cloud.objects(name=cloud).first()
            schedules = Schedule.current_schedule(cloud=cloud_obj)
            conflict = False
            for schedule in schedules:
                end_date = schedule.end + timedelta(weeks=2)
                available = Schedule.is_host_available(
                    host=schedule.host.name, start=schedule.end, end=end_date
                )
                if not available:
                    conflict = True
                    await jira.add_label(ticket_key, no_extend_label)
                    logger.info(f"{cloud} labeled {no_extend_label}")
                    break

            if not conflict:
                await jira.add_label(ticket_key, extend_label)
                logger.info(f"{cloud} labeled {extend_label}")

            parent = fields.get("parent")
            if parent:
                p_ticket_key = parent.get("key").split("-")[-1]
                watchers = await jira.get_watchers(p_ticket_key)
                for watcher in watchers["watchers"]:
                    await jira.add_watcher(ticket_key, watcher["key"])
    return 0


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    err = loop.run_until_complete(main(loop))
    sys.exit(err)
