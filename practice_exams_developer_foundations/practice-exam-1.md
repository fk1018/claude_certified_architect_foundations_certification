# CCDVF Practice Exam 1

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer and multiple-response practice set — most items have one correct answer and three distractors; a few state how many responses to select. |
| Scenarios | 4 (DevOps Agent with the Claude Agent SDK, Document Intelligence API Pipeline, High-Volume Summarization Optimization, Claude Code + MCP for a Platform Team) |
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

## Scenario A: DevOps Agent with the Claude Agent SDK (Questions 1–15)

You are building an internal DevOps agent using the Claude Agent SDK. It has custom tools (`get_deploy_status`, `restart_service`, `read_logs`, `page_oncall`) and helps engineers diagnose and resolve production incidents. Some actions are destructive or expensive, so tool access and enforcement matter as much as reasoning quality.

---

**Question 1.** An engineer wants the agent's tool-use loop to keep executing tools and returning results until the model has no more tool calls to make. What should the loop key off?

- A) Scan the assistant's response text for phrases like "done," "resolved," or "no further action needed" and stop the loop once one appears.
- B) Enforce a fixed cap of ten tool calls per incident and end the loop unconditionally once that count is reached, regardless of `stop_reason`.
- C) The `stop_reason` field on each response: keep executing tools and returning results while it reads `"tool_use"`, and terminate the loop once it reads `"end_turn"`.
- D) Whether the most recently executed tool call returned an error, treating any error result as the signal that the loop should stop.

**Question 2.** After the agent calls `restart_service` and your code executes it, what must happen for the agent to correctly continue reasoning about the incident?

- A) Append a `tool_result` block referencing the matching `tool_use` ID, then send the updated conversation back to the model.
- B) Store the restart confirmation in your incident database only, without returning any result to the model or the ongoing conversation.
- C) Inject the restart result into the system prompt so it persists as background context for the rest of the conversation instead of a turn-level result.
- D) Start a brand-new session that summarizes the restart in a fresh system prompt, and continue the entire incident investigation from there instead.

**Question 3.** Company policy requires human approval before `restart_service` is called on any payment-processing host. The system prompt states this clearly, but logs show occasional autonomous restarts on payment hosts. What is the most reliable fix?

- A) Repeat the approval rule at both the start and the end of the system prompt, hoping the redundant framing raises adherence to the stated policy.
- B) Add several few-shot examples showing the agent correctly escalating payment-host restarts for human approval before calling the tool.
- C) Implement a hook that intercepts every `restart_service` call and deterministically blocks any call targeting a payment-processing host without prior human approval.
- D) Lower the model's temperature so it more consistently follows the stated policy, on the theory that less-random sampling means fewer missed rules.

**Question 4.** The team wants the agent to always call a `classify_severity` tool first, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State clearly in the system prompt that `classify_severity` must always run before any other tool, and rely on the model to follow that instruction on every incident.
- B) Set `tool_choice: "any"` on the first request so the model is guaranteed to call some tool, without pinning which one that call must be.
- C) Set `tool_choice: {"type": "tool", "name": "classify_severity"}` on the first request to force that specific tool, then revert to normal tool choice for subsequent turns.
- D) Add several few-shot examples in the prompt demonstrating `classify_severity` being called first, before any other tool, on past incidents.

**Question 5. (Select TWO responses.)** The agent currently has 16 tools, including several rarely-used ones (billing lookup, customer notification, feature-flag toggles) unrelated to incident response. Tool selection has become unreliable.

Question: Which two changes best address this?

- A) Remove or scope out the tools unrelated to the agent's core incident-response role, such as billing lookup and customer notification, from its tool list entirely.
- B) Split the unrelated responsibilities — billing, notifications, feature flags — into separate, specialized agents, each with its own narrow tool set.
- C) Keep all sixteen tools available but add a system prompt note listing which ones are "primary" for incident response, hoping the model weighs them accordingly.
- D) Increase `max_tokens` so the agent has more room in its response to reason through which of the sixteen tools is the right one to pick.

**Question 6.** `read_logs` currently returns the string `"Error"` for every possible failure — invalid host, permission denied, or log service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every `read_logs` call in an automatic retry policy that re-issues the request a fixed number of times whenever the string `"Error"` comes back.
- B) Delegate failure-type classification to a separate subagent whose only job is to infer which of the three failure types occurred from context clues.
- C) Return structured error metadata from the tool itself: an error category, a retryable flag, and a human-readable description of what actually failed.
- D) Increase the log service's timeout so slow queries fail less often, on the assumption that most of the current `"Error"` responses are really timeouts.

**Question 7.** When `read_logs` finds no matching log lines for a query, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Return a successful response containing an empty result set for a query with no matches, reserving actual error responses for genuine access failures.
- B) Add a hook that intercepts the "no logs matched" case, suppresses the error entirely, and ends the conversation without informing the agent.
- C) Have the agent call `get_deploy_status` first on every query to check whether logs should exist before it ever calls `read_logs` at all.
- D) Add a system prompt note explaining to the model that this particular error usually just means no logs matched the query, not a real failure.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `get_deploy_status`, then `read_logs`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for incident response? (Select ONE response.)

