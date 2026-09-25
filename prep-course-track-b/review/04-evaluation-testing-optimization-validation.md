# Domain 4 — Evaluation, Testing & Optimization: VALIDATION

Validator pass, 2026-09-24. Independent fact-check of `drafts/04-evaluation-testing-optimization-draft.md`
against primary sources. Every source in the researcher's table that backs a load-bearing claim was opened
and read in surrounding context, not accepted from the table. Source IDs `D04-V01…` resolve at the end.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. §3.5 effort-lever numbers carry neither their baseline nor their model. The measurements were taken on
   Claude Fable 5 (knowledge work) and Claude Opus 5 (coding) against those models' `high` default. Claude
   Opus 5.5 — the docs' current default recommendation — defaults to `medium` [D04-V05]. As written,
   "~2 points at `medium` for half the cost" is unusable-to-wrong on the current lineup, because on Opus 5.5
   `medium` IS the default and the delta is zero by construction. Fix: name the model and the baseline.
2. Two citations do not support the text they carry. §3.7 "multiple comparisons (Bonferroni/BH) or
   sequential/Bayesian methods [D04-S30]" — that page contains none of it [D04-V13]. §2.6 "p95/p99 catch
   queueing, cold starts and interference that averages hide [D04-S27, D04-S29]" — D04-S27 says only that
   median is the typical experience and p99 is the slowest 1%; the mechanism list is not there [D04-V11].
   Both statements are correct content with invented provenance. Strip or re-source the tags.
3. Line 3 is factually wrong twice: Domain 4 at 16% is the **third**-heaviest domain (Integration 19%,
   Solution Design 17%), and the exam guide publishes **three** sample items — one each for Domains 3, 2
   and 4 — so Domain 4 is not "the one the exam guide chose to illustrate" [D04-V01].
