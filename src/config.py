# Copyright (c) 2024 bilive.

import os
from pathlib import Path
from datetime import datetime
import configparser
import torch
import toml
import src.log.logger as scan_log
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
        scan_log.error(f"cannot find {file_path}")
    except toml.TomlDecodeError as e:
        scan_log.error(f"cannot parse {file_path} as a valid toml file, error: {e}")
    except Exception as e:
        scan_log.error(f"unknown error when loading config file, error: {e}")
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
    scan_log.info("Initialize the database")
    create_table()

config = load_config_from_toml(os.path.join(BILIVE_DIR, 'settings.toml'))
if config is None:
    scan_log.error("failed to load config file, please check twice")
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
