"""渲染后单场景抽帧：4 张拼 1920x1080，红线标出字幕区上沿（y≈960）"""
import sys, json, subprocess
from PIL import Image, ImageDraw
tm = json.load(open("timing_w45.json"))
for s in sys.argv[1:]:
    d = tm[s]["total"]; W = Image.new("RGB", (1920, 1080))
    fr = [float(x) for x in (sys.argv and [0.3, 0.55, 0.8, 0.95])]
    for i, f in enumerate(fr):
        out = f"build_w45/pk_{s}_{i}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(d * f), "-i", f"media_w45/videos/scenes_w45/1080p30/{s}.mp4", "-frames:v", "1", out], check=True)
        im = Image.open(out); dr = ImageDraw.Draw(im); dr.line([(0, 960), (1920, 960)], fill="red", width=3)
        W.paste(im.resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
    W.save(f"build_w45/pk_{s}.png")
