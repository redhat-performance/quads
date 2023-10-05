from datetime import datetime, timedelta

import pytest

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from tests.cli.config import HOST, CLOUD
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    cloud = CloudDao.get_cloud(CLOUD)
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

    if cloud:
        CloudDao.remove_cloud(CLOUD)

    if default_cloud:
        CloudDao.remove_cloud("cloud01")


@pytest.fixture
def define_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], vlan.vlan_id, cloud.name
    )


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    today = datetime.now()
    tomorrow = today + timedelta(weeks=2)

    cloud = CloudDao.create_cloud(CLOUD)
    default_cloud = CloudDao.create_cloud("cloud01")
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    assignment = AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], vlan.vlan_id, cloud.name
    )
    schedule = ScheduleDao.create_schedule(
        today.strftime("%Y-%m-%d %H:%M"),
        tomorrow.strftime("%Y-%m-%d %H:%M"),
        assignment,
        host,
    )
    assert schedule


class TestReport(TestBase):
    def test_report_available(self, define_fixture):
        self.quads_cli_call("report_available")
        assert self._caplog.messages[0].startswith("QUADS report for ")
        assert self._caplog.messages[1] == "Percentage Utilized: 0%"
        assert (
            self._caplog.messages[2]
            == "Server Type | Total|  Free| Scheduled| 2 weeks| 4 weeks"
        )
        assert (
            self._caplog.messages[3]
            == "host        |     1|     1|        0%|       1|       1"
        )
