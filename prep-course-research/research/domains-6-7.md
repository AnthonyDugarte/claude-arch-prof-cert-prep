# Research record: Domains 6 and 7

**Research date:** 2026-09-24. **Scope:** supplied local blueprint, Domain 6 Stakeholder Communication & Lifecycle Management and Domain 7 Developer Productivity & Operational Enablement. The local file `claude-arch-professional-guide.md` is treated as the requested course blueprint only; this work does not establish that it is a publicly published or official Anthropic certification guide. The two course modules contain original teaching material and original practice items, not official exam questions.

## Blueprint mapping

The local guide gives Domain 6 a 14% weight and these five tasks: structured discovery and requirement gathering (mapped here to **D6.1**); communicate architecture decisions and trade-offs (**D6.2**); manage feedback and align expectations including SLAs (**D6.3**); document architecture and implementation guidance (**D6.4**); support discovery through design, handoff, monitoring, and iteration (**D6.5**). It gives Domain 7 a 7% weight and three tasks: configure Claude tools/environments for teams (**D7.1**); improve developer workflows with AI-assisted tooling (**D7.2**); support debugging and operational issue resolution (**D7.3**). These D6.x/D7.x labels are course labels applied to the exact objective order, not labels from the source blueprint.

## Dedicated search log

Searches below were run on 2026-09-24 through web search; indexed snippets were used only to discover sources, and claims in the modules were checked against the opened source where marked.

### Domain 6 query group

- `site:docs.anthropic.com/en/docs/claude-code/settings settings.json user project local managed settings scope`
- `site:docs.anthropic.com/en/docs/claude-code/permissions Claude Code permissions allow deny ask rules`
- `site:docs.anthropic.com/en/docs/claude-code/hooks Claude Code hooks lifecycle hooks`
- `site:docs.anthropic.com/en/docs/claude-code best practices team deployment Claude Code enterprise managed settings`
- `site:sei.cmu.edu architecture decision records stakeholders documentation software architecture`
- `site:martinfowler.com/articles/architecture-decision-records.html ADR`
- `site:nasa.gov systems engineering stakeholder expectations requirements lifecycle handbook pdf`
- `site:nist.gov AI RMF lifecycle monitor AI system stakeholders`

### Domain 7 query group

- `site:docs.anthropic.com/en/docs/claude-code Claude Code settings permissions hooks managed settings team deployment`
- `site:docs.anthropic.com/en/docs/claude-code Claude Code settings scopes hooks permissions managed policies`
- `site:code.claude.com/docs/en/claude-code "debug" "Claude Code" troubleshooting logs`
- `site:code.claude.com/docs/en/claude-code workflows tests debugging Claude Code best practices`
- `site:code.claude.com/docs/en/claude-code "permissions" "hooks" "managed-settings" enterprise`
- `site:code.claude.com/docs/en/claude-code team settings shared project settings deployment`

### Cross-domain operational / reliability query group

- `SEI architecture decision records stakeholder documentation architecture viewpoints ISO 42010 official`
- `Google SRE service level objectives error budgets stakeholder expectations official book`
- `site:sei.cmu.edu architecture decision records stakeholders documentation software architecture`
- `site:martinfowler.com/articles/architecture-decision-records.html ADR`
- `site:nasa.gov systems engineering stakeholder expectations requirements lifecycle handbook pdf`
- `site:nist.gov AI RMF lifecycle monitor AI system stakeholders`

Queries sometimes returned multilingual versions or older indexed Anthropic docs. The current documentation links below resolve to `code.claude.com`; final Claude Code claims use pages opened there on the research date. Exact technical behavior, defaults, and available settings can change and should be checked against the reader’s installed version and current docs.

## Source register

Access date for all entries: **2026-09-24**. “Opened” means the linked first-party page was opened and read in the research session, rather than only appearing as a search result. Search-result discovery does not serve as a citation in the course files.

