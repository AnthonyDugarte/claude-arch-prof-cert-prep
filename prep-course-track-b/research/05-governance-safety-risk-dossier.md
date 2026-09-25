# Domain 5 — Governance, Safety & Risk Management — Research Dossier

Domain weight 14% (~9 of 63 items). Source IDs `D05-S01`…`D05-S30` resolve in
`research/05-governance-safety-risk-sources.md`. Today's date for verification purposes: 2026-09-24.

---

## 1. Objective-by-objective findings

### Objective 1 — Implement guardrails and safety controls

**Control taxonomy, strength-ordered (strongest to weakest containment):**

1. **Architectural removal of the capability** — the tool/permission/data path does not exist. Nothing to bypass. This is the exam guide's own sample-item answer for least privilege: removing the refund/delete tools, not logging or confirming them [D05-S30, Sample 1].
2. **Human approval gate** — a person must act before an irreversible or high-impact effect occurs. Strong only if the gate is on the *action*, not just visible in a log.
3. **Classifier/filter (programmatic, model-based)** — input/output screened by a separate, narrowly-scoped model or rule set before it reaches the primary model or the outside world. Anthropic's own documented pattern: use a lightweight model (e.g., Claude Haiku 4.5) as a harmlessness screen or injection screen with structured-output classification [D05-S19].
4. **Programmatic validation** — schema enforcement, allow-lists, range checks, type checks in code, independent of the model's judgment. Deterministic, testable, cheap to run per request.
5. **Prompt-level instruction** — system-prompt wording asking the model to behave a certain way. **Weakest control.** The model can be argued with, distracted, or overridden by adversarial input; it has no enforcement mechanism outside the model's own weights. Anthropic's guidance frames prompt engineering as one layer among several ("chain safeguards"), never the sole layer, for anything that matters [D05-S19].

**Exam-relevant insight:** prompt-level instructions are necessary (they shape behavior cheaply and fast) but categorically insufficient as the *only* control for a material risk (financial loss, PHI exposure, irreversible action, legal exposure). An item describing "we added a system-prompt rule against X" as the complete fix for a high-stakes failure is testing whether the candidate spots the missing programmatic/architectural layer.

**Guardrail engineering primitives documented by Anthropic** [D05-S19, D05-S20]:
- Input screening / harmlessness screens (small model + structured output classification).
- Hardened system prompts stating values and refusal behavior explicitly.
- Two distinct threat models: **direct prompt injection/jailbreak** (the user is the adversary) vs. **indirect prompt injection** (the user is trusted, but third-party content — web pages, emails, tool results — carries adversarial instructions). Different mitigations apply to each; conflating them is a common exam distractor pattern.
- For indirect injection: put untrusted content **only** in `tool_result` blocks (never in `system` or plain user text), tell the model explicitly what the content is and where it came from, JSON-encode untrusted strings to prevent "breakout," and never place your own instructions inside a tool result (the model is trained to treat tool-result content with skepticism, so instructions placed there may be ignored).
- Least privilege for agents: minimal tool scope, sandboxed execution, narrow permissions — reduces blast radius of a successful injection rather than trying to make injection impossible.
- Continuous monitoring and red-teaming close the loop but are detective, not preventive (see Objective-2 taxonomy below).
- Hallucination-specific guardrails [D05-S20]: explicit permission to say "I don't know"; extract-quotes-first grounding for long documents (>20K tokens); citation-then-verify (retract claims lacking a supporting quote); chain-of-thought verification; best-of-N consistency checks; explicit restriction to only the provided context. Anthropic's own docs state these "significantly reduce" but do **not eliminate** hallucination — always validate critical/high-stakes output through an independent path.

### Objective 2 — Identify risks, limitations, and failure modes of LLM systems

**Failure-mode taxonomy with architectural mitigation (not just a label):**

