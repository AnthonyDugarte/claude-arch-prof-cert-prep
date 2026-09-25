# Domain 3 — Integration

Blueprint weight: **19%**. The eight objective IDs follow the supplied guide. Source-backed protocol facts are linked; design recommendations, lab criteria, and practice cases are instructional. Research checked 2026-09-24. MCP references intentionally identify specification version 2025-11-25; verify negotiated versions and target-platform support when implementing.

## D3.1 — Evaluate tool and agent configuration for capability bloat

**Capability bloat** occurs when an agent has more tools, agents, permissions, or context than its task warrants. It increases both selection ambiguity and the scope of possible mistakes. A support drafting assistant generally needs ticket reading and draft creation; a refund or account-deletion capability requires its own demonstrated use case and authority.

Inventory each capability by consumer, task, permission, side effect, usage frequency, schema size, failure rate, and owner. Remove unused dangerous capabilities before optimizing how their descriptions are loaded. Hiding a tool through discovery is not revoking its permission.

| Configuration | Appropriate use | Trade-off |
|---|---|---|
| Small explicit toolset | Narrow, stable workflow | Clear choices; limited breadth |
| Role/task-specific subsets | Several distinct responsibilities | Better fit; routing and configuration maintenance |
| Large discoverable catalog | Broad tasks with sparse tool usage | Smaller initial context; discovery can miss tools |
| One generic shell/database tool | Controlled engineering environment | Flexible but broad authority and validation burden |

Tool design is an interface-design problem. Prefer descriptions that specify when to use the tool, required identifiers, constraints, and meaningful result fields. Avoid near-duplicate operations with ambiguous names. Anthropic documents context and tool-selection costs from large catalogs and describes on-demand discovery as one remedy. [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)

**Example:** Replace five overlapping customer-search tools with an approved customer-lookup operation that returns stable IDs and minimal fields. Do not combine unrelated privileged actions merely to reduce tool count. Capability clarity and least privilege matter more than a cosmetic number of tools.

## D3.2 — Analyze authentication and authorization gaps

**Authentication** identifies the caller. **Authorization** decides whether that caller may perform a particular operation on a particular resource. Both must survive delegation. A valid platform API key does not establish that a specific end user can access a particular customer account.

Trace identity end to end: user → application → agent runtime → connector → downstream service. At each hop ask who the principal is, what permissions apply, where credentials live, and who performs object-level checks. Scope searches by tenant and user before returning evidence to the model. Test guessed resource IDs and stale permissions, not just successful login.

For HTTP-based MCP authorization, the cited specification requires intended-recipient validation and resource indicators in the authorization flow. Tokens for an upstream service are not interchangeable with tokens issued to the MCP server. [MCP authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)

MCP security guidance explicitly rejects token passthrough: accepting a token without verifying it is intended for the server and forwarding it downstream undermines security boundaries. Use the appropriate separate authorization flow for downstream APIs. [MCP security best practices](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices)

Recommended gap analysis:

| Gap | Why it matters | Design response |
|---|---|---|
| Shared broad service account | User intent may gain excessive authority | Narrow scopes plus server-side user/resource checks |
| Tenant filter added after generation | Unauthorized content already reached the model | Enforce before retrieval results leave storage |
| Prompt-only permission rule | Model behavior substitutes for access control | Check every operation in trusted code |
| Secrets in tool output or logs | Credentials spread across model and telemetry | Secret storage and output/log redaction |
| Approval detached from parameters | Approved action can differ from executed action | Bind approval to exact operation, target, and parameters |

A confirmation screen does not fix a tool that can access any tenant. Conversely, an authorized read does not authorize sending its contents to an unrelated destination. Evaluate combined capabilities and data flow, not each tool in isolation.

## D3.3 — Justify accuracy–latency trade-offs

An integration pipeline's latency includes queues, discovery, retrieval, reranking, model generation, tools, retries, and validation. First-token latency and completed-answer latency answer different questions. A faster visible token does not mean a verified action has completed.

| Decision | Potential quality benefit | Added cost | When simpler wins |
|---|---|---|---|
| Rerank retrieval candidates | Better evidence ordering | Additional inference/service call | Easy exact-ID queries already retrieve correctly |
| Query expansion | Better recall for ambiguous language | More searches and irrelevant matches | Query has an authoritative identifier |
| More evidence chunks | Broader coverage | Tokens, distraction, processing | Extra chunks are redundant |
| Additional reviewer agent | Detect some errors | Tokens and critical-path latency | Deterministic validator already checks the property |
| Parallel independent reads | Similar result with shorter critical path | Concurrency pressure | Quotas or dependencies require serialization |

Build a latency budget and test under representative load. If retrieval takes 150 ms but a second model review takes 3 s, optimizing the index alone will not meet a 2 s requirement. If a larger model avoids two retries, it may reduce completion time despite slower individual inference.

Treat a quality–latency comparison as constrained experimentation. Fix the test cases, measure grounding and task success, and vary one decision at a time. Evaluate the tail: a low median can conceal long agent loops and rate-limit retries. When a deadline expires, return an explicit partial/queued state rather than a fabricated successful result.

