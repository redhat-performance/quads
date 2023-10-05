import os.path
import pytest

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.disk import DiskDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.dao.memory import MemoryDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.models import db
from tests.cli.config import (
    HOST,
    CLOUD,
    MODEL,
    HOST_TYPE,
    IFNAME,
    IFBIOSID,
    IFMAC,
    IFIP,
    IFPORT,
    IFSPEED,
    IFVENDOR,
)
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    host_import = HostDao.get_host("imported.example.com")
    cloud = CloudDao.get_cloud(CLOUD)
    cloud_import = CloudDao.get_cloud("cloud42")
    default_cloud = CloudDao.get_cloud("cloud01")
    schedules = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

    if schedules:
        ScheduleDao.remove_schedule(schedules[0].id)
        AssignmentDao.remove_assignment(schedules[0].assignment_id)

    assignments = AssignmentDao.get_assignments()
    for ass in assignments:
        AssignmentDao.remove_assignment(ass.id)

    if host:
        HostDao.remove_host(name=HOST)

    if host_import:
        HostDao.remove_host(name="imported.example.com")

    if cloud_import:
        CloudDao.remove_cloud("cloud42")

    if cloud:
        CloudDao.remove_cloud(CLOUD)

    if default_cloud:
        CloudDao.remove_cloud("cloud01")


@pytest.fixture
def define_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.create_cloud(CLOUD)
    cloud_imported = CloudDao.create_cloud("cloud42")
    host = HostDao.create_host(HOST, MODEL, HOST_TYPE, CLOUD)
    host_import = HostDao.create_host("imported.example.com", MODEL, HOST_TYPE, CLOUD)
    InterfaceDao.create_interface(
        HOST, IFNAME, IFBIOSID, IFMAC, IFIP, IFPORT, IFSPEED, IFVENDOR, True, False
    )
    DiskDao.create_disk(HOST, "NVME", 4096, 10)
    DiskDao.create_disk(HOST, "SATA", 4096, 5)
    MemoryDao.create_memory(HOST, "DIMM1", 4096)


class TestExport(TestBase):
    def test_export(self, define_fixture):

        self.quads_cli_call("host_metadata_export")

        assert self._caplog.messages[0].startswith("Metadata successfully exported to ")
        filename = self._caplog.messages[0].split()[-1][:-1]
        assert os.path.exists(filename)
        with open(filename, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if not i.startswith("  created_at: "):
                    f.write(i)
            f.truncate()

        assert list(open(filename)) == list(
            open(os.path.join(os.path.dirname(__file__), "fixtures/metadata"))
        )


class TestImport(TestBase):
    def test_import(self, define_fixture):
        self.cli_args["metadata"] = os.path.join(
            os.path.dirname(__file__), "fixtures/metadata_import.yaml"
        )

        self.quads_cli_call("define_host_metadata")

        assert self._caplog.messages[0] == (
            "imported.example.com [RECREATING]: ['broken', 'disks', 'host_type', "
            "'interfaces', 'memory', 'model', 'retired']"
        )
        host = HostDao.get_host("imported.example.com")
        db.session.refresh(host)
        assert host.broken
        assert host.retired
        assert host.default_cloud.name == "cloud42"
        assert host.host_type == "imported"
        assert host.model == "IMPORTED"
        assert host.disks[0].disk_type == "NVME"
        assert host.disks[0].size_gb == 4096
        assert host.disks[0].count == 10
        assert host.disks[1].disk_type == "SATA"
        assert host.disks[1].size_gb == 4096
        assert host.disks[1].count == 5
        assert host.memory[0].handle == "DIMM1"
        assert host.memory[0].size_gb == 4096
        assert host.interfaces[0].name == "em1"
        assert host.interfaces[0].bios_id == "NIC.Intel.1"
        assert host.interfaces[0].mac_address == "A0:B1:C2:D3:E4:F5"
        assert not host.interfaces[0].maintenance
        assert host.interfaces[0].switch_ip == "10.0.0.1"
        assert host.interfaces[0].switch_port == "et-4:0/0"
        assert host.interfaces[0].speed == 1000
        assert host.interfaces[0].vendor == "Intel"
