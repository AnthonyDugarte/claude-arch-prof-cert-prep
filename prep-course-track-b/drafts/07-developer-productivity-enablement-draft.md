# Domain 7: Developer Productivity & Operational Enablement

**Weight:** 7% of the exam (approximately 4-5 of 63 scored items).

**Objectives (verbatim from the exam guide, Section 6):**
1. Configure Claude tools and environments for teams (e.g., Claude Code)
2. Improve developer workflows using AI-assisted tooling
3. Support debugging and operational issue resolution

---

## 1. Exam-relevance framing

This domain tests judgment about deploying an agentic developer tool to a team -- Claude Code is the named example, and items expect you to reason about its configuration surfaces (settings.json, CLAUDE.md, permission modes, hooks, MCP), not just cite abstract principles. The underlying judgment -- where a rule belongs, who can override it, what happens when the agent is wrong or unattended -- generalizes to any agentic tool an architect owns. Because this is a fast-moving 7%-weight surface, items reward durable architectural reasoning over memorized flag syntax, while still expecting stable facts: precedence order for settings and permission rules, the difference between advisory instructions and enforced control, and why cloud-provider deployments trade model currency for compliance fit.

Recurring distractor archetypes:

1. **"Log it / confirm it" instead of removing it.** A destructive capability is present; the tempting wrong answer adds logging or a confirmation prompt instead of removing the capability or moving it behind OS-level isolation.
2. **"Put it all in CLAUDE.md" / "prompt harder."** A team-scale context or configuration problem (conventions, a one-off procedure, external access, a zero-exception rule) is solved by stuffing everything into one instruction file or asking the model to "be careful," when a skill, subagent, MCP server, or hook is correct.
3. **"Individual override wins."** A scenario describes an org-wide requirement, and a wrong answer lets a project- or user-level setting override it, when managed settings are (almost always) the ceiling.
4. **"Activity equals productivity."** A rollout-measurement item offers lines-of-code, commit count, or session count as the success metric, when the discriminator is whether the metric reflects outcome, not volume.
5. **"Plausible root cause without evidence."** A debugging scenario is resolved by picking the most plausible-sounding explanation rather than the one with the cheapest, most direct verification step.

---

## 2. Core concepts

**Two independent configuration hierarchies.** Conflating these is the most exam-relevant trap in this domain. `settings.json` (behavior, permissions, telemetry) is an **override** stack -- managed (`managed-settings.json`/MDM/server-managed) > CLI `--settings` > project-local (`.claude/settings.local.json`) > shared project (`.claude/settings.json`, checked into git) > user (`~/.claude/settings.json`) -- one deterministic winner per key, enforced by the client regardless of what the model decides. Most list-valued keys (e.g., `permissions.allow`) merge across scopes; a short, deliberate set of security-sensitive keys instead take the *stricter* value from any scope regardless of level [D07-S01]. `CLAUDE.md` (instructions) is a **concatenation** stack: managed-policy, user, project, and local files all load together, root-to-leaf, and a contradiction between two loaded files is *not* resolved by precedence -- Claude may follow either arbitrarily [D07-S02]. *Decision it drives:* for "which value applies," check whether the key lives in settings/permission rules (one winner) or CLAUDE.md (no tiebreaker -- keep files consistent instead). *Misconception:* a more specific CLAUDE.md file "overrides" a broader one -- it's only read later in context, not authoritative over it.

