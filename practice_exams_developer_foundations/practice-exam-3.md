# CCDVF Practice Exam 3

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Order-Fulfillment Automation Agent for an E-Commerce Retailer, Multi-Vendor (Bedrock/Vertex) API Integration for a SaaS Platform, Model Tiering for a High-Volume Ticket-Triage Service, Claude Code and MCP for a Mobile App Team's CI Pipeline) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (approximate, matches the official blueprint weightings):

| Domain | Questions |
|---|---|
| D1: Agents and Workflows (14.7%) | 9 |
| D2: Applications and Integration (33.1%) | 16 |
| D3: Claude Code (3.1%) | 3 |
| D4: Eval, Testing, and Debugging (2.6%) | 3 |
| D5: Model Selection and Optimization (16.8%) | 12 |
| D6: Prompt and Context Engineering (11.0%) | 7 |
| D7: Security and Safety (8.1%) | 5 |
| D8: Tools and MCPs (10.6%) | 5 |

Answer key with explanations is at the end of this file. Answer every question before checking — the real exam does not allow skipping.

---

## Scenario A: Order-Fulfillment Automation Agent for an E-Commerce Retailer (Questions 1–15)

You are building an internal agent for a mid-size e-commerce retailer using the Claude Agent SDK. It handles order-fulfillment exceptions — backorders, address problems, damaged-item claims, and refund requests — using custom tools (`check_inventory`, `create_shipping_label`, `issue_refund`, `notify_customer`). Refunds and label creation carry real financial and operational cost, so tool access and enforcement matter as much as reasoning quality.

---

**Question 1.** The fulfillment agent calls `create_shipping_label` and `issue_refund` tools within a single turn. What should the orchestration code key off to know whether to keep executing tool calls and feeding results back, versus finishing the turn?

- A) Watch the assistant's text for closing phrases such as "order resolved" or "all set," and end the loop as soon as one of those phrases appears.
- B) Cap the loop at a fixed 5 tool calls per order, ending it once that count is reached regardless of what `stop_reason` the response actually carries.
- C) Treat any tool call that returns without an error as confirmation the turn is finished, ending the loop the first time a call succeeds cleanly.
- D) Key off the response's `stop_reason`: keep looping while it reads `tool_use`, and stop once it reads `end_turn`.

**Question 2.** After the agent calls `check_inventory` and your backend executes it, what must the integration code do so the agent can correctly continue reasoning about the order?

- A) Append a `tool_result` block referencing the matching `tool_use` ID, then resend the full conversation to the model.
- B) Store the inventory count in the order database and let the agent infer that the check already happened from later context.
- C) Insert the inventory count into the system prompt so it persists as background instructions for the rest of the session.
- D) End the current turn and open a new conversation whose system prompt summarizes the inventory count for the agent.

**Question 3.** Policy requires manager approval before `issue_refund` is called for any order over $500. The system prompt states this clearly, but audit logs show the agent occasionally issues large refunds without a recorded approval. What is the most reliable fix?

- A) Restate the $500 approval threshold at both the top and the bottom of the system prompt so the rule is harder to miss.
- B) Add several few-shot examples showing the agent correctly escalating refunds over $500 for manager sign-off first.
- C) Add a hook that intercepts `issue_refund` calls and blocks any call over $500 lacking a recorded approval.
- D) Reduce the model's temperature so it follows the stated $500 approval policy more consistently across refund requests.

**Question 4.** The team wants the agent to always call `check_inventory` first on every new order, with no exceptions, before any other tool executes. What is the most reliable implementation?

- A) Set `tool_choice` to force `check_inventory` specifically on the first request, then use normal tool choice afterward.
- B) Add several few-shot examples showing `check_inventory` being called first on past orders, before any other tool runs.
- C) State in the system prompt that `check_inventory` must always run first, before any other tool call.
- D) Set `tool_choice: "any"` on the first request so some tool call is guaranteed to happen immediately, without pinning down which specific tool that call has to be.

**Question 5.** The agent currently has 14 tools, including several rarely used ones (loyalty-point adjustments, gift-wrap scheduling, marketing opt-in toggles) unrelated to fulfillment exceptions. Tool selection has become unreliable, with the agent sometimes picking irrelevant tools.

- A) Remove or scope out the tools unrelated to fulfillment, or delegate them to a separate agent.
- B) Keep all fourteen tools available but add a system-prompt note listing which ones count as "primary" for fulfillment work.
- C) Increase `max_tokens` so the agent has more room to reason through which of the fourteen tools is the right one to call.
- D) Add few-shot examples covering every combination of tools the agent might need across all fulfillment scenarios.

