# Domain 5: Governance, Safety & Risk Management

**Weight:** 14% of the exam (~9 of 63 scored items)

**Objectives covered:**
1. Implement guardrails and safety controls
2. Identify risks, limitations, and failure modes of LLM systems
3. Apply human-in-the-loop validation strategies
4. Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP)
5. Address ethical AI considerations (bias, fairness, transparency)

---

## 1. Exam-relevance framing

This domain does not test recall of GDPR articles or HIPAA rule numbers. It tests whether, given a system under a named constraint, you pick the response that actually satisfies the constraint — not the one that merely *looks* responsible. Items are scenario stems where several options are defensible-sounding and only one survives scrutiny of what the control actually does.

Recurring distractor archetypes:

1. **Detective dressed as preventive.** "Add logging/monitoring/flag for review" offered as the fix for a risk requiring the action never happen without approval. Logging tells you a bad thing occurred; it doesn't stop it.
2. **Prompt-only fix for a material risk.** A system-prompt instruction offered as the complete mitigation for a financial, safety-critical, or irreversible risk. Prompt instructions are real but weak; the correct answer adds a programmatic, classifier, or architectural layer, or removes the capability.
3. **Compliance-by-vendor-claim.** "We use Claude, so we're HIPAA/FedRAMP compliant." Compliance is a property of the deployment configuration — BAA, feature eligibility, retention arrangement, authorized boundary — never of the model alone.
4. **Confusing model behavior with retrieval behavior.** A hallucination or drift symptom attributed to "the model got worse" when the retrieval index or tool output is the actual failure point.
5. **Uniform HITL regardless of reversibility.** "Review everything" or "review nothing" offered when the right answer scales review depth to reversibility and impact.
6. **Ethics as a one-time check.** Bias/fairness testing framed as a pre-launch checkbox instead of a recurring eval re-run on every model or prompt change.

---

## 2. Core concepts

### 2.1 The control-strength hierarchy

Five places a control can live, strongest to weakest containment:

1. **Architectural removal** — the capability doesn't exist. Nothing to circumvent.
2. **Human approval gate** — a person must act before an irreversible/high-impact effect fires.
3. **Classifier/filter** — a separate, narrow model or rule set screens input/output before it reaches the primary model or the outside world.
4. **Programmatic validation** — deterministic code: schema checks, allow-lists, range/type checks.
5. **Prompt-level instruction** — system-prompt wording asking the model to behave a certain way.

*Why it matters:* effort spent hardening layer 5 while layer 1 is available is misallocated — the exam guide's own sample item confirms this: removing unused tools beats logging, a confirmation prompt, or a "smarter model" [D05-S30, Sample 1]. *Decision it drives:* before reaching for a classifier or prompt rule, ask whether the capability can simply be removed. *Misconception:* stacking prompt instructions is "defense in depth" — depth means different *kinds* of control; a prompt rule repeated three ways is still one layer.

### 2.2 Preventive vs. detective vs. compensating controls

- **Preventive** — stops the outcome before it happens (remove a tool, reject malformed output, gate before execution).
- **Detective** — notices the outcome after the fact (logs, dashboards, audit trails).
- **Compensating** — limits *impact* without preventing or detecting directly (transaction caps, reversible-by-default design, rate limits).

*Why it matters:* "we log it" answers a forensics question, not a prevention question — a system can log a harm faithfully and still cause it. Regulators distinguish these explicitly; an EU AI Act high-risk conformity file expects logging *and* a separate human-oversight mechanism, not logging alone [D05-S16]. *Decision it drives:* for any named risk, confirm at least one preventive or compensating control exists — detective alone never suffices for an irreversible or regulated action. *Misconception:* that monitoring is a mitigation. It answers "did this happen," not "can this happen."

### 2.3 Failure-mode taxonomy for LLM systems

Each failure mode has a *specific* architectural mitigation, not a generic "test more" answer:

- **Hallucination/fabrication** → retrieval grounding, citation-then-verify, quote-extraction-first prompting, explicit permission to abstain [D05-S20].
- **Prompt injection, direct** (user is the adversary) → input screening classifier, hardened system prompt, throttling repeat offenders [D05-S19].
- **Prompt injection, indirect** (trusted user, adversarial third-party content) → isolate untrusted content to `tool_result` blocks only, label provenance, JSON-encode untrusted strings, screen tool output before the model sees it [D05-S19].
- **Excessive agency** → remove unneeded tools/scopes — architectural removal, not confirmation dialogs.
- **Insecure output handling** → treat model output as untrusted input downstream: schema validation, output encoding, parameterized queries, sandboxed execution [D05-S11].
- **Data leakage, cross-tenant** → tenant-scoped retrieval filters enforced at the data layer, not the prompt layer.
- **Data leakage, into logs** → redact/tokenize before persistence; short-TTL or zero retention where feasible [D05-S04].
- **Supply-chain/MCP-server trust** → verified/signed sources only, sandboxed execution, treat MCP config as untrusted input [D05-S23].
- **Nondeterminism/silent drift** → version-pin models and prompts as controlled artifacts, regression-test on every change; confident-but-wrong after a document refresh (model/latency unchanged) is a retrieval symptom, not a model symptom [D05-S30, Sample 3].
- **Over-reliance/automation bias** → statistical sampling audits, injected test cases in review queues, tracked override rates.

### 2.4 Human-in-the-loop tiers

Five tiers, decreasing coverage, increasing throughput: **100% review → risk-tiered review → confidence/uncertainty-triggered escalation → statistical sampling → post-hoc audit**.

*Why it matters:* the tier is chosen from **reversibility × impact**, not a generic "how important is this." An irreversible, high-impact action (wire transfer, dosing suggestion, permanent deletion) needs a synchronous gate *before* execution — post-hoc audit cannot undo it. A reversible, low-impact action (a draft awaiting a human "send") tolerates sampling or post-hoc review. *Decision it drives:* classify each *action*, not the whole system, by reversibility × impact before assigning a tier. *Misconception:* escalation should trigger only on low model confidence — confidently wrong outputs exist; irreversibility and anomaly signals must also trigger escalation [D05-S25].

### 2.5 Regulatory and framework primitives

- **GDPR** — Art. 5: purpose limitation and data minimization bound what may reach a model [D05-S12]. Art. 22: no *solely* automated decision with legal/significant effect except under law-with-safeguards, explicit consent, or contract necessity — with a retained right to human intervention and to contest [D05-S13]. Anthropic is processor on the 1P API/Claude Platform on AWS; the cloud provider is processor on Bedrock/Google Cloud [D05-S04].
- **HIPAA** — PHI only to a BAA-covered, HIPAA-readiness-enabled surface, restricted to eligible features (API returns `400` on an ineligible feature under a HIPAA-enabled org) [D05-S04, D05-S05]. Minimum necessary [D05-S14] and de-identification (Safe Harbor or Expert Determination) [D05-S15] reduce exposure before any technical safeguard is needed.
- **FedRAMP** — a property of the *deployment surface*, not the model. Bedrock in AWS GovCloud: FedRAMP High + DoD IL4/5. Vertex AI Assured Workloads: FedRAMP High + IL2 only. The 1P API is not itself a FedRAMP-authorized boundary [D05-S06, D05-S07, D05-S08].
- **EU AI Act** — four risk tiers; prohibited practices since Feb 2025; transparency (Art. 50) from Aug 2026; high-risk obligations shifted by a 2026 amendment to Dec 2027 (Annex III) / Aug 2028 (Annex I) [D05-S16].
- **NIST AI RMF** — voluntary, four functions (Govern, Map, Measure, Manage) applied iteratively [D05-S17].
- **ISO/IEC 42001** — certifiable AI management system standard (PDCA cycle); a due-diligence signal for vendors, a target for your own maturity [D05-S18].
- **OWASP Top 10 for LLM Apps** — an engineering baseline, not law: prompt injection, sensitive info disclosure, supply chain, data/model poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, unbounded consumption [D05-S10, D05-S11].

*Misconception across all of these:* that a framework is satisfied by the vendor's certifications alone. Each is satisfied by the *combination* of vendor posture (contract, BAA, authorized boundary) and your own system design (minimization, logging, oversight, retention).

### 2.6 Ethical AI, operationalized

- **Bias/fairness testing is an eval discipline** — run and re-run, segmented by the dimension of concern, on every model or prompt change, not a pre-launch checkbox. Anthropic's published methodology (a paired-viewpoint even-handedness eval, model-as-judge scored) is a worked example [D05-S22].
- **Disparate-impact review** slices outcome metrics *by segment* — an aggregate accuracy number can hide a large per-segment gap.
- **Transparency/disclosure** — tell the end user when AI produced or assisted a decision, a floor under both Anthropic's Usage Policy for high-risk domains and the EU AI Act's limited-risk tier [D05-S21, D05-S16].
- **Explainability vs. grounding** — citations show *where* a claim came from, not *why* the model chose to say it. Anthropic's own docs acknowledge occasional citation/quote mismatches [D05-S26, D05-S20].
- **Contestability** — GDPR Art. 22 implies a designed appeal path, not merely a HITL gate on the way in [D05-S13].
- **Documentation artifacts** — model/system cards, AI risk registers (a NIST RMF "Manage" output) [D05-S17], and DPIAs are the standard paper trail an architecture should produce evidence for.

