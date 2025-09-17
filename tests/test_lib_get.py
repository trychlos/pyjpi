"""Tests for JPILibrary methods."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from pyjpi import jpiInit

from .const import URL

@pytest.mark.asyncio
async def test_get_uses_session_and_returns_text():
    # fake response context manager
    class FakeResp:
        status = 200
        async def text(self): return "OK"
        async def __aenter__(self): return self
        async def __aexit__(self, *exc): pass

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit( session )
    out = await lib.get( URL )
    assert out['text'] == "OK"
    assert out["resp"].status == 200

    session.get.assert_awaited_once_with( URL )
