"""Constants for the Niko Doorbell integration."""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "niko_doorbell"

CONF_RTSP_PORT = "rtsp_port"
CONF_STREAM_PATH = "stream_path"
CONF_VERIFY_SSL = "verify_ssl"

DEFAULT_PORT = 80
DEFAULT_RTSP_PORT = 554
DEFAULT_STREAM_PATH = "/live/stream1"
DEFAULT_TIMEOUT = 10

UPDATE_INTERVAL = timedelta(seconds=5)

ATTR_CALL_ACTIVE = "call_active"
ATTR_MUTED = "muted"

MANUFACTURER = "Niko"
MODEL = "Doorbell NHC1"
