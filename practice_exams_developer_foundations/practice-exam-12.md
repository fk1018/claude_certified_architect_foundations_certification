# CCDVF Practice Exam 12

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Sales Research Agent with Subagents for a B2B SaaS Company, Product-Catalog Enrichment Pipeline for an Online Marketplace, Cost/Latency Tuning for a Code-Review Assistant, MCP Servers for a Data-Engineering Team) |
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

## Scenario A: Sales Research Agent with Subagents for a B2B SaaS Company (Questions 1–15)

Meridian CRM is building an internal sales research agent for its account executives. Before a call, the agent pulls company background, funding signals, and contact details using tools like `lookup_company`, `pull_funding_data`, `find_contacts`, and `draft_call_brief`, and can delegate parts of the research to subagents.

---

**Question 1.** An engineer builds a tool-execution loop for the research agent that must keep calling tools and returning results until Claude has nothing more to do on its own. What should the loop check to decide when to stop?

- A) Continue while `stop_reason` is `"tool_use"`, and stop once it becomes `"end_turn"`.
- B) Stop as soon as `find_contacts` has been called once.
- C) Stop after a fixed 5-second timer regardless of tool calls.
- D) Stop when the response text contains the word "brief."

**Question 2.** After `pull_funding_data` runs, what must the integration code do so Claude can correctly reason about the result on the next turn?

- A) Insert the raw funding data directly into a new system prompt for the remainder of the session.
- B) Append a `tool_result` block referencing the `tool_use` ID to the conversation and resend the full conversation to the model.
- C) Store the funding data in the CRM database only; the model doesn't need to see it directly.
- D) Start a new session and paste a summary of the funding data as the first user message.

**Question 3.** Meridian's policy requires that contacts from EU-based companies never be surfaced with personal emails unless a consent flag is set. The rule is stated clearly in the system prompt, but logs show occasional violations. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt.
- B) Add a hook that intercepts `find_contacts` output and redacts personal emails for EU contacts lacking a consent flag.
- C) Add few-shot examples of correctly redacting EU contacts.
- D) Lower the model's temperature so it follows the stated policy more consistently.

**Question 4.** The team wants `classify_account_tier` to always run first, with no exceptions, before any other tool.

Question: What is the most reliable implementation?

- A) Set `tool_choice: {"type": "tool", "name": "classify_account_tier"}` on the first request, then use normal tool choice afterward.
- B) State in the system prompt that `classify_account_tier` must always run first.
- C) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- D) Add several few-shot examples showing the classification tool called first.

**Question 5.** The research agent has grown to 14 tools, including several rarely-used ones (expense-report lookup, internal HR directory) unrelated to sales research. Tool selection has become unreliable.

Question: What is the best fix?

- A) Increase `max_tokens` so the agent has more room to reason about which tool to pick.
- B) Add a system prompt note listing which tools are "primary," while keeping all 14 available.
- C) Add more few-shot examples showing correct tool selection among all 14 tools.
- D) Remove or scope out the tools unrelated to the agent's core sales-research role.

**Question 6.** `find_contacts` currently returns the string `"Error"` for every possible failure — invalid domain, permission denied, or directory-service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry policy.
- B) Add a system prompt instruction telling the agent to infer the failure type from context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the directory service's timeout so failures become rarer.

**Question 7.** When `find_contacts` finds no matching contacts at a target account, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Have the agent call `lookup_company` first to check whether contacts should exist.
- B) Add a hook that suppresses the error and ends the conversation.
- C) Return a successful response with an empty result set, reserving errors for actual access failures.
- D) Add a system prompt note explaining that this error usually means no contacts matched.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `lookup_company`, then `pull_funding_data`, then `find_contacts`. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for account research?

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) The Claude Agent SDK technically cannot run fixed tool sequences.
- C) Research needs vary by account and depend on intermediate findings, which a fixed sequence can't adapt to.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team is deciding whether to give the main research agent a `send_outreach_email` tool directly or delegate it to a separate, narrowly-scoped subagent. Sending outreach has real cost (reaching a real prospect) and should only happen under specific approval criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent?

- A) Subagents are required any time a tool has real-world side effects.
- B) A narrowly-scoped subagent given only the email tool and explicit approval criteria reduces the chance the main agent sends outreach while reasoning about unrelated research tools.
- C) The main agent's context window is too small to hold the email tool's schema.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During research on a large enterprise account, the agent's context fills with raw funding-database dumps, leaving little room for reasoning about which contacts to prioritize.

