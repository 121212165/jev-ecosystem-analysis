# devmortimer/pi-warden — 深读档

> STATUS: 深采（B4 晋级名额）｜ 分析人：本战役 agent ｜ 日期：2026-09-19

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | devmortimer/pi-warden（Pi 编码 agent 的护栏扩展） |
| 类别 | B4 Agent 决策 |
| License | MIT |
| 提交 | 首 2026-09-16／跨 09-17→09-19 三日／作者 DevMortimer + MacLeodMike（2 人，非脚手架） |
| Stars | 70（本批晋级胜出，非预排序头名） |
| 真实调用 Jev | 是——经 `pi-typesafe` 的 `ask/choice/noul/score`；README 附 `npm run test:live` 真跑输出（含 verdict 原文） |
| 文档占比 | README 225 行，判定逻辑用散文 + 代码块各半，非纯宣传 |

## 1. 接口形态
- 三原语混用：动作判定用固定问题集（irreversible/off-task/changes-anything/relates-to-task/contradicts-plan/effect-visible）→ 概率；规则合规用四态 Choice（compliant/violation/not applicable/insufficient context）。
- 一次请求打包：用户请求 + 至多 8 条上文 + agent 行动前的自述计划 + 待判调用本身；write 时 slop/security 问题"搭车"同一请求，规则检查是并行的第二请求。
- 关键点：**"insufficient context" 是显式第四态**，不是把缺上下文硬塞进 compliant/violation 二选一——与 snifftest 的 not_for 字段同一血统。

## 2. 校准与阈值策略
- 三条 hold 线：破坏性模式命中 / `deny` 规则 / `irreversible ≥ 0.7`。其余（off-task、plan-mismatch、slop、规则违规、安全味）一律"告诉 agent 但放行"。
- 规则违规线：violation ≥ 0.7 才回引规则文本，且写操作永不 hold（半途文件更糟）。
- **在自有数据上量过校准**：`calibrate-action.mjs --all` 回放 321 会话/17,160 次受保护调用 → 42 次 hold，用户下一条消息批准 5 次（即 37 次站得住）；off-task 触发 56 次误唤"无一抱怨"→ 降级为只 steer 不 hold。这正是 yibie"置信 0.82 实准 0.70"教训的正向解法：阈值被回放数据改写过。
- 无 fallback 升级 LLM——降级路径是**离线仍跑**：无 key 时模式表/失控停止/重复输出/敏感路径/凭据形状照常工作。

## 3. 工程质量
- `npm run check` = 类型检查 + **185 个离线测试（mock transport）** + 构建；`test:live` 才花真 token；`eval:ab --dry-run` 列批次不花费。三层"离线可验证"设计罕见扎实。
- provider 抽象：guard 是纯函数，任何带 `evaluate` 的 judge 都能注入，库不依赖 Pi 运行时（§7 复跑据此绕开 pi-tui）。
- 错误处理：模式表设地板、Jev 只能抬高不能压低；agent 计划可加提醒但永不能撤销一次 hold——**概率非法/冲突时的优先级写死在架构里**。
- 成本/延迟：动作判定 ~0.3s/次，有数；155x/$0.0002 等对标在兄弟库，本库自报只到"够便宜到每次受保护调用都跑"。

## 4. 可移植模式清单
1. **机械 checker 与被测件零共享代码 + fixture 埋捷径陷阱**：它的 A/B（150 配对 run，违规 6→0）之所以可信，是因为评分脚本不 import guard 逻辑、且测试样本故意"能过浅检却违反深规"。→ 搬进 DoD-2：每条建议的验收样本必须"过表面检查但违反实质"，checker 独立于被验收代码。
2. **"回放自有会话→改阈值"闭环**：`/warden status` 持续把用户对每次 hold 的反应（批准/拒绝/转向/抱怨）当标签。→ 映射本地：jev_eval 的 quarantine 复核结果应回灌成阈值拟合数据（接 B3-S1 jevcal 思路，但这里是"用真实使用流而非留出集"）。
3. **四态判定含 insufficient-context**：题面信息不足时有合法出口，不污染正负样本。→ 直接进我们 noul 题的枚举扩展（B5 §四 no_judgment 同源）。
4. **模式地板 + 概率只收紧**：确定性规则先设不可降下界，模型概率只能在其上更严。→ 映射 K50/K100 硬指标先于主观档：硬指标违规时 LLM 分只能压低不能翻案。
5. **不搬**：steer/confirm/advise 三模运行期语义（评测链路无"放行执行"这层，判定只有三带读数出口）；把护栏塞进 agent 每步的实时形态（我们是离线批量评测，节奏不同）。

## 5. 与本地 Jev 评测链路的映射
- `src/eval/jev_eval.py`：可移植件 #1（独立 checker）直接改造 DoD-2 验收脚本；#4（下界只收紧）对应"改档位不重测"防线——硬指标下界一旦违反，加权分不得救回。
- 盲审协议：#2 回灌闭环 = 把 quarantine 的人工裁决变成 gold 拟合样本，正补我们"自一致率 ≥85%"缺的持续标注流。
- Ending 二级树/Score 锚定：#3 的 insufficient-context 第四态可作"证据不足"归档出口，避免强塞主/子档。

## 6. 结论
- [x] **深采**：A/B 评测设计（零共享 checker + 捷径陷阱 fixture）与"回放改阈值"闭环是本项目给评测链路的两件硬核；离线可验证三层结构（185 mock 测试 / dry-run / 无 key 降级）是我们 demo 复跑的标杆形态。

## 7. 复跑记录（本战役第三次零 key 复跑）
- 安装：`npm install --global pi-warden` → v0.26.0 / 33s（npm 通道第二次生效）。
- 障碍：包 ESM-only，barrel `index.js` 静态 `export ... from "./widget.js"`，而 widget 顶层 `import { wrapTextWithAnsi } from "@earendil-works/pi-tui"`（Pi TUI 运行时，未随包安装）→ 直接 require 触发 ERR_MODULE_NOT_FOUND。
- 解法：全库仅 widget.js 用到 pi-tui 这一个函数、且只在状态栏渲染路径 → 写 5 行 stub + Node loader hook 重定向解析，**不改包、不触判定逻辑**。
- 结果（`evaluateAction` 无 judge = 纯离线路径）4/4 命中文档：
  | 用例 | 输出 | 对应文档断言 |
  |---|---|---|
  | `git push --force origin main` | `level=confirm source=pattern pattern=git-force-push/destructive` | 模式表设地板 ✓ |
  | `git status && ls` | `level=allow source=read-only` | 只读跳过 ✓ |
  | `supabase db reset`（离线） | `level=allow source=pattern`（无 hold） | 破坏性属 Jev 臂，离线不该拦——"未拦=设计"反例 ✓ |
  | echo 内嵌 `git push --force` 文本 | `allow` + dataText 说明 | 数据文本非命令 ✓ |
- 未跑臂：Jev 判定（0.3s/次）、`eval:ab` 150 配对——按"跑不动记录后不强跑"停；6vs0、17,160/42holds 保持"自测已发布"级，引用带限定词（见 batch04 §三）。
