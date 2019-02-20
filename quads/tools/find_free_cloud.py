#!/usr/bin/env python
# tool to query lab schedule and find free cloud
# ./find-availably.py

import argparse
import os
import sys
import yaml
import time
import datetime

parser = argparse.ArgumentParser(description='Find free clouds for lab reservation')


def printf(_format, *args):
    sys.stdout.write(_format % args)


args = parser.parse_args()

quads_config = os.path.dirname(__file__) + "/../../conf/quads.yml"
quads = {}


def load_quads_config():
    global quads_config
    global quads
    global quadsdata

    try:
        with open(quads_config, 'r') as config_file:
            quads = yaml.safe_load(config_file)
    except yaml.YAMLError as ex:
        print(ex)
        exit(1)

    try:
        with open(quads["data_dir"] + "/schedule.yaml", 'r') as data_file:
            quadsdata = yaml.safe_load(data_file)
    except yaml.YAMLError as ex:
        print(ex)
        exit(1)


load_quads_config()


available_list = []
print("==================")
print("Clouds in use:")
curdate_obj = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
for c in sorted(quadsdata["clouds"].iterkeys()):
    available = True
    for h in sorted(quadsdata["hosts"].keys()):
        if "schedule" in list(quadsdata["hosts"][h].keys()):
            for s in quadsdata["hosts"][h]["schedule"]:
                s_cloud = quadsdata["hosts"][h]["schedule"][s]["cloud"]
                end_obj = datetime.datetime.strptime(quadsdata["hosts"][h]["schedule"][s]["end"], '%Y-%m-%d %H:%M')
                if curdate_obj <= end_obj and s_cloud == c:
                    print("  cloud: " + c)
                    print("    host: " + h)
                    print("      schedule: " + str(s))
                    available = False
                    break
            if not available:
                break
    if available:
        available_list.append(c)

print("==================")
print("The following are available for use:")
for c in available_list:
    print("  " + c)

exit(0)
