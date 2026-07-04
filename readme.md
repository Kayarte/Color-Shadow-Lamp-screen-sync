# Color Shadow Lamp — ESPHome + Screen Sync

ESPHome firmware for the [RCTestFlight Color Shadow Lamp](https://www.rctestflight.com/store/p/color-shadow-lamp), [Github](https://github.com/rctestflight/Color-Shadow-Lamp) with PC screen sync (ambilight) support.

Based on [meslater's ESPHome port](https://github.com/meslater/Color-Shadow-Lamp).

## UPDATE*
Connect lamp to same network where you run this from.
pip install aioesphomeapi
cd to the .\Color-Shadow-Lamp-screen-sync\esphome 
esphome run color_shadow.yaml
wait...
wait..
wait.
when done, it should tell you: "
INFO Successfully compiled program.
INFO Connecting to 192.168.0.193 port 6767...
"
unplug lamp, wait, plug lamp back in.
run screen_sync.py

you can see logs and other settinga at 192.168.0.193

you may nee you press the button to turn off maunal control the log should tell you.

Now it does EDGE sampling, so its a nice gaming, or movie pc back light using this cool lamp.

## Hardware

- **Lamp**: [Color Shadow Lamp from RCTestFlight](https://www.rctestflight.com/store/p/color-shadow-lamp)
- **Chip**: ESP32-C3

## Credits

- Original lamp & firmware: [RCTestFlight](https://github.com/rctestflight/Color-Shadow-Lamp)
- ESPHome port: [meslater](https://github.com/meslater/Color-Shadow-Lamp)
- Screen sync: Added in this fork
