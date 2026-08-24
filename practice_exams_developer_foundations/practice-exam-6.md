# CCDVF Practice Exam 6

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
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

Kestrel Cloud runs virtual-machine and container hosting for mid-market customers. Its SRE team is building "Warden," an on-call assistant built on the Claude Agent SDK with custom tools (`check_node_health`, `restart_container`, `rotate_api_key`, `notify_customer`, `page_sre`). Warden triages incidents overnight before a human ever looks at them, so tool-execution correctness and guardrails matter as much as reasoning quality.

---

**Question 1.** Warden's harness needs to know when to keep feeding tool results back to the model versus when the model is finished responding for the turn.

Question: What should the harness check? (Select ONE response.)

- A) Track whether the running transcript contains resolution language such as "incident resolved," "fixed," or "closed," and stop the loop once any of those phrases appears in the assistant's most recent text block.
- B) Cap the harness at a fixed eight tool calls per session, on the reasoning that most Warden incidents resolve within that many exchanges.
- C) Stop once `notify_customer` has been called, since notifying the customer is treated as the terminal step of every incident.
- D) Check the `stop_reason` on each response: keep looping while it's `"tool_use"`, and stop once it becomes `"end_turn"`.

**Question 2.** After Warden calls `rotate_api_key` and the harness executes it, what is required for Warden to reason correctly about the outcome on its next turn?

- A) Log the rotation to the audit database and reference it by ticket number in the next prompt, since the audit trail is the durable record of what happened.
- B) Summarize the rotation result in a fresh system prompt for a brand-new session, discarding the current conversation so the summary becomes the new baseline.
- C) Append the rotated key's confirmation to the end of the running system prompt so it persists across the rest of the session.
- D) Add a `tool_result` block keyed to the original `tool_use` ID into the conversation and resend the full conversation, so the model sees the outcome in the turn it's expecting it.

**Question 3.** Kestrel's policy requires a human approve any `restart_container` call targeting a customer's primary database container. The system prompt states this rule prominently, but audits show a handful of autonomous restarts on database containers anyway.

Question: What is the most reliable fix? (Select ONE response.)

- A) Move the rule to the very first line of the system prompt, on the theory that primacy within the instructions increases compliance.
- B) Add several few-shot transcripts showing Warden pausing to escalate a database-container restart instead of executing it immediately, reinforcing the desired behavior by example.
- C) Lower the temperature parameter so Warden's behavior becomes more deterministic and it follows the written policy more literally on borderline cases.
- D) Add a hook that intercepts `restart_container` calls and blocks any targeting a database container unless a human-approval flag is already set — not a wording or temperature change.

**Question 4.** The SRE team wants Warden to always call `check_node_health` first on every incident, with zero exceptions, before considering any other tool.

Question: What is the most reliable way to enforce this? (Select ONE response.)

- A) State the ordering requirement clearly and prominently in the system prompt, spelling out that `check_node_health` must always run first, before any other tool, and repeating that instruction near the top of every incident-handling turn.
- B) Set `tool_choice: "any"` on the first request so some tool call is guaranteed.
- C) Set `tool_choice` to force `check_node_health` specifically on the first request, then revert to normal tool choice afterward.
- D) Add a hook that silently reorders any tool call list so `check_node_health` sorts first, without changing which tool the model actually chose to call.

**Question 5.** Warden currently has 19 tools registered, including several that belong to unrelated teams (billing adjustments, marketing-email suppression, feature-flag rollout). Tool selection accuracy has degraded noticeably.

Question: What is the single most direct fix? (Select ONE response.)

- A) Remove or scope out the tools that don't belong to Warden's incident-response responsibility, such as billing adjustments, marketing-email suppression, and feature-flag rollout.
- B) Add a "primary tools" note to the system prompt clarifying which of the 19 registered tools matter most for incident response, without removing any of the others.
- C) Increase `max_tokens` so Warden has more room to reason through which of the 19 tools to select before committing to a call.
- D) Rename the unrelated tools with less appealing, more generic descriptions so Warden is statistically less likely to select them during triage.

**Question 6.** `check_node_health` currently returns the bare string `"unavailable"` whether the node doesn't exist, the health-check agent timed out, or Warden lacks permission to query it. Warden's downstream behavior is inconsistent across these cases.

Question: What is the best fix? (Select ONE response.)

- A) Return structured error data — a category, a retryable flag, and a short description — so Warden can branch appropriately.
- B) Have Warden guess the cause from surrounding conversation context.
- C) Wrap every call in an automatic three-retry policy regardless of cause, rather than adding a hook that branches on it.
- D) Extend the health-check agent's timeout window so timeout-related failures occur less often in practice, leaving not-found and permission failures to still return the same unhelpful, undifferentiated string as before.

**Question 7.** When `check_node_health` finds a node exists but simply has no recent metrics (a quiet, healthy node), it currently returns an error. Warden then apologizes for a "system issue" and repeats the query.

Question: What should change? (Select ONE response.)

- A) Return a successful response with an empty result for a quiet node; reserve errors for genuine access failures.
- B) Add a system-prompt note explaining that this particular error usually just means the node is quiet and has no recent data to report, so Warden should treat it as routine rather than escalating or apologizing.
- C) Have Warden call `page_sre` automatically the moment this specific error string appears, treating silence as an emergency.
- D) Add a hook that silently ends the turn whenever this error appears, without informing the on-call engineer either way.

