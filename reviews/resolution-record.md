# Review resolution and completion evidence

Date: 2026-09-24. Independent reports are preserved as findings against the versions each role inspected; this record connects them to the revised pack. Review roles did not rewrite one another's reports or teaching content. The lead author applied corrections.

## Findings and disposition

| Review finding | Revision | Verification |
|---|---|---|
| Reviewer: D4 lab implies supplied fixtures that do not exist | D4 lab now explicitly asks learners to construct 60 cases and paired snapshots/traces; gives type counts, required fields, three example failure rows and reproducibility manifest | Inspect D4 practical lab; no supplied trace/dataset claim remains |
| Reviewer: capstone numeric threshold permits missing critical evidence | Four critical areas require 2/2 artifact-plus-test evidence; negative authorization/revocation and diagnosis demonstrations are pass/fail prerequisites | Inspect capstone acceptance rubric before applying 12/16 learning score |
| Reviewer: practice too easy to exercise tradeoffs | Added 14-case supplement, two/domain, with decision defenses; revised A3 to compare measured alternatives against two gates and A5/A7/A13 to use more credible competing approaches | Module checks remain warmups; advanced practice is not a calibrated exam or score predictor |
| Reviewer: attempts versus executed unauthorized actions | D4 Q3 explicitly states a prespecified attempt-rate promotion gate and that executor blocks calls | Question key follows the stated gate without conflating attempts with effects |
| Reviewer: D2 account-tool relevance absent | D2 Q2 explicitly includes both arbitrary-ID retrieval and account-read tools | Both selected controls map to a named data path |
| Reviewer: D1 write exercise underspecified | Names approved-reply record, stable key, create-or-return and read-back reconciliation | D1 lab now supplies action/contract boundary |
| Reviewer: self-study exemplar missing | Capstone adds an annotated simulated revocation artifact and a failed-latency release decision | Example distinguishes evidence for a case from global assurance |
| Adversarial M1: inconsistent budget scope | Ceiling now explicitly includes model plus variable retrieval/hosting; human and fixed infrastructure are separate | Worked $25/1,000 arithmetic uses the same boundary |
| Adversarial M2: unspecified confidence routing | D5 calls for calibrated uncertainty and validated risk signals; rejects self-reported confidence alone | Consistent with D2, capstone and A10 |
| Adversarial O2: idempotency contract too implicit | D1 specifies downstream atomic deduplication, parameter binding, lookup, lifetime and crash-after-commit exercise; stops automatic retry where reconciliation is unavailable | Clearly hypothetical application contract, not universal provider guarantee |
| Adversarial O3: streaming disclosure before revocation check | Capstone buffers sensitive text until delivery authorization; covers in-flight responses and stored context | Cannot claim invalidation recalls already disclosed bytes |
| Adversarial O4: mutable hooks versus independent gate | D7 distinguishes local feedback hooks from protected release requirements and asks who can alter controls | Separates deterministic execution from independent enforcement |
| Validator: missing navigation files | Added coverage map, consolidation handoff, reference inventory and this resolution record | Structural audit checks every local file link |
| Validator: headless hook trust nuance | D7 adds `claude -p`/SDK trust behavior and review/isolation before unfamiliar-repository execution, citing hooks docs | Follows independently opened source in validator log |
| Lead check: inconsistent selection-count formatting | Standardized D4–D7 single/select-three item labels | Structural audit checks 42 module items plus 14 advanced keys |

## Requirement-by-requirement evidence

| User requirement | Authoritative evidence in this pack |
|---|---|
| Build preparation material from supplied Professional guide | Seven modules map all 38 detailed objectives; coverage map plus independent reviewer inspection against the original guide |
| Dedicated search for each section | `research/guide-sections.md` has 16 actual queries and outcomes; three domain research logs have additional dedicated technical queries |
| Researcher, reviewer, validator and adversarial reviewer | Separate researcher outputs and three independent reports; role/model table in CONSOLIDATION.md |
| Do not use Astra for every subagent | Sol researchers/reviewer/validator and Luna researcher, alongside inherited researcher and Astra adversarial reviewer |
| Find preparation resources | Orientation links official Professional path, public Academy catalog/syllabus and technical readings; access limits in guide register |
| Define concepts with example situations | Explicit objective sections, scenario comparisons, worked calculations and original decision practice in each module |
| Professional focus on tradeoffs and established approaches | Alternatives tables, “when another wins” reasoning, professional casebook, capstone and failure exercises; primary engineering/specification sources |
| Keep this team's results in a subfolder at initial handoff | Originally delivered in `prep-course-research/`; promoted to the repository root at the user's request on 2026-09-25. The original guide remains intact |
| Track referenced material | `references.md` deduplicates external URLs and backlinks; registers record dates, exact queries, claim support and access/uncertainty |

## Verification limits

The structural checker verifies expected objective headings, item counts, answer selection counts and local file links. The independent reviewer inspected teaching substance; the validator freshly checked selected volatile/high-risk source claims; the adversarial reviewer tested boundaries and calculations. None of these proves empirical model performance, legal compliance or exam readiness. No paid API runs or production deployment were performed; labs are learner exercises. Full remote URL availability and every source claim were not independently re-audited. Exam-policy details remain attributed to the supplied guide where public verification was unavailable. These are documented boundaries, not missing promised execution.

## Final closure

All three independent roles rechecked the revised files and appended closure to their own reports on 2026-09-24. The educational reviewer closed every original finding; the validator closed both integration findings; the adversarial reviewer closed both must-fix findings and all four optional improvements. No reported must-fix remains open.

Final command: `python3 tools/audit_materials.py --write-indexes`. Result: **38 objective headings, 42 module questions, 14 advanced questions, 64 distinct external URLs; structural audit passed**. An additional cross-check found **no course URL absent from the research registers**. The final pack contains 23 Markdown files plus the audit utility. The source guide's SHA-256 at handoff is `fc67cf6a30b963879bb26a40ed93d4e0ed008a58f03a15cd747e42ec2e39ae74` for later version comparison.
