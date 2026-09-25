# Adversarial review — Domain 2: Claude Models, Prompting & Context Engineering

**Reviewed:** `research/02-models-prompting-context-dossier.md`, `drafts/02-models-prompting-context-draft.md`
**Cross-referenced against:** `AGENT-BRIEF.md`, `VERIFIED-FACTS.md`, `claude-arch-professional-guide.md` §6/§8

```
VERDICT: MAJOR-REWORK
Top 3 must-fix items:
1. The chapter states several "current models return 400 for X" facts (temperature/top_p/top_k,
   assistant prefill, forced tool_choice, citations+structured-outputs) as flat, unhedged fact in
   core concepts, a heuristic, the failure-mode table, and TWO practice-item answer keys (items 4, 9)
   — despite VERIFIED-FACTS.md explicitly instructing every agent: "do not state these as fact in a
   chapter until the Domain 2 validation file confirms them." No such validation file exists yet.
   Hedge every instance as [UNVERIFIED] or rebuild the affected items on confirmed facts.
2. Practice item 3's answer key asserts changing `tool_choice` from `auto` to `none` "invalidates the
   tools and system caches but not the messages cache" — a claim absent from the dossier's own
   cache-preserving-escape-hatches research (which never lists tool_choice) and absent from
   VERIFIED-FACTS. This looks fabricated to make a distractor set work. Verify against primary docs
   or replace the option.
3. Heuristic 10 ("Adaptive thinking is the CoT... manual scaffolding is the fallback, not the
   default") is falsified by the chapter's own sourced fact that Haiku 4.5 — the chapter's named
   efficiency-first default model, used in Scenario 5.3 — has no adaptive thinking at all and only
   supports manual budget_tokens extended thinking, off by default. Add the model-scoped carve-out.
```

---

## Internal contradictions

**C1 — VERIFIED-FACTS.md contradicts itself, and the draft resolves the contradiction the wrong way.**

Quote A (canonical "Thinking and effort" section, presented with no hedge):
> "Extended thinking (the manual `enabled` + `budget_tokens` mode) is **deprecated on Opus 4.6 and Sonnet 4.6 and not accepted on later models**."
> "**Adaptive thinking is always on and cannot be disabled on Opus 5.5** — `thinking: {"type": "disabled"}` returns a 400 at every effort level."

Quote B (later section, same file, same day):
> "Reported by the Domain 2 researcher and **pending validator confirmation** — do not state these as fact in a chapter until the Domain 2 validation file confirms them... current models are reported to return **400** for non-default `temperature`/`top_p`/`top_k`, assistant **prefill**, `budget_tokens`, `thinking: {"type":"disabled"}` (Opus 5.5/Fable 5.1), forced `tool_choice`, and citations combined with structured outputs."

`thinking:disabled` and `budget_tokens`-rejection are stated as settled fact in Quote A and simultaneously listed as unconfirmed in Quote B. **Resolution: treat those two as confirmed** (double-sourced, one instance unhedged) — but **temperature/top_p/top_k 400s, prefill 400s, forced tool_choice 400s, and the citations+structured-outputs incompatibility appear nowhere else in VERIFIED-FACTS as confirmed** — they exist only in the "pending" list. Those four remain genuinely unconfirmed.

The draft ignores Quote B's instruction entirely for all six items. Direct quotes from the draft stating them as flat fact:
- Heuristic 11: *"`temperature` is not a lever. Non-default sampling values return 400 on current frontier models."*
- Core concepts, Structured outputs: *"how you guarantee a machine-readable contract now that assistant prefill returns 400 on every current model."*
- Failure-mode table: *"400 on a request that worked on the previous model | ... `temperature`/`top_p`/`top_k` non-default; prefill; `budget_tokens`; `thinking:"disabled"`; forced `tool_choice`"*
- Item 9 rationale: *"**A** also returns 400 — non-default sampling values are rejected... **C** returns 400 on Opus 5.5 and Fable 5.1, where forced tool use is unsupported."*
- Item 4 / Scenario 5.2: *"Citations plus `output_config.format` in one request returns **400**."*

The draft's own "Remaining [UNVERIFIED] claims" section (§11) lists three caveats (context-editing model support, pre-Opus-5.5 authorship, caching-impact ranges) but **omits all four of these**, despite VERIFIED-FACTS naming them by name as pending. **Which side is right:** VERIFIED-FACTS' explicit instruction — the four unconfirmed items must not be taught as settled fact yet. This is a BLOCKER: a candidate who memorizes heuristic 11 or item 9's elimination logic and it turns out temperature tuning is merely discouraged (not a 400), or forced `tool_choice` still works on some path, fails an item for a reason this chapter taught them.

