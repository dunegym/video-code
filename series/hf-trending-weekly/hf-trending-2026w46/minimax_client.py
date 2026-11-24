"""MiniMax TTS client. API key is read at runtime; no secrets in code or logs."""
import json, os, pathlib, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent
BASE_URL = 'https://api.minimaxi.com'
KEY_PATH = pathlib.Path('/home/box/.config/minimax/api_key')
MODEL = 'speech-2.8-hd'
VOICE = 'male-qn-jingying'
SPEED = 1.1
TONES = [
    '重新/(chong2)(xin1)', '执行/(zhi2)(xing2)', '长成/(zhang3)(cheng2)', '最长/(zui4)(chang2)', '重复/(chong2)(fu4)',
    '调整/(tiao2)(zheng3)', '背面/(bei4)(mian4)', '背包/(bei1)(bao1)', '一小撮/(yi4)(xiao3)(cuo1)', '差一截/(cha4)(yi4)(jie2)',
    '转着/(zhuan4)(zhe5)', '转了一圈/(zhuan4)(le5)(yi2)(quan1)', '卡在/(qia3)(zai4)', '塞进/(sai1)(jin4)', '还得/(hai2)(dei3)',
    '占便宜/(zhan4)(pian2)(yi5)', '数量级/(shu4)(liang4)(ji2)', '打个折扣/(da3)(ge4)(zhe2)(kou4)', '落在/(luo4)(zai4)', '落后/(luo4)(hou4)',
    '冲上/(chong1)(shang4)', '给多/(gei3)(duo1)', '量化/(liang4)(hua4)', '一大截/(yi2)(da4)(jie2)', '大得多/(da4)(de5)(duo1)',
    'CCORE/C core', 'Speridlabs/Sperid labs',
    '打折扣/(da3)(zhe2)(kou4)', '占了/(zhan4)(le5)', '偏长/(pian1)(chang2)',
    '当裁判/(dang4)(cai2)(pan4)', '看成/(kan4)(cheng2)',
    'Jackrong/Jack rong', 'Arete/阿瑞忒', 'Nous Research/Nous Research',
]

def synthesize(text, out_stem, voice=VOICE, speed=SPEED):
    out_stem=pathlib.Path(out_stem)
    payload = {
        'model': MODEL, 'text': text, 'stream': False,
        'voice_setting': {'voice_id': voice, 'speed': speed, 'vol': 1, 'pitch': 0, 'emotion': 'calm'},
        'pronunciation_dict': {'tone': TONES},
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
    meta={'model':MODEL,'voice':voice,'speed':speed,'text':text,'extra_info':data.get('extra_info'), 'subtitle_url_received':bool(url)}
    out_stem.with_suffix('.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print(out_stem.name, 'duration_ms',data.get('extra_info',{}).get('audio_length'),'billed',data.get('extra_info',{}).get('usage_characters'))
    return data
