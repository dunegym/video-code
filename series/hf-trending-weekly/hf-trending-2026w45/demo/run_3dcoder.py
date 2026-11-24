import json,time
from gradio_client import Client
c=Client("akhaliq/qwen35-3d-coder-studio",verbose=False)
SYS="Use only the Three.js core ES module from https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.module.min.js. Do not import addons or legacy examples/js paths; implement any camera controls directly inside the HTML."
prompt="Please create one self-contained HTML file with Three.js from cdnjs showing a small lighthouse on a rocky island with a wooden pier and a sailboat. Render it as a deliberate 3D voxel model built from visible cubic blocks, with clear depth, readable silhouettes, and solid spatial relationships."
out={"space":"akhaliq/qwen35-3d-coder-studio","system_hint":SYS,"prompt":prompt,"runs":[]}
for mt in [int(x) for x in __import__("sys").argv[1:]]:
    t0=time.time()
    try: r=c.predict(SYS+"\n\n"+prompt,False,1729,False,mt,None,api_name="/generate")
    except Exception as e: r={"error":repr(e)[:800]}
    out["runs"].append({"max_tokens":mt,"secs":round(time.time()-t0,1),"result":r})
    print(mt,time.time()-t0,str(r)[:500])
json.dump(out,open("3dcoder_sample.json","w"),ensure_ascii=False,indent=1)
