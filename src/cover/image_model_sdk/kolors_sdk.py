import requests
import base64
import time
import os
from src.config import SILICONFLOW_API_KEY


def kolors_generate_cover(your_file_path):
    """Generater cover image using SiliconFlow api of Kolors(Kwai)
    Args:
        your_file_path: str, path to the image file
    Returns:
        str, local download path of the generated cover image file
    """
    with open(your_file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode("utf-8")

    payload = {
        "model": "Kwai-Kolors/Kolors",
        "prompt": "这是一个视频截图，请尝试生成对应的日本动漫类型的封面",
        "image_size": "1024x1024",
        "batch_size": 1,
        "num_inference_steps": 20,
        "guidance_scale": 7.5,
        "image": f"data:image/webp;base64,{data}",
    }
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json",
    }
    url = "https://api.siliconflow.cn/v1/images/generations"
    response = requests.request("POST", url, json=payload, headers=headers)
    if response.status_code == 200:
        image_url = response.json()["images"][0]["url"]
        img_data = requests.get(image_url).content
        cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
        temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
        with open(temp_cover_path, "wb") as handler:
            handler.write(img_data)
        os.remove(your_file_path)
        return temp_cover_path
    else:
        print(response.text, flush=True)
        return None


if __name__ == "__main__":
    your_file_path = ""
    print(kolors_generate_cover(your_file_path))
