"""MiniMax TTS client. API key is read at runtime; no secrets in code or logs."""
import json, os, pathlib, time, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent
BASE_URL = 'https://api.minimaxi.com'
KEY_PATH = pathlib.Path('/home/box/.config/minimax/api_key')
MODEL = 'speech-2.8-hd'
VOICE = 'male-qn-jingying'
SPEED = 1.1
TONES = [
    '重新/(chong2)(xin1)',
    '执行/(zhi2)(xing2)',
    '长成/(zhang3)(cheng2)',
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
