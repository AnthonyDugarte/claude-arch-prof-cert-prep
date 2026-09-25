# Domain 4 — Evaluation, Testing & Optimization

**Weight: 16% of scored items (~10 of 63).** The second-heaviest domain, and the one the exam guide chose to
illustrate with a published sample item [D04-S01].

**Objectives measured** [D04-S01]: (1) define evaluation metrics (accuracy, latency, cost, safety, security);
(2) design evaluation datasets and test frameworks using mixed methodologies; (3) conduct A/B testing and
iterative improvements; (4) diagnose system issues (prompt failure, hallucinations, model mismatch); (5) optimize
token usage, latency, and cost-performance trade-offs; (6) monitor system performance using logging and
observability tools.

---

## 1. What this domain actually tests

Domain 4 puts you in front of a misbehaving system, or a change someone wants to ship, and asks what you measure,
probe, or gate **first**. The published sample shows the mechanics [D04-S01]: a RAG system returns confident but
incorrect answers after a document refresh, "while latency and model version are unchanged," and the answer is that
retrieval is feeding the model poor context. That clause is not scenery — it exists to kill distractors. These are
differential-diagnosis stems: the right answer is the only hypothesis consistent with everything stated, including
what did *not* change.

| Distractor archetype | How it looks right | Why it loses |
|---|---|---|
| Plausible-but-untriggered cause | "Model weights changed"; "the context window shrank" | Nothing in the stem could have caused it |
| Fix before diagnosis | "Switch to a larger model"; "lower the temperature" | The stem asked for the first probe, or the fix does not address the symptom |
| Unvalidated proxy | "Track average response length as a quality metric" | Optimizing a proxy with no guardrail is the Goodhart trap |
| Averages over tails | "Monitor mean latency"; "report overall accuracy" | Safety, security and SLO questions live in p95/p99 or worst-case aggregation |
| More data instead of better measurement | "Add 500 more test cases" | Volume multiplies the error of a conflating harness or an uncalibrated judge |
| Offline confidence for an online question | "Re-run the golden set" when the question is user outcomes | Offline evals cannot see drift or user behavior |
| Cost cut with no quality gate | "Downshift the model to save money" | Cost changes are non-inferiority questions |

---

## 2. Core concepts

**2.1 Success criteria that can fail.** A criterion is *Specific, Measurable, Achievable, Relevant* and states a
threshold on a named population [D04-S10]. "Safe outputs" is not a criterion; "less than 0.1% of outputs out of
10,000 trials flagged for toxicity by the content filter" is. Latency and price are two of the eight named criterion
categories — speed and cost are quality criteria, not afterthoughts. *Decision:* whether a release can be gated at
all; a criterion that cannot fail cannot gate, and "most use cases need multidimensional evaluation along several
success criteria" [D04-S10].

**2.2 Primary, guardrail, and component metrics.** The primary metric is the one a change may move; guardrails must
not regress outside noise; component metrics attribute a task result to a stage (retrieval, generation, tool
selection, formatting). *Decision:* what the eval records per case, and therefore what a failing run tells you. On
labeled sets report precision, recall, specificity and false-positive rate separately — "a variant that 'wins' on
accuracy may have quietly traded recall for precision" [D04-S03]. *Misconception:* that component health implies
task health; a case needing retrieval *and* reasoning *and* formatting "shows 0 whenever any one breaks" [D04-S04].
A metric is *actionable* when one named lever moves it: contextual relevancy → top-k and chunk size; contextual
recall → embedding model; contextual precision → reranker; answer relevancy → prompt; faithfulness →
model/prompt/temperature [D04-S28].

**2.3 pass@k vs pass^k.** pass@k "measures the likelihood that an agent gets at least one correct solution in k
attempts"; pass^k "measures the probability that all k trials succeed"; identical at k=1, and "by k=10, they tell
opposite stories" [D04-S19]. *Decision:* which reliability number goes in the SLA — pass@k when a checker or human
filters candidates, pass^k for unattended customer-facing behavior. *Misconception:* that one run is a measurement;
"a single rep is a point estimate with no error bar" [D04-S04].

**2.4 Noise floor, headroom, minimum detectable effect.** For a binary pass rate the 95% CI half-width is roughly
`1/sqrt(n·reps)`: 25 cases × 2 reps ≈ ±14 points, 50 × 2 ≈ ±10, 100 × 2 ≈ ±7 [D04-S04, D04-S05]. *Decision:*
whether the eval can see the win, computed before spending — put noise floor, headroom (ceiling − baseline) and the
smallest shippable improvement side by side; reps are the cheaper knob. *Misconception:* that a saturated eval is a
good one; above ~95% baseline the remaining variance is "dominated by format quirks, grader tie-breaking, or mild
reward-hacking rather than capability" [D04-S04].

