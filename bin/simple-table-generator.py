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
        stream = open(quads_config, 'r')
        try:
            quads_config_yaml = yaml.load(stream)
            stream.close()
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
sys.path.append(os.path.dirname(__file__) + "/../lib")

# Load QUADS object
import libquads

defaultstatedir = quads_config["data_dir"] + "/state"
defaultmovecommand = "/bin/echo"

quads = libquads.Quads(quads_config["data_dir"] + "/schedule.yaml",
                       defaultstatedir, defaultmovecommand,
                       None, None, False, False)

# Set maxcloud to maximum defined clouds
maxcloud = len(quads.quads.clouds.data)

# define color palette
# https://www.google.com/#q=rgb+color+picker&*
def get_spaced_colors():
    return [(190,193,212),
            (2,63,165),
            (216,19, 19),
            (187,119,132),
            (142,6,59),
            (74,111,227),
            (230,175,185),
            (211,63,106),
            (17,198,56),
            (239,151,8),
            (15,207,192),
            (247,156,212),
            (229, 244, 66),
            (107, 66, 6),
            (161, 0, 255),
            (155, 255, 140)]

# covert palette to hex
def get_cell_color(a, b, c):
    return "#" + ('0' if len(hex(a)) < 4 else '') + hex(a)[2:] + ('0' if len(hex(b)) < 4 else '') + hex(b)[2:] + ('0' if len(hex(c)) < 4 else '') + hex(c)[2:]

colors = get_spaced_colors()
color_array = []

for i in colors:
    color_array.append(get_cell_color(i[0], i[1], i[2]))

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
    print "<table>"
    print "<tr>"
    print "<th>Name</th>"
    print "<th>Color</th>"
    print "</tr>"
    # Here we generate the range of defined clouds for visuals
    for i in range(0, int(maxcloud)):
        print "<tr>"
        print "<td> cloud" + ('0' if i < 9 else '') + str(i+1) + " </td>"
        print "<td bgcolor=\"" + str(color_array[i]) + "\"></td>"
    print "</table>"
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
            for c in sorted(quads.quads.cloud_history.data["cloud" + str(chosen_color)]):
                if datetime.fromtimestamp(c) <= cell_time:
                    display_description = quads.quads.cloud_history.data["cloud" + str(chosen_color)][c]["description"]
                    display_owner = quads.quads.cloud_history.data["cloud" + str(chosen_color)][c]["owner"]
                    display_ticket = quads.quads.cloud_history.data["cloud" + str(chosen_color)][c]["ticket"]
            print "<td bgcolor=\"" + \
                color_array[int(chosen_color)-1] + \
                "\" data-toggle=\"tooltip\" title=\"" + \
                "Description: " + display_description + "\n" +\
                "Env: cloud" + str(chosen_color) + "\n" + \
                "Owner: " + display_owner + "\n" + \
                "RT: " + display_ticket + "\n" + \
                "\"></td>"
        print "</tr>"
    print "</table>"
    print "</body>"
    print "</html>"
    return

import csv

if host_file:
    with open(host_file, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
else:
    your_list = []
    for h in sorted(quads.quads.hosts.data.iterkeys()):
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
        default, current, override = quads._quads_find_current(h[0],"{}-{}-{} 00:00".format(year,month,daystring))
        one_host.append(current.lstrip("cloud"))
    your_list_colors.append(one_host)

print_simple_table(your_list, your_list_colors, days)
