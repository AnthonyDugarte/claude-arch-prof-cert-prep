# Integrated capstone: a support copilot you can defend

This is an original design and implementation exercise spanning D1–D7. All business numbers below are **hypothetical exercise assumptions**, not Anthropic limits or universal production thresholds. Use the technical references in the seven modules when implementing. No live customer data or production side effects are required.

## Brief and constraints

A software vendor wants a copilot that reads support tickets, retrieves approved product documentation and tenant-specific contract terms, and drafts replies for support staff. It must never issue refunds or delete accounts. Contract terms change daily; common documentation changes weekly. Tenants must not see each other's contracts. Some tickets contain personal information and some attached documents contain hostile instructions.

The sponsor asks for 30% lower median handling time without a higher materially incorrect-reply rate. The operational target is a draft within 8 seconds at p95 under 20 concurrent requests. Drafts require a human send action; the assistant does not send messages. A provisional variable-cost ceiling is $0.04 per request for model calls plus variable retrieval/hosting. Human review and fixed infrastructure overhead are accounted separately in the business case. These are targets to test and negotiate, not assumed achievements.

Discovery establishes that 80% of tickets are routine questions, 15% require contract interpretation by trained support staff and 5% lack sufficient evidence. A read-only ticket API already exists. Finance owns refunds in a separate system. The knowledge team owns source approval; a platform team operates retrieval and identity. The service desk has a real staffing limit, so increasing escalation has a measurable queue cost.

## Required artifacts and evidence

| Deliverable | What it must contain | Blueprint |
|---|---|---|
| One-page discovery brief | Users, baseline, excluded actions, measurable success, assumptions, owner and stop condition | D1.1, D1.6, D6.1 |
| Architecture and three decision records | Workflow versus agent; model/context strategy; direct API versus MCP; credible rejected option and reconsideration trigger | D1.2–D1.5, D2, D3.7, D6.2 |
| Threat/data-flow sketch | Identity and tenant checks, source trust, ingestion, retrieval, tool execution, storage/log retention, reviewer boundary | D3.1–D3.2, D5 |
| Small working or explicitly simulated request path | Authorization → retrieval → evidence selection → draft → citation checks → human queue | D3, D7.2 |
| Evaluation pack | Synthetic fixtures, frozen splits, scoring rubric, repeated runs, slices, traces, failure localization, measured or explicitly simulated results | D4 |
| Release and handoff pack | Version manifest, limited rollout, rollback, alerts, runbook, owners, team configuration and change policy | D6.3–D6.5, D7.1–D7.3 |

A paper design is useful but does not establish operational readiness. If API access is unavailable, execute a deterministic stub that injects the listed failures and label those results **simulation**. Later substitute real model/retriever calls and repeat the evaluation before claiming measured quality, latency or cost. Writing a production application is not required to study this course; implementing the exercise strengthens the evidence for your own readiness.

## Build the smallest informative experiment

Create two tenants, two users with different entitlements, and approximately 20 synthetic documents. Include a revoked contract, two conflicting versions, an exact error identifier, a long table, a source containing “ignore previous instructions,” and a document belonging to the other tenant. Give each record tenant, source ID, version, effective date, approval state and ACL metadata. Define how deletions and permission changes invalidate derived chunks, caches and citations.

Prepare 30 learning cases and a separate 30-case held-out set. Within each set include routine answerable questions, missing-evidence questions, exact identifiers, multi-document questions, stale/version conflicts, injected instructions and forbidden tenant requests. Record expected authorized evidence and prohibited outcomes, not only ideal prose. This small pack tests the method; it is insufficient to establish a low production failure probability.

Compare two retrieval approaches on the same cases. A reasonable starting comparison is lexical retrieval versus hybrid lexical/vector retrieval with optional reranking. Measure authorized evidence recall, citation support, abstention quality, end-to-end latency and total variable cost. Change one component at a time during diagnosis. If reranking helps rare complex queries but breaks the common path latency target, evaluate routing with a measurable trigger instead of reranking everything.

