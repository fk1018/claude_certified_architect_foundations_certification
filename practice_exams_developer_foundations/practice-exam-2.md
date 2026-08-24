# CCDVF Practice Exam 2

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Incident-Response Ops Agent for a Cloud Hosting Provider, Batch Invoice-Extraction Pipeline for a Logistics Company, Prompt and Context Engineering for a Financial-Reporting Generator, Claude Code Governance for a Growing Platform Org) |
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

## Scenario A: Incident-Response Ops Agent for a Cloud Hosting Provider (Questions 1–15)

NimbusHost, a mid-size cloud hosting provider, has built an internal incident-response agent on the Claude Agent SDK. The agent has custom tools (`get_instance_health`, `restart_container`, `scale_cluster`, `notify_customer`, `query_billing_status`) and helps on-call engineers triage infrastructure incidents. Several of these actions cost real money or affect paying customers directly, so tool governance matters as much as reasoning quality.

---

**Question 1.** NimbusHost's incident agent calls tools sequentially and the orchestration code needs to know when to stop executing tool calls and surface a final answer to the on-call engineer. What should it check after each model turn?

- A) Whether the response text exceeds a fixed character count, treating any sufficiently long reply as though the model must be finished.
- B) Whether the response text happens to contain a customer-facing summary phrase, before deciding the current turn is complete.
- C) The `stop_reason` field: keep executing tool_use turns, and only surface the final answer once `stop_reason` reads `"end_turn"`.
- D) The elapsed wall-clock time since the incident was opened, ending the loop once a fixed duration has elapsed.

**Question 2.** After `restart_container` executes, what must happen for the agent to correctly continue reasoning about the incident?

- A) Email the restart result to the on-call channel directly and do not feed it back into the model's ongoing conversation at all.
- B) Append a summary of the restart to the system prompt so the outcome persists as background context rather than a turn-level result.
- C) Start a brand-new conversation that briefly summarizes the restart before continuing the whole incident investigation from scratch.
- D) Append a `tool_result` block referencing the matching `tool_use` ID to the conversation, then send the full updated conversation back to the model.

**Question 3.** Policy requires that `scale_cluster` never increase a cluster beyond 3x its baseline size without a VP's prior approval. The system prompt states this clearly, but logs show occasional autonomous scale-ups past that threshold. What is the most reliable fix?

- A) Repeat the 3x scale-up rule at both the start and end of the system prompt so the model sees it twice per turn.
- B) Add a hook that intercepts `scale_cluster` calls and blocks any request exceeding 3x baseline without a recorded prior approval.
- C) Add several few-shot examples showing the agent correctly escalating oversized scale requests to a VP for approval first.
- D) Lower the model's temperature so it samples less randomly and follows the stated 3x threshold policy more consistently across incidents.

**Question 4.** The team wants `get_instance_health` to run first on every incident, with no exceptions, before any other tool executes.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State in the system prompt, in clear and repeated language, that `get_instance_health` must always run first before any other tool on every incident.
- B) Set `tool_choice: "any"` on the first request so the model is guaranteed to call some tool, without pinning which tool that call must be.
- C) Set `tool_choice: {"type": "tool", "name": "get_instance_health"}` on the first request, then use normal tool choice afterward, without relying on temperature adjustments to enforce order.
- D) Add several few-shot examples in the prompt showing `get_instance_health` being called first on past incidents.

**Question 5.** The agent currently has 20 tools, including several rarely-used ones (refund issuance, marketing-campaign toggles, internal survey dispatch) unrelated to incident response. Tool selection has become unreliable.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` so the agent has noticeably more room in its response to reason about which of the twenty available tools is the right one to pick.
- B) Keep all twenty tools available but add a hook that logs which tool was selected each time, without actually reducing the twenty-tool list the model must choose from.
- C) Lower the temperature so tool choice becomes more consistent across similar incidents, without actually changing the underlying tool list itself.
- D) Remove or scope out the tools unrelated to this agent's incident-response role, such as refund issuance and marketing-campaign toggles, from its tool list.

**Question 6.** `restart_container` currently returns the generic string `"Failed"` for every possible failure — invalid container ID, permission denied, or orchestrator timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every `restart_container` call in an automatic retry policy that re-issues the request a fixed number of times whenever `"Failed"` comes back.
- B) Add a system prompt instruction telling the agent to infer the failure type from whatever context clues are available in the incident.
- C) Return structured error metadata from the tool itself: an error category, a retryable flag, and a human-readable description of the failure.
- D) Increase the orchestrator's timeout so that timeout-related failures become rarer, on the assumption most `"Failed"` results are really timeouts.

**Question 7.** When `get_instance_health` is called on a newly provisioned instance that hasn't reported its first health check yet, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same call. What should change?

- A) Add a hook that suppresses the error and quietly ends the conversation whenever a newly provisioned instance triggers it.
- B) Have the agent call `scale_cluster` first on every single incident to check the instance's provisioning state before it ever calls `get_instance_health` at all.
- C) Return a successful response indicating health data isn't available yet, reserving errors for actual access failures rather than pending states.
- D) Add a system prompt note explaining that this particular error usually just means the instance is new, not a real access problem.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `get_instance_health`, then `restart_container`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for incident response? (Select ONE response.)

- A) Model-driven selection is always cheaper than a fixed sequence, since letting the model choose skips reasoning tokens a rigid script would spend.
- B) Incidents are high-ambiguity: the right tools and their order vary by case and depend on intermediate results, which a fixed sequence can't adapt to.
- C) The Claude Agent SDK is technically incapable of executing a fixed, hard-coded sequence of tool calls like "always restart then check health."
- D) A fixed, hard-coded sequence of tool calls cannot invoke custom tools such as `restart_container` or `scale_cluster`; it is limited to Anthropic's built-in tools only.

**Question 9.** The team wants to add a `notify_customer` capability, which posts customer-facing status-page updates, but is deciding whether to give the main incident agent that tool directly or delegate notification decisions to a separate, narrowly-scoped subagent. Incorrect customer communication carries real reputational cost.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) A narrowly-scoped subagent given only `notify_customer` and explicit criteria reduces the chance the main agent sends a premature or incorrect customer update while reasoning about unrelated tools.
- B) Subagents are required by the SDK any time a tool has a real-world side effect, such as restarting a container or notifying a customer.
- C) The main agent's context window is too small to hold the `notify_customer` tool's schema alongside its existing tool definitions.
- D) Subagents execute their tool calls measurably faster than the same tool called directly from the main agent's own tool loop.

**Question 10.** During a long-running incident, the agent's context fills with verbose raw output from repeated `get_instance_health` calls, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` on each response so the agent has noticeably more room to write out its full reasoning about the accumulated raw health-check output across the incident.
- B) Delegate health-check exploration to a subagent that returns a distilled summary of relevant findings, rather than an increase to `max_tokens` to cope with the growing raw output.
- C) Read only the first 50 lines of every health-check result, on the assumption the relevant detail is always near the top.
- D) Disable health checks entirely for the remainder of the incident and rely on `restart_container` alone to resolve it.

