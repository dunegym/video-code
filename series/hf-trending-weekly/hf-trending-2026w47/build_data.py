"""汇总 data.json：热榜快照（合并后 Top 5）+ 画面中所有图表数字及来源。"""
import json, collections, datetime
from pathlib import Path

tr = {m["id"]: (i, m) for i, m in enumerate(json.load(open("raw/trending_models.json")), 1)}

def hf(repo):
    i, m = tr[repo]
    return dict(
        trending_position=i, likes=m["likes"], downloads_30d=m["downloads"],
        trendingScore=m["trendingScore"], createdAt=m.get("createdAt"),
        pipeline_tag=m.get("pipeline_tag"),
    )

def liker_months(path, months=None):
    d = json.load(open(path))
    c = collections.Counter()
    for u in d:
        oid = u.get("_id") or ""
        if len(oid) >= 8:
            c[datetime.datetime.fromtimestamp(int(oid[:8], 16), datetime.UTC).strftime("%Y-%m")] += 1
    months = months or ["2026-08", "2026-09", "2026-10", "2026-11"]
    new = sum(v for k, v in c.items() if k >= "2026-08")
    nov = c.get("2026-11", 0)
    return dict(
        total=len(d), new_since_aug=new,
        share_new=round(100 * new / len(d), 1) if d else None,
        new_since_nov=nov, share_nov=round(100 * nov / len(d), 1) if d else None,
        by_month={k: c.get(k, 0) for k in months},
    )

LIK = Path("raw/likers")
lc_inkling = liker_months(LIK / "likers_thinkingmachines_Inkling-2-Mini.json")
lc_haru = liker_months(LIK / "likers_higurashi-ai_Haru-4B.json")
lc_pi = liker_months(LIK / "likers_harness-hub_Qwen3.8-27B-pi-adapted.json")
lc_sentinel = liker_months(LIK / "likers_Sentinel7_h3.json")
lc_ltx = liker_months(LIK / "likers_Lightricks_LTX-2.5.json")
lc_hy4 = liker_months(LIK / "likers_tencent_Hy4-flash.json")
lc_small = liker_months(LIK / "likers_thinkingmachines_Inkling-2-Small.json")
lc_inworld = liker_months(LIK / "likers_inworld_voice-isolator.json")
lc_qwen = liker_months(LIK / "likers_Qwen_Qwen3.8-27B.json")

snap = hf("thinkingmachines/Inkling-2-Mini")
haru = hf("higurashi-ai/Haru-4B")
pi = hf("harness-hub/Qwen3.8-27B-pi-adapted")
sent = hf("Sentinel7/h3")
ltx = hf("Lightricks/LTX-2.5")

# 上周 LTX（w46 README / data.json）
ltx_w46 = dict(likes=11836, downloads_30d=2777667, trendingScore=424, share_new=58.5, share_nov=8.6, likers=11837, nov=1022)
ltx_w45 = dict(likes=10904, downloads_30d=2643778, share_new=57.7)

items = {}

