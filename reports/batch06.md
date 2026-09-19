# batch06 — B6 分类路由 + 内容审核批（扫读批·深读名额经晋级获得 + 顺路三件 tarball 核数）

日期：2026-09-19 ｜ 池：**14 库**（v7）｜ 状态：**完成**（遗留见 §七）
**深采 1 · 浅采·要点 6 · 浅采 3 · 留矩阵 4 · 丢弃 0**（合计 14；统计由 `_rb6_precheck.py` 从 §二 处置列解析回填。0xnatoshi 头条"省 ~60%"系写前精读源文件 L11 拦下的误写，非事后更正——见 §六；24 个数字 token 经脚本 token→源文件反查全 HIT、0 MISS）

## 一、深读名额与晋级说明 + 顺路核数结论

- 本批 PLAN 定位"只扫读进矩阵"（B4/B6 各 1 深读名额，经晋级扫描产生）。
- **晋级 = kyotofin/tax-doc-classifier（193★）**：三标准全 ✓ 且是全批唯一"可复现严格基准（错 或 置信<0.95 皆计错）+ 与被替代 LLM 同机同时段基线对照（34× 省钱 / 6× 提速 / 30→261 表单）+ 数据溯源（criteria.json 由 IRS 官方 PDF 生成）+ 诚实 limits（'先在你自己页面上校准再选门限'）"的评测设计库。零 key 离线臂**实测可跑**（§三，本战役第 4 次复跑成功：clone 49KB → install 18.5s → typecheck exit0 → vitest 3/3 → criteria.json 独立数得 261 表单与宣称逐字对上）。
- 深读档：`analyses/kyotofin__tax-doc-classifier.md`
- 预排序次名 `gargpratyush/jev-router` 169★：真·多作者活跃项目（I7 见 §五），但 Jev 内容集中在路由 UX 呈现（p=0.98/复杂度 0.82），无独立可复现基准面 → 浅采（热度不折名额，B1/B2/B4/B5 同尺）。
- **顺路三件挂账核数（B4/B5 → B6 同趟）全部核实通过**：
  1. **abide** `benchmarks/replay/` → 已提交 `results-2026-09-18.json`(9,243B) + README；headline **Edits 39 flagged→10 confirmed(26%) / Turns 15 flagged→11 confirmed(73%)** 与 B5 挂账数字**逐字对上**。
  2. **zhuyansen/jev-search-rerank-eval** `results/robustness.md`(2,713B) + `per_query.csv`(95,919B) + `src/jse/robustness.py` 齐备 → 换 judge 重打分**确已落地**；真实调用证据 `jev-1.13-20260917` + eval 成本 $0.066。
  3. **pi-warden** `docs/guards.md`(31,930B) + `eval/reports/` **12 个已提交批次报告** 齐备 → headline"150 配对 run / 违规 6→0"经 README L51 分表**自洽复核**（glm 60→5 + deepseek 90→1 = 150→6，warden 两 cell 均 0）；B4 §2 措辞无需更正。

## 二、14 库 stay/go 矩阵

