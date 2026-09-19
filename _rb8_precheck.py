# -*- coding: utf-8 -*-
"""B8 前置核账（承 B7 教训：矩阵须与权威元数据池行级 diff）：
 (1) 解析 batch08 §二 处置列 → Counter + rows，核对 rows == POOL(68)；
 (2) 行级 diff：矩阵 slug 集 vs _b8_meta.txt slug 集 → 报幻影(矩阵有元数据无)/漏库(元数据有矩阵无)；
 (3) 数字 token → 声称来源文件 反查（防张冠李戴/臆造）；
 (4) 文件体积事实走 getsize（十进制 KB）。
"""
import io, os, re, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
REP = os.path.join(BASE, "reports", "batch08.md")
SRC = os.path.join(BASE, "_b8")
META = os.path.join(BASE, "_b8_meta.txt")
POOL = 68
VALID = {"深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"}

text = open(REP, encoding="utf-8").read()

# ---------- (1) 处置列 Counter ----------
disp = Counter(); rows = 0; bad = []; matrix_slugs = []
for line in text.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) < 3:
        continue
    col0 = cells[0]
    if col0.startswith("库") or set(col0) <= set("-: ") or col0 == "":
        continue
    slug = re.sub(r"\*+", "", col0).split()[0].strip("`*")
    matrix_slugs.append(slug)
    d = re.sub(r"\*+", "", cells[2]).strip()
    if d not in VALID:
        bad.append((slug, d)); continue
    disp[d] += 1; rows += 1

print("=== (1) 处置列 Counter ===")
for k in ["深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"]:
    if disp.get(k, 0):
        print(f"  {k:10s} {disp.get(k,0)}")
print(f"  合计行数 = {rows} | 声明池 = {POOL} | header ok: {rows == POOL}")
if bad:
    print("  !! 非法处置值：", bad)

# ---------- (2) 行级 diff vs 元数据池 ----------
meta_slugs = []
for ml in open(META, encoding="utf-8", errors="replace"):
    ml = ml.strip()
    if not ml:
        continue
    meta_slugs.append(ml.split()[-1])
mset, sset = set(meta_slugs), set(matrix_slugs)
phantom = sorted(sset - mset)          # 矩阵有、元数据无 → 幻影
missing = sorted(mset - sset)          # 元数据有、矩阵无 → 漏库
print("\n=== (2) 行级 diff（矩阵 vs _b8_meta）===")
print(f"  元数据 slug {len(meta_slugs)}（唯一 {len(mset)}）| 矩阵 slug {len(matrix_slugs)}（唯一 {len(sset)}）")
print(f"  幻影(矩阵有/池无): {phantom if phantom else '无'}")
print(f"  漏库(池有/矩阵无): {missing if missing else '无'}")

# ---------- (3) 数字 token → 源文件反查 ----------
def core(t):
    return t[2:] if t.startswith("0.") else t

MAP = {
    "yodablocks__jev-orderby-bench.md": ["0.036", "0.143", "0.016", "360"],
    "jourdanlabs__assay-001.md": ["0.0204", "0.0936"],
    "gaurav-gosain__jev-sec-bench.md": ["96.5", "662", "263", "95.1"],
    "firassx914__janus.md": ["0.67", "80.2", "77.8"],
    "iamvatsalpatel__tiershift.md": ["13.23", "7.95", "4.77"],
    "ikermoel__open-alternative-jev.md": ["0.90", "0.84", "92.6"],
    "qkal__canny.md": ["0.05"],
    "owner-A__jev-curate.md": ["15,000", "50,000"],
    "nekuda-ai__windtunnel.md": ["3,087"],
    "noelzappy__tripwire.md": ["0.85", "0.80"],
    "stephanj__parallelconstraintdecoding.md": ["1.34", "2388"],
    "theoleecj__semif.md": ["20.03"],
    "vinnylarouge__jevlike.md": ["98"],
    "santos-sanz__jev-audio-beeper.md": ["0.72"],
    "sufianetaouil__every.md": ["1,842"],
    "teyhouse__jev-secret-detection.md": ["0.25"],
    "sosopop__jev_stock.md": ["0.68"],
    "skyvern-ai__jevscape.md": ["0.17"],
    "reachjalil__jev-tree.md": ["320", "255"],
    "realzachi__pg-jev.md": ["2,000", "0.012"],
    "supercorp-ai__supercov.md": ["96"],
    "devagrawal09__jev-code.md": ["0.0.1"],
    "kevthetech143__super-jev.md": ["0.80"],
}
print("\n=== (3) 数字 token → 源文件反查 ===")
hit = 0; miss = []
for fn, toks in MAP.items():
    p = os.path.join(SRC, fn)
    if not os.path.exists(p):
        print(f"  [NOFILE] {fn}"); miss.append((fn, "<no file>")); continue
    body = open(p, encoding="utf-8", errors="replace").read()
    for t in toks:
        if (t in body) or (core(t) in body and len(core(t)) >= 2):
            hit += 1
        else:
            print(f"  [MISS] {t!r} not in {fn}"); miss.append((fn, t))
print(f"  token 命中 {hit} / {hit + len(miss)} | MISS {len(miss)}")

# ---------- (4) 体积事实 ----------
SIZE_FACTS = [("dabit3__jev-experiments.md", 0)]  # KB 下取整=0（266B<500B）
print("\n=== (4) 体积事实（KB，getsize）===")
size_bad = []
for fn, kb in SIZE_FACTS:
    p = os.path.join(SRC, fn)
    actual = int(os.path.getsize(p) // 1000) if os.path.exists(p) else -1
    ok = actual == kb
    print(f"  {fn}: 声称 {kb}KB(≈) / 实测 {actual}KB ({os.path.getsize(p) if os.path.exists(p) else '?'}B)  {'OK' if ok else 'MISMATCH'}")
    if not ok:
        size_bad.append(fn)

gate = (rows == POOL) and not bad and not phantom and not missing and not miss and not size_bad
print("\n=== 判定 ===")
print("header ok:", rows == POOL, "| 处置合法:", not bad, "| 幻影:", not phantom, "| 漏库:", not missing,
      "| token 全 HIT:", not miss, "| 体积:", not size_bad)
print("GATE:", "PASS ✅" if gate else "FAIL ❌（按上面 MISS/幻影/漏库定位后回改报告，勿先改脚本迁就）")
