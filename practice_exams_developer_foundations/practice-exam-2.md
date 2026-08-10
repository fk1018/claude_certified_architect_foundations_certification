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

- A) Whether the response text exceeds a fixed character count.
- B) Whether the text contains a customer-facing summary.
- C) The `stop_reason` field: keep executing tool_use turns and only surface the final answer once `stop_reason` is `"end_turn"`.
- D) The elapsed wall-clock time since the incident was opened.

**Question 2.** After `restart_container` executes, what must happen for the agent to correctly continue reasoning about the incident?

- A) Email the result to the on-call channel and do not feed it back to the model.
- B) Append a summary of the restart to the system prompt so it persists.
- C) Start a brand-new conversation summarizing the restart.
- D) Append a `tool_result` block referencing the `tool_use` ID to the conversation, then send the full conversation back to the model.

**Question 3.** Policy requires that `scale_cluster` never increase a cluster beyond 3x its baseline size without a VP's prior approval. The system prompt states this clearly, but logs show occasional autonomous scale-ups past that threshold. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt.
- B) Add a hook that intercepts `scale_cluster` calls and blocks any request exceeding 3x baseline without a recorded prior approval.
- C) Add few-shot examples of the agent correctly escalating oversized scale requests.
- D) Lower the model's temperature so it follows the stated policy more consistently.

**Question 4.** The team wants `get_instance_health` to run first on every incident, with no exceptions, before any other tool executes.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State in the system prompt that `get_instance_health` must always run first.
- B) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- C) Set `tool_choice: {"type": "tool", "name": "get_instance_health"}` on the first request, then use normal tool choice afterward.
- D) Add several few-shot examples showing `get_instance_health` called first.

**Question 5.** The agent currently has 20 tools, including several rarely-used ones (refund issuance, marketing-campaign toggles, internal survey dispatch) unrelated to incident response. Tool selection has become unreliable.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` so the agent has more room to reason about which tool to pick.
- B) Keep all tools but add a system prompt note listing which tools are "primary."
- C) Lower the temperature to make tool choice more consistent.
- D) Remove or scope out the tools unrelated to this agent's incident-response role.

**Question 6.** `restart_container` currently returns the generic string `"Failed"` for every possible failure — invalid container ID, permission denied, or orchestrator timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry policy.
- B) Add a system prompt instruction telling the agent to infer the failure type from context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the orchestrator's timeout so failures become rarer.

**Question 7.** When `get_instance_health` is called on a newly provisioned instance that hasn't reported its first health check yet, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same call. What should change?

- A) Add a hook that suppresses the error and ends the conversation.
- B) Have the agent call `scale_cluster` first to check provisioning state.
- C) Return a successful response indicating health data isn't available yet, reserving errors for actual access failures.
- D) Add a system prompt note explaining that this error usually means the instance is new.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `get_instance_health`, then `restart_container`, then decide. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for incident response? (Select ONE response.)

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) Incidents are high-ambiguity; the right tools and order vary by case and depend on intermediate results, which a fixed sequence can't adapt to.
- C) The Claude Agent SDK technically cannot run fixed tool sequences.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team wants to add a `notify_customer` capability, which posts customer-facing status-page updates, but is deciding whether to give the main incident agent that tool directly or delegate notification decisions to a separate, narrowly-scoped subagent. Incorrect customer communication carries real reputational cost.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) A narrowly-scoped subagent given only `notify_customer` and explicit criteria reduces the chance the main agent sends a premature or incorrect customer update while reasoning about unrelated tools.
- B) Subagents are required any time a tool has real-world side effects.
- C) The main agent's context window is too small to hold the notification tool's schema.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During a long-running incident, the agent's context fills with verbose raw output from repeated `get_instance_health` calls, leaving little room for reasoning about the actual root cause.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` so responses can be longer.
- B) Delegate health-check exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on diagnosis.
- C) Read only the first 50 lines of every health-check result.
- D) Disable health checks and rely on `restart_container` alone.

**Question 11.** The agent successfully restarts a container, but the on-call engineer later has no visibility into what the agent tried before escalating — logs show 15 minutes of tool calls with no accessible summary.