| 库（★/lic） | ①复跑②量化③调用 | 处置 | 一句话依据 |
|---|---|---|---|
| kyotofin/tax-doc-classifier (193/Apache-2.0) | ✓✓✓ | **深采（晋级）** | 可复现严格基准 + 34×/6× 同机基线 + 261 表单数据溯源 + 诚实 limits；零 key 离线臂实跑通过 |
| 0xnatoshi/jev-codex-router (61/MIT) | ✗✓✓ | 浅采·要点 | 7 天自身 Codex replay 回测，决策 ~$0.00003/0.6s·turn，头条**省 ~60%**（非 80%——80% 是"naive 全前沿回退反吞 savings"的另一码事）；每 turn 落决策日志供校准 |
| brainstormity/jev-moderation-bot (29/lic=None) | ✗✓✗ | 浅采·要点 | 四级升级 + **动态假阳学习**：管理员 pardon → 存为 safe precedent 回注后续检查（赦免样本回注 context）；profile 扫 10–100 条 |
| abovecolin/ha-jev (17/MIT) | ✗✓✓ | 浅采 | 智能家居 Choice 判定：`degraded`@0.59 且次选 marginal@0.40、置信仅 0.46 = 模型自报"数据不足"；act-above-0.6 门限 + 兜底 agent 转交 |
| godsboy/jev-agent-skill-router (7/MIT) | ✗✓✓ | 浅采·要点 | 68/72(94.4%) vs 词法 51/72；**自曝**"routing questions 中途改过、未改切分仅 64/72、Neither run establishes calibrated probabilities、typed output 只保形状不保正确" = 测试集污染自检范本 |
| adarshmishra07/jcm-router (2/MIT) | ✗✓✓ | 浅采·要点 | 诚实负结果：早期全路由 309 请求花 $106.73 vs 什么都不做 $87.19 = **净亏 $19.53**（$17.12 来自主聊天）；"router 只在切换划算处切换"由此亏损故事逼出 |
| codealive-ai/mastra-jev-moderation (2/MIT) | ✗✓✓ | 浅采·要点 | 58 cases=9/9 拦截 hostile + 0/49 误杀真实问题，median 0.39–0.44s ~920 token；**category 标签永不参与 gate 决策**（只 blocking 判）+ 3 次连败熔断 60s fail-open |
| cephalization/jev-triage (1/MIT) | ✗✓✗ | 浅采·要点 | 每 issue 固定 typed 问 + 人工纠正**全部保留并回显**（金标修正闭环，对照我们 drift_within_round）；pure `decide()` 策略与重启不卡死 |
| gargpratyush/jev-router (169/MIT) | ✗✓✗ | 浅采 | 真多作者活跃项目（I7 通过），把 Claude Code 任务路由到最便宜可用模型；但 Jev 面止于路由 UX 数值展示，无独立基准 |
| mejiasd3v/pi-jev-router (6/MIT) | ✗✓✗ | 浅采 | 每 turn 前置 Jev 检查 skill pin；192,000 UTF-8 byte 上限 + 超时 3× 重试共享 ceiling；需 Vercel AI Gateway key |
| giesn/typesafe-jev-workflow (4/lic=None) | ✗✓✗ | 留矩阵 | LangGraph 邮件意图二分类；作者自标"smoke check 非 accuracy benchmark"（诚实但薄，2.4KB） |
| gtaras7/typesafe-jev (2/MIT) | ✗✓✗ | 留矩阵 | "判定与算术分离 → 改权重/问题 20ms 零成本重评全部候选"一句话点题（与 tax-doc formConfidence、pi-warden 独立 checker 同宗），但 hub README 薄（1KB）指向 cv-screen |
| prismhq/jev-router (2/MIT) | ✗✗✗ | 留矩阵 | LiteLLM 代理层，Jev 做单 model-id 前端路由；请求最小化摘要，无量化面 |
| jekozyra/pi-typesafe-router (0/MIT) | ✗✗✓ | 留矩阵 | 多网关（TypeSafe/Cloudflare/Vercel/OpenRouter）自动路由；`npm run check` 离线；0★ 新建薄 |

## 三、零 key 复跑记录（tax-doc-classifier）+ 顺路核数明细

**tax-doc-classifier 离线臂（本战役第 4 次复跑成功）**：

| 步骤 | 命令 | 结果 |
|---|---|---|
| 克隆 | `git clone --depth 1`（gh-proxy） | 仓库总 size **49 KB**，秒下 |
| 装依赖 | `pnpm install` | 18.5s（仅 fflate + tsx/typescript/vitest，全 npm registry 直连） |
| 类型 | `pnpm typecheck`（tsc --noEmit） | **exit 0** 干净 |
| 测试 | `pnpm test`（vitest run） | **3/3 通过**（src/ids.test.ts） |
| 数据核验 | 独立 `json.load(data/criteria.json)` | **恰好 261 key** ↔ README"261 IRS forms"逐字对上 |

