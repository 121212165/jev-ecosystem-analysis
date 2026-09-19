# Batch 02 报告 — 游戏/实时决策（"典型 demo"主矿）

> 日期：2026-09-19 · 池：inventory v4 之 B2 = 21 库（README 到手 21/21）
> 判定标准（PLAN v2）：典型 demo 预期——本地完整回路零 LLM 生成（读 state → 问 → 执行）
> 产出：深采 2 · 浅采(含要点) 7 · 留矩阵 9 · 移批 1 · 丢弃(含候选) 2
> 修订单（RB2 复审后）：头部原写『浅 8·留 6·移 3』与矩阵实态不符；且 killmyidea/jevthoven/slidepilot 的移批建议未经批次定义核对即写出，复核后改判留矩阵（见 §2 行内改注）

## 1. 深读换槽（证据驱动，续 B1 先例）

PLAN 预点名 pokemon + drone 路线。实扫后深读槽改为 **jev-ultrafast + jev-drone**：

| 候选 | 换槽依据 |
|---|---|
| browser-use/jev-ultrafast ↑ | 池内★断层第一（6238★）；官方合作；证据纪律最严（headline "7.1 s" 正文收敛为 7,073 ms 且标测量起点；"3 repeats of one task, not a general reliability benchmark" 自我设限）；带来全池独有的"投机多头单往返"架构 |
| milanboers/jev-plays-pokemon ↓浅采+ | 1★；battle 自认弱点、仅教程区调优；其 RAM→文本状态面与 mario 对重叠（对照表已覆盖），边际信息低于 ultrafast |
| romanslack/jev-drone = | 维持：全批唯一 no-Jev 消融表 + 负面结果自报（早期竞技场 0/3） |

## 2. Stay/Go 矩阵（21 库）

| 库 | ★ | License | 处置 | 一句话理由 |
|---|---|---|---|---|
| browser-use/jev-ultrafast | 6238 | MIT | **深采** | 投机多头单往返 + 合法域预过滤 + typed→受限执行范本 |
| romanslack/jev-drone | 66 | MIT | **深采** | 消融纪律 + "state 必须包含答案" + 分层速率职责表 |
| shantanugoel/mario-jev | 10 | 无⚠️ | 浅采+ | RAM 几何流路线代表；自报 scripted(2471) > Jev(1594) 的诚实数字；无 License 只读不抄 |
| fhshaik/typesafe-mario | 268 | 无⚠️ | 浅采+ | 对象中心 JSON + `reaction_timing` 把模型自身延迟做成 typed fact；无 License 只读不抄 |
| ably-labs/jev-pong | 0 | Apache-2.0 | 浅采 | 跨模型延迟对照表（Jev 227ms/4.4dq/s vs 聊天模型 2.5–3.5s）；`replay-stats.json` 构建时读数=数字防腐机制 |
| milanboers/jev-plays-pokemon | 1 | NOASSERTION⚠️只读不抄 | 浅采 | harness 记忆协议（recent_hints/recent_actions/explored_fraction）+ warp 表读出口 + 成本表（$0.042/MTok、≈1600–2100 tok/决策） |
| lbotinelly/jev-little-airways | 3 | MIT | 浅采 | "决策要估计量不要原始数据"（`faults.fuel:0.83` 反例）+ 150ms 校准置信度话术 |
| phyous/tsai-sc | 15 | MIT | 浅采 | StarCraft 受限于 bounded candidate commands；median API 382.95 ms 入账 |
| anxkhn/jevplayspokemon | 2 | GPL-3.0 | 浅采 | 语义 ID 反位置漂移（switch=personality value 非 slot 3）；"no backup brain"（非法即停） |
| owner-B/heist-one | 5 | MIT | 留矩阵 | 潜行游戏+全量决策遥测（evidence/proposed/applied/latency/fallback）；视频工程占比大 |
| jexp/neo4jev | 21 | MIT | 留矩阵 | 图导航：Noul "goal reached" 过阈值即停——评测链路可借的停止判据 |
| thruwire/foreman | 315 | MIT | **移 B4** | PLAN 已预告：completion-gate 模式（needs human 0.80 表），属编码代理监管而非游戏 |
| monteduro/killmyidea | 17 | 无 | 留矩阵（B3 交叉复核标注） | 创意评估器（8 Score×25 加权→KILL/FIX/SHIP 阈值 50/65）；属'读 state→问→执行'回路成立，但Score→verdict 形态与 B3 评分批同构，FINAL 前交叉复核 |
| cocktailpeanut/jevthoven | 4 | 无 | 留矩阵 | 符号音乐工作室：选计划/乐器/小节也是实时决策回路，符合 B2 标准；B6 定义（分类路由+审核）经核不适用 |
| harshil1712/slidepilot | 3 | MIT | 留矩阵 | 演讲字幕推进器；三阈值 0.68/0.65/0.55 是好的生产 gate 配置样例，B6 定义不符维持本批 |
| kavehmz/typesafe-playground | 9 | 无 | 留矩阵 | Docker+多 demo 合集，单库信息密度低 |
| kxzk/typesafe-jev-drone-demo | 0 | 无 | 留矩阵 | 与 romanslack 同题但无消融；其"rechecks chosen movement against current world"校验步可摘一句 |
| lukaske/jev-doom-agent | 1 | 无 | 留矩阵 | WASM Doom+空间 state，README 2.9KB 信息薄 |
| siroccomask/snake-jev | 0 | MIT | 留矩阵 | 自报"不规划全局长路线"的诚实边界声明 |
| sorrycc/typesafe-snake | 17 | 无 | 丢弃候选 | 1.2KB 纯外链，无宣称无数据 |
| joshlarsen/jev-t-rex-runner | 0 | BSD-3 | 丢弃 | Chromium 跑酷换皮+贡献者头像墙，JE 信息量≈0 |

