# Domain 1 — Solution Design & Architecture

## 1. Front matter

**Domain 1 · Weight 17% · ~10–11 of 63 scored items** (arithmetic on the published weight; Anthropic
states weights are approximate) [D01-S01].

**Objectives (verbatim) [D01-S01]:** (1) Translate business problems into Claude-based AI solutions.
(2) Design end-to-end architectures (input → processing → output → feedback loops). (3) Select appropriate
architectural patterns (workflow, agentic, augmented LLM). (4) Design multi-agent systems and orchestration
strategies. (5) Apply decomposition techniques for complex problem solving. (6) Align solutions to business
value pillars (efficiency, transformation, productivity, cost, performance SLAs).

Objective 3 names the three tiers explicitly — *workflow, agentic, augmented LLM* — the taxonomy of
Anthropic's "Building effective agents" [D01-S02]. That article's vocabulary is the spine of this domain.

---

## 2. Exam-relevance framing

This domain does not test whether you can define "orchestrator-workers." It tests whether, given four
defensible-looking options, you identify **the simplest architecture that satisfies the binding
constraint** — usually an error-cost ceiling, a latency budget, an auditability requirement, a context
limit, or a named business metric. The governing sentence is Anthropic's: *"finding the simplest solution
possible, and only increasing complexity when needed. This might mean not building agentic systems at
all."* [D01-S02] Every archetype below violates it.

| # | Distractor archetype | How it looks right | The tell |
|---|---|---|---|
| A1 | **Complexity escalation** | Adds agents/tools/models because the problem "sounds hard" | The stem says the decision tree *is* enumerable. Predictable work takes a workflow [D01-S02]. |
| A2 | **Pattern name-drop** | A real pattern applied to the wrong signal | Orchestrator-workers requires that subtasks *cannot* be predicted; if the stem lists them, it is parallelization [D01-S02]. |
| A3 | **Loop in the wrong place** | In-loop self-critique where offline eval or human review belongs | Self-evaluation "confidently prais[es] the work" [D01-S08]. |
| A4 | **SLA blindness** | Right on accuracy/cost, silently breaks a stated p95 or retention window | Reread the stem for a number with a unit. |
| A5 | **Model-everywhere** | Uses Claude for a lookup, a calculation, or a published rule table | If a rule can express "correct," code it [D01-S06]. |
| A6 | **Value-pillar mismatch** | Real improvement against a metric nobody asked for | The stem names the pillar. Optimize *that*. |

---

## 3. Core concepts

Format: **definition → the decision it drives → common misconception.** Alternatives are named in brackets.

**3.1 Augmented LLM** — an LLM enhanced with retrieval, tools, and memory, generating its own queries and
selecting its own tools [D01-S02]. *Drives:* whether you need any orchestration at all; one well-specified
transform over unstructured input (classify, extract, summarize, rewrite) is one call. *Misconception:*
that it means "basic" — retrieval + tools + a constrained output format is a complete production
architecture. [Alt: workflow, agent]

**3.2 Workflow vs. agent** — a workflow orchestrates "through predefined code paths"; an agent is a system
where LLMs "dynamically direct their own processes and tool usage" [D01-S02]. *Drives:* everything —
predictability, auditability, cost variance, and blast radius all follow from *who decides what happens
next*. Anthropic's discriminator: "workflows offer predictability and consistency for well-defined tasks,
whereas agents are the better option when flexibility and model-driven decision-making are needed at
scale" [D01-S02]. *Misconception:* that tool use makes something an agent. A workflow calls tools too;
agency is about who chooses the next step. [Alt: augmented LLM]

**3.3 The five workflow patterns** [D01-S02] — all are workflows; your code owns control flow.
*Prompt chaining:* fixed sequence, each call processes the previous output, optional programmatic gates;
"trade off latency for higher accuracy." *Routing:* classify, then dispatch to a specialized handler;
requires that "classification can be handled accurately." *Parallelization/sectioning:* known independent
subtasks run concurrently. *Parallelization/voting:* the same task run several times for confidence.
*Orchestrator-workers:* a central LLM decomposes, delegates, synthesizes — defining property: "subtasks
aren't pre-defined, but determined by the orchestrator based on the specific input."
*Evaluator-optimizer:* generator plus critic in a loop, for when there are "clear evaluation criteria" and
"iterative refinement provides measurable value." *Misconception:* that orchestrator-workers and
parallelization are interchangeable. They differ on one axis: can you enumerate the subtasks before the
input arrives?

**3.4 The agent loop and ground truth** — "gather context → take action → verify work → repeat" [D01-S06];
the agent must "gain 'ground truth' from the environment at each step (such as tool call results or code
execution) to assess its progress" [D01-S02]. *Drives:* whether the agentic tier is available at all. No
cheap objective signal in the environment (tests, compiler, schema, a query returning rows) → no agent.
*Misconception:* that stopping conditions are optional; Anthropic recommends "stopping conditions (such as
a maximum number of iterations)" [D01-S02].

**3.5 Harness** — the loop that calls Claude, routes tool calls, and manages context across one or many
context windows. Anthropic virtualizes it as **session** (append-only event log), **harness** (the loop),
**sandbox** (execution environment) [D01-S09]. *Drives:* where durability lives. Because the session
"lives outside Claude's context window," a crashed harness resumes "from the last event" rather than
restarting [D01-S09]. *Misconception:* that harness complexity is a permanent asset. "Every component in a
harness encodes an assumption about what the model can't do on its own, and those assumptions are worth
stress testing" [D01-S08] — Anthropic *removed* sprint decomposition after a model upgrade.

**3.6 Context rot / attention budget** — "as the number of tokens in the context window increases, the
model's ability to accurately recall information from that context decreases," a consequence of the
transformer's n² pairwise relationships, producing "a performance gradient rather than a hard cliff"
[D01-S05]. *Drives:* just-in-time retrieval (lightweight identifiers, load on demand) vs. pre-inference
retrieval; "The decision boundary for the 'right' level of autonomy depends on the task" [D01-S05].
*Misconception:* that a 1M-token window removes the need to decompose. It moves the threshold, not the
gradient.

**3.7 Context isolation (subagents)** — "intermediate tool calls and results stay inside the subagent; only
its final message returns to the parent" [D01-S19], typically a 1,000–2,000 token summary [D01-S05].
*Drives:* whether to decompose by context boundary, and what goes in the handoff prompt — "the only
content you pass from parent to subagent is the Agent tool's prompt string" [D01-S19]. It also buys least
privilege: a reviewer subagent can hold read-only tools [D01-S19]. *Misconception:* that subagents talk to
each other. They cannot [D01-S20], which is why dependent chains are a poor fit.

**3.8 Four decomposition techniques** — **task** (work into ordered steps inside one context; ~zero
coordination cost); **prompt chaining** (steps into separate calls with gates; serial latency);
**context** (information across isolated windows; handoff and summary loss); **tool** (the action surface
into named typed capabilities; schema tokens are a permanent context cost). *Drives:* which axis you cut
along — cutting the wrong axis is the most common error in this domain. *Misconception:* that these are
one technique at different scales. You can decompose tasks without decomposing context, and context
without adding agents.

