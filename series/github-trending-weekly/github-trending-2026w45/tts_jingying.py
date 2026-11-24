"""Use MiniMax's word timestamps for scene cues and punctuation-broken subtitles."""
import json, os, pathlib, re, subprocess, sys
from script_w45 import SCENES, ORDER
from minimax_client_jingying import synthesize, VOICE, SPEED
ROOT=pathlib.Path(__file__).resolve().parent
os.chdir(ROOT)
LEAD,TAIL=0.25,0.65

def vw(s): return sum(1 if ord(c)>0x2e80 else 0.55 for c in s)
def split_lines(sent,maxw=22):
    chunks=[c for c in re.split(r'(?<=[，。；：？！])',sent) if c]
    lines=[];cur=''
    for c in chunks:
        if cur and vw(cur)>=5 and vw(cur)+vw(c)>maxw:
            lines.append(cur);cur=c
        else: cur+=c
    if cur:
        if lines and vw(cur)<6 and vw(lines[-1])+vw(cur)<=maxw+4:lines[-1]+=cur
        else:lines.append(cur)
    out=[]
    for l in lines:
        while vw(l)>maxw+4:
            cut=len(l)//2
            while cut>4 and re.match(r'[A-Za-z0-9./_-]',l[cut]) and re.match(r'[A-Za-z0-9./_-]',l[cut-1]):cut-=1
            out.append(l[:cut]);l=l[cut:]
        out.append(l)
    return out

def do_scene(scene,sents):
    text=''.join(sents)
    stem=pathlib.Path('audio_jingying')/scene
    meta=synthesize(text,stem)
    words=[]
    for seg in json.load(stem.with_suffix('.json').open()):
        words.extend(seg.get('timestamped_words',[]))
    assert words and words[-1]['word_end']==len(text), (scene,'incomplete word timestamps')
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
    print(scene, total, 'billed',meta.get('extra_info',{}).get('usage_characters'))
    return {'total':total,'cues':cues,'subs':subs}

def main():
    path=pathlib.Path('timing_jingying.json')
    tm=json.load(path.open()) if len(sys.argv)>1 and path.exists() else {}
    billed=sum(json.load(open(f'audio_jingying/{s}.meta.json'))['extra_info']['usage_characters'] for s in tm)
    for sc in (sys.argv[1:] or ORDER):
        tm[sc]=do_scene(sc,SCENES[sc])
        billed+=json.load(open(f'audio_jingying/{sc}.meta.json'))['extra_info']['usage_characters']
    pathlib.Path('timing_jingying.json').write_text(json.dumps(tm,ensure_ascii=False,indent=1))
    summary={'provider':'MiniMax','model':'speech-2.8-hd','voice':VOICE,'speed':SPEED,'characters_billed_main':billed,'pronunciation_rules':['重新/(chong2)(xin1)','执行/(zhi2)(xing2)','长成/(zhang3)(cheng2)'],'selected_from_samples':7}
    pathlib.Path('build_jingying/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('TOTAL',sum(v['total'] for v in tm.values()),'BILLED',billed)
if __name__=='__main__':main()
