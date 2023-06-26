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
    assignment = AssignmentDao.create_assignment(
        description="Test cloud",
        owner="scalelab",
        ticket="123456",
        qinq=0,
        wipe=False,
        ccuser=[],
        vlan_id=1,
        cloud=CLOUD
    )


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

        assert self._caplog.messages[0] == 'Cloud cloud99 created.'
        assert self._caplog.messages[1] == 'Assignment created.'

        cloud = CloudDao.get_cloud(CLOUD)
        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        assert assignment is not None
        assert cloud is not None
        assert cloud.name == CLOUD

    def test_remove_cloud(self, remove_fixture):
        self.cli_args["cloud"] = CLOUD
        cloud = CloudDao.get_cloud(CLOUD)

        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        AssignmentDao.udpate_assignment(assignment_id=assignment.id, active=False)

        self.quads_cli_call("rmcloud")

        rm_cloud = CloudDao.get_cloud(CLOUD)

        assert self._caplog.messages[0] == 'Successfully removed'
        assert not rm_cloud

    def test_mod_cloud(self, remove_fixture):
        new_description = "Modified description"
        self.cli_args["cloud"] = CLOUD
        self.cli_args["description"] = new_description
        self.cli_args["cloudowner"] = None
        self.cli_args["ccusers"] = None
        self.cli_args["cloudticket"] = None

        self.quads_cli_call("modcloud")

        assert self._caplog.messages[0] == 'Cloud modified successfully'

        cloud = CloudDao.get_cloud(CLOUD)
        assert cloud

        assignment = AssignmentDao.get_active_cloud_assignment(cloud)
        assert assignment
        assert assignment.description == new_description

    def test_ls_cloud(self, remove_fixture):
        self.quads_cli_call("cloud")

        assert self._caplog.messages[0] == CLOUD