import logging

from tests.cli.config import RESPONSE_DEF_HOST, RESPONSE_RM_HOST
from tests.cli.test_base import TestBase


class TestHost(TestBase):

    def test_define_host(self):
        self.cli_args["hostresource"] = "host9.example.com"
        self.cli_args["hostcloud"] = "cloud01"
        self.cli_args["hosttype"] = "scalelab"
        self.cli_args["model"] = "r640"

        with self._caplog.at_level(logging.INFO, logger="test.cli.test_base"):
            self.quads_cli_call("hostresource")
        assert self._caplog.text == RESPONSE_DEF_HOST

    def test_remove_host(self):
        self.cli_args["host"] = "host9.example.com"

        with self._caplog.at_level(logging.INFO, logger="test.cli.test_base"):
            self.quads_cli_call("rmhost")
        assert self._caplog.text == RESPONSE_RM_HOST
