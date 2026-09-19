# batch05 — B5 校验/护栏/文本质量批（去 AI 味提级批）

日期：2026-09-19 ｜ 池：**18 库**（v7）｜ 状态：**完成**（遗留见 §七）
**深采 2 · 浅采·要点 5 · 留矩阵 9 · 留矩阵·存疑 2 · 移批 0 · 丢弃 0**（合计 18；首版手写"浅6留10"被核账脚本打脸——第四复发，见 b5_review R1）

## 一、深读名额说明

- 预排序头名 `devagrawal09/jev-review` **293★（全批最高）**：README 仅 3.3KB，stage-gate 形态与 frostney（B3 深读）重叠，无独有量化面 → 降级留矩阵（RB5 审出：首版误写"浅采·要点"，以矩阵处置列为准）。热度不折进名额（B1/B2 同尺）。
- **入选 = snifftest + abide**：snifftest 是 PLAN 点名"深读首选"且全池唯一零 key 臂可复跑的文本判定库（§三）；abide 的独立确认召回统计法 + rubric 溯源行号与 snifftest 互补（读数制度 vs 审计修订制度），无一面重叠。
- 深读档：`analyses/danrwilloughby__snifftest.md`、`analyses/coldteadotai__abide.md`

## 二、18 库 stay/go 矩阵

| 库（★/lic） | ①复跑②量化③调用 | 处置 | 一句话依据 |
|---|---|---|---|
| danrwilloughby/snifftest (14/MIT) | ✓✓✓ | **深采** | 三带读数（0.4–0.6=显式无判定）；植入缺陷三臂 eval；零 key countable 臂本地复跑成功（§三）；缓存键含模型名 |
| coldteadotai/abide (92/MIT) | ✗✓✓ | **深采** | 独立确认召回法（flag 39 确认 10 并排印）；死规则 calibrate 自动禁用；漏检进 events.jsonl 不静默 |
| ghalebdweikat/winnow (17/MIT) | △✓✓ | 浅采·要点 | **ECE 与 AUC 必须并报**（"报 base rate 的裁判 ECE 很漂亮且什么都能藏"）；`--fake` 关键词裁判走真管线；regret=校准曲线；shadow 模式 |
| shiftynick/jev-axi (13/MIT) | △✓✓ | 浅采·要点 | 负结果自曝：6 次/条件测不出方向（均值中位数符号相反）"用我们做判决别代替读码"；skills-do-not-get-used 附录；本机路由（routine 命令本地放行零成本） |
| doeixd/jev-pref (2/MIT) | ✗✓✓ | 浅采·要点 | `tune --sweep`：**冻结一次 live 答案，0.5–0.9 离线扫阈值**（API 成本 1 次、阈值实验 N 次）；DIRECT/NEEDS SHAPING/NOT FOR JEV 题面成型三分法 |
| leepokai/jev-guard (8/MIT) | ✗✓✓ | 浅采·要点 | claimed vs measured 并排表（官方 150ms vs 实测 0.75s 含 TLS）——宣称-实测分栏范本 |
| choxos/jev-reviewer (4/MIT) | ✗✓✓ | 浅采·要点 | 双判一致率进正文（"212 of 240 agree, 88%"）+ 分歧 Keep mine/Use theirs 人工裁决回路 |
| devagrawal09/jev-review (293/MIT) | ✗✓△ | 留矩阵 | 全批最高星但文档最薄：stage-gate+反例+决策边界句，形态与 frostney 重叠 |
| bitnovus/jev-spam-eval (0/MIT) | ✗✓✓ | 留矩阵 | **zero-shot vs supervised 对照**：Jev 98.64%（5,733 封）对 TF-IDF+LR（4,600 标注训练）——"零样本离训练分类器多远"的问法范本 |
| luantak/is-malicious (8/无声明) | ✗✓✓ | 留矩阵 | **noul 线上无独立 confidence 字段，报告端自行合成**——与我们 LLM-as-Jev 合成置信度同构，wire 层事实值得记；只读不抄（无 Lic） |
| niazmorshed2007/jev-review (132/MIT) | ✗✓△ | 留矩阵 | 1–10 分+0–1 置信独立打；"correctness 永远压过提分，高分不洗白投机架构"=反 halo 条款同款 |
| hyunjunjeon/jev-judgment (2/MIT) | ✗✓△ | 留矩阵 | "Jev 置信是关于语境的证据，不是行动许可"——一句话版权限边界 |
| kelbie/hunch (0/无声明) | ✗✓△ | 留矩阵 | 题面强制选原语（noul/choice/score 三选一）+`configure` 证伪有效；`doctor` 命令族 |
| owner-A/jev-git (1/MIT) | ✗✓✗ | 留矩阵·存疑 | "筛 AI hallucinations <100ms"无测无出处；HTML 注释塞 SEO 关键词；owner 在预警名单（B3 §七已判） |
| owner-A/jev-seo (7/无声明) | ✗△△ | 留矩阵·存疑 | 同上 owner；"scored deterministically without hallucination"是宣称非测量 |
| raihankhan-rk/diffjury (3/无声明) | ✗✓△ | 留矩阵 | PR 风险路由一跳，无评测面 |
| devanshbatham/commit-miner (23/无声明) | ✗✓△ | 留矩阵 | Rust CLI 分类提交，无数字 |
| useopencompany/opencompany (6/MIT) | ✗△△ | 留矩阵 | Jev 走 workspace 审批一景，无独立可借件 |

