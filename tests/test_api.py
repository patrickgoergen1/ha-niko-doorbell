"""Tests for the Niko Doorbell API client."""
from __future__ import annotations

import pytest
from aioresponses import aioresponses

from custom_components.niko_doorbell.api import (
    PATH_HANGUP,
    PATH_MUTE,
    PATH_STATUS,
    NikoDoorbellApiClient,
    NikoDoorbellApiError,
    NikoDoorbellAuthError,
)


@pytest.fixture
def mock_aiohttp():
    with aioresponses() as m:
        yield m


async def test_get_status(hass, mock_aiohttp):
    """Status is parsed correctly from the doorbell response."""
    mock_aiohttp.get(
        f"http://1.2.3.4:80{PATH_STATUS}",
        payload={"call_active": True, "muted": False, "firmware_version": "1.2.3"},
    )
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    client = NikoDoorbellApiClient(session, "1.2.3.4", 80)

    status = await client.async_get_status()

    assert status.call_active is True
    assert status.muted is False
    assert status.firmware_version == "1.2.3"


async def test_get_status_auth_error(hass, mock_aiohttp):
    """A 401 response is surfaced as an auth error."""
    mock_aiohttp.get(f"http://1.2.3.4:80{PATH_STATUS}", status=401)
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    client = NikoDoorbellApiClient(session, "1.2.3.4", 80)

    with pytest.raises(NikoDoorbellAuthError):
        await client.async_get_status()


async def test_get_status_connection_error(hass, mock_aiohttp):
    """A 500 response is surfaced as a generic API error."""
    mock_aiohttp.get(f"http://1.2.3.4:80{PATH_STATUS}", status=500)
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    client = NikoDoorbellApiClient(session, "1.2.3.4", 80)

    with pytest.raises(NikoDoorbellApiError):
        await client.async_get_status()


async def test_set_mute(hass, mock_aiohttp):
    """Muting sends the expected payload."""
    mock_aiohttp.post(f"http://1.2.3.4:80{PATH_MUTE}", payload={})
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    client = NikoDoorbellApiClient(session, "1.2.3.4", 80)

    await client.async_set_mute(True)


async def test_hangup(hass, mock_aiohttp):
    """Hangup calls the expected endpoint."""
    mock_aiohttp.post(f"http://1.2.3.4:80{PATH_HANGUP}", payload={})
    session = hass.helpers.aiohttp_client.async_get_clientsession()
    client = NikoDoorbellApiClient(session, "1.2.3.4", 80)

    await client.async_hangup()
