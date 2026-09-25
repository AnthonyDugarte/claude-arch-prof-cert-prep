# Domain 6: Stakeholder Communication & Lifecycle Management

**Weight:** 14% of the exam (approximately 9 of 63 scored items).

**Objectives measured:**
1. Conduct structured discovery and requirement gathering.
2. Communicate architectural decisions and trade-offs.
3. Manage stakeholder feedback loops and expectation alignment (including SLAs).
4. Document architectures and provide implementation guidance.
5. Support lifecycle phases (discovery, design, handoff, monitoring, iteration).

This domain does not test writing skill or interpersonal style. It tests whether you know the **named, established artifact or technique** for a given moment in a project's life, and can tell it apart from a plausible but wrong neighbor: a decision memo where an ADR belongs; an SLA where only an SLO is honest; a demo mistaken for a promotion gate.

---

## 1. Exam-relevance framing

The Minimally Qualified Candidate runs discovery, writes the trade-off record, negotiates the SLA, and hands a probabilistic system to an operating team. Items are scenario stems ending in "what should the architect do first / next / instead," almost never trivia ("what does RACI stand for").

**Recurring distractor archetypes in this domain:**

1. **The eloquent-but-wrong document.** Offers a full architecture document when an ADR is correct, or a verbal/slide recommendation when a trade-off table is correct. Tests whether you know which artifact matches which decision's durability and audience.
2. **The unfalsifiable commitment.** Offers "99% accuracy" or "no hallucinations" as an SLA option. Tests whether you know an SLO must be a measured band against a disclosed eval set, not a promise about arbitrary future inputs.
3. **The demo-as-evidence trap.** Treats a pilot that worked on curated cases as sufficient grounds for production rollout. Tests whether you require an eval-gate pass rate on a production-representative sample before promotion.
4. **The false binary on automation.** Offers "give the stakeholder 100% automation" or "refuse and keep everything manual" as the only options. Tests whether you reframe around reversibility and error budget instead.
5. **The premature scope answer.** Offers a technical fix to what is actually an unanswered discovery question (no baseline, no named accuracy owner, no reversibility answer). Tests whether you recognize the architecture can't be chosen yet.
6. **The ownerless handoff.** Offers to "monitor performance" or "add logging" without naming who owns the SLO, who approves prompt changes, or who is on call. Tests whether you know a lifecycle gate requires a named accountable person, not just a capability.

---

## 2. Core concepts

Each concept: definition → why an architect cares → the decision it drives → common misconception.

**Structured discovery (Quality Attribute Workshop / mini-QAW lineage) [D06-S16, D06-S17].** A facilitated session eliciting measurable *quality-attribute scenarios* (stimulus/response) from stakeholders before an architecture exists, not a form stakeholders fill in alone. Cares because unstructured discovery collects untestable adjectives ("fast," "accurate," "secure"). Drives whether a real acceptance criterion can be written at all. Misconception: discovery is a one-time kickoff, not a repeatable technique.

**Jobs to Be Done [D06-S18].** The underlying progress a stakeholder seeks, distinct from the feature requested. Cares because building the literal request over- or under-scopes the system relative to the actual job. Drives scope boundaries and the success metric. Misconception: "what do you want" surfaces the job — it surfaces the request, which must be interrogated further.

**MoSCoW / value-vs-feasibility scoring [D06-S19, D06-S20].** Techniques for sorting candidates into committed-scope vs. explicitly-deferred. Cares because an unscoped pilot is the direct precursor to mid-pilot scope creep. Drives what ships in v1 versus what's documented as deferred. Misconception: dismissing these as busywork rather than the artifact that later proves something was explicitly out of scope.

**Baseline before promising improvement.** Before committing to "this will improve X," current human or system performance on X must be measured. Cares because an SLO or business case with no baseline can never be shown true or false later. Drives whether a success criterion is falsifiable at all. Misconception: assuming the current process is "obviously" near-perfect without measuring it either.

