"""JPI Library."""

from __future__ import annotations

import asyncio
import importlib.metadata

import aiohttp

from .library import JPILibrary


async def jpiInit(session: aiohttp.ClientSession) -> JPILibrary:
    """
    Initialize the library.
    Returns an object with an initialized HTTP session.
    This same object will have to be provided later on each called method.
    """
    version = await asyncio.to_thread(importlib.metadata.version, "pyJPI")
    return JPILibrary(session, version)
