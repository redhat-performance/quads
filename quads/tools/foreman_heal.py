#! /usr/bin/env python

from quads.config import conf
from quads.tools.foreman import Foreman
from quads.model import Schedule, Cloud

import asyncio


def main():
    loop = asyncio.get_event_loop()

    foreman = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )

    clouds = Cloud.objects()
    for cloud in clouds:
        if cloud.name != "cloud01":
            user_id = asyncio.run(foreman.get_user_id(cloud.name))
            roles = asyncio.run(foreman.get_user_roles(user_id))
            current_schedule = Schedule.current_schedule(cloud=cloud)

            for role in roles:
                match = [
                    schedule.host.name for schedule in current_schedule
                    if schedule.host.name == role["name"]
                ]
                if not match:
                    asyncio.run(foreman.remove_role(cloud.name, role["name"]))

            for schedule in current_schedule:
                # want to run these separetely to avoid ServerDisconnect
                loop.run_until_complete(
                    foreman.add_role(
                        schedule.cloud.name,
                        schedule.host.name
                    )
                )


if __name__ == "__main__":
    main()
