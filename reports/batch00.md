# batch00 — B0 官方基座与镜像目录（先决批）小结

日期：2026-09-19 ｜ 状态：**完成**（遗留 2 项见 §六）｜ 产出：`eval/inventory.csv`（**259 库**，v7 修订定稿；历史：v3 266 → v6 263 → v7 259，见 `reports/b0_review.md` §三与 `reports/batch03.md` §五）+ `eval/existence_v3.csv`

## 一、信息源拉取实录（网络策略首次实测）

| 通道 | 结果 | 用途 |
|---|---|---|
| `gh-proxy.com/https://raw.githubusercontent.com/...` | ✅ **主力通道**，5/5 目录全通 | raw 文件、仓库内容 |
| `fastly.jsdelivr.net/gh/...` | ⚠️ 仅当文件已被缓存（yibie README 通，其余 301→raw 被墙） | 兜底 |
| `cdn.jsdelivr.net` / `raw.githubusercontent.com` 直连 | ❌ 超时 | — |
| `docs.typesafe.ai/<path>.md` | ✅ **Markdown 原生**（Accept: text/markdown），9 页全通 | 官方口径 |
| `evals.typesafe.ai` | ✅ 200（HTML 65KB） | Workflow Evals |
| `hf-mirror.com` | ❌ 不支持 Spaces（tracker 拿不到） | — |
| `madewithjev.com` | ⚠️ 客户端渲染，curl 只提出 2 个 gh 链接（已在清单内），**需 browser 工具** | 社区展示 |

git 通道实测：`git clone https://gh-proxy.com/https://github.com/<owner>/<repo>.git` ✅（adapter 上游已浅克隆到 `_upstream_adapter/`）。
→ **回写 PLAN 风险条款**：兜底顺序修正为 gh-proxy(raw) → fastly jsdelivr → git clone via gh-proxy；HF 资源本网络基本不可用，B1 复跑涉及 HF 权重的库要提前评估。

## 二、五目录 diff 结果

