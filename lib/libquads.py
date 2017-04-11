from datetime import datetime
import time
import yaml
import os
import requests
import logging
import sys
import importlib
from subprocess import check_call
from hardware_services.inventory_service import get_inventory_service, set_inventory_service
from hardware_services.network_service import get_network_service, set_network_service
sys.path.append(os.path.dirname(__file__) + "/hardware_services/inventory_drivers/")
sys.path.append(os.path.dirname(__file__) + "/hardware_services/network_drivers/")


class Hosts(object):
    def __init__(self, data):
        """
        Initialize a Hosts object. This is a subset of
        data required by the Quads object.
        """
        self.logger = logging.getLogger("quads.Hosts")
        self.logger.setLevel(logging.DEBUG)
        if 'hosts' not in data:
            self.logger.error("data missing required \"hosts\" section.")
            exit(1)

        self.data = data["hosts"]

    # list the hosts
    def host_list(self):
        # list just the hostnames
        for h in sorted(self.data.iterkeys()):
            print h

class Clouds(object):
    def __init__(self, data):
        """
        Initialize a Clouds object. This is a subset of
        data required by the Quads object.
        """
        self.logger = logging.getLogger("quads.Clouds")
        self.logger.setLevel(logging.DEBUG)
        if 'clouds' not in data:
            self.logger.error("data missing required \"clouds\" section.")
            exit(1)

        self.data = data["clouds"]

   # list the clouds
    def cloud_list(self):
        # list just the clouds
        for c in sorted(self.data.iterkeys()):
            print c

class History(object):
    def __init__(self, data):
        """
        Initialize a History object. This is a subset of
        data required by the Quads object. (used for host
        history tracking)
        """
        if 'history' not in data:
            self.data = {}
        else:
            self.data = data["history"]

class QuadsData(object):
    def __init__(self, data):
        """
        Initialize the QuadsData object.
        """
        self.hosts = Hosts(data)
        self.clouds = Clouds(data)
        self.history = History(data)


