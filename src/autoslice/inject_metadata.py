# Copyright (c) 2024 bilive.

import subprocess
from src.log.logger import scan_log


# https://stackoverflow.com/questions/64849478/cant-insert-stream-metadata-into-mp4
def inject_metadata(video_path, generate_title, output_path):
    """Slice the video using ffmpeg."""
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-metadata:g",
        f"generate={generate_title}",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_path,
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")
