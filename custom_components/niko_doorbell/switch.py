"""Switch platform for Niko Doorbell (mute switch)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NikoDoorbellCoordinator
from .entity import NikoDoorbellEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the switch platform."""
    coordinator: NikoDoorbellCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NikoDoorbellMuteSwitch(coordinator)])


class NikoDoorbellMuteSwitch(NikoDoorbellEntity, SwitchEntity):
    """Mutes/unmutes the doorbell's ringer and call audio."""

    _attr_translation_key = "mute"

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_mute_switch"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.muted

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.client.async_set_mute(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.client.async_set_mute(False)
        await self.coordinator.async_request_refresh()
