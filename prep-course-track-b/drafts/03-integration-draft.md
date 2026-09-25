# Domain 3 — Integration

## 1. Front matter

| | |
|---|---|
| **Domain** | 3 — Integration |
| **Weight** | 19% — the heaviest domain |
| **Approx. items** | ~12 of 63 scored items |
| **Exam** | CCAR-P, 63 items / 120 min, cut score 720 of 100–1000 `[D03-S01]` |

**Objectives (verbatim, `[D03-S01]` §6):** (1) Evaluate tool/agent configuration for capability bloat. (2) Analyze
authentication and authorization requirements to identify security gaps. (3) Evaluate accuracy-latency trade-offs
and justify configuration decisions. (4) Analyze observability challenges and select monitoring strategies at scale.
(5) Design a RAG pipeline with appropriate chunking and indexing strategies. (6) Apply retrieval strategies matched
to data shape and query pattern. (7) Evaluate connection protocols and select the appropriate integration mechanism
(MCP, API/CLI, agent-to-agent). (8) Evaluate progressive discovery vs. monolithic context strategy.

> **Model note (verified 2026-09-24, `[D03-S29]`).** Current lineup: Fable 5.1 (1M context, $10/$50 per MTok),
> Opus 5.5 (1M, $4/$20), Sonnet 5 (1M, $2/$10), Haiku 4.5 (200K, $1/$5). Opus 5 and earlier releases are legacy but
> still served. Batch is 50% off; cache reads cost 10% of base input (5% on Opus 5.5, 2.5% on Fable 5.1). This
> chapter reasons in **tiers** — Opus-tier, Sonnet-tier, Haiku-tier — because the exam tests the trade-off, not the
> price list.

---

## 2. Exam-relevance framing

Integration carries the largest weight because it is where architectural judgment is most visible and most expensive
to get wrong. It does not test parameter recall. It tests whether, given a working system and a competing
constraint, you pick the change that moves the *binding* constraint. The guide's Sample 1 `[D03-S01]` is the
template: four changes that all "reduce risk," one of which removes the privilege.

| Distractor archetype | How it reads | Why it loses | Tell |
|---|---|---|---|
| **Compensating control as control** | "Log the destructive tool." "Add a confirmation." | Detective and deterrent controls do not shrink the attack surface; least privilege means removal `[D03-S01]`. | Stem names a principle; one option deletes the capability. |
| **Prompt-side enforcement** | "Instruct the model not to read other tenants' records." | Defeated by injection; MCP requires servers to verify every inbound request and never trust client-supplied identity `[D03-S06]`, `[D03-S11]`. | A security rule placed in text the model reads. |
| **Bigger model as architecture** | "Use a more capable model so it follows instructions." | Model capability is unrelated to authorization scope, index freshness, or tenant isolation `[D03-S01]`. | Deterministic symptom, probabilistic remedy. |
| **Right lever, wrong bottleneck** | "Enable streaming" for a cost problem; "change tier" for a stale index. | Streaming changes perceived first-token latency only; tier does not fix retrieval `[D03-S25]`. | Map symptom to layer before reading options. |
| **Monolithic context as thoroughness** | "Load all 200 tool definitions so nothing blocks." | Selection degrades past 30–50 tools; definitions alone can cost ~55K tokens `[D03-S02]`, `[D03-S15]`. | Option maximizing availability over need. |
| **Retrieval where a query belongs** | "Embed the transactions table to answer spend questions." | Embeddings cannot aggregate; chunking rows destroys join semantics. | Stem's data is tabular, temporal, or graph-shaped. |

**Reading a stem.** Name the layer the symptom lives in (identity, tool surface, retrieval, transport, telemetry);
the binding constraint (accuracy, p95, cost, blast radius, audit); and whether the question wants the **best**, the
**first**, or the **most likely**. "First" rewards the cheapest diagnostic; "best" rewards the structural fix.

---

## 3. Core concepts

**3.1 Capability bloat** — a configuration exposing capabilities the role does not require. Three independent costs
with three different fixes: *token overhead* (schemas render into the prefix every request; the tool-use system
prompt alone is 286 tokens on Opus-tier `[D03-S03]`) → defer; *selection degradation* (accuracy falls past **30–50
tools** `[D03-S02]`) → consolidate, namespace, search; *blast radius* → **remove**. *Decision:* per tool, does this
role need it? No → delete. Rarely → defer. Often → keep and describe explicitly. *Alternatives:* consolidation into
one tool with an `action` parameter, service namespacing (`github_list_prs`) `[D03-S04]`, `[D03-S18]`, tool search,
MCP toolset allowlisting, filesystem/code-execution discovery. *Misconception:* that logging or confirming a
dangerous tool satisfies least privilege `[D03-S01]`.

**3.2 Progressive disclosure and context rot** — every tool definition is still sent in `tools`, but those marked
`defer_loading: true` stay out of the model's context until a search tool discovers them and the API appends a
`tool_reference` `[D03-S02]`. This matters because "as the number of tokens in the context window increases, the
model's ability to accurately recall information from that context decreases" `[D03-S17]`, so loading more is not
monotonically better. Crucially, deferred loading cuts context **without breaking the prompt cache** — "The prefix
is untouched, so prompt caching is preserved" `[D03-S02]` — whereas rewriting `tools` per turn changes the front of
the prefix and invalidates everything `[D03-S31]`. *Decision:* hybrid. Pre-load the small always-needed context and
expose primitives for just-in-time retrieval, as Claude Code does with pre-loaded conventions plus grep/glob,
accepting that "runtime exploration is slower than retrieving pre-computed data" `[D03-S17]`. Enable tool search at
≥10 tools or ~10K tokens of definitions, keeping the 3–5 most-used tools non-deferred `[D03-S02]`.
*Misconceptions:* that `defer_loading` reduces what you *transmit* (it reduces what enters context), and that a 1M
window ends context engineering (it changes what fits, not what the model attends to).

**3.3 Agent identity vs. end-user identity** — the agent's own principal (service account, workload identity) is
distinct from the human it acts for. *Delegated* (on-behalf-of) access carries the user's authorization downstream;
*service-account* access carries the agent's. A service account holding the union of all users' permissions makes
downstream systems unable to answer "who did this," and turns prompt injection into privilege escalation.
*Decision:* if the downstream system enforces per-user authorization, delegate and let it say no; if the work is
genuinely system-level (index build, nightly reconciliation), use a narrowly scoped service account and record the
initiating user as metadata. *Misconception:* that authentication settles authorization — MCP lists "treating
claimed scopes in token as sufficient without server-side authorization logic" as a common mistake `[D03-S06]`.

