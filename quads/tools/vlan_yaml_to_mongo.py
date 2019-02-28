#! /usr/bin/env python3
import logging
import argparse
import yaml

from quads.model import Vlan, Cloud

logger = logging.getLogger(__name__)


def main(_args):
    if _args.yaml:
        try:
            with open(_args.yaml, "r") as _vlans_read:
                try:
                    vlans = yaml.safe_load(_vlans_read)
                except yaml.YAMLError:
                    logger.error("quads: Invalid YAML config: " + _args.yaml)
                    exit(1)
                for vlan, properties in vlans.items():
                    vlan_obj = Vlan.objects(vlan_id=properties["vlanid"]).first()
                    cloud_name = "cloud0%s" % properties["cloud"] if int(properties["cloud"]) < 10 \
                        else "cloud%s" % properties["cloud"]
                    cloud_obj = Cloud.objects(name=cloud_name).first()
                    result, data = Vlan.prep_data(properties)
                    if not result:
                        if cloud_obj:
                            data["cloud"] = cloud_obj
                        else:
                            data.pop("cloud")
                    else:
                        logger.error("Failed to validate all fields")
                        exit(1)
                    if vlan_obj:
                        vlan_obj.update(**data)
                        logger.info("Updated vlan: %s" % data["vlan_id"])
                    else:
                        Vlan(**data).save()
                        logger.info("Inserted vlan: %s" % data["vlan_id"])
        except IOError as ex:
            logger.debug(ex)
            logger.error("Error reading %s" % _args.yaml)
            exit(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--yaml", dest="yaml", type=str, required=True)

    args = parser.parse_args()
    main(args)