**Question 8.** An engineer proposes replacing Warden's tool reasoning with a fixed script: always call `check_node_health`, then `restart_container`, then decide, arguing this is more predictable.

Question: Why does model-driven tool selection remain the better fit here? (Select ONE response.)

- A) Incidents vary in cause and severity, and the right next tool depends on what earlier tool results revealed — a fixed sequence can't adapt to that.
- B) Fixed sequences technically cannot invoke custom tools registered through the Agent SDK's tool-definition schema, only built-in ones.
- C) Model-driven tool selection is always cheaper in tokens than a scripted sequence, because the model skips steps it judges unnecessary.
- D) A fixed script would require Warden's entire set of tool schemas to be rewritten from scratch before it could run at all.

**Question 9.** The team is deciding whether `page_sre` (which wakes a human at 3 a.m.) should live directly on Warden's main tool list, or be delegated to a small, narrowly-scoped subagent whose only job is deciding whether paging criteria are met.

Question: What is the strongest argument for the narrowly-scoped subagent? (Select ONE response.)

- A) A subagent given only the paging tool and explicit criteria is less likely to page unnecessarily while the main agent's system prompt stays focused on unrelated diagnostic tools.
- B) Subagents are required by the Agent SDK for any tool that has real-world side effects outside the conversation.
- C) Subagents always execute tool calls faster than the main agent, since they carry a smaller context window.
- D) A hook could technically block excess paging calls after the fact, but the main agent's context window is too small to hold the paging tool's schema alongside its other tool definitions in the first place.

**Question 10.** During a drawn-out incident, Warden's context fills with verbose raw health-check output, crowding out room for reasoning about root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Delegate health-check exploration to a subagent that returns only a distilled summary of relevant findings, keeping the main context focused on diagnosis.
- B) Truncate every tool result automatically to its first 20 lines, on the assumption that the most useful diagnostic detail always appears near the top of the output.
- C) Raise `max_tokens` so Warden's replies can run longer without hitting a length ceiling mid-explanation.
- D) Turn off automatic health-check querying during long incidents and rely solely on customer-submitted reports instead.

**Question 11.** Warden escalates an incident to a human on-call engineer after 25 minutes of tool calls, but the engineer has no easy way to see what Warden already tried.

Question: What should the escalation include? (Select ONE response.)

- A) The full raw tool-call transcript, unedited, so that no diagnostic detail is ever omitted from what the human engineer sees, even if it takes them several minutes just to scroll through it.
- B) Just the final error message, on the assumption that the human engineer will re-investigate the whole incident from scratch anyway.
- C) A tone/urgency rating generated from the conversation, so the human can gauge how serious Warden judged the incident to be.
- D) A structured handoff summarizing what was tried, what was found, and a recommended next action.

**Question 12.** Kestrel is deciding between running Warden through a hosted, Anthropic-managed execution environment versus self-hosting the agent harness on its own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Self-hosted agents technically cannot register or execute custom tools the way a managed environment can.
- B) Operational control (self-hosted) versus operational burden (managed) — the tools Warden can call don't differ based on where it runs.
- C) Managed execution environments are inherently less secure than self-hosting the harness on Kestrel's own infrastructure.
- D) Managed environments categorically cannot reach into Kestrel's private network under any configuration, no matter what networking or peering is set up.

**Question 13.** A junior engineer asks whether Warden's incident triage should be built as a fixed workflow or as an agent.

Question: What should decide this? (Select ONE response.)

- A) Whether the implementation language is Python or TypeScript, since some SDK versions expose agentic-loop features earlier in one language's package than the other.
- B) Whether the task is well-defined and repeatable, or instead high-ambiguity with a path that depends on intermediate findings.
- C) Whether the task must finish in under one minute of wall-clock time to satisfy an SRE on-call SLA.
- D) Whether more than five tools are involved in the resolution path for a given incident type.

**Question 14.** A proposed "log-correlation subagent" has the description "Looks at logs." Warden rarely delegates to it even when correlating logs across services is clearly the right move.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent's temperature parameter is set too low, making it too conservative to ever be selected for delegation.
- B) Subagents must be explicitly listed in `.mcp.json` before the main agent is permitted to delegate to them.
- C) The description drives delegation decisions; rewriting it to specifically state what the subagent does and when to use it will most directly fix the under-delegation.
- D) The subagent needs additional tools added to its definition — beyond basic log access — before Warden will reliably consider delegating log-correlation work to it.

**Question 15.** Kestrel wants a hard, non-negotiable guarantee that `restart_container` is never called more than twice on the same container within a single incident, regardless of what Warden decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A clearly worded two-call limit stated directly in the system prompt, repeated near the top of the instructions for emphasis.
- B) A note about the two-call limit placed inside the `restart_container` tool's description field instead of the system prompt.
- C) Few-shot transcripts showing an agent stopping after exactly two restarts on the same container in a past incident.
- D) A hook that tracks per-container call counts and deterministically blocks the tool call once the limit is reached.

---

## Scenario B: Batch Invoice-Extraction Pipeline for a Logistics Company (Questions 16–30)

Meridian Freight Logistics runs a nightly pipeline that extracts structured line-item data from carrier invoices — tens of thousands per night — plus a smaller interactive flow where a billing clerk uploads a single disputed invoice and waits for results. Some invoices are scanned images with degraded OCR, and the pipeline is being expanded to run across multiple regional cloud vendors.