**3.4 Token passthrough and the confused deputy** — passthrough is "an anti-pattern where an MCP server accepts
tokens from an MCP client without validating that the tokens were properly issued *to the MCP server* and passes
them through to the downstream API" `[D03-S06]`. The rules: "MCP servers **MUST NOT** accept any tokens that were
not explicitly issued for the MCP server" `[D03-S06]`; "the MCP server **MUST NOT** pass through the token it
received from the MCP client" `[D03-S07]`. The *confused deputy* is the proxy variant — a static third-party client
ID, clients registering dynamically, a consent cookie already set at the third-party authorization server, and no
per-client consent before forwarding — so an attacker's registered client with an attacker-controlled `redirect_uri`
harvests an authorization code with the consent screen silently skipped `[D03-S06]`. Both pass functional testing
and surface as incidents. *Decision:* validate audience server-side on every inbound token (RFC 8707 `resource`);
mint a separate upstream token; check a per-user registry of approved `client_id`s **before** forwarding; match
`redirect_uri` by exact string comparison; store `state` server-side only **after** consent, single-use and
short-lived `[D03-S06]`, `[D03-S23]`. *Misconception:* that a "pure proxy" is neutral — it breaks audit on both
sides, bypasses downstream rate limiting, and lets a stolen token use your server for exfiltration.

**3.5 Tool descriptions and results are untrusted input** — text from a tool server enters context
indistinguishable from instruction unless the harness intervenes. Clients "**MUST** consider tool annotations to be
untrusted unless they come from trusted servers," should "Validate tool results before passing to LLM," and should
"Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration"
`[D03-S10]`. *Decision:* pin third-party tool lists — connector pinning exists so "a server that changes its tools
doesn't change what Claude sees partway through a conversation" `[D03-S05]`; allowlist, not denylist; never let a
tool result authorize an action. *Misconception:* that `readOnlyHint`/`destructiveHint` are enforcement.

**3.6 Retrieval strategy vs. RAG pipeline** — a *strategy* is the mechanism (semantic, lexical, SQL, graph, live API
lookup, agentic file search, full-context stuffing); a *pipeline* is the machinery behind one of them (chunking,
enrichment, embedding, indexing, refresh, retrieval, reranking, assembly). Most production failures are strategy
errors: a vector index over a transactions table, or over data whose value was freshness. *Decision:* pick the
mechanism from data shape and query pattern first (§4.6), design the pipeline second; under ~200K tokens (~500
pages), skip the pipeline and stuff the corpus with caching `[D03-S14]`. *Misconception:* that RAG means vector
database — Anthropic's measured pipeline is explicitly hybrid `[D03-S14]`.

**3.7 Contextual retrieval** — before embedding and BM25 indexing, prepend to each chunk a short model-generated
statement of where it sits in its parent document: *"Please give a short succinct context to situate this chunk
within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the
succinct context and nothing else."* Context runs 50–100 tokens per chunk; one-time preprocessing with caching costs
**$1.02 per million document tokens**. Measured top-20 failure rate: 5.7% baseline → 3.7% with contextual embeddings
(−35%) → 2.9% adding contextual BM25 (−49%) → **1.9%** adding reranking (−67%) `[D03-S14]`. *Decision:* it is the
highest-leverage change to a dense-only pipeline and costs nothing at query time, unlike reranking — add it first
when latency is tight. *Misconception:* that chunk size is the main lever. Anthropic says chunk size, boundary, and
overlap "can affect retrieval performance" and recommends experimentation; it prescribes no value `[D03-S14]`.

**3.8 Observability for agentic systems** — a trace per request, a span per model call and per tool call, with usage
and cost as attributes. The OpenTelemetry GenAI conventions name inference spans
`{gen_ai.operation.name} {gen_ai.request.model}`, **require** `gen_ai.operation.name` and `gen_ai.provider.name`,
conditionally require `gen_ai.request.model` and `error.type`, and **recommend** `gen_ai.usage.input_tokens`,
`gen_ai.usage.output_tokens`, `gen_ai.response.model`, `gen_ai.conversation.id`, and
`gen_ai.response.finish_reasons` `[D03-S21]`. Tool execution is its own `execute_tool` span; agent workflows add
`create_agent`, `invoke_agent`, `invoke_workflow`, and `plan`, with agent identity recorded "at span creation time
**for sampling decisions**" `[D03-S22]`. *Decision:* instrument structure at 100%, content selectively — content "is
likely to contain sensitive information including user/PII data" and instrumentations "**SHOULD NOT** capture this
attribute by default. Capture **SHOULD** be gated by an explicit user opt-in" `[D03-S21]`. *Misconception:* that
dashboards are observability. Aggregates say *that* quality dropped; only a trace tied to a complaint says *why*,
and the join key is the `request-id` response header, also the `request_id` in error bodies `[D03-S25]`.

**3.9 Protocol as an architectural commitment** — MCP, a direct API/SDK call, a CLI subprocess, and agent-to-agent
protocols each fix a different set of properties: reuse, runtime discoverability, hop count, trust boundary, and who
operates it. Sharpest discriminator: **MCP exposes stateless tools and data to a model; agent-to-agent protocols let
two autonomous agents negotiate.** A2A's own framing is that wrapping an agent as a simple tool is "limiting: it
can't capture the agent's full capabilities" `[D03-S19]`. *Misconception:* that MCP is always the modern choice —
for one application calling three fixed endpoints it adds a server, an OAuth resource server, and a hop for no
reuse benefit.

---

## 4. Trade-off analyses

### 4.1 Reducing risk on an over-broad tool surface

| Change | Control type | Removes capability? | Token cost after | Survives injection? | Choose when |
|---|---|---|---|---|---|
| Delete the tool, or scope tool sets per role | Preventive | **Yes** | Zero | Yes | The role never needs it — default answer to a least-privilege stem `[D03-S01]` |
| MCP toolset allowlist (`default_config: {enabled: false}` + per-tool enable) | Preventive, enforced API-side | Yes | Zero for disabled tools | Yes | Tools come from a third-party server you don't control `[D03-S05]` |
| Narrower tool (`refund(max_amount)`) | Preventive | Reduces it | Similar | Yes | Action needed, but only within bounds |
| Human confirmation gate | Compensating | No | Full | Only if the human reads the arguments | Legitimately needed, hard to reverse `[D03-S32]` |
| Audit logging | Detective | No | Full | No | Evidence requirements — in addition to, never instead of, removal |
| `defer_loading: true` | Efficiency, not security | No | Near zero until discovered | No — still callable | Needed occasionally, context budget tight `[D03-S02]` |
| Larger model | Neither | No | Higher | No | Never, for an authorization problem `[D03-S01]` |

**Discriminator:** *least privilege / blast radius* → remove. *Auditability* → log. *Context budget / selection
accuracy* → defer or consolidate.

### 4.2 Scaling the tool surface

