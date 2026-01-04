# Color Shadow Lamp — ESPHome + Screen Sync

ESPHome firmware for the [RCTestFlight Color Shadow Lamp](https://www.rctestflight.com/store/p/color-shadow-lamp), [Github](https://github.com/rctestflight/Color-Shadow-Lamp) with PC screen sync (ambilight) support.

Based on [meslater's ESPHome port](https://github.com/meslater/Color-Shadow-Lamp) which preserves manual RGB control via the knobs while adding WiFi connectivity.

## Features

- **Screen Sync**: Python script captures your PC screen color and sends it to the lamp in real-time
- **WiFi Control**: Control the lamp over your network via HTTP
- **Manual Control**: Knobs and button still work exactly like the original firmware
- **Web Interface**: Access the lamp at `http://<lamp-ip>` 
- **OTA Updates**: Update firmware over WiFi after initial flash
- **Home Assistant Ready**: Works with ESPHome integration (optional)

## Quick Start

### 1. Flash the Firmware

```bash
cd esphome
pip install esphome
```

Put the lamp in boot mode (hold button → plug in 12V → plug in USB → release), then:

```bash
esphome run color_shadow.yaml --device COM* ##Check your port where lamp is plugged in. 
```

### 2. Connect to WiFi

1. Connect your phone to the **"Color Shadow Setup"** WiFi network
2. Open `http://192.168.4.1` in your browser
3. Enter your home WiFi credentials
4. The lamp will reboot and join your network

### 3. Find the Lamp's IP

Check your router's admin page for "color-shadow-lamp" or try:

```bash
ping color-shadow-lamp.local
```

### 4. Test It

Open in browser or curl:

```bash
curl "http://<lamp-ip>/light/color_shadow_lamp/turn_on?brightness=255&r=255&g=0&b=0"
```

The lamp should turn red.

## Screen Sync (Ambilight)

The Python script captures your screen's average color and sends it to the lamp.

### Install

```bash
pip install mss numpy requests
```

### Run

```bash
python Screen sync/screen_sync.py
```

### Configuration

Edit the script to tune these settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `LAMP_IP` | `192.168.0.193` | Your lamp's IP address |
| `CAPTURE_FPS` | `15` | Updates per second (10-30) |
| `SMOOTHING` | `0.3` | Transition smoothness (0.1 = snappy, 0.5 = smooth) |
| `SATURATION_BOOST` | `1.3` | Color intensity (1.0 = natural, 2.0 = vivid) |
| `DOWNSAMPLE` | `8` | Pixel sampling rate (lower = more accurate) |

## Hardware

- **Lamp**: [Color Shadow Lamp from RCTestFlight](https://www.rctestflight.com/store/p/color-shadow-lamp)
- **Chip**: ESP32-C3

## Credits

- Original lamp & firmware: [RCTestFlight](https://github.com/rctestflight/Color-Shadow-Lamp)
- ESPHome port: [meslater](https://github.com/meslater/Color-Shadow-Lamp)
- Screen sync: Added in this fork

## License

MIT
