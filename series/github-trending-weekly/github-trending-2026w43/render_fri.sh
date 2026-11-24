#!/bin/bash
# 周五版串行渲染：./render_fri.sh [场景...]
cd /workspace/github-trending-2026w43-fri
SC=${@:-S0_Intro P3a P3b P3c P5a P5b P5c P4a P4b P4c P2a P2b P2c P1a P1b P1c S6_Outro}
for S in $SC; do .venv/bin/manim render -qh --fps 30 -r 1920,1080 --disable_caching -v WARNING --media_dir media_fri scenes_fri.py $S > build_fri/r_$S.log 2>&1 && echo "ok $S" || { echo "FAIL $S"; tail -8 build_fri/r_$S.log; }; done
