# Adversarial review — Domain 4: Evaluation, Testing & Optimization

Reviewed: `research/04-evaluation-testing-optimization-dossier.md`, `drafts/04-evaluation-testing-optimization-draft.md`,
against `AGENT-BRIEF.md`, `VERIFIED-FACTS.md`, and the exam guide (Sample 3, §6, §8).

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. The cost-optimization content (§3.5–3.7) never states that changing top-level `effort` invalidates the
   prompt cache, even though the diagnostic table (§5, "cost per request jumped") already knows this fact.
   This corrupts the chapter's own "sweep effort" methodology (S3, §3.7) and omits the Opus-5.5-defaults-to-
   `medium` gotcha as a cause in the "quality drop after a model swap" row, where the prescribed fix
   (re-author the prompt) is actively wrong if the true cause is an unset effort default.
2. Practice item 6 is quantitatively defective: the chapter's own stated batch cache hit-rate range
   (30–98%, §3.6) means the "correct" answer (cache-on) is only cheaper above roughly a 53% hit rate under
   the stated discount-stacking rules — below that, cache-off is cheaper. The item asserts no hit-rate
   floor, so a well-prepared candidate can defend the "wrong" answer with the chapter's own numbers.
3. The flagship diagnostic row ("confident-but-wrong after a data refresh ⇒ retrieval") pairs a
   correctly-discriminating probe with a too-narrow fix list (re-index / embedding parity) that does not
   cover a same-day permission/ACL filter change or a chunking regression — both produce the identical
   "retrieved chunks lack the answer" signature but need entirely different fixes.
