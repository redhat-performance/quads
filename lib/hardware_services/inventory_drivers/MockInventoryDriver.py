# inherits from hardware_service.py and overwrites methods. This is a mock driver for testing purposes and will not be attached to any specific hardware
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

from hardware_services.inventory_service import InventoryService

class MockInventoryDriver(InventoryService):

    def update_cloud(self, quadsinstance, **kwargs):
        if kwargs['description'] is None:
            quadsinstance.logger.error("--description is required when using --define-cloud")
            exit(1)
        else:
            if kwargs['cloudresource'] in quadsinstance.quads.clouds.data and not kwargs['forceupdate']:
                quadsinstance.logger.error("Cloud \"%s\" already defined. Use --force to replace" % kwargs['cloudresource'])
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
            quadsinstance.quads.clouds.data[kwargs['cloudresource']] = { "description": kwargs['description'], "networks": {},
                "owner": kwargs['cloudowner'], "ccusers": kwargs['ccusers'], "ticket": kwargs['cloudticket'], "qinq": kwargs['qinq']}
            quadsinstance.quads_write_data()

        return


    def update_host(self, quadsinstance, **kwargs):
        if kwargs['hostcloud'] is None:
            quadsinstance.logger.error("--default-cloud is required when using --define-host")
            exit(1)
        else:
            if kwargs['hostcloud'] not in quadsinstance.quads.clouds.data:
                print "Unknown cloud : %s" % kwargs['hostcloud']
                print "Define it first using:  --define-cloud"
                exit(1)
            if kwargs['hostresource'] in quadsinstance.quads.hosts.data and not kwargs['forceupdate']:
                quadsinstance.logger.error("Host \"%s\" already defined. Use --force to replace" % kwargs['hostresource'])
                exit(1)

            if kwargs['hostresource'] in quadsinstance.quads.hosts.data:
                quadsinstance.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": self.quads.hosts.data[kwargs['hostresource']]["interfaces"],
                    "schedule": quadsinstance.quads.hosts.data[kwargs['hostresource']]["schedule"] }
                quadsinstance.quads.history.data[kwargs['hostresource']][int(time.time())] = kwargs['hostcloud']
            else:
                quadsinstance.quads.hosts.data[kwargs['hostresource']] = { "cloud": kwargs['hostcloud'], "interfaces": {}, "schedule": {}}
                quadsinstance.quads.history.data[kwargs['hostresource']] = {}
                quadsinstance.quads.history.data[kwargs['hostresource']][0] = kwargs['hostcloud']
            quadsinstance.quads_write_data()

            return


    def remove_cloud(self, quadsinstance, **kwargs):
        # remove a cloud (only if no hosts use it)
        if kwargs['rmcloud'] not in quadsinstance.quads.clouds.data:
            print kwargs['rmcloud'] + " not found"
            return
        for h in quadsinstance.quads.hosts.data:
            if quadsinstance.quads.hosts.data[h]["cloud"] == kwargs['rmcloud']:
                print kwargs['rmcloud'] + " is default for " + h
                print "Change the default before deleting this cloud"
                return
            for s in quadsinstance.quads.hosts.data[h]["schedule"]:
                if quadsinstance.quads.hosts.data[h]["schedule"][s]["cloud"] == kwargs['rmcloud']:
                    print kwargs['rmcloud'] + " is used in a schedule for "  + h
                    print "Delete schedule before deleting this cloud"
                    return
        del(quadsinstance.quads.clouds.data[kwargs['rmcloud']])
        quadsinstance.quads_write_data()

        return

    def remove_host(self, quadsinstance, **kwargs):
        # remove a specific host
        print(quadsinstance)
        #print(kwargs)
        if kwargs['rmhost'] not in quadsinstance.quads.hosts.data:
            print kwargs['rmhost'] + " not found"
            return
        del(quadsinstance.quads.hosts.data[kwargs['rmhost']])
        quadsinstance.quads_write_data()

        return


    def list_clouds(self,quadsinstance):
        quadsinstance.quads.clouds.cloud_list()

    def list_hosts(self,quadsinstance):
        quadsinstance.quads.hosts.host_list()

    def load_data(self, quadsinstance, force):
        if initialize:
            quadsinstance.quads_init_data(force)
        try:
            stream = open(quadsinstance.config, 'r')
            quadsinstance.data = yaml.load(stream)
            stream.close()
        except Exception, ex:
            quadsinstance.logger.error(ex)
            exit(1)

    def write_data(self, quadsinstance, doexit = True):
        quadsinstance.quads_write_data_(doexit)

    def sync_state(self, quadsinstance):
        quadsinstance.quads_sync_state_()

    def init_data(self, quadsinstance, force):
        quadsinstance.quads_init_data_(force)