**Question 6.** `create_shipping_label` currently returns the string `"Error"` for every failure — invalid address, carrier API timeout, or weight-limit exceeded. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every `create_shipping_label` call in an automatic blind retry that re-issues the request a fixed number of times.
- B) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- C) Add a hook that logs each failure by category, without changing what `create_shipping_label` actually returns to the agent.
- D) Increase the carrier API's timeout so address, weight-limit, and connectivity failures all become somewhat rarer.

**Question 7.** When `check_inventory` finds a SKU with zero matching warehouse records (a valid "not stocked" outcome), it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same lookup. What should change?

- A) Return a successful response with a "not stocked" result, reserving actual errors for genuine lookup failures.
- B) Add a hook that silently suppresses the "not stocked" error and ends the conversation without telling the agent.
- C) Have the agent call `notify_customer` first on every lookup to double-check whether the SKU should exist at all.
- D) Add a system-prompt note explaining that this particular error usually just means the SKU isn't currently stocked.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `check_inventory`, then `create_shipping_label`, then `notify_customer`, arguing this makes behavior predictable. Why is model-driven tool selection the better fit for order exceptions?

- A) Model-driven selection is always cheaper, since letting the model choose skips reasoning tokens a fixed script would spend.
- B) Exceptions are high-ambiguity; the right tools and order vary case by case and depend on intermediate results.
- C) The Claude Agent SDK is technically incapable of running a fixed, hard-coded sequence of tool calls like this one.
- D) A fixed sequence of tool calls cannot invoke custom tools such as `check_inventory`, only Anthropic's built-in ones.

**Question 9.** The team wants to add `issue_refund` but is deciding whether to give the main fulfillment agent that tool directly or delegate refund decisions to a separate, narrowly-scoped subagent. Refunds have real financial cost and should only trigger under specific eligibility criteria.

- A) A narrowly-scoped subagent can be given only the refund tool and explicit eligibility criteria, limiting unnecessary refunds.
- B) Subagents are required by the SDK any time a tool call has a real financial effect, such as issuing a refund.
- C) The main agent's context window is too small to hold the `issue_refund` tool's schema alongside its other tools.
- D) Subagents execute their tool calls faster than the same tool called directly, since subagents provide a more structured execution path.

**Question 10.** During a complex multi-item order dispute, the agent's context fills with verbose raw warehouse and carrier API responses, leaving little room for reasoning about the actual resolution.

- A) Increase `max_tokens` so the agent's responses can run longer without running out of room mid-explanation.
- B) Read only the first 50 lines of every warehouse and carrier API response before passing them to the agent.
- C) Disable carrier lookups entirely and rely on `check_inventory` alone for the rest of the dispute resolution.
- D) Delegate the raw-data exploration to a subagent that returns a distilled summary of the relevant findings.

**Question 11.** The agent successfully resolves a straightforward backorder but escalates a complex, multi-carrier shipping dispute to a human. The human has no visibility into what the agent tried — logs show 15 minutes of tool calls with no accessible summary.

- A) Provide a structured handoff summary: what was tried, what was found, and a recommended next action for the human.
- B) Provide the full raw transcript of every tool call and result from the fifteen minutes of investigation.
- C) Provide just the final error message, on the assumption the human can re-investigate everything from there.
- D) Provide a sentiment analysis of how frustrated the customer's original message seemed, without including any of the tool call history.

**Question 12.** The team is deciding between letting the agent run via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own warehouse-adjacent infrastructure.

- A) Managed, Anthropic-hosted agents cannot reach private, warehouse-adjacent infrastructure under any configuration.
- B) It's operational control versus operational burden — tool-calling capability doesn't actually differ between the two.
- C) Self-hosted agents running on the team's own harness cannot be given access to custom fulfillment tools at all.
- D) Managed agents are always less secure than self-hosted ones, regardless of how either deployment option is actually configured in practice.

**Question 13.** An engineer asks whether order-exception handling should be built as a fixed workflow or an agent.

- A) Whether the task involves calling more than three distinct tools over the course of resolving a single order dispute.
- B) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on findings.
- C) Whether the team building the automation prefers writing it in Python or in TypeScript.
- D) Whether the task needs to finish end-to-end in under thirty seconds of wall-clock time.

**Question 14.** The `AgentDefinition` for a proposed "carrier-dispute subagent" has a vague description: "Helps with shipping stuff." The main agent rarely delegates to it even when a carrier dispute is clearly in progress.

- A) Add several more carrier-related tools to the subagent's definition so it has more capability to draw on.
- B) Subagents cannot be delegated to at all unless they're separately registered inside the project's `.mcp.json` file.
- C) Rewrite the subagent's description to state specifically what it does and when to use it, since description drives delegation.
- D) Lower the main agent's temperature, since low temperature is what's currently discouraging it from delegating.

**Question 15.** The team wants a hard guarantee that `issue_refund` is never called more than once for the same order within one session, regardless of what the model decides mid-conversation.

