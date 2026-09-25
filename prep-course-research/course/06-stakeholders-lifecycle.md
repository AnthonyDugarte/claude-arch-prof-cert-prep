# Domain 6 — Stakeholder Communication & Lifecycle Management

**Blueprint weight: 14%.** This module follows the supplied local exam guide, which is the authority for what this course covers. These are original study materials and original practice questions, not official Anthropic certification content. The detailed objectives in this module are mapped to the guide’s five Domain 6 tasks.

## What this domain asks you to do

An architect translates goals and concerns from multiple groups into an agreed system boundary, measurable outcomes, explicit decisions, and a path from discovery through operation. For a Claude solution, “the model answered” is rarely the whole product outcome. A contact-center assistant may need to reduce handling time while preserving policy compliance, keep p95 response time within a service target, avoid exposing personal data, and leave agents in control of high-impact actions. These concerns belong to different stakeholders and need different evidence.

### D6.1 — Conduct structured discovery and requirement gathering

Discovery is the disciplined work of learning what problem is worth solving, who is affected, and how the proposed system will be judged. A stakeholder is an individual or group with an interest in or affected by a program; NASA distinguishes an expectation (which may be qualitative) from a requirement that is made clear, feasible, and verifiable. In practice, preserve the original expectation before translating it into a testable requirement. [NASA Systems Engineering Handbook glossary](https://www.nasa.gov/reference/system-engineering-handbook-appendix/)

Start by naming user groups and decision owners: end users, product/business owner, operations/SRE, security/privacy/legal, data owners, accessibility representatives, and affected customers. Ask about current workflow, frequency and volume, consequences of wrong or unavailable output, exception paths, data permissions and retention, latency tolerance, integration boundaries, and adoption constraints. Separate a desired outcome (“reduce time to resolution”) from a solution proposal (“use an autonomous agent”), and separate hard constraints from preferences.

Turn broad goals into operational statements with a measure, population, measurement window, threshold, and response. Example: “For English-language password-reset requests in pilot, at least 90% of drafts are accepted with no policy correction, measured weekly by agent disposition; an agent must approve every outgoing message.” This is more useful than “accurate and safe.” Pair offline quality measures with workflow outcomes; a high benchmark score does not prove a human workflow improved.

Discovery artifacts can be lightweight: a current/future workflow sketch, stakeholder-and-concern map, assumptions and unknowns list, requirements table with owner and verification method, risk register, and a pilot decision record. Interview actual operators and review representative cases. A workshop alone can overrepresent senior sponsors; private interviews, artifact review, and usability sessions expose different evidence. Keep traceability from each important concern to a requirement, architecture decision, test, and production signal.

**Professional example.** A bank asks for a “Claude fraud investigator.” Discovery finds that analysts spend time gathering case facts, but policy requires an analyst to make every disposition. Reframe the first release as a source-linked case brief with no write access. Requirements include source provenance, analyst review, a maximum time-to-brief, and measures for omissions and false assertions. This solution preserves the objective while constraining system authority to the proven task.

### D6.2 — Communicate architectural decisions and trade-offs

An architectural decision explains a consequential choice, why it was needed, what alternatives were considered, and what follows from the choice. A short Architecture Decision Record (ADR) makes the rationale and consequences discoverable later; accepted ADRs should remain historical records and be superseded when a decision changes. The exact template is a team convention, not a universal standard. [Martin Fowler, “Architecture Decision Record”](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)

Choose a form for the audience and decision. Executives usually need outcome, cost/risk, and the decision requested. Developers need component boundaries, contracts, failure handling, test obligations, and rollout steps. Security reviewers need data flows, trust boundaries, access, retention, and audit evidence. SRE needs the user-facing SLI/SLO, dependencies, runbooks, alert routing, and rollback. A context diagram and sequence diagram may explain flow better than prose; an ADR captures the decision and alternatives. Neither artifact substitutes for the other.

Make trade-offs explicit in comparable terms: quality and error consequences; latency and throughput; token/model cost; integration and operational burden; data exposure; reversibility; and time to learn. For example, compare “retrieve current procedure at answer time” with “embed policy into prompt,” not as abstract technologies but on freshness, source traceability, latency, change control, and stale-answer risk. State what evidence could cause reconsideration.

| Communication artifact | Best when | Strength | Cost or limitation |
|---|---|---|---|
| One-page decision brief | A sponsor must choose among options | Fast alignment on impact and ask | Too little implementation detail |
| ADR | A durable system choice needs rationale | Searchable history, alternatives, consequences | Does not show the whole system |
| Architecture views/diagrams | Several roles need different system aspects | Makes structure and interactions inspectable | Can become stale without ownership |
| Live design review | Ambiguity or disagreement needs resolution | Questions surface assumptions quickly | Decisions evaporate without a record |

State a recommendation, its evidence, and an explicit confidence level. A credible architect does not hide a weak assumption under a diagram. Label unknowns, identify a cheap experiment, and record a decision trigger such as “revisit if policy freshness exceeds 24 hours or source attribution falls below the agreed threshold.”

### D6.3 — Manage feedback loops and expectation alignment, including SLAs

An SLI is a measurement of a user-relevant behavior; an SLO is its target; an SLA is an agreement with commitments and consequences. Google SRE recommends starting from what users care about, specifying the measurement conditions, and avoiding automatic targets based on current performance. SLO targets involve product and business trade-offs, not only technical tuning. [Google SRE, “Service Level Objectives”](https://sre.google/sre-book/service-level-objectives/)

For an AI workflow, choose SLIs that expose user impact: successful completion of a request, time to usable response, grounded-answer acceptance, safe abstention, tool execution success, or escalation rate. Define denominators and exclusions; “accuracy” without task population and labeling rules is not an operational promise. Distinguish model quality evaluation from service availability. An API can be up while the system produces ungrounded answers; conversely, an occasional model refusal may be the correct safe behavior.

Close the loop at two speeds. Fast operational feedback uses dashboards, alerts, support tickets, and incident review. Slower product feedback uses user interviews, sampled output review, acceptance and correction rates, and periodic reprioritization. Assign who reviews each signal, how often, and what action follows. An error budget is a useful negotiation device when service reliability and feature work compete; it does not itself define acceptable model quality. [Google SRE, “Embracing Risk”](https://sre.google/sre-book/embracing-risk/)

Expectation alignment means explaining what the system can and cannot do, what is measured, who owns review, what happens during degradation, and when the team will pause rollout. For example, set an initial pilot expectation that the assistant drafts but never sends, provide a human override and escalation path, and review a representative sample weekly. Do not present a pilot threshold as a contractual SLA until operations, measurement, exclusions, and remedies are agreed.

### D6.4 — Document architectures and provide implementation guidance

Architecture documentation serves the people who must understand, build, operate, assess, or change the system. The SEI’s stakeholder-centered review approach asks whether documentation enables its intended readers to do their jobs and helps expose gaps. [SEI, “A Structured Approach for Reviewing Architecture Documentation”](https://www.sei.cmu.edu/library/a-structured-approach-for-reviewing-architecture-documentation/)

Useful handoff material for a Claude system usually includes: scope and non-goals; context and deployment views; request/data flow; prompt, retrieval, tools, and model responsibilities; identity and authorization boundaries; evaluation and release gates; failure behavior and fallbacks; dashboards and runbooks; owner/contact and escalation; known limitations; and open decisions. Provide implementation guidance as an ordered path: prerequisites, interfaces and schemas, sequence, test fixtures, secrets handling, rollout stages, acceptance criteria, and operational ownership. Document who can approve prompt/model changes and how those changes are evaluated.

Tailor the views. A product lead can use a workflow and outcome map; developers need contracts and sequence; privacy needs data lineage and retention; operators need a dependency map and failure playbooks. A single giant architecture document often hides the answer each reader needs. Conversely, a diagram without a legend, ownership, or update path creates false confidence. Review documentation with its intended audience, then tie key claims to implementation or operating evidence.

### D6.5 — Support discovery, design, handoff, monitoring, and iteration

Lifecycle ownership continues after design approval. NASA describes stakeholder-expectation elicitation across applicable life-cycle phases and validation against the baselined expectations. NIST’s voluntary AI RMF frames risk work through Govern, Map, Measure, and Manage, and stresses actors across the AI lifecycle; its published page says the framework is being updated, so check current status before treating it as organizational policy. [NASA handbook](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) · [NIST AI RMF](https://airc.nist.gov/airmf-resources/airmf/)

At discovery, define the outcome, affected people, constraints, and evidence. At design, establish architecture, risk controls, evaluation, SLOs, and decision records. At build and verification, turn requirements into tests and resolve integration assumptions. At pilot and deployment, use staged exposure, human oversight where needed, rollback, support ownership, and clear user communication. At operations, monitor technical and user outcomes, review incidents and drift, and feed evidence into the next design iteration. At retirement, revoke access, archive required records, and provide a transition plan.

For a model or prompt change, treat it as a potentially behavior-changing release: version it, run the relevant evaluation set, compare against baseline, test failure cases, obtain required review, and roll out gradually. Keep an explicit rollback trigger. These are professional practices derived from lifecycle/risk principles; the blueprint itself does not mandate a specific framework or artifact template.

## Decision patterns and failure modes

| Choice | Choose it when | What it buys | What it costs / when another choice wins |
|---|---|---|---|
| Strict deterministic gate | A measurable invariant must never be violated | Clear release or workflow control | Can block useful changes if the metric is poor; use a human review or staged threshold when judgment is needed |
| Human review before action | Error impact is high or evidence is immature | Accountability and recovery | Slower and expensive at scale; automate only bounded, validated actions |
| Pilot with limited cohort | Real-world evidence is needed | Lower blast radius and learning | Slower broad value; use when uncertainty justifies staged exposure |
| Full launch | Risk is low, controls are mature, and demand warrants it | Fast availability | Larger incident radius; avoid when rollback and monitoring are unproven |

Common failures include interviewing only the sponsor; turning a vague wish directly into a model choice; recording a metric without a denominator; promising 100% reliability; mixing “API available” with “answer correct”; failing to name owners for alerts or policy decisions; documenting only happy-path architecture; treating human review as an unspecified checkbox; and handing off code without runbooks or change control. In each case, the correction is to make the concern, owner, evidence, and response explicit.

## Hands-on lab: design a claims-intake assistant

**Scenario:** An insurer wants Claude to summarize submitted claim packets and suggest missing documents. A licensed adjuster must make all eligibility and payment decisions. Build a reviewable discovery-to-handoff pack, not a running application.

**Tasks:**

1. Identify at least five stakeholder groups and one concern each; include an end user and an affected customer.
2. Write three measurable requirements: one task-quality, one service/latency, and one privacy or control requirement. Give each a measure, population, threshold, owner, and verification method.
3. Sketch the data flow and mark trust boundaries, retrieval sources, model call, reviewer, and audit record.
4. Write a one-page ADR choosing one approach for source retrieval and one alternative. State rationale, consequences, confidence, and a revisit trigger.
5. Propose one SLI/SLO pair and a pilot feedback cadence; state the action if the target misses.
6. Produce a handoff checklist with rollout, rollback, evaluation, runbook owner, and change approval.

**Acceptance criteria:** Another team can identify the user outcome, model boundary, permitted action, test for every requirement, operational owner, and rollback trigger without verbal clarification. The ADR includes a real alternative and evidence-based trade-off. No requirement permits Claude to decide eligibility or pay claims. The proposed SLO has an explicit denominator and measurement window. A missed target has a named response and review owner.

## Original scenario practice

These questions are original study exercises, not official exam items.

**1. Select ONE.** A director asks for “a chatbot that gets claim decisions right.” Which discovery response is strongest?

A. Select the largest model and benchmark it against public QA data.  
B. Ask which users and decisions are in scope, quantify error impact, define success measures and human authority, then test representative cases.  
C. Commit to 99.99% API availability as the definition of “right.”  
D. Ask the vendor to define accuracy after implementation.

**Answer: B.** It makes the problem, consequences, workflow, and evidence concrete before prescribing a solution. A’s benchmark may not represent the claims task; C measures service availability rather than decision quality; D delegates requirements to a party without the business context.

**2. Select TWO.** A durable architecture choice between live policy retrieval and a static prompt copy must be reviewed by developers and compliance. Which two actions best support that review?

A. Record the decision, rationale, alternatives, consequences, status, and reconsideration trigger in an ADR.  
B. Share a data-flow view showing source, access boundary, freshness, and model context.  
C. Send only a cost estimate because compliance can infer data movement.  
D. Wait until production and reconstruct why the design was chosen.

**Answer: A and B.** A preserves decision context while B makes data handling visible. C omits the compliance concern; D loses an opportunity to catch a material risk before implementation.

**3. Select ONE.** An executive proposes that an internal assistant “meet a 99.99% SLA.” What should the architect do first?

A. Accept the target because higher is always better.  
B. Convert it into a user-relevant SLI, define the population/window and response to violation, then review cost and business impact with owners.  
C. Replace it with model accuracy.  
D. Promise it for API uptime and assume users interpret it the same way.

**Answer: B.** A service commitment needs precise measurement and a consequence, and its target reflects business trade-offs. A can be wasteful or undefined; C is a different quality dimension; D silently conflates availability with user success.

**4. Select ONE.** A retrieval assistant meets latency targets but customer-support agents report that citations often point to retired policy pages. What is the best feedback-loop response?

A. Tune the model’s temperature until agents stop noticing.  
B. Add a freshness/provenance measure, sample incidents with agents and policy owners, correct indexing/retirement controls, then verify in a staged release.  
C. Increase the uptime target.  
D. Tell agents to ignore citations.

**Answer: B.** The reported issue is source currency and trust, so it needs a measurable signal, joint diagnosis, remediation, and reevaluation. A does not address stale evidence; C measures the wrong property; D discards a safety aid.

**5. Select ONE.** A team is handing a Claude-based triage service to operations. Which handoff item is most critical to add to an architecture diagram?

A. The preferred color palette for dashboards.  
B. Failure modes, alert ownership, runbook and rollback steps, and the thresholds that trigger them.  
C. A list of model names without versioning.  
D. A copy of the original workshop transcript.

**Answer: B.** The operator needs actionable ownership and recovery guidance. A and D may be useful in context but do not enable incident response; C is incomplete without change and rollback policy.

**6. Select THREE.** A pilot’s answer acceptance is lower for Spanish-language cases, even though aggregate quality meets the launch target. What should the lifecycle review include?

A. Segment the metric by language and case type and validate sample size and labeling.  
B. Interview affected users and inspect representative failures with a domain reviewer.  
C. Continue rollout because the aggregate target passes.  
D. Record the risk, decide whether to narrow or pause scope, and define a retest/rollout condition.  
E. Remove the language field from reports to avoid biasing future decisions.

**Answer: A, B, and D.** Segmentation reveals a hidden disparity, user and expert review explains it, and a documented scope decision plus retest condition makes iteration controlled. C ignores the subgroup; E hides relevant evidence.

## Objective checklist

You are ready to move on when you can conduct structured discovery (D6.1), explain options and rationale (D6.2), align measures and feedback with stakeholders (D6.3), tailor architecture/handoff documentation (D6.4), and define evidence and ownership through operation and iteration (D6.5).
