# Production Engineering, Evals, and Security Practice Questions

## Question 1

Scenario: A team ships a customer-message field-extraction feature after watching it correctly handle about a dozen manually chosen example messages. Two weeks after launch, a message containing two dates in one sentence causes the feature to extract the wrong date. Every existing validation check (non-empty text, populated date field, well-formed date) still passes on that message.

Question: What was the actual root cause of this failure, and what should the team have done differently before launch?

A. The model was too small for the task; upgrading to a more capable tier would have prevented the failure.

B. There was no graded eval case covering a message with two dates, so the expected behavior for that input shape was never defined or checked.

C. The validation checks were too strict and rejected valid extractions.

D. The feature needed a retry loop, since the wrong extraction was a transient failure that a second attempt would have corrected.

Correct answer: B

Explanation: Validation confirmed the extracted value was well-formed and populated, but not that it was the *right* value. The dozen manual tries all used single-date messages, so no graded case ever exercised the two-date scenario. The fix is defining expected behavior for edge cases as checkable eval cases before shipping, not upgrading the model, loosening validation, or adding a retry.

Distractors:

- A: The postmortem found no bug in the model or prompt capability; the missing piece was a graded eval case, not model capacity.
- C: The validation checks worked exactly as designed — they just couldn't verify semantic correctness, only shape.
- D: This is a deterministic extraction error given the input, not a transient condition — retrying the identical request would produce the identical wrong extraction every time.

## Question 2

Scenario: An engineer is deciding how to grade three different features: (1) a classifier that must return exactly one of five fixed labels, (2) a function that must return valid, well-formed JSON matching a schema, and (3) a one-paragraph rationale explaining a recommendation.

Question: Which grading method should be used for each, respectively?

A. LLM-as-judge for all three, since it is the most thorough method available.

B. Exact/string match for the classifier, a code-graded check for the JSON output, and an LLM-as-judge for the rationale.

C. A code-graded check for all three, since code checks are cheapest and scale to any output type.

D. Exact/string match for the JSON output, a code-graded check for the classifier, and exact match for the rationale.

Correct answer: B

Explanation: The grading method follows the shape of the output: a single correct label fits exact/string match (cheap, zero ambiguity); structured output fits a code-graded check (validates shape, like a JSON parse); open-ended quality with no single correct phrasing requires an LLM-as-judge, since no code rule or string match can assess whether a rationale is good.

Distractors:

- A: Using a judge for the classifier and the JSON check is unnecessarily expensive and noisy when a cheap, deterministic check would work just as well.
- C: A code check can confirm the rationale is a non-empty string, but that is nearly worthless as a quality signal — it can't judge faithfulness or completeness.
- D: This mismatches methods to outputs — a JSON structure needs a parse check, not a literal string match (any valid reordering would falsely fail), and a rationale can't be checked with exact match at all.

## Question 3

Scenario: A team calibrates a new LLM-as-judge by comparing its scores against a small set of human-labeled cases, and finds the judge agrees with the human labels on only 45% of cases, despite always returning a confident-looking numeric score.

Question: What should the team do next?

A. Trust the judge's scores anyway, since a numeric score is inherently more objective than a human's subjective judgment.

B. Discard LLM-as-judge entirely and switch to exact/string match for this open-ended task.

C. Tighten the rubric — clarify what each score band means, add examples of good and bad answers — then re-measure agreement before relying on the scores.

D. Increase the judge's max_tokens parameter so it can write a longer response.

Correct answer: C

Explanation: Low agreement with human labels means the judge is not yet calibrated and its scores are not defensible. The fix is to tighten the rubric (clarify score bands, add worked examples) and re-measure agreement, repeating until the judge is trustworthy — not to trust an uncalibrated score or abandon judging in favor of a method that doesn't fit open-ended output.

Distractors:

- A: A confident-looking number from an uncalibrated judge provides no value — the whole point of calibration is verifying the score reflects actual quality.
- B: Exact/string match is the wrong tool for open-ended output; no two good answers are phrased identically, so it would fail nearly every case.
- D: Response length is unrelated to score calibration; the issue is what the rubric asks for and how well-anchored the scoring is, not verbosity.

## Question 4

Scenario: A retrieval-augmented feature has a `retrieve()` function with a passing unit test and a `model.call()` function with a passing functional test. The full end-to-end test fails, and a trace shows `retrieve()` returns a list of dictionaries while `build_prompt()` was written expecting a plain string, so the model receives malformed context and answers from memory instead.

Question: What is the correct diagnosis and fix?

A. The parser is broken; rewrite `parse_date` even though its unit test already passes.

B. The prompt wording is unclear; add "answer carefully and cite the policy" to the system prompt.

C. The handoff contract between `retrieve()` and `build_prompt()` was never defined or tested; align the data shapes and add an integration test that drives both components together with real data.

D. The model needs to be upgraded to a more capable tier to better infer the intended context format.

Correct answer: C

Explanation: Each component passes in isolation, which is exactly the signature of an integration-seam failure — the handoff between two individually correct components was never exercised together. The fix is aligning the data contract (e.g., extracting `.content` before joining) and adding an integration test, which is the only test level that would have caught this.

Distractors:

- A: The parser already has a passing unit test and isn't implicated by the trace — the failure is upstream, at the retrieval-to-prompt handoff.
- B: Rewording the prompt doesn't fix a structural data-shape mismatch; the model is receiving malformed context regardless of instructions.
- D: A more capable model still can't correctly interpret context that was passed in the wrong data shape; this is a data contract bug, not a capability gap.

## Question 5

Scenario: A production feature makes calls to the Claude API in a loop with no error handling, because it never failed during development testing. At the first real traffic peak, a 429 rate-limit response is raised as an unhandled exception and the whole request fails. The developer's first fix attempt adds an immediate retry in a tight loop, which makes the problem worse.

Question: Why did the immediate tight-loop retry make things worse, and what is the correct fix?

A. Retries should never be used for a 429; the correct fix is to fail immediately and show the user an error.

B. Each instant retry counts as another request against the same rate limit, deepening it; the correct fix is exponential backoff with a capped number of attempts, honoring the `retry-after` header when present.

C. The bug is that the loop uses `for` instead of `while`; switching loop types resolves rate-limit errors.

D. The correct fix is to switch to a smaller, cheaper model, which is not subject to rate limits.

Correct answer: B

Explanation: A 429 is retriable — the correct handling is to wait before retrying, using exponential backoff capped at a maximum attempt count, and reading `retry-after` when the response provides it. An immediate, uncapped retry loop sends more requests into the same limit window, deepening rather than relieving the rate limit.

Distractors:

- A: A 429 is explicitly retriable in the module's classification — failing immediately without ever retrying wastes a recoverable request unnecessarily.
- C: The loop construct (`for` vs `while`) is irrelevant; the defect is the absence of backoff and status-based classification, not the iteration syntax.
- D: Model tier has nothing to do with rate limits, which are governed by request volume and account/API limits, not which model is called.

## Question 6

Scenario: A tool call inside an agent's flow fails due to a downstream service timeout. The developer's code catches the exception and returns an empty string as the tool result so the agent loop can continue without crashing.

Question: What is wrong with this approach, and what should happen instead?

A. Nothing is wrong; returning an empty string lets the loop continue safely, which is the primary goal.

B. The empty result is read by the model as valid data, so it will continue reasoning as if the tool succeeded with no results, producing a confident but wrong downstream answer; the tool result should instead be returned with `is_error: true` and a description of the failure.

C. The bug is that exceptions should never be caught in a tool wrapper; let them propagate and crash the request instead.

D. The fix is to retry the tool call in an infinite loop until it succeeds, since all tool failures are retriable.

Correct answer: B

