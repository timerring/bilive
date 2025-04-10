# whisper model parameters

This project uses the [OpenAI's open source whisper model](https://github.com/openai/whisper) for Automatic Speech Recognition (ASR) tasks.

## Model information
The basic parameters and links of the model are as follows, note that the GPU VRAM must be greater than the required VRAM:

> [!TIP]
> If you pursue recognition accuracy, it is recommended to use models with parameters `small` or above.

|  Size  | Parameters | Multilingual model | Required VRAM |
|:------:|:----------:|:------------------:|:-------------:|
|  tiny  |    39 M    |       [`tiny`](https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt)       |     ~1 GB     |
|  base  |    74 M    |       [`base`](https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt)       |     ~1 GB     |
| small  |   244 M    |      [`small`](https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt)       |     ~2 GB     |
| medium |   769 M    |      [`medium`](https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt)      |     ~5 GB     |
| large  |   1550 M   |      [`large`](https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt)       |    ~10 GB     |


## Calculate VRAM requirements

Use Nvidia GPU to accelerate the rendering process of ffmpeg, each task requires approximately 180 MB of VRAM. The VRAM required for the `whisper` model is as shown in the table above.

Therefore, you can roughly calculate the required VRAM.

For example, using the `small` model:
+ If using the `pipeline` mode, since it runs in parallel, at least 180 + 2620 = 2800 MB of VRAM is required.
+ If using the `append` or `merge` mode, at least 2620 MB of VRAM is required.

> [!WARNING]
> Please ensure that the GPU VRAM is greater than the calculated result, otherwise the VRAM will be exhausted, resulting in `RuntimeError: CUDA out of memory.`

## Change model method

1. Please set the `Inference_Model` parameter in the `bilive.toml` file to the corresponding model size name, such as `tiny`, `base`, `small`, `medium`, `large`.
2. Download the corresponding model file and place it in the `src/subtitle/models` folder.
3. Re-run the `./scan.sh` script.
