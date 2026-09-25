# Validation Report — Domain 1: Solution Design & Architecture

Validator deliverable. Independent fact-check against primary sources, performed 2026-09-24. Draft
reviewed: `drafts/01-solution-design-draft.md`. Dossier and source table read but not trusted; every
citation below was checked against the live source or `VERIFIED-FACTS.md`.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. Three places present a paraphrase as a verbatim quotation (quotation marks around text that does
   not match the live source word-for-word): the S5 scenario's "exact worked example" claim (§5), and
   two quotes in §4.8 ("handoff and merge cost more than the plan"; "must beat the single model's full
   effort curve"). Fix wording or drop the quotation marks — see Corrections Required.
2. §11's model-currency note and §4.8's multi-model section never name Claude Fable 5.1 or state the
   docs' "default → raise effort → only then change model" escalation method, even though
   VERIFIED-FACTS.md flags this as the single most important model-selection heuristic. Not a factual
   error, but a completeness gap on a heavily-weighted objective (model selection feeds Domain 2 too).
3. D01-S18 (Managed Agents multiagent orchestration docs) is listed in the bibliography but never cited
   in the chapter body — dead citation, low severity but should be removed or used.
```

No BLOCKER findings. The highest-scrutiny items (pattern taxonomy, token multipliers, business-value-pillars
attribution, model currency) all came back clean or better-than-expected. The chapter is unusually well
sourced — of ~45 distinct quoted or numeric claims independently traced to primary sources in this pass,
41 were CONFIRMED verbatim or near-verbatim, 3 were CONFIRMED-in-substance-but-misquoted (listed above),
and 1 is a NIT (unused citation). Zero CONTRADICTED-in-substance findings.

---

## Pattern taxonomy audit

Source: "Building effective agents," Anthropic Engineering, <https://www.anthropic.com/engineering/building-effective-agents>,
fetched live 2026-09-24 (multiple targeted fetches for verbatim text). This is the domain's single most
load-bearing citation (D01-S02) and the brief's highest-scrutiny item (a).

| Claimed pattern | Name matches source? | Mechanics match? | Evidence |
|---|---|---|---|
| Augmented LLM | Yes | Yes | "an LLM enhanced with augmentations such as retrieval, tools, and memory"; "generating their own search queries, selecting appropriate tools, and determining what information to retain" |
| Workflow (category) | Yes | Yes, exact | "Workflows are systems where LLMs and tools are orchestrated through predefined code paths" |
| Agent (category) | Yes | Yes, exact | "Agents...are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks" |
| Prompt chaining | Yes | Yes | "decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one"; "ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks"; "trade off latency for higher accuracy" |
| Routing | Yes | Yes, exact | "classifies an input and directs it to a specialized followup task"; "where classification can be handled accurately" |
| Parallelization — sectioning | Yes | Yes | "Breaking a task into independent subtasks run in parallel" |
| Parallelization — voting | Yes | Yes | "Running the same task multiple times to get diverse outputs"; "multiple perspectives or attempts are needed for higher confidence results" |
| Orchestrator-workers | Yes | Yes, exact | "A central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results"; "subtasks aren't pre-defined, but determined by the orchestrator based on the specific input" |
| Evaluator-optimizer | Yes | Yes, exact | "One LLM call generates a response while another provides evaluation and feedback in a loop"; "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value" |
| Agent loop / ground truth | Yes | Yes | "gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress"; "common to include stopping conditions (such as a maximum number of iterations)" |

**Governing quotes** — all CONFIRMED verbatim:
- "finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all."
- "you should consider adding complexity _only_ when it demonstrably improves outcomes." (source italicizes "only")
- "workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale."
- "Agentic systems often trade latency and cost for better task performance"
- Three implementation principles confirmed: simplicity, transparency of planning steps, and ACI craftsmanship including "Poka-yoke your tools. Change the arguments so that it is harder to make mistakes."
- "Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production."

**No pattern is renamed, merged, split, or invented.** This is the strongest-verified section of the
chapter, not a weak point.

---

## Claim verification table

Legend: `CONFIRMED` = verified verbatim or in exact substance against a live primary source or
VERIFIED-FACTS.md. `CONFIRMED*` = substance correct, but quoted text does not match the source word for
word (see Corrections Required). `NOT-FOUND` = claim not located in the cited or any searched source.
`CONTRADICTED` = source says something different.

| # | Claim | Location | Status | Source | Note |
|---|---|---|---|---|---|
| 1 | Full ten-pattern taxonomy + governing quotes (Building effective agents) | §3.1–3.4, §4.1, §4.3 | CONFIRMED | D01-V01 | See taxonomy audit above |
| 2 | "Multi-agent system...outperformed single-agent Claude Opus 4 by 90.2%" on internal research eval | §4.2 | CONFIRMED | D01-V02 | Exact: "a multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval." Anthropic's own internal eval, not a public benchmark; 90.2% is a relative improvement over the single-agent baseline's score, not an absolute accuracy figure. |
| 3 | Agents "~4× more tokens than chat"; multi-agent "~15× more tokens than chats" | §4.2 | CONFIRMED | D01-V02 | Exact: "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats." Baseline = plain chat, correctly labeled throughout the draft. |
| 4 | Multi-agent "3 to 10 times more tokens than single-agent approaches" | §3.9, §4.2 (M2), §4.6, §4.8, Items 3/8/11/12 | CONFIRMED | D01-V03 | Exact (appears twice): "multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks." Baseline = single agent, correctly distinguished from the chat baseline everywhere checked in the draft. |
| 5 | "Token usage by itself explains 80% of the variance" (BrowseComp) | Dossier only (not restated as a numbered claim in draft body, informs §4.2 framing) | CONFIRMED | D01-V02 | Exact: "three factors explained 95% of the performance variance in the BrowseComp evaluation... token usage by itself explains 80% of the variance." |
| 6 | Parallel subagents "cut research time by up to 90% for complex queries" | Dossier only | CONFIRMED | D01-V02 | Verbatim. |
| 7 | ~20 test cases as an evaluation starting point | Dossier only | CONFIRMED | D01-V02 | Exact: "We started with a set of about 20 queries representing real usage patterns." |
| 8 | Rainbow deployments quote | Dossier only | CONFIRMED | D01-V02 | Verbatim match. |
| 9 | Context-protection example: order history degrading technical diagnosis | §4.2, S5 | CONFIRMED* | D01-V03 | Source: "If every order lookup adds thousands of tokens to the context, the agent's ability to reason about the technical problem degrades." Draft/S5 renders this as "Order details add thousands of tokens that degrade reasoning about the technical problem" **inside quotation marks, labeled "Anthropic's exact worked example."** It is a paraphrase, not a verbatim quote — see Corrections Required. |
| 10 | "20+" tools specialization signal | §3.9, §4.2, Item 3 | CONFIRMED | D01-V03 | Exact: "An agent with too many tools (often 20+) struggles to select the appropriate one." |
| 11 | Telephone-game quote + "spent more tokens on coordination than on actual work" | §3.9, §4.6, failure-mode table | CONFIRMED | D01-V03 | Both verbatim. |
| 12 | "An agent handling a feature should also handle its tests..." | §3.9 | CONFIRMED | D01-V03 | Verbatim (source: "Dividing by context boundaries means an agent handling a feature should also handle its tests, because it already possesses the necessary context.") |
| 13 | Verification subagent "dominant failure mode" = marking outputs passing without thorough testing | §4.5, Item 12 | CONFIRMED | D01-V03 | Source: "The most significant failure mode for verification subagents is marking outputs as passing without thorough testing." Draft's "dominant" for "most significant" is an acceptable synonym, quoted portion matches exactly. |
| 14 | "Verification requires minimal context transfer by nature" | §4.5, Item 12 | CONFIRMED | D01-V03 | Verbatim. |
| 15 | "Two subagents editing the same file in parallel is a recipe for conflict" | §4.6, Item 12 | CONFIRMED | D01-V04 | Verbatim, from D01-S20 (correctly cited there, not D01-S04). |
| 16 | "Exploring ten or more files, or...three or more independent pieces of work" delegation signal | §4.2 | CONFIRMED | D01-V04 | Verbatim. |
| 17 | Subagents "cannot communicate directly" | §3.7, §4.2, Item 8 | CONFIRMED (substance) | D01-V04 | Source phrasing: "Subagents report back to the main conversation but can't talk to one another." Draft never quotes this directly (states it as a paraphrase, uncited in quotation marks), so no fidelity issue. |
| 18 | "Too many specialist agents" / sequential dependent work poor fit | §4.6 | CONFIRMED | D01-V04 | Verbatim substance: "flooding Claude with options makes automatic delegation less reliable"; sequential-chain guidance confirmed. |
| 19 | "business value pillars" / 5-item list is blueprint-only, no Anthropic source uses it | §3.12, §4.8 | CONFIRMED | D01-V05, D01-V06 | Targeted web search for the exact phrase and for the 5-item list returned no Anthropic material using either. The enterprise ebook (D01-S21, directly read as PDF, 20 pages) uses "Create business value" as a stage title but never "pillars," and never lists efficiency/transformation/productivity/cost/performance-SLAs together. Draft's `[UNVERIFIED]`-as-Anthropic-framework flag is correct and should be preserved. |
| 20 | "27% of Claude-assisted work wouldn't have been done otherwise" | §3.12, §4.8, Item 11 | CONFIRMED (near-verbatim) | D01-V07 | Live page: "27% of Claude-assisted work consists of tasks that wouldn't have been done otherwise." Draft's phrasing is a trivial, meaning-preserving compression, not flagged as a quote in the draft — fine. Population: 132 Anthropic engineers/researchers, surveyed August 2025; article published Dec 2025. |
| 21 | Enterprise-ebook pilot-selection criteria (7 items) verbatim | §3.12 dossier, used to ground Objective 1 in draft §2/§4.8 | CONFIRMED | D01-V08 | All seven criteria phrases ("Well suited to LLM capabilities," "Meaningful and measurable success metrics," "Clear return on investment," "Business critical, but low security risk," "Abundant data," "Minimal disruption to existing processes," "Scalable and duplicable") appear verbatim on p.15–16 of the PDF. |
| 22 | External/revenue-oriented vs. internal/cost-and-risk-oriented use-case split | Dossier (Objective 1) | CONFIRMED | D01-V08 | Verbatim table headers on p.5 of the PDF: "External, revenue-oriented" / "Internal, cost- and risk-oriented." |
| 23 | Success-criteria rubric: Specific/Measurable/Aligned/Time-bound | Dossier (Objective 1) | CONFIRMED | D01-V08 | Verbatim on p.16. |
| 24 | Graduation criteria: Performance thresholds / Operational readiness / Risk management infrastructure | Dossier (Objective 1) | CONFIRMED | D01-V08 | Verbatim on p.6. |
| 25 | Enterprise ebook is stale on model names (Claude 3.5 Sonnet / 3 Opus / 3.5 Haiku, 200K context) | §6 dossier note; draft correctly avoids using this content as current | CONFIRMED | D01-V08 | p.18–19 of the PDF: "Claude 3.5 Sonnet may be most suitable...Claude 3 Opus excels...Claude 3.5 Haiku...All Claude 3 (including 3.5 models) offer a 200K token context window." Confirms this content is stale; draft's decision not to use it for current model facts is correct. |
| 26 | Claude Opus 5.5 is the docs' current default; $4/$20 per MTok, 1M context, 128K max output, default effort `medium`, released 2026-09-22 | §11 (and source table) | CONFIRMED | VF, D01-V09 | Matches VERIFIED-FACTS.md and live models overview exactly. No instance found anywhere in the draft presenting Opus 5 (not 5.5) as current — every Opus 5 mention is explicitly framed as the stale/legacy fact being corrected. |
| 27 | Tool-use system-prompt overhead: 286 (Opus 5.5) / 354 (Sonnet 5) / 496 (Haiku 4.5) tokens | §4.7 | CONFIRMED | D01-V10 | Live docs table (auto/none column) matches exactly. |
| 28 | Batch API: 50% discount, "most batches finishing in less than 1 hour," 100,000 requests/256 MB limit, 24-hour expiry, results any order keyed by `custom_id` | §3.10, §4.4, §4.8, Items 1/9 | CONFIRMED | D01-V09 | All verbatim against live batch-processing docs. |
| 29 | Streaming changes TTFT/perceived latency, not total generation time; required for very large `max_tokens` | §3.10, §4.4 | CONFIRMED | D01-V09 | Live docs: streaming required for "requests with large max_tokens values, where the SDKs require streaming to avoid HTTP timeouts." Latency-perception framing is a reasonable, non-contradicted characterization of SSE mechanics. |
| 30 | Cache-read pricing (10% base; 5% Opus 5.5; 2.5% Fable 5.1/Mythos 5.1) | Dossier / VF only | N/A — not restated in draft body | — | Grepped the full draft: no cache-read percentage figures appear anywhere in the shipped chapter text. Nothing to contradict; flagged as a completeness gap, not an error (see must-fix #2). |
| 31 | "Managed Agents" session/harness/sandbox virtualization + TTFT p50 −60%/p95 >90% | §3.5 | CONFIRMED | D01-V11 | Verbatim: "our p50 TTFT dropped roughly 60% and p95 dropped over 90%"; session/harness/sandbox definitions match exactly, including `wake(sessionId)` / resume-from-last-event. |
| 32 | Harness components "encode an assumption...those assumptions are worth stress testing"; sprint decomposition removed after model upgrade | §3.5, AP7 | CONFIRMED | D01-V12 | Verbatim, including the specific example of context-reset code becoming unnecessary on a newer model. |
| 33 | Self-evaluation "confidently prais[es] the work" | §3.11, §4.5, AP4, Item 4 | CONFIRMED | D01-V12 | Verbatim: "agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre." |
| 34 | "A reset provides a clean slate, at the cost of the handoff artifact..." | §3.5, §4.6, Item 10 | CONFIRMED | D01-V12 | Verbatim. |
| 35 | "The best form of feedback is providing clearly defined rules..." | §3.11, §4.5, Item 4 | CONFIRMED | D01-V13 | Verbatim. |
| 36 | "generally not a very robust method, and can have heavy latency tradeoffs" (LLM-as-judge) | §4.5 | CONFIRMED | D01-V13 | Verbatim. |
| 37 | "gather context → take action → verify work → repeat" | §3.4, §4.1 | CONFIRMED | D01-V13 | Verbatim (source uses "->" arrows; trivial typographic difference). |
| 38 | Context rot definition + n² pairwise relationships + "performance gradient rather than a hard cliff" | §3.6, AP6 | CONFIRMED | D01-V14 | All three phrases verbatim. |
| 39 | Subagent summaries "typically 1,000–2,000 tokens" | §3.7, §4.2 | CONFIRMED | D01-V14 | Source: "often 1,000-2,000 tokens." |
| 40 | Tool consolidation example (`schedule_event` vs. `list_users`+`list_events`+`create_event`); "more tools don't always lead to better outcomes" | §4.7, AP5 | CONFIRMED | D01-V15 | Verbatim. |
| 41 | "Price the tail...two problems carried 43% of the spend" (WideSearch) | §4.8 | CONFIRMED | D01-V16 | Verbatim, including the specific 20-problem/43%-spend example. |
| 42 | Caching "cut agent-loop cost by a factor of 2.7 to 5.3" | §4.8 | CONFIRMED | D01-V16 | Verbatim. |
| 43 | Advisor strategy: pays when consultations replace running the advisor model for the whole task; fails when "an executor at low effort can stop detecting that it is stuck" | §4.8 | CONFIRMED | D01-V16 | Quoted fragment verbatim. |
| 44 | Orchestrator strategy: pays with bulk/parallel work exceeding one context; "handoff and merge cost more than the plan" | §4.8, Item 6 | CONFIRMED* | D01-V16 | Substance correct, but the quoted fragment is not verbatim — see Corrections Required. |
| 45 | "Multi-model configurations must beat the single model's full effort curve" | §4.8 | CONFIRMED* | D01-V16 | Live doc: "A multi-model configuration must beat the single model's whole curve." Not verbatim — see Corrections Required. |
| 46 | "Tuning effort is often a better lever than switching models" | §4.8 dossier (Objective 6 latency levers) | CONFIRMED | D01-V17 | Verbatim on the "Choosing the right model" page. |
| 47 | Subagent SDK: four benefits (context isolation, parallelization, specialized instructions, tool restrictions); doc-reviewer example; "the only content you pass...is the Agent tool's prompt string"; depth default 3, concurrency default 20, spend uncapped by default | §3.7, §4.2, Item 5, Item 8 | CONFIRMED | D01-V18 | All verbatim, including the exact env-var defaults table. |
| 48 | Exam mechanics: 63 items, 17% weight for Domain 1, ~10–11 item count | Front matter §1, §11 | CONFIRMED | D01-V19 (exam guide) | 17% × 63 = 10.71; "~10–11" is a correct, appropriately hedged rounding. No instance of 120 min/720/175/12-month restated incorrectly — these simply are not restated in this domain chapter at all (not required by scope). |
| 49 | D01-S18 (Managed Agents multiagent orchestration docs, "escalation" delegation pattern) | Bibliography only | N/A | — | Never cited inline anywhere in the draft body (grepped). Dead citation — NIT. |

---

## Corrections required

1. **§5, Scenario S5** — currently: *"This stem contains Anthropic's exact worked example — 'Order
   details add thousands of tokens that degrade reasoning about the technical problem' — and its exact
   specialization signal [D01-S04]."*
   Replace with: *"This stem mirrors Anthropic's own worked example — 'If every order lookup adds
   thousands of tokens to the context, the agent's ability to reason about the technical problem
   degrades' — and its specialization signal [D01-S04]."* Either use the real sentence or drop "exact."

2. **§4.8** — currently: *"it loses when work fits one context or the chain is dependent, because
   'handoff and merge cost more than the plan.'"*
   The live source reads: *"the orchestrator pays for a plan, a handoff, and a merge that a single model
   gets for free."* Replace the quoted fragment with this text, or rephrase without quotation marks as
   the chapter's own paraphrase.

3. **§4.8** — currently: *"Governing bar: 'Multi-model configurations must beat the single model's full
   effort curve.'"*
   The live source reads: *"A multi-model configuration must beat the single model's whole curve."*
   Correct the quote to "whole curve" (singular "configuration," not plural) or remove the quotation
   marks.

4. **§4.8 / §11 (completeness, not a factual error)** — add one sentence naming Claude Fable 5.1's role
   ("for demanding reasoning and long-horizon agentic work, or when effort increases on Opus 5.5 still
   fall short") so the chapter states the full docs' recommendation method
   ("default → raise effort → only then change model"), not just the Opus 5.5 half of it. VF calls this
   "the model-selection method the course should teach."

5. **§11 Sources** — remove D01-S18 from the bibliography, or add one inline use of it (e.g., naming the
   Managed Agents "escalation" delegation pattern as a third sanctioned pattern alongside
   parallelization/specialization in §4.2/§4.6) so every listed source is load-bearing.

None of these require rewriting substantive architectural claims — all five are quote-precision or
completeness fixes.

---

## Answer-key audit

Independently re-solved all 12 items from the stems before comparing to the key.

| Item | Verdict | Reasoning |
|---|---|---|
| 1 | KEY-CORRECT | Nine known classes + next-day consumption + cost-stated goal uniquely selects batch + caching (B). A adds unneeded tool/agentic cost; C misapplies orchestrator-workers to an enumerable set (at most parallelization); D forfeits the batch discount for latency nobody needs. |
| 2 | KEY-CORRECT | "Analysts cannot predict which sources a question needs" is precisely Anthropic's stated orchestrator-workers condition. A and B require a fixed/known split the stem denies; D is a verification, not decomposition, mechanism. |
| 3 | KEY-CORRECT | A (20+ tools across domains) and C (context-protection example) are the two named justifications in D01-S04. D ("billing squad wants ownership") is organizational convenience, not one of the three legitimate justifications, and is the textbook org-chart anti-pattern (AP1) — correctly excluded, not arguable. B is a symptom without a diagnosed cause; E is irrelevant. |
| 4 | KEY-CORRECT | Enumerable one-page checklist → rules-based validator (B) is the correct fix per the draft's own §4.5/§3.11 framework. A/D lift general quality without fixing the broken gate; C compounds the self-praise failure mode. |
| 5 | KEY-CORRECT | Long-running process + crash losing all progress → durability/resumption (B), not capacity (A), restart (C, the anti-pattern being tested), or a latency workaround (D). |
| 6 | KEY-CORRECT | Dependent chain AND fits one context window are exactly the two stated failure conditions for the orchestrator strategy in the draft's own §4.8 (traced to live docs: "when the work is one dependent chain, or fits in a single context, the orchestrator pays for a plan, a handoff, and a merge that a single model gets for free"). C's "price the baseline first" is the documented discipline; A asserts the conclusion the source contradicts for this shape; B is good hygiene but doesn't fix a wrong strategy; D removes the only cost argument. |
| 7 | KEY-CORRECT | A 30-day date comparison against a published policy is deterministic; routing it through an LLM call is the "model-in-the-rule-table" anti-pattern (B). D is impossible — the steps are sequentially dependent (each needs the prior step's output), so "run in parallel" cannot work, which the rationale correctly notes. |
| 8 | KEY-CORRECT | A and D are directly confirmed by the SDK docs (context isolation; tool restriction as a least-privilege lever). B is false (subagents cannot message each other — confirmed against live docs). C is false — a non-fork subagent starts fresh; live docs confirm "the only content you pass from parent to subagent is the Agent tool's prompt string." E is false and directly contradicted by the draft's own 3–10× figure. No ambiguity. |
| 9 | KEY-CORRECT | Nobody waiting + 3-week deadline + cost-stated goal + sampling verification maps cleanly onto batch + offline eval (B). A forfeits the discount for interactivity not required; C multiplies tokens for redundant per-file fact-checking when sampling already provides the check; D is agentic complexity for a single summarization task. |
| 10 | KEY-CORRECT | "Clear, independently verifiable milestones... fully capturable in a progress file and version control" is precisely the condition the draft's own §3.5/§4.6 material (and the harness-design source) gives for favoring a reset over compaction. A explicitly favors compaction per source language ("extensive back-and-forth"); C argues against a reset (the artifact is the external state); D is irrelevant to the choice. |
| 11 | KEY-CORRECT | The sponsor explicitly names the transformation pillar ("categories of analysis they can't produce today," not "cheaper"). B correctly reframes the metric and architecture; A and C optimize cost/efficiency, which the stem explicitly deprioritizes; D doesn't expand capability. |
| 12 | KEY-CORRECT | A, B, C are each independently confirmed against primary sources (minimal context transfer, dominant failure mode, ROI-boundary rule). D ("always reduce total token consumption") is an absolute claim contradicted by the draft's own 3–10× token-multiplier finding — a verifier is additional agent spend, not savings. E is directly contradicted by "recipe for conflict" (D01-S20). Exactly 3 of 5 options are defensible, matching "select 3" with no ambiguity. |

**No KEY-WRONG or KEY-ARGUABLE items found.** All 12 keys are correct, are the single best (or complete
multi-select) answer, and every distractor rationale correctly explains the flaw. This is a genuinely
strong answer key — no item requires an inference beyond what the stem states.

---

## Attribution hygiene

| Location | What's dressed as sourced fact | Correct framing |
|---|---|---|
| §3.12, §4.8 ("Business value pillars") | Draft already correctly marks this `[UNVERIFIED]` as an Anthropic framework and explains the mapping is "a synthesis." **This is the right treatment — preserve it.** Independent search confirms no Anthropic material uses this phrase or list. | No change needed; this is exemplary attribution hygiene, not a violation. |
| §5, S5 scenario | "Anthropic's exact worked example" — the quoted sentence is a paraphrase of the source, not the source's actual sentence. | Correction #1 above: quote the real sentence or say "closely mirrors" instead of "exact." |
| §4.8, orchestrator failure quote | Quotation marks imply verbatim Anthropic wording; the phrase is the chapter authors' compression of the source's actual sentence. | Correction #2 above. |
| §4.8, "full effort curve" | Same issue — quotation marks around a near-paraphrase. | Correction #3 above. |
| §4.6, "Item 10" heuristic anchor ("iterative development with clear milestones") | Minor — this phrase from the dossier's M6 table is a light paraphrase of D01-S05's compaction-use condition; not directly quoted in the shipped draft body, so no fix needed there specifically, but worth the editor's attention if reused verbatim elsewhere. | No action required in this chapter; flagged for editor awareness only. |

Everywhere else checked (the ten-pattern taxonomy, the six governing "Building effective agents" quotes,
the harness/session/sandbox material, the context-engineering material, the tool-writing material, the
evals material, and the SDK subagent material) uses quotation marks only where the text is genuinely
verbatim. The chapter's discipline about not inventing "Anthropic recommends" attributions is otherwise
sound: every "Anthropic states/recommends/says" sentence checked traces to an actual sentence in the
named source.

---

## Volatility watchlist

| Claim | Why it may change | Re-check trigger |
|---|---|---|
| Claude Opus 5.5 as the docs' default recommendation; Fable 5.1 for demanding reasoning | Anthropic ships new model generations frequently (Opus 5.5 itself shipped 2026-09-22, days before this review) | Any new model announcement on anthropic.com/news or a new row in the models-overview comparison table |
| Tool-use system-prompt overhead (286/354/496 tokens) | Anthropic has changed this table with past model releases (the fetched table shows different values across Opus 4.5–4.8–5–5.5) | Re-fetch platform.claude.com/docs/en/agents-and-tools/tool-use/overview at each model-lineup change |
| Cache-read pricing percentages (10%/5%/2.5%) | Pricing structures are commercial terms that can change independent of model releases | Re-fetch the models-overview / pricing page before each cohort |
| "3–10×" and "~15×"/"~4×" multi-agent token multipliers | Both figures come from specific internal evals (research-system post, June 2025; multi-agent-systems post, undated but later) on specific workloads (research, BrowseComp) — not universal constants | Re-verify if either source post is revised, or before citing the numbers for a workload type (e.g. coding) the posts themselves say they don't generalize to |
| 90.2% multi-agent uplift figure | Explicitly an internal, single-eval result on Opus 4/Sonnet 4 — models now two generations legacy | Treat as a historical illustration of *why* the architecture can pay off, not a current performance guarantee; re-anchor to current-generation evals if this course is revised |
| Advisor/orchestrator cost figures (2.7–5.3× caching factor; 43% spend example) | Sourced from "Optimizing for cost and intelligence," which explicitly measures against a specific benchmark set (DeepResearch Bench II, WideSearch) that may be superseded | Re-fetch platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence if benchmark citations change |
| "Business value pillars" as blueprint-only | Depends on Anthropic *not yet* having published this framing; Anthropic's enterprise messaging evolves (e.g., the "Enterprise AI Transformation Guide" found during this review uses a different adoption/efficiency/quality/satisfaction framing) | Re-search "business value pillars" / the 5-item list against anthropic.com before each course revision — if Anthropic ever adopts this exact vocabulary, the `[UNVERIFIED]` flag should be lifted |
| Exam blueprint's ~10–11 item count for Domain 1 | Arithmetic on a published percentage, not a published count; Anthropic could rebalance weights in a future guide version | Re-check against the current exam guide version number before each course revision |

---

## Sources consulted

| ID | Title | URL | Publisher/Author | Type | Accessed | Trust | Used for |
|----|-------|-----|------------------|------|----------|-------|----------|
| D01-V01 | Building effective agents | https://www.anthropic.com/engineering/building-effective-agents | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | Full pattern-taxonomy verification (§3.1–3.4, 4.1, 4.3) |
| D01-V02 | How we built our multi-agent research system | https://www.anthropic.com/engineering/multi-agent-research-system | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | 90.2% uplift, 4×/15× token figures, 80% variance, 90% time-cut, ~20 test queries, rainbow deployments |
| D01-V03 | Building multi-agent systems: when and how to use them | https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | Anthropic / Claude blog | anthropic-blog | 2026-09-24 | primary | 3–10× token multiplier, three justifications, 20+ tools signal, telephone game, verification-subagent failure mode |
| D01-V04 | How and when to use subagents in Claude Code | https://claude.com/blog/subagents-in-claude-code | Anthropic / Claude blog | anthropic-blog | 2026-09-24 | primary | Delegation signal, no direct agent-to-agent messaging, parallel-file-edit conflict, specialist-agent proliferation |
| D01-V05 | Web search: "business value pillars" Anthropic Claude | (search) | — | other | 2026-09-24 | primary/negative-result | No Anthropic use of this phrase found |
| D01-V06 | Web search: efficiency/transformation/productivity/cost Anthropic enterprise | (search) | — | other | 2026-09-24 | primary/negative-result | No Anthropic 5-pillar framework found; surfaced the differently-framed "Enterprise AI Transformation Guide" (adoption/efficiency/quality/satisfaction) — noted in Volatility watchlist |
| D01-V07 | How AI is transforming work at Anthropic | https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic | Anthropic Research | anthropic-blog | 2026-09-24 | primary | 27% statistic, survey population/date |
| D01-V08 | Building trusted AI in the enterprise (PDF, read directly, 20 pages) | https://www-cdn.anthropic.com/e5c9de22bc8884089970bd262ca0c8b952cb9136.pdf | Anthropic | other | 2026-09-24 | primary | Pilot-selection criteria, revenue/cost-risk use-case split, success-criteria rubric, graduation criteria, staleness of model references |
| D01-V09 | Models overview; Batch processing; Streaming (via subagent + direct fetch) | https://platform.claude.com/docs/en/about-claude/models/overview ; https://platform.claude.com/docs/en/build-with-claude/batch-processing ; https://platform.claude.com/docs/en/build-with-claude/streaming | Anthropic (docs) | anthropic-docs | 2026-09-24 | primary | Model lineup/pricing cross-check against VERIFIED-FACTS.md, batch limits/discount, streaming behavior |
| D01-V10 | Tool use with Claude (overview) | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Anthropic (docs) | anthropic-docs | 2026-09-24 | primary | Tool-use system-prompt token overhead table |
| D01-V11 | Scaling Managed Agents: Decoupling the brain from the hands | https://www.anthropic.com/engineering/managed-agents | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | Session/harness/sandbox, TTFT p50/p95 improvement figures, wake/resume mechanics |
| D01-V12 | Harness design for long-running application development | https://www.anthropic.com/engineering/harness-design-long-running-apps | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | Self-evaluation bias, reset-vs-compaction tradeoff, stale-assumption principle, $9-vs-$200 example |
| D01-V13 | Building agents with the Claude Agent SDK | https://claude.com/blog/building-agents-with-the-claude-agent-sdk | Anthropic / Claude blog | anthropic-blog | 2026-09-24 | primary | Agent loop phrase, LLM-as-judge caveat, rules-based feedback quote |
| D01-V14 | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | Context-engineering definition, context rot / n² relationships, subagent summary length |
| D01-V15 | Writing effective tools for agents — with agents | https://www.anthropic.com/engineering/writing-tools-for-agents | Anthropic Engineering | anthropic-blog | 2026-09-24 | primary | Tool consolidation example, "more tools" quote, namespacing |
| D01-V16 | Optimizing for cost and intelligence | https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence | Anthropic (docs) | anthropic-docs | 2026-09-24 | primary | Cost-per-completed-task, price-the-tail example, advisor/orchestrator strategy wording, caching cost-reduction factor |
| D01-V17 | Choosing the right model | https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Anthropic (docs) | anthropic-docs | 2026-09-24 | primary | Effort-vs-model-switch guidance, efficiency-first/capability-first strategies, model selection matrix |
| D01-V18 | Subagents in the SDK | https://code.claude.com/docs/en/agent-sdk/subagents | Anthropic (Claude Code docs) | anthropic-docs | 2026-09-24 | primary | Four subagent benefits, context-inheritance rules, depth/concurrency/spend defaults |
| D01-V19 | Claude Certified Architect – Professional Exam Guide v1.0 | (local) `../claude-arch-professional-guide.md` | Anthropic | exam-guide | 2026-09-24 | primary | Exam mechanics cross-check (63 items, 17% weight, blueprint objectives, Section 8 style) |
| D01-V20 | VERIFIED-FACTS.md | (local) `../VERIFIED-FACTS.md` | Project orchestrator (Anthropic-sourced) | other | 2026-09-24 | primary | Canonical model lineup/pricing/effort cross-check |

Note on method: web verification for D01-V02–D01-V18 was performed via direct WebFetch of each live URL in
this session (several via a general-purpose subagent whose quoted output was independently spot-checked
against the same URLs by direct WebFetch where noted above), not via the researcher's dossier or source
table. The `claude-api` skill was also invoked and confirmed to still carry the stale Opus-5-as-current
table dated 2026-06-24 — consistent with VERIFIED-FACTS.md's own warning that the skill is stale; this is
not a draft error since the draft does not rely on the skill's cached model claim.
