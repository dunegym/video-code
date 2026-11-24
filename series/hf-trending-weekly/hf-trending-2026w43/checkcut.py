"""对最终成片逐场景抽帧：每个场景取 4 个时间点（含字幕），每张 sheet 拼 2 个场景"""
import json, subprocess
from PIL import Image
from script import ORDER
tm = json.load(open("timing.json")); off = 0; shots = []
for s in ORDER:
    d = tm[s]["total"]
    for f in (0.2, 0.45, 0.7, 0.96):
        shots.append((s, round(off + d * f, 2)))
    off += d
ims = []
for s, t in shots:
    out = f"build_chk_final/f_{s}_{t}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", "hf_trending_top5_w43_sat.mp4", "-frames:v", "1", "-vf", "scale=640:-1", out], check=True)
    ims.append(out)
for k in range(0, len(ims), 8):
    W = Image.new("RGB", (2560, 720))
    for i, p in enumerate(ims[k:k + 8]): W.paste(Image.open(p), ((i % 4) * 640, (i // 4) * 360))
    W.save(f"build_chk_final/cut_{k // 8:02d}.png")
print(len(ims))