Question: What is the best structural fix?

- A) Increase `max_tokens` so responses can be longer.
- B) Read only the first 50 rows of every funding-data result.
- C) Delegate the funding-data lookup to a subagent that returns a distilled summary of relevant findings.
- D) Disable funding lookups and rely on `find_contacts` alone.

**Question 11.** After a call brief is built, the account executive has no visibility into what the agent tried or found — logs show 15 minutes of tool calls with no accessible summary.

Question: What should the handoff to the rep include?

- A) The full raw transcript of every tool call and result.
- B) Just the final error message, since the rep can re-investigate from there.
- C) A sentiment analysis of how promising the account seemed.
- D) A structured handoff summary: what was researched, what was found, and a recommended talking point.

**Question 12.** The team is deciding between running the research agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff?

- A) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- B) Self-hosted agents cannot use custom tools.
- C) Managed agents are always less secure than self-hosted ones.
- D) Managed agents cannot access private infrastructure at all.

**Question 13.** An engineer asks whether the account-research task should be built as a fixed workflow or an agent.

Question: What is the deciding factor?

- A) Whether the task involves more than three tools.
- B) Whether the team prefers Python or TypeScript.
- C) Whether it needs to run in under 30 seconds.
- D) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.

**Question 14.** The `AgentDefinition` for a proposed "contact-finder subagent" has a vague description: "Finds people." The main agent rarely delegates to it even when contact lookup is clearly needed.

Question: What is the most likely cause and fix?

- A) The description drives delegation choices; rewriting it to state specifically what it does and when to use it will most directly fix under-delegation.
- B) The subagent needs more tools; add several more directory-related tools to its definition.
- C) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- D) The main agent's temperature is too low to consider delegating.

**Question 15.** The team wants a hard guarantee that `send_outreach_email` is never called more than once per contact per day, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism?

- A) A hook that tracks per-contact call counts/timestamps and blocks the tool call once the daily limit is reached.
- B) A system prompt instruction stating the daily limit clearly.
- C) A note in the tool's description mentioning the limit.
- D) Few-shot examples showing an agent stopping after one email per contact.

---

## Scenario B: Product-Catalog Enrichment Pipeline for an Online Marketplace (Questions 16–30)

Fernhollow Marketplace runs a catalog enrichment pipeline that generates product descriptions, assigns categories, and extracts attributes (size, material, color) from seller-submitted text and images. It handles both interactive single-listing requests and nightly batch jobs covering hundreds of thousands of listings.

---

**Question 16.** The nightly job processes 200,000 listings with no user waiting on the result, and no step needs the model to call a tool mid-request.

Question: Which API best fits, and why?

- A) The synchronous Messages API with a smaller model to reduce cost.
- B) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- C) The synchronous Messages API with `max_tokens` reduced to the minimum.
- D) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.

**Question 17.** An engineer wants to add an "extract attributes, validate against taxonomy, retry failed attributes" loop to the batch pipeline, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed?

- A) The Batch API doesn't support system prompts.
- B) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.
- C) The 24-hour window makes any retry logic impossible.
- D) The Batch API's context window is too small for listing text.

**Question 18.** The interactive single-listing flow shows sellers a real-time progress indicator while Claude enriches their upload.

Question: What technique best supports this user experience?

- A) The Batch API, since it's designed for real-time feedback.
- B) Increasing `max_tokens` so the full response arrives faster.
- C) Polling the Batch API status endpoint every second.
- D) Streaming, so the UI can render output incrementally and reduce perceived latency.

**Question 19.** Every request sends the same 5,000-token attribute taxonomy and style guide, followed by the listing-specific text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests?

- A) Move the taxonomy into a few-shot example block instead.
- B) Place the stable taxonomy and style guide first, enable prompt caching, and put the varying listing text last.
- C) Truncate the taxonomy to save tokens.
- D) Switch to the smallest available model regardless of extraction quality.

**Question 20.** The schema requires a `material` field on every listing. Many listings genuinely don't specify material, and the model has started inventing plausible-sounding materials rather than reporting unknown.

Question: What schema change fixes this?

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Lower the temperature to reduce invented values.
- D) Make `material` nullable so its absence can be reported truthfully.

**Question 21.** Two extraction passes on the same listing disagree on garment size — one reads "M" and another "Medium (US 8–10)" — and there's no way to tell which is more precise from context alone.

Question: What should the pipeline do?

