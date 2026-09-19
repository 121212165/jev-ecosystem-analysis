# batch03 — B3 评分/排序/裁判批（jev_eval.py 反哺批）

日期：2026-09-19 ｜ 池：**21 库**（v6 剔 2 条 `tests/*` 垃圾行，v7 再剔 1 条 B5 假阳性——翻案实录见 §五）｜ 状态：**完成**（遗留见 §八）
**深采 2 · 浅采(含要点) 7 · 留矩阵 12 · 移批 0 · 丢弃 0**（移批 0 有判据：21 库全部落在 PLAN B3 定义"评分/排序/裁判"内，逐一对照过 B4/B6 节原文，无一条更符合——戒条③"移批先核批次定义"本轮零触发）

## 一、深读名额说明（三条准入标准实判）

预排序呼声最高的是两颗高星：chetaslua/jevmeter 60★、vinilana/jev-eval-agent 86★。实判：

- **jevmeter ✗标准①**：全链路需 TYPESAFE_API_KEY + whisper + ffmpeg + 视频素材，无 key 一键复跑不成立。降浅采（要点照记 §六-5）。
- **vinilana ✗标准①**：真跑同样双 key；`JEV_STUB=1` mock 冒烟只验管线不验宣称数字。降浅采（要点 §六-6）。
- **入选 = abhixhek/jevcal + zhuyansen/jev-search-rerank-eval**：前者是全池唯一**本网络无 key 完整复跑成功**的库（demo 数字逐位复现 + 测试全绿，§三）且正面回答"阈值抄用不可靠"痛点；后者给出裁判循环性**可测量方案**（三标签列），与我们 LLM-as-Jev 方法的固有偏差直接同构。
- 深读档：`analyses/abhixhek__jevcal.md`、`analyses/zhuyansen__jev-search-rerank-eval.md`

## 二、21 库 stay/go 矩阵

| 库（★/lic） | ①复跑②量化③调用 | 处置 | 一句话依据 |
|---|---|---|---|
| abhixhek/jevcal (5/MIT) | ✓✓✓ | **深采** | 阈值从自有数据拟合+半切留出+保守下界；demo/测试无 key 全复跑成功（本战役首例） |
| zhuyansen/jev-search-rerank-eval (4/MIT) | △✓✓ | **深采** | 裁判循环性三标签列（llm_only 保守列 −0.028 揭示偏差方向）；paired bootstrap ΔCI；冻结标签 |
| tky-27/jevslop (0/MIT) | △✓✓ | 浅采·要点 | 八原子 Score + overall 是 Jev 直接 choice **非轴均值**；"not authorship probability" 宣称边界声明 |
| marissafamularo/citation-verifier (0/MIT) | △✓✓ | 浅采·要点 | 三级流水线：代码读取→Claude 定位并**证明引文存在否则丢弃**→Jev 评分→人终裁；自注"阈值未经验证" |
| frostney/clean-code-review (4/MIT) | △✓✓ | 浅采·要点 | 判定与行文分离：34 布尔/文件一次调用 ~0.5s，Luna 只从 findings 写评语；docs read-not-judged；$0.02/24 文件 PR |
| komikat/jev-bfs (0/MIT) | ✗✓✓ | 浅采·留 | 排序类 state 压缩范本：只发 link title+URL 不发正文，≤128 候选/请求；"不宣称最短性"边界句 |
| superagents-lab/jev-search (155/MIT) | ✗✓✓ | 浅采·留 | B3 星数第二；同属排序提问 state 压缩（PLAN 与 jev-bfs 并名） |
| vinilana/jev-eval-agent (86/—) | △✓✓ | 浅采·要点 | done-gate：noul(done)<0.5 时**拦截抢答的 respond_to_user、改露次优工具**；相似名干扰工具集（100 mock tools）；committed eval-results 版本化 |
| chetaslua/jevmeter (60/MIT) | ✗✓✓ | 浅采·要点 | flag 阈值=该题实测分布 98 分位（floor 0.5）非拍脑袋；200 held-out 句含近似陷阱样本；"同句问题人人高分→只互比不比零"读数纪律 |
| iammrduncan/typesafe-ai-benchmark (32/MIT) | △✓✓ | 留矩阵 | latency/cost p50–p99 口径表可借；评测对象是通用 benchmark 非写作态 |
| mahlernim/jev-korean-benchmark (5/—) | △✓✓ | 留矩阵 | **乱序翻转 13–14% vs 重复翻转 1–2% 基线**——我们 ≥85% 自一致阈值的量化背景板；"翻译指令不买到任何东西"（韩≈英 1–2pt） |
| anessbelbati/jev-rerank-bench (1/MIT) | ✗✓✓ | 留矩阵 | Jev 0.692 vs Cohere 0.691——**未建立胜者**就如实发表，负结果写法范本 |
| anisselbd/jev-phishing-bench (0/—) | ✗✓✓ | 留矩阵 | 负结果：Jev 62.6% vs Haiku 81.3（带 CI）；锚定模型版本 jev-1.13.0 |
| vclic/smoking-extraction-benchmark (0/—) | ✗✓✓ | 留矩阵 | 负结果：Jev 92.4% vs OpenAI structured 98.7%；自曝 moving alias 漂移风险（实测 jev-1.13.0） |
| owner-B/jev-benchmarks (9/Apache) | ✗✓✓ | 留矩阵 | ≤5% 误差下覆盖率表；seed+preregistered protocol tag+SHA-256 清单（I7 抽查见 §七） |
| shogo-nfrealmusic/jev-eval (0/—) | ✗✓✓ | 留矩阵 | Jev vs gpt-4o-mini vs Sonnet 同条件串行对照；warm-up 丢弃、pilot 子集**见结果前机械固定**（subsets.ts 注释自证） |
| hegargarcia/jev-playground (0/无声明) | ✗✓△ | 留矩阵 | 一致性=同 state 重复评测的选项漂移（对照我们自一致协议）；缺失值显 unavailable 不推断；无 License 行 |
| 4esv/jev-eval (0/—) | ✗✓✓ | 留矩阵 | 300 项/任务小样本网格；版本锚 jev-1.13.0 |
| jgridifier/jev-research-eval (1/NOASSERTION) | ✗✓△ | 留矩阵 | 在固定 pin 上克隆 jev-ultrafast（B2 深读库的下游样本，佐证 ultrafast 模式被复用） |
| tokentrim/jev-agent-failure-benchmark (1/Apache) | ✗✓✓ | 留矩阵 | 6,257 traces 对比表；"beats GPT-5.4 every axis"式营销比较句需按宣称纪律打折 |
| owner-A/jev-scout (1/MIT) | △✗△ | 留矩阵·存疑 | owner 5 库同日分布（§七），宣称抽查未见量化支撑 |

