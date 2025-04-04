# Copyright (c) 2024 bilive.

import subprocess
import os
import sys
from src.config import SRC_DIR, BILIVE_DIR, RESERVE_FOR_FIXING, UPLOAD_LINE
from datetime import datetime
from src.upload.generate_upload_data import generate_video_data, generate_slice_data
from src.upload.extract_video_info import generate_title
from src.log.logger import upload_log
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from db.conn import get_single_upload_queue, delete_upload_queue, update_upload_queue_lock, get_single_lock_queue
from .bilitool.bilitool import UploadController, FeedController, LoginController
from src.log.retry import Retry

@Retry(max_retry = 3, interval = 5).decorator
def upload_video(upload_path):
    try:
        if upload_path.endswith('.flv'):
            copyright, title, tid, tag = generate_slice_data(upload_path)
            yaml, desc, source, cover, dynamic = ("",) * 5
            if title is None:
                upload_log.error("Fail to upload slice video, the files will be reserved.")
                update_upload_queue_lock(upload_path, 0)
                return False
        else:
            copyright, title, desc, tid, tag, source, cover, dynamic = generate_video_data(upload_path)
            yaml = ""
        result = UploadController().upload_video_entry(upload_path, yaml, copyright, tid, title, desc, tag, source, cover, dynamic, cdn=UPLOAD_LINE)
        if result == True:
            upload_log.info("Upload successfully, then delete the video")
            os.remove(upload_path)
            delete_upload_queue(upload_path)
            return True
        else:
            upload_log.error("Fail to upload, the files will be reserved.")
            update_upload_queue_lock(upload_path, 0)
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The upload_video called failed, the files will be reserved. error: {e}")
        update_upload_queue_lock(upload_path, 0)
        return False

@Retry(max_retry = 3, interval = 5).decorator
def append_upload(upload_path, bv_result):
    try:
        result = UploadController().append_video_entry(upload_path, bv_result, cdn=UPLOAD_LINE)
        # Check if the command was successful
        if result == True:
            upload_log.info("Upload successfully, then delete the video")
            os.remove(upload_path)
            delete_upload_queue(upload_path)
            return True
        else:
            upload_log.error("Fail to append, the files will be reserved.")
            update_upload_queue_lock(upload_path, 0)
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The append_upload called failed, the files will be reserved. error: {e}")
        update_upload_queue_lock(upload_path, 0)
        return False

def video_gate(video_path):
    if video_path.endswith('.flv'): # slice video tag
        # upload slice video
        upload_video(video_path)
    else:
        # get the uploaded video list
        upload_dict = FeedController().get_video_dict_info(20, "pubed,not_pubed,is_pubing")
        query = generate_title(video_path)
        bv_result = upload_dict.get(query) # query this title
        if bv_result:
            upload_log.info(f"The series of videos has already been uploaded, the BV number is: {bv_result}")
            append_upload(video_path, bv_result)
        else:
            upload_log.info("First upload this live")
            upload_video(video_path)
    time.sleep(5) # avoid JIT read error

def read_append_and_delete_lines():
    while True:
        if LoginController().check_bilibili_login():
            pass
        else:
            file = BILIVE_DIR + "/cookie.json"
            LoginController().login_bilibili_with_cookie_file(file)
            # LoginController().login_bilibili(export=False) # reserve for docker version
            continue
        upload_queue = get_single_upload_queue()
        lock_queue = get_single_lock_queue()
        if upload_queue:  
            video_path = upload_queue['video_path']
            time.sleep(3) # avoid JIT read error
            if video_path.endswith('.flv'):
                video_gate(video_path)
            else:
                query = generate_title(video_path)
                if query is None: # JIT read error or MOOV crash error or interrupted error
                    if not os.path.exists(video_path):
                        # Interrupted error, the file has been uploaded. But record is not deleted.
                        delete_upload_queue(video_path) # Directly delete the record
                        continue
                    else:
                        # JIT read error or MOOV crash error
                        upload_log.error(f"Error occurred in ffprobe: {video_path}")
                        update_upload_queue_lock(video_path, 1) # Lock first, wait for the lock execute round
                        continue
                upload_log.info(f"deal with {video_path}")
                video_gate(video_path)
        elif lock_queue:
            # check the lock video
            video_path = lock_queue['video_path']
            if not os.path.exists(video_path):
                # Interrupted error, the file has been uploaded. But record is not deleted.
                delete_upload_queue(video_path) # Directly delete the record
                continue
            else:
                query = generate_title(video_path)
                if query is None:
                    if RESERVE_FOR_FIXING:
                        # MOOV crash error
                        upload_log.error(f"MOOV crash error, {video_path} is reserved for fixing")
                        update_upload_queue_lock(video_path, 2) # Reserve for fixing
                    else:
                        # JIT read error
                        delete_upload_queue(video_path) # Directly delete the record
                        os.remove(video_path)
                else:
                    upload_log.info(f"deal with {video_path} in lock queue")
                    video_gate(video_path)
        else:
            upload_log.info("Empty queue, wait 2 minutes and check again.")
            time.sleep(120)
        

if __name__ == "__main__":    
    # max_workers = os.getenv("MAX_WORKERS", 1)
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     future_to_upload = {executor.submit(read_append_and_delete_lines) for _ in range(max_workers)}
    read_append_and_delete_lines()
        