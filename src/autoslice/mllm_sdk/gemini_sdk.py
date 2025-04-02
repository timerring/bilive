from google import genai
from google.genai import types 
from src.log.logger import scan_log
from src.config import GEMINI_API_KEY

def gemini_generate_title(video_path, artist):

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Only for videos of size <20Mb
    video_bytes = open(video_path, 'rb').read()

    response = client.models.generate_content(
        model='models/gemini-2.0-flash',
        contents=types.Content(
            parts=[
                types.Part(text=f'视频是{artist}的直播的切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，只需要返回一个标题即可，无需返回其他内容'),
                types.Part(
                    inline_data=types.Blob(data=video_bytes, mime_type='video/mp4')
                )
            ]
        )
    )
    scan_log.info("使用 Gemini-2.0-flash 生成切片标题")
    scan_log.info(f"Prompt: 视频是{artist}的直播的切片，请根据该视频中的内容及弹幕信息，为这段视频起一个调皮并且吸引眼球的标题，只需要返回一个标题即可，无需返回其他内容")
    scan_log.info(f"生成的切片标题为: {response.text}")
    return response.text