```

---

## Attacks that landed

`[BLOCKER] §3.5–§3.7, cost/effort optimization` — The chapter teaches "sweep effort" as a standard
hillclimbing lever (S3 scenario, §3.7 "model × effort staircase") and separately teaches "validate a
caching diff on a warm cache or the 1.25× writes dominate" (§3.6) — but never applies the analogous warning
to effort. VERIFIED-FACTS is explicit that changing top-level effort invalidates cached prefixes while a
per-message effort change (beta) preserves them. **Counter-scenario:** a team runs an effort sweep
(low/medium/high) to find the cheapest cell that clears the quality bar. Each effort-level switch re-bills
the full cached prefix as a fresh write. If they measure "cost per request" on the first request at each
level, low effort's true steady-state savings are masked by a one-time cache-write charge, and medium/high
levels look artificially cheap if their first sampled request happened to hit a warm cache from a prior run
at the same level. The chapter gives no instruction to control for this, despite giving the identical
warning for the caching-vs-caching-off comparison one section earlier. **Fix:** add a sentence to §3.5/§3.7:
"Effort participates in the cache key; changing top-level effort between requests forces a full cache-write
re-bill. Warm the cache at each effort level before comparing costs, or use the per-message effort beta
(preserves cache) where the model supports it." Cross-reference the existing §5 row that already states this.

`[BLOCKER] §5 triage table, row "Quality drop after a model swap"` — Candidate causes offered are "prompt
debt across generations" and (implicitly) reduced capability. **Counter-scenario:** a team migrates within
the same family (e.g., an Opus-generation upgrade) and does not set `effort` explicitly. If the new model
defaults to a lower effort level than the old one, output quality drops for a reason that is neither prompt
debt nor a capability regression — it is an unset default. Following the chapter's prescribed probe ("golden
set on both models, then a prompt audit") would lead the analyst to re-author the prompt to compensate for
what is actually a one-line `effort` fix, and the audit might even "succeed" by accident (a more explicit
prompt partially compensates for lower effort) while never surfacing the real lever. VERIFIED-FACTS calls
the effort-defaults-differ-by-model fact "the single most important correction... it changes Domain 4's
cost/latency levers" — this is exactly the row it should have landed in. **Fix:** add "effort default
differs across model generations/tiers; confirm the effective `effort` on both arms before concluding
prompt debt" as a third candidate cause with its own discriminating check (log the request's effective
`effort` value, not just the model ID).

`[MAJOR] §5 triage table, row "Confident-but-wrong after a data refresh"` — The probe ("log retrieved
chunks for a failing query") correctly discriminates retrieval-broadly from non-retrieval causes, but the
**fix column only offers two remedies (re-index; verify embedding parity)** for a symptom that has at least
four distinct root causes with the identical "chunks lack the answer" signature: (1) stale/broken re-index,
(2) embedding-model version mismatch, (3) a same-day permission/ACL filter change hiding still-valid
documents from a subset of users, (4) a chunking-strategy regression that fragments the answer across
chunks. Re-indexing does nothing for (3) or (4). **Counter-scenario:** a legal/financial RAG system ships a
document refresh and an access-control update in the same release; retrieved chunks for affected users
genuinely lack the answer (because it's now filtered, not stale); "re-index" is prescribed and does nothing;
the investigation stalls exactly where the chapter claims it should not. **Fix:** expand the fix column to
"re-index; verify embedding parity; **diff the retrieval filter/ACL policy for same-day changes; verify
chunk boundaries around the affected passage**," and add "same symptom, different cause" callouts the way
the worked scenario (S1) already does for the manual-context-paste confirmatory test — but that confirmatory
step lives only in prose (S1), not in the reference table itself, which is the artifact meant to double as a
triage reference per AGENT-BRIEF §3.6.

`[MAJOR] §3.4 canary/A-B guidance` — Canary (1%→5%→20%→50%→100%, rollback on p99/refusal thresholds) and
A/B testing are presented as the standard validation path for any serving-behavior change, with no exception
for safety-critical or irreversible-harm domains. **Counter-scenario:** a change to a self-harm-response
flow, a medical dosage recommendation, or a content-moderation bypass. Exposing even 1% of live users before
the change has cleared adversarial/expert review is itself the harm the exam's governance domain (5) exists
to prevent, and "24–48h minimum per stage" is not a safety property — a bad cell can hurt real users for two
days before rollback triggers. The chapter's own worked scenarios never test this boundary (S4's government
scenario is about injection resistance, not about whether to canary a safety-critical change at all).
**Fix:** add a qualifier to §3.4: "canary and A/B assume the failure mode is reversible and boundedly costly;
for irreversible-harm domains, gate on offline adversarial + shadow + expert/internal-user review, and treat
any live exposure as a governance decision, not a testing default."

`[MAJOR] §3.1/§7 heuristic 5 ("validate the judge before trusting it")` — No bootstrapping path is given for
a first-week project with zero labeled data, even though the dataset-size guidance elsewhere ("20–50 cases
is a great start") explicitly targets exactly this situation. Judge validation needs "a few dozen cases a
human labelled independently" — a separate, additional labeling cost the chapter never sequences against
the golden-set bootstrap. **Counter-scenario:** a team building its first eval this week has no labels at
all and a deadline. Following "never trust an uncalibrated judge" literally blocks any judge-graded gate
indefinitely. **Fix:** state the fallback explicitly: code-based/structural checks only until calibration
data accumulates; judge scores are advisory (dashboard, not gate) until the human-labeled calibration set
exists; calibration labels can be drawn from the same 20–50 seed cases used to build the golden set, so the
two efforts are not additive from scratch.

`[MAJOR] §3.4/§3.7/item 10 — no low-traffic alternative to A/B` — "A/B when the decision hinges on user
outcomes and the traffic exists; otherwise you will read noise" correctly gates the decision but gives no
alternative branch. §3.7 quotes "tens of thousands of sessions per arm" for a 5% MDE as if it were a
universal target. **Counter-scenario:** the exam's own stated audience skews toward financial services,
healthcare, gov, and enterprise B2B — deployments that may never see tens of thousands of sessions per arm,
ever. The chapter gives these architects no prescribed path (wider non-inferiority margins on whatever
traffic exists, longer observation windows, cohort/named-account ramps instead of percentage ramps, heavier
reliance on shadow + expert review as the terminal validation rather than a means to an eventual A/B).
**Fix:** add a "traffic-constrained" branch to §3.4/§3.7 naming these alternatives explicitly.

`[MAJOR] §3.5 lever table — missing alternative` — VERIFIED-FACTS states the docs' own model-selection
method is "default → raise effort → only then change model." The chapter's lever table documents effort
**reduction** (lowering effort to save money) but never states the symmetric case: raising effort on the
current/cheaper model as an explicit alternative to upgrading to a pricier model for a quality shortfall.
Heuristic 7's ordering ("effort → model last") implies this but the "Effort" row itself only shows the
cost-cutting direction. **Fix:** add a row or sentence: "quality shortfall on the current model: raise
effort before switching models; only change model when evals at the current model's highest supported
effort still fall short" — this is a plausible exam distractor pattern ("the answer looks like a model
upgrade; the correct answer is raise effort first") and the chapter currently doesn't arm the candidate for it.

`[MINOR] §7 heuristic list vs §3.5 prose` — The exam-day heuristic "caching → input hygiene → loop hygiene →
output → batch → effort → model last" is stated without its own stated exception ("once an eval exists, walk
model × effort early"). Heuristics are explicitly designed to be memorized standalone as tiebreakers; the
exception living only in prose one section away risks being dropped exactly where it matters most.

`[MINOR] §3.4 canary ramp` — "1%→5%→20%→50%→100%" with no traffic-volume qualifier. At low daily-active-user
counts, 1% is functionally a handful of named accounts, not a statistical sample — worth a one-line caveat.

`[MINOR] Missing coverage: task budgets` — VERIFIED-FACTS names "task budgets" (advisory token budget for an
agentic loop) as "related surface worth covering" for Domain 4's cost/latency optimization objective. Absent
from the draft entirely.

`[MINOR] Item 4's practice rationale risks over-teaching "synthetic data = bad"` — see Missing alternatives
below.

