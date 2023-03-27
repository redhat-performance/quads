import logging
import sys

from quads.cli import QuadsCli
from quads.config import DEFAULT_CONF_PATH, Config
from quads.quads_api import QuadsApi
from unittest import TestCase


_logger = logging.getLogger(__name__)


class TestBase(TestCase):
    cli_args = {"datearg": None, "filter": None}

    def quads_cli_call(self, action):
        stdout_stream = logging.StreamHandler(sys.stdout)
        _logger.addHandler(stdout_stream)
        _logger.propagate = False

        Config.load_from_yaml(DEFAULT_CONF_PATH)

        quads = QuadsApi(config=Config)

        qcli = QuadsCli(
            quads=quads,
            logger=_logger,
        )

        return qcli.run(
            action=action,
            cli_args=self.cli_args,
        )
