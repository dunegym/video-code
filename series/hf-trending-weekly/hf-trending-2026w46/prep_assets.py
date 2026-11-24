"""确认封面和画面所用头像、示例图已在 assets/proc。"""
from pathlib import Path
need = [
    "av_jackrong.png", "av_h3img.png", "av_ltx.png", "av_qwen.png", "av_arete.png",
    "h3_hero.png", "h3_edit_map.png", "h3_edit_multi.png", "h3_edit_render.png",
    "h3_text.png", "h3_scene.png", "h3_photo.png", "h3_art.png", "h3_char.png",
]
missing = [n for n in need if not Path("assets/proc", n).exists()]
if missing:
    raise SystemExit(f"missing proc assets: {missing}")
print("ok", len(need), "proc assets")
