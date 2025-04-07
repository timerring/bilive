from openai import OpenAI
from src.config import RECRAFT_API_KEY
import requests
import os
import time


def recraft_generate_cover(your_file_path):
    try:
        client = OpenAI(
            base_url='https://external.api.recraft.ai/v1',
            api_key=RECRAFT_API_KEY,
        )

        response = client.post(
            path='/images/imageToImage',
            cast_to=object,
            options={'headers': {'Content-Type': 'multipart/form-data'}},
            files={
                'image': open(your_file_path, 'rb'),
            },
            body={
                'prompt': 'This is a video screenshot, please generate a cover in the style of a manga',
                'strength': 0.75,
            },
        )
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content
        cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
        temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
        with open(temp_cover_path, "wb") as handler:
            handler.write(img_data)
        os.remove(your_file_path)
        return temp_cover_path
    except Exception as e:
        print(e, flush=True)
        return None