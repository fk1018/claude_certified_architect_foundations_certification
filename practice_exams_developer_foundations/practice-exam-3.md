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

- A) Whether the agent's text includes phrases like "order resolved."
- B) A hard limit of 5 tool calls per order.
- C) Whether the last tool call succeeded without errors.
- D) The `stop_reason` value returned with the response: keep looping while it is `"tool_use"`, stop when it becomes `"end_turn"`.

**Question 2.** After the agent calls `check_inventory` and your backend executes it, what must the integration code do so the agent can correctly continue reasoning about the order?

- A) Append a `tool_result` block referencing the `tool_use` ID into the conversation, then send the full conversation back to the model.
- B) Store the inventory count in a database and let the agent infer it was checked.
- C) Insert the result into the system prompt for the remainder of the session.
- D) End the turn and start a new conversation summarizing the inventory count.

**Question 3.** Policy requires manager approval before `issue_refund` is called for any order over $500. The system prompt states this clearly, but audit logs show the agent occasionally issues large refunds without a recorded approval. What is the most reliable fix?

- A) Restate the threshold at both the top and bottom of the system prompt.
- B) Add few-shot examples showing the agent escalating large refunds.
- C) Implement a hook that intercepts `issue_refund` calls and blocks any refund over $500 lacking a recorded approval.
- D) Reduce the model's temperature so it follows the policy more consistently.

**Question 4.** The team wants the agent to always call `check_inventory` first on every new order, with no exceptions, before any other tool executes. What is the most reliable implementation?

- A) Set `tool_choice` to force the `check_inventory` tool specifically on the first request, then use normal tool choice afterward.
- B) Add several few-shot examples showing `check_inventory` called first.
- C) State in the system prompt that `check_inventory` must always run first.
- D) Set `tool_choice: "any"` on the first request so some tool call is guaranteed.

**Question 5.** The agent currently has 14 tools, including several rarely used ones (loyalty-point adjustments, gift-wrap scheduling, marketing opt-in toggles) unrelated to fulfillment exceptions. Tool selection has become unreliable, with the agent sometimes picking irrelevant tools.

- A) Remove or scope out the tools unrelated to the agent's core fulfillment role, or delegate them to a separate agent.
- B) Keep all tools but add a system-prompt note listing which tools are "primary."
- C) Increase `max_tokens` so the agent has more room to reason about which tool to pick.
- D) Add few-shot examples covering every possible tool combination.

**Question 6.** `create_shipping_label` currently returns the string `"Error"` for every failure — invalid address, carrier API timeout, or weight-limit exceeded. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic blind retry.
- B) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- C) Add a system prompt instruction telling the agent to infer the failure type from context.
- D) Increase the carrier API's timeout so failures become rarer.

**Question 7.** When `check_inventory` finds a SKU with zero matching warehouse records (a valid "not stocked" outcome), it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same lookup. What should change?

- A) Return a successful response with a "not stocked" result, reserving errors for actual lookup failures.
- B) Add a hook that suppresses the error and silently ends the conversation.
- C) Have the agent call `notify_customer` first to check whether the SKU should exist.
- D) Add a system-prompt note explaining that this error usually means the SKU is unstocked.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `check_inventory`, then `create_shipping_label`, then `notify_customer`, arguing this makes behavior predictable. Why is model-driven tool selection the better fit for order exceptions?

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) Exceptions are high-ambiguity; the right tools and order vary by case and depend on intermediate results, which a fixed sequence can't adapt to.
- C) The Claude Agent SDK technically cannot run fixed tool sequences.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team wants to add `issue_refund` but is deciding whether to give the main fulfillment agent that tool directly or delegate refund decisions to a separate, narrowly-scoped subagent. Refunds have real financial cost and should only trigger under specific eligibility criteria.

- A) A narrowly-scoped subagent can be given only the refund tool and explicit eligibility criteria, reducing the chance the main agent issues refunds unnecessarily while reasoning about unrelated tools.
- B) Subagents are required any time a tool has real-world financial effects.
- C) The main agent's context window is too small to hold the refund tool's schema.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During a complex multi-item order dispute, the agent's context fills with verbose raw warehouse and carrier API responses, leaving little room for reasoning about the actual resolution.