```

## What is good and must be preserved

- **`pass@k` / `pass^k` is correct throughout.** Definitions are verbatim from the Anthropic engineering post
  [D04-V04], the k=1/k=10 divergence is stated correctly, and every downstream use (SLA framing in §2.3,
  golden-set aggregation in §3.3, SLO wording in §3.8) uses `pass^k` in the all-must-succeed sense. This was
  the designated BLOCKER risk and the chapter clears it.
- **No `budget_tokens` anywhere.** The string does not appear in the draft. The optimization sections treat
  `effort` as the control. This is the correct current story [D04-V05] and better than most prep material.
- **No Console eval-tool claim.** Verified: neither `define-success` nor `develop-tests` documents such a
  tool [D04-V08, D04-V09], and the draft asserts nothing about one. The `[UNVERIFIED]` note in §10 is honest.
- **Per-model cache-read economics are present.** §2.7 carries 0.1× / 0.025× (Fable 5.1, Mythos 5.1) / 0.05×
  (Opus 5.5), exactly matching live pricing [D04-V03] and `VERIFIED-FACTS.md`.
- **No stale-model text.** The only model names in the body are in the §2.7 cache-rate parenthesis and the
  §10 volatility note, which correctly lists Opus 5 as legacy. The Domain 1 lineup lesson was absorbed.
- **Quotation fidelity is unusually high.** ~45 quoted fragments were checked; all but the two in must-fix 2
  are verbatim or faithful paraphrase of the cited source.
- The triage table (§5), the free-wins-before-tradeoffs sequence (§3.5), and the non-inferiority gate (§3.7)
  are all documented practice, not invention [D04-V06, D04-V07].

---

## Numbers audit

`CONFIRMED` 28 · `CONFIRMED-BUT-UNCONDITIONED` 15 · `CONTRADICTED` 1 · `NOT-FOUND` 2 ·
`AUTHOR-DERIVATION-UNLABELED` 0

| # | Claim as stated | Loc | Value correct? | Baseline stated? | Conditions stated? | Source says it? | Verdict | Correct formulation |
|---|---|---|---|---|---|---|---|---|
| N1 | "16% of scored items (~10 of 63)" | L3 | Yes (0.16×63=10.08) | n/a | Yes | Yes [D04-V01] | CONFIRMED | — |
| N2 | "The second-heaviest domain" | L3 | **No** | n/a | n/a | No — D3=19%, D1=17% | **CONTRADICTED** | "The third-heaviest domain, behind Integration (19%) and Solution Design (17%)." |
| N3 | "the one the exam guide chose to illustrate with a published sample item" | L4 | **No** | n/a | n/a | No — guide publishes 3 samples (D3, D2, D4) | **CONTRADICTED** | "one of the three domains the guide illustrates with a published sample item." |
| N4 | "less than 0.1% of outputs out of 10,000 trials flagged for toxicity by the content filter" | §2.1 | Yes | Yes | Yes | Yes, verbatim [D04-V08] | CONFIRMED | — |
| N5 | "eight named criterion categories … latency and price" | §2.1 | Yes (8: task fidelity, consistency, relevance/coherence, tone/style, privacy preservation, context utilization, latency, price) | n/a | Yes | Yes [D04-V08] | CONFIRMED | — |
| N6 | pass@k = at least one of k; pass^k = all k; identical at k=1, "opposite stories" by k=10 | §2.3 | Yes | Yes | Yes | Yes, verbatim [D04-V04] | CONFIRMED | — |
| N7 | "95% CI half-width is roughly `1/sqrt(n·reps)`: 25×2 ≈ ±14, 50×2 ≈ ±10, 100×2 ≈ ±7" | §2.4, §7 h9 | Yes. Algebra checks: 1/√50=0.1414, 1/√100=0.100, 1/√200=0.0707. Statistically sound: the exact 95% binomial half-width 1.96·√(p(1−p)/N) equals 0.98/√N at p=0.5, so `1/√N` is the worst-case form. | Partly — "of a binary pass rate" is stated; ±14 is in **percentage points of pass rate at 95%** (stated) | **No** — two conditions missing: (a) it is a worst-case approximation at p≈0.5 and tightens sharply near the ceiling; (b) `n·reps` treats reps as independent draws, which reps on the same case are not (D04-S04 itself frames it as a *paired-difference* CI, D04-S05 as a plain pass-rate CI — the sources disagree) | **Yes, verbatim** — `eval-audit.md` §5 and `eval-hillclimb.md` [D04-V06]. **This is NOT an author derivation.** ±10 at 50×2 is in `eval-hillclimb.md` | CONFIRMED-BUT-UNCONDITIONED | "For a binary pass rate the 95% CI half-width is roughly `1/sqrt(n·reps)` — 25 cases × 2 reps ≈ ±14 points, 50 × 2 ≈ ±10, 100 × 2 ≈ ±7 [D04-S04, D04-S05]. It is a worst-case figure (widest at a 50% pass rate, much tighter near the ceiling) and it treats reps as independent observations, which correlated reps on the same case are not — so read it as a floor on resolution, not a precise interval." |
| N8 | "above ~95% baseline the remaining variance is 'dominated by format quirks, grader tie-breaking, or mild reward-hacking rather than capability'" | §2.4 | Yes | Yes | No — the quoted clause attaches to "near the ceiling" in the source; the "~95%+" number comes from a *different* bullet ("the eval cannot discriminate at the top") | Both halves present, adjacent, but fused by the draft [D04-V06] | CONFIRMED-BUT-UNCONDITIONED | Keep the ~95% figure and the quote in separate sentences; do not present the quote as attached to the number. |
| N9 | "resource configuration alone moved one agentic coding benchmark's pass rate about 6 percentage points (p<0.01)" | §2.5, §5 | Yes | **No** — the 6 pp is the gap between the **most- and least-resourced** setups (1× strict enforcement vs uncapped) | No — benchmark unnamed (Terminal-Bench 2.0) and the **counter-example omitted**: on SWE-bench the same sweep moved only **1.54 pp at 5× RAM**, i.e. the effect is benchmark-specific | Yes [D04-V02] | CONFIRMED-BUT-UNCONDITIONED | "On Terminal-Bench 2.0 the gap between the most- and least-resourced harness configurations was about 6 percentage points (p<0.01); on SWE-bench the same variation moved only 1.54 points. Infrastructure noise is real and benchmark-specific — the post's own rule is that leaderboard gaps under 3 points deserve skepticism absent documented infra matching [D04-S20]." |
| N10 | "harness infrastructure errors ranged from 5.8% under strict enforcement to 0.5% uncapped" | §2.5, §5 | Yes | Yes | Yes (adds 2.1% at ~3× headroom in dossier, dropped in draft — acceptable) | Yes [D04-V02] | CONFIRMED | — |
| N11 | "pass rates fluctuate with time of day" | §2.5, §5 | Yes | n/a | No — the post presents this anecdotally, not as a quantified finding | Yes, as an observation [D04-V02] | CONFIRMED-BUT-UNCONDITIONED | Mark as an observation, not a measured effect. |
| N12 | "TPOT = (E2EL − TTFT)/(output tokens − 1)"; "E2EL = TTFT + generation time"; "goodput = requests per second completing within SLO"; ITL = gap between consecutive tokens | §2.6 | Yes, all four | Yes | Yes | Yes [D04-V11] | CONFIRMED | — |
| N13 | "p95/p99 catch queueing, cold starts and interference that averages hide [D04-S27, D04-S29]" | §2.6 | Substance is standard | n/a | n/a | **No.** D04-S27 says only: median "shows the typical user experience", P99 "reveals worst-case performance for the slowest 1%" and "captures tail latency". Queueing / cold starts / batch interference appear nowhere | **NOT-FOUND** | Either drop the mechanism list, or state it as the chapter's own synthesis and cite D04-S27 only for "p50 = typical, p99 = slowest 1%". |
| N14 | "Total prompt size = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`; `input_tokens` alone is the uncached remainder" | §2.7 | Yes | Yes | Yes | Yes, verbatim [D04-V06] | CONFIRMED | — |
| N15 | "cache write 1.25× base input at the 5-minute TTL, 2× at the 1-hour TTL" | §2.7, §3.6 | Yes | Yes | Yes | Yes [D04-V03] | CONFIRMED | — |
| N16 | "cache read 0.1× base input (0.025× on Fable 5.1/Mythos 5.1, 0.05× on Opus 5.5)" | §2.7 | Yes | Yes | Yes | Yes [D04-V03], matches `VERIFIED-FACTS.md` | CONFIRMED | — |
| N17 | "Batch API 50% off input and output, discounts stack" | §2.7, §3.5, §3.6 | Yes | Yes | Yes | Yes [D04-V03, D04-V10] | CONFIRMED | — |
| N18 | "`count_tokens` is free with its own RPM limits, returns an estimate, and rejects server tools, the MCP connector and `url`/`file` sources" | §2.7 | Yes (RPM 5,000/10,000/20,000 by tier) | Yes | Almost — the **advisor tool is the one server tool that is supported** | Yes [D04-V12] | CONFIRMED | Add "(every server tool except the advisor tool)". |
| N19 | "token guesses are routinely off by 3-10×" | §2.7 | Yes | Yes | Yes | Yes, verbatim [D04-V06] | CONFIRMED | — |
| N20 | "a third-party tokenizer, which undercounts Claude tokens by ~15–20% on prose and more on code" | §2.7, item 9 | Yes | Yes | No — the measurement is specifically for **`tiktoken`/`gpt-tokenizer`** (OpenAI tokenizers), not "third-party tokenizers" in general | Yes [D04-V06] | CONFIRMED-BUT-UNCONDITIONED | "`tiktoken` (and `gpt-tokenizer`) undercount Claude tokens by ~15–20% on typical text and by much more on code or non-English input [D04-S09]." |
| N21 | "the newer tokenizer 'produces approximately 30% more tokens for the same text'" | §2.7, item 9 | Yes, direction and magnitude correct | Yes (same text) | **No** — the boundary is unstated. Docs: "Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer … Claude Sonnet 4.6 and earlier models use the previous tokenizer." **Haiku 4.5 is on the old tokenizer**, so the +30% applies to a Haiku 4.5 → Opus 5.5 move but **not** to Opus 5 → Opus 5.5 | Yes, verbatim [D04-V03, D04-V12] | CONFIRMED-BUT-UNCONDITIONED | "Opus 4.7 and later (plus Mythos Preview) use a newer tokenizer that produces roughly 30% more tokens for identical text; Sonnet 4.6 and earlier — including Haiku 4.5 — use the previous one. So the migration hazard is generation-crossing, not universal: re-count with `count_tokens` under the target model ID [D04-S15, D04-S17]." |
| N22 | "well below ~90% on clear-cut cases means the judge prompt needs another iteration before its scores can steer changes" | §3.2 | Yes | Yes (a few dozen independently human-labeled cases) | Yes | Yes, verbatim [D04-V06] | CONFIRMED | — |
| N23 | "strong judges reach 'over 80% agreement' with human preference, 'the same level of agreement between humans', on subjective pairwise tasks" | §3.2 | Yes | Yes | Partly — unstated: the judge measured was **GPT-4**, the benchmarks were **MT-Bench and Chatbot Arena**, and the paper is from 2023 | Yes, verbatim [D04-V14] | CONFIRMED-BUT-UNCONDITIONED | Add "(GPT-4 as judge on MT-Bench and Chatbot Arena, Zheng et al. 2023)". The draft's explicit note that this is a different population from the ~90% gate is **correct and should be kept** — this is the single best-handled number in the chapter. |
| N24 | "'20-50 simple tasks drawn from real failures is a great start'"; "15–100 for a first eval" | §3.3 | Yes, both | Yes | Yes | Yes, verbatim [D04-V04, D04-V06] | CONFIRMED | — |
| N25 | "'simple formatting changes … can lead to a ~5% change in accuracy'" | §3.3 | Yes | Yes | **No — and the ellipsis deletes the condition.** Full quote: "Simple formatting changes to the evaluation, such as **changing the options from (A) to (1)** … can lead to a ~5% change in accuracy." It is multiple-choice option relabeling on an MMLU-style benchmark | Yes [D04-V15] | CONFIRMED-BUT-UNCONDITIONED | "On a multiple-choice benchmark, relabeling the answer options — (A) to (1) — moved accuracy about 5% [D04-S21]." Do not elide the example. |
| N26 | one model "initially scored 42%" until "rigid grading that penalized '96.12' when expecting '96.124991…'" | §3.3 | Yes (Opus 4.5 on CORE-Bench) | Yes | Yes | Yes, verbatim [D04-V04] | CONFIRMED | — |
| N27 | canary ramp "1% → 5% → 20% → 50% → 100% with at least 24–48 hours per stage" | §3.4 | Yes | Yes | Source is a **practitioner blog**, not a standard | Yes, verbatim [D04-V16] | CONFIRMED | Label as one published convention, not "the" ramp. |
| N28 | shadow "~doubles inference spend while running" | §3.4 | Yes | Yes | Yes | Yes, verbatim [D04-V16] | CONFIRMED | — |
| N29 | "automated rollback thresholds such as p99 latency +40% or refusal rate +5%" | §3.4, §3.8, item 7 | Yes | Yes | Draft hedges with "such as" in §3.4 — good. **Item 7's rationale calls it "a standard canary rollback trigger"**, which over-claims a single secondary source | Yes, verbatim [D04-V16] | CONFIRMED | In item 7, "a common rollback trigger" not "a standard" one. |
| N30 | "'plan for tens of thousands of sessions per arm' for a 5% MDE at 80% power / 95% confidence" | §3.7 | Yes | Yes | Yes (MDE, power, confidence all stated — well done) | Yes, verbatim [D04-V16]. **Answers dossier open question 3: no primary Anthropic figure exists; this is practitioner-sourced only** | CONFIRMED | Add "(practitioner estimate; no Anthropic figure published)". |
| N31 | "'LLM output adds variance an order of magnitude larger' than product A/B math assumes" | §3.7 | Quote is on the page | **No** — "larger than" what is never quantified | No — the page attributes it to **Atil et al. (2024)**; D04-S30 is relaying, not measuring, and is `low` trust | Present, with a third-party attribution the draft drops [D04-V13] | CONFIRMED-BUT-UNCONDITIONED | Either attribute to Atil et al. via D04-S30, or replace with the durable statement: "LLM outputs are not deterministic even at temperature 0, so variance exceeds what standard product A/B sample-size math assumes; power the test on measured variance, not on a click-through analogy." |
| N32 | "multiple comparisons (Bonferroni/BH) or sequential/Bayesian methods [D04-S30]" | §3.7 | Content correct (textbook statistics) | n/a | n/a | **No.** The page contains no Bonferroni, no Benjamini-Hochberg, no Bayesian method, and only one passing mention of sequential testing | **NOT-FOUND** | State it uncited as standard practice, or cite a statistics reference. Remove the `[D04-S30]` tag. |
| N33 | "agent-loop cost cut 2.5–3.7× at 81–90% hit rates; one triage agent's bill fell 83%" | §3.5 | Yes. **It is cost, not latency** — the draft is correct on this | Yes (uncached agent loop) | Yes (hit rates stated) | Yes, verbatim: "it cut agent-loop cost by a factor of 2.5 to 3.7, at 81% to 90% hit rates; a small issue-triage agent's bill fell 83% from caching alone" [D04-V07] | CONFIRMED | — |
| N34 | "programmatic tool calling: −24% input tokens with a higher score" | §3.5 | Yes | Yes | Yes (agentic search benchmarks) | Yes [D04-V07] | CONFIRMED | — |
| N35 | "unaudited cross-generation prompts cost +36% per ticket at no accuracy gain; audited, 14% cheaper and 97% vs 92% accurate" | §3.5, §5 | Yes | **No** — "14% cheaper" is cheaper **than unaudited**, not than the original | No — the measurement is a **support-desk evaluation on the Opus 4.8 → Opus 5 migration**, both now legacy models | Yes [D04-V07] | CONFIRMED-BUT-UNCONDITIONED | "On one support-desk evaluation, prompts written for Opus 4.8 cost 36% more per ticket on Opus 5 with no accuracy change; after an audit the same prompts were 14% cheaper **than the unaudited versions** and more accurate (97% of tickets vs 92%) [D04-S07]." |
| N36 | "compaction cut a long run's bill a further 38%" | §3.5 | Yes | Yes ("a further" — after the free wins) | Yes (a long triage run, where it fired) | Yes [D04-V07] | CONFIRMED | — |
| N37 | "knowledge work: `low` gives up 1–3 points for a third to a half off" | §3.5 | Yes | **No** — the baseline is the model's **default effort**, which was `high` | **No** — "in Anthropic's runs (all with **Claude Fable 5**)". Draft names no model. The source also carries "`medium` matched the default's accuracy at 70%–85% of its cost", which the draft drops | Yes [D04-V07] | CONFIRMED-BUT-UNCONDITIONED | See Corrections C1. |
| N38 | "coding: ~2 points at `medium` for half the cost, ~8 points at `low` for a quarter" | §3.5 | Yes | **No** — baseline is `high`, the **Opus 5** default | **No** — measured on **Claude Opus 5**. On **Opus 5.5 `medium` is the default**, so this row as written implies a saving that does not exist there | Yes [D04-V07] | CONFIRMED-BUT-UNCONDITIONED | See Corrections C1. **This is the most dangerous number in the chapter.** |
| N39 | "~93% pass at ~$0.70/task vs 91.7% at $1.39 running everything at default" | §3.5 | Yes | Yes (all-at-default) | Partly — Anthropic's coding runs; requires a usable failure signal (the draft's "skip when" column covers this); drops "starting at `medium` solved ~94% for ~$0.95" and the doubled wall-clock on failures | Yes [D04-V07] | CONFIRMED-BUT-UNCONDITIONED | Add "on Anthropic's coding runs" and the wall-clock cost. Dollar figures are per-task at 2026 prices — date them. |
| N40 | "on one run 'two problems carried 43% of the spend'" | §3.5 | Yes | Yes | No — it was a **20-problem** research run, i.e. 10% of problems carried 43% of spend. Without the denominator the number loses its point | Yes [D04-V07] | CONFIRMED-BUT-UNCONDITIONED | "on one 20-problem research run, two problems carried 43% of the spend". |
| N41 | "a 16,384 cap ended 15% of one model's attempts and a third of another's, none solved, so cost per solved task did not improve" | §3.5, §6 | Yes | Yes | Yes (Anthropic coding runs; models sensibly anonymized) | Yes [D04-V07] | CONFIRMED | — |
| N42 | "context editing 'cost more than it saved' in the measured run" | §3.5 | Yes | Yes | Yes | Yes, verbatim [D04-V07] | CONFIRMED | — |
| N43 | Break-even: "first read at the 5-minute TTL (1.25× write + 0.1× read = 1.35× vs 2× uncached); second read at the 1-hour TTL (2× + 0.2× = 2.2× vs 3×)" | §3.6 | Yes — and the counting matches the pricing page's own wording ("pays off after one cache read for the 5-minute duration … after two cache reads for the 1-hour duration") | Yes | **No** — the arithmetic silently assumes a **0.1× read**. On Opus 5.5 (0.05×) it is 1.30× vs 2× and 2.10× vs 3×; on Fable 5.1/Mythos 5.1 (0.025×) 1.275× and 2.05×. I verified the **conclusions survive at all three rates** (1h TTL still needs a second read even at 0.025×), but the displayed numbers are model-specific and §3.6 does not say so | Yes [D04-V03, D04-V06] | CONFIRMED-BUT-UNCONDITIONED | Append: "arithmetic shown at the standard 0.1× read; on Opus 5.5 (0.05×) and Fable 5.1/Mythos 5.1 (0.025×) every break-even moves down proportionally, though the read-count conclusions do not change." |
| N44 | "minimum cacheable prefix is model-dependent (512–4096 tokens) and fails silently" | §3.6 | Yes (512 on the 5-series; 1024; 2048; 4096 on Opus 4.6/4.5/Haiku 4.5) | Yes | Yes. The non-monotonicity (Haiku 4.5 at 4096, newest models at 512) is a good exam discriminator the draft could add | Yes [D04-V06] | CONFIRMED | Optional: note the minimum is **not monotonic** across generations. |
| N45 | Batch: "most batches finish under 1 hour; results at completion or 24 h, whichever first; batches expire at 24 h and expired requests are not billed; 100,000 requests or 256 MB per batch; in-batch cache hits best-effort (observed 30–98%)" | §3.6 | **All correct** | Yes | Yes | Yes, all verbatim [D04-V10] | CONFIRMED | — |
| N46 | "prefer the 1-hour TTL" for batches | §3.6, item 6 | Yes | Yes | Yes | Yes: "Because batches can take longer than 5 minutes to process, consider using the 1-hour cache duration … for better cache hit rates when processing batches with shared context" [D04-V10] | CONFIRMED | — |
| N47 | "the published bar for a production cutover is around fifty cases and at least five trials per configuration" | §3.7 | Yes | Yes | Yes | Yes, verbatim [D04-V07] | CONFIRMED | — |
| N48 | "'verify twice' cost +48% per case, 'be maximally thorough' +39%" | S3 | Yes | Yes (per-case cost) | No — measured on one flow via duplicate lookups/re-deliberation (+48%) and unneeded tool calls (+39%); mechanism not stated in the draft | Yes [D04-V17] | CONFIRMED-BUT-UNCONDITIONED | Name the mechanism: "+48% through duplicate lookups and re-deliberation; +39% through unneeded tool calls". |
| N49 | "re-grading shrank a claimed +9-point win to +3 in a measured case" | §5, §7 h12 | Yes | Yes | Yes | Yes, verbatim [D04-V17] | CONFIRMED | — |
| N50 | "without [judge_usage], up to half the real cost of a model-graded eval is invisible" | §3.8 | Yes | Yes | Yes | Yes, verbatim [D04-V06] | CONFIRMED | — |
| N51 | "1M context / prices / lineup as published 2026-09-24" (§10 volatility note) | §10 | Yes — Fable 5.1, Opus 5.5, Sonnet 5, Haiku 4.5 current; Opus 5 legacy | n/a | Yes (dated) | Yes [D04-V03, D04-V18] | CONFIRMED | — |
| N52 | Item 6 stem: "80,000 requests … 11,000-token prefix" | item 6 | Request count is under the 100,000 limit, **but the payload is not.** 11,000 tokens ≈ 37 KB × 80,000 ≈ 3 GB, roughly 12× the **256 MB per-batch** limit | n/a | n/a | Limits per [D04-V10] | CONFIRMED-BUT-UNCONDITIONED (item defect) | Reduce to ~5,000 requests, or say "batched in submissions under the 256 MB limit". As written a well-prepared candidate can object to the keyed answer. |

**Explicit clearance on the flagged suspicion:** the noise-floor formula and the "25 × 2 ≈ ±14 points" worked
example are **not** the researcher's derivation. Both appear verbatim in Anthropic's bundled `claude-api`
skill (`shared/evals/eval-audit.md` §5 and `shared/evals/eval-hillclimb.md`), which is primary material.
The citation `[D04-S04, D04-S05]` is correct. The only defect is missing conditions (N7).

---

## Metric definition audit

| Metric | Definition as written in the draft | Correct? | Authoritative definition |
|---|---|---|---|
| pass@k | "measures the likelihood that an agent gets at least one correct solution in k attempts" | **Correct**, verbatim | Same [D04-V04] |
| pass^k | "measures the probability that all k trials succeed" | **Correct**, verbatim | Same [D04-V04] |
| Baseline latency | "model processing time for prompt plus response" | **Correct** | "the time taken by the model to process the prompt and generate the response, without considering the input and output tokens per second" [D04-V19] |
| TTFT | "time to the first token from send, 'particularly relevant when you're using streaming'" | **Correct**, verbatim | Same [D04-V19] |
| TPOT | "(E2EL − TTFT)/(output tokens − 1)" | **Correct** | Same [D04-V11] |
| ITL | "the gap between consecutive tokens" | **Correct** | "the exact pause between two consecutive tokens" [D04-V11] |
| E2EL | "TTFT + generation time" | **Correct** | Same [D04-V11] |
| Goodput | "requests per second completing **within** SLO" | **Correct** | "how many requests per second the LLM successfully completes while meeting your defined SLOs" [D04-V11] |
| Total prompt size | "`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`" | **Correct** | Same, verbatim [D04-V06] |
| precision / recall / specificity / FPR | Named, told to report separately, never defined | **Not wrong — undefined** | Standard confusion-matrix quantities. D04-S03 requires them as separate metrics [D04-V06] |
| recall@k | Named once (S5), **never defined** | **Undefined** | Fraction of all relevant items that appear in the top-k retrieved set |
| context precision / contextual precision | Named twice, **never defined** | **Undefined** | Per D04-S28: "whether the retrieval context is ranked in the correct order" [D04-V20] |
| contextual relevancy | Named, **never defined** | **Undefined** | "How relevant the retrieval context is to the input" [D04-V20] |
| contextual recall | Named, **never defined** | **Undefined** | "Whether the retrieval context contains all the information required to produce the ideal output" [D04-V20] |
| answer relevancy | Named, **never defined** | **Undefined** | "How relevant the generated response is to the given input" [D04-V20] |
| faithfulness | Named 3×, **never defined** | **Undefined** | "Whether the generated response contains hallucinations relative to the retrieval context" — the proportion of claims in the output not contradicted by the retrieved context [D04-V20] |
| groundedness | Used 2× (triage, item 7) as if interchangeable with faithfulness, **never defined** | **Undefined and unrelated to faithfulness by name** | Treat as the same property (every claim traceable to retrieved context) or drop one term. Using both without definition invites an item-level ambiguity |
| MRR, nDCG | **Absent from the draft** (present in the dossier) | n/a | Not a defect, but see Corrections C4 |
| ROUGE-L, cosine similarity | Named with their use cases, **never defined** | **Undefined** | ROUGE-L: longest common subsequence between candidate and reference. Cosine similarity: sentence-embedding similarity, 1 = identical [D04-V09] |
| "faithfulness → model/prompt/temperature" (the actionability mapping) | Asserted as part of a cited mapping | **NOT-FOUND at the cited source.** D04-S28 gives the lever for contextual relevancy (top-K, chunk size), contextual recall (embedding model), contextual precision (reranker) and answer relevancy (prompt template) — **but names no hyperparameter for faithfulness** | Keep four arms of the mapping; drop or relabel the faithfulness arm as inference [D04-V20] |

**Finding (MAJOR):** the chapter's first measured objective is "Define evaluation metrics," and it names
eleven component/RAG metrics without defining any of them. No definition is *wrong* — so this is not a
BLOCKER — but the objective is not met by naming. The metric→lever mapping also imports DeepEval/Confident-AI
vendor terminology ("contextual relevancy", "contextual precision") as if it were industry-standard
vocabulary; a candidate meeting those names for the first time on an exam will not recognize them.

---

## Claim verification table

| Claim | Location | Verdict | Source ID | Note |
|---|---|---|---|---|
| Exam guide Sample 3 is a Domain 4 item; answer B; "the other options would not be triggered specifically by a document refresh" | §1, S1, item 4, h1 | CONFIRMED | D04-V01 | Quoted accurately |
| Domain 4 objectives, all six, verbatim | front matter, §9 | CONFIRMED | D04-V01 | Exact match |
| Domain 4 is the "second-heaviest" domain | L3 | **CONTRADICTED** | D04-V01 | Third. D3=19%, D1=17% |
| Domain 4 is "the one" the guide illustrates with a sample | L4 | **CONTRADICTED** | D04-V01 | Three samples: D3, D2, D4 |
| Criteria are Specific, Measurable, Achievable, Relevant | §2.1 | CONFIRMED | D04-V08 | Verbatim |
| "…and states a threshold on a named population" | §2.1 | AUTHOR SYNTHESIS inside a cited sentence | D04-V08 | True and useful, but not in D04-S10. Split the sentence |
| "most use cases need multidimensional evaluation along several success criteria" | §2.1 | CONFIRMED | D04-V08 | Verbatim |
| "a variant that 'wins' on accuracy may have quietly traded recall for precision" | §2.2 | CONFIRMED | D04-V06 | Verbatim |
| A blended case "shows 0 whenever any one breaks" | §2.2, S5 | CONFIRMED | D04-V06 | Faithful |
| Metric→lever mapping (4 of 5 arms) | §2.2 | CONFIRMED | D04-V20 | faithfulness arm NOT-FOUND — see metric audit |
| "a single rep is a point estimate with no error bar" | §2.3 | CONFIRMED | D04-V06 | Faithful |
| Conflation definition (non-model artifact in the scored column) | §2.5 | CONFIRMED | D04-V06 | Verbatim in substance |
| "'No answer' is not 'negative answer'" | §2.5 | CONFIRMED | D04-V06 | Verbatim |
| "a `$0.00` cost or `0.0s` latency is almost never a real measurement" | §2.5 | CONFIRMED | D04-V06 | Verbatim |
| Truncated rows counted, not averaged in as wrong | §2.5 | CONFIRMED | D04-V06 | Verbatim in `build-eval.md` |
| "for rare high-stakes behaviours … fail-on-any or worst-case reflects what matters better than a mean diluted by easy cases" | §2.8 | CONFIRMED | D04-V06 | Verbatim |
| "one-sided evals produce one-sided optimisation" | §2.8 | CONFIRMED | D04-V06 | Verbatim |
| "red-team your own agent … test your workflow with documents, emails, and tool outputs that deliberately contain injection attempts" | §2.8, S4 | CONFIRMED | D04-V21 | Verbatim |
| Untrusted content belongs only in `tool_result`, never `system` or plain user text | §2.8, S4, §5 | CONFIRMED | D04-V21 | Verbatim in substance |
| Screen tool output with a classifier before returning it | S4, §5 | CONFIRMED | D04-V21 | Verbatim in substance |
| JSON-encode untrusted content; narrow tool scope | §5 | CONFIRMED | D04-V21 | Both on the page |
| Code-based grading "by far the best grading method if you can design an eval that allows for it" | §3.1 | CONFIRMED | D04-V22 | Verbatim |
| "often all that lies between you and an automatable eval is clever design" | §3.1 | CONFIRMED | D04-V06 | Faithful to `build-eval.md` |
| Grading is "a cost you will incur every time you re-run your eval, in perpetuity" | §3.1 | CONFIRMED | D04-V22 | Verbatim |
| Human grading "limits how often the eval can run" | §3.1 | CONFIRMED | D04-V22 | Faithful ("incredibly slow and expensive") |
| "judges are better at 'which of these two is better' than at placing a single output on an absolute scale" | §3.2 | CONFIRMED | D04-V06 | Verbatim |
| "never regenerate the reference, or 'win rate' silently changes meaning between rounds" | §3.2 | CONFIRMED | D04-V06 | Verbatim |
| Cross-case mode collapse is structurally invisible to a per-case pairwise judge | §3.2 | CONFIRMED | D04-V06 | Verbatim in substance |
| Cosine similarity for consistency; ROUGE-L for summarization | §3.2 | CONFIRMED | D04-V09 | Both on the page |
| Gold from the incumbent "makes the incumbent look best by construction" | §3.2, §6, item 2 | CONFIRMED | D04-V06 | Verbatim |
| Judge negatives: empty string, "I don't know", confident answer to the wrong question must all fail | §3.2 | CONFIRMED | D04-V06 | Verbatim |
| Position bias exists; mitigation = randomize order | §3.2, item 5 | CONFIRMED | D04-V06, D04-V14 | Named by Zheng et al.; randomization is `build-eval.md`'s own default |
| Verbosity bias exists; mitigation = instruct against length + track it | §3.2, item 5 | CONFIRMED | D04-V06, D04-V14 | Note D04-S26 finds verbosity preference **heterogeneous across judge models** — a nuance worth one clause |
| Self-preference bias exists; mitigation = cross-family judge | §3.2, item 5 | CONFIRMED | D04-V14, D04-V23 | D04-S25's actual mechanism is **perplexity/familiarity**: judges prefer low-perplexity text "regardless of whether the outputs were self-generated". The mitigation still follows; the mechanism claim should be stated as familiarity, not literal self-recognition |
| Label deference; mitigation = hide which is the reference | §3.2, item 5 | CONFIRMED | D04-V06 | In `eval-audit.md` |
| "use a different model to evaluate than the model used to generate" | §3.1–3.2, h5 | CONFIRMED | D04-V09 | Verbatim |
| D04-S26 exists and is a real paper | §3.2 | CONFIRMED | D04-V24 | arXiv 2604.23178 = "Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines", Soumik, Apr 2026. Not fabricated. Citation is decorative — every mitigation it backs is independently in D04-S03/S04 |
| "Prioritize volume over quality: more questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals" | §3.3 | CONFIRMED | D04-V09, D04-V22 | Verbatim in both |
| Edge-case list (irrelevant/nonexistent input, overlong input, harmful input, ambiguous cases) | §3.3 | CONFIRMED | D04-V09 | Verbatim |
| Leakage surfaces (prompt, few-shot, tool description, readable file, open web) | §3.3 | CONFIRMED | D04-V06 | Faithful |
| Benchmark contamination | §3.3 | CONFIRMED | D04-V15 | Page argues it via MMLU specifically; generalization is mild |
| Mislabeled / unanswerable benchmark items | §3.3 | CONFIRMED | D04-V15 | Verbatim (MMLU) |
| Automated evals "can create false confidence if misaligned with real usage" | §3.4, §3.7 | CONFIRMED | D04-V04 | Verbatim |
| A/B testing is "slow; days or weeks to reach significance and requires sufficient traffic" | §3.4 | CONFIRMED | D04-V04 | Verbatim |
| Shadow mode records outputs/latency/cost/errors and never returns output to users | §3.4 | CONFIRMED | D04-V16 | Faithful |
| Session-sticky assignment; lock the flag for the session | §3.4, §3.7, h10, item 10 | CONFIRMED | D04-V16 | Verbatim in substance |
| Three pre-registered adoption gates (quality band, cost margin, mechanism); "a cost tie with the right mechanism and a cost win with the wrong mechanism are both rejections" | §3.7, h6 | CONFIRMED | D04-V17 | Verbatim |
| "never keep or revert on a one-case swing" | §3.7 | CONFIRMED | D04-V07 | Verbatim |
| Validate a caching diff on a warm cache or "the 1.25× writes dominate and the free win reads as a regression" | §3.7, §5 | CONFIRMED | D04-V07 | Verbatim |
| Overfit signature: train up, test flat ⇒ revert | §3.7, §6 | CONFIRMED | D04-V06 | In `eval-hillclimb.md` |
| Re-grade every variant after any grader change | §3.7, §5 | CONFIRMED | D04-V06 | Verbatim |
| Free wins before tradeoffs "because each one changes what the model can do, and overshooting costs quality that the free wins never touch" | §3.5, h7 | CONFIRMED | D04-V07 | Verbatim |
| "the largest single lever on every model and benchmark Anthropic measured" (caching) | §3.5 (implied), dossier | CONFIRMED | D04-V07 | Verbatim |
| "with an eval you can *detect* that a stronger model at lower effort is the cheaper cell" | §3.5 | CONFIRMED | D04-V17 | Faithful |
| "output tokens are the latency lever too" | §3.5 | CONFIRMED | D04-V17 | Verbatim in `cost-hillclimb.md` §421 |
| "trying to reduce latency prematurely might prevent you from discovering what top performance looks like" | §3.5, §7 | CONFIRMED | D04-V19 | Verbatim |
| Streaming improves **perceived** responsiveness only | §2.6, h2, item 1 | CONFIRMED | D04-V19 | Verbatim ("can significantly improve the perceived responsiveness") |
| `max_tokens` is a blunt instrument that truncates | §3.5, §5, §6 | CONFIRMED | D04-V19, D04-V07 | Both sources |
| TTL choice by **start-to-start** gap; generation time counts against the TTL | §3.6, §5 | CONFIRMED | D04-V06 | Verbatim |
| Silent cache invalidators: timestamp, UUID, unsorted JSON, per-user tool list, effort change, model switch | §3.6, §5 | CONFIRMED | D04-V06, D04-V05 | Live effort page: "changing the top-level effort value between requests invalidates prompt caching" |
| Instrument `model` read from the **response**, not the config | §3.8, item 2 | CONFIRMED | D04-V06 | Verbatim, incl. "a silently substituted model … invalidates the comparison" |
| Restore quote-grounding and "I don't know" permission | §5, S1 | CONFIRMED | D04-V25 | Both on the page; direct-quote grounding is specified for >20k-token documents |
| Every production failure gets "a path back into the offline test set" | §3.8 | CONFIRMED (weak source) | D04-S31 (`low`) | Corroborated by `eval-audit.md`'s living-suite guidance [D04-V06]. Cite the primary, not the blog |
| SLOs written over rates measured on samples; goodput as the serving objective | §3.8 | CONFIRMED (synthesis) | D04-V11 | Reasonable synthesis; goodput definition is sourced, the SLO framing is the chapter's |
| Hallucination techniques reduce but do not eliminate | **absent** | n/a | D04-V25 | Docs carry the caveat explicitly; a safety-adjacent chapter should too |
| Bundled `claude-api` skill cached table (D04-S02) is stale | dossier §7.1 | CONFIRMED | D04-V26 | Verified by invoking the skill: its Current Models table is cached 2026-06-24, omits Opus 5.5, prices Opus 5 at $5/$25, and instructs "ALWAYS use `claude-opus-5`". The researcher was right to override it with live docs. The draft correctly follows live docs |
| No Claude Console eval tool claimed | §10 | CONFIRMED | D04-V08, D04-V09 | Neither page documents one. Dossier open question 1 answered: not found on either page today |

---

## Corrections required

**C1 — `[MAJOR]` §3.5, "Effort reduction" and "Re-run failures at higher effort" rows.** Replace the
Measured-effect cells with text that carries the model and the baseline:

> Effort reduction — *Measured effect:* against each model's **default** effort, on Anthropic's runs:
> knowledge work (all on Claude Fable 5, default `high`) `low` gave up 1–3 points for a third to a half off
> cost per task, and `medium` matched the default's accuracy at 70–85% of its cost; long-horizon coding (on
> Claude Opus 5, default `high`) gave up ~2 points at `medium` for half the cost and ~8 points at `low` for a
> quarter. **These are legacy models and the baseline is `high`. Claude Opus 5.5 defaults to `medium`, so a
> request that omits `effort` already runs one level below where Opus 5 ran** — the documented instruction is
> to run an effort sweep on your own evals rather than carry settings across generations [D04-S07, VF,
> platform.claude.com/docs/en/build-with-claude/effort].

Add one row to §2.7 or §3.5 stating the effort surface itself: `output_config.effort` ∈ {`low`, `medium`,
`high`, `xhigh`, `max`}; `high` is the default on every supporting model **except Opus 5.5, which defaults to
`medium`**; effort is "a behavioral signal, not a strict token budget"; it applies to all output tokens
including tool calls; and the manual `thinking: {enabled, budget_tokens}` mode is deprecated on the 4.6
generation and rejected later. Without this the chapter's central cost lever has no definition.

**C2 — `[MAJOR]` §3.7 "Corrections" row.** Delete `[D04-S30]` from the multiple-comparisons cell. Replace with:

> Corrections — multiple comparisons across variants and slices (Bonferroni or Benjamini-Hochberg), or a
> sequential / Bayesian design chosen in advance. *(Standard experimental statistics; no Anthropic guidance
> published on this point.)*

**C3 — `[MAJOR]` §2.6 misconception clause.** Replace:

