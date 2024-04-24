import os

from datetime import datetime
from unittest.mock import patch

from quads.config import Config
from tests.cli.test_base import TestBase
from tests.tools.test_regenerate_wiki import WikiStub


class TestRegen(TestBase):
    def test_regen_heatmap(self):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("visual_web_dir", os.path.join(os.path.dirname(__file__), "artifacts/"))
        self.quads_cli_call("regen_heatmap")

        files = [
            "index.html",
            "current.html",
            "next.html",
            f"{datetime.now().strftime('%Y-%m')}.html",
        ]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/{f}"))
        assert self._caplog.messages == ["Regenerated web table heatmap."]

    @patch("quads.tools.regenerate_wiki.Wordpress", WikiStub)
    @patch("quads.tools.regenerate_vlans_wiki.Wordpress", WikiStub)
    def test_regen_wiki(self):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__(
            "wp_wiki_git_repo_path",
            os.path.join(os.path.dirname(__file__), "artifacts/git/wiki"),
        )
        self.quads_cli_call("regen_wiki")

        files = ["assignments.md", "main.md"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{f}"))
        assert "Regenerated wiki." in self._caplog.messages
