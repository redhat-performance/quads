import logging

from unittest.mock import patch

from quads.config import Config
from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from tests.cli.test_base import TestBase
from tests.tools.test_validate_env import NetcatStub, SSHHelperStub, switch_config_stub


class TestValidateEnv(TestBase):
    @patch("quads.tools.validate_env.socket.gethostbyname", switch_config_stub)
    @patch("quads.tools.validate_env.switch_config", switch_config_stub)
    @patch("quads.tools.validate_env.SSHHelper", SSHHelperStub)
    @patch("quads.tools.validate_env.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_validate_env(self, mocked_smtp):
        Config.__setattr__("foreman_unavailable", True)
        mocked_smtp()
        assignments = AssignmentDao.get_assignments()
        for assignment in assignments:
            setattr(assignment, "provisioned", True)
            BaseDao.safe_commit()

        self._caplog.set_level(logging.INFO)
        self.quads_cli_call("validate_env")

        assert self._caplog.messages[-5:] == [
            "Validating cloud04",
            "Quads assignments validation executed.",
        ]
        cloud = CloudDao.get_cloud(name="cloud04")
        ass = AssignmentDao.get_active_cloud_assignment(cloud=cloud)
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
        self.quads_cli_call("validate_env")

        assert self._caplog.messages[-2:] == [
            "No cloud with this name.",
            "Quads assignments validation executed.",
        ]
