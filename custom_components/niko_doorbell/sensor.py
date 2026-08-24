"""Sensor platform for Niko Doorbell (call status, mute status)."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NikoDoorbellCoordinator
from .entity import NikoDoorbellEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator: NikoDoorbellCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            NikoDoorbellCallStatusSensor(coordinator),
            NikoDoorbellMuteStatusSensor(coordinator),
        ]
    )


class NikoDoorbellCallStatusSensor(NikoDoorbellEntity, SensorEntity):
    """Reports whether the doorbell currently has an active call."""

    _attr_translation_key = "call_status"
    _attr_device_class = None
    _attr_options = ["idle", "ringing"]

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_call_status"

    @property
    def native_value(self) -> str:
        return "ringing" if self.coordinator.data.call_active else "idle"


class NikoDoorbellMuteStatusSensor(NikoDoorbellEntity, SensorEntity):
    """Reports whether the doorbell's ringer/audio is muted."""

    _attr_translation_key = "mute_status"
    _attr_options = ["muted", "unmuted"]
    _attr_entity_registry_enabled_default = True

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_mute_status"

    @property
    def native_value(self) -> str:
        return "muted" if self.coordinator.data.muted else "unmuted"