- A) Increase `max_tokens` so responses can be longer.
- B) Read only the first 50 lines of every API response.
- C) Disable carrier lookups and rely on `check_inventory` alone.
- D) Delegate the raw-data exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on resolution.

**Question 11.** The agent successfully resolves a straightforward backorder but escalates a complex, multi-carrier shipping dispute to a human. The human has no visibility into what the agent tried — logs show 15 minutes of tool calls with no accessible summary.

- A) A structured handoff summary: what was tried, what was found, and a recommended next action.
- B) The full raw transcript of every tool call and result.
- C) Just the final error message, since the human can re-investigate from there.
- D) A sentiment analysis of how frustrated the customer's message seemed.

**Question 12.** The team is deciding between letting the agent run via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own warehouse-adjacent infrastructure.

- A) Managed agents cannot access private infrastructure at all.
- B) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- C) Self-hosted agents cannot use custom tools.
- D) Managed agents are always less secure than self-hosted ones.

**Question 13.** An engineer asks whether order-exception handling should be built as a fixed workflow or an agent.

- A) Whether the task involves more than three tools.
- B) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.
- C) Whether the team prefers Python or TypeScript.
- D) Whether the task needs to run in under 30 seconds.

**Question 14.** The `AgentDefinition` for a proposed "carrier-dispute subagent" has a vague description: "Helps with shipping stuff." The main agent rarely delegates to it even when a carrier dispute is clearly in progress.

- A) The subagent needs more tools; add several more carrier-related tools to its definition.
- B) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- C) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.
- D) The main agent's temperature is too low to consider delegating.

**Question 15.** The team wants a hard guarantee that `issue_refund` is never called more than once for the same order within one session, regardless of what the model decides mid-conversation.

- A) A system-prompt instruction stating the one-call limit clearly.
- B) A note in the tool's description mentioning the limit.
- C) A hook that tracks per-order call counts and blocks the tool call once the limit is reached.
- D) Few-shot examples showing an agent stopping after one refund.

---

## Scenario B: Multi-Vendor (Bedrock/Vertex) API Integration for a SaaS Platform (Questions 16–30)

You are integrating Claude into a SaaS platform's contract-review feature, deployed across the direct Anthropic API, Amazon Bedrock, and Google Vertex AI for regional compliance and redundancy. The feature supports interactive single-document review (a tenant uploads one contract and waits) and a nightly batch job that reprocesses tens of thousands of stored contracts across all tenants.

---

**Question 16.** The nightly job reprocesses 25,000 stored documents across all tenants with no user waiting on the result, and no step needs the model to call a tool mid-request. Which API best fits, and why?

- A) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- B) The synchronous Messages API with a smaller model to reduce cost.
- C) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- D) The synchronous Messages API with `max_tokens` reduced to the minimum.

**Question 17.** An engineer wants to add an "extract, validate against schema, retry failed clauses" loop to the nightly batch job to improve accuracy, and proposes running the whole loop through the Batch API for its cost savings. Why won't this work as designed?

- A) The Batch API doesn't support system prompts.
- B) The 24-hour window makes any retry logic impossible.
- C) The Batch API's context window is too small for contract-length documents.
- D) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.

**Question 18.** The interactive single-document review flow shows tenants a real-time progress indicator while Claude analyzes their uploaded contract. What technique best supports this user experience?

- A) The Batch API, since it's designed for real-time feedback.
- B) Increasing `max_tokens` so the full response arrives faster.
- C) Streaming, so the UI can render output incrementally and reduce perceived latency.
- D) Polling the Batch API status endpoint every second.

**Question 19.** Every request sends the same 5,000-token clause checklist and review instructions, followed by the specific contract text, which varies per request. What optimization most directly reduces both latency and cost across many requests?

- A) Move the clause checklist into a few-shot example block instead.
- B) Switch to the smallest available model regardless of review quality.
- C) Place the stable instructions and checklist first, enable prompt caching, and put the varying contract text last.
- D) Truncate the checklist to save tokens.

**Question 20.** The review schema currently requires a `renewal_clause` field on every contract summary. Many contracts have no renewal clause, and the model has started inventing plausible-sounding clause text rather than reporting none.

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Lower the temperature to reduce invented values.
- D) Make `renewal_clause` nullable so its absence can be reported truthfully.

**Question 21.** Two credible review passes on the same contract disagree on the liability cap: one reads $2,000,000 and another reads $2,500,000, and there's no way to tell which is correct from context alone.

