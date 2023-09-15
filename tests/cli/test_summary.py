from datetime import timedelta, datetime

import pytest

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from tests.cli.config import CLOUD, HOST
from tests.cli.test_base import TestBase


def finalizer():
    host = HostDao.get_host(HOST)
    cloud = CloudDao.get_cloud(CLOUD)
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
        CloudDao.remove_cloud("cloud03")


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    cloud = CloudDao.create_cloud(CLOUD)
    cloud03 = CloudDao.create_cloud("cloud03")
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


class TestSummary(TestBase):
    def test_summary_all_detail(self, remove_fixture):
        self.cli_args["all"] = True
        self.cli_args["detail"] = True
        self.quads_cli_call("summary")

        assert self._caplog.messages[0] == "cloud99 (test): 1 (test) - 1234"
        assert self._caplog.messages[1] == "cloud03 (): 0 () - "

    def test_summary(self, remove_fixture):
        self.cli_args["all"] = False
        self.cli_args["detail"] = False
        self.quads_cli_call("summary")

        assert len(self._caplog.messages) == 1
        assert self._caplog.messages[0] == "cloud99: 1 (test)"
