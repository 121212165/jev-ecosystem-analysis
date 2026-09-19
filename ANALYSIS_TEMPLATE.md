# JEV 生态库分批分析 — 单库分析模板

> 每分析一个仓库，复制本模板到 `analyses/<owner>__<repo>.md` 填写。
> 目标不是"读懂代码"，而是回答：**这个库的模式能否搬进 本地网文创作系统（独立私有仓，未随本仓发布） 的 Jev 评测链路**。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 / 链接 | |
| 类别（所属批次） | |
| License | （无 License = 只能读不能抄，标注） |
| 首次提交 / 最近提交 / 提交数 | （识别"当日批量脚手架"账号，volume ≠ quality） |
| Stars / Forks | |
| 是否真实调用 Jev API | 搜 `api.typesafe.ai` / `systemone` / `system_one` / `jev-latest`，必须看到请求体和解析后的响应 |
| prompt 文档占比 | 代码行数 vs Markdown 行数（很多库 90% 是散文） |

## 1. 接口形态
- 用的是哪种原语：Noul / Choice / Score / 混合？一次请求几个问题？
- state 是什么结构？纯文本 / JSON？JSON 时是否在 instructions 里用点号路径指名字段？
- 是否利用并行提问（13 问一次调用 ≈ 11.5x 便宜、9.6x 快）？
- 元数据字段：probabilities、confidence 怎么用？还是只取了 argmax？

## 2. 校准与阈值策略（重点）
- confidence 阈值定在哪？是否分层（自动执行 / 复核 / 转人工）？
- 有没有在自己的数据上量过校准（对照 yibie 实测：平均置信度 0.82、实际准确率 0.70 的教训）？
- 采样策略：单采样还是多采样（本地链路已定 JEV_SAMPLES=5，输出均值/中位数/标准差）？
- 低置信度时的 fallback 路径是什么（升级 LLM？重问？隔离 quarantine？）。

## 3. 工程质量
- 可运行性：有没有测试 / 预期输出示例 / demo 脚本？
- provider 抽象：能不能无缝换到 DeepSeek/OpenAI 兼容端点（对照本地 `JEV_PROVIDER=local|adapter|jev` 三模式设计）？
- 错误处理：概率分布非法时是否归一（normalize_probabilities）？
- 成本/延迟：有无实测数字，且数字可溯源？

## 4. 可移植模式清单
- 列出 2~5 个"可直接搬进我们评测链路"的具体做法（精确到函数/配置级别）。
- 列出 1~2 个"不要搬"的反模式及原因。

## 5. 与本地 Jev 评测链路的映射
本地链路锚点（`<local-novel-eval>`）：
- `src/eval/jev_eval.py` — 评测入口，local|adapter|jev 三 provider
- `<未发布长篇>/jev_gate.py`、`<未发布长篇>/04-Jev决策层.md` — 决策层实践
- `docs/guides/Jev接入评测集指南.md`
既有规范约束（记忆）：
- 盲审协议：正常判 → 隐藏答案倒序盲判 → 不一致或 confidence<0.6 进 quarantine，自一致率目标 ≥85%
- Score 维度锚定：档位必须写"情形"而非"程度"；情绪密度=每千字转折数；K 完成度拆 K50/K100
- Ending 二级树：主档（反转/关系/认知/无）+ 子档（身份/规则/动机）
- `hot_block_overlap_with_mid`：模型分与 LLM 金标对齐字段
问题：该库的哪些设计能强化上述某一条？写入对应条目。

## 6. 结论（三选一）
- [ ] **深采**：模式直接可用，写复现 demo（记入 demos/ 清单）
- [ ] **浅采**：只吸收 1~2 个点，批次报告里一段带过
- [ ] **丢弃**：脚手架/无真实调用/无 License，记录原因即可
