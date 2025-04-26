# Copyright (c) 2024 bilive.

import argparse
import os
import subprocess
from src.config import SRC_DIR, VIDEOS_DIR
from src.danmaku.generate_danmakus import get_resolution, process_danmakus
from src.subtitle.subtitle_generator import generate_subtitle
from src.burn.render_command import render_command
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


def merge_command(in_final_video, title, artist, date, merge_list):
    """Merge the video segments and preserve the first video's metadata
    Args:
        in_final_video: str, the path of videos will be merged
    """
    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        merge_list,
        "-metadata",
        f"title={title}",
        "-metadata",
        f"artist={artist}",
        "-metadata",
        f"date={date}",
        "-use_wallclock_as_timestamps",
        "1",
        "-c",
        "copy",
        in_final_video,
    ]
    try:
        scan_log.info("Begin merging videos...")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")
    subprocess.run(
        ["rm", merge_list], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def render_then_merge(video_path_list):
    title = ""
    artist = ""
    date = ""
    output_video_path = ""
    merge_list = SRC_DIR + "/burn/mergevideo.txt"

    for line in video_path_list:
        stripped_line = str(line).strip()
        if stripped_line:
            directory = os.path.dirname(stripped_line)
            video_name = os.path.basename(stripped_line)
            tmp = directory + "/tmp/"
            if output_video_path == "":
                title, artist, date = get_video_info(stripped_line)
                output_video_path = normalize_video_path(stripped_line)
                scan_log.info("The output video is " + output_video_path)
                subprocess.run(
                    ["mkdir", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

            video_to_be_merged = tmp + video_name
            original_video_path = stripped_line
            xml_path = original_video_path[:-4] + ".xml"
            ass_path = original_video_path[:-4] + ".ass"
            srt_path = original_video_path[:-4] + ".srt"
            jsonl_path = original_video_path[:-4] + ".jsonl"
            # Recoginze the resolution of video
            resolution_x, resolution_y = get_resolution(original_video_path)
            # Process the danmakus to ass and remove emojis
            subtitle_font_size, subtitle_margin_v = process_danmakus(
                xml_path, resolution_x, resolution_y
            )
            # Generate the srt file via whisper model
            generate_subtitle(original_video_path)
            # Burn danmaku or subtitles into the videos
            render_command(
                original_video_path,
                video_to_be_merged,
                subtitle_font_size,
                subtitle_margin_v,
            )
            if not os.path.exists(merge_list):
                open(merge_list, "w").close()
            with open(merge_list, "a") as f:
                f.write(f"file '{video_to_be_merged}'\n")
            scan_log.info("Complete danamku burning and wait for uploading!")

        for remove_path in [
            original_video_path,
            xml_path,
            ass_path,
            srt_path,
            jsonl_path,
        ]:
            if os.path.exists(remove_path):
                os.remove(remove_path)

        # # For test part
        # test_path = original_video_path[:-4]
        # os.rename(original_video_path, test_path)

    merge_command(output_video_path, title, artist, date, merge_list)
    subprocess.run(["rm", "-r", tmp])

    if not insert_upload_queue(output_video_path):
        scan_log.error("Cannot insert the video to the upload queue")
