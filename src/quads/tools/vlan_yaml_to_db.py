#!/usr/bin/env python3

import logging
import argparse
import yaml

from quads.config import Config, DEFAULT_CONF_PATH
from quads.quads_api import QuadsApi, APIBadRequest, APIServerException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main(_args):
    Config.load_from_yaml(DEFAULT_CONF_PATH)

    quads = QuadsApi(config=Config)
    vlans = None

    if _args.yaml:
        try:
            with open(_args.yaml, "r") as _vlans_read:
                try:
                    vlans = yaml.safe_load(_vlans_read)
                except yaml.YAMLError:
                    logger.error("quads: Invalid YAML config: " + _args.yaml)
                    exit(1)
        except IOError as ex:
            logger.debug(ex)
            logger.error("Error reading %s" % _args.yaml)
            exit(1)
        if vlans:
            for vlan, properties in vlans.items():
                try:
                    vlan = quads.get_vlan(properties["vlan_id"])
                except (APIServerException, APIBadRequest):
                    quads.create_vlan(properties)
                    logger.info("Inserted vlan: %s" % properties["vlan_id"])
                    continue
                quads.update_vlan(properties["vlan_id"], properties)
                logger.info("Updated vlan: %s" % properties["vlan_id"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", dest="yaml", type=str, required=True)

    args = parser.parse_args()
    main(args)
