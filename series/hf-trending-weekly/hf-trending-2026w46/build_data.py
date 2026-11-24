"""汇总 data.json：热榜快照（合并后 Top 5）+ 画面中所有图表数字及来源。"""
import json, collections, datetime
tr = {m["id"]: (i, m) for i, m in enumerate(json.load(open("raw/trending_models.json")), 1)}
def hf(repo):
    i, m = tr[repo]
    return dict(trending_position=i, likes=m["likes"], downloads_30d=m["downloads"], trendingScore=m["trendingScore"], createdAt=m.get("createdAt"), pipeline_tag=m.get("pipeline_tag"))
def liker_months(path, months=None):
    d = json.load(open(path)); c = collections.Counter()
    for u in d:
        c[datetime.datetime.fromtimestamp(int(u["_id"][:8], 16), datetime.UTC).strftime("%Y-%m")] += 1
    months = months or ["2026-08", "2026-09", "2026-10", "2026-11"]
    new = sum(v for k, v in c.items() if k >= "2026-08")
    nov = c.get("2026-11", 0)
    return dict(total=len(d), new_since_aug=new, share_new=round(100 * new / len(d), 1),
                new_since_nov=nov, share_nov=round(100 * nov / len(d), 1),
                by_month={k: c.get(k, 0) for k in months})

# 登上原榜 #1 的是 heretic 衍生仓库
heretic = "xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic"
canon = "Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B"
h = hf(heretic)
# 原作者仓库不在本周 Top 40，点赞等用单独 API 快照
jack_api = json.load(open("raw/Jackrong_DeepSeek-V4-Pro-Qwen3.5-9B.api.json"))

