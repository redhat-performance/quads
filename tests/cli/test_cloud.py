import logging
import pytest

from quads.server.dao.cloud import CloudDao
from tests.cli.config import RESPONSE_DEF_HOST, RESPONSE_RM_HOST, CLOUD
from tests.cli.test_base import TestBase


class TestCloud(TestBase):

    @pytest.fixture(scope="function")
    def setup(self):
        CloudDao.create_cloud(name=CLOUD)

    @pytest.fixture(scope="function")
    def teardown(self):
        CloudDao.remove_cloud(name=CLOUD)

    def test_define_cloud(self, teardown):
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
        assert self._caplog.text == RESPONSE_DEF_HOST

    def test_remove_cloud(self, setup):
        self.cli_args["cloud"] = CLOUD

        with self._caplog.at_level(logging.INFO, logger="test_logger"):
            self.quads_cli_call("rmcloud")
        assert self._caplog.text == RESPONSE_RM_HOST
