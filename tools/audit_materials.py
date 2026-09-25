"""Check local course structure and optionally regenerate its navigation indexes.

Run from any directory: python3 path/to/audit_materials.py --write-indexes
This checks structure, not factual truth or professional teaching quality.
"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "01-solution-design.md", "02-models-prompts-context.md", "03-integration.md",
    "04-evaluation-optimization.md", "05-governance-safety.md",
    "06-stakeholders-lifecycle.md", "07-developer-enablement.md",
]
COUNTS = [6, 5, 8, 6, 5, 5, 3]
WEIGHTS = [17, 13, 19, 16, 14, 14, 7]
LINK = re.compile(r"\[([^\]\n]+)\]\(([^\s)]+)\)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-indexes", action="store_true")
    args = parser.parse_args()
    errors = []
    coverage = []
    total_questions = 0
    for domain, (filename, count, weight) in enumerate(zip(MODULES, COUNTS, WEIGHTS), 1):
        path = ROOT / "course" / filename
        if not path.exists():
            errors.append(f"Missing module: {path}")
            continue
        text = path.read_text()
        headings = dict(re.findall(r"^#{2,3} (D\d\.\d+) [—–-] (.+)$", text, re.M))
        for objective in range(1, count + 1):
            key = f"D{domain}.{objective}"
            if key not in headings:
                errors.append(f"Missing objective heading: {key}")
            coverage.append((key, weight, headings.get(key, "MISSING"), filename))
        questions = list(re.finditer(r"^\*\*(\d+)\. Select (ONE|TWO|THREE)\.\*\*", text, re.M))
        total_questions += len(questions)
        if len(questions) != 6:
            errors.append(f"{filename}: expected 6 questions with explicit selection counts, found {len(questions)}")
        for i, question in enumerate(questions):
            block = text[question.end():questions[i + 1].start() if i + 1 < len(questions) else len(text)]
            answer = re.search(r"\*\*Answers?: ([A-E](?:, | and |, and |[A-E])*)\.", block)
            wanted = {"ONE": 1, "TWO": 2, "THREE": 3}[question.group(2)]
            selected = re.findall(r"\b[A-E]\b", answer.group(1)) if answer else []
            if len(selected) != wanted or len(set(selected)) != wanted:
                errors.append(f"{filename} question {question.group(1)}: expected {wanted} unique keyed answers, got {selected}")
    advanced = (ROOT / "course/10-advanced-casebook.md").read_text()
    advanced_questions = re.findall(r"\*\*A(\d+) · D\d · Select (ONE|TWO|THREE)\.\*\*", advanced)
    if len(advanced_questions) != 14:
        errors.append(f"Expected 14 advanced questions, found {len(advanced_questions)}")
    for number, count in advanced_questions:
        answer = re.search(rf"\*\*A{number}: ([A-E, ]+)\.\*\*", advanced)
        selected = re.findall(r"\b[A-E]\b", answer.group(1)) if answer else []
        if len(set(selected)) != {"ONE": 1, "TWO": 2, "THREE": 3}[count]:
            errors.append(f"Advanced A{number}: selection count mismatch")

    inventory = {}
    for path in sorted(ROOT.rglob("*.md")):
        if path.name in {"references.md", "coverage-map.md"}:
            continue
        for title, target in LINK.findall(path.read_text()):
            if target.startswith(("https://", "http://")):
                url = target.split("#")[0]
                item = inventory.setdefault(url, {"title": title, "files": set()})
                item["files"].add(path.relative_to(ROOT).as_posix())

    if args.write_indexes:
        rows = ["# Blueprint coverage map", "", "The guide has 38 detailed objectives across seven domains. D1.1-style identifiers are local course labels in the guide's objective order. The table links each teaching section to its module; module labs and question sets provide additional practice. This index proves location, not mastery or factual accuracy. Independent reviews assess substance.", "", "| ID | Domain weight | Teaching section | Module |", "|---|---:|---|---|"]
        for key, weight, heading, filename in coverage:
            rows.append(f"| {key} | {weight}% | {heading} | [{filename[:2]}](course/{filename}) |")
        rows += ["", "Each module contains six warmup scenario items, option rationales and a lab. The [advanced casebook](course/10-advanced-casebook.md) adds two items per domain; the [capstone](course/08-capstone.md) integrates all seven. The 16 numbered guide sections are separately mapped to actual searches in the [guide search log](research/guide-sections.md).", ""]
        (ROOT / "coverage-map.md").write_text("\n".join(rows))
        rows = ["# Referenced materials", "", "Research date: **2026-09-24**. This deduplicated URL inventory locates every clickable external reference in the pack, including reviewer validation sources. A URL's presence is not a claim that its entire page was read or that it remains current.", "", "Use the source registers for source IDs, actual queries, claim support, access status and limitations:", "", "- [Guide sections 1–16 and preparation resources](research/guide-sections.md)", "- [Domains 1–3](research/domains-1-3.md)", "- [Domains 4–5](research/domains-4-5.md)", "- [Domains 6–7](research/domains-6-7.md)", "- [Independent source validation](reviews/validator.md)", "", "The supplied [exam guide](claude-arch-professional-guide.md) supplies blueprint/policy statements. Official platform and protocol documentation supplies technical behavior; regulatory agencies supply their own guidance. Worked scenarios and recommendations are original synthesis. Indexed-only Partner Academy pages are flagged in the guide register; failed opens are not treated as verified page contents. Recheck product limits, settings, contracts, eligibility and program policies before relying on them operationally.", "", f"## URL inventory ({len(inventory)} distinct URLs; fragments collapsed)", "", "| Reference | Referenced in |", "|---|---|"]
        for url, item in sorted(inventory.items()):
            locations = ", ".join(f"[{p}]({p})" for p in sorted(item["files"]))
            rows.append(f"| [{item['title'].replace('|', '/')} ]({url}) | {locations} |")
        rows.append("")
        (ROOT / "references.md").write_text("\n".join(rows))

    for path in ROOT.rglob("*.md"):
        for _, target in LINK.findall(path.read_text()):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target_path = target.split("#")[0]
            if not (path.parent / target_path).exists():
                errors.append(f"Broken local file link: {path.relative_to(ROOT)} -> {target}")
    print(f"Objective headings: {len(coverage)}; module questions: {total_questions}; advanced questions: {len(advanced_questions)}; external URLs: {len(inventory)}")
    print("Scope: local file links, expected objective headings, item counts and keyed selection counts; not remote link availability or factual validation.")
    for error in errors:
        print("ERROR:", error)
    if errors:
        raise SystemExit(1)
    print("Structural audit passed.")


if __name__ == "__main__":
    main()
