# Copyright (c) 2024 bilive.

import subprocess
import os
import sys
from src.config import SRC_DIR, BILIVE_DIR
from datetime import datetime
from src.upload.generate_upload_data import generate_video_data, generate_slice_data
from src.upload.extract_video_info import generate_title
from src.log.logger import upload_log
import time
import fcntl
from concurrent.futures import ThreadPoolExecutor, as_completed
from db.conn import get_single_upload_queue, delete_upload_queue, update_upload_queue_lock
import threading
from .bilitool.bilitool import UploadController, FeedController, LoginController

# read_lock = threading.Lock()

def upload_video(upload_path):
    try:
        if upload_path.endswith('.flv'):
            copyright, title, tid, tag = generate_slice_data(upload_path)
        else:
            copyright, title, desc, tid, tag, source, cover, dynamic = generate_video_data(upload_path)
            yaml = ""
        result = UploadController().upload_video_entry(upload_path, yaml, copyright, tid, title, desc, tag, source, cover, dynamic)
        if result == True:
            upload_log.info("Upload successfully, then delete the video")
            os.remove(upload_path)
            delete_upload_queue(upload_path)
        else:
            upload_log.error("Fail to upload, the files will be reserved.")
            update_upload_queue_lock(upload_path, 0)
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The upload_video called failed, the files will be reserved. error: {e}")
        update_upload_queue_lock(upload_path, 0)
        return False

def find_bv_number(target_str, my_list):
    for element in my_list:
        if target_str in element:
            parts = element.split('|')
            if len(parts) > 0:
                return parts[1].strip()
    return None


def append_upload(upload_path, bv_result):
    try:
        result = UploadController().append_video_entry(upload_path, bv_result)
        # Check if the command was successful
        if result == True:
            upload_log.info("Upload successfully, then delete the video")
            os.remove(upload_path)
            delete_upload_queue(upload_path)
        else:
            upload_log.error("Fail to append, the files will be reserved.")
            update_upload_queue_lock(upload_path, 0)
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The append_upload called failed, the files will be reserved. error: {e}")
        update_upload_queue_lock(upload_path, 0)
        return False
    
    
def read_append_and_delete_lines():
    while True:
        # upload_queue = None
        # read the queue and update lock status to prevent other threads from reading the same data
        if LoginController().check_bilibili_login():
            pass
        else:
            file = BILIVE_DIR + "/cookie.json"
            LoginController().login_bilibili_with_cookie_file(file)
            # LoginController().login_bilibili(export=False)
            continue
        # with read_lock:
        upload_queue = get_single_upload_queue()
        # if there is a task in the queue, try to lock the task
        if upload_queue:  
            video_path = upload_queue['video_path']
            time.sleep(3)
            query = generate_title(video_path)
            if query is None:
                if not os.path.exists(video_path):
                    delete_upload_queue(video_path)
                    continue
                else:
                    upload_log.error(f"Error occurred in ffprobe: {video_path}")
                    update_upload_queue_lock(video_path, 1)
                    continue
            upload_log.info(f"deal with {video_path}")
            # check if the live is already uploaded
            if video_path.endswith('.flv'):
                # upload slice video
                upload_video(video_path)
            else:
                upload_dict = FeedController().get_video_dict_info(20, "pubed,not_pubed,is_pubing")
                bv_result = upload_dict.get(query)
                if bv_result:
                    upload_log.info(f"The series of videos has already been uploaded, the BV number is: {bv_result}")
                    append_upload(video_path, bv_result)
                else:
                    upload_log.info("First upload this live")
                    upload_video(video_path)
            time.sleep(20)
        else:
            upload_log.info("Empty queue, wait 2 minutes and check again.")
            time.sleep(120)
        

if __name__ == "__main__":    
    # max_workers = os.getenv("MAX_WORKERS", 1)
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     future_to_upload = {executor.submit(read_append_and_delete_lines) for _ in range(max_workers)}
    read_append_and_delete_lines()
        