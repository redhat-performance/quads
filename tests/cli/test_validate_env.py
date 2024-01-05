import logging
from datetime import datetime, timedelta

import pytest

from unittest.mock import patch

from quads.config import Config
from quads.exceptions import CliException
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.models import db
from tests.cli.config import HOST1, NetcatStub, SSHHelperStub, switch_config_stub
from tests.cli.test_base import TestBase


def finalizer():
    cloud = CloudDao.get_cloud(name="cloud04")
    schedule = ScheduleDao.get_current_schedule(cloud=cloud)
    if schedule:
        ScheduleDao.remove_schedule(schedule[0].id)


@pytest.fixture
def validate_fixture(request):
    request.addfinalizer(finalizer)
    yesterday = datetime.now() - timedelta(days=1)
    tomorrow = yesterday + timedelta(weeks=2)
    cloud = CloudDao.get_cloud(name="cloud04")
    ass = AssignmentDao.get_active_cloud_assignment(cloud=cloud)
    ass.provisioned = True
    ass.wipe = True
    BaseDao.safe_commit()
    host = HostDao.get_host(HOST1)
    schedule = ScheduleDao.create_schedule(
        start=yesterday, end=tomorrow, assignment=ass, host=host
    )
    assert schedule


class TestValidateEnv(TestBase):
    @patch("quads.tools.validate_env.socket.gethostbyname", switch_config_stub)
    @patch("quads.tools.validate_env.switch_config", switch_config_stub)
    @patch("quads.tools.validate_env.SSHHelper", SSHHelperStub)
    @patch("quads.tools.validate_env.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_validate_env(self, mocked_smtp, validate_fixture):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()

        self._caplog.set_level(logging.INFO)
        self.quads_cli_call("validate_env")

        assert self._caplog.messages[-5:] == [
            "Validating cloud04",
            "Quads assignments validation executed.",
        ]
        cloud = CloudDao.get_cloud(name="cloud04")
        ass = AssignmentDao.get_active_cloud_assignment(cloud=cloud)
        db.session.refresh(ass)
        assert ass.notification.fail is False
        assert ass.validated is True

    @patch("quads.tools.validate_env.socket.gethostbyname", switch_config_stub)
    @patch("quads.tools.validate_env.switch_config", switch_config_stub)
    @patch("quads.tools.validate_env.SSHHelper", SSHHelperStub)
    @patch("quads.tools.validate_env.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_validate_env_no_cloud(self, mocked_smtp):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()
        assignments = AssignmentDao.get_assignments()
        for assignment in assignments:
            setattr(assignment, "provisioned", True)
            BaseDao.safe_commit()

        self._caplog.set_level(logging.INFO)
        self.cli_args.update({"cloud": "cloud02"})
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("validate_env")

        assert str(ex.value) == "Cloud not found: cloud02"
