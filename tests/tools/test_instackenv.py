#!/usr/bin/env python3
import os

from quads.config import Config
from quads.tools.make_instackenv_json import make_env_json
from tests.tools.test_base import TestBase


class TestInstackenv(TestBase):
    async def test_make_instackenv_json(self):
        Config.__setattr__("openstack_management", True)
        Config.__setattr__("foreman_unavailable", True)
        cloud99_instackenv = await make_env_json("instackenv", "cloud99")
        assert list(cloud99_instackenv) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )

    async def test_make_ocpinventory_json(self):
        Config.__setattr__("openshift_management", True)
        Config.__setattr__("foreman_unavailable", True)
        cloud99_ocpinventory = await make_env_json("ocpinventory", "cloud99")
        assert list(cloud99_ocpinventory) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/cloud99_env.json"))
        )
