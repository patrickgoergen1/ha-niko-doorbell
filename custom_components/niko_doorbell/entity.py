"""Base entity for Niko Doorbell entities."""
from __future__ import annotations

from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_info import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import NikoDoorbellCoordinator


class NikoDoorbellEntity(CoordinatorEntity[NikoDoorbellCoordinator]):
    """Base class tying an entity to the doorbell device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        super().__init__(coordinator)
        entry = coordinator.entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer=MANUFACTURER,
            model=MODEL,
            configuration_url=f"http://{entry.data[CONF_HOST]}",
            sw_version=coordinator.data.firmware_version if coordinator.data else None,
        )
