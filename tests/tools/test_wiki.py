import pytest
import os

from datetime import datetime, timedelta
from unittest.mock import patch

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from tests.cli.config import CLOUD, HOST1
from quads.tools.regenerate_wiki import main as regenerate_wiki_main
from tests.tools.test_base import TestBase


class WikiStub:
    def __init__(self, url, username, password):
        pass

    def update(self, _page_title, _page_id, _markdown):
        pass


def finalizer():
    for schedule in ScheduleDao.get_schedules():
        ScheduleDao.remove_schedule(schedule.id)

    assignments = AssignmentDao.get_assignments()
    for ass in assignments:
        AssignmentDao.remove_assignment(ass.id)

    for host in HostDao.get_hosts():
        HostDao.remove_host(host.name)

    cloud = CloudDao.get_cloud(CLOUD)
    if cloud:
        CloudDao.remove_cloud(CLOUD)


@pytest.fixture
def wiki_fixture(request):
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


class TestWiki(TestBase):
    @patch("quads.tools.regenerate_wiki.Wiki", WikiStub)
    @patch("quads.tools.regenerate_vlans_wiki.Wiki", WikiStub)
    def test_regenerate_wiki(self, wiki_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "wp_wiki_git_repo_path", os.path.join(os.path.dirname(__file__), "artifacts/git/wiki")
        )
        regenerate_wiki_main()

        files = ["assignments.md", "main.md"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{f}"))

        assignment_md = open(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{files[0]}"), 'r')
        assignment_md = "".join(assignment_md.readlines())
        host_assignment_str = "| host1 | <a href=http://mgmt-host1.example.com/ target=_blank>console</a> |\n"
        assert host_assignment_str in assignment_md
