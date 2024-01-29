import os
from unittest.mock import patch, MagicMock

from quads.tools.external.wordpress import Wordpress


class TestWordpress:
    def test_wp_parameters_https(self):
        wiki = Wordpress(url="https://unittest.com", username="unittest", password="password")
        assert wiki.api_endpoint == "https://unittest.com/xmlrpc.php"

    @patch("quads.tools.external.wiki.Client")
    @patch("quads.tools.external.wiki.WordPressPage")
    @patch("quads.tools.external.wiki.EditPost")
    def test_wp_update(self, mock_edit, mock_wpp, mock_client):
        mock_edit.return_value.__aenter__.return_value = MagicMock()
        mock_wpp.return_value.__aenter__.return_value = MagicMock()
        mock_client.return_value.__aenter__.return_value = MagicMock()
        wordpress = Wordpress(url="https://unittest.com", username="unittest", password="password")
        readme = os.path.join(os.path.dirname(__file__), "../../README.md")
        wordpress.update_page(_page_title="Unit Test", _page_id="1", _markdown=readme)
