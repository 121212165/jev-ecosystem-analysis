# b4_review — RB4 复审轮（对 batch04.md 及 B4 工件的 LLM-as-Jev 复审）

日期：2026-09-19 ｜ 数据：`eval/b4_review.jsonl`（2 条 × 5 问，`jev_eval.py --check` ✓，盲审一致 10/10）
**核心结论：本轮事后复审零新发现缺陷——因为 `_rb4_precheck.py` 已在定稿前拦掉 3 处。这是 B0 起计数漂移四连发之后，该缺陷族第一次"发布前"而非"发布后"被清零，验证了 B5 §三教训（脚本是文档的上游）落地生效。**

## 一、前置核账在定稿前拦住的 3 处（本轮不计入"事后缺陷"，但记为流程胜利）

| # | 初稿缺陷 | 真值 | 发现阶段 |
|---|---|---|---|
| P1 | 0.55 归给 wakegate | 0.55 是 moritzkremb/jev-voice-browser；wakegate 真值 0.30/0.20 | `_rb4_precheck.py` token grep MISS → 定稿前修 |
| P2 | minReductionRatio 归给 tamaratran | 该变量名不在 tamaratran（用 keepThreshold 0.5 + reductionRatio<0.25）；同名变体在他池 leonaaardob | 同上，probe 证实后修 |
| P3 | 核账行"23 含此 1" | Counter 把"存疑"单列，23 不含该 1（1+5+23+1=30） | 写核账行时自查修 |

**缺陷分类（复审题 attribution_error_class gold=选项1，0.82）**：P1/P2 是"跨库张冠李戴"——数字真实存在于别的库，扫读多库时行串位。这类错**通用计数脚本抓不到**（汇总数没错），只有"数字 token → 应属源文件"的定向回溯能抓，正是 `_rb4_precheck.py` 的 checks 段在做的事。

## 二、事后复审的结果（RB4-A/B）

**RB4-A（工件一致性）**：`script_gate_effective` = 0.90——同类归因错 B5 靠定稿后人工复审发现（第四复发），B4 被脚本在写头部前拦下，机制从"事后纠错"前移到"事前门禁"；`precheck_covers_matrix` = 选项1（0.84）——一次跑完"回填计数 + 23 token 全 HIT + 触发 2 处修"三件事；`phantom_write_handling` = 2 档（0.76）——每次写报失败即验盘再继续，本批零因误信失败而重复写。

**RB4-B（复跑与深读质量）**：`promotion_over_stars` = 0.94（本批最高置信）——json-render 16,656★ 的 Jev 仅 compose 一笔，pi-warden 70★ 三标准全✓且唯一可零 key 复跑，热度与质价完全倒挂，晋级正是打破倒挂；`stub_rerun_legitimacy` = 选项1（0.80）——先证 pi-tui 仅被 widget 顶层 1 渲染函数使用、stub 不进 evaluateAction 路径，故是干净的依赖裁剪而非篡改；`partial_rerun_honesty` = 2 档（0.72）——既有臂级限定又有"成功级=snifftest 单臂"横向对标，双重限定是最严写法。

## 三、需带进 FINAL 的两条

1. **`i7_starvelocity_verdict` = 1 档弱多数（0.62）**："星速异常≠脚手架"本批成立**仅因有镜像库互证这一强证据**；作为一般规律不可推广——条件不满足时须回到默认存疑。FINAL 的 I7 规则应补此边界。
2. **归因错（张冠李戴）是计数漂移之外的第二缺陷族**：前者靠处置列 Counter 回填抓，后者靠"token→应属文件"定向 grep 抓，两者都要在**定稿前**跑。B6–B8 沿用 `_rbN_precheck.py` 模板（含 checks 段）。

## 四、本轮未复现的历史缺陷（正面确认）

- 计数漂移：无（头部数字=Counter 实产出，非手写）
- 预防性勾选 `[x]`：无（§七 RB4 行在产物落地后才翻勾，见下）
- legend 程度词：无（本轮 legend 全用情形描述，`--check` 一次通过未触发 lint）
