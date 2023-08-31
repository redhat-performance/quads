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
    HOST_TYPE,
    MODEL,
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
    HostDao.create_host(HOST, MODEL, HOST_TYPE, CLOUD)


@pytest.fixture
def mod_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, MODEL, HOST_TYPE, CLOUD)
    InterfaceDao.create_interface(
        HOST, IFNAME, IFBIOSID, IFMAC, IFIP, IFPORT, IFSPEED, IFVENDOR, False, False
    )


class TestInterface(TestBase):
    def test_define_disk(self, remove_fixture):
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
