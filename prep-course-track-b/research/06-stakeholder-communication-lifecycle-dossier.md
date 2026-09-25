# Domain 6 Research Dossier — Stakeholder Communication & Lifecycle Management (14%)

Sources cited as `D06-Sxx`, resolved in `06-stakeholder-communication-lifecycle-sources.md`. Model/pricing facts (where they appear) were checked via the `claude-api` skill (cache dated 2026-06-24) per AGENT-BRIEF — current lineup: Opus 5, Sonnet 5, Fable 5.1, Haiku 4.5.

## Objective 1 — Conduct structured discovery and requirement gathering

**What actually changes the architecture.** Discovery is not a form-filling exercise; it's a small set of questions whose answers gate architecture-pattern choice, model choice, and go/no-go. Established techniques converge on this being workshop-based and quality-attribute-led, not a requirements document handed over the wall:

- **Quality Attribute Workshop / mini-QAW** [D06-S17], derived from ATAM's utility-tree method [D06-S16] — bring stakeholders together *before* an architecture exists, elicit quality-attribute *scenarios* (stimulus/response, measurable), not adjectives ("fast", "accurate"). This is the direct ancestor of "turn 'it must be accurate' into a measurable acceptance criterion."
- **Jobs to Be Done** [D06-S18] — separates the stated request ("build me a chatbot") from the underlying job ("reduce time-to-first-response on tier-1 tickets without increasing headcount"). The architectural implication: designing to the stated request over-scopes (a general chatbot) when the job wants a narrow workflow automation.
- **MoSCoW** [D06-S19] and **value-vs-feasibility / RICE** [D06-S20] — force an explicit, revisitable scope boundary before build starts, which is the artifact that prevents "scope creep" later (Objective 3).