- A) Add a system-prompt instruction stating clearly that `issue_refund` may only be called once per order.
- B) Add a note inside the tool's own description mentioning that it should only be called once per order.
- C) Add a hook that tracks per-order refund-call counts and blocks the tool call once the one-call limit is reached.
- D) Add few-shot examples showing an agent correctly stopping after issuing exactly one refund per order.

---

## Scenario B: Multi-Vendor (Bedrock/Vertex) API Integration for a SaaS Platform (Questions 16–30)

You are integrating Claude into a SaaS platform's contract-review feature, deployed across the direct Anthropic API, Amazon Bedrock, and Google Vertex AI for regional compliance and redundancy. The feature supports interactive single-document review (a tenant uploads one contract and waits) and a nightly batch job that reprocesses tens of thousands of stored contracts across all tenants.

---

**Question 16.** The nightly job reprocesses 25,000 stored documents across all tenants with no user waiting on the result, and no step needs the model to call a tool mid-request. Which API best fits, and why?

- A) The Message Batches API — latency-tolerant, non-blocking, high-volume work processed at reduced per-token cost.
- B) The synchronous Messages API paired with a smaller model, to bring the per-request cost down instead.
- C) The synchronous Messages API run in parallel across many threads, to finish the whole batch as fast as possible.
- D) The synchronous Messages API with `max_tokens` reduced to the minimum needed for each document's summary.

**Question 17.** An engineer wants to add an "extract, validate against schema, retry failed clauses" loop to the nightly batch job to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings. Why won't this work as designed?

- A) The Batch API doesn't support system prompts, so structured validation instructions would have nowhere to live.
- B) The 24-hour completion window the Batch API allows for a job to finish makes any kind of iterative retry logic structurally impossible to run within it.
- C) The Batch API's context window is too small to hold contract-length documents alongside the checklist.
- D) The Batch API can't execute a validation tool call mid-request and feed results back within a single request.

**Question 18.** The interactive single-document review flow shows tenants a real-time progress indicator while Claude analyzes their uploaded contract. What technique best supports this user experience?

- A) The Batch API, since it's the option specifically designed to support real-time, incremental feedback to users.
- B) Increasing `max_tokens` so the full analysis response has room to arrive complete rather than getting cut off.
- C) Streaming, so the UI can render output incrementally as it arrives and reduce perceived latency for the tenant.
- D) Polling the Batch API's status endpoint once every second until the analysis job reports as finished.

**Question 19.** Every request sends the same 5,000-token clause checklist and review instructions, followed by the specific contract text, which varies per request. What optimization most directly reduces both latency and cost across many requests?

- A) Move the 5,000-token clause checklist into a few-shot example block instead of plain instruction text.
- B) Switch to the smallest available model regardless of the effect that has on review quality and accuracy across contracts reviewed.
- C) Place the stable instructions and checklist first, enable prompt caching, and put the varying contract text last.
- D) Truncate the clause checklist so fewer tokens are spent on it in every single review request sent.

**Question 20.** The review schema currently requires a `renewal_clause` field on every contract summary. Many contracts have no renewal clause, and the model has started inventing plausible-sounding clause text rather than reporting none.

- A) Remove the `renewal_clause` field from the schema entirely, for every contract summary going forward.
- B) Add a prompt instruction telling the model explicitly not to invent renewal-clause values that aren't present.
- C) Lower the model's temperature, on the theory that less-random sampling will reduce invented clause values.
- D) Make `renewal_clause` nullable so its genuine absence can be reported truthfully instead of invented.

**Question 21.** Two credible review passes on the same contract disagree on the liability cap: one reads $2,000,000 and another reads $2,500,000, and there's no way to tell which is correct from context alone.

- A) Average the two liability-cap values together and report the midpoint as the contract's actual liability cap.
- B) Always trust whichever review pass ran first and treat its liability-cap reading as the authoritative one.
- C) Discard the contract from the pipeline entirely, on the theory that disagreement makes the data unreliable.
- D) Flag the liability-cap field for human review with both candidate values and their source, rather than picking one.

**Question 22.** The review tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the downstream tenant dashboard. What is the most reliable fix?

- A) Wrap the parse in a try/catch block and retry the exact same request with "valid JSON only" appended to the prompt text.
- B) Define a `submit_review` tool whose schema matches the review structure, and read data from the `tool_use` block.
- C) Ask the model for YAML output instead of JSON, since YAML is more forgiving of small formatting drift.
- D) Add a JSON-repair library that attempts to fix common syntax issues in the text before parsing runs.

**Question 23.** Since switching to strict schema-constrained review output, extraction always parses successfully, but some extracted per-clause obligation amounts don't sum to the stated total contract value.

