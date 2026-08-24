# CCDVF Practice Exam 10

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

NimbusHost operates virtual machines and managed containers for thousands of customers. The platform team is building "Aegis," an internal incident-response agent built on the Claude Agent SDK, with custom tools including `check_node_status`, `restart_container`, `scale_replica_pool`, `open_customer_incident`, and `escalate_to_oncall`. Several of these tools are destructive or customer-visible, so how tool access is granted and enforced matters as much as Aegis's reasoning quality.

---

**Question 1.** An engineer wants Aegis's tool-use loop to keep executing tools and returning results until Claude has no further tool calls to make. What should the loop's continue/stop decision key off?

- A) Check the response's `stop_reason` field: keep looping while it reads `tool_use`, and stop once it reads `end_turn`.
- B) Cap the loop at a fixed five tool calls per session and stop once that count is reached, no matter what Claude requests next.
- C) Scan the assistant's generated text for closing phrases such as "issue resolved" or "no further action needed."
- D) Stop the loop once any single tool call's round-trip exceeds a fixed two-second latency threshold.

**Question 2.** After `restart_container` executes, what must the client code do so Aegis can keep reasoning correctly about the incident?

- A) Fold the restart outcome into a fresh system prompt for the next request, replacing the prior one entirely.
- B) Append a `tool_result` block tagged with the matching `tool_use_id`, then resend the conversation.
- C) Log the outcome only to the incident ticket, on the assumption Aegis will infer success from later context.
- D) Close the current turn and start an entirely new conversation containing just the restart's result, dropping every earlier turn about the incident.

**Question 3.** Policy requires human approval before `restart_container` runs on any production load-balancer node. The system prompt states this clearly, but logs show occasional unapproved restarts on those nodes anyway. What is the most reliable fix?

- A) Add a hook that intercepts `restart_container` and blocks it against a load-balancer node unless a recorded approval exists.
- B) Restate the approval requirement in both the opening and closing paragraphs of the system prompt for emphasis.
- C) Add a few-shot transcript demonstrating Aegis correctly requesting approval before restarting a node.
- D) Lower the model's temperature and also restate the same approval policy as a bolded bullet point at the very top of the system prompt, hoping the emphasis and reduced randomness make Aegis comply more literally with the existing policy every time.

**Question 4.** The team wants `check_node_status` to always run first on every incident, with no exceptions, before any other tool executes.

Question: What is the most reliable implementation?

- A) State plainly in the system prompt that `check_node_status` must run before any other tool, every time.
- B) Force `tool_choice` to `check_node_status` specifically on the first request, then use normal tool choice afterward, independent of the model's temperature setting.
- C) Add a few-shot transcript showing `check_node_status` being called first, before any other tool appears.
- D) Set `tool_choice: "any"` on the first request so Aegis is guaranteed to call some tool immediately.

**Question 5.** Aegis now has 18 tools, including several rarely used ones (billing lookup, marketing email tool, feature-flag toggle) unrelated to incident response, and tool selection has become unreliable.

Question: What is the most effective fix?

- A) Add a system-prompt note explaining which of the 18 tools count as "core" versus "auxiliary" for incident work.
- B) Raise `max_tokens` so Aegis has more room to reason through which of the 18 tools to pick.
- C) Keep the full 18-tool set but reorder the tool list alphabetically so related tools sit near each other.
- D) Remove the unrelated tools from Aegis's definition, scoping it to incident-response actions only.

**Question 6.** `check_node_status` currently returns the bare string `"Error"` for every possible failure — invalid node ID, permission denied, or monitoring-service timeout. Aegis responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry hook that blindly resends the request up to three times.
- B) Return structured metadata with an error category, a retryable flag, and a description.
- C) Add a system-prompt instruction telling Aegis to infer the failure type from the wording of the error string.
- D) Increase the monitoring service's own timeout setting so fewer of these failures occur in the first place.

**Question 7.** A `query_incident_history` tool returns an error whenever no past incidents match the query. Aegis responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Return success with an empty result set, reserving errors for genuine access failures.
- B) Add a hook that silently ends the conversation the moment this particular error appears.
- C) Have Aegis call `check_node_status` first, as a way of confirming whether any history should exist.
- D) Add a system-prompt note explaining that this particular error usually just means nothing matched.

**Question 8.** An engineer proposes replacing Aegis's reasoning with a fixed sequence — always call `check_node_status`, then `query_incident_history`, then decide — arguing this makes behavior predictable.

Question: Why is model-driven tool selection the better fit here?

