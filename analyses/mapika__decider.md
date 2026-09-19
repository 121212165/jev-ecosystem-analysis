STATUS: 深采

# mapika/decider — 单库深度分析

> 结论先行：decider 是本次见到的**工程完成度最高的开源 System One 复刻**——94 个公开任务上量了 acc/NLL/Brier/ECE/AURC，v1→v9 迭代全记录在 `docs/HISTORY.md`，还实现了 schema 缓存 + CUDA graph 的生产级服务栈。它把"校准"从口号做成了可复现的实验矩阵，是我们评测口径最好的老师。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | github.com/Mapika/decider |
| 类别 | B1 开源复刻 |
| License | Apache-2.0 |
| 提交 | created 2026-09-16 / pushed 2026-09-18；last-100 分布 09-16×21、09-17×10、09-18×7（真迭代） |
| Stars / Forks | 27 / 2 |
| 是否真实调用 Jev API | 否——它是独立复刻，不连 Jev；但 wire format 是 TypeSafe `/v1/systemone`，SDK 可直连 |
| prompt 文档占比 | 低，纯代码 + 结果表 |

## 1. 接口形态
- Choice（2–255，选项可带 description 或 **JSON rubric**）、Score（2–10 描述档，返回期望档）、Noul。
- state 可为 string 或**任意 JSON**，question 用**点号路径**指名字段（`` `tickets[3].text` ``），≤32k token——**这正是我们"structured state + instructions 里点号路径"的做法**，decider 把它做成了可评测的一等公民，并量了弱点：从 64 条 JSON 数组里按位置挑记录仅 0.51（按 key 0.70）。
- **独立性是设计不变量**：增删/重排 question 不改其他答案（一行一 question）。packed 版重排会改最多 12% 答案，独立版 0%。
- Score **隔离档位**：每个档位单独判（看不到自己序号与邻居），再归一化 per-level fit——防"相邻档位互相污染"。

## 2. 校准与阈值策略（重点，全 B1 最强）
- **proper scoring rule 训练 + 单参数 temperature**：在一个 in-task 数据上拟合 T，在 held-out 任务上验（v8 T=1.30：in-task 0.811/ECE 0.037，held-out 0.741/NLL 0.655/ECE 0.088）。
- 完整指标族：acc / NLL / **Brier** / **ECE** / **AURC** / selective accuracy——AURC 与 selective accuracy 直接对应我们"低置信转人工"的阈值曲线。
- 弃权（abstention）：catch-all 选项（other/none）在不匹配时被选，且专门量了 abstention battery 8/8。对应我们"无合适档就隔离"。
- **诚实标注校准边界**："calibration 是在公开数据集与 teacher 探针上量的，不是你的流量——在你自己的标签上再验一遍。"

## 3. 工程质量
- 极完整：train/evaluate/serve/probes/bench/games/vision 全模块；`tests/` 无需 GPU（`python -m pytest tests`）。
- `TYPESAFE_BASE_URL=http://localhost:8000 TYPESAFE_API_KEY=local` 直接喂官方 SDK——与我们 adapter 设计对齐。
- schema 缓存：固定问题集预算一次前缀，请求只跑 state（151 选项单问 217→11.5ms，19x）。**代价**：schema-first 掉精度（选项每题变的任务掉 5 点）——它把 trade-off 量化给你看，而不是默认开启。
- 复跑：需 CUDA（bf16 ~4GB）。本机 CPU-only 跑不动（记 batch01）。

## 4. 可移植模式清单
1. **指标族补齐**：我们 gold/预测对比目前看一致率，应加 **Brier + ECE + AURC**——AURC 给出"置信度阈值 vs 覆盖率"曲线，直接指导我们自动执行/复核/隔离三档线与官方 risk-scaled 阈值对齐。
2. **独立评分 vs 打包评分**双跑对照（decider 用 12% vs 0% 说明打包会引入题间耦合）——我们盲审协议里"倒序盲判"应同时在 packed 与 per-question 两种下发方式下测，量化串扰。
3. **Score 隔离档位归一化**：每档独立判 + 归一化 fit，作为我们 Ending 二级树/情绪密度分档打分的实现范式（避免档位互相拉扯）。
4. **结构化 state 点名弱点测试**：仿它做"从 N 条 JSON 记录按位置/按 key 点名"的探针——我们的 `<未发布长篇>/jev_gate.py` 处理多场稿时正是这个形态。
- 反模式（不搬）：95 数据集 + 27B teacher 标数据的混合配方——我们无算力重训，只借其**评测口径**，不借其训练管线。

## 5. 与本地链路映射
- `jev_eval.py`：Brier/ECE/AURC 计算可直接参考 `decider/report.py`（temperature fit + 对比表）实现，补进我们的评分侧。
- Score 维度锚定规范（"档位写情形不写程度"）：decider 的 isolated-levels + 期望档输出是该规范的**已验证实现**，legend→level index 映射可照搬。
- 官方 confidence 口径：decider choice 出 `confidence`+`certainty`+`probabilities`，noul 仅概率——再次印证 Noul 无 confidence。

## 6. 复测表
| 指标 | 宣称 | 实测 | 环境 | 偏差 |
|---|---|---|---|---|
| 94 任务 held-out acc | 0.741 | 未跑通 | 需 CUDA，本机 CPU-only + 网络拉码失败 | 采信（有 HISTORY 分阶段数据佐证） |
| 151 选项缓存加速 | 19x | 未跑通 | 同上 | 采信 |

## 7. 结论
- [x] **深采**：Brier/ECE/AURC 指标族 + 独立 vs 打包双跑 + Score 隔离档位，三点强化我们评测口径；wire format 参照。
- 遗留：`decider/report.py` 的 AURC/temperature-fit 实现值得单独细读并移植进 `jev_eval.py` 的评分侧（待有代码读取通道）。
