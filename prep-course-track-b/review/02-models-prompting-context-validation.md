# Validation — Domain 2: Claude Models, Prompting & Context Engineering (13%)

Validator pass. All verification performed **2026-09-24** against live primary documentation at
`https://platform.claude.com/docs/en/…` (and two `anthropic.com/engineering` pages). Every page was
opened in this session. The bundled `claude-api` skill was **not** treated as a source of fact; where the
dossier's figure traces only to the skill, that is called out. Source IDs resolve in
`## Sources consulted` at the end.

```
VERDICT: SHIP-WITH-FIXES
Top 3 must-fix items:
1. [BLOCKER] §9 item 3 — the cache-invalidation fact behind option D is INVERTED against live docs.
   `tool_choice` changes invalidate the MESSAGES cache and leave tools+system valid (the draft says the
   opposite). D therefore does not preserve a cached prefix in a long conversation, the key "A and D" is
   wrong, and only one of the five options is correct while the item says "select two."
2. [BLOCKER] §3 (Structured outputs) — "assistant prefill returns 400 on every current model" is
   SCOPE-WRONG. Prefill is rejected from the Claude 4.6 generation onward; **Claude Haiku 4.5 is a
   current model and accepts prefill** (and accepts `temperature`/`top_p`, one at a time). The same
   over-generalization appears in §8 heuristic 11 and item 9's rationale.
3. [MAJOR] §5.2 and §9 item 4 — "the restriction is on the request, so wrapping it in a `strict` tool
   does not help" is NOT-FOUND in live docs. The documented 400 is citations + `output_config.format`
   only; docs say JSON outputs and strict tool use are separate features that may be combined. As
   written, item 4's distractor D is not demonstrably wrong, which breaks the item's uniqueness.
```

### What is good and must be preserved

- **The draft did not repeat the researcher's riskiest numbers.** It never states a prompt-caching
  cost multiplier in the body, never states the "~10K schema tokens" tool-search breakeven, never states
  the "1 in 14,000 turns" `max_tokens` figure, and never writes "Anthropic recommends." All three of
  those dossier rows are wrong or unsupported. The draft's restraint is the single best thing about it.
- **Every price, model ID, context window, max output, latency tier, effort default, thinking mode,
  knowledge cutoff and retirement date in the draft is CONFIRMED verbatim** against `models/overview`
  and `pricing`. Zero drift from `VERIFIED-FACTS.md`. Opus 5 is correctly presented as legacy.
- The §4.5 caching section is the strongest passage in the chapter: prefix-match invariant, render order,
  automatic-breakpoint-after-unique-tail surcharge, TTL start-to-start-gap discriminator, and the
  breakeven arithmetic are all CONFIRMED, and the breakeven now has a first-party citation it did not
  have before (`pricing`, D02-V02).
- §5.6 (the migration that got slower) is verbatim-accurate against live docs, including 36% / 14% /
  97%-vs-92%. Keep it.
- §4.8's three-layer guardrail table and §9 item 6 map cleanly onto `mitigate-jailbreaks` wording.
- The exam-guide facts (13%, ≈8 of 63, the five objectives verbatim, Sample 2) are CONFIRMED against the
  local guide.

---

## 400-error claim adjudication

This is the headline section. **Precision of scope is the whole point:** four of the six claims are true
only for a named subset of models, and two of those subsets exclude a *current* model.

### Claim 1 — non-default `temperature` / `top_p` / `top_k` return 400

**Verdict: PARTIALLY-CONFIRMED.** True for Opus 4.7 and later Opus models, Sonnet 5, and Fable 5.1 /
Mythos 5.1. **False for Claude Haiku 4.5**, which is in the current lineup. Not asserted for
Opus 4.6 / Sonnet 4.6.

- D02-V20 (`opus-5-5/migration-guide`), "Sampling parameters removed":
  > "Setting `temperature`, `top_p`, or `top_k` to any non-default value on Claude Opus 4.7 and later
  > models, including Claude Opus 5.5, returns a 400 error. The Python SDK (v1.0 and later) does not
  > define them, and passing them raises a `TypeError`. The safest migration path is to omit these
  > parameters entirely from request payloads. Prompting is the recommended way to guide model behavior
  > on Claude Opus 5.5. If you were using `temperature = 0` for determinism, note that it never
  > guaranteed identical outputs on prior models."
- D02-V20, "What every request to Claude Opus 5.5 must satisfy":
  > "**Sampling parameters:** Omit `temperature`, `top_p`, and `top_k`, or leave them at their defaults:
  > any other value is rejected. Use prompting to guide the model's behavior."
- D02-V21 (`sonnet-5/migration-guide`): > "**Sampling parameters removed:** Sampling parameters
  (`temperature`, `top_p`, `top_k`) set to a non-default value are not accepted and return a 400 error."
- D02-V22 (`fable-5-1/whats-new`), "Unchanged from Claude Fable 5":
  > "Non-default `temperature`, `top_p`, or `top_k` values return a 400 error."
- D02-V21, Haiku 4.5 section: > "**Sampling parameters removed:** `temperature` and `top_p` work on
  Claude Haiku 4.5 (one at a time, not both). On Claude Sonnet 5, setting `temperature`, `top_p`, or
  `top_k` to a non-default value returns a 400 error."

**Sentence the chapter should use:** "On Claude Opus 4.7 and later Opus models, Claude Sonnet 5, and
Claude Fable 5.1 / Mythos 5.1, a non-default `temperature`, `top_p`, or `top_k` returns a 400 —
sampling is no longer a design lever there, and docs say to use prompting instead. Claude Haiku 4.5 is
the exception in the current lineup: `temperature` and `top_p` still work there, one at a time, not
both. Note also that `temperature = 0` never guaranteed identical outputs on the models that accepted
it [D02-V20, D02-V21, D02-V22]."

### Claim 2 — assistant prefill returns 400

**Verdict: PARTIALLY-CONFIRMED.** True from the Claude 4.6 generation onward (plus Mythos Preview).
**False for Claude Haiku 4.5**, a current model, where prefill still works. The draft's "every current
model" is wrong.

- D02-V18 (`claude-prompting-best-practices`), "Migrating away from prefilled responses":
  > "Starting with Claude 4.6 models and Claude Mythos Preview, prefilled responses (providing a partial
  > assistant message for Claude to continue from) on the last assistant turn are no longer supported.
  > Requests with prefilled assistant messages to these models return a 400 error. Model intelligence
  > and instruction following have advanced such that most use cases of prefill no longer require it.
  > **Earlier models continue to support prefills**, and adding assistant messages elsewhere in the
  > conversation is not affected."
- D02-V21: > "**Assistant prefill removed:** Prefilling the assistant message **works on Claude Haiku
  4.5** but returns a 400 error on Claude Sonnet 5."
- D02-V20: > "**Prefill:** Don't end `messages` with a prefilled assistant turn: it is rejected. Use
  structured outputs or system prompt instructions instead."
- D02-V22: > "Prefilling the assistant response returns a 400 error."

**Sentence the chapter should use:** "Prefilling the last assistant turn returns a 400 on Claude 4.6 and
later models — so on Opus 5.5, Fable 5.1 and Sonnet 5 — and the documented replacements are structured
outputs, `output_config.format`, or system-prompt instructions. Claude Haiku 4.5 still accepts prefill,
which is why a prefill-based extractor can survive a Haiku deployment and break the moment it is moved up
a tier [D02-V18, D02-V21]."

### Claim 3 — `budget_tokens` (manual extended thinking) returns 400

**Verdict: PARTIALLY-CONFIRMED, and the scope is a three-way split, not a binary.** Rejected on Claude
4.7 and later; deprecated-but-still-working on Opus 4.6 / Sonnet 4.6; it is the **only** thinking mode
on Haiku 4.5, Opus 4.5 and Sonnet 4.5.

- D02-V06 (`thinking-troubleshooting`):
  > "Extended thinking (`thinking.type: "enabled"` with `budget_tokens`) is deprecated on the Claude 4.6
  > models (requests using it still succeed). Claude 4.7 and later models do not support it and reject
  > requests that use it, returning a 400 error. On Claude 4.5 and earlier models that support thinking,
  > extended thinking is the only available thinking mode."
- Error string (D02-V06, D02-V19): > `"thinking.type.enabled" is not supported for this model. Use
  "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.`

**Sentence the chapter should use:** "`thinking: {type: "enabled", budget_tokens: N}` returns a 400 on
Claude 4.7 and later models, is deprecated but still accepted on Opus 4.6 / Sonnet 4.6, and is the only
thinking mode available on Claude Haiku 4.5, Opus 4.5 and Sonnet 4.5. `effort` is its replacement
everywhere it is rejected [D02-V06]."

### Claim 4 — `thinking: {"type":"disabled"}` returns 400 on Opus 5.5 / Fable 5.1

**Verdict: CONFIRMED**, and the confirmed set is *larger* than the researcher claimed. The per-model
table is the authority and should be the chapter's citation.

- D02-V06, "Thinking support, defaults, and rejected configurations by model" — rejected-with-400 column:
  Fable 5.1 `"enabled"`,`"disabled"` · Mythos 5.1 same · Fable 5 same · Mythos 5 same · Mythos Preview
  `"disabled"` · **Opus 5.5 `"enabled"`,`"disabled"`** · Opus 5 `"enabled"`,`"disabled"`² ·
  Opus 4.8 `"enabled"` · Opus 4.7 `"enabled"` · **Sonnet 5 `"enabled"` only** · Opus 4.6 None ·
  Sonnet 4.6 None · Opus 4.5 `"adaptive"` · **Haiku 4.5 `"adaptive"`** · Sonnet 4.5 `"adaptive"`.
  Footnote 2: > "Claude Opus 5 accepts `"disabled"` at effort `high` or below; combining it with effort
  `xhigh` or `max` returns a 400 error. This restriction is enforced on each request."
  > "Models marked `Always on` cannot turn thinking off. Models marked `On` default to thinking but
  > accept `thinking: {type: "disabled"}`."
- D02-V05 (`effort`), Opus 5.5 section: > "Requests that set `thinking: {"type": "disabled"}` return a
  400 error at every effort level."
- D02-V19: > "The first three also apply on Claude Fable 5.1." (of the four Opus 5.5 breaking changes)
- D02-V21: Sonnet 5 — > "To turn thinking off, pass `thinking: {type: "disabled"}`." D02-V20 adds that
  Sonnet 5 "accepts `thinking: {"type": "disabled"}`, in its case at any effort level."

**Sentence the chapter should use:** "Thinking cannot be turned off on Claude Fable 5.1, Mythos 5.1 and
Opus 5.5: `thinking: {"type":"disabled"}` returns a 400 at every effort level, and so does a manual
budget. Omit the field or send `{"type":"adaptive"}`. Sonnet 5 runs adaptive thinking on by default but
still accepts `disabled` at any effort level; Opus 5 accepts it only at `high` or below; Haiku 4.5
rejects `adaptive` and uses manual extended thinking, off by default. The consequence for the architect
is that 'turn thinking off to cut cost' is not a portable lever — lower `effort` instead [D02-V06, D02-V05,
D02-V19]."

