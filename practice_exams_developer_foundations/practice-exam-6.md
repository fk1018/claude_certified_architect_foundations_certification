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

- A) Whether the assistant's text includes phrases like "incident resolved."
- B) A hardcoded limit of eight tool calls per session.
- C) Whether `notify_customer` has been called yet.
- D) The `stop_reason` on the response: keep looping while it is `"tool_use"`, and stop once it becomes `"end_turn"`.

**Question 2.** After Warden calls `rotate_api_key` and the harness executes it, what is required for Warden to reason correctly about the outcome on its next turn?

- A) Log the rotation to the audit database and let the next prompt reference it by ticket number.
- B) Summarize the rotation result in a fresh system prompt for a new session.
- C) Append the rotated key's confirmation to the end of the system prompt so it persists.
- D) Add a `tool_result` block keyed to the original `tool_use` ID into the conversation and resend the full conversation to the model.

**Question 3.** Kestrel's policy requires a human approve any `restart_container` call targeting a customer's primary database container. The system prompt states this rule prominently, but audits show a handful of autonomous restarts on database containers anyway.

Question: What is the most reliable fix? (Select ONE response.)

- A) Move the rule to the very first line of the system prompt.
- B) Add several few-shot transcripts showing Warden escalating instead of restarting.
- C) Lower temperature so Warden follows written policy more literally.
- D) Add a hook that intercepts `restart_container` calls and blocks any targeting a database container unless a human-approval flag is already set.

**Question 4.** The SRE team wants Warden to always call `check_node_health` first on every incident, with zero exceptions, before considering any other tool.

Question: What is the most reliable way to enforce this? (Select ONE response.)

- A) State the ordering requirement clearly in the system prompt.
- B) Set `tool_choice: "any"` on the first request so some tool call is guaranteed.
- C) Set `tool_choice` to force `check_node_health` specifically on the first request, then revert to normal tool choice afterward.
- D) Provide five few-shot examples that all open with `check_node_health`.

**Question 5.** Warden currently has 19 tools registered, including several that belong to unrelated teams (billing adjustments, marketing-email suppression, feature-flag rollout). Tool selection accuracy has degraded noticeably.

Question: What is the single most direct fix? (Select ONE response.)

- A) Remove or scope out the tools that don't belong to Warden's incident-response responsibility.
- B) Add a "primary tools" note to the system prompt listing which ones matter most.
- C) Increase `max_tokens` so Warden has more room to think through tool choice.
- D) Rename the unrelated tools with less appealing descriptions so Warden avoids them.

**Question 6.** `check_node_health` currently returns the bare string `"unavailable"` whether the node doesn't exist, the health-check agent timed out, or Warden lacks permission to query it. Warden's downstream behavior is inconsistent across these cases.

Question: What is the best fix? (Select ONE response.)

- A) Return structured error data: a category (not-found, timeout, permission), a retryable flag, and a short human-readable description.
- B) Have Warden guess the cause from surrounding conversation context.
- C) Wrap every call in an automatic three-retry policy regardless of cause.
- D) Extend the health-check agent's timeout so timeouts occur less often.

**Question 7.** When `check_node_health` finds a node exists but simply has no recent metrics (a quiet, healthy node), it currently returns an error. Warden then apologizes for a "system issue" and repeats the query.

Question: What should change? (Select ONE response.)

- A) Return a successful response with an empty/no-recent-metrics result, reserving errors for genuine access failures.
- B) Add a system prompt note explaining this error usually just means the node is quiet.
- C) Have Warden call `page_sre` automatically whenever this happens.
- D) Add a hook that silently ends the turn when this error appears.

**Question 8.** An engineer proposes replacing Warden's tool reasoning with a fixed script: always call `check_node_health`, then `restart_container`, then decide, arguing this is more predictable.

Question: Why does model-driven tool selection remain the better fit here? (Select ONE response.)

- A) Incidents vary in cause and severity, and the right next tool depends on what earlier tool results revealed — a fixed sequence can't adapt to that.
- B) Fixed sequences technically cannot call custom tools registered with the SDK.
- C) Model-driven selection is always cheaper because it uses fewer tokens.
- D) A fixed script would require rewriting all of Warden's tool schemas.

