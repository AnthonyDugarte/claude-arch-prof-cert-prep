# Domain 7 — Developer Productivity & Operational Enablement

**Blueprint weight: 7%.** This module follows the supplied local exam guide, which is the authority for this course. Questions below are original study exercises, not official Anthropic certification items. Claude Code changes quickly; the configuration details here were checked against the official docs on September 24, 2026. Recheck those docs and the installed version before copying a policy into production.

## What this domain asks you to do

Developer enablement means making useful work easier while keeping team behavior understandable, secure, and supportable. AI assistance can speed up discovery, implementation, documentation, and debugging, but it does not remove the need for tests, review, least privilege, and operational ownership. The architect’s job is to configure the right shared defaults, help people adopt a repeatable workflow, and diagnose problems using observable evidence.

### D7.1 — Configure Claude tools and environments for teams

Claude Code reads settings from files with different audiences. Current docs describe user settings in `~/.claude/settings.json`, shared project settings in `.claude/settings.json`, personal project overrides in `.claude/settings.local.json`, and organization-managed settings delivered through managed sources. Shared project settings are suitable for team permissions, hooks, plugins, and environment variables needed by a repository; commit them when teammates should receive them. Keep local overrides out of source control. Managed settings enforce organization policy with the highest precedence, subject to a few documented security-sensitive exceptions. Check `/status` for setting sources and use `claude doctor` for rejected entries. [Claude Code settings and precedence](https://code.claude.com/docs/en/settings) · [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory)

Do not assume every setting merges the same way. Scalar values generally follow precedence, while permission lists combine; a higher-level allow entry does not erase lower-level rules. Inspect the current permissions UI and source files when effective behavior is unclear. Environment variables can have per-key precedence distinct from the settings stack. Strict JSON means comments and trailing commas can invalidate a file. Configuration is part of the team’s software supply chain: review changes, explain why each permission exists, and validate it on a representative developer environment.

| Scope | Typical use | Good team decision |
|---|---|---|
| User | Personal model/theme defaults across projects | Let the developer choose preferences; avoid relying on these for shared security controls |
| Project shared | Repository instructions, reviewed team permissions/hooks/plugins | Commit a minimal, useful baseline and review it like code |
| Project local | Personal exceptions and experiments | Keep it untracked; diagnose differences when behavior diverges |
| Managed | Organization-wide security and administration | Apply centrally and verify delivery/precedence with `/status` |

Permission rules express `allow`, `ask`, or `deny`. These are tool controls enforced by Claude Code, whereas a prompt instruction such as “do not run deployments” merely guides model behavior. Current permissions docs evaluate deny before ask before allow; a broad deny cannot be carved out by a narrow allow. Prefer fine-grained rules for approved development commands, keep destructive or production actions denied or approval-gated, and avoid broad `Bash` approval that effectively removes review. A `Read(./.env)` denial only controls the matching Claude Code file tool; it does not establish an operating-system boundary against shell commands, subprocesses, or connected tools. Keep secrets out of the workspace and process environment when possible, avoid injecting production credentials, and use an isolated workspace or OS/container controls when access must be prevented. Verify all access paths. A `bypassPermissions` mode skips prompts and is documented for isolated containers or VMs where Claude cannot cause damage. Managed settings can disable bypass and auto modes. [Configure permissions](https://code.claude.com/docs/en/permissions)

Hooks run user-defined commands, HTTP endpoints, MCP tool calls, prompts, or agents at defined lifecycle events. Use a hook for a deterministic action such as formatting after edits, running a required check, or blocking a known unsafe command; use `CLAUDE.md` or a skill for guidance that requires model interpretation. Hooks can be configured in settings by event, matcher, and handler. A PreToolUse hook can control an attempted tool call. Hooks are powerful: command hooks execute with the developer’s user permissions, so review and test them. For policy gates, verify the event-specific failure semantics; for most events exit code 2 blocks, while a bad hook path or exit code 1 can be non-blocking. A silently non-blocking failure is a dangerous false sense of enforcement. [Hooks reference](https://code.claude.com/docs/en/hooks) · [Skills reference](https://code.claude.com/docs/en/skills)

For noninteractive `claude -p` or SDK sessions, the current hook documentation says a folder is treated as trusted without the interactive trust dialog. Review committed project settings and hook code before running against an unfamiliar repository; use an isolated environment for initial inspection. [Hooks reference](https://code.claude.com/docs/en/hooks)

Managed policy and shared config solve different problems. The repository should provide useful local context and narrow team conventions; central management should enforce organization constraints that must not be overridden. When developers report differing behavior, inspect version, launch directory, settings sources, permission mode, environment variables, and project trust before changing policy. Never commit credentials. For MCP or plugins, curate what is installed and review access scope rather than granting every developer every integration by default.

**Professional example.** A 60-person team wants Claude Code for refactoring. Platform engineering offers a reviewed repo-level baseline that allows deterministic lint and unit-test commands and installs a formatter hook. Security centrally disables permission-bypass mode. The team keeps personal model preferences in user scope. Developers work in environments without production credentials, and the team checks file access, shell commands, subprocess behavior, and MCP tools against the data boundary; `Read` denies are defense in depth, not proof of isolation. A two-team pilot compares setup friction and permission prompts, then adjusts narrow rules based on real command needs. This creates shared enablement without turning a convenient setup into universal shell authority.

### D7.2 — Improve developer workflows using AI-assisted tooling

Start by fitting Claude Code to the repository, not by asking it to infer every convention. A concise `CLAUDE.md` can explain build/test commands, module boundaries, naming, and non-obvious constraints; path-specific rules or on-demand skills can hold less frequently needed material. Avoid a giant instruction file that consumes context and conflicts with current code. Keep factual project guidance maintained by owners and validate examples.

Use a sequence that reduces rework: explore the relevant code and evidence, state an implementation plan, make a small change, run a project check, inspect the diff, and iterate. Anthropic recommends separating research/planning from implementation and giving Claude a way to verify its work; tests, builds, linters, fixtures, or screenshots provide a pass/fail signal that can close the loop. [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

Ask for bounded work with explicit context: the user-visible behavior, files or interfaces involved, constraints, examples, and a verifiable acceptance condition. A broad “clean up the app” prompt encourages unrelated edits. For an unfamiliar production bug, first request a diagnosis and evidence, then authorize a focused fix after checking the hypothesis. For code review, ask for findings with file/line evidence and severity, not an unsupported “is this good?”

| Workflow tool/pattern | Best use | Trade-off / when another wins |
|---|---|---|
| `CLAUDE.md` | Stable project facts used most sessions | Adds context each time; use a skill for rare detailed workflows |
| Skill or slash command | Reusable procedure used on demand | Model interprets it; a deterministic hook is better for mandatory invariants |
| Hook | Repeatable formatting/check/guard behavior at a lifecycle point | Adds runtime and maintenance burden; keep it fast and observable |
| Plan-first interaction | Broad, ambiguous, or risky change | Extra planning time; a tiny isolated task may need only a precise prompt |
| CLI/IDE interactive use | Collaborative work with human review | Manual throughput; scripts/CI are better for repeatable unattended jobs |

Measure enablement by useful outcomes, not raw generated lines. Candidate signals include cycle time for a defined task, review rework, test failures caught, developer-reported friction, tool cost, and adoption across roles. Anthropic documents OpenTelemetry metrics for Claude Code usage such as sessions, token usage, session cost, active time, code edit permission decisions, commits, and PR counts. These can inform operations, but lines changed or usage volume alone do not prove productivity or code quality. [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage)

**Professional example.** A developer asks for an API migration touching twelve services. The productive workflow first has Claude map call sites, identify compatibility constraints, and propose a staged plan. The team tests one service, checks the public API contract, then uses the verified pattern to continue. The developer reviews each diff and CI runs tests. This preserves human judgment and uses AI’s search/synthesis strengths while limiting the cost of a mistaken global edit.

### D7.3 — Support debugging and operational issue resolution

Debug systematically: reproduce and scope the problem; gather the precise symptom and timestamp; separate configuration, environment, network/provider, model behavior, and application-code causes; form a testable hypothesis; make one controlled change; and verify recovery. For Claude Code itself, current troubleshooting docs direct users to `/doctor` or `claude doctor` for installation/settings/extensions/context checks, `/mcp` for MCP status, and a safe-mode launch to see whether a customization such as a hook, plugin, or MCP server causes a performance problem. [Troubleshooting Claude Code](https://code.claude.com/docs/en/troubleshooting)

When a setting or hook does not apply, inspect `/status`, confirm the active source and scope, run `claude doctor`, check JSON syntax, verify the session working directory and project trust, inspect hook matchers and executable paths, and review debug output. Do not “fix” an unexplained mismatch by disabling all permissions. If runtime behavior is slow, compare a clean/safe-mode session to the configured session and remove customizations one at a time. For remote service symptoms, gather API error codes, timestamps, model/configuration, rate-limit state, and reproduction without logging sensitive prompts or code.

Claude Code’s debug logging is opt-in and can be enabled with `--debug` or `/debug`. Logs and transcripts may contain code, prompts, and tool results, so follow organizational data handling rules before sharing. OpenTelemetry usage metrics help answer operational questions like aggregate sessions and cost, but they are not a substitute for application-level traces, model quality evaluations, or user feedback. [CLI reference](https://code.claude.com/docs/en/cli-reference) · [`.claude` directory reference](https://code.claude.com/docs/en/claude-directory) · [Monitoring](https://code.claude.com/docs/en/monitoring-usage)

For an AI-assisted feature, distinguish failure classes: configuration mismatch (wrong permission or model), retrieval/data issue (missing or stale context), prompt/task mismatch, tool/API failure, model/provider availability, and downstream application defect. Preserve enough request identifiers and redacted context to correlate events. Use a known-good test case and baseline. If errors risk user harm or unauthorized action, disable the affected capability or roll back first, then investigate. A productive incident report records impact, detection, contributing factors, mitigation, follow-up owner, and a test or alert that will prevent recurrence.

**Professional example.** After a team rollout, Claude Code stops running a test hook for one developer but works for others. Start by checking the installed version and `/status`; then inspect the loaded project settings, repository trust, hook event/matcher, executable bit and path, and `claude doctor` output. Run the hook directly with a safe fixture and enable debug logging for one reproduction. If the hook path is wrong, correct it in the reviewed shared file and verify behavior on a second machine. Do not grant unrestricted Bash merely to bypass the problem.

## Failure modes and sound choices

Common errors include committing personal `settings.local.json`; using prompt text as a security boundary; approving all shell commands for convenience; assuming project settings override managed policy; writing hooks that fail open or run slowly; putting every team fact in `CLAUDE.md`; asking for a broad change without an acceptance condition; trusting model self-report instead of running checks; optimizing generated lines rather than quality; and sharing debug logs containing secrets. Operationally, avoid making several configuration changes at once, because then a successful outcome does not identify the cause.

Choose the lightest mechanism that meets the requirement. If behavior must happen identically every time, use a deterministic tested hook for local feedback or an independently enforced CI gate for release requirements. Identify who can edit or disable each control. A mutable repository hook is not an independent release gate: protect the required check and its policy outside the change being evaluated, using the organization's managed or protected execution boundary. If a choice depends on context and reasoning, provide instructions or an on-demand skill and verify its output. If an organization must prevent a mode or tool regardless of individual preference, use managed settings where supported. If the feature is risky, stage rollout and retain a human approval path. These are engineering recommendations; exact supported Claude Code keys and behavior must be verified in the version-specific official reference.

## Hands-on lab: prepare a safe team rollout

**Scenario:** A team wants Claude Code to help fix issues in a TypeScript service. Developers should be able to read and edit the repository, run lint/unit tests, and use a project MCP issue tracker. They must not read local secret files or run production deployment commands. All edits still require human review.

**Tasks:**

1. Propose a scope map for project instructions, shared settings, local preferences, and one organization-managed control.
2. Draft a small JSON permission policy with narrow test/lint allowances, tool-level denies for secret-file reads, and an ask/deny policy for deploy commands. Explain precedence and a `/status` validation step. State why those denies do not isolate secrets from shell commands, subprocesses, or MCP tools.
3. Choose one hook to improve workflow. Describe event, trigger, command, timeout, and what happens on script failure. State how you will test the hook before committing it.
4. Write a five-step prompt/workflow for a bug fix with a concrete acceptance condition and human review checkpoint.
5. Provide a diagnostic runbook for a teammate whose test hook does not run and whose session behaves differently from peers.
6. Pick two adoption measures and explain why each is more meaningful than lines generated.

**Acceptance criteria:** The shared file contains no credentials or personal preferences; the policy does not grant blanket shell access; managed policy is correctly treated as the enforcement boundary; any secret prohibition is supported by an isolated environment with no production credentials, and access paths through file tools, shell/subprocesses, and MCP are considered; the hook has a tested path and intentional failure behavior; workflow includes a runnable check and diff review; runbook checks version, source, syntax, trust, matcher/path, and logs before widening permissions; selected measures cover both quality or cycle time and user experience/cost.

## Original scenario practice

These questions are original study exercises, not official exam items.

**1. Select ONE.**

A team commits one developer’s `.claude/settings.local.json` because “that is where our test permission already works.” What is the best correction?

- **A.** Move shared, reviewed defaults to `.claude/settings.json`; keep personal overrides in the local file and out of version control.
- **B.** Move the file to `~/.claude/settings.json` and require all developers to copy it.
- **C.** Put API keys and permissions together in `CLAUDE.md`.
- **D.** Run Claude Code in bypass mode so file scope no longer matters.

**Answer: A.**

Shared project settings are designed for team-shared configuration; local settings are personal. B lacks repository-specific controlled rollout; C exposes secrets and treats prose as settings; D removes prompts and does not solve configuration ownership.

**2. Select TWO.**

A team needs formatting after every edit and also needs Claude to understand how to run a rare database migration. Which pairing is best?

- **A.** Use a tested PostToolUse hook for the deterministic formatter.
- **B.** Put the migration procedure in a skill or focused instruction file invoked when needed.
- **C.** Put both procedures only in a system prompt sentence.
- **D.** Add a broad allow rule for every Bash command.

**Answer: A and B.**

Formatting is repeatable and should run deterministically; migration guidance is conditional knowledge and can be loaded on demand. C is neither enforceable nor scoped; D grants far more authority than needed.

**3. Select ONE.**

A managed organization policy disables permission bypass, but a developer says `--settings` restored it. What should the architect conclude?

- **A.** CLI arguments always have highest precedence.
- **B.** Verify the loaded managed source and effective state; organization-managed policy takes precedence over ordinary user/project settings and session overrides, subject to documented exceptions.
- **C.** Remove the project settings file.
- **D.** Assume the developer’s behavior is impossible and close the incident.

**Answer: B.**

Settings precedence places managed policy above CLI and local files; checking `/status` and `claude doctor` grounds the diagnosis. A is false; C is unrelated; D ignores possible stale version, other launch environment, or misreported state.

**4. Select ONE.**

A hook is intended to block `git push`, but the push still runs when the script cannot be found. What is the strongest next step?

- **A.** Treat a missing hook as a configuration defect: verify the path, matcher and executable state, test in a controlled session, and confirm documented blocking semantics before rollout.
- **B.** Add “never push” to `CLAUDE.md`.
- **C.** Assume any nonzero script exit always blocks.
- **D.** Grant all Git commands automatically so Claude can retry.

**Answer: A.**

Hook behavior depends on event and exit/output semantics; a missing hook can fail non-blockingly. B is instruction, not enforcement; C is false for typical events; D worsens the permission surface.

**5. Select ONE.**

Developers say an AI coding rollout is “twice as productive” because generated lines doubled. Which evaluation plan is stronger?

- **A.** Keep lines generated as the sole KPI.
- **B.** Compare a defined task’s cycle time and review rework or defect rate, collect developer feedback, and track cost with a baseline.
- **C.** Count prompts per developer.
- **D.** Compare the largest user’s output volume across two weeks.

**Answer: B.**

It includes outcome, quality, user experience, and cost with a comparison baseline. A, C, and D are activity measures that can rise without useful delivery.

**6. Select THREE.**

One developer gets a different Claude Code permission prompt and reports that a required hook did not run. What should you inspect first?

- **A.** Installed Claude Code version and launch directory/project trust.
- **B.** `/status` and `claude doctor` to identify loaded settings and configuration errors.
- **C.** Hook event/matcher, script path/permissions, and a controlled debug reproduction.
- **D.** Immediately disable all organization rules.
- **E.** Approve unrestricted Bash as a temporary permanent fix.

**Answer: A, B, and C.**

Version and working context can affect behavior; loaded sources and validation output reveal policy state; hook configuration plus a controlled reproduction isolates the failure. D discards governance without diagnosis; E expands access and masks the issue.

## Objective checklist

You are ready to move on when you can select scopes and tools for a team (D7.1), design an AI-assisted workflow with explicit checks and measured outcomes (D7.2), and isolate Claude Code or AI-feature failures using controlled diagnostic evidence (D7.3).
