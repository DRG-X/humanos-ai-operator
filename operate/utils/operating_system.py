# please remember this mf .. all executor functions should return bool indicating success/failure becuase everything depends on them

import pyautogui
import time
from typing import Optional
import math

from operate.utils.misc import convert_percent_to_decimal

class OperatingSystem:
    def __init__(self, typing_interval: float = 0.01):
        """
        typing_interval: delay between keystrokes (seconds)
        """
        self.typing_interval = typing_interval

    def write(self, content: str) -> bool:
        """
        Types text into the currently focused input.

        Assumptions (for MVP):
        - Correct window/input is already focused
        - content is trusted
        """

        if not isinstance(content, str): 
            raise ValueError("write() expects a string")

        # Normalize text
        content = content.replace("\\n", "\n")

        if len(content) == 0:
            return True  # nothing to type

        try:
            # Use bulk typing (fast & reliable for MVP)
            pyautogui.write(
                content,
                interval=self.typing_interval
            )
            return True

        except Exception as e:
            print("[OperatingSystem][write] failed:", e)
            return False

    def press(self, keys):
        try:
            for key in keys:
                pyautogui.keyDown(key)
            time.sleep(0.1)
            for key in keys:
                pyautogui.keyUp(key)
            return True
        except Exception as e:
            print("[OperatingSystem][press] error:", e)
            return False

    def mouse(self, click_detail) -> bool:
        try:
            x = convert_percent_to_decimal(click_detail.get("x"))
            y = convert_percent_to_decimal(click_detail.get("y"))
            return self.click_at_percentage(x, y)
        except Exception as e:
            print("[OperatingSystem][mouse] error:", e)
            return False

    def click_at_percentage(self, x_percent: float, y_percent: float):
        try:
            screen_width, screen_height = pyautogui.size()
            x_pixel = int(screen_width * x_percent)
            y_pixel = int(screen_height * y_percent)
            pyautogui.moveTo(x_pixel, y_pixel)
            pyautogui.click()
            return True
        
        except Exception as e:
            print("[OperatingSystem][click_at_percentage] error:", e)
            return False
        
        
    def click(self, x: float, y: float) -> bool:
        """
        Adapter for executor-level click action.
        Expects normalized coordinates (0.0–1.0).
        """
        return self.click_at_percentage(x, y)