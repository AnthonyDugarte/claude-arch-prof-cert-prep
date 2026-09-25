# Research dossier — Domain 2: Claude Models, Prompting & Context Engineering (13%)

Researcher pass. All verification performed 2026-09-24 in-session via the bundled `claude-api` skill
(Anthropic, v2.1.273) plus WebFetch against `platform.claude.com/docs` and `anthropic.com/engineering`.
Source IDs resolve in `02-models-prompting-context-sources.md`.

**Note on the canonical docs host.** The task brief and AGENT-BRIEF §0 say `docs.claude.com`. The live
canonical documentation host is **`platform.claude.com/docs/en/...`**; `docs.claude.com` URLs and the
older `about-claude/models/overview` path either redirect or 404. All doc citations in this dossier use
the live host. This is a correction to AGENT-BRIEF §0, not a contradiction of it.

---

## 0. BLOCKER-level contradiction with AGENT-BRIEF §0 — the lineup has moved

AGENT-BRIEF §0 states: *"Current Claude model lineup as of today: Claude 5 family (Opus 5, Sonnet 5,
Fable 5.1) and Haiku 4.5."*

Live primary docs on 2026-09-24 say otherwise [D02-S09, D02-S25]:

- The current comparison table lists **Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5, Claude Haiku 4.5**.
- **Claude Opus 5 is listed under "Legacy models (still available)"**, together with Fable 5, Opus 4.8/4.7/4.6/4.5, Sonnet 4.6/4.5.
- `choosing-a-model` now says *"Most workloads start with Claude Opus 5.5"* and *"If you're unsure which model to use, start with Claude Opus 5.5"* [D02-S09, D02-S12].
- The bundled `claude-api` skill's own model table is stamped **cached 2026-06-24** and predates Opus 5.5; its default-model instruction (`claude-opus-5`) is a code-generation default, not a statement about the current lineup [D02-S02].

**Consequence for the course:** any Domain 2 chapter that presents Opus 5 as the current flagship is
already stale. The draft names Opus 5.5 as today's default recommendation and Fable 5.1 as the
capability ceiling, and treats Opus 5 as legacy-but-served. The consolidation session must re-verify
this before publication — the lineup moved inside a three-month window, which is itself the chapter's
most important lesson.

---

## 1. Volatile facts table (re-check every one of these before publication)