**统计核账**（独立解析处置列核过）：深采 2 + 浅采·要点 5（jevslop/citation-verifier/frostney/vinilana/jevmeter）+ 浅采·留 2（jev-bfs/jev-search）+ 留矩阵 11 + 留矩阵·存疑 1（合并计入头部“12”档）= **21** ✓；丢弃 0（B3 无玩具库，最低质也带可借模式）。

## 三、复跑实录：jevcal——本战役首次无 key 完整成功

| 项 | 命令 | 结果 |
|---|---|---|
| 源码获取 | codeload tarball via gh-proxy（765KB/<120s） | ✅ pip git+https 直连与代理均死，小库 tarball 可行——**B1"批量传输全死"结论修正为体积相关** |
| demo 复现 | `python -m jevcal.cli demo` | ✅ README 数字**逐位复现**：is_urgent 0.994 / 21.2% / 100.0% / 94.5% / 3.5%；escalate 85.4%；$1.930 vs $2.25 |
| 测试套件 | `pytest`（需 `PYTHONPATH=<repo>/src`） | ✅ 24 passed（首轮 3 collection error=未安装+src 布局，非代码缺陷） |
| 产物落盘 | `jevcal-main/` + demo 输出 `jevcal-demo/` | ✅ 锁文件与报告工件齐 |

zhuyansen 库本体未复跑（数据文件体积未验，且其 `jse robustness` 零 API 重打分列为下轮候选——tarball 通道已开，1MB 级以下都变得可行）。

## 四、核心产出：jev_eval.py 改造建议清单（每条附 DoD-2 验收步骤）

现状锚点：`src/eval/jev_eval.py`（本地网文创作系统（独立私有仓，未随本仓发布））已有 `--check --files` 静态校验、5 采样、逆序盲审、≥85% 自一致阈值。以下按优先级：

