import pytest
from unittest.mock import patch, MagicMock
from quads.tools.verify_switchconf import verify


@patch("quads.tools.verify_switchconf.QuadsApi")
def test_verify_with_valid_cloud_and_host(mock_quads_api):
    mock_quads_api.get_cloud.return_value = MagicMock()
    mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
    mock_quads_api.filter_hosts.return_value = [MagicMock()]
    verify("cloud1", "host1")


@patch("quads.tools.verify_switchconf.QuadsApi.get_cloud")
def test_verify_with_invalid_cloud(mock_quads_api):
    mock_quads_api.return_value = None
    with pytest.raises(SystemExit):
        verify("invalid_cloud", "host1")


@patch("quads.tools.verify_switchconf.QuadsApi.filter_hosts")
@patch("quads.tools.verify_switchconf.QuadsApi.get_cloud")
def test_verify_with_invalid_host(mock_get, mock_filter):
    mock_get.return_value = MagicMock()
    mock_filter.return_value = []
    with pytest.raises(SystemExit):
        verify("cloud1", "invalid_host")


@patch("quads.tools.verify_switchconf.QuadsApi")
def test_verify_with_no_cloud_and_host(mock_quads_api):
    with pytest.raises(SystemExit):
        verify(None, None)


@patch("quads.tools.verify_switchconf.QuadsApi")
def test_verify_with_change(mock_quads_api):
    mock_quads_api.get_cloud.return_value = MagicMock()
    mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
    mock_quads_api.filter_hosts.return_value = [MagicMock()]
    verify("cloud1", "host1", True)
