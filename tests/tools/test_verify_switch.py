import pytest
from unittest.mock import patch, MagicMock
from quads.tools.verify_switchconf import verify
from tests.tools.test_base import TestBase


class TestVerifySwitchConf(TestBase):
    @patch("quads.tools.verify_switchconf.QuadsApi")
    def test_verify_with_valid_cloud_and_host(self, mock_quads_api):
        mock_quads_api.get_cloud.return_value = MagicMock()
        mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
        mock_quads_api.filter_hosts.return_value = [MagicMock()]
        verify("cloud1", "host1")

    @patch("quads.tools.verify_switchconf.QuadsApi.get_cloud")
    def test_verify_with_invalid_cloud(self, mock_quads_api, caplog):
        mock_quads_api.return_value = None
        verify("invalid_cloud", "host1")
        assert "Cloud not found." in caplog.text

    @patch("quads.tools.verify_switchconf.QuadsApi.filter_hosts")
    @patch("quads.tools.verify_switchconf.QuadsApi.get_cloud")
    def test_verify_with_invalid_host(self, mock_get, mock_filter, caplog):
        mock_get.return_value = MagicMock()
        mock_filter.return_value = []
        verify("cloud1", "invalid_host")
        assert "Host not found." in caplog.text

    @patch("quads.tools.verify_switchconf.QuadsApi")
    def test_verify_with_no_cloud_and_host(self, mock_quads_api, caplog):
        mock_quads_api.return_value = MagicMock()
        verify(None, None)
        assert "At least one of --cloud or --host should be specified." in caplog.text

    @patch("quads.tools.verify_switchconf.QuadsApi")
    def test_verify_with_change(self, mock_quads_api):
        mock_quads_api.get_cloud.return_value = MagicMock()
        mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
        mock_quads_api.filter_hosts.return_value = [MagicMock()]
        verify("cloud1", "host1", True)