items["inkling"] = dict(
    rank=1, name="Inkling-2-Mini", org="thinkingmachines",
    repo="thinkingmachines/Inkling-2-Mini",
    url="https://huggingface.co/thinkingmachines/Inkling-2-Mini",
    type="image-text-to-text · 循环 MoE 多模态（Apache-2.0）",
    **snap,
    merged=["unsloth/Inkling-2-Mini-GGUF（原榜 #7，GGUF 量化）"],
    facts=dict(
        created="2026-11-17 创建，模型卡标注发布于 2026-11-20",
        arch="循环 Transformer：24 层，中间 12 层共享权重跑 3 遍，每 token 48 次层计算；每层路由 8/128 专家；混合局部/全局注意力；ViT 视觉编码器",
        params="26.4B 总参数，3.4B 激活；循环额外约 1.0B×2，有效激活约 5.4B（模型卡）",
        context="原生最多 1M tokens；文本+图像输入，文本输出；NVFP4 / MXFP8 混合精度，单检查点约 20GB",
        license="Apache 2.0；另有 Model Acceptable Use Policy",
        loop="层 0–5 一次、6–17 三遍、18–23 一次；HF 博客：跨遍用 cross-pass messages 与门控混合",
    ),
    likes_check=dict(
        listed=lc_inkling, displayed_likes=snap["likes"],
        controls={
            "Qwen3.8-27B": lc_qwen["share_new"],
            "Hy4-flash": lc_hy4["share_new"],
            "Inkling-2-Small": lc_small["share_new"],
            "voice-isolator": lc_inworld["share_new"],
        },
    ),
    self_reported=dict(
        note="模型卡评测表，作者自报；对照包括 Gemma 4 31B、Muse Glimmer、Qwen3.8-27B、Nemotron 3.5 Super VL。表中 AA Index 与第三方页面一致，其余分项为作者评测设置。",
        params_active_total="5/26 vs 31/31、30/30、27/27、12/125",
        selected={
            "AA Index (v5.0)": {"Inkling 2 Mini": 20.1, "Gemma 4 31B": 4.4, "Muse Glimmer": 6.3, "Qwen3.8-27B": 20.1, "Nemotron 3.5 Super VL": 13.6},
            "SWE-bench Pro v2 Hard (mini-swe-agent)": {"Inkling 2 Mini": 77.9, "Gemma 4 31B": 14.2, "Muse Glimmer": 44.3, "Qwen3.8-27B": 73.8, "Nemotron 3.5 Super VL": 44.1},
            "Terminal Bench 2.1 (pi v0.83.0)": {"Inkling 2 Mini": 71.6, "Gemma 4 31B": 43.4, "Muse Glimmer": 51.7, "Qwen3.8-27B": 73.0, "Nemotron 3.5 Super VL": 60.7},
            "BrowseComp": {"Inkling 2 Mini": 79.0, "Gemma 4 31B": 37.0, "Muse Glimmer": 63.9, "Qwen3.8-27B": 61.6, "Nemotron 3.5 Super VL": 78.9},
            "MMMU Pro Standard 10": {"Inkling 2 Mini": 74.9, "Gemma 4 31B": 73.4, "Muse Glimmer": 74.3, "Qwen3.8-27B": 76.3, "Nemotron 3.5 Super VL": 72.3},
        },
    ),
    third_party={"Artificial Analysis": {
        "note": "2026-11-21 查询 https://artificialanalysis.ai/models/inkling-2-mini ；页面写 Intelligence Index 为 20，JSON 为 20.1315。可比模型中位数 10。输出 token 总量 161M（中位数 85.7M），偏长。AA 把该模型标为 reasoning、open weights、Apache 2.0，参数 26B、有效激活 5.4B、上下文 1,024,000。",
        "intelligence_index": 20,
        "intelligence_index_raw": 20.1315214698783,
        "comparable_median": 10,
        "tokens_generated_index_m": 161,
        "tokens_generated_median_m": 85.7,
        "price_input_per_1m_usd": 0.15,
        "price_output_per_1m_usd": 0.50,
        "price_input_median": 0.14,
        "price_output_median": 0.32,
        "cost_per_task_usd": 0.59,
        "minutes_per_task": 9.0,
        "minutes_per_task_median": 9.2,
        "url": "https://artificialanalysis.ai/models/inkling-2-mini",
        "queried": "2026-11-21",
    }},
    community=["讨论区有人反馈重复说 actually let me act（#7）；有地区不可用投诉（#10）；有人在做 MLX / 本地部署（#11）。均为社区讨论概述。"],
    sources=[
        "https://huggingface.co/thinkingmachines/Inkling-2-Mini",
        "https://huggingface.co/blog/inkling2mini",
        "https://artificialanalysis.ai/models/inkling-2-mini",
        "https://huggingface.co/unsloth/Inkling-2-Mini-GGUF",
    ],
)

