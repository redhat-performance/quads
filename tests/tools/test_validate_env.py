import asyncio
import logging

import pytest

from datetime import datetime, timedelta
from unittest.mock import patch

from quads.server.dao.assignment import AssignmentDao
from quads.server.dao.baseDao import BaseDao
from quads.server.dao.cloud import CloudDao
from quads.server.dao.host import HostDao
from quads.server.dao.interface import InterfaceDao
from quads.server.dao.schedule import ScheduleDao
from quads.server.dao.vlan import VlanDao
from quads.tools.validate_env import main as validate_env_main
from tests.tools.test_base import TestBase, _logger
from tests.cli.config import (
    CLOUD,
    HOST1,
    IFNAME1,
    IFMAC1,
    IFIP1,
    IFPORT1,
    IFBIOSID1,
    IFSPEED,
    IFVENDOR1,
)


class NetcatStub:
    def __init__(self, ip, port=22, loop=None):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def connect(self):
        pass

    async def close(self):
        pass

    async def write(self, data):
        pass

    async def health_check(self):
        self.__sizeof__()
        return True


class SSHHelperStub(object):
    def __init__(self, _host, _user=None, _password=None):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def run_cmd(self, cmd=None):
        return True, []

    def copy_ssh_key(self, _ssh_key):
        pass


def switch_config_stub(host=None, old_cloud=None, new_cloud=None):
    return True


class TestValidateEnv(TestBase):
    @patch("quads.tools.validate_env.socket.gethostbyname", switch_config_stub)
    @patch("quads.tools.validate_env.switch_config", switch_config_stub)
    @patch("quads.tools.validate_env.SSHHelper", SSHHelperStub)
    @patch("quads.tools.validate_env.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_validate_env(self, mocked_smtp):
        self._caplog.set_level(logging.INFO)
        mocked_smtp()
        _args = {
            "cloud": None,
            "skip_system": False,
            "skip_network": False,
            "skip_hosts": [],
        }
        assignments = AssignmentDao.get_assignments()
        for assignment in assignments:
            setattr(assignment, "provisioned", True)
            BaseDao.safe_commit()

        _loop = asyncio.get_event_loop()
        asyncio.set_event_loop(_loop)

        validate_env_main(_args, _loop, _logger)

        assert self._caplog.messages == [
            "Validating cloud99",
            "There was something wrong with your request.",
            "Unable to query Foreman for cloud: cloud99",
            "Verify Foreman password is correct: rdu2@1234",
        ]
        assignments = AssignmentDao.get_assignments()
        for assignment in assignments:
            assert assignment.notification.fail is False

    @patch("quads.tools.validate_env.socket.gethostbyname", switch_config_stub)
    @patch("quads.tools.validate_env.switch_config", switch_config_stub)
    @patch("quads.tools.validate_env.SSHHelper", SSHHelperStub)
    @patch("quads.tools.validate_env.Netcat", NetcatStub)
    @patch("quads.tools.external.postman.SMTP")
    def test_validate_env_no_cloud(self, mocked_smtp):
        self._caplog.set_level(logging.INFO)
        mocked_smtp()
        _args = {
            "cloud": "cloud02",
            "skip_system": False,
            "skip_network": False,
            "skip_hosts": [],
        }
        assignments = AssignmentDao.get_assignments()
        for assignment in assignments:
            setattr(assignment, "provisioned", True)
            BaseDao.safe_commit()

        _loop = asyncio.get_event_loop()
        asyncio.set_event_loop(_loop)

        validate_env_main(_args, _loop, _logger)

        assert self._caplog.messages == ["No cloud with this name."]
