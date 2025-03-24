
# Quick start
## Mode
首先介绍本项目三种不同的处理模式：
1. `pipeline` 模式(默认): 目前最快的模式，需要 GPU 支持，最好在 `blrec` 设置片段为半小时以内，asr 识别和渲染并行执行，分 p 上传视频片段。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-17-33-15.png)
2. `append` 模式: 基本同上，但 asr 识别与渲染过程串行执行，比 pipeline 慢预计 25% 左右，对 GPU 显存要求较低，兼顾硬件性能与处理上传效率。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-19-07-12.png)
3. `merge` 模式: 等待所有录制完成，再进行识别渲染合并过程，上传均为完整版录播（非分 P 投稿），等待时间较长，效率较慢，适合需要上传完整录播的场景。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-19-08-58.png)

> [!IMPORTANT]
> 凡是用到 GPU 均需保证 GPU 显存大于运行程序所需 VRAM，具体计算 VRAM 方法可以参考[该部分](./models.md#计算-vram-需求)。

## Installation(有 GPU 版本)

> 是否有 GPU 以 `nvidia-smi` 显示 nvidia GPU 驱动以及 `nvcc -V` 显示 `CUDA` 版本号为准。如果未配置显卡驱动或未安装 `CUDA`，即使有 GPU 也无法使用，而会使用 CPU 推理（不推荐，可根据自身硬件条件判断是否尝试 CPU 推理）。

> [!NOTE]
> 如果你是 windows 用户，请使用 WSL 运行本项目。

### 1. 安装依赖(推荐先 `conda` 创建虚拟环境)

```
cd bilive
pip install -r requirements.txt
```

此外请根据各自的系统类型安装对应的 [`ffmpeg`](https://www.ffmpeg.org/download.html)，例如 [ubuntu 安装 ffmpeg](https://gcore.com/learning/how-to-install-ffmpeg-on-ubuntu/)。

[常见问题收集](./install-questions)

### 2. 设置环境变量用于保存项目根目录

```
./setPath.sh && source ~/.bashrc
```

### 3. 配置 whisper 模型

项目默认采用 [`small`](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt) 模型，请点击下载所需文件，并放置在 `src/subtitle/models` 文件夹中。

> [!TIP]
> 使用该参数模型至少需要保证有显存大于 2.7GB 的 GPU，否则请使用其他参数量的模型。
> + 更多模型请参考 [whisper 参数模型](./models) 部分。
> + 更换模型方法请参考 [更换模型方法](./models.md#更换模型方法) 部分。


### 4. biliup-rs 登录

首先按照 [biliup-rs](https://github.com/biliup/biliup-rs) 登录b站，登录脚本在 `src/utils/biliup` ，登录产生的`cookies.json`保留在该文件夹下即可。

然后同样通过 `bilitool login` 扫码登录（biliup 的 list 对应 api 已经失效，因此我写了 [`bilitool`](https://github.com/timerring/bilitool) 工具作为替换）。

[常见问题收集](./biliup)

### 5. 启动自动录制

```bash
./record.sh
```

[常见问题收集](./record)

### 6. 启动自动上传

请先确保你已经完成`步骤 3`，正确下载并放置了模型文件。

#### 6.1 启动扫描渲染进程

输入以下指令即可检测已录制的视频并且自动合并分段，自动进行弹幕转换，字幕识别与渲染的过程：

```bash
./scan.sh
```

[常见问题收集](./scan)

#### 6.2 启动自动上传进程

```bash
./upload.sh
```

[常见问题收集](./upload)


### 7. 查看执行日志

相应的执行日志请在 `logs` 文件夹中查看，如果有问题欢迎在 [`issue`](https://github.com/timerring/bilive/issues/new/choose) 中提出。
```
logs # 日志文件夹
├── blrec # blrec 录制日志
│   └── ...
├── scan # scan 处理日志
│   └── ...
├── upload # upload 上传日志
│   └── ...
└── runtime # 每次执行的日志
    └── ...
```


## Installation(无 GPU 版本)
无 GPU 版本过程基本同上，可以跳过步骤 3，需要注意在执行步骤 5 **之前**完成以下设置将确保完全用 CPU 渲染视频弹幕。

1. 请将 `src/config.py` 文件中的 `GPU_EXIST` 参数设置为 `False`。（若不置为 `False` 且则会使用 CPU 推理，不推荐，可自行根据硬件条件进行尝试。）
2. 将 `MODEL_TYPE` 调整为 `merge` 或者 `append`。

## Docker 运行

也可以直接拉取 docker 镜像运行，默认 latest。守护进程是 upload，而 record 以及 scan 需要在配置后手动启动，相关配置以及启动流程从 3.2 开始即可，此版本 docker 镜像无 GPU 配置。

> [!IMPORTANT]
> 如果不需要使用可视化页面可以忽略以下提醒：
> - 不推荐在有公网 ip 的服务器上直接暴露 22333 端口访问管理页面，如果使用请自行限制端口入站 ip 规则或者采用 nginx 等反向代理配置密钥限制他人访问。
> - 管理页面主要针对 record 模块，只有手动运行 record 后(步骤5)才能访问到管理页面。

### Docker
```bash
sudo docker run \
    -itd \
    --name bilive_docker \
    -p 22333:2233 \
    timerring/bilive:0.2.10
```

### Docker Compose

#### 使用镜像

默认 CPU latest version，如需使用 GPU 版本，请将 `image: ghcr.io/timerring/bilive:latest` 修改为 `image: ghcr.io/timerring/bilive-gpu:latest`。
```bash
docker compose up -d
```

#### 自行构建

相关配置已经写好，请自行将 `compose.yml` 3-6 行替换为：

```yaml
    build:
        context: .
        dockerfile: Dockerfile # Dockerfile-GPU
    # image: ghcr.io/timerring/bilive:latest # ghcr.io/timerring/bilive-gpu:latest
```

然后执行以下命令：

```bash
docker build
docker compose up -d
```