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

from hardware_services.network_service import NetworkService

class MockNetworkDriver(NetworkService):

    def move_hosts(self, quadsinstance, **kwargs):
        print "moving hosts"
        for key in kwargs:
            print key, ": ", kwargs[key]



