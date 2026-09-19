# -*- coding: utf-8 -*-
"""B0 产物诊断统计：给 b0_review 评估条目提供结构化证据。"""
import csv, io, sys, re
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
INV = r".\eval\inventory.csv"
rows = list(csv.DictReader(open(INV, encoding="utf-8-sig")))

stats = {}
stats["total"] = len(rows)

# 1) desc 覆盖率
no_desc = [r for r in rows if not r["desc"] or r["desc"].startswith("PLAN 点名")]
stats["desc_missing"] = len(no_desc)
stats["desc_missing_repos"] = [r["repo"] for r in no_desc]

# 2) 关键词误伤检查：test 子串、sim 子串（similar）、gate 子串（aggregate）、skill 在句中
susp = []
for r in rows:
    repo = r["repo"]
    name = repo.split("/", 1)[1]
    if r["assign"] == "keyword":
        for w in ("test", "sim", "gate", "check", "commit", "diff", "rank", "rank", "buy", "sell"):
            if w in name and not re.search(rf"(^|[-_]){w}($|[-_])", name):
                susp.append((repo, r["batch"], w, name))
stats["substring_suspects"] = susp[:20]
stats["substring_suspect_count"] = len(susp)

# 3) B1/B2/B3 池子 vs 深读名额
cap = {"B1": 3, "B2": 2, "B3": 2, "B5": 1}
for b, c in cap.items():
    n = sum(1 for r in rows if r["batch"] == b)
    stats[f"pool_{b}"] = n
    stats[f"cap_{b}"] = c

# 4) 单源且低交叉验证占比（单源风险）
single = [r for r in rows if int(r["n_lists"]) == 1]
stats["single_source"] = len(single)
stats["single_source_pct"] = round(len(single) / len(rows), 3)
per_src = Counter(r["in_lists"] for r in single)
stats["single_by_source"] = dict(per_src)

# 5) 存在性验证状态：0 验证过
stats["existence_verified"] = 0

# 6) 高 owner_repos 预警中官方/正常混入
warn = sorted({r["repo"].split("/")[0] for r in rows if int(r["owner_repos"]) >= 3})
stats["warn_owners"] = warn

# 7) desc 质量抽样：超长截断/无意义
short_desc = [r for r in rows if r["desc"] and len(r["desc"]) < 25]
stats["desc_short"] = len(short_desc)

# 8) unclassified→B8 的数量（复分类债）
stats["unclassified"] = sum(1 for r in rows if r["assign"] == "unclassified→B8")

import json
print(json.dumps(stats, ensure_ascii=False, indent=1))