> 挂账：mario 双库**均无 License**（gh api 确认 lic=None）→ 只能做模式借鉴，不可抄码。此前我们默认"复刻库皆 MIT"需在后续批次继续逐库核对。

## 3. PLAN 点名对照：mario 双库 = RAM 观察的两代压缩

同题（SMB1 1-1、RAM→结构化、无截图）不同答案，是 PLAN "state 设计模式"最干净的一组对照：

| 维度 | shantanugoel/mario-jev | fhshaik/typesafe-mario |
|---|---|---|
| state 粒度 | **几何流**：tile 列、跳跃走廊 128px 跨度、逐帧 transition、recent_frames | **语义流**：player/trajectory/hazard/terrain/reaction_timing/recent_control/episode 七组对象中心 JSON |
| 提问形态 | 并行 4 问：movement(Choice)+start_jump/ceiling_hop/sustain_jump(Noul, 0.5 阈)，代码合成按键 | 每请求 3 判：Choice(宏动作)+Noul(该跳吗)+Score(danger，仅供可视化) |
| 时序处理 | 4 帧动作+落地中断（自报多耗 ~50% 调用） | 把**实测观测-执行延迟**做成 typed fact `jump_must_start_this_decision` 直接喂给模型 |
| 成绩自报 | scripted x=2471 > Jev x=1594（明示"individual runs, not completion rate"） | 无量化通关宣称（仅 dashboard 遥测） |
| 对我们的启示 | 多原语拆按钮合成 vs 宏动作直选 = 我们"读字母/写数字"之外的第三种分叉：**拆问题 vs 拆动作** | "告诉模型它自己有几帧反应时间"是把回路约束写进 state 的孤例，值得进 state 设计检查单 |

结论：生态内 RAM→结构化已无异议，前沿差在**语义压缩层谁来做**——shantanugoel 把几何原样上供让 Jev 自己推，fhshaik 由代码预推导成事实。drone 的"state 必须包含答案"表明后者是当前胜率更高的一极。

## 4. 复跑状态（续 PLAN"跑不动记录后不强跑"）

B2 全部库的 Jev 侧回路都需要 `TYPESAFE_API_KEY`（云端 API）→ **零 key 不可复跑**，与 B1 结论一致，无新增例外。可离线部分（`mario-jev --policy scripted`、`jev-drone --no-jev` 消融、pong `pnpm test`）全部卡在整仓传输（B1 五路失败结论，不重复撞墙）。
→ DoD 未完成项 #1 追加子条目：**jev-drone 免费消融侧**（验证 baseline 结构性卡死 17.7m）列为拿到传输窗口后的首选项——它零成本、直接检验"判断层增益"宣称。

## 5. I7 第二维度（提交分布）证据

- B2 全池 created=2026-09-16..18、pushed 与 created 间隔 ≤2 天：**整批是发布窗口期产物**，无"隔月续更"库——后续批次的 commit 分布监控（owner-A/owner-B 等）在此批未见新异常。
- 0★+单日+无 License 的旧可疑模式在本批仅 joshlarsen/kxzk/siroccomask 命中，但均有真实可运行代码结构（非 us/jev-local 式空壳），降级为普通低信息库。
- 6238★/2 天 = 官方 promo 效应（browser-use 本体大项目引流），不构成质量证据也不构成造假证据。

## 6. 本批可移植要点（进流程规范的排序）

1. **state 入库前必查"答案在 state 内"**（drone）→ 写进盲审 gold 样本入库检查单。
2. **报告数字脚本生成**（pong 的 replay-stats.json 构建时读数）→ 我们 batch 报告统计行应改由脚本 dump，杜绝 batch00 式数字漂移复发。
3. **合法域预过滤**（ultrafast compatible-options-only）→ Ending 二级树子档提问时裁剪非法选项。
4. **硬否决层先于置信度阈值**（drone 物理否决）→ 评测链路三层阈值前加格式/长度/缺字段 veto。
5. **消融基线列**（drone `--no-jev`）→ 宣称增益的评测报告固定带无 Jev 对照列，负面结果照报。
6. **测量边界句**（ultrafast/pong）→ 每条量化宣称必含"从何时测、含什么、几次重复、不是什么"。
7. 估计量优先于原始遥测（little-airways）+ 模型自延迟入 state（fhshaik）→ 我们决策层 prompt 的两条 state 设计守则。

## 7. 产物索引

- `analyses/browser-use__jev-ultrafast.md`（深采）
- `analyses/romanslack__jev-drone.md`（深采）
- `_b2/*.md`（21 份 README 快照）
- 脚本已通用化：`b2_fetch.py <BATCH>` / `b2_meta.py <BATCH>` 可直接用于 B3+
- 挂账更新：**~~foreman→B4~~ ✅已入 inventory v5（B2=20/B4=30/总 266）**；killmyidea/jevthoven/slidepilot 复核后改判留矩阵，不再挂账；sorrycc 丢弃候选终审随 FINAL；DoD#1 新增 drone 消融优先项
- 本轮复审（RB2-A-01/RB2-B-01，`eval/b2_review.jsonl`，10 问盲判 10/10）新增流程戒条：①**名→源回溯**：引用任何『PLAN 点名库』前必须先命中 PLAN/inventory 原文（本会话曾带 13 个压缩虚构名空跑一次探测，零污染但零容忍）；②**负结果双通道**：目录级检索 0 命中必须换单文件/第二工具交叉后才可下『不存在』结论（ripgrep 同会话内一真阴一假阴）；③**移批判定须先核批次定义**（三条『移批建议』中两条引用了不存在的 B7/B8 定义，实际 B7=SDK/Infra）