**C2 — Item 3's answer key vs. the dossier's own caching research.**

Item 3 rationale: *"**D**: `tool_choice` invalidates the tools and system caches but **not** the messages cache [D02-S13]."*

The dossier's own "Cache-preserving escape hatches" table (built specifically to enumerate every top-level change and its cache-preserving alternative) lists exactly five rows — system prompt content, per-turn reminder, tool definitions, `effort` change, model switch — **and never mentions `tool_choice`**. Nothing else in the 314-line dossier discusses `tool_choice` interacting with caching at all. **Which side is right:** unknown — this is a question for the validator, not an assertion I can resolve — but the item cites [D02-S13] (the platform prompt-caching page) for a claim the same-sourced dossier never transcribed from that page. Either the citation is wrong or the fact was invented during item-writing. Treat as DEFECTIVE until verified.

**C3 — Heuristic 10 vs. the chapter's own Haiku 4.5 facts.**

Heuristic 10: *"Adaptive thinking is the CoT. Manual `<thinking>` scaffolding is the thinking-off fallback, not the default."*

Dossier (Objective 3 findings, sourced): *"Thinking on Haiku 4.5 | Manual extended thinking only (`{"type":"enabled",budget_tokens:N}`), **off by default**; rejects `adaptive`."*

Haiku 4.5 is not an edge case here — it is the model the chapter's own §4.1 table names for "efficiency-first" and the model Scenario 5.3 actually deploys. On Haiku 4.5 there is no adaptive thinking to fall back from; manual CoT prompting (or no thinking at all) is the only regime that exists. **Which side is right:** the Haiku-4.5 fact — heuristic 10 needs a per-model carve-out or it will misfire on exactly the tier the chapter recommends for high-volume work.

**C4 — Capability-first "Fits" column vs. the chapter's own flat-curve finding.**

§4.1 table, Capability-first row: *"Fits | Complex reasoning, advanced coding, high-autonomy agentic work."*

§4.3 discriminator text (same chapter): *"on research work the default bought nothing measurable over `medium`, so those thinking tokens were waste."* Dossier is more explicit still: *"on DeepResearch-style work effort was flat, so that is **not** a frontier-only signal — flatness means the cheaper setting already does the work."*

