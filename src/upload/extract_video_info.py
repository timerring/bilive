# Copyright (c) 2024 bilive.

import subprocess
import re
import json
import os
from datetime import datetime
from src.upload.query_search_suggestion import get_bilibili_suggestions
from src.config import TITLE, DESC
from src.log.logger import upload_log


def get_video_info(video_file_path):
    """get the title, artist and date of the video file via ffprobe
    Args:
        video_file_path: str, the path of the video file
    Returns:
        str: the title of the video file, if failed, return None
    """
    try:
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            video_file_path,
        ]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode(
            "utf-8"
        )
        parsed_output = json.loads(output)
        title_value = parsed_output["format"]["tags"]["title"]
        artist_value = parsed_output["format"]["tags"]["artist"]
        date_value = parsed_output["format"]["tags"]["date"]
        if len(date_value) > 8:
            dt = datetime.fromisoformat(date_value)
            new_date = dt.strftime("%Y%m%d")
        else:
            new_date = date_value
        return title_value, artist_value, new_date
    except Exception as e:
        # Log the exception if needed
        upload_log.error(f"Error occurred in get_video_info: {e}")
        return None, None, None


def generate_title(video_path):
    title, artist, date = get_video_info(video_path)
    if title is None:
        upload_log.error(f"Error occurred in generate_title: {title}")
        return None
    source_link = generate_source(video_path)
    formatted_title = TITLE.format(
        artist=artist, date=date, title=title, source_link=source_link
    )
    new_title = f"{formatted_title}"
    return new_title


def generate_desc(video_path):
    title, artist, date = get_video_info(video_path)
    source_link = generate_source(video_path)
    formatted_desc = DESC.format(
        artist=artist, date=date, title=title, source_link=source_link
    )
    new_desc = f"{formatted_desc}"
    return new_desc


def generate_tag(video_path):
    title, artist, date = get_video_info(video_path)
    artist_text = re.sub(r"\W+", "", artist)

    tags = get_bilibili_suggestions(artist_text)

    if not tags:
        tags = "直播回放"

    return tags


def generate_source(video_path):
    file_name = os.path.basename(video_path)
    match_result = re.search(r"^([^_]*)", file_name)
    if match_result:
        part_before_underscore = match_result.group(1)
        source_link = "https://live.bilibili.com/" + part_before_underscore
        return source_link
    else:
        return "https://live.bilibili.com/"


if __name__ == "__main__":
    video_path = ""
    video_title = generate_title(video_path)
    print(video_title)
    video_desc = generate_desc(video_path)
    print(video_desc)
    video_tag = generate_tag(video_path)
    print(video_tag)
    video_source = generate_source(video_path)
    print(video_source)
