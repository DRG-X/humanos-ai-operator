import mss
import numpy as np
import cv2
import base64
import json
from openai import OpenAI
import os
import time 
import logging 


logger = logging.getLogger(__name__)

screenshot_dir = "logs/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

def capture_and_optimize_screen(scale=0.5, quality=60):
    """
    Takes a screenshot using mss
    Downscales it
    Compresses it
    Returns image bytes
    """

    with mss.mss() as sct:
        monitor = sct.monitors[1]   # FIXED
        screenshot = sct.grab(monitor)

    image = np.array(screenshot)
    img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # FIXED

    h, w, _ = img.shape
    # print(f"Before downscaling: {w}x{h}, pixels={w*h}")

    logger.info(
        "ScreenShot Captured" , 
        extra = {
            "width": w,
            "height": h,
            "pixels": w*h
        }
    )

    # Downscale
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    h_ds, w_ds, _ = img.shape
    # print(f"After downscaling: {w_ds}x{h_ds}, pixels={w_ds*h_ds}")
    logger.info(
        "ScreenShot Downscaled" , 
        extra = {
            "width": w_ds,
            "height": h_ds,
            "pixels": w_ds*h_ds
        }
    )


    # Compress
    _, buffer = cv2.imencode(
        ".jpg",
        img,
        [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    )
    image_bytes = buffer.tobytes()

    logger.info(
        "ScreenShot Compressed" , 
        extra = {
            "size_bytes": len(image_bytes)
        }
    )


    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.jpg"
    image_path = os.path.join(screenshot_dir, filename)

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    logger.info(f"Screenshot saved to {image_path}")

    return image_bytes 
    

image_bytes  = capture_and_optimize_screen()
image_base64 = base64.b64encode(image_bytes).decode("utf-8")

