import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from tests.cli.config import (
    HOST,
    CLOUD,
    IFNAME,
    IFMAC,
    IFIP,
    IFPORT,
    IFBIOSID,
    IFSPEED,
    IFVENDOR,
)
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    if host:
        HostDao.remove_host(name=HOST)
    cloud = CloudDao.get_cloud(CLOUD)
    if cloud:
        CloudDao.remove_cloud(CLOUD)


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


@pytest.fixture
def mod_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    InterfaceDao.create_interface(
        HOST, IFNAME, IFBIOSID, IFMAC, IFIP, IFPORT, IFSPEED, IFVENDOR, False, False
    )


class TestInterface(TestBase):
    def test_define_interface_no_params(self, remove_fixture):
        try:
            self.quads_cli_call("addinterface")
        except CliException as ex:
            assert str(ex) == (
                "Missing option. All these options are required for --add-interface:\n"
                "\t--host\n"
                "\t--interface-name\n"
                "\t--interface-mac\n"
                "\t--interface-ip\n"
                "\t--interface-port"
            )

    def test_define_interface_missing_bios_id(self, remove_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME
        self.cli_args["ifmac"] = IFMAC
        self.cli_args["ifip"] = IFIP
        self.cli_args["ifport"] = IFPORT
        try:
            self.quads_cli_call("addinterface")
        except CliException as ex:
            assert "Missing argument: bios_id" == str(ex)

    def test_define_interface_missing_speed(self, remove_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME
        self.cli_args["ifmac"] = IFMAC
        self.cli_args["ifip"] = IFIP
        self.cli_args["ifport"] = IFPORT
        self.cli_args["ifbiosid"] = IFBIOSID
        try:
            self.quads_cli_call("addinterface")
        except CliException as ex:
            assert "Missing argument: speed" == str(ex)

    def test_define_interface_missing_vendor(self, remove_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME
        self.cli_args["ifmac"] = IFMAC
        self.cli_args["ifip"] = IFIP
        self.cli_args["ifport"] = IFPORT
        self.cli_args["ifbiosid"] = IFBIOSID
        self.cli_args["ifspeed"] = IFSPEED
        try:
            self.quads_cli_call("addinterface")
        except CliException as ex:
            assert "Missing argument: vendor" == str(ex)

    def test_define_interface(self, remove_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME
        self.cli_args["ifmac"] = IFMAC
        self.cli_args["ifip"] = IFIP
        self.cli_args["ifport"] = IFPORT
        self.cli_args["ifbiosid"] = IFBIOSID
        self.cli_args["ifspeed"] = IFSPEED
        self.cli_args["ifvendor"] = IFVENDOR

        self.quads_cli_call("addinterface")

        host = HostDao.get_host(HOST)
        assert len(host.interfaces) == 1
        assert host.interfaces[0].name == IFNAME
        assert host.interfaces[0].mac_address == IFMAC
        assert host.interfaces[0].switch_ip == IFIP
        assert host.interfaces[0].switch_port == IFPORT
        assert host.interfaces[0].bios_id == IFBIOSID
        assert host.interfaces[0].speed == IFSPEED
        assert host.interfaces[0].vendor == IFVENDOR
        assert not host.interfaces[0].pxe_boot
        assert not host.interfaces[0].maintenance

    def test_mod_interface(self, mod_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME
        self.cli_args["ifip"] = "192.168.0.1"

        self.quads_cli_call("modinterface")

        host = HostDao.get_host(HOST)
        assert len(host.interfaces) == 1
        assert host.interfaces[0].name == IFNAME
        assert host.interfaces[0].switch_ip == "192.168.0.1"
