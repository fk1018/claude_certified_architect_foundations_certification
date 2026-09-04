# MSO Foundations Practice Questions

## Question 1

Scenario: A QA engineer writes an automated test that calls a Claude-powered summarization feature and asserts that the response exactly matches a hardcoded string captured from a previous run. The test now fails intermittently even though manual review shows every failing response is a correct summary.

Question: What is the most accurate diagnosis and fix?

A. The API is broken and retries should be added around every call.

B. Sampling makes wording non-deterministic even for correct answers; the test should assert on properties (required content, structure, or a model-graded eval) instead of exact text.

C. The test should switch to a lower-tier model, since only weaker models produce inconsistent wording.

D. The test should set temperature to a negative value to force deterministic output.

Correct answer: B

Explanation: Non-determinism is a direct consequence of sampling — identical inputs do not guarantee identical outputs, so exact-text assertions are inherently unreliable. The correct pattern is to assert on the property that must hold, or use a model-graded eval when judging meaning.

Distractors:
- A: Nothing indicates the API is malfunctioning; varying wording on correct answers is expected sampling behavior, not an error condition.
- C: Model tier does not eliminate sampling-driven wording variation; smaller and larger models both sample.
- D: Temperature values are non-negative, and even temperature 0 does not guarantee identical output across calls.

## Question 2

Scenario: A developer wants to reduce how much a hard, multi-step financial-reconciliation task costs per call while keeping quality high, and separately wants to reduce cost on a simple spam-classification call.

Question: Which combination of settings best fits the module's guidance?

A. Disable reasoning on both tasks to save tokens uniformly.

B. Enable reasoning (higher effort) on the reconciliation task since it's hard and multi-step; leave reasoning off on the spam classification, since reasoning is wasted on lookups and classification.

C. Switch both tasks to Fable, since the most capable tier always reduces total cost.

D. Enable reasoning on the spam classification to guarantee a more confident label, and disable it on reconciliation to save tokens.

Correct answer: B

Explanation: The module states reasoning earns its cost on hard, multi-step problems and is wasted on lookups and classification. Model choice and reasoning mode are independent levers, so effort should be spent where the task actually benefits.

Distractors:
- A: Disabling reasoning on the hard reconciliation task would remove value where it's actually earned.
- C: Fable is the most capable tier, not necessarily the cheapest; tier should be chosen based on eval-shown need, not applied uniformly to cut cost.
- D: This reverses the guidance — reasoning is wasted on classification and valuable on the hard multi-step task.

## Question 3

Scenario: A pipeline needs to process 50,000 scanned invoices overnight. No user is watching, and the team's priority is minimizing total cost, not turnaround time.

Question: Which request pattern best fits, and why?

A. A synchronous loop calling the API once per invoice, since it's the simplest pattern to implement.

B. Streaming, since it lets the pipeline start processing each invoice's output sooner.

C. The Message Batches API: submit the requests in a batch and poll for completion, accepting up to 24 hours of latency for a lower per-token cost.

D. A single request with the largest possible context window, packing all 50,000 invoices into one call.

Correct answer: C

Explanation: The Batches API is explicitly designed for bulk offline workloads where no user is waiting and cost matters more than turnaround time, offering a lower per-token cost in exchange for latency of up to 24 hours.

Distractors:
- A: A synchronous loop at this volume would hit rate limits and tie up the application unnecessarily.
- B: Streaming reduces perceived latency for a watching user; it provides no benefit to an unattended overnight bulk job.
- D: The context window is a fixed per-request budget; packing 50,000 documents into one request would likely exceed it and is not how bulk volume is handled.

## Question 4

Scenario: A long-running multi-turn agent session that worked fine in testing (short inputs, few turns) starts failing in production once real users have long conversations with many tool calls.

Question: What is the most accurate explanation of what's happening and who is responsible for fixing it?

A. The context window automatically expands to accommodate longer sessions, so this must be an unrelated bug.

B. The context window is a fixed token budget; as history and tool results accumulate it fills, and the application — not the API — is responsible for trimming or summarizing history before each call to prevent input from becoming oversized or generation from hitting the ceiling.

C. This only happens because temperature was left at a high value; lowering it will fix the growing-context issue.

D. This is expected and requires no application-side handling, since the model always silently drops the oldest turns to make room.

Correct answer: B

Explanation: The context window holds the system prompt, full conversation, injected documents, tool results, and output as one fixed token budget. Development environments rarely hit this because test inputs are short; production sessions with longer history fill the window faster. Managing this — trimming or summarizing — is explicitly the application's job.

Distractors:
- A: The window is fixed, not auto-expanding; assuming otherwise is exactly the trap the module calls out.
- C: Temperature affects sampling variability, not the size of the context-window budget.
- D: The model does not silently drop old turns; an oversized input is rejected before generation, and a mid-generation ceiling hit returns truncated output with a specific stop reason — neither is "no application-side handling needed."

## Question 5

Scenario: A team is evaluating whether to upgrade a feature currently running on Sonnet to Opus, believing the upgrade will "obviously" improve quality.

Question: According to the module's guidance on model tier selection, what should drive this decision?

A. Upgrade immediately, since a higher tier is always strictly better regardless of task.

B. Move up a tier only when an eval shows the current tier is missing the quality bar for the specific task; Sonnet remains the practical default until evidence says otherwise.

C. Never upgrade past Sonnet, since it is described as the "balanced default" for all production workloads.