**Architecture Decision Record (ADR) [D06-S09, D06-S10].** A short, immutable record of one significant decision: Title, Status, Context, Decision, Consequences. Cares because decisions made under pressure get re-litigated unless the "why" is written down. Drives what gets written *after* a decision, not before. Misconception: an ADR persuades a stakeholder — it records a decision already made, including its downsides.

**C4 model [D06-S11] and arc42 [D06-S12].** C4 is diagram notation at four zoom levels (system context, container, component, code) matched to different audiences; arc42 is a 12-section prose template (goals, constraints, context, solution strategy, building blocks, runtime, deployment, crosscutting concepts, decisions, quality, risks, glossary) for a complete architecture document. Cares because "document the architecture" is not one artifact. Drives what a security reviewer, new engineer, or executive each actually needs to see. Misconception: one monolithic diagram serves every audience.

**RFC / design doc [D06-S23, D06-S24].** A pre-decision proposal circulated to solicit disagreement, distinct from an ADR's post-decision record. Cares because skipping the RFC loses documented alternatives; skipping the ADR after it loses the durable record once the thread is archived. Drives a two-step process for consequential, contested decisions. Misconception: treating RFC and ADR as the same document at different times — they serve different purposes and often have different authors.

**SLI / SLO / SLA / error budget [D06-S13].** An SLI is a measured indicator; an SLO is a target range for it; an SLA adds an external, usually financial, consequence for missing the SLO; the error budget is `1 − SLO target`, spent as changes ship. Cares because "accuracy" for a probabilistic system must become an SLI computed from a disclosed eval set, not a promise. Drives whether prompt/model changes are budget-gated the way infra changes are gated in SRE practice. Misconception: treating SLA and SLO as interchangeable — an SLA specifically implies a contractual consequence; most internal quality commitments are SLOs.

**Eval gate as promotion criterion [D06-S03, D06-S06].** A documented, threshold-based pass rate on an eval set sourced from real tasks/failures, required before a phase transition (build → pilot, pilot → production). Cares because it replaces "the demo looked good" with a reproducible, falsifiable criterion. Drives the entire pilot-to-production transition. Misconception: one eval run at launch suffices forever — the suite must be refreshed from production sampling and re-run on every prompt/model change.

**RACI [D06-S21].** Responsible / Accountable / Consulted / Informed — assigns exactly one Accountable party per decision or ongoing responsibility. Cares because "the team owns it" satisfies neither an incident retrospective nor an auditor. Drives handoff design: who approves prompt changes, who owns the SLO, who is consulted on data sensitivity, who is informed of incidents. Misconception: naming multiple people Accountable — RACI's value is forcing exactly one.

**Runbook [D06-S22].** An action-oriented procedure for a specific scenario ("what to do when the eval pass rate drops below threshold"), distinct from the architecture doc (what the system is) and the ADR (why a decision was made). Cares because on-call quality shouldn't depend on the original author being reachable. Drives what ships at handoff, not what gets written after the first incident.

---

## 3. Trade-off analyses

### 3.1 Which document for which decision

| Situation | Artifact | Choose this when... | The wrong choice loses... |
|---|---|---|---|
| Persuade an executive to fund Option A over B | One-page decision memo | Non-technical approver, time-boxed ask | ADR (not persuasive); full arch doc (too long, buries the ask) |
| Record why RAG was rejected in favor of long-context | ADR [D06-S09] | Decision is made; future maintainers will ask "why" | RFC thread (gets archived and lost); nothing (decision gets silently re-litigated) |
| Solicit disagreement on a contested integration pattern before committing | RFC / design doc [D06-S23, S24] | Decision is consequential, reversible pre-commit, multiple valid options | Jumping straight to an ADR — no documented alternatives, less buy-in |
| Give a compliance auditor the whole system | Architecture doc: C4 diagrams + arc42 sections [D06-S11, S12] | Audience needs the full system, at multiple zoom levels, plus constraints/risks | ADR log alone (decisions with no map of how they compose) |
| Tell on-call what to do at 3am when the pass-rate SLO breaches | Runbook [D06-S22] | Action-oriented, time-pressured, non-original-author reader | Architecture doc (too much context, not action-oriented) |