- A) Automatically pick whichever value appeared in the first pass.
- B) Flag the field for human review with both candidate values and their source rather than silently picking one.
- C) Average the two values numerically.
- D) Discard the listing entirely since the data is unreliable.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 4% of listings produce malformed JSON that crashes the catalog loader.

Question: What is the most reliable fix?

- A) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library to fix common syntax issues before parsing.
- C) Define a `submit_attributes` tool whose input schema matches the extraction structure, and read the data from the structured `tool_use` block instead of parsing free text.
- D) Ask for YAML output instead, since it's more forgiving of formatting drift.

**Question 23.** Since switching to strict schema-constrained tool use, attribute output always parses successfully, but some listings have a `sale_price` value that is higher than the listed `price`, even though both fields pass schema validation.

Question: What should you conclude and do?

- A) Strict schemas eliminate semantic errors as well as syntax errors, so no further action is needed.
- B) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks logical constraints (e.g., `sale_price` ≤ `price`) on top of schema compliance.
- C) `max_tokens` is too low, truncating output mid-generation.
- D) Abandon tool use and return to free-text extraction with human review.

**Question 24.** A subset of listing photos have overlaid seller text (size charts, care instructions) that a separate OCR pass on the image often garbles, and extraction quality is poor when only that OCR text is sent to Claude.

Question: What is the most direct fix?

- A) Reject listings with overlay text from the pipeline entirely.
- B) Send the listing image itself as a content block alongside the extraction instructions, using Claude's native vision input instead of relying solely on OCR text.
- C) Increase `max_tokens` so the model can work harder on the degraded OCR text.
- D) Switch to a larger model, since bigger models are always better at reading noisy text.

**Question 25.** The pipeline needs to enrich five attribute categories (color, size, material, style, care) of a multi-variant listing concurrently rather than one at a time, to keep latency reasonable.

Question: What must the integration layer support to do this?

- A) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- B) Streaming, since only streaming supports concurrency.
- C) The Batch API, since it's the only way to run more than one request at a time.
- D) A single request with all five categories concatenated, since Claude parallelizes internally.

**Question 26.** The marketplace plans to run the enrichment pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted version of the model, for regional compliance reasons.

Question: What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) The third-party vendor requires a completely different prompting and schema design.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) Extraction accuracy is guaranteed to be identical to the millisecond in latency across vendors.

**Question 27.** The team enables extended thinking on a complex multi-step categorization-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly?

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Convert thinking output into a separate tool call.
- C) Discard thinking content only when tools are involved.
- D) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.

**Question 28.** Finance asks for an accurate per-listing cost breakdown for the enrichment pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately?

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) A flat per-listing fee regardless of token usage.
- D) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the enrichment pipeline's application code since "the AI part is the risky part."

Question: What is the correct response?

- A) Review should be skipped for any code that calls an external API.
- B) Code review is unnecessary once evals pass.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.

**Question 30.** A single long-running session is used across an entire day to enrich unrelated catalogs from different sellers, and the team notices Claude increasingly referencing details from an unrelated earlier seller's listings.

Question: What is the best fix?

- A) Reduce temperature to prevent cross-referencing.
- B) Increase the context window so more history fits without confusion.
- C) Start a fresh session (or `/compact`) at natural task boundaries, such as between different sellers' catalogs, rather than accumulating unrelated context in one long session.
- D) Ask the model to "ignore earlier listings" at the start of each new batch.

---

## Scenario C: Cost/Latency Tuning for a Code-Review Assistant (Questions 31–45)

Ridgeline DevTools runs a code-review assistant that fires on every pull request across dozens of internal repos, generating inline comments and a review summary. Given the CI volume, cost, latency, and consistency all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most PRs are small and the review task is straightforward; latency and cost per PR matter far more than handling rare, deeply architectural changes well.

Question: Which model tier best fits the default path?

- A) The highest-capability tier available, to guarantee quality on every PR.
- B) A fast, low-latency tier suited to high-volume/low-complexity review, reserving a higher tier only for PRs flagged as complex.
- C) Whichever tier is cheapest per token regardless of task fit.
- D) The same tier used for the company's hardest reasoning tasks, for consistency.

**Question 32.** A small fraction of PRs require deep multi-file reasoning (a cross-service refactor) where the fast default model produces shallow comments.

Question: What is the most targeted fix?

- A) Add more few-shot examples to the fast model's prompt for every PR.
- B) Switch every PR to the highest-capability tier to be safe.
- C) Increase `max_tokens` for all PRs.
- D) Route only the flagged complex PRs to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, review tone and comment structure shifted noticeably without any code change.