- A) Model-driven selection is always the cheaper option, since it skips reasoning tokens a fixed sequence would spend anyway.
- B) Incidents are high-ambiguity: the right tools and order depend on intermediate findings a fixed sequence can't adapt to.
- C) The Claude Agent SDK has no mechanism capable of executing a fixed, hardcoded tool sequence at all.
- D) A fixed sequence is limited to built-in tools and structurally cannot invoke a custom tool like `check_node_status`.

**Question 9.** The team is deciding whether to give Aegis the `escalate_to_oncall` tool directly or delegate paging decisions to a separate, narrowly-scoped subagent, since paging has a real cost (waking someone up) and should only happen under specific criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent?

- A) A subagent holding only the escalation tool and explicit paging criteria reduces accidental pages while Aegis reasons about unrelated tools.
- B) Subagents are required by the SDK any time a tool has a real-world side effect like paging someone.
- C) The main agent's context window is too small to hold the escalation tool's schema alongside the other 17 tools.
- D) Subagents always execute tool calls faster than the main agent, since they run in a separate process.

**Question 10.** During a long-running incident, Aegis's context fills with verbose raw log and status output, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix?

- A) Raise `max_tokens` so Aegis's responses have more room to be longer.
- B) Delegate log exploration to a subagent that returns a distilled summary, keeping the main context focused on diagnosis.
- C) Read only the first 20 lines of every log query result and discard the rest before it reaches Aegis, on the assumption that whatever caused the incident always shows up early in the log output.
- D) Disable log querying entirely and have Aegis rely solely on `check_node_status`.

**Question 11.** Aegis escalates an incident to a human, but the on-call engineer has no visibility into what Aegis already tried — logs show 20 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include?

- A) The full raw transcript of all 20 minutes of tool calls and their results, for completeness.
- B) A structured handoff: what was tried, what was found, and a recommended next action.
- C) Just the final error message, on the assumption the human can re-investigate from there.
- D) A sentiment score rating how urgent the incident sounded in Aegis's generated text.

**Question 12.** The team is deciding between a hosted, Anthropic-managed execution environment for Aegis versus self-hosting the agent harness on NimbusHost's own infrastructure.

Question: What is the core tradeoff?

- A) A self-hosted harness cannot register or call any custom tool, unlike a managed environment.
- B) A managed execution environment structurally cannot reach any of NimbusHost's private infrastructure, since Anthropic's hosted sandbox has no network path back into a customer's own VPC or on-prem systems.
- C) A managed environment is always the less secure of the two options, regardless of configuration.
- D) Operational control versus operational burden — the tools an agent can call don't differ by hosting choice.

**Question 13.** An engineer asks whether the incident-response task should be built as a fixed workflow or as an agent.

Question: What is the deciding factor?

- A) Whether the task involves calling more than three distinct tools during a typical run.
- B) Whether the platform team prefers building the harness in Python or in TypeScript.
- C) Whether the task must complete in under 30 seconds to satisfy an SLA.
- D) Whether the task is well-defined and repeatable, or high-ambiguity with a path depending on intermediate findings.

**Question 14.** A proposed "log-analysis subagent" has a vague `AgentDefinition` description: "Helps with logs." Aegis rarely delegates to it even when log analysis is clearly needed.

Question: What is the most likely cause and fix?

- A) The subagent needs more tools; adding several more log-related tools to its definition will fix delegation.
- B) Subagents cannot be delegated to at all unless they are separately registered in `.mcp.json`.
- C) The main agent's temperature is set too low to consider delegating to a subagent in the first place.
- D) Delegation is driven by the description; rewriting it to state specifically what it does and when to use it fixes under-delegation.

**Question 15.** The team wants a hard guarantee that `restart_container` is never called more than twice for the same host within one incident, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism?

- A) A system-prompt instruction stating the two-call-per-host limit as clearly as possible.
- B) A note added to the tool's own description mentioning the two-call limit.
- C) A hook that tracks per-host call counts and blocks the call once the limit is reached, regardless of the model's temperature setting.
- D) Few-shot examples demonstrating Aegis stopping itself after exactly two restarts on a host.

---

## Scenario B: Batch Invoice-Extraction Pipeline for a Logistics Company (Questions 16–30)

Cascade Logistics runs a document-intelligence pipeline that extracts structured line-item and total data from freight invoices and bills of lading. The pipeline handles two flows: an overnight batch job processing tens of thousands of scanned invoices with no one waiting, and an interactive lookup used by customer-service reps who upload a single invoice and wait on the result.

---

**Question 16.** The overnight batch job processes 25,000 freight invoices with no user waiting on the result, and no step requires Claude to call a tool mid-request.

Question: Which API best fits, and why?

- A) The synchronous Messages API with the smallest available model, purely to minimize per-token cost.
- B) The synchronous Messages API fanned out across many parallel threads, to finish the run as fast as possible.
- C) The Message Batches API — latency-tolerant, non-blocking, high-volume processing at reduced cost.
- D) The synchronous Messages API with `max_tokens` set to the minimum the schema could plausibly need.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry failed fields" loop to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed?

