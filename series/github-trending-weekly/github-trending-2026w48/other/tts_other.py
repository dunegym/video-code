"""Per-sentence MiniMax TTS via mmx CLI with semantic inter-sentence pacing and waveform-aligned punctuation subtitle splits."""
import json
import os
import pathlib
import re
import subprocess
import sys
import numpy as np
import av

from script_other import SCENES, ORDER
from minimax_client import synthesize_sentence, tones_for, VOICE, SPEED, MODEL

ROOT = pathlib.Path(__file__).resolve().parent
os.chdir(ROOT)

LEAD = 0.25
INTER_SENT = 0.38
TAIL = 0.65
SR = 48000
AUD = pathlib.Path("audio_other")
AUD.mkdir(exist_ok=True)


def vw(s: str) -> float:
    return sum(1.0 if ord(c) > 0x2E80 else 0.55 for c in s)


def split_lines(sent: str, maxw: float = 22.0):
    chunks = [c for c in re.split(r"(?<=[，。；：？！])", sent) if c]
    lines = []
    cur = ""
    for c in chunks:
        if cur and vw(cur) >= 5 and vw(cur) + vw(c) > maxw:
            lines.append(cur)
            cur = c
        else:
            cur += c
    if cur:
        if lines and vw(cur) < 6 and vw(lines[-1]) + vw(cur) <= maxw + 4:
            lines[-1] += cur
        else:
            lines.append(cur)
    return lines


def decode_mono(flac_path: pathlib.Path):
    with av.open(str(flac_path)) as container:
        sr = container.streams.audio[0].rate
        chunks = []
        for frame in container.decode(audio=0):
            arr = frame.to_ndarray()
            if arr.ndim == 2:
                arr = arr.mean(axis=0)
            arr = arr.astype(np.float32)
            if np.max(np.abs(arr)) > 1.5:
                arr = arr / 32768.0
            chunks.append(arr)
    audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)
    return audio, sr


def trim_silence(audio: np.ndarray, sr: int, thresh: float = 0.008, pad_s: float = 0.04):
    if len(audio) == 0:
        return audio
    win = max(1, int(sr * 0.01))
    n = len(audio) // win
    if n == 0:
        return audio
    rms = np.sqrt(np.mean(audio[: n * win].reshape(n, win) ** 2, axis=1))
    nz = np.where(rms > thresh)[0]
    if len(nz) == 0:
        return audio
    s = max(0, int(nz[0] * win - pad_s * sr))
    e = min(len(audio), int((nz[-1] + 1) * win + pad_s * sr))
    return audio[s:e]


def find_pause_split(audio: np.ndarray, sr: int, target_frac: float, window_frac: float = 0.16) -> float:
    dur = len(audio) / sr
    if dur < 0.8:
        return dur * target_frac
    win = int(sr * 0.025)
    hop = int(sr * 0.01)
    if len(audio) <= win:
        return dur * target_frac
    frames = np.lib.stride_tricks.sliding_window_view(audio, win)[::hop]
    rms = np.sqrt(np.mean(frames ** 2, axis=1))
    times = (np.arange(len(rms)) * hop + win / 2) / sr
    lo = max(0.15, dur * (target_frac - window_frac))
    hi = min(dur - 0.15, dur * (target_frac + window_frac))
    mask = (times >= lo) & (times <= hi)
    if not np.any(mask):
        return dur * target_frac
    idxs = np.where(mask)[0]
    scores = rms[idxs] + 0.015 * np.abs(times[idxs] - dur * target_frac)
    best = idxs[int(np.argmin(scores))]
    return float(times[best])


def write_wav_stereo_48k(mono_audio: np.ndarray, in_sr: int, out_wav: pathlib.Path):
    tmp_raw = out_wav.with_suffix(".tmp.wav")
    pcm = np.clip(mono_audio, -1.0, 1.0)
    pcm16 = (pcm * 32767.0).astype("<i2")
    import wave
    with wave.open(str(tmp_raw), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(in_sr)
        wf.writeframes(pcm16.tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(tmp_raw), "-ar", str(SR), "-ac", "2", str(out_wav)],
        check=True,
    )
    tmp_raw.unlink(missing_ok=True)


