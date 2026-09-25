# Domain 5 — Governance, Safety & Risk Management — Independent Validation

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. [BLOCKER] §4 Scenario 3 + §2.5 + §3 T5 + §7 + §8 Item 4 rationale — the chapter teaches
   "CUI requires FedRAMP High + DoD IL4/5" and "the 1P Anthropic API is not a FedRAMP-authorized
   boundary." Both are wrong. Anthropic's own Public Sector FAQ states: "Claude for Government is
   Anthropic's FedRAMP-High authorized product" and "CUI and FIPS 199 High Impact data are
   authorized in Claude for Government, which is FedRAMP High authorized." DoD IL4/5 is a DoD
   construct, not a CUI prerequisite for a civilian federal agency. Scenario 3's recommended answer
   and every "why the others lose" line in it must be rewritten. [D05-V08, D05-V32]
2. [BLOCKER] §2.6 + §8 Item 12 rationale — "Anthropic's own docs acknowledge occasional
   citation/quote mismatches [D05-S26, D05-S20]" is an attribution to guidance that does not exist.
   Neither cited source says it. The Citations doc says the opposite: "citations are guaranteed to
   contain valid pointers to the provided documents." Remove or re-ground the claim. [D05-V21, D05-V22]
3. [BLOCKER] §4 Scenario 1 — "pick a non-'Covered Model' if ZDR is also required" builds the
   healthcare scenario on a false coupling. Anthropic: "If your organization handles PHI, HIPAA
   readiness is the arrangement to use; you do not also need ZDR." The Covered-Model/ZDR tension is
   irrelevant to a PHI workload under HIPAA readiness. [D05-V01]
