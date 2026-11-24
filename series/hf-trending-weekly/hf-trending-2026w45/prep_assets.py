"""从 assets/src 生成 assets/proc（动图 → 首帧 PNG + 循环 MP4，用于 ffmpeg 叠加）。"""
import subprocess, os, shutil, tempfile
from PIL import Image, ImageSequence
S, D = "assets/src/", "assets/proc/"
def anim(src, stem, loop_s):
    im = Image.open(src); tmp = tempfile.mkdtemp(); durs = []
    for i, fr in enumerate(ImageSequence.Iterator(im)):
        f = fr.convert("RGB"); w, h = f.size
        f = f.resize((w - w % 2, h - h % 2)); f.save(f"{tmp}/{i:04d}.png"); durs.append(fr.info.get("duration", 40) or 40)
        if i == 0: f.save(D + stem + "_f0.png")
    fps = round(1000 / (sum(durs) / len(durs)), 3)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i", f"{tmp}/%04d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", D + stem + ".mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", D + stem + ".mp4", "-t", str(loop_s), "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", D + stem + "_loop.mp4"], check=True)
    shutil.rmtree(tmp); print(stem, len(durs), "frames", fps, "fps")
for n in ["armchair", "lamp", "castle", "grandma"]: anim(S + f"idol_{n}.webp", f"idol_{n}", 24)
anim(S + "glb_riftward.gif", "glb_riftward", 40)
for n in ["cc_tree_ref", "cc_tree_out", "glb_coral", "glb_goblin", "cc_roma3"]: Image.open(S + n + ".png").convert("RGB").save(D + n + ".png")
Image.open("demo/idol_backpack_input.webp").convert("RGB").save(D + "idol_backpack_input.png")