"Complex reasoning" is heterogeneous — coding-style reasoning has a steep, real effort/capability curve (§4.3's own coding numbers); open-ended research/synthesis reasoning is documented as flat. The §4.1 table's "Fits" column lumps both under one label with no discriminator between them, which a candidate could read as "reasoning task → spend more" — the opposite of the chapter's own flat-curve finding for research-shaped reasoning. **Which side is right:** the flat-curve finding (empirically sourced) should qualify the "Fits" column, not the reverse. No item currently tests the flat-curve case in the wrong direction (see Item-by-item section, gap noted under Item 2).

**C5 — §4.1's stepping-down/eval-gate method vs. Scenario 5.3's downshift-by-assertion.**

§4.1: *"Stepping-down method, in order: sweep effort on the current model → if `low` passes the eval, drop one tier → confirm which parameters and effort levels that tier accepts → reset effort to the new tier's own default → re-sweep."*

Scenario 5.3 recommends replacing "the frontier model at default effort" with Haiku 4.5 for 380-way fine-grained retail classification on the strength of *"Haiku 4.5 is the documented fit for high-volume straightforward work"* — with no mention of running the eval gate the chapter itself just prescribed, and no acknowledgment that 380 overlapping leaf categories may not be "straightforward." **Which side is right:** the stepping-down method — Scenario 5.3 should show the eval step, not assert the downshift is safe by category label alone. This is also Attack #3's "downgrade without an eval gate" pattern landing directly in the chapter's own worked example.

---

## Attacks that landed

**[BLOCKER] Core concepts / Heuristic 11 / §6 failure-mode table / Items 4 & 9 — unconfirmed "classic levers return 400" facts taught as settled.** See C1. Counter-scenario: a candidate answers item 9 with B because "temperature also 400s" per heuristic 11; on the real exam (or in production) `temperature: 0` turns out to still be accepted (merely discouraged, not rejected) — the elimination logic collapses and the candidate has been trained on a false discriminator. Fix: hedge all four unconfirmed facts (temperature/top_p/top_k, prefill, forced tool_choice, citations+structured-outputs) with `[UNVERIFIED — pending Domain 2 validation]` everywhere they appear, and until confirmed, rebuild items 4 and 9 around confirmed facts (effort defaults, structured-outputs GA status, Skills governance) rather than the 400-behaviors.

**[BLOCKER] Item 3, option D — unsourced tool_choice/cache claim.** See C2. Fix: either get validator confirmation against `platform.claude.com/docs/en/build-with-claude/prompt-caching`, or replace option D with a documented escape hatch from the dossier's own table (e.g., an `inline-tools-2026-09-15` tool-definition change, framed as a wrong answer because tool definitions do invalidate).

**[MAJOR] Heuristic 10 vs. Haiku 4.5.** See C3. Fix: append "— except Haiku 4.5, which has no adaptive thinking; manual CoT prompting is a live primary technique there, not a fallback."

**[MAJOR] §4.1 "Fits" column vs. flat-curve finding.** See C4. Fix: split "complex reasoning" into "reasoning with a measured steep curve (coding, multi-step tool-use)" vs. "open-ended research/synthesis (often flat — verify per task before upgrading)."

**[MAJOR] Scenario 5.3 skips its own eval gate.** See C5. Fix: add one sentence — "confirmed via eval that Haiku 4.5's per-category accuracy meets the acceptance bar before cutover" — or the scenario silently teaches "label the task 'straightforward' and downshift" as sufficient justification, contradicting §4.1.

**[MAJOR] §4.5 TTL table drops the per-model cache-read pricing discriminator VERIFIED-FACTS calls out by name.** VERIFIED-FACTS: *"Cache-read economics now differ *by model* — a real architectural discriminator."* The dossier itself applies this: *"On Fable 5.1, where reads are 0.025x, a `max_tokens: 0` keep-alive on the 5-minute TTL usually beats buying the 1-hour TTL unless pauses approach an hour."* The draft's §4.5 TTL row states one universal breakeven ("5-minute pays back on the second request... 1-hour on the third") computed at the generic 0.1x rate, with no model-dependent caveat anywhere in the table or the worked scenarios. Counter-scenario: an architect designing a Fable-5.1-backed agent with 20-40 minute gaps follows the table verbatim, buys the 1-hour TTL, and pays a needless 2x write premium when a cheap keep-alive read (0.025x on Fable 5.1) would have kept the 5-minute cache warm for less. Fix: add a per-model row or footnote to the TTL table.

**[MAJOR] Least-privilege tool removal vs. per-role dynamic tool lists breaking caching — never reconciled.** §4.8/Item 6 teach "remove the tool from the config" as the gold-standard, hard-guarantee guardrail. §4.5/§6 teach that any change to the tool list changes the whole downstream prefix and kills caching for that request. In a real multi-role agent (support staff vs. supervisors, each with a different tool set), applying least-privilege literally — a distinct tool list per caller — fragments the cache into as many prefixes as there are roles, at scale a real cost trade-off the chapter never surfaces. Counter-scenario: an architect removes tools per-user for least privilege, then can't explain why cache hit rate collapsed. Fix: add a note — bucket callers into a small, fixed number of role-based tool-set variants (each its own stable, cacheable prefix) rather than per-user tool removal, or accept the cache cost as the price of the security posture and say so explicitly.

**[MAJOR] "Ways to buy accuracy" (§4.3) omits "fix retrieval/input quality" as an instrument.** The table lists four instruments (effort, few-shot, decomposition, tier upgrade) for buying accuracy. Elsewhere the chapter itself says the discriminator for many symptoms is *"if prompt and model are unchanged, the change is in what got into context — retrieval, not the model"* (heuristic 11) — echoing the exam guide's own Domain 4 Sample 3. Yet this exact instrument is missing from the one table titled "ways to buy accuracy," inviting a candidate to reach for effort/few-shot/decomposition/tier on a problem that is actually a context/retrieval defect no prompting technique fixes. Fix: add a fifth row, "repair retrieval/input quality," with the discriminator "wrong or missing facts in an otherwise well-reasoned answer."

**[MINOR] Modularization boundary missing.** §4.7 covers templated/modular prompts' versioning and blast-radius trade-offs but never notes the debuggability cost: many small runtime-composed fragments can eliminate any single human-readable "as-sent" prompt, making failures harder to diagnose than either a monolithic prompt or a Skill bundle. Fix: one sentence noting the need to log/reconstruct the fully rendered prompt regardless of authoring modularity.

**[MINOR] Skill-vs-template overhead boundary missing.** §4.7's "Prerequisites" row lists Skills' requirements (code execution tool, ≤20/request, ≤30MB, workspace isolation) but the prose never states the negative case: a single-team, single-tenant service gains little from Skill governance and inherits real operational cost (sandboxed execution, workspace planning) that a versioned template in the app repo avoids. Fix: add "Skill when reuse crosses team or tenant boundaries; template when it does not" to the discriminator sentence.

**[MINOR] Item 5 keys on a volatile implementation constant.** The "20-position lookback" number is an implementation detail, not an architectural principle — a plausible target for staleness. The reasoning chain in the item is otherwise sound (30 sequential calls clearly exceed any plausible lookback), so the item survives even if 20 changes, but the answer key's citation of the exact number as load-bearing should be phrased as "exceeds the documented lookback window" rather than requiring recall of "20."

---

## Caching decision audit

**Verdict: the prose is conditioned; the item bank and one comparison table are reflexive.**

The chapter's running text does real conditioning work: a mode gate (automatic vs. explicit vs. combined), a TTL gate keyed to the start-to-start gap, a cacheable-minimum gate (with the Haiku 4.5 trap called out twice), and two explicit anti-cargo-cult statements — *"Caching is not a substitute for context reduction"* and *"Caching reprices; it does not reduce"* (heuristic 6). Scenario 5.4 shows a caching-adjacent mechanism (context editing) actively costing more than it saved. This is well above reflexive.

Two gaps keep it from being fully conditioned:

1. **No worked scenario or practice item where "enable caching" is the wrong or insufficient answer.** All ten items and six scenarios that touch caching assume caching is the correct general move and test only correct implementation (placement, TTL, mode). Given the exam guide's own Sample 2 rewards "enable prompt caching" directly, the chapter needs at least one item/scenario where the tempting distractor *is* "enable caching" and the correct answer is something else — e.g., traffic so sparse (daily batch, single call per prefix) that the write premium never amortizes and the right answer is "do not cache; the shared content should be behind a Skill/tool loaded on demand instead," or a "static" system prompt that in fact varies per authenticated user (a personalization block silently defeating the whole prefix).
2. **Per-model cache-read pricing is dropped from the one table that needs it** (see Attacks-that-landed, TTL finding above) — VERIFIED-FACTS calls this "a real architectural discriminator" and the dossier applies it; the draft's TTL decision table does not.

Required additions: (a) one scenario/item where caching is a trap (sparse traffic or a falsely "static" prefix), (b) a per-model note on the TTL table, (c) explicit treatment of the least-privilege-vs-cache-fragmentation tension above.

---

## Item-by-item adversarial re-solve

**Item 1 (caching breakpoint placement).** Strongest alternative case: none credible — B is the only option that stops writing an unread entry. **SOUND.** VOLATILE-DEPENDENCY: no (tests the prefix-match mechanism, not a number). Tightening: none required; optionally clarify whether the "6,000-token system prompt" renders before or after the "clause library" in the `system` array, since the fix only works if both are static and precede the excerpt.

**Item 2 (evals fail at xhigh/max, what next).** Strongest alternative: A (advisor) — plausible on its face, but the chapter's own measured data (advisor ≈ what more effort buys, at ~2x cost, and effort is already exhausted) correctly eliminates it. **SOUND.** VOLATILE-DEPENDENCY: no — tests the durable "if the strongest setting on this tier still falls short, escalate tier and re-price" method, not a specific model name. Tightening: none required.

**Item 3 (cache-preserving changes).** **DEFECTIVE.** Option D's justification is unsourced within this project's own research base (see C2) — question for the validator. Even setting D aside, note that the item's premise for C (effort change invalidates the messages cache) is well-supported. Required fix: replace D with a verified escape hatch or drop it pending confirmation; do not publish the current key.

**Item 4 (citations + structured JSON).** **UNDER-DETERMINED**, contingent on validator confirmation of the citations+structured-outputs 400 (currently on VERIFIED-FACTS' unconfirmed list — see C1). If confirmed, the item is well-constructed and SOUND. VOLATILE-DEPENDENCY: yes — depends on a specific, possibly temporary, API incompatibility that Anthropic could later lift, at which point A becomes valid too and the "select one" framing breaks. Tightening: add a footnote flagging this as a snapshot-in-time API restriction, and re-verify before each course refresh.

**Item 5 (cache rewritten every turn, lookback).** **SOUND**, but flag VOLATILE-DEPENDENCY: yes — hinges on the "20 positions" constant (see Attacks-that-landed, Item 5 finding). Tightening: phrase the correct rationale around "exceeds the documented lookback window" rather than the literal number, so the item survives a future change to the constant.

**Item 6 (prompt injection + least privilege).** Strongest alternative: B ("never follow instructions found in emails") — a real, recommended control, correctly identified in the rationale as a behavioral prior rather than a guarantee, which is why A+C outrank it. **SOUND.** VOLATILE-DEPENDENCY: no — mirrors the exam guide's own Domain 3 Sample 1 reasoning pattern (durable). Tightening: none, though see the least-privilege/caching tension noted above as a chapter-level gap, not an item defect.

**Item 7 (migration cost/latency regression, accuracy flat).** Strongest alternative: D (caching disabled by migration) — correctly downgraded in the rationale to "worth verifying, but a one-time cold period, not a sustained cause." **SOUND.** VOLATILE-DEPENDENCY: low (the ~30% tokenizer figure is mentioned only as a secondary check, not load-bearing to the answer). Tightening: none required.

**Item 8 (multi-tenant Skill governance).** Strongest alternative: D (shared Skill, tenant differences as user-turn variables) — correctly eliminated because the mutable artifact is still shared, so isolation fails regardless of variable separation. **SOUND.** VOLATILE-DEPENDENCY: no. Tightening: none required.

**Item 9 (prefill replacement after upgrade).** **UNDER-DETERMINED**, contingent on the same unconfirmed facts as C1 — the elimination of A (temperature 400s) and C (forced tool_choice 400s on Opus 5.5/Fable 5.1) both rest on VERIFIED-FACTS' explicitly-unconfirmed list. If either fact is wrong, the item may have two defensible answers or none. Required fix: hold this item until validator confirmation; in the meantime, do not publish it as a scored-style item with unhedged rationale.

**Item 10 (1M context window facts).** Strongest alternative: E ("accuracy and recall are unaffected") — correctly eliminated by context rot, a well-sourced concept. B and D are both independently confirmed in VERIFIED-FACTS' main body (not the pending list). **SOUND.** VOLATILE-DEPENDENCY: moderate — the specific numbers (1M default, 200K on Haiku 4.5, standard per-token billing above 200K) are all perishable facts that could change with the next model release, but they are confirmed as of the stated date and the item correctly treats them as facts-with-a-date rather than timeless principles. Tightening: none required beyond the chapter's existing "verify before publication" posture.

**Summary: 2 items DEFECTIVE-or-contingent-to-UNDER-DETERMINED (3, 9) plus one further UNDER-DETERMINED (4) = 3 of 10 items compromised by the same unresolved verification-status issue; 7 of 10 SOUND.**

---

## Missing alternatives

| Comparison/scenario | Omitted credible option | Why it matters |
|---|---|---|
| §4.3 "Ways to buy accuracy" | Fix retrieval/input quality | The chapter's own heuristic 11 names this as the correct move for a whole failure class, but it is missing from the one table enumerating "instruments" — a candidate could reach for effort/few-shot/decomposition/tier on a defect none of them fix |
| §5.3 retail bulk classification into a fixed 380-label taxonomy | A non-LLM classifier (embeddings nearest-neighbor, or a lightweight fine-tuned model) | Textbook shape for a cheaper non-LLM solution at 4M records/night; the scenario format promises "why the plausible alternatives lose" but never raises this one |
| §4.5 / caching decision generally | "Do not cache at all" for genuinely sparse, single-hit traffic | Only implicit in the TTL table's ">1h" row; never a standalone recommendation or worked scenario (see Caching decision audit) |
| §4.8 / Item 6 least-privilege tool removal | Role-bucketed tool-set variants (a small fixed number of cacheable prefixes) as an alternative to per-user tool removal | Reconciles the security guidance with the caching guidance; currently the two are taught in isolation and can conflict at scale |
| §5.2 healthcare citations scenario | A deterministic post-hoc validator that checks `cited_text` is an exact substring of the source document | Belt-and-suspenders check consistent with the "programmatic guardrail" row's own "post-hoc validation" entry; not applied here even though the scenario is explicitly about auditability |
| Item 9 / prefill replacement | Noting that "ask for JSON only + defensive parsing with retry" is a weaker but available fallback where structured outputs isn't reachable (older model, unsupported surface) | Gives the discriminator some texture beyond "the one correct migration path" |

---

## Heuristic boundary conditions

1. **"Order static first, volatile last" (heuristic 3).** Fails to help when the unique per-request payload (e.g., a large retrieved context block) dwarfs the static portion — reordering buys little; the fix is shrinking the variable payload, not reordering it.
2. **"Effort before model" (heuristic 4).** Only recovers reasoning-depth failures on information already present in context. Cannot supply a fact that was never retrieved. A context/retrieval defect and a reasoning-depth defect look identical from the symptom alone; the discriminator is whether the needed fact appears anywhere in the transcript.
3. **"Few-shot for format control" (§4.4, anti-patterns).** Needs diversity or it anchors the model onto an unintended shared pattern — already documented as a failure mode in the chapter (a genuine strength, see Must preserve), but stated only as a mitigation ("diversity"), not as a hard boundary ("N examples from the same case type will actively mislead, not just under-perform").
4. **"Summarize/compact when context grows" (§4.6).** Already correctly qualified — "overly aggressive compaction can result in the loss of subtle but critical context." Preserve as-is; do not weaken this hedge in editing.
5. **"Modularize prompts" (§4.7).** Needs: fragmentation across many runtime-composed templates can eliminate any single human-readable "as-sent" artifact, hurting production debuggability even though each module is independently testable.
6. **"Prefer Skills for reuse" (§4.7).** Needs: Skills solve a cross-team/cross-tenant governance problem; a single-team, single-tenant service inherits real operational cost (code execution tool, workspace-isolation planning, ≤20/request, ≤30MB) for no governance benefit it needs. A versioned template in the app repo is often sufficient.
7. **"Adaptive thinking is the CoT" (heuristic 10).** Does not hold on Haiku 4.5, which has no adaptive thinking at all (manual `budget_tokens` only, off by default) — see C3.
8. **"Remove the tool for least privilege" (§4.8/Item 6).** Correct for a single fixed role. At scale, per-caller tool removal fragments the prompt cache into one prefix per role/user — the chapter should say this trade-off exists, not imply removal is a free, uniformly-best move.
9. **"Raise `effort` where the curve is steep" (§4.3).** "Complex reasoning" is not one curve — coding-style reasoning measured steep, open-ended research/synthesis measured flat. The chapter's own capability-first "Fits" column should not list "complex reasoning" as a single undifferentiated category (see C4).

---

## Must preserve

1. **Cost-per-completed-task discipline, with the tail-risk framing.** The Fable-5.1-at-`low`-beats-Sonnet-5-default-per-solved-task result (11 points more accurate, 35% cheaper per solved task, at 5x the per-token price) is a genuinely counter-intuitive, well-sourced number that correctly kills the "cheapest per-token = cheapest" instinct. This is the chapter's best material and must survive length cuts.
2. **Prompt-caching-as-prefix-match mental model plus the explicit "caching reprices; it does not reduce" distinction.** This is exactly the discipline needed to avoid turning the exam guide's own Sample 2 into a reflex ("saw a static prefix → say caching") rather than a reasoned answer. The TTL breakeven math and the mode/placement discriminators are genuinely useful and non-obvious.
3. **The three-layer guardrail taxonomy (system-prompt / programmatic / classifier) with precise "enforces / cannot enforce" columns**, and the message-shape framing of prompt injection defense (deliver untrusted content only in `tool_result`; never put your own instructions there). This is a rigorous, exam-appropriate discriminator framework that matches Domain 5's own rigor and should not be compressed away.

**Right but suspicious-looking — do not let an editor "fix" this back to conventional wisdom:** the framework that effort/adaptive-thinking/structured-outputs have superseded temperature tuning, assistant prefill, and hand-written CoT scaffolding as the primary determinism and reasoning-depth levers correctly contradicts nearly all pre-2026 published prompt-engineering advice. The *direction* of this claim should survive editing even though, per the BLOCKER above, its current *unhedged confidence level* must not — the fix is to hedge the specific 400-behaviors, not to revert the underlying "effort and structured outputs are now the primary levers" thesis, which is well-supported independent of the pending facts (effort is GA and confirmed; structured outputs are GA and confirmed; only the *rejection* behavior of the old levers is unconfirmed).

---

## Sources introduced by this review

No new external sources were consulted; all findings are derived from cross-referencing the five files listed in the task brief against each other. No `D02-A0x` IDs are introduced.
