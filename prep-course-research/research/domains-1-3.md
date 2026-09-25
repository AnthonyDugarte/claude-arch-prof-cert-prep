# Research record — Domains 1, 2, and 3

Researcher role: architecture/models/integration researcher. Retrieval date for every source below: **2026-09-24**. Scope derives from the user-supplied `claude-arch-professional-guide.md`, read locally. The local guide is a task specification; this research does not publicly authenticate its exam details or establish official course endorsement.

Deliverables: [Domain 1](../course/01-solution-design.md), [Domain 2](../course/02-models-prompts-context.md), [Domain 3](../course/03-integration.md). Each objective has a teaching section, and each module has original scenarios, comparisons, a practical lab, and six original questions. Numerical worked examples and lab thresholds are explicitly instructional rather than vendor benchmarks or exam standards.

## Dedicated search log

Queries are recorded exactly as submitted. Search-engine results were discovery aids. Only the opened primary sources in the register underpin technical claims; community and third-party hits were not used as authorities.

| Search ID | Domain/objective groups | Exact query | Outcome |
|---|---|---|---|
| Q1 | D1.1–D1.3, D1.5–D1.6 | `site.anthropic.com engineering building effective agents workflows agents parallelization` | Located S1 pattern definitions and original engineering guidance |
| Q2 | D1.4–D1.5 | `site.anthropic.com engineering multi-agent research system token cost` | Located S2 production research-system case study |
| Q3 | D2.1–D2.2, D2.5 | `site.platform.claude.com docs models overview prompt caching prompt engineering skills` | Located official platform reference families; opened exact pages S3–S5 and S8 |
| Q4 | D2.3–D2.4 | `site.platform.claude.com docs prompt engineering multishot chain of thought context windows` | Located prompting/context guidance; opened S6–S7 |
| Q5 | D3.1, D3.3, D3.5–D3.6, D3.8 | `site.anthropic.com engineering contextual retrieval advanced tool use tool search` | Located S9–S10; evaluated engineering results as workload-specific |
| Q6 | D3.2, D3.7 | `site.modelcontextprotocol.io specification authorization security best practices` | Broad results included mirrors; used canonical official S11–S13 only |
| Q7 | D2.2–D2.5 follow-up | `site.platform.claude.com docs prompting best practices context windows agent skills overview` | Confirmed living reference and skill authoring guidance; S6–S8 |
| Q8 | D3.2 follow-up | `site.modelcontextprotocol.io specification 2025-11-25 security best practices token passthrough` | Verified protocol-version-specific security source S12 |
| Q9 | D3.4 | `site.opentelemetry.io docs concepts signals traces metrics logs` | Located S14, opened and inspected signal definitions |
| Q10 | D3.7 agent delegation | `site.a2a-protocol.org latest topics key concepts agent card task` | Located S15; used as an example of agent-to-agent concepts, not a mandated exam protocol |

Searches were submitted in domain-specific batches; Q7–Q10 were follow-ups to close individual objective gaps. Additional resources S16–S17 were opened by direct official-repository URL after the Anthropic documentation linked to interactive tutorials/cookbook material.

## Primary-source register

All entries are **opened**, not merely indexed. “Opened” means the actual source page was requested through the web tool; some pages were additionally inspected using find against relevant terms. No source code example in these modules claims to have been executed. URLs are canonical where a redirect was observed.

