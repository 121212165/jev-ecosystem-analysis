STATUS: 深采

# danrwilloughby/snifftest (Sniff Test) — 单库深度分析

> 结论先行：这是**散文质量判决链路**与我们去 AI 味目标同构度最高的库（PLAN 定其"深读首选"成立）。最大的可搬件不是它的规则，是它的**三带读数制度**：≥0.7 才成 flag、0.4–0.6 显式输出"无判定"、countable 恒 1.00——"平坦的中段数字是唯一长得像干净稿的失败"这句设计理由，直接命中我们 LLM-as-Jev 采样均值 ≈0.5 时的静默放行风险。

## 0. 基本信息
| 字段 | 值 |
|---|---|
| 仓库 | https://github.com/DanRWilloughby/snifftest |
| 类别 | B5 校验/护栏/文本质量 |
| License | MIT ✅ |
| 创建/最近 | 2026-09-17 / 09-18（14★，npm 已发布 `snifftest@0.1.0`） |
| 真实调用 Jev API | ✅ `https://api.typesafe.ai/v1/systemone`；`src/jev.ts` 自称全工具唯一开网文件；bench 表带 measured 标记与口径脚注 |
| prompt 文档占比 | README 18KB 全方法学；规则文件 `rules/default.yaml` 即文档 |

## 1. 接口形态
- 每段一次请求，**一条规则一个 Boolean（noul）**，返回每规则一个概率；无自由文本（"no general model in the loop"两处重申）
- 规则两分：**countable**（regex，本机跑，恒 1.00，成本 0）与 **judgment**（须"读而非数"的语义），marketing 标签 5 条默认停用（`--only marketing` 显式开启）
- 自定义 judgment 规则强制三件套：`what` + **`not_for`（反例边界）** + `true/false criteria`——"有 what 没 not_for 的规则会 flag 你没打算抓的东西"
- 送出内容白名单制：只发段落正文 + 规则文本；标题/表格/front matter/代码围栏永不发送

## 2. 校准与阈值策略（重点）
- **三带读数**：flag ≥0.7（可 `--threshold` 覆写）；**0.4–0.6 = "no judgment"，既不是 flag 也不是 pass**——制度化的中间带隔离；<0.4 静默
- 阈值出处坦白：0.7 是约定而非拟合值（与我们同病），但它把"未拟合"的失败模式（中段平坦）设计出来了
- `snifftest eval` **植入缺陷法**：往你自己的干净段落里每种规则植 1 个已知缺陷，三臂对照（A=无工具 / B=countable / C=+judgment），报告"抓到多少 + 在 54 段原文上误报多少"
- bench 表自曝摇摆：同 corpus 同日多跑，Jev 读到 59–64/80，"**那个摆动幅度就是读每一行数字的尺**"——把 run-to-run 方差印在主表旁边

## 3. 工程质量
- 零运行时依赖，Node 20+；`--dry-run` 离线臂完整可用（§7 实测）
- **consent 协议**：一次一目的地——"给 TypeSafe 的 yes 永远不是给别人的 yes"；yes 存 `~/.config` 不存被检目录（防提交进 repo 替所有克隆者作答）；CI 用 `SNIFFTEST_SEND=1` 单次授权不落盘
- **缓存键 = 段落哈希 + 问题原文 + 模型名**：改问法/换模型自动失效；段落正文永不写盘；14 天过期
- 退出码语义严格：0 无 flag / 1 有 flag / 2 工具不能干活 / 3 需要 yes 没拿到；fork PR 永远只跑 countable；Action 拒绝 `*_target` 事件与浮动 version
- pre-commit hook 失败时**让路**（下载失败不是关于你散文的证据），`SNIFFTEST_STRICT=1` 反转

## 4. 可移植模式清单
1. **三带隔离（→我们盲审协议）**：5 采样均值落 0.4–0.6 → 输出 `no_judgment` 状态而非按阈值判 pass/fail；quarantine 入口从"仅盲审不一致"扩到"中段均值"。验收：合成一条均值 0.5 的 gold，输出必须是"无判定"（对偶 batch03-S8 的拒评设计）
2. **植入缺陷三臂 eval**：我们的 gold 集加"往真样本植 1 个已知维度缺陷"生成器，报 caught/clean-flagged 双列（对既有 S2/S3 是数据面补全）
3. **协议版本进缓存键**：LLM-as-Jev 结果缓存键含 protocol-hash（batch03-S11 版本戳的缓存侧落地）
4. **`not_for` 强制字段**：我们每维度的问题定义补反例边界栏（"情绪密度≠标点密度"类），进 jev_eval 题面 schema
5. **方差随行表**：复测表旁印 run-to-run 摆动区间
- **反模式①**：全局常数阈值 0.7 未分题拟合——与 jevcal 路线对照，正是 batch03-S1 的动机例
- **反模式②**：单采样成判（每段每规则一问一次调用无重复）——被我们 5 采样制度碾压，勿学

## 5. 与本地 Jev 评测链路映射
- `jev_eval.py`：三带输出（§4-1）直接改判定枚举；`no_judgment` 进 quarantine 统计
- 盲审协议：中段带与 confidence<0.6 隔离带合并设计时注意——snifftest 证明"均值平"与"方差大"是两回事，前者进无判定、后者进分裂样本复审
- Score 维度锚定："档位写情形不写程度"与 `not_for` 同法——都是给判决模型可观察边界

## 6. 结论
**深采** ✅。判定与行文分离（frostney/B3）+ 三带读数 + 植入缺陷 eval 三件构成我们去 AI 味评测的骨架级参照。

## 7. 复跑记录（零 key，本批部分成功）
| 项 | 命令 | 结果 |
|---|---|---|
| 安装 | `npm install --global snifftest`（registry 通道直连可用） | ✅ v0.1.0，27s |
| countable 臂 | `snifftest check --dry-run` 合成缺陷样本 | ✅ 命中 `colon_heavy` 1.00，exit=1 与文档约定相符 |
| 二次确认 | 真 em-dash（U+2014）+ slop 词样本，`--format json` | ✅ `dash_present`+`slop_vocab` 双命中；JSON 的 judgment 块显式 `"state":"not run","reason":"--dry-run was asked for"`——无判定块本身有出处 |
| 反向验证 | hyphen(-) 不触发 dash_present | ✅ 与文档"A hyphen is fine"一致（首次未命中即此规则，属设计而非漏检） |
| judgment 臂 | 需 TYPESAFE_API_KEY | ✗ 按"跑不动记录后不强跑"终止；bench 表数字（63/80、1/54、182ms、$0.0129）留作宣称未独立复核态 |