**3.9 Context-centric decomposition** — "adopt a context-centric view rather than a problem-centric view
when decomposing work"; "An agent handling a feature should also handle its tests, because it already
possesses the necessary context" [D01-S04]. *Drives:* where the cut lines go in any multi-agent design.
Problem-centric splits produce the **telephone game** — "passing information back and forth with each
handoff degrading fidelity," to the point that "the subagents spent more tokens on coordination than on
actual work" [D01-S04]. *Misconception:* that mirroring the org chart (QA agent, security agent, docs
agent) is good design. It is the canonical problem-centric split.

**3.10 Execution mode** — synchronous; **streaming** (SSE, incremental delivery of the same request)
[D01-S16]; asynchronous/queued (your queue, your callback); and the **Message Batches API** — Anthropic-side
async at **50% of standard prices**, "most batches finishing in less than 1 hour," results at completion
or 24 hours (whichever first), batches expiring at 24 hours [D01-S15]. *Drives:* whether a latency
requirement is real; if nobody is waiting, batch halves the bill. *Misconception:* that streaming makes a
request faster. It changes time-to-first-token and perceived latency; total generation time is unchanged.
(It is separately *required* for very large `max_tokens`, which otherwise hit HTTP timeouts [D01-S16].)

**3.11 Feedback-loop placements** — inline rules-based verification; inline self-critique; a separate
evaluator agent; an offline eval suite; production telemetry with human review. *Drives:* latency cost,
what the loop can catch, and whether users are affected before you know. *Misconception:* that in-loop
self-critique substitutes for evaluation. "Separating the agent doing the work from the agent judging it
proves to be a strong lever," because self-evaluating models "respond by confidently praising the
work—even when, to a human observer, the quality is obviously mediocre" [D01-S08].

**3.12 Business value pillars** — the blueprint names efficiency, transformation, productivity, cost,
performance SLAs [D01-S01]. `[UNVERIFIED]` as an official Anthropic framework: no Anthropic publication
uses that phrase or that list. Anthropic's own enterprise framing splits use cases into "External,
revenue-oriented" and "Internal, cost- and risk-oriented" [D01-S21], and separates efficiency from
transformation — internally, "27% of Claude-assisted work wouldn't have been done otherwise" [D01-S22].
*Drives:* the metric, and therefore the architecture (§4.8). *Misconception:* that cost and efficiency are
one pillar. Efficiency is throughput per unit of human effort; cost is spend per completed unit. A design
can improve one and worsen the other.

---

## 4. Trade-off analyses

### 4.1 Augmented LLM vs. workflow vs. agentic loop

| Axis | Augmented LLM | Workflow | Agentic loop |
|---|---|---|---|
| Who chooses the next step | Nobody (one step) | Your code | The model |
| Predictability required | Fully specified | Decision tree enumerable in advance | Path unknowable in advance |
| Step count | 1 | Fixed / bounded | Unbounded; needs a stop condition [D01-S02] |
| Auditability | Trivial | High — every branch is reviewable code | Lower; "non-deterministic between runs, even with identical prompts" [D01-S03] |
| Latency | Lowest, predictable | Predictable (sum for chains, max for parallel) | High variance, unbounded tail |
| Error-cost tolerance | Any | Any | Errors must be **recoverable** (tests, review, rollback) [D01-S24] |
| Relative cost | 1× | ~steps × 1× | ~4× a chat interaction [D01-S03] |
| Dominant failure | Complexity ceiling | Falls off the enumerated path | Compounding errors, loops, runaway spend |

**Choose augmented LLM** when the unit of work is one transform and the output format can be constrained.
**Choose workflow** when you can draw the decision tree before seeing the input, or when determinism is a
requirement rather than a preference. **Choose agentic** when step count and path are unpredictable, the
environment yields cheap ground truth each step, and errors are recoverable. The gate before building an
agent [D01-S24]: Complexity, Value, Viability, **Cost of error** — "If the answer is 'no' to any of these,
stay at a simpler tier."

### 4.2 Single agent with more tools vs. multi-agent decomposition

| Axis | Single agent, broader tool set | Multi-agent decomposition |
|---|---|---|
| Token cost | 1× | **3–10× single-agent** [D01-S04]; research systems ~15× a chat interaction [D01-S03] |
| Wall clock | Serial | Faster *only* when subtasks are genuinely independent; otherwise slower overall [D01-S04] |
| Context quality | One window; pollution accumulates | Isolated windows; ~1–2k token summaries return [D01-S05][D01-S19] |
| Tool selection | Degrades past ~20 tools or across unrelated domains [D01-S04] | Each agent sees a focused surface |
| Operational surface | One prompt, one loop | "another potential point of failure, another set of prompts to maintain" [D01-S04] |
| Coordination | None | Telephone game; no agent-to-agent channel [D01-S04][D01-S20] |
| Security | One privilege set | Per-agent tool restriction = least privilege [D01-S19] |
| Governance | One budget | Depth (default 3), concurrency (default 20) and spend caps must be set explicitly [D01-S19] |

**Choose multi-agent only on a demonstrated constraint** [D01-S04]: **context protection** (order history
polluting a technical diagnosis is Anthropic's own example), **parallelization** (independent exploration
of a larger search space), or **specialization** (20+ tools, unrelated domains, or new tools degrading
existing tasks). **Choose single agent** for dependent chains, frequent synchronization, or work that fits
one context. Anthropic: "Most coding tasks involve fewer truly parallelizable tasks than research, and LLM
agents are not yet great at coordinating and delegating to other agents in real time" [D01-S03].
Delegation signal within one agent: "exploring ten or more files, or… three or more independent pieces of
work" [D01-S20]. Calibrate the upside honestly — the measured **+90.2%** multi-agent uplift [D01-S03] came
from open-ended research with heavy parallelism and information exceeding one context window, precisely
the justified case; it does not generalize to coding, triage, or pipelines.

### 4.3 Pattern selection: chaining vs. routing vs. parallelization vs. orchestrator-workers vs. evaluator-optimizer

