"""Tests for JPILibrary methods."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from pyjpi import jpiInit

from .const import URL

@pytest.mark.asyncio
async def test_battInfo_parses_and_returns_expected_dict():
    class FakeResp:
        status = 200
        def raise_for_status(self):
            return None
        async def text(self):
            return "Niveau: 87%\nEn charge: OUI\nAlim. connectée: NON"
        async def __aenter__(self):
            return self
        async def __aexit__(self, *exc):
            return None

    session = MagicMock()
    session.get = AsyncMock(return_value=FakeResp())

    lib = await jpiInit(session)

    info = await lib.battInfo( URL )

    assert isinstance(info, dict)
    assert set(info.keys()) == {"level", "charging", "power"}
    assert isinstance(info["level"], int)
    assert isinstance(info["charging"], bool)
    assert isinstance(info["power"], bool)
    assert info == {"level": 87, "charging": True, "power": False}

    # keep assertion flexible re: extra kwargs
    assert session.get.await_args.args[0] == f"{URL}?action=battInfo"