- A) Model-driven selection is always cheaper than a fixed sequence, since letting the model choose skips the reasoning tokens a rigid script would otherwise spend.
- B) The Claude Agent SDK is technically incapable of executing a fixed, hard-coded sequence of tool calls like "always `get_deploy_status` then `read_logs`."
- C) Incidents are high-ambiguity: the right tools and their order vary case by case and depend on intermediate findings, which a fixed sequence can't adapt to.
- D) A fixed, hard-coded sequence of tool calls cannot invoke custom tools like `get_deploy_status`; it can only invoke Anthropic's built-in tools.

**Question 9.** The team wants to add a `page_oncall` capability but is deciding whether to give the main incident agent that tool directly or delegate paging decisions to a separate, narrowly-scoped subagent. Paging has real cost (waking someone up) and should only happen under specific escalation criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) Subagents are required by the SDK any time a tool call has a real-world side effect like restarting a service or paging a human being.
- B) The main incident agent's context window is too small to hold the paging tool's schema alongside its existing tool definitions and conversation history.
- C) A narrowly-scoped subagent given only the paging tool and explicit criteria reduces the chance of unnecessary paging while the main agent reasons about unrelated tools.
- D) A subagent that owns the paging tool executes its calls faster than the same tool called directly from the main incident agent's own tool loop.

**Question 10.** During a long-running incident, the agent's context fills with verbose raw log output, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` on each response so the agent has more room to write out its reasoning about the accumulated raw log output.
- B) Read only the first 50 lines of every log query result, on the assumption that the root cause is always near the top of the output.
- C) Delegate log exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on diagnosis.
- D) Disable `read_logs` entirely for the remainder of the incident and rely on `get_deploy_status` alone to diagnose the root cause.

**Question 11.** The agent successfully restarts a service, but the human on-call engineer later has no visibility into what the agent tried before escalating — logs show 20 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include? (Select ONE response.)

- A) The full raw transcript of every tool call and result from the past 20 minutes, so the human can reconstruct the investigation line by line.
- B) Just the final error message from the last failed tool call, since the human on-call engineer can re-investigate everything else from there.
- C) A structured handoff summary covering what was tried, what was found, and a recommended next action, so the human can act immediately.
- D) A sentiment analysis of how urgent the conversation seemed, based on the tone and word choice across the agent's tool-use turns.

**Question 12.** The team is deciding between letting engineers run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Operational control on the self-hosted side versus operational burden on the managed side — there's no capability difference in what tools the agent can actually call.
- B) Self-hosted agents running on the team's own infrastructure cannot register or invoke custom tools like `restart_service` or `page_oncall`.
- C) Managed, Anthropic-hosted execution environments are always less secure than a self-hosted harness, regardless of how either is configured.
- D) Managed execution environments can never reach private infrastructure at all, making custom tools like `read_logs` impossible to wire up.

**Question 13.** An engineer asks whether the incident-response task should be built as a fixed workflow or an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task involves more than three tools, since workflows above that count are assumed to need full agentic tool-choice reasoning.
- B) Whether the team prefers to implement the harness in Python or TypeScript, since each language favors a different execution pattern.
- C) Whether the task is well-defined and repeatable versus high-ambiguity, with a path that depends on intermediate findings the workflow can't predict up front.
- D) Whether the task needs to complete in under 30 seconds, since fixed workflows are assumed to always run faster than an agent's reasoning loop.

**Question 14.** The agent's `AgentDefinition` for a proposed "log-analysis subagent" has a vague description: "Helps with logs." The main agent rarely delegates to it even when log analysis is clearly needed.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent needs more tools; add several more log-related tools to its `AgentDefinition` so it has more capability to draw on.
- B) Subagents cannot actually be delegated to by the main agent unless they are explicitly registered as MCP servers in `.mcp.json`.
- C) The main agent's temperature is set too low to consider delegating to a subagent instead of just handling log analysis inline itself.
- D) The subagent's description drives delegation choices; rewriting it to state specifically what it does and when to use it will fix the under-delegation.

**Question 15.** The team wants a hard guarantee that `restart_service` is never called more than twice for the same host within one incident, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the two-restart-per-host limit clearly and asking the model to track its own call count across the incident.
- B) A note in the `restart_service` tool's description mentioning the two-call limit, so the model sees it every time it considers calling the tool.
- C) Few-shot examples in the prompt showing a prior agent correctly stopping after two restarts on the same host during a similar incident.
- D) A hook that tracks per-host call counts across the conversation and deterministically blocks the tool call once the two-restart limit is reached.
---

## Scenario B: Document Intelligence API Pipeline (Questions 16–30)

You are integrating Claude into a document-intelligence pipeline that extracts structured data from contracts, invoices, and reports. The pipeline processes both interactive single-document requests (a user uploads one file and waits) and large overnight batch jobs (tens of thousands of documents).

---