| Pattern | Buys | Costs | Choose when | Reject when |
|---|---|---|---|---|
| Prompt chaining | Accuracy via smaller checkable steps + gates | Serial latency = sum of steps | "the task can be easily and cleanly decomposed into fixed subtasks" [D01-S02] | Steps can't be checked individually |
| Routing | Specialized handling per class; cheap model per class | One hop; misroute risk | "distinct categories that are better handled separately, and where classification can be handled accurately" [D01-S02] | Classes overlap, or misroutes are expensive and undetectable |
| Parallelization (sectioning) | Sum of latencies becomes max of latencies | N× tokens for 1× elapsed | Subtasks known in advance and independent | Subtasks share state |
| Parallelization (voting) | Confidence via diverse attempts | N× tokens; needs an aggregation rule | "multiple perspectives or attempts are needed for higher confidence results" [D01-S02] | You can't reconcile disagreement |
| Orchestrator-workers | Handles inputs whose decomposition is unknown until arrival | Coordination tokens; non-determinism; synchronous bottleneck [D01-S03] | "complex tasks where you can't predict the subtasks needed" [D01-S02] | You can list the subtasks in the design doc |
| Evaluator-optimizer | Measurable iterative improvement against explicit criteria | Unbounded loop risk; two models' cost | "clear evaluation criteria" **and** "iterative refinement provides measurable value" [D01-S02] | You can't articulate criteria, or a rules check would do it |

**One-line discriminators.** Chaining vs. parallelization: *do the steps depend on each other?*
Parallelization vs. orchestrator-workers: *can you enumerate the subtasks before seeing the input?*
Routing vs. orchestrator-workers: *is the decision a classification into known buckets, or a plan?*
Evaluator-optimizer vs. offline eval: *must the improvement happen inside this request?*

### 4.4 Synchronous vs. streaming vs. async/queued vs. batch

| Mode | Latency class | Cost | Hard constraints | Choose when |
|---|---|---|---|---|
| Synchronous | Full generation before response | List | Long generations hit HTTP timeouts | Short interactive calls, modest `max_tokens` |
| Streaming (SSE) | TTFT in ms; total unchanged | List | Required for very large `max_tokens` [D01-S16] | A human watches the output render |
| Async / queued (yours) | Seconds–minutes, you control | List | You own queue, retry, idempotency, callback | Long agentic runs; webhook integrations; surviving client disconnect |
| **Message Batches** | "most batches finishing in less than 1 hour"; results at completion or 24 h, whichever first; expire at 24 h | **50% of standard** | 100,000 requests or 256 MB per batch; results arrive in **any order** — key by `custom_id` | Bulk classification, backfills, eval runs, nightly enrichment [D01-S15] |

**Choose batch** whenever no human is blocked and a 24-hour ceiling is tolerable — it is a named "free
win" [D01-S12]. **Choose streaming** when the pillar is *productivity* (perceived responsiveness) rather
than *efficiency* (throughput); Anthropic treats TTFT as the latency users "most acutely *feel*," and cut
p50 TTFT ~60% and p95 >90% purely by not provisioning a sandbox until a tool call needed one [D01-S09].
**Reject batch** on any per-request SLA: the 24-hour expiry is an unacceptable tail even if "most" batches
finish in under an hour.

### 4.5 Where to put the feedback loop

| Placement | Runtime latency | Catches | Blind to | Choose when |
|---|---|---|---|---|
| Inline rules-based (tests, lint, schema, policy engine) | ms | Anything a rule can express | Semantic quality | A rule can express "correct": "the best form of feedback is providing clearly defined rules for an output, then explaining which rules failed and why" [D01-S06] |
| Inline self-critique (same context) | One call | Obvious slips | Its own blind spots [D01-S08] | Cheap safety net only — never the primary gate |
| Separate evaluator agent | One agent; low context transfer | Quality against an articulated rubric | Whatever the rubric omits; may rubber-stamp [D01-S04] | "when the task sits beyond what the current model does reliably solo" [D01-S08] |
| Offline eval suite | None | Regressions; model-swap and prompt-change risk | Novel production distributions | Pre-launch and CI/CD [D01-S10] |
| Production telemetry + human review | None | Distribution drift; real failure modes; grader miscalibration | Only *after* users are affected [D01-S10] | Always, alongside offline — the two are "complementary, not competing" [D01-S10] |

**Grade outcomes, not trajectories:** "grade what the agent produced, not the path it took," since
path-grading yields "overly brittle tests, as agents regularly find valid approaches"; for a booking agent
the outcome "is whether a reservation exists in the environment's SQL database" [D01-S10].
**Reliability metric:** use **pass^k** (all k trials succeed), not pass@k, for "customer-facing agents where
users expect reliable behavior every time" [D01-S10] — 90% right once is 59% right five times running.
**LLM-as-judge** is weak as an in-loop runtime gate — "generally not a very robust method, and can have
heavy latency tradeoffs" [D01-S06] — and acceptable offline with human calibration [D01-S10].

### 4.6 How far to decompose before coordination overhead dominates

| Signal | Decompose further | Stop |
|---|---|---|
| Token ratio | Work tokens dominate | "The subagents spent more tokens on coordination than on actual work" [D01-S04] |
| Dependency structure | Pieces independent | Sequential dependent work; "frequent synchronization" [D01-S04][D01-S20] |
| Handoff artifact | Artifact carries the state cleanly | It cannot — a reset would lose the thread [D01-S08] |
| Shared write surface | Disjoint outputs | "Two subagents editing the same file in parallel is a recipe for conflict" [D01-S20] |
| Model capability | Model loses coherence at this span | Model sustains it solo — sprint decomposition was *removed* when it stopped helping [D01-S08] |
| Delegation surface | Few clearly-described specialists | "Too many specialist agents" makes delegation unreliable [D01-S20] |

**Anthropic's calibration anchor, embedded in a production orchestrator prompt** [D01-S03]: "Simple
fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with
10-15 calls each, and complex research might use more than 10 subagents." The split scales with the
question, not with ambition. Delegation quality is part of the architecture: each subagent needs "an
objective, an output format, guidance on the tools and sources to use, and clear task boundaries" — vague
instructions caused duplicated work [D01-S03].

### 4.7 Tool decomposition: bash vs. dedicated tools vs. consolidated workflow tools

| Option | Buys | Costs | Choose when |
|---|---|---|---|
| Bash / general execution | Maximum breadth, one schema | Harness sees only an opaque string — cannot gate, render, or parallelize safely | Exploratory breadth, low-risk environments [D01-S25] |
| Dedicated typed tool | An action-specific hook to intercept, gate, render, audit, or mark parallel-safe | Permanent schema tokens | You must **gate, render, audit, or parallelize** — especially hard-to-reverse actions [D01-S25] |
| Consolidated workflow tool | Fewer decision points, fewer round trips | Less compositional flexibility | The workflow is stable: `schedule_event` over `list_users` + `list_events` + `create_event` [D01-S11] |
| Programmatic tool calling | Intermediate results return to a running script, not context — "Token cost scales with final output, not intermediate results" | Needs a code-execution environment | Many sequential calls or large intermediate payloads [D01-S25] |

**Sanity test:** "If a human engineer can't definitively say which tool should be used in a given
situation, an AI agent can't be expected to do better" [D01-S05]. And: "More tools don't always lead to
better outcomes. A common error we've observed is tools that merely wrap existing software functionality
or API endpoints" [D01-S11]. Schemas are not free — the tool-use system prompt alone costs 286 tokens on
Claude Opus 5.5, 354 on Sonnet 5, 496 on Haiku 4.5, before your definitions [D01-S17, accessed 2026-09-24].