items = {}
items["jackrong"] = dict(
    rank=1, name="DeepSeek-V4-Pro-Qwen3.5-9B", org="Jackrong",
    repo=canon, url=f"https://huggingface.co/{canon}",
    type="文本生成 · Qwen3.5-9B 蒸馏（数学 / STEM）",
    trending_position=h["trending_position"],
    likes=h["likes"], downloads_30d=h["downloads_30d"], trendingScore=h["trendingScore"],
    createdAt=jack_api.get("createdAt"), pipeline_tag="text-generation",
    canonical_likes=jack_api.get("likes"), canonical_downloads=jack_api.get("downloads"),
    merged=[dict(repo=heretic, note="Heretic / 去审查衍生仓库（原榜 #1）；合并计入原作者蒸馏模型，名次取组内最高", **h)],
    facts={
        "params": "9B（Qwen3.5-9B 底座）",
        "teacher": "DeepSeek-V4-Pro（Max Effect）蒸馏",
        "data": "约 25 万条数学与 STEM 样本；监督微调后再做轻度 GSPO 强化学习；两阶段都没有编程数据",
        "eval_backends": "GSM8K 用 NVFP4 + vLLM（四次平均）；MMLU-Pro 用 MTP-Q8_0 GGUF + llama.cpp、8K 上下文",
        "license": "Apache-2.0",
        "author_note": "作者写明 MMLU-Pro 是每个子集抽 500 题，不是完整题库；GSM8K 与 MMLU-Pro 用了不同推理后端，不能据此比较量化一致性",
        "created_canonical": "2026-07-19", "created_heretic": "2026-10-30",
    },
    bench_gsm8k={"cols": ["DeepSeek-V4-Pro-Qwen3.5-9B", "DeepSeek-V4-Pro（教师）", "Llama-3.3-70B-Instruct", "Llama-3.1-405B-Instruct", "MiMo-V2.5-Pro"],
                 "GSM8K": [94.50, 92.60, 94.84, 96.80, 99.60],
                 "source": "Jackrong 模型卡（官方自报；本模型为 NVFP4、vLLM、四次平均 94.50%；其余分数转引自 openai/gsm8k 仓库）"},
    bench_mmlu={"cols": ["DeepSeek-V4-Pro-Qwen3.5-9B", "Qwen3.5-9B", "Claude Mythos-distilled 9B", "Claude Mythos-distilled 27B", "DeepSeek-V4-Pro-Qwen3.5-4B"],
                "Math": [92.40, 90.60, 86.00, 88.40, 80.40],
                "Physics": [89.40, 89.00, 78.60, 87.60, 74.20],
                "Chemistry": [89.80, 89.20, 78.60, 82.60, 74.80],
                "Average": [90.53, 89.60, 81.07, 86.20, 76.47],
                "source": "Jackrong 模型卡（官方自报；每个子集 500 题、共 1500 题；9B 行为 MTP-Q8_0 GGUF）"},
    efficiency={"cols": ["DeepSeek-V4-Pro-Qwen3.5-9B", "Qwen3.5-9B", "Claude Mythos-distilled 9B"],
                "accuracy": [90.53, 89.60, 81.07],
                "tokens_per_correct": [3157, 4938, 4083],
                "correct_per_1m": [316.8, 202.5, 244.9],
                "vs_qwen_token_save_pct": 36.1,
                "source": "Jackrong 模型卡（官方自报，同一 1500 题 MMLU-Pro 样本）"},
    format_follow={"this": {"terse_letter_pct": 97.2, "verbose_pct": 0.2},
                   "Qwen3.5-9B": {"terse_letter_pct": 37.3, "verbose_pct": 62.1},
                   "Claude Mythos-distilled 9B": {"terse_letter_pct": 69.6, "verbose_pct": 21.1},
                   "source": "Jackrong 模型卡（官方自报，MMLU-Pro 同一题、同一系统提示）"},
    likes_check={
        "heretic": liker_months("raw/likers_xtools-at_DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic.json"),
        "canonical": liker_months("raw/likers_Jackrong_DeepSeek-V4-Pro-Qwen3.5-9B.json"),
        "MiniMax-H3-Image": liker_months("raw/likers_MiniMaxAI_MiniMax-H3-Image.json"),
        "Arete-27B": liker_months("raw/likers_NousResearch_Arete-27B.json"),
        "method": "公开点赞列表 /api/models/<repo>/likers，按账号 _id（ObjectId）前 8 位解析账号创建时间（UTC），2026-11-14 抓取；只能说明点赞账号的注册时间，不能证明刷量或谁在操作",
        "headline_likes_are": "衍生仓库（原榜 #1）的点赞 / 下载 / 热度分；原作者仓库不在本周 Top 40",
    },
    third_party={"Artificial Analysis": "未收录（2026-11-14 检查）"},
    community={"Jackrong #1": "有用户把它和 ornith 1.5 9B 比较（讨论很少）",
               "heretic #1": "有人反映 config.json 仍声明 MTP 层，但权重已去掉，下游会报错（已关闭）",
               "heretic #3/#5": "有人询问图像能力和 GGUF（社区观点，概述）"},
    sources=["https://huggingface.co/Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B",
             "https://huggingface.co/xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic"],
    self_reported=["bench_gsm8k", "bench_mmlu", "efficiency", "format_follow"],
)

