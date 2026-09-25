# AGENT BRIEF — Claude Certified Architect – Professional (CCAR-P) prep course, Track B

**Read this file in full before doing your task.** It is the shared contract for every agent working on
this course. The authoritative exam guide is `../claude-arch-professional-guide.md` (read it too).

## 0. Context you must not get wrong

- Today's date: **2026-09-24**. Exam guide version 1.0, **effective July 2026**, exam code **CCAR-P**.
- Exam: 63 items, 120 minutes, multiple-choice + multiple-response, proctored (Pearson VUE),
  scaled score 100–1000, **cut score 720**, $175 USD, credential valid 12 months.
- Scoring is **criterion-referenced** (fixed standard, not a curve). Domain percentages on the score
  report are diagnostic only; pass/fail is on total scaled score.
- **Model lineup: read `VERIFIED-FACTS.md` in this folder. It is canonical and overrides this brief.**
  The current lineup verified 2026-09-24 against platform.claude.com is **Claude Fable 5.1, Claude Opus 5.5,
  Claude Sonnet 5, Claude Haiku 4.5**, with Opus 5.5 the docs' default recommendation and Opus 5 now legacy.
  `VERIFIED-FACTS.md` also carries the **`effort` parameter / adaptive-thinking** model that replaces the old
  `budget_tokens` extended-thinking story, the per-model cache-read economics, and the Covered-Models /
  zero-data-retention interaction. Do NOT present Claude 3.x/4.x, or Opus 5, as "current". If you name a model, a price,
  a context-window number, a rate limit, or an API parameter, it must be **verified against primary
  Anthropic documentation in this session** — either by invoking the local `claude-api` skill (via the
  Skill tool, skill name `claude-api`) or by fetching `https://docs.claude.com/...` / `https://www.anthropic.com/...`.
  Your training memory is not a source. Anything you cannot verify must be marked `[UNVERIFIED]`.
- Never invent product features, parameter names, endpoint names, limits, or "official" Anthropic
  guidance. A fabricated detail in prep material is worse than an acknowledged gap. Prefer durable,
  architectural statements over volatile numbers; when a number matters, cite it with a date.

## 1. Who this course is for

The exam's **minimally qualified candidate (MQC)**: a mid-to-senior solution architect / AI engineer /
tech lead with 3+ years systems architecture, 6+ months production LLM experience, who translates
business problems into Claude-based architectures and owns the trade-off conversations with security,
legal, and executive stakeholders.

Therefore the course must operate at **professional / architect altitude**:

- The reader already knows what a prompt and an API call are. Do not teach basics for their own sake.
- The exam tests **judgment under competing constraints**, not recall. Almost every item is
  "which is *best/most likely/first*" with several defensible-looking options.
- So: for every concept, the material must state **the decision it supports, the alternatives, the
  trade-off axes (accuracy, latency, cost, safety, maintainability, blast radius, governance), and the
  signal that tells you which branch to take.** "It depends" is never an acceptable stopping point —
  say what it depends *on* and give the discriminator.

## 2. Exam blueprint (weights drive depth — spend effort proportionally)

| # | Domain | Weight |
|---|--------|--------|
| 1 | Solution Design & Architecture | 17% |
| 2 | Claude Models, Prompting & Context Engineering | 13% |
| 3 | Integration | 19% |
| 4 | Evaluation, Testing & Optimization | 16% |
| 5 | Governance, Safety & Risk Management | 14% |
| 6 | Stakeholder Communication & Lifecycle Management | 14% |
| 7 | Developer Productivity & Operational Enablement | 7% |

Objectives per domain are listed verbatim in the exam guide, Section 6. **Every objective must be
covered explicitly and be traceable** — each chapter carries an objective-coverage table.

## 3. Required chapter structure (course/NN-*.md)

Each domain chapter must contain, in this order:

1. **Front matter** — domain name, weight, approx. item count out of 63, objective list.
2. **Exam-relevance framing** — what this domain actually tests, and the 3–6 recurring item patterns
   ("distractor archetypes") used in it.
3. **Core concepts** — each concept written as: definition → why an architect cares → *the decision it
   drives* → common misconception. Concepts must be defined precisely enough to be usable, and each
   one names its alternatives.
4. **Trade-off analyses** — the heart of the chapter. Comparison tables with explicit axes and a
   "choose A when… / choose B when…" discriminator. Minimum 4–6 substantive comparisons per chapter
   (more for domains ≥16%).
5. **Worked scenarios** — 4–8 realistic, industry-flavored situations (financial services, healthcare,
   retail, gov, etc.) with: situation → constraints → candidate approaches → recommended approach →
   *why the plausible alternatives lose* → what would change the answer.
6. **Failure modes & diagnostics** — symptom → likely cause → first thing to check → fix. Written as a
   table so it doubles as a triage reference.
7. **Anti-patterns** — named, with the "looks-right" reasoning that leads people into them.
8. **Exam-day heuristics** — the tiebreakers for this domain (e.g. "least privilege = remove the
   capability, not log it"; "confident-but-wrong after a data refresh = retrieval, not the model").
9. **Practice items** — 8–12 exam-style items (mix of single- and multiple-response, with the item
   stating how many to select), each with a rationale that explains **why each distractor is wrong**.
   Match the cognitive level of the guide's Section 8 samples: scenario stem, no trivia.
10. **Objective-coverage table** — objective → where covered in this chapter.
11. **Sources** — every non-obvious claim, with URL and access date. Mark `[UNVERIFIED]` items clearly.

Style: dense, declarative, skimmable. Tables and comparisons over prose. No filler, no marketing
language, no "in today's fast-moving AI landscape". American English. Markdown, ATX headings.
Target 3,500–6,000 words per chapter (scale with domain weight). Code/config snippets only when they
carry architectural meaning.

## 4. Roles and file conventions

All paths are relative to this folder (`prep-course-track-b/`). `NN` is the zero-padded domain number
and `slug` is the domain slug given in your task prompt.

| Role | Writes | Reads |
|------|--------|-------|
| Researcher | `research/NN-slug-dossier.md` + `drafts/NN-slug-draft.md` | exam guide, primary docs, web |
| Content reviewer | `review/NN-slug-content-review.md` | dossier + draft |
| Validator | `review/NN-slug-validation.md` | dossier + draft + primary sources |
| Adversarial reviewer | `review/NN-slug-adversarial.md` | dossier + draft |
| Editor | `course/NN-slug.md` | draft + all three reviews |

**Do not edit another role's file.** Reviewers never rewrite the draft; they report. The editor is the
only role that produces `course/`.

Each reviewer file must open with a verdict block:

```
VERDICT: SHIP | SHIP-WITH-FIXES | MAJOR-REWORK
Top 3 must-fix items:
1. ...
```

and then list findings as `[SEVERITY] location — problem — required fix`, severity in
`BLOCKER | MAJOR | MINOR | NIT`. Findings must be specific and actionable; "add more detail" is not a
finding. Reviewers must also state what is **good and must be preserved**, so the editor does not
delete strengths.

## 5. Hard rules for everyone

1. Cover the objectives; do not drift into adjacent topics that the blueprint does not measure.
2. Never reproduce or claim knowledge of live exam items — everything is original, written against the
   published objectives. The guide's own Section 8 samples may be discussed as style references.
3. Prefer well-established, documented approaches; where the field is genuinely unsettled, say so and
   give the decision framework rather than a false certainty.
4. Verify before asserting. Flag `[UNVERIFIED]`. Contradictions between sources get surfaced, not smoothed.
5. Write files with the Write tool; **return at most 200 words** to the orchestrator (what you wrote,
   headline findings, open risks). Long output in the return value is wasted — the files are the deliverable.
6. No emoji. No "As an AI". No hedging filler.

## 6. Reference tracking (mandatory)

Every agent that consults an external source records it. Sources are a first-class deliverable of this
course, not a footnote: the consolidation session needs to know exactly what each claim rests on.

**Researchers** additionally write `research/NN-slug-sources.md` as a table with one row per source and
**no prose**, using exactly these columns:

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|

- `ID`: `DNN-S01`, `DNN-S02`, … (e.g. `D03-S04` = domain 3, source 4). Stable — cite these IDs inline.
- `Type`: `anthropic-docs | anthropic-blog | anthropic-cookbook | vendor-docs | standard/regulation |
  academic | practitioner-blog | community | exam-guide | other`.
- `Trust`: `primary` (Anthropic/standards body official), `secondary` (reputable third party),
  `low` (unverified, community, or content that may be SEO/AI-generated). Say it honestly.
- `Used for`: the specific claim(s) it backs.

**Validators** record any source they used to check a claim in their own file, same table format, with
IDs `DNN-V01`…, and state for each verified claim: `CONFIRMED | CONTRADICTED | NOT-FOUND`.

**Reviewers and adversarial reviewers** cite source IDs when disputing a claim; if they introduce a new
source, list it at the end of their file in the same table shape (`DNN-R01…`, `DNN-A01…`).

**Editors** keep inline citations in the finished chapter as `[D03-S04]` style tags, and end the chapter
with a Sources section resolving every ID used, plus an explicit list of remaining `[UNVERIFIED]` claims.

Also flag, in a `## Prep-material landscape` section of the dossier, any third-party CCAR-P prep
material you find (courses, question banks, blog write-ups), with a trust judgment. This certification
is new (effective July 2026), so expect low-quality or AI-generated "braindump" content — note it, mark
it `low` trust, and never copy from it; the course must stand on primary sources plus reasoning.

## 7. Systemic defects found across chapters (added mid-project — every editor and item writer must fix)

Independent reviewers found the same defects in chapter after chapter. Treat these as standing rules, not
per-chapter findings.

1. **The answer-length tell.** The keyed answer was the longest, most-qualified option in most items across
   multiple chapters (Domain 1: all 12; Domain 5: 6 of 12, some keys 3–4× their distractors' word count).
   This is a validity defect: a test-wise candidate scores without reading the stem. **Equalize option
   length and qualification density.** Distractors must be as specific and as hedged as the key.
2. **Keyword-reflex items.** Items where a trigger word in the stem selects the answer ("PHI ⇒ BAA",
   "latency ⇒ Haiku", "many tools ⇒ tool search", "SLA ⇒ error budget", and any set where most keys share a
   giveaway word such as "eval"). These train the wrong reasoning and fail against well-written items.
   The trigger must be something the candidate has to *recognize*, not something the stem announces.
3. **Giveaway stems.** Do not name the regulatory or architectural trigger in the stem ("data containing
   PHI", "CUI-level", "legally significant"). Describe the situation and make classification part of the task.
4. **Items that re-test a worked scenario.** An item that repeats a scenario's exact vertical and lesson
   measures recall of our examples, not transfer. Change the vertical, the constraint, or the failing axis.
5. **Volatile-dependency items.** No item may hinge on recalling a price, model name, parameter default,
   spec revision, or measured benchmark figure. Those date and are unfair. Test the decision procedure.
6. **Internal contradictions.** Prose contradicting its own table, or a stated rule contradicting a practice
   item's key, was the single worst defect found (Domains 5 and 6 both had one). Before shipping a chapter,
   cross-check prose against tables, tables against each other, and every heuristic against every answer key.
7. **Dishonest coverage tables.** Do not credit an objective to a scenario that does not actually turn on it.
   An honest "thin here" beats a padded matrix — the consolidation session needs to know where the gaps are.
8. **Unconditioned numbers.** Every figure carries its baseline, its conditions, and its source, or it is cut.
   Teach the mechanism so an item with different numbers is still answerable.