- A) The Batch API can't run a mid-request validation tool call and feed results back within one request, which the loop needs.
- B) The Batch API does not support including a system prompt in its requests.
- C) The 24-hour completion window makes any form of retry logic structurally impossible to schedule.
- D) The Batch API's context window is too small to hold a full freight invoice's extracted text alongside the 6,000-token schema reference, so the validation step would run out of room before it even started.

**Question 18.** The interactive single-invoice flow shows the customer-service rep a real-time progress indicator while Claude processes the upload.

Question: What technique best supports this user experience?

- A) The Batch API, since it was purpose-built to feed real-time progress indicators.
- B) Raising `max_tokens` so the complete response is generated and arrives sooner overall.
- C) Streaming, so the UI renders output incrementally and perceived latency drops.
- D) Polling the Batch API's status endpoint once per second until the job completes.

**Question 19.** Every request sends the same 6,000-token extraction instructions and field-schema reference, followed by the specific invoice text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests?

- A) Move the 6,000-token schema reference into a few-shot example block instead of a plain instruction.
- B) Switch to the smallest available model regardless of the effect on extraction quality.
- C) Put the stable instructions and schema first, enable prompt caching, and put the varying invoice text last.
- D) Truncate the schema reference down to the fields used most often, to save tokens per request.

**Question 20.** The extraction schema currently requires a `discount_amount` field on every invoice. Many invoices have no discount, and the model has started inventing small values rather than reporting none.

Question: What schema change fixes this?

- A) Remove the `discount_amount` field from the schema entirely, so it's never extracted.
- B) Add a prompt instruction directly telling the model not to invent discount values.
- C) Make `discount_amount` nullable so its genuine absence can be reported truthfully.
- D) Lower the temperature setting to reduce the rate of invented values.

**Question 21.** Two credible extraction passes on the same invoice disagree: one reads the total as $6,140.00, the other as $6,140.50, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do?

- A) Average the two candidate totals and store the averaged figure as the final value.
- B) Discard the invoice from the pipeline entirely, on the assumption that any invoice producing two disagreeing extraction passes is inherently unreliable and not worth the review effort.
- C) Flag the field for human review with both candidate values and their source, rather than silently picking one.
- D) Always trust whichever of the two extraction passes happened to run first.

**Question 22.** The extraction step's JSON output occasionally fails to parse — about 3% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix?

- A) Wrap the parse call in a try/catch and retry once with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library to the pipeline to validate and fix common syntax issues before parsing.
- C) Switch the output format to YAML instead, since it's more forgiving of structured formatting drift than JSON.
- D) Define a `submit_extraction` tool matching the schema, and read the data from the `tool_use` block instead of parsing free text.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some extracted line-item amounts don't sum to the stated invoice total.

Question: What should you conclude and do?

- A) Make the schema's numeric types even stricter, which should resolve the summation mismatch.
- B) `max_tokens` is likely too low, silently truncating output mid-generation before the total is written, which would also explain why the extracted line items look otherwise valid.
- C) Abandon schema-constrained tool use and fall back to free-text extraction with human review.
- D) Schema compliance guarantees syntax, not semantics; add a validation step checking totals against line-item sums.

**Question 24.** A subset of incoming invoices are scanned images with no text layer. The pipeline currently sends only OCR-extracted text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix?

- A) Reject scanned invoices with no text layer from the pipeline entirely, routing them elsewhere.
- B) Send the invoice image itself as a content block alongside the instructions, using vision input instead of relying solely on OCR text, which can increase accuracy on damaged scans.
- C) Raise `max_tokens` so the model has more room to work through the degraded OCR text.
- D) Switch to a larger model on the assumption that bigger models always read noisy, damaged OCR text better regardless of whether the underlying image itself was ever given to the model at all.

**Question 25.** The pipeline needs to run extraction on several sections of a long bill of lading concurrently to keep latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this?

- A) Async/concurrent request handling, so several API calls can be in flight without blocking each other.
- B) Streaming, since streaming is the only mechanism that supports running requests concurrently.
- C) The Batch API, since it's the only way to have more than one request active at once.
- D) A single request with every section concatenated together, since Claude parallelizes work internally.

**Question 26.** Cascade Logistics plans to run the same extraction pipeline through both the direct Anthropic API and Amazon Bedrock for different regional deployments.

Question: What should the team expect?

