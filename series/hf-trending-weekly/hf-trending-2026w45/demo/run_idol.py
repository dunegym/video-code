import json,time,shutil
from gradio_client import Client,handle_file
c=Client("speridlabs/idol",verbose=False)
t0=time.time()
r=c.predict(handle_file("teapot.jpg"),"Real photo",50,3.0,3.0,42,False,"262,144",api_name="/run")
dt=time.time()-t0
print(dt,r)
p=r[0]; shutil.copy(p,"idol_teapot"+p[p.rfind('.'):])
json.dump({"space":"speridlabs/idol","input":"teapot.jpg (Wikimedia Commons, Auckland Museum, CC BY 4.0)","params":{"mode":"Real photo","steps":50,"cfg":3.0,"rescale_t":3.0,"seed":42,"gaussians":"262,144"},"secs":round(dt,1),"output_file":p,"html":r[2]},open("idol_sample.json","w"),ensure_ascii=False,indent=1)
