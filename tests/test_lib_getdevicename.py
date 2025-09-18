"""Tests for JPILibrary methods."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from pyjpi import jpiInit

from .const import URL


@pytest.mark.asyncio
async def test_getDeviceName_returns_device_name_string():  # pylint: disable=W0631,C0103
    """Test for 'action=getDeviceName' query."""

    class FakeResp:
        """Fake response context manager."""

        status = 200

        def raise_for_status(self):  # pylint: disable=C0116
            return None

        async def text(self):
            """Returns a fake (but with the expected format) answer."""
            return "Pixel-XL (JPI)"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return None

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit(session)

    name = await lib.getDeviceName(URL)

    assert isinstance(name, str)
    assert name == "Pixel-XL (JPI)"

    # keep assertion flexible re: extra kwargs
    assert session.get.await_args.args[0] == f"{URL}?action=getDeviceName"
