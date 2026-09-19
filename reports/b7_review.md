# b7_review — RB7 复审轮报告

日期：2026-09-19 ｜ 工件：`eval/b7_review.jsonl`（2 条 × 5 问，13,444 B）｜ 校验：`jev_eval.py --check` **✓ 2/2**（exit 0）｜ 反向盲审：**10/10 自洽**（盲重答各 gold 值与我独立判定一致，一致率 100% ≥ 85% 门槛）

## 一、本轮性质：前置核账抓出"新子型缺陷"（发布前）

延续 B4"零新缺陷（前置核账已拦）"的传统，但本轮抓到的不是老面孔：

- **不是计数漂移**（B0 59vs67 / B2 / B3 / B5：汇总 ≠ 枚举），而是**枚举本身不完整且被污染**——初稿矩阵 Counter 自洽到 60，靠 `_rb7_precheck.py` 里 `header ok = rows==POOL(61)` 这道**与权威元数据对齐的硬门**才逼出真因：`2 条幻影 dup 占位行（stumble-dup / dakdevs-dup）+ 漏 3 实库（blakestone-x / genierobot / tumf）`。回 diff `_b7_meta.txt` 的 61 行逐一定位，删幻影 + 补 3 行后方 = 61。
- **幻影 dup 行的缺陷族**：与 B5 §七"过早勾 [x]"同宗——**把预期/意图写成既有事实**（当时预感 inventory 或有同名重复，先落成"若重复则单行合并"的占位行，而元数据证明本无重复）。落点从"复选框"扩展到"数据行"。
- **通用规则升级 R7-a**：处置 Counter 自洽 ≠ 交付完整；矩阵**必须与权威元数据池做行级 diff**（本批靠 `header ok==POOL` 一条断言触发，成本零、拦下 3 库静默漏检）。此断言已并入 B8/FINAL 前置核账模板。

## 二、单位口径缺陷的正确处置（"勿迁就"纪律的边界案例）

skillranker "README 113KB 疑似膨胀"经脚本核出 MISMATCH（÷1024 得 111KB）：

- 纪律原话是"按 MISS 定位后回改报告、勿先改脚本迁就"。本轮是**该纪律的反向适用**——回 `Get-Item` 取字节 **113,274 B**，确认报告用十进制 KB（÷1000=113，与 GitHub/fetch 日志一致），**报告属实、脚本除数（÷1024）才是错的**。
- 遂改脚本除数并注明。区分点：**被怀疑的一方有无字节级背书**。有（113,274B）→ 报告对、修脚本；无 → 才是"改脚本迁就臆造"。
- **通用规则升级 R7-b**：体积/量纲类宣称（KB、tokens/req、ms）不属"正文数字"，应**单独走 `getsize`/字节核**，勿混进 body-token grep（否则必然假 MISS）。

## 三、盲审一致性（10 项全 agree）

| gold 项 | 值 | 5 采样一致 | 反向盲审 |
|---|---|---|---|
| completeness_gate_effective | noul 0.88 | ✓ | agree |
| phantom_dup_defect_class | "把意图写成既有行" | ✓ | agree |
| size_fact_unit_handling | score 2 | ✓ | agree |
| decision_not_silence | noul 0.85 | ✓ | agree |
| rb7_coverage | "四维齐" | ✓ | agree |
| grading_not_inflated | noul 0.82 | ✓ | agree |
| dod1_no_slot_for_best_match | "不违背(批级预算)" | ✓ | agree |
| order_sensitivity_actionability | score 2 | ✓ | agree |
| theme_convergence_strength | noul 0.83 | ✓ | agree |
| rajivkuriakose_grade_selfconsistency | noul 0.62 | ✓ | agree（低置信，见下） |

**唯一低置信自留项**：`rajivkuriakose_grade_selfconsistency` 给 0.62（留 0.38）——它是本批少数 ③=✗（无真实调用证据）却进"浅采·要点"的库，理由是"公开可跑 demo + 0.60 路由门"这一可移植点；但与同批"有②有数字却因单薄留矩阵"的库并置，"公开可跑"是否足以压过"无可移植数字"存在真张力。**处置**：不强改为高置信，登记为 FINAL 用统一 rubric（浅采·要点须含 ≥1 带对照的量化点）复核的对象。

## 四、反哺项净增（B7 → FINAL 主线）

- **新增第 4 主题**（判据顺序敏感性）：blakestone 生产实测"仅反转 criteria 顺序即致 32/200 翻转、翻转项均值 conf 0.42"→ 金标集应跑**多排列一致检验**、对高翻转且低 conf 的条目降权/加测；直接并入我们已有的反向盲审协议（把"换排列"归入"换措辞/换序"一致性门）。
- **S-B6-1 增强**："confidence≠correctness"从 B6 单批升到 **B7 内 5 库 + 跨批 pi-warden = 6 库同调**（每条挂各自源文件 token 反查），限幅：只覆盖"confidence 语义"这一窄面，不外推为"一切自报置信皆不可信"。

## 五、销账 / 挂账

- 本批**无跨批挂账可销**（不同于 B6 清了 B4/B5 三件）；B7 未占用顺路核数出行。
- B7 净新增 **4 条 FINAL 挂账**（见 `batch07.md §五`）：`vercel-labs/ai-cli` README 三 ref 全 MISS（与 vlad-terin 同批用 jsDelivr+contents 复核）；`jevsql/jev-dsl/skillranker` 等 lic=None 授权统一裁定；skillranker 113KB 膨胀抽查"深读性价比"；多语言同名 SDK（jev-go×2、typesafe-sdk-php×3、sqlite-jev 系）去重说明"冗余度作热度证据非独立设计数"。
- 结论：RB7 前置核账**在定稿前**拦下 1 完整性缺陷 + 1 单位口径缺陷，并把"POOL 行级 diff""量纲走字节核"两条固化进 B8/FINAL 模板——过程再前进一步，交付零带病发布。