items["haru"] = dict(
    rank=2, name="Haru-4B", org="higurashi-ai",
    repo="higurashi-ai/Haru-4B",
    url="https://huggingface.co/higurashi-ai/Haru-4B",
    type="audio-to-audio · 全双工语音对话基座（Apache-2.0）",
    **haru,
    merged=[],
    facts=dict(
        created="2026-11-12 创建，技术博客 2026-11-13，作者 Rikuto Kotoge",
        arch="Qwen3.5-4B 文本骨干（32 层，hidden 2560）；用户音频 / 模型音频 / 模型文本每 133 ms（7.5 Hz）相加进同一位置；VibeVoice 声学 tokenizer，24 kHz，每潜变量 3200 样本；4 层 MLP MeanFlow 头，1 步采样，默认 guidance 1.5",
        data="预训练超过 4000 万小时真实语音，覆盖 160+ 语言，主攻 9 语；刻意排除 LLM/TTS 合成轮替对话。第二阶段用 FastDialogueSidon 分离得到约 1300 万小时全双工数据，样本最长 60 分钟。256×NVIDIA B200，约 8 天，Megatron-LM。",
        latency="作者自测：M1 Max + 原生 Swift / Metal，int8，端到端约 65.2±1.5 ms（不含最多 133 ms 的帧填充）。B300 上编码+一步 LM 约 15 ms。",
        license="Apache-2.0；研究用预训练基座，不是可靠助手；只用有权使用的参考音色。",
        demo="官方博客有投资咨询等英文对话演示视频；约 12 GB 显存可跑。",
    ),
    likes_check=dict(
        displayed_likes=haru["likes"],
        listed=lc_haru,
        mismatch=True,
        note="热榜/模型页显示 5,711 点赞（页面写作 5.71k），公开 /likers 列表即使用登录 token 也只有 801 条，且无分页续页。列出的 801 条里，2026-08 及以后只占 11.4%。这是点赞计数与列表的不一致，不能据此推断列表内账号被刷。",
        controls={
            "Inkling-2-Mini": lc_inkling["share_new"],
            "Hy4-flash": lc_hy4["share_new"],
            "Qwen3.8-27B": lc_qwen["share_new"],
        },
    ),
    self_reported=["latency_m1_max", "training_hours", "arch"],
    third_party={"Artificial Analysis": "未就 Haru-4B 语音对话模型做对等收录（2026-11-21 未找到模型页）"},
    community=["讨论区问 12GB 显存能否跑（#3）、是否会出指令微调版（#4）、请求 Spaces 演示（#1）；有社区把模型接到 CMF 推理栈（#2）。均为概述。"],
    sources=[
        "https://huggingface.co/higurashi-ai/Haru-4B",
        "https://blog.higurashi.ai/melte/haru4b/",
        "https://github.com/higurashi-ai/Haru",
    ],
)

