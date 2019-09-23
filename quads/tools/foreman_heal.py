#! /usr/bin/env python

from quads.config import conf
from quads.tools.foreman import Foreman
from quads.model import Schedule

import asyncio


def main():
    loop = asyncio.get_event_loop()

    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )

    current_schedule = Schedule.current_schedule()
    for schedule in current_schedule:
        # want to run these separetely to avoid ServerDisconnect
        loop.run_until_complete(foreman.add_role(schedule.cloud.name, schedule.host.name))


if __name__ == "__main__":
    main()