### 4.8 Business problem → value pillar → architecture → SLA

| Pillar | Sponsor is buying | Metric shape [D01-S21] | Architecture it selects |
|---|---|---|---|
| **Efficiency** | Same work, less handling per unit | ↓ time to resolution, ↓ queue time, ↑ volume handled | Workflow/routing over agentic; caching; batch; smaller model at lower effort |
| **Transformation** | Work that would not otherwise happen | New artifact classes; newly feasible analyses — "27% of Claude-assisted work wouldn't have been done otherwise" [D01-S22] | Justifies agentic/multi-agent spend; measured by volume of newly feasible work, not unit cost |
| **Productivity** | More output per person, human in the loop | ↑ first-contact resolution, ↑ developer throughput, ↑ CSAT | Assistive UX, streaming, low TTFT, approval gates |
| **Cost** | Lower unit economics | ↓ cost per ticket / conversation / review | Batch, caching, effort down, model down — measured as **cost per completed task** [D01-S12] |
| **Performance SLA** | A bounded contractual characteristic | p95 latency, availability, throughput, accuracy floor | Constrains the tier *before* anything else; a hard p95 eliminates unbounded loops |

**Cost rules that decide items** [D01-S12]: "You pay for completed tasks… compare models on cost per
completed task" — a cheaper request needing three retries is not cheaper. "Price the tail of your
workload, not the median" (reported: two of twenty problems "carried 43% of the spend"). Order of levers:
**free wins first** — caching, token hygiene, batch, spend limits — *then* trade-offs (model, effort,
output caps, multi-model); caching alone "cut agent-loop cost by a factor of 2.7 to 5.3."

**Multi-model orchestration** [D01-S12]: the **advisor** (cheap executor escalates hard decisions) pays
only when the executor actually consults — "An executor at low effort can stop detecting that it is
stuck," and the pairing can then score below the executor alone. The **orchestrator** (frontier model
delegates bulk work) pays when work exceeds one context window with massive parallelism, or as insurance
against a cost tail; it loses when work fits one context or the chain is dependent, because "handoff and
merge cost more than the plan." Governing bar: **"Multi-model configurations must beat the single model's
full effort curve."**

**When the answer is "don't use an LLM for this step."** Lookups, arithmetic, schema validation,
deterministic transforms, entitlement checks, and decisions with a published rule table belong in code.
Anthropic points the same way: prefer code-based graders "when fast, cheap, and objective verification is
possible" [D01-S10]. Reserve the model for the unstructured boundary — read the document, classify the
intent, draft the language, explain the decision.

---

## 5. Worked scenarios

**S1 · Financial services — commercial loan document intake.** Twelve document types, each with a known
extraction schema; values reconcile against core banking; every decision reconstructible for seven-year
regulatory exam; processed overnight. **Recommended:** routing by document type → per-type extraction
chain → deterministic reconciliation in code → exception queue, submitted via Message Batches.
**Alternatives lose:** a single agent makes a fully enumerable decision tree non-deterministic between runs
[D01-S03] (A1); orchestrator-workers is wrong because the subtasks are known before the input arrives
[D01-S02] (A2); an evaluator-optimizer over reconciliation is worse than arithmetic against a system of
record [D01-S06] (A5). **What changes it:** unbounded, unknown document types → orchestrator-workers
becomes defensible; a two-minute per-package SLA → batch is out, synchronous sectioning is in.

**S2 · Healthcare — prior authorization triage.** Criteria published in a medical policy; denials must be
issued by a licensed reviewer; p95 under 30 seconds on a clinician portal. **Recommended:** augmented LLM
extracts structured clinical facts → deterministic rules engine evaluates policy → approvals auto-issue;
denials and ambiguous cases route to a human with a drafted rationale. **Alternatives lose:** an agent
issuing decisions puts a regulated determination in a non-deterministic loop and breaks
delegation-of-authority (A1, A5); an evaluator-optimizer adds cost and latency without moving decision
authority; batch's 24-hour ceiling violates the p95 [D01-S15] (A4). **What changes it:** if the policy were
genuinely narrative and not reducible to rules, the rules engine collapses and every output goes to human
review with the model downgraded to drafting.

**S3 · Retail — catalog enrichment across 4M SKUs.** Monthly refresh, no user waiting, unit cost is the
stated metric, 95% attribute accuracy on a held-out sample. **Recommended:** Message Batches with a cheaper
model, prompt caching on the shared taxonomy prefix, and an offline eval gate before publish.
**Alternatives lose:** synchronous high-concurrency forfeits the 50% discount for latency nobody consumes
[D01-S15] (A6); orchestrator-workers adds coordination tokens for a split already known [D01-S02]; an
agentic per-SKU research loop pays ~4× chat token cost [D01-S03] for an accuracy bar that does not require
it. **What changes it:** if ~30% of SKUs lacked source data, a routing step splits the traffic and only the
research branch pays agent economics.

**S4 · Government — benefits eligibility intake.** Eligibility defined in statute and encoded in an
existing rules service; caseworkers hold decision authority; applicants wait in the portal; appeals
require explainability. **Recommended:** streaming augmented LLM normalizes the narrative into the
structured schema → the existing rules service computes eligibility → the model drafts a plain-language
explanation of the service's output. The model brackets the deterministic core and never computes
eligibility. **Alternatives lose:** any option letting a model participate in a statutory determination
(A5) — the appeals record would have to explain a non-deterministic step; an intake/eligibility/explanation
three-agent split is the canonical problem-centric decomposition [D01-S04] with no context boundary being
protected (A1). **What changes it:** nothing about model quality — only a change in who holds decision
authority.

**S5 · SaaS/telecom — a support agent that grew to 26 tools.** Billing, network diagnostics, order history,
account admin; users report it "forgets" the technical problem mid-conversation and mis-selects tools;
streaming UX with a p95 first-token under 2 seconds. **Recommended:** split into a coordinator with domain
subagents scoped by **context boundary**, each holding a focused tool set and isolated context.
**Alternatives lose:** a stronger model still reads the same polluted context and faces the same 26-tool
selection problem [D01-S04]; better tool descriptions help at the margin [D01-S03] but do not fix context
accumulation; an evaluator agent adds a synchronous hop to a 2-second TTFT budget (A4). This stem contains
Anthropic's exact worked example — "Order details add thousands of tokens that degrade reasoning about the
technical problem" — and its exact specialization signal [D01-S04]. **What changes it:** at 8 tools with
only occasional mis-selection, tool consolidation [D01-S11] is correct and multi-agent is
over-engineering at 3–10× the tokens.

