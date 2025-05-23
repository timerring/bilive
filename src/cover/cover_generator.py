from functools import wraps
from src.log.logger import upload_log
from src.config import IMAGE_GEN_MODEL
import subprocess


def cut_cover_use_ffmpeg(video_path):
    """Cut cover use ffmpeg
    Args:
        video_path: str, path to the video file
    Returns:
        str: the video cut cover path
    """
    upload_log.info("begin to generate cover")
    cover_path = video_path[:-4] + ".jpg"
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-t",
        "1",
        "-r",
        "1",
        cover_path,
    ]
    try:
        result = subprocess.run(
            ffmpeg_command, check=True, capture_output=True, text=True
        )
        upload_log.debug(f"FFmpeg output: {result.stdout}")
        if result.stderr:
            upload_log.debug(f"FFmpeg debug: {result.stderr}")
        return cover_path
    except subprocess.CalledProcessError as e:
        upload_log.error(f"Error: {e.stderr}")
        return None


def cover_generator(model_type):
    """Decorator to select cover generation function based on model type
    Args:
        model_type: str, type of model to use
    Returns:
        function: wrapped title generation function
    """

    def decorator(func):
        def wrapper(video_path):
            cover_path = cut_cover_use_ffmpeg(video_path)
            if cover_path is None:
                upload_log.error("Failed to generate cover using ffmpeg")
                return None
            if model_type == "minimax":
                from .image_model_sdk.minimax_sdk import minimax_generate_cover

                return minimax_generate_cover(cover_path)
            elif model_type == "siliconflow":
                from .image_model_sdk.kolors_sdk import kolors_generate_cover

                return kolors_generate_cover(cover_path)
            elif model_type == "tencent":
                from .image_model_sdk.tencent_sdk import hunyuan_generate_cover

                return hunyuan_generate_cover(cover_path)
            elif model_type == "baidu":
                from .image_model_sdk.baidu_sdk import baidu_generate_cover

                return baidu_generate_cover(cover_path)
            elif model_type == "stability":
                from .image_model_sdk.stability_sdk import (
                    stable_diffusion_generate_cover,
                )

                return stable_diffusion_generate_cover(cover_path)
            elif model_type == "luma":
                from .image_model_sdk.luma_sdk import luma_generate_cover

                return luma_generate_cover(cover_path)
            elif model_type == "ideogram":
                from .image_model_sdk.ideogram_sdk import ideogram_generate_cover

                return ideogram_generate_cover(cover_path)
            elif model_type == "recraft":
                from .image_model_sdk.recraft_sdk import recraft_generate_cover

                return recraft_generate_cover(cover_path)
            elif model_type == "amazon":
                from .image_model_sdk.amazon_sdk import amazon_generate_cover

                return amazon_generate_cover(cover_path)
            elif model_type == "hidream":
                from .image_model_sdk.hidream_sdk import hidream_generate_cover

                return hidream_generate_cover(cover_path)
            else:
                upload_log.error(f"Unsupported model type: {model_type}")
                return None

        return wrapper

    return decorator


@cover_generator(IMAGE_GEN_MODEL)
def generate_cover(video_path):
    """Generate cover for video
    Args:
        video_path: str, path to the video file
    Returns:
        str: generated cover
    """
    pass  # The actual implementation is handled by the decorator
