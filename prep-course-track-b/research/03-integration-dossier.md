# Domain 3 — Integration (19%) — Research Dossier

Researcher: Domain 3. Compiled 2026-09-24. All source IDs resolve in `research/03-integration-sources.md`.
Weight 19% of 63 items ≈ **12 items** (19% × 63 = 11.97). Heaviest domain on the exam.

Objectives (verbatim, `[D03-S01]` §6):
1. Evaluate tool/agent configuration for capability bloat
2. Analyze authentication and authorization requirements to identify security gaps
3. Evaluate accuracy-latency trade-offs and justify configuration decisions
4. Analyze observability challenges and select monitoring strategies at scale
5. Design a RAG pipeline with appropriate chunking and indexing strategies
6. Apply retrieval strategies matched to data shape and query pattern
7. Evaluate connection protocols and select the appropriate integration mechanism (MCP, API/CLI, agent-to-agent)
8. Evaluate progressive discovery vs. monolithic context strategy

---

## 0. CRITICAL CONTRADICTION — model lineup vs. AGENT-BRIEF

`AGENT-BRIEF.md` §0 states the current lineup is "Claude 5 family (Opus 5, Sonnet 5, Fable 5.1) and Haiku 4.5."
**Primary docs fetched 2026-09-24 `[D03-S29]` disagree.** Verified current lineup:

| Model | API ID | Context | Max output | Input $/MTok | Output $/MTok | Default effort |
|---|---|---|---|---|---|---|
| Claude Fable 5.1 | `claude-fable-5-1` | 1M | 128K | $10 | $50 | `high` |
| Claude Opus 5.5 | `claude-opus-5-5` | 1M | 128K | $4 | $20 | `medium` |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 128K | $2 | $10 | `high` |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | 64K | $1 | $5 | n/a (extended thinking) |

`[D03-S29]` lists **Claude Opus 5 as legacy** ("still available"), alongside Fable 5, Opus 4.8/4.7/4.6/4.5, Sonnet 4.6/4.5.
Docs recommend "start with Claude Opus 5.5 for most workloads." Batch = 50% off; cache reads = 10% of base input
price (2.5% on Fable 5.1 / Mythos 5.1, 5% on Opus 5.5) `[D03-S29]`.

**Resolution used in the draft:** the chapter is written in **tier language** (Opus-tier / Sonnet-tier / Haiku-tier)
so it does not rot, with one dated footnote carrying the verified lineup above. Editors should not "correct" the
draft back to the brief's list without re-verifying. Flag for the consolidation session.

Other verified version facts that will surprise readers:
- **MCP current protocol revision is `2026-07-28`** `[D03-S13]`, not 2025-06-18 or 2025-11-25. Versioning is
  `YYYY-MM-DD`, incremented only on backwards-incompatible change. Negotiation moved to a per-request
  `io.modelcontextprotocol/protocolVersion` `_meta` key plus the `MCP-Protocol-Version` header on Streamable HTTP;
  a new mandatory `server/discover` RPC returns supported versions/capabilities in one call.
- In MCP `2026-07-28`, **Dynamic Client Registration (RFC 7591) is deprecated**, superseded by
  **OAuth Client ID Metadata Documents** (URL-as-`client_id`) `[D03-S08]`. RFC 9207 `iss` validation is now
  normative for clients. This matters because the classic confused-deputy write-up is framed around DCR.
- Forced tool use (`tool_choice` `any`/`tool`) returns **400** on Claude Opus 5.5, Fable 5.1, Mythos 5.1 `[D03-S04]`.
  Substitutes: `auto` + prompt instruction, `strict: true`, or structured outputs.

---

## 1. Objective 1 — Capability bloat

### 1.1 Measured facts (all primary)

| Fact | Value | Source |
|---|---|---|
| Tool-selection accuracy degrades once available tools exceed | **30–50 tools** | `[D03-S02]` |
| Typical 5-server MCP setup (GitHub, Slack, Sentry, Grafana, Splunk) = 58 tools | **~55K tokens** in definitions before any work | `[D03-S02]`, `[D03-S15]` |
| Tool search typical context reduction | **over 85%**; loads only the 3–5 tools needed | `[D03-S02]` |
| Blog variant of the same measurement | ~77K → ~8.7K tokens, "preserving 95% of context window" | `[D03-S15]` |
| Tool search on MCP evaluations, Opus 4 | **49% → 74%** | `[D03-S15]` |
| Tool search on MCP evaluations, Opus 4.5 | **79.5% → 88.1%** | `[D03-S15]` |
| Programmatic tool calling, complex research tasks | **43,588 → 27,297 tokens (37% reduction)** | `[D03-S15]` |
| PTC accuracy, internal knowledge retrieval | 25.6% → 28.5% | `[D03-S15]` |
| PTC accuracy, GIA benchmark | 46.5% → 51.2% | `[D03-S15]` |
| Tool use examples (`input_examples`) on complex parameter handling | **72% → 90%** | `[D03-S15]` |
| Code-execution-with-MCP (filesystem tool discovery) | **150,000 → 2,000 tokens, 98.7% saving** | `[D03-S16]` |
| Tool-use system prompt overhead (Opus 5.5, `auto`/`none`) | 286 tokens | `[D03-S03]` |
| Tool-use system prompt overhead (Opus 5: `auto`/`none` vs `any`/`tool`) | 286 vs 406 tokens | `[D03-S03]` |
| `input_examples` token cost | ~20–50 simple, ~100–200 complex nested | `[D03-S04]` |
| Max deferred tools per request | 10,000 | `[D03-S02]` |
| Tool search default results per search | 5 (Claude may set `limit` 1–10,000) | `[D03-S02]` |

**CONTRADICTION (minor, surfaced not smoothed):** `[D03-S02]` says a 5-server setup consumes "~55k tokens" and
that tool search reduces "by over 85 percent"; `[D03-S15]` reports "~77K tokens" → "~8.7K" for what appears to be
the same class of setup, and also states "85% reduction." The 55K figure is the sum of the itemized per-server
numbers in `[D03-S15]` (26K+21K+3K+3K+2K = 55K), so 77K likely includes a system prompt and non-MCP tools. Draft
uses **~55K for 58 tools across 5 servers** and **"over 85% reduction"** as the defensible pair.

