# b6_review — RB6 复审轮报告

日期：2026-09-19 ｜ 工件：`eval/b6_review.jsonl`（2 条 × 5 问，11,992 B）｜ 校验：`jev_eval.py --check` **✓ 2/2**（exit 0）｜ 反向盲审：**10/10 自洽**（盲重答各 gold 值与我独立判定一致，一致率 100% ≥ 85% 门槛）

## 一、复审轮抓到的可执行跟进（本轮非零发现）

与 B4"复审零新缺陷（因前置核账已拦）"不同，RB6 靠 `piwarden_reconcile`（noul 0.84，留 0.16 给"挂账项本身应同步标已清"）**逼出一条销账纪律**：

- B6 顺路清掉了三条跨批挂账，但 **B4 §7 / B5 §七 的对应复选框仍是 `[ ]`** ——若不同步更新，FINAL 阶段 grep `[ ]` 会把这些"已在 B6 核实"的项重新捞成未办，造成重复劳动 + 状态失真。
- 处置：本轮把 B4/B5 三件挂账复选框回勾为 `[x]` 并注"已清 by B6 见 batch06 §三"。
- 升为通用规则：**顺路核数完成后，核销动作要同时落到"来源批次的挂账行"，不只记在"执行批次"**。挂账是双向指针，销一项要两头摘。

## 二、各题金标与盲审

### RB6-A-01 · 工件一致性与核账
| 题 | 原语 | 金标 | 置信 | 盲审 |
|---|---|---|---|---|
| pre_write_catch_effective | noul | 0.86 | 0.82 | agree |
| attribution_class | choice | 跨语义张冠李戴（数真·绑错论断） | 0.80 | agree |
| verify_vs_assert | score | 2（验提交物+逐字核对） | 0.76 | agree |
| independent_count_value | noul | 0.83 | 0.80 | agree |
| counter_backfill | choice | Counter+24 token HIT+头条防错，覆盖充分 | 0.85 | agree |

### RB6-B-01 · 复跑与深读质量
| 题 | 原语 | 金标 | 置信 | 盲审 |
|---|---|---|---|---|
| offline_arm_partial_honesty | noul | 0.90 | 0.88 | agree |
| promotion_topstar_not_violation | choice | 不违反（星数既非准入亦非排除证） | 0.82 | agree |
| star_velocity_grade | score | 1（判合法但标注+挂 FINAL 复查） | 0.72 | agree |
| piwarden_reconcile | noul | 0.84（含销账跟进） | 0.80 | agree |
| circularity_mainline | noul | 0.80（留 0.2 防过度归并） | 0.76 | agree |

## 三、复审自曝的两处残余风险（带入 FINAL，非本批可闭）

1. **circularity_mainline = 0.80（最低分题）**：godsboy 改题污染 / zhuyansen judge 循环 / pi-warden 独立 checker 三者是"自评自证循环性"的**不同侧面**，合成一条主线有**过度归并**、丢掉各自独特可操作点的风险。FINAL 落笔时须保留三条各自的可执行项，只在总标题下并列、不强行并为一条。
2. **star_velocity_grade = 1（非 2）**：tax-doc 已 clone 验真（261 表 + src + 测试），代码非空壳；但 <1 天 193★ / 2 commit 的星速-提交速背离仍属 I7 统计异常，判"合法但待核"而非"直接成熟"——FINAL 须复查是否 TypeSafe 官方 showcase 助推（关系到"热度不折名额"尺度的跨批一致性表述）。

## 四、流程自评

- **写前拦截 vs 事后更正**：本批头条数字误写（60/80）在**写矩阵前**靠逐库 grep 拦下，前置核账脚本再确认 0 MISS——较 B4（Counter 回填抓归因错）、B5（定稿后人工复审才抓）又前移一道。但 `pre_write_catch_effective` 仅 0.86 非满分：**它仍依赖"人主动去 grep 精确行"**，尚未升为脚本强制门禁（脚本只能在写后验 token 归属，无法强制作者写前去源文件核对语义）。这一"人力前置 vs 机器门禁"的缺口记入 FINAL 方法论段。
- **幻影写处置延续**：本批 4 个辅助脚本 + 报告均现"save failed 但 Get-Item 验盘完整"，一律先验再续、未误信失败重写（与 B4 同尺，未复发重复写缺陷）。
