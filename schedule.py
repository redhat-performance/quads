#!/bin/python

from datetime import datetime
import yaml
import argparse

parser = argparse.ArgumentParser(description='Query current cloud for a given host')
parser.add_argument('--host', dest='host', type=str, default=None, help='Specify the host to query')
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

args = parser.parse_args()

host = args.host
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

if config is None:
    config = "/etc/labsched/schedule.yaml"

fname = config

if initialize:
    try:
        stream = open(fname, 'w')
        data = {"clouds":{}, "hosts":{}}
        stream.write( yaml.dump(data, default_flow_style=False))
        exit(0)

    except Exception, ex:
        print "There was a problem with your file %s" % ex
        SystemExit(4)

if hostresource is not None and cloudresource is not None:
    print "--define-cloud and --define-host are mutually exclusive."
    exit(1)

# load the current data
try:
    stream = open(fname, 'r')
    data = yaml.load(stream)
    stream.close()
except Exception, ex:
    print "There was a problem with your file %s" % ex
    SystemExit(4)


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
        try:
            stream = open(fname, 'w')
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)
        except Exception, ex:
            print "There was a problem with your file %s" % ex
            SystemExit(4)


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
        try:
            stream = open(fname, 'w')
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)
        except Exception, ex:
            print "There was a problem with your file %s" % ex
            SystemExit(4)

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

    data['hosts'][host]["schedule"][len(data['hosts'][host]["schedule"].keys())] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
    try:
        stream = open(fname, 'w')
        stream.write( yaml.dump(data, default_flow_style=False))
        exit(0)
    except Exception, ex:
        print "There was a problem with your file %s" % ex
        exit(1)

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
    try:
        stream = open(fname, 'w')
        stream.write( yaml.dump(data, default_flow_style=False))
        exit(0)
    except Exception, ex:
        print "There was a problem with your file %s" % ex
        SystemExit(4)


# If we're here, we're done with all other options and just need to
# print either summary, full report if no host is specified
if host is None:
    summary = {}

    for cloud in sorted(data['clouds'].iterkeys()):
        summary[cloud] = []

    for h in sorted(data['hosts'].iterkeys()):
        default_cloud = data['hosts'][h]["cloud"]
        current_cloud = default_cloud
        if "schedule" in data['hosts'][h].keys():
            for override in data['hosts'][h]["schedule"]:
                # print data['hosts'][h]["schedule"][override]
                start_obj = datetime.strptime(data['hosts'][h]["schedule"][override]["start"], '%Y-%m-%d %H:%M')
                end_obj = datetime.strptime(data['hosts'][h]["schedule"][override]["end"], '%Y-%m-%d %H:%M')
                if datearg is None:
                    current_time = datetime.now()
                else:
                    current_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')
                if start_obj <= current_time and current_time <= end_obj:
                    current_cloud = data['hosts'][h]["schedule"][override]["cloud"]
        summary[current_cloud].append(h)

    if summaryreport:
        for cloud in sorted(data['clouds'].iterkeys()):
            print cloud + " : " + str(len(summary[cloud])) + " (" + data["clouds"][cloud]["description"] + ")"
    else:
        for cloud in sorted(data['clouds'].iterkeys()):
            print cloud + ":"
            for h in summary[cloud]:
                print "  - " + h

# print the cloud a host belongs to
else:
    if host in data['hosts'].keys():
        default_cloud = data['hosts'][host]["cloud"]
        current_cloud = default_cloud
        if "schedule" in data['hosts'][host].keys():
            for override in data['hosts'][host]["schedule"]:
                # print data['hosts'][host]["schedule"][override]
                start_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["start"], '%Y-%m-%d %H:%M')
                end_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["end"], '%Y-%m-%d %H:%M')
                if datearg is None:
                    current_time = datetime.now()
                else:
                    current_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')

                if start_obj <= current_time and current_time <= end_obj:
                    current_cloud = data['hosts'][host]["schedule"][override]["cloud"]

        if lsschedule:
            print "Default cloud: " + default_cloud
            print "Current cloud: " + current_cloud
            print "Defined schedules:"
            for override in data['hosts'][host]["schedule"]:
                print "  " + str(override) + ":"
                print "    start: " + data['hosts'][host]["schedule"][override]["start"]
                print "    end: " + data['hosts'][host]["schedule"][override]["end"]
                print "    cloud: " + data['hosts'][host]["schedule"][override]["cloud"]
        else:
            print current_cloud


