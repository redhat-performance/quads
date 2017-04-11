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

from hardware_services.network_service import NetworkService

class QuadsNativeNetworkDriver(NetworkService):

    def move_hosts(self, quadsinstance, **kwargs):
        # move a host
        for h in sorted(quadsinstance.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = quadsinstance._quads_find_current(h, kwargs['datearg'])
            if not os.path.isfile(kwargs['statedir'] + "/" + h):
                try:
                    stream = open(kwargs['statedir'] + "/" + h, 'w')
                    stream.write(current_cloud + '\n')
                    stream.close()
                except Exception, ex:
                    quadsinstance.logger.error("There was a problem with your file %s" % ex)
            else:
                stream = open(kwargs['statedir'] + "/" + h, 'r')
                current_state = stream.readline().rstrip()
                stream.close()
                if current_state != current_cloud:
                    quadsinstance.logger.info("Moving " + h + " from " + current_state + " to " + current_cloud)
                    if not kwargs['dryrun']:
                        try:
                            check_call([kwargs['movecommand'], h, current_state, current_cloud])
                        except Exception, ex:
                            quadsinstance.logger.error("Move command failed: %s" % ex)
                            exit(1)
                        stream = open(kwargs['statedir'] + "/" + h, 'w')
                        stream.write(current_cloud + '\n')
                        stream.close()
        return


