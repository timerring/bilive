# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.config import (
    SRC_DIR,
    MODEL_TYPE,
    AUTO_SLICE,
    SLICE_DURATION,
    MIN_VIDEO_SIZE,
    VIDEOS_DIR,
    SLICE_NUM,
    SLICE_OVERLAP,
    SLICE_STEP,
)
from src.danmaku.generate_danmakus import get_resolution, process_danmakus
from src.subtitle.subtitle_generator import generate_subtitle
from src.burn.render_command import render_command
from autoslice import slice_video_by_danmaku
from src.autoslice.inject_metadata import inject_metadata
from src.autoslice.title_generator import generate_title
from src.upload.extract_video_info import get_video_info
from src.log.logger import scan_log
from db.conn import insert_upload_queue


def normalize_video_path(filepath):
    """Normalize the video path to upload
    Args:
        filepath: str, the path of video
    """
    parts = filepath.rsplit("/", 1)[-1].split("_")
    date_time_parts = parts[1].split("-")
    new_date_time = f"{date_time_parts[0][:4]}-{date_time_parts[0][4:6]}-{date_time_parts[0][6:8]}-{date_time_parts[1]}-{date_time_parts[2]}"
    return filepath.rsplit("/", 1)[0] + "/" + parts[0] + "_" + new_date_time + "-.mp4"


def check_file_size(file_path):
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    return file_size_mb


def render_video(video_path):
    if not os.path.exists(video_path):
        scan_log.error(f"File {video_path} does not exist.")
        return

    original_video_path = str(video_path)
    format_video_path = normalize_video_path(original_video_path)
    xml_path = original_video_path[:-4] + ".xml"
    ass_path = original_video_path[:-4] + ".ass"
    srt_path = original_video_path[:-4] + ".srt"
    jsonl_path = original_video_path[:-4] + ".jsonl"

    # Recoginze the resolution of video
    resolution_x, resolution_y = get_resolution(original_video_path)
    try:
        # Process the danmakus to ass and remove emojis
        subtitle_font_size, subtitle_margin_v = process_danmakus(
            xml_path, resolution_x, resolution_y
        )
    except TypeError as e:
        scan_log.error(f"TypeError: {e} - Check the return value of process_danmakus")
    except FileNotFoundError as e:
        scan_log.error(f"FileNotFoundError: {e} - Check if the file exists")

    # Generate the srt file via whisper model
    if MODEL_TYPE != "pipeline":
        generate_subtitle(original_video_path)

    # Burn danmaku or subtitles into the videos
    render_command(
        original_video_path, format_video_path, subtitle_font_size, subtitle_margin_v
    )
    scan_log.info("Complete danamku burning and wait for uploading!")

    if AUTO_SLICE:
        if check_file_size(format_video_path) > MIN_VIDEO_SIZE:
            title, artist, date = get_video_info(format_video_path)
            slices_path = slice_video_by_danmaku(
                ass_path,
                format_video_path,
                SLICE_DURATION,
                SLICE_NUM,
                SLICE_OVERLAP,
                SLICE_STEP,
            )
            for slice_path in slices_path:
                try:
                    slice_title = generate_title(slice_path, artist)
                    slice_video_flv_path = slice_path[:-4] + ".flv"
                    inject_metadata(slice_path, slice_title, slice_video_flv_path)
                    os.remove(slice_path)
                    if not insert_upload_queue(slice_video_flv_path):
                        scan_log.error("Cannot insert the video to the upload queue")
                except Exception as e:
                    scan_log.error(f"Error in {slice_path}: {e}")

    # Delete relative files
    for remove_path in [original_video_path, xml_path, ass_path, srt_path, jsonl_path]:
        if os.path.exists(remove_path):
            os.remove(remove_path)

    # # For test
    # test_path = original_video_path[:-4]
    # os.rename(original_video_path, test_path)

    if not insert_upload_queue(format_video_path):
        scan_log.error("Cannot insert the video to the upload queue")
