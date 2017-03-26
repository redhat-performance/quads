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

    def update_cloud(self, **kwargs):
        print "updated cloud"

    def update_host(self, **kwargs):
        print "Updated host"

    def remove_cloud(self, **kwargs):
        print "removed cloud"

    def remove_host(self, **kwargs):
        print "removed host"

    def move_hosts(self, **kwargs):
        print "moved hosts"

    def list_clouds(self):
        print "list clouds"

    def list_hosts(self):
        print "list hosts"


