# 生成 eval/b5_review.jsonl（RB5 复审轮，2 条 × 5 问，LLM-as-Jev 自写合成样本）
import json, pathlib

root = pathlib.Path(r".")

a_state = {
    "pool": 18,
    "header_claim_first_draft": {"深采": 2, "浅采含要点": 6, "留矩阵": 10, "移批": 0, "丢弃": 0},
    "actual_matrix_counts": {"深采": 2, "浅采要点": 5, "留矩阵": 9, "留矩阵存疑": 2},
    "note_devagrawal": "预排序头名 293★ 处置=留矩阵（§一名额说明用词'浅采·要点'与矩阵处置列不一致，RB5 二次审出）",
    "drift_recurrence_index": ["B0 59vs67", "B2 浅8vs7", "B3 S2 8vs7", "B5 浅6留10 vs 浅5留9+疑2"],
    "precheck_script": "_rb5_precheck.py（写后核账，18 行全 token 命中原文 grep）",
    "premature_checkbox": {"line": "§七 RB5", "defect": "产物未创建即勾 [x] 并写出文件名/盲审分数", "fix": "改回 [ ] 实态，闭环后翻勾"},
    "rerun": {"channel": "npm registry 直连", "install": "snifftest v0.1.0 27s",
              "arm_runnable": "countable", "arm_blocked": "judgment 需 key",
              "reverse_check": "hyphen 不触发 dash=设计而非漏检"},
    "deep_slots": [{"repo": "danrwilloughby/snifftest", "basis": "PLAN 点名+零 key 臂唯一可复跑"},
                   {"repo": "coldteadotai/abide", "basis": "与 snifftest 制度面互补无重叠"}],
}

b_state = {
    "feedback_items_first_draft": 8,
    "feedback_items_actual": {"do_steal": 7, "dont_steal": 1},
    "rerun_campaign_history": {"B1": "受阻", "B2": "零 key 不可复跑", "B3 jevcal": "完整成功", "B5 snifftest": "countable 臂部分成功"},
    "second_success_wording": "标题写'本战役第二次无 key 复跑'——jevcal 为完整回路，snifftest 为单臂部分成功，'第二次'未区分完全性",
    "i7": {"owner": "owner-A", "triggers": 2, "prior_trigger": "B3 已判 scaffold", "action": "降级令扩至全部 5 库"},
    "dual_channel": {"jev_code_missing": "inventory grep 证实落 B8", "winnow_nofile": "首查文件名猜错，双通道暴露"},
}

def q(qid, prim, question, options=None, legend=None):
    d = {"qid": qid, "primitive": prim, "question": question}
    if options: d["options"] = options
    if legend: d["legend"] = legend
    return d

