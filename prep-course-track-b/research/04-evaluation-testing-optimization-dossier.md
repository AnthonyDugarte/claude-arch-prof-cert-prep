# Research dossier — Domain 4: Evaluation, Testing & Optimization (16%)

Researcher pass, 2026-09-24. Exam guide v1.0, effective July 2026, code CCAR-P [D04-S01].
Weight 16% of 63 scored items ⇒ **~10 items** (16% × 63 = 10.08).

Every source ID resolves in `04-evaluation-testing-optimization-sources.md`. Claims not verified against a
primary Anthropic source in this session are marked `[UNVERIFIED]`.

---

## 0. How this domain is actually tested

The guide's own Sample 3 is a Domain 4 item and defines the shape [D04-S01]:

> "A RAG system suddenly returns confident but incorrect answers after a document refresh, while latency and
> model version are unchanged. What is the most likely first place to investigate?" → **B. The retrieval/indexing
> step is returning irrelevant or stale chunks.** Rationale: "The other options would not be triggered
> specifically by a document refresh."

Three structural lessons for authoring and for candidates:

1. The stem carries **negative evidence** ("latency and model version are unchanged") whose only function is to
   eliminate distractors. Domain 4 items are differential-diagnosis items: the answer is the hypothesis that
   explains *all* the stated facts, including the ones that did not change.
