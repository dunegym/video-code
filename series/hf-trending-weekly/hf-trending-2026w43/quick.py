import json, subprocess, sys
from PIL import Image
tm = json.load(open('timing.json'))
sc = sys.argv[1:]
ims = []
for s in sc:
    o = f'build_chk/q_{s}.png'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(tm[s]['total'] - 0.75), '-i', f'media/videos/scenes/1080p30/{s}.mp4', '-frames:v', '1', o], check=True); ims.append(o)
for k in range(0, len(ims), 2):
    W = Image.new('RGB', (2560, 720))
    for i, p in enumerate(ims[k:k+2]): W.paste(Image.open(p).resize((1280, 720)), (i*1280, 0))
    W.save(f'build_chk/qp_{k//2:02d}.png')