### 2.7 Governance mechanics

Prompts and model versions are **controlled artifacts**: change management like code — versioned, reviewed, regression-tested against a fixed eval set, with a rollback path. An AI review board typically owns approval of new high-risk use cases, exceptions touching Article-22-like automated decisions, and incident response for AI-specific failures. AI incident response differs from classical IR in one respect: the "bug" may be a prompt or a retrieval index rather than code, so the fix path must include prompt/index rollback, not only a code deploy.

---

## 3. Trade-off analyses

### T1 — Control placement: prompt vs. programmatic vs. classifier vs. architectural vs. human gate

| Axis | Prompt instruction | Programmatic validation | Classifier/filter | Architectural removal | Human approval gate |
|---|---|---|---|---|---|
| Bypass resistance | Low | High for what it checks | Medium — a second model can also be fooled | Highest | High if the gate is on the action itself |
| Cost to add | Near zero | Low-medium | Medium (a model call, latency) | Free to costly | Latency + staffing |
| Best for | Low-stakes tone/format | Deterministic, checkable constraints | Fuzzy judgment not needing a human | Any capability the role never needs | Irreversible/high-impact actions |

**Choose prompt-level** for stylistic, low-stakes shaping. **Programmatic validation** for deterministic constraints. **A classifier** for fuzzy judgment that doesn't need a human. **Architectural removal** whenever the role genuinely never needs the capability — dominates when available. **A human gate** whenever the action is irreversible or high-impact, regardless of the other layers; they reduce how often the gate fires, not whether it's needed.

### T2 — Preventive vs. detective vs. compensating controls

| Axis | Preventive | Detective | Compensating |
|---|---|---|---|
| When it acts | Before the harm | After the harm | Alongside/after, limits impact |
| Answers | Can this happen? | Did this happen? | How bad was it? |
| Regulatory sufficiency alone | Often sufficient if well-designed | Never sufficient alone for irreversible/regulated actions | Only when paired with accepted residual risk |
| Example | Remove the delete-account tool | Audit log of tool calls | Transaction cap per action |

**Preventive** is the default target for anything material. **Detective** is always added for forensics and drift detection — never presented as the fix. **Compensating** bounds damage when full prevention isn't feasible.

### T3 — Guardrail strictness vs. utility

| Axis | Strict (favor blocking) | Loose (favor completion) |
|---|---|---|
| False positives (over-refusal) | High | Low |
| False negatives (harm passes through) | Low | High |
| Right domain | Irreversible/regulated actions, PHI/financial handling | Low-stakes drafting, human-reviewed internal tools |

*Discriminator:* the operating point is set by the **cost of a false negative** relative to the **cost of a false positive** in that domain — not a universal constant. A medical-dosing assistant should over-refuse; a marketing-copy tool should rarely refuse, because a human reviews before publication. An item testing this describes downstream reversibility/impact and expects the operating point to shift accordingly.

### T4 — Human-in-the-loop tiers

| Tier | Coverage | Cost/latency | Fatigue risk | Best for |
|---|---|---|---|---|
| 100% review | Complete | Highest | Highest | Low-volume, very-high-impact, irreversible actions |
| Risk-tiered review | Matches risk class | Medium | Medium | Mixed-risk action sets (most agents) |
| Confidence-triggered | Flagged low-confidence only | Low | Low | High-volume, well-calibrated confidence |
| Statistical sampling | Partial, representative | Low | Low | Quality monitoring at scale |
| Post-hoc audit | After the fact only | Lowest | Lowest | Reversible, low-impact actions |

*Discriminator:* pick the tier from reversibility × impact of the specific *action class*, not the system as a whole — one agent commonly needs different tiers per tool ("draft reply" = post-hoc audit; "refund over $1,000" = 100% review).

### T5 — Compliance-driven deployment surface: 1P API vs. Amazon Bedrock vs. Google Vertex AI