**Discriminator:** ask "is this decision-persuasion, decision-record, whole-system-reference, or emergency-action?" — each maps to exactly one artifact above. Never let "it depends" stop there — the answer depends on *audience* and *durability required*, both statable in one sentence.

### 3.2 SLA vs. SLO vs. no formal commitment, for a probabilistic feature

| Commitment type | Committable for an LLM feature? | Mechanism | Example |
|---|---|---|---|
| Availability / uptime SLA | Yes | Standard infra SLA, unrelated to model behavior | "99.9% API availability" |
| Latency SLO | Yes | Measured continuously against the serving path | "p95 < 3s" |
| Quality SLO with error budget | Yes, if disclosed eval set exists [D06-S13] | Pass rate against a named, versioned eval set, reviewed on a cadence | "≥92% pass rate on eval suite v7, reviewed weekly" |
| Fixed accuracy SLA on arbitrary future input | No | No eval set covers "any input"; unfalsifiable and will be breached by inputs never seen | "95% factual accuracy" |
| "No hallucinations" | No | Contradicts how the system produces output | — |
| Degradation/fallback commitment | Yes | Behavioral commitment, not a number | "Falls back to human queue when confidence signal is low" |

**Discriminator:** if the commitment can be evaluated against a specific, disclosed, versioned dataset with a stated cadence, it's committable as an SLO (and an SLA if a contractual consequence is attached). If it can only be evaluated against "whatever the user happens to ask," it is not committable — reframe it as a band plus a degradation path.

### 3.3 Prioritization technique fit: MoSCoW vs. value-vs-feasibility vs. RICE

| Technique | Best fit | Weak fit |
|---|---|---|
| MoSCoW [D06-S19] | Time-boxed delivery where "what ships in this release" must be forced to a binary | Long-lived backlogs needing relative ranking among many "Should"s |
| Value-vs-feasibility 2x2 [D06-S20] | Fast, low-data-requirement first pass across many candidate use cases | Fine-grained ranking within a cluster that all land "high value / high feasibility" |
| RICE (Reach/Impact/Confidence/Effort) [D06-S20] | Comparing many candidates with enough data to estimate reach and confidence | Early-stage discovery where reach/impact aren't estimable yet |

**Discriminator:** MoSCoW answers "what's in this release," the 2x2 answers "which use case do we even attempt first," RICE answers "how do we rank a mature backlog." Using RICE at kickoff (no data to estimate reach/confidence) or MoSCoW across a whole multi-year portfolio (too coarse) are both the "looks-right, is-wrong" answer on this exam.

### 3.4 Human review posture: 100% review vs. sampled review vs. no review

| Posture | Choose when... | Fails when... |
|---|---|---|
| 100% human review before action | Actions are irreversible and high-blast-radius [D06-S04]; human capacity is available | Volume exceeds review capacity — becomes a bottleneck that quietly gets bypassed |
| Sampled review with production feedback into eval set [D06-S03] | Actions are reversible or low-blast-radius; volume is high | Sample size/selection is not representative of true failure modes |
| No human review, fully autonomous | Actions are reversible, cheap to fix, and an error budget with a fallback exists | Applied to irreversible actions "because it scaled fine in the pilot" |

**Discriminator:** the axis is reversibility and blast radius, not volume or executive preference. High volume is a reason to move from 100% review toward *sampled* review with a feedback loop — it is never on its own a reason to remove review from irreversible actions.

### 3.5 Eval-gate promotion vs. demo-based sign-off vs. fixed-calendar launch

| Promotion criterion | What it actually validates | Where it fails |
|---|---|---|
| Eval-gate pass rate on production-representative sample [D06-S03, S06] | The system's behavior on the distribution it will actually see | Requires upfront investment in building and maintaining the eval set |
| Demo-based stakeholder sign-off | That curated cases work and stakeholders are engaged | Curated cases are not the production distribution — this is the demo-to-production gap [D06-S05] |
| Fixed-calendar launch ("we said Q3") | Nothing about the system; it validates a date | Ships regardless of measured quality; the most common source of an unplanned SLA breach |

