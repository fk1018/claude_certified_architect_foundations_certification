# Enterprise Integration & Production Practice Questions

## Question 1

Scenario: A team built a contract-review assistant. They manually tested it against ten contracts their own team knew well, declared it ready, and shipped. Two weeks later, it started failing on contracts with non-standard obligation structures — a class of input the eval suite had never seen because the golden dataset was built from those same ten contracts.

Question: What is the root architectural failure here?

A. The model tier chosen was too weak for contract review.

B. The eval dataset was not representative of the production input distribution, so a passing eval suite gave false confidence.

C. The team should have used a code-based eval instead of manual spot-checks.

D. The contracts exceeded the model's context window.

Correct answer: B

Explanation: The failure mode described is a non-representative golden dataset — built from convenient inputs the team already knew, rather than a sample that covers the input distribution production will actually see. A passing eval suite built on the wrong dataset measures a different system than the one being shipped.

Distractors:

- A: The scenario gives no evidence of a model-capability limit; it describes a data-coverage gap in the eval.
- C: The problem isn't code-based vs. manual grading, it's dataset representativeness — even a well-automated eval over the same ten contracts would have missed the same gap.
- D: No context-window limit is described; the failure is about an untested category of contract structure, not document length.

## Question 2

Scenario: A team is sizing a customer service agent expected to handle 50,000 requests/month with a 5,000-token stable system prompt, a $800/month cost ceiling, and a 3-second p95 latency target. Their initial configuration is over budget.

Question: Which single lever is most likely to close the gap with the least tradeoff, given the details in the scenario?

A. Switch to Opus for maximum output quality, since a bigger model is always the safer choice.

B. Turn on prompt caching, since the 5,000-token system prompt is stable and reused across all 50,000 requests.

C. Raise the max_tokens cap so responses have more headroom.

D. Reduce call volume by asking the business to route fewer conversations through the system.

Correct answer: B

Explanation: A long, stable system prompt reused across high volume is exactly the case prompt caching is built for — cached tokens are billed well below the standard input rate, and caching directly cuts the dominant cost driver here without touching model tier or output quality.

Distractors:

- A: Opus increases cost per token; "most capable is always safest" ignores that this is a cost/latency-constrained decision, not a quality-limited one.
- C: Raising max_tokens increases potential output cost and does not address the input-token cost driven by the repeated 5,000-token system prompt.
- D: Cutting call volume is a business decision outside the architect's cost-lever toolkit and isn't suggested by anything in the scenario — the fix belongs in the architecture, not in reducing service.

## Question 3

Scenario: An architect is asked by a partner whether Claude can power a document-review assistant. The architect confirms the model is good at reading and flagging clauses and commits to a six-week build timeline. Two weeks into the build, the partner mentions they process 800 contracts/day, some running 300 pages, with results needed in under 30 seconds.

Question: What should the architect have done differently before committing to the timeline?

A. Nothing — the capability confirmation was accurate and the timeline is unaffected by these details.

B. Gathered call volume, input size, and latency requirements before issuing any feasibility verdict or committing to a schedule.

C. Insisted the partner reduce their volume to under 100 contracts/day before starting.

D. Refused the engagement entirely, since 300-page documents are never feasible.

Correct answer: B

Explanation: A feasibility verdict is only as sound as the constraints gathered before it. Volume, input size, and latency are the inputs that determine model tier (context window needs), architecture (chunking or not), and whether sequential processing is viable — all of which should be settled before a commitment is made, not two weeks into the build.

Distractors:

- A: The capability answer alone left out constraints that materially affect model tier and architecture choice — the commitment was made before the design was actually validated.
- C: There's no requirement in the scenario to shrink the partner's real volume; the architect's job is to design for the stated volume, not negotiate it down.
- D: Whether 300-page documents fit is a function of model tier context window (some tiers handle it natively; others require chunking) — it isn't automatically disqualifying, and the scenario doesn't support an outright refusal.

## Question 4

Scenario: A regulated healthcare intake tool sends a system prompt asking Claude to "extract presenting concerns, medications, and allergies," but the user message includes the patient's name, DOB, SSN, and Insurance ID alongside the clinical narrative. A pre-production audit finds these fields captured in plaintext in the application layer's request logs.

Question: What is the correct architectural fix?

A. Switch to a more capable model that is less likely to leak sensitive fields in its output.

B. Add a disclaimer to the system prompt instructing Claude not to repeat sensitive fields back to the user.

