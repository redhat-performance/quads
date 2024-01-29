#!/usr/bin/env python3
import argparse
import asyncio
import logging

from quads.config import Config
from quads.model import Host, Interface
from quads.tools.external.badfish import BadfishException, badfish_factory
from quads.tools.helpers import get_running_loop

logger = logging.getLogger(__name__)


class Populator(object): # pragma: no cover
    def __init__(self, _loop=None):
        self.loop = _loop if _loop else get_running_loop()

    @staticmethod
    async def list_interfaces(badfish):
        data = None
        na_supported = await badfish.check_supported_network_interfaces(
            "NetworkAdapters"
        )
        ei_supported = await badfish.check_supported_network_interfaces(
            "EthernetInterfaces"
        )
        if na_supported:
            logger.debug("  Getting Network Adapters")
            data = await badfish.get_network_adapters()
        elif ei_supported:
            logger.debug("  Getting Ethernet interfaces")
            data = await badfish.get_ethernet_interfaces()
        else:
            logger.error("  Server does not support this functionality")
        return data

    async def populate(self, host):
        logger.info(host.name)
        badfish = None
        interfaces = None
        try:
            badfish = await badfish_factory(
                "mgmt-" + host.name,
                str(Config["ipmi_username"]),
                str(Config["ipmi_password"]),
                loop=self.loop,
            )
            interfaces = await self.list_interfaces(badfish)
        except BadfishException as ಥ﹏ಥ:
            logger.debug(ಥ﹏ಥ)
            if badfish:
                logger.warning(
                    f"  There was something wrong trying to boot from Foreman interface for: {host.name}"
                )
                await badfish.reboot_server()
            else:
                logger.error(f"  Could not initiate Badfish instance for: {host.name}")

        if interfaces:
            for interface, properties in interfaces.items():
                logger.info(f"  {interface}:")

                values = {}

                link_capabilities = properties.get("SupportedLinkCapabilities")
                if link_capabilities:
                    speed = link_capabilities[0].get("LinkSpeedMbps")
                    if speed:
                        values["speed"] = speed

                mac_address = properties.get("MACAddress")
                if mac_address:
                    values["mac_address"] = mac_address.lower()
                else:
                    logger.error(
                        "  No MAC Address defined for this interface. SKIPPING."
                    )
                    continue

                bios_id = properties.get("Id")
                if bios_id:
                    values["bios_id"] = bios_id

                vendor = properties.get("Vendor")
                if vendor:
                    values["vendor"] = vendor.split()[0].upper()

                mod_interface = None
                for host_interface in host.interfaces:
                    bf_mac_address = values.get("mac_address")
                    if host_interface.mac_address.lower() == bf_mac_address.lower():
                        mod_interface = host_interface
                        break

                if not mod_interface:
                    logger.error("  BF interface not declared on Quads")
                    continue

                new_interface = Interface()
                for key in mod_interface:
                    if values.get(key):
                        new_interface[key] = values[key]
                    else:
                        new_interface[key] = mod_interface[key]

                if values:
                    try:
                        kwargs = {"set__interfaces__S": new_interface}
                        Host.objects.filter(
                            name=host.name,
                            interfaces__mac_address=values["mac_address"],
                        ).update_one(**kwargs)
                        logger.info(
                            f"    Interface {mod_interface.name} successfully updated"
                        )
                    except Exception as ex:
                        logger.error(
                            f"    Failed to update {mod_interface.name} interface"
                        )
                        logger.debug(ex)

        else:
            logger.warning(
                f"  No interfaces information could be retrieved for {host.name}"
            )

        return


def main(_loop): # pragma: no cover
    validator = Populator(_loop)
    hosts = Host.objects()
    for host in hosts:
        try:
            _loop.run_until_complete(validator.populate(host))
        except Exception as ex:
            logger.debug(ex)
            logger.info("  Failed to populate interfaces for %s" % host.name)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description="Validate Quads assignments")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Show debugging information.",
    )
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(message)s")

    loop_main = asyncio.get_event_loop()
    asyncio.set_event_loop(loop_main)

    main(loop_main)