**Question 9.** The team is deciding whether `page_sre` (which wakes a human at 3 a.m.) should live directly on Warden's main tool list, or be delegated to a small, narrowly-scoped subagent whose only job is deciding whether paging criteria are met.

Question: What is the strongest argument for the narrowly-scoped subagent? (Select ONE response.)

- A) A subagent given only the paging tool and explicit escalation criteria is less likely to page unnecessarily while Warden is reasoning about unrelated diagnostic tools.
- B) Subagents are required by the SDK for any tool with real-world side effects.
- C) Subagents always execute tool calls faster than the main agent.
- D) The main agent's context window is too small to hold the paging tool's schema.

**Question 10.** During a drawn-out incident, Warden's context fills with verbose raw health-check output, crowding out room for reasoning about root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Delegate health-check exploration to a subagent that returns only a distilled summary of relevant findings, keeping the main context focused on diagnosis.
- B) Truncate every tool result to its first 20 lines automatically.
- C) Raise `max_tokens` so Warden's replies can be longer.
- D) Turn off health-check querying and rely solely on customer reports.

**Question 11.** Warden escalates an incident to a human on-call engineer after 25 minutes of tool calls, but the engineer has no easy way to see what Warden already tried.

Question: What should the escalation include? (Select ONE response.)

- A) The full raw tool-call transcript, so nothing is omitted.
- B) Just the final error, since the human will re-investigate anyway.
- C) A tone/urgency rating generated from the conversation.
- D) A structured handoff: what was tried, what was found, and a recommended next action.

**Question 12.** Kestrel is deciding between running Warden through a hosted, Anthropic-managed execution environment versus self-hosting the agent harness on its own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Self-hosted agents cannot register custom tools.
- B) Operational control (self-hosted) versus operational burden (managed) — the set of tools Warden can call doesn't differ based on hosting choice.
- C) Managed execution is inherently less secure than self-hosting.
- D) Managed environments cannot reach Kestrel's private network at all.

**Question 13.** A junior engineer asks whether Warden's incident triage should be built as a fixed workflow or as an agent.

Question: What should decide this? (Select ONE response.)

- A) Whether the implementation language is Python or TypeScript.
- B) Whether the task is well-defined and repeatable, or instead high-ambiguity with a path that depends on intermediate findings.
- C) Whether the task must finish in under one minute.
- D) Whether more than five tools are involved.

**Question 14.** A proposed "log-correlation subagent" has the description "Looks at logs." Warden rarely delegates to it even when correlating logs across services is clearly the right move.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent's temperature is too low to be considered for delegation.
- B) Subagents must be listed in `.mcp.json` before they can be delegated to.
- C) The description drives delegation decisions; rewriting it to specifically state what the subagent does and when to use it will most directly fix the under-delegation.
- D) The subagent needs more tools added to its definition.

**Question 15.** Kestrel wants a hard, non-negotiable guarantee that `restart_container` is never called more than twice on the same container within a single incident, regardless of what Warden decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A clearly worded two-call limit in the system prompt.
- B) A note about the limit inside the tool's description field.
- C) Few-shot transcripts showing an agent stopping after two restarts.
- D) A hook that tracks per-container call counts and blocks the tool call once the limit is reached.

---

## Scenario B: Batch Invoice-Extraction Pipeline for a Logistics Company (Questions 16–30)

Meridian Freight Logistics runs a nightly pipeline that extracts structured line-item data from carrier invoices — tens of thousands per night — plus a smaller interactive flow where a billing clerk uploads a single disputed invoice and waits for results. Some invoices are scanned images with degraded OCR, and the pipeline is being expanded to run across multiple regional cloud vendors.

---

**Question 16.** The nightly job processes 60,000 carrier invoices with no user waiting on any individual result, and no step needs Claude to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- B) The synchronous Messages API, run across as many parallel threads as the rate limit allows.
- C) The synchronous Messages API with `max_tokens` set to the minimum possible value.
- D) The synchronous Messages API paired with the smallest available model.

