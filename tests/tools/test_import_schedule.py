import os

from unittest.mock import patch, MagicMock
from quads.tools.import_current_schedules import import_current_schedules
from tests.tools.test_base import TestBase


class TestImportSchedules(TestBase):
    input_file = os.path.join(os.path.dirname(__file__), "fixtures/valid_input.yaml")

    @patch("quads.tools.import_current_schedules.QuadsApi")
    def test_import_current_schedules_with_valid_data(self, mock_quads_api):
        mock_quads_api.get_cloud.return_value = None
        mock_quads_api.get_active_cloud_assignment.return_value = None
        import_current_schedules(self.input_file)

    @patch("quads.tools.import_current_schedules.QuadsApi")
    def test_import_current_schedules_with_existing_cloud_and_assignment(self, mock_quads_api):
        mock_quads_api.get_cloud.return_value = MagicMock()
        mock_quads_api.get_active_cloud_assignment.return_value = MagicMock()
        import_current_schedules(self.input_file)

    @patch("quads.tools.import_current_schedules.QuadsApi")
    def test_import_current_schedules_with_undefined_host(self, mock_quads_api):
        mock_quads_api.get_host.side_effect = Exception("Undefined host")
        import_current_schedules(self.input_file)

    @patch("quads.tools.import_current_schedules.QuadsApi")
    def test_import_current_schedules_with_moved_schedule(self, mock_quads_api):
        mock_quads_api.get_cloud.return_value = None
        mock_quads_api.get_active_cloud_assignment.return_value = None
        import_current_schedules(self.input_file)