| Strategy | Context before first turn | Accuracy at scale | Cache | New failure modes | Choose when |
|---|---|---|---|---|---|
| Load every tool | ~55K tokens for 58 tools / 5 MCP servers `[D03-S02]`, `[D03-S15]` | Degrades past 30–50 tools | Fully cacheable | None | <10 tools, all used most requests, <100 tokens of definitions `[D03-S02]` |
| Consolidate + namespace | Lower | Best per tool exposed | Stable | Fat `action`-enum tools can be misused | Always, first `[D03-S04]`, `[D03-S18]` |
| Tool search + `defer_loading` | **>85% reduction**; loads the 3–5 needed `[D03-S02]` | MCP-eval 79.5% → 88.1% `[D03-S15]` | **Preserved** — references appended, prefix untouched | One search hop; weak descriptions become undiscoverable | ≥10 tools, >10K tokens of definitions, multi-server aggregation |
| Programmatic tool calling | Unchanged | +2.9 pts internal retrieval, +4.7 pts GIA `[D03-S15]` | Unchanged | Needs a code-execution environment | 3+ dependent calls or bulky intermediates; 43,588 → 27,297 tokens (−37%) `[D03-S15]` |
| Tools as files in a sandbox | 150,000 → 2,000 tokens (−98.7%) `[D03-S16]` | High — read on demand | n/a | Needs "a secure execution environment with appropriate sandboxing, resource limits, and monitoring" `[D03-S16]` | Thousands of tools **and** you already run a sandbox; intermediates and PII never enter context |
| Mid-conversation tool changes | Unchanged | n/a | Preserved (tools pre-declared deferred) | App must decide correctly | Your app, not the model, must grant or revoke a capability mid-session `[D03-S31]` |

**Discriminator:** *discovery* → tool search. *Control* → mid-conversation tool changes `[D03-S31]`.
*Intermediate-result volume* → programmatic tool calling. *Two near-identical tools* → consolidate; search will not
resolve ambiguity.

### 4.3 Identity and token model

| Model | Authorized downstream | "Who did this?" | Injection blast radius | Choose when |
|---|---|---|---|---|
| One service account, union of all permissions | The agent | "The agent" — useless | Everything the agent can reach | Never in a multi-user system |
| Service account per job, least-scoped | The agent, narrowly | The job | That job only | System-level work: index builds, reconciliation, batch scoring |
| Delegated / on-behalf-of, correct audience | The end user | The user, natively in downstream logs | The user's own permissions | Downstream already enforces per-user authorization — **default for interactive agents** |
| Client token forwarded unchanged | Ambiguous | Broken on both sides | Whatever the token reaches anywhere | **Forbidden** — token passthrough `[D03-S06]` |
| Broad scopes up front (`files:*`, `admin:*`) | Over-authorized | Noisy — "omnibus scope masks user intent per operation" `[D03-S06]` | Maximal; enables privilege chaining | Never. Minimal initial scopes with incremental elevation via `WWW-Authenticate` scope challenges `[D03-S06]` |

**Discriminator:** "if this agent is prompt-injected, what can the injected instruction reach?" That answer is the
identity model's blast radius, and it is the only question a security review really has.

### 4.4 Multi-tenant isolation in retrieval

| Approach | Isolation | Query latency | Ops cost | Dominant failure mode | Choose when |
|---|---|---|---|---|---|
| One index per tenant | Physical | Best | Highest (N indexes, N refresh jobs) | Index sprawl; per-tenant staleness drift | Few large tenants; contractual or regulatory isolation |
| Shared index, tenant filter injected server-side at query time | Strong if unbypassable | Best | Lowest | One code path omits the filter → full leak | Many tenants, uniform schema, filter injected by the service and never taken from the model |
| Shared index, per-document ACLs filtered against caller's groups | Fine-grained | Good | Medium | ACL sync lag — a revoked user still retrieves the doc | Document systems with per-item permissions |
| Retrieve IDs, then authorize each hit at the system of record | Strongest logical | Worst (+1 hop per hit) | Highest | Load on the system of record | Stale ACLs are unacceptable |
| Instruct the model to filter | **None** | — | — | Defeated by injection | Never — not a control `[D03-S06]` |

**Discriminator:** the filter value must come from the authenticated session and be applied by code the model cannot
influence. If an answer puts the tenant ID anywhere the model can rewrite, it is wrong.

### 4.5 Accuracy / latency / cost knobs

| Knob | Accuracy | p95 latency | Cost | Reach for it when |
|---|---|---|---|---|
| Model tier up | ↑ | ↑ | ↑ | Quality gap persists at max effort on the cheaper tier `[D03-S29]` |
| `effort` up | ↑ | ↑ | ↑ | Cheaper than a tier change; lower effort means "fewer and more-consolidated tool calls, less preamble" `[D03-S32]` |
| Fewer agent turns | ↑ or neutral | ↓↓ | ↓↓ | Cost grows with roughly the square of turn count `[D03-S33]` |
| Parallel tool calls | neutral | ↓↓ | neutral | Independent reads. Return **all** results in one user message or the model stops parallelizing `[D03-S31]` |
| Programmatic tool calling | ↑ | ↓ (removes inference passes) | ↓37% tokens | Chained calls with bulky intermediates `[D03-S15]` |
| Prompt caching | neutral | ↓ TTFT | ↓2.5–3.7× on agent loops at 81–90% hit rate `[D03-S33]` | Always. Cached input also doesn't count toward ITPM on most models `[D03-S24]` |
| Streaming | neutral | ↓ **perceived** only | neutral | User-facing text; also the mitigation for 504 on long generations `[D03-S25]` |
| Reranking | ↑↑ (2.9% → 1.9% failure) `[D03-S14]` | ↑ one hop | ↑ | Accuracy dominates and latency has room |
| Contextual embeddings + contextual BM25 | ↑↑ (−49% failures) `[D03-S14]` | **neutral at query time** | One-time $1.02/M doc tokens | Accuracy matters and latency is tight |
| top-k up | ↑ then flat or ↓ (context rot) | ↑ | ↑ | Recall is the measured gap `[D03-S17]` |
| Async + callback, or Batch | neutral | Removes the user from the wait; batch in hours (most <1h, 24h expiry) | Batch **−50%** | No human waiting; 100,000 requests or 256 MB per batch, results kept 29 days `[D03-S26]` |
| `max_tokens` | Truncation = failed attempt | — | — | A backstop, not a knob — a 16,384 cap ended 15% of Opus-tier coding attempts, "none of them solved" `[D03-S33]` |

**Discriminator:** levers that change the *number of terms* in the latency sum (turn count, parallelism, PTC)
dominate levers that shrink each term (tier, effort). Streaming changes no term.

### 4.6 Retrieval strategy by data shape and query pattern

| Data shape | Query pattern | Choose | Why the plausible alternative loses |
|---|---|---|---|
| Relational / tabular (ledger, claims, inventory) | Aggregate, filter, join | Parameterized SQL behind a narrow tool | Embeddings cannot compute `SUM`; chunking rows destroys join semantics |
| Relational, thousands of result rows | Aggregate then summarize | SQL + programmatic tool calling / code execution | Raw rows blow the budget; PTC filters before context `[D03-S15]`, `[D03-S16]` |
| Long prose (policy, contracts, manuals) | Conceptual, paraphrased | Hybrid dense + BM25 over contextualized chunks, then rerank | Dense-only leaves 3.7% top-20 failure vs 1.9% `[D03-S14]` |
| Long prose | Exact identifier (clause 7.3.1, error `E4012`, SKU) | Lexical/BM25 or exact-match pre-filter first | Dense embeddings under-weight rare tokens — the gap contextual BM25 closes `[D03-S14]` |
| Source code | "Where is X implemented / what calls Y" | Agentic file search over the live tree (glob/grep/read) | An embedding index is stale one commit later `[D03-S17]` |
| Tickets / CRM with rich metadata | "Similar prior cases, last 90 days" | Dense semantic **plus** metadata filters | Lexical misses paraphrase; unfiltered dense returns relevant-but-inapplicable hits |
| Time series, metrics, logs | Trend, anomaly, windowed aggregate | The store's own query language via a tool | Serialized points are lossy and unaggregatable once chunked |
| Entity–relationship graph (supply chain, fraud rings) | Multi-hop ("who else touched this claim") | Graph traversal tool | Chunk retrieval cannot follow edges |
| Live system-of-record state (order status, balance) | Point lookup by ID | **Direct API call — do not index** | Any index adds staleness to data whose whole value is freshness |
| Corpus under ~200K tokens (~500 pages) | Anything | Full-context stuffing + prompt caching | Below the threshold a pipeline adds failure modes without adding recall `[D03-S14]` |
| Mixed corpus, open-ended research | Exploratory, multi-step | Agentic search: successive narrowing queries | One-shot top-k cannot reformulate; each result informs the next `[D03-S17]` |

