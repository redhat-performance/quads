from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from quads.config import Config
from quads.exceptions import CliException
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from quads.server.models import db
from tests.cli.config import CLOUD, HOST2, HOST1, DEFAULT_CLOUD, MOD_CLOUD
from tests.cli.test_base import TestBase


def finalizer():
    cloud = CloudDao.get_cloud(CLOUD)
    host = HostDao.get_host(HOST2)
    schedules = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

    if schedules:
        ScheduleDao.remove_schedule(schedules[0].id)
        AssignmentDao.remove_assignment(schedules[0].assignment_id)


@pytest.fixture
def define_fixture(request):
    request.addfinalizer(finalizer)

    cloud = CloudDao.get_cloud(CLOUD)
    host = HostDao.get_host(HOST2)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id
    )


@pytest.fixture
def remove_fixture(request):
    request.addfinalizer(finalizer)

    today = datetime.now()
    tomorrow = today + timedelta(weeks=2)

    cloud = CloudDao.get_cloud(CLOUD)
    host = HostDao.get_host(HOST2)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    assignment = AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id
    )
    schedule = ScheduleDao.create_schedule(
        today.strftime("%Y-%m-%d %H:%M"),
        tomorrow.strftime("%Y-%m-%d %H:%M"),
        assignment,
        host,
    )
    assert schedule


class TestSchedule(TestBase):
    def test_add_schedule(self):
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        self.cli_args["schedstart"] = today.strftime("%Y-%m-%d %H:%M")
        self.cli_args["schedend"] = tomorrow.strftime("%Y-%m-%d %H:%M")
        self.cli_args["schedcloud"] = CLOUD
        self.cli_args["host"] = HOST2
        self.cli_args["omitcloud"] = None

        self.quads_cli_call("add_schedule")
        host = HostDao.get_host(HOST2)
        cloud = CloudDao.get_cloud(CLOUD)
        schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)
        assert schedule

    def test_remove_schedule(self, remove_fixture):
        host = HostDao.get_host(HOST2)
        cloud = CloudDao.get_cloud(CLOUD)
        schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        self.cli_args["schedid"] = schedule[0].id
        self.cli_args["host"] = HOST2

        self.quads_cli_call("rmschedule")
        schedule = ScheduleDao.get_schedule(int(self.cli_args["schedid"]))
        assert not schedule

    @patch.object(
        Config,
        "spare_pool_name",
        CLOUD,
    )
    def test_available(self, define_fixture):
        self.cli_args["schedstart"] = None
        self.cli_args["schedend"] = None
        self.cli_args["schedcloud"] = None
        self.cli_args["host"] = HOST2
        self.cli_args["omitcloud"] = None
        self.cli_args["filter"] = None

        self.quads_cli_call("available")
        assert self._caplog.messages[0] == f"{HOST2}"

    def test_mod_schedule(self, remove_fixture):
        host = HostDao.get_host(HOST2)
        cloud = CloudDao.get_cloud(CLOUD)
        _schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        today = datetime.now()
        atomorrow = today + timedelta(days=2)

        self.cli_args["schedid"] = _schedule[0].id
        self.cli_args["schedend"] = atomorrow.strftime("%Y-%m-%d %H:%M")

        self.quads_cli_call("modschedule")
        schedule_obj = ScheduleDao.get_schedule(_schedule[0].id)
        db.session.refresh(schedule_obj)

        assert schedule_obj.end.strftime("%Y-%m-%dT%H:%M") == atomorrow.strftime(
            "%Y-%m-%dT%H:%M"
        )

    def test_ls_schedule(self, remove_fixture):
        self.cli_args["host"] = HOST2
        self.quads_cli_call("schedule")
        assert self._caplog.messages[0] == f"Default cloud: {CLOUD}"
        assert self._caplog.messages[1] == f"Current cloud: {CLOUD}"
        assert self._caplog.messages[2].startswith("5| start=")

    def test_host(self, remove_fixture):
        self.cli_args["host"] = HOST2
        self.quads_cli_call("host")
        assert self._caplog.messages[0] == f"{CLOUD}"

    def test_ls_schedule_bad_host(self, remove_fixture):
        self.cli_args["host"] = "BADHOST"
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("schedule")

        assert str(ex.value) == f"Host not found: BADHOST"

    def test_ls_schedule_no_host(self, remove_fixture):
        if self.cli_args.get("host"):
            self.cli_args.pop("host")
        self.quads_cli_call("schedule")
        assert self._caplog.messages[0] == f"{DEFAULT_CLOUD}:"
        assert self._caplog.messages[1] == f"{MOD_CLOUD}:"
        assert self._caplog.messages[2] == f"{CLOUD}:"
        assert self._caplog.messages[3] == HOST1


class TestExtend(TestBase):
    def test_extend_schedule(self, remove_fixture):
        host = HostDao.get_host(HOST2)
        cloud = CloudDao.get_cloud(CLOUD)
        _schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        today = datetime.now()
        atomorrow = today + timedelta(weeks=4)

        self.cli_args["weeks"] = 2
        self.cli_args["host"] = HOST2

        self.quads_cli_call("extend")
        schedule_obj = ScheduleDao.get_schedule(_schedule[0].id)
        db.session.refresh(schedule_obj)

        assert schedule_obj.end.strftime("%Y-%m-%d %H:%M") == atomorrow.strftime(
            "%Y-%m-%d %H:%M"
        )


class TestShrink(TestBase):
    @patch("quads.cli.cli.input")
    def test_shrink_schedule(self, mock_input, remove_fixture):
        mock_input.return_value = "y"
        host = HostDao.get_host(HOST2)
        cloud = CloudDao.get_cloud(CLOUD)
        _schedule = ScheduleDao.get_current_schedule(host=host, cloud=cloud)

        today = datetime.now()
        atomorrow = today + timedelta(weeks=1)

        self.cli_args["weeks"] = 1
        self.cli_args["host"] = HOST2

        self.quads_cli_call("shrink")
        schedule_obj = ScheduleDao.get_schedule(_schedule[0].id)
        db.session.refresh(schedule_obj)

        assert schedule_obj.end.strftime("%Y-%m-%d %H:%M") == atomorrow.strftime(
            "%Y-%m-%d %H:%M"
        )