**S6 · Life sciences — competitive and regulatory intelligence.** Briefs synthesizing filings, trial
registries, publications, and press across an unpredictable source set; source attribution mandatory; the
sponsor wants analyses the team "currently cannot do at all." **Recommended:** orchestrator-workers — a
lead agent plans, spawns subagents per facet with explicit objective / output format / tool guidance /
task boundaries, synthesizes, then a citation pass attributes claims. **Alternatives lose:** RAG plus one
call cannot cover sources unknowable in advance with a corpus exceeding one window [D01-S04][D01-S12]; a
fixed chain cannot fix stages that depend on the question [D01-S02]; one long-running agent makes a single
context window the ceiling, and parallel subagents with separate windows are what buys the compression
[D01-S03]. **Pillar note:** the sponsor named **transformation**, which is what justifies 3–10× token cost
[D01-S04] and sets the metric to newly feasible brief volume. **What changes it:** a fixed set of ten known
registries with a stable question template collapses this to parallel sectioning — far cheaper, same
output.

**S7 · Legal — contract redlining against a playbook.** A written negotiation playbook with explicit
fallback positions; single-pass drafts are "directionally right but miss fallbacks"; an attorney reviews
every output; 10-minute turnaround is fine. **Recommended:** evaluator-optimizer — generator drafts
redlines, a **separate** evaluator scores clause-by-clause against the playbook and returns specific
failures, with a hard iteration cap. **Alternatives lose:** a better single-pass prompt does not address
incompleteness against articulated criteria, which is Anthropic's stated condition for
evaluator-optimizer [D01-S02]; an agentic loop has no environmental ground truth — there is no compiler
for a contract [D01-S02]; a per-section multi-agent split fractures shared definitional context into the
telephone game [D01-S04]. The critic must be a separate call: self-evaluation "confidently prais[es] the
work" [D01-S08]. **What changes it:** no written playbook → no criteria to score against → single-pass
drafting plus attorney review.

**S8 · Logistics — real-time exception triage.** ~40,000 exceptions/day; operators need a recommended
action within 3 seconds; 80% fall into six known categories with standard playbooks; 20% are novel; wrong
recommendations are visible and reversible. **Recommended:** routing — a fast classifier sends the 80% to
deterministic playbook lookup (no model call for the action) and the 20% to a bounded agentic
investigation with a step cap, streamed. **Alternatives lose:** one agentic loop for everything puts an
unbounded loop on a hard 3-second p95 (A4) and pays agent economics for a table lookup (A5); batch's
24-hour ceiling is disqualifying [D01-S15]; orchestrator-workers adds coordination to a latency-critical
single decision. **Pillar note:** two pillars, two tiers, one system — **efficiency** for the 80%,
**transformation/productivity** for the 20%. Merging them into one tier is what breaks the SLA.
**What changes it:** if the bounded branch still misses 3 seconds, degrade gracefully — return the
classification immediately and stream the investigation.

---

## 6. Failure modes & diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| Quality degrades as the conversation lengthens; early facts "forgotten" | Context rot [D01-S05] | Token count at failure vs. success; share of transcript that is stale tool results | Context editing, then compaction or a context reset with a handoff artifact [D01-S25][D01-S08] |
| Multi-agent costs 5× projection with no quality gain | Coordination exceeding work; problem-centric split | Coordination-to-work token ratio; whether cuts follow context boundaries [D01-S04] | Re-cut along context boundaries; collapse dependent chains into one agent |
| Subagents duplicate each other's work | Vague delegation instructions | Does each subagent prompt carry objective, output format, tool guidance, task boundaries? [D01-S03] | Rewrite delegation prompts with all four; add scaling rules |
| Far too many subagents for trivial queries | No embedded scaling heuristic; no caps | Depth/concurrency/spend caps; scaling rule in the orchestrator prompt [D01-S03][D01-S19] | Set caps; embed "1 agent for fact-finding, 2–4 for comparisons" |
| Agent declares success on incomplete work | Premature completion; no external completion criterion | Does a machine-checkable done-list exist outside the model's context? [D01-S07] | Externalize completion state (explicit `passing: false` list); verify against the environment, not the transcript |
| Evaluator passes everything | Verification subagent rubber-stamping — its "most significant failure mode" [D01-S04] | Did the evaluator exercise the artifact or only read about it? | Give it real interaction (run the tests, click the app) and concrete grading criteria [D01-S08] |
| Self-critique never finds problems | Self-evaluation in the same context [D01-S08] | Does the critic share the generator's context? | Move the critic to a separate call with only the artifact and the rubric |
| p95 latency blows up while p50 is fine | Unbounded loop on the tail — where the spend also lives [D01-S12] | Step-count distribution, not the mean | Iteration caps and task budgets; route tail cases to an async path |
| Cost per token fell but the bill rose | More retries/turns per completed task | Cost per *completed task* [D01-S12] | Restore effort or upgrade the model; re-measure on completed tasks |
| Cache hit rate near zero in an agent loop | Volatile content before the cacheable prefix; tools or model changed mid-session | `usage.cache_read_input_tokens` across repeated requests [D01-S24] | Freeze the prefix; append rather than swap tools; keep the loop on one model [D01-S25] |
| Long run dies and restarts from zero | State lives in the transcript | Is there an append-only session log or artifact outside the context window? [D01-S09] | Persist progress artifacts; design for resumption, not restart [D01-S03][D01-S09] |
| Passes eval, fails in production | Offline suite drifted from real traffic | Production distribution vs. eval set composition [D01-S10] | Add production monitoring alongside offline evals; refresh from real failures |
| Agent finds valid solutions but eval marks them wrong | Trajectory grading instead of outcome grading [D01-S10] | Does the grader inspect the final environment state or the path? | Grade the end state; add partial credit for multi-component tasks |

---

## 7. Anti-patterns

**AP1 · The org-chart multi-agent.** Mirroring team structure into agents (QA agent, security agent, docs
agent). *Looks right:* maps cleanly to how humans divide work and is easy to explain upward. *Fails:*
canonical problem-centric split → telephone game; "the subagents spent more tokens on coordination than on
actual work" [D01-S04]. *Instead:* cut along context boundaries.

**AP2 · Agentic by default.** Reaching for an agent because the domain sounds complex. *Looks right:*
agents are the most capable tier and feel future-proof. *Fails:* trades predictability, auditability, and
bounded latency for flexibility the problem did not need, at ~4× chat token cost [D01-S03]. *Instead:* run
the four-criterion gate [D01-S24]; if you can draw the decision tree, build a workflow.

**AP3 · Orchestrator for a known decomposition.** *Looks right:* the most sophisticated pattern in the
catalog. *Fails:* the pattern's defining property is that "subtasks aren't pre-defined" [D01-S02]; when
they are, you buy planning tokens and non-determinism for a split you could hardcode. *Instead:* parallel
sectioning.

**AP4 · The self-grading agent.** An in-loop "review your own answer" step treated as the quality gate.
*Looks right:* one extra call, confident-sounding review text. *Fails:* self-evaluation praises the work
[D01-S08], so the gate is decorative. *Instead:* rules-based inline checks plus a separate evaluator or
human gate.

