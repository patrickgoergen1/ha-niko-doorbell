"""Lightweight HTTP client for the Niko Doorbell (NHC1) local API.

The doorbell exposes a small local REST API used to read call/mute state
and to trigger the mute switch and hangup button. Endpoint paths are
defined as constants below so they can be adjusted in one place if a
firmware revision changes them.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import aiohttp
from aiohttp import BasicAuth

from .const import DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)

PATH_STATUS = "/api/v1/status"
PATH_MUTE = "/api/v1/mute"
PATH_HANGUP = "/api/v1/hangup"


class NikoDoorbellApiError(Exception):
    """Raised for any communication error with the doorbell."""


class NikoDoorbellAuthError(NikoDoorbellApiError):
    """Raised when authentication with the doorbell fails."""


@dataclass
class NikoDoorbellStatus:
    """Snapshot of the doorbell state."""

    call_active: bool
    muted: bool
    firmware_version: str | None = None
    serial_number: str | None = None


class NikoDoorbellApiClient:
    """Talks to a single Niko Doorbell unit over its local REST API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        host: str,
        port: int,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool = True,
    ) -> None:
        self._session = session
        self._base_url = f"http://{host}:{port}"
        self._auth = BasicAuth(username, password) if username else None
        self._verify_ssl = verify_ssl

    async def async_get_status(self) -> NikoDoorbellStatus:
        """Fetch the current call/mute status from the doorbell."""
        data = await self._request("GET", PATH_STATUS)
        return NikoDoorbellStatus(
            call_active=bool(data.get("call_active", False)),
            muted=bool(data.get("muted", False)),
            firmware_version=data.get("firmware_version"),
            serial_number=data.get("serial_number"),
        )

    async def async_set_mute(self, muted: bool) -> None:
        """Mute or unmute the doorbell."""
        await self._request("POST", PATH_MUTE, json={"muted": muted})

    async def async_hangup(self) -> None:
        """Terminate an active call."""
        await self._request("POST", PATH_HANGUP)

    async def async_test_connection(self) -> None:
        """Validate host/credentials, raising on failure. Used by config flow."""
        await self.async_get_status()

    async def _request(
        self, method: str, path: str, json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        try:
            async with asyncio.timeout(DEFAULT_TIMEOUT):
                async with self._session.request(
                    method,
                    url,
                    json=json,
                    auth=self._auth,
                    ssl=self._verify_ssl if url.startswith("https") else None,
                ) as response:
                    if response.status in (401, 403):
                        raise NikoDoorbellAuthError(
                            f"Authentication failed ({response.status})"
                        )
                    response.raise_for_status()
                    if response.content_type == "application/json":
                        return await response.json()
                    return {}
        except NikoDoorbellAuthError:
            raise
        except TimeoutError as err:
            raise NikoDoorbellApiError(f"Timeout communicating with {url}") from err
        except aiohttp.ClientError as err:
            raise NikoDoorbellApiError(f"Error communicating with {url}: {err}") from err
