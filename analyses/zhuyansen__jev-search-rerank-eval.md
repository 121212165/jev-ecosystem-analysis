# zhuyansen/jev-search-rerank-eval — 裁判循环偏置的可测量化处理（本批头号情报）

> STATUS: 深采 · 类别：B3 · 选取理由：9,831 标注对 + 配对 bootstrap CI + **同一结论在三套标签下重打分**，把"Jev 既当裁判又当选手"的循环偏置从口号变成 −0.028/+0.012/+0.053 三个可对照的数——直击我们 LLM-as-Jev"自答自评"的结构性软肋。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/zhuyansen/jev-search-rerank-eval |
| License | MIT ✅（ash_ranker 逐字复制自 MIT CLI） |
| 真实调用 Jev API | ✅ `typesafe/jev-1.13-20260917` 经 OpenRouter `/alpha/decisions`；"Every response's `model` field is recorded"；总账单 $2.6 全公开 |
| prompt 文档占比 | README 12KB 全是方法+表格；标签协议 8 步逐条可审 |

## 1. 接口形态
- Jev 用法：每候选一个 `score` 问题（0–3 四档 legend），25 候选/调用——**排序问题拆成逐点打分**，非整表 Choice。
- 双裁判：Jev（便宜，$0.069）+ Haiku temp0 独立家庭（$2.37）；二次加权 κ=0.71、±1 档内一致 98%；系统性分歧定位到 **1↔2 边界 1,768 对**。
- 终标 = 手裁(30 题核子集) > 双裁一致(5,224) > **不取整的均值**（"rounding half up would adopt the more generous judge"——四舍五入方向性偏差都防了）。

## 2. 校准与阈值策略
- 三标签集设计：final / **llm_only**（Jev 无权置喙，保守估计）/ jev_only。凡涉 Jev 的宣称必须活过 llm_only 才算数。
- 结果范式："Jev 独立重排不赢（llm_only −0.028 显著为负）；**融合赢**（rrf +0.064 显著）；弱候选集上 Jev 重排赢（+0.037）"——同一模型三种用法三种结论，拒绝一句话吹捧。
- 手核还反转了一次直觉：分歧手裁 30 对里 Jev 18:2 占优（Haiku 的过度给分是标签词重合无意图匹配）。

## 3. 工程质量
- `jse robustness` 零 API 重打分（缓存的 runs  committed）；标签 `labels_final.jsonl` **先冻结后评分、永不编辑**；池化无偏声明+局限都写。
- 30 题手核子集与全集逐系统 ±0.02 内一致——核子集本身就是个校验实验。
- 中文场景专项：交付的关键词排序器缺陷集中在中国近义查询（0.539 vs 0.756）；混语 bge-m3 > text-embedding-3-small。

## 4. 可移植模式清单
1. **★ 双裁判 + 保守列**：我们盲审 gold 全由同一 LLM-as-Jev 链路产出=单裁判。照此加独立第二信号（不同模型/不同协议，例如倒序盲判已经算半个），**评测报告涉自身的数字必须给"自己无权置喙"的保守列**。
2. **★ 分歧边界分析**：不满足于"κ=0.71"，定位到具体 1↔2 档边界+例子类别（tag 重合无意图匹配）→ 我们两轮盲审不一致样本应聚档出"边界在哪"而不是逐条进 quarantine。
3. **★ 分数不取整**：我们概率均值/中位数聚合时，半值向上取整=偏向更宽松的采样——聚合规则里显式禁 round-half-up。
4. **标签冻结先于打分 + 永不编辑**：对应我们 gold 集加 git-hash 冻结点，评测报告记 hash。
5. **配对 bootstrap CI 报差值**（Δ+CI 而非两点各自 CI）：jev_eval 输出对比表升级项；样本单位=题目，重采样 1000 次即得。
6. 拆点打分做排序（25 项/调用 score）：我们"排序类提问"（候选章节排序/结尾档排序）可借——比 Choice-K 大 K 时便宜。
7. 反模式（对我）：手核由"Claude, in one sitting"完成——单会话人裁无盲审，其自报局限也承认无人类子集；我们不学。

## 5. 与本地 Jev 评测链路的映射
- `jev_eval.py`：模式 1 直接改报告（加 llm-blind 列）；模式 5 改对比输出；模式 3 改聚合函数。
- 盲审协议：模式 2 把 quarantine 从"逐条孤岛"升级为"边界地图"。
- DoD-2 验收：任一改造后，用 b0/b2_review 既有 20 问重跑，报告 ΔCI 宽度变化即验收数据。

## 6. 结论
- [x] **深采**：方法论密度全批最高；"judge circularity is measurable, not assumed away"一句应进 FINAL 总报告扉页。

## 7. 复跑状态
- 环境阻断：需 OpenRouter key + bge-m3 本地推理（CPU 可跑但慢）；但 `jse robustness` 号称零 API 重打分（数据全 committed）→ 与 jevcal 同批挂整仓传输（估 10–50MB，含 search-index.gz），列 DoD#1 之后顺位。
