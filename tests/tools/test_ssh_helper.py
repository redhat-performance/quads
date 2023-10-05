import pytest

from unittest.mock import patch, MagicMock
from quads.tools.external.ssh_helper import SSHHelper
from paramiko import SSHException
from tests.tools.test_base import TestBase


class TestSSHHelper(TestBase):
    @patch("quads.tools.external.ssh_helper.SSHHelper.connect")
    def test_connect_with_valid_credentials(self, mock_connect):
        mock_connect.return_value = MagicMock()
        ssh_helper = SSHHelper("valid_host", "valid_user", "valid_password")
        assert ssh_helper.ssh is not None

    @patch("quads.tools.external.ssh_helper.SSHHelper.connect")
    def test_connect_exception(self, mock_connect):
        mock_connect.side_effect = SSHException("Invalid credentials")
        with pytest.raises(SSHException) as ex:
            SSHHelper("invalid_host", "invalid_user", "invalid_password")
        assert str(ex.value) == "Invalid credentials"

    @patch("quads.tools.external.ssh_helper.SSHConfig")
    @patch("quads.tools.external.ssh_helper.SSHClient")
    def test_run_cmd_with_error(self, mock_client, mock_config):
        mock_config.return_value = MagicMock()
        stderr_mock = MagicMock()
        stderr_mock.readlines.return_value = ["Error here"]
        mock_client.return_value.exec_command.return_value = (
            MagicMock(),
            MagicMock(),
            stderr_mock,
        )
        ssh_helper = SSHHelper("invalid_host", "invalid_user", "invalid_password")
        result, error = ssh_helper.run_cmd("ls")
        assert not result
        assert error == ["Error here"]

    @patch("quads.tools.external.ssh_helper.SSHConfig")
    @patch("quads.tools.external.ssh_helper.SSHClient")
    def test_run_cmd(self, mock_client, mock_config):
        mock_config.return_value = MagicMock()
        stderr_mock = MagicMock()
        stderr_mock.readlines.return_value = []
        stdout_mock = MagicMock()
        stdout_mock.channel.recv_exit_status.return_value = 0
        mock_client.return_value.exec_command.return_value = (
            MagicMock(),
            stdout_mock,
            stderr_mock,
        )
        ssh_helper = SSHHelper("invalid_host", "invalid_user", "invalid_password")
        result, error = ssh_helper.run_cmd("ls")
        assert result