### 1.2 Precise definitions

- **Capability bloat** — a tool/agent configuration exposing capabilities the agent's role does not require. Two
  distinct costs: (a) *token overhead* (schemas render into the cached prefix on every request `[D03-S03]`), and
  (b) *selection degradation* (accuracy falls past 30–50 tools `[D03-S02]`). Least privilege addresses a third,
  independent cost: *blast radius*.
- **Least privilege (exam sense)** — remove the capability from the configuration. `[D03-S01]` Sample 1 answer key:
  "Least privilege means removing capabilities the role does not require, eliminating the attack surface rather
  than monitoring or guarding it. Logging (A) and confirmations (C) are detective/compensating controls, not
  removal of unnecessary privilege; model size (D) is unrelated to authorization scope."
- **`defer_loading: true`** — controls what enters the *context window*, not what you send. You still send every
  definition in `tools` on every request; the API excludes deferred tools from the system-prompt prefix and appends
  a `tool_reference` inline when discovered, so **prompt caching is preserved** `[D03-S02]`. At least one tool must
  be non-deferred or 400 `At least one tool must have defer_loading=false`. A deferred tool cannot also carry
  `cache_control` (400). Strict-mode grammar builds from the full toolset, so `defer_loading` + `strict` compose
  without grammar recompilation `[D03-S02]`.
- **MCP allowlist mode** — `default_config: {enabled: false}` on the `mcp_toolset` entry plus per-tool
  `configs: {tool: {enabled: true}}`. Precedence: per-tool `configs` > set-level `default_config` > system defaults
  `[D03-S05]`. This is *removal*, enforced server-side by the API, not a prompt instruction.
- **Tool-list pinning** — beta `mcp-client-2026-09-15` records the tool list a server returns and lets you pin it,
  "so a server that changes its tools doesn't change what Claude sees partway through a conversation" `[D03-S05]`.
  This is the control against tool-set drift / rug-pull from a third-party server.

### 1.3 Design guidance (primary)

- "Consolidate related operations into fewer tools. Rather than creating a separate tool for every action
  (`create_pr`, `review_pr`, `merge_pr`), group them into a single tool with an `action` parameter" `[D03-S04]`.
- "Use meaningful namespacing in tool names… prefix names with the service (for example, `github_list_prs`)…
  especially important when using tool search" `[D03-S04]`, `[D03-S18]` (`asana_search` vs `jira_search`,
  `asana_projects_search`).
- "More tools don't always lead to better outcomes" — build "a few thoughtful tools targeting specific high-impact
  workflows" rather than wrapping every API endpoint `[D03-S18]`.
- "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be
  expected to do better" `[D03-S17]`.
- Descriptions: "Aim for at least 3–4 sentences for each tool description, more if the tool is complex"
  `[D03-S04]`. "Even small refinements to tool descriptions can yield dramatic improvements" `[D03-S18]`.
- Bash vs dedicated tool: bash gives breadth but hands the harness "only an opaque command string, the same shape
  for every action." Promote to a dedicated tool when you need to **gate, render, audit, or parallelize**
  `[D03-S32]`. Reversibility is the criterion for gating.
- Tool search **when**: ≥10 tools, definitions >10K tokens, selection accuracy dropping, aggregating multiple MCP
  servers (200+ tools), library growing. **Not when**: <10 tools, every tool used every request, definitions <100
  tokens total `[D03-S02]`.

---

## 2. Objective 2 — AuthN/AuthZ gaps

### 2.1 MCP spec normative quotes (verbatim — use these in the chapter)

Token passthrough `[D03-S06]`:
> "'Token passthrough' is an anti-pattern where an MCP server accepts tokens from an MCP client without validating
> that the tokens were properly issued *to the MCP server* and passes them through to the downstream API."
> … "MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server."

Audience binding `[D03-S07]`, `[D03-S08]`:
> "MCP servers **MUST** validate that access tokens were issued specifically for them as the intended audience,
> according to RFC 8707 Section 2." … "MCP servers **MUST** only accept tokens that are valid for use with their
> own resources. MCP servers **MUST NOT** accept or transit any other tokens."

Separate upstream token `[D03-S07]`:
> "If the MCP server makes requests to upstream APIs, it may act as an OAuth client to them. The access token used
> at the upstream API is a separate token, issued by the upstream authorization server. The MCP server **MUST NOT**
> pass through the token it received from the MCP client."

Resource indicators `[D03-S07]`, `[D03-S08]`:
> "MCP clients **MUST** implement Resource Indicators for OAuth 2.0 as defined in RFC 8707… **MUST** be included in
> both authorization requests and token requests… **MUST** identify the MCP server that the client intends to use
> the token with… MCP clients **MUST** send this parameter regardless of whether authorization servers support it."

Confused deputy `[D03-S06]`: vulnerable when **all four** hold — static client ID at the third-party AS; MCP clients
may dynamically register (each getting its own `client_id`); the third-party AS sets a consent cookie after first
authorization; the proxy does not implement per-client consent before forwarding. Mitigation: proxy **MUST**
maintain a per-user registry of approved `client_id` values and check it **before** initiating the third-party
flow; consent page MUST name the client, show requested third-party scopes and the registered `redirect_uri`, have
CSRF protection, and be un-iframeable; `redirect_uri` validated by **exact string matching (not pattern matching or
wildcards)**; `state` generated cryptographically, stored server-side **only after** consent approval, single-use,
short expiry (e.g. 10 minutes). "The consent cookie or session containing the `state` value **MUST NOT** be set
until **after** the user has approved the consent screen."

