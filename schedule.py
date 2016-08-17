#!/usr/bin/env python

from datetime import datetime
import yaml
import argparse
import os
from subprocess import call

defaultconfig = "/etc/lab/schedule.yaml"
defaultstatedir = "/etc/lab/state"
defaultmovecommand = "/bin/echo"

parser = argparse.ArgumentParser(description='Query current cloud for a given host')
parser.add_argument('--host', dest='host', type=str, default=None, help='Specify the host to query')
parser.add_argument('--cloud-only', dest='cloudonly', type=str, default=None, help='Limit full report to hosts only in this cloud')
parser.add_argument('-c', '--config', dest='config',
                                            help='YAML file with cluster data',
                                            default=None, type=str)
parser.add_argument('-d', '--datetime', dest='datearg', type=str, default=None, help='date and time to query; e.g. "2016-06-01 08:00"')
parser.add_argument('-i', '--init', dest='initialize', action='store_true', help='initialize the schedule YAML file')
parser.add_argument('--define-cloud', dest='cloudresource', type=str, default=None, help='Define a cloud environment')
parser.add_argument('--define-host', dest='hostresource', type=str, default=None, help='Define a host resource')
parser.add_argument('--description', dest='description', type=str, default=None, help='Defined description of cloud')
parser.add_argument('--default-cloud', dest='hostcloud', type=str, default=None, help='Defined default cloud for a host')
parser.add_argument('--force', dest='force', action='store_true', help='Force host or cloud update when already defined')
parser.add_argument('--summary', dest='summary', action='store_true', help='Generate a summary report')
parser.add_argument('--add-schedule', dest='addschedule', action='store_true', help='Define a host reservation')
parser.add_argument('--schedule-start', dest='schedstart', type=str, default=None, help='Schedule start date/time')
parser.add_argument('--schedule-end', dest='schedend', type=str, default=None, help='Schedule end date/time')
parser.add_argument('--schedule-cloud', dest='schedcloud', type=str, default=None, help='Schedule cloud')
parser.add_argument('--ls-schedule', dest='lsschedule', action='store_true', help='List the host reservations')
parser.add_argument('--rm-schedule', dest='rmschedule', type=int, default=None, help='Remove a host reservation')
parser.add_argument('--ls-hosts', dest='lshosts', action='store_true', default=None, help='List all hosts')
parser.add_argument('--ls-clouds', dest='lsclouds', action='store_true', default=None, help='List all clouds')
parser.add_argument('--rm-host', dest='rmhost', type=str, default=None, help='Remove a host')
parser.add_argument('--rm-cloud', dest='rmcloud', type=str, default=None, help='Remove a cloud')
parser.add_argument('--statedir', dest='statedir', type=str, default=None, help='Default state dir')
parser.add_argument('--sync', dest='syncstate', action='store_true', default=None, help='Sync state of hosts')
parser.add_argument('--move-hosts', dest='movehosts', action='store_true', default=None, help='Move hosts if schedule has changed')
parser.add_argument('--move-command', dest='movecommand', type=str, default=None, help='External command to move a host')
parser.add_argument('--dry-run', dest='dryrun', action='store_true', default=None, help='Dont update state when used with --move-hosts')

args = parser.parse_args()

host = args.host
cloudonly = args.cloudonly
config = args.config
datearg = args.datearg
initialize = args.initialize
cloudresource = args.cloudresource
hostresource = args.hostresource
description = args.description
hostcloud = args.hostcloud
forceupdate = args.force
summaryreport = args.summary
addschedule = args.addschedule
schedstart = args.schedstart
schedend = args.schedend
schedcloud = args.schedcloud
lsschedule = args.lsschedule
rmschedule = args.rmschedule
lshosts = args.lshosts
lsclouds = args.lsclouds
rmhost = args.rmhost
rmcloud = args.rmcloud
statedir = args.statedir
syncstate = args.syncstate
movehosts = args.movehosts
movecommand = args.movecommand
dryrun = args.dryrun

if config is None:
    config = defaultconfig

if statedir is None:
    statedir = defaultstatedir

if movecommand is None:
    movecommand = defaultmovecommand

if not os.path.exists(statedir):
    try:
        os.makedirs(statedir)
    except Exception, ex:
        print ex
        exit(1)

fname = config

def initConfig():
    global initialize
    global fname
    global data

    if initialize:
        try:
            stream = open(fname, 'w')
            data = {"clouds":{}, "hosts":{}}
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)

        except Exception, ex:
            print "There was a problem with your file %s" % ex
            exit(1)

def checkDefineOpts():
    global hostresource
    global cloudresource

    if hostresource is not None and cloudresource is not None:
        print "--define-cloud and --define-host are mutually exclusive."
        exit(1)