def do_scene(scene: str, sents: list, force: bool = False):
    cues = []
    subs = []
    segs = []
    sr_ref = 32000
    t = LEAD
    segs.append(np.zeros(int(LEAD * sr_ref), dtype=np.float32))
    scene_tones = []

    for idx, sent in enumerate(sents):
        stem = AUD / f"{scene}_s{idx}"
        flac = stem.with_suffix(".flac")
        meta_p = stem.with_suffix(".meta.json")
        tones = tones_for(sent)
        scene_tones.extend(tones)

        cached = flac.exists() and meta_p.exists()
        if cached:
            m = json.loads(meta_p.read_text(encoding="utf-8"))
            cached = (
                m.get("text") == sent
                and m.get("tones") == tones
                and m.get("voice") == VOICE
                and m.get("speed") == SPEED
                and m.get("model") == MODEL
            )
        if force or not cached:
            info, _ = synthesize_sentence(sent, flac)
            meta = {"model": MODEL, "voice": VOICE, "speed": SPEED, "text": sent, "tones": tones, "info": info}
            meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  synth {stem.name} ({len(sent)} chars)")
        else:
            print(f"  cached {stem.name}")

        audio, sr = decode_mono(flac)
        sr_ref = sr
        audio = trim_silence(audio, sr)
        dur = len(audio) / sr

        s_start = t
        s_end = t + dur
        cues.append({"text": sent, "start": round(s_start, 3), "end": round(s_end, 3)})

        lines = split_lines(sent)
        if len(lines) == 1:
            subs.append({"text": lines[0].strip().rstrip("，。；："), "start": round(s_start, 3), "end": round(s_end, 3)})
        else:
            weights = [max(1.0, vw(l)) for l in lines]
            tot_w = sum(weights)
            cum = 0.0
            cuts = [0.0]
            for w in weights[:-1]:
                cum += w
                cuts.append(find_pause_split(audio, sr, cum / tot_w))
            cuts.append(dur)
            for li, ltxt in enumerate(lines):
                subs.append({
                    "text": ltxt.strip().rstrip("，。；："),
                    "start": round(s_start + cuts[li], 3),
                    "end": round(s_start + cuts[li + 1], 3),
                })

        segs.append(audio)
        t = s_end
        if idx < len(sents) - 1:
            segs.append(np.zeros(int(INTER_SENT * sr_ref), dtype=np.float32))
            t += INTER_SENT

    segs.append(np.zeros(int(TAIL * sr_ref), dtype=np.float32))
    total = round(t + TAIL, 3)

    for x, y in zip(subs, subs[1:]):
        if y["start"] - x["end"] < 0.45:
            x["end"] = y["start"]

    full_mono = np.concatenate(segs)
    write_wav_stereo_48k(full_mono, sr_ref, AUD / f"{scene}.wav")
    print(f"SCENE {scene}: {total:.2f}s ({len(sents)} sents, {len(subs)} subs)")
    return {"total": total, "cues": cues, "subs": subs, "tones": sorted(set(scene_tones))}


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    path = pathlib.Path("timing_other.json")
    tm = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for sc in (args or ORDER):
        tm[sc] = do_scene(sc, SCENES[sc], force)
    tm = {k: tm[k] for k in ORDER if k in tm}
    path.write_text(json.dumps(tm, ensure_ascii=False, indent=1), encoding="utf-8")
    pathlib.Path("build").mkdir(exist_ok=True)
    summary = {
        "provider": "MiniMax CN via mmx CLI",
        "model": MODEL,
        "voice": VOICE,
        "speed": SPEED,
        "total_duration_s": round(sum(v["total"] for v in tm.values()), 2),
        "scenes": len(tm),
    }
    pathlib.Path("build/tts_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TOTAL OTHER:", summary["total_duration_s"], "s across", len(tm), "scenes")


if __name__ == "__main__":
    main()
