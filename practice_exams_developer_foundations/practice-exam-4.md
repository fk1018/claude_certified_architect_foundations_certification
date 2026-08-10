# CCDVF Practice Exam 4

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

Meridian Cloud, a mid-market B2B SaaS company, is building an internal Claude Agent SDK research agent that preps account executives before sales calls. The main agent orchestrates subagents — a company-researcher, a contacts-finder, and a competitive-analyst — and has tools including `search_web`, `get_crm_record`, `enrich_contact`, and `log_research_note`.

---

**Question 1.** The main research agent calls `search_web` multiple times in sequence, each time waiting for results before deciding what to do next. What should determine when the tool-use loop stops iterating?

- A) When `log_research_note` has been called at least once.
- B) A fixed cap of exactly 3 `search_web` calls per prospect.
- C) When the conversation exceeds 4,000 tokens.
- D) The API response's `stop_reason`: keep executing tool calls while it is `"tool_use"`, stop when it becomes `"end_turn"`.

**Question 2.** After the `enrich_contact` tool executes and your code runs it, what must happen for the agent to correctly continue reasoning about the contact?

- A) Summarize the enrichment result into the system prompt for future turns.
- B) Save the enrichment result to the CRM only, without informing the agent.
- C) Start a new conversation turn that references the enrichment output by ID.
- D) Append a `tool_result` block tied to the original `tool_use` ID and resend the full conversation to the model.

**Question 3.** Meridian's compliance team requires that `log_research_note` never record data sourced from a prospect's personal social media profile, regardless of what the agent reasons about mid-task. The system prompt states this clearly, but logs show it happened anyway. What is the most reliable fix?

- A) Restate the rule more forcefully at the very top of the prompt.
- B) Add few-shot examples of the agent correctly declining to log personal social data.
- C) Reduce temperature so instructions are followed more literally.
- D) Add a hook that inspects `log_research_note` calls and blocks any whose content is tagged as sourced from personal social media.

**Question 4.** Sales leadership wants the agent to always call `get_crm_record` first, with no exceptions, before starting any web research, so existing account history is never missed.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State the requirement clearly in the system prompt.
- B) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- C) Set `tool_choice` to force `get_crm_record` specifically on the first request, then revert to normal tool choice afterward.
- D) Add several few-shot transcripts showing `get_crm_record` called first.

**Question 5.** The agent has grown to include 18 tools, several unrelated to research (invoice lookup, support-ticket creation, internal HR lookup) added for "future use." Tool-selection reliability has degraded.

Question: What is the best fix? (Select ONE response.)

- A) Keep all tools, but mark the research-relevant ones "primary" in the system prompt.
- B) Increase `max_tokens` so the agent has more room to reason about tool choice.
- C) Remove or scope out the unrelated tools so the agent's toolset matches its actual research role.
- D) Add a longer tool-selection policy section to the prompt explaining when each tool applies.

**Question 6.** `get_crm_record` currently returns the literal string `"No Data"` whenever the CRM record doesn't exist, the API key is invalid, or the CRM service is down. The agent treats all three identically and gives inconsistent guidance to the account executive.

Question: What is the best fix? (Select ONE response.)

- A) Retry the call automatically every time `"No Data"` appears.
- B) Return structured error metadata distinguishing "record not found" from "auth failure" from "service unavailable," each machine-readable.
- C) Add a system-prompt note asking the agent to guess which case applies.
- D) Increase the CRM API's timeout value.

**Question 7.** When `search_web` finds no recent news about a small prospect company, it currently returns an error, and the agent apologizes for a "technical issue" and retries the identical query repeatedly.

Question: What should change? (Select ONE response.)

- A) Add a hook that silently ends the research task.
- B) Return a successful response with an empty results list, reserving errors for genuine access failures.
- C) Have the agent call `get_crm_record` instead whenever `search_web` errors.
- D) Add a prompt note telling the agent this error usually means no news exists.

**Question 8.** A sales-ops engineer proposes hardcoding a fixed sequence for every prospect: always `get_crm_record`, then `search_web`, then `enrich_contact`, then `log_research_note`, arguing this makes output predictable across account executives.

Question: Why is model-driven tool selection the better fit here? (Select ONE response.)

- A) Fixed sequences are cheaper because they skip reasoning tokens.
- B) The Claude Agent SDK technically cannot execute a fixed tool order.
- C) Prospect research is high-ambiguity — the right tools, order, and depth depend on what's found along the way, which a fixed sequence can't adapt to.
- D) Fixed sequences can only call built-in tools, not custom ones.

**Question 9.** The team is deciding whether the main research agent should call `enrich_contact` directly, or delegate contact enrichment to a separate, narrowly-scoped contacts-finder subagent with only that tool and explicit rules about which contact fields it may fetch.

Question: What is the strongest argument for the narrowly-scoped subagent? (Select ONE response.)

- A) A narrowly-scoped subagent limits the tool and rule surface exposed for this one task, reducing the chance the main agent misuses enrichment while reasoning about unrelated research steps.
- B) Subagents are mandatory anytime a tool touches personal data.
- C) Subagents always run cheaper than tools called by the main agent.
- D) The main agent's context window can't hold the `enrich_contact` schema.

**Question 10.** During a deep-dive on an enterprise prospect, the agent's context fills with raw `search_web` results — full page text from dozens of articles — leaving little room to actually reason about competitive positioning.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` so responses can be longer.
- B) Only read the first 3 `search_web` results per query.
- C) Delegate web research to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on synthesis.
- D) Disable `search_web` and rely only on `get_crm_record`.

**Question 11.** After a two-hour research session, the account executive opens the output and finds 40 minutes of tool-call logs with no accessible summary of what was actually found.

Question: What should the handoff to the account executive include? (Select ONE response.)

- A) The full raw transcript of every tool call.
- B) A structured handoff: key findings, open questions, and a recommended talking-points summary for the call.
- C) Only the final tool call's result.
- D) A sentiment analysis of how enthusiastic the research sounded.

**Question 12.** Meridian is deciding between running the research agent through a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Operational control (self-hosted) versus operational burden (managed) — the tools the agent can call don't differ by deployment model.
- B) Self-hosted agents cannot call custom tools like `enrich_contact`.
- C) Managed agents are inherently less secure than self-hosted ones.
- D) Managed agents cannot reach a company's internal CRM at all.

**Question 13.** An engineer asks whether prospect research should be built as a fixed workflow or as an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task uses more than three tools.
- B) Whether the team prefers Python or TypeScript.
- C) Whether the task must finish in under a minute.
- D) Whether the task is well-defined and repeatable, versus high-ambiguity with a path that depends on intermediate findings.

**Question 14.** The competitive-analyst subagent's `AgentDefinition` description just says "Helps with competitors." The main agent rarely delegates to it even for clearly competitive questions.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The description drives delegation decisions; rewriting it to state specifically what the subagent does and when to invoke it will most directly fix the under-delegation.
- B) The subagent needs more tools to be delegated to more often.
- C) Subagents can only be delegated to if registered in `.mcp.json`.
- D) The main agent's temperature is too low to consider delegating.

**Question 15.** Compliance wants a hard guarantee that `enrich_contact` is never called more than once per contact per day, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system-prompt instruction stating the once-per-day limit.
- B) A hook that tracks per-contact call timestamps and blocks the call once the daily limit is reached.
- C) A note in the tool's description mentioning the limit.
- D) Few-shot examples showing the agent respecting the limit.

---

## Scenario B: Product-Catalog Enrichment Pipeline for an Online Marketplace (Questions 16–30)

Fernbridge Marketplace lets sellers upload raw product listings — title, bullet points, sometimes a photo — in bulk. Claude enriches each listing into structured attributes (category, material, dimensions, safety flags) used for search and filtering. The pipeline handles both an interactive single-listing flow (a seller uploads one item and waits) and a nightly batch flow (hundreds of thousands of listings).

---

