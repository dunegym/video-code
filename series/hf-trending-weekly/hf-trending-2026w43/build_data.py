"""汇总 data.json：热榜快照（合并后 Top 5）+ 画面中所有图表数字及来源。"""
import json
ref = json.load(open("/workspace/hf-trending-2026w43/data.json"))["items"]
tr = {m["id"]: (i, m) for i, m in enumerate(json.load(open("raw/trending_models.json")), 1)}
def hf(repo):
    i, m = tr[repo]
    return dict(trending_position=i, likes=m["likes"], downloads_30d=m["downloads"], trendingScore=m["trendingScore"], createdAt=m.get("createdAt"), pipeline_tag=m.get("pipeline_tag"))
def merged(repos): return [dict(repo=r, **hf(r)) for r in repos]
items = {}
d = ref["deepseek"]; items["deepseek"] = dict(rank=1, name="DeepSeek-V4.1-Flash-1017", org="deepseek-ai", repo="deepseek-ai/DeepSeek-V4.1-Flash-1017",
    url="https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017", type="多模态大语言模型（image-text-to-text）", **hf("deepseek-ai/DeepSeek-V4.1-Flash-1017"),
    merged=merged(["dealignai/DeepSeek-V4.1-Flash-1017-UNCENSORED-FP8", "unsloth/DeepSeek-V4.1-Flash-1017-GGUF"]),
    facts=d["facts"], bench_card_1017=d["bench_card_1017"],
    third_party={"Artificial Analysis": {"intelligence_index": 45, "rank_open_weights": "2 / 121", "output_tokens_per_s": 195.2, "price_in_out_per_1M_usd": [0.3, 1.2],
                 "tokens_to_run_index": "210M（中位数 140M）", "ttft_s": 1.14, "checked": "2026-10-24", "url": "https://artificialanalysis.ai/models/deepseek-v4-1-flash-1017"},
                 "Hacker News": d["third_party"]["Hacker News"]}, sources=d["sources"], self_reported=["bench_card_1017", "kv_per_token_bytes"])
items["flint"] = dict(rank=2, name="Flint", org="RecursiveSI", repo="RecursiveSI/flint", url="https://huggingface.co/RecursiveSI/flint",
    type="文本生成 · 稀疏 MoE 编程智能体模型", **hf("RecursiveSI/flint"), merged=merged(["unsloth/flint-GGUF"]),
    facts={"params": "39.8B 总参数 / ~2.5B 激活（主体 ~2.2B）", "layers": "49 层：2 稠密 + 47 MoE；256 路由专家选 6 + 1 共享",
           "attention": "35 层滑动窗口（513 token，RoPE）+ 14 层全局注意力（NoPE）；QK RMSNorm；可学习 attention sink",
           "context": "262K（博客：最长 512K，推荐 256K）", "license": "Apache-2.0",
           "training": "从零训练：预训练 → 中期训练 → SFT → RL；不到 4 个月；架构搜索与量化方案由自动化研究系统 Eureka Machine 参与（35B-A3B 基线 → 40B-A2.5B）",
           "quant": "lm_head 量化到 4 bit；用 16 bit 教师在自选 coreset 上离线自蒸馏恢复（步数约为 QAT 一半）；NVFP4 与 BF16 差距 ≤0.7 分",
           "speed_self_reported": "M4 Pro MacBook Pro >125 tok/s；64GB RTX Spark >150 tok/s；Metal 解码 megakernel（M4/M5）"},
    bench_card={"cols": ["Flint BF16", "Flint NVFP4", "Qwen3.5", "Qwen3.6", "Laguna XS 2.1", "Qwen3.8", "Muse Glimmer", "Gemma 4"],
                "groups": {"Sparse MoE 33–35B/3B": ["Qwen3.5", "Qwen3.6", "Laguna XS 2.1"], "Dense 27–31B": ["Qwen3.8", "Muse Glimmer", "Gemma 4"]},
                "Terminal-Bench 2.1": [54.9, 53.7, 38.7, 44.9, 24.7, 73.0, 51.7, 43.4], "SWE-bench Pro v2": [89.7, 88.5, 68.6, 73.8, 38.6, 94.9, 86.0, 61.7],
                "SWE-bench Verified": [74.2, 74.1, 69.2, 73.4, 70.9, 75.6, 76.0, 66.6], "LiveCodeBench v6": [80.3, 80.8, 74.6, 80.4, 49.5, 90.3, 63.5, 80.0],
                "IFBench": [89.2, 88.1, 70.2, 67.9, 34.4, 79.5, 77.0, 76.0], "IFEval": [95.1, 94.6, 91.9, 89.6, 73.7, 94.6, 94.7, 94.6],
                "note": "† 为 Recursive 内部测得；全部为官方自报", "source": "RecursiveSI/flint 模型卡 flint_benchmarks_nvfp4.png"},
    third_party={"Artificial Analysis": "未收录（2026-10-24 检查）", "Hacker News": {"points": 27, "comments": 5, "url": "https://news.ycombinator.com/item?id=50183678"},
                 "Ollama": "flint:40b-a2b", "TechCrunch 2026-10-21": "报道可在笔记本运行、主要由 AI 系统研发"},
    demo={"space": "mrfakename/flint（社区 Space，非官方）", "file": "demo/flint_sample.json", "observed": "54.4 tok/s（Space 共享 GPU，不代表本地速度）；代码对 list 输入正确，但会原地修改传入列表、tuple 输入报错；把“两条断言”写成了输入检查"},
    sources=["https://huggingface.co/RecursiveSI/flint", "https://recursive.com/updates/introducing-recursive-flint", "https://news.ycombinator.com/item?id=50183678"], self_reported=["bench_card", "speed_self_reported"])
