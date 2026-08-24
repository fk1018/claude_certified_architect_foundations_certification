# CCDVF Practice Exam 7

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Order-Fulfillment Automation Agent for an E-Commerce Retailer, Multi-Vendor Bedrock/Vertex API Integration for a SaaS Platform, Model Tiering for a High-Volume Ticket-Triage Service, Claude Code and MCP for a Mobile App Team's CI Pipeline) |
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

You are building an internal agent for a mid-size e-commerce retailer's warehouse operations team using the Claude Agent SDK. The agent has custom tools (`check_inventory`, `reroute_shipment`, `issue_refund`, `notify_customer`) and helps ops staff resolve stuck orders and delayed shipments. Reroutes and refunds carry real logistics and financial cost, so tool governance matters as much as reasoning quality.

---

**Question 1.** An engineer wants the agent's tool-use loop to keep executing tools and returning results until the model has no more tool calls to make. What should the loop key off?

- A) Whether the assistant's reply text includes a closing phrase such as "resolved" or "done," checked with a simple string match.
- B) A fixed cap of five tool calls per case, escalating automatically once the cap is hit regardless of whether more calls are queued.
- C) Whether the most recently executed tool returned an error field, treating any error response as the natural stopping point.
- D) The `stop_reason` field on the response: keep looping while it reads `tool_use`, and stop once it reads `end_turn`.

**Question 2.** After the agent calls `reroute_shipment` and your code executes it, what must happen for the agent to correctly continue reasoning about the case?

- A) Write the reroute confirmation to an internal audit log, without feeding anything back into the conversation Claude sees.
- B) Append a `tool_result` block referencing the matching `tool_use` ID to the conversation, then send the full conversation back to the model.
- C) Fold a short summary of the reroute outcome into the system prompt so it stays visible for the rest of the conversation.
- D) Close out the current conversation entirely and open a new one that begins with a written summary of the reroute, then continue reasoning about the case there.

**Question 3.** Company policy requires manager approval before `issue_refund` is called for any refund above $500. The system prompt states this clearly, but logs show occasional autonomous refunds above the threshold. What is the most reliable fix?

- A) Repeat the $500 rule at both the start and end of the system prompt, add a bolded warning line, and restate the exact threshold again inside the tool's own description field for good measure.
- B) Implement a hook that intercepts `issue_refund` calls and blocks any refund above the threshold without prior approval.
- C) Add several few-shot examples of the agent correctly escalating refunds over $500 to a manager.
- D) Lower the model's temperature so it follows the stated $500 policy more consistently.

**Question 4.** The team wants the agent to always call a `classify_order_risk` tool first, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation?

- A) State in the system prompt that `classify_order_risk` must always run first, above every other instruction.
- B) Set `tool_choice: "any"` on the first request so a tool call of some kind is guaranteed to happen.
- C) Add several few-shot examples showing `classify_order_risk` called before any other tool.
- D) Set `tool_choice: {"type": "tool", "name": "classify_order_risk"}` on the first request, then use normal tool choice on later turns.

**Question 5.** The agent currently has 18 tools, including several rarely-used ones (loyalty-point adjustments, marketing-email triggers, warranty lookups) unrelated to fulfillment. Tool selection has become unreliable.

Question: What is the most direct fix?

- A) Add a system prompt note listing which of the 18 tools count as "primary" for fulfillment work, with a short justification for each one kept on the list.
- B) Increase `max_tokens` so the agent has more room to reason before picking a tool.
- C) Remove or scope out the unrelated tools.
- D) Add more few-shot examples of correct tool selection covering all 18 tools.

**Question 6.** `check_inventory` currently returns the string `"Error"` for every possible failure — invalid SKU, permission denied, or warehouse-system timeout. The agent responds inconsistently to each. What is the best fix?

- A) Add a hook that automatically retries every failed call the same way, regardless of whether that particular failure is retryable.
- B) Add a system prompt instruction telling the agent to infer the failure type from the surrounding conversation.
- C) Return structured error metadata from the tool itself: an error category, a retryable flag, and a human-readable description.
- D) Increase the warehouse system's timeout threshold so timeout failures become rarer.

**Question 7.** When `reroute_shipment` finds a shipment is already at its final hub and needs no reroute, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same call. What should change?

