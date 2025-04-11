# Copyright (c) 2024 bilive.

import os
import subprocess
from src.config import GPU_EXIST
from src.log.logger import scan_log


def render_command(
    in_video_path, out_video_path, in_subtitle_font_size, in_subtitle_margin_v
):
    """Burn the danmakus and subtitles into the videos
    Args:
        in_video_path: str, the path of video
        out_video_path: str, the path of rendered video
        in_subtitle_font_size: str, the font size of subtitles
        in_subtitle_margin_v: str, the bottom margin of subtitles
    """
    in_ass_path = in_video_path[:-4] + ".ass"
    if not os.path.isfile(in_ass_path):
        scan_log.warning("Cannot find danmaku file, return directly")
        subprocess.run(
            ["mv", in_video_path, out_video_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    in_srt_path = in_video_path[:-4] + ".srt"
    if os.path.isfile(in_srt_path):
        if GPU_EXIST:
            scan_log.info("Current Mode: GPU with subtitles")
            gpu_srt_ass_command = [
                "ffmpeg",
                "-y",
                "-hwaccel",
                "cuda",
                "-c:v",
                "h264_cuvid",
                "-i",
                in_video_path,
                "-c:v",
                "h264_nvenc",
                "-vf",
                f"subtitles={in_srt_path}:force_style='Fontsize={in_subtitle_font_size},MarginV={in_subtitle_margin_v}',subtitles={in_ass_path}",
                out_video_path,
            ]
            try:
                result = subprocess.run(
                    gpu_srt_ass_command, check=True, capture_output=True, text=True
                )
                scan_log.debug(f"FFmpeg output: {result.stdout}")
                if result.stderr:
                    scan_log.debug(f"FFmpeg debug: {result.stderr}")
            except subprocess.CalledProcessError as e:
                scan_log.error(f"Error: {e.stderr}")
        else:
            scan_log.info("Current Mode: CPU with subtitles")
            cpu_srt_ass_command = [
                "ffmpeg",
                "-y",
                "-i",
                in_video_path,
                "-vf",
                f"subtitles={in_srt_path}:force_style='Fontsize={in_subtitle_font_size},MarginV={in_subtitle_margin_v}',subtitles={in_ass_path}",
                "-preset",
                "ultrafast",
                out_video_path,
            ]
            try:
                result = subprocess.run(
                    cpu_srt_ass_command, check=True, capture_output=True, text=True
                )
                scan_log.debug(f"FFmpeg output: {result.stdout}")
                if result.stderr:
                    scan_log.debug(f"FFmpeg debug: {result.stderr}")
            except subprocess.CalledProcessError as e:
                scan_log.error(f"Error: {e.stderr}")
    else:
        if GPU_EXIST:
            scan_log.info("Current Mode: GPU without subtitles")
            gpu_ass_command = [
                "ffmpeg",
                "-y",
                "-hwaccel",
                "cuda",
                "-c:v",
                "h264_cuvid",
                "-i",
                in_video_path,
                "-c:v",
                "h264_nvenc",
                "-vf",
                f"ass={in_ass_path}",
                out_video_path,
            ]
            try:
                result = subprocess.run(
                    gpu_ass_command, check=True, capture_output=True, text=True
                )
                scan_log.debug(f"FFmpeg output: {result.stdout}")
                if result.stderr:
                    scan_log.debug(f"FFmpeg debug: {result.stderr}")
            except subprocess.CalledProcessError as e:
                scan_log.error(f"Error: {e.stderr}")
        else:
            scan_log.info("Current Mode: CPU without subtitles")
            cpu_ass_command = [
                "ffmpeg",
                "-y",
                "-i",
                in_video_path,
                "-vf",
                f"ass={in_ass_path}",
                "-preset",
                "ultrafast",
                out_video_path,
            ]
            try:
                result = subprocess.run(
                    cpu_ass_command, check=True, capture_output=True, text=True
                )
                scan_log.debug(f"FFmpeg output: {result.stdout}")
                if result.stderr:
                    scan_log.debug(f"FFmpeg debug: {result.stderr}")
            except subprocess.CalledProcessError as e:
                scan_log.error(f"Error: {e.stderr}")
