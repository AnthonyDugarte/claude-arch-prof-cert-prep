# Domain 5: Governance, Safety & Risk Management

**Weight:** 14% of the exam (~9 of 63 scored items)

**Objectives covered:**
1. Implement guardrails and safety controls
2. Identify risks, limitations, and failure modes of LLM systems
3. Apply human-in-the-loop validation strategies
4. Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP)
5. Address ethical AI considerations (bias, fairness, transparency)

**Scope and cross-references.** Domain 3 owns the *mechanics* of tool configuration, MCP, authentication, and multi-tenant isolation; Domain 4 owns eval construction, adversarial/red-team sets, and drift measurement. This chapter does not re-derive them. It decides **which control to reach for, how strong it actually is, and what obligation makes it non-optional**, and it cites those domains where the mechanism lives.

**Legal caution.** Everything below describes *architectural* obligations and the evidence an architecture must produce. It is not legal advice, and no authorization, certification, or retention arrangement is asserted beyond what the dated sources in §10 support. Compliance facts move; every specific authorization here carries an access date and must be re-verified per engagement.

---

## 1. Exam-relevance framing

This domain does not test recall of GDPR articles, HIPAA rule numbers, or authorization tables. It tests whether, given a system under a constraint the stem *describes but does not name*, you pick the response that actually satisfies the constraint rather than the one that looks responsible. Expect four defensible-sounding options and one that survives scrutiny of what the control does.

Recurring distractor archetypes:

1. **Detective dressed as preventive.** "Add logging / monitoring / flag for review" offered as the fix for a risk that requires the effect never to occur unapproved. Logging tells you a harm happened; it does not stop it.
2. **Prompt-only fix for a material risk.** A system-prompt instruction as the *complete* mitigation for a financial, safety-critical, or irreversible risk. Prompt rules are real but have no enforcement outside the model's weights.
3. **Compliance-by-vendor-claim.** "We use Claude, so we're HIPAA/FedRAMP compliant." Vendor posture (BAA, DPA, authorized boundary, certification) is necessary and never sufficient; the correct option names both the vendor instrument and the customer-side design obligation.
4. **Uniform human review.** "Review everything" or "review nothing," where the right answer scales review to reversibility and impact of the specific action.
5. **The over-applied reflex.** The same move that is right in one stem and wrong in another: *removal* where the role genuinely needs the capability (the answer is narrowed authority), or *a human gate* where the action could simply be made reversible.
6. **Ethics as a one-time aggregate check.** Bias testing framed as a pre-launch checkbox on an aggregate metric, instead of a segmented, re-run measurement of the deployed system.

One pattern is scored in Domain 4 and appears here once, in §5: confident-but-wrong output after a content refresh, with model and latency unchanged, is a retrieval/data-plane symptom, not a model symptom [D05-S30, Sample 3].

---

## 2. Core concepts

### 2.1 Control strength has two axes, not one ranking

A control layer is described by two independent properties:

- **Bypass resistance** — can an adversary, or an ordinary mistake, get past it? Architectural removal and deterministic code are highest; classifiers and humans are probabilistic; a prompt instruction is lowest because it has no enforcement mechanism outside the model's weights [D05-S19].
- **Expressiveness** — can the constraint even be *stated* in this layer? Humans and classifiers can judge fuzzy things ("is this tax advice?") that no predicate expresses; code and removal cover only what you can specify.

Ranking the layers on a single line is the mistake, because the two axes trade against each other. The operative rule:

> **Express the constraint deterministically if it can be expressed deterministically. Use a classifier or a human only for the residue that resists deterministic expression.**

A model-based screen is itself promptable and carries a false-negative rate; a beneficiary allow-list enforced in the payment service is not and does not. Conversely, a scope statement like "do not give tax advice" has no deterministic form, so there the available answer is prompt + classifier + a measured eval + blast-radius limits — the correct option *adds measurement and containment*, it does not delete the prompt (see Domain 2 for prompt and guardrail authoring).

Two corollaries the exam rewards:

- **A human gate is required when the decision contains judgment that cannot be reduced to a predicate.** When the action's parameters can be fully constrained in code (refund only the exact amount of a verified charge, to the original instrument, once, within 90 days), the deterministic control has *substituted* for the gate; adding a gate manufactures a rubber stamp.
- **Depth means different *kinds* of control.** A prompt rule repeated three ways is still one layer.

*Misconception:* that the control menu is "remove it" or "review it." Five moves change the problem itself, and each can be an exam key: **narrow the authority** (§2.3), **make the action reversible** (§2.4), **change what crosses the boundary** (minimize, tokenize, de-identify — T5, T6), **change whose authority the call carries** (§2.3), and **don't use the model for the decision** (§2.8).

### 2.2 Preventive, detective, compensating — and the four risk treatments

- **Preventive** stops the outcome (remove a tool, reject invalid output, gate before execution).
- **Detective** notices it (logs, audit trails, drift and disparity monitoring).
- **Compensating** bounds the impact without preventing or detecting (transaction caps, rate limits, undo windows).

*Why an architect cares:* a system can log a harm faithfully and still cause it. *Decision it drives:* for any named risk, confirm at least one preventive or compensating control exists — detective alone is never sufficient for an action whose harm is irreversible.

Two qualifications that distinguish a professional-level answer:

- **Detection is the primary control for slow-onset risks** — model or prompt drift, emergent disparate impact, index degradation, misuse of legitimately granted access. There is no discrete action to gate, so monitoring *is* the mitigation. Eliminating every "monitor it" option is a trained reflex that costs items.
- **Logging can be independently mandated, not a fallback.** Under the EU AI Act, record-keeping (Art. 12) and human oversight (Art. 14) are *separate* obligations for high-risk systems [D05-V28, D05-V29]. Removing the capability that caused an incident does not discharge either.

Governance vocabulary is four-way, not three-way: **avoid** (don't build it / don't use the model for that step), **reduce** (the controls above), **transfer** (indemnity, insurance, contractual liability allocation), **accept** with a named owner and a documented residual risk. "We accept this, signed by the risk owner" is a legitimate answer the three-way split cannot express.

### 2.3 Narrowed authority, and whose authority the call carries

When the role genuinely needs the capability, the move is to narrow the authority, not to remove the tool and not to log it:

| Lever | Example |
|---|---|
| Per-transaction limit | Credit capped at $50; anything above routes to a gate |
| Budget / rate / quota | Per-agent daily spend; calls per minute |
| Credential scope | Read-only role; single-tenant key; short-lived token |
| Tenancy scope | Per-tenant index or database role, enforced at the data layer |
| Idempotency | One credit per order ID, replay-safe |
| Staged rollout | Canary cohort plus a kill switch |

**Runtime identity is the governance question behind most data-leak incidents.** Every tool call carries *someone's* authority, and there are three answers: the **agent's service account** (the widest, and the one that produces confused-deputy failures — the agent does something the requesting user could not have done), an **end-user delegated credential** (the agent can only reach what this user could reach), or a **per-tenant scoped credential**. Cross-tenant leakage, over-privileged retrieval, and "the agent read a record that user was not entitled to" are all the same defect. Enforce scoping in the data layer and propagate identity; a prompt instruction to respect tenancy is not a control. See Domain 3 for token exchange, OAuth scopes, and isolation mechanics.

### 2.4 Reversibility is a design choice, not a property of the action

Define it operationally: **an effect is irreversible if the operator cannot undo it within the harm window, at acceptable cost, without the counterparty's cooperation.** A sent email is irreversible; a drafted email is not. A soft-deleted document with a 30-day restore window is not.

This reframes the human-in-the-loop question. Before gating an action with a person, try to move it into the reversible column: pending/staged state, undo window, delayed settlement, soft delete, claw-back, two-phase commit, holdback execution of a batch. Then:

> **Irreversible + high impact → first make it reversible; gate with a human only the residue that cannot be made reversible, and only where a qualified reviewer is available inside the action's latency budget at the expected volume.**

A card-freeze decision with a one-second budget cannot have a synchronous human gate; the architecture is automate + fast self-service reversal + monitored reversal rate. A gate no one can staff at 3 a.m. is a queue, not a control.

### 2.5 Failure modes, grouped by plane

