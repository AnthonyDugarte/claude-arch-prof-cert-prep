# Advanced decision practice

These 14 original items emphasize plausible competing architectures. They supplement the module questions; they are not a calibrated exam simulation. Select the stated number before reading the key. Facts and mechanisms are explained and sourced in the linked modules; all scenario measurements are hypothetical.

## Questions

**A1 · D1 · Select ONE.** An insurer uses a fixed six-step intake process. Some submissions need unpredictable external investigation, but these are only 3% of cases and a specialist currently handles them. A workflow meets the quality/latency target for the other 97%. Which next architecture experiment best matches the evidence?

A. Replace all six steps with a planning agent so every case shares one flexible execution model.  
B. Keep the workflow, measure the specialist cases, and test a bounded investigation agent on that slice against specialist outcomes.  
C. Add a separate agent to every step and use a supervisor to approve each transition.  
D. Keep human investigation permanently because a fixed workflow already meets the majority target.

**A2 · D1 · Select TWO.** A research service can decompose a request into five independent evidence searches. A single agent meets quality but misses the latency target. A parallel prototype is faster but contradicts itself in the final report. Which two improvements make the comparison decision-worthy?

A. Give each worker a bounded evidence contract with source IDs and an explicit synthesis/conflict-resolution stage.  
B. Report only time to the first worker result because it best demonstrates parallel speed.  
C. Compare complete-task correctness, final latency and total cost under the same workload and failure budget.  
D. Give each worker the entire conversation and all tools to eliminate handoff constraints.  
E. Accept the prototype once most workers agree, since independent execution makes errors independent.

**A3 · D2 · Select ONE.** A service analyzes one approved 40-page manual for cross-section contradictions. The release gates are at least 98% correct and p95 under 6 seconds. On representative held-out cases, full context with measured cache hits scores 99%, 5 seconds, $0.025 per request; hybrid retrieval scores 95%, 3 seconds, $0.010; hybrid plus reranking scores 99%, 8 seconds, $0.018. All users may access the manual, and context limits are satisfied. Which initial release is supported by these measurements?

A. Release hybrid retrieval because its lower cost leaves room for later quality tuning.  
B. Release the measured full-context cached path, monitor cache misses and end-to-end gates, and reassess as corpus size or permissions change.  
C. Release hybrid plus reranking because it meets the quality target and has lower variable cost.  
D. Route exception-heavy requests to reranking, assuming a new classifier will eliminate the measured tail delay.

**A4 · D2 · Select TWO.** A cheaper-model cascade saves money on routine extraction. On ambiguous cases the second pass raises p95 latency beyond the SLA; escalation currently depends only on the first model saying it is unsure. Which two experiments are best justified?

A. Send difficult task classes directly to a capable model using a validated router, and measure routing mistakes.  
B. Increase the first model's instructed confidence so fewer requests escalate.  
C. Compare the cascade with one capable model on cost per accepted outcome, missed escalations and end-to-end tail latency.  
D. Cache all users' prior final answers by question text without identity or version keys.  
E. Evaluate only average latency because p95 exaggerates uncommon cases.

**A5 · D3 · Select ONE.** One internal application uses three stable read-only endpoints through an existing audited API gateway. Two other teams may adopt the same data next year. The release is in two weeks, and no MCP service exists. What is the most defensible current decision?

A. Invest the remaining two weeks in an MCP server so future clients get discovery, even though this adds a new service to secure and operate.  
B. Use the audited API with a narrow adapter, document the contract, and revisit MCP when shared client demand makes the reuse worth its operations cost.  
C. Build a queue-backed read service so API retries can be processed asynchronously, adding a new persistence and worker layer.  
D. Build both direct and MCP paths now to preserve protocol flexibility, including contract tests and monitoring for each.

**A6 · D3 · Select TWO.** A hybrid retriever improves paraphrase recall, but after a document refresh some answers cite revoked tenant contracts. Both vector similarity and reranker scores are high. Which two actions address the observed failure most directly?

A. Trace source/ACL versions through ingestion, index update, caches and citation resolution.  
B. Increase top-k so more revoked and current passages compete.  
C. Enforce current tenant entitlements and document validity at retrieval/use boundaries and test revocation propagation.  
D. Move from hybrid search to lexical-only search because lexical scores encode authorization.  
E. Train the reranker on more paraphrases before checking ingestion state.