Question: What should the team do differently?

- A) Nothing — behavior drift across releases is expected and requires no process.
- B) Roll back to the oldest available model version permanently.
- C) Disable all prompt caching to prevent drift.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Reviews need a consistent structure (summary, issues by severity, suggested fix) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help?

- A) Write an even longer, more detailed prose description of the structure.
- B) Lower the temperature to zero.
- C) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- D) Ask the model to restate the structure before reviewing.

**Question 35.** A PR diff is very large (2,000+ changed lines). The team wants a maximally detailed review and considers requesting a very long output to match.

Question: What tradeoff must they account for?

- A) Input and output share the same context-window budget, so a very long diff leaves less room for a long review, and vice versa.
- B) None — input and output tokens are budgeted completely independently.
- C) Output length has no effect on latency.
- D) Long outputs are always truncated regardless of context window size.

**Question 36.** The review prompt currently places the PR diff before the general review instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability?

- A) Order has no effect on either consistency or caching.
- B) Placing instructions last always improves model attention.
- C) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; diff-specific content should come after as the varying part.
- D) Reordering only affects cost, never consistency.

**Question 37.** Finance wants to know exactly how much the review service costs per PR, but the team currently estimates cost only from average diff size.

Question: What should be instrumented instead?

- A) Wall-clock latency per PR, used as a cost proxy.
- B) Number of API calls only, regardless of token count.
- C) Actual token usage per request — input, output, and cache — attributed per PR, rather than an estimate from average size.
- D) A flat cost assumption based on lines-changed count.

**Question 38.** An engineer writes an automated eval that asserts the review output must exactly match a fixed reference string for a sample PR, and the eval fails intermittently even though the reviews look correct on manual review.

Question: What is the most likely issue with the eval design?

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** PR metadata dumps (every CI check, every commit timestamp, every file mode change) bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix?

- A) Increase `max_tokens` to accommodate the extra data.
- B) Switch to a model with a larger context window so the bloat matters less.
- C) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.
- D) Summarize the metadata with a second Claude call before reviewing.

**Question 40.** For very large diffs, the team notices reviews consistently miss issues in files in the middle of the diff while covering the first and last files well.

Question: What is the most effective mitigation?

- A) Switch to a model with an even larger context window.
- B) Add an instruction telling the model to "pay equal attention to the whole diff."
- C) Alphabetize the files before reviewing.
- D) Put a brief overview or key-facts summary at the start of the input and organize the detailed content under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 41.** A review confidently states that a function "already has null checks" that, on manual inspection, don't actually exist in the diff.

Question: What practice would most help catch this class of error before it reaches the PR?

- A) Apply defensive parsing and skepticism toward confident output — verify key claims against the source diff rather than accepting fluency as correctness.
- B) Trust confident, fluent-sounding output as evidence of correctness by default.
- C) Increase the model's temperature so answers sound less confident.
- D) Shorten the review so there's less room for errors.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach?

- A) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- B) Repeat the JSON instruction more emphatically.
- C) Post-process every response to strip text before the first `{`.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a repo's full commit history for related past bugs before reviewing the current PR, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach?

- A) Load the entire commit history directly into the main prompt every time.
- B) Skip historical context entirely to avoid the bloat risk.
- C) Increase the context window so the full history always fits.
- D) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main review step.

**Question 44.** For the simplest, most common review type (formatting-only lint fixes), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice?

- A) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- B) Multi-shot is always strictly better regardless of task simplicity.
- C) Zero-shot is required whenever latency matters at all.
- D) The choice has no effect on cost or latency.

**Question 45.** The review prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this?

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt so no one can ever change it again.
- C) Only allowing one designated engineer to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: MCP Servers for a Data-Engineering Team (Questions 46–60)

Cascade Analytics has a 40-engineer data-engineering team that uses Claude Code alongside internal MCP servers for warehouse queries, pipeline status, and a data catalog. You lead team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the team's dbt repository, but Claude Code doesn't apply the team's established SQL style conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause?

- A) The new engineer needs to run `/memory` to activate memory files.
- B) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- C) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- D) The conventions file exceeded a size limit and was silently truncated.

**Question 47.** A nightly CI job invokes Claude Code to review dbt model changes and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause?

- A) The pull requests are too large for Claude Code to process.
- B) The CI runner lacks permission to call the Claude API.
- C) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream service parses Claude Code's pipeline-review output with regex to post inline comments on dbt pull requests, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix?

