import os

from datetime import datetime

from quads.config import Config
from quads.tools.simple_table_web import main as web_main
from tests.tools.test_base import TestBase


class TestTable(TestBase):
    def test_simple_table_web(self):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "visual_web_dir", os.path.join(os.path.dirname(__file__), "artifacts/")
        )
        web_main()
        current = open(
            os.path.join(os.path.dirname(__file__), "artifacts/current.html"), "r"
        )
        current = [n for n in current.readlines() if "Emoji" not in n]
        current = "".join(current)
        response = f"""title=
        "Description: test
        Env: cloud99
        Owner: test
        Ticket: 1234
        Day: {datetime.now().day + 1}">"""
        assert isinstance(current, str) is True
        assert response in current
