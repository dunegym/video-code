#!/bin/bash
cd "$(dirname "$0")"
SC=${@:-S0_Intro P4a P4b P4c P3a P3b P3c P2a P2b P2c P1a P1b P1c S6_Outro}
mkdir -p build/scenes
for S in $SC; do
  manim render -qh --fps 30 -r 1920,1080 --disable_caching -v WARNING --media_dir media_other scenes_other.py "$S" > "build/r_$S.log" 2>&1 && echo "ok $S" || { echo "FAIL $S"; tail -n 40 "build/r_$S.log"; exit 1; }
done
