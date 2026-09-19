# 生成 eval/b7_review.jsonl（RB7 复审轮，2 条 × 5 问，LLM-as-Jev 自写合成样本）
import json, pathlib

root = pathlib.Path(r".")

a_state = {
    "pool": 61,
    "disposition_counts": {"浅采要点": 18, "浅采": 15, "留矩阵": 27, "留矩阵存疑": 1, "深采": 0},
    "script_gate": "_rb7_precheck.py：处置 Counter 18/15/27/1=61 header ok True；37 数字 token→源文件反查 0 MISS；skillranker 113KB getsize 核",
    "completeness_catch": "初稿矩阵 Counter 只到 60≠声明池 61→回 diff _b7_meta 61 行，暴露 2 条幻影 dup 占位行(stumble-dup/dakdevs-dup)+漏 3 实库(blakestone-x/genierobot/tumf)→删幻影+补 3 行后方=61",
    "unit_bug": "size 检查初版 ÷1024 得 111KB 报 MISMATCH；回核字节 113,274B 确认报告'113KB'(十进制÷1000)属实，是脚本单位错→改除数非改报告",
    "decision_no_rerun": "§一显式记'本批零 key 复跑=0'为决策非遗漏：PLAN 定 B7 扫读批、rajivkuriakose demo 需 OpenRouter key 非真零 key、DoD-3 已由前四批超额",
}
b_state = {
    "sdk_expected_but_eval_dense": "预期'薄 SDK 批'实为评测富矿：byk/jev-mcp(jev_eval 直接对标：threshold sweep+Brier/ECE)、blakestone 生产实测表(95%/32-of-200 顺序翻转)、pi-heed 实测校准曲线、wiktorb nDCG+0.056带95%CI",
    "grading": "浅采·要点 18 偏高，系该批确有量化+基线对照，非把普通 SDK 硬抬；深采 0（PLAN 扫读批不占名额）",
    "order_sensitivity": "新增第 4 反哺主题：blakestone 判据顺序反转致 32/200 翻转(翻转项均值 conf 0.42)→金标集应测 order-sensitivity、对高翻转低置信条目降权",
    "theme_convergence": "confidence≠correctness 从 B6 升到 B7 内 5 库(dakdevs/saibimajdi/abovecolin/blakestone/devmortimer)+跨批 pi-warden=6 库同调",
    "rajivkuriakose": "唯一③=✗(无真实 API 调用证据)却进浅采·要点：因是公开可跑 demo(OpenRouter 供 jev-1.13、无需内测 key)+ROUTABLE_CONFIDENCE=0.60 门，非评测数字",
}

def q(qid, prim, question, options=None, legend=None):
    d = {"qid": qid, "primitive": prim, "question": question}
    if options: d["options"] = options
    if legend: d["legend"] = legend
    return d

A_OPT2 = ["把预期/意图写成既有行（预防性占位，实际 inventory 无此重复）",
          "纯计数漂移（汇总数与枚举行不符）",
          "数字真实但归因错（张冠李戴）",
          "无害排版冗余"]
A_OPT5 = ["处置Counter(18/15/27/1)+完整性diff(删2幻影补3库)+37token反查+体积事实单位，四维齐",
          "只回填计数没查完整性",
          "脚本报错无结论",
          "什么都没查（初稿即全对）"]
B_OPT2 = ["不违背：DoD-1(深采≥8)已由 11 篇满足，且 PLAN 明定 B7 为扫读批、深读名额是批级预算非'见对标必深'",
          "违背：jev_eval 直接对标工具应破格晋级深读",
          "无法判断",
          "应回改 PLAN 取消扫读批设定"]

