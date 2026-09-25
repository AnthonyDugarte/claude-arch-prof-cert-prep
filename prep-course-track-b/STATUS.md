# Status

| Domain | Research | Content review | Validation | Adversarial | Final chapter |
|--------|----------|----------------|------------|-------------|---------------|
| 01 Solution Design | done | running | running | running | — |
| 02 Models/Prompting/Context | running | — | — | — | — |
| 03 Integration | running | — | — | — | — |
| 04 Evaluation/Testing/Optimization | running | — | — | — | — |
| 05 Governance/Safety/Risk | done | SHIP-WITH-FIXES | running | running | — |
| 06 Stakeholder/Lifecycle | done | SHIP-WITH-FIXES | running | running | — |
| 07 Developer Productivity | running | — | — | — | — |

Cross-cutting: master index — pending · trade-off compendium — pending · mock exam — pending ·
consolidated bibliography — pending · study plan — pending

## Corrections applied mid-flight

- **2026-09-24:** `AGENT-BRIEF.md` §0 asserted Claude Opus 5 as current. The Domain 1 researcher
  contradicted it against live docs and was right. Orchestrator verified against
  platform.claude.com: current lineup is **Fable 5.1 / Opus 5.5 / Sonnet 5 / Haiku 4.5**, Opus 5 is
  legacy. Also surfaced the **`effort` parameter + adaptive thinking** model that supersedes
  `budget_tokens` extended thinking, per-model cache-read pricing, and the **Covered Models 30-day
  retention / ZDR exclusion**. All captured in `VERIFIED-FACTS.md`, which is now canonical; the brief
  was patched to point at it. Drafts written before this correction must be checked for stale model
  claims — every validator is instructed to do so.
