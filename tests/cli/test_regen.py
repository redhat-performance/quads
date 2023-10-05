import pytest
import os
import glob

from datetime import datetime, timedelta
from unittest.mock import patch

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from tests.cli.config import CLOUD, HOST1
from tests.cli.test_base import TestBase
from tests.tools.test_wiki import WikiStub


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
    for f in glob.glob("artifacts/cloud99_*"):
        os.remove(f)
    for f in glob.glob("artifacts/git/wiki/*.md"):
        os.remove(f)


@pytest.fixture
def regen_fixture(request):
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
        "test", "test", "1234", 0, False, [""], cloud.name, vlan.vlan_id,
    )
    schedule = ScheduleDao.create_schedule(
        today,
        tomorrow,
        assignment,
        host,
    )
    assert schedule


class TestRegen(TestBase):
    def test_regen_heatmap(self, regen_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "visual_web_dir", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        self.quads_cli_call("regen_heatmap")

        files = ["index.html", "current.html", "next.html", f"{datetime.now().strftime('%Y-%m')}.html"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/{f}"))
        assert self._caplog.messages == ['Regenerated web table heatmap.']

    def test_regen_instack(self, regen_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("openstack_management", True)
        Config.__setattr__("openshift_management", True)
        Config.__setattr__(
            "json_web_path", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        self.quads_cli_call("regen_instack")

        files = ["cloud99_ocpinventory.json", "cloud99_instackenv.json"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/{f}"))
        assert self._caplog.messages == [
            "Regenerated 'instackenv' for OpenStack Management.",
            "Regenerated 'ocpinventory' for OpenShift Management.",
        ]

    @patch("quads.tools.regenerate_wiki.Wiki", WikiStub)
    @patch("quads.tools.regenerate_vlans_wiki.Wiki", WikiStub)
    def test_regen_wiki(self, regen_fixture):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "wp_wiki_git_repo_path", os.path.join(os.path.dirname(__file__), "artifacts/git/wiki")
        )
        self.quads_cli_call("regen_wiki")

        files = ["assignments.md", "main.md"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{f}"))
        assert "Regenerated wiki." in self._caplog.messages
