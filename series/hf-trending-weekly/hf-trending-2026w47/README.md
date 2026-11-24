# Hugging Face 本周热榜 Top 5 · 2026 第 47 周（11 月 21 日）

成片：`hf_trending_top5_w47.mp4`（1920×1080，30fps，335.2 秒 ≈ 5:35，烧录 60px 字幕，整片约 -16 LUFS）+ `hf_trending_top5_w47.srt`
封面：`cover.png`（1920×1080）/ `cover_4x3.png`（1440×1080）/ `cover_3x4.png`（1080×1440），缩略预览在 build_covers/；视频描述：`description.txt`
榜单快照：`https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true`，2026-11-21 17:54:32（北京时间，UTC+8）= 01:54:32 PST（raw/snapshot_time.txt、raw/trending_models.json）。

## 榜单（合并重复项后）
| # | 模型 | 类型 | 点赞 / 30 天下载 / 热度分 |
|---|---|---|---|
| 1 | [thinkingmachines/Inkling-2-Mini](https://huggingface.co/thinkingmachines/Inkling-2-Mini) | image-text-to-text（循环 MoE 多模态，Apache-2.0） | 1,101 / 136 / 844 |
| 2 | [higurashi-ai/Haru-4B](https://huggingface.co/higurashi-ai/Haru-4B) | audio-to-audio（全双工语音对话基座，Apache-2.0） | 5,711 / 7,323 / 622（热榜显示 5,711，公开点赞列表只有 801 条） |
| 3 | [harness-hub/Qwen3.8-27B-pi-adapted](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) | Qwen3.8-27B 的 LoRA 适配器（为 pi 编程代理，Apache-2.0） | 835 / 1,874 / 600 |
| 4 | [Sentinel7/h3](https://huggingface.co/Sentinel7/h3) | 社区 LoRA 合集（面向 MiniMax H3 视频，无模型卡） | 563 / 0 / 479 |
| 5 | [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | image-to-video / 音视频联合生成（22B DiT，LTX-2.x 社区许可） | 12,843 / 3,000,544 / 361 |

合并规则：同一模型的量化 / GGUF / 去审查 / ComfyUI 封装 / Base 等衍生仓库并入原模型，按组内最高名次排序。本周只有一项合并进入相关组，且不改变前五名次：
- **thinkingmachines/Inkling-2-Mini（#1）← unsloth/Inkling-2-Mini-GGUF（#7）**。画面数字用的是官方原仓库。
- **没有合并**：thinkingmachines/Inkling-2-Small（#27）是同一系列的更大尺寸；harness-hub/Qwen3.8-27B-pi-adapted（#3）是面向 pi 编程代理的第三方强化学习 LoRA，虽同底座但不并入 Qwen/Qwen3.8-27B（判断方式同上周的 Arete-27B）；harness-hub/Qwen3.8-27B-opencode-adapted（#23）同理；Sentinel7/h3（#4）是 MiniMax H3 视频模型的社区 LoRA 合集，不是官方发布，也不并入 MiniMax-H3 或 MiniMax-H3-Image；tencent/Hy4-flash（#6）与 tencent/Hy4（#24）是不同结构版本（Flash 引入混合注意力、LatentMoE、Engram），不互相合并；AngelSlim/Hy4-flash-GGUF（#31）并入 Hy4-flash，不影响前五。
- Qwen/Qwen3.8-27B 官方仓库本周原榜 #11，其 GGUF / Heretic / abliterated 衍生仓库（#20、#22、#34）已并入，组内最高名次仍是 #11，未进入前五。DaisyRose-27B（#13）、clairic（#21）是第三方微调，不并入。
- 顺延的下一名：tencent/Hy4-flash（#6）、inworld/voice-isolator（#8）、meituan-longcat/LongCat-Video-Avatar-1.6（#9）、n4ze3m/tiny-voca（#10）。
- 上周前五的去向：Jackrong 蒸馏及其 Heretic 衍生仓库、Arete-27B 本周不在 Top 40；MiniMax-H3-Image 落到原榜 #14（点赞 1,067→1,693，近 30 天下载 437,039→876,986）；Qwen3.8-27B 官方落到 #11（点赞 19,926→20,749，近 30 天下载 6,757,964→6,298,190）。

## 自报 / 第三方 / 社区观点（画面中均已标注）
- **官方自报**：Inkling 2 Mini 模型卡评测表（对照含 Gemma 4 31B、Muse Glimmer、Qwen3.8-27B、Nemotron 3.5 Super VL；表中 AA Index 与第三方页面一致，其余分项为作者评测设置）。Haru-4B 技术博客：超过 4,000 万小时真实语音、约 1,300 万小时分离后的全双工数据、M1 Max int8 端到端约 65 ms（不含最多 133 ms 的帧填充）；256×B200 训练约 8 天。pi-adapted 模型卡：在 pi 框架下 SWE-bench Pro（hard 51）与 Terminal-Bench 2.1 的配对结果；作者写明不可与 Qwen3.8-27B 模型卡数字直接比较，并修正过两轮早先公布的分数（输出截断、评测通道故障）。LTX-2.5 的架构与许可沿用官方模型卡 / LTX-2 论文。
- **第三方**：Artificial Analysis（2026-11-21 查询）。Inkling 2 Mini 智能指数 20（页面 JSON 20.13），同尺寸可比中位数 10；每任务约 9.0 分钟（中位数 9.2）、约 $0.59 / 任务，输入 $0.15 / 1M、输出 $0.50 / 1M；评估该指数时生成 161M token（中位数 85.7M），偏长。AA 视频竞技场：文生视频 LTX-2.5 Fast 第 29（Elo 937.72，上周第 28 / Elo 942），图生视频 Fast 第 33（Elo 912，上周第 32 / Elo 912）；文生视频榜首仍是 Wan 3.0（Elo 1175.5）。全榜名次 = 页面 JSON 的 values.rank + 1；AA 测的是 LTX 的 API Fast / Pro 版本。Haru-4B 与 pi-adapted 在 AA 未做对等收录。
- **我们自己的复核（点赞账号注册时间）**：拉取公开点赞列表 `/api/models/<repo>/likers`，用账号 `_id`（ObjectId）前 8 位十六进制换算账号创建时间（UTC），2026-11-21 抓取。这只能说明账号的注册时间，**不能证明刷量，也看不出是谁在操作**。
  - Inkling 2 Mini：列表 1,036 条（热榜 1,101），8 月及以后占 23.9%，11 月 19.1%。与对照接近（Qwen3.8-27B 24.4%，Hy4-flash 30.2%）。
  - Haru-4B：**热榜 / 模型页显示 5,711 点赞（页面写作 5.71k），公开列表即使用登录 token 也只有 801 条，且无分页续页。** 列出的 801 条里，8 月及以后只占 11.4%，注册时间并不异常。这是点赞计数与列表的不一致，不能据此推断列表内账号被刷。
  - pi-adapted：列表 798 条（热榜 835），8 月及以后占 29.1%，没有明显的新号扎堆。
  - Sentinel7/h3：列表 564 条（热榜 563，抓取时刻略有差别），8 月及以后占 24.3%，与对照接近。异常主要是下载为 0 却有五百多点赞，且没有模型卡。
  - LTX-2.5：列表 12,843 条，与热榜完全一致。8 月及以后占 59.8%（第 45 周同口径 57.7%，第 46 周 58.5%），仍明显高于对照的两到三成。11 月注册 1,674 条（13.0%；上周 1,022 / 8.6%）。点赞 11,836→12,843，近 30 天下载 2,777,667→3,000,544。社区讨论 #97 仍开放。
- **社区观点（都是概述，不是原话）**：Inkling 讨论区有人反馈重复说 “actually let me act”，也有地区不可用和本地部署讨论。Haru 讨论区关心 12GB 显存和是否会出指令微调版。pi-adapted 有人问离开 pi 框架后真实使用有没有变好。Sentinel7/h3 讨论区有多条内容投诉和补模型卡请求，不构成已裁定结论。
- **数据不一致**：Haru 热榜点赞 5,711、点赞列表 801（即使用登录请求也如此）；Inkling 热榜 1,101、列表 1,036；pi-adapted 热榜 835、列表 798；Sentinel7/h3 热榜 563、列表 564。AA 智能指数页面写 20，JSON 为 20.13。

## 实测（本周没有调用在线 Space）
Inkling 有第三方小 Space，Haru 有 hugging-apps/haru-4b 等语音演示，LTX 有官方视频 Space——语音/视频演示都不便宜，本周没有匿名调用。画面里的数字和图来自模型卡、官方博客和 Artificial Analysis 页面。没有在 Space 调用里使用 HF token，也没有在本机加载权重。Sentinel7/h3 的成片不展示任何样例。

## 素材来源与许可
| 素材 | 来源 / 许可 |
|---|---|
| 头像 av_* | 各组织 / 作者的 HF 头像（Sentinel7 是用户头像） |
| 其余图表 | 用 Manim 按模型卡、技术博客、AA 页面和我们抓取的点赞列表、文件清单重绘，画面里都注明了出处 |
| 字体 | Noto Sans CJK（SIL OFL） |
| 配音 | MiniMax T2A v2（api.minimaxi.com），speech-2.8-hd，音色 male-qn-jingying（精英青年），语速 1.1 |

下载了但封面或成片未全部用到的：Inkling 模型卡 logo、Haru 官方 architecture.svg、pi-adapted 的 banner / card-pi / trajectory 官方图。LTX-2.5 的模型卡 README 与 hero 图对未登录或未授权请求返回 401 / Access denied，用已登录的 `hf` CLI 拉取了 README，hero 图因仓库需审批未能下载，成片改用图表。

## 安全
只读调研：没有执行任何仓库代码，没有加载任何 pickle 权重，也没有下载模型权重；只拉取了 API JSON、模型卡 README、论文信息、公开图片、公开点赞列表和仓库文件名清单。MiniMax API key 只在运行时从 `/home/box/.config/minimax/api_key` 读取，没有打印，也没有写进脚本、日志或任何输出。Sentinel7/h3 含成人向 LoRA，成片只做结构与热度说明，不展示样例。

## 旁白
`tts.py` 按场景合成，每段前留 0.25 秒、后留 0.65 秒；用 MiniMax 的词级时间戳（subtitle_type=word）生成画面时间点（timing.json）和字幕（只在句读标点处断行）。多音字和英文名用 `pronunciation_dict` 校正（列表在 minimax_client.py 的 TONES 和 build/tts_summary.json），例如 重新、执行、打折扣、占了、偏长、对不上、还得、还是、占比，以及 Inkling → Ink ling、Haru → 哈鲁、higurashi → Higurashi、Sentinel7 → Sentinel seven、pi 这个编程代理 → pai。主合成一次到位，旁白总长 335.2 秒 ≈ 5:35，计费约 3,586 字符。没有用到 edge-tts 兜底。

## 流水线
`build_data.py → data.json` → `script.py`（旁白）→ `tts.py`（MiniMax，生成 timing.json 和 audio/）→ `prep_assets.py` → `scenes.py` + `render.sh`（Manim 1080p30，按场景顺序渲染）→ `sheet.py`（每个场景抽帧检查，结果在 build_chk/）→ `assemble.py`（ffmpeg 拼接、烧录 60px ASS 字幕、生成 SRT、loudnorm -16 LUFS、x264 crf20、faststart）→ `checkcut.py`（成片抽帧，结果在 build_chk_final/）。
封面：`make_covers.py .`（读取 cover.json 和 data.json）。
Python 环境：`.venv` 软链到 `/workspace/github-trending-2026w45/.venv`（manim 0.22.1、Pillow、av）；`.gvenv`（gradio_client）软链到 `/workspace/hf-trending-2026w43-sat/.gvenv`；`.rvenv` 软链到 w45 `.rvenv`（本周未做点渲染）。
