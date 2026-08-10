# CCDVF Practice Exam 11

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
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

You are building an internal fulfillment agent for Cascade Outfitters, a mid-size e-commerce retailer selling outdoor gear, using the Claude Agent SDK. It has custom tools (`check_inventory`, `reserve_stock`, `create_shipping_label`, `cancel_order`, `notify_customer`, `escalate_to_ops`) and resolves order exceptions — backorders, address problems, fraud holds — that the automated fulfillment system can't handle on its own.

---

**Question 1.** The fulfillment agent's tool-use loop must decide when to stop executing tools and hand control back to the human ops queue. What should drive that decision?

- A) Whether the last tool result contains the word "complete."
- B) A hard limit of five tool calls per order.
- C) Whether the model's response text is longer than 200 tokens.
- D) The `stop_reason` field: keep executing tools while it equals `"tool_use"`, and stop once it becomes `"end_turn"`.

**Question 2.** After `reserve_stock` runs and returns a result, what must the integration code do so the agent can reason correctly on the next turn?

- A) Append a `tool_result` block referencing the `tool_use` id and send the full updated conversation back to the model.
- B) Write the result to an order log and let the next user message summarize it.
- C) Inject the result directly into the system prompt for the rest of the session.
- D) Start a new conversation seeded with just the result.

**Question 3.** Ops policy requires that `cancel_order` never be called on any order already marked "shipped." The system prompt states this clearly, but logs show occasional violations. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt.
- B) Add few-shot examples of the agent correctly refusing to cancel shipped orders.
- C) Lower the model's temperature so it follows the stated policy more consistently.
- D) Implement a hook that intercepts `cancel_order` calls and blocks any targeting an order already marked shipped.

**Question 4.** The team wants the agent to always call a `classify_exception` tool first, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State in the system prompt that `classify_exception` must always run first.
- B) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- C) Add several few-shot examples showing `classify_exception` called first.
- D) Set `tool_choice: {"type": "tool", "name": "classify_exception"}` on the first request, then use normal tool choice afterward.

**Question 5.** The agent currently has 15 tools, including several rarely-used ones (marketing-email triggers, loyalty-points adjustments, warehouse-staffing lookups) unrelated to order-exception handling. Tool selection has become unreliable.

Question: What is the single best fix? (Select ONE response.)

- A) Remove or scope out the tools unrelated to the agent's core exception-handling role.
- B) Keep all tools but add a system prompt note listing which tools are "primary."
- C) Increase `max_tokens` so the agent has more room to reason about which tool to pick.
- D) Add several few-shot examples covering every tool so the agent recognizes each one.

**Question 6.** `check_inventory` currently returns the string `"Error"` for every possible failure — unknown SKU, warehouse system offline, or request timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry policy.
- B) Add a system prompt instruction telling the agent to infer the failure type from context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the warehouse system's timeout so failures become rarer.

**Question 7.** When `check_inventory` finds zero matching SKU rows, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Add a hook that suppresses the error and ends the conversation.
- B) Have the agent call `reserve_stock` first to check whether inventory should exist.
- C) Return a successful response with an empty result set, reserving errors for actual access failures.
- D) Add a system prompt note explaining that this error usually means no SKU matched.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `check_inventory`, then `reserve_stock`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for order-exception handling? (Select ONE response.)

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) The Claude Agent SDK technically cannot run fixed tool sequences.
- C) Exceptions are high-ambiguity; the right tools and order vary by case and depend on intermediate results, which a fixed sequence can't adapt to.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team wants to add an `escalate_to_ops` capability but is deciding whether to give the main fulfillment agent that tool directly or delegate escalation decisions to a separate, narrowly-scoped subagent. Escalating pulls a human ops specialist off other work and should only happen under specific criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) Subagents are required any time a tool has real-world side effects.
- B) A narrowly-scoped subagent can be given only the escalation tool and explicit escalation criteria, reducing the chance the main agent escalates unnecessarily while reasoning about unrelated tools.
- C) The main agent's context window is too small to hold the escalation tool's schema.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During a complex multi-warehouse exception, the agent's context fills with verbose raw inventory dumps, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` so responses can be longer.
- B) Read only the first 50 rows of every inventory query result.
- C) Disable inventory checks and rely on order metadata alone.
- D) Delegate inventory exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on diagnosis.

