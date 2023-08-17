import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.dao.memory import MemoryDao
from quads.server.dao.processor import ProcessorDao
from tests.cli.config import HOST, CLOUD
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    if host:
        HostDao.remove_host(name=HOST)
    cloud = CloudDao.get_cloud(CLOUD)
    if cloud:
        CloudDao.remove_cloud(CLOUD)


@pytest.fixture
def define_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


class TestHost(TestBase):
    def test_define_host(self, define_fixture):
        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = "scalelab"
        self.cli_args["model"] = "r640"

        self.quads_cli_call("hostresource")

        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        assert self._caplog.messages[0] == HOST

    def test_define_host_missing_model(self, define_fixture):
        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = "scalelab"

        try:
            self.quads_cli_call("hostresource")
        except CliException as ex:
            assert str(ex) == "Missing argument: model"

    def test_remove_host(self, remove_fixture):
        self.cli_args["host"] = HOST

        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        self.quads_cli_call("rmhost")

        host = HostDao.get_host(HOST)
        assert not host

    def test_ls_host(self, remove_fixture):
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == HOST

    def test_ls_processors(self, remove_fixture):
        self.cli_args["host"] = HOST
        ProcessorDao.create_processor(HOST, "P1", "Intel", "i7", 2, 4)
        self.quads_cli_call("processors")

        assert self._caplog.messages[0] == "processor: P1"
        assert self._caplog.messages[1] == "  vendor: Intel"
        assert self._caplog.messages[2] == "  product: i7"
        assert self._caplog.messages[3] == "  cores: 2"
        assert self._caplog.messages[4] == "  threads: 4"

    def test_ls_memory(self, remove_fixture):
        self.cli_args["host"] = HOST
        MemoryDao.create_memory(HOST, "DIMM1", 2000)
        MemoryDao.create_memory(HOST, "DIMM2", 2000)
        self.quads_cli_call("memory")

        assert self._caplog.messages[0] == "memory: DIMM1"
        assert self._caplog.messages[1] == "  size: 2000"
        assert self._caplog.messages[2] == "memory: DIMM2"
        assert self._caplog.messages[3] == "  size: 2000"

    def test_ls_interface(self, remove_fixture):
        self.cli_args["host"] = HOST
        InterfaceDao.create_interface(
            HOST,
            "em1",
            "Int.Nic.1",
            "A0:B1:C2:D4",
            "10.0.0.1",
            "ex-0/1/0",
            1000,
            "Intel",
            True,
            False,
        )
        self.quads_cli_call("interface")

        assert self._caplog.messages[0] == "interface: em1"
        assert self._caplog.messages[1] == "  bios id: Int.Nic.1"
        assert self._caplog.messages[2] == "  mac address: A0:B1:C2:D4"
        assert self._caplog.messages[3] == "  switch ip: 10.0.0.1"
        assert self._caplog.messages[4] == "  port: ex-0/1/0"
        assert self._caplog.messages[5] == "  speed: 1000"
        assert self._caplog.messages[6] == "  vendor: Intel"
        assert self._caplog.messages[7] == "  pxe_boot: True"
        assert self._caplog.messages[8] == "  maintenance: False"
