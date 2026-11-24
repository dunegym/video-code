"""合成：场景视频 + 动图/转台叠加（build/ov_<scene>.json）+ MiniMax 旁白；
按 MiniMax 词级时间戳生成 ASS/SRT（60px，只在句读标点处断行）并烧录；整片响度归一到 -16 LUFS。"""
import json, os, subprocess
from script import ORDER
tm = json.load(open("timing.json", encoding="utf-8"))
run = lambda *a: subprocess.run(list(a), check=True)
os.makedirs("build", exist_ok=True)
NAME = "hf_trending_top5_w45"
parts = []
for s in ORDER:
    out = f"build/{s}_av.mp4"
    if os.environ.get("SKIP_PARTS") and os.path.exists(out): parts.append(out); continue
    d = tm[s]["total"]
    ovf = f"build/ov_{s}.json"
    ov = json.load(open(ovf)) if os.path.exists(ovf) else []
    ins = ["-i", f"media/videos/scenes/1080p30/{s}.mp4"]
    fc = "[0:v]tpad=stop_mode=clone:stop_duration=2,fps=30,format=rgba[b0];"; last = "b0"
    for k, o in enumerate(ov, 1):
        ins += ["-i", o["clip"]]
        fc += (f'[{k}:v]trim=start={o["ss"]},setpts=(PTS-STARTPTS)/{o["speed"]:.4f},fps=30,scale={o["w"]}:{o["h"]}:flags=lanczos,format=rgba,'
               f'setpts=PTS+{o["t0"]}/TB[g{k}];'
               f'[{last}][g{k}]overlay={o["x"]}:{o["y"]}:eof_action=pass:enable=\'between(t,{o["t0"]},{o["t0"] + o["dur"]:.3f})\'[b{k}];')
        last = f"b{k}"
    na = len(ov) + 1
    ins += ["-i", f"audio/{s}.wav"]
    fc += f"[{last}]trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p[v];[{na}:a]atrim=0:{d},asetpts=PTS-STARTPTS[a]"
    run("ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
        "-crf", "16", "-r", "30", "-c:a", "pcm_s16le", "-ar", "48000", "-t", str(d), out)
    parts.append(out); print("scene", s, d, "overlays", len(ov))
open("build/list.txt", "w").write("".join(f"file '{p.split('/')[-1]}'\n" for p in parts))
run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "build/list.txt", "-c", "copy", "build/joined.mkv")
def ts_ass(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def ts_srt(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
ev, off = [], 0.0
for s in ORDER:
    for c in tm[s]["subs"]:
        ev.append((off + c["start"], off + c["end"], c["text"].rstrip("、，。；："), "Sub"))
    off += float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"build/{s}_av.mp4"],
                                capture_output=True, text=True, check=True).stdout)
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Noto Sans CJK SC,60,&H00F3EDE6,&H00FFFFFF,&H00110D0D,&H99000000,0,0,0,0,100,100,1,0,1,3.5,0,2,60,60,34,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open("subtitles.ass", "w", encoding="utf-8").write(head + "".join(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},{st},,0,0,0,,{t}\n" for a, b, t, st in ev))
open(f"{NAME}.srt", "w", encoding="utf-8").write("\n".join(f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n{t}\n" for i, (a, b, t, st) in enumerate(ev, 1)))
run("ffmpeg", "-y", "-v", "error", "-i", "build/joined.mkv", "-vf", "ass=subtitles.ass",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", f"{NAME}.mp4")
print("done")
