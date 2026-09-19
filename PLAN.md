# JEV 生态库分批分析计划

**版本**：v2（2026-09-19，按 `reports/plan_review.md` Jev 体检四项硬伤修订：①排期改为分层计时+双档；②新增完成定义 DoD 与回归闭环；③典型 demo 入选标准写死；④风险册补『网络与获取』与成本预算；⑤优先级-排期换算规则消解隔离项）

**目标**：从 GitHub 的 ~170 个 JEV 相关库中，分批筛选典型 demo 与可移植模式，反哺本地 `本地网文创作系统（独立私有仓，未随本仓发布）` 的 Jev 评测链路（`src/eval/jev_eval.py`，local|adapter|jev 三 provider 已建成）。

**信息源（已核实）**：
- 主目录：`yibie/awesome-jev`（13 类、~170 条，含收录标准与"批量脚手架"警告）
- 平行目录：`cobanov/awesome-jev`、`AnotiaWang/awesome-jev`、`owner-B/awesome-typesafe`、`Anil-matcha/awesome-jev-by-typesafe`（有 8 个项目视频 walkthrough）
- 社区展示：madewithjev.com（Agents/Browsers 等分类页）
- 复现追踪：HF Space `multimodalart/jev-reproductions-tracker`（开源复刻 checkpoint 汇总）
- 本地积累：Trae 会话（2026-09-18/19 部署 MCP server、DeepSeek 适配器、5 轮闭环迭代、网文审稿三玩法）+ Clippings 两篇（yibie 使用手册、卡兹克发布解读）

**方法论**：每批 8~12 个库，用 `ANALYSIS_TEMPLATE.md` 逐库填写；批次结束写 `reports/batchNN.md`；全部完成后写总对比矩阵。深读只给"典型 demo"，其余扫读 10 分钟内定去留。

**优先级-排期换算规则**（v2 写死，消除歧义）：优先级决定**深读名额与是否要求逐库建档**，不决定排期长短——高/最高 = 有 ≥2 个深读名额且逐库建档；中 = 1~2 个深读名额、其余建档；低 = **只扫读进总矩阵，不建单库档**，扫读固定 10 分钟/库。故 B7 库数最多但排期最短是自洽的。

**典型 demo 入选标准**（v2 新增，B1/B2 深读挑选用，三条全满足才深读）：
1. **可一键复跑**：README 给出完整脚本或 ≤3 步命令，依赖可锁定；
2. **有量化宣称**：时延/成本/校准度/一致率至少一项有具体数字（如 7s $0.0039、n=1316 校准 0.83、35ms、182ms 中位）；
3. **真实调用证据**：能出示题目原文/日志/录屏/GIF 证明真的调用了 Jev 接口（防脚手架拼凑，与模板第 1 节"是否真实调用"核查联动）。

**demo 验收**：复跑成功后填**原始宣称指标复测表**（宣称值 vs 实测值 vs 环境），偏差 >30% 标红并回写该库分析文档，不允许只贴截图。

---

## 批次总览

| 批次 | 主题 | 库数 | 预估耗时 | 优先级 |
|---|---|---|---|---|
| B0 | 官方基座与镜像目录 | 8 | 0.5 天 | 必做，先决 |
| B1 | 开源复刻（本地可跑） | 10 | 1 天（扫10×10min+深读3×2h+复跑1） | 最高（与我们排队现状匹配） |
| B2 | 游戏/实时决策典型 demo | 8 | 1 天（扫8×10min+深读2×2h+复跑1~2） | 高（"典型 demo"主来源） |
| B3 | 评分/排序/裁判（与评测链路同构） | 10 | 1 天（扫10×10min+深读2×2h） | 高 |
| B4 | Agent 决策与浏览器自动化 | 12 | 0.5 天（只扫读进矩阵） | 中（深读名额 1，经晋级获得） |
| B5 | 校验/护栏/文本质量 | 12 | 0.75 天（扫12×10min+深读1×2h） | 中（去 AI 味相关可提级） |
| B6 | 分类路由 + 内容审核 | 14 | 0.5 天（只扫读进矩阵） | 中（深读名额 1，经晋级获得） |
| B7 | SDK/Infra/DB 集成 | 16 | 0.5 天（只扫读进矩阵） | 低（够用即可，不建单库档） |
| B8 | 金融/法律/标注/其余 | 8 | 0.25 天（只扫读进矩阵） | 低 |
| 汇总 | FINAL 矩阵+报告 | — | 0.5 天 | — |

加总 = **6.5 个全天（13 个半天）**；标准档排期 **7 个全天含 8% 缓冲**，压缩档见执行节奏。缓冲的 0.5 天专门支出 B4/B6 各 1 个库的**晋级深读**（扫读中命中三条入选标准才晋级），超支即挤占 FINAL 日并记录为 DoD 未完成项。

