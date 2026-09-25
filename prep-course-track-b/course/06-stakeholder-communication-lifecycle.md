# Domain 6: Stakeholder Communication & Lifecycle Management

**Weight:** 14% of the exam — approximately 9 of 63 scored items [D06-S01].

**Objectives measured** [D06-S01]:
1. Conduct structured discovery and requirement gathering.
2. Communicate architectural decisions and trade-offs.
3. Manage stakeholder feedback loops and expectation alignment (including SLAs).
4. Document architectures and provide implementation guidance.
5. Support lifecycle phases (discovery, design, handoff, monitoring, iteration).

This domain does not test writing skill or interpersonal style. It tests whether you know the **named, established artifact or technique** for a given moment in a project's life, and can tell it apart from a plausible but wrong neighbor: a decision memo where an ADR belongs; an SLA where only an SLO is honest; a demo mistaken for a promotion gate. Items resolve on architecture and process, never on temperament — if an option wins because it "builds trust," it is not the key.

---

## 1. Exam-relevance framing

The MQC runs discovery, writes the trade-off record, negotiates the commitment, and hands a probabilistic system to a team that did not build it. Stems are scenarios ending in "what should the architect do first / next / instead," rarely definition recall.

**Recurring distractor archetypes:**

1. **The eloquent-but-wrong document** — an architecture document where an ADR belongs, or where an auditor wants control evidence. Tests artifact-to-audience matching.
2. **The unfalsifiable commitment** — "99% accuracy," "no hallucinations." Tests whether a quality commitment is quantified over a disclosed, versioned, sampled input domain.
3. **The demo-as-evidence trap** — a curated pilot treated as grounds for rollout. Tests whether you require a graded sample of real traffic first.
4. **The false binary on automation** — full autonomy or nothing. Tests whether you reframe on reversibility tiers.
5. **The premature scope answer** — a technical fix for an unanswered discovery question (no baseline, no named accuracy owner, no reversibility answer).
6. **The ownerless handoff** — "monitor performance," with nobody accountable for the SLO or for approving prompt changes.

**What this domain does not own.** Eval-set construction, judge validation and monitoring tooling are Domain 4; the HITL control mechanism and regulatory compliance are Domain 5; pattern and model selection are Domains 1–2; tool scope and authorization are Domain 3. Domain 6 owns the stakeholder-facing face of each: the eval **gate** as a promotion decision, the eval **report** as the artifact someone signs, the review posture as a **commitment that can grow**, and the discovery answer that gates the pattern choice.

---

## 2. Core concepts

**Structured discovery.** A facilitated session eliciting measurable quality-attribute scenarios (stimulus → measurable response) before an architecture exists — the ATAM utility-tree lineage [D06-S16] in its lightweight mini-QAW form [D06-S17]. Unstructured discovery returns untestable adjectives; this technique decides whether any acceptance criterion can be written at all (§3.2). Misconception: that discovery is a kickoff event rather than a technique re-run at every scope change.

**Discovery answers and what each changes** [D06-S16, D06-S17, D06-S04, D06-S13, VF]:

| Question | What the answer changes |
|---|---|
| Volume, peak concurrency | Batch vs. real-time, caching, cost model — a *parameter*, not the pattern |
| Latency tolerance | Model tier, streaming, workflow vs. agentic (Domains 1–2) |
| Accuracy bar **and who defines it** | Whether an eval set with a named owner must exist before build; whether legal or the business owner signs the threshold, not engineering alone |
| Cost ceiling | Caching and batching first, then tier; whether a cascade is justified (Domain 2) |
| Data sensitivity, residency | Deployment surface, retention, pre-prompt redaction — and it can eliminate a model: ZDR eligibility excludes Covered Models, so "we require zero data retention" and "we want the Mythos-class model" cannot both hold [VF] |
| Reversibility of automated actions | Whether approval must *precede* the action [D06-S04]; tool write-scope |
| Human review capacity | Review posture (§3.5) and whether the proposed commitment is achievable |
| Integration surface | MCP vs. bespoke API vs. agent-to-agent (Domain 3); auth model |
| Success metric and its **baseline** | Whether "improvement" is measurable at all (§3.2) |
| Release authority; which review or consultation bodies must be engaged | Whether the architect can gate the launch (§3.9). Some jurisdictions add a staff-consultation body for rollouts that change how people work `[UNVERIFIED]` — ask, do not assume |

Most answers set **parameters**. Four change **structure**: reversibility (does an approval step exist), data sensitivity (surface and retention), the accuracy owner (is an eval gate a precondition), and the baseline (is a commitment possible).

