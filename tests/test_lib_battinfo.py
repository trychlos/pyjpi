"""Tests for JPILibrary methods."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from pyjpi import jpiInit

from .const import URL


@pytest.mark.asyncio
async def test_battInfo_empty():
    """Test for 'action=battInfo' query."""

    class FakeResp:
        """Fake response context manager."""

        status = 200

        def raise_for_status(self):  # pylint: disable=C0116
            return None

        def release(self):
            """Release the fake response."""

        async def text(self):
            """Returns a fake empty answer."""
            return "\n"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return None

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit(session)

    info = await lib.battInfo(URL)

    assert isinstance(info, dict)
    assert not info

    # keep assertion flexible re: extra kwargs
    assert session.get.await_args.args[0] == f"{URL}/?action=battInfo"


@pytest.mark.asyncio
async def test_battInfo_parses_and_returns_expected_dict():
    """Test for 'action=battInfo' query."""

    class FakeResp:
        """Fake response context manager."""

        status = 200

        def raise_for_status(self):  # pylint: disable=C0116
            return None

        def release(self):
            """Release the fake response."""

        async def text(self):
            """Returns a fake (but with the expected format) answer."""
            return "Niveau: 87%\nEn charge: OUI\nAlim. connectée: NON"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            return None

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit(session)

    info = await lib.battInfo(URL)

    assert isinstance(info, dict)
    assert set(info.keys()) == {"level", "charging", "power"}
    assert isinstance(info["level"], int)
    assert isinstance(info["charging"], bool)
    assert isinstance(info["power"], bool)
    assert info == {"level": 87, "charging": True, "power": False}

    # keep assertion flexible re: extra kwargs
    assert session.get.await_args.args[0] == f"{URL}/?action=battInfo"


@pytest.mark.asyncio
async def test_battInfo_preserves_existing_query():
    """Test the action is added without discarding existing query parameters."""
    lib = await jpiInit(MagicMock())
    lib.get = AsyncMock(
        return_value={"text": "Niveau: 87%\nEn charge: OUI\nAlim. connectée: NON"}
    )

    await lib.battInfo(f"{URL}?token=secret")

    lib.get.assert_awaited_once_with(f"{URL}/?token=secret&action=battInfo")
