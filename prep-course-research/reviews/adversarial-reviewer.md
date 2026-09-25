# Independent adversarial review

Reviewed 2026-09-24. Scope: the complete supplied `claude-arch-professional-guide.md`, seven domain modules, capstone, 14-item advanced casebook, and supporting decision templates. This review tests architecture recommendations against counterexamples and checks internal consistency; it does not independently revalidate every external product or regulatory citation. No external pages were fetched for this pass, so there are no new source URLs or retrieval claims to add. The separate source validator owns current product/protocol verification.

## Verdict

The teaching content generally supports professional architectural judgment. It repeatedly gives conditions under which simpler workflows, direct APIs, full-document context, deterministic checks, or humans beat additional agents, MCP, retrieval, or model judges. I found no remaining high-severity authorization or action-safety defect in the inspected text. The principal limitation is assessment discrimination: most advanced items still make the correct answer conspicuous by making the other choices violate an explicit requirement.

Two medium wording corrections below should be resolved before presenting the affected passages as consistent standalone guidance. Optional improvements would deepen the professional exercises without changing the course's central recommendations.

## Must-fix wording findings

### M1 — Medium: the worked budget changes the cost boundary

**Location:** `course/08-capstone.md`, “Brief and constraints” and “Worked calculations with explicit assumptions.”

**Finding:** The brief defines a $0.04/request variable-cost ceiling “with human review and infrastructure accounted separately.” The calculation then includes $7 of “retrieval/hosting variable cost” alongside $18 of model cost and declares $25/1,000 below that ceiling. The arithmetic is correct, but the cost population changes or remains ambiguous.

**Break scenario:** Two learners compare the same systems: one excludes hosting from the ceiling, the other includes it. A design with $0.035 model cost and $0.020 variable hosting cost passes one interpretation and fails the other. Neither learner has violated the written requirements unambiguously.

**Correction:** Define the ceiling explicitly as model plus variable retrieval/tool/hosting costs, with human review and fixed overhead separately reported, and use that definition throughout. Alternatively, keep an inference-only ceiling and label the worked aggregate as a different business-case measure. Preserve separate request and accepted-draft denominators.

### M2 — Medium: low-confidence routing needs the qualification taught elsewhere

**Location:** `course/05-governance-safety.md`, “D5.3 — Make human oversight meaningful.”

**Finding:** The review-capacity paragraph offers “low confidence” among explicit risk-routing signals without identifying its source or requiring calibration. D2, the capstone and advanced A10 correctly reject uncalibrated model confidence as the sole escalation signal.

**Break scenario:** A benefits workflow routes only recommendations that the model labels uncertain. Confident but wrong recommendations bypass scarce review; aggregate confidence rises while missed high-risk cases increase. Measuring those misses eventually helps, but the local recommendation did not establish a valid routing signal.

**Correction:** Say “validated risk signals, such as conflicting evidence, missing required support, unusual amounts, or confidence scores calibrated against adjudicated outcomes; never model self-reported confidence alone.” Retain the requirement that a mandatory human decision cannot be bypassed to manage capacity.

## Optional improvements

### O1 — Medium: make a subset of advanced questions genuinely close decisions

**Location:** `course/10-advanced-casebook.md`, especially A3, A5 and A13.

**Finding:** The answer keys are consistent with the stated scenarios, and I found no clear multiple-answer ambiguity. However, many distractors announce their own defect: A3 says fewer tokens “always” mean cheaper outcomes or accepts known missing exceptions; A5 says direct APIs cannot support agents; A13 relies on prose, assumed file-rule coverage, or final-answer-only redaction. These are useful boundary checks but remain easy for a professional candidate.

**Break scenario:** A learner scores 14/14 by rejecting absolutes and choosing the longest answer, but cannot choose between two architectures that both meet authorization and quality requirements while trading operational cost against latency.

