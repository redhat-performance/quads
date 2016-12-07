#!/bin/python

from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
from subprocess import call
from subprocess import check_call

# used to load the configuration for quads behavior
def quads_load_config(quads_config):
    try:
        stream = open(quads_config, 'r')
        quads = yaml.load(stream)
        stream.close()
    except Exception, ex:
        print ex
        exit(1)
    return(quads)

# if passed --init, the config data is wiped. Consider a confirmation dialog here
def quads_init_config(initialize, fname):
    if initialize:
        try:
            stream = open(fname, 'w')
            data = {"clouds":{}, "hosts":{}}
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)
        except Exception, ex:
            print "There was a problem with your file %s" % ex
            exit(1)

# check for mutually exclusive define options
def quads_check_define_opts(hostresource, cloudresource):
    if hostresource is not None and cloudresource is not None:
        print "--define-cloud and --define-host are mutually exclusive."
        exit(1)

# anything we do needs our data to be loaded.  So we start with that
def quads_load_data(fname):
    # load the current data
    try:
        stream = open(fname, 'r')
        data = yaml.load(stream)
        stream.close()
    except Exception, ex:
        print ex
        exit(1)
    return data

# we occasionally need to write the data back out
def quads_write_data(fname, data, doexit = True):
    try:
        stream = open(fname, 'w')
        stream.write( yaml.dump(data, default_flow_style=False))
        if doexit:
            exit(0)
    except Exception, ex:
        print "There was a problem with your file %s" % ex
        if doexit:
            exit(1)


