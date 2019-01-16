#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import sys

from quads.helpers import quads_load_config
from quads.quads import Quads

logger = logging.getLogger('quads')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def print_hosts(quads):
    for host in quads.get_hosts():
        print(host)


def print_clouds(quads):
    for cloud in quads.get_clouds():
        print(cloud)


def get_owners(quads, cloudonly):
    _owners = []
    for item in quads.get_owners(cloudonly):
        for cloud, owner in item.items():
            _owners.append("{}: {}".format(cloud, owner))
    return _owners


def print_owners(quads, cloudonly):
    for item in get_owners(quads, cloudonly):
        print(item)


def get_cc(quads, cloud_only):
    _cc = []
    for item in quads.get_cc(cloud_only):
        for cloud, cc_list in item.items():
            if cc_list is not None:
                _cc.append("{}: {}".format(cloud, ''.join(cc_list)))
            else:
                _cc.append(cloud)
    return _cc


def print_cc(quads, cloud_only):
    for item in get_cc(quads, cloud_only):
        print(item)


def get_tickets(quads, cloudonly):
    _tickets = []
    for item in quads.get_tickets(cloudonly):
        for cloud, ticket in item.items():
            _tickets.append("{}: {}".format(cloud, ticket))
    return _tickets


def print_tickets(quads, cloudonly):
    for item in get_tickets(quads, cloudonly):
        print(item)


def print_qinq(quads, cloudonly):
    for item in quads.get_qinq(cloudonly):
        for cloud, qinq in item.items():
            print("{}: {}".format(cloud, qinq))


def print_host_cloud(quads, host, datearg):
    print(quads.query_host_cloud(host, datearg))


def get_cloud_hosts(quads, datearg, cloudonly):
    hosts = []
    cloud_hosts = quads.query_cloud_hosts(datearg)
    if cloudonly is not None:
        if cloudonly in cloud_hosts:
            for host in cloud_hosts[cloudonly]:
                hosts.append(host)
        else:
            print("Requested cloud does not exist")
    else:
        for cloud, hostlist in sorted(cloud_hosts.items()):
            hosts.append("{}:".format(cloud))
            for host in hostlist:
                hosts.append(" - {}".format(host))
    return hosts


def print_cloud_hosts(quads, datearg, cloudonly):
    cloud_hosts = get_cloud_hosts(quads, datearg, cloudonly)
    for host in cloud_hosts:
        print(host)


def print_host_schedule(quads, host, datearg):
    default_cloud, current_cloud, current_schedule, full_schedule = quads.query_host_schedule(host, datearg)
    print("Default cloud: {}".format(default_cloud))
    print("Current cloud: {}".format(current_cloud))
    if current_schedule is not None:
        print("Current schedule: {}".format(current_schedule))
    if len(full_schedule) > 0:
        print("Defined schedules:")
        for item in full_schedule:
            for override, schedule in item.items():
                sys.stdout.write("  {}| ".format(override))
                for schedkey, schedval in schedule.items():
                    if schedkey == 'start' or schedkey == 'end':
                        sys.stdout.write("{}={},".format(schedkey, schedval))
                    else:
                        print("{}={}".format(schedkey, schedval))


def get_cloud_summary(quads, datearg, activesummary):
    _cloud_summary = quads.query_cloud_summary(datearg, activesummary)
    _lines = []
    if len(_cloud_summary) > 0:
        for item in _cloud_summary:
            for cloudname, details in item.items():
                hosts_count = "0"
                description = ""
                for param, value in details.items():
                    if param == 'hosts':
                        hosts_count = value
                    elif param == 'description':
                        description = value
                line = "%s : %s (%s)\n" % (cloudname, hosts_count, description)
                _lines.append(line)
    return _lines


def print_cloud_summary(quads, datearg, activesummary):
    _cloud_summary = get_cloud_summary(quads, datearg, activesummary)
    for line in _cloud_summary:
        print(line)


def print_cloud_postconfig(quads, datearg, activesummary, postconfig):
    clouds = quads.query_cloud_postconfig(datearg, activesummary, postconfig)
    for cloud in clouds:
        print(cloud)


