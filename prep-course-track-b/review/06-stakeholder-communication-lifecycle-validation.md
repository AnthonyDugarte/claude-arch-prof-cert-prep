# Domain 6 Validation — Stakeholder Communication & Lifecycle Management

VERDICT: SHIP-WITH-FIXES

Top 3 must-fix items:
1. **[MAJOR]** The draft repeatedly bracket-cites the Google SRE book [D06-S13] for the claim that "accuracy" for a probabilistic system "must become an SLI computed from a disclosed eval set" (concept definition, §2; trade-off table §3.2 row "Quality SLO with error budget"; scenario 4.2's recommended answer). Direct verification of `sre.google/sre-book/service-level-objectives/` confirms the SLI/SLO/SLA/error-budget *definitions* are accurate, but the chapter itself **does not discuss LLM/eval-based quality SLIs at all** — that mapping is the course authors' own architectural synthesis. As written, a candidate cannot tell where the SRE book's documented content ends and the chapter's extension begins. Reframe every eval-SLI instance as an explicit adaptation ("this course applies SRE's error-budget mechanism to a quality SLI — the SRE book itself does not define this").
2. **[MINOR, dossier]** The dossier (Objective 3, and the Objective 4 gate-checklist table) says the Cowork guide prescribes "a pre-scale security review." The primary source (PDF, p.11 and p.14) places the security review at the *start* of Month 1 ("Evaluate" — before the pilot even begins), not specifically gated before the Scale phase (months 4-6). This did not propagate into the draft chapter, but should be corrected in the dossier before any later editor pulls from it.
3. **[MINOR, dossier]** The dossier presents `"structured disagreement before commitment"` in quotation marks as if it were Gergely Orosz's own words from `blog.pragmaticengineer.com/rfcs-and-design-docs/` [D06-S24]. Direct fetch of that post found no such phrase — it is the dossier author's paraphrase dressed as a quotation. The draft itself avoids this (it paraphrases without quote marks), so no fix is required there, but the dossier's citation should be corrected for hygiene.

No cited Anthropic (or other) publication was found to be non-existent. All five highest-risk Anthropic titles exist, are published by Anthropic/Claude, and contain the specific frameworks attributed to them (see audit below) — this is the single most important finding: **the publication-fabrication risk this review was built to catch did not materialize.**

---

## Publication existence audit

| Title | Claimed URL | Exists? | Contains attributed framework? | Evidence |
|---|---|---|---|---|
| Building Effective Agents | anthropic.com/engineering/building-effective-agents | Yes (Anthropic, Dec 2024) | Yes — "start simple" default-to-non-agentic principle, explicit cost/latency trade-off language, sandboxed-testing recommendation all present | Fetched directly; found "optimizing single LLM calls...is usually enough," "higher costs, and the potential for compounding errors," "extensive testing in sandboxed environments" |
| Demystifying evals for AI agents | anthropic.com/engineering/demystifying-evals-for-ai-agents | Yes (Anthropic, Jan 2026) | Yes — 20-50 task starter set, bug-tracker/support-queue sourcing, dedicated-evals-team + domain-experts ownership split, "living artifact...as routine as maintaining unit tests" all verbatim-confirmed | Fetched directly; exact quotes matched dossier/draft claims |
| Agentic Misalignment: How LLMs could be insider threats | anthropic.com/research/agentic-misalignment | Yes (Anthropic Research, June 2025) | Partially — it IS primarily a stress-test research report on blackmail/insider-threat behaviors, not a design guide. The "human approval for irreversible-consequence actions" and "information-access minimization" recommendations do appear, but only in a brief conclusion, framed as precautionary, not as the paper's central thesis. The chapter cites it correctly (only for the reversibility/access-minimization point), so this is not a misattribution, but note that the paper's overall character (behavioral stress-test) is not what a reader would infer from the chapter's framing alone | Fetched directly; confirmed both the research framing and the conclusion-section recommendations |
| Deploying Claude across your organization (Claude Cowork enterprise guide) | claude.com/blog/... + PDF | Yes (Anthropic/Claude, April 29, 2026) | Yes, and precisely — read full PDF text directly (pp. 1-20). Confirmed verbatim: five-level maturity ladder (0 Chat, 1 Build, 2 Skill, 3 Bundle/Schedule, 4 Department plugin); Evaluate=Month 1/Champions reach Level 1, Pilot=Months 2-3/Champions reach Levels 2-3, Scale=Months 4-6/Department reaches Level 4; "2-3 champion teams"; "Track how many champion-authored skills exist at the end of the pilot; it's the leading indicator for the scale phase" (near-verbatim match). One imprecision: the security review is placed pre-pilot (Month 1), not specifically "pre-scale" — see Correction #2 | PDF fetched via alternate CDN URL and read directly with the Read tool (blog page itself 403's/paraphrases only) |
| The AI-Native SDLC Playbook | claude.com/blog/the-ai-native-sdlc-playbook | Yes (Anthropic/Claude, Aug 21, 2026) | Yes — Plan/Design/Build/Test/Deploy/Maintain confirmed; "Evals are the AI-native equivalent of stage-gate QA" is a verbatim quote; named roles (product owner, engineer, code owner, release manager, service owner) confirmed; "a hook enforces the production gate" / "a hook blocks the release until a named release manager authorizes it" confirms the hook-as-technical-control claim exactly | Fetched directly, quotes matched |

---

## Claim verification table

| Claim | Location | Status | Source ID | Note/correct value |
|---|---|---|---|---|
| "Start simple" / default-to-non-agentic; agentic cost-latency trade-off; sandbox testing | Dossier Obj.1 | CONFIRMED | D06-V01 | Verbatim-adjacent quotes found |
| Eval set 20-50 tasks from real failures/support queue; eval-team + domain-expert ownership; living artifact | Dossier Obj.1/4/5; Draft Item 8, §2 "Eval gate" | CONFIRMED | D06-V02 | Exact match |
| Human approval required for irreversible-consequence actions; info-access minimization | Dossier Obj.1; Draft §2, §3.4, scenarios 4.1/4.4, Item 3/5/9 | CONFIRMED | D06-V03 | Confirmed, correctly scoped to the paper's conclusion section only |
| Claude Cowork: 5-level ladder (chat→build→skill→schedule→department plugin) | Dossier Obj.1/5 (not asserted by name in draft body) | CONFIRMED | D06-V04, D06-V05 | Exact structural match |
| Cowork pilot: Month 1 / Months 2-3 / Months 4-6 phases with named targets | Dossier Obj.3/5 (not asserted by name in draft body) | CONFIRMED | D06-V05 | Exact match to PDF table (p.14) |
| "Champion-authored reusable skills" as leading indicator | Dossier Obj.3 | CONFIRMED | D06-V05 | Near-verbatim: "the leading indicator for the scale phase" |
| "Pre-scale security review" | Dossier Obj.3, Obj.4 gate table | CONTRADICTED (imprecise) | D06-V05 | Guide places the review pre-pilot (Month 1), not specifically pre-Scale. Correct to "pre-pilot security review" |
| AI-Native SDLC: Plan→Design→Build→Test→Deploy→Maintain; eval suite = "stage-gate QA"; hook-enforced release-manager gate | Dossier Obj.4/5; Draft §2 ("Eval gate"), §3.6, scenario 4.6, Item 4 | CONFIRMED | D06-V06 | Verbatim quotes matched |
| SLI/SLO/SLA definitions; "no explicit consequence ⇒ SLO not SLA"; avoid 100% targets; error budget gates release pace | Draft §2 "SLI/SLO/SLA/error budget", §3.2 | CONFIRMED | D06-V07 | Definitions match Google SRE book verbatim |
| "Quality SLI derived from a disclosed eval set" attributed via [D06-S13] bracket to the same paragraph as the SRE definitions | Draft §2, §3.2 row, scenario 4.2 | NOT-FOUND (in the cited source) | D06-V07 | SRE book chapter does not discuss LLM/eval SLIs. This is the chapter's own synthesis — see Attribution Hygiene and Correction #1 |
| ADR fields (Title, Status, Context, Decision, Consequences); superseded-not-edited | Draft §2, §3.1, Item 6 | CONFIRMED | D06-V08 | Verbatim match, including the "keep the old one around, but mark it as superseded" rationale |
| ADR template variants (Nygard, Y-statement, MADR) exist and are community-convergent | Draft §2 (adr.github.io cite) | CONFIRMED | D06-V09 | Site references all three |
| C4 model: system context / container / component / code | Draft §2, §3.1, Item 7 | CONFIRMED | D06-V10 | Exact terminology match |
| arc42: 12-section template | Draft §2 | CONFIRMED (paraphrased) | D06-V11 | Draft's shortened labels ("goals," "quality," "risks") map 1:1 onto the official names (Introduction & Goals, Quality Requirements, Risks & Technical Debt); substance correct, wording is not verbatim — NIT only |
| ATAM utility-tree method; SEI/Kazman-Klein-Clements origin | Draft §2 (via QAW lineage cite) | CONFIRMED | D06-V12 | Confirmed |
| AWS Well-Architected: pillar trade-offs are inevitable and must be documented; security/operational excellence generally not traded away | Dossier Obj.2 (not asserted by name in draft body) | CONFIRMED | D06-V13 | Verbatim: "Security and operational excellence are generally not traded-off against the other pillars." Note: current framework has 6 pillars (added Sustainability); irrelevant to the claims actually made |
| Jobs to Be Done: stated request vs. underlying job; Christensen/Moesta | Draft §2, §3.1(4.1), Item n/a | CONFIRMED | D06-V14 | Distinction confirmed with sourced examples; page itself doesn't name authors, but public attribution to Christensen/Moesta is standard and uncontested |
| MoSCoW: Dai Clegg, DSDM origin, 1994 | Draft §2, §3.3 | CONFIRMED | D06-V16 | Exact match |
| RICE (Reach×Impact×Confidence/Effort); value-vs-feasibility 2x2 | Draft §3.3 | CONFIRMED | D06-V17 | Formula and framing confirmed via secondary corroboration (direct Atlassian page returned nav-only content) |
| RACI origin "genuinely disputed" | Dossier "Contradictions" section (draft makes no origin claim) | CONFIRMED (as "undocumented," not necessarily "disputed") | D06-V15 | Wikipedia gives no origin info at all — consistent with dossier's cautious framing; draft correctly makes no origin claim |
| Design Docs at Google: context/goals-non-goals/design/alternatives-considered/cross-cutting concerns; author Malte Ubl | Draft §2, §3.1 | CONFIRMED | D06-V18 | Exact section match |
| RFC = "structured disagreement before commitment" (quoted) | Dossier Obj.2 (quoted); Draft §2/§3.1 (paraphrased, unquoted) | CONTRADICTED (dossier only) | D06-V19 | Phrase not found in source; it's the dossier's own synthesis mis-marked as a quotation. Draft's unquoted paraphrase ("circulated to solicit disagreement") is acceptable |
| Mini-QAW: Michael Keeling, ATAM-derived, "Design It!" | Draft §2 | CONFIRMED | D06-V20 | Confirmed via Keeling's book and IEEE Software column |
| Runbook: action-oriented, tacit-knowledge transfer | Draft §2, §3.1, Item 4 | CONFIRMED | D06-V21 | Confirmed |
| Google SRE production-readiness-review / launch-checklist practice | Dossier Obj.2/4 (not cited by ID in draft body) | CONFIRMED (minor nuance) | D06-V22, D06-V23 | Launch checklist confirms dependency/failure-mode/capacity review content; the "evolving engagement model" page frames PRR as occurring at SRE-team-onboarding time rather than strictly "pre-launch," a minor nuance not material to any draft claim |
| Pilot-failure percentages (e.g. "88% of pilots fail") | Dossier flags as low-trust/UNVERIFIED; **not used anywhere in the draft** | CONFIRMED absent from draft | D06-S25 (dossier's own source) | Correctly excluded from graded content — verified via full-text grep of the draft for "%" (see below) |
| All percentages actually appearing in the draft (99%, 97%, 95%, 92%, 99.9%, 100%, "9 of 63," "14%") | Draft (multiple) | CONFIRMED as hypothetical/exam-mechanics only | — | Every instance is either (a) a hypothetical contract/SLA number inside a worked scenario or practice item, explicitly framed as a stakeholder's *ask* to be countered, or (b) the exam's own 14%-weight/9-of-63-item arithmetic (14% × 63 ≈ 8.8, correctly rounded and hedged "approximately"). No unsourced real-world statistic is asserted as fact anywhere in the chapter |
| Exam mechanics (63 items, 120 min, cut score 720/100-1000, $175, 12-month validity, retake 14/30/90-day waiting periods up to 4x/12mo, free non-proctored renewal) | Guide §5, §9, §11, §14 vs. draft front matter | CONFIRMED | D06-S01 / exam guide (direct read) | Draft only restates "14% of the exam (approximately 9 of 63 scored items)" and the five objectives verbatim from the guide — no drift found |
| Five Domain-6 objectives, quoted in draft front matter | Draft lines 5-10 vs. guide §6 | CONFIRMED | D06-S01 | Word-for-word match to the guide |

---

## Corrections required

1. **Draft §2 "SLI / SLO / SLA / error budget [D06-S13]"** — split the citation. Replace:
   > "Cares because 'accuracy' for a probabilistic system must become an SLI computed from a disclosed eval set, not a promise."
   with:
   > "Cares because 'accuracy' for a probabilistic system must become an SLI computed from a disclosed eval set, not a promise — this is this course's application of the SRE error-budget mechanism to a quality metric; the SRE book itself defines SLI/SLO/SLA/error budget for infrastructure signals and does not discuss LLM evals."
   Apply the same qualifier to the §3.2 trade-off table row ("Quality SLO with error budget... [D06-S13]") and to scenario 4.2's recommended-answer citation.

2. **Dossier, Objective 3 ("Expectation management")** — replace "a pre-scale security review" with "a security review conducted at the start of the pilot (Month 1), before champion teams begin building" [D06-S05 / D06-V05, PDF p.11: "Before you pilot, run the security review"; p.14: Month 1 "Evaluate" actions include "Security review"].

3. **Dossier, Objective 2** — replace the quoted `"structured disagreement before commitment"` with either (a) an actual short excerpt from D06-S24, or (b) an unquoted paraphrase matching the draft's own (correct) approach: "an RFC solicits disagreement and alternatives before a decision is committed."

4. **NIT, draft §2 (C4/arc42 concept) and elsewhere** — arc42's official section names are "Introduction & Goals," "Building Block View," "Quality Requirements," "Risks & Technical Debt," etc. The draft's shortened labels ("goals," "building blocks," "quality," "risks") are substantively correct but not verbatim; optional to tighten for a candidate who might see the official names on the exam.

---

## Answer-key audit

| Item | Verdict | Reasoning |
|---|---|---|
| 1 | KEY-CORRECT | B is the only falsifiable promotion criterion; A is the demo-to-production trap the item is testing for; C (cost) and D (disclaimer/UX) don't address the actual question (readiness), confirmed consistent with D06-V02/V05 |
| 2 | KEY-CORRECT | C is the only disclosed, falsifiable commitment; A is unfalsifiable against arbitrary future documents; B abandons the negotiation; D ("zero hallucinations") is strictly worse than A, not a "stronger" commitment — rationale correctly identifies this |
| 3 | KEY-CORRECT | B (reversibility) is the only discovery answer that gates architecture per D06-V03's irreversibility-approval principle; A/C/D are cosmetic/operational and correctly dismissed |
| 4 | KEY-CORRECT | A (runbook) and C (RACI) are the only load-bearing operational artifacts per D06-V06/V21; B and D are historical/marketing artifacts with no operational function |
| 5 | KEY-CORRECT | C reframes on reversibility/error-budget consistent with D06-V03 and the Cowork ladder's "nobody needs to reach Level 4 in month 1" logic (D06-V05); A creates unmanaged liability, B/D forfeit negotiating leverage without addressing any low-risk subset |
| 6 | KEY-CORRECT | C matches Nygard's format and immutability rule exactly (D06-V08); A describes an RFC, B violates immutability, D confuses ADR log scope with a full architecture document |
| 7 | KEY-CORRECT | B is the only answer matching confirmed C4 (notation, 4 levels) vs. arc42 (12-section template) distinction (D06-V10/V11); A/C/D invent constraints neither framework states |
| 8 | KEY-CORRECT | C matches D06-V02's "20-50 simple tasks drawn from real failures" almost verbatim; A over-invests before knowing failure modes, B stalls indefinitely, D substitutes a weak proxy signal for task-level grading |
| 9 | KEY-CORRECT | A and B are the two reasons the chapter's own §3.4 discriminator names (capacity and reversibility/blast-radius); C and D are named in that same section as insufficient/wrong bases. Internally consistent with the chapter's own framework and with D06-V02/V03 |
| 10 | KEY-CORRECT | B is the only answer consistent with error-budget governance (a model-version change can shift the SLI a prior SLO was validated against) per D06-V06/V07; A wrongly assumes uniform improvement, C/D wait for harm/contract language instead of validating proactively |

No wrong or arguable keys found. All ten items independently re-solved to the keyed answer.

---

## Attribution hygiene

1. **[MAJOR]** *Eval-derived quality SLI attributed via the same bracket as Google SRE definitions.* See Correction #1. This is the pattern the task brief specifically warned about (item c) — a genuinely useful architectural synthesis (SRE error-budget mechanics + Anthropic eval-gate practice = "quality SLO") is presented with a citation format identical to the surrounding, actually-sourced SRE definitions, with no verbal marker distinguishing "documented by Google" from "this course's application." Fix: add an explicit "this is an adaptation, not a documented SRE-book practice" sentence at first use (§2) and keep the phrasing "SRE-style error-budget governance" (already used correctly in Item 10's rationale) everywhere else instead of a bare [D06-S13] bracket.
2. **[MINOR, dossier]** *"Pre-scale security review"* and *quoted "structured disagreement before commitment"* — both are dossier-level precision drift (see Corrections #2-3); neither reached the graded draft, but both should be fixed before an editor consolidates from the dossier.
3. **Good practice worth preserving:** the draft consistently declines to state real-world pilot-failure percentages (the "88% of pilots fail" style claim), correctly treating the dossier's own low-trust flag on D06-S25 as disqualifying for graded content — every percentage that does appear in the draft is either a worked-scenario hypothetical explicitly framed as a stakeholder's unfalsifiable ask, or the exam's own weight arithmetic. This is exactly the discipline the brief's §0 verification rule asks for and should not be diluted by an editor looking to "add color" with a real-world stat.
4. **Good practice worth preserving:** citations to Anthropic's Agentic Misalignment paper [D06-S04] are correctly scoped to only the paper's conclusion-section recommendation (human approval for irreversible actions), not its central research finding (insider-threat behavioral stress tests) — the chapter never overclaims what that paper is "about."
5. No instance of "Anthropic recommends X" or "the exam expects Y" phrasing was found anywhere in the draft or dossier; all exam-scope claims trace to the guide's actual blueprint text (confirmed word-for-word in the front matter).

---

## Sources consulted

| ID | Title | URL | Publisher/Author | Type | Accessed | Trust | Used for |
|----|-------|-----|------------------|------|----------|-------|----------|
| D06-V01 | Building Effective Agents | https://www.anthropic.com/engineering/building-effective-agents | Anthropic | anthropic-blog | 2026-09-24 | primary | Verified start-simple/cost-latency/sandbox claims |
| D06-V02 | Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Anthropic | anthropic-blog | 2026-09-24 | primary | Verified 20-50 task set, eval ownership, living-artifact claims |
| D06-V03 | Agentic Misalignment: How LLMs could be insider threats | https://www.anthropic.com/research/agentic-misalignment | Anthropic | anthropic-blog | 2026-09-24 | primary | Verified irreversible-action approval / info-minimization claims and paper's actual scope |
| D06-V04 | Deploying Claude across the enterprise with Claude Cowork (blog page) | https://claude.com/blog/new-guide-deploying-claude-across-the-enterprise-with-claude-cowork | Anthropic/Claude | anthropic-blog | 2026-09-24 | primary | Confirmed guide exists, publisher, top-level framing |
| D06-V05 | Deploying Claude Across Your Organization (Cowork guide, PDF) | https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69f24d3e09b921b92403774e_Claude-Deploying-Claude-Across-Your-Organization-04292026.pdf | Anthropic/Claude | anthropic-blog | 2026-09-24 | primary | Full-text verification of 5-level ladder, month 1/2-3/4-6 structure, champion-skill leading indicator, security-review timing |
| D06-V06 | The AI-Native SDLC Playbook | https://claude.com/blog/the-ai-native-sdlc-playbook | Anthropic/Claude | anthropic-blog | 2026-09-24 | primary | Verified 6-stage lifecycle, "stage-gate QA" quote, hook-enforced release-manager gate, named roles |
| D06-V07 | SRE Book — Service Level Objectives | https://sre.google/sre-book/service-level-objectives/ | Google SRE | vendor-docs | 2026-09-24 | primary | Verified SLI/SLO/SLA/error-budget definitions verbatim; confirmed absence of LLM/eval-SLI content |
| D06-V08 | Documenting Architecture Decisions | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | Michael Nygard | practitioner-blog | 2026-09-24 | secondary | Verified ADR fields and immutability/supersession rule |
| D06-V09 | Architectural Decision Records | https://adr.github.io/ | adr.github.io/MADR | practitioner-blog | 2026-09-24 | secondary | Verified template-variant claims |
| D06-V10 | The C4 model | https://c4model.com/ | Simon Brown | practitioner-blog | 2026-09-24 | secondary | Verified 4-level naming |
| D06-V11 | arc42 overview | https://arc42.org/overview/ | arc42 project | practitioner-blog | 2026-09-24 | secondary | Verified 12-section list |
| D06-V12 | Architecture Tradeoff Analysis Method | https://en.wikipedia.org/wiki/Architecture_tradeoff_analysis_method | SEI (Kazman, Klein, Clements) | academic | 2026-09-24 | secondary | Verified utility-tree method and origin |
| D06-V13 | AWS Well-Architected Framework — Definitions | https://docs.aws.amazon.com/wellarchitected/latest/framework/definitions.html | AWS | vendor-docs | 2026-09-24 | secondary | Verified pillar trade-off quote verbatim |
| D06-V14 | Jobs to Be Done Theory | https://www.christenseninstitute.org/theory/jobs-to-be-done/ | Christensen Institute | academic | 2026-09-24 | secondary | Verified stated-request-vs-job distinction |
| D06-V15 | Responsibility assignment matrix (RACI) | https://en.wikipedia.org/wiki/Responsibility_assignment_matrix | — | community | 2026-09-24 | secondary | Confirmed no documented origin (supports dossier's cautious framing) |
| D06-V16 | MoSCoW method | https://en.wikipedia.org/wiki/MoSCoW_method | community | community | 2026-09-24 | secondary | Verified Dai Clegg/DSDM origin |
| D06-V17 | RICE prioritization (Atlassian + secondary corroboration) | https://www.atlassian.com/agile/product-management/prioritization-framework | Atlassian | vendor-docs | 2026-09-24 | secondary | Verified RICE formula/framing (direct page returned nav-only; corroborated via search) |
| D06-V18 | Design Docs at Google | https://www.industrialempathy.com/posts/design-docs-at-google/ | Malte Ubl | practitioner-blog | 2026-09-24 | secondary | Verified design-doc section list |
| D06-V19 | RFCs and Design Docs | https://blog.pragmaticengineer.com/rfcs-and-design-docs/ | Gergely Orosz | practitioner-blog | 2026-09-24 | secondary | Checked for "structured disagreement" phrase — not found verbatim; flagged as dossier misquote |
| D06-V20 | Mini-Quality Attribute Workshop | https://www.neverletdown.net/p/mini-quality-attribute-workshop.html (+ search corroboration) | Michael Keeling | practitioner-blog | 2026-09-24 | secondary | Verified ATAM-derived attribution and "Design It!" origin |
| D06-V21 | What are runbooks | https://incident.io/blog/what-are-runbooks | incident.io | practitioner-blog | 2026-09-24 | secondary | Verified runbook definition |
| D06-V22 | SRE launch checklist | https://sre.google/sre-book/launch-checklist/ | Google SRE | vendor-docs | 2026-09-24 | secondary | Verified pre-launch review content (dependencies, failure modes, capacity) |
| D06-V23 | Evolving the SRE engagement model | https://sre.google/sre-book/evolving-sre-engagement-model/ | Google SRE | vendor-docs | 2026-09-24 | secondary | Verified PRR exists; noted post-launch/engagement-model framing nuance |
| D06-V24 | Enterprise Readiness: A CISO's Guide to Deploying Claude | https://www.anthropic.com/webinars/enterprise-readiness-a-cisos-guide-to-deploying-claude | Anthropic | anthropic-blog | 2026-09-24 | primary | Spot-checked existence/topic alignment (not cited for a specific graded claim in the draft) |
| D06-S01 | Claude Certified Architect – Professional Exam Guide, v1.0 | ../../claude-arch-professional-guide.md (local) | Anthropic | exam-guide | 2026-09-24 | primary | Verified all exam-mechanics facts and objective list verbatim (read directly, not re-listed as D06-V) |
