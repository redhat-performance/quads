#!/usr/bin/env python
# tool to query lab schedule and find available nodes
# e.g. find 10 nodes for 20 consecutive days
# ./find-availably.py -c 10 -d 20

import itertools
import string
import argparse
import os
import sys
import array
import yaml
from subprocess import call
from subprocess import check_call

parser = argparse.ArgumentParser(description='Find first available time for lab reservation')
requiredArgs=parser.add_argument_group('Required Arguments')
requiredArgs.add_argument('-c', '--count', dest='count', type=int, required=True, default=None, help='number of nodes needed')
requiredArgs.add_argument('-d', '--days', dest='days', type=int, required=True, default=None, help='number of days needed')
parser.add_argument('-l', '--limit', dest='limited', type=str, required=False, default=None, help='limit hostnames to match')
parser.add_argument('--debug', dest='debug', action='store_true', required=False, help='debug output')
parser.add_argument('-C', '--cli', dest='cli', action='store_true', required=False, help='print QUADS example schedule commands')

def printf(format, *args):
    sys.stdout.write(format % args)

args = parser.parse_args()
count = args.count
days = args.days
limited = args.limited
debug = args.debug
cli = args.cli

hostset = ()
hostnames = ()

quads_config = os.path.dirname(__file__) + "/../conf/quads.yml"
quads = {}

def load_quads_config():
    global quads_config
    global quads

    try:
        stream = open(quads_config, 'r')
        quads = yaml.load(stream)
        stream.close()
    except Exception, ex:
        print ex
        exit(1)

load_quads_config()


def avail_for(start_day, n, duration):
    global hostset
    global hostnames
    global limited
    global debug
    global quads

    if debug:
        print "DEBUG: avail_for called with : start_days = " + str(start_day) + ", n = " + str(n) + ", duration = " + str(duration)
    datecommand = "date -d \"today + " + str(start_day) + " days \" '+%Y-%m-%d 08:00'"
    datestring = os.popen(datecommand).read().rstrip('\n')
    schedulepycommand = quads["install_dir"] + "/bin/quads.py --cloud-only cloud01 --date \"" + datestring + "\""
    if limited != None:
        schedulepycommand += "| egrep '" + limited + "'"
    if debug:
        print "DEBUG: schedulepycommand = " + schedulepycommand
    myoutput = os.popen(schedulepycommand).read().rstrip('\n')
    if debug:
        print "DEBUG: myoutput = " + myoutput
    host_list = [y for y in (x.strip() for x in myoutput.splitlines()) if y]
    myresult = host_list
    hostnames = myresult

    i = []
    for j in range(0, len(myresult)):
        i.append(j)

    if n <= len(myresult):
		# item is a single combination of hosts (expressed as integer index into myresult)
		# we are iterating over them.
        for item in itertools.combinations(i, n):
            fail = False
			# k is a single host in the combination (actually the index)
            for k in item:
				# here we check that the host stays in cloud01 (in other words available)
				# for the duration of days we are requesting
                for t in range(start_day, (start_day + duration)):
                    datecommand = "date -d \"today + " + str(t) + " days \" '+%Y-%m-%d 08:00'"
                    datestring = os.popen(datecommand).read().rstrip('\n')
                    schedulepycommand = quads["install_dir"] + "/bin/quads.py --host " + myresult[k] + " --date \"" + datestring + "\""
                    if debug:
                        print "DEBUG: schedulepycommand = " + schedulepycommand
                    schedulepyresult = os.popen(schedulepycommand).read().rstrip('\n')
                    if schedulepyresult != "cloud01":
                        fail = True
			if not fail:
				hostset = item
				return 0
    if debug:
        print "DEBUG: avail_for return(1)"
    return 1

def find_date(node_count, for_days):
    global debug
    global quads

    count = 0
    increment = 0
    while count < node_count and avail_for(increment, node_count, for_days) != 0:
        datecommand = "date -d \"today + " + str(increment) + " days \" '+%Y-%m-%d 08:00'"
        datestring = os.popen(datecommand).read().rstrip('\n')
        schedulepycommand = quads["install_dir"] + "/bin/quads.py --cloud-only cloud01 --date \"" + datestring + "\""
        if limited != None:
            schedulepycommand += "| egrep '" + limited + "'"
        schedulepycommand += "| wc -l"
        schedulepystring = os.popen(schedulepycommand).read().rstrip('\n')
        count = int(schedulepystring)
        if count < node_count:
            if debug:
                print "DEBUG: only " + str(count) + " nodes available. Continuing"
            increment += 1
    if debug:
        print "DEBUG: count = " + str(count) + ", node_count = " + str(node_count)
        print "DEBUG: find_date return(" + str(increment) + ")"
    return increment

first_avail = find_date(count, days)
datecommand = "date -d \"today + " + str(first_avail) + " days \" '+%Y-%m-%d 08:00'"
startdatestring = os.popen(datecommand).read().rstrip('\n')
print "=================="
print "First available date = " + startdatestring
datecommand = "date -d \"today + " + str(first_avail + days) + " days \" '+%Y-%m-%d 08:00'"
if debug:
    print "DEBUG: datecommand for end date = " + datecommand
enddatestring = os.popen(datecommand).read().rstrip('\n')
if debug:
    print "DEBUG: datestring for end date = " + enddatestring
print "Requested end date = " + enddatestring
print "hostnames = "
for k in hostset:
    print hostnames[k]
if cli:
    print "=================="
    print "Schedule Commands:"
    print "------------------"
    for k in hostset:
        print quads["install_dir"] + "/bin/quads.py --host " + hostnames[k] + " --add-schedule --schedule-start \"" + startdatestring + "\" --schedule-end \"" + enddatestring + "\" --schedule-cloud cloudXX"

exit(0)
