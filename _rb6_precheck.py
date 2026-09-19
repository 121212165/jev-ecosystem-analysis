# -*- coding: utf-8 -*-
"""B6 前置核账：
 (1) 解析 batch06 §二 矩阵处置列 → Counter，供头部回填；
 (2) 数字 token → 声称来源文件 反查（每个 token 必须在指定 _b6 源文件里出现，否则 MISS=可能张冠李戴）。
"""
import io, os, re, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
REP = os.path.join(BASE, "reports", "batch06.md")
SRC = os.path.join(BASE, "_b6")

text = open(REP, encoding="utf-8").read()

# (1) 解析矩阵处置列
disp = Counter()
rows = 0
for line in text.splitlines():
    if line.startswith("|") and line.count("|") >= 5:
        cells = [c.strip() for c in line.strip("|").split("|")]
        lib = cells[0]
        if lib in ("库（★/lic）", "---") or set(lib) <= set("-: "):
            continue
        if "①复跑" in lib or not lib or lib.startswith("S-B6"):
            continue
        d = cells[2]
        if "深采" in d or "浅采" in d or "留矩阵" in d or "丢弃" in d or "移批" in d:
            disp[d.replace("**", "")] += 1
            rows += 1
print("== 矩阵处置 Counter ==")
for k, v in sorted(disp.items(), key=lambda x: -x[1]):
    print(f"  {v:>2}  {k}")
print(f"  合计 {rows} 行")
expect = 14
print(f"  header ok: {rows == expect}  (期望 {expect})")

# (2) token → 来源文件 反查
def src_text(name):
    p = os.path.join(SRC, name)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""

CHECKS = [
    # (token, 源文件, 说明)
    ("261",    "kyotofin__tax-doc-classifier.md", "261 IRS forms"),
    ("314",    "kyotofin__tax-doc-classifier.md", "bench pages"),
    ("5.05",   "kyotofin__tax-doc-classifier.md", "blank strict err%"),
    ("34×",    "kyotofin__tax-doc-classifier.md", "34x cheaper"),
    ("0.95",   "kyotofin__tax-doc-classifier.md", "gate"),
    ("60 %",   "0xnatoshi__jev-codex-router.md", "头条 savings≈60%"),
    ("80%",    "0xnatoshi__jev-codex-router.md", "naive 全前沿吞 80%（另一码事）"),
    ("0.00003","0xnatoshi__jev-codex-router.md", "决策成本"),
    ("19.53",  "adarshmishra07__jcm-router.md", "净亏$"),
    ("106.73", "adarshmishra07__jcm-router.md", "花$"),
    ("87.19",  "adarshmishra07__jcm-router.md", "基线$"),
    ("309",    "adarshmishra07__jcm-router.md", "requests"),
    ("94.4",   "godsboy__jev-agent-skill-router.md", "68/72"),
    ("70.8",   "godsboy__jev-agent-skill-router.md", "51/72 lexical"),
    ("64/72",  "godsboy__jev-agent-skill-router.md", "未改切分"),
    ("1,287",  "godsboy__jev-agent-skill-router.md", "median latency"),
    ("49",     "codealive-ai__mastra-jev-moderation.md", "0/49"),
    ("920",    "codealive-ai__mastra-jev-moderation.md", "tokens/call"),
    ("0.7",    "codealive-ai__mastra-jev-moderation.md", "threshold"),
    ("0.59",   "abovecolin__ha-jev.md", "degraded 置信"),
    ("0.46",   "abovecolin__ha-jev.md", "confidence"),
    ("20 ms",  "gtaras7__typesafe-jev.md", "重评零成本"),
    ("192,000","mejiasd3v__pi-jev-router.md", "byte cap"),
    ("10 to 100", "brainstormity__jev-moderation-bot.md", "profile 扫消息数"),
]
print("\n== 数字 token → 来源文件 反查 ==")
miss = 0
for tok, f, note in CHECKS:
    hit = tok in src_text(f)
    if not hit:
        miss += 1
    print(f"  {'HIT ' if hit else 'MISS'}  '{tok}'  <- {f}  ({note})")
print(f"\nMISS 合计: {miss}")

# (3) 头条防错断言：矩阵里写 0xnatoshi 时必须是 60 不是把 80 当头条
sec = text
warn = ""
if re.search(r"省[^0-9]{0,4}80\s*%", sec):
    warn += "  ⚠ 正文疑似把 80% 写成'省'的头条（应为 60%）\n"
if "省 ~60%" not in sec and "头条**省 ~60%**" not in sec and "省 ~60%（非" not in sec:
    warn += "  ⚠ 未找到 '省 ~60%' 头条表述\n"
print("\n== 头条防错 ==")
print(warn.strip() or "  ok：0xnatoshi 头条=60%，80% 已限定为次要")