- 关键：测试第 1 条即"criteria.json 每个 id 必合 `ID_GRAMMAR`"的**数据完整性门**，README 所述"test suite refuses a bad criteria.json"属实、离线可验。
- **未跑臂**：`pnpm eval`（需 `TYPESAFE_API_KEY`，走真实 Jev 调用）——依"跑不动记录后不强跑"止步；headline 的 0.00%/5.05% 严格错误率与 34×/6× 基线对照属**作者自报、结构可复现**（`pnpm eval` + TaxCalcBench 外部语料，不随仓分发）。

**顺路三件核数（同趟）**：见 §一末。abide 用 `git/trees` 确认 `benchmarks/replay/` 提交物存在后 raw 抓 README+results.json，headline 39/10·15/11 逐字命中；zhuyansen 抓 `results/robustness.md`+`results.md`，发现 jev-score 增益**随信任哪个 judge 翻符号**（final +0.012 不显著 / llm_only **-0.028 显著负** / jev_only +0.053 显著正）；pi-warden 枚举 `eval/reports/` 12 批共 474 sessions（含早期 5-task 探索批），确认 headline 150/6→0 系 15-task 设计（glm5+deep1）而非全批总和，另新证 L62 夜间稳定性 **109 cycles/13,952 cases/100%/zero drift** 与 L77 作者自曝循环性免责。

## 四、反哺本地链路（jev_eval.py）改造建议

| 编号 | 来源库 | 可移植模式 | 落到我们链路的哪一处 |
|---|---|---|---|
| S-B6-1 | zhuyansen robustness | **金标 judge 与被评模型家族重叠 = 循环自证，会使增益翻符号** | jev_eval `--compare`：至少一组金标须由**非 Jev 家族**标注，或报"judge 换源后一致率"作鲁棒性列（我们现在 LLM-as-Jev 自标自评，正踩此雷，须显式标注这一局限） |
| S-B6-2 | godsboy | **中途改题=测试集污染，须同时报"未改切分"分数** | 我们改判据/改维度题时，保留一份 frozen split 报双数（改前/改后），不单报改后 |
| S-B6-3 | mastra | **决策位与记录位分离**：category 只记录、永不 gate；blocking 是唯一 yes/no 门 | Ending 二级树/维度题：把"仅用于日志的分类标签"与"参与 pass/fail 的判定"物理分开，防标签泄漏进分数 |
| S-B6-4 | tax-doc | **置信=多步取 min，门限上执行/门限下兜底**；且"先自校再选门限" | 多步判定（如梗筛选→复核）复合置信取 min 而非均值；热区块门限须先跑一轮校准再定值 |
| S-B6-5 | jcm-router | **净亏就缩小动作面**：router 只在"切换划算"处切，主链路不动 | 我们引入任何"更聪明的默认路由"前先算它相对"什么都不做"基线的净收益，负则收窄触发面 |
| S-B6-6 | moderation-bot / triage | **赦免/纠正样本回注 context + 全保留回显** = 金标修正闭环 | 盲审协议：被驳回的判定存为"安全先例"回注下次检查，且纠正历史可见（对照 drift_within_round 追踪） |
| S-B6-7 | pi-warden eval README | **评分器与被测零共享代码 + 负结果留表 + claim 不复跑即重写 + 每宣称挂 report 目录** | 与我们 DoD-2/复跑纪律同构，可反向引用作为"独立 checker"设计的社区先例写进 FINAL |

不抄项：ha-jev 的 Assist 语音转交、0xnatoshi 的 Codex lane 分层（依赖其私有回放数据，不可迁）。

## 五、I7 提交分布抽查