**Question 16.** The overnight batch job processes 40,000 invoices with no user waiting on the result. No step needs the model to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API with a smaller, faster model swapped in, since a lighter model reduces cost even at high volume.
- B) The synchronous Messages API run in parallel across many worker threads, so all 40,000 invoices finish processing as fast as possible.
- C) The Message Batches API — a fit for latency-tolerant, non-blocking, high-volume work like this, processed at meaningfully reduced cost.
- D) The synchronous Messages API with `max_tokens` reduced to the bare minimum needed, to shrink per-request cost across all 40,000 invoices.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry failed fields" loop to the batch pipeline to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts, so the extraction instructions and schema reference the loop depends on can't be sent at all.
- B) The Batch API's 24-hour completion window makes any kind of retry logic across the whole batch structurally impossible to schedule.
- C) The Batch API's context window is too small to hold contract-length documents alongside the extraction instructions and schema reference.
- D) The Batch API cannot execute a validation tool call mid-request and feed the result back to the model within a single request, which this loop requires.

**Question 18.** The interactive single-document flow shows users a real-time progress indicator while Claude processes their upload.

Question: What technique best supports this user experience? (Select ONE response.)

- A) Streaming, so the UI can render extracted fields incrementally as they arrive and reduce the user's perceived latency while waiting.
- B) The Batch API, since it's specifically designed to give a user real-time, incremental feedback while a single document is processed.
- C) Increasing `max_tokens` on the request, so the full extraction response is generated and arrives at the client faster.
- D) Polling the Batch API's status endpoint every second for the single document, translating each poll into a progress-bar tick.

**Question 19.** Every request sends the same 6,000-token extraction instructions and field-schema reference, followed by the specific document text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Move the 6,000-token schema reference into a few-shot example block instead, since examples are treated differently by the cache than instructions.
- B) Switch every request to the smallest available model regardless of extraction quality, accepting worse field accuracy for a flat cost reduction.
- C) Truncate the schema reference to a shorter form to save input tokens, accepting that some rarely-used fields may be extracted less reliably.
- D) Place the stable extraction instructions and schema reference first, enable prompt caching on that prefix, and put the varying document text last.

**Question 20.** The extraction schema currently requires a `discount_amount` field on every invoice. Many invoices have no discount, and the model has started inventing small values rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the `discount_amount` field from the schema entirely, so the model is never asked about discounts on any invoice at all.
- B) Add a prompt instruction telling the model not to invent a discount value when none is actually present on the invoice.
- C) Make `discount_amount` nullable in the schema so its genuine absence can be reported truthfully instead of forcing a fabricated number.
- D) Lower the temperature on extraction requests to reduce the rate at which the model invents small discount values.

**Question 21.** Two credible extraction passes on the same invoice disagree: one reads the total as $4,200.00 and another as $4,200.05, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do? (Select ONE response.)

- A) Average the two candidate values ($4,200.00 and $4,200.05) and record the midpoint as the resolved total.
- B) Discard the invoice entirely from the pipeline, treating the disagreement between passes as evidence the whole document is unreliable.
- C) Always trust the first extraction pass by convention, treating any later disagreeing pass as noise to be ignored.
- D) Flag the `total` field for human review with both candidate values and their source pass, rather than silently picking one over the other.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 3% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Wrap every JSON parse in a try/catch, and on failure retry the whole request with "valid JSON only" appended to the extraction prompt.
- B) Add a JSON-repair library to the downstream loader that fixes common syntax issues — missing commas, unquoted keys — before parsing.
- C) Ask the model for YAML output instead of JSON on every single request, since YAML is generally far more forgiving of minor formatting drift issues.
- D) Define a `submit_extraction` tool whose input schema matches the extraction structure, and read data from the `tool_use` block directly.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some extracted line-item amounts don't sum to the stated invoice total.

Question: What should you conclude and do? (Select ONE response.)

- A) Strict schemas eliminate syntax errors, not semantic errors — add a validation step checking line-item sums against the stated total.
- B) The schema needs stricter numeric types on the amount fields, such as constraining them to two decimal places, to fix the mismatched sums.
- C) `max_tokens` is set too low on these requests, truncating the line-item array mid-generation before every item has been listed.
- D) Abandon schema-constrained tool use and return to free-text extraction with mandatory human review of every invoice's totals.

**Question 24.** A subset of incoming invoices are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject scanned invoices with no text layer from the pipeline entirely, routing them to a separate manual-entry process outside Claude.
- B) Increase `max_tokens` on the extraction request so the model has more room to work harder at interpreting the degraded OCR text.
- C) Switch to a larger, higher-capability model, assuming bigger models are always better at reading noisy OCR text without ever needing vision-based image input.
- D) Send the invoice image itself as a content block alongside the extraction instructions, using native vision input instead of the OCR text.

**Question 25.** The pipeline needs to run extraction on five sections of a long report concurrently to keep latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Streaming responses for each section, since streaming is the only mechanism that supports more than one request being processed at a time.
- B) The Batch API for the five sections, since it's the only way in the Messages ecosystem to run more than one request concurrently.
- C) A single request with all five sections concatenated into one prompt, since Claude parallelizes its internal reasoning across sections automatically.
- D) Async/concurrent request handling in the integration layer, so multiple API calls for the five sections can be in flight at once without blocking on each other.