**Question 16.** The nightly batch job enriches 200,000 listings with no user waiting on the result, and no step needs a tool call mid-request.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API with a smaller model to reduce cost.
- B) The synchronous Messages API run in parallel across many threads, to finish as fast as possible.
- C) The synchronous Messages API with `max_tokens` reduced to the minimum.
- D) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.

**Question 17.** An engineer wants to add an "extract attributes, validate against the category schema, retry failed attributes" loop to the batch pipeline, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API doesn't support system prompts.
- B) The 24-hour completion window makes any retry logic impossible.
- C) The Batch API's context window is too small for long listings.
- D) The Batch API cannot execute a validation tool call mid-request and feed results back to the model within a single request — required for this iterative loop.

**Question 18.** The interactive single-listing flow shows a seller a live progress indicator while their listing is being enriched.

Question: What technique best supports this user experience? (Select ONE response.)

- A) The Batch API, since it's built for real-time feedback.
- B) Increasing `max_tokens` so the full response arrives sooner.
- C) Polling the Batch API status endpoint every second.
- D) Streaming, so the UI can render enrichment fields incrementally and reduce perceived latency.

**Question 19.** Every enrichment request sends the same 5,000-token attribute schema and category taxonomy reference, followed by listing-specific text that varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Move the taxonomy reference into a few-shot example block instead.
- B) Switch to the smallest available model regardless of enrichment quality.
- C) Truncate the taxonomy reference to save tokens.
- D) Place the stable schema and taxonomy reference first, enable prompt caching, and put the varying listing text last.

**Question 20.** The schema requires a `battery_type` field on every listing. Non-battery products don't have one, and the model has started inventing plausible-sounding values rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Make `battery_type` nullable so its absence can be reported truthfully.
- D) Lower the temperature to reduce invented values.

**Question 21.** Two credible enrichment passes on the same listing disagree on `weight_kg`: one reports 1.2, another 1.25, and nothing in the listing text resolves which is correct.

Question: What should the pipeline do? (Select ONE response.)

- A) Average the two values.
- B) Discard the listing entirely since the data is unreliable.
- C) Always trust the first enrichment pass.
- D) Flag the field for human review with both candidate values and their source rather than silently picking one.

**Question 22.** The enrichment tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the catalog loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library to fix common syntax issues before parsing.
- C) Define a `submit_attributes` tool whose input schema matches the enrichment structure, and read the data from the structured `tool_use` block instead of parsing free text.
- D) Ask for YAML output instead, since it's more forgiving of formatting drift.

**Question 23.** Since switching to strict schema-constrained tool use, enrichment output always parses successfully, but some extracted `dimensions` (length × width × height) don't match the volume implied elsewhere in the listing.

Question: What should you conclude and do? (Select ONE response.)

- A) Abandon tool use and return to free-text extraction with human review.
- B) The schema needs stricter numeric types to fix this.
- C) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that cross-checks dimensions against other listing fields on top of schema compliance.
- D) `max_tokens` is too low, truncating output mid-generation.

**Question 24.** A subset of incoming listings are seller-submitted photos of a spec sheet with overlaid text and no separate text field. The pipeline currently OCRs the image and sends only the OCR text to Claude, and quality is poor on damaged or low-resolution photos.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject listings that only include image input.
- B) Send the image itself as a content block alongside the enrichment instructions, using Claude's native vision input instead of relying solely on OCR text.
- C) Switch to a larger model, since bigger models are always better at reading noisy text.
- D) Increase `max_tokens` so the model can work harder on the degraded OCR text.

**Question 25.** The pipeline needs to enrich five sections of a very long product manual concurrently to keep interactive latency reasonable, rather than processing sections one at a time.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- B) Streaming, since only streaming supports concurrency.
- C) The Batch API, since it's the only way to run more than one request at a time.
- D) A single request with all five sections concatenated, since Claude parallelizes internally.

**Question 26.** Fernbridge plans to run the same enrichment pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted Claude offering for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) The vendor offering requires a completely different prompting approach and schema design.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) Extraction accuracy and latency are guaranteed identical to the millisecond across vendors.

**Question 27.** The team enables extended thinking on a complex multi-step enrichment-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Convert thinking output into a separate tool call.
- C) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- D) Discard thinking content only when tools are involved.

**Question 28.** Finance asks for an accurate per-listing cost breakdown for the enrichment pipeline, but the current cost model only estimates based on average listing length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- D) A flat per-listing fee regardless of token usage.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the enrichment pipeline's surrounding application code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.
- B) Review should be skipped for any code that calls an external API.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Code review is unnecessary once evals pass.

**Question 30.** A single long-running session is used across an entire day to process unrelated catalog batches from different sellers, and the team notices Claude increasingly referencing details from an unrelated earlier seller's listings.

Question: What is the best fix? (Select ONE response.)

- A) Reduce temperature to prevent cross-referencing.
- B) Start a fresh session (or `/compact`) at natural task boundaries, such as between different sellers' batches, rather than accumulating unrelated context in one long session.
- C) Ask the model to "ignore earlier listings" at the start of each new batch.
- D) Increase the context window so more history fits without confusion.

---

## Scenario C: Cost/Latency Tuning for a Code-Review Assistant (Questions 31–45)

Codeforge runs an internal code-review assistant that fires on every pull request across a large monorepo, summarizing changes, flagging risks, and suggesting fixes. It runs on every PR, so cost and latency matter, but a small fraction of PRs are complex refactors that need deeper reasoning.

---

**Question 31.** Most PRs are small and reviewable with straightforward checks; latency and cost per PR matter far more than handling rare, highly complex refactors well.

Question: Which model tier best fits the default path? (Select ONE response.)

- A) A fast, low-latency tier suited to high-volume/low-complexity review, reserving a higher tier only for PRs flagged as complex.
- B) The highest-capability tier available, to guarantee quality on every PR.
- C) Whichever tier is cheapest per token regardless of task fit.
- D) The same tier used for the hardest architectural reasoning tasks, for consistency.

**Question 32.** A small fraction of PRs are complex multi-file refactors where the fast default model produces shallow, generic review comments.

Question: What is the most targeted fix? (Select ONE response.)

- A) Add more few-shot examples to the fast model's prompt for every PR.
- B) Route only the flagged complex PRs to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.
- C) Switch every PR to the highest-capability tier to be safe.
- D) Increase `max_tokens` for all PRs.

**Question 33.** The service floats to "whatever model is latest" in production. After a routine model update, review tone and the kinds of issues flagged shifted noticeably with no code change.

Question: What should the team do differently? (Select ONE response.)

- A) Nothing — behavior drift across releases is expected and requires no process.
- B) Roll back to the oldest available model version permanently.
- C) Disable all prompt caching to prevent drift.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Reviews need a consistent structure (summary, risk level, specific issues, suggested fix), but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- B) Write an even longer, more detailed prose description of the structure.
- C) Lower the temperature to zero.
- D) Ask the model to restate the structure before reviewing.

**Question 35.** A PR diff is very large (2,000+ changed lines). The team wants a maximally detailed review and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) None — input and output tokens are budgeted completely independently.
- B) Input and output share the same context-window budget, so a very long diff leaves less room for a long review, and vice versa.
- C) Output length has no effect on latency.
- D) Long outputs are always truncated regardless of context window size.

**Question 36.** The review prompt currently places the specific diff text before the general review instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last always improves model attention.
- B) Order has no effect on either consistency or caching.
- C) Reordering only affects cost, never consistency.
- D) Stable, role-defining instructions belong in the system prompt or placed first so they form a consistent, cacheable prefix; diff-specific content should come after as the varying part.

**Question 37.** Finance wants to know exactly how much the review assistant costs per PR, but the team currently estimates cost only from average diff size.

Question: What should be instrumented instead? (Select ONE response.)

- A) Actual token usage per request — input, output, and cache — attributed per PR, rather than an estimate from average size.
- B) Wall-clock latency per PR, used as a cost proxy.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on diff line count.

