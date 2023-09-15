import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.memory import MemoryDao
from tests.cli.config import (
    HOST,
    CLOUD,
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
    MemoryDao.create_memory(HOST, "DIMM1", 2048)
    MemoryDao.create_memory(HOST, "DIMM2", 2048)


@pytest.fixture
def nomem_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


class TestMemory(TestBase):
    def test_ls_memory(self, mod_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("memory")

        assert self._caplog.messages[0] == f"memory: DIMM1"
        assert self._caplog.messages[1] == f"  size: 2048"
        assert self._caplog.messages[2] == f"memory: DIMM2"
        assert self._caplog.messages[3] == f"  size: 2048"

    def test_ls_memory_missing_host(self, remove_fixture):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("memory")
        assert (
            str(ex.value)
            == "Missing option. --host option is required for --ls-memory."
        )

    def test_ls_memory_bad_host(self, remove_fixture):
        self.cli_args["host"] = "BADHOST"
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("memory")
        assert str(ex.value) == "Host not found: BADHOST"

    def test_ls_memory_nomem_host(self, nomem_fixture):
        self.cli_args["host"] = HOST
        self.quads_cli_call("memory")
        assert self._caplog.messages[0] == f"No memory defined for {HOST}"
