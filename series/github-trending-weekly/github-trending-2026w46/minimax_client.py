"""MiniMax TTS client. API key is read at runtime; no secrets in code or logs."""
import json, os, pathlib, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent
BASE_URL = 'https://api.minimaxi.com'
KEY_PATH = pathlib.Path('/home/box/.config/minimax/api_key')
MODEL = 'speech-2.8-hd'
VOICE = 'male-qn-jingying'
SPEED = 1.1
TONES_ALL = [
    '重新/(chong2)(xin1)', '执行/(zhi2)(xing2)', '长成/(zhang3)(cheng2)', '重放/(chong2)(fang4)', '重跑/(chong2)(pao3)',
    '还是/(hai2)(shi4)', '还有/(hai2)(you3)', '还没/(hai2)(mei2)', '还能/(hai2)(neng2)', '还把/(hai2)(ba3)',
    '只能/(zhi3)(neng2)', '只提/(zhi3)(ti2)', '只是/(zhi3)(shi4)', '只占/(zhi3)(zhan4)', '只发/(zhi3)(fa1)',
    '更新/(geng1)(xin1)', '差哪个/(cha4)(na3)(ge4)', '差不多/(cha4)(bu4)(duo1)', '供应链/(gong1)(ying4)(lian4)',
    '少记/(shao3)(ji4)', '准确率/(zhun3)(que4)(lv4)', '得拿/(dei3)(na2)', '调试/(tiao2)(shi4)', '调度/(diao4)(du4)',
    '薄入口/(bo2)(ru4)(kou3)', '命令行/(ming4)(ling4)(hang2)', '卡片/(ka3)(pian4)', '加载/(jia1)(zai4)',
    '校验/(jiao4)(yan4)', '答不了/(da2)(bu4)(liao3)', '经得起/(jing1)(de5)(qi3)', '分层/(fen1)(ceng2)',
    'OpenMausBot/Open Maus Bot', 'security-audit-skill/security audit skill', 'agent-browser/agent browser',
]
def tones_for(text):
    return [t for t in TONES_ALL if t.split('/')[0] in text]
TONES = TONES_ALL
def synthesize(text, out_stem, voice=VOICE, speed=SPEED):
    out_stem=pathlib.Path(out_stem)
    payload = {
        'model': MODEL, 'text': text, 'stream': False,
        'voice_setting': {'voice_id': voice, 'speed': speed, 'vol': 1, 'pitch': 0, 'emotion': 'calm'},
        'pronunciation_dict': {'tone': tones_for(text)},
        'audio_setting': {'sample_rate': 32000, 'format': 'flac', 'channel': 1},
        'subtitle_enable': True, 'subtitle_type': 'word', 'language_boost': 'Chinese',
    }
    req=urllib.request.Request(BASE_URL+'/v1/t2a_v2',data=json.dumps(payload,ensure_ascii=False).encode(),headers={'Authorization':'Bearer '+KEY_PATH.read_text().strip(),'Content-Type':'application/json'})
    raw=None
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r: raw=r.read()
            data=json.loads(raw)
            if data.get('base_resp',{}).get('status_code') == 0: break
            raise RuntimeError(json.dumps(data.get('base_resp'),ensure_ascii=False))
        except urllib.error.HTTPError as e:
            # Response may contain only an API error, never a credential.
            msg=e.read().decode(errors='replace')
            raise RuntimeError(f'HTTP {e.code}: {msg[:1500]}') from None
        except (urllib.error.URLError, TimeoutError):
            if i==2: raise
            time.sleep(3*(i+1))
    out_stem.parent.mkdir(parents=True,exist_ok=True)
    out_stem.with_suffix('.flac').write_bytes(bytes.fromhex(data['data']['audio']))
    url=data['data'].get('subtitle_file')
    if url:
        with urllib.request.urlopen(url,timeout=60) as r: subs=r.read()
        out_stem.with_suffix('.json').write_bytes(subs)
    meta={'model':MODEL,'voice':voice,'speed':speed,'text':text,'tones':tones_for(text),'extra_info':data.get('extra_info'), 'subtitle_url_received':bool(url)}
    out_stem.with_suffix('.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print(out_stem.name, 'duration_ms',data.get('extra_info',{}).get('audio_length'),'billed',data.get('extra_info',{}).get('usage_characters'))
    return data
