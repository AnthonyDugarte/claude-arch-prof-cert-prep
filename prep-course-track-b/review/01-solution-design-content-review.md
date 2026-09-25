# Content Review — Domain 1: Solution Design & Architecture

Reviewer: Content Reviewer (axes per AGENT-BRIEF §4 / task brief). Files read: AGENT-BRIEF.md,
VERIFIED-FACTS.md, claude-arch-professional-guide.md, research/01-solution-design-dossier.md,
drafts/01-solution-design-draft.md. Draft measured at **8,929 words** (`wc -w`) against a **6,000-word
ceiling** for this domain (17% weight, per task brief).

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. Cut ~2,900 words (8,929 → ≤6,000) using the itemized Cut list below. This is mechanical, not
   conceptual — no section needs new research, and one section (Core concepts) needs a small, specific
   addition funded by cuts elsewhere.
2. Objective 1 ("translate business problems into Claude-based AI solutions") is the thinnest-taught
   objective despite being the first-listed blueprint item, and the objective-coverage table papers over
   it by citing all eight worked scenarios generically. The dossier researched a full, source-anchored
   methodology for this objective (Anthropic's pilot-selection criteria, a SMART-style success-criteria
   rubric, a four-question business-to-architecture translation rule) — none of it reached the draft. Add
   a compact concept for it (~150 words, budgeted in the cut list).
3. Every one of the 12 practice items has a length tell: the correct option is the longest and most
   qualified-sounding option, several extremely so (Items 5, 6, 11 run 3–4x the word count of their
   distractors). This is a systemic item-writing defect, not an isolated one — a candidate could clear a
   meaningful fraction of this set on option length alone, with zero domain knowledge.
```

---

## Cut list

Target: **≤6,000 words total**, prioritized lowest exam-value-per-word first. "Current" figures are
per-section word counts (approximate, `awk` split on `## N.` headings; sum ≈8,877 vs. `wc`'s 8,929 due to
heading/table-syntax counting differences — treat as directional, not exact).

