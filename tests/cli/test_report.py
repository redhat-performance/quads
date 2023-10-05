import pytest

from datetime import datetime, timedelta
from quads.exceptions import CliException
from tests.cli.test_base import TestBase


class TestReport(TestBase):
    def test_report_available(self):
        self.quads_cli_call("report_available")
        assert self._caplog.messages[0].startswith("QUADS report for ")
        assert self._caplog.messages[1] == "Percentage Utilized: 23%"
        assert self._caplog.messages[2] == "Average build delta: 0:00:00"
        assert self._caplog.messages[3] == "Server Type | Total|  Free| Scheduled| 2 weeks| 4 weeks"
        assert self._caplog.messages[4] == "host2       |     1|     1|        0%|       1|       1"
        assert self._caplog.messages[5] == "host1       |     1|     0|      100%|       0|       0"

    def test_report_scheduled(self):
        # TODO: Fix this test
        self.cli_args["months"] = 12
        self.cli_args["year"] = None
        self.quads_cli_call("report_scheduled")
        assert self._caplog.messages[0] == "Month   | Scheduled|  Systems|  % Utilized| "
        assert self._caplog.messages[1] == "2023-10 |         1|        2|         23%| "
        assert self._caplog.messages[2] == "2023-09 |         0|        2|          0%| "

    def test_report_scheduled_no_args(self):
        self.cli_args["months"] = None
        self.cli_args["year"] = None
        with pytest.raises(CliException) as ex:
            self.quads_cli_call("report_scheduled")

        assert str(ex.value) == "Missing argument. --months or --year must be provided."

    def test_report_scheduled_year(self):
        today = datetime.now()
        # TODO: Fix this test
        self.cli_args["months"] = None
        self.cli_args["year"] = today.year
        self.quads_cli_call("report_scheduled")
        assert self._caplog.messages[0] == "Month   | Scheduled|  Systems|  % Utilized| "
        assert self._caplog.messages[1] == f"{today.year}-{today.month:02d} |         1|        2|         23%| "
        assert self._caplog.messages[2] == f"{today.year}-{today.month - 1:02d} |         0|        2|          0%| "

    def test_report_detailed(self):
        today = datetime.now()

        future = today + timedelta(weeks=2)
        # TODO: Fix this test
        self.cli_args["months"] = None
        self.cli_args["year"] = today.year
        self.quads_cli_call("report_detailed")
        assert (
            self._caplog.messages[0] == "Owner    |    Ticket|    Cloud| Description| Systems|  Scheduled| Duration| "
        )
        assert (
            self._caplog.messages[1]
            == f"test     |      1234|  cloud99|        test|       1| {today.strftime('%Y-%m-%d')}|       14| "
        )