Question: What should the escalation to a human include? (Select ONE response.)

- A) The full raw transcript of every tool call and result.
- B) Just the final status code, since the human can re-investigate from there.
- C) A sentiment analysis of how urgent the conversation seemed.
- D) A structured handoff summary: what was tried, what was found, and a recommended next action.

**Question 12.** The team is deciding between letting engineers run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on NimbusHost's own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Self-hosted agents cannot use custom tools.
- B) Managed agents are always less secure than self-hosted ones.
- C) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- D) Managed agents cannot access private infrastructure at all.

**Question 13.** An engineer asks whether a proposed "nightly disk-cleanup" task should be built as a fixed workflow or an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task involves more than three tools.
- B) Whether the team prefers Python or TypeScript.
- C) Whether the task needs to run in under 30 seconds.
- D) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.

**Question 14.** The `AgentDefinition` for a proposed "billing-lookup subagent" has a vague description: "Helps with billing." The main agent rarely delegates to it even when a billing question is clearly relevant.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent needs more tools; add several more billing-related tools to its definition.
- B) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- C) The main agent's temperature is too low to consider delegating.
- D) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.

**Question 15.** The team wants a hard guarantee that `restart_container` is never called more than three times for the same instance within one incident, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the three-call limit clearly.
- B) A hook that tracks per-instance call counts and blocks the tool call once the limit is reached.
- C) A note in the tool's description mentioning the limit.
- D) Few-shot examples showing an agent stopping after three restarts.

---

## Scenario B: Batch Invoice-Extraction Pipeline for a Logistics Company (Questions 16–30)

Meridian Freight integrates Claude into a pipeline that extracts structured data — shipper, consignee, weight, freight charges, and accessorial fees — from bills of lading and carrier invoices. The pipeline handles both interactive single-document requests (an ops clerk uploads one document and waits) and large overnight batch runs (tens of thousands of documents).

---

**Question 16.** An overnight batch job processes 50,000 bills of lading with no user waiting on the result. No step needs the model to call a tool mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- B) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- C) The synchronous Messages API with a smaller model to reduce cost.
- D) The synchronous Messages API with max_tokens reduced to the minimum.

**Question 17.** An engineer wants to add an iterative "extract, validate against schema, retry mismatched fields" loop to the batch pipeline, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts.
- B) The 24-hour completion window makes any retry logic impossible.
- C) The Batch API's context window is too small for bill-of-lading-length documents.
- D) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.

**Question 18.** The interactive single-document flow shows ops clerks a real-time progress indicator while Claude processes their upload.

Question: What technique best supports this user experience? (Select ONE response.)

- A) The Batch API, since it's designed for real-time feedback.
- B) Streaming, so the UI can render output incrementally and reduce perceived latency.
- C) Increasing max_tokens so the full response arrives faster.
- D) Polling the Batch API status endpoint every second.

**Question 19.** Every request sends the same 5,000-token extraction instructions and field-schema reference, followed by the specific bill-of-lading text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Place the stable instructions and schema reference first, enable prompt caching, and put the varying document text last.
- B) Move the schema reference into a few-shot example block instead.
- C) Truncate the schema reference to save tokens.
- D) Switch to the smallest available model regardless of extraction quality.

**Question 20.** The extraction schema currently requires an `accessorial_charges` field on every invoice. Many shipments have no accessorial charges, and the model has started inventing small values rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Lower the temperature to reduce invented values.
- D) Make `accessorial_charges` nullable so its absence can be reported truthfully.

**Question 21.** Two credible extraction passes on the same invoice disagree: one reads the total freight charge as $12,400.00 and another as $12,400.50, and there's no way to tell which is correct from context alone.

Question: What should the pipeline do? (Select ONE response.)

- A) Flag the field for human review with both candidate values and their source rather than silently picking one.
- B) Average the two values.
- C) Discard the invoice entirely since the data is unreliable.
- D) Always trust the first extraction pass.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the downstream loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Define a `submit_extraction` tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of parsing free text.
- B) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- C) Add a JSON-repair library to fix common syntax issues before parsing.
- D) Ask for YAML output instead, since it's more forgiving of formatting drift.