**Question 26.** The company plans to run the same extraction pipeline through both the direct Anthropic API and Amazon Bedrock for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) Extraction accuracy and latency are guaranteed to be identical down to the millisecond between the direct API and Bedrock for the same model.
- B) Bedrock requires a completely different prompting approach and a redesigned extraction schema, since its request format is fundamentally incompatible.
- C) Batch processing for high-volume extraction is unavailable on all third-party vendor integrations, including Bedrock, regardless of region.
- D) The Messages API contract stays conceptually the same across vendors, though authentication, plumbing, and feature-rollout timing can differ.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Ignore the thinking content block entirely when assembling each turn, since extended thinking never affects how later tool-use turns should be built.
- B) Handle the thinking content block as distinct from the final answer text, typically preserving it across the multi-turn tool-use conversation.
- C) Convert the model's thinking output into a separate synthetic tool call so the downstream validation step can inspect that reasoning directly instead.
- D) Discard the thinking content block specifically in turns where a tool call is also present, but keep it in turns with plain text only.

**Question 28.** Finance asks for an accurate per-document cost breakdown for the extraction pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, assuming prompt caching alone is now the single dominant cost driver for this pipeline's entire per-document spend.
- B) Only output tokens, on the assumption that input tokens are effectively free compared to what the model generates in response.
- C) A flat per-document fee applied uniformly regardless of how many tokens any individual document's extraction actually consumes.
- D) Input, output, and cache read/write tokens tracked separately, since Anthropic prices each of these categories differently.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the extraction pipeline's application code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Review should be skipped for any code that calls an external API, since API-calling code is inherently simpler than logic that makes decisions.
- B) Code review is unnecessary once the pipeline's evals pass, since passing evals alone is sufficient proof the whole surrounding system behaves correctly.
- C) Only the prompt itself needs review; the surrounding application code that calls it is low-risk by definition and can be merged unreviewed.
- D) Standard SDLC practices — code review, testing, version control — still apply to the code around Claude; an LLM doesn't replace engineering discipline.

**Question 30.** A single long-running session is used across an entire day to process unrelated document batches from different clients, and the team notices Claude increasingly referencing details from unrelated earlier documents.

Question: What is the best fix? (Select ONE response.)

- A) Reduce the temperature on extraction requests, on the assumption that lower randomness will stop the model from cross-referencing unrelated documents.
- B) Increase the context window in use so more accumulated history from the day's batches fits without the model appearing to confuse clients.
- C) Ask the model to "ignore all earlier documents" in a prompt instruction at the start of each new client's batch, then continue in the same session.
- D) Start a fresh session (or `/compact`) at natural task boundaries, such as between different clients' batches, rather than accumulating unrelated context in one long session.
---

## Scenario C: Optimizing a High-Volume Support Summarization Service (Questions 31–45)

You run a service that summarizes support tickets for internal dashboards, processing hundreds of thousands of tickets per day. Cost, latency, and consistency all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the summarization task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) The highest-capability model tier available across the board, to guarantee top-tier summary quality on every single ticket regardless of complexity.
- B) A fast, low-latency tier suited to high-volume, low-complexity tasks, reserving a higher-capability tier only for tickets flagged as complex.
- C) Whichever tier happens to be cheapest per token at the moment, chosen without regard to whether it actually fits this summarization task.
- D) The same high-capability tier the company uses for its hardest reasoning tasks elsewhere, applied here purely for consistency across teams.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a complex multi-product billing dispute) where the fast default model produces shallow summaries.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt for every ticket, hoping the extra examples teach it to reason through complex billing disputes too.
- B) Switch every ticket, complex or not, to the highest-capability tier to be safe, accepting the added cost and latency across the whole volume.
- C) Increase `max_tokens` for all tickets uniformly, on the assumption that the fast model just needs more room to write a much deeper, more thorough summary.
- D) Route only the flagged complex tickets to a higher-capability tier or one with extended thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, summary tone and structure shifted noticeably without any code change.

Question: What should the team do differently? (Select ONE response.)

- A) Pin a specific model version in production and deliberately test any upgrade before rolling it out, rather than floating to whatever is latest.
- B) Nothing — behavior drift in tone and structure across routine model releases is fully expected and requires no additional process to manage.
- C) Roll back to the oldest available model version permanently, since older, more established versions are inherently more stable in tone.
- D) Disable all prompt caching in production entirely to prevent drift, on the assumption that cached prefixes are what's actually causing tone to shift after releases.

**Question 34.** Summaries need a consistent structure (issue, root cause, resolution, follow-up) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Provide two to three few-shot examples in the prompt that demonstrate the exact desired structure — issue, root cause, resolution, follow-up — directly.
- B) Write an even longer, more detailed prose description of the four-part structure, adding further qualifiers to each section's expectations.
- C) Lower the temperature to zero across all summarization requests, on the assumption that less sampling randomness will produce more consistent structure.
- D) Ask the model to restate the four-part structure back in its own words immediately before it writes the actual ticket summary each time.

**Question 35.** A ticket thread is very long (50+ messages). The team wants a maximally detailed summary and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input tokens and output tokens are budgeted from two completely independent pools, so a long 50-message thread costs the output nothing.
- B) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- C) Output length has no effect on latency at all, so requesting a maximally detailed summary costs nothing extra in response time.
- D) Long outputs are always truncated regardless of context window size, so requesting more detail than a fixed cap allows is pointless either way.