| Axis | Anthropic 1P API | Amazon Bedrock (GovCloud) | Google Vertex AI (Assured Workloads) |
|---|---|---|---|
| Data residency | `inference_geo`: `"us"` or `"global"` only — no EU-specific pin [D05-S27] | Region set by endpoint | Region set by endpoint |
| FedRAMP/DoD | Not itself an authorized boundary | FedRAMP High + IL4/5 [D05-S06, D05-S07] | FedRAMP High + IL2 only [D05-S08] |
| HIPAA path | Direct BAA with Anthropic [D05-S05] | BAA through AWS (AWS is processor) | BAA through Google (Google is processor) |
| ZDR | Yes, by approval [D05-S04] | Platform-specific — verify per engagement | Platform-specific — verify per engagement |

*Discriminator:* choose **1P API** for fastest access to newest features when a direct BAA/DPA with Anthropic satisfies the need. Choose **Bedrock GovCloud** for FedRAMP High/IL4-5 (CUI-level) workloads or when AWS must be sole processor. Choose **Vertex Assured Workloads** when IL2 suffices and the org is GCP-native — never for IL4/5-level workloads; it cannot meet that bar today.

### T6 — Data minimization vs. retrieval richness

| Axis | Minimal retrieval | Rich retrieval |
|---|---|---|
| Answer completeness | Lower risk of missing context | Higher grounding |
| PII/PHI exposure surface | Smaller | Larger |
| Minimization/minimum-necessary alignment | Strong | Weak unless de-identified first |

*Discriminator:* set retrieval breadth by task need, trim to the minimum that satisfies it, then re-check against minimization obligations — never maximize "for better answers" by default. Where richness and minimization conflict, filter or de-identify *before* retrieval so sensitive fields never enter the prompt.

### T7 — Full observability logging vs. privacy obligations

| Axis | Full raw-content logging | Redacted/tokenized logging |
|---|---|---|
| Debuggability | Highest | Reduced |
| GDPR/HIPAA exposure | High — logs become another regulated store | Low |
| Retention conflict | May conflict with ZDR/erasure commitments | Resolved — safe to retain longer |

*Discriminator:* redact or tokenize PII/PHI *before* it's written to logs, keeping structural metadata (latency, tool name, token counts) fully observable while the sensitive payload is masked or replaced with a reversible token under separate access control [D05-S04]. This gives debuggability without turning observability into an uncontrolled second copy of regulated data.

---

## 4. Worked scenarios

**1 — Healthcare: clinical documentation assistant.** *Situation:* a hospital wants Claude to draft visit summaries from clinician dictation referencing patient history — PHI throughout. *Approaches:* (a) use the 1P API with no special configuration; (b) execute a BAA, enable org-level HIPAA readiness, restrict to eligible features; (c) de-identify everything first, forgo the BAA. *Recommended:* (b) — and pick a non-"Covered Model" if ZDR is also required, or accept 30-day retention if the Covered Model's capability is worth that trade. *Why the others lose:* (a) sends PHI to a non-BAA org — the violation itself; (c) discards clinical detail and doesn't scale to free-text dictation, where reliable de-identification pre-model is itself unsolved. *Changes the answer:* aggregate, already-de-identified analytics (not per-patient documentation) make (c) viable and cheaper.

**2 — Financial services: loan-underwriting assistant.** *Situation:* a lender wants Claude to recommend approve/deny, EU applicants in scope — a denial is legally significant. *Approaches:* (a) fully automate; (b) require a loan officer to finalize every recommendation, with disclosure; (c) automate, log for later audit. *Recommended:* (b). *Why the others lose:* (a) violates GDPR Art. 22 absent a narrow exception ordinary underwriting doesn't meet; (c) is detective — the wrongful denial already occurred. *Changes the answer:* genuine explicit consent or contract-necessity permits limited automation, but human-intervention/contestability paths remain required.

**3 — Public sector: citizen-services chatbot.** *Situation:* a federal agency wants a chatbot answering benefits questions from CUI-level internal policy documents. *Approaches:* (a) call the 1P API directly; (b) deploy via Bedrock in AWS GovCloud; (c) deploy via Vertex AI Assured Workloads. *Recommended:* (b) — CUI requires the FedRAMP High + IL4/5 boundary Bedrock GovCloud provides. *Why the others lose:* (a) has no FedRAMP-authorized boundary; (c) tops out at IL2, insufficient for CUI. *Changes the answer:* if the documents are genuinely public (no CUI), IL2 or even (a) with appropriate contracts becomes reconsiderable — but reclassification belongs to the agency's data-classification authority, not the architect.