**Question 23.** Since switching to strict schema-constrained tool use, extraction output always parses successfully, but some line-item weights don't sum to the stated gross shipment weight.

Question: What should you conclude and do? (Select ONE response.)

- A) Abandon tool use and return to free-text extraction with human review.
- B) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks totals against line-item sums on top of schema compliance.
- C) The schema needs stricter numeric types to fix this.
- D) max_tokens is too low, truncating output mid-generation.

**Question 24.** A subset of incoming bills of lading are scanned images with no text layer. The pipeline currently sends only extracted OCR text to Claude, and quality is poor on documents with damaged OCR output.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject scanned bills of lading from the pipeline entirely.
- B) Send the document image itself as a content block alongside the extraction instructions, using Claude's native vision input instead of relying solely on OCR text.
- C) Increase max_tokens so the model can work harder on the degraded OCR text.
- D) Switch to a larger model, since bigger models are always better at reading noisy text.

**Question 25.** The pipeline needs to run extraction on five sections of a long consolidated freight manifest concurrently to keep latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- B) Streaming, since only streaming supports concurrency.
- C) The Batch API, since it's the only way to run more than one request at a time.
- D) A single request with all five sections concatenated, since Claude parallelizes internally.

**Question 26.** Meridian plans to run the same extraction pipeline through both the direct Anthropic API and Google Vertex AI for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) Extraction accuracy is guaranteed to be identical to the millisecond in latency across vendors.
- B) Vertex AI requires a completely different prompting approach and schema design.
- C) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- D) Batch processing is unavailable on all third-party vendor integrations.

**Question 27.** The team enables extended thinking on a complex multi-step extraction-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- B) Ignore thinking content entirely, since it never affects downstream turns.
- C) Convert thinking output into a separate tool call.
- D) Discard thinking content only when tools are involved.

**Question 28.** Finance asks for an accurate per-document cost breakdown for the extraction pipeline, but the current cost model only estimates based on average document length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- C) A flat per-document fee regardless of token usage.
- D) Only output tokens, since input is effectively free.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the extraction pipeline's application code since "the model does the hard part."

Question: What is the correct response? (Select ONE response.)

- A) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that calls an external API.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Code review is unnecessary once evals pass.

**Question 30.** A single long-running session is used across an entire shift to process unrelated invoice batches from different carrier clients, and the team notices Claude increasingly referencing details from unrelated earlier carriers.

Question: What is the best fix? (Select ONE response.)

- A) Reduce temperature to prevent cross-referencing.
- B) Increase the context window so more history fits without confusion.
- C) Start a fresh session (or `/compact`) at natural task boundaries, such as between different carriers' batches, rather than accumulating unrelated context in one long session.
- D) Ask the model to "ignore earlier documents" at the start of each new batch.

---

## Scenario C: Prompt and Context Engineering for a Financial-Reporting Generator (Questions 31–45)

Ledgerline Analytics generates quarterly financial reports — narrative commentary plus supporting tables — for mid-market clients from raw general-ledger exports and transaction histories. Reports must follow a consistent structure and cite figures precisely, and the team is tuning model selection, prompting, and context handling to hit quality and cost targets.

---

**Question 31.** Most report sections are short, templated commentary (e.g., a routine "expense summary") generated at high volume with simple structure. Latency and cost matter far more than handling rare, highly complex sections well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) The highest-capability tier available, to guarantee quality on every section.
- B) A fast, low-latency tier suited to high-volume/low-complexity sections, reserving a higher tier only for sections flagged as complex.
- C) Whichever tier is cheapest per token regardless of task fit.
- D) The same tier used for the firm's hardest reasoning tasks, for consistency.

**Question 32.** A small fraction of report sections require tracing a multi-entity intercompany reconciliation, where the fast default model produces shallow, incomplete commentary.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt for every section.
- B) Switch every section to the highest-capability tier to be safe.
- C) Route only the flagged complex sections to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.
- D) Increase max_tokens for all sections.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, report tone and numeric-citation style shifted noticeably without any code change.

Question: What should the team do differently? (Select ONE response.)