# sync the statedir db for hosts with schedule
def quads_sync_state(syncstate, data, statedir, datearg):
    # sync state
    if datearg is not None:
        print "--sync and --date are mutually exclusive."
        exit(1)
    if syncstate:
        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = quads_find_current(data, datearg, h)
            if not os.path.isfile(statedir + "/" + h):
                try:
                    stream = open(statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    print "There was a problem with your file %s" % ex
        exit(0)

# as needed move host(s) based on defined schedules
def quads_move_hosts(movehosts, movecommand, dryrun, data, statedir, datearg):
    # move a host
    if datearg is not None:
        print "--move-hosts and --date are mutually exclusive."
        exit(1)
    if movehosts:
        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = quads_find_current(data, datearg, h)
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
                        try:
                            check_call([movecommand, h, current_state, current_cloud])
                        except Exception, ex:
                            print "Move command failed: %s" % ex
                            exit(1)
                        stream = open(statedir + "/" + h, 'w')
                        stream.write(current_cloud + '\n')
                        stream.close()
        exit(0)

# initialize history        
def quads_history_init(fname, data):
    updateyaml = False
    if 'history' not in data:
        data['history']  = {}
        updateyaml = True

    for h in sorted(data['hosts'].iterkeys()):
        if h not in data['history']:
            data['history'][h] = {}
            default_cloud, current_cloud, current_override = quads_find_current(data, None, h)
            data['history'][h][0] = current_cloud
            updateyaml = True

    if updateyaml:
        quads_write_data(fname, data, False)

    return data

# list the hosts
def quads_list_hosts(lshosts, data):
    # list just the hostnames
    if lshosts:
        for h in sorted(data['hosts'].iterkeys()):
            print h
        exit(0)

# list the clouds
def quads_list_clouds(lsclouds, data):
    # list just the clouds
    if lsclouds:
        for c in sorted(data['clouds'].iterkeys()):
            print c
        exit(0)

# list the owners
def quads_list_owners(lsowner, data, cloudonly):
    # list the owners
    if lsowner:
        if cloudonly is not None:
            if cloudonly not in data['clouds']:
                exit(0)
            print data['clouds'][cloudonly]['owner']
            exit(0)

        for c in sorted(data['clouds'].iterkeys()):
            print c + " : " + data['clouds'][c]['owner']

        exit(0)

# list the tickets
def quads_list_tickets(lsticket, data, cloudonly):
    # list the service request tickets
    if lsticket:
        if cloudonly is not None:
            if cloudonly not in data['clouds']:
                exit(0)
            if 'ticket' not in data['clouds'][cloudonly]:
                exit(0)
            print data['clouds'][cloudonly]['ticket']
            exit(0)

        for c in sorted(data['clouds'].iterkeys()):
            if 'ticket' in data['clouds'][c]:
                print c + " : " + data['clouds'][c]['ticket']

        exit(0)


# remove a host
def quads_remove_host(fname, data, rmhost):
    # remove a specific host
    if rmhost is not None:
        if rmhost not in data['hosts']:
            print rmhost + " not found"
            exit(1)
        del(data['hosts'][rmhost])
        quads_write_data(fname, data)

    return data

# remove a cloud
def quads_remove_cloud(fname, data, rmcloud):
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
        quads_write_data(fname, data)

    return data

# update a host resource
def quads_update_host(fname, hostresource, hostcloud, data, forceupdate):
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
                data["history"][hostresource][int(time.time())] = hostcloud
            else:
                data["hosts"][hostresource] = { "cloud": hostcloud, "interfaces": {}, "schedule": {}}
                data["history"][hostresource] = {}
                data["history"][hostresource][0] = hostcloud
            quads_write_data(fname, data)

    return data

# update a cloud resource
def quads_update_cloud(fname, cloudresource, description, data, forceupdate, cloudowner, cloudticket):
    # define or update a cloud resource
    if cloudresource is not None:
        if description is None:
            print "--description is required when using --define-cloud"
            exit(1)
        else:
            if cloudresource in data['clouds'] and not forceupdate:
                print "Cloud \"%s\" already defined. Use --force to replace" % cloudresource
                exit(1)
            if cloudowner is None:
                cloudowner = "nobody"
            if cloudticket is None:
                cloudticket = "00000"
            data["clouds"][cloudresource] = { "description": description, "networks": {}, "owner": {}, "ticket": {}}
            if cloudowner is not None:
                data["clouds"][cloudresource]["owner"] = cloudowner
            if cloudticket is not None:
                data["clouds"][cloudresource]["ticket"] = cloudticket
            quads_write_data(fname, data)

    return data

# define a schedule for a given host
def quads_add_host_schedule(fname, addschedule, schedstart, schedend, schedcloud, host, data):
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

            if s_start_obj <= schedstart_obj and schedstart_obj < s_end_obj:
                print "Error. New schedule conflicts with existing schedule."
                print "New schedule: "
                print "   Start: " + schedstart
                print "   End: " + schedend
                print "Existing schedule: "
                print "   Start: " + s_start
                print "   End: " + s_end
                exit(1)

            if s_start_obj < schedend_obj and schedend_obj <= s_end_obj:
                print "Error. New schedule conflicts with existing schedule."
                print "New schedule: "
                print "   Start: " + schedstart
                print "   End: " + schedend
                print "Existing schedule: "
                print "   Start: " + s_start
                print "   End: " + s_end
                exit(1)

        data['hosts'][host]["schedule"][len(data['hosts'][host]["schedule"].keys())] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
        quads_write_data(fname, data)

    return data

# modify an existing schedule
def quads_mod_host_schedule(fname, modschedule, schedstart, schedend, schedcloud, host, data):
    # add a scheduled override for a given host
    if modschedule is not None:
        if host is None:
            print "Missing option. Need --host when using --mod-schedule"
            exit(1)

        if schedstart is None and schedend is None and schedcloud is None:
            print "Missing option. At least one these options are required for --mod-schedule:"
            print "    --schedule-start"
            print "    --schedule-end"
            print "    --schedule-cloud"
            exit(1)

        if schedstart:
            try:
                datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
            except Exception, ex:
                print "Data format error : %s" % ex
                exit(1)

        if schedend:
            try:
                datetime.strptime(schedend, '%Y-%m-%d %H:%M')
            except Exception, ex:
                print "Data format error : %s" % ex
                exit(1)

        if schedcloud:
            if schedcloud not in data['clouds']:
                print "cloud \"" + schedcloud + "\" is not defined."
                exit(1)

        if host not in data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        if modschedule not in data['hosts'][host]["schedule"].keys():
            print "Could not find schedule for host"
            exit(1)

        # before updating the schedule (modifying the new override), we need to
        # ensure the host does not have existing schedules that overlap the 
        # schedule being updated


        if not schedcloud:
            schedcloud = data['hosts'][host]["schedule"][modschedule]["cloud"]

        if not schedstart:
            schedstart = data['hosts'][host]["schedule"][modschedule]["start"]

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')

        if not schedend:
            schedend = data['hosts'][host]["schedule"][modschedule]["end"]

        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in data['hosts'][host]["schedule"]:
            if s != modschedule:
                s_start = data['hosts'][host]["schedule"][s]["start"]
                s_end = data['hosts'][host]["schedule"][s]["end"]
                s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
                s_end_obj = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

                # need code to see if schedstart or schedend is between s_start and
                # s_end

                if s_start_obj <= schedstart_obj and schedstart_obj < s_end_obj:
                    print "Error. Updated schedule conflicts with existing schedule."
                    print "Updated schedule: "
                    print "   Start: " + schedstart
                    print "   End: " + schedend
                    print "Existing schedule: "
                    print "   Start: " + s_start
                    print "   End: " + s_end
                    exit(1)

                if s_start_obj < schedend_obj and schedend_obj <= s_end_obj:
                    print "Error. Updated schedule conflicts with existing schedule."
                    print "Updated schedule: "
                    print "   Start: " + schedstart
                    print "   End: " + schedend
                    print "Existing schedule: "
                    print "   Start: " + s_start
                    print "   End: " + s_end
                    exit(1)

        data['hosts'][host]["schedule"][modschedule]["start"] = schedstart
        data['hosts'][host]["schedule"][modschedule]["end"] = schedend
        data['hosts'][host]["schedule"][modschedule]["cloud"] = schedcloud

        quads_write_data(fname, data)

    return data

# remove a scheduled override for a given host
def quads_rm_host_schedule(fname, rmschedule, host, data):
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
        quads_write_data(fname, data)

    return data

# helper function called from other methods.  Never called from main()
def quads_find_current(data, datearg, host):
    if host in data['hosts'].keys():
        default_cloud = data['hosts'][host]["cloud"]
        current_cloud = default_cloud
        current_override = None

        if datearg is None:
            current_time = datetime.now()
        else:
            try:
                current_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')
            except Exception, ex:
                print "Data format error : %s" % ex
                exit(1)

        if "schedule" in data['hosts'][host].keys():
            for override in data['hosts'][host]["schedule"]:
                start_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["start"], '%Y-%m-%d %H:%M')
                end_obj = datetime.strptime(data['hosts'][host]["schedule"][override]["end"], '%Y-%m-%d %H:%M')

                if start_obj <= current_time and current_time < end_obj:
                    current_cloud = data['hosts'][host]["schedule"][override]["cloud"]
                    current_override = override
                    return default_cloud, current_cloud, current_override

        for history in data['history'][host]:
            if datetime.fromtimestamp(history) <= current_time:
                current_cloud = data['history'][host][history]

        return default_cloud, current_cloud, current_override

    else:
        return None, None, None

