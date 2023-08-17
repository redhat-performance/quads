import pytest

from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from tests.cli.config import CLOUD, HOST
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    if host:
        HostDao.remove_host(HOST)
    cloud = CloudDao.get_cloud(CLOUD)
    if cloud:
        CloudDao.remove_cloud(name=CLOUD)


@pytest.fixture
def mb_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)


@pytest.fixture
def mr_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    assert HostDao.update_host(name=HOST, broken=True)


class TestBroken(TestBase):
    def test_mark_broken(self, mb_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("mark_broken")

        assert self._caplog.messages[0] == f"Host {HOST} is now marked as broken"

        host = HostDao.get_host(HOST)
        assert host.broken

    def test_mark_broken_already(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("mark_broken")

        assert self._caplog.messages[0] == f"Host {HOST} has already been marked broken"

        host = HostDao.get_host(HOST)
        assert host.broken

    def test_mark_repaired(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("mark_repaired")

        assert self._caplog.messages[0] == f"Host {HOST} is now marked as repaired"

        host = HostDao.get_host(HOST)
        assert not host.broken

    def test_mark_repaired_not_broken(self, mb_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("mark_repaired")

        assert (
            self._caplog.messages[0] == f"Host {HOST} has already been marked repaired"
        )

        host = HostDao.get_host(HOST)
        assert not host.broken

    def test_ls_broken(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("ls_broken")

        assert self._caplog.messages[0] == HOST

        host = HostDao.get_host(HOST)
        assert host.broken