```

**Verification tally:** 62 claims of fact extracted. **43 CONFIRMED · 11 CONTRADICTED · 8 NOT-FOUND.**

---

## What is good and must be preserved

- **The control-strength hierarchy and the preventive/detective/compensating split (§2.1, §2.2, T1, T2).**
  This is the chapter's best asset and it maps exactly onto the exam guide's own Sample 1 answer
  rationale. Keep the framing verbatim.
- **§2.3's direct-vs-indirect prompt-injection distinction and every mitigation listed under it.**
  I verified this line-by-line against Anthropic's `mitigate-jailbreaks` page: the two threat models,
  `tool_result`-only isolation, provenance labeling, JSON-encoding to prevent breakout, "don't put
  your own instructions in tool results," Haiku 4.5 as the screening model, tool-output screening,
  and least-privilege blast-radius reduction are all present in the primary source, in that shape.
  This is the most accurately sourced section of the chapter. [D05-V19]
- **§2.4 / T4's reversibility × impact discriminator, and the insistence that the tier attaches to the
  *action class*, not the system.** Architecturally correct and exam-shaped.
- **Practice Items 1, 3, 5, 6, 7, 9, 10, 11** — keys correct, distractors genuinely wrong, cognitive
  level matches the guide's Section 8 samples.
- **The §7 exam-day heuristics list**, except the FedRAMP line (see corrections).
- **§6's "BAA-washing" and "Logging as prevention" anti-patterns** — these are the right named traps
  and the primary sources back the underlying precision.

---

## Claim verification table

### Model lineup, model IDs, retention (task item a, b, j)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Covered Models are "Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, Claude Mythos 5" | Dossier §3 line 101; draft §4 Scen. 1 (as "Covered Model") | **CONFIRMED** | D05-V01, D05-V30 | Verbatim: "Claude Fable 5.1, Claude Mythos 5.1, Claude Fable 5, and Claude Mythos 5 are designated Covered Models … and require 30-day data retention". **Every one of these model names is real.** The task prompt's suspicion that "Mythos 5.1" / "Mythos 5" are fabricated is itself incorrect — `claude-mythos-5-1` and `claude-mythos-5` are documented active models (Project Glasswing access program only). No model name, family name, or ID anywhere in the dossier or draft is unverifiable. |
| Mythos 5.1 / Mythos 5 are generally available like Fable 5.1 | Dossier §3 (implied — listed flat alongside Fable) | **CONTRADICTED** | D05-V30 | Both are "Active (Project Glasswing only)"; Mythos 5.1 is "offered only to approved Project Glasswing customers" and is "Not offered on Claude Platform on AWS." Listing them undifferentiated beside Fable 5.1 misleads. |
| Covered Models require 30-day retention and are **not** ZDR-eligible unless expressly authorized by Anthropic | Dossier §3; draft §4 Scen. 1 | **CONFIRMED** | D05-V01, D05-V03, D05-V30 | Verbatim: "ZDR is therefore not available for any of them unless expressly authorized by Anthropic." Error is `400 invalid_request_error`, message "In order to access this model, your organization or workspace must have data retention enabled." |
| "Claude API standard retention is 30 days **by default**" | Dossier §3 line 101 | **CONTRADICTED** | D05-V01 | Verbatim: "Conversation content (your prompts and Claude's outputs) is **not retained by default**; the exception is Covered Models, which require 30-day retention." 30 days is the Covered-Model requirement, not a platform default. Dossier-only error, but it must not reach the chapter. |
| ZDR orgs can enable 30-day retention for a single workspace to reach Covered Models | not in draft | **CONFIRMED** | D05-V01 | Useful, missing nuance: "Organizations with a ZDR arrangement can make these models available in a specific workspace by enabling 30-day retention for that workspace only." |
| Flagged / trust-and-safety content may be retained up to 2 years regardless of arrangement | Dossier §3 | **CONFIRMED** | D05-V01 | Verbatim: "if a chat or session is flagged, Anthropic may retain inputs and outputs for up to 2 years." Not carried into the draft — worth adding. |
| ZDR is available "by approval" on the 1P API | Draft T5 | **CONFIRMED** | D05-V01 | "To request ZDR for your organization, contact the Anthropic sales team… ZDR is enabled per organization." |
| Current lineup per AGENT-BRIEF (Opus 5, Sonnet 5, Fable 5.1, Haiku 4.5) | brief §0 | **CONFIRMED (incomplete)** | D05-V30 | Full active catalog is larger: Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5, Opus 4.8/4.7/4.6, Sonnet 5, Sonnet 4.6, Haiku 4.5. The draft names no model at all, so no exposure. |

### `inference_geo` and data residency (task item d)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| The parameter is named `inference_geo` and supports only `"us"` or `"global"` | Draft T5; §2.5 compliance matrix (dossier) | **CONFIRMED** | D05-V02 | Doc table: `"global"` (Default) and `"us"`. Current limitations section: "**Inference geo:** Only `"us"` and `"global"` are available." |
| There is **no** EU-specific residency pin on the first-party API | Draft T5 | **CONFIRMED** | D05-V02 | No EU value exists. Workspace geo: "Currently, `"us"` is the only available workspace geo." |
| `inference_geo` is a top-level `POST /v1/messages` parameter | dossier implied | **CONFIRMED** | D05-V02, D05-V30 | "Add it to any `POST /v1/messages` call." On Managed Agents it nests inside the agent's `model` object instead. |
| `inference_geo` does not apply on Bedrock or Vertex (region set by endpoint), and Foundry uses a US Data Zone deployment type instead | Dossier §3 | **CONFIRMED** | D05-V02, D05-V30 | Verbatim in the doc's Note, including the Foundry "US Data Zone Standard deployment type" wording. |
| Workspace-level controls exist | dossier (as `data_residency` config) | **CONFIRMED** | D05-V02 | `allowed_inference_geos` and `default_inference_geo`, configurable via Console or Admin API "under the `data_residency` field." |
| *(Missing, material)* `inference_geo: "us"` costs 1.1x standard rates on all token categories | absent from draft | **NOT-FOUND in draft** | D05-V02 | A residency decision has a documented 1.1x price. A cost/compliance trade-off chapter that omits this is incomplete. |

### HIPAA (task item e)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Anthropic offers a BAA; PHI requires a signed BAA + org-level HIPAA readiness + eligible features only | Draft §2.5, T5, Item 2 | **CONFIRMED** | D05-V01, D05-V03 | "With a signed BAA and a HIPAA-enabled organization, you can use supported API features to process PHI." |
| The API returns `400` on an ineligible feature under a HIPAA-enabled org | Draft §2.5, Item 2 | **CONFIRMED (with exception)** | D05-V01 | Confirmed verbatim, but: "Client-side tools whose Details column … says they are not blocked are accepted but remain outside HIPAA readiness." The draft states enforcement as absolute. Add the carve-out. |
| A PHI workload needs ZDR in addition to HIPAA readiness, creating a Covered-Model trade-off | Draft §4 Scenario 1 | **CONTRADICTED** | D05-V01 | "If your organization handles PHI, HIPAA readiness is the arrangement to use; **you do not also need ZDR**." And: "HIPAA readiness applies a broader set of privacy and security safeguards than ZDR … rather than requiring immediate deletion." |
| HIPAA readiness is org-level and cannot be mixed with non-HIPAA workloads | absent from draft | **CONFIRMED** | D05-V01 | "HIPAA readiness is enforced at the organization level… use separate organizations for each." Also: "Once HIPAA readiness is enabled … the configuration is **permanent and cannot be disabled** by an administrator." Both are architect-grade facts the chapter omits. |
| BAA covers the 1P API and sales-assisted Claude Enterprise | Dossier §3 | **CONFIRMED (partially)** | D05-V03 | BAA article covers Claude Enterprise (Chat, Projects, Artifacts, File creation & code execution, Voice, Web Search, Research, Skills) and Claude Platform 1P API (Messages, Token Counting, Models, Org Management, Compliance APIs). Note the retention page's own "What HIPAA readiness covers" lists **only** the Claude API — the two Anthropic pages differ in scope; surface that, don't smooth it. |
| BAA does not cover "the Claude for Teams tier" | Dossier §3 | **NOT-FOUND** | D05-V03 | The BAA article's exclusions name consumer products (Free/Pro/Max), Claude Console, Claude Cowork, and beta features. "Teams" is not named there. (The retention page separately says Claude Teams interfaces are not *ZDR*-eligible — a different arrangement.) Not in the draft; do not import it. |
| 1P API BAA excludes Batch API, Files API, Skills API, Code Execution, Computer Use, Web Fetch | absent from draft | **CONFIRMED** | D05-V03 | Concrete and exam-usable. The chapter says "eligible features" abstractly; this list is the substance. |
| "Never place PHI in JSON schema fields" | Dossier §2 matrix | **CONFIRMED** | D05-V01 | Verbatim: "**Do not include PHI in JSON schema definitions.** This restriction applies to schema property names, `enum` values, `const` values, and `pattern` regular expressions." Not in the draft — a genuine loss. |
| Minimum-necessary standard | Draft §2.5 | **CONFIRMED** | D05-V25 | 45 CFR 164.502(b), 164.514(d): "make reasonable efforts to limit protected health information to the minimum necessary to accomplish the intended purpose." |
| De-identification via Safe Harbor or Expert Determination | Draft §2.5 | **CONFIRMED** | D05-V24 | Expert Determination §164.514(b)(1); Safe Harbor §164.514(b)(2) (18 identifier types). Official names match. |
| Bedrock HIPAA path: "BAA through AWS (AWS is processor)" | Draft T5 | **CONFIRMED** | D05-V26, D05-V01 | Amazon Bedrock is a HIPAA-eligible service; AWS BAA required first. Processor role confirmed by D05-V01. |
| Vertex HIPAA path: "BAA through Google (Google is processor)" | Draft T5 | **NOT-FOUND** | D05-V27 | Google offers a BAA, but "Vertex AI," "Vertex AI Platform," and "Agent Platform" are **not** in Google Cloud's Covered Products list as such (the list names *Vertex AI Workbench instances*, *Generative AI on Gemini Enterprise Agent Platform*, *Gemini Enterprise Agent Platform*). Google's own instruction: "Disable or otherwise ensure that you do not use Google Cloud Products that are not explicitly covered by the BAA … when working with PHI." This T5 cell carries **no citation at all** and routes PHI on an unverified basis. |
| HIPAA readiness is **not** available on Claude Platform on AWS or Microsoft Foundry | absent from draft | **CONFIRMED** | D05-V01 | Directly contradicts the intuition that Anthropic-operated surfaces inherit HIPAA posture. Belongs in T5. |

### FedRAMP / DoD posture (task item c) — the weakest thread in the chapter

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Bedrock in AWS GovCloud (US) reaches FedRAMP High + DoD IL4/5 for Claude | Draft §2.5, T5, §7, Item 4 | **CONFIRMED** | D05-V05, D05-V08 | "Claude models are approved for use in FedRAMP High and DoD Impact Level 4 and 5 workloads through Amazon Bedrock in AWS GovCloud (US) regions" (Anthropic, 2025-06-11). Corroborated: "ITAR data can only be processed in Claude via AWS Bedrock, which is IL5 accredited." |
| Google Vertex AI (Assured Workloads) tops out at IL2 | Draft §2.5, T5, §7, Item 4 opt. C | **CONFIRMED (stale, must be date-stamped)** | D05-V06, D05-V08 | Source is a **2025-04-02** announcement: "Claude models are now authorized for FedRAMP High and IL-2 workloads," which itself says it "lays groundwork toward future IL5 compatibility." Anthropic's *current* Public Sector FAQ restates Vertex only as "FedRAMP-High" and does not repeat IL2; it corroborates the IL ceiling indirectly by routing ITAR/IL5 to Bedrock only. Defensible today, but the chapter states it as timeless fact ("it cannot meet that bar today") on an 18-month-old blog. Date-stamp it. |
| "The 1P Anthropic API is not itself a FedRAMP-authorized boundary" | Draft §2.5, T5, §7, Item 4 rationale | **CONTRADICTED** as written | D05-V08, D05-V10 | Anthropic: "**Claude for Government is Anthropic's FedRAMP-High authorized product**, which is available to both government customers and contractors" and "Claude for Government (C4G) is our standalone application that is FedRAMP-High authorized." A separate FedRAMP Marketplace listing for CSP "Anthropic," product "Claude," shows status "Not yet certified," phase "Initial Implementation," 0 ATOs — so the *commercial* `api.anthropic.com` boundary claim is narrowly survivable, but the chapter's blanket phrasing erases an Anthropic-native FedRAMP High path and is wrong for a public-sector engagement. |
| "CUI requires the FedRAMP High + IL4/5 boundary Bedrock GovCloud provides" | Draft §4 Scenario 3 | **CONTRADICTED** | D05-V08, D05-V32 | Anthropic: "**CUI and FIPS 199 High Impact data are authorized in Claude for Government, which is FedRAMP High authorized.**" DoD ILs are a DoD Cloud Computing SRG construct (IL2/4/5/6); IL4 accommodates CUI *for DoD communities*, IL5 unclassified NSS data. A civilian federal agency processing CUI needs the appropriate FedRAMP baseline, not DoD IL4/5. The scenario's stem, recommendation reason, and both "why the others lose" lines are all built on the false requirement. |
| Vertex Assured Workloads is "insufficient for CUI" | Draft §4 Scenario 3 opt. (c) | **CONTRADICTED** | D05-V08 | Vertex with Assured Workloads is FedRAMP-High per Anthropic's own FAQ; FedRAMP High covers CUI/FIPS 199 High. It is insufficient for **IL4/5/ITAR**, not for CUI. |
| Bedrock's ceiling for Claude is IL4/5 | Draft §7 heuristic | **CONTRADICTED (understated)** | D05-V08 | "Claude is available in the AWS Secret region (IL6) via Amazon Bedrock." The stated ceiling is one level too low. |
| D05-S07 (AWS GovCloud / Opus 4.8) supports a FedRAMP claim | Dossier §3, §4 | **CONTRADICTED** | D05-V07 | The AWS page announces availability only and "contains no mention of FedRAMP certification or DoD Impact Level compliance." The dossier's inference ("Confirms the FedRAMP High GovCloud authorization roster is extended…") is not in the source. Separately, the page is dated **June 30, 2026**, not "May 2026" as the dossier and the source-table URL path imply. |
| "FedRAMP authorization lags model release by design; re-authorization is a compliance process, not a deploy" | Dossier §4 finding 1; draft §10 UNVERIFIED list | **CONTRADICTED** | D05-V09 | Anthropic: "**There is no separate FedRAMP audit per model. Vertex's authorization is infrastructure-level, not per-model. Once the Claude for Government environment is authorized, new models inherit that authorization automatically.**" And: "New models are typically available in Claude for Government the same day or within one to two days of their commercial release." The draft's standing `[UNVERIFIED]` note ("whether the current Claude 5-family lineup is FedRAMP-authorized … only Opus 4.8 is confirmed") encodes a misconception and must be deleted, not carried forward. |
| Anthropic's certification page lists no FedRAMP authorization | supports draft's 1P framing | **CONFIRMED** | D05-V04 | Page lists only HIPAA-ready (BAA available), ISO 27001:2022, ISO/IEC 42001:2023, SOC 2 Type I & II. No FedRAMP. Consistent with C4G's authorization living outside this commercial-certifications page. |

### GDPR (task item f)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Art. 5 contains purpose limitation and data minimisation | Draft §2.5, T6 | **CONFIRMED** | D05-V12 | Art. 5(1)(b) purpose limitation; 5(1)(c) data minimisation ("adequate, relevant and limited to what is necessary"). Art. 5(1)(e) storage limitation and 5(2) accountability also confirmed — both relevant to the draft's logging/retention arguments and currently uncited. |
| Art. 22 restricts solely-automated decisions with legal or similarly significant effect | Draft §2.5, Item 3 | **CONFIRMED** | D05-V11 | Art. 22(1) quoted verbatim. |
| The three lawful bases are contract necessity, EU/Member-State law with safeguards, explicit consent | Draft §2.5 | **CONFIRMED** | D05-V11 | Art. 22(2)(a)–(c). |
| A retained right to human intervention and to contest | Draft §2.5, §2.6, Scenario 2 | **CONFIRMED (with precision gap)** | D05-V11 | Art. 22(3) safeguards — "the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision" — apply to bases **(a) and (c) only** (contract and explicit consent), not to the law-authorized basis (b). Scenario 2's "changes the answer" line gets this right; §2.5's flat phrasing does not. |
| Anthropic is processor on the 1P API / Claude Platform on AWS; the cloud provider is processor on Bedrock / Google Cloud | Draft §2.5 | **CONFIRMED (incomplete)** | D05-V01 | Verbatim: "This page covers the Claude API (`api.anthropic.com`), Claude Platform on AWS, and Claude in Microsoft Foundry, where Anthropic is the data processor. On Amazon Bedrock and Google Cloud's Agent Platform, the cloud provider is the data processor." **Microsoft Foundry is omitted from the draft** and belongs on the Anthropic-as-processor side. |
| Art. 17 erasure is cited | — | **NOT-FOUND (no exposure)** | — | The draft cites no article number for erasure; the dossier matrix says only "GDPR — erasure/retention." No wrong article number exists anywhere in either file. Task item (f)'s Art. 17 concern does not apply. |
| Sub-processor objection window is 15 days | Dossier §3, flagged `[UNVERIFIED]` | **NOT-FOUND** | — | Correctly flagged and correctly excluded from the draft. Do not promote it. |
| Moving logs outside the EU does not avoid GDPR (Item 9 opt. D) | Item 9 rationale | **CONFIRMED** | D05-V11, D05-V12 | Rationale says "misreads GDPR's extraterritorial scope" — true, but the sharper defect is that an export is itself a Chapter V restricted transfer. Strengthen. |

### EU AI Act (task item g)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Risk-tiered structure with four tiers | Draft §2.5 | **CONFIRMED** | D05-V13 | EC page names them verbatim: "Unacceptable risk", "High risk", "**Transparency risk**", "Minimal or no risk". |
| The tier requiring disclosure is the "limited-risk tier" | Draft §2.6 | **CONTRADICTED** | D05-V13 | "Limited risk" is legacy/informal terminology. The Commission's current naming is **transparency risk**. Exam prep must use the current official name. |
| Prohibited practices in force since Feb 2, 2025 | Draft §2.5 | **CONFIRMED** | D05-V13, D05-V14 | 2 February 2025, prohibitions 1–8 plus AI-literacy obligations. Note prohibition 9 (non-consensual intimate material / CSAM) applies December 2026. |
| Art. 50 transparency obligations from Aug 2026 | Draft §2.5 | **CONFIRMED** | D05-V13, D05-V14 | 2 August 2026, with providers of synthetic-media systems given until 2 December 2026 to comply. Art. 50 heading confirmed as "Transparency Obligations for Providers and Deployers of Certain AI Systems." |
| High-risk obligations shifted to Dec 2027 (Annex III) / Aug 2028 (Annex I) by a 2026 amendment | Draft §2.5 | **CONFIRMED** | D05-V13, D05-V14, D05-V15 | 2 December 2027 (Annex III / Chapter III high-risk in sensitive areas) and 2 August 2028 (Annex I / high-risk embedded in regulated products). |
| The amendment ("Digital Omnibus") passage date is `[UNVERIFIED]` | Dossier §3, §4; draft §10 | **CONTRADICTED — now verifiable** | D05-V13, D05-V15 | The AI Omnibus was proposed **19 November 2025**, reached political agreement **7 May 2026**, and **entered into force 27 July 2026**. It is adopted and in force as of 2026-09-24. Remove the `[UNVERIFIED]` flag and state the dates. |
| A high-risk conformity file expects logging **and** a separate human-oversight mechanism | Draft §2.2, cited to D05-S16 | **NOT-FOUND at the cited source; CONFIRMED elsewhere** | D05-V13, D05-V28, D05-V29 | The EC overview page does not say this. Regulation (EU) 2024/1689 does: Art. 12 "Record-Keeping" ("High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system") and Art. 14 "Human Oversight" are distinct obligations. Re-cite to the Regulation. |

### Certifications and frameworks (task item h)

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Anthropic holds SOC 2 Type I & II, ISO 27001:2022, ISO/IEC 42001:2023, HIPAA-ready config; page updated 2026-03-16 | Dossier §3 | **CONFIRMED** | D05-V04 | Exact list and "Last Updated: March 16, 2026" both match. |
| NIST AI RMF functions are Govern, Map, Measure, Manage; framework is voluntary | Draft §2.5 | **CONFIRMED** | D05-V16 | "Govern, Measure, Manage, Map"; "intended for voluntary use". AI RMF 1.0, released January 26, 2023. |
| ISO/IEC 42001 is a certifiable AI management system standard using PDCA | Draft §2.5 | **CONFIRMED (secondary only)** | D05-V04, D05-S18 | The certification's existence and Anthropic's holding of it are primary-confirmed. PDCA structure rests on a certification-body summary; the standard text is paywalled. Correctly flagged in the dossier. |
| OWASP Top 10 for LLM Applications 2025 list, ten entries | Draft §2.5 | **CONFIRMED** | D05-V17 | All ten verified verbatim: LLM01 Prompt Injection · LLM02 Sensitive Information Disclosure · LLM03 Supply Chain · LLM04 Data and Model Poisoning · LLM05 Improper Output Handling · LLM06 Excessive Agency · LLM07 System Prompt Leakage · LLM08 Vector and Embedding Weaknesses · LLM09 Misinformation · LLM10 Unbounded Consumption. 2025 is the current version; no newer edition. The draft's §2.5 list matches in content and order. |
| §2.3 names the category "**Insecure** output handling" | Draft §2.3 | **CONTRADICTED** | D05-V17 | The 2025 name is "**Improper** Output Handling" (LLM05:2025). "Insecure Output Handling" is the superseded 2023 name. §2.5 gets it right; §2.3 does not — internally inconsistent and teaches a retired label. |
| OWASP list could not be primary-verified (dossier open question) | Dossier §5 | **CONTRADICTED** | D05-V17 | `https://genai.owasp.org/llm-top-10/` serves the full ranked list. The dossier's "primary-verified only via two secondary summaries" caveat can be retired. |