---

**Question 16.** The nightly job processes 60,000 carrier invoices with no user waiting on any individual result, and no step needs Claude to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The Message Batches API — latency-tolerant, high-volume work at reduced cost.
- B) The synchronous Messages API, run across as many parallel threads as the account's rate limit allows for the night, trading higher per-call cost for real-time responses that nothing in this workload actually needs.
- C) The synchronous Messages API with `max_tokens` set to the minimum value that still lets extraction complete.
- D) The synchronous Messages API paired with the smallest available model, to keep unit economics acceptable at this volume.

**Question 17.** An engineer wants to add an "extract, validate line totals, retry any failed fields" loop to the nightly pipeline and proposes running that entire loop inside the Batch API to keep the cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't accept a system prompt, so the validation instructions have nowhere to live within a structured batch request.
- B) Batch requests are capped at a context window too small to hold a multi-page invoice alongside the schema and validation instructions.
- C) The Batch API can't execute a validation tool call mid-request and feed the result back to the model within a single request — which this iterative retry loop requires.
- D) The 24-hour batch turnaround window makes any kind of retry logic technically impossible to implement around it.

**Question 18.** The interactive single-invoice flow shows the billing clerk a live, incrementally-updating view of the extraction as it happens.

Question: What technique best supports this? (Select ONE response.)

- A) Polling the Batch API's status endpoint every second to approximate a live view of progress for the clerk.
- B) Streaming, so the UI can render partial output as it arrives and reduce the clerk's perceived latency.
- C) Raising `max_tokens` so the full extraction response completes and returns to the clerk sooner overall.
- D) The Batch API, since it's optimized for exactly this kind of real-time, single-invoice feedback loop the clerk is waiting on.

**Question 19.** Every extraction request sends the same 5,500-token field-schema and carrier-code reference, followed by invoice-specific text that varies per request.

Question: What single change most directly reduces both latency and cost across the whole pipeline? (Select ONE response.)

- A) Move the schema reference into a few-shot example instead of describing it in prose, on the theory that examples cache more efficiently than instructions.
- B) Place the stable schema and carrier-code reference first, enable prompt caching on that prefix, and put the varying invoice text last so the shared prefix is reused across requests.
- C) Truncate the carrier-code reference down to only the most common carriers, dropping the long tail to shrink the prompt.
- D) Switch to the smallest available model regardless of the effect on extraction quality, since latency matters more than accuracy here.

**Question 20.** The schema requires a `fuel_surcharge` field on every invoice line. Many lines have no surcharge, and the model has started inventing small nonzero values instead of reporting its absence.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field entirely so the issue can't occur.
- B) Add a prompt instruction warning the model against inventing values for fields that don't apply to a given invoice line, and repeat that warning near the schema definition.
- C) Lower the temperature parameter, since more deterministic sampling should reduce the rate of fabricated, nonzero surcharge values.
- D) Make `fuel_surcharge` nullable in the schema so its true absence can be reported instead of invented.

**Question 21.** Two extraction passes on the same invoice disagree on a weight field — one reads 2,140 lb, the other 2,410 lb — and there is no way to resolve the discrepancy from the surrounding text.

Question: What should the pipeline do? (Select ONE response.)

- A) Always trust whichever extraction pass ran first, on the assumption that earlier passes are less affected by drift.
- B) Average the two conflicting readings and record the midpoint as the accepted weight value.
- C) Flag the field for human review with both candidate values and their source, rather than silently picking one.
- D) Discard the invoice entirely as unreliable whenever any two extraction passes disagree on a numeric field, even if every other field on the invoice matches cleanly.

**Question 22.** The pipeline's free-text JSON extraction output fails to parse cleanly on roughly 4% of runs, crashing the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Ask the model for YAML instead of JSON, since YAML tolerates minor formatting drift better than strict JSON syntax.
- B) Add a JSON-repair library step that attempts to fix malformed output before it reaches the downstream loader.
- C) Retry the request with "return valid JSON only" appended to the prompt whenever a parse failure is detected.
- D) Define a tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of an increase in parsing retries on free text.

**Question 23.** After switching to strict schema-constrained tool use, output always parses successfully, but some line-item amounts still don't sum to the invoice's stated total.

Question: What should you conclude and do? (Select ONE response.)

- A) Strict schemas guarantee syntactic validity, not semantic correctness — add a validation step checking totals against summed line items.
- B) `max_tokens` must be set too low, truncating the structured output mid-generation before every field is populated.
- C) The schema needs stricter numeric types on the amount fields to prevent this class of mismatch.
- D) Abandon tool use and return to free-text extraction with manual review of every invoice, since structured output apparently can't be trusted for financial totals either.

**Question 24.** A subset of incoming invoices are scanned images with a badly damaged text layer, and the current pipeline sends only the OCR'd text to Claude, with poor results on the worst scans.

Question: What is the most direct fix? (Select ONE response.)

- A) Send the invoice image itself as a content block alongside the extraction instructions, using native vision input instead of relying solely on OCR text.
- B) Reject scanned invoices from the pipeline entirely and route them to a fully manual entry queue.
- C) Increase `max_tokens` so the model has more room to work through the degraded OCR text.
- D) Switch to a larger model, since bigger models always parse noisy OCR text better than smaller ones, regardless of how badly the underlying scan itself is damaged.

