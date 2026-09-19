# batch08 — B8 其余批（独立评测/基准富矿·扫读为主·无深读名额）

日期：2026-09-19 ｜ 池：**68 库**（v7）｜ 状态：**完成**（遗留见 §五）
**浅采·要点 28 · 浅采 18 · 留矩阵 20 · 留矩阵·存疑 2 · 深采 0**（合计 68；统计由 `_rb8_precheck.py` 从 §二 处置列解析回填，header ok ✓。**行级 diff vs `_b8_meta.txt`：幻影 0 / 漏库 0**（初稿误写的 2 条幻影占位行已按 B7 教训在跑脚本前主动删除）；41 个数字 token→源文件反查 **0 MISS**；dabit3 266B 近空壳经 getsize 核实）

## 一、批次定性与零复跑说明

- PLAN B8 = "其余"杂项，执行节奏 D7 与 B7 合并为**扫读批**，**不分配深读名额**；DoD-1"深采≥8"已由 11 篇单库档满足。
- 但 B8 名不副实地**是整场战役的"独立评测/基准"富矿**：出现一簇"第三方独立、预注册、带基线/CI/负结果"的评测库（assay-001 / jev-orderby-bench / jev-sec-bench / legalforecastbench / jev-behavior-study / windtunnel / tiershift / open-alternative-jev），恰好从**外部复证**我们反复内部撞见的两条主线——① 自评自证循环性 ② confidence≠校准。
- **本批零 key 复跑记 0**（决策非遗漏）：PLAN 定扫读、DoD-3 已由前四批 4 次复跑超额满足；且本批多数评测库复跑需真 API key（assay/orderBy/sec-bench 打的是真 jev endpoint）或需自带数据集，不属"一条命令零 key 可跑"。理由留此免被 FINAL 当漏项。
- 若干库 README 极薄/是占位（dabit3 266B、devagrawal09 npm 0.0.1 无工作命令、kuhung 正文在自建站点）→ 归 留矩阵/存疑，见 §二标⚠与 §五。

## 二、68 库 stay/go 矩阵

