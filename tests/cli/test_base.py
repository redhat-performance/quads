import logging
import pytest

from quads.cli import QuadsCli
from quads.config import DEFAULT_CONF_PATH, Config
from quads.quads_api import QuadsApi

from quads.server.app import create_app, user_datastore
from quads.server.database import drop_all, populate, init_db

_logger = logging.getLogger("test_log")
_logger.setLevel(logging.INFO)
_logger.propagate = True


class TestBase:
    cli_args = {"datearg": None, "filter": None, "force": "False"}

    @pytest.fixture(autouse=True)
    def test_client(self):
        """
        | Creates a test client for the app from the testing config.
        | Drops and then initializes the database and populates it with default users.
        """
        self.flask_app = create_app()
        self.flask_app.config.from_object("quads.server.config.TestingConfig")

        with self.flask_app.test_client() as testing_client:
            with self.flask_app.app_context():
                drop_all(self.flask_app.config)
                init_db(self.flask_app.config)
                populate(user_datastore)
                yield testing_client

    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self._caplog = caplog

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
        except Exception as ex:
            raise ex