- A) Add a hook that silently suppresses this specific error code and ends the conversation.
- B) Have the agent call `check_inventory` first every time, to determine in advance whether a reroute will be needed.
- C) Return a successful response indicating no reroute is needed, reserving error responses for actual failures.
- D) Add a system prompt note explaining that this particular error usually just means no reroute is needed.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `check_inventory`, then `reroute_shipment`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for fulfillment exceptions?

- A) Model-driven selection is always cheaper, since it structurally skips unnecessary reasoning tokens on every case, no matter how the mix of cases shifts over time.
- B) Fulfillment exceptions are high-ambiguity; the right tools and order vary by case, which a fixed sequence can't adapt to.
- C) The Claude Agent SDK technically cannot execute a fixed, hard-coded tool sequence at all.
- D) A fixed sequence cannot invoke custom tools like `reroute_shipment`, only built-in ones.

**Question 9.** The team is deciding whether to give the main fulfillment agent the `issue_refund` tool directly or delegate refund decisions to a separate, narrowly-scoped subagent. Refunds have real financial cost and should only happen under specific criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent?

- A) Subagents are strictly required any time a tool has a real-world side effect, by design of the Agent SDK, regardless of how narrow that tool's scope already is.
- B) The main agent's context window is too small to hold the refund tool's schema alongside its other 17 tools.
- C) A narrowly-scoped subagent reduces the chance of unnecessary refunds.
- D) Subagents execute measurably faster than the same tool called directly by the main agent.

**Question 10.** During a long-running case investigation, the agent's context fills with verbose raw inventory-log output, leaving little room for reasoning about the actual root cause of the delay.

Question: What is the best structural fix?

- A) Delegate the exploration to a subagent that returns a distilled summary, keeping the main agent's context focused on diagnosis.
- B) Increase `max_tokens` on every request so the agent's responses have more room, and raise the per-call timeout so slower warehouse-system queries don't get cut off mid-response.
- C) Read only the first 50 lines of every inventory query result before passing it along.
- D) Disable inventory checks entirely and rely on shipment status alone for root-cause reasoning.

**Question 11.** The agent successfully reroutes a stuck shipment, but the human ops lead later has no visibility into what the agent tried before escalating — logs show 15 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include?

- A) A fully structured transcript listing every tool call and result in chronological order, with no summary or recommendation attached.
- B) A short handoff summary: what was tried, what was found, and a recommended next action.
- C) Just the final error message, since the human can re-investigate the rest from there.
- D) A sentiment score estimating how urgent the case seemed based on wording.

**Question 12.** The team is deciding between letting ops staff run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own warehouse infrastructure.

Question: What is the core tradeoff?

- A) Self-hosted agents structurally cannot register or call custom tools like `reroute_shipment`.
- B) Managed agents cannot reach any private warehouse infrastructure under any configuration.
- C) Operational control (self-hosted) versus operational burden (managed) — there is no difference in which tools the agent can call.
- D) Managed agents are, as a category, always less secure than a self-hosted deployment of the same harness.

**Question 13.** An engineer asks whether the order-exception handling task should be built as a fixed workflow or an agent.

Question: What is the deciding factor?

- A) Whether the task involves calling more than three distinct tools in a case.
- B) Whether the team prefers to write the harness in Python or TypeScript.
- C) Whether the task needs to finish in under 30 seconds end to end.
- D) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.

**Question 14.** The `AgentDefinition` for a proposed "refund subagent" has a vague description: "Handles refunds." The main agent rarely delegates to it even when a refund decision is clearly needed.

Question: What is the most likely cause and fix?

- A) The description drives delegation choices; rewriting it to state what the subagent does will fix under-delegation.
- B) The subagent needs more tools attached; add several more refund-related tools to widen its definition.
- C) The main agent's temperature setting is too low for it to consider delegating work out at all.
- D) Subagents cannot be delegated to at all unless they are also registered as MCP servers in `.mcp.json`, separate from the `AgentDefinition` itself.

**Question 15.** The team wants a hard guarantee that `reroute_shipment` is never called more than once for the same order within one case, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism?

- A) A system prompt instruction stating the one-call-per-order limit as clearly as possible.
- B) A note in the tool's own description mentioning that the limit exists.
- C) Several few-shot examples showing an agent correctly stopping after one reroute.
- D) A hook that tracks per-order call counts and blocks the tool call once the limit is reached.

---

## Scenario B: Multi-Vendor (Bedrock/Vertex) API Integration for a SaaS Platform (Questions 16–30)

