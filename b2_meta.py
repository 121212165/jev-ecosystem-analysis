# -*- coding: utf-8 -*-
"""通用批次元数据：stars/pushed_at/created_at/archived（api.github.com 双代理重试）"""
import csv, io, json, os, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BATCH = (sys.argv[1] if len(sys.argv) > 1 else "B2").upper()
BASE = r"."
PROXIES = ["https://gh-proxy.com/", "https://ghproxy.net/"]

rows = [r["repo"] for r in csv.DictReader(open(BASE + r"\eval\inventory.csv", encoding="utf-8-sig"))
        if r["batch"] == BATCH]

def meta(repo):
    for attempt in range(3):
        for px in PROXIES:
            try:
                req = urllib.request.Request(px + "https://api.github.com/repos/" + repo,
                                             headers={"User-Agent": "curl/8", "Accept": "application/vnd.github+json"})
                with urllib.request.urlopen(req, timeout=25) as r:
                    d = json.load(r)
                return (f"{d.get('stargazers_count', 0):>5}* {d.get('pushed_at','')[:10]} "
                        f"created={d.get('created_at','')[:10]} arch={d.get('archived')} lic={(d.get('license') or {}).get('spdx_id')}")
            except Exception:
                time.sleep(1.5)
    return "META-FAIL"

for repo in rows:
    print(f"{meta(repo)}  {repo}")