class Quads(object):

    def __init__(self, config, statedir, movecommand, datearg, syncstate, initialize, force, hardwareservice):
        """
        Initialize a quads object.
        """
        self.config = config
        self.statedir = statedir
        self.movecommand = movecommand
        self.datearg = datearg
        self.logger = logging.getLogger("quads.Quads")
        self.logger.setLevel(logging.DEBUG)

        #EC528 addition - dynamically import driver module and set inventory and network services
        inventoryservice = hardwareservice + "InventoryDriver"
        networkservice = hardwareservice + "NetworkDriver"

        importlib.import_module(inventoryservice)
        importlib.import_module(networkservice)

        set_inventory_service(getattr(sys.modules[inventoryservice], inventoryservice)())
        set_network_service(getattr(sys.modules[networkservice], networkservice)())

        self.inventory_service = get_inventory_service()
        self.network_service = get_network_service()

        if initialize:
            self.quads_init_data(force)
        try:
            stream = open(config, 'r')
            self.data = yaml.load(stream)
            stream.close()
        except Exception, ex:
            self.logger.error(ex)
            exit(1)

        self.quads = QuadsData(self.data)
        self._quads_history_init()

        if syncstate or not datearg:
            self.quads_sync_state()

    # initialize history
    def _quads_history_init(self):
        updateyaml = False

        for h in sorted(self.quads.hosts.data.iterkeys()):
            if h not in self.quads.history.data:
                self.quads.history.data[h] = {}
                default_cloud, current_cloud, current_override = self._quads_find_current(h, None)
                self.quads.history.data[h][0] = current_cloud
                updateyaml = True

        if updateyaml:
            self.quads_write_data(False)

    # we occasionally need to write the data back out
    def quads_write_data(self, doexit = True):
        try:
            stream = open(self.config, 'w')
            self.data = {"clouds":self.quads.clouds.data, "hosts":self.quads.hosts.data, "history":self.quads.history.data}
            stream.write( yaml.dump(self.data, default_flow_style=False))
            if doexit:
                exit(0)
        except Exception, ex:
            self.logger.error("There was a problem with your file %s" % ex)
            if doexit:
                exit(1)

    # if passed --init, the config data is wiped.
    # typically we will not want to continue execution if user asks to initialize
    def quads_init_data(self, force):
        if not force:
            if os.path.isfile(self.config):
                self.logger.warn("Warning: " + self.config + " exists. Use --force to initialize.")
                exit(1)
        try:
            stream = open(self.config, 'w')
            data = {"clouds":{}, "hosts":{}, "history":{}}
            stream.write( yaml.dump(data, default_flow_style=False))
            exit(0)
        except Exception, ex:
            self.logger.error("There was a problem with your file %s" % ex)
            exit(1)

    # helper function called from other methods.  Never called from main()
    def _quads_find_current(self, host, datearg):
        hosts = self.quads.hosts.data
        history = self.quads.history.data

        if host in hosts.keys():
            default_cloud = hosts[host]["cloud"]
            current_cloud = default_cloud
            current_override = None
            current_time = datetime.now()

            if datearg is None:
                requested_time = current_time
            else:
                try:
                    requested_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')
                except Exception, ex:
                    self.logger.error("Data format error : %s" % ex)
                    exit(1)

            if "schedule" in hosts[host].keys():
                for override in hosts[host]["schedule"]:
                    start_obj = datetime.strptime(hosts[host]["schedule"][override]["start"], '%Y-%m-%d %H:%M')
                    end_obj = datetime.strptime(hosts[host]["schedule"][override]["end"], '%Y-%m-%d %H:%M')

                    if start_obj <= requested_time and requested_time < end_obj:
                        current_cloud = hosts[host]["schedule"][override]["cloud"]
                        current_override = override
                        return default_cloud, current_cloud, current_override

            # only consider history data when looking at past data
            if requested_time < current_time:
                for h in sorted(history[host]):
                    if datetime.fromtimestamp(h) <= requested_time:
                        current_cloud = history[host][h]

            return default_cloud, current_cloud, current_override

        else:
            return None, None, None

    # sync the statedir db for hosts with schedule
    def quads_sync_state(self):
        # sync state
        if self.datearg is not None:
            self.logger.error("--sync and --date are mutually exclusive.")
            exit(1)
        for h in sorted(self.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = self._quads_find_current(h, self.datearg)
            if not os.path.isfile(self.statedir + "/" + h):
                try:
                    stream = open(self.statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
        return

    # list the hosts
    def quads_list_hosts(self):
        # list just the hostnames
        self.inventory_service.list_hosts(self)

    # list the hosts
    def quads_list_clouds(self):
        # list just the hostnames
        self.inventory_service.list_clouds(self)

    # list the owners
    def quads_list_owners(self, cloudonly):
        # list the owners
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            print self.quads.clouds.data[cloudonly]['owner']
            return

        for c in sorted(self.quads.clouds.data.iterkeys()):
            print c + " : " + self.quads.clouds.data[c]['owner']

        return

    # list the cc users
    def quads_list_cc(self, cloudonly):
        # list the cc users
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            if 'ccusers' not in self.quads.clouds.data[cloudonly]:
                return
            for u in self.quads.clouds.data[cloudonly]['ccusers']:
                print u
        else:
            for c in sorted(self.quads.clouds.data.iterkeys()):
                if 'ccusers' in self.quads.clouds.data[c]:
                    print c + " : " + " ".join(self.quads.clouds.data[c]['ccusers'])
        return

    # list the tickets
    def quads_list_tickets(self, cloudonly):
        # list the service request tickets
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            if 'ticket' not in self.quads.clouds.data[cloudonly]:
                return
            print self.quads.clouds.data[cloudonly]['ticket']
            return

        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'ticket' in self.quads.clouds.data[c]:
                print c + " : " + self.quads.clouds.data[c]['ticket']

        return

    # list qinq status
    def quads_list_qinq(self, cloudonly):
        # list the environment qinq state
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            if 'qinq' not in self.quads.clouds.data[cloudonly]:
                return
            print self.quads.clouds.data[cloudonly]['qinq']
            return

        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'qinq' in self.quads.clouds.data[c]:
                print c + " : " + self.quads.clouds.data[c]['qinq']

        return

    # remove a host
    def quads_remove_host(self, rmhost):
        # remove a specific host

        kwargs = {'rmhost': rmhost}

        self.inventory_service.remove_host(self, **kwargs)

        return

    # remove a cloud
    def quads_remove_cloud(self, rmcloud):
        # remove a cloud (only if no hosts use it)

        kwargs = {'rmcloud': rmcloud}

        self.inventory_service.remove_cloud(self, **kwargs)

        return

    # update a host resource
    def quads_update_host(self, hostresource, hostcloud, forceupdate):
        # define or update a host resouce

        kwargs = {'hostresource': hostresource, 'hostcloud': hostcloud, 'forceupdate': forceupdate}

        self.inventory_service.update_host(self, **kwargs)

        return

    # update a cloud resource
    def quads_update_cloud(self, cloudresource, description, forceupdate, cloudowner, ccusers, cloudticket, qinq):
        # define or update a cloud resource

        kwargs = {'cloudresource': cloudresource, 'description': description, 'forceupdate': forceupdate,
                  'cloudowner': cloudowner, 'ccusers': ccusers, 'cloudticket': cloudticket, 'qinq': qinq}

        self.inventory_service.update_cloud(self, **kwargs)

        return

    # define a schedule for a given host
    def quads_add_host_schedule(self, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
        try:
            datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        except Exception, ex:
            self.logger.error("Data format error : %s" % ex)
            exit(1)

        try:
            datetime.strptime(schedend, '%Y-%m-%d %H:%M')
        except Exception, ex:
            self.logger.error("Data format error : %s" % ex)
            exit(1)

        if schedcloud not in self.quads.clouds.data:
            self.logger.error("cloud \"" + schedcloud + "\" is not defined.")
            exit(1)

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            exit(1)

        # before updating the schedule (adding the new override), we need to
        # ensure the host does not have existing schedules that overlap the new
        # schedule being requested

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in self.quads.hosts.data[host]["schedule"]:
            s_start     = self.quads.hosts.data[host]["schedule"][s]["start"]
            s_end       = self.quads.hosts.data[host]["schedule"][s]["end"]

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

        # the next available schedule index should be the max index + 1
        self.quads.hosts.data[host]["schedule"][max(self.quads.hosts.data[host]["schedule"].keys() or [-1])+1] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
        self.quads_write_data()

        return data

    # remove a scheduled override for a given host
    def quads_rm_host_schedule(self, rmschedule, host):
        # remove a scheduled override for a given host
        if host is None:
            self.logger.error("Missing --host option required for --rm-schedule")
            exit(1)

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            exit(1)

        if rmschedule not in self.quads.hosts.data[host]["schedule"].keys():
            self.logger.error("Could not find schedule for host")
            exit(1)

        del(self.quads.hosts.data[host]["schedule"][rmschedule])
        self.quads_write_data()

        return

    # modify an existing schedule
    def quads_mod_host_schedule(self, modschedule, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
        if schedstart:
            try:
                datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
            except Exception, ex:
                self.logger.error("Data format error : %s" % ex)
                exit(1)

        if schedend:
            try:
                datetime.strptime(schedend, '%Y-%m-%d %H:%M')
            except Exception, ex:
                self.logger.error("Data format error : %s" % ex)
                exit(1)

        if schedcloud:
            if schedcloud not in self.quads.clouds.data:
                self.logger.error("cloud \"" + schedcloud + "\" is not defined.")
                exit(1)

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            exit(1)

        if modschedule not in self.quads.hosts.data[host]["schedule"].keys():
            self.logger.error("Could not find schedule for host")
            exit(1)

        # before updating the schedule (modifying the new override), we need to
        # ensure the host does not have existing schedules that overlap the
        # schedule being updated


        if not schedcloud:
            schedcloud = self.quads.hosts.data[host]["schedule"][modschedule]["cloud"]

        if not schedstart:
            schedstart = self.quads.hosts.data[host]["schedule"][modschedule]["start"]

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')

        if not schedend:
            schedend = self.quads.hosts.data[host]["schedule"][modschedule]["end"]

        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        for s in self.quads.hosts.data[host]["schedule"]:
            if s != modschedule:
                s_start = self.quads.hosts.data[host]["schedule"][s]["start"]
                s_end   = self.quads.hosts.data[host]["schedule"][s]["end"]

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

        self.quads.hosts.data[host]["schedule"][modschedule]["start"] = schedstart
        self.quads.hosts.data[host]["schedule"][modschedule]["end"] = schedend
        self.quads.hosts.data[host]["schedule"][modschedule]["cloud"] = schedcloud

        self.quads_write_data()

        return

    # as needed move host(s) based on defined schedules
    def quads_move_hosts(self, movecommand, dryrun, statedir, datearg):
        # move a host

        kwargs = {'movecommand': movecommand, 'dryrun': dryrun, 'statedir': statedir,
                  'datearg': datearg}

        self.network_service.move_hosts(self, **kwargs)

        exit(0)

    # generally the last thing that happens is reporting results
    def quads_print_result(self, host, cloudonly, datearg, summaryreport, fullsummaryreport, lsschedule):
        # If we're here, we're done with all other options and just need to
        # print either summary, full report if no host is specified
        if host is None:
            summary = {}

            for cloud in sorted(self.quads.clouds.data.iterkeys()):
                summary[cloud] = []

            for h in sorted(self.quads.hosts.data.iterkeys()):
                default_cloud, current_cloud, current_override = self._quads_find_current(h, datearg)
                summary[current_cloud].append(h)

            if summaryreport or fullsummaryreport:
                if fullsummaryreport:
                    for cloud in sorted(self.quads.clouds.data.iterkeys()):
                        print cloud + " : " + str(len(summary[cloud])) + " (" + self.quads.clouds.data[cloud]["description"] + ")"
                else:
                    for cloud in sorted(self.quads.clouds.data.iterkeys()):
                        if len(summary[cloud]) > 0:
                            print cloud + " : " + str(len(summary[cloud])) + " (" + self.quads.clouds.data[cloud]["description"] + ")"
            else:
                for cloud in sorted(self.quads.clouds.data.iterkeys()):
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
                if host in self.quads.hosts.data.keys():
                    for override in self.quads.hosts.data[host]["schedule"]:
                        print "  " + str(override) + "| start=" + self.quads.hosts.data[host]["schedule"][override]["start"] + \
                            ",end=" + self.quads.hosts.data[host]["schedule"][override]["end"] + \
                            ",cloud=" + self.quads.hosts.data[host]["schedule"][override]["cloud"]
            else:
                print current_cloud


    # add for EC528 HIL-QUADS integration project
    def quads_rest_call(self, method, url, request, json_data=None):
        r = requests.request(method, url + request, data=json_data)
        if method == 'GET':
            return r


