from unittest.mock import patch, MagicMock

import pytest
from quads.tools.external.ssh_helper import SSHHelper
from tempfile import NamedTemporaryFile
from getpass import getuser

from tests.tools.test_base import TestBase


class TestSSHHelper(TestBase):
    string = "test"

    @pytest.fixture(autouse=True)
    def setup(self):
        tmp = NamedTemporaryFile(delete=False)
        with open(tmp.name, "w") as _file:
            _file.write(self.string)
        self.tmp_file = tmp.name

    def teardown(self):
        self.helper.disconnect()

    def test_run_cmd(self):
        self.helper = SSHHelper(_host="localhost", _user=getuser())

        out = self.helper.run_cmd(f"cat {self.tmp_file}")
        assert out[0]
        assert out[1][0] == 'test'