- A) Give the schema stricter numeric types, since that is what's letting the totals mismatch through undetected.
- B) Raise `max_tokens`, since output is likely being truncated mid-generation before every obligation is captured.
- C) Abandon tool-use output entirely and return to free-text extraction paired with full human review.
- D) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks totals against clause-level sums.

**Question 24.** A subset of incoming contracts are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

- A) Reject scanned contracts with no text layer from the pipeline entirely, routing them to manual review instead.
- B) Increase `max_tokens` so the model has more room to work through the degraded, damaged OCR text it receives.
- C) Switch to a larger model, since a bigger model is always better at reading noisy or damaged OCR text.
- D) Send the contract image itself as a content block alongside the review instructions, using native vision input.

**Question 25.** The pipeline needs to run review on six sections of a long master service agreement concurrently to keep latency reasonable, rather than processing sections one at a time.

- A) Use streaming for each section's request, since streaming is the only mechanism that supports concurrency.
- B) Use the Batch API, since it's the only way in the platform to have more than one request running at once.
- C) Send a single request with all six agreement sections concatenated together, on the assumption that Claude parallelizes work internally across them.
- D) Handle sections with async, non-blocking requests so several can be in flight at once, increasing effective concurrency.

**Question 26.** The platform plans to run the same review pipeline through the direct Anthropic API, Amazon Bedrock, and Google Vertex AI for different regional deployments. What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth and rollout timing can differ.
- B) Bedrock and Vertex each require a completely different prompting approach and schema design from one another and from the direct API.
- C) Batch processing is unavailable across all three vendor integrations the platform plans to deploy through.
- D) Extraction accuracy and latency are guaranteed identical to the millisecond across all three vendors used.

**Question 27.** The team enables extended thinking on a complex multi-step review-and-validation task that uses tool calls across several turns. What must the integration layer do correctly?

- A) Ignore thinking content entirely in the integration layer, since it never affects any downstream turn.
- B) Convert the thinking output into a separate tool call before continuing the multi-step review conversation.
- C) Handle the thinking content block as distinct from the final answer, typically preserving it across turns.
- D) Discard thinking content only in turns where a tool call also happens to be present in the response.

**Question 28.** Finance asks for an accurate per-tenant cost breakdown for the review pipeline, but the current cost model only estimates based on average prompt length. What should the improved cost model account for separately?

- A) Account only for cache read tokens, since caching is assumed to be the single dominant cost driver here.
- B) Account only for output tokens, treating input tokens as effectively free in the per-tenant cost model.
- C) Account for input tokens, output tokens, and cache read/write tokens separately, since each is priced differently, to increase the breakdown's accuracy.
- D) Apply a flat per-contract fee regardless of how many tokens any individual review actually consumes.

**Question 29.** A new engineer argues that once Claude is integrated across all three vendors, the team can skip code review on the pipeline's application code since "the AI part is the risky part." What is the correct response?

- A) Standard SDLC practices — review, testing, version control — still apply to the application code around Claude.
- B) Review should be skipped entirely for any code in the pipeline that happens to call out to an external, third-party API service.
- C) Code review becomes unnecessary for the pipeline's code once its evals are consistently passing.
- D) Only the prompt itself needs review; the surrounding vendor-routing code is low-risk by definition.

**Question 30.** A single long-running session is used across a whole day to process unrelated contract batches from different tenants, and the team notices Claude increasingly referencing details from unrelated earlier tenants' contracts.

- A) Reduce the model's temperature, on the theory that less-random sampling will prevent cross-tenant referencing.
- B) Start a fresh session (or `/compact`) at natural boundaries, such as between different tenants' batches.
- C) Ask the model to "ignore earlier contracts" at the start of processing each new tenant's batch.
- D) Increase the context window so more history fits in a single session without causing confusion.

---

## Scenario C: Model Tiering for a High-Volume Ticket-Triage Service (Questions 31–45)

You run a service that triages hundreds of thousands of inbound support tickets per day — classifying category, urgency, and suggested team — before a human ever sees them. Cost, latency, and consistency all matter, and the team is tuning model tiering, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the triage classification task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well. Which model tier best fits the default path?

- A) The highest-capability tier available for every ticket, to guarantee quality regardless of how simple it is.
- B) A fast, low-latency tier suited to high-volume/low-complexity work, reserving a higher tier for flagged complex tickets, independent of any temperature or sampling settings.
- C) Whichever tier happens to be cheapest per token, regardless of whether it actually fits the triage task.
- D) The same tier used for the company's hardest reasoning tasks, applied uniformly for consistency's sake.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a complex multi-product billing dispute) where the fast default model produces shallow triage decisions. What is the most targeted fix?

- A) Route only the flagged complex tickets to a higher tier or one with extended thinking, keeping the rest on the fast path.
- B) Add more few-shot examples to the fast model's prompt, applied uniformly across every ticket that arrives.
- C) Switch every incoming ticket to the highest-capability tier available, just to be safe across the board.
- D) Increase `max_tokens` for every ticket, including the vast majority that never come close to the current limit at all.