items["h3img"] = dict(
    rank=2, name="MiniMax-H3-Image", org="MiniMaxAI", repo="MiniMaxAI/MiniMax-H3-Image",
    url="https://huggingface.co/MiniMaxAI/MiniMax-H3-Image",
    type="文生图 / 图像编辑 · 33.1B DiT（H3 去音频）",
    **hf("MiniMaxAI/MiniMax-H3-Image"),
    merged=[dict(repo="Comfy-Org/MiniMax-H3-Image", note="官方 ComfyUI 封装，并入原模型", **hf("Comfy-Org/MiniMax-H3-Image"))],
    facts={
        "dit": "33.1B 稠密单流 Transformer，50 层，hidden 5376，56 头，FFN 14336，3D multimodal RoPE；BF16，嵌入/时间步/输出层 FP32",
        "text_encoder": "沿用 MiniMax-H3 的 Qwen3-VL 文本编码器（不在本仓库，约 66.7 GB），DiT 读第 50 层隐状态",
        "vae": "CNN 编码器 + 24 层 2D ViT 解码器，16× 空间下采样，24 个潜在通道；2×2 patch → 每 token 覆盖 32×32 像素",
        "sampling": "蒸馏到 6 步（6 NFE），不用 classifier-free guidance；guidance_scale 必须为 1，步数必须为 6",
        "resolution": "直接生成约 16MP，常见尺寸 4096×4096（1:1）至 6272×2688（21:9），不用超分；有效工作范围约 4–20MP",
        "refs": "最多 16 张参考图；生成与编辑共用一个检查点",
        "pe": "可选提示词扩展 MiniMax-H3-Image-PE（NVFP4，17.9 GB）；API 侧对应 H3-Image-Context-IR",
        "license": "MiniMax-H3-Image Community License（2026-11-10）：适用地区为全球，但不包括欧盟、英国、韩国和美国；年收入超过 100 万美元，或对外提供托管服务，需另行书面授权",
        "created": "仓库 2026-11-03 创建；许可写明发布日期 2026-11-10",
    },
    likes_check={"MiniMax-H3-Image": liker_months("raw/likers_MiniMaxAI_MiniMax-H3-Image.json")},
    third_party={
        "Artificial Analysis": {
            "checked": "2026-11-14",
            "note": "Elo 为配对人类偏好投票；全榜名次按页面 JSON 的 0 起始 rank + 1；AA 同时给出 API 定价。H3-Image Highspeed 为 API 版本。",
            "editing": {
                "board": "AA-Image-Editing v2.1",
                "H3-Image": {"rank_overall": 13, "elo": 1136.84, "appearances": 3201, "elo_pm": 16, "price_per_1k_usd": 26.54, "open_weights_rank": 1},
                "H3-Image Highspeed": {"rank_overall": 14, "elo": 1133.83, "appearances": 3151, "price_per_1k_usd": 45.25},
                "url": "https://artificialanalysis.ai/image/leaderboard/editing/open-weights",
            },
            "t2i": {
                "board": "AA-Image-T2I v2.1",
                "H3-Image": {"rank_overall": 25, "elo": 1065.68, "appearances": 3258, "elo_pm": 14, "price_per_1k_usd": 21.79, "open_weights_rank": 1},
                "H3-Image Highspeed": {"rank_overall": 24, "elo": 1071.67, "appearances": 3362, "price_per_1k_usd": 35.29},
                "followers_open": {"Qwen-Image-2.1": 1047, "FLUX 3 Image Klein": 1041},
                "url": "https://artificialanalysis.ai/image/leaderboard/text-to-image",
                "faq": "AA 页面说明：开源权重文生图由 H3-Image 以 Elo 1066 领先，其后为 Qwen-Image-2.1（1047）与 FLUX 3 Image Klein（1041）",
            },
        }
    },
    community={"#3": "许可条款问答较活跃",
               "#23": "有用户称它是开源改图第一（社区观点，概述；与后来 AA 开源改图第一的结果方向一致，但是发帖者当时的看法）",
               "#27": "有人抱怨名字容易和 H3 视频 / 视觉模型混淆",
               "#9": "有用户对比了它和原版 MiniMax H3 的出图",
               "#20/#25": "有人分享在苹果芯片和低显存设备上的运行方法（社区自述）"},
    sources=["https://huggingface.co/MiniMaxAI/MiniMax-H3-Image",
             "https://artificialanalysis.ai/image/leaderboard/editing/open-weights",
             "https://artificialanalysis.ai/image/leaderboard/text-to-image"],
    self_reported=[],
)

