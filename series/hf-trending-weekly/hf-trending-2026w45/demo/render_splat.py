"""Simple point-splat preview of an Idol 3DGS .ply (read-only parse with numpy; no repo code)."""
import numpy as np, sys, os, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
src=sys.argv[1]; outdir=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 48
os.makedirs(outdir,exist_ok=True)
raw=open(src,'rb').read(); h=raw.index(b'end_header\n')+11
d=np.frombuffer(raw[h:],dtype='<f4').reshape(-1,17)
xyz=d[:,0:3].astype(np.float64); dc=d[:,6:9]; op=1/(1+np.exp(-d[:,9])); sc=np.exp(d[:,10:13]).mean(1)
rgb=np.clip(0.5+0.28209479*dc,0,1)
keep=op>0.05; xyz,rgb,op,sc=xyz[keep],rgb[keep],op[keep],sc[keep]
c=xyz.mean(0); xyz-=c; R=np.percentile(np.linalg.norm(xyz,axis=1),99)
print('points',len(xyz),'bbox',xyz.min(0),xyz.max(0))
W=720
for i in range(n):
    a=np.pi/2+2*np.pi*i/n; el=np.deg2rad(15)
    # assume y up in 3DGS convention may be -y; try both via argv
    up=-1 if (len(sys.argv)>4 and sys.argv[4]=='flip') else 1
    Ry=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
    Rx=np.array([[1,0,0],[0,np.cos(el),-np.sin(el)],[0,np.sin(el),np.cos(el)]])
    p=xyz@Ry.T@Rx.T
    z=p[:,2]+3.2*R; f=1.9*R
    u=p[:,0]*3.2*R/z; v=-up*p[:,1]*3.2*R/z
    order=np.argsort(-z)
    s=(sc*3.2*R/z/R*0.9*W/2*72/100*2.8)**2
    s=np.clip(s,0.3,60)
    fig=plt.figure(figsize=(W/100,W/100),dpi=100); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    fig.patch.set_alpha(0)
    col=np.concatenate([rgb,op[:,None]],1)[order]
    ax.scatter(u[order]/R*0.9,v[order]/R*0.9,s=s[order],c=col,linewidths=0,marker='o')
    fig.savefig(f'{outdir}/f{i:03d}.png',transparent=True); plt.close(fig)
    if i==0: print('frame0 done')
