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

parser = argparse.ArgumentParser(description='Generate a simple HTML table with color depicting resource usage for the month')
requiredArgs=parser.add_argument_group('Required Arguments')
requiredArgs.add_argument('-d', '--days', dest='days', type=int, required=True, default=None, help='number of days to generate')
requiredArgs.add_argument('--host-file', dest='host_file', type=str, required=True, default=None, help='file with list of hosts')
requiredArgs.add_argument('--host-color-file', dest='host_color_file', type=str, required=True, default=None, help='file with list of colors to use across days per host')
parser.add_argument('--gentime', '-g', dest='gentime', type=str, required=False, default=None, help='generate timestamp when created')

args = parser.parse_args()
host_file = args.host_file
host_color_file = args.host_color_file
days = args.days
gentime = args.gentime

def get_spaced_colors():
    return [(190,193,212),(2,63,165),(216,19, 19),(187,119,132),(142,6,59),(74,111,227),(230,175,185),(211,63,106),(17,198,56),(239,151,8),(15,207,192),(247,156,212)]

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
    print "<table>"
    print "<tr>"
    print "<th>Name</th>"
    print "<th>Color</th>"
    print "</tr>"
    for i in range(0, 10):
        print "<tr>"
        print "<td> cloud" + ('0' if i < 9 else '') + str(i+1) + " </td>"
        print "<td bgcolor=\"" + str(color_array[i]) + "\"></td>"
    print "</table>"
    print "<br>"
    print "<table>"
    print "<tr>"
    print "<th>Name</th>"
    for i in range(0, days):
        print "<th>" + ('0' if i < 9 else '') + str(i+1) + "</th>"
    print "</tr>"
    for i in range(0, len(data)):
        print "<tr>"
        print "<td>" + str(data[i][0]) + "</td>"
        for j in range(0, days):
            chosen_color = data_colors[i][j]
            print "<td bgcolor=\"" + color_array[int(chosen_color)-1] + "\"></td>"
        print "</tr>"
    print "</table>"
    print "</body>"
    print "</html>"
    return

import csv
with open(host_file, 'r') as f:
    reader = csv.reader(f)
    your_list = list(reader)

with open(host_color_file, 'r') as f:
    reader = csv.reader(f)
    your_list_colors = list(reader)

print_simple_table(your_list, your_list_colors, days)