Each mode has a *specific* mitigation; "test more" is never the answer.

**Data plane (what reaches or leaves the model)**
- *Hallucination/fabrication* → retrieval grounding, quote-extraction-first for long documents, citation-then-verify with retraction of unsupported claims, explicit permission to abstain. These "significantly reduce" but "don't eliminate" hallucination [D05-S20].
- *Indirect prompt injection* (trusted user, adversarial third-party content) → put untrusted content **only** in `tool_result` blocks, never in `system` or plain user text; label provenance explicitly; JSON-encode untrusted strings to prevent breakout; never place your own instructions inside a tool result; screen tool output before the model sees it [D05-S19].
- *Direct prompt injection / jailbreak* (the user is the adversary) → input screening with a small classifier model and structured outputs, hardened system prompt, throttling repeat offenders [D05-S19].
- *Cross-tenant leakage* → tenant scoping at the data layer plus identity propagation (§2.3), not a prompt filter.
- *Leakage into logs and derived stores* → redact or tokenize before persistence; design delete-by-tenant/document-ID into vector indices and caches, or erasure requests are unimplementable.

**Action plane (what the system can do)**
- *Excessive agency* → remove capabilities the role does not need; narrow authority where it does.
- *Improper output handling* (OWASP LLM05:2025 — the 2023 name "insecure output handling" is retired) → treat model output as untrusted input to the next system: parameterized queries, output encoding at the rendering boundary, schema validation, sandboxed execution [D05-V17].
- *Supply-chain / third-party tool-server trust* → verified or pinned sources, sandboxed execution with egress restriction, its own least-privilege credential, mediated and logged invocation [D05-S23].

**Drift plane (what changes underneath you)**
- *Silent behavior drift* → version-pin models and prompts as controlled artifacts; regression-gate every change; canary with automatic rollback.
- *Emergent disparate impact* → segmented outcome monitoring (§2.9).
- *Over-reliance / automation bias* → sampled audits, injected known-bad cases in review queues, tracked override rates.

**The design premise that ties the action plane together: assume injection succeeds.** No documented mitigation makes injection impossible; least privilege "reduces blast radius of a successful injection rather than trying to make injection impossible" [D05-S19]. Where all the standard mitigations are already present, the remaining move is containment — remove the write scope, run the untrusted-content step in a tool-free context, separate the reading identity from the acting identity, require a human to send.

### 2.6 Human-in-the-loop: tier, trigger, and whether the review is real

Five tiers, decreasing coverage and increasing throughput: **100% review → risk-tiered review → triggered escalation → statistical sampling → post-hoc audit**. This ladder is a design framework synthesized from practice [D05-S25], not published Anthropic or standards-body doctrine; the *reasoning* is what transfers.

- **Choose the tier from reversibility × impact of the specific action class, not of the system.** One agent commonly needs different tiers per tool: "draft reply" = post-hoc audit; "refund over $1,000" = gate before execution.
- **Self-reported model confidence is not a calibrated probability and is not a usable trigger on its own.** Confidently wrong output exists. Usable triggers: retrieval-score floor, self-consistency across samples, novelty/out-of-distribution detection, validator or schema failure, value threshold, irreversibility flag, anomaly signal.
- **The review must be meaningful, or it is not a control.** Operationally the reviewer has (a) access to the underlying inputs, (b) authority to overrule, (c) a caseload that permits consideration, and (d) a measured override rate that is not approximately zero. Reviewer capacity and coverage hours are constraints, not assumptions.

Anthropic's Usage Policy is a floor here: in defined high-risk domains (legal, healthcare, insurance, finance, employment and housing, academic testing/admissions, media and journalism) a qualified professional must review the content or decision before dissemination or finalization, and AI involvement must be disclosed to the user [D05-S21].

### 2.7 Guardrail engineering: the five decisions

Objective 1 items live here, not in the taxonomy.

1. **Where the screen sits.** Input screening catches the adversarial user; an **output screen is the one you cannot skip**, because it is the only layer that sees the consequence of an injection you failed to prevent.
2. **Fail-open or fail-closed when the guardrail is unavailable.** A deliberate design decision, set by the same cost ratio as the threshold: fail closed where a false negative is the expensive error (clinical, financial, safety), fail open where refusal is the expensive error (internal drafting behind human review). "We never thought about it" defaults to fail-open, which is a finding.
3. **Streaming or buffered.** You cannot retract a token you already streamed. A streamed surface needs buffering before release, a post-stream retraction path, or a control that does not depend on inspecting the complete output.
4. **Graduated response, not a binary block.** Warn, redact, ask a clarifying question, downgrade to a safe answer, or route to a human — a block/allow toggle cannot express the right answer for ambiguous input.
5. **Where the threshold comes from.** You cannot locate an operating point without a **labeled harm set**; without one, "tune the threshold" is guesswork. Budget the guardrail's own latency and cost, and decide what happens when the guardrail is the single point of failure. Anthropic's documented pattern is a small, fast model as the screen with structured outputs [D05-S19]. Eval construction for these sets is Domain 4.

### 2.8 Compliance primitives

**Role chain first.** Anthropic is the data processor on the Claude API, Claude Platform on AWS, and Claude in Microsoft Foundry; on Amazon Bedrock and Google Cloud the cloud provider is the processor [D05-S04]. Your own organization's role is set by **contract, not architecture**: a SaaS vendor building on Claude is typically a processor for its own customers, which changes who answers a data-subject request, who owes the impact assessment, and who may decide retention. "Who answers the DSAR" is the decision this concept drives.

**Retention.** Prompts and outputs are not retained by default on the Claude API; the exception is the provider-designated **Covered Models**, which require a 30-day retention window and are therefore **not zero-data-retention eligible unless expressly authorized** [D05-S04, VF]. That makes "we require ZDR" and "we want a Covered Model" mutually exclusive requirements — one has to give. Covered Models are the Fable- and Mythos-class models; **Mythos variants are restricted-access, not generally available** [VF]. A separate exception survives every arrangement: content flagged for trust-and-safety review may be retained for up to two years [D05-S04, accessed 2026-09-24]. No architecture can promise a customer absolute erasure.