**Jobs to Be Done** [D06-S18]. The progress the stakeholder is hiring the system for, distinct from the feature requested; building the literal request over- or under-scopes the system. Misconception: that "what do you want?" surfaces the job — it surfaces the request. Domain 1 owns translating job to pattern; Domain 6 owns the elicitation and its signed record.

**Use-case qualification, including "no."** Rank candidates on value × feasibility × **evaluability** × **reversibility**; the last two are the LLM-specific axes, and neither MoSCoW [D06-S19] nor value-vs-effort or RICE scoring [D06-S20] contains them. MoSCoW still earns its place as the artifact that later proves something was explicitly out of scope. Three discriminators say *not this system, or not yet*: (a) the job needs deterministic, independently recomputable, auditable output — a rules engine wins, and the documented default is to start simple and add complexity only when a simpler approach demonstrably falls short [D06-S02]; (b) reversibility is low and review capacity is near zero [D06-S04]; (c) no baseline or success metric can be defined, so no gate can ever run. Practitioner "kill criteria" — no path to a baseline, a known blocker unresolved across several review cycles, no nameable accountable business owner — are directional consulting convention, not documented doctrine [D06-S26].

**Baseline.** The incumbent measured **on the same eval set with the same grader** the new system will face, by a named owner, before design freeze. A before/after across different sets or graders is not a comparison, and the baseline is also how a threshold gets derived (§3.2). Misconception: assuming the current process is obviously near-perfect without measuring it either.

**ADR** [D06-S09, D06-S10]. A short record of one architecturally significant decision: Title, Status, Context, Decision, Consequences. Immutability stated precisely: **the Context and Decision of an accepted ADR are never rewritten; only Status changes**, to Deprecated or "Superseded by ADR-MMM" [D06-S09]. Significance threshold: write one when the decision is costly to reverse or when someone outside the room will later ask why — not for a two-week throwaway with a scheduled sunset. Override: a regulated quality-management system or the contract may prescribe the artifact set. Misconception: that an ADR persuades — it records a decision already made, including its downsides.

```
# ADR-NNN: <short noun phrase>
## Status        Proposed | Accepted | Deprecated | Superseded by ADR-MMM
## Context       Forces at play, stated neutrally. Include the discovery answers that
                 drove this: volume, latency bar, accuracy bar and its owner, cost
                 ceiling, data sensitivity/residency, reversibility of the actions.
## Decision      "We will ..." — one primary decision per ADR.
## Alternatives  Option | Why rejected (measured eval delta, or cost of re-deciding later)
## Consequences  Positive and negative, including what this forecloses.
```

**RFC / design doc** [D06-S23, D06-S24]. A pre-decision proposal circulated to solicit disagreement — context, goals, non-goals, design, alternatives considered, cross-cutting concerns [D06-S23]. Contested consequential decisions take two steps: RFC before commitment, ADR after. Misconception: treating them as one document at two times.

**Notations and their limits.** C4 is diagram *notation* at four zoom levels — system context, container, component, code [D06-S11]. arc42 is a 12-section prose *template* for a full architecture document (goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting concepts, decisions, quality requirements, risks, glossary) [D06-S12]. They compose. Neither is audit evidence: an auditor wants a **control-evidence package** — data-flow diagram, data classification and retention configuration, subprocessor list, access-control evidence, approved-change record — with the C4 context diagram attached [D06-S07].

**SLI / SLO / SLA / error budget** [D06-S13]. An SLI is a measured indicator; an SLO a target *range* (never 100%); an SLA an SLO plus an external, usually financial consequence — no explicit consequence means you have an SLO, not an SLA; the error budget is `1 − SLO target`, and its exhaustion throttles release pace. **Attribution note:** that source defines these for infrastructure signals and does not discuss LLM or eval-derived indicators. Everything below that applies error-budget mechanics to a *quality* SLI is this course's adaptation, not documented SRE practice.

**Quality SLO and the eval gate.** The adaptation: define the SLI as the pass rate of a versioned eval suite on a **production-representative sample** — drawn from production traffic over a stated window, stratified by task type and channel, with known failure classes deliberately included, re-drawn on a cadence — and require a documented threshold before a phase transition [D06-S03, D06-S06]. Breach mechanics: exhaustion freezes **prompt and model changes**, not feature work; the SLO's accountable role lifts the freeze; the review cadence is the burn-rate proxy. A second SLI is often the better offer to a stakeholder: the **automation rate**, tracked and *grown* as the budget proves out [D06-S05]. Misconception: that one launch-time eval run suffices — the suite is a living artifact maintained as routinely as unit tests, fed primarily by production failures and the support queue [D06-S03]. Domain 4 owns how sets and graders are built.