### Guardrails, hallucination, HITL, ethics

| Claim | Location | Verdict | Source | Note / correct value |
|---|---|---|---|---|
| Two distinct threat models: jailbreak/direct injection vs. indirect injection | Draft §2.3 | **CONFIRMED** | D05-V19 | Verbatim in the doc, with the user-as-adversary vs. trusted-user/third-party-content distinction stated exactly as the draft frames it. |
| Untrusted content goes **only** in `tool_result` blocks, never `system` or plain user text | Draft §2.3, Item 6 | **CONFIRMED** | D05-V19 | "Put untrusted content only in tool results… never in `system` prompts or plain user `text` blocks." |
| Label provenance; JSON-encode untrusted strings; don't put your own instructions in tool results | Draft §2.3 | **CONFIRMED** | D05-V19 | All three present verbatim, including the "break out" rationale for JSON encoding. |
| Screen tool outputs with a lightweight model (Haiku 4.5) using structured outputs | Dossier §1; draft §2.3 | **CONFIRMED** | D05-V19 | "pass its raw output to a small classifier call with Claude Haiku 4.5". |
| Hallucination mitigations: permit "I don't know"; quote-extraction first for long docs; citation-then-verify with retraction; chain-of-thought verification; best-of-N; external-knowledge restriction | Draft §2.3, §2.6, Item 11 | **CONFIRMED** | D05-V20 | All present. The >20k-token threshold is verbatim: "For tasks involving long documents (>20k tokens)". |
| These techniques reduce but do not eliminate hallucination | Draft §2.3 (implied), Item 11 | **CONFIRMED** | D05-V20 | Verbatim: "while these techniques significantly reduce hallucinations, they don't eliminate them entirely. Always validate critical information, especially for high-stakes decisions." |
| "Anthropic's own docs acknowledge occasional citation/quote mismatches" | Draft §2.6, Item 12 rationale | **CONTRADICTED** | D05-V21, D05-V22 | Neither cited source says this. The Citations documentation says: "**Better citation reliability:** … citations are guaranteed to contain valid pointers to the provided documents." The launch blog reports a customer reducing "source hallucinations and formatting issues from 10% to 0%." This is an attribution to Anthropic guidance that does not exist. |
| Citations ground a claim but do not explain the model's reasoning | Draft §2.6, Item 12 key B | **CONFIRMED (as reasoning, not as citation)** | D05-V21 | Substantively correct and the right thing to teach — the docs describe citations as returning "the exact passages that support each claim, so you can verify answers," never as an explainability mechanism. But no Anthropic source *states* the negative; present it as analysis, not as quoted guidance. |
| Anthropic's Usage Policy mandates qualified-professional review before dissemination in high-risk domains, plus AI disclosure | Draft §2.6, dossier §1 | **CONFIRMED** | D05-V18 | Verbatim: "a qualified professional in that field must review the content or decision prior to dissemination or finalization" and "you must disclose to them that you are using AI to help produce your advice, decisions, or recommendations. This disclosure must be provided at a minimum at the beginning of each session." Consumer-facing chatbots additionally "must disclose to users that they are interacting with AI rather than a human." |
| The high-risk domain list | Dossier §1 | **CONFIRMED** | D05-V18 | Legal · Healthcare · Insurance · Finance · Employment and housing · Academic testing, accreditation and admissions · Media or professional journalistic content. |
| Anthropic's bias-eval methodology: paired opposing-viewpoint prompts, model-as-judge | Draft §2.6 | **CONFIRMED (mis-cited)** | D05-V23 | "We tested the models using **1,350 pairs of prompts across 9 task types and 150 topics**"; graded by **Claude Sonnet 4.5** as automated grader, with cross-checks using other Claude models and GPT-5. Scored on even-handedness, opposing perspectives, refusals. The draft cites D05-S22 (Transparency Hub); the actual source is the political-even-handedness publication. Re-cite. |
| HITL tiering, escalation triggers beyond model confidence | Draft §2.4, T4, Item 7 | **CONFIRMED as practitioner synthesis** | D05-S25 (secondary) | No primary/regulatory source backs the five-tier ladder. The draft does not overclaim it as vendor guidance — acceptable, but the chapter should say plainly that this taxonomy is a design framework, not published Anthropic or standards-body doctrine. |
| MCP/tool supply-chain risk (third-party servers run with agent privileges; sandbox + verified sources) | Draft §2.3, Scenario 7 | **CONFIRMED as secondary** | D05-S23 (secondary) | Architecturally uncontroversial and OWASP LLM03-aligned. Single practitioner-blog source for a specific STDIO shell-injection finding; the general mitigation set is safe to teach. |
| §2.1's hierarchy ranks Classifier/filter (3) above Programmatic validation (4) | Draft §2.1 vs. T1 | **CONTRADICTED (internal)** | — | T1's own bypass-resistance row rates programmatic validation "High for what it checks" and classifier "Medium — a second model can also be fooled." The §2.1 ordering inverts the chapter's own analysis. Not an external-source error, but it breaks the chapter's central teaching device. |