Session hijacking `[D03-S06]`:
> "MCP servers that implement authorization **MUST** verify all inbound requests. MCP Servers **MUST NOT** use
> sessions for authentication." … "MCP servers **MUST** use secure, non-deterministic session IDs." … "MCP servers
> **SHOULD** bind session IDs to user-specific information… Use a key format like `<user_id>:<session_id>`. This
> ensures that even if an attacker guesses a session ID, they cannot impersonate another user as the user ID is
> derived from the user token and not provided by the client."

Scope minimization `[D03-S06]`: broad scopes (`files:*`, `db:*`, `admin:*`) → "Expanded blast radius… Higher
friction on revocation… Audit noise… Privilege chaining… Consent abandonment… Scope inflation blindness."
Mitigation: "Minimal initial scope set (e.g., `mcp:tools-basic`) containing only low-risk discovery/read
operations; Incremental elevation via targeted `WWW-Authenticate` `scope="..."` challenges when privileged
operations are first attempted; Down-scoping tolerance." Common mistakes include "Publishing all possible scopes in
`scopes_supported`", "Using wildcard or omnibus scopes (`*`, `all`, `full-access`)", and — the one exam writers
love — **"Treating claimed scopes in token as sufficient without server-side authorization logic."**

Tool-description / tool-result trust `[D03-S10]`:
> "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted unless they come
> from trusted servers." (annotations = `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)

Server/client security duties `[D03-S10]`: servers **MUST** validate all tool inputs, implement proper access
controls, rate limit tool invocations, sanitize tool outputs. Clients **SHOULD** prompt for user confirmation on
sensitive operations, **"Show tool inputs to the user before calling the server, to avoid malicious or accidental
data exfiltration"**, **"Validate tool results before passing to LLM"**, implement timeouts, log tool usage for
audit. Plus: "For trust & safety and security, there **SHOULD** always be a human in the loop with the ability to
deny tool invocations."

SSRF via OAuth metadata discovery `[D03-S06]`: a malicious MCP server can put internal URLs in the
`WWW-Authenticate` `resource_metadata`, in `authorization_servers`, or in AS metadata endpoints — targeting
`169.254.169.254` (cloud metadata → IAM credentials), `localhost:6379`, private ranges, DNS rebinding, redirect
chains. Clients **SHOULD** require HTTPS, block private/reserved ranges (10/8, 172.16/12, 192.168/16, 127/8,
169.254/16, fc00::/7, fe80::/10), validate redirect targets, use egress proxies, and beware TOCTOU DNS.
"Avoid implementing IP validation manually."

Elicitation `[D03-S11]`: servers **MUST NOT** use *form mode* to request "passwords, API keys, access tokens, or
payment credentials"; **MUST** use *URL mode* for those. Third-party credentials **MUST NOT** transit the MCP
client; the server **MUST NOT** use the client's credentials for the third-party service (that is token
passthrough); state **MUST NOT** be associated with session IDs alone; user identity **MUST** derive from
authorization credentials (e.g. `sub` claim), not from client-supplied claims — "Incorrect: Treat user input like
'I am joe@example.com' as authoritative."

Sampling `[D03-S12]`: inverts the trust direction — the *server* asks the *client's* model to generate.
"there **SHOULD** always be a human in the loop with the ability to deny sampling requests"; clients SHOULD
rate-limit and allow prompt review/edit before send.

### 2.2 OAuth 2.0 Security BCP (RFC 9700) points that map onto agents `[D03-S23]`

- Public clients **MUST** implement PKCE; AS **MUST** support and enforce `code_verifier`, and reject token
  requests carrying `code_verifier` when no `code_challenge` was in the authorization request (downgrade defense).
- Implicit grant and token-in-authorization-response are **deprecated**; use the code flow.
- Resource owner password credentials grant **MUST NOT** be used.
- Redirect URIs: **exact string matching** except for localhost port numbers in native apps.
- Access tokens **SHOULD** be audience-restricted to a specific resource server (RFC 9068 `aud`, or RFC 8707
  `resource`), and scope-restricted to specific resources and actions.
- Public-client refresh tokens **MUST** be sender-constrained or rotated.
- Sender-constraining (mTLS RFC 8705, DPoP RFC 9449) **SHOULD** be used to "prevent misuse of stolen and leaked
  access tokens."
- Multi-AS clients **MUST** prevent mix-up attacks via `iss` (RFC 9207) or per-AS redirect URIs.

### 2.3 Anthropic-platform auth surface (verified)

- **MCP connector `authorization_token`**: "API consumers are expected to handle the OAuth flow and obtain the
  access token prior to making the API call, and to refresh the token as needed" `[D03-S05]`. So the *token
  lifecycle is the integrator's problem*, and a token placed there is scoped per request — not per end user unless
  the caller makes it so.
- **MCP connector is not ZDR-eligible**: "Data exchanged with MCP servers, including tool definitions and execution
  results, is retained according to Anthropic's standard data retention policy" `[D03-S05]`. This is a governance
  gap that appears in regulated-industry scenarios.
- **MCP connector supports only tool calls** — not resources, prompts, sampling, or elicitation; the server must be
  publicly exposed over HTTPS (Streamable HTTP or SSE); "Local STDIO servers cannot be connected directly"
  `[D03-S05]`.
- Bash tool: "commands are untrusted model output… apply an **allowlist** of permitted executables and reject shell
  operators (`&&`, `|`, `;`, backtick, `$()`)… A blocklist is not sufficient" `[D03-S31]`.
- Text editor tool: "`path` is untrusted model output. Confine every file operation to a fixed project root"
  (canonicalize then verify containment; reject `..`, symlinks, `%2e%2e%2f`) `[D03-S31]`.
- Memory tool: "Never store API keys, passwords, tokens… The reference implementations have no built-in access
  control; in multi-user systems, implement per-user memory directories and authentication in your tool handlers"
  `[D03-S31]`.

### 2.4 Multi-tenant retrieval isolation — raw matrix

