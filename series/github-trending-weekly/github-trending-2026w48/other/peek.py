"""渲染后单场景抽帧：4 张拼 1920x1080，红线标出字幕区上沿（y≈960）"""
import sys, json, pathlib, subprocess
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
tm = json.loads((ROOT / "timing_other.json").read_text(encoding="utf-8"))
(ROOT / "build").mkdir(exist_ok=True)
for s in sys.argv[1:]:
    d = tm[s]["total"]
    W = Image.new("RGB", (1920, 1080))
    for i, f in enumerate([0.3, 0.55, 0.8, 0.93]):
        out = ROOT / f"build/pk_{s}_{i}.png"
        vid = ROOT / f"media_other/videos/scenes_other/1080p30/{s}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(d * f), "-i", str(vid), "-frames:v", "1", str(out)], check=True)
        im = Image.open(out)
        dr = ImageDraw.Draw(im)
        dr.line([(0, 960), (1920, 960)], fill="red", width=3)
        W.paste(im.resize((960, 540)), ((i % 2) * 960, (i // 2) * 540))
    W.save(ROOT / f"build/pk_{s}.png")
    print("peeked", s)
