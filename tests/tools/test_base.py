import logging
import sys

import pytest

from quads.cli import QuadsCli
from quads.config import DEFAULT_CONF_PATH, Config
from quads.quads_api import QuadsApi

_logger = logging.getLogger("test_log")
_logger.setLevel(logging.INFO)
_logger.propagate = True


class TestBase:
    cli_args = {"datearg": None, "filter": None, "force": "False"}

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        caplog.set_level(logging.DEBUG)
        self._caplog = caplog

    @pytest.fixture(autouse=True)
    def capture_wrap(self):
        sys.stderr.close = lambda *args: None
        sys.stdout.close = lambda *args: None
        yield

    def quads_cli_call(self, action):
        Config.load_from_yaml(DEFAULT_CONF_PATH)

        quads = QuadsApi(config=Config)

        qcli = QuadsCli(
            quads=quads,
            logger=_logger,
        )

        try:
            qcli.run(
                action=action,
                cli_args=self.cli_args,
            )
        except Exception:
            pass
