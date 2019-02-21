#!/usr/bin/env python

from quads.config import conf
from quads.tools.foreman import Foreman


class TestForeman(object):
    def setup(self):
        self.foreman = Foreman(
            conf["foreman_api_url"],
            conf["ipmi_username"],
            conf["ipmi_password"],
        )

    def test_get_all_hosts(self):
        hosts = self.foreman.get_all_hosts()
        assert isinstance(hosts, type(dict))

    def test_get_broken_hosts(self):
        hosts = self.foreman.get_broken_hosts()
        assert isinstance(hosts, type(dict))
