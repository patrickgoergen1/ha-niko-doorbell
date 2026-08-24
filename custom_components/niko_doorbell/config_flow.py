"""Config flow for the Niko Doorbell integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import NikoDoorbellApiClient, NikoDoorbellApiError, NikoDoorbellAuthError
from .const import (
    CONF_RTSP_PORT,
    CONF_STREAM_PATH,
    CONF_VERIFY_SSL,
    DEFAULT_PORT,
    DEFAULT_RTSP_PORT,
    DEFAULT_STREAM_PATH,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_USERNAME): str,
        vol.Optional(CONF_PASSWORD): str,
        vol.Optional(CONF_RTSP_PORT, default=DEFAULT_RTSP_PORT): int,
        vol.Optional(CONF_STREAM_PATH, default=DEFAULT_STREAM_PATH): str,
        vol.Optional(CONF_VERIFY_SSL, default=True): bool,
    }
)


class NikoDoorbellConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Niko Doorbell."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
            )
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(
                self.hass, verify_ssl=user_input.get(CONF_VERIFY_SSL, True)
            )
            client = NikoDoorbellApiClient(
                session=session,
                host=user_input[CONF_HOST],
                port=user_input[CONF_PORT],
                username=user_input.get(CONF_USERNAME),
                password=user_input.get(CONF_PASSWORD),
                verify_ssl=user_input.get(CONF_VERIFY_SSL, True),
            )

            try:
                await client.async_test_connection()
            except NikoDoorbellAuthError:
                errors["base"] = "invalid_auth"
            except NikoDoorbellApiError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error validating Niko Doorbell connection")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=f"Niko Doorbell ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )
