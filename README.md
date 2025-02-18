<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="BILIVE" />
  </picture>

*7 x 24 小时无人监守录制、渲染弹幕、识别字幕、自动切片、自动上传、兼容超低配机器，启动项目，人人都是录播员。*

[:page_facing_up: Documentation](https://timerring.github.io/bilive/) |
[:gear: Installation](#quick-start) |
[:thinking: Reporting Issues](https://github.com/timerring/bilive/issues/new/choose)

支持模型

  <img src="assets/openai.svg" alt="OpenAI whisper" width="60" height="60" />
  <img src="assets/zhipu-color.svg" alt="Zhipu GLM-4V-PLUS" width="60" height="60" />
  <img src="assets/gemini-brand-color.svg" alt="Google Gemini 1.5 Pro" width="60" height="60" />

</div>

##  1. Introduction

> 如果您觉得项目不错，欢迎 :star: 也欢迎 PR 合作，如果有任何疑问，欢迎提 issue 交流。

自动监听并录制B站直播和弹幕（含付费留言、礼物等），根据分辨率转换弹幕、语音识别字幕并渲染进视频，根据弹幕密度切分精彩片段并通过视频理解大模型生成有趣的标题，自动投稿视频和切片至B站，兼容无GPU版本，兼容超低配置服务器与主机。

## 2. Major features

- **速度快**：采用 `pipeline` 流水线处理视频，理想情况下录播与直播相差半小时以内，没下播就能上线录播，**目前已知 b 站录播最快版本**！
- **多房间**：同时录制多个直播间内容视频以及弹幕文件（包含普通弹幕，付费弹幕以及礼物上舰等信息）。
- **占用小**：自动删除本地已上传的视频，极致节省空间。
- **模版化**：无需复杂配置，开箱即用，( :tada: NEW)通过 b 站搜索建议接口自动抓取相关热门标签。
- **检测片段并合并**：对于网络问题或者直播连线导致的视频流分段，能够自动检测合并成为完整视频。
- **自动渲染弹幕**：自动转换xml为ass弹幕文件并且渲染到视频中形成**有弹幕版视频**并自动上传。
- **硬件要求极低**：无需GPU，只需最基础的单核CPU搭配最低的运存即可完成录制，弹幕渲染，上传等等全部过程，无最低配置要求，10年前的电脑或服务器依然可以使用！
- **( :tada: NEW)自动渲染字幕**(如需使用本功能，则需保证有 Nvidia 显卡)：采用 OpenAI 的开源模型 [`whisper`](https://github.com/openai/whisper)，自动识别视频内语音并转换为字幕渲染至视频中。
- **( :tada: NEW)自动切片上传**：根据弹幕密度计算寻找高能片段并切片，结合多模态视频理解大模型 [`GLM-4V-PLUS`](https://bigmodel.cn/dev/api/normal-model/glm-4) 自动生成有意思的切片标题及内容，并且自动上传。

项目架构流程如下：

```mermaid
graph TD
        User((用户))--record-->startRecord(启动录制)
        startRecord(启动录制)--保存视频和字幕文件-->videoFolder[(Video 文件夹)]

        User((用户))--scan-->startScan(启动扫描 Video 文件夹)
        videoFolder[(Video 文件夹)]<--间隔两分钟扫描一次-->startScan(启动扫描 Video 文件夹)
        startScan <--视频文件--> whisper[whisperASR模型]
        whisper[whisperASR模型] --生成字幕-->parameter[查询视频分辨率]
        subgraph 启动新进程
        parameter[查询分辨率] -->ifDanmaku{判断}
        ifDanmaku -->|有弹幕| DanmakuFactory[DanmakuFactory]
        ifDanmaku -->|无弹幕| ffmpeg1[ffmpeg]
        DanmakuFactory[DanmakuFactory] --根据分辨率转换弹幕--> ffmpeg1[ffmpeg]
        ffmpeg1[ffmpeg] --渲染弹幕及字幕 --> Video[视频文件]
        Video[视频文件] --计算弹幕密度并切片--> GLM[多模态视频理解模型]
        GLM[多模态视频理解模型] --生成切片信息--> slice[视频切片]
        end
        
        slice[视频切片] --> uploadQueue[(上传队列)]
        Video[视频文件] --> uploadQueue[(上传队列)]

        User((用户))--upload-->startUpload(启动视频上传进程)
        startUpload(启动视频上传进程) <--扫描队列并上传视频--> uploadQueue[(上传队列)]
```


## 3. 测试硬件
+ OS: Ubuntu 22.04.4 LTS

  >尽量使用 22.04+ 的版本，更早版本的 ubuntu 自带 gcc 版本无法更新至 DanmakuFactory 以及 biliup-rs 所需版本，若使用较早版本，请参考 [version `GLIBC_2.34‘ not found简单有效解决方法](https://blog.csdn.net/huazhang_001/article/details/128828999)。
+ CPU：2核 Intel(R) Xeon(R) Platinum 85
+ GPU：无
+ 内存：2G
+ 硬盘：40G
+ 带宽: 3Mbps
  > 个人经验：若想尽可能快地更新视频，主要取决于上传速度而非弹幕渲染速度，因此建议网络带宽越大越好。

## 4. Quick start

更详细的教程请参考文档 [bilive](https://timerring.github.io/bilive/)

> [!NOTE]
> 如果你是 windows 用户，请不要使用命令提示符（Command Prompt）或 Windows PowerShell，请使用 [PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4) 或 Linux 终端例如 WSL 或 **Git Bash**(推荐)。

### Mode
首先介绍本项目三种不同的处理模式：
1. `pipeline` 模式(默认): 目前最快的模式，需要 GPU 支持，最好在 `blrec` 设置片段为半小时以内，asr 识别和渲染并行执行，分 p 上传视频片段。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-17-33-15.png)
2. `append` 模式: 基本同上，但 asr 识别与渲染过程串行执行，比 pipeline 慢预计 25% 左右，对 GPU 显存要求较低，兼顾硬件性能与处理上传效率。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-19-07-12.png)
3. `merge` 模式: 等待所有录制完成，再进行识别渲染合并过程，上传均为完整版录播（非分 P 投稿），等待时间较长，效率较慢，适合需要上传完整录播的场景。
![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2024-12-11-19-08-58.png)

> [!IMPORTANT]
> 凡是用到 GPU 均需保证 GPU 显存大于运行程序所需 VRAM，具体计算 VRAM 方法可以参考[该部分](https://timerring.github.io/bilive/models.html#计算-vram-需求)。

### Installation(有 GPU 版本)

> 是否有 GPU 以 `nvidia-smi` 显示 nvidia GPU 驱动以及 `nvcc -V` 显示 `CUDA` 版本号为准。如果未配置显卡驱动或未安装 `CUDA`，即使有 GPU 也无法使用，而会使用 CPU 推理（不推荐，可根据自身硬件条件判断是否尝试 CPU 推理）。

> [!TIP]
> 如果你是 windows 用户，请不要使用命令提示符（Command Prompt）或 Windows PowerShell，请使用 [PowerShell](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4) 或 WSL 或 **Git Bash**(推荐)。
> 
> **注意：PowerShell 和 Windows PowerShell 是[不同的应用程序](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.4&viewFallbackFrom=powershell-7.3)。**

#### 1. 安装依赖(推荐先 `conda` 创建虚拟环境)

```
cd bilive
pip install -r requirements.txt
```

此外请根据各自的系统类型安装对应的 [`ffmpeg`](https://www.ffmpeg.org/download.html)，例如 [ubuntu 安装 ffmpeg](https://gcore.com/learning/how-to-install-ffmpeg-on-ubuntu/)。

[常见问题收集](https://timerring.github.io/bilive/install-questions.html)

#### 2. 设置环境变量用于保存项目根目录

```
./setPath.sh && source ~/.bashrc
```

#### 3. 配置 whisper 模型及 GLM-4V-PLUS 模型

##### 3.1 whisper 模型
项目默认采用 [`small`](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt) 模型，请点击下载所需文件，并放置在 `src/subtitle/models` 文件夹中。

> [!TIP]
> 使用该参数模型至少需要保证有显存大于 2.7GB 的 GPU，否则请使用其他参数量的模型。
> + 更多模型请参考 [whisper 参数模型](https://timerring.github.io/bilive/models.html) 部分。
> + 更换模型方法请参考 [更换模型方法](https://timerring.github.io/bilive/models.html#更换模型方法) 部分。

##### 3.2 GLM-4V-PLUS 模型

> 此功能默认关闭，如果需要打开请将 `src/config.py` 文件中的 `AUTO_SLICE` 参数设置为 `True`

在配置文件 `src/config.py` 中，`SLICE_DURATION` 以秒为单位设置切片时长（不建议超过 1 分钟），在项目的自动切片功能需要使用到智谱的 [`GLM-4V-PLUS`](https://bigmodel.cn/dev/api/normal-model/glm-4) 模型，请自行[注册账号](https://www.bigmodel.cn/invite?icode=shBtZUfNE6FfdMH1R6NybGczbXFgPRGIalpycrEwJ28%3D)并申请 API Key，填写到 `src/config.py` 文件中对应的 `Your_API_KEY` 中。

#### 4. biliup & bilitool 登录

首先按照 [biliup-rs](https://github.com/biliup/biliup-rs) 登录b站，登录脚本在 `src/upload/biliup` ，登录产生的`cookies.json`保留在该文件夹下即可。

然后同样通过 `bilitool login` 扫码登录（biliup 的 list 对应 api 已经失效，因此我写了 [bilitool](https://github.com/timerring/bilitool) 工具作为替换）。

[常见问题收集](https://timerring.github.io/bilive/biliup.html)

#### 5. 启动自动录制

```bash
./record.sh
```

[常见问题收集](https://timerring.github.io/bilive/record.html)

#### 6. 启动自动上传

请先确保你已经完成`步骤 3`，正确下载并放置了模型文件。

##### 6.1 启动扫描渲染进程

输入以下指令即可检测已录制的视频并且自动合并分段，自动进行弹幕转换，字幕识别与渲染的过程：

```bash
./scan.sh
```

[常见问题收集](https://timerring.github.io/bilive/scan.html)

##### 6.2 启动自动上传进程

```bash
./upload.sh
```

[常见问题收集](https://timerring.github.io/bilive/upload.html)


#### 7. 查看执行日志

相应的执行日志请在 `logs` 文件夹中查看，如果有问题欢迎在 [`issue`](https://github.com/timerring/bilive/issues/new/choose) 中提出。
```
logs # 日志文件夹
├── blrecLog # blrec 录制日志
│   └── ...
├── burningLog # 弹幕渲染日志
│   └── ...
├── mergeLog # 片段合并日志
│   └── ...
├── scanLog # scan运行日志
│   └── ...
├── uploadLog # 视频上传日志
│   └── ...
└── blrec.log # record.sh 运行日志
```

### Installation(无 GPU 版本)
无 GPU 版本过程基本同上，可以跳过步骤 3 配置 whisper 的部分，需要注意在执行步骤 5 **之前**完成以下设置将确保完全用 CPU 渲染视频弹幕。

1. 请将 `src/config.py` 文件中的 `GPU_EXIST` 参数设置为 `False`。（若置为 `True` 但又没有 GPU 或者 Nvidia 驱动找不到，则会使用 CPU 推理，非常消耗 CPU 计算资源，不推荐，可自行根据硬件条件进行尝试。）
2. 将 `MODEL_TYPE` 调整为 `merge` 或者 `append`。

> [!TIP]
> 上传默认参数如下，[]中内容全部自动替换。也可在 src/upload/extract_video_info.py 中自定义相关配置：
> + 默认标题是"【弹幕+字幕】[XXX]直播回放-[日期]-[直播间标题]"。
> + 默认描述是"【弹幕+字幕】[XXX]直播，直播间地址：[https://live.bilibili.com/XXX] 内容仅供娱乐，直播中主播的言论、观点和行为均由主播本人负责，不代表录播员的观点或立场。"
> + 默认标签是根据主播名字自动在 b 站搜索推荐中抓取的[热搜词]，详见[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/search/suggest.md)。

### Docker 运行

也可以直接拉取 docker 镜像运行，默认 latest。默认启动 upload 进程，record 以及 scan 可以在配置后手动启动，相关配置流程从 3.2 开始即可，此版本 docker 镜像无 GPU 配置。

> [!IMPORTANT]
> 如果因为网络原因无法pull，考虑使用镜像地址，例如 https://dockerpull.cn/ ，将镜像改为 `dockerpull.cn/timerring/bilive` 即可。
> 
> 如果不需要使用可视化页面可以忽略以下提醒：
> - 不推荐在有公网 ip 的服务器上直接暴露 22333 端口访问管理页面，如果使用请自行限制端口入站 ip 规则或者采用 nginx 等反向代理配置密钥限制他人访问。

```bash
sudo docker run \
    -itd \
    --name bilive_docker \
    -p 22333:2233 \
    timerring/bilive:0.2.9
```

## 特别感谢

- [biliup/biliup-rs](https://github.com/biliup/biliup-rs)
- [hihkm/DanmakuFactory](https://github.com/hihkm/DanmakuFactory)
- [acgnhiki/blrec](https://github.com/acgnhiki/blrec)
- [OpenAI/whisper](https://github.com/OpenAI/whisper)