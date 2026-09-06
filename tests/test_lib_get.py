"""Tests for JPILibrary HTTP requests."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from pyjpi import JPIConnectionError, JPIResponseError, jpiInit

from .const import URL


def create_response(text: str = "OK", status: int = 200) -> MagicMock:
    """Create a mocked aiohttp response."""
    response = MagicMock()
    response.status = status
    response.text = AsyncMock(return_value=text)
    return response


@pytest.mark.asyncio
async def test_get_uses_session_and_returns_text():
    """Test a successful HTTP GET request."""
    response = create_response()
    session = MagicMock()
    session.get = AsyncMock(return_value=response)
    lib = await jpiInit(session)

    result = await lib.get(URL)

    assert result == {"text": "OK", "resp": response}
    session.get.assert_awaited_once_with(URL)
    response.raise_for_status.assert_called_once_with()
    response.release.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_raises_on_http_error():
    """Test an HTTP error is mapped to JPIResponseError."""
    response = create_response(status=404)
    response.raise_for_status.side_effect = aiohttp.ClientResponseError(
        request_info=MagicMock(),
        history=(),
        status=404,
        message="Not Found",
    )
    session = MagicMock()
    session.get = AsyncMock(return_value=response)
    lib = await jpiInit(session)

    with pytest.raises(
        JPIResponseError,
        match="JPI request failed with HTTP status 404",
    ):
        await lib.get(URL)

    response.release.assert_called_once_with()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error",
    [
        aiohttp.ClientConnectionError("connection failed"),
        asyncio.TimeoutError(),
    ],
)
async def test_get_raises_on_connection_error(error: Exception):
    """Test connection and timeout errors are mapped consistently."""
    session = MagicMock()
    session.get = AsyncMock(side_effect=error)
    lib = await jpiInit(session)

    with pytest.raises(JPIConnectionError, match="Unable to communicate with JPI"):
        await lib.get(URL)