| # | 建议 | 源（证据） | DoD-2 验收步骤 |
|---|---|---|---|
| S1 | **题级阈值拟合**：`fit_thresholds.py` 从自有 gold 集按题型拟合置信度阈值→目标准确率，半切留出验证，输出带 CI 的锁文件（沿用 jevcal 的 `--conservative` 取 95% 下界口径） | jevcal：拟合→留出→lock 全链路，demo 已本地复现 | 用合成数据（构造已知最优阈值的分布）跑拟合，**留出集准确率落在目标 ±2pp 内**；阈值不再从别处抄 |
| S2 | **gold lint 前置**：`--check` 增校验：概率和≈1±0.02、samples=5、blind=agree、rationale 非空、note 必含"自写合成样本"、qid 唯一、primitive ∈ {noul,choice,score} | jevcal lint（措辞检查）+ zhuyansen 冻结+哈希标签 | 各构造 1 处违规的坏副本，**7 类错误全部非零退出并指认到行**；全绿 gold 退出 0 |
| S3 | **confident-and-wrong 优先表**：check 输出新增小节——高置信但 gold 判错的条目按置信度降序，作为人工复审第一清单 | jevcal README 明言"confident and wrong 清单优先处理" | 注入 1 条合成"高置信判错"条目，**必须出现在该表首行**；无则整节省略且打印"无" |
| S4 | **口径声明字段**：每处置信度数字强制标注口径（top_prob / margin / entropy / API-confidence 四选），报告模板内嵌口径句 | jevcal `--measure auto` 四口径实测对比表 | 跑一次全量：报告每个置信度数字**旁都有口径标签**；漏标即 lint 失败 |
| S5 | **保守对照列（去循环性）**：LLM-as-Jev 出分之外加 `llm_only` 保守列（不经 Jev 修正的同料直评），两列差值即循环性度量，报告并排展示 | zhuyansen 三标签列实测：jev_only +0.053 / final +0.012 / llm_only −0.028——偏差方向肉眼可见 | 造 20 条含已知偏好错的合成 gold，**jev 列与保守列差值符号与注入方向一致** |
| S6 | **聚合纪律**：中间量不四舍五入（末位再舍）；gold 集先冻结（带日期+SHA-256 进报告头）再打分 | zhuyansen：未取整均值融合 + "freeze labels before scoring" | 打乱 gold 样本输入顺序重跑，**汇总统计逐位不变**；报告头含哈希可验 |
| S7 | **overall≠轴均值**：多维评分的总分要么显式声明"=各轴算术平均"，要么单设一问让模型直接给整体 choice | jevslop：overall 是 Jev 直接 choice 非加权平均，README 三处重申 | 取 20 篇真实样本两法对比，**一致率 <90% 则强制采用 direct-choice 并在报告注明** |
| S8 | **存在性预检入 state 流程**：评引用/事实前，先核验"该引文真的存在于给定语料"，不存在→拒评并标 error，而非给低分 | citation-verifier：Claude 证明引文存在否则丢弃（比"评低分"干净一个量级） | 在 state 注入 1 条虚构引文，**输出必须是"存在性校验失败，拒评"而非任何分数** |
| S9 | **分位数 flag 阈值**：异常标记（如"这句在吹"）的触发阈值取该题实测分布 98 分位（floor 0.5），非全局常数 | jevmeter：`flag` 默认=该题分数分布 P98，floor 0.5 | 用 mock 分布运行，**输出阈值与该分布 P98 误差 <0.01**；阈值随题而异的证明用例 |
| S10 | **乱序翻转率并报**：每轮评审同时报"重复翻转率"（基线）与"乱序翻转率"，两数并出而非只报其一 | mahlernim：乱序 13–14% vs 重复 1–2%——只报其一会系统性误估模型不稳定度 | 采样 5 次中 2 次题目乱序，**报告同时含两个翻转率字段且乱序≥重复方向成立**（不成立时告警而非静默） |
| S11 | **模型/协议版本戳**：每次评审 run 记录协议模板哈希+日期+执行通道（LLM-as-Jev 下"模型版本"=提示协议版本），报告头强制字段 | 所有负结果库（phishing/smoking/4esv）都锚死 jev-1.13.0 出数；zhuyansen 记录每个响应的 model 字段 | 连跑两次：报告含相同 protocol-hash；改协议后 hash 变化并在报告中标"不可与旧轮对比" |

**不写的建议**（无验收步骤或本链路上不可行，按 PLAN 戒条剔除）：API-confidence 直采（我们无 key）、多模型对照矩阵（超出 LLM-as-Jev 单通道）、$成本报表（无账单面）。

## 五、存在性翻案实录（B0-I2 结案的批次级修正）

B3 拉取时 2 条 `tests/test_decision_policies(.py)` "MISS"，顺藤查 `existence.csv` 竟标 200 → 证实 **gh-proxy 对任意 `github.com/<o>/<r>` 页面路径一律返回自身主页 200**：B0 轮"266/266 全 200 零幻觉库"验的是代理存活度，结论作废。

