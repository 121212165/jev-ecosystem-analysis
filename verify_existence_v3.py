# -*- coding: utf-8 -*-
"""存在性验证 v3：主通道 jsDelivr CDN（直连、无限流、大小写不敏感、真 404）；
jsd 双分支 404 的走 gh-proxy API 复核（无 README 的真库会假阴性，必须兜底）。
正负对照先行，不合格中止。结果 eval/existence_v3.csv"""
import csv, io, json, sys, time, urllib.request, urllib.error
import concurrent.futures as cf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
UA = {"User-Agent": "curl/8"}

def get_status(url, timeout=20):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            r.read(64)
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

def jsd(repo):
    for br in ("main", "master"):
        s = get_status(f"https://cdn.jsdelivr.net/gh/{repo}@{br}/README.md")
        if s == 200:
            return "EXIST_README"
        if s == 0:
            time.sleep(2)
            s2 = get_status(f"https://cdn.jsdelivr.net/gh/{repo}@{br}/README.md")
            if s2 == 200:
                return "EXIST_README"
    return None  # jsd 不定论 → API 兜底

def api(repo):
    for i in range(4):
        s = get_status("https://gh-proxy.com/https://api.github.com/repos/" + repo, timeout=25)
        if s == 200:
            return "EXIST_API"
        if s == 404:
            return "MISSING"
        time.sleep(6 + 10 * i)
    return "UNKNOWN"

# ---- 通道自检 ----
ctrl = {r: (jsd(r) or api(r)) for r in
        ["romanslack/jev-drone", "bogus99887711zz/nonexistent-repo-xyz", "tests/test_decision_policies"]}
print("controls:", ctrl, flush=True)
if ctrl["romanslack/jev-drone"] not in ("EXIST_README", "EXIST_API") or \
   ctrl["bogus99887711zz/nonexistent-repo-xyz"] != "MISSING":
    print("CONTROL FAILED"); sys.exit(1)

rows = [r["repo"] for r in csv.DictReader(open(BASE + r"\eval\inventory.csv", encoding="utf-8-sig"))]

def check(repo):
    st = jsd(repo)
    return repo, st or api(repo)

out = []
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for i, (repo, st) in enumerate(ex.map(check, rows)):
        out.append((repo, st))
        if i % 25 == 0:
            print(f"{i+1}/{len(rows)} ...", flush=True)

from collections import Counter
cnt = Counter(s for _, s in out)
with open(BASE + r"\eval\existence_v3.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["repo", "status"]); w.writerows(sorted(out))
print("DONE", len(out), dict(cnt), flush=True)
for tag in ("MISSING", "UNKNOWN"):
    lst = [r for r, s in out if s == tag]
    print(tag, lst)
