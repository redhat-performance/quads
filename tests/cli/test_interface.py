import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.models import db
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
        HOST, IFNAME, IFBIOSID, IFMAC, IFIP, IFPORT, IFSPEED, IFVENDOR, True, False
    )


@pytest.fixture
def noiface_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


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

    def test_rm_interface(self, mod_fixture):
        self.cli_args["host"] = HOST
        self.cli_args["ifname"] = IFNAME

        self.quads_cli_call("rminterface")

        host = HostDao.get_host(HOST)
        db.session.refresh(host)
        assert len(host.interfaces) == 0

    def test_ls_interface(self, mod_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("interface")

        assert self._caplog.messages[0] == f"interface: {IFNAME}"
        assert self._caplog.messages[1] == f"  bios id: {IFBIOSID}"
        assert self._caplog.messages[2] == f"  mac address: {IFMAC}"
        assert self._caplog.messages[3] == f"  switch ip: {IFIP}"
        assert self._caplog.messages[4] == f"  port: {IFPORT}"
        assert self._caplog.messages[5] == f"  speed: {IFSPEED}"
        assert self._caplog.messages[6] == f"  vendor: {IFVENDOR}"
        assert self._caplog.messages[7] == "  pxe_boot: True"
        assert self._caplog.messages[8] == "  maintenance: False"

    def test_ls_interface_missing_host(self, remove_fixture):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("interface")
        assert (
            str(ex.value)
            == "Missing option. --host option is required for --ls-interface."
        )

    def test_ls_interface_bad_host(self, remove_fixture):
        self.cli_args["host"] = "BADHOST"
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("interface")
        assert str(ex.value) == "Host not found: BADHOST"

    def test_ls_interface_noiface_host(self, noiface_fixture):
        self.cli_args["host"] = HOST
        self.quads_cli_call("interface")
        assert self._caplog.messages[0] == f"No interfaces defined for {HOST}"