---

## Diagnostic robustness audit

Per row of the §5 triage table (verdict: DISCRIMINATING = probe correctly isolates cause even under
substitution; WEAK = probe correctly rules in/out but the table doesn't route to the next hypothesis or its
fix list is too narrow; MISLEADING = probe/fix actively points the wrong direction under a plausible variant).

| Row | Counter-case (same symptom, different cause) | Verdict |
|---|---|---|
| Confident-but-wrong after data refresh | Permission/ACL filter hides valid docs same day; chunking regression fragments the answer | **WEAK** — probe discriminates retrieval-vs-not correctly, but fix list (re-index, embedding parity) doesn't cover either variant |
| Confident-but-wrong after a prompt edit | A floating model alias moved the same day as an unrelated cosmetic prompt edit | **WEAK** — re-running the golden set on the old prompt would correctly fail to recover (ruling out the prompt), but the row never routes to "assert served model from the response" as the next step, even though that exact discipline is taught elsewhere (item 2) |
| Output correct, unparseable | A prompt-template edit changed the output-format instruction (not truncation, not a missing schema) | **DISCRIMINATING** — `stop_reason` cleanly separates truncation from everything else; only gap is no explicit "if not truncation, check the rendered format instruction" next step |
| One case fails every round | The case is the longest input and reliably times out (infra flake), not a grader bug | **WEAK** — if the harness conflates infra errors with scored rows (the exact anti-pattern the chapter itself names elsewhere), "read the output" may show a garbled result and misdiagnose infra as a grading bug; the row should say "check the errors sidecar first" the way the harness-noise row already does |
| Quality drop after a model swap | Effort-default differs between model generations/tiers (Opus-5.5-style default change); or the golden-set labels/distribution drifted, not the model | **MISLEADING** — the prescribed fix (re-author the prompt) is actively wrong when the true cause is an unset effort default; see BLOCKER above |
| Cost per request jumped | Legitimate traffic-mix shift (longer inputs/outputs), not a cache invalidator | **DISCRIMINATING** — reading `usage` correctly separates cache health from other cost drivers; minor gap only |
| p95/p99 up, p50 flat | A prompt/quality change legitimately requires more tool calls or longer output on hard queries (extra work is warranted, not a regression) | **WEAK** — the row correctly attributes E2EL-up to output length, but the prescribed fix (cap top-k, shorten outputs) can actively harm quality if the extra work was necessary; no gate on "is this a quality-driven change" before applying latency levers, despite the chapter's own quality-first doctrine (§3.5, D04-S12) |
| Eval score swings, no code change | A floating alias drifted mid-week, producing a genuine (not noise) shift that a no-change control might not catch if the control also calls the drifting alias | **WEAK** — same systemic gap as row 2: "assert served model" isn't cross-referenced into this row |
| Agent follows instructions from a document | An over-permissive system prompt authorizes following document instructions (a design flaw, not an attack); content correctly arrives via `tool_result` | **WEAK** — the stated check (delivery channel) passes even though the system is still misbehaving; fix list doesn't include auditing the system prompt for instruction-following grants |

