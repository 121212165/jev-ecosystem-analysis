# FINAL — JEV 生态分析战役总报告

日期：2026-09-19 ｜ 战役：`jev-analysis/PLAN.md` v2（9 批 B0–B8）｜ 池：**259 库**（`eval/inventory.csv` v7，去重）｜ 深读档：**11 篇**（`analyses/`）｜ 复审轮：RB0/RB3/RB4/RB5/RB6/RB7/RB8 + plan_review（`reports/*_review.md`）

> 数据源与口径以脚本为准：全战役覆盖核账 `_final_coverage.py`（259 行 / 唯一 259 / 全局幻影 0 / B1–B8 覆盖 0 缺）；各批处置数以 `reports/batchNN.md` 头部（由 `_rbN_precheck.py` 从 §二 处置列解析回填、并经行级 diff）为准。

## 〇、一页速览

| 指标 | 值 | 说明 |
|---|---|---|
| 分析池 | **259** | v7 去重清单，9 批全覆盖 |
| 深读建档 | **11** | DoD-1"≥8"超额；B1×3 / B2×2 / B3×2 / B4×1(晋级) / B5×2 / B6×1(晋级) |
| 浅采·要点 + 浅采 | **118** | B4 起分列（要点 62 + 普通 36），B1–B3 合并计 20 |
| 留矩阵 / 存疑 / 丢弃 | 112 / 7 / 4 | 存疑项全部挂 FINAL 二次取证 |
| 复跑记分板 | **4 次** | jevcal（首例零 key 全复跑）> tax-doc ≈ snifftest > pi-warden |
| 反哺建议 | **S1–S11 + 15 主题项** | 每条附 DoD-2 验收步骤 |
| 金标基线（keyless local） | Noul 37/44 = **84.1%**，MAE 0.187 | 120 金标 `--check` ✓；`--compare --provider local` 回归锚 |

## 一、覆盖矩阵：259 库全汇总

### 1.1 各批处置分布（v7 池，与各批 `_rbN_precheck` 一致）

| 批 | 主题 | v7 池 | 深采 | 浅采·要点 | 浅采 | 留矩阵 | 留矩阵·存疑 | 丢弃 |
|---|---|---|---|---|---|---|---|---|
| B0 | 官方基座/镜像目录 | 7 | 0 | 0 | 2 | 5 | 0 | 0 |
| B1 | 开源复刻 | 20 | 3 | —(并入浅采) | 6 | 8 | 1 | 2 |
| B2 | 游戏/实时决策 | 20 | 2 | — | 7 | 9 | 0 | 2 |
| B3 | 评分/排序/裁判 | 21 | 2 | — | 7 | 12 | 0 | 0 |
| B4 | Agent/浏览器 | 30 | 1(晋级) | 5 | 0 | 23 | 1 | 0 |
| B5 | 校验/护栏/文本质量 | 18 | 2 | 5 | 0 | 9 | 2 | 0 |
| B6 | 分类路由+审核 | 14 | 1(晋级) | 6 | 3 | 4 | 0 | 0 |
| B7 | SDK/Infra/DB | 61 | 0 | 18 | 15 | 27 | 1 | 0 |
| B8 | 其余（评测/基准富矿） | 68 | 0 | 28 | 18 | 20 | 2 | 0 |
| **合计** | | **259** | **11** | **62** | **58** | **117** | **7** | **4** |

> 口径注：① 六桶相加 **深 11 + 要点 62 + 浅 58 + 留 117 + 存 7 + 丢 4 = 259 ✓**；② B1–B3 早于"浅采·要点/浅采"分列（彼时合并记"浅采(含要点)"= 20），B4 起拆列；故 **B1–B8 浅采类 = 要点 62 + 普通浅采 56 = 118**（§〇 记分板即按此 B1–B8 口径：深 11 / 浅类 118 / 留 112 / 存 7 / 丢 4 = 252）；③ 本表 浅采 58 = 上述 56 + B0 的 2（adapter/skills 参照），留矩阵 117 = 112 + B0 的 5。

### 1.2 B0 基座/目录 7 库子矩阵（补齐 `batch00.md` 未逐行化的官方仓库 → 关闭 DoD-1 覆盖缺口）

`_final_coverage.py` 报 B0 有 5 库未以字面 slug 现于 `batch00.md`（该报告以通道表 + 目录 diff + 官方口径速查卡的形式覆盖，非逐库 stay/go 矩阵）。此处显式补行，使 DoD-1"100% 出现在 FINAL 矩阵"字面成立：