| Approach | Isolation strength | Cost / ops | Cross-tenant query | Failure mode | Choose when |
|---|---|---|---|---|---|
| Index per tenant | Strongest (physical) | Highest (N indexes, N refresh jobs, poor small-tenant economics) | Impossible without fan-out | Tenant count explosion; per-tenant staleness drift | Few, large, contractually isolated tenants; regulated (HIPAA/FedRAMP) |
| Shared index + mandatory tenant filter applied server-side at query time | Strong *if* the filter cannot be bypassed | Lowest | Easy | A code path that forgets the filter leaks everything; filter must be injected by the retrieval service, never accepted from the model or the prompt | Many tenants, uniform schema, strong service-side enforcement |
| Shared index + per-document ACL list, filtered at query time against the caller's groups | Strong, fine-grained | Medium; ACL sync lag is the risk | Easy | Permission changes at the source not reflected until re-index → "revoked user still gets the doc" | Document management systems with per-item ACLs |
| Retrieve candidate IDs from index, then authorize each hit against the system of record before returning text | Strongest logical guarantee; no stale ACLs | Extra round trip per hit → latency | Easy | Latency and load on the system of record | Highly sensitive corpora where stale ACLs are unacceptable |
| Trust the model / prompt to filter | None | None | n/a | Prompt injection defeats it; not a control | Never |

Anchor: authorization must be enforced **server side, at query time, by code the model cannot influence**. The
model's prompt is not an enforcement point. Corollary from `[D03-S06]` scope minimization: "Treating claimed scopes
in token as sufficient without server-side authorization logic" is itself listed as a common mistake.

---

## 3. Objective 3 — Accuracy / latency / cost

### 3.1 Knob inventory (verified)

| Knob | Accuracy | Latency | Cost | Notes / source |
|---|---|---|---|---|
| Model tier | ↑ with tier | ↑ with tier (Fable slowest → Haiku fastest) | ↑ with tier | `[D03-S29]` comparative-latency row |
| `output_config.effort` (`low`→`max`) | ↑ | ↑ | ↑ | Lower effort → "fewer and more-consolidated tool calls, less preamble, terser confirmations" `[D03-S32]`. Default effort is per-model (`medium` on Opus 5.5, `high` on Sonnet 5 / Fable 5.1) `[D03-S29]` |
| Adaptive thinking on/off | ↑ when on | ↑ when on | ↑ when on | Disabling on some models causes tool calls to leak into visible text — prefer low effort over disabling `[D03-S31]` |
| Retrieval depth (top-k) | ↑ then plateaus/degrades (context rot) | ↑ | ↑ | Contextual Retrieval measured at **top-20** `[D03-S14]`; context rot argument `[D03-S17]` |
| Reranking | Large ↑ (67% vs 49% failure reduction) | + one rerank hop | + rerank spend | `[D03-S14]` |
| Hybrid (dense + BM25) vs dense-only | ↑ (35% → 49% failure reduction) | + second retrieval path + fusion | + index cost | `[D03-S14]` |
| Number of agent turns | ↑ to a point | Linear ↑ | Superlinear ↑ (each turn resends history) | "a 40-turn task sends its first turn 40 times and task cost grows with roughly the square of turn count" `[D03-S33]` |
| Parallel tool calls (default on) | neutral | ↓ wall clock | neutral | Return **all** `tool_result` blocks in a single user message; splitting them "silently trains Claude to stop making parallel calls" `[D03-S31]` |
| Programmatic tool calling | ↑ (25.6→28.5; 46.5→51.2) | ↓ ("eliminating 19+ inference passes when orchestrating 20+ tool calls") | ↓ 37% tokens | `[D03-S15]` |
| Streaming | neutral | ↓ *perceived* only; total unchanged | neutral | Required for large `max_tokens`; 504 `timeout_error` guidance `[D03-S25]` |
| Prompt caching | neutral | ↓ TTFT | ↓ 2.5–3.7× on agent loops at 81–90% hit rates | `[D03-S33]`; cache reads at 10% of input (5% Opus 5.5, 2.5% Fable 5.1) `[D03-S29]` |
| Cache reads and rate limits | — | — | Raises effective throughput | "only uncached input tokens count toward your ITPM rate limits" for most models; 2M ITPM at 80% hit rate ≈ 10M total input tokens/min `[D03-S24]` |
| Batch API | neutral | Hours (most <1h; 24h expiry) | **−50%** | 100,000 requests or 256 MB per batch; results retained 29 days; `max_tokens: 0` not allowed in batch `[D03-S26]` |
| `max_tokens` | Truncation = failed attempt | — | — | "a backstop, not a tuning knob"; a 16,384 cap ended 15% of Opus 5's coding attempts, "none of them solved" `[D03-S33]` |
| Context editing | Can *hurt* cost | — | Often ↑ | "in the run measured for the platform docs, context editing cost more than it saved" — it is a context-window tool, not a savings lever `[D03-S33]` |
| Compaction | neutral | — | ↓ 38% on a long triage run where it fired once | `[D03-S33]` |
| Subagents on a cheaper model | depends | ↓ if parallel | ↓ | Caches are per-model, so a cascade forfeits cross-model cache reuse `[D03-S33]` |

### 3.2 SLA justification skeleton (derived, for the chapter)

p95 end-to-end = (network + queue) + Σ per-turn (TTFT + generation) + Σ tool latency + retrieval latency.
Levers that change the *number* of terms (turn count, PTC, parallel calls) dominate levers that change each term
(model tier, effort). Streaming moves the *perceived* start of the first term to near zero but changes no term.
Async + callback removes the user from the sum entirely; batch removes the SLA.

Retry/idempotency facts `[D03-S25]`: retryable = 408/409/429/5xx + connection errors; SDKs retry twice by default
with exponential backoff, honoring `retry-after`. **Timeouts are retried, so wall-clock can reach
`timeout × (max_retries + 1)`** `[D03-S31]`. A 429 from the **tier spend cap** has **no `retry-after`** and keeps
failing until access resumes — distinguish it by `error.details.error_code == "enforced_spend_limit_reached"`
`[D03-S24]`. Mid-stream errors arrive **after** a 200 and do not follow the standard mechanism `[D03-S25]`.
There is no documented request-level idempotency key on the Messages API → **[UNVERIFIED]** for "idempotency key";
the documented correlation handle is the `request-id` response header / `request_id` error field `[D03-S25]`.

