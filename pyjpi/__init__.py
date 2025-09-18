"""JPI Library."""

from __future__ import annotations

import asyncio
from importlib.metadata import PackageNotFoundError, version

import aiohttp

from .library import JPILibrary


async def _get_version() -> str:
    """Returns the version of the package (hopefully)."""
    try:
        return await asyncio.to_thread(version, "pyJPI")
    except PackageNotFoundError:
        return "0+local"


async def jpiInit(session: aiohttp.ClientSession) -> JPILibrary:
    """
    Initialize the library.
    Returns an object with an initialized HTTP session.
    This same object will have to be provided later on each called method.
    """
    package_version = await _get_version()
    return JPILibrary(session, package_version)