items["ltx"] = dict(
    rank=3, name="LTX-2.5", org="Lightricks", repo="Lightricks/LTX-2.5",
    url="https://huggingface.co/Lightricks/LTX-2.5",
    type="音视频联合生成（image-to-video 等）· 22B DiT",
    **hf("Lightricks/LTX-2.5"), merged=[],
    facts={"created": "2026-07-23 创建",
           "new": "原生多镜头一次生成；按场景复杂度动态分配算力；扩散视频解码器取代 VAE 重建；定制 Gemma 4 12B 文本编码器",
           "arch_paper": "LTX-2（arXiv:2601.03233）：非对称双流 Transformer，14B 视频流 + 5B 音频流，双向音视频交叉注意力，模态感知 CFG",
           "ckpt": "22B DiT（dev / distilled 8 步，bf16 / int8 / NVFP4）",
           "license": "LTX-2.x Community License：年收入 < 1000 万美元免费商用；以上需付费协议"},
    likes_check={"LTX-2.5": liker_months("raw/likers_Lightricks_LTX-2.5.json"),
                 "MiniMax-H3-Image": liker_months("raw/likers_MiniMaxAI_MiniMax-H3-Image.json"),
                 "Arete-27B": liker_months("raw/likers_NousResearch_Arete-27B.json"),
                 "method": "公开点赞列表 /api/models/<repo>/likers，按账号 _id 前 8 位解析账号创建时间（UTC），2026-11-14 抓取；只能说明账号注册时间，不能证明刷量或谁在操作",
                 "community": "讨论 #97 首先提出质疑并给出同样方法（社区观点）",
                 "likes_w45": 10904, "downloads_w45": 2643778, "share_new_w45": 57.7},
    third_party={"Artificial Analysis Video Arena": {
        "checked": "2026-11-14",
        "note": "[名次, Elo, 对比次数]；全榜名次 = JSON rank + 1；AA 测的是 LTX API 的 Fast / Pro 版本",
        "text-to-video": {
            "LTX-2.5 Fast": [28, 941.87, 4859],
            "LTX-2.5 Pro": [29, 937.61, 4735],
            "MiniMax H3 (768p)": [3, 1160.91, 7948],
            "Wan 3.0": [1, 1175.13, 7787],
            "Pika H3 Flex": [14, 1124.81, 4817],
            "url": "https://artificialanalysis.ai/video/leaderboard/text-to-video",
            "open_weights_faq": "AA 说明开源权重文生视频由 MiniMax H3 以 Elo 1161 领先，其后为 Pika H3 Flex（1125）与 LTX-2.5 Fast（942）",
        },
        "image-to-video": {
            "LTX-2.5 Fast": [32, 911.77, 4842],
            "LTX-2.5 Pro": [31, 911.98, 4911],
            "MiniMax H3 (768p)": [4, 1133.69, 6594],
            "url": "https://artificialanalysis.ai/video/leaderboard/image-to-video",
        }}},
    sources=["https://huggingface.co/Lightricks/LTX-2.5", "https://arxiv.org/abs/2601.03233",
             "https://huggingface.co/Lightricks/LTX-2.5/discussions/97"],
    self_reported=[],
)

