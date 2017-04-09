# this class will inherit from hardware_service.py and overwrite all of its methods
# with hil-specific behaviors - mostly through api calls to the HIL server

from datetime import datetime
import calendar
import time
import yaml
import argparse
import os
import sys
import requests
import logging
import json
from subprocess import call
from subprocess import check_call

from hardware_services.network_service import NetworkService

# added for EC528 HIL-QUADS integration project
hil_url = 'http://127.0.0.1:5000'

class HilNetworkDriver(NetworkService):


    def move_hosts(self, quadsinstance, **kwargs):
        targetProject = kwargs['movecommand']
        current = kwargs['statedir']
        quadsinstance.quads_rest_call("POST", hil_url, '/project/'+current+'/detach_node')
        quadsinstance.quads_rest_call("POST", hil_url, '/project/'+targetProject+'/connect_node')