**Discovery question bank organized by what each answer changes** (synthesized from ATAM/QAW quality-attribute elicitation [D06-S16, S17], Anthropic's agentic-misalignment guidance on irreversibility [D06-S04], and Google SRE SLO practice [D06-S13]):

| Question | What it changes if the answer is "high/hard" |
|---|---|
| Volume (requests/day, peak concurrency) | Batch vs. real-time API; whether prompt caching/priority tiering matters; cost model |
| Latency tolerance (sync UI vs. async batch) | Model tier (Opus vs. Sonnet vs. Haiku), streaming vs. non-streaming, workflow vs. agent pattern |
| Accuracy bar, and **who defines it** | Whether an eval set with a named owner must exist before build; whether legal/compliance must sign the threshold, not engineering alone |
| Cost ceiling (per-request and aggregate) | Model tier, prompt length/caching strategy, whether a cascade (cheap model first) is justified |
| Data sensitivity / residency | Deployment surface (first-party API vs. Bedrock/Vertex/on-prem), retention settings, whether PII must be redacted pre-prompt |
| Reversibility of automated actions | Whether human-in-the-loop approval gates the action (irreversible ⇒ mandatory approval per [D06-S04]); blast radius of tool scope |
| Human capacity for review | Sampling rate for QA, whether 100% review is even possible (drives SLA realism, Objective 3) |
| Integration surface (systems Claude must read/write) | Tool/connector count, auth model, MCP vs. bespoke API vs. agent-to-agent |
| Success metric and its **baseline** (current system or human performance) | Whether "improvement" is even measurable; prevents promising gains against no baseline |

**Detecting a use case that should not be an LLM use case.** No single named framework owns this, but the discriminators are consistent across sources: (a) the "job" needs deterministic, auditable, 100%-repeatable output (tax calculation, not summarization) — a workflow/rules engine wins; (b) reversibility is low and human review capacity is near zero (e.g., autonomous trading) — the risk profile fails the agentic-misalignment guidance [D06-S04] outright; (c) there is no way to define a baseline or success metric — you cannot run an eval gate (Objective 3/5), so you cannot govern quality at all. Anthropic's own agent-design guidance is explicit that the default should be *not* agentic, or not LLM-based at all, and complexity is added only when a simpler deterministic approach demonstrably falls short [D06-S02].

**Qualification criteria that kill a bad project early** — practitioner material (low trust, [D06-S26]) converges on: no path to a baseline/eval, a known infra/data blocker unresolved across multiple review cycles, and inability to name an accountable business owner. These are directionally useful but not citable as an "Anthropic-endorsed" checklist — treat as reasoning, not doctrine.

## Objective 2 — Communicate architectural decisions and trade-offs

**The documentation hierarchy (this is the trade-off spine).**

| Artifact | Scope | Written when | Audience | Durability |
|---|---|---|---|---|
| One-page decision memo | One decision, framed for a go/no-go | Before or at a decision point needing non-engineering sign-off | Executive/business, sometimes legal | Point-in-time; superseded by the ADR once decided |
| ADR (Nygard format: Title/Status/Context/Decision/Consequences) [D06-S09, S10] | One architecturally significant decision | At the moment the decision is made | Engineering, future maintainers, auditors | Permanent, immutable, superseded-not-edited |
| RFC / design doc [D06-S23, S24] | A proposal, pre-decision | Before committing, to solicit disagreement | Engineering peers, senior reviewers | Discarded or converted into ADR(s) once decided |
| Full architecture document (C4 [D06-S11] + arc42 [D06-S12]) | The whole system | Once, then living | Engineering across teams, new hires, security/compliance reviewers | Living document, revised on major change |

Key discriminators:
- **ADR vs. decision memo**: an ADR records *that a decision was made and why*, for people who will later ask "why did we do it this way?" — it is not written to persuade. A decision memo *is* written to persuade/inform a non-technical stakeholder who must approve or fund something. Same decision can produce both: memo first (persuasion), ADR after (record).
- **C4 vs. arc42**: C4 is a *notation* for diagrams at four zoom levels (context/container/component/code) [D06-S11], answering "which diagram for which audience." arc42 is a *document template* with 12 sections (goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting concepts, decisions, quality, risks, glossary) [D06-S12] — it tells you what prose sections a full architecture document needs, independent of diagram notation. They compose: C4 diagrams populate arc42's "building block" and "context" sections.
- **Design doc/RFC vs. ADR**: an RFC is "structured disagreement before commitment" [D06-S24]; an ADR is the record after commitment. Skipping the RFC and going straight to ADR loses the alternatives-considered discussion; skipping the ADR after an RFC loses the durable "why" once the RFC thread is archived.

**Audience-tailored framing without changing substance.** AWS Well-Architected is explicit that pillar trade-offs are *inevitable business decisions* that must be made and documented, not hidden — "security and operational excellence are generally not traded away" against the others [D06-S15]. This gives a concrete tailoring rule: to an executive, lead with the decision and the cost of the rejected alternative in dollars/time/risk; to security/legal, lead with the pillar that was *not* traded (what stayed fixed) plus the residual risk; to engineering, lead with the mechanism and the ADR. The substance (the actual trade-off table) does not change across audiences — only which row is foregrounded.

**Trade-off table over recommendation-only narrative.** This is reinforced by every source in this cluster (ADR "Consequences" section, arc42 "Decisions" section, Google design docs' "Alternatives Considered" [D06-S23], AWS Well-Architected's pillar table [D06-S15]) — the common failure mode named across all of them is documenting *only* the chosen option, which erases the ability to answer "why not X" later and makes the decision look arbitrary on audit.

## Objective 3 — Manage stakeholder feedback loops and expectation alignment (including SLAs)

**SLI/SLO/SLA adapted to a probabilistic feature.** Google SRE's formal stack [D06-S13]:
- SLI = a measured indicator (latency, error rate, throughput, availability — and for an LLM feature, a *quality* score from an eval/judge).
- SLO = a target *range* for that SLI (not a point, not 100%).
- SLA = the SLO plus an external, usually financial, consequence for missing it. "If missing targets has no explicit consequence, you have an SLO, not an SLA" [D06-S13].
- Error budget = `1 − SLO target`; while budget remains, the team ships; when it's exhausted, work shifts to reliability, and *this same governance mechanism is what should throttle model/prompt changes* against a quality SLO, not just infra changes.

**Applying this to quality (not just latency/availability):** the architectural move is to define a quality SLI from the eval suite's pass rate against a production-representative sample [D06-S03], set an SLO as a *band* (e.g., "≥92% pass rate on the standing eval, reviewed weekly"), and treat any drop below the floor as budget exhaustion that halts further prompt/model changes until root-caused — exactly the SRE release-pace mechanism [D06-S13] transposed onto prompt/model releases, and directly consistent with the AI-Native SDLC playbook's framing of the eval suite as "the AI-native equivalent of stage-gate QA" [D06-S06].

**What you can and cannot contractually commit to.** You can commit to: availability/uptime of the serving path, p95/p99 latency, a *measured quality band* on a defined, disclosed eval set, and a defined degradation/fallback behavior when the primary path fails. You cannot honestly commit to a fixed accuracy percentage on inputs the eval set hasn't seen, "no hallucinations," or a static number that a model/prompt update won't move — because a change to the model or prompt can shift the SLI, which is why the SLO must be re-validated against the eval suite on every material prompt/model change, not assumed stable [D06-S03, S06].

**Graceful degradation and fallback** — the practitioner pattern (moderate-trust, general-purpose but consistent with Anthropic's own agent-simplicity stance [D06-S02]) is: primary model → smaller/cheaper fallback model or cached/templated response → explicit "we can't answer confidently" surfaced to the user rather than a silent wrong answer. This belongs in the SLA as *what happens when the primary path can't meet its SLO*, not as an afterthought.

**Expectation management — demo-to-production gap.** The pattern (directional, low-trust sourcing on specific stats [D06-S25], but structurally consistent with Anthropic's own agent-scaling guidance [D06-S02, S05]): pilots succeed because they run on curated data, narrow scope, and heavy human review — exactly the conditions production removes. Anthropic's own Cowork enterprise guide independently prescribes the antidote: pilots are explicitly time-boxed and scoped (Month 1 = 2-3 champion teams reach Level 1; Months 2-3 = build/schedule; Months 4-6 = department-wide), with a pre-scale security review and a named leading indicator (number of champion-authored, reusable skills) rather than "it worked in the demo" [D06-S05]. The generalizable move: **the promotion criterion from pilot to production is a documented eval-gate pass rate against a production-representative sample, not stakeholder enthusiasm from a curated demo.**

**The "100% automation" stakeholder.** The architecturally correct response is not "yes" (dishonest, sets up SLA breach) or "no" (reads as obstruction) — it is to reframe the ask around reversibility and error budget: fully autonomous where actions are reversible and cheap to fix, human-in-the-loop where actions are irreversible or high-blast-radius [D06-S04], with the automation rate itself tracked as an SLI that can be *grown* over time as the error budget proves out — mirroring the Cowork maturity ladder's explicit "nobody needs to reach Level 4 in the first month" framing [D06-S05].

## Objective 4 — Document architectures and provide implementation guidance

**Documentation set and audiences** (compiled across D06-S09–S12, S22–S24, S06):

| Document | Purpose | Primary audience | Cost of skipping it |
|---|---|---|---|
| Architecture document (C4 + arc42) | Whole-system shared understanding | Engineering org, new hires, auditors | Tribal knowledge; every onboarding re-derives the design from code |
| ADR log | Durable record of *why*, decision-by-decision | Future engineers, auditors, incident responders | Decisions get silently re-litigated or reversed by someone who didn't know the original context |
| Runbook [D06-S22] | Step-by-step operational procedure (what to do when X happens) | On-call/operations | 3am incidents depend on the one engineer who remembers how it works |
| Eval report | Evidence the system meets its quality bar, with method and sample | Stakeholders approving promotion, compliance/legal | Promotion decisions become "it felt fine in the demo" |
| Prompt/model change log | Versioned record of what changed, when, and against what eval delta | Ops, evals owner, auditors | No way to correlate a quality regression with a specific change; SLO governance (Objective 3) becomes impossible |
| Integration/implementation guide | How to call/extend the system (APIs, tools, auth) | Downstream engineering teams | Every integrator reverse-engineers the contract independently |
| Handoff checklist | Confirms ownership, on-call, cost owner, retraining triggers are assigned | Operating team taking over from the build team | System ships with no one accountable when it breaks |

**ADR template (reusable artifact, Nygard format [D06-S09] plus MADR's optional fields [D06-S10]):**

```
# ADR-NNN: <short noun phrase>

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-MMM

## Context
The forces at play (technical, business, regulatory, timeline) stated neutrally.
Include the discovery answers that drove this decision (volume, latency bar,
accuracy bar + owner, cost ceiling, data sensitivity, reversibility).

## Decision
"We will ..." — stated in active voice, one primary decision per ADR.

## Alternatives considered
Option | Why rejected

## Consequences
Positive and negative, including what this forecloses later.
```

**Gate checklist (reusable artifact) — what must be true to pass each lifecycle gate**, synthesizing the AI-Native SDLC playbook's artifact-driven, human-accountable phase model [D06-S06] with Google's production readiness review practice [D06-S14] and the Cowork guide's pilot structure [D06-S05]:

| Gate | Must be true to pass |
|---|---|
| Discovery → Design | Discovery question bank answered and signed off by a named business owner; baseline/success metric defined; use case has not tripped a kill criterion |
| Design → Build | ADR(s) exist for the architecture pattern, model choice, and data-handling approach; security/legal have seen the data-sensitivity answer, not just the final build |
| Build → Eval gate | An eval set exists, sourced from real tasks/failures (20-50 to start) [D06-S03], with a named owner and a documented pass-rate threshold |
| Eval gate → Pilot | Eval suite passes the agreed threshold on a held-out or production-sampled set; rollback path rehearsed [D06-S06] |
| Pilot → Production | Pilot ran on a defined cohort/timeframe with a pre-declared success signal (not enthusiasm); security/compliance review completed before scale, not after [D06-S05] |
| Production → Monitoring | SLOs (availability, latency, quality) published; error budget policy defined; on-call/runbook exists |
| Monitoring → Iteration | Production samples are being fed back into the eval set on a cadence; a named owner triages feedback into a prioritized backlog, not ad hoc prompt edits [D06-S03, S06] |
| Iteration → Deprecation | Retraining/re-eval triggers defined in advance (e.g., model version change, data drift signal, SLO breach) trigger a scheduled review, not silent decay |

## Objective 5 — Support lifecycle phases (discovery, design, handoff, monitoring, iteration)

**Lifecycle model.** Two independently-sourced Anthropic lifecycle framings converge on the same shape: the Cowork enterprise guide's Evaluate (month 1) → Pilot (months 2-3) → Scale (months 4-6) arc for organizational adoption [D06-S05], and the AI-Native SDLC playbook's Plan → Design → Build → Test → Deploy → Maintain arc for a single system, where "a stage ends by committing an artifact the next stage can read" and progression is gated by an eval suite rather than a manual sign-off ceremony [D06-S06]. Composited for a single Claude-based feature: **discovery → design → build → eval gate → pilot → production → monitoring → iteration → deprecation.**

**Handoff to an operating team.** The AI-Native SDLC playbook's ownership model is directly reusable: product owner signs off on requirements, engineer approves the implementation plan, code owner approves changes despite AI-generated findings, release manager authorizes production deployment (enforced by a hook — a technical control, not a policy on paper), and service owner triages monitoring findings before further changes ship [D06-S06]. This maps cleanly onto a RACI [D06-S21] for a Claude feature: who is *Responsible* for prompt/model changes, *Accountable* for the SLO, *Consulted* on data-sensitivity questions (security/legal), and *Informed* of production incidents (business owner).

**Feedback loops.** Anthropic's own eval guidance is explicit that production failures and support-queue items are the *primary* source of new eval cases, that an eval suite is a living artifact needing ongoing ownership "as routine as maintaining unit tests," and that a dedicated evals-infrastructure team plus domain-expert contributors is the effective ownership split [D06-S03]. This directly answers "how feedback becomes a prioritized backlog rather than ad hoc prompt tinkering": sampled production failures → converted into eval cases → eval delta reviewed on a cadence → prioritized against the SLO's error budget, with a named owner (not whoever is free) making the prompt/model change and logging it.

## Comparison matrices (raw)

**Documentation artifact selection**

| Situation | Right artifact | Wrong artifact and why it fails |
|---|---|---|
| Need exec approval to spend budget on Option A over B | One-page decision memo | Full architecture doc — too long, buries the ask; ADR — not written to persuade |
| Need future engineers to know why we didn't use RAG | ADR | Design doc/RFC — gets archived/lost once the thread closes; nothing forces it to be found later |
| Need a security reviewer to understand the whole system before a compliance audit | Architecture doc (C4 + arc42) | ADR log alone — gives decisions with no map of how they compose into the system |
| Need on-call to fix a stuck queue at 3am | Runbook | Architecture doc — too much context, not action-oriented |
| Need to prove to a stakeholder the system meets the promised quality bar | Eval report | Verbal assurance / demo — not reproducible, not auditable |

**SLA/SLO commitment matrix**

| Claim | Committable? | Mechanism |
|---|---|---|
| "99.9% API availability" | Yes | Infra SLO, standard SRE practice |
| "p95 latency < 3s" | Yes | Latency SLO, measured continuously |
| "≥92% pass rate on our disclosed eval set, reviewed weekly" | Yes | Quality SLO with error budget |
| "95% factual accuracy on any input" | No | No eval set covers "any input"; unfalsifiable |
| "Will never hallucinate" | No | Contradicts the nature of the system |
| "Degrades to a templated response / human handoff when confidence is low" | Yes | Fallback/degradation commitment, not an accuracy number |

## Contradictions and open questions

- **How much accuracy improvement can be promised before launch?** Sources agree a baseline must exist before promising improvement, but none of the frameworks (SRE, ATAM, Anthropic eval guidance) specify a minimum eval size or confidence interval for declaring an improvement statistically real versus noise. Treat as an open judgment call the architect must make explicit (sample size, variance) rather than a settled number. `[UNVERIFIED]`
- **Is a single static eval set ever "enough"?** Anthropic's evals guidance frames the eval suite as perpetually living [D06-S03]; the AI-Native SDLC playbook frames it as a gate that runs "whenever configuration changes" [D06-S06]. Neither source states a maximum staleness interval before an eval set is considered untrustworthy — the course should teach the principle (refresh from production sampling) without inventing a specific cadence number.
- **Percentage claims about pilot failure rates** (e.g., "88% of pilots never reach production," "61% scope creep") appear across multiple aggregator/marketing sources [D06-S25] with no primary study cited consistently across them — treat the *pattern* (curated pilot vs. live production divergence, scope creep onto adjacent workflows) as reliable and cite it qualitatively; mark any specific percentage `[UNVERIFIED]` if used.
- **RACI's origin** is genuinely disputed/undocumented in the sources found (some trace it to 1970s-80s management consulting, none to a single canonical publication) [D06-S21] — cite it as an established, widely-used convention rather than attributing it to a specific author.

## Prep-material landscape

Multiple third-party CCAR-P "exam prep" products already exist (Learning Tree bootcamp, two distinct Udemy courses, Tutorials Dojo study guide, claudecertificationguide.com, Preporato practice tests + "complete guide," CertSafari and SkillCertPro question banks) [D06-S27–S32]. All are marked **low trust** and were not used for any content in this dossier or the draft chapter, for two independent reasons: (1) the exam is version 1.0, effective July 2026, with no public item bank and a signed NDA prohibiting disclosure of live content — any product already claiming "450+ exam-style practice questions aligned with the latest exam guide" two months after go-live is near-certainly speculative or AI-generated rather than grounded in real item exposure; (2) none of the surfaced pages cite Anthropic or SEI/Google/AWS primary sources for their claims — they read as generic cert-prep SEO content restyled for a new exam code. Recommendation for the course: do not reference, quote, or structurally mirror any of these products; if a validator or reviewer encounters overlapping phrasing between this course and one of them, treat it as this course predating or independently converging on standard architecture-practice vocabulary (ADR, RACI, SLO), not as evidence either copied the other.