- A) Average the two values.
- B) Always trust the first review pass.
- C) Discard the contract entirely since the data is unreliable.
- D) Flag the field for human review with both candidate values and their source rather than silently picking one.

**Question 22.** The review tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the downstream tenant dashboard. What is the most reliable fix?

- A) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- B) Define a `submit_review` tool whose input schema matches the review structure, and read the data from the structured `tool_use` block instead of parsing free text.
- C) Ask for YAML output instead, since it's more forgiving of formatting drift.
- D) Add a JSON-repair library to fix common syntax issues before parsing.

**Question 23.** Since switching to strict schema-constrained review output, extraction always parses successfully, but some extracted per-clause obligation amounts don't sum to the stated total contract value.

- A) The schema needs stricter numeric types to fix this.
- B) `max_tokens` is too low, truncating output mid-generation.
- C) Abandon tool use and return to free-text extraction with human review.
- D) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks totals against clause-level sums on top of schema compliance.

**Question 24.** A subset of incoming contracts are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

- A) Reject scanned contracts from the pipeline entirely.
- B) Increase `max_tokens` so the model can work harder on the degraded OCR text.
- C) Switch to a larger model, since bigger models are always better at reading noisy text.
- D) Send the contract image itself as a content block alongside the review instructions, using Claude's native vision input instead of relying solely on OCR text.

**Question 25.** The pipeline needs to run review on six sections of a long master service agreement concurrently to keep latency reasonable, rather than processing sections one at a time.

- A) Streaming, since only streaming supports concurrency.
- B) The Batch API, since it's the only way to run more than one request at a time.
- C) A single request with all six sections concatenated, since Claude parallelizes internally.
- D) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.

**Question 26.** The platform plans to run the same review pipeline through the direct Anthropic API, Amazon Bedrock, and Google Vertex AI for different regional deployments. What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) Bedrock and Vertex require a completely different prompting approach and schema design from each other.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) Extraction accuracy is guaranteed to be identical to the millisecond in latency across all three vendors.

**Question 27.** The team enables extended thinking on a complex multi-step review-and-validation task that uses tool calls across several turns. What must the integration layer do correctly?

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Convert thinking output into a separate tool call.
- C) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- D) Discard thinking content only when tools are involved.

**Question 28.** Finance asks for an accurate per-tenant cost breakdown for the review pipeline, but the current cost model only estimates based on average prompt length. What should the improved cost model account for separately?

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- D) A flat per-contract fee regardless of token usage.

**Question 29.** A new engineer argues that once Claude is integrated across all three vendors, the team can skip code review on the pipeline's application code since "the AI part is the risky part." What is the correct response?

- A) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that calls an external API.
- C) Code review is unnecessary once evals pass.
- D) Only the prompt needs review; the surrounding vendor-routing code is low-risk by definition.

**Question 30.** A single long-running session is used across a whole day to process unrelated contract batches from different tenants, and the team notices Claude increasingly referencing details from unrelated earlier tenants' contracts.

- A) Reduce temperature to prevent cross-referencing.
- B) Start a fresh session (or `/compact`) at natural task boundaries, such as between different tenants' batches, rather than accumulating unrelated context in one long session.
- C) Ask the model to "ignore earlier contracts" at the start of each new batch.
- D) Increase the context window so more history fits without confusion.

---

## Scenario C: Model Tiering for a High-Volume Ticket-Triage Service (Questions 31–45)

You run a service that triages hundreds of thousands of inbound support tickets per day — classifying category, urgency, and suggested team — before a human ever sees them. Cost, latency, and consistency all matter, and the team is tuning model tiering, prompting, and context handling to hit targets.

---

**Question 31.** Most tickets are short and the triage classification task is simple and extremely high-volume. Latency and cost per ticket matter far more than handling rare, highly complex edge cases well. Which model tier best fits the default path?

- A) The highest-capability tier available, to guarantee quality on every ticket.
- B) A fast, low-latency tier suited to high-volume/low-complexity tasks, reserving a higher tier only for tickets flagged as complex.
- C) Whichever tier is cheapest per token regardless of task fit.
- D) The same tier used for the company's hardest reasoning tasks, for consistency.