# 直接构造 gold
entry_a = {
    "id": "RB5-A-01",
    "category": "B5 工件一致性",
    "state": json.dumps(a_state, ensure_ascii=False),
    "questions": [
        q("header_vs_matrix_drift_class", "score",
          "首版头部'浅6留10'与矩阵实数'浅5留9+疑2'的偏差属于哪一档？legend: 0=文档无矩阵可对照（虚构声明）; 1=矩阵存在但头部计数与处置列脱钩（人写漂移）; 2=头部计数由脚本生成且与矩阵一致",
          legend={"0": "文档无矩阵可对照（虚构声明）", "1": "矩阵存在但头部计数与处置列脱钩（人写漂移）", "2": "头部计数由脚本生成且与矩阵一致"}),
        q("checkbox_before_artifact", "noul",
          "§七在 b5_review.jsonl/b5_review.md 尚不存在时即写'[x] 已完成+盲审 10/10'——这是否构成'未发生事实写入完成态'缺陷（不同于计数漂移，这是凭空宣称执行）？"),
        q("precheck_catches_all", "choice",
          "RB5 前置核账脚本（18 行处置解析+7 组数字 token 原文 grep）在定稿缺陷发现上的实际作用？",
          options=["抓出唯一实锤缺陷（头部计数），其余 token 全命中", "什么都没抓到（文档本来就对）", "抓出多处包括矩阵行错漏", "脚本本身跑挂未产出结论"]),
        q("npm_channel_generality", "choice",
          "'npm registry 直连可用'这一通道事实对本战役后续（B6-B8 复跑）的适用性？",
          options=["仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道", "对所有 GitHub 仓库普遍适用", "对 Docker 镜像分发同样适用", "npm 通道随时会失效不应依赖"]),
        q("partial_vs_full_rerun", "score",
          "把 snifftest countable 臂成功与 jevcal 完整回路成功并记为'第二次无 key 复跑'，措辞严谨度？legend: 0=标题宣称完整而正文无任何臂级限定; 1=可接受但应加限定词; 2=完全严谨（§三表格已分列 arms）",
          legend={"0": "标题宣称完整而正文无任何臂级限定", "1": "可接受但应加限定词", "2": "完全严谨（§三表格已分列 arms）"}),
    ],
    "gold": [
        {"qid": "header_vs_matrix_drift_class", "score": 1, "probabilities": [0.08, 0.84, 0.08], "confidence": 0.84,
         "samples": [1, 1, 1, 2, 1], "blind": "agree",
         "rationale": "矩阵 18 行处置列完整存在且可解析，头部是另一只手写的汇总——典型'人写计数与实枚举脱钩'（同类第四复发）；给 2 的样本混淆了'事后修对'与'生成方式'，修对后当前版才是 2，但题目问首版偏差定性"},
        {"qid": "checkbox_before_artifact", "noul": 0.95, "probabilities": [0.95, 0.05], "confidence": 0.93,
         "samples": [0.95, 0.98, 0.9, 0.95, 0.9], "blind": "agree",
         "rationale": "文件不存在、--check 未跑、盲审分数无从产生，却在挂账区以完成态写出全部三个事实要素——比计数漂移重一档（凭空宣称执行）；0.05 留给'可能是打算稍后补齐所以先写'的善意解释，但复审协议下产物落地才算闭环"},
        {"qid": "precheck_catches_all", "choice": "抓出唯一实锤缺陷（头部计数），其余 token 全命中", "probabilities": [0.86, 0.04, 0.06, 0.04], "confidence": 0.86,
         "samples": ["抓出唯一实锤缺陷（头部计数），其余 token 全命中", "抓出唯一实锤缺陷（头部计数），其余 token 全命中", "抓出多处包括矩阵行错漏", "抓出唯一实锤缺陷（头部计数），其余 token 全命中", "抓出唯一实锤缺陷（头部计数），其余 token 全命中"], "blind": "agree",
         "rationale": "实测输出：98.64/5,733/212/88/150/0.75/39 对 _b5 原文全 HIT，snifftest 四 token 全 True，唯一 False 即 header ok（浅6留10）；'抓出多处'高估了——矩阵行本身无误"},
        {"qid": "npm_channel_generality", "choice": "仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道", "probabilities": [0.8, 0.05, 0.07, 0.08], "confidence": 0.8,
         "samples": ["仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道", "仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道", "对所有 GitHub 仓库普遍适用", "仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道", "仅对 npm 分发的 JS/TS 库适用，Python 库仍需 pip/源包通道"], "blind": "agree",
         "rationale": "已验证事实只覆盖 npm 包（snifftest 系 JS CLI）；pip git+https 本战役实测已死是反例——通道按分发介质各记各的，'npm 随时失效'无证据支撑不选"},
        {"qid": "partial_vs_full_rerun", "score": 1, "probabilities": [0.14, 0.66, 0.2], "confidence": 0.62,
         "samples": [1, 1, 2, 1, 0], "blind": "agree",
         "rationale": "边缘题：§三表格确已分列 countable 跑通/judgment 需 key 被阻（判 2 的样本据此），但节标题'第二次无 key 复跑'单独成立时会高估完全性——加'（countable 臂）'限定词即无歧义；判 0 过严，正文限定充分"},
    ],
    "note": "自写合成样本（对 B5 产物的结构化诊断统计），非任何真实作品",
}

