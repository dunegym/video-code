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
    '重排/(chong2)(pai2)', '重做/(chong2)(zuo4)',
    '还是/(hai2)(shi4)', '还有/(hai2)(you3)', '还没/(hai2)(mei2)', '还能/(hai2)(neng2)', '还把/(hai2)(ba3)',
    '还在/(hai2)(zai4)', '还剩/(hai2)(sheng4)', '还要/(hai2)(yao4)',
    '只能/(zhi3)(neng2)', '只提/(zhi3)(ti2)', '只是/(zhi3)(shi4)', '只占/(zhi3)(zhan4)', '只发/(zhi3)(fa1)',
    '只有/(zhi3)(you3)', '只负责/(zhi3)(fu4)(ze2)', '只剩/(zhi3)(sheng4)',
    '更新/(geng1)(xin1)', '差哪个/(cha4)(na3)(ge4)', '差不多/(cha4)(bu4)(duo1)', '差距/(cha1)(ju4)',
    '得拿/(dei3)(na2)', '得把/(dei3)(ba3)', '都得/(dou1)(dei3)', '得自己/(dei3)(zi4)(ji3)',
    '调试/(tiao2)(shi4)', '调度/(diao4)(du4)', '调过/(tiao2)(guo4)',
    '卡片/(ka3)(pian4)', '卡死/(ka3)(si3)', '加载/(jia1)(zai4)', '侧载/(ce4)(zai3)',
    '校验/(jiao4)(yan4)', '分层/(fen1)(ceng2)', '行里/(hang2)(li3)', '银行/(yin2)(hang2)',
    '一行/(yi4)(hang2)', '落下/(luo4)(xia4)', '倒手/(dao3)(shou3)', '铺出/(pu1)(chu1)',
    '数量/(shu4)(liang4)', '数里/(shu4)(li3)', '星数/(xing1)(shu4)',
    '回答/(hui2)(da2)', '答不了/(da2)(bu4)(liao3)',
    '朝上/(chao2)(shang4)', '种子/(zhong3)(zi5)', '一种/(yi4)(zhong3)',
    '模型/(mo2)(xing2)', '模块/(mo2)(kuai4)',
    'Plannotator/Plan otator', 'last30days-skill/last thirty days skill',
    'last30days/last thirty days', 'Open Code Review/Open Code Review',
    'modern-web-guidance-src/modern web guidance',
    'modern-web-guidance/modern web guidance',
    'stitch-skills/stitch skills', 'Stitch/Stitch',
    'mvanhorn/M Van Horn', 'Google Labs/Google Labs',
    'Astryx/Astryx', 'HermesEnabler/Hermes Enabler',
    'watchOS/watch OS', 'Clocky/Clocky', 'Univer/Univer',
    'Sure/Sure', 'Maybe Finance/Maybe Finance',
    'dream-num/dream num', 'we-promise/we promise', 'pookjw/pook j w',
    'Gester/Gester', 'Meta/Meta',

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
