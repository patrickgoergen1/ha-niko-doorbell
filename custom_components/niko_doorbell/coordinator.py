"""DataUpdateCoordinator for the Niko Doorbell integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import NikoDoorbellApiClient, NikoDoorbellApiError, NikoDoorbellStatus
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class NikoDoorbellCoordinator(DataUpdateCoordinator[NikoDoorbellStatus]):
    """Polls the doorbell for call/mute status."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, client: NikoDoorbellApiClient
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.entry = entry
        self.client = client

    async def _async_update_data(self) -> NikoDoorbellStatus:
        try:
            return await self.client.async_get_status()
        except NikoDoorbellApiError as err:
            raise UpdateFailed(f"Error fetching Niko Doorbell status: {err}") from err
