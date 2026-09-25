# Research Dossier — Domain 1: Solution Design & Architecture (17%)

Researcher deliverable. Exam: CCAR-P v1.0, effective July 2026 [D01-S01]. Research date: 2026-09-24.
Source table: `01-solution-design-sources.md`. Cite IDs inline.

---

## 0. Scope control

Domain 1 is **17% of 63 scored items ≈ 10–11 items** [D01-S01]. The six objectives are reproduced verbatim
in §1. Adjacent material that belongs to *other* domains and must not be over-taught here:

| Tempting topic | Actually belongs to |
|---|---|
| Chunking, embeddings, retrieval strategy detail | Domain 3 (RAG pipeline design) |
| MCP vs. API/CLI vs. agent-to-agent protocol choice | Domain 3 |
| Model selection *criteria* in depth, prompt caching mechanics | Domain 2 |
| Eval dataset construction, A/B testing, judge calibration | Domain 4 |
| Guardrail implementation, HITL as a *safety* control, GDPR/HIPAA | Domain 5 |
| SLA *negotiation* with stakeholders, documentation artifacts | Domain 6 |

Domain 1 owns the **shape of the system** and the **first architectural commitment**: which tier, which
pattern, how decomposed, where the loop closes, and which business value the shape is buying. Where a
Domain 1 item touches a neighbor's topic, it does so as a *design consequence*, not as mechanism.

---

## 1. Objectives (verbatim from the blueprint) [D01-S01]

1. Translate business problems into Claude-based AI solutions
2. Design end-to-end architectures (input → processing → output → feedback loops)
3. Select appropriate architectural patterns (workflow, agentic, augmented LLM)
4. Design multi-agent systems and orchestration strategies
5. Apply decomposition techniques for complex problem solving
6. Align solutions to business value pillars (efficiency, transformation, productivity, cost, performance SLAs)

Note the objective wording of #3 names the three tiers explicitly — *workflow, agentic, augmented LLM* —
which is the taxonomy of [D01-S02]. This is the strongest available signal that the exam's pattern
vocabulary is Anthropic's own "Building effective agents" vocabulary. Treat that article as the spine.

---

## 2. Concept inventory (precise definitions + alternatives)

