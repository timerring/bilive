# Copyright (c) 2024 bilive.

import subprocess
from src.config import SRC_DIR
from src.log.logger import scan_log
import os

# Generate the srt file via whisper model
def generate_subtitles(in_video_path):
    """Generate subtitles via whisper model
    Args:
        in_video_path: str, the path of video
    """
    try:
        subprocess.run(
            ['python', os.path.join(SRC_DIR, 'subtitle', 'generate.py'), in_video_path],
            stdout=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Generate subtitles failed: {e.stderr}")