# Content Review — Domain 5: Governance, Safety & Risk Management

Reviewer: Content Reviewer (axes per AGENT-BRIEF §4). Files read: AGENT-BRIEF.md,
claude-arch-professional-guide.md, research/05-governance-safety-risk-dossier.md,
drafts/05-governance-safety-risk-draft.md.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. Objective 5 (ethical AI: bias, fairness, transparency) is the weakest-covered objective and the
   objective-coverage table (§9) papers over it — it credits Scenarios 2 and 5 to Objective 5, but
   neither scenario's decision turns on bias/fairness/transparency. Add one dedicated worked scenario
   whose recommended answer requires disparate-impact reasoning (not just an HITL/GDPR gate), a matching
   anti-pattern, and a failure-mode/diagnostics row, then correct the coverage table.
2. Three worked scenarios and two practice items give away the regulatory trigger in the stem instead of
   requiring the candidate to recognize it: Scenario 1 states "PHI throughout," Scenario 3 states
   "CUI-level," Scenario 2 states "a denial is legally significant," Item 2 states "containing PHI," Item
   4 states "requiring DoD Impact Level 4/5 authorization." This converts a judgment test into a
   keyword-match test. Rewrite stems to describe the data/effect functionally and let the candidate
   derive the classification.
3. At least three practice items substantially re-test the same industry-vertical-plus-lesson pairing as
   an existing worked scenario rather than applying the concept in a new context: Item 1 ≈ Scenario 4
   (tool removal, support agent), Item 3 ≈ Scenario 2 (EU lender, Art. 22), Item 11 ≈ Scenario 6 (legal
   contract review, quote-grounding + sign-off). This is closer to memorization of the chapter's own
   examples than transfer. Swap verticals/framing on these three items.
