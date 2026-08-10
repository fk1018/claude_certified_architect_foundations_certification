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

- A) Whether the response text contains words like "done" or "resolved."
- B) A fixed cap of 10 tool calls per incident.
- C) The `stop_reason` field: continue while it is `"tool_use"`, terminate at `"end_turn"`.
- D) Whether the most recent tool call returned an error.

**Question 2.** After the agent calls `restart_service` and your code executes it, what must happen for the agent to correctly continue reasoning about the incident?

- A) Append a `tool_result` block referencing the `tool_use` ID to the conversation, then send the full conversation back to the model.
- B) Store the restart confirmation in your incident database only.
- C) Inject the result into the system prompt so it persists for the rest of the conversation.
- D) Start a new session summarizing the restart and continue there.

**Question 3.** Company policy requires human approval before `restart_service` is called on any payment-processing host. The system prompt states this clearly, but logs show occasional autonomous restarts on payment hosts. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt.
- B) Add few-shot examples of the agent correctly escalating payment-host restarts.
- C) Implement a hook that intercepts `restart_service` calls and blocks any targeting a payment-processing host without prior human approval.
- D) Lower the model's temperature so it follows the stated policy more consistently.

**Question 4.** The team wants the agent to always call a `classify_severity` tool first, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State in the system prompt that `classify_severity` must always run first.
- B) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- C) Set `tool_choice: {"type": "tool", "name": "classify_severity"}` on the first request, then use normal tool choice afterward.
- D) Add several few-shot examples showing `classify_severity` called first.

**Question 5. (Select TWO responses.)** The agent currently has 16 tools, including several rarely-used ones (billing lookup, customer notification, feature-flag toggles) unrelated to incident response. Tool selection has become unreliable.

Question: Which two changes best address this?

- A) Remove or scope out the tools unrelated to the agent's core incident-response role.
- B) Split the unrelated responsibilities into separate, specialized agents.
- C) Keep all tools but add a system prompt note listing which tools are "primary."
- D) Increase max_tokens so the agent has more room to reason about which tool to pick.

**Question 6.** `read_logs` currently returns the string `"Error"` for every possible failure — invalid host, permission denied, or log service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry policy.
- B) Add a system prompt instruction telling the agent to infer the failure type from context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the log service's timeout so failures become rarer.

**Question 7.** When `read_logs` finds no matching log lines for a query, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Return a successful response with an empty result set, reserving errors for actual access failures.
- B) Add a hook that suppresses the error and ends the conversation.
- C) Have the agent call `get_deploy_status` first to check whether logs should exist.
- D) Add a system prompt note explaining that this error usually means no logs matched.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `get_deploy_status`, then `read_logs`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for incident response? (Select ONE response.)

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) The Claude Agent SDK technically cannot run fixed tool sequences.
- C) Incidents are high-ambiguity; the right tools and order vary by case and depend on intermediate results, which a fixed sequence can't adapt to.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team wants to add a `page_oncall` capability but is deciding whether to give the main incident agent that tool directly or delegate paging decisions to a separate, narrowly-scoped subagent. Paging has real cost (waking someone up) and should only happen under specific escalation criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) Subagents are required any time a tool has real-world side effects.
- B) The main agent's context window is too small to hold the paging tool's schema.
- C) A narrowly-scoped subagent can be given only the paging tool and explicit escalation criteria, reducing the chance the main agent pages unnecessarily while reasoning about unrelated tools.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During a long-running incident, the agent's context fills with verbose raw log output, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` so responses can be longer.
- B) Read only the first 50 lines of every log query result.
- C) Delegate log exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on diagnosis.
- D) Disable log reading and rely on `get_deploy_status` alone.

**Question 11.** The agent successfully restarts a service, but the human on-call engineer later has no visibility into what the agent tried before escalating — logs show 20 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include? (Select ONE response.)

- A) The full raw transcript of every tool call and result.
- B) Just the final error message, since the human can re-investigate from there.
- C) A structured handoff summary: what was tried, what was found, and a recommended next action.
- D) A sentiment analysis of how urgent the conversation seemed.

**Question 12.** The team is deciding between letting engineers run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- B) Self-hosted agents cannot use custom tools.
- C) Managed agents are always less secure than self-hosted ones.
- D) Managed agents cannot access private infrastructure at all.

