#!/usr/bin/env python3
"""Merge every per-domain source table into one consolidated bibliography.

Reads research/NN-*-sources.md and any reviewer tables that follow AGENT-BRIEF.md §6
(IDs like D03-S04, D05-V12, D01-R02, D02-A01), de-duplicates by URL, and writes
REFERENCES.md. Re-runnable: just run it again after later waves land.
"""
import re, pathlib, collections, datetime

ROOT = pathlib.Path(__file__).parent
ROW = re.compile(r"^\|\s*(D\d{2}-[SVRA]\d+)\s*\|(.+)$")
ID = re.compile(r"^D(\d{2})-([SVRA])(\d+)$")
ROLE = {"S": "researcher", "V": "validator", "R": "content reviewer", "A": "adversarial reviewer"}
DOMAIN = {
    "01": "Solution Design & Architecture",
    "02": "Models, Prompting & Context",
    "03": "Integration",
    "04": "Evaluation, Testing & Optimization",
    "05": "Governance, Safety & Risk",
    "06": "Stakeholder Comms & Lifecycle",
    "07": "Developer Productivity",
}

def cells(rest):
    parts = [c.strip() for c in rest.split("|")]
    while parts and parts[-1] == "":
        parts.pop()
    return parts

def url_of(parts):
    for c in parts:
        m = re.search(r"https?://[^\s)\]>|]+", c)
        if m:
            return m.group(0).rstrip(".,;")
    return ""

records = []
for path in sorted(ROOT.glob("research/*-sources.md")) + sorted(ROOT.glob("review/*.md")):
    for line in path.read_text(errors="replace").splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        sid, rest = m.group(1), m.group(2)
        parts = cells(rest)
        if not parts or set("".join(parts)) <= set("-: "):
            continue
        records.append({"id": sid, "url": url_of(parts), "cells": parts, "file": path.name})

by_url = collections.OrderedDict()
no_url = []
for r in records:
    if r["url"]:
        by_url.setdefault(r["url"], []).append(r)
    else:
        no_url.append(r)

def trust_of(cells_):
    blob = " ".join(cells_).lower()
    for t in ("primary", "secondary", "low"):
        if re.search(rf"\b{t}\b", blob):
            return t
    return "unrated"

trust_counts = collections.Counter()
domain_counts = collections.Counter()
role_counts = collections.Counter()
for url, rs in by_url.items():
    trust_counts[trust_of(rs[0]["cells"])] += 1
for r in records:
    m = ID.match(r["id"])
    if m:
        domain_counts[m.group(1)] += 1
        role_counts[ROLE.get(m.group(2), "?")] += 1

out = []
out.append("# Consolidated bibliography — Track B\n")
out.append(f"Generated {datetime.date.today().isoformat()} by `build-references.py`. "
           "Re-run after any wave lands.\n")
out.append(f"**{len(by_url)} unique URLs** across **{len(records)} citation rows** "
           f"from {len(set(r['file'] for r in records))} files.\n")
out.append("Trust mix (by unique URL): " +
           ", ".join(f"{k}: {v}" for k, v in trust_counts.most_common()) + "\n")
out.append("Citation rows by domain: " +
           ", ".join(f"D{k} {v}" for k, v in sorted(domain_counts.items())) + "\n")
out.append("Citation rows by role: " +
           ", ".join(f"{k}: {v}" for k, v in role_counts.most_common()) + "\n")
out.append("\nIDs follow AGENT-BRIEF.md §6: `S`=researcher, `V`=validator, `R`=content reviewer, "
           "`A`=adversarial reviewer. A URL cited by several agents lists every ID, which is how you "
           "see where two tracks independently corroborated a claim.\n")

out.append("\n## Sources by domain\n")
for dom in sorted(DOMAIN):
    rows = [(u, rs) for u, rs in by_url.items()
            if any((ID.match(r["id"]) or [None, None]) and ID.match(r["id"]).group(1) == dom for r in rs)]
    if not rows:
        continue
    out.append(f"\n### Domain {dom} — {DOMAIN[dom]}\n")
    out.append("| IDs | Trust | URL | Detail (as recorded) |")
    out.append("|-----|-------|-----|----------------------|")
    for url, rs in sorted(rows, key=lambda x: x[1][0]["id"]):
        ids = ", ".join(sorted({r["id"] for r in rs}))
        detail = " · ".join(c for c in rs[0]["cells"] if c and not c.startswith("http"))[:240]
        detail = detail.replace("|", "\\|")
        out.append(f"| {ids} | {trust_of(rs[0]['cells'])} | <{url}> | {detail} |")

if no_url:
    out.append("\n## Citation rows without a resolvable URL\n")
    out.append("These need a URL added during consolidation.\n")
    out.append("| ID | File | Detail |")
    out.append("|----|------|--------|")
    for r in sorted(no_url, key=lambda x: x["id"])[:120]:
        detail = " · ".join(c for c in r["cells"] if c)[:200].replace("|", "\\|")
        out.append(f"| {r['id']} | {r['file']} | {detail} |")

(ROOT / "REFERENCES.md").write_text("\n".join(out) + "\n")
print(f"{len(by_url)} unique URLs / {len(records)} rows -> REFERENCES.md")
print("trust:", dict(trust_counts))
print("by domain:", dict(sorted(domain_counts.items())))