```

---

## Findings

### Blueprint coverage

- **[BLOCKER]** §9 Objective-coverage table, row "Address ethical AI considerations" — cites "§4 (Scenarios
  2, 5)" as evidence. Scenario 2 (loan underwriting) is decided entirely on GDPR Art. 22 / HITL grounds;
  Scenario 5 (insurance triage) is decided on reversibility-asymmetry grounds. Neither scenario's
  "recommended approach" or "why the plausible alternatives lose" section turns on bias, fairness, or
  transparency — disparate impact by protected class is never raised in either. This is a padded citation,
  exactly what AGENT-BRIEF's honesty requirement for this table is meant to catch. Required fix: remove
  Scenarios 2/5 from that row (or make the row honestly say "partial — HITL/legal-effect overlap only") and
  add a scenario that is actually decided on a fairness/disparate-impact axis, e.g., a credit-scoring or
  resume-screening tool where an aggregate accuracy number looks fine but a per-segment slice reveals a
  gap, and the candidate must choose "re-run a segmented eval and hold the launch" over "ship, aggregate
  metric passed."
- **[MAJOR]** §5 Failure modes & diagnostics table has no row for a bias/fairness failure signature (e.g.,
  "approval/denial rate diverges by protected-class proxy; aggregate accuracy unchanged" → likely cause:
  eval only measured aggregate accuracy, no segment slicing → first check: outcome metrics sliced by
  segment → fix: re-run segmented eval, treat as regression gate). §2.6 already states the underlying
  insight ("an aggregate accuracy number can hide a large per-segment gap") but it is never operationalized
  as a diagnosable symptom. Add the row — this table is supposed to double as a triage reference across all
  five objectives, and right now it only serves four.
- **[MAJOR]** §6 Anti-patterns has no named pattern for "aggregate-metric fairness" / "fairness-washing"
  (evaluating fairness once, in aggregate, and calling it done), even though §2.6 states the exact insight
  that would justify one. This is a one-line promotion of existing content, not new research — the editor
  should lift it into the anti-patterns table.
- **[MINOR]** §3 has seven trade-off tables (T1–T7), all guardrail/compliance-flavored. None addresses an
  ethical-AI-specific trade-off (e.g., "aggregate accuracy vs. per-segment fairness metrics as the
  regression gate" or "in-context bias mitigation vs. eval-gated launch review"). Not required to hit the
  4–6 minimum (7 already clears it), but given Objective 5's overall thinness, one more table here would
  do double duty.
- **[MINOR]** §2.7 "Governance mechanics" (AI review board, prompt/model version control, AI-specific
  incident response) is good, genuinely Domain-5-owned content, but it is not tied to any objective in the
  coverage table, has no trade-off, scenario, or practice item built on it, and risks reading as an
  appendix. Either tie it explicitly to Objective 1 (guardrails) in §9, or trim it if it's not pulling
  weight.

### Altitude

- No basic prompt/API teaching found; the chapter consistently operates at "which control, and why" rather
  than "what is a control." Good.
- **[MINOR]** §2.5's compliance primitives stay at the right altitude (architectural requirement +
  control), but Item 2 and Item 4 (below) drift toward compliance trivia by naming the classification
  outright in the stem — see the stem-giveaway finding under Practice items.

### Trade-off quality

- T1–T7 all have explicit axes and a stated "choose X when" discriminator; this is the chapter's strongest
  section. No false binaries found — every comparison table has 2–5 real options, not a strawman pair.
- **[MINOR]** T5, row "ZDR": both Bedrock and Vertex are marked "Platform-specific — verify per engagement"
  with no stated dependency (what actually determines ZDR availability on each platform — contract tier?
  data-processing addendum? region?). This is the one "it depends" in the trade-off set that doesn't say
  what it depends on. Either state the dependency or cut the row rather than leave a bare "verify."
- The control-strength ordering (§2.1) is not asserted as dogma — T1's table (bypass resistance, cost,
  best-for) gives the reasoning that makes it decidable in a novel scenario, satisfying the specific risk
  called out for this axis.

### Scenario realism

- **[MAJOR]** Scenario 1: "a hospital wants Claude to draft visit summaries from clinician dictation
  referencing patient history — **PHI throughout**." Stating "PHI throughout" removes the inferential step
  the exam is designed to test (recognizing that dictated patient history constitutes PHI). Fix: describe
  the data functionally ("dictation referencing diagnosis, treatment plan, and patient identifiers") and
  let the candidate classify it.
- **[MAJOR]** Scenario 3: "...answering benefits questions from **CUI-level** internal policy documents."
  Same defect — states the classification instead of describing data a candidate must classify as CUI.
- **[MAJOR]** Scenario 2: "...EU applicants in scope — **a denial is legally significant**." "Legally
  significant" is the Art. 22 term of art; stating it directly hands the candidate the trigger instead of
  requiring them to recognize a loan denial as a legally/similarly-significant effect.
- **[MINOR]** Scenario 5 is comparatively better — it states facts ("false denials harm real people")
  without naming the legal term, forcing more inference. Use this scenario's phrasing style as the fix
  template for 1/2/3 above.
- Scenarios 4, 6, and 7 are decidable via constraints rather than giveaways, and their "why the plausible
  alternatives lose" sections do real analytical work (e.g., Scenario 6 distinguishes "used purely for
  associate triage with full independent review always following" as the condition that would relax
  grounding strictness — a genuine discriminator, not a restatement).
- **[MAJOR]** Scenario 4 (retail support agent: read tickets, draft replies, issue refunds, delete
  accounts) reuses the exam guide's own Section 8 Sample 1 fact pattern almost verbatim (same four
  capabilities, same "only the first two are needed" framing). The brief permits discussing guide samples
  as a style reference (AGENT-BRIEF §5.2), but this goes further and re-presents it as an original worked
  scenario, then reuses the identical concept again in Item 1 with cosmetic renaming (refund/delete →
  credit-issuing). Combined with §2.1's citation of the same sample and the "remove capability" heuristic
  in §7, this idea appears five times. Recommend cutting Scenario 4 as a distinct worked scenario (keep the
  citation in §2.1 as the style reference) and replacing it with a scenario that earns Domain 5 credit the
  current set doesn't yet cover (ethical AI — see Blueprint coverage finding above).

### Practice-item quality (see also dedicated item-by-item section below)

- **[MAJOR]** Systematic answer-length tell: in Items 2, 6, 9, and 11 the correct option is the longest,
  most multi-clause option on the list, while distractors are short single-clauses. Example, Item 2: correct
  B — "A signed BAA, org-level HIPAA readiness enabled, and use restricted to eligible features." — vs. A/C/D,
  each a single short clause. A test-savvy candidate can select the most detailed-sounding option without
  domain knowledge. Fix: pad distractors to comparable length/specificity or compress the correct answer.
- **[MINOR]** Item 5, distractor A ("Nothing — model behavior is inherently unpredictable") is a strawman,
  not attractive to a plausibly-reasoning candidate — weakens the item's discriminating power. Replace with
  something a reasonable-but-wrong architect might pick, e.g., "Wait for user complaints to reach a
  threshold before investigating."
- **[MINOR]** Item 3, distractor D ("FedRAMP authorization boundary violation") is similarly a throwaway —
  nothing in a commercial EU-lender scenario suggests a federal-cloud concept. Replace with a more adjacent
  wrong answer, e.g., a GDPR Art. 5 minimization angle to force discrimination between two GDPR articles
  rather than between GDPR and an unrelated framework.
- **[MINOR]** Item 4 and Item 8 each hinge on a fact that is plausibly volatile before a candidate sits the
  exam: Item 4 on "Vertex AI Assured Workloads currently tops out at IL2" (a FedRAMP ceiling that could be
  raised) and Item 8 on the named "OWASP Top 10 for LLM Applications (2025)" list (subject to revision).
  The dossier itself flags FedRAMP-authorization currency as something to re-verify per engagement. Given
  the exam's own hard rule against durable-sounding items resting on moving facts, reduce Item 4's
  precision (test the architectural pattern — "boundary is platform-specific, not vendor-wide" — rather
  than the exact IL number) or accept the risk explicitly and flag it for the validator.

### Structure and style compliance

- All 11 required sections present, in the required order, with front matter, exam-relevance framing,
  core concepts, trade-offs, scenarios, failure modes, anti-patterns, exam-day heuristics, practice items,
  objective-coverage table, and sources.
- **[MINOR]** Word count is 5,631 words, above the 4,000–5,500 target band for this chapter (roughly 130
  words over). Trimming the redundant Scenario 4 (see above) largely closes this gap while also freeing
  room for the missing ethical-AI scenario.
- No emoji, no marketing language, no filler found. Tables are used consistently for comparisons and
  triage content, matching the required "skimmable" style.

### Pedagogical sequencing and redundancy

- **[MAJOR]** The "remove the capability beats log/confirm/monitor" point appears in §2.1 (concept), T1
  (trade-off), T2 (example row), Scenario 4, §6 ("Kitchen-sink tool agent"), §7 (first heuristic), and Item
  1 — seven touchpoints for one idea in a 14%-weight, five-objective chapter. Some reinforcement is by
  design (AGENT-BRIEF's own example heuristic is a restatement of a concept), but seven is excessive
  relative to Objective 5 getting effectively zero dedicated worked-example touchpoints. Trim at least two
  of these (recommend cutting Scenario 4 as stated above, and considering whether both the T1 row and the
  T2 row need the identical "remove the delete-account tool" example).
- **[MAJOR]** Item 1 ≈ Scenario 4 (support-agent tool removal), Item 3 ≈ Scenario 2 (EU lender, Art. 22),
  Item 11 ≈ Scenario 6 (legal contract review, quote-grounding + sign-off) — three of twelve items retest
  an existing worked scenario's exact vertical and exact recommended fix rather than transferring the
  concept to a new context. This reduces the effective number of independent knowledge checks in the
  practice set from 12 to roughly 9, ironically about the item count the domain actually carries on the
  real exam — meaning a candidate who has memorized this chapter's scenarios, rather than internalized the
  underlying judgment, could pass a meaningful fraction of the practice set. Change the vertical or
  framing on these three items.
- Exam-day heuristics (§7) are restatement-style, matching the brief's own example ("least privilege =
  remove the capability, not log it" is itself a restatement). Not flagged as a defect on its own, but see
  the redundancy finding above — the aggregate effect across sections is the problem, not §7 alone.

### Overlap management

- **[MAJOR]** No cross-reference to Domain 3 anywhere in the chapter, despite three points of direct
  overlap: (1) Scenario 4 / Item 1's tool-removal least-privilege content is close to identical to Domain
  3's own objective "Evaluate tool/agent configuration for capability bloat"; (2) §2.3's "Data leakage,
  cross-tenant" row names "tenant-scoped retrieval filters enforced at the data layer" — this is Domain 3's
  "multi-tenant isolation" territory; (3) Scenario 7 (MCP supply-chain trust) touches Domain 3's "connection
  protocols... MCP" objective. Add one-line cross-references (e.g., "see Domain 3 for tool/agent
  configuration mechanics; this chapter treats capability removal as the strongest node in the general
  safety-control hierarchy") so the reader understands why the same fact pattern appears in both places
  without concluding it's duplicated by accident.
- **[MINOR]** §2.6's bias-eval methodology (segmented eval sets, re-run on every change) is conceptually
  the same discipline as Domain 4's "adversarial eval sets" and "evaluation datasets... using mixed
  methodologies" objective, but the draft doesn't note the connection (the dossier does, in its Objective-5
  writeup, but the sentence didn't carry over into the draft). Add a short cross-reference so this chapter
  is clearly scoped to "what to measure and how often for fairness specifically," not re-deriving eval
  mechanics Domain 4 owns.
- **[MINOR]** The dossier's guardrail primitives (§1, Objective 1) mention "continuous monitoring and
  red-teaming" as closing the guardrail loop; this did not carry into the draft's concepts, anti-patterns,
  or failure modes at all. Either add a brief mention with a Domain 4 cross-reference (red-teaming as an
  adversarial eval activity) or confirm the omission is intentional so it isn't lost between dossier and
  final chapter.

---

## Practice items — item-by-item

1. **Item 1 (tool removal, select 1).** Well-formed distractors, clear discriminator. Verdict: ACCEPTABLE
   but redundant with Scenario 4 and the guide's own Sample 1 — recommend replacing with a different
   concept (e.g., a classifier-vs-programmatic-validation discriminator) to reduce repetition.
2. **Item 2 (HIPAA combination, select 1).** Correct answer conspicuously longer/more detailed than
   distractors (length tell). Stem states "containing PHI" outright, reducing the inferential step. Verdict:
   NEEDS FIX — rebalance option lengths and soften the stem.
3. **Item 3 (EU lender, GDPR Art. 22, select 1).** Distractor D is a throwaway (FedRAMP, unrelated domain).
   Also retests Scenario 2's exact vertical. Verdict: NEEDS FIX — change vertical and strengthen distractor D.
4. **Item 4 (FedRAMP ceiling, select 2).** Good use of multiple-response with a stated "select 2." Stem
   states the required IL level outright rather than describing CUI and letting the candidate derive it; also
   rests on a compliance-ceiling fact that could shift. Verdict: NEEDS FIX — soften stem, flag volatility.
5. **Item 5 (version drift, select 1).** Distractor A is a strawman (defeatist, not plausible). Otherwise
   solid, well-differentiated from the retrieval-drift heuristic elsewhere. Verdict: NEEDS FIX — replace
   distractor A.
6. **Item 6 (indirect injection, select 1).** Correct answer notably longer than distractors (length tell).
   Otherwise a strong, well-targeted item matching documented Anthropic guidance. Verdict: ACCEPTABLE with
   a length-balance fix.
7. **Item 7 (HITL tier matching, select 1).** Clear, well-calibrated, good use of the reversibility×impact
   discriminator across four options. Verdict: SHIP AS-IS.
8. **Item 8 (OWASP categories, select 2).** Pure recall of a named list — no scenario, no architectural
   judgment tested; also names a dated ("2025") external standard subject to revision. The weakest item in
   the set structurally. Verdict: REWRITE — turn into a scenario where the candidate must recognize which
   OWASP-named risk category a described failure exemplifies, rather than naming the list directly.
9. **Item 9 (logging vs. GDPR, select 1).** Correct answer longer than distractors (length tell). Otherwise
   a strong, well-targeted trade-off item matching T7. Verdict: ACCEPTABLE with a length-balance fix.
10. **Item 10 (stale bias eval, select 1).** One of only two items covering Objective 5; solid distractors,
    appropriately scenario-framed as a critique-the-claim item. Verdict: SHIP AS-IS.
11. **Item 11 (contract-review hallucination, select 1).** Correct answer longer/more detailed than
    distractors (length tell). Also retests Scenario 6's exact vertical and exact fix. Verdict: NEEDS FIX —
    change vertical/failure axis and rebalance option lengths.
12. **Item 12 (citations vs. explainability, select 1).** Good conceptual item; distractor D (conflating a
    product feature with an EU AI Act requirement) is a genuinely attractive plausible-but-wrong option.
    Verdict: SHIP AS-IS.

Net: 5 of 12 items ship as-is or with only cosmetic fixes; 6 need a specific, stated fix (length balance,
distractor strength, or stem giveaway); 1 (Item 8) should be rewritten from scratch.

---

## Must preserve

- The five-level control-strength hierarchy (§2.1) and its T1 trade-off table — correctly sourced to the
  exam guide's own sample item, with a genuine "why it's decidable" reasoning chain (bypass resistance,
  cost, best-for), not just an asserted ranking.
- The failure-mode taxonomy (§2.3) pairing each named failure with a *specific* architectural mitigation
  rather than a generic "test more" — this is exactly the altitude the brief calls for, and the direct vs.
  indirect prompt-injection distinction is handled correctly.
- The FedRAMP deployment-surface trade-off (T5, Scenario 3, Item 4) — a genuinely non-trivial, exam-relevant
  discriminator (1P API vs. Bedrock GovCloud IL4/5 vs. Vertex Assured Workloads IL2) explained with real
  architectural reasoning, not vendor-marketing framing.
- The citations-vs-explainability distinction (§2.6, Item 12) — correctly scoped and sourced, avoids the
  common overclaim that grounding equals explainability.
- The failure modes & diagnostics table (§5) — genuinely doubles as a triage reference, matching the
  brief's intent, for the four objectives it covers.
- Consistent practice-item rationale discipline: nearly every item explains why each individual distractor
  fails, not just why the correct answer is correct.
- Scenario 5 (insurance triage) and Scenario 6 (legal contract review) — both have "why the plausible
  alternatives lose" sections that do real analytical work and state a genuine "what would change the
  answer" condition, which is the hardest part of this section type to get right.

---

## Coverage matrix

| Objective | Covered adequately? | Evidence |
|---|---|---|
| Implement guardrails and safety controls | Yes — strong | §2.1, §2.2, §2.3, T1–T3, Scenarios 6/7, §5, §6, Items 1/6/9. Deepest and most redundant coverage in the chapter (see redundancy findings). |
| Identify risks, limitations, and failure modes of LLM systems | Yes — strong | §2.3 taxonomy (10 failure modes, each with a named mitigation), §5, Items 1/5/6/11/12. |
| Apply human-in-the-loop validation strategies | Yes — adequate | §2.4, T4, Scenarios 2/5/6, Items 3/7/11. Good tiering discriminator (reversibility × impact); no major gaps found. |
| Ensure compliance with regulations (GDPR, HIPAA, FedRAMP) | Yes — strong, arguably over-weighted relative to other objectives | §2.5, T5–T7, Scenarios 1/2/3, Items 2/3/4/9. Three of seven worked scenarios and three trade-off tables sit here; see stem-giveaway findings for Scenarios 1–3. |
| Address ethical AI considerations (bias, fairness, transparency) | **No — thin, and the coverage table is padded** | §2.6 (concept-only, no trade-off table), Items 10/12 (the only two items that genuinely test this objective). No dedicated worked scenario; the two scenarios credited in §9 (2, 5) do not actually test bias/fairness/transparency. No anti-pattern or failure-mode-table entry despite the underlying insight already existing in §2.6. |

---

## Sources

No new external sources were consulted for this review. All findings were derived from AGENT-BRIEF.md,
claude-arch-professional-guide.md, and the two files reviewed
(research/05-governance-safety-risk-dossier.md, drafts/05-governance-safety-risk-draft.md), including the
source IDs (D05-S01…D05-S30) already cited within them and resolved in
research/05-governance-safety-risk-sources.md. Where a finding disputes emphasis or balance rather than a
factual claim, no source citation is required per AGENT-BRIEF §6; where a finding references the exam
guide's own sample item, it is the same source the draft itself already cites as `D05-S30`.
