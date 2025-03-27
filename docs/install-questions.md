# 安装常见问题

> 如果没有找到遇到的问题，请及时在 [issues](https://github.com/timerring/bilive/issues/new/choose) 中提出。

## OSError: sndfile library not found

Reference: https://github.com/timerring/bilive/issues/106

解决方案：安装对应的库即可 `apt-get install libsndfile1`。

## Error /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.34’ not found

Reference: https://blog.csdn.net/huazhang_001/article/details/128828999

尽量使用 22.04+ 的版本，更早版本的 ubuntu 自带 gcc 版本无法更新至 biliup-rs 所需版本。

解决方案：手动更新版本，参照链接操作即可。

## requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))

https://stackoverflow.com/questions/70379603/python-script-is-failing-with-connection-aborted-connectionreseterror104

众所周知的网络环境原因

解决方案：proxy。

## ERROR: Could not find a version that satisfies the requirement triton==3.1.0 (from versions: none) ERROR: No matching distribution found for triton==3.1.0

From [issue 168](https://github.com/timerring/bilive/issues/168)

根据 https://github.com/triton-lang/triton/issues/1057 确实可能存在这样的问题。

解决方案：我查 pypi 里已经更新了 triton 3.1.0 版本：https://pypi.org/project/triton/#history 可以考虑升级一下 pip，或者直接从 huggingface 上拉 whl 安装也没问题。测试机器版本 linux python3.10.12 pip 下是没问题的。

> 另外，triton 是一个推理的库，如果不需要用到 whisper 生成字幕的话，不装它也可以。

## ModuleNotFoundError: No module named 'fcntl'

文件锁 `fcntl` 模块不支持 windows，有一些替代方式，但是最佳的解决方法就是使用 WSL 运行本项目。

解决方案：使用 WSL 运行本项目。