**AP5 · Tool-per-endpoint.** *Looks right:* a mechanical, complete mapping of the backend. *Fails:* "tools
that merely wrap existing software functionality or API endpoints" is a named common error [D01-S11], and
selection quality degrades past ~20 tools [D01-S04]. *Instead:* consolidate to workflow-shaped tools.

**AP6 · Context maximalism.** Loading everything into a 1M-token window because it fits. *Looks right:* the
model "has all the information." *Fails:* context rot means recall degrades as the window fills [D01-S05] —
you paid for tokens that made the answer worse. *Instead:* just-in-time retrieval or context decomposition.

**AP7 · Permanent scaffolding.** Keeping harness components a newer model no longer needs. *Looks right:*
battle-tested; removing it feels risky. *Fails:* each component "encodes an assumption about what the model
can't do on its own," and assumptions go stale [D01-S08][D01-S09]. *Instead:* re-test at each model
upgrade and delete what no longer earns its place.

**AP8 · Model-in-the-rule-table.** Asking the model to apply a published deterministic rule set. *Looks
right:* the model can read the policy, so why maintain a second implementation? *Fails:* makes a
deterministic decision non-deterministic and unauditable, and is strictly worse than an engine that names
the failed rule [D01-S06]. *Instead:* model extracts, code decides, model explains.

---

## 8. Exam-day heuristics

1. **Find the binding constraint first** — a number with a unit, or a legal/authority statement. It
   eliminates options before pattern reasoning starts.
2. **Simplest tier that satisfies the constraint wins** [D01-S02]. When two options both work, take the
   less complex one.
3. **"Can you enumerate the subtasks before seeing the input?"** Yes → parallelization or routing (code
   owns the split). No → orchestrator-workers or an agent (the model owns it).
4. **"Who decides what happens next?"** Your code → workflow. The model → agent. Tool use alone is not
   agency.
5. **Multi-agent needs a named constraint** — context protection, parallelization, or specialization
   [D01-S04]. Absent one, it is the distractor, at 3–10× tokens.
6. **Decompose by context boundary, not job title** [D01-S04].
7. **If a rule can express "correct," use the rule** [D01-S06][D01-S10].
8. **Self-critique is not a gate** — separate the generator from the judge [D01-S08].
9. **Grade outcomes, not trajectories**; for customer-facing reliability think pass^k, not pass@k
   [D01-S10].
10. **Nobody waiting → batch.** 50% off, most under an hour, 24-hour ceiling [D01-S15].
11. **Streaming buys perceived latency, not throughput.** If the problem is total processing time,
    streaming is the wrong lever.
12. **Cost is per completed task, and the tail is where it lives** [D01-S12].
13. **A more capable model is not a fix for a context or authorization problem** — compare the guide's own
    Domain 3 sample, where a larger model is the wrong answer to an authorization-scope question [D01-S01].
14. **Free wins before trade-offs** — caching, token hygiene, batch, spend limits before model downgrades
    and effort cuts [D01-S12].
15. **Match the metric to the pillar the stem names.** A real improvement against an unnamed metric is
    still a losing option.

---

## 9. Practice items

> Original items written against the published objectives. They do not reproduce live exam content.

**Item 1 (select 1).** A utility processes 2.3M meter-anomaly reports per month. Each is free text; the
output is one of nine anomaly codes plus a confidence score, consumed from a next-day work-order queue.
The sponsor's goal is cost per processed report. Best architecture?
**A.** Agentic loop with meter-history and weather tools per report. **B.** One augmented-LLM classification
call per report via Message Batches, with a cached shared taxonomy prefix. **C.** Orchestrator-workers, a
worker per anomaly code. **D.** Synchronous calls at high concurrency to minimize latency.
**Answer: B.** Nine known classes plus a next-day consumer make this a bounded classification with no
latency pressure; batch is 50% off with most batches under an hour [D01-S15], and caching is a named free
win [D01-S12]. **A** pays ~4× chat token cost [D01-S03] for a single classification and adds unbounded
latency. **C** misapplies orchestrator-workers: the subtasks are enumerable, making this parallelization at
most [D01-S02]. **D** optimizes latency nobody asked for and forfeits the discount (A6).

**Item 2 (select 1).** An investment firm wants answers to arbitrary diligence questions drawing on
filings, news, court records, and a subscription data provider. Analysts cannot predict which sources a
given question needs. Answers within the hour, with citations. Most appropriate pattern?
**A.** Prompt chaining with fixed stages per source type. **B.** Routing to one of four source-specific
handlers. **C.** Orchestrator-workers, with a lead agent planning and spawning subagents per facet.
**D.** Evaluator-optimizer between a researcher and a citation checker.
**Answer: C.** The decomposition depends on the question — Anthropic's stated condition: "complex tasks
where you can't predict the subtasks needed" [D01-S02]; parallel subagents with separate windows are also
what makes a corpus exceeding one window tractable [D01-S03][D01-S04]. **A** requires fixed subtasks, which
the stem denies. **B** routes to a single class; diligence questions span sources simultaneously. **D** is a
verification mechanism, not a decomposition mechanism.

**Item 3 (select 2).** A team is deciding whether to split a single customer-service agent into multiple
agents. Which **two** observations most justify the split?
**A.** It exposes 24 tools spanning billing, diagnostics, and account administration. **B.** Average handle
time rose 8% since launch. **C.** Order-history retrieval fills the context and measurably degrades
reasoning on the subsequent technical diagnosis. **D.** The team wants billing logic owned by the billing
squad. **E.** It occasionally produces a typo.
**Answer: A and C.** A is the specialization signal — selection degrades past ~20 tools across unrelated
domains [D01-S04]. C is context protection, Anthropic's own worked example [D01-S04]. **B** is a symptom
with no identified cause. **D** is organizational convenience — a problem-centric split inviting the
telephone game [D01-S04]. **E** has no bearing on decomposition.

**Item 4 (select 1).** A generated marketing brief passes the model's own "review your work" step every
time, yet human editors reject 40% for missing required disclosures. The requirements are a one-page
checklist. Which change most directly fixes this?
**A.** Increase reasoning effort on generation. **B.** Replace the self-review with a deterministic checklist
validator that names the specific missing disclosure. **C.** Add a second self-review pass. **D.** Switch to
a more capable model.
**Answer: B.** The requirements are enumerable, so a rule can express "correct" — "the best form of feedback
is providing clearly defined rules for an output, then explaining which rules failed and why" [D01-S06].
**A** and **D** may lift general quality but leave the broken gate. **C** compounds it: self-evaluation
"confidently prais[es] the work" [D01-S08], so a second pass praises it twice.