Record cold and warm cache runs separately. Test policy updates, low cache reuse and model escalation rather than reporting only the most favorable warm path. Use the same representative workload and concurrency for alternatives. For nondeterministic outputs, repeat a subset and report variability. Keep tuning data separate from the held-out set; if you use held-out failures for tuning, create a fresh holdout for the next release decision.

## Challenge injections

| Injected condition | Evidence to inspect first | Minimum safe behavior |
|---|---|---|
| Correct document disappears after reindex | Index manifest, ingestion failure, filters, embedding/index versions | No invented answer; preserve previous valid index or abstain according to freshness policy |
| User guesses another tenant's document ID | Entitlement evaluation, tenant filter, downstream document access | Deny without returning document contents, embeddings-derived snippets or citation details |
| Tool timeout followed by retry | Trace spans, retry budget, deadline | Bounded retry within deadline; actionable fallback; no retry storm |
| Retrieved text asks the assistant to call a refund tool | Tool inventory, executor policy, model proposal | Refund capability absent; source content cannot grant authority |
| ACL revoked after retrieval but before draft delivery | Current authorization at use/delivery and cache invalidation | Do not disclose newly unauthorized evidence; re-evaluate or suppress draft |
| Model or prompt update improves average score but harms contract cases | Versioned, stratified evaluation results | Block rollout or restrict affected segment pending accepted remediation |
| Review queue exceeds capacity | Escalation arrival rate, reviewer throughput, oldest item age | Rate limit or reduce service scope; preserve human review requirement |
| Telemetry backend is unavailable | Local bounded buffers, failover and mandatory-audit policy | Apply explicit risk policy; mandatory-audit actions fail closed, permitted read-only service may degrade if policy allows |

For this exercise, buffer sensitive draft text until the delivery authorization check passes. Do not stream contract excerpts before that check. Test revocation against in-flight responses, stored conversation context, cached results and citation access as well as the retrieval index. Previously disclosed bytes cannot be recalled by invalidation. A streaming variant needs an explicit, tested policy for the delivery boundary and revocation behavior.

“Zero leaks observed” in a tiny test is an acceptance check for that test set, not proof that leakage is impossible. A red-team corpus, source review and ongoing monitoring address different failure classes.

## Worked design defense

**Architecture.** Start with a bounded workflow: authenticate, load authorized ticket, retrieve approved evidence, draft with citations, check schema/support, place in human review. The task graph and forbidden actions are known. A research agent becomes a candidate if investigations repeatedly require an unpredictable sequence of evidence-gathering steps and a bounded workflow demonstrably fails. Multi-agent parallelism is justified only if independent subtasks provide enough quality or latency benefit to offset additional calls and coordination errors.

**Integration.** Use the existing read-only API directly for one application if it already supplies the required identity and telemetry contract. Consider MCP when multiple clients need standardized capability discovery and reuse. Neither protocol choice supplies application authorization automatically. Keep tenant identity outside model control and enforce it in retrieval and execution services.

**Context.** Put stable task rules ahead of dynamic evidence when the chosen caching API supports the intended prefix. Use retrieved evidence for changing contracts rather than expecting model knowledge to be current. For a small, approved static manual, supplying the whole document may beat a complex retrieval stack; measure whether relevant evidence is lost in long inputs and include cache economics. Version all policy and source references.

**Model.** Select candidates by held-out task success and p95 latency, then compare cost per accepted outcome. Escalation to a more capable model can help hard synthesis but cannot fix missing evidence or denied access. Detect escalation conditions with validated signals—missing support, failed checks, task category—not the model's uncalibrated confidence alone. Any fallback model must independently meet the applicable safety requirements.