---

## Corrections required

**C1 — §4 Scenario 3, replace the whole scenario body.**

> **3 — Public sector: citizen-services chatbot.** *Situation:* a federal civilian agency wants a
> chatbot answering benefits questions from internal policy documents classified as CUI.
> *Approaches:* (a) call the commercial 1P Claude API directly; (b) deploy on a FedRAMP High
> authorized surface — Claude for Government, Bedrock in AWS GovCloud, or Vertex AI with Assured
> Workloads; (c) assume DoD IL4/5 is required and deploy only via Bedrock GovCloud.
> *Recommended:* (b). CUI and FIPS 199 High Impact data are authorized at the **FedRAMP High**
> baseline; Anthropic states that "CUI and FIPS 199 High Impact data are authorized in Claude for
> Government, which is FedRAMP High authorized" [D05-V08]. All three FedRAMP High paths qualify;
> choose among them on procurement, existing ATO reuse, and cloud-native fit.
> *Why the others lose:* (a) the commercial `api.anthropic.com` boundary is not the authorized
> environment — Claude for Government is a distinct offering. (c) over-constrains: DoD Impact
> Levels are a DoD Cloud Computing SRG construct (IL2/4/5/6), not a prerequisite for a civilian
> agency's CUI [D05-V32]. *Changes the answer:* a **DoD** component, or ITAR data, moves this to
> Bedrock — "ITAR data can only be processed in Claude via AWS Bedrock, which is IL5 accredited,"
> and Claude is available in the AWS Secret region (IL6) via Bedrock [D05-V08]. Data
> classification belongs to the agency's classification authority, not the architect.

**C2 — §2.5 FedRAMP bullet, replace.**

> - **FedRAMP** — a property of the *deployment surface*, not the model, and FedRAMP baselines
>   (Low/Moderate/High) are a separate construct from DoD Impact Levels (IL2/4/5/6). As of
>   2026-09-24: Claude for Government is Anthropic's FedRAMP High authorized standalone product,
>   with CUI and FIPS 199 High Impact data in scope; Bedrock in AWS GovCloud (US) adds DoD IL4/5
>   (and IL6 in the AWS Secret region); Vertex AI with Assured Workloads is FedRAMP High. ITAR is
>   Bedrock-only. The **commercial** 1P API (`api.anthropic.com`) is not the authorized boundary —
>   a public-sector deployment moves to C4G or a CSP path. Authorization is **infrastructure-level,
>   not per-model**: "There is no separate FedRAMP audit per model… new models inherit that
>   authorization automatically" [D05-V08, D05-V09, D05-V06, D05-V32].

