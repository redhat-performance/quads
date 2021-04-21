#! /usr/bin/env python
import asyncio
from datetime import timedelta

from quads.config import conf
from quads.model import Cloud, Schedule
from quads.tools.jira import Jira


async def main(_loop):
    jira = Jira(
        conf["jira_url"],
        conf["jira_username"],
        conf["jira_password"],
        loop=_loop,
    )
    tickets = await jira.get_pending_tickets()
    for ticket in tickets["issues"]:
        ticket_key = ticket.get("key").split("-")[-1]
        fields = ticket.get("fields")
        if fields:
            cloud = fields.get("description").split()[-1]
            cloud_obj = Cloud.objects(name=cloud).first()
            schedules = Schedule.current_schedule(cloud=cloud_obj)
            conflict=False
            for schedule in schedules:
                end_date = schedule.end + timedelta(weeks=2)
                available = Schedule.is_host_available(host=schedule.host.name,
                                                       start=schedule.end,
                                                       end=end_date)
                if not available:
                    conflict = True
                    await jira.add_label(ticket_key, "CANNOT_EXTEND")
                    break

            if not conflict:
                await jira.add_label(ticket_key, "CAN_EXTEND")

            parent = fields.get("parent")
            if parent:
                p_ticket_key = parent.get("key").split("-")[-1]
                watchers = await jira.get_watchers(p_ticket_key)
                for watcher in watchers["watchers"]:
                    await jira.add_watcher(ticket_key, watcher["key"])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