**Governance.** Human reviewers see the ticket, cited evidence, policy version, uncertainty and a clear approve/edit/reject action. Review is not a ritual click. Forbidden actions stay unavailable even after approval. Legal/security stakeholders assess applicable obligations and deployment contracts; selecting a cloud service does not itself establish compliance for the whole workflow.

**Business case.** Demonstrate the 30% handling-time change on comparable tasks and include correction/review time. Report satisfaction and error slices alongside median time. A faster draft with higher reviewer effort may be a net loss. Keep quality and security release gates even if the sponsor prefers a fast rollout.

## Worked calculations with explicit assumptions

Suppose 1,000 requests incur $18 model cost, $7 retrieval/hosting variable cost, and 900 accepted drafts. Variable cost per request is $25 / 1,000 = **$0.025**; per accepted draft it is $25 / 900 ≈ **$0.0278**. The first is under the provisional ceiling; the second exposes rejected work. If average human review is 30 seconds at an assumed $30/hour, review adds $0.25/request—ten times the infrastructure/model variable cost. These are fabricated arithmetic inputs, not estimates of real Claude pricing.

For cache analysis, let B be a repeated prefix's uncached cost, W its cache-write cost, R its cache-read cost and n the number of uses within the valid reuse period. Uncached prefix cost is nB; one write then hits costs W + (n−1)R. Caching is cheaper when n(B−R) > W−R, assuming eligibility and actual hits. Add dynamic input/output costs separately and use the current platform rates. Cache misses, version changes and expiry can invalidate this simple expected benefit.

Latency is a critical-path property: parallel retrieval branches contribute approximately the slower branch plus coordination overhead; serial steps add. Do not add individual component p95 values and call the result a measured end-to-end p95. Measure complete requests under the intended load, including retries and queuing.

## Acceptance rubric and oral defense

Score each area 0–2: 0 absent; 1 plausible explanation; 2 supported by an artifact and relevant test. Areas: requirement clarity; architecture alternatives; context/model choice; identity/tool boundaries; retrieval freshness; evaluation quality; risk/oversight; operational handoff. The maximum is 16. Before applying the total, require artifact-plus-test evidence (2/2) in identity/tool boundaries, retrieval freshness, evaluation quality and risk/oversight. The forbidden-action, cross-tenant, revocation and trace-backed diagnosis demonstrations are pass/fail prerequisites. Then require at least 12/16 overall as a suggested learning gate. A plausible explanation cannot substitute for a missing critical demonstration. This is **our instructional rubric**, not a certification cut score.

Demonstrate each forbidden action and cross-tenant request being blocked by deterministic controls. Show at least one diagnosed failure and a trace that supports the diagnosis. If measured quality or latency targets fail, report the failure and a justified next experiment; fabricated passing results do not satisfy the exercise.

Defend the design to a skeptical reviewer: What fact would make you choose an agent? Which control still works when the model follows a malicious document? What does the caller see when retrieval is unavailable? Who can roll back a bad policy/index/model combination? Which cost did your first estimate omit? What changes if autonomous sending becomes a real requirement? Answers should connect to evidence, owners and changed constraints.

## Annotated evidence example

Illustrative learner artifact, **simulated**, not a result obtained by this research team: case `revoked-contract-02` carries tenant A and source version 3; retrieval occurs at t0, authorization is revoked at t1, and the buffered draft reaches the delivery gate at t2. The gate denies disclosure and emits a metadata-only trace; the user sees a request for re-review. An assertion checks that no contract text or citation escaped. This earns evidence credit for that specific revocation test, not for the entire identity threat model.

A release record might then read: “Candidate B passes all supplied negative authorization tests, but measured p95 is 9.2 seconds against an 8-second target at the specified load. Do not promote. Owner: platform team. Next experiment: bypass reranking only for validated exact-identifier queries, retain the held-out quality and security gates, and rerun end-to-end latency.” The distinction between passing a security fixture and failing an operational target is the lesson; inventing a green aggregate score would hide the tradeoff.
