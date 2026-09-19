# RB4 前置核账：batch04.md 声明 vs 实数（先脚本后定稿）
import collections, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(r".")
md = (root / "reports" / "batch04.md").read_text(encoding="utf-8")

sec = md.split("## 二、")[1].split("## 三、")[0]
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
print(dict(dispo), "sum:", sum(dispo.values()))

raw = {p.name: p.read_text(encoding="utf-8", errors="ignore") for p in (root / "_b4").glob("*.md")}
print("_b4 files:", len(raw))
checks = [
    ("150 paired", "devmortimer__pi-warden.md"), ("17,160", "devmortimer__pi-warden.md"),
    ("42", "devmortimer__pi-warden.md"), ("13,952", "devmortimer__pi-warden.md"),
    ("40/42", "agent-labs-dev__fastbrowse.md"), ("14/42", "agent-labs-dev__fastbrowse.md"),
    ("$0.0002", "awlevin__typesafe-computer-use.md"), ("155", "awlevin__typesafe-computer-use.md"),
    ("0.55", "shitianfang__wakegate.md"), ("0.85", "jkudish__jev-browser.md"),
    ("minReduction", "tamaratran__fast-jev-compaction.md"), ("0.25", "tamaratran__fast-jev-compaction.md"),
    ("not independent proof", "droidrun__mobile-jev.md"), ("reserveFloor", "nidhi-singh02__agent-router.md"),
    ("30 candidates", "realzachi__typesafe-adblock.md"), ("7,607", "silbercue__public-browser.md"),
]
for token, f in checks:
    status = "NOFILE" if f not in raw else ("HIT" if token.lower() in raw[f].lower() else "MISS")
    print(f"{token!r} in {f}: {status}")
