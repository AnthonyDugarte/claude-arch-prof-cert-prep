# Content review — Domain 4: Evaluation, Testing & Optimization

Reviewer pass, 2026-09-24. Reviewed against `AGENT-BRIEF.md` §3/§4, `VERIFIED-FACTS.md`, the exam guide
(Sample 3), the research dossier, and the draft at `drafts/04-evaluation-testing-optimization-draft.md`.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. [BLOCKER] The `effort` ladder is absent as a first-class lever. VERIFIED-FACTS names this "exam-grade
   material" for Domain 4 specifically: the low/medium/high/xhigh/max levels, Opus 5.5 defaulting to
   `medium` (so an omitted `effort` runs one level lower than it did on Opus 5), and the rule that
   top-level effort changes invalidate the prompt cache while a per-message effort change (beta,
   specific models) preserves it. The draft's "Effort reduction" row (§3.5) only names `low`/`medium`
   quality deltas and never states the ladder, the Opus 5.5 default, or the caching interaction as an
   explicit rule — it appears once, buried, as one clause in a triage-table cause list ("effort or
   thinking change"). Add a short paragraph or table row in §2 or §3.5 that states this as policy, not
   just as a possible cache-invalidation trigger.
2. [MAJOR] Word count is ~6,380 (wc -w), not the researcher's self-reported ~5,985, against a
   4,500–5,500 target. See Cut list below — concentrate cuts in §3, which currently restates the same
   cache-multiplier arithmetic in both §2.7 and §3.6, and carries multi-statistic table cells that could
   be compressed without losing the lesson.
3. [MAJOR] Practice item 3 reuses the exact worked example from §2.4 (25 cases × 2 reps ≈ ±14 points)
   with the same numbers, so a candidate can pattern-match to the teaching example instead of applying
   `1/sqrt(n·reps)`. Change the item's n/reps to a different pair (e.g., 40 × 3) so it tests the method,
   not recall of the illustration — this is exactly the failure mode the brief warns against for this
   chapter's numeric anchors.
```

---

## Numbers audit

| Anchor | Conditioned? | Sourced? | Teaches method? | Verdict | Note |
|---|---|---|---|---|---|
| pass@k vs pass^k | Yes — k=1 identical, k=10 diverge, worked | Yes [D04-S19] | Yes — decision rule (checker-filtered vs. unattended) | TEACHES-METHOD | Clean; preserve as-is. |
| Noise floor ≈ `1/sqrt(n·reps)`, worked 25×2≈±14 | Yes — stated for binary pass rate, three more worked points (50×2, 100×2) | Yes [D04-S04, D04-S05] | Yes — decision (reps before cases, MDE vs. headroom) | TEACHES-METHOD in the chapter body; **DECORATIVE-RISK in Item 3**, which reuses the identical numbers instead of forcing re-derivation. Fix the item, not the concept section. |
| Judge calibration ~90% (vs. academic >80%) | Yes — explicitly flagged as two different populations ("clear-cut labelled" vs. "subjective pairwise"), neither called "the" threshold | Yes [D04-S04, D04-S24] | Yes | TEACHES-METHOD | This is the single best-handled number in the chapter — model this treatment elsewhere. |
| Infra-config ~6 pp benchmark shift | Yes — attached to specific conditions (5.8% vs 0.5% error rate across resource settings) | Yes [D04-S20] | Yes — drives "run a no-change control before trusting a swing" | TEACHES-METHOD | Not tested in any item; used purely as evidentiary backing for the triage row. Good. |
| Caching gains 2.5–3.7× / 83% | Partially — hit-rate range (81–90%) given, but presented as flat fact in the §3.5 table row without an in-row "measured in one workload" hedge (citation only) | Yes [D04-S07] | Yes, via §3.6's `usage`-field verification method | TEACHES-METHOD, borderline DECORATIVE in the table cell | Add an inline hedge ("in one measured agent loop") to the §3.5 row itself, not just the footnote citation. |
| Batch 50% off, 24 h expiry | Yes — mechanism given (concurrent execution, best-effort cache hits) | Yes [D04-S17, D04-S18] | Yes — Item 6 tests the *mechanism* (why 1-hour TTL beats 5-minute under concurrency), not raw recall of "50%" | TEACHES-METHOD | Acceptable; this is a stable API characteristic, not a one-off measured statistic like the others on this list. |
| Tokenizer effect ~+30% | Yes — attached to "4.7-generation tokenizer," framed as "re-count, don't assume stability" | Yes [D04-S15, D04-S17] | Yes — Item 9's correct answer is conceptual ("counts don't transfer"), not the digit | TEACHES-METHOD | Good; the exact percentage never has to be recalled to answer correctly. |
| Secondary cluster: prompt-audit ±36%/14%, programmatic tool calling −24%, compaction −38%, action-triggering phrases +48%/+39%, "43% of spend on two problems" | Inconsistently hedged — some rows say "one triage agent's" / "a long run's"; others (prompt-audit row, tool-calling row) give no in-row qualifier, relying only on the trailing citation | Yes, all [D04-S06, D04-S07] | Partially — each illustrates a lever's *direction*, but the sheer density (6+ distinct one-off percentages in a single table) risks candidates memorizing digits from a single measured run rather than the ranking/sequencing lesson | DECORATIVE-RISK (density, not falsity) | Compress: keep one illustrative number per lever, state "(measured in one workload; treat as illustrative, not a guarantee)" once at the top of §3.5 rather than re-hedging every cell. This also serves the cut list. |

No number in the anchor list is asserted as universal, and none is DANGEROUS (i.e., none is stated in a way that would mislead an architect into an unsafe or wrong action). The chapter's strongest numbers-pedagogy is the judge-calibration reconciliation; its weakest spot is density in §3.5, not accuracy or framing.

---

## Diagnostic table audit (§5)

| Row (symptom) | First probe discriminating? | Verdict | Fix |
|---|---|---|---|
| Confident-but-wrong after data refresh; latency/model unchanged | Yes — retrieved-chunk inspection directly tests the only hypothesis consistent with the stated trigger | DISCRIMINATING | None. |
| Confident-but-wrong right after a prompt edit | Yes — diff + re-run on prior prompt isolates prompt vs. retrieval | DISCRIMINATING | None. |
| Answers correct, output unparseable | Yes — `stop_reason` cleanly separates truncation from a schema/format bug | DISCRIMINATING | None. |
| One case fails every round regardless of change | Probe itself is fine (read output, judge reasoning, expected value), but the **discriminating-evidence column cites an unrelated case-study statistic** ("+9-point win shrank to +3") instead of a generalizable signal to look for in the candidate's own investigation | WEAK-EVIDENCE-COLUMN | Replace with something checkable in the moment, e.g. "the model's answer is independently defensible but disagrees only with the stored expected value" or "the judge's stated rationale contradicts the label it assigns." |
| Quality drop after a model swap | Yes, though it is a two-step probe (both-models-same-prompt, then audit) rather than a single check | DISCRIMINATING (compound but acceptable — the guide's own Sample 3 rewards ordered probes) | None required; optionally label it "first *two* probes" for honesty. |
| Cost per request jumped, "nothing changed" | Yes — `cache_read_input_tokens` ≈ 0 vs. `cache_creation_input_tokens` ≈ full conversation is a hard, unambiguous signal | DISCRIMINATING | None; this is the table's strongest row. |
| p95/p99 up, p50 flat | Yes at the level a "first probe" should discriminate (TTFT-up vs. E2EL-up-alone) | DISCRIMINATING | None; further sub-causes (prefill vs. queue vs. cold cache) correctly belong to a second probe, not this row. |
| Eval score swings, no code change | Yes — a no-change control inside vs. outside the noise band is a clean binary discriminator | DISCRIMINATING | None. |
| Agent follows instructions found in a document | Partially — checking whether untrusted content arrived via `tool_result` vs. plain text rules out one failure class, but injection can still succeed *inside* a correctly-placed `tool_result` if no screening runs, so the probe alone can produce a false "ruled out" | PARTIALLY-DISCRIMINATING | Add a second check to the same row: "and whether a screening/classifier step ran on that tool output" — one clause, keeps the row a single line. |

Net: 7 of 9 rows are cleanly discriminating — a genuinely high bar met. Two rows need a small, specific fix (not a rewrite): row 4's evidence column and row 9's second clause.

---

## Cut list (target: ~5,300–5,400 words, from current ~6,380; §5 protected)

| Section | Current | Target | What to cut |
|---|---|---|---|
| Front matter | 90 | 90 | No cut. |
| §1 What this domain tests | 285 | 240 | Compress the two sentences after the Sample-3 quote ("That clause is not scenery... including what did not change") into one; the archetype table already carries the lesson. |
| §2 Core concepts | 953 | 860 | In 2.7, drop the restated cache-multiplier arithmetic (1.25×/2×/0.1× etc.) — it is fully repeated in §3.6's break-even table. Keep only "cost is derived from the four token classes in `usage`; rates are in §3.6." Also cut the "token guesses are routinely off by 3–10×" aside (redundant with the third-party-tokenizer point that follows it). |
| §3 Trade-off analyses | 2,304 | 1,650 | Largest cut. (a) Remove the duplicate "Batch API ... 50% off ... stacks with caching" clause from the §3.5 lever table (already stated fully in §3.6); replace with "(mechanics in §3.6)". (b) Compress the "Effort reduction" and "Re-run failures at higher effort" rows into one row — keep one illustrative number per claim, drop the second digit pair ("~2 points... ~8 points..." → "more expensive per point given up on long-horizon coding than on knowledge work"). (c) Add one sentence at the top of §3.5 hedging all figures as "measured in one workload each, illustrative not universal" instead of re-hedging every cell — this also fixes the density issue flagged in the Numbers audit. (d) Trim §3.7's statistics row by one clause. |
| §4 Worked scenarios | 588 | 545 | Trim S3 and S6 by ~20 words each — both currently spend a clause restating a lever already fully covered in §3.5/§3.6; keep the diagnostic/decision content, cut the recap. |
| §5 Failure modes & diagnostics | 443 | 443 | **Protected — no word-count cut.** Apply only the two content fixes above (row 4, row 9), which are net word-neutral. |
| §6 Anti-patterns | 195 | 180 | Tighten "Cache markers without verification" and "Scoring the plumbing" bullets by a clause each. |
| §7 Exam-day heuristics | 228 | 210 | Combine heuristics 2 and 3 (both are "match cause to trigger" restatements) into one line. |
| §8 Practice items | 929 | 900 | Net-neutral after Item 3's number swap; no other cuts needed — this section is already dense and well-targeted. |
| §9 Objective coverage | 117 | 117 | No cut. |
| §10 Sources | 207 | 190 | Tighten the linking prose between the ID list clauses; the IDs themselves must stay. |
| **Total** | **~6,339 (+~45 rule lines)** | **~5,365** | |

Note: the researcher's self-reported ~5,985 does not match `wc -w` (~6,384 for the full file). Use `wc -w` as the reconciliation baseline when checking the cut lands in band.

---

## Findings

- [BLOCKER] §2.7, §3.5 (absence) — VERIFIED-FACTS requires the `effort` parameter (low/medium/high/xhigh/max) treated as a first-class cost/quality lever, with Opus 5.5's `medium` default and the top-level-vs-per-message cache-invalidation rule stated explicitly — **required fix**: add a short paragraph (or a table row) stating the ladder, the Opus 5.5 default gotcha ("a call migrated to Opus 5.5 that omits `effort` silently runs a level lower than it did on Opus 5 — a quality regression that looks like a model problem but is a config default"), and the caching rule (top-level effort change invalidates cached prefixes; per-message effort change on supporting models preserves it, per `[VF]`). This is squarely Domain 4's objective 5 territory (optimize cost/latency/quality trade-offs) and is currently the chapter's single largest content gap.
- [MAJOR] Whole document — actual word count ~6,380 vs. reported ~5,985 vs. target band 4,500–5,500 — **required fix**: apply the Cut list above; do not cut §5.
- [MAJOR] §8 Item 3 (lines ~386–390) — reuses the exact "25 cases × 2 reps ≈ ±14 points" figures from the §2.4 worked example verbatim — **required fix**: change the case/rep counts (e.g., 40 cases × 3 reps, or 60 × 2) and recompute the correct discriminator so the item tests formula application, not memory of the illustration.
- [MAJOR] §5 triage row "One case fails every round regardless of change" (line ~320) — the discriminating-evidence column cites an unrelated historical statistic ("+9-point win shrank to +3") instead of a generalizable signal — **required fix**: replace with a checkable-in-the-moment signal (see Diagnostic table audit).
- [MINOR] §5 triage row "Agent follows instructions found in a document" (line ~325) — probe (check where untrusted content entered the request) does not fully discriminate injection-via-misplacement from injection-despite-correct-placement-with-no-screening — **fix**: add "and whether a screening step ran on that tool output" as a second clause.
- [MINOR] §2.7 and §3.6 (lines 85–94, 216–224) — the cache-write/read multipliers (1.25×, 2×, 0.1×, 0.05×) are stated in full twice — **fix**: state once in §3.6 (where the trade-off/decision belongs), cross-reference from §2.7.
- [MINOR] §3.5 lever table (lines 196–206) — several rows (prompt-audit ±36%/14%, programmatic tool calling −24%) lack an in-row hedge that the figure is from one measured workload, relying only on the trailing citation — **fix**: one hedge sentence at the top of §3.5 covering the whole table (also serves the cut list).
- [MINOR] §4 worked scenarios S3 (retail) and S6 (telecom) — industry flavor is thinner than S1/S2/S4/S5 (no retail- or telecom-specific constraint drives the decision; either scenario's lesson would transfer unchanged to a generic support chatbot) — **fix**: not required, but if the editor has room, add one retail-specific constraint to S3 (e.g., peak-season traffic multiplying the cost-cut urgency) and one telecom-specific constraint to S6 (e.g., a carrier SLA credit tied to p95).
- [MINOR] §2 core concepts (2.1–2.8) — the brief's four-part concept format (definition → why an architect cares → the decision it drives → common misconception) is present in substance but only two of the four parts are explicitly labeled (*Decision*, *Misconception*); "why an architect cares" is folded into the opening sentence rather than called out — **fix**: cosmetic only, no content is missing; leave to editor's discretion given the word-budget pressure.
- [NIT] §3.7 "Statistics" row — states the "tens of thousands of sessions per arm" A/B figure without the same worked-interpretation treatment given to the noise-floor formula (no sketch of why LLM variance inflates required N beyond the one-line mechanism already given) — acceptable given table-cell space constraints; not required for SHIP-WITH-FIXES.
- [NIT] §3.7/dossier gap — the dossier's stall-handling taxonomy (after 2–3 rounds inside the noise band, categorize failures as artifact gap / grader disagreement / harness-infra / structural / variance) is compressed in the draft to a single "train up, test flat ⇒ revert" line — a real simplification of "iterative improvements" (objective 3), but not a blocking gap since the overfitting signature itself is preserved. Optional addition if cuts free space; do not add without cutting elsewhere.

---

## Practice items — item-by-item

| # | Verdict | Note |
|---|---|---|
| 1 | SHIP | Clean tail-latency discriminator; no volatile-number dependency. |
| 2 | SHIP | Two-correct-answer set well-chosen; tests silent-substitution and non-inferiority framing, not recall. |
| 3 | REVISE (numbers) | Reuses the exact §2.4 worked-example numbers — see Findings. Fix the numbers, not the lesson. |
| 4 | SHIP | Matches the guide's Sample 3 shape almost exactly; strong differential-diagnosis item. |
| 5 | SHIP | Bias-mitigation mapping is precise; distractors (self-judge, label reveal, cosine blending) are each a genuine, distinct trap. |
| 6 | SHIP | Tests the batch-concurrency-vs-TTL mechanism, not raw recall of "50%"; acceptable per Numbers audit. |
| 7 | SHIP | Clean dashboard/alert/weekly-review discriminator. |
| 8 | SHIP | Good "implausible jump is suspicious" item; distractors each address a different wrong instinct (ship, tighten CI, reduce grader variance). |
| 9 | SHIP | Tests conceptual tokenizer-non-transferability, not the specific ~30% figure. |
| 10 | SHIP | Sequencing item (shadow → canary → A/B) is the chapter's best synthesis item; correctly rewards blast-radius discipline over speed. |

9 of 10 ship as-is; only Item 3 needs a numeric fix.

---

## Must preserve

- The Sample-3-anchored framing in §1 (distractor archetype table) — this is exactly the right altitude and directly trains the exam's actual cognitive pattern (differential diagnosis via negative evidence).
- The judge-calibration reconciliation in §3.2 (90% operational gate vs. >80% research ceiling, explicitly named as different populations) — the single best-handled number in the chapter; a model for how the other numeric anchors should read.
- The conflation concept (§2.5) and its consequences in the triage table — sharp, exam-relevant, and correctly generalized beyond any one number.
- The `usage`-field diagnostics in the triage table (cache_read vs. cache_creation for cost jumps; `stop_reason` for truncation) — genuinely discriminating, concrete, and directly checkable by a candidate in production.
- The three-gate non-inferiority framework for cost-reduction changes (§3.7: quality band, cost margin, mechanism) — a clean, teachable decision rule that resists "it depends."
- The safety/security measurement treatment in §2.8 and Scenario S4 — explicitly covers bidirectional refusal correctness, PII/secret leakage, injection resistance, and fail-on-any aggregation, which is exactly what the blueprint's naming of "safety, security" as metrics requires and what a shallower chapter would have skipped.
- The lever-sequencing logic in §3.5 ("free wins before tradeoffs... except once an eval exists, walk model × effort early") — teaches the reasoning, not just an ordered list.
- Clean domain boundary-keeping: the chapter does not drift into Domain 3's RAG-pipeline-design territory or Domain 5's guardrail-design territory even though it touches retrieval metrics and adversarial testing — it stays on "how do you measure this," which is Domain 4's mandate.

---

## Coverage matrix

| Objective | Covered adequately? | Evidence |
|---|---|---|
| Define evaluation metrics (accuracy, latency, cost, safety, security) | Yes | §2.1–2.3, §2.6–2.8, §3.1, Items 1, 9. Safety/security explicitly measured via adversarial sets, bidirectional refusal, PII leakage, injection resistance (§2.8, S4) — not just named. |
| Design evaluation datasets and test frameworks using mixed methodologies | Yes | §2.4–2.5, §3.1–3.3 (grading ladder, judge-shape, dataset taxonomy), S2/S4/S5, Items 3, 5. |
| Conduct A/B testing and iterative improvements | Yes, with a minor thinness on the "iterative" half | §3.4, §3.7, S3, Items 2, 10. A/B mechanics (shadow/canary/A-B, non-inferiority, power) are strong; the iterative-hillclimb stall-handling taxonomy is compressed to one line (see NIT above). |
| Diagnose system issues (prompt failure, hallucinations, model mismatch) | Yes | §1, §2.5, §5 triage table (9 rows, 7 cleanly discriminating), S1/S5, Items 4, 8. All three named symptom classes (prompt failure: row 2; hallucination: row 1 + S1/S2; model mismatch: row 5) have a dedicated row or scenario. |
| Optimize token usage, latency, and cost-performance trade-offs | Partial | §2.6–2.7, §3.5–3.6, S3, S6, Items 1, 6, 9 cover caching, batch, token accounting, latency decomposition well. **Gap: `effort` as a ladder with the Opus 5.5 default and cache-invalidation rule is missing** — see BLOCKER finding. This is the objective most affected by the gap. |
| Monitor system performance using logging and observability tools | Yes | §3.8 (dashboard/alert/weekly-review), instrumentation field list (model from response, four token classes, `stop_reason`, refusal flag, `judge_model`/`judge_usage`), Items 7, 10. SLO framing over sampled rates (pass^k, ungrounded %, p95 E2EL, goodput) is present and correctly scoped away from Domain 3's infra-scaling territory. |

---

## Sources

No new external sources were consulted; all findings cite source IDs already established in
`research/04-evaluation-testing-optimization-sources.md` (D04-S01…D04-S31, as referenced inline above)
plus `VERIFIED-FACTS.md` (cited as `[VF]`) for the `effort`/caching-interaction requirement. This review
file introduces no `DNN-R0x` sources.
