# GitHub Trending 周榜研究笔记（2026 年第 48 周）

- 来源：https://github.com/trending?since=weekly（All languages）
- 抓取时间：2026-11-27 17:01:56（Asia/Shanghai，CST）/ 2026-11-27 01:01:56（PST）
- 原始 HTML：`raw/trending_weekly.html`；抓取时刻：`raw/snapshot_time.txt`
- 页面条目数：15（与第 45 周 16 条、第 46 周 11 条、第 47 周 13 条同量级，视为本周完整可用列表）
- 名次规则：按页面从上到下的顺序；分类后在各类内保留该顺序，取该类前五。两类互斥，同一仓库不进入两个视频。
- 分类依据：以 README / 文档中的**主用途**为准，不单靠名称或关键词。通用产品仅因提到 AI 集成，不归入 Agent/AI。

## 完整周榜与分类

| 页序 | 仓库 | 本周星 | 总星 | 语言 | 分类 | 理由 |
|---:|---|---:|---:|---|---|---|
| 1 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | 1631 | 15318 | TypeScript | **AI** | 本地浏览器评审工作台，主用途是让人批注、决定并把反馈送回编码智能体（Inbox、计划/代码审查、HTML 批注）。 |
| 2 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 2619 | 13411 | TypeScript | **AI** | 面向 Google Stitch 的 Agent Skills / 插件库，按开放技能规范编写，供编码智能体在设计稿与代码间流转。README 写明不是 Google 官方产品。 |
| 3 | [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 2209 | 11335 | TypeScript | **AI** | Modern Web Guidance 的源码与评测仓库；产品本身是「把现代网页指南嵌入编码智能体」的技能包，配套安装包为 `GoogleChrome/modern-web-guidance`。 |
| 4 | [n8n-io/nod](https://github.com/n8n-io/nod) | 1165 | 4111 | TypeScript | **AI** | n8n 团队开源的自带沙盒工作区与浏览器的个人智能体，主用途是在真实网站与应用里代办事务并在动作前请求审批。 |
| 5 | [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 2284 | 56753 | Go | **AI** | 阿里巴巴开源的 AI 代码审查 CLI：确定性流水线 × LLM Agent 混合架构，主用途就是智能代码审查。 |
| 6 | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 5090 | 76015 | Python | AI（未入选前五） | 明确的近三十天舆情调研 Agent Skill，页序在 AI 类中排第 6，未进入本期 Top 5。 |
| 7 | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 1175 | 59551 | TypeScript | AI（未入选前五） | 给编码智能体用的 Chrome DevTools MCP / CLI，AI 类第 7。 |
| 8 | [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | 1381 | 8654 | Python | AI（未入选前五） | Claude Code 交易/投研技能集，AI 类第 8。 |
| 9 | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 1269 | 21885 | TypeScript | AI（未入选前五） | Agent-User Interaction Protocol，把智能体接入前端的协议，AI 类第 9。 |
| 10 | [meta/astryx](https://github.com/meta/astryx) | 2519 | 33434 | TypeScript | **非 AI 类项目** | Meta 开源设计系统（组件、主题、模板、CLI）。「agent ready」是设计原则与配套说明，主用途仍是设计系统，不归入 AI。 |
| 11 | [pookjw/HermesEnabler](https://github.com/pookjw/HermesEnabler) | 325 | 2556 | Objective-C | **非 AI 类项目** | 在普通 Apple Watch 上启用爱马仕表盘的侧载工具，与 AI 无关。 |
| 12 | [we-promise/sure](https://github.com/we-promise/sure) | 1430 | 18140 | Ruby | **非 AI 类项目** | 社区维护的个人理财应用（Maybe Finance 的 fork）。大模型代理只是多种客户端之一，主用途是记账与财富管理。 |
| 13 | [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) | 704 | 54141 | Shell | AI（未入选前五） | README 首行明确为「Agent Skills for use with Obsidian」，遵循 Agent Skills 规范，主用途是教智能体操作 Obsidian 与 Markdown/Canvas 等开放格式。AI 类第 10。 |
| 14 | [dream-num/univer](https://github.com/dream-num/univer) | 1825 | 32010 | TypeScript | **非 AI 类项目** | 可嵌入的 Office SDK（表格/文档的编辑、计算、协作）。本仓开源 Web SDK 核心；AI SDK 是独立授权商业扩展。主用途仍是办公套件，不归入 AI。 |
| 15 | [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | 3229 | 11683 | Python | AI（未入选前五） | 给编码智能体用的本地 FFmpeg 视频剪辑技能与 MCP，AI 类第 11。 |

星数与名次均取自 2026-11-27 17:01:56 CST 的周榜页面快照，不以事后 API 实时值替换。

## 入选名单

### Agent/AI Top 5（类内页序，视频按 #5 → #1 展开）

| 类内名次 | 页序 | 仓库 | 本周星 | 总星 | 语言 | 许可 | 创建日期 | 最新版本 |
|---:|---:|---|---:|---:|---|---|---|---|
| #1 | 1 | backnotprop/plannotator | 1631 | 15318 | TypeScript | Apache-2.0 | 2025-12-28 | v0.29.5 (2026-11-26) |
| #2 | 2 | google-labs-code/stitch-skills | 2619 | 13411 | TypeScript | Apache-2.0 | 2026-01-16 | v1.0 (2026-05-18) |
| #3 | 3 | GoogleChrome/modern-web-guidance-src | 2209 | 11335 | TypeScript | Apache-2.0 | 2026-01-27 | 无正式 Release |
| #4 | 4 | n8n-io/nod | 1165 | 4111 | TypeScript | Apache-2.0 | 2026-09-25 | nod-v0.10.0 (2026-11-27) |
| #5 | 5 | alibaba/open-code-review | 2284 | 56753 | Go | Apache-2.0 | 2026-05-18 | v1.14.4 (2026-11-26) |

### 非 AI 类项目（类内仅 4 项，短少 1 项）

本周可用周榜共 15 条，按主用途划分后 **Agent/AI 11 条、非 AI 类项目 4 条**。非 AI 类项目不足 5 项，**不补凑、不改用其他榜单、不伪造第五项**。成片、封面、字幕与简介均按实际 4 项（Top 4）如实说明。

| 类内名次 | 页序 | 仓库 | 本周星 | 总星 | 语言 | 许可 | 创建日期 | 最新版本 |
|---:|---:|---|---:|---:|---|---|---|---|
| #1 | 10 | meta/astryx | 2519 | 33434 | TypeScript | MIT | 2026-01-09 | v0.7.17 |
| #2 | 11 | pookjw/HermesEnabler | 325 | 2556 | Objective-C | MIT | 2024-12-14 | 1.6.3 |
| #3 | 12 | we-promise/sure | 1430 | 18140 | Ruby | AGPL-3.0 | 2025-07-23 | v0.7.6-hotfix.2 |
| #4 | 14 | dream-num/univer | 1825 | 32010 | TypeScript | Apache-2.0 | 2022-09-29 | v1.6.2 |

## 星数与来源说明（只记录证据与不确定性，不下结论）

- `alibaba/open-code-review`：2026-05-18 创建，半年多总星 56,753；官方背景为阿里内部代码审查工具开源。
- `n8n-io/nod`：2026-09-25 创建，总星 4,111，本周新进入 Agent/AI 类前五；README 标注处于 **research preview** 阶段，评测数据为官方在模拟账号与网站下的自报测试结果，非第三方独立评测。
- 本周 15 条记录中，有 13 条来自上周榜单续热，新增 `n8n-io/nod` 与 `obsidianmd/obsidian-skills`；GitHub REST API 在抓取前 5 个仓库后触发匿名速率限制（403），后 5 个仓库的 README 与最新版本直接从 `raw.githubusercontent.com` 和 `github.com` 公开页面核验获取，许可证与创建日期沿用公开元数据。

## 各入选项目研究卡片

### 1. backnotprop/plannotator（AI #1）
- **定位**：给人盯智能体的本地浏览器评审工作台（官网 https://plannotator.ai ）。
- **高层架构**：智能体提出方案、提交改动或发起提问时，通过钩子或收件箱在本地浏览器打开；人在界面里批注、做决定，再一键把结构化意见送回提出问题的那一次运行。收件箱汇总多个智能体的提问、文件与引导式审查；代码审查支持本地 diff / GitHub PR / GitLab MR，并可对本地运行页面透过代理直接画点批注（保留热更新）及终端批注。
- **本周进展**：2026-11-26 发布 `v0.29.5`；近期 `v0.29.3–v0.29.4` 新增跨关联电脑合并会话、在线程里点名另一台机器上的智能体、以及让智能体把 PR 一路推进到合并的 Ship 流程。

### 2. google-labs-code/stitch-skills（AI #2）
- **定位**：对接 Google Stitch 的开放技能库（README 明确声明**非 Google 官方产品**）。
- **高层架构**：分为设计（stitch-design：出稿、改稿、管理设计系统、从前端代码抽稿上传）、构建（stitch-build：生成 React / React Native 组件、检查设计令牌一致、制作演示视频）和工具（stitch-utilities：补全提示词、生成 DESIGN.md / SITE.md、一句话铺多页站点）三组插件，均连向 Stitch 服务，通过脚本做校验与上传，知识库存放清单和样例。技能间存在依赖关系，需配套安装。

### 3. GoogleChrome/modern-web-guidance-src（AI #3）
- **定位**：现代网页指南的源码与评测仓库（Chrome、Edge、Firefox、MDN 共同维护；编码智能体安装的是配套的 `modern-web-guidance` 包）。
- **高层架构**：技能激活后在本地用离线嵌入加 BM25 做语义检索（不走联网搜索接口），按编号取回短小精悍的指南（含写法、坑与退路），覆盖体验布局、性能、表单原生组件、无障碍和浏览器内置本地模型接口。核心取舍是闭环评测驱动剪枝：模型本来就会的内容会被删掉，只保留真正拉开通过率差距的条目。

### 4. n8n-io/nod（AI #4，本周新晋前五）
- **定位**：n8n 团队开源的自带沙盒电脑与浏览器的个人智能体（官网 https://nod.n8n.io ，当前为 Research Preview；独立应用，不依赖 n8n）。
- **高层架构**：单机运行一个 Node.js 24 服务进程（含 Pi 运行时、策略信任检查、Vault 凭证库、记忆、定时任务与 PostgreSQL + pg-boss），向外调度两个 Docker 容器：Linux 沙盒工作区与 Chromium 浏览器。用户可通过桌面端、Telegram 或 WhatsApp 下达跨 Gmail、Calendar、Slack、Notion 和真实网页的事务（如晨间会议简报、按报价表草拟回复并待审批、定时盯价、催发票、取消试用）。
- **安全与设计取舍**：策略校验写在服务端而非提示词里；所有应用和网页返回内容默认标记为不可信数据而非指令；模型 API 密钥不进入沙盒或浏览器；Vault 私下代填密码与卡片，不把敏感信息暴露给模型；记忆只从用户本人消息学习，每条可查看、编辑或遗忘。
- **本周进展与边界**：2026-11-27 发布 `nod-v0.10.0`，改用单一常驻浏览器保存网站登录态，同时为每个对话、任务与定时运行隔离上下文，并新增结构化卡片回复（列表、日程、对比与消息草稿）。官方自报评测（GPT-6.1 Sol，模拟环境，226 项任务×3 轮）：98% 完成率、678 次运行 0 次不安全动作、LongMemEval-S 93.2% 召回；但官方同时提醒安全检查仍依赖模型判断，小模型在 240 次测试决策中放行了 8 次不安全操作，且默认经由 n8n 托管服务连接应用并开启基础用量上报（可在设置中关闭）。

### 5. alibaba/open-code-review（AI #5）
- **定位**：阿里巴巴开源的混合架构代码审查命令行工具（官网 https://open-codereview.ai ）。
- **高层架构**：把确定性工程与大模型代理拆开——选文件、相关文件分组打包、规则匹配、行级评论定位与反省校验由确定性流水线卡死；提示词与从生产调用记录收束出的工具集交给隔离的子代理并行审查。支持原生审查，也支持只做选文件与规则匹配、把审查委托给当前编码智能体。
- **评测与进展**：官方 200 个真实 PR 自报对比中，同模型下精确率与 F1 更高、词元消耗约通用代理九分之一，召回率更低（主动少报、少误报）。2026-11-26 发布 `v1.14.4`，支持从固定快照审查 GitHub PR、排除 C/C++ 测试与基准目录，并补充敏感路径过滤文档。

### 6. meta/astryx（非 AI 类 #1）
- **定位**：Meta 内部使用约八年后开源的设计系统（官网 https://astryx.atmeta.com ，当前 Beta，基于 React 19+ 与 StyleX，最新 `v0.7.17`）。
- **高层架构**：分基础（字体、颜色、布局）、组件（官网写超过 180 个；README 仍写 150+，以官网为准并注明）与页面模式三层；StyleX 对使用者透明，支持 Tailwind 或普通 CSS 覆盖，主题以 CSS 变量驱动；原则为引导而非强制，CLI 会把用法写入说明文件，让人和智能体共用同一套接口与参考。

### 7. pookjw/HermesEnabler（非 AI 类 #2）
- **定位**：在普通 Apple Watch 上启用爱马仕表盘的侧载工具（最新 `1.6.3`）。
- **要点与边界**：需侧载并开启开发者模式，删除前须在应用内恢复 MobileGestalt 备份；说明限定 watchOS 27.0 至 27.3 beta 1（1.6.3 加入 27.2 beta 2，不支持 watchOS 26 及 27.3 beta 2）；借用 Gester 部分代码，非苹果官方能力，版本不符时作者建议改用其另一项目 Clocky，自行承担风险。

### 8. we-promise/sure（非 AI 类 #3）
- **定位**：社区接手维护的可自托管个人理财应用（Maybe Finance 分支，最新 `v0.7.6-hotfix.2`，官网 https://sure.am ）。
- **高层架构与要点**：原团队商业化未成后开源并停止托管，社区在 AGPL-3.0 协议下继续维护（因商标仍属原公司而改名 Sure）。Docker 一键自托管，浏览器、桌面、移动端、API 及大模型代理共用同一套账本；v0.7.6 系列新增「开支对比自身历史」与贷款本息节奏视图，并在演示站公开慢请求以便社区优化。

### 9. dream-num/univer（非 AI 类 #4）
- **定位**：可嵌入产品的开源 Office SDK（官网 https://univer.ai ，最新 `v1.6.2`）。
- **高层架构**：本仓开源 Web SDK 核心（内容模型、插件与命令系统、公式与渲染引擎、门面接口与表格/文档能力）；功能插件管规则数据、UI 插件管交互，改动走统一命令体系实现跨功能撤销重做；应用与外部智能体共用同一套开源门面接口，服务端协作/导入导出与商业 AI SDK 另行授权，并提供 Univer Workspace 作为参考应用。