| Fact | Value | Source | Verified |
|---|---|---|---|
| Current recommended default model | Claude Opus 5.5, `claude-opus-5-5` | D02-S09, D02-S12 | 2026-09-24 |
| Highest-capability widely released model | Claude Fable 5.1, `claude-fable-5-1` | D02-S09, D02-S12 | 2026-09-24 |
| Balanced tier | Claude Sonnet 5, `claude-sonnet-5` | D02-S09 | 2026-09-24 |
| Fastest / cheapest tier | Claude Haiku 4.5, alias `claude-haiku-4-5`, pinned `claude-haiku-4-5-20251001` | D02-S09 | 2026-09-24 |
| Opus 5.5 price | $4 / MTok input, $20 / MTok output | D02-S10, D02-S25 | 2026-09-24 |
| Opus 5.5 cache writes / reads | $5 (5m), $8 (1h), $0.20 read (0.05x input) | D02-S10, D02-S25 | 2026-09-24 |
| Fable 5.1 price | $10 in / $50 out; $12.50 (5m), $20 (1h), $0.25 read (0.025x) | D02-S10 | 2026-09-24 |
| Sonnet 5 price | $2 in / $10 out; $2.50 (5m), $4 (1h), $0.20 read (0.1x). The $2/$10 "introductory" rate is now the standard price; the scheduled rise to $3/$15 will not occur | D02-S10 | 2026-09-24 |
| Haiku 4.5 price | $1 in / $5 out; $1.25 (5m), $2 (1h), $0.10 read | D02-S10 | 2026-09-24 |
| Opus 5 (legacy) price | $5 in / $25 out; $0.50 read | D02-S10 | 2026-09-24 |
| Context window | 1M tokens on Fable 5.1 / Mythos 5.1 / Fable 5 / Mythos 5 / Opus 5.5 / Opus 5 / 4.8 / 4.7 / 4.6 / Sonnet 5 / Sonnet 4.6; **200K on Haiku 4.5** and on Sonnet 4.5 | D02-S09, D02-S11 | 2026-09-24 |
| 1M context gating | **Default, no beta header**, and billed at **standard pricing** — a 900K-token request is billed at the same per-token rate as a 9K one | D02-S11, D02-S10 | 2026-09-24 |
| Max output (synchronous) | 128K on the 1M-context models; 64K on Haiku 4.5. Batch API supports up to 300K output on Opus 5.5/5/Sonnet 5/Opus 4.8/4.7/4.6/Sonnet 4.6 with beta `output-300k-2026-03-24` | D02-S09 | 2026-09-24 |
| Default `effort` | `medium` on Opus 5.5; `high` on every other model that supports effort; **not supported on Haiku 4.5** | D02-S14, D02-S09 | 2026-09-24 |
| Effort levels | `low`, `medium`, `high`, `xhigh`, `max`. `xhigh` is not on every model that has `max` (e.g. Opus 4.6 has `max`, not `xhigh`) | D02-S14 | 2026-09-24 |
| Effort parameter location | `output_config.effort` — nested, not top-level. GA, no beta header | D02-S14 | 2026-09-24 |
| Thinking on Opus 5.5 / Fable 5.1 | Always on. `thinking:{"type":"disabled"}` and `{"type":"enabled",budget_tokens:N}` both return **400** | D02-S25, D02-S14 | 2026-09-24 |
| Thinking on Sonnet 5 | Adaptive, on by default when `thinking` omitted; `disabled` accepted; `budget_tokens` → 400 | D02-S26 | 2026-09-24 |
| Thinking on Haiku 4.5 | Manual extended thinking only (`{"type":"enabled",budget_tokens:N}`), **off by default**; rejects `adaptive` | D02-S26, D02-S02 | 2026-09-24 |
| `thinking.display` default | `omitted` on Fable/Mythos 5.x, Opus 5.5/5/4.8/4.7, Sonnet 5 (was `summarized` on Opus 4.6 / Sonnet 4.6). Display does not change billing — thinking is billed either way | D02-S26, D02-S02 | 2026-09-24 |
| Sampling parameters | `temperature`, `top_p`, `top_k` at **non-default values return 400** on Sonnet 5 and the current frontier models. `temperature`/`top_p` still work on Haiku 4.5, one at a time | D02-S26 | 2026-09-24 |
| Assistant prefill | **400** on Claude 4.6 and later (so on every current model). Migrate to structured outputs or system-prompt instructions | D02-S16, D02-S26 | 2026-09-24 |
| Forced tool use | `tool_choice` `{"type":"any"}` / `{"type":"tool"}` returns **400** on Opus 5.5 and Fable 5.1 (also on `count_tokens` and Batches). `auto` and `none` still work | D02-S25 | 2026-09-24 |
| Cache breakpoints | Max **4** `cache_control` breakpoints per request; the top-level automatic breakpoint consumes one slot | D02-S13, D02-S03 | 2026-09-24 |
| Cache TTLs and multipliers | 5-minute write = **1.25x** base input; 1-hour write = **2x**; read = **0.1x** base (0.025x Fable 5.1 / Mythos 5.1; 0.05x Opus 5.5) | D02-S10, D02-S13 | 2026-09-24 |
| Cacheable-prefix minimum | 512 tokens (Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5); 1,024 (Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5, Opus 4.1, Opus 4); 2,048 (Opus 4.7, Mythos Preview); **4,096 (Opus 4.6, Opus 4.5, Haiku 4.5)**. Not monotonic across generations; below the minimum, caching is skipped silently with no error | D02-S13, D02-S03 | 2026-09-24 |
| Cache render order | `tools` → `system` → `messages`. A breakpoint on the last system block caches tools + system together | D02-S03, D02-S13 | 2026-09-24 |
| Cache lookback | A breakpoint walks back at most **20 positions** to find a prior entry; consecutive `tool_use` runs and consecutive `tool_result` runs each collapse to one position | D02-S03 | 2026-09-24 |
| Cache isolation | Per **workspace** on Claude API / Claude Platform on AWS / Microsoft Foundry; per **organization** on Bedrock and Google Cloud; never across organizations | D02-S13, D02-S03 | 2026-09-24 |
| Batch discount | **50% off input and output**, stacking with prompt-cache multipliers; results within 24 h (an expiry, not an SLA) | D02-S10, D02-S04 | 2026-09-24 |
| Tokenizer change | Claude 4.7 and later (and Fable/Mythos 5.x, Sonnet 5) use a newer tokenizer producing **≈30% more tokens for the same text**. Re-count against the target model; do not reuse older counts for cost or context-fit estimates | D02-S10, D02-S22, D02-S26 | 2026-09-24 |
| Token counting endpoint | `POST /v1/messages/count_tokens`. Free; separate rate limits (5,000 / 10,000 / 20,000 RPM at Start / Build / Scale). Returns an **estimate**. Rejects server tools, MCP connector, and `url`/`file` image/document sources | D02-S22 | 2026-09-24 |
| Context editing | Beta `context-management-2025-06-27`; strategies `clear_tool_uses_20250919` (defaults: trigger 100,000 input tokens, keep 3 tool uses) and `clear_thinking_20251015`. When combined, `clear_thinking_20251015` must be listed first | D02-S18 | 2026-09-24 |
| Compaction | Two beta forms: **on demand** (beta `compact-2026-09-04`, top-level `compaction` parameter, you choose when, can run in the background, can keep recent turns verbatim) and **at a token threshold** (the API compacts inside the request that crosses the trigger). The skill's `compact-2026-01-12` header is superseded | D02-S19, D02-S25, D02-S02 | 2026-09-24 |
| Mid-conversation system messages | `{"role":"system"}` inside `messages[]`. Available on Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Opus 4.8, Fable 5, Mythos 5. **Not on Sonnet 5.** No beta header for the basic form; `clear_at:"next_user_message"` needs beta `mid-conversation-system-clear-at-2026-08-21` | D02-S24, D02-S03 | 2026-09-24 |
| Per-message effort | Beta `mid-conversation-output-config-2026-07-01`; Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5. Preserves the prompt cache where a top-level effort change would not | D02-S14 | 2026-09-24 |
| Skills | `SKILL.md` with YAML frontmatter `name` (≤64 chars, lowercase/digits/hyphens, no "anthropic"/"claude") and `description` (≤1024 chars); optional `display_name` (≤255). Bundle ≤30 MB uncompressed. Passed via `container.skills`, **max 20 per request**, requires the code execution tool. **Workspace is the isolation boundary** | D02-S20 | 2026-09-24 |
| Structured outputs | `output_config.format` with `{"type":"json_schema","schema":{...}}`; `additionalProperties:false` required. `strict:true` on a tool guarantees valid tool input. **Incompatible with citations** (400). Changing `output_config.format` invalidates the prompt cache. Grammar is cached 24 h from last use | D02-S21 | 2026-09-24 |
| Citations | `citations:{"enabled":true}` per `document` block, **all documents or none** in a request. Locations: `char_location` (text), `page_location` (PDF, 1-indexed), `content_block_location` (custom content). Document indices are 0-indexed. Citation blocks cannot be cached; cache the source document blocks instead | D02-S23 | 2026-09-24 |
| Tool-use system-prompt overhead | Adding any tool injects a tool-use system prompt: 286 tokens on Opus 5.5, 354 on Sonnet 5, 496 on Haiku 4.5 (auto/none) | D02-S10 | 2026-09-24 |
| Context-window overflow | Input alone over the window → 400 `invalid_request_error` ("prompt is too long"). On Claude 4.5+ models, input + `max_tokens` over the window is **accepted**, and generation stops with `stop_reason:"model_context_window_exceeded"` | D02-S11 | 2026-09-24 |
| Context awareness (injected token budget) | Sonnet 5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5 receive `<budget:token_budget>` and post-tool `<system_warning>` tags automatically. Opus 4.7+ and Fable/Mythos models do **not** — use task budgets there | D02-S11 | 2026-09-24 |
| Measured caching impact | Cut agent-loop cost by a factor of **2.7 to 5.3** on Anthropic's benchmarks; cut a small triage agent's bill **83%** (88% with input trimming). Real traffic reads a **median 84%** of input from cache; top-decile harnesses 94%+ | D02-S17 | 2026-09-24 |
| Measured effort curves | Research benchmarks: `low` loses 1–3 points for 33–50% cost cut; `medium` matches default accuracy at 70–87% of cost; default buys nothing measurable over `medium`. SWE-bench Pro (coding) on Opus 5.5: `medium` −2.5 points at ~70% cost; `low` −8 points at ~33%; `xhigh` +1.4 points at 2.5x the cost of `high` | D02-S17 | 2026-09-24 |
| Measured cost-per-solved-task inversions | Fable 5.1 at `low`: 88.6% solved at $0.54/solved vs Sonnet 5 default 77.4% at $0.84/solved — **11 points more accurate for 35% less per solved task despite 5x the per-token price**. Opus 5.5 at `medium`: 92.8% at $0.22/solved vs Fable 5.1 default 92.3% at $1.19/solved | D02-S17 | 2026-09-24 |
| Failure re-run economics | Opus 5.5 on SWE-bench Pro: all at `low` (13% fail) then re-run failures at `high` → 97% pass at $0.17/task, vs 95.3% at $0.29/task running everything at `high` | D02-S17 | 2026-09-24 |
| `max_tokens` economics | A 16K cap ended 1 in 14,000 turns; only 1 of 66 capped attempts passed, so cost per **solved** task was unchanged. Recommended 64,000 for agentic work; 128,000 costs nothing extra per solved task | D02-S17, D02-S04 | 2026-09-24 |
| Orchestrator measured | 21.6M-token corpus, Fable 5.1 + 25 Sonnet 5 workers: **47–55% cheaper** than Fable 5.1 solo, 10–12 points less accurate, 2.3 h vs 15–20 h. On work that fits one context, the coordinator's model alone at lower effort won every time | D02-S17, D02-S04 | 2026-09-24 |
| Advisor measured | Opus 5.5 executor + Fable 5.1 advisor: 90.1% at $2.92/attempt vs Opus 5.5 alone at `high` 88.4% at ~$1.40 and at `xhigh` 91.1% at $4.11 — the advisor buys roughly what more effort buys, at ~2x cost | D02-S17 | 2026-09-24 |
| Tool search breakeven | Pays once tool schemas run past roughly **10K tokens** / ~20 tools; below that the extra lookup turn is overhead. At 502 tools, cost stayed flat ($0.56) vs $1.02 with all tools loaded — 45% less at no accuracy loss | D02-S28, D02-S04, D02-S17 | 2026-09-24 |
| Files API + code execution vs inlining | CSV pasted into the prompt: 6/25 questions correct at $5.01. Same data uploaded and computed in the sandbox: 25/25 at $0.40 — ~12x cheaper and more accurate | D02-S17 | 2026-09-24 |
| Long-context prompt ordering | Put longform documents near the top, above the query, instructions, and examples. Queries at the end improved response quality **by up to 30%** in Anthropic's tests, especially on complex multidocument inputs | D02-S16 | 2026-09-24 |
| Few-shot count | **3–5 examples** for best results; wrap in `<example>` / `<examples>` tags; make them relevant, diverse, and structured | D02-S16 | 2026-09-24 |
| Sub-agent summary size | Anthropic's guidance: each sub-agent returns a condensed summary, "often 1,000–2,000 tokens" | D02-S29 | 2026-09-24 |
| Fast mode | Research preview, Claude API only (not Bedrock/Google Cloud/Foundry/Claude Platform on AWS). Opus 5.5 at $8/$40; Opus 5 and Opus 4.8 at $10/$50. Up to ~2.5x output speed. Not available with Batch API. Not on Opus 4.7 (error) | D02-S10, D02-S12, D02-S02 | 2026-09-24 |
| `inference_geo` | `"us"` applies a **1.1x** multiplier to every token category, including cache writes and reads. Claude 4.6+ only | D02-S10 | 2026-09-24 |

