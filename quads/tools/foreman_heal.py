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

    foreman = Foreman(
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
        if cloud.name not in ignore:
            logger.info(f"Processing {cloud.name}")
            user_id = loop.run_until_complete(foreman.get_user_id(cloud.name))
            roles = loop.run_until_complete(foreman.get_user_roles(user_id))
            current_schedule = Schedule.current_schedule(cloud=cloud)
            if current_schedule:
                infra_pass = f"{conf['infra_location']}@{cloud.ticket}"
                loop.run_until_complete(foreman.update_user_password(cloud.name, infra_pass))
                logger.info(f"  Current Roles:")
                for role in roles:
                    logger.info(f"    {role}")

                for role, data in roles.items():
                    match = [
                        schedule.host.name for schedule in current_schedule
                        if schedule.host.name == role
                    ]
                    if not match:
                        loop.run_until_complete(foreman.remove_role(cloud.name, role))
                        logger.info(f"* Removed role {role}")

                for schedule in current_schedule:
                    match = [role for role in roles if role == schedule.host.name]
                    if not match:
                        # want to run these separetely to avoid ServerDisconnect
                        loop.run_until_complete(
                            foreman.add_role(
                                schedule.cloud.name,
                                schedule.host.name
                            )
                        )
                        logger.info(f"* Added role {schedule.host.name}")
            else:
                if roles:
                    logger.info("  No active schedule, removing pre-existing roles.")
                    for role, data in roles.items():
                        loop.run_until_complete(foreman.remove_role(cloud.name, role))
                        logger.info(f"* Removed role {role}")
                else:
                    logger.info("  No active schedule nor roles assigned.")


if __name__ == "__main__":
    main()
