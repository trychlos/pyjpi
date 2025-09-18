"""Test jpiInit() calls."""

from unittest.mock import MagicMock

import pytest

from pyjpi import jpiInit, JPILibrary


@pytest.mark.asyncio
async def test_jpiInit_returns_library():
    """Test for jpiInit() function."""
    session = MagicMock()  # acts like a ClientSession for this test
    lib = await jpiInit(session)
    assert isinstance(lib, JPILibrary)
