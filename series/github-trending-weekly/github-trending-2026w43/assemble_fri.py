"""v3 合成：场景视频 + ffmpeg 叠加官方 GIF 演示 + 旁白；按 WordBoundary 时间生成 ASS/SRT（60px）并烧录。
输出 github_trending_top5_fri.mp4（v1 文件不动）"""
import json, os, subprocess
from script_fri import ORDER
tm = json.load(open("timing_fri.json", encoding="utf-8"))
run = lambda *a: subprocess.run(list(a), check=True)
os.makedirs("build", exist_ok=True)
parts = []
for s in ORDER:
    out = f"build/fri_{s}_av.mp4"; d = tm[s]["total"]
    ovf = f"build_fri/ov_{s}.json"
    ov = json.load(open(ovf)) if os.path.exists(ovf) else []
    inputs = ["-i", f"media_fri/videos/scenes_fri/1080p30/{s}.mp4"]
    fc = "[0:v]tpad=stop_mode=clone:stop_duration=2[b0];"
    last = "b0"
    for k, o in enumerate(ov, 1):
        inputs += ["-i", o["clip"]]
        fc += (f"[{k}:v]trim=start={o['ss']},setpts=(PTS-STARTPTS)/{o['speed']:.4f},fps=30,scale={o['w']}:{o['h']}:flags=lanczos,"
               f"format=rgba,setpts=PTS+{o['t0']}/TB[g{k}];"
               f"[{last}][g{k}]overlay={o['x']}:{o['y']}:enable='between(t,{o['t0']},{o['t0'] + o['dur']:.3f})'[b{k}];")
        last = f"b{k}"
    na = len(ov) + 1
    inputs += ["-i", f"audio_fri/{s}.wav"]
    fc += f"[{last}]trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p[v];[{na}:a]atrim=0:{d},asetpts=PTS-STARTPTS[a]"
    run("ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-r", "30", "-c:a", "pcm_s16le", "-ar", "48000", out)
    parts.append(out); print("scene", s, d, "overlays", len(ov))
open("build/list_fri.txt", "w").write("".join(f"file '{p.split('/')[-1]}'\n" for p in parts))
run("ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "build/list_fri.txt", "-c", "copy", "build/joined_fri.mkv")
def ts_ass(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
def ts_srt(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
ev, off = [], 0.0
for s in ORDER:
    for c in tm[s]["subs"]:
        ev.append((off + c["start"], off + c["end"], c["text"].rstrip("、，。；：")))
    off += tm[s]["total"]
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
open("subtitles_fri.ass", "w", encoding="utf-8").write(head + "".join(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Sub,,0,0,0,,{t}\n" for a, b, t in ev))
open("subtitles_fri.srt", "w", encoding="utf-8").write("\n".join(f"{i}\n{ts_srt(a)} --> {ts_srt(b)}\n{t}\n" for i, (a, b, t) in enumerate(ev, 1)))
run("ffmpeg", "-y", "-v", "error", "-i", "build/joined_fri.mkv", "-vf", "ass=subtitles_fri.ass",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", "github_trending_top5_fri.mp4")
print("done")