Your SaaS company offers customers a choice of running its Claude-powered features through the direct Anthropic API, Amazon Bedrock, or Google Vertex AI, depending on each customer's compliance region. The integration team maintains a single adapter layer across all three, supporting both interactive customer-facing chat and large nightly batch jobs.

---

**Question 16.** A nightly job classifies 25,000 support documents with no user waiting on the result. No step needs the model to call a tool mid-request.

Question: Which API best fits, and why?

- A) The synchronous Messages API with a smaller model chosen mainly to reduce cost per call.
- B) The synchronous Messages API run in parallel across many worker threads, to finish as fast as possible.
- C) The synchronous Messages API with `max_tokens` reduced to the minimum viable value.
- D) The Message Batches API — latency-tolerant, non-blocking, high-volume work at a reduced per-token rate.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry failed fields" loop to the nightly job to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed?

- A) The Batch API silently drops any system prompt included in a request.
- B) The 24-hour completion window makes any kind of retry logic structurally impossible.
- C) The Batch API cannot execute a validation tool call mid-request and feed results back within a single request.
- D) The Batch API's context window is too small to hold a full support document alongside the extraction schema and instructions.

**Question 18.** The interactive customer-facing chat feature shows users a real-time progress indicator while Claude composes its reply.

Question: What technique best supports this user experience?

- A) The Batch API, since it's the API purpose-built for real-time interactive feedback.
- B) Increasing `max_tokens` so the complete response arrives to the client sooner.
- C) Streaming, so the UI can render output incrementally and reduce perceived latency.
- D) Polling the Batch API's status endpoint once per second until the job completes.

**Question 19.** Every request sends the same 5,000-token platform instructions and configuration schema, followed by customer-specific data that varies per request.

Question: What optimization most directly reduces both latency and cost across many requests?

- A) Move the configuration schema into a few-shot example block near the end of the request instead.
- B) Place the stable instructions and schema first in the system prompt, enable prompt caching, and put the varying customer data last.
- C) Truncate the configuration schema down to save on input tokens.
- D) Switch to the smallest available model across the board, regardless of the quality tradeoff.

**Question 20.** The extraction schema currently requires a `discount_code` field on every order record. Many orders have no discount, and the model has started inventing small codes rather than reporting none.

Question: What schema change fixes this?

- A) Remove the `discount_code` field from the schema entirely, along with the data it captures.
- B) Add a prompt instruction telling the model not to invent discount code values.
- C) Make `discount_code` nullable in the schema so its genuine absence can be reported truthfully.
- D) Lower the sampling temperature to reduce the rate of invented values.

**Question 21.** Two credible extraction passes on the same customer record disagree — one reads a value as $1,050.00, the other as $1,050.05 — and there's no way to tell which is correct from context alone.

Question: What should the pipeline do?

- A) Average the two candidate values and store the result as the final figure.
- B) Discard the record entirely, on the assumption that any disagreement means the data is unreliable.
- C) Always trust whichever extraction pass ran first, since it's deterministic which one that is.
- D) Flag the field for human review with both candidate values and their source, rather than silently picking one.

**Question 22.** The extraction pipeline's JSON output occasionally fails to parse — about 3% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix?

- A) Define a `submit_result` tool matching the extraction structure and read data from the `tool_use` block.
- B) Wrap the parse step in a try/catch, retry the request with "valid JSON only" appended to the prompt, and fall back to a stricter delimiter-based format on the second attempt if it fails again.
- C) Add a JSON-repair library that patches common syntax issues and validates the result before parsing it.
- D) Ask the model for YAML output instead, since it tolerates minor formatting drift better than JSON.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some extracted line-item amounts don't sum to the stated order total.

Question: What should you conclude and do?

- A) The schema needs stricter numeric types on every monetary field to fix this outright.
- B) `max_tokens` is set too low and is truncating output partway through generation, and should simply be raised until the mismatches disappear.
- C) Abandon tool use and return to free-text extraction with a human validating every record before it ships.
- D) Add a validation step that checks totals against line-item sums on top of schema compliance.

**Question 24.** A subset of incoming documents are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix?

- A) Send the document image as a content block, using native vision input instead of OCR text alone.
- B) Increase `max_tokens` so the model has more room to work through the degraded OCR text.
- C) Switch to a larger model, on the assumption that bigger models always read noisy text better, and pair it with a longer, more emphatic prompt insisting on careful reading.
- D) Reject scanned documents from the pipeline entirely and route them elsewhere.