**Accountability that survives an audit.** RACI assigns exactly one Accountable party per responsibility [D06-S21]. For a 24/7 system the object is one accountable **role** with a named current holder and a documented escalation path: "the platform team's service owner of record, currently J. Okafor, escalating to the platform director" passes; "the team owns it" fails because it names no role. RACI has no single documented origin — cite it as established convention, not a named framework [D06-S21].

**The operating artifact set.** Beyond the architecture document, a running feature depends on: the **runbook** (per-scenario action, including rollback, so on-call does not depend on the author) [D06-S22]; the **eval report** (method, sample, date — the artifact a stakeholder signs); the **prompt/model change log** (what changed, when, against what eval delta, and *which ADR it implements* — which makes the log the ADR index); the **integration guide** for consuming teams (input contract and its stability guarantees, tool schemas, auth, rate and quota expectations, the documented fallback, and where the eval set and threshold live so a consumer can tell whether their use case is inside the tested distribution); and the **handoff checklist** (accountable role, on-call, cost owner — spend caps and usage analytics are administrable [D06-S08] — and pre-declared re-eval triggers).

---

## 3. Trade-off analyses

### 3.1 Which artifact for which need

| Need | Artifact | What the plausible wrong artifact loses |
|---|---|---|
| Fund Option A over B (non-technical approver) | One-page decision memo | An architecture document buries the ask; an ADR is not written to persuade |
| Record why RAG lost to long context | ADR [D06-S09] | An RFC thread is archived and lost; nothing means silent re-litigation |
| Solicit disagreement before committing | RFC / design doc [D06-S23, D06-S24] | Jumping to an ADR loses the alternatives record and the buy-in |
| Give engineers the whole system | C4 + arc42 [D06-S11, D06-S12] | An ADR log alone is decisions with no map of how they compose |
| Satisfy a compliance auditor | Control-evidence package + C4 context diagram [D06-S07] | arc42 is architecture context, not evidence; it answers no request-list line item |
| Prove the quality bar to the approver | Eval report | A demo is not reproducible; verbal assurance is not auditable |
| Tell on-call what to do at 3am | Runbook [D06-S22] | An architecture document is context, not action |
| Let another team integrate safely | Integration guide | A repo link makes every integrator reverse-engineer the contract and the tested distribution |
| Transfer ownership | Handoff checklist + RACI | A walkthrough meeting leaves no record of who is accountable |
| Correlate a regression with a change | Prompt/model change log | Git history has no eval delta and no ADR reference |

**Discriminator:** classify the need as persuasion, record, reference, evidence, or action. The mapping is many-to-many over time — one contested regulated decision legitimately produces RFC → ADR → architecture-document update → memo. Two questions settle it for a concrete decision: who must approve it, and must the reason survive the author's departure? For "we chose Sonnet 5 over Fable 5.1 for tier-1 triage," that is a named engineering owner and yes — so an ADR, not a memo.

### 3.2 Worked: turning "it must be accurate" into a committable criterion

The vague ask is the stakeholder's sentence: *"The claim summaries must be accurate."* Six moves make it falsifiable.