**Question 11.** The agent escalates a fraud-hold case, but the human ops specialist has no visibility into what the agent tried before escalating — logs show 20 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include? (Select ONE response.)

- A) A structured handoff summary: what was tried, what was found, and a recommended next action.
- B) The full raw transcript of every tool call and result.
- C) Just the final error message, since the human can re-investigate from there.
- D) A sentiment analysis of how urgent the case seemed.

**Question 12.** The team is deciding between letting engineers run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Self-hosted agents cannot use custom tools.
- B) Managed agents are always less secure than self-hosted ones.
- C) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- D) Managed agents cannot access private infrastructure at all.

**Question 13.** An engineer asks whether order-exception handling should be built as a fixed workflow or an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.
- B) Whether the task involves more than three tools.
- C) Whether the team prefers Python or TypeScript.
- D) Whether the task needs to run in under 30 seconds.

**Question 14.** The `AgentDefinition` for a proposed "inventory-analysis subagent" has a vague description: "Helps with inventory." The main agent rarely delegates to it even when inventory analysis is clearly needed.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent needs more tools; add several more inventory-related tools to its definition.
- B) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- C) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.
- D) The main agent's temperature is too low to consider delegating.

**Question 15.** The team wants a hard guarantee that `cancel_order` is never called more than once for the same order within one session, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the one-call limit clearly.
- B) A note in the tool's description mentioning the limit.
- C) Few-shot examples showing an agent stopping after one cancellation.
- D) A hook that tracks per-order call counts and blocks the tool call once the limit is reached.

---

## Scenario B: Multi-Vendor (Bedrock/Vertex) API Integration for a SaaS Platform (Questions 16–30)

You maintain Fenwick Analytics, a SaaS platform that routes Claude requests through the direct Anthropic API, Amazon Bedrock, or Google Vertex AI depending on each enterprise customer's data-residency and procurement requirements. The platform handles both interactive ticket classification for live dashboards and large overnight batch jobs.

---

**Question 16.** An overnight job classifies 50,000 support tickets with no user waiting on the result and no step that needs the model to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- B) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- C) The synchronous Messages API with a smaller model to reduce cost.
- D) The synchronous Messages API with `max_tokens` reduced to the minimum.

**Question 17.** An engineer wants to add an iterative "classify, validate against taxonomy, retry mismatches" loop to the batch pipeline to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts.
- B) The 24-hour window makes any retry logic impossible.
- C) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.
- D) The Batch API's context window is too small for ticket-length threads.

**Question 18.** The interactive dashboard shows a real-time progress indicator while Claude classifies an incoming ticket.

Question: What technique best supports this user experience? (Select ONE response.)

- A) Streaming, so the UI can render output incrementally and reduce perceived latency.
- B) The Batch API, since it's designed for real-time feedback.
- C) Increasing `max_tokens` so the full response arrives faster.
- D) Polling the Batch API status endpoint every second.

**Question 19.** Every request sends the same 5,000-token classification taxonomy, followed by the specific ticket text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Move the taxonomy into a few-shot example block instead.
- B) Switch to the smallest available model regardless of classification quality.
- C) Truncate the taxonomy to save tokens.
- D) Place the stable taxonomy first, enable prompt caching, and put the varying ticket text last.

**Question 20.** The classification schema currently requires an `urgency_reason` field on every ticket. Many tickets have no clear urgency driver, and the model has started inventing plausible-sounding reasons rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field from the schema entirely.
- B) Make `urgency_reason` nullable so its absence can be reported truthfully.
- C) Add a prompt instruction telling the model not to invent values.
- D) Lower the temperature to reduce invented values.

