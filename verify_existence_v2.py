# -*- coding: utf-8 -*-
"""存在性验证 v2：api.github.com/repos/<r> 经 gh-proxy，404/200 可判别（v1 的 github.com 页面 HEAD 是假通道）。
先跑正负对照证明通道判别力，不合格即中止；全量结果写 eval/existence_v2.csv"""
import csv, io, json, os, sys, time, urllib.request, urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
PX = "https://gh-proxy.com/"

def probe(repo, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(PX + "https://api.github.com/repos/" + repo,
                                         headers={"User-Agent": "curl/8", "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            return "EXIST", d.get("full_name", "")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "MISSING", ""
            if e.code in (403, 429):
                time.sleep(8 + 12 * i); continue
            time.sleep(3 + 3 * i)
        except Exception:
            time.sleep(3 + 3 * i)
    return "UNKNOWN", ""

# 通道自检：真库必须 EXIST、假库必须 MISSING，否则整个验证无意义
s_real, _ = probe("romanslack/jev-drone")
s_fake, _ = probe("bogus99887711zz/nonexistent-repo-xyz")
print(f"control: real={s_real} fake={s_fake}")
if s_real != "EXIST" or s_fake != "MISSING":
    print("CONTROL FAILED — 通道无判别力，中止"); sys.exit(1)

rows = [r["repo"] for r in csv.DictReader(open(BASE + r"\eval\inventory.csv", encoding="utf-8-sig"))]
out = []
for i, repo in enumerate(rows):
    st, fn = probe(repo)
    out.append((repo, st, fn))
    if st != "EXIST" or i % 20 == 0:
        print(f"[{i+1}/{len(rows)}] {st:8} {repo}")
    time.sleep(0.6)

with open(BASE + r"\eval\existence_v2.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["repo", "status", "full_name"]); w.writerows(out)
from collections import Counter
print("DONE:", dict(Counter(s for _, s, _ in out)), "of", len(out))
print("MISSING:", [r for r, s, _ in out if s == "MISSING"])
print("UNKNOWN:", [r for r, s, _ in out if s == "UNKNOWN"])
