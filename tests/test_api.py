"""Tests for the Niko Doorbell API client."""
from __future__ import annotations

from unittest.mock import MagicMock

import aiohttp
import pytest

from custom_components.niko_doorbell.api import (
    PATH_HANGUP,
    PATH_MUTE,
    PATH_STATUS,
    NikoDoorbellApiClient,
    NikoDoorbellApiError,
    NikoDoorbellAuthError,
)


class FakeResponse:
    """Minimal stand-in for aiohttp.ClientResponse, used as an async context manager."""

    def __init__(self, status=200, json_data=None, content_type="application/json"):
        self.status = status
        self.content_type = content_type
        self._json_data = json_data if json_data is not None else {}

    async def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status >= 400:
            raise aiohttp.ClientResponseError(
                request_info=MagicMock(), history=(), status=self.status
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False


def make_client(response: FakeResponse) -> NikoDoorbellApiClient:
    session = MagicMock()
    session.request = MagicMock(return_value=response)
    return NikoDoorbellApiClient(session, "1.2.3.4", 80)


async def test_get_status():
    """Status is parsed correctly from the doorbell response."""
    client = make_client(
        FakeResponse(
            json_data={"call_active": True, "muted": False, "firmware_version": "1.2.3"}
        )
    )

    status = await client.async_get_status()

    assert status.call_active is True
    assert status.muted is False
    assert status.firmware_version == "1.2.3"


async def test_get_status_auth_error():
    """A 401 response is surfaced as an auth error."""
    client = make_client(FakeResponse(status=401))

    with pytest.raises(NikoDoorbellAuthError):
        await client.async_get_status()


async def test_get_status_connection_error():
    """A 500 response is surfaced as a generic API error."""
    client = make_client(FakeResponse(status=500))

    with pytest.raises(NikoDoorbellApiError):
        await client.async_get_status()


async def test_set_mute():
    """Muting sends the expected payload."""
    client = make_client(FakeResponse())

    await client.async_set_mute(True)

    client._session.request.assert_called_once()
    args, kwargs = client._session.request.call_args
    assert args[0] == "POST"
    assert args[1] == f"http://1.2.3.4:80{PATH_MUTE}"
    assert kwargs["json"] == {"muted": True}


async def test_hangup():
    """Hangup calls the expected endpoint."""
    client = make_client(FakeResponse())

    await client.async_hangup()

    client._session.request.assert_called_once()
    args, _kwargs = client._session.request.call_args
    assert args[0] == "POST"
    assert args[1] == f"http://1.2.3.4:80{PATH_HANGUP}"