**Question 36.** The summarization prompt currently places the specific ticket text before the general summarization instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Stable instructions belong in the system prompt or first in the prompt, forming a cacheable prefix; ticket text should come after as the varying part.
- B) Order has no effect on either output consistency or cache hit rate, so moving the ticket text earlier or later changes nothing measurable.
- C) Placing the summarization instructions last, right before generation begins, always improves the model's attention to them regardless of prompt caching.
- D) Reordering the prompt only affects cost through cache hits, and never touches the consistency of the summary's structure across different tickets at all.

**Question 37.** Finance wants to know exactly how much the summarization service costs per ticket, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead? (Select ONE response.)

- A) Actual token usage per request — input, output, and cache — attributed per ticket, rather than an estimate derived from average prompt length.
- B) Wall-clock latency per ticket, used as a cost proxy on the assumption that slower requests reliably cost more in tokens than faster ones.
- C) The number of API calls made per ticket only, regardless of how many tokens each of those calls actually consumed.
- D) A flat cost assumption derived from each ticket's raw character count, applied uniformly without reference to actual token usage.

**Question 38.** An engineer writes an automated eval that asserts the summarization output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the summaries look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model is broken and producing genuinely wrong answers on this sample ticket, which is why the assertion against the fixed reference string fails.
- B) LLM output is non-deterministic across calls; exact-match evals are the wrong tool here — they should tolerate reasonable variation.
- C) The eval needs a much longer, more deterministic reference string that captures every single possible acceptable phrasing the model might ever produce.
- D) Temperature should be increased on the summarization requests to fix the intermittent failures the exact-match eval keeps reporting.

**Question 39.** Ticket threads include full raw metadata dumps (every field of every message) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Prune the raw metadata dumps to just the relevant fields before they enter the prompt, rather than passing every field through.
- B) Increase `max_tokens` on the summarization request to accommodate the extra metadata volume that's now bloating every single ticket's prompt considerably.
- C) Switch to a model with a larger context window so the metadata bloat matters less relative to the total space available per request.
- D) Summarize the raw metadata with a second, separate Claude call before feeding that summary into the main ticket-summarization call.

**Question 40.** For very long ticket threads, the team notices summaries consistently miss details from the middle of the conversation while capturing the opening and closing messages well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Switch to a model with an even larger context window, on the assumption that sheer extra headroom alone will fix uneven attention across the whole thread.
- B) Put a key-facts summary at the start and organize detail under clear headers, countering the tendency to favor the thread's beginning and end.
- C) Add a prompt instruction telling the model to "pay equal attention to the whole conversation" regardless of message position.
- D) Alphabetize the fifty-plus messages by sender name before summarizing, so no single position in the thread is inherently favored.

**Question 41.** A summary confidently states a resolution that, on manual review, never actually happened in the ticket thread.

Question: What practice would most help catch this class of error before it reaches the dashboard? (Select ONE response.)

- A) Trust confident, fluent-sounding output as sufficient evidence of correctness by default, since well-phrased summaries rarely misstate what happened.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims against the source thread rather than accepting fluency as correctness.
- C) Increase the model's temperature so its answers sound less confident, on the theory that hedged language would have flagged this fabricated resolution.
- D) Shorten the summary so there's simply less room in the output for a fabricated claim like an incorrect resolution to appear.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the "always output valid structured JSON" instruction even more emphatically, in multiple places throughout the prompt.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip any free text that appears before the first `{`, treating the preamble as noise to be discarded.
- D) Increase `max_tokens` so there's guaranteed room for both the free-text preamble and the full structured JSON payload.

**Question 43.** The team wants to add an exploratory step that scans a customer's full ticket history for context before summarizing the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Have a subagent perform the historical scan in an isolated context and return only a distilled summary to the main summarization step.
- B) Load the customer's entire ticket history directly into the main summarization prompt every time, alongside the current ticket's own content.
- C) Skip historical context entirely for every ticket to avoid the bloat risk, even in cases where past tickets would clearly change the resulting summary.
- D) Increase the context window in use so the customer's full ticket history always fits directly alongside the current ticket being summarized.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot prompting is always strictly better than zero-shot, regardless of how simple, common, or high-volume the underlying task actually happens to be.
- B) For a simple, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its cost on formatting or edge-case needs.
- C) Zero-shot prompting is required whenever latency matters at all, since including any examples always adds meaningful response time.
- D) The choice between zero-shot and multi-shot has no measurable effect on either cost or latency for a high-volume task like this one.

**Question 45.** The summarization prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt file's structured format entirely so no engineer can ever change it again, regardless of future task or quality requirements.
- C) Only allowing one designated engineer to ever read or touch the prompt, restricting all future changes to that single person.
- D) Rewriting the prompt from scratch every quarter on a fixed schedule, regardless of whether anything about the task has changed.

---

## Scenario D: Claude Code and MCP for an Internal Developer Platform Team (Questions 46–60)

You support a 50-engineer team's use of Claude Code and a set of internal MCP servers (ticketing, deployment status, internal docs). You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the team's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- B) The new engineer simply needs to run `/memory` after cloning to activate the project's memory files before conventions will apply.
- C) `CLAUDE.md` requires an explicit `@import` directive from the project root before its contents take effect for any engineer at all.
- D) The team's conventions file apparently exceeded an internal size limit and was silently truncated the moment the new engineer's client loaded it.

