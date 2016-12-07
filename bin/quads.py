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

class Quads(object):
    def __init__(self, config, statedir, movecommand, datearg, syncstate, initialize, force):
        """
        config: string
        Initialize a quads object.
        """
        self.config = config
        self.statedir = statedir
        self.movecommand = movecommand
        self.datearg = datearg

        if initialize:
            self.quads_init_data(force)
        try:
            stream = open(config, 'r')
            self.data = yaml.load(stream)
            stream.close()
        except Exception, ex:
            print ex
            exit(1)
        self._quads_history_init()
        if syncstate:
            self.quads_sync_state()

    # initialize history
    def _quads_history_init(self):
        updateyaml = False
        if 'history' not in self.data:
            self.data['history']  = {}
            updateyaml = True

        for h in sorted(self.data['hosts'].iterkeys()):
            if h not in self.data['history']:
                self.data['history'][h] = {}
                default_cloud, current_cloud, current_override = self._quads_find_current(h, None)
                self.data['history'][h][0] = current_cloud
                updateyaml = True

        if updateyaml:
            self.quads_write_data(False)

    # we occasionally need to write the data back out
    def quads_write_data(self, doexit = True):
        try:
            stream = open(self.config, 'w')
            stream.write( yaml.dump(self.data, default_flow_style=False))
            if doexit:
                exit(0)
        except Exception, ex:
            print "There was a problem with your file %s" % ex
            if doexit:
                exit(1)

    # if passed --init, the config data is wiped.
    # typically we will not want to continue execution if user asks to initialize
    def quads_init_data(self, force):
        if not force:
            if os.path.isfile(self.config):
                print "Warning: " + self.config + " exists. Use --force to initialize."
                exit(1)
        try:
            stream = open(self.config, 'w')
            data = {"clouds":{}, "hosts":{}, "history":{}}
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)
        except Exception, ex:
            print "There was a problem with your file %s" % ex
            exit(1)

    # helper function called from other methods.  Never called from main()
    def _quads_find_current(self, host, datearg):
        data = self.data

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

    # sync the statedir db for hosts with schedule
    def quads_sync_state(self):
        # sync state
        if self.datearg is not None:
            print "--sync and --date are mutually exclusive."
            exit(1)
        for h in sorted(self.data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = self._quads_find_current(h, self.datearg)
            if not os.path.isfile(self.statedir + "/" + h):
                try:
                    stream = open(self.statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    print "There was a problem with your file %s" % ex
        exit(0)

    # list the hosts
    def quads_list_hosts(self):
        # list just the hostnames
        for h in sorted(self.data['hosts'].iterkeys()):
            print h

    # list the clouds
    def quads_list_clouds(self):
        # list just the clouds
        for c in sorted(self.data['clouds'].iterkeys()):
            print c

    # list the owners
    def quads_list_owners(self, cloudonly):
        # list the owners
        if cloudonly is not None:
            if cloudonly not in self.data['clouds']:
                return
            print self.data['clouds'][cloudonly]['owner']
            return

        for c in sorted(self.data['clouds'].iterkeys()):
            print c + " : " + self.data['clouds'][c]['owner']

        return

    # list the tickets
    def quads_list_tickets(self, cloudonly):
        # list the service request tickets
        if cloudonly is not None:
            if cloudonly not in self.data['clouds']:
                return
            if 'ticket' not in self.data['clouds'][cloudonly]:
                return
            print self.data['clouds'][cloudonly]['ticket']
            return

        for c in sorted(self.data['clouds'].iterkeys()):
            if 'ticket' in self.data['clouds'][c]:
                print c + " : " + self.data['clouds'][c]['ticket']

        return

    # remove a host
    def quads_remove_host(self, rmhost):
        # remove a specific host
        if rmhost not in self.data['hosts']:
            print rmhost + " not found"
            return
        del(self.data['hosts'][rmhost])
        self.quads_write_data()

        return

    # remove a cloud
    def quads_remove_cloud(self, rmcloud):
        # remove a cloud (only if no hosts use it)
        if rmcloud not in self.data['clouds']:
            print rmcloud + " not found"
            return
        for h in self.data['hosts']:
            if self.data['hosts'][h]["cloud"] == rmcloud:
                print rmcloud + " is default for " + h
                print "Change the default before deleting this cloud"
                return
            for s in self.data['hosts'][h]["schedule"]:
                if self.data['hosts'][h]["schedule"][s]["cloud"] == rmcloud:
                    print rmcloud + " is used in a schedule for "  + h
                    print "Delete schedule before deleting this cloud"
                    return
        del(self.data['clouds'][rmcloud])
        self.quads_write_data()

        return

    # update a host resource
    def quads_update_host(self, hostresource, hostcloud, forceupdate):
        # define or update a host resouce
        if hostcloud is None:
            print "--default-cloud is required when using --define-host"
            exit(1)
        else:
            if hostcloud not in self.data['clouds']:
                print "Unknown cloud : %s" % hostcloud
                print "Define it first using:  --define-cloud"
                exit(1)
            if hostresource in self.data['hosts'] and not forceupdate:
                print "Host \"%s\" already defined. Use --force to replace" % hostresource
                exit(1)

            if hostresource in self.data['hosts']:
                self.data["hosts"][hostresource] = { "cloud": hostcloud, "interfaces": self.data["hosts"][hostresource]["interfaces"], "schedule": self.data["hosts"][hostresource]["schedule"] }
                self.data["history"][hostresource][int(time.time())] = hostcloud
            else:
                self.data["hosts"][hostresource] = { "cloud": hostcloud, "interfaces": {}, "schedule": {}}
                self.data["history"][hostresource] = {}
                self.data["history"][hostresource][0] = hostcloud
            self.quads_write_data()

        return

    # update a cloud resource
    def quads_update_cloud(self, cloudresource, description, forceupdate, cloudowner, cloudticket):
        # define or update a cloud resource
        if description is None:
            print "--description is required when using --define-cloud"
            exit(1)
        else:
            if cloudresource in self.data['clouds'] and not forceupdate:
                print "Cloud \"%s\" already defined. Use --force to replace" % cloudresource
                exit(1)
            if not cloudowner:
                cloudowner = "nobody"
            if not cloudticket:
                cloudticket = "00000"
            self.data["clouds"][cloudresource] = { "description": description, "networks": {}, "owner": cloudowner, "ticket": cloudticket}
            self.quads_write_data()

        return

    # define a schedule for a given host
    def quads_add_host_schedule(self, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
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

        if schedcloud not in self.data['clouds']:
            print "cloud \"" + schedcloud + "\" is not defined."
            exit(1)

        if host not in self.data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        # before updating the schedule (adding the new override), we need to
        # ensure the host does not have existing schedules that overlap the new
        # schedule being requested

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in self.data['hosts'][host]["schedule"]:
            s_start     = self.data['hosts'][host]["schedule"][s]["start"]
            s_end       = self.data['hosts'][host]["schedule"][s]["end"]
            s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
            s_end_obj   = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

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

        self.data['hosts'][host]["schedule"][len(self.data['hosts'][host]["schedule"].keys())] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
        self.quads_write_data()

        return data

    # remove a scheduled override for a given host
    def quads_rm_host_schedule(self, rmschedule, host):
        # remove a scheduled override for a given host
        if host is None:
            print "Missing --host option required for --rm-schedule"
            exit(1)

        if host not in self.data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        if rmschedule not in self.data['hosts'][host]["schedule"].keys():
            print "Could not find schedule for host"
            exit(1)

        del(self.data['hosts'][host]["schedule"][rmschedule])
        self.quads_write_data()

        return

    # modify an existing schedule
    def quads_mod_host_schedule(self, modschedule, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
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
            if schedcloud not in self.data['clouds']:
                print "cloud \"" + schedcloud + "\" is not defined."
                exit(1)

        if host not in self.data['hosts']:
            print "host \"" + host + "\" is not defined."
            exit(1)

        if modschedule not in self.data['hosts'][host]["schedule"].keys():
            print "Could not find schedule for host"
            exit(1)

        # before updating the schedule (modifying the new override), we need to
        # ensure the host does not have existing schedules that overlap the 
        # schedule being updated


        if not schedcloud:
            schedcloud = self.data['hosts'][host]["schedule"][modschedule]["cloud"]

        if not schedstart:
            schedstart = self.data['hosts'][host]["schedule"][modschedule]["start"]

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')

        if not schedend:
            schedend = self.data['hosts'][host]["schedule"][modschedule]["end"]

        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in self.data['hosts'][host]["schedule"]:
            if s != modschedule:
                s_start = self.data['hosts'][host]["schedule"][s]["start"]
                s_end   = self.data['hosts'][host]["schedule"][s]["end"]
                s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
                s_end_obj   = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

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

        self.data['hosts'][host]["schedule"][modschedule]["start"] = schedstart
        self.data['hosts'][host]["schedule"][modschedule]["end"] = schedend
        self.data['hosts'][host]["schedule"][modschedule]["cloud"] = schedcloud

        self.quads_write_data()

        return

    # as needed move host(s) based on defined schedules
    def quads_move_hosts(self, movecommand, dryrun, statedir, datearg):
        # move a host
        for h in sorted(self.data['hosts'].iterkeys()):
            default_cloud, current_cloud, current_override = self._quads_find_current(h, datearg)
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

    # generally the last thing that happens is reporting results
    def quads_print_result(self, host, cloudonly, datearg, summaryreport, fullsummaryreport, lsschedule):
        # If we're here, we're done with all other options and just need to
        # print either summary, full report if no host is specified
        if host is None:
            summary = {}

            for cloud in sorted(self.data['clouds'].iterkeys()):
                summary[cloud] = []

            for h in sorted(self.data['hosts'].iterkeys()):
                default_cloud, current_cloud, current_override = self._quads_find_current(h, datearg)
                summary[current_cloud].append(h)

            if summaryreport or fullsummaryreport:
                if fullsummaryreport:
                    for cloud in sorted(self.data['clouds'].iterkeys()):
                        print cloud + " : " + str(len(summary[cloud])) + " (" + self.data["clouds"][cloud]["description"] + ")"
                else:
                    for cloud in sorted(self.data['clouds'].iterkeys()):
                        if len(summary[cloud]) > 0:
                            print cloud + " : " + str(len(summary[cloud])) + " (" + self.data["clouds"][cloud]["description"] + ")"
            else:
                for cloud in sorted(self.data['clouds'].iterkeys()):
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
            default_cloud, current_cloud, current_override = self._quads_find_current(host, datearg)

            if lsschedule:
                print "Default cloud: " + str(default_cloud)
                print "Current cloud: " + str(current_cloud)
                if current_override is not None:
                    print "Current schedule: " + str(current_override)
                print "Defined schedules:"
                if host in self.data['hosts'].keys():
                    for override in self.data['hosts'][host]["schedule"]:
                        print "  " + str(override) + "| start=" + self.data['hosts'][host]["schedule"][override]["start"] + ",end=" + self.data['hosts'][host]["schedule"][override]["end"] + ",cloud=" + self.data['hosts'][host]["schedule"][override]["cloud"]
            else:
                print current_cloud



# used to load the configuration for quads behavior
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

def main(argv):
    quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads_config = quads_load_config(quads_config_file)

    if "data_dir" not in quads_config:
        print "quads: Missing \"data_dir\" in " + quads_config_file
        exit(1)

    defaultconfig = quads_config["data_dir"] + "/schedule.yaml"
    defaultstatedir = quads_config["data_dir"] + "/state"
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

    # Note: defaults are read in from /path/to/bin/../conf/quads.yml
    #       Which at a minimum needs to be a valid yaml config file, and
    #       also include a definition for "data_dir" where data will be stored.
    #
    # instanciate the quads object.  The required arguments are:
    #   config - This is the yaml data where hosts, clouds and schedules are defined.
    #            passed as a filename. Calculated above from args and config.
    #            Default value:  data_dir/schedule.yaml
    #            Override using:  --config </path/to/file>
    #
    #   statedir - Where the state of each host will be kept.
    #            Default value: data_dir/state/
    #            Override using:  --statedir
    #
    #   movecommand - The external program that handles that actual moving of hosts
    #            Default value: /bin/echo
    #            Override using:  --move-command </path/to/program>
    #            Takes 3 arguments, hostname, old_cloud, new_cloud
    #
    #   datearg - some queries allow looking at other dates.
    #            Format is "YYYY-MM-DD hh:mm".  Needs to be passed in quotes,
    #            e.g. --date "2017-01-01 05:00"
    #
    #   syncstate - whether or not to sync the state data.  Generally not needed
    #            unless you want to manually override.  When a host is defined,
    #            the state data is created and defaults to the current cloud.
    #            Using --sync forces the creation of the state file for defined hosts.
    #            Default value: False
    #            Override using:  --sync (no additional arg)
    #
    #   initialize - wipe and re-initialize the schedule data. Needed if the
    #            data file doesn't exist.  Useful in testing quads if no data
    #            exists.
    #            Default value: False
    #            Override using:  --init
    #            (Requires --force if data already exists and you want to wipe)
    #
    #   force -  Some operations require --force.  E.g. if you want to redefine
    #            a cloud environment.
    
    quads = Quads(args.config, args.statedir, args.movecommand, args.datearg,
                  args.syncstate, args.initialize, args.force)

    # should these be mutually exclusive?
    if args.lshosts:
        quads.quads_list_hosts()
        exit(0)

    if args.lsclouds:
        quads.quads_list_clouds()
        exit(0)

    if args.lsowner:
        quads.quads_list_owners(args.cloudonly)
        exit(0)

    if args.lsticket:
        quads.quads_list_tickets(args.cloudonly)
        exit(0)

    if args.rmhost and args.rmcloud:
        print "--rm-host and --rm-cloud are mutually exclusive"
        exit(1)

    if args.rmhost:
        quads.quads_remove_host(args.rmhost)
        exit(0)

    if args.rmcloud:
        quads.quads_remove_cloud(args.rmcloud)
        exit(0)

    if args.hostresource is not None and args.cloudresource is not None:
        print "--define-cloud and --define-host are mutually exclusive."
        exit(1)

    if args.hostresource:
        quads.quads_update_host(args.hostresource, args.hostcloud, args.force)
        exit(0)

    if args.cloudresource:
        quads.quads_update_cloud(args.cloudresource, args.description, args.force, args.cloudowner, args.cloudticket)
        exit(0)

    if (args.addschedule and args.rmschedule) or (args.addschedule and args.modschedule) or (args.rmschedule and args.modschedule):
        print "Online one of the following is allowed:"
        print "    --add-schedule"
        print "    --rm-schedule"
        print "    --mod-schedule"
        exit(1)

    if args.addschedule:
        if args.schedstart is None or args.schedend is None or args.schedcloud is None or args.host is None:
            print "Missing option. All these options are required for --add-schedule:"
            print "    --host"
            print "    --schedule-start"
            print "    --schedule-end"
            print "    --schedule-cloud"
            exit(1)
        quads.quads_add_host_schedule(args.schedstart, args.schedend, args.schedcloud, args.host)
        exit(0)

    if args.rmschedule is not None:
        quads.quads_rm_host_schedule(args.rmschedule, args.host)
        exit(0)

    if args.modschedule is not None:
        if args.host is None:
            print "Missing option. Need --host when using --mod-schedule"
            exit(1)

        if args.schedstart is None and args.schedend is None and args.schedcloud is None:
            print "Missing option. At least one these options are required for --mod-schedule:"
            print "    --schedule-start"
            print "    --schedule-end"
            print "    --schedule-cloud"
            exit(1)

        quads.quads_mod_host_schedule(args.modschedule, args.schedstart, args.schedend, args.schedcloud, args.host)
        exit(0)

    if args.movehosts:
        if args.datearg is not None and not args.dryrun:
            print "--move-hosts and --date are mutually exclusive unless using --dry-run."
            exit(1)
        quads.quads_move_hosts(args.movecommand, args.dryrun, args.statedir, args.datearg)
        exit(0)

    # finally, this part is just reporting ...
    quads.quads_print_result(args.host, args.cloudonly, args.datearg, args.summary, args.fullsummary, args.lsschedule)

    exit(0)

if __name__ == "__main__":
       main(sys.argv[1:])
