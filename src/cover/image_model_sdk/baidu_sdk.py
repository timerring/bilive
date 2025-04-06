import requests
import json
import os
import base64
from PIL import Image
from io import BytesIO
import time
from src.upload.bilitool.bilitool.model.model import Model
from src.config import BAIDU_API_KEY


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


def baidu_generate_cover(your_file_path):
    """Generater cover image using baidu api
    Args:
        your_file_path: str, path to the image file
    Returns:
        str, local download path of the generated cover image file
    """
    try:
        cover_url = cover_up(your_file_path)

        url = "https://qianfan.baidubce.com/v2/images/generations"
        payload = json.dumps(
            {
                "model": "irag-1.0",
                "prompt": "这是视频截图，请根据该图生成对应的动漫类型的封面",
                "refer_image": cover_url,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BAIDU_API_KEY}",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            image_url = response.json()["data"][0]["url"]
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
    except Exception as e:
        print(e, flush=True)
        return None


if __name__ == "__main__":
    print(baidu_generate_cover(""))
