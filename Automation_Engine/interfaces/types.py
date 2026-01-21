# interfaces/types.py

from dataclasses import dataclass
from typing import Optional
import numpy as np
import time


@dataclass
class ScreenFrame:
    image: np.ndarray          # raw image (RGB or BGR)
    width: int
    height: int
    timestamp: float = time.time()
 

@dataclass
class Action:
    type: str                  # "click", "type", "scroll", etc.
    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None


@dataclass
class ActionResult:
    success: bool
    reason: Optional[str] = None
