import pytest

from quads.exceptions import CliException
from quads.server.dao.host import HostDao
from quads.server.models import db
from tests.cli.config import (
    CLOUD,
    HOST_TYPE,
    DEFINE_HOST,
    MODEL1,
    HOST1,
    IFIP1,
    HOST2,
)
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(DEFINE_HOST)
    if host:
        HostDao.remove_host(name=DEFINE_HOST)


@pytest.fixture
def remove_host(request):
    finalizer()
    request.addfinalizer(finalizer)


@pytest.fixture
def add_host(request):
    host = HostDao.create_host(DEFINE_HOST, MODEL1, HOST_TYPE, CLOUD)
    assert host


class TestHost(TestBase):
    def test_define_host(self, remove_host):
        self.cli_args["hostresource"] = DEFINE_HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = HOST_TYPE
        self.cli_args["model"] = MODEL1

        self.quads_cli_call("hostresource")

        host = HostDao.get_host(DEFINE_HOST)
        assert host is not None
        assert host.name == DEFINE_HOST

        assert self._caplog.messages[0] == DEFINE_HOST

    def test_define_host_missing_model(self, remove_host):
        self.cli_args["hostresource"] = DEFINE_HOST
        self.cli_args["hostcloud"] = CLOUD
        self.cli_args["hosttype"] = HOST_TYPE

        try:
            self.quads_cli_call("hostresource")
        except CliException as ex:
            assert str(ex) == "Missing argument: model"

    def test_remove_host(self, add_host):
        self.cli_args["host"] = DEFINE_HOST

        host = HostDao.get_host(DEFINE_HOST)
        assert host is not None
        assert host.name == DEFINE_HOST

        self.quads_cli_call("rmhost")

        host = HostDao.get_host(DEFINE_HOST)
        assert not host

    def test_ls_host(self):
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == HOST1
        assert self._caplog.messages[1] == HOST2

    def test_ls_host_filter(self):
        self.cli_args["filter"] = f"model=={MODEL1}"
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == HOST1
        assert len(self._caplog.messages) == 1

    def test_ls_host_filter_interface(self):
        self.cli_args["filter"] = f"interfaces.switch_ip=={IFIP1}"
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == HOST1
        assert len(self._caplog.messages) == 1

    def test_ls_host_filter_bad_interface(self):
        self.cli_args["filter"] = f"interfaces.switch_ip==10.99.99.5"
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == "No hosts found."

    def test_ls_no_host(self):
        self.quads_cli_call("ls_hosts")

        assert self._caplog.messages[0] == "No hosts found."

    def test_ls_processors(self):
        self.cli_args["host"] = HOST1
        self.quads_cli_call("processors")

        assert self._caplog.messages[0] == "processor: P1"
        assert self._caplog.messages[1] == "  vendor: Intel"
        assert self._caplog.messages[2] == "  product: i7"
        assert self._caplog.messages[3] == "  cores: 2"
        assert self._caplog.messages[4] == "  threads: 4"

    def test_ls_processors_no_host(self):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("processors")

        assert (
            str(ex.value)
            == "Missing option. --host option is required for --ls-processors."
        )

    def test_ls_processors_no_processor(self):
        self.cli_args["host"] = HOST2
        self.quads_cli_call("processors")

        assert self._caplog.messages[0] == f"No processors defined for {HOST2}"

    def test_ls_memory(self):
        self.cli_args["host"] = HOST1
        self.quads_cli_call("memory")

        assert self._caplog.messages[0] == "memory: DIMM1"
        assert self._caplog.messages[1] == "  size: 2048"
        assert self._caplog.messages[2] == "memory: DIMM2"
        assert self._caplog.messages[3] == "  size: 2048"
