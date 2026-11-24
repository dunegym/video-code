# GitHub Trending 周榜研究笔记（2026 年第 47 周）

- 来源：https://github.com/trending?since=weekly（All languages）
- 抓取时间：2026-11-20 17:58（Asia/Shanghai，CST）
- 原始 HTML：`raw/trending_weekly.html`
- 页面条目数：13（公开页与带 GitHub 登录凭证再抓一次均为 13 条；与第 45 周 16 条、第 46 周 11 条同量级，视为本周完整可用列表）
- 名次规则：按页面从上到下的顺序；分类后在各类内保留该顺序，取该类前五。两类互斥，同一仓库不进入两个视频。
- 分类依据：以 README / 文档中的**主用途**为准，不单靠关键词。通用产品仅因提到 AI 集成，不归入 Agent/AI。

## 完整周榜与分类

| 页序 | 仓库 | 本周星 | 总星 | 语言 | 分类 | 理由 |
|---:|---|---:|---:|---|---|---|
| 1 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | 3468 | 13763 | TypeScript | **AI** | 本地浏览器评审工作台，主用途是让人批注、决定并把反馈送回编码智能体（Inbox、计划/代码审查、HTML 批注）。 |
| 2 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 1829 | 10858 | TypeScript | **AI** | 面向 Google Stitch 的 Agent Skills / 插件库，按开放技能规范编写，供编码智能体在设计稿与代码间流转。README 写明不是 Google 官方产品。 |
| 3 | [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 6858 | 9338 | TypeScript | **AI** | 这是 Modern Web Guidance 的源码与评测仓库；产品本身是「把现代网页指南嵌入编码智能体」的技能包。配套安装包在 `GoogleChrome/modern-web-guidance`。 |
| 4 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 4492 | 54507 | Go | **AI** | 阿里巴巴开源的 AI 代码审查 CLI：确定性流水线 × LLM Agent 的混合架构，主用途就是智能审查，不是「顺便带了模型」的通用审查器。 |
| 5 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 3179 | 71103 | Python | **AI** | 明确的 AI agent skill：在社交平台、代码仓库、预测市场等来源并行检索近三十天讨论，再合成有出处的简报。 |
| 6 | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 3229 | 58445 | TypeScript | AI（未入选前五） | 给编码智能体用的 Chrome DevTools MCP / CLI，主用途是让智能体控制并检查 Chrome。页序在 AI 类中排第 6，未进入本集 Top 5。 |
| 7 | [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | 3385 | 7330 | Python | AI（未入选前五） | Claude Code 交易/投研技能集。AI 类第 7。 |
| 8 | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 3455 | 20721 | TypeScript | AI（未入选前五） | Agent-User Interaction Protocol，把智能体接入前端。AI 类第 8。 |
| 9 | [meta/astryx](https://github.com/meta/astryx) | 4977 | 31166 | TypeScript | **其它** | Meta 开源设计系统（组件、主题、模板、CLI）。「agent ready」是设计原则和配套能力，主产品仍是设计系统，不因提到智能体而归入 AI。 |
| 10 | [pookjw/HermesEnabler](https://github.com/pookjw/HermesEnabler) | 904 | 2271 | Objective-C | **其它** | 在普通 Apple Watch 上启用爱马仕表盘的侧载工具，与 AI 无关。 |
| 11 | [we-promise/sure](https://github.com/we-promise/sure) | 3226 | 16804 | Ruby | **其它** | 社区维护的个人理财应用（Maybe Finance 的 fork）。「LLM agents」只是多种客户端之一，主用途是记账与财富管理。 |
| 12 | [dream-num/univer](https://github.com/dream-num/univer) | 7248 | 30755 | TypeScript | **其它** | 可嵌入的 Office SDK（表格/文档的编辑、计算、协作）。本仓库开源的是 Web SDK 核心；AI SDK 是单独授权的商业扩展。营销文案写「AI office」，但主用途仍是办公套件，不因可接智能体而归入 AI。 |
| 13 | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 2998 | 8565 | Python | AI（未入选前五） | 给编码智能体用的本地 FFmpeg 视频工具 / MCP。AI 类第 9。 |

星数均取自 17:58 CST 的周榜页面（不是之后的 API 实时值；例如 last30days 页面总星 71103，约一小时后 API 为 71104）。

## 入选名单

### Agent/AI Top 5（类内页序，视频从 #5 讲到 #1）

| 类内名次 | 页序 | 仓库 | 本周 | 总星 | 语言 | 许可 | 创建 |
|---:|---:|---|---:|---:|---|---|---|
| #1 | 1 | backnotprop/plannotator | 3468 | 13763 | TypeScript | Apache-2.0 | 2025-12-28 |
| #2 | 2 | google-labs-code/stitch-skills | 1829 | 10858 | TypeScript | Apache-2.0 | 2026-01-16 |
| #3 | 3 | GoogleChrome/modern-web-guidance-src | 6858 | 9338 | TypeScript | Apache-2.0 | 2026-01-27 |
| #4 | 4 | alibaba/open-code-review | 4492 | 54507 | Go | Apache-2.0 | 2026-05-18 |
| #5 | 5 | mvanhorn/last30days-skill | 3179 | 71103 | Python | MIT | 2026-01-23 |

### 其它项目（类内仅 4 项，短少 1 项）

本周可用周榜共 13 条，按主用途划分后 **Agent/AI 9 条、其它 4 条**。其它类不足 5 条，**不编造、不改用别的排序补位**。视频按这 4 项制作，封面与旁白均按 Top 4 陈述短少。

| 类内名次 | 页序 | 仓库 | 本周 | 总星 | 语言 | 许可 | 创建 |
|---:|---:|---|---:|---:|---|---|---|
| #1 | 9 | meta/astryx | 4977 | 31166 | TypeScript | MIT | 2026-01-09 |
| #2 | 10 | pookjw/HermesEnabler | 904 | 2271 | Objective-C | MIT | 2024-12-14 |
| #3 | 11 | we-promise/sure | 3226 | 16804 | Ruby | AGPL-3.0 | 2025-07-23 |
| #4 | 12 | dream-num/univer | 7248 | 30755 | TypeScript | Apache-2.0 | 2022-09-29 |

## 星数不确定处（只记录，不做判断）

- `mvanhorn/last30days-skill`：2026-01-23 创建，约 10 个月总星 71103，增速很高。
- `alibaba/open-code-review`：2026-05-18 创建，约 6 个月总星 54507；官方背景是阿里内部审查助手开源。
- `GoogleChrome/modern-web-guidance-src`：本周 6858 / 总星 9338，本周约占 73%，涨幅很陡。上榜的是源码与评测仓，用户安装的是配套的 `modern-web-guidance` 包。
- 其余高星项目（chrome-devtools-mcp 58445、astryx 31166、univer 30755）有官方或长期项目背景，一并记入完整列表，未作额外推断。

## 各入选项目要点（供脚本使用）

### backnotprop/plannotator
本地浏览器评审层：智能体提出计划、交上改动或抛来问题后，在浏览器打开，人批注并送回。Inbox 把多智能体的提问、文件和引导式审查收在同一窗口，不必占着会话。计划评审由钩子弹出；代码审查支持本地 diff / GitHub PR / GitLab MR，引导式审查把 diff 按章节排序。也可批注本地页面（本地代理，热更新仍在）和终端里的 Markdown。v0.29.1 于 2026-11-19 20:08 UTC（CST 11-20 04:08）发布，v0.29.0 重做了代码审查窗口（双栏、文件树、语义差异、就评论与智能体对话）。官网 https://plannotator.ai

### google-labs-code/stitch-skills
三组插件：stitch-design（出稿/改稿/设计系统/从代码抽稿并上传）、stitch-build（转 React / React Native、Remotion 演示视频等）、stitch-utilities（增强提示词、DESIGN.md / SITE.md、从一句话铺多页站点）。依赖 Stitch MCP。技能标准结构：SKILL.md + scripts + resources + examples。仓库声明非 Google 官方产品。官网需登录，素材用官方 OG 图 https://app-companion-430619.appspot.com/static/og.png（stitch.google.com）。

### GoogleChrome/modern-web-guidance-src
技能激活后，CLI 在本地做语义检索（离线嵌入 + BM25，无搜索 API），再按 id 取回指南。内容按体验/布局、性能、表单与原生组件、无障碍、浏览器内置本地模型接口等方向归类；指南刻意写短，模型已会的会被剪掉。评测看板 2026-11-20 快照：近一周任务有指南时最佳实践通过率约 53%→92%（+39pp，229 对任务），无障碍检查 +36pp（59%→94%）。Chrome、Edge、Firefox、MDN 共同维护。文档 https://developer.chrome.com/docs/modern-web-guidance ，看板 https://googlechrome.github.io/modern-web-guidance-src/

### alibaba/open-code-review
确定性工程负责选文件、打包、规则匹配、评论定位与反省；Agent 负责动态决策与上下文检索，工具集从生产调用记录收束。相关文件捆成一组，由隔离子代理并行审。官方对比：同样模型下精确率与 F1 更高，词元约 1/9，更快；召回更低是少报、少误报的取舍。可原生审查，也可只做选文件/匹配规则、把审查交给当前编码智能体。v1.13.13（2026-11-19）把排行榜链到 AACR-Bench。官网 https://open-codereview.ai

### mvanhorn/last30days-skill
流程：解析相关账号/仓库/社区 → 多源并行检索 → 按互动、相关、时效打分 → 同一事件并簇 → 带引用简报。来源分社交讨论、视频转录、开发者社区、预测盘，以及公司招聘页/专利等。v4 增加专利与招聘「秘密信号」。默认同机检索；仅在配置重排模型时才把片段送出。演示 GIF：`media/pr-assets/last30days-ad.gif`。今日 v4.4.0 多为修复，旁白不展开。

### meta/astryx
Meta 内部约八年的设计系统，官网写 Over 180 components（README 仍写 150+，画面与旁白以官网为准并注明）。StyleX 对使用者透明，可用 Tailwind / 普通 CSS 覆盖；主题是 CSS 变量。CLI 把说明写入 AGENTS.md / CLAUDE.md。结构：Foundations / Components / Patterns。原则：引导而非强制；人和智能体用同一套接口。官网 https://astryx.atmeta.com ，当前 Beta，构建于 React 19+ 与 StyleX。v0.7.16 发布于 2026-11-14。

### pookjw/HermesEnabler
在普通 Apple Watch 上启用爱马仕表盘。README：支持 watchOS 27.0 至 27.3 beta 1；1.6.3（2026-11-19）加入 27.2 beta 2（明确不是 27.3 beta 2）；watchOS 26 不支持。需要侧载并打开开发者模式；删除前须在应用内恢复 MobileGestalt 备份。使用了 Gester 的代码，作者写明自行承担风险。视频只做产品层介绍，不逐步演示绕过专属表盘的安装操作。配图 `image.png`。

### we-promise/sure
Maybe Finance 社区 fork（原团队商业化未成后开源，托管版也未持续）。Docker 自托管；客户端包括浏览器、macOS、移动端、API 以及大模型代理。稳定版 v0.7.6 / hotfix.1（2026-10-31 / 11-12）：「Spending vs normal」把开支和自身历史对比，贷款账户展示本金/利息/还款节奏。AGPL-3.0，「Maybe」商标不可用，故名 Sure。官网 https://sure.am ，仪表盘截图在 docs/screenshots。

### dream-num/univer
Office SDK：Web SDK（本仓开源核心：内容模型、插件与命令、公式与渲染、Facade API、Sheets/Docs）、Server SDK（协作、历史、导入导出，另发）、AI SDK（商业扩展，另授权）。功能插件管规则，UI 插件管交互；改动走统一命令，可跨功能撤销重做。应用和智能体通过同一套 Facade API 与事件读写。另有 Univer Workspace 作为参考应用。本周星 7248，为整份 13 条周榜中本周增长最多。官网 https://univer.ai ，默认分支 `dev`，v1.5.2 于 2026-11-16 发布。

## 未纳入的 AI 项目（避免与 Top 5 混淆）

chrome-devtools-mcp、claude-trading-skills、ag-ui、ffmpeg-skill 均为明确的智能体工具/协议/技能，因类内页序在第 6–9，不进入本集。
