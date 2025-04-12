import requests
import json
import uuid
import base64
from src.config import HIDREAM_API_KEY, COVER_PROMPT
 
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def _get_task_id(image_path):
    image_base64 = get_image_base64(image_path)
    headers = {
        'Authorization': f'Bearer {HIDREAM_API_KEY}',
        'Content-Type': 'application/json',
        'API-User-ID': ''
    }
    
    data = {
        "image": image_base64,
        "prompt": COVER_PROMPT,
        "negative_prompt": "sun",
        "img_count": 1,
        "version": "v1",
        "resolution": "2048*2048",
        "request_id": str(uuid.uuid4())
    }
    
    url = 'https://www.hidreamai.com/api-pub/gw/v3/image/img2img/async'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        if response.json()['code'] == 0:
            task_id = response.json()['result']['task_id']
            return task_id
        else:
            print(response.json()['message'])
            return None
    else:
        print(response.status_code)
        return None

def hidream_generate_cover(your_file_path):
    task_id = _get_task_id(your_file_path)
    if task_id:
        headers = {
            'Authorization': f'Bearer {HIDREAM_API_KEY}'
        }
        
        params = {
            'task_id': task_id,
            'request_id': ''
        }
        
        url = 'https://www.hidreamai.com/api-pub/gw/v3/image/img2img/async/results'
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            if response.json()['code'] == 0:
                image_url = response.json()['result']['sub_task_results']['image']
                img_data = requests.get(image_url).content
                cover_name = time.strftime("%Y%m%d%H%M%S") + ".jpg"
                temp_cover_path = os.path.join(os.path.dirname(your_file_path), cover_name)
                with open(temp_cover_path, "wb") as handler:
                    handler.write(img_data)
                os.remove(your_file_path)
                return temp_cover_path                    
            else:
                print(response.json()['message'])
                return None
        else:
            print(response.status_code)
            return None
    else:
        return None


if __name__ == "__main__":
    print(hidream_generate_cover(""))