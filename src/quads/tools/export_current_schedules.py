#! /usr/bin/env python

import argparse
import logging

import yaml

from quads.config import Config
from quads.quads_api import QuadsApi, APIServerException, APIBadRequest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
quads = QuadsApi(Config)


def export_current_schedules(output):
    current_schedules = []
    clouds = {}
    try:
        future_schedules = quads.get_future_schedules()
    except (APIServerException, APIBadRequest) as e:
        logger.error(f"Failed to get future schedules: {e}")
        return
    for schedule in future_schedules:
        cloud = schedule.assignment.cloud
        if cloud.name not in clouds:
            clouds[cloud.name] = {
                "description": schedule.assignment.description,
                "owner": schedule.assignment.owner,
                "ticket": schedule.assignment.ticket,
                "qinq": schedule.assignment.qinq,
                "wipe": schedule.assignment.wipe,
                "ccuser": [cc for cc in schedule.assignment.ccuser],
                "vlan": schedule.assignment.vlan.vlan_id if schedule.assignment.vlan else None,
            }
        current_schedules.append(
            {
                "cloud": cloud.name,
                "host": schedule.host.name,
                "start": schedule.start,
                "end": schedule.end,
                "build_start": schedule.build_start,
                "build_end": schedule.build_end,
            }
        )

    data = {"clouds": clouds, "current_schedules": current_schedules}

    with open(output, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export current schedules to a YAML file.")
    parser.add_argument("--output", type=str, help="The name of the output file.")
    args = parser.parse_args()
    export_current_schedules(args.output)