**Discriminator:** only the eval-gate criterion is falsifiable and reproducible. Demo sign-off and calendar dates are organizationally real pressures but are never the *architectural* answer to "how do we know it's ready."

### 3.6 Lifecycle ownership model: single owner vs. RACI vs. no named owner

| Model | Choose when... | Fails when... |
|---|---|---|
| Single named owner for the SLO and prompt/model changes | Small system, one team, low cross-functional dependency | System touches security, legal, and multiple engineering teams — single owner becomes a bottleneck or a rubber stamp |
| RACI across roles (product owner, release manager, service owner, security consulted) [D06-S06, S21] | Cross-functional handoff, regulated environment, multiple teams touch the lifecycle | Overhead exceeds the coordination benefit for a very small, single-team system |
| No named owner ("the team owns it") | Never the right answer at handoff | Always — incidents and audits require exactly one Accountable name |

**Discriminator:** the exam will never accept "the team is responsible" as correct when a RACI-style question is asked; it is testing whether you know Accountable must resolve to one person.

---

## 4. Worked scenarios

**4.1 Financial services — loan-underwriting copilot discovery.** A regional bank wants Claude to "help underwriters process loan applications faster." *Constraints:* regulated decisions, explainable adverse-action reasons, costly-to-reverse denials. *Candidates:* (a) fully autonomous approve/deny; (b) Claude drafts recommendation + explanation, underwriter decides; (c) Claude only summarizes, human does the rest. *Recommended:* (b) — the underlying job is faster underwriting, not automated lending, and low reversibility keeps a human as decision-maker; (c) underuses the model against the actual job. *(a) loses:* treats "faster" as "unattended," ignoring reversibility [D06-S04]. *(c) loses:* fails Jobs to Be Done — doesn't touch the real bottleneck (drafting a defensible rationale) [D06-S18]. *Changes the answer:* a large volume of low-dollar, easily-reversible micro-loans would make autonomy defensible for that subset, under a tight error budget.

**4.2 Healthcare — clinical documentation assistant, SLA negotiation.** A hospital's vendor-management team wants a contractual "99% accuracy" clause for ambient clinical-note drafting. *Constraints:* no eval set yet; clinicians edit drafts before signing; legal wants an enforceable number. *Candidates:* (a) accept the 99% clause; (b) counter with an SLO — pass rate on a jointly-defined, disclosed eval set, reviewed quarterly, plus a latency/availability SLA; (c) refuse any quantitative commitment. *Recommended:* (b) [D06-S13]. *(a) loses:* unfalsifiable against undefined future notes, breached by the first edge case. *(c) loses:* stakeholders need some measurable commitment; refusing reads as no quality discipline. *Changes the answer:* an existing large, adjudicated note corpus would justify a tighter band sooner.

**4.3 Retail — the pilot that worked on 20 curated tickets (over-promised pilot).** A support agent handled 20 hand-picked refund tickets flawlessly; the VP of CX wants it live for all inbound tickets in two weeks, including account changes. *Constraints:* production volume/diversity dwarf the pilot set; account changes are harder to reverse than refunds. *Candidates:* (a) launch at full volume and full tool scope as requested; (b) launch at original scope (refunds only) against a production-sampled eval gate, defer account changes pending their own reversibility review; (c) delay indefinitely for a full enterprise eval program. *Recommended:* (b) [D06-S03, S05]. *(a) loses:* mistakes the curated demo for production evidence — the demo-to-production gap — and expands tool scope without the reversibility discovery it requires [D06-S04]. *(c) loses:* stalls demonstrated value; the fix is scoping and gating, not refusing. *Changes the answer:* a 24-hour undo window on account changes would let that tool join the same gated rollout instead of waiting.