**Question 21.** Two credible classification passes on the same ticket disagree on the assigned category, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do? (Select ONE response.)

- A) Average the two categorical outputs.
- B) Discard the ticket entirely since the data is unreliable.
- C) Flag the field for human review with both candidate values and their source rather than silently picking one.
- D) Always trust the first classification pass.

**Question 22.** The classification tool's JSON output occasionally fails to parse — about 3% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Define a `submit_classification` tool whose input schema matches the classification structure, and read the data from the structured `tool_use` block instead of parsing free text.
- B) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- C) Add a JSON-repair library to fix common syntax issues before parsing.
- D) Ask for YAML output instead, since it's more forgiving of formatting drift.

**Question 23.** Since switching to strict schema-constrained tool use, classification output always parses successfully, but some extracted line-item totals don't sum to the stated ticket-refund amount.

Question: What should you conclude and do? (Select ONE response.)

- A) The schema needs stricter numeric types to fix this.
- B) `max_tokens` is too low, truncating output mid-generation.
- C) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks totals against line-item sums on top of schema compliance.
- D) Abandon tool use and return to free-text extraction with human review.

**Question 24.** A subset of incoming tickets include scanned receipt images with no text layer. The pipeline currently sends only OCR-extracted text to Claude, and quality is poor on receipts with damaged OCR output.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject tickets with scanned receipts from the pipeline entirely.
- B) Increase `max_tokens` so the model can work harder on the degraded OCR text.
- C) Send the receipt image itself as a content block alongside the classification instructions, using Claude's native vision input instead of relying solely on OCR text.
- D) Switch to a larger model, since bigger models are always better at reading noisy text.

**Question 25.** The pipeline needs to classify five ticket batches concurrently to keep latency reasonable, rather than processing batches one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Streaming, since only streaming supports concurrency.
- B) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- C) The Batch API, since it's the only way to run more than one request at a time.
- D) A single request with all five batches concatenated, since Claude parallelizes internally.

**Question 26.** The team runs the same classification pipeline through the direct Anthropic API, Amazon Bedrock, and Google Vertex AI for different enterprise customers' data-residency needs.

Question: What should the team expect? (Select ONE response.)

- A) Extraction accuracy is guaranteed to be identical to the millisecond in latency across vendors.
- B) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) Bedrock and Vertex each require a completely different prompting approach and schema design.

**Question 27.** The team enables extended thinking on a complex multi-step classification-and-escalation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- C) Convert thinking output into a separate tool call.
- D) Discard thinking content only when tools are involved.

**Question 28.** Finance asks for an accurate per-ticket cost breakdown for the classification pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- D) A flat per-ticket fee regardless of token usage.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the classification pipeline's application code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that calls an external API.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Code review is unnecessary once evals pass.

**Question 30.** A single long-running session is used across an entire day to process unrelated ticket batches from different enterprise customers, and the team notices Claude increasingly referencing details from unrelated earlier customers.

Question: What is the best fix? (Select ONE response.)

- A) Reduce temperature to prevent cross-referencing.
- B) Increase the context window so more history fits without confusion.
- C) Start a fresh session (or `/compact`) at natural task boundaries, such as between different customers' batches, rather than accumulating unrelated context in one long session.
- D) Ask the model to "ignore earlier customers" at the start of each new batch.

---

## Scenario C: Model Tiering for a High-Volume Ticket-Triage Service (Questions 31–45)

You run Solstice Support, a customer-support software vendor whose triage service classifies and routes hundreds of thousands of tickets per day across many client accounts. Cost, latency, and consistency all matter, and the team is tuning model tier selection, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the triage task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) The highest-capability tier available, to guarantee quality on every ticket.
- B) Whichever tier is cheapest per token regardless of task fit.
- C) The same tier used for the company's hardest reasoning tasks, for consistency.
- D) A fast, low-latency tier suited to high-volume/low-complexity tasks, reserving a higher tier only for tickets flagged as complex.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a multi-account billing dispute) where the fast default model produces shallow triage notes.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt for every ticket.
- B) Switch every ticket to the highest-capability tier to be safe.
- C) Increase `max_tokens` for all tickets.
- D) Route only the flagged complex tickets to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, triage categories and tone shifted noticeably without any code change.