### 4.7 Protocol / integration-mechanism selection

| Mechanism | Reuse across clients | Runtime discovery | Latency | Trust boundary | Ops surface | Choose when |
|---|---|---|---|---|---|---|
| Direct API/SDK call in your code | None | None | Lowest, in-process | Inside your app | Smallest | One consumer, fixed operations, tightest control |
| **MCP, remote (Streamable HTTP)** | High — any MCP client | Yes (`tools/list`, `listChanged`) | +1 hop per call | New: you run an OAuth 2.1 resource server that must validate token audience `[D03-S07]` | Server, auth, `Origin` validation (403 on invalid), sessions `[D03-S09]` | Several clients reuse the capability and it deploys independently; pin the tool list `[D03-S05]` |
| **MCP, local (stdio)** | Per machine | Yes | Lowest MCP option | Subprocess with the client's privileges; credentials "from the environment," not OAuth `[D03-S07]` | Process lifecycle; sandboxing advised `[D03-S06]` | Workstation tooling — "Clients **SHOULD** support stdio whenever possible" `[D03-S09]` |
| CLI / subprocess wrap | Low | No | Process-spawn overhead | Weakest — an opaque command string, same shape for every action `[D03-S32]` | Easy to write, hard to gate or audit | No API exists; a documented path is the Claude Code CLI with `-p --output-format json` `[D03-S30]` |
| **Agent-to-agent (A2A)** | High | Agent Card at `/.well-known/agent-card` `[D03-S19]` | Highest — long-running, async, streamed artifacts | Two autonomous parties; "opaque execution" protects each side's logic and IP `[D03-S19]` | Task lifecycle, streaming, per-counterparty auth | The counterpart is itself an agent needing multi-turn negotiation and delegation |
| Managed Agents / Agent SDK | n/a — a harness, not a protocol | n/a | n/a | Anthropic hosts the loop (+sandbox), or you host the Claude Code harness | Versioned agent configs | You want the agent loop and built-in tools, not a new integration surface `[D03-S30]` |

**Discriminators.** One consumer → direct call. Many consumers, one capability → MCP. Local only → stdio MCP.
Autonomous counterpart → A2A. No API exists → CLI, with an executable allowlist and shell-operator rejection, since
"commands are untrusted model output… A blocklist is not sufficient" `[D03-S31]`. Two constraints decide cases on
their own: the Anthropic MCP connector supports **only tool calls** — no resources, prompts, sampling, or
elicitation — requires a **public HTTPS** server, cannot reach local stdio servers, and is **not ZDR-eligible**
`[D03-S05]`. If you need resources, prompts, or a local server, run your own MCP client.

### 4.8 Observability capture strategy at scale

| Strategy | Debuggability | Telemetry cost / cardinality | Privacy exposure | Choose when |
|---|---|---|---|---|
| Full prompt and completion capture | Highest | Highest; grows with tokens | Highest — PII in traces `[D03-S21]` | Pre-production, or an explicit opt-in debug session |
| Structural spans 100% + content on a small gated sample | High enough | Moderate | Low | **Default at scale** — content capture "SHOULD NOT" be on by default `[D03-S21]` |
| Add 100% of errors and high-cost traces, and head-sample by session | High where it matters; whole sessions survive, not fragments | Moderate | Low | You need the pathological tail, which uniform sampling loses, and a single span is meaningless in a multi-turn agent `[D03-S40]` *(practitioner)* |
| Metrics only | Low — says *that*, never *why* | Lowest | None | Capacity planning only |

**Non-negotiables regardless of strategy:** a span per tool call with tool name and call ID `[D03-S21]`; token count
and computed cost as numeric span attributes so the sampler can keep expensive traces `[D03-S40]`; the platform
`request-id` on spans so a complaint resolves to an API call `[D03-S25]`; retrieval-quality signals (which chunks
were returned, whether the answer cited them) so a recall regression is visible before it looks like a
hallucination; and no unbounded-cardinality span names — the conventions deliberately omit a response ID from one
span name "due to high cardinality" `[D03-S21]`.

### 4.9 Chunking, enrichment, and indexing

| Strategy | Retrieval precision | Answer completeness | Build cost | Choose when |
|---|---|---|---|---|
| Fixed-size with overlap | Baseline | Overlap mitigates boundary loss | Lowest | Homogeneous prose; a defensible default while you measure `[D03-S14]` |
| Structure-aware (heading, clause, row) | High — boundaries match how users ask | High | A parser per format | Real structure: policies, contracts, API docs, statutes |
| Semantic (split on topic shift) | High | Medium | Model calls per document | Transcripts and notes with no reliable markup |
| Contextual enrichment | **−35% failures alone, −49% with BM25** `[D03-S14]` | High | One-time $1.02/M doc tokens | Almost always — preprocessing only, no query-time cost |
| Parent-document (retrieve small, return large) | High | High — model sees surrounding context | Extra parent store | Chunks precise enough to find but too small to answer from |

**Citation granularity is a chunking decision.** Plain-text documents are chunked into sentences and cite by
character index; PDFs by sentence, citing by page; custom-content blocks get no further chunking and cite by block
index `[D03-S28]`. So: one chunk per plain-text `document` block when you want **sentence-level** citations into your
chunks; `custom content` blocks when you want citations at **your** boundaries and no further splitting `[D03-S28]`.
`search_result` blocks carry `source` and `title` for RAG attribution, with guidance to "Break long content into
logical text blocks to give Claude finer citation boundaries" `[D03-S27]`. Citations are all-or-none per request and
**incompatible with structured outputs** (400) `[D03-S28]`.

**Indexing and refresh.** Pin the embedding-model identifier as index metadata so a model change forces a full
re-embed instead of silently mixing vector spaces. Upsert incrementally keyed on a content hash; write tombstones
for deletions. Treat maximum index lag as an SLO with a metric behind it. Evaluate retrieval **separately** from
generation (failure-rate at k on a labeled query set) so a recall regression is caught before it looks like a
hallucination — the diagnosis the guide's Sample 3 rewards `[D03-S01]`.

### 4.10 Progressive discovery vs. monolithic context

