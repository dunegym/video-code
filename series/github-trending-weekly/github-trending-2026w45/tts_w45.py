"""逐场景整段合成旁白（edge-tts），用 WordBoundary 事件求出每句与每行字幕的时间。"""
import asyncio, json, os, re, subprocess
import edge_tts
from script_w45 import SCENES, ORDER, REUSE
import shutil
REDO = [s for s in ORDER if s not in REUSE]
os.chdir(os.path.dirname(os.path.abspath(__file__)))
VOICE, RATE = "zh-CN-XiaoxiaoNeural", "+30%"
LEAD, TAIL = 0.35, 0.75          # 场景开头留白 / 结尾留白（含淡出）
PUNCT = "，。；：、？！“”（）"

def vw(s):  # 视觉宽度：中文 1，拉丁字符约 0.55
    return sum(1 if ord(c) > 0x2e80 else 0.55 for c in s)

def split_lines(sent, maxw=22):
    """字幕断行：只在 ，。；：？！ 处断开（不在“、”和列举中间断），单行视觉宽度 ≤ maxw"""
    chunks = [c for c in re.split(r"(?<=[，。；：？！])", sent) if c]
    lines, cur = [], ""
    for c in chunks:
        if cur and vw(cur) >= 5 and vw(cur) + vw(c) > maxw:
            lines.append(cur); cur = c
        else:
            cur += c
    if cur:
        if lines and vw(cur) < 6 and vw(lines[-1]) + vw(cur) <= maxw + 4: lines[-1] += cur
        else: lines.append(cur)
    out = []
    for l in lines:                      # 仍过长（极少）：在空格或中文处切，不切断英文单词
        while vw(l) > maxw + 4:
            cut = len(l) // 2
            while cut > 4 and re.match(r"[A-Za-z0-9./_-]", l[cut]) and re.match(r"[A-Za-z0-9./_-]", l[cut - 1]):
                cut -= 1
            out.append(l[:cut]); l = l[cut:]
        out.append(l)
    return out

async def synth(scene, sents):
    text = "".join(sents)
    mp3 = f"audio_w45/{scene}.mp3"
    words = []
    comm = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    with open(mp3, "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
    # 字符位置 → 时间
    cstart, cend = [None] * len(text), [None] * len(text)
    cur = 0
    for s, e, w in words:
        i = text.find(w, cur)
        if i < 0: continue
        for k in range(i, i + len(w)): cstart[k], cend[k] = s, e
        cur = i + len(w)
    def span(a, b):   # text[a:b] 的起止时间
        ss = [cstart[k] for k in range(a, b) if cstart[k] is not None]
        ee = [cend[k] for k in range(a, b) if cend[k] is not None]
        return (min(ss), max(ee)) if ss else (None, None)
    cues, subs, pos = [], [], 0
    for sent in sents:
        a, b = pos, pos + len(sent); pos = b
        s, e = span(a, b)
        cues.append({"text": sent, "start": round(s + LEAD, 3), "end": round(e + LEAD, 3)})
        lp = a
        for line in split_lines(sent):
            s2, e2 = span(lp, lp + len(line)); lp += len(line)
            if s2 is not None:
                subs.append({"text": line.strip().rstrip("，。；："), "start": round(s2 + LEAD, 3), "end": round(e2 + LEAD, 3)})
    # 字幕首尾相接（消除闪烁），但不跨越超过 0.6 s 的停顿
    for x, y in zip(subs, subs[1:]):
        if y["start"] - x["end"] < 0.6: x["end"] = y["start"]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3]))
    total = round(LEAD + dur + TAIL, 3)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp3, "-af", f"adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad,atrim=0:{total}",
                    "-ar", "48000", "-ac", "2", f"audio_w45/{scene}.wav"], check=True)
    return {"total": total, "cues": cues, "subs": subs}

async def main():
    import sys
    timing = json.load(open("timing_w45.json")) if os.path.exists("timing_w45.json") else {}
    redo = sys.argv[1:] or REDO
    for sc in redo:
        sents = SCENES[sc]
        for attempt in range(4):
            try:
                timing[sc] = await synth(sc, sents); break
            except Exception as e:
                print("retry", sc, type(e).__name__); await asyncio.sleep(3)
        else:
            raise SystemExit("TTS failed: " + sc)
        print(sc, timing[sc]["total"], [c["start"] for c in timing[sc]["cues"]])
    json.dump(timing, open("timing_w45.json", "w"), ensure_ascii=False, indent=1)
    timing = {k: timing[k] for k in ORDER}; json.dump(timing, open("timing_w45.json", "w"), ensure_ascii=False, indent=1)
    print("TOTAL", round(sum(v["total"] for v in timing.values()), 2))
if __name__ == "__main__":
    asyncio.run(main())
