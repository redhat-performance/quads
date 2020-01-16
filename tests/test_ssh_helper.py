#!/usr/bin/env python3

from quads.tools.ssh_helper import SSHHelper
from tempfile import NamedTemporaryFile
from getpass import getuser


class TestSSHHelper(object):
    string = "test"

    def setup(self):
        self.helper = SSHHelper(_host="localhost", _user=getuser())
        tmp = NamedTemporaryFile(delete=False)
        with open(tmp.name, "w") as _file:
            _file.write(self.string)
        self.tmp_file = tmp.name

    def teardown(self):
        self.helper.disconnect()

    def test_run_cmd(self):
        out = self.helper.run_cmd(f"cat {self.tmp_file}")
        assert out == self.string
