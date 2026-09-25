# Adversarial Review — Domain 6: Stakeholder Communication & Lifecycle Management (14%)

Target: `drafts/06-stakeholder-communication-lifecycle-draft.md` (read in full)
Against: `claude-arch-professional-guide.md` §6 objectives + §8 sample items/rationales; `research/06-stakeholder-communication-lifecycle-dossier.md`; `AGENT-BRIEF.md`

```
VERDICT: MAJOR-REWORK
Top 3 must-fix items:
1. Practice Item 9 is keyed against the chapter's own discriminator. §3.4 says "high volume ...
   is never on its own a reason to remove review"; Item 9 then keys "review volume has exceeded
   human review capacity" as a legitimate reason. A candidate who learned §3.4 correctly answers
   Item 9 wrong. Fix the item, not the discriminator — and add the missing fourth posture
   (risk-tiered review: 100% on the high-risk slice, sampled on the rest), which is the answer a
   real exam is most likely to key and which the chapter's 3-row table cannot express.
2. §7 bullet 2 ("never a promised percentage") contradicts §3.2 row 3 (">=92% pass rate on eval
   suite v7" = committable). As written the chapter installs a keyword trap — "option contains a
   percentage therefore wrong" — that its own best content refutes. Restate the rule as a rule
   about the *domain of quantification*, not about numbers: a number over a disclosed, versioned,
   sampled input domain with a re-measurement trigger is committable; the same number over an
   unbounded input domain is not.
3. The draft dropped the three dossier artifacts that carry its two thinnest objectives: the
   discovery question -> "what it changes" table (Objective 1), the 8-row lifecycle gate checklist
   (Objective 5), and the audience-tailoring rule (Objective 2). It also never covers
   deprecation / model-retirement / forced migration, despite claiming Objective 5 coverage.
   Candidates are left with artifact-naming where the objectives ask for discovery reasoning,
   lifecycle gating, and trade-off *communication*.
```

Scope note for the editor: §1 (distractor archetypes), §2, §3.1–§3.2, §3.4–§3.6 and §6 are largely
salvageable and in places excellent. The rework is concentrated in §7 (heuristics, which need
qualifiers or are actively wrong), §8 (7 of 10 items need rebuilding), §3.3 (weakest and most
off-objective section), and the missing content listed above.

---

## Attacks that landed

### Self-contradiction and installed keyword traps

**[BLOCKER] §8 Item 9 vs. §3.4 discriminator — the chapter grades its own best reasoning as wrong.**
§3.4 states: "the axis is reversibility and blast radius, not volume or executive preference. High
volume is a reason to move from 100% review toward *sampled* review with a feedback loop — it is
never on its own a reason to remove review from irreversible actions." Item 9 then keys A ("Review
volume has exceeded human review capacity") *and* B as the two "legitimate reasons," with a rationale
calling both "architecture-relevant." Counter-scenario: a candidate faces a stem where a hospital's
medication-reconciliation assistant is at 100% pharmacist review, volume has tripled, and the
actions (order changes) are not reversible once dispensed. The §3.4 discriminator gives the right
answer — add capacity or tier the review, do not sample. Item 9 trains the opposite instinct, and
because no third risk-based option exists in the option set, the candidate is forced to affirm the
capacity argument to score the item.
*Required fix:* rewrite as a select-1: "Which finding, **on its own**, justifies moving from 100%
review to sampled review?" with the reversibility/blast-radius option correct and capacity,
executive request, headcount cost, and "the pilot had no errors" as distractors. Then add a separate
select-2 on *what must accompany* a capacity-driven change (risk-tiered sampling, stratified sample
design, error-budget floor).

**[BLOCKER] §7 bullet 2 vs. §3.2 row 3 — "never a promised percentage" is refuted three tables
earlier.** §3.2 correctly makes ">=92% pass rate on eval suite v7, reviewed weekly" committable.
§7 then says "never a promised percentage ... If an option promises a fixed accuracy number against
arbitrary future input, it's wrong regardless of how confident it sounds." The second clause is
correct; the headline is not, and the headline is what a candidate memorizes. Counter-scenario: a
federal RFP requires a numeric quality KPI with liquidated damages before award; a competent
architect commits "≥94% field-level extraction accuracy measured quarterly on a 500-document
stratified sample drawn from the agency's own corpus, with a re-measurement trigger on any model
version change and an out-of-distribution exclusion for document classes absent from the sample."
That is a promised percentage in a contract and it is the right answer. A candidate trained on the
§7 headline eliminates it.
*Required fix:* replace the §7 bullet with: "A quality commitment is committable when the input
domain it is quantified over is disclosed, versioned and sampled, and when a re-measurement trigger
is attached. Numbers are not the problem — unbounded input domains are. Reject 'X% on any input' and
'no hallucinations'; accept 'X% on corpus v7, re-measured on model change.'"