Question: What should the team do differently? (Select ONE response.)

- A) Nothing — behavior drift across releases is expected and requires no process.
- B) Roll back to the oldest available model version permanently.
- C) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- D) Disable all prompt caching to prevent drift.

**Question 34.** Triage notes need a consistent structure (category, priority, suggested queue) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Write an even longer, more detailed prose description of the structure.
- B) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- C) Lower the temperature to zero.
- D) Ask the model to restate the structure before triaging.

**Question 35.** A ticket thread is very long (50+ messages). The team wants maximally detailed triage notes and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input and output tokens are budgeted completely independently.
- B) Output length has no effect on latency.
- C) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- D) Long outputs are always truncated regardless of context window size.

**Question 36.** The triage prompt currently places the specific ticket text before the general triage instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Order has no effect on either consistency or caching.
- B) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; ticket-specific content should come after as the varying part.
- C) Placing instructions last always improves model attention.
- D) Reordering only affects cost, never consistency.

**Question 37.** Finance wants to know exactly how much the triage service costs per ticket, but the team currently estimates cost only from average prompt length.

Question: What should be instrumented instead? (Select ONE response.)

- A) Wall-clock latency per ticket, used as a cost proxy.
- B) Actual token usage per request — input, output, and cache — attributed per ticket, rather than an estimate from average length.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on ticket character count.

**Question 38.** An engineer writes an automated eval that asserts the triage output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the notes look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** Ticket payloads include full raw metadata dumps (every field of every message) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.
- B) Increase `max_tokens` to accommodate the extra data.
- C) Switch to a model with a larger context window so the bloat matters less.
- D) Summarize the metadata with a second Claude call before triaging.

**Question 40.** For very long ticket threads, the team notices triage notes consistently miss details from the middle of the conversation while capturing the opening and closing messages well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Switch to a model with an even larger context window.
- B) Add an instruction telling the model to "pay equal attention to the whole conversation."
- C) Alphabetize the messages before triaging.
- D) Put a brief overview or key-facts summary at the start of the input and organize the detailed content under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 41.** A triage note confidently states a resolution that, on manual review, never actually happened in the ticket thread.

Question: What practice would most help catch this class of error before it reaches the dashboard? (Select ONE response.)

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Increase the model's temperature so answers sound less confident.
- C) Shorten the note so there's less room for errors.
- D) Apply defensive parsing and skepticism toward confident output — verify key claims (e.g., "resolution" fields) against the source thread rather than accepting fluency as correctness.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the JSON instruction more emphatically.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip text before the first `{`.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a customer account's full ticket history for context before triaging the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load the entire ticket history directly into the main prompt every time.
- B) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main triage step.
- C) Skip historical context entirely to avoid the bloat risk.
- D) Increase the context window so the full history always fits.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) Zero-shot is required whenever latency matters at all.
- C) The choice has no effect on cost or latency.
- D) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.

**Question 45.** The triage prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Locking the prompt so no one can ever change it again.
- B) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- C) Only allowing one designated engineer to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: Claude Code and MCP for a Mobile App Team's CI Pipeline (Questions 46–60)

You support Trailmark Mobile's iOS and Android engineering team's use of Claude Code and a set of internal MCP servers (build-status, crash-reporting, app-store-metadata). You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the mobile team's repository, but Claude Code doesn't apply the team's established Swift and Kotlin style conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The new engineer needs to run `/memory` to activate memory files.
- B) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- C) The conventions file exceeded a size limit and was silently truncated.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.

**Question 47.** A nightly CI job invokes Claude Code to review mobile pull requests and consistently hangs until timeout, with no visible error in the logs.

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