| 库 | 处置 | 依据 |
|---|---|---|
| typesafe-ai/system-one-adapter-python | 浅采 | 官方 adapter；`batch00.md §五` 已析"上游 vs 本地 patch 是否值得提 PR" |
| typesafe-ai/skills | 浅采 | 官方 agent skill 提问范式，直接对照我们的题目写法（`batch00.md §四`） |
| typesafe-ai/typesafe-sdk-js | 留矩阵 | 官方 JS SDK，基座参照（模式记录，无评测内容） |
| typesafe-ai/typesafe-sdk-python | 留矩阵 | 官方 Python SDK，基座参照 |
| vercel-labs/ai-python | 留矩阵 | Vercel AI SDK（与 B7 `vercel-labs/ai-cli` 同族） |
| vercel-labs/fx | 留矩阵 | Vercel 反应式运行时，基座参照 |
| yibie/awesome-jev | 留矩阵 | 主目录（清单源，非 Jev 应用） |

**按设计排除的 4 个平行目录**（`_final_coverage.py` 唯一"幻影"命中）：`cobanov/awesome-jev`、`AnotiaWang/awesome-jev`、`owner-B/awesome-typesafe`、`Anil-matcha/awesome-jev-by-typesafe` —— 它们是 inventory 的**抓取源目录**本身，不是被分析的 Jev 应用，故不入 259 池（非缺陷）。

## 二、DoD 逐条验收（PLAN §完成定义）

| DoD | 判据 | 结论 | 证据 |
|---|---|---|---|
| **1 覆盖** | 去重清单 100% 现于 FINAL 矩阵；深采 ≥8 单库档齐 | ✅ **PASS** | 259/259（§1.1 + §1.2 补齐 B0 5 库）；`_final_coverage.py` B1–B8 覆盖缺 0、全局幻影 0；深采 **11** ≥ 8，`analyses/` 11 篇七节齐 |
| **2 闭环回归** | 改造建议每条附后照；采纳改动合入后 `--compare`（120 金标）不下降 | 🟡 **PARTIAL（前置就绪，合入待做）** | S1–S11 每条附验收步骤（§3.1）；120 金标 `--check` ✓ exit 0；`--provider local --compare` 基线 Noul 84.1%/MAE 0.187 已锁为回归锚。**本战役止于"建议 + 验收步骤"，未将代码改动合入 `jev_eval.py`**，"合入后不下降"须待采纳轮执行——如实记 PARTIAL 非 PASS |
| **3 demo 实证** | ≥1 demo 复跑成功且带宣称指标复测表（偏差>30% 标红） | ✅ **PASS（超额）** | 首例 `abhixhek/jevcal` 零 key 全复跑 + 宣称复测表；另 `kyotofin/tax-doc`(261↔宣称逐字对)、`snifftest`(dry-run 离线臂)、`pi-warden`(离线 185 mock) 共 4 次。**residual**：未单建 `demos/` 目录，复测表内嵌各 `analyses/*.md §7`（见 §6 挂账） |
| **4 三玩法反哺基线** | 开工前基线 + 完工两项不劣化 + ≥1 结论进对应玩法改造建议 | 🟡 **PARTIAL** | 基线锚已 keyless 跑通（`--check ✓` + `--compare local`）；≥1 结论已进玩法建议（S5 保守对照列→循环性度量、snifftest 三带读数→判定枚举加 `no_judgment` 第四态）。"不劣化"门因本战役未合入代码而暂 N/A，随 DoD-2 合入轮一并验 |
| **5 隔离清零** | `plan_review.md` 隔离项已裁决、复核三件修订落地 | ✅ **PASS** | 四隔离项 `priority_coherence`/`cost_budget`/`gap_ranking`/`what_missing_most` 全 PRESENT；PLAN v2 已据此修订（优先级-排期换算规则消解 priority_coherence、成本预算上节制、风险册补"网络与获取"）；`quarantine.jsonl`(9 条) 不进默认 `--check`（`jev_eval.py:388` 隔离名单确认） |

## 三、反哺建议总表

### 3.1 S1–S11（B3 核心产出，`reports/batch03.md §四`）

