import pytest

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from tests.cli.config import CLOUD
from tests.cli.test_base import TestBase


def finalizer():
    cloud = CloudDao.get_cloud(CLOUD)
    if cloud:
        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        if assignment:
            AssignmentDao.delete_assignment(assignment.id)
        CloudDao.remove_cloud(name=CLOUD)


@pytest.fixture
def define_fixture(request):

    request.addfinalizer(finalizer)


@pytest.fixture
def remove_fixture(request):

    request.addfinalizer(finalizer)

    CloudDao.create_cloud(name=CLOUD)


class TestCloud(TestBase):
    def test_define_cloud(self, define_fixture):
        self.cli_args["cloud"] = CLOUD
        self.cli_args["description"] = "Test cloud"
        self.cli_args["cloudowner"] = "scalelab"
        self.cli_args["ccusers"] = None
        self.cli_args["qinq"] = None
        self.cli_args["cloudticket"] = "1225"
        self.cli_args["force"] = True
        self.cli_args["wipe"] = True

        self.quads_cli_call("cloudresource")
        cloud = CloudDao.get_cloud(CLOUD)
        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        assert assignment is not None
        assert cloud is not None
        assert cloud.name == CLOUD

    def test_remove_cloud(self, remove_fixture):
        self.cli_args["cloud"] = CLOUD

        self.quads_cli_call("rmcloud")

        cloud = CloudDao.get_cloud(CLOUD)
        assert not cloud

    def test_mod_cloud(self, remove_fixture):
        new_description = "Modified description"
        self.cli_args["cloud"] = CLOUD
        self.cli_args["description"] = new_description
        self.cli_args["cloudowner"] = None
        self.cli_args["ccusers"] = None
        self.cli_args["cloudticket"] = None

        self.quads_cli_call("modcloud")

        cloud = CloudDao.get_cloud(CLOUD)
        assignment = AssignmentDao.get_all_cloud_assignments(cloud)
        assert cloud
        assert cloud["description"] == new_description