def loadData():
    global fname
    global data

    # load the current data
    try:
        stream = open(fname, 'r')
        data = yaml.load(stream)
        stream.close()
    except Exception, ex:
        print ex
        exit(1)

def writeData():
    global fname
    global data

    try:
        stream = open(fname, 'w')
        stream.write( yaml.dump(data, default_flow_style=False))
        exit(0)
    except Exception, ex:
        print "There was a problem with your file %s" % ex
        exit(1)


def syncState():
    global syncstate
    global data
    global statedir

    # sync state
    if syncstate:
        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = findCurrent(h)
            if not os.path.isfile(statedir + "/" + h):
                try:
                    stream = open(statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    print "There was a problem with your file %s" % ex
        exit(0)

def moveHosts():
    global movehosts
    global movecommand
    global dryrun
    global data
    global statedir

    if movehosts:
        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = findCurrent(h)
            if not os.path.isfile(statedir + "/" + h):
                try:
                    stream = open(statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    print "There was a problem with your file %s" % ex
            else:
                stream = open(statedir + "/" + h, 'r')
                current_state = stream.readline().rstrip()
                stream.close()
                if current_state != current_cloud:
                    print "INFO: Moving " + h + " from " + current_state + " to " + current_cloud
                    if not dryrun:
                        call([movecommand, h, current_state, current_cloud])
                        stream = open(statedir + "/" + h, 'w')
                        stream.write(current_cloud + '\n')
                        stream.close()
        exit(0)

def listHosts():
    global lshosts
    global data

    # list just the hostnames
    if lshosts:
        for h in sorted(data['hosts'].iterkeys()):
            print h
        exit(0)

def listClouds():
    global lsclouds
    global data

    # list just the clouds
    if lsclouds:
        for c in sorted(data['clouds'].iterkeys()):
            print c
        exit(0)

def removeHost():
    global rmhost
    global data

    # remove a specific host
    if rmhost is not None:
        if rmhost not in data['hosts']:
            print rmhost + " not found"
            exit(1)
        del(data['hosts'][rmhost])
        writeData()

def removeCloud():
    global rmcloud
    global data

    # remove a cloud (only if no hosts use it)
    if rmcloud is not None:
        if rmcloud not in data['clouds']:
            print rmcloud + " not found"
            exit(1)
        for h in data['hosts']:
            if data['hosts'][h]["cloud"] == rmcloud:
                print rmcloud + " is default for " + h
                print "Change the default before deleting this cloud"
                exit(1)
            for s in data['hosts'][h]["schedule"]:
                if data['hosts'][h]["schedule"][s]["cloud"] == rmcloud:
                    print rmcloud + " is used in a schedule for "  + h
                    print "Delete schedule before deleting this cloud"
                    exit(1)
        del(data['clouds'][rmcloud])
        writeData()

def updateHost():
    global hostresource
    global hostcloud
    global data
    global forceupdate

    # define or update a host resouce
    if hostresource is not None:
        if hostcloud is None:
            print "--default-cloud is required when using --define-host"
            exit(1)
        else:
            if hostcloud not in data['clouds']:
                print "Unknown cloud : %s" % hostcloud
                print "Define it first using:  --define-cloud"
                exit(1)
            if hostresource in data['hosts'] and not forceupdate:
                print "Host \"%s\" already defined. Use --force to replace" % hostresource
                exit(1)

            if hostresource in data['hosts']:
                data["hosts"][hostresource] = { "cloud": hostcloud, "interfaces": data["hosts"][hostresource]["interfaces"], "schedule": data["hosts"][hostresource]["schedule"] }
            else:
                data["hosts"][hostresource] = { "cloud": hostcloud, "interfaces": {}, "schedule": {}}
            writeData()

def updateCloud():
    global cloudresource
    global description
    global data
    global forceupdate

    # define or update a cloud resource
    if cloudresource is not None:
        if description is None:
            print "--description is required when using --define-cloud"
            exit(1)
        else:
            if cloudresource in data['clouds'] and not forceupdate:
                print "Cloud \"%s\" already defined. Use --force to replace" % cloudresource
                exit(1)
            data["clouds"][cloudresource] = { "description": description, "networks": {}}
            writeData()

def addHostSchedule():
    global addschedule
    global schedstart
    global schedend
    global schedcloud
    global host
    global data

    # add a scheduled override for a given host
    if addschedule:
        if schedstart is None or schedend is None or schedcloud is None or host is None:
            print "Missing option. All these options are required for --add-schedule:"
            print "    --host"
            print "    --schedule-start"
            print "    --schedule-end"
            print "    --schedule-cloud"
            exit(1)

        try:
            datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        except Exception, ex:
            print "Data format error : %s" % ex
            exit(1)

        try:
            datetime.strptime(schedend, '%Y-%m-%d %H:%M')
        except Exception, ex:
            print "Data format error : %s" % ex
            exit(1)

        if schedcloud not in data['clouds']:
            print "cloud \"" + schedcloud + "\" is not defined."
            exit(1)

        if host not in data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        # before updating the schedule (adding the new override), we need to
        # ensure the host does not have existing schedules that overlap the new
        # schedule being requested

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in data['hosts'][host]["schedule"]:
            s_start = data['hosts'][host]["schedule"][s]["start"]
            s_end = data['hosts'][host]["schedule"][s]["end"]
            s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
            s_end_obj = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

            # need code to see if schedstart or schedend is between s_start and
            # s_end

            if s_start_obj <= schedstart_obj and schedstart_obj <= s_end_obj:
                print "Error. New schedule conflicts with existing schedule."
                print "New schedule: "
                print "   Start: " + schedstart
                print "   End: " + schedend
                print "Existing schedule: "
                print "   Start: " + s_start
                print "   End: " + s_end
                exit(1)

            if s_start_obj <= schedend_obj and schedend_obj <= s_end_obj:
                print "Error. New schedule conflicts with existing schedule."
                print "New schedule: "
                print "   Start: " + schedstart
                print "   End: " + schedend
                print "Existing schedule: "
                print "   Start: " + s_start
                print "   End: " + s_end
                exit(1)

        data['hosts'][host]["schedule"][len(data['hosts'][host]["schedule"].keys())] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
        writeData()

def rmHostSchedule():
    global rmschedule
    global host
    global data

    # remove a scheduled override for a given host
    if rmschedule is not None:
        if host is None:
            print "Missing --host option required for --rm-schedule"
            exit(1)

        if host not in data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        if rmschedule not in data['hosts'][host]["schedule"].keys():
            print "Could not find schedule for host"
            exit(1)

        del(data['hosts'][host]["schedule"][rmschedule])
        writeData()

def findCurrent(host):
    global data
    global datearg
    global summary

    if host in data['hosts'].keys():
        default_cloud = data['hosts'][host]["cloud"]
        current_cloud = default_cloud
        current_override = None
        if "schedule" in data['hosts'][host].keys():
            for override in data['hosts'][host]["schedule"]:
                start_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["start"], '%Y-%m-%d %H:%M')
                end_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["end"], '%Y-%m-%d %H:%M')
                if datearg is None:
                    current_time = datetime.now()
                else:
                    try:
                        current_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')
                    except Exception, ex:
                        print "Data format error : %s" % ex
                        exit(1)

                if start_obj <= current_time and current_time <= end_obj:
                    current_cloud = data['hosts'][host]["schedule"][override]["cloud"]
                    current_override = override
        return default_cloud, current_cloud, current_override
    else:
        return None, None, None