**Question 25.** The pipeline needs to process five customer regions' worth of data concurrently to keep latency reasonable, rather than processing them one at a time.

Question: What must the integration layer support to do this?

- A) Streaming, since streaming is the only mechanism that unlocks concurrency at all.
- B) The Batch API, since it's the only way to have more than one request in flight at once.
- C) A single request with all five regions' data concatenated together, since Claude parallelizes internally.
- D) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.

**Question 26.** The platform runs the same feature through the direct Anthropic API, Bedrock, and Vertex AI depending on each customer's region.

Question: What should the team expect?

- A) Extraction accuracy and latency are both guaranteed to match to the millisecond across all three vendors.
- B) Vertex AI requires a completely different prompting approach and a separately designed schema.
- C) Batch processing is structurally unavailable on every third-party vendor integration.
- D) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns, run through all three vendor integrations.

Question: What must the integration layer do correctly?

- A) Ignore thinking content entirely, strip it out of every stored turn, and rebuild each vendor's request from just the final answer text and tool calls.
- B) Handle the thinking content block as distinct from final answer text, typically preserving it across the conversation.
- C) Convert any thinking output it receives into a separate synthetic tool call.
- D) Discard thinking content, but only on turns where a tool happens to be involved.

**Question 28.** Finance asks for an accurate per-customer cost breakdown across all three vendors, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately?

- A) Only cache read tokens, on the assumption that caching is the single dominant cost driver.
- B) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- C) A flat per-request fee that applies regardless of how many tokens the request actually used.
- D) Only output tokens, on the assumption that input tokens are effectively free.

**Question 29.** A new engineer argues that once Claude is integrated across the three vendors, the team can skip code review on the adapter code since "the AI part is the risky part."

Question: What is the correct response?

- A) Standard SDLC practices still apply to the code around Claude; an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that primarily calls an external API rather than doing its own logic, since the vendor's own testing already covers correctness of that call path.
- C) Code review becomes unnecessary for this adapter once its evals are passing consistently.
- D) Only the prompt text itself needs review; the surrounding adapter code is low-risk by definition.

**Question 30.** A single long-running session is used across an entire day to process unrelated data batches from different tenants, and the team notices Claude increasingly referencing details from unrelated earlier tenants.

Question: What is the best fix?

- A) Reduce the sampling temperature to make the model less likely to cross-reference earlier tenants, since lower temperature narrows which prior details it draws on.
- B) Increase the context window so that more history fits without causing confusion.
- C) Ask the model to "ignore earlier tenants" at the very start of each new batch.
- D) Start a fresh session (or `/compact`) at natural task boundaries between tenants.

---

## Scenario C: Model Tiering for a High-Volume Ticket-Triage Service (Questions 31–45)

You run a service that classifies and routes hundreds of thousands of inbound support tickets per day into the correct queue and priority level. Cost, latency, and consistency all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the triage task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well.

Question: Which model tier best fits the default path?

- A) A fast, low-latency tier suited to high-volume/low-complexity tasks, reserving a higher tier only for tickets flagged as complex.
- B) The highest-capability tier available across the board, to guarantee quality on every single ticket.
- C) Whichever tier happens to be cheapest per token that month, regardless of how well it fits the task.
- D) The same tier the company uses for its hardest reasoning tasks, purely for operational consistency.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a multi-product billing dispute) where the fast default model produces shallow, unreliable routing decisions.

Question: What is the most targeted fix?

- A) Route only the flagged complex tickets to a higher tier or one with extended thinking enabled.
- B) Add many more few-shot examples to the fast model's prompt, applied uniformly to every ticket, so the same lightweight model can pattern-match its way through the harder cases too.
- C) Switch every ticket in the pipeline to the highest-capability tier to be safe.
- D) Increase `max_tokens` for every ticket so there's more room for reasoning regardless of complexity.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, triage categories shifted noticeably without any code change.

Question: What should the team do differently?

- A) Nothing — behavior drift across model releases is expected and doesn't warrant a process change.
- B) Roll back permanently to the oldest model version the vendor still supports.
- C) Disable all prompt caching across the pipeline, on the theory that cached prefixes are driving the drift.
- D) Pin a specific model version in production and test changes, including prompt and temperature tweaks, before upgrading.

**Question 34.** Triage decisions need a consistent structure (category, priority, queue, rationale) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help?

- A) Write an even longer and more detailed prose description of the required structure.
- B) Provide 2–3 few-shot examples that demonstrate the exact structure the team wants.
- C) Lower the sampling temperature to zero across every request.
- D) Ask the model to restate the required structure back before it actually triages the ticket.

**Question 35.** A ticket thread is very long (50+ messages). The team wants a maximally detailed triage rationale and considers requesting a very long output to match.

Question: What tradeoff must they account for?

- A) None — input tokens and output tokens are budgeted from two entirely independent pools, so a 50-message thread can be paired with an unlimited-length rationale with no tradeoff at all.
- B) Long outputs are truncated by the API automatically, regardless of the context window's size.
- C) Input and output share the same context-window budget, so a long input leaves less room for output, and no increase to `max_tokens` alone can manufacture space that already went to input.
- D) Output length has no measurable effect on end-to-end request latency.

**Question 36.** The triage prompt currently places the specific ticket text before the general triage instructions and desired output format in every request.

Question: Why might reordering improve both consistency and cacheability?

- A) Order has no measurable effect on either consistency or caching across providers, so reordering is purely cosmetic and not worth the engineering time to change.
- B) Placing instructions last always improves how closely the model attends to them.
- C) Reordering only ever affects cost, and never affects consistency.
- D) Stable instructions belong in the system prompt as a cacheable prefix; ticket content should come after.

**Question 37.** Finance wants to know exactly how much the triage service costs per ticket, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead?

- A) Wall-clock latency per ticket, used as a stand-in proxy for cost, on the theory that slower responses generally correlate with heavier token usage.
- B) The raw number of API calls made, regardless of how many tokens each call used.
- C) Actual token usage per request — input, output, and cache — attributed per ticket.
- D) A flat cost assumption derived from the character count of each ticket.

**Question 38.** An engineer writes an automated eval that asserts the triage output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the routing decisions look correct on manual review.

Question: What is the most likely issue with the eval design?

- A) The model should behave deterministically call-to-call, so any variation between runs means the model itself is broken and needs to be swapped out for a different vendor entirely.
- B) LLM output is non-deterministic across calls even at fixed temperature; exact-match evals are the wrong tool — they should tolerate reasonable variation instead.
- C) The eval simply needs a longer, more detailed reference string to compare against.
- D) The sampling temperature should be raised so the intermittent failures stop occurring.

**Question 39.** Ticket payloads include full raw metadata dumps (every field of every internal system event) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix?

- A) Prune tool/data output to the relevant fields before it enters the prompt, rather than passing raw dumps and hoping an increase to `max_tokens` compensates.
- B) Increase `max_tokens` on every request so the pipeline can accommodate the extra data.
- C) Switch to a model with a larger context window so the metadata bloat matters less in practice.
- D) Add a second Claude call whose only job is to summarize the metadata before the real triage call runs.

**Question 40.** For very long ticket threads, the team notices triage rationales consistently miss details from the middle of the conversation while capturing the opening and closing messages well.

Question: What is the most effective mitigation?

- A) Switch to a model with an even larger context window, on the theory that more headroom alone resolves an attention pattern rather than a capacity limit.
- B) Put a key-facts summary at the start and organize detail under clear section headers, easing the tendency to under-attend to the middle of long inputs.
- C) Add an instruction telling the model to "pay equal attention to the whole conversation."
- D) Alphabetize the ticket's messages before sending them for triage.

**Question 41.** A triage decision confidently states a rationale referencing a prior escalation that, on manual review, never actually happened in the ticket thread.

Question: What practice would most help catch this class of error before it reaches the queue?

- A) Apply defensive skepticism toward confident output — verify claims like "prior escalation" against the source thread.
- B) Trust confident, fluent-sounding output as evidence of correctness by default, since a model producing a specific, plausible-sounding detail is unlikely to have fabricated it outright.
- C) Increase the sampling temperature so answers read as less confident.
- D) Shorten the rationale into a tightly structured bullet list, which reduces prose but does nothing to verify the claims within it.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach?

- A) Repeat the same JSON instruction even more emphatically in the prompt.
- B) Post-process every response to strip text before the first `{`, then validate the stripped text against the schema after the fact.
- C) Increase `max_tokens` so there's guaranteed room for both the preamble and the JSON.
- D) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.

**Question 43.** The team wants to add an exploratory step that scans a customer's full prior-ticket history for context before triaging the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach?