items["pi"] = dict(
    rank=3, name="Qwen3.8-27B-pi-adapted", org="harness-hub",
    repo="harness-hub/Qwen3.8-27B-pi-adapted",
    url="https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted",
    type="Qwen3.8-27B 的 LoRA 适配器（为 pi 编程代理，Apache-2.0）",
    **pi,
    merged=[],
    facts=dict(
        created="2026-11-16 创建",
        method="AsyncGRPO（TRL 实验接口）+ LoRA；r=32, alpha=64，作用于 q/k/v/o/gate/up/down；奖励为任务 verifier 的 correctness + 0.1 工具效率奖励",
        data="750 个 scale800 任务与 300 个 TermGrade 任务交错；本检查点为 step 160（计划 1000，跑到 191 停止）；8 rollouts/任务，温度 0.8，思考关闭，每条最多 50 步 / 1800 秒；2×B200（vLLM + trainer）",
        harness="pi 编程代理；Harbor + OpenEnv，HF sandbox，safeagents 审查工具调用；视觉塔不提供服务，纯文本",
        license="Apache-2.0；底座 Qwen/Qwen3.8-27B",
        gguf="另有 harness-hub/Qwen3.8-27B-pi-adapted-GGUF（本周未进入 Top 40）",
    ),
    likes_check=dict(displayed_likes=pi["likes"], listed=lc_pi),
    self_reported=dict(
        note="全部为作者在 pi 框架下的自报：每题一次尝试，100 步预算，思考默认关闭，温度 0.8。作者写明不可与 Qwen3.8-27B 模型卡数字直接比较（后者用 Terminus / Claude Code、最大思考、更大预算、完整 SWE-bench Pro）。checkpoint 按 SWE-bench Pro 与 Terminal-Bench 2.1 的 18 题子集挑选。",
        table={
            "SWE-bench Pro (hard 51)": {"base": 39.2, "base_xhigh": 74.5, "adapter": 64.7, "adapter_xhigh": 74.5},
            "Terminal-Bench 2.1": {"base": 41.0, "base_xhigh": 54.2, "adapter": 56.6, "adapter_xhigh": 56.6},
        },
        paired={
            "SWE-bench Pro (hard 51)": {"tasks": 51, "base": 39.2, "adapter": 64.7, "delta": 25.5, "ci95": 14.2, "gained": 15, "lost": 2, "p": 0.0023},
            "Terminal-Bench 2.1": {"tasks": 86, "base": 39.5, "adapter": 55.8, "delta": 16.3, "ci95": 9.1, "gained": 16, "lost": 2, "p": 0.0013},
        },
        tokens_vs_thinking="相对底座 xhigh 思考：生成 token 约 4.5× 更少（SWE 中位 48.8k / 9.4k，Terminal 16.5k / 3.7k）",
        corrections=["思考开、16k 截断时曾报过偏低分数，改为 32k 后底座与适配器在 SWE-bench Pro 均为 74.5%", "早期 29.4%→62.7% 含评测通道中途故障，已重跑"],
        caveats="底座在 SWE 31 次失败里有 20 次用尽 100 次模型调用，适配器没有；思考开时 Terminal 常碰到 1 小时时限。部分提升来自更能在预算内完成。",
    ),
    third_party={"Artificial Analysis": "未单独收录该适配器（2026-11-21）"},
    community=["有讨论询问离开 pi 框架后真实质量（#8、#16）；有人关注训练时的网络访问（#14）以及关掉思考后仍会大段可见推理（#11）。均为概述。"],
    sources=[
        "https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted",
        "https://huggingface.co/blog/harness-adapters-at-scale",
        "https://github.com/earendil-works/pi",
    ],
)

items["sentinel"] = dict(
    rank=4, name="h3", org="Sentinel7",
    repo="Sentinel7/h3",
    url="https://huggingface.co/Sentinel7/h3",
    type="社区 LoRA 合集（面向 MiniMax H3 视频，无模型卡）",
    **sent,
    merged=[],
    facts=dict(
        created="2026-08-06 创建，最近修改 2026-11-19；无 README / cardData / pipeline_tag / license",
        structure="快照中 861 个文件：404 组数字目录（类似模型站 id/version），404 个 README，419 个 safetensors；317 个权重文件名含 h3 或 minimax。不是官方基础模型。",
        content="从文件名看，合集面向 MiniMax H3 视频模型的社区 LoRA，其中不少为成人向。成片不展示任何样例。",
        author="用户 Sentinel7（2025-10-28 注册）。同作者另有 14 个类似打包仓库（krea2、qwen-image、ltxv、wan、flux 等），热榜快照时这些仓库近 30 天下载均为 0。另有 2026-11-21 新建的 Sentinel7/minimax-h3-image，与本仓库不是同一项。",
        not_official="与 MiniMaxAI/MiniMax-H3 或 MiniMax-H3-Image 均不是同一模型，不能合并。",
    ),
    likes_check=dict(
        displayed_likes=sent["likes"], listed=lc_sentinel,
        note="点赞列表 564 条，与热榜 563 接近（抓取时刻略有差别）。2026-08 及以后占 24.3%，与对照接近，没有出现新账号占比异常。异常主要是：下载为 0，却有五百多点赞，且没有模型卡。",
        controls={"Inkling-2-Mini": lc_inkling["share_new"], "Hy4-flash": lc_hy4["share_new"], "Qwen3.8-27B": lc_qwen["share_new"]},
    ),
    self_reported=[],
    third_party={"Artificial Analysis": "不适用（不是基础模型发布）"},
    community=["讨论区有多条内容投诉（#3、#5、#6），也有人要求补 README（#2、#9）或停止更新（#4、#7）。均为讨论区概况，不构成已裁定结论。"],
    sources=["https://huggingface.co/Sentinel7/h3"],
)