**统计核账**（脚本解析处置列）：深采 2 · 浅采·要点 5 · 留矩阵 9 · 留矩阵·存疑 2 = **18** ✓（devagrawal09 按实际处置"留矩阵"计，不折进浅采档）

## 三、复跑实录：snifftest 零 key 臂（本战役第二次无 key 复跑，countable 臂部分成功）

| 项 | 结果 |
|---|---|
| 安装 | `npm install --global snifftest` → v0.1.0/27s（**npm registry 通道直连可用**，新通道事实：GitHub 受阻时 npm 是 Python 库之外的第二条路） |
| 冒烟 1 | 合成缺陷稿 `check --dry-run`：`colon_heavy 1.00` 命中，exit=1 与文档退出码表相符 |
| 冒烟 2 | 真 em-dash + slop 词：`dash_present`+`slop_vocab` 双命中；`--format json` 的 judgment 块显式 `"state":"not run"`——无判定有出处 |
| 反向验证 | hyphen 不触发 dash（文档"A hyphen is fine"）——首跑"未命中"经核对是设计而非漏检 |
| judgment 臂 | 需 key，按"跑不动记录后不强跑"终止；bench 表（63/80、1/54、182ms）留未复核态 |

abide/jev-axi/winnow 均无零 key 臂（核心回路含 API）；abide 的 headline 数据 committed 于 `benchmarks/replay/`，拉取核数挂 B6 顺路。

## 四、去 AI 味链路直接反哺（本批 PLAN 特别条款）

B5 = "去 AI 味相关提级深读"。对 `本地网文创作系统（独立私有仓，未随本仓发布）` 的 AI 味检测链路（ONNX detector + 我们评测层）：

1. **三带读数（snifftest）→ jev_eval 判定枚举加 `no_judgment`**：5 采样均值落 0.4–0.6 → 显式"无判定"，禁止静默 pass/fail。DoD-2：合成均值 0.5 的 gold，输出必须是无判定态。
2. **植入缺陷三臂 eval（snifftest）→ 我们的维度题体检**：往真样本按维度植已知缺陷，报 caught/clean-flagged 双列——batch03-S6 冻结之后、上线之前的中间站。DoD-2：每维 8 植入样本 + 54 干净样本跑通出双列。
3. **独立确认召回表（abide）→ 复测表格式**：自动 flag 数与独立确认数并排印，两数不齐不上 banner。
4. **死规则体检（abide calibrate）→ 题集发火率监控**：长期恒 ~0.4 不触发的维度题自动点名禁用。DoD-2：注入永不发火合成题必须被点名。
5. **ECE+AUC 并报（winnow）→ 我们的校准汇报纪律**：单报 ECE 会被"恒报 base rate"骗过；有 gold 标签后双指标并报。
6. **`tune --sweep` 先冻后扫（jev-pref）→ 阈值实验零增本**：live 答案一次冻结（=S6），阈值 0.5–0.9 离线重打分——S1 拟合的成本补丁。
7. **反例边界字段（snifftest `not_for`）→ 维度题面 schema**：每题必带"不抓什么"栏。
8. **不搬**：snifftest 全局常数 0.7（未分题拟合）、单采样成判（对抗我们 5 采样制度）。

## 五、I7 抽查（本批新触 owner）

owner-A 第 2 次触发（jev-git/jev-seo）：两库宣称均无测量出处，README 含 SEO 关键词注释——**降级令扩至其全部 5 库**；其数字/模式引用一律需第三方佐证。

## 六、协议执行记录

- 戒条①名→源回溯：矩阵所有星数/Lic 逐行对 §b2_meta 输出；"98.64%、39/10、212/240"等数字逐条对 `_b5/*.md` 原文 grep 命中后才写入
- 戒条②负结果双通道：jev-code 缺失用 inventory grep 证实（落 B8 行）；winnow 首查 NOFILE 系文件名错（双通道暴露）
- 戒条③移批先核定义：winnow 留在 B5（PLAN B5 定义"校验/护栏"+B1 已预告"归 B5 更当"）；无其他移批候选
- 教训"计数脚本生成"：**本轮违例实录**——头部统计仍是先手写后声称"从解析抄写"，被 RB5 前置核账脚本抓出（浅6留10 → 实为浅5留9+存疑2），规则本身有效但执行序错（应先跑脚本再写文档）

## 七、遗留与挂账

- [x] snifftest 零 key 复跑（§三）
- [x] RB5 复审轮已闭环：`eval/b5_review.jsonl`（2×5 问，`--check` ✓，盲审 10/10）+ `reports/b5_review.md`；审出 R1 计数漂移四复发/R2 预防性勾选/R3 用词冲突/R4 legend 程度词被 lint 抓，均已修
- [x] ~~abide `benchmarks/replay/` tarball 拉取核数（39/10、15/11 两组）~~ → **已清 by B6**（results-2026-09-18.json 9,243B 实存；headline 39 flagged→10 confirmed(26%) / 15→11(73%) 逐字命中，见 batch06 §三）
- [x] ~~zhuyansen `jse robustness` 无 key 重打分~~ → **已清 by B6**（results/robustness.md+per_query.csv+src/jse/robustness.py 齐备；换 judge 重打分已落地，真实调用证据 jev-1.13-20260917/$0.066，见 batch06 §三与 S-B6-1）
- [ ] snifftest judgment 臂数字（63/80、1/54）未独立复核——引用带"自测已发布"级
- [ ] choxos/jev-reviewer（37KB 长文档）浅采是否低估：留 FINAL 晋级扫描复看