**4.4 Government — the "100% automation" hostile stakeholder.** A budget-pressured program director insists a permit-approval agent run with "no humans in the loop." *Constraints:* wrong approvals carry legal/public-safety consequences; the director is skeptical of "vendors always wanting more review." *Candidates:* (a) agree to full automation; (b) flatly refuse any automation beyond drafting; (c) reframe around reversibility and error budget — full automation now for low-risk, easily-reversible permit types, with an SLO-gated path to expand autonomy as track record accumulates. *Recommended:* (c) [D06-S04, S05]. *(a) loses:* sets up an SLA the architecture can't honestly meet; creates public-sector liability. *(b) loses:* reads as obstruction to a hostile stakeholder and forfeits credibility to negotiate; ignores any genuinely low-risk subset. *Changes the answer:* if every permit type were equally high-stakes with no low-risk tier, the honest answer shifts to human-in-the-loop for the full scope, argued in a decision memo to the director.

**4.5 Manufacturing — predictive-maintenance discovery under a hard cost ceiling.** A plant wants Claude to triage sensor-alert narratives under a strict per-request cost ceiling. *Constraints:* high volume, loose latency (batch is fine), ceiling rules out a top-tier model on every request. *Candidates:* (a) run every alert through the most capable model; (b) cheap-model triage, escalate only ambiguous/high-severity alerts; (c) skip the LLM, hand-code a rules engine. *Recommended:* (b) — matches high volume, loose latency, hard ceiling to a cascade pattern. *(a) loses:* ignores the stated cost ceiling, a discovery answer that should gate model choice before build. *(c) loses:* free-text alert narratives are exactly where a rules engine gets brittle. *Changes the answer:* if triage misses were shown safety-critical rather than efficiency-only, the cost ceiling itself becomes negotiable against that safety case.

**4.6 Legal — handoff documentation for a contract-review copilot.** A law firm's innovation team hands a contract-clause-flagging copilot to IT operations, which will own it going forward. *Constraints:* IT ops has no context on prior model/prompt choices; partners expect zero unexplained downtime. *Candidates:* (a) codebase plus a verbal walkthrough; (b) full documentation set — architecture doc, ADR log, runbook, eval report, change log, RACI — with a named accountable owner in IT ops; (c) keep the innovation team as permanent on-call. *Recommended:* (b) [D06-S06, S21, S22]. *(a) loses:* verbal knowledge doesn't survive turnover and blocks safe future changes. *(c) loses:* isn't a handoff — leaves the build team a permanent, non-scaling bottleneck. *Changes the answer:* nothing here changes it; this is a near-pure test of the documentation set itself.

**4.7 Insurance — feedback loop ownership after launch.** Six months post-launch, a claims-triage assistant's support team has a growing "the model got this wrong" backlog that goes nowhere. *Constraints:* the build team has moved on; reports are emailed to whoever answers first. *Candidates:* (a) let the original build team handle reports informally when free; (b) name an eval owner who converts sampled production failures into eval cases on a cadence, with a RACI-defined approver for resulting changes; (c) tell support to stop forwarding reports. *Recommended:* (b) [D06-S03, S21]. *(a) loses:* whoever's-free handling is exactly the ad hoc prompt-tinkering pattern this mechanism exists to prevent, and won't survive team turnover. *(c) loses:* discards the richest source of new eval cases — real production failures [D06-S03]. *Changes the answer:* near-zero report volume would justify a lighter, non-dedicated cadence — the mechanism should scale with volume, not disappear.

---

## 5. Failure modes & diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| Pilot succeeded on curated cases, fails at broader rollout | Eval/demo set not representative of production distribution [D06-S05] | Compare demo case selection against a random production sample | Rebuild the eval set from sampled production data before re-promoting |
| Stakeholders keep expanding scope after go-live | No documented scope boundary before build | Check whether a MoSCoW/value-feasibility artifact or scope section in a decision memo exists | Write or retrieve the scope decision; route new asks through a change process, not ad hoc agreement |
| Accuracy complaints despite a passing eval | Eval set is stale relative to current traffic mix | Check the eval set's last-updated date vs. recent production samples | Refresh the eval set from current production sampling; re-run the gate |
| Executive expects near-100% accuracy "because it's AI" | No baseline was ever agreed before launch | Check discovery records / decision memo for a stated baseline | Reframe the SLA conversation around a measured band plus error budget versus the documented baseline |
| No one can say who owns a failed prompt change | No RACI or named owner assigned at handoff | Check the handoff checklist / runbook for a named Accountable party | Assign an owner explicitly; add to the runbook and RACI |
| Security blocks launch at the last gate | Discovery didn't include security in the room early | Check whether security was present during discovery, not just final review | Add security/legal as Consulted stakeholders during discovery, not only at a late review gate |
| Prompt is hand-edited in production with no record | No prompt/model change log | Check for a versioned change log tied to eval deltas | Require every prompt/model change to log a version and its eval-delta result |
| Quality "feels" worse after a model upgrade, no eval evidence | SLO wasn't re-validated against the new model version | Check whether the eval gate re-ran post-upgrade | Treat every model/prompt change as a release requiring an eval-gate re-run before it counts as promoted |

