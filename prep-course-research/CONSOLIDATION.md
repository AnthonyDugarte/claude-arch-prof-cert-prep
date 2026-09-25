# Consolidation handoff

This folder is one research team's contribution for consolidation with the user's other researcher. It preserves independent source evidence and review findings rather than overwriting the supplied guide or another team's material. Reference date: 2026-09-24. All objective IDs refer to the seven-domain Professional guide in this repository, not a Foundations exam blueprint.

## Deliverables and provenance

| Contribution | Agent role | Model | Artifacts |
|---|---|---|---|
| Domains 1–3 research and lessons | Researcher | Inherited parent model | `course/01`–`03`; `research/domains-1-3.md` |
| Domains 4–5 research and lessons | Researcher | GPT-6 Sol | `course/04`–`05`; `research/domains-4-5.md` |
| Domains 6–7 research and lessons | Researcher | GPT-6 Luna | `course/06`–`07`; `research/domains-6-7.md` |
| Educational completeness and assessments | Independent reviewer | GPT-6 Sol | [Reviewer report](reviews/reviewer.md) |
| Source grounding and structural checks | Independent validator | GPT-6 Sol | [Validator report](reviews/validator.md) |
| Counterexamples and failure analysis | Independent adversarial reviewer | GPT-6 Astra | [Adversarial report](reviews/adversarial-reviewer.md) |
| Guide-section searches, orientation, capstone, advanced cases, indexes and reconciliation | Lead consolidator | Parent agent | Remaining files in this folder |

The roles ran separately. Reports are point-in-time findings; the [resolution record](reviews/resolution-record.md) tracks edits and final verification. Researchers opened primary sources and recorded query trails. The validator independently re-opened selected high-risk sources; this is not a claim that every external page was independently re-audited.

## How to compare contributions

Compare by objective ID in the [coverage map](coverage-map.md), then compare each claim's source and applicability in the [reference inventory](references.md). Preserve stronger examples from either pack. When advice differs, identify the changed constraint—task predictability, authority, corpus freshness, deployment platform, evaluation method, latency target or risk—before calling it a contradiction.

Keep these distinctions explicit during merging:

- **Blueprint facts:** sourced to the local guide. Policies and format are not all independently authenticated online.
- **Product facts:** tied to a dated primary document; changing model names, limits, prices, feature support and settings should be rechecked.
- **Architecture recommendations:** conditional synthesis, supported by an example and a credible alternative; not universal vendor requirements.
- **Hypothetical exercise data:** constraints, timings, costs, thresholds and scores created for teaching. No live API benchmark or deployment was performed.
- **Access limits:** Partner Academy pages were indexed but direct retrieval returned 403; detailed lesson content was not inspected. Public Academy syllabi were opened.
- **Practice provenance:** original teaching questions and rationales, with the guide's samples explicitly attributed separately. No live exam material was sought or reproduced.

## Suggested consolidation agenda

1. Lock the target guide version and domain mapping; flag source or policy conflicts rather than silently overwriting them.
2. For each domain, choose the clearest concept definition, strongest constrained tradeoff, useful failure example and most actionable exercise.
3. Reconcile high-risk claims against current primary sources: authorization, caching/context, Claude Code enforcement, compliance scope and exam access.
4. Keep warmup questions separate from advanced decision practice; resolve ambiguous keys and duplicate situations.
5. Retain the capstone's evidence prerequisites, operational handoff and original/simulated-data labels.
6. Carry forward open uncertainties and source access status. Re-run structural checks after moving files.

Run `python3 prep-course-research/tools/audit_materials.py --write-indexes` from the workspace root to regenerate references and the coverage map and check local structure. Review reports provide the separate semantic checks. This command does not validate the continued availability or truth of remote sources.
