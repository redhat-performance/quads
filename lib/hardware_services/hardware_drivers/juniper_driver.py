# this class will inherit from hardware_service.py and overwrite all of its methods
# with the current quads behavior (calling scripts that interface with juniper switches)
from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
import requests
import logging
from subprocess import call
from subprocess import check_call

from hardware_services.hardware_service import HardwareService

class JuniperDriver(HardwareService):

    def update_cloud(self, **kwargs):
        if kwargs['description'] is None:
            self.logger.error("--description is required when using --define-cloud")
            exit(1)
        else:
            if kwargs['cloudresource'] in self.quads.clouds.data and not kwargs['forceupdate']:
                self.logger.error("Cloud \"%s\" already defined. Use --force to replace" % kwargs['cloudresource'])
                exit(1)
            if not kwargs['cloudowner']:
                kwargs['cloudowner'] = "nobody"
            if not kwargs['cloudticket']:
                kwargs['cloudticket'] = "00000"
            if not kwargs['qinq']:
                kwargs['qinq'] = "0"
            if not kwargs['ccusers']:
                ccusers = []
            else:
                ccusers = ccusers.split()
            self.quads.clouds.data[kwargs['cloudresource']] = { "description": kwargs['description'], "networks": {}, 
                "owner": ['cloudowner'], "ccusers": kwargs['ccusers'], "ticket": kwargs['cloudticket'], "qinq": kwargs['qinq']}
            self.quads_write_data()

        return


    def update_host(self, **kwargs):
        if kwargs['hostcloud'] is None:
            self.logger.error("--default-cloud is required when using --define-host")
            exit(1)
        else:
            if kwargs['hostcloud'] not in self.quads.clouds.data:
                print "Unknown cloud : %s" % kwargs['hostcloud']
                print "Define it first using:  --define-cloud"
                exit(1)
            if kwargs['hostresource'] in self.quads.hosts.data and not kwargs['forceupdate']:
                self.logger.error("Host \"%s\" already defined. Use --force to replace" % kwargs['hostresource'])
                exit(1)

            if kwargs['hostresource'] in self.quads.hosts.data:
                self.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": self.quads.hosts.data[kwargs['hostresource']]["interfaces"], 
                    "schedule": self.quads.hosts.data[kwargs['hostresource']]["schedule"] }
                self.quads.history.data[kwargs['hostresource']][int(time.time())] = kwargs['hostcloud']
            else:
                self.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": {}, "schedule": {}}
                self.quads.history.data[kwargs['hostresource']] = {}
                self.quads.history.data[kwargs['hostresource']][0] = kwargs['hostcloud']
            self.quads_write_data()
            
            return


    def remove_cloud(self, **kwargs):
        # remove a cloud (only if no hosts use it)
        if kwargs['rmcloud'] not in self.quads.clouds.data:
            print kwargs['rmcloud'] + " not found"
            return
        for h in self.quads.hosts.data:
            if self.quads.hosts.data[h]["cloud"] == kwargs['rmcloud']:
                print kwargs['rmcloud'] + " is default for " + h
                print "Change the default before deleting this cloud"
                return
            for s in self.quads.hosts.data[h]["schedule"]:
                if self.quads.hosts.data[h]["schedule"][s]["cloud"] == kwargs['rmcloud']:
                    print kwargs['rmcloud'] + " is used in a schedule for "  + h
                    print "Delete schedule before deleting this cloud"
                    return
        del(self.quads.clouds.data[kwargs['rmcloud']])
        self.quads_write_data()

        return
        
    def remove_host(self, **kwargs):
        # remove a specific host
        if kwargs['rmhost'] not in self.quads.hosts.data:
            print kwargs['rmhost'] + " not found"
            return
        del(self.quads.hosts.data[kwargs['rmhost']])
        self.quads_write_data()

        return

    def move_hosts(self, **kwargs):
        # move a host
        for h in sorted(self.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = self._quads_find_current(h, kwargs['datearg'])
            if not os.path.isfile(kwargs['statedir'] + "/" + h):
                try:
                    stream = open(kwargs['statedir'] + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    self.logger.error("There was a problem with your file %s" % ex)
            else:
                stream = open(kwargs['statedir'] + "/" + h, 'r')
                current_state = stream.readline().rstrip()
                stream.close()
                if current_state != current_cloud:
                    self.logger.info("Moving " + h + " from " + current_state + " to " + current_cloud)
                    if not kwargs['dryrun']:
                        try:
                            check_call([kwargs['movecommand'], h, current_state, current_cloud])
                        except Exception, ex:
                            self.logger.error("Move command failed: %s" % ex)
                            exit(1)
                        stream = open(kwargs['statedir'] + "/" + h, 'w')
                        stream.write(current_cloud + '\n')
                        stream.close()
        exit(0)

    def list_clouds(self):
        self.quads.clouds.cloud_list()

    def list_hosts(self):
        self.quads.hosts.host_list()


