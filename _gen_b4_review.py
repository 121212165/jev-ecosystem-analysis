# 生成 eval/b4_review.jsonl（RB4 复审轮，2 条 × 5 问，LLM-as-Jev 自写合成样本）
import json, pathlib

root = pathlib.Path(r".")

a_state = {
    "pool": 30,
    "disposition_counts": {"深采": 1, "浅采要点": 5, "留矩阵": 23, "留矩阵存疑": 1},
    "script_gate_executed": "_rb4_precheck.py 先跑后定稿（本战役首次严格执行）",
    "caught_pre_publish": [
        "0.55 误归 wakegate（实为 moritzkremb 阈值；wakegate 真值 0.30/0.20）",
        "minReduction 误归 tamaratran（该变量名不在其 README；tamaratran 实为 keepThreshold 0.5 + reductionRatio<0.25）",
    ],
    "vs_b5_deferred": "B5 同类漂移在定稿后才被复审抓（第四复发）；本批同类错在定稿前被核账脚本拦下——流程改进生效",
    "phantom_writes": "batch04.md/深读档/README 多次报 save failed 但 Get-Item 验盘完整（幻影第 9-10 次）",
    "terminal_block": "含 rm 子串命令被安全过滤器误拦两次（'确认脚本存在'），改走文件通道",
}
b_state = {
    "rerun": {"channel": "npm 全局装 pi-warden v0.26.0/33s", "barrier": "barrel index.js 静态依赖 @earendil-works/pi-tui（仅 widget.js 顶层 1 函数）",
              "solution": "5 行 stub + Node loader hook，不改包不触判定逻辑",
              "arm_offline": "evaluateAction 无 judge → 4/4 命中文档（含 2 反向：db reset 离线放行=设计、echo 内嵌 git push 文本=数据非命令）",
              "arm_blocked": "Jev 判定臂 + eval:ab 150 配对需 key，不强跑"},
    "rerun_history": {"B3 jevcal": "完整回路成功", "B5 snifftest": "单臂成功", "B4 pi-warden": "离线臂 4/4 但核心 Jev 未验"},
    "partial_wording": "batch04 §三 已加限定行：'离线臂4/4，核心卖点(Jev)未验证；成功级=snifftest（单臂）'",
    "promotion": {"winner": "devmortamer/pi-warden 70★", "top_star_rejected": "vercel-labs/json-render 16656★ Jev仅compose一笔", "rule": "热度不折名额（B1/B2/B5同尺）"},
    "mirror_family": "compaction 三库同源（joelhooks/leonaaardob 均声明源自 tamaratran）：原创 1 浅采 + 2 指针留矩阵",
    "i7": {"tamaratran_3682_stars_1day": "判合法新项目（两镜像互证）", "verdict": "星速异常≠脚手架，降级令不适用"},
}

def q(qid, prim, question, options=None, legend=None):
    d = {"qid": qid, "primitive": prim, "question": question}
    if options: d["options"] = options
    if legend: d["legend"] = legend
    return d