**Question 47.** A nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The pull requests being reviewed are too large for Claude Code to fully process within a single nightly CI run's time budget.
- C) The CI runner is missing the environment variable holding its Claude API credentials, and silently retries the handshake until it times out.
- D) The repository's `CLAUDE.md` file is malformed, causing Claude Code to loop while repeatedly attempting to parse its contents.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- B) Harden the regex with more permissive fallback patterns that tolerate the formatting drift between runs.
- C) Post the entire raw review output as a single PR comment instead of trying to parse individual findings out of it.
- D) Add a stronger prompt instruction telling Claude never to deviate from the expected comment format, however it renders it.

**Question 49.** The team's `/audit-deps` custom command prints thousands of lines of dependency-graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- B) `allowed-tools`, restricting the command to read-only operations so it can't modify the dependency graph it's reporting on.
- C) `argument-hint`, so developers scope the analysis more narrowly before the thousands of lines of output are generated.
- D) Removing the `/audit-deps` command entirely, since no configuration change can prevent it from polluting context.

**Question 50.** An internal `/scaffold-service` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Add a warning in the skill's instructions telling Claude never to run shell commands during scaffolding.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation, making Bash structurally unavailable.
- C) Require developers to commit their work before running any skill, so unintended shell changes are easy to revert.
- D) Convert the skill into a slash command instead, since slash commands are structurally incapable of running any tools at all.

**Question 51.** An engineer needs to understand how authentication flows across a large, unfamiliar codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Use the Explore subagent for discovery, so exploration happens in an isolated context and only a summary returns.
- B) Read every single file in the codebase in one long pass to be thorough, regardless of how much context that ends up consuming.
- C) Skip exploration entirely and infer the authentication architecture from directory and file names alone.
- D) Split the discovery and implementation work across two separate terminal windows running independent sessions.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session entirely and rely on memory of what was already learned during the earlier discovery phase.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving the key findings already gathered.
- C) Delete the project `CLAUDE.md` temporarily to free up context space, instead of forking the discovery into a separate sub-agent context.
- D) Continue working as-is; Claude automatically discards irrelevant context once the window nears its limit.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal MCP tool, and writes a report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Re-read the config file again, since that's the earliest step in the pipeline and the most likely place for a subtle mistake.
- B) The step between receiving the MCP tool's data and producing the final report, since that's most likely where the divergence occurred.
- C) The network connection to the MCP server, since that's typically considered the most complex and failure-prone step in the whole pipeline.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run until it produces a different result.

**Question 54.** A deployment tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Assume from the start that it's a model problem and rewrite the prompt before looking at any trace or log data.
- B) Isolate whether the failure is in the integration layer (the API call and response) versus the model's output, via the trace.
- C) Switch to a completely different model entirely to see whether the same deployment failure persists under it.
- D) Restart the CI runner and try the deployment again, without changing anything else about the integration.

**Question 55.** The internal ticketing system needs to be reachable from Claude Code sessions across the whole engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Build an MCP server exposing ticketing operations as tools, hosted and maintained centrally, shared across the whole org.
- B) Have each team paste their own copy of ticketing API credentials into their own project's `CLAUDE.md` file.
- C) Hard-code ticketing logic into each team's custom skill as a stdio integration, duplicating it per team instead of centralizing.
- D) Ask each engineer to curl the ticketing API manually from the terminal whenever they need ticket data.

**Question 56.** An MCP server for internal documentation exposes both a `search_docs` tool and a way for agents to see what documentation exists without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP tool, functionally identical to `search_docs` and interchangeable with it in every workflow.
- B) An MCP resource — content and catalog visibility distinct from a tool, which performs an action instead.
- C) A built-in tool provided automatically by the Claude Code platform, requiring no server-side configuration.
- D) A Claude Code Skill, packaged and distributed together alongside the documentation MCP server itself, for convenience.

**Question 57.** The team is deciding whether an internal MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) Where the server runs relative to the client and who needs access — stdio per-machine, remote for shared services.
- B) stdio servers are always faster than remote servers, regardless of how many clients need to reach them.
- C) MCP only supports one communication pattern, so there's no real deployment decision for the team to make.
- D) Remote, network-hosted MCP servers reportedly cannot expose tools at all, only read-only resources for clients to browse through.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret is never committed to version control.
- B) Base64-encode the token before committing it, since encoding prevents the value from being read directly.
- C) Move `.mcp.json` to a private repository instead, treating privacy as protection while leaving the token hardcoded inside the file.
- D) Rotate the ticketing token on a weekly schedule instead of ever removing it from the committed file.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Add logging around the deletion tools so any future misuse can be reviewed carefully after the fact.
- B) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities.
- C) Add a confirmation prompt before any deletion call executes, without changing what the tool is actually permitted to do.
- D) Leave access as-is for now, since no misuse of the broad deletion rights has been observed yet.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific reporting workflow used by a single small team, versus a widely-reused authentication-checking capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) Both as MCP servers exposing each capability as either a tool or a resource, since MCP is the correct architectural choice for any capability, one-off or widely shared.
- B) The one-off reporting workflow as a Skill or custom tool scoped to that team; the widely-reused authentication capability as an MCP server maintained centrally for all consuming agents.
- C) Both of these should be built as Skills, since Skills are assumed to always be equally reusable regardless of how narrow or broad their intended audience actually is.
- D) Both as built-in tools, since built-in tools require the least setup for any team building on top of them, much like running Claude Code in headless mode requires no additional interactive setup.

