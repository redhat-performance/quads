#!/usr/bin/env python

import argparse
import datetime
import json
import logging
import os
import requests
import subprocess
import sys
import urllib
import yaml

logger = logging.getLogger('quads-validation')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# used to load the configuration for quads behavior
def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except Exception, ex:
                print "quads: Invalid YAML config: " + quads_config
                exit(1)
    except Exception, ex:
        print ex
        exit(1)
    return(quads_config_yaml)

def main(argv):
    quads_config_file = os.path.dirname(__file__) + "/../conf/quads.yml"
    quads_config = quads_load_config(quads_config_file)

    if "data_dir" not in quads_config:
        print "quads: Missing \"data_dir\" in " + quads_config_file
        exit(1)

    if "install_dir" not in quads_config:
        print "quads: Missing \"install_dir\" in " + quads_config_file
        exit(1)

    if "quads_base_url" not in quads_config:
        print "quads: Missing \"quads_base_url\" in " + quads_config_file
        exit(1)

    sys.path.append(quads_config["install_dir"] + "/lib")
    sys.path.append(os.path.dirname(__file__) + "/../lib")
    from Elastic import Elastic
# Read in passed resultfile, which will contain the failures.

# Parse hostnames out

# Insert hostnames into the hostname key ['b01.h01','...'] failed_hosts

# Insert message into the message key.