items["qwen"] = dict(
    rank=4, name="Qwen3.8-27B", org="Qwen", repo="Qwen/Qwen3.8-27B",
    url="https://huggingface.co/Qwen/Qwen3.8-27B",
    type="多模态稠密模型（image-text-to-text）· 27B",
    **hf("Qwen/Qwen3.8-27B"),
    merged=[
        dict(repo="DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF",
             note="Heretic / 去审查 GGUF，并入官方模型", **hf("DavidAU/Qwen3.8-27B-TURBO-Fable-Cold-Fusion-735-882-Heretic-Uncensored-NEO-CODER-MAX-MTP-GGUF")),
        dict(repo="unsloth/Qwen3.8-27B-GGUF", note="官方模型的 GGUF 量化", **hf("unsloth/Qwen3.8-27B-GGUF")),
        dict(repo="huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF", note="abliterated GGUF，并入官方模型", **hf("huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF")),
    ],
    facts={
        "params": "27B 稠密 · 64 层 · hidden 5120 · 词表 248,320（padded）",
        "layout": "16 ×（3 ×（Gated DeltaNet → FFN）→ 1 ×（Gated Attention → FFN））",
        "deltanet": "线性注意力：V 48 头、QK 16 头，头维 128",
        "attn": "门控注意力：Q 24 头、KV 4 头，头维 256，RoPE 维 64",
        "ffn": "中间维 17,408",
        "context": "原生 262,144，可扩展至 1,000,000",
        "mtp": "训练了多步 MTP",
        "thinking": "默认开思考，可按请求关闭；可用 reasoning_effort 调节深度，preserve_thinking 保留历史推理",
        "vl": "原生视觉语言模型，支持图像和视频",
        "license": "Apache-2.0",
        "created": "2026-08-05",
    },
    bench_text={
        "cols": ["Qwen3.8-27B", "Qwen3.6-27B", "Qwen3.7-Plus", "Muse Glimmer-30B", "Opus4.6 Max"],
        "Terminal Bench 2.1": [73.0, 63.4, 64.0, 51.7, 78.2],
        "SWE-bench Pro": [61.7, 53.5, 57.6, 51.2, 53.4],
        "CoWorkBench": [70.7, 61.0, 65.1, None, 68.2],
        "IFBench": [79.5, 69.1, 79.1, 77.0, 62.5],
        "GPQA Diamond": [89.2, 87.8, 90.3, 83.5, 91.3],
        "LiveCodeBench v6": [90.3, 83.9, 89.6, None, 88.8],
        "source": "Qwen/Qwen3.8-27B 模型卡（官方自报；SWE-bench Pro 等用 Claude Code 工具链复测，Opus 一行用官方报告分；部分基准为通义自建）",
    },
    bench_vl={
        "cols": ["Qwen3.8-27B", "Qwen3.6-27B", "Qwen3.7-Plus", "Muse Glimmer-30B", "Opus4.6 Max"],
        "OSWorld-Verified": [84.3, 63.9, 73.3, 65.9, 72.7],
        "WebArena-Verified": [64.8, 48.8, 55.3, None, None],
        "AndroidWorld": [81.9, 70.3, 81.0, None, 62.0],
        "MathVision (w/o CI)": [90.0, 85.1, 90.3, None, 65.5],
        "source": "Qwen/Qwen3.8-27B 模型卡（官方自报）",
    },
    third_party={"Artificial Analysis": {
        "intelligence_index_v5_0_1": 20,
        "efforts": {"xhigh": 20, "medium": 17, "low": 16, "non-reasoning": 10},
        "comparable_open_median": 8,
        "time_per_task_min": {"xhigh": 44.1, "medium": 34.0, "low": 31.1, "non-reasoning": 18.6, "median_comparable": 14.9},
        "output_tok_s": 42,
        "cost_per_task_usd": 3.53,
        "price_in_out_per_1M_usd": [0.50, 3.00],
        "blended_7_2_1_per_1M_usd": 0.47,
        "output_tokens_index": 128_000_000,
        "output_tokens_median": 77_700_000,
        "context": "256k（AA 页面；模型卡写原生 262,144、可至 1M）",
        "provider": "基于 Alibaba API",
        "checked": "2026-11-14",
        "url": "https://artificialanalysis.ai/models/qwen3-8-27b",
    }},
    community={"#243": "有用户反馈关闭思考时出现无限工具调用循环",
               "#225": "有人分享本地 GPU 测速（社区自述）",
               "#234": "独立 NVFP4 移植笔记",
               "#228": "有人分享在韩国转播中自动剪辑比赛集锦的生产案例（社区自述）"},
    sources=["https://huggingface.co/Qwen/Qwen3.8-27B", "https://artificialanalysis.ai/models/qwen3-8-27b"],
    self_reported=["bench_text", "bench_vl"],
)

