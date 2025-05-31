from google import genai
from google.genai import types
from src.log.logger import scan_log
from src.config import GEMINI_API_KEY, SLICE_PROMPT


def gemini_generate_title(video_path, artist):

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Only for videos of size <20Mb
    video_bytes = open(video_path, "rb").read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=types.Content(
            parts=[
                types.Part(text=SLICE_PROMPT.format(artist=artist)),
                types.Part(
                    inline_data=types.Blob(data=video_bytes, mime_type="video/mp4")
                ),
            ]
        ),
    )
    scan_log.info("Using Gemini-2.5-Flash to generate slice title")
    scan_log.info(f"Prompt: {SLICE_PROMPT.format(artist=artist)}")
    scan_log.info(f"Generated slice title: {response.text}")
    return response.text