正确通道重验（`verify_existence_v3.py`：jsDelivr 主 + gh-proxy API 兜底，正负对照内置）259 行全量：

- **256 存在**（255 README + 1 API）
- **2 真库仅 HF**（alexwortega/openjev、drinkmoonshine/parallel-constrained-decoding——B1 挂起行就此闭环：GH 侧确认无物，价值在 HF 侧）
- **1 链接 404**（vlad-terin/jev-browser，anotiawang 清单原文引用；存在性核验转为清单质量证据）
- **5 分类器假阳性删除**：`typesafe/jev-1`（OpenRouter 模型标识被 BARE+backtick 误捕）、`port/derivative`（散文短语）、`source/platform`（yibie 模板占位）、`danwilloughby/snifftest`（PLAN L105 拼写变体，真库 danrwilloughby/snifftest 健在）、`tests/test_decision_policies.py`（v6 已删）
- 分类器 **v7**：STOP_WORDS+{source,port}、DELETE 集（行级+溯源注释）、补录/输出双点过滤 → **263→259**（B8 68、B5 18）；batch00/b0_review 已同步修订（新增 I9 行）
- 通道教训入 b0_review §四-6：**探活通道必须正对照（真库 200）+负对照（假库 404）双测，缺一结论作废**

## 六、可迁移要点（浅采库所得，编号对应 §四）

1. **jevslop**：八维镜像——"每轴一个原子 Score + 总体另行直判"结构照搬进我们情绪密度/K 完成度维度（→S7）；"结果不是作者身份概率"的宣称边界句写法。
2. **citation-verifier**：三级流水线含"证明存在否则丢弃"（→S8）；"not in abstract 弱于 not in paper"的分级表述。
3. **frostney**：判定与行文分离——34 布尔一次调用，评语由另一模型从 findings 生成；"文档只读不判"（问题集中没有散文问题就不该有散文裁决）→ 我们章评协议的架构范本。
4. **mahlernim**：翻转率必须区分乱序/重复两基线（→S10）；5→100 题自我修正轶事=小样本宣称打折的又一例。
5. **jevmeter**：分位数阈值（→S9）；held-out 集专设"近似陷阱"样本（礼貌感谢语 vs 真回避）；keep-alive 省 15 倍 TLS 握手。
6. **vinilana**：done-gate=完成度 veto 在路由之前的实现样例；干扰工具相似命名测误触——可移植到我们要害问答的"近似混淆选项"设计。
7. **shogo**：pilot 子集"见结果前机械固定"且源码注释自证——我们 gold 冻结（→S6）的同款做法。

## 七、I7 抽查实录（bulk-suspect 第二维证据）

| owner | 抽查库 | commits/day | 判 |
|---|---|---|---|
| owner-A (5 库) | jev-scout (B3) | 2 commits / 全 09-18 单日 / 单一 author | **脚手架特征成立**，其 B3 库降"留矩阵·存疑"，引用其数字需第三方佐证 |
| owner-B (5 库) | jev-benchmarks (B3) | 4 commits / 全 09-17 单日；**但** awesome-typesafe 30 commits 含 21 位外部作者 | **正当维护者**：单库快迭代是风格，目录有真实社区流；解除名单 |
| kitze (3 库) | 其 B3 关联库 404（jev 名不在清单） | — | 留待 B7 批（其库集中在 SDK 侧）复核 |

## 八、遗留与挂账

- [x] RB3 复审轮闭环：`eval/b3_review.jsonl`（2×5 问，`--check` ✓，盲审 10/10）+ `reports/b3_review.md`；两处实缺陷（S2 8vs7、核账粒度）已修入本文，详见 b3_review §三
- [x] v3 存在性全量重验 + v7 分类器（§五）
- [x] batch00 / b0_review 翻案传导
- [ ] zhuyansen `jse robustness` 无 key 重打分（tarball 通道已开，其数据体积待验）→ 挂 B4 批顺路
- [ ] agentjournal.dev 是博客非仓库（PLAN L88 点名项），"单问 vs 12-14 维分解 0.9076 vs 0.8373"数据点未溯源 → 下轮用 web-fetch 通道补
- [ ] Hegar Garcia 无 License 行：模式照记（评测代码无授权声明），不引其代码
- [ ] S1–S11 改造建议的**实施**属 本地网文创作系统（独立私有仓，未随本仓发布） 侧工作，本战役只交付清单+验收步骤
