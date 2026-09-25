# Track B pipeline — provenance and process

Second, independent research track for the **Claude Certified Architect – Professional (CCAR-P)** prep
course. Deliberately separate from `../prep-course-research/` so the two tracks can be consolidated later
without cross-contamination. Track B agents were not shown Track A's output.

Session date: 2026-09-24. Orchestrator: Claude Opus 5 (1M context).

## Roles (per domain, minimum set required by the sponsor)

| Role | Mandate | Output |
|------|---------|--------|
| **Researcher** | Dedicated search per domain against primary sources; builds dossier + full draft chapter + source table | `research/NN-*-dossier.md`, `drafts/NN-*-draft.md`, `research/NN-*-sources.md` |
| **Content reviewer** | Pedagogy, altitude, blueprint coverage, trade-off quality, item quality | `review/NN-*-content-review.md` |
| **Validator** | Independent fact-check of every checkable claim against primary sources; CONFIRMED / CONTRADICTED / NOT-FOUND per claim | `review/NN-*-validation.md` |
| **Adversarial reviewer** | Attacks the material: wrong-but-plausible framings, exam mismatch, missing alternatives, hidden assumptions, items with defensible second answers | `review/NN-*-adversarial.md` |
| **Editor** | Merges draft + three reviews into the shippable chapter; resolves conflicts; keeps citations | `course/NN-*.md` |

Reviewers never edit the draft; the editor is the only writer of `course/`.

## Model assignment

Mixed by design (no single model across all sub-agents, per sponsor instruction; Fable not used).

| Domain | Weight | Researcher | Content review | Validator | Adversarial | Editor |
|--------|--------|-----------|----------------|-----------|-------------|--------|
| 1 Solution Design & Architecture | 17% | Opus 5 | Sonnet 5 | Sonnet 5 | Opus 5 | Opus 5 |
| 2 Models, Prompting & Context | 13% | Opus 5 | Sonnet 5 | Opus 5 | Sonnet 5 | Opus 5 |
| 3 Integration | 19% | Opus 5 | Sonnet 5 | Opus 5 | Opus 5 | Opus 5 |
| 4 Evaluation, Testing & Optimization | 16% | Opus 5 | Sonnet 5 | Opus 5 | Sonnet 5 | Opus 5 |
| 5 Governance, Safety & Risk | 14% | Sonnet 5 | Sonnet 5 | Opus 5 | Opus 5 | Opus 5 |
| 6 Stakeholder Comms & Lifecycle | 14% | Sonnet 5 | Opus 5 | Sonnet 5 | Opus 5 | Opus 5 |
| 7 Developer Productivity | 7% | Sonnet 5 | Sonnet 5 | Sonnet 5 | Sonnet 5 | Opus 5 |

Rationale: heavy/technical domains get Opus on research and adversarial passes; validators run on a
different model than the researcher wherever possible so a shared blind spot is less likely to survive;
the smallest domain runs lean.

## Waves

1. **Wave A** — 7 researchers in parallel (dossier + draft + sources).
2. **Wave B** — 21 reviewers in parallel (content / validation / adversarial per domain).
3. **Wave C** — 7 editors in parallel (final chapters).
4. **Wave D** — cross-cutting assets: master index, cross-domain trade-off compendium, full-length
   mock exam + adversarial item review, consolidated bibliography, study plan.

## Status

Updated as waves complete; see `STATUS.md`.
