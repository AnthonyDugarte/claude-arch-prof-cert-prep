# Content review — Domain 6: Stakeholder Communication & Lifecycle Management (14%)

Reviewed: `drafts/06-stakeholder-communication-lifecycle-draft.md` (275 lines, 5,559 words) against
`research/06-stakeholder-communication-lifecycle-dossier.md`, `AGENT-BRIEF.md` §3/§4/§6, and the exam
guide's Section 6 objectives and Section 8 sample cognitive level. Line numbers are draft line numbers.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. Objective 5 (lifecycle phases) is claimed in the coverage table but not substantively covered.
   The chapter has no lifecycle-phase model and no gate-criteria table, although the dossier
   already contains both (dossier lines 106-118 and 121). This is one of five blueprint objectives
   in a 14% domain, left effectively uncovered. Port the gate table and the phase chain, and add a
   practice item that turns on a gate criterion.
2. The domain's central examinable skill — converting "it must be accurate" into a measurable
   acceptance criterion — is asserted at least six times (lines 35, 41, 51, 79, 84, 182) and never
   once demonstrated. Related: "production-representative sample" is used as the load-bearing term
   of the whole chapter (lines 24, 110, 114, 183, 195) and is never defined operationally, and the
   "92%" threshold appears twice (lines 79, 145 of dossier / line 79 of draft) with no method for
   deriving a threshold. Add one worked transformation with named fields.
3. Practice items: item 9 contradicts the chapter's own discriminator in §3.4 and therefore has no
   single defensible answer; items 6 and 7 are definitional trivia, not scenario stems, in violation
   of AGENT-BRIEF §3.9 and of the chapter's own line 18; items 3 and 4 carry tells (color schemes,
   marketing decks) that put them below professional difficulty. Five of ten items need work.
