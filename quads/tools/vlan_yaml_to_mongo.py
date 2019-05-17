#!/usr/bin/python3

import logging
import argparse
import yaml

from quads.model import Vlan

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def main(_args):
    if _args.yaml:
        vlans = None
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
                vlan_obj = Vlan.objects(vlan_id=properties["vlanid"]).first()
                result, data = Vlan.prep_data(properties)
                if result:
                    logger.error("Failed to validate all fields")
                    exit(1)
                if vlan_obj:
                    vlan_obj.update(**data)
                    logger.info("Updated vlan: %s" % data["vlan_id"])
                else:
                    Vlan(**data).save()
                    logger.info("Inserted vlan: %s" % data["vlan_id"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", dest="yaml", type=str, required=True)

    args = parser.parse_args()
    main(args)