**Question 11.** The agent successfully restarts a container, but the on-call engineer later has no visibility into what the agent tried before escalating — logs show 15 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include? (Select ONE response.)

- A) The full raw transcript of every tool call and result from the past 15 minutes, so the human can reconstruct it line by line.
- B) Just the final status code from the last tool call, since the human can re-investigate everything else from there.
- C) A sentiment analysis of how urgent the conversation seemed, based on tone and word choice across the agent's turns.
- D) A structured handoff summary covering what was tried, what was found, and a recommended next action, so the human can act immediately.

**Question 12.** The team is deciding between letting engineers run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on NimbusHost's own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Self-hosted agents running on NimbusHost's own infrastructure cannot register or invoke custom tools like `restart_container`.
- B) Managed, Anthropic-hosted execution environments are always less secure than a self-hosted harness, regardless of configuration.
- C) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- D) Managed execution environments can never reach private infrastructure at all, making tools like `query_billing_status` impossible to wire up in that model.

**Question 13.** An engineer asks whether a proposed "nightly disk-cleanup" task should be built as a fixed workflow or an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task involves more than three tools, since workflows above that count are assumed to need full agentic reasoning.
- B) Whether the team prefers to implement the orchestration code in Python or TypeScript, since each language favors a different pattern.
- C) Whether the task needs to run in under 30 seconds, since fixed workflows are assumed to always run deterministically faster than an agent's reasoning loop.
- D) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings the workflow can't predict.

**Question 14.** The `AgentDefinition` for a proposed "billing-lookup subagent" has a vague description: "Helps with billing." The main agent rarely delegates to it even when a billing question is clearly relevant.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent needs more tools; adding several more billing-related tools to its `AgentDefinition` will supposedly give it more capability to draw on when deciding whether to delegate.
- B) Subagents cannot actually be delegated to unless they are explicitly registered as MCP servers in `.mcp.json`.
- C) The main agent's temperature is set too low to consider delegating to a subagent instead of handling billing questions inline.
- D) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.

**Question 15.** The team wants a hard guarantee that `restart_container` is never called more than three times for the same instance within one incident, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the three-call limit clearly and asking the model to track its own count across the incident.
- B) A hook that tracks per-instance call counts and blocks the tool call once the three-restart limit is reached.
- C) A note in the tool's description mentioning the limit, so the model sees it each time it considers calling the tool.
- D) Few-shot examples in the prompt showing a prior agent correctly stopping after three restarts on the same instance during a similar incident.

---

## Scenario B: Batch Invoice-Extraction Pipeline for a Logistics Company (Questions 16–30)

Meridian Freight integrates Claude into a pipeline that extracts structured data — shipper, consignee, weight, freight charges, and accessorial fees — from bills of lading and carrier invoices. The pipeline handles both interactive single-document requests (an ops clerk uploads one document and waits) and large overnight batch runs (tens of thousands of documents).

---

**Question 16.** An overnight batch job processes 50,000 bills of lading with no user waiting on the result. No step needs the model to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API, run in parallel across many worker threads, to finish all fifty thousand documents as quickly as the infrastructure allows.
- B) The Message Batches API — latency-tolerant, non-blocking, high-volume work processed at a meaningfully reduced per-token cost compared to synchronous calls.
- C) The synchronous Messages API paired with a smaller model, trading away some extraction quality for a lower per-call cost across the whole batch.
- D) The synchronous Messages API with `max_tokens` reduced to the practical minimum, to shrink the size of each individual response returned.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry mismatched fields" loop to the batch pipeline, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts at all, so the schema and validation instructions in the loop have nowhere to live.
- B) The 24-hour completion window makes any retry logic within the loop practically impossible to schedule reliably alongside validation callbacks.
- C) The Batch API's context window is too small to hold bill-of-lading-length documents alongside the full extraction instructions, the structured field schema, and the validation criteria all at once.
- D) The Batch API cannot execute a tool call mid-request and feed results back to the model within a single request — required for this iterative extract-validate-retry loop.

**Question 18.** The interactive single-document flow shows ops clerks a real-time progress indicator while Claude processes their upload.

Question: What technique best supports this user experience? (Select ONE response.)