f = ref["flux"]; items["flux"] = dict(rank=3, name="FLUX 3 Image Klein", org="black-forest-labs", repo="black-forest-labs/flux-3-image-klein",
    url="https://huggingface.co/black-forest-labs/flux-3-image-klein", type="图像生成 + 编辑（text-to-image / image-to-image）", **hf("black-forest-labs/flux-3-image-klein"),
    merged=merged(["black-forest-labs/flux-3-image-klein-comfy"]), facts=f["facts"],
    third_party={"DesignArena": {"overall_win_rate": "47%", "elo": 1165, "rank": 48, "tournaments": 972, "checked": "2026-10-24", "url": "https://www.designarena.ai/models/flux-3-image-klein"},
                 "Artificial Analysis": f["third_party"]["Artificial Analysis"]}, demo=f["demo"], sources=f["sources"], self_reported=["bfl_internal", "vram"])
m = ref["moss"]; items["moss"] = dict(rank=4, name="MOSS-Image", org="OpenMOSS-Team", repo="OpenMOSS-Team/MOSS-Image-SFT",
    url="https://huggingface.co/OpenMOSS-Team/MOSS-Image-SFT", type="文生图（text-to-image）", **hf("OpenMOSS-Team/MOSS-Image-SFT"),
    merged=merged(["OpenMOSS-Team/MOSS-Image-Base", "Comfy-Org/MOSS-Image"]), facts=m["facts"], bench_paper=m["bench_paper"], third_party=m["third_party"],
    demo=m["demo"], sources=m["sources"], self_reported=["bench_paper"])
items["ltx"] = dict(rank=5, name="LTX-2.5", org="Lightricks", repo="Lightricks/LTX-2.5", url="https://huggingface.co/Lightricks/LTX-2.5",
    type="音视频联合生成（image-to-video / text-to-video，带音频）", **hf("Lightricks/LTX-2.5"), merged=[],
    facts={"params": "22B DiT", "released": "2026-08-11（仓库创建 2026-07-23，最后更新 2026-10-11）",
           "base_arch_LTX2_paper": "非对称双流 DiT（LTX-2：14B 视频 + 5B 音频），双向音视频交叉注意力只用时间维 RoPE；跨模态 AdaLN；分模态 VAE；arXiv:2601.03233",
           "new_in_2.5": ["原生多镜头（一次生成，跨镜头保持人物/光线/声音）", "Diffusion fidelity rendering：按画面复杂度动态分配算力", "扩散视频解码器取代 VAE 重建",
                          "定制 Gemma 4 12B 文本编码器", "提示增强器", "可选时长预测头", "改进的蒸馏版（8 步，CFG=1）"],
           "packaging": "按 ComfyUI 组件格式拆分发布；多数 LTX-2.3 LoRA 可直接使用", "license": "LTX-2.x Community License：年收入 < 1000 万美元免费商用",
           "speed_vendor": "2×GB200 上 6.8 秒生成 10 秒 720p（厂商口径，VentureBeat 报道）"},
    third_party={"Artificial Analysis T2V v2.1 开放权重（带音频）": {"MiniMax H3 (768p)": 1158, "LTX-2.5 Fast": 949, "LTX-2.5 Pro": 945, "LTX-2.3 Pro": 888, "LTX-2.3 Fast": 839,
                 "note": "Fast/Pro 为 LTX API 档位；总榜 #1 Wan 3.0（1175），LTX-2.5 Fast/Pro 为 #24/#25；Kling 3.0 Pro=1000 锚点", "checked": "2026-10-24",
                 "url": "https://artificialanalysis.ai/text-to-video/arena"}},
    demo={"space": "Lightricks/LTX-2.5（官方）", "file": "demo/ltx_sample.mp4", "meta": "demo/ltx_sample.json"},
    sources=["https://huggingface.co/Lightricks/LTX-2.5", "https://arxiv.org/abs/2601.03233", "https://artificialanalysis.ai/text-to-video/arena"], self_reported=["speed_vendor"])
repack = [("Flint", "RecursiveSI/flint", "unsloth/flint-GGUF", "GGUF（Unsloth）"),
          ("FLUX 3 Klein", "black-forest-labs/flux-3-image-klein", "black-forest-labs/flux-3-image-klein-comfy", "ComfyUI 版（官方）"),
          ("MOSS-Image", "OpenMOSS-Team/MOSS-Image-SFT", "Comfy-Org/MOSS-Image", "ComfyUI 版（Comfy-Org）"),
          ("DeepSeek 1017", "deepseek-ai/DeepSeek-V4.1-Flash-1017", "unsloth/DeepSeek-V4.1-Flash-1017-GGUF", "GGUF（Unsloth）")]
charts = {"repack_downloads": [dict(model=a, original=o, original_dl=tr[o][1]["downloads"], repack=r, repack_dl=tr[r][1]["downloads"], label=l) for a, o, r, l in repack],
          "source_note": "Hugging Face API downloads 字段（近 30 天；创建不足 30 天的仓库为创建以来）"}
out = dict(snapshot={"time": open("raw/snapshot_time.txt").read().strip(), "endpoint": "https://huggingface.co/api/models?sort=trendingScore&limit=40&full=true",
                     "runners_up": ["XHToken/Spark-X2.6-4B (#6)", "fishaudio/drama-3 (#7)"]}, items=items, on_screen_charts=charts)
json.dump(out, open("data.json", "w"), ensure_ascii=False, indent=1)
for k, v in items.items(): print(v["rank"], k, v["likes"], v["downloads_30d"], v["trendingScore"], [x["repo"] for x in v["merged"]])
print(charts)