| | Monolithic | Progressive | Hybrid (recommended) |
|---|---|---|---|
| Tokens before first useful turn | Highest — ~55K for 5 MCP servers `[D03-S02]` | Lowest | Small fixed core |
| Accuracy / latency | Degrades with context rot and tool count `[D03-S17]`; one round trip | High per decision; extra discovery turns | High; core instant, rest on demand |
| Cache | Cacheable if the prefix is stable | Cacheable **only** via tool search, deferred tools, or skills `[D03-S02]` | Cacheable |
| Failure mode | Ignores the middle of a huge context; picks among near-duplicates | Never discovers what it needs; "may spend discovery turns fetching what it previously read inline" `[D03-S33]` | Mis-drawing the line between core and on-demand |
| Choose when | <10 tools; small corpus; uniform requests | Large tool libraries and corpora; heterogeneous requests | Default `[D03-S17]` |

**Threshold:** tool search "pays once schemas run past roughly 10K tokens (MCP servers reach that fast); below that
the search step is overhead" `[D03-S33]`.

---

## 5. Worked scenarios

**S1 — Financial services: a support agent that can wire money.** A bank's agent exposes `read_ticket`,
`draft_reply`, `issue_refund`, `initiate_transfer`, `close_account`; tier-1 staff only read and draft. SOX
auditability; pen test in flight. *Candidates:* log the write tools; confirmation modal; split into a tier-1 agent
with two tools and a supervisor agent with the rest; larger model. *Recommended:* the split. Logging is detective —
the money still moves; a modal leaves the capability reachable and click-through approval is theater; model size is
unrelated to authorization scope `[D03-S01]`. *What would change it:* if tier-1 needed small refunds, the answer
becomes a narrow `issue_refund(max_amount)` plus a gate — a smaller capability, not a guarded large one.

**S2 — Healthcare: 40,000 clinical policy PDFs, confident-but-wrong after a refresh.** Answers turn confidently
wrong the morning after a quarterly refresh; latency and model version unchanged. *Candidates:* raise `effort`;
inspect retrieval/indexing; lower temperature; enlarge the window. *Recommended:* inspect retrieval — whether the
re-index completed, deletions were tombstoned, and the embedding model changed between old and new vectors
`[D03-S01]`, `[D03-S14]`. Nothing about a document refresh changes what the model knows, how it samples, or how much
it holds; the other three treat a data-plane failure as a model-plane one. *Then:* make retrieval separately
measurable and add contextual embeddings plus contextual BM25 — 5.7% → 2.9% top-20 failure `[D03-S14]`.

**S3 — Retail: 6 MCP servers, 180 tools, wrong tool ~20% of the time.** Definitions cost tens of thousands of
tokens; p95 over budget. *Candidates:* six specialist agents; tool search with `defer_loading` keeping five loaded;
shorten every description; faster tier. *Recommended:* tool search, after consolidating near-duplicates and
namespacing by service — >85% context reduction with MCP-eval accuracy 79.5% → 88.1% `[D03-S02]`, `[D03-S15]`.
Splitting into six agents adds orchestration and handoff loss for a configuration problem; shortening descriptions
makes tools *less* discoverable, since search matches names, descriptions, and argument descriptions `[D03-S02]`;
tier trades on the wrong axis. *What would change it:* genuinely ambiguous tools — "If a human engineer can't
definitively say which tool should be used… an AI agent can't be expected to do better" `[D03-S17]` — need
consolidation, not discovery.

**S4 — Government: an MCP server fronting a records API.** The team plans to forward the caller's bearer token
upstream unchanged. FedRAMP-style audit; citizen PII. *Candidates:* ship with logging; validate the inbound token's
audience and obtain a separate upstream token as an OAuth client; allowlist caller IPs; move to stdio.
*Recommended:* audience validation plus a separate upstream token — "MCP servers **MUST NOT** accept any tokens that
were not explicitly issued for the MCP server," and the server "**MUST NOT** pass through the token it received"
`[D03-S06]`, `[D03-S07]`. Logging is the anti-pattern with a log line; IP allowlisting is network control for an
identity failure; stdio breaks the multi-client requirement. *Also required:* per-client consent before forwarding
to any third-party authorization server, exact-string `redirect_uri` matching, `Origin` validation returning 403,
and session IDs never used for authentication `[D03-S06]`, `[D03-S09]`.

**S5 — Multi-tenant SaaS: one tenant sees another's document.** A shared vector index serves 4,000 tenants; the
system prompt already says "only use the current tenant's documents." *Candidates:* strengthen the prompt; inject a
mandatory tenant filter in the retrieval service from the authenticated session, plus a test that fails if absent;
one index per tenant; filter foreign snippets out of the answer. *Recommended:* the server-side filter. Prompt
hardening is prompt-side enforcement of a server-side invariant; per-tenant indexes are correct but
disproportionate at 4,000 and leave the leak live for weeks; answer-side filtering still admits foreign data into
context, where it can be paraphrased before filtering. *What would change it:* churning per-document ACLs escalate
to authorizing each hit at the system of record.

**S6 — Telco: p95 of 13s against a 6s SLA.** Nine agent turns, top-k 40 with reranking, Opus-tier at `high` effort,
non-streaming; accuracy already acceptable. *Candidates:* smallest tier; drop reranking; collapse three chained
lookups into one programmatic tool call, parallelize independent reads, stream, confirm the prefix is cached; raise
`max_tokens`. *Recommended:* the fourth. Turn count dominates — cost and latency grow with roughly the square of
turns `[D03-S33]` — and programmatic tool calling removes inference passes while cutting tokens 37% `[D03-S15]`;
streaming makes first token near-immediate `[D03-S25]`; caching cuts TTFT and, because cached input doesn't count
toward ITPM on most models, raises headroom `[D03-S24]`. Tier and reranking both spend accuracy the stem says you
have; `max_tokens` affects neither.

**S7 — Legal: every sentence must be attributable.** The team concatenates retrieved chunks into one prompt and
asks the model to quote sources; quotes are occasionally invented. *Candidates:* instruct harder; pass each chunk as
its own plain-text `document` with citations enabled, or as `search_result` blocks with `source` and `title`;
string-match quotes post hoc; fine-tune. *Recommended:* the citation-native path `[D03-S27]`, `[D03-S28]`.
Instruction creates no verifiable link; post-hoc matching is a fragile guardrail over a solved problem; fine-tuning
is the most expensive fix for a grounding concern. *Watch out:* citations are all-or-none per request and
**incompatible with structured outputs** — if a consumer needs strict JSON you must choose, and attribution
requirements win `[D03-S28]`.

**S8 — Cross-cutting: justifying a configuration to a CFO and a CISO at once.** Bring three numbers and one
boundary. Cost per *completed task*, not per token — "a cheaper request that needs more turns or retries to finish
the job isn't cheaper" `[D03-S33]`. Measured accuracy, with retrieval measured separately from generation. p95
decomposed into terms, so the CFO sees that batch (−50% `[D03-S26]`) and caching (2.5–3.7× on agent loops
`[D03-S33]`) are free wins while effort and tier are purchases. The boundary is blast radius: which tools exist,
whose identity they run as, and what an injected instruction could reach.