## D3.4 — Select observability strategies at scale

**Metrics** show aggregate behavior; **traces** follow an execution across components; **logs/events** capture particular occurrences. OpenTelemetry provides these complementary signals and the means to collect and export them. [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)

Recommended trace spans: authorization, retrieval, reranking, model call, each tool attempt, validation, and final outcome. Propagate a correlation ID through asynchronous work. Record model/prompt/tool versions, index version, latency, token usage, cache status, retry count, and sanitized error category. Preserve source IDs and action IDs without copying all source content into every event.

| Scale challenge | Monitoring design |
|---|---|
| High trace volume | Sample routine traces while retaining selected failures and slow runs |
| Rare safety failures | Separate audit events and targeted tests; random sampling alone is insufficient |
| High-cardinality customer IDs | Keep identifiers in controlled traces, avoid unbounded metric labels |
| Sensitive prompts | Redact/minimize capture, enforce retention and access policies |
| Aggregate quality hides segments | Break down by task, tenant tier where appropriate, language, and version |
| Async execution | Preserve parent/child or linked execution identifiers |

A green HTTP success metric proves transport success, not answer correctness. Couple operational metrics with sampled quality review and delayed business outcomes. For a sudden regression, versioned traces should distinguish a prompt rollout from an index refresh or tool outage.

Sampling is an explicit evidence limitation. If 1% of traces are retained, absence of a bad trace does not prove absence of a failure. Preserve security-relevant decisions through a suitably governed audit mechanism and keep alert thresholds tied to user impact.

## D3.5 — Design RAG chunking and indexing

**Retrieval-augmented generation (RAG)** selects external evidence and supplies it to the model for answering. Its pipeline has separate ingestion and query paths:

`ingest → parse → normalize → chunk → attach metadata/ACLs → embed/index → version/publish`

`query → authenticate/filter → retrieve → optional rerank → pack evidence → generate → validate/cite`

Chunking chooses the retrievable unit; indexing makes those units searchable. Small chunks can isolate relevant details but lose context. Large chunks preserve relationships but may dilute matching and increase prompt size. Start with document structure—headings, paragraphs, tables, functions—and test against actual questions. Keep headings, document IDs, versions, dates, and location information with chunks.

Anthropic's contextual-retrieval approach prepends document-specific explanatory context to chunks before embedding and lexical indexing. It also evaluates hybrid retrieval and reranking. Its reported gains come from particular datasets and configurations; they are not universal thresholds. [Contextual retrieval](https://www.anthropic.com/engineering/contextual-retrieval)

**Example:** “The limit is 30 days” is ambiguous without the policy, region, and exception it belongs to. Preserve those relationships in chunk metadata or surrounding content. For a table, retain headers and units; splitting cells independently can turn a correct number into a wrong claim.

Version the embedding model and index configuration together. Re-embedding documents without compatible query embeddings can break retrieval. Publish refreshed indexes deliberately, test known questions, and support rollback. Apply deletions and access changes to searchable data promptly. A citation to an obsolete policy is still an error even when the generated text accurately quotes it.

## D3.6 — Match retrieval to data shape and query pattern

| Data/query | Preferred starting point | Why | Limitation |
|---|---|---|---|
| Exact invoice or error code | Identifier lookup or lexical search | Preserves exact symbols | Does not handle broad paraphrases well |
| Natural-language policy question | Dense semantic or hybrid retrieval | Matches meaning and terminology | Can retrieve plausible but wrong neighboring policies |
| Counts, sums, latest account status | Authorized structured query/API | Computes over authoritative records | Requires schema and access controls |
| Hierarchical technical documents | Child retrieval with parent context | Combines precise matching and surrounding explanation | More context can include noise |
| Multi-hop relationship question | Staged retrieval or structured relationship query | Follows dependencies | More steps and compounded failure opportunities |
| Small complete document comparison | Full-context input candidate | Avoids chunk omission | Context cost and distractors |

Hybrid retrieval combines lexical and semantic evidence, useful when users mix exact product codes with paraphrases. Reranking can improve ordering after broad candidate retrieval, but cannot recover a relevant passage never retrieved. Measure recall separately from answer faithfulness.

Construct a retrieval test set with known supporting documents, unanswerable questions, old/new policy conflicts, exact codes, and cross-tenant traps. If the correct evidence is absent from candidates, work on ingestion/retrieval. If present but ignored, inspect packing, prompting, and synthesis. Changing the model first can mask the true cause.

## D3.7 — Select MCP, direct API/CLI, or agent-to-agent integration

MCP defines standard transports including stdio and Streamable HTTP in the cited version. Transport selection has operational and security consequences; do not assume local-process and remote HTTP authorization work identically. [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)

| Mechanism | Prefer when | Trade-offs |
|---|---|---|
| Direct API/SDK | Stable service integration and precise contracts | Minimal protocol layers; custom adapter maintenance |
| CLI | Existing trusted developer tool performs the needed operation | Practical reuse; process permissions, output parsing, shell risks |
| MCP | Standard tool/context exposure across compatible clients | Interoperability; server lifecycle, negotiation, permission design |
| Agent-to-agent protocol | Delegate a task to an independently operated agent | Task lifecycle and capability discovery; distributed trust/failure handling |