- A) The Batch API, since its asynchronous design is well suited to giving ops clerks real-time feedback while a document is processed.
- B) Streaming, so the UI can render output incrementally as it's generated, reducing perceived latency for the clerk.
- C) Increasing `max_tokens` so the full response is generated and returned to the client faster than before.
- D) Polling the Batch API's status endpoint once per second until the batch job reports completion.

**Question 19.** Every request sends the same 5,000-token extraction instructions and field-schema reference, followed by the specific bill-of-lading text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Place the stable 5,000-token instructions and schema reference first as a consistent, cacheable prefix, enable prompt caching, and put the varying document text last.
- B) Move the schema reference out of the system prompt entirely and into a few-shot example block placed just before the varying document text on every request.
- C) Truncate the schema reference down to a much shorter summary to save tokens on every single request, even if some field definitions become ambiguous.
- D) Switch to the smallest available model regardless of the effect on extraction quality, to reduce per-token cost across the entire batch.

**Question 20.** The extraction schema currently requires an `accessorial_charges` field on every invoice. Many shipments have no accessorial charges, and the model has started inventing small values rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the `accessorial_charges` field from the schema entirely, since most shipments don't have any.
- B) Add a prompt instruction telling the model not to invent values for `accessorial_charges` when none are present.
- C) Lower the temperature so the model is less likely to generate an invented `accessorial_charges` value.
- D) Make `accessorial_charges` nullable in the schema so a genuine absence of charges can be reported truthfully instead of being filled in.

**Question 21.** Two credible extraction passes on the same invoice disagree: one reads the total freight charge as $12,400.00 and another as $12,400.50, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do? (Select ONE response.)

- A) Flag the field for human review, presenting both candidate values and their extraction source, rather than silently picking one on the pipeline's own authority.
- B) Average the two candidate values and use $12,400.25 as the reported freight charge.
- C) Discard the invoice entirely from the batch, since the extraction has proven unreliable for this document.
- D) Always trust the first extraction pass's value over the second, regardless of which one is actually closer to the true freight charge stated on the original invoice document.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Define a `submit_extraction` tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of parsing free text.
- B) Wrap the JSON parse in a try/catch, and on every single failure automatically retry the whole request with "valid JSON only, no explanation text" appended to the prompt each time.
- C) Add a JSON-repair library to the pipeline to fix common syntax issues in the model's output before parsing it.
- D) Ask the model for YAML output instead of JSON, since YAML is generally more forgiving of small formatting drift.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some line-item weights don't sum to the stated gross shipment weight.

Question: What should you conclude and do? (Select ONE response.)

- A) Abandon tool use altogether and return to plain free-text extraction with mandatory human review on every single document going forward indefinitely, discarding the schema entirely.
- B) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks line-item weights against the stated gross weight on top of schema compliance.
- C) Tighten the schema's numeric field types even further, since the current field types are apparently too permissive to catch this kind of mismatch.
- D) `max_tokens` is set too low, causing the model to truncate its output mid-generation before the line-item totals become internally consistent.

**Question 24.** A subset of incoming bills of lading are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject scanned bills of lading with no text layer from the pipeline entirely, routing them to a fully manual process instead.
- B) Send the document image itself as a content block alongside the extraction instructions, using Claude's native vision input instead of relying solely on OCR text.
- C) Increase `max_tokens` so the model has more room to work through the degraded OCR text and infer the missing detail.
- D) Switch to a larger model on the theory that a bigger model is always better at reading noisy or damaged OCR text.

**Question 25.** The pipeline needs to run extraction on five sections of a long consolidated freight manifest concurrently to keep latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Async/concurrent request handling in the integration layer, so multiple API calls for different sections can be in flight at once without blocking on each other.
- B) Streaming responses for each section individually, since streaming is what supposedly allows more than one request to run at the same time.
- C) The Batch API, since it's assumed to be the only mechanism capable of running more than one extraction request concurrently.
- D) A single request with all five manifest sections concatenated together into one long document, relying on Claude to internally parallelize its handling of each section on its own.

**Question 26.** Meridian plans to run the same extraction pipeline through both the direct Anthropic API and Google Vertex AI for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) Extraction accuracy and latency are guaranteed to be identical to the millisecond across both vendor integrations.
- B) Vertex AI requires a completely different prompting approach, schema design, and extraction structure than the direct Anthropic API integration uses today.
- C) The Messages API contract stays conceptually the same across vendors, though auth/plumbing details and feature-rollout timing can differ.
- D) Batch processing is unavailable through any third-party vendor integration, only through the direct Anthropic API.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- B) Ignore thinking content entirely and strip it before storage, since it supposedly never affects how later turns in the multi-turn conversation are interpreted.
- C) Convert the thinking output into a synthetic tool call so it's tracked and stored the same way other tool interactions in the conversation are.
- D) Discard thinking content only in turns where a tool is also called, but preserve it fully in turns that have no tool calls at all.

**Question 28.** Finance asks for an accurate per-document cost breakdown for the extraction pipeline, but the current cost model only estimates based on average document length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, since caching is assumed to be the single dominant driver of extraction cost.
- B) Input tokens, output tokens, and cache read/write tokens separately, since each of these token categories is priced differently.
- C) A flat per-document fee that ignores document length or token usage entirely, for simplicity.
- D) Only output tokens, on the assumption that input tokens are effectively free by comparison.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the extraction pipeline's application code since "the model does the hard part."

Question: What is the correct response? (Select ONE response.)

- A) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that merely calls an external API like Claude's, since the API provider is assumed to be fully responsible for correctness of the whole pipeline.
- C) Only the prompt itself needs review, since Claude's structured output already guarantees the surrounding application code is low-risk by definition.
- D) Code review becomes unnecessary once the pipeline's evals are passing consistently.

