# -*- coding: utf-8 -*-
"""批量存在性验证：对 inventory.csv 全部 repo 经 gh-proxy 做 HEAD 探测。
输出 eval/existence.csv (repo, status)。非 200/301/302/307/404 的标 unknown 需人工看。"""
import csv, io, sys, urllib.request, urllib.error, concurrent.futures as cf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
INV, OUT = BASE + r"\eval\inventory.csv", BASE + r"\eval\existence.csv"

def head(repo):
    url = f"https://gh-proxy.com/https://github.com/{repo}"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "curl/8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return repo, r.status
    except urllib.error.HTTPError as e:
        return repo, e.code
    except Exception:
        try:  # 重试一次，代理偶发抖动
            with urllib.request.urlopen(req, timeout=25) as r:
                return repo, f"{r.status}R"
        except urllib.error.HTTPError as e:
            return repo, f"{e.code}R"
        except Exception as e2:
            return repo, f"ERR:{type(e2).__name__}"

rows = list(csv.DictReader(open(INV, encoding="utf-8-sig")))
repos = [r["repo"] for r in rows]
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(head, repos))

with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["repo", "status"])
    w.writerows(results)

from collections import Counter
c = Counter(str(s) for _, s in results)
print("status counts:", dict(c))
bad = [r for r, s in results if str(s) not in ("200", "301", "302", "307", "200R")]
print("non-OK repos:", len(bad))
for r, s in [(r, s) for r, s in results if str(s) not in ("200", "301", "302", "307", "200R")][:40]:
    print("  ", r, s)