**4 — Retail: customer-support agent with account tools.** *Situation:* an agent can read tickets, draft replies, issue refunds, and delete accounts; staff only need the first two. *Approaches:* (a) keep all four tools, add audit logging on refunds/deletes; (b) keep all four, add a confirmation prompt; (c) remove the refund and delete tools entirely. *Recommended:* (c). *Why the others lose:* (a) is detective; (b) is a weaker gate a crafted injection or rushed human can still push through, and the capability remains an attack surface. *Changes the answer:* a genuinely different privileged role needing refund/delete should get its own tightly scoped agent, not shared access "just in case." (Mirrors the exam guide's own Domain 3 sample [D05-S30, Sample 1].)

**5 — Insurance: claims-triage with automated decisioning.** *Situation:* an insurer wants to auto-approve low-dollar claims and route the rest; some claimants are EU residents; false denials harm real people. *Approaches:* (a) auto-approve and auto-deny under a threshold; (b) auto-approve under a threshold, but route every denial to a human with disclosure; (c) route everything to a human. *Recommended:* (b), tiering by the reversibility of a *denial* specifically — an erroneous approval is a reversible cost (claw-back); an erroneous denial is a harder-to-reverse harm. *Why the others lose:* (a) risks unreviewed adverse decisions for EU claimants; (c) discards throughput on the larger, lower-risk approval side. *Changes the answer:* a mandate for 100% sign-off on all decisions forces (c).

**6 — Legal: contract-review assistant.** *Situation:* a firm wants Claude to flag risky clauses in vendor contracts; hallucinated interpretations create malpractice exposure; associates, not clients, are the intended reviewers. *Approaches:* (a) let output reach clients directly; (b) require quoted source text for each flag, plus associate sign-off before anything reaches a client; (c) rely on a system prompt about accuracy. *Recommended:* (b) — quote-grounding reduces (not eliminates) hallucination, and sign-off is the human gate for a high-liability output. *Why the others lose:* (a) removes the human gate entirely; (c) is a prompt-only fix for a material risk. *Changes the answer:* if used purely for an associate's own triage, with full independent review always following regardless, grounding strictness can relax slightly since human review already dominates.

**7 — Engineering: agentic system using third-party MCP servers.** *Situation:* a team wants an agent using community MCP servers to query internal systems and file tickets; servers run with the agent's privileges. *Approaches:* (a) install anything useful, trusting the model to behave; (b) install only verified/signed servers, sandbox execution, monitor invocations; (c) disable MCP, hand-write every tool. *Recommended:* (b). *Why the others lose:* (a) ignores documented supply-chain risk — a compromised server can exfiltrate data or achieve RCE regardless of model alignment [D05-S23]; (c) discards ecosystem benefit disproportionately to a manageable risk. *Changes the answer:* for a data path touching PHI/PCI, the verification bar should rise further, potentially justifying (c) for that path specifically.

---

## 5. Failure modes & diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| Confident-but-wrong after a document refresh; model/latency unchanged | Retrieval/indexing returning stale or irrelevant chunks | Re-index freshness, embedding mismatch, chunk relevance | Rebuild/validate the index, add a retrieval-quality eval — not a model swap [D05-S30, Sample 3] |
| Agent takes an unexpected destructive action | Excessive agency, or a successful injection | Tool manifest for that role; recent tool-call logs | Remove the unneeded tool; add tool-result isolation for untrusted content |
| PII/PHI appears in logs or traces | No redaction before persistence | Logging pipeline configuration | Redact/tokenize before write; separate access-controlled store for raw payloads |
| Spike in over-refusal complaints | Guardrail strictness miscalibrated for the domain | Recent system-prompt/classifier/threshold changes | Re-tune the operating point against domain-specific false-positive/negative cost |
| One tenant's data appears in another's output | Retrieval filter not enforced at the data layer | Whether tenant ID is enforced in the retrieval call itself | Enforce tenant scoping at the data/index layer, never the prompt |
| Behavior silently changes after a routine deploy | Model/prompt version changed without regression testing | Diff against the last known-good eval run | Treat prompts/model versions as controlled artifacts; require an eval gate before promotion |
| Reviewers approve nearly everything flagged | Automation bias / reviewer fatigue from volume | Reviewer throughput and override rate over time | Reduce volume via better tiering; inject known-bad test cases |
| Cited sources don't support the claim | Citation/grounding mismatch | Spot-check citation-to-source alignment | Add a citation-verification step before rendering [D05-S20] |

---

## 6. Anti-patterns

- **Guardrail as suggestion.** Treating a prompt instruction as sufficient for a financial, safety-critical, or irreversible risk — fast to ship, works until an adversarial input finds the gap.
- **Logging as prevention.** An audit trail presented as the fix for a risk needing a preventive/compensating control — necessary, never sufficient alone.
- **One-size-fits-all human review.** Reviewing everything (fatigue, automation bias) or nothing (unsafe for the irreversible subset) — simpler to state than a tiered policy, wrong either way.
- **BAA-washing.** Assuming a signed BAA alone makes any product use HIPAA-safe, without checking feature eligibility or org-level enablement.
- **Compliance theater via documentation only.** A model card or risk register produced once at launch, then treated as governance-complete — bias and drift are ongoing properties.
- **Kitchen-sink tool agent.** Giving one agent every tool "in case," maximizing blast radius for every future injection or misconfiguration.
- **Regex redaction as a complete PII solution.** Pattern-matching catches obvious cases (SSNs, emails); free-text PHI/PII rarely matches cleanly, creating false confidence.

---

## 7. Exam-day heuristics

- **"Remove the capability" beats "log/confirm/monitor it"** whenever removal is possible — the least-privilege tiebreaker.
- **Detective controls never answer "how do we prevent."** If the stem asks for prevention and an option only detects, it's a distractor.
- **A prompt instruction is never the complete answer for a material risk** — find the option adding a programmatic, classifier, architectural, or human layer.
- **Irreversible + high-impact → synchronous human gate before execution**, not post-hoc audit or sampling.
- **Confident-but-wrong + document refresh + model/latency unchanged → retrieval/indexing, not the model.**
- **"Compliant because we use Claude" is always wrong** — compliance is a property of the deployment configuration, never the vendor alone.
- **FedRAMP High + IL4/5 → Bedrock GovCloud; FedRAMP High + IL2 only → Vertex Assured Workloads** — know the ceiling difference.
- **Citations ground a claim; they don't explain the model's reasoning.**
- **Bias/fairness testing is recurring, not a one-time gate.**

---

## 8. Practice items

**Item 1 (select 1).** A team's agent can read customer records, draft emails, and issue account credits up to $10,000. Only the first two are needed for the current use case. Applying least privilege, what is the best change?
A. Add a confirmation step before any credit is issued.
B. Remove the credit-issuing tool from this agent's configuration.
C. Lower the credit limit to $1,000.
D. Log every credit issuance for later review.

*Correct: B.* Removing the unused capability eliminates the attack surface. A is a weaker gate, still exploitable; C reduces impact but keeps an unneeded capability; D is detective, not preventive.

**Item 2 (select 1).** A healthcare organization wants Claude to summarize doctor's notes containing PHI. Which combination is required first?
A. Enterprise-tier subscription and a strong confidentiality system prompt.
B. A signed BAA, org-level HIPAA readiness enabled, and use restricted to eligible features.
C. Zero data retention (ZDR) enabled for the organization.
D. Running only during business hours with encrypted transport.

*Correct: B.* Matches Anthropic's documented HIPAA-readiness requirements [D05-S04, D05-S05]. A confuses subscription tier with compliance. C is a separate, partly-incompatible arrangement for certain models — not a substitute. D is generic hygiene, not HIPAA-specific.

**Item 3 (select 1).** An EU lender wants to fully automate loan denials with no human involvement. What is the most likely compliance issue?
A. GDPR Article 5 data-minimization violation.
B. GDPR Article 22 restriction on solely automated decisions with legal/significant effect.
C. HIPAA minimum-necessary violation.
D. FedRAMP authorization boundary violation.

*Correct: B.* A denial is a legally significant effect from solely automated processing, restricted absent a qualifying basis and a human-intervention path [D05-S13]. A concerns collection scope, not decision automation. C is healthcare-specific, irrelevant here. D concerns federal cloud boundaries, unrelated to a commercial lender.

**Item 4 (select 2).** A federal agency must process Controlled Unclassified Information (CUI) requiring DoD Impact Level 4/5 authorization. Which two statements are accurate?
A. The first-party Anthropic API alone satisfies this requirement.
B. Amazon Bedrock in AWS GovCloud can satisfy FedRAMP High + IL4/5.
C. Google Vertex AI Assured Workloads currently tops out at IL2, insufficient for this workload.
D. Any cloud deployment of Claude automatically inherits DoD IL4/5 authorization.

*Correct: B and C.* Reflect the documented ceiling difference between the two hyperscaler paths [D05-S06, D05-S07, D05-S08]. A is wrong — the 1P API is not itself a FedRAMP-authorized boundary. D is wrong — authorization is boundary-specific and doesn't transfer automatically.

**Item 5 (select 1).** After a routine model version upgrade, an agent's tone and refusal behavior shifted overnight with no code or prompt changes. What most defensibly prevents this surprise?
A. Nothing — model behavior is inherently unpredictable.
B. Version-pin the model and run a regression eval suite before promoting any change.
C. Add more few-shot examples to the prompt after the fact.
D. Switch to a smaller model to reduce variability.

*Correct: B.* Pinning the version with a pre-promotion eval gate catches shifts before production. A is defeatist and wrong — this is exactly what governance catches. C is reactive. D doesn't address unmanaged version promotion and trades capability for an unrelated reason.

**Item 6 (select 1).** A pipeline retrieves an inbound customer email body and passes it to Claude to draft a reply. Which design best defends against indirect prompt injection from the email?
A. Place the email body directly in the system prompt for visibility.
B. Deliver it only inside a `tool_result` block, explicitly labeled as untrusted third-party content.
C. Ask the model in plain English not to follow instructions found in emails.
D. Increase the output token limit so the model has room to flag suspicious content.

*Correct: B.* Matches Anthropic's documented indirect-injection defense: isolate untrusted content with explicit provenance labeling [D05-S19]. A elevates untrusted content's trust level, which is dangerous. C is a prompt-only instruction, the weakest layer. D is unrelated to the risk.

**Item 7 (select 1).** Which pairing correctly matches a human-in-the-loop tier to the action it suits?
A. Post-hoc audit — for an irreversible fund transfer over $50,000.
B. 100% synchronous review — for every low-value draft-reply suggestion in a high-volume chat system.
C. Synchronous human approval before execution — for an irreversible fund transfer over $50,000.
D. Statistical sampling — for an irreversible fund transfer over $50,000.

*Correct: C.* Irreversible, high-impact actions need a gate before execution. A and D let the harm occur before review, which cannot undo a transfer. B misapplies the costliest tier to a low-impact, reversible action, guaranteeing fatigue without benefit.

**Item 8 (select 2).** Which two are OWASP Top 10 for LLM Applications (2025) categories?
A. Prompt Injection
B. Excessive Agency
C. Insufficient Context Window
D. Slow Inference Latency

*Correct: A and B.* Both are named 2025 categories [D05-S10, D05-S11]. C and D are engineering/performance concerns, not named security-risk categories in this framework.

**Item 9 (select 1).** A team wants rich observability (full prompt/response logging) for debugging, but processes EU personal data under GDPR. What best resolves the tension?
A. Disable all logging to avoid any exposure.
B. Log full raw content indefinitely, since logs are needed for debugging.
C. Redact or tokenize sensitive fields before persisting logs, keeping structural metadata fully observable.
D. Move logs outside the EU to avoid GDPR applicability.

*Correct: C.* Resolves the debuggability-vs-privacy tension directly per documented practice: mask the payload, keep the rest observable [D05-S04]. A sacrifices debuggability unnecessarily. B ignores minimization/storage-limitation obligations. D misreads GDPR's extraterritorial scope.

**Item 10 (select 1).** A team claims its system is fair because it passed a bias evaluation before launch six months ago with no complaints since. What is the strongest critique?
A. Bias evaluations are inherently unreliable and shouldn't be used.
B. Fairness must be re-evaluated on an ongoing basis, especially after model or prompt changes, since a one-time check misses later drift.
C. Absence of complaints proves fairness conclusively.
D. Bias testing is only relevant for consumer-facing products.

*Correct: B.* Fairness testing is a recurring eval discipline; a post-launch model/prompt change is exactly when re-running it matters [D05-S22]. A overstates the critique. C mistakes absent complaints for absent disparate impact. D is false — internal tools affecting people carry the same stakes.

**Item 11 (select 1).** A contract-review assistant hallucinated a clause interpretation that reached a client without review. Which change most directly addresses the root cause?
A. Add a disclaimer that the tool may be wrong.
B. Require quoted source text for each flagged clause, plus an associate's sign-off before anything reaches a client.
C. Increase the context window so the model sees the whole contract at once.
D. Switch to a higher-effort reasoning setting for all requests.

*Correct: B.* Combines grounding with a human approval gate before release — addressing the missing control that let an unreviewed output reach a client [D05-S20]. A is disclosure, not mitigation. C and D may modestly help quality but don't address the missing human gate.

**Item 12 (select 1).** Which statement most accurately describes what Claude's citation feature provides?
A. It exposes the model's full internal chain of reasoning.
B. It grounds a claim in a specific source passage, improving auditability, but doesn't explain why the model chose to make the claim.
C. It guarantees zero hallucination in any cited response.
D. It is equivalent to a formal explainability method required under the EU AI Act for all high-risk systems.

*Correct: B.* Matches the documented scope and limits of citations [D05-S26, D05-S20]. A overstates what citations do. C is contradicted by Anthropic's own acknowledgment of occasional mismatches. D conflates a product feature with a specific regulatory requirement.

---

## 9. Objective-coverage table

| Objective | Covered in |
|---|---|
| Implement guardrails and safety controls | §2.1, §2.2, §2.3, §3 (T1–T3), §4 (Scenarios 4, 6, 7), §5, §6, §8 (Items 1, 6, 9) |
| Identify risks, limitations, and failure modes of LLM systems | §2.3, §4 (Scenarios 4, 6, 7), §5, §6, §8 (Items 1, 5, 6, 11, 12) |
| Apply human-in-the-loop validation strategies | §2.4, §3 (T4), §4 (Scenarios 2, 5, 6), §6, §8 (Items 3, 7, 11) |
| Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP) | §2.5, §3 (T5–T7), §4 (Scenarios 1, 2, 3), §6, §8 (Items 2, 3, 4, 9) |
| Address ethical AI considerations (bias, fairness, transparency) | §2.6, §4 (Scenarios 2, 5), §6, §8 (Items 10, 12) |