### Claim 5 — forced `tool_choice` returns 400

**Verdict: PARTIALLY-CONFIRMED.** True on Opus 5.5, Fable 5.1 and Mythos 5.1 **only**. The Messages API
validation also applies to `count_tokens`. **Claude Sonnet 5 explicitly ACCEPTS forced tool choice** —
so does Haiku 4.5. The dossier's extra claim that it also 400s on the Batches API is **NOT-FOUND**.

- D02-V19, "Forced tool use is not supported":
  > "Claude Opus 5.5 doesn't support forced tool use. `tool_choice` set to `{"type": "any"}` or
  > `{"type": "tool", "name": "..."}` returns a 400 `invalid_request_error`:" · error string:
  > `tool_choice: type "tool" and "any" are not supported for this model.` ·
  > "`tool_choice: {"type": "auto"}` (the default) and `{"type": "none"}` are supported, and the same
  > validation applies to the token counting endpoint."
- D02-V22: > "Claude Fable 5.1 and Claude Mythos 5.1 don't support forced tool use. … The same
  validation applies to the token counting endpoint." Plus the *reason*, which is good chapter material:
  > "Thinking is always on for these models, and a forced tool call would skip it. The model would write
  > its working-out into the tool arguments instead, which lowers argument quality."
- D02-V20, "Migrating to Claude Opus 5.5 from Claude Sonnet 5": Sonnet 5, like Opus 5,
  > "Accepts forced tool choice and the `computer_20251124` tool."
- Batches: NOT-FOUND on any page consulted. (Separately, `max_tokens: 0` pre-warming rejects
  `tool_choice` of `{"type":"tool"}`/`{"type":"any"}` — a different restriction, D02-V07.)

**Sentence the chapter should use:** "On Claude Opus 5.5, Fable 5.1 and Mythos 5.1, `tool_choice` of
`{"type":"any"}` or `{"type":"tool","name":…}` returns a 400, and the same validation applies to the
token-counting endpoint; `auto` and `none` are supported. Claude Sonnet 5 and Haiku 4.5 still accept
forced tool use, so 'force the tool' is a model-scoped lever, not a general one. Where it is rejected,
the documented replacements are `tool_choice: auto` plus `strict: true`, or moving the schema into
structured outputs, and telling the model in the prompt when the tool applies [D02-V19, D02-V22, D02-V20]."

### Claim 6 — citations combined with structured outputs returns 400

**Verdict: CONFIRMED, narrowly.** The documented 400 is citations + `output_config.format` (or the
deprecated `output_format`). **There is no documented incompatibility between citations and
`strict: true` tool use**, and the structured-outputs page says the two structured-output features are
separable.

- D02-V13 (`citations`), `<Warning>` "Citations and structured outputs are incompatible":
  > "Citations cannot be used together with structured outputs. If you enable citations on any
  > user-provided document (`document` blocks or `search_result` blocks) and also include the
  > `output_config.format` parameter (or the deprecated `output_format` parameter), the API returns a 400
  > error." · "This is because citations require interleaving citation blocks with text output, which is
  > incompatible with the strict JSON schema constraints of structured outputs."
- D02-V12 (`structured-outputs`), "Feature compatibility → Incompatible with":
  > "**Citations:** Citations require interleaving citation blocks with text, which conflicts with strict
  > JSON schema constraints. Returns 400 error if citations enabled with `output_config.format`."
  Also incompatible: > "**Message Prefilling:** Incompatible with JSON outputs".
- D02-V12: > "**JSON outputs** control Claude's response format (what Claude says) · **Strict tool use**
  validates tool parameters (how Claude calls your functions)" and > "**Combined usage:** Use JSON
  outputs (`output_config.format`) and strict tool use (`strict: true`) together in the same request".
- D02-V25 (`strict-tool-use`): no citations restriction; no programmatic-tool-calling restriction.
  **NOT-FOUND.**

**Sentence the chapter should use:** "Citations and `output_config.format` are mutually exclusive: enable
citations on any `document` or `search_result` block and also send `output_config.format` and the request
returns a 400. Split them across two requests — citations for the human-facing answer, a schema-constrained
request for the machine record. Note the boundary precisely: the documented conflict is with
`output_config.format`, not with `strict: true` on a tool, and docs treat JSON outputs and strict tool use
as separable features [D02-V13, D02-V12]."

### Architect-level takeaway the chapter must state

The draft's framing — determinism moved from sampling parameters to `effort`, structured outputs and
tool-forced schemas — is correct and CONFIRMED in substance. But it must be stated with the model scope
attached, because **the exceptions are all Haiku 4.5**, the cheap tier a cost-driven scenario most often
points at. The clean formulation: *the newer and more expensive the tier, the fewer request-shaping knobs
it accepts; the levers that survive across the whole lineup are prompt content, structured outputs, and
`max_tokens`.*

---

## Volatile-facts verification table

One row per dossier volatile fact (the dossier's table runs to 56 rows, not 48 — the count in the task
brief is low), plus draft-only claims at the end. Verdicts: `CONFIRMED | CONTRADICTED | NOT-FOUND |
SCOPE-WRONG`.