**Question 38.** An engineer writes an automated eval that asserts the review output must exactly match a fixed reference string for a sample PR, and the eval fails intermittently even though the reviews look correct on manual read.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** PR diffs include full raw CI-log dumps attached to every review request, most of it irrelevant noise, bloating the prompt and slowing the pipeline.

Question: What is the best fix? (Select ONE response.)

- A) Prune the CI output to the relevant fields (failures, relevant lines) before it enters the prompt, rather than passing raw dumps.
- B) Increase `max_tokens` to accommodate the extra data.
- C) Switch to a model with a larger context window so the bloat matters less.
- D) Summarize the CI logs with a second Claude call before reviewing.

**Question 40.** For very long PR diffs, reviewers notice the assistant consistently misses issues in the middle of the diff while covering the first and last files well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Put a brief overview or key-facts summary at the start of the diff and organize file-by-file changes under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.
- B) Switch to a model with an even larger context window.
- C) Add an instruction telling the model to "pay equal attention to the whole diff."
- D) Alphabetize the files before reviewing.

**Question 41.** A review confidently states that a particular function is now covered by a new test, but on manual check, no such test exists in the diff.

Question: What practice would most help catch this class of error before it reaches the PR? (Select ONE response.)

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims (e.g., "test coverage" statements) against the actual diff rather than accepting fluency as correctness.
- C) Increase the model's temperature so answers sound less confident.
- D) Shorten the review so there's less room for errors.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" for the review still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the JSON instruction more emphatically.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip text before the first `{`.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a file's past PR history for context before reviewing the current change, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main review step.
- B) Load the entire file history directly into the main prompt every time.
- C) Skip historical context entirely to avoid the bloat risk.
- D) Increase the context window so the full history always fits.

**Question 44.** For the simplest, most common PR type (dependency version bumps), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- C) Zero-shot is required whenever latency matters at all.
- D) The choice has no effect on cost or latency.

**Question 45.** The review prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this? (Select ONE response.)

- A) Locking the prompt so no one can ever change it again.
- B) Only allowing one designated engineer to ever read the prompt.
- C) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: MCP Servers for a Data-Engineering Team (Questions 46–60)

Northlake's data-engineering team supports about 30 engineers using Claude Code alongside a set of internal MCP servers: a warehouse-query server, a pipeline-status server, and a data-catalog server. The platform team is responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new data engineer clones the team's repository, but Claude Code doesn't apply the team's SQL style conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- B) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- C) The new engineer needs to run `/memory` to activate memory files.
- D) The conventions file exceeded a size limit and was silently truncated.

**Question 47.** A nightly CI job invokes Claude Code to review data-pipeline pull requests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The pull requests are too large for Claude Code to process.
- B) The CI runner lacks permission to call the Claude API.
- C) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream service parses Claude Code's pipeline-review output with regex to post inline comments, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Harden the regex with more permissive fallback patterns.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- C) Post the entire raw output as a single PR comment instead of parsing it.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** The team's `/audit-schema` custom command prints thousands of lines of table and column metadata, and engineers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `allowed-tools`, restricting the command to read-only operations.
- B) `argument-hint`, so engineers scope the analysis more narrowly.
- C) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- D) Removing the command entirely.

**Question 50.** An internal `/new-pipeline` skill is meant only to scaffold new pipeline files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands.
- C) Require engineers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how a large, unfamiliar ETL codebase's data-lineage tracking works before making a change, and worries that reading dozens of files will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Read every file in the codebase in one pass to be thorough.
- B) Skip exploration and infer the architecture from directory names.
- C) Split the work across two separate terminal windows.
- D) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the pipeline change in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Start a brand-new session and rely on memory of what was learned.
- B) Delete the project CLAUDE.md temporarily to free context space.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a pipeline config, calls an internal MCP warehouse-query tool, and writes a status report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- B) Re-read the config file again, since that's the earliest step.
- C) The network connection to the MCP server, since that's the most complex step.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run.

**Question 54.** A pipeline-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Assume it's a model problem and rewrite the prompt.
- B) Switch to a different model to see if the failure persists.
- C) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.
- D) Restart the CI runner and try again.

