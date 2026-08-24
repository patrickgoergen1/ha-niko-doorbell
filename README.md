# Niko Doorbell

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A [Home Assistant](https://www.home-assistant.io/) custom integration for the
**Niko Doorbell (NHC1)**, communicating with the doorbell over your local
network — no cloud account required.

## Features

- 📹 **RTSP Camera** — live video feed from the doorbell, shown through
  Home Assistant's built-in stream player
- ☎️ **Call status sensor** — reports `idle` / `ringing`
- 🔇 **Mute status sensor** — reports `muted` / `unmuted`
- 🔈 **Mute switch** — mute or unmute the doorbell's ringer/call audio
- ⏹️ **Hang up button** — terminate an active call
- 🧙 **Config Flow** — set up entirely from the Home Assistant UI, no YAML
- 📦 **HACS compatible** — install and update through HACS

## Supported devices

Currently tested against:

- Niko Doorbell 550-22001

Other NHC1-based Niko Doorbell models will likely work but have not been
verified yet. Please open an issue if you test this integration on a
different model.

## Requirements

- Home Assistant 2024.1.0 or newer
- The doorbell reachable on your local network (same LAN/VLAN as Home
  Assistant, or routed access to it)
- The doorbell's local IP address (and RTSP/API credentials, if configured)

## Installation

### Via HACS (recommended)

1. In Home Assistant, go to **HACS → Integrations**.
2. Click the three-dot menu → **Custom repositories**.
3. Add `https://github.com/patrickgoergen1/ha-niko-doorbell` as an
   **Integration**.
4. Find **Niko Doorbell** in HACS and click **Download**.
5. Restart Home Assistant.

### Manual installation

1. Download the latest release of this repository.
2. Copy the `custom_components/niko_doorbell` folder into your Home
   Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

Configuration is done entirely through the UI:

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Niko Doorbell**.
3. Enter the doorbell's host/IP address, REST API port, and (if your
   doorbell is secured) username/password, plus the RTSP port and stream
   path for the camera feed.
4. Submit — the integration validates the connection before creating the
   entry.

This creates one device with the following entities:

| Entity              | Platform | Description                              |
| ------------------- | -------- | ----------------------------------------- |
| Camera               | `camera` | Live RTSP video feed                      |
| Call status          | `sensor` | `idle` or `ringing`                       |
| Mute status          | `sensor` | `muted` or `unmuted`                      |
| Mute                  | `switch` | Mute/unmute the doorbell                  |
| Hang up               | `button` | Terminates an active call                 |

## A note on the local API

Niko does not publish an official specification for the NHC1 doorbell's
local REST/RTSP interface. This integration's HTTP client
(`custom_components/niko_doorbell/api.py`) is built around the most common
pattern for these devices (a small JSON status endpoint plus RTSP for
video) and is easy to adjust — the endpoint paths are defined as constants
at the top of that file. If your unit uses different paths, please open an
issue (or a pull request) with the details from your device so the defaults
can be corrected. See [`docs/api.md`](docs/api.md) for more detail on these
assumptions.

## Roadmap

See the [project issues](https://github.com/patrickgoergen1/ha-niko-doorbell/issues)
for planned work, including:

- Door opener support
- Snapshot support
- Event detection (e.g. HA events on ring/hangup)
- SIP support
- Official HACS default repository listing

## Contributing

Issues and pull requests are welcome. If you own a Niko Doorbell and can
confirm (or correct) the REST API behavior described above, that
information is especially useful.

## Status

🚧 Under active development — core entities (camera, sensors, switch,
button) and the config flow are implemented; see the Roadmap above for
what's next.

## License

See [LICENSE](LICENSE).