**Question 32.** A small fraction of tickets require multi-step reasoning (tracing a complex multi-product billing dispute) where the fast default model produces shallow triage decisions. What is the most targeted fix?

- A) Route only the flagged complex tickets to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.
- B) Add more few-shot examples to the fast model's prompt for every ticket.
- C) Switch every ticket to the highest-capability tier to be safe.
- D) Increase `max_tokens` for all tickets.

**Question 33.** The triage service currently floats to "whatever model is latest" in production. After a routine model update, category assignments shifted noticeably without any code change. What should the team do differently?

- A) Roll back to the oldest available model version permanently.
- B) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- C) Disable all prompt caching to prevent drift.
- D) Nothing — behavior drift across releases is expected and requires no process.

**Question 34.** Triage output needs a consistent structure (category, urgency, suggested team, confidence) but detailed prose instructions describing the structure haven't produced consistent output. What technique is most likely to help?

- A) Write an even longer, more detailed prose description of the structure.
- B) Ask the model to restate the structure before triaging.
- C) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- D) Lower the temperature to zero.

**Question 35.** A ticket thread is very long (60+ messages). The team wants a maximally detailed triage rationale and considers requesting a very long output to match. What tradeoff must they account for?

- A) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.
- B) None — input and output tokens are budgeted completely independently.
- C) Output length has no effect on latency.
- D) Long outputs are always truncated regardless of context window size.

**Question 36.** The triage prompt currently places the specific ticket text before the general classification instructions and desired format in every request. Why might reordering improve both consistency and cacheability?

- A) Placing instructions last always improves model attention.
- B) Reordering only affects cost, never consistency.
- C) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; ticket-specific content should come after as the varying part.
- D) Order has no effect on either consistency or caching.

**Question 37.** Finance wants to know exactly how much the triage service costs per ticket, but the team currently estimates cost only from average prompt length. What should be instrumented instead?

- A) Actual token usage per request — input, output, and cache — attributed per ticket, rather than an estimate from average length.
- B) Wall-clock latency per ticket, used as a cost proxy.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on ticket character count.

**Question 38.** An engineer writes an automated eval that asserts the triage category output must exactly match a fixed reference string for a sample ticket, and the eval fails intermittently even though the categorizations look correct on manual review. What is the most likely issue with the eval design?

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** Ticket threads include full raw metadata dumps (every field of every message, including internal routing headers) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost. What is the best fix?

- A) Increase `max_tokens` to accommodate the extra data.
- B) Switch to a model with a larger context window so the bloat matters less.
- C) Summarize the metadata with a second Claude call before triaging.
- D) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.

**Question 40.** For very long ticket threads, the team notices triage decisions consistently miss details from the middle of the conversation while capturing the opening and closing messages well. What is the most effective mitigation?

- A) Switch to a model with an even larger context window.
- B) Add an instruction telling the model to "pay equal attention to the whole conversation."
- C) Alphabetize the messages before triaging.
- D) Put a brief overview or key-facts summary at the start of the input and organize the detailed content under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 41.** A triage rationale confidently states that a customer already received a refund, but on manual review, no refund was ever issued in the ticket thread. What practice would most help catch this class of error before it reaches routing?

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims (e.g., "refund issued") against the source thread rather than accepting fluency as correctness.
- C) Increase the model's temperature so answers sound less confident.
- D) Shorten the rationale so there's less room for errors.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON. What is the more reliable approach?

- A) Repeat the JSON instruction more emphatically.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip text before the first `{`.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a customer's full ticket history for context before triaging the current ticket, but worries the exploration will bloat the main context with mostly-irrelevant historical detail. What is the best structural approach?

- A) Load the entire ticket history directly into the main prompt every time.
- B) Skip historical context entirely to avoid the bloat risk.
- C) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main triage step.
- D) Increase the context window so the full history always fits.

**Question 44.** For the simplest, most common ticket type (password reset requests), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples. What consideration should drive the choice?

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- C) Zero-shot is required whenever latency matters at all.
- D) The choice has no effect on cost or latency.

**Question 45.** The triage prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression. What practice would have prevented this?

- A) Locking the prompt so no one can ever change it again.
- B) Only allowing one designated engineer to ever read the prompt.
- C) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: Claude Code and MCP for a Mobile App Team's CI Pipeline (Questions 46–60)

