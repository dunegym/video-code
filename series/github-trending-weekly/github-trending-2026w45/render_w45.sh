#!/bin/bash
# 串行渲染：./render_w45.sh [场景...]
cd /workspace/github-trending-2026w45
SC=${@:-S0_Intro P5a P5b P5c P4a P4b P4c P3a P3b P3c P2a P2b P2c P1a P1b P1c S6_Outro}
for S in $SC; do .venv/bin/manim render -qh --fps 30 -r 1920,1080 --disable_caching -v WARNING --media_dir media_w45 scenes_w45.py $S > build_w45/r_$S.log 2>&1 && echo "ok $S" || { echo "FAIL $S"; tail -8 build_w45/r_$S.log; }; done
