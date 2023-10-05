from unittest.mock import patch

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from tests.cli.config import (
    CLOUD,
    HOST1,
    DEFINE_CLOUD,
    REMOVE_CLOUD,
    MOD_CLOUD,
    DEFAULT_CLOUD,
)
from tests.cli.test_base import TestBase
import pytest


@pytest.fixture(autouse=True)
def remove_cloud(request):
    def finalizer():
        cloud = CloudDao.get_cloud(DEFINE_CLOUD)
        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        if assignment:
            AssignmentDao.remove_assignment(assignment.id)
        if cloud:
            CloudDao.remove_cloud(DEFINE_CLOUD)

    finalizer()
    request.addfinalizer(finalizer)


@pytest.fixture(autouse=True)
def define_cloud(request):
    CloudDao.create_cloud(DEFINE_CLOUD)


class TestCloud(TestBase):
    def test_define_cloud(self, remove_cloud):
        self.cli_args["cloud"] = DEFINE_CLOUD
        self.cli_args["description"] = "Test cloud"
        self.cli_args["cloudowner"] = "scalelab"
        self.cli_args["ccusers"] = None
        self.cli_args["qinq"] = None
        self.cli_args["cloudticket"] = "1225"
        self.cli_args["force"] = True
        self.cli_args["wipe"] = True

        self.quads_cli_call("cloudresource")

        assert self._caplog.messages[0] == f"Cloud {DEFINE_CLOUD} created."
        assert self._caplog.messages[1] == "Assignment created."

        cloud = CloudDao.get_cloud(CLOUD)
        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        assert assignment is not None
        assert cloud is not None
        assert cloud.name == CLOUD

    def test_remove_cloud(self, define_cloud):
        self.cli_args["cloud"] = REMOVE_CLOUD

        self.quads_cli_call("rmcloud")

        rm_cloud = CloudDao.get_cloud(REMOVE_CLOUD)

        assert not rm_cloud

    def test_mod_cloud(self):
        new_description = "Modified description"
        self.cli_args["cloud"] = MOD_CLOUD
        self.cli_args["description"] = new_description
        self.cli_args["cloudowner"] = None
        self.cli_args["ccusers"] = None
        self.cli_args["cloudticket"] = None

        self.quads_cli_call("modcloud")

        assert self._caplog.messages[0] == "Cloud modified successfully"

        cloud = CloudDao.get_cloud(MOD_CLOUD)
        assert cloud

        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        assert assignment
        assert assignment.description == new_description

    @patch("quads.quads_api.requests.Session.get")
    def test_ls_no_clouds(self, mock_get):
        mock_get.return_value.json.return_value = []
        self.quads_cli_call("ls_clouds")

        assert self._caplog.messages[0] == "No clouds found."

    def test_ls_clouds(self):
        self.quads_cli_call("ls_clouds")

        assert self._caplog.messages[0] == DEFAULT_CLOUD
        assert self._caplog.messages[1] == MOD_CLOUD
        assert self._caplog.messages[2] == CLOUD

    def test_ls_wipe(self):
        self.quads_cli_call("wipe")

        assert self._caplog.messages[0] == f"{CLOUD}: False"

    def test_ls_ticket(self):
        self.quads_cli_call("ticket")

        assert self._caplog.messages[0] == f"{CLOUD}: 1234"

    def test_ls_owner(self):
        self.quads_cli_call("owner")

        assert self._caplog.messages[0] == f"{CLOUD}: test"

    def test_ls_qinq(self):
        self.quads_cli_call("qinq")

        assert self._caplog.messages[0] == f"{CLOUD}: 0"

    def test_ls_cc_users(self):
        self.quads_cli_call("ccuser")

        assert self._caplog.messages[0] == f"{CLOUD}: ['']"

    def test_ls_vlan(self):
        self.quads_cli_call("ls_vlan")

        assert self._caplog.messages[0] == f"1: {CLOUD}"

    def test_free_cloud(self):
        self.quads_cli_call("free_cloud")

        assert self._caplog.messages[0].startswith(f"{MOD_CLOUD} (reserved: ")
        assert self._caplog.messages[0].endswith("min remaining)")


class TestCloudOnly(TestBase):
    def test_cloud_only(self):
        self.cli_args["cloud"] = CLOUD
        self.quads_cli_call("cloudonly")
        assert self._caplog.messages[0] == f"{HOST1}"
