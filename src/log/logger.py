# Copyright (c) 2024 bilive.

import logging
import time
import os
from typing import Optional
from functools import partial
from config import LOG_DIR

class Logger:
    def __init__(self, log_file_prefix: Optional[str] = None):
        self.log_file_prefix = log_file_prefix
        self._logger = None

    def __get__(self, instance, owner):
        if self._logger is None:
            self._logger = self._create_logger()
        return self._logger

    def _create_logger(self):
        logger = logging.getLogger(f"bilive {self.log_file_prefix}")
        if not logger.handlers:
            logger.setLevel('DEBUG')
            formatter = logging.Formatter('[%(levelname)s] - [%(asctime)s %(name)s] - %(message)s')
            
            # console output
            console_handler = logging.StreamHandler()
            console_handler.setLevel('INFO')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # file output
            now = time.strftime('%Y%m%d', time.localtime(time.time()))
            log_folder = f"{LOG_DIR}/{self.log_file_prefix}"
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)
            path = f"{log_folder}/{self.log_file_prefix}-{now}.log"
            file_handler = logging.FileHandler(path, encoding='UTF-8')
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        return logger

class Log:
    def __init__(self, log_file_prefix: Optional[str] = None):
        self.logger = Logger(log_file_prefix)

    @property
    def debug(self):
        return partial(self.logger.__get__(None, None).debug)
        
    @property
    def info(self):
        return partial(self.logger.__get__(None, None).info)
        
    @property
    def warning(self):
        return partial(self.logger.__get__(None, None).warning)
        
    @property
    def error(self):
        return partial(self.logger.__get__(None, None).error)
        
    @property
    def critical(self):
        return partial(self.logger.__get__(None, None).critical)

scan_log = Log("scan")
upload_log = Log("upload")

if __name__ == '__main__':
    for i in range(1000):
        scan_log.info(f"Starting scan module... {i}")
        time.sleep(0.1)
        scan_log.debug(f"Debug information in scan module {i}")

        upload_log.info(f"Starting upload module... {i}")
        time.sleep(0.1)
        upload_log.error(f"Upload failed! {i}")