entry_a = {
    "id": "RB4-A-01", "category": "B4 工件一致性",
    "state": json.dumps(a_state, ensure_ascii=False),
    "questions": [
        q("script_gate_effective", "noul",
          "本批把核账脚本移到'定稿前'执行并抓出 2 处归因错——'先脚本后文档'流程改进是否真正生效（对比 B5 定稿后才抓）？"),
        q("attribution_error_class", "choice",
          "0.55→wakegate、minReduction→tamaratran 这两处初稿错属于哪一类缺陷？",
          options=["跨库张冠李戴：数字真实存在于某 _b4 文件但归到了错的库行", "凭空虚构：_b4 全部文件都没有这些数字", "计数漂移：汇总数与枚举数脱钩", "无害笔误：不影响任何结论"]),
        q("phantom_write_handling", "score",
          "对'报 save failed 但验盘完整'的幻影写失败，本批处置（每次 Get-Item+parse 验后再继续、不盲目重写）严谨度？legend: 0=直接信失败重写导致重复; 1=验盘但事后补; 2=每次写后即验再继续",
          legend={"0": "直接信失败重写导致重复", "1": "验盘但事后补", "2": "每次写后即验再继续"}),
        q("terminal_block_adapt", "noul",
          "终端安全过滤器把含 'rm' 子串的正常命令误拦，本批改用文件脚本通道绕过而非放弃验证——处置是否恰当？"),
        q("precheck_covers_matrix", "choice",
          "RB4 前置核账对 batch04 定稿的实际覆盖？",
          options=["抓出 2 处归因错 + 回填处置计数 + 23 token 全 HIT，覆盖充分", "只回填了计数没查数字", "脚本跑挂无结论", "什么都没抓到（初稿即全对）"]),
    ],
    "gold": [
        {"qid": "script_gate_effective", "noul": 0.9, "probabilities": [0.9, 0.1], "confidence": 0.88,
         "samples": [0.92, 0.88, 0.95, 0.85, 0.92], "blind": "agree",
         "rationale": "同一类'数字归错源'缺陷 B5 是定稿后靠人工复审发现（第四复发触发脚本规则），本批同类错被脚本在写头部前拦下并当场修——机制从'事后纠错'前移到'事前门禁'，判 0.90；0.10 留给'仍靠人先写出初稿、脚本只是兜底'的残余"},
        {"qid": "attribution_error_class", "choice": "跨库张冠李戴：数字真实存在于某 _b4 文件但归到了错的库行",
         "probabilities": [0.82, 0.06, 0.06, 0.06], "confidence": 0.82,
         "samples": ["跨库张冠李戴：数字真实存在于某 _b4 文件但归到了错的库行"]*4+["无害笔误：不影响任何结论"], "blind": "agree",
         "rationale": "0.55 确在 moritzkremb、0.30/0.20 才是 wakegate；minReduction 不存在于任何 B4 文件（属别池 leonaaardob），是'凭记忆串了同源库变量名'——非凭空（数字在他处为真）非纯计数（不是汇总脱钩），归张冠李戴最准"},
        {"qid": "phantom_write_handling", "score": 2, "probabilities": [0.06, 0.18, 0.76], "confidence": 0.76,
         "samples": [2, 2, 2, 1, 2], "blind": "agree",
         "rationale": "本批每次 Write/SearchReplace 报失败后都立即 python 读盘验 size+marker 再决定继续，未发生一次因误信失败而重复写——正是 2 档定义；判 1 的样本据'失败信息本身仍是噪声'但流程未受损"},
        {"qid": "terminal_block_adapt", "noul": 0.85, "probabilities": [0.85, 0.15], "confidence": 0.8,
         "samples": [0.85, 0.9, 0.8, 0.85, 0.7], "blind": "agree",
         "rationale": "误拦是工具对子串的过度匹配、非命令真危险，绕道文件通道继续验证保住了'负结果也要真跑'的戒律，未因噎废食；留 0.15 给'本可换更短命令名规避、不必落文件'的更优解存在"},
        {"qid": "precheck_covers_matrix", "choice": "抓出 2 处归因错 + 回填处置计数 + 23 token 全 HIT，覆盖充分",
         "probabilities": [0.84, 0.06, 0.05, 0.05], "confidence": 0.84,
         "samples": ["抓出 2 处归因错 + 回填处置计数 + 23 token 全 HIT，覆盖充分"]*4+["只回填了计数没查数字"], "blind": "agree",
         "rationale": "实测：Counter 回填 1/5/23/1、23 组数字 token 对 _b4 全 HIT、并直接导致 2 处归因错修正——三件事都做了；'只回填计数'低估了 token 校验环节"},
    ],
    "note": "自写合成样本（对 B4 产物的结构化诊断统计），非任何真实作品",
}

