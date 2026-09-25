# Domain 4 — Evaluation, Testing & Optimization

**Blueprint weight:** 16%. **Objectives:** D4.1 define evaluation metrics; D4.2 design datasets and mixed-method tests; D4.3 conduct A/B tests and iterate; D4.4 diagnose prompt failures, hallucinations, and model mismatch; D4.5 optimize tokens, latency, and cost-performance; D4.6 monitor performance with logging and observability. This module teaches architectural decisions, not a particular model release or an official exam item bank. The six practice questions below are original.

## The operating model

An evaluation, or *eval*, supplies a task, runs the system, and grades an outcome. For an agent, a *trial* is one attempt; a *trace* records messages, tool calls, intermediate results, and final output. Repeated trials matter because output and tool paths can vary. Anthropic recommends combining code-based, model-based, and human graders, then using production monitoring and A/B tests to fill the gaps left by offline suites. [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). A test of the Claude call alone misses retrieval, authorization, external tools, formatting, and the downstream action. The unit of evaluation should be the user task and its final state.

**Scenario:** A claims assistant answers from a policy archive and drafts a disposition for an adjuster. The sponsor asks for “95% accuracy.” An architect should first ask whether the target concerns retrieved passages, factual statements, final dispositions, or all three. A correct answer retrieved from a superseded policy is a system failure even if the wording looks plausible. Define a measurable outcome, the population on which it applies, the label owner, and a release threshold before prompt tuning. Anthropic's guidance similarly starts with specific, measurable success criteria. [Claude Platform, “Define success criteria and build evaluations”](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests).

## D4.1 — Metrics form a decision contract

Specify a **quality vector**, not one blended score. For the claims assistant, useful dimensions are: answer correctness against an adjudicated reference; groundedness (claims supported by retrieved evidence); retrieval recall at *k* on known relevant passages; citation correctness; task completion; unsafe-action rate; sensitive-data disclosure rate; p50/p95 end-to-end latency; cost per *resolved* claim; and human override rate. Distinguish a low unsafe-action rate from safety coverage: a system may simply refuse legitimate work. Define the denominator and exclusions for every rate. Segment by policy version, document language, claim type, and customer cohort so a good average does not hide a bad subgroup. These are recommended design metrics; the blueprint names accuracy, latency, cost, safety, and security without prescribing numeric pass marks.

