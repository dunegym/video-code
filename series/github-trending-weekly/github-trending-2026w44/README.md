# GitHub 本周热榜 Top 5 · 2026 第 44 周（10 月 30 日）

成片：github_trending_top5_w44.mp4（1080p30，约 5:18）；字幕：github_trending_top5_w44.srt（已烧录）；封面：cover.png / cover_4x3.png / cover_3x4.png；简介：description.txt；素材：assets.md。

流水线（沿用 w43-fri）：
1. script_w44.py 文案 → `.venv/bin/python tts_w44.py [场景…]`（edge-tts zh-CN-XiaoxiaoNeural，+30%）→ audio_w44/、timing_w44.json
2. `./render_w44.sh [场景…]`（Manim，scenes_w44.py）→ `.venv/bin/python peek.py 场景` 抽帧检查
3. `.venv/bin/python assemble_w44.py`（GIF 叠加、ASS 字幕 60px、响度归一）→ `checkcut_w44.py` 检查成片
4. `.venv/bin/python make_covers.py .`（cover.json；16:9 卡片用 descs_wide 短描述）
