import logging

import pytest

from quads.server.dao.host import HostDao
from tests.cli.config import RESPONSE_DEF_HOST, RESPONSE_RM_HOST, HOST, CLOUD
from tests.cli.test_base import TestBase


class TestHost(TestBase):

    @pytest.fixture(scope="function")
    def setup(self):
        HostDao.create_host(name=HOST)

    @pytest.fixture(scope="function")
    def teardown(self):
        HostDao.remove_host(name=HOST)

    def test_define_host(self):
        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = "scalelab"
        self.cli_args["model"] = "r640"

        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("hostresource")
        assert self._caplog.messages[0] == RESPONSE_DEF_HOST

    def test_remove_host(self):
        self.cli_args["host"] = HOST

        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("rmhost")
        assert self._caplog.messages[0] == RESPONSE_RM_HOST
