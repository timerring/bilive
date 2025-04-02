from src.config import QWEN_API_KEY
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
                "content": [{"type":"text","text": "你是一个视频切片员"}]},
            {
                "role": "user",
                "content": [
                    {
                        "type": "video_url",
                        "video_url": {"url": f"data:video/mp4;base64,{base64_video}"},
                    },
                    {"type": "text", "text": f"视频是{artist}的直播切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，标题中不要表情符号，可以适当使用网络热词或流行语"},
                ],
            }
        ],
    )
    scan_log.info("使用 Qwen-2.5-72B-Instruct 生成切片标题")
    scan_log.info(f"Prompt: 视频是{artist}的直播切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，标题中不要表情符号，可以适当使用网络热词或流行语")
    scan_log.info(f"生成的切片标题为: {completion.choices[0].message.content.strip('"')}")
    return completion.choices[0].message.content.strip('"')
