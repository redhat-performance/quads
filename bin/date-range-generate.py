#!/usr/bin/env python
#
# generates date range

from subprocess import call
import argparse
import os
import datetime

parser = argparse.ArgumentParser(description='Generate ical file showing resource allocations')
parser.add_argument('--start-date', dest='startdate', type=str, default=None, help='Specify start date')
parser.add_argument('--end-date', dest='enddate', type=str, default=None, help='Specify end date')

args=parser.parse_args()

# authentication and wp url
startdate = args.startdate
enddate = args.enddate

if startdate is None or enddate is None:
    print "Both --start-date and --end-date are required"
    exit(1)

try:
    datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M')
except Exception, ex:
    print "Data format error : %s" % ex
    exit(1)

try:
    datetime.datetime.strptime(enddate, '%Y-%m-%d %H:%M')
except Exception, ex:
    print "Data format error : %s" % ex
    exit(1)

def daterange( start_date, end_date ):
    if start_date <= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            yield start_date + datetime.timedelta( n )
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            yield start_date - datetime.timedelta( n )


for date in daterange( datetime.datetime.strptime(startdate, '%Y-%m-%d %H:%M'),
                       datetime.datetime.strptime(enddate, '%Y-%m-%d %H:%M')
                      ):
    print date