**C3 — §7 heuristic, replace the FedRAMP line.**

> - **FedRAMP High ≠ DoD IL.** CUI / FIPS 199 High → any FedRAMP High surface (Claude for
>   Government, Bedrock GovCloud, Vertex Assured Workloads). DoD IL4/5 or ITAR → Bedrock GovCloud
>   only; IL6 → Bedrock AWS Secret region. An option that says "the commercial API is fine for a
>   federal CUI workload" is wrong; so is one that says "CUI requires IL4/5."

**C4 — §8 Item 4, revise stem and rationale.** Keep keys B and C, but (i) date-stamp option C:
`"Google Vertex AI Assured Workloads was authorized at FedRAMP High and DoD IL2 (April 2025), below this workload's IL4/5 bar"`;
(ii) replace option A's rationale with: *"A is wrong — the commercial 1P API is not the authorized
environment, and Anthropic's own FedRAMP High offering (Claude for Government) is authorized at
FedRAMP High, not DoD IL4/5; ITAR/IL5 routes to Bedrock GovCloud."*

**C5 — §4 Scenario 1, replace the recommendation clause.** Delete "and pick a non-'Covered Model'
if ZDR is also required, or accept 30-day retention if the Covered Model's capability is worth that
trade." Replace with:

> *Recommended:* (b). Under HIPAA readiness, ZDR is not additionally required — "If your
> organization handles PHI, HIPAA readiness is the arrangement to use; you do not also need ZDR"
> [D05-V01]. The real design constraints are the eligible-feature list (no Batch API, Files API,
> Skills API, code execution, computer use, or web fetch under the BAA), the rule that PHI must
> never appear in JSON schema definitions, and the fact that HIPAA readiness is org-level and
> permanent once enabled — so a HIPAA org is a separate org from general-purpose workloads.

**C6 — §2.6, delete the citation-mismatch claim.** Replace the bullet with:

> - **Explainability vs. grounding** — citations return the exact source passages supporting a
>   claim, which makes the answer auditable; they do not expose why the model chose to make the
>   claim. Anthropic documents citations as a verification affordance ("citations are guaranteed to
>   contain valid pointers to the provided documents" [D05-V21]) — a valid pointer is not the same
>   as a *sufficient* one, so a claim can still overreach the passage it cites. Auditability is not
>   mechanistic explainability.

**C7 — §8 Item 12 rationale, replace the reason C fails.** *"C is wrong because a guaranteed-valid
pointer into a source document is not a guarantee that the claim it supports is correct: Anthropic
states that grounding techniques 'significantly reduce hallucinations' but 'don't eliminate them
entirely' [D05-V20]."*

**C8 — §2.3, rename the OWASP category.** "Insecure output handling" → **"Improper Output Handling
(OWASP LLM05:2025)"**. Apply verbatim OWASP names in §2.5 as well: *Sensitive Information
Disclosure · Supply Chain · Data and Model Poisoning · Improper Output Handling · Excessive Agency ·
System Prompt Leakage · Vector and Embedding Weaknesses · Misinformation · Unbounded Consumption.*

**C9 — §2.6, rename the AI Act tier.** "the EU AI Act's limited-risk tier" → **"the EU AI Act's
transparency-risk tier (Art. 50)"**. In §2.5, name all four: *unacceptable risk, high risk,
transparency risk, minimal or no risk* [D05-V13].

**C10 — §2.5 EU AI Act bullet, de-hedge the amendment.** Replace "shifted by a 2026 amendment" with:
*"shifted by the AI Omnibus (proposed 19 Nov 2025, political agreement 7 May 2026, in force 27 July
2026) to 2 Dec 2027 (Annex III) / 2 Aug 2028 (Annex I) [D05-V13, D05-V15]."* Add that Art. 50
transparency applies from 2 Aug 2026 with a 2 Dec 2026 compliance window for synthetic-media
providers.

**C11 — §10 UNVERIFIED list, delete two entries.** Remove "whether the current Claude 5-family
lineup is FedRAMP-authorized on Bedrock GovCloud today specifically (only Opus 4.8, May 2026, is
confirmed)" — the premise is wrong; authorization is infrastructure-level, not per-model [D05-V09].
Remove the Digital Omnibus passage-date entry — it is now verified [D05-V15].

**C12 — §3 T5, fix three cells.** (i) Vertex HIPAA cell: replace "BAA through Google (Google is
processor)" with *"Google BAA required; confirm the specific Google Cloud product is on Google's
Covered Products list before routing PHI — 'Vertex AI' is not listed by that name [D05-V27]"*.
(ii) Add a row: *HIPAA readiness availability — 1P API: Yes; Claude Platform on AWS: No; Microsoft
Foundry: No [D05-V01]*. (iii) FedRAMP row, 1P column: replace "Not itself an authorized boundary"
with *"Commercial API: no. Claude for Government (separate Anthropic offering): FedRAMP High
[D05-V08]"*.

**C13 — §2.5 GDPR bullet, add Foundry.** "Anthropic is processor on the 1P API, Claude Platform on
AWS, **and Claude in Microsoft Foundry**; the cloud provider is processor on Amazon Bedrock and
Google Cloud's Agent Platform [D05-V01]."

**C14 — §2.5 GDPR Art. 22, add the safeguard precision.** The Art. 22(3) human-intervention /
view / contest safeguards attach to the contract-necessity and explicit-consent bases, not to the
law-authorized basis [D05-V11].

**C15 — §2.1, reorder to match T1.** Swap tiers 3 and 4 so programmatic validation ranks above
model-based classification, or add one sentence explaining why the ordering differs from T1's
bypass-resistance row. As written the chapter contradicts itself on its own central device.

**C16 — §2.5 HIPAA bullet, add the enforcement carve-out.** The `400` is automatic "except for the
client-side tools whose Details column … says they are not blocked (those are accepted but remain
outside HIPAA readiness)" [D05-V01].

**C17 — T5 data-residency row, add the price.** `inference_geo: "us"` is billed at **1.1x** standard
rates across input, output, cache writes and cache reads, and draws 1.1 tokens per token against
Priority Tier capacity [D05-V02]. A residency trade-off table without the cost axis is incomplete.

---

## Answer-key audit

I solved each item independently before reading the draft's rationale.

