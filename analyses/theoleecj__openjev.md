STATUS: 深采

# theoleecj/openjev (SemIf) — 单库深度分析

> 结论先行：SemIf 是社区声量最大的复刻（1671★），但它的真正价值不是模型——是**宣称纪律**。全库没有一句没有出处的数字：每条结果链到 committed 的 fixture/runner/raw json/prompt hash，跑不了 live Jev 就明说"这是系统对比，不是语义等价宣称"。这是给我们 DoD"复测表 + >30% 标红"制度找的最好的现成范本。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | github.com/TheoLeeCJ/SemIf（原 OpenJev，repo 名 theoleecj/openjev） |
| 类别 | B1 开源复刻 |
| License | MIT（代码）；模型各自许可 |
| 提交 | created 2026-09-16 / pushed 2026-09-19；活跃 4 天，5 issues |
| Stars / Forks | **1671 / 110**（B1 池最高） |
| 是否真实调用 Jev API | **否，且明说**："The Jev number is read from TypeSafe's published records; we did not run a live Jev endpoint."——对比对象是 evals.typesafe.ai 公开数据 |
| prompt 文档占比 | 低 |

## 1. 接口形态
- 输入是**自研简化格式**（id/state/question/options[{id,description}]），非 TypeSafe 原 wire format——读 typed option logits，无 answer sentence/JSON repair/decode 循环。
- state 可为非空 JSON object/array；direct 模式保留结构，reranker 模式渲染成文本。
- 模式分层：`--mode direct`（逐问）/ `--mode shared`（同 state 一次 prefill 并行多准则）——后者对应我们并行提问需求。
- 每行结果带 **timing + 精确 model revision + prompt hash**——可审计性是接口设计的一部分，不是事后补丁。

## 2. 校准与阈值策略
- 不训校准器（冻结 4B 读 logits），但给出**分层模型梯子**的实测：Qwen3-0.6B 0.440 → MiniCPM5-2B 0.686 → Qwen3.5-4B 0.813（authored balanced acc），TypeSafe 子集一致率 0.407→0.845，对照 published Jev 0.883。**"要多大的模型才够到可用线"**这个问题，它给了量化的答案。
- 诚实标注：概率是"条件于所给选项"的，"要上的工作流上自己标定"。
- BF16 复用路径改变了 777 决策中 5–6 个 argmax——**连自家加速路径的语义代价都量了**（我们 ONNX/量化路径就该照这个标准交代的数字）。

## 3. 工程质量
- 可运行性：pip install -e '.[test]'；MLX 后端（Apple）；CUDA + 4B BF16 GPU。浏览器 WebGPU demo（0.6B Q8 639MB 起）完全免装。
- `docs/REPRODUCE.md`：精确环境 + pinned 命令 + 扰动 + 验证步骤——"Reproduce" 是独立文档，不是 README 一句话。
- 时间学：direct 1.023s vs JSON 自回归 5.332s（21 准则）；共享 state 串行 10.75/s vs 并行 20.03/s——并行的收益有 owner fixture 背书。
- 本机：4B 太重跑不了推理；**WebGPU 浏览器 demo 是唯一可无 key 无装跑的活体**（需浏览器工具，与 madewithjev 遗留项合并做）。

## 4. 可移植模式清单
1. **每条数字带溯源链**：结果 json/fixture/runner 全 committed + prompt hash——我们批次报告的复测表升级为"宣称 → 出处链接 → 实测 → 偏差"四列，出处不可点=数字不采信。
2. **claim boundary 句式**："这是系统对比而非语义等价宣称"、"覆盖可对齐的 102 行，不是 TypeSafe 报的 711 行聚合"——我们所有对照实验照此写边界，防 DoD 复验时被自己报告的含糊话骗过。
3. **模型尺寸-质量梯子**：给我们"本地复刻最少要多大模型"提供实测锚（0.6B 不够、2B 勉强、4B 到 0.81），directives 我们权重预算（30GB 上限内选 4B 级是甜点）。
4. **加速路径的语义代价必测**：任何量化/缓存/复用改动都要报"argmax 改变数"——对应我们未来 `--provider onnx` 的验收。
- 反模式（不搬）：自研简化输入格式——我们已决定对齐 TypeSafe wire format（kev 路线），不应再造一层。

## 5. 与本地链路映射
- DoD 第 4 条（复跑指标复测表）：SemIf 的 REPRODUCE.md + results/raw/ 结构就是复测表该长成的样子，直接模仿。
- `run_plan_eval.py`：给每个 gold 判分记录加 prompt hash 与环境字段，使回归对比可溯源。
- evals.typesafe.ai：SemIf 用它做子集对齐——**B0 遗留的 evals HTML（65KB 未解析）可以先解析**，它就是我们的公共对照集。

## 6. 复测表
| 指标 | 宣称 | 实测 | 环境 | 偏差 |
|---|---|---|---|---|
| 21 准则 direct 延迟 | 1.023s (RTX 3090) | 未跑通 | 本机无 CUDA；4B 超预算 | 采信（raw json committed） |
| TypeSafe 子集一致率 | 0.845 (4B) / Jev 0.883 | 未复现 | 同上 | 采信 |

## 7. 结论
- [x] **深采**：宣称纪律四列复测表 + claim boundary 句式 + 尺寸-质量梯子 + 加速语义代价，全部搬进我们的报告规范与 DoD。
- 联动：WebGPU demo 留给浏览器工具会话补测（与 madewithjev 同批）。
