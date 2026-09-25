# Orientation: what to study and how to use the evidence

## The scope of this course

The [supplied guide](../../claude-arch-professional-guide.md) describes a practitioner who owns the lifecycle of a Claude system. Read its Sections 1–4 together: individual prompt fluency is insufficient. The candidate must connect business value, architecture, implementation, evaluation, security, and operations. Its recommended experience is three or more years in architecture/platform work and six or more months with production LLM systems; these are recommendations, not mandatory prerequisites.

Use this baseline check before studying. Can you explain why a workflow beats an agent in one task, but loses in another? Trace user identity from request to a retrieved document and a tool side effect? Distinguish a retrieval miss from unsupported generation? Estimate cost per accepted task including retries and human review? Name the owner who can stop an unsafe release? If any answer is vague, prioritize the corresponding module and lab.

## Exam facts: preserve the source boundary

The following are **facts stated in the supplied July 2026 guide**, not independently revalidated booking promises. Section 16 says the guide may change. Confirm the program's current policy and appointment instructions before paying or scheduling.

| Guide section | What the supplied guide says | Preparation implication |
|---|---|---|
| 5, 9 | 63 multiple-choice/multiple-response items; 120 minutes; each item specifies how many answers to select | Practice selecting exactly the requested count; the average budget is about 114 seconds per item |
| 5, 9 | Passing scaled score 720 on a 100–1,000 scale; domain percentages accompany the result | **720 is not evidence of a 72% raw pass mark.** No raw-to-scaled conversion is supplied |
| 5 | $175 USD fee; validity 12 months | Recheck checkout price, eligibility, and the current renewal terms |
| 10 | Start in Partner Academy, then use Pearson instructions; cancellation/rescheduling up to 24 hours before appointment | Set reminders using the actual appointment timezone and current policy |
| 11 | Matching valid government photo ID; accommodations approved before scheduling | Resolve name discrepancies and accommodations before booking |
| 11 | Retake waits 14, 30, then 90 days after successive failures; four attempts per rolling 12 months | Budget time for learning, not repeated immediate attempts |
| 12–13 | Proctor rules, no unauthorized aids or content capture, NDA required | Use original practice material; follow actual program and proctor instructions |
| 14 | Free non-proctored on-time renewal; lapsed credentials require the full exam; major changes can require re-examination | Track award date and check updated requirements before renewal |
| 15 | Program support routes, a 14-day appeal window, and privacy policies | Read the exact guide and current program policy for the applicable trigger and support channel |

No mandatory prior certification does not mean unrestricted registration. Anthropic's public [certification announcement](https://claude.com/blog/four-role-based-claude-certifications) says exam access is through the Claude Partner Network. The indexed [program FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) says Professional does not formally require Foundations, but direct retrieval of that FAQ returned 403 during this research. Treat registration access and learning prerequisites as different questions and confirm current eligibility in the program portal.

The generic Pearson [OnVUE requirements](https://www.pearsonvue.com/us/en/onvue/requirements.html) call for a system test and controlled testing environment; program-specific exceptions and appointment instructions matter. The [accommodation page](https://www.pearsonvue.com/us/en/test-takers/accommodations.html) directs candidates to their specific exam program. Generic rules from another certification are not evidence for CCAR-P policies.

## A curated preparation path

The [official Professional prep path](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional) was discoverable through indexed first-party content, but its full page returned 403. The indexed overview lists architecture, production integration, safety/risk, stakeholder/lifecycle and team-enablement lessons. This establishes a relevant resource to visit; we did **not** audit its gated lesson content or claim its completion guarantees passing.

The public [Claude Academy catalog](https://academy.claude.com/courses) is readable. These resources complement the seven-domain blueprint; course completion badges and professional certification are distinct.

| Resource | Use it for | Follow-up task in this pack |
|---|---|---|
| [Building with the Claude API](https://academy.claude.com/courses/building-with-the-claude-api) | Implementation grounding across prompts, tools, retrieval and evaluation | D1–4: build a measured request path rather than memorize SDK syntax |
| [Academy catalog: MCP introduction and advanced topics](https://academy.claude.com/courses) | Integration vocabulary and protocol mechanics | D3: justify MCP versus a direct API and secure either choice |
| [Academy catalog: agent skills and subagents](https://academy.claude.com/courses) | Reuse and delegation mechanics | D1–2: demonstrate when added orchestration is worth its overhead |
| [Academy catalog: Claude Code in action and AI-native SDLC](https://academy.claude.com/courses) | Engineering workflows | D7: prove productivity with reviewed, tested changes |
| [Academy catalog: AI capabilities/limitations and AI fluency](https://academy.claude.com/courses) | Shared concepts and human oversight | D5–6: explain uncertainty and assign accountable reviewers |
| Technical sources cited inside each module | Current behavior, constraints and specification details | Recheck volatile features against your chosen deployment platform |

Read the [API course syllabus](https://academy.claude.com/courses/building-with-the-claude-api) selectively if you already know the basics. It includes practical retrieval, tool-use, evaluation and orchestration topics. This pack adds architecture decisions, failure analysis and cross-domain defenses; reading alone does not replace implementation experience.

## How to answer professional scenarios

First extract the business outcome, explicit constraints, trust boundaries and failure cost. Eliminate choices that violate a hard constraint before comparing desirable features. Prefer evidence tied to the stated trigger: after an index refresh, inspect retrieval; after a prompt change, compare prompt versions with fixed inputs. A larger model is not a substitute for authorization or valid source data.

Do not learn slogans as universal rules. Removing unused dangerous tools is appropriate least privilege; removing a required capability may break the business objective. A bounded workflow is easier to test for predictable tasks; open-ended research can justify an agent. Human approval helps only when reviewers have time, evidence, authority and a safe default on timeout.

For the guide's Section 8 samples, the supplied key is **B, C, B**. Explain why monitoring cannot replace removing unnecessary privilege; why a stable cacheable prefix can help repeated work; and why a document-refresh failure points first to retrieval/indexing. Then change the constraint and explain when a different architectural choice would become sensible.

For practice, use an error journal: objective ID; your answer; missed constraint; strongest rejected alternative; evidence to collect next; retest date. Reattempt with a different scenario, not just the same answer order. You may time the original module questions, but their number, difficulty and domain mix do not reproduce a full calibrated exam.
