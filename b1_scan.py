# -*- coding: utf-8 -*-
"""B1 扫读信号提取：从 _b1/*.md 抓标题/量化校准/规模/安装/中文能力等关键行。"""
import io, os, re, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = r"."
OUT = os.path.join(BASE, "_b1")

# 补拉两个 MISS 的常见替代文件名
for repo in ("alexwortega/openjev", "drinkmoonshine/parallel-constrained-decoding"):
    fn = os.path.join(OUT, repo.replace("/", "__") + ".md")
    for name in ("readme.md", "README.MD", "Readme.md", "README", "docs/README.md"):
        got = False
        for ref in ("HEAD", "main", "master"):
            url = f"https://gh-proxy.com/https://raw.githubusercontent.com/{repo}/{ref}/{name}"
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=20) as r:
                    data = r.read()
                if len(data) > 50:
                    open(fn, "wb").write(data)
                    print(f"[recovered {ref}/{name} {len(data)}B] {repo}")
                    got = True
                    break
            except Exception:
                continue
        if got:
            break
    else:
        print(f"[still-miss] {repo}")

SIG_CAL = re.compile(r"(calibrat|brier|ECE|\bacc\b|accuracy|agreement|\d+(\.\d+)?\s*%|0\.\d{2})", re.I)
SIG_ENV = re.compile(r"(pip install|uv |cargo|npm i|docker|ollama|vllm|mlx|onnx|webgpu)", re.I)
SIG_ZH  = re.compile(r"(chinese|中文|bilingual|双语|mandarin|multilingual|japanese)", re.I)
SIG_W   = re.compile(r"(huggingface\.co|weights|checkpoint|\d+(\.\d+)?B\b|\d{3,4}M\b)", re.I)

for fn in sorted(os.listdir(OUT)):
    if not fn.endswith(".md"):
        continue
    text = open(os.path.join(OUT, fn), encoding="utf-8", errors="replace").read()
    lines = [l.strip() for l in text.splitlines()]
    title = next((l for l in lines if l.startswith("#")), fn)
    stars = text.count("★")
    cal = [l for l in lines if SIG_CAL.search(l) and not l.startswith("!")][:4]
    env = next((l for l in lines if SIG_ENV.search(l)), "")
    zh = [l for l in lines if SIG_ZH.search(l)][:2]
    wgt = [l for l in lines if SIG_W.search(l)][:2]
    lic = next((l for l in lines if re.search(r"licen[cs]e", l, re.I)), "(no license line)")
    print(f"\n===== {fn[:-3]}  ({len(text)}B)")
    print(f"  T: {title[:100]}")
    print(f"  LIC: {lic[:80]}")
    for l in cal: print(f"  CAL: {l[:150]}")
    if env: print(f"  ENV: {env[:100]}")
    for l in zh: print(f"  ZH : {l[:110]}")
    for l in wgt: print(f"  WGT: {l[:110]}")
