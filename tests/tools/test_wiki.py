import os
from unittest.mock import patch, MagicMock

from quads.tools.external.wiki import Wiki


class TestWiki:
    def test_wiki_parameters_https(self):
        wiki = Wiki(
            url="https://unittest.com", username="unittest", password="password"
        )
        assert wiki.endpoint == "https://unittest.com/xmlrpc.php"

    def test_wiki_parameters_http(self):
        wiki = Wiki(url="http://unittest.com", username="unittest", password="password")
        assert wiki.endpoint == "http://unittest.com/xmlrpc.php"

    @patch("quads.tools.external.wiki.Client")
    @patch("quads.tools.external.wiki.WordPressPage")
    @patch("quads.tools.external.wiki.EditPost")
    def test_wiki_update(self, mock_edit, mock_wpp, mock_client):
        mock_edit.return_value.__aenter__.return_value = MagicMock()
        mock_wpp.return_value.__aenter__.return_value = MagicMock()
        mock_client.return_value.__aenter__.return_value = MagicMock()
        wiki = Wiki(
            url="https://unittest.com", username="unittest", password="password"
        )
        readme = os.path.join(os.path.dirname(__file__), "../../README.md")
        wiki.update(_page_title="Unit Test", _page_id="1", _markdown=readme)