---

## 2. Findings by objective

### Objective 1 — Select appropriate Claude models based on trade-offs

**Two sanctioned starting methods, not one** [D02-S12]:

| Method | Procedure | Best for |
|---|---|---|
| Efficiency-first | Start Haiku 4.5 → test thoroughly → evaluate against requirements → upgrade only for a specific capability gap | Prototyping, tight latency budgets, cost-sensitive high-volume straightforward tasks |
| Capability-first | Start Opus 5.5 → optimize prompts *for that model* → evaluate → increase efficiency by lowering effort or downgrading over time → if evals at `xhigh`/`max` still fall short, move to Fable 5.1 | Complex reasoning, scientific/mathematical work, nuanced understanding, advanced coding, high-autonomy agentic work, accuracy-over-cost |

Two rules make this an engineering decision rather than a preference:

1. **Effort before model.** "Tuning effort is often a better lever than switching models" [D02-S12]. Cost-optimization order puts model selection *last*, after every lever that does not constrain the intelligence ceiling [D02-S04, D02-S17]. One exception: with a real eval in a hillclimb loop, sweep model × effort early, because only an eval can find the cell where a stronger model at lower effort is the cheaper choice [D02-S04].
2. **Price cost per completed task, not per token.** Per-token price lists do not predict the ranking; a 5x-per-token model can be 35% cheaper per solved task [D02-S17]. And **price the tail, not the median** — on one 20-problem research run, two problems carried 43% of the spend [D02-S04, D02-S17].