- A) Extraction accuracy and latency will be identical to the millisecond across both vendors.
- B) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- C) Bedrock requires a completely different prompting approach and a redesigned extraction schema, since the underlying model behaves as a fundamentally different product once hosted through a third-party cloud vendor.
- D) Batch-style processing is unavailable on every third-party vendor integration, including Bedrock.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly?

- A) Ignore the thinking content block entirely, since it never influences any later turn.
- B) Handle the thinking block as distinct from the final answer text, typically preserving it across the multi-turn tool-use conversation.
- C) Convert the model's thinking output into an additional tool call for the client to execute.
- D) Discard thinking content, but only on turns where a tool call is also present.

**Question 28.** Finance asks for an accurate per-invoice cost breakdown for the extraction pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately?

- A) Only cache read tokens, on the assumption that caching is by far the single dominant cost driver for a pipeline reusing the same 6,000-token schema reference on every invoice.
- B) Only output tokens, on the assumption input tokens are effectively free.
- C) A flat per-document fee applied regardless of actual token usage.
- D) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the extraction pipeline's application code since "the AI part is the risky part."

Question: What is the correct response?

- A) Skip review for any code in the pipeline that happens to call an external API.
- B) Code review becomes unnecessary once the pipeline's evals are passing consistently.
- C) Only the prompt itself needs review; the surrounding application code is low-risk by definition.
- D) Standard SDLC practices — review, testing, version control — still apply to the code around Claude.

**Question 30.** A single long-running session is used across an entire day to process unrelated invoice batches from different shipping clients, and the team notices Claude increasingly referencing details from unrelated earlier invoices.

Question: What is the best fix?

- A) Reduce the temperature setting to prevent cross-referencing between unrelated invoices.
- B) Start a fresh session (or `/compact`) at natural boundaries, such as between different clients' batches.
- C) Ask the model to "ignore earlier invoices" at the start of each new client's batch.
- D) Switch to a model with a larger context window, on the assumption that fitting more of the day's unrelated invoice history in at once will make the cross-referencing problem go away on its own.

---

## Scenario C: Prompt and Context Engineering for a Financial-Reporting Generator (Questions 31–45)

Ledgerline Analytics generates automated narrative commentary for corporate finance teams — quarterly variance write-ups, budget-vs-actual summaries, and consolidated multi-entity reports. Most reports are short and routine; a smaller fraction involve complex multi-entity consolidations that require careful cross-referencing. The team is tuning model selection, prompt structure, and context handling to hit accuracy, cost, and latency targets.

---

**Question 31.** Most reports are short, routine variance write-ups, and the task is simple and extremely high-volume. Latency and cost per report matter far more than handling rare, highly complex consolidations well.

Question: Which model tier best fits the default path?

- A) The highest-capability tier available for every single report regardless of volume, to guarantee top-end quality even on the shortest, most routine variance write-up the team produces.
- B) Whichever tier happens to be cheapest per token, without regard to whether it fits the task.
- C) The same tier the company reserves for its hardest reasoning work, kept for consistency.
- D) A fast, low-latency tier suited to high-volume/low-complexity work, reserving a higher tier for flagged complex reports.

**Question 32.** A small fraction of reports require multi-step reasoning (a multi-entity consolidation with intercompany eliminations) where the fast default model produces shallow commentary.

Question: What is the most targeted fix?

- A) Add more few-shot examples to the fast model's prompt, applied uniformly to every report.
- B) Route only the flagged complex reports to a higher-capability tier or one with extended thinking, keeping the fast path for the rest.
- C) Switch every report in the entire pipeline to the highest-capability tier across the board, to be safe, even though most reports are short and routine enough for the fast default.
- D) Raise `max_tokens` for every report regardless of whether the report is actually complex.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, report tone and structure shifted noticeably without any code change.

Question: What should the team do differently?

- A) Nothing — behavior drift across model releases is expected and needs no process around it, since model output was never meant to be deterministic anyway.
- B) Roll back permanently to the single oldest model version the vendor still supports.
- C) Pin a specific model version in production and test deliberately before any upgrade.
- D) Disable prompt caching across the pipeline, on the theory that caching is causing the drift.

**Question 34.** Reports need a consistent structure (headline variance, root cause, forward outlook) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help?

- A) Write an even longer and more detailed prose description of the required structured format.
- B) Ask the model to restate the required structure back before it starts drafting the report.
- C) Provide 2–3 few-shot examples that demonstrate the exact desired structure directly.
- D) Lower the temperature setting all the way to zero across every report.

**Question 35.** A consolidated report draws on very long source data (50+ pages of ledger detail). The team wants a maximally detailed narrative and considers requesting a very long output to match.

Question: What tradeoff must they account for?

- A) Input and output share one context-window budget, so a long input leaves less room for a long output.
- B) None — input tokens and output tokens are budgeted from two completely independent pools.
- C) Output length has no measurable effect on the request's overall latency.
- D) Long outputs are always truncated by the API regardless of the context window's size.

