import logging
import pytest

from datetime import datetime, timedelta
from unittest.mock import patch

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from tests.cli.config import CLOUD, HOST1
from quads.tools.notify import main as notify_main
from tests.tools.test_base import TestBase, _logger
from tests.tools.test_validate_env import NetcatStub


def finalizer():
    for schedule in ScheduleDao.get_schedules():
        ScheduleDao.remove_schedule(schedule.id)

    for assignment in AssignmentDao.get_assignments():
        AssignmentDao.remove_assignment(assignment.id)

    for host in HostDao.get_hosts():
        HostDao.remove_host(host.name)

    for cloud in CloudDao.get_clouds():
        CloudDao.remove_cloud(cloud.name)


@pytest.fixture
def notify_fixture(request):
    request.addfinalizer(finalizer)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    finalizer()
    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST1, "r640", "scalelab", CLOUD)
    host2 = HostDao.create_host("host2.example.com", "r750", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    assignment = AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id
    )
    assignment2 = AssignmentDao.create_assignment(
        "test2", "test", "1235", 0, False, [""], cloud.name, vlan.vlan_id

    )
    schedule = ScheduleDao.create_schedule(
        today,
        tomorrow,
        assignment,
        host,
    )
    schedule2 = ScheduleDao.create_schedule(
        today + timedelta(days=3),
        tomorrow + timedelta(days=7),
        assignment2,
        host2,
    )
    assert schedule
    assert schedule2


class TestNotify(TestBase):
    @patch("quads.tools.external.postman.SMTP")
    def test_notify_not_validated(self, mocked_smtp, notify_fixture):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()
        self._caplog.set_level(logging.INFO)
        notify_main(_logger=_logger)

        cloud = CloudDao.get_cloud(name="cloud99")
        notification_obj = AssignmentDao.filter_assignments({"cloud_id": cloud.id})[0].notification
        assert notification_obj.pre_initial is True
        assert self._caplog.messages == ["=============== Future Initial Message"]

    @patch("quads.tools.notify.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_notify_validated(self, mocked_smtp, notify_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("webhook_notify", True)
        mocked_smtp()
        cloud = CloudDao.get_cloud(name="cloud99")
        assignments = AssignmentDao.filter_assignments({"cloud_id": cloud.id})
        for assignment in assignments:
            setattr(assignment, "validated", True)
            BaseDao.safe_commit()

        self._caplog.set_level(logging.INFO)
        notify_main(_logger=_logger)

        notification_obj = assignments[0].notification
        assert notification_obj.pre_initial is True
        assert notification_obj.pre is True
        assert notification_obj.initial is True
        assert self._caplog.messages == [
            "=============== Initial Message",
            "Beep boop we can't communicate with your webhook.",
            "=============== Additional Message",
            "=============== Future Initial Message",
            "=============== Additional Message"
        ]