| 库（★/lic） | ①复跑②量化③调用 | 处置 | 一句话依据 |
|---|---|---|---|
| yodablocks/jev-orderby-bench (lic=?) | ✗✓✓ | 浅采·要点 | **预注册 6 门**（2026-09-18 headline 全过）：360 人工标注行、布尔翻转率 0.036 / Score 序翻转 0.143 vs 0.15 门（"弱链"）/ 否定不对称 0.016；"校准(ECE,Brier)也报但**单它不构成门**" |
| jourdanlabs/assay-001 (lic=?) | ✗✓✓ | 浅采·要点 | **独立预注册校准核查**：CLINC150 chosen-prob **ECE 0.0204 校准**、Banking77 **ECE 0.0936 系统性过conf**；`score.py --sum-tol 0.02`——同模型不同数据集校准结论相反 |
| gaurav-gosain/jev-sec-bench (lic=?) | ✗✓✓ | 浅采·要点 | 盲注入门 + 漏洞码检测：**662 条消息/263 注入**、0.50 一刀切下 accuracy **96.5%/prec 96.2/recall 95.1**；"要的是可阈值化的数、非须解析的段落" |
| rinnecoder/jev-behavior-study (lic=?) | ✗✓✓ | 浅采·要点 | 独立合成任务研究，**诚实负结果**："两步法多花一次请求、**无准确率理由为此付费**"；"无投喂答案、每模型选择原样执行"；贪吃蛇另有独立 verifier |
| firassx914/janus (MIT) | ✗✓✓ | 浅采·要点 | **不发默认阈值、测一个**：Banking77 threshold **0.67→80.2%**（优于任一单模），always_primary 77.8%/always_fallback 78.8%，cov/acc/cost/p50 全表——路由门阈值扫描范本 |
| johnhughes3/legalforecastbench (lic=?) | ✗✓✓ | 浅采·要点 | 联邦驳回动议预测基准：**micro-Brier** 校准度量、**训练数据截止**而非发布日定资格、预注册不可变 revision——"高主观法律工作也能基准化" |
| iamvatsalpatel/tiershift (MIT) | ✗✓✓ | 浅采·要点 | 策略约束路由实测：默认政策与 always-flagship **同质量 4.77** 而成本 **$13.23→$7.95**；**自曝"本基准证不了什么"**（单轮清晰题） |
| ikermoel/open-alternative-jev (lic=?) | ✗✓✓ | 浅采·要点 | 开源 Jev-shape 决策模型：acc 92.6→92.8% 批量；**"raw confidence 高约 5 点（MMLU 均值 conf 0.90 vs acc 0.84）"**、对称扰动使聚合不降但单决策可翻——循环自证量化 |
| qkal/canny (lic=?) | ✓✓✓ | 浅采·要点 | 证据台账挑战编码 agent **无据"done"宣称**；关键实测"**Jev 概率已校准但跨 run 漂移约 0.05**"→ 直对 nous drift_within_round + pi-warden done-check |
| owner-A/jev-curate (MIT) | ✗✓✓ | 浅采·要点 | 语料清洗：LLM 判合成行 **$15k–50k/十亿** vs Jev **~$4.20/100M**（100×/700× 便宜）；"未压缩输入致 context rot"——novel 语料清洗可借 |
| nekuda-ai/windtunnel (Apache-2.0) | ✗✓✓ | 浅采·要点 | 浏览器 agent 基准：49 任务×8 站/**21 配置 3087 次尝试**，WebMCP 100% 完成、2.5–4.5× 快、3–7× 省；**harness 免 key 免 Docker 可跑** |
| noelzappy/tripwire (lic=?) | ✓✓✗ | 浅采·要点 | 响应前 7 检 ~100ms：per-check 阈值(pii 0.85/injection 0.80/halluc 0.80)；eval CLI 打印各阈值 precision/recall/coverage；**诚实"尚无对真 Jev 的准确率、29 mock 测试"** |
| kevthetech143/super-jev (lic=?) | ✗✓✓ | 浅采·要点 | **"floor 之上再加 margin"**：top-1 高但亚军也高=仍是猜；`permit(state,action)` **域规则独立于模型 confidence**；离线 admission bench（脚本 stub） |
| nullpo-jp/pocketjev (Apache-2.0) | ✓✓✗ | 浅采·要点 | 端上 iPhone 视觉决策；**"这是决策 UI 非校准分类器，分数是 option-relative 模型分非校准 confidence"**、基准未发布——诚实去魅 |
| stephanj/parallelconstraintdecoding (lic=?) | ✗✓✓ | 浅采·要点 | 并行约束解码极限：欺诈/分诊/255 关税路由延迟表（**1.08–1.34× vs Python**，2388→266ms）；每选项校准 confidence |
| theoleecj/semif (lic=?) | ✗✓✓ | 浅采·要点 | 独立 typed-option 读出研究（前身 OpenJev）：并列后缀 20.03 万 tok/s vs 串行 10.75；**"Jev 数取自公开记录、未跑 live endpoint"** 诚实划界 + 扰动平衡准确率表 |
| vinnylarouge/jevlike (lic=?) | ✗✓✗ | 浅采·要点 | 训一个单遍 one-pass 打分器：合成菜单 **~98% top-1**、Wikispeedia next-link 偏低；attention 从 image patch 给手柄打分 |
| zhengxuyu/litjev (lic=?) | ✓✓✗ | 浅采·要点 | Jev 本地复现（Qwen）：**"概率默认未校准"** 置顶声明 + 完整 prob/conf 样例；复现 schema 非 internals |
| hr98w/jev-visual (MIT) | ✗✓✗ | 浅采·要点 | 教育性 VLM 推理（Apple Silicon）：**"独立社区实现、不声称复现 Jev 专有架构/RLCD 训练/校准"**——干净的非等价免责范式 |
| santos-sanz/jev-audio-beeper (lic=?) | ✓✓✗ | 浅采·要点 | 低延迟音频脏话消音：阈值 **0.72 明标"POC 起点非生产宣称"、须按语言/方言/引语校准**、误报毁音频代价高 |
| sufianetaouil/every (lic=?) | ✗✓✓ | 浅采·要点 | 语义码搜 CLI（1842 函数/214 文件/3.1s/$0.03）：**"落在阈值 ±0.10 内→重问取平均"**——边界带二次判，近 nous 上下文不足态 |
| vicente-md/jev-resilience (MIT) | ✗✓✗ | 浅采·要点 | Spring WebFlux **语义熔断器**：`@SemanticCircuitBreaker(confidenceThreshold=0.85)` 判"伪装成成功的失败"→抛异常而非放行 |
| teyhouse/jev-secret-detection (lic=?) | ✗✓✓ | 浅采·要点 | 密钥入 diff 检测：报 **Brier(0 完美/0.25=恒答 0.5)+AUC(阈值无关排序)** + 分类别 accuracy；实测 p50 75–90ms 印证 100ms |
| sosopop/jev_stock (lic=?) | ✗✓✓ | 浅采·要点 | 港股方向预测：**"危险在'probability'一词——down:0.68 只是对所给问题的模型概率、不自动=下注真实概率"**；职责分离（Python 管数据/防泄漏，Jev 管语义） |
| skyvern-ai/jevscape (lic=?) | ✗✓✓ | 浅采·要点 | RuneBench RuneScape harness：tick 400ms、**整轮 Jev sweep 成本 $0.17**、Jev $0.042 vs Free 对照；重点击全来自 Jev restart 判定 |
| reachjalil/jev-tree (MIT) | ✗✓✓ | 浅采·要点 | **递归 Choice 破 255 选项上限**：320 叶多区事件目录/180 标注工单，"截到 255 会丢**尾部 0%**"——大类目分档（对 nous Ending 二级树） |
| realzachi/pg-jev (PostgreSQL) | ✗✓✓ | 浅采·要点 | PG 扩展行级 `jev(row,cond[,thr])`：2000 行实测首跑 ~3.5s/100 请求 ~296k tok **~$0.012**、二跑 ~50ms（按行内容缓存） |
| 24601/augustus (MIT) | ✗✓✗ | 浅采·要点 | agent skill：把 Choice/Score/Noul 映射到选择性二元决策，**references/validation.md 带 Brier/reliability/threshold-cost sweep 设计门** |
| owner-B/bicameral (MIT) | ✗✓✓ | 浅采 | Pi 编码 harness：S2 写码/S1(Jev) 供 typed 反射，exfiltration 0.91→block 12ms、deadline 900ms、decideGate/HonestFinish/Stuck |
| achimala/jevinci (lic=?) | ✗✓✗ | 浅采 | 逐像素并行调用作图（极限并行示例），550ms/帧、网络与渲染计时分离 |
| owner-A/jev-superpowers (MIT) | ✗✓✗ | 浅采 | 开发框架：对照表（包幻觉 14%→0%、门延迟 3.5–12s→70–120ms、$0.015→$0.00001/决策）+ <400ms 离线 7/7 测——偏营销但离线臂真 |
| ashutoshvjti/progressgate (lic=?) | ✗✓✗ | 浅采 | 检 agent 循环语义停滞：materialProgress 0.42 判"字面 deploy 成功却无进展"一步 |
| bastani-inc/atomic (MIT) | ✗✓✗ | 浅采 | 可验证运行时（64KB README 营销重）：~95% merge/0% revert 自报、人在环门、steer/pause/abort |
| ellipsis-dev/blink (lic=?) | ✗✓✗ | 浅采 | 码搜：一组 walker 问 Jev 哪个文件答问题，文件相关度 %(74/16/10%) |
| jarrodwatts/jev-trader (lic=?) | ✗✓✓ | 浅采 | 每 Monad 块一买/卖：Kuru MON-USDC、~300ms、probabilities{buy.77}、SSE 事件流 |
| kitze/pagegrade (MIT) | ✗✓✗ | 浅采 | Chrome 扩展给页面分节评清晰/写作/切题，BYO Vercel 网关 key（kitze 亦 B4 unclutter 作者） |
| lakeday-org/perch (lic=?) | ✗✓✓ | 浅采 | 语义码 linter：confidence+severity 表（P1(0.8)/wrong_order 81%），可配 rule 语法 |
| ljedrz/nachalnik (lic=?) | ✗✓✗ | 浅采 | Jev 辅助 compaction 示例（B3/B5 压缩族）：token/保留计数、"拿走回执"博文 |
| mrnugget/jev-shell-history (lic=?) | ✗✓✓ | 浅采 | zsh 补全：JEV_THRESHOLD 0.5/STRONG_SCORE 0.9 覆盖、[0.970] 分数显示 |
| pithings/advocaat (lic=?) | ✗✓✗ | 浅采 | 类型安全客户端：`ask.if` yes>0.5 可改阈、choice 返回 typed union |
| query-farm/vgi-typesafe (MIT) | ✗✓✗ | 浅采 | DuckDB VGI 扩展：**472 离线/26 live 测试**、lint 100/100 L2 |
| reachjalil/jevlogs (MIT) | ✗✓✗ | 浅采 | OTel 日志分诊：Jev 评诊断价值/优先级、低价值跳过 LLM 分析支 |
| sharziki/semdecide (lic=?) | ✗✓✓ | 浅采 | "意义的 grep/判断的 jq" CLI：probability 0.86 vs threshold 0.70、Noul confidence=null |
| supercorp-ai/supercov (lic=?) | ✗✓✗ | 浅采 | 编码 agent 码质：Jev 答 12 条 Noul 属性（long_method 0.96…）+ MC/DC 覆盖 |
| trungdq88/youtube-sponsor-detection (lic=?) | ✗✓✓ | 浅采 | 赞助段跳过：对照 SponsorBlock 报准确率、≥70/80% conf 才跳 |
| ufec/jev-block-android-ad (JitPack) | ✗✓✗ | 浅采 | Android 通知/SMS 噪声门：结构化 state（noiseRatio 0.25）+ userRules 自然语言 |
| andrelandgraf/safer-with-jev (lic=?) | ✗✗✗ | 留矩阵 | Neon Function 代理 + 新闻站，无评测内容 |
| aowang-ai/jev-trade (MIT) | ✗✓✗ | 留矩阵 | Hyperliquid 加密多空 Choice 示例，JEV_PROVIDER=gateway |
| different-ai/openwork (目录分授权) | ✗✓✗ | 留矩阵 | 工程工作流把 Jev 接入 eval testkit 作验证器（EE/开源分目录，类 GitLab） |
| kieranklaassen/ruby_llm-typesafe (lic=?) | ✗✓✗ | 留矩阵 | RubyLLM2 TypeSafe provider；noul 0.95/probs 展示 |
| kuhung/understanding-jev (lic=?) | ✗✗✗ | 留矩阵 | **中文深度解读**（PLAN 点名）但 README 仅 ~1KB、正文在 `build_site.py` 自建站——离线不可核，存 §五 |
| n3ndor/n8n-nodes-typesafe-jev (lic=?) | ✗✓✗ | 留矩阵 | n8n 社区节点：Continue On Fail/Retry、无运行依赖 |
| obie/ruby_decision_model (lic=?) | ✗✓✗ | 留矩阵 | 标准库传输 Ruby 客户端；backoff_jitter 0.25 |
| phureewat29/got-jev (lic=?) | ✗✓✗ | 留矩阵 | 权游角色扮演（GPT 叙述 + Jev 决策 resolve/retry） |
| phyous/tsai-civ2 (lic=?) | ✗✓✗ | 留矩阵 | Jev×文明II：选帝国/城市，概率显示彩蛋 |
| rafalwilinski/vibecheck (lic=?) | ✗✓✗ | 留矩阵 | X 帖打分 Chrome 扩展（polarity+weight 合成裁决） |
| ryankung/rotom (LGPLv3) | ✗✓✗ | 留矩阵 | 本地 OpenAI/Anthropic 兼容网关 |
| ryanwaits/secondlayer (lic=?) | ✗✓✗ | 留矩阵 | 自托管 Stacks 故障分诊 Slack 门（薄） |
| samtay32/jev-system-architect (lic=?) | ✗✗✗ | 留矩阵 | skill：找脆弱语义逻辑转 typed（route/rank/verify/ask/escalate/execute，2.7KB 薄） |
| silverstein/minutes (MIT) | ✗✗✗ | 留矩阵 | 本地转写会议记（Jev 仅次要），cargo 安装 |
| simxnherrera/jevr (lic=?) | ✗✓✗ | 留矩阵 | 原生 R 客户端，provider-无关响应 |
| smithersai/smithers (lic=?) | ✗✗✗ | 留矩阵 | TS 工作流框架带 Jev session 通道（3KB 薄） |
| taruntomar122/jev-askable-arm (lic=?) | ✗✓✗ | 留矩阵 | 模拟 Franka 机械臂零样本英语目标（无图入 Jev） |
| twister915/typesafe-ai (lic=?) | ✗✓✗ | 留矩阵 | 又一个 Rust 客户端：async+blocking、lazy iterator |
| unicodeveloper/jevocks (lic=?) | ✗✓✗ | 留矩阵 | 终端股票决策（returns/range/volume 归约）；jev-trader.vercel.app 属此圈 |
| usenotra/notra (lic=?) | ✗✗✗ | 留矩阵 | 营销 GEO 平台（PLAN 称 300ms p50，README 无该指标），NOTRA_JEV_CLASSIFIER 环境变量 |
| dabit3/jev-experiments (lic=?) | ✗✗✗ | **留矩阵·存疑** | README 仅 **266B**（近乎空壳，称"可检视 Jev demo 集合"无实质），存在但内容缺席 → §五复核 |
| devagrawal09/jev-code (MIT) | ✗✓✗ | **留矩阵·存疑** | npm `jev-code` **0.0.1 占位、无工作命令**（自曝 release status）；概念（有界固定问题工作流）佳但落地缺席 → §五 |

## 三、跨批主题收敛（B8 是本战役"独立评测"外部复证集群）

1. **独立 + 预注册 = 抗循环自证的外部锚**（B8 头号）：assay-001 / jev-orderby-bench / legalforecastbench / jev-behavior-study / windtunnel / jev-sec-bench 六库**由第三方、先注册判据、再对 jev 打分**——正是 pi-warden/tax-doc "独立 checker 零共享代码"原则的生态级放大，直接支撑我们 DoD-2"金标不下降 + 每条附验收步骤"与 FINAL 主线"预注册复现"。
2. **校准跨数据集/跨 run 不稳**：assay-001（CLINC ECE 0.0204 校准 vs Banking 0.0936 过conf）、open-alternative（MMLU conf 高 5 点）、canny（跨 run 漂移 ~0.05）、litjev/pocketjev（默认未校准/option-relative）→ 复证 S-B6-1，并把"confidence≠correctness"细化到"**即便校准也随数据集与 run 抖动**"→ 对接 nous drift_within_round。
3. **阈值要"测"不要"拍" + 边界二次判**：janus"不发默认阈值、测一个"、every"±0.10 内重问取平均"、audio-beeper"0.72 是 POC 非生产"、tripwire"各阈值报 precision/recall/coverage"→ 直治我们"改档位不重测"缺陷族（第四/五复发），给出可执行替代：金标集扫阈值曲线 + 边界带复采样。
4. **去魅式免责成为成熟库标配**：hr98w/jev-visual、semif、windtunnel、pocketjev 均**主动声明"未跑 live Jev/不声称复现专有"**——与我们"作者自报 vs 实测"分级同律，可写成 ANALYSIS_TEMPLATE §7 复跑记录的话术范式。

## 四、反哺映射（B8 → jev_eval.py / novel 链路）

- **金标阈值曲线 + 边界带复采样**（janus/every）：jev_eval 的 Score 维度门与梗筛选命中率，应输出 threshold–coverage–accuracy 三线表，对 |p−阈值|<0.10 的条目**二次判定取均值或转人工**（等价引入"上下文不足"第四态的边界版）。
- **预注册复现协议**（assay/orderBy/legalforecast）：我们的 120 金标 `--compare` 应在改动**前**冻结判据与期望方向（像 jev-orderby 6 门），改动后只判"过/不过门"，杜绝事后挑指标（呼应 R-b 的"claim 不经复跑不重写"）。
- **margin-on-floor**（super-jev/jev-dsl B7）：金标记录里 top1 与 top2 差 <margin 时降级为"待人工"，与 B7 第 3 主题合流为 jev_eval 增列 margin。
- **语义熔断/伪装失败检测**（jev-resilience/tripwire/canny done-gate）：novel 链路"稿件体检"可借 done-check——模型宣称"改好了/无注味"但证据不足时抛 `SemanticFailure` 而非放行。

## 五、核账 / 遗留

- 头部处置统计由 `_rb8_precheck.py` 解析回填；量化 token（0.0204/0.0936/0.67/80.2/96.5/0.05/0.72/$0.012/$0.17/255/98%/±0.10 等）经 token→源文件反查核归因；矩阵须与 `_b8_meta.txt` 68 行做**行级 diff**（承 B7 教训，防幻影/漏库）。
- [ ] `dabit3/jev-experiments`（266B 近空壳）、`devagrawal09/jev-code`（npm 0.0.1 占位）→ FINAL 用 contents API 复核仓库真实规模，判定是"占位坑位"还是"正文在他处"。
- [ ] `kuhung/understanding-jev` 正文在自建站非 README、`usenotra/notra` PLAN 的 300ms p50 README 未见 → FINAL 决定是否按存在性通道二次取证（不臆测）。
- [ ] 一批 `lic=None/未标` 库（assay/orderBy/jevc-sec-bench 等）→ FINAL 授权表统一裁定。
- [ ] `bastani-inc/atomic`（64KB）、`reachjalil/jevlogs`（26KB）、`super-jev`（31KB）、`jev-orderby-bench`（35KB）README 偏大 → FINAL 抽查是否生成物/营销堆砌影响"深读性价比"。
- [x] RB8 复审轮闭环：`eval/b8_review.jsonl`（2×5，15,313B）`--check` ✓ 2/2 exit 0、反向盲审 10/10 自洽；`reports/b8_review.md` 记录 R7-a 教训左移生效（源头自查拦下 2 幻影行→脚本首跑即 PASS）、28 要点名实相符、独立评测集群升 FINAL 主线，并留 tripwire/canny 两项低置信自留交 FINAL 统一 rubric 复核。