**Question 36.** The reporting prompt currently places the specific ledger data before the general drafting instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability?

- A) Placing instructions last, right after the ledger data, always improves how closely the model attends to them, regardless of how the surrounding prompt caching is set up.
- B) Reordering the prompt only ever affects cost, never the consistency of the output.
- C) The order of prompt content has no measurable effect on either consistency or caching.
- D) Stable, role-defining instructions belong in the system prompt or start of the turn as a cacheable prefix; report-specific data should follow as the varying part.

**Question 37.** Finance wants to know exactly how much the reporting service costs per report, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead?

- A) Wall-clock latency per report, used in place of actual token counts as a cost proxy.
- B) The raw number of API calls made, without regard to how many tokens each call used.
- C) Actual per-request token usage — input, output, and cache — attributed to each report.
- D) A flat cost assumption derived from each report's page count rather than its actual token usage, on the theory that longer reports reliably cost proportionally more to generate.

**Question 38.** An engineer writes an automated eval that asserts the report output must exactly match a fixed reference string for a sample quarter, and the eval fails intermittently even though the reports look correct on manual review.

Question: What is the most likely issue with the eval design?

- A) The model is broken in some way and is genuinely producing wrong answers on this quarter.
- B) LLM output is non-deterministic across calls, so exact-string-match is the wrong eval design; check for required content or structure instead.
- C) The eval simply needs a longer reference string to match against.
- D) Raising the temperature setting should resolve these intermittent eval failures.

**Question 39.** Source ledger exports include full raw metadata for every transaction (system IDs, timestamps, internal codes) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix?

- A) Raise `max_tokens` so the pipeline has room to accommodate the extra metadata.
- B) Switch to a model with a larger context window so the metadata bloat matters less.
- C) Prune the source data to relevant fields before it ever enters the prompt.
- D) Run a second Claude call first to summarize the metadata before drafting the actual report.

**Question 40.** For very long consolidated reports, the team notices generated commentary consistently misses details from the middle of the source ledger data while capturing the opening and closing sections well.

Question: What is the most effective mitigation?

- A) Switch to a model with an even larger context window than the one currently used, on the assumption that more raw context capacity alone fixes uneven attention across a long document.
- B) Add an instruction telling the model to "pay equal attention to the whole document."
- C) Put a key-facts summary at the start and organize detail under clear section headers.
- D) Alphabetize the source sections before they're handed to the model for drafting.

**Question 41.** A generated report confidently states a variance driver that, on manual review, never actually appears in the underlying ledger data.

Question: What practice would most help catch this class of error before it reaches finance leadership?

- A) Treat confident, fluent-sounding output as sufficient evidence of correctness by default.
- B) Increase the model's temperature so its answers come across as less confident overall.
- C) Verify key figures and claims against the source data rather than accepting fluency as correctness.
- D) Shorten the report so there is less surface area for an error like this to appear in.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach?

- A) Use schema-constrained tool use instead of a prose instruction to enforce the output structure.
- B) Repeat the same JSON instruction even more emphatically in the prompt.
- C) Post-process every response to strip any text appearing before the first `{`.
- D) Raise `max_tokens` so there's enough room in the response for both the stray free-text preamble and the full JSON object that follows it, without either one getting cut off.

**Question 43.** The team wants to add an exploratory step that scans a client's full historical filings for context before drafting the current report, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach?

- A) Load the entire filing history directly into the main drafting prompt on every single report run, regardless of how much of that history is actually relevant to the current quarter.
- B) Skip historical context entirely, avoiding the bloat risk by not scanning filings at all.
- C) Have a subagent scan the history in an isolated context and return only a distilled summary.
- D) Switch to a model with a large enough context window that the full history always fits.

**Question 44.** For the simplest, most common report type (a single-entity monthly variance summary), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice?

- A) For a simple, high-volume task, zero-shot may be cheaper and sufficient; multi-shot earns its cost on tasks needing precise formatting or edge-case consistency.
- B) Multi-shot prompting is always strictly better than zero-shot, regardless of how simple the task is.
- C) Zero-shot prompting is required by design whenever latency is a consideration at all.
- D) The zero-shot-versus-multi-shot choice has no measurable effect on either cost or latency.

**Question 45.** The reporting prompt has been modified informally by several analysts over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this?

- A) Version prompts as tracked artifacts, similar to code, so changes can be attributed and rolled back.
- B) Lock the prompt file so that no analyst is ever able to change it again.
- C) Restrict prompt access so only one designated analyst is allowed to read it.
- D) Rewrite the entire prompt from scratch on a fixed quarterly schedule going forward.

