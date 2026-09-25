# Claude Certified Architect – Professional: preparation course

This is an independent preparation pack for **CCAR-P**, aligned to the user-supplied [exam guide](claude-arch-professional-guide.md), version 1.0, effective July 2026. Research date: **2026-09-24**. It teaches production architecture decisions, with original scenarios and exercises. It is not an Anthropic course or a source of live exam questions.

This repository contains the course, its source research, and independent review records. The supplied guide remains the blueprint authority. Product documentation supplies technical facts; examples, thresholds, schedules, and architectural recommendations are teaching material unless explicitly attributed.

## Start here

1. Read [orientation and preparation resources](course/00-orientation.md). Identify your weakest objectives using the [coverage map](coverage-map.md).
2. Study each module, explain the rejected alternatives aloud, and complete its exercise before reading its practice answer key.
3. Work through the [14 advanced decision cases](course/10-advanced-casebook.md), then complete the [integrated capstone](course/08-capstone.md) and use the [decision templates](course/09-decision-templates.md) to defend the design.
4. Revisit missed objectives and the actual guide's three sample questions. Consult the [research and review provenance](PROVENANCE.md) for source boundaries and validation history.

| Module | Blueprint weight | What you must be able to defend |
|---|---:|---|
| [1. Solution design and architecture](course/01-solution-design.md) | 17% | Why the simplest adequate architecture fits the business and failure model |
| [2. Models, prompting and context](course/02-models-prompts-context.md) | 13% | Model, prompt, context and reuse decisions under measurable constraints |
| [3. Integration](course/03-integration.md) | 19% | Retrieval, tools, protocols, identity and observability choices |
| [4. Evaluation, testing and optimization](course/04-evaluation-optimization.md) | 16% | Evidence of quality, diagnosis and safe cost/latency improvements |
| [5. Governance, safety and risk](course/05-governance-safety.md) | 14% | Controls, escalation and evidence proportional to risk |
| [6. Stakeholders and lifecycle](course/06-stakeholders-lifecycle.md) | 14% | Requirements, decisions, ownership, rollout and operational handoff |
| [7. Developer productivity and enablement](course/07-developer-enablement.md) | 7% | Team configuration, verified engineering workflows and incident response |

Weights are from Section 6 of the supplied guide; they are not guaranteed counts of questions. Sections 1–16 each have a dedicated query in the [guide-section search log](research/guide-sections.md). The [reference inventory](references.md) tracks all linked external materials. Domain searches and evidence are in [domains 1–3](research/domains-1-3.md), [domains 4–5](research/domains-4-5.md), and [domains 6–7](research/domains-6-7.md).

## Suggested study rhythm

For an experienced engineer, reserve an illustrative **40 hours**, adjusting after self-assessment: orientation 1; D1 5; D2 4; D3 6; D4 5; D5 4; D6 4; D7 2; capstone and remediation 9. This is a study plan, not an official duration or a promise of readiness. It excludes optional external courses and building a fully deployed production service.

For every decision, practice this five-part answer: **constraint → viable options → choice → cost/risk accepted → evidence that would change the choice**. A response that names a feature without explaining its boundary or rejected alternative is incomplete at this level.

Readiness means you can diagnose a failing system, defend alternatives, identify missing evidence, and operate the controls. The original module exercises and questions are learning checks; they do not estimate the official scaled score.

## Repository layout and maintenance

- `course/`: orientation, seven domain modules, capstone, templates, and advanced practice.
- `research/`: dedicated searches and source registers with access dates and limitations.
- `reviews/`: independent reviews, corrections, and validation history.
- `tools/`: the structural audit and navigation-index generator.
- [references.md](references.md): linked source inventory.
- [coverage-map.md](coverage-map.md): all 38 blueprint objectives mapped to teaching sections.

From the repository root, check objective coverage, question counts, answer-selection counts, and local links:

```sh
python3 tools/audit_materials.py
```

After changing references or module headings, regenerate the indexes and run the same checks:

```sh
python3 tools/audit_materials.py --write-indexes
```
