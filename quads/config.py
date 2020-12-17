#!/usr/bin/env python3
import logging
import os
import yaml

logger = logging.getLogger(__name__)


def quads_load_config(quads_config):
    try:
        with open(quads_config, 'r') as config_file:
            try:
                quads_config_yaml = yaml.safe_load(config_file)
            except yaml.YAMLError as ex:
                logger.debug(ex)
                logger.error("quads: Invalid YAML config: " + quads_config)
                return
    except Exception as ex:
        logger.debug(ex)
        return
    return quads_config_yaml


quads_config_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(quads_config_file)

QUADSVERSION = "1.1.4.1"
QUADSCODENAME = "gaúcho"
SUPPORTED = ["fc640", "r620", "r630", "r640", "640", "r720", "r730xd", "r930", "r730", "r740xd", "740xd", "r720xd"]
OFFSETS = {"em1": 0, "em2": 1, "em3": 2, "em4": 3, "em5": 4}
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")
INTERFACES = {
    "em1": ["172.16", "172.21"],
    "em2": ["172.17", "172.22"],
    "em3": ["172.18", "172.23"],
    "em4": ["172.19", "172.24"],
    "em5": ["172.20", "172.25"],
}
LOGFMT = "%(asctime)-12s : %(levelname)-8s - %(message)s"
STDFMT = "- %(levelname)-8s - %(message)s"

API = "v2"
API_URL = os.path.join(conf['quads_base_url'], 'api', API)