---

## 6. Failure modes and diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| Confident-but-wrong right after a data refresh; latency and model unchanged | Broken re-index, mismatched embedding model, un-tombstoned deletions | Index doc count and build timestamp vs. source; embedding-model ID in index metadata | Re-embed with a pinned model ID; incremental upsert on content hash; index-lag SLO `[D03-S01]` |
| Right document exists, never retrieved for an exact identifier | Dense-only retrieval under-weights rare tokens | Same query through a lexical index | Add BM25 alongside dense (3.7% → 2.9%) `[D03-S14]` |
| Recall is fine; answers still miss | Chunks too small to answer from, or no reranking | What was actually placed in context | Parent-document retrieval; add reranking (→1.9%) `[D03-S14]` |
| Wrong tool as the library grows | Past 30–50 tools; overlapping descriptions | Tool count in context; diff the candidates' descriptions | Consolidate, namespace, then tool search with `defer_loading` `[D03-S02]` |
| A deferred tool is never found | Name/description don't match how the task is phrased | Search covers names, descriptions, argument names and descriptions | Add task-phrased keywords; namespace by service `[D03-S02]` |
| Cache hit rate near zero on a long loop | Dynamic content above a breakpoint; tools or model changed mid-session; `effort` changed | `usage.cache_read_input_tokens` vs `input_tokens` | Freeze the prefix; use tool search or mid-conversation tool changes instead of rewriting `tools` `[D03-S31]`, `[D03-S33]` |
| Cost grew far faster than traffic | Turn count grew; history resent each turn | Turns per completed task; input/output split | Consolidate tools, PTC, caching — then effort, then tier `[D03-S33]` |
| Sporadic 429 with no `retry-after`; retries never succeed | Tier monthly spend cap, not a rate limit | `error.details.error_code == "enforced_spend_limit_reached"` | Raise the tier or limit; backing off will not clear it `[D03-S24]` |
| Intermittent 504 on long generations; or errors appearing *after* a 200 on a streamed request | Non-streaming with large `max_tokens`; mid-stream error event | Whether the call streams; whether you read stream error events, not just HTTP status | Stream, or move to Batch; handle mid-stream errors explicitly — they "don't follow these standard mechanisms" `[D03-S25]` |
| One tenant's data surfaces for another | Filter missing on a code path, or enforced in the prompt | Where the filter is applied and where its value comes from | Inject server-side from the session; add a test that fails when absent |
| Agent performs an action no user authorized | Injection via a tool result or document, plus an over-scoped identity | The tool's identity and scopes; whether tool results are treated as instruction | Remove the capability; narrow scopes; validate tool results `[D03-S06]`, `[D03-S10]` |
| A third-party server's tools changed mid-conversation | Server emitted `tools/list_changed` | Whether the tool list is pinned | Pin it; allowlist rather than denylist `[D03-S05]` |
| A user complaint ties to no trace | No `request-id` recorded; uniform sampling discarded the session | Whether `request-id` is a span attribute and sampling is session-keyed | Record it per span; head-sample by session; keep 100% of errors `[D03-S25]` |
| Telemetry bill rivals inference bill | Full content capture; high-cardinality span names | Span-name cardinality; content-capture flag | Structural spans at 100%, content on a gated sample `[D03-S21]` |

---

## 7. Anti-patterns

| Anti-pattern | The "looks-right" reasoning | Why it fails |
|---|---|---|
| **Log or confirm the dangerous tool instead of removing it** | "Keep the capability, gain evidence / a human approves." | Detective and compensating controls; the capability stays reachable and the harm still happens `[D03-S01]`. |
| **Token passthrough proxy** | "The MCP server is just plumbing." | Forbidden; breaks audience validation, audit on both sides, and downstream rate limiting `[D03-S06]`. |
| **Grant all scopes up front** | "Fewer consent dialogs." | "Consent abandonment," "privilege chaining," revocation that "disrupts all workflows" `[D03-S06]`. |
| **Authorization in the system prompt** | "The model is told not to cross tenants." | Not an enforcement point; one injected instruction ends it. |
| **Trusting tool annotations** | "`readOnlyHint: true`, so auto-approve." | Clients "**MUST** consider tool annotations to be untrusted unless they come from trusted servers" `[D03-S10]`. |
| **Sessions as authentication** | "The session ID proves who they are." | "MCP Servers **MUST NOT** use sessions for authentication" `[D03-S06]`. |
| **Load every tool** | "Availability beats efficiency." | ~55K tokens before work starts; degradation past 30–50 tools `[D03-S02]`, `[D03-S15]`. |
| **Vector-index everything, including tables and live state** | "One retrieval layer for all data." | Embeddings cannot aggregate; indexing live state manufactures staleness. |
| **RAG for a 50-page corpus** | "RAG is best practice." | Under ~200K tokens, stuff and cache `[D03-S14]`. |
| **Swapping the `tools` array each turn** | "Progressive disclosure, hand-rolled." | Invalidates the whole cache; supported mechanisms append `[D03-S02]`, `[D03-S31]`. |
| **Context editing as a cost lever** | "Clearing old tool results saves money." | Each pass rewrites the cached conversation; it "cost more than it saved" `[D03-S33]`. |
| **Streaming to fix cost or throughput** | "It feels faster, so it's cheaper." | Perceived latency only. |
| **Full prompt/completion capture in production** | "We'll want everything when debugging." | Content capture "SHOULD NOT" be default; a PII liability and a cost center `[D03-S21]`. |
| **MCP for a single in-house consumer** | "MCP is the modern standard." | You inherit a server, an OAuth resource server, `Origin` validation, sessions, and a hop — for zero reuse. |
| **Wrapping an autonomous agent as a stateless tool** | "Everything is a tool." | It "can't capture the agent's full capabilities" `[D03-S19]`. |

---

## 8. Exam-day heuristics

1. **Least privilege = remove the capability, not monitor it** `[D03-S01]`.
2. **Authorization lives server-side.** Any option enforcing a security rule in prompt text, or trusting a
   model-supplied tenant/user identifier, is wrong.
3. **Never forward a caller's token downstream.** Validate audience in; mint a new token out `[D03-S06]`.
4. **Confident-but-wrong after a data refresh = retrieval, not the model** `[D03-S01]`.
5. **Match mechanism to data shape.** Tabular → SQL. Graph → traversal. Live state → API call. Code → file search.
   Long prose → hybrid + rerank. Tiny corpus → stuff and cache `[D03-S14]`.
6. **Turn count beats model tier** for latency and cost; it grows roughly quadratically `[D03-S33]`.
7. **Streaming changes perception; batch changes cost (−50%); async removes the user from the wait** `[D03-S26]`.
8. **Free wins before trade-offs:** caching, prompt/tool hygiene, batch — then effort, then tier `[D03-S33]`.
9. **30–50 tools is the accuracy cliff; ~10K tokens of definitions is the tool-search threshold** `[D03-S02]`.
10. **Progressive disclosure must be cache-compatible.** Tool search and deferred tools append; rewriting `tools`
    invalidates `[D03-S02]`.
