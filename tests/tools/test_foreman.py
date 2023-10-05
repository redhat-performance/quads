#!/usr/bin/env python3
from unittest.mock import patch, AsyncMock

import pytest

from quads.tools.external.foreman import Foreman


class TestForeman(object):
    @pytest.mark.asyncio
    async def test_initialize_foreman_with_valid_parameters(self):
        foreman = Foreman("https://example.com", "username", "password")

        assert foreman.url == "https://example.com"
        assert foreman.username == "username"
        assert foreman.password == "password"

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_all_hosts(self, session_mock):
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com"}]}

        session_mock.return_value.__aenter__.return_value = resp

        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_all_hosts()

        assert all_hosts == {"host.example.com": {"name": "host.example.com"}}

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_broken_hosts(self, session_mock):
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com"}]}

        session_mock.return_value.__aenter__.return_value = resp

        # Create the Foreman object with mocked session
        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_broken_hosts()

        assert all_hosts == {"host.example.com": {"name": "host.example.com"}}

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_build_hosts(self, session_mock):
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com"}]}

        session_mock.return_value.__aenter__.return_value = resp

        # Create the Foreman object with mocked session
        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_build_hosts()

        assert all_hosts == {"host.example.com": {"name": "host.example.com"}}

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_parametrized(self, session_mock):
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com"}]}

        session_mock.return_value.__aenter__.return_value = resp

        # Create the Foreman object with mocked session
        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_parametrized("build", True)

        assert all_hosts == {"host.example.com": {"name": "host.example.com"}}

    @patch("quads.tools.external.foreman.aiohttp.ClientSession.get")
    @pytest.mark.asyncio
    async def test_get_host_id(self, session_mock):
        resp = AsyncMock()
        resp.json.return_value = {"results": [{"name": "host.example.com", "id": "host1"}]}

        session_mock.return_value.__aenter__.return_value = resp

        # Create the Foreman object with mocked session
        foreman = Foreman("https://example.com", "username", "password")
        all_hosts = await foreman.get_host_id("host.example.com")

        assert all_hosts == "host1"