**The stepping-down method** [D02-S04]: sweep effort on the current model; if `low` passes the eval, drop one tier; confirm which parameters and effort levels the target tier accepts; **reset effort to the target tier's own default** rather than carrying a level across; re-sweep from there; one notch at a time. Haiku 4.5 has no effort parameter, so there it is a single-configuration evaluation.

**What makes a task frontier-only** (synthesis from D02-S12, D02-S17): (a) evals at `xhigh`/`max` on the default-tier model still fall short; (b) long-horizon agentic sessions measured in hours; (c) multistep deep research carried through to a finished artifact; (d) a reasoning ceiling where every effort step still buys score (on DeepResearch-style work effort was flat, so that is *not* a frontier-only signal — flatness means the cheaper setting already does the work).

**Hidden costs of cascades and routing** [D02-S03, D02-S04, D02-S17]:
- Caches are **model-scoped**, so a cascade forfeits cache reuse across its models; a mid-session model switch is a full cache rebuild with no escape hatch.
- Advisor consult rate is the fragile variable: lowering effort can drop a pairing from consulting on most tasks to almost none, after which it scores *below* the executor alone. Gating the consult requires a cheap external signal — asking the executor to recognize hard cases demands the judgment it lacks. "The advisor can only hand over capability the executor lacks."
- Orchestrators pay for a plan, a handoff, and a merge. They win only when there is genuine bulk to partition, ideally more than fits one context window.
- Thinking blocks are bound to the producing model. Opus 5.5 reads Opus 5 and earlier Opus/Sonnet/Haiku blocks but not Fable/Mythos blocks; only Fable 5.1 / Mythos 5.1 read Opus 5.5 blocks. A router that moves a live conversation between tiers silently drops reasoning (unbilled) [D02-S25].

### Objective 2 — Design system prompts, templates, and guardrails

**Precise concept — "the right altitude"** [D02-S29]: an effective system prompt avoids both failure modes — hardcoded brittle logic that tries to elicit exact behavior (fragile, high maintenance), and vague high-level guidance that gives no concrete signal. Target: "specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics."

Verified prompt-construction rules [D02-S16]:
- Golden rule: if a colleague with minimal context would be confused by the prompt, so will Claude.
- Give the *motivation*, not just the prohibition: "Your response will be read aloud by a text-to-speech engine, so never use ellipses" outperforms "NEVER use ellipses." Claude generalizes from the explanation.
- Say what to do, not what not to do ("Your response should be composed of smoothly flowing prose paragraphs" over "Do not use markdown").
- Match prompt style to desired output style; removing markdown from the prompt reduces markdown in the output.
- Set the role in the system prompt; even one sentence changes behavior.
- Structure with XML tags (`<instructions>`, `<context>`, `<input>`), consistent names, nested where there is a hierarchy.

**Three distinct guardrail layers, with different enforcement guarantees:**

