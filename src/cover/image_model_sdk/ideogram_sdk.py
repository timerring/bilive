import requests
import json
import os
import time
from src.config import IDEOGRAM_API_KEY


def ideogram_generate_cover(your_file_path):
    """Generater cover image using ideogram V_2 model
    Args:
        your_file_path: str, path to the image file
    Returns:
        str, local download path of the generated cover image file
    """
    try:
        url = "https://api.ideogram.ai/remix"

        files = {"image_file": open(your_file_path, "rb")}
        payload = {
            "image_request": json.dumps(
                {
                    "prompt": "This is a video screenshot, please generate a cover in the style of a manga",
                    "aspect_ratio": "ASPECT_10_16",
                    "image_weight": 75,
                    "magic_prompt_option": "ON",
                    "model": "V_2",
                }
            )
        }
        headers = {"Api-Key": f"{IDEOGRAM_API_KEY}"}

        response = requests.post(url, data=payload, files=files, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            image_url = response_json["data"][0]["url"]
            img_data = requests.get(image_url).content
            cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
            temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
            with open(temp_cover_path, "wb") as handler:
                handler.write(img_data)
            os.remove(your_file_path)
            return temp_cover_path
        else:
            raise Exception(response.text)
    except Exception as e:
        print(e, flush=True)
        return None


if __name__ == "__main__":
    print(ideogram_generate_cover(""))