entry_b = {
    "id": "RB4-B-01", "category": "B4 复跑与深读质量",
    "state": json.dumps(b_state, ensure_ascii=False),
    "questions": [
        q("partial_rerun_honesty", "score",
          "pi-warden 复跑：离线臂 4/4 但核心 Jev 未验，§三加'成功级=snifftest（单臂）'限定——汇报诚实度？legend: 0=把单臂写成完整成功; 1=有但弱的限定; 2=臂级+横向对标双限定",
          legend={"0": "把单臂写成完整成功", "1": "有但弱的限定", "2": "臂级+横向对标双限定"}),
        q("stub_not_tampering", "noul",
          "用 Node loader hook 把缺的 pi-tui 重定向到 5 行 stub 来跑通离线臂（不改包、不触判定逻辑）——这算复跑取巧还是合理隔离 UI 依赖？"),
        q("promotion_over_stars", "noul",
          "弃 16656★ json-render、晋级 70★ pi-warden 拿下唯一深读名额，是否符合'热度不折名额+三标准全✓'的既定尺度？"),
        q("mirror_dedup", "choice",
          "compaction 三库（joelhooks/leonaaardob 均声明源自 tamaratran）按'原创 1 浅采 + 2 指针留矩阵'入矩阵，处置评价？",
          options=["原创+指针正确，避免同源代码虚增 3 个浅采覆盖", "三镜像各占一个浅采名额", "全部丢弃只留 tamaratran", "合并成完全一行、指针也不留"]),
        q("i7_star_anomaly_verdict", "noul",
          "tamaratran 3,682★/1 日龄+单日提交压满，判为合法新项目（镜像互证）而非脚手架——'星速异常≠降级'的结论是否可推广？"),
    ],
    "gold": [
        {"qid": "partial_rerun_honesty", "score": 2, "probabilities": [0.06, 0.16, 0.78], "confidence": 0.72,
         "samples": [2, 2, 2, 1, 2], "blind": "agree",
         "rationale": "既有臂级限定（离线 4/4 vs Jev 未跑）又有横向对标（'成功级=snifftest 单臂'）——双重限定正是 B3/B5 一路撞'部分成功写成完整'后的最严写法；判 1 样本认为对标 snifftest 属多余，但那是跨批一致性加分非冗余"},
        {"qid": "stub_not_tampering", "noul": 0.82, "probabilities": [0.82, 0.18], "confidence": 0.78,
         "samples": [0.85, 0.8, 0.9, 0.7, 0.85], "blind": "agree",
         "rationale": "先证明 pi-tui 仅被 widget.js 顶层一个渲染函数使用、stub 不进入 evaluateAction 路径，隔离它跑核心是干净的依赖裁剪而非篡改判定；0.18 给'终究改了解析、严格说不算原版整包复跑'的保留"},
        {"qid": "promotion_over_stars", "noul": 0.93, "probabilities": [0.93, 0.07], "confidence": 0.9,
         "samples": [0.95, 0.92, 0.95, 0.9, 0.95], "blind": "agree",
         "rationale": "json-render 的 Jev 仅 compose 路径一笔（③△），pi-warden 三标准全✓ 且唯一有可跑臂——晋级完全按既定尺（热度不折名额，B1/B2/B5 三度同尺）执行，无例外"},
        {"qid": "mirror_dedup", "choice": "原创+指针正确，避免同源代码虚增 3 个浅采覆盖",
         "probabilities": [0.8, 0.06, 0.08, 0.06], "confidence": 0.8,
         "samples": ["原创+指针正确，避免同源代码虚增 3 个浅采覆盖"]*4+["三镜像各占一个浅采名额"], "blind": "agree",
         "rationale": "两镜像 README 自陈'从 tamaratran 移植'，各记浅采会让 259 覆盖数虚高且掩盖真实独立设计数——原创+指针兼顾可追溯与不注水；'全合并丢指针'会丢移植生态这一事实本身"},
        {"qid": "i7_star_anomaly_verdict", "noul": 0.75, "probabilities": [0.75, 0.25], "confidence": 0.7,
         "samples": [0.8, 0.7, 0.85, 0.7, 0.72], "blind": "agree",
         "rationale": "本次判合法有独立佐证（两个第三方库真实引用它为核心、README 互证）故非仅凭星速翻案；但'星速异常≠脚手架'作为一般规律不可推广——脚手架同样可能被引用包装，0.25 留给'此结论依赖镜像互证这一强证据、条件不满足时须回到默认存疑'"},
    ],
    "note": "自写合成样本（对 B4 产物的结构化诊断统计），非任何真实作品",
}

