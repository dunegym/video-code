import sys, json, shutil, time
from gradio_client import Client, handle_file
which = sys.argv[1]; t0 = time.time()
if which == "ltx":
    c = Client("Lightricks/LTX-2.5", verbose=False)
    prompt = "The yellow emoji balloon slowly drifts upward over the night city as the camera gently pushes in; city lights twinkle and a soft wind hum is heard."
    r = c.predict(prompt=prompt, image_path=handle_file("flux_sample.png"), height=768, width=768, duration_s=3.0, seed=24,
                  decoder="diffusion", auto_len=False, randomize_seed=False, do_enhance=True, api_name="/run")
    v = r[0]["video"] if isinstance(r[0], dict) else r[0]
    shutil.copy(v, "ltx_sample.mp4")
    json.dump({"space": "Lightricks/LTX-2.5", "prompt": prompt, "input_image": "flux_sample.png (FLUX 3 Klein Space output)", "enhanced": r[1], "seed": r[2], "length": r[3],
               "settings": "768x768, 3s, decoder=diffusion, prompt enhancer on"}, open("ltx_sample.json", "w"), ensure_ascii=False, indent=1)
elif which == "flint":
    c = Client("mrfakename/flint", verbose=False)
    msg = "Write a Python function that merges overlapping intervals, with a short docstring and two asserts. Keep it under 20 lines."
    r = c.predict(message=msg, system_prompt="", max_new_tokens=2048, temperature=1.0, top_p=0.95, top_k=20, api_name="/chat")
    json.dump({"space": "mrfakename/flint", "message": msg, "response": r[0], "md": r[1]}, open("flint_sample.json", "w"), ensure_ascii=False, indent=1)
print(which, "ok", round(time.time() - t0, 1))