| 库 | commits(≤40) | 作者分布 | 活跃天数 | 判读 |
|---|---|---|---|---|
| tax-doc-classifier (193★) | 2 | 单作者 Nedwize | 1（09-18） | **代码本体是实的**（261 表 criteria.json+src+测试+eval），属成品整包首发；但**星速 ≫ 提交速**（<1 天 193★），star 只作传播度证据，不作成熟度证据 → 挂 FINAL 复查 |
| gargpratyush/jev-router (169★) | 40+（封顶） | 多作者：gargpratyush+Pratyush Garg（同人）37、MrJev 1、phetzy 1、gargpratyush_microsoft 1 | 3（09-17~19） | 健康真项目，多贡献者，活跃迭代 |
| 0xnatoshi/jev-codex-router (61★) | 15 | 单作者 0xNatoshi | 1（09-17，后停更） | 单日首发即停更；~60% 省为自身 replay 自报，无外部验证 → 浅采·要点恰当 |

## 六、核账 / 缺陷记录（本批实跑）

- **写前拦下 1 起头条数字误写**：0xnatoshi 头条节省一度按 fetch 预览写成"~80%"，精读源文件 L11 校正为 **~60%**（80% 是"naive 全前沿回退反吞 savings"的另一处数字）。属 B4"张冠李戴/数字漂移"缺陷类的**写前拦截**，靠"逐库 grep 精确行"而非批量预览。
- 头部处置统计将由 `_rb6_precheck.py` 解析矩阵列回填，数字型宣称（261/314/38/5.05/34/60/19.53/68/94.4/64/920/0.7 等）由脚本 token→源文件反查核归因。

## 七、挂账（移交 FINAL 或后续）

- [ ] tax-doc-classifier：193★/2-commit 的星速-提交速背离，FINAL 复查是否 TypeSafe 官方 showcase 助推（影响"热度不折名额"尺度一致性）。
- [ ] tax-doc-classifier 真实 `pnpm eval` 0.00%/5.05% + 34×/6×：需 key，属"结构可复现、数值作者自报"，FINAL 标注证据等级。
- [ ] giesn/typesafe-jev-workflow（4★）+ brainstormity/jev-moderation-bot（29★）Lic=None → FINAL 授权表统一裁定（badge 与 API spdx 冲突排查）。
- [x] ~~zhuyansen "9,831 labelled pairs"（语料）vs "164 eval queries"（评测子集）口径：确认 B3 深读档未把二者混记~~ → **已核 by B6：未混记**（B3 档 L3 写"9,831 标注"=pairs 作语料、另引 30 查询子集，未把 9831 当 queries）。**诚实修正**：B3 档 L3 已引用 −0.028/+0.012/+0.053 换 judge 翻符号——故 S-B6-1 是对 B3 已有发现的**跨批复证**（增强为多库现象），非本批新 claim。
- [ ] 顺路三件核数**已完成**，回写 B4/B5 挂账复选框为已勾（本批 §三留证）。
- [x] RB6 复审轮已闭环：`eval/b6_review.jsonl`（2×5，`--check` ✓ exit0，盲审 10/10）+ `reports/b6_review.md`；审出 1 项销账跟进（B4/B5 三挂账已回勾），本轮已执行

## 八、结论

B6 全 14 库进矩阵，晋级深读 tax-doc-classifier（第 10→11 篇深读档），零 key 离线臂第 4 次复跑成功并独立复核 261 表单宣称。顺路清掉 B4/B5 遗留的三件 tarball 核数，全部核实通过——其中 pi-warden"150/6→0"经分表自洽、无需更正 B4，zhuyansen 换 judge 翻符号（B3 已记、B6 取提交物复证 → 升为跨批主线）。本批方法论收获最重：三个库（godsboy 改题污染、zhuyansen judge 循环、pi-warden 独立 checker）从不同角度收敛到同一条我们链路正踩的坑——**自评自证的循环性**，应写进 FINAL 作为改造建议主线。