---

## Scenario D: Claude Code Governance for a Growing Platform Org (Questions 46–60)

Fenwick Platform Engineering supports roughly 90 engineers using Claude Code across dozens of repositories, alongside internal MCP servers for ticketing, deployment status, and internal documentation. As adoption grows, the platform team owns team-wide configuration, CI integration, and security governance for how Claude Code and MCP are used across the org.

---

**Question 46.** A new engineer clones the team's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause?

- A) `CLAUDE.md` requires an explicit `@import` from the project root before it takes effect at all, and without that import line the file is silently ignored on every machine that clones the repo.
- B) The new engineer needs to run `/memory` once to activate memory files on a fresh clone.
- C) The conventions file exceeded a size limit and was silently truncated during load.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine, not in version control.

**Question 47.** A nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause?

- A) The pull requests being reviewed are simply too large for Claude Code to process.
- B) The CI runner's service account lacks permission to call the Claude API at all.
- C) The repository's `CLAUDE.md` file is malformed and fails to parse on load.
- D) The job is missing `-p`/`--print` (headless mode), so it waits for interactive input the CI runner never provides.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix?

- A) Run with `--output-format json` and a `--json-schema` for machine-parseable output.
- B) Harden the existing regex with additional, more permissive fallback patterns for structured output that occasionally drifts.
- C) Post the entire raw output as a single PR comment instead of trying to parse or validate it at all.
- D) Add a stronger prompt instruction telling the model never to deviate from the format, and repeat that instruction at both the start and the end of every single PR review request.

**Question 49.** The team's `/audit-deps` custom command prints thousands of lines of dependency-graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this?

- A) `allowed-tools`, restricting the command to read-only operations only.
- B) `argument-hint`, so developers are nudged to scope the dependency analysis more narrowly before running the command against the entire monorepo.
- C) Removing the `/audit-deps` command from the repository entirely.
- D) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns.

**Question 50.** An internal `/scaffold-service` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail?

- A) Add a warning inside the skill's instructions telling Claude never to run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation, making Bash unavailable.
- C) Require developers to commit their work before running any skill, as a safety net.
- D) Convert the skill into a slash command instead, since commands structurally cannot run tools and therefore could never have touched files outside the intended template directory.

**Question 51.** An engineer needs to understand how authorization flows across a large, unfamiliar codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach?

- A) Use the Explore subagent for discovery, so verbose exploration runs in an isolated context and only a summary returns.
- B) Read every file in the codebase in a single pass, prioritizing thoroughness over context usage.
- C) Skip exploration entirely and infer the authorization architecture from directory names alone.
- D) Split the exploration work across two separate terminal windows running in parallel.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do?

- A) Start a brand-new session and rely on memory of what was learned during discovery, rather than trying to preserve any of it inside the current, nearly-full context window.
- B) Run `/compact` to summarize the conversation and free context while preserving key findings.
- C) Delete the project `CLAUDE.md` file temporarily to free up context space.
- D) Keep working as-is; Claude automatically discards irrelevant context on its own.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal MCP tool, and writes a report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next?

- A) The step between receiving the MCP tool's valid data and producing the final report.
- B) Re-read the config file a second time, since that was the earliest step in the pipeline.
- C) The network connection to the MCP server, since it's the most technically complex step involved.
- D) Nowhere in particular — a wrong report with correct inputs just means the task hit an unrelated fluke and should simply be re-run from the beginning without further investigation.

**Question 54.** A deployment-tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step?

- A) Assume the failure is a model problem right away and start rewriting the prompt before checking anything about the actual request or response the integration sent.
- B) Switch to a different model entirely and see whether the same failure persists.
- C) Restart the CI runner and try again, since deployment failures are rarely deterministic anyway.
- D) Examine the trace of what was sent and received to isolate integration-layer versus model-output failure.

**Question 55.** The internal ticketing system needs to be reachable from Claude Code sessions across the whole engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach?

- A) Build an MCP server exposing ticketing operations as tools, shared and maintained centrally across the org.
- B) Have each team paste their own ticketing API credentials directly into their team's `CLAUDE.md`.
- C) Hard-code the ticketing logic separately into each team's own custom skill.
- D) Ask each engineer to curl the ticketing API by hand whenever a ticket needs updating.

**Question 56.** An MCP server for internal documentation exposes both a `search_docs` tool and a way for agents to see what documentation exists without an exploratory search call.

Question: What is the second capability an example of?

- A) An MCP tool, functionally identical in purpose to `search_docs`.
- B) A built-in tool the platform provides to every agent automatically.
- C) An MCP resource — content/catalog visibility distinct from a tool that performs an action.
- D) A Claude Code Skill packaged and distributed alongside the MCP server, bundled together so both ship as part of the same internal documentation release.

