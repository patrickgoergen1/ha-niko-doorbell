"""Camera platform for Niko Doorbell (RTSP stream)."""
from __future__ import annotations

from homeassistant.components.camera import Camera, CameraEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_RTSP_PORT, CONF_STREAM_PATH, DOMAIN
from .coordinator import NikoDoorbellCoordinator
from .entity import NikoDoorbellEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the camera platform."""
    coordinator: NikoDoorbellCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NikoDoorbellCamera(coordinator)])


class NikoDoorbellCamera(NikoDoorbellEntity, Camera):
    """RTSP camera exposed by the Niko Doorbell.

    Relies on Home Assistant's built-in `stream` integration to turn the
    RTSP feed into a live view / HLS stream and thumbnail snapshots -
    no ffmpeg custom component dependency required.
    """

    _attr_translation_key = "doorbell_camera"
    _attr_supported_features = CameraEntityFeature.STREAM

    def __init__(self, coordinator: NikoDoorbellCoordinator) -> None:
        NikoDoorbellEntity.__init__(self, coordinator)
        Camera.__init__(self)
        entry = coordinator.entry
        host = entry.data[CONF_HOST]
        rtsp_port = entry.data[CONF_RTSP_PORT]
        stream_path = entry.data[CONF_STREAM_PATH]
        username = entry.data.get(CONF_USERNAME)
        password = entry.data.get(CONF_PASSWORD)

        credentials = f"{username}:{password}@" if username else ""
        self._stream_source = f"rtsp://{credentials}{host}:{rtsp_port}{stream_path}"
        self._attr_unique_id = f"{entry.entry_id}_camera"

    async def stream_source(self) -> str:
        """Return the RTSP stream URL for HA's stream integration to consume."""
        return self._stream_source

    @property
    def is_recording(self) -> bool:
        return False

    @property
    def motion_detection_enabled(self) -> bool:
        return False