| # | Type | Keyed | Verdict | Reasoning |
|---|---|---|---|---|
| 1 | select 1 | B | **KEY-CORRECT** | Removing the credit tool is architectural removal. A (confirmation) is a weaker gate on a capability that still exists; C (lower limit) is a compensating control that preserves an unneeded capability; D is detective. Mirrors the guide's Sample 1 exactly. Distractor analysis is accurate. |
| 2 | select 1 | B | **KEY-CORRECT** | BAA + org-level HIPAA readiness + eligible-features-only is precisely Anthropic's documented requirement [D05-V01, D05-V03]. A conflates tier with compliance; C is a different arrangement Anthropic explicitly says is not additionally needed for PHI; D is generic hygiene. *Rationale fix:* sharpen C from "partly-incompatible … not a substitute" to "not required — Anthropic states HIPAA readiness is the arrangement for PHI and you do not also need ZDR." |
| 3 | select 1 | B | **KEY-CORRECT** | A denial is a legal/similarly-significant effect from solely-automated processing → Art. 22 [D05-V11]. A (Art. 5) is about collection scope; C is healthcare-only; D is federal-cloud-only. Single best answer. |
| 4 | select 2 | B, C | **KEY-ARGUABLE** | Both keys are defensible and A and D remain wrong, so the item still has exactly two correct options. But the item leans on two soft spots: (i) C's "currently tops out at IL2" rests solely on an April 2025 blog that itself anticipates future IL5, with no current Anthropic restatement — date-stamp it or the item ages into wrongness; (ii) the **rationale for A is factually wrong** — "the 1P API is not itself a FedRAMP-authorized boundary" ignores Claude for Government's FedRAMP High authorization [D05-V08]. A stays wrong for the stated IL4/5 bar, but for the wrong published reason. Apply C4. |
| 5 | select 1 | B | **KEY-CORRECT** | Version-pin + pre-promotion regression eval is the governance control for silent behavior change. A is defeatist; C is reactive; D trades capability without addressing unmanaged promotion. *Minor:* on the 1P API model IDs are already pinned, so the stem's "routine model version upgrade with no code changes" is slightly artificial — rephrase as "a scheduled upgrade to a newer model ID shipped by the platform team" to keep the premise clean. |
| 6 | select 1 | B | **KEY-CORRECT** | Verbatim Anthropic guidance: untrusted content only in `tool_result`, with explicit provenance [D05-V19]. A directly violates the doc ("never in `system` prompts"); D is unrelated. *Rationale fix:* C is not merely "the weakest layer" — the same doc **does** recommend stating an untrusted-content policy in the system prompt. Say instead: "C is one of Anthropic's recommended layers but insufficient alone, because it leaves untrusted content structurally indistinguishable from your instructions; B changes the structure." Leaving the rationale as-is teaches candidates to dismiss a documented mitigation. |
| 7 | select 1 | C | **KEY-CORRECT** | Irreversible + high-impact → synchronous pre-execution gate. A and D let the transfer complete; B applies the costliest tier to a reversible, low-impact action. Clean single best answer. |
| 8 | select 2 | A, B | **KEY-CORRECT but the item should be cut or rebuilt** | LLM01:2025 Prompt Injection and LLM06:2025 Excessive Agency are both verified category names [D05-V17]; C and D are not categories. The key is right. The item is however pure recall with two obviously invented distractors — it violates AGENT-BRIEF §3.9 ("scenario stem, no trivia") and the guide's Section 8 cognitive level. Rebuild as a scenario that requires *classifying* a described failure into the correct OWASP category, with distractors drawn from adjacent real categories (e.g. LLM05 Improper Output Handling vs. LLM06 Excessive Agency vs. LLM02 Sensitive Information Disclosure). |
| 9 | select 1 | C | **KEY-CORRECT** | Redact/tokenize before persistence while keeping structural metadata is the documented resolution. A over-corrects; B ignores minimization and storage limitation (Art. 5(1)(c), (e)); D misreads scope. *Rationale fix:* D fails on two counts — Art. 3 territorial scope **and** Chapter V restricted-transfer rules. Also: D05-S04 is cited for C, but the retention page does not prescribe log redaction; the practice is sound but should cite GDPR Art. 5(1)(c)/(e) [D05-V12] instead of implying Anthropic guidance. |
| 10 | select 1 | B | **KEY-CORRECT** | Ongoing re-evaluation after model/prompt change. A overstates; C is the absence-of-evidence fallacy; D is false. *Citation fix:* the eval methodology cited belongs to the political-even-handedness publication [D05-V23], not the Transparency Hub. |
| 11 | select 1 | B | **KEY-CORRECT** | Quote-grounding plus a pre-release human gate addresses both the grounding gap and the missing approval gate [D05-V20]. A is disclosure; C and D may help quality without restoring the gate. |
| 12 | select 1 | B | **KEY-CORRECT, rationale MAJOR-wrong** | B is the best answer. But the published reason C fails — "contradicted by Anthropic's own acknowledgment of occasional mismatches" — cites guidance that does not exist, and the Citations doc says citations "are guaranteed to contain valid pointers to the provided documents" [D05-V21]. A candidate who checks the source will conclude the course is unreliable. Apply C7. |

**Item-set observations.** 12 items, only 2 multiple-response (Items 4, 8) — thin against the brief's
"mix," and both multiple-response items are the two weakest. No item tests the failure-mode
diagnostics table (§5), the cross-tenant leakage pattern, or the MCP supply-chain scenario (§4.7),
all of which are richer exam territory than Item 8's OWASP recall. Consider replacing Item 8 with a
tenant-isolation or indirect-injection-via-MCP scenario.

---

## Volatility watchlist