| Layer | Mechanism | What it can enforce | What it cannot |
|---|---|---|---|
| System-prompt guardrail | Values block, explicit refusal string, untrusted-content policy [D02-S31] | Tone, refusal wording, default posture, how to treat tool content | Nothing with a hard guarantee — it is a behavioral prior; the model can be talked around it and a compromised tool result can try |
| Programmatic guardrail | Structured outputs / `strict: true` tools (constrained decoding), removing the tool from the config, least-privilege scoping, sandboxing, post-hoc validation [D02-S21, D02-S31] | Schema validity absolutely; capability absence absolutely | Semantic correctness; whether the *content* inside a valid schema is appropriate |
| Classifier guardrail | A separate cheap-model call (Haiku 4.5) screening input, or screening tool output before it becomes a `tool_result`, with structured outputs constraining the verdict to a parseable boolean [D02-S31] | Probabilistic detection of harmful input or injection attempts, on a branchable signal | Determinism; it is itself a model call with its own false-positive/negative rate and latency |

**Indirect prompt injection is a message-shape problem, not a wording problem** [D02-S31]:
- Put third-party content **only in `tool_result` blocks** — never in `system` or in plain user `text`. Claude is trained to treat instructions inside tool results with skepticism.
- State the nature and source of the content in the tool `description` or the result structure.
- JSON-encode untrusted strings so an attacker cannot close a quote or tag and break out into instruction context.
- **Do not put your own instructions in tool results** — they may be ignored or flagged as injection. Send them in the following `user` turn, or as a mid-conversation system message.
- `{"role":"system"}` inside `messages[]` is the non-spoofable operator channel with operator-over-user priority; text inside a user turn can be forged by anything that writes user-visible input [D02-S24, D02-S03].

### Objective 3 — Prompt engineering techniques (zero-shot, few-shot, chain-of-thought)

- **Zero-shot** works where the instruction is unambiguous and the output shape is simple. Prompt engineering presupposes success criteria and a way to test against them — without those, do that first [D02-S15].
- **Few-shot / multishot**: "one of the most reliable ways to steer Claude's output format, tone, and structure." 3–5 examples; relevant, diverse, structured in `<example>` tags. Diversity matters specifically so Claude does not pick up unintended patterns — that is the anchoring failure mode named in primary docs [D02-S16]. Do not stuff a laundry list of edge cases; curate diverse canonical examples [D02-S29].
- **Chain-of-thought is now mostly a model feature, not a prompt pattern.** Adaptive thinking is the mechanism: Claude calibrates thinking from `effort` plus query complexity, and on easy queries responds directly. "In internal evaluations, adaptive thinking reliably drives better performance than extended thinking" [D02-S16]. Manual `<thinking>`/`<answer>` CoT is explicitly the **fallback for when thinking is off**, and on Opus 5 running with thinking disabled can leak internal XML tags into visible output [D02-S16]. Prefer general instructions ("think thoroughly") over hand-written step plans: "Claude's reasoning frequently exceeds what a human would prescribe."
- **Multishot composes with thinking**: `<thinking>` tags inside few-shot examples show the reasoning pattern and Claude generalizes that style into its own thinking blocks [D02-S16].
- **Self-check is model-dependent.** "Before you finish, verify your answer against [criteria]" catches errors reliably — except on Opus 5, which verifies well unprompted, where carried-over verification instructions cause over-verification and waste tokens and latency [D02-S16].
- **Thinking can be over-triggered by prompting.** Large or complex system prompts make the model think more often than wanted; there is a sanctioned counter-instruction ("Thinking adds latency and should only be used when it will meaningfully improve answer quality… When in doubt, respond directly") [D02-S16].
- **When thinking tokens are wasted:** when the effort curve is flat on the workload (research/knowledge work — default bought nothing measurable over `medium`), on structured-output or classification tasks where `max` can cause overthinking, and on follow-up requests that only process tool results [D02-S17, D02-S14].

### Objective 4 — Optimize context windows and manage token usage

**Precise definition of the core constraint** [D02-S11, D02-S29]: "more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as *context rot*. This makes curating what's in context just as important as how much space is available." The mechanism is an **attention budget**: transformer attention is n² in pairwise relationships, and models have less training experience and fewer specialized parameters for context-wide dependencies.

Everything counts toward the window: system prompt, every message including tool results / images / documents, tool definitions, and the model's own output including thinking. Cached prefixes still occupy the window — caching changes what you pay for those tokens, not whether they count [D02-S11].

**Four strategies, mapped to the pressure each relieves:**

| Strategy | Relieves | Mechanism | Cost |
|---|---|---|---|
| Stuff the context | nothing | Everything inline | Context rot; full re-billing each turn unless cached; hits the 1M ceiling |
| Retrieve / progressive disclosure | Reference material and tool schemas | Document behind a tool or Skill; tool search with `defer_loading` | Discovery turns; skip when most calls need most of the document, or when evals miss on rules the model must now go find [D02-S04] |
| Summarize / compact | Accumulated history | Server-side compaction (on demand or at a threshold) | Lossy — "overly aggressive compaction can result in the loss of subtle but critical context" [D02-S29]; each compaction rewrites the cached prefix |
| Externalize to files / memory | Cross-session and cross-window state | Memory tool, Files API + code execution, progress files, structured feature lists, git history | Harness complexity; "compaction isn't sufficient" for multi-window coherence [D02-S30] |