| # | 建议（→ `jev_eval.py`/链路） | 源证据 | 验收步骤 | 强化批 |
|---|---|---|---|---|
| S1 | 题级阈值拟合（gold 拟合 conf 阈→目标准确率，半切留出，带 CI 锁文件，`--conservative` 取 95% 下界） | jevcal 拟合→留出→lock 全链路（已本地复现） | 合成已知最优阈分布，留出集准确率落目标 ±2pp | B8 janus/every |
| S2 | gold lint 前置（概率和≈1±.02、samples=5、blind=agree、rationale 非空、note 含"自写合成样本"、qid 唯一、primitive 合法） | jevcal lint + zhuyansen 冻结哈希标签 | 各造 1 违规坏副本，7 类全部非零退出并指认到行 | 已实现于 `--check` ✓ |
| S3 | confident-and-wrong 优先表（高置信判错按 conf 降序 = 人工复审首清单） | jevcal "confident and wrong 优先处理" | 注入 1 条高置信判错，须现于表首行 | B4 pi-warden quarantine 回灌 |
| S4 | 口径声明字段（每个置信度数字强制标 top_prob/margin/entropy/API-confidence） | jevcal `--measure auto` 四口径对比 | 每个置信度数字旁都有口径标签，漏标即 lint 失败 | B7 dakdevs/inanna |
| S5 | 保守对照列（`llm_only` 不经 Jev 修正直评，两列差 = 循环性度量，并排展示） | zhuyansen 三标签：jev_only +0.053/final +0.012/llm_only −0.028 | 造 20 条含已知偏好错 gold，差值符号与注入方向一致 | B6 循环自证、B8 assay |
| S6 | 聚合纪律（中间量不四舍五入、gold 先冻结带日期+SHA-256 再打分） | zhuyansen 未取整均值 + "freeze before scoring" | 打乱输入顺序重跑，汇总逐位不变 | B4 两段式路由 |
| S7 | overall≠轴均值（总分要么声明"=算术平均"要么单设 direct-choice 问） | jevslop overall 是 Jev 直接 choice | 20 样本两法对比，一致率<90% 则强制 direct-choice | B8 八维 Score |
| S8 | 存在性预检入 state（引用先核验存在，不存在→拒评标 error 而非给低分） | citation-verifier 存在否则丢弃 | 注入 1 条虚构引文，输出须为"存在性校验失败，拒评" | B0 存在性通道 |
| S9 | 分位数 flag 阈值（异常标记触发阈取该题分布 P98，floor 0.5） | jevmeter flag=P98 floor=0.5 | mock 分布运行，输出阈值与 P98 误差<0.01 | B8 super-jev margin-on-floor |
| S10 | 乱序翻转率并报（同报"重复翻转率"与"乱序翻转率"两数） | mahlernim 乱序 13–14% vs 重复 1–2% | 5 采样中 2 次乱序，两翻转率字段并出且乱序≥重复 | B7 blakestone 32/200 |
| S11 | 模型/协议版本戳（每次 run 记协议模板哈希+日期+通道，报告头强制字段） | 负结果库锚死 jev-1.13.0；zhuyansen 记 model 字段 | 连跑两次含相同 protocol-hash；改协议后 hash 变并标"不可与旧轮对比" | B8 预注册协议 |

### 3.2 B4–B8 主题级净新增（`reports/batch0X.md §四`）

- **独立 checker 零共享代码 + 捷径陷阱 fixture**（B4 pi-warden / B6 / B8 八库放大）：自评产物送"独立一判"（我们用逆序盲审充当），并排印"flag 数/确认数"双列 → 复测表格式增补；生态级支撑 DoD-2。
- **判定枚举加 `no_judgment` 第四态**（B5 snifftest 三带读数 0.4–0.6=显式无判定）：区别于"低置信"，上下文不足/边界带应显式转人工而非硬判 → 与 S9 阈值带合流。
- **改档位不重测 → 金标阈值三线表 + 边界带二次判**（B6 gtaras7 "政策改后重评零成本"、B8 janus/every/audio-beeper/tripwire）：Score 维门与梗筛选输出 **threshold–coverage–accuracy 三线表**，对 `|p−阈值|<0.10` 二次判定取均值或转人工。
- **决策位与记录位分离 + 多步取 min + 门限下兜底**（B6）：置信=链上各步取 min，高于门执行、低于门兜底；`permit(state,action)` 域规则独立于 confidence（B7 super-jev）。
- **done-check / 语义熔断**（B4 droidrun "DONE≠证据"、B8 canny/tripwire/jev-resilience）：模型宣称"改好了/无注味"但证据不足时抛 `SemanticFailure` 而非放行 → novel 链路"稿件体检"直接可借。
- **ECE 与 AUC 必须并报 + 校准随数据集/run 抖动**（B5 winnow、B7/B8 assay/open-alt/canny）：校准汇报纪律，且"即便校准也跨数据集/跨 run 不稳"（CLINC ECE 0.0204 校准 vs Banking 0.0936 过conf；跨 run 漂移 ~0.05）→ 对接 `drift_within_round`。

