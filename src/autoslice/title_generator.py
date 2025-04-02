from functools import wraps
from src.log.logger import scan_log
from src.config import MLLM_MODEL

def title_generator(model_type):
    """Decorator to select title generation function based on model type
    Args:
        model_type: str, type of model to use
    Returns:
        function: wrapped title generation function
    """
    def decorator(func):
        def wrapper(video_path, artist):
            if model_type == "zhipu":
                from .mllm_sdk.zhipu_sdk import zhipu_glm_4v_plus_generate_title
                return zhipu_glm_4v_plus_generate_title(video_path, artist)
            elif model_type == "gemini":
                from .mllm_sdk.gemini_sdk import gemini_generate_title
                return gemini_generate_title(video_path, artist)
            else:
                scan_log.error(f"Unsupported model type: {model_type}")
                return None
        return wrapper
    return decorator

@title_generator(MLLM_MODEL)
def generate_title(video_path, artist):
    """Generate title for video
    Args:
        video_path: str, path to the video file
        artist: str, artist name
    Returns:
        str: generated title
    """
    pass  # The actual implementation is handled by the decorator