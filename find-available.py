#!/usr/bin/env python
# query availability of machines
# e.g.
# find 4 machines for 4 days of type r620
# find-available.py -c 4 -d 4 -l '620'

import itertools
import string
import argparse
import os
import sys
import array
from subprocess import call
from subprocess import check_call

parser = argparse.ArgumentParser(description='Find first available time for lab reservation')
parser.add_argument('-c', '--count', dest='count', type=int, default=None, help='number of nodes needed')
parser.add_argument('-d', '--days', dest='days', type=int, default=None, help='number of days needed')
parser.add_argument('-l', '--limit', dest='limited', type=str, default=None, help='limit hostnames to match')
parser.add_argument('--debug', dest='debug', action='store_true',help='debug output')

def printf(format, *args):
    sys.stdout.write(format % args)

args = parser.parse_args()
count = args.count
days = args.days
limited = args.limited
debug = args.debug

hostset = ()
hostnames = ()

if count is None or days is None:
    print "Usage: find-available.py -c COUNT -d DAYS"
    exit(1)

def avail_for(start_day, n, duration):
    global hostset
    global hostnames
    global limited
    global debug

    if debug:
        print "DEBUG: avail_for called with : start_days = " + str(start_day) + ", n = " + str(n) + ", duration = " + str(duration)
    datecommand = "date -d \"today + " + str(start_day) + " days \" '+%Y-%m-%d 08:00'"
    datestring = os.popen(datecommand).read().rstrip('\n')
    schedulepycommand = "/root/schedule.py --cloud-only cloud01 --date \"" + datestring + "\""
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
        for item in itertools.combinations(i, n):
            fail = False
            for k in item:
                for t in range(start_day, (start_day + duration)):
                    datecommand = "date -d \"today + " + str(t) + " days \" '+%Y-%m-%d 08:00'"
                    datestring = os.popen(datecommand).read().rstrip('\n')
                    schedulepycommand = "/root/schedule.py --host " + myresult[k] + " --date \"" + datestring + "\""
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

    count = 0
    increment = 0
    while count < node_count and avail_for(increment, node_count, for_days) != 0:
        datecommand = "date -d \"today + " + str(increment) + " days \" '+%Y-%m-%d 08:00'"
        datestring = os.popen(datecommand).read().rstrip('\n')
        schedulepycommand = "/root/schedule.py --cloud-only cloud01 --date \"" + datestring + "\""
        if limited != None:
            schedulepycommand += "| egrep '" + limited + "'"
#        schedulepycommand = "/root/schedule.py --full-summary --date \"" + datestring + "\" | grep cloud01 | awk '{ print $3 }'"
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
print "================"
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
print "================"
print "Schedule Commands:"
print "------------------"
for k in hostset:
    print "schedule.py --host " + hostnames[k] + " --add-schedule --schedule-start \"" + startdatestring + "\" --schedule-end \"" + enddatestring + "\" --schedule-cloud cloudXX"

exit(0)