## 四、复跑记分板（11 深读档，DoD-3 证据）

| 库（批） | 零 key 可跑性 | 复跑结果 | 宣称 vs 实测 |
|---|---|---|---|
| abhixhek/jevcal (B3) | ✅ 内置模拟器 | **全复跑成功（战役首例）** | 拟合→留出→lock 全链路可跑，带宣称复测表 |
| kyotofin/tax-doc (B6) | ✅ 数据核验 | 复跑成功 | `criteria.json` 独立数得 **261 key** ↔ 宣称"261 IRS forms"逐字对 |
| d.willoughby/snifftest (B5) | ✅ `--dry-run` 离线臂 | 部分成功 | 离线臂完整可用（§7 实测） |
| devmortimer/pi-warden (B4) | ✅ 离线三层 | 部分成功 | 185 mock 测试 / dry-run / 无 key 降级，绕开 pi-tui |
| theoleecj/openjev (B1) | △ 未跑 live endpoint | 用公开记录复现 | 分层梯子 0.440→0.686→0.813，每条带 committed 溯源 |
| zhuyansen/rerank-eval (B3) | △ 需数据 | 三标签重打分 | 循环偏置 −0.028/+0.012/+0.053 肉眼可见 |
| coldteadotai/abide (B5) | △ bench 可跑 | 成本实测带日期 | "Measured 2026-09-18"，flag 39 确认 10 并排印 |
| jaredpalmer/kev (B1) | ✗ CPU-only 跑不动 | 环境受阻 | HF 权重 ~1GB；ECE 0.065→0.031（作者自报） |
| mapika/decider (B1) | ✗ 需 CUDA | 环境受阻 | bf16 ~4GB；94 任务全表（作者自报） |
| browser-use/jev-ultrafast (B2) | ✗ 需 key + CDP | 环境阻断 | headline "7.1 s" 正文收敛 7,073 ms（边界显式） |
| romanslack/jev-drone (B2) | ✗ 需 GL + key | 环境阻断 | 全批唯一 no-Jev 消融表；早期竞技场 0/3 负面自报 |

**记分板序**：jevcal（全复跑）> tax-doc（数据核验逐字对）≈ snifftest（离线臂）> pi-warden（离线三层）；其余 7 库受 key/硬件/网络阻断，如实记"环境受阻"、未臆测通过。

## 五、跨批主题收敛（战役主命题）

1. **confidence ≠ correctness（全场最强线）**：B4 pi-warden → B5 → B6 → **B7 内 5 库 + B8 assay/open-alt** 累计成 10+ 库同调；细化为"即便校准，也随数据集与 run 抖动"。
2. **循环自证是评测的头号效度威胁**：B3 zhuyansen 三标签（llm_only −0.028）、B6 金标 judge 与被评模型家族重叠会翻符号、**B8 八库以第三方预注册提供外部锚**——前七批的自证短板由 B8 补上。
3. **阈值要"测"不要"拍" + 边界二次判**：S1/S9 + B6/B7/B8 反复出现，直治我们"改档位不重测"缺陷族（第 4/5 次复发）。
4. **判定与行文/执行分离 + done-check**：B2/B4/B6/B8 的"独立 checker 零共享代码""伪装失败检测""语义熔断"，与"作者自报 vs 实测"分级同律。
5. **宣称纪律 = 成熟库标配**：openjev（每条带 committed 溯源）、semif/windtunnel/pocketjev（主动声明"未跑 live/不声称复现专有"）→ 写成 ANALYSIS_TEMPLATE §7 复跑话术范式。

## 六、遗留挂账总表（跨批 deferred → 采纳轮处理）