Explanation: An empty string looks like a valid (if unhelpful) result to the model, which will reason on top of it as though it were real data. Setting `is_error: true` lets the model know the call actually failed, so it can try a different approach, ask for clarification, or stop — rather than confidently building an answer on missing data.

Distractors:

- A: Continuing the loop is fine in principle, but an empty result that looks like valid data is exactly the failure mode the module warns against — the model can't tell "empty result" from "successfully found nothing."
- C: Catching the exception is correct; the defect is what gets returned afterward (silent empty content instead of a flagged error), not the act of catching it.
- D: Not all tool failures are retriable, and an infinite retry loop with no cap or backoff risks the same rate-limit-deepening problem seen with model calls; some tool failures are terminal and should surface immediately.

## Question 7

Scenario: A team is deciding which Claude model tier to use for three workloads: (1) a high-volume classification step labeling millions of short messages daily, where an eval shows the cheapest tier already holds the quality bar; (2) a multi-step agent planning a dependent refactor, where an eval shows the balanced default tier missing the bar on the hardest cases and a wrong early step is expensive; (3) mixed traffic where most requests are simple lookups and a few are complex synthesis tasks.

Question: What is the correct tier decision for each workload?

A. Use the most capable tier for all three, since capability never hurts and simplifies the architecture.

B. Use the cheapest tier for (1) since the eval confirms it holds the bar; step up to a more capable tier for (2) since the eval shows the default missing the bar on costly failures; and route (3) with a balanced default plus an override to the more capable tier only for complex requests.

C. Use the balanced default tier for all three workloads, since it is designed to handle mixed and varied traffic without further tuning.

D. Use the cheapest tier for all three to minimize cost, since eval scores are only a secondary consideration behind cost.

Correct answer: B

Explanation: Model tier decisions should be made on eval evidence: the cheap tier is justified for (1) because the eval confirms it holds the bar at high volume; the more capable tier is justified for (2) because the eval shows the default missing the bar where a wrong answer is costly; and for mixed traffic like (3), routing (a default plus an override on a cheap signal) avoids paying the most-capable-tier cost on every request while still covering the complex subset.

Distractors:

- A: Defaulting to the most capable tier everywhere is explicitly named as the most common and expensive model-selection mistake in production — it ignores what the eval evidence actually shows.
- C: A single balanced tier for all three ignores the eval evidence in both directions — it overspends on workload (1) and underdelivers on workload (2).
- D: Cost should be optimized only above a reliability/quality floor established by eval evidence — using the cheapest tier for workload (2), where an eval already shows it missing the bar on costly failures, trades a wrong answer's real cost for a lower bill.

## Question 8

Scenario: A developer moves a coding task — where each step depends on completing the previous step — into an orchestrator-worker setup with a lead agent and five parallel subagents, expecting faster completion. The wall-clock time barely improves, the bill roughly triples, and answer quality is unchanged.

Question: What is the best explanation and correction?

A. The task doesn't decompose into independent parallel parts, so the subagents are mostly waiting on each other; fan-out pays the roughly 15x token multiplier without buying any parallel benefit, and a single agent with good context should be used instead.

B. Five subagents is too many; reducing to two subagents would fix the cost problem while preserving the speed benefit.

C. Orchestrator-worker setups are never appropriate for engineering work of any kind and should be replaced with a single agent universally.

D. The bill increase is unrelated to the orchestration pattern and is more likely explained by a pricing change on the API.

Correct answer: A

Explanation: The orchestrator-worker pattern earns its cost multiplier only when a task genuinely splits into independent parts that can be explored in parallel, like research across separate sources. A tightly coupled task like this refactor, where each step depends on the last, gets no parallel benefit — the subagents wait on each other — while still paying roughly the reported 15x token multiplier for the fan-out.

Distractors:

