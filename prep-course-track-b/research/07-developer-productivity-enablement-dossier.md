# Domain 7 Research Dossier — Developer Productivity & Operational Enablement

Weight: 7%. Objectives (verbatim from exam guide, Section 6):
1. Configure Claude tools and environments for teams (e.g., Claude Code)
2. Improve developer workflows using AI-assisted tooling
3. Support debugging and operational issue resolution

All product facts below were fetched live on 2026-09-24 from `code.claude.com/docs/en/*` (Claude Code docs moved from `docs.claude.com` — every `docs.claude.com/en/docs/claude-code/*` URL in the brief now 301-redirects there; use `code.claude.com` going forward). Model/API facts were cross-checked against the local `claude-api` skill (cached 2026-06-24, [D07-S26]). Source IDs `D07-S01`…`D07-S35` per the companion sources table.

---

## 1. Volatile product facts table

**This surface changes fast. Every row is a snapshot as of 2026-09-24 — re-verify before reuse in a live course.**

| Feature / setting | Current behavior (2026-09-24) | Source | Date verified |
|---|---|---|---|
| Settings file hierarchy | 4 local files + managed: user `~/.claude/settings.json`, shared project `.claude/settings.json`, project local `.claude/settings.local.json`, managed `managed-settings.json`/MDM/server-managed. | D07-S01 | 2026-09-24 |
| Settings precedence | Managed > command-line (`--settings`) > project local > shared project > user. Managed overrides everything except a short list of security-sensitive exceptions where the *stricter* value from any scope wins regardless of level (e.g. `disableClaudeAiConnectors=true`, `isolatePeerMachines=true`, `maxEffortLevel` lower cap). | D07-S01 | 2026-09-24 |
| List-valued keys (e.g. `permissions.allow`) | **Merge** across scopes rather than override; four model-list keys (`fallbackModel`, `modelPicker`, `availableModels`, `modelSettings`) are exceptions with their own non-merge rules. | D07-S01 | 2026-09-24 |
| Managed settings file path — macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` | D07-S08 | 2026-09-24 |
| Managed settings file path — Linux/WSL | `/etc/claude-code/managed-settings.json` | D07-S08 | 2026-09-24 |
| Managed settings file path — Windows | `C:\Program Files\ClaudeCode\managed-settings.json` (legacy `C:\ProgramData\ClaudeCode\...` is **not** read) | D07-S08 | 2026-09-24 |
| Managed CLAUDE.md path (distinct file, same tier) | Same three OS directories, filename `CLAUDE.md`; also settable inline via the `claudeMd` key inside `managed-settings.json`. Cannot be excluded by `claudeMdExcludes`. | D07-S02 | 2026-09-24 |
| Precedence across *multiple* managed sources | `managedSourcesBehavior`: default `"first-wins"` (highest-ranked source with any policy key wins, others ignored); optional `"merge"` (v2.1.242+) combines by kind of key. Order: (1) server-managed/gateway, (2) MDM/OS policy, (3) `managed-settings.json` + `managed-settings.d/*.json`, (4) Windows HKCU registry (fallback only). | D07-S08 | 2026-09-24 |
| CLAUDE.md file types/locations | Managed policy (org, all projects) → user `~/.claude/CLAUDE.md` → project `./CLAUDE.md` or `./.claude/CLAUDE.md` → local `./CLAUDE.local.md` (gitignored). All loaded and **concatenated** (not override-replaced), root-to-leaf order, `CLAUDE.local.md` last within a directory. | D07-S02 | 2026-09-24 |
| CLAUDE.md conflict resolution | **None** — because layers concatenate rather than override, a contradiction between two loaded CLAUDE.md files is *not* resolved by precedence; Claude "may pick either one arbitrarily." Contrast sharply with `settings.json`, where the same conflict has one deterministic winner. | D07-S02 | 2026-09-24 |
| CLAUDE.md imports | `@path/to/file` syntax, relative or absolute, max recursion depth **4 hops**; external imports (resolving outside the working directory) require a one-time approval dialog. | D07-S02 | 2026-09-24 |
| CLAUDE.md size guidance | Target **under 200 lines**; hard cap 4 MiB (larger files skipped entirely). Longer files reduce instruction adherence — not just token cost. | D07-S02, D07-S18 | 2026-09-24 |
| Permission rule precedence | **Deny → Ask → Allow**, first match wins; rule *specificity does not change order* — a broad deny (`Bash(aws *)`) blocks a narrower allow (`Bash(aws s3 ls)`). | D07-S06 | 2026-09-24 |
| Permission rule syntax | `Tool` or `Tool(specifier)`; wildcards `*`; a bare tool name as a deny rule removes the tool from the model's context entirely (it never sees the tool exists) — the strongest form of "remove the capability." | D07-S06 | 2026-09-24 |
| Permission modes (current set) | `default` (labeled **Manual**), `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. `manual` is now an accepted alias for `default`. | D07-S07 | 2026-09-24 |
| **Default starting mode — major shift** | On **Pro/Max/Team plans**, the built-in starting mode for interactive terminal/VS Code sessions is now **`auto`** (classifier-reviewed), not Manual. Enterprise plans and Console API keys still default to Manual (`default`). `claude -p` / Agent SDK always default to Manual regardless of plan. | D07-S07 | 2026-09-24 |
| Auto-mode classifier | A **separate model** reviews tool calls in place of a human prompt; blocks scope escalation, unrecognized infrastructure, and actions that look driven by hostile content Claude read. Explicit `ask` rules always still force a human prompt even in auto mode. Classifier requests strip tool *results* from what it sees (only user messages, non-read tool calls, and CLAUDE.md) specifically so injected content in a file/webpage can't manipulate the classifier directly. | D07-S07 | 2026-09-24 |
| Auto-mode model requirements | Direct API/Claude Platform on AWS: Opus 4.6+, Sonnet 4.6+, or a Fable model. Bedrock/Vertex/Foundry/gateway: only Sonnet 5, Opus 4.7+, Fable models. Older models (Sonnet 4.5, Opus 4.5, Haiku, Claude 3.x) unsupported anywhere. | D07-S07 | 2026-09-24 |
| Auto-mode fallback thresholds | Falls back to prompting after **3 consecutive** or **20 total** classifier blocks in a session (not configurable). | D07-S07 | 2026-09-24 |
| `bypassPermissions` mode | Skips essentially all prompts, including writes to protected paths like `.git`/`.claude`. Explicit guidance: "Only use this mode in isolated environments like containers or VMs." Org can disable via `permissions.disableBypassPermissionsMode`. | D07-S07 | 2026-09-24 |
| Sandbox implementation | macOS: built-in Seatbelt (nothing to install). Linux/WSL2: `bubblewrap` (filesystem) + `socat` (network relay), must be installed. No native Windows support (use WSL2). | D07-S09 | 2026-09-24 |
| Sandbox isolation layers | Two **independent** layers: filesystem (`sandbox.filesystem.*`) and network (`sandbox.network.*`); either can be disabled while keeping the other. | D07-S09 | 2026-09-24 |
| Sandbox `denyRead`/`allowRead` precedence | Narrower path wins regardless of allow/deny; a narrow deny holds *inside* a wider allow (a broad allow can't silently re-expose a denied secret path). | D07-S09 | 2026-09-24 |
| Hook events (current full list) | `SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Notification`, `MessageDisplay`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `Elicitation`, `ElicitationResult`, `SessionEnd`. | D07-S04 | 2026-09-24 |
| Hook enforcement guarantee | CLAUDE.md/skills are *advisory context*; only a `PreToolUse` hook (exit code 2) or a permission rule *deterministically* blocks an action "regardless of what Claude decides." | D07-S02, D07-S06 | 2026-09-24 |
| Hook admin lockdown | `allowManagedHooksOnly` (managed settings) restricts execution to managed-policy hooks only, blocking user/project/local/plugin hooks. | D07-S04 | 2026-09-24 |
| Subagent config | Markdown + YAML frontmatter (`name`, `description` required; optional `tools`/`disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `memory`, `mcpServers`, `hooks`, `isolation`). Stored at `.claude/agents/` (project, shareable) or `~/.claude/agents/` (personal). Runs in an isolated context window; up to depth-3 nested spawning. | D07-S13 | 2026-09-24 |
| Skills structure | `SKILL.md` with YAML frontmatter + Markdown body; progressive disclosure (only description loads by default, full body loads on invocation); `allowed-tools` frontmatter pre-approves tools for that invocation; `context: fork` + `agent:` runs a skill in an isolated subagent. | D07-S14 | 2026-09-24 |
| MCP config scopes | Local (default, `~/.claude.json`, per-project-private) < Project (`.mcp.json` at repo root, checked into git, team-shared) < User (`~/.claude.json`, cross-project personal). Project-scoped servers require interactive approval on first use; `-p` runs skip that prompt. | D07-S16 | 2026-09-24 |
| Headless flags | `-p`/`--print`; `--bare` skips hooks/skills/commands/subagents/plugins/MCP/auto-memory/CLAUDE.md for reproducible CI runs; `--output-format text\|json\|stream-json`; `--allowedTools`; `--permission-mode`; `--permission-prompts none` (deny anything that would need a human, don't retry). | D07-S11 | 2026-09-24 |
| GitHub Action guardrails | Two mandatory checks before any run: triggering user needs **write access** to the repo (bypassable only via explicit `allowed_non_write_users`), and the actor must be **human** unless explicitly allowlisted in `allowed_bots` (blocks bot-triggered loops). | D07-S12 | 2026-09-24 |
| OTel cost/usage metrics | `claude_code.session.count`, `claude_code.cost.usage` (USD), `claude_code.token.usage`, `claude_code.lines_of_code.count`, `claude_code.code_edit_tool.decision`, `claude_code.active_time.total`. Team attribution via `OTEL_RESOURCE_ATTRIBUTES` (custom keys like `team.id`, `cost_center`). No built-in dashboard — OTel is the "bring your own observability stack" path. | D07-S15 | 2026-09-24 |
| Seat vs. API-metered cost model | Claude for Teams/Enterprise: usage draws from a **per-seat allowance** (Standard/Premium tier, resets on rolling 5-hour + weekly windows, shared with Claude chat/Cowork) — usage inside the allowance isn't metered in dollars. Console/API and all three cloud providers: **billed per token** to the org, no seat concept. Enterprise average reported as ~$13/developer/active day, ~$150–250/developer/month, <$30/day for 90% of users — treat as a rough planning anchor, not a guaranteed figure. | D07-S19 | 2026-09-24 |
| Per-user cost attribution by deployment | Teams/Enterprise: spend-report CSV + Enterprise Analytics API. Console: Console dashboard + Claude Code Analytics API. Cloud providers (Bedrock/Vertex/Foundry): **no native per-user breakdown** — must use OpenTelemetry export, a self-hosted Claude apps gateway, or a third-party LLM gateway (e.g., LiteLLM) for per-key attribution. | D07-S19 | 2026-09-24 |
| Rate-limit sizing guidance (Console/API) | Documented TPM/RPM-per-user table decreases as org size grows (e.g., 1–5 users: 200k–300k TPM/user; 500+ users: 10k–15k TPM/user) because concurrent usage share shrinks with scale — sized at the org level, not hard-partitioned per user. | D07-S19 | 2026-09-24 |
| Runaway-cost pattern: agent teams | Agent teams (experimental, opt-in via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) use **~7x more tokens** than a standard session when teammates run in plan mode, because each teammate is a separate Claude instance with its own full context window. Documented mitigation: use a cheaper model for teammates, keep teams small, keep spawn prompts focused, shut down teammates when done. | D07-S19 | 2026-09-24 |
| Devcontainer reference firewall | `init-firewall.sh` restricts outbound traffic to an allowlist; requires `NET_ADMIN`/`NET_RAW` capabilities via `runArgs`; explicitly optional — "not required for Claude Code itself." | D07-S10 | 2026-09-24 |
| Model-pin env vars for cloud providers | `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` — without pinning, aliases resolve to Claude Code's built-in default for that provider, which "can lag the newest release and may not yet be enabled in your account." | D07-S17 | 2026-09-24 |

---

## 2. Findings per objective

### Objective 1 — Configure Claude tools and environments for teams

- **Two independent hierarchies, easy to conflate on the exam.** `settings.json` is an **override** stack (highest-precedence value wins outright, deterministic, enforced by the client regardless of what the model decides). `CLAUDE.md` is a **concatenation** stack (every applicable file loads together into one context; conflicts are *not* resolved — Claude may pick either arbitrarily). This is the single most exam-relevant distinction in this objective: "which config wins" only has a clean answer for `settings.json`/permission rules; for CLAUDE.md the correct answer to a conflict is "keep the files consistent," not "the more specific one wins." [D07-S01, D07-S02]
- **Layering model (durable):** managed (org) > CLI override (session) > project-local (individual, this project) > shared-project (team, version-controlled) > user (individual, all projects). Shared-project settings sit *above* user settings, so a team's checked-in `.claude/settings.json` is the correct place for team-wide permission rules, hooks, and MCP servers — it beats "everyone configures their own machine" for consistency and auditability, and individuals can still layer personal exceptions in `settings.local.json` without a commit. [D07-S01]
- **Secret handling in shared config:** shared settings are checked into git, so never put a static secret in `.claude/settings.json`. Documented mechanisms: `apiKeyHelper` (dynamic script), `env` blocks referencing already-provisioned environment secrets, MCP server `headers` using `${VAR}` interpolation (redacted in transcripts), and for CI, GitHub Actions secrets (`ANTHROPIC_API_KEY` / `CLAUDE_CODE_OAUTH_TOKEN`) or OIDC/workload-identity-federation to avoid a stored secret entirely. [D07-S01, D07-S03, D07-S16, D07-S12]
- **Enterprise policy delivery:** three independent mechanisms — server-managed settings (claude.ai console, polled hourly, reaches cloud sessions), MDM/OS policy (plist/registry, checked every 30 min), and a `managed-settings.json` file (read at startup, hot-reloaded on file change). All three converge on the same precedence tier; when more than one is present, `managedSourcesBehavior` decides "first-wins" (default) vs "merge." [D07-S08]
- **Team environment setup patterns:** devcontainer (reference implementation ships a firewall script + persistent auth volume) for a fully reproducible sandboxed environment; the Claude Code Dev Container Feature for lighter-weight adoption. Devcontainers, `managed-settings.json` baked into the image, and `.mcp.json` checked into the repo root together give a "clone and go" team setup. [D07-S10, D07-S16]

### Objective 2 — Improve developer workflows using AI-assisted tooling

- **Vehicle selection is the core architectural judgment** (see comparison matrix below): CLAUDE.md for durable, always-relevant project facts; Skills for on-demand reusable procedures; slash commands for fixed user-triggered actions; subagents for isolated/delegated work; MCP for external system access. Documented anti-pattern stated directly: an over-specified CLAUDE.md causes Claude to *ignore* content because "important rules get lost in the noise" — this is a token-cost problem **and** an attention/adherence problem, not just a cost problem. [D07-S02, D07-S13, D07-S14, D07-S18, D07-S19]
- **Verification-loop pattern:** the documented core practice is giving Claude something that returns a pass/fail signal (tests, build, lint, screenshot diff) so a session can "close the loop" itself instead of the human being the only verification path. Three escalating enforcement levels: ask in the same prompt < a `/goal` condition (evaluated every turn) < a `Stop` hook (deterministic gate, script-enforced, capped at 8 consecutive blocks before Claude Code overrides it). [D07-S18]
- **Explore → Plan → Code → Commit** is the documented default workflow, using Plan mode to separate research from execution; explicitly *not* recommended for small/obvious diffs ("if you could describe the diff in one sentence, skip the plan"). [D07-S18]
- **Parallelization patterns:** worktrees (isolated git checkouts per session), Writer/Reviewer two-session pattern (fresh context avoids self-review bias), and fan-out via `claude -p` loops or `/batch` for large mechanical migrations. Cost caveat: parallelization (especially agent teams) multiplies token spend roughly with instance count — documented at ~7x for agent teams in plan mode — so fan-out needs the same cost governance as any other scaling decision. [D07-S18, D07-S19]
- **Rollout pattern (pilot → champions → org-wide), from Anthropic's own scaling guide:** start with a pilot of **20–50 developers** already comfortable with AI-assisted tools — framed explicitly as "not just your early adopters... your future agentic coding champions." Give the pilot concrete artifacts to produce, not just free exploration: custom slash commands tailored to the org's codebase/standards, a checked-in project `CLAUDE.md` documenting gotchas and conventions, and an inventory of repetitive workflows worth automating. Preferred launch mechanism is a **kickoff hackathon** rather than a phased/waitlisted rollout, specifically because it lets pilot users mentor everyone else in the same room and creates adoption network effects. The pilot cohort's designed end-state is to **become internal consultants** who run their own workshops — this is the "champions" stage made concrete, not a separate program. [D07-S22]
- **Two named adoption failure modes and their fixes**, from the same guide: (1) the **"do everything" trap** — unbounded tasks with poor results — fixed by test-driven development as the guardrail (write test specs first, implement incrementally, validate at each checkpoint, expand scope gradually); (2) the **"context gap"** — vague symptom descriptions ("this isn't working") that waste iterations — fixed by over-sharing context (full error/stack trace, environment/dependency versions, before/after screenshots or terminal output for UI/CLI issues respectively). Both map onto this domain's debugging objective as much as the workflow objective: a scoped, evidence-bearing prompt is simultaneously a productivity practice and a debugging practice. [D07-S22]
- **Admin decision surface for a team rollout** (separate from the developer-facing settings/permissions surface): choice of API provider (direct/Teams-Enterprise vs. a cloud provider vs. self-hosted gateway), how managed policy reaches devices, and what usage-visibility/spend-control options exist per plan type are consolidated into one admin-facing setup flow. [D07-S23]
- **IDE surfaces are a distinct configuration/adoption lever**, not just a CLI concern: the VS Code extension and JetBrains plugin read the same settings files as the terminal but add their own affordances (inline diffs, plan review, built-in IDE MCP server for diagnostics) and their own security caveats — the JetBrains integration explicitly warns about an unencrypted `ws://` transport risk when accepting connections from all network interfaces. Rolling out "Claude Code" to a team is therefore also a decision about which surface(s) to standardize on, since permission-mode defaults and settings visibility differ slightly by surface (see §3.6 in the draft; auto-mode default behavior in particular is surface-dependent). [D07-S24, D07-S25]
- **The Claude Agent SDK is the programmatic counterpart, not a competing product.** Anthropic frames it as giving "the same tools, agent loop, and context management that power Claude Code," packaged as Python/TypeScript libraries (`claude-agent-sdk` / `@anthropic-ai/claude-agent-sdk`) for embedding the agent inside a self-hosted application/process rather than running the interactive CLI. It shares Claude Code's capability surface — built-in tools, hooks, subagents, MCP, permissions, sessions, skills/commands/memory (loaded the same way from `.claude/`), and plugins — and is explicitly distinguished from three adjacent options: the CLI itself (interactive/one-off use), the Client SDK + optional beta Tool Runner (call the Claude API directly, own the tool loop), and Managed Agents (Anthropic hosts the agent and its sandbox). A documented restriction: SDK-built products may not offer claude.ai login or claude.ai rate limits to their own end users — third-party agents must use API-key auth. To drive the same agent loop from a language other than Python/TypeScript, the documented path is running the CLI as a subprocess with `-p --output-format json`. [D07-S20]

### Objective 3 — Support debugging and operational issue resolution

- **Hypothesis-driven / evidence-based debugging is the documented discriminator.** The best-practices guide explicitly reframes vague prompts ("fix the login bug") into scoped, falsifiable ones ("users report X, check Y, write a failing test that reproduces it, then fix it") and states the rule as "address root causes, not symptoms" / "don't suppress the error." [D07-S18]
- **"Trust-then-verify gap" is a named failure mode:** "Claude produces a plausible-looking implementation that doesn't handle edge cases... If you can't verify it, don't ship it." This maps directly onto the exam guide's own Sample Item 3 pattern (confident-but-wrong output needs an evidence check, not blind trust) — this domain's version of that same discriminator applied to developer tooling rather than RAG. [D07-S18, D07-S27]
- **A long-running-agent harness confirms the same discriminator from the infrastructure side.** Anthropic engineering's own harness-design writeup for long-running coding agents describes two concrete failure patterns without a verification loop: agents "attempting too much simultaneously" and "prematurely declaring projects complete." Its fix is structurally the same as the best-practices guidance above — track a feature list with explicit pass/fail status, run an end-to-end test before trusting any "done" claim, and note that agents did not verify their own work well until *explicitly told* to "test as humans would." The same writeup flags single- vs. multi-agent harness design as an open question, not a solved one. [D07-S21]
- **A dedicated Anthropic rollout guide independently confirms the LOC-metric warning verbatim.** "Beyond simply measuring lines of code (which is [a] notoriously spotty metric), teams are finding both quantitative and qualitative ways to quantify agentic coding's impact": sprint throughput, time-to-completion, migration acceleration, developer-satisfaction surveys, onboarding speed, and cross-team collaboration are offered as the honest alternatives, alongside Claude Code's own built-in Activity Metrics (lines-of-code accepted, suggestion accept rate, DAU/session trends, spend tracking). The guide's own framing of the single most convincing signal is qualitative, not a metric at all: *"This task used to take our team a week. Now one engineer completes it in half a day."* [D07-S22]
- **Adversarial review as an operational practice:** running a fresh subagent (or the bundled `/code-review` skill) against a diff, with the reviewer seeing only the diff and stated criteria (not the implementer's reasoning), is the documented way to catch gaps before merge. Guidance also warns about over-triggering: "a reviewer prompted to find gaps will usually report some, even when the work is sound" — treat only correctness/requirement gaps as findings, not style nits. [D07-S18]
- **Log/trace triage at scale:** OpenTelemetry export (`claude_code.tool_result` events, `prompt.id` correlation, `event.sequence` ordering) is the documented mechanism for after-the-fact operational investigation across a fleet of sessions, distinct from in-session debugging. [D07-S15]
- **When to escalate to a human / stop trusting automation:** auto mode's own fallback rule is a built-in model for this — after 3 consecutive or 20 total classifier blocks, Claude Code stops trying to route around the block and returns control to a human prompt. The documented cause is usually "the classifier is missing context about your infrastructure," resolved by an administrator adding trusted-infrastructure entries — not by the developer disabling the safety layer. This is a useful analogue for a human-debugging escalation rule: repeated denial/failure is a signal to add context or hand off, not to force through. [D07-S07]
- **Productivity metrics that mislead:** OTel exposes `claude_code.lines_of_code.count` as a volume metric — the same metric Goodhart's-Law-prone teams have long over-indexed on for human developers. Nothing in the primary docs frames LOC as a *quality* or *value* signal; it sits alongside cost/token/session metrics as raw usage data. The honest framing for a rollout is: usage/attribution metrics answer "who is using it and what does it cost," not "is it making the team better" — that needs an independent measure (cycle time, defect/rollback rate, review turnaround, retention of tool usage after the novelty period). [D07-S15]

---

## 3. Comparison matrices (raw, for the draft's trade-off section)

### 3.1 Configuration layering — two hierarchies

| | `settings.json` (behavior/security) | `CLAUDE.md` (instructions) |
|---|---|---|
| Resolution model | Override — highest precedence wins outright | Concatenation — every applicable file loads together |
| Conflict handling | Deterministic (one winner per key, enforced by the client) | Non-deterministic (Claude may pick either arbitrarily) |
| Enforcement | Hard — client evaluates rules regardless of model judgment | Soft — advisory context the model tries to follow |
| Exceptions | A short list of security-sensitive keys where the stricter value wins regardless of level | Managed-policy CLAUDE.md cannot be excluded by `claudeMdExcludes`, but this is inclusion, not conflict-resolution |
| Correct team practice | Put non-negotiable policy at managed tier; team defaults in shared project file; individual tweaks in local file | Keep one, small, cross-consistent set of instructions; use path-scoped rules/skills instead of stacking contradictory guidance |

[D07-S01, D07-S02]

### 3.2 Configuration layering (settings.json precedence)

| Layer | Who sets it | Scope | Overridable by | Best for |
|---|---|---|---|---|
| Managed (`managed-settings.json`/MDM/server-managed) | Org/security admin | Every session on every reached machine | Nothing, except a short stricter-value exception list | Compliance-mandated policy, non-negotiable deny rules |
| Command line (`--settings`) | Individual, per-invocation | One session | N/A (already top of non-managed stack) | One-off testing, CI parameter injection |
| Project local (`.claude/settings.local.json`) | Individual | This project, this machine, gitignored | Managed, CLI | Personal exceptions, saved "yes and don't ask again" approvals |
| Shared project (`.claude/settings.json`) | Team, checked into git | Everyone who clones the repo | Managed, CLI, project local | Team permission rules, hooks, MCP servers, project conventions |
| User (`~/.claude/settings.json`) | Individual | Every project on this machine | All four above | Personal defaults (theme, default model, personal allow rules) |

### 3.3 Permission strategy

| Strategy | Velocity | Blast radius | Where enforced | Best for |
|---|---|---|---|---|
| Prompt on everything (Manual/`default` mode) | Lowest — every write/exec/network call stops the session | Lowest, but habituation risk ("click yes to continue") over long sessions | Human judgment per call | Sensitive/unfamiliar repos, first-time setup |
| Curated allowlist (`permissions.allow` rules) | High for the allowed set, unchanged elsewhere | Scales with rule breadth; wildcard placement matters (`Bash(git *)` ≠ `Bash(git log *)`) | Claude Code's rule engine (deny > ask > allow) | Known-safe repeated commands (lint, test, commit) |
| Auto mode (classifier) | High, broad | Bounded by classifier judgment, which only sees text/CLAUDE.md, not tool *results* — so it cannot be manipulated by injected content, but also cannot verify claims tool output would disprove | Server/local classifier model, deny/ask rules still apply first | Long autonomous tasks where a human isn't watching every call, on a supported model |
| `bypassPermissions` | Highest | Unbounded except a short hard-coded no-touch list (critical-path `rm`, cross-session messaging) | None — explicit warning to use only in an isolated container/VM | Fully unattended runs *inside* disposable, network-restricted compute |
| Sandboxing (independent of the above) | Neutral — layers under any mode | Enforced by the OS (Seatbelt/bubblewrap), not by the model's judgment | Kernel/OS | The correct way to bound `bypassPermissions`/`auto` blast radius; not a substitute for permission rules, a complement |

**Discriminator:** destructive capability belongs behind *removal from the tool surface* (a deny rule, or simply not granting the tool) or *OS-level sandboxing*, not behind a confirmation dialog a user will eventually click through by habit. This mirrors the exam guide's own Sample Item 1 rationale (remove the capability, don't add logging/confirmation). [D07-S06, D07-S07, D07-S09, D07-S27]

### 3.4 Instruction/context vehicle selection

| Vehicle | Loaded | Right for | Wrong for | Cost if misused |
|---|---|---|---|---|
| CLAUDE.md | Every session, always | Durable project conventions Claude can't infer from code (build commands, non-default style, repo etiquette) | Rarely-needed domain knowledge, long tutorials, anything Claude can derive by reading | Token bloat *and* reduced adherence — bloated files make Claude ignore real instructions |
| Skills (SKILL.md) | On demand (progressive disclosure: description always visible, body loads on invocation) | Reusable multi-step procedures, reference material used sometimes | Something that must run unconditionally on every turn (that's a hook) | Wasted authoring effort if it never triggers; under-triggering if description is vague |
| Slash commands | Invoked by name | Fixed, user-triggered actions with no need for a custom system prompt or isolated context | Delegated exploration that would pollute main context | Context pollution if used for open-ended research |
| Subagents | Spawned on delegation, isolated context window | Tasks that read many files / need restricted tools or a different (often cheaper) model, keeping the parent context clean | Simple one-shot lookups (delegation overhead not worth it) | Wasted latency/cost for trivial tasks; parent loses visibility into raw work |
| MCP servers | Connection-time; tools listed to the model | External system access (tickets, databases, docs) that no built-in tool covers | Storing instructions or conventions (that's CLAUDE.md/skills) | Capability bloat if every tool from every server is granted rather than scoped |
| Hooks | Registered at settings load, fire on lifecycle events | Actions that must happen with zero exceptions (deterministic enforcement) | General behavioral guidance (hooks are pass/fail, not judgment) | False sense of "enforced" if a hook only warns instead of exiting 2 |

### 3.5 Enterprise deployment surface

| Dimension | Claude for Teams/Enterprise (direct) | Amazon Bedrock | Google Cloud Agent Platform (Vertex) | Microsoft Foundry | Self-hosted LLM gateway |
|---|---|---|---|---|---|
| Identity/SSO | claude.ai SSO, org domain capture (Enterprise) | AWS IAM / API key | GCP credentials (ADC) | API key or Microsoft Entra ID | Whatever IdP the gateway integrates (per-IdP-group policy possible) |
| Network egress | Direct to Anthropic | Through AWS region/VPC | Through GCP region | Through Azure region | Fully operator-controlled; gateway is the enforcement point |
| Cost attribution | Per-seat allowance + usage-credit spend report (CSV)/Enterprise Analytics API; usage inside the seat allowance isn't metered in dollars | AWS Cost Explorer, usage-metered per token; no native per-user breakdown (needs OTel/gateway) | GCP Billing, usage-metered per token; same per-user gap | Azure Cost Management, usage-metered per token; same per-user gap | Gateway's own metering; enables centralized cross-team/cross-provider tracking a single cloud bill can't give |
| Model availability lag | Newest models available fastest (Anthropic-operated) | Can lag; pin with `ANTHROPIC_DEFAULT_*_MODEL` | Can lag; same pinning mechanism | Can lag; same pinning mechanism | Depends entirely on upstream provider the gateway routes to |
| Data handling posture | Anthropic's data-handling terms directly | AWS-side data boundary/compliance posture (BAA, region residency options via AWS) | GCP-side data boundary/compliance posture | Azure-side data boundary/compliance posture | Operator-defined; can add its own retention/redaction layer in front of any provider |
| When to choose | Most orgs — least infra, includes claude.ai web access, seat model gives predictable per-head budgeting | Existing AWS compliance/procurement relationship | Existing GCP compliance/procurement relationship | Existing Azure/Microsoft compliance relationship | Need centralized auth/rate-limiting/budgets across multiple providers or teams, or must avoid a per-cloud static credential (OIDC federation) |

[D07-S03, D07-S17, D07-S19]

### 3.6 Interactive vs. headless/CI usage

| Dimension | Interactive session | Headless (`-p`) / CI |
|---|---|---|
| Good fit | Exploration, pairing, judgment calls, first-time-in-a-repo work | Bounded, verifiable, repeatable tasks: lint/test triage, PR review, mechanical migration fan-out, scheduled reports |
| Poor fit | N/A (default surface) | Tasks needing ambiguous human judgment, irreversible actions with no review gate, anything where "looks done" is the only success signal |
| Default permission mode | `auto` (Pro/Max/Team) or Manual (Enterprise/Console) | **Manual**, regardless of plan — must be set explicitly (`--permission-mode`) |
| Guardrails | Human is the reviewer of record | `--allowedTools` scoping, `--bare` for reproducibility, `--permission-prompts none` for unattended runs, `dontAsk` mode for CI, GitHub Action's write-access + human-actor checks, branch protection / required PR review before merge, `--max-turns` and workflow timeouts against runaway loops |

[D07-S07, D07-S11, D07-S12, D07-S18]

### 3.7 Cost model: seat vs. API-metered

| | Seat-based (Claude for Teams/Enterprise) | API-metered (Console/Bedrock/Vertex/Foundry) |
|---|---|---|
| Budgeting | Predictable per-head cost; usage inside allowance untracked in dollars | Scales directly with consumption; harder to forecast, easier to attribute precisely |
| Runaway-usage exposure | Bounded by seat allowance + org spend limits on usage credits | Bounded only by workspace/API rate limits and any gateway-side cap you add |
| Per-user attribution | Native (spend report CSV / Enterprise Analytics API) | Native on Console; **not native** on cloud providers — requires OTel, gateway, or LLM proxy |
| Fits best when | Team wants one predictable line item and claude.ai web access bundled in | Org already meters all AI/cloud spend per-token and wants that to include Claude Code |

[D07-S19]

---

## 4. Contradictions and version sensitivity

- **Third-party prep material vs. exam guide on structure:** the exam guide explicitly states: *"There are no mandatory prerequisites or courses required to sit this exam... The credential is awarded based on exam performance alone."* One community write-up found in the landscape scan describes "5 Domains" for the Claude Certified Architect exam, which does not match the official 7-domain blueprint in this guide — a clear sign of drift, confusion with a different/earlier framing, or low editorial care. [D07-S27 vs. D07-S35]
- **Auto mode as default is a recent, plan-gated change** and is exactly the kind of fact this domain warns about: it depends on plan (Pro/Max/Team vs Enterprise/Console), surface (`-p`/SDK always defaults to Manual), model (requires 4.6-tier or later), and provider (narrower model list on Bedrock/Vertex/Foundry/gateway). A course item that says "Claude Code always asks before acting by default" is now stale; one that says "auto mode with a classifier is always on" is equally wrong for Enterprise/Console/headless. The only safe exam-durable framing is the *trade-off itself* (broad-auto vs. curated-allowlist vs. prompt-everything vs. bypass), not a specific default. [D07-S07]
- **`docs.claude.com/en/docs/claude-code/*` → `code.claude.com/docs/en/*`:** every URL pattern in the original task brief 301-redirects. Any older third-party prep material or cached course content still citing the old path is at minimum stale on link, and plausibly stale on content given how much the permission-mode model has changed underneath it.

---

## 5. Open questions / things marked [UNVERIFIED]

- Exact current seat price for Claude for Enterprise is not published (contact-sales only); the Teams "~$150/seat Premium" figure and the "~$13/day, $150–250/month" enterprise cost anchors are snapshot figures from the docs, not durable exam facts — **do not put a specific dollar figure in the course chapter as if it were stable**; mark any such number `[UNVERIFIED]`/omit it.
- Whether `auto` mode's classifier is itself billed as a separate API call in all cases, versus folded into session cost, was referenced ("notice about classifier request charges" on accounts where those requests are billed) but the exact billing mechanics were not independently re-verified beyond the docs' own statement — treat as `[UNVERIFIED]` for any precise cost claim.
- No official Anthropic content was found specifically naming "runaway agent loop" as a single canonical ops concept outside auto-mode's own fallback thresholds, `--max-turns`/workflow timeouts, and the documented agent-team ~7x multiplier; the dossier treats these mechanisms collectively as the answer.

---

## Prep-material landscape

Multiple third-party CCAR-P prep products already exist even though the certification is new (effective July 2026): Udemy courses, Preporato practice tests, CertSafari practice questions, Tutorials Dojo study guide, claudecertificationguide.com (mock exam + guide), a community GitHub repo (`avidevelops/claude-architect-exam-prep`), flashgenius.net interactive guide, and a dev.to community write-up describing a mismatched "5 domains" structure. [D07-S28–D07-S35]

**Trust assessment: all `low`.** None are Anthropic-affiliated; several show signs of rapid, likely AI-assisted content generation keyed off the public exam guide (near-identical domain/format summaries across sites, at least one directly contradicting the guide's own domain count). None should be used as a source of fact for this course. Where useful at all, they only confirm that the *format* (63 items, 120 min, domain weights) matches the public guide — which is already the primary source. Do not copy structure, question style, or claimed "practice questions" from any of these into the course material.
