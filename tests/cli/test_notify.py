from unittest.mock import patch

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from tests.cli.test_base import TestBase
from tests.tools.test_notify import notify_fixture
from tests.tools.test_validate_env import NetcatStub

assert notify_fixture, "notify_fixture is imported for its side effects."


class TestNotify(TestBase):
    @patch("quads.tools.external.postman.SMTP")
    def test_notify_not_validated(self, mocked_smtp, notify_fixture):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()

        self.quads_cli_call("notify")

        cloud = CloudDao.get_cloud(name="cloud99")
        notification_obj = AssignmentDao.filter_assignments({"cloud_id": cloud.id})[0].notification
        assert notification_obj.pre_initial is True
        assert self._caplog.messages == [
            "=============== Future Initial Message",
            "Notifications sent out.",
        ]

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

        self.quads_cli_call("notify")

        notification_obj = assignments[0].notification
        assert notification_obj.pre_initial is True
        assert notification_obj.pre is True
        assert notification_obj.initial is True
        assert self._caplog.messages == [
            "=============== Initial Message",
            "Beep boop we can't communicate with your webhook.",
            "=============== Additional Message",
            "=============== Future Initial Message",
            "=============== Additional Message",
            "Notifications sent out.",
        ]