**Systemic finding:** across rows 2, 4, and 8, the table teaches good rule-out probes but never says where to
look next when the probe rules out the primary hypothesis. A table meant to double as a triage reference
(AGENT-BRIEF §3.6) should chain to a "if ruled out, check X" pointer, especially since the chapter elsewhere
teaches the very facts (served-model assertion, errors-sidecar-first) that would fill the gap.

---

## False-precision audit

| Number | Where | Transplant scenario that misleads | Condition it needs |
|---|---|---|---|
| Noise-floor half-width ≈ `1/sqrt(n·reps)` (25×2≈±14, 50×2≈±10, 100×2≈±7) | §2.4, item 3 | This is the **p≈0.5 worst-case** approximation. At a saturated 95% baseline (which the chapter itself says is common and calls out separately), the true 95% CI half-width at 25×2 is ≈±6 points, not ±14 — more than double the apparent precision. A real 8–10-point improvement at a saturated baseline would be wrongly dismissed as "inside the noise floor" by a candidate applying the taught formula literally. | State the formula assumes pass rate near 50%; near-saturated baselines have a materially tighter true CI and should use `1.96·sqrt(p(1-p)/n·reps)` with the observed p, not the generic rule of thumb. (Item 3 itself is unaffected — its baseline, ~67-71%, is close enough to 50% that the naive and corrected formulas agree; the risk is in future items or real use at more extreme baselines.) |
| Cache break-even worked example: "1.25× write + 0.1× read = 1.35× vs 2× uncached" | §3.6 | Uses the generic 0.1× read rate. Transplanted to Fable 5.1/Mythos 5.1 (0.025×) or Opus 5.5 (0.05×), the exact ratio is wrong (1.275× or 1.30×, not 1.35×) even though the qualitative "pays off after one read" conclusion still holds. An exam item asking for the precise break-even ratio on a named current model would be miscalculated by a candidate who memorized 1.35× as universal. | State inline: "using the 0.1× base rate; substitute the model-specific read discount (0.025×/0.05×) for an exact figure — the qualitative break-even-after-one-read conclusion holds across all of them." |
| "Agent-loop cost cut 2.5–3.7× at 81–90% hit rates; one triage agent's bill fell 83%" | §3.5 | Presented in a ranked lever table as prompt caching's "measured effect," inviting generalization to "caching always yields this." At a genuinely low hit rate (short sessions, prefixes below the 512–4096-token cacheable minimum, request gaps exceeding the TTL), the multiplier collapses toward 1× or **below** 1× (net loss from the write premium). The hit-rate precondition is present in the same cell but easily read as color, not as a load-bearing qualifier. | Make the hit-rate precondition a first-class condition, not a trailing clause: "yields this multiplier only when hit rate stays above ~80%; below that, verify in `usage` before claiming savings." |
| Batch cache hit rates "observed 30–98%" (§3.6) vs. item 6's answer key assuming caching-on beats caching-off | §3.6, item 6 | Under the stated discount-stacking rule (batch 50% off stacks with cache multipliers), a cache **write** in-batch costs 2×·0.5 = 1.0×, i.e. double the plain uncached-batch rate of 1×·0.5 = 0.5×; only a cache **read** (0.1×·0.5 = 0.05×) beats it. Expected cost with caching = `(1-h)·1.0 + h·0.05` vs. `0.5` uncached ⇒ caching only wins above **h ≈ 52.6%**. The chapter's own stated range (30–98%) straddles that crossover, so "batch + caching wins" is not universally true even in the exact scenario item 6 describes. | Either state a hit-rate floor assumption in the item stem, or note explicitly in §3.6: "in-batch caching only pays off above roughly a 50% hit rate under these discount-stacking rules; below that, disable caching for the batch." |
| Effort-reduction yields ("low gives up 1–3 points for a third to a half off"; "~93% pass at $0.70/task, failures re-run at default") | §3.5 | The "run cheap, retry failures at default" strategy silently assumes a **cheap, reliable failure detector** (tests passing, exact-match) exists. Transplanted to open-ended/subjective tasks (summarization quality, judge-graded work) there is no free signal for "which outputs to retry" — determining that requires a judge call, which erodes or eliminates the savings the pattern promises. | State the precondition: "this retry-at-default pattern requires a cheap, deterministic failure signal; it does not transfer to judge-graded or open-ended tasks without first paying for the judge call that would tell you which cases to retry." |
| Reps as independent samples (implicit in the `n·reps` noise formula) | §2.4 | At low/zero temperature or otherwise low-entropy decoding, repeated reps of the identical case can return near-identical outputs — not independent draws — so `n·reps` overstates the effective sample size and understates the true noise floor. | Note that reps only add independent information when the pipeline has genuine per-call stochasticity (temperature, sampling); otherwise treat reps as diagnostic-only (catching flaky infra) rather than as a noise-reduction lever. |
| "Plan for tens of thousands of sessions per arm" (5% MDE, 80%/95%) | §3.7, dossier flags D04-S29 as secondary/practitioner | Presented in-table as a plain fact with equal footing to primary Anthropic figures elsewhere in the same table. A candidate has no signal that this number is directional/practitioner-sourced rather than a documented Anthropic constant, and might defend a specific numeric exam answer built on it. | Mark as directional/order-of-magnitude guidance from a secondary source, not a fixed target — the actual number is workload- and MDE-dependent (this is a question for the validator: is there any primary-sourced A/B sample-size figure to anchor this instead?). |

**Reverse check (over-hedged numbers that teach nothing):** no clear instance found. Vague-but-appropriate
guidance ("small but broad in attack classes" for adversarial sets) reflects genuine irreducible variability
rather than an author dodging a number that exists — that is a legitimate "it depends, and here is what it
depends on" per AGENT-BRIEF §1, not empty hedging.

---

## Item-by-item adversarial re-solve

**Item 1** (p95 +45%, p50/TTFT flat; best first action). Strongest alternative: D (enable streaming) — a
candidate could argue streaming is a legitimate "first action" since it's cheap and immediate. The chapter's
own material refutes it (streaming changes perceived latency only, not E2EL, which is what regressed), so C
remains correct. **Verdict: SOUND**, but the stem says "best first action" while the chapter's own distractor
archetype table criticizes "fix before diagnosis" items — tighten by rewording to "best first diagnostic
step" so the item doesn't undercut the lesson it's built on.

**Item 2** (protect a cheaper-model comparison; select two). B and C are unambiguously correct against the
chapter's own stated rules; A, D, E are each clearly wrong for stated reasons. **Verdict: SOUND.**

**Item 3** (25×2, 64%→71%; what do you say first). B is correct and — importantly — robust to the p=0.5
false-precision issue found above: at this baseline (~67%, close to 50%), the naive and baseline-corrected CI
half-widths are close (≈14 vs ≈13), so the item's conclusion doesn't change under the correction.
**Verdict: SOUND**, and a good example of an item that reasons rather than requiring a memorized constant.

**Item 4** (index rebuild, superseded clauses; which evidence best confirms cause). B is best among the four
choices regardless of which retrieval sub-cause (stale index, embedding mismatch, permission filter,
chunking) is true — the item asks for confirming evidence of "retrieval," not the specific mechanism, so it
survives the diagnostic-table gap found above. **Verdict: SOUND.**

**Item 5** (reduce judge bias; select two). A, D correct. E (average with cosine similarity) is a
semi-plausible distractor — a candidate reasoning from general ML ensembling instinct might defend blending
metrics to dilute verbosity bias, but the chapter's own atomic-metrics doctrine (never blend) rules it out
for a careful reader. **Verdict: SOUND**, with E flagged as a distractor that rewards close reading over
surface pattern-matching (good design, not a defect).

**Item 6** (80k nightly requests, 11k shared prefix, not latency-sensitive; cheapest config). See the
False-precision audit and Attacks-landed BLOCKER above: under the chapter's own stated discount-stacking
rules and its own stated batch cache hit-rate range (30–98%), answer A (cache-on) is only cheaper above a
~53% hit rate. The stem never asserts a hit rate, and 30% is within the chapter's own documented range.
**Verdict: DEFECTIVE.** Tighten by stating an expected/typical hit-rate assumption for a fully-shared single
prefix in the stem, or restructure the options so the answer doesn't hinge on an unstated hit rate. This item
also doubly teaches the wrong reflex (see below): "cost concern + shared prefix ⇒ always cache," without the
hit-rate caveat that the chapter itself supplies elsewhere.

**Item 7** (alert vs dashboard vs weekly). B is clearly the best fit (deterministic, minutes-actionable,
matches the stated canary rollback discipline). **Verdict: SOUND.**

**Item 8** (judge score 5.9→7.6; first action). C is defensible under the chapter's own doctrine
("implausible jump is a bug until proven otherwise"), but the stem gives no sample size, so a candidate could
reasonably ask why the "check noise first" reflex taught in item 3 (for a binary pass rate) doesn't apply
here first, before the more expensive hand-check. The two items teach different first moves for superficially
similar "did quality really improve" questions, and the chapter never states the rule that would let a
candidate generalize correctly (continuous judge scores don't have the same clean CI formula as a binary
pass rate, and the far larger relative jump raises gaming risk that dominates sampling-noise concern at this
effect size). **Verdict: UNDER-DETERMINED.** Tighten by adding one clause explaining why hand-checking
precedes noise-checking specifically for judge-graded continuous scores at large jumps.

**Item 9** (token-accounting facts; select two). B, C correct; A, D, E each false for reasons that don't
depend on the exact tokenizer percentage (any material shift makes E false). **Verdict: SOUND** — tests a
durable structural fact, not a volatile number, despite citing one.

**Item 10** (retrieval win rolls out; best sequence). B is the best general-purpose answer. It implicitly
assumes sufficient traffic exists to reach a powered A/B — the same missing branch flagged under low-traffic
deployments above. Under the stated (unconstrained) stem, **Verdict: SOUND**, but flagged as depending on the
same unstated traffic assumption as the missing-alternatives finding.

**Summary: 1 item DEFECTIVE (6), 1 item UNDER-DETERMINED (8), 8 items SOUND.**

---

## Missing alternatives

| Comparison/scenario | Omitted credible option | Why it matters |
|---|---|---|
| §3.5 cost/quality lever table | Raising `effort` on the current/cheaper model as an explicit alternative to a model upgrade | VERIFIED-FACTS names this as the docs' own selection method ("default → raise effort → only then change model"); Domain 4 currently only documents the cost-cutting direction of the effort lever |
| §3.5 cost lever table | Reducing retrieval `top-k` as a pre-model-downshift cost/latency lever | Appears only in a latency scenario (S6), not connected to the S3 cost-cut decision or the ranked lever table, despite being a cheap, reversible lever that should sit ahead of model downshift |
| §3.3 dataset taxonomy | Synthetic (model-generated, human-spot-checked) case generation for scaling adversarial/edge-case coverage | Practice item 4 rejects "add 400 synthetic cases" for a specific, narrow reason (doesn't fix this round's comparison resolution) but the chapter never states when synthetic generation *is* appropriate (expanding attack-class coverage from a few hand-verified seeds) — risk of over-generalizing to "synthetic data is always bad" |
| §3.4 canary/A-B | For safety-critical/irreversible-harm changes: internal dogfood, expert sign-off, or a much longer, cohort-based (not percentage-based) rollout in place of a standard canary | See BLOCKER above; the chapter has no branch for when live user exposure is itself unacceptable |
| §3.4/§3.7 A-B testing | Explicit alternative decision framework for traffic too low to ever reach a powered A/B (non-inferiority on available traffic, cohort/named-account ramps, shadow+expert review as terminal validation) | The exam's own target industries (financial services, healthcare, gov, enterprise) are disproportionately likely to be traffic-constrained |
| §3.1 judge validation | Bootstrapping path for zero-label, week-one projects (code-based-only gate; judge as advisory, not gating, until calibration accumulates) | See MAJOR finding above |
| §5 optimization objective | Task budgets (advisory per-loop token budget) | Named in VERIFIED-FACTS as a related surface worth covering; absent from the draft |

---

## Heuristic boundary conditions

