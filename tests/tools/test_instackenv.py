#!/usr/bin/env python3
import os

from quads.config import Config
from quads.tools.make_instackenv_json import main
from tests.tools.test_base import TestBase


class TestInstackenv(TestBase):
    def test_make_instackenv_json(self):
        Config.__setattr__("openstack_management", True)
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("json_web_path", os.path.join(os.path.dirname(__file__), "artifacts/"))
        main()
        assert list(open(os.path.join(os.path.dirname(__file__), "artifacts/cloud99_instackenv.json"))) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )

    def test_make_ocpinventory_json(self):
        Config.__setattr__("openshift_management", True)
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("json_web_path", os.path.join(os.path.dirname(__file__), "artifacts/"))
        main()
        assert list(open(os.path.join(os.path.dirname(__file__), "artifacts/cloud99_ocpinventory.json"))) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )
