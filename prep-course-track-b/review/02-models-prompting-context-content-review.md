# Content review — Domain 2: Claude Models, Prompting & Context Engineering (13%)

Reviewed: `drafts/02-models-prompting-context-draft.md` (6,315 body words by section count, 6,369 by
`wc -w`) against `research/02-models-prompting-context-dossier.md`, `AGENT-BRIEF.md` §3/§4/§6,
`VERIFIED-FACTS.md`, and the exam guide's Section 6 objectives and Section 8 Sample 2 cognitive level.
Line numbers are draft line numbers from the version read this session.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. Two practice items (4, 9) and one scenario (5.2) have their entire correctness logic built on facts
   VERIFIED-FACTS.md explicitly marks "pending validator confirmation" (citations+structured-outputs
   400; prefill/temperature/forced-tool_choice 400s). The front matter (line 15) claims blanket
   verification ("Every model ID, price, limit, and parameter here was verified") that is not true of
   these facts. If validation contradicts any one of them, these items have no single defensible
   answer. Rewrite the rationale of items 4 and 9 to not rest solely on "returns 400," and correct the
   front-matter claim.
2. §10's objective-coverage table is systematically mismapped, not merely imprecise: §4.8 (Guardrails —
   literally Objective 2's content) is cited under Objective 1 and never once appears under Objective 2;
   §4.4 (zero-shot vs. few-shot — Objective 3's home) is absent from the Objective 3 row; §4.6
   (context-window strategy — Objective 4's home) is absent from the Objective 4 row, which instead
   cites §4.5 (caching — Objective 5's content). This is the exact table AGENT-BRIEF §3.10 requires to
   be an honest audit trail, and right now it would mislead an editor into thinking guardrails and
   context-window strategy are uncovered when they are in fact the chapter's strongest sections.
3. Four of six worked scenarios (5.2, 5.3, 5.5, 5.6) omit "what would change the answer," a required
   element of every scenario per AGENT-BRIEF §3.5. Only 5.1 and 5.4 have it.
```

**Overall judgment.** The chapter's hard pedagogical job — reconciling a blueprint objective ("chain-of-
thought") with a mechanism that no longer works the way the objective implies — is done well, and the
caching and model-selection sections are the best material in the draft: genuinely method-first,
appropriately concrete, and load-bearing for the guide's own Sample-2 item shape. The defects are
specific and repairable: a broken coverage table, two exam-fairness-risking items, a structural gap in
half the scenarios, some Objective-4 thinning relative to what the dossier actually researched, no
cross-references to neighboring domains, and roughly 1,300–1,800 words over the domain's 3,500–5,000
target. None of this requires re-conceiving the chapter.

---

## Durable-vs-volatile audit

Verdict per section, with the required rewrite demand for every `TEACHES-SNAPSHOT` finding.

**§1 Front matter — TEACHES-METHOD.** Correctly frames the lineup as perishable and points to the
Models API for runtime capability checks (line 19) instead of a hardcoded table — this is the right
posture and should be a model for the rest of the course. **Defect, not a verdict downgrade:** line 15's
blanket verification claim is inaccurate for the six pending-status facts (see must-fix #1). **Fix:** add
one sentence: "The `400`-on-classic-levers findings (temperature/top_p/top_k, prefill, `budget_tokens`,
`thinking:disabled`, forced `tool_choice`, citations+structured-outputs) are reported by this course's
research pass and pending independent validation; treat the mechanism (schema-level determinism replacing
sampling-level determinism) as the durable lesson regardless of which specific 400s hold at exam time."

**§2 Exam-relevance framing — TEACHES-METHOD.** The distractor-archetype table (lines 34–41) names
patterns, not values, and matches the guide's own Sample 2 cognitive level. No snapshot risk.

**§3 Core concepts — BOTH.** "Cost per completed task," "context rot," "prompt caching as prefix
match," "the right altitude," and "Agent Skill" are durable, mechanism-first definitions with correctly
identified misconceptions — TEACHES-METHOD. Two entries lean on unconfirmed volatile facts stated as
settled: "Effort" (line 54–58) and "Adaptive thinking" (line 60–66) both assert the 400-on-disable and
`budget_tokens`-deprecated facts without hedging, and "Structured outputs" (line 92–96) asserts prefill
returns 400 as the reason structured outputs is now required. **Rewrite demand:** keep the concepts —
they are correctly the load-bearing determinism story of the domain — but change "returns 400" to "is
currently rejected on the top-tier models (verify against the model's parameter-support docs before
relying on it)" everywhere it appears, so the concept's *durable* claim (effort/schema-level control
supersedes sampling-level control) is decoupled from the *volatile* claim (which specific call currently
errors). Also add the Haiku 4.5 caveat: manual `budget_tokens` extended thinking is not a deprecated
relic everywhere — it is the *only* thinking mechanism Haiku 4.5 supports (off by default), so "manual CoT
is the fallback for thinking-off models" needs a one-clause exception naming Haiku 4.5, or a multi-model
exam item about Haiku's thinking will read as contradicting this concept.

**§4 Trade-off analyses — TEACHES-METHOD, the chapter's strongest section.** §4.1's capability-first row
states the exact sanctioned sequence (start Opus 5.5 → optimize prompts for that model → evaluate → lower
effort or downgrade → only move tiers if evals at `xhigh`/`max` still fall short) and frames cost as
per-completed-task throughout §3/§4.1/§4.2/§4.3/item 2 — never reducible to "big model = hard task." §4.5
(caching) teaches mode, TTL, and placement as decision procedures with worked breakeven arithmetic, not a
value table. One gap, not a snapshot problem: the fact that changing top-level `effort` invalidates the
cache — explicitly named in the task brief as "exam-grade material" and confirmed (not pending) in
VERIFIED-FACTS — is taught only inside item 3's rationale (line 423), never stated in §4.5's own body. A
candidate who reads §4 without first working the items never learns it. **Fix:** add one sentence to
§4.5's TTL/placement table or discussion: "Changing top-level `effort` between requests reshapes the
rendered prompt and invalidates every cached breakpoint at or after it — hold effort constant within a
cached conversation; vary it across workloads, not within one." Also missing: the `adaptive`-is-a-
thinking-mode-not-an-effort-value trap (a concrete, decidable, VERIFIED-FACTS-confirmed mechanic, not a
pending one) — good exam material currently absent from the whole chapter.

**§5 Worked scenarios — BOTH.** 5.1, 5.3, 5.4, 5.5 reason from durable architecture (traffic-pattern TTL
choice, Batch + enum, externalized state, workspace-scoped Skill isolation) — TEACHES-METHOD. 5.6 is
durable but redundant with existing content (see Cut list). **5.2 is TEACHES-SNAPSHOT:** its entire
"why the alternatives lose" argument for options A and D rests on the pending citations+structured-outputs
incompatibility ("returns 400... the restriction is on the request," line 275). If that specific
restriction is not confirmed, option A (one request) becomes strictly better than the recommended answer
(fewer calls, same guarantees), not just a distractor. **Rewrite demand:** keep the two-request
recommendation, but ground it in a durable reason independent of the 400: citations return API-computed
spans traceable to source bytes, while a schema-constrained JSON generation pass asks the model to also
*produce* a quote field, which is model-authored regardless of whether the two features can technically
coexist in one call — the auditability requirement specifically wants the API-computed kind. State the
400 as a secondary, dated observation, not the load-bearing reason.

**§6 Failure modes and diagnostics — TEACHES-METHOD**, with one snapshot-flavored row: "400 on a request
that worked on the previous model" (line 356) lists the six pending-status parameters as a fixed
enumeration. **Rewrite demand:** reframe the "first check" column as "consult the target model's current
parameter-support docs for the specific field" rather than presenting the list as settled fact; keep the
list as an illustrative "commonly affected" set, explicitly dated.

**§7 Anti-patterns — TEACHES-METHOD.** All seven are durable ("looks-right" reasoning plus the actual
cost). No snapshot risk, though see Cut list for redundancy with §4/§5/§6.

**§8 Exam-day heuristics — BOTH.** Heuristics 1–10 are durable tiebreakers. **Heuristic 11 is
TEACHES-SNAPSHOT:** "`temperature` is not a lever. Non-default sampling values return 400 on current
frontier models" (line 386) states a pending fact as an absolute, exam-day rule. **Rewrite demand:**
"Determinism now comes from schemas and forced structure, not sampling parameters — verify current
parameter acceptance before relying on `temperature`/`top_p`/`top_k`, and prefer structured outputs
regardless of whether the knob currently errors." This survives being right or wrong about the specific
400, which a heuristic meant to outlive the chapter's publication date must do.

**§9 Practice items — mixed**, see item-by-item section below; items 4 and 9 are the chapter's two
`VOLATILE-DEPENDENCY` cases.

**§10 Objective coverage / §11 Sources — not applicable to this axis** (audit and citation content, not
teaching content); see Findings for §10's accuracy problem.

---

## Cut list

Current: 6,315 words (section totals via `##` headings). Domain-specific target given to the researcher:
3,500–5,000. Recommendation: land at **≈4,900–5,000**, the top of the band — this is a fact-dense,
mechanism-heavy 13% domain with 8 trade-off tables and a hard reconciliation job; going toward the 3,500
floor is achievable only by cutting real coverage (a scenario, two items, or a trade-off table), which is
not recommended given axis priorities 1, 4, and 5. The budget below nets to ~5,000 after the required
additions (hedging language, missing scenario clauses, the effort-invalidates-cache sentence, the
`adaptive`-is-a-mode note).

| Section | Current | Target | Action |
|---|---|---|---|
| 1. Front matter | 126 | 145 | +1 sentence hedging the pending-validation facts (must-fix #1) |
| 2. Exam-relevance framing | 304 | 250 | Tighten archetype table's "why it loses" cells; keep all 6 rows |
| 3. Core concepts | 568 | 480 | Cut the SWE-bench-Pro digit recitation in "Cost per completed task" to one clause + citation (it repeats in §4); add the Haiku 4.5 thinking-mode caveat; hedge per rewrite demand above |
| 4. Trade-off analyses | 1875 | 1700 | **Protect.** Trim repeated "Measured:" digit strings in §4.2/§4.3 (e.g., §4.2's paragraph cites four separate benchmark pairs — keep two); add the effort-invalidates-cache sentence and the `adaptive`-is-a-mode note (~40 words); do not touch §4.5's caching mechanics or §4.1's sequence |
| 5. Worked scenarios | 1011 | 880 | Cut scenario 5.6 (Telecom) as a standalone scenario — its lesson (prompt cruft, tokenizer shift) duplicates the anti-pattern "Carrying settings across a migration" (§7) and item 7 almost exactly; fold its one unique fact (tokenizer ≈30% shift) into that anti-pattern in one clause. Add "what would change it" to 5.2, 5.3, 5.5 (~90 words total, must-fix #3). Reground 5.2 per the rewrite demand above (roughly flat length) |
| 6. Failure modes | 377 | 330 | Hedge the pending-facts row (rewrite demand above); tighten prose in 2–3 other rows |
| 7. Anti-patterns | 240 | 170 | Every one of the seven currently restates content already taught in §3/§4/§5/§6 in full sentences. Cut each to name + one-clause "looks right because X, but Y," with a parenthetical cross-reference instead of re-explaining the mechanism (e.g., "Marker-first caching... (see §4.5)"). Absorb 5.6's tokenizer fact here (~20 words) |
| 8. Exam-day heuristics | 205 | 185 | Reword heuristic 11 (rewrite demand above, same length); no other cuts needed |
| 9. Practice items | 1256 | 1000 | Cut item 4 outright — its lesson is already carried by (rewritten) scenario 5.2, and it is the more exam-fairness-risky of the two 400-dependent items since it stacks two pending facts in one item. Rewrite item 9 per the item-by-item section below (should not grow). Tighten rationale prose in items 2, 6, 7 by ~10%. Result: 9 items, still within AGENT-BRIEF §3.9's 8–12 |
| 10. Objective coverage | 127 | 150 | Rebuild the table per the must-fix #2 finding (net addition, not a cut) |
| 11. Sources | 226 | 180 | Tighten the prose source list; the `[UNVERIFIED]` list is already good, keep it in full |
| **Total** | **6,315** | **~4,990** | |

If the editor needs headroom below 5,000, the next lever (not first-choice) is dropping one more scenario
(5.5 Insurance, whose governance lesson is otherwise fully carried by §4.7's table) rather than touching
§4's caching or model-selection material.

---

## Findings

**[BLOCKER] Front matter line 15; §3 lines 62–63, 74, 95–96; §6 line 356; §8 line 386; item 9 lines
482–490; item 4 lines 426–435; scenario 5.2 lines 264–279 — chapter certainty outruns its own evidence
status.** VERIFIED-FACTS.md states these six behaviors are "reported by the Domain 2 researcher and
pending validator confirmation — do not state these as fact in a chapter until the Domain 2 validation
file confirms them." The draft states all six as unconditional fact in at least one location each, and
two full practice items plus one scenario have no correct answer if any single one turns out false.
**Required fix:** apply the hedging rewrites specified in the Durable-vs-volatile audit; do not publish
items 4 and 9 in their current form regardless of what validation finds, because the *design* (correctness
resting entirely on "returns 400") is fragile even if the fact is confirmed true today — a later model
could re-permit the parameter and silently break the item.

**[BLOCKER] §10 (lines 506–512) — objective-coverage table is mismapped, not just optimistic.** Detailed
mapping errors: Objective 1's row cites §4.8 (Guardrails), which has nothing to do with model selection;
Objective 2's row cites §4.6 (context-window strategy) and §4.7 (prompt-reuse shapes) but never §4.8
(Guardrails), which is the section actually written for this objective; Objective 3's row cites §4.2
(one-model-vs-two) but never §4.4 (zero-shot vs. few-shot), the section actually written for this
objective; Objective 4's row cites §4.5 (caching) but never §4.6 (context-window strategy), the section
actually written for this objective; Objective 5's row cites §4.4 and §4.6 but never §4.5 (caching) or
§4.7 (reuse shapes), the two sections actually written for this objective. This reads as the table having
been drafted against an earlier §4 ordering and never updated after §4 was reorganized. **Required fix:**
rebuild the table from the actual §4.1–4.8 topics; also re-audit the item citations in the same table (item
2 is cited under Objective 3 but tests model-tier escalation, not zero-shot/few-shot/CoT; item 4 is cited
under Objective 5 but tests citations/structured-outputs, which belongs under Objective 2 or 3; item 5 is
cited under Objective 4 but is a pure caching-mechanics item, Objective 5's territory).

**[MAJOR] §5, four of six scenarios (5.2 lines 264–279, 5.3 lines 280–295, 5.5 lines 312–326, 5.6 lines
328–343) — missing "what would change the answer."** AGENT-BRIEF §3.5 requires this element for every
scenario; only 5.1 (lines 260–262) and 5.4 (implicit in "Compaction stays as a within-window mechanism")
have it, and 5.4's is thin. **Required fix:** add one sentence per scenario. Suggested forks: 5.2 — if the
citations+structured-outputs restriction did not exist, would a single request with both features still
be worse (yes, per the reground rationale above — this is a good place to demonstrate the fix); 5.3 — if
the 380 categories were not fixed but growing weekly, enum-constrained structured outputs stops being a
clean fit and few-shot classification re-enters consideration; 5.5 — if two carriers legitimately needed
divergent logic (not just data), the "80% shared" assumption breaks and the design becomes two Skills, not
one with variables; 5.6 (if kept, see Cut list) — if accuracy *had* dropped post-migration, the diagnosis
would point to the model change itself, not prompt cruft.

**[MAJOR] Objective 4 (context windows/token usage) is thinner in the draft than in the dossier's own
research.** The dossier's Objective-4 findings (dossier lines 160–179) include several vivid, durable,
exam-worthy mechanisms that did not make it into the draft: the Files-API-vs-inlining example (a CSV
pasted inline scored 6/25 at $5.01; the same data computed via code execution scored 25/25 at $0.40 — ~12x
cheaper *and* more accurate, dossier line 88/177), `count_tokens` as an ingestion gate on unbounded user
input, image tokenization economics (≈1 token per 28×28 pixel patch), programmatic tool calling's
documented 24%-fewer-input-tokens result, and the ~10K-token/~20-tool breakeven for tool search. The draft's
§4.6 mentions "Files API + code execution" and "tool search with `defer_loading`" only as one-word
mentions inside a table cell (lines 201). **Required fix:** port the Files-API contrast (it is the single
most memorable, durable illustration in the dossier — inlining large tabular data is worse *and* more
expensive than sandboxed compute, a lesson that survives any price change) and the tool-search breakeven
number into §4.6 or §6, funded by the Cut list's §5/§7 trims.

**[MAJOR] No cross-references to neighboring domains anywhere in the chapter.** Three concrete seams:
(a) §4.6's "retrieve / progressive disclosure" row and the tool-search/`defer_loading` mention are the
same territory as Domain 3's explicit objective "Evaluate progressive discovery vs. monolithic context
strategy." **Recommended split:** Domain 2 owns *what* content strategy relieves context rot and how it's
costed (token/cache economics); Domain 3 owns *how* a tool/agent configuration is evaluated for capability
bloat and which discovery mechanism (MCP tool search, dynamic loading) is architecturally appropriate. Add
a one-line cross-reference at §4.6. (b) §4.2's advisor/orchestrator patterns overlap Domain 1's "design
multi-agent systems and orchestration strategies" — Domain 2 should own the cost-per-completed-task lens
on a cascade, Domain 1 the pattern-selection lens; cross-reference at §4.2. (c) §4.1's stepping-down method
and §5.6's diagnosis both depend on having an eval to sweep against — that construction is Domain 4's
territory ("Optimize token usage, latency, and cost-performance trade-offs," "Diagnose system issues...
model mismatch"). Cross-reference at §4.1 and wherever 5.6's content lands after the cut.

**[MAJOR] Scenario 5.1 and item 1 mirror the exam guide's own Sample 2 too closely on specifics, not just
shape.** Guide Sample 2: ~8,000 static tokens (system prompt + policy), a short varying user message,
latency and cost both named, answer = order static-first and cache. Scenario 5.1: 900 + 7,100 = 8,000
static tokens, 40–200-token question, "p95 latency is the complaint, cost second." AGENT-BRIEF hard rule 2
allows the guide's samples to be "discussed as style references," not re-skinned with the same token
totals. **Required fix:** change the numbers (e.g., a 3,200-token system prompt, a 22,000-token multi-
document policy corpus, a 400–900-token question) so the scenario is recognizably original while keeping
the same *shape*, which is correctly the point.

**[MINOR] §3 "Effort" concept and §4.1 both state Opus 5.5's default as `medium` with no forward-looking
caveat that per-model defaults are exactly the kind of number due to shift.** Not wrong, but pair it with
the existing "verify via Models API" framing from the front matter rather than stating it as chapter-wide
received wisdom in two more places.

**[NIT] §11 Sources (lines 521–530) is a prose list of IDs, not the table format AGENT-BRIEF §6 implies
for a resolved source list.** Low cost to fix at editor stage; the `[UNVERIFIED]` list itself (lines
527–530) is honest and complete and should be kept as-is, just re-formatted.

---

## Practice items — item-by-item

Set: 10 items (8 single-response, 2 multiple-response), each states how many to select — meets
AGENT-BRIEF §3.9. Recommend cutting to 9 per the Cut list (drop item 4).

**Item 1 (cache breakpoint on unique tail, select 1) — PASS.** Pure mechanism, no volatile dependency,
closely and appropriately matches the guide's Sample-2 skill via an original scenario. Rationale correctly
disposes of all three distractors on architectural grounds.

**Item 2 (evals fail at `xhigh`/`max`, select 1) — PASS.** Generic "current default model" / "highest-
capability model" framing avoids naming a specific model, so it will not date. Correctly tests the
capability-first escalation gate rather than a static capability table. No volatile dependency.

**Item 3 (which changes preserve a cached prefix, select 2) — PASS.** Tests confirmed (non-pending)
mechanics: mid-conversation system messages, `tool_choice` auto→none leaving the messages cache intact,
top-level effort invalidating the cache (confirmed in VERIFIED-FACTS, not on the pending list), and
model-scoped caches. No volatile dependency. This item currently carries content (effort invalidates
cache) that should also be stated in §4.5's body — see the Durable-vs-volatile finding.

**Item 4 (citations + structured outputs, select 1) — `VOLATILE-DEPENDENCY`, BLOCKER, recommend CUT.**
Every distractor is eliminated by asserting a 400 that is explicitly pending validation (twice — once for
combining the features directly, once for wrapping the combination in a `strict` tool). If either 400 does
not hold, two of four options become defensible and the item has no single best answer. Its lesson is
otherwise fully carried by the (rewritten) scenario 5.2. Recommend removing it rather than patching it,
since patching would require the same rationale rebuild as scenario 5.2 for no net new coverage.

**Item 5 (cache-creation ≈ full conversation, sequential tool calls, select 1) — PASS.** Tests the
20-position lookback window and the tool_use/tool_result collapse rule, both confirmed mechanics, not
pending ones. Well-constructed distractors (byte-identical overlap explicitly rules out C; conversation
size rules out D).

**Item 6 (prompt injection, select 2) — PASS.** Tests message-shape defense and least-privilege removal,
neither dependent on any pending fact. Good distractor set: B is a real recommendation correctly demoted
to "not a guarantee," D is cleanly detective, E correctly demoted as effort buying reasoning depth, not a
security boundary.

**Item 7 (post-migration prompt cruft, select 1) — PASS.** Diagnostic reasoning is durable (same accuracy,
more cost/latency after an ID-only change → audit the prompt first); the specific percentages in the
rationale are illustrative, not required to answer. No volatile dependency, though this item and scenario
5.6 teach the identical lesson — after the 5.6 cut (Cut list), this becomes the chapter's sole carrier of
that lesson, which is the right outcome.

**Item 8 (multi-tenant Skill isolation, select 1) — PASS.** Tests workspace-scoped isolation and version
pinning as governance mechanisms, not a value or default. No volatile dependency.

**Item 9 (prefill removed, correct replacement, select 1) — `VOLATILE-DEPENDENCY`, BLOCKER, REWRITE.** The
rationale eliminates A (temperature) and C (forced `tool_choice`) by asserting two separate pending 400s in
addition to the prefill 400 the stem itself is built on — three pending facts stacked in one item, the
worst case in the set. **Required fix:** keep the stem (prefill removed after an upgrade) since prefill
returning 400 on 4.6+ is the most load-bearing and most-cited of the pending facts, but change the
rationale for A and C to architectural grounds that hold regardless of whether those specific calls
currently error: A loses because a fixed low temperature narrows the sampling distribution but gives no
schema guarantee, which is what the bulk-extraction job actually needs; C loses because forcing a specific
tool still returns free-form text in that tool's `input`, not a validated object, unless paired with
`strict: true` — and even where `strict` is available, D02-S21 documents it is "not compatible with
programmatic tool calling," so it does not compose cleanly with a bulk pipeline the way `output_config.format`
does. This makes B correct on its own merits, not by process of eliminating options via unconfirmed errors.

**Item 10 (1M context-window facts, select 2) — PASS WITH MINOR VOLATILE-DEPENDENCY.** B and D are
durable and confirmed (flat pricing regardless of context length; cached tokens still occupy the window).
Options A and C, however, require recalling current specifics (no beta header for 1M context; Haiku 4.5's
window is 200K, not 1M) rather than reasoning from a principle — this is closer to the "recall a limit
value" pattern axis 9 warns against, even though it is not disqualifying since the item's *correct*
answers (B, D) do not depend on it. **Recommended fix:** replace C with a durable-reasoning distractor,
e.g. "A 1M-token request always completes faster than a 200K-token request on the same model" (false on
architectural grounds — larger prompts take longer to process regardless of window ceiling — decidable
without knowing any model's specific window size).

---

## Must preserve

The editor must not delete or thin any of the following while cutting toward the word target:

1. **§4.1's capability-first sequence and stepping-down method** (lines 106–120). This is the chapter's
   best answer to "model selection as method": start at the top, optimize for that model, lower effort or
   downgrade over time, only change tiers when evals at `xhigh`/`max` still fall short, and cost is priced
   per completed task with the tail specifically called out. This is exactly what axis 4 demands and it is
   already done correctly — do not compress it to make room for cuts elsewhere.
2. **§4.5 in full** (lines 170–194), including the JSON code block showing render order and breakpoint
   placement. This is the deepest, most exam-relevant material in the chapter and matches the guide's own
   Sample 2 shape. The breakeven arithmetic (5-minute pays back on request 2, 1-hour on request 3) is
   exactly the kind of concrete mechanic axis 1 says must not be sacrificed to over-abstraction.
3. **§3's "Adaptive thinking" concept plus §4.3's discriminator plus heuristic 10** — together this is the
   chapter's reconciliation of the CoT objective with the current mechanism (adaptive thinking calibrated
   by effort and query complexity; manual `<thinking>` as the fallback, not the default; naming when
   thinking tokens are wasted). This triad is the hardest pedagogical job in the domain and it is handled
   well; the fix required (hedging language) does not touch the underlying teaching.
4. **§4.8's three-layer guardrail table** (lines 226–238) and the message-shape framing of prompt
   injection. Precise, decidable, and correctly distinguishes "what each layer can and cannot guarantee" —
   this is architect-altitude content, not prompt-writing tips.
5. **§4.6's four-strategy context table** (lines 198–207) and the explicit statement that context editing
   "cost more than it saved" in Anthropic's own measured run — a genuinely counter-intuitive, durable, and
   memorable finding that should not be cut for space.
6. **§2's distractor-archetype table** (lines 34–41) — this is the correct level of abstraction for
   "exam-relevance framing" and should be a model for other domains.
7. **§5.4 (Government) in full** — the "compaction isn't sufficient" finding and the externalize-state
   recommendation is a genuinely non-obvious, well-sourced lesson and the scenario's fork logic is sound.

---

## Coverage matrix

| Objective | Covered adequately? | Evidence |
|---|---|---|
| 1. Select appropriate Claude models based on trade-offs | **Yes** | §3 (cost per completed task), §4.1 (sequence method), §4.2 (single vs. cascade with hidden costs), §5.3/§5.6 scenarios, items 2/7. Strong, method-first, matches axis 4's exact requirement. Coverage-table row is wrong (cites §4.8) but the actual content is sound. |
| 2. Design system prompts, templates, and guardrails | **Yes, but mis-cited** | Real content: §3 ("the right altitude"), §4.8 (three-layer guardrail table), §5.5 scenario, §7 anti-pattern "prompt-as-policy," items 6/8. The §10 table never cites §4.8 for this objective — a documentation defect, not a coverage defect. |
| 3. Apply prompt engineering techniques (zero-shot, few-shot, CoT) | **Partial — zero-shot is thin, CoT is strong** | §4.4 covers zero-shot in one table row and one sentence — thin relative to few-shot and CoT, and zero-shot is one of three techniques named explicitly in the objective. CoT is the chapter's strongest reconciliation (see Must preserve #3). Few-shot is well covered (§4.4, §7 anchoring anti-pattern). Gap: no coverage of the Haiku 4.5 manual-thinking exception (see Durable-vs-volatile audit). |
| 4. Optimize context windows and manage token usage | **Partial, thinner than the dossier supports** | §3 (context rot/attention budget), §4.6 (four strategies), §5.4 scenario, §6 failure modes, item 10. Missing the dossier's Files-API-vs-inlining example, `count_tokens`-as-gate, image tokenization, programmatic tool calling's token savings, and the tool-search breakeven number — all durable, all cheap to port (see MAJOR finding). |
| 5. Implement prompt reuse strategies (caching, modular prompts, Skills) | **Yes — the chapter's deepest objective** | §4.5 (caching mode/TTL/placement/breakeven), §4.7 (inline/templated/Skill governance table), §5.1/§5.2/§5.5 scenarios, §6, §7, items 1/3/5/8. All of axis 5's required elements are present except the effort-invalidates-cache fact is taught only inside an item's rationale rather than in §4.5's body (see finding), and the dossier's explicit cache-preserving-escape-hatch table never made it into the chapter body (only implied in item 3). |

---

## Sources

No new external sources were consulted. All citations above reference the dossier's existing `D02-S##`
IDs as they appear in `research/02-models-prompting-context-dossier.md` and the draft, plus
`VERIFIED-FACTS.md` and `AGENT-BRIEF.md`, both supplied in-task. No new `D02-R##` rows are required.
