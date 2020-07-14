#!/usr/bin/env python3

from quads.config import conf
from quads.tools.foreman import Foreman
from quads.model import Schedule, Cloud

import asyncio
import logging
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.propagate = False
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    loop = asyncio.get_event_loop()

    foreman_admin = Foreman(
        conf["foreman_api_url"],
        conf["foreman_username"],
        conf["foreman_password"],
        loop=loop,
    )

    ignore = ["cloud01"]
    foreman_rbac_exclude = conf.get("foreman_rbac_exclude")
    if foreman_rbac_exclude:
        ignore.extend(foreman_rbac_exclude.split("|"))
    clouds = Cloud.objects()
    for cloud in clouds:

        infra_pass = f"{conf['infra_location']}@{cloud.ticket}"
        loop.run_until_complete(
            foreman_admin.update_user_password(cloud.name, infra_pass)
        )

        foreman_cloud_user = Foreman(
            conf["foreman_api_url"],
            cloud.name,
            infra_pass,
            loop=loop,
        )

        if cloud.name not in ignore:
            logger.info(f"Processing {cloud.name}")

            cloud_hosts = loop.run_until_complete(foreman_cloud_user.get_all_hosts())

            user_id = loop.run_until_complete(foreman_admin.get_user_id(cloud.name))
            admin_id = loop.run_until_complete(
                foreman_admin.get_user_id(conf["foreman_username"])
            )

            current_schedule = Schedule.current_schedule(cloud=cloud)
            if current_schedule:

                logger.info(f"  Current Host Permissions:")
                for host, properties in cloud_hosts.items():
                    logger.info(f"    {host}")

                    match = [
                        schedule.host.name
                        for schedule in current_schedule
                        if schedule.host.name == host
                    ]
                    if not match:
                        loop.run_until_complete(
                            foreman_admin.put_parameter(host, "host['owner_id']", admin_id)
                        )
                        logger.info(f"* Removed permission {host}")

                for schedule in current_schedule:
                    match = [
                        host
                        for host, _ in cloud_hosts.items()
                        if host == schedule.host.name
                    ]
                    if not match:
                        # want to run these separetely to avoid ServerDisconnect
                        loop.run_until_complete(
                            foreman_admin.put_parameter(schedule.host.name, "host['owner_id']", user_id)
                        )
                        logger.info(f"* Added permission {schedule.host.name}")
            else:
                if cloud_hosts:
                    logger.info("  No active schedule, removing pre-existing roles.")
                    for host, properties in cloud_hosts.items():
                        loop.run_until_complete(
                            foreman_admin.put_parameter(host, "host['owner_id']", admin_id)
                        )
                        logger.info(f"* Removed permission {host}")
                else:
                    logger.info("  No active schedule nor roles assigned.")


if __name__ == "__main__":
    main()
