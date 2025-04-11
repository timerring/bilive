from google import genai
from google.genai import types
from src.log.logger import scan_log
from src.config import GEMINI_API_KEY, SLICE_PROMPT


def gemini_generate_title(video_path, artist):

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Only for videos of size <20Mb
    video_bytes = open(video_path, "rb").read()

    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=types.Content(
            parts=[
                types.Part(text=SLICE_PROMPT),
                types.Part(
                    inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")
                ),
            ]
        ),
    )
    scan_log.info("使用 Gemini-2.0-flash 生成切片标题")
    scan_log.info(f"Prompt: {SLICE_PROMPT}")
    scan_log.info(f"生成的切片标题为: {response.text}")
    return response.text