def main(argv=None):
    quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads_config = quads_load_config(quads_config_file)

    if "data_dir" not in quads_config:
        print("quads: Missing \"data_dir\" in " + quads_config_file)
        exit(1)

    if "install_dir" not in quads_config:
        print("quads: Missing \"install_dir\" in " + quads_config_file)
        exit(1)

    sys.path.append(quads_config["install_dir"] + "/lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib")

    defaultconfig = quads_config["data_dir"] + "/schedule.yaml"
    defaultstatedir = quads_config["data_dir"] + "/state"
    defaultmovecommand = "/bin/echo"

    parser = argparse.ArgumentParser(description='Query current cloud for a given host')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ls-owner', dest='lsowner', action='store_true', default=None, help='List owners')
    group.add_argument('--ls-cc-users', dest='lsccusers', action='store_true', default=None, help='List CC list')
    group.add_argument('--ls-ticket', dest='lsticket', action='store_true', default=None, help='List request ticket')
    group.add_argument('--ls-qinq', dest='lsqinq', action='store_true', default=None, help='List cloud qinq state')
    group.add_argument('--define-host', dest='hostresource', type=str, default=None, help='Define a host resource')
    group.add_argument('--define-cloud', dest='cloudresource', type=str, default=None,
                       help='Define a cloud environment')
    group.add_argument('--add-schedule', dest='addschedule', action='store_true', help='Define a host reservation')
    group.add_argument('--mod-schedule', dest='modschedule', type=int, default=None, help='Modify a host reservation')
    group.add_argument('--rm-schedule', dest='rmschedule', type=int, default=None, help='Remove a host reservation')
    group.add_argument('--ls-hosts', dest='lshosts', action='store_true', default=None, help='List all hosts')
    group.add_argument('--ls-clouds', dest='lsclouds', action='store_true', default=None, help='List all clouds')
    group.add_argument('--rm-host', dest='rmhost', type=str, default=None, help='Remove a host')
    group.add_argument('--rm-cloud', dest='rmcloud', type=str, default=None, help='Remove a cloud')
    group.add_argument('--summary', dest='summary', action='store_true', help='Generate a summary report')
    group.add_argument('--full-summary', dest='fullsummary', action='store_true', help='Generate a summary report')
    parser.add_argument('--host', dest='host', type=str, default=None, help='Specify the host to query')
    parser.add_argument('--cloud-only', dest='cloudonly', type=str, default=None,
                        help='Limit full report to hosts only in this cloud')
    parser.add_argument('-c', '--config', dest='config', help='YAML file with cluster data', default=defaultconfig,
                        type=str)
    parser.add_argument('-d', '--datetime', dest='datearg', type=str, default=None,
                        help='date and time to query; e.g. "2016-06-01 08:00"')
    parser.add_argument('-i', '--init', dest='initialize', action='store_true',
                        help='initialize the schedule YAML file')
    parser.add_argument('--cloud-owner', dest='cloudowner', type=str, default=None, help='Define environment owner')
    parser.add_argument('--cc-users', dest='ccusers', type=str, default=None, help='Define environment CC list')
    parser.add_argument('--qinq', dest='qinq', type=str, default=None, help='Define environment qinq state')
    parser.add_argument('--cloud-ticket', dest='cloudticket', type=str, default=None, help='Define environment ticket')
    parser.add_argument('--description', dest='description', type=str, default=None,
                        help='Defined description of cloud')
    parser.add_argument('--default-cloud', dest='hostcloud', type=str, default=None,
                        help='Defined default cloud for a host')
    parser.add_argument('--force', dest='force', action='store_true',
                        help='Force host or cloud update when already defined')
    parser.add_argument('--schedule-query', dest='schedquery', action='store_true',
                        help='Query the schedule for a specific month')
    parser.add_argument('--month', dest='month', type=str, default=datetime.datetime.now().month,
                        help='Query the schedule for a specific month and year')
    parser.add_argument('--year', dest='year', type=str, default=datetime.datetime.now().year,
                        help='Query the schedule for a specific month and year')
    parser.add_argument('--schedule-start', dest='schedstart', type=str, default=None, help='Schedule start date/time')
    parser.add_argument('--schedule-end', dest='schedend', type=str, default=None, help='Schedule end date/time')
    parser.add_argument('--schedule-cloud', dest='schedcloud', type=str, default=None, help='Schedule cloud')
    parser.add_argument('--ls-schedule', dest='lsschedule', action='store_true', help='List the host reservations')
    parser.add_argument('--statedir', dest='statedir', type=str, default=defaultstatedir, help='Default state dir')
    parser.add_argument('--sync', dest='syncstate', action='store_true', default=None, help='Sync state of hosts')
    parser.add_argument('--move-hosts', dest='movehosts', action='store_true', default=None,
                        help='Move hosts if schedule has changed')
    parser.add_argument('--move-command', dest='movecommand', type=str, default=defaultmovecommand,
                        help='External command to move a host')
    parser.add_argument('--dry-run', dest='dryrun', action='store_true', default=None,
                        help='Dont update state when used with --move-hosts')
    parser.add_argument('--log-path', dest='logpath', type=str, default=None, help='Path to quads log file')
    parser.add_argument('--post-config', dest='postconfig', type=str, default=None, nargs='*', choices=['openstack'],
                        help='Post provisioning configuration to apply')
    parser.add_argument('--version', dest='version', type=str, default=None, help='Version of Software to apply')
    parser.add_argument('--puddle', dest='puddle', type=str, default='latest', help='Puddle to apply')
    parser.add_argument('--os-control-scale', dest='controlscale', type=int, default=None,
                        help='Number of controller nodes for OpenStack deployment')
    parser.add_argument('--os-compute-scale', dest='computescale', type=int, default=None,
                        help='Number of compute nodes for OpenStack deployment')
    parser.add_argument('--host-type', dest='hosttype', type=str, default=None,
                        help='Model/Make/Type of host DellR620  for example')

    args = parser.parse_args(argv)
    if args.logpath:
        quads_config["log"] = args.logpath

    if not os.path.exists(quads_config["log"]):
        try:
            open(quads_config["log"], 'a').close()
        except IOError:
            logger.error("Log file does not exist : {}".format(quads_config["log"]))
            exit(1)

    fh = logging.FileHandler(quads_config["log"])
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    if not os.path.exists(args.statedir):
        try:
            os.makedirs(args.statedir)
        except Exception as ex:
            print(ex)
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
    if args.lshosts:
        print_hosts(quads)
        exit(0)

    if args.lsclouds:
        print_clouds(quads)
        exit(0)

    if args.lsowner:
        print_owners(quads, args.cloudonly)
        exit(0)

    if args.lsccusers:
        print_cc(quads, args.cloudonly)
        exit(0)

    if args.lsticket:
        print_tickets(quads, args.cloudonly)
        exit(0)

    if args.lsqinq:
        print_qinq(quads, args.cloudonly)
        exit(0)

    if args.rmhost:
        quads.remove_host(args.rmhost)
        exit(0)

    if args.rmcloud:
        quads.remove_cloud(args.rmcloud)
        exit(0)

    if args.hostresource:
        result = quads.update_host(args.hostresource, args.hostcloud,
                                   args.hosttype, args.force)
        for r in result:
            print(r)
        if len(result) == 0:
            exit(1)
        if result[0] != "OK":
            for r in result:
                logger.error(r)
            exit(1)
        exit(0)

    if args.cloudresource:
        result = quads.update_cloud(args.cloudresource, args.description,
                                    args.force, args.cloudowner, args.ccusers,
                                    args.cloudticket, args.qinq,
                                    args.postconfig, args.version, args.puddle,
                                    args.controlscale, args.computescale)
        for r in result:
            print(r)
        if len(result) == 0:
            exit(1)
        if result[0] != "OK":
            for r in result:
                logger.error(r)
            exit(1)
        exit(0)

    if args.schedquery:
        schedule = quads.hosts_schedule_query(month=args.month, year=args.year)

        print("Host Schedule for {}/{}".format(args.year, args.schedquery))
        print("Note: This is a per-day view. Every entry is a day in a given month.")
        print("      This only shows the cloud number per entry")
        for host in sorted(schedule.keys()):
            _daily = ""
            for day in schedule[host][args.year][args.month]:
                _daily = "{} {}".format(_daily, schedule[host][args.year][args.month][day][1].strip('cloud'))
            print("{}\t {}".format(host.split('.')[0], _daily))
        exit(0)

    if args.addschedule:
        if args.schedstart is None or args.schedend is None or args.schedcloud is None or args.host is None:
            print("Missing option. All these options are required for --add-schedule:")
            print("    --host")
            print("    --schedule-start")
            print("    --schedule-end")
            print("    --schedule-cloud")
            exit(1)
        result = quads.add_host_schedule(args.schedstart, args.schedend, args.schedcloud, args.host)
        for r in result:
            print(r)
        if len(result) == 0:
            exit(1)
        if result[0] != "OK":
            for r in result:
                logger.error(r)
            exit(1)
        exit(0)
    if args.rmschedule is not None:
        result = quads.rm_host_schedule(args.rmschedule, args.host)
        for r in result:
            print(r)
        if len(result) == 0:
            exit(1)
        if result[0] != "OK":
            for r in result:
                logger.error(r)
            exit(1)
        exit(0)

    if args.modschedule is not None:
        if args.host is None:
            print("Missing option. Need --host when using --mod-schedule")
            exit(1)

        if args.schedstart is None and args.schedend is None and args.schedcloud is None:
            print("Missing option. At least one these options are required for --mod-schedule:")
            print("    --schedule-start")
            print("    --schedule-end")
            print("    --schedule-cloud")
            exit(1)
        result = quads.mod_host_schedule(args.modschedule, args.schedstart, args.schedend, args.schedcloud, args.host)
        for r in result:
            print(r)
        if len(result) == 0:
            exit(1)
        if result[0] != "OK":
            for r in result:
                logger.error(r)
            exit(1)
        exit(0)

    if args.movehosts:
        if args.datearg is not None and not args.dryrun:
            print("--move-hosts and --date are mutually exclusive unless using --dry-run.")
            exit(1)
        quads.move_hosts(args.movecommand, args.dryrun, args.statedir, args.datearg)
        exit(0)

    if args.host:
        if args.lsschedule:
            print_host_schedule(quads, args.host, args.datearg)
        else:
            print_host_cloud(quads, args.host, args.datearg)
        exit(0)

    if args.postconfig:
        print_cloud_postconfig(quads, args.datearg, args.summary, args.postconfig)
        exit(0)

    if args.summary or args.fullsummary:
        print_cloud_summary(quads, args.datearg, args.summary)
        exit(0)

    print_cloud_hosts(quads, args.datearg, args.cloudonly)
    exit(0)


if __name__ == "__main__":
    main()
