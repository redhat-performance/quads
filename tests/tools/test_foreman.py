#!/usr/bin/env python3
from unittest.mock import patch, AsyncMock

import pytest

from quads.tools.external.foreman import Foreman


class TestForeman(object):
    @pytest.mark.asyncio
    async def test_initialize_foreman_with_valid_parameters(self):
        foreman = Foreman("https://example.com", "username", "password")

        # Assert the attributes of the Foreman object
        assert foreman.url == "https://example.com"
        assert foreman.username == "username"
        assert foreman.password == "password"

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_all_hosts(self, session_mock):
        # Mock the aiohttp session
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com"}]}

        session_mock.return_value.__aenter__.return_value = resp

        # Create the Foreman object with mocked session
        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_all_hosts()

        assert all_hosts == {"host.example.com": {"name": "host.example.com"}}