**Question 30.** A single long-running session is used across an entire shift to process unrelated invoice batches from different carrier clients, and the team notices Claude increasingly referencing details from unrelated earlier carriers.

Question: What is the best fix? (Select ONE response.)

- A) Reduce the temperature for the remainder of the shift, on the theory that this alone will prevent the model from cross-referencing unrelated carriers.
- B) Increase the context window in use so an entire shift's worth of unrelated carrier history technically fits without the model apparently ever getting confused between different clients.
- C) Start a fresh session (or `/compact`) at natural task boundaries, such as between different carriers' batches, rather than trying to reset behavior via the system prompt mid-session.
- D) Ask the model to "ignore earlier documents" at the start of each new carrier's batch, within the same ongoing session.

---

## Scenario C: Prompt and Context Engineering for a Financial-Reporting Generator (Questions 31–45)

Ledgerline Analytics generates quarterly financial reports — narrative commentary plus supporting tables — for mid-market clients from raw general-ledger exports and transaction histories. Reports must follow a consistent structure and cite figures precisely, and the team is tuning model selection, prompting, and context handling to hit quality and cost targets.

---

**Question 31.** Most report sections are short, templated commentary (e.g., a routine "expense summary") generated at high volume with simple structure. Latency and cost matter far more than handling rare, highly complex sections well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) The highest-capability tier available, applied to every section, to guarantee quality even on the rare complex one.
- B) A fast, low-latency tier suited to high-volume, low-complexity sections, reserving a higher tier only for sections flagged as complex.
- C) Whichever tier happens to be cheapest per token, chosen without regard to whether it actually fits the task.
- D) The same tier used for the firm's hardest reasoning tasks, applied here too for consistency across the whole reporting pipeline.

**Question 32.** A small fraction of report sections require tracing a multi-entity intercompany reconciliation, where the fast default model produces shallow, incomplete commentary.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt across every section, hoping the extra examples close the reasoning gap.
- B) Switch every single report section across the whole pipeline to the highest-capability tier available, to be safe on the rare intercompany reconciliation case.
- C) Route only flagged complex sections to a higher tier, or one with extended thinking, keeping the fast path for everything else.
- D) Increase `max_tokens` for every section so there's more room for the model to reason through the intercompany reconciliation.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, report tone and numeric-citation style shifted noticeably without any code change.

Question: What should the team do differently? (Select ONE response.)

- A) Roll back permanently to the oldest available model version the team has ever used in production, to avoid any future behavior drift.
- B) Do nothing differently, since behavior drift across routine model releases is expected and needs no process change.
- C) Disable all prompt caching across the pipeline, on the theory that caching is what's causing the tone and citation-style shift.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Reports need a consistent structure (executive summary, variance analysis, notable transactions, outlook) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Write an even longer, more detailed prose description of the four-section structure than the team has already tried in prior iterations of the prompt.
- B) Lower the temperature to zero across all report generation, on the theory that removing randomness by itself will reliably produce a consistent four-section structure.
- C) Ask the model to restate the four-section structure back to itself before writing the actual report, as a brief self-check step.
- D) Provide 2–3 few-shot examples demonstrating the exact desired structure — executive summary, variance analysis, notable transactions, outlook — end to end.

**Question 35.** A client's ledger export is very long (thousands of transaction rows). The team wants a maximally detailed narrative and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input tokens and output tokens are budgeted from completely independent pools with no shared limit.
- B) Output length has no measurable effect on the request's overall latency.
- C) Long outputs are always truncated regardless of the model's context-window size, so requesting more detail is pointless.
- D) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.

**Question 36.** The reporting prompt currently places the specific transaction data before the general reporting instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; transaction-specific content should come after as the varying part.
- B) Order has no effect on either output consistency or cache hit rate, so the current ordering is fine as-is.
- C) Placing the specific reporting instructions last, immediately after all of the raw transaction data every time, always improves how closely and faithfully the model ends up attending to them.
- D) Reordering the prompt only ever affects cost, never output consistency, so it's a pure cost-tuning lever.

**Question 37.** Finance wants to know exactly how much the reporting service costs per client report, but the team currently estimates cost only from average ledger-export length.

Question: What should be instrumented instead? (Select ONE response.)

- A) Wall-clock latency per report, used as a stand-in proxy for actual dollar cost.
- B) Actual token usage per request — input, output, and cache — attributed per report, rather than an estimate from average export length.
- C) The number of API calls made per report only, without regard to how many tokens each call actually used.
- D) A flat cost assumption derived from the transaction-row count in each client's ledger export, regardless of how the model actually used tokens.

**Question 38.** An engineer writes an automated eval that asserts the generated variance-analysis paragraph must exactly match a fixed reference string, and the eval fails intermittently even though the reports look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model itself is broken and is producing genuinely wrong numeric answers on the variance-analysis paragraph specifically, independent of anything about how the eval was written or what it asserts.
- B) The eval needs a longer, more detailed reference string to match against.
- C) Temperature should be increased so the intermittent failures happen less often.
- D) LLM output is non-deterministic across calls; exact-match evals are the wrong tool — evals should tolerate reasonable variation (checking required content/structure) rather than exact text.

**Question 39.** Ledger exports include full raw metadata for every transaction (internal batch codes, system timestamps, routing IDs) that bloats the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Increase `max_tokens` on every request to accommodate the extra batch-code, timestamp, and routing-ID metadata.
- B) Switch to a model with a larger context window so the metadata bloat matters proportionally less.
- C) Prune tool/data output to the relevant fields — shipper, consignee, weight, charges — before they enter the prompt, rather than an increase to `max_tokens` to absorb the raw dumps.
- D) Summarize the raw metadata with a second Claude call before generating the report, adding an extra request per document.

