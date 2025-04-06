import requests
from src.config import STABILITY_API_KEY
import time
import os


def stable_diffusion_generate_cover(your_file_path):
    """Generater cover image using stability api
    Args:
        image_path: str, path to the image file
    Returns:
        str, local download path of the generated cover image file
    """

    cover_name = time.strftime("%Y%m%d%H%M%S") + ".jpeg"
    temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)

    with open(your_file_path, "rb") as img_file:
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*",
            },
            files={"image": ("image.jpg", img_file, "image/jpeg")},
            data={
                "prompt": "This is a video screenshot, please generate a cover in the style of a manga",  # English only
                "strength": 0.75,
                "output_format": "jpeg",
                "mode": "image-to-image",
                "model": "sd3.5-large-turbo",
            },
        )

    if response.status_code == 200:
        with open(temp_cover_path, "wb") as file:
            file.write(response.content)
        os.remove(your_file_path)
        return temp_cover_path
    else:
        raise Exception(str(response.json()))
        return None


if __name__ == "__main__":
    print(stable_diffusion_generate_cover(""))
