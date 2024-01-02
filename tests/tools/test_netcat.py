from unittest.mock import AsyncMock

import pytest

from quads.tools.external.netcat import Netcat


class TestNetcat:

    @pytest.mark.asyncio
    async def test_parameters_init(self):
        netcat = Netcat(ip="10.0.0.9")
        assert netcat.ip == "10.0.0.9"

    @pytest.mark.asyncio
    async def test__aenter__(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        response = await netcat.__aenter__()
        assert response

    @pytest.mark.asyncio
    async def test__aexit__(self):
        netcat = Netcat(ip="10.0.0.9")
        await netcat.__aexit__()
        assert netcat.close()

    @pytest.mark.asyncio
    async def test_health_check(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        response = await netcat.health_check()
        assert response

    @pytest.mark.asyncio
    async def test_health_check_error(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.connect = AsyncMock()
        netcat.connect.side_effect = TimeoutError("timeout")
        response = await netcat.health_check()
        assert not response

    @pytest.mark.asyncio
    async def test_read(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        response = await netcat.read()
        assert response

    @pytest.mark.asyncio
    async def test_read_until(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        response = await netcat.read_until(data="")
        assert not response

    @pytest.mark.asyncio
    async def test_write(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        await netcat.write(data="unittest")

    @pytest.mark.asyncio
    async def test_connect(self):
        netcat = Netcat(ip="10.0.0.9")
        netcat.loop = AsyncMock()
        await netcat.connect()

    @pytest.mark.asyncio
    async def test_close(self):
        netcat = Netcat(ip="10.0.0.9")
        await netcat.close()
        netcat.socket = False
        assert not netcat.socket

