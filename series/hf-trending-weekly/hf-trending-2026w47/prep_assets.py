"""确认封面和画面所用头像、示例图已在 assets/proc。"""
from pathlib import Path
need = [
    "av_inkling.png", "av_haru.png", "av_pi.png", "av_sentinel.png", "av_ltx.png",
    "pi_card.png", "pi_traj.png",
]
missing = [n for n in need if not Path("assets/proc", n).exists()]
if missing:
    raise SystemExit(f"missing proc assets: {missing}")
print("ok", len(need), "proc assets")
