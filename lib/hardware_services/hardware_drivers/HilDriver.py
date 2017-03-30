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
from subprocess import call
from subprocess import check_call

from hardware_services.hardware_service import HardwareService

# added for EC528 HIL-QUADS integration project - not a good place for this variable - should be moved eventually
hil_url = 'http://127.0.0.1:5000'

class HilDriver(HardwareService):


    def update_cloud(self, quadsinstance, **kwargs):


    def update_host(self, quadsinstance, **kwargs):


    def remove_cloud(self, quadsinstance, **kwargs):
        targetProject = kwargs['rmcloud']
        quadsinstance.quads_rest_call("DELETE", hil_url, '/project/'+ targetProject)


    def remove_host(self,quadsinstance, **kwargs):
        targetHost = kwargs['rmhost']
        quadsinstance.quads_rest_call("DELETE", hil_url, '/node/'+ targetHost)


    def move_hosts(self, quadsinstance, **kwargs):
        targetProject = kwargs['movecommand']
        current = kwargs['statedir']
        quadsinstance.quads_rest_call("POST", hil_url, '/project/'+current+'/detach_node')
        quadsinstance.quads_rest_call("POST", hil_url, '/project/'+targetProject+'/connect_node')


    def list_clouds(self, quadsinstance):
        quadsinstance.quads_rest_call("GET", hil_url, '/projects')


    def list_hosts(self, quadsinstance):
        quadsinstance.quads_rest_call("GET", hil_url, '/nodes/all')