C. Add a server-side redaction step that strips non-essential PII before the Claude call, and a retrieval function that supplies only the fields the language task needs.

D. Encrypt the request logs after the fact so the captured SSNs are no longer readable in plaintext.

Correct answer: C

Explanation: The problem is a data-architecture decision, not a model behavior problem: SSN and Insurance ID were never necessary for the summarization task and shouldn't have entered the context window at all. The fix is upstream — redact/filter before the API call and retrieve only what the task needs, applying the necessity filter to every field.

Distractors:

- A: The summarization worked correctly; the failure was data handling, not model capability, so a bigger model doesn't address it.
- B: A prompt instruction doesn't prevent the sensitive fields from being transmitted in the API request and captured by the application's own request logging — the data is already in the request regardless of what Claude does with it.
- D: Encrypting logs after the fact doesn't fix the design flaw that put PHI in the context window unnecessarily, and doesn't address the ongoing exposure on every future request.

## Question 5

Scenario: A customer support tool injects the authenticated user's role into the system prompt from the session's identity service. A competing design proposal instead asks users to state their role directly in their chat message (e.g., "As a senior manager, show me...") to simplify the integration.

Question: Why should the architect reject the second design?

A. It increases token usage compared to server-side injection.

B. A user-asserted role in their own message is unverified and can be manipulated, so authorization decisions must be driven by server-side identity, not user input.

C. It requires an additional API call to validate the role claim.

D. Claude cannot parse role claims embedded in user messages.

Correct answer: B

Explanation: Anything in the user's message is under the user's control. A self-asserted role claim can be faked by any user typing the right words, defeating the authorization model. Identity and role must be injected server-side from the authentication layer, where it can't be tampered with.

Distractors:

- A: Token overhead is a minor, secondary concern compared to the security failure — even if token cost were identical, this design would still be wrong.
- C: The issue isn't about needing an extra validation call; it's that no validation of the user's self-reported claim occurs at all in this design.
- D: Claude can parse and act on the claim just fine, which is precisely the danger — it will act on false claims because nothing verifies them.

## Question 6

Scenario: A multi-tenant SaaS company runs a customer-service agent for all its tenants behind a single shared Claude API key. A traffic spike from one tenant trips the org-level rate limit, and every tenant's requests begin failing simultaneously.

Question: What integration change would have prevented this failure mode?

A. Increase the overall rate limit ceiling for the shared key.

B. Issue a separate API key per tenant for cost attribution and rate-limit isolation.

C. Add a circuit breaker at the service boundary in front of the shared key.

D. Cache the system prompt to reduce overall request volume.

Correct answer: B

Explanation: A shared key across tenants makes it impossible to attribute a rate-limit breach to the tenant that caused it, and every tenant absorbs the impact of one tenant's spike. Per-tenant API keys are required for both cost attribution and isolation in a production multi-tenant deployment.

Distractors:

- A: A higher ceiling delays the problem without fixing the underlying attribution and isolation gap — the next larger spike from any single tenant still takes everyone down.
- C: A circuit breaker protects against a failing dependency's error rate; it doesn't solve the problem of one tenant's legitimate volume exhausting a shared limit that all tenants depend on.
- D: Caching reduces cost and latency for repeated stable prompts but does nothing to isolate one tenant's traffic spike from affecting others under a shared key.

## Question 7

Scenario: A team runs a revised system prompt against 50 customer sessions and the current prompt against another 50 sessions. The new version shows a 68% task success rate versus 62% for the old version. They declare the new version the winner and ship it. Two weeks later in full production, the new version's success rate settles at 61%.

Question: Which combination of problems best explains why the initial comparison was misleading?

A. The judge model used to score task success was miscalibrated.

B. The sample size was too small to distinguish a 6-point difference from noise, the input distribution across the two groups wasn't controlled, and the primary metric was effectively chosen after seeing which one moved favorably.

C. The team should have used a code-based eval instead of measuring task success rate at all.

D. Shadow testing would have been unnecessary if they had simply run the test for one more day.

Correct answer: B

Explanation: All three problems compound: 50-session groups are far too small to reliably detect a 6-point difference on a high-variance metric; if the 50 sessions per group weren't randomly and evenly assigned, the difference could be an artifact of which inputs landed where; and since the team appears to have anchored on task success rate because it happened to move favorably, that's outcome-shopping rather than a pre-specified metric.

Distractors:

