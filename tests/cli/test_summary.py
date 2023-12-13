from datetime import datetime
from tests.cli.test_base import TestBase


class TestSummary(TestBase):
    def test_summary_all_detail(self):
        self.cli_args["all"] = True
        self.cli_args["detail"] = True
        self.quads_cli_call("summary")

        assert self._caplog.messages[0] == "cloud99 (test): 1 (test) - 1234"
        assert self._caplog.messages[1] == "cloud01 (test): 0 (test) - 1234"
        assert "cloud03" in self._caplog.messages[2] or "cloud04" in self._caplog.messages[2]

    def test_summary(self):
        self.cli_args["all"] = False
        self.cli_args["detail"] = False
        self.quads_cli_call("summary")

        assert len(self._caplog.messages) == 1
        assert "cloud99" in self._caplog.messages[0]

    def test_summary_date(self):
        today = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.cli_args["datearg"] = today
        self.cli_args["all"] = False
        self.cli_args["detail"] = False
        self.quads_cli_call("summary")

        assert len(self._caplog.messages) == 1
        assert "cloud99" in self._caplog.messages[0]

# Changing the asserting format to tacle the parallel pytest execution,
# this cause creation of multiple hosts and multiple schedules
