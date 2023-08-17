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
    assert HostDao.update_host(name=HOST, retired=True)


class TestRetired(TestBase):
    def test_mark_retired(self, mb_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("retire")

        assert self._caplog.messages[0] == f"Host {HOST} is now marked as retired"

        host = HostDao.get_host(HOST)
        assert host.retired

    def test_mark_retired_already(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("retire")

        assert (
            self._caplog.messages[0]
            == f"Host {HOST} has already been marked as retired"
        )

        host = HostDao.get_host(HOST)
        assert host.retired

    def test_mark_unretired(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("unretire")

        assert self._caplog.messages[0] == f"Host {HOST} is now marked as unretired"

        host = HostDao.get_host(HOST)
        assert not host.retired

    def test_mark_unretired_already(self, mb_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("unretire")

        assert (
            self._caplog.messages[0] == f"Host {HOST} has already been marked unretired"
        )

        host = HostDao.get_host(HOST)
        assert not host.retired

    def test_ls_retired(self, mr_fixture):
        self.cli_args["host"] = HOST

        self.quads_cli_call("ls_retired")

        assert self._caplog.messages[0] == HOST

        host = HostDao.get_host(HOST)
        assert host.retired