**Question 57.** The team is deciding whether an internal MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision?

- A) A local stdio server is always faster than a remote one, regardless of deployment context, network topology, or how many developers actually need to reach it.
- B) MCP only supports a single communication pattern, so there is no real decision to make here.
- C) A remote-hosted server structurally cannot expose tools, only resources.
- D) Where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for shared services.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix?

- A) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so it isn't committed.
- B) Base64-encode the token in place before committing the file again.
- C) Move the whole `.mcp.json` file into a separate private repository instead.
- D) Rotate the token on a weekly schedule instead of removing it from the file.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles?

- A) Add a hook that logs calls to the broad-access tools so any misuse can be reviewed after the fact, without actually narrowing what those tools are still able to do to ticket data.
- B) Leave access as it is for now, since no actual misuse has been observed yet.
- C) Scope the exposed tools down to only the operations actual workflows require.
- D) Add a confirmation prompt in front of any deletion operation before it executes.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific reporting workflow used by a single small team, versus a widely-reused authentication-checking capability needed by every agent across the org.

Question: How should each be built?

- A) Both as MCP servers, on the assumption MCP is the correct choice for any capability that's shared.
- B) The reporting workflow as a Skill or custom tool scoped to that team; the auth check as an MCP server or built-in tool maintained centrally.
- C) Both as Skills, on the assumption Skills are always the reusable option.
- D) Both as built-in tools, since built-in tools require the least setup effort of any option.

---
# Answer Key — Practice Exam 10

**Quick key:** 1-A, 2-B, 3-A, 4-B, 5-D, 6-B, 7-A, 8-B, 9-A, 10-B, 11-B, 12-D, 13-D, 14-D, 15-C, 16-C, 17-A, 18-C, 19-C, 20-C, 21-C, 22-D, 23-D, 24-B, 25-A, 26-B, 27-B, 28-D, 29-D, 30-B, 31-D, 32-B, 33-C, 34-C, 35-A, 36-D, 37-C, 38-B, 39-C, 40-C, 41-C, 42-A, 43-C, 44-A, 45-A, 46-D, 47-D, 48-A, 49-D, 50-B, 51-A, 52-B, 53-A, 54-D, 55-A, 56-C, 57-D, 58-A, 59-C, 60-B

---

**1. A** — The tool-use loop must key off `stop_reason`: continue while it's `tool_use` (execute tools, return results), stop at `end_turn`. A fixed call cap (B) is a backstop at best; text-scanning (C) and latency (D) don't indicate completion.

**2. B** — Tool results must be appended as a `tool_result` block referencing the `tool_use_id`, then the conversation resent so the model can incorporate it. A misuses the system prompt for turn-level data; C keeps the result from the model; D discards conversational state unnecessarily.

**3. A** — A safety-critical rule affecting customer-facing infrastructure needs deterministic enforcement via a hook that blocks the call outright. B, C, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. B** — Forcing tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (D) guarantees some call but not which one; A and C are probabilistic.

**5. D** — Removing the unrelated tools shrinks the candidate set Aegis reasons over, directly improving selection reliability. A adds prompt overhead without removing the underlying bloat; B doesn't touch selection reliability; C is cosmetic reordering.

**6. B** — Structured error metadata (category, retryable flag, description) lets Aegis respond appropriately to each failure kind. Blind retry (A) wastes calls on non-retryable failures; asking the model to guess (C) is worse than the tool reporting it; D just lowers frequency without fixing the missing information.

**7. A** — "No matching history" is a valid empty result, not a failure — return success with an empty set. B hides real signal by ending the conversation; C adds an unnecessary extra tool call; D patches around the symptom while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools and order depend on intermediate findings are the core case for model-driven selection over a rigid sequence. A, C, and D are unsupported claims about cost or capability.

**9. A** — A narrowly-scoped subagent holding only the paging tool and explicit criteria minimizes accidental paging while the main agent reasons about unrelated tools. B overgeneralizes a hard requirement that doesn't exist; C and D are unsupported technical claims.

**10. B** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis rather than raw logs. A and C don't address the root accumulation problem; D removes needed capability outright.

**11. B** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately without reconstruction. A forces the human to dig through a raw transcript; C omits diagnostic context entirely; D conveys mood, not facts.

**12. D** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, B, and C are unsupported absolute claims about what each option can reach or how secure it is.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, implementation language, or a runtime deadline.

**14. D** — Tool/subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent holds. A, B, and C misdiagnose the actual cause.

**15. C** — A per-host call-count hook is the only option here that deterministically guarantees the limit; A, B, and D remain probabilistic prompt-level guidance the model can still violate.

