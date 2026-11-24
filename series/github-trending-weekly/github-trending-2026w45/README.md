# GitHub 本周热榜 Top 5 · 2026 第 45 周（11 月 6 日）

成片：`github_trending_top5_w45.mp4`（1080p30）；字幕：`github_trending_top5_w45.srt`（已烧录）；封面：`cover.png` / `cover_4x3.png` / `cover_3x4.png`；简介：`description.txt`；素材：`assets.md`。

流水线（沿用 w44）：
1. `script_w45.py` → `.venv/bin/python tts_w45.py` → `audio_w45/`、`timing_w45.json`
2. `./render_w45.sh`（Manim，`scenes_w45.py`）→ `.venv/bin/python peek.py 场景`
3. `.venv/bin/python assemble_w45.py` → `checkcut_w45.py`
4. `.venv/bin/python make_covers.py .`