11. **Observability: structure at 100%, content by exception.** A complaint must resolve to a `request-id`
    `[D03-S21]`, `[D03-S25]`.
12. **MCP exposes tools to a model; A2A lets agents negotiate.** Reuse across clients justifies MCP `[D03-S19]`.
13. **When two options are both defensible, prefer the one that removes a failure mode over the one that detects
    it.**

---

## 9. Practice items

**1.** A claims agent exposes `search_claims`, `read_claim`, `draft_letter`, `approve_payment`, `delete_claim`. The
intake team it serves only searches, reads, and drafts. Applying least privilege, which change best reduces risk?
*(Select one.)* **A.** Audit-log the two write tools. **B.** Remove them from the intake agent's configuration.
**C.** Require supervisor confirmation before both. **D.** Set `defer_loading: true` on both.
**B.** Removal eliminates the capability. **A** is detective — the payment still executes. **C** is a compensating
control leaving the capability reachable. **D** is efficiency, not security: deferred tools leave context but stay
fully callable once discovered `[D03-S02]`.

**2.** A vendor's MCP server proxies a third-party CRM, passing the caller's bearer token straight through. Which
statement best describes the problem? *(Select one.)* **A.** Acceptable with TLS and a short-lived token.
**B.** The server must validate the token was issued for itself, and obtain a separate token for the CRM.
**C.** Acceptable if every forwarded call is logged. **D.** Acceptable because the CRM validates it independently.
**B.** "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server"; the upstream
token "is a separate token, issued by the upstream authorization server" `[D03-S06]`, `[D03-S07]`. **A** addresses
transport, not audience. **C** is the anti-pattern plus a log line — passthrough is what destroys audit fidelity.
**D** is the confused-deputy setup: the CRM may assume you validated it.

**3.** A RAG assistant over 80,000 engineering documents starts answering confidently and incorrectly the morning
after a scheduled corpus refresh. Latency, model version, and prompt are unchanged. Most likely first place to
investigate? *(Select one.)* **A.** Sampling temperature. **B.** The retrieval and indexing step. **C.** Context
window size. **D.** System-prompt guardrails.
**B.** A refresh can only affect the data plane: incomplete re-index, un-tombstoned deletions, or a changed
embedding model mixing vector spaces `[D03-S01]`, `[D03-S14]`. **A**, **C**, and **D** were untouched by the refresh
and cannot be triggered by it.

**4.** An operations agent aggregates seven MCP servers totaling ~210 tools. Definitions cost tens of thousands of
tokens and the agent increasingly picks the wrong tool. Which two changes address both the context cost and the
selection accuracy? *(Select two.)* **A.** Enable tool search and set `defer_loading: true` on all but the 3–5
most-used tools. **B.** Consolidate near-duplicate tools and namespace names by service. **C.** Shorten every
description to one sentence. **D.** Switch to a lower-latency tier. **E.** Increase `max_tokens`.
**A and B.** Tool search cuts context by over 85% while preserving the cache and raised MCP-eval accuracy 79.5% →
88.1% `[D03-S02]`, `[D03-S15]`; consolidation and namespacing reduce ambiguity `[D03-S04]`, `[D03-S18]`. **C** is
counterproductive — search matches names, descriptions, and argument descriptions, and description quality is "by
far the most important factor in tool performance" `[D03-S04]`. **D** trades on the wrong axis. **E** affects
neither input context nor selection.

**5.** A shared-index RAG service for 3,500 tenants leaks a snippet across tenants. The system prompt already says to
use only the current tenant's documents. Which change best fixes the isolation gap? *(Select one.)* **A.** Strengthen
the prompt and add a refusal example. **B.** Apply the tenant filter inside the retrieval service before the query
runs, sourced from the authenticated session. **C.** Provision a separate index per tenant this quarter.
**D.** Filter foreign snippets out of the model's answer.
**B.** Authorization must be enforced by code the model cannot influence. **A** is prompt-side enforcement of a
server-side invariant. **C** is defensible for a few contractually isolated tenants but disproportionate at 3,500,
and leaves the leak live for a quarter. **D** still admits foreign data into context, where it can be paraphrased
before filtering.

**6.** A field-service assistant averages nine agent turns and misses a 6-second p95 SLA at 13 seconds. Accuracy is
acceptable. Which change most directly reduces p95 without spending accuracy? *(Select one.)* **A.** Enable
streaming. **B.** Collapse three chained dependent tool calls into one programmatic tool call and parallelize
independent reads. **C.** Drop to the smallest tier. **D.** Reduce `max_tokens`.
**B.** Turn count is the dominant term; programmatic tool calling removes inference passes and cut tokens 37%
`[D03-S15]`, and cost and latency scale with roughly the square of turn count `[D03-S33]`. **A** improves *perceived*
latency only. **C** spends accuracy the stem says you have. **D** truncates output; hitting the cap is a failed
attempt, not a speedup `[D03-S33]`.

**7.** Which mechanism best fits "total claims payout by region for Q2, excluding reversals" over a 40-million-row
relational table? *(Select one.)* **A.** Dense vector search over row-level chunks, top-k 50. **B.** Parameterized
SQL behind a narrow tool, with large result sets aggregated in code before entering context. **C.** Hybrid dense +
BM25 with reranking over serialized rows. **D.** Full-context stuffing of the quarter's rows.
**B.** An aggregation with an exclusion predicate is a structured query, and filtering before context keeps
intermediates out of the window `[D03-S15]`, `[D03-S16]`. **A** and **C** cannot compute sums and lose join
semantics once rows are chunked. **D** exceeds any context window and still leaves arithmetic to the model.

**8.** A knowledge base is 140,000 tokens of stable policy text, queried thousands of times a day with paraphrased
questions. Most appropriate design? *(Select one.)* **A.** Chunk, embed, retrieve top-10 with reranking. **B.** Place
the full corpus ahead of the varying question and enable prompt caching. **C.** Build and traverse a knowledge
graph. **D.** Fine-tune on the policy text.
**B.** Below roughly 200,000 tokens (~500 pages), use the whole knowledge base directly rather than build a pipeline
`[D03-S14]`; caching makes the repeated prefix cheap, cuts TTFT, and cached input doesn't count toward ITPM on most
models `[D03-S24]`. **A** adds failure modes without recall. **C** is for multi-hop relationship queries. **D** is
the most expensive way to handle text that changes.

**9.** Which three practices make a high-volume agent platform debuggable without creating a PII liability or a
telemetry cost problem? *(Select three.)* **A.** A span per model call and per tool call, with token counts and
computed cost as attributes. **B.** Full prompt and completion capture on every request by default. **C.** Record
the provider `request-id` on spans. **D.** Gate content capture behind explicit opt-in and keep 100% of errors while
sampling the rest. **E.** Put the response identifier in the span name.
**A, C, and D.** The conventions define per-call and `execute_tool` spans and recommend usage-token attributes
`[D03-S21]`; `request-id` is the platform correlation handle `[D03-S25]`; content "SHOULD NOT" be captured by
default, with capture "gated by an explicit user opt-in" `[D03-S21]`. **B** is the PII-and-cost anti-pattern.
**E** creates unbounded span-name cardinality — the conventions omit a response ID from a span name for that exact
reason `[D03-S21]`.

