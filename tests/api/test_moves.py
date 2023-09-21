import logging
import pytest

from urllib.parse import urlencode

from quads.cli import QuadsCli
from quads.config import DEFAULT_CONF_PATH, Config
from quads.quads_api import QuadsApi
from tests.helpers import unwrap_json

prefill_settings = ["clouds, vlans, hosts, assignments, schedules"]

_logger = logging.getLogger("test_log")
_logger.setLevel(logging.INFO)
_logger.propagate = True


def quads_cli_call(action):
    _cli_args = {
        "datearg": None,
        "filter": None,
        "force": "False",
        "dryrun": None,
        "movecommand": "/quads/quads/tools/move_and_rebuild.py",
    }
    Config.load_from_yaml(DEFAULT_CONF_PATH)
    quads = QuadsApi(config=Config)
    qcli = QuadsCli(quads=quads, logger=_logger)
    try:
        qcli.run(action=action, cli_args=_cli_args)
    except Exception as ex:
        raise ex


class TestReadMoves:
    @pytest.mark.parametrize("prefill", prefill_settings, indirect=True)
    def test_valid_not_moved(self, test_client, auth, prefill):
        """
        | GIVEN: Defaults, auth, clouds, vlans, hosts, assignments and schedules and NOT moved out hosts
        | WHEN: User tries to read a list of all hosts that need to be moved
        | THEN: User should be able to get the list of hosts with information where they need to moved
        """
        auth_header = auth.get_auth_header()
        resp = [
            {"current": "cloud01", "host": "host2.example.com", "new": "cloud02"},
            {"current": "cloud01", "host": "host3.example.com", "new": "cloud03"},
        ]
        response = unwrap_json(
            test_client.get(
                "/api/v3/moves",
                headers=auth_header,
            )
        )
        assert response.status_code == 200
        assert response.json == resp

    @pytest.mark.parametrize("prefill", prefill_settings, indirect=True)
    def test_valid_moved(self, test_client, auth, prefill):
        """
        | GIVEN: Defaults, auth, clouds, vlans, hosts, assignments and schedules and moved out hosts
        | WHEN: User tries to read a list of all hosts that need to be moved
        | THEN: User should be able to get the list of hosts with information where they need to moved (empty)
        """
        quads_cli_call("movehosts")
        auth_header = auth.get_auth_header()
        response = unwrap_json(
            test_client.get(
                "/api/v3/moves",
                headers=auth_header,
            )
        )
        assert response.status_code == 200
        assert response.json == []

    @pytest.mark.parametrize("prefill", prefill_settings, indirect=True)
    def test_valid_date(self, test_client, auth, prefill):
        """
        | GIVEN: Defaults, auth, clouds, vlans, hosts, assignments and schedules and moved out hosts
        | WHEN: User tries to read a list of all hosts that need to be moved at a specified date
        | THEN: User should be able to get the list of hosts with information where they need to moved
        """
        auth_header = auth.get_auth_header()
        req = {"date": "2055-01-01T00:00"}
        resp = [
            {"current": "cloud02", "host": "host2.example.com", "new": "cloud01"},
            {"current": "cloud03", "host": "host3.example.com", "new": "cloud01"},
        ]
        response = unwrap_json(
            test_client.get(
                f"/api/v3/moves?{urlencode(req)}",
                headers=auth_header,
            )
        )
        assert response.status_code == 200
        assert response.json == resp
