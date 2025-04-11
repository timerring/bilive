# Copyright (c) 2024 bilive.

import queue
import time
from src.subtitle.subtitle_generator import generate_subtitle
from src.burn.render_video import render_video
from src.log.logger import scan_log


class VideoRenderQueue:
    def __init__(self):
        self.render_queue = queue.Queue()

    def pipeline_render(self, video_path):
        generate_subtitle(video_path)
        self.render_queue.put(video_path)

    def monitor_queue(self):
        while True:
            if not self.render_queue.empty():
                video_path = self.render_queue.get()
                try:
                    render_video(video_path)
                except Exception as e:
                    scan_log.error(f"Error processing video {video_path}: {e}")
            else:
                time.sleep(1)
