# Installation common issues

> If you don't find the problem you encountered, please submit it in [issues](https://github.com/timerring/bilive/issues/new/choose).

## OSError: sndfile library not found

Reference: https://github.com/timerring/bilive/issues/106

Solution: Install the corresponding library `apt-get install libsndfile1`.

## requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))

https://stackoverflow.com/questions/70379603/python-script-is-failing-with-connection-aborted-connectionreseterror104

Known network environment reasons

Solution: proxy.

## ERROR: Could not find a version that satisfies the requirement triton==3.1.0 (from versions: none) ERROR: No matching distribution found for triton==3.1.0

From [issue 168](https://github.com/timerring/bilive/issues/168)

According to https://github.com/triton-lang/triton/issues/1057, there may be such a problem.

Solution: I checked that the pypi library has updated the triton 3.1.0 version: https://pypi.org/project/triton/#history, you can consider upgrading pip, or directly pull the whl installation from huggingface, it is not a problem. The test machine version is linux python3.10.12 pip, it is not a problem.

> Also, triton is a library for inference, if you don't need to use whisper to generate subtitles, you can also not install it.

## ModuleNotFoundError: No module named 'fcntl'

The file lock `fcntl` module does not support windows, there are some alternative ways, but the best solution is to use WSL to run this project.

Solution: Use WSL to run this project.