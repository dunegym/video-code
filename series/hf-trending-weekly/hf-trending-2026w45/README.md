# Hugging Face 本周热榜 Top 5 · 2026 第 45 周（11 月 7 日）

成片：`hf_trending_top5_w45.mp4`（1920×1080，30fps，357.0 秒 ≈ 5:57，烧录 60px 字幕，整片 -16 LUFS）+ `hf_trending_top5_w45.srt`
封面：`cover.png`（1920×1080）/ `cover_4x3.png`（1440×1080）/ `cover_3x4.png`（1080×1440），缩略预览在 build_covers/；视频描述：`description.txt`
榜单快照：`https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true`，2026-11-07 18:15:12（北京时间，UTC+8）= 02:15 PST（raw/snapshot_time.txt、raw/trending_models.json）。

## 榜单（合并重复项后）
| # | 模型 | 类型 | 点赞 / 30 天下载 / 热度分 |
|---|---|---|---|
| 1 | [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) | image-text-to-text（2.8T / 104B 激活 MoE，Kimi K3.1-Pro 许可 = 改版 MIT） | 1,580 / 22,571 / 1,027 |
| 2 | [speridlabs/idol](https://huggingface.co/speridlabs/idol) | image-to-3d（自有 0.66B，Apache-2.0） | 994 / 20,689 / 706 |
| 3 | [ccore/Qwen3.5-4B-3D-Coder](https://huggingface.co/ccore/Qwen3.5-4B-3D-Coder) | Qwen3.5-4B 微调（Three.js 代码，Apache-2.0） | 816 / 221,506 / 414 |
| 4 | [Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5) | image-to-video / 音视频联合生成（22B DiT，LTX-2.x 社区许可） | 10,904 / 2,643,778 / 377 |
| 5 | [ricursiveAI/Ripple-65B-Preview](https://huggingface.co/ricursiveAI/Ripple-65B-Preview) | text-generation（65B 稠密，Apache-2.0） | 348 / 3,803 / 339 |

合并规则：同一模型的量化 / GGUF / 去审查 / Base 衍生仓库并入原模型，按组内最高名次排序。本周的合并都发生在 Top 5 之外，没有改变前五：
- Qwen/Qwen3.8-27B（#8）← DavidAU/…-Heretic-Uncensored-…-GGUF（#10）
- deepseek-ai/DeepSeek-V4.1-Flash-1017（#15）← AtomicChat/…-Uncensored-GSQ-RCO-GGUF（#11）、OBLITERATUS/…-obliterated（#14）、ISTA-DASLab/…-Coder-GGUF（#27）
- **没有合并**：ccore/Qwen3.5-4B-GLB-3D-Coder（原榜 #19）是同作者、同底座但另外训练的模型（数据集和目标都不同），在 #3 的章节里一起介绍，不计入名次。
- 顺延的下一名：burner22/numbat（#6，自称“Anthropic 泄露的预训练检查点”，来源无法核实，按名次自然落在第六，没有进入视频）、FusionCow/Sulphur-3（#7，早期访问版，模型卡没有内容）、Qwen/Qwen3.8-27B（#8）。

## 自报 / 第三方 / 社区观点（画面中均已标注）
- **官方自报**：Kimi 模型卡的对比表（Terminal-Bench 4.0、BenchCAD、OfficeQA Pro v2、HLE-Diamond、ExploitBench；对手分数一部分转引自各家报告）；Kimi 博客的 xdev-bench-hard 90.5 → 81.0（内部基准）；Idol 的 PSNR/SSIM/LPIPS/IoU/DINOv2/CLIP 以及显存、各 GPU 耗时（1×H100）；ccore 技术报告的开发测试（8 个场景、18 次调用，作者自己说是“探索性”测试）；Ripple 模型卡的 Terminal-Bench 2.1、SWE-bench Pro、MMLU-Pro、SciCode、MCP Atlas（模型卡斜体标出的对手分数是 Ricursive 自己补测的），以及 $32M 研发成本、1.4M rollout、40% MFU、团队人数。
- **第三方**：Artificial Analysis（2026-11-07 查询）——Kimi K3.1 Pro 智能指数 v5.0.1 = 46.45，开源同级第 1；单任务 $3.68、36.2 分钟（同级中位数 14.2 分钟）、33 tok/s（基于 Kimi 官方 API）。AA 视频竞技场：文生视频 LTX-2.5 Fast 排第 26（Elo 942）、MiniMax H3 768p 排第 3（1160），H3 是该榜标注为开源权重的模型中最高的；AA 测的是 LTX 的 API 版本。Ripple 在 AA 暂未收录（相关页面返回 404）。
- **我们自己的复核（LTX 点赞）**：拉取公开点赞列表 `/api/models/<repo>/likers`，用账号 `_id`（ObjectId）前 8 位十六进制换算账号创建时间（UTC）。LTX-2.5 的 10,905 个点赞中有 6,288 个（57.7%）来自 2026-08 之后注册的账号；对照组 MiniMaxAI/MiniMax-H3 是 1,387 / 6,640（20.9%）。按月分布见画面。30 天下载：上周 2,441,077 → 本周 2,643,778。这只能说明账号的注册时间，**不能证明刷量，也看不出是谁在操作**；社区讨论 #97 最早提出质疑，用的是同样的方法。
- **社区观点（都是概述，不是原话）**：Kimi #5 抱怨模型总坚持自称 Kimi；#7/#12 第三方 NVFP4 移植笔记提到检查点约 1.5 TB，单张 96GB 显卡生成约 2 tok/s、预填充约 40 tok/s（发帖者自述，未核实）。Idol #3 有人申请 DINOv3 被拒，没法运行。3D-Coder #15 有人把它当子代理、由大模型指挥分步搭建；#14 作者贴出和 DeepSeek V4.1 Flash 的对比。
- **数据不一致**：Idol 模型卡一处写“under 2 seconds”，但它自己的计时表里 H100 要 6.7 秒、单次请求 6.8 秒；视频用的是表里的数字，旁白不提秒数。

## 实测（匿名调用在线 Space，本机没有运行任何仓库代码）
| 文件 | 说明 |
|---|---|
| demo/idol_default.ply → demo/idol_turntable_x4.mp4 | Space `speridlabs/idol` 的 `/show_default_example`（预置背包示例，不占 GPU），返回 262,144 个高斯的标准 3DGS PLY。render_splat.py 用 numpy + matplotlib 画成点渲染转台，**不是真正的高斯光栅化**，孔洞和颗粒感是这个简化渲染造成的（画面和旁白都说明了）。输入图 demo/idol_backpack_input.webp 来自该 Space 的 examples/obj-backpack.webp |
| demo/idol（自备图片） | **失败**：用自备的茶壶图（Wikimedia，CC BY 4.0，demo/teapot_meta.json）调用 `/run`，匿名 ZeroGPU 额度不够；画面用的是预置示例 |
| demo/3dcoder_sample.json | **失败**：Space `akhaliq/qwen35-3d-coder-studio` 申请 330 秒 GPU，超过匿名用户上限 |
| demo/ripple_sample.json | **失败**：Space `akhaliq/ripple-65b-zerogpu` 跑了 102 秒只返回一截被截断的输出，然后额度用完；视频里没有用 |
| — | 没有在 Space 调用里使用 HF token |

## 素材来源与许可
| 素材 | 来源 / 许可 |
|---|---|
| idol_{armchair,lamp,castle,grandma} 动图 | speridlabs/idol 模型卡 Examples（Apache-2.0 仓库） |
| idol_backpack_input、idol_default.ply | speridlabs/idol Space 预置示例 |
| cc_tree_ref / cc_tree_out | ccore/Qwen3.5-4B-3D-Coder 模型卡（Apache-2.0）；参考图是社区讨论 #9 里网友提供的，版权归原作者 |
| glb_coral、glb_riftward | ccore/Qwen3.5-4B-GLB-3D-Coder 模型卡对比图、作者 Space 的 RIFTWARD 游戏动图（Apache-2.0） |
| 头像 av_* | 各组织 / 作者的 HF 头像 |
| 其余图表 | 用 Manim 按模型卡、技术报告、AA 和我们抓取的数据重绘，画面里都注明了出处 |
| 字体 | Noto Sans CJK（SIL OFL） |
| 配音 | MiniMax T2A v2（api.minimaxi.com），speech-2.8-hd，音色 male-qn-jingying（精英青年），语速 1.1 |
下载了但没有用在成片里的：kimi_* 博客封面、cc_roma3 / cc_sakura / cc_dragon、glb_goblin、teapot.jpg。LTX 的主图是 gated 下载（401），所以没有用。

## 安全
只读调研：没有执行任何仓库代码，没有加载任何 pickle 权重，也没有下载模型权重；只拉取了 API JSON、模型卡 README、技术报告 PDF、图片和 Space 返回的示例结果（一个 PLY 点云文件）。MiniMax API key 只在运行时从 `/home/box/.config/minimax/api_key` 读取，没有打印，也没有写进脚本、日志或任何输出。

## 旁白
`tts.py` 按场景合成，每段前留 0.25 秒、后留 0.65 秒；用 MiniMax 的词级时间戳（subtitle_type=word）生成画面时间点（timing.json）和字幕（只在句读标点处断行）。多音字和英文名用 `pronunciation_dict` 校正（列表在 minimax_client.py 的 TONES 和 build/tts_summary.json），例如 重新、长成、最长、重复、调整、背面、一小撮、差一截、转了一圈、卡在、还得、数量级、打个折扣、落在、冲上、给多，以及 CCORE → C core、Speridlabs → Sperid labs。没有用到 edge-tts 兜底。
盒子中途被重置过一次：已经合成的 13 段音频直接复用（tts.py 会检查文本是否一致，不重复计费），丢失的 P5b 和 S6_Outro 两段重新合成了一次。

## 流水线
`build_data.py → data.json` → `script.py`（旁白）→ `tts.py`（MiniMax，生成 timing.json 和 audio/）→ `prep_assets.py`（把动图转成首帧 PNG 和循环 MP4）→ `scenes.py` + `render.sh`（Manim 1080p30，按场景顺序渲染；动图位置写入 build/ov_<scene>.json）→ `sheet.py`（每个场景抽帧检查，结果在 build_chk/）→ `assemble.py`（ffmpeg 叠加动图和转台、拼接、烧录 60px ASS 字幕、生成 SRT、loudnorm -16 LUFS、x264 crf20、faststart）→ `checkcut.py`（成片抽帧，结果在 build_chk_final/）。
封面：`make_covers.py .`（读取 cover.json 和 data.json）。
Python 环境：`.venv` 软链到 `/workspace/github-trending-2026w45/.venv`（盒子重置后用 conda-forge 重建：manim 0.22.1、Pillow、av）；`.gvenv`（gradio_client）软链到 w43-sat；`.rvenv`（numpy、matplotlib，用于点渲染）。