You support a 20-engineer mobile app team (iOS and Android) that uses Claude Code locally and in CI for PR review, release-note generation, and native-dependency auditing. The team also relies on MCP servers for its issue tracker, build-status system, and internal design docs. You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the mobile team's repository, but Claude Code doesn't apply the team's established Kotlin/Swift style conventions for them, even though a teammate's machine applies them correctly. What is the most likely cause?

- A) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- B) The new engineer needs to run `/memory` to activate memory files.
- C) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- D) The conventions file exceeded a size limit and was silently truncated.

**Question 47.** A nightly CI job invokes Claude Code to generate release notes from merged PRs and consistently hangs until timeout, with no visible error in the logs. What is the most likely cause?

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The pull requests are too large for Claude Code to process.
- C) The CI runner lacks permission to call the Claude API.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream release dashboard parses Claude Code's release-notes output with regex to categorize entries, and the parser breaks whenever output formatting drifts slightly between runs. What is the robust fix?

- A) Harden the regex with more permissive fallback patterns.
- B) Post the entire raw output as a single changelog entry instead of parsing it.
- C) Add a stronger prompt instruction never to deviate from the format.
- D) Run with `--output-format json` and a `--json-schema` defining the release-notes structure for machine-parseable output.

**Question 49.** The team's `/audit-native-libs` custom command prints thousands of lines of native-dependency graph data, and developers report that Claude's answers about their actual task get noticeably worse right after running it. What frontmatter change fixes this?

- A) `argument-hint`, so developers scope the analysis more narrowly.
- B) `allowed-tools`, restricting the command to read-only operations.
- C) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- D) Removing the command entirely.

**Question 50.** An internal `/scaffold-screen` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files. What is the correct guardrail?

- A) Add a warning in the skill's instructions telling Claude never to run shell commands.
- B) Require developers to commit their work before running any skill.
- C) Convert the skill into a slash command, since commands cannot run tools.
- D) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.

**Question 51.** An engineer needs to understand how push-notification handling flows across a large, unfamiliar codebase before making a change, and worries that reading dozens of files will exhaust context before implementation begins. What is the best approach?

- A) Read every file in the codebase in one pass to be thorough.
- B) Skip exploration and infer the architecture from directory names.
- C) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- D) Split the work across two separate terminal windows.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings. What should they do?

- A) Start a brand-new session and rely on memory of what was learned.
- B) Delete the project CLAUDE.md temporarily to free context space.
- C) Continue working; Claude automatically discards irrelevant context.
- D) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.

**Question 53.** A multi-step Claude Code task that reads a build-config file, calls an internal MCP tool for build status, and writes a QA report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data. Where should debugging focus next?

- A) Re-read the config file again, since that's the earliest step.
- B) Nothing — a wrong final report with correct inputs means the task should simply be re-run.
- C) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- D) The network connection to the MCP server, since that's the most complex step.

**Question 54.** A build-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did. What is the correct first diagnostic step?

- A) Assume it's a model problem and rewrite the prompt.
- B) Switch to a different model to see if the failure persists.
- C) Restart the CI runner and try again.
- D) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.

**Question 55.** The internal issue-tracking system needs to be reachable from Claude Code sessions across the whole mobile organization, not just one squad, and should be maintainable by the platform team independently of any consuming application. What is the best approach?

- A) Ask each engineer to curl the issue-tracking API manually when needed.
- B) Build an MCP server exposing issue-tracking operations as tools, shared across the org.
- C) Have each team paste issue-tracker API credentials into their own CLAUDE.md.
- D) Hard-code issue-tracking logic into each squad's custom skill separately.

**Question 56.** An MCP server for internal design docs exposes both a `search_docs` tool and a way for agents to see what documentation exists without an exploratory search call. What is the second capability an example of?

- A) A built-in tool provided by the platform automatically.
- B) An MCP tool, functionally identical to `search_docs`.
- C) A Claude Code Skill.
- D) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.

**Question 57.** The team is deciding whether the build-status MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service. What should drive the decision?

- A) stdio servers are always faster regardless of deployment context.
- B) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- C) MCP only supports one communication pattern, so there's no real decision to make.
- D) Remote servers cannot expose tools, only resources.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has an issue-tracker API token hardcoded directly in the file. What is the correct fix?

