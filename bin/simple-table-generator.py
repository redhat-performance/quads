#!/usr/bin/env python
# feeds from simple-table-generator.sh
# generates HTML visualization map for machine allocations

import random
import string
import argparse
import os
import sys
import array
import yaml
import csv
from subprocess import call
from subprocess import check_call
from datetime import datetime

parser = argparse.ArgumentParser(description='Generate a simple HTML table with color depicting resource usage for the month')
requiredArgs=parser.add_argument_group('Required Arguments')
requiredArgs.add_argument('-d', '--days', dest='days', type=int, required=True, default=None, help='number of days to generate')
requiredArgs.add_argument('-m', '--month', dest='month', type=str, required=True, default=None, help='Month to generate')
requiredArgs.add_argument('-y', '--year', dest='year', type=str, required=True, default=None, help='Year to generate')
requiredArgs.add_argument('--host-file', dest='host_file', type=str, required=False, default=None, help='file with list of hosts')
parser.add_argument('--gentime', '-g', dest='gentime', type=str, required=False, default=None, help='generate timestamp when created')

args = parser.parse_args()
host_file = args.host_file
days = args.days
month = args.month
year = args.year
gentime = args.gentime


# Load QUADS yaml config
def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except Exception, ex:
                print "quads: Invalid YAML config: " + quads_config
                exit(1)
    except Exception, ex:
        print ex
        exit(1)
    return(quads_config_yaml)


quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
quads_config = quads_load_config(quads_config_file)

# Sanity checks to determine QUADS dir structure is intact
if "data_dir" not in quads_config:
    print "quads: Missing \"data_dir\" in " + quads_config_file
    exit(1)

if "install_dir" not in quads_config:
    print "quads: Missing \"install_dir\" in " + quads_config_file
    exit(1)

sys.path.append(quads_config["install_dir"] + "/lib")
sys.path.append(os.path.dirname(__file__) + "../lib")

from Quads import Quads

defaultstatedir = quads_config["data_dir"] + "/state"
defaultmovecommand = "/bin/echo"

quads = Quads(quads_config["data_dir"] + "/schedule.yaml",
                       defaultstatedir, defaultmovecommand,
                       None, None, False, False)

# Set maxcloud to maximum defined clouds
maxcloud = len(quads.get_clouds())

def get_spaced_colors(visual_colors):
    result = []
    for k in sorted(visual_colors.keys()):
        result.append(visual_colors[k].split())
    return result

# covert palette to hex
def get_cell_color(a, b, c):
    return "#" + ('0' if len(hex(int(a))) < 4 else '') + hex(int(a))[2:] + ('0' if len(hex(int(b))) < 4 else '') + hex(int(b))[2:] + ('0' if len(hex(int(c))) < 4 else '') + hex(int(c))[2:]

colors = get_spaced_colors(quads_config["visual_colors"])
color_array = []

for i in colors:
    if int(i[0]) >= 0:
        color_array.append(get_cell_color(i[0], i[1], i[2]))
    else:
        color_array.append(i[1])

def print_simple_table(data, data_colors, days):

    print "<html>"
    print "<head>"
    if gentime:
        print "<title>" + gentime + "</title>"
    else:
        print "<title> Monthly Allocation </title>"
    print "</head>"
    print "<body>"
    if gentime:
        print "<b>" + gentime + "</b><br>"
        print "<br>"
    print "<table>"
    print "<tr>"
    print "<th>Name</th>"
    for i in range(0, days):
        print "<th width=20>" + ('0' if i < 9 else '') + str(i+1) + "</th>"
    print "</tr>"
    for i in range(0, len(data)):
        print "<tr>"
        print "<td>" + str(data[i][0]) + "</td>"
        for j in range(0, days):
            chosen_color = data_colors[i][j]
            cell_date = year + "-" + month + "-" + str(j + 1) + " 00:00"
            cell_time = datetime.strptime(cell_date, '%Y-%m-%d %H:%M')
            cell_day = j + 1
            history = quads.get_history()
            for c in sorted(history["cloud" + str(chosen_color)]):
                if datetime.fromtimestamp(c) <= cell_time:
                    display_description = history["cloud" + str(chosen_color)][c]["description"]
                    display_owner = history["cloud" + str(chosen_color)][c]["owner"]
                    display_ticket = history["cloud" + str(chosen_color)][c]["ticket"]

            if color_array[int(chosen_color)-1][0] == "#":
                tdata = "<td bgcolor=\""
            else:
                tdata = "<td background=\""
            print tdata + \
                color_array[int(chosen_color)-1] + \
                "\" data-toggle=\"tooltip\" title=\"" + \
                "Description: " + display_description + "\n" +\
                "Env: cloud" + str(chosen_color) + "\n" + \
                "Owner: " + display_owner + "\n" + \
                "RT: " + display_ticket + "\n" + \
                "Day: " + str(cell_day) + "\n" + \
                "\"></td>"
        print "</tr>"
    print "</table>"
    print "</body>"
    print "</html>"
    return

if host_file:
    with open(host_file, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
else:
    your_list = []
    for h in sorted(quads.data['hosts'].iterkeys()):
        your_list.append([h])

your_list_colors = []
for h in your_list:
    one_host = []
    for d in range(0, days):
        day = d + 1
        if day < 10:
            daystring = "0" + str(day)
        else:
            daystring = str(day)
        default, current, override = quads.find_current(h[0],"{}-{}-{} 00:00".format(year,month,daystring))
        if current:
          one_host.append(current.lstrip("cloud"))
    your_list_colors.append(one_host)

print_simple_table(your_list, your_list_colors, days)