**Question 13.** An engineer asks whether the incident-response task should be built as a fixed workflow or an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task involves more than three tools.
- B) Whether the team prefers Python or TypeScript.
- C) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.
- D) Whether the task needs to run in under 30 seconds.

**Question 14.** The agent's `AgentDefinition` for a proposed "log-analysis subagent" has a vague description: "Helps with logs." The main agent rarely delegates to it even when log analysis is clearly needed.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent needs more tools; add several more log-related tools to its definition.
- B) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- C) The main agent's temperature is too low to consider delegating.
- D) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.

**Question 15.** The team wants a hard guarantee that `restart_service` is never called more than twice for the same host within one incident, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the two-call limit clearly.
- B) A note in the tool's description mentioning the limit.
- C) Few-shot examples showing an agent stopping after two restarts.
- D) A hook that tracks per-host call counts and blocks the tool call once the limit is reached.
---

## Scenario B: Document Intelligence API Pipeline (Questions 16–30)

You are integrating Claude into a document-intelligence pipeline that extracts structured data from contracts, invoices, and reports. The pipeline processes both interactive single-document requests (a user uploads one file and waits) and large overnight batch jobs (tens of thousands of documents).

---

**Question 16.** The overnight batch job processes 40,000 invoices with no user waiting on the result. No step needs the model to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API with a smaller model to reduce cost.
- B) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- C) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- D) The synchronous Messages API with max_tokens reduced to the minimum.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry failed fields" loop to the batch pipeline to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts.
- B) The 24-hour window makes any retry logic impossible.
- C) The Batch API's context window is too small for contract-length documents.
- D) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.

**Question 18.** The interactive single-document flow shows users a real-time progress indicator while Claude processes their upload.

Question: What technique best supports this user experience? (Select ONE response.)

- A) Streaming, so the UI can render output incrementally and reduce perceived latency.
- B) The Batch API, since it's designed for real-time feedback.
- C) Increasing max_tokens so the full response arrives faster.
- D) Polling the Batch API status endpoint every second.

**Question 19.** Every request sends the same 6,000-token extraction instructions and field-schema reference, followed by the specific document text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Move the schema reference into a few-shot example block instead.
- B) Switch to the smallest available model regardless of extraction quality.
- C) Truncate the schema reference to save tokens.
- D) Place the stable instructions and schema reference first, enable prompt caching, and put the varying document text last.

**Question 20.** The extraction schema currently requires a `discount_amount` field on every invoice. Many invoices have no discount, and the model has started inventing small values rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Make `discount_amount` nullable so its absence can be reported truthfully.
- D) Lower the temperature to reduce invented values.

**Question 21.** Two credible extraction passes on the same invoice disagree: one reads the total as $4,200.00 and another as $4,200.05, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do? (Select ONE response.)

- A) Average the two values.
- B) Discard the invoice entirely since the data is unreliable.
- C) Always trust the first extraction pass.
- D) Flag the field for human review with both candidate values and their source rather than silently picking one.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 3% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library to fix common syntax issues before parsing.
- C) Ask for YAML output instead, since it's more forgiving of formatting drift.
- D) Define a `submit_extraction` tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of parsing free text.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some extracted line-item amounts don't sum to the stated invoice total.

Question: What should you conclude and do? (Select ONE response.)

- A) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks totals against line-item sums on top of schema compliance.
- B) The schema needs stricter numeric types to fix this.
- C) max_tokens is too low, truncating output mid-generation.
- D) Abandon tool use and return to free-text extraction with human review.

**Question 24.** A subset of incoming invoices are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject scanned invoices from the pipeline entirely.
- B) Increase max_tokens so the model can work harder on the degraded OCR text.
- C) Switch to a larger model, since bigger models are always better at reading noisy text.
- D) Send the invoice image itself as a content block alongside the extraction instructions, using Claude's native vision input instead of relying solely on OCR text.

**Question 25.** The pipeline needs to run extraction on five sections of a long report concurrently to keep latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Streaming, since only streaming supports concurrency.
- B) The Batch API, since it's the only way to run more than one request at a time.
- C) A single request with all five sections concatenated, since Claude parallelizes internally.
- D) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.

