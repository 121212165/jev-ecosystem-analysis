# -*- coding: utf-8 -*-
"""B7 前置核账（先脚本后文档）：
 (1) 解析 batch07 §二 矩阵处置列 → Counter，供头部回填，并核对总数 == 声明池 61；
 (2) 数字 token → 声称来源文件 反查（每 token 必须在指定 _b7 源文件出现，否则 MISS=可能张冠李戴/臆造）。
容忍格式差：token 支持字面量 或 去前导"0."的数字核（如 0.396 亦可命中 .396/396）。
"""
import io, os, re, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
REP = os.path.join(BASE, "reports", "batch07.md")
SRC = os.path.join(BASE, "_b7")
POOL = 61

text = open(REP, encoding="utf-8").read()

# ---------- (1) 解析矩阵处置列 ----------
VALID = {"深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"}
disp = Counter()
rows = 0
bad_disp = []
for line in text.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) < 3:
        continue
    lib, d = cells[0], re.sub(r"\*+", "", cells[2]).strip()
    if lib.startswith("库") or set(lib) <= set("-: ") or lib == "":
        continue
    if d not in VALID:
        # 允许处置列带尾注（如 "浅采·要点 "），已在 strip；若仍非法记录
        bad_disp.append((lib, d))
        continue
    disp[d] += 1
    rows += 1

print("=== (1) 处置列 Counter ===")
for k in ["深采", "浅采·要点", "浅采", "留矩阵", "留矩阵·存疑", "丢弃"]:
    if disp.get(k, 0):
        print(f"  {k:8s} {disp.get(k,0)}")
print("  合计行数 =", rows, "| 声明池 =", POOL, "| header ok:", rows == POOL)
if bad_disp:
    print("  !! 非法处置值：", bad_disp)

# ---------- (2) 数字 token → 源文件反查 ----------
# (slug_file, display, probe)  probe 为容忍核（去前导 0.）
def core(tok):
    return tok[2:] if tok.startswith("0.") else tok

MAP = {
    "wiktorb2004__llama-index-jev.md": ["0.396", "0.056", "0.042", "0.072"],
    "nyarlathoteppppp__pi-heed.md": ["71.4", "97.6", "16.3", "139"],
    "nyarlathoteppppp__pi-jev-context.md": ["265", "96"],
    "inanna-malick__jev-dsl.md": ["0.78", "0.17", "0.74"],
    "kylemclaren__jevql.md": ["129", "82"],
    "jkudish__jev-mcp.md": ["0.75", "0.25"],
    "devmortimer__pi-typesafe.md": ["0.36"],
    "jomatsu__zod-jev.md": ["0.87"],
    "brainwires__jevwire.md": ["0.85", "0.88", "0.93"],
    "y0usaf__pi-jev.md": ["300"],
    "theooliveira__pi-jev.md": ["0.65"],
    "ilkerulusoy__pi-jev-compact.md": ["0.25", "15.5", "33.5"],
    "kevinpita__pi-jev-context.md": ["0.8"],
    "hyunjunjeon__pi-quiet-ask.md": ["120", "250"],
    "giuliosmall__pg_typesafe.md": ["0.86"],
    "blakestone-x__jev-mcp.md": ["200", "0.42", "95"],
    "stumble__jev-go.md": ["85"],
    "rajivkuriakose__typesafe-jev-examples.md": ["0.60"],
    "mizchi__jev-gomoku.md": ["0.0024"],
}

print("\n=== (2) 数字 token → 源文件反查 ===")
miss = []
hit = 0
for fn, toks in MAP.items():
    path = os.path.join(SRC, fn)
    if not os.path.exists(path):
        print(f"  [NOFILE] {fn}")
        miss.append((fn, "<no file>", ""))
        continue
    body = open(path, encoding="utf-8", errors="replace").read()
    for t in toks:
        ok = (t in body) or (core(t) in body and len(core(t)) >= 2)
        if ok:
            hit += 1
        else:
            print(f"  [MISS] {t!r} not in {fn}")
            miss.append((fn, t, ""))
print(f"  token 命中 {hit} / {hit+len(miss)}  |  MISS {len(miss)}")

# ---------- (3) 文件体积事实（README 膨胀宣称，走 getsize 非 body grep） ----------
# (slug_file, 声称KB)
SIZE_FACTS = [("dicklesworthstone__skillranker.md", 113)]
print("\n=== (3) 文件体积事实（KB，getsize 核） ===")
size_bad = []
for fn, kb in SIZE_FACTS:
    p = os.path.join(SRC, fn)
    actual = round(os.path.getsize(p) / 1000) if os.path.exists(p) else -1  # 十进制 KB（与 GitHub/fetch 日志一致）
    ok = actual == kb
    print(f"  {fn}: 声称 {kb}KB / 实测 {actual}KB  {'OK' if ok else 'MISMATCH'}")
    if not ok:
        size_bad.append(fn)

gate = (rows == POOL) and not bad_disp and not miss and not size_bad
print("\n=== 判定 ===")
print("header ok:", rows == POOL, "| 处置合法:", not bad_disp, "| token 全 HIT:", not miss, "| 体积事实:", not size_bad)
print("GATE:", "PASS ✅" if gate else "FAIL ❌（按上面 MISS/非法项定位后回改报告，勿先改脚本迁就）")
