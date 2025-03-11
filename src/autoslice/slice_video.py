# Copyright (c) 2024 bilive.

import base64
import subprocess
from src.config import Your_API_KEY, SLICE_DURATION
from zhipuai import ZhipuAI
from src.autoslice.calculate_density import extract_dialogues, calculate_density, format_time
from src.log.logger import scan_log

def zhipu_glm_4v_plus_generate_title(video_path, artist):
    with open(video_path, 'rb') as video_file:
        video_base = base64.b64encode(video_file.read()).decode('utf-8')

    client = ZhipuAI(api_key=Your_API_KEY)
    response = client.chat.completions.create(
        model="glm-4v-plus",
        messages=[
        {
            "role": "user",
            "content": [
            {
                "type": "video_url",
                "video_url": {
                    "url" : video_base
                }
            },
            {
                "type": "text",
                "text": f"视频是{artist}的直播的切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，注意标题中如果有“主播”请替换成{artist}。"
            }
            ]
        }
        ]
    )
    return response.choices[0].message.content.replace("《", "").replace("》", "")

# https://stackoverflow.com/questions/64849478/cant-insert-stream-metadata-into-mp4
def inject_metadata(video_path, generate_title, output_path):
    """Slice the video using ffmpeg."""
    command = [
        'ffmpeg',
        '-i', video_path,
        '-metadata:g', f'generate={generate_title}',
        '-c:v', 'copy',
        '-c:a', 'copy',
        output_path
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")

def slice_video(video_path, start_time, output_path, duration=f'00:00:{SLICE_DURATION}'):
    """Slice the video using ffmpeg."""
    command = [
        'ffmpeg',
        '-ss', format_time(start_time),
        '-i', video_path,
        '-t', duration,
        '-map_metadata', '-1',
        '-c:v', 'copy',
        '-c:a', 'copy',
        output_path
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        scan_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            scan_log.debug(f"FFmpeg debug: {result.stderr}")
    except subprocess.CalledProcessError as e:
        scan_log.error(f"Error: {e.stderr}")