- A) Harden the regex with more permissive fallback patterns.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- C) Post the entire raw output as a single PR comment instead of parsing it.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** The team's `/audit-lineage` custom command prints thousands of lines of table-lineage graph data, and engineers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this?

- A) `allowed-tools`, restricting the command to read-only operations.
- B) `argument-hint`, so engineers scope the analysis more narrowly.
- C) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- D) Removing the command entirely.

**Question 50.** An internal `/scaffold-pipeline` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail?

- A) Add a warning in the skill's instructions telling Claude never to run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- C) Require engineers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how a complex data-lineage flow crosses an unfamiliar warehouse schema before making a change, and worries that reading dozens of model files will exhaust context before implementation begins.

Question: What is the best approach?

- A) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- B) Read every file in the schema in one pass to be thorough.
- C) Skip exploration and infer the schema from table names.
- D) Split the work across two separate terminal windows.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the pipeline change in the same session and wants to preserve key findings.

Question: What should they do?

- A) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- B) Start a brand-new session and rely on memory of what was learned.
- C) Delete the project CLAUDE.md temporarily to free context space.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a pipeline config, calls the warehouse-query MCP tool, and writes a report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next?

- A) Re-read the config file again, since that's the earliest step.
- B) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- C) The network connection to the MCP server, since that's the most complex step.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run.

**Question 54.** A pipeline-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step?

- A) Assume it's a model problem and rewrite the prompt.
- B) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.
- C) Switch to a different model to see if the failure persists.
- D) Restart the CI runner and try again.

**Question 55.** The internal warehouse-query capability needs to be reachable from Claude Code sessions across the whole data org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach?

- A) Have each team paste warehouse credentials into their own CLAUDE.md.
- B) Hard-code query logic into each team's custom skill separately.
- C) Build an MCP server exposing warehouse-query operations as tools, shared across the org.
- D) Ask each engineer to run the warehouse CLI manually when needed.

**Question 56.** An MCP server for the data catalog exposes both a `search_tables` tool and a way for agents to see what tables and schemas exist without an exploratory search call.

Question: What is the second capability an example of?

- A) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- B) An MCP tool, functionally identical to `search_tables`.
- C) A built-in tool provided by the platform automatically.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether the pipeline-status MCP server should run as a local stdio process per engineer's machine or as a remote, centrally-hosted network service.

Question: What should drive the decision?

- A) stdio servers are always faster regardless of deployment context.
- B) MCP only supports one communication pattern, so there's no real decision to make.
- C) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- D) Remote servers cannot expose tools, only resources.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a warehouse API token hardcoded directly in the file.

Question: What is the correct fix?

- A) Base64-encode the token before committing it.
- B) Move `.mcp.json` to a private repository instead.
- C) Rotate the token weekly instead of removing it from the file.
- D) Move the token to environment-variable expansion (e.g., `${WAREHOUSE_TOKEN}`) so the secret isn't committed to version control.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full table-drop rights) than any actual data-engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles?

- A) Add logging so misuse can be reviewed after the fact.
- B) Add a confirmation prompt before any drop operation.
- C) Leave access as-is, since no misuse has been observed yet.
- D) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific data-quality reporting workflow used by a single small team, versus a widely-reused schema-validation capability needed by every pipeline agent across the org.

Question: How should each be built?

- A) Both as MCP servers, since MCP is the correct choice for any shared capability.
- B) The one-off reporting workflow as a Skill or custom tool scoped to that team; the widely-reused schema-validation capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key

**Quick key:** 1-A, 2-B, 3-B, 4-A, 5-D, 6-C, 7-C, 8-C, 9-B, 10-C, 11-D, 12-A, 13-D, 14-A, 15-A, 16-D, 17-B, 18-D, 19-B, 20-D, 21-B, 22-C, 23-B, 24-B, 25-A, 26-A, 27-D, 28-D, 29-D, 30-C, 31-B, 32-D, 33-D, 34-C, 35-A, 36-C, 37-C, 38-B, 39-C, 40-D, 41-A, 42-A, 43-D, 44-A, 45-A, 46-C, 47-C, 48-B, 49-C, 50-B, 51-A, 52-A, 53-B, 54-B, 55-C, 56-A, 57-C, 58-D, 59-D, 60-B

---

**1. A** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (D) are unreliable; a single-call stop (B) or fixed timer (C) don't reflect what Claude actually needs.

**2. B** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. C keeps the result from the model entirely. A misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. B** — A compliance-critical rule needs deterministic enforcement via a hook that redacts the data outright. A, C, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. A** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (C) guarantees some tool call, but not which one. B and D are probabilistic.

