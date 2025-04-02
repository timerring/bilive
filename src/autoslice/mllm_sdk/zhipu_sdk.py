# Copyright (c) 2024 bilive.

import base64
from src.config import ZHIPU_API_KEY
from zhipuai import ZhipuAI
from src.log.logger import scan_log

def zhipu_glm_4v_plus_generate_title(video_path, artist):
    with open(video_path, 'rb') as video_file:
        video_base = base64.b64encode(video_file.read()).decode('utf-8')

    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    response = client.chat.completions.create(
        model="glm-4v-plus-0111",
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
                "text": f"视频是{artist}的直播的切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，注意标题中如果有“主播”请替换成{artist}"
            }
            ]
        }
        ]
    )
    scan_log.info("使用 Zhipu-glm-4v-plus 生成切片标题")
    scan_log.info(f"Prompt: 视频是{artist}的直播的切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，注意标题中如果有“主播”请替换成{artist}")
    scan_log.info(f"生成的切片标题为: {response.choices[0].message.content}")
    return response.choices[0].message.content.replace("《", "").replace("》", "")