"""MiniMax T2A v2 per-scene narration; word timestamps drive scene cues and punctuation-broken subtitles.
Re-synthesizes a scene only if its text (or pronunciation rules) changed."""
import json, os, pathlib, re, subprocess, sys
from script_ai import SCENES, ORDER
from minimax_client import synthesize, tones_for, VOICE, SPEED, MODEL
ROOT=pathlib.Path(__file__).resolve().parent
os.chdir(ROOT)
LEAD,TAIL=0.25,0.65
AUD=pathlib.Path('audio_ai'); AUD.mkdir(exist_ok=True)

def vw(s): return sum(1 if ord(c)>0x2e80 else 0.55 for c in s)
def split_lines(sent,maxw=22):
    # break only after sentence punctuation (never after 、 so lists stay intact)
    chunks=[c for c in re.split(r'(?<=[，。；：？！])',sent) if c]
    lines=[];cur=''
    for c in chunks:
        if cur and vw(cur)>=5 and vw(cur)+vw(c)>maxw:
            lines.append(cur);cur=c
        else: cur+=c
    if cur:
        if lines and vw(cur)<6 and vw(lines[-1])+vw(cur)<=maxw+4:lines[-1]+=cur
        else:lines.append(cur)
    return lines

def do_scene(scene,sents,force=False):
    text=''.join(sents)
    stem=AUD/scene
    mp=stem.with_suffix('.meta.json')
    cached = mp.exists() and stem.with_suffix('.json').exists() and stem.with_suffix('.flac').exists()
    if cached:
        m=json.load(mp.open())
        cached = m.get('text')==text and m.get('tones')==tones_for(text) and m.get('voice')==VOICE and m.get('speed')==SPEED
    if force or not cached:
        synthesize(text,stem)
    else:
        print(scene,'cached')
    words=[]
    for seg in json.load(stem.with_suffix('.json').open()):
        words.extend(seg.get('timestamped_words',[]))
    assert words and words[-1]['word_end']==len(text), (scene,'incomplete word timestamps',words[-1] if words else None,len(text))
    def span(a,b):
        ws=[w for w in words if w['word_begin']<b and w['word_end']>a]
        if not ws: raise ValueError((scene,a,b))
        return LEAD+min(w['time_begin'] for w in ws)/1000,LEAD+max(w['time_end'] for w in ws)/1000
    cues=[];subs=[];pos=0
    for sent in sents:
        a,b=pos,pos+len(sent);pos=b
        s,e=span(a,b);cues.append({'text':sent,'start':round(s,3),'end':round(e,3)})
        lp=a
        for line in split_lines(sent):
            s2,e2=span(lp,lp+len(line));lp+=len(line)
            subs.append({'text':line.strip().rstrip('，。；：'),'start':round(s2,3),'end':round(e2,3)})
    for x,y in zip(subs,subs[1:]):
        if y['start']-x['end']<0.6:x['end']=y['start']
    import av
    with av.open(str(stem.with_suffix('.flac'))) as container:
        dur=sum(frame.samples for frame in container.decode(audio=0))/container.streams.audio[0].rate
    total=round(LEAD+dur+TAIL,3)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(stem.with_suffix('.flac')),'-af',f'adelay={int(LEAD*1000)},apad,atrim=0:{total}','-ar','48000','-ac','2',str(stem.with_suffix('.wav'))],check=True)
    print(scene, total)
    return {'total':total,'cues':cues,'subs':subs}

def main():
    args=[a for a in sys.argv[1:] if a!='--force']; force='--force' in sys.argv
    path=pathlib.Path('timing_ai.json')
    tm=json.load(path.open()) if path.exists() else {}
    for sc in (args or ORDER):
        tm[sc]=do_scene(sc,SCENES[sc],force)
    tm={k:tm[k] for k in ORDER if k in tm}
    path.write_text(json.dumps(tm,ensure_ascii=False,indent=1))
    billed=sum((json.load(open(AUD/f'{s}.meta.json')).get('extra_info') or {}).get('usage_characters',0) for s in tm)
    summary={'provider':'MiniMax (api.minimaxi.com)','model':MODEL,'voice':VOICE,'speed':SPEED,'characters_billed_latest':billed,
             'pronunciation_rules':{s:json.load(open(AUD/f'{s}.meta.json')).get('tones') for s in tm}}
    pathlib.Path('build').mkdir(exist_ok=True)
    pathlib.Path('build/tts_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('TOTAL',round(sum(v['total'] for v in tm.values()),2),'scenes',len(tm))
if __name__=='__main__':main()