1. **Name the task class and the failures that matter.** Two, not one: an *unsupported fact* (a policy limit, date of loss or name not present in the file) and a *material omission* (an exclusion that changes the outcome). Their costs differ, so they are graded separately.
2. **Define the eval set, versioned.** `claims-summary-v3`: 120 cases from 90 days of production traffic, stratified by line of business and intake channel, with each of 14 known failure classes represented at least 3 times. That is what **production-representative** means operationally — stated window, stated stratification, known failure classes forced in, re-drawn on a cadence. Not "some real examples."
3. **Name the grader.** Programmatic assertion for the six extractable fields; rubric grading for material omission, with an LLM judge used only after calibration against a human-adjudicated slice. Judge construction and calibration are Domain 4.
4. **Make the metric a per-case pass.** A case passes with zero unsupported facts *and* no material omission; the SLI is the share passing. A composite pass rule stops a high average from hiding a class that fails completely.
5. **Derive the threshold — never assert it.** Measure the incumbent on the same set with the same grader: suppose 88%. Floor at the incumbent (do no harm); set the target above it (say 93%) using cost asymmetry — an unsupported limit costs a rework loop, a missed exclusion can cost a wrong payment, so recall carries more weight. Floor-to-target is the error budget. State n and the run-to-run variance across three repeat runs, and refuse to report a difference smaller than that variance. **No primary source fixes a minimum sample size or confidence interval for calling an improvement real** `[UNVERIFIED]`, so the honest artifact states n and variance rather than a bare percentage. (88 and 93 are this example's own numbers, not measured facts.)
6. **Attach cadence, owner, consequence.** Re-measured on every prompt or model change and monthly on a fresh draw; one accountable role owns set and number; below floor, prompt and model changes freeze until root-caused, and a second consecutive breach turns on the fallback path for the affected stratum.

Output: one sentence a stakeholder signs and an auditor checks — *"≥93% case pass rate on `claims-summary-v3` (120 production-sampled cases, stratified, grader documented); floor 88% = measured incumbent; re-measured on every model/prompt change and monthly; owned by the claims-platform service owner of record; below floor, prompt and model changes freeze."* Every clause is one of the six moves. This is the transformation the domain keeps asking for; it is not a slogan about measurability.

### 3.3 What can and cannot be committed

| Commitment | Committable? | What makes it falsifiable, or why it is not |
|---|---|---|
| Availability / uptime | Yes, as an SLA | Infra measurement, independent of model behavior |
| p95 / p99 latency | Yes | Measured continuously on the serving path |
| Pass rate on a disclosed, versioned corpus | Yes as an SLO; as an SLA with a remedy | Input domain disclosed, sampled, versioned; threshold derived per §3.2; needs a re-measurement trigger |
| Human-review turnaround (e.g. 95% within 4 business hours) | Yes | A capacity commitment — often the right thing to offer a client demanding an accuracy number |
| Throughput / concurrency | Yes | Capacity, measurable |
| Degradation behavior | Yes, **if the trigger is named** | "Cases flagged by <named detector> route to review, with the detector's recall and the abstention rate on corpus v7 disclosed and re-measured on model change" |
| Re-measurement and distribution-shift terms | Yes — and load-bearing | Who re-measures after a model change, who pays, what happens when the corpus stops matching traffic. The most-often-missing term in an LLM quality contract |
| Fixed accuracy on arbitrary future input | No | No corpus covers "any input"; breached by the first unseen class |
| "No hallucinations" | No | Describes a property the system does not have |

**Discriminator:** if the commitment can be evaluated against a specific, disclosed, versioned dataset with a stated cadence, it is committable as an SLO — and as an SLA if a contractual consequence is attached. If it can only be evaluated against "whatever the user happens to ask," it is not committable; reframe as a band plus a degradation path.

**The number is not the problem; the input domain is.** A numeric quality KPI with a remedy is sometimes a procurement precondition, and the correct response is to *scope* it rather than refuse it: "≥94% field-level accuracy, measured quarterly on a stratified 500-document sample from the client's own corpus, re-measured on any model or prompt change, with document classes absent from the corpus excluded in writing" is a promised percentage in a contract and it is defensible. "95% accuracy" with no corpus, cadence or exclusion is not. Specify the remedy too — credits, rework, or a cure period — because an unspecified remedy turns the first miss into a dispute.

**Unmeasured self-confidence is not a trigger.** A model response carries no calibrated confidence by default, so "falls back when confidence is low" ships as a clause and fails as a control. Legitimate triggers: judge score below threshold, retrieval top-k score below threshold, explicit abstention in the output, disagreement between two models in a cascade, or a schema/validator failure. The degradation ladder, in order: primary path → cheaper or smaller fallback model, or a cached/templated response → an explicit "we cannot answer this confidently" shown to the user. The last rung matters most: **fail visibly, not silently** — and put the ladder *in* the commitment as the defined behavior when the primary path cannot meet its SLO.

### 3.4 One trade-off, four audiences

The substance — a single trade-off table — does not change across audiences; only the foregrounded row does [D06-S15].

| Audience | Lead with | What stays fixed | Who signs |
|---|---|---|---|
| Executive / CFO | The decision, and the rejected alternative's cost in dollars, time, risk | The business outcome being bought | Funding |
| Security / legal | The pillar **not** traded, plus residual risk after controls | Classification, residency, retention, egress | The classification and retention answer |
| Engineering | The mechanism and the ADR, with the measured eval delta on the rejected option | Interfaces and the eval threshold | The implementation plan |
| Operating team | The runbook path, the rollback, what freezes on breach | The accountable role and on-call | The handoff checklist |

**Discriminator:** security and operational excellence are generally not traded away against the other pillars [D06-S15], so an option that trades either for cost or speed is wrong regardless of the pressure behind it — and an option that *hides* a trade-off is wrong even when the chosen option is right, because pillar trade-offs are inevitable business decisions that must be documented [D06-S15].