| Heuristic (as stated) | Missing qualifier |
|---|---|
| "Confident-but-wrong after a data/index change ⇒ retrieval, not the model" | Only holds when the stem's stated invariants (model version, latency unchanged) are independently verified, not merely asserted; a same-day permission/ACL or chunking change produces the identical signature with a different fix |
| "A judge is trusted only after calibration against human labels" | Needs a bootstrap exception for teams with no labels yet: judge scores stay advisory until a calibration set exists, rather than blocking all judge-graded gating |
| "Cost-reduction changes are non-inferiority tests with a pre-registered band" | Needs an exception for safety-critical changes, where even a passing non-inferiority band on a live experiment is the wrong instrument — the change should clear offline/adversarial/expert review before any live exposure |
| "Free wins before tradeoffs: caching → ... → effort → model last" | Needs its own stated exception restated at the heuristic level (not just in §3.5 prose): "once an eval exists, walk model × effort earlier — an eval is what lets you detect the cheaper cell" |
| "A/B when the decision hinges on user outcomes and the traffic exists" | Needs the explicit converse: when traffic does not exist (a very likely condition for this exam's audience), name the substitute framework instead of leaving it as "otherwise you will read noise" with no next step |
| Canary ramp 1%→5%→20%→50%→100%, 24–48h/stage | Needs a minimum-daily-traffic qualifier; at low DAU, 1% is a handful of named accounts, not a statistical sample, and 24–48h may not accumulate any signal at all for infrequently-used enterprise tools |
| "Gate every change on an eval" (implicit throughout) | Needs the explicit release valve the chapter's own noise-floor material supports: a change too small for the eval's resolution to see should be handled by code review/reasoning, not forced through a statistical gate that cannot discriminate at the available n |

---

## Must preserve

1. **The differential-diagnosis discipline itself** — "trigger-to-cause matching" (heuristic 2), the
   distractor-archetype table, and the consistent "what did *not* change" reasoning that mirrors the exam
   guide's own Sample 3 rationale verbatim. This is the chapter's structural core and is well-executed; the
   findings above are about incompleteness within individual rows, not a flaw in the diagnostic framework
   itself. Do not let editing collapse the triage table's columns for space — the "discriminating evidence"
   column is exactly what separates this from generic "symptom → cause" tables in weaker prep material.

2. **The harness/conflation discipline** (§2.5): errors-sidecar separation, `stop_reason` tracking, "no
   answer is not negative answer," oracle/null testing, and the infra-noise magnitude data (≈6pp swing from
   resource configuration alone). This is sophisticated, correctly sourced, non-obvious content that most
   competing prep material omits entirely (confirmed in the dossier's prep-material landscape survey — no
   third-party source addresses this depth). It is foundational to trusting every other diagnostic in the
   chapter and should be cut last, not first, if space runs short.

3. **The explicit reconciliation of the two judge-agreement numbers** (>80% subjective-pairwise research
   ceiling vs. ~90% clear-cut-cases operational gate) and the volume-vs-rigor tension (docs say "prioritize
   volume," the audit checklist demands label provenance and spot-checks). Both are **correct but
   suspicious-looking** — an editor under word pressure may "simplify" two seemingly-conflicting numbers into
   one, or drop the reconciling sentence that explains they measure different populations. That reconciling
   sentence is itself a good exam discriminator (a distractor built on citing the wrong number for the wrong
   population) and must survive editing intact. Likewise: the per-model cache-read discounts (0.1× / 0.025×
   / 0.05×) look asymmetric enough to be mistaken for a typo — they are correctly sourced from VERIFIED-FACTS
   and must not be "cleaned up" into a single uniform rate. The CORE-Bench 42%-score grading-bug anecdote
   also looks like filler but is a sourced, memorable, correct illustration of benchmark brittleness — keep it.

---

## Sources

No new external sources introduced. All findings above are derived by (a) cross-referencing claims already
present in the draft/dossier against each other (the §3.6/§5 effort-cache inconsistency; the §3.6 batch
hit-rate range against item 6's answer key), and (b) direct arithmetic from figures already cited in the
draft/dossier and VERIFIED-FACTS (cache-write/read multipliers, batch discount stacking, the noise-floor
formula). Where a figure's precise stacking mechanics were inferred rather than independently verified
(the batch+cache multiplicative-stacking assumption behind the ~53% crossover in item 6), this is flagged
inline as a question for the validator; the qualitative conclusion (a low enough hit rate flips the answer)
holds under any reasonable interpretation of "discounts stack," since cache writes (1.25–2×) always cost more
than the base rate while only reads provide savings.
