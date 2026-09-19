# -*- coding: utf-8 -*-
"""B0 目录合并器：5 份 awesome 目录 + PLAN.md 批次归位 → eval/inventory.csv
规则：
1) 抽 owner/repo（github 链接与 owner/repo 裸引用），统一小写；
2) 批次：先按 PLAN.md 各 B 节显式名单归位，再按关键词规则，最后未分类；
3) 脚手架预警：同一 owner 名下 ≥3 库 → bulk_siblings 计数（对齐风险条款）。"""
import re, csv, io, sys
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

D = Path(r".")
YIBIE_CATS = ["agent-decisions", "calibration-research", "classification-routing", "compliance-legal",
              "content-moderation", "data-labeling-curation", "evaluation-benchmarking", "finance-trading",
              "game-simulation", "infra-sdks-integrations", "related-practices-discussions",
              "scientific-pipelines", "scoring-ranking", "verification-guardrails"]
LISTS = [("yibie", "_raw_yibie.md")] + [("yibie", f"_raw_yibie_cat_{c}.md") for c in YIBIE_CATS] + [
    ("anotiawang", "_raw_anotiawang.md"), ("cobanov", "_raw_cobanov.md"),
    ("owner-B", "_raw_owner-B.md"), ("anilmatcha", "_raw_anilmatcha.md")]

