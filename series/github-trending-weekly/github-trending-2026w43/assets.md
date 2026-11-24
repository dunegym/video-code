# v2 素材清单与许可（github_trending_top5_v2.mp4）

所有借用素材在画面上都有来源字幕。v2 没有加背景音乐，因为没有确认到 CC0 许可的曲目。

| 文件 (assets/) | 用在 | 原始地址 | 许可 |
|---|---|---|---|
| rea_flow.png（由 rea_flow.svg 转出） | P1b 官方调查流程图 | https://github.com/morluto/rea/blob/main/website/public/assets/figures/rea-investigation-flow.svg | MIT（morluto/rea） |
| rea_hopper.png | P1c Hopper 截图 | https://github.com/morluto/rea/blob/main/docs/assets/rea-hopper-analysis.png | MIT |
| rea_showcases.png | P1a 案例插图 | morluto/rea README 中的 showcase 图 | MIT |
| ruflo_capabilities.png | P4a 横幅 | ruvnet/ruflo README 资源（docs/assets） | MIT（ruvnet/ruflo） |
| ruflo_learning.png | P4b 学习循环 | ruvnet/ruflo README（“Experience becomes context”） | MIT |
| ruflo_federation.png | P4c 联邦流程 | ruvnet/ruflo README（federation flow） | MIT |
| ruflo_console.gif | P4c 真实会话录屏（约 2.7× 速度） | https://github.com/ruvnet/ruflo/blob/main/docs/assets/ruflo-console-claude-control.gif | MIT |
| kd_scanpy.png / kd_rdkit.png | P3a / P3c 技能流程图 | https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/docs/images | MIT（K-Dense-AI/scientific-agent-skills） |
| android_gemini_skills_demo.gif | P5c 官方演示（约 1.6× 速度） | https://developer.android.com/static/tools/agents/videos/gemini_cli_skills_demo.gif | developer.android.com 内容，按 https://developer.android.com/license 为 CC BY 2.5（代码为 Apache 2.0） |
| android_skill_files.png | P5b Android Studio 技能目录 | https://developer.android.com/static/studio/images/skill-files.png | 同上，CC BY 2.5 |
| avatar_*.png | 头像，仅用于标识 | https://github.com/{morluto,anthropics,K-Dense-AI,ruvnet,android}.png | 仅用于标识仓库所有者 |
| assets/proc/*.png | 上面图片转成 RGBA 后的副本（Manim 需要） | — | 与原图相同 |

已下载但没有使用：
- android_blog_hero：画面里有真人照片。
- ruflo_tui.svg：动画 SVG，转成静态图后是空白。
- kd_diffdock.png、kd_literature-review.png、ruflo_ch14.jpg、ruflo_consolecard.png：时长不够，没有放进去。

## 我们自己跑的终端演示（demos/，都是真实输出，2026-10-22 运行）
- demos/android_tree.txt：`gh api repos/android/skills/git/trees/main?recursive=1 --jq ... | head -8`
- demos/kdense_preview.txt：`gh skill preview K-Dense-AI/scientific-agent-skills rdkit`
- demos/kdense_skillmd.txt：skills/rdkit/SKILL.md 的前 11 行（经 gh api 读取，画面里长行截断）
- demos/plugins_market.txt：对 2026-10-22 拉取的 marketplace.json 跑 jq 统计
- demos/plugins_pluginjson.txt：`gh api .../plugins/code-review/.claude-plugin/plugin.json`

所有演示都只是只读查询，没有执行 rea 或 ruflo 的任何二进制或安装脚本。

## 事实依据（旁白引用）
- REA：README、docs/architecture.mermaid、https://rea.tools/showcase/notion/ 、HN https://news.ycombinator.com/item?id=50028275 （389 points / 144 comments，为抓取时的数据）、InfoQ https://www.infoq.com/news/2026/10/reverse-engineer-anything/ （2026-10-17）
- claude-plugins-official：README、.claude-plugin/marketplace.json、plugins/code-review/README.md
- K-Dense：README（177 个技能、EGFR 示例、所用技能列表）、skills/rdkit/SKILL.md
- ruflo：README（架构层次、学习循环图注、console 录屏说明“创建任务不等于功能已实现”、联邦示例）
- android/skills：README、v1.0.16 release、developer.android.com 的 Agent Skills 概览页

---
# v3 变更（github_trending_top5_v3.mp4）

v3 去掉了以下内容：
- 自录的 gh 终端演示（v3 不再使用 demos/ 目录）
- android_skill_files.png（Android Studio 目录树截图）
- 所有 SKILL.md、plugin.json、marketplace.json 的字段、条目和分类统计
- 文件名和目录树

v3 保留的借用素材（都带来源字幕）：
- REA：rea_flow.png、rea_hopper.png、rea_showcases.png（MIT）
- Ruflo：
  - ruflo_capabilities.png、ruflo_learning.png、ruflo_federation.png（MIT）
  - ruflo_console.gif（MIT）：v3 只截取 4–30 秒，约 2.1× 速度，结尾换成原 GIF 的最后一帧（收回控制）
- K-Dense：kd_scanpy.png、kd_rdkit.png（MIT）
- Android：android_gemini_skills_demo.gif（developer.android.com，CC BY 2.5，约 1.7× 速度）
- avatar_*.png：仅用于标识

架构图都是按官方 README 或架构文档简化重绘的示意图。

## v4 变更（2026-10-22）
- 新增图表全部为本片自绘（Manim），数据来源：
  - #5 android/skills：33 个 SKILL.md 的名称与描述（Apache-2.0），**8 类分类为本片自行整理**；“选题集中在大模型表现欠佳场景”出自 Android 官方博客/文档（CC BY 2.5）。
  - #3 K-Dense：README 的技能分类计数与 “What's Included” 数量（MIT）。
  - #2 claude-plugins-official：`.claude-plugin/marketplace.json`（2026-10-22 拉取，Apache-2.0）的 category / author 统计；code-review、feature-dev、security-guidance 的流程摘自各插件 README（Apache-2.0）。
- 沿用素材：android_gemini_skills_demo.gif（CC BY 2.5，1.4× 播放）、ruflo_console.gif / ruflo_federation / ruflo_capabilities / ruflo_learning（MIT）、kd_scanpy / kd_rdkit（MIT）、rea_flow / rea_hopper / rea_showcases（MIT）、头像。
- 不再使用：Android 官方技能结构说明卡片、插件目录结构/JSON 讲解。仍无背景音乐。

## v5 变更
- 无新增素材；仅改 #5/#3/#2 分类段旁白与动画节奏，数据来源同 v4。

## 2026-10-23（周五版）更新
- 素材与来源未变，全部沿用上表；P1a 去掉了安装命令的打字动画（不放终端演示）。
- Hacker News 讨论（item 50028275）数据于 2026-10-23 重新读取：814 points / 340 comments（之前为 389 / 144）。
- 插件目录 marketplace.json 于 2026-10-23 重新拉取（marketplace_now.json）：仍为 315 个，分类计数与 10-22 相同。
