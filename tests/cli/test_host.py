import pytest

from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
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

    def test_remove_host(self, remove_fixture):
        self.cli_args["host"] = HOST

        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        self.quads_cli_call("rmhost")

        host = HostDao.get_host(HOST)
        assert not host
