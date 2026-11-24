import json, time
from gradio_client import Client
c = Client("akhaliq/lfm3-studio", verbose=False)
text = "Um, so okay, the launch review is moved to Thursday, October twenty ninth at three thirty. Wait, Thursday? I thought it was Friday. Do we still need the Kubernetes migration plan? Yeah, Priya will send the plan and the budget is about twelve thousand five hundred dollars."
fields = "meeting, date, time, owner, deliverable, budget_usd"
out = {"space": "akhaliq/lfm3-studio", "runs": []}
t0 = time.time()
try: r = c.predict(text, fields, 512, 0, api_name="/extract")
except Exception as e: r = "ERROR " + repr(e)[:400]
out["runs"].append({"endpoint": "/extract", "text": text, "fields": fields, "output": r, "secs": round(time.time() - t0, 1)}); print(json.dumps(r, ensure_ascii=False, indent=1)[:3000])
json.dump(out, open("lfm3_sample.json", "w"), ensure_ascii=False, indent=1)