- A) Load the entire ticket history directly into the main prompt on every triage call.
- B) Skip historical context entirely, to avoid the bloat risk altogether.
- C) Increase the context window so the full history always fits without truncation.
- D) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main triage step.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice?

- A) For a simple, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its cost on tasks needing format or edge-case consistency.
- B) Multi-shot prompting is always strictly better than zero-shot, regardless of how simple, repetitive, or well-understood the underlying task already is.
- C) Zero-shot is mandatory whenever latency matters at all, even slightly.
- D) The choice between zero-shot and multi-shot has no measurable effect on cost or latency.

**Question 45.** The triage prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this?

- A) Treat the prompt (including the system prompt) as a versioned artifact, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Add a pre-commit hook that blocks any change to the prompt file outright, freezing it in place.
- C) Restrict read access to the prompt so only one designated engineer can ever view it.
- D) Rewrite the prompt from scratch on a fixed quarterly schedule, discarding the prior version each time.

---

## Scenario D: Claude Code and MCP for a Mobile App Team's CI Pipeline (Questions 46–60)

You support a mobile app team (iOS and Android) that uses Claude Code both locally and in CI for automated PR review, release-note generation, and crash-log triage. The team relies on internal MCP servers for crash reporting, app-store metadata, and build status.

---

**Question 46.** A new engineer clones the team's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause?

- A) CLAUDE.md requires an explicit `@import` from the project root before it takes effect at all.
- B) The new engineer needs to run `/memory` once to activate any memory files.
- C) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- D) The conventions file exceeded a size limit and was silently truncated on load.

**Question 47.** A nightly CI job invokes Claude Code to generate release notes and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause?

- A) The job is missing `-p`/`--print` (headless mode), so it waits on interactive input the CI runner never provides.
- B) The generated release notes are simply too large for Claude Code to finish processing, so it stalls partway through writing the file rather than exiting with an error.
- C) The CI runner lacks permission to reach the Claude API from its network.
- D) The repository's CLAUDE.md file is malformed and can't be parsed.

**Question 48.** A downstream service parses Claude Code's crash-triage output with regex to file tickets automatically, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix?

- A) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- B) Harden the regex with more permissive fallback patterns, then validate the captured groups look reasonable before filing tickets.
- C) Post the entire raw output as a single ticket comment instead of trying to parse it at all.
- D) Add a stronger prompt instruction telling the model never to deviate from the expected format.

**Question 49.** The team's `/audit-crashlogs` custom command prints thousands of lines of raw crash-stack data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this?

- A) `argument-hint`, so developers are nudged to scope the analysis more narrowly up front.
- B) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- C) `allowed-tools`, restricting the command to read-only operations only.
- D) Removing the command from the team's repository entirely.

**Question 50.** An internal `/scaffold-screen` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail?

- A) Add a warning in the skill's own instructions telling Claude never to run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- C) Require developers to commit their working tree before running any skill, as a safety net.
- D) Convert the skill into a slash command instead, since commands structurally cannot run tools.

**Question 51.** An engineer needs to understand how push-notification handling flows across a large, unfamiliar mobile codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach?

- A) Read every file in the codebase in one long pass, in file-tree order, to be as thorough as possible before writing a single line of the change.
- B) Skip exploration entirely and infer the architecture from directory names alone.
- C) Use the Explore subagent for discovery, so only a summary returns to the main conversation.
- D) Split the investigation across two separate terminal windows running side by side.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do?

- A) Start a brand-new session and rely on memory of what was learned during discovery.
- B) Delete the project's CLAUDE.md file temporarily to free up context space.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- D) Keep working as-is; Claude automatically discards context it decides is irrelevant.

**Question 53.** A multi-step Claude Code task reads a build-config file, calls an internal MCP crash-reporting tool, and writes a triage report, but produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next?

- A) Re-read the config file again from scratch, since that was the earliest step in the pipeline, and re-verify its checksum against the version stored in the build system before trusting it a second time.
- B) The step between receiving the MCP tool's valid data and producing the final report, since that's where the divergence most likely occurred.
- C) The network connection to the MCP server, since that's the most complex piece of infrastructure involved.
- D) Nothing — a wrong final report despite correct inputs just means the task should be re-run as-is.

**Question 54.** A build-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step?

