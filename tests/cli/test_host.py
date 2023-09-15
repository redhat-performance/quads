import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.memory import MemoryDao
from quads.server.dao.processor import ProcessorDao
from tests.cli.config import HOST, CLOUD, MODEL, HOST_TYPE
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
    HostDao.create_host(HOST, MODEL, HOST_TYPE, CLOUD)
    HostDao.create_host("NEWHOST.example.com", "NEWMODEL", HOST_TYPE, CLOUD)


class TestHost(TestBase):
    def test_define_host(self, define_fixture):
        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = HOST_TYPE
        self.cli_args["model"] = MODEL

        self.quads_cli_call("hostresource")

        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        assert self._caplog.messages[0] == HOST

    def test_define_host_missing_model(self, define_fixture):
        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = HOST_TYPE

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

        assert self._caplog.messages[0] == "NEWHOST.example.com"
        assert self._caplog.messages[1] == HOST

    def test_ls_host_filter(self, remove_fixture):
        self.cli_args["filter"] = f"model=={MODEL}"
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == HOST
        assert len(self._caplog.messages) == 1

    def test_ls_no_host(self):
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == "No hosts found."

    def test_ls_processors(self, remove_fixture):
        self.cli_args["host"] = HOST
        ProcessorDao.create_processor(HOST, "P1", "Intel", "i7", 2, 4)
        self.quads_cli_call("processors")

        assert self._caplog.messages[0] == "processor: P1"
        assert self._caplog.messages[1] == "  vendor: Intel"
        assert self._caplog.messages[2] == "  product: i7"
        assert self._caplog.messages[3] == "  cores: 2"
        assert self._caplog.messages[4] == "  threads: 4"

    def test_ls_processors_no_host(self, remove_fixture):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("processors")

        assert (
            str(ex.value)
            == "Missing option. --host option is required for --ls-processors."
        )

    def test_ls_processors_no_processor(self, remove_fixture):
        self.cli_args["host"] = HOST
        self.quads_cli_call("processors")

        assert self._caplog.messages[0] == f"No processors defined for {HOST}"

    def test_ls_memory(self, remove_fixture):
        self.cli_args["host"] = HOST
        MemoryDao.create_memory(HOST, "DIMM1", 2000)
        MemoryDao.create_memory(HOST, "DIMM2", 2000)
        self.quads_cli_call("memory")

        assert self._caplog.messages[0] == "memory: DIMM1"
        assert self._caplog.messages[1] == "  size: 2000"
        assert self._caplog.messages[2] == "memory: DIMM2"
        assert self._caplog.messages[3] == "  size: 2000"
