# Copyright (c) 2024 bilive.

import os
import time
import codecs
from datetime import datetime
from src.upload.extract_video_info import generate_title, generate_desc, generate_tag, generate_source
import subprocess
import json

def generate_video_data(video_path):
    copyright = 1
    title = generate_title(video_path)
    desc = generate_desc(video_path)
    tid = 138
    tag = generate_tag(video_path)
    source = generate_source(video_path)
    cover = ""
    dynamic = ""
    return copyright, title, desc, tid, tag, source, cover, dynamic

def generate_slice_data(video_path):
    try:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            video_path
        ]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
        parsed_output = json.loads(output)
        title = parsed_output["format"]["tags"]["generate"]
        copyright = 1
        tid = 138
        tag = "直播切片"
        return copyright, title, tid, tag
    except Exception as e:
        scan_log.error(f"Error in generate_slice_data: {e}")
        return None, None, None, None

if __name__ == "__main__":    
    pass
