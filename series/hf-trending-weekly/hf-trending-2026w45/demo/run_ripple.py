import json,time
from gradio_client import Client
c=Client("akhaliq/ripple-65b-zerogpu",verbose=False)
qs=["Write a single bash one-liner that finds the 5 largest files under the current directory (recursively) and prints their sizes in human-readable form. Then explain each part in one short line.",
    "A train leaves at 14:05 and arrives at 17:50 the same day, but the clock at the destination is one hour behind the origin. How long was the trip? Answer briefly."]
out={"space":"akhaliq/ripple-65b-zerogpu","runs":[]}
for q in qs:
    t0=time.time()
    try: r=c.predict(q,"",768,api_name="/ask")
    except Exception as e: r="ERROR "+repr(e)[:800]
    out["runs"].append({"prompt":q,"secs":round(time.time()-t0,1),"output":r}); print(round(time.time()-t0,1),r[:1500],'\n----')
json.dump(out,open("ripple_sample.json","w"),ensure_ascii=False,indent=1)