entry_b = {
    "id": "RB4-B-01", "category": "B4 复跑与深读质量",
    "state": "见 b_state",
    "questions": [
        q("promotion_over_stars", "noul",
          "深读名额给 pi-warden(70★) 而非预排序头名 json-render(16,656★)，是否忠于'热度不折名额'的晋级标准？"),
        q("stub_rerun_legitimacy", "choice",
          "用 5 行 stub + loader hook 绕开未安装的 UI 依赖来跑离线臂——这算真复跑吗？",
          options=["算：stub 只触渲染不触判定路径，离线路径真实执行", "不算：改了运行环境就是伪造", "算但应同时跑通 Jev 臂才叫复跑", "该放弃：任何 npm 障碍即视同不可复跑"]),
        q("negative_result_selfdisclose", "noul",
          "pi-warden README 专节列'哪些轴没差异/样本小/仪器与被测同仓'——这种自曝对其深采价值是加分还是减分？"),
        q("mirror_dedup", "choice",
          "compaction 三库同源（两库声明源自 tamaratran），'原创 1 浅采 + 2 指针留矩阵'的处置质价？",
          options=["避免同源代码占三格虚增独立设计数，正确", "三镜像应各占一个浅采名额", "全丢只留 tamaratran", "应合并成只一行"]),
        q("i7_starvelocity_verdict", "score",
          "把 tamaratran(3,682★/1日龄/全压单日) 判'合法新项目'而非脚手架，证据强度？legend: 0=应入预警名单; 1=可判合法但需标'待核'; 2=镜像互证充分可直判合法",
          legend={"0": "应入预警名单", "1": "可判合法但需标'待核'", "2": "镜像互证充分可直判合法"}),
    ],
    "gold": [
        {"qid": "promotion_over_stars", "noul": 0.94, "probabilities": [0.94, 0.06], "confidence": 0.9,
         "samples": [0.95, 0.9, 0.95, 0.92, 0.95], "blind": "agree",
         "rationale": "json-render 16,656★ 但 Jev 仅 compose 一笔、无独立量化面；pi-warden 70★ 却三标准全✓且是唯一可零 key 复跑的护栏库——质价与热度完全倒挂，按'热度不折名额'晋级正是要打破这种倒挂（B1/B2/B5 同尺）"},
        {"qid": "stub_rerun_legitimacy", "choice": "算：stub 只触渲染不触判定路径，离线路径真实执行",
         "probabilities": [0.8, 0.08, 0.06, 0.06], "confidence": 0.8,
         "samples": ["算：stub 只触渲染不触判定路径，离线路径真实执行"]*3 + ["算但应同时跑通 Jev 臂才叫复跑", "算：stub 只触渲染不触判定路径，离线路径真实执行"], "blind": "agree",
         "rationale": "barrel 顶层 import pi-tui 仅为状态栏渲染的 1 个函数，evaluateAction 核心路径不碰它——stub 等于把可选 UI 依赖摸除，离线 4/4 命中文档是真执行；'必跑 Jev 臂才叫复跑'的样本把部分成功当全或无，但 batch04 已明标'单臂+Jev 未验'不属此罪"},
        {"qid": "negative_result_selfdisclose", "noul": 0.9, "probabilities": [0.9, 0.1], "confidence": 0.88,
         "samples": [0.9, 0.92, 0.85, 0.9, 0.93], "blind": "agree",
         "rationale": "'What it does not do yet' 整节自曝无差异轴 + 承认样本 15 任务/2 模型 + 仪器与被测同仓——与 winnow'报 base rate 的裁判什么都能藏'同理，主动交出负面恰恰是不可信宣称的对立面，直接强化深采"},
        {"qid": "mirror_dedup", "choice": "避免同源代码占三格虚增独立设计数，正确",
         "probabilities": [0.8, 0.06, 0.08, 0.06], "confidence": 0.8,
         "samples": ["避免同源代码占三格虚增独立设计数，正确"]*4 + ["应合并成只一行"], "blind": "agree",
         "rationale": "joelhooks/leonaaardob 明写移植自 tamaratran，若各占浅采会虚增'独立设计'数；但'合并成一行'过头——移植版各有宿主差异且矩阵须覆盖全 30 行(DoD-1)，故保留三行、只在原创行记设计点；B3 模板四复发正是缺此纪律"},
        {"qid": "i7_starvelocity_verdict", "score": 1, "probabilities": [0.1, 0.7, 0.2], "confidence": 0.62,
         "samples": [1, 1, 2, 1, 2], "blind": "agree",
         "rationale": "边缘题：两镜像库真实存在且声明源引 tamaratran 构成互证（判 2 的据），但 1 日龄 3,682★ 仍属统计异常，I7 制度下'合法但标待核'更保守——与 B5 partial_vs_full 同类判 1，尺度一致；0.2 分给'互证已足够'的另一读法"},
    ],
    "note": "自写合成样本（对 B4 产物的结构化诊断统计），非任何真实作品",
}

out = root / "eval" / "b4_review.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(entry_a, ensure_ascii=False) + "\n")
    f.write(json.dumps(entry_b, ensure_ascii=False) + "\n")
for i, line in enumerate(out.read_text(encoding="utf-8").splitlines()):
    e = json.loads(line)
    for gg in e["gold"]:
        s = sum(gg["probabilities"])
        assert abs(s - 1.0) <= 0.02 + 1e-9, (i, gg["qid"], s)
        assert gg["blind"] == "agree" and len(gg["samples"]) == 5
    print(e["id"], "gold:", len(e["gold"]), "q:", len(e["questions"]), "probs ok")
print("bytes:", out.stat().st_size)