A2A uses Agent Cards to advertise capabilities and supports tasks for longer-running work, along with messages and artifacts. It is useful to study as an agent-to-agent example; the supplied blueprint does not prescribe one named A2A implementation. [A2A core concepts](https://a2a-protocol.org/latest/topics/key-concepts/)

MCP and A2A can coexist: a remote agent may perform a delegated investigation and use MCP tools internally. Neither protocol proves output quality or grants business authorization by itself. Choose based on the abstraction needed—operation invocation versus delegated task ownership—and the organization's ability to secure and operate it.

## D3.8 — Evaluate progressive discovery versus monolithic context

**Monolithic context** loads all available instructions/tool descriptions upfront. **Progressive discovery** starts with compact descriptions and loads details when needed. Discovery saves initial context for large catalogs but introduces an extra decision and possible miss. Anthropic's advanced tool-use design explicitly identifies this latency-versus-context trade-off. [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)

For four short tools used on every request, eager loading is often simpler. For hundreds of specialized tools, discovery may reduce ambiguity and overhead. A hybrid keeps frequently used essentials immediately available and defers rare capabilities. Measure discovery recall, wrong-tool rate, total tokens, and completion latency.

Do not defer mandatory safety controls or treat absence from context as a permission boundary. Authorization must apply even if a tool is discovered unexpectedly. Give discovery metadata realistic synonyms and disambiguating purpose; “process_data” is a weak discovery description.

## Practical lab — Integrate a permissioned knowledge assistant

Build or specify a corpus of 20 documents with two tenants, old/new versions, exact product codes, a table, and one adversarial instruction embedded as document data. Create 20 labeled queries including five unanswerable or unauthorized cases. Compare lexical, semantic, and hybrid retrieval, then test one reranking option. Mark runtime measurements unmeasured if only designing the experiment.

Add two read tools and one separately authorized write tool; document API versus MCP selection. Trace an entire run, inject one downstream timeout, and test eager versus deferred discovery on a larger synthetic catalog.

**Acceptance criteria:** zero cross-tenant evidence exposure in the test cases; permissions checked at the service boundary; citations resolve to the correct document version; retrieval recall and answer support measured separately; p95 includes integration stages; expired credentials and ambiguous write outcomes handled explicitly; tool discovery never substitutes for authorization. Report which configuration meets the declared quality/latency constraints and when another would win.

## Original practice questions — not official exam items

**1. Select ONE.** A draft-only assistant exposes deletion tools that are never used. Best first change?

A. Hide deletion behind discovery. B. Remove deletion from its capabilities and permissions. C. Log deletions. D. Rename deletion more clearly.

**Answer: B.** A changes visibility, not authority. B removes unnecessary capability. C helps detection after access exists. D improves clarity but retains the unnecessary risk.

**2. Select TWO.** A remote MCP server accepts a downstream-service token and forwards it without intended-recipient validation. Which changes address the gap?

A. Validate tokens intended for the MCP server. B. Put the token in the model prompt. C. Use the appropriate separate downstream authorization flow. D. Trust the token because it has not expired.

**Answer: A, C.** A restores audience binding. B exposes credentials and does not validate authority. C avoids forbidden passthrough. D ignores who the token was issued for.

**3. Select ONE.** Exact error-code queries fail semantic retrieval while paraphrased policy queries work. Best experiment?

A. Use lexical or hybrid retrieval for code-sensitive queries. B. Increase answer temperature. C. Double output length. D. Remove error codes from the corpus.

**Answer: A.** A directly addresses exact-symbol matching. B and C affect generation rather than candidate retrieval. D deletes the evidence users need.

**4. Select ONE.** Every API call returns HTTP 200, but users report wrong policies after an index refresh. Most useful next evidence?

A. Overall HTTP availability only. B. Versioned retrieval traces and known-question tests. C. Prompt character count. D. Number of connected tools.

**Answer: B.** A cannot prove semantic success. B links the refresh to retrieved evidence and affected questions. C and D may be contextual metadata but do not diagnose this trigger.

**5. Select TWO.** A catalog has 300 tools, with only four commonly used. Which design choices are defensible?

A. Keep common tools eager and test discovery for rare tools. B. Enforce permissions regardless of loading strategy. C. Treat deferred tools as inaccessible by definition. D. Promise discovery always lowers latency.

**Answer: A, B.** A balances frequent access and context cost. B preserves the security boundary. C confuses discovery with authorization. D ignores search latency and misses.

**6. Select ONE.** Another organization's agent owns a multi-hour investigation and returns artifacts asynchronously. Which abstraction most directly matches the need?

A. A single synchronous database lookup. B. An agent-to-agent task lifecycle with explicit status, artifacts, and authorization. C. A shell command with unrestricted credentials. D. A larger system prompt containing the other organization's entire implementation.

**Answer: B.** A cannot represent the delegated work lifecycle. B matches independent task ownership. C grants unnecessary authority and lacks the contract. D is neither necessary nor a workable task interface.
