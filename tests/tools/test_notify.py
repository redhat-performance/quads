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
from quads.server.models import db
from tests.cli.config import CLOUD, HOST1
from quads.tools.notify import main as notify_main
from tests.tools.test_base import TestBase, _logger
from tests.tools.test_validate_env import NetcatStub


class TestNotify(TestBase):
    @patch("quads.tools.external.postman.SMTP")
    def test_notify_not_validated(self, mocked_smtp):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()
        self._caplog.set_level(logging.INFO)
        notify_main(_logger=_logger)

        cloud = CloudDao.get_cloud(name="cloud99")
        notification_obj = AssignmentDao.filter_assignments({"cloud_id": cloud.id})[0].notification
        assert notification_obj.pre_initial is True
        assert self._caplog.messages == [
            "=============== Future Initial Message",
            "=============== Future Initial Message",
        ]

    @patch("quads.tools.notify.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_notify_validated(self, mocked_smtp):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("webhook_notify", True)
        mocked_smtp()
        cloud = CloudDao.get_cloud(name="cloud99")
        ass = AssignmentDao.get_active_cloud_assignment(cloud=cloud)
        ass.validated = True
        BaseDao.safe_commit()

        self._caplog.set_level(logging.INFO)
        notify_main(_logger=_logger)
        ass = AssignmentDao.get_active_cloud_assignment(cloud=cloud)
        db.session.refresh(ass)

        assert ass.notification.pre_initial is True
        assert ass.notification.pre is True
        assert ass.notification.initial is True
        assert self._caplog.messages == [
            "=============== Initial Message",
            "Beep boop we can't communicate with your webhook.",
            "=============== Additional Message",
            "=============== Future Initial Message",
            "=============== Additional Message",
        ]
