import pytest
from unittest.mock import patch, MagicMock
from quads.quads_api import APIServerException, APIBadRequest
from quads.tools.export_current_schedules import export_current_schedules


@patch("quads.tools.export_current_schedules.QuadsApi")
def test_export_current_schedules_with_valid_data(mock_quads_api):
    mock_quads_api.get_future_schedules.return_value = [
        MagicMock(
            assignment={
                "cloud": {"name": "cloud1"},
                "description": "description1",
                "owner": "owner1",
                "ticket": "ticket1",
                "qinq": "qinq1",
                "wipe": "wipe1",
                "ccuser": ["ccuser1"],
                "vlan": {"vlan_id": "vlan_id1"},
            },
            start="Mon, 01 Jan 2022 00:00:00 GMT",
            end="Tue, 02 Jan 2022 00:00:00 GMT",
            build_start="Mon, 01 Jan 2022 00:00:00 GMT",
            build_end="Tue, 02 Jan 2022 00:00:00 GMT",
            host={"name": "host1", "cloud": {"name": "cloud1"}, "default_cloud": {"name": "cloud1"}},
        )
    ]
    export_current_schedules("output.yaml")


@patch("quads.tools.export_current_schedules.QuadsApi")
def test_export_current_schedules_with_no_future_schedules(mock_quads_api):
    mock_quads_api.get_future_schedules.return_value = []
    export_current_schedules("output.yaml")


@patch("quads.tools.export_current_schedules.QuadsApi.get_future_schedules")
def test_export_current_schedules_with_api_exception(mock_quads_api):
    mock_quads_api.side_effect = APIServerException("API Server Exception")
    with pytest.raises(APIServerException):
        export_current_schedules("output.yaml")


@patch("quads.tools.export_current_schedules.QuadsApi.get_future_schedules")
def test_export_current_schedules_with_api_bad_request(mock_quads_api):
    mock_quads_api.side_effect = APIBadRequest("API Bad Request")
    with pytest.raises(APIBadRequest):
        export_current_schedules("output.yaml")
