#! /usr/bin/env python

import argparse
import logging

import yaml

from quads.config import Config
from quads.quads_api import QuadsApi, APIServerException, APIBadRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
quads = QuadsApi(Config)


def import_current_schedules(filepath):

    with open(filepath, "r") as infile:
        data = yaml.safe_load(infile)

    clouds = data["clouds"]
    schedules = data["current_schedules"]

    for cloud, properties in clouds.items():
        data = {
            "cloud": cloud,
            "description": properties["description"],
            "owner": properties["owner"],
            "ccuser": properties["ccuser"],
            "qinq": properties["qinq"],
            "ticket": properties["ticket"],
            "wipe": properties["wipe"],
        }

        cloud = quads.get_cloud(cloud)
        if not cloud:
            quads.insert_cloud(data)

        active_assignment = quads.get_active_cloud_assignment(cloud)
        if not active_assignment:
            quads.insert_assignment(data)
        else:
            logger.info(f"Cloud {cloud} already has an active assignment.")

    for schedule in schedules:
        try:
            quads.get_host(schedule["host"])
        except (APIServerException, APIBadRequest):
            logger.info(f"Undefined host: {schedule['host']}. SKIPPING")
            continue

        schedule_data = {
            "cloud": schedule["cloud"],
            "hostname": schedule["host"],
            "start": schedule["start"],
            "end": schedule["end"],
            "build_start": schedule["build_start"],
            "build_end": schedule["build_end"],
        }
        quads.insert_schedule(schedule_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import current schedules from a YAML file.")
    parser.add_argument("--input", type=str, help="The name of the input file.")
    args = parser.parse_args()
    import_current_schedules(args.input)
