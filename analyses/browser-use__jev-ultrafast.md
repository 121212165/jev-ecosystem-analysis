# browser-use/jev-ultrafast — 结构化 DOM 快照驱动的超快浏览器决策回路

> STATUS: 深采 · 类别：B2 游戏/实时决策批 · 选取理由：池内★最高（6238★，五目录均点名）、证据纪律最严（每条量化宣称都标了测量边界）、"动态索引动作空间 + 单请求多头"是我们评测链路里没有的架构面。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/browser-use/jev-ultrafast |
| 类别 | B2（实时决策 · 浏览器自动化，PLAN 点名五目录同标） |
| License | MIT ✅（可抄） |
| 首次/最近提交 | created 2026-09-16 / pushed 2026-09-18（发布即火，2 天 6k★） |
| Stars | 6238（全池断层第一） |
| 真实调用 Jev API | ✅ 是。走 `api.typesafe.ai` Jev，"one TypeSafe request" 产 operation+target；文档明列 `TYPESAFE_API_KEY`。README 有 loop 链接 `jev_ultrafast/agent.py`、`model.py`（Dynamic operation/target heads） |
| prompt 文档占比 | README 8.6KB，代码/文档配比健康；"Small enough to read"表列出 6 个源文件职责，非散文堆砌 |

## 1. 接口形态
- 原语：**Choice 为主**（operation 选型 + 每个 target 头选型）。一次网络往返内并行问多个头：`operation` / `click_target` / `type_text_target` / `select_target`。
- 关键设计：**"Target questions are speculative"** —— operation 与 target 头共享同一份被观测 state，一次请求全出，但只有 operation 命中的那个 target 会执行。**两次决策，一次往返**（省延迟的核心）。
- state 结构：**结构化 DOM 元素表**（`[1] button ... · Round trip`），非截图、非散文。"No screenshots in the default agent loop. Jev consumes structured state."——与 mario/pokemon 的 RAM→JSON 同族，但这里是 DOM→索引元素表。
- 每个 target 头**只喂兼容元素**（Each target head contains only compatible elements）——动作合法性由 harness 预过滤，模型不在非法选项里幻想。

## 2. 校准与阈值策略
- 未见显式 confidence 阈值分层；把关靠**执行期校验**而非阈值：每个被选 target 从"已观测节点"解析，执行前 recheck 页面新鲜度 + 点击遮挡（occlusion），"Animation alone does not force another prediction"。
- 安全边界是硬的：**模型输出永不变成选择器/坐标/shell/可执行 JS**；text-helper 输出必须先 parse 成小 JSON 才允许输入。→ 这是"typed decision → 受限执行"的教科书隔离。
- 采样：未提多样采样；延迟敏感场景（7 秒目标）走的是单请求 + 投机多头，而非重复采样取均值——与我们 JEV_SAMPLES=5 的取舍相反（见 §4 反模式）。

## 3. 工程质量
- 可运行性：`uv sync` → `uv run jev` → 本地 inspector（编号元素、operation/target 概率、执行动作全可视化）。离线测试 `uv run pytest`；`scripts/check_guards.py` 无模型调用即可验真实控件。
- 复现证据链：录制脚本 `record_flights.py` + `render_demo.py` 以 1× 渲染、裁掉 Google 账号栏；每条量化宣称都指向 `docs/performance.md` 溯源（runs/failures/source hashes/measurement boundaries）。**"DONE choice 仍需独立结果校验"**——不信任模型自报完成。
- 成本/延迟：全部可溯源且标注测量起点（"timing starts after initial page observation"）。

## 4. 可移植模式清单（★ = 优先搬）
1. **★ 投机多头单往返**：一次请求并行问"选哪个操作 + 该操作下的目标元素"，只有被选操作的 target 落地。搬到我们决策/评测链路：当"选类别 + 选类别内实例"是两步时，合并为一次 typed 调用可省一次往返（对照 `jev_eval.py` 目前逐问组织）。
2. **★ 合法性预过滤（only compatible options offered）**：harness 先把非法选项剔除再问模型。我们的 Ending 二级树（主档→子档）可照此：问子档时只喂主档合法子集，避免模型跨档幻想。
3. **★  typed→受限执行 + 执行前重校验**：模型只出"编号/标签"，落地前用真实几何/新鲜度再验；模型永不产出可执行选择器/坐标。对应我们"读字母不写数字"路线（见 mini-jev 挂账），是本批又一独立佐证。
4. **测量边界显式化**：每个数字标"从何时测含哪些环节、几个 repeat、什么 profile、不是什么"。这是我们 batch 报告/宣称表该直接采纳的书写规范（与 B1 SemIf 的 4 列溯源表同族，此处再补"边界句"）。
5. 反模式（不搬）：**单请求投机多头用于延迟敏感**——它牺牲了多次采样的一致性红利换延迟。我们的评测链路要的是稳定校准分数，不能照搬其"单样本换速度"；两条路线（JEV_SAMPLES=5 求稳 vs 投机多头求快）应显式并存、按任务选。

## 5. 与本地 Jev 评测链路的映射
- `src/eval/jev_eval.py`：合法性预过滤(模式2)可用于 Choice 题的选项裁剪；投机单往返(模式1)可作 adapter provider 的批量提问合并。
- Ending 二级树：主档→子档用"compatible options only"约束，减少跨档幻觉。
- 盲审协议：模式4"边界句"直接提升 gold 样本 note 的可审计性。
- typed→受限执行(模式3)：强化"读字母不写数字"证据链，呼应 mini-jev 挂账的字母读出对照实验。

## 6. 结论
- [x] **深采**：架构面（动态索引动作空间 + 投机多头 + 合法域预过滤 + typed→受限执行）是本批最直接可搬的一库；证据纪律是书写规范级别的模板。唯一不能复现处：需 Chrome+Browser Harness+付费 API（见下）。

## 7. 复现状态（本地环境）
- **环境阻断**：需要 (a) `TYPESAFE_API_KEY` + OpenRouter `TEXT_MODEL_API_KEY`（云端付费，无 key 不可跑）；(b) Chrome + Browser Harness CDP 连接；(c) 实时网页。本机 CPU-only、无 key、且 PLAN 定"零 LLM 生成、纯决策回路"针对的是游戏本地回路——本库是浏览器回路，天然不满足一键离线复跑。
- 依据 PLAN"跑不动记录后不强跑"→ 记入 DoD 未完成项，复现条件：有 API key + 联网 GUI 机时。