**Question 25.** The pipeline needs to process six sections of a very long consolidated freight manifest concurrently to keep total latency reasonable.

Question: What must the integration layer support? (Select ONE response.)

- A) Streaming, since concurrent processing of the six sections is only possible once streaming is enabled on each request.
- B) A single request with all six manifest sections concatenated together, relying on the model to parallelize internally across the sections in a single pass without separate calls.
- C) The Batch API, since it's the only mechanism that allows more than one request to be issued at a time.
- D) Async/concurrent request handling in the integration layer, so multiple calls run without blocking on one another.

**Question 26.** Meridian plans to run the same extraction pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted offering for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) The Messages API contract stays conceptually the same across vendors, though auth, plumbing, and feature-rollout timing can differ.
- B) Batch processing will be unavailable on every third-party vendor's hosted integration, regardless of which vendor is chosen.
- C) Extraction accuracy and latency are guaranteed to be identical across the direct API and every third-party vendor.
- D) Prompts and schemas need to be rewritten from scratch for each vendor's hosted offering before anything will work, since the underlying request format is assumed to differ completely.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task involving several tool-use turns.

Question: What must the integration layer handle correctly? (Select ONE response.)

- A) Convert any thinking content automatically into an additional tool call on the same turn it appears.
- B) Discard thinking content only on turns that also happen to include a tool call, keeping it on turns that don't.
- C) Ignore thinking content entirely across the conversation, since it never influences how later turns are reasoned about.
- D) Treat the thinking content block as distinct from the final answer text, and typically preserve it appropriately across the multi-turn conversation.

**Question 28.** Finance asks for accurate per-invoice cost accounting, but the current model only estimates cost from average prompt length.

Question: What should the improved model account for separately? (Select ONE response.)

- A) Only output tokens, treating input tokens as effectively free since they're typically much cheaper per unit.
- B) Input tokens, output tokens, and cache read/write tokens — an increase in granularity over a flat estimate — since each is priced differently.
- C) A flat per-invoice fee applied uniformly, regardless of how many tokens a given invoice actually consumes.
- D) Only cache read tokens, on the theory that caching dominates overall cost once the pipeline is warmed up.

**Question 29.** A new engineer argues code review can be skipped on the extraction pipeline's surrounding application code now that Claude does the extraction, since "the model is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Only the prompt needs review going forward; the surrounding application code is low-risk by definition once Claude handles extraction.
- B) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- C) Review is unnecessary once the pipeline's evals are consistently passing in CI.
- D) Review can be skipped for any code that primarily calls an external API rather than implementing logic directly, since the risk in that code is assumed to sit entirely with the API provider.

**Question 30.** A single long-running session processes invoice batches for several unrelated carrier clients across a full shift, and the team notices the model increasingly referencing details from an earlier, unrelated client's invoices.

Question: What is the best fix? (Select ONE response.)

- A) Ask the model to "ignore earlier invoices" at the start of each new client's batch, restating the instruction each time a client switches.
- B) Increase the context window so more history fits in a single session without the model losing track of which client is which, even as more unrelated clients' data accumulates over the shift.
- C) Lower the temperature parameter, on the theory that more deterministic sampling reduces the model's tendency to cross-reference details between clients.
- D) Start a fresh session (or `/compact`) at natural task boundaries, such as between different clients' batches, rather than accumulating unrelated context.

---

## Scenario C: Prompt and Context Engineering for a Financial-Reporting Generator (Questions 31–45)

Ashcroft & Vale, a mid-size accounting firm, runs a service that turns structured quarterly ledger data into narrative sections of client-facing financial reports — hundreds of reports per week during close season. The team is tuning model selection, prompt structure, and context handling to keep cost, latency, and factual reliability under control.

---

**Question 31.** Most report sections are short, formulaic narrative (e.g., "revenue summary") generated at high volume, where speed and cost per section matter far more than rare, deeply complex cases.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) Whichever tier is cheapest per token, chosen independent of whether it actually fits this task's complexity.
- B) The same tier used for the firm's hardest audit-reasoning work, applied here too for consistency across the whole service, even though this workload's complexity profile looks nothing like that audit work.
- C) A fast, low-latency tier suited to high-volume, low-complexity generation, reserving a higher tier only for sections flagged as complex.
- D) The highest-capability tier available for every section, to guarantee quality regardless of how simple the section is.

**Question 32.** A small fraction of report sections require multi-step reasoning (reconciling a multi-entity intercompany transfer) where the fast default model produces shallow, occasionally wrong narrative.

Question: What is the most targeted fix? (Select ONE response.)

- A) Increase `max_tokens` across the board for every section, on the assumption that more room to write fixes shallow reasoning.
- B) Switch every report section to the highest-capability tier available, to be safe against the rare complex case.
- C) Route only the flagged complex sections to a higher-capability tier or one with extended/adaptive thinking, keeping the fast path for everything else.
- D) Add more few-shot examples to the fast model's prompt, applied uniformly across all section types.

**Question 33.** The service currently always calls "whatever model is latest." After a routine model update, report tone and section structure shifted noticeably with no code change on Ashcroft & Vale's side.

Question: What should the team do differently? (Select ONE response.)

- A) Disable prompt caching across the pipeline, on the theory that cached prefixes are what's causing the tone shift.
- B) Do nothing — behavioral drift across model releases is an expected cost of using a hosted model and needs no process around it.
- C) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- D) Permanently roll back to the oldest available model version and freeze the pipeline there indefinitely.

