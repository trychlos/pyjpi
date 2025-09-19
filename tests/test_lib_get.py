"""Tests for JPILibrary methods."""

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from pyjpi import jpiInit

from .const import URL


@pytest.mark.asyncio
async def test_get_uses_session_and_returns_text():
    """Test for a HTTP GET method."""

    class FakeResp:
        """Fake response context manager."""

        status = 200

        async def text(self):  # pylint: disable=C0116
            return "OK"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit(session)
    out = await lib.get(URL)
    assert out["text"] == "OK"
    assert out["resp"].status == 200

    session.get.assert_awaited_once_with(URL)


# pylint: disable=import-outside-toplevel
@pytest.mark.asyncio
async def test_get_raises_on_http_error():
    """get() should raise when the response is an HTTP error (e.g., 404)."""
    from aiohttp import ClientResponseError
    from aiohttp.client_reqrep import RequestInfo
    from multidict import CIMultiDict, CIMultiDictProxy
    from yarl import URL as YURL

    # Minimal RequestInfo for the exception
    req_info = RequestInfo(
        url=YURL(URL),
        method="GET",
        headers=CIMultiDictProxy(CIMultiDict()),
        real_url=YURL(URL),
    )

    class FakeErrResp:
        """Fake response error."""

        status = 404

        async def text(self):
            """Raise when your code calls .text()."""
            raise ClientResponseError(
                request_info=req_info,
                history=(),
                status=404,
                message="Not Found",
            )

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeErrResp())

    lib = await jpiInit(session)

    with pytest.raises(ClientResponseError):
        await lib.get(URL)

    session.get.assert_awaited_once_with(URL)


# pylint: disable=import-outside-toplevel
@pytest.mark.asyncio
async def test_get_returns_false_on_connection_error(caplog):
    """If the URL is unavailable (wrong port/host), get() returns False and logs an error."""
    import aiohttp

    session = MagicMock()
    session.get = AsyncMock(
        side_effect=aiohttp.ClientConnectionError("connection failed")
    )

    lib = await jpiInit(session)

    # If your library logger has a known name, pass it here:
    # with caplog.at_level(logging.ERROR, logger="pyjpi"):
    with caplog.at_level(logging.ERROR):
        out = await lib.get(URL)

    assert out is False
    # Either check the aggregated text…
    assert "Error exception:" in caplog.text
    # …or iterate records robustly
    assert any("Error exception:" in rec.getMessage() for rec in caplog.records)


@pytest.mark.asyncio
async def test_get_returns_false_on_timeout(caplog):
    """Specifically tet for timeouts."""

    session = MagicMock()
    session.get = AsyncMock(side_effect=asyncio.TimeoutError())

    lib = await jpiInit(session)

    with caplog.at_level("ERROR"):
        out = await lib.get(URL)

    assert out is False
