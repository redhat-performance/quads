import pytest

from quads.exceptions import CliException
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from tests.cli.config import (
    CLOUD,
    HOST1,
    HOST2,
)
from tests.cli.test_base import TestBase


class TestDisk(TestBase):
    def test_ls_disk(self):
        self.cli_args["host"] = HOST1

        self.quads_cli_call("disks")

        assert self._caplog.messages[0] == f"disk0:"
        assert self._caplog.messages[1] == f"  type: NVME"
        assert self._caplog.messages[2] == f"  size: 4096"
        assert self._caplog.messages[3] == f"  count: 10"
        assert self._caplog.messages[4] == f"disk1:"
        assert self._caplog.messages[5] == f"  type: SATA"
        assert self._caplog.messages[6] == f"  size: 4096"
        assert self._caplog.messages[7] == f"  count: 5"

    def test_ls_disk_missing_host(self):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("disks")
        assert (
            str(ex.value) == "Missing option. --host option is required for --ls-disks."
        )

    def test_ls_disk_bad_host(self):
        self.cli_args["host"] = "BADHOST"
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("disks")
        assert str(ex.value) == "Host not found: BADHOST"

    def test_ls_disk_nodisk_host(self):
        self.cli_args["host"] = HOST2
        self.quads_cli_call("disks")
        assert self._caplog.messages[0] == f"No disks defined for {HOST2}"
