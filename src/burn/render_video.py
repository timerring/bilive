# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.config import GPU_EXIST, SRC_DIR, MODEL_TYPE, AUTO_SLICE, SLICE_DURATION, MIN_VIDEO_SIZE
from src.danmaku.generate_danmakus import get_resolution, process_danmakus
from src.subtitle.generate_subtitles import generate_subtitles
from src.burn.render_command import render_command
from src.autoslice.slice_video import slice_video, inject_metadata, zhipu_glm_4v_plus_generate_title
from src.autoslice.calculate_density import extract_dialogues, calculate_density, format_time
from src.upload.extract_video_info import get_video_info
from src.log.logger import scan_log

def normalize_video_path(filepath):
    """Normalize the video path to upload
    Args:
        filepath: str, the path of video
    """
    parts = filepath.rsplit('/', 1)[-1].split('_')
    date_time_parts = parts[1].split('-')
    new_date_time = f"{date_time_parts[0][:4]}-{date_time_parts[0][4:6]}-{date_time_parts[0][6:8]}-{date_time_parts[1]}-{date_time_parts[2]}"
    return filepath.rsplit('/', 1)[0] + '/' + parts[0] + '_' + new_date_time + '-.mp4'

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
    xml_path = original_video_path[:-4] + '.xml'
    ass_path = original_video_path[:-4] + '.ass'
    srt_path = original_video_path[:-4] + '.srt'
    jsonl_path = original_video_path[:-4] + '.jsonl'

    # Recoginze the resolution of video
    resolution_x, resolution_y = get_resolution(original_video_path)
    try:
        # Process the danmakus to ass and remove emojis
        subtitle_font_size, subtitle_margin_v = process_danmakus(xml_path, resolution_x, resolution_y)
    except TypeError as e:
        scan_log.error(f"TypeError: {e} - Check the return value of process_danmakus")
    except FileNotFoundError as e:
        scan_log.error(f"FileNotFoundError: {e} - Check if the file exists")

    # Generate the srt file via whisper model
    if GPU_EXIST:
        if MODEL_TYPE != "pipeline":
            generate_subtitles(original_video_path)

    # Burn danmaku or subtitles into the videos 
    render_command(original_video_path, format_video_path, subtitle_font_size, subtitle_margin_v)
    scan_log.info("Complete danamku burning and wait for uploading!")

    if AUTO_SLICE:
        if check_file_size(format_video_path) > MIN_VIDEO_SIZE:
            title, artist, date = get_video_info(format_video_path)
            slice_video_path = format_video_path[:-4] + '_slice.mp4'
            dialogues = extract_dialogues(ass_path)
            max_start_time, max_density = calculate_density(dialogues)
            formatted_time = format_time(max_start_time)
            scan_log.info(f"The 30-second window with the highest density starts at {formatted_time} seconds with {max_density} danmakus.")
            slice_video(format_video_path, max_start_time, slice_video_path)
            glm_title = zhipu_glm_4v_plus_generate_title(slice_video_path, artist)
            slice_video_flv_path = slice_video_path[:-4] + '.flv'
            inject_metadata(slice_video_path, glm_title, slice_video_flv_path)
            os.remove(slice_video_path)

    # Delete relative files
    for remove_path in [original_video_path, xml_path, ass_path, srt_path, jsonl_path]:
        if os.path.exists(remove_path):
            os.remove(remove_path)
    
    # # For test
    # test_path = original_video_path[:-4]
    # os.rename(original_video_path, test_path)

    with open(f"{SRC_DIR}/upload/uploadVideoQueue.txt", "a") as file:
        file.write(f"{format_video_path}\n")
        if AUTO_SLICE:
            scan_log.info("Complete slice video and wait for uploading!")
            slice_video_path = format_video_path[:-4] + '_slice.mp4'
            slice_video_flv_path = slice_video_path[:-4] + '.flv'
            file.write(f"{slice_video_flv_path}\n")