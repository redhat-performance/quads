#!/usr/bin/env python3

import logging
import pexpect

from quads.config import conf

logger = logging.getLogger(__name__)


def juniper_convert_port_public(ip_address, switch_port, old_vlan, new_priv_vlan, new_pub_vlan):
    try:
        logger.debug("Connecting to switch: %s" % ip_address)
        child = pexpect.spawn("ssh -o StrictHostKeyChecking=no %s@%s" % (conf["junos_username"], ip_address))
        child.expect(">")

        logger.debug("edit")
        child.sendline("edit")
        child.expect("#")

        logger.debug("rollback")
        child.sendline("rollback")
        child.expect("#")

        logger.debug("delete interfaces %s" % switch_port)
        child.sendline("delete interfaces %s" % switch_port)
        child.expect("#")

        logger.debug("set interfaces %s native-vlan-id %s" % (switch_port, new_priv_vlan))
        child.sendline("set interfaces %s native-vlan-id %s" % (switch_port, new_priv_vlan))
        child.expect("#")

        logger.debug("set interfaces %s unit 0 family ethernet-switching interface-mode trunk" % switch_port)
        child.sendline("set interfaces %s unit 0 family ethernet-switching interface-mode trunk" % switch_port)
        child.expect("#")

        logger.debug("set interfaces %s unit 0 family ethernet-switching vlan members [ vlan%s vlan%s ]" % (
            switch_port, new_priv_vlan, new_pub_vlan))
        child.sendline("set interfaces %s unit 0 family ethernet-switching vlan members [ vlan%s vlan%s ]" % (
            switch_port, new_priv_vlan, new_pub_vlan))
        child.expect("#")

        logger.debug("delete vlans vlan%s interface %s" % (old_vlan, switch_port))
        child.sendline("delete vlans vlan%s interface %s" % (old_vlan, switch_port))
        child.expect("#")

        logger.debug("commit")
        child.sendline("commit")
        child.expect("#")

        logger.debug("exit")
        child.sendline("exit")
        child.expect(">")

        logger.debug("exit")
        child.sendline("exit")
        child.close()

    except pexpect.exceptions.TIMEOUT:
        logger.error("Timeout trying to change settings on switch %s" % ip_address)
        return False
    return True
