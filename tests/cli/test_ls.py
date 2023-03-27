from tests.cli.test_base import TestBase


class TestLs(TestBase):
    def test_host(self):

        self.quads_cli_call("ls_hosts")