**Context editing is not a savings lever** [D02-S04]: every clearing pass rewrites the cached conversation and works against prompt caching. In the run measured for the platform docs it *cost more than it saved*. Use it to make room in the window; set the trigger high enough that clears stay infrequent; clear in a few large batches; `clear_at_least` exists to make each clear large enough to justify the cache invalidation it causes [D02-S18].

**Token-usage levers verified** [D02-S04, D02-S17, D02-S28]: caching first; delete tool recaps from the system prompt (schemas already render); tool search past ~10K schema tokens; pre-downscale images (vision is tokenized by pixel area, roughly one token per 28×28 patch; 1280×720 caps an image near 1,200 tokens); Files API + code execution instead of inlining tables; `count_tokens` as an ingestion gate on unbounded user input; programmatic tool calling to keep intermediates out of context (documented at 24% fewer input tokens with a higher score); narrow accessors over data-dump tools; batch anything nobody is waiting on.

**Prompt cruft is a real cost.** Prompts written for an older model make the current one over-work: a support-desk evaluation ran 36% more expensive per ticket on Opus 5 with prompts written for Opus 4.8, at no accuracy gain; audited, the same prompts were 14% cheaper *and* more accurate (97% vs 92% of tickets) [D02-S04].

### Objective 5 — Prompt reuse strategies (caching, modular prompts, Skills)

**The one invariant:** prompt caching is a **prefix match**. Any byte change anywhere in the prefix invalidates everything after it. Render order is `tools` → `system` → `messages` [D02-S03, D02-S13]. This makes the ordering decision — stable content physically before volatile content — more important than marker placement, and it is exactly what the exam guide's own Sample 2 tests [D02-S01].

**Placement patterns** [D02-S03]:
- Large shared system prompt → breakpoint on the **last system text block** (catches tools + system).
- Multi-turn conversation → breakpoint on the last content block of the most recently appended turn; earlier breakpoints stay valid read points, so hits accrue as the conversation grows.
- Shared prefix + varying suffix → breakpoint at the **end of the shared portion**, not the end of the prompt. Otherwise every request writes a distinct entry and nothing is ever read.
- Prompts that differ from the first 1K tokens → **do not cache**; markers only buy the write premium.
- Robust agent-loop shape: one **explicit** breakpoint on the static system prefix (guaranteed read point that survives whatever happens later in `messages`) **plus** top-level automatic caching for the growing tail.

**Automatic caching is a surcharge in one specific case** [D02-S03]: when the prompt ends in unique per-request content, the automatic breakpoint lands after the unique tail, so every request pays a write premium on bytes never read back. Signature: `cache_creation_input_tokens` on every request while `cache_read_input_tokens` never covers the full shared prefix.

**TTL decision from the start-to-start gap** (generation time counts against the TTL; a read refreshes the timer free) [D02-S03, D02-S17]:

| Gap between requests sharing the prefix | Choose | Why |
|---|---|---|
| Under 5 min | 5-minute | Every request refreshes it; strictly cheaper than paying 2x writes |
| 5–60 min | 1-hour | The only window where the 2x write pays off; Anthropic's rule of thumb is about 1 turn in 20 pausing 5 min–1 h |
| Over 1 h | Neither directly | Scheduled re-warm (`max_tokens: 0`) or accept the cold miss |

Breakeven: 5-minute TTL breaks even on the second request (1.25x + 0.1x = 1.35x vs 2x uncached); 1-hour needs three (2x + 0.2x = 2.2x vs 3x) [D02-S03]. On Fable 5.1, where reads are 0.025x, a `max_tokens: 0` keep-alive on the 5-minute TTL usually beats buying the 1-hour TTL unless pauses approach an hour.

**Caching is not a substitute for context reduction.** It reprices the resend at 0.1x; it does not stop the resending, and cached tokens still occupy the window and still contribute to context rot [D02-S04, D02-S11]. An agentic task resends its whole growing history every turn, so task cost grows roughly with the square of turn count; caching flattens the price, not the growth.

**Verification is the only ground truth, and the failure is silent** [D02-S03]: `cache_read_input_tokens` should dominate `input_tokens` in a warmed loop, and `cache_creation_input_tokens` should be about one turn's worth. `input_tokens` is the uncached remainder only; total prompt size is the sum of all three. The typical production failure is a *regression* — caching worked when written, then a later prompt-assembly change (a new dynamic field, a history-rewriting feature, a non-deterministic tool list) misses on every request and nobody notices for months. Standing assertion in CI beats a one-time look.

**Three reuse shapes, with governance properties:**

| Shape | Versioning | Testability | Blast radius of a change | Who owns edits |
|---|---|---|---|---|
| Inline monolithic prompt | Whatever the app repo does | Only via the app | Every request on that code path, at deploy | Whoever owns the service |
| Templated / modular prompt (fixed template + `{{VARIABLE}}` slots) | App repo, reviewable diff | Template can be unit-tested and eval'd per module | Scoped to the module, but a change above a cache breakpoint invalidates everything after it | Service owner, with prompt review |
| Agent Skill | First-class: date-based versions for Anthropic skills, `skver_...` IDs for custom, or `"latest"` [D02-S20] | Versioned bundle can be pinned in an eval | Pinning a version bounds it; `"latest"` means any re-upload changes production behavior immediately | Skill author, separate from the calling service — which is the point and the risk |