D. Base the decision solely on latency requirements, ignoring quality entirely.

Correct answer: B

Explanation: The module's stated discipline is to start with Sonnet and move up a tier only when an eval shows the current tier is missing the quality bar — and, symmetrically, move down to Haiku only when an eval shows the quality drop is acceptable. Tier changes should be evidence-driven, not assumption-driven.

Distractors:
- A: Higher tiers cost more and are not automatically the right choice; the guidance is explicitly to upgrade only when evidence (an eval) supports it.
- C: Sonnet is the default starting point, not a hard ceiling; Opus and Fable exist precisely for tasks that exceed Sonnet's envelope.
- D: Latency is one factor among cost, latency, and capability tradeoffs, but the module's specific guidance for tier changes centers on eval-demonstrated quality gaps, not latency alone.

## Question 6

Scenario: A developer keeps getting output in the wrong casing and structure from a zero-shot prompt despite rewriting the instructions several times with more detail.

Question: What does the module suggest trying next, and what is the cost implication?

A. Add one or two correct input-output examples (moving to one-shot or multi-shot) to show the model the exact structure; this typically fixes structure problems faster than more instruction text, but adds token cost on every future call.

B. Switch to a smaller model tier, since structure problems are always caused by using too capable a model.

C. Raise the temperature to encourage the model to explore more output formats until it finds the right one.

D. Retrain the model on the desired structure by sending the examples once in an initial call.

Correct answer: A

Explanation: The module states that adding two or three correct examples usually fixes a structure problem that more instruction text did not, at the cost of extra tokens on every call — so the discipline is to add the fewest examples that make output reliable.

Distractors:
- B: Model tier is unrelated to prompt structure problems; a smaller model is not more likely to fix formatting.
- C: Raising temperature increases output variability, which would make an already-inconsistent structure problem worse, not better.
- D: Examples are not training data; they must be included in every relevant prompt going forward, not sent once.

## Question 7

Scenario: A developer says, "Since we enabled extended thinking on this model, it's now a different, more powerful model than before."

Question: What is the best correction based on the module?

A. This is correct — enabling thinking effectively swaps in a different underlying model.

B. This is incorrect — model choice (which family member runs) and reasoning mode (thinking on/off, effort level) are separate, composable settings; the same model can run with reasoning on or off per call.

C. This is correct only for Haiku, since Haiku cannot reason without switching models.

D. This is incorrect because reasoning mode is a fixed, account-level setting that cannot be changed per call.

Correct answer: B

Explanation: The module is explicit that choosing which model to run is one decision, and whether the model reasons is a separate, per-call decision. The two levers compose independently rather than one implying the other.

Distractors:
- A: This conflates two independent settings; enabling thinking does not change which model is running.
- C: There's no basis in the module for a Haiku-specific exception; reasoning mode is described as a general per-call setting.
- D: Reasoning mode is described as configured per request/call, not fixed at the account level.

## Question 8

Scenario: A developer is deciding whether to call the Claude REST API directly with a custom HTTP client or use the official SDK for a new Python service.

Question: What does the module say about the relationship between the SDK and raw REST access?

A. The SDK reaches a separate, faster API endpoint than raw REST calls.

B. The SDK and raw REST reach the same API and the same model; the SDK is a thin convenience layer handling auth, request construction, retries, and response parsing, reducing boilerplate.

C. Raw REST access is deprecated and no longer functions for current Claude models.

D. The SDK is required because raw REST calls cannot include tool definitions or conversation history.

Correct answer: B

Explanation: The module states plainly that the SDK is a thin convenience layer over the same REST API — same endpoint, same model — that just saves the developer from assembling requests, handling retries, and parsing responses by hand.

Distractors:
- A: There is no separate faster endpoint; both paths reach the same API.
- C: Raw REST remains fully callable with any HTTP client; the module explicitly describes constructing a request directly against the endpoint.
- D: Nothing in the module suggests raw REST is functionally limited in what it can send; the SDK's value is reduced boilerplate, not unlocking otherwise-unavailable capabilities.

## Question 9

Scenario: A developer needs a Claude-powered chat UI where users watch replies appear progressively rather than waiting for the full answer, and separately needs a backend job that fires off many concurrent Claude calls without blocking the main application thread.

Question: Which two patterns correctly address these two needs, respectively?

A. Streaming (SSE) for the watched chat UI; async/await (e.g., AsyncAnthropic in Python) for the concurrent, non-blocking backend calls.

B. Message Batches API for the chat UI; synchronous calls for the backend job.

C. Synchronous calls for the chat UI; streaming for the backend job.

D. Async/await for the chat UI; Message Batches API for the backend job.

Correct answer: A

Explanation: Streaming is specifically for cases where a response is long or a user is watching, sending pieces over SSE so output appears immediately. Async/await patterns (AsyncAnthropic in Python, the Promise-based TypeScript client) let an application issue calls without tying up its thread while still getting real-time responses — exactly the concurrent-backend-job need described.

Distractors:
- B: Batches is for bulk offline workloads with no one waiting and can take up to 24 hours — wrong fit for a live chat UI; synchronous calls in a loop would block the backend job's thread.
- C: Synchronous calls make a watching user wait for the full response with no incremental output, defeating the purpose; streaming isn't the concurrency mechanism the backend job needs.
- D: Async/await doesn't stream partial output to a watching user; Batches is for offline bulk work, not a job that needs real-time concurrent calls.
