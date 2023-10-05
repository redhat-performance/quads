import pytest
import os
import glob

from datetime import datetime, timedelta

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from quads.tools.simple_table_web import main as web_main
from tests.cli.config import CLOUD, HOST1
from tests.tools.test_base import TestBase


def finalizer():
    for schedule in ScheduleDao.get_schedules():
        ScheduleDao.remove_schedule(schedule.id)

    for assignment in AssignmentDao.get_assignments():
        AssignmentDao.remove_assignment(assignment.id)

    for host in HostDao.get_hosts():
        HostDao.remove_host(host.name)

    for cloud in CloudDao.get_clouds():
        CloudDao.remove_cloud(cloud.name)

    for f in glob.glob("artifacts/*.html"):
        os.remove(f)


@pytest.fixture
def table_fixture(request):
    request.addfinalizer(finalizer)
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    finalizer()
    cloud = CloudDao.create_cloud(CLOUD)
    host = HostDao.create_host(HOST1, "r640", "scalelab", CLOUD)
    vlan = VlanDao.create_vlan(
        "192.168.1.1", 122, "192.168.1.1/22", "255.255.255.255", 1
    )
    assignment = AssignmentDao.create_assignment(
        "test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id
    )
    schedule = ScheduleDao.create_schedule(
        today,
        tomorrow,
        assignment,
        host,
    )
    assert schedule


class TestTable(TestBase):
    def test_simple_table_web(self, table_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "visual_web_dir", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        web_main()
        current = open(os.path.join(os.path.dirname(__file__), "artifacts/current.html"), 'r')
        current = [n for n in current.readlines() if 'Emoji' not in n]
        current = "".join(current)
        response = f"""title=
        "Description: test
        Env: cloud99
        Owner: test
        Ticket: 1234
        Day: {datetime.now().day + 1}">"""
        assert isinstance(current, str) is True
        assert response in current

