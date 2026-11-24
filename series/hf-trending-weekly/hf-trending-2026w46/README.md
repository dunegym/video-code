# Hugging Face 本周热榜 Top 5 · 2026 第 46 周（11 月 14 日）

成片：`hf_trending_top5_w46.mp4`（1920×1080，30fps，297.9 秒 ≈ 4:58，烧录 60px 字幕，整片约 -16 LUFS）+ `hf_trending_top5_w46.srt`
封面：`cover.png`（1920×1080）/ `cover_4x3.png`（1440×1080）/ `cover_3x4.png`（1080×1440），缩略预览在 build_covers/；视频描述：`description.txt`
榜单快照：`https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true`，2026-11-14 18:11:46（北京时间，UTC+8）= 02:11:46 PST（raw/snapshot_time.txt、raw/trending_models.json）。

## 榜单（合并重复项后）
| # | 模型 | 类型 | 点赞 / 30 天下载 / 热度分 |
|---|---|---|---|
| 1 | [Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B](https://huggingface.co/Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B) | 文本生成（Qwen3.5-9B 蒸馏，Apache-2.0） | 7,109 / 21,586 / 4,354（登顶的 Heretic 衍生仓库；原作者仓库点赞 75、近 30 天下载 2,320） |
| 2 | [MiniMaxAI/MiniMax-H3-Image](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) | 文生图 / 图像编辑（33.1B DiT，MiniMax-H3-Image 社区许可） | 1,067 / 437,039 / 984 |
| 3 | [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | image-to-video / 音视频联合生成（22B DiT，LTX-2.x 社区许可） | 11,836 / 2,777,667 / 424 |
| 4 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | image-text-to-text（27B 稠密，Apache-2.0） | 19,926 / 6,757,964 / 412 |
| 5 | [NousResearch/Arete-27B](https://huggingface.co/NousResearch/Arete-27B) | Qwen3.8-27B 监督微调（价值对齐，Apache-2.0） | 580 / 5,545 / 410 |

合并规则：同一模型的量化 / GGUF / 去审查 / ComfyUI 封装 / Base 等衍生仓库并入原模型，按组内最高名次排序。本周有一项合并改变了前五：
- **Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B ← xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic（原榜 #1）**。原作者蒸馏仓库本身不在 Top 40；画面和封面展示的 7,109 点赞来自这个 Heretic 衍生仓库，旁白和封面都说明需要打折扣。
- MiniMaxAI/MiniMax-H3-Image（#2）← Comfy-Org/MiniMax-H3-Image（#9，官方 ComfyUI 封装）。画面数字用的是官方原仓库。
- Qwen/Qwen3.8-27B（#4）← DavidAU/…-Heretic-Uncensored-…-GGUF（#7）、unsloth/Qwen3.8-27B-GGUF（#13）、huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF（#36）。画面数字用的是官方原仓库。
- **没有合并**：NousResearch/Arete-27B（#5）是第三方价值对齐 SFT，虽同底座但不并入 Qwen3.8-27B；tencent/Qwen3.8-27B-DSpine-b16（#16）是投机解码草稿模型；ConceptCountry/qwen-concept-27b（#38）是权重编辑研究；Viggle/Viggle-Remake（#19）是 MiniMax-H3（视频）上的角色替换 LoRA；VideoRebirthAI/hyperflow-h3-flash（#18）是 MiniMax-H3（视频）的量化——后两项都不并入 H3-Image。
- 顺延的下一名：speridlabs/idol（#6）、moonshotai/Kimi-K3.1-Pro（#8）、Zyphra/ZONOS3-Mini（#10）、thinkingmachines/Inkling-2-Small（#11）。

## 自报 / 第三方 / 社区观点（画面中均已标注）
- **官方自报**：Jackrong 模型卡的 GSM8K（本模型 NVFP4 + vLLM、四次平均 94.50%；对照转引自 openai/gsm8k）、MMLU-Pro（每个子集抽 500 题共 1500 题，不是完整题库；9B 为 MTP-Q8_0 GGUF + llama.cpp）、每道答对题的推理 token，以及“只输出一个字母”的格式跟随比例。Qwen3.8-27B 模型卡的文本与视觉/智能体对比表（SWE-bench Pro 等用 Claude Code 工具链复测，部分基准为通义自建）。Arete-27B 模型卡与 nousresearch.com/arete 的 Propaganda_Eval（803 题 × 5 次，裁判为 Grok 4.7；Arete / 底座 temperature 0、其余对照 0.6，不完全可比），以及 Hermes Bench、Terminal-Bench 2.1（作者写明不把 Terminal-Bench 的看似提升视为自己的成绩）。
- **第三方**：Artificial Analysis（2026-11-14 查询）。全榜名次 = 页面 JSON 的 0 起始 rank + 1。H3-Image 图像编辑 Elo 1137（全榜第 13，开源权重第 1）、文生图 Elo 1066（全榜第 25，开源权重第 1）；Highspeed 是 API 版本。Elo 来自两两偏好投票，不是指令执行正确率。AA 视频竞技场：文生视频 LTX-2.5 Fast 第 28（Elo 942）、MiniMax H3 768p 第 3（1161）、Wan 3.0 第 1（1175）；图生视频 LTX-2.5 Fast 第 32（Elo 912）。AA 测的是 LTX 的 API 版本。Qwen3.8-27B 智能指数 v5.0.1（xhigh）= 20，同尺寸开源中位数 8；单任务 44.1 分钟（中位数 14.9 分钟）、$3.53 / 任务，基于 Alibaba API。Jackrong 蒸馏模型和 Arete-27B 在 AA 暂未收录（相关页面返回 404）。
- **我们自己的复核（点赞账号注册时间）**：拉取公开点赞列表 `/api/models/<repo>/likers`，用账号 `_id`（ObjectId）前 8 位十六进制换算账号创建时间（UTC），2026-11-14 抓取。这只能说明账号的注册时间，**不能证明刷量，也看不出是谁在操作**。
  - Heretic 衍生仓库：列表 7,119 条（热榜显示 7,109），其中 6,046（84.9%）来自 2026-08 及以后注册的账号，5,064（71.1%）来自 11 月注册；按月：8 月 64、9 月 69、10 月 849、11 月 1–14 日 5,064。原作者仓库 75 个点赞里，8 月之后占 32.0%。
  - LTX-2.5：列表 11,837 条（热榜显示 11,836），8 月及以后占 58.5%（上周同口径 57.7%）；30 天下载上周 2,643,778 → 本周 2,777,667。对照组 MiniMax-H3-Image 为 20.0%，Arete-27B 为 22.4%。社区讨论 #97 最早用同样方法提出质疑。
- **社区观点（都是概述，不是原话）**：H3-Image 讨论区许可条款较活跃，有人抱怨名字容易和 H3 视频 / 视觉模型混淆。Qwen 讨论 #243 有用户反馈关闭思考时出现无限工具调用循环。Arete 讨论区对“西方价值观”的定义、是否有必要做政治向微调存在明显分歧；#23 有用户对比底座后认为在提问不存在的事物时可能有副作用（未独立核实）。
- **数据不一致**：Heretic 热榜点赞 7,109、点赞列表 7,119；LTX 热榜 11,836、列表 11,837（抓取时间略有差别）。AA 页面把 Qwen3.8-27B 上下文写成 256k，模型卡写原生 262,144、可至 1M。Arete 官网博客把宣传口径 0.9% 写成约 1%。Jackrong 的 GSM8K 与 MMLU-Pro 用了不同推理后端，作者自己写明不能据此比较量化一致性。

## 实测（本周没有调用在线 Space）
本周五个模型都没有适合匿名、低成本调用的官方 Space 演示（H3-Image 的出图需要较大 GPU）。画面里的 H3-Image 样张全部来自官方模型卡 showcase（文生图多风格、游戏地图改第一人称场景、空房 + 九件家具改客厅），已注明“官方”。没有在 Space 调用里使用 HF token，也没有在本机加载权重。

## 素材来源与许可
| 素材 | 来源 / 许可 |
|---|---|
| h3_hero / h3_edit_map / h3_edit_multi 等 showcase | MiniMaxAI/MiniMax-H3-Image 模型卡 assets（MiniMax-H3-Image Community License，2026-11-10；许可不包括欧盟、英国、韩国和美国） |
| 头像 av_* | 各组织 / 作者的 HF 头像（Jackrong、xtools-at 是用户头像，不是组织） |
| 其余图表 | 用 Manim 按模型卡、AA 页面和我们抓取的点赞列表重绘，画面里都注明了出处 |
| 字体 | Noto Sans CJK（SIL OFL） |
| 配音 | MiniMax T2A v2（api.minimaxi.com），speech-2.8-hd，音色 male-qn-jingying（精英青年），语速 1.1 |

下载了但封面或成片未全部用到的：h3_art / h3_char / h3_logo / h3_photo / h3_ref / h3_scene / h3_surreal / h3_text / h3_wf_* 等其他官方样张。LTX-2.5 的模型卡 README 对未登录请求返回 401，用已登录的 `hf` CLI 拉取。

## 安全
只读调研：没有执行任何仓库代码，没有加载任何 pickle 权重，也没有下载模型权重；只拉取了 API JSON、模型卡 README、论文信息、图片和公开点赞列表。MiniMax API key 只在运行时从 `/home/box/.config/minimax/api_key` 读取，没有打印，也没有写进脚本、日志或任何输出。

## 旁白
`tts.py` 按场景合成，每段前留 0.25 秒、后留 0.65 秒；用 MiniMax 的词级时间戳（subtitle_type=word）生成画面时间点（timing.json）和字幕（只在句读标点处断行）。多音字和英文名用 `pronunciation_dict` 校正（列表在 minimax_client.py 的 TONES 和 build/tts_summary.json），例如 重新、执行、长成、打折扣、占了、偏长、当裁判、看成，以及 Jackrong → Jack rong、Arete → 阿瑞忒、Nous Research。第一轮合成时长约 4:07，低于 5–6 分钟目标，随后扩写了格式跟随、16 张参考图、AA 偏好投票说明、LTX 许可、262K/1M 上下文、Arete 评测方法等段落，复用未改动的音频，最终旁白总长 297.8 秒 ≈ 4:58。没有用到 edge-tts 兜底。主合成计费约 3,471 字符（扩写后又补合成了部分场景）。

## 流水线
`build_data.py → data.json` → `script.py`（旁白）→ `tts.py`（MiniMax，生成 timing.json 和 audio/）→ `prep_assets.py` → `scenes.py` + `render.sh`（Manim 1080p30，按场景顺序渲染）→ `sheet.py`（每个场景抽帧检查，结果在 build_chk/）→ `assemble.py`（ffmpeg 拼接、烧录 60px ASS 字幕、生成 SRT、loudnorm -16 LUFS、x264 crf20、faststart）→ `checkcut.py`（成片抽帧，结果在 build_chk_final/）。
封面：`make_covers.py .`（读取 cover.json 和 data.json）。
Python 环境：`.venv` 软链到 `/workspace/github-trending-2026w45/.venv`（manim 0.22.1、Pillow、av）；`.gvenv`（gradio_client）软链到 `/workspace/hf-trending-2026w43-sat/.gvenv`；`.rvenv` 软链到 w45 `.rvenv`（本周未做点渲染）。