- A) Roll back to the oldest available model version permanently.
- B) Nothing — behavior drift across releases is expected and requires no process.
- C) Disable all prompt caching to prevent drift.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Reports need a consistent structure (executive summary, variance analysis, notable transactions, outlook) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Write an even longer, more detailed prose description of the structure.
- B) Lower the temperature to zero.
- C) Ask the model to restate the structure before writing the report.
- D) Provide 2–3 few-shot examples demonstrating the exact desired structure.

**Question 35.** A client's ledger export is very long (thousands of transaction rows). The team wants a maximally detailed narrative and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input and output tokens are budgeted completely independently.
- B) Output length has no effect on latency.
- C) Long outputs are always truncated regardless of context window size.
- D) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.

**Question 36.** The reporting prompt currently places the specific transaction data before the general reporting instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; transaction-specific content should come after as the varying part.
- B) Order has no effect on either consistency or caching.
- C) Placing instructions last always improves model attention.
- D) Reordering only affects cost, never consistency.

**Question 37.** Finance wants to know exactly how much the reporting service costs per client report, but the team currently estimates cost only from average ledger-export length.

Question: What should be instrumented instead? (Select ONE response.)

- A) Wall-clock latency per report, used as a cost proxy.
- B) Actual token usage per request — input, output, and cache — attributed per report, rather than an estimate from average length.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on transaction-row count.

**Question 38.** An engineer writes an automated eval that asserts the generated variance-analysis paragraph must exactly match a fixed reference string, and the eval fails intermittently even though the reports look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model is broken and producing wrong answers.
- B) The eval needs a larger reference string.
- C) Temperature should be increased to fix the intermittent failures.
- D) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.

**Question 39.** Ledger exports include full raw metadata for every transaction (internal batch codes, system timestamps, routing IDs) that bloats the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Increase max_tokens to accommodate the extra data.
- B) Switch to a model with a larger context window so the bloat matters less.
- C) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.
- D) Summarize the metadata with a second Claude call before generating the report.

**Question 40.** For clients with very long transaction histories, the team notices generated reports consistently miss mid-period transactions while capturing the opening and closing period well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Put a brief overview or key-figures summary at the start of the input and organize the detailed transactions under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.
- B) Switch to a model with an even larger context window.
- C) Add an instruction telling the model to "pay equal attention to the whole period."
- D) Alphabetize the transactions before summarizing.

**Question 41.** A generated report confidently states a reconciled balance that, on manual review, never actually appears anywhere in the source ledger.

Question: What practice would most help catch this class of error before it reaches a client? (Select ONE response.)

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Increase the model's temperature so answers sound less confident.
- C) Apply defensive parsing and skepticism toward confident output — verify key claims (e.g., stated balances) against the source ledger rather than accepting fluency as correctness.
- D) Shorten the report so there's less room for errors.

**Question 42.** Detailed prose asking the model to "always output the report as valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the JSON instruction more emphatically.
- B) Increase max_tokens so there's room for both the preamble and the JSON.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Post-process every response to strip text before the first `{`.

**Question 43.** The team wants to add an exploratory step that scans a client's prior-quarter reports for context before drafting the current one, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load the entire prior-quarter report history directly into the main prompt every time.
- B) Skip historical context entirely to avoid the bloat risk.
- C) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main drafting step.
- D) Increase the context window so the full history always fits.

**Question 44.** For the simplest, most common report section (a standard cash-position summary), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) Zero-shot is required whenever latency matters at all.
- C) The choice has no effect on cost or latency.
- D) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.

**Question 45.** The reporting prompt has been modified informally by several analysts over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt so no one can ever change it again.
- C) Only allowing one designated analyst to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: Claude Code Governance for a Growing Platform Org (Questions 46–60)

Arbor Platform Engineering supports Claude Code and a set of internal MCP servers (deployment status, incident ticketing, an internal wiki) across an engineering org that has grown from 20 to 150 engineers in under a year. The platform team is responsible for team-wide configuration, CI integration, and troubleshooting as usage scales.

---

**Question 46.** A new engineer clones Arbor's repository, but Claude Code doesn't apply the team's established coding conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The new engineer needs to run `/memory` to activate memory files.
- B) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- C) The conventions file exceeded a size limit and was silently truncated.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.

