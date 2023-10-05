from datetime import datetime
from unittest.mock import patch

import pytest

from quads.config import Config
from quads.exceptions import CliException
from tests.cli.config import CLOUD, DEFAULT_CLOUD, HOST2, MOD_CLOUD, HOST1
from tests.cli.test_base import TestBase


class TestQuads(TestBase):
    def test_default_action(self):

        # TODO: Check host duplication here
        self.quads_cli_call(None)
        assert self._caplog.messages[0] == f"{DEFAULT_CLOUD}:"
        assert self._caplog.messages[1] == f"  - {HOST2}"
        assert self._caplog.messages[2] == f"{MOD_CLOUD}:"
        assert self._caplog.messages[3] == f"  - {HOST1}"
        assert self._caplog.messages[4] == f"{CLOUD}:"
        assert self._caplog.messages[5] == f"  - {HOST1}"

    @patch("quads.quads_api.requests.Session.get")
    def test_default_action_500_exception(self, mock_get):
        mock_get.return_value.status_code = 500
        with pytest.raises(CliException) as ex:
            self.quads_cli_call(None)
        assert str(ex.value) == "Check the flask server logs"

    @patch("quads.quads_api.requests.Session.get")
    def test_default_action_400_exception(self, mock_get):
        mock_get.return_value.status_code = 400
        with pytest.raises(CliException) as ex:
            self.quads_cli_call(None)

    def test_default_action_date(self):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cli_args["datearg"] = f"{date} 22:00"
        self.quads_cli_call(None)

    def test_version(self):
        self.quads_cli_call("version")
        assert (
            self._caplog.messages[0]
            == f'"QUADS version {Config.QUADSVERSION} {Config.QUADSCODENAME}"\n'
        )
