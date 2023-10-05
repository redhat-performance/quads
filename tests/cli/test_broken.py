import pytest

from quads.server.dao.host import HostDao
from tests.cli.config import HOST1
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST1)
    if host:
        HostDao.update_host(name=HOST1, broken=False)


@pytest.fixture
def mr_fixture(request):
    request.addfinalizer(finalizer)
    assert HostDao.update_host(name=HOST1, broken=True)


class TestBroken(TestBase):
    def test_mark_broken(self):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("mark_broken")

        assert self._caplog.messages[0] == f"Host {HOST1} is now marked as broken"

        host = HostDao.get_host(HOST1)
        assert host.broken

    def test_mark_broken_already(self, mr_fixture):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("mark_broken")

        assert (
            self._caplog.messages[0] == f"Host {HOST1} has already been marked broken"
        )

        host = HostDao.get_host(HOST1)
        assert host.broken

    def test_mark_repaired(self, mr_fixture):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("mark_repaired")

        assert self._caplog.messages[0] == f"Host {HOST1} is now marked as repaired"

        host = HostDao.get_host(HOST1)
        assert not host.broken

    def test_mark_repaired_not_broken(self):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("mark_repaired")

        assert (
            self._caplog.messages[0] == f"Host {HOST1} has already been marked repaired"
        )

        host = HostDao.get_host(HOST1)
        assert not host.broken

    def test_ls_broken(self, mr_fixture):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("ls_broken")

        assert self._caplog.messages[0] == HOST1

        host = HostDao.get_host(HOST1)
        assert host.broken