**Correction:** Replace a few distractors with credible, constraint-compliant alternatives. For example, compare a validated direct router against a single capable model with explicit measured p95, missed-escalation rate, and cost per accepted task; compare a cached approved full document against authorized hybrid retrieval when both meet quality but differ in freshness and operational burden. State the deciding constraint so there remains one defensible best answer. Keep current safety-boundary items as warmups.

### O2 — Medium: turn idempotency into one executable failure exercise

**Location:** `course/01-solution-design.md`, D1.2 and practice question 4; `course/10-advanced-casebook.md`, A9.

**Finding:** The text correctly requires reconciliation after ambiguous write outcomes. It would teach more if one example specified the downstream idempotency contract instead of stopping at “idempotency key” or “prevents duplicate execution.”

**Break scenario:** An application records an action ID locally, the downstream refund commits, and the local process crashes before recording success. A retry with the same local ID still duplicates the refund if the downstream service does not enforce deduplication. A separately reviewed request can also change parameters under an old approval unless the executor rejects that mismatch.

**Correction:** Add a hypothetical executor contract: stable key scoped to tenant and operation; atomic deduplication with the actual side effect or documented provider support; same key plus different parameters rejected; outcome lookup; defined deduplication lifetime; unknown results remain pending and require reconciliation. Include a crash-after-commit trace. If the provider offers neither deduplication nor reliable lookup, explain when automatic retry must stop. This expands an already sound recommendation rather than correcting a claimed guarantee.

### O3 — Low: define the streaming boundary in the revocation exercise

**Location:** `course/08-capstone.md`, “Challenge injections,” ACL revoked after retrieval but before draft delivery.

**Finding:** The capstone correctly requires current authorization at use/delivery and suppression of newly unauthorized evidence. It does not specify whether any draft bytes can already be streamed to a recipient before the final authorization check.

**Break scenario:** An implementation streams sensitive contract text while generating, then suppresses the completed draft after discovering revocation. The final object is blocked, but earlier bytes have already been disclosed.

**Correction:** For this exercise, require buffering sensitive draft content until the delivery check passes, or explicitly define and test the authorization/revocation policy for streaming. Include in-flight responses and stored conversation context when testing invalidation. Previously disclosed information cannot be recalled merely by invalidating a cache.

### O4 — Low: distinguish hook convenience from an independent release gate

**Location:** `course/07-developer-enablement.md`, D7.1 hooks and “Failure modes and sound choices.”

**Finding:** The module usefully warns about non-blocking hook failures and secret access through subprocesses. Its recommendation of a deterministic hook “or normal CI gate” could be sharpened where enforcement must survive repository edits or local configuration changes.

**Break scenario:** A mandatory quality check runs as an editable repository hook; a generated change modifies or bypasses that hook, and local execution reports success. Deterministic behavior of the current script does not establish independent enforcement of the policy.

**Correction:** Ask who may alter the hook and which independent protected gate verifies the requirement. Use local hooks for feedback; when the requirement is a release invariant, identify the centrally managed or protected execution boundary. This is relevant to the module's stated team configuration and mandatory-invariant goals, not a request for a general security checklist.

## Counterexamples the course already handles well

| Challenge | Inspected response and assessment |
|---|---|
| A prompt says “authorized” but the caller guesses another account ID | D2/D3 require trusted object-level authorization and tenant identity outside model control. Sound. |
| Revoked evidence survives in a cache or citation | D3 plus the capstone require invalidation and checks at use/delivery; advanced A6 distinguishes relevance from authorization. Sound, with streaming refinement above. |
| MCP accepts a valid token intended for another service | D3 distinguishes recipient validation, downstream authorization and forbidden passthrough. Source semantics remain subject to the separate validator. |
| A write times out after commitment | D1 distinguishes accepted, committed and delivered states and directs reconciliation rather than a new transaction. Sound; optional contract exercise above deepens it. |
| Human approval becomes a rubber stamp or queue timeout | D5 and A10 require evidence, authority, effective override and sufficient capacity; the capstone preserves review when overloaded. Sound. |
| More agents, MCP, RAG or review must always be better | All relevant modules provide simpler alternatives and applicability boundaries. No universal technology mandate found. |
| Claude Code file denial is bypassed by shell access | D7 explicitly covers shell, subprocesses and MCP, removes production credentials and requires environment isolation where necessary; A13 reinforces it. Sound. |

