# Copyright (c) 2024 bilive.

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .auto_slice_video.autosv import slice_video_by_danmaku

__all__ = ["slice_video_by_danmaku"]