Skills add a **workspace-scoped isolation boundary**: custom Skills are visible to the whole workspace, not per user or per session, so multi-tenant platforms need a workspace per tenant [D02-S20]. Skills also require the code execution tool and a compatible model, so they are not a drop-in replacement for a system prompt in a plain text workload.

**Skill vs system prompt vs tool** [D02-S20]: Skill for complex multi-file operations needing code execution and structured resources; system prompt for static instructions, role, behavioral guidelines applying to all conversations; tool for a specific function or API call. Progressive disclosure: the `SKILL.md` description sits in context, the supporting files load during execution when needed.

**Cache-preserving escape hatches** (each availability-gated separately) [D02-S03, D02-S24, D02-S14]:

| Top-level change that invalidates | Cache-preserving form |
|---|---|
| System prompt content | `{"role":"system"}` message in `messages[]` — available today, no beta header, on the supporting models |
| Per-turn reminder (inject then delete) | `clear_at:"next_user_message"` system message, left in the transcript, never deleted |
| Tool definitions (add/remove) | `tool_addition` / `tool_removal` blocks (beta); `inline-tools-2026-09-15` carries full definitions |
| `effort` change | `{"role":"system","content":[],"output_config":{"effort":...}}` (beta) |
| Model switch | **None.** Caches are model-scoped |

---

## 3. Raw comparison matrices

### 3.1 Current lineup (verbatim from D02-S09, D02-S10)

| | Fable 5.1 | Opus 5.5 | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|---|
| Purpose | Demanding reasoning, long-horizon agentic | Long-running agentic coding and knowledge work | Best speed/intelligence combination | Fastest, near-frontier |
| Claude API ID | `claude-fable-5-1` | `claude-opus-5-5` | `claude-sonnet-5` | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) |
| Comparative latency | Slower | Moderate | Fast | Fastest |
| Input / output $ per MTok | 10 / 50 | 4 / 20 | 2 / 10 | 1 / 5 |
| Cache read $ per MTok (multiplier) | 0.25 (0.025x) | 0.20 (0.05x) | 0.20 (0.1x) | 0.10 (0.1x) |
| Batch input / output | 5 / 25 | 2 / 10 | 1 / 5 | 0.50 / 2.50 |
| Thinking | Adaptive, always on | Adaptive, always on | Adaptive | Extended (`budget_tokens`) |
| Default effort | `high` | `medium` | `high` | not supported |
| Context window | 1M | 1M | 1M | 200K |
| Max output (sync) | 128K | 128K | 128K | 64K |
| Reliable knowledge cutoff | Jun 2026 | Jun 2026 | Jan 2026 | Feb 2025 |
| Retirement no sooner than | 2027-09-01 | 2027-09-22 | 2027-06-30 | 2026-10-15 |
| Cacheable-prefix minimum | 512 | 512 | 1,024 | 4,096 |

### 3.2 Determinism levers and their limits

| Lever | Status on current models | Guarantee | Limit |
|---|---|---|---|
| `temperature` / `top_p` / `top_k` | Non-default → **400** on Sonnet 5 and current frontier models; still usable on Haiku 4.5 (one of temperature/top_p) [D02-S26] | None | Gone as a design lever; docs say use prompting instead |
| Assistant prefill | **400** on Claude 4.6+ [D02-S16, D02-S26] | Was structural, not semantic | Removed; migrate to structured outputs or instructions |
| Structured outputs (`output_config.format`) | GA [D02-S21] | Constrained decoding: always valid JSON, schema-compliant, typed, no retries needed | Schema subset only (no recursion, no numeric/length constraints, no `additionalProperties:true`); incompatible with citations; invalidates prompt cache when changed |
| `strict: true` tool use | GA [D02-S21] | Tool `input` validates exactly | Not compatible with programmatic tool calling; says nothing about whether calling the tool was right |
| Forced `tool_choice` | `any`/`tool` → **400** on Opus 5.5 and Fable 5.1 [D02-S25] | — | Replace with `auto` + explicit prompt instruction, or `strict`/structured outputs |
| Enum in a tool schema | GA | Constrains classification labels; values are case-sensitive [D02-S21] | Only for the label set, not the reasoning |
| `max_tokens` | Always | Hard ceiling on total output including thinking | The model never sees it; hitting it truncates mid-thought with `stop_reason:"max_tokens"` and the attempt still bills [D02-S04, D02-S17] |
| Task budgets | Beta [D02-S02, D02-S04] | The model sees the countdown and paces itself | Advisory, not enforced; 20,000-token floor; very tight budgets can produce refusal-like behavior; a mid-task change invalidates the cache |

---

## 4. Contradictions and open questions