**Question 33.** The triage service currently floats to "whatever model is latest" in production. After a routine model update, category assignments shifted noticeably without any code change. What should the team do differently?

- A) Roll back to the oldest available model version and keep the triage service pinned there permanently.
- B) Pin a specific model version in production and deliberately test before any upgrade, rather than floating to latest.
- C) Disable all prompt caching across the service, on the theory that caching is what's driving the drift.
- D) Do nothing — model output is inherently non-deterministic, so pinning a version wouldn't change the drift anyway.

**Question 34.** Triage output needs a consistent structure (category, urgency, suggested team, confidence) but detailed prose instructions describing the structure haven't produced consistent output. What technique is most likely to help?

- A) Write an even longer, more detailed prose description of the same category/urgency/team/confidence structure the prompt already specifies.
- B) Ask the model to restate the desired structure back and self-validate it before it actually triages the ticket.
- C) Provide 2–3 few-shot examples demonstrating the exact structure — category, urgency, team, confidence — desired.
- D) Lower the temperature to zero, on the theory that determinism alone will produce consistent structure.

**Question 35.** A ticket thread is very long (60+ messages). The team wants a maximally detailed triage rationale and considers requesting a very long output to match. What tradeoff must they account for?

- A) Input and output tokens share one context-window budget, so a long input leaves less room for output.
- B) None — input tokens and output tokens are budgeted from two completely independent token pools.
- C) Output length has essentially no measurable effect on the request's overall end-to-end latency.
- D) Long outputs get truncated automatically regardless of how large the model's context window actually is.

**Question 36.** The triage prompt currently places the specific ticket text before the general classification instructions and desired format in every request. Why might reordering improve both consistency and cacheability?

- A) Placing every instruction last in the request always improves how closely the model attends to it.
- B) Reordering the prompt only ever affects cost, and it never has any bearing on output consistency.
- C) Stable instructions belong first (or in the system prompt) to form a cacheable prefix; ticket text follows as the varying part.
- D) The order requests are assembled in has no measurable effect on either consistency or on caching.

**Question 37.** Finance wants to know exactly how much the triage service costs per ticket, but the team currently estimates cost only from average prompt length. What should be instrumented instead?

- A) Instrument actual token usage per request — input, output, and cache — attributed back to each individual ticket, to increase visibility into the real cost driver.
- B) Instrument wall-clock latency per ticket and use that measured latency as a stand-in proxy for cost.
- C) Instrument the number of API calls made only, without regard to how many tokens any call actually used.
- D) Apply a flat cost assumption derived from the raw character count of each incoming ticket's text.

**Question 38.** An engineer writes an automated eval that asserts the triage category output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the categorizations look correct on manual review. What is the most likely issue with the eval design?

- A) The model itself is broken and is now consistently producing incorrect triage categorizations.
- B) LLM output is non-deterministic; exact-string-match evals are the wrong tool — check for required content instead.
- C) The eval simply needs a longer, more detailed reference string for the comparison to succeed reliably.
- D) Temperature should be raised on these requests, since a higher temperature is what will fix these intermittent exact-match failures.

**Question 39.** Ticket threads include full raw metadata dumps (every field of every message, including internal routing headers) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost. What is the best fix?

- A) Increase `max_tokens` on every request so the pipeline has room to accommodate the extra metadata.
- B) Switch to a model with an even larger context window so the metadata bloat matters proportionally less across every request.
- C) Summarize the raw metadata dump with a second Claude call before it's handed off to triage.
- D) Prune tool and metadata output down to the relevant fields before it ever enters the triage prompt.

**Question 40.** For very long ticket threads, the team notices triage decisions consistently miss details from the middle of the conversation while capturing the opening and closing messages well. What is the most effective mitigation?

- A) Switch to a model with an even larger context window than the one currently used for triage.
- B) Add an instruction telling the model to "pay equal attention to the whole conversation" uniformly.
- C) Alphabetize the individual messages in the thread before handing the conversation off for triage.
- D) Put a key-facts summary at the start and organize detailed content under clear headers to counter the mid-text miss.

**Question 41.** A triage rationale confidently states that a customer already received a refund, but on manual review, no refund was ever issued in the ticket thread. What practice would most help catch this class of error before it reaches routing?

- A) Trust confident, fluent-sounding rationale text as evidence of correctness by default, without further checks.
- B) Apply skepticism toward confident output — verify claims such as "refund issued" against the source thread.
- C) Increase the model's temperature so its answers come across as sounding noticeably less confident.
- D) Shorten the rationale text so there is simply less room within it for errors to appear, without adding any real validation step.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON. What is the more reliable approach?

