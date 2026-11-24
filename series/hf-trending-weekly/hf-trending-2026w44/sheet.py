"""逐场景抽帧检查：每个 cue 后 2 秒 + 结尾前 0.8 秒，拼成 2×2 大图（960×540 每格）"""
import json, subprocess, sys
from PIL import Image
tm = json.load(open("timing.json"))
for s in sys.argv[1:]:
    d = tm[s]; ts = [min(c["start"] + 2.0, d["total"] - 0.8) for c in d["cues"]] + [d["total"] - 0.8]
    ts = sorted(set(round(t, 2) for t in ts))[-4:] if len(ts) > 4 else ts
    ims = []
    for t in ts:
        o = f"build_chk/{s}_{t}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", f"media/videos/scenes/1080p30/{s}.mp4", "-frames:v", "1", o], check=True)
        ims.append(o)
    W = Image.new("RGB", (1920, 1080 if len(ims) > 2 else 540))
    for i, p in enumerate(ims): W.paste(Image.open(p).resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
    W.save(f"build_chk/sheet_{s}.png"); print(s, ts)
