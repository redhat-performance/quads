import pytest
import os

from unittest.mock import patch

from quads.config import Config
from quads.tools.regenerate_wiki import main as regenerate_wiki_main
from tests.tools.test_base import TestBase


class WikiStub:
    def __init__(self, url, username, password):
        pass

    def update(self, _page_title, _page_id, _markdown):
        pass


class TestWiki(TestBase):
    @patch("quads.tools.regenerate_wiki.Wiki", WikiStub)
    @patch("quads.tools.regenerate_vlans_wiki.Wiki", WikiStub)
    def test_regenerate_wiki(self):
        Config.__setattr__("foreman_unavailable", True)
        Config.__setattr__("wp_wiki_git_repo_path", os.path.join(os.path.dirname(__file__), "artifacts/git/wiki"))
        regenerate_wiki_main()

        files = ["assignments.md", "main.md"]
        for f in files:
            assert os.path.exists(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{f}"))

        assignment_md = open(os.path.join(os.path.dirname(__file__), f"artifacts/git/wiki/{files[0]}"), "r")
        assignment_md = "".join(assignment_md.readlines())
        host_assignment_str = "| host1 | <a href=http://mgmt-host1.example.com/ target=_blank>console</a> |\n"
        assert host_assignment_str in assignment_md
