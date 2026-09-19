# RB5 前置核账：batch05.md 声明 vs 实数（计数脚本生成纪律）
import collections, pathlib

root = pathlib.Path(r".")
md = (root / "reports" / "batch05.md").read_text(encoding="utf-8")

# 1) 解析 §二 矩阵行
sec = md.split("## 二、")[1].split("**统计核账**")[0]
rows = [l for l in sec.splitlines() if l.strip().startswith("|")]
rows = [r for r in rows if "---" not in r and "处置" not in r]
print("matrix rows:", len(rows))
dispo = collections.Counter()
for r in rows:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]
    d = cells[2]
    if "深采" in d:
        dispo["深采"] += 1
    elif "浅采·要点" in d:
        dispo["浅采·要点"] += 1
    elif "留矩阵·存疑" in d:
        dispo["留矩阵·存疑"] += 1
    elif "留矩阵" in d:
        dispo["留矩阵"] += 1
    else:
        dispo["?" + d] += 1
print(dict(dispo))
print("header ok:", dispo["深采"] == 2 and dispo["浅采·要点"] == 6
      and dispo["留矩阵"] == 10 and dispo["留矩阵·存疑"] == 2 and len(rows) == 18)

# 2) 矩阵内数字对 _b5 原文 spot-check（戒条①）
raw = {p.name: p.read_text(encoding="utf-8", errors="ignore")
       for p in (root / "_b5").glob("*.md")}
checks = [
    ("98.64", "bitnovus__jev-spam-eval.md"),
    ("5,733", "bitnovus__jev-spam-eval.md"),
    ("212", "choxos__jev-reviewer.md"),
    ("88", "choxos__jev-reviewer.md"),
    ("150", "leepokai__jev-guard.md"),
    ("0.75", "leepokai__jev-guard.md"),
    ("39", "coldteadotai__abide.md"),
]
for token, f in checks:
    if f not in raw:
        print(f"{token!r} in {f}: NOFILE")
    else:
        print(f"{token!r} in {f}: {'HIT' if token in raw[f] else 'MISS'}")

sn = raw.get("danrwilloughby__snifftest.md", "")
for tok in ["0.4", "0.6", "not_for", "cache"]:
    print("snifftest", tok, tok in sn)

# 3) §七 承诺的 RB5 产物现状
for rel in ["eval/b5_review.jsonl", "reports/b5_review.md"]:
    p = root / rel
    print(rel, p.exists(), p.stat().st_size if p.exists() else "-")

# 4) analyses 深读档实数
docs = sorted(p.name for p in (root / "analyses").glob("*__*.md"))
print("analyses docs:", len(docs))
for d in docs:
    print("  ", d)

# 5) jev-axi "6 次/条件、均值中位数符号相反" 声明核对
ax = raw.get("shiftynick__jev-axi.md", "")
for tok in ["Six runs", "25%", "29%"]:
    print("jev-axi", tok, tok in ax)
