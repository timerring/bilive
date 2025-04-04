from time import sleep
from src.log.logger import scan_log
from typing import Any, Tuple

class Retry:
    def __init__(self, max_retry: int, interval: int = 5, check_func = lambda r: r,  default = None):
        '''retry the function and check the return value
        Args:
            max_retry: the maximum of retries
            interval: the interval of retries
            check_func: the function to check the return value
            default: the default return value
        
        Return:
            status: the status of the excution of the function
            return_value: the return value of the function
        '''
        self.max_retry = max_retry
        self.check_func = check_func
        self.interval = interval
        self.default = default

    def run(self, func, *args, **kwargs) -> Tuple[bool, Any]:
        status = (False, self.default)
        for i in range(0, self.max_retry):
            try:
                return_value = func(*args, **kwargs)
                if self.check_func(return_value):
                    status = (True,return_value)
                    break
            except Exception as e:
                scan_log.error(f"Exceptions in trial {i+1}/{self.max_retry} : {e}")
                sleep(self.interval)

        return status

    def decorator(self, func):
        def _(*args, **kwargs):
            return self.run(func, *args, **kwargs)[1]
        return _
