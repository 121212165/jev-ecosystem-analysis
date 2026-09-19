STATUS: 深采

# jaredpalmer/kev — 单库深度分析

> 结论先行：kev 是 B1 里**与我们评测链路最同构**的复刻——它把 TypeSafe 的 `/v1/systemone` 契约在本地 0.5B 上跑通，官方 `typesafe-sdk` 改个 `base_url` 就能直连，且附了**隔离性/排列敏感性/边界伪造**三组机理实验。这三组实验正是我们盲审协议要防的失效模式的量化版。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | github.com/jaredpalmer/kev |
| 类别 | B1 开源复刻（本地可跑） |
| License | Apache-2.0（基座 Qwen2.5-0.5B 各自许可） |
| 提交 | created 2026-09-17 / pushed 2026-09-19；last-100 分布 09-17×13、09-18×30（真实迭代，非单日脚手架） |
| Stars / Forks | 245 / 16 |
| 是否真实调用 Jev API | **是（对照）**：`kev.jev` 经 Vercel AI Gateway 打真 `typesafe-ai/jev`，结果落 `runs/kev-vs-jev-v1.json`；另用官方 SDK 跑本地 server（`tests/test_api.py`） |
| prompt 文档占比 | 低——是真正的训练/服务/评测代码，非散文拼凑 |

## 1. 接口形态
- 三原语齐：`noul`（yes/no）、`choice`（2–255 选项，带 description）、`score`（有序档位）。**一个共享 readout 头**同时出三类。
- state：string | object | array，结构化字段被 flatten 成带标签文本；questions 用 id 索引（模型看不到 id）。
- **并行提问是其核心卖点**：state 只编码一次，多 question 在 block-causal mask 下作为互不可见的分支并行解出（packed vs separate 概率差 4e-6）。这正是我们"13 问一次调用"的本地实现版。
- 元数据：choice 出 `probabilities`+`confidence`（公式 `(p_max−1/K)/(1−1/K)`）；score 出 `Σk·p[k]`+legend+分布；noul 只出 `p[yes]`（**印证官方口径：Noul 不带 confidence**）。

## 2. 校准与阈值策略（重点）
- **有量化校准且诚实**：held-out ECE 0.065，一步 temperature scaling 后 0.031。明确写"校准是在训练分布内的，换工作流必须重新用带标签数据标定"——与我们"金标必须来自本任务实测"的教训一致。
- 采样：单前向出完整分布（非多采样），因为概率是 readout 头直接算的，不是让模型写数字。这比我们 `JEV_SAMPLES=5` 取均值的路子更干净——**可移植点：能拿到 logits 分布时，用单次全分布代替多次采样求稳**。
- fallback：无显式低置信转人工逻辑（它是模型层，不是编排层）。

## 3. 工程质量
- `/v1/systemone` + `/permute` + `/separate` 三端点；422 校验错误；无鉴权（本地用）。
- provider 抽象：`base_url` 一换即可用官方 SDK——**与我们 `JEV_PROVIDER=adapter` 走 base_url 的设计完全对齐**。
- 机理实验（对我们最有价值）：
  - **Isolation probe**：把秘密放在兄弟 question 里，p=0.03；放 state 里 p=0.99 → 证明分支真隔离。对应我们"题目串扰"担忧。
  - **Permutation**：4 种选项序下 argmax 翻转率 7.4% → **选项顺序敏感性**的量化基线。对应我们盲审里"倒序盲判"的合理性：应显式测翻转率。
  - **Boundary forgery**：选项文本伪造分隔符，伪造项 p≤0.09 → 抗注入。
- 复跑：`uv sync --extra serve` + `python -m kev.serve --run jaredpalmer/kev-0.5b`（HF 权重 ~1GB）。**本机 CPU-only 无法验**（见 batch01 复跑记录）。

## 4. 可移植模式清单
1. **单次全分布 > 多次采样**：能直接读 readout 概率时，弃用 `JEV_SAMPLES` 均值，改一遍出全分布并存 `probabilities`——省 token 且方差可控。
2. **翻转率作为独立指标**：把"倒序/换序后 argmax 是否翻"做成 `run_plan_eval.py` 的一个显式列（kev 给了 7.4% 的量级参照），而非仅靠盲审一致率。
3. **`confidence` 派生公式**：`(p_max−1/K)/(1−1/K)` 直接搬进我们 Score/Choice 的 confidence 自报口径（对齐官方"由概率派生"）。
4. **transfer 诚实测**：kev 自曝训练内 81%、域外 transfer −19.1pp（63.3% vs Jev 82.3%）——提醒我们：**本地复刻的域内一致率不能外推到网文新领域**，DoD 回归要在自有数据上量。
- 反模式（不搬）：它自带 LoRA 训练管线（6 数据集转换），我们无 GPU 也不重训，别被"可训练复刻"诱导扩大范围。

## 5. 与本地链路映射
- `jev_eval.py`：kev 的 `/v1/systemone` 响应结构 = 我们 `--provider adapter` 期望的解析目标；其 probabilities/confidence 字段命名与我们 gold schema 一致，可作 **adapter provider 的本地 mock server 参照实现**。
- 盲审协议：Permutation 翻转率 7.4% 为"倒序盲判"提供量化阈值参考（一致率 ≥85% ↔ 翻转率 ≤15% 同构）。
- `hot_block_overlap_with_mid`：kev 的 transfer 落差法（同模型域内 vs 域外）可移植为"模型分与金标对齐"按领域分桶报告。

## 6. 复测表（宣称 vs 实测）
| 指标 | 宣称 | 实测 | 环境 | 偏差 |
|---|---|---|---|---|
| 服务延迟(6 问) | ~160ms | **未跑通** | 本机 CPU-only，无 CUDA/MPS，proxy 拉代码/权重多次超时 | n/a（记 DoD 未完成项） |
| ECE | 0.065→0.031 | 未独立复现 | 同上 | 采信其 README（有 raw json 佐证） |

## 7. 结论
- [x] **深采**：`/v1/systemone` 本地 mock + 单次全分布 + 翻转率指标 + confidence 派生公式，四点直接可用。
- 遗留：待有 CUDA 或稳定网络时，跑通 kev server 作为我们 `--provider adapter` 的活体本地端点，做一次端到端对照。
