# Local API notes

This document explains the assumptions the integration makes about the
Niko Doorbell's local API, since Niko does not publish an official spec
for it.

## Status endpoint

`GET /api/v1/status`

Expected JSON response:

```json
{
  "call_active": false,
  "muted": false,
  "firmware_version": "1.2.3",
  "serial_number": "ABC123"
}
```

Only `call_active` and `muted` are required; the other fields are used for
device info if present and are otherwise ignored.

## Mute endpoint

`POST /api/v1/mute`

Request body:

```json
{ "muted": true }
```

## Hangup endpoint

`POST /api/v1/hangup`

No request body.

## Video stream

The camera entity builds an RTSP URL from the configured host, RTSP port
(default `554`) and stream path (default `/live/stream1`):

```
rtsp://[username:password@]<host>:<rtsp_port><stream_path>
```

Home Assistant's built-in `stream` integration handles the actual RTSP →
HLS conversion for the live view and thumbnails.

## Adjusting these defaults

All paths above are defined as constants near the top of
[`custom_components/niko_doorbell/api.py`](../custom_components/niko_doorbell/api.py),
and the RTSP port/stream path are configurable in the config flow. If your
doorbell uses different values, either:

- change them through **Settings → Devices & Services → Niko Doorbell →
  Configure** (for RTSP port/path), or
- edit the `PATH_*` constants in `api.py` and open a pull request so the
  defaults work out of the box for others.