| # | Concept | Definition (source-anchored) | Named alternatives |
|---|---|---|---|
| C1 | **Augmented LLM** | The baseline building block: an LLM "enhanced with augmentations such as retrieval, tools, and memory," where the model generates its own search queries, selects tools, and decides what to retain [D01-S02]. | Raw single call (no augmentation); workflow; agent |
| C2 | **Workflow** | "Systems where LLMs and tools are orchestrated through **predefined code paths**" [D01-S02]. Control of *what happens next* lives in your code. | Agent; augmented LLM |
| C3 | **Agent** | "Systems where LLMs **dynamically direct their own processes and tool usage**, maintaining control over how they accomplish tasks" [D01-S02]. Control of *what happens next* lives in the model. | Workflow; augmented LLM |
| C4 | **Prompt chaining** | Decomposes a task into a fixed sequence of steps, each LLM call processing the previous output; optional programmatic gates between steps [D01-S02]. | Single call with a longer prompt; routing; agent |
| C5 | **Routing** | Classifies an input and directs it to a specialized follow-up task [D01-S02]. | One prompt handling all classes; orchestrator-workers |
| C6 | **Parallelization — sectioning** | Breaking a task into independent subtasks run in parallel, then aggregating [D01-S02]. | Sequential chaining; orchestrator-workers |
| C7 | **Parallelization — voting** | Running the same task multiple times to get diverse outputs, then aggregating for confidence [D01-S02]. | Single pass; evaluator-optimizer |
| C8 | **Orchestrator-workers** | A central LLM "dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results"; the key difference from parallelization is that "subtasks aren't pre-defined, but determined by the orchestrator based on the specific input" [D01-S02]. | Parallelization (pre-defined split); routing; single agent |
| C9 | **Evaluator-optimizer** | One LLM call generates, another evaluates and gives feedback, in a loop [D01-S02]. Applies when "we have clear evaluation criteria, and when iterative refinement provides measurable value." | Single pass + offline eval; human review; voting |
| C10 | **Agent loop** | "gather context → take action → verify work → repeat" [D01-S06]. During execution the agent must "gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress" [D01-S02]. | Fixed pipeline; evaluator-optimizer |
| C11 | **Harness** | The loop around the model that calls Claude, routes tool calls, and manages context across one or many context windows [D01-S09]. Anthropic virtualizes it as three parts: **session** (append-only event log), **harness** (the loop), **sandbox** (execution environment) [D01-S09]. | Ad-hoc `while` loop; Tool Runner; Agent SDK; Managed Agents |
| C12 | **Context engineering** | "The set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference," the successor discipline to prompt engineering [D01-S05]. | Monolithic context; naive RAG |
| C13 | **Context rot / attention budget** | "As the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases"; transformers create "n² pairwise relationships for n tokens," producing "a performance gradient rather than a hard cliff" [D01-S05]. | — (a constraint, not a choice) |
| C14 | **Context isolation (subagent)** | A subagent runs in its own conversation; "intermediate tool calls and results stay inside the subagent; only its final message returns to the parent" [D01-S19]; typical returned summary is 1,000–2,000 tokens [D01-S05]. | Single shared context; compaction; note-taking |
| C15 | **Context-centric decomposition** | "Adopt a context-centric view rather than a problem-centric view when decomposing work"; e.g. "An agent handling a feature should also handle its tests, because it already possesses the necessary context" [D01-S04]. | Problem-centric split (writer / tester / reviewer) |
| C16 | **Compaction** | Summarizing a conversation nearing the context limit and reinitiating a new window with the summary [D01-S05]. Server-side compaction is a Claude API beta [D01-S24]. | Context editing (clear, don't summarize); context reset; memory |
| C17 | **Structured note-taking / memory** | Notes persisted outside the context window and re-read later; "persistent memory with minimal overhead" [D01-S05]. Cross-session persistence, unlike editing/compaction which are within-session [D01-S25]. | Compaction; longer context |
| C18 | **Context reset + handoff artifact** | Clearing context entirely and starting a fresh agent from a structured artifact: "A reset provides a clean slate, at the cost of the handoff artifact having enough state for the next agent to pick up the work cleanly" [D01-S08]. | Compaction; single long run |
| C19 | **Tool decomposition** | Choosing the granularity of the action surface. Consolidate: implement `schedule_event` rather than `list_users` + `list_events` + `create_event` [D01-S11]. Promote an action from bash to a dedicated tool when you need to **gate, render, audit, or parallelize** it [D01-S25]. | Bash-only surface; one tool per API endpoint |
| C20 | **Execution mode** | Synchronous request/response, streaming (SSE, same request, incremental), asynchronous/queued (your own queue + callback), and Message Batches (Anthropic-side async, 50% cost, most batches < 1 hour, 24-hour expiry) [D01-S15][D01-S16]. | — |
| C21 | **Outcome vs. trajectory grading** | Grade the final environment state, not the path: "grade what the agent produced, not the path it took," because path-grading yields "overly brittle tests, as agents regularly find valid approaches" [D01-S10]. | Step-by-step trajectory scoring |
| C22 | **pass@k vs. pass^k** | pass@k = at least one of k attempts succeeds; pass^k = **all** k succeed, the right metric "for customer-facing agents where users expect reliable behavior every time" [D01-S10]. | Single-run accuracy |
| C23 | **Business value pillars** | The blueprint names five: efficiency, transformation, productivity, cost, performance SLAs [D01-S01]. Anthropic's enterprise framing splits use cases into "External, revenue-oriented" and "Internal, cost- and risk-oriented" [D01-S21], and separates efficiency (same work, faster/cheaper) from transformation (work that would not have happened at all — "27% of Claude-assisted work wouldn't have been done otherwise") [D01-S22]. | — |

---

## 3. Findings by objective

### Objective 1 — Translate business problems into Claude-based AI solutions

**Primary framework (Anthropic's own pilot-selection criteria) [D01-S21]:** the most suitable first
project should be:

- "**Well suited to LLM capabilities.** It should leverage core LLM strengths – such as processing
  unstructured data, content classification, or format transformation."
- "**Meaningful and measurable success metrics.** Don't just focus on technical performance. Look for use
  cases which directly impact key business indicators e.g. reduced processing time, increased throughput,
  or improved accuracy."
- "**Clear return on investment.**"
- "**Business critical, but low security risk.** Your first use case shouldn't carry extreme operational or
  security risks."
- "**Abundant data.** Do you have enough data to support the use case, and is it in the format needed, with
  permission to use it?"
- "**Minimal disruption to existing processes.** Consider parallel deployment—running AI-enhanced
  processes alongside existing workflows until performance and reliability are proven."
- "**Scalable and duplicable.**"

**Success-criteria rubric [D01-S21]:** Specific / Measurable / Aligned with business objectives / Time
bound. The document's worked examples are architecture-relevant because they are *thresholds*: "95%
accuracy in customer inquiry classification", "reduction in average resolution time from 45 to 30
minutes", "less than 0.1% of outputs flagged for bias across 10,000 interactions."

**Graduation criteria for pilot→scale [D01-S21]:** Performance thresholds (accuracy, speed/latency, cost
efficiencies); Operational readiness (system stability, support infrastructure, team capability); Risk
management infrastructure (security compliance, data protection, operational controls).

**Architectural translation rule (synthesis, grounded in D01-S02 + D01-S21):** a business problem becomes
an architecture through four questions in this order — (1) what is the *unit of work* and can you
enumerate its decision tree in advance? (2) what is the *cost of an error* and who absorbs it? (3) what is
the *latency budget* and is it per-request or per-batch? (4) which *value pillar* is the sponsor buying?
Answers 1–3 pick the tier and pattern; answer 4 picks the metric the architecture is optimized against.

**The "don't use an LLM for this step" rule.** Anthropic's own guidance is explicit that the best form of
feedback is "providing clearly defined rules for an output, then explaining which rules failed and why"
[D01-S06], and that code-based graders are preferred "when fast, cheap, and objective verification is
possible" [D01-S10]. The architectural corollary: any step that is a lookup, an arithmetic calculation, a
schema validation, a deterministic transform, an authorization check, or a regulated decision with a
published rule table should be code, not a model call. The model's job is the unstructured boundary —
reading the document, classifying the intent, drafting the language.

### Objective 2 — End-to-end architectures (input → processing → output → feedback loops)

**The canonical loop [D01-S06]:** "gather context → take action → verify work → repeat." Map it onto the
blueprint's four-stage phrasing:

| Blueprint stage | What it is architecturally | Primary-source anchors |
|---|---|---|
| Input | Ingress, normalization, routing, retrieval/context assembly, PII handling | just-in-time vs. pre-inference retrieval [D01-S05]; routing [D01-S02] |
| Processing | Tier + pattern choice; tool surface; model + effort; context strategy | [D01-S02][D01-S12][D01-S05] |
| Output | Format constraint, citation, confidence signal, action vs. recommendation | structured outputs, citations [D01-S24]; "grade what the agent produced" [D01-S10] |
| Feedback loops | Four distinct placements — see below | [D01-S06][D01-S08][D01-S10] |

**Four feedback-loop placements (this is the part candidates conflate):**

1. **Inline / in-loop verification.** The agent checks its own work against ground truth from the
   environment each step: tool results, test runs, linter output, compiler errors [D01-S02][D01-S06].
   Best form: rules-based. "The best form of feedback is providing clearly defined rules for an output,
   then explaining which rules failed and why" [D01-S06].
2. **Separate evaluator agent (in-run, out-of-context).** A distinct generator/evaluator split.
   "Separating the agent doing the work from the agent judging it proves to be a strong lever," because
   self-evaluating models "respond by confidently praising the work—even when, to a human observer, the
   quality is obviously mediocre" [D01-S08]. Verification subagents are cheap because "verification
   requires minimal context transfer by nature" [D01-S04] — but their dominant failure is "marking
   outputs as passing without thorough testing" [D01-S04].
3. **Offline evaluation.** Automated evals "enable faster iteration" and are "fully reproducible" without
   user impact; best pre-launch and in CI/CD [D01-S10]. Start with 20–50 realistic tasks drawn from
   actual failures [D01-S10]; the multi-agent team started with ~20 test cases [D01-S03].
4. **Production telemetry / human review.** Production monitoring "reveals real user behavior at scale"
   and "catches issues that synthetic evals miss," but is reactive — "problems reach users before you
   know about them" [D01-S10]. Offline and production are "complementary, not competing" [D01-S10].
   Human review is mandatory for grader calibration: "You won't know if your graders are working well
   unless you read the transcripts and grades from many trials" [D01-S10].

**Statefulness and recovery are part of the architecture, not an ops afterthought.** "Agents can run for
long periods of time, maintaining state across many tool calls… without effective mitigations, minor
system failures can be catastrophic"; the fix is resumption rather than restart [D01-S03]. Anthropic's
Managed Agents architecture makes this structural: the session is "the append-only log of everything that
happened," living "outside Claude's context window," so a failed harness reboots with `wake(sessionId)`
and resumes "from the last event" [D01-S09]. Deployment guidance: "rainbow deployments to avoid
disrupting running agents, by gradually shifting traffic from old to new versions while keeping both
running simultaneously" [D01-S03].

### Objective 3 — Select the architectural pattern (workflow / agentic / augmented LLM)

**The governing rule [D01-S02]:** "finding the simplest solution possible, and only increasing complexity
when needed. This might mean not building agentic systems at all." And: "you should consider adding
complexity only when it demonstrably improves outcomes."

**The discriminator, stated by Anthropic [D01-S02]:** "workflows offer predictability and consistency for
well-defined tasks, whereas agents are the better option when flexibility and model-driven
decision-making are needed at scale."

**The cost side [D01-S02]:** "Agentic systems often trade latency and cost for better task performance,
and you should consider when this tradeoff makes sense."

**Agents specifically [D01-S02]:** use them "for open-ended problems where it's difficult or impossible to
predict the required number of steps, and where you can't hardcode a fixed path," and only where "you must
have some level of trust in its decision-making." Risks: "higher costs, and the potential for compounding
errors."

**The four-criterion gate before building an agent [D01-S24]:** Complexity (multi-step and hard to specify
in advance), Value (outcome justifies higher cost and latency), Viability (Claude is capable at this task
type), Cost of error (errors can be caught and recovered — tests, review, rollback). "If the answer is
'no' to any of these, stay at a simpler tier."

**Pattern → signal map (compiled from [D01-S02]):**

| Pattern | Use when | Cost you accept |
|---|---|---|
| Augmented LLM (single call) | One well-specified transform over unstructured input | Ceiling on task complexity |
| Prompt chaining | "the task can be easily and cleanly decomposed into fixed subtasks"; "The main goal is to trade off latency for higher accuracy" | Serial latency = sum of steps |
| Routing | "distinct categories that are better handled separately, and where classification can be handled accurately" | One extra hop; misroute risk |
| Parallelization (sectioning) | "subtasks can be parallelized for speed" | N× tokens for 1× wall-clock |
| Parallelization (voting) | "multiple perspectives or attempts are needed for higher confidence results" | N× tokens; needs an aggregation rule |
| Orchestrator-workers | "complex tasks where you can't predict the subtasks needed" | Coordination tokens + non-determinism |
| Evaluator-optimizer | "clear evaluation criteria" + "iterative refinement provides measurable value"; specifically when a human's articulated feedback demonstrably improves the output and the LLM can produce that feedback | Unbounded loop risk; needs a stop condition |
| Autonomous agent | Can't enumerate the step count or the path; you trust the decisions; errors are recoverable | Highest cost/latency; compounding errors |

**Three implementation principles for agents [D01-S02]:** (1) maintain simplicity in design; (2) prioritize
transparency by explicitly showing the agent's planning steps; (3) carefully craft the agent-computer
interface (ACI) through thorough tool documentation and testing. Anthropic asks architects to invest as
much in the ACI as in HCI, and to "Poka-yoke your tools" — change arguments so mistakes are harder to make.

**Framework caution [D01-S02]:** "Frameworks can help you get started quickly, but don't hesitate to
reduce abstraction layers and build with basic components as you move to production."

**A newer, important corollary [D01-S08][D01-S09]:** "every component in a harness encodes an assumption
about what the model can't do on its own, and those assumptions are worth stress testing." When Opus 4.6
shipped with better planning and code review, previously necessary harness components "became overhead
candidates," and sprint decomposition was removed entirely from the V2 harness. Architecturally: the
correct amount of scaffolding is a function of the current model's capability, and it is expected to
*shrink* over time. This is a live exam-relevant judgment: the option that adds scaffolding a current
model no longer needs is a wrong answer dressed as diligence.

### Objective 4 — Multi-agent systems and orchestration strategies

**The three legitimate justifications [D01-S04]:**

1. **Context protection.** "Context accumulates information from one subtask that is irrelevant to
   subsequent subtasks." Example given: a support agent pulling order history while diagnosing a technical
   issue — "Order details add thousands of tokens that degrade reasoning about the technical problem."
2. **Parallelization.** "Running multiple agents in parallel allows you to explore a larger search space
   than a single agent can cover."
3. **Specialization.** Three signals: an agent with "20+" tools struggles with selection; tools spanning
   "multiple unrelated domains"; "Adding new tools degrades performance on existing tasks."

**The cost [D01-S04]:** "Multi-agent systems typically consume 3 to 10 times more tokens than single-agent
approaches," and they "often take longer overall than single-agent systems because of the sheer increase
in total computation." Overhead is not only tokens: "Every additional agent represents another potential
point of failure, another set of prompts to maintain, and another source of unexpected behavior."

**The measured upside, in the one domain where it clearly pays [D01-S03]:** "Multi-agent system with
Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by
90.2%" on an internal research eval. Token economics from the same post: agents use "about 4× more tokens
than chat interactions" and multi-agent systems "about 15× more tokens than chats"; "token usage by itself
explains 80% of the variance" in BrowseComp performance. Parallel subagents plus parallel tool calls "cut
research time by up to 90% for complex queries."

**Where it does not pay [D01-S03]:** "Most coding tasks involve fewer truly parallelizable tasks than
research, and LLM agents are not yet great at coordinating and delegating to other agents in real time";
unsuitable for "Domains that require all agents to share the same context or involve many dependencies
between agents."

**Decomposition boundary rule [D01-S04]:** decompose by **context boundary**, not by problem type. Wrong:
one agent writes features, another writes tests, a third reviews. Right: "An agent handling a feature
should also handle its tests, because it already possesses the necessary context." Bad boundaries named
explicitly: sequential phases of the same work (planning → implementation → testing), tightly coupled
components requiring "constant back-and-forth," and work requiring "frequent synchronization."

**The telephone game [D01-S04]:** "When agents are split by problem type, they engage in a 'telephone
game,' passing information back and forth with each handoff degrading fidelity." Observed consequence:
"The subagents spent more tokens on coordination than on actual work."

**Orchestrator prompt-engineering requirements [D01-S03]:** each subagent needs "an objective, an output
format, guidance on the tools and sources to use, and clear task boundaries." Vague instructions like
"research the semiconductor shortage" caused duplicated work and misinterpretation. Embed explicit scaling
rules: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4
subagents with 10-15 calls each, and complex research might use more than 10 subagents." Instill "good
heuristics rather than rigid rules."

**Early coordination failure modes observed in production [D01-S03]:** spawning "50 subagents for simple
queries"; "scouring the web endlessly for nonexistent sources"; "distracting each other with excessive
updates"; continuing despite having "sufficient results."

**Architectural bottleneck [D01-S03]:** synchronous execution "simplifies coordination, but creates
bottlenecks" — the lead agent cannot steer running subagents, subagents cannot coordinate with each other,
and "the entire system can be blocked while waiting for a single subagent to finish." Confirmed by the
Claude Code guidance: "subagents cannot communicate directly" [D01-S20].

**Platform mechanics that make the trade-offs concrete:**

- Managed Agents multiagent: each agent runs in its own **session thread**, "a context-isolated event
  stream with its own conversation history"; agents share sandbox, filesystem and vault credentials, but
  "Tools, MCP servers, and context are not shared" [D01-S18]. Three sanctioned delegation patterns:
  **parallelization, specialization, escalation** [D01-S18].
- Agent SDK subagents: four benefits — context isolation, parallelization, specialized instructions,
  **tool restrictions** (a least-privilege lever: "a `doc-reviewer` subagent might only have access to Read
  and Grep tools") [D01-S19]. The hard constraint: "The only content you pass from parent to subagent is
  the Agent tool's prompt string, so include any file paths, error messages, or decisions the subagent
  needs directly in that prompt" [D01-S19].
- Cost governance is a first-class design input: "Each subagent makes its own API requests, which count
  toward the query's `total_cost_usd`, and a subagent can spawn subagents of its own, so one prompt can
  grow into a tree of agents." Caps exist for depth (default 3), concurrency (default 20), and spend
  (`maxBudgetUsd` / `max_budget_usd`, no default) [D01-S19].
- Delegation signal for a *single* agent that should delegate [D01-S20]: "When a task requires exploring
  ten or more files, or involves three or more independent pieces of work, that's a strong signal to
  direct Claude toward subagents." Against: "Sequential, dependent work"; "Two subagents editing the same
  file in parallel is a recipe for conflict"; "Too many specialist agents" floods the delegation choice.

**Multi-model composition as an orchestration strategy [D01-S12]:** two named strategies.

| Strategy | Control flow | Frontier model's role | Pays when | Fails when |
|---|---|---|---|---|
| **Advisor** | Smaller model runs the loop, escalates on demand | Consulted for plans and corrections | Executor gap is large *and* the executor actually consults | "An executor at low effort can stop detecting that it is stuck" — consult rate collapses and the pairing can score below the executor alone |
| **Orchestrator** | Frontier model runs the loop, delegates bulk work | Plans, dispatches, synthesizes | Work exceeds one context window with massive parallelism; or as insurance against cost-tail spirals | "work fits single context and not spiraling on tail"; dependent chains; work that "easily fits one context" — handoff and merge cost more than the plan |

The governing rule [D01-S12]: **"Multi-model configurations must beat the single model's full effort
curve to justify the added latency and complexity."** Always price the baseline first: "First price
frontier model alone at low effort. This is the baseline your multi-model must beat."

### Objective 5 — Decomposition techniques

Four distinct techniques, frequently conflated on exam-style items:

| Technique | What is split | Applies when | Coordination cost | Source |
|---|---|---|---|---|
| **Task decomposition** | The work into steps, executed by one context | Steps are enumerable and mostly sequential | Near zero | [D01-S02] (prompt chaining); [D01-S07] (one feature at a time) |
| **Prompt chaining** | Steps into separate LLM calls with programmatic gates between | Each step has a checkable intermediate output; you want a gate | Low; serial latency | [D01-S02] |
| **Context decomposition** | The *information* across isolated windows | Context from subtask A pollutes subtask B; corpus exceeds one window | Medium: handoff prompt + summary loss | [D01-S04][D01-S05][D01-S19] |
| **Tool decomposition** | The action surface into named, typed capabilities | You need to gate, render, audit, or parallelize an action; or a workflow deserves one consolidated tool | Low, but schema tokens are permanent context cost | [D01-S11][D01-S25][D01-S17] |

**How far to decompose — the stopping rules, all source-anchored:**

- Stop when coordination tokens approach work tokens: "The subagents spent more tokens on coordination
  than on actual work" is the reported failure signature [D01-S04].
- Stop at dependency boundaries: sequential, dependent work and "frequent synchronization" are
  anti-signals [D01-S04][D01-S20].
- Stop when the handoff artifact can no longer carry the state: a reset is only viable when "the handoff
  artifact [has] enough state for the next agent to pick up the work cleanly" [D01-S08].
- Stop when the model no longer needs the scaffolding: sprint-level decomposition was *removed* when the
  model could sustain coherence longer [D01-S08].
- Scale the split to the question, not to ambition: 1 agent / 3–10 tool calls for simple fact-finding;
  2–4 subagents / 10–15 calls for direct comparisons; >10 subagents only for complex research [D01-S03].

**Tool-granularity rules [D01-S11][D01-S25]:**
- "More tools don't always lead to better outcomes. A common error we've observed is tools that merely
  wrap existing software functionality or API endpoints" [D01-S11].
- Consolidate to the workflow: `schedule_event` instead of `list_users` + `list_events` + `create_event`
  [D01-S11].
- "Make sure each tool you build has a clear, distinct purpose"; overlapping tools "distract agents from
  pursuing efficient strategies" [D01-S11]. Restated for context engineering: "If a human engineer can't
  definitively say which tool should be used in a given situation, an AI agent can't be expected to do
  better" [D01-S05].
- Promote bash → dedicated tool for: **security gating** (hard-to-reverse actions), **staleness checks**,
  **rendering**, **scheduling/parallel-safety**. "Start with bash for breadth. Promote to dedicated tools
  when you need to gate, render, audit, or parallelize the action" [D01-S25].
- Namespacing groups related tools under common prefixes when there are many [D01-S11].
- **Programmatic tool calling** is a decomposition lever with a token argument: intermediate results
  return to a running script rather than the context window, so "Token cost scales with final output, not
  intermediate results" [D01-S25].
- Tool schemas are not free: tool-use system prompt overhead is 286 tokens on Claude Opus 5.5, 354 on
  Sonnet 5, 496 on Haiku 4.5, *excluding* your own tool definitions [D01-S17].

### Objective 6 — Business value pillars and SLAs

The blueprint's five pillars, with the architecture each one actually selects:

| Pillar | What the sponsor is buying | Metric shape [D01-S21] | Architectural consequence |
|---|---|---|---|
| **Efficiency** | Same work, less time/handling per unit | ↓ time to resolution, ↓ queue processing time, ↑ volume handling | Favors workflow/routing over agentic; favors caching, batch, smaller models at lower effort |
| **Transformation** | Work that would not otherwise happen | new capability, new artifact classes; "27% of Claude-assisted work wouldn't have been done otherwise" [D01-S22] | Justifies agentic/multi-agent spend; measured by *volume of newly feasible work*, not unit cost |
| **Productivity** | More output per worker, human stays in the loop | ↑ developer productivity, ↑ first-contact resolution, ↑ CSAT | Favors assistive/streaming UX, human-in-the-loop, low TTFT |
| **Cost** | Lower unit economics | ↓ cost per ticket, ↓ cost per conversation, ↓ cost per review | Batch (50% off), caching, effort down, smaller model; measured as **cost per completed task**, not per token [D01-S12] |
| **Performance SLA** | A bounded, contractual response characteristic | p95 latency, availability, throughput, accuracy floor | Constrains tier before anything else: a hard p95 kills unbounded agentic loops; streaming changes perceived latency; batch trades a 24-hour ceiling for 50% cost |

**Cost measurement rules that are exam-relevant [D01-S12]:**
- "Price lists are written per token… You pay for completed tasks, though, so compare models on cost per
  completed task."
- "Price the tail of your workload, not the median: compare models on the hardest tenth of your tasks, not
  the typical one." Reported example: "On a 20-problem WideSearch run, two problems carried 43% of the
  spend."
- Order of levers: **free wins first** (prompt caching, token hygiene, batch, spend limits), *then*
  trade-offs (model choice, effort, output caps, multi-model). Reported caching effect: "it cut agent-loop
  cost by a factor of 2.7 to 5.3."

**Latency levers, ranked by what they actually change:**
1. Execution mode (batch vs. sync) — changes the SLA class entirely [D01-S15].
2. Streaming — changes *perceived* latency / TTFT, not total generation time [D01-S16]. Anthropic's own
   infrastructure work treats TTFT as the latency users "most acutely *feel*" and cut p50 TTFT ~60% and
   p95 >90% by not provisioning a sandbox until a tool call needed one [D01-S09].
3. Pattern (parallelization vs. chaining) — parallel sectioning converts a sum of step latencies into the
   max of them [D01-S19]; chaining explicitly "trade[s] off latency for higher accuracy" [D01-S02].
4. Model + effort — effort "trades intelligence for latency and cost within a single model," and "Tuning
   effort is often a better lever than switching models" [D01-S13].

---

## 4. Comparison matrices (raw form, for the draft)

### M1 — Augmented LLM vs. workflow vs. agent

| Axis | Augmented LLM | Workflow | Agent |
|---|---|---|---|
| Who chooses the next step | Nobody (one step) | Your code | The model |
| Task predictability | Fully specified | Decision tree enumerable in advance | Path unknowable in advance |
| Step count | 1 | Fixed / bounded | Unbounded, needs a stop condition |
| Auditability | Trivial | High — each branch is code | Lower — non-deterministic between runs [D01-S03] |
| Latency profile | Lowest, predictable | Predictable (sum or max of steps) | Unbounded variance |
| Error cost tolerance | Any | Any | Must be recoverable (tests/review/rollback) [D01-S24] |
| Cost | Baseline | ~Steps × baseline | ~4× chat baseline [D01-S03] |
| Failure mode | Ceiling on complexity | Falls off the enumerated path | Compounding errors, loops, runaway spend |
| Choose when | One clean transform | "predictability and consistency for well-defined tasks" [D01-S02] | "flexibility and model-driven decision-making… at scale" [D01-S02] |

### M2 — One agent with more tools vs. multi-agent decomposition

| Axis | Single agent, broader tool set | Multi-agent decomposition |
|---|---|---|
| Token cost | 1× | 3–10× [D01-S04]; ~15× vs. chat for research systems [D01-S03] |
| Wall clock | Serial | Faster only when subtasks are genuinely independent; otherwise slower overall [D01-S04] |
| Context | One window, pollution accumulates | Isolated windows; ~1–2k token summaries return [D01-S05][D01-S19] |
| Tool selection quality | Degrades past ~20 tools / unrelated domains [D01-S04] | Each agent sees a focused surface |
| Failure surface | One prompt, one loop | "another potential point of failure, another set of prompts to maintain" [D01-S04] |
| Coordination | None | Telephone game; no direct agent-to-agent channel [D01-S04][D01-S20] |
| Security | One privilege set | Per-agent tool restriction = least privilege [D01-S19] |
| Choose multi-agent when | — | Context protection, parallelization, or specialization is a *demonstrated* constraint [D01-S04] |

### M3 — Pattern selection matrix

| Signal in the stem | Pattern |
|---|---|
| Fixed steps, each checkable, willing to pay serial latency | Prompt chaining |
| Distinct input classes handled better separately, classification is reliable | Routing |
| Independent subtasks, want wall-clock speed | Parallelization (sectioning) |
| Want confidence via multiple attempts/perspectives | Parallelization (voting) |
| Subtasks cannot be enumerated until the input arrives | Orchestrator-workers |
| Clear criteria + refinement measurably improves output | Evaluator-optimizer |
| Step count unknowable, path unknowable, errors recoverable | Autonomous agent |

### M4 — Execution mode vs. SLA and cost

| Mode | Latency class | Cost | Constraints | Use when |
|---|---|---|---|---|
| Synchronous | Full generation before response | List price | HTTP timeouts on long generations | Short, interactive, low `max_tokens` |
| Streaming (SSE) | TTFT in ms; total unchanged | List price | Required for very large `max_tokens` [D01-S16][D01-S24] | Human waiting on the output |
| Async / queued (yours) | Seconds–minutes, you control | List price | You own the queue, retry, callback | Long agentic runs; webhook-style integration |
| Message Batches | "most batches finishing in less than 1 hour"; results at completion or 24 h, whichever first; batch expires at 24 h | **50% of standard** | 100,000 requests or 256 MB per batch; results arrive in any order — key by `custom_id` | Bulk classification, backfills, evals, anything with no user waiting [D01-S15] |

### M5 — Feedback-loop placement

| Placement | Latency added | Catches | Blind to | Choose when |
|---|---|---|---|---|
| Inline rules-based verification | Milliseconds | Schema, lint, tests, policy violations | Semantic/subjective quality | A rule can express "correct" [D01-S06] |
| Inline self-critique (same context) | One extra call | Obvious slips | Its own blind spots — self-eval "confidently prais[es] the work" [D01-S08] | Cheap safety net only; never the primary gate |
| Separate evaluator agent | One agent's cost, low context transfer | Quality against an articulated rubric | Whatever the rubric omits; may rubber-stamp [D01-S04] | Task sits beyond what the model does reliably solo [D01-S08] |
| Offline eval suite | None at runtime | Regressions, model-swap risk | Novel production distributions | Pre-launch, CI/CD [D01-S10] |
| Production telemetry + human review | None at runtime | Distribution drift, real failure modes | Only after users are affected [D01-S10] | Always, in addition to offline |

### M6 — Long-horizon context strategy

| Strategy | Keeps | Loses | Choose when | Source |
|---|---|---|---|---|
| Context editing (clear tool results) | Recent reasoning | Old tool payloads | Transcript is bloated by stale results | [D01-S25] |
| Compaction (summarize) | Conversational flow | "subtle but critical context whose importance only becomes apparent later" | "tasks requiring extensive back-and-forth" | [D01-S05] |
| Context reset + handoff artifact | Whatever the artifact encodes | Everything else | Clear milestones; artifact can carry the state | [D01-S08] |
| Structured note-taking / memory | Cross-session state | Nuance not written down | "iterative development with clear milestones"; multi-session work | [D01-S05][D01-S25] |
| Sub-agent architectures | Clean main context | Detail inside the subagent | "complex research and analysis where parallel exploration pays dividends" | [D01-S05] |

### M7 — Multi-model composition

See the Advisor/Orchestrator table under Objective 4. Governing rule: price the single model across its
effort curve first; the multi-model configuration must beat that whole curve [D01-S12].

---

## 5. Verified platform facts used in the draft

All verified in this session against primary Anthropic sources on 2026-09-24.

| Fact | Value | Source |
|---|---|---|
| Current recommended default model | Claude Opus 5.5 (`claude-opus-5-5`), released 2026-09-22 | [D01-S14][D01-S23] |
| Opus 5.5 price / context / output / default effort | $4 in / $20 out per MTok; 1M context; 128K max output; default effort `medium` | [D01-S14] |
| Claude Fable 5.1 (`claude-fable-5-1`) | $10 / $50 per MTok; 1M context; 128K output; default effort `high`; "most capable widely released model" | [D01-S14][D01-S13] |
| Claude Sonnet 5 (`claude-sonnet-5`) | $2 / $10 per MTok; 1M context; 128K output | [D01-S14] |
| Claude Haiku 4.5 (`claude-haiku-4-5`) | $1 / $5 per MTok; 200K context; 64K output; no effort parameter | [D01-S14] |
| Batch discount and SLA | 50% of standard prices; "most batches finishing in less than 1 hour"; results at completion or 24 h, whichever first; expire at 24 h | [D01-S15] |
| Batch size limits | 100,000 requests or 256 MB, whichever comes first | [D01-S15] |
| Cache read pricing | 10% of base input price (5% on Opus 5.5; 2.5% on Fable 5.1 / Mythos 5.1) | [D01-S14] |
| Tool-use system prompt overhead | Opus 5.5: 286 tokens; Sonnet 5: 354; Haiku 4.5: 496 (auto/none) | [D01-S17] |
| Subagent governance defaults (Agent SDK) | Depth 3, concurrency 20, spend uncapped by default | [D01-S19] |
| Multi-agent token multiplier | 3–10× single-agent [D01-S04]; agents ~4× chat, multi-agent ~15× chat [D01-S03] |
| Multi-agent research uplift | +90.2% vs. single-agent Opus 4 on Anthropic's internal research eval | [D01-S03] |

---

## 6. Contradictions and tensions between sources (surfaced, not smoothed)

1. **The course brief's model lineup is out of date.** `AGENT-BRIEF.md` states the current lineup is
   "Claude 5 family (Opus 5, Sonnet 5, Fable 5.1) and Haiku 4.5," and the bundled `claude-api` skill's
   cached table (dated 2026-06-24) lists Opus 5 at $5/$25 [D01-S24]. The live models overview fetched
   today lists **Claude Opus 5.5** (`claude-opus-5-5`, $4/$20, released 2026-09-22) as the recommended
   default, with Claude Opus 5 moved to the legacy list [D01-S14][D01-S23]. **Resolution used in the
   draft:** follow the live docs, name Opus 5.5 where a current model must be named, and prefer durable
   architectural statements over model names wherever possible. Editors should not "correct" the draft
   back to Opus 5.
2. **Token-multiplier figures differ because the baselines differ.** [D01-S03] says multi-agent uses "about
   15× more tokens than chats" and agents "about 4× more tokens than chat"; [D01-S04] says multi-agent
   consumes "3 to 10 times more tokens than single-agent approaches." These are consistent once the
   baseline is named (chat vs. single *agent*). The draft must always state the baseline. 15/4 ≈ 3.75×,
   which sits at the bottom of the 3–10× band.
3. **Enthusiasm for multi-agent differs by vintage and domain.** [D01-S03] (June 2025) reports a +90.2%
   uplift and reads as an endorsement; [D01-S04] (later) opens with "start with single agents" and frames
   multi-agent as overhead to be justified. Both are Anthropic. Reconciliation: the 90.2% result is
   *domain-specific* (open-ended research with heavy parallelism and information exceeding one context
   window) — exactly the condition [D01-S04] lists as justified. Do not generalize it to coding, support
   triage, or pipelines; [D01-S03] itself says most coding tasks are a poor fit.
4. **Orchestration enthusiasm vs. cost data.** [D01-S03] treats orchestrator-workers as the winning
   architecture; [D01-S12] measures that an orchestrator "loses to single model at lower effort" whenever
   work fits a single context, the chain is dependent, or there is no cost tail to insure against. Not a
   contradiction — different questions (quality ceiling vs. cost per completed task) — but exam items will
   exploit the gap. Discriminator: does the work exceed one context window *and* split into genuinely
   independent pieces?
5. **Harness complexity: build it vs. delete it.** [D01-S07] (Nov 2025) builds an elaborate harness
   (initializer agent, 200-feature JSON list, one feature per session). [D01-S08] (Mar 2026) reports
   removing sprint decomposition entirely after a model upgrade. The reconciling principle is stated in
   [D01-S08] and [D01-S09]: harness components encode assumptions about model limitations, and those
   assumptions "go stale as models improve." Architecturally this means *scaffolding is a depreciating
   asset*.
6. **LLM-as-judge status.** [D01-S06] calls it "generally not a very robust method, and can have heavy
   latency tradeoffs." [D01-S03] uses an LLM judge as its scaling evaluation method, and [D01-S10] treats
   model-based graders as the right choice for open-ended tasks. Reconciliation: LLM-as-judge is weak as an
   *in-loop runtime gate* and acceptable as an *offline evaluation* method with human calibration.
   The draft states this distinction explicitly.
7. **The enterprise ebook [D01-S21] is partly stale.** Its model-selection section names Claude 3.5 Sonnet
   / 3 Opus / 3.5 Haiku and a 200K context window, and its prompt structure recommends assistant prefill —
   which current models reject [D01-S24]. Its *use-case selection*, *success criteria*, *graduation
   criteria*, and *success-metric* content is durable and is what the draft uses. The model and prefill
   content is explicitly not used.

---

## 7. Open questions / `[UNVERIFIED]` items

- **No Anthropic publication uses the exact phrase "business value pillars," nor the exact five-item list
  "efficiency, transformation, productivity, cost, performance SLAs."** That list appears only in the exam
  blueprint [D01-S01]. The mapping of each pillar to metrics and architectures in this dossier is a
  synthesis from [D01-S21], [D01-S22], and [D01-S12], not a quotation. `[UNVERIFIED]` as an official
  Anthropic framework; verified only as blueprint language.
- The per-domain item count (~10–11 of 63 for Domain 1) is arithmetic on the published weight, not a
  published number [D01-S01]. Anthropic states weights are "approximate."
- Whether the exam will use Anthropic's newer vocabulary (harness, session/sandbox decoupling, coordinator
  rosters) or stay with the 2024 "Building effective agents" vocabulary is unknown. The blueprint's
  wording of objective 3 points to the latter; the draft teaches the 2024 taxonomy as primary and the
  newer vocabulary as named extensions. `[UNVERIFIED]`.
- No Anthropic source gives a numeric threshold for "too many tools." The closest is [D01-S04]'s "20+"
  signal for specialization and [D01-S05]'s qualitative test ("If a human engineer can't definitively say
  which tool should be used…"). Any hard number beyond "20+" would be invented; the draft does not
  invent one.
- Whether a real CCAR-P item would treat "streaming" as an SLA lever or as a Domain 3 integration topic is
  unknown. The draft covers it as an SLA consequence only.
- Anthropic's enterprise ebook [D01-S21] is undated on its face; the internal citations (Bain 2024,
  McKinsey 2024) and model references place it in the Claude 3.5 era. Treat quantitative claims from it as
  historical.

---

## 8. Prep-material landscape

Third-party CCAR-P material found on 2026-09-24. The credential is ~3 months old; the market is already
saturated with question banks, which is itself a signal.

| Source | What it claims | Trust | Assessment |
|---|---|---|---|
| Tutorials Dojo [D01-S27] | CCAR-P practice tests, timed/review/section modes, flashcards | low | Established brand in cloud certification prep, but no Anthropic affiliation and no visible primary-source citation for CCAR-P content. Volume-first. |
| Udemy listings ×2 [D01-S28] | "360 CCAR-P exam questions across 6 timed practice tests," claims answers "cited to official documentation" | low | Self-published; citation claims unverifiable without purchase. Two distinct courses with near-identical claims suggests template-driven production. |
| Preporato [D01-S29] | "6 complete practice exams, 390+ unique questions," 10 free samples | low | Free sample inspected. Scenario stems are reasonable in *shape* (bank onboarding, e-commerce agent, logistics classification, medical summarization) and correctly reference real features (prompt caching, Message Batches, tool use, structured outputs). **No citations at all.** Also describes the exam as 65 questions; the published guide says **63** [D01-S01] — a small but telling accuracy failure. |
| CertSafari [D01-S30] | "456 exam-style practice questions… aligned with the latest exam guide" | low | Bank-only; no instructional content; no sourcing visible. |
| Claude Certification Guide [D01-S31] | 30 lessons + 250+ practice questions, free | low | The most honest of the set: carries an explicit disclaimer ("not affiliated with, endorsed by, or sponsored by Anthropic") and correctly cites the published exam facts (63 items, 120 minutes, 720 cut score). Still unsourced on technical content, and the Professional track was described as under development. |
| Clearcat blog [D01-S32] | Exam guide + topics + practice questions blog post | low | SEO-shaped listicle; restates the blueprint. |

**Judgments for the course team:**

1. **Every one of these is `low` trust and none may be copied from.** They are recorded here so the
   consolidation session knows the competitive landscape and so reviewers can recognize if any draft
   language drifts toward them.
2. **The one verifiable accuracy check failed.** At least one vendor states the item count as 65 rather
   than the published 63 [D01-S01][D01-S29]. Expect similar drift on the cut score, weights, and model
   facts elsewhere in this market.
3. **Model-name drift is the dominant risk in third-party material.** One vendor's content was assessed as
   referencing model names that a reviewer could not match to public releases. Our defense is the brief's
   rule: every model name, price, context number, and parameter is verified against primary docs in
   session, or marked `[UNVERIFIED]`.
4. **Differentiation for this course:** these banks sell *volume of items*. None of them teach the
   trade-off spine — the discriminators between workflow/agent, single/multi-agent, and the four
   decomposition techniques — with primary-source grounding. That is where this chapter should win.

---

## 9. Draft-construction notes (handoff to reviewers/editor)

- The chapter leads with the **simplicity gradient** ([D01-S02]'s "simplest solution possible") because
  every distractor archetype in this domain is a complexity-escalation trap.
- Eight trade-off comparisons are included (brief minimum is 4–6; 17% weight warrants more).
- Eight worked scenarios span financial services, healthcare, retail, government, SaaS/telecom, life
  sciences, legal, and logistics — matching the industry list in the exam guide's audience section
  [D01-S01].
- Twelve practice items, mixing single- and multiple-response, each stating the number to select, each
  with per-distractor rationale, matching the guide's Section 8 cognitive level (scenario stem, no
  trivia) [D01-S01].
- Volatile numbers are dated and cited inline. Durable architectural statements are preferred wherever a
  number would age badly.
