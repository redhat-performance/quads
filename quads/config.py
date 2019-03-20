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

QUADSVERSION = "1.1.0"
QUADSCODENAME = "gaúcho"
SUPPORTED = ["r620", "r630", "r720", "r730", "r930"]
SUPERMICROS = ["1029p", "1029u", "1028r", "6029p", "6018r", "6048r", "5039ms"]
OFFSETS = {"em1": 0, "em2": 1, "em3": 2, "em4": 3}
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "templates")
TOLERANCE = 14400
INTERFACES = {
    "em1": ["172.16", "172.20"],
    "em2": ["172.17", "172.21"],
    "em3": ["172.18", "172.22"],
    "em4": ["172.19", "172.23"],
}
LOGFMT = "%(asctime)-12s : %(levelname)-8s - %(message)s"
STDFMT = "- %(levelname)-8s - %(message)s"

API = "v2"
API_URL = os.path.join(conf['quads_base_url'], 'api', API)