| Failure mode | Definition | Architectural mitigation |
|---|---|---|
| Hallucination / fabrication | Model generates fluent, plausible content unsupported by source or fact | Retrieval grounding + citations, quote-extraction-first prompting, independent verification pass, confidence-gated escalation to a human for unsupported claims [D05-S20, D05-S26] |
| Prompt injection — direct | Adversarial end user crafts input to override guardrails | Input screening classifier, hardened system prompt, output validation, rate-limiting/banning repeat offenders [D05-S19] |
| Prompt injection — indirect | Adversarial instructions arrive via retrieved content or tool output the model treats as legitimate | Isolate untrusted content to `tool_result` blocks, explicit provenance labeling, JSON-encoding, screen tool output before it reaches the model, least-privilege tool scope [D05-S19] |
| Excessive agency | Agent holds more tools/permissions/autonomy than the task requires | Remove unused tools/scopes (architectural), not just log or confirm — matches the exam guide's own least-privilege sample answer [D05-S30] |
| Insecure output handling | Model output is passed downstream (SQL, shell, HTML, another API) without validation, enabling injection/XSS/RCE in the consuming system | Treat model output as untrusted input to the next system: schema validation, output encoding/escaping, parameterized queries, sandboxed execution — this is OWASP LLM category "Improper Output Handling" [D05-S11] |
| Data leakage — cross-tenant | Multi-tenant RAG/agent system returns one customer's data to another | Tenant-scoped retrieval filters enforced at the data layer (not the prompt layer), per-tenant API keys/workspaces, isolation testing as part of eval suite |
| Data leakage — into logs | PII/PHI/secrets captured in observability logs, traces, or prompt-caching artifacts | Redaction/tokenization before persistence, log-field allow-lists, ZDR or short-TTL retention where feasible [D05-S04] |
| Supply-chain / MCP-server trust | Third-party MCP server or tool package executes with the agent's privileges; malicious or compromised servers can exfiltrate data or achieve RCE via unsanitized STDIO input | Install only from verified/signed sources, sandbox tool execution, treat MCP server config as untrusted input, monitor tool invocations, supply-chain attestation [D05-S23] |
| Nondeterminism / silent behavior drift | A model or prompt version change silently shifts output distribution; confident-but-wrong answers appear after a document refresh with model/latency unchanged | Version-pin models and prompts as controlled artifacts, regression-test against a fixed eval set on every change, and — per the exam guide's own sample item — treat "confident but wrong after a data refresh, model/latency unchanged" as a retrieval/indexing problem first, not a model problem [D05-S30, Sample 3] |
| Over-reliance / automation bias | Humans in a review loop rubber-stamp model output because it is usually right | Statistical sampling audits, deliberately injected error cases in review queues, tracking reviewer override/agreement rates, capping reviewer throughput to preserve attention |

### Objective 3 — Apply human-in-the-loop validation strategies

Design points, corroborated by industry practice (not a regulatory source) [D05-S25] and by Anthropic's own Usage Policy stance on high-risk domains [D05-S21]:

- **Tiers, in increasing cost/decreasing coverage-of-error:** 100% human review → risk-tiered review (review depth scales with an action's risk classification) → confidence/uncertainty-triggered escalation (route low-confidence outputs to a reviewer, high-confidence outputs proceed) → statistical sampling (review a random or stratified subset) → post-hoc audit (review after the action already took effect).
- **The tier choice is a function of two variables: action reversibility and impact magnitude.** An irreversible, high-impact action (fund transfer, medical dosing recommendation, account deletion) needs a synchronous human approval gate *before* execution — post-hoc audit cannot undo it. A reversible, low-impact action (drafting a reply for later human send) tolerates post-hoc audit or sampling.
- **Confidence-triggered escalation is not solely a function of the model's stated confidence** — industry pattern notes that escalation should also fire on irreversibility flags, anomaly signals, and approaching SLA breaches, independent of model confidence, because a model can be confidently wrong.
- **Costs of over-review:** reviewer fatigue and automation bias both degrade with volume — a reviewer who approves 500 items/day trends toward rubber-stamping. 100% review does not guarantee quality; it guarantees latency and cost.
- **Anthropic's own Usage Policy operationalizes this for a defined set of high-risk domains** (legal, medical/healthcare, insurance, financial advice, employment/housing decisions, academic assessment, journalism): it requires (a) a qualified human professional to review the content/decision before it is disseminated or finalized, and (b) disclosure to the end user that AI assisted in producing the advice or decision [D05-S21]. This is a policy-level HITL mandate architects should treat as a floor, not a ceiling, for regulated deployments.

### Objective 4 — Ensure compliance with regulations (GDPR, HIPAA, FedRAMP, and related frameworks)

See the **Compliance Matrix** (Section 2) and **Volatile Compliance Facts** (Section 3) below for the load-bearing detail. Summary of primitives:

- **GDPR**: purpose limitation and data minimization are Article 5 principles [D05-S12] that constrain what an architect may feed into a prompt or retrieve into context — richer retrieval is in direct tension with minimization (see trade-off spine). Article 22 restricts solely-automated decisions with legal/similarly-significant effect to three narrow lawful bases (law with safeguards, explicit consent, contract necessity) [D05-S13] — in practice this drives a human-in-the-loop requirement for consequential automated decisions in the EU. Controller/processor roles and international-transfer safeguards are handled contractually via Anthropic's DPA (processor role on the 1P API/Claude Platform on AWS; the cloud provider is processor on Bedrock/Google Cloud) [D05-S04].
- **HIPAA**: PHI may only flow to a BAA-covered surface with HIPAA readiness enabled at the organization level; this is enforced by the API itself (ineligible-feature requests return `400`) [D05-S04, D05-S05]. Minimum-necessary [D05-S14] and de-identification (Safe Harbor vs. Expert Determination) [D05-S15] are the two levers for reducing what PHI reaches the model at all — the strongest compliance posture minimizes PHI in the prompt before relying on contractual/technical safeguards around it.
- **FedRAMP**: the Anthropic 1P API itself is not a FedRAMP-authorized boundary; FedRAMP posture is a property of the *deployment surface*. Amazon Bedrock in AWS GovCloud carries FedRAMP High + DoD Impact Level 4/5 authorization [D05-S06, D05-S07]; Google Vertex AI (Assured Workloads) carries FedRAMP High + DoD IL2 only [D05-S08] — a materially lower ceiling for CUI-sensitive federal/defense workloads. This IL4/5-vs-IL2 gap is a genuine, exam-relevant discriminator between the two hyperscaler paths.
- **EU AI Act**: risk-tiered (unacceptable/high/limited/minimal); prohibited practices already in force since Feb 2025; transparency obligations (Art. 50) from Aug 2026; high-risk obligations pushed to Dec 2027 (Annex III) / Aug 2028 (Annex I) by the 2026 "Digital Omnibus" amendment [D05-S16] — architects must treat these dates as moving and verify against the current Official Journal text before committing to a compliance date in a real engagement.
- **NIST AI RMF**: voluntary, four-function lifecycle (Govern, Map, Measure, Manage) [D05-S17] — frequently referenced contractually as an evidentiary framework even where not legally mandated.
- **ISO/IEC 42001**: certifiable AI management system standard, PDCA-based [D05-S18]; Anthropic itself holds this certification [D05-S02] — useful as a due-diligence signal when *evaluating* an AI vendor, and as a target framework when a customer organization must demonstrate its own AI governance maturity.

### Objective 5 — Address ethical AI considerations (bias, fairness, transparency)

- **Bias/fairness testing as an eval discipline**, not a one-time check: Anthropic publishes a methodology example (political even-handedness eval: 1,350 paired opposing-viewpoint prompts across 150 topics and 9 task types, scored by a Claude-as-judge on even-handedness, acknowledgment of opposing views, and refusal rate) [D05-S22]. The architectural takeaway: bias evaluation needs a *designed, repeatable eval set* segmented by the dimension of concern (viewpoint, demographic proxy, language, geography), re-run on every model/prompt change — the same regression discipline as any other eval (Domain 4 overlap), applied to fairness metrics specifically. Disparate-impact review means slicing outcome metrics *by segment* and checking for gaps, not just an aggregate accuracy number.
- **Transparency and disclosure**: Anthropic's Usage Policy requires disclosing AI involvement to end users in consumer-facing chatbots and in the high-risk domains listed above [D05-S21]. This is a floor for any deployment; many regulatory regimes (EU AI Act Art. 50 limited-risk tier) independently require it.
- **Explainability and what citations/grounding can and cannot deliver**: Citations ground a claim in a specific source passage and make the response auditable, but Anthropic's own materials acknowledge occasional citation/quote mismatches, and citations do not explain the model's internal reasoning — they only show *where a stated fact came from*, not *why the model chose to say it* [D05-S26, D05-S20]. Architects should not conflate "the answer is grounded in a cited source" with "the decision process is explainable"; the former is evidentiary support, the latter is mechanistic insight that current LLMs do not natively provide.
- **Contestability/appeal paths**: implied by GDPR Article 22's exceptions (a data subject retains the right to obtain human intervention, express their view, and contest a solely-automated decision) [D05-S13] — architecturally this requires a designed appeal workflow, not just a HITL gate on the way in.
- **Documentation artifacts**: model cards/system cards (Anthropic publishes these per model, covering safety evaluations, alignment assessment, and model welfare [search-corroborated, see System Card references]), risk registers (NIST AI RMF Manage function output) [D05-S17], and DPIAs (GDPR-mandated for high-risk processing) are the standard governance paper trail an architect should expect to produce or feed into.

---

## 2. Compliance matrix

| Regulation/Framework | Architectural requirement | Control | Evidence artifact |
|---|---|---|---|
| GDPR — Art. 5 (purpose limitation, data minimization) | Only collect/forward the personal data needed for the stated purpose | Field-level filtering before prompt/RAG construction; scoped retrieval indices; upstream consent/legitimate-interest gate | Data-flow diagram, DPIA, DPA with Anthropic [D05-S12] |
| GDPR — Art. 22 (automated decision-making) | No solely-automated decision with legal/similarly-significant effect absent a qualifying basis | Human-in-the-loop approval before the decision is finalized; documented exception basis if automation proceeds; contestability/appeal workflow | Decision-workflow diagram with sign-off step; UI disclosure text; appeal process doc [D05-S13] |
| GDPR — erasure/retention | Support DSAR/erasure requests | Zero/short data retention (ZDR) where feasible; deletion workflow for logs and vector-store entries; redact PII pre-persistence | ZDR contract confirmation or documented log-retention policy [D05-S04] |
| GDPR — international transfers | Personal data must not leave an approved jurisdiction without a transfer safeguard | `inference_geo="us"` restriction (1P API/Claude Platform on AWS only) — note: no EU-specific pin exists on the 1P API; true EU-only inference residency requires a regional Bedrock/Vertex deployment instead | Workspace `data_residency` config; SCCs/DPA reference [D05-S27] |
| HIPAA — PHI handling | PHI only to a BAA-covered, HIPAA-enabled surface, using eligible features only | Execute BAA; enable HIPAA readiness at org level; restrict to eligible API features (enforced by API `400` on ineligible features); never place PHI in JSON schema fields | Signed BAA + HIPAA Implementation Guide; code-review checklist referencing feature-eligibility table [D05-S05, D05-S04] |
| HIPAA — minimum necessary | Limit PHI exposure to what the task requires | Field-level minimization before retrieval/prompt assembly; de-identify (Safe Harbor or Expert Determination) where full PHI isn't required | Data-minimization design doc; de-identification method record [D05-S14, D05-S15] |
| FedRAMP — federal/public-sector workloads | System must operate within an authorized boundary at the required impact level | Deploy via Amazon Bedrock in AWS GovCloud for FedRAMP High + DoD IL4/5 (CUI-level) workloads, or Google Vertex AI Assured Workloads for FedRAMP High + IL2 (lower-sensitivity) workloads; the 1P Anthropic API is not itself a FedRAMP-authorized boundary | Agency ATO referencing the cloud provider's FedRAMP package; architecture diagram showing the authorized boundary [D05-S06, D05-S07, D05-S08] |
| EU AI Act — high-risk systems | Conformity assessment, risk-management system, human oversight, logging, post-market monitoring before market placement | Designed human-oversight gate; immutable audit log of model version/prompt/inputs/outputs; technical documentation package | Technical file; EU declaration of conformity; EU database registration [D05-S16] |
| NIST AI RMF (contractual/voluntary) | Structured, iterative Govern→Map→Measure→Manage lifecycle | AI risk register with named owner; periodic re-measurement of safety/fairness metrics; governance charter | Risk register; governance charter document [D05-S17] |
| ISO/IEC 42001 (AI management system) | Certifiable AIMS with PDCA cycle | Documented AI policy; internal audit cadence; management review | Certificate (if pursuing certification) or self-attestation against clauses [D05-S18] |
| OWASP Top 10 for LLM Apps (engineering baseline, not law) | Defend against prompt injection, sensitive-info disclosure, excessive agency, improper output handling, supply-chain risk | Input/output classifiers; least-privilege tool scoping; tool-result isolation for untrusted content; sandboxed execution; signed/verified MCP servers | Threat model mapped to OWASP categories; red-team test report [D05-S10, D05-S11, D05-S19, D05-S23] |

---

## 3. Volatile compliance facts (verify before quoting in a live engagement)

| Claim | Source | Date verified |
|---|---|---|
| Claude API standard retention is 30 days by default; ZDR available on approval; Covered Models (Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5) require 30-day retention and are **not** ZDR-eligible unless expressly authorized by Anthropic | D05-S04, D05-S28 | 2026-09-24 |
| Flagged/trust-and-safety content may be retained up to 2 years regardless of ZDR or HIPAA arrangement | D05-S04 | 2026-09-24 |
| Anthropic holds SOC 2 Type I & II, ISO 27001:2022, and ISO/IEC 42001:2023; offers HIPAA-ready configuration (page last updated 2026-03-16) | D05-S02 | 2026-09-24 |
| HIPAA BAA covers the 1P Claude API (Messages API + a defined eligible-feature list) and sales-assisted Claude Enterprise; it does **not** cover the Claude.ai consumer product or the Claude for Teams tier | D05-S05, D05-S04 | 2026-09-24 |
| Claude via Amazon Bedrock in AWS GovCloud (US): FedRAMP High + DoD Impact Level 4/5 authorized; the specific model roster under this authorization expands over time with a lag (Claude Opus 4.8 added May 2026) | D05-S06, D05-S07 | 2026-09-24 |
| Claude via Google Vertex AI (Assured Workloads): FedRAMP High + DoD IL2 only — a materially lower ceiling than Bedrock's IL4/5 for CUI-sensitive workloads | D05-S08 | 2026-09-24 |
| The `inference_geo` API parameter supports only `"us"` or `"global"` — there is no EU-specific residency pin on the first-party API; the parameter does not apply on Bedrock or Vertex (region is set by endpoint/inference profile) or on Microsoft Foundry (which instead offers a separate US Data Zone deployment type) | D05-S27 | 2026-09-24 |
| EU AI Act: prohibited-practices provisions in force since Feb 2, 2025; transparency obligations (Art. 50) apply from Aug 2, 2026; high-risk obligations shifted by the 2026 "Digital Omnibus" amendment to Dec 2, 2027 (Annex III systems) and Aug 2, 2028 (Annex I systems) | D05-S16 | 2026-09-24 — treat exact Omnibus passage date and any further shift as [UNVERIFIED]; confirm against the current Official Journal text before an engagement relies on it |
| Anthropic's DPA is incorporated automatically into the Commercial Terms of Service; new sub-processors receive an objection window before use (reported externally as 15 days) | D05-S24 (secondary, not independently verified against Anthropic's primary DPA text) | 2026-09-24 — **[UNVERIFIED]** notice-period figure |