**Question 55.** The internal data catalog needs to be reachable from Claude Code sessions across the whole data-engineering org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Have each team paste catalog API credentials into their own CLAUDE.md.
- B) Build an MCP server exposing catalog operations as tools, shared across the org.
- C) Hard-code catalog logic into each team's custom skill separately.
- D) Ask each engineer to curl the catalog API manually when needed.

**Question 56.** The warehouse-query MCP server exposes both a `run_query` tool and a way for agents to see what tables and schemas exist without an exploratory query call.

Question: What is the second capability an example of? (Select ONE response.)

- A) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- B) An MCP tool, functionally identical to `run_query`.
- C) A built-in tool provided by the platform automatically.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether the pipeline-status MCP server should run as a local stdio process per engineer's machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) stdio servers are always faster regardless of deployment context.
- B) MCP only supports one communication pattern, so there's no real decision to make.
- C) Remote servers cannot expose tools, only resources.
- D) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a warehouse API token hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Base64-encode the token before committing it.
- B) Rotate the token weekly instead of removing it from the file.
- C) Move the token to environment-variable expansion (e.g., `${WAREHOUSE_TOKEN}`) so the secret isn't committed to version control.
- D) Move `.mcp.json` to a private repository instead.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full table-drop rights) than any actual data-engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Add logging so misuse can be reviewed after the fact.
- B) Add a confirmation prompt before any drop operation.
- C) Leave access as-is, since no misuse has been observed yet.
- D) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific dashboard-refresh workflow used by a single small team, versus a widely-reused schema-validation capability needed by every agent across the data-engineering org.

Question: How should each be built? (Select ONE response.)

- A) Both as MCP servers, since MCP is the correct choice for any shared capability.
- B) Both as Skills, since Skills are always reusable.
- C) Both as built-in tools, since built-in tools require the least setup.
- D) The one-off dashboard-refresh workflow as a Skill or custom tool scoped to that team; the widely-reused schema-validation capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.

---
# Answer Key

**Quick key:** 1-D, 2-D, 3-D, 4-C, 5-C, 6-B, 7-B, 8-C, 9-A, 10-C, 11-B, 12-A, 13-D, 14-A, 15-B, 16-D, 17-D, 18-D, 19-D, 20-C, 21-D, 22-C, 23-C, 24-B, 25-A, 26-A, 27-C, 28-C, 29-A, 30-B, 31-A, 32-B, 33-D, 34-A, 35-B, 36-D, 37-A, 38-B, 39-A, 40-A, 41-B, 42-B, 43-A, 44-B, 45-C, 46-B, 47-C, 48-B, 49-C, 50-A, 51-D, 52-C, 53-A, 54-C, 55-B, 56-A, 57-D, 58-C, 59-D, 60-D

---

**1. D** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (B) is a backstop, not a primary mechanism; token count (C) doesn't indicate loop completion.

**2. D** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. A misuses the system prompt for turn-level data; B keeps the result from the model entirely; C discards conversational state unnecessarily.

**3. D** — A compliance-critical rule needs deterministic enforcement via a hook that blocks the call outright. A, B, and C all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and D are probabilistic.

**5. C** — Removing tools unrelated to the agent's core research role directly reduces the candidate set the agent must reason over, improving selection reliability. A and D add prompt overhead without removing the actual capability bloat; B doesn't address the root cause.

**6. B** — Structured error metadata (record-not-found vs. auth failure vs. service unavailable) lets the agent respond appropriately to each case. Blanket retry (A) wastes calls on non-retryable failures; asking the model to guess (C) is strictly worse than the tool reporting it; D reduces frequency without fixing the missing information.

**7. B** — "No news found" is a valid empty result, not a failure — return success with an empty set. C invents an unnecessary extra step; A hides real signal; D patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, B, and D are false or irrelevant claims about the technology.

**9. A** — A narrowly-scoped subagent with only the enrichment tool and explicit field rules minimizes accidental misuse while the main agent reasons about unrelated tools. B, C, and D are unsupported technical claims.