---

## 6. Anti-patterns

**Demo-driven architecture.** A polished live demo becomes the de facto spec; no discovery record says what was actually agreed. Looks right because the demo is real, working software — but it answers "can it work," not "what must it do, for whom, at what accuracy, at what cost."

**Recommendation-only slide.** A trade-off conversation is presented as "we recommend X" with no table of alternatives. Looks right because it's decisive — but it erases the audit trail; six months later no one can reconstruct why B was rejected, and B gets re-proposed as new.

**Verbal SLA.** A quality commitment stated in a meeting ("it'll be about 95% accurate") never gets written into an SLO/SLA with a named eval set and cadence. Looks right because it satisfies the room — but it's unenforceable and becomes the thing stakeholders quote back during an incident.

**The one eval to rule them all.** A single eval set built at launch is treated as permanently sufficient. Looks right because "we have an eval" sounds like diligence — but a static set doesn't track a shifting production distribution or a model/prompt change, so a passing eval stops meaning anything.

**The ADR graveyard.** ADRs get written but never indexed or consulted before new decisions. Looks right because the practice is in place — but if no one reads them first, they protect nothing.

**The automation ratchet.** A "100% automation" mandate is accepted at kickoff without documenting the reversibility trade-off. Looks right because it satisfies the loudest voice immediately — but it locks in an architecture that cannot honestly meet its own future SLA once an irreversible error occurs.

**Silent scope creep in agentic projects.** Every new stakeholder request during a pilot is treated as a small bug fix rather than a scope change needing its own discovery and decision record. Looks right because each ask seems minor — but tool scope, reversibility, and blast radius compound, and the system evaluated is not the system that ships.

---

## 7. Exam-day heuristics

- **Match the artifact to durability and audience, not to how important the decision feels.** A single significant technical decision → ADR. A funding ask → one-page memo. The whole system → C4 + arc42. An emergency procedure → runbook.
- **"Quality" for an LLM feature is an SLO with a measured band and an error budget — never a promised percentage or "no hallucinations."** If an option promises a fixed accuracy number against arbitrary future input, it's wrong regardless of how confident it sounds.
- **A demo on curated cases is evidence of feasibility, not evidence of production readiness.** The correct promotion criterion is always an eval-gate pass rate on a production-representative sample.
- **When a stakeholder demands "100% automation," reframe around reversibility and error budget — never a flat yes or a flat no.**
- **Discovery answers that gate architecture (reversibility, accuracy owner, data sensitivity, human review capacity) come before pattern/model selection, not after.** If an item's correct-seeming answer picks a model or pattern before those questions are settled, it's the trap.
- **RACI's Accountable is exactly one name.** "The team" or "the platform" is never a correct answer to an ownership question.
- **Model/prompt changes are releases.** Any option that treats them as exempt from the eval gate or SLO re-validation is wrong.

---

## 8. Practice items

**Item 1 (select 1).** A mid-size insurer's pilot of a claims-summary assistant performed flawlessly on 20 claims the project team selected to demonstrate the tool to leadership. Leadership wants to expand to all incoming claims next week. What should the architect recommend first?
A. Expand to all claims immediately, since the pilot proved the model works.
B. Build an eval set sampled from real incoming claims and require a passing threshold before expanding scope.
C. Reduce the model to a cheaper tier to control cost at the new volume.
D. Add a disclaimer to outputs so users know the tool can be wrong.

