"""Render one 1080p MP4 with one-second title cards and punctuation-timed sample subtitles."""
import json,pathlib,subprocess
from PIL import Image,ImageDraw,ImageFont
import re
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'voice_samples';BUILD=OUT/'build';BUILD.mkdir(exist_ok=True)
data=json.load(open(OUT/'voices.json'))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
BG=(13,17,23);FG=(230,237,243);MUTED=(139,148,158);YELLOW=(227,179,65);BLUE=(47,129,247)

def vw(text):return sum(1 if ord(c)>0x2e80 else .55 for c in text)
def subtitle_lines(text):
    chunks=[c for c in re.split(r'(?<=[，。；：？！])',text) if c]
    return [''.join(chunks[i:i+2]).strip().rstrip('，。；：') for i in range(0,len(chunks),2)]
def f(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def wrap(draw,text,font,max_width):
    lines=[];cur=''
    for ch in text:
        # Do not end a line on opening punctuation or start one with Chinese closing punctuation.
        nxt=cur+ch
        if draw.textlength(nxt,font=font)>max_width and cur:
            if ch in '，。；：？！）」、':cur+=ch;lines.append(cur);cur=''
            else:lines.append(cur);cur=ch
        else:cur=nxt
    if cur:lines.append(cur)
    return lines

def card(v,subtitle=None):
    im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((110,85,230,150),radius=12,outline=BLUE,width=3)
    d.text((139,94),f"{v['number']:02d} / 11",font=f(30),fill=YELLOW)
    d.text((112,220),v['name'],font=f(72,True),fill=FG)
    d.text((112,325),v['voice_id'],font=f(32),fill=BLUE)
    d.line((112,485,1808,485),fill=(48,54,61),width=2)
    if subtitle is None:
        d.text((112,545),'普通话 · 语速 1.1 · 同一段旁白',font=f(40),fill=MUTED)
        d.text((112,625),v['gender']+'声｜'+v['description'],font=f(36),fill=FG)
        d.text((112,840),'speech-2.8-hd',font=f(30),fill=MUTED)
    else:
        d.text((112,540),'试听片段',font=f(30),fill=MUTED)
        lines=wrap(d,subtitle,f(64,True),1680)
        y=700-(len(lines)-1)*48
        for line in lines:
            w=d.textlength(line,font=f(64,True));d.text(((1920-w)/2,y),line,font=f(64,True),fill=FG);y+=102
        d.text((112,840),v['name'],font=f(38),fill=MUTED)
    d.text((112,960),'MiniMax 中文配音试听',font=f(30),fill=MUTED)
    d.text((1460,960),'GitHub 周热榜 · 第 45 周',font=f(30),fill=MUTED)
    return im

run=lambda a:subprocess.run(a,check=True)
timeline=[];parts=[];offset=0.;total_billed=0
for v in data['voices']:
    num=v['number'];mp3=OUT/pathlib.Path(v['file']).name;flac=mp3.with_suffix('.flac')
    import av
    with av.open(str(flac)) as c:dur=sum(frame.samples for frame in c.decode(audio=0))/c.streams.audio[0].rate
    cardtime=offset;audiotime=offset+1.0
    v.update(start=round(audiotime,3),title_start=round(cardtime,3),audio_duration=round(dur,3))
    c=BUILD/f'{num:02d}_title.png';card(v).save(c)
    title=BUILD/f'{num:02d}_title.mp4'
    run(['ffmpeg','-y','-v','error','-loop','1','-i',str(c),'-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t','1','-r','30','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000',str(title)])
    # Whole-sample static visual leaves wording readable for longer than any single caption.
    # Timed subtitles below follow word timestamps and only break at punctuation.
    s=BUILD/f'{num:02d}_sample.png';card(v,data['text']).save(s)
    sample=BUILD/f'{num:02d}_sample.mp4'
    run(['ffmpeg','-y','-v','error','-loop','1','-i',str(s),'-i',str(mp3),'-t',f'{dur+0.6:.3f}','-af',f'apad=whole_dur={dur+0.6:.3f},aresample=48000','-r','30','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',str(sample)])
    parts.extend([title,sample]);timeline.append(v)
    words=[]
    for seg in json.load(flac.with_suffix('.json').open()):words.extend(seg.get('timestamped_words',[]))
    pos=0
    for line in subtitle_lines(data['text']):
        a,b=pos,pos+len(line);pos=b
        matched=[w for w in words if w['word_begin']<b and w['word_end']>a]
        if matched:v.setdefault('subtitles',[]).append({'text':line,'start':round(audiotime+min(w['time_begin'] for w in matched)/1000,3),'end':round(audiotime+max(w['time_end'] for w in matched)/1000,3)})
    offset+=1.+dur+0.6;total_billed+=v['billed']
    print(num,v['name'],round(audiotime,3),round(dur,3))
concat=BUILD/'list.txt';concat.write_text(''.join("file '"+p.name+"'\n" for p in parts))
filters=','.join(f"drawtext=font='Noto Sans CJK SC':text='{c['text'].replace(chr(39), chr(92)+chr(39))}':fontcolor=0xE6EDF3:fontsize=52:bordercolor=0x0D0D11:borderw=4:x=(w-text_w)/2:y=h-118:enable='between(t,{c['start']},{c['end']})'" for v in timeline for c in v.get('subtitles',[]))
(BUILD/'subtitles.ffscript').write_text(filters)
run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(concat),'-filter_script:v',str(BUILD/'subtitles.ffscript'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-r','30','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(ROOT/'voice_samples_minimax.mp4')])
data['voices']=timeline;data['characters_billed_main']=total_billed;data['compilation_duration_seconds']=round(offset,3)
# Pronunciation dictionary stays the same as the remake.
data['pronunciation_dict']=['重新/(chong2)(xin1)','执行/(zhi2)(xing2)','长成/(zhang3)(cheng2)']
(OUT/'voices.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(OUT/'timestamps.txt').write_text('\n'.join(f"{v['number']}. {v['name']} | {v['voice_id']} | start {v['start']:.3f} s" for v in timeline)+'\n')
print('Total duration',offset)