1. **AGENT-BRIEF §0 lineup vs live docs.** See §0. Opus 5.5 is current; Opus 5 is legacy. Live docs win. Flagged for consolidation.
2. **Canonical docs host.** Brief says `docs.claude.com`; live host is `platform.claude.com/docs/en/...`. Old `about-claude/models/overview` and `pricing.md` paths 404 or redirect.
3. **Bundled skill is stale relative to live docs** on three points: model table stamped 2026-06-24 (no Opus 5.5); compaction beta header given as `compact-2026-01-12` where live docs document `compact-2026-09-04` (on demand) plus a separate threshold form; Haiku 3.5 cacheable minimum listed as 2,048 in the skill and 2,048 on the docs page but the skill groups it with Opus 4.7 — cosmetic, both say 2,048. Where the skill and live docs disagree, **live docs win**.
4. **Caching impact figures differ between two Anthropic sources.** The skill's cost-optimization file says caching "cut agent-loop cost by a factor of 2.5 to 3.7, at 81% to 90% hit rates"; the live platform guide says "2.7 to 5.3" with a median 84% read rate [D02-S04 vs D02-S17]. Surfaced, not smoothed. The draft cites the live-docs range and describes both as order-of-magnitude directional.
5. **Mid-conversation system messages on Sonnet 5.** The skill notes that the model config marks it supported while every canonical docs page omits it, and advises treating it as unsupported and catching the 400 [D02-S03]. The live page states plainly "Not available: Claude Sonnet 5" [D02-S24]. Treat as unsupported.
6. **Context-editing model support.** The live page says "Available on: All supported Claude models" in one place and "Supported models: Claude Opus 5.5, Sonnet 4.6, Haiku 4.5, and newer" in another. Internally inconsistent; check per model before designing around it. `[UNVERIFIED]` for any specific older model.
7. **Effort on Opus 4.5.** Docs call Opus 4.5 "the only extended-thinking-only model that supports effort," where effort and `budget_tokens` work together [D02-S14]. Edge case; not load-bearing for the chapter.
8. **Open question — cache-read rate on Mythos 5.1.** The skill says whether Mythos 5.1 shares Fable 5.1's 0.025x rate "is open at launch"; the live pricing table lists $0.25/MTok for Mythos 5.1, which resolves it in favor of parity [D02-S10]. Mythos models are Project Glasswing invitation-only and out of scope for the chapter.
9. **Open question — whether the exam was authored against the Opus 5 / Sonnet 5 / Fable 5.1 lineup.** The guide is dated July 2026, before Opus 5.5. Exam items are written against objectives, not model IDs [D02-S01], and Domain 2's objectives name no model. The chapter therefore teaches the *method* and treats specific IDs as perishable — which is also the safest exam posture.
10. **Not verified: any claim about how CCAR-P items are worded or weighted beyond the published guide.** No live-item knowledge was sought or used.

---

## 5. Exam-relevance notes for the draft

The guide's own Domain 2 sample (Sample 2) is a caching-ordering item: 8,000 static tokens plus a short
varying user message, both latency and cost as constraints, correct answer "place the static system
prompt and policy before the dynamic content and enable prompt caching," with truncation, blind
downsizing, and few-shot relocation as distractors [D02-S01]. That fixes the expected cognitive level:
one scenario, four defensible-looking options, one that addresses both stated constraints without
discarding required context. The recurring distractor shapes visible in it — lose required information
to save tokens; change the model instead of the request shape; move content somewhere that does not
create a reusable prefix — are reproduced as archetypes in the draft.

---

## Prep-material landscape

A sweep on 2026-09-24 found a substantial commercial prep market for a credential effective July 2026:

| Source | Shape | Trust | Judgment |
|---|---|---|---|
| Udemy — at least four distinct CCAR-P listings, incl. "CCAR-P Exam Prep", "…Exam 2026", "…2026 Exams", "6 Practice Tests" [D02-S34] | Video course + practice tests | low | Multiple near-duplicate listings against a brand-new blueprint is the classic signature of blueprint-scraped, largely generated content. No named SME. Not used. |
| Tutorials Dojo — CCAR-P Study Guide [D02-S35] | Study guide + practice tests | low | The publisher has a real reputation in AWS certification, which raises the prior slightly. The page could not be fetched in full (content truncated), so nothing on it was verifiable. Not used. |
| CertSafari — 456 practice questions [D02-S36] | Question bank | low | An item count that large for a 63-item exam with no public item bank implies generation at volume. Not used. |
| Claude Certification Guide — 30 lessons, 250+ questions, free, no sign-up [D02-S37] | Free course + mock exams | low | Unattributed publisher; domain registered around the credential name. Not used. |
| Learning Tree — instructor-led prep, module-per-domain, mock exam [D02-S38] | Instructor-led | low | Established training vendor and the structure described matches the blueprint, but no verifiable SME authorship or accuracy claim. Not used. |
| Preporato — timed practice exams + flashcards [D02-S39] | Question bank | low | Not used. |

**Standing judgment.** None of this material was read for content and none of it informs a single claim
in the dossier or draft. The specific risk with third-party CCAR-P material in this domain is not
plagiarism but *staleness*: any question bank written before September 2026 that names a model, a price,
a context limit, or a parameter is likely wrong now (Opus 5.5 shipped; Sonnet 5's price schedule
changed; `temperature` now 400s; prefill now 400s; compaction's beta header changed). Candidates
should be told to treat third-party numbers as untrustworthy by default and verify against
`platform.claude.com/docs` and the Models API. That warning belongs in the chapter.
