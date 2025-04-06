# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from datetime import datetime
import configparser
import torch
import toml
from db.conn import create_table

def load_config_from_toml(file_path):
    """
    load config from toml file and update global variables
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = toml.load(file)
            return config
    except FileNotFoundError:
        print(f"cannot find {file_path}", flush=True)
    except toml.TomlDecodeError as e:
        print(f"cannot parse {file_path} as a valid toml file, error: {e}", flush=True)
    except Exception as e:
        print(f"unknown error when loading config file, error: {e}", flush=True)
    return None

def get_model_path():
    SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
    model_dir = os.path.join(SRC_DIR, 'subtitle', 'models')
    model_path = os.path.join(model_dir, f'{INFERENCE_MODEL}.pt')
    return model_path

def get_interface_config():
    interface_config = configparser.ConfigParser()
    interface_dir = os.path.join(SRC_DIR, 'subtitle')
    interface_file = os.path.join(interface_dir, "en.ini")
    interface_config.read(interface_file, encoding='utf-8')
    return interface_config

SRC_DIR = str(Path(os.path.abspath(__file__)).parent)
BILIVE_DIR = str(Path(SRC_DIR).parent)
LOG_DIR = os.path.join(BILIVE_DIR, 'logs')
VIDEOS_DIR = os.path.join(BILIVE_DIR, 'Videos')
if not os.path.exists(SRC_DIR + '/db/data.db'):
    print("Initialize the database", flush=True)
    create_table()

config = load_config_from_toml(os.path.join(BILIVE_DIR, 'bilive.toml'))
if config is None:
    print("failed to load config file, please check twice", flush=True)
    exit(1)

GPU_EXIST = torch.cuda.is_available()
MODEL_TYPE = config.get('model', {}).get('model_type')
ASR_METHOD = config.get('asr', {}).get('asr_method')
WHISPER_API_KEY = config.get('asr', {}).get('whisper_api_key')
INFERENCE_MODEL = config.get('asr', {}).get('inference_model')

TITLE = config.get('video', {}).get('title')
DESC = config.get('video', {}).get('description')
GIFT_PRICE_FILTER = config.get('video', {}).get('gift_price_filter')
RESERVE_FOR_FIXING = config.get('video', {}).get('reserve_for_fixing')
UPLOAD_LINE = config.get('video', {}).get('upload_line')
AUTO_SLICE = config.get('slice', {}).get('auto_slice')
SLICE_DURATION = config.get('slice', {}).get('slice_duration')
SLICE_NUM = config.get('slice', {}).get('slice_num')
SLICE_OVERLAP = config.get('slice', {}).get('slice_overlap')
SLICE_STEP = config.get('slice', {}).get('slice_step')
MIN_VIDEO_SIZE = config.get('slice', {}).get('min_video_size')
MLLM_MODEL = config.get('slice', {}).get('mllm_model')
ZHIPU_API_KEY = config.get('slice', {}).get('zhipu_api_key')
GEMINI_API_KEY = config.get('slice', {}).get('gemini_api_key')
QWEN_API_KEY = config.get('slice', {}).get('qwen_api_key')

GENERATE_COVER = config.get('cover', {}).get('generate_cover')
IMAGE_GEN_MODEL = config.get('cover', {}).get('image_gen_model')
MINIMAX_API_KEY = config.get('cover', {}).get('minimax_api_key')
SILICONFLOW_API_KEY = config.get('cover', {}).get('siliconflow_api_key')
TENCENT_SECRET_ID = config.get('cover', {}).get('tencent_secret_id')
TENCENT_SECRET_KEY = config.get('cover', {}).get('tencent_secret_key')
BAIDU_API_KEY = config.get('cover', {}).get('baidu_api_key')
STABILITY_API_KEY = config.get('cover', {}).get('stability_api_key')