*Correct: B.* A curated 20-case demo is not evidence about the production distribution [D06-S03, S05]. *A* is the demo-to-production gap. *C* addresses cost, a question this stem never raised. *D* is a UX mitigation, not a promotion criterion, and doesn't answer whether the system is ready.

**Item 2 (select 1).** A stakeholder insists on a contract clause guaranteeing "97% accuracy" for a document-classification feature. Which counter-proposal is most defensible?
A. Accept the clause; 97% is achievable based on early testing.
B. Refuse to include any quality language in the contract.
C. Propose an SLO stated as a pass rate on a disclosed, versioned eval set, reviewed on a fixed cadence.
D. Propose a clause guaranteeing zero hallucinations instead, which is a stronger commitment.
*Correct: C.* This is the only falsifiable, disclosed-methodology commitment [D06-S13]. *A* is unfalsifiable against arbitrary future documents. *B* fails to give the stakeholder any measurable commitment. *D* is not achievable or meaningful for a probabilistic system.

**Item 3 (select 1).** During discovery for an agent that will issue refunds automatically, which question most changes the resulting architecture?
A. What color scheme should the refund confirmation email use?
B. How reversible is an incorrectly issued refund?
C. Which project management tool does the team use?
D. How many engineers are on the build team?
*Correct: B.* Reversibility directly gates whether human approval is required before action [D06-S04]. The others are operational or cosmetic and don't change the architecture.

**Item 4 (select 2).** Which two artifacts belong in a handoff to an operating team taking over a production Claude-based feature? (Select 2.)
A. A runbook covering known failure scenarios.
B. The original brainstorming notes from the kickoff meeting.
C. A named RACI for prompt/model change approval and SLO ownership.
D. A copy of the vendor's marketing deck used to sell the project internally.
*Correct: A, C.* Both are load-bearing for ongoing operation [D06-S06, S21, S22]. *B* and *D* are historical artifacts with no operational function.

**Item 5 (select 1).** A program director tells an architect, "I don't want any humans reviewing this system's decisions — that defeats the purpose of automation." The system approves permits, some of which have public-safety consequences. What is the architect's best response?
A. Agree, since the director controls the budget.
B. Refuse outright and insist on full manual review of every permit.
C. Propose full automation for low-risk, easily-reversible permit types now, with a documented path to expand autonomy as the eval track record accumulates.
D. Recommend delaying the project until the director changes their position.
*Correct: C.* Reframes around reversibility/error budget rather than a binary yes/no [D06-S04, S05]. *A* creates unmanaged liability. *B* is likely to be rejected by a stakeholder already skeptical of "AI vendors wanting more review" and ignores any low-risk subset that exists. *D* stalls value with no negotiation attempted.

**Item 6 (select 1).** Which statement about Architecture Decision Records is correct?
A. An ADR is written before a decision to solicit alternative proposals.
B. An ADR should be edited in place when a later decision supersedes it.
C. An ADR records a decision already made, including its negative consequences, and is superseded rather than edited.
D. An ADR replaces the need for a full architecture document.
*Correct: C* [D06-S09]. *A* describes an RFC. *B* violates the immutability principle. *D* confuses scope — an ADR log and a full architecture document serve different purposes (Section 3.1).

**Item 7 (select 1).** Which of the following is the best discriminator between using C4 diagrams and using an arc42 document structure?
A. C4 is for regulated industries; arc42 is for unregulated industries.
B. C4 provides diagram notation at multiple zoom levels; arc42 provides the prose section structure a complete architecture document needs — they compose together.
C. C4 replaces the need for any written documentation.
D. arc42 is only used for microservice architectures.
*Correct: B* [D06-S11, S12]. The others invent constraints not supported by either framework.

**Item 8 (select 1).** An eval-owning team wants to decide how to source their first eval set for a newly launched agent. What is the most defensible starting approach?
A. Write 500 synthetic test cases covering every conceivable input before launch.
B. Wait until a formal enterprise-wide eval program is funded and staffed.
C. Draw 20-50 tasks from real development checks, known failure modes, and (once live) the support queue.
D. Rely entirely on user star-ratings as the eval signal.
*Correct: C* [D06-S03]. *A* over-invests before knowing what actually fails. *B* delays indefinitely for no architectural reason. *D* is a weak, indirect quality signal, not a grading method tied to specific tasks.