> *Misconception:* that p50 is the user experience. The median is the typical experience and p99 is the
> slowest 1% of requests — the tail that queueing, cold caches, retries and a single slow tool live in
> [D04-S27 for the percentile definitions; the mechanism list is this chapter's synthesis], which is why
> canary rollback rules are written against p99 [D04-S29].

**C4 — `[MAJOR]` §2.2, add definitions.** The chapter must define, in one compact table, the component
metrics it then reasons with: recall@k, contextual/context precision, contextual recall, contextual
relevancy, answer relevancy, faithfulness (and either drop "groundedness" or define it as the same
property). Use the definitions in the Metric definition audit above. Also drop the faithfulness arm of the
metric→lever mapping, or relabel it:

> contextual relevancy → top-k and chunk size; contextual recall → embedding model; contextual precision →
> reranker; answer relevancy → prompt template [D04-S28]. Faithfulness has no single named knob — it moves
> with the grounding instructions, the model, and whether the retrieved context actually contains the answer.

Note in the chapter that "contextual relevancy / recall / precision" is DeepEval/Confident-AI vocabulary, not
a universal standard, so a candidate is not surprised by the naming.

**C5 — `[MAJOR]` line 3–4.** Replace with:

> **Weight: 16% of scored items (~10 of 63).** The third-heaviest domain, behind Integration (19%) and
> Solution Design (17%) — and one of the three the exam guide illustrates with a published sample item
> [D04-S01].

**C6 — `[MAJOR]` §2.7 and item 9 rationale, tokenizer.** Replace with the N21 formulation. The current text
implies every Claude-to-Claude migration incurs +30%; Haiku 4.5 is on the **older** tokenizer, so the effect
is generation-crossing (Opus 4.7 and later vs Sonnet 4.6 and earlier), not universal.

**C7 — `[MAJOR]` §3.3 formatting-change quote.** Restore the deleted condition per N25. The ellipsis removes
exactly the clause ("such as changing the options from (A) to (1)") that makes ~5% interpretable.

**C8 — `[MAJOR]` §2.5 and §5, infrastructure noise.** Add the SWE-bench counterpoint per N9. As written, a
candidate will generalize "infra config moves benchmarks ~6 points" to any harness change; the same study
measured 1.54 points on a different benchmark.

**C9 — `[MINOR]` §3.6 break-even row.** Append the per-model caveat from N43.

**C10 — `[MINOR]` §3.5 prompt-audit row.** Per N35: "14% cheaper **than the unaudited prompts**", and name
the Opus 4.8 → Opus 5 support-desk migration as the setting.

**C11 — `[MINOR]` §2.7.** `count_tokens` rejects every server tool **except the advisor tool**.

**C12 — `[MINOR]` §2.7.** "a third-party tokenizer" → "`tiktoken` and similar OpenAI tokenizers". The
~15–20% figure is measured for those, not for third-party tokenizers as a class.

**C13 — `[MINOR]` §3.7.** Attribute the variance claim to Atil et al. (2024) via D04-S30, or replace with
the durable statement in N31. Add "(practitioner estimate; no Anthropic figure published)" to the
tens-of-thousands-of-sessions figure.

**C14 — `[MINOR]` §3.2.** One clause on the two bias mechanisms: self-preference operates through
**familiarity / low perplexity**, not literal self-recognition [D04-S25]; and verbosity preference is
**heterogeneous across judge models** [D04-S26], so "instruct against length" is a mitigation to verify, not
a guaranteed fix.

**C15 — `[MINOR]` §2.4 and §7 heuristic 9.** Add the two missing conditions from N7 (worst-case at a 50%
pass rate; reps are not independent draws). Heuristic 9 currently reads "noise floor ≈ `1/sqrt(n·reps)`" with
no statement of what quantity it bounds — say "the 95% CI half-width on a binary pass rate, in points".

**C16 — `[MINOR]` §3.8 / §5.** Add the documented exception to the effort-invalidates-cache rule: on Fable
5.1, Mythos 5.1, Opus 5.5 and Opus 5, a per-message `output_config.effort` change (beta
`mid-conversation-output-config-2026-07-01`) **preserves** the prompt cache. Guidance: hold top-level effort
constant inside a cached conversation. Note the bundled skill's flat claim that mid-conversation effort
switching always re-bills the prefix is now superseded by the live effort page for these four models.

**C17 — `[MINOR]` item 6 stem.** Per N52, reduce the request count or acknowledge multiple batch submissions;
80,000 requests × an 11,000-token prefix is roughly 12× the 256 MB per-batch limit.

**C18 — `[MINOR]` item 3 distractor rationale.** See the Answer-key audit; the current rationale for D
contradicts the formula the item relies on.

**C19 — `[NIT]` §2.1.** Split "and states a threshold on a named population" out of the `[D04-S10]`-cited
sentence; it is the chapter's own (correct) addition.

**C20 — `[NIT]` §2.4 / N8.** Do not fuse the "~95%+" discrimination threshold with the "near the ceiling"
quotation; they are separate bullets in the source.

**C21 — `[NIT]` item 7 rationale.** "a common rollback trigger", not "a standard canary rollback trigger" —
the source is one practitioner blog.

**C22 — `[NIT]` §3.8.** Cite `eval-audit.md`'s living-suite guidance (primary) rather than D04-S31 (`low`)
for "every production failure becomes an offline case".

**C23 — `[NIT]` §2.8.** Add the docs' own caveat that grounding techniques "significantly reduce
hallucinations" but "don't eliminate them entirely" [D04-S13] — it is the reason groundedness needs a
measured rate rather than a checkbox.

---

## Answer-key audit

I solved all ten items independently before reading the keys.

| # | Keyed | My answer | Verdict | Notes |
|---|---|---|---|---|
| 1 | C | C | **KEY-CORRECT** | Flat TTFT + raised p95 E2EL localizes the regression after the first token; C is the only probe. A is fix-before-diagnosis and explains no tail-only effect; B truncates (D04-V07, D04-V19); D is perceived latency only (D04-V19). Distractor rationales all correct. No volatile dependency. |
| 2 | B, C | B, C | **KEY-CORRECT** | Exactly two defensible choices. A is the gold-from-the-incumbent trap [D04-V06]; D raises variance in a comparison; E is selection on the favorable tail. Set is complete and minimal. |
| 3 | B | B | **KEY-ARGUABLE** + **VOLATILE-DEPENDENCY** | B is right and the ±14 figure is correctly sourced (1/√50 = 0.141), so a 7-point move is inside the floor. Two defects: (a) the item's correctness turns entirely on the `1/sqrt(n·reps)` rule of thumb — if the floor were ±5, B would be false and the key would flip; (b) **the rationale for D is wrong on its own arithmetic.** Adding 400 cases *does* fix resolution (425 × 2 → ≈ ±3.4 points), so "without fixing this comparison's resolution" misstates the formula the item just used. Rewrite D's rationale to attack provenance: "400 *synthetic* cases add unlabeled volume — the same guidance that prefers volume also requires label provenance and grader spot-checks [D04-S04], and new cases cannot re-resolve the comparison already run." Also consider deleting distractor C, which introduces a judge the stem never mentions. |
| 4 | B | B | **KEY-CORRECT** | Directly tests the hypothesis the trigger implies [D04-V01]. A does not follow from a rebuild and cannot repair bad context; C is truncation; D is a cost signal. Cleanest item in the set. |
| 5 | A, D | A, D | **KEY-CORRECT** | A → position bias (randomize which candidate is A per case, D04-V06, D04-V14); D → verbosity bias (D04-V06). B invites label deference; C invites self-preference/self-enhancement [D04-V14, D04-V23]; E blends an unrelated signal into a metric that should stay atomic. Mitigations are the ones the literature actually supports. |
| 6 | A | A | **KEY-CORRECT** + **VOLATILE-DEPENDENCY** | Batch is 50% off both directions and stacks with caching [D04-V03, D04-V10], and the 1-hour TTL is the docs' own recommendation for batches with shared context [D04-V10]. 11,000 tokens clears every minimum cacheable prefix. Two soft defects: distractor C's rationale quotes "0.1× base input", which is model-dependent (0.05× on Opus 5.5, 0.025× on Fable 5.1/Mythos 5.1) though the conclusion holds at all three rates; and the stem's payload exceeds the 256 MB per-batch limit (N52, C17). "Batch requests run concurrently over up to 24 hours" is loose — 24 h is an expiry, and most batches finish in under an hour. |
| 7 | B | B | **KEY-CORRECT** | A deterministic, minutes-actionable step change. A and C need human judgment and change the test suite; D is suite hygiene. Rationale over-claims "standard" for a single secondary source (C21), but the item does not depend on the +5% number — a 2%→9% step in an hour is alertable on any threshold. |
| 8 | C | C | **KEY-CORRECT** | Matches the documented rule: treat an implausible judge-graded jump as suspicious before treating it as good news; "an LLM judge being gamed looks exactly like a breakthrough until you check" [D04-V06]. B tightens an interval around a possibly gamed metric; D reduces grader variance, not gameability. **Set-design note for the editor:** items 3 and 8 both present "surprising eval movement" and reach opposite verdicts on "add reps". The discriminator (inside the noise floor vs a large jump on a *model-graded* metric) is real but is never stated side by side in the chapter. Worth one sentence in §7. |
| 9 | B, C | B, C | **KEY-CORRECT** | B verified verbatim [D04-V06]; C verified against live docs — free, separate RPM limits by tier, returns an estimate [D04-V12]. A, D, E all false. E's rationale should carry the 4.7 boundary (C6). |
| 10 | B | B | **KEY-CORRECT** | Each stage answers a different question and only this order bounds blast radius while still reaching a causal read. A has no blast-radius control; C cannot see drift or user behavior [D04-V04]; D skips the operational check. The specific ladder is secondary-sourced [D04-V16] but the ordering logic is independent of it, so the item is fair. |

**Totals:** 9 KEY-CORRECT, 1 KEY-ARGUABLE, 0 KEY-WRONG. 2 items carry a VOLATILE-DEPENDENCY (3, 6). Item
count (10), format mix (7 single / 3 multiple-response with the count stated), and cognitive level all meet
the brief.

---

## Volatility watchlist

| Item | Current value (2026-09-24) | Re-check trigger |
|---|---|---|
| Cache-read multiplier per model | 0.1× base; 0.025× Fable 5.1 / Mythos 5.1; 0.05× Opus 5.5 | Any new model launch, or any change to the pricing page's prompt-caching footnotes. Re-check before every course revision — this is now a per-model fact, so each launch can add a row |
| Default effort per model | `high` everywhere except **Opus 5.5 = `medium`** | Any model launch. A new flagship with a different default silently changes every "vs default" effort figure in §3.5 |
| Effort measurement baselines | Fable 5 (knowledge), Opus 5 (coding), both vs `high` | When the `cost-optimization.md` guide is re-measured on current models, or when Fable 5 / Opus 5 retire (not before 2027-09-01 / 2027-09-22) |
| Tokenizer boundary | Opus 4.7 and later + Mythos Preview = new tokenizer (+~30%); Sonnet 4.6 and earlier, incl. Haiku 4.5 = old | When Haiku 4.5 is replaced (retirement not sooner than 2026-10-15) — a new Haiku on the current tokenizer removes the last old-tokenizer model from the lineup and changes the migration story |
| Batch semantics | 50% off; most <1 h; results at completion or 24 h; expire at 24 h, unbilled; 100,000 requests / 256 MB; in-batch cache hits 30–98% | Any change to the batch-processing page. Watch the `output-300k-2026-03-24` beta in particular — if 300K output goes GA, item 6-style stems need review |
| Cache break-even counting | Pays off after 1 read (5 m) / 2 reads (1 h), stated on the pricing page in the 0.1× frame | Same trigger as the cache-read multiplier. If a model's read rate drops further the arithmetic shown becomes more wrong even though the conclusion holds |
| Per-message effort beta | `mid-conversation-output-config-2026-07-01` on Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5 | GA promotion, or extension to more models. The bundled skill's contrary claim is already stale |
| Judge-agreement anchors | ~90% clear-cut operational gate (Anthropic); >80% human-preference agreement (Zheng et al. 2023) | If Anthropic publishes a judge-calibration number in public docs, promote it and demote the arXiv anchor |
| Minimum cacheable prefix | 512 / 1024 / 2048 / 4096 by model, non-monotonic | Every model launch |
| Domain weights and exam mechanics | 63 items, 120 min, cut 720, $175, 12 months; D4 = 16% | Exam guide version bump past v1.0 (effective July 2026) |
| Console eval tool | No live page found; chapter asserts nothing | Re-check `platform.claude.com/docs/en/test-and-evaluate/` quarterly. If such a tool ships, §3.1's grading ladder gains an option |
| Practitioner rollout numbers (24–48 h/stage, p99 +40%, refusal +5%, tens of thousands of sessions) | Single practitioner blog, `secondary` | Replace on sight with any primary Anthropic or major-vendor publication. These are the chapter's weakest-sourced numbers |

---

## Sources consulted

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|
| D04-V01 | Claude Certified Architect – Professional Exam Guide v1.0 | local: `/Users/anthonydugarte/Code/beon/claude-cert/claude-arch-professional-guide.md` | Anthropic | exam-guide | 2026-09-24 | primary | Domain weights (D3 19%, D1 17%, D4 16%) — contradicts "second-heaviest"; three sample items (D3, D2, D4) — contradicts "the one … chose to illustrate"; Sample 3 stem, key and rationale verbatim; Domain 4 objectives verbatim; 63 items / 120 min / cut 720 / $175 / 12 months |
| D04-V02 | Quantifying infrastructure noise in agentic coding evals | https://www.anthropic.com/engineering/infrastructure-noise | Anthropic (engineering) | anthropic-blog | 2026-09-24 | primary | "the gap between the most- and least-resourced setups on Terminal-Bench 2.0 was 6 percentage points (p < 0.01)"; infra errors 5.8% (1×) → 2.1% (3×) → 0.5% (uncapped); **SWE-bench only 1.54 pp at 5× RAM**; "leaderboard differences below 3 percentage points deserve skepticism"; time-of-day variation stated anecdotally |
| D04-V03 | Pricing | https://platform.claude.com/docs/en/about-claude/pricing | Anthropic | anthropic-docs | 2026-09-24 | primary | Current prices (Fable 5.1 $10/$50, Opus 5.5 $4/$20, Sonnet 5 $2/$10, Haiku 4.5 $1/$5); cache writes 1.25× (5 m) / 2× (1 h); cache read 0.1× with 0.025× Fable 5.1 + Mythos 5.1 and 0.05× Opus 5.5; "caching pays off after one cache read for the 5-minute duration … after two cache reads for the 1-hour duration"; Batch 50% both directions; discounts stack; web search $10/1,000; `inference_geo: "us"` 1.1×; **tokenizer: Claude 4.7+ and Mythos Preview ≈ +30% tokens, "Claude Sonnet 4.6 and earlier models use the previous tokenizer"** |
| D04-V04 | Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Anthropic (engineering) | anthropic-blog | 2026-09-24 | primary | pass@k / pass^k definitions verbatim; k=1 identical, k=10 "opposite stories"; "20-50 simple tasks drawn from real failures is a great start"; A/B "slow; days or weeks … requires sufficient traffic"; Opus 4.5 "initially scored 42%" on CORE-Bench with the 96.12 / 96.124991 grading bug; "better to grade what the agent produced, not the path it took" |
| D04-V05 | Effort | https://platform.claude.com/docs/en/build-with-claude/effort | Anthropic | anthropic-docs | 2026-09-24 | primary | Levels low/medium/high/xhigh/max; "Most Claude models default to high effort … Claude Opus 5.5 defaults to medium"; "a request that omits `effort` runs one level lower than it did on Claude Opus 5"; "Effort is a behavioral signal, not a strict token budget"; effort applies to all output tokens incl. tool calls; "Run an effort sweep on your own evals rather than carrying settings over from an earlier model"; "Changing the top-level effort value between requests invalidates prompt caching"; per-message effort preserves cache on Fable 5.1 / Mythos 5.1 / Opus 5.5 / Opus 5 via `mid-conversation-output-config-2026-07-01`; `budget_tokens` only alongside effort on Opus 4.5 |
| D04-V06 | `claude-api` skill — `shared/evals/{build-eval,eval-audit,eval-hillclimb}.md`, `shared/prompt-caching.md`, `shared/token-counting.md` | local: `/private/tmp/claude-501/bundled-skills/2.1.273/864daa6fbf18712038c2d2f2e5bb8b65/claude-api/shared/…` | Anthropic | anthropic-docs | 2026-09-24 | primary | Noise floor `1/sqrt(n·R)` with 25×2 ≈ ±14, 50×2 ≈ ±10, 100×2 ≈ ±7 (verified verbatim — **not** an author derivation); judge "well below ~90% on clear-cut cases" gate; ~95%+ discrimination bullet and the separate "near the ceiling" quote; conflation; "'No answer' is not 'negative answer'"; fail-on-any for rare high-stakes behaviours; both-directions coverage; pairwise defaults and frozen reference; cross-case mode collapse; `$0.00`/`0.0s` rule; token guesses off 3-10×; tiktoken −15–20%; `input_tokens` is the uncached remainder; min cacheable prefix table 512–4096 (non-monotonic); start-to-start TTL rule; judge_usage / "up to half the real cost is invisible"; assert the served model |
| D04-V07 | `claude-api` skill — `shared/cost-optimization.md` | local skill path (as above) | Anthropic | anthropic-docs | 2026-09-24 | primary | Caching "cut agent-loop cost by a factor of 2.5 to 3.7, at 81% to 90% hit rates; a small issue-triage agent's bill fell 83%"; "largest single lever on every model and benchmark Anthropic measured"; prompt audit Opus 4.8 → Opus 5, +36% per ticket, audited 14% cheaper than unaudited at 97% vs 92%; effort curves (**knowledge work all on Claude Fable 5; long-horizon coding on Claude Opus 5**); re-run failures 93% @ ~$0.70 vs 91.7% @ $1.39 (and ~94% @ ~$0.95 from `medium`); `max_tokens` 16,384 ended 15% of Opus 5's and a third of Fable 5's attempts, none solved; compaction −38%; context editing cost more than it saved; programmatic tool calling −24% input tokens; 20-problem run, two problems 43% of spend; fifty cases / five trials; warm-cache validation; "never keep or revert on a one-case swing"; batch 50% off every token incl. cache reads and writes |
| D04-V08 | Define success criteria | https://platform.claude.com/docs/en/test-and-evaluate/define-success | Anthropic | anthropic-docs | 2026-09-24 | primary | Eight criterion categories incl. latency and price; Specific/Measurable/Achievable/Relevant verbatim; "Less than 0.1% of outputs out of 10,000 trials flagged for toxicity by the content filter"; "Most use cases need multidimensional evaluation along several success criteria"; **no Console eval tool mentioned or linked** |
| D04-V09 | Develop test cases | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests | Anthropic | anthropic-docs | 2026-09-24 | primary | "Prioritize volume over quality: More questions with slightly lower signal automated grading is better than fewer questions with high-quality human hand-graded evals"; exact match / cosine similarity (SBERT) / ROUGE-L (longest common subsequence) / LLM Likert-binary-ordinal; edge-case list verbatim; "use a different model to evaluate than the model used to generate"; **no Console eval tool** |
| D04-V10 | Batch processing | https://platform.claude.com/docs/en/build-with-claude/batch-processing | Anthropic | anthropic-docs | 2026-09-24 | primary | 50% of standard prices; "most batches finishing in less than 1 hour"; "access batch results when all messages have completed or after 24 hours, whichever comes first. Batches expire if processing does not complete within 24 hours"; expired requests "You will not be billed"; 100,000 requests or 256 MB; cache hits best-effort, "30% to 98%"; "consider using the 1-hour cache duration … when processing batches with shared context"; `max_tokens: 0` unsupported in batch; `output-300k-2026-03-24` beta raises max_tokens to 300,000 on Opus 5.5 / 5 / 4.8 / 4.7 / 4.6, Sonnet 5, Sonnet 4.6 |
| D04-V11 | LLM Inference Handbook — key inference metrics | https://handbook.modular.com/llm-inference-basics/llm-inference-metrics | Modular | vendor-docs | 2026-09-24 | secondary | TTFT, E2EL = TTFT + generation time, TPOT = (E2EL − TTFT)/(output tokens − 1), ITL "the exact pause between two consecutive tokens", RPS/TPS, goodput "requests per second the LLM successfully completes while meeting your defined SLOs"; metric-by-workload table. **Fetched twice with a targeted percentile prompt: the page says median "shows the typical user experience" and P99 "reveals worst-case performance for the slowest 1%" / "captures tail latency" — it does NOT mention queueing, cold starts or batch interference** |
| D04-V12 | Token counting | https://platform.claude.com/docs/en/build-with-claude/token-counting | Anthropic | anthropic-docs | 2026-09-24 | primary | Free, RPM 5,000 / 10,000 / 20,000 by tier, separate from message-creation limits; "The token count is an **estimate**"; rejects server tools **except the advisor tool**, the MCP connector, and `url`/`file` sources; "Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer. The same input text produces approximately 30 percent more tokens than on earlier models"; no caching in count_tokens |
| D04-V13 | How to A/B test LLM applications in production | https://atlan.com/know/ab-testing-llm-applications/ | Atlan | practitioner-blog | 2026-09-24 | low | "LLM output adds variance an order of magnitude larger, **per Atil et al. (2024)**". **Contains no Bonferroni, no Benjamini-Hochberg, no Bayesian method, and only a single passing mention of sequential testing; no non-inferiority discussion** — the draft's §3.7 Corrections citation is unsupported |
| D04-V14 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | https://arxiv.org/abs/2306.05685 | Zheng et al. (NeurIPS 2023) | academic | 2026-09-24 | secondary | "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans"; benchmarks MT-Bench and Chatbot Arena; names position bias, verbosity bias, self-enhancement bias, limited reasoning ability |
| D04-V15 | Challenges in evaluating AI systems | https://www.anthropic.com/research/evaluating-ai-systems | Anthropic (research) | anthropic-blog | 2026-09-24 | primary | "Simple formatting changes to the evaluation, **such as changing the options from (A) to (1)** … can lead to a ~5% change in accuracy"; MMLU contamination argument; "we have found examples in MMLU that are mislabeled or unanswerable"; "Red teaming AI systems is presently more art than science" |
| D04-V16 | Releasing AI features without breaking production: shadow mode, canary, A/B testing for LLMs | https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing | Tian Pan | practitioner-blog | 2026-09-24 | secondary | "roughly doubles your inference spend during evaluation"; "1% → 5% → 20% → 50% → 100%" with "24-48 hours minimum"; session-sticky assignment; "if p99 latency increases by more than 40%, if the refusal rate jumps by more than 5%"; "plan for tens of thousands of sessions per arm" at "5% minimum detectable effect with 80% power and 95% confidence" |
| D04-V17 | `claude-api` skill — `shared/evals/cost-hillclimb.md` | local skill path (as above) | Anthropic | anthropic-docs | 2026-09-24 | primary | Three pre-registered gates and "a cost tie with the right mechanism and a cost win with the wrong mechanism are both rejections"; "verify twice" +48% via duplicate lookups/re-deliberation and "be maximally thorough" +39% via unneeded tool calls; "+9-point win to +3"; "Output tokens are the latency lever too"; 650-character directive that only tied on cost; 3/3 effort switches re-billed the full prefix, 0/9 same-effort continuations did — **and the now-superseded claim that per-surface cache-preserving effort switching "does not transfer to API customers"** |
| D04-V18 | Models overview | https://platform.claude.com/docs/en/about-claude/models/overview | Anthropic | anthropic-docs | 2026-09-24 | primary | Current lineup and IDs (via `VERIFIED-FACTS.md` cross-check); Opus 5 legacy; latency ordering |
| D04-V19 | Reducing latency | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency | Anthropic | anthropic-docs | 2026-09-24 | primary | Baseline latency and TTFT definitions verbatim; "It's always better to first engineer a prompt that works well … Trying to reduce latency prematurely might prevent you from discovering what top performance looks like"; streaming "can significantly improve the perceived responsiveness"; `max_tokens` "a blunt technique"; paragraph/sentence limits beat word counts |
| D04-V20 | RAG evaluation metrics: answer relevancy, faithfulness and more | https://www.confident-ai.com/blog/rag-evaluation-metrics-answer-relevancy-faithfulness-and-more | Confident AI | practitioner-blog | 2026-09-24 | secondary | Definitions of contextual relevancy / recall / precision, answer relevancy, faithfulness; levers confirmed for contextual relevancy → top-K + chunk size, contextual recall → embedding model, contextual precision → reranker, answer relevancy → prompt template. **No hyperparameter is named for faithfulness — the draft's "faithfulness → model/prompt/temperature" is not supported here** |
| D04-V21 | Mitigate jailbreaks and prompt injections | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | Anthropic | anthropic-docs | 2026-09-24 | primary | Two threat models; "Put untrusted content only in tool results … never in `system` prompts or plain user `text` blocks"; "Screen tool outputs before Claude acts on them"; JSON-encode untrusted content; least privilege; "Red-team your own agent. Before deploying, test your workflow with documents, emails, and tool outputs that deliberately contain injection attempts"; continuous monitoring for successful injection |
| D04-V22 | Cookbook — Building evals (`misc/building_evals.ipynb`) | https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/misc/building_evals.ipynb | Anthropic | anthropic-cookbook | 2026-09-24 | primary | Four parts of an eval verbatim; "by far the best grading method if you can design an eval that allows for it, as it is super fast and highly reliable"; human grading "incredibly slow and expensive … mostly try to avoid"; "a cost you will incur every time you re-run your eval, in perpetuity"; "your preference should be for higher volume and lower quality of questions over very low volume with high quality" |
| D04-V23 | Self-Preference Bias in LLM-as-a-Judge | https://arxiv.org/abs/2410.21819 | Wataoka, Takahashi, Ri | academic | 2026-09-24 | secondary | Real paper (Oct 2024, rev. Jun 2025). Mechanism is **perplexity/familiarity**: "LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, **regardless of whether the outputs were self-generated**" — supports the cross-family mitigation but refines the "prefers its own text" framing |
| D04-V24 | Judging the Judges: A Systematic Evaluation of Bias Mitigation Strategies in LLM-as-a-Judge Pipelines | https://arxiv.org/abs/2604.23178 | Sadman Kabir Soumik | academic | 2026-09-24 | low | **Verified real** (Apr 2026, rev. Jun 2026) — the researcher's `low`-trust flag was about access method, not existence. Nine debiasing methods, five judge models, three benchmarks, four bias categories; style bias predominant; **verbosity preferences heterogeneous across models**. Citation in the draft is decorative; every mitigation it backs is independently primary-sourced |
| D04-V25 | Reduce hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Anthropic | anthropic-docs | 2026-09-24 | primary | "Allow Claude to say 'I don't know'"; direct quotes for factual grounding on documents ">20k tokens"; verify-with-citations and retract-unsupported-claims; CoT verification; best-of-N; external knowledge restriction; "while these techniques significantly reduce hallucinations, they don't eliminate them entirely" |
| D04-V26 | `claude-api` skill invocation (v2.1.273) — Current Models table | local: skill base `/private/tmp/claude-501/bundled-skills/2.1.273/864daa6fbf18712038c2d2f2e5bb8b65/claude-api` | Anthropic | anthropic-docs | 2026-09-24 | primary (but **stale**) | Invoked per task instruction. Table is cached **2026-06-24**: omits Opus 5.5, prices Opus 5 at $5/$25, instructs "ALWAYS use `claude-opus-5`", states effort "default `high`" without the Opus 5.5 exception, and records the Mythos 5.1 cache rate as "open at launch". Live docs [D04-V03, D04-V05] and `VERIFIED-FACTS.md` supersede it on every point. Confirms the researcher's dossier §7.1 contradiction finding |
| D04-V27 | VERIFIED-FACTS.md (project canonical ground truth) | local: `/Users/anthonydugarte/Code/beon/claude-cert/prep-course-track-b/VERIFIED-FACTS.md` | orchestrator, from Anthropic primaries | other | 2026-09-24 | primary (derived) | Cross-checked against live docs on every point I touched — **no discrepancies found.** Lineup, prices, default effort (incl. Opus 5.5 = `medium`), cache-read multipliers, batch 50%, 300K-output beta header and model list, tokenizer boundary, and the per-message-effort cache exception all match the live pages I fetched |