---

## B0 — 官方基座与镜像目录（先决）

- typesafe-ai/system-one-adapter-python：本地已改版（site-packages 动过）。对照上游差异、多厂商 patch 是否值得提 PR
- typesafe-ai/skills：官方 agent skill 的提问范式，直接对照我们的题目写法
- docs.typesafe.ai 的 patterns / api / confidence：设计模式、置信度官方口径
- evals.typesafe.ai：Workflow Evals 方法论（策略拆 harness，Noul/Choice/Score + 代码规则）
- yibie/awesome-jev：主目录，兼各批次入口
- cobanov / AnotiaWang / owner-B / Anil-matcha 四个平行目录：diff 出 yibie 未收录的库，补进各批次
- madewithjev.com：社区 build 展示，抓遗漏

产出：完整待分析清单（去重）+ 官方口径速查卡。

## B1 — 开源复刻（最高优先：排队没排到也能本地跑通）

- AlexWortega/openjev (HF, Qwen3.5-4B NLI)：predict/rerank/grade 三方法；Flappy Bird 与 Doom 零样本
- us/jev-local：兼容 `/v1/systemone` 的 drop-in server，n=1316 校准数据（0.83）——直接替换我们 local provider 后端的第一候选
- TianyuCodings/NanoJev：0.6B 全分布输出，训练管线+权重+数据集开源
- NandhaKishorM/laya：非自回归、单次约 35ms，PyPI/HF 均发布
- jaredpalmer/kev：Qwen2.5-0.5B 可训练复刻，MacBook 可跑，附评测脚本
- Mapika/decider：Qwen3.5-2B 微调，单遍输出校准概率
- TheoLeeCJ/openjev：接口模式复刻（与 AlexWortega 版对比）
- zhihz/openjev：双语概率问答——中文能力是网文场景刚需
- r-ms/mini-jev、drinkmoonshine/parallel-constrained-decoding (HF)：轻量参照；后者即 yibie 实测 0.82/0.70 校准差距的那个

判定标准：能否支撑 `JEV_PROVIDER=local` 走我们的盲审协议（自一致率 ≥85%）；中文 state 表现。深读名额 3，按方法论节三条入选标准筛。
典型 demo 期望：本地 zero-shot 玩游戏的完整回路（读状态→提问→执行）。

## B2 — 游戏/实时决策（"典型 demo"主矿）

- fhshaik/typesafe-mario、shantanugoel/mario-jev：两个 Mario 实现对照，state 设计差异（RAM 观察 vs 结构化特征）
- browser-use/jev-ultrafast：社区最出名 demo，7 秒查机票 $0.0039；动作空间=Choice，LLM 只在打字时兜底
- milanboers/jev-plays-pokemon：game state 转文本→typed questions→确定性代码执行，与"审稿→打分→改稿"同构
- thruwire/foreman：独立判断实现是否完成/测试是否充分——completion gate 范式
- ably-labs/jev-pong：Jev vs LLM 头对头擂台，评测可视化可借鉴
- phyous/tsai-sc、RomanSlack/jev-drone：高频决策+预算控制的边界案例
- kavehmz/typesafe-playground：多个小实验合集，适合截图做教程素材

典型 demo 期望：挑 1~2 个本机复跑（优先 OpenJev 本地路线，不耗 API key），验收按方法论节『原始宣称指标复测表』执行。

## B3 — 评分/排序/裁判（与 jev_eval.py 同构，直接反哺）

- TKY-27/JevSlop：八维 Score 轴 + 普通代码合成 0-100 总分——我们情绪密度/K 完成度维度设计的镜像
- agentjournal.dev「judge call vs dimension scores」实测：单问 vs 12-14 维分解（0.9076 vs 0.8373）——多因素拆分加权范式的实证
- hegargarcia/jev-playground：序列决策质量与一致性评测——对照我们自一致率 ≥85%
- abhixhek/jevcal：每题拟合置信度阈值→目标准确率→留出集验证→CI 锁定——正是我们"阈值抄用不可靠"痛点的工具化
- Shogo-nfrealmusic/jev-eval：Jev vs GPT-4o-mini vs Sonnet 同条件对照——对照我们 DeepSeek adapter 跑法
- GoSailGlobal reranking 实测（X，33047 条目）：Jev rerank 未胜向量检索的负面结果——防止我们误用
- frostney/clean-code-review：31 个布尔检核 + 度量→写作模型出评语："判定与行文分离"，可用于章评
- MarissaFamularo/citation-verifier：Claude 定位 + Jev 评分 + 人终裁的三级流水线 = 我们金标/隔离流程模板
- komikat/jev-bfs、superagents-lab/jev-search：排序类提问的 state 压缩技巧

