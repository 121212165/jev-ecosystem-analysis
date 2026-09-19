# kyotofin/tax-doc-classifier — 深读档

> 批次 B6 晋级深读（本战役第 11 篇单库档）｜分析日期 2026-09-19

## §0 基本盘

- **星数/授权**：193★ ｜ **Apache-2.0**（另 `DATA-LICENSE.md` 单列 IRS 派生数据授权）｜ B6 全批最高星 + 唯一干净宽授权。
- **规模**：仓库总 size **49 KB**；仅 2 commits / 单作者（Nedwize）/ 活跃 1 天（2026-09-18）→ 成品整包首发，星速 ≫ 提交速（§5 I7 已注）。
- **定位**：把 PDF 税务页面分类到 261 个 IRS 表单 + 7 种页面类型；替代一套"每页发 PDF 给 Claude Sonnet + 表单表塞 prompt"的旧管线，宣称 **34× 省钱 / 6× 提速**。

## §1 接口形态（Noul / Choice / Score）

- **Choice 为主**：一次请求两问——`kind`（7 选项）+ `form`（230 选项 + `not_in_this_list`）；5 个母公司表单（5471/8865/8933/1118/5713）触发**第二小问**取其附表 → 两阶路由，层级只在"页面把母公司印得比附表更清楚"处存在。
- **Score/置信**：返回 `formConfidence` + 完整 `probabilities`。关键定义：**`formConfidence` = 各步置信取 min**（不是均值）——最弱一步决定整体可信度。
- **无 Noul 面**：纯判别，不产文本。空页**不发请求**直接判 `blank`（省调用）。

## §2 校准与阈值

- **门限**：`gated = formConfidence >= 0.95`。gate 上执行、gate 下**兜底回退到"你今天用的任何东西"**（不是硬猜）。
- **严格计分定义**：一页判错**或**置信<0.95 都算 error（strict）。两语料：
  | 语料 | 页 | 表单 | 判错 | strict err | 成本 |
  |---|---|---|---|---|---|
  | TaxCalcBench 填充表 | 314 | 15 | 0 | **0 (0.00%)** | $0.36 |
  | 空白 IRS 表 | 753 | 261 | 0 | 38 (5.05%) | $0.86 |
- **诚实标注**：38 个 strict error **无一"判错"**，全是"不点名表单的说明页/深层企业表/单附表对冲母公司"的低置信页；且明文"**先在你自己页面上校准，再选门限**"——不假装 0.95 通用。
- 三种页面类型（state/broker/letter）**定义了但未评测** → 明说不宣称。

## §3 工程质量

- `pnpm install && pnpm typecheck && pnpm test` 全离线（仅 `pnpm eval` 需 `TYPESAFE_API_KEY`）。
- **数据完整性门**：`data/criteria.json` 由 `pnpm build-criteria` 从 IRS XLSX + 官方 PDF 机械生成（**从不手改**）；`src/ids.test.ts` 第 1 条断言"criteria.json 每个 id 必合 `ID_GRAMMAR`"，坏数据直接让测试红。
- **Backend 抽象**：单方法 `ask(state, questions) → {answers, inputTokens}`，每个 answer 是选项上的概率分布；`jevBackend` 是唯一实现，但"任何能返回校准概率的模型都可插" → 与被评模型解耦。
- 键从环境读、`never written to disk or logged`。

## §4 可移植模式

**可抄（→ 我们链路）**：
1. **置信 = 多步取 min**（§1/§2）：复合判定的可信度由最弱环节定，杜绝"平均掉一个低置信步"。
2. **strict 计分 = 错 或 低置信 皆计错**：把"不确定"显式并入错误预算，而非只数硬错——正对我们热区块"宁漏勿误杀"的度量口径。
3. **门限下兜底而非硬路由**：低置信时交回旧逻辑/人工，不是勉强给个答案。
4. **数据文件机械生成 + 语法测试守门**：金标/配置类数据不手改，用 test 拒非法结构（对照我们 eval/inventory 的 build 脚本化）。
5. **"先自校再选门限"写进文档**：把阈值可移植性的边界主动交代。

**反模式（不抄）**：
- 无（本库诚实度高）。唯一保留：其两阶"母公司→附表"层级依赖 IRS 印刷惯例这一特定领域，不具普适迁移价值。

## §5 本地链路映射（jev_eval.py / <未发布长篇> / 盲审协议）

- **min-over-steps** → Ending 二级树复合置信计算：子节点任一低置信应压低父判定，勿用均值。
- **strict error 定义** → `hot_block_overlap_with_mid` 等"误杀即错"场景的评分口径直接可借。
- **Backend 解耦 + 独立数据门** → 呼应本批 S-B6-1（judge 循环性）与 pi-warden"checker 零共享代码"：评分/数据完整性与被评对象隔离。
- **不抄**：TaxCalcBench 外部语料不随仓（我们金标须自带可复现）。

## §6 结论：**深采（晋级）** ✓✓✓

三标准全中：①零 key 离线臂实跑通过（typecheck+vitest）；②量化面极丰（0.00%/5.05%、34×/6×、0.95 门、min-over-steps）；③真实调用结构可复现（`pnpm eval` + 逐页结果落 `eval/results/`，虽需 key 但脚手架齐全）。B6 全批唯一同时具备"可复现严格基准 + 同机基线对照 + 数据溯源 + 诚实 limits"的评测设计库。

## §7 零 key 复跑记录

| 步骤 | 命令 | 结果 |
|---|---|---|
| 克隆 | `git clone --depth 1`（gh-proxy） | 49 KB 秒下 |
| 装依赖 | `pnpm install` | 18.5s（esbuild 构建脚本需 `pnpm rebuild esbuild` 放行 vitest 原生二进制） |
| 类型 | `pnpm typecheck` | **exit 0** |
| 测试 | `pnpm test`（vitest） | **3/3 通过**（src/ids.test.ts） |
| 数据核验 | `json.load(data/criteria.json)` | **独立数得 261 key** ↔ 宣称"261 IRS forms"逐字对上 |

- **达成**：离线臂全绿；criteria.json 表单数被独立复核（非抄 README）。
- **未跑**：`pnpm eval`（需 `TYPESAFE_API_KEY`）→ 0.00%/5.05% 与 34×/6× 属"结构可复现、数值作者自报"，依"跑不动不强跑"止步，不冒充实测。
- 复跑产物：`_b6/tdc/`（浅克隆）；信号快照 `_b6/kyotofin__tax-doc-classifier.md`。
