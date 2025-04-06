import requests
import json
import time
import os
import base64
from PIL import Image
from io import BytesIO
from lumaai import LumaAI
from src.upload.bilitool.bilitool.model.model import Model
from src.config import LUMA_API_KEY


def cover_up(img: str):
    """Upload the cover image
    Parameters
    ----------
    - img: img path or stream
    Returns
    -------
    - url: str
        the url of the cover image in bili server
    """
    from PIL import Image
    from io import BytesIO

    request = requests.Session()
    request.headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108",
        "referer": "https://www.bilibili.com/",
        "connection": "keep-alive",
    }
    model = Model().get_config()
    request.cookies.set("SESSDATA", model["cookies"]["SESSDATA"])
    with Image.open(img) as im:
        # you should keep the image ratio 16:10
        xsize, ysize = im.size
        if xsize / ysize > 1.6:
            delta = xsize - ysize * 1.6
            region = im.crop((delta / 2, 0, xsize - delta / 2, ysize))
        else:
            delta = ysize - xsize * 10 / 16
            region = im.crop((0, delta / 2, xsize, ysize - delta / 2))
        buffered = BytesIO()
        region.save(buffered, format=im.format)
    r = request.post(
        url="https://member.bilibili.com/x/vu/web/cover/up",
        data={
            "cover": b"data:image/jpeg;base64,"
            + (base64.b64encode(buffered.getvalue())),
            "csrf": model["cookies"]["bili_jct"],
        },
        timeout=30,
    )
    buffered.close()
    res = r.json()
    if res.get("data") is None:
        raise Exception(res)
    print(res["data"]["url"], flush=True)
    return res["data"]["url"]


def luma_generate_cover(your_file_path):
    """Generate cover for video using Luma Photon
    Args:
        your_file_path: str, path to the video file
    Returns:
        str: generated cover
    """
    try:
        cover_url = cover_up(your_file_path)
        client = LumaAI(
            auth_token=LUMA_API_KEY,
        )
        generation = client.generations.image.create(
            prompt="This is a video screenshot, please generate a cover in the style of a manga",
            image_ref=[{"url": cover_url, "weight": 0.85}],
        )
        completed = False
        while not completed:
            generation = client.generations.get(id=generation.id)
            if generation.state == "completed":
                completed = True
            elif generation.state == "failed":
                raise RuntimeError(f"Generation failed: {generation.failure_reason}")
            print("Dreaming")
            time.sleep(2)

        image_url = generation.assets.image

        response = requests.get(image_url, stream=True)
        cover_name = time.strftime("%Y%m%d%H%M%S") + ".jpg"
        temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
        with open(temp_cover_path, "wb") as file:
            file.write(response.content)
        os.remove(your_file_path)
        return temp_cover_path
    except Exception as e:
        print(e, flush=True)
        return None


if __name__ == "__main__":
    print(luma_generate_cover(""))