**Question 34.** Report sections need a consistent structure (headline figure, drivers, comparison to prior period, outlook), but detailed prose instructions describing that structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Ask the model to restate the structure before writing the section, as a self-check step embedded in the same response.
- B) Provide 2–3 few-shot examples demonstrating the exact desired structure, rather than relying on a temperature change.
- C) Lower the temperature parameter to zero so output becomes more deterministic across runs.
- D) Write an even longer, more detailed prose description of the structure than what's already failing to work, spelling out every subsection and schema rule explicitly.

**Question 35.** A ledger detail input is unusually long (a full year of transaction-level entries), and the team wants a maximally detailed narrative output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) Long outputs are always truncated regardless of the context window size configured for the request.
- B) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- C) Output length has no bearing on request latency, regardless of how much the model has to generate.
- D) Input and output tokens are budgeted entirely independently of each other within a single request, so a longer input never reduces how much output room remains.

**Question 36.** The report-generation prompt currently places the specific client's ledger data before the general narrative-writing instructions and formatting rules in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last in the prompt always improves how carefully the model attends to them, regardless of what precedes them or how long the preceding client data runs.
- B) Stable, role-defining instructions belong first to form a consistent, cacheable prefix; the varying ledger data should come after.
- C) Reordering the prompt affects cost only, and has no bearing on output consistency either way.
- D) Prompt order has no measurable effect on either consistency or caching in practice.

**Question 37.** Finance wants an exact per-report cost figure for the narrative-generation service, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead? (Select ONE response.)

- A) A flat cost assumption based on ledger line count, applied the same way regardless of actual token usage per report.
- B) Actual token usage per request — input, output, and cache — attributed per report, rather than an estimate from average length.
- C) Number of API calls only, regardless of how many tokens each individual call actually consumed.
- D) Wall-clock latency per report, used as a stand-in proxy for cost.

**Question 38.** An engineer writes an automated eval asserting that a report section's output must exactly match a fixed reference string, and the eval fails intermittently even though manual review shows the generated sections are correct.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) Temperature should be raised so the model's output varies less predictably, which the team believes would fix the intermittent failures.
- B) LLM output is inherently non-deterministic across calls; exact-string-match evals are the wrong tool — check for required content instead.
- C) The reference string used for comparison needs to be made longer and more detailed.
- D) The model itself is broken and is producing incorrect narrative content on the failing runs, since a well-functioning model would never phrase the same correct figure two different ways.

**Question 39.** Ledger exports include full raw metadata for every transaction (internal system IDs, timestamps down to the millisecond, batch codes) that bloats the prompt with mostly-irrelevant data.

Question: What is the best fix? (Select ONE response.)

- A) Have a second Claude call summarize the raw metadata before it's handed to the main narrative-generation call, adding an extra request and a second prompt to maintain without a validation step confirming the summary kept what mattered.
- B) Switch to a model with a larger context window so the metadata bloat matters proportionally less.
- C) Prune the export to relevant financial fields before it enters the prompt, rather than passing raw dumps.
- D) Raise `max_tokens` to accommodate the extra structured metadata alongside the narrative output.

**Question 40.** For unusually long report sections drawing on a full year of ledger history, the generated narrative consistently captures the opening and closing quarters well but misses details from the middle of the year.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Add an instruction telling the model to "weigh all quarters equally" when writing the narrative, on the assumption that restating the goal in the prompt is enough to correct an attention pattern like this.
- B) Switch to a model with an even larger context window, without changing how the input itself is structured or organized, on the assumption that more capacity alone fixes uneven attention.
- C) Put a brief key-facts overview at the start and organize quarter-by-quarter data under clear section headers, countering the tendency to attend most to the beginning and end of long inputs.
- D) Sort the ledger entries alphabetically by account name before summarizing them into the narrative.

**Question 41.** A generated report section confidently states a revenue driver that, on manual review, doesn't actually appear anywhere in the underlying ledger data.

Question: What practice would most help catch this class of error before it reaches a client? (Select ONE response.)

- A) Shorten the section so there's less surface area for an unverified claim to appear in.
- B) Raise the temperature parameter so the model sounds less confident about claims it can't fully support.
- C) Apply defensive parsing and skepticism toward confident output — verify key claims against the source ledger data rather than trusting fluency alone.
- D) Trust well-written, fluent-sounding output as evidence of correctness by default, treating fluency itself as a validation step and skipping any separate check against the underlying ledger data entirely.

**Question 42.** Prose instructions telling the model to "always output valid structured JSON for the metrics block with these exact fields" still occasionally produce a free-text preamble before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Increase `max_tokens` so there's enough room for both the preamble text and the JSON block that follows it.
- B) Repeat the JSON-only instruction more emphatically at the very end of the prompt, right before the model starts generating.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Post-process every response to strip any text that appears before the first `{` character.

**Question 43.** The team wants to add a step that scans a client's prior four quarters of reports for context before drafting the current one, but worries this exploration will bloat the main prompt with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load all four prior quarters' full reports directly into the main prompt every time, regardless of how much of it turns out to be relevant.
- B) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main drafting step.
- C) Increase the context window so the full four-quarter history always fits alongside the current quarter's data.
- D) Skip historical context entirely to avoid the bloat risk, drafting each report from the current quarter alone.

