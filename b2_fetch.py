# -*- coding: utf-8 -*-
"""通用批次拉取+信号提取：python b2_fetch.py B2   （库存 _b2/ 下）"""
import csv, io, os, re, sys, urllib.request, concurrent.futures as cf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BATCH = (sys.argv[1] if len(sys.argv) > 1 else "B2").upper()
BASE = r"."
OUT = os.path.join(BASE, f"_{BATCH.lower()}")
os.makedirs(OUT, exist_ok=True)
PROXIES = ["https://gh-proxy.com/", "https://ghproxy.net/"]

rows = [r for r in csv.DictReader(open(BASE + r"\eval\inventory.csv", encoding="utf-8-sig"))
        if r["batch"] == BATCH]
print(f"{BATCH} rows: {len(rows)}")
for r in sorted(rows, key=lambda x: -int(x["n_lists"])):
    print(f"  {r['n_lists']} {r['assign']:<14} {r['repo']:<46} {r['desc'][:80]}")

def fetch(repo):
    names = ["README.md", "readme.md", "docs/README.md"]
    for name in names:
        for ref in ("HEAD", "main", "master"):
            for px in PROXIES:
                url = f"{px}https://raw.githubusercontent.com/{repo}/{ref}/{name}"
                try:
                    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=25) as r:
                        data = r.read()
                    if len(data) > 50:
                        open(os.path.join(OUT, repo.replace("/", "__") + ".md"), "wb").write(data)
                        return repo, f"OK {ref}/{name.split('/')[0]} {len(data)}B"
                except Exception:
                    continue
    return repo, "MISS"

with cf.ThreadPoolExecutor(max_workers=6) as ex:
    miss = []
    for repo, st in ex.map(fetch, [r["repo"] for r in rows]):
        print(f"  [{st}] {repo}")
        if st == "MISS":
            miss.append(repo)

SIG_CAL = re.compile(r"(calibrat|brier|ECE|\bacc\b|accuracy|agreement|consistent|\d+(\.\d+)?\s*%|0\.\d{2}|\d+\s*ms|\$\d)", re.I)
SIG_ENV = re.compile(r"(pip install|uv |cargo|npm i|npm run|docker|ollama|vllm|mlx|onnx|webgpu)", re.I)
SIG_GATE = re.compile(r"(threshold|confidence|fallback|route|retry|abort|quarantin|gate)", re.I)

for fn in sorted(os.listdir(OUT)):
    if not fn.endswith(".md"):
        continue
    text = open(os.path.join(OUT, fn), encoding="utf-8", errors="replace").read()
    lines = [l.strip() for l in text.splitlines()]
    title = next((l for l in lines if l.startswith("#")), fn)
    cal = [l for l in lines if SIG_CAL.search(l) and not l.startswith("![")][:5]
    gate = [l for l in lines if SIG_GATE.search(l)][:3]
    env = next((l for l in lines if SIG_ENV.search(l)), "")
    lic = next((l for l in lines if re.search(r"licen[cs]e", l, re.I)), "(no license line)")
    print(f"\n===== {fn[:-3]}  ({len(text)}B)")
    print(f"  T: {title[:100]}")
    print(f"  LIC: {lic[:80]}")
    for l in cal: print(f"  CAL: {l[:150]}")
    for l in gate: print(f"  GATE: {l[:140]}")
    if env: print(f"  ENV: {env[:100]}")
