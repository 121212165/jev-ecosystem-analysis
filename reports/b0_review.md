# b0_review — 用 Jev 对 B0 产物做多轮判定复盘

日期：2026-09-19 ｜ 方法：LLM-as-Jev（无 key），每题 5 次采样 + 逆序盲审一遍 ｜ 数据集：`eval/b0_review.jsonl`（2 条目 × 10 问，`--check` 通过）

## 一、协议执行

- 判定前先跑 `b0_stats.py` 拿**实据**（desc 覆盖、子串误伤例、单源占比、池/名额比、存在性验证数），state 字段即诊断快照——不凭印象打分
- 盲审逆序 RB-B→RB-A，**10/10 与首判一致（自一致率 100% ≥85%）**，无隔离题
- 边缘题（样本分裂 ≥2/5）：`single_source_risk`（3:2）、`biggest_risk`（4:1）、`iterate_next`（4:1）——已按多数判，置信度 0.72–0.75 如实压低

## 二、判定结果一览

| qid | 原语 | 判值 | conf | 结论 |
|---|---|---|---|---|
| kw_substring_ok | Noul | **0.15** | 0.90 | 关键词归位不可直接信任（实锤误伤 2+ 例） |
| existence_checked | Noul | **0.05** | 0.95 | 277/277 存在性未验证，开工前最大债 |
| single_source_risk | Score | **1** | 0.75 | 单源 63.5%>五成，但 n_lists 字段已备好，缺显式动作规则 |
| biggest_risk | Choice | 存在性未验证 | 0.72 | 误分类局部可肉眼纠，存在性是全局 277 库 |
| slot_pressure | Noul | **0.30** | 0.78 | 三条标准判不出 20 选 3 的相对次序，需预排序 |
| report_consistency | Score | **0** | 0.92 | batch00 数字与实态不符且未标注（59/67 时点漂移） |
| fallback_resilience | Noul | **0.20** | 0.85 | gh-proxy 单点故障无降级路径 |
| warn_rule_precision | Noul | 0.40 | 0.70 | owner≥3 不看时间分布，kitze 类误伤仍在 |
| iterate_next | Choice | 批量存在性验证 | 0.74 | 10 分钟脚本消最高威胁 |
| offline_reproducible | Noul | 0.88 | 0.88 | 快照+幂等脚本齐备；扣分：绝对路径写死 |

## 三、迭代点与闭环状态

| # | 迭代点 | 处置 | 状态 |
|---|---|---|---|
| I1 | **子串误伤实锤**：`latest` 触发 test→jev-latest 误入 B3；`snifftest` 被 B3 抢走破坏 B5 深读路径；大写 owner（`DanWilloughby/`）因 BARE 只配小写而漏归 plan | 分类器 v3：词边界锚定 + BARE 大小写不敏感 + 列表语境前瞻 + 停用词表 | ✅ 已修，重跑 **277→266**，snifftest→B5/plan ✓，零假阳性 |
| I2 | **存在性 0/277 验证**（21 个 PLAN 点名库来源是早前会话侦察，若含幻觉库 B1 直接撞墙） | 新增 `verify_existence.py`，gh-proxy HEAD ×266 | ⚠️ 曾判“266/266 全 200 零幻觉”，**B3 批被 I9 翻案作废**（通道无效），已用正确通道重验 |
| I3 | batch00 报告数字漂移（277/59/176 与实态不符未标注） | batch00.md 就地更新为 v3 值 + 加修订标注行 | ✅ |
| I4 | 单源 169 库缺显式处置规则 | 动作句已写入 batch00 §二（存在性已批量核过，扫读时只剩实际 API 调用核验一步）——I2 完成后此风险等级从 1 可降为 2 | ✅ |
| I5 | B1 深读名额 20 选 3 无预排序 | 待做：进 B1 前按 `n_lists≥2 + desc 含量化校准声明 + 支持本地/无 key 运行` 给 B1 池打预排序分 | ⏳ 归入 B1 开工第一步 |
| I6 | gh-proxy 单点故障无第二代理域 | 实测 5 候选：`ghproxy.net` ✅200（可用备胎）；mirror.ghproxy.com/×SSL、github.moeyy.xyz/×SSL、raw.fastgit.org/×超时 均死；gh-proxy 自身用假仓库探到 502→能区分通道死/仓库死 | ✅ 备胎已写入 PLAN 网络策略 |
| I7 | 预警名单只看 owner≥3，误伤多产正当开发者（kitze） | 待做：B1 扫读时对上述 6 个 owner 各抽查 1 库，补『同日提交/共享文件指纹』第二维证据后再定名单 | ⏳ 并入各批扫读 |
| I8 | 脚本绝对路径写死，换机不可携 | 低优先，D7 收尾时统一改 argv | ⏳ |
| I9 | **（B3 批新增）I2 存在性验证翻案**：gh-proxy 对任意 `github.com/<owner>/<repo>` 页面路径都返回自身主页 200——验的是代理存活度；用已删 `tests/*` 垃圾行实测坐实（200）。重验（`verify_existence_v3.py`，jsDelivr 主 + API 兜底，正负对照先过）：259 行中 **256 存在 / 2 真库仅 HF / 1 链接 404 / 5 分类器假阳性删除**（B8×4、B5×1）；分类器 v7：STOP_WORDS+source/port，DELETE 集+溯源注释 | 目测 266→259；批次数字 263→259 已同表刷新（batch00 §二/§七） | ✅ 已闭环于 B3 批 |

## 四、对评估协议本身的迭代收获

1. **判定必须配诊断脚本**：这次 4 个"Noul 低置信No"全部有 stats 实据支撑，比 plan_review 轮纯阅读判断更硬
2. **前瞻式 state 快照**：`n_lists`、`existence_verified_count` 这类字段先建后用，题目可复判——建议后续每批复盘都先跑 stats
3. **修 classifier 会连带翻案**：v3 重跑后 single_source_risk 从档 1 实际升到档 2（存在性已核）——复验表应随批次报告滚动更新
4. **GBK 环境**：jev_eval.py 输出 ✓ 会崩，固定用 `$env:PYTHONIOENCODING='utf-8'` 前缀（已验证）
5. **502 假阴性陷阱**：存在性/连通性探测要用真实存在的仓库做对照，否则『代理挂了』与『仓库不存在』混为一谈（本轮实测踩过一次）
6. **（B3 补）正对照也会不够**：I2 轮有假仓库探 502 的对照，但缺『**必死仓库必须真死**』的负对照——代理对页面路径一律 200 时，只有 `tests/*` 这种已知删除行才能揭穿。探活通道必须同时跑正（真库 200）负（假库 404）双对照，缺一即结论作废（v3 验证器已内置，不合格即 abort）

## 五、产物索引

- 评估数据集：`eval/b0_review.jsonl`（gold 内联，`--check` 通过）
- 诊断脚本：`b0_stats.py`；存在性验证：`verify_existence.py` → `eval/existence.csv`
- 被修对象：`build_inventory.py` v3、`eval/inventory.csv`（266 行）、`reports/batch00.md`（v3 修订）