**Item 5 (select 1).** A clinical-summary agent runs 20–40 minutes per chart and occasionally crashes
mid-run, losing all progress. Most direct architectural fix?
**A.** Switch to a 1M-token model. **B.** Persist progress to an append-only event log or structured
artifact outside the context window and resume from the last recorded event. **C.** Retry wrapper that
restarts from the beginning. **D.** Lower reasoning effort so runs finish faster.
**Answer: B.** For long-running agents "minor system failures can be catastrophic" without mitigation, and
the remedy is resumption rather than restart [D01-S03]; a session that "lives outside Claude's context
window" lets a crashed harness resume "from the last event" [D01-S09]. **A** addresses capacity, not
durability. **C** is restart — the thing to avoid — and doubles cost on failure. **D** shortens exposure
without removing the failure mode.

**Item 6 (select 1).** A team proposes replacing a single Opus-class agent with a coordinator plus four
cheaper workers to cut cost. The work is a dependent chain and fits comfortably in one context window.
What do you tell them?
**A.** Proceed; delegating bulk work to cheaper models reliably lowers cost. **B.** Proceed, but cap subagent
depth and concurrency. **C.** Do not proceed yet — first price the single model across its effort levels,
because an orchestrator loses to a single model at lower effort when work fits one context and the chain
is dependent. **D.** Proceed only if workers use the coordinator's model.
**Answer: C.** The orchestrator strategy pays when work exceeds one context window with massive parallelism
or as tail insurance; when work fits one context or the chain is dependent, "handoff and merge cost more
than the plan," and "Multi-model configurations must beat the single model's full effort curve" [D01-S12].
**A** states the conclusion the measurement contradicts for this shape. **B** is good hygiene [D01-S19] but
does not fix a strategy wrong for the shape. **D** removes the only cost argument for the split.

**Item 7 (select 1).** A returns-processing design routes each request through: (1) an LLM call to extract
the order ID, (2) an LLM call to decide whether the 30-day return window has expired given the purchase
date, (3) an LLM call to draft the customer response. Strongest architectural criticism?
**A.** Merge the three calls into one to cut latency. **B.** Step 2 is a deterministic date comparison
against a published policy and should be code. **C.** Replace the chain with an agent so it handles
exceptions. **D.** Run the steps in parallel.
**Answer: B.** A 30-day window comparison is arithmetic against a published rule; making it a model call
makes a deterministic decision non-deterministic and unauditable for no benefit (A5), and code-based
verification is preferred "when fast, cheap, and objective verification is possible" [D01-S10]. **A** would
remove the intermediate gates that make chaining valuable [D01-S02]. **C** escalates complexity for a fully
enumerable tree. **D** is impossible: the steps are dependent.

**Item 8 (select 2).** Which **two** statements about subagents are correct?
**A.** Only a subagent's final message returns to the parent; intermediate tool calls and results stay
inside it. **B.** Subagents can message one another directly to coordinate. **C.** A subagent inherits the
parent's full conversation history by default. **D.** A subagent can be restricted to a subset of tools, a
least-privilege lever. **E.** Subagents reduce total token consumption relative to one agent doing the same
work.
**Answer: A and D.** A is stated directly [D01-S19] and is the mechanism behind context isolation; returned
summaries are typically 1,000–2,000 tokens [D01-S05]. D is one of the four named benefits — e.g. a reviewer
limited to read-only tools [D01-S19]. **B** is false: subagents cannot communicate directly [D01-S20].
**C** is false: a non-fork subagent starts fresh, and "the only content you pass from parent to subagent is
the Agent tool's prompt string" [D01-S19]. **E** is inverted — multi-agent typically consumes 3–10× the
tokens [D01-S04].

**Item 9 (select 1).** An insurer must summarize 90,000 claim files for an annual regulatory filing due in
three weeks. Nobody consumes the summaries interactively; cost is the stated constraint; accuracy is
verified by sampling. Best fit?
**A.** Synchronous calls behind an internal API so compliance can spot-check as they arrive. **B.** Message
Batches submission with results keyed by `custom_id` and an offline eval gate on a stratified sample.
**C.** Multi-agent with a summarizer and a fact-checker per file. **D.** An agentic loop per file with a
document-retrieval tool.
**Answer: B.** Nobody is waiting, so the 50% discount applies with a 24-hour ceiling well inside three
weeks; results arrive in any order and must be keyed by `custom_id` [D01-S15]; the sampling requirement is
an offline eval, the right placement for a pre-launch gate [D01-S10]. **A** forfeits the discount for
interactivity nobody requires. **C** multiplies tokens 3–10× [D01-S04] where sampling already provides the
check. **D** is agentic complexity for a single summarization.

**Item 10 (select 1).** A long-running coding agent loses coherence after ~90 minutes. The team is choosing
between compaction and a context reset with a structured handoff artifact. Which consideration most favors
the reset?
**A.** The task involves extensive conversational back-and-forth with the user that must be preserved.
**B.** Work proceeds through clear, independently verifiable milestones whose state is fully capturable in
a progress file and version control. **C.** The team wants to avoid maintaining any state outside the
model's context. **D.** The team wants fewer API calls.
**Answer: B.** A reset "provides a clean slate, at the cost of the handoff artifact having enough state for
the next agent to pick up the work cleanly" [D01-S08]; milestone work with a progress file and git history
is exactly where the artifact can carry the state [D01-S07]. **A** favors compaction, which "maintains
conversational flow for tasks requiring extensive back-and-forth" [D01-S05]. **C** argues against the reset —
the artifact *is* external state. **D** is unrelated; neither technique is chosen on call count.

**Item 11 (select 1).** An executive sponsor says: "I don't want a cheaper version of what we already do. I
want my analysts producing categories of analysis they can't produce today." Most appropriate
architectural response?
**A.** Optimize the existing pipeline with caching and batch to lower unit cost. **B.** Design for the
transformation pillar — accept higher per-task cost for an agentic or multi-agent architecture that makes
previously infeasible analyses possible, and measure success as volume of newly feasible work rather than
cost per analysis. **C.** Route everything to the smallest model meeting the current accuracy bar.
**D.** Add a human approval gate to increase trust in existing outputs.
**Answer: B.** The sponsor named transformation — work that "wouldn't have been done otherwise" [D01-S22].
That is the pillar justifying 3–10× tokens for multi-agent exploration [D01-S04], and it changes the
success metric. **A** and **C** optimize cost and efficiency, explicitly deprioritized (A6). **D** addresses
trust in existing output without expanding what is possible.

**Item 12 (select 3).** A proposal adds a "quality assurance agent" that reviews every output of a
production coding agent before commit. Which **three** considerations should most shape your
recommendation?
**A.** Verification requires minimal context transfer, so a verifier can black-box test the work without
the full history. **B.** The dominant failure mode of verification subagents is marking outputs as passing
without thorough testing. **C.** A verifier is worth the overhead only when the task sits beyond what the
current model does reliably solo. **D.** Verification agents always reduce total token consumption by
preventing rework. **E.** Two agents editing the same files in parallel reliably speeds up remediation.
**Answer: A, B, C.** A is why this is the cheapest multi-agent pattern [D01-S04]. B is the named dominant
failure mode and dictates that the verifier actually exercise the artifact against concrete criteria
[D01-S04][D01-S08]. C is the stated ROI rule — include evaluation "when the task sits beyond what the
current model does reliably solo," a boundary that moves outward as models improve [D01-S08]. **D** is
unsupported: the verifier adds cost, and multi-agent raises token use 3–10× [D01-S04]. **E** is an
anti-pattern — "Two subagents editing the same file in parallel is a recipe for conflict" [D01-S20].