**GDPR.** Art. 5 purpose limitation and data minimization bound what may reach a model at all [D05-S12]. Art. 22 restricts *solely* automated decisions with legal or similarly significant effect to three bases — EU/Member-State law with safeguards, explicit consent, contract necessity — and the Art. 22(3) safeguards (human intervention, expressing a view, contesting the decision) attach to the consent and contract bases, not the law-authorized one [D05-S13]. The statutory exceptions exist, but their availability in consumer-credit-type contexts is contested; the architecturally safe design keeps meaningful human involvement plus a contestability path regardless of which basis counsel asserts. Note also that HIPAA de-identification (Safe Harbor's enumerated identifiers, or Expert Determination) is a **defined-method** US construct [D05-S15]; GDPR anonymization is an **outcome test** with no enumerated list, so "de-identified per Safe Harbor" does not remove EU personal data from scope.

**HIPAA.** Protected health information may flow only to a BAA-covered surface with HIPAA readiness enabled **at the organization level**, restricted to eligible features; ineligible-feature requests under a HIPAA-enabled organization return `400` (with a documented carve-out: certain client-side tools are accepted but remain outside HIPAA readiness) [D05-S04, D05-S05]. Two architect-grade consequences: readiness is org-level and **permanent once enabled**, so a HIPAA workload belongs in a separate organization from general-purpose workloads; and identifiers must never appear in JSON schema definitions — property names, `enum` and `const` values, or regex patterns [D05-S04]. Minimum-necessary [D05-S14] and de-identification [D05-S15] reduce exposure before any technical safeguard is needed. On the cloud surfaces the BAA is with the cloud provider: Bedrock is a HIPAA-eligible AWS service under an AWS BAA [D05-V26]; on Google Cloud, confirm the specific product appears on Google's covered-products list before routing PHI — "Vertex AI" is not named there by that name [D05-V27]. HIPAA readiness is **not** available on Claude Platform on AWS or Microsoft Foundry [D05-S04].

**Public sector (FedRAMP, CUI) — teach the procedure, not the matrix.** Authorization attaches to an **environment boundary**, not to a model version, and "there is no separate FedRAMP audit per model" — new models inherit the environment's authorization [D05-V09, VF]. The four-step architect procedure:

1. **Identify the obligation** — the agency's own data categorization and the baseline it requires, and whether the mission is DoD. FedRAMP baselines (Low/Moderate/High) and DoD Impact Levels (IL2/4/5/6) are *different constructs*: ILs come from the DoD Cloud Computing SRG and apply to DoD workloads. **Controlled Unclassified Information does not require a DoD Impact Level** [VF, D05-V32].
2. **Choose an authorized surface.** As of 2026-09-24: **Claude for Government** is Anthropic's FedRAMP High offering; **Claude in Amazon Bedrock (AWS GovCloud)** is approved for FedRAMP High and DoD IL4/5 workloads; **Claude on Google Cloud Vertex AI with Assured Workloads** is FedRAMP High and IL2 authorized. CUI may be processed in a FedRAMP High environment via any of the three [VF, D05-V08, D05-V05, D05-V06]. The narrow true point about the first-party path is that the **standard commercial Claude API is not the FedRAMP route** — a public-sector deployment moves to Claude for Government or an authorized cloud-provider path [D05-V08, D05-V10].
3. **Confirm the current authorization *and* model availability** for that surface at engagement time; model availability inside Claude for Government is its own question [D05-V09].
4. **Document the evidence** — the ATO package, the boundary diagram, and which authorization the system inherits. Reuse of an existing agency ATO is usually the cheapest correct answer. Reclassification of the data belongs to the agency's classification authority, not the architect.

**Frameworks.** EU AI Act: four tiers named *unacceptable risk, high risk, transparency risk, minimal or no risk*; prohibitions in force 2 Feb 2025; Art. 50 transparency from 2 Aug 2026 (with a 2 Dec 2026 window for synthetic-media providers); high-risk obligations moved by the AI Omnibus (in force 27 July 2026) to 2 Dec 2027 for Annex III and 2 Aug 2028 for Annex I [D05-S16, D05-V13, D05-V15]. NIST AI RMF: voluntary, four functions — Govern, Map, Measure, Manage — applied iteratively [D05-S17]. ISO/IEC 42001: certifiable AI management system standard, held by Anthropic alongside SOC 2 Type I/II and ISO 27001:2022 [D05-S02, D05-S18]. OWASP Top 10 for LLM Applications (2025) is an engineering baseline, not law, and the verbatim current names matter: Prompt Injection, Sensitive Information Disclosure, Supply Chain, Data and Model Poisoning, Improper Output Handling, Excessive Agency, System Prompt Leakage, Vector and Embedding Weaknesses, Misinformation, Unbounded Consumption [D05-V17].

*Misconception across all of these:* that a framework is satisfied by the vendor's certifications. Each is satisfied by the combination of vendor posture and your own design — minimization, oversight, retention, logging, evidence.

### 2.9 Ethical AI, operationalized

- **Removing a protected attribute does not remove disparate impact.** Correlated features — postal code, school, device, language, name, tenure — reconstruct the signal. "We deleted the gender field from the prompt" is not a fairness control; the test is whether **outcome rates differ across segments in the deployed pipeline**.
- **Measure the system, not the model.** Thresholds, retrieval coverage, language support, OCR quality, and fallback paths produce disparity even where the model is even-handed. Anthropic's published paired-viewpoint, model-as-judge even-handedness evaluation [D05-V23] is a good example of *eval discipline* — a designed, repeatable, segmented set re-run on change — but it is **not** the template for disparate-impact review of a deployed decision system, where you need segmented outcome-rate comparison on real or held-out decisions, and where a judge model scoring the system under test has an independence problem.
- **Several standard fairness criteria cannot be satisfied simultaneously.** Equal error rates, equal outcome rates, and within-group calibration conflict when base rates differ, so someone must **choose and document the metric and the tolerance** before launch. That choice is a governance decision with a named owner, not a technical default. `[UNVERIFIED]` — this impossibility result is standard in the fairness literature but no primary citation was verified in this session; teach the consequence (choose and document), not a specific theorem attribution.
- **"No complaints" is uninformative without a channel.** Absent a feedback and appeal path, complaint volume measures the absence of a mechanism.
- **Explainability vs. grounding.** Anthropic documents citations as returning valid pointers into the provided documents — citations "are guaranteed to contain valid pointers" [D05-V21, VF]. A valid pointer proves **provenance**: which passage the claim was drawn from. It does not prove the source is correct, that the claim is entailed by the passage, or that the model's stated rationale is the process that produced the output. Grounding "significantly reduces" but does not eliminate hallucination [D05-S20]. **Citations are an auditability affordance, not an explainability guarantee.**
- **Therefore: don't use the model for the decision when the regime requires reasons.** Where an affected person is owed specific reasons, the defensible architecture produces the decision from an interpretable model or deterministic rule set and confines Claude to assembling the file and drafting the explanation from the decision's own reason codes. A post-hoc rationale a model writes about its own output is not evidence of the process that produced it.
- **Transparency and contestability.** Disclose AI involvement — a floor under Anthropic's Usage Policy for high-risk domains and consumer chatbots [D05-S21] and an independent requirement in the EU AI Act's transparency-risk tier (Art. 50) [D05-S16]. Contestability is a designed appeal path, not merely a gate on the way in [D05-S13].

### 2.10 Governance mechanics

Prompts, model IDs, retrieval indices, and guardrail thresholds are **controlled artifacts**: versioned, reviewed, regression-gated against a fixed eval set before promotion, with a rollback path and a named approver for exceptions. AI incident response differs from classical IR in what can be rolled back — the defect is often a prompt, a threshold, or an index rather than code, so the runbook must name who can roll back each one, whether a kill switch exists, and what the notification duty is. Documentation artifacts an architecture should be able to feed: model/system cards, an AI risk register with a named owner (a NIST RMF "Manage" output) [D05-S17], and impact assessments.

---

## 3. Trade-off analyses

### T1 — Control placement (the two axes made concrete)

| Control layer | Bypass resistance | Expressiveness | Cost | Characteristic failure |
|---|---|---|---|---|
| Remove the capability | Highest — nothing to bypass | Lowest — binary; the function is gone | Free, or the lost use case | Applied where the role actually needs the function |
| Deterministic code (allow-list, schema, predicate) | High for exactly what it checks | Low–medium — only the specifiable | Low | Mis-specified; unenumerated cases pass |
| Narrowed authority (cap, quota, credential, tenancy, idempotency) | High — enforced outside the model | Medium — bounds magnitude, not judgment | Low–medium | Scope creeps; nobody reviews it |
| Model-based classifier / screen | Medium — promptable, has false negatives | High — judges the fuzzy | Medium (extra call, latency) | Trusted as deterministic; unmeasured threshold |
| Human approval gate | Medium–high, decays with volume | Highest — discretion and context | Highest (latency, staffing) | Rubber stamp: ~0% override, no access to inputs |
| Prompt instruction | Lowest — no enforcement outside the weights | High — states anything | Near zero | Presented as the whole control |

**Choose** deterministic code or removal wherever the constraint is specifiable; **narrowed authority** when the capability is required; **a classifier** for fuzzy judgment that does not need a person; **a human gate** for judgment that cannot be reduced to a predicate; **a prompt instruction** as a necessary layer that is never the whole answer.

### T2 — Preventive vs. detective vs. compensating

| Axis | Preventive | Detective | Compensating |
|---|---|---|---|
| When it acts | Before the harm | After / continuously | Alongside; bounds impact |
| Answers | Can this happen? | Did this happen? Is it drifting? | How bad can it get? |
| Sufficient alone? | Never where logging, human oversight, or post-market monitoring are independently mandated [D05-V28, D05-V29] | Never for an irreversible discrete action; **primary** for slow-onset risk (drift, disparity, degradation, insider misuse) | Only with accepted, owned residual risk |
| Example | Remove the delete tool | Segmented outcome monitoring | Per-transaction cap, undo window |

### T3 — Guardrail strictness, response shape, and unavailability

| Axis | Strict / fail-closed | Loose / fail-open |
|---|---|---|
| Error you are buying | Over-refusal (false positive) | Harm passes through (false negative) |
| Right domain | Irreversible, regulated, clinical, financial | Low-stakes drafting behind human review |
| Behavior when the screen is down | Safe fallback plus human path | Serve, and reconcile after the fact |

*Discriminator:* the operating point and the unavailability behavior are both set by the **cost of a false negative relative to a false positive in that domain** — and you cannot locate either without a labeled harm set. Prefer a **graduated** response (warn, redact, clarify, downgrade, route to a human) over a binary block; a binary toggle cannot express the right answer for ambiguous input.

### T4 — Human review tiers vs. reversibility engineering

| Option | Coverage | Cost / latency | Fatigue risk | Requires | Best for |
|---|---|---|---|---|---|
| Make the action reversible | Structural | Low | None | Undo/staging design, claw-back path | Anything where a staged or undoable state is feasible |
| 100% review | Complete | Highest | Highest | Reviewer capacity at volume and hours | Low-volume, high-impact, truly irreversible |
| Risk-tiered review | Matches risk class | Medium | Medium | A risk classification per action | Mixed-risk action sets (most agents) |
| Triggered escalation | Flagged subset | Low | Low | External trigger signals, not self-reported confidence | High volume with measurable signals |
| Sampling / post-hoc audit | Partial | Lowest | Lowest | Tolerance for harm already done | Reversible, low-impact actions |

*Discriminator:* tier by reversibility × impact **of the action class**, after asking whether the action can be made reversible at all — and check that a qualified reviewer exists within the action's latency budget at the expected volume.

### T5 — Compliance-driven deployment surface

Ask first whether the regulated data must cross the boundary at all: field minimization, tokenization with downstream re-identification, structured extraction of only the needed fields, a de-identified index with a separate authorized re-identification step, or keeping the regulated decision out of the model entirely. Surface selection is the *second* question.

| Axis | Commercial Claude API | Claude for Government | Bedrock (AWS GovCloud) | Vertex AI (Assured Workloads) |
|---|---|---|---|---|
| Public-sector posture | Not the FedRAMP route [D05-V08, D05-V10] | Anthropic's FedRAMP High offering [VF, D05-V08] | FedRAMP High + DoD IL4/5 [VF, D05-V05] | FedRAMP High + IL2 [VF, D05-V06] |
| PHI path | Direct BAA + org-level HIPAA readiness, eligible features only [D05-S04, D05-S05] | Out of scope here — public-sector instrument | AWS BAA; Bedrock is HIPAA-eligible [D05-V26] | Google BAA; confirm the product is on Google's covered-products list [D05-V27] |
| Processor | Anthropic [D05-S04] | Anthropic | AWS [D05-S04] | Google [D05-S04] |
| Residency lever | `inference_geo`: `"us"` or `"global"` only, no EU pin; `"us"` bills at 1.1x [D05-S27] | Environment-defined | Region/endpoint; regional endpoints guarantee routing | Region/endpoint |

Microsoft Foundry is a fifth surface with Anthropic as processor and its own US data-zone deployment type; HIPAA readiness is not available there or on Claude Platform on AWS [D05-S04, VF].

> **Authorization snapshot — accessed 2026-09-24. Re-verify before any engagement relies on it.** Claude for Government: FedRAMP High. Bedrock in AWS GovCloud: FedRAMP High and DoD IL4/5. Vertex AI with Assured Workloads: FedRAMP High and IL2 (announced April 2025). Authorization attaches to the environment, not the model version [D05-V09]. Do not memorize these as durable facts; memorize the four-step procedure in §2.8.

### T6 — Data minimization vs. retrieval richness

| Axis | Minimal / structured retrieval | Rich whole-document retrieval |
|---|---|---|
| Grounding quality | Risk of missing context | Higher |
| Regulated-data exposure | Smaller | Larger unless de-identified first |
| Erasure implementability | Easier — fewer derived copies | Harder — index and cache entries must be deletable by tenant/document ID |

*Discriminator:* the mechanisms, not the posture — tokenize or de-identify **before** retrieval, extract only the needed fields, and scope indices by **purpose and tenant** so the minimization argument is structural rather than re-argued per request.

### T7 — Observability vs. privacy obligations

| Axis | Full raw-content logging | Reversible tokenization | Irreversible redaction / hashing |
|---|---|---|---|
| Debuggability | Highest | High | Reduced |
| Regulatory scope | Logs become a second regulated store | **Still personal data**; the token vault is itself a regulated store | Materially reduced |
| Retention effect | Conflicts with minimization and storage limitation | Reduced, not eliminated — retention must stay bounded and the token map deletable | Longest defensible retention |

*Discriminator:* keep structural metadata (latency, tool name, token counts, decision codes) fully observable and treat the sensitive payload separately — irreversible redaction where you will never need the value, a separately access-controlled reversible token where you will, and a log of a replayable record ID instead of the payload where that suffices. Pseudonymization is not anonymization.

### T8 — Fairness gate: aggregate metric vs. segmented metric

| Axis | Aggregate accuracy gate | Segmented outcome gate |
|---|---|---|
| What it detects | Overall quality regression | Per-segment divergence in the *deployed* pipeline |
| Cost | Low — one number | Segment definitions, volume per segment, a declared metric and tolerance |
| Blind spot | A large per-segment gap can leave the aggregate unchanged | Small segments are noisy; the metric choice is contestable |

*Discriminator:* gate on the segmented metric for any system whose outputs affect people's access to money, housing, employment, care, or benefits; declare the metric and tolerance in advance (they conflict — see §2.9) and name the owner. Aggregate accuracy remains the quality gate, not the fairness gate. Eval construction and cadence belong to Domain 4; what to slice and how often is this chapter's concern.

---

## 4. Worked scenarios

**1 — Healthcare: clinical documentation assistant.** *Situation:* a hospital wants Claude to draft visit summaries from clinician dictation that references diagnoses, medication histories, and patient identifiers, and the drafted note enters the medical record. *Constraints:* the hospital already holds a BAA with its cloud provider; the product team wants the provider's strongest reasoning tier; procurement wants a contractual no-retention commitment. *Candidates:* (a) commercial API, no special configuration; (b) a BAA-covered surface with HIPAA readiness enabled in a **separate organization**, restricted to eligible features, with identifiers tokenized before the call and clinician sign-off before the note enters the record; (c) de-identify everything first and forgo the BAA. *Recommended:* (b). *Why the others lose:* (a) routes identifiable health data to a non-covered configuration — that is the violation itself; (c) discards clinical detail, and reliable de-identification of free-text dictation is itself unsolved. *The real discriminators:* HIPAA readiness is org-level and permanent, so this workload needs its own organization; the eligible-feature restriction is what teams actually get wrong; and the "strongest tier + no retention" pair is **unsatisfiable** if that tier is a Covered Model, which requires 30-day retention and is not ZDR-eligible absent express authorization [D05-S04, VF] — one requirement must give, and trust-and-safety retention means absolute erasure cannot be promised anyway. *Changes the answer:* an aggregate, already-de-identified analytics use case makes (c) viable and cheaper. A dictated note that a clinician never signs is a draft, not a record, which relaxes the gate but not the data-handling posture.

**2 — Financial services: underwriting assistant.** *Situation:* an EU-facing lender wants Claude to recommend approve/deny; a denial affects the applicant's access to credit and the regulator expects specific reasons. *Candidates:* (a) automate and log for audit; (b) add a loan-officer confirmation step to every recommendation; (c) keep the decision in the existing interpretable scoring model, use Claude to assemble the file and draft the applicant-facing reasons from the model's reason codes, and give officers real discretion over exceptions plus a contestability path. *Recommended:* (c). *Why the others lose:* (a) is detective — the wrongful denial already happened — and a solely automated decision with a significant effect needs a qualifying basis [D05-S13]; (b) looks like compliance but a reviewer with 300 files a day, no access to the underlying record, and a ~0% override rate is a rubber stamp, and a model's own post-hoc rationale is not the explanation the regime wants (§2.9). *Changes the answer:* if the decision genuinely cannot come from an interpretable model, the fallback is (b) *plus* the meaningfulness conditions in §2.6 and a documented lawful basis — and reviewer capacity becomes the binding constraint on volume.

**3 — Public sector: benefits chatbot.** *Situation:* a federal civilian agency wants a chatbot answering benefits questions from internal policy documents that are marked not publicly releasable and subject to handling restrictions. The agency already holds an ATO covering a FedRAMP High environment for another system. *Candidates:* (a) call the commercial Claude API and keep the corpus in a private index; (b) run in the already-authorized FedRAMP High environment, confirm the needed model is available there, and document boundary and model availability as ATO evidence; (c) assume a DoD Impact Level is required and stand up a new GovCloud boundary. *Recommended:* (b) — inherit the authorized boundary. *Why the others lose:* (a) the commercial API is not the FedRAMP route; the move when a requirement lands is to change the surface, not to add a prompt instruction or a private index [D05-V08]. (c) over-constrains and buys a new authorization the agency does not need: **Impact Levels are a DoD Cloud Computing SRG construct and are not a prerequisite for controlled unclassified information at a civilian agency** [VF, D05-V32]; all three Claude public-sector paths were FedRAMP High as of 2026-09-24. *Changes the answer:* a DoD component changes the baseline conversation to Impact Levels; a genuinely public-releasable corpus reopens cheaper surfaces — but classification is the agency's call, not the architect's; and if the needed model is not yet available inside the authorized environment, the choice is wait, use an available model, or authorize another boundary [D05-V09].

**4 — Payments: treasury operations agent.** *Situation:* an agent drafts and submits supplier payments; finance requires same-day execution, so routing every payment to a human defeats the purpose. Payments must only ever reach pre-approved beneficiaries. *Candidates:* (a) a classifier that screens each payment destination for legitimacy; (b) a system prompt listing approved beneficiaries; (c) enforce the beneficiary allow-list in the payment service, cap per-transaction and daily amounts, require an idempotency key per invoice, issue the agent a scoped credential that can only submit (not create) payees, and gate only payments above the cap. *Recommended:* (c). *Why the others lose:* (a) a model-based screen is promptable and has a false-negative rate on a constraint that is perfectly specifiable — this is the canonical case for deterministic enforcement; (b) has no enforcement outside the weights. *Changes the answer:* if the requirement were "flag payments that look unusual for this supplier relationship," no predicate expresses it and a classifier plus a review queue becomes correct — the constraint's expressibility decides the layer, not a ranking of layers.

**5 — Housing: tenant-screening assistant.** *Situation:* a property manager uses Claude to summarize applicant files and recommend "approve / refer to manual review." The team removed the applicant's protected attributes from the prompt; pre-launch aggregate accuracy passed; six months later, no complaints have been received. *Candidates:* (a) treat the launch eval as sufficient evidence; (b) re-run the same aggregate eval on the current model version; (c) measure outcome rates in the *deployed* pipeline sliced by the segments of concern and their likely proxies, declare the fairness metric and tolerance in advance with a named owner, gate releases on it, and open a feedback and appeal channel. *Recommended:* (c). *Why the others lose:* (a) and (b) both measure the wrong thing — deleting an attribute does not remove the signal carried by correlated features (postal code, prior address stability, language of the file), and an aggregate number can be unchanged while a segment gap opens; "no complaints" measures the absence of a channel. *Changes the answer:* if segments are too small for a stable rate, the answer becomes pooling periods, a pre-declared minimum detectable difference, and a manual-review default for the sparse segment — not dropping the measurement. Note that fairness criteria conflict, so the choice of metric must be documented as a governance decision, not presented as the neutral one.

**6 — Engineering: agent using third-party tool servers.** *Situation:* a platform team wants an agent to use community-maintained tool servers to query internal systems and file tickets. Today the servers inherit the agent's privileges, and the agent's service account can read every tenant's records. *Candidates:* (a) install what is useful and rely on the model to behave; (b) install only verified servers, sandbox them, and monitor invocations; (c) (b) **plus** fix the authority: each server runs under its own least-privilege credential, the data-access path uses a short-lived credential scoped to the requesting user and tenant, tenancy is enforced at the data layer, servers are pinned at a reviewed version, traffic is mediated through a gateway that allow-lists and logs calls, and the sandbox has restricted egress. *Recommended:* (c). *Why the others lose:* (a) ignores documented supply-chain risk — a compromised server can exfiltrate or execute regardless of model alignment [D05-S23]; (b) is the common answer and leaves the confused-deputy defect untouched: privilege inheritance, not server provenance, is what makes the blast radius unacceptable. *Changes the answer:* a path touching regulated data may justify hand-written tools for that path only. Mechanics of credential exchange and isolation are Domain 3's.

---

## 5. Failure modes & diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| Confident-but-wrong after a content refresh; model and latency unchanged | Retrieval returning stale or irrelevant chunks | Re-index freshness, embedding match, chunk relevance | Rebuild/validate the index; add a retrieval-quality eval — not a model swap [D05-S30, Sample 3] |
| Agent took an unexpected destructive action | Excessive agency, or a successful injection | Tool manifest for that role; recent tool-call logs | Remove the unneeded tool; narrow authority where it is needed; isolate untrusted content to tool results |
| A user received another tenant's data | Scoping applied in the prompt, or the agent's service account is over-broad | Whether tenant identity is enforced in the data call itself | Enforce tenancy at the data layer; propagate user identity with a scoped, short-lived credential |
| Model output caused an injection/XSS/RCE downstream | Output treated as trusted input by the consuming system | The boundary where output is executed or rendered | Parameterize, encode at the boundary, validate against a schema, sandbox |
| Identifiers appear in logs, traces, or a vector index | No redaction before persistence; no delete path in derived stores | Logging pipeline config; whether the index supports delete-by-tenant/document ID | Redact or tokenize before write; build erasure into derived stores |
| Approval/denial rates diverge by segment while aggregate accuracy is flat | Fairness gate measured the aggregate, and the model rather than the pipeline | Outcome metrics sliced by segment and proxy; threshold and retrieval coverage per segment | Segmented outcome gate with a declared metric, tolerance, and owner (§T8) |
| Reviewers approve nearly everything | Automation bias, or review without access/authority/capacity | Override rate over time; reviewer caseload; what the reviewer can actually see | Reduce volume by tiering; grant access and authority; inject known-bad cases |
| Behavior changed after a routine deploy | Prompt, threshold, index, or model version changed without a gate | Diff against the last known-good eval run | Treat all four as controlled artifacts; regression gate plus canary and rollback |
| Refusal complaints spike after a guardrail change | Operating point moved without a cost-ratio rationale | Recent threshold/classifier changes; the labeled harm set | Re-locate the threshold against domain-specific error costs; prefer graduated responses |
| Requests fail when the screening service is down | Unavailability behavior never specified | Whether the design fails open or closed, and by decision | Choose deliberately per domain; add a safe fallback and a human path |

---

## 6. Anti-patterns

- **Logging as prevention.** An audit trail offered as the fix for a risk that needs a preventive or compensating control. Necessary; never sufficient.
- **Guardrail as suggestion.** A prompt instruction treated as sufficient for a financial, safety-critical, or irreversible risk. Fast to ship; holds until the first adversarial input.
- **Removal reflex.** Deleting a capability the role demonstrably needs, because "least privilege" was learned as a slogan. The answer there is narrowed authority.
- **The gate that cannot be staffed.** A synchronous human approval on a 24/7, high-volume, or sub-second action. It is a queue, or a rubber stamp, not a control.
- **Review theater.** A confirmation click with no access to the underlying record, no authority to overrule, and no throughput budget — measurable as a ~0% override rate.
- **BAA-washing.** Assuming a signed agreement makes any product use compliant, without org-level enablement, feature eligibility, or minimization.
- **ZDR-washing.** Promising a customer that a zero-retention arrangement means nothing is retained anywhere, ignoring that flagged content can be retained for up to two years and that Covered Models require a retention window [D05-S04, VF].
- **Fairness-washing.** One pre-launch aggregate check, unsegmented, on the model rather than the deployed pipeline, with no appeal channel — then citing the absence of complaints as evidence.
- **Confused-deputy agent.** Tools called under the agent's service account, with tenancy enforced in the prompt. Every cross-tenant incident has this shape.
- **Kitchen-sink tool agent.** Every tool "in case," maximizing blast radius for every future injection or misconfiguration.
- **Regex redaction as a complete solution.** Pattern matching catches formatted identifiers; free-text clinical or personal detail rarely matches cleanly, and the false confidence is the risk.
- **Compliance theater by document.** A model card and risk register produced once at launch, then treated as governance-complete.

---

## 7. Exam-day heuristics

- **Remove the capability when the role's actual task does not require it.** When it does, narrow the authority — scope, cap, rate, tenancy, credential lifetime — rather than removing the tool or logging its use [D05-S30, Sample 1].
- **Express it deterministically if it can be expressed deterministically.** A predicate beats a model-based screen on any specifiable constraint; a classifier earns its place only on judgment no predicate expresses.
- **A prompt instruction is never *sufficient* alone for a material risk** — but where the constraint is genuinely fuzzy, the correct option adds measurement and containment, not the deletion of the prompt.
- **Irreversible + high impact → first make it reversible**, then gate only the residue, and only where a qualified reviewer exists inside the latency budget at volume.
- **A human gate is for judgment that cannot be reduced to a predicate.** Fully constrain the action's parameters in code and the deterministic control substitutes for the gate.
- **Detective controls never answer "how do we prevent"** — except for slow-onset risks (drift, disparity, degradation, insider misuse), where detection *is* the control, and except where logging is independently mandated.
- **Vendor posture is necessary and never sufficient.** The best option names both the instrument (BAA, DPA, authorized boundary) and the customer-side obligation.
- **Compliance posture is chosen at the deployment surface or the contract — never in the prompt.** And the prior question is whether the regulated data needs to cross the boundary at all.
- **FedRAMP baseline ≠ DoD Impact Level.** Controlled unclassified information calls for a FedRAMP High environment; Impact Levels are a DoD construct for DoD missions. Authorization attaches to the boundary, not the model version, so verify current authorization *and* model availability.
- **Confident-but-wrong after a data refresh, model and latency unchanged → the data plane, not the model.**
- **Citations prove provenance, not correctness or entailment** — and never the model's reasoning. Where reasons are owed, the decision should not come from the model.
- **Deleting a protected attribute is not a fairness control**, and an aggregate metric is not a fairness gate.

---

## 8. Practice items

Twelve items. Each states how many options to select.

**Item 1 (select 1).** A freight carrier's support agent can look up shipments, draft replies, and issue goodwill credits. Operations data shows about one in five calls is resolved with a credit, and the business requires same-call resolution. Credits are currently uncapped. Which change best reduces risk while preserving the workflow?

A. Remove the credit tool from this agent and route every credit request to the back-office billing team for handling.
B. Keep the credit tool and require the agent to display a confirmation dialog to the representative before each credit is issued.
C. Cap credits per transaction and per representative per day, require an idempotency key per shipment, and gate anything above the cap.
D. Keep the credit tool and log every credit with representative, shipment, and amount for a weekly reconciliation review.

*Key: C.* The role genuinely needs the capability, so the move is narrowing authority. **A** removes a capability the stated workflow requires, breaking same-call resolution. **B** is a weak gate on an unbounded capability: a rushed or misled representative confirms, and the amount is still unlimited. **D** is detective — reconciliation finds the loss after the money has moved.

**Item 2 (select 1).** A treasury agent submits supplier payments. Policy is that funds may only ever reach beneficiaries already on an approved payee list maintained in the ERP. Which control most reliably enforces the policy?

A. Screen each proposed payment destination with a separate classifier model trained to recognize unapproved or suspicious beneficiaries.
B. Enforce the approved-payee list inside the payment service, rejecting any submission whose destination is not present on it.
C. Include the current approved-payee list in the system prompt and instruct the model to submit payments only to those destinations.
D. Have a second model review the first model's proposed payment and require the two to agree before submission proceeds.

*Key: B.* The constraint is exactly specifiable, so it belongs in deterministic code outside the model. **A** substitutes a promptable component with a false-negative rate for a predicate that has neither. **C** has no enforcement outside the model's weights and leaks the list into context. **D** doubles the cost and correlates the errors; two models can be fooled by the same input.

**Item 3 (select 1).** A behavioral-health provider wants Claude to summarize session transcripts that include diagnoses, medication histories, and member identifiers. A business associate agreement with the provider's Claude vendor is already signed. Which deployment best satisfies the provider's obligations?

A. Run the workload in the company's existing general-purpose organization, using the asynchronous batch endpoint overnight to reduce per-token cost.
B. Run the workload in a dedicated organization with health-data readiness enabled, restricted to eligible features, with member identifiers tokenized before the call.
C. Run the workload in the vendor's consumer chat product so that clinicians can page through transcripts interactively while summaries are produced.
D. Run the workload in the existing organization and add a system-prompt rule forbidding the model from repeating identifiers, with all requests logged.

*Key: B.* Readiness is enforced at the organization level and is permanent once enabled, so a regulated workload belongs in its own organization, restricted to eligible features, with exposure minimized before the call. **A** mixes regulated and general traffic in one organization and reaches for a feature outside the agreement's eligible set. **C** uses a product the agreement does not cover. **D** is a prompt-only control over data that has already crossed the boundary, plus logging that creates a second regulated store.

**Item 4 (select 1).** A federal civilian agency already holds an authorization to operate covering a cloud environment used by another system. A new assistant will answer staff questions from internal documents marked not publicly releasable. The team wants the newest available model. What should the architect do first?

A. Call the vendor's commercial API for the newest model, routing only non-sensitive questions through it and keeping sensitive ones in the authorized environment.
B. Confirm the model is offered inside the already-authorized environment, then document the boundary and that model's availability as evidence for the authorization package.
C. Initiate a separate assessment of the new model itself, since each model version carries its own authorization independent of the environment it runs in.
D. Deploy the model in the authorized environment and rely on the provider's published Department of Defense impact rating to establish the agency's required baseline.

*Key: B.* Authorization attaches to the environment boundary, not the model version, so the architect's job is to inherit the existing boundary and confirm model availability inside it, with evidence. **A** puts part of a system handling restricted documents outside the authorized boundary, and the split is a classification judgment the agency owns. **C** misstates the mechanism: there is no separate per-model authorization. **D** confuses two frameworks — impact levels are a Department of Defense construct and do not set a civilian agency's baseline, which follows the agency's own categorization.

**Item 5 (select 1).** A card issuer must block a compromised card within about one second or the fraudulent transaction settles. The fraud team staffs business hours only; blocks inconvenience legitimate cardholders. Which design best fits?

A. Require a fraud analyst to approve each block before it takes effect, escalating to an on-call analyst outside business hours to preserve coverage.
B. Execute the block automatically, provide immediate self-service unblocking in the app, and review block and reversal rates on a sampled basis.
C. Queue each candidate block for review the next business morning, notifying the cardholder that a hold is pending on the account in the meantime.
D. Execute the block automatically and log every decision with the model's stated confidence so the fraud team can audit decisions weekly.

*Key: B.* The action is inside a latency budget no human meets, so the answer is to automate it and make it reversible, then monitor the reversal rate as the control signal. **A** guarantees the harm the system exists to stop, and on-call staffing does not close a one-second budget. **C** is the same failure with extra latency. **D** automates without a reversal path, leaving affected cardholders with a weekly audit as their only remedy.

**Item 6 (select 1).** A consumer-facing assistant answers medication questions. Every response passes an output screen before display. During an incident the screening service becomes unavailable. What should the design specify?

A. Serve the unscreened response with a visible notice that automated safety checking is temporarily unavailable for this answer.
B. Return a safe fallback response and route the user to a staffed channel, declining to serve unscreened output for this domain.
C. Serve the unscreened response if it is short, on the basis that brief answers are less likely to contain harmful content.
D. Apply the most recent screening decision for a similar question and serve the response on that basis until the service recovers.

*Key: B.* Unavailability behavior is a design decision set by which error costs more; where a false negative is a medication-safety harm, the system fails closed with a fallback and a human path. **A** fails open in the domain where that trade is worst, and a notice transfers risk to the user. **C** invents a proxy for harm with no basis in a labeled harm set. **D** applies a decision made about different content, which is not a screen at all.

**Item 7 (select 1).** A retailer's product-description assistant writes copy that is stored and later rendered directly into customer-facing pages. A security test shows model output containing markup can execute in the visitor's browser. What is the correct fix?

A. Instruct the model in its system prompt never to emit HTML, script tags, or other markup in generated product descriptions.
B. Add an output classifier that inspects each generated description for malicious strings and blocks any that appear dangerous.
C. Encode or escape the stored output at the rendering boundary and allow only a validated subset of markup through to the page.
D. Sanitize the merchant-supplied input fields before they are placed in the prompt so that no markup reaches the model at all.

*Key: C.* Model output is untrusted input to the next system, and the defect lives at the boundary where it is rendered; encoding plus an allow-list fixes it there. **A** is a prompt-level control over a deterministic problem. **B** is a probabilistic screen where a parser-level rule is available, and it fails on novel encodings. **D** addresses the wrong boundary: the model can produce markup that no input contained.

**Item 8 (select 2).** A B2B SaaS assistant answers questions for many customer organizations from a shared document index. The service calls the index with the application's own credential, and the current design appends the requesting organization's ID to the prompt with an instruction to use only its documents. Which two changes most reduce the risk of one customer receiving another's data?

A. Pass the requesting user's identity to the retrieval call using a short-lived credential scoped to that user and organization.
B. Enforce organization scoping in the index or database layer, so a query cannot return documents outside the caller's scope.
C. Restate the scoping rule more forcefully in the system prompt and repeat the organization ID immediately before the question.
D. Log every retrieval with the requesting organization and the returned document IDs, and alert on any cross-organization match.

*Keys: A and B.* Together they move the boundary from the prompt to identity and the data layer, which is where it can be enforced. **C** is the same prompt-layer control restated; repetition does not add a layer. **D** is detective — the alert fires after the data has been disclosed. Isolation and credential-exchange mechanics are Domain 3's; the governance point is that the call must carry the user's authority, not the application's.

**Item 9 (select 1).** A property manager's screening assistant recommends "approve" or "refer to manual review." The team removed applicants' protected attributes from the prompt, and aggregate approval accuracy exceeded the pre-launch threshold. They conclude the disparate-impact risk is addressed. What is the strongest objection?

A. Features correlated with the removed attributes can carry the same signal, so the open question is whether outcome rates differ across segments in the deployed pipeline.
B. The evaluation used aggregate accuracy, and a more capable model would raise that number without changing which applicants are referred to review.
C. No single fairness metric is universally correct, so no measurement can settle whether the system treats applicant groups differently.
D. The applicants were not told that an automated system contributed to the recommendation, which is the obligation the team has actually left unmet.

*Key: A.* Deleting an attribute does not remove the signal that correlated features carry, and the test is segmented outcome rates in the deployed pipeline, not the model in isolation. **B** is true about aggregate accuracy but draws the wrong conclusion — capability is not the issue. **C** starts from a real fact (the criteria conflict) and ends in nihilism; the response is to choose, document, and measure one. **D** names a genuine but separate transparency obligation and does not address disparate impact.

**Item 10 (select 2).** An insurer must give claimants the specific reasons for a denial. The team proposes having Claude both decide low-value claims and write the denial letter, with the model's own explanation of its reasoning stored as the reason record. Which two changes most directly satisfy the requirement?

A. Produce the decision from the insurer's existing interpretable rules or scoring model, and have Claude draft the letter from that model's reason codes.
B. Give claimants a path to human review in which they can submit their point of view and contest the outcome, with the outcome recorded.
C. Enable source citations on the model's narrative so each statement in the denial letter carries a pointer into the claim file.
D. Store the model's stated reasoning alongside the decision so the insurer can produce a written rationale for any denial on request.

*Keys: A and B.* The reasons must come from the process that actually made the decision, and a contestability path is the other half of what a consequential-decision regime expects. **C** adds provenance for statements in a letter; a valid pointer shows where text came from, not why the decision was made. **D** stores a post-hoc narrative about an output, which is not evidence of the process that produced it.

**Item 11 (select 1).** A SaaS vendor's enterprise customer demands a contractual commitment that none of its prompts or outputs are retained anywhere in the AI provider's systems. The product team wants to use the provider's strongest reasoning tier, which the provider designates as requiring a 30-day retention window and offers only to approved organizations. What should the architect tell both sides?

A. Enable the retention-required tier in a dedicated workspace and inform the customer that the retention window does not apply to their traffic.
B. Treat the two requirements as incompatible: either choose a tier without the retention requirement or seek an express exception, and disclose the residual retention paths.
C. Request a zero-retention arrangement for the organization and rely on the provider to exempt the retention-required tier from it automatically.
D. Sign a contractual amendment committing to zero retention and keep the tier, since a negotiated commitment overrides the platform's default behavior.

*Key: B.* A designated retention requirement and a zero-retention arrangement are mutually exclusive absent express authorization, so one requirement has to move — and no arrangement supports a promise of absolute erasure, because content flagged for safety review can be retained regardless. **A** asserts an exemption that the workspace mechanism does not create. **C** inverts the relationship: the arrangement excludes the tier rather than the reverse. **D** treats a contract as capable of changing platform behavior it does not control.

**Item 12 (select 2).** A benefits administrator routes every automated eligibility denial to a reviewer who confirms it before it is sent. Each reviewer handles about 300 cases a day, sees only the model's recommendation and a one-line summary, and the measured override rate is under one percent. Which two changes are most necessary for the review to function as a control?

A. Give reviewers access to the underlying case record and explicit authority to overrule the recommendation without escalation.
B. Set a caseload per reviewer that permits actual consideration, and treat the override rate as a monitored control signal.
C. Require a second confirmation action, so that two separate clicks are needed before a denial is finalized and sent.
D. Record each review with reviewer identity and timestamp so the organization can evidence that a human reviewed every denial.

*Keys: A and B.* Review is a control only when the reviewer can see the inputs, can disagree, and has the time to do so — and a near-zero override rate is the signal that none of that is true. **C** adds a second click to a decision the reviewer still cannot evaluate. **D** produces evidence that review occurred, which is exactly what a rubber stamp also produces.

---

## 9. Objective-coverage table

Honest assessment. "Thin" means a candidate should seek additional practice beyond this chapter.

| Objective | Depth | Covered in |
|---|---|---|
| 1. Implement guardrails and safety controls | Strong | §2.1 (two axes, operative rule), §2.3 (narrowed authority, runtime identity), §2.7 (placement, fail-open/closed, streaming, graduated response, threshold), T1, T3, Scenarios 4 and 6, §5, §6, Items 1, 2, 6, 7, 8 |
| 2. Identify risks, limitations, and failure modes | Strong | §2.5 (data/action/drift planes, "assume injection succeeds"), §5 diagnostics table, §6, Items 7, 8, and the diagnostic reasoning in Items 1 and 5 |
| 3. Apply human-in-the-loop validation strategies | Strong | §2.4 (reversibility as a design choice), §2.6 (tier, trigger, meaningfulness), T4, Scenarios 1, 2, 5, Items 5, 12 |
| 4. Ensure compliance with regulations | Strong on procedure, deliberately thin on specifics | §2.8 (role chain, retention, GDPR, HIPAA, four-step public-sector procedure, frameworks), T5, T6, T7, Scenarios 1, 2, 3, Items 3, 4, 11. Specific authorizations are dated and demoted to one snapshot box by design — the exam tests the procedure, and the specifics move inside a 12-month credential window |
| 5. Address ethical AI considerations | Adequate — improved but still the lightest objective | §2.9 (proxies, system-vs-model measurement, incompatible metrics, contestability, disclosure, citations vs. explainability, "don't use the model for the decision"), T8, Scenario 5, §6 (fairness-washing), §5 (segment-divergence row), Items 9, 10. Gap: no worked treatment of multi-turn or memory-mediated fairness effects, and the metric-incompatibility claim carries an `[UNVERIFIED]` flag |

Deliberately *not* claimed: Scenario 2 and Item 11 touch transparency but are decided on legal-effect and retention grounds, not on a fairness axis; Item 10 sits under Objective 5 for the explainability strand, not the bias strand.

---

## 10. Sources

| ID | Title | URL | Accessed | Trust |
|---|---|---|---|---|
| VF | `VERIFIED-FACTS.md` — orchestrator adjudication (Covered Models and ZDR; Mythos restricted access; public-sector/FedRAMP posture; citations wording; deployment surfaces) | local project file | 2026-09-24 | primary |
| D05-S02 | What Certifications has Anthropic obtained? | https://privacy.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained | 2026-09-24 | primary |
| D05-S04 | API and data retention (retention defaults, Covered Models, ZDR scope, flagged-content retention, HIPAA readiness scope and enforcement, processor split) | https://platform.claude.com/docs/en/manage-claude/api-and-data-retention | 2026-09-24 | primary |
| D05-S05 | Business Associate Agreements (BAA) for Commercial Customers | https://privacy.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers | 2026-09-24 | primary |
| D05-S12 | GDPR Article 5 — principles (purpose limitation, minimization, storage limitation) | https://gdpr-info.eu/art-5-gdpr/ | 2026-09-24 | secondary (regulation text mirror) |
| D05-S13 | GDPR Article 22 — automated individual decision-making; 22(3) safeguards | https://gdpr-info.eu/art-22-gdpr/ | 2026-09-24 | secondary (regulation text mirror) |
| D05-S14 | HIPAA minimum-necessary requirement (45 CFR 164.502(b), 164.514(d)) | https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html | 2026-09-24 | primary |
| D05-S15 | Guidance on methods for de-identification of PHI (Safe Harbor; Expert Determination) | https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html | 2026-09-24 | primary |
| D05-S16 | EU AI Act — regulatory framework, risk tiers, application dates | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | 2026-09-24 | primary |
| D05-S17 | NIST AI Risk Management Framework (Govern, Map, Measure, Manage; voluntary) | https://www.nist.gov/itl/ai-risk-management-framework | 2026-09-24 | primary |
| D05-S18 | Understanding ISO 42001 (AI management system, PDCA) | https://www.a-lign.com/articles/understanding-iso-42001 | 2026-09-24 | secondary (standard text paywalled) |
| D05-S19 | Mitigate jailbreaks and prompt injections (direct vs. indirect threat models; tool-result isolation; provenance labeling; JSON encoding; screening model; least privilege as blast-radius reduction) | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | 2026-09-24 | primary |
| D05-S20 | Reduce hallucinations (abstention, quote extraction, citation-then-verify; "significantly reduce… don't eliminate") | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | 2026-09-24 | primary |
| D05-S21 | Usage Policy — high-risk use-case requirements (qualified professional review; AI disclosure) | https://www.anthropic.com/legal/aup | 2026-09-24 | primary |
| D05-S23 | MCP/tool supply-chain vulnerability research | https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/ | 2026-09-24 | secondary |
| D05-S25 | Human-in-the-loop governance for AI agents (tier ladder and escalation triggers — practitioner synthesis) | https://www.arthur.ai/column/human-in-the-loop-governance-for-ai-agents | 2026-09-24 | secondary |
| D05-S27 | Data residency (`inference_geo` values; no EU pin; 1.1x pricing for `"us"`; platform applicability) | https://platform.claude.com/docs/en/manage-claude/data-residency | 2026-09-24 | primary |
| D05-S30 | Claude Certified Architect – Professional Exam Guide v1.0 (blueprint, Domain 5 objectives, Samples 1 and 3) | local project file | 2026-09-24 | primary |
| D05-V05 | Claude in Amazon Bedrock: approved for FedRAMP High and DoD IL4/5 workloads (pub. 2025-06-11) | https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high | 2026-09-24 | primary |
| D05-V06 | Claude on Google Cloud Vertex AI: FedRAMP High and IL2 authorized (pub. 2025-04-02) | https://claude.com/blog/claude-on-google-cloud-fedramp-high | 2026-09-24 | primary |
| D05-V08 | Public Sector FAQs (Claude for Government as Anthropic's FedRAMP High product; CUI authorized in a FedRAMP High environment) | https://support.claude.com/en/articles/13756069-public-sector-faqs | 2026-09-24 | primary |
| D05-V09 | Model availability in Claude for Government ("no separate FedRAMP audit per model"; authorization is infrastructure-level) | https://support.claude.com/en/articles/14503794-model-availability-in-claude-for-government | 2026-09-24 | primary |
| D05-V10 | FedRAMP Marketplace listing, CSP Anthropic, product "Claude" (status: not yet certified) | https://www.fedramp.gov/marketplace/products/FR2633053633/ | 2026-09-24 | primary |
| D05-V13 | EU AI Act tier names and application dates; AI Omnibus timeline | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | 2026-09-24 | primary |
| D05-V15 | AI Omnibus enters into force (27 July 2026) | https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force | 2026-09-24 | primary |
| D05-V17 | OWASP Top 10 for LLM Applications 2025 — verbatim LLM01–LLM10 names | https://genai.owasp.org/llm-top-10/ | 2026-09-24 | primary |
| D05-V21 | Citations ("citations are guaranteed to contain valid pointers to the provided documents") | https://platform.claude.com/docs/en/build-with-claude/citations | 2026-09-24 | primary |
| D05-V23 | Measuring political even-handedness (paired-prompt, model-as-judge methodology) | https://www.anthropic.com/news/political-even-handedness | 2026-09-24 | primary |
| D05-V26 | AWS HIPAA-eligible services reference (Amazon Bedrock; AWS BAA required) | https://aws.amazon.com/compliance/hipaa-eligible-services-reference/ | 2026-09-24 | primary |
| D05-V27 | HIPAA compliance on Google Cloud (covered-products list; "Vertex AI" not named) | https://cloud.google.com/security/compliance/hipaa | 2026-09-24 | primary |
| D05-V28 | Regulation (EU) 2024/1689 consolidated text (Art. 14 human oversight) | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 2026-09-24 | primary |
| D05-V29 | AI Act Article 12 — record-keeping (distinct from Art. 14 human oversight) | https://artificialintelligenceact.eu/article/12/ | 2026-09-24 | secondary (regulation mirror) |
| D05-V32 | FedRAMP baselines and DoD Cloud Computing SRG Impact Levels (separate constructs) | https://www.fedramp.gov/rev5/baselines/ · https://dodcio.defense.gov/library/ | 2026-09-24 | primary |

`D05-Sxx` IDs resolve in `research/05-governance-safety-risk-sources.md`; `D05-Vxx` IDs resolve in `review/05-governance-safety-risk-validation.md`, which records the verification verdict for each.

### Remaining `[UNVERIFIED]` claims

1. **Fairness-metric incompatibility** (§2.9, T8). The impossibility of simultaneously satisfying equal error rates, equal outcome rates, and within-group calibration when base rates differ is standard in the fairness literature, but no primary citation was verified in this session. The chapter teaches the architectural consequence (choose, document, and own the metric) and attributes no specific result.
2. **Bedrock's Impact Level ceiling above IL4/5**, including availability in a Secret region at IL6, and the claim that ITAR-regulated data can only be processed via Bedrock. Both were reported by the validator from Anthropic's Public Sector FAQ but were **not** confirmed in the orchestrator's own verification of that page. No teaching point or practice item in this chapter depends on either.
3. **Sub-processor change-notice period** (reported externally as 15 days). Not verified against Anthropic's primary DPA text; excluded from the chapter.
4. **ISO/IEC 42001 clause-level detail.** The standard text is paywalled; only a certification body's summary was available, so the chapter claims only the standard's existence, scope, and Anthropic's certification [D05-S02, D05-S18].
5. **The five-tier human-review ladder** (§2.6, T4) is a practitioner synthesis [D05-S25], not published Anthropic or standards-body doctrine. The reversibility × impact reasoning is what transfers; the tier names are not authoritative vocabulary.
6. **Product naming drift.** Anthropic's retention documentation refers to "Google Cloud's Agent Platform" while its public-sector material still says "Vertex AI with Assured Workloads." The chapter uses the public-sector naming for public-sector claims; expect both names in the field.