**Question 17.** An engineer wants to add an "extract, validate line totals, retry any failed fields" loop to the nightly pipeline and proposes running that entire loop inside the Batch API to keep the cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't accept system prompts.
- B) Batch requests are capped at a context window too small for multi-page invoices.
- C) The Batch API can't execute a validation tool call mid-request and feed the result back to the model within a single request — which this iterative loop requires.
- D) The 24-hour batch window makes any retry logic technically impossible.

**Question 18.** The interactive single-invoice flow shows the billing clerk a live, incrementally-updating view of the extraction as it happens.

Question: What technique best supports this? (Select ONE response.)

- A) Polling the Batch API's status endpoint every second.
- B) Streaming, so the UI can render partial output as it arrives and reduce perceived latency.
- C) Raising `max_tokens` so the full response completes sooner.
- D) The Batch API, since it's optimized for real-time feedback.

**Question 19.** Every extraction request sends the same 5,500-token field-schema and carrier-code reference, followed by invoice-specific text that varies per request.

Question: What single change most directly reduces both latency and cost across the whole pipeline? (Select ONE response.)

- A) Move the schema reference into a few-shot example instead of prose.
- B) Place the stable schema/instructions first, enable prompt caching on that prefix, and put the varying invoice text last.
- C) Truncate the carrier-code reference to the most common carriers only.
- D) Switch to the smallest available model regardless of extraction quality impact.

**Question 20.** The schema requires a `fuel_surcharge` field on every invoice line. Many lines have no surcharge, and the model has started inventing small nonzero values instead of reporting its absence.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field entirely so the issue can't occur.
- B) Add a prompt instruction warning against invented values.
- C) Lower temperature to reduce fabricated values.
- D) Make `fuel_surcharge` nullable so its true absence can be reported.

**Question 21.** Two extraction passes on the same invoice disagree on a weight field — one reads 2,140 lb, the other 2,410 lb — and there is no way to resolve the discrepancy from the surrounding text.

Question: What should the pipeline do? (Select ONE response.)

- A) Always trust whichever pass ran first.
- B) Average the two readings.
- C) Flag the field for human review with both candidate values and their source, rather than silently picking one.
- D) Discard the invoice entirely as unreliable.

**Question 22.** The pipeline's free-text JSON extraction output fails to parse cleanly on roughly 4% of runs, crashing the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Ask for YAML instead, since it tolerates minor formatting drift better.
- B) Add a JSON-repair library step before parsing.
- C) Retry with "return valid JSON only" appended to the prompt whenever a parse fails.
- D) Define a tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of parsing free text.

**Question 23.** After switching to strict schema-constrained tool use, output always parses successfully, but some line-item amounts still don't sum to the invoice's stated total.

Question: What should you conclude and do? (Select ONE response.)

- A) Strict schemas guarantee syntactic validity, not semantic correctness — add a separate validation step checking totals against summed line items.
- B) `max_tokens` must be too low, truncating output mid-generation.
- C) The schema needs stricter numeric types.
- D) Abandon tool use and return to free-text extraction with manual review.

**Question 24.** A subset of incoming invoices are scanned images with a badly damaged text layer, and the current pipeline sends only the OCR'd text to Claude, with poor results on the worst scans.

Question: What is the most direct fix? (Select ONE response.)

- A) Send the invoice image itself as a content block alongside the extraction instructions, using native vision input instead of relying solely on OCR text.
- B) Reject scanned invoices from the pipeline entirely.
- C) Increase `max_tokens` so the model can work harder on the degraded text.
- D) Switch to a larger model, since bigger models always parse noisy OCR better.

**Question 25.** The pipeline needs to process six sections of a very long consolidated freight manifest concurrently to keep total latency reasonable.

Question: What must the integration layer support? (Select ONE response.)

- A) Streaming, since concurrency is only possible with streaming enabled.
- B) A single request with all six sections concatenated, relying on internal parallelization.
- C) The Batch API, as the only way to issue more than one request at a time.
- D) Async/concurrent request handling, so multiple API calls can be in flight simultaneously without blocking on one another.

