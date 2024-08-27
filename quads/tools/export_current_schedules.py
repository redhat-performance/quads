#! /usr/bin/env python3

import argparse
import logging
from datetime import datetime

import yaml

from quads.model import Schedule

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def export_current_schedules(output):
    current_schedules = []
    clouds = {}
    future_schedules = Schedule.future_schedules()
    for schedule in future_schedules:
        cloud = schedule.cloud
        if cloud.name not in clouds:
            clouds[cloud.name] = {
                "description": cloud.description,
                "owner": cloud.owner,
                "ticket": cloud.ticket,
                "qinq": cloud.qinq,
                "wipe": cloud.wipe,
                "ccuser": [cc for cc in cloud.ccuser],
                "vlan": cloud.vlan.vlan_id if cloud.vlan else None,
            }
        format_str = "%a, %d %b %Y %H:%M:%S %Z"
        _start = datetime.strptime(str(schedule.start), format_str)
        _end = datetime.strptime(str(schedule.end), format_str)
        _build_start = (
            datetime.strptime(str(schedule.build_start).split(".")[0], format_str) if schedule.build_start else None
        )
        _build_end = (
            datetime.strptime(str(schedule.build_end).split(".")[0], format_str) if schedule.build_end else None
        )
        current_schedules.append(
            {
                "cloud": cloud.name,
                "host": cloud.name,
                "start": _start,
                "end": _end,
                "build_start": _build_start,
                "build_end": _build_end,
                "moved": schedule.host.cloud.name != schedule.host.default_cloud.name,
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