**Question 26.** The company plans to run the same extraction pipeline through both the direct Anthropic API and Amazon Bedrock for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) Extraction accuracy is guaranteed to be identical to the millisecond in latency across vendors.
- B) Bedrock requires a completely different prompting approach and schema design.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- C) Convert thinking output into a separate tool call.
- D) Discard thinking content only when tools are involved.

**Question 28.** Finance asks for an accurate per-document cost breakdown for the extraction pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) A flat per-document fee regardless of token usage.
- D) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the extraction pipeline's application code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Review should be skipped for any code that calls an external API.
- B) Code review is unnecessary once evals pass.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.

**Question 30.** A single long-running session is used across an entire day to process unrelated document batches from different clients, and the team notices Claude increasingly referencing details from unrelated earlier documents.

Question: What is the best fix? (Select ONE response.)

- A) Reduce temperature to prevent cross-referencing.
- B) Increase the context window so more history fits without confusion.
- C) Ask the model to "ignore earlier documents" at the start of each new batch.
- D) Start a fresh session (or `/compact`) at natural task boundaries, such as between different clients' batches, rather than accumulating unrelated context in one long session.
---

## Scenario C: Optimizing a High-Volume Support Summarization Service (Questions 31–45)

You run a service that summarizes support tickets for internal dashboards, processing hundreds of thousands of tickets per day. Cost, latency, and consistency all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the summarization task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) The highest-capability tier available, to guarantee quality on every ticket.
- B) A fast, low-latency tier suited to high-volume/low-complexity tasks, reserving a higher tier only for tickets flagged as complex.
- C) Whichever tier is cheapest per token regardless of task fit.
- D) The same tier used for the company's hardest reasoning tasks, for consistency.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a complex multi-product billing dispute) where the fast default model produces shallow summaries.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt for every ticket.
- B) Switch every ticket to the highest-capability tier to be safe.
- C) Increase max_tokens for all tickets.
- D) Route only the flagged complex tickets to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, summary tone and structure shifted noticeably without any code change.

Question: What should the team do differently? (Select ONE response.)

- A) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- B) Nothing — behavior drift across releases is expected and requires no process.
- C) Roll back to the oldest available model version permanently.
- D) Disable all prompt caching to prevent drift.

**Question 34.** Summaries need a consistent structure (issue, root cause, resolution, follow-up) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- B) Write an even longer, more detailed prose description of the structure.
- C) Lower the temperature to zero.
- D) Ask the model to restate the structure before summarizing.

**Question 35.** A ticket thread is very long (50+ messages). The team wants a maximally detailed summary and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input and output tokens are budgeted completely independently.
- B) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- C) Output length has no effect on latency.
- D) Long outputs are always truncated regardless of context window size.

**Question 36.** The summarization prompt currently places the specific ticket text before the general summarization instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; ticket-specific content should come after as the varying part.
- B) Order has no effect on either consistency or caching.
- C) Placing instructions last always improves model attention.
- D) Reordering only affects cost, never consistency.

**Question 37.** Finance wants to know exactly how much the summarization service costs per ticket, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead? (Select ONE response.)

- A) Actual token usage per request — input, output, and cache — attributed per ticket, rather than an estimate from average length.
- B) Wall-clock latency per ticket, used as a cost proxy.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on ticket character count.

**Question 38.** An engineer writes an automated eval that asserts the summarization output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the summaries look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** Ticket threads include full raw metadata dumps (every field of every message) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.
- B) Increase max_tokens to accommodate the extra data.
- C) Switch to a model with a larger context window so the bloat matters less.
- D) Summarize the metadata with a second Claude call before summarizing the ticket.

**Question 40.** For very long ticket threads, the team notices summaries consistently miss details from the middle of the conversation while capturing the opening and closing messages well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Switch to a model with an even larger context window.
- B) Put a brief overview or key-facts summary at the start of the input and organize the detailed content under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.
- C) Add an instruction telling the model to "pay equal attention to the whole conversation."
- D) Alphabetize the messages before summarizing.

**Question 41.** A summary confidently states a resolution that, on manual review, never actually happened in the ticket thread.

