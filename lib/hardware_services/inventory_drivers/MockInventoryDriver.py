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
        print "updating cloud"
        print "just kidding - it's the Mock Driver! Going to list all keyword arguments for testing"
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


    def list_clouds(self, quadsinstance):
        print "listing clouds"
        print "just kidding - no clouds here, it's the Mock Driver!"

    def list_hosts(self, quadsinstance):
        print "listing hosts"

    def load_data(self, quadsinstance, force):
        print("data is loaded")

    def write_data(self, quadsinstance, doexit = True):
        print("data is written")

    def sync_state(self, quadsinstance):
        print("data is synchronized")

    def init_data(self, quadsinstance, force):
        print("data is initialized")


