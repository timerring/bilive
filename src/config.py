# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from datetime import datetime
import configparser

# ============================ Your configuration ============================
GPU_EXIST=True
# Can be pipeline, append, merge
MODEL_TYPE = "append"
Inference_Model = "small"
# ============================ The video slice configuration ==================
AUTO_SLICE = False
SLICE_DURATION = 30
# The minimum video size to be sliced (MB)
MIN_VIDEO_SIZE = 200
# Apply for your own GLM-4v-Plus API key at https://www.bigmodel.cn/invite?icode=shBtZUfNE6FfdMH1R6NybGczbXFgPRGIalpycrEwJ28%3D
Your_API_KEY = ""
# ============================ Basic configuration ============================
SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
BILIVE_DIR = str(Path(SRC_DIR).parent)
LOG_DIR = os.path.join(BILIVE_DIR, 'logs')
VIDEOS_DIR = os.path.join(BILIVE_DIR, 'Videos')

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