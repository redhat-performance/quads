import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.disk import DiskDao
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
    DiskDao.create_disk(HOST, "NVME", 4096, 10)
    DiskDao.create_disk(HOST, "SATA", 4096, 5)
    MemoryDao.create_memory(HOST, "DIMM1", 2048)
    MemoryDao.create_memory(HOST, "DIMM2", 2048)


@pytest.fixture
def nodisk_fixture(request):
    request.addfinalizer(finalizer)

    CloudDao.create_cloud(CLOUD)
    HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


class TestDisk(TestBase):
    def test_ls_disk(self, mod_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("disks")

        assert self._caplog.messages[0] == f"disk0:"
        assert self._caplog.messages[1] == f"  type: NVME"
        assert self._caplog.messages[2] == f"  size: 4096"
        assert self._caplog.messages[3] == f"  count: 10"
        assert self._caplog.messages[4] == f"disk1:"
        assert self._caplog.messages[5] == f"  type: SATA"
        assert self._caplog.messages[6] == f"  size: 4096"
        assert self._caplog.messages[7] == f"  count: 5"

    def test_ls_disk_missing_host(self, remove_fixture):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("disks")
        assert (
            str(ex.value) == "Missing option. --host option is required for --ls-disks."
        )

    def test_ls_disk_bad_host(self, remove_fixture):
        self.cli_args["host"] = "BADHOST"
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("disks")
        assert str(ex.value) == "Host not found: BADHOST"

    def test_ls_disk_nodisk_host(self, nodisk_fixture):
        self.cli_args["host"] = HOST
        self.quads_cli_call("disks")
        assert self._caplog.messages[0] == f"No disks defined for {HOST}"
