# Copyright (c) 2024 bilive.

import os
import subprocess
from config import SRC_DIR, ASR_METHOD, WHISPER_API_KEY
from log.logger import scan_log
from functools import wraps


def subtitle_generator(asr_method):
    """Decorator to select subtitle generation function based on model type
    Args:
        model_type: str, type of model to use
    Returns:
        function: wrapped subtitle generation function
    """
    def decorator(func):
        def wrapper(video_path):
            if asr_method == "api":
                from .api.whisper_sdk import generate_srt
                return generate_srt(video_path)
            elif asr_method == "deploy":
                try:
                    subprocess.run(
                        ['python', os.path.join(SRC_DIR, 'subtitle', 'generate.py'), video_path],
                        stdout=subprocess.DEVNULL
                    )
                    return video_path[:-4] + ".srt"
                except subprocess.CalledProcessError as e:
                    scan_log.error(f"Generate subtitles failed: {e.stderr}")
                    return None
            elif asr_method == "none":
                return None
            else:
                scan_log.error(f"Unsupported asr method: {asr_method}")
                return None
        return wrapper
    return decorator

# Generate the srt file via whisper model
@subtitle_generator(ASR_METHOD)
def generate_subtitle(in_video_path):
    """Generate subtitles via whisper model
    Args:
        in_video_path: str, the path of video
    """
    pass


