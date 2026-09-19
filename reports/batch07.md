# batch07 — B7 SDK/Infra/DB 集成批（扫读为主·无深读名额）

日期：2026-09-19 ｜ 池：**61 库**（v7）｜ 状态：**完成**（遗留见 §五）
**浅采·要点 18 · 浅采 15 · 留矩阵 27 · 留矩阵·存疑 1 · 深采 0**（合计 61；统计由 `_rb7_precheck.py` 从 §二 处置列解析回填，header ok ✓。前置核账拦下矩阵**完整性缺陷**：初稿误含 2 条幻影 dup 占位行、漏 3 实库 blakestone-x/genierobot/tumf（元数据证 61 库无重复）→ 删幻影+补齐后方为 61；37 个数字 token→源文件反查 **0 MISS**；skillranker "113KB" 经 getsize 核实（113,274B，十进制 KB；脚本初版误用 ÷1024 已改为 ÷1000）

## 一、批次定性与零复跑说明

- PLAN B7 定位"SDK/Infra/DB 集成，**扫读为主**"，**不分配深读名额**；本战役 DoD-1"深采≥8"已由 11 篇单库档满足，B7/B8 均纯扫读进 FINAL 矩阵。
- **本批不跑零 key 复跑**（决策非遗漏）：PLAN 点名的 `rajivkuriakose/typesafe-jev-examples` 虽标"新手 demo 候选"，但其判定臂需 OpenRouter key（非真零 key），且 DoD-3"≥1 demo 复测表"已由前四批 4 次复跑超额满足；故 B7 复跑预算记 0，理由留此免得被当成漏项。
- 全批 = 各语言薄客户端（Swift/Ruby/PHP×3/Go×3/Rust×3/.NET×2/Elixir×2/Java/Net/Haskell/Zod）+ MCP server 群 + SQL/DB 扩展群 + Pi 扩展群 + 少数真评测设计库。**Jev 面集中在"confidence≠correctness""threshold 显式化""gate 动作分层"三主题**。

## 二、61 库 stay/go 矩阵