**16. C** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost at all; A and D risk quality or truncate output without touching the actual cost lever.

**17. A** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. B, C, and D misidentify the actual limitation the loop runs into.

**18. C** — Streaming supports incremental rendering, which is what reduces perceived latency for a real-time progress UI. A is simply the wrong API for this use case; B and D don't address perceived latency at all.

**19. C** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, cutting both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without touching caching.

**20. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance; A removes the field's value entirely rather than fixing the reporting.

**21. C** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and D all discard information or guess at an answer.

**22. D** — Tool use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated up front; C swaps one fragile text format for another.

**23. D** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top of it. A, B, and C misdiagnose or abandon a mechanism that is otherwise working correctly.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. C and D don't touch the actual data-quality bottleneck; A discards otherwise-processable documents unnecessarily.

**25. A** — Concurrent tool/API calls require async, non-blocking request handling in the integration layer itself. B, C, and D all misstate how concurrency is actually achieved here.

**26. B** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — that's the realistic expectation, not identical latency or missing features.

**27. B** — Thinking content is a distinct block type that must be handled, and typically preserved, separately from final answer text across multi-turn tool-use conversations. A, C, and D mishandle or misdescribe this.

**28. D** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-document cost breakdown. A, B, and C all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. B** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. C is unreliable prompt-level mitigation; A and D are unrelated levers that don't address cross-contamination between clients.

**31. D** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and B overspend or ignore task fit; C is an unrelated consideration entirely.

**32. B** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, C, and D apply broad, costly fixes to what is a narrow problem.

**33. C** — Pinning a version and deliberately testing before upgrading avoids unattributed behavior drift reaching production. A accepts avoidable risk; B and D are overcorrections unrelated to the actual fix needed.

**34. C** — Concrete few-shot examples are the most effective lever for consistent structure once prose alone hasn't worked. A repeats a failed approach; B and D don't reliably fix structural consistency.

**35. A** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. B, C, and D all misstate this relationship.

**36. D** — Stable instructions first, ideally as a cacheable prefix, with variable content after, improves both consistency (clear role separation) and caching. A, B, and C misstate the actual effect of ordering.

**37. C** — Actual per-request token usage (input/output/cache) attributed per report gives an accurate cost picture; estimates from average length or unrelated proxies (A, B, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on genuinely correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism at all.

**39. C** — Pruning to relevant fields before data ever enters the prompt removes the actual bloat at its source. A and B work around the symptom without reducing waste; D adds an extra call and complexity for a problem simple filtering solves directly.

**40. C** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and D don't touch the underlying attention pattern.

**41. C** — Verifying key claims against the source data catches confident-but-wrong output that fluency alone would let through unnoticed. A is the failure mode itself, stated as a practice; B and D don't address correctness.

**42. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift into a preamble. B and C are workarounds for a problem that can be structurally eliminated; D doesn't fix the preamble issue at all.

**43. C** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still surfacing relevant findings. A and D reintroduce the bloat risk; B discards potentially useful context entirely.

**44. A** — Task simplicity and volume should drive the zero-shot-versus-multi-shot tradeoff; multi-shot earns its cost on tasks needing format or edge-case consistency, which a simple high-volume task may not need. B and C are absolute claims that don't hold generally; D is false.

**45. A** — Versioning prompts like code enables attribution and rollback when a quality regression appears. B, C, and D are impractical overcorrections that don't provide the actual missing capability, which is change tracking.

**46. D** — User-level `CLAUDE.md` never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how `CLAUDE.md` loading actually works.

**47. D** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. A, B, and C would typically produce different, more specific failure signatures instead.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. B, C, and D are reactive fixes or abandon the structured-comment requirement altogether.

**49. D** — `context: fork` isolates the verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A restricts capability, not output destination; B narrows scope but doesn't isolate output; C removes useful functionality outright.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic, and the violation already happened despite instructions; C mitigates damage after the fact rather than preventing it; D is a false claim about slash commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly instead of preserving it; C guesses instead of investigating; D doesn't meaningfully share context between two separate windows.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve here. A discards findings outright; C frees trivial space while losing standards; D describes behavior that doesn't actually exist.

**53. A** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. B and C re-check already-verified steps; D skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and B guess without diagnosis; C doesn't investigate the actual cause at all.

**55. A** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. B, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and D mischaracterize this capability.

**57. D** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and C are false or oversimplified claims about MCP's communication patterns.

**58. A** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. B is easily reversible obfuscation, not real protection; C and D don't remove the exposed credential from history or ongoing risk.

**59. C** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and D are detective or compensating controls; B accepts unnecessary risk outright.

**60. B** — Matching each capability's actual reuse scope — Skill or custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 10.*