产出重点：本批直接生成对 `jev_eval.py` 的改造建议清单；**每条建议必须附后照验收步骤（见 DoD-2），不写无法验证的建议**。

## B4 — Agent 决策与浏览器（只扫读进矩阵）

agent-labs-dev/fastbrowse、jkudish/jev-browser、Silbercue/public-browser（token -30% / 成本 -25% 实测）、Stagehand + a11y-tree 范式（kylejeong）、kitze/unclutter、realZachi/typesafe-adblock（逐元素 Noul 流）、vercel-labs/json-render、joelhooks/pi-fast-jev-compaction + tamaratran/fast-jev-compaction + leonaaardob/fast-dev-compaction（compaction 三镜像，注意 theo 的公开反驳）、shitianfang/wakegate（低置信不唤醒的 gating ≈ 我们的 quarantine）、noplan-inc/limpet（Stop hook 完成判定）、compozy/yoshi、dzhng/duet-agent。

## B5 — 校验/护栏/文本质量（去 AI 味相关提级深读）

- DanWilloughby/snifftest：**深读首选**。散文 linter：每段 10 个 Boolean、0.7 阈值、182ms 中位、54 段clean 样本对照 Haiku（37:1 误报差）——与去 AI 味 ONNX 链路（Eslzzyl/aigc-detector-zh-onnx）互补
- Kelbie/hunch、doeixd/jev-pref（AGENTS.md 规则→diff 检核）、leepokai/jev-guard、shiftynick/jev-axi（44/44 标注自检集）
- luantak/is-malicious、owner-A/jev-git、coldteadotai/abide（39 改动中 10 处经独立确认的召回统计法）
- HyunjunJeon/jev-judgment、devagrawal09/jev-review + jev-code、raihankhan-rk/diffjury、bitnovus/jev-spam-eval（vs TF-IDF 基线）

## B6 — 分类路由 + 内容审核

Notra（生产级 300ms p50 指标）、gargpratyush/jev-router、prismhq/jev-router、adarshmishra07/jcm-router、mejiasd3v/pi-jev-router、GodsBoy/jev-agent-skill-router、gtaras7/typesafe-jev（政策改后重评零成本 = 我们"改档位不重测"的同款诉求）、GiesN/typesafe-jev-workflow（LangGraph 路由）、AboveColin/HA-Jev、brainstormity/Jev-Moderation-Bot（四级升级阶梯 + 赦免样本回注 context）、CodeAlive-AI/mastra-jev-moderation（9/9 拦截 0/49 误杀、fail-open + 熔断）、cephalization/jev-triage（每 issue 固定 5 问 + 人工纠正回显 = 金标修正闭环，对照我们 drift_within_round 追踪）。

## B7 — SDK/Infra/DB 集成（扫读为主）

typesafe-sdk（官方 Python）、jevclient (PyPI)、jev-go、alterhq/typesafe-sdk-swift、Butochnikov/laravel-typesafe-jev、dannote/jev (Elixir)、jamesward/zio-typesafe-ai、tumf/jev-cli、jkudish/jev-mcp + blakestone-x/jev-mcp + dakdevs/decide-mcp（对照我们自建 jev-mcp-server 的 4 工具设计）、gamesonrblx/Jevbridge、kylemclaren/jevql + mgaitan/sqlite-jev + DuckDB 扩展（SQL 行级 jev() 谓词——评测集筛选可能直接可用）、yusukebe/hono-jev-router、vercel/eve + vercel-labs/ai-cli + ai-python、WiktorB2004/llama-index-jev（nDCG@5 0.340→0.396 实测）、rajivkuriakose/typesafe-jev-examples（无 key 可跑的 OpenRouter 示例——新手 demo 候选）。

## B8 — 其余

sosopop/jev_stock、aowang-ai/jev-trade、unicodeveloper/jevocks（jev-trader.vercel.app 属此圈）、johnhughes3/LegalForecastBench（micro-Brier 校准度量参考）、achimala/jevinci（并行像素 = 极限并行调用示例）、owner-A/jev-curate（Noul 筛合成数据流——语料清洗可借）、silverstein/minutes、nekuda-ai/WindTunnel、kuhung/understanding-jev（中文深度解读）、backnotprop poker 实验、moritzkremb 教程线程（3 个 demo：语音浏览 / AI memory / YouTube 预处理）。

---

## 执行节奏（双档，v2）

