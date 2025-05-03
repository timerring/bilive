import http.client
import json
import base64
import requests
import time
import os
from src.config import DMX_API_TOKEN, COVER_PROMPT


conn = http.client.HTTPSConnection("www.dmxapi.cn")

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_cover(your_file_path):
    image_base = get_image_base64(your_file_path)
    payload = json.dumps({
    "model_name": "kling-v1-5",
    "prompt": COVER_PROMPT,
    "image": image_base,
    "image_reference": "subject"
    })
    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}',
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/kling/v1/images/generations?=null", payload, headers)
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    print(json_data)
    return json_data['data']['task_id']

def get_kling_cover(task_id):
    action = "images"
    action2 = "generations"

    query_path = f"/kling/v1/{action}/{action2}/{task_id}"

    headers = {
    'Authorization': f'Bearer {DMX_API_TOKEN}'
    }

    conn.request("GET", query_path, None, headers)
    res = conn.getresponse()
    json_data = json.loads(res.read().decode("utf-8"))
    if json_data['data']['task_status'] == "succeed":
        return json_data['data']['task_result']['images'][0]['url']
    else: 
        return None

def kling_generate_cover(your_file_path):
    task_id = generate_cover(your_file_path)
    start_time = time.time()
    timeout = 60

    while True:
        image_url = get_kling_cover(task_id)
        if image_url is not None:
            img_data = requests.get(image_url).content
            cover_name = time.strftime("%Y%m%d%H%M%S") + ".png"
            temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
            with open(temp_cover_path, "wb") as handler:
                handler.write(img_data)
            os.remove(your_file_path)
            return temp_cover_path
        
        if time.time() - start_time > timeout:
            print(f"Generate cover {timeout} seconds timeout")
            return None

        time.sleep(1)
        print(f"Waiting for cover generation, {int(time.time() - start_time)} seconds", flush=True)

if __name__ == "__main__":
    your_file_path = ""
    print(kling_generate_cover(your_file_path))