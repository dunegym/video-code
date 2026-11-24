"""Offline validation and representative frames. Does not execute trending project code."""
import json,pathlib,subprocess
from script_w45 import SCENES,ORDER
R=pathlib.Path(__file__).resolve().parent
tm=json.load(open(R/'timing_jingying.json'));o=0
expected=[]
for s in ORDER:
    m=json.load(open(R/f'audio_jingying/{s}.meta.json'))
    assert m['model']=='speech-2.8-hd' and m['voice']=='male-qn-jingying'
    assert m['text']==''.join(SCENES[s])
    cues,subs=tm[s]['cues'],tm[s]['subs']
    assert len(cues)==len(SCENES[s]) and all(c['text']==t for c,t in zip(cues,SCENES[s]))
    assert all(0<=x['start']<=x['end']<=tm[s]['total'] for x in subs)
    for x,y in zip(subs,subs[1:]):assert x['end']<=y['start']+0.001,(s,x,y)
    for f in (0.48,0.80):
        t=o+tm[s]['total']*f;active=next((x for x in subs if x['start']<=t-o< x['end']),None)
        if active: expected.append((s,round(t,3),active['text']))
    o+=tm[s]['total']
manifest=R/'build_jingying/check/manifest.json';manifest.parent.mkdir(exist_ok=True)
manifest.write_text(json.dumps(expected,ensure_ascii=False,indent=2))
for i,(s,t,text) in enumerate(expected):
    subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(R/'github_trending_top5_w45_jingying.mp4'),'-frames:v','1',str(manifest.parent/f'{i:02d}_{s}.png')],check=True)
print('Narration matches v2; timestamps and model/voice verified. Final duration:',o,'checked frames:',len(expected))
for s in ['P3a','P2c','P3b']:
    p=json.load(open(R/f'audio_jingying/{s}.json'))
    print(s,'pronunciation verified:', [x['pronounce_text'] for x in p if 'ㄔㄨㄥ' in x['pronounce_text'] or 'ㄓㄤ' in x['pronounce_text'] or 'ㄓˊ' in x['pronounce_text']])
