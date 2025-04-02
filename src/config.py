# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from datetime import datetime
import configparser
from db.conn import create_table

# ============================ Your configuration ============================
GPU_EXIST=True
# Can be pipeline, append, merge
MODEL_TYPE = "append"
Inference_Model = "small"
TITLE = "{artist}直播回放-{date}-{title}" 
# You can change the title as you like, eg.
# f"{artist}直播回放-{date}-{title}" - Streamer直播回放-20250328-Live title
# f"{date}-{artist}直播回放" - 20250328-Streamer直播回放
DESC = "{artist}直播回放，直播间地址：{source_link} 内容仅供娱乐，直播中主播的言论、观点和行为均由主播本人负责，不代表录播员的观点或立场。"
# You can change the description as you like.
GIFT_PRICE_FILTER = 1 # The gift whose price is less than this value will be filtered, unit: RMB
RESERVE_FOR_FIXING = False # If encounter MOOV crash error, delete the video or reserve for fixing
# ============================ The video slice configuration ==================
AUTO_SLICE = False
SLICE_DURATION = 60 # better not exceed 300 seconds
SLICE_NUM = 2
SLICE_OVERLAP = 30
SLICE_STEP = 1
# The minimum video size to be sliced (MB)
MIN_VIDEO_SIZE = 200
# the multi-model LLMs, can be "gemini" or "zhipu" or "qwen"
MLLM_MODEL = "gemini" # Please make sure you have the right API key for the LLM you choose
# Apply for your own GLM-4v-Plus API key at https://www.bigmodel.cn/invite?icode=shBtZUfNE6FfdMH1R6NybGczbXFgPRGIalpycrEwJ28%3D
ZHIPU_API_KEY = ""
# Apply for your own Gemini API key at https://aistudio.google.com/app/apikey
GEMINI_API_KEY = ""
# Apply for your own Qwen API key at https://bailian.console.aliyun.com/?apiKey=1
QWEN_API_KEY = ""
# ============================ Basic configuration ============================
SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
BILIVE_DIR = str(Path(SRC_DIR).parent)
LOG_DIR = os.path.join(BILIVE_DIR, 'logs')
VIDEOS_DIR = os.path.join(BILIVE_DIR, 'Videos')


if not os.path.exists(SRC_DIR + '/db/data.db'):
    print("Initialize the database")
    create_table()

if not os.path.exists(VIDEOS_DIR):
    os.makedirs(VIDEOS_DIR)
if not os.path.exists(VIDEOS_DIR + '/upload_conf'):
    os.makedirs(VIDEOS_DIR + '/upload_conf')

def get_model_path():
    SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
    model_dir = os.path.join(SRC_DIR, 'subtitle', 'models')
    model_path = os.path.join(model_dir, f'{Inference_Model}.pt')
    return model_path

def get_interface_config():
    interface_config = configparser.ConfigParser()
    interface_dir = os.path.join(SRC_DIR, 'subtitle')
    interface_file = os.path.join(interface_dir, "en.ini")
    interface_config.read(interface_file, encoding='utf-8')
    return interface_config