2. The stem asks for the **first place to investigate**, not the fix. Items reward probe ordering.
3. Distractors are mechanistically wrong, not merely worse ("model weights silently changed", "context window
   shrank") — i.e. they describe events that the stated trigger cannot cause.

---

## 1. Objective 1 — Define evaluation metrics (accuracy, latency, cost, safety, security)

### 1.1 Verified official framing

Anthropic's success-criteria guidance requires criteria that are **Specific, Measurable, Achievable, Relevant**
and names eight criterion categories: task fidelity, consistency, relevance and coherence, tone and style,
privacy preservation, context utilization, **latency**, **price** [D04-S10]. Verbatim contrasts worth teaching:

- Bad: "The model should classify sentiments well." Good: "an F1 score of at least 0.85 … on a held-out test set
  of 10,000 diverse Twitter posts … which is a 5% improvement over the current baseline" [D04-S10, D04-S11].
- Hazy → measurable: "Safe outputs" → "Less than 0.1% of outputs out of 10,000 trials flagged for toxicity by
  the content filter" [D04-S10]. This is the canonical pattern for making a *safety* criterion gradeable.
- "Most use cases need multidimensional evaluation along several success criteria," with the worked example
  pairing F1 ≥ 0.85, 99.5% non-toxic, 90% of errors benign, and 95% of responses under 200 ms [D04-S10].

### 1.2 Metric layers (architect-level synthesis)

| Layer | Examples | What it answers | Failure if used alone |
|---|---|---|---|
| Task/outcome | task success, resolution rate, pass^k | "Did the user get what they came for?" | Cannot localize the broken component |
| Component | recall@k, nDCG, tool-selection accuracy, faithfulness, format validity | "Which stage is broken?" | Can all look healthy while the task still fails |
| Operational | TTFT, E2EL p95/p99, cost per completed task, error/refusal rate, cache-read share | "Can we afford and serve it?" | Blind to quality regressions |
| Safety/security | refusal correctness (both directions), jailbreak resistance, PII leakage rate, injection resistance | "What is the tail risk?" | Averages hide it; needs adversarial sets |

Anthropic's own layering of metric families: for labeled sets, "don't collapse grading to a single pass-rate" —
report precision, recall, specificity and false-positive rate as separate metrics, because "a variant that 'wins'
on accuracy may have quietly traded recall for precision" [D04-S03, D04-S04].

**Actionability test** (synthesis from D04-S03/S04/S28): a metric is actionable when a single named lever moves
it. Confident-AI's mapping is the cleanest published example: contextual relevancy → top-k and chunk size;
contextual recall → embedding model; contextual precision → reranker; answer relevancy → prompt template;
faithfulness → model/prompt/temperature [D04-S28].

### 1.3 Reliability metrics unique to nondeterministic systems

From [D04-S19], verbatim: **pass@k** "measures the likelihood that an agent gets at least one correct solution in
k attempts"; **pass^k** "measures the probability that all k trials succeed." "At k=1, they're identical … By
k=10, they tell opposite stories: pass@k approaches 100% while pass^k falls to 0%." Architectural read: pass@k is
the right metric when a human or a checker filters candidates (draft generation, code with tests); pass^k is the
right metric for unattended customer-facing behavior, where "users expect reliable behavior every time."

### 1.4 Safety and security measurement

- Refusal correctness is two-sided. An eval for "does the agent refuse when it should" also needs "does it *not*
  refuse when it shouldn't"; otherwise always-refuse scores perfectly and "one-sided evals produce one-sided
  optimisation" [D04-S04].
- Refusals are a **graded outcome, not an error**, and must be recorded as their own metric so "refusal-zeros and
  capability-zeros aren't summed" [D04-S03, D04-S04].
- Injection resistance requires adversarial construction: "Red-team your own agent. Before deploying, test your
  workflow with documents, emails, and tool outputs that deliberately contain injection attempts" [D04-S14].
- Aggregation must match the stakes: "for rare high-stakes behaviours (data deletion, irreversible actions),
  fail-on-any or worst-case reflects what matters better than a mean diluted by easy cases" [D04-S04].
- Red-teaming is not yet a standardized measurement discipline: "Red teaming AI systems is presently more art
  than science" [D04-S21].

### 1.5 Latency metric definitions (verified)

- **Baseline latency**: "the time taken by the model to process the prompt and generate the response, without
  considering the input and output tokens per second" [D04-S12].
- **TTFT**: "the time it takes for the model to generate the first token of the response, from when the prompt
  was sent … particularly relevant when you're using streaming" [D04-S12].
- **TPOT** = (E2EL − TTFT) / (output tokens − 1); **ITL** is the exact pause between two consecutive tokens;
  **E2EL** = TTFT + generation time; **goodput** = requests/second that complete *within* SLO [D04-S27].
- Percentiles: p50 is the typical experience, p95/p99 are near-worst-case and catch queueing, cold starts and
  batch interference that averages hide [D04-S27].
- Metric-by-workload: interactive chat → TTFT then ITL; streaming → ITL and E2EL; batch/offline → tokens/s and
  cost; latency-constrained services → goodput [D04-S27].
- Published comparative latency ordering for the current lineup: Haiku 4.5 "Fastest", Sonnet 5 "Fast", Opus 5.5
  "Moderate", Fable 5.1 "Slower" — and "actual latency depends on prompt length, output length, and thinking
  effort" [D04-S16].

### 1.6 Cost metric definition

Cost is measured **per completed task, not per token**: "A model with a higher sticker price can be the cheaper
option if it finishes the job in fewer turns, and a cheaper model that fails still bills its tokens, then the
retry, then whatever the failure costs downstream" [D04-S07]. Cost must be *derived* from each row's recorded
`model` × `usage` (four token classes) plus the judge's own `judge_model` × `judge_usage`, never from a flat
assumed rate — "otherwise up to half the real cost is invisible" on model-graded evals [D04-S03].

---

## 2. Objective 2 — Design evaluation datasets and test frameworks using mixed methodologies

### 2.1 Eval anatomy (verified)

Four parts: "An input prompt that is fed to the model", "An output that comes from running the input prompt
through the model", "A 'golden answer' to which we compare the model output", "A score, generated by one of the
grading methods" [D04-S23]. Operationally an eval is "a set of input examples, a way to run the app against each
input, and a way to grade each output" [D04-S03].

### 2.2 Grading ladder — raw comparison matrix

| Method | Cost/case | Throughput | Determinism | Bias exposure | Best for | Verified notes |
|---|---|---|---|---|---|---|
| Code-based / programmatic | ~0 | CI-speed | Deterministic | None | Constrained output space: label from a closed set, JSON schema, exact/numeric answer, tests pass, end-state check | "By far the best grading method if you can design an eval that allows for it, as it is super fast and highly reliable" [D04-S23]. For agents, read the **end state**, not the transcript [D04-S03, D04-S04] |
| Pairwise blind comparison (judge) | 1 judge call | High | Non-deterministic | Position, verbosity | Comparative questions (migration, v1 vs v2); fuzzy criteria | "Judges are better at 'which of these two is better' than at placing a single output on an absolute scale"; randomize A/B per case, allow `tie`/`both_bad`, freeze the reference outputs once [D04-S03] |
| Pointwise rubric (judge) | 1 judge call | High | Non-deterministic | Verbosity, self-preference | No baseline exists; absolute per-case score wanted | Write the rubric as "concrete, checkable claims" not "rate helpfulness 1-5"; use structured outputs for a deterministic parse [D04-S03] |
| Reference-based similarity (cosine, ROUGE-L) | ~0 | CI-speed | Deterministic | Rewards phrasing | Consistency and summarization checks | Docs give cosine similarity for consistency and ROUGE-L for summarization [D04-S11] |
| Human review | high | very low | Human-variance | Annotator effects | Criteria no rubric can express; judge calibration; final arbitration | "The most capable grading method as it *can* be used on almost any task" but "incredibly slow and expensive"; "avoid designing evals that require human grading if you can help it" [D04-S23] |

Mixed-methodology default (synthesis of D04-S03, S19, S23): cheap deterministic gate on every commit → judge on
the dimensions code cannot see → human review on a small stratified sample and on every judge recalibration.
Grading is "a cost you will incur every time you re-run your eval, in perpetuity" [D04-S23], which is why the gate
order is cost-ascending.

### 2.3 Judge discipline (the highest-yield exam content)

| Bias | Mechanism | Mitigation | Source |
|---|---|---|---|
| Position | Verdict flips when candidates are reordered | Randomize A/B per case, or score both orders and average | D04-S04, D04-S24, D04-S26 |
| Verbosity | Longer answers preferred without added content | Instruct against rewarding length; add a length penalty; track output length as its own column | D04-S04, D04-S26 |
| Self-preference / self-enhancement | Judge prefers text resembling its own | Never use the exact model under test as its own judge; prefer a different family; use a jury for close calls | D04-S03, D04-S04, D04-S24, D04-S25 |
| Label deference | Judge favors whichever output is labeled "reference"/"human" | Don't tell the judge which is which | D04-S04 |
| Criterion conflation | One blended score hides per-property movement | Atomic per-property metrics, ideally a separate judge call per property | D04-S04, D04-S26 |
| Prompt injection into the judge | Candidate text instructs the judge | Judge system prompt treats both candidates as untrusted data | D04-S03 |

**Validation bar before a judge is trusted**: "Validate the judge on a few dozen cases a human labelled
independently and report agreement. Well below ~90% on clear-cut cases means the judge prompt needs another
iteration before its scores can steer changes" [D04-S04]. Independent academic anchor: strong LLM judges reach
"over 80% agreement" with human preference — "the same level of agreement between humans" [D04-S24]. Note the two
numbers measure different things (human-preference agreement on open-ended pairwise judgments vs. agreement on
clear-cut labelled cases); the ~90% figure is the operational gate, the >80% figure is the research ceiling on
subjective pairwise tasks. Also test the judge on known negatives: an empty string, "I don't know", and a
confident answer to the wrong question must all fail [D04-S03, D04-S04].

### 2.4 Dataset taxonomy — raw comparison matrix

| Set | Provenance | Size guidance | Refresh cadence | Runs when | Primary risk |
|---|---|---|---|---|---|
| Golden / acceptance set | Hand-built + production-sampled, human-verified labels | "20-50 simple tasks drawn from real failures is a great start" [D04-S19]; 15–100 inputs for a first eval [D04-S03] | Grows as new failure modes appear | Pre-merge and pre-release | Stale labels; unrepresentative distribution |
| Regression suite | Every production incident becomes a case | Monotonically grows | Append-only | Every commit / CI | Saturation — near the ceiling it measures format quirks, not capability [D04-S04] |
| Adversarial / red-team set | Deliberately constructed attacks and edge cases | Small but broad in attack classes | After each new attack class | Pre-release and on schedule | Average-case aggregation hides tail failures; needs fail-on-any [D04-S04, D04-S14] |
| Production-sampled set | Stratified sample of live traffic | Large enough to stratify by segment | Continuous, re-drawn per period | Drift watch, weekly review | PII/retention constraints; label cost [D04-S03] |
| Train (analyzer-visible) vs test (held-out) slices | Random split stratified by primary tag | Test slice sized to the noise floor | Fixed once | Every iteration round | Splitting by baseline score guarantees regression-to-mean artifacts [D04-S04, D04-S05] |

Edge cases the docs explicitly want in the set: "Irrelevant or nonexistent input data; Overly long input data or
user input; [Chat use cases] Poor, harmful, or irrelevant user input; Ambiguous test cases where even humans
would find it hard to reach an assessment consensus" [D04-S11].

**Volume-vs-quality rule, verified twice**: "Prioritize volume over quality: More questions with slightly lower
signal automated grading is better than fewer questions with high-quality human hand-graded evals" [D04-S11];
"your preference should be for higher volume and lower quality of questions over very low volume with high
quality" [D04-S23]. This is *not* a licence for sloppy labels — the same body of guidance requires label
provenance, oracle/null testing and grader spot-checks [D04-S04].

### 2.5 Label provenance and leakage (high-yield)

- Record whether gold is human-written, human-verified, or a model's output and which model. "Never use model A's
  outputs as gold when the question is A vs B" — in a migration, gold derived from the incumbent "makes the
  incumbent look best by construction" [D04-S04].
- Leakage checks: expected answer or near-paraphrase visible in prompt, few-shot block, system message, tool
  description, or any file the agent can read; "answerable from memory" for named real entities when the intent
  was to test retrieval; ground truth reachable through the open web for public benchmarks [D04-S04, D04-S05].
- Benchmark hazards: contamination because widely used sets appear in training data; "Simple formatting changes
  to the evaluation … can lead to a ~5% change in accuracy"; benchmark items that are "mislabeled or
  unanswerable" [D04-S21]. CORE-Bench example: Opus 4.5 "initially scored 42%" until researchers found "rigid
  grading that penalized '96.12' when expecting '96.124991…'" [D04-S19].

### 2.6 Harness hygiene — the conflation rule

"The central failure mode is **conflation**: any time a non-model artifact — an infra error, a truncated response,
a broken tool, a retry delay — lands in the same column as a genuine model result, the eval attributes to the
model something that belongs to the plumbing" [D04-S04]. Required separations:

- Failed attempts with no scorable output go to an `errors.jsonl` sidecar with a failure class, never into the
  scored rows [D04-S03, D04-S04].
- `stop_reason` recorded; `status: truncated` when `max_tokens` was hit; truncated rows counted but not averaged
  in as wrong [D04-S03].
- "'No answer' is not 'negative answer'" — a model asserting "no vulnerabilities found" must not share a label
  with an empty/crashed/unparseable output [D04-S04].
- Assert the **served** model from the response, not the config; a silent provider fallback "invalidates the
  comparison" [D04-S03, D04-S04, D04-S06].
- Oracle/null test before the first paid pass: push the reference answers through (expect ~100%) and a null
  baseline through (expect ~0%). "Two runs, minutes, and it catches most wiring bugs before they cost a full
  pass" [D04-S04].
- Environment noise is measurable and large: infrastructure configuration alone moved Terminal-Bench 2.0 pass
  rate ~6 percentage points (p<0.01), with infra error rate 5.8% under strict resource enforcement vs 0.5%
  uncapped and 2.1% at ~3× headroom; on SWE-bench the effect was 1.54 pp at 5× RAM; "pass rates fluctuate with
  time of day" [D04-S20].

### 2.7 Detectability arithmetic

For a binary pass-rate, the 95% CI half-width is roughly `1/sqrt(n·reps)`: 25 cases × 2 reps ≈ **±14 points**;
50 × 2 ≈ **±10**; 100 × 2 ≈ **±7** [D04-S04, D04-S05]. Before round 1, put three numbers side by side: noise
floor, headroom (ceiling − baseline), and the smallest improvement the owner would ship on. "If the noise floor
exceeds either, say so plainly now" and offer more reps (cheapest), more cases, a continuous instead of binary
metric, or trimming to discriminating cases with a full-set confirm at the end [D04-S04].

---

## 3. Objective 3 — Conduct A/B testing and iterative improvements

### 3.1 The evaluation-layer stack (verified, with what each cannot do)

From [D04-S19], with its Swiss-cheese framing — "no single evaluation layer catches every issue. With multiple
methods combined, failures that slip through one layer are caught by another":

| Layer | Strengths (verbatim) | Weaknesses (verbatim/paraphrase) | Latency to signal | Confidence |
|---|---|---|---|---|
| Automated evals | "Faster iteration, Fully reproducible, No user impact, Can run on every commit" | upfront investment, maintenance, "can create false confidence if misaligned with real usage" | minutes | high on covered cases only |
| Production monitoring | "Reveals real user behavior at scale, Catches issues that synthetic evals miss" | reactive — problems reach users first; noisy; needs instrumentation | hours–days | descriptive, not causal |
| A/B testing | "Measures actual user outcomes (retention, task completion), Controls for confounds, Scalable" | "Slow; days or weeks to reach significance and requires sufficient traffic" | days–weeks | causal |
| User feedback + transcript review | surfaces unanticipated problems; builds failure intuition | "Sparse, self-selected, time-intensive, doesn't scale" | continuous | anecdotal |
| Systematic human studies | "Gold-standard quality judgments, handle subjective tasks" | "Expensive, slow turnaround, difficult to run frequently" | weeks | highest per-case |

Shadow and canary are the two stages the Anthropic post does not name; practitioner sources fill them:
shadow mirrors traffic to a candidate and never returns its output to users, recording "outputs, latency, cost,
errors, and eval scores for comparison" and roughly doubling inference spend while it runs [D04-S29, D04-S31];
canary ramps 1% → 5% → 20% → 50% → 100% with a 24–48 h minimum per stage, session-sticky assignment, monitoring
"latency percentiles (p50, p95, p99) — not averages", cost/request, error and refusal rates, output-length
distribution, and implicit user signals, with automated rollback thresholds such as p99 +40% or refusal +5%
[D04-S29].

### 3.2 A/B discipline for probabilistic outputs

| Concern | What goes wrong | Discipline | Source |
|---|---|---|---|
| Unit of randomization | Per-request assignment splits one conversation across arms | Assign at session/user level and lock the flag for the session | D04-S29 |
| Variance | "LLM output adds variance an order of magnitude larger"; temperature 0 does not make it deterministic | Larger samples than product A/B math suggests; "plan for tens of thousands of sessions per arm" for a 5% MDE at 80% power / 95% confidence | D04-S29, D04-S30 |
| Multiple comparisons | Many variants/slices manufacture significance | Bonferroni / Benjamini-Hochberg, or sequential (alpha-spending) / Bayesian hierarchical methods | D04-S30 |
| Novelty / time effects | Early enthusiasm or time-of-day load skews the read | Run full cycles; note that measured pass rates fluctuate with time of day | D04-S20, D04-S29 `[UNVERIFIED]` for novelty specifically |
| Heterogeneity | Model wins on one request type and loses on another | "Pre-stratify analysis by request type before aggregation" | D04-S29 |
| Cost-reduction changes | A superiority test cannot answer "is quality unharmed?" | Frame as **non-inferiority** with a pre-registered margin; use non-inferiority tests for guardrail metrics | D04-S30, D04-S06 |
| Selection-on-the-data | Three sequential selections each made on the data that chose them overstate the combined win | Pre-registered confirm run is the headline, not per-round selection scores | D04-S06 |

### 3.3 Pre-registered adoption gates (the cleanest published decision rule)

A candidate change is adopted only if **all three** pass [D04-S06]:
1. **Quality band** — held-out score within a named band of the incumbent (band stated before running).
2. **Cost margin** — strictly cheaper beyond a registered margin, at a stated pricing basis.
3. **Mechanism** — the predicted mechanism appears in the measurements. "A cost tie with the right mechanism and
   a cost win with the wrong mechanism are both rejections: the first is an edit that didn't bite, the second is
   an unexplained confound that will not survive contact with production."

Additional discipline: one lever per round so effects attribute [D04-S06, D04-S05]; "never keep or revert on a
one-case swing" [D04-S07]; the published bar for a production cutover is "around fifty cases and at least five
trials per configuration" [D04-S07]; a caching diff must be validated on a **warm** cache or "the 1.25× writes
dominate and the free win reads as a regression" [D04-S07]; cells in a model × effort search never share cache
(cache is per-model and effort participates in the cache key — measured: 3/3 effort switches re-billed the full
prefix, 0/9 same-effort continuations did), so walk readings are cache-cold and must be annotated [D04-S06].

### 3.4 Overfitting signature and stall handling

- Train up, test flat ⇒ the change overfit to the cases the analyzer read; revert [D04-S05].
- Train down, test up at low rep counts ⇒ treat as noise; keep only if it repeats [D04-S05].
- Implausible judge-graded jump ⇒ "treat it as suspicious before treating it as good news"; spot-check by hand.
  "An LLM judge being gamed looks exactly like a breakthrough until you check" [D04-S05].
- After 2–3 rounds inside the noise band, stop iterating content and **categorize** remaining failures:
  artifact gap / grader disagreement / harness-infra / structural / variance — each bucket has a different fix
  and only the first is the iteration loop's home turf [D04-S05].

---

## 4. Objective 4 — Diagnose system issues

### 4.1 Diagnostic differential table

| Symptom | Candidate causes (ranked) | First probe | Discriminating evidence | Ruled out by |
|---|---|---|---|---|
| Confident but wrong, began after a document refresh; latency and model unchanged | Retrieval/index: stale or mismatched chunks, embedding-model mismatch, partial re-index | Log retrieved chunk IDs + text for a failing query and check whether the answer is supported | Retrieved context does not contain the answer, or contains the superseded version | Same query with manually pasted correct context answers correctly ⇒ retrieval, not generation [D04-S01] |
| Confident but wrong across all queries, no data change, after a prompt edit | Prompt failure: grounding instruction removed, "I don't know" permission removed | Diff the rendered prompt; re-run golden set on the previous prompt | Golden set recovers on the old prompt with identical retrieval | Retrieval logs identical between arms [D04-S13] |
| Answers correct but format/JSON invalid | Output contract not enforced | Check `stop_reason` and whether structured outputs / `strict` are in use | `stop_reason: max_tokens` ⇒ truncation, not format failure | Valid JSON on shorter outputs ⇒ truncation [D04-S03, D04-S07] |
| Quality fell after a model swap; prompt unchanged | Model mismatch **or** dated prompt carried across generations | Re-run the golden set on both models with the same prompt; then run a prompt audit | Cross-generation prompts cost 36% more per ticket at no accuracy gain in one measured migration; audited, 14% cheaper and 97% vs 92% accurate | If the audited prompt recovers, it was prompt debt, not capability [D04-S07] |
| Cost per request jumped, prompt "unchanged" | Silent cache invalidator (timestamp/UUID/unsorted JSON in prefix, tool-list change, effort/thinking change, model switch, workspace split) | Read `usage`: is `cache_read_input_tokens` ≈ 0 while `cache_creation_input_tokens` ≈ full conversation? | Healthy loop reads the whole prior prefix and writes only the last turn's delta | Payload diff of adjacent requests, or cache diagnostics, names the divergence point [D04-S08] |
| Token count/cost estimate off by ~30% after migration | Tokenizer change across model generations | Re-count the same request with `count_tokens` under both model IDs | 4.7-generation tokenizer produces ~30% more tokens for the same text | Byte-identical prompt, two counts [D04-S15, D04-S17] |
| p95 latency regressed; p50 flat | Tail: queueing, retries counted in latency, cold cache, one slow tool | Decompose into TTFT vs E2EL and per-tool timings; check retry counts | TTFT flat + E2EL up ⇒ longer output or slower generation; TTFT up ⇒ prefill/queue/cold cache | Per-call breakdown for agentic runs separates a slow tool from a slow model [D04-S27, D04-S04] |
| Eval score swings run-to-run with no code change | Harness/infra noise, insufficient reps, stochastic build step | Run a no-change control at the same rep count; read the errors sidecar | Infra config alone moved one benchmark ~6 pp; infra error rate 5.8% → 0.5% across resource settings | Control run inside the noise band ⇒ variance, not regression [D04-S20, D04-S05] |
| Agent stops mid-task / claims success with nothing changed | `max_tokens` truncation; no-op behavior; tool error swallowed | Check `stop_reason`, then the end state of the workspace | A 16,384-token cap ended 15% of one model's attempts, none solved | End-state check plus a no-op detector [D04-S07, D04-S03] |
| Agent leaks data or follows instructions from a document | Indirect prompt injection | Replay the exact tool output through an injection screen; check whether untrusted content arrived as `tool_result` | Untrusted content delivered in `system` or plain user text rather than `tool_result` | Adversarial set with embedded instructions [D04-S14] |
| One eval case fails every round regardless of change | Grader bug or stale ground truth, not model capability | Read the output, the judge's reasoning and the expected value | Re-grading has shrunk a claimed +9-point win to +3 in a measured case | "When a case fails every round, suspect the grader before grinding prompt content at it" [D04-S06, D04-S05] |

### 4.2 Diagnostic heuristics worth teaching as rules

- **Trigger-to-cause matching**: the cause must be something the stated trigger could have caused. A document
  refresh cannot change model weights or the context window [D04-S01].
- **Confidence is not a quality signal**: fluent, confident, wrong is the signature of *bad context*, not of a
  weak model — the model is faithfully summarizing what it was given.
- **Separate "did the mechanism engage" from "did it help"**: track tool-call/retrieval/memory engagement as its
  own column. "A score that moved while the engagement rate didn't is probably noise or a harness artifact"
  [D04-S05].
- **Don't trust a zero**: `$0.00` cost, `0.0s` latency, empty `usage`, or a flat constant across cases "is almost
  never a real measurement — it's a field-name mismatch, a silent lookup failure, or a default that papered over
  an exception" [D04-S03].

---

## 5. Objective 5 — Optimize token usage, latency, and cost-performance trade-offs

### 5.1 Verified economics

| Fact | Value | Source |
|---|---|---|
| Cache write, 5-minute TTL | 1.25× base input | D04-S17 |
| Cache write, 1-hour TTL | 2× base input | D04-S17 |
| Cache read | 0.1× base input; 0.025× on Fable 5.1 / Mythos 5.1; 0.05× on Opus 5.5 | D04-S16, D04-S17 |
| Cache break-even | Pays off after **one** read at 5-minute TTL (1.25 + 0.1 = 1.35 vs 2.0 uncached); after **two** reads at 1-hour TTL (2.0 + 0.2 = 2.2 vs 3.0) | D04-S08, D04-S17 |
| Minimum cacheable prefix | Model-dependent, 512–4096 tokens; non-monotonic across generations; shorter prefixes fail silently (`cache_creation_input_tokens: 0`) | D04-S08 |
| Batch discount | 50% on input and output; stacks with caching discounts | D04-S17, D04-S18 |
| Batch limits | 100,000 requests or 256 MB per batch; most complete in under 1 hour; results at completion or 24 h, whichever first; batches expire at 24 h and expired requests are not billed | D04-S18 |
| Batch caching | Cache hits are best-effort because requests run concurrently; observed hit rates 30–98%; use the 1-hour TTL for batches | D04-S18 |
| Token counting | Free, separate RPM limits (5,000 / 10,000 / 20,000 by tier), an estimate, rejects server tools + MCP + `url`/`file` sources | D04-S15 |
| Tokenizer shift | 4.7-generation tokenizer produces ~30% more tokens for the same text | D04-S15, D04-S17 |
| Measured caching yield | Agent-loop cost cut 2.5–3.7× at 81–90% hit rates; one triage agent's bill fell 83% from caching alone | D04-S07 |
| Measured effort yield (research/knowledge) | `low` gave up 1–3 points for a third to a half off cost per task; `medium` matched default accuracy at 70–85% of cost | D04-S07 |
| Measured effort yield (long-horizon coding) | ~2 points given up at `medium` for half the cost; ~8 points at `low` for a quarter | D04-S07 |
| Re-run-failures pattern | ~93% pass at ~$0.70/task (all at `low`, failures re-run at default) vs 91.7% at $1.39 running everything at default | D04-S07 |
| `max_tokens` as a cost knob | A 16,384 cap ended 15% of one model's attempts and a third of another's, **none solved** — cost per solved task did not improve | D04-S07 |
| Context editing | "Every clearing pass rewrites the cached conversation… in the run measured for the platform docs, context editing cost more than it saved" | D04-S07 |
| Compaction | Cut a long triage run's bill a further 38% where it fired | D04-S07 |
| Programmatic tool calling | 24% fewer input tokens on agentic search benchmarks, with a higher score | D04-S07 |
| Action-triggering prompt text | "Verify twice" +48% per-case cost; "be maximally thorough" +39%; one extra tool round ≈ +1/3 of per-case cost, while inert prompt text is nearly free **when cached** | D04-S06 |
| Web search / data residency | Web search $10 per 1,000 searches; `inference_geo: "us"` applies a 1.1× multiplier on all token categories | D04-S17 |

### 5.2 Lever sequencing (free wins before tradeoffs)

Order from [D04-S07]: (1) prompt caching — "the largest single lever on every model and benchmark Anthropic
measured", and it stays on permanently; (2) input-token hygiene / progressive disclosure, including a prompt
audit; (3) agent-loop hygiene (prune, compaction, subagents); (4) output-token hygiene; (5) batch; *then* the
tradeoffs: (6) effort and task budgets; (7) model selection, last. With an eval in hand the order changes: the
model × effort staircase moves early, because "with an eval you can *detect* that a stronger model at lower
effort is the cheaper cell" [D04-S06].

Perceived vs actual latency: streaming does not reduce E2EL; it "can significantly improve the perceived
responsiveness of your application" by moving the user's wait to TTFT [D04-S12]. Caching reduces TTFT on the
cached prefix and pre-warming with `max_tokens: 0` removes the first-request cold write from the user's path —
worth it only when first-request latency is user-visible, the prefix is large, and there is a moment before
traffic [D04-S08].

Quality-first sequencing is explicit in the docs: "It's always better to first engineer a prompt that works well
without model or prompt constraints, and then try latency reduction strategies afterward. Trying to reduce
latency prematurely might prevent you from discovering what top performance looks like" [D04-S12].

### 5.3 Break-even math patterns to teach

- **Caching**: with a 5-minute TTL, the second request on a shared prefix is already cheaper than not caching.
  Decide TTL from the **start-to-start** gap between requests sharing the prefix (generation time counts against
  the TTL): <5 min → 5-minute TTL; 5–60 min → 1-hour TTL; >1 h → re-warm on a schedule or accept the miss
  [D04-S08].
- **Batch**: 50% off is unconditional on the token side; the cost is a 24-hour expiry window and no mid-batch
  tool loop. Eval runs, backfills and scheduled jobs are the canonical fit [D04-S07, D04-S18].
- **Charge an optimization its own mass**: a standing prompt directive that rides every request must net positive
  against its own token mass at the cache-adjusted price — one measured 650-character directive produced the
  intended behavior change and still only tied on cost [D04-S06].
- **Price the tail, not the median**: "on the typical task every model looks similar and the cheapest looks best,
  but the bill is decided by the tasks the cheap model fails" — on one 20-problem research run, two problems
  carried 43% of the spend [D04-S07].

---

## 6. Objective 6 — Monitor system performance using logging and observability tools

### 6.1 What to instrument (verified fields)

Per request: `model` (from the **response**), the four token classes (`input_tokens`,
`cache_creation_input_tokens`, `cache_read_input_tokens`, `output_tokens`), `stop_reason`, latency, tool-call
count, retry/attempt count, refusal flag, and — for model-graded paths — `judge_model` + `judge_usage`
[D04-S03, D04-S04, D04-S08]. Total prompt size = `input_tokens + cache_creation_input_tokens +
cache_read_input_tokens`; `input_tokens` alone is only the uncached remainder [D04-S08].

Organization-level: the Usage and Cost Admin API splits usage into exactly the quantities the levers act on
(`uncached_input_tokens`, `cache_read_input_tokens`, `cache_creation.ephemeral_5m/1h_input_tokens`,
`output_tokens`) and the cost report segments by `model`, `cost_type`, `token_type`, `service_tier`; data appears
within ~5 minutes; a key shared across projects blends traffic and makes per-project reads unattributable
[D04-S07].

Managed Agents exposes observability as an **event stream** (`session.*`, `span.*` including
`span.model_request_start`/`_end`, `agent.message`, `agent.tool_use`, `agent.thinking`), a persisted filterable
event history, permission-evaluation fields, and webhooks. The observability page documents no first-party
OpenTelemetry exporter; external tracing/metrics are built by consuming the events [D04-S22].

### 6.2 Dashboard vs alert vs weekly review (synthesis)

| Signal | Surface | Why |
|---|---|---|
| TTFT/E2EL p50/p95/p99, error rate, refusal rate, cost/request, cache-read share, throughput | Dashboard | Continuous, fast-moving, needed for triage |
| SLO/error-budget burn, p99 breach, refusal-rate step change, cost-per-request step change, injection-screen hits, served-model mismatch | Alert | Deterministic threshold, actionable in minutes, blast-radius-bounded (see canary rollback thresholds: p99 +40%, refusal +5% [D04-S29]) |
| Judge-graded quality on production samples, drift in input distribution, new failure taxonomy, judge-vs-human recalibration, saturated regression cases | Weekly review | Noisy at request granularity; requires human judgment; changes the test suite rather than the runtime |

Two rules that make the loop close: **every production failure becomes an offline case** or "the same failure
will resurface after the next model update" [D04-S31, corroborated by the living-suite guidance in D04-S04]; and
**latency dashboards cannot see quality regressions** — nothing in TTFT, error rate or cost moves when a prompt
change makes answers subtly less grounded, which is why a judge-graded production sample belongs on the weekly
review even when every operational chart is green [D04-S19, D04-S04].

SLO/error-budget thinking adapts to nondeterminism by writing objectives over **rates measured on samples**, not
per-response guarantees: e.g. "pass^k ≥ X on the golden set", "≤ Y% of sampled production answers ungrounded",
"p95 E2EL ≤ Z ms", with goodput (requests/s completing within SLO) as the serving-side objective [D04-S27,
D04-S19].

### 6.3 Drift

Input drift is the failure that offline suites structurally cannot see: "a model that scored 92% offline three
months ago may be quietly handling a different mix of queries now" [D04-S31]. Detection options: embedding-based
distribution monitoring on inputs [D04-S31, low trust], segment-level task-success monitoring, and periodic
re-drawing of the production-sampled eval set [D04-S03]. Anthropic's layer table assigns drift detection to
production monitoring, not to automated evals [D04-S19].

---

## 7. Contradictions and cautions surfaced (not smoothed)

1. **Model lineup.** `AGENT-BRIEF.md` states the current lineup is "Claude 5 family (Opus 5, Sonnet 5, Fable 5.1)
   and Haiku 4.5". The bundled `claude-api` skill's cached table (cached 2026-06-24) agrees and prices Opus 5 at
   $5/$25 [D04-S02]. The **live docs fetched today** list the current lineup as Claude Fable 5.1, **Claude Opus
   5.5** (`claude-opus-5-5`, $4/$20 input/output, default effort `medium`, cache read 0.05×), Claude Sonnet 5
   ($2/$10) and Claude Haiku 4.5 ($1/$5), with Opus 5 moved to "Legacy models (still available)" [D04-S16,
   D04-S17]. Resolution for the course: the live pricing/models pages win on facts; the chapter should avoid
   depending on a specific model name where possible and cite prices with a date. Flagging for the editor:
   any chapter text that calls Opus 5 "current" is now stale.
2. **Volume vs. rigor.** Docs and cookbook say "prioritize volume over quality" [D04-S11, D04-S23], while the
   eval-audit checklist is emphatic about label correctness, provenance and grader spot-checks [D04-S04]. These
   are reconcilable (volume of *automatable* questions, rigor of *labels and graders*) but the tension is real
   and exam items could lean either way; teach the reconciliation, not one side.
3. **Judge-agreement numbers.** ">80% agreement, the same level of agreement between humans" [D04-S24] vs "well
   below ~90% on clear-cut cases means the judge prompt needs another iteration" [D04-S04]. Different
   populations (subjective pairwise vs clear-cut labelled). Do not present either as "the" threshold.
4. **Context editing.** Marketed as a context-window tool; measured as a cost *increase* in one Anthropic run
   [D04-S07]. Any item implying context editing is a savings lever is answering against measured evidence.
5. **Effort and caching.** The cost-hillclimb guide reports a probe in which 3/3 effort switches re-billed the
   full prefix, and warns that "reports from first-party product surfaces that effort can be switched without
   losing the cache do not transfer to API customers" [D04-S06]. Treat mid-conversation effort changes as cache
   invalidating on the Messages API, with the per-message-effort beta as the documented exception on specific
   models [D04-S08].
6. **Managed Agents observability.** The page documents events/webhooks only; the absence of an OTel exporter is
   an absence of documentation, which I am recording as such rather than as a product limitation [D04-S22].
7. **Console evaluation tool.** I could not fetch a live page documenting a Claude Console "Evaluate" feature at
   `/docs/en/test-and-evaluate/eval-tool` (the fetch resolved to the define-success content) [D04-S10 attempt].
   The existence, capabilities and limits of a Console eval tool are `[UNVERIFIED]` in this session; the chapter
   must not assert them.

---

## 8. Open questions for the validator

1. Does a Console-based evaluation/prompt-comparison tool currently exist, and if so what are its grading
   options and case limits? (Chapter currently makes no claim.)
2. Is `claude-opus-5-5` the correct current default for course-wide examples, and should the whole course be
   re-baselined off Opus 5? (Cross-domain decision; Domain 4 draft avoids naming a default model.)
3. Is there a published Anthropic figure for A/B traffic requirements, or is the "tens of thousands of sessions
   per arm" figure only practitioner-sourced? (Currently attributed to D04-S29, secondary.)
4. Novelty effects in LLM A/B tests: no primary source found; the draft mentions them as a general
   experimentation caution, marked `[UNVERIFIED]`.
5. Whether `pass^k` / `pass@k` terminology appears in any exam-adjacent Anthropic doc beyond the engineering
   blog [D04-S19], which would raise its likelihood of being tested.

---

## Prep-material landscape

Third-party CCAR-P material found on 2026-09-24. The credential is new (effective July 2026), and the material
below shows the expected profile of fast-published, SEO-optimized, partly AI-generated prep content. **Nothing
below was used as a source for any technical claim in the dossier or draft**, and none of it should be copied.

| Source | What it claims | Trust judgment |
|---|---|---|
| Tutorials Dojo — CCAR-P Practice Exams [D04-S33] | Timed/review/section/randomized modes, explanations, references, flashcards | `low` for content, but the publisher has a long track record in cloud certification prep; most likely the highest-quality third-party option. Still written against the same public blueprint we are, with no access to the live bank. |
| claudecertificationguide.com [D04-S34] | "30 lessons and 250+ practice questions, no sign-up required" | `low`. Unaffiliated domain chosen to imply officiality; no named authors; no way to audit item quality. |
| CertSafari [D04-S35] | "456 exam-style practice questions aligned with the latest exam guide" | `low`. Item count is implausibly high for a 63-item exam with a July-2026 blueprint; volume claims like this usually indicate generated items. |
| Preporato [D04-S36] | Timed practice exams + flashcards, "every question explained" | `low`. Also publishes a "complete guide 2026" blog that paraphrases the official guide. |
| DumpsBase [D04-S37] | "114 exam questions with answer explanations", "free dumps" | `low` and an **integrity hazard**. Dump-style vendors trade in purported live-item content; using them risks the NDA and rules-of-conduct violations described in the official guide (invalidation, revocation, ban) [D04-S01 §12–13]. Note this to learners explicitly. |
| Clearcat blog [D04-S38] | Exam guide, topics, practice questions | `low`. Reads as a paraphrase of the official guide with generated items appended. |

Two observations that matter for course positioning:

- No third-party source found addresses Domain 4 at the depth the objectives imply — they enumerate topics
  (evaluation, monitoring) without the trade-off reasoning the guide's own sample items require. The gap this
  course fills is the *discriminators*, not the topic list.
- Several sites reproduce the official blueprint text near-verbatim. That is public material, but it means
  candidate-facing prep is converging on the same surface; anything that differentiates has to come from primary
  docs plus measured engineering evidence, which is what sources D04-S02 through D04-S23 provide.