**Item 9 (select 2).** Which two of the following are legitimate reasons to move from 100% human review to sampled review with production feedback into the eval set? (Select 2.)
A. Review volume has exceeded human review capacity.
B. The actions being reviewed are reversible and low-blast-radius.
C. An executive has requested faster turnaround regardless of risk profile.
D. The build team wants to reduce headcount costs this quarter.
*Correct: A, B* [D06-S03, S04]. Both are architecture-relevant (capacity and risk profile). *C* and *D* are pressure, not a risk-based justification, and would be the wrong basis for the decision on their own.

**Item 10 (select 1).** A stakeholder asks, "Since we upgraded to a newer model version last week, do we need to re-run our eval suite?" What is the correct architectural answer?
A. No, newer models are strictly better, so re-running is unnecessary.
B. Yes — a model version change is a release and must be validated against the eval gate before the existing SLO is considered still met.
C. Only if users have already complained.
D. Only if the contract explicitly requires it.
*Correct: B* [D06-S03, S06, S13]. A model change can shift the SLI the SLO was set against; treating it as a release requiring re-validation is the only option consistent with SRE-style error-budget governance. *A* assumes uniform improvement across all tasks, which is not guaranteed. *C* and *D* wait for harm or contract language instead of validating proactively.

---

## 9. Objective-coverage table

| Objective | Covered in |
|---|---|
| Conduct structured discovery and requirement gathering | §2 (Structured discovery, JTBD, MoSCoW, baseline); §3.3, §3.4; §4.1, §4.5; §5; Practice items 1, 3, 8 |
| Communicate architectural decisions and trade-offs | §2 (ADR, C4/arc42, RFC); §3.1; §4.6; §6; §7; Practice items 6, 7 |
| Manage stakeholder feedback loops and expectation alignment (including SLAs) | §2 (SLI/SLO/SLA, eval gate); §3.2, §3.5; §4.2, §4.3, §4.4, §4.7; §5; §6; Practice items 2, 5, 9, 10 |
| Document architectures and provide implementation guidance | §2 (ADR, C4/arc42, runbook); §3.1; §4.6; §6; Practice items 6, 7 |
| Support lifecycle phases (discovery, design, handoff, monitoring, iteration) | §2 (eval gate, RACI, runbook); §3.5, §3.6; §4.6, §4.7; §5; §6; Practice items 4, 10 |

---

## 10. Sources

Full table with URLs, publishers, types, trust ratings, and specific claims backed: `research/06-stakeholder-communication-lifecycle-sources.md`. Key sources cited above: Anthropic engineering and research blog posts on agent design, evals, and agentic misalignment [D06-S02, S03, S04]; Anthropic/Claude enterprise adoption guides [D06-S05, S06, S07, S08]; Michael Nygard's ADR format and the adr.github.io template project [D06-S09, S10]; the C4 model and arc42 template [D06-S11, S12]; the Google SRE book's SLI/SLO/SLA/error-budget definitions and launch/production-readiness practice [D06-S13, S14]; AWS Well-Architected Framework's pillar trade-off guidance [D06-S15]; SEI's Architecture Tradeoff Analysis Method and the derived Quality Attribute Workshop [D06-S16, S17]; Jobs to Be Done theory [D06-S18]; MoSCoW, value-vs-feasibility/RICE, and RACI conventions [D06-S19, S20, S21]; runbook practice [D06-S22]; and design-doc/RFC practice from Google and industry writing [D06-S23, S24]. Directional-only, low-trust sources on pilot-failure statistics and generic use-case-qualification framing are cited only for pattern, not for specific figures, and are marked `[UNVERIFIED]` where a number is used [D06-S25, S26]. No content in this chapter is drawn from third-party CCAR-P prep material; see the dossier's "Prep-material landscape" section for the products found and why they were excluded.
