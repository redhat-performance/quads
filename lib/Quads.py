# This file is part of QUADs.
#
# QUADs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QUADs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QUADs.  If not, see <http://www.gnu.org/licenses/>.

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
from Clouds import Clouds
from History import History
from QuadsData import QuadsData
from CloudHistory import CloudHistory

class Quads(object):
    def __init__(self, config, statedir, movecommand, datearg, syncstate, initialize, force):
        """
        Initialize a quads object.
        """
        self.config = config
        self.statedir = statedir
        self.movecommand = movecommand
        self.datearg = datearg
        self.logger = logging.getLogger("quads.Quads")
        self.logger.setLevel(logging.DEBUG)

        self.init_data(initialize, force)
        self.read_data()
        self.history_init()

        if syncstate or not datearg:
            self.sync_state()

    def get_history(self):
        return self.quads.cloud_history.data

    # initialize history
    def history_init(self):
        updateyaml = False

        for h in sorted(self.quads.hosts.data.iterkeys()):
            if h not in self.quads.history.data:
                self.quads.history.data[h] = {}
                default_cloud, current_cloud, current_override = self.find_current(h, None)
                self.quads.history.data[h][0] = current_cloud
                updateyaml = True

        for c in sorted(self.quads.clouds.data.iterkeys()):
            if c not in self.quads.cloud_history.data:
                self.quads.cloud_history.data[c] = {}
                if 'ccusers' in self.quads.clouds.data[c]:
                    savecc = []
                    for cc in self.quads.clouds.data[c]['ccusers']:
                        savecc.append(cc)
                    ccusers = savecc
                else:
                    ccusers = []
                if 'description' in self.quads.clouds.data[c]:
                    description = self.quads.clouds.data[c]['description']
                else:
                    description = ""
                if 'owner' in self.quads.clouds.data[c]:
                    owner = self.quads.clouds.data[c]['owner']
                else:
                    owner = "nobody"
                if 'qinq' in self.quads.clouds.data[c]:
                    qinq = self.quads.clouds.data[c]['qinq']
                else:
                    qinq = '0'
                if 'ticket' in self.quads.clouds.data[c]:
                    ticket = self.quads.clouds.data[c]['ticket']
                else:
                    ticket = '000000'
                self.quads.cloud_history.data[c][0] = {'ccusers':ccusers,
                                                       'description':description,
                                                       'owner':owner,
                                                       'qinq':qinq,
                                                       'ticket':ticket}
                updateyaml = True

        if updateyaml:
            self.write_data()

    def read_data(self):
        if not os.path.isfile(self.config):
            try:
                stream = open(self.config, 'w')
                data = {"clouds":{}, "hosts":{}, "history":{}, "cloud_history":{}}
                stream.write( yaml.dump(data, default_flow_style=False))
                stream.close()
            except Exception, ex:
                self.logger.error("There was a problem with your file %s" % ex)
        try:
            stream = open(self.config, 'r')
            self.data = yaml.load(stream)
            stream.close()
        except Exception, ex:
            self.logger.error(ex)
            exit(1)

        self.loadtime = time.time()
        self.quads = QuadsData(self.data)
        self.history_init()
        return

    # we occasionally need to write the data back out
    def write_data(self):
        if self.config_newer_than_data():
            self.read_data()
            return False
        else:
            try:
                stream = open(self.config, 'w')
                self.data = {"clouds":self.quads.clouds.data, "hosts":self.quads.hosts.data, "history":self.quads.history.data, "cloud_history":self.quads.cloud_history.data}
                stream.write( yaml.dump(self.data, default_flow_style=False))
                stream.close()
                return True
            except Exception, ex:
                self.logger.error("There was a problem with your file %s" % ex)
                return False

    def config_newer_than_data(self):
        if os.path.isfile(self.config):
            if os.path.getmtime(self.config) > self.loadtime:
                return True
        return False

    # if passed --init, the config data is wiped.
    # typically we will not want to continue execution if user asks to initialize
    def init_data(self, initialize=False, force=False):
        if initialize:
            if os.path.isfile(self.config):
                if not force:
                    self.logger.warn("Warning: " + self.config + " exists. Use --force to initialize.")
                    return False
            else:
                try:
                    stream = open(self.config, 'w')
                    data = {"clouds":{}, "hosts":{}, "history":{}, "cloud_history":{}}
                    stream.write( yaml.dump(data, default_flow_style=False))
                    return True
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
                    return False
        else:
            return False

    # helper function called from other methods.  Never called from main()
    def find_current(self, host, datearg):
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
                    return None, None, None

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

    # Provide schedule for a given month and year
    def hosts_schedule_query(self,
                             month=datetime.now().month,
                             year=datetime.now().year):
        hosts = self.quads.hosts.data
        schedule = {}
        for host in hosts :
            schedule[host] = {}
            schedule[host][year] = {}
            schedule[host][year][month] = {}
            for day in range(1,calendar.monthrange(int(year),int(month))[1]):
              schedule[host][year][month][day] = self.find_current(host,"{}-{}-{} 00:00".format(year,month,day))

        return schedule

    # sync the statedir db for hosts with schedule
    def sync_state(self):
        # sync state
        if self.datearg is not None:
            self.logger.error("--sync and --date are mutually exclusive.")
            return False
        for h in sorted(self.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = self.find_current(h, self.datearg)
            if not os.path.isfile(self.statedir + "/" + h):
                try:
                    stream = open(self.statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
        return

    # list the hosts
    def print_hosts(self):
        # print just the hostnames
        self.quads.hosts.print_hosts()

    def get_hosts(self):
        # return hosts
        if self.config_newer_than_data():
            self.read_data()
        return self.quads.hosts.get()

    # list the hosts
    def print_clouds(self):
        # print just the hostnames
        if self.config_newer_than_data():
            self.read_data()
        self.quads.clouds.print_clouds()

    def get_clouds(self):
        # return clouds
        if self.config_newer_than_data():
            self.read_data()
        return self.quads.clouds.get()

    # list the owners
    def print_owners(self, cloudonly):
        # list the owners
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            print self.quads.clouds.data[cloudonly]['owner']
            return
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'owner' in self.quads.clouds.data[c]:
                print c + " : " + self.quads.clouds.data[c]['owner']
        return

    # get the owners
    def get_owners(self, cloudonly):
        # return the owners
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return []
            if 'owner' in self.quads.clouds.data[cloudonly]:
                return [self.quads.clouds.data[cloudonly]['owner']]
            return []
        result = []
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'owner' in self.quads.clouds.data[c]:
                result.append(c + " : " + self.quads.clouds.data[c]['owner'])

        return result

    # list the cc users
    def print_cc(self, cloudonly):
        # list the cc users
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            if 'ccusers' not in self.quads.clouds.data[cloudonly]:
                return
            for u in self.quads.clouds.data[cloudonly]['ccusers']:
                print u
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'ccusers' in self.quads.clouds.data[c]:
                print c + " : " + " ".join(self.quads.clouds.data[c]['ccusers'])
        return

    # get the cc users
    def get_cc(self, cloudonly):
        # return the cc users
        result = []
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return []
            if 'ccusers' not in self.quads.clouds.data[cloudonly]:
                return []
            for u in self.quads.clouds.data[cloudonly]['ccusers']:
                result.append(u)
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'ccusers' in self.quads.clouds.data[c]:
                result.append(c + " : " + " ".join(self.quads.clouds.data[c]['ccusers']))
        return result

    # list the tickets
    def print_tickets(self, cloudonly):
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

    # get the tickets
    def get_tickets(self, cloudonly):
        # get the service request tickets
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return []
            if 'ticket' not in self.quads.clouds.data[cloudonly]:
                return []
            return [self.quads.clouds.data[cloudonly]['ticket']]
        result = []
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'ticket' in self.quads.clouds.data[c]:
                result.append(c + " : " + self.quads.clouds.data[c]['ticket'])
        return result

    # print qinq status
    def print_qinq(self, cloudonly):
        # list the environment qinq state
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return
            if 'qinq' not in self.quads.clouds.data[cloudonly]:
                print "0"
                return
            print self.quads.clouds.data[cloudonly]['qinq']
            return
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'qinq' in self.quads.clouds.data[c]:
                print c + " : " + self.quads.clouds.data[c]['qinq']
            else:
                print c + " : 0"
        return

    # get qinq status
    def get_qinq(self, cloudonly):
        # get the environment qinq state
        if cloudonly is not None:
            if cloudonly not in self.quads.clouds.data:
                return []
            if 'qinq' not in self.quads.clouds.data[cloudonly]:
                return ["0"]
            return [self.quads.clouds.data[cloudonly]['qinq']]
        result = []
        for c in sorted(self.quads.clouds.data.iterkeys()):
            if 'qinq' in self.quads.clouds.data[c]:
                result.append(c + " : " + self.quads.clouds.data[c]['qinq'])
            else:
                result.append(c + " : 0")
        return result

    # remove a host
    def remove_host(self, rmhost):
        # remove a specific host
        if rmhost not in self.quads.hosts.data:
            return [rmhost + " not found"]
        del(self.quads.hosts.data[rmhost])
        if self.write_data():
            return ["OK"]
        else:
            return ["ERROR"]

    # remove a cloud
    def quads_remove_cloud(self, rmcloud):
        # remove a cloud (only if no hosts use it)
        if rmcloud not in self.quads.clouds.data:
            return [rmcloud + " not found"]
        for h in self.quads.hosts.data:
            if self.quads.hosts.data[h]["cloud"] == rmcloud:
                return [rmcloud + " is default for " + h,
                        "Change the default before deleting this cloud"]
            for s in self.quads.hosts.data[h]["schedule"]:
                if self.quads.hosts.data[h]["schedule"][s]["cloud"] == rmcloud:
                    return [rmcloud + " is used in a schedule for " + h,
                            "Delete schedule before deleting this cloud"]
        del(self.quads.clouds.data[rmcloud])
        if self.write_data():
            return ["OK"]
        else:
            return ["ERROR"]

    # update a host resource
    def update_host(self, hostresource, hostcloud, forceupdate):
        # define or update a host resouce
        if hostcloud is None:
            self.logger.error("--default-cloud is required when using --define-host")
            return ["--default-cloud is required when using --define-host"]
        else:
            if hostcloud not in self.quads.clouds.data:
                return ["Unknown cloud : %s" % hostcloud,
                        "Define it first using:  --define-cloud"]
            if hostresource in self.quads.hosts.data and not forceupdate:
                self.logger.error("Host \"%s\" already defined. Use --force to replace" % hostresource)
                return ["Host \"%s\" already defined. Use --force to replace" % hostresource]

            if hostresource in self.quads.hosts.data:
                self.quads.hosts.data[hostresource] = { "cloud": hostcloud, "interfaces": self.quads.hosts.data[hostresource]["interfaces"], "schedule": self.quads.hosts.data[hostresource]["schedule"] }
                self.quads.history.data[hostresource][int(time.time())] = hostcloud
            else:
                self.quads.hosts.data[hostresource] = { "cloud": hostcloud, "interfaces": {}, "schedule": {}}
                self.quads.history.data[hostresource] = {}
                self.quads.history.data[hostresource][0] = hostcloud
            if self.write_data():
                return ["OK"]
            else:
                return ["ERROR"]

    # update a cloud resource
    def update_cloud(self, cloudresource, description, forceupdate, cloudowner, ccusers, cloudticket, qinq):
        # define or update a cloud resource
        if description is None:
            self.logger.error("--description is required when using --define-cloud")
            return ["--description is required when using --define-cloud"]
        else:
            if cloudresource in self.quads.clouds.data and not forceupdate:
                self.logger.error("Cloud \"%s\" already defined. Use --force to replace" % cloudresource)
                return ["Cloud \"%s\" already defined. Use --force to replace" % cloudresource]
            if not cloudowner:
                cloudowner = "nobody"
            if not cloudticket:
                cloudticket = "00000"
            if not qinq:
                qinq = "0"
            if not ccusers:
                ccusers = []
            else:
                ccusers = ccusers.split()
            if cloudresource in self.quads.clouds.data:
                if 'ccusers' in self.quads.clouds.data[cloudresource]:
                    savecc = []
                    for cc in self.quads.clouds.data[cloudresource]['ccusers']:
                        savecc.append(cc)
                else:
                    savecc = []
                if 'description' in self.quads.clouds.data[cloudresource]:
                    save_description = self.quads.clouds.data[cloudresource]['description']
                else:
                    save_description = ""
                if 'owner' in self.quads.clouds.data[cloudresource]:
                    save_owner = self.quads.clouds.data[cloudresource]['owner']
                else:
                    save_owner = "nobody"
                if 'qinq' in self.quads.clouds.data[cloudresource]:
                    save_qinq = self.quads.clouds.data[cloudresource]['qinq']
                else:
                    save_qinq = '0'
                if 'ticket' in self.quads.clouds.data[cloudresource]:
                    save_ticket = self.quads.clouds.data[cloudresource]['ticket']
                else:
                    save_ticket = '000000'
                self.quads.cloud_history.data[cloudresource][int(time.time())] = {'ccusers':savecc,
                                                       'description':save_description,
                                                       'owner':save_owner,
                                                       'qinq':save_qinq,
                                                       'ticket':save_ticket}
            self.quads.clouds.data[cloudresource] = { "description": description, "networks": {}, "owner": cloudowner, "ccusers": ccusers, "ticket": cloudticket, "qinq": qinq}
            if self.write_data():
                return ["OK"]
            else:
                return ["ERROR"]

    # define a schedule for a given host
    def add_host_schedule(self, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
        try:
            datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        except Exception, ex:
            self.logger.error("Data format error : %s" % ex)
            return ["Data format error : %s" % ex]

        try:
            datetime.strptime(schedend, '%Y-%m-%d %H:%M')
        except Exception, ex:
            self.logger.error("Data format error : %s" % ex)
            return ["Data format error : %s" % ex]

        if schedcloud not in self.quads.clouds.data:
            self.logger.error("cloud \"" + schedcloud + "\" is not defined.")
            return ["cloud \"" + schedcloud + "\" is not defined."]

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            return ["host \"" + host + "\" is not defined."]

        # before updating the schedule (adding the new override), we need to
        # ensure the host does not have existing schedules that overlap the new
        # schedule being requested

        schedstart_obj = datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
        schedend_obj = datetime.strptime(schedend, '%Y-%m-%d %H:%M')

        if schedend_obj < schedstart_obj:
            self.logger.error("Error. Requested end time is before start time.")
            return ["Error. Requested end time is before start time."]
        if schedend_obj == schedstart_obj:
            self.logger.error("Error. Requested start and end time cannot be the same.")
            return ["Error. Requested start and end time cannot be the same."]

        for s in self.quads.hosts.data[host]["schedule"]:
            s_start = self.quads.hosts.data[host]["schedule"][s]["start"]
            s_end = self.quads.hosts.data[host]["schedule"][s]["end"]

            s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
            s_end_obj = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

            # need code to see if schedstart or schedend is between s_start and
            # s_end

            if s_start_obj <= schedstart_obj and schedstart_obj < s_end_obj:
                return ["Error. New schedule conflicts with existing schedule.",
                        "New schedule: ",
                        "   Start: " + schedstart,
                        "   End: " + schedend,
                        "Existing schedule: ",
                        "   Start: " + s_start,
                        "   End: " + s_end]

            if s_start_obj < schedend_obj and schedend_obj <= s_end_obj:
                return ["Error. New schedule conflicts with existing schedule.",
                        "New schedule: ",
                        "   Start: " + schedstart,
                        "   End: " + schedend,
                        "Existing schedule: ",
                        "   Start: " + s_start,
                        "   End: " + s_end]

        # the next available schedule index should be the max index + 1
        self.quads.hosts.data[host]["schedule"][max(self.quads.hosts.data[host]["schedule"].keys() or [-1])+1] = { "cloud": schedcloud, "start": schedstart, "end": schedend }
        if self.write_data():
            return ["OK"]
        else:
            return ["ERROR"]

    # remove a scheduled override for a given host
    def rm_host_schedule(self, rmschedule, host):
        # remove a scheduled override for a given host
        if host is None:
            self.logger.error("Missing --host option required for --rm-schedule")
            return ["Missing --host option required for --rm-schedule"]

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            return ["host \"" + host + "\" is not defined."]

        if rmschedule not in self.quads.hosts.data[host]["schedule"].keys():
            self.logger.error("Could not find schedule for host")
            return ["Could not find schedule for host"]

        del(self.quads.hosts.data[host]["schedule"][rmschedule])
        if self.write_data():
            return ["OK"]
        else:
            return ["ERROR"]

    # modify an existing schedule
    def mod_host_schedule(self, modschedule, schedstart, schedend, schedcloud, host):
        # add a scheduled override for a given host
        if schedstart:
            try:
                datetime.strptime(schedstart, '%Y-%m-%d %H:%M')
            except Exception, ex:
                self.logger.error("Data format error : %s" % ex)
                return ["Data format error : %s" % ex]

        if schedend:
            try:
                datetime.strptime(schedend, '%Y-%m-%d %H:%M')
            except Exception, ex:
                self.logger.error("Data format error : %s" % ex)
                return ["Data format error : %s" % ex]

        if schedcloud:
            if schedcloud not in self.quads.clouds.data:
                self.logger.error("cloud \"" + schedcloud + "\" is not defined.")
                return ["cloud \"" + schedcloud + "\" is not defined."]

        if host not in self.quads.hosts.data:
            self.logger.error("host \"" + host + "\" is not defined.")
            return ["host \"" + host + "\" is not defined."]

        if modschedule not in self.quads.hosts.data[host]["schedule"].keys():
            self.logger.error("Could not find schedule for host")
            return ["Could not find schedule for host"]

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

        if schedend_obj < schedstart_obj:
            self.logger.error("Error. Requested end time is before start time.")
            return ["Error. Requested end time is before start time."]
        if schedend_obj == schedstart_obj:
            self.logger.error("Error. Requested start and end time cannot be the same.")
            return ["Error. Requested start and end time cannot be the same."]

        for s in self.quads.hosts.data[host]["schedule"]:
            if s != modschedule:
                s_start = self.quads.hosts.data[host]["schedule"][s]["start"]
                s_end = self.quads.hosts.data[host]["schedule"][s]["end"]

                s_start_obj = datetime.strptime(s_start, '%Y-%m-%d %H:%M')
                s_end_obj = datetime.strptime(s_end, '%Y-%m-%d %H:%M')

                # need code to see if schedstart or schedend is between s_start and
                # s_end

                if s_start_obj <= schedstart_obj and schedstart_obj < s_end_obj:
                    return ["Error. Updated schedule conflicts with existing schedule.",
                            "Updated schedule: ",
                            "   Start: " + schedstart,
                            "   End: " + schedend,
                            "Existing schedule: ",
                            "   Start: " + s_start,
                            "   End: " + s_end]

                if s_start_obj < schedend_obj and schedend_obj <= s_end_obj:
                    return ["Error. Updated schedule conflicts with existing schedule.",
                            "Updated schedule: ",
                            "   Start: " + schedstart,
                            "   End: " + schedend,
                            "Existing schedule: ",
                            "   Start: " + s_start,
                            "   End: " + s_end]

        self.quads.hosts.data[host]["schedule"][modschedule]["start"] = schedstart
        self.quads.hosts.data[host]["schedule"][modschedule]["end"] = schedend
        self.quads.hosts.data[host]["schedule"][modschedule]["cloud"] = schedcloud

        if self.write_data():
            return ["OK"]
        else:
            return ["ERROR"]

    # as needed move host(s) based on defined schedules
    # this method will be deprecated in favor of pending_moves
    def move_hosts(self, movecommand, dryrun, statedir, datearg):
        # move a host
        if self.datearg is not None and not dryrun :
            self.logger.error("--move-hosts and --date are mutually exclusive unless using --dry-run.")
            exit(1)
        for h in sorted(self.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = self.find_current(h, datearg)
            if not os.path.isfile(statedir + "/" + h):
                try:
                    stream = open(statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
            else:
                stream = open(statedir + "/" + h, 'r')
                current_state = stream.readline().rstrip()
                stream.close()
                if current_state != current_cloud:
                    self.logger.info("Moving " + h + " from " + current_state + " to " + current_cloud)
                    if not dryrun:
                        try:
                            check_call([movecommand, h, current_state, current_cloud])
                        except Exception, ex:
                            self.logger.error("Move command failed: %s" % ex)
                            exit(1)
                        stream = open(statedir + "/" + h, 'w')
                        stream.write(current_cloud + '\n')
                        stream.close()
        exit(0)

    def pending_moves(self, statedir, datearg):
        # return an array of dicts showing pending moves, e.g.:
        # [{"host":"hostname1", "current":"cloudXX", "new":"cloudYY"},
        #  {"host":"hostname2", "current":"cloudXX", "new":"cloudYY"},
        #  ... ]
        result = []
        for h in sorted(self.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = self.find_current(h, datearg)
            if not os.path.isfile(statedir + "/" + h):
                try:
                    stream = open(statedir + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
            else:
                stream = open(statedir + "/" + h, 'r')
                current_state = stream.readline().rstrip()
                stream.close()
                if current_state != current_cloud:
                    result.append({"host":h, "current":current_state, "new":current_cloud})
        return result

    # generally the last thing that happens is reporting results
    def query(self, host, cloudonly, datearg, summaryreport, fullsummaryreport, lsschedule):
        # If we're here, we're done with all other options and just need to
        # print either summary, full report if no host is specified
        result = []
        if host is None:
            summary = {}

            for cloud in sorted(self.quads.clouds.data.iterkeys()):
                summary[cloud] = []

            for h in sorted(self.quads.hosts.data.iterkeys()):
                default_cloud, current_cloud, current_override = self.find_current(h, datearg)
                summary[current_cloud].append(h)

            cloud_history = self.quads.cloud_history.data
            current_time = datetime.now()
            if datearg is None:
                requested_time = current_time
            else:
                try:
                    requested_time = datetime.strptime(datearg, '%Y-%m-%d %H:%M')
                except Exception, ex:
                    self.logger.error("Data format error : %s" % ex)
                    result.append("Data format error : %s" % ex)
                    return result

            if summaryreport or fullsummaryreport:
                if fullsummaryreport:
                    for cloud in sorted(self.quads.clouds.data.iterkeys()):
                        if requested_time < current_time:
                            for c in sorted(cloud_history[cloud]):
                                if datetime.fromtimestamp(c) <= requested_time:
                                    requested_description = cloud_history[cloud][c]["description"]
                        else:
                            requested_description = self.quads.clouds.data[cloud]["description"]
                        result.append(cloud + " : " + str(len(summary[cloud])) + " (" + requested_description + ")")
                else:
                    for cloud in sorted(self.quads.clouds.data.iterkeys()):
                        if len(summary[cloud]) > 0:
                            if requested_time < current_time:
                                for c in sorted(cloud_history[cloud]):
                                    if datetime.fromtimestamp(c) <= requested_time:
                                        requested_description = cloud_history[cloud][c]["description"]
                            else:
                                requested_description = self.quads.clouds.data[cloud]["description"]
                            result.append(cloud + " : " + str(len(summary[cloud])) + " (" + requested_description + ")")
            else:
                for cloud in sorted(self.quads.clouds.data.iterkeys()):
                    if cloudonly is None:
                        result.append(cloud + ":")
                        for h in summary[cloud]:
                            result.append("  - " + h)
                    else:
                        if cloud == cloudonly:
                            for h in summary[cloud]:
                                result.append(h)

        # print the cloud a host belongs to
        else:
            default_cloud, current_cloud, current_override = self.find_current(host, datearg)

            if lsschedule:
                result.append("Default cloud: " + str(default_cloud))
                result.append("Current cloud: " + str(current_cloud))
                if current_override is not None:
                    result.append("Current schedule: " + str(current_override))
                result.append("Defined schedules:")
                if host in self.quads.hosts.data.keys():
                    for override in self.quads.hosts.data[host]["schedule"]:
                        result.append("  " + str(override) + "| start=" + self.quads.hosts.data[host]["schedule"][override]["start"] +
                            ",end=" + self.quads.hosts.data[host]["schedule"][override]["end"] +
                            ",cloud=" + self.quads.hosts.data[host]["schedule"][override]["cloud"])
            else:
                result.append(current_cloud)

        return result