**Question 26.** Meridian plans to run the same extraction pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted offering for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) Batch processing will be unavailable on every third-party vendor integration.
- C) Extraction accuracy and latency are guaranteed to be identical across vendors.
- D) Prompts and schemas need to be rewritten from scratch for each vendor.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task involving several tool-use turns.

Question: What must the integration layer handle correctly? (Select ONE response.)

- A) Convert thinking content into an additional tool call automatically.
- B) Discard thinking content only on turns that also involve a tool call.
- C) Ignore thinking content entirely, since it never influences later turns.
- D) Treat the thinking content block as distinct from final answer text, and typically preserve it appropriately across the multi-turn conversation.

**Question 28.** Finance asks for accurate per-invoice cost accounting, but the current model only estimates cost from average prompt length.

Question: What should the improved model account for separately? (Select ONE response.)

- A) Only output tokens, treating input as effectively free.
- B) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- C) A flat per-invoice fee regardless of token usage.
- D) Only cache read tokens, since caching dominates overall cost.

**Question 29.** A new engineer argues code review can be skipped on the extraction pipeline's surrounding application code now that Claude does the extraction, since "the model is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Only the prompt needs review; the surrounding code is low-risk by definition.
- B) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- C) Review is unnecessary once evals are passing.
- D) Review can be skipped for any code that primarily calls an external API.

**Question 30.** A single long-running session processes invoice batches for several unrelated carrier clients across a full shift, and the team notices the model increasingly referencing details from an earlier, unrelated client's invoices.

Question: What is the best fix? (Select ONE response.)

- A) Ask the model to "ignore earlier invoices" at the start of each new client's batch.
- B) Increase the context window so more history fits without confusion.
- C) Lower temperature to reduce cross-referencing.
- D) Start a fresh session (or `/compact`) at natural task boundaries, such as between different clients' batches, rather than accumulating unrelated context.

---

## Scenario C: Prompt and Context Engineering for a Financial-Reporting Generator (Questions 31–45)

Ashcroft & Vale, a mid-size accounting firm, runs a service that turns structured quarterly ledger data into narrative sections of client-facing financial reports — hundreds of reports per week during close season. The team is tuning model selection, prompt structure, and context handling to keep cost, latency, and factual reliability under control.

---

**Question 31.** Most report sections are short, formulaic narrative (e.g., "revenue summary") generated at high volume, where speed and cost per section matter far more than rare, deeply complex cases.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) Whichever tier is cheapest per token, independent of task fit.
- B) The same tier used for the firm's hardest audit-reasoning work, for consistency.
- C) A fast, low-latency tier suited to high-volume/low-complexity generation, reserving a higher tier only for sections flagged as complex.
- D) The highest-capability tier available, to guarantee quality on every section.

**Question 32.** A small fraction of report sections require multi-step reasoning (reconciling a multi-entity intercompany transfer) where the fast default model produces shallow, occasionally wrong narrative.

Question: What is the most targeted fix? (Select ONE response.)

- A) Increase `max_tokens` across the board for every section.
- B) Switch every report section to the highest-capability tier to be safe.
- C) Route only the flagged complex sections to a higher-capability tier or one with extended/adaptive thinking, keeping the fast path for everything else.
- D) Add more few-shot examples to the fast model's prompt for all sections.

**Question 33.** The service currently always calls "whatever model is latest." After a routine model update, report tone and section structure shifted noticeably with no code change on Ashcroft & Vale's side.

Question: What should the team do differently? (Select ONE response.)

- A) Disable prompt caching to prevent drift.
- B) Nothing — behavioral drift across model releases is expected and needs no process.
- C) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- D) Permanently roll back to the oldest available model version.

**Question 34.** Report sections need a consistent structure (headline figure, drivers, comparison to prior period, outlook), but detailed prose instructions describing that structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Ask the model to restate the structure before writing the section.
- B) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- C) Lower temperature to zero.
- D) Write an even longer, more detailed prose description of the structure.

