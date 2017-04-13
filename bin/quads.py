#!/bin/python

from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
import logging
from subprocess import call
from subprocess import check_call

sys.path.append(os.path.dirname(__file__) + "/../")
#from lib.hardware_services.hardware_service import set_hardware_service


logger = logging.getLogger('quads')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

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

    if "install_dir" not in quads_config:
        print "quads: Missing \"install_dir\" in " + quads_config_file
        exit(1)


    if "hardware_service" not in quads_config:
        print "quads: Missing \"hardware_service\" in " + quads_config_file
        exit(1)

    sys.path.append(quads_config["install_dir"] + "/lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib/hardware_services/hardware_drivers/")
    import libquads

    defaultconfig = quads_config["data_dir"] + "/schedule.yaml"
    defaultstatedir = quads_config["data_dir"] + "/state"
    defaultmovecommand = "/bin/echo"

    # EC528 addition - sets hardware service
    defaulthardwareservice = quads_config["hardware_service"]


    parser = argparse.ArgumentParser(description='Query current cloud for a given host')
    parser.add_argument('--host', dest='host', type=str, default=None, help='Specify the host to query')
    parser.add_argument('--cloud-only', dest='cloudonly', type=str, default=None, help='Limit full report to hosts only in this cloud')
    parser.add_argument('-c', '--config', dest='config',
                                            help='YAML file with cluster data',
                                            default=defaultconfig, type=str)
    parser.add_argument('-d', '--datetime', dest='datearg', type=str, default=None, help='date and time to query; e.g. "2016-06-01 08:00"')
    parser.add_argument('-i', '--init', dest='initialize', action='store_true', help='initialize the schedule YAML file')
    parser.add_argument('--ls-owner', dest='lsowner', action='store_true', default=None, help='List owners')
    parser.add_argument('--ls-cc-users', dest='lsccusers', action='store_true', default=None, help='List CC list')
    parser.add_argument('--ls-ticket', dest='lsticket', action='store_true', default=None, help='List request ticket')
    parser.add_argument('--ls-qinq', dest='lsqinq', action='store_true', default=None, help='List cloud qinq state')
    parser.add_argument('--cloud-owner', dest='cloudowner', type=str, default=None, help='Define environment owner')
    parser.add_argument('--cc-users', dest='ccusers', type=str, default=None, help='Define environment CC list')
    parser.add_argument('--qinq', dest='qinq', type=str, default=None, help='Define environment qinq state')
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
    parser.add_argument('--schedule-query', dest='schedquery', action='store_true', help='Query the schedule for a specific month')
    parser.add_argument('--month', dest='month', type=str, default=datetime.now().month, help='Query the schedule for a specific month and year')
    parser.add_argument('--year', dest='year', type=str, default=datetime.now().year, help='Query the schedule for a specific month and year')
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
    parser.add_argument('--log-path', dest='logpath',type=str,default=None, help='Path to quads log file')

    parser.add_argument('--set-hardware-service', dest='hardwareservice', type=str, default=defaulthardwareservice, help='Set Hardware Serve');


    args = parser.parse_args()

    if args.logpath :
        quads_config["log"] = args.logpath

    if not os.path.exists(quads_config["log"]) :
        try :
            open(quads_config["log"],'a').close()
        except Exception:
            logger.error("Log file does not exist : {}".format(quads_config["log"]))
            exit(1)

    fh = logging.FileHandler(quads_config["log"])
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

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

    quads = libquads.Quads(args.config, args.statedir, args.movecommand, args.datearg,
                  args.syncstate, args.initialize, args.force, args.hardwareservice)

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

    if args.lsccusers:
        quads.quads_list_cc(args.cloudonly)
        exit(0)

    if args.lsticket:
        quads.quads_list_tickets(args.cloudonly)
        exit(0)

    if args.lsqinq:
        quads.quads_list_qinq(args.cloudonly)
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
        quads.quads_update_cloud(args.cloudresource, args.description, args.force, args.cloudowner, args.ccusers, args.cloudticket, args.qinq)
        exit(0)

    if (args.addschedule and args.rmschedule) or (args.addschedule and args.modschedule) or (args.rmschedule and args.modschedule):
        print "Online one of the following is allowed:"
        print "    --add-schedule"
        print "    --rm-schedule"
        print "    --mod-schedule"
        exit(1)

    if args.schedquery:
        schedule = None
        schedule = quads.quads_hosts_schedule(month=args.month,year=args.year)

        print "Host Schedule for {}/{}".format(args.schedquery,args.year)
        print "Note: This is a per-day view. Every entry is a day in a given month."
        print "      This only shows the cloud number per entry"
        for host in sorted(schedule.iterkeys()) :
            _daily=""
            for day in schedule[host][args.year][args.month]:
                _daily = "{} {}".format(_daily,schedule[host][args.year][args.month][day][1].strip('cloud'))
            print "{}\t {}".format(host.split('.')[0],_daily)
        exit(0)

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
        # if args.datearg is not None and not args.dryrun:
        #     print "--move-hosts and --date are mutually exclusive unless using --dry-run."
        #     exit(1)
        quads.quads_move_hosts(args.movecommand, args.dryrun, args.statedir, args.datearg)
        exit(0)

    # finally, this part is just reporting ...
    quads.quads_print_result(args.host, args.cloudonly, args.datearg, args.summary, args.fullsummary, args.lsschedule)

    exit(0)

if __name__ == "__main__":
       main(sys.argv[1:])
