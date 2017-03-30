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

from hardware_services.hardware_service import HardwareService

class MockDriver(HardwareService):

    def update_cloud(self, quadsinstance, **kwargs):
        print "updating cloud"
        for key in kwargs:
            print key, ": ", kwargs[key]

    def update_host(self, quadsinstance, **kwargs):
        print "Updating host"
        for key in kwargs:
            print key, ": ", kwargs[key]

    def remove_cloud(self, quadsinstance, **kwargs):
        print "removing cloud"
        for key in kwargs:
            print key, ": ", kwargs[key]

    def remove_host(self, quadsinstance, **kwargs):
        print "removing host from cloud"

    def move_hosts(self, quadsinstance, **kwargs):
        print "moving hosts"
        for key in kwargs:
            print key, ": ", kwargs[key]

    def list_clouds(self, quadsinstance):
        print "listing clouds"

    def list_hosts(self, quadsinstance):
        print "listing hosts"