---
# Answer Key — Practice Exam 1

**Quick key:** 1-C, 2-A, 3-C, 4-C, 5-A+B, 6-C, 7-A, 8-C, 9-C, 10-C, 11-C, 12-A, 13-C, 14-D, 15-D, 16-C, 17-D, 18-A, 19-D, 20-C, 21-D, 22-D, 23-A, 24-D, 25-D, 26-D, 27-B, 28-D, 29-D, 30-D, 31-B, 32-D, 33-A, 34-A, 35-B, 36-A, 37-A, 38-B, 39-A, 40-B, 41-B, 42-B, 43-A, 44-B, 45-A, 46-A, 47-A, 48-A, 49-A, 50-B, 51-A, 52-B, 53-B, 54-B, 55-A, 56-B, 57-A, 58-A, 59-B, 60-B

---

**1. C** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a hard cap (B) is a backstop, not the primary mechanism, and ignores `stop_reason` entirely; tool errors (D) don't indicate loop completion.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. Storing the confirmation only in a database (B) never returns it to the model; injecting it into the system prompt (C) misuses turn-level data as persistent context; starting a new session (D) discards conversational state unnecessarily.

**3. C** — A financial/safety-critical rule needs deterministic enforcement via a hook that blocks the call outright. Repeating the rule (A), few-shot examples (B), and lowering temperature (D) all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns revert to normal tool choice. `tool_choice: "any"` (B) guarantees some tool call, but not which one. Prose instructions (A) and few-shot examples (D) are probabilistic.

**5. A, B** — Removing unrelated tools and/or splitting responsibilities into specialized agents both directly reduce the candidate tool set an agent must reason over, improving selection reliability. A "primary tools" note (C) adds prompt overhead without removing the actual capability bloat. More `max_tokens` (D) doesn't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Delegating the guesswork to a subagent (B) still leaves the tool reporting an undifferentiated `"Error"` string — it just moves the inference problem, it doesn't fix the missing information. Reducing timeout frequency (D) doesn't fix the other two failure types.

**7. A** — "No matching logs" is a valid empty result, not a failure — return success with an empty set. A hook that suppresses the error and ends the conversation (B) hides real signal from the agent entirely. Calling `get_deploy_status` first (C) invents an unnecessary extra step. A system prompt note (D) patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. Cost claims (A), and false capability claims about the SDK or fixed sequences (B, D), don't hold up.

**9. C** — A narrowly-scoped subagent with only the paging tool and explicit criteria minimizes accidental paging while the main agent reasons about unrelated tools. A (an absolute requirement) overgeneralizes; B and D are unsupported technical claims about context size and execution speed.

**10. C** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis. More `max_tokens` (A) and truncating to the first 50 lines (B) don't address the root accumulation problem; disabling log reading (D) removes needed capability.

**11. C** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. The raw 20-minute transcript (A) forces reconstruction from scratch. Just the final error (B) omits diagnostic context. Sentiment analysis (D) conveys mood, not facts.

**12. A** — The real tradeoff is operational control on the self-hosted side versus operational burden on the managed side; which tools the agent can call doesn't differ between the two deployment models. B and D are false capability claims — both deployment models can register and reach custom tools like `restart_service` or private infrastructure. C overreaches into an absolute security claim ("always less secure") that isn't true either way: security depends on how each option is configured and operated, not on which one is chosen.

**13. C** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime speed.

**14. D** — Tool/subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. Adding more tools (A), a false registration requirement (B), and temperature (C) all misdiagnose the cause.

**15. D** — A per-host call-count hook is the only option that deterministically guarantees the limit; a system prompt instruction (A), a tool-description note (B), and few-shot examples (C) all remain probabilistic prompt-level guidance the model could still violate.

**16. C** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. A smaller model (A) and minimal `max_tokens` (D) risk quality without addressing the actual cost lever; brute-force parallel threads (B) don't reduce per-token cost at all.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. Missing system prompt support (A), the 24-hour window (B), and context window size (C) all misidentify the actual limitation.

**18. A** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. The Batch API (B) is the wrong tool for single-document, real-time feedback; more `max_tokens` (C) and polling a batch status endpoint (D) don't address perceived latency the way incremental rendering does.

**19. D** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. Moving the schema into a few-shot block (A), swapping models (B), and truncating the schema (C) either break the cacheable prefix or degrade quality without addressing caching.

**20. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. A prompt instruction (B) and lower temperature (D) rely on probabilistic compliance; removing the field (A) loses the ability to report a discount at all when one does exist.

**21. D** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. Averaging (A), discarding (B), and blindly trusting the first pass (C) all discard information or guess.

**22. D** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. Try/catch-and-retry (A) and a repair library (B) are recovery layers for a problem that can be eliminated; switching to YAML (C) swaps one fragile text format for another.

