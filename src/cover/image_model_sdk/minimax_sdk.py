import requests
import json
import base64
import os
import time
from src.config import MINIMAX_API_KEY


def minimax_generate_cover(your_file_path):
    """Generater cover image using minimax api
    Args:
        your_file_path: str, path to the image file
    Returns:
        str, local download path of the generated cover image file
    """
    cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
    temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)

    with open(your_file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')

    payload = json.dumps({
        "model": "image-01",
        "prompt": "这是一个视频截图，请生成其对应的吉普力风格的图片",
        "subject_reference": [
            {
                "type": "character",
                "image_file": f"data:image/jpeg;base64,{data}"
            }
        ],
        "n": 2
    })
    headers = {
        'Authorization': f'Bearer {MINIMAX_API_KEY}',
        'Content-Type': 'application/json'
    }

    url = "https://api.minimax.chat/v1/image_generation"
    response = requests.request("POST", url, headers=headers, data=payload).json()
    if response['base_resp']['status_code'] == 0:
        image_url = response['data']['image_urls'][0]
        img_data = requests.get(image_url).content
        with open(temp_cover_path, 'wb') as handler:
            handler.write(img_data)
        os.remove(your_file_path)
        return temp_cover_path
    else:
        print(response['base_resp']['error_msg'])
        return None

if __name__ == "__main__":
    your_file_path = ""
    print(minimax_generate_cover(your_file_path))