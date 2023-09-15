import pytest

from urllib.parse import urlencode

from tests.helpers import unwrap_json

prefill_settings = ["clouds, vlans, hosts, assignments, schedules"]


class TestReadAvailable:
    @pytest.mark.parametrize("prefill", prefill_settings, indirect=True)
    def test_valid_filter(self, test_client, auth, prefill):
        """
        | GIVEN: Defaults, auth, clouds, vlans, hosts, assignments and schedules
        | WHEN: User tries to read the currently available hosts (by dates and by current assigned cloud)
        | THEN: User should be able to get the available host(s) for each case
        """
        auth_header = auth.get_auth_header()
        responses = [
            [
                "host1.example.com",
                "host2.example.com",
                "host4.example.com",
                "host5.example.com",
            ],
            ["host1.example.com", "host4.example.com", "host5.example.com"],
            ["host3.example.com"],
        ]
        requests = [
            {"start": "2043-03-20T00:00"},
            {"start": "2035-01-01T00:00", "end": "2040-01-01T00:00"},
            {"start": "2045-01-01T00:00", "cloud": "cloud03"},
        ]
        for i, (req, resp) in enumerate(zip(requests, responses)):
            api_resp = unwrap_json(
                test_client.get(
                    f"/api/v3/available?{urlencode(req)}",
                    headers=auth_header,
                )
            )
            assert api_resp.status_code == 200
            assert api_resp.json == resp

    @pytest.mark.parametrize("prefill", prefill_settings, indirect=True)
    def test_valid_is_available(self, test_client, auth, prefill):
        """
        | GIVEN: Defaults, auth, clouds, vlans, hosts, assignments and schedules
        | WHEN: User tries to verify if a host is/will be available for a given date range
        | THEN: User should be able to get an answer if it is or isn't
        """
        auth_header = auth.get_auth_header()
        hostname = "host2.example.com"
        responses = [
            {hostname: "True"},
            {hostname: "False"},
        ]
        requests = [
            {"start": "2043-03-20 00:00"},
            {"start": "2035-01-01 00:00", "end": "2040-01-01 00:00"},
        ]
        for i, (req, resp) in enumerate(zip(requests, responses)):
            api_resp = unwrap_json(
                test_client.get(
                    f"/api/v3/available/{hostname}?{urlencode(req)}",
                    headers=auth_header,
                )
            )
            assert api_resp.status_code == 200
            assert api_resp.json == resp