**23. A** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top. Stricter numeric types (B), a `max_tokens` theory (C), and abandoning tool use (D) misdiagnose or abandon a working mechanism.

**24. D** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. A bigger model without vision input (C) and more `max_tokens` (B) don't address the actual data-quality bottleneck; rejecting the documents (A) discards otherwise-processable invoices.

**25. D** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. Streaming (A), the Batch API (B), and a single concatenated request (C) misstate how concurrency is actually achieved.

**26. D** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency (A), an incompatible request format (B), or unavailable batch processing (C).

**27. B** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. Ignoring it (A), converting it into a synthetic tool call (C), and selectively discarding it (D) all mishandle or misdescribe this.

**28. D** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-document cost breakdown. Cache-only (A), output-only (B), and a flat fee (C) all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system. A, B, and C all rationalize skipping review for code that still needs it.

**30. D** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. Lower temperature (A) doesn't address cross-contamination; a bigger context window (B) makes the accumulation worse, not better; a prompt instruction to "ignore earlier documents" (C) is unreliable prompt-level mitigation.

**31. B** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. The highest tier by default (A) and matching a company-wide "hardest task" tier (D) overspend by default; picking by price alone (C) ignores task fit.

**32. D** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. More few-shot examples (A), switching everything to the top tier (B), and more `max_tokens` (C) apply broad, costly, or ineffective fixes to a narrow problem.

**33. A** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. Accepting drift as normal (B), permanently rolling back to the oldest version (C), and disabling caching (D) are unhelpful overcorrections unrelated to the actual fix.

**34. A** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A longer prose description (B) repeats a failed approach; zero temperature (C) and asking the model to restate the structure first (D) don't reliably fix structural consistency.

**35. B** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. A, C, and D all misstate this relationship.

**36. A** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. B, C, and D misstate the effect of ordering on consistency or caching.

**37. A** — Actual per-request token usage (input/output/cache) attributed per ticket gives an accurate cost picture; latency as a proxy (B), call counts alone (C), and character counts (D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. Blaming the model (A) and asking for a longer reference string (C) misdiagnose the cause; raising temperature (D) makes the underlying non-determinism worse, not better.

**39. A** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. More `max_tokens` (B) and a bigger context window (C) work around the symptom without reducing waste; a second summarization call (D) adds cost and complexity for a problem solvable by simple filtering.

**40. B** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A bigger context window alone (A) doesn't guarantee the effect disappears; a "pay equal attention" instruction (C) and alphabetizing messages (D) don't address the underlying attention pattern.

**41. B** — Verifying key claims against the source thread catches confident-but-wrong output that fluency alone would let through. Trusting fluent output by default (A) is the failure mode itself; raising temperature (C) and shortening the summary (D) don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. Repeating the instruction (A) and stripping preambles after the fact (C) are workarounds for a problem that can be structurally eliminated; more `max_tokens` (D) doesn't address the preamble issue at all.

**43. A** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. Loading the full history directly (B) and a bigger context window (D) reintroduce the bloat risk; skipping history entirely (C) discards potentially useful context.

**44. B** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. "Multi-shot always wins" (A) and "zero-shot whenever latency matters" (C) are absolute claims that don't hold generally; D is false — the choice does affect cost and latency.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. Locking the prompt (B), restricting access to one person (C), and scheduled full rewrites (D) are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. A** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A `/memory` step (B), a required `@import` (C), and a silent size-limit truncation (D) misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. Oversized PRs (B), a missing credential (C), and a malformed CLAUDE.md (D) would typically produce different, more specific failure signatures rather than an indefinite hang.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. Hardening the regex (B), posting raw output (C), and a stronger prompt instruction (D) are reactive or abandon the structured-comment requirement.

**49. A** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. `allowed-tools` (B) restricts capability, not output destination; `argument-hint` (C) narrows scope but doesn't isolate output; removing the command (D) removes useful functionality.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A prose warning (A) is probabilistic and the violation already happened despite instructions; committing before running (C) mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. Reading every file directly (B) floods context; inferring from names (C) guesses instead of investigating; splitting across terminal windows (D) doesn't share context between sessions meaningfully.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. Starting over (A) discards findings; deleting CLAUDE.md (C) frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. Re-reading the config (A) and inspecting the network connection (C) re-check already-verified steps; simply re-running (D) skips diagnosis entirely.

**54. B** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. Assuming a model problem (A) and switching models (C) guess without diagnosis; restarting the CI runner (D) doesn't investigate the cause at all.

**55. A** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. Per-team credentials in CLAUDE.md (B), duplicated per-team stdio integrations (C), and manual curl calls (D) all fail to provide reusable, centrally maintained access.

**56. B** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. Calling it just another tool (A), a platform built-in (C), and a Skill (D) mischaracterize this capability.

**57. A** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. B, C, and D are false or oversimplified claims about MCP's communication patterns and what remote servers can expose.

**58. A** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. Base64 encoding (B) is easily reversible obfuscation, not real protection; moving the repo private (C) and rotating on a schedule (D) don't remove the exposed credential from history or ongoing risk.

**59. B** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. Logging (A) and a confirmation prompt (C) are detective/compensating controls that leave the excess access in place; leaving it as-is (D) accepts unnecessary risk.

**60. B** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 1.*
