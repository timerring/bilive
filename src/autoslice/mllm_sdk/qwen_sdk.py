from src.config import QWEN_API_KEY, SLICE_PROMPT
from src.log.logger import scan_log
from openai import OpenAI
import os
import base64


def encode_video(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")


def qwen_generate_title(video_path, artist):
    client = OpenAI(
        api_key=QWEN_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    base64_video = encode_video(video_path)
    completion = client.chat.completions.create(
        model="qwen2.5-vl-72b-instruct",
        messages=[
            {
                "role": "system",
                "content": [{"type": "text", "text": "你是一个视频切片员"}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "video_url",
                        "video_url": {"url": f"data:video/mp4;base64,{base64_video}"},
                    },
                    {"type": "text", "text": SLICE_PROMPT.format(artist=artist)},
                ],
            },
        ],
    )
    scan_log.info("Using Qwen-2.5-72B-Instruct to generate slice title")
    scan_log.info(f"Prompt: {SLICE_PROMPT.format(artist=artist)}")
    scan_log.info(f"Generated slice title: {completion.choices[0].message.content}")
    return completion.choices[0].message.content.strip('"')