**Question 44.** For the simplest, most common section type (a one-line cash-position statement), the team is deciding between a zero-shot prompt and a multi-shot prompt with several worked examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Zero-shot is required whenever latency matters at all, since any additional examples always slow down generation.
- B) Multi-shot is always strictly better than zero-shot, regardless of how simple or repetitive the underlying task's schema is, because more examples can never hurt output quality.
- C) For a simple, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its cost on tasks needing specific formatting or edge-case consistency.
- D) The choice between zero-shot and multi-shot has no effect on either cost or latency for a task like this.

**Question 45.** The report-generation prompt has been informally modified by several analysts over close seasons with no record of what changed or why, making a recent quality regression hard to diagnose.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treat prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Rewrite the prompt from scratch every quarter, discarding whatever accumulated changes came before.
- C) Allow only one designated analyst to ever read the prompt, restricting access to prevent further informal edits.
- D) Lock the prompt so it can never be changed again by anyone on the team, even to fix a bug found after the freeze.

---

## Scenario D: Claude Code Governance for a Growing Platform Org (Questions 46–60)

Corvid Systems has grown from 12 to 85 engineers in a year. Its platform team now owns Claude Code standards across the org, several internal MCP servers (ticketing, deployment status, internal wiki), and a CI pipeline that runs Claude Code headlessly for automated PR review.

---

**Question 46.** A newly hired engineer clones a Corvid repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) CLAUDE.md requires an explicit `@import` from the project root before its contents take effect at all.
- B) The team's conventions file exceeded an undocumented size limit and was silently truncated when Claude Code loaded it, so only part of the guidance ever reached the model.
- C) The new engineer needs to run `/memory` first to activate any memory files for the session.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level configuration that never travels through version control.

**Question 47.** Corvid's nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so it waits for interactive input the CI runner never provides.
- B) The repository's CLAUDE.md file is malformed and causing the session to fail silently on load.
- C) The pull requests being reviewed are too large for Claude Code to process within the CI job's timeout, given how much diff context a large PR review can require.
- D) The CI runner lacks permission to call the Claude API and is retrying the request indefinitely.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Post the entire raw output as a single PR comment instead of attempting to parse it into inline comments.
- B) Harden the regex with more permissive fallback patterns to catch the formatting variations that currently slip through.
- C) Add a stronger prompt instruction telling the model never to deviate from the expected output format.
- D) Run with `--output-format json` and a `--json-schema` defining the findings structure, for machine-parseable output the downstream parser can rely on.

**Question 49.** Corvid's `/audit-deps` custom command prints thousands of lines of dependency-graph data, and engineers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `argument-hint`, so engineers are prompted to scope the dependency analysis more narrowly before running it.
- B) `allowed-tools`, restricting the command to read-only operations so it can't modify the dependency graph it inspects, even though this wouldn't stop the verbose output itself from filling the main conversation.
- C) Removing the command entirely, since no configuration change reliably prevents this kind of context pollution.
- D) `context: fork`, so the command's output runs in an isolated sub-agent context instead of the main system prompt, returning only a summary.

**Question 50.** Corvid's internal `/scaffold-module` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Convert the skill into a slash command instead, since slash commands technically cannot invoke Bash or other tools.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands during scaffolding.
- C) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- D) Require engineers to commit their work before running any skill, so unrelated changes made by a misbehaving skill can be identified and reverted afterward, even though the modification itself already happened.

**Question 51.** An engineer needs to understand how permission checks flow through a large, unfamiliar service before making a change, and worries that reading dozens of files will exhaust context before implementation even begins.

Question: What is the best approach? (Select ONE response.)

- A) Split the investigation across two separate terminal windows, working the permission-check trail in parallel from both.
- B) Read every file in the service in one pass, in file order, to be as thorough as possible before making any change, trusting that completeness now saves confusion later.
- C) Use the Explore subagent for discovery so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- D) Skip exploration entirely and infer the architecture from directory and file names alone.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Delete the project's CLAUDE.md file temporarily to free up context space for the implementation work.
- B) Continue working as-is; Claude automatically discards context that becomes irrelevant as the session progresses.
- C) Start a brand-new session and rely on memory of what was learned during discovery, without carrying anything forward explicitly.
- D) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal MCP deployment-status tool, and writes a rollout report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) The step between receiving the MCP tool's valid data and producing the final report — since the inputs were confirmed correct, the divergence likely happened afterward.
- B) The network connection to the MCP server, since that's the most technically complex step in the pipeline and complex steps are the most likely place for silent failures to hide.
- C) Re-read the config file again from scratch, since that's the earliest step in the sequence.
- D) Nothing — a wrong report produced from correct inputs means the task should simply be re-run as-is.

**Question 54.** A deployment-status integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Restart the CI runner and try the deployment-status integration again without changing anything else.
- B) Switch to a different model and see whether the same integration failure persists under it, on the assumption that a different model would simply route around whatever the first one got wrong.
- C) Assume the failure is a model problem and rewrite the prompt before looking at anything else.
- D) Isolate whether the failure occurred at the integration layer (the API/tool call and response) versus the model's output, by examining the trace.