- A) Repeat the "always output valid structured JSON with these exact fields" instruction even more emphatically in the prompt.
- B) Use tool-use/schema-constrained output so structure is enforced by the API mechanism, not requested through prose.
- C) Post-process every response to strip out any text that appears before the first opening brace.
- D) Increase `max_tokens` so there's enough room for both the free-text preamble and the JSON that follows.

**Question 43.** The team wants to add an exploratory step that scans a customer's full ticket history for context before triaging the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail. What is the best structural approach?

- A) Load the customer's entire ticket history directly into the main triage prompt on every single incoming request, regardless of length.
- B) Skip historical context entirely, to avoid any risk of the exploratory scan bloating the main context.
- C) Have a subagent scan the ticket history in an isolated context and return only a distilled, relevant summary.
- D) Increase the context window used for triage so the full ticket history always fits without trimming.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples. What consideration should drive the choice?

- A) Multi-shot prompting is always strictly better than zero-shot, regardless of how simple the task is.
- B) For a simple, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its cost on harder formatting needs, temperature settings aside.
- C) Zero-shot prompting is required by the platform whenever latency is a consideration at all for a task.
- D) The choice between zero-shot and multi-shot has no measurable effect on either cost or latency.

**Question 45.** The triage prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression. What practice would have prevented this?

- A) Lock the prompt entirely so no engineer can change it again, on the assumption that a frozen prompt guarantees deterministic behavior forever.
- B) Restrict prompt access so only one designated engineer is ever allowed to read it.
- C) Treat prompts as versioned artifacts, like code, so changes are tracked and regressions can be attributed and rolled back.
- D) Rewrite the triage prompt completely from scratch once every calendar quarter.

---

## Scenario D: Claude Code and MCP for a Mobile App Team's CI Pipeline (Questions 46–60)

You support a 20-engineer mobile app team (iOS and Android) that uses Claude Code locally and in CI for PR review, release-note generation, and native-dependency auditing. The team also relies on MCP servers for its issue tracker, build-status system, and internal design docs. You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the mobile team's repository, but Claude Code doesn't apply the team's established Kotlin/Swift style conventions for them, even though a teammate's machine applies them correctly. What is the most likely cause?

- A) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config, never version-controlled.
- B) The new engineer needs to run `/memory` first in order to activate any of Claude Code's memory files.
- C) A project `CLAUDE.md` requires an explicit `@import` from the repository root before it takes effect at all.
- D) The conventions file exceeded a size limit and was silently truncated when the repository was cloned.

**Question 47.** A nightly CI job invokes Claude Code to generate release notes from merged PRs and consistently hangs until timeout, with no visible error in the logs. What is the most likely cause?

- A) The job is missing `-p`/`--print` (headless mode), so it's waiting on interactive input CI never provides.
- B) The pull requests being summarized by the nightly job are simply too large for Claude Code to process in a single run.
- C) The CI runner lacks the necessary permission to call the Claude API from within its pipeline.
- D) The repository's `CLAUDE.md` file is malformed in a way that's causing the process to hang.

**Question 48.** A downstream release dashboard parses Claude Code's release-notes output with regex to categorize entries, and the parser breaks whenever output formatting drifts slightly between runs. What is the robust fix?

- A) Harden the existing regex with more permissive fallback patterns to catch the structured output's drifting formats.
- B) Post the entire raw output as a single unparsed changelog entry instead of attempting to parse it.
- C) Add an even stronger prompt instruction telling the model never to deviate from the expected format.
- D) Run with `--output-format json` and a `--json-schema` defining the release-notes structure for machine-parseable output.

**Question 49.** The team's `/audit-native-libs` custom command prints thousands of lines of native-dependency graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it. What frontmatter change fixes this?