**Question 35.** A ledger detail input is unusually long (a full year of transaction-level entries), and the team wants a maximally detailed narrative output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) Long outputs are always truncated regardless of context window size.
- B) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- C) Output length has no bearing on latency.
- D) Input and output tokens are budgeted entirely independently of one another.

**Question 36.** The report-generation prompt currently places the specific client's ledger data before the general narrative-writing instructions and formatting rules in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last always improves how carefully the model attends to them.
- B) Stable, role-defining instructions belong first (or in the system prompt) to form a consistent, cacheable prefix, while the client-specific ledger data — which varies — should come after.
- C) Reordering affects cost only, never consistency.
- D) Order has no measurable effect on either consistency or caching.

**Question 37.** Finance wants an exact per-report cost figure for the narrative-generation service, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead? (Select ONE response.)

- A) A flat cost assumption based on ledger line count.
- B) Actual token usage per request — input, output, and cache — attributed per report, rather than an estimate from average length.
- C) Number of API calls only, regardless of token volume.
- D) Wall-clock latency per report, used as a cost proxy.

**Question 38.** An engineer writes an automated eval asserting that a report section's output must exactly match a fixed reference string, and the eval fails intermittently even though manual review shows the generated sections are correct.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) Temperature should be raised to fix the intermittent failures.
- B) LLM output is inherently non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation and check for required content/structure instead.
- C) The reference string needs to be longer.
- D) The model is broken and producing incorrect narrative.

**Question 39.** Ledger exports include full raw metadata for every transaction (internal system IDs, timestamps down to the millisecond, batch codes) that bloats the prompt with mostly-irrelevant data.

Question: What is the best fix? (Select ONE response.)

- A) Have a second Claude call summarize the raw metadata before the main narrative call.
- B) Switch to a model with a larger context window so the bloat matters less.
- C) Prune the export to relevant financial fields before it enters the prompt, rather than passing raw dumps.
- D) Raise `max_tokens` to accommodate the extra metadata.

**Question 40.** For unusually long report sections drawing on a full year of ledger history, the generated narrative consistently captures the opening and closing quarters well but misses details from the middle of the year.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Add an instruction telling the model to "weigh all quarters equally."
- B) Switch to a model with an even larger context window.
- C) Put a brief key-facts overview at the start of the input and organize detailed quarter-by-quarter data under clear section headers, countering the tendency to attend most to the beginning and end of long inputs.
- D) Sort the ledger entries alphabetically by account name before summarizing.

**Question 41.** A generated report section confidently states a revenue driver that, on manual review, doesn't actually appear anywhere in the underlying ledger data.

Question: What practice would most help catch this class of error before it reaches a client? (Select ONE response.)

- A) Shorten the section so there's less room for errors.
- B) Raise temperature so the model sounds less confident.
- C) Apply defensive parsing and skepticism toward confident output — verify key claims against the source ledger data rather than accepting fluency as correctness.
- D) Trust well-written, fluent-sounding output as evidence of correctness by default.

**Question 42.** Prose instructions telling the model to "always output valid structured JSON for the metrics block with these exact fields" still occasionally produce a free-text preamble before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Increase `max_tokens` so there's room for both the preamble and the JSON.
- B) Repeat the JSON instruction more emphatically at the end of the prompt.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Post-process every response to strip text before the first `{`.

**Question 43.** The team wants to add a step that scans a client's prior four quarters of reports for context before drafting the current one, but worries this exploration will bloat the main prompt with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load all four prior quarters' full reports directly into the main prompt every time.
- B) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main drafting step.
- C) Increase the context window so the full history always fits.
- D) Skip historical context entirely to avoid the bloat risk.

**Question 44.** For the simplest, most common section type (a one-line cash-position statement), the team is deciding between a zero-shot prompt and a multi-shot prompt with several worked examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Zero-shot is required whenever latency matters at all.
- B) Multi-shot is always strictly better, regardless of task simplicity.
- C) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- D) The choice has no effect on either cost or latency.