---

## 10. Sources

Inline citations resolve against `research/05-governance-safety-risk-sources.md` (IDs `D05-S01`…`D05-S30`). Key sources used in this chapter:

- [D05-S02] What Certifications has Anthropic obtained? — Anthropic Privacy Center, accessed 2026-09-24.
- [D05-S04] API and data retention — Anthropic, accessed 2026-09-24.
- [D05-S05] Business Associate Agreements (BAA) for Commercial Customers — Anthropic Privacy Center, accessed 2026-09-24.
- [D05-S06], [D05-S07] Claude/FedRAMP High/DoD IL4-5 on Amazon Bedrock GovCloud — Anthropic and AWS, accessed 2026-09-24.
- [D05-S08] Claude on Google Cloud's Vertex AI: FedRAMP High and IL2 Authorized — Anthropic, accessed 2026-09-24.
- [D05-S09] Anthropic's Responsible Scaling Policy — Anthropic, accessed 2026-09-24.
- [D05-S10], [D05-S11] OWASP Top 10 for LLM Applications 2025 — OWASP GenAI Security Project / Aembit summary, accessed 2026-09-24.
- [D05-S12], [D05-S13] GDPR Articles 5 and 22 — GDPR-Text.com, accessed 2026-09-24.
- [D05-S14], [D05-S15] HIPAA minimum necessary and de-identification guidance — HHS OCR, accessed 2026-09-24.
- [D05-S16] EU AI Act regulatory framework — European Commission, accessed 2026-09-24.
- [D05-S17] AI RMF Core — NIST, accessed 2026-09-24.
- [D05-S18] Understanding ISO 42001 — A-LIGN, accessed 2026-09-24.
- [D05-S19] Mitigate jailbreaks and prompt injections — Anthropic, accessed 2026-09-24.
- [D05-S20] Reduce hallucinations — Anthropic, accessed 2026-09-24.
- [D05-S21] Usage Policy — Anthropic, accessed 2026-09-24.
- [D05-S22] Anthropic's Transparency Hub — Anthropic, accessed 2026-09-24.
- [D05-S23] MCP supply-chain vulnerability research — OX Security, accessed 2026-09-24.
- [D05-S25] Human-in-the-Loop Governance for AI Agents — Arthur AI, accessed 2026-09-24.
- [D05-S26] Introducing Citations on the Anthropic API — Anthropic, accessed 2026-09-24.
- [D05-S27] Data residency — Anthropic, accessed 2026-09-24.
- [D05-S30] Claude Certified Architect – Professional Exam Guide v1.0 — Anthropic, accessed 2026-09-24.

**Remaining [UNVERIFIED] items:** the exact sub-processor change-notice period (D05-S24, secondary only); the precise passage date of the 2026 EU AI Act "Digital Omnibus" amendment (resulting deadlines are corroborated; the amendment's own date is not); whether the current Claude 5-family lineup is FedRAMP-authorized on Bedrock GovCloud today specifically (only Opus 4.8, May 2026, is confirmed); ISO/IEC 42001 clause-level detail (secondary certification-body summaries only, not the paywalled standard).