**Question 55.** The internal ticketing system needs to be reachable from Claude Code sessions across all of Corvid's engineering teams, not just one, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Ask each engineer to curl the ticketing API manually whenever they need ticket data during a session.
- B) Build an MCP server exposing ticketing operations as tools, shared and maintained centrally across the org.
- C) Hard-code ticketing logic separately into each team's own custom skill, duplicated per team.
- D) Have each team paste its own ticketing API credentials into its own CLAUDE.md file.

**Question 56.** Corvid's internal wiki MCP server exposes both a `search_wiki` tool and a way for agents to see what pages exist without making an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) A built-in tool the platform provides automatically to every Claude Code session without configuration.
- B) A Claude Code Skill packaged alongside the wiki server's other capabilities.
- C) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- D) An MCP tool, functionally identical to `search_wiki` in how it's invoked, just returning a catalog instead of search results.

**Question 57.** Corvid's platform team is deciding whether an internal MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) MCP only supports one communication pattern, so there's no real architectural decision to make here.
- B) Where the server needs to run relative to the client and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services.
- C) Remote MCP servers cannot expose tools at all, only read-only resources.
- D) stdio servers are always faster than remote servers, regardless of deployment context, network conditions, or how many clients are trying to reach the server at once.

**Question 58.** Corvid's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Rotate the ticketing API token weekly, while still leaving the current token hardcoded directly in the file.
- B) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret isn't committed to version control.
- C) Base64-encode the token before committing `.mcp.json` with the encoded value in place.
- D) Move `.mcp.json` to a private repository instead, keeping the token hardcoded as-is.

**Question 59.** An audit finds several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow at Corvid requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Leave access as-is for now, since no misuse of the broader ticket-deletion rights has actually been observed yet.
- C) Add a confirmation prompt before any deletion, so at least one extra step stands between the tool and an irreversible action.
- D) Add logging around the deletion tool so any misuse can be reviewed after the fact.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific release-notes workflow used by a single small team, versus a widely-reused permission-check capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) The one-off release-notes workflow as a Skill scoped to that team; the widely-reused permission-check capability as a centrally maintained MCP server or built-in tool.
- B) Both as MCP servers, since MCP is described as the correct choice for any capability that's shared across more than one team.
- C) Both as Skills, since Skills are described as reusable across any team that wants to invoke them, regardless of how many other teams and agents would eventually need to depend on that same capability.
- D) Both as built-in tools, since built-in tools are described as requiring the least setup effort of any option.

---
# Answer Key

**Quick key:** 1-D, 2-D, 3-D, 4-C, 5-A, 6-A, 7-A, 8-A, 9-A, 10-A, 11-D, 12-B, 13-B, 14-C, 15-D, 16-A, 17-C, 18-B, 19-B, 20-D, 21-C, 22-D, 23-A, 24-A, 25-D, 26-A, 27-D, 28-B, 29-B, 30-D, 31-C, 32-C, 33-C, 34-B, 35-B, 36-B, 37-B, 38-B, 39-C, 40-C, 41-C, 42-C, 43-B, 44-C, 45-A, 46-D, 47-A, 48-D, 49-D, 50-C, 51-C, 52-D, 53-A, 54-D, 55-B, 56-C, 57-B, 58-B, 59-A, 60-A

---

**1. D** — The loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text keywords (A) are unreliable, a call-count cap (B) is only a backstop, and waiting on a specific tool (C) doesn't reflect turn completion generally.

**2. D** — Tool results must be attached as a `tool_result` block referencing the original `tool_use` ID, with the full conversation resent so the model incorporates the outcome in the turn it expects it. Logging elsewhere (A) keeps the result out of the model's reasoning; appending to the system prompt (C) misuses turn-level data as persistent context; starting a new session (B) discards useful conversational state unnecessarily.

**3. D** — A safety-critical rule needs deterministic enforcement via a hook that blocks the call outright; prompt placement (A), few-shot examples (B), and temperature (C) all remain probabilistic compliance, which is exactly what's failing.

**4. C** — Forcing tool choice to a specific tool on the first turn guarantees it runs first; normal choice resumes afterward. `tool_choice: "any"` (B) guarantees a call but not which one; A remains probabilistic prompt guidance, and D's reordering hook doesn't change which tool the model actually decided to call in the first place.

**5. A** — Removing tools outside the agent's actual responsibility directly shrinks the candidate set it must reason over, which is the direct fix for degraded selection accuracy. B adds prompt overhead without removing the bloat; C and D don't address the root cause.

**6. A** — Structured error metadata (category, retryable flag, description) lets the agent respond appropriately to each distinct failure mode. Guessing (B) is strictly worse than the tool reporting it; blanket retries (C) waste calls on non-retryable failures; extending the timeout (D) only reduces one failure mode's frequency while leaving the other two just as ambiguous.

**7. A** — A quiet node with no recent metrics is a valid empty result, not a failure, so it should return success with an empty payload. A system-prompt workaround (B) patches the symptom while the underlying conflation of "no data" with "error" remains; C and D don't fix the misclassification itself.

**8. A** — Incident cause and severity vary, and the right next tool depends on what earlier results revealed — exactly the case model-driven selection is built for. B, C, and D are unsupported or false technical claims.

**9. A** — A narrowly-scoped subagent with only the paging tool and explicit criteria minimizes unnecessary paging while the main agent handles unrelated tools. B, C, and D are unsupported claims about subagents, and D's premise is also solvable more directly by trimming unrelated tools rather than assuming the context window itself is the constraint.