# generally the last thing that happens is reporting results
def quads_print_result(host, cloudonly, data, datearg, summaryreport, fullsummaryreport, lsschedule):
    # If we're here, we're done with all other options and just need to
    # print either summary, full report if no host is specified
    if host is None:
        summary = {}

        for cloud in sorted(data['clouds'].iterkeys()):
            summary[cloud] = []

        for h in sorted(data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = quads_find_current(data, datearg, h)
            summary[current_cloud].append(h)

        if summaryreport or fullsummaryreport:
            if fullsummaryreport:
                for cloud in sorted(data['clouds'].iterkeys()):
                    print cloud + " : " + str(len(summary[cloud])) + " (" + data["clouds"][cloud]["description"] + ")"
            else:
                for cloud in sorted(data['clouds'].iterkeys()):
                    if len(summary[cloud]) > 0:
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
        default_cloud, current_cloud, current_override = quads_find_current(data, datearg, host)

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


def main(argv):
    quads_config = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads = {}
    data = {}

    quads = quads_load_config(quads_config)

    defaultconfig = quads["data_dir"] + "/schedule.yaml"
    defaultstatedir = quads["data_dir"] + "/state"
    defaultmovecommand = "/bin/echo"

    parser = argparse.ArgumentParser(description='Query current cloud for a given host')
    parser.add_argument('--host', dest='host', type=str, default=None, help='Specify the host to query')
    parser.add_argument('--cloud-only', dest='cloudonly', type=str, default=None, help='Limit full report to hosts only in this cloud')
    parser.add_argument('-c', '--config', dest='config',
                                            help='YAML file with cluster data',
                                            default=defaultconfig, type=str)
    parser.add_argument('-d', '--datetime', dest='datearg', type=str, default=None, help='date and time to query; e.g. "2016-06-01 08:00"')
    parser.add_argument('-i', '--init', dest='initialize', action='store_true', help='initialize the schedule YAML file')
    parser.add_argument('--ls-owner', dest='lsowner', action='store_true', default=None, help='List owners')
    parser.add_argument('--ls-ticket', dest='lsticket', action='store_true', default=None, help='List request ticket')
    parser.add_argument('--cloud-owner', dest='cloudowner', type=str, default=None, help='Define environment owner')
    parser.add_argument('--cloud-ticket', dest='cloudticket', type=str, default=None, help='Define environment ticket')
    parser.add_argument('--define-cloud', dest='cloudresource', type=str, default=None, help='Define a cloud environment')
    parser.add_argument('--define-host', dest='hostresource', type=str, default=None, help='Define a host resource')
    parser.add_argument('--description', dest='description', type=str, default=None, help='Defined description of cloud')
    parser.add_argument('--default-cloud', dest='hostcloud', type=str, default=None, help='Defined default cloud for a host')
    parser.add_argument('--force', dest='force', action='store_true', help='Force host or cloud update when already defined')
    parser.add_argument('--summary', dest='summary', action='store_true', help='Generate a summary report')
    parser.add_argument('--full-summary', dest='fullsummary', action='store_true', help='Generate a summary report')
    parser.add_argument('--add-schedule', dest='addschedule', action='store_true', help='Define a host reservation')
    parser.add_argument('--mod-schedule', dest='modschedule', type=int, default=None, help='Modify a host reservation')
    parser.add_argument('--schedule-start', dest='schedstart', type=str, default=None, help='Schedule start date/time')
    parser.add_argument('--schedule-end', dest='schedend', type=str, default=None, help='Schedule end date/time')
    parser.add_argument('--schedule-cloud', dest='schedcloud', type=str, default=None, help='Schedule cloud')
    parser.add_argument('--ls-schedule', dest='lsschedule', action='store_true', help='List the host reservations')
    parser.add_argument('--rm-schedule', dest='rmschedule', type=int, default=None, help='Remove a host reservation')
    parser.add_argument('--ls-hosts', dest='lshosts', action='store_true', default=None, help='List all hosts')
    parser.add_argument('--ls-clouds', dest='lsclouds', action='store_true', default=None, help='List all clouds')
    parser.add_argument('--rm-host', dest='rmhost', type=str, default=None, help='Remove a host')
    parser.add_argument('--rm-cloud', dest='rmcloud', type=str, default=None, help='Remove a cloud')
    parser.add_argument('--statedir', dest='statedir', type=str, default=defaultstatedir, help='Default state dir')
    parser.add_argument('--sync', dest='syncstate', action='store_true', default=None, help='Sync state of hosts')
    parser.add_argument('--move-hosts', dest='movehosts', action='store_true', default=None, help='Move hosts if schedule has changed')
    parser.add_argument('--move-command', dest='movecommand', type=str, default=defaultmovecommand, help='External command to move a host')
    parser.add_argument('--dry-run', dest='dryrun', action='store_true', default=None, help='Dont update state when used with --move-hosts')

    args = parser.parse_args()

    if not os.path.exists(args.statedir):
        try:
            os.makedirs(args.statedir)
        except Exception, ex:
            print ex
            exit(1)

    quads_init_config(args.initialize, args.config)
    quads_check_define_opts(args.hostresource, args.cloudresource)
    data = quads_load_data(args.config)
    quads_sync_state(args.syncstate, data, args.statedir, args.datearg)
    data = quads_history_init(args.config, data)
    quads_list_hosts(args.lshosts, data)
    quads_list_clouds(args.lsclouds, data)
    quads_list_owners(args.lsowner, data, args.cloudonly)
    quads_list_tickets(args.lsticket, data, args.cloudonly)
    data = quads_remove_host(args.config, data, args.rmhost)
    data = quads_remove_cloud(args.config, data, args.rmcloud)
    data = quads_update_host(args.config, args.hostresource, args.hostcloud, data, args.force)
    data = quads_update_cloud(args.config, args.cloudresource, args.description, data, args.force, args.cloudowner, args.cloudticket)
    data = quads_add_host_schedule(args.config, args.addschedule, args.schedstart, args.schedend, args.schedcloud, args.host, data)
    data = quads_rm_host_schedule(args.config, args.rmschedule, args.host, data)
    data = quads_mod_host_schedule(args.config, args.modschedule, args.schedstart, args.schedend, args.schedcloud, args.host, data)
    quads_move_hosts(args.movehosts, args.movecommand, args.dryrun, data, args.statedir, args.datearg)
    quads_print_result(args.host, args.cloudonly, data, args.datearg, args.summary, args.fullsummary, args.lsschedule)


if __name__ == "__main__":
       main(sys.argv[1:])