**Question 40.** For clients with very long transaction histories, the team notices generated reports consistently miss mid-period transactions while capturing the opening and closing period well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Put a key-figures summary at the start of the input and organize the transactions under clear section headers, countering the tendency to attend most to the start and end of long inputs.
- B) Switch to a model with an even larger context window so every single transaction technically fits in one request without changing how the input is organized or summarized at all, regardless of the underlying attention pattern.
- C) Add an instruction telling the model to "pay equal attention to the whole period" regardless of how the input is organized.
- D) Alphabetize the transactions by counterparty name before summarizing them.

**Question 41.** A generated report confidently states a reconciled balance that, on manual review, never actually appears anywhere in the source ledger.

Question: What practice would most help catch this class of error before it reaches a client? (Select ONE response.)

- A) Trust confident, fluent-sounding output as sufficient evidence of correctness, since the report reads as well-supported.
- B) Increase the model's temperature so the balance is stated with less apparent confidence.
- C) Apply defensive parsing and skepticism toward confident output — verify key claims, such as stated balances, against the source ledger rather than accepting fluency as correctness.
- D) Shorten the report overall, on the theory that a shorter report leaves less room for a confidently wrong figure to appear.

**Question 42.** Detailed prose asking the model to "always output the report as valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the structured JSON-formatting instruction even more emphatically at both the start and end of the prompt.
- B) Increase `max_tokens` so there's enough room for both the preamble text and the full JSON body.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Post-process every response by stripping any text that appears before the first `{` character, then parse the remainder as JSON.

**Question 43.** The team wants to add an exploratory step that scans a client's prior-quarter reports for context before drafting the current one, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load the entire prior-quarter report history directly into the main drafting prompt for every client, every quarter.
- B) Skip historical context entirely for the current quarter's draft, to avoid the bloat risk altogether.
- C) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main drafting step.
- D) Increase the context window in use so the full multi-quarter history always technically fits alongside the current draft.

**Question 44.** For the simplest, most common report section (a standard cash-position summary), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot prompting is always strictly better than zero-shot for absolutely every task and client, regardless of how simple, well-understood, or high-volume the task already is in practice.
- B) Zero-shot prompting is required whenever latency matters at all, even for tasks with strict formatting needs.
- C) The choice between zero-shot and multi-shot has no measurable effect on either cost or latency.
- D) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.

**Question 45.** The reporting prompt has been modified informally by several analysts over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Adding a hook that blocks any edit to the prompt file entirely, rather than tracking changes to it as versioned history.
- C) Only allowing one single designated analyst to ever read or edit the reporting prompt going forward, indefinitely.
- D) Rewriting the reporting prompt from scratch every single quarter, discarding whatever informal changes accumulated during the previous quarter each time.

---

## Scenario D: Claude Code Governance for a Growing Platform Org (Questions 46–60)

Arbor Platform Engineering supports Claude Code and a set of internal MCP servers (deployment status, incident ticketing, an internal wiki) across an engineering org that has grown from 20 to 150 engineers in under a year. The platform team is responsible for team-wide configuration, CI integration, and troubleshooting as usage scales.

---

**Question 46.** A new engineer clones Arbor's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The new engineer needs to run `/memory` to activate memory files before conventions take effect.
- B) CLAUDE.md requires an explicit `@import` from the project root before it takes effect at all, and the new clone is missing that import.
- C) The conventions file exceeded an internal size limit and was silently truncated when the new engineer cloned it.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control to a fresh clone.

**Question 47.** A nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so the process waits indefinitely for interactive input a CI runner never provides.
- B) The pull requests being reviewed are simply too large in diff size for Claude Code to process correctly within a single automated CI run.
- C) The CI runner lacks the necessary permission to call the Claude API at all.
- D) The repository's CLAUDE.md file is malformed in a way that stalls the review.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Harden the existing regex with more permissive fallback patterns to tolerate whatever structured formatting drift shows up next.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure, for machine-parseable output.
- C) Post the entire raw review output as a single unparsed PR comment instead of extracting individual findings.
- D) Add a stronger prompt instruction telling the model never to deviate from the expected structured output format.

**Question 49.** Arbor's `/audit-licenses` custom command prints thousands of lines of dependency-license data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `allowed-tools`, restricting the command to read-only operations so it can't modify anything.
- B) `argument-hint`, so developers are prompted up front to scope the license analysis more narrowly before the command is ever run against the codebase.
- C) `context: fork`, so the command's verbose license output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- D) Removing the `/audit-licenses` command from the team's shared commands entirely.

**Question 50.** An internal `/new-microservice` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash structurally unavailable during execution.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands while creating a new microservice.
- C) Require developers to commit their current work before running any skill, so unwanted changes are at least recoverable.
- D) Convert the skill into a slash command instead, since slash commands are unable to run tools at all.

