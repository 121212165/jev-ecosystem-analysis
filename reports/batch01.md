# batch01 — B1 开源复刻批

日期：2026-09-19 ｜ 池：21 库（inventory v3）｜ 完成：**扫读 21/21 + 深读 3（名额内换将 1 次）+ 复跑 1 → 环境受阻（已记录）**

## 一、深读名额换将说明（证据驱动）

原 I5 预排序 picks = kev / nanojev / decider。读全文后发现 `theoleecj/openjev`(SemIf) **1671★（全池最高）**、方法论最严（每条数字带 committed 溯源、明写 claim boundary），且其"零装浏览器 WebGPU demo"满足三条标准①的程度最高。nanojev 与 kev/decider 在"训练管线+游戏基准"上重叠度高。**名额改为：kev + decider + SemIf；nanojev 降浅采**。深读三档已建：`analyses/jaredpalmer__kev.md`、`analyses/mapika__decider.md`、`analyses/theoleecj__openjev.md`（全部 STATUS: 深采）。

## 二、21 库 stay/go 矩阵

| 库 | ★/Lic | ①复跑②量化③真实调用 | 判定 | 一句话情报 |
|---|---|---|---|---|
| jaredpalmer/kev | 245/Apache | ✓✓✓ | **深采** | /v1/systemone 本地 drop-in；ECE 0.065→0.031；隔离/翻转/伪造三组机理实验；kev-vs-Jev 域外 −19.1pp 自曝 |
| mapika/decider | 27/Apache | ✓✓✓ | **深采** | 94 任务 acc/NLL/Brier/ECE/AURC 全表；Score 隔离档位+归一化 fit；独立性=行级评分 0% 重排漂移 |
| theoleecj/openjev (SemIf) | **1671**/MIT | ✓✓✓(对照公开数据,自认) | **深采** | 宣称纪律范本；模型尺寸-质量梯子 0.6B 0.44→4B 0.81 vs Jev 0.883；BF16 加速的语义代价(777 中改 5-6)都量 |
| tianyucodings/nanojev | 508/MIT | ✓✓✓ | 浅采·留 | 0.6B 全分布+CE/Brier/paired-proper-reward 三臂实验；迷宫基准 NanoJev 244 次 vs Jev 2738 次到关；README 中文化；需 CUDA 活跑 |
| nandhakishorm/laya | 379/Apache | ✓✓✓ | 浅采·留 | 非自回归 35ms；`pip install laya`；**laya-multilingual 322M mmBERT 变体=中文 state 刚需的现成答案**，B1 内最优先补验对象 |
| heman10x-ngu/verdict-open-jev | /— | △✓△ | 浅采·留 | 151M ModernBERT+RLCD+Brier loss，WebGPU playground——小尺寸上限参照 |
| r-ms/mini-jev | /— | ✓✓✓ | **浅采·要点** | 冻结 Qwen3-4B+xgrammar"读字母不写字母"：6750 配对观测证明读字母不损精度且 4× 快；**直接反驳 LLM-as-Jev 让模型写概率数的做法**，与官方"写数字"路线构成张力——我们下轮盲审协议要测这条 |
| genai-craft/openvons | /— | ✓✓✓ | 浅采·留 | 校准工具箱（temperature/isotonic/**带 none 选项的校准**）+ECE/Brier/NLL 指标；日语语音场景 |
| zhihz/openjev | 9/NOASSERTION | ✓△✓ | 浅采·留 | 双语概率问答（zh README）；坦承无校准宣称——中文态表现的可对照样本 |
| ekzhang/openjev-sglang | /— | ✗✓✗ | 留矩阵 | prefill-only 服务化，自述"非校准估计"；35B-A3B 与我们规模不符 |
| featherless-ai/simple-jev | /无声明 | ✓△△ | 留矩阵 | logits→typed decisions 无需服务端；demo 模型 26B 级过重；License 缺失只记模式 |
| kshetrajna12/reflex | /— | ✓△✓ | 留矩阵 | 浏览器 WebGPU 650MB 0.8B 引擎；shared-state+隔离分支与 kev 同构 |
| kikoncuo/jevfire | /MIT | ✓✓△ | 留矩阵 | vLLM CUDA + 浏览器 Mario，71ms/worker 实测；用 RLCD 公开权重 |
| razorback16/openjev | 51/Apache | ✓△✓ | 留矩阵 | DiffusionGemma 26B vLLM；附带 api.codiv.ai 引流（100M free tokens）——营销味，降权 |
| bnsd55/jevmlx | /CI 有 | ✓△△ | 留矩阵 | Apple MLX 专属，本机 Windows 无价值 |
| ghalebdweikat/winnow | /— | ✓✓✓ | 移 B5 候选 | 实为 Claude Code 上下文裁判（guardrail 形态），归 B5 更当；含 `WINNOW_JUDGE=adapter` 无 key 兜底设计可记 |
| jonesmelton/verdict | /— | ✓✗✗ | 丢弃 | OCaml SDK，与 Python 链路无关 |
| asfarsadewa/human-compiler | /— | ✓✗✗ | 丢弃 | npm 玩具（被动攻击指数），无校准无调用证据 |
| us/jev-local | 0/**无License** | ✓✓△ | 存疑·浅采 | 4 提交/0★/单日；但 leaderboard 有 Wilson CI + n=1316 校准 0.83 宣称——数值无第三方佐证，只记模式不引数值 |
| alexwortega/openjev | /— | — 无 GH 顶层 README | 挂起 | HF-only（hf.co **直连 200 可用**，旧结论修正）；下轮拉 HF model card |
| drinkmoonshine/parallel-constrained-decoding | /— | — 同上 | 挂起 | 其价值在 yibie 引用的 0.82/0.70 校准差数据点，仓库本体低优先 |

**统计**：深采 3 ｜ 浅采 6 ｜ 留矩阵 8 ｜ 移批 1（winnow→B5）｜ 丢弃 2 ｜ 存疑 1 ｜ 挂起 2。

## 三、本地复跑记录（受阻，DoD 未完成项 #1）

选定 kev（唯一 CPU 理论可行 + /v1/systemone 对齐我们 adapter 链路）。环境实测：
- torch 2.10.0+**cpu**（无 CUDA/MPS）、transformers ✅、**peft ✗**、磁盘余 84.8GB
- **huggingface.co 直连 200 可用**（修正 B0 的"HF 通道不可靠"认知；hf-mirror 反而不通）
- 失败路径全记录：① git clone 经 gh-proxy → sideband early EOF；② codeload tarball 双代理 → 240s 超时；③ git 直连 github.com → 90s 超时；④ sparse+blob:none → promisor blob 拉取失败（checkout 空）；⑤ API trees 端点 → 超时/403
- 结论：**小文件（README×21、API repo 元数据）通道稳定，大仓库传输通道本机当前不可用**。复跑改期条件：网络窗口稳定 或 换有 GPU+网机房
- 复跑改期不阻塞：深读三档的复测表已按"宣称值+出处采信等级"填写（kev/decider/SemIf 均有 raw json 佐证可后验）

## 四、I7 预警名单第二维证据

| owner | 库数 | 提交时间分布（last-100） | 判定 |
|---|---|---|---|
| typesafe-ai | 4-6 | 官方 | 豁免（B0 已定） |
| jaredpalmer | 1 | 2 天 43 提交，渐进迭代 | **正当**（kev 系真工作） |
| mapika | 1 | 3 天 38 提交，v1→v9 演进 | 正当 |
| theoleecj | 1 | 4 天活跃+issue 往来 | 正当 |
| **owner-A** | 5 | 未抽查（其 5 库全在 B4/B7/B8） | 待 B4/B7 扫读时按同法查 |
| **owner-B** | 5 | 未抽查（列表主=本人，利益冲突在 B0 已记） | 待查 |
| kitze | 3 | 独立小工具向 | 倾向误伤，维持"正当多产" |
| **us** (jev-local) | 1 | 单日 4 提交、0★、无 License、"us"org 名可疑 | **新增预警**（B8 复分类时定夺） |

## 五、本批可移植要点（并入 FINAL 矩阵的候选行）

1. **`JEV_SAMPLES=5` 均值路线应加对照**：kev/decider 证明"能读 logits 就读一遍全分布"；mini-jev 的 6750 配对观测证明"读字母 ≥ 写字母且 4× 快"——我们 LLM-as-Jev 让模型**写出**概率数值的协议处在两条证据的反面，下轮盲审要加"字母读数 vs 数字写作"一致率对照（零成本，只改题目模板）
2. **AURC/selective accuracy 入评分侧**（decider）：三档线（自动/复核/隔离）的定阈从拍脑袋变成曲线上选点
3. **换序翻转率成显式指标**（kev 7.4% 参照值）
4. **复测表四列制 + claim boundary 句式**（SemIf）：批次报告模板下批起执行
5. **laya-multilingual**：中文 state 复刻的现成权重，等网络窗口与 kev 一起复跑

## 六、产物索引

- 深读档 ×3：`analyses/{jaredpalmer__kev,mapika__decider,theoleecj__openjev}.md`
- README 快照：`_b1/*.md`（19 份，全部 21 库中 19 份顶层 README）
- 脚本：`b1_fetch.py`（幂等拉取+双代理回退）、`b1_scan.py`（信号提取）、`b1_meta.py`/`b1_meta_html.py`（元数据）
- 挂账：kev 复跑（环境）；alexwortega/drinkmoonshine HF 侧补拉；~~winnow 移 B5~~ ✅已入 inventory v4（B1=20/B5=19）；us/jev-local 存疑待 B8
