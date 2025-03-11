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

def read_and_delete_lines(file_path):
    while True:
        if os.path.getsize(file_path) == 0:
            upload_log.info("Empty queue, wait 2 minutes and check again.")
            time.sleep(120)
            continue

        with open(file_path, "r") as file:
            lines = file.readlines()
            upload_video_path = lines.pop(0).strip()
            upload_log.info(f"deal with {upload_video_path}")
            # generate the yaml template
            yaml_template = generate_yaml_template(upload_video_path)
            yaml_file_path = SRC_DIR + "/upload/upload.yaml"
            with open(yaml_file_path, 'w', encoding='utf-8') as file:
                file.write(yaml_template)
            upload_video(upload_video_path, yaml_file_path)
        with open(file_path, "w") as file:
            file.writelines(lines)

def upload_video(upload_path, yaml_file_path):
    try:
        # Construct the command
        command = [
            f"{BILIVE_DIR}/src/upload/biliup",
            "-u",
            f"{SRC_DIR}/upload/cookies.json",
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
        else:
            upload_log.error("Fail to upload, the files will be reserved.")
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The upload_video called failed, the files will be reserved. error: {e}")
        return False

def find_bv_number(target_str, my_list):
    for element in my_list:
        if target_str in element:
            parts = element.split('|')
            if len(parts) > 0:
                return parts[1].strip()
    return None

def read_append_and_delete_lines(file_path):
    try:
        while True:
            if os.path.getsize(file_path) == 0:
                upload_log.info("Empty queue, wait 2 minutes and check again.")
                time.sleep(120)
                return

            with open(file_path, "r+") as file:
                fcntl.flock(file, fcntl.LOCK_EX)
                lines = file.readlines()
                upload_video_path = lines.pop(0).strip()
                file.seek(0)
                file.writelines(lines)
                # Truncate the file to the current position
                file.truncate()
                # Release the lock
                fcntl.flock(file, fcntl.LOCK_UN)

            upload_log.info(f"deal with {upload_video_path}")
            # check if the live is already uploaded
            if upload_video_path.endswith('.flv'):
                # upload slice video
                yaml_template = generate_slice_yaml_template(upload_video_path)
                yaml_file_path = SRC_DIR + "/upload/upload.yaml"
                with open(yaml_file_path, 'w', encoding='utf-8') as file:
                    file.write(yaml_template)
                upload_video(upload_video_path, yaml_file_path)
                return
            else:
                query = generate_title(upload_video_path)
                result = subprocess.check_output("bilitool" + " list", shell=True)
                # print(result.decode("utf-8"), flush=True)
                upload_list = result.decode("utf-8").splitlines()
                bv_result = find_bv_number(query, upload_list)
                if bv_result:
                    upload_log.info(f"The series of videos has already been uploaded, the BV number is: {bv_result}")
                    append_upload(upload_video_path, bv_result)
                else:
                    upload_log.info("First upload this live")
                    # generate the yaml template
                    yaml_template = generate_yaml_template(upload_video_path)
                    yaml_file_path = SRC_DIR + "/upload/upload.yaml"
                    with open(yaml_file_path, 'w', encoding='utf-8') as file:
                        file.write(yaml_template)
                    upload_video(upload_video_path, yaml_file_path)
                    return
                
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The read_append_and_delete_lines called failed, the files will be reserved. error: {e}")
        return False

def append_upload(upload_path, bv_result):
    try:
        # Construct the command
        command = [
            f"{BILIVE_DIR}/src/upload/biliup",
            "-u",
            f"{SRC_DIR}/upload/cookies.json",
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
        else:
            upload_log.error("Fail to append, the files will be reserved.")
            return False
    
    except subprocess.CalledProcessError as e:
        upload_log.error(f"The append_upload called failed, the files will be reserved. error: {e}")
        return False

if __name__ == "__main__":    
    # read the queue and upload the video
    queue_path = SRC_DIR + "/upload/uploadVideoQueue.txt"
    # read_and_delete_lines(queue_path)
    while True:
        read_append_and_delete_lines(queue_path)
        upload_log.info("wait for 20 seconds")
        time.sleep(20)