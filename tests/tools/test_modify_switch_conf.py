from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.tools.modify_switch_conf import verify as modify_switch_verify


def test_verify_false():
    assert not modify_switch_verify("host.verify.example.com.example.com")


def test_verify_empty():
    CloudDao.create_cloud("cloudverify")
    HostDao.create_host("host.verify.example.com", "r640", "unittest", "cloudverify")
    response = modify_switch_verify("host.verify.example.com")
    assert not response
    HostDao.remove_host("host.verify.example.com")
    CloudDao.remove_cloud("cloudverify")


# def test_verify():
    # cloud_name = "cloudverify"
    # host_name = "host.verify.example.com"
    # CloudDao.create_cloud(cloud_name)
    # HostDao.create_host(host_name, "r640", "unittest", cloud_name)
    # interface = InterfaceDao.create_interface(hostname=host_name,
    #                               name="em1",
    #                               bios_id="NIC.Integrated.1",
    #                               mac_address="00:d3:00:e4:00:c2",
    #                               switch_ip="192.168.1.2",
    #                               switch_port="et-0/0/0:1",
    #                               speed=1000,
    #                               vendor="Mellanox",
    #                               pxe_boot=False,
    #                               maintenance=False)
    # modify_switch_verify("host1.example.com")
    # InterfaceDao.delete_interface(interface.id)
    # HostDao.remove_host(host_name)
    # CloudDao.remove_cloud("cloud99", nic1="")
