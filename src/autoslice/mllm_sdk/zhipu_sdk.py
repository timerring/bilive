# Copyright (c) 2024 bilive.

import base64
from src.config import ZHIPU_API_KEY, SLICE_PROMPT
from zhipuai import ZhipuAI
from src.log.logger import scan_log


def zhipu_glm_4v_plus_generate_title(video_path, artist):
    with open(video_path, "rb") as video_file:
        video_base = base64.b64encode(video_file.read()).decode("utf-8")

    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    response = client.chat.completions.create(
        model="glm-4v-plus-0111",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "video_url", "video_url": {"url": video_base}},
                    {"type": "text", "text": SLICE_PROMPT.format(artist=artist)},
                ],
            }
        ],
    )
    scan_log.info("Using Zhipu-glm-4v-plus to generate slice title")
    scan_log.info(f"Prompt: {SLICE_PROMPT.format(artist=artist)}")
    scan_log.info(f"Generated slice title: {response.choices[0].message.content}")
    return response.choices[0].message.content.replace("《", "").replace("》", "")
