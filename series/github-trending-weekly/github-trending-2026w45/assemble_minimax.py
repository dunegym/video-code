"""Reassemble identical Manim visuals at new MiniMax timing; add burned subtitles, SRT and AAC."""
import json, os, pathlib, subprocess
from script_w45 import ORDER
ROOT=pathlib.Path(__file__).resolve().parent;os.chdir(ROOT)
tm=json.load(open('timing_minimax.json',encoding='utf8'))
run=lambda *a:subprocess.run(list(a),check=True)
outdir=pathlib.Path('build_minimax/final');outdir.mkdir(exist_ok=True)
parts=[]
for s in ORDER:
    out=str(outdir/f'{s}.mp4');d=tm[s]['total'];ovf=pathlib.Path('build_minimax/scenes_minimax')/f'ov_{s}.json'
    ov=json.load(ovf.open()) if ovf.exists() else []
    inputs=['-i',f'media_minimax/videos/scenes_minimax/1080p30/{s}.mp4']
    fc='[0:v]tpad=stop_mode=clone:stop_duration=2[b0];';last='b0'
    for k,o in enumerate(ov,1):
        inputs+=['-i',o['clip']]
        fc+=(f'[{k}:v]trim=start={o["ss"]},setpts=(PTS-STARTPTS)/{o["speed"]:.4f},fps=30,scale={o["w"]}:{o["h"]}:flags=lanczos,format=rgba,setpts=PTS+{o["t0"]}/TB[g{k}];'
             f'[{last}][g{k}]overlay={o["x"]}:{o["y"]}:enable=\'between(t,{o["t0"]},{o["t0"]+o["dur"]:.3f})\'[b{k}];')
        last=f'b{k}'
    na=len(ov)+1;inputs+=['-i',f'audio_minimax/{s}.wav']
    fc+=f'[{last}]trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p[v];[{na}:a]atrim=0:{d},asetpts=PTS-STARTPTS[a]'
    run('ffmpeg','-y','-v','error',*inputs,'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-preset','medium','-crf','16','-r','30','-c:a','pcm_s16le','-ar','48000',out)
    parts.append(out);print('scene',s,d)
listp=outdir/'list.txt';listp.write_text(''.join(f"file '{p.split('/')[-1]}'\n" for p in parts))
run('ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listp),'-c','copy',str(outdir/'joined.mkv'))
def ts_ass(t):return f'{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}'
def ts_srt(t):
    ms=int(round(t*1000));return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
ev=[];off=0.
for s in ORDER:
    for c in tm[s]['subs']:ev.append((off+c['start'],off+c['end'],c['text'].rstrip('、，。；：')))
    off+=tm[s]['total']
head='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Sub,Noto Sans CJK SC,60,&H00F3EDE6,&H00FFFFFF,&H00110D0D,&H99000000,0,0,0,0,100,100,1,0,1,3.5,0,2,60,60,34,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'''
base='github_trending_top5_w45_minimax'
pathlib.Path(base+'.ass').write_text(head+''.join(f'Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Sub,,0,0,0,,{t}\n' for a,b,t in ev),encoding='utf8')
pathlib.Path(base+'.srt').write_text('\n'.join(f'{i}\n{ts_srt(a)} --> {ts_srt(b)}\n{t}\n' for i,(a,b,t) in enumerate(ev,1)),encoding='utf8')
run('ffmpeg','-y','-v','error','-i',str(outdir/'joined.mkv'),'-vf',f'ass={base}.ass','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-profile:v','high','-r','30','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',base+'.mp4')
print('DONE',base+'.mp4',off)
