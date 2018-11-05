#!/usr/bin/env python

import os
from quads.helpers import quads_load_config
from quads.foreman import Foreman

conf_file = os.path.join(os.path.dirname(__file__), "../conf/quads.yml")
conf = quads_load_config(conf_file)


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