**A7 · D4 · Select ONE.** An LLM judge reports that prompt B beats A by 8 points, while blinded specialists report no improvement. B produces longer, more polished answers; the judge's rubric never defines factual correctness. What is the strongest next step?

A. Run a large online A/B test immediately, using the same judge score as the primary quality metric.  
B. Use exact-match answers for all questions to obtain a deterministic score before repeating the comparison.  
C. Calibrate a source-grounded rubric against adjudicated labels, blind/pair the comparison and rerun before choosing a winner.  
D. Increase the number of judge trials and select the prompt with the tighter confidence interval.

**A8 · D4 · Select TWO.** A release halves inference cost per request but doubles the rework rate. Its experiment dashboard excludes retries, fallbacks and abandoned sessions. Which two changes improve the release decision?

A. Count total cost and successful business outcomes for all assigned eligible traffic, including fallback/rework.  
B. Keep inference cost as the only metric because it is easiest to attribute.  
C. Apply prespecified quality and safety gates, inspect affected slices, and estimate uncertainty before expanding traffic.  
D. Remove abandoned sessions from both variants because they have no final answer to grade.  
E. Shift assignments every turn to balance the number of calls exactly.

**A9 · D5 · Select ONE.** A refund capability is genuinely required. Policy allows agents to propose refunds, requires human approval above a threshold, and requires account-level authorization for every refund. Which design best preserves useful automation and the policy?

A. Remove refunds entirely because least privilege always means read-only.  
B. Let the model determine authorization from the conversation and request confirmation above the threshold.  
C. Expose a narrow proposal operation; the executor independently checks current account entitlement and limits, binds any required approval to exact parameters, and prevents duplicate execution.  
D. Keep a general finance API and audit every call after execution.

**A10 · D5 · Select TWO.** A high-impact benefits workflow requires a human decision before denial. The team proposes “human in the loop,” but reviewers see only the recommendation and the queue is already over capacity. Which two changes address the control's actual weakness?

A. Provide relevant evidence, contradictory records, policy version and an effective reject/edit/escalate path.  
B. Auto-approve after two minutes to retain the promised latency.  
C. Reduce rollout or scope to available review capacity and define a safe timeout that preserves the human decision requirement.  
D. Add a disclaimer that the model might be wrong, keeping the interface unchanged.  
E. Route only on the model's uncalibrated confidence because it knows when it is uncertain.

**A11 · D6 · Select ONE.** Sales promises a two-second “response SLA.” Engineering measures first token; users care about a completed verified answer, which takes seven seconds. All teams claim their metric is correct. What should the architect do first?

A. Optimize first-token latency and keep the wording because a response has technically begun.  
B. Define the user-visible event, workload, percentile/window, dependencies and remedy with stakeholders, then test feasible targets before committing.  
C. Accept seven seconds as the new contractual SLA because it matches current implementation.  
D. Use provider availability as the response metric to simplify measurement.

**A12 · D6 · Select TWO.** A solution passes acceptance tests but only its architect knows how to rotate a tool credential, reindex safely or revert a prompt. The architect leaves next week. Which two actions best address lifecycle risk?

A. Record dependency/version compatibility, procedures, accountable owners and rollback conditions.  
B. Ask the model to generate documentation and treat generation as successful handoff.  
C. Have the receiving team perform a controlled recovery exercise from the runbook, then fix observed gaps.  
D. Freeze all updates indefinitely so no operational knowledge is needed.  
E. Add a more detailed architecture diagram without testing operator tasks.

**A13 · D7 · Select ONE.** A repository denies the file-reading tool access to `.env`, but a permitted test script can spawn a shell that reads it. The requirement is that the assistant cannot access production credentials. What change best meets the requirement?

A. Add reviewed PreToolUse checks for common secret-file paths and keep the current process credentials.  
B. Run all test scripts inside a container that mounts the full developer home directory so dependencies and credentials remain available.  
C. Remove production credentials from the assistant's environment, use scoped test credentials and an enforced process/filesystem boundary, then test all permitted access paths.  
D. Scan tool output for known secret patterns and block final responses containing matches, retaining current process access.

**A14 · D7 · Select TWO.** A coding pilot doubles lines generated but increases review time and escaped defects. Developers value exploration help, while broad autonomous edits perform poorly. What next iteration is best supported?