**Question 49.** The team's `/audit-native-deps` custom command prints thousands of lines of dependency-graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- B) `allowed-tools`, restricting the command to read-only operations.
- C) `argument-hint`, so developers scope the analysis more narrowly.
- D) Removing the command entirely.

**Question 50.** An internal `/scaffold-screen` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands.
- C) Require developers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how push-notification handling flows across a large, unfamiliar mobile codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Read every file in the codebase in one pass to be thorough.
- B) Skip exploration and infer the architecture from directory names.
- C) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- D) Split the work across two separate terminal windows.

**Question 52.** Mid-session, context is nearly full of verbose discovery output about the crash-reporting integration, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session and rely on memory of what was learned.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md temporarily to free context space.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a build-config file, calls an internal MCP tool for crash data, and writes a triage report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid crash data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Re-read the config file again, since that's the earliest step.
- B) Just the final error message, since the human can re-investigate from there.
- C) The network connection to the MCP server, since that's the most complex step.
- D) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.

**Question 54.** A build-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.
- B) Assume it's a model problem and rewrite the prompt.
- C) Switch to a different model to see if the failure persists.
- D) Restart the CI runner and try again.

**Question 55.** The internal crash-reporting system needs to be reachable from Claude Code sessions across the whole mobile engineering org, not just one team, and should be maintainable by the platform team independently of any consuming app.

Question: What is the best approach? (Select ONE response.)

- A) Have each team paste crash-reporting API credentials into their own CLAUDE.md.
- B) Build an MCP server exposing crash-reporting operations as tools, shared across the org and maintained centrally by the platform team.
- C) Hard-code crash-reporting logic into each team's custom skill separately.
- D) Ask each engineer to curl the crash-reporting API manually when needed.

**Question 56.** An MCP server for build-status exposes both a `check_build` tool and a way for agents to see what recent builds exist without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP tool, functionally identical to `check_build`.
- B) A built-in tool provided by the platform automatically.
- C) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether the app-store-metadata MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) stdio servers are always faster regardless of deployment context.
- B) MCP only supports one communication pattern, so there's no real decision to make.
- C) Remote servers cannot expose tools, only resources.
- D) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.

**Question 58.** The team's `.mcp.json`, committed to the mobile repository, currently has an app-store-metadata API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Move the token to environment-variable expansion (e.g., `${APP_STORE_TOKEN}`) so the secret isn't committed to version control.
- B) Base64-encode the token before committing it.
- C) Move `.mcp.json` to a private repository instead.
- D) Rotate the token weekly instead of removing it from the file.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full crash-log deletion rights) than any actual mobile engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Add logging so misuse can be reviewed after the fact.
- B) Add a confirmation prompt before any deletion.
- C) Leave access as-is, since no misuse has been observed yet.
- D) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific release-notes generator used by a single small mobile squad, versus a widely-reused build-status-checking capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) The one-off release-notes generator as a Skill or custom tool scoped to that team; the widely-reused build-status capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- B) Both as MCP servers, since MCP is the correct choice for any shared capability.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-D, 5-A, 6-C, 7-C, 8-C, 9-B, 10-D, 11-A, 12-C, 13-A, 14-C, 15-D, 16-B, 17-C, 18-A, 19-D, 20-B, 21-C, 22-A, 23-C, 24-C, 25-B, 26-B, 27-B, 28-C, 29-A, 30-C, 31-D, 32-D, 33-C, 34-B, 35-C, 36-B, 37-B, 38-B, 39-A, 40-D, 41-D, 42-B, 43-B, 44-D, 45-B, 46-D, 47-A, 48-A, 49-A, 50-A, 51-C, 52-B, 53-D, 54-A, 55-B, 56-C, 57-D, 58-A, 59-D, 60-A

---

