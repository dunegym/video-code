import json, time
from gradio_client import Client, handle_file
c = Client("hugging-apps/nemotron-3-5-transcribe", verbose=False)
out = {"space": "hugging-apps/nemotron-3-5-transcribe", "audio": "demo/nemotron_test.wav (edge-tts 合成的双人英文对话，含口头禅与重复)", "runs": []}
for preset in ["Verbatim transcription", "Clean transcript", "Speaker-attributed transcription"]:
    ins, think, temp = c.predict(preset, api_name="/_apply_preset")
    t0 = time.time()
    try:
        r = c.predict(handle_file("nemotron_test.wav"), ins, think, temp, 1024, api_name="/transcribe")
    except Exception as e:
        r = "ERROR " + repr(e)[:300]
    out["runs"].append({"preset": preset, "instruction": ins, "reasoning": think, "temperature": temp, "output": r, "secs": round(time.time() - t0, 1)})
    print(preset, "\n", r, "\n")
ins = "Please translate the given speech to Chinese."
r = c.predict(handle_file("nemotron_test.wav"), ins, False, 0.0, 1024, api_name="/transcribe")
out["runs"].append({"preset": "custom translate", "instruction": ins, "output": r}); print(r)
json.dump(out, open("nemotron_sample.json", "w"), ensure_ascii=False, indent=1)