---

## 10. Objective-coverage table

| # | Objective [D01-S01] | Where covered |
|---|---|---|
| 1 | Translate business problems into Claude-based AI solutions | §2; §3.12; §4.8; S1–S8; Items 1, 9, 11 |
| 2 | Design end-to-end architectures (input → processing → output → feedback loops) | §3.4, §3.5, §3.10, §3.11; §4.4, §4.5; §6; S1, S2, S4, S8; Items 4, 5, 9 |
| 3 | Select appropriate architectural patterns (workflow, agentic, augmented LLM) | §3.1–§3.3; §4.1, §4.3; AP2, AP3; S1, S3, S6, S7, S8; Items 1, 2, 7 |
| 4 | Design multi-agent systems and orchestration strategies | §3.7, §3.9; §4.2, §4.6, §4.8 (advisor vs. orchestrator); AP1; S5, S6; Items 3, 6, 8, 12 |
| 5 | Apply decomposition techniques for complex problem solving | §3.8, §3.9; §4.6, §4.7; AP1, AP5, AP6; S1, S5, S6; Items 3, 8, 10, 12 |
| 6 | Align solutions to business value pillars | §3.12; §4.4, §4.8; §8 heuristics 1, 10, 12, 14, 15; S3, S6, S8; Items 1, 9, 11 |

---

## 11. Sources

| ID | Source | URL | Accessed |
|---|---|---|---|
| D01-S01 | Claude Certified Architect – Professional Exam Guide v1.0, Anthropic | (local) `../claude-arch-professional-guide.md` | 2026-09-24 |
| D01-S02 | "Building effective agents," Anthropic Engineering | https://www.anthropic.com/engineering/building-effective-agents | 2026-09-24 |
| D01-S03 | "How we built our multi-agent research system," Anthropic Engineering | https://www.anthropic.com/engineering/multi-agent-research-system | 2026-09-24 |
| D01-S04 | "Building multi-agent systems: when and how to use them," Anthropic | https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | 2026-09-24 |
| D01-S05 | "Effective context engineering for AI agents," Anthropic Engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2026-09-24 |
| D01-S06 | "Building agents with the Claude Agent SDK," Anthropic | https://claude.com/blog/building-agents-with-the-claude-agent-sdk | 2026-09-24 |
| D01-S07 | "Effective harnesses for long-running agents," Anthropic Engineering | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2026-09-24 |
| D01-S08 | "Harness design for long-running application development," Anthropic Engineering | https://www.anthropic.com/engineering/harness-design-long-running-apps | 2026-09-24 |
| D01-S09 | "Scaling Managed Agents: Decoupling the brain from the hands," Anthropic Engineering | https://www.anthropic.com/engineering/managed-agents | 2026-09-24 |
| D01-S10 | "Demystifying evals for AI agents," Anthropic Engineering | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-09-24 |
| D01-S11 | "Writing effective tools for agents — with agents," Anthropic Engineering | https://www.anthropic.com/engineering/writing-tools-for-agents | 2026-09-24 |
| D01-S12 | "Optimizing for cost and intelligence," Anthropic docs | https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence | 2026-09-24 |
| D01-S13 | "Choosing the right model," Anthropic docs | https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | 2026-09-24 |
| D01-S14 | "Models overview," Anthropic docs | https://platform.claude.com/docs/en/about-claude/models/overview | 2026-09-24 |
| D01-S15 | "Batch processing / Message Batches API," Anthropic docs | https://platform.claude.com/docs/en/build-with-claude/batch-processing | 2026-09-24 |
| D01-S16 | "Streaming messages," Anthropic docs | https://platform.claude.com/docs/en/build-with-claude/streaming | 2026-09-24 |
| D01-S17 | "Tool use with Claude (overview)," Anthropic docs | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | 2026-09-24 |
| D01-S18 | "Multiagent orchestration," Managed Agents docs (beta) | https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration | 2026-09-24 |
| D01-S19 | "Subagents in the SDK," Claude Code docs | https://code.claude.com/docs/en/agent-sdk/subagents | 2026-09-24 |
| D01-S20 | "How and when to use subagents in Claude Code," Anthropic | https://claude.com/blog/subagents-in-claude-code | 2026-09-24 |
| D01-S21 | "Building trusted AI in the enterprise," Anthropic (PDF) | https://www-cdn.anthropic.com/e5c9de22bc8884089970bd262ca0c8b952cb9136.pdf | 2026-09-24 |
| D01-S22 | "How AI is transforming work at Anthropic," Anthropic Research | https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic | 2026-09-24 |
| D01-S23 | "Introducing Claude Opus 5.5," Anthropic | https://www.anthropic.com/news/claude-opus-5-5 | 2026-09-24 |
| D01-S24 | `claude-api` local skill bundle, SKILL.md (cached model table dated 2026-06-24) | (local skill) | 2026-09-24 |
| D01-S25 | `claude-api` local skill bundle, `shared/agent-design.md` | (local skill) | 2026-09-24 |

Full source table, including third-party prep material assessed at `low` trust and never used for a
technical claim, is in `research/01-solution-design-sources.md`.

**`[UNVERIFIED]` claims in this chapter.** (1) *"Business value pillars" as an Anthropic framework* — the
five-item list appears only in the exam blueprint [D01-S01]; the pillar→metric→architecture mapping in
§3.12 and §4.8 is a synthesis from [D01-S21], [D01-S22], and [D01-S12]. (2) *Item count for this domain
(~10–11 of 63)* — arithmetic on the published 17% weight; Anthropic publishes no per-domain item counts.
(3) *Which vocabulary the exam uses* — whether items use the 2024 "Building effective agents" taxonomy or
Anthropic's newer harness/session/coordinator vocabulary is unknown; objective 3's wording points to the
former, which this chapter teaches as primary. (4) *No numeric "too many tools" threshold exists in
Anthropic documentation* — the "20+" figure is a signal from [D01-S04], not a limit, and is presented as
such.

**Model currency note.** The course brief and the bundled `claude-api` skill's cached table (2026-06-24)
list Claude Opus 5 as current. Verification against the live models overview on **2026-09-24** shows
**Claude Opus 5.5** (`claude-opus-5-5`, $4 in / $20 out per MTok, 1M context, 128K max output, default
effort `medium`), released **2026-09-22**, as the recommended default, with Claude Opus 5 moved to the
legacy list [D01-S14][D01-S23]. This chapter follows the live documentation and deliberately keeps model
names out of architectural statements wherever the argument does not depend on one.
