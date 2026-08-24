"""Tests for the Niko Doorbell config flow."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

from custom_components.niko_doorbell.api import (
    NikoDoorbellApiError,
    NikoDoorbellAuthError,
    NikoDoorbellStatus,
)
from custom_components.niko_doorbell.const import DOMAIN

USER_INPUT = {
    "host": "1.2.3.4",
    "port": 80,
    "rtsp_port": 554,
    "stream_path": "/live/stream1",
    "verify_ssl": True,
}


async def test_user_flow_success(hass):
    """A successful connection creates a config entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM

    # The config flow only calls async_test_connection, but creating the
    # entry also triggers a real integration setup in the background (via
    # the coordinator's first refresh), so async_get_status needs mocking
    # too or it will try to open a real socket.
    with (
        patch(
            "custom_components.niko_doorbell.config_flow.NikoDoorbellApiClient.async_test_connection",
            new=AsyncMock(return_value=None),
        ),
        patch(
            "custom_components.niko_doorbell.api.NikoDoorbellApiClient.async_get_status",
            new=AsyncMock(return_value=NikoDoorbellStatus(call_active=False, muted=False)),
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Niko Doorbell (1.2.3.4)"
    assert result["data"] == USER_INPUT


async def test_user_flow_cannot_connect(hass):
    """A connection error keeps the user on the form with an error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.niko_doorbell.config_flow.NikoDoorbellApiClient.async_test_connection",
        new=AsyncMock(side_effect=NikoDoorbellApiError("boom")),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_invalid_auth(hass):
    """An auth error keeps the user on the form with an error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.niko_doorbell.config_flow.NikoDoorbellApiClient.async_test_connection",
        new=AsyncMock(side_effect=NikoDoorbellAuthError("boom")),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], USER_INPUT
        )

    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}