**Question 45.** The report-generation prompt has been informally modified by several analysts over close seasons with no record of what changed or why, making a recent quality regression hard to diagnose.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treat prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Rewrite the prompt from scratch every quarter.
- C) Allow only one designated analyst to ever read the prompt.
- D) Lock the prompt so it can never be changed again.

---

## Scenario D: Claude Code Governance for a Growing Platform Org (Questions 46–60)

Corvid Systems has grown from 12 to 85 engineers in a year. Its platform team now owns Claude Code standards across the org, several internal MCP servers (ticketing, deployment status, internal wiki), and a CI pipeline that runs Claude Code headlessly for automated PR review.

---

**Question 46.** A newly hired engineer clones a Corvid repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- B) The conventions file exceeded a size limit and was silently truncated.
- C) The new engineer needs to run `/memory` to activate memory files.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level configuration that never travels through version control.

**Question 47.** Corvid's nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The repository's CLAUDE.md is malformed.
- C) The pull requests being reviewed are too large for Claude Code to process.
- D) The CI runner lacks permission to call the Claude API.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Post the entire raw output as a single PR comment instead of parsing it.
- B) Harden the regex with more permissive fallback patterns.
- C) Add a stronger prompt instruction never to deviate from the format.
- D) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.

**Question 49.** Corvid's `/audit-deps` custom command prints thousands of lines of dependency-graph data, and engineers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `argument-hint`, so engineers scope the analysis more narrowly.
- B) `allowed-tools`, restricting the command to read-only operations.
- C) Removing the command entirely.
- D) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.

**Question 50.** Corvid's internal `/scaffold-module` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Convert the skill into a slash command, since commands cannot run tools.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands.
- C) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- D) Require engineers to commit their work before running any skill.

**Question 51.** An engineer needs to understand how permission checks flow through a large, unfamiliar service before making a change, and worries that reading dozens of files will exhaust context before implementation even begins.

Question: What is the best approach? (Select ONE response.)

- A) Split the work across two separate terminal windows.
- B) Read every file in the service in one pass to be thorough.
- C) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- D) Skip exploration and infer the architecture from directory names.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Delete the project CLAUDE.md temporarily to free context space.
- B) Continue working; Claude automatically discards irrelevant context.
- C) Start a brand-new session and rely on memory of what was learned.
- D) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal MCP deployment-status tool, and writes a rollout report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) The step between receiving the MCP tool's valid data and producing the final report — since the inputs were confirmed correct, the divergence most likely happened in how that data was reasoned about or transformed afterward.
- B) The network connection to the MCP server, since that's the most complex step.
- C) Re-read the config file again, since that's the earliest step.
- D) Nothing — a wrong report with correct inputs means the task should simply be re-run.

**Question 54.** A deployment-status integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Restart the CI runner and try again.
- B) Switch to a different model to see if the failure persists.
- C) Assume it's a model problem and rewrite the prompt.
- D) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.

**Question 55.** The internal ticketing system needs to be reachable from Claude Code sessions across all of Corvid's engineering teams, not just one, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Ask each engineer to curl the ticketing API manually when needed.
- B) Build an MCP server exposing ticketing operations as tools, shared across the org.
- C) Hard-code ticketing logic into each team's custom skill separately.
- D) Have each team paste ticketing API credentials into their own CLAUDE.md.

**Question 56.** Corvid's internal wiki MCP server exposes both a `search_wiki` tool and a way for agents to see what pages exist without making an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) A built-in tool provided by the platform automatically.
- B) A Claude Code Skill.
- C) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- D) An MCP tool, functionally identical to `search_wiki`.

**Question 57.** Corvid's platform team is deciding whether an internal MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) MCP only supports one communication pattern, so there's no real decision to make.
- B) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- C) Remote servers cannot expose tools, only resources.
- D) stdio servers are always faster regardless of deployment context.

**Question 58.** Corvid's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Rotate the token weekly instead of removing it from the file.
- B) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret isn't committed to version control.
- C) Base64-encode the token before committing it.
- D) Move `.mcp.json` to a private repository instead.

