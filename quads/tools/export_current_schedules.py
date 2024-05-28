#! /usr/bin/env python

import argparse
from quads.model import Schedule
import yaml


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