**10.** An internal capability must be callable by three Claude-based applications plus an interactive developer
tool, each on its own release cycle, and its operations will change monthly. Which mechanism is most appropriate?
*(Select one.)* **A.** A direct SDK call embedded in each application. **B.** A remote MCP server over Streamable
HTTP, with OAuth and tool-list pinning per consumer. **C.** A CLI binary each application shells out to.
**D.** An agent-to-agent endpoint.
**B.** Reuse across several clients, runtime discovery, and independent release cadence is MCP's case; pinning
protects consumers from mid-conversation tool changes `[D03-S05]`, `[D03-S09]`. **A** duplicates the integration four
times and couples every release. **C** gives the harness only an opaque command string, making gating and auditing
hard, and shell-invoked input is untrusted model output `[D03-S31]`. **D** is for autonomous counterpart agents, not
a stateless capability `[D03-S19]`.

**11.** A dense-only RAG pipeline misses documents when users search by exact error codes and clause numbers;
top-20 failures sit around 5–6%. Query-time latency has almost no headroom. Which two changes give the largest
accuracy gain for the least query-time latency? *(Select two.)* **A.** Contextual enrichment of each chunk before
embedding. **B.** A lexical BM25 index over the same contextualized chunks, fused with dense results.
**C.** Reranking over the top 150 candidates. **D.** Increase top-k from 20 to 100. **E.** A higher model tier.
**A and B.** Both are index-side: contextual embeddings alone cut top-20 failures 35% (5.7% → 3.7%), and adding
contextual BM25 reaches 49% (→2.9%), with no query-time model hop; BM25 recovers exact-token matches `[D03-S14]`.
**C** gives the largest additional gain (→1.9%) but adds a query-time hop the budget cannot absorb. **D** raises
latency and cost and invites context rot `[D03-S17]`. **E** does not change what is retrieved.

**12.** A regulated client requires that no data exchanged with third-party tool servers be retained by the model
provider, and needs MCP resources and prompts as well as tools, including one server that runs locally. Which
approach is correct? *(Select one.)* **A.** The Messages API MCP connector with `mcp_servers`, adding the local
server by URL. **B.** Run your own MCP client — stdio to the local server, Streamable HTTP to the remote ones — and
integrate its tools through your own tool definitions. **C.** Use the connector and disable retention in the toolset
configuration. **D.** Expose the local server over public HTTPS so the connector can reach it.
**B.** The connector supports only tool calls, requires a publicly exposed HTTPS server, cannot reach local stdio
servers, and is not ZDR-eligible; your own client is the documented path when you need local servers, prompts, or
resources `[D03-S05]`. **A** fails on both the local server and the feature set. **C** invents a configuration
option — retention eligibility is a feature property, not a toolset flag `[D03-S05]`. **D** exposes a local server
with environment-sourced credentials to the internet, the opposite of guidance favoring stdio "to limit access to
just the MCP client" `[D03-S06]`.

---

## 10. Objective coverage

| Objective | Where covered |
|---|---|
| 1. Capability bloat | §3.1, §3.2, §4.1, §4.2, §4.10; S1, S3; items 1, 4; heuristics 1, 9, 10 |
| 2. AuthN/AuthZ security gaps | §3.3–§3.5, §4.3, §4.4; S4, S5; items 2, 5, 12; anti-patterns 1–6; heuristics 2, 3 |
| 3. Accuracy–latency trade-offs | §4.5; S6, S8; items 6, 8, 11; heuristics 6, 7, 8 |
| 4. Observability at scale | §3.8, §4.8, §6; item 9; heuristic 11 |
| 5. RAG pipeline, chunking and indexing | §3.6, §3.7, §4.9; S2, S7; items 3, 11; §6 rows 1–3 |
| 6. Retrieval strategy by data shape and query pattern | §4.6; S7; items 7, 8; heuristic 5 |
| 7. Connection protocol selection | §3.9, §4.7; S3, S4; items 10, 12; heuristic 12 |
| 8. Progressive discovery vs. monolithic context | §3.2, §4.2, §4.10; S3; items 1, 4; heuristics 9, 10 |

---

## 11. Sources

Full table with URLs, publishers, types, trust levels, and access dates: `research/03-integration-sources.md`.

`[D03-S01]` CCAR-P Exam Guide v1.0 · `[D03-S02]` Tool search tool · `[D03-S03]` Tool use overview · `[D03-S04]`
Define tools · `[D03-S05]` MCP connector · `[D03-S06]` MCP spec, Security Best Practices · `[D03-S07]` MCP spec,
Authorization (2025-06-18) · `[D03-S08]` MCP spec, Authorization (2026-07-28) · `[D03-S09]` MCP spec, Transports ·
`[D03-S10]` MCP spec, Tools · `[D03-S11]` MCP spec, Elicitation · `[D03-S12]` MCP spec, Sampling · `[D03-S13]` MCP
spec, Versioning · `[D03-S14]` Anthropic, "Introducing Contextual Retrieval" · `[D03-S15]` Anthropic Engineering,
"Advanced tool use" · `[D03-S16]` Anthropic Engineering, "Code execution with MCP" · `[D03-S17]` Anthropic
Engineering, "Effective context engineering for AI agents" · `[D03-S18]` Anthropic Engineering, "Writing tools for
agents" · `[D03-S19]` A2A Protocol, "What is A2A" · `[D03-S21]`–`[D03-S22]` OpenTelemetry GenAI semantic
conventions (spans, agent spans) · `[D03-S23]` RFC 9700, OAuth 2.0 Security BCP · `[D03-S24]` Rate limits ·
`[D03-S25]` API errors · `[D03-S26]` Batch processing · `[D03-S27]` Search results · `[D03-S28]` Citations ·
`[D03-S29]` Models overview · `[D03-S30]` Claude Agent SDK overview · `[D03-S31]`–`[D03-S33]` `claude-api` skill
reference files (tool-use concepts, agent design, cost optimization) · `[D03-S40]` practitioner LLM-observability
sources (**secondary**). `[D03-S02]`–`[D03-S05]` and `[D03-S24]`–`[D03-S30]` are Anthropic platform documentation.

### Remaining `[UNVERIFIED]` claims

1. **Request-level idempotency keys on the Messages API** — `[UNVERIFIED]`. Not documented in `[D03-S25]`; the
   documented correlation handle is the `request-id` header / `request_id` error field. The architectural point
   stands independently: make retried side-effecting *tool* calls idempotent in your own handlers.
2. **Sampling percentages in §4.8** come from `[D03-S40]`, aggregated practitioner sources, and are labeled
   practitioner guidance — not Anthropic or OpenTelemetry guidance. The normative parts (per-tool-call spans, usage
   attributes, opt-in content capture, cardinality avoidance) are from `[D03-S21]`/`[D03-S22]`.
3. **Chunk-size numbers** — deliberately absent. No source prescribes one; `[D03-S14]` recommends experimentation,
   and its 800-token figure appears only inside a cost example. §4.9 names chunking *strategies*, not sizes.
