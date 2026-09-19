# -*- coding: utf-8 -*-
"""FINAL 全战役核账（R7-a 放大到 259 规模）：
 (1) inventory.csv 全局：259 行、slug 去重、每库唯一 batch 归属；
 (2) 覆盖门（DoD-1）：每个 inventory 库的 slug 是否出现在其批次报告文本中（大小写归一）；
 (3) 各批次报告矩阵处置列 Counter 汇总（跨批总量：深采/浅采·要点/浅采/留矩阵/存疑/丢弃）；
 (4) 幻影：报告矩阵 col0 出现的 owner/repo 但不在全局 inventory（防臆造/串批）。
"""
import io, os, re, sys, csv
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
INV = os.path.join(BASE, "eval", "inventory.csv")

# ---------- (1) inventory ----------
rows = list(csv.DictReader(open(INV, encoding="utf-8-sig")))
inv_batch = defaultdict(set)   # batch -> set(lower slug)
all_slugs = []
for r in rows:
    slug = r["repo"].strip()
    b = r["batch"].strip()
    inv_batch[b].add(slug.lower())
    all_slugs.append(slug.lower())
glob_set = set(all_slugs)
print("=== (1) inventory 全局 ===")
print(f"  行数 {len(rows)} | 唯一 slug {len(glob_set)} | 重复 {len(rows)-len(glob_set)}")
dupes = [s for s, n in Counter(all_slugs).items() if n > 1]
print(f"  重复 slug: {dupes if dupes else '无'}")
per = {b: len(v) for b, v in sorted(inv_batch.items())}
print(f"  每批池: {per}  | 合计 {sum(per.values())}")

# ---------- (2) 覆盖门 ----------
print("\n=== (2) DoD-1 覆盖门（每库须现于其批次报告）===")
report_of = {b: os.path.join(BASE, "reports", f"batch{int(b[1:]):02d}.md") for b in inv_batch}
total_missing = []
for b, slugs in sorted(inv_batch.items()):
    rp = report_of[b]
    if not os.path.exists(rp):
        print(f"  [NOREPORT] {b} -> {rp}"); continue
    text = open(rp, encoding="utf-8", errors="replace").read().lower()
    miss = [s for s in slugs if s not in text]
    print(f"  {b}: 池 {len(slugs)} | 命中 {len(slugs)-len(miss)} | 缺 {len(miss)} {miss if miss else ''}")
    total_missing += [(b, s) for s in miss]
print(f"  全战役覆盖缺口的库: {len(total_missing)}  {total_missing if total_missing else '（0，259/259 全覆盖）'}")

# ---------- (3) 处置列 Counter 汇总 ----------
VALID = {"深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"}
print("\n=== (3) 各批处置列 Counter（矩阵 col0→col_处置）===")
grand = Counter()
for b in sorted(inv_batch):
    rp = report_of.get(b)
    if not rp or not os.path.exists(rp):
        continue
    disp = Counter(); n_rows = 0
    for line in open(rp, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        c0 = re.sub(r"\*+", "", cells[0]).strip()
        # 处置列位置：库/★/①②③/处置/依据 → col2 或 col3，视批表头
        cand = [re.sub(r"\*+", "", c).strip() for c in cells]
        d = next((c for c in cand if c in VALID), None)
        if d is None or c0.startswith("库") or c0.startswith("候选") or set(c0) <= set("-: "):
            continue
        disp[d] += 1; n_rows += 1
    grand += disp
    top = disp.most_common()
    print(f"  {b}: 矩阵行≈{n_rows} | " + " ".join(f"{k}={v}" for k, v in sorted(disp.items())))
print("  —— 全战役处置总计 ——")
for k in ["深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"]:
    if grand.get(k, 0):
        print(f"    {k:10s} {grand.get(k,0)}")
print(f"    合计处置行 {sum(grand.values())}（注：B0 为目录/通道批，矩阵口径异于 B1–B8）")

# ---------- (4) 幻影 ----------
print("\n=== (4) 幻影扫描（矩阵 col0 有 slug 但不在全局 inventory）===")
slug_re = re.compile(r"^[|]\s*`?\*?([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)")
phantom = []
for b in sorted(inv_batch):
    rp = report_of.get(b)
    if not rp or not os.path.exists(rp):
        continue
    for line in open(rp, encoding="utf-8", errors="replace"):
        m = slug_re.match(line.rstrip("\n"))
        if m:
            s = m.group(1).lower()
            if s not in glob_set:
                phantom.append((b, s))
# 过滤明显的非库 token（含斜杠但非 repo，如通道 URL 已不以 | 开头）
phantom = [p for p in phantom if "http" not in p[1] and "github" not in p[1] and "jsdelivr" not in p[1]]
print(f"  幻影 col0 slug: {phantom if phantom else '无'}")
