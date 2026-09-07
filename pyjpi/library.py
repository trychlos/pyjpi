"""
A library to interact with JPI devices.
Rationale: according to HomeAssistant documentation, the integration MUST not interact directly with the physical devices.
Instead, it MUST use a library published on pyPI repository.
This file is so the first version of such the interaction library.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TypedDict

import aiohttp
from yarl import URL

from .exceptions import JPIConnectionError, JPIResponseError


class BatteryInfo(TypedDict):
    """Battery information returned by JPI."""

    level: int
    charging: bool
    power: bool


class JPIResponse(TypedDict):
    """Raw response and decoded text returned by JPI."""

    text: str
    resp: aiohttp.ClientResponse


class JPILibrary:
    """Class for the pyJPI library."""

    def __init__(self, session: aiohttp.ClientSession, version: str) -> None:
        """Initialize a HTTP session."""
        self._session = session
        self._initialized = datetime.now(UTC)
        self._log = logging.getLogger(__name__)
        self._log.debug("JPILibrary v%s successfully instantiated", version)

    def _batt_parse_text(self, text: str) -> BatteryInfo:
        """
        Parse battery info text into a structured dictionary.
        Input:
            Niveau: 52%
            En charge: NON
            Alim. connectée: NON
        Output:
            {'level': 52, 'charging': False, 'power': False}
        """
        level: int | None = None
        charging: bool | None = None
        power: bool | None = None
        try:
            for line in text.splitlines():
                if not line.strip():
                    continue

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key == "Niveau":
                    level = int(value.removesuffix("%").strip())
                elif key == "En charge":
                    charging = self._parse_boolean(value)
                elif key == "Alim. connectée":
                    power = self._parse_boolean(value)
        except ValueError as err:
            raise JPIResponseError("Invalid battery information response") from err

        if level is None or charging is None or power is None:
            raise JPIResponseError("Incomplete battery information response")

        if not 0 <= level <= 100:
            raise JPIResponseError("Battery level is outside the valid range")

        resp: BatteryInfo = {
            "level": level,
            "charging": charging,
            "power": power,
        }
        self._log.debug("battInfo parsed=%r", resp)

        return resp

    @staticmethod
    def _parse_boolean(value: str) -> bool:
        """Parse a JPI OUI/NON boolean."""
        normalized = value.upper()
        if normalized not in {"OUI", "NON"}:
            raise ValueError(f"Invalid boolean value: {value}")
        return normalized == "OUI"

    async def battInfo(self, url: str) -> BatteryInfo:
        """
        Returns the battery informations as a hash:
            level: <int>
            charging: <bool>
            power: <bool>
        """
        target = str(URL(url).update_query(action="battInfo"))
        resp = await self.get(target)
        self._log.debug("battInfo resp=%s", resp)
        return self._batt_parse_text(resp["text"])

    async def get(self, url: str) -> JPIResponse:
        """
        Returns an object containing the raw HTTP response from GETting the provided url plus the got text content.
        Uses async I/O to avoid blocking the main event loop.
        Throw an exception in case of an error.
        """
        resp: aiohttp.ClientResponse | None = None
        try:
            resp = await self._session.get(url)
            resp.raise_for_status()
            text = await resp.text()
        except aiohttp.ClientResponseError as err:
            raise JPIResponseError(
                f"JPI request failed with HTTP status {err.status}"
            ) from err
        except (aiohttp.ClientError, TimeoutError) as err:
            raise JPIConnectionError("Unable to communicate with JPI") from err
        finally:
            if resp is not None:
                resp.release()

        assert resp is not None
        return {"text": text, "resp": resp}

    async def getDeviceName(self, url: str) -> str:
        """
        Returns the device name as provided by the manufacturer.
        E.g. Samsung sets that as 'Samsung SM-J320FN' for a Galaxy J3.
        """
        target = str(URL(url).update_query(action="getDeviceName"))
        resp = await self.get(target)
        self._log.debug("getDeviceName resp=%s", resp)
        device_name = resp["text"].strip()
        if not device_name:
            raise JPIResponseError("Empty device name response")
        return device_name
