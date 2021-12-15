import logging
import pexpect

from quads.config import conf

logger = logging.getLogger(__name__)


class JuniperException(Exception):
    pass


class Juniper(object):
    def __init__(self, ip_address, switch_port, old_vlan, new_vlan):
        self.ip_address = ip_address
        self.switch_port = switch_port
        self.old_vlan = str(old_vlan)
        self.new_vlan = str(new_vlan)
        self.child = None

    def connect(self):
        logger.debug("Connecting to switch: %s" % self.ip_address)
        try:
            self.child = pexpect.spawn(
                "ssh -o StrictHostKeyChecking=no %s@%s"
                % (conf["junos_username"], self.ip_address)
            )
            self.child.expect(">")
        except pexpect.exceptions.TIMEOUT:
            raise JuniperException("Timeout trying to connect via SSH")

    def close(self):
        self.child.close()

    def execute(self, command, expect="#"):
        logger.debug(command)
        try:
            self.child.sendline(command)
            self.child.expect(expect, timeout=120)
        except pexpect.exceptions.TIMEOUT:
            raise JuniperException(f"Timeout trying to execute the command: {command}")

    def set_port(self):
        try:
            self.execute("edit")
            self.execute("rollback")
            self.execute(f"delete interfaces {self.switch_port}")
            self.execute(
                f"set interfaces {self.switch_port} apply-groups QinQ_vl{self.new_vlan}"
            )

            if self.old_vlan:
                self.execute(
                    f"delete vlans vlan{self.old_vlan} interface {self.switch_port}"
                )

            self.execute(f"set vlans vlan{self.new_vlan} interface {self.switch_port}")
            self.execute("commit", "commit complete")
        except JuniperException as ex:
            logger.debug(ex)
            return False
        return True

    def convert_port_public(self):
        try:
            self.execute("edit")
            self.execute("rollback")
            self.execute(f"delete interfaces {self.switch_port}")
            self.execute(
                f"set interfaces {self.switch_port} native-vlan-id {self.new_vlan}"
            )
            self.execute(
                f"set interfaces {self.switch_port} unit 0 family ethernet-switching interface-mode trunk"
            )
            self.execute(
                f"set interfaces {self.switch_port} unit 0 family ethernet-switching vlan members vlan{self.new_vlan}"
            )

            if self.old_vlan and self.old_vlan != self.new_vlan:
                self.execute(
                    f"delete vlans vlan{self.old_vlan} interface {self.switch_port}"
                )

            self.execute("commit", "commit complete")
        except JuniperException as ex:
            logger.debug(ex)
            return False
        return True