- A) Add an `argument-hint`, so developers are nudged to scope the dependency-graph analysis more narrowly.
- B) Add `allowed-tools`, restricting the command so it can only perform read-only dependency operations.
- C) Set `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns.
- D) Remove the `/audit-native-libs` command entirely, since its output volume can't otherwise be controlled.

**Question 50.** An internal `/scaffold-screen` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files. What is the correct guardrail?

- A) Add a warning inside the skill's instructions telling Claude never to run shell commands during scaffolding.
- B) Add a hook that logs every Bash command the skill runs, without actually restricting which tools remain callable.
- C) Convert the skill into a slash command instead, since slash commands are structurally unable to run tools.
- D) Configure `allowed-tools` in the skill's frontmatter to permit only file creation, so Bash becomes unavailable.

**Question 51.** An engineer needs to understand how push-notification handling flows across a large, unfamiliar codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins. What is the best approach?

- A) Read every file in the entire codebase in one continuous pass, to be as thorough as possible up front.
- B) Skip exploration entirely and infer the push-notification architecture just from the directory names.
- C) Use the Explore subagent for discovery, so verbose exploration runs in an isolated context and only a summary returns.
- D) Split the exploration and implementation work across two separate terminal windows running side by side.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings. What should they do?

- A) Start a brand-new session and rely on memory of what was discovered during the earlier exploration.
- B) Delete the project's `CLAUDE.md` file temporarily, to free up a bit of extra context space for the remaining implementation work.
- C) Continue working as-is; Claude automatically discards context that has become irrelevant on its own.
- D) Run `/compact` to summarize the conversation and reduce context usage while preserving the key findings.

**Question 53.** A multi-step Claude Code task that reads a build-config file, calls an internal MCP tool for build status, and writes a QA report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data. Where should debugging focus next?

- A) Re-read the build-config file again from scratch, since that was the earliest step in the whole task.
- B) Do nothing further — correct inputs producing a wrong report means the task should simply be re-run.
- C) Focus on the step between the MCP tool's confirmed-valid data and the final report, since that's where reasoning could diverge.
- D) Focus on the network connection to the MCP server, since that's the most operationally complex step.

**Question 54.** A build-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did. What is the correct first diagnostic step?

- A) Assume the failure is a model problem from the outset and rewrite the prompt accordingly.
- B) Switch to a different underlying model to see whether the same failure still occurs.
- C) Restart the CI runner and simply try running the same failing job again.
- D) Isolate whether the failure is in the integration layer or the model's output by examining the actual trace of what was sent and received.

**Question 55.** The internal issue-tracking system needs to be reachable from Claude Code sessions across the whole mobile organization, not just one squad, and should be maintainable by the platform team independently of any consuming application. What is the best approach?

- A) Have each engineer curl the issue-tracking API manually whenever they need tracker data during a session.
- B) Build an MCP server exposing issue-tracking operations as tools, shared and maintained centrally across the org.
- C) Have each team paste their own issue-tracker API credentials directly into their individual `CLAUDE.md`.
- D) Hard-code issue-tracking logic separately inside each squad's own custom skill, maintaining one duplicate implementation per squad.

**Question 56.** An MCP server for internal design docs exposes both a `search_docs` tool and a way for agents to see what documentation exists without an exploratory search call. What is the second capability an example of?

- A) A built-in tool the platform provides automatically to every connected agent by default, without any MCP server involved.
- B) An MCP tool, functionally identical in behavior to the existing `search_docs` tool, sharing its input schema.
- C) A Claude Code Skill packaged specifically for browsing the internal design-docs catalog.
- D) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.

**Question 57.** The team is deciding whether the build-status MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service. What should drive the decision?

- A) stdio servers are always faster than a remote, network-hosted deployment, regardless of the actual deployment context or number of clients accessing them.
- B) It should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote for shared services.
- C) MCP only supports a single communication pattern, so there's no real decision here to make.
- D) Remote, network-hosted servers can't expose tools at all — only resources are available remotely.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has an issue-tracker API token hardcoded directly in the file. What is the correct fix?

- A) Base64-encode the token before committing the same `.mcp.json` file to the repository, since encoding hides it from a casual glance at the file's schema.
- B) Rotate the token on a weekly schedule instead of removing it from the committed file at all.
- C) Move the token to environment-variable expansion so the secret isn't committed to version control.
- D) Move the entire `.mcp.json` file into a private repository instead of the current public one.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full issue-deletion rights) than any actual mobile-team workflow requires. What is the correct remediation, consistent with least-privilege principles?

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities.
- B) Add logging around the broad-access tools so any future misuse can be reviewed after the fact.
- C) Add a confirmation prompt before any issue-deletion call goes through, leaving the broader granted scope and its full-deletion rights otherwise unchanged.
- D) Leave access as it currently is, since no actual misuse has been observed by the team yet.

**Question 60.** The platform team is choosing how to expose a one-off, squad-specific release-checklist workflow used by a single small team, versus a widely-reused build-status-checking capability needed by every agent across the mobile org. How should each be built?

- A) Build both as MCP servers, since MCP is claimed to be the correct choice for any shared capability at all.
- B) Build the one-off checklist as a Skill scoped to that squad, and the shared build-status capability as a centrally maintained MCP server.
- C) Build both as Skills, since Skills are asserted to always be reusable across squads by design.
- D) Build both as built-in tools, since built-in tools are claimed to require the least setup overall regardless of how narrowly or widely each capability is actually used.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-D, 2-A, 3-C, 4-A, 5-A, 6-B, 7-A, 8-B, 9-A, 10-D, 11-A, 12-B, 13-B, 14-C, 15-C, 16-A, 17-D, 18-C, 19-C, 20-D, 21-D, 22-B, 23-D, 24-D, 25-D, 26-A, 27-C, 28-C, 29-A, 30-B, 31-B, 32-A, 33-B, 34-C, 35-A, 36-C, 37-A, 38-B, 39-D, 40-D, 41-B, 42-B, 43-C, 44-B, 45-C, 46-A, 47-A, 48-D, 49-C, 50-D, 51-C, 52-D, 53-C, 54-D, 55-B, 56-D, 57-B, 58-C, 59-A, 60-B

---

**1. D** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text phrases (A) are unreliable; a fixed call cap (B) ignores what `stop_reason` actually says; a clean tool result (C) doesn't indicate the turn itself is complete.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. C** — A financial/safety-critical rule needs deterministic enforcement via a hook that blocks the call outright. A, B, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. A** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (D) guarantees some tool call, but not which one. B and C are probabilistic.

**5. A** — Removing tools unrelated to fulfillment (or delegating them elsewhere) directly reduces the candidate set the agent must reason over, improving selection reliability. B adds prompt overhead without removing the actual capability bloat. C and D don't address tool-selection reliability at all.

**6. B** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. A hook that only logs (C) doesn't change what the agent itself receives. D reduces frequency without fixing the missing information.

**7. A** — "Not stocked" is a valid empty result, not a failure — return success with that result. B hides real signal from the agent. C invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, C, and D are false claims about the technology.

**9. A** — A narrowly-scoped subagent with only the refund tool and explicit criteria minimizes accidental refunds while the main agent reasons about unrelated tools. B overgeneralizes; C and D are unsupported technical claims.

**10. D** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on resolution. A and B don't address the root accumulation problem; C removes needed capability.

**11. A** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. B forces reconstruction from a raw transcript. C omits diagnostic context. D conveys mood, not facts.

**12. B** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, C, and D are unsupported absolute claims.

**13. B** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. C** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, B, and D misdiagnose the cause.

**15. C** — A per-order call-count hook is the only option that deterministically guarantees the limit; A, B, and D remain probabilistic prompt-level guidance.

**16. A** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. C doesn't reduce per-token cost; B and D risk quality or truncate output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and C misidentify the actual limitation.

**18. C** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case; B and D don't address perceived latency.

**19. C** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and C rely on probabilistic compliance; A removes the field's value entirely.

**21. D** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and C all discard information or guess.

**22. B** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and D are recovery layers for a problem that can be eliminated; C swaps one fragile text format for another.

**23. D** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against clause-level sums) is needed on top. A, B, and C misdiagnose or abandon a working mechanism.

**24. D** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B and C don't address the actual data-quality bottleneck; A discards otherwise-processable documents.

**25. D** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**26. A** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. C** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and D mishandle or misdescribe this.

**28. C** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-tenant cost breakdown. A, B, and D all oversimplify in ways that produce an inaccurate model.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. B** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. C doesn't address cross-contamination; D is an unreliable prompt-level mitigation; A is an unrelated lever.

**31. B** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and D overspend by default; C ignores task fit.

**32. A** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. B, C, and D apply broad, costly fixes to a narrow problem.

**33. B** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. D wrongly assumes non-determinism explains version-to-version drift and so accepts avoidable risk; A and C are unhelpful overcorrections unrelated to the actual fix.

**34. C** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A repeats a failed approach; B and D don't reliably fix structural consistency.

**35. A** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. B, C, and D misstate this relationship.

**36. C** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. A, B, and D misstate the effect of ordering.

**37. A** — Actual per-request token usage (input/output/cache) attributed per ticket gives an accurate cost picture; estimates from average length or unrelated proxies (B, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. D** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. B and C work around the symptom without reducing waste; A adds cost without fixing anything.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and C don't address the underlying attention pattern.

**41. B** — Verifying key claims against the source thread catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; C and D don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue.

**43. C** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and D reintroduce the bloat risk; B discards potentially useful context entirely.

**44. B** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and C are absolute claims that don't hold generally; D is false.

**45. C** — Versioning prompts like code enables attribution and rollback for quality regressions. A wrongly assumes freezing a prompt makes its behavior deterministic; B and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. A** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. B, C, and D misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. D** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, B, and C are reactive or abandon the structured-output requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; A narrows scope but doesn't isolate output; D removes useful functionality.

**50. D** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; B only logs after the fact rather than preventing the action; C is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. D** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; B frees trivial space while losing standards; C describes behavior that doesn't exist.

**53. C** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and D re-check or skip already-verified steps; B skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and B guess without diagnosis; C doesn't investigate the cause at all.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. D** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and C mischaracterize this capability.

**57. B** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. C** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and D don't remove the exposed credential from history or ongoing risk.

**59. A** — Least privilege means removing unnecessary capability, not just observing or gating its misuse after the fact. B and C are detective/compensating controls that leave the broad grant itself in place; D accepts unnecessary risk.

**60. B** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, squad-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 3.*
