import os

from config import conf, OFFSETS
from helpers import is_supported
from model import Host, Cloud
from tools import make_instackenv_json
from tools.badfish import Badfish
from tools.ssh_helper import SSHHelper


def move_and_rebuild(host, old_cloud, new_cloud, rebuild=False):
    scripts_dir = os.path.join(conf["install_dir"], "scripts")
    expect_script = os.path.join(scripts_dir, "juniper-set-port.exp")
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
        ssh_helper = SSHHelper(interface.ip_address)
        # TODO: check output
        old_vlan = ssh_helper.run_cmd("show configuration interfaces %s" % interface.switch_port)
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

        os.subprocess.call(
            [expect_script,
             interface.ip_address,
             interface.switch_port,
             old_vlan,
             new_vlan]
        )

    make_instackenv_json.main()

    ipmi_new_pass = _new_cloud_obj.ticket if _new_cloud_obj.ticket else conf["$ipmi_password"]

    # TODO: Add user update to Foreman API Wrapper
    # hammer user update --login $new_cloud --password $foreman_user_password

    ipmi_set_pass = [
        "ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "set", "password", conf["ipmi_cloud_username_id"], ipmi_new_pass
    ]
    os.subprocess.call(ipmi_set_pass)

    ipmi_set_operator = [
        "ipmitool",
        "-I", "lanplus",
        "-H", "mgmt-%s" % host,
        "-U", conf["ipmi_username"],
        "-P", conf["ipmi_password"],
        "user", "priv", conf["ipmi_cloud_username_id"], "0x4"
    ]
    os.subprocess.call(ipmi_set_operator)
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
