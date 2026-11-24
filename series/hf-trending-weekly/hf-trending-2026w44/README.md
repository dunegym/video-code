# Hugging Face 本周热榜 Top 5 · 2026 第 44 周（10 月 31 日）

成片：`hf_trending_top5_w44.mp4`（1920×1080，30fps，356.9 秒 ≈ 5:57，烧录 60px 字幕）+ `hf_trending_top5_w44.srt`
封面：`cover.png`（1920×1080）/ `cover_4x3.png`（1440×1080）/ `cover_3x4.png`（1080×1440）；视频描述：`description.txt`
榜单快照：`https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true`，2026-10-31 03:12:58 PDT（raw/snapshot_time.txt 记录的是盒子本地时间 18:12:58 CST，即 UTC+8）。

## 榜单（合并重复项后）
| # | 模型 | 类型 | 点赞 / 30 天下载 / 热度分 | 合并进来的仓库 |
|---|---|---|---|---|
| 1 | [Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | text-generation（33.1B 稠密，Apache-2.0） | 814 / 13,832 / 795 | — |
| 2 | [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | image-text-to-text（763B MoE，MIT） | 4,047 / 156,373 / 786 | ISTA-DASLab/…-GSQ-RCO-GGUF（原榜 #9）、orcarouter/…-abliterated-GGUF（#15，gated，未读取内容） |
| 3 | [LiquidAI/LFM3-1.7B](https://huggingface.co/LiquidAI/LFM3-1.7B) | text-generation（1.73B，LFM Open License v1.0） | 591 / 32,933 / 568 | LiquidAI/LFM3-1.7B-GGUF（#29）、AtomicChat/LFM3-1.7B-Uncensored-GGUF（#32） |
| 4 | [nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B) | automatic-speech-recognition（约 34B / 4.3B 激活，OpenMDW-1.1） | 514 / 24,357 / 483 | — |
| 5 | [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | image-text-to-text（约 1T / 49B 激活，Mistral Ecosystem Open-Weight License） | 1,367 / 2,945 / 421 | — |

合并后顺延的下一名：baidu/Unlimited-OCR-2（原榜 #6）、Lightricks/LTX-2.5（#7），未进入 Top 5。
排名按 trendingScore；点赞/下载为抓取时数值（片头卡片里数字从上周值滚动到本周值）。下载数统计的是文件请求次数，分片多的 GGUF 仓库会偏高。

## 自报 / 第三方 / 社区观点（画面中均已标注）
- **官方自报**：Nanbeige 的智能体/JobBench/GPQA/AIME 分数；LFM3 的 iPhone 17 Pro 速度与内存、WebArena 等评测；Nemotron 的各项 WER、2,238× 实时速率、0.13 秒；Mistral 的 DSpark 1.9×、“token 少 47%”（Mistral 引用 AA 的说法）。
- **量化作者自测**：ISTA-DASLab 模型卡中 IQ1_M / IQ2_XXS / IQ2_XS 三项平均（AIME25、GPQA-D、LCB v6）与恢复率；模型卡中 Strata 引擎部分仍标注待补充。
- **第三方**：Artificial Analysis（2026-10-31 查询）——DeepSeek V4.1 Flash 1017 智能指数 v5 = 32、175 tok/s、单任务 $0.60；Mistral Large 4 = 26（第 9/22）、161.3 tok/s、单任务 $2.06。上周画面里 DeepSeek 的 45 是旧版指数，两者不可直接比较（画面已注明）。Nanbeige 与 LFM3 在 AA 未收录。Nanbeige 的 KV 缓存 111.7 GB / 4 bit 19.8 GB 为 the9.pro 第三方测算。
- **媒体/官方博客**：Nemotron “VoiceArena 第一 · David AI 说话人分离榜错误率最低”出自 NVIDIA 的 HF 博客，未独立核实；模型卡说明训练数据含 David AI 授权数据（相关评测集已排除）。另见 TechCrunch 10/28 报道。
- **数据不一致**：Nanbeige 模型卡的 JobBench 柱状图与表格有出入（如 Muse 图中 18.3、表中 16.6），视频统一采用表格数字。Mistral HF 博客里有几处数字与模型卡不一致，以模型卡为准。
- Nanbeige 团队归属（BOSS直聘 / 看准科技）：模型卡只给了 @kanzhun.com 联系邮箱，归属是根据邮箱域名和公开信息判断的。

## 实测（在线 Space 匿名调用，本机未运行任何仓库代码）
| 文件 | 说明 |
|---|---|
| demo/nemotron_test.wav | 用 edge-tts（Guy / Jenny）合成的 25.3 秒英文双人对话，故意加入 um / uh 和重复（mk_audio.py） |
| demo/nemotron_sample.json | Space `hugging-apps/nemotron-3-5-transcribe`（HF 的 hugging-apps 组织，**不是** NVIDIA 官方，ZeroGPU，每次约 4.5–5 秒）。逐字模式保留了口头禅和重复；清理模式全部去掉；说话人模式标对了 spk0/spk1/spk0；自定义指令“翻译成中文”也能输出 |
| demo/lfm3_sample.json | **失败**：ZeroGPU 报错 “requested GPU duration (450s) is larger than maximum allowed”（匿名额度），LFM3 没有实测画面 |
| — | Nanbeige 的 Space（apathy-exe）无法获取 Gradio 配置，已跳过；Mistral 官方 Space 是调用 Mistral API 的 docker 应用，不算模型实测，已跳过 |

## 素材来源与许可
| 素材 | 来源 / 许可 |
|---|---|
| nem_hero / nem_arch | NVIDIA-Nemotron-3.5-Transcribe-30B-A4B 模型卡图片（OpenMDW-1.1） |
| lfm3_post | LFM3-1.7B 模型卡 / Liquid AI 博客的后训练流程图（LFM Open License v1.0） |
| 头像 av_* / avatar_* | 各组织的 HF 头像 |
| 其余图表 | 用 Manim 按模型卡 / AA 数字重绘，画面内注明出处 |
| 字体 | Noto Sans CJK（SIL OFL） |
| 配音 | edge-tts zh-CN-XiaoxiaoNeural |
nb_bench.png、lfm3_pre.png 下载了但没有用在成片里。评测图和截图都是说明性引用。

## 安全
只读调研：没有执行任何仓库代码，没有加载任何 pickle 权重，也没有下载模型权重；只拉取了 API JSON、模型卡 README、config.json 和图片。orcarouter 的 gated 仓库只读取了 API 元数据。

## 流水线
`build_data.py → data.json` → `script.py`（旁白）→ `tts.py`（edge-tts，+25%，生成 timing.json 和 audio/）→ `scenes.py` + `render.sh`（Manim 1080p30，按场景顺序渲染）→ `sheet.py`（每个场景抽帧检查，结果在 build_chk/）→ `assemble.py`（拼接、烧录 60px ASS 字幕、生成 SRT、loudnorm、x264 crf20、faststart）→ `checkcut.py`（成片抽帧，结果在 build_chk_final/）。
封面：`make_covers.py .`（读取 cover.json 和 data.json；4:3 列表行的名称宽度改为按实际字体测量，避免长名称碰到星标）。
Python 环境：`.venv` 软链到 `/workspace/github-trending-2026w43-fri/.venv`（manim 0.22.0、edge-tts、Pillow），`.gvenv`（gradio_client）软链到 w43-sat。