- A) Base64-encode the token before committing it.
- B) Rotate the token weekly instead of removing it from the file.
- C) Move the token to environment-variable expansion (e.g., `${ISSUE_TRACKER_TOKEN}`) so the secret isn't committed to version control.
- D) Move `.mcp.json` to a private repository instead.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full issue-deletion rights) than any actual mobile-team workflow requires. What is the correct remediation, consistent with least-privilege principles?

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Add logging so misuse can be reviewed after the fact.
- C) Add a confirmation prompt before any deletion.
- D) Leave access as-is, since no misuse has been observed yet.

**Question 60.** The platform team is choosing how to expose a one-off, squad-specific release-checklist workflow used by a single small team, versus a widely-reused build-status-checking capability needed by every agent across the mobile org. How should each be built?

- A) Both as MCP servers, since MCP is the correct choice for any shared capability.
- B) The one-off release-checklist workflow as a Skill or custom tool scoped to that squad; the widely-reused build-status capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-D, 2-A, 3-C, 4-A, 5-A, 6-B, 7-A, 8-B, 9-A, 10-D, 11-A, 12-B, 13-B, 14-C, 15-C, 16-A, 17-D, 18-C, 19-C, 20-D, 21-D, 22-B, 23-D, 24-D, 25-D, 26-A, 27-C, 28-C, 29-A, 30-B, 31-B, 32-A, 33-B, 34-C, 35-A, 36-C, 37-A, 38-B, 39-D, 40-D, 41-B, 42-B, 43-C, 44-B, 45-C, 46-A, 47-A, 48-D, 49-C, 50-D, 51-C, 52-D, 53-C, 54-D, 55-B, 56-D, 57-B, 58-C, 59-A, 60-B

---

**1. D** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (B) is a backstop, not a primary mechanism; tool errors (C) don't indicate loop completion.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. C** — A financial/safety-critical rule needs deterministic enforcement via a hook that blocks the call outright. A, B, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. A** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (D) guarantees some tool call, but not which one. B and C are probabilistic.

**5. A** — Removing tools unrelated to the agent's core role (or delegating them elsewhere) directly reduces the candidate set the agent must reason over, improving selection reliability. B adds prompt overhead without removing the actual capability bloat. C and D don't address tool-selection reliability at all.

**6. B** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (C) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. A** — "Not stocked" is a valid empty result, not a failure — return success with that result. B hides real signal. C invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, C, and D are false claims about the technology.

**9. A** — A narrowly-scoped subagent with only the refund tool and explicit criteria minimizes accidental refunds while the main agent reasons about unrelated tools. B overgeneralizes; C and D are unsupported technical claims.

**10. D** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on resolution. A and B don't address the root accumulation problem; C removes needed capability.

**11. A** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. B forces reconstruction from a raw transcript. C omits diagnostic context. D conveys mood, not facts.

**12. B** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, C, and D are unsupported absolute claims.

**13. B** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. C** — Tool/subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, B, and D misdiagnose the cause.

**15. C** — A per-order call-count hook is the only option that deterministically guarantees the limit; A, B, and D remain probabilistic prompt-level guidance.

**16. A** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. C doesn't reduce per-token cost; B and D risk quality or truncate output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and C misidentify the actual limitation.

**18. C** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case; B and D don't address perceived latency.

**19. C** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and C rely on probabilistic compliance or lose data; A removes the field's value entirely.

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

**33. B** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. D accepts avoidable risk; A and C are unhelpful overcorrections unrelated to the actual fix.

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

**45. C** — Versioning prompts like code enables attribution and rollback for quality regressions. A, B, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. A** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. B, C, and D misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. D** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, B, and C are reactive or abandon the structured-comment requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. B restricts capability, not output destination; A narrows scope but doesn't isolate output; D removes useful functionality.

**50. D** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; B mitigates damage rather than preventing it; C is a false claim about slash commands.

**51. C** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. D** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; B frees trivial space while losing standards; C describes behavior that doesn't exist.

**53. C** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and D re-check or skip already-verified steps; B skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and B guess without diagnosis; C doesn't investigate the cause at all.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. D** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and C mischaracterize this capability.

**57. B** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. C** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and D don't remove the exposed credential from history or ongoing risk.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. B and C are detective/compensating controls; D accepts unnecessary risk.

**60. B** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, squad-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 3.*
