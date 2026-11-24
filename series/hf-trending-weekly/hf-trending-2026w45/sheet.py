"""逐场景抽帧检查：每个 cue 后 2 秒 + 结尾前 0.8 秒，拼成 3×2 大图（640×360 每格；另存全尺寸帧）"""
import json, subprocess, sys, os
from PIL import Image
tm = json.load(open("timing.json")); os.makedirs("build_chk", exist_ok=True)
for s in sys.argv[1:]:
    d = tm[s]; ts = sorted(set(round(min(c["start"] + 2.5, d["total"] - 0.8), 2) for c in d["cues"]) | {round(d["total"] - 0.8, 2)})[-6:]
    ims = []
    for t in ts:
        o = f"build_chk/{s}_{t}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", f"media/videos/scenes/1080p30/{s}.mp4", "-frames:v", "1", o], check=True)
        ims.append(o)
    W = Image.new("RGB", (1920, 720))
    for i, p in enumerate(ims): W.paste(Image.open(p).resize((640, 360)), ((i % 3) * 640, (i // 3) * 360))
    W.save(f"build_chk/sheet_{s}.png"); print(s, ts)