| Claim | Status today (2026-09-24) | Re-check trigger |
|---|---|---|
| Covered Models = Fable 5.1, Mythos 5.1, Fable 5, Mythos 5 | Confirmed | Any new frontier-tier model launch. The Covered-Model set has grown with each Fable/Mythos release; re-read `api-and-data-retention#model-specific-data-retention-requirements`. |
| `inference_geo` values limited to `"us"` / `"global"`; workspace geo `"us"` only | Confirmed, and the doc labels both as "Current limitations" | Any EU-residency announcement. The doc's own "Current limitations" heading signals this is expected to change; an EU value would invalidate the chapter's flat "no EU pin" teaching and T5. |
| Vertex AI Assured Workloads = FedRAMP High + DoD IL2 | Rests on an April 2025 Anthropic blog that anticipates "future IL5 compatibility" | Any Google Cloud / Anthropic IL announcement, or an update to Anthropic's Public Sector FAQ. If Vertex reaches IL4/5, Item 4's option C flips and the item breaks. **Highest-risk item in the chapter.** |
| Claude for Government FedRAMP High; FedRAMP Marketplace shows Anthropic/"Claude" as "Not yet certified, Initial Implementation, 0 ATOs" | Both true simultaneously | Marketplace status change to Authorized, or a C4G scope change. Re-check `fedramp.gov/marketplace` for package FR2633053633. |
| "No separate FedRAMP audit per model; authorization is infrastructure-level" | Confirmed via Anthropic help center | Any change in C4G's serving infrastructure (currently gated on Vertex availability). |
| EU AI Act high-risk dates: 2 Dec 2027 / 2 Aug 2028 | Confirmed; AI Omnibus in force 27 July 2026 | Any further omnibus or delay instrument. These dates have already moved once from the original 2 Aug 2026 / 2 Aug 2027. Re-check the EC AI Act page and EUR-Lex before any engagement relies on them. |
| Commission tier naming "transparency risk" | Current | EC page revision. The informal "limited risk" label persists in secondary coverage; re-verify naming rather than copying blogs. |
| OWASP Top 10 for LLM Applications = 2025 edition | Current; no 2026 edition | Any new OWASP GenAI release. Entry names and ordering changed materially between 2023 and 2025 (e.g. Insecure → Improper Output Handling); re-verify names verbatim, do not paraphrase from memory. |
| Anthropic certifications list (SOC 2 I & II, ISO 27001:2022, ISO/IEC 42001:2023, HIPAA-ready) | Page last updated 2026-03-16 | Page-update date change, or any FedRAMP entry appearing on it. |
| "Google Cloud's Agent Platform" (Anthropic's current name for the Google surface) vs. the chapter's "Google Vertex AI" | Anthropic's retention doc now says "Google Cloud's Agent Platform"; the FedRAMP FAQ still says "Google Vertex with Assured Workloads" | Product renaming in progress. Expect the chapter's "Vertex AI" naming to age; re-check both Anthropic pages. |
| `inference_geo: "us"` at 1.1x pricing | Confirmed | Pricing page revision. |
| HIPAA self-serve enablement in Console; permanent once enabled | Confirmed | Console flow change. |

---

## Sources consulted

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|
| D05-V01 | API and data retention | https://platform.claude.com/docs/en/manage-claude/api-and-data-retention | Anthropic | anthropic-docs | 2026-09-24 | primary | Covered Models list; "not retained by default"; ZDR scope and exclusions; 30-day workspace override; 2-year flagged retention; HIPAA readiness scope/exclusions; `400` enforcement + client-side-tool carve-out; PHI-not-in-JSON-schema rule; org-level permanence; processor split incl. Microsoft Foundry |
| D05-V02 | Data residency | https://platform.claude.com/docs/en/manage-claude/data-residency | Anthropic | anthropic-docs | 2026-09-24 | primary | `inference_geo` name, values `"us"`/`"global"`, no EU pin, top-level parameter, model availability (4.6+), Bedrock/Vertex/Foundry non-applicability, `allowed_inference_geos`/`default_inference_geo`, workspace geo `"us"`-only, 1.1x pricing |
| D05-V03 | Business Associate Agreements (BAA) for Commercial Customers | https://privacy.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers | Anthropic (Privacy Center) | anthropic-docs | 2026-09-24 | primary | BAA-covered surfaces (Claude Enterprise features; 1P Messages/Token Counting/Models/Org Mgmt/Compliance APIs); exclusions (Batch, Files, Skills, Code Execution, Computer Use, Web Fetch; consumer; Console; Cowork; beta); Covered-Model/ZDR statement |
| D05-V04 | What Certifications has Anthropic obtained? | https://privacy.claude.com/en/articles/10015870-what-certifications-has-anthropic-obtained | Anthropic (Privacy Center) | anthropic-docs | 2026-09-24 | primary | SOC 2 Type I & II, ISO 27001:2022, ISO/IEC 42001:2023, HIPAA-ready (BAA available); no FedRAMP listed; last updated 2026-03-16 |
| D05-V05 | Claude in Amazon Bedrock: Approved for Use in FedRAMP High and DoD IL4/5 Workloads | https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high | Anthropic | anthropic-blog | 2026-09-24 | primary | Bedrock GovCloud (US) FedRAMP High + DoD IL4/5; named model roster (Claude 3.5 Sonnet v1, Claude 3 Haiku); pub. 2025-06-11 |
| D05-V06 | Claude on Google Cloud's Vertex AI: FedRAMP High and IL2 Authorized | https://claude.com/blog/claude-on-google-cloud-fedramp-high | Anthropic | anthropic-blog | 2026-09-24 | primary | Vertex AI + Assured Workloads = FedRAMP High and IL-2; "lays groundwork toward future IL5 compatibility"; pub. 2025-04-02 |
| D05-V07 | Claude Opus 4.8 is now available in AWS GovCloud (US) | https://aws.amazon.com/about-aws/whats-new/2026/05/claude-opus-4.8-aws-govcloud-us/ | AWS | vendor-docs | 2026-09-24 | primary | Availability only — **no FedRAMP or DoD IL statement on the page**; posted 2026-06-30 (not May 2026) |
| D05-V08 | Public Sector FAQs | https://support.claude.com/en/articles/13756069-public-sector-faqs | Anthropic (Help Center) | anthropic-docs | 2026-09-24 | primary | "Claude for Government is Anthropic's FedRAMP-High authorized product"; "CUI and FIPS 199 High Impact data are authorized in Claude for Government"; "ITAR data can only be processed in Claude via AWS Bedrock, which is IL5 accredited"; "Claude is available in the AWS Secret region (IL6) via Amazon Bedrock"; C4G + Bedrock GovCloud + Vertex Assured Workloads "are all FedRAMP-High" |
| D05-V09 | Model availability in Claude for Government | https://support.claude.com/en/articles/14503794-model-availability-in-claude-for-government | Anthropic (Help Center) | anthropic-docs | 2026-09-24 | primary | "There is no separate FedRAMP audit per model… authorization is infrastructure-level, not per-model"; new models inherit authorization; same-day-to-two-day availability |
| D05-V10 | Claude — FedRAMP Marketplace listing (package FR2633053633) | https://www.fedramp.gov/marketplace/products/FR2633053633/ | FedRAMP PMO | standard/regulation | 2026-09-24 | primary | CSP Anthropic, product "Claude": status "Not yet certified", phase "Initial Implementation", 0 ATOs/ATUs |
| D05-V11 | Art. 22 GDPR — Automated individual decision-making, including profiling | https://gdpr-info.eu/art-22-gdpr/ | GDPR-info (regulation text) | standard/regulation | 2026-09-24 | secondary | Art. 22(1) right; 22(2)(a)–(c) three bases; 22(3) safeguards limited to (a) and (c); 22(4) special categories |
| D05-V12 | Art. 5 GDPR — Principles relating to processing of personal data | https://gdpr-info.eu/art-5-gdpr/ | GDPR-info (regulation text) | standard/regulation | 2026-09-24 | secondary | 5(1)(a)–(f) principles incl. purpose limitation, data minimisation, storage limitation; 5(2) accountability |
| D05-V13 | AI Act — Regulatory framework for AI | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | European Commission | standard/regulation | 2026-09-24 | primary | Four tiers named "Unacceptable risk / High risk / Transparency risk / Minimal or no risk"; all application dates; AI Omnibus proposed 19 Nov 2025, political agreement 7 May 2026, in force 27 July 2026 |
| D05-V14 | Implementation Timeline | https://artificialintelligenceact.eu/implementation-timeline/ | Future of Life Institute (AI Act mirror) | standard/regulation | 2026-09-24 | secondary | Entry into force 1 Aug 2024; 2 Feb 2025 prohibitions; 2 Aug 2025 GPAI; 2 Aug 2026 Art. 50 (2 Dec 2026 for synthetic media); 2 Dec 2027 Annex III; 2 Aug 2028 Annex I |
| D05-V15 | AI Omnibus enters into force (and related Council/Parliament records) | https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force | European Commission | standard/regulation | 2026-09-24 | primary | Confirms the AI Omnibus entered into force 27 July 2026 and the extended high-risk timelines |
| D05-V16 | AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | NIST | standard/regulation | 2026-09-24 | primary | Core functions Govern/Map/Measure/Manage; "intended for voluntary use"; AI RMF 1.0, 2023-01-26 |
| D05-V17 | OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/llm-top-10/ | OWASP GenAI Security Project | standard/regulation | 2026-09-24 | primary | Verbatim LLM01–LLM10:2025 entry IDs and titles; 2025 is the current edition (retires the dossier's "could not be primary-verified" caveat) |
| D05-V18 | Usage Policy | https://www.anthropic.com/legal/aup | Anthropic | anthropic-docs | 2026-09-24 | primary | High-Risk Use Case Requirements: seven domains; "a qualified professional in that field must review the content or decision prior to dissemination or finalization"; AI-use disclosure at session start; consumer-chatbot AI disclosure |
| D05-V19 | Mitigate jailbreaks and prompt injections | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | Anthropic | anthropic-docs | 2026-09-24 | primary | Two threat models; harmlessness screens with Claude Haiku 4.5 + structured outputs; input validation; repeat-offender throttling; `tool_result`-only isolation; provenance labeling; system-prompt untrusted-content policy; JSON encoding; don't-instruct-in-tool-results; least privilege; tool-output screening; red-teaming; chain safeguards |
| D05-V20 | Reduce hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Anthropic | anthropic-docs | 2026-09-24 | primary | Allow "I don't know"; >20k-token quote extraction; verify-with-citations + retraction; chain-of-thought verification; best-of-N; iterative refinement; external-knowledge restriction; "significantly reduce… don't eliminate them entirely" |
| D05-V21 | Citations | https://platform.claude.com/docs/en/build-with-claude/citations | Anthropic | anthropic-docs | 2026-09-24 | primary | "citations are guaranteed to contain valid pointers to the provided documents"; **no** statement anywhere about citation/quote mismatches or inaccuracy; ZDR note excluding Covered Models |
| D05-V22 | Introducing Citations on the Anthropic API | https://claude.com/blog/introducing-citations-api | Anthropic | anthropic-blog | 2026-09-24 | primary | "increasing recall accuracy by up to 15%"; customer "reduced source hallucinations and formatting issues from 10% to 0%"; no mismatch acknowledgment |
| D05-V23 | Measuring political even-handedness | https://www.anthropic.com/news/political-even-handedness | Anthropic | anthropic-blog | 2026-09-24 | primary | "1,350 pairs of prompts across 9 task types and 150 topics"; Claude Sonnet 4.5 as automated grader; three scored dimensions; cross-grader validation |
| D05-V24 | Guidance Regarding Methods for De-identification of PHI | https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html (direct fetch 403; content confirmed via hhs.gov search index and https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/understanding/coveredentities/De-identification/hhs_deid_guidance.pdf) | HHS Office for Civil Rights | standard/regulation | 2026-09-24 | primary | Expert Determination §164.514(b)(1) and Safe Harbor §164.514(b)(2) as the two Privacy Rule methods |
| D05-V25 | Minimum Necessary Requirement | https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/understanding/coveredentities/minimumnecessary.pdf (index page 403) | HHS Office for Civil Rights | standard/regulation | 2026-09-24 | primary | 45 CFR 164.502(b), 164.514(d): reasonable efforts to limit PHI to the minimum necessary; treatment and individual-authorization exceptions |
| D05-V26 | HIPAA Eligible Services Reference | https://aws.amazon.com/compliance/hipaa-eligible-services-reference/ | AWS | vendor-docs | 2026-09-24 | primary | Amazon Bedrock is HIPAA-eligible; AWS BAA required before processing PHI |
| D05-V27 | HIPAA Compliance on Google Cloud | https://cloud.google.com/security/compliance/hipaa | Google Cloud | vendor-docs | 2026-09-24 | primary | Google will enter BAAs; Covered Products list does **not** name "Vertex AI" / "Agent Platform"; instruction not to use non-covered products with PHI |
| D05-V28 | Regulation (EU) 2024/1689 (AI Act), consolidated text | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | EUR-Lex / EU | standard/regulation | 2026-09-24 | primary | Regulation number and title; Art. 14 "Human oversight" |
| D05-V29 | AI Act Article 12 — Record-Keeping | https://artificialintelligenceact.eu/article/12/ | Future of Life Institute (AI Act mirror) | standard/regulation | 2026-09-24 | secondary | Art. 12 "Record-Keeping" para. 1 (automatic logging over system lifetime); Art. 14 "Human Oversight"; Art. 50 "Transparency Obligations for Providers and Deployers of Certain AI Systems" — establishes logging and human oversight as distinct obligations |
| D05-V30 | `claude-api` skill bundle (`shared/models.md`, `shared/platform-availability.md`, `shared/model-migration.md`, `shared/error-codes.md`) | local skill bundle, cached 2026-06-24 | Anthropic (via Claude Code skill bundle) | anthropic-docs | 2026-09-24 | primary | Full active model catalog and exact model IDs; Mythos 5.1 / Mythos 5 as Project Glasswing-only; Covered-Model 30-day retention and `400` behavior; `inference_geo` platform availability matrix and Managed Agents nesting |
| D05-V31 | Anthropic Trust Center | https://trust.anthropic.com/ | Anthropic | anthropic-docs | 2026-09-24 | primary | Attempted; page is JS-rendered and yielded no extractable body text (same outcome the researcher reported for D05-S01). No claim rests on it. |
| D05-V32 | FedRAMP baselines and DoD Cloud Computing SRG Impact Levels | https://www.fedramp.gov/rev5/baselines/ and https://iase.disa.mil/cloud_security/cloudsrg/Pages/ImpactLevels.aspx (via fedramp.gov / public.cyber.mil / dodcio.defense.gov search index) | FedRAMP PMO / DISA / DoD CIO | standard/regulation | 2026-09-24 | primary | FedRAMP High = "the government's most sensitive, unclassified data"; DoD ILs 2/4/5/6 are a separate DoD construct; IL4 for DoD/government communities; IL5 for unclassified NSS data per CNSSP 32 — establishes that CUI does not require DoD IL4/5 for a civilian agency |

---

## Findings list (severity-ordered)

- **[BLOCKER]** §4 Scenario 3 (whole scenario), §2.5 FedRAMP bullet, §7 FedRAMP heuristic, §8 Item 4
  rationale — "CUI requires FedRAMP High + IL4/5" and "the 1P Anthropic API is not a
  FedRAMP-authorized boundary." Contradicted by Anthropic's Public Sector FAQ and by the
  FedRAMP/DoD-SRG distinction. Fix: C1, C2, C3, C4.
- **[BLOCKER]** §2.6 and §8 Item 12 rationale — fabricated attribution ("Anthropic's own docs
  acknowledge occasional citation/quote mismatches"). Fix: C6, C7.
- **[BLOCKER]** §4 Scenario 1 — false HIPAA/ZDR coupling; contradicted verbatim by Anthropic. Fix: C5.
- **[MAJOR]** §3 T5 Vertex HIPAA cell — uncited PHI-routing claim not supported by Google's Covered
  Products list. Fix: C12(i).
- **[MAJOR]** §10 `[UNVERIFIED]` list — carries a contradicted premise (per-model FedRAMP
  authorization) and a now-verified item (AI Omnibus dates). Fix: C11.
- **[MAJOR]** §2.3 vs §2.5 — OWASP category named "Insecure output handling" (2023 name) in one
  place and "improper output handling" (2025 name) in another. Fix: C8.
- **[MAJOR]** §2.1 vs T1 — the control hierarchy's ordering contradicts the chapter's own
  bypass-resistance analysis. Fix: C15.
- **[MAJOR]** §8 Item 6 rationale — dismisses a mitigation Anthropic explicitly recommends. Fix in
  the Answer-key audit row for Item 6.
- **[MAJOR]** §8 Item 8 — recall trivia with two invented distractors; below the guide's cognitive
  level. Rebuild as a classification scenario.
- **[MAJOR]** §2.5 EU AI Act — "limited-risk tier" is not the Commission's current tier name. Fix: C9.
- **[MINOR]** §2.2 EU AI Act logging/oversight claim cited to the EC overview page, which does not
  say it; re-cite to Regulation (EU) 2024/1689 Arts. 12 and 14.
- **[MINOR]** §2.5 GDPR — Microsoft Foundry omitted from the Anthropic-as-processor list. Fix: C13.
- **[MINOR]** §2.5 GDPR Art. 22 — Art. 22(3) safeguards attach only to bases (a) and (c). Fix: C14.
- **[MINOR]** §2.5 HIPAA — `400` enforcement stated as absolute; client-side-tool carve-out omitted.
  Fix: C16.
- **[MINOR]** §3 T5 — no HIPAA-availability row for Claude Platform on AWS / Foundry (both No), and
  no `inference_geo` 1.1x cost axis. Fix: C12(ii), C17.
- **[MINOR]** §2.6 / Item 10 — bias-eval methodology cited to the Transparency Hub rather than the
  political-even-handedness publication. Fix: re-cite to D05-V23.
- **[MINOR]** §8 Item 5 stem — "routine model version upgrade with no code changes" is artificial on
  a platform where model IDs are explicitly pinned; rephrase the premise.
- **[MINOR]** §8 Item 9 rationale — D fails on Chapter V transfer rules as well as Art. 3 scope; and
  the log-redaction practice is cited to D05-S04, which does not prescribe it.
- **[NIT]** §2.4 / T4 — the five-tier HITL ladder is a practitioner synthesis with one secondary
  source; say so rather than letting it read as established doctrine.
- **[NIT]** Chapter-wide — "Google Vertex AI" naming will age; Anthropic's retention documentation
  now says "Google Cloud's Agent Platform."
- **[NIT]** Draft is ~4,100 words against a 3,500–6,000 target for a 14% domain — acceptable, and the
  corrections above add substance rather than padding.
