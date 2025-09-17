"""Test jpiInit() calls."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from pyjpi import jpiInit, JPILibrary

@pytest.mark.asyncio
async def test_jpiInit_returns_library():
    session = MagicMock()  # acts like a ClientSession for this test
    lib = await jpiInit( session )
    assert isinstance( lib, JPILibrary )