- A: The scenario describes a sampling and experimental-design failure, not a judge-calibration issue — no judge model or rubric is mentioned as the scoring mechanism.
- C: Task success rate can be a legitimate metric regardless of grading method; the failure is in experimental design (sample size, randomization, metric pre-specification), not in choosing the wrong eval type.
- D: Running longer with the same lack of randomization and pre-specified metric wouldn't fix the underlying design flaws — the fix is proper sample-size calculation and controlled assignment, not simply more elapsed time.

## Question 8

Scenario: An architect is deciding between a live A/B test and shadow testing for a proposed prompt-architecture change to a medical intake summarizer, where a wrong output could delay patient treatment.

Question: Which testing approach is most appropriate, and why?

A. A live A/B test, because it captures real downstream user-acceptance signal that shadow testing cannot.

B. Shadow testing, because a single bad output in this domain carries too much risk, and exposing patients to an unvalidated change may not be permissible at all in a regulated deployment.

C. A 50-session manual comparison, because the sample is small enough to review by hand for safety.

D. Neither — this change should skip experimentation and go straight to full production deployment.

Correct answer: B

Explanation: Shadow testing runs the new version against a copy of live traffic and scores it offline while every real user still gets the current version's response — no patient is ever exposed to the unvalidated change. For a regulated, high-stakes domain where a single bad output is unacceptable, this is often the only acceptable way to validate the change before deployment.

Distractors:

- A: Live A/B testing does provide downstream signal, but it does so by exposing some real patients to the new, unvalidated version — an unacceptable risk given the stated stakes.
- C: A small manual comparison doesn't solve the exposure-risk problem, and per the module's own case study, small-sample comparisons are prone to noise regardless of who reviews them.
- D: Skipping experimentation entirely removes any validation gate before a high-stakes deployment, which is the opposite of the module's guidance to test before shipping changes.

## Question 9

Scenario: A team's dashboard shows average cost per request comfortably within budget and an acceptable average error rate. A later investigation reveals that 3% of requests — long, unusual documents — are consuming 60% of the monthly token spend and producing most of the incorrect outputs.

Question: What observability practice would have surfaced this problem earlier?

A. Increasing the frequency of the aggregate dashboard refresh from daily to hourly.

B. Per-request decomposition of cost and error metrics, rather than relying on aggregate averages alone.

C. Switching the primary metric from cost per request to latency p50.

D. Adding a circuit breaker to the request pipeline.

Correct answer: B

Explanation: Aggregate metrics can look healthy while a small fraction of requests consumes most of the budget and drives most of the failures. Per-request decomposition protects against exactly this non-obvious failure mode, which aggregate-only dashboards structurally cannot detect.

Distractors:

- A: A faster refresh rate on the same aggregate metric still hides the same underlying skew — the problem is the level of aggregation, not the polling frequency.
- C: Switching to p50 latency doesn't address cost or error-rate visibility at all, and median latency specifically hides tail behavior, which is the opposite of what's needed here.
- D: A circuit breaker protects against a failing downstream dependency; it does nothing to reveal which fraction of requests is driving cost and error concentration.

## Question 10

Scenario: A metric on a production dashboard shows a sudden shift in output quality. The on-call architect needs to decide whether the fix is a prompt change, a retrieval/grounding change, a model-selection change, or a multi-agent trace investigation.

Question: Which step should happen before any of those fixes are applied?

A. Immediately roll back to the previous prompt version, since that is always the safest first response.

B. Classify the failure into a specific category (prompt failure, hallucination, model mismatch, or orchestrator-workers failure), since each has a different root cause and fix.

C. Increase the max_tokens cap, since most quality regressions are caused by truncated output.

D. Re-run the eval suite unchanged and wait to see if the score naturally recovers.

Correct answer: B

Explanation: Diagnosis must precede treatment. The four failure classes are distinct and require different fixes — a prompt failure is fixed in the prompt, a hallucination needs grounding (not a stronger instruction), a model mismatch needs a re-evaluated model swap, and an orchestrator-workers failure needs a trace spanning both the orchestrator and its subagents. Applying the wrong fix for the actual failure type wastes effort and can mask the real problem.

Distractors:

- A: Rolling back may be reasonable once the cause is known, but jumping straight to rollback without classifying the failure risks reverting a change that wasn't the actual cause, or missing a hallucination that needs grounding regardless of prompt version.
- C: Truncation is only one narrow possible cause; assuming it without diagnosis skips the classification step and may not address the actual failure type at all.
- D: Passively waiting doesn't diagnose anything and risks letting a real regression continue to affect users while doing nothing to identify or fix the root cause.
