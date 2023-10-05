from tests.cli.test_base import TestBase


class TestReport(TestBase):
    def test_report_available(self):
        self.quads_cli_call("report_available")
        assert self._caplog.messages[0].startswith("QUADS report for ")
        assert self._caplog.messages[1] == "Percentage Utilized: 23%"
        assert self._caplog.messages[2] == "Average build delta: 0:00:00"
        assert (
            self._caplog.messages[3]
            == "Server Type | Total|  Free| Scheduled| 2 weeks| 4 weeks"
        )
        assert (
            self._caplog.messages[4]
            == "host2       |     1|     1|        0%|       1|       1"
        )
        assert (
            self._caplog.messages[5]
            == "host1       |     1|     0|      100%|       0|       0"
        )
