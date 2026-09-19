# romanslack/jev-drone — 分层速率控制回路中的"判断层"（附消融）

> STATUS: 深采 · 类别：B2 · 选取理由：全批唯一带 **no-Jev 消融对照表** 的库；宣称纪律与 SemIf 同级（"defensible claim is narrow and specific"）；"state 必须包含答案"是生态里最有价值的一条可迁移教训。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/romanslack/jev-drone |
| 类别 | B2（机器人/实时决策，MuJoCo 摄影机-only 无人机） |
| License | MIT ✅（Skydio X2 模型另有 Menagerie 许可） |
| 创建/最近推送 | 2026-09-16 / 2026-09-17 |
| Stars | 66 |
| 真实调用 Jev API | ✅ 三层证据：`tactics.py` 全部 Jev-facing 问题/rubric/阈值集中声明；运行日志 `TRACE=1` 打印每次判断；结果表带调用数/延迟/token（80 calls/65s/0.11s median/96k tokens） |
| prompt 文档占比 | README 14KB，一半是量化结果+事故复盘，散文占比低 |

## 1. 接口形态
- **一问三原语同请求**：`maneuver`(Choice 6 选项) + `risk`(Score) + `target_truly_lost`(Noul)，一次调用。是"13 问一次调用"并行提问家族的真实工程样本。
- **分层速率架构**（生态里最清晰的职责表）：500Hz 几何控制 / 50Hz 安全反射（**可否决 Jev**）/ 15Hz 感知 / **~2.5Hz Jev 战术判断，advisory only**。"Code decides *what is there*; Jev decides *what to do about it*."
- state：numpy 深度+分割→紧凑符号场景（5 前向距离扇区、遮挡物高度、顶缘是否可见、自身爬升上限），**无真值泄漏**（no ground truth）。
- 元数据用法：不是取 argmax——"muddy case"里 Choice p=0.24 被弃用，改用同请求 Noul=0.12 做门控，**"Use the primitive that actually fits the question"**。

## 2. 校准与阈值策略
- 代码决定何时问：开阔走廊+目标在视→不发请求；场景指纹去重→未变场景复用上轮判断（65s 飞行仅 ~110 次调用的原因）。
- 硬性物理否决：climb 只在实测顶缘低于爬升 ceiling 时被放行——**置信度再高也过不了物理检查**，这是比阈值更硬的门。
- 校准诚实度：手搭场景 6/7 强概率正确，第 7 例（短暂遮挡）明示"muddy"并解释改用 Noul——等于自带失败案例分析。

## 3. 工程质量
- 一键程度高：`./setup.sh` + `.env` + 单命令跑；消融免费（`--no-jev` 不调 API）；`replay.py` 从 `.tape.npy` 重渲视频零 API。
- **消融表**：baseline 三次全卡 17.7m（站2），Jev 77.5m 通关；target in view 19%→82%；reflex 卡死时间 65-71%→9%；碰撞 0。
- **主动报负面结果**：更早的简单竞技场 3-seed 匹配对照 **Jev 0/3 无优势**；tunnel 实验只算 partial（零碰撞 94% 可视的最佳运行有，但不能稳定通关）。单跑 65s 的 Jev 列自己标注"not a seed-matched average"。
- 延迟预算分解（罕见的好东西）：感知 0.03s + Jev 0.118s + 决策龄 0.024s + **机体 0.70s 横移 2m** →"模型占回路 13%，机体占 80%，再快也没用"。
- 「Simulator bugs worth stealing」13 条工程事故复盘（MuJoCo znear 是分数不是米、四元数误差救 179° 倒飞、仿真时间≠墙钟时间导致 152/182 请求堆积……）。

## 4. 可移植模式清单
1. **★ state 必须包含答案**："climb 永不出现"根因是水平扇区无垂直信息——**state-design bug，不是 model failure**。对照我们评测链路：金标判不准时先查喂进去的 state 是否含判定依据（如 K 完成度必须带可数的转折字段，情绪密度必须带逐千字标记），再怀疑模型。
2. **★ 物理/程序硬否决优先于置信度**：我们的三层阈值(0.85/0.60)之上可加一层"硬规则否决"（格式非法、长度越界、字段缺失直接打回，不看 confidence）。
3. **★ 免费消融基线**：`--no-jev` 不调 API 即出对照。我们的 `JEV_PROVIDER=local` 天然支持——评测报告应固定带"无 Jev 基线"列，声称增益必须有消融支撑（学它的 0/3 负面结果也要报）。
4. **★ 按问题选原语**：Choice 犹豫时看同请求的 Noul——多原语同请求时，每个子问题用最贴合的原语做门控，不要全押 Choice。
5. 场景指纹复用判断（相同 state 不重问）：可省 JEV_SAMPLES 预算，但**盲审协议场景不可复用**（会污染独立性），只可用于生产 gate 不可用于评测采样。
6. 反模式：**仿真时间不 pacing 墙钟**——若我们做时延/吞吐类评测，必须像它踩过的坑一样先锁时钟，否则测的是排队不是模型。

## 5. 与本地 Jev 评测链路的映射
- `jev_eval.py`：报告模板加"消融基线"列（模式3）+ "hard-veto 前置层"（模式2）；多原语 gold 条目按模式4 设计门控字段。
- 盲审协议：模式1 转成检查清单条目——"判定所需信息是否 100% 在 state 内"应作为 gold 样本入库前的必查项。
- 三层阈值体系：加硬否决后变"veto → auto(≥0.85) → review → quarantine"。

## 6. 结论
- [x] **深采**：判断层职责表 + 消融纪律 + state-design 教训，三样都能直接进我们流程规范。

## 7. 复现状态
- **环境阻断**：MuJoCo 需 GL 上下文（glfw/egl）+ `TYPESAFE_API_KEY`；消融半侧（`--no-jev`）理论可离线跑，但整仓 clone 在 B1 已证实的批量传输阻断之下（同一网络窗口不重复撞墙）。记入 DoD 未完成项：优先复跑 **免费消融侧**（验证 baseline 卡 17.7m 的结构不可达性），条件=可获得整仓传输窗口。
