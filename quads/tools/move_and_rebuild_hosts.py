import subprocess

import pexpect

from quads.config import conf, OFFSETS
from quads.helpers import is_supported
from quads.model import Host, Cloud
from quads.tools import make_instackenv_json
from quads.tools.badfish import Badfish
from quads.tools.ssh_helper import SSHHelper


def juniper_set_port(ip_address, switch_port, old_vlan, new_vlan):
    try:
        child = pexpect.spawn("ssh -o StrictHostKeyChecking=no %s@%s" % (conf["junos_username"], ip_address))
        child.expect(">")
        child.sendline("edit")
        child.expect("#")
        child.sendline("rollback")
        child.expect("#")
        child.sendline("delete interfaces %s" % switch_port)
        child.expect("#")
        child.sendline("set interfaces %s apply-groups QinQ_vl%s" % (switch_port, new_vlan))
        child.expect("#")
        child.sendline("delete vlans vlan%s interface %s" % (old_vlan, switch_port))
        child.expect("#")
        child.sendline("set vlans vlan%s interface %s" % (new_vlan, switch_port))
        child.expect("#")
        child.sendline("commit")
        child.expect("#")
        child.sendline("exit")
        child.expect(">")
        child.sendline("exit")
        child.close()
    except pexpect.exceptions.TIMEOUT:
        print("Timeout trying to change settings on switch %s" % ip_address)
        return False
    return True


def move_and_rebuild(host, old_cloud, new_cloud, rebuild=False):
    untouchable_hosts = conf["untouchable_hosts"]
    _host_obj = Host.objects(name=host).first()
    if not _host_obj.interfaces:
        print("Host has no interfaces defined.")
        return False

    if host in untouchable_hosts:
        print("No way...")
        return False

    _old_cloud_obj = Cloud.objects(name=old_cloud).first()
    _new_cloud_obj = Cloud.objects(name=new_cloud).first()
    _old_qinq = _old_cloud_obj.qinq

    for interface in _host_obj.interfaces:
        ssh_helper = SSHHelper(interface.ip_address, conf["junos_username"])
        old_vlan_out = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
        old_vlan = old_vlan_out[0].split(";")[0].split()[1][7:]
        if not old_vlan:
            print(
                "Warning: Could not determine the previous VLAN for %s on %s, switch %s, switchport %s"
                % host, interface.name, interface.ip_address, interface.switch_port
            )
        else:
            old_cloud_offset = int(old_cloud[5:]) * 10
            old_base_vlan = 1090 + old_cloud_offset
            if _old_qinq:
                old_vlan = old_base_vlan + OFFSETS["em1"]
            else:
                old_vlan = old_base_vlan + OFFSETS[interface.name]

        cloud_offset = int(new_cloud[5:]) * 10
        base_vlan = 1090 + cloud_offset
        if _old_qinq:
            new_vlan = base_vlan + OFFSETS["em1"]
        else:
            new_vlan = base_vlan + OFFSETS[interface.name]

        if old_vlan != new_vlan:
            success = juniper_set_port(
                interface.ip_address,
                interface.switch_port,
                str(old_vlan),
                str(new_vlan)
            )
            if success:
                print("Successfully update switch settings.")
            else:
                print("There was something wrong updating switch for %s:%s" % (host, interface.name))

    make_instackenv_json.main()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    # TODO: Add user update to Foreman API Wrapper
    # hammer user update --login $new_cloud --password $foreman_user_password

    ipmi_set_pass = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "set", "password", conf["ipmi_cloud_username_id"], ipmi_new_pass
    ]
    subprocess.call(ipmi_set_pass)

    ipmi_set_operator = [
        "/usr/bin/ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "priv", conf["ipmi_cloud_username_id"], "0x4"
    ]
    subprocess.call(ipmi_set_operator)
    if rebuild and _new_cloud_obj.name != "cloud01":
        badfish = Badfish("mgmt-%s" % host, conf["ipmi_username"], conf["ipmi_password"])

        if conf["pdu_management"]:
            # TODO: pdu management
            pass

        if not is_supported(host):
            badfish.set_next_boot_pxe()

        # TODO: skip ids and Foreman delete interface

        # TODO: Foreman set-parameter

        badfish.reboot_server()