**标准档（7 个全天，推荐）**：
1. D1：B0 全部 + 建 `analyses/` 骨架 + diff 四平行目录补全清单（产出去重清单 `eval/inventory.csv` 离线缓存）
2. D2~D3：B1（扫读 + 深读 3 库 + 本地复跑 1 个）
3. D4：B2（扫读 + 深读 2 + 复跑 1~2 含宣称指标复测表）
4. D5：B3（扫读 + 深读 2 + 改造建议清单，每条附后照验收步骤）
5. D6：B5（含 snifftest 深读）+ B4/B6 扫读晋级扫描
6. D7：B7/B8 扫读 + FINAL 矩阵与报告

**压缩档（4 个半天，仅当工期硬约束时启用，须知代价）**：只保留 B0+B1+B3+FINAL；B2/B5 降为扫读；demos/ 复跑与复测表推迟到下一轮。DoD-3（至少 1 个 demo 复测表）在压缩档内标记为**未完成项而非取消**，不允许静默降标。

## 完成定义 DoD（v2 新增，逐条打钩才算完工）

1. **覆盖**：去重后清单 100% 出现在 FINAL 矩阵行（含只扫读库）；深采库 ≥8 个（B1×3、B2×2、B3×2、B5×1）单库档齐全
2. **闭环回归**：改造建议每条附后照；采纳的改动合入后跑 `jev_eval.py --compare`（120 条金标）一致率**不下降**，结果写回 FINAL；未采纳的注明理由
3. **demo 实证**：`demos/` 至少 1 个复跑成功且带原始宣称指标复测表（偏差>30% 标红）
4. **三玩法反哺基线**：开工前先照一次基线（稿件体检 5 样本一致率 / 梗筛选抽样命中率），完工时两项**均不劣化**，且至少 1 条分析结论写进对应玩法的改造建议（可指向未采纳但需给理由）
5. **隔离清零**：体检报告 `reports/plan_review.md` 隔离项 priority_coherence 已由『优先级-排期换算规则』裁决消解；复核档三项（cost_budget/gap_ranking/what_missing_most）对应修订已落地

## 交付物

- `jev-analysis/analyses/*.md` — 逐库分析（模板填写）
- `jev-analysis/reports/batch01~07.md` — 批次小结（每批：深采/浅采/丢弃三清单）
- `jev-analysis/reports/FINAL.md` — 对比矩阵（原语用法 × 校准策略 × 可移植性）+ Top10 典型 demo 榜 + 本地链路落地建议（接入优先级排序）
- `jev-analysis/demos/` — 复跑成功的典型 demo（README + 锁定依赖 + 宣称指标复测表）
- `jev-analysis/eval/inventory.csv` — 去重后全量清单（B0 产出，离线缓存）

## 风险与约束

- **批量脚手架**：同作者同日多库、共享 AGENTS.md/STATE.md 脚手架的，先按"线索"对待，验证真实 API 调用后再深读
- **无 License 条目**：只记录模式，不复制代码
- **网络与获取**（v2 新增，已发生过的战况；B0 已实测校准）：github 直连 WebFetch 超时是实况。实测可用通道优先级：**① `gh-proxy.com/https://raw.githubusercontent.com/...`（主力，5/5 目录全通；失效时用备胎① `ghproxy.net` 同前缀格式，B0 复盘实测 200 可用；mirror.ghproxy.com/github.moeyy.xyz/fastgit 均死）→ ② 整库 `git clone https://gh-proxy.com/https://github.com/<owner>/<repo>.git`（已验）→ ③ fastly.jsdelivr.net（仅命中缓存的文件可用）→ ④ cdn.jsdelivr/直连 raw 均不可用**；HF 镜像不支持 Spaces，HF-only 资源（如 AlexWortega/openjev、权重下载）需单独评估；docs.typesafe.ai 加 `.md` 后缀可拿 Markdown 原生页。克隆一律 `--depth 1 --filter=blob:none`；B0 产出去重清单已落 `eval/inventory.csv` 离线缓存，断网可续扫
- **API 配额**：官方 jev 仍在排队放人；深读阶段优先走本地复刻（B1）与 OpenRouter 示例（rajivkuriakose），官方 key 只留给最终对照实验
- **成本预算上限**（v2 新增）：本地复跑权重磁盘上限 **30GB**（OpenJev 4B≈8GB、decider 2B≈4GB、NanoJev/kev 0.5~0.6B≈各 1.2GB，够装全部候选），跑不动的 4B 级模型记录后放弃不强跑；adapter 对照实验（如后续用 LLM-as-Jev 复测）预算 ≤20 万 token；官方 key 到手后对照实验预算 ≤$5，超出先停下来报批
- **时效**：目录生成于 2026-09-19，生态每天在涨；每轮分析前重跑一次 B0 的目录 diff
