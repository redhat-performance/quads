from unittest.mock import patch, MagicMock

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.dao.vlan import VlanDao
from quads.tools.ls_switch_conf import verify


def test_verify_ls_switch_conf_not_present():
    cloud_name = "cloud0"

    class Args:
        cloud = cloud_name

    assert not verify(Args())


@patch("quads.tools.ls_switch_conf.logger")
@patch("quads.tools.external.ssh_helper.SSHConfig")
@patch("quads.tools.external.ssh_helper.SSHClient")
def test_verify_ls_switch_conf(mock_client, mock_config, mock_logger):
    mock_config.return_value = MagicMock()
    stdout_mock = MagicMock()
    stdout_mock.readlines.side_effect = [['set vlans vlan1130 interface et-0/0/10:1.0\n'],
                                         [],
                                         ['apply-groups QinQ_vl1134;\n']]
    stdout_mock.channel.recv_exit_status.side_effect = [0, 0, 0]
    stderr_mock = MagicMock()
    stderr_mock.readlines.return_value = False
    mock_client.return_value.exec_command.return_value = (
        MagicMock(),
        stdout_mock,
        stderr_mock,
    )
    cloud_name = "cloud_conf"
    host_name = "cloud_host.example.com"
    cloud = CloudDao.create_cloud(cloud_name)
    HostDao.create_host(host_name, "r640", "unittest", cloud_name)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)
    InterfaceDao.create_interface(hostname=host_name,
                                  name="em1",
                                  bios_id="NIC.Integrated.1",
                                  mac_address="00:d3:00:e4:00:c2",
                                  switch_ip="192.168.1.2",
                                  switch_port="et-0/0/0:1",
                                  speed=1000,
                                  vendor="Mellanox",
                                  pxe_boot=False,
                                  maintenance=False)
    InterfaceDao.create_interface(hostname=host_name,
                                  name="em2",
                                  bios_id="NIC.Integrated.2",
                                  mac_address="00:d3:00:e4:00:c3",
                                  switch_ip="192.168.1.2",
                                  switch_port="et-0/0/0:2",
                                  speed=1000,
                                  vendor="Mellanox",
                                  pxe_boot=False,
                                  maintenance=False)
    InterfaceDao.create_interface(hostname=host_name,
                                  name="em3",
                                  bios_id="NIC.Integrated.3",
                                  mac_address="00:d3:00:e4:00:c4",
                                  switch_ip="192.168.1.2",
                                  switch_port="et-0/0/0:2",
                                  speed=1000,
                                  vendor="Mellanox",
                                  pxe_boot=False,
                                  maintenance=False)

    class Args:
        cloud = cloud_name
        all = True

    verify(Args())
    info = [info[0][0] for info in mock_logger.info.call_args_list]
    assert "Interface em1 appears to be a member of VLAN 1130" in info
    assert "Could not determine the previous VLAN member for em2, switch 192.168.1.2, switch port et-0/0/0:2 " in [
        warn[0][0] for warn in mock_logger.warning.call_args_list]
    assert "Interface em3 appears to be a member of VLAN 1134" in info
    CloudDao.remove_cloud(cloud_name)


def test_verify_ls_switch_conf_empty_hosts():
    cloud_name = "cloud_conf1"
    cloud = CloudDao.create_cloud(cloud_name)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)

    class Args:
        cloud = cloud_name
        all = False

    verify(Args())


@patch("quads.tools.ls_switch_conf.logger")
def test_verify_ls_switch_conf_empty_interfaces(mock_logger):
    cloud_name = "cloud_conf2"
    host_name = "cloud_host2.example.com"
    cloud = CloudDao.create_cloud(cloud_name)
    HostDao.create_host(host_name, "r640", "unittest", cloud_name)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)

    class Args:
        cloud = cloud_name
        all = False

    verify(Args())
    info = [error[0][0] for error in mock_logger.error.call_args_list]
    assert "The cloud has no hosts or the host has no interfaces defined" in info


@patch("quads.tools.ls_switch_conf.logger")
@patch("quads.tools.external.ssh_helper.SSHConfig")
@patch("quads.tools.external.ssh_helper.SSHClient")
def test_verify_ls_switch_conf_one_interface(mock_client, mock_config, mock_logger):
    mock_config.return_value = MagicMock()
    stdout_mock = MagicMock()
    stdout_mock.readlines.side_effect = [['set vlans vlan1130 interface et-0/0/10:1.0\n']]
    stdout_mock.channel.recv_exit_status.side_effect = [0]
    stderr_mock = MagicMock()
    stderr_mock.readlines.return_value = False
    mock_client.return_value.exec_command.return_value = (
        MagicMock(),
        stdout_mock,
        stderr_mock,
    )
    cloud_name = "cloud_conf4"
    host_name = "cloud_host4.example.com"
    cloud = CloudDao.create_cloud(cloud_name)
    HostDao.create_host(host_name, "r640", "unittest", cloud_name)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id)
    InterfaceDao.create_interface(hostname=host_name,
                                  name="em1",
                                  bios_id="NIC.Integrated.1",
                                  mac_address="00:d3:00:e4:00:c2",
                                  switch_ip="192.168.1.2",
                                  switch_port="et-0/0/0:1",
                                  speed=1000,
                                  vendor="Mellanox",
                                  pxe_boot=False,
                                  maintenance=False)

    class Args:
        cloud = cloud_name
        all = True

    verify(Args())
    info = [info[0][0] for info in mock_logger.info.call_args_list]
    assert "Interface em1 appears to be a member of VLAN vlans" in info
    CloudDao.remove_cloud(cloud_name)