```

**Overall judgment.** This is a good draft with a specific, repairable shape of failure. Platitude
density is genuinely low — roughly 5% of substantive lines, listed exhaustively below — which for this
domain is the hardest thing to achieve and the editor should recognize it as an accomplishment, not a
baseline. The real defect is different: the draft **drops three of the dossier's four reusable
artifacts** (the discovery question→consequence table, the ADR template, the lifecycle gate table) and
substitutes assertion for demonstration on the two skills that carry the most exam weight. Everything
required is fixable additively from material the researcher already produced; no existing prose needs
rewriting. That is why this is SHIP-WITH-FIXES and not MAJOR-REWORK, notwithstanding three BLOCKERs.

---

## Platitude audit

Nine entries. Each would survive unchanged in a generic consulting deck about any technology in any
era. None are fatal individually; all are cheap to convert, and each conversion adds decision-bearing
content the chapter currently lacks.

**P1 — [MAJOR] §5, failure-mode row 6 (line 155).** `"Security blocks launch at the last gate | Discovery didn't include security in the room early | Check whether security was present during discovery, not just final review | Add security/legal as Consulted stakeholders during discovery, not only at a late review gate"`
This is "engage security early," true of every IT project since 1970. **Required fix:** name the
Claude-specific discovery answers security must sign *before* design freeze — data sensitivity and
residency, whether PII is redacted pre-prompt, retention and prompt/response logging settings, the
deployment surface (first-party API vs. Bedrock/Vertex/on-prem), and tool write-scope / blast radius.
Rewrite "first thing to check" as: "whether the data-sensitivity and deployment-surface discovery
answers carry a named security sign-off, not whether security attended a meeting." The dossier already
has these (dossier line 21); this row is the natural place to land them.

**P2 — [MAJOR] §6 anti-pattern "Recommendation-only slide" (line 165).** `"A trade-off conversation is presented as 'we recommend X' with no table of alternatives."`
Generic. **Required fix:** specify what the table must carry for a *Claude* decision, so the
anti-pattern has teeth: the axes are model tier against latency and cost, workflow against agentic,
RAG against long-context-plus-caching, and autonomy against HITL; and the rejected option's row must
state either the measured eval delta or the cost of re-deciding later. Without named axes this
anti-pattern cannot be recognized in an item stem.

**P3 — [MAJOR] §6 anti-pattern "The ADR graveyard" (line 171).** `"ADRs get written but never indexed or consulted before new decisions."`
Generic documentation hygiene; nothing here is about an LLM system. **Required fix:** name the
Claude-specific invalidation triggers that must force an ADR re-read — a model-version change, a
pricing change, or a context-window change can each invalidate the ADR's Context section without
anyone touching the code — and make the prompt/model change log reference the ADR it implements, so
the change log *is* the index. That converts a truism into a mechanism.

**P4 — [MINOR] §3.1 discriminator tail (line 71).** `"Never let 'it depends' stop there — the answer depends on *audience* and *durability required*, both statable in one sentence."`
This is AGENT-BRIEF §1 addressed to the reader as meta-instruction; it teaches nothing. **Required
fix:** cut the sentence, or replace it with the two-question test applied to a concrete Claude
decision ("we chose Sonnet 5 over Opus 5 for tier-1 triage" → who must approve, and must the reason
survive the author's departure).

**P5 — [MAJOR] §5, failure-mode row 2 fix (line 151).** `"route new asks through a change process, not ad hoc agreement"`
Generic change control. **Required fix:** state the consequence chain that makes this architectural: a
new ask that adds a tool or a task class changes blast radius and voids eval coverage, so it requires
its own reversibility answer, new eval cases for that class, and a re-run of the gate before it ships.
That is the same move §6's "silent scope creep in agentic projects" (line 175) already makes well —
this row should point at it rather than reach for generic governance language.

**P6 — [MINOR] §2 core concept "Baseline before promising improvement" (line 41).** `"Before committing to 'this will improve X,' current human or system performance on X must be measured."`
True of any project in any field. **Required fix:** sharpen to the version that is actually hard for an
LLM system and actually testable: the baseline must be measured *on the same eval set, with the same
grader or rubric*, that the system will later be measured against — otherwise the before/after
comparison is not a comparison — and name who measures it and by when (before design freeze). This
also closes a gap: the chapter currently gives no method for setting the "92%" threshold it cites.

**P7 — [MAJOR] §3.2 table row 6 (line 82).** `"Falls back to human queue when confidence signal is low"`
"Confidence signal" is undefined, and an LLM's self-reported confidence is not calibrated by default —
this is exactly the hand-wave that becomes a wrong answer on an exam item. **Required fix:** name the
mechanisms that can actually trigger it (judge score below threshold, retrieval top-k score below
threshold, explicit abstention in the output, disagreement between the two models in a cascade, or a
schema/validator failure), and state that the commitment is to the *behavior* with the trigger
disclosed, not to a confidence number.

**P8 — [MAJOR] §4.4 (line 136) and Item 5 rationale (line 227).** `"(b) loses: reads as obstruction to a hostile stakeholder and forfeits credibility to negotiate"` and `"*B* is likely to be rejected by a stakeholder already skeptical of 'AI vendors wanting more review'"`
This is precisely the defect the domain is most at risk of: the distractor fails on persuasion and
temperament, not on architecture. A candidate cannot decide this from the stated constraints.
**Required fix:** re-anchor B's failure on capacity allocation, which §3.4 line 100 already states:
blanket manual review spends finite reviewer capacity on the reversible low-risk permit tier, so
review of the high-risk tier becomes the bottleneck that gets rubber-stamped or bypassed. That is
decidable from the stem. Delete the credibility/obstruction reasoning from both places.

**P9 — [MINOR] §3.6 table row 3 (line 122).** `"No named owner ('the team owns it') | Never the right answer at handoff | Always"`
A non-option padding a trade-off table. Its presence makes §3.6 read as a three-way choice when it is
a two-way, and a row whose "choose when" is "never" is not a trade-off. **Required fix:** move it to §6
anti-patterns (it duplicates archetype 6 at line 27 anyway) and give §3.6 a real threshold for the
remaining two-way comparison — e.g., single owner while the system touches one team and no external
Consulted party; RACI once security or legal must be Consulted or once release authority sits outside
the build team.

---

## Findings

### Blueprint coverage and objective honesty

**[BLOCKER] §9 coverage table row 5 (line 274) and chapter-wide — Objective 5 is claimed but not covered.**
The row cites `"§2 (eval gate, RACI, runbook); §3.5, §3.6; §4.6, §4.7; §5; §6; Practice items 4, 10"`.
Those sections cover ownership models, one promotion gate, one handoff scenario and one feedback-loop
scenario. **No section of the chapter names the lifecycle phases, and no section states gate criteria.**
The objective is "Support lifecycle phases (discovery, design, handoff, monitoring, iteration)" — the
phases are named in the objective itself and appear in the draft only in the front-matter restatement
at line 10. There is no coverage of deprecation, retirement, or pre-declared re-eval triggers at all.
**Required fix:** add a numbered subsection (suggest §3.7, or a standalone §3.5 promoted to its own
section) carrying (a) the composited phase chain from dossier line 121 — discovery → design → build →
eval gate → pilot → production → monitoring → iteration → deprecation — and (b) the eight-row gate
table from dossier lines 108-118, which is already written and already sourced to D06-S03/S05/S06/S14.
Add one practice item that turns on a gate criterion (e.g., which gate a project has actually failed,
given a stem where the eval set exists but has no named owner and no documented threshold). Then
rewrite the coverage row to point at real locations.

**[BLOCKER] Chapter-wide — the accuracy-to-acceptance-criterion transformation is asserted, never demonstrated.**
Lines 35 (`"unstructured discovery collects untestable adjectives"`), 41, 51, 79, 84 and 182 all
presuppose the reader can perform the conversion; the chapter never performs it. Two dependent terms
are also undefined: **"production-representative sample"** (lines 24, 110, 114, 183, 195) is used as a
talisman five times with no operational content, and the threshold `"≥92% pass rate on eval suite v7"`
(line 79) appears with no method for choosing 92 over 85 or 97. **Required fix:** add a short worked
transformation in §2 or as a new §3 comparison, taking one stakeholder adjective ("the summaries must
be accurate") to a criterion with these named fields: task class; eval set name, version, size and
sampling method; grader type (programmatic assertion / LLM-as-judge with rubric / human adjudication);
threshold and how it was derived (measured baseline plus the cost asymmetry of a false positive versus
a false negative); measurement cadence; named owner; and the defined consequence of a breach. Define
"production-representative" in one sentence — drawn from production traffic over a stated window,
stratified by task type and channel, including known failure classes, re-drawn on a cadence — and
state honestly, per the dossier's own open question (dossier line 152), that no source fixes a minimum
sample size or confidence interval, so the architect must state sample size and variance explicitly
rather than quote a bare percentage.

**[MAJOR] §2 and §3 — the dossier's discovery question bank is missing (dossier lines 13-26).**
This is the most decision-bearing and most Claude-specific table in the research: nine questions, each
paired with what its answer changes (volume → batch vs. real-time and caching; latency tolerance →
model tier and workflow-vs-agent; accuracy bar *and who defines it* → whether an eval set with a named
owner must exist before build; cost ceiling → cascade; data sensitivity → deployment surface;
reversibility → mandatory HITL; human review capacity → SLA realism; integration surface → MCP vs.
bespoke API; success metric and its baseline → whether improvement is measurable at all). The draft
teaches none of it, yet **Item 3 (line 208) tests exactly this table** and §7's fifth heuristic (line
185) depends on it. **Required fix:** port the table into §2 under "Structured discovery" or as §3.0.
It is the single highest-yield addition available and it is already written.

**[MAJOR] §2 — no coverage of "this should not be an LLM use case" / kill criteria (dossier lines 27, 29).**
The dossier gives three discriminators (deterministic auditable output required → rules engine; low
reversibility with near-zero review capacity → fails the agentic-misalignment posture; no definable
baseline or success metric → cannot be governed at all) plus three kill criteria, correctly marked as
reasoning rather than doctrine. The draft's only trace is option (c) in scenario 4.5. Discovery that
cannot conclude "no" is not discovery, and archetype 5 (line 26) is otherwise unsupported. **Required
fix:** add the three discriminators to §2 and one kill-criterion line to §7's heuristics, preserving
the dossier's honesty about their provenance.

**[MAJOR] §3.1 and §2 — Objective 2's audience-tailoring rule is missing (dossier line 47).**
The draft covers *which artifact* but never *what to foreground within it*. The dossier's rule is
decidable and citable to D06-S15: to an executive, lead with the decision and the cost of the rejected
alternative in dollars, time and risk; to security and legal, lead with the pillar that was *not*
traded plus the residual risk; to engineering, lead with the mechanism and the ADR — and the substance,
the trade-off table itself, does not change across audiences, only which row is foregrounded. The
companion discriminator (security and operational excellence are generally not traded away, so an
option that trades them is wrong regardless of the business pressure) is also absent and belongs in
§7. Without these, an item asking how the same trade-off is presented to a CISO versus a CFO is
unanswerable from this chapter — and this is the axis on which a communication item can be made
decidable rather than a matter of taste. **Required fix:** add as a §3 comparison with the three
audiences as rows and "what to foreground / what stays fixed / who signs off" as columns.

**[MAJOR] §3.1 (lines 63-69) — the artifact-selection table omits the two Claude-specific artifacts.**
The dossier's documentation set (dossier lines 73-81) has seven entries; §3.1 carries five and drops
exactly the two that distinguish this chapter from a generic software-architecture chapter: the **eval
report** (evidence the system meets its quality bar, with method and sample, for the stakeholder who
approves promotion — cost of skipping: promotion becomes "it felt fine in the demo") and the
**prompt/model change log** (versioned record of what changed against what eval delta — cost of
skipping: no way to correlate a regression with a change, which makes the §3.2 quality SLO
ungovernable). The change log appears only as a failure-mode row (line 156) and the eval report not at
all. **Required fix:** add both rows to §3.1 with their "choose this when" and "the wrong choice loses"
columns, and make the change log's dependency on §3.2 explicit.

**[MAJOR] Objective 4, second half — "provide implementation guidance" is essentially uncovered.**
The objective has two clauses; the chapter covers "document architectures" well and "provide
implementation guidance" not at all. The dossier's integration/implementation guide (dossier line 80,
audience: downstream engineering teams, cost of skipping: every integrator reverse-engineers the
contract) has no counterpart in the draft. **Required fix:** add a row to §3.1 and two sentences naming
what a consuming team actually needs: the prompt/input contract and its stability guarantees, tool
schemas and auth model, rate and quota expectations, the documented fallback behavior from §3.2, and
where the eval set and its threshold live so the consumer can tell whether their use case is inside
the tested distribution. That last point is the Claude-specific one and is the reason this artifact is
not just an API doc.

**[MINOR] §4.6 / §2 — the ADR template is dropped (dossier lines 83-104).**
The draft names the five ADR fields at line 43 but never shows the template, and specifically never
shows the dossier's one Claude-specific instruction: the Context section must include the discovery
answers that drove the decision (volume, latency bar, accuracy bar plus its owner, cost ceiling, data
sensitivity, reversibility). That instruction is what makes the ADR section more than a 2011 Nygard
restatement, and it ties Objectives 1, 2 and 4 together. **Required fix:** include the template as a
code block in §2 or §3.1, with the Context guidance intact.

**[MINOR] §3.2 / §2 — error-budget mechanics for a *quality* SLO are defined only by analogy.**
Line 49 defines the error budget as `1 − SLO target`, which is the availability formulation. For a
quality SLI expressed as a pass rate the budget behaves differently, and the dossier states the actual
mechanism (dossier line 59): a drop below the floor is treated as budget exhaustion that halts further
prompt and model changes until root-caused. The draft never states what freezes, who authorizes the
un-freeze, or what the burn signal is. **Required fix:** add two sentences: what the exhaustion of a
quality budget freezes (prompt and model changes, not feature work), who lifts the freeze (the SLO's
single Accountable party from §3.6), and that the review cadence is the burn-rate proxy.

**[MINOR] §3.2 — the degradation ladder is compressed into one table cell (dossier line 63).**
The dossier gives an ordered ladder: primary model → smaller or cheaper fallback model, or
cached/templated response → explicit "we cannot answer confidently" surfaced to the user rather than a
silent wrong answer. Ordering is the teachable part, and the last rung (fail visibly rather than fail
silently) is the architecturally important one. **Required fix:** state the ladder as three ordered
rungs and note that it belongs *in* the SLA as the defined behavior when the primary path cannot meet
its SLO, not as an operational afterthought.

**[MINOR] §3.4 / §4.4 — "automation rate as a grown SLI" is used but never named (dossier line 67).**
Scenario 4.4 and Item 5 both turn on "a documented path to expand autonomy," which is the right answer,
but the chapter never names the mechanism that makes it concrete: the automation rate is itself tracked
as an SLI and raised as the error budget proves out. **Required fix:** name it in §2 or §3.4 so it is
recognizable in an item stem rather than inferable only from a scenario.

### Decidability, trade-offs, scenarios

**[MAJOR] §4.6 (line 140) — a scenario with no fork.** `"*Changes the answer:* nothing here changes it; this is a near-pure test of the documentation set itself."`
AGENT-BRIEF §3.5 requires "what would change the answer" as a structural element; a scenario that
admits nothing changes it is a definition check wearing a scenario's clothes, and it is the weakest of
the seven. **Required fix:** add a real fork that is decidable from constraints — IT operations has no
eval capability and no budget for an eval owner. The answer then genuinely changes: ops becomes
Accountable for availability and latency while the build team retains Accountable for the quality SLO
under an explicit sunset date and a named successor, rather than either a clean handoff or permanent
build-team on-call. That fork also repairs the false binary between candidates (b) and (c).

**[MAJOR] §4.5 (line 138) — this scenario belongs to Domain 1/2, not Domain 6.** Its substance is
cost-ceiling-driven model tiering and the cascade pattern; its Domain 6 hook is one clause ("a
discovery answer that should gate model choice before build"). With Objective 5 uncovered and chapter
word budget already at the top of range, this is the space to reclaim. **Required fix:** either
re-point the scenario at the genuinely Domain 6 question — the cost ceiling and the accuracy bar are
in direct conflict, who owns each number, where the conflict is recorded, and who arbitrates — or cut
it and spend the words on a lifecycle-gate scenario. Cross-reference Domain 1/2 for the cascade.

**[MINOR] §3.3 (lines 86-94) — decidable but the lowest-yield comparison in the chapter.** MoSCoW vs.
2x2 vs. RICE passes the named-practice test and the discriminator at line 94 is real, but the content
is generic product management; RICE appears nowhere in the blueprint. **Required fix:** compress to
three or four lines (keep the discriminator sentence, drop the table) and reallocate the words to the
lifecycle gate table. Do not cut it entirely — MoSCoW is load-bearing for the scope-creep failure mode
at line 151.

**[MINOR] §3.6 — see P9. The table's third row is not an option.**

**[NIT] Line 12 and line 18 — strong framing, one overreach.** `"This domain does not test writing skill or interpersonal style"` is exactly the right orientation and must stay. But line 18's `"almost never trivia ('what does RACI stand for')"` is directly contradicted by the chapter's own Items 6 and 7, which are trivia. Fix the items, not the framing.

### Structure and style

**[MINOR] §6 Anti-patterns (lines 161-176) — prose, not a table.** Seven named anti-patterns each with
"looks right because… but…" reasoning; content is good, format is not a usable triage reference.
**Required fix:** convert to a three-column table (Anti-pattern | The looks-right reasoning | What it
actually costs), matching §5's format. Named entries and reasoning are already there; this is
mechanical.

**[NIT] Word count.** 5,559 words — inside AGENT-BRIEF §3's 3,500–6,000 but above the 4,000–5,500
target given for this chapter, before the required additions. The additions above (gate table,
acceptance-criterion worked example, discovery question bank, audience-tailoring comparison) will add
roughly 700–900 words. **Required fix:** fund them by cutting §4.5 (~180 words), compressing §3.3
(~150 words), and deleting the two rewritten-to-nothing rationale clauses in P8. Net target ~5,800,
still inside the brief's ceiling.

**[NIT] §10 Sources (line 280) — one paragraph of prose listing IDs.** AGENT-BRIEF §6 requires the
editor to resolve every ID used and to list remaining `[UNVERIFIED]` claims explicitly. The draft's
prose paragraph gestures at the sources file instead. Also: `[UNVERIFIED]` appears nowhere in the body
even though the dossier flags four open questions (dossier lines 152-155), including the RACI
provenance question and the eval-set staleness cadence. **Required fix (editor):** table format,
resolved IDs, and an explicit `[UNVERIFIED]` list carrying at least the sample-size/confidence
question and the pilot-failure-statistics caveat.

**[NIT] No emoji, no marketing tone, no filler.** Confirmed clean throughout. Tone is dense and
declarative as required.

### Overlap management

**[MAJOR] No cross-references anywhere in the chapter.** The draft contains not a single pointer to a
neighbor chapter, which guarantees either duplication or a gap at the seams. Three specific seams:

- **Domain 4 (eval design, metrics, monitoring).** Item 8 (line 243) is a Domain 4 item as written —
  "how to source their first eval set" is eval-dataset design. §3.4's "sampled review with production
  feedback into eval set" and the eval-refresh cadence are likewise Domain 4 mechanics. Domain 6 must
  own the *stakeholder-facing* framing: the eval gate as the promotion *decision*, the eval report as
  the artifact a stakeholder signs, the quality SLO as an external *commitment*. **Required fix:**
  reframe Item 8's stem around the promotion gate ("what must be true about the eval set before it can
  serve as the promotion criterion") and add a one-line cross-reference to Domain 4 for construction
  and grading methodology.
- **Domain 5 (HITL validation, risk).** §3.4 in full, Item 9, and parts of §4.1 and §4.4 are HITL
  design, which is an explicit Domain 5 objective. Domain 6's ownership is the expectation-setting
  version: the risk-tier conversation with the stakeholder, and the automation rate as a commitment
  that grows against demonstrated error-budget evidence. **Required fix:** keep §3.4 (it is needed to
  make §4.4 and Item 5 decidable) but re-point its framing at the commitment, and cross-reference
  Domain 5 for the HITL mechanism itself.
- **Domain 1 (business-problem translation, value pillars).** JTBD at line 37 and §4.5 overlap Domain
  1's "translate business problems" objective. Domain 6 owns the *elicitation technique and its
  artifact* (the workshop, the question bank, the signed discovery record); Domain 1 owns the
  translation to pattern and value pillar. **Required fix:** one cross-reference at line 37; cut or
  re-point §4.5 per the finding above.

---

## Practice items — item-by-item

Set-level: 10 items (8 single-response, 2 multiple-response), each stating how many to select. Meets
AGENT-BRIEF §3.9's count. Distribution is skewed: four items on documents and definitions (3.1/ADR/C4
territory), none on a lifecycle gate, none on the accuracy-to-criterion conversion, none on the
SLA-versus-SLO consequence distinction as such, none on audience-tailored framing. With Objective 5
uncovered, at least one of Items 6/7 should be replaced by a gate item rather than merely rewritten.

**Item 1 (claims-summary pilot, select 1) — PASS.** Decidable from the stem, B is uniquely correct,
rationale addresses each distractor, and it lands the domain's most examinable pattern. *Optional
hardening:* A is transparently wrong, so the item is easier than professional level. Replace A with
"expand to all claims but require human review of every summary for the first month" — attractive,
defensible-sounding, and loses because it substitutes a labor control for a measured promotion
criterion and produces no evidence about the production distribution.

**Item 2 (97% accuracy clause, select 1) — PASS WITH FIX.** C is correct and the concept is core, but
B and D are throwaways and A is the only real competitor, putting difficulty below professional.
**Required fix:** replace D ("zero hallucinations," already the stuff of §3.2 row 5 and archetype 2, so
it teaches nothing new here) with a genuinely attractive wrong answer: "Put availability and latency in
the contract as the only SLAs and handle quality as a non-binding internal SLO." That is what many
architects actually do, and it loses because the stakeholder's need for a *quality* commitment can in
fact be met falsifiably against a disclosed eval set — refusing to commit at all forfeits the one
quality guarantee that is honest.

**Item 3 (which discovery question changes the architecture, select 1) — REWRITE.** Tests the right
thing; the distractors disqualify it. `"What color scheme should the refund confirmation email use?"`,
`"Which project management tool does the team use?"` and `"How many engineers are on the build team?"`
are not discovery questions at all — they are tells, and the item is answerable without reading the
stem. Professional difficulty requires all four options to be legitimate discovery questions of
*differing architectural leverage*. **Required fix:** keep B (reversibility of an incorrect refund,
which gates mandatory HITL) and replace the other three with questions that change *parameters* rather
than *architecture*: peak concurrency at month-end (changes capacity and caching, not the pattern);
the distribution of refund values (changes a threshold, not the pattern); which CRM holds the order
history (changes the connector, not the pattern). Rationale then explains the distinction, which is
the actual teachable point and is currently nowhere in the chapter (see the missing-question-bank
finding).

**Item 4 (handoff artifacts, select 2) — REWRITE.** `"The original brainstorming notes from the kickoff meeting"` and `"A copy of the vendor's marketing deck used to sell the project internally"` are jokes;
nobody at professional level picks them. **Required fix:** make it select 3 and use the three
load-bearing Claude-specific artifacts — the runbook, the RACI naming exactly one Accountable party for
the quality SLO and prompt/model change approval, and the prompt/model change log with the location and
version of the standing eval set — against distractors that are plausible documentation but not
operationally load-bearing: the eval report from the pilot gate (real evidence, but point-in-time and
superseded by the standing suite), a recorded walkthrough of the demo, and a list of prompts tried and
discarded during development. That version is answerable only by someone who understands which
artifacts a *running* system depends on.

**Item 5 (program director, no humans in the loop, select 1) — PASS WITH REQUIRED FIX.** This is the
hostile-stakeholder item, and the flagged trap is *mostly* avoided: C is a specific architectural move
(risk-tiered autonomy with a gated expansion path), not "communicate better." Keep the item.
**Required fix:** the rationale for B rests on stakeholder temperament — `"likely to be rejected by a stakeholder already skeptical of 'AI vendors wanting more review'"` — which is not decidable from the
stem and violates the domain's own discipline (see P8). Re-anchor it on capacity allocation: blanket
manual review of every permit spends finite reviewer capacity on the reversible low-risk tier, so
review of the public-safety tier degrades to a rubber stamp. Also strengthen A's rationale from
`"unmanaged liability"` to the architectural failure: it commits to an SLA the design cannot honestly
meet, because no eval set covers the permit types the system has not seen.

**Item 6 (which statement about ADRs is correct, select 1) — REWRITE.** Definitional recall with no
scenario, in violation of AGENT-BRIEF §3.9 ("scenario stem, no trivia") and of the chapter's own line
18. The correct answer C also telegraphs itself by being the longest and most qualified option — a
classic tell. **Required fix:** convert to a scenario: a team is reversing a documented long-context
decision in favor of RAG eighteen months after ADR-014 recorded it, because the cost profile changed
with a model version. Options: write ADR-031 recording the new decision and mark ADR-014 superseded
(correct); edit ADR-014's Decision section to reflect current practice; open an RFC and skip the ADR
because the decision is already made; add a note to the architecture document's decisions section. That
tests immutability, supersession, and the RFC/ADR boundary at once, on a realistic trigger.

**Item 7 (C4 versus arc42 discriminator, select 1) — REWRITE OR CUT.** The weakest item in the set.
It is definitional, and `"C4 is for regulated industries; arc42 is for unregulated industries"`,
`"C4 replaces the need for any written documentation"` and `"arc42 is only used for microservice architectures"` are not plausible to any candidate who has heard of either — the correct answer is
identifiable by elimination alone. **Recommendation:** cut it and spend the slot on the lifecycle-gate
item the chapter needs (see the Objective 5 BLOCKER). If retained, convert to a scenario in which an
external auditor, a newly hired engineer, and an executive sponsor each need something within the same
week, and the candidate must select what is produced for whom — which tests §3.1's actual
discriminator (audience and durability) rather than the names of two frameworks.

**Item 8 (sourcing the first eval set, select 1) — PASS WITH FIX (overlap).** C is correct and well
rationalized. Two issues: the stem as written is a Domain 4 item (eval-dataset design), and `"20-50"`
reads as doctrine when the dossier's own open question (dossier line 152) concedes no source fixes a
minimum. **Required fix:** reframe the stem around the Domain 6 hook — the eval set is about to be used
as the promotion gate a stakeholder will sign, so what must be true of it — and soften the numeric
range to "a small set (order of tens) drawn from real development checks, known failure modes, and the
support queue," so the item does not assert a threshold the sources do not support.

**Item 9 (moving from 100% review to sampled review, select 2) — BLOCKER, REWRITE.** The item has no
single defensible answer set because option A contradicts the chapter's own discriminator. §3.4 line
104 states: `"the axis is reversibility and blast radius, not volume or executive preference. High volume is a reason to move from 100% review toward *sampled* review with a feedback loop — it is never on its own a reason to remove review from irreversible actions."` The item's key then accepts A
(`"Review volume has exceeded human review capacity"`) as a standalone legitimate reason and its
rationale calls capacity `"architecture-relevant"`. A candidate who learned §3.4 correctly rejects A and
has only one answer for a select-2 item. **Required fix:** keep B (reversible and low-blast-radius
actions) as one correct answer and make the second correct answer the *precondition* the chapter
already teaches — a representative sampling scheme exists with a documented path from sampled failures
into the eval set — then demote volume pressure to a distractor alongside the executive-request and
headcount options, with the rationale explaining that capacity pressure is a trigger to *redesign* the
review posture but never on its own a justification for reducing it. That version is consistent with
§3.4 and is a harder, better item.

**Item 10 (re-run evals after a model upgrade, select 1) — PASS.** B is correct, the concept is central
(model/prompt changes are releases), and the rationale handles each distractor. Two refinements: the
stem says the upgrade shipped `"last week"`, so the strongest answer arguably includes reverting or
freezing further changes until re-validation — either tighten the stem to "we are about to upgrade" or
extend B to name the freeze. And A/C/D are weak; replacing one with "run an A/B test in production and
compare user thumbs-up rates between versions" would raise difficulty materially, since it is
attractive, superficially empirical, and loses because it exposes users during validation and
substitutes a weak indirect signal for a graded eval.

---

## Must preserve

The editor must not delete any of the following while making the fixes above.

1. **Line 12 and §1's positioning.** `"This domain does not test writing skill or interpersonal style. It tests whether you know the named, established artifact or technique for a given moment in a project's life"` — this single sentence is what keeps the chapter out of the platitude trap, and the
   six distractor archetypes (lines 22-27) are the best-calibrated archetype list I would expect from
   this domain. Archetypes 2, 3, 4 and 6 in particular are recognizable in real item stems.
2. **§3.2, the SLA/SLO commitment table (lines 75-84).** The strongest single asset in the chapter.
   Six rows, an honest committable/not-committable column, a *mechanism* column, and a discriminator
   (line 84) that is genuinely decidable: "if it can be evaluated against a specific, disclosed,
   versioned dataset with a stated cadence, it is committable." Preserve verbatim apart from the P7
   fix to the fallback row.
3. **§3.5 (lines 106-114), eval gate vs. demo sign-off vs. calendar launch.** The "fixed-calendar
   launch" row — `"What it actually validates: Nothing about the system; it validates a date"` — is
   the sharpest line in the draft and the correct treatment of a real organizational pressure.
4. **§3.4's discriminator (line 104).** Reversibility and blast radius as the axis, volume as a reason
   to change the review *shape* and never to remove review. Item 9 must be brought into line with
   this sentence, not the other way round.
5. **§7 Exam-day heuristics (lines 181-187), all seven.** Every one is an actual tiebreaker rather than
   a restatement: artifact matched to durability and audience; quality is a band with an error budget,
   never a promised percentage; a demo is feasibility evidence, not readiness evidence; reframe 100%
   automation rather than answering yes or no; discovery answers precede pattern and model selection;
   Accountable is exactly one name; model and prompt changes are releases. This section alone would
   move a borderline candidate.
6. **Scenarios 4.2, 4.3, 4.4 and 4.7.** All four are decidable from stated constraints, all four have
   real "what would change the answer" clauses that turn on a named constraint (an adjudicated note
   corpus; a 24-hour undo window; the absence of a low-risk permit tier; near-zero report volume), and
   4.3 and 4.4 are exactly the over-promised-pilot and hostile-stakeholder scenarios done right — the
   answers are architectural and process moves, not "communicate better."
7. **§5's failure-mode table structure and rows 1, 3, 4, 7, 8.** Symptom → cause → first thing to check
   → fix, with the checks genuinely diagnostic (`"Check the eval set's last-updated date vs. recent production samples"`, `"Check whether the eval gate re-ran post-upgrade"`). Row 4 — an executive
   expecting near-100% accuracy traced to a missing agreed baseline — is a particularly good
   cause-attribution.
8. **§6's anti-pattern names and their looks-right reasoning**, especially "the one eval to rule them
   all," "verbal SLA," and "silent scope creep in agentic projects." Convert the format to a table;
   keep every name and every reason.
9. **The near-absence of platitudes overall.** Nine entries in a 5,500-word soft-skills chapter is a
   result. Any addition made in response to this review must meet the same bar, and the editor should
   reject any new sentence that would survive unchanged in a deck about a non-LLM system.

---

## Coverage matrix

| Objective | Covered adequately? | Evidence and gap |
|---|---|---|
| 1. Conduct structured discovery and requirement gathering | **Partial** | Present: §2 concepts (QAW/mini-QAW lineage line 35, JTBD line 37, MoSCoW line 39, baseline line 41), §3.3 prioritization fit, §4.1 and §4.5, §5 rows 2 and 4, Items 3 and 8. Gap: the dossier's discovery question→architectural-consequence table (dossier lines 13-26) is absent; the "should not be an LLM use case" discriminators and kill criteria (dossier lines 27, 29) are absent; the accuracy-adjective-to-criterion conversion is asserted and never demonstrated; Item 3 tests the missing table with tell-laden distractors. |
| 2. Communicate architectural decisions and trade-offs | **Partial** | Present and strong on artifact selection: §2 (ADR line 43, C4/arc42 line 45, RFC line 47), §3.1 table with discriminator, §6 "recommendation-only slide," §7 heuristic 1, Items 6 and 7. Gap: the audience-tailoring rule (what to foreground for exec vs. security/legal vs. engineering, substance unchanged — dossier line 47) is absent, which leaves the "how do you present this to whom" item type unanswerable; the "security and operational excellence are generally not traded away" discriminator (D06-S15) is absent; the ADR template with Claude-specific Context fields is dropped; Items 6 and 7 are trivia rather than scenarios. |
| 3. Manage stakeholder feedback loops and expectation alignment (including SLAs) | **Yes — the chapter's strongest objective** | §2 (SLI/SLO/SLA/error budget line 49, eval gate line 51), §3.2 commitment table, §3.5 promotion criteria, §4.2 SLA negotiation, §4.3 over-promised pilot, §4.4 100%-automation stakeholder, §4.7 feedback-loop ownership, §5 rows 1/3/4/7/8, §6 "verbal SLA" and "one eval to rule them all," §7 heuristics 2/3/4/7, Items 1/2/5/9/10. Gap: error-budget mechanics for a *quality* SLI stated only by analogy; the degradation ladder compressed to one cell; "confidence signal" undefined; no method for deriving a threshold; "production-representative sample" never defined. |
| 4. Document architectures and provide implementation guidance | **Partial** | Present: §2 (ADR, C4/arc42, runbook line 55), §3.1 five-artifact selection table, §4.6 handoff documentation set, §6 "ADR graveyard," §7 heuristic 1, Items 6 and 7. Gap: §3.1 omits the eval report and the prompt/model change log — the two artifacts specific to a Claude system; the second clause of the objective, "provide implementation guidance," has no coverage at all (no integration/implementation guide for a downstream consuming team, no prompt/input contract, no statement of where the eval set and threshold live so a consumer can tell whether their use case is inside the tested distribution); no ADR template. |
| 5. Support lifecycle phases (discovery, design, handoff, monitoring, iteration) | **No** | Claimed in §9 (line 274). Actually present: one promotion gate (§3.5), ownership models (§3.6), one handoff scenario (§4.6), one monitoring/iteration scenario (§4.7), Items 4 and 10. Absent: any statement of the lifecycle phases (the phases appear only in the front-matter restatement at line 10); any gate-criteria table, although eight gates with pass conditions are already written in the dossier (lines 108-118); the handoff checklist as an artifact, including the token/cost owner and pre-declared re-eval triggers (dossier line 81); deprecation and retirement entirely. No practice item turns on a gate criterion. This is the BLOCKER. |

---

## Sources

No external sources were consulted for this review. All citations above refer to the researcher's
existing `D06-S##` IDs as they appear in the dossier and draft, or to `AGENT-BRIEF.md` and the exam
guide, both supplied in-task. No new `D06-R##` rows are required.