Question: What practice would most help catch this class of error before it reaches the dashboard? (Select ONE response.)

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims (e.g., "resolution" fields) against the source thread rather than accepting fluency as correctness.
- C) Increase the model's temperature so answers sound less confident.
- D) Shorten the summary so there's less room for errors.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the JSON instruction more emphatically.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip text before the first `{`.
- D) Increase max_tokens so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a customer's full ticket history for context before summarizing the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main summarization step.
- B) Load the entire ticket history directly into the main prompt every time.
- C) Skip historical context entirely to avoid the bloat risk.
- D) Increase the context window so the full history always fits.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- C) Zero-shot is required whenever latency matters at all.
- D) The choice has no effect on cost or latency.

**Question 45.** The summarization prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt so no one can ever change it again.
- C) Only allowing one designated engineer to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: Claude Code and MCP for an Internal Developer Platform Team (Questions 46–60)

You support a 50-engineer team's use of Claude Code and a set of internal MCP servers (ticketing, deployment status, internal docs). You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the team's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- B) The new engineer needs to run `/memory` to activate memory files.
- C) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- D) The conventions file exceeded a size limit and was silently truncated.

**Question 47.** A nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The pull requests are too large for Claude Code to process.
- C) The CI runner lacks permission to call the Claude API.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- B) Harden the regex with more permissive fallback patterns.
- C) Post the entire raw output as a single PR comment instead of parsing it.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** The team's `/audit-deps` custom command prints thousands of lines of dependency-graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- B) `allowed-tools`, restricting the command to read-only operations.
- C) `argument-hint`, so developers scope the analysis more narrowly.
- D) Removing the command entirely.

**Question 50.** An internal `/scaffold-service` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Add a warning in the skill's instructions telling Claude never to run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- C) Require developers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how authentication flows across a large, unfamiliar codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- B) Read every file in the codebase in one pass to be thorough.
- C) Skip exploration and infer the architecture from directory names.
- D) Split the work across two separate terminal windows.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session and rely on memory of what was learned.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md temporarily to free context space.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal MCP tool, and writes a report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Re-read the config file again, since that's the earliest step.
- B) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- C) The network connection to the MCP server, since that's the most complex step.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run.

**Question 54.** A deployment tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Assume it's a model problem and rewrite the prompt.
- B) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.
- C) Switch to a different model to see if the failure persists.
- D) Restart the CI runner and try again.

**Question 55.** The internal ticketing system needs to be reachable from Claude Code sessions across the whole engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Build an MCP server exposing ticketing operations as tools, shared across the org.
- B) Have each team paste ticketing API credentials into their own CLAUDE.md.
- C) Hard-code ticketing logic into each team's custom skill separately.
- D) Ask each engineer to curl the ticketing API manually when needed.

**Question 56.** An MCP server for internal documentation exposes both a `search_docs` tool and a way for agents to see what documentation exists without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP tool, functionally identical to `search_docs`.
- B) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- C) A built-in tool provided by the platform automatically.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether an internal MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- B) stdio servers are always faster regardless of deployment context.
- C) MCP only supports one communication pattern, so there's no real decision to make.
- D) Remote servers cannot expose tools, only resources.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret isn't committed to version control.
- B) Base64-encode the token before committing it.
- C) Move `.mcp.json` to a private repository instead.
- D) Rotate the token weekly instead of removing it from the file.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Add logging so misuse can be reviewed after the fact.
- B) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- C) Add a confirmation prompt before any deletion.
- D) Leave access as-is, since no misuse has been observed yet.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific reporting workflow used by a single small team, versus a widely-reused authentication-checking capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) Both as MCP servers, since MCP is the correct choice for any shared capability.
- B) The one-off reporting workflow as a Skill or custom tool scoped to that team; the widely-reused authentication capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key — Practice Exam 1

**Quick key:** 1-C, 2-C, 3-C, 4-C, 5-A+B, 6-C, 7-C, 8-C, 9-C, 10-C, 11-C, 12-C, 13-C, 14-D, 15-D, 16-C, 17-D, 18-C, 19-D, 20-C, 21-D, 22-D, 23-D, 24-D, 25-D, 26-D, 27-B, 28-D, 29-D, 30-D, 31-B, 32-D, 33-A, 34-A, 35-B, 36-A, 37-A, 38-B, 39-A, 40-B, 41-B, 42-B, 43-A, 44-B, 45-A, 46-A, 47-A, 48-A, 49-A, 50-B, 51-A, 52-B, 53-B, 54-B, 55-A, 56-B, 57-A, 58-A, 59-B, 60-B