**[MAJOR] §8 keyed-answer distribution rewards the word "eval," not reasoning.** Five of ten keyed
answers (Items 1, 2, 8, 9, 10) contain "eval set / eval suite / eval gate." A candidate can score
this practice set at 100% by selecting the option containing "eval" without reading the stem. That
is the exact "keyword pattern-matching over reasoning" failure the exam punishes — a real item bank
will put "eval" in distractors ("run the existing eval suite again," "expand the eval set to 5,000
synthetic cases," "have the vendor's eval team certify it").
*Required fix:* at least three items must have an eval-flavored distractor that loses — e.g. an item
where the correct answer is "define the baseline first, because the eval threshold cannot be set
without it" against a distractor "build the eval set now"; and an item where the correct answer is
"narrow the scope" against a distractor "raise the eval threshold."

**[MAJOR] §3.6 discriminator claims knowledge of live exam behavior — AGENT-BRIEF §5 rule 2
violation.** "the exam will never accept 'the team is responsible' as correct when a RACI-style
question is asked." Also §3.3 ("are both the 'looks-right, is-wrong' answer on this exam") and §3.5
("are never the *architectural* answer"). The brief forbids claiming knowledge of live items; these
sentences assert it. They are also pedagogically corrosive: they teach elimination-by-phrase.
*Required fix:* convert each to a claim about the *concept* ("an accountability record that does not
resolve to a single party cannot support an incident retrospective or an audit finding") and drop
every "the exam will/never" construction.

### Heuristics that misfire

**[MAJOR] §2 "ADR ... immutable" and §8 Item 6 option B — the chapter's own template contradicts the
immutability claim.** §2 and Item 6 treat "edited in place when superseded" as a violation. But the
dossier's own ADR template (carried from MADR) lists `Superseded by ADR-MMM` as a Status value —
which is written into the original ADR after the fact, i.e. an in-place edit. Immutability applies
to Context and Decision, not to Status. A pedantic, correct candidate can defend B.
*Required fix:* state the rule precisely: "the Context and Decision of an accepted ADR are never
rewritten; only Status changes, to record deprecation or supersession." Then reword Item 6 option B
to "An ADR's Context and Decision should be rewritten when a later decision supersedes it."

**[MAJOR] "Always gate promotion on an eval" has no emergency or forced-migration branch.** §7
bullet 7: "Model/prompt changes are releases. Any option that treats them as exempt from the eval
gate or SLO re-validation is wrong." Counter-scenarios: (a) a live prompt-injection exploit is
exfiltrating data through a tool; the correct action is to ship the mitigating prompt/tool-scope
change immediately with compensating controls (tool disabled, 100% review, feature flag, narrowed
authz) and run the gate inside a declared window; (b) the provider retires the pinned model version
in 10 days and the full suite takes three weeks of grader time; the correct action is a risk-targeted
subset re-run (the highest-severity and highest-traffic strata) plus a canary, not "block the
migration." Item 10 also assumes an unlimited eval budget and full-suite re-runs.
*Required fix:* add the boundary condition: "An eval gate may be bypassed only with (1) a named
approver accepting the risk in writing, (2) compensating controls that bound blast radius, and (3) a
declared deadline for the deferred gate run. A forced migration is re-validated against a
risk-stratified subset, not the full suite, with the coverage gap documented."

**[MAJOR] "Never a flat no" forecloses the correct answer when the use case is not automatable.**
§7 bullet 4: "never a flat yes or a flat no." Counter-scenario: the stakeholder wants autonomous
adverse-action denials on credit applications, or autonomous clinical diagnosis, where a licensed
human or a specific-reasons statement is legally required. "No, not as specified — here is the
narrowed scope that is lawful" *is* a flat no to the ask. Worse: the draft dropped the dossier's
entire "detecting a use case that should not be an LLM use case" and "kill criteria" material, so
"decline / recommend not building" never appears as a candidate option anywhere in the chapter — in
seven worked scenarios and ten items, zero have declining as a live option.
*Required fix:* restore the dossier's kill criteria as a §2 concept with its three discriminators
(deterministic auditable output required; low reversibility with no review capacity; no definable
baseline), add one worked scenario and one item where the correct answer is "recommend not building
this / route to a deterministic system," and requalify bullet 4 as "never a *reflexive* yes or no —
but a documented refusal is correct when a legal or licensure constraint makes the ask
unimplementable."

**[MAJOR] "Discovery answers come before pattern/model selection" misfires on the feasibility
spike.** §7 bullet 5 and archetype 5 ("the premature scope answer") make "pick a pattern before
discovery is settled" always the trap. Counter-scenario: a stakeholder cannot state an accuracy bar
in the abstract — nobody can say what "good enough" means for clause-flagging until they see
outputs. The correct first action is a time-boxed, production-dependency-free spike on 30 real
documents, used to make the accuracy conversation concrete. A candidate who memorized the absolute
eliminates "run a two-day bounded prototype on real samples to calibrate the accuracy bar with the
stakeholder," which is a very plausible keyed answer.
*Required fix:* qualify to *commitment*: "unanswered discovery questions gate production
architecture and any external commitment — they do not gate exploration. A spike with no production
dependency and no commitment attached is a legitimate discovery instrument."

**[MAJOR] "Accountable is exactly one name" is wrong for 24/7 systems and over-literal for audits.**
§7 bullet 6 and §3.6 row 3 demand "exactly one Accountable name." No single human is accountable for
a 24/7 quality SLO; what is named is one accountable *role* (service owner of record) resolved to a
human at any instant by a rotation and escalation path — which is what an auditor accepts.
*Required fix:* "exactly one accountable *role*, with a named current holder and a documented
rotation/escalation. 'The team owns it' fails because it names no role; 'the service owner of record,
currently J. Okafor, escalating to the platform director' passes." Otherwise a candidate
pattern-matching on the word "team" will eliminate "the platform team's service owner of record,"
which is correct.

**[MAJOR] §3.2's "safe" fallback row smuggles in exactly the unfalsifiable promise the table
condemns.** Row 6: "Falls back to human queue when confidence signal is low — Yes, behavioral
commitment, not a number." A Claude API response does not emit a calibrated confidence by default;
"low confidence" is undefined until someone builds and calibrates a detector. Counter-scenario: the
clause ships, the stakeholder reads it as "the system catches its own errors," and the first incident
is a confidently wrong output that never routed. This is the Verbal-SLA anti-pattern in contractual
clothing.
*Required fix:* the committable form is "cases flagged by <named detector> route to human review;
the detector's recall and the resulting abstention rate on eval set v7 are disclosed and
re-measured on model change." Add a sentence: a degradation commitment is only as falsifiable as the
signal that triggers it.

**[MINOR] "Document the decision in an ADR" has no significance threshold.** Nygard's criterion is
*architecturally significant*. Counter-scenario: a two-week internal throwaway with one maintainer
and a scheduled delete date — an ADR log is pure overhead and the correct answer is a comment in the
PR plus the sunset date on the ticket. Conversely, in a regulated QMS the document set is
*prescribed* (design-history-file / technical-documentation obligations), and choosing arc42 vs. a
decision memo is not the architect's free choice.
*Required fix:* add the threshold ("costly to reverse, or will be asked about by someone not in the
room") and the override ("unless a regulated QMS or the contract prescribes the artifact set").

### The "communicate better" cop-out

**[MAJOR] §5 row 6 — "Add security/legal as Consulted stakeholders during discovery" is earlier
engagement with no artifact.** Counter-scenario: a central security function with a ticket queue and
a six-week review SLA will not attend your workshop; the invitation is refused and the launch is
still blocked.
*Required fix:* the architectural answer is to make the review cheap and to start its clock early —
file the architecture-intake ticket at design time so queue time runs in parallel; submit a data-flow
diagram and a written data-classification/retention answer as the ADR's Context; and *reduce the
reviewable surface* (redact at the boundary, no PII in prompts, no new egress, retention off) so the
review has less to object to. "Invite them earlier" is the platitude; "shrink what they must approve
and pre-answer their questions in writing" is the fix.

**[MAJOR] §4.7 names an owner for a broken intake path and calls it solved.** The stated defect is
"reports are emailed to whoever answers first." The recommended answer (b) names an eval owner and
a cadence — but leaves the capture path as email. Counter-scenario: the new owner inherits an inbox;
six weeks later the backlog is the same size with one person's name on it.
*Required fix:* the load-bearing artifact is the capture mechanism: an in-product "this was wrong"
control that writes input, output, retrieved context, model/prompt version and reviewer note into a
triage queue with a required disposition field. The owner and cadence sit *on top of* that. Add
"instrument the feedback path before assigning it an owner" as a heuristic.

**[MINOR] §5 row 2 — "route new asks through a change process" is unspecified.** Name the gate: a
scope-change request is admissible only with (a) an eval case demonstrating the requested behavior,
(b) a reversibility/blast-radius answer for any new tool, (c) an error-budget impact estimate; and
the default disposition is the next release. Architecturally: freeze the tool manifest; new
capability = new tool = new authz scope = new review.

**[MINOR] §4.4 / Item 5 — "a documented path to expand autonomy as the eval track record
accumulates" is a platitude without a pre-registered criterion.** The exam will plausibly contrast
this with a quantified promotion rule. Supply one: "tier-2 permit types move to autonomous after N
consecutive decisions at >=X agreement with the human reviewer, zero severity-1 reversals, and
sign-off by the named accountable owner — pre-registered before the pilot, not judged after."

### Wishful process / org-maturity assumptions

**[BLOCKER] "Eval set sampled from real production inputs" collides with the chapter's own regulated
scenarios, and the collision is never named.** §2, §3.5, §5 row 1, §5 row 3, §4.3 and §4.7 all
prescribe production sampling into the eval set. §4.2 is ambient *clinical notes* and §4.6 is
privileged *legal* documents. Retaining those inputs for eval use is a PHI/privilege question with a
BAA, minimum-necessary, and retention answer attached — and in many deployments the vendor may never
see them. Two of the chapter's own prescriptions contradict each other and a candidate is given no
way to resolve it.
*Required fix:* add a degraded-mode row: when production inputs cannot be retained or exported —
(1) de-identify and hold the eval corpus inside the customer's compliance boundary, with the vendor
receiving only aggregate pass rates; (2) synthesize from the real schema and the real failure
taxonomy rather than from the real records; (3) use a customer-held blind eval the vendor never
sees; (4) if none is possible, the quality SLO must be stated over the proxy corpus with the
distribution gap disclosed. State explicitly that "sample production" is a default, not a
universal.

**[MAJOR] The eval gate assumes an eval platform, graders and labels most candidates will not
have.** No degraded mode anywhere.
*Required fix:* the minimum viable gate: 20–50 cases in a spreadsheet; a rubric; two independent
human raters on a 30-case calibration slice with inter-rater agreement reported; an LLM judge only
after it is calibrated against that slice. Where no ground truth exists, pairwise preference against
the incumbent process. Where no incumbent exists, a pre-registered rubric plus an outcome metric
measured in a canary.

**[MAJOR] §4.6's six-artifact handoff set assumes budget and a competent receiving team — and its
"what would change the answer" line explicitly refuses to think.** "*Changes the answer:* nothing
here changes it; this is a near-pure test of the documentation set itself." That is false confidence
in a section whose purpose is to teach what moves an answer. Counter-scenario: IT ops has no LLM
operating experience and no eval capability. Handing them an arc42 document does not make them able
to run the system; the correct answer is a bounded joint-operation period with a written exit
criterion (ops independently passes the eval gate and resolves one drill incident), or retaining the
function as a service, or buying managed support.
*Required fix:* state a minimum viable handoff (runbook + named accountable role + prompt/model
change log + eval set with threshold and a rehearsed rollback) and mark the architecture doc and ADR
log as back-fillable. Replace the "nothing changes it" line with the receiving-team-capability
condition.

**[MAJOR] The chapter assumes the architect has authority to set gates and refuse launches.** Most
MQCs advise; they do not hold release authority. Nothing in the chapter covers the most common real
situation: the business is launching over your objection.
*Required fix:* add the degraded-mode play — write the residual risk in one page, obtain the named
accountable executive's *written risk acceptance* (this is the artifact), and unilaterally reduce
blast radius within your own control (tool scope, rate limit, cohort size, kill switch, 100% review
on the irreversible slice). This is a highly testable pattern and the chapter has nothing on it.

**[MINOR] §3.6 and RACI assume someone will accept Accountable.** Degraded mode: if no owner can be
found, accountability defaults to the executive sponsor and that fact is recorded as a launch
blocker; simultaneously reduce autonomy so an unowned failure is bounded.

### Exam mismatch and blueprint drift

**[BLOCKER] Objective 5 ("support lifecycle phases") has no deprecation / migration content, and the
dossier's 8-row gate checklist was dropped.** The draft's lifecycle stops at "iteration." The
dossier had "Iteration → Deprecation: retraining/re-eval triggers defined in advance ... trigger a
scheduled review, not silent decay." For a *Claude* architect exam this is the highest-value
lifecycle content that exists: pinned model versions get retired, which forces a re-eval and a
migration plan on someone else's calendar. Nothing in the chapter prepares a candidate for a stem
about a deprecation notice, a version-pinning policy, or a sunset decision.
*Required fix:* restore the gate checklist as a table (it is the single most exam-usable artifact in
the dossier) and add a deprecation/migration subsection: version pinning vs. alias, the
notice-window-to-migration-plan sequence, risk-stratified re-eval, stakeholder communication of a
forced change the architect did not choose, and sunset criteria for the feature itself. Model names,
windows and policy specifics must be verified per AGENT-BRIEF §0 — flag to the validator, do not
write from memory.

**[BLOCKER] Objective 1 lost its reasoning content.** The dossier's nine-row discovery table
(question → what it changes if the answer is "high/hard") is exactly the "decision it supports +
discriminator" shape AGENT-BRIEF §1 demands. The draft compressed it into four words inside one §7
bullet. What remains under Objective 1 is technique names (QAW, JTBD, MoSCoW) — vocabulary, not
reasoning. A candidate facing "which discovery answer most changes the architecture" has memorized
"reversibility" and nothing else.
*Required fix:* restore the table verbatim and add one item that discriminates among *four
legitimate* discovery questions by what each one gates.

**[MAJOR] Objective 2 is covered as artifact-selection only; the dossier's audience-tailoring rule
was dropped.** The dossier's concrete rule — to an executive, lead with the decision and the cost of
the rejected alternative in dollars/time/risk; to security/legal, lead with the pillar that was *not*
traded plus residual risk; to engineering, lead with the mechanism and the ADR; the substance does
not change across audiences, only which row is foregrounded — is the only content in either document
that teaches *communicating* a trade-off rather than *filing* it. The objective says "communicate
architectural decisions and trade-offs." Restore it, and add an item where all four options contain
the same true trade-off framed for different audiences and the stem names the audience.

**[MAJOR] §3.3 (MoSCoW vs. 2x2 vs. RICE) is the weakest section, is product-management trivia, and
omits the only two axes this chapter otherwise argues matter.** A "which technique" item rewards
recall, and the "weak fit" claims are unsourced convention. Worse, a value × feasibility 2x2 omits
*evaluability* (can we tell whether it worked?) and *reversibility* — the two axes the rest of the
chapter correctly treats as decisive.
*Required fix:* cut §3.3 to a three-line note and replace it with an LLM-specific qualification
screen: value × feasibility × evaluability × reversibility, with "no definable baseline or eval ⇒
not yet a project" as the discriminator. This also serves the restored kill criteria.

**[MAJOR] Items 6, 7 and 10 are below the §8 sample cognitive level.** All three guide samples are
scenario stems with genuinely tempting distractors (logging and confirmation prompts as
least-privilege decoys; few-shot relocation as a caching decoy). Item 6 is "which statement about
ADRs is correct," Item 7 is "C4 vs. arc42 definitions," Item 10 is answerable from the word
"release." The chapter's own §1 says items are "almost never trivia ('what does RACI stand for')" —
then supplies three trivia items.
*Required fix:* recast each as a scenario. Item 7 example: "A security reviewer must assess trust
boundaries and third-party data egress before a HIPAA audit. Which do you produce?" with a
right-framework-wrong-zoom-level distractor (C4 code-level diagrams) and a right-artifact-wrong-
audience distractor (the ADR log). Item 10 example: the provider retires the pinned version in ten
days and full-suite grading takes three weeks — now the answer requires reasoning about
stratification and compensating controls.

**[MAJOR] Item 8 is Domain 4 content (AGENT-BRIEF §5 rule 1: do not drift).** "How do I source my
first eval set" is verbatim Domain 4's "design evaluation datasets and test frameworks." Spending
one of ~9 Domain 6 items on it costs coverage of discovery-with-conflicting-stakeholders,
RFC-vs-ADR, deprecation, or written risk acceptance — all of which currently have zero items. The
"20–50" figure is also a recall trap presented as doctrine (validator: confirm D06-S03 states a
range and that it is framed as a starting heuristic, not a standard).
*Required fix:* replace with a Domain 6 item. If eval content must stay, make the *stakeholder* the
subject: who signs the threshold, who owns the set, what the stakeholder is told when the set is
refreshed and the number moves.

**[MINOR] §3.1 sends a compliance auditor an arc42 document — plausible and wrong.** A SOC 2 / HIPAA
auditor asks for control evidence mapped to a framework: data-flow diagram, data classification and
retention configuration, subprocessor list, access-control evidence, an approved-change record. An
arc42 prose document is architecture context, not evidence. Counter-scenario: the auditor's request
list arrives, arc42 answers none of its line items, and the finding is "insufficient evidence of
change control."
*Required fix:* split the row — "new engineer / cross-team engineering audience ⇒ C4 + arc42";
"compliance auditor ⇒ control-evidence package (DFD, classification/retention config, change log,
access evidence), with C4 context diagram as an attachment." Also add the eval report to §3.1; the
dossier has it and the draft's own §4.6 lists it.

**[MINOR] §2 "Structured discovery" and §3.1 carry an implicit greenfield / single-aligned-
stakeholder assumption.** No scenario in the chapter has two stakeholder groups in genuine conflict
— the hardest and most testable case. The nearest thing (§4.4's "hostile stakeholder") is one person
to be managed, not two legitimate requirements in collision. The chapter's own prescriptions produce
one such collision (security wants zero prompt retention; the eval owner needs retained production
inputs) and never resolve it.
*Required fix:* add a worked scenario with two irreconcilable stakeholder requirements, where the
answer is a documented, signed trade-off with a named decider — not a synthesis that makes both
happy.

**[NIT] US/English-corporate norms are assumed.** "One-page memo," a single named accountable
individual, and the architect negotiating scope directly with a budget holder are not universal. In
several EU jurisdictions an internal rollout that changes how staff work can require works-council
consultation — a real lifecycle gate absent from a lifecycle chapter; and in public procurement the
scope may be fixed by the SOW so §4.4's "reframe the ask" may be contractually unavailable without a
formal modification. *Validator question:* confirm before asserting any specific statute. At minimum
add "and any jurisdiction-specific consultation body" to the discovery stakeholder list.

---

## Item-by-item adversarial re-solve

**Item 1 (curated 20-case pilot → expand).** Keyed B. Strongest alternative: none of the offered
options beats B, because the two strongest real alternatives are absent — a shadow/canary
deployment on live claims (which serves leadership's one-week timeline *and* generates the
production sample B needs) and a segment-limited launch at 100% review. C (cost) and D (disclaimer)
are non-credible at MQC level, so the item is effectively two-option.
**Verdict: SOUND but non-discriminating.** *Tightening:* replace C and D with the shadow-mode option
and a "launch to one segment with 100% review while the eval set is built" option, then key the
composite answer or ask for "first." As written the item tests nothing a Domain 4 candidate does not
already know.

**Item 2 ("97% accuracy" contract clause).** Keyed C ("propose an SLO..."). Strongest alternative:
the stem says *contract clause*; by the chapter's own §2 definition an SLO has no external
consequence, so C answers a contract question with a non-contractual instrument. The defensible
answer is an **SLA** whose SLI is the pass rate on a jointly defined, versioned corpus, with a
remedy, a re-measurement cadence, and an out-of-distribution exclusion — and a client who requires a
number for procurement reasons can be given 97% *scoped to that corpus*. B and D are strawmen.
**Verdict: UNDER-DETERMINED.** *Tightening:* reword C to name an SLA with remedy + re-measurement
trigger + disclosed corpus; add a genuinely tempting distractor — "accept 97% measured on the
client's 500-document sample, with no re-measurement clause" — so the discriminator becomes the
*re-measurement and distribution-shift terms*, not the presence of a number.

**Item 3 (which discovery question most changes the architecture).** Keyed B (reversibility). Options
A (email color scheme), C (PM tool), D (team size) are not credible; the item is solvable by
eliminating jokes.
**Verdict: SOUND but non-discriminating; below MQC level.** *Tightening:* make all four options real
discovery questions that all change something — data residency, peak concurrency, latency tolerance,
reversibility — and ask specifically which one gates *whether human approval must precede the
action*. That forces the candidate to know what each answer gates, which is the objective.

**Item 4 (two handoff artifacts).** Keyed A, C. B (brainstorming notes) and D (marketing deck) are
filler.
**Verdict: SOUND but non-discriminating.** *Tightening:* draw all four options from the legitimate
handoff set — runbook, ADR log, prompt/model change log, eval report, architecture doc, RACI — and
ask which two are load-bearing for *continuing safe operation* (change log + named accountable
role/runbook) versus valuable but back-fillable. That is a real judgment; the current item is not.

**Item 5 (program director, no humans in the loop).** Keyed C. Strongest alternative: C silently
equates "low-risk" with "easily reversible." The stem establishes only that *some* permits lack
public-safety consequences — low stakes is not reversibility, and an issued permit a citizen has
relied on may be legally hard to revoke. Two credible options are absent: (i) full automation of
issuance with a pre-declared revocation window plus sampled post-hoc audit (gives the director the
throughput he wants while preserving reversal), and (ii) verify delegated approval authority first —
in many agencies the statute or delegation rules decide whether software may approve at all, and
that legal answer precedes the architecture. The rationale for B is also temperament, not
architecture ("reads as obstruction... forfeits credibility") — that reasoning is exactly what makes
items in this domain unanswerable.
**Verdict: UNDER-DETERMINED.** *Tightening:* add to the stem that a permit-class taxonomy already
exists distinguishing administratively reversible classes (re-issuable, 30-day revocation window,
legal has confirmed revocation authority) from safety-critical ones. Then C wins uniquely on stated
constraints. And re-base B's rationale on the design fact (it over-constrains a class the
constraints allow to be automated), keeping the credibility point secondary.

**Item 6 (which statement about ADRs is correct).** Keyed C. Strongest alternative: **B is
defensible.** Under MADR — and under the chapter's own ADR template, which lists "Superseded by
ADR-MMM" as a Status value — the superseded ADR *is* edited in place to record supersession.
Immutability covers Context and Decision. The item also has no scenario.
**Verdict: DEFECTIVE.** *Tightening:* reword B to "An accepted ADR's Context and Decision should be
rewritten when a later decision supersedes it," and convert the stem to a scenario: a decision made
18 months ago is being reversed — what do you write, and what do you do to the original record?

**Item 7 (C4 vs. arc42 discriminator).** Keyed B. A, C, D invent constraints nobody would pick. Pure
definitional recall; framework-naming substituting for judgment.
**Verdict: SOUND but non-discriminating; wrong cognitive level.** *Tightening:* make it a scenario
with an audience and include a right-framework-wrong-zoom-level distractor (see Attacks).

**Item 8 (sourcing the first eval set).** Keyed C. C is the best of the four, but the item belongs to
Domain 4, and a defensible alternative exists for the stem's stated condition ("newly launched"):
stratified sampling from the launch traffic itself, supplemented by *deliberately synthetic* cases
for rare high-severity failure modes you cannot afford to wait to observe. The "20–50" range risks
being memorized as a standard.
**Verdict: SOUND but off-blueprint.** *Tightening:* replace with a Domain 6 item, or reframe around
who signs the threshold and how the stakeholder is told when a refresh moves the number.

**Item 9 (moving from 100% to sampled review — select 2).** Keyed A, B. **A directly contradicts
§3.4**, which says volume is never on its own a reason to remove review from irreversible actions.
The stem does not state reversibility, so a candidate applying the chapter's own discriminator cannot
endorse A. The missing fourth posture (risk-tiered review) is also the strongest real answer and is
unavailable.
**Verdict: DEFECTIVE.** *Tightening:* see Attacks — split into a select-1 on sufficient
justification and a select-2 on required accompanying controls; add risk-tiered review to §3.4 first.

**Item 10 (re-run evals after a model upgrade).** Keyed B. A, C, D are indefensible; the stem is
answerable from the word "release." No boundary condition: it assumes full-suite re-runs are always
affordable and always the right granularity.
**Verdict: SOUND but non-discriminating.** *Tightening:* add cost and time pressure to the stem (the
version is retired in ten days; full grading takes three weeks) so the correct answer must reason
about risk-stratified subsets, a canary, and written risk acceptance for the deferred coverage.

**Count: 2 DEFECTIVE (6, 9), 2 UNDER-DETERMINED (2, 5), 6 SOUND — of which 5 are
non-discriminating and 1 is off-blueprint.** One item (Item 5's rationale for B) resolves partly on
temperament. Zero items test discovery reasoning beyond a single word, audience-tailored trade-off
communication, RFC-vs-ADR sequencing, deprecation, declining a use case, or written risk acceptance.

---

## Missing alternatives

| Location | Omitted credible option | Why it matters |
|---|---|---|
| §3.4 (review posture) | **Risk-tiered review**: 100% on the irreversible/high-severity slice, sampled on the rest; plus **post-hoc review with automatic rollback**, **confidence-gated routing**, and **dual control / second-model check** | BLOCKER. A 3-row table (100% / sampled / none) cannot express the answer most real systems use and that an exam is most likely to key. It is also what makes Item 9's capacity pressure resolvable without weakening safety. |
| §3.5 (promotion criterion) | **Shadow mode, canary by segment, A/B against the incumbent, decision-support-first-then-autonomous** | BLOCKER. The chapter presents promotion as a *criterion* and never a *mechanism*. Shadow mode is the standard answer to "we have no production-representative sample yet" — the exact gap the chapter's own advice creates. It appears nowhere in the chapter. |
| Chapter-wide | **Decline the use case / route to a deterministic system** | BLOCKER. The dossier's kill criteria were dropped. In 7 scenarios and 10 items, declining is never an option. |
| Chapter-wide | **Buy instead of build**; **run it as a service instead of handing it off** | MAJOR. §4.2 (ambient clinical documentation) and §4.6 (handoff to unequipped IT ops) are the two scenarios where procurement or retained operation is the strongest answer. Neither is mentioned. |
| Chapter-wide | **Narrow to a reliably solvable slice** (LLM extracts, deterministic engine decides) | MAJOR. This is the dominant real resolution for regulated decisions and is absent from §4.1, §4.4, §4.5. |
| §4.1 (loan underwriting) | Hybrid: LLM does document extraction and completeness checks, a rules engine makes the credit decision; and decision-support that does *not* draft the adverse-action rationale | MAJOR. The recommended answer has Claude draft the *explanation* — in consumer lending the adverse-action reason statement is itself the regulated artifact and must state the actual, specific reasons for the decision. A generated rationale that does not reflect the true decision factors is a compliance exposure, not a productivity win. *Validator question:* confirm the ECOA/Reg B specific-reasons requirement and bank model-risk-management expectations before the editor states this as fact. |
| §4.2 (clinical notes SLA) | Commit at the **system** level including the human ("no unsigned note reaches the chart"; clinician edit-distance band), and **scope the number to a bounded subtask** (medication list extraction) while SLO-banding the free narrative | MAJOR. Both are more defensible than the keyed "counter with an SLO," and both are what actually gets signed. |
| §4.3 (retail pilot) | **Change the human-review tier instead of the scope**: launch full scope in two weeks with 100% review on account changes and sampled review on refunds | MAJOR. This satisfies the VP's timeline *and* the reversibility constraint — strictly better than the keyed answer's "defer account changes," which the stem gives no reason to prefer. Exam could key it. |
| §4.4 (permits) | Automate issuance with a **pre-declared revocation window + sampled post-hoc audit**; automate the recommendation and the paperwork while retaining the signature; **verify delegated approval authority** before designing | MAJOR. See Item 5. |
| §4.5 (cost ceiling) | **Renegotiate the ceiling on unit economics** (cost per avoided truck roll, not cost per request); **batch processing and prompt caching before changing model tier**; hybrid rules-engine-plus-LLM split | MAJOR. The chapter treats the ceiling as fixed, then concedes in one line that it is negotiable. On a Claude exam, the cost levers available *before* downgrading the model are the point. Numbers require AGENT-BRIEF §0 verification — validator. |
| §4.7 (feedback loop) | **Instrument the capture path** (in-product failure-report control writing input/output/context/version into a triage queue) | MAJOR. Naming an owner for an email inbox is the cop-out; the architectural defect is the intake. |
| §3.2 (commitments) | **Human-review turnaround SLA** ("95% of escalations reviewed within 4 business hours"), **throughput/capacity commitment**, **scope-of-use exclusions**, **remedy structure** (credits vs. re-work), **distribution-shift clause**, **who pays for re-measurement after a model upgrade** | MAJOR. The turnaround SLA is highly committable and is often the right thing to offer a client demanding an accuracy number. The distribution-shift clause is the single most important term in an LLM quality contract and is missing. |
| §3.1 (artifact selection) | **Eval report**, **threat model / DPIA**, **control-evidence package**, **integration guide**, **handoff checklist** | MINOR–MAJOR. The dossier had all of these; the draft's table has five rows and sends the auditor the wrong one. |
| §3.6 (ownership) | **Platform team owns the runtime, business unit owns the SLO, with an interface contract**; **vendor owns it under a support contract** | MINOR. The real-world third option is neither "one owner" nor "RACI across roles." |
| §3.3 (prioritization) | **Evaluability and reversibility as ranking axes**; cost-of-delay/WSJF | MAJOR. See Attacks. |

---

## Heuristic boundary conditions

| Heuristic (as written) | Required qualifier |
|---|---|
| §7.1 "Match the artifact to durability and audience" | Add the significance threshold (costly to reverse, or someone outside the room will ask why) and the override: a regulated QMS or the contract may prescribe the artifact set; a short-lived throwaway with a scheduled sunset needs no ADR. Also: the mapping is many-to-many — a contested, regulated decision produces RFC → ADR → arch-doc update → memo. |
| §7.2 "never a promised percentage" | Rewrite as a rule about the **input domain**: committable when the domain is disclosed, versioned, sampled, and carries a re-measurement trigger. A contractually mandated numeric KPI (public procurement; regulated high-risk-system accuracy declaration — *validator to confirm the regulatory citation*) is met by scoping, not by refusing. |
| §7.3 "the promotion criterion is *always* an eval-gate pass rate on a production-representative sample" | Add: (a) for greenfield with no production traffic, use a documented proxy distribution plus a shadow/canary phase with a pre-declared stop rule, and schedule a distribution-shift review; (b) for high-severity systems the eval gate is necessary but not sufficient — add adversarial/red-team pass and a rehearsed rollback; (c) a canary with a pre-declared stop rule on live outcomes is also falsifiable, and measures outcomes rather than proxies. |
| §7.4 "never a flat yes or a flat no" to 100%-automation demands | Add: a documented refusal is correct when a legal, licensure, or statutory-authority constraint makes the ask unimplementable as specified. Reframing is the default, not the universal. |
| §7.5 "discovery answers come before pattern/model selection" | Scope to *commitment and production architecture*. A time-boxed spike with no production dependency is a legitimate discovery instrument and is sometimes the correct "first" action — particularly when the stakeholder cannot state an accuracy bar in the abstract. |
| §7.6 "Accountable is exactly one name" | Exactly one accountable **role**, with a named current holder, rotation, and escalation path. "Platform team's service owner of record, currently X" passes; "the team" fails because it names no role. |
| §7.7 "Model/prompt changes are releases; any exemption is wrong" | Add the bypass protocol: a named approver's written risk acceptance + compensating controls that bound blast radius + a declared deadline for the deferred gate run. Security hotfixes and provider-forced migrations are the two canonical cases. Forced migrations re-validate against a risk-stratified subset with the coverage gap documented, not the full suite. |
| §2 "ADR is immutable" | Context and Decision are never rewritten; Status changes to record deprecation or supersession. |
| §2 "Baseline before promising improvement" | Keep — but add the degraded mode: when the incumbent process is unmeasured and cannot be instrumented in time, construct a one-week sampled baseline on 30–50 cases and state its confidence limits, rather than either measuring nothing or delaying the project. Also flag the open question the dossier honestly raised: no source specifies a minimum sample for declaring an improvement real — the architect must state sample size and variance explicitly. |
| §3.2 "degradation/fallback commitments are safe because they are not numbers" | Only as falsifiable as the trigger signal. Requires a named detector with disclosed recall and a measured abstention rate. |
| §3.4 "the axis is reversibility and blast radius" | Keep verbatim (see Must preserve) — but add the risk-tiered posture so capacity pressure has a correct resolution. |
| §3.6 "no named owner is never right" | True at handoff; but the correct object is a role, and the degraded mode (no one will accept it) is: accountability defaults to the executive sponsor, recorded as a launch blocker, with autonomy reduced so an unowned failure is bounded. |

---

## Degraded-mode gaps

| Recommendation | Org maturity it assumes | Required fallback the chapter must add |
|---|---|---|
| Eval gate on a production-representative sample | Eval platform, graders, labeled data, retained production inputs | 20–50 cases in a spreadsheet; rubric; two human raters on a 30-case calibration slice with inter-rater agreement reported; LLM judge only after calibration; pairwise preference against the incumbent when no ground truth exists |
| Production sampling into the eval set | Legal permission to retain inputs | De-identified corpus held inside the customer's boundary (vendor sees aggregate pass rates only); synthesis from real schema + real failure taxonomy; customer-held blind eval; or SLO stated over a proxy corpus with the distribution gap disclosed |
| "Add security/legal as Consulted during discovery" | A cooperative, available security function | File the architecture-intake ticket at design time so queue time runs in parallel; submit DFD + written classification/retention answer as ADR Context; shrink the reviewable surface (boundary redaction, retention off, no new egress) |
| RACI with a named Accountable at handoff | Authority to assign accountability | Escalate to the executive sponsor as default Accountable; record the gap as a launch blocker; reduce autonomy to bound an unowned failure |
| Six-artifact handoff set (§4.6) | Documentation budget and an LLM-capable receiving team | Minimum viable handoff: runbook + named accountable role + prompt/model change log + eval set with threshold + rehearsed rollback. Arch doc and ADR log are back-fillable. If the receiving team lacks capability: bounded joint-operation period with a written exit criterion, or retain as a service, or buy managed support |
| "Standing eval, reviewed weekly"; dedicated eval owner (§4.7) | Dedicated reviewer time | Scale the cadence to report volume (the chapter says this once, in §4.7's "changes the answer" — promote it to a rule); minimum viable version is a monthly 20-case regression run owned by the on-call rotation |
| Architect sets gates and can block a launch | Release authority | One-page residual-risk memo + **written risk acceptance from the named accountable executive** (this is the artifact); unilaterally reduce blast radius within the architect's own control (tool scope, rate limits, cohort size, kill switch, 100% review on the irreversible slice) |
| Quality SLO with an error budget that halts changes | An org that will actually stop shipping | Pre-commit the *specific* consequence at SLO-definition time (which change classes freeze; who can override; what the override costs) — an error-budget policy nobody agreed to in advance is not a control |
| Gate checklist / phase model (in dossier, dropped) | A stage-gated SDLC | Restore it, and add the lightweight version: a single pre-launch checklist with owner, threshold, rollback, and on-call — four lines, not eight gates |

---

## Must preserve

1. **§3.2 commitment matrix and its discriminator.** "If the commitment can be evaluated against a
   specific, disclosed, versioned dataset with a stated cadence, it's committable as an SLO (and an
   SLA if a contractual consequence is attached). If it can only be evaluated against 'whatever the
   user happens to ask,' it is not committable — reframe it as a band plus a degradation path." This
   is the best paragraph in the chapter and the correct refusal of something stakeholders want.
   **Correct-but-looks-wrong:** the "No" rows ("95% factual accuracy," "no hallucinations"). An
   editor under pressure to seem accommodating may soften these into "negotiate a lower number" —
   that would be wrong. Scope them to the input domain; do not weaken them.

2. **§3.4's discriminator that the axis is reversibility and blast radius, not volume or executive
   preference.** Counterintuitive, correct, and the single most transferable idea in the chapter.
   **Correct-but-looks-wrong:** it appears to conflict with Item 9. Fix Item 9; do not touch the
   discriminator.

3. **§1's distractor-archetype taxonomy**, especially archetype 5 ("the premature scope answer" —
   a technical fix offered for an unanswered discovery question) and archetype 6 ("the ownerless
   handoff"). These are the chapter's best pedagogical assets and they give a candidate something to
   do under time pressure.

Also preserve, and do not let an editor "fix":

- **§1's opening frame**: "This domain does not test writing skill or interpersonal style." Correct
  and load-bearing — it is the defense against exactly the temperament-and-etiquette items this
  domain attracts.
- **§2 on ADRs**: "an ADR persuades a stakeholder — it records a decision already made, including its
  downsides." The refusal to make the ADR persuasive looks like pedantry and is right.
- **§2 baseline misconception**: "assuming the current process is 'obviously' near-perfect without
  measuring it either." Reads as nitpicking; is the actual reason business cases collapse.
- **§4.2's refusal of the 99% clause** and **§4.4's refusal of both the flat yes and the flat no** as
  *defaults*. Both are correct defaults that look like fence-sitting. Add the boundary conditions
  above without reversing the defaults.
- **§6 anti-patterns**, particularly "Verbal SLA" and "The one eval to rule them all" — concrete,
  correctly diagnosed, with the looks-right reasoning named.
- **The dossier's honesty about open questions** (no source specifies a minimum eval size for
  declaring an improvement real; no source sets a maximum eval staleness interval; RACI's origin is
  undocumented). The draft dropped these. Restore them as explicit open judgment calls rather than
  inventing cadence numbers — an editor's instinct will be to supply a number, which would be a
  fabrication under AGENT-BRIEF §0.

---

## Questions for the validator

1. Does D06-S03 state the "20–50 cases" starting range, and is it framed as a heuristic rather than a
   standard? (Item 8 and §2 both lean on it as doctrine.)
2. Confirm before the editor asserts any of these as fact: the ECOA/Regulation B requirement to state
   *specific* reasons for adverse action (relevant to §4.1's generated rationale); bank
   model-risk-management expectations for model-generated credit rationales; whether the EU AI Act
   requires declared accuracy metrics/technical documentation for high-risk systems (relevant to the
   §7.2 counter-scenario — my argument stands on public-procurement KPI practice alone if the
   statutory citation cannot be confirmed); whether EU works-council consultation can be triggered by
   an internal AI tool rollout (§ discovery stakeholder list).
3. MADR / adr.github.io: confirm that the superseded-status convention involves editing the original
   ADR's Status field in place. My Item 6 DEFECTIVE verdict depends on this. The internal evidence is
   sufficient on its own — the dossier's own template lists "Superseded by ADR-MMM" as a Status value
   — but an external confirmation makes the fix unarguable.
4. Any Claude-specific lifecycle facts the editor adds for the deprecation/migration gap (version
   pinning vs. aliases, deprecation notice practice, Batch/caching cost levers for §4.5) must be
   verified per AGENT-BRIEF §0. I deliberately assert none.

---

## Sources introduced by this review

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|
| D06-A01 | Claude Certified Architect – Professional Exam Guide v1.0 | (local) `claude-arch-professional-guide.md` | Anthropic | exam-guide | 2026-09-24 | primary | §6 Domain 6 objectives; §8 sample items/rationales used as the cognitive-level benchmark for the Items 6/7/10 mismatch finding |
| D06-A02 | AGENT BRIEF — CCAR-P prep course, Track B | (local) `AGENT-BRIEF.md` | this project | other | 2026-09-24 | primary | §1 "state the decision, alternatives, discriminator"; §3 chapter structure; §5 rule 1 (no blueprint drift, basis for the Item 8 finding) and rule 2 (no claims about live items, basis for the §3.6 finding); §0 verification rule |
| D06-A03 | Domain 6 research dossier | (local) `research/06-stakeholder-communication-lifecycle-dossier.md` | this project | other | 2026-09-24 | secondary | Evidence that the discovery question table, gate checklist, audience-tailoring rule, kill criteria, eval report, and deprecation gate existed and were dropped in the draft |
| D06-A04 | ADR organization / MADR template project | https://adr.github.io/ | adr.github.io maintainers | practitioner-blog | not fetched in session `[UNVERIFIED]` | secondary | Superseded-status convention behind the Item 6 DEFECTIVE verdict — validator to confirm (see Question 3); the finding also stands on the dossier's own template |
| D06-A05 | Google SRE Workbook — Implementing SLOs / error budget policy | https://sre.google/workbook/implementing-slos/ | Google | vendor-docs | not fetched in session `[UNVERIFIED]` | secondary | The "error-budget policy must pre-commit its specific consequence" degraded-mode point — validator to confirm the framing before the editor cites it |
| D06-A06 | ECOA / Regulation B adverse-action reason requirements | — (validator to resolve; CFPB / 12 CFR part 1002) | CFPB | standard/regulation | not fetched in session `[UNVERIFIED]` | secondary | §4.1 finding that a generated adverse-action rationale is itself a regulated artifact — see Question 2; do not state as fact until confirmed |