**Question 59.** An audit finds several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow at Corvid requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Leave access as-is, since no misuse has been observed yet.
- C) Add a confirmation prompt before any deletion.
- D) Add logging so misuse can be reviewed after the fact.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific release-notes workflow used by a single small team, versus a widely-reused permission-check capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) The one-off release-notes workflow as a Skill or custom tool scoped to that team; the widely-reused permission-check capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- B) Both as MCP servers, since MCP is the correct choice for any shared capability.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key

**Quick key:** 1-D, 2-D, 3-D, 4-C, 5-A, 6-A, 7-A, 8-A, 9-A, 10-A, 11-D, 12-B, 13-B, 14-C, 15-D, 16-A, 17-C, 18-B, 19-B, 20-D, 21-C, 22-D, 23-A, 24-A, 25-D, 26-A, 27-D, 28-B, 29-B, 30-D, 31-C, 32-C, 33-C, 34-B, 35-B, 36-B, 37-B, 38-B, 39-C, 40-C, 41-C, 42-C, 43-B, 44-C, 45-A, 46-D, 47-A, 48-D, 49-D, 50-C, 51-C, 52-D, 53-A, 54-D, 55-B, 56-C, 57-B, 58-B, 59-A, 60-A

---

**1. D** — The loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text keywords (A) are unreliable, a call-count cap (B) is only a backstop, and waiting on a specific tool (C) doesn't reflect turn completion generally.

**2. D** — Tool results must be attached as a `tool_result` block referencing the original `tool_use` ID and the full conversation resent so the model can incorporate it. Logging elsewhere (A) keeps the result out of the model's reasoning; C misuses the system prompt for turn-level data; D-as-new-session (labeled B here) discards useful state unnecessarily.

**3. D** — A safety-critical rule needs deterministic enforcement via a hook that blocks the call outright; prompt placement (A), few-shot examples (B), and temperature (C) all remain probabilistic compliance, which is exactly what's failing.

**4. C** — Forcing tool choice to a specific tool on the first turn guarantees it runs first; normal choice resumes afterward. `tool_choice: "any"` (B) guarantees a call but not which one; A and D remain probabilistic.

**5. A** — Removing tools outside the agent's actual responsibility directly shrinks the candidate set it must reason over, which is the direct fix for degraded selection accuracy. B adds prompt overhead without removing the bloat; C and D don't address the root cause.

**6. A** — Structured error metadata (category, retryable flag, description) lets the agent respond appropriately to each distinct failure mode. Guessing (B) is strictly worse than the tool reporting it; blanket retries (C) waste calls on non-retryable failures; D reduces frequency without adding missing information.

**7. A** — A quiet node with no recent metrics is a valid empty result, not a failure, so it should return success with an empty payload. B patches symptoms while the underlying conflation remains; C and D don't fix the misclassification itself.

**8. A** — Incident cause and severity vary, and the right next tool depends on what earlier results revealed — exactly the case model-driven selection is built for. B, C, and D are unsupported or false technical claims.

**9. A** — A narrowly-scoped subagent with only the paging tool and explicit criteria minimizes unnecessary paging while the main agent handles unrelated tools. B, C, and D are unsupported absolute claims about subagents.

**10. A** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis instead of raw output. B and C are blunt workarounds; D removes needed capability.

**11. D** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately without reconstructing a transcript. A is unfiltered raw data; B omits diagnostic context; C conveys mood, not facts.

**12. B** — The real tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between managed and self-hosted deployments. A, C, and D are unsupported absolute claims.

**13. B** — Task predictability versus dependency on intermediate findings is the deciding factor between a fixed workflow and an agent, not language, runtime speed, or tool count.

**14. C** — Subagent/tool descriptions drive delegation decisions; a vague description causes under-delegation regardless of tool count. A, B, and D misdiagnose the actual cause.

**15. D** — A per-container call-count hook is the only mechanism that deterministically guarantees the limit; A, B, and C remain probabilistic prompt-level guidance.

**16. A** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost; C and D risk quality or truncate output without addressing the real cost lever.

**17. C** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and D misidentify the actual limitation.

**18. B** — Streaming supports incremental rendering, which is what reduces perceived latency for a live progress view. D is the wrong API for this use case; A and C don't address perceived latency.