**10. C** — Delegating web research to a subagent that returns a distilled summary keeps the main agent's context focused on synthesis. A and B don't address the root accumulation problem; D removes needed capability.

**11. B** — A structured handoff (findings, open questions, recommended talking points) lets the account executive act immediately. A forces reconstruction from a raw transcript; C omits diagnostic context; D conveys mood, not facts.

**12. A** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, C, and D are unsupported absolute claims.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not language, tool count, or runtime.

**14. A** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. B, C, and D misdiagnose the cause.

**15. B** — A per-contact call-tracking hook is the only option that deterministically guarantees the limit; A, C, and D remain probabilistic prompt-level guidance.

**16. D** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost; A and C risk quality or truncate output without addressing the actual cost lever.

**17. D** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. A, B, and C misidentify the actual limitation.

**18. D** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case; B and C don't address perceived latency.

**19. D** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, B, and C either break the cacheable prefix or degrade quality without addressing caching.

**20. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance or lose data; A removes the field's value entirely.

**21. D** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, B, and C all discard information or guess.

**22. C** — Tool use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated; D swaps one fragile text format for another.

**23. C** — Schema validity guarantees syntax, not semantics; a separate validation step (checking dimensions against other fields) is needed on top. A, B, and D misdiagnose or abandon a working mechanism.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged documents. C and D don't address the actual data-quality bottleneck; A discards otherwise-processable listings.

**25. A** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. B, C, and D misstate how concurrency is actually achieved.

**26. A** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. C** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and D mishandle or misdescribe this.

**28. C** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-listing cost breakdown. A, B, and D all oversimplify in ways that produce an inaccurate model.

**29. A** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. B** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. C is unreliable prompt-level mitigation; A is an unrelated lever; D doesn't address cross-contamination.

**31. A** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. B and D overspend by default; C ignores task fit.

**32. B** — Targeted routing of only the flagged complex cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, C, and D apply broad, costly fixes to a narrow problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. A accepts avoidable risk; B and C are unhelpful overcorrections unrelated to the actual fix.

**34. A** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. B repeats a failed approach; C and D don't reliably fix structural consistency.

**35. B** — Input and output share one context-window budget, so a long diff directly constrains available output length and vice versa. A, C, and D misstate this relationship.

**36. D** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. A, B, and C misstate the effect of ordering.

**37. A** — Actual per-request token usage (input/output/cache) attributed per PR gives an accurate cost picture; estimates from average size or unrelated proxies (B, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. A** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. C and D work around the symptom without reducing waste; B adds cost without addressing the root problem.

**40. A** — Placing a key-facts summary up front and organizing detail under clear file headers directly counteracts the tendency to under-attend to the middle of long inputs. B is costly and doesn't guarantee the effect disappears; C and D don't address the underlying attention pattern.

**41. B** — Verifying key claims against the actual diff catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; C and D don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue.

**43. A** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. B and D reintroduce the bloat risk; C discards potentially useful context entirely.

**44. B** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and C are absolute claims that don't hold generally; D is false.

**45. C** — Versioning prompts like code enables attribution and rollback for quality regressions. A, B, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. B** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, C, and D misdescribe how CLAUDE.md loading actually works.

**47. C** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. A, B, and D would typically produce different, more specific failure signatures.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive or abandon the structured-comment requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A restricts capability, not output destination; B narrows scope but doesn't isolate output; D removes useful functionality.

**50. A** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. B is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. D** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; C doesn't share context between windows meaningfully.

**52. C** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; B frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. A** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. B and C re-check already-verified steps; D skips diagnosis entirely.

**54. C** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A, B, and D guess or fail to investigate the cause.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. A** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. B, C, and D mischaracterize this capability.

**57. D** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and C are false or oversimplified claims about MCP's communication patterns.

**58. C** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and D don't remove the exposed credential from history or ongoing risk.

**59. D** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and B are detective/compensating controls; C accepts unnecessary risk.

**60. D** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, B, and C force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 4.*
