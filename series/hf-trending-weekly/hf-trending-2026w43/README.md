# Hugging Face 本周热榜 Top 5 · 2026 第 43 周（10 月 24 日，周六版）

成片：`hf_trending_top5_w43_sat.mp4`（1920×1080 · 30fps · 约 5:53）+ `hf_trending_top5_w43_sat.srt`
封面：`cover.png`（1920×1080）/ `cover_4x3.png`（1440×1080）/ `cover_3x4.png`（1080×1440）
简介：`description.txt`

## 榜单（合并重复项后）
数据：`https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true`，抓取于 2026-10-24 18:15:25（Asia/Shanghai），原始数据见 `raw/trending_models.json`。

| # | 模型 | 类型 | 合并进来的条目（原榜位置） |
|---|---|---|---|
| 1 | deepseek-ai/DeepSeek-V4.1-Flash-1017 | 多模态 LLM | dealignai/…-UNCENSORED-FP8（#12，第三方去对齐微调+FP8）、unsloth/…-GGUF（#34） |
| 2 | RecursiveSI/flint | 稀疏 MoE 编程模型 | unsloth/flint-GGUF（#21） |
| 3 | black-forest-labs/flux-3-image-klein | 文生图/编辑 | 官方 flux-3-image-klein-comfy（#3，排名比原仓库更靠前；片头计数用的是 comfy 仓库数据，画面有注明） |
| 4 | OpenMOSS-Team/MOSS-Image-SFT | 文生图 | OpenMOSS-Team/MOSS-Image-Base（#8）、Comfy-Org/MOSS-Image（#11） |
| 5 | Lightricks/LTX-2.5 | 音视频联合生成 | — |

合并后顺延的下一名：XHToken/Spark-X2.6-4B（#6）、fishaudio/drama-3（#7）。

## 自报 / 第三方 / 社区观点（画面中均已标注）
- 厂商自报：DeepSeek 模型卡基准与 KV 字节数；Flint 基准与速度（Recursive 官方博客/模型卡）；FLUX 3 Klein 的 +91 Elo 为 BFL 内部评测，显存数字为官方；MOSS-Image 全部评测来自其论文（arXiv:2610.23374）；LTX 速度为厂商数字。
- 第三方：Artificial Analysis（DeepSeek 智能指数/速度/价格；LTX 视频竞技场，LTX-2.5 条目为 LTX API 的 Fast/Pro 两档）；Design Arena（FLUX 3 Klein）。Flint、MOSS-Image 暂无第三方榜单收录。
- 社区：Hacker News 讨论为概括转述，非引用。

## 实测（均为在线 Space 匿名调用，未在本机运行任何仓库代码）
| 文件 | 来源 |
|---|---|
| demo/flux_sample.png | 官方 Space black-forest-labs/flux-3-image-klein（蒸馏版 16 步，seed 7，提示扩写开启）—沿用参考版 hf-trending-2026w43 的实测素材 |
| demo/moss_sample.png | 官方 Space OpenMOSS-Team/MOSS-Image（Base，1024²，50 步，CFG 3，seed 20261022）—沿用参考版 hf-trending-2026w43 的实测素材 |
| demo/flint_sample.json | 社区 Space mrfakename/flint（非官方）；54.4 tok/s 为共享 GPU 速度，不代表本地。返回的 Python 代码在本机做了纯文本检查+小测试：列表输入结果正确，但会原地修改输入，元组输入报 TypeError |
| demo/ltx_sample.mp4 | 官方 Space Lightricks/LTX-2.5，输入为上面的 flux_sample.png（768²，73 帧，3 秒，seed 24，扩散解码器+提示增强）。成片里静音循环叠加播放（原片音轨极弱，约 −46.6 dB） |

## 素材来源与许可
| 素材 | 来源 / 许可 |
|---|---|
| ds_arch / ds_kvcache | DeepSeek-V4.1-Flash 技术报告 Fig.3 / Fig.1b（模型仓库内 PDF，MIT） |
| flint_benchmarks_nvfp4 | RecursiveSI/flint 模型卡图片（Apache-2.0） |
| flux_teaser / ui_flux | flux-3-image-klein 模型卡图片（FLUX Kommunity License）/ 官方 Space 页面截图 |
| moss_arch / moss_teaser / moss_layout | MOSS-Image 技术报告 Fig.2（arXiv:2610.23374）/ 模型卡图片（Apache-2.0） |
| ltx_arch / ltx_attn | LTX-2 论文 Fig.1 与注意力可视化（arXiv:2601.03233 HTML 版）；LTX-2.5 仓库为 gated，模型卡主图未下载 |
| 头像 av_* | 各组织 HF 头像（Flint 白色 logo 合成到深色底） |
| 字体 | Noto Sans CJK（SIL OFL） |
| 配音 | edge-tts zh-CN-XiaoxiaoNeural |
评测/截图均为说明性引用，画面内注明出处。

## 安全
只读调研：未执行任何仓库代码、未加载任何 pickle 权重、未下载模型权重；只下载了模型卡 README 与图片。Gated 仓库（LTX-2.5）仅用 `hf download … README.md` 读取模型卡，未申请访问。

## 流水线
`build_data.py → data.json` → `script.py`（旁白）→ `tts.py`（edge-tts，+25%，→ timing.json / audio/）→ `scenes.py` + `render.sh`（Manim 1080p30，逐场景顺序渲染）→ `sheet.py`（逐场景抽帧检查）→ `assemble.py`（拼接、P5s 叠加 LTX 视频、60px ASS 字幕烧录、SRT、loudnorm、x264 crf20）→ `checkcut.py`（成片抽帧到 build_chk_final/）。
封面：`make_covers.py .`（读取 cover.json + data.json，基于 github-trending-2026w43-fri 版本，16:9 卡片增加了一行中文描述）。

Python 环境：任务指定的 `/workspace/sky-blue-demo/.venv` 不存在，`.venv` 软链到 `/workspace/github-trending-2026w43-fri/.venv`（manim 0.22.0、edge-tts、Pillow）。gradio_client 在 `.gvenv`。