**Question 51.** An engineer needs to understand how a large, unfamiliar payments module works before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Read every file in the large payments module in one pass within the main conversation itself, to be as thorough as absolutely possible before making any change.
- B) Skip exploration entirely and infer the module's architecture from directory and file names alone.
- C) Split the exploration and implementation work across two separate terminal windows running independently.
- D) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session and rely on memory of what was learned during the discovery phase, without the original transcript.
- B) Delete the project's CLAUDE.md file temporarily to free up context space for the implementation step.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information already found.
- D) Continue working as-is; Claude automatically discards irrelevant context on its own without any command needed.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal deployment-status MCP tool, and writes a rollout report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Re-read the config file again from scratch, since that was the earliest step in the pipeline.
- B) The step between receiving the MCP tool's valid data and producing the report — the earlier inputs were confirmed correct, so the divergence is most likely in how that data was reasoned about afterward.
- C) The network connection to the MCP server, since that's the most technically complex step in the pipeline.
- D) Nothing — a wrong final report produced from confirmed-correct config and MCP inputs simply means the whole task should be re-run from scratch, and whatever new result comes back should be accepted without further diagnosis.

**Question 54.** A deployment-status integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Isolate whether the failure is at the integration layer (the API/tool call and its response) or in the model's output, by examining the trace of what was sent and received — not by first tweaking settings like temperature.
- B) Assume from the start that it's a model problem and rewrite the prompt before checking any of the surrounding integration code or its configuration.
- C) Switch to a different underlying model entirely to see whether the exact same failure still persists under the replacement.
- D) Restart the CI runner and simply try the identical deployment-status call again without changing any configuration.

**Question 55.** The internal incident-ticketing system needs to be reachable from Claude Code sessions across the whole engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Hard-code ticketing logic separately inside each individual team's own custom skill, duplicating the same integration work repeatedly across the org.
- B) Build an MCP server exposing ticketing operations as tools, shared across the org and maintained independently by the platform team.
- C) Have each team paste their own copy of ticketing API credentials directly into their project's CLAUDE.md.
- D) Ask each engineer to manually curl the ticketing API from their own terminal whenever a ticket needs to be created or updated.

**Question 56.** An MCP server for the internal wiki exposes both a `search_wiki` tool and a way for agents to see what wiki spaces exist without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP tool, functionally identical to `search_wiki` in that it performs a search-like action against the wiki on the agent's behalf.
- B) An MCP resource — content/catalog visibility distinct from a tool, which performs an action rather than exposing existing content.
- C) A built-in capability the platform provides automatically to every MCP server without configuration.
- D) A Claude Code Skill packaged alongside the wiki server's tool definitions.

**Question 57.** The team is deciding whether the deployment-status MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) stdio-based servers are always meaningfully faster and more deterministic than network-hosted ones, regardless of how many separate developer clients need to reach the server.
- B) MCP only ever supports one single communication pattern in practice, so there's no real architectural decision to make here at all.
- C) Where the server needs to run relative to the client and who needs access — local stdio for per-machine resources, remote/network hosting for centrally shared services.
- D) Remote, network-hosted MCP servers cannot expose tools at all under any configuration — only local stdio servers can, so remote hosting would eliminate the tool interface entirely for every consumer.

**Question 58.** Arbor's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Base64-encode the ticketing token before committing `.mcp.json`, so it isn't stored as obvious plain text in the repository.
- B) Move `.mcp.json` into a private repository instead of the current one, while still keeping the token hardcoded inside it.
- C) Rotate the ticketing token on a weekly basis going forward, without ever removing the hardcoded value from the file itself.
- D) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret itself is never committed to version control.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Scope the exposed tools down to only the operations workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Add detailed logging around the broad-access, ticket-deletion-capable tools so that any future misuse can at least be reviewed after the fact by the platform team during a periodic audit.
- C) Add a confirmation prompt before any deletion operation is executed, while leaving the underlying broad access itself completely unchanged.
- D) Leave access as-is for now, since no actual ticket-deletion misuse has been observed by the platform team yet.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific reporting workflow used by a single small team, versus a widely-reused authentication-checking capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) The one-off reporting workflow as a Skill or custom tool scoped to that team; the shared authentication capability as an MCP server or built-in tool maintained centrally for all consuming agents.
- B) Both the one-off workflow and the widely-reused authentication capability as MCP servers, since MCP is claimed to be the single correct architectural choice for any capability more than one team ever touches.
- C) Both as Skills, on the assumption that Skills are inherently reusable across every team regardless of how narrowly each one was originally scoped by its author.
- D) Both as built-in tools, since built-in tools are assumed to require the least setup regardless of how widely each capability actually ends up being used org-wide.

---
# Answer Key — Practice Exam 2

**Quick key:** 1-C, 2-D, 3-B, 4-C, 5-D, 6-C, 7-C, 8-B, 9-A, 10-B, 11-D, 12-C, 13-D, 14-D, 15-B, 16-B, 17-D, 18-B, 19-A, 20-D, 21-A, 22-A, 23-B, 24-B, 25-A, 26-C, 27-A, 28-B, 29-A, 30-C, 31-B, 32-C, 33-D, 34-D, 35-D, 36-A, 37-B, 38-D, 39-C, 40-A, 41-C, 42-C, 43-C, 44-D, 45-A, 46-D, 47-A, 48-B, 49-C, 50-A, 51-D, 52-C, 53-B, 54-A, 55-B, 56-B, 57-C, 58-D, 59-A, 60-A

---

**1. C** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. A fixed character count (A) and a customer-facing phrase (B) are text-based signals unrelated to completion state; elapsed time (D) doesn't reflect whether reasoning is actually done.

**2. D** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. A withholds the result from the model entirely. B misuses the system prompt for turn-level data instead of the conversation. C discards conversational state unnecessarily.

**3. B** — A financially consequential rule needs deterministic enforcement via a hook that blocks the call outright. Repeating the rule (A), adding few-shot examples (C), and lowering temperature (D) all remain probabilistic prompt-level compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns can revert to normal tool choice. `tool_choice: "any"` (B) guarantees some tool call but not which one. Prompt instructions (A) and few-shot examples (D) remain probabilistic.