A. Keep broad autonomy because generated output measures adoption success.  
B. Focus the next pilot on bounded exploration and small verified changes with acceptance criteria and human diff review.  
C. Compare cycle time, rework, defects, cost and user experience on comparable tasks against a baseline.  
D. Disable tests temporarily to isolate raw generation speed.  
E. Require all teams to adopt the current workflow so the sample grows faster.

## Answer key and defenses

**A1: B.** [D1](01-solution-design.md) favors evidence-based decomposition. B preserves the working path and tests uncertainty where it exists. A expands risk without evidence; C adds coordination everywhere; D treats an initial choice as permanent. Reconsider broader agents if task variability expands and measured outcomes justify it.

**A2: A, C.** A makes evidence transfer and conflicts inspectable; C measures the user's completed task. B excludes synthesis; D adds context/authority without ensuring correctness; E assumes correlated models and sources fail independently. Parallelism pays only when its complete path improves the constrained outcome.

**A3: B.** [D2](02-models-prompts-context.md) compares context strategies by actual evidence needs. B is the only measured candidate meeting both hard gates. A misses the quality gate; C misses latency; D is a plausible next experiment but its classifier and critical path have no evidence yet. Retrieval becomes attractive when scale, updates or permissions make full context unsuitable.

**A4: A, C.** A can remove a predictable second pass on hard classes; C tests whether cascade complexity pays. B manipulates a signal without improving reliability; D risks stale/cross-user answers; E ignores a hard tail constraint. Neither A nor C guarantees a win without workload evidence.

**A5: B.** [D3](03-integration.md) treats protocols as integration choices. B exploits the existing audited path and preserves an adapter seam. A could pay off with established shared-client demand but adds unproven delivery and operations work now; C fits asynchronous work if synchronous dependencies are inadequate, which the stem does not establish; D preserves options at the cost of duplicating release/monitoring work. Shared demand may later justify MCP.

**A6: A, C.** A localizes freshness and propagation; C enforces data authority regardless of ranking. B can increase exposure; D mistakes relevance for authorization; E targets relevance despite evidence of a validity failure. A relevant source can still be revoked or unauthorized.

**A7: C.** [D4](04-evaluation-optimization.md) requires a grader that measures the intended outcome. C investigates disagreement and style bias. A exposes users while retaining the suspect metric; B can fit exact structured tasks but loses valid semantic answers here; D reduces sampling noise without correcting construct/style bias.

**A8: A, C.** A restores the real denominator and economics; C protects the required outcome and exposes subgroup regressions. B hides downstream cost; D excludes adverse outcomes; E contaminates repeated-session comparisons. A cheaper call is not necessarily a cheaper completed task.

**A9: C.** [D5](05-governance-safety.md) limits necessary capability rather than banning all useful actions. C separates proposal from authorization and exact execution. A violates business scope; B trusts model interpretation as authority; D detects harm after a broad capability already acted. Approval must not be reusable for altered parameters.

**A10: A, C.** A equips the human to decide; C makes required oversight feasible. B violates the policy; D does not supply evidence or capacity; E uses an unvalidated signal for consequential routing. If the human gate cannot be staffed, renegotiate scope or latency rather than silently bypass it.

**A11: B.** [D6](06-stakeholders-lifecycle.md) converts vague promises into measurable agreements. A exploits ambiguity; C unilaterally rewrites the contract; D substitutes a dependency measure for the user's outcome. Separate internal targets from contractual commitments and document who accepts the tradeoff.

**A12: A, C.** A captures operational ownership and compatibility; C proves the receiving team can use it. B produces unverified text; D blocks necessary lifecycle work; E may help understanding but does not demonstrate recovery capability.

**A13: C.** [D7](07-developer-enablement.md) distinguishes application permission rules from OS/process isolation. C addresses the real credential boundary. A can catch known commands but arbitrary subprocess behavior remains; B keeps credentials inside the container boundary; D detects some disclosures after the process has accessed secrets and may miss transformed values. Test subprocess and integration access as well as direct reads.

**A14: B, C.** B narrows the workflow to the observed strength while keeping verification; C measures useful delivery. A substitutes activity for outcome; D removes quality evidence; E scales the known failure. Broad autonomous work can be reconsidered when bounded trials show acceptable quality.
