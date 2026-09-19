# b8_review — RB8 复审轮报告

日期：2026-09-19 ｜ 工件：`eval/b8_review.jsonl`（2 条 × 5 问，15,313 B）｜ 校验：`jev_eval.py --check` **✓ 2/2**（exit 0）｜ 反向盲审：**10/10 自洽**（盲重答各 gold 值与我独立判定一致，一致率 100% ≥ 85% 门槛）

## 一、本轮性质：R7-a 教训"左移"生效（首次前置自查而非脚本逼出）

延续 B4/B7"零带病发布"传统，但本轮的过程结论与 B7 相反方向：

- **B7 是靠脚本逼出**：`header ok==POOL(61)` 硬门把"Counter 自洽到 60"回溯成"缺 3 库 + 多 2 幻影"，多花一轮 diff + 改脚本才清账。
- **B8 是脚本前自查删除**：初稿我又习惯性写了 2 条幻影占位行（`owner-B-more` / `owner-A-jev-git`，与 B7 同错同族），但因 R7-a 已内化，**在跑 `_rb8_precheck.py` 前就手动列 slug 集与 `_b8_meta.txt` 做行级 diff、当场删幻影**，致脚本首跑即 `68=68 / 幻影 0 / 漏库 0 / 41 token 0 MISS / dabit3 266B getsize 核实` 一次 GATE PASS。
- **进步的正确标定（盲审 gold 只给 0.8 不给更高）**：拦截**成本**左移了（脚本逼出→源头自查），但缺陷**产生率没降**（我还是起草了幻影行）。理想的下一级是"连幻影占位行都不再起草"——登记为 FINAL 后自我约束项：**写矩阵时先落 slug 列表核对池、再写行**，把 diff 从"事后校验"再前移到"起草前"。

## 二、B8 定性判断（评测富矿批的定级与升主线）

- **28 浅采·要点 = 名实相符，非通胀**（盲审 0.78）：判据是"有值得单独记的可移植机制/数字"，本批密集出现预注册门（orderBy 6 门）、ECE/Brier（assay CLINC 0.0204 vs Banking 0.0936、sec-bench 96.5/96.2/95.1）、阈值扫描曲线（janus 0.67→80.2%）、成本-质量对照（tiershift $13.23→$7.95 同质量 4.77）、诚实负结果（behavior-study）——与 B0/B1 纯传输客户端不可同日而语。留 0.22 给"要点/非要点线仍由我主观划、缺机器可复核 rubric"（同 B7 未决项）。
- **升 FINAL 主线成立**（盲审选项"自然汇聚"0.8）：前七批校准/循环性结论全部来自"我方自读自评"，效度短板正是**自证**；B8 八库是第一方之外、**先注册判据再打分**的独立测量，等于给内部两主线补了外部锚。"仅此一批"的稀缺性恰是升主线的理由，而非"扫读批就该低权重"——采集深度 ≠ 证据效度。

## 三、盲审一致性（10 项全 agree）

| gold 项 | 值 | 5 采样一致 | 反向盲审 |
|---|---|---|---|
| phantom_self_catch_leftshift | noul 0.80 | ✓ | agree |
| r7a_what_first_pass_proves | "缺陷仍在/拦截左移" | ✓ | agree |
| zero_rerun_justification | "需真key+DoD-3已超额" | ✓ | agree |
| empty_shell_handling | noul 0.86 | ✓ | agree |
| rb8_coverage | "四维齐首跑即PASS" | ✓ | agree |
| grading_28_not_inflated | noul 0.78 | ✓ | agree |
| eval_cluster_as_mainline | "自然汇聚升主线" | ✓ | agree |
| threshold_antidote_actionability | score 2 | ✓ | agree |
| canny_drift_convergence | noul 0.70 | ✓ | agree（标注量纲边界） |
| tripwire_c3_gap_selfflag | noul 0.60 | ✓ | agree（低置信，见下） |

**两项低置信自留**：
- `tripwire_c3_gap_selfflag` 给 0.60（留 0.40）——tripwire ③=✗（自曝"尚无对真 Jev 准确率、29 mock 测试"）却凭①（免 key eval CLI）②（per-check 阈值表带 precision/recall/coverage）进"浅采·要点"，与 B7 `rajivkuriakose` **同型**："有可跑评测脚手架"能否补偿"尚无有效测量结果"存真张力。不强改高置信，与 B7 合并为 FINAL 统一 rubric（浅采·要点须含 ≥1 带对照的量化点）复核对象。
- `canny_drift_convergence` 给 0.70（留 0.30）——canny"已校准但跨 run 漂移 ~0.05"（校准≠稳定）与 nous `drift_within_round`（轮内多次采样一致性）同指"输入不变输出抖"但**量纲不同**（run 间绝对位移 vs 轮内相对抖动）。并入 drift 主题须标注此差异，勿混为一谈。

## 四、反哺项净增（B8 → FINAL 主线）

- **"阈值要测不要拍 + 边界带二次判"**（janus/every/audio-beeper/tripwire）：直治我们"**改档位不重测**"缺陷族（第 4/5 次复发）。给出可执行替代：金标集输出 **threshold–coverage–accuracy 三线表**，对 `|p−阈值|<0.10` 的条目**二次判定取均值或转人工**（等价引入"上下文不足/边界带"第四态）。
- **预注册复现协议**（assay/orderBy/legalforecastbench）：我们的 120 金标 `--compare` 应在改动**前**冻结判据与期望方向（像 jev-orderby 6 门），改后只判"过/不过门"，杜绝事后挑指标。
- **独立 checker 生态级放大**：B8 八库把 pi-warden/tax-doc"独立 checker 零共享代码"原则从单库升到生态级，支撑 DoD-2"金标不下降 + 每条附验收步骤"。

## 五、销账 / 挂账

- 本批**无跨批挂账可销**（同 B7，B8 未占顺路核数出行）。
- B8 净新增 **4 条 FINAL 挂账**（见 `batch08.md §五`）：`dabit3/jev-experiments`(266B 近空壳)、`devagrawal09/jev-code`(npm 0.0.1 占位) → FINAL 用 contents API 复核真实规模；`kuhung/understanding-jev`(正文在自建站非 README)、`usenotra/notra`(PLAN 的 300ms p50 README 未见) → 存在性通道二次取证；一批 `lic=None` 库 → FINAL 授权表统一裁定；`atomic`(64KB)/`jevlogs`(26KB)/`super-jev`(31KB)/`jev-orderby-bench`(35KB) README 偏大 → 抽查是否生成物/营销堆砌影响深读性价比。
- 结论：RB8 前置核账**首跑即 PASS**（源头自查拦下 2 幻影行），并把"缺陷产生率未降→diff 前移到起草前"记为 FINAL 后自我约束项——过程再前进一步（从"脚本逼出"到"脚本前自查"），交付零带病发布。