**5. D** — Removing tools unrelated to the agent's core role directly shrinks the candidate set the model must reason over, improving selection reliability. A logging hook (B) records what was chosen but doesn't remove the bloat causing unreliable choices; increasing `max_tokens` (A) and lowering temperature (C) don't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately to each distinct failure. Blanket retry (A) wastes calls on non-retryable failures like permission denials. Asking the model to guess (B) is strictly worse than the tool reporting it. Increasing the timeout (D) reduces one failure type's frequency without fixing the missing information problem.

**7. C** — A not-yet-available health check is a valid pending state, not a failure — return success rather than an error so the agent doesn't misread it as "technical difficulties." Suppressing the error via a hook (A) hides real signal entirely. Checking provisioning state through `scale_cluster` (B) invents an unnecessary extra step. A prompt note (D) patches the symptom while the underlying success/error conflation remains in the tool itself.

**8. B** — High-ambiguity tasks where tools and order depend on intermediate findings are the core case for model-driven selection. Claiming model-driven selection is "always cheaper" (A) isn't reliably true, and the SDK claims in C and D are false — fixed sequences can call custom tools, they just can't adapt when the case doesn't fit the script.

**9. A** — A narrowly-scoped subagent with only the notification tool and explicit criteria minimizes accidental customer communication while the main agent reasons about unrelated tools. B overgeneralizes an SDK requirement that doesn't exist; C and D are unsupported technical claims about context size and execution speed.

**10. B** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis instead of raw output. Increasing `max_tokens` (A) doesn't reduce the accumulated input bloat; truncating to the first 50 lines (C) risks missing the actual finding; disabling health checks (D) removes needed capability.

**11. D** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately without reconstructing the investigation. The raw transcript (A) forces manual reconstruction; the status code alone (B) omits diagnostic context; sentiment analysis (C) conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, B, and D are all unsupported absolute claims about capability or security that don't hold in practice.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language choice, or an assumed runtime difference in A and C.

**14. D** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A misdiagnoses the cause as a capability gap; B and C are false claims about registration requirements and temperature's role in delegation.

**15. B** — A per-instance call-count hook is the only option that deterministically guarantees the limit regardless of what the model decides mid-conversation. A, C, and D all remain probabilistic prompt-level guidance that the model could still fail to follow.

**16. B** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at meaningfully reduced cost versus synchronous calls. Parallel synchronous calls (A) don't reduce per-token cost; a smaller model (C) and a lower `max_tokens` cap (D) risk quality or truncated output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request — each batch item is a single independent request. A, B, and C misidentify the actual limitation: system prompts are supported, the window doesn't block retries between separate requests, and context size isn't the constraint.

**18. B** — Streaming supports incremental rendering as tokens are generated, directly reducing perceived latency for a real-time progress indicator. The Batch API (A, D) is built for asynchronous, latency-tolerant work, not live per-document feedback; raising `max_tokens` (C) doesn't make the response arrive faster.

**19. A** — Only a stable, unchanged prefix is cacheable; placing the instructions and schema first with the varying content last maximizes cache hits, cutting both latency and cost. Moving the schema into few-shot examples (B) doesn't address caching; truncating it (C) risks losing needed detail; a smaller model (D) trades quality for cost without touching the caching problem.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. A prompt instruction (B) and a lower temperature (C) both rely on probabilistic compliance rather than fixing the schema constraint that's forcing the behavior; removing the field (A) loses the data entirely for shipments that do have charges.

**21. A** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. Averaging (B) invents a value neither pass produced; discarding the invoice (C) loses otherwise-good data; trusting the first pass by convention (D) is an arbitrary tiebreak with no basis.

**22. A** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. Retrying with a stronger prompt (B) and a repair library (C) are recovery layers for a problem that can be eliminated at the source; switching to YAML (D) swaps one fragile text format for another.

**23. B** — Schema validity guarantees syntax, not semantics; a separate validation step checking totals against line-item sums is needed on top of a working schema-constrained mechanism. Abandoning tool use (A) discards a mechanism that isn't actually broken; tighter numeric types (C) wouldn't catch an arithmetic mismatch; truncation (D) is a different failure mode than a completed-but-inconsistent total.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. A larger model (D) and more `max_tokens` (C) don't address the actual data-quality bottleneck, which is that OCR already dropped information before the model ever saw it; rejecting the documents (A) discards otherwise-processable work.

**25. A** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer so multiple in-flight requests don't block each other. Streaming (B) affects how one response arrives, not whether multiple requests run concurrently; the Batch API (C) isn't the only path to concurrency and isn't suited to this latency-sensitive case; concatenating sections into one request (D) doesn't achieve real concurrency and risks losing per-section attribution.

**26. C** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — that's the realistic expectation, not identical performance (A) or an entirely different prompting model (B). D is also false; batch-style processing is available beyond the direct API.

**27. A** — Thinking content is a distinct block type that must be handled — and typically preserved — separately from final answer text across multi-turn tool-use conversations. Stripping it unconditionally (B), converting it into a tool call (C), and discarding it only in some turns (D) all mishandle a block type the integration layer needs to track correctly.

**28. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-document cost breakdown. Focusing only on cache reads (A) or only on output (D) both ignore priced categories; a flat fee (C) ignores token usage entirely.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system. B, C, and D all treat some category of code as exempt from review for reasons that don't hold up.

**30. C** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. A larger context window (B) would let even more unrelated history accumulate rather than fixing the contamination; a lower temperature (A) and an in-session instruction to ignore prior context (D) are both unreliable levers that don't actually clear the accumulated context.

