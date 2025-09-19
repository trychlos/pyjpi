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


# pylint: disable=import-outside-toplevel, too-few-public-methods
@pytest.mark.asyncio
async def test_jpiInit_falls_back_to_local_version(monkeypatch):
    """Test for PackageNotFoundError exception."""
    import pyjpi as pkg
    from importlib.metadata import PackageNotFoundError

    # Make version lookup fail
    def fake_version(_):
        raise PackageNotFoundError

    monkeypatch.setattr(pkg, "version", fake_version)

    # Capture what jpiInit passes to JPILibrary
    captured = {}

    class FakeLib:  # pylint: disable R0903
        """A fake library class to raise the expected exception."""

        def __init__(self, session, package_version):
            captured["session"] = session
            captured["version"] = package_version

    monkeypatch.setattr(pkg, "JPILibrary", FakeLib)

    session = MagicMock()
    lib = await jpiInit(session)

    assert isinstance(lib, FakeLib)
    assert captured["version"] == "0+local"
    assert captured["session"] is session