- A) Isolate whether the failure is in the integration layer or the model's output, by examining the trace of exactly what was sent and received.
- B) Assume it's a model problem up front and start rewriting the prompt from scratch, since a failing tool call is more often a sign of unclear instructions than of broken plumbing underneath it.
- C) Switch to a different model to see whether the failure persists under the new one.
- D) Restart the CI runner and simply try the same job again.

**Question 55.** The internal crash-reporting system needs to be reachable from Claude Code sessions across the whole mobile engineering org, not just one squad, and should be maintainable by the platform team independently of any consuming app.

Question: What is the best approach?

- A) Have each squad paste crash-reporting API credentials directly into their own CLAUDE.md.
- B) Hard-code the crash-reporting logic separately into each squad's own custom skill.
- C) Ask each engineer to curl the crash-reporting API by hand whenever it's needed.
- D) Build an MCP server exposing crash-reporting operations as tools, shared across the org.

**Question 56.** An MCP server for app-store metadata exposes both a `search_listings` tool and a way for agents to see what metadata categories exist without an exploratory search call.

Question: What is the second capability an example of?

- A) An MCP tool, functionally identical to `search_listings`, just returning a different schema of results.
- B) A built-in tool the platform provides automatically to every agent.
- C) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- D) A Claude Code Skill packaged alongside the MCP server.

**Question 57.** The team is deciding whether an internal build-status MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision?

- A) Where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services.
- B) stdio servers are always faster than network-hosted ones, regardless of deployment context, network topology, or how many clients are calling them concurrently.
- C) MCP only supports a single communication pattern, so there's no real decision to make either way.
- D) Remote servers structurally cannot expose tools, only resources.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a crash-reporting API token hardcoded directly in the file.

Question: What is the correct fix?

- A) Base64-encode the token in place before committing it, so it isn't stored as plain text.
- B) Move the token to environment-variable expansion (e.g., `${CRASH_API_TOKEN}`) so the secret isn't committed to version control.
- C) Move `.mcp.json` into a private repository instead of the current one.
- D) Keep the token where it is but rotate it weekly on a fixed schedule.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full crash-log deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles?

- A) Add logging and a periodic validation report covering every tool call, plus a monthly access-review meeting, so misuse can be reviewed after the fact without changing what the tools can actually do.
- B) Scope the exposed tools down to only the operations actual workflows require.
- C) Add a confirmation prompt before any deletion call goes through.
- D) Leave access as it is for now, since no misuse has actually been observed yet.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific release-notes workflow used by a single squad, versus a widely-reused build-status-checking capability needed by every agent across the org.

Question: How should each be built?

- A) Both as MCP servers, on the theory that MCP is the correct choice for any shared capability, since it standardizes the transport regardless of how many teams actually use a given one.
- B) Both as Skills, on the theory that Skills are always reusable across teams by default.
- C) The release-notes workflow as a Skill scoped to that squad; the shared build-status capability as an MCP server maintained centrally.
- D) Both as built-in tools, since built-in tools require the least amount of setup work.

---
# Answer Key

**Quick key:** 1-D, 2-B, 3-B, 4-D, 5-C, 6-C, 7-C, 8-B, 9-C, 10-A, 11-B, 12-C, 13-D, 14-A, 15-D, 16-D, 17-C, 18-C, 19-B, 20-C, 21-D, 22-A, 23-D, 24-A, 25-D, 26-D, 27-B, 28-B, 29-A, 30-D, 31-A, 32-A, 33-D, 34-B, 35-C, 36-D, 37-C, 38-B, 39-A, 40-B, 41-A, 42-D, 43-D, 44-A, 45-A, 46-C, 47-A, 48-A, 49-B, 50-B, 51-C, 52-C, 53-B, 54-A, 55-D, 56-C, 57-A, 58-B, 59-B, 60-C

---

**1. D** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed call cap (B) is a backstop, not a primary mechanism; tool errors (C) don't reliably indicate loop completion.

**2. B** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. A keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. B** — A financial policy needs deterministic enforcement via a hook that blocks the call outright, on top of whatever the system prompt already says. A, C, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. D** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and C are probabilistic.

**5. C** — Removing tools unrelated to the agent's core role directly reduces the candidate tool set it must reason over, improving selection reliability. A adds prompt overhead without removing the actual capability bloat. B and D don't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (B) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. C** — "Already at final hub" is a valid non-error outcome, not a failure — return success indicating no reroute is needed. A hides real signal. B invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, C, and D are false or unsupported claims about the technology.

