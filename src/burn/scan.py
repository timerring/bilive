# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from src.burn.only_render import render_video_only, VideoRenderQueue
from src.burn.render_and_merge import render_and_merge
import time
from src.config import VIDEOS_DIR, MODEL_TYPE
import threading
from src.log.logger import scan_log

def process_folder_merge(folder_path):
    # Don't process the recording folder
    flv_files = list(Path(folder_path).glob('*.flv'))
    if flv_files:
        scan_log.info(f"Found flv files in {folder_path}. Skipping.")
        return

    files_by_date = {}

    # process the recorded files
    mp4_files = [mp4_file for mp4_file in Path(folder_path).glob('*.mp4') if not mp4_file.name.endswith('-.mp4')]
    for mp4_file in mp4_files:
        date_part = mp4_file.stem.split('_')[1].split('-')[0]

        if date_part not in files_by_date:
            files_by_date[date_part] = []
        files_by_date[date_part].append(mp4_file)

    for date, files in files_by_date.items():
        if len(files) > 1:
            # If there are multiple segments with the same date, merge them
            sorted_files = sorted(files, key=lambda x: x.stem.split('_')[1])
            scan_log.info(f"Merging {sorted_files}...")
            render_and_merge(sorted_files)
        else:
            for file in files:
                scan_log.info(f"Begin processing {file}...")
                render_video_only(file)

def process_folder_append(folder_path):
    # process the recorded files
    mp4_files = [mp4_file for mp4_file in Path(folder_path).glob('*.mp4') if not mp4_file.name.endswith('-.mp4')]
    mp4_files.sort()
    for file in mp4_files:
        scan_log.info(f"Begin processing {file}...")
        if MODEL_TYPE == "pipeline":
            video_render_queue.pipeline_render(file)
        else:
            render_video_only(file)

if __name__ == "__main__":
    room_folder_path = VIDEOS_DIR
    video_render_queue = VideoRenderQueue()
    monitor_thread = threading.Thread(target=video_render_queue.monitor_queue)
    monitor_thread.start()
    while True:
        for room_folder in Path(room_folder_path).iterdir():
            if room_folder.is_dir():
                if MODEL_TYPE == "merge":
                    process_folder_merge(room_folder)
                else:
                    process_folder_append(room_folder)
        scan_log.info("There is no file recorded. Check again in 120 seconds.")
        time.sleep(120)