entry_b = {
    "id": "RB5-B-01",
    "category": "B5 深读与反哺质量",
    "state": json.dumps(b_state, ensure_ascii=False),
    "questions": [
        q("devagrawal_wording_conflict", "noul",
          "§一用'浅采·要点'描述 devagrawal09 的降级去向，矩阵处置列实为'留矩阵'——两处用词是否一致？"),
        q("deep_pair_complement", "choice",
          "snifftest+abide 这对深读组合的互补性论证（读数制度 vs 审计修订制度）强度？",
          options=["互补面清晰：三带读数/缓存键 vs 召回审计/死规则体检，交集近零", "重叠过多：两者都是文本 flag 工具", "abide 应让位给 293★ 的 devagrawal09", "snifftest 不应入选（PLAN 点名不算独立论证）"]),
        q("feedback_do_dont_split", "score",
          "§四 8 项中 7 项'可搬'+1 项'不搬'的配置（第 8 项集中列反模式），对反哺清单的实用性？legend: 0=反模式不该出现在反哺清单; 1=该有但应逐项内联标注; 2=集中列法最优（读清单的人一眼看到边界）",
          legend={"0": "反模式不该出现在反哺清单", "1": "该有但应逐项内联标注", "2": "集中列法最优（读清单的人一眼看到边界）"}),
        q("i7_extension_soundness", "noul",
          "owner-A 第 2 次触发后把降级令扩至其全部 5 库（含未逐库复查的 3 库）——'owner 级推定'在本战役证据标准下是否可接受（处置仅为存疑标记非丢弃）？"),
        q("rerun_claim_next_audience", "choice",
          "本批复跑结论进 FINAL 总报告时，最低限度必须携带的限定信息？",
          options=["countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套", "只需'复跑成功'四字", "只需安装方式（npm）", "需附上 snifftest 全部 63/80 数字"]),
    ],
    "gold": [
        {"qid": "devagrawal_wording_conflict", "noul": 0.0, "probabilities": [0.0, 1.0], "confidence": 0.9,
         "samples": [0.0, 0.0, 0.05, 0.0, 0.0], "blind": "agree",
         "rationale": "同文档两节对同一库给出两个处置档位词，直接可判不一致；矩阵是处置的权威源（核账脚本只解析它），§一应改'→留矩阵'——RB5 二次审出，同轮修复"},
        {"qid": "deep_pair_complement", "choice": "互补面清晰：三带读数/缓存键 vs 召回审计/死规则体检，交集近零", "probabilities": [0.78, 0.08, 0.07, 0.07], "confidence": 0.78,
         "samples": ["互补面清晰：三带读数/缓存键 vs 召回审计/死规则体检，交集近零", "互补面清晰：三带读数/缓存键 vs 召回审计/死规则体检，交集近零", "abide 应让位给 293★ 的 devagrawal09", "互补面清晰：三带读数/缓存键 vs 召回审计/死规则体检，交集近零", "重叠过多：两者都是文本 flag 工具"], "blind": "agree",
         "rationale": "snifftest 贡献判定读出制度（三带/反例字段/缓存键），abide 贡献事后审计制度（召回确认表/死规则禁用/漏检入账）——§四 7 项可搬件两两来源不重叠即为证据；'让位 293★'违反热度不折名额的既立尺度（B1/B2 同尺）"},
        {"qid": "feedback_do_dont_split", "score": 2, "probabilities": [0.1, 0.3, 0.6], "confidence": 0.6,
         "samples": [2, 1, 2, 2, 1], "blind": "agree",
         "rationale": "边缘题：反哺清单的读者是评测链路改造者，边界（什么不能照抄）与内容同等重要，集中列'不搬'项+理由正是 snifftest not_for 模式在文档自身的运用（判 2）；判 1 样本主张内联标注更防漏读——2:1 但置信 0.60 记为弱多数"},
        {"qid": "i7_extension_soundness", "noul": 0.82, "probabilities": [0.82, 0.18], "confidence": 0.78,
         "samples": [0.85, 0.8, 0.9, 0.7, 0.85], "blind": "agree",
         "rationale": "I7 制度本就作用于 owner（B3 对 owner-A 首判时亦已扩及其余库），且处置是'存疑'非'丢弃'——可逆的保守标记按 owner 推定成立，逐库复查成本与收益不匹配；0.18 留给'第三复发风险：推广未复查行的数字若被下游引用'的暴露面"},
        {"qid": "rerun_claim_next_audience", "choice": "countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套", "probabilities": [0.88, 0.04, 0.04, 0.04], "confidence": 0.88,
         "samples": ["countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套", "countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套", "只需复跑成功四字", "countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套", "countable 臂成功+judgment 臂未跑+bench 数字未独立复核 三件套"], "blind": "agree",
         "rationale": "与 partial_vs_full_rerun 同源的汇报纪律：三件套缺一即让读者高估验证深度；'带全部数字'反而复制未复核数字进 FINAL，与挂账区'引用带自测已发布级'的既定标注冲突"},
    ],
    "note": "自写合成样本（对 B5 产物的结构化诊断统计），非任何真实作品",
}

out = root / "eval" / "b5_review.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(entry_a, ensure_ascii=False) + "\n")
    f.write(json.dumps(entry_b, ensure_ascii=False) + "\n")
# 自校验：概率和、盲审字段
for i, line in enumerate(out.read_text(encoding="utf-8").splitlines()):
    e = json.loads(line)
    for gg in e["gold"]:
        s = sum(gg["probabilities"])
        assert abs(s - 1.0) <= 0.02 + 1e-9, (i, gg["qid"], s)
        assert gg["blind"] == "agree" and len(gg["samples"]) == 5
    print(e["id"], "gold:", len(e["gold"]), "q:", len(e["questions"]), "probs ok")
print("bytes:", out.stat().st_size)
