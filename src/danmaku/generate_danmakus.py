# Copyright (c) 2024 bilive.

import os
import subprocess
from src.log.logger import scan_log
from .adjust_price import update_danmaku_prices
from .DanmakuConvert.dmconvert import convert_xml_to_ass


def get_resolution(in_video_path):
    """Return the resolution of video
    Args:
        in_video_path: str, the path of video
    Return:
        resolution: str.
    """
    try:
        # Use ffprobe to acquire the video resolution
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=s=x:p=0', in_video_path],
            check=True,
            text=True,
            capture_output=True
        )
        scan_log.debug(f"get_resolution FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"get_resolution FFmpeg debug: {result.stderr}")
        resolution = result.stdout.strip()
        resolution_x, resolution_y = map(int, resolution.split('x'))
        scan_log.info(f"The video resolution x is {resolution_x} and y is {resolution_y}")
        return resolution_x, resolution_y
    except subprocess.CalledProcessError as e:
        scan_log.error(f"get_resolution Error: {e.stderr}")
        return 1920, 1080

def process_danmakus(in_xml_path, resolution_x, resolution_y):
    """Generate and process the danmakus according to different resolution.
    Args:
        in_xml_path: str, the xml path to generate ass file
        resolution_x: int, the x resolution of the video
        resolution_y: int, the y resolution of the video
    Return:
        subtitle_font_size: str, the font size of subtitles
        subtitle_margin_v: str, the margin v of subtitles
    """
    if os.path.isfile(in_xml_path):
        # Adjust the price of sc and guard
        update_danmaku_prices(in_xml_path)
        out_ass_path = in_xml_path[:-4] + '.ass'
        if resolution_x == 1280 and resolution_y == 720:
            boxfont = 30
            danmakufont = 38
            subtitle_font_size = '15'
            subtitle_margin_v = '20'
        elif resolution_x == 720 and resolution_y == 1280:
            boxfont = 30
            danmakufont = 38
            subtitle_font_size = '8'
            subtitle_margin_v = '60'
        elif resolution_x == 1920 and resolution_y == 1080:
            boxfont = 42
            danmakufont = 42
            subtitle_font_size = '16'
            subtitle_margin_v = '60'
        elif resolution_x == 1080 and resolution_y == 1920:
            boxfont = 42
            danmakufont = 42
            subtitle_font_size = '8'
            subtitle_margin_v = '60'
        else:
            boxfont = 38
            danmakufont = 38
            subtitle_font_size = '16'
            subtitle_margin_v = '60'
        # Convert danmakus to ass file
        convert_xml_to_ass(danmakufont, boxfont, resolution_x, resolution_y, in_xml_path, out_ass_path)
        return subtitle_font_size, subtitle_margin_v