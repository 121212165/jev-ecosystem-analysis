# abhixhek/jevcal — 把"阈值抄用不可靠"痛点做成一条命令

> STATUS: 深采 · 类别：B3 · 选取理由：五目录同收（n_lists=5，B3 最高）；**全生态唯一零 key 可跑**（内置模拟器 demo）的评测工具；功能与我们三层阈值痛点一一对位；作者对"厂商数字不可信"的立场与我们"LLM-as-Jev 本地判"同源。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/abhixhek/jevcal |
| License | MIT ✅ |
| 创建/推送 | 见 b3_meta（发布窗口期） |
| Stars | 见元数据表 |
| 真实调用 Jev API | ✅ "Verified end to end against the live TypeSafe API on `jev-1.13.0`, 2026-09-18"；且**声明式区分**：demo 用模拟器（"That is simulator output, not a Jev benchmark"），不混充 |
| prompt 文档占比 | README 8.8KB，几乎全是工作流+数字语义，无灌水 |

## 1. 接口形态
- questions.yaml 与 TypeSafe API 同形（noul/choice + criteria 档位描述 + 每题 target）。
- 全流程七命令：`lint`(措辞缺陷静态检核，零 key) → `label`(LLM 教师补标) → `measure` → `compile`(选阈值出 lock+报告，零 key) → `run` → `optimize`(LLM 改写问题、留出集裁决保留) → `check`(CI 防漂移)。
- 并行提问："extra questions are nearly free on Jev"——optimize 把全部候选改写放进单请求逐行评估。
- lock 文件 = 阈值 + **证据**（`decisions.lock.json` "thresholds + the evidence behind them"）。

## 2. 校准与阈值策略（本库核心）
- 阈值不是拍的：在你的数据上按"达到目标准确率的最低阈值"拟合，**半数选阈、半数验证**；验证不过就明说而不是报漂亮数。`--conservative` 要求 95% 置信下界过线。
- 置信度度量可换：`top_prob` 默认，`margin`/`entropy`/API 自带 `confidence` 同测，`--measure auto` 只在显著更分时切换——**"哪个分数真正区分对错"是测出来的，不是假设的**。
- 级联经济学：报告直接给"多少流量要升级给 LLM、省了百分之几"；"bottleneck 是 is_urgent 一题"——按题归因。
- "confident and wrong" 行单独列出且**优先读**："多数是错标或问题措辞歧义，修它们比调阈值更能移动数字"。
- 诚实边界：<100 标注行/题 阈值别指望hold；API 概率只精确到两位小数且同请求偶发换答案（check 留容差，勿设零）。

## 3. 工程质量
- 零 key 路径完整（demo/lint/compile/check-cache 全离线）；`claude-cli:<model>` provider 甚至复用本地 Claude Code 登录不用 API key——**provider 抽象含"无 key 本地模式"，与我们 JEV_PROVIDER=local 同构**。
- 报告= reliability 图 + accuracy-vs-coverage 曲线 + 逐答案准确率 + 成本拆分（HTML）。
- CI 防漂移：accepted acc 掉线 / coverage 下降 / `--strict` 下模型版本≠调阈版本 → exit 1。**"jev-latest 是移动的别名，今天调的阈值明天漂"被点名**。

## 4. 可移植模式清单
1. **★ 阈值拟合脚本化**：我们三层线 (0.85/0.60) 至今是拍的。照 jevcal 做一个 `fit_thresholds.py`：在既有 gold 上按题拟"达目标准确率最低阈 + 留出验证"，输出 lock+证据，报告引用之。（验收：新 gold 划分训练/验证两半，验证半 accepted-acc ≥ 目标才算过）
2. **★ lint 措辞静态检核**：negations/counting/dates/compound/overlap 五类已知弱点的题目正则——盲审 gold 入库前先过 lint。（验收：对 b0/b2_review 全部题跑一遍，命中项人工确认 ≥1 例真缺陷）
3. **★ "confident-and-wrong"清单优先**：jev_eval.py 输出加一节列出高置信但盲判翻转/低分的样本，第一优先复核——大概率是题目措辞或 gold 本身错，不是模型。
4. **★ 模型版本 pin + check 防漂移**：gold 文件头记 `JEV_MODEL_VERSION`（我们现在裸用"LLM-as-Jev"无版本戳）；协议升版后旧 gold 全部重验（`--strict` 语义）。
5. **--measure auto 思路**：我们只信 confidence 字段；jevcal 证明 margin/entropy 可同测选优——本地链路可直接比较"自报 confidence vs 概率分布导出量"哪个预测盲判一致率。
6. 反模式：LLM 教师补标 gold（`label`）——与我们"gold 必须人/盲审链产出"的规范冲突，最多当草稿，永不进正式库（它自己也写"teacher signal, not ground truth"）。

## 5. 与本地 Jev 评测链路的映射
- `jev_eval.py`：模式 1/3/5 直接改代码；模式 4 进 gold schema（加 model_version 字段）。
- 盲审协议：模式 2 是新增前置步骤；模式 3 是 quarantine 池的进料优先级。
- `--conservative`（95% 下界过线）→ 我们自动通过档 (≥0.85) 的上线判据应改成下界判据，样本 <30 时自动降级人工。

## 6. 结论
- [x] **深采**：jev_eval.py 改造建议清单的头号来源；DoD-2 验收步骤已随各模式内嵌。

## 7. 复跑记录 ✅（生态分析战役首例成功复跑）

通道：`codeload tarball 经 gh-proxy`（765KB，120s 内完成）——修正 B1"整仓传输全死"结论为**尺寸相关**：小仓（亚 MB）可穿，kev（百 MB 级含数据）不可。提交流：curl tarball → tar 解包 → PYTHONPATH=src 直跑，零安装零 key。

| 宣称 | 出处 | 实测 | 偏差 |
|---|---|---|---|
| demo 输出表：is_urgent 阈 0.994/handled 21.2%/accepted 100.0%/all 94.5%/ECE 3.5% | README 首段代码块 | 逐位一致（含 escalation 85.4%、$1.930/1k vs $2.25、省 14.4%） | **0**（模拟器确定性） |
| 测试套件全绿（README "Development: pytest"） | README 尾节 | 24 passed in 7.52s | ✓ |
| lock+report 产物 | 工作流第 4 步 | `jevcal-demo/decisions.lock.json` + `report.html` 落地 | ✓ |
| "内置模拟器故意 overconfident 供发现" | README | 报告确实产出 confident-and-wrong 清单节 | ✓ |

结论：①一键复跑标准①在"零 key 半侧"意义上**全满足**；②它的报告/lock 产物格式可直接拄到我们 jev_eval 输出设计（先照格式再换真数据）。