def printResult():
    global host
    global cloudonly
    global data
    global datearg
    global summary
    global summaryreport

    # If we're here, we're done with all other options and just need to
    # print either summary, full report if no host is specified
    if host is None:
        summary = {}

        for cloud in sorted(data['clouds'].iterkeys()):
            summary[cloud] = []

        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = findCurrent(h)
            summary[current_cloud].append(h)

        if summaryreport:
            for cloud in sorted(data['clouds'].iterkeys()):
                print cloud + " : " + str(len(summary[cloud])) + " (" + data["clouds"][cloud]["description"] + ")"
        else:
            for cloud in sorted(data['clouds'].iterkeys()):
                if cloudonly is None:
                    print cloud + ":"
                    for h in summary[cloud]:
                        print "  - " + h
                else:
                    if cloud == cloudonly:
                        for h in summary[cloud]:
                            print h

    # print the cloud a host belongs to
    else:
        default_cloud, current_cloud, current_override = findCurrent(host)

        if host is not None:
            if lsschedule:
                print "Default cloud: " + str(default_cloud)
                print "Current cloud: " + str(current_cloud)
                if current_override is not None:
                    print "Current schedule: " + str(current_override)
                print "Defined schedules:"
                if host in data['hosts'].keys():
                    for override in data['hosts'][host]["schedule"]:
                        print "  " + str(override) + "| start=" + data['hosts'][host]["schedule"][override]["start"] + ",end=" + data['hosts'][host]["schedule"][override]["end"] + ",cloud=" + data['hosts'][host]["schedule"][override]["cloud"]
            else:
                print current_cloud


initConfig()
checkDefineOpts()
loadData()
syncState()
listHosts()
listClouds()
removeHost()
removeCloud()
updateHost()
updateCloud()
addHostSchedule()
rmHostSchedule()
moveHosts()
printResult()