**2.5 Conflation — the harness bug that invalidates everything.** Conflation is any non-model artifact (API error,
timeout, truncation, broken tool, grader crash) landing in the same column as a genuine model result [D04-S04].
Infrastructure is measurably large: resource configuration alone moved one agentic coding benchmark's pass rate
about **6 percentage points** (p<0.01), harness infrastructure errors ranged from 5.8% under strict enforcement to
0.5% uncapped, and "pass rates fluctuate with time of day" [D04-S20]. *Decision:* the runner's schema — failed
attempts with no scorable output go to an error sidecar with a failure class; `stop_reason` and a truncated status
are recorded; refusals are their own metric, since a refusal is not a capability failure and a harness kill is
neither [D04-S03, D04-S05]. "'No answer' is not 'negative answer'" [D04-S04]. *Misconception:* that a zero is a
zero — a `$0.00` cost or `0.0s` latency "is almost never a real measurement" [D04-S03].

**2.6 Latency decomposition.** *Baseline latency* is model processing time for prompt plus response; *TTFT* is time
to the first token from send, "particularly relevant when you're using streaming" [D04-S12]. *TPOT* =
(E2EL − TTFT)/(output tokens − 1); *ITL* is the gap between consecutive tokens; *E2EL* = TTFT + generation time;
*goodput* = requests per second completing **within** SLO [D04-S27]. *Decision:* which lever — TTFT up with E2EL
flat implicates prefill, queueing or a cold cache; E2EL up with TTFT flat implicates output length or generation
speed. *Misconception:* that p50 is the user experience; p95/p99 catch queueing, cold starts and interference that
averages hide, which is why canary rollback rules are written against p99 [D04-S27, D04-S29].