**Permission modes vs. permission rules.** Modes -- `default` (Manual), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` -- set a session's baseline; rules (`allow`/`ask`/`deny`, scoped by tool pattern) layer exceptions on top. Rule resolution is **deny -> ask -> allow, first match wins; specificity does not change the order** [D07-S06, D07-S07]. *Decision it drives:* the fastest way to make a capability permanently unreachable is a deny rule (or never granting the tool) -- a mode change affects everything, an allow-list edit only adds exceptions. *Misconception:* `auto` and `bypassPermissions` are the same "let it run" setting -- `auto` runs a background classifier that blocks scope escalation and hostile-content-driven behavior and is itself built to distrust its input (it reviews the request and CLAUDE.md but not raw tool *results*, so injected content can't manipulate it, though it also can't verify a claim tool output would disprove); `bypassPermissions` disables checking entirely and is documented as safe only in isolated, disposable compute [D07-S07].

**Sandboxing vs. `bypassPermissions`.** The sandboxed Bash tool enforces filesystem and network boundaries at the OS layer (macOS Seatbelt; Linux/WSL2 namespace isolation), so routine commands run unprompted because the kernel, not a dialog, enforces the boundary [D07-S09]. `bypassPermissions` removes checking with no enforced boundary, and is restricted by Anthropic's own guidance to "isolated environments like containers or VMs." *Decision it drives:* want fewer prompts without losing a real boundary -> sandbox; `bypassPermissions` only where the infrastructure itself is already the boundary. *Misconception:* a container alone makes bypass mode safe -- dev-container docs pair it with an explicit network-egress restriction, because a container alone doesn't stop credential exfiltration over an open network [D07-S10].

**Hooks vs. advisory instructions.** A hook runs at a defined lifecycle event (`PreToolUse`, `Stop`, `SessionStart`, and dozens more); a `PreToolUse` hook that blocks with a non-zero exit **deterministically** stops the action "regardless of what Claude decides," while CLAUDE.md and skills remain advisory context the model can deprioritize under crowded context [D07-S02, D07-S04, D07-S06]. *Decision it drives:* a zero-exception rule belongs in a hook or a deny rule, never a more emphatic CLAUDE.md sentence. *Misconception:* a hook that only logs is "enforcing" anything -- only a blocking exit code is preventive; logging alone is detective.

**Instruction/context vehicle selection.** CLAUDE.md loads every session, always; a **skill** loads on demand (progressive disclosure); a **slash command** loads on explicit invocation; a **subagent** spawns on delegation with its own isolated context window and optionally a cheaper pinned model; an **MCP server** provides access to an external system [D07-S02, D07-S13, D07-S14, D07-S16]. *Decision it drives:* always-true and always-needed -> CLAUDE.md; only matters sometimes -> skill; needs isolation or a different model -> subagent; needs an external system -> MCP (detailed in 3.3). *Misconception:* more context in one file is strictly safer than less -- an over-long CLAUDE.md measurably reduces adherence because "important rules get lost in the noise" [D07-S18].

**Headless mode, deployment surface, and observability.** `claude -p` defaults to **Manual** regardless of plan, unlike interactive Pro/Max/Team sessions which now default to `auto` -- unattended policy must be set explicitly [D07-S07, D07-S11]. A **deployment surface** (Teams/Enterprise, Console, Bedrock, Vertex, Foundry) decides where inference runs and how it's billed; an **LLM gateway** is a separate, composable layer adding centralized auth and per-team attribution on top of any surface [D07-S17]. Claude Code ships no built-in cross-provider dashboard -- it emits OpenTelemetry metrics (session count, cost, tokens, lines of code) taggable via `OTEL_RESOURCE_ATTRIBUTES`, which is the *only* source of per-user cost data on a cloud-provider deployment [D07-S15, D07-S19]. *Decision it drives:* pick the surface for identity/network/compliance fit first, instrument OTel from day one on any cloud provider, and treat "wait for an answer" as a failure mode in any human-free workflow. *Misconception:* a cloud billing console gives per-developer attribution, or cloud deployments get day-one model parity with the direct API -- both are false; the latter is mitigated by pinning env vars such as `ANTHROPIC_DEFAULT_OPUS_MODEL` [D07-S17].

---

## 3. Trade-off analyses

### 3.1 Configuration layering: managed policy vs. shared project config vs. individual override

| Axis | Managed (org) | Shared project (checked-in `.claude/settings.json`) | Individual (user/local) |
|---|---|---|---|
| Who can change it | Security/platform team, via `managed-settings.json`, MDM, or server-managed console | Anyone with repo write access, via code review | Each developer, unilaterally |
| Auditability | High -- deployed and versioned centrally | High -- git history, PR review | Low -- invisible to the team |
| Overridable by lower scopes | No, except a short, deliberate list of stricter-value exceptions | Partially -- user/local can add, but a project deny/ask still binds | N/A |
| Right for | Compliance mandates, non-negotiable deny rules, telemetry enforcement | Team conventions, shared hooks/MCP servers, permission allowlists everyone needs | Personal preferences, saved "don't ask again" approvals |

**Choose managed** when a rule must hold regardless of who is on the project. **Choose shared project** for consistency within a codebase that should survive code review but not require central IT. **Choose individual** only for genuine personal preference. Checked-in project config beats per-developer setup on **auditability and reproducibility** -- a security review can read `.claude/settings.json` in git history; it cannot read forty laptops. Secrets never belong in a checked-in file; use an `apiKeyHelper` script, `env` values referencing already-provisioned secrets, `${VAR}`-interpolated MCP headers, or CI secrets/OIDC federation instead [D07-S01, D07-S03, D07-S12, D07-S16].

### 3.2 Permission strategy: prompt-on-everything vs. curated allowlist vs. auto (classifier) vs. bypass

| Approach | Velocity | Blast radius | Enforced by | Where it belongs |
|---|---|---|---|---|
| Prompt-on-everything (Manual) | Lowest | Degrades into habituated rubber-stamping over a long session | Human judgment per call | Sensitive/unfamiliar repos, first week on a project |
| Curated allowlist (`permissions.allow`) | High for the allowed set | Bounded to the reviewed rule set; deny still overrides | Rule engine (deny -> ask -> allow) | Default target state for most teams |
| `auto` (classifier) | High, broad | Bounded by a classifier reviewing text/CLAUDE.md but not tool results -- immune to injected content, but can't verify claims results would disprove | Background classifier; deny/ask still apply first | Long unattended tasks where classifier judgment substitutes for a human's |
| `bypassPermissions` | Highest | Unbounded except a short hard-coded no-touch list | Nothing -- safe only in isolated, disposable compute | Network-restricted containers/VMs only |
| Sandboxing (independent axis) | Neutral | OS kernel, not model judgment | Kernel | Bounds `auto`/`bypassPermissions` blast radius -- complements rules, doesn't substitute |

**The trap this axis tests:** prompt-on-everything degrades into rubber-stamping -- a developer who has approved the same command forty times stops reading the fortieth. This mirrors the exam guide's own least-privilege rationale: destructive capability belongs behind *removal from the tool surface* or OS-level sandboxing, not a confirmation dialog [D07-S06, D07-S07, D07-S09].

### 3.3 Context/instruction vehicle: CLAUDE.md vs. skill vs. slash command vs. subagent vs. MCP server

| Vehicle | Loaded | Right for | Wrong for |
|---|---|---|---|
| CLAUDE.md | Every session, always | Durable conventions Claude can't infer from code (build commands, non-default style, etiquette) | Rarely-needed knowledge, long procedures, anything derivable by reading |
| Skill (`SKILL.md`) | On demand (progressive disclosure) | Reusable multi-step procedures or reference material needed only sometimes | Zero-exception rules (that's a hook) |
| Slash command | On explicit invocation | Fixed, user-triggered actions, especially with side effects | Open-ended exploration that would pollute the main context |
| Subagent | On delegation, fresh isolated context window | Tasks reading many files, needing restricted tools, or a cheaper pinned model | Simple one-shot lookups -- delegation overhead isn't worth it |
| MCP server | Connection-time | External-system access (tickets, docs, database) no built-in tool covers | Storing instructions -- that's CLAUDE.md or a skill |

**Choose CLAUDE.md** for facts Claude should hold in *every* session. **Choose a skill** the moment an instruction only matters *sometimes*. **Choose a subagent** specifically for *context isolation*, not merely because a task is "distinct." **Choose an MCP server** only for external-system access -- a tool-access mechanism, not a context-injection one. Cramming a procedure, a delegated task, and API-access instructions all into one CLAUDE.md produces a large, always-loaded file that dilutes the instructions that matter most.

### 3.4 Deployment surface: direct/Teams-Enterprise vs. cloud provider vs. self-hosted gateway

| Dimension | Teams/Enterprise (direct) | Bedrock / Vertex / Foundry | Self-hosted LLM gateway |
|---|---|---|---|
| Identity/SSO | claude.ai SSO, domain capture on Enterprise | Cloud IAM (AWS/GCP) or Entra ID | Whatever corporate IdP the gateway integrates |
| Network egress | Direct to Anthropic | Stays inside the cloud's network boundary | Fully operator-controlled -- single enforcement point |
| Cost attribution | Per-seat allowance + spend report/Analytics API | Cloud billing console (aggregate only); per-user needs OTel or a gateway | Native per-key/per-team tracking -- the reason to add one |
| Model availability | Fastest -- Anthropic-operated | Can lag; mitigated by `ANTHROPIC_DEFAULT_*_MODEL` pinning | Inherits whatever the underlying provider offers |
| Data handling | Anthropic's own terms directly | Cloud provider's compliance/residency posture | Operator-defined; can add its own retention layer |

**Choose direct/Teams-Enterprise** when identity, network, and compliance already fit an Anthropic-first posture and fastest model access matters. **Choose a cloud provider** when procurement or existing cloud IAM investment requires inference to stay inside an already-approved boundary, accepting a documented model-availability lag mitigated by pinning. **Choose a gateway** -- layered on top of a deployment surface, not instead of it -- for centralized cross-team budgets or cross-provider attribution the surface doesn't natively give [D07-S17, D07-S19].

### 3.5 Interactive vs. headless/CI usage

| Dimension | Interactive session | Headless (`-p`) / CI |
|---|---|---|
| Good fit | Exploration, pairing, judgment-heavy debugging, unfamiliar repos | Bounded, verifiable, repeatable tasks: lint/test triage, PR review, migration fan-out |
| Poor fit | High-volume mechanical repetition | Judgment-heavy work with no available verification signal |
| Default permission mode | `auto` on Pro/Max/Team; Manual on Enterprise/Console | Manual, regardless of plan -- must be set explicitly |
| Guardrails | A human is the reviewer of record | Scoped tool allowlist, `--bare` for reproducibility, `dontAsk`/`--permission-prompts none` for unattended runs, no write access to the trunk branch, required review gate, turn/timeout caps |

CI pays off where a cheap, automatable verification signal (a linter, a test suite, a build) substitutes for the absent human, and is a poor fit where correctness needs domain judgment a script can't encode. GitHub Actions' own guardrails match this: it checks the triggering user has repo **write access** and the actor is **human** (rejecting bots unless allowlisted, closing the "bot re-triggers itself" loop), with minimum necessary scope and **reviewing changes before merging** as the stated best practice [D07-S12, D07-S18].

### 3.6 Cost model: seat-based subscription vs. API-metered usage

| Axis | Seat-based (Teams/Enterprise) | API-metered (Console, Bedrock, Vertex, Foundry) |
|---|---|---|
| Predictability | High -- fixed per-seat cost; in-allowance usage isn't separately billed | Low -- scales directly with tokens consumed |
| Per-user attribution | Native (spend-report CSV, Analytics API) | Native on Console; **not native** on cloud providers -- requires OTel or a gateway |
| Best fit | Predictable-workload teams wanting budget certainty plus bundled web/chat access | Variable/bursty workloads, or orgs with existing per-token chargeback |
| Risk if misapplied | Power users (agent teams, parallel sessions) can exhaust the seat allowance | An unbounded workspace can spike unpredictably without a rate limit |

A mixed fleet is normal, not an edge case -- each developer is metered by the credential they authenticated with. The decision is "match cost model to workload variance and required attribution granularity," instrumenting OTel from day one for anyone on a cloud provider [D07-S19].

---

## 4. Worked scenarios

**Scenario A -- Financial services, allowlist vs. compliance mandate.** A trading-platform team wants Claude Code to run tests, commits, and internal deploy scripts without prompting. Compliance requires the tool never have standing access to production credentials. *Recommended:* a curated `permissions.allow` list in checked-in `.claude/settings.json` for the specific safe commands, with the credential boundary enforced by never exposing production credentials to the environment. *Why alternatives lose:* `bypassPermissions` satisfies velocity but removes the compliance boundary entirely; a project-level "ask" rule on production commands is a habituation risk, since deny -- not ask -- is the only unconditional control. *What would change the answer:* inside a disposable, network-isolated deploy container with zero credential access, `bypassPermissions` becomes defensible because the boundary now lives in the infrastructure.

**Scenario B -- Healthcare, CLAUDE.md bloat.** A clinical-data team's CLAUDE.md has grown to 600 lines covering style, HIPAA handling, a migration runbook, and a ticketing workflow; developers report Claude increasingly misses the HIPAA rule specifically. *Recommended:* keep only durable, always-relevant facts in CLAUDE.md; move the migration runbook to a skill and ticketing access to an MCP server; if the HIPAA rule is truly zero-tolerance, enforce it with a `PreToolUse` hook rather than prose. *Why alternatives lose:* adding "IMPORTANT" to the existing rule treats a context-crowding problem as a wording problem and won't fix a file already too dense to be followed reliably [D07-S18]. *What would change the answer:* if the rule is life-safety-critical, the answer shifts entirely toward a deterministic hook.

**Scenario C -- Retail, CI code-review rollout.** A retail org wants Claude to review every pull request for common bugs before human review. *Recommended:* the GitHub Actions integration in automation mode, triggered on pull-request events, read/comment-only scope, with the existing human merge gate unchanged. *Why alternatives lose:* granting write/merge access conflates "review" with "act," expanding blast radius for no benefit in a review-only use case. *What would change the answer:* if the goal shifted to auto-fixing trivial lint failures, a scoped write-access workflow with a turn cap becomes appropriate for that narrow subset only.

**Scenario D -- Government, cloud-boundary deployment with model lag.** A public-sector team must keep inference inside an existing authorized cloud boundary. *Recommended:* deploy via the approved cloud provider and explicitly pin models via `ANTHROPIC_DEFAULT_*_MODEL` so the org controls exactly when an upgrade rolls out for its own re-certification process. *Why alternatives lose:* the direct API doesn't meet the network-boundary requirement regardless of faster model availability; an unpinned alias introduces an uncontrolled variable into a compliance-sensitive environment. *What would change the answer:* if the real requirement were centralized per-team budget enforcement rather than a network boundary, a gateway in front of the cloud provider is the more precise fit.

---

## 5. Failure modes & diagnostics

| Symptom | Likely cause | First thing to check | Fix |
|---|---|---|---|
| A setting keeps reverting to a value the developer didn't set | A higher-precedence scope (managed, or a checked-in project setting) sets the same key | Which file supplied the active value | Move the intended value to the correct scope, or accept the higher scope's policy is intentional |
| Claude keeps violating a rule clearly written in CLAUDE.md | File is too long, the rule is buried, or a nested-directory CLAUDE.md contradicts it -- and there's no tiebreaker for CLAUDE.md conflicts | Line count/structure; whether a second loaded CLAUDE.md says something different | Prune to essentials; move procedure to a skill; convert the rule to a hook if it must be absolute |
| A permission rule "should" allow a command but it still prompts or is blocked | A deny or ask rule from another scope matches, and deny/ask always precede allow regardless of scope | Permission rules across managed/project/user scopes | Adjust or remove the conflicting rule at its source; don't try to out-rank it with a broader allow |
| Unattended CI run hangs or fails unpredictably on an unfamiliar action | No pre-decided policy for unmatched actions; headless mode defaults to Manual regardless of plan | Whether `--permission-mode`, an explicit tool allowlist, or `--permission-prompts none` was set | Set an explicit fail-closed policy; never assume a human will be present to answer |
| Automation posts changes a human never reviewed before they landed | Workflow scoped with write/merge access instead of comment-only, or no required review gate | The workflow's granted permission scope and branch protections | Scope to the minimum access the task needs; keep a required human review/approval step |
| Org can't tell which team is driving a cost spike | No OTel export, or no per-team resource attributes set | Whether telemetry is enabled and `OTEL_RESOURCE_ATTRIBUTES` is configured | Turn on OTel with team/cost-center tags -- the only per-user signal on a cloud-provider deployment |
| Auto mode keeps falling back to prompting mid-task | The classifier hit its block threshold, usually because it lacks context about trusted infrastructure the task touches | What the classifier is blocking and why | Add the infrastructure to a trusted/allowed pattern; don't respond by disabling the safety layer entirely |

---

## 6. Anti-patterns

- **Confirmation-as-safety.** Wrapping a destructive tool in a yes/no prompt and calling it least privilege. Looks right because a control point visibly exists; fails because repeated approval habituates the human into a rubber stamp while the tool remains reachable by design.
- **The kitchen-sink CLAUDE.md.** Putting conventions, one-off procedures, external-system access, and delegated-task definitions all in one file. Looks right because "Claude reads this every time, so put everything important here"; fails because size measurably degrades adherence, and because CLAUDE.md conflicts have no deterministic tiebreaker the way settings do.
- **Bypass-mode-as-default-for-CI.** Reaching for `--dangerously-skip-permissions` in a CI job because "nobody's watching anyway." Looks right because headless runs genuinely have no human to answer prompts; fails because it removes checking entirely rather than substituting a pre-decided, fail-closed policy -- and headless mode already disables first-run trust verification for unfamiliar repositories, so stacking bypass mode on top removes the last remaining checks simultaneously.
- **Vanity-metric rollout reporting.** Reporting adoption success as total lines of code generated, commits authored, or sessions started. Looks right because these numbers are easy to pull from telemetry and trend upward; fails because Claude Code's own telemetry exposes them explicitly as *usage* counters, with no documented claim they correlate with code quality, defect rate, or business outcome.
- **Plausible-story debugging.** Accepting an AI-generated root-cause explanation because it sounds coherent, without requiring the reproduction or evidence that would confirm it. Looks right because a well-written explanation is persuasive; fails because coherence is not correctness -- the documented discipline is a falsifiable, reproducible claim, not the most plausible-sounding story.

---

## 7. Exam-day heuristics

- **Removal beats detection beats confirmation.** When an item offers "remove the capability," "log/monitor it," and "add a confirmation step" as competing least-privilege answers, removal wins unless the stem explicitly requires the capability to remain available.
- **Deny and ask both precede allow, at any scope.** The more restrictive rule wins regardless of which scope it came from and regardless of which rule is more specific.
- **Settings override; CLAUDE.md concatenates.** If an item asks "which value applies," check whether the key lives in settings/permission rules (one deterministic winner) or CLAUDE.md (no tiebreaker -- the correct answer is "keep the files consistent," not "the more specific file wins").
- **Advisory vs. enforced.** If a requirement must hold with zero exceptions, the answer is a hook or a deny rule -- never a CLAUDE.md instruction or a more emphatic prompt.
- **Match the vehicle to the durability and shareability of the knowledge.** Always-true and always-needed -> CLAUDE.md. Sometimes-needed procedure -> skill. Needs isolation or a different model -> subagent. Needs an external system -> MCP.
- **A plausible root cause is not evidence.** The discriminator this exam rewards is verification (a reproduction, a log line, a passing/failing test), not plausibility.

---

## 8. Practice items

**Item 1 (select one).** A platform team checks a `.claude/settings.json` into their repository with a broad `permissions.allow` list so new hires get a productive setup on day one. Security later requires that no Claude Code session in this repository ever run `curl` to an external host. Which change enforces this regardless of what any individual developer configures locally?
A. Add a comment to the README asking developers not to allow `curl`.
B. Add a `deny` rule for `curl` in managed settings.
C. Remove `curl` from the project's `allow` list only.
D. Ask developers to switch to Manual mode when running near sensitive data.

*Correct: B.* Managed-scope deny rules cannot be overridden by any other scope, and deny precedes allow regardless of scope. *A* is not enforced. *C* only removes an explicit allow; `curl` could still be approved once in Manual mode. *D* relies on discipline, not a control.

**Item 2 (select one).** A CLAUDE.md file has grown to include coding conventions, a 40-step database migration runbook, and instructions for querying an internal ticketing system. Developers report Claude increasingly misses basic coding-convention rules that used to work reliably. What is the most direct fix?
A. Add "IMPORTANT" before every rule in the file.
B. Move the migration runbook into a skill and the ticketing access into an MCP server, leaving only durable conventions in CLAUDE.md.
C. Split CLAUDE.md into two files of the same total length.
D. Switch the team to `auto` permission mode.

*Correct: B.* Matches the documented cause (an over-long, mixed-purpose file dilutes adherence) with the correct vehicle per content type. *A* adds emphasis without shrinking the file. *C* doesn't reduce total loaded content -- CLAUDE.md files concatenate, not override. *D* addresses permission mode, not context content.

**Item 3 (select one).** An engineering team wants Claude Code to run routine, low-risk shell commands without interrupting the developer, while still enforcing a real boundary against unexpected filesystem or network access. Which mechanism fits best?
A. `bypassPermissions` mode.
B. The sandboxed Bash tool with defined filesystem/network boundaries.
C. A CLAUDE.md instruction telling Claude to "be careful with shell commands."
D. `dontAsk` mode.

*Correct: B.* Sandboxing reduces prompts while the OS kernel enforces the boundary. *A* removes checking with no enforced boundary. *C* is advisory, not enforced. *D* denies unmatched actions outright, blocking legitimate novel actions instead of safely allowing them.

**Item 4 (select one).** Which statement about Claude Code's headless mode (`claude -p`) is accurate?
A. It defaults to `auto` permission mode on Pro, Max, and Team plans, same as an interactive session.
B. It requires a human to answer any permission prompt before continuing, just like an interactive session.
C. It defaults to Manual permission mode regardless of plan, so an unattended run's policy must be set explicitly.
D. It cannot be used in CI pipelines because it requires a terminal.

*Correct: C.* Headless sessions default to Manual regardless of the account's interactive default, because no human may be present to escalate to. *A* inverts the documented behavior. *B* is false -- `--permission-prompts none`/`dontAsk` exist to avoid needing a human. *D* contradicts headless mode's purpose.

**Item 5 (select two).** Which two changes are appropriate guardrails for a GitHub Actions workflow that runs Claude Code automatically on every pull request to suggest fixes?
A. Give the workflow write access to merge pull requests directly.
B. Scope the workflow's permissions to the minimum needed (e.g., read contents, comment on PRs).
C. Require a human to review and approve before any suggested change is merged.
D. Authenticate the workflow using a developer's personal long-lived OAuth token shared across the whole org.

*Correct: B and C.* Minimum necessary scope and a human review/merge gate are the documented best practices here. *A* expands blast radius beyond what "suggest fixes" requires. *D* is a credential-hygiene anti-pattern for a shared org workflow.

**Item 6 (select one).** An organization runs Claude Code through a cloud provider (Bedrock or Vertex) for compliance reasons. Six months later, developers ask why they don't have access to a newly released Claude model that direct-API customers already have. What is the correct response?
A. The cloud-provider deployment enables new models automatically; something else must be broken.
B. Model availability can lag on cloud-provider deployments; the org should check and deliberately set its pinned model environment variables.
C. Cloud-provider deployments never receive new models, so this is expected permanently.
D. The organization should switch away from the cloud provider immediately.

*Correct: B.* This is the documented trade-off: aliases "can lag the newest release," mitigated by deliberate pinning, not assumed parity. *A* and *C* overstate certainty in opposite wrong directions. *D* is disproportionate -- the compliance reason for the deployment likely still holds.

**Item 7 (select one).** A cost-conscious engineering lead wants to know, per team, how much of the Claude Code bill on a cloud-provider deployment is attributable to each department. Which approach actually provides this?
A. The cloud provider's own billing console alone.
B. The Anthropic Console usage dashboard.
C. OpenTelemetry export with `OTEL_RESOURCE_ATTRIBUTES` tagging each session by team/cost center.
D. Asking each team to self-report their usage.

*Correct: C.* On a cloud-provider deployment Anthropic never sees the usage data, so its dashboards (B) don't cover it; the billing console (A) shows aggregate spend only. OTel resource-attribute tagging is the documented mechanism for this. *D* doesn't scale or verify.

**Item 8 (select one).** Auto permission mode repeatedly falls back to prompting a developer mid-task on a long-running job. What is the most likely documented cause, and the appropriate response?
A. The classifier is broken and should be disabled going forward.
B. The classifier has hit its block threshold, usually because it lacks context about trusted infrastructure the task touches; an administrator should add that context rather than disable the safety layer.
C. The developer should switch to `bypassPermissions` to avoid further interruptions.
D. This is expected behavior with no available remediation.

*Correct: B.* The fallback is a designed safety behavior tied to the classifier repeatedly blocking actions it can't confidently approve, typically for unrecognized infrastructure; the fix is adding trusted context, not disabling the check. *A* and *C* remove a safety layer instead of addressing the cause. *D* is inaccurate -- remediation is documented.

**Item 9 (select one).** A subagent is defined identically in a project's `.claude/agents/` directory and in the organization's managed settings, with conflicting tool restrictions. Which definition does Claude Code use?
A. The project-level definition, because it is closer to the code being worked on.
B. The managed-settings definition, because managed sources take precedence over project-level configuration.
C. Whichever was created most recently.
D. Both are merged, with the stricter tool restriction winning.

*Correct: B.* Subagent precedence places managed settings above project- and user-level agent directories. *A* and *C* invert or ignore that order. *D* describes settings-list merge behavior, which doesn't apply to subagent definition resolution.

---

## 9. Objective-coverage table

| Objective | Where covered in this chapter |
|---|---|
| 1. Configure Claude tools and environments for teams (e.g., Claude Code) | Core concepts (settings layering, two hierarchies, permission modes/rules, sandboxing, deployment surface); Trade-off analyses 3.1, 3.2, 3.4; Worked scenarios A, D; Failure modes rows 1-4, 7; Anti-patterns 1, 2, 6; Practice items 1, 3, 6, 10 |
| 2. Improve developer workflows using AI-assisted tooling | Core concepts (instruction vehicles, headless mode); Trade-off analyses 3.3, 3.5; Worked scenarios B, C; Failure modes rows 2, 5, 8; Anti-patterns 2, 3; Practice items 2, 4, 5 |
| 3. Support debugging and operational issue resolution | Core concepts (classifier untrusted-input design, OTel observability); Trade-off analysis 3.6; Failure modes rows 6, 9; Anti-patterns 4, 5; Practice items 7, 8, 9 |

---

## 10. Sources

Full source table with URLs, publishers, access dates, and trust ratings: `research/07-developer-productivity-enablement-sources.md` (IDs `D07-S01`-`D07-S35`). Primary sources cited inline: D07-S01 (Settings files and precedence), D07-S02 (Memory/CLAUDE.md), D07-S03 (Authentication), D07-S04 (Hooks reference), D07-S06 (Configure permissions), D07-S07 (Permission modes), D07-S09 (Sandboxing), D07-S10 (Development containers), D07-S11 (Headless mode), D07-S12 (GitHub Actions), D07-S13 (Subagents), D07-S14 (Agent Skills), D07-S15 (Monitor usage/OpenTelemetry), D07-S16 (MCP), D07-S17 (Enterprise deployment overview), D07-S18 (Best practices), D07-S19 (Manage costs effectively), D07-S27 (Exam guide). D07-S28-D07-S35 are third-party CCAR-P prep material, all rated `low` trust and not used for any factual claim (see the dossier's Prep-material landscape section).

No claims in this chapter are marked `[UNVERIFIED]`. Specific figures that are documented but explicitly volatile (per-seat pricing, exact classifier fallback thresholds, precise multipliers for parallel-session cost) are treated in the dossier as dated snapshots, not durable exam facts, and are described in this chapter only in relative/qualitative terms for that reason.