| # | Fact | Location | Verdict | Source | Correct value / note |
|---|---|---|---|---|---|
| 1 | Recommended default model = Opus 5.5 | dossier, draft §1/§4.1 | CONFIRMED | D02-V01, D02-V03 | "If you're unsure which model to use, start with Claude Opus 5.5 for most workloads" (V01); "Most workloads start with Claude Opus 5.5." (V03) |
| 2 | Fable 5.1 = highest-capability widely released | dossier, draft §4.1 | CONFIRMED | D02-V03 | "Claude Fable 5.1 (`claude-fable-5-1`) is Anthropic's most capable widely released model." |
| 3 | Sonnet 5 = balanced tier | dossier | CONFIRMED | D02-V01 | "The best combination of speed and intelligence" |
| 4 | Haiku 4.5 alias / pinned ID | dossier | CONFIRMED | D02-V01 | ID `claude-haiku-4-5-20251001`, alias `claude-haiku-4-5`; Google Cloud `claude-haiku-4-5@20251001` |
| 5 | Opus 5.5 $4 / $20 | dossier, draft | CONFIRMED | D02-V01, D02-V02, D02-V19 | — |
| 6 | Opus 5.5 cache $5 (5m) / $8 (1h) / $0.20 read = 0.05x | dossier, draft §4.5 | CONFIRMED | D02-V02, D02-V19 | Footnote 2: "Cache hits and refreshes on Claude Opus 5.5 are priced at 0.05x the base input price." |
| 7 | Fable 5.1 $10/$50; $12.50 / $20 / $0.25 = 0.025x | dossier, draft §4.5 | CONFIRMED | D02-V02, D02-V22 | Footnote 1 confirms 0.025x for Fable 5.1 **and Mythos 5.1** |
| 8 | Sonnet 5 $2/$10 is now standard; $3/$15 rise cancelled | dossier | CONFIRMED | D02-V02 | Footnote 3: "…is now the standard price. The previously scheduled increase to $3/$15 … will not occur." |
| 9 | Haiku 4.5 $1/$5; $1.25 / $2 / $0.10 | dossier | CONFIRMED | D02-V02 | — |
| 10 | Opus 5 (legacy) $5/$25; $0.50 read | dossier | CONFIRMED | D02-V02 | Also $6.25 (5m) / $10 (1h) |
| 11 | 1M-context model list; 200K on Haiku 4.5 and Sonnet 4.5 | dossier, draft item 10 | CONFIRMED | D02-V08, D02-V01 | Docs list also includes Claude Mythos Preview |
| 12 | 1M is default, no beta header, standard pricing | dossier, draft item 10 | CONFIRMED | D02-V08, D02-V02 | "Claude 4.6 and later models … include the full 1M token context window at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.)" — **there is no tiered long-context premium anywhere** |
| 13 | Max output 128K / 64K; Batch 300K with `output-300k-2026-03-24` | dossier | CONFIRMED | D02-V01 | Model set: Opus 5.5, Opus 5, Sonnet 5, Opus 4.8, 4.7, 4.6, Sonnet 4.6 |
| 14 | Default effort `medium` Opus 5.5, `high` elsewhere, unsupported on Haiku 4.5 | dossier, draft §3 | CONFIRMED | D02-V05, D02-V01 | Effort `supportedModels` frontmatter contains no Haiku model |
| 15 | Levels `low`…`max`; `xhigh` not on every model with `max` | dossier | CONFIRMED | D02-V05 | `xhigh`: Fable 5.1/5, Mythos 5.1/5, Opus 5.5/5/4.8/4.7, **Sonnet 5**. `max` adds Mythos Preview, Opus 4.6, Sonnet 4.6. "Not every model that supports `max` supports `xhigh`." |
| 16 | `output_config.effort`, GA, no beta header | dossier, draft §3 | CONFIRMED | D02-V05 | "The top-level effort parameter is available on all supported models with no beta header required." |
| 17 | Opus 5.5 / Fable 5.1 thinking always on; `disabled` and `budget_tokens` → 400 | dossier, draft §3 | CONFIRMED | D02-V06, D02-V05, D02-V19, D02-V22 | See Claim 4 above |
| 18 | Sonnet 5: adaptive on by default, `disabled` accepted, `budget_tokens` → 400 | dossier | CONFIRMED | D02-V06, D02-V21 | `disabled` accepted "at any effort level" (D02-V20) |
| 19 | Haiku 4.5: extended only, off by default, rejects `adaptive` | dossier | CONFIRMED | D02-V06, D02-V21 | — |
| 20 | `thinking.display` default `omitted`; thinking billed regardless | dossier | CONFIRMED | D02-V21, D02-V06, D02-V08 | "Thinking tokens are billed as output tokens even when the thinking text is not returned." |
| 21 | Non-default sampling → 400 | dossier, draft §8 h.11 | SCOPE-WRONG | D02-V20, D02-V21, D02-V22 | Scope is Opus 4.7+ / Sonnet 5 / Fable-Mythos 5.x. Haiku 4.5 accepts `temperature` or `top_p`, one at a time |
| 22 | Prefill → 400 "on every current model" | dossier, draft §3 | SCOPE-WRONG | D02-V18, D02-V21 | Claude 4.6 generation onward; **Haiku 4.5 accepts prefill** |
| 23 | Forced `tool_choice` → 400 "also on `count_tokens` and Batches" | dossier | SCOPE-WRONG / NOT-FOUND | D02-V19, D02-V22, D02-V20 | Opus 5.5 / Fable 5.1 / Mythos 5.1 only; `count_tokens` CONFIRMED; **Batches NOT-FOUND**; Sonnet 5 accepts it |
| 24 | Max 4 `cache_control` breakpoints; automatic consumes one | dossier, draft §4.5, item 1 | CONFIRMED | D02-V07 | "the automatic cache breakpoint uses one of the 4 available breakpoint slots" |
| 25 | TTL write 1.25x / 2x; read 0.1x with per-model exceptions | dossier, draft §4.5 | CONFIRMED | D02-V07, D02-V02 | Read: 0.1x; 0.025x Fable 5.1 + Mythos 5.1; 0.05x Opus 5.5 |
| 26 | Cacheable-prefix minimums, non-monotonic | dossier, draft §5.1/§5.3/§6/§8 | CONFIRMED | D02-V07 | 512 (Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5) · 1,024 (Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4, Sonnet 4) · 2,048 (Mythos Preview, Opus 4.7, **Haiku 3.5**) · 4,096 (Opus 4.6, Opus 4.5, **Haiku 4.5**) |
| 27 | Render order `tools` → `system` → `messages` | dossier, draft §3/§4.5 | CONFIRMED | D02-V07, D02-V17 | "Cache prefixes are created in the following order: tools, system, then messages." |
| 28 | 20-position lookback; consecutive `tool_use` / `tool_result` runs collapse | dossier, draft §6, item 5 | CONFIRMED | D02-V07 | "The lookback window is 20 blocks… a run of consecutive `tool_use` blocks counts as one position, and so does a run of consecutive `tool_result` blocks" |
| 29 | Cache isolation: workspace on Claude API / Claude Platform on AWS / Foundry; org on Bedrock + Google Cloud | dossier, draft §5.1 | CONFIRMED | D02-V07 | Verbatim |
| 30 | Batch 50% off input and output, stacks with cache, 24 h | dossier, draft §5.3 | CONFIRMED | D02-V02, D02-V04 | "takes 50% off every token of a request, including cached ones" |
| 31 | Tokenizer ≈ 30% more tokens; recount per model | dossier, draft §5.6 | CONFIRMED | D02-V15, D02-V21, D02-V22 | "Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer… approximately 30 percent more tokens" |
| 32 | `count_tokens`: free, 5k/10k/20k RPM, estimate, rejects server tools + MCP + url/file | dossier | SCOPE-WRONG (minor) | D02-V15 | Tiers are named Start / Build / Scale. The **advisor tool is an explicit exception** — it is supported |
| 33 | Context editing: `context-management-2025-06-27`; `clear_tool_uses_20250919` + `clear_thinking_20251015`; trigger 100,000 / keep 3; thinking-clearing listed first | dossier, draft §4.6 | CONFIRMED | D02-V09 | Also `clear_at_least` None, `exclude_tools` None, `clear_tool_inputs` false |
| 34 | Compaction beta headers: `compact-2026-09-04` on demand; "the skill's `compact-2026-01-12` header is superseded" | dossier | SCOPE-WRONG | D02-V10, D02-V11 | `compact-2026-09-04` is the only beta header. `compact_20260112` is **not a header** — it is the threshold-compaction `context_management` *edit name*. The two forms in the researcher's note are a header and an edit, not two spellings of one header |
| 35 | Mid-conversation system messages: model set; not Sonnet 5; no header; `clear_at` beta | dossier, draft §4.8, item 3 | CONFIRMED | D02-V17, D02-V20 | Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 4.8, Opus 5. "This feature is not available on Claude Sonnet 5." Header for `clear_at`: `mid-conversation-system-clear-at-2026-08-21`. Platforms: Claude API, Bedrock, Google Cloud only |
| 36 | Per-message effort: `mid-conversation-output-config-2026-07-01`; Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5; preserves cache | dossier, draft item 3 | CONFIRMED | D02-V05, D02-V22, D02-V07 | Error on unsupported models: `output_config.effort requires a model that supports per-turn effort; this model does not` |
| 37 | Skills: `name` ≤64 / `description` ≤1024 / `display_name` ≤255 as SKILL.md frontmatter; ≤30 MB; `container.skills` max 20; code execution; workspace isolation | dossier, draft §3/§4.7 | SCOPE-WRONG (one part) | D02-V14 | All CONFIRMED **except**: SKILL.md frontmatter is `name` + `description` only. `display_name` is an API-level Skill field (≤255 chars, optional, non-unique), not frontmatter |
| 38 | Structured outputs shape, `additionalProperties: false`, `strict: true`, citations 400, format change invalidates cache, grammar cached 24 h | dossier, draft §3/§4.8 | CONFIRMED | D02-V12 | Docs word it "must be set to `false` for objects" rather than "required". Now GA — no beta header |
| 39 | Citations: per-document `enabled`, all-or-none, `char_location`/`page_location`/`content_block_location`, 0-/1-indexed, citation blocks not cacheable | dossier, draft §5.2 | CONFIRMED | D02-V13 | All end indices are **exclusive**; the incompatibility also covers `search_result` blocks |
| 40 | Tool-use system-prompt overhead 286 / 354 / 496 | dossier | CONFIRMED | D02-V02 | 286 Opus 5.5 and Opus 5 · 354 Sonnet 5 · 496 Haiku 4.5, Opus 4.5, Sonnet 4.5 (**497** on Opus 4.6 / Sonnet 4.6) |
| 41 | Overflow: 400 "prompt is too long"; `model_context_window_exceeded` on 4.5+ | dossier | CONFIRMED | D02-V08 | Earlier models can opt in with `model-context-window-exceeded-2025-08-26` |
| 42 | Context awareness on Sonnet 5 / 4.6 / 4.5 and Haiku 4.5; Opus 4.7+ and Fable/Mythos use task budgets | dossier | CONFIRMED | D02-V08 | `<budget:token_budget>` and `<system_warning>` injected automatically |
| 43 | Caching cut agent-loop cost by 2.7–5.3x; 83% / 88% on triage; median 84% read; top decile 94%+ | dossier; draft §11 only | CONFIRMED | D02-V04 | See `## Caching mechanics audit` for exactly what each figure measures |
| 44 | Effort curves (research flat; SWE-bench Pro deltas) | dossier, draft §4.3 | CONFIRMED | D02-V04 | `low` −1 to −3 pts for a third-to-half off; `medium` = default accuracy at 70–87% cost; Opus 5.5 SWE-bench Pro: `medium` −2.5 @ ~70%, `low` −8 @ ~33%, `xhigh` +1.4 @ 2.5x `high` |
| 45 | Cost-per-solved-task inversions (88.6% @ $0.54 vs 77.4% @ $0.84; 92.8% @ $0.22 vs 92.3% @ $1.19) | dossier, draft §3 | CONFIRMED | D02-V04 | Verbatim match |
| 46 | Failure re-run: `low` then re-run failures at `high` → ~97% @ $0.17 vs 95.3% @ $0.29 | dossier | CONFIRMED | D02-V04 | Docs add: "use this policy for the saving, not the lift" |
| 47 | `max_tokens`: "a 16K cap ended 1 in 14,000 turns" | dossier | CONTRADICTED | D02-V04 | Two separate facts were merged. At **64,000**, "2 of about 14,000 Claude Fable 5.1 turns at its default effort were still cut off (no Claude Opus 5.5 turn was)". The 16,384-token cap "ended about a quarter of Claude Opus 5.5's attempts and 43% of Claude Fable 5.1's" |
| 48 | `max_tokens`: only 1 of 66 capped attempts passed; cost per solved task unchanged; 64,000 recommended | dossier, draft §6/§7 | CONFIRMED | D02-V04 | Also "`max_tokens` caps a single response, **invisibly to the model**" — this confirms the draft's "the model never sees it" |
| 49 | Orchestrator: 21.6M-token corpus, Fable 5.1 + 25 Sonnet 5 workers, 47–55% cheaper, 10–12 pts lower, 2.3 h vs 15–20 | dossier, draft §4.2 | CONFIRMED | D02-V04 | — |
| 50 | Advisor: 90.1% @ $2.92 vs Opus 5.5 `high` 88.4% (~$1.40) and `xhigh` 91.1% ($4.11) | dossier, draft §4.2 | CONFIRMED | D02-V04 | 88.4% is derived from "1.7 points over Opus 5.5 alone at `high`"; the ~$1.40 is the $1.38 executor figure |
| 51 | Tool search "pays past roughly 10K tokens / ~20 tools" | dossier | NOT-FOUND (token figure) | D02-V23 | Docs give only a tool count: "Add tool search once your toolset grows past roughly 20 tools or your baseline context usage becomes noticeable." No token breakeven exists on that page |
| 52 | 502 tools: $0.56 flat vs $1.02, 45% less, no accuracy loss | dossier | CONFIRMED but misattributed | D02-V04 | These figures are on `optimizing-for-cost-and-intelligence`, **not** on `manage-tool-context`. Same for the 24%-fewer-input-tokens programmatic-tool-calling figure |
| 53 | Files API + code execution vs inlining: 6/25 @ $5.01 vs 25/25 @ $0.40 | dossier | CONFIRMED | D02-V04 | "about a twelfth as much" |
| 54 | Long-context ordering: documents at top, query last, up to 30% | dossier, draft §3 (implicit) | CONFIRMED | D02-V18 | Docs spell it "up to 30 percent … in tests" |
| 55 | Few-shot 3–5 examples, `<example>` tags, diversity | dossier, draft §4.4 | CONFIRMED | D02-V18 | "Include 3–5 examples for best results"; "Cover edge cases and vary enough that Claude doesn't pick up unintended patterns" |
| 56 | Sub-agent summaries "often 1,000–2,000 tokens" | dossier, draft §4.3 | CONFIRMED | D02-V26 | "returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)" |
| 57 | Fast mode: research preview, Claude API only, Opus 5.5 $8/$40, Opus 5 + 4.8 $10/$50, ~2.5x, not with Batch, error on Opus 4.7 | dossier | CONFIRMED | D02-V02, D02-V03 | Opus 4.6 runs at standard speed and bills at standard rates rather than erroring |
| 58 | `inference_geo: "us"` → 1.1x on all token categories, Claude 4.6+ | dossier | CONFIRMED | D02-V02 | Earlier models return 400 if the parameter is sent. Distinct from Bedrock/Google Cloud's 10% regional-endpoint premium |
| **Draft-only claims** | | | | | |
| 59 | "Adaptive thinking reliably drives better performance than extended thinking" | draft §3 | CONFIRMED | D02-V18 | "In internal evaluations, adaptive thinking reliably drives better performance than extended thinking." |
| 60 | Manual CoT is the thinking-off fallback; Opus 5 with thinking off can leak XML tags | draft §3/§8 h.10 | CONFIRMED | D02-V18, D02-V06 | V06: "This happens on Claude Opus 5 when thinking is disabled, most commonly on tool-heavy workloads" |
| 61 | Counter-instruction "Thinking adds latency…" | draft §4.3 | CONFIRMED | D02-V18 | Verbatim: "Thinking adds latency and should only be used when it will meaningfully improve answer quality - typically for problems that require multistep reasoning. When in doubt, respond directly." (plain hyphen, not em dash) |
| 62 | Opus 5 self-verification exception (over-verification) | draft §5.6 | CONFIRMED | D02-V18 | "Claude Opus 5 is the exception: it verifies its own work well without explicit instruction…" |
| 63 | Context rot definition and attention budget / n² | draft §3 | CONFIRMED | D02-V08, D02-V26 | Verbatim on both |
| 64 | Cached prefixes still occupy the window | draft §3/§4.5/item 10 | CONFIRMED | D02-V08 | "Cached prompt prefixes still occupy the context window: prompt caching changes what you pay for those tokens, not whether they count." |
| 65 | "The right altitude" definition | draft §3 | CONFIRMED | D02-V26 | "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics to guide behavior" |
| 66 | Aggressive compaction loses "subtle but critical context" | draft §4.6/§5.4 | CONFIRMED | D02-V26 | Verbatim |
| 67 | "Compaction isn't sufficient" for multi-window coherence | draft §4.6/§5.4 | NOT-VERIFIED THIS PASS | — | Cited to the long-running-harnesses blog (D02-S30), which I did not open. Editor must confirm the phrase before quoting it as a quotation |
| 68 | Caching breakeven: 5-minute on the 2nd request, 1-hour on the 3rd | draft §4.5 | CONFIRMED | D02-V02 | "caching pays off after one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write)" — now citable to a live doc, not only the bundled skill |
| 69 | "~1 turn in 20 pausing in that band" as the 1-hour-TTL rule of thumb | draft §4.5 | CONFIRMED | D02-V04 | Live docs carry a "1-in-20 rule"; reference 16 states the measured crossover is "about 3.3% of turns on Claude Sonnet 5 and 3.1% to 3.2% on Claude Opus 5.5" and that "The page's 1-in-20 rule sits above the measured crossover" |
| 70 | A read refreshes the TTL for free; generation time counts | draft §4.5 | CONFIRMED (first half) | D02-V07 | "The cache is refreshed for no additional cost each time the cached content is used." The "generation time counts against the TTL" half is NOT-FOUND in live docs — trace it or drop it |
| 71 | `max_tokens: 0` re-warm | draft §4.5 | CONFIRMED | D02-V07 | "The API reads your prompt into the model and writes the cache at any `cache_control` breakpoint, then returns immediately" — and it is rejected alongside `stream: true`, extended thinking, structured outputs, and forced `tool_choice` |
| 72 | Context editing "cost more than it saved" | draft §4.6/§5.4/§6 | CONFIRMED (sharpen) | D02-V04 | Verbatim: "context editing, a token-hygiene lever, cost more than it saved in the run measured in this section" and "On the 20-issue run they saved nothing, and context editing cost 74% more. On the long run the prune saved 39% and compaction 32%, while context editing changed nothing." |
| 73 | Thinking blocks are bound to the producing model; a router silently drops reasoning, unbilled | draft §4.2 | CONFIRMED | D02-V19, D02-V22 | "the request succeeds, and dropped blocks aren't billed" |
| 74 | "On work fitting one context, the coordinator's model alone at lower effort won **every time**" | draft §4.2 | SCOPE-WRONG | D02-V04 | Overstated. Docs give supporting cases ("on the full, harder BrowseComp set, Claude Fable 5 alone reached the coordinator configuration's accuracy at 22% to 30% lower cost"; DeepWideSearch `low` matched an orchestrator at 29% lower cost) **and a counter-case**: on the easy BrowseComp slice the coordinator cost about half on average and a third at p90 |
| 75 | `tool_choice` invalidates the tools and system caches but **not** the messages cache | draft §9 item 3 rationale | CONTRADICTED | D02-V07 | Exactly inverted. Row reads `Tool choice ✓ ✓ ✘` with legend "✘ indicates that the cache is invalidated, while ✓ indicates that the cache remains valid" and note "Changes to `tool_choice` parameter only affect message blocks" |
| 76 | "The restriction is on the request, so wrapping it in a `strict` tool does not help" | draft §5.2, item 4 | NOT-FOUND | D02-V12, D02-V13, D02-V25 | No page states a citations ↔ `strict: true` conflict |
| 77 | Context editing's supported-model set is self-contradictory in live docs | draft §11 UNVERIFIED | CONTRADICTED | D02-V09 | The page makes exactly one availability claim: "Context editing is available on all supported Claude models." There is no `supportedModels` frontmatter and no "Available on:" line. The list the researcher read as an availability statement is the **thinking-block-clearing default** table (Opus 4.5+/Sonnet 4.6+/Haiku through 4.5/Fable-Mythos all) |
| 78 | Skills are "workspace-scoped"; multi-tenant needs a workspace per tenant | draft §3/§4.7/§5.5/item 8 | CONFIRMED | D02-V14 | "The workspace is the isolation boundary for custom Skills, so a workspace per tenant gives each tenant's Skills hard isolation." Also: "Each organization can have up to 100 workspaces by default" — which bounds the §5.5 (60 carriers) and item 8 (40 tenants) designs, both fine |
| 79 | `"latest"` in production means any re-upload changes behavior with no deploy | draft §4.7/§7/item 8 | CONFIRMED | D02-V14 | "a version uploaded by anyone in the workspace immediately changes what your production agents run" |
| 80 | Skills use "progressive disclosure" | draft §3/§4.6 | NOT-FOUND (as docs' term) | D02-V14 | The words never appear. The mechanism is documented as "Metadata discovery: Claude sees metadata for each Skill (name, description) in the system prompt" + "Claude loads full Skill instructions only when needed." Keep the mechanism, drop the doc attribution for the label |
| 81 | 13% weight, ≈8 of 63 items, five objectives verbatim, Sample 2 | draft §1/§2 | CONFIRMED | D02-V27 | Objectives and Sample 2 match the guide word for word |

**Counts:** CONFIRMED 63 · SCOPE-WRONG 8 · CONTRADICTED 4 · NOT-FOUND 5 · not verified this pass 1.

---

## Caching mechanics audit

Every caching claim in the chapter, with its live-doc citation. All from D02-V07 (`prompt-caching`) unless
noted.

| Claim | Verdict | Live-doc wording |
|---|---|---|
| `cache_control` type value | CONFIRMED | "Currently, 'ephemeral' is the only supported cache type, which by default has a 5-minute lifetime." |
| Placement: on individual content blocks (explicit) or one top-level field (automatic) | CONFIRMED | "Automatic caching: Add a single cache_control field at the top level of your request… Explicit cache breakpoints: Place cache_control directly on individual content blocks" |
| Automatic places the breakpoint on the **last cacheable block** and advances with the conversation | CONFIRMED | Verbatim. This is the mechanism behind the draft's "surcharge" case and behind item 1 |
| Automatic is the docs' own starting recommendation | CONFIRMED — draft should acknowledge | "This is the recommended starting point for most use cases." The draft's §4.5 discriminator is compatible but reads as neutral; say that automatic is the default advice and explicit is the exception |
| 4 breakpoints maximum; automatic uses one slot | CONFIRMED | "the automatic cache breakpoint uses one of the 4 available breakpoint slots" |
| Prefix order `tools` → `system` → `messages`; the full prefix is hashed up to the breakpoint | CONFIRMED | "Cache prefixes are created in the following order: tools, system, then messages. This order forms a hierarchy…" |
| 20-block lookback; parallel tool runs collapse; lookback finds only entries already written | CONFIRMED | "The lookback window is 20 blocks… The lookback can only find entries that earlier requests already wrote… Add a second breakpoint closer to that position from the start" |
| TTL: 5-minute default 1.25x write; 1-hour 2x write | CONFIRMED | D02-V02 pricing table rows |
| Cache read 0.1x base input | CONFIRMED | D02-V02: "A cache hit costs 10% of the standard input price" |
| **Per-model read economics** | CONFIRMED | Fable 5.1 **0.025x** ($0.25) · Mythos 5.1 **0.025x** ($0.25) · Opus 5.5 **0.05x** ($0.20) · Opus 5 0.1x ($0.50) · Sonnet 5 0.1x ($0.20) · Haiku 4.5 0.1x ($0.10). **Fable 5 is 0.1x ($1.00)** — only the *.1* models get the quarter-price read. The draft's "0.1x (0.05x Opus 5.5, 0.025x Fable 5.1)" is exactly right |
| Breakeven: 5-minute after 1 read, 1-hour after 2 | CONFIRMED | D02-V02: "caching pays off after one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write)" |
| TTL choice on the inter-request gap; a read refreshes free | CONFIRMED | "The cache is refreshed for no additional cost each time the cached content is used." + "If you have prompts that are used at a regular cadence (…more frequently than every 5 minutes), continue to use the 5-minute cache… The 1-hour cache is best used… When you have prompts that are likely used less frequently than 5 minutes, but more frequently than every hour." |
| "~1 turn in 20" band for the 1-hour TTL | CONFIRMED | D02-V04 reference 16: measured crossover "about 3.3% of turns on Claude Sonnet 5 and 3.1% to 3.2% on Claude Opus 5.5"; "The page's 1-in-20 rule sits above the measured crossover" — i.e. deliberately conservative. State it that way |
| Keep-alive beats the 1-hour TTL on Fable 5.1 | CONFIRMED | D02-V04 reference 19: "On Claude Fable 5.1, at 0.025x, keep-alive was cheaper even with a pause before every turn, except at 45-minute pauses." On Opus 5.5, keep-alive was 8–18% cheaper at 5–10% of turns paused |
| Minimum cacheable prefix per model; below it, caching is silently skipped | CONFIRMED | Full table in row 26 above. No error is raised — the draft's "no error, both counters zero" is the right operational cue |
| **Invalidation — tool definitions** | CONFIRMED | `✘ ✘ ✘` — "Modifying tool definitions (names, descriptions, parameters) invalidates the entire cache" |
| **Invalidation — `tool_choice`** | **CONTRADICTED in the draft** | `✓ ✓ ✘` — "Changes to `tool_choice` parameter only affect message blocks." Tools and system caches **remain valid**; the messages cache is invalidated |
| **Invalidation — top-level `effort`** | CONFIRMED | "Changing the `output_config.effort` value always invalidates message blocks, with the same model-specific effect on tool and system caches as thinking parameters. **Setting effort explicitly to the model's default is equivalent to omitting it and does not invalidate.** On models that support per-message effort, an effort change carried in a `role: "system"` message inside `messages` leaves the cached prefix intact." |
| Invalidation — thinking configuration | CONFIRMED | Model-specific on tools/system, always invalidates messages. D02-V06 adds the diagnostic: "`cache_read_input_tokens` falls to zero on requests that previously hit the cache" |
| Invalidation — images, web-search toggle, citations toggle, `speed: "fast"` | CONFIRMED | Citations toggle and web-search toggle "modif[y] the system prompt" (`✓ ✘ ✘`); images affect message blocks (`✓ ✓ ✘`); speed invalidates system and message caches |
| Invalidation — `output_config.format` | CONFIRMED | D02-V12: "Changing the `output_config.format` parameter will invalidate any prompt cache for that conversation thread" |
| Invalidation — dropped thinking blocks | CONFIRMED (missing from draft) | New row: when the API drops a Fable 5.1 / Mythos 5.1 / Opus 5.5 thinking block, "the cached prefix changes from that block's position onward on that request" |
| Invalidation — model switch | CONFIRMED | Caches are scoped to the model; no escape hatch. Also note D02-V22's fallback credit: "For Claude Fable 5.1, fallback credit refunds the prompt-cache cost of switching models" — a real nuance for refusal-fallback designs |
| Context editing invalidates from the clear point; `clear_at_least` exists to justify it | CONFIRMED | D02-V09: "Tool result clearing: Invalidates cached prompt prefixes when content is cleared… Use the `clear_at_least` parameter to ensure a minimum number of tokens is cleared each time." |
| Thinking-block clearing preserves the cache when blocks are **kept** | CONFIRMED (missing from draft) | D02-V09: "When thinking blocks are kept in context (not cleared), the prompt cache is preserved… When thinking blocks are cleared, the cache is invalidated at the point where clearing occurs." |
| Task-budget changes invalidate the prefix | CONFIRMED (missing from draft) | D02-V16 / D02-V04: "set it once, on the first request" |
| Usage fields and total | CONFIRMED | `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`; `input_tokens` is the uncached remainder after the last breakpoint |
| Isolation: workspace (Claude API, Claude Platform on AWS, Microsoft Foundry) vs organization (Bedrock, Google Cloud) | CONFIRMED | Verbatim |
| Cannot cache: thinking blocks directly, citation sub-blocks, empty text blocks | CONFIRMED | "the top-level document content blocks that serve as the source material for citations can be cached" |
| Concurrency | CONFIRMED (missing from draft) | "a cache entry only becomes available after the first response begins. If you need cache hits for parallel requests, wait for the first response before sending subsequent requests." Worth a failure-mode row: a fan-out that fires N parallel requests on a cold prefix pays N writes |

### Per-model economics, stated correctly for the chapter

> A cache read costs 10% of base input on most models, **5% on Claude Opus 5.5** ($0.20/MTok against $4)
> and **2.5% on Claude Fable 5.1 and Claude Mythos 5.1** ($0.25/MTok against $10). Writes are 1.25x base
> input for the 5-minute TTL and 2x for the 1-hour TTL on every model. So the read discount, not the
> per-token list price, is what decides a long agentic session's bill: Fable 5.1 reads its prefix at a
> quarter the rate Fable 5 did, which is most of why Fable 5.1 "matches Claude Fable 5's score for 43%
> less per solved task" [D02-V02, D02-V04, D02-V22]. It also inverts the TTL decision: at 0.025x, a
> `max_tokens: 0` keep-alive on the 5-minute cache beats buying the 1-hour TTL at almost any pause
> length [D02-V04 ref. 19].

---

## The caching-impact discrepancy — ruling

**The two figures are not two co-equal Anthropic sources.**

| Figure | Source | What it actually measures |
|---|---|---|
| **2.7 to 5.3x** | D02-V04, live platform doc | *Cost.* "it cut agent-loop cost by a factor of 2.7 to 5.3 on this guide's benchmarks and cut a small triage agent's bill by 83%, or 88% with input trimming added." The levers table repeats it in the Cost column and separately marks latency "Faster." The supporting run: DeepResearch Bench II, "Claude Fable 5.1 falls from $37.94 to $7.12 per task and Claude Sonnet 5 from $3.20 to $1.20", reading "79% to 90% of their input tokens from the cache" |
| **2.5 to 3.7x at 81–90% hit rates** | bundled `claude-api` skill, `shared/cost-optimization.md` (dossier D02-S04) | A **cached snapshot** of the same guide, stamped 2026-06-24 per `VERIFIED-FACTS.md`. It measures the same thing (agent-loop cost) on an earlier set of runs at an earlier model lineup |

**Ruling for the chapter.** This is not a live contradiction between two Anthropic publications; it is a
stale local snapshot versus the current live page, and `VERIFIED-FACTS.md` already states the resolution
rule ("live docs win on every fact"). Therefore:

1. Delete the framing "two Anthropic sources differ" from §11. It grants the stale skill parity it has
   not earned and it will mislead the consolidation session.
2. Do **not** put any multiplier in the body. The draft is already right to omit it — keep that.
3. Where a magnitude is genuinely needed, cite the live figure with its scope attached and the two
   companion numbers that are more durable and more useful to an architect: the **median 84% cache-read
   share** and the **≈3% crossover** for the 1-hour TTL.
4. The 84% figure needs its population stated or it is misleading. It is not per request and not per
   conversation: D02-V04 reference 17 defines it as the median over **303,003 organization-days across
   106,487 organizations** in the 14 days ending 2026-08-23, where an organization-day counts as an agent
   loop only if its requests carry tool definitions and tool results, average 9+ prior tool calls, use
   caching, and number at least 10. Docs also give the actionable threshold: "Below about 80%, look for
   something breaking the cache."

Silently picking one figure would have been a finding. The draft did not do that — it declared both. The
remaining defect is only the parity framing.

---

## Corrections required

`[SEVERITY] location — problem — required fix`

**[BLOCKER] §9 item 3 (and its rationale) — inverted cache-invalidation fact; key wrong; item
unanswerable as posed.** Live docs: `tool_choice` leaves the tools and system caches valid and
invalidates the messages cache (D02-V07). With D removed from the correct set, only A is correct while
the item demands two. Replace the whole item with:

> **3 (select two).** A long agentic conversation on Claude Opus 5.5 relies on prompt-cache hits across
> turns. Which two changes leave the existing cached prefix intact?
> A. Appending a `{"role":"system"}` message immediately after the latest user turn.
> B. Editing the top-level `system` field.
> C. Changing top-level `output_config.effort` from `high` to `low`.
> D. Carrying the same effort change in a `{"role":"system","content":[],"output_config":{"effort":"low"}}`
> message with the `mid-conversation-output-config-2026-07-01` beta header.
> E. Changing `tool_choice` from `auto` to `none`.
>
> **A and D.** A mid-conversation system message is appended after the cached prefix, so the prefix hash
> is unchanged and "the next request still reads it from cache" [D02-V17]; the per-message effort form
> "leaves the cached prefix intact" where a top-level change does not [D02-V07, D02-V05]. **B** rewrites
> the prefix ahead of the whole conversation. **C** "always invalidates message blocks" — and note that
> setting effort explicitly to the model's default is *not* a change and does not invalidate [D02-V07].
> **E** invalidates the messages cache; the tools and system caches survive, but in a long conversation
> the message history is the cache that matters [D02-V07].

**[BLOCKER] §3 (Structured outputs concept), §8 heuristic 11, §9 item 9 rationale — prefill and sampling
scope over-generalized to "every current model."** Haiku 4.5 is current and accepts both. Replace:

- §3: "…now that assistant prefill returns 400 on every current model" →
  "…now that assistant prefill returns 400 from the Claude 4.6 generation onward — Opus 5.5, Fable 5.1 and
  Sonnet 5 — with Claude Haiku 4.5 the one current model that still accepts it [D02-V18, D02-V21]."
- §8 heuristic 11 first sentence → "**`temperature` is not a lever above the Haiku tier.** Non-default
  `temperature`/`top_p`/`top_k` return 400 on Opus 4.7 and later, Sonnet 5, and Fable 5.1; Haiku 4.5 still
  accepts `temperature` or `top_p`, one at a time. Determinism comes from schemas, not sampling."
- §9 item 9 rationale for A → "**A** returns 400 on every model that also rejects prefill except Haiku 4.5;
  and `temperature = 0` never guaranteed identical outputs even where it was accepted [D02-V20]."
- §9 item 9 rationale for C → "**C** returns 400 on Opus 5.5, Fable 5.1 and Mythos 5.1, where forced tool
  use is unsupported; Sonnet 5 still accepts it, so C is a model-scoped workaround rather than a portable
  answer [D02-V19, D02-V20]."

**[MAJOR] §5.2 "Why the alternatives lose" and §9 item 4 rationale for D — unsupported claim that a
`strict` tool inherits the citations restriction.** Replace both occurrences:

- §5.2 → "Citations plus `output_config.format` in one request returns **400**; the documented conflict is
  with `output_config.format` specifically, on `document` and `search_result` blocks [D02-V13]. A `strict`
  tool is not the way around it either, but for a different reason: `strict: true` guarantees the *shape*
  of the recorded finding, not the provenance of the quote inside it, so a `source_quote` field is still
  model-generated text [D02-V12]."
- §9 item 4 rationale for D → "**D** fails for the same reason as C, not for A's reason: `strict: true`
  constrains the tool input's schema, so the `quote` field is still model-generated. Docs document no
  citations ↔ `strict: true` conflict, and they describe JSON outputs and strict tool use as separable
  features that can be combined [D02-V12, D02-V25]."

**[MAJOR] §11 "Remaining `[UNVERIFIED]`" bullet 1 — the doc contradiction it reports does not exist.**
`context-editing` makes exactly one availability claim. Replace with:

> - Context editing's availability: the page states "Context editing is available on all supported Claude
>   models" [D02-V09] and carries no per-model support list. The per-model table on that page governs the
>   **default for thinking-block clearing** (keep all prior thinking on Opus 4.5+, Sonnet 4.6+ and all
>   Fable/Mythos models; keep only the last turn on Opus 4.1 and earlier, Sonnet 4.5 and earlier, and every
>   Haiku model through 4.5), not availability. Verify per model before designing around the clearing
>   *defaults*, not around support.

**[MAJOR] §11 "Remaining `[UNVERIFIED]`" bullet 3 — remove the "two Anthropic sources" parity framing.**
Replace with:

> - Prompt caching's measured cost impact: the live platform guide reports "a factor of 2.7 to 5.3" on its
>   own agent-loop benchmarks, plus 83% (88% with input trimming) on a triage agent [D02-V04]. The narrower
>   2.5–3.7x range circulating in the bundled `claude-api` skill is a June 2026 snapshot of the same guide
>   and is superseded. No multiplier is used in this chapter; the durable numbers are the median 84%
>   cache-read share across agent-loop organization-days and the "below about 80%, look for something
>   breaking the cache" threshold [D02-V04].

**[MAJOR] §4.2 — "won every time" overstates the evidence.** Replace with: "on the work measured that fits
one context window, the coordinator's own model at lower effort matched or beat the orchestrator at 22–30%
lower cost; on an easier slice the coordinator was the cheaper insurance, halving average cost and cutting
the 90th percentile from $33 to $12. Measure your own tail before choosing [D02-V04]."

**[MAJOR] §10 objective-coverage table — every cross-reference in three of five rows points at the wrong
section**, which breaks the mandatory traceability in AGENT-BRIEF §3.10. Correct mapping: guardrails are
**§4.8** (not §4.6/§4.7); context-window strategy is **§4.6** (not §4.5); caching is **§4.5** and prompt
reuse is **§4.7** (not §4.4/§4.6). Re-derive the table against the final section numbers.

**[MAJOR] coverage gap — context awareness and task budgets are absent.** The chapter's Objective-4
material implies the model manages its own remaining window, but this is model-dependent and is a clean
architectural discriminator. Add one row or paragraph: "Claude Sonnet 5, Sonnet 4.6, Sonnet 4.5 and Haiku
4.5 receive an injected `<budget:token_budget>` and post-tool `<system_warning>`; you enable nothing and
you never send the tags yourself. Claude Opus 4.7 and later Opus models and the Fable/Mythos models do
**not** — there you give the model an explicit allowance with **task budgets** (beta,
`task-budgets-2026-03-13`, 20,000-token floor, advisory not enforced, `max_tokens` remains the only
enforced cap), and you set it once because changing it mid-task invalidates the cached prefix
[D02-V08, D02-V16, D02-V04]." Note also that a budget obviously too small for the task "may [cause the
model to] decline to attempt the task at all" [D02-V16] — a good failure-mode row.

**[MAJOR] §4.5/§4.6/§6 — the thinking-block prefix binding is missing, and it changes the advice.** On
Fable 5.1 and Opus 5.5, editing anything before a thinking block does not merely cost a cache miss; for
accounts created on or after **2026-08-31** it returns a **400** (`The block is bound to a different
conversation`). Add to §4.6 and to the failure-mode table:

> On Claude Fable 5.1 and Claude Opus 5.5 the conversation must be **append-only**. Editing, reordering or
> removing an earlier turn, injecting a per-turn reminder you delete next request, or rebuilding `system`
> or `tools` invalidates every later thinking block; the request is rejected with a 400 unless you send
> `thinking-binding-controls-2026-08-01` with `prefix_mismatch_behavior: "drop_block"`. Server-side
> compaction and context editing never trigger it, and moving `cache_control` markers and changing `effort`
> between requests are explicitly safe. Use mid-conversation system messages (turn-scoped, beta
> `mid-conversation-system-clear-at-2026-08-21`) instead of inject-and-delete [D02-V22, D02-V06, D02-V09].

This is the single most valuable fact the chapter is currently missing: it converts "don't rewrite history"
from a caching optimization into a hard API constraint.

**[MINOR] §3 (Agent Skill) — `display_name` is not SKILL.md frontmatter.** Replace "with `SKILL.md`
(frontmatter `name`, `description`, optional `display_name`)" with "with `SKILL.md` (frontmatter `name`,
≤64 chars lowercase/digits/hyphens and no reserved words 'anthropic' or 'claude', plus `description`,
≤1024 chars) — `display_name` is an optional API-level field, ≤255 characters, derived from `name` when
omitted [D02-V14]."

**[MINOR] §4.6 — sharpen the context-editing economics with the measured numbers.** Replace "in the run
measured for the platform docs it *cost more than it saved*" with "on the short (20-issue) run it cost 74%
more and saved nothing; on the long run it changed nothing, while a hand-written prune at task boundaries
saved 39% and server-side compaction 32% [D02-V04]." The prune is the more useful teaching point and it is
documented.

**[MINOR] §4.5 — two small attribution fixes.** (a) The claim that "generation time counts against the
TTL" is NOT-FOUND in live docs; either trace it or drop it — the refresh half is confirmed. (b) Note that
docs call automatic caching "the recommended starting point for most use cases," so the discriminator
should read as "automatic by default; go explicit when…" [D02-V07].

**[MINOR] §4.6/§3 — "progressive disclosure" is the course's label, not the docs'.** Keep the mechanism,
drop the implied doc attribution: the documented wording is that Claude "sees metadata for each Skill
(name, description) in the system prompt" and "loads full Skill instructions only when needed" [D02-V14].

**[MINOR] §4.8 / item 6 — add the live-doc citation for least privilege.** D02-V24: "Apply the principle
of least privilege so that a successful injection can do minimal damage: don't give Claude access to
secrets it doesn't need, run tools in sandboxed environments, and scope permissions as narrowly as
possible." Currently only the exam guide is cited for this.

**[NIT] §5.3 — flag the enum-size risk.** A 380-value string enum is within documented JSON-Schema support,
but structured outputs enforce complexity limits and a 180-second grammar-compilation timeout, and over-limit
schemas fail with "Schema is too complex for compilation" [D02-V12]. Add a half-sentence telling the reader
to compile it once before committing to the design.

**[NIT] §6 — add three rows now that they are verified:** parallel fan-out on a cold prefix pays N cache
writes because "a cache entry only becomes available after the first response begins" [D02-V07]; `stop_reason:
"refusal"` arrives as HTTP 200 with `stop_details` on Opus 5.5, Fable 5.1 and Sonnet 5 [D02-V19, D02-V22,
D02-V21]; and progress text that "goes quiet between tool calls" after a migration is the `thinking.display`
default of `"omitted"`, not a hang [D02-V19].

---

## Answer-key audit

I solved all ten items independently before reading the keys.

| # | Key | Verdict | Notes |
|---|---|---|---|
| 1 | B | **KEY-CORRECT** | Uniquely best and now doubly supported: automatic caching places the breakpoint on the last cacheable block (the unique excerpt), and "the lookback can only find entries that earlier requests already wrote" [D02-V07]. A is correctly dead (reads refresh free; 20-second cadence keeps a 5-minute entry warm). C and D fail as stated; D's "the limit is 4" is right. No volatile dependency — no model, price or default is load-bearing. |
| 2 | C | **KEY-CORRECT** | Matches the documented gate verbatim: "If your evals at `xhigh` or `max` effort still fall short on demanding reasoning or long-horizon agentic work, move to Claude Fable 5.1" [D02-V03]. A is well-refuted by the advisor data; B is a backstop; D is refuted by "lowering effort beat an architecture change" on DeepWideSearch [D02-V04]. Model-free stem — good. |
| 3 | A and D | **KEY-WRONG** | D is inverted against D02-V07 (see BLOCKER 1). With D excluded only A remains, so the stated count is unachievable. Replacement item supplied in `## Corrections required`. |
| 4 | B | **KEY-ARGUABLE** | B is right and the 400 is confirmed [D02-V13, D02-V12]. But D's stated failure ("the restriction applies to the request") is NOT-FOUND, and docs describe strict tool use as combinable with JSON outputs — so a candidate who has read `structured-outputs` can defend D. Repair the rationale as specified; the key then stands. |
| 5 | B | **KEY-CORRECT** | The stem is carefully built: "byte-identical" kills C, "preserves prior thinking blocks" kills the stripping cause, and a *sequential* 30-call chain is not a consecutive run of one block type, so it does not collapse to one position — 20 is exceeded [D02-V07]. A is refuted by free refresh; D by the conversation's size. Add the docs' own fix wording ("Add a second breakpoint closer to that position from the start"). |
| 6 | A and C | **KEY-CORRECT** | Both are documented: "Put untrusted content only in tool results… Claude is trained to treat instructions that appear inside tool results with appropriate skepticism" and the least-privilege bullet [D02-V24]. Tighten B's rationale so it is clear that B is *also* recommended by docs ("State the policy in your system prompt") but is a behavioral prior — otherwise the item reads as though B were bad advice. D is detective; E is not a boundary. |
| 7 | A | **KEY-CORRECT** | Verbatim-supported: "prompts written for Claude Opus 4.8 cost 36% more per ticket on Claude Opus 5 for no change in accuracy… the audit made Opus 5 both cheaper (by 14%) and more accurate (97% of tickets, up from 92%)" [D02-V04]. C's rationale is right to send the tokenizer check second. D's rationale ("a cold period, not a sustained third") is sound. |
| 8 | B | **KEY-CORRECT** | Strongly supported: the workspace is the isolation boundary, docs explicitly prescribe a workspace per tenant for multi-tenant platforms, and pinning bounds the blast radius while `"latest"` does not [D02-V14]. 40 tenants sits inside the documented 100-workspace default. Uniquely best. |
| 9 | B | **KEY-CORRECT**, rationales need scope | B is the documented migration for prefill on every model that rejects it [D02-V18, D02-V12]. But A and C are only 400s on subsets, and the stem names no target model, so the rationales must carry the scope (fix supplied above). Once scoped, B remains uniquely best because it is the only option that is correct on all of Opus 5.5, Fable 5.1 and Sonnet 5. |
| 10 | B and D | **KEY-CORRECT** · **VOLATILE-DEPENDENCY** | Both keys are verbatim-supported: "A 900k-token request is billed at the same per-token rate as a 9k-token request" [D02-V02] and "Cached prompt prefixes still occupy the context window" [D02-V08]. A, C, E all fail. **But the item's correctness rests on model specs**: option C encodes Haiku 4.5's 200K window, and the premise "the 1M-token context window" is true only of the 1M-window models. Either replace C with a non-model distractor ("It must be requested per model with a `context-1m` beta header") or accept that this item expires with the lineup. |

**Volatile-dependency flags:** item 10 (model window in option C). Items 1–9 are clean: none turns on a
price, a model ID, or a parameter default, and items 2 and 3 deliberately keep the stem model-free. That
is good item design and should be preserved — with the one exception that item 3's replacement names Opus
5.5 in the stem purely to make per-message effort available, which is a capability statement rather than a
spec lookup.

---

## Unresolvable / contradictory in the docs

**1. `Opus 5` vs `Opus 5.5` as the start-here model — a genuine live contradiction between two current
pages.**

- D02-V22 (`models/fable-5-1/whats-new-fable-5-1`, a *current-model* page):
  > "For most workloads, start with Claude Opus 5 (see Choosing a model). Use Claude Fable 5.1 for
  > demanding reasoning and long-horizon agentic work, or when your evals on **Claude Opus 5** at higher
  > effort still fall short."
- D02-V01 (`models/overview`):
  > "If you're unsure which model to use, start with **Claude Opus 5.5** for most workloads. Use Claude
  > Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on **Claude Opus
  > 5.5** at higher effort still fall short."

The Fable 5.1 page was written before Opus 5.5 shipped (2026-09-22) and has not been refreshed.
**Hedge the chapter must adopt:** cite `models/overview` and `choosing-a-model` for the start-here model
and say explicitly that the Fable 5.1 what's-new page still names Opus 5 because it predates the Opus 5.5
release — then use that as the chapter's live example of why a model ID is the least durable thing in a
prep course. Do not quote the Fable page for model selection.

**2. Where the "raise effort before changing model" sentence actually lives.** The phrasing the dossier
attributes to `choosing-a-model` ("or when your evals on Claude Opus 5.5 at higher effort still fall
short") is on `models/overview` and `optimizing-for-cost-and-intelligence`. `choosing-a-model` says
instead: > "If your evals at `xhigh` or `max` effort still fall short on demanding reasoning or long-horizon
agentic work, move to Claude Fable 5.1." Not a contradiction, but the chapter must quote whichever page it
cites. The *method* — default → optimize prompts for that model → evaluate → lower effort or downgrade →
only then change tier — is CONFIRMED verbatim on `choosing-a-model` Option 2, and "Tuning effort is often a
better lever than switching models" is CONFIRMED verbatim there too.

**3. The 1-in-20 TTL rule versus its own measurement.** Docs carry a "1-in-20" rule of thumb while the
underlying reference reports a measured crossover of 3.1–3.3% of turns and says outright that "the page's
1-in-20 rule sits above the measured crossover" [D02-V04 ref. 16]. That is a deliberate conservatism, not
an error. **Hedge:** state the rule *and* that it is deliberately above the ~3% measured crossover, so a
workload sitting between 3% and 5% is a measure-it case rather than a rule case.

**4. Reported-but-refuted: context editing's supported-model set.** The researcher reported this as
self-contradictory. It is not. The page states one availability claim ("all supported Claude models") and
separately tabulates thinking-clearing *defaults*. The chapter must not hedge availability; it should hedge
the clearing defaults instead. Recording this as a finding because a fabricated doc contradiction in a
prep course is as damaging as a fabricated fact.

**5. Reported-but-refuted: compaction's beta header "in two forms."** `compact-2026-09-04` is the only
beta header [D02-V10, D02-V11]. `compact_20260112` is the threshold-compaction `context_management` edit
name [D02-V09, D02-V11]. Also note the authoritative on-demand support set lives in
`compaction-on-demand` frontmatter — 12 models, **no Haiku model**, and **Amazon Bedrock: not available** —
while the `compaction` overview page carries no support metadata at all.

**6. Unknowable, and the draft handles it correctly.** Whether the July 2026 item bank was authored against
the pre-Opus-5.5 lineup. Domain 2's published objectives name no model [D02-V27], so teaching the method
and treating IDs and prices as perishable is the right posture. Keep §11's bullet on this.

---

## Volatility watchlist

Sorted by expected blast radius. Re-check every row at consolidation and before any republication. Every
page is also retrievable as raw Markdown at `<page-url>.md`, which exposes the `featureMetadata` /
`supportedModels` frontmatter — that is the fastest reliable re-check and it is how the support sets in this
file were read.

| # | Fact | Where it appears | Re-check trigger | Page to open |
|---|---|---|---|---|
| V1 | The four-model lineup, and which is the start-here model | §1, §4.1, §4.2, §5.x, §9 items 2/10 | **Any** model announcement; the lineup moved twice inside three months | D02-V01, D02-V03 |
| V2 | Opus 5 is legacy, not current | §1 | Any Opus release or deprecation notice | D02-V01, `about-claude/model-deprecations` |
| V3 | Default effort `medium` on Opus 5.5 / `high` elsewhere | §3, §4.1, §5.6, §7 | Any new model, or any Opus point release | D02-V05, D02-V01 |
| V4 | Which models reject `thinking: disabled` / `enabled` | §3, §6, §8 h.10, §9 item 9 | Any new model; the rejection table is the canonical page and changes per release | D02-V06 |
| V5 | Which models reject non-default sampling parameters | §3, §8 h.11, §9 item 9 | Any new model. **Scope currently excludes Haiku 4.5** — re-check on any Haiku release | D02-V20, D02-V21 |
| V6 | Which models reject prefill | §3, §9 item 9 | Any new Haiku release: Haiku 4.5 is the last current model accepting prefill | D02-V18, D02-V21 |
| V7 | Which models reject forced `tool_choice` | §3, §4.8, §6, §9 item 9 | Any new model. **Sonnet 5 currently accepts it** — that is the fact most likely to flip | D02-V19, D02-V22 |
| V8 | Per-model cache-read multipliers (0.1x / 0.05x / 0.025x) | §4.5, §5.1 | Any model launch or pricing note; these multipliers are new and per-model | D02-V02 |
| V9 | Minimum cacheable prefix per model (512 / 1,024 / 2,048 / 4,096) | §5.1, §5.3, §6, §8 h.9 | Any model launch. Non-monotonic across generations, so never interpolate | D02-V07 |
| V10 | Cache-invalidation table rows, especially `tool_choice`, `effort`, dropped thinking blocks | §4.5, §6, §9 item 3 | Any new request parameter; rows have been added (dropped thinking blocks, speed setting) | D02-V07 |
| V11 | Prices: $10/$50, $4/$20, $2/$10, $1/$5 and all cache rows | §3, §4.5, §5.x | Any pricing-page change; Sonnet 5's schedule already changed once | D02-V02 |
| V12 | No long-context premium above any threshold | §9 item 10 | Any new context-window tier or a 1M rollout to a new model | D02-V02 (`#long-context-pricing`), D02-V08 |
| V13 | Tokenizer ≈30% more tokens; 1M ≈ 555k words vs ≈750k pre-Opus-4.7 | §5.6 | Any tokenizer change; both figures are tokenizer-generation-specific | D02-V01 (Context window footnote), D02-V15 |
| V14 | Per-message effort beta header and its model set | §9 item 3 (replacement), §4.5 | Beta → GA transition, or a model added | D02-V05 |
| V15 | Mid-conversation system messages: model set, no-header status, `clear_at` beta | §4.8, §9 item 3 | Sonnet-tier support landing would change the guardrail advice materially | D02-V17 |
| V16 | Context editing beta header `context-management-2025-06-27` and strategy names | §4.6 | Beta → GA; strategy names are date-stamped and will be superseded | D02-V09 |
| V17 | Compaction: `compact-2026-09-04`, on-demand support set, Bedrock unavailability | §4.6, §5.4 | Beta → GA; threshold compaction has its own separate header | D02-V10, D02-V11 |
| V18 | Task budgets: `task-budgets-2026-03-13`, 20,000 floor, model set | new §4.6 material | Beta → GA; floor is described as "the current 20,000-token floor" | D02-V16 |
| V19 | Thinking-block prefix binding, the 2026-08-31 account cutoff, `thinking-binding-controls-2026-08-01` | new §4.6 / §6 material | The cutoff means enforcement broadens over time; re-check whether it has become universal | D02-V22, D02-V06 |
| V20 | Skills: 20 per request, 30 MB, 100 workspaces, out-of-beta status, no ZDR coverage | §3, §4.7, §5.5, §9 item 8 | Any Skills API change; it recently left beta | D02-V14 |
| V21 | Structured outputs GA status, schema limitations, complexity limits, 180 s compile timeout | §3, §4.8, §5.3 | GA features still gain schema support; `minItems` is currently limited to 0 or 1 | D02-V12 |
| V22 | Citations ↔ structured outputs 400 | §5.2, §9 item 4 | A docs note saying the two now interoperate would invalidate item 4 entirely | D02-V13, D02-V12 |
| V23 | Measured figures: 2.7–5.3x, 84%, effort curves, advisor/orchestrator, 502 tools, CSV run | §3, §4.2, §4.3, §11 | The optimizing page is re-measured per model generation; every figure is dated in its reference | D02-V04 |
| V24 | Context awareness model set; injected tag format | new §4.6 material | Any model launch; Opus and Fable models deliberately do not receive the tags | D02-V08 |
| V25 | Retirement dates (2027-09-01 / 2027-09-22 / 2027-06-30 / **2026-10-15**) | §1 (implicitly) | **Haiku 4.5's "not sooner than 2026-10-15" is three weeks out** — the most urgent row in this table | D02-V01, `about-claude/model-deprecations` |
| V26 | Batch 300K output beta `output-300k-2026-03-24` and its model set | §5.3 context | Beta → GA | D02-V01 |
| V27 | Fast mode pricing, research-preview status, platform exclusivity | not in draft; dossier only | Research preview → GA, or a platform gaining it | D02-V02 |
| V28 | ZDR interaction: Fable 5.1 **and** Mythos 5.1 are Covered Models with 30-day retention and are not ZDR-eligible without express authorization | cross-domain (D5); affects any "use Fable 5.1" recommendation in §4.1/§5.x | Any Covered-Models policy change | D02-V22, D02-V06 |
| V29 | `inference_geo` 1.1x; Bedrock/Google Cloud 10% regional premium | dossier only | Data-residency pricing changes | D02-V02 |
| V30 | Exam facts: 13%, ≈8 of 63, objectives, cut score 720 | §1, §2, §10 | Any exam-guide version after v1.0 (effective July 2026) | D02-V27 |

**Standing note for consolidation.** `VERIFIED-FACTS.md` describes Covered Models as "Mythos-class." Live
docs are broader: "Claude Fable 5.1 and Claude Mythos 5.1 carry 30-day data retention and aren't available
under zero data retention unless expressly authorized by Anthropic. Both are Covered Models, like Claude
Fable 5 and Claude Mythos 5" [D02-V22], and `thinking-troubleshooting` repeats that Fable 5.1, Mythos 5.1,
Fable 5 and Mythos 5 "are not available under zero data retention unless expressly authorized by Anthropic"
[D02-V06]. **The whole Fable family is Covered, not just Mythos.** That materially changes any Domain 2 or
Domain 5 recommendation that reaches for Fable 5.1 under a ZDR constraint, and `VERIFIED-FACTS.md` should
be amended. Recording it here as required by the file's standing instruction.

---

## Sources consulted

All accessed **2026-09-24**. `Type`: `anthropic-docs | anthropic-blog | exam-guide | other`.
`Trust`: `primary | secondary | low`.

| ID | Title | URL | Publisher/Author | Type | Accessed (YYYY-MM-DD) | Trust | Used for |
|----|-------|-----|------------------|------|-----------------------|-------|----------|
| D02-V01 | Models overview | https://platform.claude.com/docs/en/models/overview | Anthropic | anthropic-docs | 2026-09-24 | primary | Full current-model comparison table; IDs and aliases per platform; latency tiers; context windows; max output; default effort; thinking modes; knowledge and training cutoffs; retirement dates; legacy list; cache-read multiplier footnote; 1M ≈ 555k words vs ≈750k pre-Opus-4.7; pinned-snapshot statement; Batch 300K beta |
| D02-V02 | Pricing | https://platform.claude.com/docs/en/about-claude/pricing | Anthropic | anthropic-docs | 2026-09-24 | primary | Per-model input/output/cache-write/cache-read prices; the three cache-read multiplier footnotes; batch discount; **long-context pricing (no premium)**; caching breakeven sentence; tool-use system-prompt overhead table; fast-mode pricing; `inference_geo` 1.1x; Sonnet 5 standard-price footnote |
| D02-V03 | Choosing the right model | https://platform.claude.com/docs/en/about-claude/models/choosing-a-model | Anthropic | anthropic-docs | 2026-09-24 | primary | "Most workloads start with Claude Opus 5.5."; "Tuning effort is often a better lever than switching models."; efficiency-first and capability-first procedures verbatim; the xhigh/max gate to Fable 5.1; model-selection matrix; fast mode ~2.5x |
| D02-V04 | Optimizing for cost and intelligence | https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence | Anthropic | anthropic-docs | 2026-09-24 | primary | Caching 2.7–5.3x and what it measures; median 84% cache-read share and its population (ref. 17); effort curves; cost-per-solved-task inversions; failure re-run policy; `max_tokens` economics and "invisibly to the model"; advisor and orchestrator measurements; 502-tool result; CSV/Files-API result; prompt-audit 36%/14%/97-vs-92; context editing cost 74% more; prune 39% / compaction 32%; price-the-tail 43%; 1-in-20 TTL rule and the ~3% measured crossover (refs. 16, 19) |
| D02-V05 | Effort | https://platform.claude.com/docs/en/build-with-claude/effort | Anthropic | anthropic-docs | 2026-09-24 | primary | `output_config.effort`, GA, no beta header; `supportedModels` frontmatter (no Haiku); five levels with per-model `xhigh`/`max` availability; "Effort is a behavioral signal, not a strict token budget."; `max_tokens` hard-limit statements; `adaptive` is a thinking mode not an effort value; Opus 5.5 `disabled` → 400 at every level; per-message effort beta header and model set; top-level effort invalidates the cache; "run an effort sweep on your own evals"; `zdr.eligibility: eligible` with "Excludes Covered Models" |
| D02-V06 | Troubleshooting thinking | https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting | Anthropic | anthropic-docs | 2026-09-24 | primary | The authoritative per-model thinking support / default / rejected-with-400 table; extended-thinking deprecation and rejection scope; exact 400 error strings; Opus 5 `disabled`-at-`xhigh`/`max` footnote; thinking-block signature 400 and the 2026-08-31 account cutoff; effort/thinking config as part of the cached prefix; Opus 5 XML-tag leakage with thinking off; Fable/Mythos ZDR exclusion |
| D02-V07 | Prompt caching | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | Anthropic | anthropic-docs | 2026-09-24 | primary | 4 breakpoints and the automatic slot; `ephemeral`; per-model minimum cacheable prefix table; TTL multipliers; render order; **full invalidation table with its ✓/✘ legend and the `tool_choice` row**; effort/thinking invalidation rows; dropped-thinking-block row; 20-block lookback; workspace vs organization isolation; usage fields; what can/cannot be cached; automatic vs explicit and "the recommended starting point"; free refresh; concurrency caveat; `max_tokens: 0` pre-warming and its rejections; TTL selection guidance |
| D02-V08 | Context windows | https://platform.claude.com/docs/en/build-with-claude/context-windows | Anthropic | anthropic-docs | 2026-09-24 | primary | Context-rot definition; everything-counts statement; 1M default with no beta header and standard pricing; per-model 1M list; thinking-block preservation by model class; context awareness model set and injected tag format; "Cached prompt prefixes still occupy the context window"; overflow 400 and `model_context_window_exceeded`; 600-image limit |
| D02-V09 | Context editing | https://platform.claude.com/docs/en/build-with-claude/context-editing | Anthropic | anthropic-docs | 2026-09-24 | primary | Beta header `context-management-2025-06-27`; strategy names; all configuration defaults; **the single availability claim ("all supported Claude models") and absence of any `supportedModels` list**; thinking-clearing default table; cache-invalidation behavior per strategy; `clear_thinking_20251015`-first ordering; `count_tokens` preview and `original_input_tokens` |
| D02-V10 | Compaction overview | https://platform.claude.com/docs/en/build-with-claude/compaction | Anthropic | anthropic-docs | 2026-09-24 | primary | The three compaction forms; who-decides-when / recent-turns-verbatim / background comparison rows; `compact-2026-09-04` as the only header on the page; absence of support metadata |
| D02-V11 | Compaction on demand | https://platform.claude.com/docs/en/build-with-claude/compaction-on-demand | Anthropic | anthropic-docs | 2026-09-24 | primary | `betaHeader: compact-2026-09-04`; the 12-model `supportedModels` set (no Haiku) and `supportedPlatforms` (Bedrock not available); `compaction: {"type":"summarize"}` flow; rejected companions (`stop_sequences`, `output_config.format`, forced `tool_choice`); `compaction_block_misplaced` 400; `compact_20260112` as the threshold edit name |
| D02-V12 | Structured outputs | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | Anthropic | anthropic-docs | 2026-09-24 | primary | GA status and `supportedModels` (includes Haiku 4.5); `output_config.format` shape; `additionalProperties: false`; constrained-decoding guarantees; schema limitations and complexity limits; citations incompatibility sentence; prefill incompatibility; format change invalidates the cache; 24-hour grammar cache; JSON-outputs vs strict-tool-use separability and combinability |
| D02-V13 | Citations | https://platform.claude.com/docs/en/build-with-claude/citations | Anthropic | anthropic-docs | 2026-09-24 | primary | GA, all active models; `citations.enabled` per document and all-or-none; sentence chunking; the three location types with index bases and exclusive ends; the structured-outputs 400 warning including `search_result` blocks; caching the document not the citation block; `cited_text` token accounting |
| D02-V14 | Using Agent Skills with the API | https://platform.claude.com/docs/en/build-with-claude/skills-guide | Anthropic | anthropic-docs | 2026-09-24 | primary | Skill definition; SKILL.md frontmatter limits and `display_name` as an API-level field; 30 MB; `container.skills` max 20; code-execution prerequisite; version formats and the `"latest"` production caution; **workspace-scoped access warning and workspace-per-tenant guidance**; 100-workspace default; out-of-beta status; no-network/no-package-install constraints; Skills not ZDR-covered; "How Skills are loaded" (no "progressive disclosure" wording); **no Skill-vs-system-prompt-vs-tool table** |
| D02-V15 | Token counting | https://platform.claude.com/docs/en/build-with-claude/token-counting | Anthropic | anthropic-docs | 2026-09-24 | primary | `/v1/messages/count_tokens`; free; Start/Build/Scale 5,000/10,000/20,000 RPM and independent limits; estimate wording; rejected inputs **with the advisor-tool exception**; ~30% tokenizer statement and recount-per-model guidance; no words-per-token ratio on this page |
| D02-V16 | Task budgets | https://platform.claude.com/docs/en/build-with-claude/task-budgets | Anthropic | anthropic-docs | 2026-09-24 | primary | Definition and `output_config.task_budget` shape; `task-budgets-2026-03-13`; 20,000-token floor; "advisory, not enforced" and `max_tokens` as the enforced cap; refusal-like behavior on undersized budgets; cache invalidation on mid-task change; supported-model table (not Sonnet 5, not Haiku 4.5, not 4.6 models); countdown invisible in responses |
| D02-V17 | Mid-conversation system messages and tool changes | https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages | Anthropic | anthropic-docs | 2026-09-24 | primary | Supported-model list and the explicit Sonnet 5 exclusion; no beta header for the basic form; `clear_at` semantics and `mid-conversation-system-clear-at-2026-08-21`; cache-preservation mechanics and "append after the breakpoint"; placement rules and every documented 400; operator-over-user priority; not-for-untrusted-content warning; `tool_addition`/`tool_removal`, `inline-tools-2026-09-15`, `defer_loading` |
| D02-V18 | Prompting best practices | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Anthropic | anthropic-docs | 2026-09-24 | primary | 3–5 few-shot examples and the diversity sentence; long-context ordering and "up to 30 percent"; adaptive-thinking-beats-extended-thinking claim; manual CoT as the thinking-off fallback; prefill removal scope ("Earlier models continue to support prefills"); the thinking-latency counter-instruction verbatim; golden rule; motivation-over-prohibition with the TTS example; Opus 5 over-verification exception; **no "Anthropic recommends" anywhere on the page** |
| D02-V19 | What's new in Claude Opus 5.5 | https://platform.claude.com/docs/en/models/opus-5-5/whats-new-opus-5-5 | Anthropic | anthropic-docs | 2026-09-24 | primary | The four breaking changes; thinking-disabled and forced-tool-use 400s with exact error strings and the `count_tokens` note; "The first three also apply on Claude Fable 5.1"; thinking-block model binding and unbilled drops; prefix-check enforcement and the 2026-08-31 cutoff; default effort `medium`; 512-token cache minimum; $4/$20 with $5/$8/$0.20 (0.05x) and batch $2/$10; progress text moving into thinking blocks; refusal handling |
| D02-V20 | Migrating to Claude Opus 5.5 | https://platform.claude.com/docs/en/models/opus-5-5/migration-guide | Anthropic | anthropic-docs | 2026-09-24 | primary | "What every request to Claude Opus 5.5 must satisfy" (thinking, effort, tool choice, sampling, prefill, computer use, no context beta header); the "Claude Opus 4.7 and later models" sampling scope and the SDK `TypeError` note; prefill scope "Claude Opus 4.6 and later Opus models"; **"Claude Sonnet 5, like Claude Opus 5: … Accepts forced tool choice"** and accepts `disabled` at any effort level; Sonnet 5 lacks mid-conversation system messages; 512 vs 1,024 cache minimum |
| D02-V21 | Migrating to Claude Sonnet 5 | https://platform.claude.com/docs/en/models/sonnet-5/migration-guide | Anthropic | anthropic-docs | 2026-09-24 | primary | Sampling parameters → 400; prefill → 400 from Sonnet 4.6 on; `budget_tokens` → 400; `disabled` accepted; `thinking.display` default change; ~30% tokenizer and re-count checklist; **Haiku 4.5 accepts prefill and `temperature`/`top_p` one at a time**; Haiku 4.5 has no effort parameter; cyber-safeguard refusals as HTTP 200 |
| D02-V22 | What's new in Claude Fable 5.1 | https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 | Anthropic | anthropic-docs | 2026-09-24 | primary | Fable 5.1 / Mythos 5.1 rejections: forced tool use (with the reason), `enabled`/`disabled`, prefill, non-default sampling; 512-token minimum; 1M at standard pricing across the whole window; default effort `high`; per-message effort and turn-scoped system messages; the editing-earlier-turns invalidation rules and the safe list; pricing table and the 0.025x read; fallback targets and fallback credit; **Covered Models / 30-day retention / not ZDR-eligible**; **the stale "start with Claude Opus 5" sentence** |
| D02-V23 | Manage tool context | https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context | Anthropic | anthropic-docs | 2026-09-24 | primary | The four levers and what each reduces; "past roughly 20 tools" as the only threshold (**no token breakeven**); the four-step adoption order; 25% cache-write markup framing; **absence of the 502-tool / $0.56-vs-$1.02 / 45% / 24% figures on this page** |
| D02-V24 | Mitigate jailbreaks and prompt injections | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks | Anthropic | anthropic-docs | 2026-09-24 | primary | Direct vs indirect injection threat models; "Put untrusted content only in tool results" and the trained-skepticism sentence; state-the-source guidance; system-prompt policy example; JSON-encoding rationale; "Don't put your own instructions in tool results"; least-privilege bullet; Haiku 4.5 screening of input and of tool output with structured outputs; red-teaming |
| D02-V25 | Strict tool use | https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use | Anthropic | anthropic-docs | 2026-09-24 | primary | What `strict: true` guarantees (grammar-constrained sampling on tool inputs); **no citations conflict and no programmatic-tool-calling conflict documented** |
| D02-V26 | Effective context engineering for AI agents | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Anthropic | anthropic-blog | 2026-09-24 | primary | Attention budget and n² pairwise relationships; "right altitude" definition; sub-agent summaries "often 1,000-2,000 tokens"; "overly aggressive compaction can result in the loss of subtle but critical context"; curated canonical examples over a laundry list of edge cases |
| D02-V27 | Claude Certified Architect – Professional Exam Guide v1.0 | (local: `claude-arch-professional-guide.md`) | Anthropic | exam-guide | 2026-09-24 | primary | Domain 2 objectives verbatim; 13% weight; Sample 2 stem, options and rationale; criterion-referenced scoring and the 720 cut score |
| D02-V28 | VERIFIED-FACTS.md | (local: `prep-course-track-b/VERIFIED-FACTS.md`) | this project's orchestrator | other | 2026-09-24 | primary (derived) | Cross-check baseline for the lineup, cache-read economics, effort model and ZDR interaction. **Amendment required:** its "Covered Models (Mythos-class)" framing is narrower than live docs, which put the whole Fable family under Covered Models and outside ZDR eligibility |

### Verdicts recorded, per AGENT-BRIEF §6

`CONFIRMED` 63 · `SCOPE-WRONG` 8 · `CONTRADICTED` 4 · `NOT-FOUND` 5 · not verified this pass 1. Every
verdict is itemized in `## Volatile-facts verification table` with its source ID.