An example release gate is: at least 98% correct citations on sampled eligible answers, zero unauthorized write actions in the adversarial suite, p95 latency under the team's agreed limit, and no material quality regression in any high-volume segment. Those values are **illustrative**, not Anthropic thresholds. Separate *hard constraints* (security or required policy controls) from goals that may trade against one another. For example, dollars per request can fall while dollars per successful task rise if a cheaper configuration increases retries. Anthropic's agent-evaluation account explicitly recommends measuring end-state outcomes and traces for multi-step agents. [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

| Metric choice | Strongest use | Blind spot; alternative wins when… |
|---|---|---|
| Exact match or deterministic assertion | Structured fields, tool permissions, transaction state | Paraphrase is legitimate; use rubric or expert review. |
| Retrieval recall / citation check | RAG coverage and provenance | Retrieved evidence can be obsolete or misread; check version and groundedness. |
| LLM rubric score | Nuanced answer quality at scale | Judge can be biased or inconsistent; calibrate against blinded human labels. |
| Human expert adjudication | High-stakes or subjective decisions | Slow and costly; deterministic checks win for unambiguous constraints. |
| Latency and cost per successful task | Production economics | Can reward shortcutting; keep quality and safety gates separate. |

## D4.2 — Build a dataset that can detect the failures you care about

An eval case should contain input, relevant context snapshot or fixture, expected end state, grading rule, risk tags, and provenance. Use a **development set** to debug; hold out a separate **validation set** for promotion. Seed both with realistic production samples, then deliberately add rare but consequential cases: missing evidence, contradictory documents, stale policies, multilingual input, ambiguous requests, malformed tool responses, and adversarial retrieved text. Keep sensitive production data out of test artifacts unless approved controls apply. Version the prompts, model identifier, tool schema, retrieval corpus, grader, and labels so a score change can be explained. Refresh cases when the product or source corpus changes; otherwise a static benchmark gradually loses relevance.

Mix grading methods. Code can assert that a refund was never issued or a JSON schema validates. An expert can judge whether an explanation is appropriate. A model judge can apply a written rubric to hundreds of answers, but first compare its ratings with independently labeled examples and inspect disagreements. Anthropic identifies code grading as scalable for objective checks, human grading as flexible but costly, and LLM grading as useful for complex judgments after reliability is tested. [Claude Platform, “Define success criteria and build evaluations”](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests); [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). Run more than one trial for stochastic agent paths. Preserve traces for failure diagnosis while applying a retention and redaction policy to their content.

## D4.3 — A/B testing and iteration

An offline improvement is a candidate for a live experiment, not proof of user benefit. In an A/B test, assign comparable eligible traffic to baseline and candidate at a stable unit (often account or user for repeated sessions), keep assignment sticky, and prespecify the primary outcome, guardrail metrics, duration, and rollback trigger. Check sample size with the team responsible for experiment analysis. Compare **intention-to-treat** outcomes so retries and fallbacks remain visible. Use a staged rollout for a consequential change, with independent monitoring of security and complaint rates. Anthropic describes A/B tests as a way to validate significant changes once traffic is sufficient, alongside offline evals, production monitoring, and transcript review. [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

If traffic is too low, a paired offline comparison with blinded expert review or a shadow run may be more informative. A shadow run can evaluate outputs without allowing actions; it will not fully measure user behavior. For a prompt update, change one major variable at a time, examine failures by slice, add new regressions to the suite, and only then evaluate the next candidate. Do not choose the winner from a single favorable aggregate metric when a hard safety gate regressed.

## D4.4 — Diagnose before changing the model

Use the **first failing boundary**. For each bad answer, inspect the user request, retrieval query, top passages and version stamps, context actually sent, tool calls/results, `stop_reason`, and final output. A sudden confident error after a document refresh, with stable model and latency, points first to ingestion, indexing, or retrieval. That is also the inference behind the guide's Domain 4 sample question. [Exam guide, §8](../claude-arch-professional-guide.md) is the supplied blueprint; [Claude Platform, “Reduce hallucinations”](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) documents that model answers can be incorrect even when fluent.

| Symptom | First checks | When a different intervention wins |
|---|---|---|
| Missing fact or stale citation | Source freshness, index job, chunk mapping, permissions, top-*k* | If good evidence reached the prompt but was ignored, revise prompt/context or model. |
| Unsupported claim with correct retrieval | Grounding instruction, contradictory context, abstention behavior | If the task exceeds capability across many prompt variants, test a stronger model. |
| Truncated answer | `stop_reason=max_tokens`, output cap, context size | If complete but wrong, increasing output cap wastes cost. |
| Wrong tool action | Tool description, authorization, routing, trace | If API rejected a valid call, repair integration and error handling. |
| Slow tail | Retrieval/tool timings, rate limits, output length, cache hits | A smaller model helps only if quality and tail latency improve on the same tasks. |

The Messages API reports `stop_reason`, including `max_tokens` for output truncation and `tool_use` when Claude requests a tool; API errors carry types and request IDs that aid debugging. [Claude Platform, “Stop reasons and fallback”](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons); [Claude Platform, “Claude API errors”](https://platform.claude.com/docs/en/api/errors). These fields are signals, not a substitute for the end-to-end trace. For hallucinations, allow an explicit “insufficient evidence” path, require source-linked claims where suitable, and verify citations. A fluent answer is not a grounding test.

## D4.5 — Optimize the quality-cost-latency frontier

Start from cost **per successful task** and p95 user-visible latency. Break latency into queueing, retrieval, model time to first token, output generation, tools, and retries. Break token cost into ordinary input, cache writes, cache reads, output, and repeated agent turns. Count total input correctly when cached content is present: `input_tokens` alone may exclude cached prefix tokens; include cache creation and read fields. [Claude Platform, “Rate limits”](https://platform.claude.com/docs/en/api/rate-limits). Anthropic's current optimization guide describes prompt caching, token hygiene, batch processing, model choice, effort, and task budgets, with batch processing trading response time for lower cost. Its measured savings are workload-specific, so benchmark your own distribution. [Claude Platform, “Optimizing for cost and intelligence”](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence).

| Lever | Likely gain | Cost or failure mode | Choose it when… |
|---|---|---|---|
| Cache stable prefix | Less repeated processing and lower cost | Changing early prompt/tool bytes breaks cache; short sessions may save little | Long common instructions or repeated context recur. |
| Trim irrelevant context | Lower tokens and sometimes faster answers | May remove decisive evidence | Retrieval quality is measured and lossless selection is feasible. |
| Smaller/faster model or lower effort | Lower unit cost/latency | Complex cases may fail and raise retries | Slice-level quality clears gates. |
| Batch asynchronous work | Lower cost | Completion is delayed | No interactive SLA applies. |
| Cap steps/output | Bounded tail and spend | Premature stop or poor answer | The cap is validated against hard cases. |
| More capable model for escalation | Higher success on hard cases | Higher per-call cost | Routing identifies hard cases accurately. |

Prompt caching works on a matching prefix; keep stable tool and system material before dynamic request content, then inspect cache read/write counters. A cache hit lowers processing cost but does not remove those tokens from the model's context or cure irrelevant context. [Claude Platform, “Prompt caching”](https://platform.claude.com/docs/en/build-with-claude/prompt-caching); [Claude Platform, “Manage tool context”](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context). Avoid memorizing prices or model rankings for the exam: they change; the architectural question is which lever preserves task quality under the actual workload.

## D4.6 — Monitoring closes the loop

Emit a trace ID and capture versioned configuration, model, prompt hash, document/index version, tool names and status, API request ID, stop reason, token usage by category, elapsed times by stage, cost estimate, final disposition, and user correction or escalation. Restrict access and redact payloads according to data classification; observing quality does not require unrestricted raw conversation storage. Aggregate dashboards should show error and timeout rates, p50/p95 latency, cost per successful task, cache-hit ratio, retrieval freshness, groundedness samples, and safety/authorization incidents. Use alerts for actionable shifts, then sample traces to understand them. Anthropic's research-system write-up describes monitoring agent decision patterns without reading individual conversation contents, an example of privacy-aware observability. [Anthropic, “How we built our multi-agent research system”](https://www.anthropic.com/engineering/multi-agent-research-system).

Assign an owner and response path to each alert: pause a bad index, roll back a prompt, disable a tool, or route cases to humans. Re-evaluate after a document, prompt, model, or tool change. Production monitoring detects drift and unanticipated failures that an offline suite cannot contain; user feedback and periodic human review supply further evidence. [Anthropic, “Demystifying evals for AI agents”](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

## Practical lab — Diagnose a policy-refresh regression

**Construct the fixtures:** create a synthetic 60-case claims set with labels and policy-version stamps, two small index snapshots (before and after refresh), and paired request traces. These are learner-created artifacts, not supplied datasets. Use 40 ordinary cases, ten cases whose refreshed retrieval incorrectly returns superseded policy, five missing-evidence cases, and five conflicting-policy cases. Within the ordinary cases inject two output truncations and two tool errors to distinguish other causes. Keep baseline and refreshed prompt/model versions fixed. Use deterministic stub outputs or optional real API calls; label synthetic timing and usage as simulated.

For each case record `case_id`, `split`, `expected_behavior`, `authorized_current_source_ids`, `before_retrieved_ids`, `after_retrieved_ids`, `answer_citations`, `stage_ms`, `usage`, `stop_reason`, and `tool_status`. A minimal example: case `stale-01` expects approved `policy-v2:section-4`; baseline retrieves that source, refreshed retrieval returns revoked `policy-v1:section-4`, and the generated answer cites v1. The expected diagnosis is source/index freshness, not insufficient output length. For `missing-01`, neither snapshot contains evidence and correct behavior is abstention. For a truncation case, current evidence is present but the output ends with `stop_reason=max_tokens`. Preserve a construction manifest so a peer can reproduce each injected failure.

1. Write a metric sheet: numerator, denominator, slices, and release gate for correctness, citation validity, abstention, unauthorized action, p95 latency, and cost per resolved task. Mark example thresholds as local design choices.
2. Partition cases into development and held-out validation sets; include at least one rare failure type in each. Add code assertions for citation IDs/version and tool permission, plus a rubric and five expert calibration labels for nuanced answers.
3. Compare baseline and refreshed index with the same prompt/model. Inspect the first failing boundary for every new error. Produce a table of retrieval failure, generation failure, truncation, and integration failure counts with trace IDs.
4. Propose a fix, rerun the paired suite, and design a live A/B or shadow experiment with guardrails and rollback conditions. Estimate token and stage latency effects.

**Acceptance criteria:** the report identifies stale retrieval as the cause where the trace supports it; distinguishes a missing-evidence abstention from a wrong answer; uses `stop_reason` to flag truncation; states why a bigger model alone would not repair a stale index; provides per-slice results and a held-out check; and includes a privacy-conscious telemetry plan. A reviewer can reproduce each conclusion from the learner-created trace IDs and fixture manifest.

## Original practice questions — not official exam content

**1. Select ONE.**

A policy assistant's citation accuracy falls after re-indexing. The prompt and model are unchanged. What is the best first investigation?

- **A.** Increase temperature.
- **B.** Inspect index version and retrieved passage IDs in failing traces.
- **C.** Increase `max_tokens`.
- **D.** Rewrite the system prompt.

**Answer: B.**

A changes variability without addressing the refresh boundary. B checks the component that changed and the evidence sent. C helps only if output was truncated. D might be needed later if correct evidence was present but ignored.

**2. Select TWO.**

A team wants a reliable pre-release evaluation for an agent that updates CRM records. Which two checks best cover task success and risk?

- **A.** Verify final CRM state with deterministic assertions.
- **B.** Grade only response tone with an LLM judge.
- **C.** Include multi-turn traces and repeated trials.
- **D.** Compare average response length only.

**Answers: A and C.**

A verifies actual outcome. B captures one quality dimension but misses state and authorization. C detects path variation and compounding tool errors. D is an efficiency measure, not task success.

**3. Select ONE.**

A team has a prespecified promotion gate forbidding an increase in unauthorized tool attempts. A candidate prompt improves offline rubric scores by 3 points but doubles those attempts, although the executor blocks them. What should the architect do?

- **A.** Release because quality rose.
- **B.** Block promotion under the security gate and diagnose attempted calls.
- **C.** Hide attempts by retrying.
- **D.** Switch the rubric judge.

**Answer: B.**

A ignores a hard constraint. B preserves the gate and investigates a concrete failure. C conceals risk and may increase it. D is justified only if calibration evidence shows judge error, which does not explain logged tool attempts.

**4. Select TWO.**

A common 12,000-token policy prefix is sent for each interactive request. Quality is stable; cost is high. Which two measurements or changes are most informative?

- **A.** Put changing timestamps before the policy.
- **B.** Cache the stable prefix and inspect cache-read/write usage.
- **C.** Measure cost per successful task and p95 latency after the change.
- **D.** Remove half the policy without testing.

**Answers: B and C.**

A breaks prefix reuse. B uses the documented mechanism and verifies hits. C checks business and user impact. D risks losing decisive rules.

**5. Select ONE.**

A completion ends mid-sentence and the API reports `stop_reason=max_tokens`. What is the first targeted correction?

- **A.** Raise or reallocate the output cap, then rerun the affected cases.
- **B.** Re-index documents.
- **C.** Remove citation checks.
- **D.** Increase sampling temperature.

**Answer: A.**

A addresses the observed stop condition and tests its cost. B concerns evidence retrieval. C weakens evaluation. D does not repair truncation.

**6. Select TWO.**

A/B traffic is enough for an experiment on a new retrieval strategy. Which practices support a credible decision?

- **A.** Prespecify primary metric and safety guardrails.
- **B.** Reassign each user to a fresh variant every turn.
- **C.** Keep assignment stable and compare eligible traffic including fallbacks.
- **D.** Stop as soon as one favorable hourly chart appears.

**Answers: A and C.**

A limits after-the-fact metric shopping and protects hard constraints. B contaminates repeated-session outcomes. C keeps exposure coherent and captures failures. D amplifies noise and selection bias.
