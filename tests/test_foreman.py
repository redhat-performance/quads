#!/usr/bin/env python3
import asyncio
import pytest

from quads.config import conf
from quads.tools.foreman import Foreman


class TestForeman(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.foreman = Foreman(
            conf["foreman_api_url"],
            conf["ipmi_username"],
            conf["ipmi_password"],
            loop=loop,
        )

    def teardown(self):
        self.foreman.loop.close()

    def test_get_all_hosts(self):
        hosts = self.foreman.loop.run_until_complete(self.foreman.get_all_hosts())
        assert isinstance(hosts, dict)

    def test_get_broken_hosts(self):
        hosts = self.foreman.loop.run_until_complete(self.foreman.get_broken_hosts())
        assert isinstance(hosts, dict)
