import logging
import pytest

from quads.server.dao.cloud import CloudDao
from tests.cli.config import RESPONSE_RM, CLOUD
from tests.cli.test_base import TestBase


@pytest.fixture
def resource(request):
    def finalizer():
        cloud = CloudDao.get_cloud(CLOUD)
        if cloud:
            CloudDao.remove_cloud(name=CLOUD)

    request.addfinalizer(finalizer)

    CloudDao.create_cloud(name=CLOUD)


class TestCloud(TestBase):
    def test_define_cloud(self, define_fixture):
        self.cli_args["cloudresource"] = CLOUD
        self.cli_args["description"] = "Test cloud"
        self.cli_args["cloudowner"] = "scalelab"
        self.cli_args["ccusers"] = None
        self.cli_args["qinq"] = None
        self.cli_args["cloudticket"] = "1225"
        self.cli_args["force"] = True
        self.cli_args["wipe"] = True

        with self._caplog.at_level(logging.INFO, logger="test_logger"):
            self.quads_cli_call("cloudresource")
        cloud = CloudDao.get_cloud(CLOUD)
        assert cloud is not None
        assert cloud.name == CLOUD

    def test_remove_cloud(self, define_fixture):
        self.cli_args["cloud"] = CLOUD

        with self._caplog.at_level(logging.INFO, logger="test_logger"):
            self.quads_cli_call("rmcloud")
        assert self._caplog.text == RESPONSE_RM