| ID | Title and URL | Status | Claims supported | Limits / uncertainty |
|---|---|---|---|---|
| S1 | [Supplied local blueprint](../../claude-arch-professional-guide.md) | Opened locally | Domain weights, exact objective wording, task order | This is the provided local course reference; research does not authenticate its public or official status. |
| S2 | [NASA Systems Engineering Handbook: Appendix and glossary](https://www.nasa.gov/reference/system-engineering-handbook-appendix/) | Opened | Stakeholder definition; expectation versus requirement; expectations elicitation across life-cycle phases; validation against baseline expectations | NASA context is systems engineering and not an exam requirement or prescriptive process for every software/LLM project. |
| S3 | [SEI, “A Structured Approach for Reviewing Architecture Documentation”](https://www.sei.cmu.edu/library/a-structured-approach-for-reviewing-architecture-documentation/) | Opened | Architecture documentation should serve stakeholder readers; stakeholder-centered review can reveal gaps | The opened SEI page provides abstract/metadata; full report is linked separately. Do not imply one mandatory documentation framework. |
| S4 | [Martin Fowler, “Architecture Decision Record”](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html) | Opened | Concise durable decision record; preserve context, rationale, alternatives and consequences; supersede changed decisions | This is practitioner guidance, not a formal standard. Templates/status names are conventions. |
| S5 | [Google SRE Book, “Service Level Objectives”](https://sre.google/sre-book/service-level-objectives/) | Opened | SLI measures service level; SLO sets target; published SLOs align user expectations; target selection is contextual | General SRE service reliability guidance; AI quality and safety require additional task-specific measures. |
| S6 | [Google SRE Book, “Embracing Risk”](https://sre.google/sre-book/embracing-risk/) | Opened | Reliability has cost/opportunity trade-offs; align system risk with business tolerance | Google operational practices are an informative primary organizational source, not universally binding. |
| S7 | [NIST AI Risk Management Framework](https://airc.nist.gov/airmf-resources/airmf/) | Opened | Voluntary AI risk resource; Govern/Map/Measure/Manage functions; multiple actors and criteria across lifecycle | NIST page says AI RMF 1.0 is being updated. It is voluntary, not a law or an Anthropic certification requirement. |
| S8 | [Claude Code settings and precedence](https://code.claude.com/docs/en/settings) | Opened | User/shared-project/project-local/managed scopes; commit team settings, local overrides, managed precedence; `/status`, settings validation, list merge caveats | Highly version-sensitive; exact settings keys and exceptional precedence behavior change. |
| S9 | [Claude Code permissions](https://code.claude.com/docs/en/permissions) | Opened | Allow/ask/deny rules; order and scope; permission modes; `bypassPermissions` caution and managed control | Verify current rule syntax and mode availability/version. Effective control depends on configured Claude Code environment. |
| S10 | [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks) | Opened | Hook types/events/configuration; PreToolUse purpose; command hooks run with user privileges; event-specific failure and exit behavior | Extensive evolving reference. Blocking semantics vary by event and hook type; never generalize one exit-code rule to every hook. |
| S11 | [Claude Code best practices](https://code.claude.com/docs/en/best-practices) | Opened | Explore/plan/code flow; provide checks that verify work; examples of runnable criteria and iterative verification | Product-specific guidance, not guaranteed productivity evidence. |
| S12 | [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory) | Opened | Current purposes/scopes of `CLAUDE.md`, settings, hooks, skills, local settings, managed settings and MCP config | Directory contents and behavior may differ across versions and product surfaces. |
| S13 | [Claude Code troubleshooting](https://code.claude.com/docs/en/troubleshooting) | Opened | `/doctor` and `claude doctor`, `/mcp`, safe mode, configuration and performance troubleshooting | Page directs to other references for issue-specific steps; procedures evolve. |
| S14 | [Claude Code monitoring and usage](https://code.claude.com/docs/en/monitoring-usage) | Opened | OpenTelemetry session, cost, token, active-time, permission decision and code activity metrics | Usage metrics are not direct measures of engineering quality or business productivity. Availability of metric attributes is version-dependent. |
| S15 | [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference) | Opened | CLI flags, including debug/verbose and diagnostic affordances | Dynamic docs; command flags should be verified against installed CLI release before runbook publication. |
| S16 | [Claude Code communications kit](https://code.claude.com/docs/en/communications-kit) | Opened | Team enablement/adoption framing and selecting realistic first tasks | Adoption advice is contextual, not a required rollout method. |
| S17 | [Claude Code IAM](https://code.claude.com/docs/en/iam) | Opened | Claude Code identity/authentication options and organization considerations | Provider and plan support may change; module does not prescribe an authentication vendor. |
| S18 | [Claude Code skills reference](https://code.claude.com/docs/en/skills) | Opened | Skills are on-demand procedures/reference material; project and personal scope; skills versus deterministic commands | Product-specific behavior changes; verify current feature support and version. |

## Findings and application to objectives

### D6.1 — Discovery and requirements

NASA’s glossary distinguishes qualitative stakeholder expectations from requirements expressed in verifiable terms. This supports teaching a preserve-then-translate method: capture the stakeholder’s wording and context, then make an outcome measurable with a population, conditions, threshold, owner, and validation method. Applied LLM recommendation: include task quality and user workflow measures alongside latency or availability, since the latter do not establish answer correctness. That distinction is the course’s engineering synthesis, not a quoted NASA prescription.

### D6.2 — Decisions and trade-offs

ADR guidance and SEI documentation review support a concise rationale plus meaningful alternatives and consequences, communicated through audience-appropriate views. Course advice to record uncertainty, confidence and a revisit trigger is a practical extension. The exact ADR template is explicitly called a convention rather than a standard.

### D6.3 — Feedback loops, expectations and SLAs

Google SRE’s SLI/SLO/SLA distinctions support precise service commitments and targets grounded in user concerns and business trade-offs. The module warns against treating API availability as AI answer quality; this follows from metric scope, and is a course recommendation. Error budgets are presented as a negotiation mechanism for service reliability versus feature work, not as a direct quality-control metric for generated answers.

### D6.4 — Architecture documentation and guidance

SEI’s stakeholder-centered review method supports tailoring views for the developers, operators, business owners, and governance roles who will use the architecture. NASA’s V&V plan outline gives examples of responsibilities, architecture context, verification/validation methods, and acceptance tests. The module applies those concepts to implementation sequencing, ownership, runbooks, and rollout evidence without claiming a required document format.

### D6.5 — Lifecycle

NASA’s life-cycle framing and NIST AI RMF’s ongoing Govern/Map/Measure/Manage functions support lifecycle work beyond design sign-off. The module’s rollout, versioning, evaluation, monitoring, feedback, and retirement practices are recommendations synthesized from those sources. The NIST framework is voluntary and explicitly under revision at access time.

### D7.1 — Team tool and environment configuration

Current Anthropic docs support configuring user, shared project, project-local, and managed settings; the managed tier is generally highest precedence, while some security-sensitive settings have documented exceptions. Permissions are enforced by Claude Code and separate from natural-language instructions. Hooks can be deterministic workflow automations but execute according to event-specific semantics; command hooks run with user permissions. Therefore, shared policy should be minimal and reviewed, central policy reserved for organization-wide constraints, and hooks tested for failure behavior. This is an architecture recommendation derived from docs, not a vendor-mandated rollout.

### D7.2 — AI-assisted workflow improvement

Anthropic’s current best-practice page recommends exploration and planning before broad coding and encourages a runnable verification method. The module develops that into bounded prompts, review checkpoints, and measures covering delivery quality, cycle time, developer experience, and cost. Official Claude Code monitoring exports use and activity metrics, but no supplied source establishes generated lines or usage as productivity proof; the module explicitly avoids that inference.

### D7.3 — Debugging and operational support

Claude Code troubleshooting docs document `/doctor`/`claude doctor`, `/mcp`, safe mode, and targeted troubleshooting. The settings page adds `/status`, and hooks docs describe debug and failure behavior. The course runbook uses these tools in a controlled diagnostic sequence: record version/context, inspect effective configuration, isolate customizations, reproduce once, change one factor, and verify. The data-sensitivity guidance for logs is a professional security recommendation; logs and transcripts may include prompts, code, and tool output, so apply local handling policies.

## Uncertainty and boundaries

1. The prep blueprint is supplied as a local file. No conclusion here verifies it against any public certification guide, live exam, or Anthropic program page.
2. Claude Code evolves rapidly. Settings, model names, commands, permissions, hook lifecycle events, and telemetry fields may change after 2026-09-24; the module intentionally gives current docs precedence and recommends checking the installed version.
3. ISO/IEC/IEEE 42010 was searched in an initial query, but no accessible primary standard was opened. The course therefore does not assert that any given architecture artifact is required for 42010 conformance.
4. The architecture, discovery, and lifecycle materials are cross-domain professional practices. The local blueprint gives objective headings but no normative templates, numeric thresholds, or official task-level subcodes.
5. NIST AI RMF is voluntary, and its official resource page stated that a revision was in progress as of access date.
