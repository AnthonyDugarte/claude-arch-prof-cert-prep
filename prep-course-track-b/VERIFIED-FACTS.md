# VERIFIED FACTS — canonical ground truth for Track B

**All facts below were fetched from primary Anthropic documentation by the orchestrator on 2026-09-24.**
Every agent must treat this file as authoritative and must NOT contradict it from training memory. Where
this file and `AGENT-BRIEF.md` once disagreed, this file wins (the brief has been corrected).

> Why this file exists: the orchestrator's own environment context asserted that Claude Opus 5 was the
> latest model. That was stale. The Domain 1 researcher caught it against live docs and was right. Treat
> this as the standing lesson of the project: **verify the lineup, never recall it.**

## Current model lineup

Source: <https://platform.claude.com/docs/en/about-claude/models/overview> (fetched 2026-09-24).

| | Claude Fable 5.1 | Claude Opus 5.5 | Claude Sonnet 5 | Claude Haiku 4.5 |
|---|---|---|---|---|
| Positioning (docs wording) | "For demanding reasoning and long-horizon agentic work" | "For long-running agentic coding and knowledge work" | "The best combination of speed and intelligence" | "The fastest model with near-frontier intelligence" |
| API ID | `claude-fable-5-1` | `claude-opus-5-5` | `claude-sonnet-5` | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) |
| Price /MTok in → out | $10 → $50 | $4 → $20 | $2 → $10 | $1 → $5 |
| Relative latency | Slower | Moderate | Fast | Fastest |
| Thinking | Adaptive (always on) | Adaptive (always on) | Adaptive | Extended |
| Default effort | `high` | `medium` | `high` | not supported |
| Context window | 1M | 1M | 1M | 200K |
| Max output (sync) | 128K | 128K | 128K | 64K |
| Reliable knowledge cutoff | Jun 2026 | Jun 2026 | Jan 2026 | Feb 2025 |
| Retirement not sooner than | 2027-09-01 | 2027-09-22 | 2027-06-30 | 2026-10-15 |

**Docs' own default recommendation:** start with **Claude Opus 5.5** for most workloads; use **Claude
Fable 5.1** for demanding reasoning and long-horizon agentic work, "or when your evals on Claude Opus 5.5
at higher effort still fall short." That sentence is the model-selection method the course should teach:
*default → raise effort → only then change model.*

**Claude Opus 5.5** released 2026-09-22; per Anthropic it leads agentic coding and knowledge work, costs
about 40% less to run than Opus 5 on typical workloads, and prices below Opus 5's $5/$25.
Sources: <https://www.anthropic.com/claude-opus-5-5>, Opus 5.5 System Card (2026-09-22).

**Claude Mythos 5.1 is real** — same underlying model as Fable 5.1 with different safeguards, limited to
vetted organizations through trusted-access programs, aimed at cybersecurity and life-sciences work.
Source: <https://www.anthropic.com/claude-fable-and-mythos-5-1>. It is not in the public comparison table
but appears in pricing and feature-support tables, so it is legitimate to reference.

**Legacy but still available:** Fable 5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Opus 4.5, Sonnet 4.6,
Sonnet 4.5. Do not present any of these as the current recommendation.

## Cost mechanics

- Batch API: **50% off**.
- Prompt cache reads: **10% of base input price**; **2.5% on Fable 5.1 and Mythos 5.1**; **5% on Opus 5.5**.
  (Cache-read economics now differ *by model* — a real architectural discriminator.)
- Message Batches API supports up to **300K output tokens** on Opus 5.5, Opus 5, Sonnet 5, Opus 4.8,
  Opus 4.7, Opus 4.6 and Sonnet 4.6 with the `output-300k-2026-03-24` beta header.
- Tokenizer changed with Opus 4.7: 1M tokens ≈ 555k words on the current tokenizer (older models ≈ 750k
  words per 1M tokens). Any "tokens ≈ words" rule of thumb must say which tokenizer it assumes.
- Every Claude model ID is a **pinned snapshot**, including the dateless IDs from the 4.6 generation on.

## Thinking and effort — replaces the old extended-thinking story

Source: <https://platform.claude.com/docs/en/build-with-claude/effort> (fetched 2026-09-24).