**Question 47.** A nightly CI job invokes Claude Code to review pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The pull requests are too large for Claude Code to process.
- C) The CI runner lacks permission to call the Claude API.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream service parses Claude Code's PR review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Harden the regex with more permissive fallback patterns.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- C) Post the entire raw output as a single PR comment instead of parsing it.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** Arbor's `/audit-licenses` custom command prints thousands of lines of dependency-license data, and developers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `allowed-tools`, restricting the command to read-only operations.
- B) `argument-hint`, so developers scope the analysis more narrowly.
- C) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- D) Removing the command entirely.

**Question 50.** An internal `/new-microservice` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands.
- C) Require developers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how a large, unfamiliar payments module works before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Read every file in the module in one pass to be thorough.
- B) Skip exploration and infer the architecture from directory names.
- C) Split the work across two separate terminal windows.
- D) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session and rely on memory of what was learned.
- B) Delete the project CLAUDE.md temporarily to free context space.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a config file, calls an internal deployment-status MCP tool, and writes a rollout report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Re-read the config file again, since that's the earliest step.
- B) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- C) The network connection to the MCP server, since that's the most complex step.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run.

**Question 54.** A deployment-status integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.
- B) Assume it's a model problem and rewrite the prompt.
- C) Switch to a different model to see if the failure persists.
- D) Restart the CI runner and try again.

**Question 55.** The internal incident-ticketing system needs to be reachable from Claude Code sessions across the whole engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Hard-code ticketing logic into each team's custom skill separately.
- B) Build an MCP server exposing ticketing operations as tools, shared across the org.
- C) Have each team paste ticketing API credentials into their own CLAUDE.md.
- D) Ask each engineer to curl the ticketing API manually when needed.

**Question 56.** An MCP server for the internal wiki exposes both a `search_wiki` tool and a way for agents to see what wiki spaces exist without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP tool, functionally identical to `search_wiki`.
- B) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- C) A built-in tool provided by the platform automatically.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether the deployment-status MCP server should run as a local stdio process per developer machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) stdio servers are always faster regardless of deployment context.
- B) MCP only supports one communication pattern, so there's no real decision to make.
- C) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- D) Remote servers cannot expose tools, only resources.

**Question 58.** Arbor's `.mcp.json`, committed to the repository, currently has a ticketing API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Base64-encode the token before committing it.
- B) Move `.mcp.json` to a private repository instead.
- C) Rotate the token weekly instead of removing it from the file.
- D) Move the token to environment-variable expansion (e.g., `${TICKETING_TOKEN}`) so the secret isn't committed to version control.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full ticket-deletion rights) than any actual engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Add logging so misuse can be reviewed after the fact.
- C) Add a confirmation prompt before any deletion.
- D) Leave access as-is, since no misuse has been observed yet.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific reporting workflow used by a single small team, versus a widely-reused authentication-checking capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) The one-off reporting workflow as a Skill or custom tool scoped to that team; the widely-reused authentication capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- B) Both as MCP servers, since MCP is the correct choice for any shared capability.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key — Practice Exam 2

**Quick key:** 1-C, 2-D, 3-B, 4-C, 5-D, 6-C, 7-C, 8-B, 9-A, 10-B, 11-D, 12-C, 13-D, 14-D, 15-B, 16-B, 17-D, 18-B, 19-A, 20-D, 21-A, 22-A, 23-B, 24-B, 25-A, 26-C, 27-A, 28-B, 29-A, 30-C, 31-B, 32-C, 33-D, 34-D, 35-D, 36-A, 37-B, 38-D, 39-C, 40-A, 41-C, 42-C, 43-C, 44-D, 45-A, 46-D, 47-A, 48-B, 49-C, 50-A, 51-D, 52-C, 53-B, 54-A, 55-B, 56-B, 57-C, 58-D, 59-A, 60-A

---

**1. C** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text-based signals (B) are unreliable, a fixed cap doesn't exist here as the deciding signal (A doesn't check completion at all), and elapsed time (D) doesn't reflect reasoning state.

**2. D** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. A keeps the result from the model entirely. B misuses the system prompt for turn-level data. C discards conversational state unnecessarily.