items["ltx"] = dict(
    rank=5, name="LTX-2.5", org="Lightricks",
    repo="Lightricks/LTX-2.5",
    url="https://huggingface.co/Lightricks/LTX-2.5",
    type="image-to-video / 音视频联合生成（22B DiT，LTX-2.x 社区许可）",
    **ltx,
    merged=[],
    facts=dict(
        created="2026-07-23 创建",
        new="原生多镜头一次生成；按场景复杂度动态分配算力；扩散视频解码器取代 VAE 重建；定制 Gemma 4 12B 文本编码器",
        arch_paper="LTX-2（arXiv:2601.03233）：非对称双流 Transformer，14B 视频流 + 5B 音频流，双向音视频交叉注意力，模态感知 CFG",
        ckpt="22B DiT（dev / distilled 8 步，bf16 / int8 / NVFP4）",
        license="LTX-2.x Community License：年收入 < 1000 万美元免费商用；以上需付费协议",
        wow={"likes": ltx["likes"] - ltx_w46["likes"], "downloads": ltx["downloads_30d"] - ltx_w46["downloads_30d"],
             "likes_w46": ltx_w46["likes"], "downloads_w46": ltx_w46["downloads_30d"],
             "likes_w45": ltx_w45["likes"], "downloads_w45": ltx_w45["downloads_30d"]},
    ),
    likes_check=dict(
        **lc_ltx,
        share_new_w46=ltx_w46["share_new"], share_new_w45=ltx_w45["share_new"],
        share_nov_w46=ltx_w46["share_nov"],
        method="公开点赞列表 /api/models/<repo>/likers，按账号 _id 前 8 位解析账号创建时间（UTC），2026-11-21 抓取；只能说明账号注册时间，不能证明刷量或谁在操作",
        community="讨论 #97 仍开放，最早用同样方法提出质疑（社区观点）",
        controls={"Hy4-flash": lc_hy4["share_new"], "Inkling-2-Mini": lc_inkling["share_new"], "Qwen3.8-27B": lc_qwen["share_new"], "voice-isolator": lc_inworld["share_new"]},
    ),
    third_party={"Artificial Analysis Video Arena": {
        "note": "全榜名次 = 页面 JSON 的 values.rank + 1（与 storedRank 一致）；AA 测的是 LTX API 的 Fast / Pro 版本。2026-11-21 查询。",
        "t2v": {
            "url": "https://artificialanalysis.ai/video/leaderboard/text-to-video",
            "board": "AA-Video-T2V v2.1",
            "LTX-2.5 Fast": {"rank_overall": 29, "elo": 937.72, "appearances": 5494, "elo_pm": 14, "price_per_min_usd": 7.8},
            "LTX-2.5 Pro": {"rank_overall": 30, "elo": 937.2, "appearances": 5334, "price_per_min_usd": 10.2},
            "Wan 3.0": {"rank_overall": 1, "elo": 1175.5},
            "w46_fast": {"rank_overall": 28, "elo": 942},
        },
        "i2v": {
            "url": "https://artificialanalysis.ai/video/leaderboard/image-to-video",
            "board": "AA-Video-I2V v2.1",
            "LTX-2.5 Fast": {"rank_overall": 33, "elo": 912, "appearances": 5007, "elo_pm": 15, "price_per_min_usd": 7.8},
            "LTX-2.5 Pro": {"rank_overall": 32, "elo": 912.41, "appearances": 5061, "price_per_min_usd": 10.2},
            "w46_fast": {"rank_overall": 32, "elo": 912},
        },
    }},
    community=["#97 点赞质疑仍开放；另有许可（#93）、口型稳定性（#106）等讨论。均为概述。"],
    sources=["https://huggingface.co/Lightricks/LTX-2.5",
             "https://artificialanalysis.ai/video/leaderboard/text-to-video",
             "https://artificialanalysis.ai/video/leaderboard/image-to-video"],
    self_reported=[],
)