| 库（★/lic） | ①复跑②量化③调用 | 处置 | 一句话依据 |
|---|---|---|---|
| byk/jev-mcp (MIT) | ✗✓✓ | 浅采·要点 | `jev-eval-mcp`：**jev_eval 工具直接对标我们**——对标注样本量测问题变体的 accuracy/calibration/**threshold sweep**/worst misses，报 F1/AUC/**Brier/ECE** |
| eugeneboondock/jevsql (lic=None) | ✗✓✓ | 浅采·要点 | SQL 自然语言谓词 + "标注行跑一次跨 threshold 比 accuracy/coverage/**review workload**"；批处理 10 req→1 req 省钱；诚实"10 行只示 shape 非校准结果，见未确立清单" |
| wiktorb2004/llama-index-jev (MIT) | ✗✓✓ | 浅采·要点 | 真基准带 CI：nDCG@5 BM25 .298/MiniLM .340/**MiniLM+Jev .396**，Δ +0.056 **95%CI 0.042–0.072 排除 0**，≈$0.0003/query |
| nyarlathoteppppp/pi-heed (MIT) | ✗✓✓ | 浅采·要点 | **实测校准曲线**：p 0.9–1.0→98% 真 / 0.7–0.9→94% / 0–0.1→7%；版本演进 71.4%→97.6%，false block 16.3%→0%；139 测试 |
| nyarlathoteppppp/pi-jev-context (MIT) | ✗✓✓ | 浅采·要点 | "**Jev 从不选 UNCERTAIN（0/265 调用）**→改用 probabilities+confidence"；96% message token 是工具结果 |
| dakdevs/decide-mcp (MIT) | ✗✓✓ | 浅采·要点 | 严格区分：**"Jev 的 confidence 不是选中项概率、不得替代"**；native 分布四舍五入可能 sum≠1，须校验 range/sum |
| inanna-malick/jev-dsl (lic=None) | ✗✓✓ | 浅采·要点 | **"数字即产品"**：**margin（冠军−亚军）区别于 confidence**；0.78/亚军0.17 ≠ 0.78/亚军0.74，程序可据此区别行动 |
| jmanhype/jev-dspy-lab (lic=None) | ✗✓✓ | 浅采·要点 | 记录/回放 TypeSafe 调用；跨 gate 报 **coverage/accuracy/selective risk**；`benchmark.json` 机器可读门禁报告（自曝"不报数据集级校准"） |
| kylemclaren/jevql (lic=None) | ✗✓✓ | 浅采·要点 | psql 形 CLI + Go/TS/Py SDK：SQL 行级 `jev()`/`jev_confidence()`，**threshold 优先级**（显式>CLI>默认）+ cache（129 判 82 命中）——评测集筛选可直用 |
| mgaitan/sqlite-jev (lic=None) | ✗✓✓ | 浅采·要点 | "把 threshold 留在 SQL 里，让它随误判成本上升而抬高"；决策持久化 + **审计回执**表；只取判定所需列省 accuracy/cost |
| jkudish/jev-mcp (MIT) | ✗✓✓ | 浅采·要点 | 注入门检测 block_at 0.75/review_at 0.25；**`jev_gate` 一次调用既审补丁又核验完成度宣称**（done-check） |
| devmortimer/pi-typesafe (lic=None) | ✗✓✓ | 浅采·要点 | "**问 state 说的、不是你推断的**"：报告写"happens every time"却判 P(yes)=0.36；confidence=分布集中度非正确性 |
| rajivkuriakose/typesafe-jev-examples (lic=None) | ✗✓✗ | 浅采·要点 | 公开可跑 demo（OpenRouter 供 `typesafe/jev-1.13`，无需内测 key）；`ROUTABLE_CONFIDENCE=0.60` 之下不自动路由 |
| jomatsu/zod-jev (MIT) | ✗✓✓ | 浅采·要点 | **形状校验(Zod 本地)+语义校验(Jev)配对**；p=0.87→"不确定、问人"三态；"不需要会漂移的 JSON mode" |
| brainwires/jevwire (lic=None) | ✗✓✓ | 浅采·要点 | 可嵌决策库+6 MCP 工具；`thresholds {auto:0.85, review:0.6}`；scope/destructive 分维 p 值（0.88/0.93） |
| dicklesworthstone/skillranker (MIT+rider) | ✗✓✗ | 浅采·要点 | 相关性门 + **sentinel 弃权** + `--why-not` 追踪候选被排除处（含阈值与恢复提示）；失败钩子静默非阻塞兜底 ｜**⚠ README 113KB 疑似膨胀** |
| y0usaf/pi-jev (lic=None) | ✗✓✓ | 浅采·要点 | destructive/exfiltration/beyond_scope 4 noul 合 **1 请求 300ms**（省 4× 往返）；gate+输出判分双用 |
| blakestone-x/jev-mcp (MIT) | ✗✓✓ | 浅采·要点 | 7 工具 MCP（ask/classify/score/check/match/screen/health）+ **生产数据实测表**：0.8–1.0 段 95% 一致、**判据顺序反转致 32/200 翻转（翻转项均值 conf 0.42）**、token/请求成本、tokens/min 限流观察；"screening 非安全边界" |
| theooliveira/pi-jev (lic=None) | ✗✓✓ | 浅采 | `JEV_THRESHOLD`0.65 激活语义工具路由；`pi-jev-gate` 退出码按 ≥0.70 判；auto/compact 皆 opt-in 默认关 |
| gamesonrblx/jevbridge (MIT) | ✗✓✗ | 浅采 | 置信门 **execute/confirm/escalate/abort** 四态；computer-use 点击监督；ACP+MCP 双栈 |
| hyunjunjeon/pi-quiet-ask (lic=None) | ✗✓✓ | 浅采 | gate 默认 **shadow 模式（warn 不 block）**先观察；`cacheSeconds 120` 同 state 去重判；~250ms |
| ilkerulusoy/pi-jev-compact (lic=None) | ✗✓✓ | 浅采 | verbatim 上下文压缩：minReductionRatio 0.25/keepThreshold，散文阈值更严（丢工具结果代价高）；15.5%→33.5% |
| kevinpita/pi-jev-context (MIT) | ✗✓✓ | 浅采 | keep 概率 **严格大于**阈值 0.8（0.80 也被隐）；显著"启用后数据离开本机"隐私告警 |
| jomatsu/pi-jev-auto-mode (lic=None) | ✗✓✓ | 浅采 | per-rule threshold tuning + docs/calibration.md 实测；判一次 ~193ms；safeCommands 白名单 |
| nshkrdotcom/typesafe_sdk (46KB Elixir) | ✗✓✗ | 浅采 | "分类器不会因换标签集就变成校准的 37 向路由"；引 RLCD（校准决策强化学习）概念 |
| saibimajdi/typesafe-dotnet-sdk (MIT) | ✗✓✗ | 浅采 | "**Confidence 只上报、绝不臆造**"；Noul 无 confidence 显式说明 |
| colliber/duckdb-jev (MIT) | ✗✓✓ | 浅采 | DuckDB 扩展：choice/score 旁挂 `<name>_confidence` 列；断连退避重试 |
| mattn/sqlite3-jev (MIT) | ✗✓✗ | 浅采 | SQLite C 扩展 `jev_choice_json/…`，`->>'$.confidence'` SQL 内取置信 |
| giuliosmall/pg_typesafe (lic=None) | ✗✓✓ | 浅采 | Postgres C 扩展（pre-alpha）；`typesafe_detect_many 0.86s`；请求可 statement_timeout 取消 |
| nasrallah-al/jev-cli (MIT) | ✗✓✗ | 浅采 | `npx jevctl` 零装；**退出码 2 = `--fail-on` 命中 → CLI 即门**（把判定编码进 shell 退出码） |
| stumble/jev-go (MIT) | ✗✓✗ | 浅采 | 无运行时依赖 + **coverage≥85% 门徽章** + AGENTS.md；TypeSafe/Vercel 双 provider |
| genierobot/typesafe-ai-rails (MIT) | ✗✓✗ | 浅采 | Rails 集成：DB 持久化 confidence 策略（specific>wildcard `*`）、`act!` **fail-closed**（无策略即 raise）、未知模型族记 `cost_usd=NULL` **不臆造价**、遥测失败默认非致命 |
| tumf/jev-cli (MIT) | ✗✓✗ | 浅采 | PyPI CLI + stdio MCP：退出码 **0/1/2/3/4 编码错误类**（认证缺失=3、限流=4）、凭据文件原子写 `0600`、多 provider key 隔离、"不做算术/比日期，确定性活留代码" |
| owner-B/s1-rs (MIT OR Apache) | ✗✓✗ | 留矩阵 | Rust derive：枚举/结构体→Choice/Score/Noul；`gate(Policy::act(0.85).review(0.6))`——薄但门控 DSL 干净 |
| owner-B/typesafe-rs | ✗✓✗ | 留矩阵 | 延迟导向 Rust 传输 SDK；conformance/fixtures 驱动真客户端打真 mock（含 429/retry-after-ms） |
| joshmn/typesafe-sdk (Ruby) | ✗✓✗ | 留矩阵 | Score 概率加权可落两级间(1.6)；"gate 用 confidence 而非概率"表述 |
| hawxy/typesafeai.net (.NET) | ✗✓✗ | 留矩阵 | actionThreshold0.7/reviewThreshold0.35/severityBlock2.0；建议"校准过再 pin 版本" |
| gaurav-gosain/jev-go | ✗✓✗ | 留矩阵 | injection≥0.70||severity≥2.0 分诊示例；p95 统计 |
| premo-cloud/typesafe-sdk-java | ✗✓✗ | 留矩阵 | Java 17 客户端：指数退避 500ms–5s+25% jitter、honoring Retry-After、401/429 异常分层 |
| gilljon/typesafe-ai-rs | ✗✓✗ | 留矩阵 | 独立 async/blocking Rust 客户端；retry/log facade |
| zhirschtritt/typesafe-go | ✗✓✗ | 留矩阵 | 惯用 Go SDK；honors Retry-After、从不重试某类 |
| abovecolin/jevclient (Py) | ✗✓✗ | 留矩阵 | 异步 Python 客户端；批量延迟表(3/25/100→~700ms)；"Noul 无 confidence 因概率即全部答案" |
| alterhq/typesafe-sdk-swift | ✗✓✗ | 留矩阵 | 官方 Swift SDK；header 优先级大小写不敏感；生产架构走网关代理 |
| ainame/swift-typesafe | ✗✓✗ | 留矩阵 | 非官方 Swift 6.4，对齐 Python SDK 0.6.0 API |
| butochnikov/laravel-typesafe-jev | ✗✓✗ | 留矩阵 | Laravel 作用域绑定；`Jev::fake()` 离线不发网络（测试替身） |
| butochnikov/typesafe-sdk-php | ✗✓✗ | 留矩阵 | PHP 客户端 DTO/promises；PSR-3 logger 默认 NullLogger |
| fox-islam/typesafe-sdk-php | ✗✓✗ | 留矩阵 | PHP 8.3 社区客户端；直连或 OpenRouter 双通道 |
| jamesward/zio-typesafe-ai | ✗✓✗ | 留矩阵 | Scala ZIO 客户端；Probability 抽象类型 |
| dannote/jev (Elixir) | ✗✓✗ | 留矩阵 | GenServer；**"子句顺序即路由、阈值即守卫"**（when c>0.85→act / c>0.6→done 模式匹配） |
| itsmostafa/typesafe-mcp | ✗✓✗ | 留矩阵 | Go 单二进制 MCP；OpenRouter 路由 Decisions API |
| cline/plugins | ✗✓✗ | 留矩阵 | Cline 官方插件集合含 jev-browser（借 Vercel 网关跑浏览器目标执行） |
| ffattiger/new-api-plugin-typesafe | ✗✓✗ | 留矩阵 | 中文：给 new-api 网关加 `/v1/systemone` 端点 + usage 计费表达式 |
| yusukebe/hono-jev-router | ✗✓✗ | 留矩阵 | Hono 中间件按语义路由 HTTP；decision 可注入替换（测试/缓存） |
| kitze/skillbox | ✗✓✗ | 留矩阵 | 自托管版本化 skills 库(React/Bun/Hono/Postgres)；可选 Jev 推荐（基础设施非评测） |
| dbreunig/building-with-jev-skill | ✗✓✗ | 留矩阵 | 社区 agent skill 文档（问题设计/状态/阈值/诊断），1.2KB 薄 |
| shantanugoel/ask-jev-skill | ✗✓✗ | 留矩阵 | Hermes skill：820B，仅指针 SKILL.md |
| legacybridge-tech/pi-typesafe-jev | ✗✓✗ | 留矩阵 | 五 Pi 工具暴露 System One；"你的代码和用户保留 threshold/weight 控制权" |
| mizchi/jev-gomoku | ✗✗✓ | 留矩阵 | MoonBit 客户端 + Jev-vs-Jev 五子棋；成本彩蛋（1 局≈$0.0024） |
| romaluev/jev-ego | ✗✓✗ | 留矩阵 | ego lite 浏览器 agent：一次请求选操作+索引；CDP 调用数优化 |
| vercel/eve | ✗✗✗ | 留矩阵 | Vercel eve 引擎 beta，Jev 作默认评测；4.4KB beta 说明薄 |
| vercel-labs/ai-cli | ✗✗✗ | **留矩阵·存疑** | README 经双代理三 ref 全 **MISS**（疑改名/迁移，PLAN 称可跑 Jev 评测）→ 存在性待 FINAL 用正确通道复核 |

## 三、跨批主题收敛（B7 内证据）

四条我们在 jev_eval 里已隐约使用、B7 多库独立显式化的原则：
1. **confidence ≠ correctness ≠ 选中概率**：dakdevs（禁替代）、saibimajdi（只上报不臆造）、abovecolin/jevclient（Noul 无 conf）、blakestone（"confidence 是分布集中度非正确性"）、devmortimer/pi-typesafe —— B7 内 5 库 + 跨批 pi-warden(B4) 共 6 库同调 → 支撑 S-B6-1 主线（评分别拿分布集中度当真值率）。
2. **threshold 显式化 + 分层动作**：owner-B s1-r act0.85/review0.6、hawxy 三段门、jevwire auto/review、jevbridge execute/confirm/escalate/abort、gamesonrblx → "门限下不是二选一而是多态兜底"。
3. **margin（冠军−亚军）是被低估的第二信号**：inanna-malick/jev-dsl 明确提出，对照我们只记 confidence——**建议 jev_eval 增列 margin**（同批 pi-quiet-ask/pi-jev 的多 noul 合批也提示"一次请求多问"省往返）。
4. **判据顺序敏感性是被测出的误差源**（blakestone 生产实测）：仅反转 criteria 顺序即致 **32/200 选择翻转，且翻转项均值 conf 仅 0.42**（低置信区最易被顺序扰动）→ 直接支撑我们的**反向盲审 / 多排列一致性检验**：单排列结论不可信，金标集应测 order-sensitivity 并对高翻转低置信条目降权。

## 四、SQL 行级 jev() 谓词专列（PLAN"评测集筛选可能直接可用"）

jevql / jevsql / sqlite-jev / duckdb-jev / sqlite3-jev / pg_typesafe 六库都把 Jev 判定嵌进 SQL 谓词。可直用点：**在评测集表上用 `WHERE jev(alias,'是否含 AI 注味',0.7)` 做行级筛选/分档**，mgaitan 的"阈值随成本抬升 + 审计回执"与 jevql 的"cache 命中省重复判定"对我们金标集清洗有直接价值。零 key 均可跑 schema/typecheck（C/Go/Rust 扩展需编译，Py/TS 侧可跑），本批未逐个实跑（记 §一决策）。

## 五、核账 / 遗留

- 头部处置统计由 `_rb7_precheck.py` 解析回填；量化 token（0.396/0.056/71.4/97.6/265/0.36/0.78/129 等）经脚本 token→源文件反查核归因。
- [ ] `vercel-labs/ai-cli` README 三 ref 全 MISS → FINAL 用 jsDelivr + contents API 双通道复核存在性（与 vlad-terin/jev-browser 同批处理）。
- [ ] `eugeneboondock/jevsql`、`inanna-malick/jev-dsl`、`dicklesworthstone/skillranker` 等 lic=None 库 → FINAL 授权表统一裁定。
- [ ] `dicklesworthstone/skillranker` README 113KB（远超同类），FINAL 抽查是否 README 膨胀/生成物堆砌影响"深读性价比"。
- [ ] 多个非官方同名 SDK（jev-go×2、typesafe-sdk-php×3、sqlite-jev 系）→ FINAL 去重说明"语言生态冗余度"作热度证据非独立设计数。
- [x] **RB7 复审轮已闭环**：`eval/b7_review.jsonl`（2×5，`--check` ✓ exit0，盲审 10/10）+ `reports/b7_review.md`；前置核账于定稿前拦下 **1 完整性缺陷**（2 幻影 dup 行 + 漏 3 实库，靠 `header ok==POOL` 硬门逼出）+ **1 单位口径缺陷**（113KB 十进制 vs ÷1024）；两条教训（矩阵须与元数据池行级 diff / 量纲类宣称走 getsize）固化入 B8·FINAL 模板。