| ID | Title and canonical URL | Supports | Access | Authority/limits |
|---|---|---|---|---|
| S1 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | D1.1–D1.3: augmented LLM, workflow/agent distinction; D1.5: pattern vocabulary | Opened 2026-09-24 | Anthropic engineering article, originally 2024-12-19; page explicitly warns tooling has evolved. Used for durable patterns, not current SDK details |
| S2 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | D1.4: coordination, parallel exploration, evaluation and cost considerations | Opened 2026-09-24 | Production case study, originally 2025-06-13; benchmark/speedup results not generalized or reproduced |
| S3 | [Models overview](https://platform.claude.com/docs/en/models/overview) | D2.1: model/platform capabilities and selection/migration reference | Opened 2026-09-24 | Redirected from `/docs/en/about-claude/models/overview`; dynamic documentation. Current model roster and prices deliberately not transcribed |
| S4 | [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | D2.5: prefix reuse, content order, write/read economics | Opened 2026-09-24 | Dynamic API documentation; target platform, minimum cacheable size, duration, pricing and support need deployment-time checks |
| S5 | [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) | D2.2: establish evaluation criteria; not every problem is a prompt problem | Opened 2026-09-24 | Official overview linking living best practices and tutorials |
| S6 | [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | D2.2–D2.3: clear instructions, examples, structure, model-specific thinking guidance | Opened; inspected thinking section 2026-09-24 | Dynamic model-specific behavior; no universal thinking parameter or historical budget copied into teaching code |
| S7 | [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) | D2.4–D2.5: context includes request/output components; cached prefixes still occupy context | Opened; inspected accounting section 2026-09-24 | Model-specific accounting and overflow behavior; limits intentionally not memorization targets |
| S8 | [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | D2.5: packaged resources, progressive loading, runtime requirements | Opened; inspected progressive-disclosure section 2026-09-24 | Product/runtime support differs; no assertion that a plain API request automatically consumes filesystem Skills |
| S9 | [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | D3.5–D3.6: contextual chunk enrichment, lexical+semantic retrieval, reranking | Opened 2026-09-24 | Engineering experiment, originally 2024-09-19; empirical results depend on corpus, embedding model and configuration |
| S10 | [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) | D3.1, D3.8: tool catalog overhead, discovery, latency/context trade-off | Opened 2026-09-24 | Original 2025-11-24 release describes beta features; module uses design mechanism, not release-era availability or benchmark percentages |
| S11 | [MCP authorization, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) | D3.2: HTTP authorization, intended-recipient validation, resource parameter, separate upstream credentials | Opened; inspected audience section 2026-09-24 | Versioned normative spec. Does not replace downstream object-level authorization design |
| S12 | [MCP security best practices, 2025-11-25](https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices) | D3.2: token passthrough prohibition and confused-deputy concerns | Opened; inspected passthrough section 2026-09-24 | Redirected from specification security-best-practices path; scoped to cited version |
| S13 | [MCP transports, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) | D3.7: stdio and Streamable HTTP | Opened; inspected stdio section 2026-09-24 | Version-specific; transport support must be negotiated with implementation |
| S14 | [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/) | D3.4: complementary traces, metrics and logs | Opened; inspected definitions 2026-09-24 | Official project documentation; course's AI trace schema and sampling policy are recommendations, not an OTel compliance claim |
| S15 | [A2A core concepts](https://a2a-protocol.org/latest/topics/key-concepts/) | D3.7: Agent Cards, task lifecycle, messages and artifacts | Opened; inspected Agent Card section 2026-09-24 | Official project documentation on mutable `latest` path; protocol example, not blueprint-specific requirement |
| S16 | [Anthropic interactive prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Optional practice for D2.2–D2.3 | Opened 2026-09-24 | Official learning repository. Exercises not executed; check current model IDs and request parameters |
| S17 | [Claude cookbooks](https://github.com/anthropics/claude-cookbooks) | Optional implementation practice across D1–D3 | Opened 2026-09-24 | Redirected from `anthropic-cookbook`; examples are starting points, not validated solutions for a reader's deployment |

## Findings and architectural synthesis

**Domain 1.** The evidence supports distinguishing control-flow choices from model capability and adding autonomy only for a task that needs adaptive steps. The module extends that source vocabulary with original architecture exercises: explicit state, action reconciliation, dependency contracts, review boundaries, and business-value calculations. These recommendations are engineering synthesis, not claims that Anthropic mandates one reference architecture.

**Domain 2.** Official documentation is deliberately living and model-specific. Teach evaluation-driven choice, output/evidence validation, context budgeting, and reuse mechanisms rather than a frozen model comparison. Prompt caching, modular templates, Skills, and application result caches are distinct. Native thinking behavior should be checked per model; no universal API snippet was included. The tutorial and cookbook offer practical learning material but are not official certification preparation guarantees.

**Domain 3.** Tool discovery is a context optimization, not permission enforcement. The MCP source provides strong normative evidence for intended-recipient checks and against token passthrough. RAG quality requires separately examining ingestion, retrieval, packing and generation. OpenTelemetry's signal taxonomy supports the monitoring vocabulary; specific spans, sampling choices and retention recommendations are course synthesis. A2A illustrates task delegation while direct APIs/CLIs and MCP address different integration needs.

## Prep-material sequence

1. **Domain 1:** Read S1 for pattern vocabulary, then S2 for a concrete multi-agent case. Sketch a simpler single-call/workflow alternative before accepting multi-agent complexity.
2. **Domain 2:** Work selected S16 exercises, then consult S5–S8 against the selected current model. Use S3–S4 to turn prompt quality into an actual cost/context experiment.
3. **Domain 3:** Read S9 and build a labeled retrieval set; compare S10's discovery mechanism with a small eager toolset. Read S11–S13 before proposing remote MCP security, and S14–S15 for observability/delegation contracts.
4. **Hands-on integration:** Select a relevant S17 recipe and adapt it to the lab constraints. Record version changes and actual measurements; do not assume repository examples are production-ready.

## Coverage and limitations

| Domain | Objectives taught explicitly | Questions | Practical output |
|---|---|---|---|
| 1 | D1.1–D1.6 | 6 original, including two select-two items | Decision brief, full flow, dependency graph, failure table, ADR |
| 2 | D2.1–D2.5 | 6 original, including two select-two items | Controlled model/prompt/context comparison with cache and compaction analysis |
| 3 | D3.1–D3.8 | 6 original, including two select-two items | Permissioned RAG integration and monitoring/discovery comparison |

No paid preparation products, exam dumps, leaked questions, or third-party claims of certification equivalence were used. Source pages were read, but external labs, repositories and API examples were not executed. Learner lab instructions distinguish unmeasured from measured runtime results. Real latency/cost/quality benefits require workload experiments. No production configuration or actual compliance certification is implied.

Review status at researcher handoff: researched and authored; independent reviewer, validator and adversarial reviewer sign-off is owned by the parent workflow and should not be inferred from this record.