**3. B** — A financially consequential rule needs deterministic enforcement via a hook that blocks the call outright. A, C, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and D are probabilistic.

**5. D** — Removing tools unrelated to the agent's core role directly shrinks the candidate set the model must reason over, improving selection reliability. B adds prompt overhead without removing the actual bloat; C and A don't address tool-selection reliability at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (B) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. C** — A not-yet-available health check is a valid pending state, not a failure — return success rather than an error. A hides real signal. B invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, C, and D are false or unsupported claims about the technology.

**9. A** — A narrowly-scoped subagent with only the notification tool and explicit criteria minimizes accidental customer communication while the main agent reasons about unrelated tools. B overgeneralizes; C and D are unsupported technical claims.

**10. B** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on diagnosis. A and C don't address the root accumulation problem; D removes needed capability.

**11. D** — A structured handoff (what was tried, what was found, recommended action) lets a human act immediately. A forces reconstruction from a raw transcript. B omits diagnostic context. C conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. A, B, and D are unsupported absolute claims.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. D** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, B, and C misdiagnose the cause.

**15. B** — A per-instance call-count hook is the only option that deterministically guarantees the limit; A, C, and D remain probabilistic prompt-level guidance.

**16. B** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. A doesn't reduce per-token cost; C and D risk quality or truncate output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and C misidentify the actual limitation.

**18. B** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case; C and D don't address perceived latency.

**19. A** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. B, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and C rely on probabilistic compliance or lose data; A removes the field's value entirely.

**21. A** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. B, C, and D all discard information or guess.

**22. A** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. B and C are recovery layers for a problem that can be eliminated; D swaps one fragile text format for another.

**23. B** — Schema validity guarantees syntax, not semantics; a separate validation step (checking totals against line items) is needed on top. A, C, and D misdiagnose or abandon a working mechanism.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. C and D don't address the actual data-quality bottleneck; A discards otherwise-processable documents.

**25. A** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. B, C, and D misstate how concurrency is actually achieved.

**26. C** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. A** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. B, C, and D mishandle or misdescribe this.

**28. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-document cost breakdown. A, C, and D all oversimplify in ways that produce an inaccurate model.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. C** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. B doesn't address cross-contamination; D is unreliable prompt-level mitigation; A is an unrelated lever.

**31. B** — High-volume, low-complexity sections fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and D overspend by default; C ignores task fit.

**32. C** — Targeted routing of only the flagged complex sections to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and D apply broad, costly fixes to a narrow problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. B accepts avoidable risk; A and C are unhelpful overcorrections unrelated to the actual fix.

**34. D** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A repeats a failed approach; B and C don't reliably fix structural consistency.

**35. D** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. A, B, and C misstate this relationship.

**36. A** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. B, C, and D misstate the effect of ordering.

**37. B** — Actual per-request token usage (input/output/cache) attributed per report gives an accurate cost picture; estimates from average length or unrelated proxies (A, C, D) don't.

**38. D** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and C misdiagnose the cause; B doesn't address the underlying non-determinism.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and B work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. A** — Placing a key-figures summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. B is costly and doesn't guarantee the effect disappears; C and D don't address the underlying attention pattern.

**41. C** — Verifying key claims against the source ledger catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; B and D don't address correctness.

**42. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and D are workarounds for a problem that can be structurally eliminated; B doesn't address the preamble issue.

**43. C** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and D reintroduce the bloat risk; B discards potentially useful context entirely.

**44. D** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and B are absolute claims that don't hold generally; C is false.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. D** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive or abandon the structured-comment requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A restricts capability, not output destination; B narrows scope but doesn't isolate output; D removes useful functionality.

**50. A** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. B is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. D** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; C doesn't share context between windows meaningfully.

**52. C** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; B frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and C re-check already-verified steps; D skips diagnosis entirely.

**54. A** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. B and C guess without diagnosis; D doesn't investigate the cause at all.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. B** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, C, and D mischaracterize this capability.

**57. C** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and D are false or oversimplified claims about MCP's communication patterns.

**58. D** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and C don't remove the exposed credential from history or ongoing risk.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. B and C are detective/compensating controls; D accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 2.*
