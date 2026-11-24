import asyncio, edge_tts, subprocess
lines = [("en-US-GuyNeural", "Um, so, okay. The, uh, the launch review is moved to Thursday, October twenty-ninth, at three thirty."),
         ("en-US-JennyNeural", "Wait, Thursday? I thought, I thought it was Friday. Do we still need the, um, the Kubernetes migration plan?"),
         ("en-US-GuyNeural", "Yeah. Priya will send the plan, and the budget is about twelve thousand five hundred dollars.")]
async def main():
    fs = []
    for i, (v, t) in enumerate(lines):
        f = f"_l{i}.mp3"; await edge_tts.Communicate(t, v, rate="+0%").save(f); fs.append(f)
    inputs = sum([["-i", f] for f in fs], [])
    n = len(fs)
    fc = "".join(f"[{i}:a]aresample=16000,apad=pad_dur=0.6[a{i}];" for i in range(n)) + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[o]", "-ac", "1", "-ar", "16000", "nemotron_test.wav"], check=True)
asyncio.run(main())
