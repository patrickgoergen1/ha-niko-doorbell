"""Button platform for Niko Doorbell (hangup button)."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NikoDoorbellCoordinator
from .entity import NikoDoorbellEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the button platform."""
    coordinator: NikoDoorbellCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NikoDoorbellHangupButton(coordinator)])


class NikoDoorbellHangupButton(NikoDoorbellEntity, ButtonEntity):
    """Terminates an active call on the doorbell."""

    _attr_translation_key = "hangup"

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_hangup_button"

    async def async_press(self) -> None:
        await self.coordinator.client.async_hangup()
        await self.coordinator.async_request_refresh()