| # | Section | Current | Target | Specific cut |
|---|---|---|---|---|
| 1 | §4 Trade-off analyses | 2,299 | **1,450** | Largest single cut. (a) Cut the TTFT infrastructure anecdote in §4.4 ("cut p50 TTFT ~60% and p95 >90% purely by not provisioning a sandbox until a tool call needed one") — a real Anthropic infra fact but not an exam-actionable architecture lesson; lowest value-per-word in the chapter (~35 words). (b) In §4.8, keep the full advisor/orchestrator explanation here (it's the trade-off section) and cut its near-verbatim restatement from Item 6's rationale (see row 6 below) — don't derive the same framework twice. (c) In §4.1/§4.4/§4.6, the prose paragraphs immediately under each table restate the table's own columns in sentence form; compress each to one sentence per branch instead of two–three (tables already carry the axes — the prose should add the discriminator, not repeat the row). (d) Drop the "90% right once is 59% right five times running" arithmetic aside in §4.5 — illustrative flourish, not required for the pass^k point already stated. |
| 2 | §9 Practice items | 1,930 | **1,300** | Cut Item 9 entirely (redundant with Item 1 — both are "batch beats sync/agentic for a bulk, non-interactive, cost-driven workload," differing only by vertical dressing; even the "keyed by `custom_id`" detail repeats). That alone saves ~145 words and moves the set from 12 to 11 items (still inside the 8–12 band). Take the remaining ~485 words from trimming rationale prose: several items re-quote a fact already established elsewhere in full (e.g., re-quoting "confidently prais[es] the work" verbatim in Item 4's rationale when it has already appeared three times) — cite, don't re-quote. Fixing the length-tell defect (see Practice-item findings) by *shortening* the correct answers in Items 5, 6, 11 (currently 21, 32, 34 words) rather than padding distractors serves this cut target directly. |
| 3 | §5 Worked scenarios | 1,108 | **800** | Cut Scenario S4 (government benefits intake). It teaches the same lesson as S2 (healthcare prior-auth): decision authority stays with a deterministic rules system / licensed human, model only extracts and drafts. S4's one distinct insight — "a better model doesn't fix an authority problem" — survives independently in Heuristic 13 and Item 7, so nothing is lost. Saves ~145 words directly; tighten the remaining seven scenarios' "Alternatives lose" clauses by dropping citations that only re-confirm a fact already established in §4 (e.g., S6 re-stating the 3–10× figure that §4.2 already owns) for the remaining ~160 words. |
| 4 | §11 Sources | 634 | **330** | Keep the source table as-is (traceability is non-negotiable). Cut the two prose paragraphs beneath it: the "`[UNVERIFIED]` claims in this chapter" paragraph (~120 words) restates points already made in full in-body (§3.12, §7 notes) — compress to a 4-item bullet list with section pointers. The "Model currency note" paragraph (~90 words) is process documentation for the course team (explaining the brief/skill-cache discrepancy), not candidate-facing content — compress to one sentence citing `[VF]` and point to `VERIFIED-FACTS.md`. |
| 5 | §3 Core concepts | 1,147 | **950 (net)** | **Add** a new concept, "Business-problem translation & pilot fit" (~150 words): Anthropic's pilot-selection criteria (well-suited to LLM strengths, measurable success criteria, clear ROI, business-critical-but-low-risk, abundant data, minimal disruption, scalable) condensed to a compact list, plus the SMART-style success-criteria rubric and the four-question translation rule (unit of work enumerable? cost of error? latency budget? which pillar?) — this is the fix for must-fix #2 and is already fully sourced in the dossier (§3, Objective 1), just unused. **Cut** ~350 words to fund it: shorten concept 3.8's "misconception" sentence (decomposition techniques are fully elaborated again in §4.6/§4.7 — 3.8 doesn't need to re-argue the point, just name it), and trim one clause from 3.1–3.11 wherever the "misconception" sentence restates something the trade-off or anti-pattern section already develops in full. |
| 6 | §7 Anti-patterns | 408 | **350** | Convert the eight bolded prose entries (Looks right: / Fails: / Instead:) into a 4-column table (Anti-pattern \| Looks right because \| Fails because \| Instead), matching §6's table format. Same content, tighter delivery — typically saves 15–20% on this kind of parallel-field content, and fixes the format-consistency finding below at the same time. |
| 7 | §2 Exam-relevance framing | 259 | **210** | Combine the two-sentence framing lead-in before the distractor-archetype table into one sentence; the table itself is already terse and should not be cut (it is the chapter's exam-pattern index). |
| 8 | §6 Failure modes & diagnostics | 523 | **460** | Keep as a table (already correct format and genuinely doubles as triage reference — do not cut rows). Tighten "First thing to check" and "Fix" cell wording where it exceeds one clause. |
| 9 | §8 Exam-day heuristics | 285 | **240** | Already dense; trim heuristic 13's parenthetical guide cross-reference to a shorter form. |
| 10 | §10 Objective-coverage table | 171 | **150** | No word cut needed beyond fixing the Objective 1 row's honesty (see Findings) — replace "S1–S8" with the specific scenarios whose recommended answer actually turns on business-problem translation (this may net-neutral on words while being materially more honest). |
| 11 | §1 Front matter | 113 | **100** | Minor tightening only. |
| | **Total** | **8,877** | **~6,000** | |

**Do not cut:** the eight trade-off tables themselves (only the prose around them), the four-criterion
agent-gate, the six required core trade-offs (§4.1–§4.6), the pass^k/pass@k distinction, the multi-agent
three-justification list (§4.2), the tool-decomposition sanity test (§4.7), and Scenario S5 (the only
scenario built on Anthropic's own worked example almost verbatim — see Must preserve).

---

## Findings

### Blueprint coverage

- **[BLOCKER]** Objective 1 ("Translate business problems into Claude-based AI solutions") has no
  dedicated methodology in the draft. The dossier's richest material for this objective — Anthropic's own
  pilot-selection criteria (7 named criteria), the Specific/Measurable/Aligned/Time-bound success-criteria
  rubric, graduation criteria for pilot→scale, and the explicit "business problem becomes an architecture
  through four questions" translation rule (dossier §3, Objective 1) — never appears in the draft. What
  the draft has instead (§3.12, §4.8 value-pillar table) answers "which pillar and what architecture
  follows," not "how do you recognize a good first Claude project and write its success criteria," which
  is what the objective's wording asks. Required fix: add the concept in the Cut list row above, and
  update the coverage table row.
- **[BLOCKER]** §10 Objective-coverage table, Objective 1 row cites "S1–S8" (all eight worked scenarios).
  Every scenario in this chapter necessarily starts from a business problem, so citing all eight is
  padding, not evidence — it is the exact defect this task was told to check for. Required fix: cite only
  the scenarios (if any, once the new concept exists) whose *recommended-approach reasoning* actually
  turns on translation methodology, or cite the new §3 concept plus §4.8 and drop the blanket scenario
  list.
- **[MAJOR]** Objective 2 ("input → processing → output → feedback loops") is covered piecemeal — context
  strategy (input), harness/execution mode (processing), feedback-loop placements (feedback) all exist —
  but the blueprint's own four-stage vocabulary never appears as an explicit synthesis anywhere in the
  body, only in the front matter's verbatim objective list and the coverage table. A candidate reading the
  chapter cannot see where "input" and "output" specifically map. Fix at near-zero word cost: add one
  compact four-row table early in §2 (stage → what it is architecturally → where it's covered in this
  chapter), replacing the equivalent prose that already exists there.
- **[MINOR]** No explicit cross-references to Domain 2, 3, or 6 anywhere in the body (one incidental
  mention of "the guide's Domain 3 sample" is not a topic pointer). The dossier's own §0 scope-control
  table shows the draft *respects* the boundaries (no RAG chunking depth, no MCP protocol comparison, no
  GDPR/HIPAA controls, no SLA negotiation technique) — the gap is that it never signals this to the
  reader. Add 2–3 one-line pointers, e.g., after §3.6 ("just-in-time vs. pre-inference retrieval — full
  retrieval-strategy trade-off is Domain 3's"), after §4.4 ("protocol/observability mechanics for these
  modes: Domain 3"), and near §4.8 ("SLA *negotiation* with stakeholders: Domain 6"). Near word-neutral if
  it replaces an existing hedge clause.

### The "business value pillars" problem

- **No finding — handled correctly, must preserve.** §3.12 states plainly that "business value pillars" is
  blueprint-only language, cites the absence of an Anthropic source for the phrase, and does not fabricate
  an official framework around it. §4.8 then proceeds to give a fully usable pillar→metric→architecture
  table grounded in real (dated, cited) Anthropic sources (enterprise ebook, "27% of Claude-assisted work"
  research post, cost-optimization docs) without re-asserting the five-item list as Anthropic's own
  taxonomy. This is the correct resolution of a genuinely hard instruction (teach it, don't fabricate it,
  don't hedge it into uselessness).
- **[MINOR]** The `[UNVERIFIED]` flag on the pillar framework appears once, in §3.12, and is not repeated
  or cross-referenced at §4.8 — the table a reader would actually use in a scenario. A reader who jumps
  straight to §4.8 (likely, given it's in the trade-off section) will use the table without seeing the
  caveat. Add "(pillar list is blueprint language, not an Anthropic framework — see §3.12)" to the §4.8
  header line; costs ~15 words, worth it given the caveat's importance.

### Altitude

- No basic prompt/API teaching found. Consistently operates at "which pattern/mechanism, and why" —
  correct altitude throughout.
- **[MINOR]** §3.6 (context rot) raises just-in-time vs. pre-inference retrieval and then quotes "the
  decision boundary... depends on the task" without stating what it depends *on* inside this chapter. This
  is legitimately Domain 3's fuller territory (per the dossier's own scope table), so the fix is not to
  develop it here but to say so explicitly (see the cross-reference finding above) rather than leaving the
  "it depends" hanging, which reads as exactly the hand-waving the brief prohibits.

### Trade-off quality (core axis)

- **Strong — must preserve.** All six required comparisons for this domain are present with explicit axes
  and "choose A when / choose B when" discriminators: augmented LLM vs. workflow vs. agentic loop (§4.1);
  single agent vs. multi-agent (§4.2); chaining vs. routing vs. parallelization vs. orchestrator-workers
  vs. evaluator-optimizer (§4.3, with an explicit "one-line discriminators" block that is exactly the
  right altitude); sync vs. streaming vs. async vs. batch (§4.4); feedback-loop placement (§4.5); and
  decomposition-stopping signals (§4.6). Two bonus tables (tool decomposition §4.7, pillar→SLA §4.8) push
  past the 4–6 minimum, appropriate for 17% weight. No false binaries found — every table has 3–8 real
  options. No recommendation is stated without the cost of the alternative; every "choose when" is paired
  with a "reject when" or an explicit cost row.
- **Must preserve specifically:** §4.1's table row distinguishing "Auditability: Trivial / High / Lower —
  non-deterministic between runs" is the cleanest single articulation in the chapter of *why* the
  workflow/agent choice matters beyond cost.
- "When NOT to use an agent" and "when not to use an LLM at all for a step" are both explicitly and
  repeatedly taught (§4.1's four-criterion gate; §4.8's "don't use an LLM for this step" section; AP8;
  Heuristic 7; distractor archetype A5) — this satisfies the task's specific check on both fronts.

### Multi-agent cost honesty

- **Strong — must preserve.** Every multiplier in the draft is stated with its baseline named in the same
  clause: "3–10× single-agent" vs. "~15× a chat interaction" vs. "~4× a chat interaction" are never
  conflated, and §4.2's table places the two baselines side by side in one cell precisely to prevent a
  reader from treating them as the same number. No instance found of a bare multiplier without a stated
  comparator.
- Multi-agent is consistently framed as a cost/complexity decision gated on three named justifications
  (context protection, parallelization, specialization), never as a sophistication upgrade — AP1–AP3 and
  Heuristic 5 all reinforce this. Good.

### Scenario realism

- **[MAJOR]** Scenario 2 (healthcare prior-auth) and Scenario 4 (government benefits eligibility) teach
  the same lesson: augmented LLM extracts facts, a deterministic rules/policy engine decides, a
  human/licensed authority holds the decision, the model only drafts. Different industries, same
  architecture and same discriminator. See Cut list row 3.
- All eight scenarios have load-bearing constraints (each stated number or authority fact maps directly to
  a piece of the recommended answer) and substantive "why the alternatives lose" reasoning — no decorative
  constraints found, no scenario where the answer is obvious from the setup with no attractive distractor
  addressed.
- **Must preserve:** Scenario 5 (SaaS/telecom, 26-tool support agent) reproduces Anthropic's own worked
  example (order-history context pollution degrading technical diagnosis) with high fidelity and pairs it
  with a genuine "what changes it" threshold (8 tools, occasional mis-selection → consolidate instead of
  splitting). This is the single best-executed scenario in the set.
- Scenario 8 (logistics, two-tier routing across efficiency/transformation pillars in one system) is a
  genuinely non-trivial synthesis and should not be touched.

### Practice-item quality

- **[BLOCKER]** Systemic answer-length tell across all 12 items. In every item, the correct option(s) are
  the longest and most qualified/detailed on the list; in Items 5, 6, and 11 the correct answer runs 3–4x
  the word count of the shortest distractor (e.g., Item 6's correct answer is 32 words against distractors
  of 6, 7, and 10 words; Item 11's is 34 words against 10–12). A test-savvy candidate with no domain
  knowledge could exploit this pattern across the set. See item-by-item section below and Cut list row 2
  for the fix direction (prefer shortening the correct answer over padding distractors, since it serves
  the word-count target simultaneously).
- **[MINOR]** Item 3's distractor E ("It occasionally produces a typo") and Item 8's original design
  otherwise are fine, but E here is a throwaway with no plausible-reasoning appeal — replace with something
  a reasonable architect might actually flag (e.g., "the agent's response time increased by 200ms").
- No item depends on a volatile fact for its correctness (prices/limits appear only as supporting color,
  never as the crux); no item is pattern-recognition trivia — all 12 are scenario stems requiring
  synthesis, matching the guide's Section 8 cognitive level. The 9 single-select / 3 multiple-response
  split matches the researcher's claim exactly (Items 3, 8, 12 are the multi-select ones), and every item
  states its select count.

### Structure and style compliance

- All 11 required sections present, in required order, with correct front matter, exam-relevance framing,
  core concepts (definition → decision → misconception format, as required), trade-offs, scenarios,
  failure modes, anti-patterns, heuristics, practice items, coverage table, and sources.
- **[MINOR]** §6 (failure modes) is a table as required; §7 (anti-patterns) is bolded prose, not a table.
  The task brief for this review calls for both as "usable tables." Convert per Cut list row 6 — also
  saves words.
- No emoji, no marketing language, no filler ("in today's fast-moving AI landscape" etc.) found anywhere.
  Dense and declarative throughout — this is the chapter's clearest across-the-board strength.

### Overlap management

- See Blueprint-coverage findings above (cross-reference gaps to Domains 2/3/6). No content was found that
  actually *belongs* in a neighbor chapter (no RAG chunking depth, no MCP/API protocol comparison, no
  prompt-caching mechanics beyond citing its cost effect, no GDPR/HIPAA control detail, no SLA negotiation
  technique) — the scope discipline itself is good; only the signposting is missing.

---

## Practice items — item-by-item

1. **Item 1 (batch classification, select 1).** Non-trivial, well-sourced. Length tell: correct B (17
   words) vs. distractors (7–11 words). Verdict: NEEDS FIX (length only).
2. **Item 2 (orchestrator-workers for diligence research, select 1).** Strong pattern-recognition item.
   Length tell: correct C (12 words) vs. 7–8-word distractors. Verdict: NEEDS FIX (length only).
3. **Item 3 (multi-agent justification signals, select 2).** Good use of multiple-response with two real
   signals (A, C) against three real-looking non-signals. Correct answers longer than incorrect ones;
   distractor E is a throwaway. Verdict: NEEDS FIX — rebalance lengths, replace E.
4. **Item 4 (checklist validator vs. self-review, select 1).** Severe length tell (14 vs. 5–6 words).
   Concept somewhat redundant with existing self-critique coverage (§3.11, AP4, Heuristic 8) but adds a
   distinct packaging (disclosure checklist) — keep, lower priority than the Item 9 cut. Verdict: NEEDS FIX.
5. **Item 5 (crash recovery via session log, select 1).** Most severe length tell in the set (21 words vs.
   5–6). Otherwise an excellent, non-obvious durability item. Verdict: NEEDS FIX (length only, high
   priority).
6. **Item 6 (orchestrator vs. single-model economics, select 1).** Second-most severe length tell (32
   words vs. 6–10). This is the chapter's best economics item — do not touch the underlying concept, only
   the option balance. Verdict: NEEDS FIX (length only, high priority).
7. **Item 7 (deterministic date check misrouted to an LLM call, select 1).** Moderate length tell (14 vs.
   5–9). Clean, well-targeted item. Verdict: NEEDS FIX (length only).
8. **Item 8 (subagent mechanics facts, select 2).** Mild length tell on A. Distractor E ("subagents reduce
   total token consumption") is a genuinely attractive, well-designed false statement. Verdict: NEEDS FIX
   (length only, minor).
9. **Item 9 (batch for regulatory filing, select 1).** Redundant with Item 1 — same discriminator (batch
   beats sync/agentic for bulk, non-interactive, cost-driven work), different vertical only. Verdict: CUT.
10. **Item 10 (compaction vs. reset, select 1).** Distinct, well-targeted concept. Length tell (18 vs.
    5–13). Verdict: NEEDS FIX (length only).
11. **Item 11 (transformation pillar, select 1).** Most extreme length tell in the entire set (34 words vs.
    10–12 — the correct answer is nearly a paragraph next to single clauses). Valuable, distinct concept —
    do not cut, but this is the top priority for the length-tell fix. Verdict: NEEDS FIX (high priority).
12. **Item 12 (QA-agent tradeoffs, select 3).** Good, rare select-3 format; correct trio (A, B, C) longer
    than the two distractors. Verdict: NEEDS FIX (length only).

Net: 0 of 12 ship as-is; 11 need the same mechanical fix (length rebalancing, direction: shorten the
correct answer where possible rather than pad distractors, to serve the word-count target
simultaneously); 1 (Item 9) should be cut for redundancy, bringing the set to 11 items.

---

## Must preserve

- The eight trade-off tables in §4 and their explicit "choose A when / choose B when / reject when"
  discriminators — this is the chapter's core deliverable and the strongest-executed section against the
  task's own top-priority axis. Do not thin these during the word cut; cut the prose around them instead.
- The baseline-honest handling of multi-agent token multipliers (§4.2's table cell placing "3–10×
  single-agent" and "~15× a chat interaction" side by side) — a direct, correct resolution of the
  dossier's own flagged contradiction between sources.
- The handling of "business value pillars" (§3.12 + §4.8): flagged `[UNVERIFIED]` as an Anthropic
  framework without fabricating structure, while still delivering a fully usable pillar→metric→architecture
  table. This must survive the length cut intact — it is the hardest instruction in this domain's brief
  and the draft got it right.
- Scenario 5 (SaaS/telecom, 26-tool agent) — the highest-fidelity scenario to a named Anthropic source
  example, with a genuine "what changes the answer" threshold. Do not cut.
- Scenario 8 (logistics, two-tier pillar routing) — a genuine synthesis scenario, not a restatement of an
  earlier pattern.
- The four-criterion agent-build gate (Complexity, Value, Viability, Cost of error) in §4.1 and its
  restatement as Heuristic 2/AP2 — a clean, source-anchored, decidable gate.
- The "don't use an LLM for this step" thread running through §4.8, AP8, Heuristic 7, distractor archetype
  A5, and Items 4/7 — thorough coverage of a task-brief-mandated check; keep at least one full statement of
  it even after trimming the repeated instances.
- Consistent per-distractor rationale discipline across all 12 practice items (a real strength independent
  of the length-tell defect) — every item explains why each wrong option fails, not just why the right one
  is right.
- Zero emoji, zero marketing language, dense declarative style throughout — do not let word-cutting edits
  introduce filler transitions to smooth the cuts.

---

## Coverage matrix

| Objective | Covered adequately? | Evidence |
|---|---|---|
| Translate business problems into Claude-based AI solutions | **No — thin, and the coverage table is padded** | §3.12 and §4.8 cover "which pillar, which architecture" but not "how to recognize/scope a good Claude project" or write its success criteria. §10's citation of "S1–S8" is generic padding. The dossier's own pilot-selection/success-rubric/translation-rule material (Objective 1, its richest section) never reached the draft. |
| Design end-to-end architectures (input → processing → output → feedback loops) | Yes — present but not synthesized | §3.4/§3.5/§3.10/§3.11 and §4.4/§4.5 cover the pieces (harness, execution mode, feedback placement) but the blueprint's own four-stage vocabulary is never assembled into one explicit passage in-body. |
| Select appropriate architectural patterns (workflow, agentic, augmented LLM) | Yes — strong | §3.1–§3.3, §4.1, §4.3, AP2/AP3, Scenarios 1/3/6/7/8, Items 1/2/7. Six-pattern taxonomy fully sourced with discriminators. |
| Design multi-agent systems and orchestration strategies | Yes — strong | §3.7/§3.9, §4.2/§4.6/§4.8 (advisor vs. orchestrator), AP1, Scenarios 5/6, Items 3/6/8/12. Baseline-honest cost treatment throughout. |
| Apply decomposition techniques for complex problem solving | Yes — adequate | §3.8/§3.9, §4.6/§4.7, AP1/AP5/AP6, Scenarios 1/5/6, Items 3/8/10/12. Four decomposition axes distinctly named; stopping rules are source-anchored and concrete. |
| Align solutions to business value pillars | Yes — strong, and correctly hedged | §3.12, §4.8, Heuristics 1/10/12/14/15, Scenarios 3/6/8 (each with an explicit "Pillar note"), Items 1/9/11. The `[UNVERIFIED]`-framework handling is a genuine strength (see Must preserve). |

---

## Sources

No new external sources were consulted for this review. All findings were derived from AGENT-BRIEF.md,
VERIFIED-FACTS.md, claude-arch-professional-guide.md, and the two files under review
(research/01-solution-design-dossier.md, drafts/01-solution-design-draft.md), including the source IDs
(D01-S01…D01-S32) already cited within them and resolved in research/01-solution-design-sources.md. Where
a finding disputes a coverage/emphasis/format judgment rather than a factual claim, no external source
citation is required per AGENT-BRIEF §6.
