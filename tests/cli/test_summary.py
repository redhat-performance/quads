import pytest

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.vlan import VlanDao
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

    cloud = CloudDao.create_cloud(name=CLOUD)
    vlan = VlanDao.create_vlan(
        gateway="10.0.0.1",
        ip_free=510,
        vlan_id=1,
        ip_range="10.0.0.0/23",
        netmask="255.255.0.0",
    )
    assignment = AssignmentDao.create_assignment(
        description="Test cloud",
        owner="scalelab",
        ticket="123456",
        qinq=0,
        wipe=False,
        ccuser=[],
        vlan_id=1,
        cloud=CLOUD,
    )


class TestSummary(TestBase):
    def test_summary(self, define_fixture):
        self.cli_args["all"] = False
        self.quads_cli_call("summary")

        assert self._caplog.messages[0] == "Cloud cloud99 created."
        assert self._caplog.messages[1] == "Assignment created."