---

**1. C** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (B) is a backstop, not a primary mechanism; tool errors (D) don't indicate loop completion.

**2. C** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. A misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. C** — A financial/safety-critical rule needs deterministic enforcement via a hook that blocks the call outright. A, B, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and D are probabilistic.

**5. A, B** — Removing unrelated tools and/or splitting responsibilities into specialized agents both directly reduce the candidate tool set an agent must reason over, improving selection reliability. C adds prompt overhead without removing the actual capability bloat. D doesn't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (B) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. C** — "No matching logs" is a valid empty result, not a failure — return success with an empty set. B hides real signal. A invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. B, A, and D are false claims about the technology.

**9. C** — A narrowly-scoped subagent with only the paging tool and explicit criteria minimizes accidental paging while the main agent reasons about unrelated tools. A overgeneralizes; B and D are unsupported technical claims.

**10. C** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis. A and B don't address the root accumulation problem; D removes needed capability.

**11. C** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. A forces reconstruction from a raw transcript. B omits diagnostic context. D conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, A, and D are unsupported absolute claims.

**13. C** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not language, tool count, or runtime.

**14. D** — Tool/subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, C, and B misdiagnose the cause.

**15. D** — A per-host call-count hook is the only option that deterministically guarantees the limit; A, C, and B remain probabilistic prompt-level guidance.

**16. C** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost; A and D risk quality or truncate output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, C, and B misidentify the actual limitation.

**18. C** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. B is the wrong API for this use case; A and D don't address perceived latency.

**19. D** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, C, and B either break the cacheable prefix or degrade quality without addressing caching.

**20. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance or lose data; A removes the field's value entirely.

**21. D** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, C, and B all discard information or guess.

**22. D** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated; C swaps one fragile text format for another.

**23. D** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top. B, C, and A misdiagnose or abandon a working mechanism.

**24. D** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B and C don't address the actual data-quality bottleneck; A discards otherwise-processable documents.

**25. D** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. B, C, and A misstate how concurrency is actually achieved.

**26. D** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. B** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, C, and D mishandle or misdescribe this.

**28. D** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-document cost breakdown. B, C, and A all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. D** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. B doesn't address cross-contamination; C is unreliable prompt-level mitigation; A is an unrelated lever.

**31. B** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and D overspend by default; C ignores task fit.

**32. D** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. B, C, and A apply broad, costly fixes to a narrow problem.

**33. A** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. B accepts avoidable risk; C and D are unhelpful overcorrections unrelated to the actual fix.

**34. A** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. B repeats a failed approach; C and D don't reliably fix structural consistency.

**35. B** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. A, C, and D misstate this relationship.

**36. A** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. B, C, and D misstate the effect of ordering.

**37. A** — Actual per-request token usage (input/output/cache) attributed per ticket gives an accurate cost picture; estimates from average length or unrelated proxies (B, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. A** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. B and C work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. B** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; C and D don't address the underlying attention pattern.

**41. B** — Verifying key claims against the source thread catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; C and D don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue.

**43. A** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. B and D reintroduce the bloat risk; C discards potentially useful context entirely.

**44. B** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and C are absolute claims that don't hold generally; D is false.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. A** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. B, C, and D misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. B, C, and D are reactive or abandon the structured-comment requirement.

**49. A** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; C narrows scope but doesn't isolate output; D removes useful functionality.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly; C guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and C re-check already-verified steps; D skips diagnosis entirely.

**54. B** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and C guess without diagnosis; D doesn't investigate the cause at all.

**55. A** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. B, C, and D all fail to provide reusable, centrally maintained access.

**56. B** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, C, and D mischaracterize this capability.

**57. A** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. B, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. A** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. B is easily reversible obfuscation, not real protection; C and D don't remove the exposed credential from history or ongoing risk.

**59. B** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and C are detective/compensating controls; D accepts unnecessary risk.

**60. B** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 1.*

