#!/usr/bin/env python
# convert the quads --schedule-start date and time and
# schedule an at notification to send an email when it fires off

import argparse
import os
import re

parser = argparse.ArgumentParser(description='Find first available time for lab reservation')
requiredArgs=parser.add_argument_group('Required Arguments')
requiredArgs.add_argument('-d', '--startdate', dest='startdate', type=str, required=True, default=None, help='enter date range e.g. 2016-11-22 08:00')
requiredArgs.add_argument('-c', '--cloud', dest='cloud', type=str, required=True, default=None, help='cloud being scheduled') 

args = parser.parse_args()
startdate = args.startdate
cloud = args.cloud

# strip out "-" and ":" characters from the date
startdate_at_pre = re.sub('[:-]', '', startdate)
# strip out any spaces
startdate_at = startdate_at_pre.translate(None, '" "')

# schedule notification with the external 'at' command
notifycmd = '/tmp/cloudstart_notify.sh %s' % cloud
atnotify = '/usr/bin/at -t %s < %s' % (startdate_at,notifycmd)
# schedule with at command
os.system(atnotify)

# print acknowledgement to the screen
print "Scheduling a Notification for %s on Starting Date %s" % (cloud,startdate)