**9. C** — A narrowly-scoped subagent with only the refund tool and explicit criteria minimizes accidental refunds while the main agent reasons about unrelated tools. A overgeneralizes; B and D are unsupported technical claims.

**10. A** — Delegating log exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis. B and C don't address the root accumulation problem; D removes needed capability.

**11. B** — A short handoff summary (what was tried, what was found, recommended action) lets a human act immediately. A forces reconstruction from a raw transcript despite being "structured" in format. C omits diagnostic context. D conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, B, and D are unsupported absolute claims.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not language, tool count, or runtime.

**14. A** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. B, C, and D misdiagnose the cause.

**15. D** — A per-order call-count hook is the only option that deterministically guarantees the limit; A, B, and C remain probabilistic prompt-level guidance.

**16. D** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at a reduced rate versus synchronous calls. B doesn't reduce per-token cost; A and C risk quality or truncate output without addressing the actual cost lever.

**17. C** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and D misidentify the actual limitation.

**18. C** — Streaming supports incremental rendering, reducing perceived latency for real-time chat UIs. A is the wrong API for this use case; B and D don't address perceived latency.

**19. B** — Only a shared prefix is cacheable; placing stable content first in the system prompt and variable content last maximizes cache hits, reducing both latency and cost. A, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance or lose data; A removes the field's value entirely.

**21. D** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and C all discard information or guess.

**22. A** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. B and C are recovery layers for a problem that can be eliminated; D swaps one fragile text format for another.

**23. D** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top. A, B, and C misdiagnose or abandon a working mechanism.

**24. A** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B and C don't address the actual data-quality bottleneck; D discards otherwise-processable documents.

**25. D** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**26. D** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. B** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, C, and D mishandle or misdescribe this.

**28. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-customer cost breakdown across vendors. A, C, and D all oversimplify in ways that produce an inaccurate model.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. D** — Resetting at natural task boundaries prevents unrelated tenant context from bleeding into new work. B doesn't address cross-contamination; C is unreliable prompt-level mitigation; A is an unrelated lever.

**31. A** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. B and D overspend by default; C ignores task fit.

**32. A** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. B, C, and D apply broad, costly fixes to a narrow problem.

**33. D** — Pinning a version and deliberately testing changes (prompt, temperature, and otherwise) before upgrading avoids unattributed behavior drift in production. A accepts avoidable risk; B and C are unhelpful overcorrections unrelated to the actual fix.

**34. B** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A repeats a failed approach; C and D don't reliably fix structural consistency.

**35. C** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa; padding `max_tokens` doesn't create space that input already consumed. A, B, and D misstate this relationship.

**36. D** — Stable instructions first (ideally cacheable, in the system prompt) and variable content after both improves consistency (clear role separation) and caching. A, B, and C misstate the effect of ordering.

**37. C** — Actual per-request token usage (input/output/cache) attributed per ticket gives an accurate cost picture; estimates from average length or unrelated proxies (A, B, D) don't.

**38. B** — LLM output is inherently non-deterministic even at fixed temperature; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. A** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source, rather than compensating with more `max_tokens`. B and C work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. B** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs, without requiring a bigger context window. A is costly and doesn't guarantee the effect disappears; C and D don't address the underlying attention pattern.

**41. A** — Verifying key claims against the source thread catches confident-but-wrong output that fluency alone would let through. B is the failure mode itself; C and D don't address correctness.

**42. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and B are workarounds for a problem that can be structurally eliminated; C doesn't address the preamble issue.

**43. D** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; B discards potentially useful context entirely.

**44. A** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. B and C are absolute claims that don't hold generally; D is false.

**45. A** — Versioning the prompt like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. C** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and D misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. B, C, and D are reactive or abandon the structured-output requirement.

**49. B** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A narrows scope but doesn't isolate output; C restricts capability, not output destination; D removes useful functionality.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. C** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; B frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and C re-check already-verified steps; D skips diagnosis entirely.

**54. A** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. B and C guess without diagnosis; D doesn't investigate the cause at all.

**55. D** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-app reuse and independent-maintenance requirement. A, B, and C all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action; it isn't just a relabeled tool with a different schema. A, B, and D mischaracterize this capability.

**57. A** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. B, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. B** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; C and D don't remove the exposed credential from history or ongoing risk.

**59. B** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and C are detective/compensating controls; D accepts unnecessary risk.

**60. C** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, B, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 7.*