items["arete"] = dict(
    rank=5, name="Arete-27B", org="NousResearch", repo="NousResearch/Arete-27B",
    url="https://huggingface.co/NousResearch/Arete-27B",
    type="Qwen3.8-27B 监督微调（价值对齐）",
    **hf("NousResearch/Arete-27B"), merged=[],
    facts={
        "base": "Qwen/Qwen3.8-27B（独立后训练，非 Qwen 官方）",
        "method": "只做 SFT，没有 RL、没有偏好优化、没有改结构",
        "teacher": "Inkling（作者选择的开源教师）",
        "data": "七个主题上生成约 2 万条提示，去重并剔除与评测集重叠的部分；训练样本 28,886 条（Nous 数据画像页），每轮约 26.4M token，两轮共约 52.8M token，64k 上下文、不打包、不截断",
        "train": "1,202 步，两轮，batch 48，峰值学习率 1e-5；bf16 计算、fp32 主权重；张量并行 4；视觉编码器冻结，MTP 头训练时关闭",
        "categories": ["言论自由", "国家意识形态", "国家与自由市场", "教育", "数据隐私与监控", "民主", "环境政策"],
        "license": "Apache-2.0",
        "created": "2026-11-06",
        "eval_set": "803 道题，来源为英文法规、新闻和研究报告；裁判为 Grok 4.7，不告知答案来自哪个模型；先在 25 题上手动校准规则",
    },
    bench_prop={
        "cols": ["Arete-27B", "Qwen3.8-27B", "Inkling（教师）", "Mistral Large 4", "GLM 5.3", "DeepSeek V4.1 Flash"],
        "fact_mean": [2.98, 2.32, 3.96, 3.65, 3.10, 2.39],
        "fact_sd": [0.03, 0.03, 0.07, 0.04, 0.06, 0.05],
        "propaganda_pct": [0.9, 22, 0.3, 0.3, 15, 16],
        "note": "Arete 与 Qwen 为 temperature 0、thinking off；其余行为 temperature 0.6。五次跑完 803 题。官网博客把 0.9% 写成约 1%。",
        "freedom_of_expression": {"fact": [0.89, 2.44], "propaganda_pct": [60, 1]},
        "score0_of_803": [359, 216],
        "source": "NousResearch/Arete-27B 模型卡与 nousresearch.com/arete（官方自报）",
    },
    bench_cap={
        "cols": ["Qwen3.8-27B", "Arete-27B"],
        "Hermes Bench": [65.77, 65.60],
        "Terminal-Bench-2.1": [67, 70],
        "source": "模型卡（官方自报；作者写明不把 Terminal-Bench 的看似提升视为自己的成绩，可能来自推理配置差异）",
    },
    likes_check={"Arete-27B": liker_months("raw/likers_NousResearch_Arete-27B.json")},
    third_party={"Artificial Analysis": "未收录（2026-11-14 检查，/models/arete-27b 返回 404）"},
    community={"多方争论": "讨论区对“西方价值观”的定义、是否有必要做政治向微调存在明显分歧（社区观点，概述，非原话）",
               "#23": "有用户对比它和底座，认为在提问不存在的事物时表现有副作用（社区观点，概述，未独立核实）",
               "#16": "有用户做了中英 A/B，质疑是否过拟合到单一价值体系（社区观点，概述）",
               "#42": "有用户称一些基础智能体任务失败（社区自述）"},
    sources=["https://huggingface.co/NousResearch/Arete-27B", "https://nousresearch.com/arete",
             "https://huggingface.co/datasets/NousResearch/Propaganda_Eval",
             "https://nousresearch.com/interactive/arete/data-profile"],
    self_reported=["bench_prop", "bench_cap"],
)

out = dict(snapshot={
    "time": open("raw/snapshot_time.txt").read().strip() + "（北京时间，UTC+8）",
    "endpoint": "https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true",
    "merge_policy": "同一模型的量化 / GGUF / 去审查 / ComfyUI 封装 / Base 等衍生仓库合并计入原模型，按组内最高名次排序",
    "merges_affecting": [
        "Jackrong/DeepSeek-V4-Pro-Qwen3.5-9B ← xtools-at/DeepSeek-V4-Pro-Qwen3.5-9B-UNCENSORED-heretic（原榜 #1；原作者仓库不在 Top 40）",
        "MiniMaxAI/MiniMax-H3-Image（#2）← Comfy-Org/MiniMax-H3-Image（#9，ComfyUI 封装）",
        "Qwen/Qwen3.8-27B（#4）← DavidAU/…-Heretic-Uncensored-…-GGUF（#7）、unsloth/Qwen3.8-27B-GGUF（#13）、huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF（#36）",
    ],
    "not_merged": [
        "NousResearch/Arete-27B（#5）是第三方价值对齐 SFT，虽同底座但不并入 Qwen3.8-27B",
        "tencent/Qwen3.8-27B-DSpine-b16（#16）是投机解码草稿模型，用途不同",
        "ConceptCountry/qwen-concept-27b（#38）是权重编辑研究，不按量化合并",
        "Viggle/Viggle-Remake（#19）是 MiniMax-H3（视频）上的角色替换 LoRA，与 H3-Image 不是同一模型",
        "VideoRebirthAI/hyperflow-h3-flash（#18）是 MiniMax-H3（视频）的量化，不并入 H3-Image",
    ],
    "runners_up": ["speridlabs/idol（#6）", "moonshotai/Kimi-K3.1-Pro（#8）", "Zyphra/ZONOS3-Mini（#10）", "thinkingmachines/Inkling-2-Small（#11）"],
}, items=items)
json.dump(out, open("data.json", "w"), ensure_ascii=False, indent=1)
for k, v in items.items():
    print(v["rank"], k, v["likes"], v["downloads_30d"], v["trendingScore"], "pos", v["trending_position"], "merged", len(v.get("merged") or []))
print("heretic likes check", items["jackrong"]["likes_check"]["heretic"])