| 目录 | 收录库数 | 说明 |
|---|---|---|
| yibie/awesome-jev | **122**（README 只有 80 条且截断，**必须拉 categories/*.md 14 个分类文件**） | 13 应用类 + Related Practices(45) |
| cobanov/awesome-jev | 114 | source-backed，带 research/2026-09-19.md 证据笔记 |
| AnotiaWang/awesome-jev | 107 | 中英双语 |
| owner-B/awesome-typesafe | 53 | 有 CI 检查 + GitHub Pages |
| Anil-matcha/awesome-jev-by-typesafe | 40 | 含 8 个视频 walkthrough |

> 上表与下列统计为 **v3 修订值**（初稿 277 库含子串误伤与散文假阳性，经 `b0_review` 评估后修复分类器重跑，详见 `reports/b0_review.md` §三）。

- **合并去重：259 库**（v7 定稿）。存在性翻案：下方“266/266 全 200”的 gh-proxy HEAD 验证已作废——代理对任意 github.com 页面路径都返回自身主页 200，实测连已删的 `tests/*` 行也是 200，即当时验的是**代理存活度不是仓库存在性**。正确通道重验（B3 批完成：jsDelivr 主 + gh-proxy API 兜底，正负对照通过）：**256 存在（255 README + 1 API）· 2 真库无 GH README（存 HF：alexwortega/openjev、drinkmoonshine/parallel-constrained-decoding）· 1 链接 404（vlad-terin/jev-browser，源清单原文如此，存疑保留）· 5 分类器假阳性已删**（详见 batch03.md §五）
- yibie 独占 66 库；**非 yibie 收录 140 库**（=平行目录净增量——当初只做 yibie 会漏掉超一半生态）
- 多源互证（≥3 目录同时收录）45 库——**这批优先信任**；单源扫读时多一步核验（存在性已按正确通道批量核过，剩实际 API 调用核验）
- 批次归位（v7）：B0×7、B1×20、B2×20、B3×21、B4×30、B5×18、B6×14、B7×61、B8×68（其中 58 库为 `unclassified→B8`，标记人工复分类；历史值 B1×21/B2×21/B3×23/B8×72 系 v3 含垃圾行所致，另 v4→v5 有 foreman→B4 实证改判）

## 三、批量脚手架预警名单（owner ≥3 库）

| owner | 库数 | 处置 |
|---|---|---|
| typesafe-ai | 6 | 官方，正常 |
| owner-A | 5 | ⚠️ B5/B8 扫读时核同日提交+共享脚手架，先按线索对待 |
| owner-B | 5 | ⚠️ 同人既是目录维护者又 5 库入库（含 s1-rs/typesafe-rs/bicameral），利益相关标注 |
| vercel-labs | 4 | 官方生态，正常 |
| kitze | 3 | ⚠️ 同扫读核查 |
| typesafe(org) | 3 | 待查与 typesafe-ai 关系 |

## 四、官方口径速查卡（docs.typesafe.ai 9 页 + skills + adapter 上游）

**置信度口径（/confidence）——两处与我们协议直接相关：**
1. `confidence` 是**从 probabilities 分布推导的统计量**，官方称是"适合多数用例的便利定义"，可用完整分布自行替换度量（我们 jev_eval 的三档 0.85/0.60 即其"三带路由"的具体化，口径一致）；
2. ⚠️ **官方 Noul 不携带 confidence**（"Noul answers don't carry one"），只有 Choice/Score 有。我们数据集给 Noul 题记 agent 自报 conf——将来 `--provider jev` 真比对时要注意：**Noul 题真 Jev 无 conf 字段**，分层对 Noul 只能靠 0/1 阈值或多样本方差。
3. 官方示例地板线 0.5（低于转人工），破坏性操作要求 >0.9——我们"改稿动作"映射到高风险档。

**四大官方模式（/patterns）：** Speculative Fan-Out（一次多问含投机题，省成本）｜ Confidence-Gated Routing（置信度作第二决策轴）｜ Composite Scoring（多维度合成总分——对应 JevSlop 八维镜像）｜ Intent Routing。
文档全站索引在 `_doc_llms.txt`（16KB），逐库分析引用官方口径时以此为导航。

**Cookbooks 高相关清单**（llms.txt 发现，B3/B5 直接对照）：`classification_using_confidence`、`consistency_choice_cookbook`、`consistency_noul_cookbook`（自一致率官方做法）、`llm_guardrails`、`rerank_typesafe`（官方 rerank 口径 vs GoSailGlobal 负面结果）、`hierarchical_classification`（Ending 二级树同款）。

**官方 skills 仓库**：`typesafe-ai/skills` → `skills/typesafe-ai/SKILL.md`（raw 可拉），Claude Code plugin + skills.sh 两种安装。B0 待办里的"对照官方提问范式"下一步做。

## 五、adapter 上游 vs 本地 patch（B0 核心问题：值不值得提 PR）

- 上游 HEAD = **v0.2.0 = 我们 fork 的基点**（零落后）；上游**没有**多厂商 registry（grep deepseek/zhipu 无）
- 本地 patch 干净：单提交 `cc437ec feat(providers): add OpenAI-compatible vendor registry`，仅 `src/system_one_adapter/providers/__init__.py` +66 行，不改既有行为
- 但已知缺陷：**JEV_PROVIDER=<vendor> 走 registry 路径对自定义 base_url 抛 Connection error**（本会话实测），目前靠显式 `OpenAIProvider(...)` 注入绕开；上游 providers 目录结构（`src/` 布局）与我们 site-packages 旧装法路径不同（`system_one_adapter/` 无 src 前缀），迁移时注意
- **结论**：值得提 PR，但先决条件是修好 registry 自定义端点 bug + 补一个回归测试（上游有完整 tests/ 目录和 CI，裸 patch 过不了 checks）。列入 B1 后时段任务，不阻塞后续批次。

## 六、遗留待办（带入 D2）

1. `madewithjev.com` 全量展示条目 → 需 browser-use 工具重跑（当前仅首页 2 链接，已被目录覆盖，损失面小）
2. HF Space `multimodalart/jev-reproductions-tracker` → hf-mirror 不支持 Spaces；候选方案：直接逐库验证 B1 复刻清单时代替 tracker 功能（jevmlx/simple-jev/verdict-open-jev 等描述里已带复现线索）
3. `unclassified→B8` 59 库在 D7 扫读时人工归位（inventory.csv `assign` 列可筛）
4. AlexWortega/openjev 是 HF-only（无 GitHub 库），不在 GitHub 清单内属预期；B1 复跑时按 HF 通道单独处理

## 七、产物索引

- 去重清单：`eval/inventory.csv`（259 行 × 7 列：repo/batch/assign/in_lists/n_lists/owner_repos/desc，v7）
- 存在性验证：`eval/existence_v3.csv`（259 行：256 存在/2 HF-only/1 404，脚本 `verify_existence_v3.py` 可重跑，正负对照内置）；旧 `eval/existence.csv`（266/266=200）已作废仅作历史保留
- 原始快照（离线缓存，断网续作）：`_raw_*.md`（5 目录 + 14 分类文件 + adapter/skills README）、`_doc_*.md`（9 官方文档页）、`_doc_llms.txt`
- 上游 adapter 克隆：`_upstream_adapter/`（depth 1）
- 构建脚本：`build_inventory.py`（幂等，改目录重跑）、`parse_madewithjev.py`
