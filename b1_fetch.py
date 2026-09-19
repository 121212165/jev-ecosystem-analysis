# -*- coding: utf-8 -*-
"""B1 扫读前置：列清单 + 经 gh-proxy 拉全部 README 落盘 _b1/。"""
import csv, io, os, sys, urllib.request, urllib.error, concurrent.futures as cf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
OUT = os.path.join(BASE, "_b1")
os.makedirs(OUT, exist_ok=True)
PROXIES = ["https://gh-proxy.com/", "https://ghproxy.net/"]

rows = [r for r in csv.DictReader(open(BASE + r"\eval\inventory.csv", encoding="utf-8-sig"))
        if r["batch"] == "B1"]
print(f"B1 rows: {len(rows)}")
for r in sorted(rows, key=lambda x: -int(x["n_lists"])):
    print(f"  {r['n_lists']} {r['assign']:<6} {r['repo']:<48} {r['desc'][:88]}")

def fetch(repo):
    for ref in ("HEAD", "main", "master", "develop"):
        for px in PROXIES:
            url = f"{px}https://raw.githubusercontent.com/{repo}/{ref}/README.md"
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
                with urllib.request.urlopen(req, timeout=25) as resp:
                    data = resp.read()
                if len(data) > 50:
                    fn = os.path.join(OUT, repo.replace("/", "__") + f".md")
                    open(fn, "wb").write(data)
                    return repo, f"OK {ref} {len(data)}B"
            except Exception:
                continue
    return repo, "MISS"

with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for repo, st in ex.map(fetch, [r["repo"] for r in rows]):
        print(f"  [{st}] {repo}")
