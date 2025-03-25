# Copyright (c) 2024 bilive.

import subprocess
import os
import sys
from src.config import SRC_DIR, BILIVE_DIR
from datetime import datetime
from src.upload.generate_yaml import generate_yaml_template, generate_slice_yaml_template
from src.upload.extract_video_info import generate_title
from src.log.logger import upload_log
import time
import fcntl
from concurrent.futures import ThreadPoolExecutor, as_completed
from db.conn import get_single_upload_queue, delete_upload_queue, update_upload_queue_lock
import threading

read_lock = threading.Lock()

def upload_video(upload_path, yaml_file_path):
    try:
        # Construct the command
        command = [
            f"{SRC_DIR}/utils/biliup",
            "-u",
            f"{SRC_DIR}/utils/cookies.json",
            "upload",
            upload_path,
            "--config",
            yaml_file_path
        ]
        
        # Execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        upload_log.debug(f"Upload output:\nstdout: {result.stdout}\nstderr: {result.stderr}")
        
        # Check if the command was successful
        if result.returncode == 0:
            upload_log.info("Upload successfully, then delete the video")
            os.remove(upload_path)
            os.remove(yaml_file_path)
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
        # Construct the command
        command = [
            f"{SRC_DIR}/utils/biliup",
            "-u",
            f"{SRC_DIR}/utils/cookies.json",
            "append",
            "--vid",
            bv_result,
            upload_path
        ]
        # Execute the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        upload_log.debug(f"Append output:\nstdout: {result.stdout}\nstderr: {result.stderr}")

        # Check if the command was successful
        if result.returncode == 0:
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
        upload_queue = None
        # read the queue and update lock status to prevent other threads from reading the same data
        with read_lock:
            upload_queue = get_single_upload_queue()
            # if there is a task in the queue, try to lock the task
            if upload_queue:
                video_path, config_path = upload_queue.values()
                # lock the task by updating the locked status to 1
                update_result = update_upload_queue_lock(video_path, 1)
                # if failed to lock, log the error and let the next thread to handle the task
                if not update_result:
                    upload_log.error(f"Failed to lock task for {video_path}, possibly already locked by another thread or database error.")
                    upload_queue = None
                    continue
            else:
                upload_log.info("Empty queue, wait 2 minutes and check again.")
                time.sleep(120)
                continue
          
        if upload_queue:  
            video_path, config_path = upload_queue.values()
            upload_log.info(f"deal with {video_path}")
            # check if the live is already uploaded
            if video_path.endswith('.flv'):
                # upload slice video
                upload_video(video_path, config_path)
                return
            else:
                query = generate_title(video_path)
                result = subprocess.check_output("bilitool" + " list", shell=True)
                # print(result.decode("utf-8"), flush=True)
                upload_list = result.decode("utf-8").splitlines()
                bv_result = find_bv_number(query, upload_list)
                if bv_result:
                    upload_log.info(f"The series of videos has already been uploaded, the BV number is: {bv_result}")
                    append_upload(video_path, bv_result)
                else:
                    upload_log.info("First upload this live")
                    upload_video(video_path, config_path)
                    return
        time.sleep(20)
        

if __name__ == "__main__":    
    max_workers = os.getenv("MAX_WORKERS", 5)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_upload = {executor.submit(read_append_and_delete_lines) for _ in range(max_workers)}
        