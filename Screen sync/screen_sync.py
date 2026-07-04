import asyncio
import time

import numpy as np
from mss import mss
from aioesphomeapi import APIClient, APIConnectionError, LightInfo

LAMP_IP = "192.168.0.193"
API_PORT = 6053
API_PASSWORD = ""
NOISE_PSK = None

CAPTURE_FPS = 30
DOWNSAMPLE = 8
EDGE_FRAC = 0.10
SMOOTHING = 0.1
SATURATION_BOOST = 1.3
MIN_BRIGHTNESS = 0.08

RECONNECT_DELAY = 2.0


def boost_saturation(r, g, b, factor):
    avg = (r + g + b) / 3.0
    return tuple(
        max(0, min(255, int(avg + (c - avg) * factor)))
        for c in (r, g, b)
    )


def make_regions(full):
    w, h = full["width"], full["height"]
    L, T = full["left"], full["top"]
    ew, eh = int(w * EDGE_FRAC), int(h * EDGE_FRAC)
    return [
        {"left": L,          "top": T, "width": ew, "height": h},
        {"left": L + w - ew, "top": T, "width": ew, "height": h},
        {"left": L + ew,     "top": T, "width": w - 2 * ew, "height": eh},
    ]


def get_screen_color(sct, regions):
    sums = np.zeros(3)
    count = 0
    for reg in regions:
        img = sct.grab(reg)
        px = np.frombuffer(img.raw, dtype=np.uint8).reshape(img.height, img.width, 4)
        s = px[::DOWNSAMPLE, ::DOWNSAMPLE, :3]
        sums += s.reshape(-1, 3).sum(axis=0)
        count += s.shape[0] * s.shape[1]
    avg = sums / count
    return int(avg[2]), int(avg[1]), int(avg[0])


def to_esphome(r, g, b):
    peak = max(r, g, b)
    if peak == 0:
        return (1.0, 1.0, 1.0), MIN_BRIGHTNESS
    rgb = (r / peak, g / peak, b / peak)
    brightness = max(MIN_BRIGHTNESS, peak / 255.0)
    return rgb, brightness


async def connect(cli):
    await cli.connect(login=True)
    entities, _ = await cli.list_entities_services()
    for e in entities:
        if isinstance(e, LightInfo):
            print(f"Connected. Light entity: {e.name} (key={e.key})")
            return e.key
    raise RuntimeError("No light entity found on device")


async def run():
    print("Screen Ambilight - ESPHome native API")
    print(f"Target: {LAMP_IP}:{API_PORT} @ {CAPTURE_FPS}fps")
    print("Ctrl+C to stop\n")

    cli = APIClient(LAMP_IP, API_PORT, API_PASSWORD, noise_psk=NOISE_PSK)
    light_key = None

    smooth = np.array([128.0, 128.0, 128.0])
    frame_time = 1.0 / CAPTURE_FPS

    with mss() as sct:
        regions = make_regions(sct.monitors[1])
        print(f"Sampling edges: left/right bars + top bar ({int(EDGE_FRAC * 100)}%)\n")

        while True:
            start = time.perf_counter()

            if light_key is None:
                try:
                    light_key = await connect(cli)
                except (APIConnectionError, OSError) as e:
                    print(f"\rConnect failed ({e}), retrying...", end="")
                    await asyncio.sleep(RECONNECT_DELAY)
                    continue

            r, g, b = get_screen_color(sct, regions)
            if SATURATION_BOOST != 1.0:
                r, g, b = boost_saturation(r, g, b, SATURATION_BOOST)

            smooth = smooth * SMOOTHING + np.array([r, g, b]) * (1 - SMOOTHING)
            rgb, brightness = to_esphome(*smooth.astype(int))

            try:
                cli.light_command(
                    key=light_key,
                    state=True,
                    rgb=(float(rgb[0]), float(rgb[1]), float(rgb[2])),
                    brightness=float(brightness),
                )
                print(
                    f"\rRGB: ({int(smooth[0]):3}, {int(smooth[1]):3},"
                    f" {int(smooth[2]):3})  bri: {brightness:.2f}",
                    end="",
                )
            except (APIConnectionError, OSError):
                print("\nLost connection, reconnecting...")
                light_key = None
                try:
                    await cli.disconnect()
                except Exception:
                    pass
                continue
            except Exception as e:
                print(f"\nSend error: {type(e).__name__}: {e}")

            elapsed = time.perf_counter() - start
            await asyncio.sleep(max(0.0, frame_time - elapsed))


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nStopped.")
