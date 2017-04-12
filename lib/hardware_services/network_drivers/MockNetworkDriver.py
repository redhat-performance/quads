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

#from bin 
from hardware_services.network_service import NetworkService

class MockNetworkDriver(NetworkService):

    #def move_hosts(self, quadsinstance, **kwargs):
	#for h in sorted(quadsinstance.quads.hosts.data.iterkeys()):	
		#default_cloud, current_cloud, current_override = quadsinstance._quads_find_current(h, kwargs['datearg'])       
		#print h
	#if (h == NULL):
	#	print "no hosts"	
	#print "moving hosts"
        #for key in kwargs:
            #print key, ": ", kwargs[key]
	    #print kwargs[key]
	#print "Moving hosts from" 


    def move_hosts(self, quadsinstance, **kwargs):
    	#move a host
        for h in sorted(quadsinstance.quads.hosts.data.iterkeys()):
            default_cloud, current_cloud, current_override = quadsinstance._quads_find_current(h, kwargs['datearg'])
	    #print current_cloud
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
	print "Moving "+ h+ " from " + default_cloud + " to " + current_cloud
        return
