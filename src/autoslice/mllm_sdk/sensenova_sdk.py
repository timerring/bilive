import requests
import os
from src.config import SENSENOVA_API_KEY, SLICE_PROMPT
from src.log.logger import scan_log


class SenseNova:
    def __init__(self, model_id):
        self.model_id = model_id
        self.headers = {"Authorization": "Bearer " + SENSENOVA_API_KEY}

    # file size limit: 45 MB
    def _upload_video(self, file_path):
        """Upload the video to the SenseNova server and return the file_id
        Docs: https://console.sensecore.cn/micro/help/docs/model-as-a-service/nova/overview/file/CreateFile/

        Args:
            file_path (str): The path to the video file
        Returns:
            str: The file_id of the uploaded video / None if failed
        """
        data = {"description": "string", "scheme": "MULTIMODAL_2"}
        url = "https://file.sensenova.cn/v1/files"
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                r = requests.post(url, headers=self.headers, data=data, files=files)
                if r.status_code == 200:
                    file_id = r.json()["id"]
                    scan_log.info(f"upload video success, file_id: {file_id}")
                    return file_id
                else:
                    scan_log.error(f"upload video failed, {r.text}")
                    return None
        except Exception as e:
            scan_log.error(e)

    def _delete_video(self, file_id):
        """Delete the video from the SenseNova server
        Docs: https://console.sensecore.cn/micro/help/docs/model-as-a-service/nova/overview/file/DeleteFile

        Args:
            file_id (str): The file_id of the video to delete
        """
        url = "https://file.sensenova.cn/v1/files/" + file_id
        r = requests.delete(url, headers=self.headers)
        if r.status_code == 200:
            scan_log.info("delete video success")
        else:
            scan_log.error("delete video failed")

    def chat_multi(self, query, file_id):
        """Chat with the SenseNova
        Docs: https://console.sensecore.cn/micro/help/docs/model-as-a-service/nova/vision/ChatCompletions/

        Args:
            query (str): The query to chat with the SenseNova server
            file_id (str): The file_id of the video to chat with
        """
        url = "https://api.sensenova.cn/v1/llm/chat-completions"
        if file_id is None:
            scan_log.error("upload video failed")
            return None
        payload = {
            "model": self.model_id,
            "messages": [
                {
                    "content": [
                        {"type": "video_file_id", "video_file_id": file_id},
                        {"text": query, "type": "text"},
                    ],
                    "role": "user",
                }
            ],
            "max_new_tokens": 1024,
            "repetition_penalty": 1.05,
            "temperature": 0.7,
            "stream": False,
            "top_p": 0.25,
        }
        r = requests.post(url, json=payload, headers=self.headers)
        # request_id = r.headers["x-request-id"]
        # first_trunk = r.elapsed.total_seconds()
        # print("first_trunk: ", first_trunk)
        # print(r, request_id, r.headers, r.text)
        if r.status_code == 200:
            title_with_french_quotes = r.json()["data"]["choices"][0]["message"]
            title = title_with_french_quotes.replace("《", "").replace("》", "")
            return title
        else:
            scan_log.error(f"chat multi failed, {r.text}")
            return None


def sensenova_generate_title(file_path, artist, model_id="SenseNova-V6-Pro"):
    query = SLICE_PROMPT.format(artist=artist)
    scan_log.info(f"Using {model_id} to generate slice title")
    scan_log.info(f"Prompt: {query}")
    try:
        sense_nova = SenseNova(model_id)
        file_id = sense_nova._upload_video(file_path)
        if file_id is None:
            scan_log.error("upload video failed")
            return None
        title = sense_nova.chat_multi(query, file_id)
        if title:
            sense_nova._delete_video(file_id)
            scan_log.info(f"Generated slice title: {title}")
            return title
        else:
            scan_log.error("Generate slice title failed")
            return None
    except Exception as e:
        scan_log.error(e)
        return None