**10. A** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis instead of raw output. B and C are blunt workarounds; D removes needed capability.

**11. D** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately without reconstructing a transcript. A is unfiltered raw data that still costs the engineer time to process; B omits diagnostic context; C conveys mood, not facts.

**12. B** — The real tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between managed and self-hosted deployments. A, C, and D are unsupported absolute claims.

**13. B** — Task predictability versus dependency on intermediate findings is the deciding factor between a fixed workflow and an agent, not language, runtime speed, or tool count.

**14. C** — Subagent/tool descriptions drive delegation decisions; a vague description causes under-delegation regardless of tool count. A, B, and D misdiagnose the actual cause.

**15. D** — A per-container call-count hook is the only mechanism that deterministically guarantees the limit; A, B, and C remain probabilistic prompt-level guidance.

**16. A** — Latency-tolerant, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost and adds infrastructure to run in parallel; C and D risk quality or truncate output without addressing the real cost lever.

**17. C** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and D misidentify the actual limitation.

**18. B** — Streaming supports incremental rendering, which is what reduces perceived latency for a live progress view. D is the wrong API for this use case; A and C don't address perceived latency directly.

**19. B** — Only a shared prefix is cacheable, so placing stable content first and variable content last maximizes cache hits and reduces both latency and cost. A, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report genuine absence instead of inventing a value to satisfy a required field. A discards the field's value entirely; B and C rely on probabilistic compliance rather than a structural fix.

**21. C** — Conflicting reads with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and D all discard information or guess.

**22. D** — Tool-use with a matching input schema guarantees structurally valid output, eliminating this parsing-failure class outright. A and B are workarounds for a problem that can be structurally eliminated; C swaps one fragile text format for another.

**23. A** — Schema validity guarantees syntax, not semantics; a separate validation step checking totals against summed line items is needed on top. B, C, and D misdiagnose the mechanism or abandon it entirely rather than adding the missing check.

**24. A** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B discards otherwise-processable invoices; C and D don't address the actual data-quality bottleneck.

**25. D** — Concurrent API calls require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**26. A** — The Messages API contract stays conceptually consistent across vendors, though plumbing and rollout timing can differ — the realistic expectation, not identical performance or a full rewrite.

**27. D** — Thinking content is a distinct block type that must be handled — and typically preserved — separately from final answer text across multi-turn tool-use conversations. A, B, and C mishandle or misdescribe this.

**28. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-invoice cost breakdown. A, C, and D all oversimplify in ways that produce an inaccurate model.

**29. B** — Standard SDLC discipline still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system. A, C, and D all wrongly exempt code from review.

**30. D** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. A is unreliable prompt-level mitigation; B makes the cross-contamination risk worse, not better, by letting more unrelated history accumulate; C is an unrelated lever.

**31. C** — High-volume, low-complexity generation fits a fast, low-latency tier, with a higher tier reserved for flagged complex sections — matching capability to actual task difficulty. A and D overspend by default; B applies a tier suited to a different, harder workload.

**32. C** — Targeted routing of only the flagged complex sections to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and D apply broad, costly fixes to a narrow problem.

**33. C** — Pinning a version and deliberately testing before upgrading avoids unattributed behavior drift in production. B accepts avoidable risk; A and D are unhelpful overcorrections unrelated to the actual fix.

**34. B** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. D repeats a failed approach at greater length; A and C don't reliably fix structural consistency.

**35. B** — Input and output share one context-window budget, so a long input directly constrains available output length and vice versa. A, C, and D misstate this relationship.

**36. B** — Stable instructions first (ideally cacheable) with variable content after improves both clear role separation (consistency) and caching. A, C, and D misstate the effect of ordering.

**37. B** — Actual per-request token usage (input/output/cache) attributed per report gives an accurate cost picture; estimates or unrelated proxies (A, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A adds a second call and prompt to maintain for a problem simple filtering solves; B and D add cost or complexity without reducing the waste.

**40. C** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. B is costly and doesn't restructure the input at all; A and D don't address the underlying attention pattern.

**41. C** — Verifying key claims against the source ledger data catches confident-but-wrong output that fluency alone would let through. D is the failure mode itself; A and B don't address correctness.

**42. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A, B, and D are workarounds for a problem that can be structurally eliminated.

**43. B** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; D discards potentially useful context entirely.

**44. C** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format or edge-case consistency, which a simple high-volume task may not need. A, B, and D are absolute or false claims.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. D** — User-level CLAUDE.md never travels through version control, so a new engineer cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. D** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, B, and C are reactive or abandon the structured-comment requirement.

**49. D** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; A narrows scope but doesn't isolate output; C removes useful functionality.

**50. C** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. B is probabilistic and the violation already happened despite instructions; D only helps clean up after the fact rather than preventing it; A is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly in service of thoroughness; D guesses instead of investigating; A doesn't meaningfully share context between windows.

**52. D** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; B describes behavior that doesn't exist.

**53. A** — Since the config and MCP data were both confirmed correct, the divergence most likely happened in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. B redirects to an already-functioning step on a complexity assumption alone; C re-checks an already-verified step; D skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A, B, and C guess without diagnosis.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-team reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and D mischaracterize this capability.

**57. B** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. B** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A and C don't remove the exposed credential from history or ongoing risk; D is easily reversible obfuscation, not real protection.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. C and D are detective/compensating controls; B accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 6.*