- B: The problem isn't the subagent count; it's that the task doesn't decompose into independent parallel work at all, so any number of subagents pays a needless multiplier.
- C: The module explicitly says the pattern genuinely helps for tasks that split into independent parts (e.g., multi-source research) — the issue here is a task-fit mismatch, not a blanket prohibition on the pattern.
- D: The scenario explicitly ties the cost increase to the fan-out (each subagent spending its own tokens in its own context), which is the documented mechanism behind the reported ~15x multiplier — this is not a pricing coincidence.

## Question 9

Scenario: An agent fetches web pages on behalf of internal, trusted employees and can write to a single file path. The developers reasoned that because the users are trusted, they didn't need to validate the pages the agent fetches. The agent later writes an unexpected file after summarizing a page that, near the bottom, contained hidden text instructing it to write its summary to a different path.

Question: What is the correct diagnosis, and what two-part fix addresses it?

A. The users were not actually trustworthy; the fix is to add stricter authentication for the employees using the agent.

B. The hostile instruction arrived through the fetched page's content, not through the trusted user's request, so trusting the user did nothing to prevent it; the fix is to treat fetched content as data rather than instructions, and add a hook that denies writes outside the permitted path.

C. The agent's model was outdated; upgrading to a newer model version would have caused it to recognize and ignore the injected instruction on its own.

D. The fix is to stop the agent from fetching any web content at all, since any content fetching is inherently unsafe.

Correct answer: B

Explanation: This is a textbook prompt injection: the hostile instruction was embedded in content the agent fetched, not in the trusted user's own prompt, so "our users are trusted" is irrelevant to the threat. The two-sided defense is (1) treating fetched content as data to be examined rather than followed as instructions, and (2) enforcing the actual action boundary with a `PreToolUse`-style hook that denies writes outside the permitted path, regardless of what the content said.

Distractors:

- A: The employees themselves did nothing wrong and were never the source of the malicious instruction — stricter user authentication does not address content-borne injection at all.
- C: Model training and classifiers reduce how often an injection lands but are explicitly described as probabilistic, not guaranteed — relying on a model upgrade alone leaves the action boundary undefended.
- D: The module's guidance is to defend the boundary (treat content as data, enforce via hooks), not to eliminate the capability entirely — a total fetch ban is a much larger functional loss than necessary.

## Question 10

Scenario: A team is scoping a Claude-based integration for a healthcare customer ahead of a security review. They have not yet documented where data is processed, how access is logged, or whether an administrator can control configuration centrally, and they have not confirmed which of their candidate models carry Zero Data Retention (ZDR) eligibility.

Question: What should the team do before the review, and why?

A. Nothing extra is needed beyond passing functional tests; regulated customers only evaluate feature correctness, not deployment or data-handling details.

B. Name data residency, access logging (mapped to the hook's audit trail), and managed configuration during scoping, and confirm each candidate model's current ZDR eligibility against the Anthropic Trust Center, since ZDR eligibility varies by model and platform and is not guaranteed even under an existing agreement.

C. Assume ZDR applies uniformly to all Claude models once any ZDR agreement is signed with Anthropic, and focus scoping effort exclusively on functional correctness.

D. Defer all data-handling and residency questions until after the review begins, since they are typically raised only if the reviewer specifically asks.

Correct answer: B

Explanation: A regulated customer reliably asks about data residency, access logging, and managed configuration early — naming these during scoping (with the hook's audit log answering the logging question) keeps the review from stalling. ZDR eligibility is explicitly called out as model- and platform-specific and not guaranteed under a broader agreement, especially for newer or higher-capability models, so it must be confirmed per model at scoping time.

Distractors:

- A: The module explicitly frames these three questions as what a regulated customer asks early, independent of whether the feature itself works correctly — treating them as out of scope invites the review to stall.
- C: The module explicitly warns that ZDR eligibility is not guaranteed for every model even under an existing ZDR agreement, and must be confirmed individually — assuming blanket coverage is precisely the mistake being warned against.
- D: Waiting for the reviewer to raise these questions unprompted, rather than naming them proactively during scoping, is described as what turns a review into a blocker rather than a checklist.