**5. D** — Removing tools unrelated to the agent's core role directly reduces the candidate set the agent must reason over, improving selection reliability. B adds prompt overhead without removing the actual capability bloat. A and C don't address the root cause.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to guess (B) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. C** — "No matching contacts" is a valid empty result, not a failure — return success with an empty set. B hides real signal. A invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity research where the right tools/order depend on intermediate findings is the core case for model-driven selection. A, B, and D are false or unsupported claims about the technology.

**9. B** — A narrowly-scoped subagent with only the outreach tool and explicit criteria minimizes accidental sends while the main agent reasons about unrelated tools. A overgeneralizes; C and D are unsupported technical claims.

**10. C** — Delegating the funding lookup to a subagent that returns a distilled summary keeps the main agent's context focused on prioritization. A and B don't address the root accumulation problem; D removes needed capability.

**11. D** — A structured handoff (what was researched, what was found, recommended talking point) lets the rep act immediately. A forces reconstruction from a raw transcript. B omits diagnostic context. C conveys a guess, not facts.

**12. A** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, C, and D are unsupported absolute claims.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. A** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. B, C, and D misdiagnose the cause.

**15. A** — A per-contact call-count/timestamp hook is the only option that deterministically guarantees the limit; B, C, and D remain probabilistic prompt-level guidance.

**16. D** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost; A and C risk quality or truncate output without addressing the actual cost lever.

**17. B** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, C, and D misidentify the actual limitation.

**18. D** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case; B and C don't address perceived latency.

**19. B** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and C rely on probabilistic compliance; A removes the field's value entirely.

**21. B** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, C, and D all discard information or guess.

**22. C** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated; D swaps one fragile text format for another.

**23. B** — Schema validity guarantees syntax, not semantics; a separate validation step (checking logical constraints between fields) is needed on top. A, C, and D misdiagnose or abandon a working mechanism.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged overlay text. C and D don't address the actual data-quality bottleneck; A discards otherwise-processable listings.

**25. A** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. B, C, and D misstate how concurrency is actually achieved.

**26. A** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. D** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and C mishandle or misdescribe this.

**28. D** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-listing cost breakdown. A, B, and C all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. C** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. B doesn't address cross-contamination; D is unreliable prompt-level mitigation; A is an unrelated lever.

**31. B** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and D overspend by default; C ignores task fit.

**32. D** — Targeted routing of only the flagged complex PRs to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and C apply broad, costly fixes to a narrow problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. A accepts avoidable risk; B and C are unhelpful overcorrections unrelated to the actual fix.

**34. C** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A repeats a failed approach; B and D don't reliably fix structural consistency.

**35. A** — Input and output share one context-window budget, so a long diff directly constrains available review length and vice versa. B, C, and D misstate this relationship.

**36. C** — Stable instructions first (ideally cacheable) and variable content after both improve consistency (clear role separation) and caching. A, B, and D misstate the effect of ordering.

**37. C** — Actual per-request token usage (input/output/cache) attributed per PR gives an accurate cost picture; estimates from average size or unrelated proxies (A, B, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and B work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and C don't address the underlying attention pattern.

**41. A** — Verifying key claims against the source diff catches confident-but-wrong output that fluency alone would let through. B is the failure mode itself; C and D don't address correctness.

**42. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. C and B are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue.

**43. D** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; B discards potentially useful context entirely.

**44. A** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. B and C are absolute claims that don't hold generally; D is false.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. C** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and D misdescribe how CLAUDE.md loading actually works.

**47. C** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. A, B, and D would typically produce different, more specific failure signatures.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive or abandon the structured-comment requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A restricts capability, not output destination; B narrows scope but doesn't isolate output; D removes useful functionality.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly; C guesses instead of investigating; D doesn't share context between windows meaningfully.

**52. A** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. B discards findings; C frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. B** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and C re-check already-verified steps; D skips diagnosis entirely.

**54. B** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and C guess without diagnosis; D doesn't investigate the cause at all.

**55. C** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, B, and D all fail to provide reusable, centrally maintained access.

**56. A** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. B, C, and D mischaracterize this capability.

**57. C** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and D are false or oversimplified claims about MCP's communication patterns.

**58. D** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and C don't remove the exposed credential from history or ongoing risk.

**59. D** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and B are detective/compensating controls; C accepts unnecessary risk.

**60. B** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 12.*