**31. B** — High-volume, low-complexity sections fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. Using the highest tier everywhere (A) and the hardest-task tier for consistency (D) both overspend by default; picking purely by price (C) ignores whether the tier fits the task at all.

**32. C** — Targeted routing of only the flagged complex sections to a higher tier addresses the actual gap without overspending on the high-volume simple path. Adding few-shot examples to the fast model (A), switching everything to the top tier (B), and raising `max_tokens` everywhere (D) all apply broad or mismatched fixes to a narrow, identifiable problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. Doing nothing (B) accepts avoidable risk; permanently pinning the oldest version (A) and disabling caching (C) are both unhelpful overcorrections unrelated to the actual fix, which is a controlled upgrade process.

**34. D** — Concrete few-shot examples are the most effective lever for consistent structure when detailed prose alone hasn't worked. Writing longer prose (A) repeats a failed approach; a restated structure (C) and a temperature of zero (B) don't reliably fix structural consistency the way worked examples do.

**35. D** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. Claiming they're independent (A), that output length doesn't affect latency (B), or that long outputs are "always truncated" regardless of context size (C) all misstate this relationship.

**36. A** — Stable, role-defining instructions form a consistent, cacheable prefix when placed first (ideally in the system prompt), improving both caching and consistency by separating fixed structure from varying content. Claiming order has no effect (B), that placing instructions last always helps (C), or that reordering only touches cost (D) all misstate the actual effect.

**37. B** — Actual per-request token usage (input, output, and cache) attributed per report gives an accurate cost picture. Latency (A), call count alone (C), and a flat assumption from row count (D) are all proxies that don't reflect what was actually billed.

**38. D** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. Assuming the model is broken (A) misdiagnoses correct-but-varying output as an error; a longer reference string (B) doesn't fix an exact-match design flaw; changing temperature (C) doesn't address the underlying non-determinism the eval design should tolerate.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. Increasing `max_tokens` (A) and a larger context window (B) work around the symptom without reducing waste; a second summarization call (D) adds cost and complexity for a problem solvable by simple field filtering.

**40. A** — Placing a key-figures summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A larger context window (B) is costly and doesn't guarantee the mid-document effect disappears; an instruction to pay equal attention (C) and alphabetizing (D) don't address the underlying attention pattern.

**41. C** — Verifying key claims against the source ledger catches confident-but-wrong output that fluency alone would let through. Trusting fluent output by default (A) is the failure mode itself; raising temperature (B) and shortening the report (D) don't address correctness at all.

**42. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike a prose request that can still drift. Repeating the instruction (A) and post-processing around the drift (D) are workarounds for a problem that can be structurally eliminated; increasing `max_tokens` (B) doesn't address the preamble issue at all.

**43. C** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. Loading full history (A) and a larger context window (D) both reintroduce the bloat risk; skipping historical context (B) discards potentially useful information entirely.

**44. D** — Task simplicity and volume should drive the zero-shot-versus-multi-shot tradeoff; multi-shot earns its cost on tasks needing format or edge-case consistency, which a simple high-volume task may not need. A and B are absolute claims that don't hold generally; C is false — the choice does affect both cost and latency.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. Blocking edits with a hook (B), restricting it to one reader (C), and rewriting it from scratch each quarter (D) are all impractical overcorrections that don't provide the actual missing capability — change tracking.

**46. D** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. Needing `/memory` (A), a missing `@import` (B), and a silent truncation (C) all misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a silent hang rather than a clean error. Oversized PRs (B), missing API permission (C), and a malformed CLAUDE.md (D) would each typically produce a distinct, visible failure rather than an indefinite hang.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. Hardening the regex (A) and a stronger instruction (D) are both reactive fixes to formatting drift that will recur; posting raw output (C) abandons the structured-comment requirement entirely.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns to the main conversation, directly fixing the described context pollution. `allowed-tools` (A) restricts capability, not where output lands; `argument-hint` (B) narrows scope but doesn't isolate the output; removing the command (D) removes useful functionality.

**50. A** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A written warning (B) is probabilistic and the violation already happened despite instructions; requiring a commit first (C) mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. D** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. Reading every file directly (A) floods the main context with exactly the material being avoided; inferring from names (B) guesses instead of investigating; splitting across terminal windows (C) doesn't meaningfully share context between them.

**52. C** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. Starting fresh (A) discards findings that took effort to gather; deleting CLAUDE.md (B) frees trivial space while losing team standards; D describes automatic behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. Re-checking the config (A) and the network connection (C) re-verify already-confirmed steps; re-running without diagnosis (D) skips finding the actual cause.

**54. A** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. Rewriting the prompt (B), swapping models (C), and simply restarting (D) all guess at a fix without first diagnosing which layer actually failed.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. Duplicating logic per team (A), pasting credentials into CLAUDE.md (C), and manual curl calls (D) all fail to provide reusable, centrally maintained access.

**56. B** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action like `search_wiki`. A, C, and D all mischaracterize this capability as a tool, a platform default, or a Skill.

**57. C** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine/local resources, remote hosting for centrally shared services accessed by many clients. A, B, and D are false or oversimplified claims about MCP's communication patterns.

**58. D** — Environment-variable expansion keeps the secret out of the version-controlled file while `.mcp.json` itself remains shareable. Base64 encoding (A) is easily reversible obfuscation, not real protection; moving repositories (B) and rotating on a schedule (C) don't remove the exposed credential from the file or its history.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. Logging (B) and a confirmation prompt (C) are detective or compensating controls that leave the excess access in place; leaving access as-is (D) accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — a Skill or custom tool for the one-off, team-specific workflow; an MCP server or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D all force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 2.*