**1. D** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (B) is a backstop, not a primary mechanism; response length (C) says nothing about completion.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. D** — A policy with real financial/operational consequences needs deterministic enforcement via a hook that blocks the call outright. A, B, and C all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. D** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and C are probabilistic.

**5. A** — Removing tools unrelated to the agent's actual role directly shrinks the candidate set the model must reason over, improving selection reliability. B adds prompt overhead without removing the underlying bloat; C and D don't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (B) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. C** — "No matching SKU" is a valid empty result, not a failure — return success with an empty set. A hides real signal. B invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, B, and D are false or irrelevant claims about the technology.

**9. B** — A narrowly-scoped subagent with only the escalation tool and explicit criteria minimizes accidental escalation while the main agent reasons about unrelated tools. A overgeneralizes; C and D are unsupported technical claims.

**10. D** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis. A and B don't address the root accumulation problem; C removes needed capability.

**11. A** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. B forces reconstruction from a raw transcript. C omits diagnostic context. D conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, B, and D are unsupported absolute claims.

**13. A** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. C** — Tool/subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, B, and D misdiagnose the cause.

**15. D** — A per-order call-count hook is the only option that deterministically guarantees the limit; A, B, and C remain probabilistic prompt-level guidance.

**16. B** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. A doesn't reduce per-token cost; C and D risk quality or truncate output without addressing the actual cost lever.

**17. C** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and D misidentify the actual limitation.

**18. A** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. B is the wrong API for this use case; C and D don't address perceived latency.

**19. D** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, B, and C either break the cacheable prefix or degrade quality without addressing caching.

**20. B** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. A discards the field's value entirely; C and D rely on probabilistic compliance rather than a structural fix.

**21. C** — Conflicting classifications with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and D all discard information or guess.

**22. A** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. B and C are recovery layers for a problem that can be eliminated; D swaps one fragile text format for another.

**23. C** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top. A, B, and D misdiagnose or abandon a working mechanism.

**24. C** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. B and D don't address the actual data-quality bottleneck; A discards otherwise-processable tickets.

**25. B** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. A, C, and D misstate how concurrency is actually achieved.

**26. B** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. B** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, C, and D mishandle or misdescribe this.

**28. C** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-ticket cost breakdown. A, B, and D all oversimplify in ways that produce an inaccurate model.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. C** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. B doesn't address cross-contamination; D is unreliable prompt-level mitigation; A is an unrelated lever.

**31. D** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and B overspend by default; C ignores task fit.

**32. D** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and C apply broad, costly fixes to a narrow problem.

**33. C** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. A accepts avoidable risk; B and D are unhelpful overcorrections unrelated to the actual fix.

**34. B** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A repeats a failed approach; C and D don't reliably fix structural consistency.

**35. C** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. A, B, and D misstate this relationship.

**36. B** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. A, C, and D misstate the effect of ordering.

**37. B** — Actual per-request token usage (input/output/cache) attributed per ticket gives an accurate cost picture; estimates from average length or unrelated proxies (A, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. A** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. B and C work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and C don't address the underlying attention pattern.

**41. D** — Verifying key claims against the source thread catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; B and C don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue.

**43. B** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and D reintroduce the bloat risk; C discards potentially useful context entirely.

**44. D** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and B are absolute claims that don't hold generally; C is false.

**45. B** — Versioning prompts like code enables attribution and rollback for quality regressions. A, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. D** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. B, C, and D are reactive or abandon the structured-comment requirement.

**49. A** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; C narrows scope but doesn't isolate output; D removes useful functionality.

**50. A** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. B is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. D** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and C re-check already-verified steps; B skips diagnosis entirely.

**54. A** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. B and C guess without diagnosis; D doesn't investigate the cause at all.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and D mischaracterize this capability.

**57. D** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and C are false or oversimplified claims about MCP's communication patterns.

**58. A** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. B is easily reversible obfuscation, not real protection; C and D don't remove the exposed credential from history or ongoing risk.

**59. D** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and B are detective/compensating controls; C accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 11.*
