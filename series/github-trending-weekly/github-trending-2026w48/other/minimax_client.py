"""MiniMax TTS client via logged-in mmx CLI. No secrets or key paths in code or logs."""
import json
import pathlib
import shutil
import subprocess
import time

MODEL = "speech-2.8-hd"
VOICE = "male-qn-jingying"
SPEED = 1.1

TONES_ALL = [
    "重新/(chong2)(xin1)", "执行/(zhi2)(xing2)", "长成/(zhang3)(cheng2)", "重放/(chong2)(fang4)", "重跑/(chong2)(pao3)",
    "重排/(chong2)(pai2)", "重做/(chong2)(zuo4)",
    "还是/(hai2)(shi4)", "还有/(hai2)(you3)", "还没/(hai2)(mei2)", "还能/(hai2)(neng2)", "还把/(hai2)(ba3)",
    "还在/(hai2)(zai4)", "还剩/(hai2)(sheng4)", "还要/(hai2)(yao4)", "还支持/(hai2)(zhi1)(chi2)", "还带来/(hai2)(dai4)(lai2)",
    "只能/(zhi3)(neng2)", "只提/(zhi3)(ti2)", "只是/(zhi3)(shi4)", "只占/(zhi3)(zhan4)", "只发/(zhi3)(fa1)",
    "只有/(zhi3)(you3)", "只负责/(zhi3)(fu4)(ze2)", "只剩/(zhi3)(sheng4)", "只留/(zhi3)(liu2)",
    "更新/(geng1)(xin1)", "差哪个/(cha4)(na3)(ge4)", "差不多/(cha4)(bu4)(duo1)", "差距/(cha1)(ju4)",
    "得拿/(dei3)(na2)", "得把/(dei3)(ba3)", "都得/(dou1)(dei3)", "得自己/(dei3)(zi4)(ji3)",
    "调试/(tiao2)(shi4)", "调度/(diao4)(du4)", "调过/(tiao2)(guo4)",
    "卡片/(ka3)(pian4)", "卡死/(ka3)(si3)", "卡住/(ka3)(zhu4)", "加载/(jia1)(zai4)", "侧载/(ce4)(zai3)",
    "校验/(jiao4)(yan4)", "分层/(fen1)(ceng2)", "行里/(hang2)(li3)", "银行/(yin2)(hang2)",
    "一行/(yi4)(hang2)", "落下/(luo4)(xia4)", "倒手/(dao3)(shou3)", "铺出/(pu1)(chu1)",
    "数量/(shu4)(liang4)", "数里/(shu4)(li3)", "星数/(xing1)(shu4)",
    "回答/(hui2)(da2)", "答不了/(da2)(bu4)(liao3)",
    "朝上/(chao2)(shang4)", "种子/(zhong3)(zi5)", "一种/(yi4)(zhong3)",
    "模型/(mo2)(xing2)", "模块/(mo2)(kuai4)",
    "Plannotator/Plan otator", "Open Code Review/Open Code Review",
    "modern-web-guidance-src/modern web guidance",
    "modern-web-guidance/modern web guidance",
    "stitch-skills/stitch skills", "Stitch/Stitch",
    "Google Labs/Google Labs", "Google Chrome/Google Chrome",
    "n8n/n eight n", "Nod/Nod", "React/React", "React Native/React Native",
    "Linux/Linux", "Astryx/Astryx", "HermesEnabler/Hermes Enabler",
    "watchOS/watch OS", "Clocky/Clocky", "Univer/Univer",
    "Sure/Sure", "Maybe Finance/Maybe Finance", "Maybe/Maybe",
    "dream-num/dream num", "we-promise/we promise", "pookjw/pook j w",
    "Gester/Gester", "Meta/Meta",
]


def tones_for(text: str):
    return [t for t in TONES_ALL if t.split("/")[0] in text]


def _mmx_bin():
    return shutil.which("mmx.cmd") or shutil.which("mmx") or "mmx"


def synthesize_sentence(text: str, out_flac: pathlib.Path, voice: str = VOICE, speed: float = SPEED):
    out_flac = pathlib.Path(out_flac)
    out_flac.parent.mkdir(parents=True, exist_ok=True)
    tones = tones_for(text)
    cmd = [
        _mmx_bin(), "speech", "synthesize",
        "--model", MODEL,
        "--voice", voice,
        "--speed", str(speed),
        "--emotion", "calm",
        "--format", "flac",
        "--sample-rate", "32000",
        "--channels", "1",
        "--language", "Chinese",
        "--text-file", "-",
        "--out", str(out_flac),
        "--output", "json",
        "--no-color",
    ]
    for rule in tones:
        cmd.extend(["--pronunciation", rule])

    last_err = None
    for attempt in range(3):
        proc = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
        )
        if proc.returncode == 0 and out_flac.exists() and out_flac.stat().st_size > 100:
            info = {}
            for line in proc.stdout.decode("utf-8", errors="replace").splitlines():
                line = line.strip()
                if line.startswith("{"):
                    try:
                        info.update(json.loads(line))
                    except Exception:
                        pass
            return info, tones
        last_err = proc.stderr.decode("utf-8", errors="replace") + "\n" + proc.stdout.decode("utf-8", errors="replace")
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"mmx speech synthesize failed after 3 attempts:\n{last_err[:1200]}")