**19. B** — Only a shared prefix is cacheable, so placing stable content first and variable content last maximizes cache hits and reduces both latency and cost. A, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report genuine absence instead of inventing a value to satisfy a required field. A discards the field's value entirely; B and C rely on probabilistic compliance.

**21. C** — Conflicting reads with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and D all discard information or guess.

**22. D** — Tool-use with a matching input schema guarantees structurally valid output, eliminating this parsing-failure class outright. A and B are workarounds for a problem that can be structurally eliminated; C swaps one fragile text format for another.

**23. A** — Schema validity guarantees syntax, not semantics; a separate validation step checking totals against summed line items is needed on top. B, C, and D misdiagnose or abandon a working mechanism.

**24. A** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B discards otherwise-processable invoices; C and D don't address the actual data-quality bottleneck.

**25. D** — Concurrent API calls require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**26. A** — The Messages API contract stays conceptually consistent across vendors, though plumbing and rollout timing can differ — the realistic expectation, not identical performance or a full rewrite.

**27. D** — Thinking content is a distinct block type that must be handled — and typically preserved — separately from final answer text across multi-turn tool-use conversations. A, B, and C mishandle or misdescribe this.

**28. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-invoice cost breakdown. A, C, and D all oversimplify in ways that produce an inaccurate model.

**29. B** — Standard SDLC discipline still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system. A, C, and D all wrongly exempt code from review.

**30. D** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. A is unreliable prompt-level mitigation; B doesn't address cross-contamination; C is an unrelated lever.

**31. C** — High-volume, low-complexity generation fits a fast, low-latency tier, with a higher tier reserved for flagged complex sections — matching capability to actual task difficulty. A and D overspend by default; B ignores task fit.

**32. C** — Targeted routing of only the flagged complex sections to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and D apply broad, costly fixes to a narrow problem.

**33. C** — Pinning a version and deliberately testing before upgrading avoids unattributed behavior drift in production. B accepts avoidable risk; A and D are unhelpful overcorrections unrelated to the actual fix.

**34. B** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. D repeats a failed approach; A and C don't reliably fix structural consistency.

**35. B** — Input and output share one context-window budget, so a long input directly constrains available output length and vice versa. A, C, and D misstate this relationship.

**36. B** — Stable instructions first (ideally cacheable) with variable content after improves both clear role separation (consistency) and caching. A, C, and D misstate the effect of ordering.

**37. B** — Actual per-request token usage (input/output/cache) attributed per report gives an accurate cost picture; estimates or unrelated proxies (A, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and D add cost or complexity for a problem solvable by simple filtering; B works around the symptom without reducing waste.

**40. C** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. B is costly and doesn't guarantee the effect disappears; A and D don't address the underlying attention pattern.

**41. C** — Verifying key claims against the source ledger data catches confident-but-wrong output that fluency alone would let through. D is the failure mode itself; A and B don't address correctness.

**42. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A, B, and D are workarounds for a problem that can be structurally eliminated.

**43. B** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; D discards potentially useful context entirely.

**44. C** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format or edge-case consistency, which a simple high-volume task may not need. A, B, and D are absolute or false claims.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. D** — User-level CLAUDE.md never travels through version control, so a new engineer cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. D** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, B, and C are reactive or abandon the structured-comment requirement.

**49. D** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; A narrows scope but doesn't isolate output; C removes useful functionality.

**50. C** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. B is probabilistic and the violation already happened despite instructions; D mitigates damage rather than preventing it; A is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly; D guesses instead of investigating; A doesn't meaningfully share context between windows.

**52. D** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; B describes behavior that doesn't exist.

**53. A** — Since the config and MCP data were both confirmed correct, the divergence most likely happened in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. B and C re-check already-verified steps; D skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A, B, and C guess without diagnosis.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-team reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and D mischaracterize this capability.

**57. B** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. B** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A and C don't remove the exposed credential from history or ongoing risk; D is easily reversible obfuscation, not real protection.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. C and D are detective/compensating controls; B accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 6.*
