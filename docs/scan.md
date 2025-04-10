# scan common issues

> If you don't find the problem you encountered, please submit it in [issues](https://github.com/timerring/bilive/issues/new/choose).

## About rendering speed

The rendering speed mainly depends on the hardware and the number of danmaku. The basic test hardware is 2 cores Xeon(R) Platinum 85 CPU, the rendering speed is between 3 ~ 6 times, and can also use Nvidia GPU acceleration. The test graphics card is GTX1650, its rendering speed is between 16 ~ 20 times.

The specific rendering time of danmaku can be estimated by `rendering speed x video duration`.

Related references for using Nvidia GPU acceleration:
+ [Using FFmpeg with NVIDIA GPU Hardware Acceleration](https://docs.nvidia.com/video-technologies/video-codec-sdk/12.0/ffmpeg-with-nvidia-gpu/index.html)
+ [Using GPU to accelerate FFmpeg](https://yukihane.work/li-gong/ffmpeg-with-gpu)

## Why does the rendering speed decrease?

Long-term use of GPU may cause the GPU to be downgraded due to temperature rise, resulting in a decrease in rendering speed. You can check the GPU frequency information by `nvidia-smi -q -d CLOCK`.

## requests request error
```
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
```

Reference: https://stackoverflow.com/questions/70379603/python-script-is-failing-with-connection-aborted-connectionreseterror104

Solution: Network problem, you should know what to do.

## Font information error
```
Glyph 0x... not found, selecting one more font for (Microsoft YaHei, 400, 0)
```
Reference：https://github.com/timerring/bilive/issues/35

Solution: Usually ffmpeg cannot render expressions, so many expressions will report errors, I have filtered out 99% of the expressions through a general regular expression, of course, there may be other strange expressions and characters, if the error is ignored, ffmpeg will render a square, which does not affect the effect.

## Why are the rendered danmaku and subtitles a square?

This is a font missing problem, often appearing in manual deployment, I default use Microsoft YaHei font, there is msyh.ttf in the assets directory of the project, install it. The docker version should not have this problem, because it has completed this process in the dockerfile. Of course, if you want to use other fonts, you can also specify the corresponding font in the DanmakuFactory instruction during conversion.

## Why did you change back to the queue rendering method?

Due to the usually 10 ~ 15x rendering speed of danmaku under nvidia acceleration, and the speed of whisper executing speech recognition is 5x, so the previous way of creating danmaku rendering by whisper is completely feasible, but for live broadcasts with a large number of danmaku (20 minutes fragment produces 15400+ danmaku), the rendering speed will drop to 2 ~ 4x, when the new whisper processed fragment is rendered, the rendering speed will further decrease, and the number of accumulated parallel danmaku rendering processes will exceed 3, which will cause failure due to the limit of the number of concurrent encoding of the graphics card, in addition, there is a risk of out of memory. Therefore, in order to ensure the quality of rendering and the stability of the program, I originally changed back to the queue rendering method to process danmaku rendering.

## WSL running error ERROR: [Errno -2] Name or service not known

The problem of host name resolution, wsl usually has more network problems. From [issue 159](https://github.com/timerring/bilive/issues/159)

Solution: There are two main ideas:
1. Check the network content: https://unix.stackexchange.com/questions/589683/wsl-dns-not-working-when-connected-to-vpn
2. Don't start with record.sh, directly execute blrec in the command line terminal, then browse to `http://localhost:2233` (default), according to https://blog.csdn.net/Yiang0/article/details/127780263, the local Windows can directly access WSL2 through localhost, check if there is a normal running process.

## No slice is produced during recording

> First check if `AUTO_SLICE` is `True`, if it is `False`, no slice processing will be performed.

By default, if the video file size is less than 200 MB, no slice processing will be performed, the purpose of this is mainly to prevent some fragmented fragments from being sliced and uploaded, because for a host with a poor network or often disconnected, a live broadcast may produce dozens of fragments, if every two minutes or three minutes of connection is sliced again, the redundant content is not good for the audience, so I set a threshold of 200 MB to ensure that only long enough fragments will be sliced.

Solution: Modify the `MIN_VIDEO_SIZE` value in `src/config` to the limit you need, then re-execute `./scan.sh` again.

## RuntimeError: CUDA error: no kernel image is available for execution on the device

The log shows that the nvidia gpu driver and cuda version of your ubuntu may not match, and the cuda core may not be correctly called.

Solution: Refer to [this article](https://zhuanlan.zhihu.com/p/466793485).