This is the single most important correction for Domain 2 (and it changes Domain 4's cost/latency levers).
Material that teaches `thinking: {type: "enabled", budget_tokens: N}` as the way to buy reasoning depth is
**out of date** for the current lineup.

- **`effort` is the primary control** for how much the model reasons and what a request costs. Set it at
  `output_config.effort`. GA, no beta header, on the top-level parameter.
- Levels: **`low`, `medium`, `high`, `xhigh`, `max`**. `high` is the default on every supporting model
  except **Opus 5.5, which defaults to `medium`** — so a request that omits `effort` runs one level lower
  on Opus 5.5 than it did on Opus 5. Not every model supporting `max` supports `xhigh`.
- Effort applies to **all output tokens**: response text, tool calls and arguments, and thinking. Lower
  effort ⇒ fewer and terser tool calls, less preamble; higher effort ⇒ more tool calls, plans stated
  before acting, fuller summaries.
- Effort is "a **behavioral signal, not a strict token budget**." `max_tokens` is the hard limit on total
  output (thinking + response text), so set it large at high effort levels.
- **Adaptive thinking is always on and cannot be disabled on Opus 5.5** — `thinking: {"type": "disabled"}`
  returns a 400 at every effort level. On Opus 5, thinking cannot be disabled at `xhigh` or `max`.
- `adaptive` is a **thinking mode, not an effort value** — passing it as effort is an error.
- Extended thinking (the manual `enabled` + `budget_tokens` mode) is **deprecated on Opus 4.6 and
  Sonnet 4.6 and not accepted on later models**. Opus 4.5 is the only extended-thinking-only model that
  also supports effort.
- **Caching interaction (exam-grade material):** changing **top-level** effort between requests reshapes
  the rendered prompt and **invalidates cached prefixes**. Fable 5.1, Mythos 5.1, Opus 5.5 and Opus 5
  support a **per-message effort change** that **preserves the prompt cache**, via a `role: "system"`
  message with empty content carrying `output_config.effort`, behind beta header
  `mid-conversation-output-config-2026-07-01`. Guidance: hold top-level effort constant within a cached
  conversation; vary effort across workloads, not within one.
- Docs guidance is to **run an effort sweep on your own evals** rather than carrying settings across model
  generations. This is the "eval gate before you change a knob" discipline the course teaches — it is
  documented practice, not just our framing.
- Related surface worth covering: **task budgets** (advisory token budget for a full agentic loop) —
  <https://platform.claude.com/docs/en/build-with-claude/task-budgets>.

## Data retention / Covered Models — compliance-relevant

- **Covered Models** (Mythos-class) retain prompts and outputs for **30 days** for safety work, on every
  platform where they are offered; policy effective **2026-06-09**. Rationale per Anthropic: cross-request
  pattern detection for large-scale misuse (state-sponsored espionage, data-extortion campaigns).
  Sources: <https://support.claude.com/en/articles/15425695-covered-models>,
  <https://privacy.claude.com/en/articles/15425996-data-retention-practices-for-covered-models>,
  <https://platform.claude.com/docs/en/manage-claude/api-and-data-retention>.
- **Zero-data-retention eligibility excludes Covered Models.** Feature docs carry a `zdr.eligibility`
  field; the effort page reads `eligible` with the note "Excludes Covered Models." So "we require ZDR" and
  "we want the Mythos-class model" are **mutually exclusive** — a genuine, testable architectural
  constraint, and a good scenario discriminator.

## Deployment surfaces

Current models are addressable on the Claude API, **Claude Platform on AWS**, **Amazon Bedrock**,
**Google Cloud (Vertex AI)** and **Microsoft Foundry**, each with its own ID form. Bedrock and Google Cloud
set their own lifecycle/retirement dates; Microsoft Foundry and Claude Platform on AWS follow Anthropic's
first-party schedule. Bedrock offers global (dynamic routing) and regional (guaranteed data routing)
endpoints for Sonnet 4.5 and later — the regional/global distinction is the data-residency lever.
**Microsoft Foundry is a fifth surface that older prep material omits.**

## Exam facts (from the official guide — never drift from these)

63 items · 120 minutes · multiple-choice and multiple-response, each item stating how many to select ·
proctored via Pearson VUE · scaled 100–1000 with cut score **720** · **$175 USD** · valid **12 months** ·
criterion-referenced · domain percentages on the score report are diagnostic only · retake waits 14/30/90
days, max 4 attempts per rolling 12 months · on-time renewal is a free non-proctored assessment on the
Anthropic Partner Academy · exam code **CCAR-P** · guide v1.0 effective July 2026.

## Standing instruction

If your task touches anything in this file, cite it as `[VF]` plus the underlying URL. If you find that
this file is itself wrong or stale, say so explicitly in your report with the contradicting primary source
— that is a valued finding, not insubordination. The Domain 1 researcher doing exactly that is why this
file exists.

## Documentation host and tool staleness (added 2026-09-24 by orchestrator)

- **Canonical docs host is `https://platform.claude.com/docs/en/…`.** `docs.claude.com` URLs redirect (302)
  or 404. Cite the `platform.claude.com` form. The orchestrator confirmed the redirect directly.
- **The bundled local `claude-api` skill is a cached snapshot (reported as 2026-06-24) and is stale on the
  model lineup.** It is still useful for API shape and idioms, but **live docs win on every fact**, and this
  file wins over the skill. Two independent researchers (Domains 1 and 4) caught the same staleness; treat
  any skill/table/memory disagreement with live docs as the skill being wrong.
- Reported by the Domain 2 researcher and **pending validator confirmation** — do not state these as fact in
  a chapter until the Domain 2 validation file confirms them, but do investigate them: current models are
  reported to return **400** for non-default `temperature` / `top_p` / `top_k`, assistant **prefill**,
  `budget_tokens`, `thinking: {"type":"disabled"}` (Opus 5.5 / Fable 5.1), forced `tool_choice`, and
  citations combined with structured outputs. If confirmed, this **retires several classic prompt-engineering
  levers** (temperature tuning and prefill especially) for the current lineup, and any chapter teaching them
  as available tools must be corrected. This is high-value exam material either way: the architect-level
  point is that determinism levers moved from sampling parameters to `effort`, structured outputs, and
  tool-forced schemas.
- Two Anthropic sources give different prompt-caching impact ranges (2.5–3.7× vs 2.7–5.3×). Do not average
  them or pick one silently: state the range with its source, or teach the mechanism and skip the multiplier.

## Public-sector / FedRAMP posture — orchestrator adjudication 2026-09-24

The Domain 5 draft got this wrong, the Domain 5 validator corrected it, and the orchestrator then verified
the correction and found it needed refinement of its own. **This is the adjudicated version. Use it.**

Verified per Anthropic's own pages (accessed 2026-09-24):

- **Claude for Government (C4G)** is Anthropic's **FedRAMP High** offering, available to U.S. federal,
  state and local government and qualifying public-sector organizations.
  <https://support.claude.com/en/articles/13756069-public-sector-faqs>,
  <https://support.claude.com/en/articles/14503590-get-started-with-claude-for-government>
- **Claude in Amazon Bedrock (AWS GovCloud)** — "Approved for Use in FedRAMP High and DoD IL4/5 Workloads".
  <https://www.anthropic.com/news/claude-in-amazon-bedrock-fedramp-high>
- **Claude on Google Cloud Vertex AI (Assured Workloads)** — "FedRAMP High and IL2 Authorized".
  <https://www.anthropic.com/news/claude-on-google-cloud-fedramp-high>
- **CUI** may be processed in a FedRAMP High environment via **C4G, Bedrock, or Vertex**. Separately,
  **Claude Enterprise has a third-party NIST attestation for CUI use**. Customers requiring FedRAMP
  compliance must use C4G or a FedRAMP-authorized CSP path (Bedrock GovCloud / Vertex Assured Workloads).

**Corrections this forces on the Domain 5 draft:**
1. "CUI requires FedRAMP High **plus DoD IL4/5**" is **wrong**. DoD Impact Levels are a DoD Cloud Computing
   SRG construct for DoD workloads; they are not a prerequisite for handling CUI. Teach CUI → FedRAMP High
   environment; teach ILs only where the customer is DoD.
2. "The first-party Anthropic offering is not a FedRAMP-authorized boundary" is **wrong as written** —
   C4G is Anthropic's FedRAMP High product. The defensible architectural point is narrower: *the standard
   commercial Claude API is not the FedRAMP path; you must move to C4G or an authorized CSP path.*
3. The draft's **Bedrock = FedRAMP High + IL4/5** and **Vertex = IL2** statements are **supported** by the
   Anthropic pages above, so the IL4/5-vs-IL2 contrast is a legitimate discriminator. The validator's
   further claim that Bedrock's ceiling is **IL6 (Secret region)** is **not confirmed by these pages** —
   treat it as `[UNVERIFIED]` and do not build an item on it. **Do not overcorrect a correct claim.**
4. Authorization attaches to the **environment/infrastructure boundary**, not to individual model versions.
   Model availability inside C4G is its own question — see
   <https://support.claude.com/en/articles/14503794-model-availability-in-claude-for-government>.

**Exam-grade takeaway to teach:** compliance posture is chosen at the **deployment surface**, and the
architect's move when a requirement lands (FedRAMP, CUI, PHI, residency) is to change the surface or the
contractual instrument — not to add a prompt instruction. Because per-surface authorizations change, teach
the *decision procedure* ("identify the obligation → pick the authorized surface → confirm current
authorization and model availability for that surface → document the evidence") rather than a memorized
matrix. Any specific authorization level in a chapter carries its access date.

## Other verified specifics worth reusing

- **Covered Models are exactly four:** `claude-fable-5-1`, `claude-mythos-5-1`, `claude-fable-5`,
  `claude-mythos-5` — 30-day retention, ZDR only if expressly authorized. Mythos access is restricted
  (trusted-access program); do not present Mythos as generally available.
- **`inference_geo`** accepts **`"us"` and `"global"`** only — there is no EU residency pin on the
  first-party API. Data-residency pinning happens via a CSP surface (e.g. Bedrock regional endpoints).
- **Citations:** Anthropic docs state citations "are guaranteed to contain valid pointers." A chapter must
  NOT claim the docs acknowledge citation/quote mismatches — that attribution was fabricated and removed.
  The honest architectural point is that a valid pointer proves provenance, **not** that the cited source is
  correct or that the surrounding claim is entailed by it.
- **MCP specification revision is 2026-07-28** (per the Domain 3 researcher), and **Dynamic Client
  Registration is deprecated in favor of Client ID Metadata Documents**. Teach version-invariant rules and
  date any version-specific statement. Pending Domain 3 validator confirmation.
