import logging

from tests.cli.config import RESPONSE_LS
from tests.cli.test_base import TestBase


class TestLs(TestBase):

    def test_host(self):
        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("ls_hosts")
        assert self._caplog.messages[0] == RESPONSE_LS

    def test_cloud(self):
        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("ls_clouds")
        assert self._caplog.messages[0] == RESPONSE_LS