# 顺延下一名（合并后）：Hy4-flash 原 #6，并入 AngelSlim GGUF #31，仍是第 6
out = dict(snapshot={
    "time": open("raw/snapshot_time.txt").read().strip(),
    "endpoint": "https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true",
    "merge_policy": "同一模型的量化 / GGUF / 去审查 / ComfyUI 封装 / Base 等衍生仓库合并计入原模型，按组内最高名次排序",
    "merges_affecting": [
        "thinkingmachines/Inkling-2-Mini（#1）← unsloth/Inkling-2-Mini-GGUF（#7，官方量化/GGUF 封装）。合并不改变前五名次。",
    ],
    "not_merged": [
        "thinkingmachines/Inkling-2-Small（#27）是同一系列的更大尺寸，不并入 Mini",
        "harness-hub/Qwen3.8-27B-pi-adapted（#3）是面向 pi 编程代理的第三方强化学习 LoRA，虽同底座但不并入 Qwen/Qwen3.8-27B（类似上周 Arete-27B）",
        "harness-hub/Qwen3.8-27B-opencode-adapted（#23）同理，是面向 OpenCode 的另一份适配器",
        "Sentinel7/h3（#4）是 MiniMax H3 视频模型的社区 LoRA 合集，不是官方发布，也不并入 MiniMax-H3-Image 或 MiniMax-H3",
        "tencent/Hy4-flash（#6）与 tencent/Hy4（#24）是不同结构版本（Flash 引入混合注意力、LatentMoE、Engram），不互相合并；AngelSlim/Hy4-flash-GGUF（#31）并入 Hy4-flash，不影响前五",
        "Qwen/Qwen3.8-27B（#11）← unsloth GGUF（#20）、DavidAU Heretic GGUF（#22）、huihui-ai abliterated GGUF（#34）；合并后官方仓库仍是组内最高名次 #11，未进入前五",
        "RadixArk/DaisyRose-27B（#13）、Cloudflare/clairic（#21）是第三方微调，不并入 Qwen3.8-27B",
    ],
    "runners_up": [
        "tencent/Hy4-flash（#6，并入 AngelSlim/Hy4-flash-GGUF #31）",
        "inworld/voice-isolator（#8）",
        "meituan-longcat/LongCat-Video-Avatar-1.6（#9）",
        "n4ze3m/tiny-voca（#10）",
    ],
    "dropped_from_w46": [
        "Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B 及 Heretic 衍生仓库本周不在 Top 40",
        "MiniMaxAI/MiniMax-H3-Image 本周原榜 #14（点赞 1,067→1,693，近 30 天下载 437,039→876,986）",
        "Qwen/Qwen3.8-27B 本周原榜 #11（点赞 19,926→20,749，近 30 天下载 6,757,964→6,298,190）",
        "NousResearch/Arete-27B 本周不在 Top 40",
    ],
}, items=items)
json.dump(out, open("data.json", "w"), ensure_ascii=False, indent=1)
for k, v in items.items():
    print(v["rank"], k, v["likes"], v["downloads_30d"], v["trendingScore"], "pos", v["trending_position"], "merged", len(v.get("merged") or []))
