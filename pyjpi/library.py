"""
A library to interact with JPI devices.
Rationale: according to HomeAssistant documentation, the integration MUST not interact directly with the physical devices.
Instead, it MUST use a library published on pyPI repository.
This file is so the first version of such the interaction library.
"""

from __future__ import annotations

from datetime import datetime
import logging

from aiohttp.web import HTTPError


class JPILibrary:
    """Class for the pyJPI library."""

    def __init__(self, session, version):
        """Initialize a HTTP session."""
        self._session = session
        self._initialized = datetime.now()
        self._log = logging.getLogger(__name__)
        self._log.debug("JPILibrary v%s successfully instantiated", version)

    def _batt_parse_text(self, text: str) -> dict:
        """
        Parse battery info text into a structured dictionary.
        Input:
            Niveau: 52%
            En charge: NON
            Alim. connectée: NON
        Output:
            {'level': 52, 'charging': False, 'power': False}
        """
        result = {}
        for line in text.splitlines():
            if not line.strip():
                continue  # skip empty lines
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "Niveau":
                result["level"] = int(value.strip("%"))
            elif key == "En charge":
                result["charging"] = value.upper() == "OUI"
            elif key == "Alim. connectée":
                result["power"] = value.upper() == "OUI"
        return result

    async def battInfo(self, url: str):
        """
        Returns the battery informations as a hash:
            level: <int>
            charging: <bool>
            power: <bool>
        """
        target = f"{url}?action=battInfo"
        resp = await self.get(target)
        result = None
        self._log.debug("battInfo resp=%s", resp)
        if resp:
            result = self._batt_parse_text(resp["text"])
        return result

    async def getDeviceName(self, url: str):
        """
        Returns the device name as provided by the manufacturer.
        E.g. Samsung sets that as 'Samsung SM-J320FN' for a Galaxy J3.
        """
        target = f"{url}?action=getDeviceName"
        resp = await self.get(target)
        self._log.debug("getDeviceName resp=%s", resp)
        device_name = None
        if resp:
            device_name = resp["text"]
        return device_name

    async def get(self, url: str):
        """
        Returns an object containing the raw HTTP response from GETting the provided url plus the got text content.
        Uses async I/O to avoid blocking the main event loop.
        Throw an exception in case of an error.
        """
        resp = None
        result = None
        try:
            resp = await self._session.get(url)
        except HTTPError as e:
            self._log.error("HTTPError exception: %s", e)
            return False
        if resp:
            text = await resp.text()
            result = {"text": text, "resp": resp}
        return result