- **存在性复核**：`vercel-labs/ai-cli`（B7 三 ref 全 MISS）、`vlad-terin/*`（B6）→ 用 jsDelivr + contents API 通道二次取证（不臆测）。
- **空壳/占位判定**：`dabit3/jev-experiments`（266B 近空壳）、`devagrawal09/jev-code`（npm 0.0.1 占位）→ contents API 核真实规模，判"占位坑位"vs"正文在他处"。
- **正文非 README**：`kuhung/understanding-jev`（自建站）、`usenotra/notra`（PLAN 的 300ms p50 README 未见）→ 存在性通道取证。
- **授权统一裁定**：一批 `lic=None/未标`（assay/orderBy/sec-bench/jevsql 等）→ 授权表统一定档。
- **README 膨胀抽查深读性价比**：`atomic`(64KB)/`jevlogs`(26KB)/`super-jev`(31KB)/`jev-orderby-bench`(35KB)/`skillranker`(113KB) → 抽查是否生成物/营销堆砌。
- **多语言同名 SDK 去重说明**（B7）：jev-go×2、typesafe-sdk-php×3、sqlite-jev 系 → 记"冗余度作热度证据、非独立设计数"。
- **demos/ 目录未建**（DoD-3 residual）：复测表现内嵌 `analyses §7`，如需对外交付可抽出打包。
- **定级 rubric 统一复核**（低置信自留项，见 `b7_review.md`/`b8_review.md`）：`rajivkuriakose`/`tripwire` "③✗仍可进要点" 张力 → 定"浅采·要点须含 ≥1 带对照的量化点" rubric。

## 七、过程纪律沉淀（方法论反哺）

- **先脚本后文档**：各批处置统计由 `_rbN_precheck.py` 从矩阵解析回填，文档头部留占位、脚本跑过再回填（B4 起严格执行，B5 首版手写"浅6留10"被脚本打脸=第四复发）。
- **R7-a（B7 立、B8 验证）**：处置 Counter 自洽 ≠ 交付完整；矩阵**必须与权威元数据池做行级 diff**。B7 靠 `header ok==POOL` 逼出"缺 3 库 + 多 2 幻影"；B8 已内化为**脚本前自查删除**，首跑即 PASS（进步=拦截成本左移，但缺陷产生率未降 → FINAL 后自我约束：写矩阵前先落 slug 列表核对池）。
- **R7-b（B7 立）**：体积/量纲类宣称（KB、tokens/req、ms）不属"正文数字"，**单独走 `getsize`/字节核**，勿混进 body-token grep（否则必假 MISS）。skillranker "113KB"（113,274B ÷1000）曾被 ÷1024 脚本误判 MISMATCH → 报告有字节背书时改脚本非改报告。
- **缺陷族分类**：① 计数漂移（B0 59vs67 / B2 / B3 / B5）；② 数字张冠李戴（真数字绑错库，token→源文件反查唯一能抓）；③ 枚举不完整/污染（B7/B8 幻影行+漏库，POOL 行级 diff 抓）；④ 过早勾 [x]（B5 §七）。
- **LLM-as-Jev 复审轮**：每批 `eval/bN_review.jsonl`（2×5）`--check` ✓ + 反向盲审 ≥85%；低置信自留项**不强抬**（rajivkuriakose 0.62、tripwire 0.60、canny 0.70），交 FINAL 统一 rubric。

## 八、Top demo 榜 + 本地链路落地优先级

**最高杠杆典型 demo（按"可直接迁就我们链路"排序）**：
1. `abhixhek/jevcal`（B3）— 零 key 全复跑、阈值拟合工具化，正解我们"阈值抄用不可靠"，落地 S1/S3/S4。
2. `devmortimer/pi-warden`（B4）— 零共享代码 checker + 捷径陷阱 + quarantine 回灌，落地 S3 + DoD-2 独立确认。
3. `zhuyansen/jev-search-rerank-eval`（B3）— 三标签列去循环性（llm_only），落地 S5。
4. `danrwilloughby/snifftest`（B5）— 三带读数第四态 + 植入缺陷三臂 eval，落地"去 AI 味"链路 `no_judgment`。
5. `theoleecj/openjev`（B1）+ `kyotofin/tax-doc`（B6）— 宣称纪律 + 严格基准 34×/6× 范式，落地 §7 复测表四列格式。

**采纳轮落地优先级（工程动作，接续本战役）**：P0 = S2（已实现，扩 7 类 lint 到全 gold）+ S11 版本戳 + S6 冻结哈希（纯文档/校验、零依赖、立刻可合入并跑 `--compare` 验不劣化）；P1 = S1 阈值拟合 + S3 优先表（需新增 `fit_thresholds.py`）；P2 = S5 保守对照列（需第二打分通道，成本最高）。合入任一改动后必跑 `--provider local --compare`（120 金标）对基线 84.1% 验证不劣化——闭合 DoD-2/DoD-4 的 PARTIAL。
