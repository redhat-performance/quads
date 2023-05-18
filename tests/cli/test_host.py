import logging

import pytest

from quads.server import app
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from tests.cli.config import RESPONSE_DEF_HOST, RESPONSE_RM, HOST, CLOUD, RESPONSE_LS
from tests.cli.test_base import TestBase


class TestHost(TestBase):

    def test_define_host(self):
        def setup():
            CloudDao.create_cloud(CLOUD)

        def teardown():
            HostDao.remove_host(name=HOST)
            CloudDao.remove_cloud(CLOUD)

        setup()

        self.cli_args["hostresource"] = HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = "scalelab"
        self.cli_args["model"] = "r640"

        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("hostresource")
        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        # teardown()

    def test_ls_host(self):
        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("ls_hosts")
        assert self._caplog.messages[0] == RESPONSE_LS

    def test_remove_host(self, ):
        def setup():
            CloudDao.create_cloud(CLOUD)
            HostDao.create_host(HOST, "r640", "scalelab", CLOUD)

        setup()

        self.cli_args["host"] = HOST

        host = HostDao.get_host(HOST)
        assert host is not None
        assert host.name == HOST

        with self._caplog.at_level(logging.INFO, logger="test_log"):
            self.quads_cli_call("rmhost")

        host = HostDao.get_host(HOST)
        assert not host