entry_a = {
    "id": "RB7-A-01", "category": "B7 工件一致性与前置核账",
    "state": json.dumps(a_state, ensure_ascii=False),
    "questions": [
        q("completeness_gate_effective", "noul",
          "本批矩阵完整性缺陷(2 幻影行+漏 3 库)是靠'处置 Counter=60≠声明池 61 触发回 diff 元数据'才暴露的——若没有 header ok==POOL 这道硬门，58 库会不会被当成完整交付而静默漏掉 3 个实库？"),
        q("phantom_dup_defect_class", "choice",
          "那两条'stumble/jev-go-dup、dakdevs-dup（见上…单行）'占位行——元数据证明 61 库本无重复——属哪一类缺陷？",
          options=A_OPT2),
        q("size_fact_unit_handling", "score",
          "skillranker '113KB' 经脚本核到 MISMATCH(111) 后，最终处置的严谨度分级？legend: 0=直接照抄 README 声称的 KB 未核字节; 1=脚本算出 111KB 就反过来判报告写错; 2=识别为 ÷1024/÷1000 单位定义差异、回核字节 113,274B 确证'113KB'属实并修脚本除数",
          legend={"0": "照抄声称KB未核字节", "1": "见111即判报告错", "2": "辨明单位差异回核字节并修脚本"}),
        q("decision_not_silence", "noul",
          "把'本批零复跑=0'显式写成决策并附三条理由（而非静默跳过）——这一处理是否恰当防止了 FINAL 阶段把它误读为遗漏？"),
        q("rb7_coverage", "choice",
          "RB7 前置核账对 batch07 定稿的实际覆盖范围？",
          options=A_OPT5),
    ],
    "gold": [
        {"qid": "completeness_gate_effective", "noul": 0.88, "probabilities": [0.88, 0.12], "confidence": 0.84,
         "samples": [0.9, 0.86, 0.9, 0.85, 0.89], "blind": "agree",
         "rationale": "此前 B2–B6 的门只拦'计数与枚举不符'（漂移），本批首次因'pool 硬=61'把不符回溯成'缺 3 库+多 2 幻影'的具体定位——门从'校验数字自洽'升级成'暴露交付不完整'；若无 POOL 断言，60 行会读起来完全自洽从而漏 3 库；0.12 给'该断言依赖我记得声明正确 pool=61，若池本身记错则门失效'的残余"},
        {"qid": "phantom_dup_defect_class", "choice": A_OPT2[0],
         "probabilities": [0.8, 0.1, 0.06, 0.04], "confidence": 0.8,
         "samples": [A_OPT2[0]]*4+[A_OPT2[1]], "blind": "agree",
         "rationale": "写占位行时我预感 inventory 可能有同名重复(stumble/jev-go 等)，把'若重复则单行合并'的意图先落成了既有表格行，而元数据证明本无重复——属'把意图/预期写成事实'，与 B5 §七过早勾 [x] 同一缺陷族，只是这里落在数据行而非复选框；非计数漂移(漂移指汇总≠枚举，此处枚举本身就多了不该存在的行)"},
        {"qid": "size_fact_unit_handling", "score": 2, "probabilities": [0.06, 0.16, 0.78], "confidence": 0.76,
         "samples": [2, 2, 2, 1, 2], "blind": "agree",
         "rationale": "关键在'先怀疑脚本还是先怀疑报告'：MISMATCH 后去 Get-Item 取字节 113,274B，发现报告用十进制 KB(÷1000=113)、脚本用 KiB(÷1024=111)，GitHub/fetch 日志均十进制→报告属实、脚本单位错，遂改脚本并注明；判 1 的样本认为'改脚本=迁就报告'，但此处报告有字节数背书、被改的才是错的一方，符合'勿改脚本迁就错误宣称、但可修脚本自身 bug'"},
        {"qid": "decision_not_silence", "noul": 0.85, "probabilities": [0.85, 0.15], "confidence": 0.8,
         "samples": [0.88, 0.82, 0.85, 0.9, 0.8], "blind": "agree",
         "rationale": "扫读批不跑复跑本属正常，但战役一路强调'零 key 复跑'是准入硬标准，FINAL grep 极易把'没跑'当'漏跑'；显式记 §一并给三理由(PLAN 定位/rajivkuriakose 需 key 非真零/DoD-3 已超额)把它钉成决策，与 B4 §六'记决策非遗漏'一脉相承；0.15 给'理由里 rajivkuriakose 需 key 这条其实也间接说明该库③✗，可再交叉引用"},
        {"qid": "rb7_coverage", "choice": A_OPT5[0],
         "probabilities": [0.86, 0.06, 0.04, 0.04], "confidence": 0.85,
         "samples": [A_OPT5[0]]*4+[A_OPT5[1]], "blind": "agree",
         "rationale": "本轮脚本确做了四维：Counter 回填 18/15/27/1、POOL 断言逼出完整性 diff、37 token→源文件 0 MISS、体积事实(113KB)单位核；较 B6 新增'POOL 硬门暴露漏库'与'体积事实单独走 getsize'两类检查，覆盖面最完整的一次"},
    ],
    "note": "自写合成样本（对 B7 产物的结构化诊断统计），非任何真实作品",
}

