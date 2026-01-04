"""
Screen Ambilight for Color Shadow Lamp
Captures average screen color and sends to ESPHome via HTTP

pip install mss numpy requests
"""

import time
import numpy as np
from mss import mss
import requests

# ============================================
# CONFIGURATION
# ============================================
LAMP_IP = "192.168.0.193"  # Your lamp's IP

# Capture settings
CAPTURE_FPS = 15  # Target frames per second (HTTP is slower than UDP)
DOWNSAMPLE = 8    # Sample every Nth pixel (faster processing)

# Color smoothing (prevents flickering)
SMOOTHING = 0.3   # 0 = instant, 1 = very slow transitions

# Brightness/saturation boost (makes colors pop more)
SATURATION_BOOST = 1.3  # 1.0 = normal, 1.5 = more vivid
MIN_BRIGHTNESS = 20     # Minimum brightness to send (0-255)

# ============================================
# MAIN CODE
# ============================================

def boost_saturation(r, g, b, factor):
    """Quick saturation boost"""
    avg = (r + g + b) / 3
    r = int(avg + (r - avg) * factor)
    g = int(avg + (g - avg) * factor)
    b = int(avg + (b - avg) * factor)
    return (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b))
    )

def get_screen_color(sct, monitor):
    """Capture screen and return average RGB"""
    img = sct.grab(monitor)
    
    # Convert to numpy array (BGRA format)
    pixels = np.frombuffer(img.raw, dtype=np.uint8)
    pixels = pixels.reshape((img.height, img.width, 4))
    
    # Sample every Nth pixel for speed
    sampled = pixels[::DOWNSAMPLE, ::DOWNSAMPLE, :3]
    avg = np.mean(sampled.reshape(-1, 3), axis=0)
    
    # BGR to RGB
    return int(avg[2]), int(avg[1]), int(avg[0])

def send_color(ip, r, g, b):
    """Send RGB color to ESPHome lamp via HTTP"""
    url = f"http://{ip}/light/color_shadow_lamp/turn_on?brightness=255&r={r}&g={g}&b={b}"
    try:
        requests.get(url, timeout=0.5)
    except:
        pass  # Don't block on timeout

def main():
    print(f"Screen Ambilight for Color Shadow Lamp")
    print(f"Target: {LAMP_IP}")
    print(f"Press Ctrl+C to stop\n")
    
    # Smoothed color values
    smooth_r, smooth_g, smooth_b = 128.0, 128.0, 128.0
    last_r, last_g, last_b = -1, -1, -1
    
    frame_time = 1.0 / CAPTURE_FPS
    
    with mss() as sct:
        # Use primary monitor (index 1)
        monitor = sct.monitors[1]
        print(f"Capturing: {monitor['width']}x{monitor['height']}")
        print(f"FPS target: {CAPTURE_FPS}\n")
        
        while True:
            start = time.perf_counter()
            
            try:
                # Get average screen color
                r, g, b = get_screen_color(sct, monitor)
                
                # Boost saturation
                if SATURATION_BOOST != 1.0:
                    r, g, b = boost_saturation(r, g, b, SATURATION_BOOST)
                
                # Smooth the color transition
                smooth_r = smooth_r * SMOOTHING + r * (1 - SMOOTHING)
                smooth_g = smooth_g * SMOOTHING + g * (1 - SMOOTHING)
                smooth_b = smooth_b * SMOOTHING + b * (1 - SMOOTHING)
                
                # Convert to int
                out_r = int(smooth_r)
                out_g = int(smooth_g)
                out_b = int(smooth_b)
                
                # Only send if color changed enough (reduces HTTP spam)
                if (abs(out_r - last_r) > 5 or 
                    abs(out_g - last_g) > 5 or 
                    abs(out_b - last_b) > 5):
                    send_color(LAMP_IP, out_r, out_g, out_b)
                    last_r, last_g, last_b = out_r, out_g, out_b
                
                # Debug output
                print(f"\rRGB: ({out_r:3}, {out_g:3}, {out_b:3})", end="")
                
            except Exception as e:
                print(f"\nError: {e}")
            
            # Maintain target FPS
            elapsed = time.perf_counter() - start
            if elapsed < frame_time:
                time.sleep(frame_time - elapsed)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
