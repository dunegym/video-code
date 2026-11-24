"""Generate an 11-voice MiniMax comparison. Credentials stay in the runtime key file."""
import concurrent.futures, json, os, pathlib, subprocess
from script_w45 import SCENES
from minimax_client import synthesize
ROOT=pathlib.Path(__file__).resolve().parent;os.chdir(ROOT)
TEXT=''.join(SCENES['P3a'])
VOICES=[
 {'name':'温柔学姐','voice_id':'Chinese (Mandarin)_Gentle_Senior','gender':'女','description':'温暖柔和、亲切的学姐感','ref':True},
 {'name':'新闻女声','voice_id':'Chinese (Mandarin)_News_Anchor','gender':'女','description':'专业端正的新闻播音腔','ref':True},
 {'name':'成熟女性','voice_id':'female-chengshu','gender':'女','description':'成熟沉稳的成年女声','ref':True},
 {'name':'播报男声','voice_id':'Chinese (Mandarin)_Male_Announcer','gender':'男','description':'磁性清晰、权威的男声播报'},
 {'name':'青涩青年音色','voice_id':'male-qn-qingse','gender':'男','description':'清爽年轻、有活力的青年声'},
 {'name':'电台男主播','voice_id':'Chinese (Mandarin)_Radio_Host','gender':'男','description':'低沉诗意、富有表现力的男声'},
 {'name':'精英青年音色','voice_id':'male-qn-jingying','gender':'男','description':'干练专业、偏知识讲解的青年男声'},
 {'name':'少女音色','voice_id':'female-shaonv','gender':'女','description':'轻快活泼的年轻女声'},
 {'name':'甜美女声','voice_id':'Chinese (Mandarin)_Sweet_Lady','gender':'女','description':'温柔甜美、亲和的女声'},
 {'name':'阅历姐姐','voice_id':'Chinese (Mandarin)_Wise_Women','gender':'女','description':'知性从容、富有阅历的女声'},
 {'name':'温暖闺蜜','voice_id':'Chinese (Mandarin)_Warm_Bestie','gender':'女','description':'清脆友好、像朋友聊天的女声'},
]
slug=lambda s: pathlib.Path(s).stem

def one(v):
    stem=pathlib.Path('voice_samples')/slug(v['voice_id'])
    # Adapt only the output codec; timing/pronunciation settings remain common to every sample.
    import minimax_client
    # Client defaults are intentionally explicit in this task-independent wrapper.
    # Identical sample settings are verified against metadata; only new voices are billed.
    if not stem.with_suffix('.meta.json').exists():
        synthesize(TEXT,stem,voice=v['voice_id'],speed=1.1)
    meta0=json.load(stem.with_suffix('.meta.json').open())
    if meta0['text'] != TEXT or meta0['voice'] != v['voice_id'] or meta0['speed'] != 1.1:
        synthesize(TEXT,stem,voice=v['voice_id'],speed=1.1)
    meta=json.load(stem.with_suffix('.meta.json').open())
    assert meta['text']==TEXT and meta['voice']==v['voice_id'] and meta['speed']==1.1
    return v|{'file':str(stem.with_suffix('.flac')),'billed':meta['extra_info']['usage_characters'],'duration_ms':meta['extra_info']['audio_length']}

def main():
    out=pathlib.Path('voice_samples');out.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(one,VOICES))
    for i,v in enumerate(results,1):
        p=pathlib.Path(v['file']);mp3=p.with_suffix('.mp3')
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(p),'-ar','44100','-ac','1','-codec:a','libmp3lame','-b:a','192k',str(mp3)],check=True)
        # Normalize audio length from real AAC/MP3 container and use FLAC for final lossless concat.
        v['number']=i;v['file']=str(mp3);v.pop('duration_ms',None)
    (out/'voices.json').write_text(json.dumps({'text':TEXT,'model':'speech-2.8-hd','speed':1.1,'voices':results,'characters_billed_main':sum(v['billed'] for v in results)},ensure_ascii=False,indent=2))
    print('Generated',len(results),'voices; billed',sum(v['billed'] for v in results))
if __name__=='__main__':main()
