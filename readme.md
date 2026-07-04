# Color Shadow Lamp — ESPHome + Screen Sync

ESPHome firmware for the [RCTestFlight Color Shadow Lamp](https://www.rctestflight.com/store/p/color-shadow-lamp), [Github](https://github.com/rctestflight/Color-Shadow-Lamp) with PC screen sync (ambilight) support.

Based on [meslater's ESPHome port](https://github.com/meslater/Color-Shadow-Lamp).

## UPDATE

Connect lamp to same network where you run this from.

```bash
pip install aioesphomeapi
cd .\Color-Shadow-Lamp-screen-sync\esphome
esphome run color_shadow.yaml
```

Wait for it to finish. When done, it should tell you:
INFO Successfully compiled program.
INFO Connecting to 192.168.0.193 port 6767...

Unplug the lamp, wait a sec, plug it back in.

Run `screen_sync.py`

You can view logs and other settings at `192.168.0.193`.

You may need to press the button to turn off manual control — the log will tell you.

Now it does **edge sampling**, so it works great as a gaming or movie PC backlight with this cool lamp 🔥

## Hardware

- **Lamp**: [Color Shadow Lamp from RCTestFlight](https://www.rctestflight.com/store/p/color-shadow-lamp)
- **Chip**: ESP32-C3

## Credits

- Original lamp & firmware: [RCTestFlight](https://github.com/rctestflight/Color-Shadow-Lamp)
- ESPHome port: [meslater](https://github.com/meslater/Color-Shadow-Lamp)
- Screen sync: Added in this fork
