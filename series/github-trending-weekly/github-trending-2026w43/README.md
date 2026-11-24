# GitHub 本周热门 Top 5：周五更新版（2026-10-23 快照）
榜单：https://github.com/trending?since=weekly，于 2026-10-23 18:09（UTC+8）抓取，原始页面存为 raw/trending_2026-10-23.html。
与 10-22 的 data.json 相比，前五名还是这五个项目，但页面顺序变了：
#1 morluto/rea · #2 anthropics/claude-plugins-official · #3 ruvnet/ruflo（原 #4）· #4 android/skills（原 #5）· #5 K-Dense-AI/scientific-agent-skills（原 #3）。

成片：github_trending_top5_fri.mp4（1080p30，约 4:59）。字幕：github_trending_top5_fri.srt（与 subtitles_fri.srt 相同），烧录版本为 subtitles_fri.ass。

## 流程（复用 v5 代码，从 ../github-trending-2026w43 复制而来）
script_fri.py → tts_fri.py → scenes_fri.py → ./render_fri.sh → assemble_fri.py → checkcut_fri.py
- script_fri.py：旁白，ORDER 已按新名次排好。场景键仍按项目命名，与名次无关：P1*=rea，P2*=plugins，P4*=ruflo，P5*=android，P3*=science。REUSE 中的 5 个 b 段（设计/分布）旁白没变，直接沿用 v5 的音频和时间轴（audio_v5/、timing_v5.json）。
- tts_fri.py：用 edge-tts 的 zh-CN-XiaoxiaoNeural 合成，语速 +27%，每段旁白整段合成。产物为 audio_fri/ 和 timing_fri.json。
- scenes_fri.py：名次和星数都从 data.json 读取，data.json 已更新为当天数据。
- ./render_fri.sh：17 个场景逐个串行渲染，输出到 media_fri/，日志在 build_fri/r_*.log。
- assemble_fri.py：叠加 GIF（叠加参数在 build_fri/ov_*.json），再烧录 60px 字幕并做响度标准化。
- checkcut_fri.py：每个场景抽 4 帧，拼成 build_fri/cut_*.png；结尾帧的大图在 build_fri/full/。
- 环境：.venv 是本目录新建的虚拟环境，装有 manim 0.22.0 和 edge-tts，系统另装了 libcairo2-dev、libpango1.0-dev。旧目录的 .venv 链接已失效。

## 相对 v5 的改动
- 每个项目的名次、本周新增星数和总星数都换成 10-23 的数据，片头头像和片尾回顾也按新顺序排列。
- 片头不再播报倒数（去掉“从第五名开始”），直接接到第五名。
- 删掉 5 处“启示”框和“启示：”旁白，改成顺着分析说出来的一句话，或者一个小提示：P3c 的注意事项、P5c 的“迁移规则来自官方指南”、P4c 的权限与审计在外壳层、P2c 的官方信任提醒、P1c 的官方安全说明。
- P1a 去掉了 `npx` 安装命令，换成一行小字注明星数增速，以页面数据为准。P3a 加了一行小字，说明名次按页面顺序，而这个项目的本周新增星数高于第三、四名。
- Hacker News 的数据更新为 814 points / 340 comments，旁白改为“800多分”。
