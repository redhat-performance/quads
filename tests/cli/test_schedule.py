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


@pytest.fixture
def define_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], vlan.vlan_id, cloud.name)


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST, "r640", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan("192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1)
    assignment = AssignmentDao.create_assignment("test", "test", "1234", 0, False, [""], vlan.vlan_id, cloud.name)
    ScheduleDao.create_schedule(today.strftime("%Y-%m-%d %H:%M"), tomorrow.strftime("%Y-%m-%d %H:%M"),assignment, host)


class TestHost(TestBase):
    def test_add_schedule(self, define_fixture):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        self.cli_args["schedstart"] = today.strftime("%Y-%m-%d %H:%M")
        self.cli_args["schedend"] = tomorrow.strftime("%Y-%m-%d %H:%M")
        self.cli_args["schedcloud"] = CLOUD
        self.cli_args["host"] = HOST
        self.cli_args["omitcloud"] = None

        self.quads_cli_call("add_schedule")
        host = HostDao.get_host(HOST)
        cloud = CloudDao.get_cloud(CLOUD)
        schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)
        assert schedule

    def test_remove_schedule(self, remove_fixture):
        host = HostDao.get_host(HOST)
        cloud = CloudDao.get_cloud(CLOUD)
        schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        self.cli_args["schedid"] = schedule[0].id
        self.cli_args["host"] = HOST

        self.quads_cli_call("rmschedule")
        schedule = ScheduleDao.get_schedule(self.cli_args["schedid"])
        assert not schedule

    def test_ls_schedule(self, remove_fixture):
        # TODO: fix this
        self.cli_args["host"] = HOST
        self.quads_cli_call("schedule")
        assert self._caplog.messages[0] == 'Default cloud: cloud99'