---

## 4. Objective 4 — Observability at scale

### 4.1 OpenTelemetry GenAI semantic conventions (primary)

- Conventions have **moved** to the `open-telemetry/semantic-conventions-genai` repository `[D03-S20]`.
- Span naming: `{gen_ai.operation.name} {gen_ai.request.model}` for inference and embeddings;
  `{gen_ai.operation.name} {gen_ai.data_source.id}` for retrievals; bare `{gen_ai.operation.name}` for
  fetch-response (response ID omitted **because of high cardinality**) and memory `[D03-S21]`.
- Span kind: `CLIENT` typically; inference **MAY** be `INTERNAL` for in-process models `[D03-S21]`.
- **Required**: `gen_ai.operation.name`, `gen_ai.provider.name`. **Conditionally required**: `gen_ai.request.model`
  (when available), `error.type` (if the operation failed) `[D03-S21]`.
- **Recommended**: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.model`,
  `gen_ai.conversation.id`, `gen_ai.response.finish_reasons` `[D03-S21]`.
- Tool execution: `gen_ai.operation.name = execute_tool`, with tool name, call ID, type, description `[D03-S21]`,
  `[D03-S22]`.
- Agent spans `[D03-S22]`: `create_agent`, `invoke_agent` (`CLIENT` for a remote agent service, `INTERNAL` for
  in-process), `invoke_workflow` (`INTERNAL`, for the orchestrator — "should be reported for graph/orchestrator
  operations but not for internal implementation details"), and `plan` (the LLM call that produces the plan is a
  **child** of `plan`; the resulting tool executions are **siblings** under the parent `invoke_agent`).
  `gen_ai.agent.id/name/description/version` "should be recorded at span creation time **for sampling decisions**."
- Content capture: message content "is likely to contain sensitive information including user/PII data";
  instrumentations "**SHOULD NOT** capture this attribute by default. Capture **SHOULD** be gated by an explicit
  user opt-in" `[D03-S21]`.

### 4.2 Practitioner-grade sampling / cost material (secondary — mark as such)

`[D03-S40]` (aggregated practitioner sources): a workable tiered policy is 100% structural spans (attributes only),
100% of errors and high-cost traces, and ~1% full-content reservoir sampling, with a collector-side redaction layer
as a safety net; above ~1,000 rps reduce envelope sampling to 10–20% and reserve token-level capture for explicit
debug sessions; use **head-based sampling keyed to session ID** so whole sessions survive rather than random
fragments; store token counts and a computed USD cost as numeric span attributes **in a span processor** so the
sampler can keep expensive traces; propagate W3C trace context across process boundaries and group spans into
conversations by session ID. These are reasonable but **secondary** — do not present as Anthropic guidance.

### 4.3 Platform correlation handles (primary)

- `request-id` header on every response; same value as `request_id` in error bodies; Python/TS SDKs expose
  `_request_id` `[D03-S25]`. This is the join key from "a user complained at 14:02" to a specific API call.
- `anthropic-workspace-id` response header identifies which workspace a request counted against `[D03-S24]`.
- Rate-limit headroom is observable from `anthropic-ratelimit-{requests,tokens,input-tokens,output-tokens}-{limit,
  remaining,reset}` headers; the `tokens-*` triple reports **the most restrictive limit currently in effect**
  `[D03-S24]`.
- Cache health is observable from `usage.cache_read_input_tokens` vs `input_tokens`; on a warmed loop reads should
  dominate and `cache_creation_input_tokens` should be roughly one turn's worth `[D03-S33]`.
- Usage/cost per model, key, workspace, service tier, and context window come from the Admin API usage/cost reports
  (`uncached_input_tokens`, `cache_read_input_tokens`, `cache_creation.ephemeral_5m/1h_input_tokens`,
  `output_tokens`); data appears ~5 minutes after a request completes `[D03-S33]`.
- A key shared across projects blends their traffic and makes per-project reads unattributable → per-project keys
  or workspaces are a **measurement prerequisite** `[D03-S33]`.

---

## 5. Objectives 5 & 6 — RAG pipeline and retrieval strategy

### 5.1 Contextual Retrieval, measured `[D03-S14]`

| Configuration | Top-20 retrieval failure rate | Reduction vs baseline |
|---|---|---|
| Baseline (dense embeddings, top-20) | **5.7%** | — |
| + Contextual Embeddings | 3.7% | **35%** |
| + Contextual Embeddings + Contextual BM25 | 2.9% | **49%** |
| + reranking | 1.9% | **67%** |

- Contextualizing prompt (verbatim): *"Please give a short succinct context to situate this chunk within the
  overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct
  context and nothing else."* Generated context runs **50–100 tokens per chunk**.
- One-time preprocessing cost **with prompt caching: $1.02 per million document tokens**.
- Threshold for skipping RAG entirely: "your knowledge base is smaller than 200,000 tokens (about 500 pages of
  material)" → stuff the whole corpus into the prompt (and cache it). Beyond that, RAG with Contextual Retrieval.
- Recommended order: contextual embeddings → contextual BM25 → rerank → retrieve top-20 into the model context.
- Chunking: the article references 800-token chunks over 8k-token documents in its cost example but "doesn't
  explicitly prescribe optimal chunk sizes." It states "chunk size, chunk boundary, and chunk overlap can affect
  retrieval performance" and **recommends experimentation**. → any specific chunk-size recommendation in the
  chapter must be framed as an experiment starting point, not an Anthropic recommendation.

### 5.2 Citation granularity is a chunking decision `[D03-S28]`

| Document type | Chunking done by the API | Citation location type |
|---|---|---|
| Plain text | Sentence | Character indices (0-indexed, exclusive end) |
| PDF | Sentence (text extracted; image citation unsupported) | Page numbers (1-indexed, exclusive end) |
| Custom content | **None** — your content blocks are used as-is | Content block indices (0-indexed, exclusive end) |

Key operational guidance, verbatim: "if you want Claude to be able to cite specific sentences from your RAG chunks,
you should put each RAG chunk into a plain text document. Otherwise, if you do not want any further chunking to be
done, or if you want to customize any additional chunking, you can put RAG chunks into custom content document(s)."
`title` and `context` are passed to the model but are **not citable**; `context` is the place for stringified
metadata. Enabling citations slightly increases input tokens; `cited_text` costs **no** output tokens and no input
tokens when replayed. **Citations + structured outputs (`output_config.format`) → 400** — they are incompatible.
Citations must be enabled on **all or none** of the documents in a request.

### 5.3 `search_result` content blocks `[D03-S27]`

Purpose-built for RAG attribution: `{type: "search_result", source, title, content: [text blocks],
citations: {enabled}}`. Two delivery paths: (1) returned from a custom tool → dynamic RAG; (2) top-level in a user
message → pre-fetched/cached content. All active models except Haiku 3 support them; no beta header.
Best practice: "Use clear, permanent source URLs", "Provide descriptive titles", and **"Break long content into
logical text blocks to give Claude finer citation boundaries."** Return "only the most relevant results to avoid
context overflow."

### 5.4 Retrieval strategy — data shape × query pattern (constructed matrix; reasoning from `[D03-S14]`, `[D03-S16]`, `[D03-S17]`, `[D03-S18]`)

| Data shape | Query pattern | Primary mechanism | Why alternatives lose |
|---|---|---|---|
| Relational / tabular (ledger, claims, inventory) | Aggregation, filter, join | Parameterized SQL behind a narrow tool | Chunking rows destroys join semantics; embeddings cannot compute `SUM` |
| Relational, large result set | Aggregation over thousands of rows | SQL + programmatic tool calling / code execution | Raw rows in context blow the budget; PTC filters before context `[D03-S15]`, `[D03-S16]` |
| Long prose (policy, contracts, manuals) | Conceptual / paraphrased lookup | Hybrid dense + BM25 over contextualized chunks, then rerank | Dense-only leaves 3.7% top-20 failure vs 1.9% `[D03-S14]` |
| Long prose | Exact identifier (clause 7.3.1, error `E4012`, SKU) | Lexical/BM25 first (optionally exact-match pre-filter) | Dense embeddings under-weight rare tokens; this is precisely what contextual BM25 adds `[D03-S14]` |
| Source code | "Where is X implemented / what calls Y" | Agentic file search over the live tree (glob/grep/read) | An embedding index is stale one commit later; Claude Code's own hybrid is pre-loaded `CLAUDE.md` + just-in-time grep/glob `[D03-S17]` |
| Tickets / CRM records (semi-structured, metadata-rich) | "Similar prior cases" | Dense semantic + metadata filters (product, version, date window) | Pure lexical misses paraphrase; pure dense ignores the filters that make results relevant |
| Time series / metrics / logs | Trend, anomaly, windowed aggregate | The store's own query language (PromQL/SQL/log query) via a tool | Retrieval over serialized points is lossy and unaggregatable |
| Entity–relationship graph (org, supply chain, fraud rings) | Multi-hop ("who else touched this claim") | Graph traversal tool | Chunk retrieval cannot follow edges; each hop needs a new query |
| Live system-of-record state (order status, balance, entitlement) | Point lookup by identifier | **Direct API call — do not index** | Any index introduces staleness on data whose whole value is freshness |
| Any corpus under ~200K tokens | Anything | Full-context stuffing + prompt caching | Below the threshold a pipeline adds failure modes without adding recall `[D03-S14]` |
| Mixed corpus, exploratory research | Open-ended, multi-step | Agentic search: model issues successive narrowing queries | One-shot top-k cannot reformulate; progressive disclosure yields signals that inform the next query `[D03-S17]` |

### 5.5 Index freshness / staleness (derived; grounded in `[D03-S01]` Sample 3)

`[D03-S01]` Sample 3 answer key: "Confident-but-wrong answers following a document refresh, with model and latency
unchanged, point to retrieval feeding the model poor context, for example a broken re-index or mismatched
embeddings." This is the canonical Domain 3/4 boundary item. Mechanisms to teach: incremental upsert keyed by a
content hash + tombstones for deletes; embedding-model version pinned as index metadata so a model swap forces a
full re-embed rather than silently mixing vector spaces; a freshness SLO (max index lag) monitored as a metric;
retrieval evaluated **separately** from generation (recall@k / failure-rate@k on a labeled query set) so a recall
regression is visible before it surfaces as a hallucination.

---

## 6. Objective 7 — Protocol selection

### 6.1 MCP transports `[D03-S09]`

- Two standard transports: **stdio** and **Streamable HTTP**. "Clients **SHOULD** support stdio whenever possible."
- stdio: client launches the server as a subprocess; newline-delimited JSON-RPC on stdin/stdout; server **MUST NOT**
  write non-MCP output to stdout; stderr is free-form and "**SHOULD NOT**" be assumed to indicate errors.
  Authorization spec does **not** apply — "retrieve credentials from the environment" `[D03-S07]`.
- Streamable HTTP: one endpoint supporting POST and GET; POST body is a single JSON-RPC message; client **MUST**
  `Accept: application/json, text/event-stream`; notifications/responses get 202; requests get either
  `application/json` or an SSE stream. GET opens a server→client SSE stream or returns 405.
- Security warning (verbatim): servers **MUST** validate the `Origin` header on all incoming connections to prevent
  DNS rebinding (invalid → **403**); when running locally servers **SHOULD** bind only to 127.0.0.1 rather than
  0.0.0.0; servers **SHOULD** implement proper authentication for all connections.
- Sessions: optional `MCP-Session-Id` on the `InitializeResult`; SHOULD be globally unique and cryptographically
  secure; visible ASCII 0x21–0x7E; client MUST echo it on every subsequent request; server MAY terminate → 404,
  and the client **MUST** then start a new session; DELETE to terminate explicitly (server MAY 405).
- Resumability: server MAY attach SSE event `id`s (globally unique per session, encoding the originating stream);
  client resumes with `Last-Event-ID` on a GET; server **MUST NOT** replay messages from a different stream.
- `MCP-Protocol-Version` header required on all subsequent HTTP requests; absent → server SHOULD assume
  `2025-03-26`; invalid/unsupported → **400**.
- The old HTTP+SSE transport (protocol `2024-11-05`) is deprecated; backwards-compat recipe given.

### 6.2 A2A `[D03-S19]`

- "An open standard for communication between AI agents." Purpose: remove point-to-point custom integrations
  between specialized agents from different developers/frameworks/organizations.
- Explicit MCP contrast: MCP "focuses on connecting Large Language Models (LLMs) with data and external
  resources — essentially exposing stateless tools to agents"; A2A lets agents "collaborate in their native
  modalities" through multi-turn interactions, "negotiate, reason, and delegate tasks." Wrapping an agent as a
  simple tool is "limiting: it can't capture the agent's full capabilities."
- Core: **Agent Card** at `/.well-known/agent-card` (capabilities + security requirements); `sendMessage` /
  `sendMessageStream`; tasks; **artifacts** streamed incrementally; auth via security schemes declared in the Agent
  Card, with OpenID Connect support for JWT acquisition; transport = HTTP + JSON-RPC + SSE.
- Design principles include **opaque execution** — the counterpart's internal logic and IP stay hidden.

### 6.3 Surfaces on the Anthropic side `[D03-S30]`, `[D03-S31]`, `[D03-S32]`

Four ways to build an agent, separated by two questions — who supplies the **harness** and who supplies the
**deployment**:

| # | Approach | You write | Harness / deployment | Tools |
|---|---|---|---|---|
| 1 | Messages API, manual loop | the `while stop_reason == "tool_use"` loop | you build both | only yours |
| 2 | Messages API + SDK Tool Runner | tool functions only | SDK harness; you host | only yours |
| 3 | Managed Agents (beta) | agent config + tool results | Anthropic harness **and** per-session sandbox | hosted sandbox + Skills/MCP + yours |
| 4 | Claude Agent SDK (separate product) | a prompt + options | Claude Code harness; you host | built-in Read/Write/Edit/Bash/Glob/Grep/Web + MCP + subagents |

Agent SDK capabilities: built-in tools, hooks, subagents, MCP, permissions, sessions, skills/commands/memory,
plugins `[D03-S30]`. "To drive the same agent loop from a language other than Python or TypeScript, run the CLI as
a subprocess with the `-p` flag and `--output-format json`" — i.e. CLI-as-integration is a documented path
`[D03-S30]`.

MCP connector vs own MCP client `[D03-S05]`: "Use the `mcp_servers` API parameter when you have remote servers
accessible by URL and only need tool support. Use the client-side helpers when you need local servers, prompts,
resources, or more control over the connection."

Tool search vs mid-conversation tool changes `[D03-S31]`: "tool search is for *discovery* — Claude finds what it
needs from a large library on its own. Mid-conversation tool changes are for *control* — your application decides
the tool set has changed (a mode switch, a resource that became available, a capability you want to revoke) and
says so explicitly." Mid-conversation tool changes use beta `mid-conversation-tool-changes-2026-07-01` with
`tool_addition` / `tool_removal` / `tool_reference` blocks on a `{"role": "system"}` message; a tool to be added
must already be declared with `defer_loading: true`.

---

## 7. Objective 8 — Progressive discovery vs monolithic context

### 7.1 The argument `[D03-S17]`

- **Context rot**: "as the number of tokens in the context window increases, the model's ability to accurately
  recall information from that context decreases." Rooted in n² attention relationships and training-distribution
  skew toward shorter sequences. Context is a **finite resource with a diminishing marginal return**.
- **Just-in-time retrieval / progressive disclosure**: keep lightweight identifiers, load data at runtime; "allows
  agents to incrementally discover relevant context through exploration," where each interaction yields signals
  informing the next.
- **Hybrid is the recommendation, not pure JIT**: "some data retrieved upfront for speed, with agents pursuing
  autonomous exploration afterward," acknowledging that "runtime exploration is slower than retrieving
  pre-computed data." Claude Code is the worked example: pre-load `CLAUDE.md`, expose grep/glob for the rest.
- Long-horizon triad: **compaction** (summarize history, keep decisions and open issues), **structured note-taking**
  (external memory files surviving context resets), **sub-agents** (focused work returning condensed summaries).
  Choice depends on task shape: compaction for long back-and-forth, notes for iterative development, multi-agent
  for parallel exploration.

### 7.2 Cache interaction — the decisive architectural detail

- Tool search **preserves the cache**: deferred tools are excluded from the system-prompt prefix and discovered
  tools are **appended** inline as `tool_reference` blocks — "The prefix is untouched, so prompt caching is
  preserved" `[D03-S02]`, `[D03-S32]`.
- By contrast, editing `tools` mid-conversation "changes the very front of the prompt prefix and invalidates the
  entire cache" `[D03-S31]`. Switching models mid-session invalidates (caches are per-model); changing
  `thinking`/`effort` invalidates the messages cache; `tool_choice` changes invalidate cached *message* blocks
  while tools and system stay cached `[D03-S04]`, `[D03-S33]`.
- So: progressive discovery is cache-compatible **only via the mechanisms designed for it** (tool search,
  `defer_loading`, mid-conversation tool changes with pre-declared deferred tools, skills). Hand-rolled "swap the
  tools array per turn" is the cache-hostile version of the same idea.

### 7.3 The cost of over-deferring

`[D03-S33]`, whole-section caveat: "a smaller prefix is not automatically a cheaper task. Deferring context means
the model may spend discovery turns fetching what it previously read inline. Validate against the eval — on the
cookbook's workload, wrapping the manual in a tool matched the explicit-breakpoint config on cost and gave back
accuracy." Also: tool search "pays once schemas run past roughly 10K tokens (MCP servers reach that fast); below
that the search step is overhead."

Code-execution / filesystem MCP tradeoff `[D D03-S16]`: "Running agent-generated code requires a secure execution
environment with appropriate sandboxing, resource limits, and monitoring. These infrastructure requirements add
operational overhead and security considerations that direct tool calls avoid… The benefits of code execution —
reduced token costs, lower latency, and improved tool composition — should be weighed against these implementation
costs." Also a *privacy* benefit: "Intermediate results stay in the execution environment by default," enabling PII
tokenization so real emails/phones "never [flow] through the model."

---

## 8. Contradictions and open questions

| # | Item | Status |
|---|---|---|
| C1 | Model lineup: AGENT-BRIEF says Opus 5 current; `[D03-S29]` says Opus 5.5 current and Opus 5 legacy | **Contradiction.** Docs win (primary, fetched 2026-09-24). Draft uses tier language + dated footnote. |
| C2 | Multi-server MCP token overhead: "~55K" `[D03-S02]` vs "~77K" `[D03-S15]` | **Contradiction (minor).** Draft cites ~55K for the itemized 58-tool/5-server figure and "over 85% reduction." |
| C3 | MCP spec revision the exam will target: 2025-06-18, 2025-11-25, and 2026-07-28 all exist; exam effective July 2026 | **Open.** Draft teaches the invariants that hold across all three (audience validation, no token passthrough, per-client consent, no sessions-for-auth) and flags DCR-deprecation as version-dependent. |
| C4 | Chunk size: no Anthropic-prescribed value; only "800 token chunks" in a cost example plus "experiment" `[D03-S14]` | **Open.** Draft must not present a chunk size as official. |
| C5 | Idempotency keys on the Messages API | **NOT FOUND** in `[D03-S25]`. Marked `[UNVERIFIED]` in the draft; the documented correlation handle is `request-id`. |
| C6 | Whether CCAR-P items reference `defer_loading`, `mcp_toolset`, or other beta-gated parameter names | **Open.** Objectives are protocol/strategy-level, not parameter-level; the draft teaches parameters as evidence for architectural claims, not as recall targets. |
| C7 | OTel GenAI conventions stability | Conventions relocated to a separate repo `[D03-S20]`; individual attributes carry their own stability. Draft treats attribute *names* as illustrative and the *instrumentation decisions* as the teachable content. |
| C8 | A2A governance/trust classification | A2A is an open standard with its own site/spec `[D03-S19]`. Treated as primary-standard but noted as a non-Anthropic ecosystem protocol; the exam objective names "agent-to-agent" generically, so the draft teaches the *category* and uses A2A as the concrete instance. |

---

## 9. Prep-material landscape

Swept 2026-09-24 via web search `[D03-S34]`–`[D03-S39]`. The certification is effective July 2026, so all of this
is at most ~3 months old and none of it is Anthropic-authored. **None of it was used as a source for the chapter,
and nothing was copied from any of it.**

| Source | What it claims | Trust | Judgment |
|---|---|---|---|
| Udemy — "Claude Certified Architect Professional CCAR-P Practice Test" `[D03-S34]` | 360 questions, 6 timed exams | **low** | Volume claims with no authoring provenance; an exam this new cannot have 360 validated items. Classic post-launch question-bank pattern. |
| Udemy — second CCAR-P practice-test listing (note the "CCAP"/"CCARP" slug typos) `[D03-S34]` | practice tests | **low** | Slug typos in the product URL are a marker of rapid, low-review listing creation. |
| Tutorials Dojo — CCAR-P study guide `[D03-S35]` | Topic coverage mirroring the blueprint | **low** (publisher is reputable for AWS; this title has no track record) | Blueprint restatement is safe but adds nothing beyond §6 of the official guide. Do not cite. |
| claudecertificationguide.com `[D03-S36]` | "30 lessons and 250+ practice questions," free, no sign-up | **low** | Unaffiliated domain that trades on the credential name; free + no-signup + high volume is the SEO/AI-generated profile the brief warns about. |
| preporato.com `[D03-S37]` | "6 practice tests with 378+ questions," $19.99 lifetime | **low** | Same profile. |
| certsafari.com `[D03-S38]` | "456 exam-style practice questions aligned with the latest exam guide" | **low** | Same profile; "aligned with the exam guide" is an unverifiable claim. |
| skillcertpro / clearcatnet blog `[D03-S39]` | question packs / "exam guide" blog posts | **low** | Same profile. |

Risk to this course: several of these sites restate the blueprint verbatim, so an editor searching for
"CCAR-P integration objectives" will surface them and may mistake restatement for authority. **Rule for reviewers:
if a claim about the exam cannot be traced to `claude-arch-professional-guide.md`, it is not an exam fact.** If a
claim about the platform cannot be traced to `platform.claude.com` / `modelcontextprotocol.io` / an Anthropic
engineering post, it is not a platform fact.

No evidence found of leaked live items (which would be a policy violation under `[D03-S01]` §12–13). No third-party
material was read beyond search-result snippets.

---

## 10. Draft-construction notes (for reviewers)

- 8 objectives → 8 named concept clusters → the trade-off tables map 1:1 onto objectives so the coverage table is
  mechanical.
- The two mandated tables are §4 T7 (retrieval strategy by data shape × query pattern) and §4 T8 (protocol
  selection). Both carry explicit axes and a "choose X when" discriminator per row.
- Worked scenarios span financial services, healthcare, retail, government, SaaS/multi-tenant, telco/field service,
  and legal — 7 scenarios plus one cross-cutting SLA negotiation.
- Practice items: 12 (8 single-response, 4 multiple-response with the count stated in the stem), each with a
  per-distractor rationale. Item cognitive level is matched to `[D03-S01]` §8 — scenario stem, "best/first/most
  likely" phrasing, no parameter-name trivia.
- Every numeric claim in the draft carries a source ID. Two claims are marked `[UNVERIFIED]`: the Messages-API
  idempotency-key gap (C5) and the practitioner sampling percentages (C-level secondary, attributed to
  `[D03-S40]` and labeled as practitioner guidance rather than vendor guidance).