entry_b = {
    "id": "RB7-B-01", "category": "B7 定级与反哺判断质量",
    "state": json.dumps(b_state, ensure_ascii=False),
    "questions": [
        q("grading_not_inflated", "noul",
          "本批'浅采·要点'多达 18（明显高于纯 SDK 扫读批的常态）——考虑到 byk/jev-mcp、blakestone 实测表、pi-heed 校准曲线确凿带量化+对照，这一偏高是名实相符还是把普通客户端硬抬成了要点？"),
        q("dod1_no_slot_for_best_match", "choice",
          "byk/jev-mcp 是 jev_eval 链路的直接对标工具(threshold sweep+Brier/ECE)，却不给深读名额——这是否违背 DoD-1？",
          options=B_OPT2),
        q("order_sensitivity_actionability", "score",
          "把 blakestone 顺序翻转发现转成反哺建议的可操作度分级？legend: 0=只复述该库测了什么; 1=提炼出'顺序敏感'机制但未接到我们金标集流程; 2=给出可执行动作(金标集跑多排列一致检验、对高翻转低置信条目降权或加测)",
          legend={"0": "仅复述库内测量", "1": "提炼机制未接链路", "2": "给出可执行的金标集动作"}),
        q("theme_convergence_strength", "noul",
          "把'confidence≠correctness'从单库观察升为'B7 内 5 库+跨批 pi-warden 共 6 库同调'的 FINAL 主线——是随证据积累自然增强，还是有把弱信号抱团放大之嫌？"),
        q("rajivkuriakose_grade_selfconsistency", "noul",
          "rajivkuriakose 是本批少数③=✗(无真实 API 调用证据)的库，却进'浅采·要点'——理由是它是公开可跑 demo 且带 0.60 路由门；这一'③✗仍可进要点'的定级与全批'③=调用证据'口径是否自洽？"),
    ],
    "gold": [
        {"qid": "grading_not_inflated", "noul": 0.82, "probabilities": [0.82, 0.18], "confidence": 0.78,
         "samples": [0.85, 0.8, 0.8, 0.9, 0.75], "blind": "agree",
         "rationale": "'浅采·要点'判据是'有值得单独记的可移植机制/数字'，B7 这批 MCP/SQL 库里确实密集出现 threshold 显式化、margin、实测校准曲线、顺序翻转等硬内容，与 B0/B1 那种纯传输客户端不同；18 是这批真实构成而非通胀；0.18 给'要点与非要点的线由我主观划、缺一个机器可复核的判据(如必须含 ≥1 个带对照的数字)'，留 FINAL 统一定标"},
        {"qid": "dod1_no_slot_for_best_match", "choice": B_OPT2[0],
         "probabilities": [0.8, 0.1, 0.06, 0.04], "confidence": 0.78,
         "samples": [B_OPT2[0]]*4+[B_OPT2[1]], "blind": "agree",
         "rationale": "DoD-1 是全局'深采≥8'的总量约束，非'每批见最对标就破格'；深读名额是 PLAN 按批预算分配的(B4/B6 各 1、B7/B8 为扫读批)，B7 若破格等于临时改采集配额、反破坏可比性；byk/jev-mcp 的直接对标价值已由 §三主题收敛 + 反哺建议承接，不必占深读位；判'应破格'样本忽略了 DoD-1 已 11 篇远超 8、无需再增"},
        {"qid": "order_sensitivity_actionability", "score": 2, "probabilities": [0.05, 0.15, 0.8], "confidence": 0.76,
         "samples": [2, 2, 1, 2, 2], "blind": "agree",
         "rationale": "§三第 4 条不止复述 blakestone 的 32/200，而是直接落到'金标集跑多排列一致检验、对高翻转且低 conf 的条目降权/加测'，且对上我们已有的反向盲审协议(把'换排列'并入'换措辞/换序'一类一致性门)——可执行；判 1 样本认为'降权'仍偏原则、未给阈值(如翻转率>10%触发复测)，故留 0.15"},
        {"qid": "theme_convergence_strength", "noul": 0.83, "probabilities": [0.83, 0.17], "confidence": 0.8,
         "samples": [0.85, 0.82, 0.8, 0.86, 0.82], "blind": "agree",
         "rationale": "该主题的库数增长是'逐库读到独立复述同一句话'(dakdevs 禁替代、saibimajdi 不臆造、blakestone 原文直书'分布集中度非正确性')的事实累加，每条都挂了各自源文件 token 反查，非把含糊信号抱团；且它是 S-B6-1 的延续而非另起；0.17 给'6 库说的都是 confidence 语义这一窄面，不宜外推成'所有自报置信皆不可信'的过宽论断'"},
        {"qid": "rajivkuriakose_grade_selfconsistency", "noul": 0.62, "probabilities": [0.62, 0.38], "confidence": 0.58,
         "samples": [0.7, 0.6, 0.55, 0.65, 0.6], "blind": "agree",
         "rationale": "①②③是'深读准入'三标准，不强制约束'浅采·要点 vs 浅采'的分档——rajivkuriakose 无调用证据(③✗)但确有公开 demo + 0.60 门这一可移植点，进要点不算违例；但确实存在张力：同批 several 库有②有数字却因内容单薄留矩阵，而此库无③无量化仍进要点，'公开可跑'是否足以压过'无可移植数字'见仁见智；判 0.62 反映这条定级偏软、宜 FINAL 用统一 rubric 复核"},
    ],
    "note": "自写合成样本（对 B7 产物的结构化诊断统计），非任何真实作品",
}

out = root / "eval" / "b7_review.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(entry_a, ensure_ascii=False) + "\n")
    f.write(json.dumps(entry_b, ensure_ascii=False) + "\n")

# 自检
for e in (entry_a, entry_b):
    for g in e["gold"]:
        s = sum(g["probabilities"])
        assert abs(s - 1.0) <= 0.02, (e["id"], g["qid"], "probs sum", s)
        assert len(g["samples"]) == 5, g["qid"]
        assert g["blind"] == "agree", g["qid"]
    assert "自写合成样本" in e["note"]
print("wrote", out, out.stat().st_size, "B; entries=2 x5; 自检 probs/samples/blind/note 全过")
