# Launch queue (orchestrator working note)

## Launched
- D5 editor (opus) — running
- D6 editor (opus) — running
- D3 content / validator / adversarial — running

## Waiting on a blocker before launch
- **D1 editor** — needs the D1 validator (content + adversarial done). D1 adversarial = MAJOR-REWORK
  (scoped): S5 violates its own 2s TTFT constraint; Item 11 teaches "sponsor said transformation ⇒
  multi-agent" (a pillar selects a *metric*, never a pattern — same defect in §4.8's column); Objective 1
  has no primary-source method though the dossier researched Anthropic's pilot-selection criteria;
  3 items DEFECTIVE (8, 11, 12), 2 UNDER-DETERMINED (2, 5); cut ~2,900 words.
- **D4 editor** — needs the D4 validator (content + adversarial done). Must-fix: the `effort` ladder is
  absent as a first-class lever; §3.5–3.7 never state that changing top-level `effort` invalidates the
  cache although §5's own table lists it; Item 6 is quantitatively defective (cache-on only wins above
  ~53% hit rate, chapter's own range starts at 30%); noise-floor formula assumes p≈0.5 and understates
  precision at 90–95% baselines; cut to 4,500–5,500 from ~6,380.
- **D2 editor** — needs all three D2 reviews (all running).
- **D3 editor** — needs all three D3 reviews (all running).
- **D7 crew + editor** — D7 research still running.

## Wave D (after all chapters)
Master index/README · cross-domain trade-off compendium · full 63-item mock exam + adversarial item
review · consolidated bibliography (merge every `research/*-sources.md` plus validator `*-V*` tables,
de-duplicated) · study plan · consolidation handoff note.

## Cross-cutting insights to carry into Wave D
- A business value pillar selects a **metric**, not an architectural pattern (D1 adversarial).
- Control strength is **two axes** — bypass resistance × expressiveness — not a linear ranking; express it
  deterministically if it can be expressed deterministically (D5 adversarial).
- Risk-tiered review (100% on the irreversible slice, sampled on the rest) is the posture that resolves
  review-capacity pressure, and the one an exam is most likely to key (D6 adversarial).
- Changing top-level `effort` invalidates the prompt cache; per-message effort preserves it. Affects both
  D2 and D4 optimization guidance.