GH_LINK = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+?)(?:\.git)?(?:[)/#\s\"'<>]|$)")
# v3：大小写不敏感，但要求后接列表条目语境（可选空格+分隔符），排除散文中 Chinese/English 类短语
BARE = re.compile(r"(?<![\w/.-])([A-Za-z0-9][\w.-]{0,37}[A-Za-z0-9])/([A-Za-z0-9][\w.-]{1,56}[A-Za-z0-9])(?![\w-])\s*(?=[-\u2013\u2014:+.\u3001\uff0c\uff1a\uff08(\u3002)\[|])", re.I)
STOP_WORDS = {"chinese", "english", "korean", "japanese", "french", "spanish", "choice", "score", "noul",
              "code", "codex", "html", "csv", "json", "yaml", "europe", "istanbul", "once", "run",
              "log", "api", "app", "web", "docs", "query", "monad", "kuru", "mlx", "qwen", "vllm",
              "inspired", "open-model", "diffusiongemma", "opentelemetry", "buy", "sell", "input",
              "output", "like", "dislike", "action", "ms", "top", "step",
              "source", "port"}  # v7: source/platform=yibie 模板占位、port/derivative=散文短语"Jev port/derivative" 被 BARE 误捕
# v7 实证删除（existence_v3 全池重验：jsDelivr+API 双通道 404）——行级删除，附溯源注释
DELETE = {
    "typesafe/jev-1",                 # cobanov 行内 `typesafe/jev-1.13` 是 OpenRouter 模型标识非仓库；backtick 在 BARE 前瞻字符类里被误捕
    "danwilloughby/snifftest",        # PLAN L105 拼写变体（真库 danrwilloughby/snifftest 已另存且 EXIST），假库补录行
}
NOISE = {"assets", "blob", "tree", "commit", "commits", "issues", "pull", "releases", "workflows",
         "src", "public", "raw", "media", "images", "files", "actions", "security", "overview",
         "v1", "v2", "api", "cdn", "vi", "badge", "shields", "en", "zh", "cn", "head", "main", "master",
         "tests", "test", "spec"}  # v6: 表格行 `| tests/xxx.py |` 被 BARE 误捕（B3 扫读发现）
CODE_EXT = (".md", ".py", ".js", ".ts", ".tsx", ".json", ".yml", ".yaml", ".txt", ".rs", ".go",
            ".rb", ".java", ".sh", ".html", ".css", ".toml", ".lock")  # v6: 仓库名以代码扩展名结尾=表格单元误捕

# PLAN.md 批次节 → 显式名单（扫该节文本里出现的 owner/repo）
plan = (D / "PLAN.md").read_text(encoding="utf-8")
plan_batch = {}
for m in re.finditer(r"^## (B\d)[^\n]*\n(.*?)(?=^## |\Z)", plan, re.M | re.S):
    tag, body = m.group(1), m.group(2)
    for mm in GH_LINK.finditer(body):
        plan_batch[f"{mm.group(1)}/{mm.group(2)}".lower()] = tag
    for mm in BARE.finditer(body):
        r = f"{mm.group(1)}/{mm.group(2)}".lower()
        owner, repo = r.split("/")
        if owner in NOISE or repo in NOISE or len(repo) < 3 or owner in STOP_WORDS or repo in STOP_WORDS or repo.endswith(CODE_EXT):
            continue
        plan_batch.setdefault(r, tag)

# v5 覆写：B2 扫读实证（batch02 §2）——foreman 属编码代理 completion-gate，PLAN B2 节原文已自注“ crossed→B4 更当”
plan_batch["thruwire/foreman"] = "B4"

KEYWORD = [  # (regex, batch)  顺序即优先级；v2：危险短词改词边界锚定，修 latest→test、simple→sim 子串误伤
    (r"openjev|jev-local|nanojev|minijev|laya|^kev$|decider|jev-clone|jevsaur|reproduction|olljev|open-system-one|jev\.onnx|jevmlx|simple-jev|human-compiler|4b|modernbert|(^|[-_])verdict($|[-_])|jevfire|reflex|openvons|local.*model", "B1"),  # v4: winnow 移除（属判器→B5）
    (r"mario|pokemon|pong|flappy|doom|drone|(^|[-_])drones($|[-_])|(^|[-_])game(s|play)?($|[-_])|plays|gaming|racing|tetris|snake|zelda|heist|stealth|jevthoven|(^|[-_])music($|[-_])|pixel|(^|[-_])sim($|[-_])|t-rex|airways|neo4jev|killmyidea|slide", "B2"),
    (r"eval|jevcal|slop|judge|citation|benchmark|scorecard|grader|rubric|(^|[-_])rank(ing|er|s)?($|[-_])|rerank|verifier|playground|phishing-bench|(^|[-_])scout($|[-_])|meter|calibration|brier|(^|[-_])test(s|ing)?($|[-_])", "B3"),
    (r"browser|browse|agent|adblock|compaction|limpet|wakegate|foreman|duet|fast-|computer-use|orchestrator|mobile|harness|warden|council|swarm", "B4"),
    (r"guard|lint|snifftest|spam|malicious|abide|preflight|(^|[-_])diff(s|ing)?($|[-_])|review|(^|[-_])axi($|[-_])|hunch|(^|[-_])check(s|er)?($|[-_])|(^|[-_])commit-|pre-commit|winnow|seo|curate|consent|privacy|phish", "B5"),
    (r"router|routing|triage|moderation|classify|classif|intent|(^|[-_])gate(s|way|d)?($|[-_])|sentiment|topic", "B6"),
    (r"sdk|client|mcp|cli|sqlite|duckdb|jevql|jevsql|laravel|swift|-go$|^jev-go|go$|elixir|zio|hono|langchain|llama-index|nova|supabase|django|rails|flutter|s1-rs|typesafe-rs|jevwire|integration|home-assistant|ha-|plugin|extension|opencode|pi-|-rs$|ocaml|haskell|postgres|pg_|zod|dsl|typesafeai\.net|dspy|skill",
     "B7"),
    (r"stock|trade|trader|trading|buy|sell|legal|financ|forecast|medical|science|scientifi|pipeline|label|labeling|airtable", "B8"),
]
OFFICIAL_OWNERS = {"typesafe-ai", "typesafeio", "browser-use", "ably-labs", "vercel-labs", "steipete"}

def kb_batch(repo: str) -> str:
    name = repo.split("/", 1)[1]
    low = repo.lower()
    for rx, tag in KEYWORD:
        if re.search(rx, name, re.I) or re.search(rx, low, re.I):
            return tag
    return "?"

rows = {}
for key, fn in LISTS:
    if not (D / fn).exists():
        continue
    text = (D / fn).read_text(encoding="utf-8", errors="replace")
    section = ""
    for line in text.splitlines():
        h = re.match(r"^#{2,3} +(.+)", line)
        if h:
            section = h.group(1).strip()
            continue
        found = []
        for mm in GH_LINK.finditer(line):
            found.append(f"{mm.group(1)}/{mm.group(2)}".lower())
        for mm in BARE.finditer(line):
            r = f"{mm.group(1)}/{mm.group(2)}".lower()
            owner, repo = r.split("/")
            if owner in NOISE or repo in NOISE or len(repo) < 3 or len(owner) < 2:
                continue
            if owner in STOP_WORDS or repo in STOP_WORDS:   # v3 停用词
                continue
            if r not in found:
                found.append(r)
        # 去自链接（awesome 列表本身、CI 徽章）
        for r in found:
            if r in {k.lower() for k in LISTS if False}:
                continue
            if re.search(r"awesome-jev|awesome-typesafe|badge", r.split("/")[1], re.I) and key != "anilmatcha":
                if r.split("/")[1] in ("awesome-jev", "awesome-typesafe"):
                    continue
            if "/.github" in r or r.endswith("/github"):
                continue
            # 垃圾过滤：分类文件/文档路径/错误截断/列表仓库自链
            repo_name = r.split("/")[1]
            owner = r.split("/")[0]
            if len(owner) <= 2 and r not in plan_batch:
                continue
            if repo_name.endswith(CODE_EXT) or owner in ("categories", "docs", "0.0002", "input", "like", "ms", "one", "top", "api"):
                continue
            if repo_name in ("buy", "rejected", "step.") or "." in repo_name[:2]:
                continue
            if re.match(r"^awesome-(jev|typesafe|generative|gpt)", repo_name):
                continue
            desc = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
            desc = re.sub(r"^[\s>*\-0-9.)+]+", "", desc).strip()[:150]
            e = rows.setdefault(r, {"sources": set(), "sections": set(), "desc": ""})
            e["sources"].add(key)
            if section:
                e["sections"].add(f"{key}:{section}")
            if not e["desc"] and len(desc) > 10:
                e["desc"] = desc

# 官方资源/文档链接也算 yibie 之外来源，但不进库统计的 owner 过滤
# PLAN 点名但五目录未收录的库 → 补录（保证计划与清单一致）
for r, tag in plan_batch.items():
    owner, repo = r.split("/", 1)
    if re.match(r"^\d", owner) or owner in NOISE or len(repo) < 3 or repo in NOISE or repo.endswith(CODE_EXT):
        continue
    if r in DELETE:
        continue
    if r not in rows:
        e = {"sources": {"PLAN"}, "sections": set(), "desc": "PLAN 点名，五目录未收录（待验证存在性）"}
        rows[r] = e

owner_repos = defaultdict(list)
for r in rows:
    owner_repos[r.split("/")[0]].append(r)

out = []
for r in sorted(rows):
    if r in DELETE:
        continue
    e = rows[r]
    batch = plan_batch.get(r)
    how = "plan"
    if not batch:
        owner = r.split("/")[0]
        if owner in OFFICIAL_OWNERS:
            batch, how = "B0", "official-owner"
        else:
            kb = kb_batch(r)
            if kb == "?":
                batch, how = "B8", "unclassified→B8"   # 入矩阵但标记人工复分类
            else:
                batch, how = kb, "keyword"
    bulk = len(owner_repos[r.split("/")[0]])
    out.append({"repo": r, "batch": batch, "assign": how, "in_lists": "|".join(sorted(e["sources"])),
                "n_lists": len(e["sources"]), "owner_repos": bulk,
                "desc": e["desc"]})

D_join = D / "eval"
D_join.mkdir(exist_ok=True)
with open(D_join / "inventory.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["repo", "batch", "assign", "in_lists", "n_lists", "owner_repos", "desc"])
    w.writeheader()
    w.writerows(out)

# 统计
cnt = defaultdict(int); only_yibie = other_only = 0
for o in out:
    cnt[o["batch"]] += 1
    s = set(o["in_lists"].split("|"))
    if s == {"yibie"}:
        only_yibie += 1
    if "yibie" not in s:
        other_only += 1
print(f"total unique repos: {len(out)}")
print("per batch:", dict(sorted(cnt.items())))
print(f"yibie-only: {only_yibie} | NOT in yibie (parallel-list additions): {other_only}")
print(f"per-list counts:", {k: sum(1 for o in out if k in o['in_lists']) for k, _ in LISTS})
sus = {o: rs for o, rs in owner_repos.items() if len(rs) >= 3}
print(f"bulk-submission suspects (owner>=3 repos): { {o: len(rs) for o, rs in sorted(sus.items(), key=lambda x:-len(x[1]))} }")
