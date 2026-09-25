# Adversarial Review — Domain 1: Solution Design & Architecture (17%)

Adversarial reviewer deliverable. Reviewed: `research/01-solution-design-dossier.md`,
`drafts/01-solution-design-draft.md`. Ground truth used: `../claude-arch-professional-guide.md` §6 objectives
and §8 samples + rationales; `VERIFIED-FACTS.md`; `AGENT-BRIEF.md`. Review date 2026-09-24.

```
VERDICT: MAJOR-REWORK (scoped)
Scope: §§2–4, 6–8 and 10–11 ship with fixes. §5 (S5, S6, S7), §9 (Items 2, 8, 11, 12), and the
Objective-1 / input-stage coverage gaps require rework before this can be taught from.

Top 3 must-fix items:
1. Item 11's answer key teaches "sponsor said transformation ⇒ pick agentic/multi-agent." That is the
   exact reflex the exam punishes (its own Sample 1 rewards REMOVING capability). A pillar selects a
   metric, never a pattern. Rewrite the key. Same defect is baked into the §4.8 pillar table's
   "Architecture it selects" column and into S6's pillar note.
2. S5 recommends a coordinator + domain subagents under a stated "p95 first-token under 2 seconds"
   budget — the same budget it uses one sentence later to eliminate an evaluator agent for "adding a
   synchronous hop." The recommendation breaks the constraint that kills its rival, and it skips the
   fix the chapter's own §6 row 1 prescribes for that exact symptom (context editing) and the fix AP5
   prescribes for 26 endpoint-shaped tools (consolidation). Re-solve the scenario.
3. Objective 1 has no primary-source content. The dossier's Anthropic pilot-selection criteria
   ("well suited to LLM capabilities," "abundant data… with permission to use it," "business critical
   but low security risk," "minimal disruption / parallel deployment"), the success-criteria rubric,
   and the graduation criteria are all in the dossier and all absent from the draft. A four-option
   "which is the best first use case?" item — the cheapest item in the domain to write — leaves the
   candidate nothing. Restore it, and drop the redundant Item 9 slot to test it.
```

Two cross-cutting judgments the orchestrator should carry forward:

- **Outcome-balanced, reasoning-biased.** Five of eight scenarios land on the simpler design, so the
  chapter passes a headcount test for agentic bias. But the two scenarios that land on agentic/multi-agent
  (S5, S6) are the two with the weakest reasoning, and the *answer key* of Item 11 plus one column of the
  §4.8 pillar table encode "more ambition ⇒ more agents" as doctrine. Bias has been pushed out of the
  conclusions and left in the justifications, which is harder to spot and worse for a candidate.
- **The chapter never once recommends: decline, narrow the scope, buy instead of build, precompute/cache
  the answer, use classical ML or a trained classifier, add a human instead of autonomy, or raise `effort`
  on one model instead of adding architecture.** Every one of those is a credible exam key. The last is the
  most dangerous omission because `VERIFIED-FACTS.md` names the docs' own method — *default → raise effort
  → only then change model* — as canonical [D01-A01].

---

## Attacks that landed

### Internal contradictions (a candidate taught this has two chapter-sanctioned opposite answers)

**[BLOCKER] §5 S5 vs. §5 S5's own rejection clause, §6 row 1, and AP5** — S5's constraints include
"streaming UX with a p95 first-token under 2 seconds." The recommendation is "a coordinator with domain
subagents." A coordinator must receive the turn, decide, spawn a subagent, wait for the subagent's tool
calls, and receive a 1–2k-token summary before the user's first token renders — minimum two model calls
plus tool round-trips serially ahead of first token, i.e. seconds, not sub-2-second. The chapter eliminates
the evaluator-agent option in the same paragraph because it "adds a synchronous hop to a 2-second TTFT
budget." One synchronous hop disqualifies the alternative; two-plus hops are recommended. Separately, the
stem's symptom — "forgets the technical problem mid-conversation" after order-history retrieval — is
verbatim row 1 of the chapter's own §6 table, whose prescribed fix is "context editing, then compaction or
a context reset," and the stem's 26 endpoint-shaped tools are verbatim AP5, whose prescribed fix is
consolidation. **Required fix:** re-solve S5 as a staged answer — (1) consolidate 26 tools to
workflow-shaped tools [D01-S11]; (2) clear stale tool results / retrieve order history just-in-time
[D01-S05][D01-S25]; (3) only if the tool surface genuinely spans unrelated domains after consolidation,
split — and then state that the split moves the TTFT budget onto a fast front agent that streams an
acknowledgment while the subagent works, or state that the 2-second budget must be renegotiated. Either
resolution is fine; silently violating the stated constraint is not.

**[BLOCKER] AP1 vs. §3.11 / §4.5 / Item 12** — AP1 says mirroring job titles into agents ("QA agent,
security agent, docs agent") is *the* canonical anti-pattern. §4.5, §3.11 and Item 12 say a **separate
evaluator agent** is "a strong lever." A separate evaluator *is* a problem-centric split by job title. The
chapter never reconciles this, so a candidate facing "should we add a reviewer agent?" has two taught,
opposite answers and will coin-flip. **Required fix:** state the reconciliation explicitly — verification is
the one legitimate problem-centric split, precisely *because* its value comes from **not** sharing the
generator's context and because "verification requires minimal context transfer by nature" [D01-S04]. The
anti-pattern is a QA agent that must *re-derive* the generator's context to do its job; the legitimate case
is a verifier that black-box tests an artifact against a rubric. One sentence in AP1 and one in §4.5.

**[BLOCKER] §3.3 vs. §8 heuristic 3** — §3.3: "The five workflow patterns… all are workflows; your code owns
control flow," including orchestrator-workers. Heuristic 3: "Can you enumerate the subtasks before seeing
the input? … No → orchestrator-workers or an agent (**the model owns it**)." The chapter both asserts and
denies that orchestrator-workers is code-owned. An item asking whether a described system is a workflow or
an agentic system — a very likely Objective-3 item, since the objective names the three tiers — is now
unanswerable from this chapter. **Required fix:** state the resolution Anthropic's taxonomy actually
implies: orchestrator-workers is a **workflow** because the control *skeleton* (plan → dispatch → synthesize
→ return) is fixed code; what the model determines is the **fan-out**, not the sequence. Contrast with an
agent, where the model chooses what step comes next including whether to stop. Add "who owns the *sequence*"
as the discriminator, not "who owns the split."

**[MAJOR] §3.4 vs. §5 S6 and S7** — §3.4 states as a gate: "No cheap objective signal in the environment
(tests, compiler, schema, a query returning rows) → no agent." S7 correctly applies it ("there is no
compiler for a contract"). S6 recommends a lead agent spawning subagents for competitive-intelligence
briefs, where there is no environmental ground truth whatsoever — the failure mode is a confident brief
citing a trial registry entry that does not say what the brief claims. The chapter enforces its own rule in
one scenario and violates it two scenarios earlier. **Required fix:** soften §3.4 to what is defensible —
absent environmental ground truth, the agentic tier requires a *substitute* verification channel (mandatory
source-quoting contracts, a retrieval-grounded citation check, or human review of every output) and you pay
for it in the design; it is not free and it is not optional. Then make S6 name its substitute.

**[MAJOR] §5 S7 vs. §9 Item 4** — Item 4's lesson: requirements that fit "a one-page checklist" ⇒ replace the
LLM critic with a deterministic validator that names the missing item. S7's stem gives "a written
negotiation playbook with **explicit fallback positions**" — enumerable — and the chapter jumps straight to
an LLM evaluator-optimizer. The cheaper, chapter-consistent answer is a deterministic coverage check ("does
the draft address each of the 14 fallback clauses?") plus regeneration, reserving the LLM evaluator for the
judgment residue (is the fallback *language* adequate?). **Required fix:** make S7's recommendation the
hybrid, and use its "what changes it" to say when a pure LLM evaluator earns its place (criteria are
qualitative and cannot be reduced to presence/absence).

### Agentic-bias and answer-key defects

**[BLOCKER] §9 Item 11 key + §4.8 pillar table, "Architecture it selects" column** — Key B asserts the correct
response to "I want analyses we can't produce today" is "an agentic or multi-agent architecture." Counter-
scenario: the newly feasible analysis is *joining two datasets nobody has joined before* — a scheduled batch
workflow over a new join, with one augmented-LLM call per record, delivers a category of analysis that did
not exist, at 1/20th the cost, with auditability the sponsor will need when the analysis is challenged. A
candidate who has internalized the chapter's own heuristic 2 can defend A (optimize what exists, then fund
the new capability from the savings) or reject B on simplicity grounds and be marked wrong. **Required fix:**
the pillar sets the **metric and the cost you can defend**, never the pattern. Rewrite B to "reframe success
measurement around volume of newly feasible work rather than cost per analysis, and let the pattern follow
from whether the new analyses require exploration whose shape is unpredictable." Rewrite the pillar table
column header to "What it changes about measurement and defensible cost," and delete "Justifies
agentic/multi-agent spend" / "Favors workflow/routing over agentic" — a pillar cannot favor a pattern
without knowing the task.

**[MAJOR] §9 Item 2** — the stem's only force toward orchestrator-workers is "analysts cannot predict which
sources a given question needs." A single agent with one federated search tool satisfies that completely,
and the chapter's own §4.2 rule requires multi-agent to rest on a **demonstrated** constraint. The item
omits the single-agent option, so it trains "multiple data sources + unpredictable ⇒ multi-agent" — the
keyword reflex. **Required fix:** add a fifth option ("a single agent with a federated search tool and a
per-claim citation contract") and put the real discriminator in the stem: the per-question corpus exceeds one
context window, 30+ sources must be explored concurrently to hold the one-hour bound, and a measured
single-agent baseline missed it. Then C wins on stated constraints instead of on vibes.

**[MAJOR] §5 S6** — the stem makes "source attribution mandatory" and the design answers it with a
**post-hoc citation pass** over synthesized text. Attributing claims after synthesis is how citation
fabrication happens: the subagent summaries have already discarded provenance, so the citation pass is
guessing which source supports a sentence. The chapter's own [D01-S03] guidance — each subagent needs "an
output format" — is the fix, and the chapter cites it two sections earlier. **Required fix:** provenance
travels in the subagent output contract (claim → source ID → quoted span); the final pass *verifies*
citations, it does not create them. Also add the omitted alternative: analysts already know the ten
registries that matter, so a curated connector set + scheduled batch retrieval + one long-context synthesis
is the cheaper baseline the design must beat.

**[MAJOR] §5 S3** — the stated metric is unit cost over 4M SKUs on a **monthly refresh**, and the
recommendation's cost levers are batch (2×) and caching. It never mentions the two levers that dominate both
by an order of magnitude: (1) **process only the delta** — a monthly refresh over a catalog means most SKUs
are unchanged, so the unit of work is changed SKUs, not 4M; (2) **deduplicate to product families** — SKU
variants (size/color) share attributes, so one call per family fans out to N SKUs. A CFO comparing a 2×
saving against a 10× saving will ask why the architect proposed the 2×. **Required fix:** add delta
processing and family-level deduplication as the first cost levers, ahead of batch and caching, and say why:
free wins operate on the number of units, not just the price per unit.

**[MAJOR] §5 S8** — "operators need a recommended action within 3 seconds" and the 20% novel branch is "a
bounded agentic investigation with a step cap, streamed." A loop with even three tool calls does not close
in 3 seconds. The chapter parks the real design in "what changes it" as a contingency. Also missing: at
8,000 novel exceptions/day the cheapest high-quality answer is **retrieval over the resolution log**
(nearest-neighbor against historically resolved exceptions) at ~0 latency, and **human triage with a
model-drafted brief** — operators are already sitting there. **Required fix:** make the async-with-immediate-
acknowledgment design the recommendation, not the fallback, and add the retrieval-over-history option as the
alternative the agentic branch must beat.

**[MAJOR] §5 S4** — the model drafts "a plain-language explanation of the service's output," and that
explanation enters an appeals record. A generated explanation of a statutory determination can misstate the
reason while the determination is correct — the exact auditability failure the scenario is built to avoid.
The chapter's own [D01-S06] principle ("explaining which rules failed and why") points at the deterministic
answer: the rules service emits the failed-rule identifiers, and a template renders them. **Required fix:**
templated explanation from failed-rule output as the recommendation; the model's role is narrowing to
readability, with the rule citation immutable.

**[MINOR] §5 S1** — "twelve document types, each with a known extraction schema" routed by an LLM classifier.
Most regulated loan forms carry a form number; a deterministic form-ID lookup or a trained classifier over
labeled history is cheaper and auditable, and commercial document-intake products exist. The chapter never
raises buy-vs-build or classical ML anywhere. **Required fix:** one clause in S1 ("the routing step is a
classifier, not necessarily a model call — use the form ID when the document carries one"), plus a line in
§4.1 that the tier ladder starts below the augmented LLM.

### Heuristics that misfire (full set in "Heuristic boundary conditions")

**[MAJOR] §8 heuristic 3 / §2 archetype A2** — "Can you enumerate the subtasks before seeing the input? Yes →
parallelization. No → orchestrator-workers." Counter-scenario: "summarize each chapter of an arbitrary book,
then synthesize." The subtask *type* is fully known; the *count* varies per input. The heuristic as written
pushes the candidate to orchestrator-workers; the correct answer is code-owned fan-out (sectioning with
dynamic N). A stem saying "the number of subtasks varies by document" is a trivially writable trap and this
chapter arms the candidate wrongly. **Required fix:** the test is enumerability of subtask **type**, not
count. Known type + variable count = parallelization your code fans out. Unknown type = orchestrator.

**[MAJOR] §8 heuristic 9 ("grade outcomes, not trajectories")** — stated as an absolute. Counter-scenario: an
agent produces the correct filing but reached it by reading 400 patient records it had no entitlement to, or
by dropping and re-creating a table. Outcome grading passes it. In regulated systems the *path* is the
requirement. **Required fix:** "Grade outcomes for **quality**; constrain and audit trajectories for
**policy** — which records were touched, which tools were called, whether any irreversible action occurred.
Never grade the path for correctness; always check it for permission."

**[MAJOR] §8 heuristic 5 + §4.2 "choose multi-agent only on a demonstrated constraint"** — three
justifications are named (context protection, parallelization, specialization), and the same §4.2 table has a
**Security** row saying per-agent tool restriction is a least-privilege lever [D01-S19]. Counter-scenario: one
agent needs PHI read access and outbound email; splitting so no single context holds both is a
compliance-driven decomposition with none of the three named justifications. Given the exam's own Sample 1
rewards capability removal, "split so the sending agent never sees PHI" is a very plausible key, and this
chapter tells the candidate it is the distractor. **Required fix:** name **blast-radius / least-privilege
containment** as a fourth legitimate justification, with the qualifier that it justifies splitting the
*privilege surface*, which may or may not require separate loops — a per-call tool allowlist can achieve it
at 1× cost.

**[MAJOR] §8 heuristic 2 ("simplest tier that satisfies the constraint wins")** — "simple" is undefined, and the
chapter silently means "fewest model-owned decisions." Counter-scenario: a one-off migration of 300
heterogeneous legacy documents. The "simpler" deterministic pipeline requires enumerating and then
maintaining twelve extraction schemas — three engineer-weeks and a permanent maintenance liability. One
agent with a schema-validation tool costs $40 and a day. For low-volume, one-shot, or long-tail-heavy work,
the agent is the simpler *system*. **Required fix:** define simplicity as "fewest moving parts you must
build, operate and maintain," and add the volume/repetition qualifier: determinism earns its build cost
through repetition. A workflow with 47 hand-maintained branches is not simpler than one agent.

**[MAJOR] §4.1 "Error-cost tolerance: errors must be recoverable" treated as a precondition** — recoverability
is mostly a **design output**, not an input filter. Counter-scenario: an agent that only ever *proposes*
(dry-run diffs, staged writes, propose-then-approve) has recoverable errors by construction, even in an
irreversible domain. The chapter's framing tells a candidate to abandon the agentic tier when the real answer
is to constrain the action surface — which is exactly the exam's Sample-1 reflex. **Required fix:** add a
line: "If errors are not recoverable, make them recoverable before you reject the tier — propose-only,
dry-run, staged writes, reversible operations, approval gate on the irreversible step."

**[MAJOR] §8 heuristic 7 ("if a rule can express correct, use the rule")** — needs a maintenance and coverage
qualifier. Counter-scenario: a 4,000-rule tax code revised annually. The rules are expressible; the
implementation is a permanent liability, and a rules gate with 5% coverage gaps fails *silently* and
over-blocks valid outputs. **Required fix:** "…if the rule set is enumerable **and stable enough that
maintaining it costs less than the errors it prevents**. Otherwise: rules for the enumerable core,
model-or-human for the residue, and instrument the residue's size."

**[MINOR] §8 heuristic 10 ("nobody waiting → batch")** — "nobody waiting" is not "no deadline."
Counter-scenario: a nightly enrichment feeding a 06:00 downstream job. Nobody waits, but the 24-hour batch
tail plus no in-flight prioritization can blow a hard 6-hour window with no partial-retry semantics.
**Required fix:** "Nobody waiting **and** no downstream deadline inside the 24-hour tail **and** you can
re-run or fall back to sync for stragglers." Also note data-residency/retention implications, which the
chapter never raises for batch.

**[MINOR] §8 heuristic 8 ("self-critique is not a gate") and AP4 ("the gate is decorative")** — over-stated.
[D01-S08]'s finding is about *subjective quality* praise. Same-context self-checks do catch objective slips
(format, unit consistency, arithmetic re-derivation), and sometimes a single extra call is all the latency
budget allows. **Required fix:** "cannot be the final gate for **subjective** quality; a rules check
dominates it on objective properties, so it is rarely the best use of a call."

**[MINOR] §8 heuristic 1 / archetype A4 ("reread the stem for a number with a unit")** — this teaches
number-hunting, which is keyword matching. Counter-scenario: a stem with two numbered constraints in tension
(p95 2s **and** 99% accuracy), or one whose binding constraint carries no number at all (S2's
"denials must be issued by a licensed reviewer"). **Required fix:** add the precedence order — legal /
delegation-of-authority > hard SLA > accuracy floor > cost target — and note that a volume figure
(2.3M/month) is a sizing input, not a constraint.

**[MINOR] §8 heuristic 14 ("free wins first")** — caching is not free: writes cost more than base input, and
prefix stability constrains the design (you cannot rotate tool sets mid-session — the chapter's own §6 says
so). Calling **batch** a "free win" is contradicted three sections later by "reject batch on any per-request
SLA." **Required fix:** "free" = *no quality cost*, not *no constraint cost*; list what each free win costs
you in flexibility. Cache-write multiplier is a validator question (Q2).

### Cost and SLA hand-waving

**[MAJOR] §4.1 "Relative cost" column and §9 Item 1 rationale** — the column reads 1× / ~steps × 1× / "~4× a
chat interaction." The baseline changes inside one column: rows 1–2 are per-call multiples, row 3 is a
multiple of a Claude.ai chat *session* [D01-S03]. The dossier flagged exactly this (§6.2: "the draft must
always state the baseline") and §4.2 complies while §4.1 does not. Worse, Item 1's rationale applies the
session-level figure to a per-request comparison: "A pays ~4× chat token cost for a single classification."
A multi-turn agentic loop with two tools against one classification call is 1–2 **orders of magnitude**,
not 4×. The chapter understates the cost of its own wrong answer while sounding quantitative. **Required
fix:** relabel the §4.1 row with its baseline, and in Item 1's rationale say "one to two orders of magnitude
more tokens than a single classification call; the published 4× and 15× multipliers are measured against
chat sessions, not against a single API call, and cannot be used as per-request multipliers."

**[MAJOR] §4.8 pillar table, "Performance SLA: … accuracy floor"** — an accuracy floor is listed beside p95
latency and availability as though it were the same kind of contractual object. It is not: latency and
availability are measured continuously on all traffic; an accuracy floor is an estimate on a *sample* from a
*distribution*, with a confidence interval, that decays as traffic drifts. Promising "95% accuracy" as an
SLA without naming the eval set, sample size, refresh cadence and remediation path is the single most
common way an architect creates an unmeetable contract. **Required fix:** add the qualifier — a quality floor
is contractible only as "≥X% on a named, versioned, periodically refreshed eval set, measured on a stated
sample, with a defined remediation process when it is breached." This is squarely Domain 1's SLA objective
and it is one sentence.

**[MAJOR] §4 and §5 — no worked unit economics anywhere** — a domain whose objective names "cost, performance
SLAs" contains zero arithmetic linking a token footprint to a bill or a latency budget to a step count. A
candidate cannot order two cost levers by magnitude without it. **Required fix:** one compact worked example
(volume × tokens-per-unit × price, then apply batch, then apply delta-only) and one latency budget
decomposition (TTFT + N tool round-trips + generation vs. the stated p95). Two short blocks; they can
replace the tool-overhead token table, which is volatile and belongs to Domain 2/3.

**[MINOR] §4.5 pass^k** — 0.9^5 = 0.590 is correct arithmetic, but "90% right once is 59% right five times
running" quietly assumes independence and quietly slides from "k trials of one task" to "five consecutive
user requests." Real agent failures are correlated (same hard input class). **Required fix:** one clause —
"assuming independent trials; correlated failure modes make the real figure worse on the hard slice, which
is why you measure pass^k on the tail, not on a random sample."

**[MINOR] §4.8 "caching alone cut agent-loop cost by a factor of 2.7 to 5.3"** — cited but baseline-free (which
loop, what cacheable-prefix share, what hit rate). **Required fix:** add "on Anthropic's reported agent
loop, where the cacheable prefix dominated the request" or drop the range and keep the direction.

**[MINOR] §9 Items 1 and 9, §5 S3 — stacking batch and cache discounts** — three correct answers depend on
prompt caching working inside Message Batches. Requests in a batch are processed in arbitrary order and in
parallel, which is not obviously compatible with a short cache TTL. The *architectural* claim (batch for
non-interactive bulk; order stable content first) survives either way; the compounded-discount arithmetic may
not. **Required fix:** state the two levers separately and do not multiply them until confirmed. See
validator Q1.

### Exam mismatch and coverage holes

**[BLOCKER] Objective 1 has no primary-source method** — detailed in the verdict block. The dossier's §3
Objective-1 content (pilot-selection criteria, success-criteria rubric, graduation criteria, parallel
deployment) is fully sourced [D01-S21] and entirely absent from the draft. The objective-coverage table
claims coverage via "§2; §3.12; §4.8; S1–S8" — none of which teaches how to *choose* or *qualify* a use
case. **Required fix:** a compact §3 concept and a "use-case qualification" table with the seven criteria,
plus the "abundant data, in the format needed, with permission to use it" clause, which is also the antidote
to the chapter's clean-data assumption. Repurpose the redundant Item 9 slot into a use-case-selection item.

**[MAJOR] Objective 2's "input" stage is uncovered** — the objective is literally "input → processing → output
→ feedback loops." The draft is rich on processing and feedback loops, thin on output, and silent on input:
no ingress normalization, no idempotency or deduplication, no request validation / cheap rejection of
malformed input, no PII redaction *before* the model, no document-to-text quality (OCR) even though S1 is a
scanned-document intake scenario where extraction accuracy is dominated by OCR, not by pattern choice. The
coverage table's Objective-2 row lists sections that are all about processing and loops. **Required fix:** an
input-stage concept with the four decisions (normalize / validate-and-reject / redact / dedupe-and-key) and
one output-stage concept (structured output, citation, confidence + **abstention**, action vs.
recommendation). Cheap in words, high in item yield.

**[MAJOR] Abstention and escalation-on-uncertainty are absent from the whole chapter** — "route low-confidence
outputs to a human instead of answering" is one of the highest-value architectural moves in the domain and a
very likely key for "what most reduces harm from wrong answers." The chapter has HITL only as an approval
gate in two scenarios, never as a confidence-triggered path. **Required fix:** add it to §4.5 as a placement
row and name the design decision (what signal, what threshold, what the user sees while waiting).

**[MAJOR] Objective 5's own taxonomy is never tested** — §3.8 calls choosing the wrong decomposition axis "the
most common error in this domain," and no item asks a candidate to pick the axis. Items 3, 8, 10 and 12 are
all about *multi-agent* decisions; none is about task vs. prompt-chain vs. context vs. tool decomposition.
**Required fix:** one new item where the correct answer is "decompose the tool surface" or "decompose the
context, not the task" and the distractors are the other three axes applied plausibly.

**[MAJOR] §9 Item 8 is trivia, not a scenario** — five product facts about subagents. The brief requires
scenario stems matching §8's cognitive level; all three of the guide's own samples are scenarios. Item 8 is
also the item most exposed to product drift. **Required fix:** convert to a scenario ("a team's reviewer
subagent keeps approving broken work and the parent agent re-does exploration the subagent already did —
which two mechanisms explain this?") or cut it and spend the slot on decomposition axes.

**[MAJOR] Answer-key length cue across the item set** — the keyed option is the longest option in Items 4, 5,
6, 11 (and arguably 1 and 9), and Items 12/8 are solvable by eliminating absolutes ("always," "reliably,"
"can message one another"). A candidate can score most of this set on test-wiseness, which inflates their
confidence and teaches nothing. **Required fix:** normalize option lengths to within ~15% within each item,
and move the reasoning from the keyed option into the rationale where it belongs.

**[MINOR] Redundant items** — Items 1 and 9 test the same discriminator (high volume + nobody waiting + cost
metric ⇒ batch) with near-identical reasoning, in a 12-item set covering six objectives. **Required fix:**
keep Item 1, repurpose Item 9's slot (Objective-1 use-case selection or the decomposition-axis item).

**[MINOR] Content below or beside exam altitude, and cut candidates given the 8.9k-word draft against a
3,500–6,000 target** — cut first: the tool-overhead token figures (286/354/496 — volatile, Domain 2/3,
low item yield); the session/harness/sandbox *naming* in §3.5 (keep the durability idea, which Item 5
tests); programmatic tool calling in §4.7 row 4 (Domain 3); §6 rows on cache hit rate, "passes eval fails in
production," and trajectory-vs-outcome grading (Domain 4 owns all three); the pass^k derivation (compress to
one clause). That frees roughly the space the Objective-1 and input-stage additions need.

**[MINOR] "Business value pillars" treatment** — the balance here is actually close to right: one `[UNVERIFIED]`
sentence plus a usable table beats either fabricating an Anthropic framework or hedging into uselessness.
The defect is narrower than "too much hedging": the **pillar → architecture** column is invented and
agentic-biased (see Item 11 above), while **pillar → metric** is defensible synthesis from [D01-S21],
[D01-S22] and [D01-S12]. **Required fix:** keep the hedge, keep pillar → metric, delete pillar → pattern,
and add the ordering rule the chapter is missing: *constraints decide feasibility; the pillar decides the
metric among feasible designs.* A named pillar never licenses breaching a constraint.

### Hidden assumptions

**[MAJOR] Team capability is never a design input** — S5 hands a coordinator plus four domain subagents to an
unspecified team; S6 hands them an orchestrator fleet. [D01-S21]'s own graduation criteria include
"operational readiness (system stability, support infrastructure, **team capability**)," and the dossier
records it. The MQC profile owns exactly this conversation. **Required fix:** add team maturity / operability
as an explicit axis in §4.2 and one "what changes it" clause: a team without agent observability, spend
caps, and eval infrastructure should not be handed a fleet, whatever the pattern table says.

**[MAJOR] Elastic budget and no capacity ceiling** — no scenario states a budget cap or a rate/throughput
limit, yet S3 (4M SKUs/month) and Item 1 (2.3M/month) are both organization-scale volumes where rate limits
and batch size caps (100,000 requests) are real design constraints. The chapter cites the 100,000 cap and
never applies it (2.3M/month needs chunking into ~1 batch/day). **Required fix:** one clause per
high-volume scenario turning the cited limit into a design consequence.

**[MINOR] Clean data / available labels / available eval set** — S3 asserts "95% attribute accuracy on a
held-out sample," Item 9 assumes stratified sampling capability, S1 assumes reconciliation ground truth in
core banking. None of the scenarios has to build its eval set first, and the dropped "abundant data… with
permission to use it" criterion is precisely the missing guard. **Required fix:** one scenario (or one "what
changes it") where the answer is "you cannot promise that number yet — build the labeled sample first, and
narrow scope to the slice you can measure."

**[MINOR] Greenfield, single jurisdiction, English corpus** — only S4 mentions an existing system; no scenario
is a brownfield integration or a multilingual intake (both are the norm in benefits and healthcare). **Required
fix:** flip one scenario to brownfield ("an existing rules engine and a 9-year-old queue you cannot replace")
— it costs nothing and it is the more common real situation.

---

## Agentic-bias audit

| Scenario | Simpler design considered? | Verdict |
|---|---|---|
| **S1** Loan intake | Yes — lands on routing + chain + code + batch, and explicitly rejects agent and orchestrator. Misses non-LLM routing (form ID / trained classifier) and buy-vs-build. | **BALANCED** |
| **S2** Prior authorization | Yes — the chapter's best scenario. Augmented LLM + rules engine + HITL; rejects agent on authority grounds and evaluator on cost/latency. This is the template. | **BALANCED** |
| **S3** Catalog enrichment | Partly — rejects agentic and orchestrator correctly, but never considers the two dominant cost levers (delta-only, family dedupe) or classical extraction. Simpler *than* agentic, not simple. | **BALANCED (under-optimized)** |
| **S4** Benefits eligibility | Yes — model brackets a deterministic core; explicitly rejects the three-agent split as problem-centric. One residual over-reach: a *generated* explanation in an appeals record where a template would do. | **BALANCED** |
| **S5** 26-tool support agent | **No.** Jumps to coordinator + subagents. Never considers tool consolidation (its own AP5), context editing / just-in-time retrieval (its own §6 row 1), dynamic per-turn tool allowlists, or human handoff for the billing domain — and the recommendation breaks the stated TTFT budget it used to kill the alternative. | **BIASED** |
| **S6** Competitive intelligence | **Barely.** Rejects "RAG plus one call" and "a fixed chain," but not the credible middles: curated connectors + batch retrieval + one long-context synthesis; analyst-in-the-loop source selection; parallel sectioning over the ten registries that actually matter (relegated to "what changes it"). Pillar note ("transformation justifies 3–10× tokens") is the bias stated as doctrine. | **BIASED** |
| **S7** Contract redlining | Partly — rejects an agentic loop on ground-truth grounds (good) and a per-section split (good), but skips the deterministic fallback-coverage check its own Item 4 mandates, going straight to an LLM evaluator loop. | **BIASED (mildly)** |
| **S8** Exception triage | Yes — 80% goes to a table lookup with *no model call*, which is the chapter's strongest anti-bias move. Misses retrieval-over-resolution-history and human triage for the 20%, and the agentic branch does not fit the stated 3-second budget. | **BALANCED** |
| §4 comparison set | Tier ladder starts at "augmented LLM"; no row for non-LLM code, an existing system, buy, cache/precompute, or human-in-the-loop. Every comparison is between LLM architectures. | **BIASED (by omission)** |
| §9 item set | Keys favor the simpler design in Items 1, 4, 5, 6, 7, 9 — genuinely good. But Item 11's key and Item 2's option set both encode the agentic reflex, and Item 12's C makes verifier ROI purely a model-capability question, ignoring blast radius. | **BIASED (2 of 12 keys)** |

---

## Item-by-item adversarial re-solve

**Item 1 (select 1) — key B.** Strongest alternative: none of A/C/D survives; the real threat is an
*unlisted* option — "deterministic keyword rules for the fraction of reports matching known meter-fault
strings, model only for the residue," which on a cost-per-report metric can beat B. **Verdict: SOUND** but
low-difficulty and keyword-shaped ("next-day" ⇒ batch). **Tightening:** replace D with a near-miss
("synchronous Haiku-class calls with caching at high concurrency") and add the rules-plus-residue option as
a distractor that loses only because the stem says the text is free-form with no stated pattern coverage.
Fix the rationale's "~4× chat token cost" misuse (see above). Batch+cache stacking → validator Q1.

**Item 2 (select 1) — key C.** Strongest alternative: a single agent with one federated search tool, which
satisfies "cannot predict which sources" completely and is what the chapter's own "start with single agents"
rule demands. It is not offered, so the item silently equates *unpredictable sources* with *multi-agent*.
**Verdict: UNDER-DETERMINED (and teaches the wrong reflex).** **Tightening:** add the single-agent option and
put the forcing constraints in the stem — per-question corpus exceeds one context window; 30+ sources must
be explored concurrently to hold the one-hour bound; a measured single-agent baseline missed it.

**Item 3 (select 2) — key A, C.** Strongest alternative: argue A justifies *tool consolidation*, not a
split — 24 endpoint-shaped tools is AP5 before it is [D01-S04]'s specialization signal, and the chapter
teaches consolidation-first in §4.7 and S5's "what changes it." B/D/E are clearly weak, so the key holds.
**Verdict: SOUND.** **Tightening:** add "after tool descriptions were consolidated and re-tested without
effect" to option A, which closes the only defensible objection. Also strengthen D's rationale (ownership
boundaries are a real maintainability concern — they are simply not a *context* boundary). Consider a
variant where a least-privilege containment option is **correct**, since the chapter currently excludes
security from its justification list.

**Item 4 (select 1) — key B.** Strongest alternative: "put the checklist into the generation prompt as a
required output section" — a prompt fix rather than a gate fix — but it is not offered and B dominates A/C/D
cleanly. **Verdict: SOUND.** Best item in the set; the "requirements are a one-page checklist" clause is the
right kind of stem signal. **Tightening:** length-normalize the options.

**Item 5 (select 1) — key B.** Strongest alternative: **C**, a retry wrapper, is what a competent architect
actually ships if crashes are rare — the stem says only "occasionally," and the question asks for the "most
direct" fix. At a 0.1% crash rate, restart is cheaper than building durable session state.
**Verdict: UNDER-DETERMINED (light).** **Tightening:** give a rate ("roughly one run in six fails
mid-execution") so restart's expected cost visibly exceeds the engineering cost of resumption.

**Item 6 (select 1) — key C.** Strongest alternative: **B** ("proceed but cap depth and concurrency") is a
correct action and a candidate reading "what do you tell them" procedurally can defend it; the rationale
handles the distinction well. **Verdict: SOUND** — and this is the one item that teaches the canonical
*measure the single model across its effort curve before adding architecture* ladder [D01-A01]. Protect it.
**Tightening:** the stem hands over both discriminators ("dependent chain," "fits comfortably in one
context"); make one of them inferable rather than stated to raise the cognitive level.

**Item 7 (select 1) — key B.** Strongest alternative: a candidate can argue step 1 (extract an order ID) is
*also* model-in-the-rule-table — an order ID is a pattern match or a lookup — so "the strongest criticism" is
arguably broader than step 2. The key still names the clearest instance. The rationale's claim that merging
"would remove the intermediate gates that make chaining valuable" asserts gates the stem never mentions.
**Verdict: SOUND** with a rationale fix. **Tightening:** convert to **select 2** with B plus "step 1 is a
pattern match against the order system, not a reasoning task" — that tests the reflex twice and removes the
ambiguity about which step is worst.

**Item 8 (select 2) — key A, D.** Two independent defects. (i) Option **E** ("subagents reduce total token
consumption relative to one agent doing the same work") is arguably **true** under its own stipulation: if a
single agent would have carried 50 turns of tool payloads in a growing context that is re-sent every turn,
isolating that subtask and returning a 1–2k-token summary can reduce cumulative prompt tokens — that is the
same economics the chapter uses to sell programmatic tool calling and context editing. [D01-S04]'s 3–10×
figure describes multi-agent systems doing *more* exploration, not the same work. A well-prepared candidate
can defend E, giving three defensible options for two slots. (ii) Option **C** ("inherits the parent's full
conversation history by default") is product-conditional: the rationale's own hedge ("a *non-fork* subagent
starts fresh") concedes that a documented forking mode inherits the parent's full context [D01-A03]. Plus
the item is pure recall in a scenario-based exam. **Verdict: DEFECTIVE.** **Tightening:** rewrite as a
scenario; replace E with a cleanly false claim about *wall clock* ("subagents always reduce end-to-end
latency," false for dependent work); scope C to the documented default and drop it if the qualifier cannot
be stated inside the option.

**Item 9 (select 1) — key B.** Strongest alternative: **A**, but its own justification ("so compliance can
spot-check as they arrive") is invented by the option and contradicted by the stem's "nobody consumes the
summaries interactively." **Verdict: SOUND** but redundant with Item 1 — same discriminator, same reasoning,
two of twelve slots. **Tightening:** repurpose the slot for Objective-1 use-case selection or the
decomposition-axis item, and if kept, drop the `custom_id` mechanics (Domain 3) in favor of the deadline-vs-
batch-tail reasoning.

**Item 10 (select 1) — key B.** Strongest alternative: an unlisted one — context editing / clearing stale tool
results, which the chapter's own §6 row 1 makes the *first* move before either compaction or reset. The stem
explicitly frames a binary ("is choosing between compaction and a context reset"), which legitimately
forecloses it. **Verdict: SOUND.** **Tightening:** add "after clearing stale tool results failed to restore
coherence" to the stem so the binary is earned rather than asserted.

**Item 11 (select 1) — key B.** See the BLOCKER above. B bundles a defensible claim (reframe the metric
around newly feasible work) with an indefensible one (therefore build agentic/multi-agent). A candidate
applying the chapter's own heuristic 2 can reject B, and a candidate accepting B learns "pillar ⇒ pattern,"
which will cost them items. **Verdict: DEFECTIVE.** **Tightening:** rewrite B to metric-only and add a
distractor that *is* the agentic over-reach ("commit to a multi-agent research platform so the analysts can
explore freely") so that choosing architecture from a pillar becomes the *wrong* answer — which is the
lesson the exam's own Sample 1 rationale implies.

**Item 12 (select 3) — key A, B, C.** The three keyed options are simply the three true statements; D and E
are eliminable by their absolutes ("always," "reliably"). It is a truth-identification item disguised as a
judgment item, solvable without reading the stem. Separately, **C** is over-stated: "worth the overhead only
when the task sits beyond what the current model does reliably solo" ignores **cost of error** — a pre-commit
gate on a production coding agent can be justified by blast radius even when the model is reliable solo, and
the chapter's own four-criterion gate lists cost of error [D01-S24]. So a sharp candidate can dispute a keyed
option. **Verdict: DEFECTIVE.** **Tightening:** make all five options plausibly true and ask for the three
*most decision-relevant*; rewrite C as "the gate's ROI depends on both model reliability on this task and
the cost of a bad commit reaching production."

**Tally: 7 SOUND · 2 UNDER-DETERMINED (2, 5) · 3 DEFECTIVE (8, 11, 12).** Two of the three
multiple-response items (8, 12) are defective, which matches the prediction in the task brief: in both
cases a listed option is defensible or a keyed option is disputable, and in both cases the item is solvable
by test-wiseness rather than reasoning.

---

## Missing alternatives

| Comparison / scenario | Omitted option | Why it matters (and why the exam could key it) |
|---|---|---|
| §4.1 tier ladder | **Non-LLM code / an existing system / buy** as tier zero | The ladder starts one rung too high. The exam's own Sample 1 rewards *removing* capability; an item whose key is "use the rules service you already own" or "this is a classifier with 10M labeled examples" is trivially writable. §4.8 has the prose ("don't use an LLM for this step") but only for a *step*, never for a use case. |
| §4.1 / §4.6 | **Raise `effort` on one model before adding architecture** | `VERIFIED-FACTS.md` names the docs' method — default → raise effort → then change model — and says to run an effort sweep on your own evals [D01-A01]. Domain 1's version is the anti-escalation ladder: prompt → effort → model → workflow → agent → multi-agent. Only Item 6 gestures at it; there is no named heuristic. An item pitting "add a verifier subagent" against "raise effort and re-measure" is very likely. |
| §4.2 single vs. multi-agent | **Dynamic per-turn tool allowlist** (one agent, code selects the tool subset by conversation phase) | Buys the specialization benefit at 1× tokens with no coordination surface. It is the missing middle column between "one agent with 26 tools" and "five agents," and it is the answer S5 should reach before splitting. |
| §4.2 | **Human handoff / escalation to a person** | The chapter treats humans only as approval gates. Routing a whole domain (billing) to a person is often cheaper and better than a subagent, and it is a standing exam key. |
| §4.2 | **Least-privilege containment as a justification** | Excluded from the three named justifications while appearing as a row in the same table. See the MAJOR above. |
| §4.3 pattern table | **Retrieval / lookup**, **cache or precompute**, **human-in-the-loop**, and **"one call with a better prompt"** rows | Four of the most common correct answers are not in the pattern table at all. Precomputation in particular is the classic answer to a hard p95 (convert a latency problem into a storage problem), and it is absent from the whole chapter. |
| §4.4 execution modes | **Precompute / materialize answers**; **respond-now-refine-async**; **queue shaping and backpressure**; **batch-tail mitigation** (smaller batches, sync fallback for stragglers) | The mode table is four rows of "when does the request run"; it omits "don't run the request." S8's own "what changes it" invents respond-now-refine-async ad hoc rather than teaching it. |
| §4.5 feedback loops | **Confidence-triggered abstention / escalation**; **stratified human audit sampling** (distinct from open-ended telemetry review); **shadow / parallel deployment** ([D01-S21], in the dossier, dropped from the draft) | Abstention is the highest-leverage harm-reduction move in the domain and appears nowhere. Parallel deployment is sourced Anthropic guidance that was researched and then lost. |
| §4.6 decomposition depth | **Don't decompose — raise effort or change model**; **decompose across time** (durable staged batches) rather than across agents | The table only ever answers "further or stop," never "a different axis entirely." |
| §4.8 pillars | **Risk / compliance** and **time-to-market** as drivers; **decline or narrow the scope** | A professional architect's most valuable output is sometimes "not this, or not yet, or only this slice." The chapter never models it. Narrowing to a reliably solvable slice is also the honest answer whenever the promised accuracy number has no eval set behind it. |
| S1 | Form-ID lookup or trained classifier for routing; commercial document-intake product; OCR quality as the real accuracy driver | Pattern choice is not the binding variable in scanned-document intake. |
| S3 | **Delta-only processing**; **dedupe to product families**; classical attribute extraction from supplier feeds | Both dominate the recommended levers by ~10× on the stated metric. |
| S5 | Tool consolidation; context editing / just-in-time order-history retrieval; dynamic tool allowlist; human handoff | The chapter prescribes the first two elsewhere for this exact symptom. |
| S6 | Curated connector set + batch retrieval + one long-context synthesis; analyst-in-the-loop source selection; provenance in the subagent output contract | The cheaper baseline the orchestrator design must beat is never priced. |
| S7 | Deterministic fallback-coverage check before any LLM critic | Item 4 teaches exactly this and S7 ignores it. |
| S8 | Retrieval over the resolved-exception history; human triage with a model-drafted brief | ~0-latency options for the 20% branch that cannot meet 3 seconds agentically. |

---

## Heuristic boundary conditions

| # | Heuristic as written | Qualifier it needs |
|---|---|---|
| 1 | Find the binding constraint — "a number with a unit" | Add the precedence order (legal / delegation of authority > hard SLA > quality floor > cost target) and note that constraints without numbers can bind hardest, while volume figures are sizing inputs, not constraints. |
| 2 | Simplest tier that satisfies the constraint wins | Define simple as "fewest parts to build, operate and maintain," not "fewest model-owned decisions," and add the repetition qualifier: determinism earns its build cost through volume. At low volume or on a long tail, one agent is the simpler system. |
| 3 | Enumerate the subtasks? Yes → parallelization; No → orchestrator | Enumerability of subtask **type**, not count. Known type + variable count = code-owned fan-out. |
| 4 | Who decides what happens next? | "Who decides the **sequence**." A model picking a branch from a fixed set, or picking content, is still a workflow. Reconcile with §3.3 so orchestrator-workers stays a workflow. |
| 5 | Multi-agent needs a named constraint (three) | Four: add least-privilege / blast-radius containment — and note it may be satisfiable by a per-call tool allowlist at 1× cost rather than by separate loops. |
| 6 | Decompose by context boundary, not job title | Except verification, which is legitimately split by role *because* independence of judgment requires a separate context and verification needs minimal context transfer. Also: when a job title genuinely implies a different corpus, it *is* a context boundary. |
| 7 | If a rule can express "correct," use the rule | Add "…and the rule set is stable and enumerable at acceptable maintenance cost." Note that rules fail silently and over-block; instrument the residue. |
| 8 | Self-critique is not a gate | Not the final gate for **subjective** quality. It still catches objective slips; it is just dominated there by a rules check. |
| 9 | Grade outcomes, not trajectories | Outcomes for quality; trajectories for **policy** — entitlement, irreversible actions, tool calls. Never grade the path for correctness; always check it for permission. |
| 10 | Nobody waiting → batch | …and no downstream deadline inside the 24-hour tail, and you can re-run or fall back to sync for stragglers. Also check retention/residency constraints. |
| 11 | Streaming buys perceived latency, not throughput | Correct as written — **preserve verbatim**. Add only that streaming is separately *required* above certain `max_tokens` (already in §3.10). |
| 12 | Cost is per completed task; the tail is where it lives | Correct — **preserve**. Add that published multipliers carry their own baselines and cannot be reused across units (see the §4.1 fix). |
| 13 | A more capable model is not a fix for a context or authorization problem | Correct and high value — **preserve**. Add the converse so it is not over-applied: for a pure *quality shortfall*, raising effort on the current model is the documented first move, before either a bigger model or more architecture [D01-A01]. |
| 14 | Free wins before trade-offs | "Free" = no quality cost, not no constraint cost. Caching constrains prefix stability and costs more on writes; batch changes your SLA class. |
| 15 | Match the metric to the pillar the stem names | Constraints decide feasibility; the pillar decides the metric **among feasible designs**. A named pillar never licenses breaching a constraint, and it never selects a pattern. |
| A4 | "Reread the stem for a number with a unit" | Reframe as constraint-typing, not number-hunting — otherwise it is the same keyword reflex the chapter is trying to inoculate against. |

---

## Must preserve

Three things the chapter gets genuinely right. It is ~8,900 words against a 3,500–6,000 target, so the
editor will cut hard; these must survive intact.

1. **The simplicity gradient as the organizing spine, plus the §2 distractor-archetype table and heuristics
   2/3/4.** This is correctly calibrated against the exam's own answer key: Sample 1 rewards removing a
   capability rather than logging or guarding it, and Sample 2 rewards reordering existing content rather
   than adding machinery. The archetype table (A1 complexity escalation, A5 model-everywhere, A6 pillar
   mismatch) is the most transferable page in the chapter. Cut examples if you must; do not cut the table.
2. **The four-decomposition-techniques taxonomy (§3.8), context-boundary-not-job-title (§3.9), and the
   stopping rules (§4.6).** This is the chapter's real differentiator over the third-party question banks the
   dossier surveyed, it serves the objective the exam will probe hardest, and it is fully source-anchored.
   It should *gain* an item, not lose words.
3. **The "model extracts, code decides, model explains" sandwich** — AP8, §4.8's "don't use an LLM for this
   step," and its applications in S2, S4, Item 4 and Item 7. This is the only reliable antidote to the
   model-everywhere distractor and the single most reusable architectural pattern in the chapter.

Also preserve: the §6 failure-mode table's symptom→first-check discipline (it doubles as a triage reference
and several rows are the only place an objective is operationalized); Item 4, Item 6 and Item 7 as items;
§4.2's explicit statement of baselines for the token multipliers; and the S2/S4/S8 pattern of putting a
deterministic core between model calls.

**Correct but suspicious-looking — do not "fix" these:**

- **"Claude Opus 5.5, default effort `medium`, $4/$20, released 2026-09-22; Opus 5 is legacy."** The course
  brief's own prose and the bundled skill's cached table say otherwise; `VERIFIED-FACTS.md` confirms the
  draft is right [D01-A01]. An editor working from memory will "correct" this backwards. Keep the model-
  currency note at the end of the chapter.
- **"Streaming changes TTFT and perceived latency; total generation time is unchanged."** Reads like a hedge;
  it is precise and load-bearing.
- **"Orchestrator-workers is a workflow."** Feels wrong because the model determines the split. It matches
  Anthropic's taxonomy. Explain it (see the BLOCKER); do not delete it.
- **"Multi-agent typically consumes 3–10× more tokens than single-agent" and "~15× a chat interaction."**
  Both are correct *with their own baselines attached*. Do not merge them into one number, and do not
  reuse either as a per-request multiplier.
- **"~1,000–2,000 token subagent summary"** and **"tool-use system prompt overhead 286/354/496 tokens."**
  Oddly specific but sourced. The summary figure is worth keeping; the overhead figures are the best
  candidate for the cut list on volatility grounds, not accuracy grounds.
- **"Batch results arrive in any order — key by `custom_id`"** and **"0.9^5 = 59%."** Both correct.
- **§3.12's efficiency-vs-cost distinction** ("a design can improve one and worsen the other"). Sounds like
  hair-splitting; it is the most answerable thing in the pillar section.

---

## Questions for the validator

These attacks depend on facts I did not verify; they are not asserted as findings.

| Q | Question | What depends on it |
|---|---|---|
| Q1 | Does prompt caching function reliably inside the Message Batches API (given arbitrary ordering and parallel processing against a short cache TTL), and do the 50% batch discount and the cache-read rate compose? | Item 1's and Item 9's rationales and S3's cost story all stack both discounts. |
| Q2 | Current cache-**write** price multiplier relative to base input, and per-model cache-read rates (VF gives 10% base / 5% Opus 5.5 / 2.5% Fable 5.1). | Whether caching may be called a "free win" without qualification (§4.8, heuristic 14). |
| Q3 | Message Batches: results retention/retrievability window, and any data-residency or retention interaction (including Covered Models / ZDR per VF). | Item 9's compliance framing and §4.4's "hard constraints" column. |
| Q4 | Are the tool-use system-prompt overhead figures (286 / 354 / 496) current for Opus 5.5, Sonnet 5 and Haiku 4.5 on 2026-09-24, and is [D01-S04]'s "20+ tools" still the only published signal? | §4.7 and AP5; both are cut candidates if stale. |
| Q5 | Does the Agent SDK document that a subagent starts with no inherited conversation history **by default**, and is there a documented forking mode that inherits the parent's full context? | Item 8 option C's key. This session's own Agent tool documents a `fork` type that "inherits your full conversation context" [D01-A03], which makes the option product-conditional. |
| Q6 | Does current Anthropic guidance still classify orchestrator-workers under **workflows** rather than agents? | The §3.3-vs-heuristic-3 contradiction and any Objective-3 item that asks a candidate to name the tier. |
| Q7 | Does [D01-S12] state the effort-before-architecture ordering explicitly, or is the ladder (prompt → effort → model → workflow → agent → multi-agent) our synthesis of [D01-S12] plus the models-overview sentence in VF? | Whether the new heuristic ships as sourced guidance or as labeled synthesis. |

---

## Sources introduced by this review

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|
| D01-A01 | VERIFIED-FACTS.md — canonical ground truth for Track B | (local) `../VERIFIED-FACTS.md` | Track B orchestrator, compiled from platform.claude.com | other (project canon over primary docs) | 2026-09-24 | primary (derived) | The `effort` parameter as the primary reasoning/cost control; the docs' "default → raise effort → only then change model" method and effort-sweep-on-your-own-evals guidance; Opus 5.5 current with default effort `medium`; per-model cache-read economics; Covered-Models/ZDR exclusivity. Basis for the missing-escalation-ladder finding and the model-currency preservation note. |
| D01-A02 | Claude Certified Architect – Professional Exam Guide v1.0, §6 objectives and §8 samples with rationale | (local) `../claude-arch-professional-guide.md` | Anthropic | exam-guide | 2026-09-24 | primary | The exam-reward standard used throughout: Sample 1's rationale (least privilege = remove the capability, not log or guard it), Sample 2's (reorder and cache existing content rather than add machinery), Sample 3's (diagnose the retrieval step, not the model). Also the scenario-stem cognitive level used to fault Item 8 as trivia. |
| D01-A03 | Agent tool specification as presented in this review session (documents a `fork` subagent type that inherits the parent's full conversation context, and that other subagent types start fresh) | (in-session tool specification) | Anthropic (Claude Code / Agent SDK surface) | vendor-docs | 2026-09-24 | secondary (in-session observation, not a fetched doc page) | Counter-example making Item 8 option C product-conditional. Flagged as validator Q5 rather than asserted as a documented default. |