**2.7 Token accounting and the cost model.** Cost is measured **per completed task, not per token** [D04-S07]. Total
prompt size = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`; `input_tokens` alone is the
uncached remainder [D04-S08]. Verified rates (2026-09-24): cache write 1.25× base input at the 5-minute TTL, 2× at
the 1-hour TTL; cache read 0.1× base input (0.025× on Fable 5.1/Mythos 5.1, 0.05× on Opus 5.5); Batch API 50% off
input and output, discounts stack [D04-S16, D04-S17]. `count_tokens` is free with its own RPM limits, returns an
estimate, and rejects server tools, the MCP connector and `url`/`file` sources [D04-S15]. *Decision:* whether a
savings claim is real — estimate from a measured pilot's `usage`, never from intuition ("token guesses are routinely
off by 3-10×" [D04-S03]) or a third-party tokenizer, which undercounts Claude tokens by ~15–20% on prose and more on
code [D04-S09]. *Misconception:* that token counts survive a migration; the newer tokenizer "produces approximately
30% more tokens for the same text" [D04-S15].

**2.8 Safety and security are measured on adversarial sets.** The measurable quantities are refusal correctness
(both directions), jailbreak resistance, PII/secret leakage rate, indirect-injection resistance and
tool-authorization violations. They are rare by construction, so an average over representative traffic cannot see
them: they need built attack sets — "red-team your own agent … test your workflow with documents, emails, and tool
outputs that deliberately contain injection attempts" [D04-S14] — and worst-case aggregation, because "for rare
high-stakes behaviours (data deletion, irreversible actions), fail-on-any or worst-case reflects what matters better
than a mean diluted by easy cases" [D04-S04]. *Misconception:* that a high refusal rate is safety; one-sided sets
produce one-sided optimization, so "refuses when it should" needs the matching "does *not* refuse when it shouldn't".

---

## 3. Trade-off analyses

### 3.1 Grading method: deterministic vs judge vs human

| Axis | Code-based | LLM-as-judge | Human |
|---|---|---|---|
| Marginal cost | ~0 | one model call per case (count judge tokens in cost) | high |
| Throughput | every commit | every PR to nightly | days |
| Reproducibility | deterministic | non-deterministic; measure grader variance | annotator variance |
| Bias exposure | none (brittleness instead) | position, verbosity, self-preference, label deference | anchoring, fatigue |
| Ceiling | constrained output spaces only | nuance, open-ended quality | anything |

**Choose code-based when** the output space is constrained — closed-set label, valid JSON, numeric answer, tests
passing, end state on disk. It is "by far the best grading method if you can design an eval that allows for it", and
"often all that lies between you and an automatable eval is clever design" [D04-S23]. **Choose a judge when** many
phrasings are valid but the property stays checkable in words (grounded in context, no fabricated parameters, cites
a source). **Choose human when** no rubric can express the criterion, when calibrating a judge, and for arbitration
on a stratified sample — accepting that it "limits how often the eval can run" [D04-S03]. **Combine in cost order**
— deterministic gate → judge → human sample — because grading is "a cost you will incur every time you re-run your
eval, in perpetuity" [D04-S23].

### 3.2 Judge shape: pointwise rubric vs pairwise vs reference-match

| Axis | Pointwise rubric | Pairwise blind | Reference-match (exact/cosine/ROUGE-L) |
|---|---|---|---|
| Yields | absolute per-case score | win rate vs a fixed baseline | similarity to a gold string |
| Fuzzy criteria | weaker | stronger — "judges are better at 'which of these two is better' than at placing a single output on an absolute scale" [D04-S03] | poor; rewards phrasing |
| Bias profile | verbosity, self-preference | + position bias | none, but brittle |
| Blind spot | scale drift over time | cross-case mode collapse is structurally invisible [D04-S03] | penalizes valid paraphrase |

**Choose pairwise when** the question is comparative (migration, v1 vs v2), and freeze the baseline's outputs once
— "never regenerate the reference, or 'win rate' silently changes meaning between rounds" [D04-S03]. **Choose
pointwise when** no baseline exists or an absolute per-case number is needed. **Choose reference-match when** the
answer really is one string — cosine similarity for consistency, ROUGE-L for summarization [D04-S11]. **Never**
derive gold from a model under comparison: in a migration, gold from the incumbent "makes the incumbent look best by
construction" [D04-S04].

**Validate before trusting.** Compare the judge against a few dozen independently human-labeled cases: "well below
~90% on clear-cut cases means the judge prompt needs another iteration before its scores can steer changes"
[D04-S04]. Research anchor: strong judges reach "over 80% agreement" with human preference, "the same level of
agreement between humans", on subjective pairwise tasks [D04-S24] — a different population from the ~90% gate, so
neither number is "the" threshold. Test known negatives too: empty string, "I don't know", and a confident answer to
the wrong question must all fail [D04-S03]. Mitigations map one-to-one onto the biases — randomize order (position),
instruct against length and track it separately (verbosity), cross-family judge (self-preference), hide the
reference label (deference), atomic per-property scores (conflation) [D04-S03, D04-S04, D04-S25, D04-S26].

### 3.3 Dataset design: golden vs regression vs adversarial vs production-sampled

| Axis | Golden/acceptance | Regression suite | Adversarial/red-team | Production-sampled |
|---|---|---|---|---|
| Built from | representative tasks + known hard cases | every past incident | attack classes, edge cases | stratified live traffic |
| Size | "20-50 simple tasks drawn from real failures is a great start" [D04-S19]; 15–100 for a first eval [D04-S03] | grows monotonically | small, broad in attack type | large enough to stratify |
| Aggregation | mean / pass^k | fail-on-any per case | fail-on-any | segment means |
| Runs on | pre-merge, pre-release | every commit | pre-release + schedule | weekly review, drift watch |
| Main risk | unrepresentative distribution; stale labels | saturation | never updated with new attack classes | PII and retention limits |

**Start with the tiny hand-built set when** the system is new: early effect sizes are large, so 20–50 cases drawn
from real failures beat a quarter spent building hundreds [D04-S19]. **Grow toward volume when** decisions get
fine-grained — the trigger is the §2.4 arithmetic. Volume beats polish for *questions* ("more questions with
slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals"
[D04-S11, D04-S23]) while label provenance, oracle/null tests and grader spot-checks stay non-negotiable [D04-S04].
**Stratify when** segments differ materially. Include the named edge cases: irrelevant or nonexistent input,
overlong input, harmful or irrelevant user input, and "ambiguous test cases where even humans would find it hard to
reach an assessment consensus" [D04-S11]. **Leakage:** the expected answer must not be reachable from the prompt,
few-shot block, tool description, a file the agent can read, or the open web [D04-S04, D04-S05]. Benchmark hazards
are real — contamination, "simple formatting changes … can lead to a ~5% change in accuracy", mislabeled items
[D04-S21] — and one model "initially scored 42%" until researchers found "rigid grading that penalized '96.12' when
expecting '96.124991…'" [D04-S19].

### 3.4 Offline eval vs shadow vs canary vs A/B test

| Axis | Offline eval | Shadow | Canary | A/B test |
|---|---|---|---|---|
| Question | "Did we break a known behavior?" | "Is the candidate obviously broken on real traffic?" | "Does it survive real serving at small blast radius?" | "Are users better off?" |
| User exposure | none | none | small slice | half |
| Latency to signal | minutes | hours | 24–48 h per stage [D04-S29] | days–weeks [D04-S19] |
| Confidence | high on covered cases only | distributional, no user outcomes | operational | causal on user outcomes |
| Marginal cost | eval spend | ~doubles inference spend while running [D04-S29] | negligible | negligible |
| Blind to | drift, novel inputs, user behavior | user reaction, session effects | small effects | anything below its MDE |

**Gate with the offline regression suite when** the change is bounded and a known behavior could break — a CI gate,
not an experiment. **Shadow when** the change is large (model upgrade, prompt restructuring) and a distributional
comparison on real inputs is worth roughly double inference spend [D04-S29]. **Canary when** serving behavior
itself is the risk: ramp 1% → 5% → 20% → 50% → 100% with at least 24–48 hours per stage, session-sticky
assignment, and automated rollback thresholds such as p99 latency +40% or refusal rate +5% [D04-S29]. **A/B when**
the decision hinges on user outcomes and the traffic exists; otherwise you will read noise.

### 3.5 Cost/latency/quality levers, ranked by measured yield

| Lever | Type | Measured effect | Skip when |
|---|---|---|---|
| Prompt caching | free win | agent-loop cost cut **2.5–3.7×** at 81–90% hit rates; one triage agent's bill fell **83%** [D04-S07] | the prefix differs per request from the first tokens [D04-S08] |
| Input hygiene / progressive disclosure | free win | programmatic tool calling: **−24% input tokens** with a higher score [D04-S07] | most calls read most of the document anyway |
| Prompt audit across model generations | free win | unaudited cross-generation prompts cost **+36% per ticket** at no accuracy gain; audited, **14% cheaper** and 97% vs 92% accurate [D04-S07] | the prompt surface is small and recently audited |
| Output-length control | free win | shorter replies, and "output tokens are the latency lever too" [D04-S06] — brevity is a real quality trade, so report the median length change | answers already terse |
| Batch API | free win | **50%** off input and output; stacks with caching [D04-S17, D04-S18] | a user is waiting |
| Compaction / pruning | free win (long loops) | compaction cut a long run's bill a further **38%** [D04-S07] | loops are short |
| Effort reduction | tradeoff | knowledge work: `low` gives up **1–3 points** for a third to a half off; coding: ~2 points at `medium` for half the cost, ~8 points at `low` for a quarter [D04-S07] | the eval has no headroom |
| Re-run failures at higher effort | tradeoff | ~**93%** pass at ~$0.70/task vs 91.7% at $1.39 running everything at default [D04-S07] | no cheap failure signal exists |
| Model downshift | tradeoff | price the tail: on one run "two problems carried 43% of the spend" [D04-S07] | no eval gates it |

**Sequence.** Free wins first, tradeoffs last, "because each one changes what the model can do, and overshooting
costs quality that the free wins never touch" [D04-S07]. Exception: once an eval exists, walk model × effort early —
only an eval detects the case where "a stronger model at lower effort is the cheaper cell" [D04-S06]. Two levers that
look like savings and are not: `max_tokens` (a 16,384 cap ended 15% of one model's attempts and a third of
another's, **none solved**, so cost per solved task did not improve) and context editing, which "cost more than it
saved" in the measured run [D04-S07]. Quality first: "trying to reduce latency prematurely might prevent you from
discovering what top performance looks like" [D04-S12].

### 3.6 Caching and batch break-even

| Question | Answer |
|---|---|
| When does caching pay off? | On the **first** read at the 5-minute TTL (1.25× write + 0.1× read = 1.35× vs 2× uncached); on the **second** read at the 1-hour TTL (2× + 0.2× = 2.2× vs 3×) [D04-S17, D04-S08] |
| Which TTL? | By **start-to-start** gap between requests sharing the prefix (generation time counts against it): <5 min → 5-minute; 5–60 min → 1-hour; >1 h → scheduled re-warm or accept the miss [D04-S08] |
| Why is caching not working? | The minimum cacheable prefix is model-dependent (512–4096 tokens) and fails **silently**, or a silent invalidator sits in the prefix — timestamp, UUID, unsorted JSON, per-user tool list [D04-S08] |
| Batch economics | 50% off both directions; most batches finish under 1 hour; results at completion or 24 h, whichever first; batches **expire** at 24 h and expired requests are not billed; 100,000 requests or 256 MB per batch; in-batch cache hits are best-effort (observed 30–98%), so prefer the 1-hour TTL [D04-S18] |

They stack, which makes the batch tier the natural home for the eval suite itself.

### 3.7 Regression gate vs experiment, and non-inferiority

| Axis | Regression gate (offline) | Experiment (A/B) |
|---|---|---|
| Question | "Did this break something we already need?" | "Is this better for users?" |
| Unit | test case | session or user, with the flag locked for the session [D04-S29] |
| Statistics | paired difference at fixed n × reps | power analysis; "plan for tens of thousands of sessions per arm" for a 5% MDE at 80% power / 95% confidence [D04-S29] |
| Main failure | false confidence when the suite is misaligned with real usage [D04-S19] | underpowered reads; "LLM output adds variance an order of magnitude larger" than product A/B math assumes [D04-S30] |
| Corrections | re-grade every variant after any grader change [D04-S05] | multiple comparisons (Bonferroni/BH) or sequential/Bayesian methods [D04-S30] |

**Cost-reduction changes are non-inferiority questions.** Register three gates before running: a quality band the
held-out score must stay inside, a cost margin it must beat at a stated pricing basis, and the **mechanism** you
predicted. "A cost tie with the right mechanism and a cost win with the wrong mechanism are both rejections"
[D04-S06]. Move one lever per round; never keep or revert on a one-case swing; the published bar for a production
cutover is around fifty cases and at least five trials per configuration [D04-S06, D04-S07]. Validate a caching diff
on a **warm** cache or "the 1.25× writes dominate and the free win reads as a regression" [D04-S07]. Overfitting
signature: train up, test flat ⇒ revert; and because sequential selections each made on the data that chose them
overstate the combined win, the pre-registered confirm run is the headline [D04-S05, D04-S06].

### 3.8 Monitoring surface: dashboard vs alert vs weekly review

| Surface | Signals | Why here |
|---|---|---|
| Dashboard | TTFT/E2EL p50/p95/p99, error rate, refusal rate, cost per request, cache-read share, tool-call counts | continuous, fast-moving, used during triage |
| Alert | SLO/error-budget burn, p99 breach, refusal-rate step change, cost-per-request step change, injection-screen hits, served-model mismatch | deterministic threshold, minutes-actionable, bounded blast radius [D04-S29] |
| Weekly review | judge-graded quality on a production sample, input-distribution drift, new failure taxonomy, judge recalibration, saturated regression cases | noisy per request; needs judgment; changes the test suite, not the runtime |

**The gap this closes:** latency and cost dashboards cannot see a quality regression — nothing in TTFT, error rate
or spend moves when a prompt edit makes answers subtly less grounded, so a judge-graded sample of real traffic
belongs on the weekly review even when every chart is green [D04-S19, D04-S04]. SLOs for a nondeterministic system
are written over **rates measured on samples** (pass^k on the golden set, ≤ Y% ungrounded sampled answers, p95 E2EL
≤ Z ms), with goodput as the serving-side objective [D04-S27]. Instrument per request: `model` read from the
**response**, all four token classes, `stop_reason`, latency, tool-call and retry counts, refusal flag, and
`judge_model`/`judge_usage` — without the last, up to half the real cost of a model-graded eval is invisible
[D04-S03]. And every production failure needs "a path back into the offline test set, or the same failure will
resurface after the next model update" [D04-S31].

---

## 4. Worked scenarios

**S1 — Financial services, RAG over policy documents.** After a nightly refresh the advisor assistant answers
confidently and wrongly; latency and model version unchanged; regulated advice, audit trail required.
*Recommended:* log the retrieved chunk IDs and text for a failing query and check whether the answer is supported — a
broken re-index or mismatched embeddings is the only cause consistent with all the facts [D04-S01]. *Alternatives
lose because* a refresh cannot change weights, temperature does not fabricate facts from good context, and the prompt
did not change. *What would change it:* if the query answers correctly with the right passage pasted in manually,
retrieval is confirmed; if it still fails, grounding instructions are implicated [D04-S13].

**S2 — Healthcare, clinical-summary quality.** A prompt change moves judge-graded quality 6.1 → 7.4 overnight.
*Recommended:* treat it as suspicious before treating it as good news — hand-check the flipped cases and verify
judge-vs-human agreement on independently labeled cases before the number steers anything [D04-S04, D04-S05].
*Alternatives lose because* shipping on the jump risks a change that games the grader, and more cases do not fix an
uncalibrated judge. *What would change it:* a deterministic check for the property that matters (PHI absent, every
claim traceable to the transcript) converts opinion into a gate [D04-S11].

**S3 — Retail, 40% cost cut on a support agent.** Incumbent is a frontier model at default effort. *Recommended:*
free wins first — verify cache health in `usage` [D04-S08], audit the prompt for dated action-triggering instructions
("verify twice" cost +48% per case, "be maximally thorough" +39% [D04-S06]), then sweep effort before touching the
model under a pre-registered non-inferiority band [D04-S07]. *Alternatives lose because* a model downshift first is
the riskiest change and forfeits the free wins, and trimming `max_tokens` buys truncation, not savings. *What would
change it:* if input is unique per request, caching's ceiling is small and the effort/model axis moves up.

**S4 — Government, document-processing agent with tools.** Security review wants evidence of injection resistance.
*Recommended:* build an adversarial set where tool results and uploaded documents carry embedded instructions,
aggregate **fail-on-any**, measure both directions of refusal, and confirm untrusted content arrives only inside
`tool_result` blocks with a screening classifier gating tool output [D04-S04, D04-S14]. *Alternatives lose because*
an average over representative traffic cannot see a rare attack class, and a high refusal rate is not evidence of
correctness. *What would change it:* a new attack class in the wild adds cases — the set is a living suite.

**S5 — Insurance, claims agent with eight tools.** Task success is 71% and nobody can say why. *Recommended:*
decompose into component metrics (tool-selection accuracy, recall@k and context precision, faithfulness, format
validity) and grade the **end state**, not the transcript, because agents "regularly find valid approaches that eval
designers didn't anticipate" [D04-S19]. *Alternatives lose because* asserting an exact tool-call sequence fails
correct behavior, and a blended score shows 0 whenever any stage breaks [D04-S04]. *What would change it:* if one
capability per case is impossible, report per-stage metrics beside the task metric.

**S6 — Telecom, chat assistant SLO.** p95 end-to-end latency regressed 40%; p50 barely moved. *Recommended:*
decompose TTFT vs E2EL, add per-tool timing, and keep client retries out of the model-latency column [D04-S04,
D04-S27]; then apply ordered levers — cache the stable prefix (also a TTFT win), cap retrieval top-k, shorten the
output contract, stream to recover perceived responsiveness [D04-S08, D04-S12]. *Alternatives lose because*
switching to the fastest model without an eval gate trades unmeasured quality, and the mean hides the tail the SLO is
written against.

---

## 5. Failure modes and diagnostics (triage table)

| Symptom | Most likely cause | First probe | Discriminating evidence | Fix |
|---|---|---|---|---|
| Confident-but-wrong after a data refresh; latency and model unchanged | Retrieval/indexing: stale, partial, or mismatched-embedding index | Log retrieved chunks for a failing query | Retrieved context lacks the answer or holds the superseded version | Re-index; verify embedding parity; add a groundedness check |
| Confident-but-wrong right after a prompt edit, no data change | Prompt failure: grounding or "I don't know" permission removed | Diff the rendered prompt; re-run the golden set on the prior prompt | Golden set recovers on the old prompt with identical retrieval | Restore quote-grounding and uncertainty permission [D04-S13] |
| Answers correct, output unparseable | Truncation, or no enforced output contract | Read `stop_reason` | `max_tokens` ⇒ truncation, not a format bug | Raise `max_tokens`, stream, enforce structured outputs [D04-S07] |
| One case fails every round regardless of change | Grader bug or stale ground truth | Read the output, the judge's reasoning and the expected value | Re-grading shrank a claimed +9-point win to +3 in a measured case | Fix the grader, then re-grade every variant in place [D04-S05, D04-S06] |
| Quality drop after a model swap | Prompt debt across generations before capability | Golden set on both models, then a prompt audit | Audited prompt recovers the score and is cheaper | Re-author the prompt for the target model [D04-S07] |
| Cost per request jumped, "nothing changed" | Silent cache invalidator: timestamp/UUID in prefix, tool-list change, effort or thinking change, model switch, workspace split | Read `usage` | `cache_read_input_tokens` ≈ 0 while `cache_creation_input_tokens` ≈ whole conversation | Move volatile content after the last breakpoint; deterministic serialization [D04-S08] |
| p95/p99 up, p50 flat | Tail: queueing, cold cache, retries counted as latency, one slow tool | Decompose TTFT vs E2EL; per-tool timings; attempt counts | TTFT up ⇒ prefill/queue/cold cache; E2EL up alone ⇒ output length | Cache and pre-warm, cap top-k, shorten outputs, stream [D04-S27, D04-S12] |
| Eval score swings with no code change | Harness/infra noise or too few reps | No-change control at the same rep count; read the errors sidecar | Control sits inside the same band ⇒ variance, not regression | Add reps; give the harness resource headroom; run at multiple times of day [D04-S20] |
| Agent follows instructions found in a document | Indirect prompt injection | Check where untrusted content entered the request | Untrusted text in `system` or a plain user block rather than `tool_result` | Move it to `tool_result`, JSON-encode it, screen tool output, narrow tool scope [D04-S14] |

---

## 6. Anti-patterns

- **The vibes gate** — shipping on "the outputs look better" with no fixed input set; the reviewer is a genuine
  expert, yet nothing is comparable across changes and nothing catches the unconsidered regression.
- **Judge-as-oracle** — trusting a grader never compared against human labels; the rubric reads sensibly while
  agreement is unmeasured and the judge stays gameable [D04-S04].
- **Grading the path** — asserting an exact tool-call sequence; looks like rigor, fails valid alternatives [D04-S19].
- **Scoring the plumbing** — letting timeouts and truncations land as model failures. Looks conservative;
  contaminates the headline and penalizes whichever arm hit more transient errors [D04-S04].
- **Hand-picking the worst cases as the tuning slice** — tunes for the tail and buys regression to the mean, whose
  signature is a healthy train gain with a flat held-out set [D04-S04, D04-S05].
- **Gold from the incumbent** — looks pragmatic; makes the incumbent win by construction [D04-S04].
- **`max_tokens` as a cost knob** — looks like a hard budget; truncates mid-thought and buys proportionally fewer
  solved tasks [D04-S07].
- **Cache markers without verification** — the costliest caching failure is silent: requests keep succeeding, the
  bill is just higher [D04-S08].

---

## 7. Exam-day heuristics

1. Confident-but-wrong after a data or index change ⇒ **retrieval**, not the model [D04-S01].
2. Match cause to trigger; "weights changed silently" and "the context window shrank" are almost never correct, and
   streaming improves perceived latency only [D04-S12].
3. "First place to investigate" ≠ "fix" — prefer the cheapest probe that discriminates between hypotheses.
4. Average-case metrics cannot measure rare harms; use adversarial sets and p95/p99 or fail-on-any [D04-S04].
5. A judge is trusted only after calibration against human labels, and never when it is the model under test
   [D04-S03, D04-S04].
6. Cost-reduction changes are non-inferiority tests with a pre-registered band [D04-S06].
7. Free wins before tradeoffs: caching → input hygiene → loop hygiene → output → batch → effort → model last
   [D04-S07].
8. "Is caching working?" resolves in `usage`, never in code review; and if the output space is constrained the
   grader is code, not a judge [D04-S08, D04-S23].
9. If the eval cannot resolve the effect, add reps or cases before rounds — noise floor ≈ `1/sqrt(n·reps)`
    [D04-S04].
10. Randomize at the session, not the request, and lock the assignment for the session [D04-S29].
11. An implausible judge-graded jump is a measurement bug until a human check says otherwise [D04-S05].
12. When a case fails every round, suspect the grader before the prompt — re-grading has shrunk a claimed +9-point
    win to +3 [D04-S06].
---

## 8. Practice items

**1.** A support assistant's p95 end-to-end latency rose 45%; p50 and TTFT are unchanged. Best first action?
*(Select one.)* **A.** Switch to the fastest model. **B.** Reduce `max_tokens`. **C.** Measure per-tool timing and
output-token counts on slow requests. **D.** Enable streaming.
→ **C.** Flat TTFT with a raised tail points after the first token — output length or a slow tool [D04-S27]. A trades
unmeasured quality and explains no tail-only regression; B truncates rather than shortens [D04-S07]; D changes only
perceived latency [D04-S12].

**2.** Deciding whether a cheaper model can replace the incumbent on a summarization path — which two practices most
protect the comparison? *(Select two.)* **A.** Generate reference summaries with the incumbent. **B.** Assert the
served `model` from each response. **C.** Frame it as a non-inferiority test with a pre-registered quality band.
**D.** Raise temperature for diversity. **E.** Report the mean of the two best runs.
→ **B, C.** Silent substitution invalidates a comparison [D04-S04]; cost reduction is a non-inferiority question
[D04-S06]. A makes the incumbent win by construction; D adds variance; E selects the favorable end of a spread.

**3.** An eval of 25 cases at 2 reps shows pass rate rising 64% → 71%. What do you say first? *(Select one.)* **A.**
Ship it. **B.** The result is inside the eval's noise floor; add reps or cases. **C.** Swap in a stronger judge.
**D.** Add 400 synthetic cases.
→ **B.** At 25 × 2 the CI half-width is roughly ±14 points [D04-S04]. A ships noise; C changes the instrument so old
and new scores stop being comparable; D adds low-fidelity volume without fixing this comparison's resolution.

**4.** After an index rebuild a legal assistant cites superseded clauses confidently; model, prompt and latency
unchanged. Which evidence best confirms the cause? *(Select one.)* **A.** Lowering temperature removes the errors.
**B.** Retrieved chunks for a failing query lack the correct clause. **C.** `stop_reason` is `max_tokens`. **D.**
Tokens per request increased.
→ **B.** Inspecting retrieved context directly tests the hypothesis the trigger implies [D04-S01]. A does not follow
from a rebuild and cannot fix bad context; C indicates truncation; D is a cost signal.

**5.** Which two choices most reduce judge bias in a pairwise eval? *(Select two.)* **A.** Randomize which candidate
is A on every case. **B.** Tell the judge which output is the human reference. **C.** Use the model under test as its
own judge. **D.** Instruct against rewarding length and log output length separately. **E.** Average the judge score
with cosine similarity.
→ **A, D.** Position bias is handled by randomizing order, verbosity bias by instructing against length and tracking
it [D04-S04, D04-S24]. B invites label deference; C invites self-preference [D04-S25]; E blends an unrelated signal
into a metric that should stay atomic.

**6.** A nightly classification job of 80,000 requests shares an 11,000-token prefix and is not latency-sensitive.
Cheapest configuration? *(Select one.)* **A.** Batch API with caching at the 1-hour TTL. **B.** Synchronous with the
5-minute TTL. **C.** Batch API with caching off to avoid write premiums. **D.** Synchronous with `max_tokens` cut.
→ **A.** Batch is 50% off both directions and stacks with caching; batch requests run concurrently over up to 24
hours, so the 1-hour TTL is the documented choice for shared context [D04-S17, D04-S18]. B forfeits 50%; C forfeits
reads at 0.1× base input; D truncates and ignores the dominant input cost.

**7.** Which signal belongs on an **alert** rather than a dashboard or weekly review? *(Select one.)* **A.**
Judge-graded groundedness on 200 sampled answers. **B.** Refusal rate stepping 2% → 9% within an hour. **C.**
Input-embedding drift over the quarter. **D.** Count of saturated regression cases.
→ **B.** A deterministic, minutes-actionable threshold and a standard canary rollback trigger [D04-S29]. A and C need
human judgment and change the test suite; D is suite hygiene.

**8.** A prompt change raises judge-graded quality 5.9 → 7.6. First action? *(Select one.)* **A.** Ship and monitor.
**B.** Re-run at higher reps. **C.** Hand-check the cases that flipped. **D.** Lower the judge's temperature.
→ **C.** An implausible jump under a model grader is suspicious before it is good news, and reading the flipped cases
is the cheapest disconfirming test [D04-S05]. A ships an unexplained gain; B tightens an interval around a possibly
gamed metric; D reduces grader variance, not gameability.

**9.** Which two statements about token accounting are correct? *(Select two.)* **A.** `input_tokens` is the total
prompt size. **B.** Total prompt size is `input_tokens` + cache creation + cache read tokens. **C.** `count_tokens`
is free, separately rate-limited, and returns an estimate. **D.** A general third-party tokenizer is adequate for
Claude cost estimates. **E.** Token counts transfer unchanged across Claude generations.
→ **B, C** [D04-S08, D04-S15]. A is the uncached remainder only; D undercounts Claude tokens materially [D04-S09];
E is false — the newer tokenizer produces roughly 30% more tokens for identical text [D04-S15].

**10.** A retrieval change wins the offline eval. Best sequence to a decision? *(Select one.)* **A.** Roll out to 100%
and watch dashboards. **B.** Shadow on mirrored traffic, canary at 1% with session-sticky assignment and automated
rollback, then a powered A/B on the business metric. **C.** Re-run the offline eval with more cases, then roll out to
100%. **D.** A/B at 50/50 immediately.
→ **B.** Each stage answers a different question — obviously broken, survives real serving, better for users — and
only this order bounds blast radius while still reaching a causal read [D04-S19, D04-S29]. A has no blast-radius
control; C cannot see drift or user behavior; D skips the operational check and exposes half of traffic to an
unvalidated serving path.

---

## 9. Objective coverage

| Objective | Covered in |
|---|---|
| Define evaluation metrics (accuracy, latency, cost, safety, security) | §2.1–2.3, §2.6–2.8, §3.1, §5, items 1, 9 |
| Design evaluation datasets and test frameworks using mixed methodologies | §2.4–2.5, §3.1–3.3, S2, S4, S5, items 3, 5 |
| Conduct A/B testing and iterative improvements | §3.4, §3.7, S3, items 2, 10 |
| Diagnose system issues (prompt failure, hallucinations, model mismatch) | §1, §2.5, §5 triage table, S1, S5, items 4, 8 |
| Optimize token usage, latency, and cost-performance trade-offs | §2.6–2.7, §3.5–3.6, S3, S6, items 1, 6, 9 |
| Monitor system performance using logging and observability tools | §2.5, §3.8, §5, items 7, 10 |

---

## 10. Sources

Full detail, access dates and trust ratings: `research/04-evaluation-testing-optimization-sources.md`.

Primary (Anthropic): **D04-S01** exam guide · **D04-S02** bundled `claude-api` skill · **D04-S03** build-eval ·
**D04-S04** eval-audit · **D04-S05** eval-hillclimb · **D04-S06** cost-hillclimb · **D04-S07** cost-optimization ·
**D04-S08** prompt-caching · **D04-S09** token-counting guide · **D04-S10** define-success · **D04-S11**
develop-tests · **D04-S12** reduce-latency · **D04-S13** reduce-hallucinations · **D04-S14** mitigate-jailbreaks ·
**D04-S15** token-counting docs · **D04-S16** models overview · **D04-S17** pricing · **D04-S18** batch processing ·
**D04-S19** demystifying evals · **D04-S20** infrastructure noise · **D04-S21** challenges in evaluating AI systems ·
**D04-S22** Managed Agents observability · **D04-S23** cookbook `building_evals.ipynb`. Secondary/academic:
**D04-S24** Zheng et al. · **D04-S25** self-preference bias · **D04-S27** inference-metrics handbook · **D04-S28**
RAG metric mapping · **D04-S29** shadow/canary/A-B patterns. Low trust, corroborated before use: **D04-S26**,
**D04-S30**, **D04-S31**, **D04-S32**.

`[UNVERIFIED]` in this session: novelty effects specific to LLM A/B tests (general experimentation caution, no
primary source found); the existence and capabilities of a Claude Console evaluation or prompt-comparison tool (no
live page retrieved — this chapter makes no claim about it). **Volatile:** prices, cache multipliers and model names
are as published 2026-09-24, when the live models page listed Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5 and
Claude Haiku 4.5 as current and Claude Opus 5 as legacy [D04-S16, D04-S17].
