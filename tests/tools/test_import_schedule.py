from unittest.mock import patch, MagicMock
from quads.tools.import_current_schedules import import_current_schedules


@patch("quads.tools.import_current_schedules.QuadsApi")
def test_import_current_schedules_with_valid_data(mock_quads_api):
    mock_quads_api.get_cloud.return_value = None
    mock_quads_api.get_active_cloud_assignment.return_value = None
    import_current_schedules("valid_input.yaml")


@patch("quads.tools.import_current_schedules.QuadsApi")
def test_import_current_schedules_with_existing_cloud_and_assignment(mock_quads_api):
    mock_quads_api.get_cloud.return_value = MagicMock()
    mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
    import_current_schedules("valid_input.yaml")


@patch("quads.tools.import_current_schedules.QuadsApi")
def test_import_current_schedules_with_undefined_host(mock_quads_api):
    mock_quads_api.get_host.side_effect = Exception("Undefined host")
    import_current_schedules("valid_input.yaml")


@patch("quads.tools.import_current_schedules.QuadsApi")
def test_import_current_schedules_with_moved_schedule(mock_quads_api):
    mock_quads_api.get_cloud.return_value = None
    mock_quads_api.get_active_cloud_assignment.return_value = None
    import_current_schedules("moved_schedule_input.yaml")