---

## 4. Contradictions surfaced

1. **FedRAMP model roster staleness.** D05-S06 (Anthropic's own Bedrock/FedRAMP announcement) still names "Claude 3.5 Sonnet v1 and Claude 3 Haiku" as the authorized models, with "additional models may be added in the future." D05-S07 (AWS, May 2026) confirms Claude Opus 4.8 was subsequently authorized in GovCloud. This is not a factual conflict so much as evidence that **FedRAMP authorization lags model release by design** (re-authorization is a compliance process, not a deploy). Course material should teach the architectural fact (Bedrock GovCloud = FedRAMP High/IL4-5 pathway) and explicitly flag "which model is authorized today" as something to verify per engagement, never asserted as fixed.
2. **"Claude is HIPAA compliant" (marketing framing) vs. primary source precision.** Multiple third-party blogs found during this research (search snippets, not cited as sources) assert blanket HIPAA compliance for Claude. Anthropic's own primary documentation (D05-S04, D05-S05) is explicit that compliance is a **shared responsibility**: a signed BAA, an org-level HIPAA-readiness flag, and use of *only* eligible features are all required together; using an ineligible feature (e.g., code execution, Batch API) under a HIPAA-enabled org returns a `400` error rather than silently proceeding. This precision gap is worth teaching explicitly as an anti-pattern ("BAA-washing").
3. **EU AI Act Digital Omnibus dating.** Secondary sources describe the 2026 amendment inconsistently (one calls it "AI Omnibus," dates it July 2026; the EC-sourced fetch describes the resulting dates but not the amendment's own passage date precisely). The resulting compliance deadlines (Dec 2027 / Aug 2028) are corroborated across sources; the amendment's exact passage date is not, and is marked [UNVERIFIED].

---

## 5. Open questions

- Exact current sub-processor list and the precise sub-processor-change notice period were not verified against Anthropic's primary DPA text (only a third-party summary was accessible in this session) — flag as [UNVERIFIED] `D05-S24`.
- Whether the *current* model lineup (Claude Opus 5, Claude Sonnet 5, Claude Haiku 4.5, Claude Fable 5.1) is FedRAMP-authorized on Bedrock GovCloud as of 2026-09-24 specifically was not confirmed beyond Opus 4.8 (May 2026) — course material should present the deployment-surface pattern, not assert a specific model's authorization status as durable fact.
- ISO/IEC 42001 clause-level requirements were sourced from secondary certification-body summaries only (the standard itself is paywalled); treat any clause-number claim as illustrative rather than verbatim.
- The OWASP Top 10 for LLM Applications 2025 official PDF could not be fetched directly (404 on the direct asset URL); the ranked list used here is corroborated by two independent secondary summaries (Aembit, Promptfoo) but not primary-verified against the OWASP document itself.
- Anthropic's precise current sub-processor GDPR "controller vs. processor" contractual language (e.g., exact DPA clause wording) was not directly read; the processor-role architecture (Anthropic is processor on 1P API/Claude Platform on AWS; the cloud provider is processor on Bedrock/Google Cloud) is corroborated by D05-S04's own explicit statement and is treated as verified.

---

## Prep-material landscape

A web search for third-party CCAR-P prep material returned multiple commercial offerings already live as of 2026-09-24, roughly two months after the exam guide's July 2026 effective date: a Learning Tree bootcamp, two distinct Udemy "CCAR-P Exam Prep" courses, a Tutorials Dojo study guide, a "Claude Certification Guide" site offering free mock exams and a 30-lesson/250+-question bank, Preporato (practice tests plus a blog "complete guide"), CertSafari (advertising 456 practice questions "aligned with the latest exam guide"), and SkillCertPro (a paid exam-questions product).

**Trust judgment: low, across the board.** None of these were consulted for content, per the brief's instruction to never copy from third-party prep material. Two independent risk signals justify the low-trust rating: (1) the exam's own confidentiality/non-disclosure terms mean no legitimate source has access to live item content, so any site claiming hundreds of "exam-style" questions "aligned with the exam guide" this soon after launch is necessarily synthesizing questions independently, with no way for a learner to verify fidelity to the real cognitive level; (2) the volume and speed of this content (multiple full question banks within ~60 days of a brand-new, narrowly-scoped professional certification going live) is a strong signature of rapid, likely AI-generated production rather than SME-authored, standard-setting-informed material. This course's practice items are original, written against the published blueprint and objectives in `claude-arch-professional-guide.md`, consistent with the brief's hard rule against reproducing or approximating live exam content.