## Numerical and scoring checks

- D1 labor arithmetic: `4 − 1 − 0.2 × 2 = 2.6` minutes is correct under the stated assumptions.
- D2 cascade arithmetic: `1 + 0.30 × 5 = 2.5` cost units is correct; it explicitly excludes additional overhead.
- Capstone: `$25 / 1,000 = $0.025`; `$25 / 900 ≈ $0.0278`; 30 seconds at $30/hour is $0.25, ten times $0.025. Correct. M1 concerns scope, not arithmetic.
- Cache inequality `n(B−R) > W−R` follows correctly from comparing `nB` with `W + (n−1)R`; the text states actual hits and eligibility assumptions.
- The capstone correctly rejects adding component p95 values as if that measured end-to-end p95.
- The README's illustrative hours sum to 40. The orientation does not equate scaled 720 with 72% raw accuracy.
- The revised capstone gate requires 2/2 in four critical areas and pass/fail demonstrations before the overall 12/16 learning threshold. The earlier numeric-gate defect is resolved in the inspected revision.

## Previously reported issues and review limits

The primary review's missing D4 lab-fixture promise was revised during this pass into an explicit construction exercise with sample cases and a reproducibility manifest. I do not list that original defect as still open. Likewise, the critical capstone evidence gate was strengthened as described above. The advanced casebook now exists and adds useful cross-domain cases; O1 assesses its remaining difficulty rather than reporting it as absent.

These findings are based on a concurrently edited working tree. The two wording findings are recorded as observed and supplied to the author for correction; their final disposition should be recorded during consolidation. No teaching content was edited by this reviewer.

## Closure check — 2026-09-24

Re-read the changed teaching passages and `reviews/resolution-record.md`. **No remaining blockers from this adversarial review.** The earlier findings above remain a historical record; this closure states their current disposition.

- **M1 resolved:** the capstone ceiling now includes model plus variable retrieval/hosting, while human review and fixed infrastructure are separate. The worked calculation uses that same boundary.
- **M2 resolved:** D5.3 now requires validated risk signals and calibrated uncertainty and expressly rejects model self-reported confidence alone.
- **O1 materially improved:** advanced A3 now supplies three measured quality/latency/cost alternatives, with only the cached full-context path satisfying both stated release gates. A5, A7 and A13 replace several implausible distractors with recognizable engineering approaches and explain why they lose under the scenario constraints. The keys remain consistent. Some other items are still straightforward boundary checks; the set remains mixed-difficulty learning practice, not a calibrated professional exam simulation, as its introduction states.
- **O2 addressed:** D1.2 now specifies a hypothetical downstream deduplication contract, parameter binding, replay behavior, lifetime, lookup and crash-after-commit exercise. It does not imply a local action ID alone guarantees idempotency and stops automatic retry when safe reconciliation is unavailable.
- **O3 addressed:** the capstone explicitly buffers sensitive draft text until delivery authorization passes and tests in-flight responses, stored context, caches and citations. The annotated revocation example reinforces that behavior without claiming already disclosed bytes can be recalled.
- **O4 addressed:** D7 now distinguishes editable local hooks from independently protected release gates and identifies control mutability as part of the boundary.

The added capstone exemplar also clearly separates a simulated authorization test from an operational latency failure and withholds promotion when the latter misses its target. These changes close the requested adversarial findings without introducing a new answer-key or arithmetic defect in the revised passages. External-source verification remains the separate validator's responsibility.
