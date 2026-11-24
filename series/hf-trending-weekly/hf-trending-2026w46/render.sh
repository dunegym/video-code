#!/bin/bash
# 串行渲染：./render.sh [场景...]
cd /workspace/hf-trending-2026w46
SC=${@:-S0_Intro P1a P1b P2a P2b P3a P3b P4a P4b P5a P5b S6_Outro}
mkdir -p build
for S in $SC; do .venv/bin/manim render -qh --fps 30 -r 1920,1080 --disable_caching -v WARNING --media_dir media scenes.py $S > build/$S.log 2>&1 && echo "ok $S" || { echo "FAIL $S"; tail -12 build/$S.log; }; done
