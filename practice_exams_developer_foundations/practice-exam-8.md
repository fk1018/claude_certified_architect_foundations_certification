# CCDVF Practice Exam 8

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

Meridian Cloud, a B2B SaaS analytics vendor, is building an internal sales-research agent for its account executives. The agent has tools (`lookup_company`, `search_news`, `get_crm_history`, `send_outreach_email`, `draft_brief`) and delegates parts of its work to narrowly-scoped subagents so account executives get a concise pre-call brief instead of a wall of raw research.

---

**Question 1.** The orchestrator agent calls `lookup_company`, receives results, and must decide whether to call another tool or finish. What should the surrounding harness key off to know when to stop feeding tool results back into the loop?

- A) Whether the response text contains a phrase like "brief complete."
- B) The `stop_reason` field: keep executing tools and returning results while it is `"tool_use"`, stop once it is `"end_turn"`.
- C) A fixed cap of five tool calls per prospect, regardless of outcome.
- D) Whether `lookup_company` returned a non-empty payload.

**Question 2.** After the orchestrator calls `search_news` and the harness executes it, what must happen for the agent to correctly continue reasoning about the prospect?

- A) Summarize the news result in a side channel and let the agent ask for it only if it asks.
- B) Store the news result in the CRM and let the agent query the CRM tool again to see it.
- C) Append a `tool_result` block referencing the original `tool_use` ID to the conversation, then send the full conversation back to the model.
- D) Rewrite the system prompt to include the news result for the rest of the session.

**Question 3.** Meridian's policy requires that `send_outreach_email` never fire on a prospect account flagged "do not contact" in the CRM. The system prompt states this rule plainly, but an audit finds a handful of emails sent to flagged accounts anyway.

Question: What is the most reliable fix? (Select ONE response.)

- A) Move the "do not contact" rule to the very top of the system prompt for emphasis.
- B) Implement a hook that checks the CRM flag before `send_outreach_email` executes and blocks the call if the account is flagged.
- C) Add few-shot examples showing the agent correctly declining to email flagged accounts.
- D) Lower the model's temperature so instructions are followed more literally.

**Question 4.** The team wants every research session to begin with `lookup_company` — no exceptions — before any other tool is considered, so the brief always starts from verified firmographic data.

Question: What is the most reliable implementation? (Select ONE response.)

- A) State in the system prompt that `lookup_company` must always run first.
- B) Set `tool_choice: "any"` on the first request so some tool call is guaranteed.
- C) Set `tool_choice: {"type": "tool", "name": "lookup_company"}` on the first request, then use normal tool choice afterward.
- D) Add several few-shot examples that show `lookup_company` called first.

**Question 5.** The orchestrator currently has 14 tools, including several rarely-used ones (partner-referral lookup, event-invite tracking, swag-request submission) that have nothing to do with pre-call research. Tool selection has become unreliable and the agent sometimes calls the wrong tool for a simple company lookup.

Question: What is the single most direct fix? (Select ONE response.)

- A) Add a system prompt note ranking which tools are "primary" versus "secondary."
- B) Increase max_tokens so the agent has more room to reason before choosing a tool.
- C) Ask the agent to double-check its tool choice with a follow-up message before executing.
- D) Remove the unrelated tools from this agent's tool set — or move them to a separate, specialized agent — so the orchestrator only reasons over tools relevant to pre-call research.

**Question 6.** `get_crm_history` currently returns the string `"lookup failed"` whether the account ID is invalid, the CRM is down, or the AE lacks access permissions. The agent responds inconsistently to each case. What is the best fix?

- A) Wrap every call in an automatic retry policy regardless of cause.
- B) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- C) Add a system prompt instruction telling the agent to guess the likely cause from context.
- D) Increase the CRM API's timeout so failures occur less often.

**Question 7.** When `search_news` finds no recent articles about a small prospect, it currently returns an error. The agent responds by apologizing for a "temporary issue" and retrying the identical query. What should change?

- A) Add a system prompt note explaining that this particular error usually just means no news exists.
- B) Return a successful response with an empty result list, reserving errors for actual access or service failures.
- C) Have the agent call `lookup_company` again first to confirm the company exists.
- D) Add a hook that silently ends the research session when this happens.

**Question 8.** A sales-ops engineer proposes replacing the orchestrator's reasoning with a fixed sequence — always `lookup_company`, then `search_news`, then `get_crm_history`, then draft — arguing it makes output more predictable.

Question: Why is model-driven tool selection still the better fit here? (Select ONE response.)

- A) Prospect research is high-ambiguity — the right tools, and whether to skip or repeat one, depend on what earlier results reveal, which a fixed sequence can't adapt to.
- B) Model-driven selection is always cheaper because it uses fewer reasoning tokens.
- C) Fixed sequences cannot invoke custom tools, only tools built into the platform.
- D) The Claude Agent SDK technically cannot execute a hardcoded tool sequence.

**Question 9.** The team is deciding whether to give the main research orchestrator the `send_outreach_email` tool directly, or delegate outreach decisions to a separate, narrowly-scoped subagent that only fires under specific qualification criteria.

Question: What is the strongest argument for the separate subagent? (Select ONE response.)

- A) Subagents always execute tool calls faster than the main agent.
- B) A narrowly-scoped subagent can be given only the outreach tool and explicit qualification criteria, reducing the chance an email fires while the main agent is reasoning about unrelated research tools.
- C) The main agent's context window is too small to hold the outreach tool's schema.
- D) Any tool with a real-world side effect legally requires a dedicated subagent.

**Question 10.** During research on a large enterprise prospect, the orchestrator's context fills with verbose raw news articles and CRM activity logs, leaving little room to reason about what actually belongs in the brief.

Question: What is the best structural fix? (Select ONE response.)

- A) Increase `max_tokens` so the final brief can be longer.
- B) Truncate every tool result to its first 200 characters.
- C) Disable `search_news` and rely on CRM history alone.
- D) Delegate research gathering to a subagent that returns a distilled set of relevant findings, keeping the main agent's context focused on synthesizing the brief.

**Question 11.** The agent finishes a research session and hands the brief to the AE, but the AE has no visibility into what was actually checked — the trace shows a dozen tool calls with no accessible summary of what was tried or found.

Question: What should the handoff to the AE include? (Select ONE response.)

- A) Just the final brief text, since the AE doesn't need to know how it was produced.
- B) A structured summary of what was checked, what was found, and any gaps or caveats, alongside the brief.
- C) The full raw transcript of every tool call and result.
- D) A confidence score with no supporting detail.

**Question 12.** Meridian is deciding between running the research agent through a hosted, Anthropic-managed execution environment versus self-hosting the agent harness on its own infrastructure.

Question: What is the core tradeoff? (Select ONE response.)

- A) Operational control (self-hosted) versus operational burden (managed) — there is no inherent difference in what tools the agent can call.
- B) Self-hosted agents cannot call custom tools like `lookup_company`.
- C) Managed agents are inherently less secure than self-hosted deployments.
- D) Managed agents cannot reach a company's internal CRM under any circumstances.

**Question 13.** An engineer asks whether generating the pre-call brief should be built as a fixed multi-step workflow or as an agent that decides its own steps.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the task involves more than four distinct tools.
- B) Whether the task is well-defined and repeatable versus high-ambiguity, where the right steps depend on intermediate findings.
- C) Whether the team's engineers prefer Python or TypeScript.
- D) Whether the brief must be produced in under ten seconds.

**Question 14.** A proposed "competitive-intel subagent" has the `AgentDefinition` description "helps with competitor stuff." The orchestrator rarely delegates to it, even for prospects clearly evaluating a competitor.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The subagent's temperature is too low to consider being delegated to.
- B) Subagents cannot be delegated to unless registered in `.mcp.json`.
- C) The subagent needs more tools added to its definition before it will be used.
- D) The description drives delegation decisions; rewriting it to state specifically what the subagent covers and when to use it will most directly fix under-delegation.

**Question 15.** Meridian wants a hard guarantee that `send_outreach_email` is never called more than once per prospect per day, regardless of what the orchestrator decides mid-session.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system prompt instruction stating the daily limit clearly.
- B) Few-shot examples showing an agent declining a second same-day email.
- C) A hook that tracks per-prospect send counts for the day and blocks the tool call once the limit is reached.
- D) A note in the tool's description mentioning the limit.

---

## Scenario B: Product-Catalog Enrichment Pipeline for an Online Marketplace (Questions 16–30)

Fernhaven Marketplace uses Claude to enrich seller-submitted product listings — normalizing titles, inferring categories, and extracting structured attributes (size, material, color) from free-text descriptions and photos. The pipeline handles both a large nightly batch of new listings and a smaller interactive flow when a seller edits a listing live on the site.

---

**Question 16.** The nightly batch enriches 60,000 new listings with no user waiting on the result, and no step requires a mid-request tool call.

Question: Which API best fits, and why? (Select ONE response.)

- A) The synchronous Messages API run across as many parallel threads as the account allows, to finish fastest.
- B) The synchronous Messages API with max_tokens set to the minimum needed.
- C) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- D) The synchronous Messages API with a smaller model chosen only to cut cost.

**Question 17.** An engineer wants to add an "extract attributes, validate against the category schema, retry unresolved fields" loop to the batch pipeline to raise accuracy, and proposes running the entire loop through the Batch API to keep the cost savings.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API cannot execute a validation tool call mid-request and feed the result back to the model within a single request — which this iterative loop requires.
- B) The Batch API's 24-hour completion window makes any retry logic impossible to schedule.
- C) The Batch API doesn't support system prompts, so validation instructions would be dropped.
- D) The Batch API's context window is too small for a full product description.

**Question 18.** The interactive flow shows a seller a live "enriching your listing..." indicator while Claude processes their edit.

Question: What technique best supports this experience? (Select ONE response.)

- A) Increasing max_tokens so the complete response arrives sooner.
- B) Polling the Batch API's status endpoint once per second.
- C) Streaming, so the UI can render partial output incrementally and reduce perceived latency.
- D) Running the request twice and showing whichever finishes first.

**Question 19.** Every enrichment request sends the same 5,000-token category taxonomy and attribute schema, followed by the specific listing text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests? (Select ONE response.)

- A) Place the stable taxonomy and schema first, enable prompt caching, and put the varying listing text last.
- B) Move the taxonomy into a few-shot example block instead of a schema reference.
- C) Switch to the smallest available model regardless of enrichment quality.
- D) Truncate the taxonomy to the most common categories to save tokens.

**Question 20.** The attribute schema currently requires a `material` field on every listing. Many listings (e.g., digital gift cards, services) have no physical material, and the model has started inventing plausible-sounding materials rather than reporting none.

Question: What schema change fixes this? (Select ONE response.)

- A) Remove the `material` field from the schema entirely.
- B) Lower the temperature to reduce invented values.
- C) Add a prompt instruction telling the model not to invent values.
- D) Make `material` nullable so genuine absence can be reported truthfully.

**Question 21.** Two enrichment passes on the same listing disagree on size: one reads "Large" and another reads "L," and there's no way to tell from the listing text which normalization the seller intended.

Question: What should the pipeline do? (Select ONE response.)

- A) Flag the field for human review with both candidate values and their source rather than silently picking one.
- B) Always trust whichever pass ran first.
- C) Discard the listing entirely since the data is unreliable.
- D) Average the two representations into a new hybrid value.

**Question 22.** The enrichment tool's JSON output occasionally fails to parse — about 4% of runs produce malformed JSON that crashes the downstream catalog loader.

Question: What is the most reliable fix? (Select ONE response.)

- A) Define a `submit_attributes` tool whose input schema matches the attribute structure, and read the data from the structured `tool_use` block instead of parsing free text.
- B) Ask for YAML output instead, since it tolerates minor formatting drift better.
- C) Add a JSON-repair library to patch common syntax issues before parsing.
- D) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.

**Question 23.** Since switching to strict schema-constrained tool use, enrichment output always parses successfully, but some listings end up with a `category` that doesn't match any `subcategory` in the fixed taxonomy tree.

Question: What should you conclude and do? (Select ONE response.)

- A) The schema needs stricter string types to fix this.
- B) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks category/subcategory consistency on top of schema compliance.
- C) max_tokens is too low, truncating output before the category is fully written.
- D) Abandon tool use and return to free-text extraction with manual review.

**Question 24.** A subset of incoming listings have only a low-quality seller photo and almost no text description. The pipeline currently sends only the sparse text to Claude, and enrichment quality is poor for these listings.

Question: What is the most direct fix? (Select ONE response.)

- A) Reject listings with insufficient text description from the pipeline entirely.
- B) Send the listing photo itself as an image content block alongside the enrichment instructions, using Claude's native vision input instead of relying solely on sparse text.
- C) Switch to a larger model, since bigger models are always better at inferring from little text.
- D) Increase max_tokens so the model can work harder on the sparse description.

**Question 25.** The pipeline needs to enrich five sections of a long, multi-variant listing (color options, size chart, care instructions, materials, shipping notes) concurrently to keep total latency reasonable.

Question: What must the integration layer support to do this? (Select ONE response.)

- A) Streaming, since only streaming supports running more than one request at a time.
- B) A single request with all five sections concatenated, since Claude parallelizes internally.
- C) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- D) The Batch API, since it's the only way to issue more than one request concurrently.

**Question 26.** Fernhaven plans to run the same enrichment pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted offering for different regional deployments.

Question: What should the team expect? (Select ONE response.)

- A) Bedrock-style vendor integrations require an entirely different prompting approach and schema design.
- B) Batch processing is unavailable through any third-party vendor integration.
- C) Enrichment accuracy and latency are guaranteed to be identical to the millisecond across vendors.
- D) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.

**Question 27.** The team enables extended thinking on a complex multi-step enrichment-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly? (Select ONE response.)

- A) Convert thinking output into an additional tool call automatically.
- B) Discard thinking content whenever a tool is also invoked in the same turn.
- C) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- D) Ignore thinking content entirely, since it never affects downstream turns.

**Question 28.** Finance asks for an accurate per-listing cost breakdown for the enrichment pipeline, but the current cost model only estimates based on average description length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- B) Only output tokens, since input is effectively free at this volume.
- C) A flat per-listing fee regardless of token usage.
- D) Only cache read tokens, since caching is the dominant cost driver.

**Question 29.** A new engineer argues the team can skip code review on the enrichment pipeline's application code since "the AI part is the risky part, not the plumbing."

Question: What is the correct response? (Select ONE response.)

- A) Review should be skipped for any code that primarily calls an external API.
- B) Only the prompt needs review; the surrounding code is low-risk by definition.
- C) Code review is unnecessary once the enrichment evals pass.
- D) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.

**Question 30.** A single long-running session is reused across an entire shift to enrich listings from many unrelated sellers, and the team notices Claude increasingly referencing attributes from unrelated earlier listings.

Question: What is the best fix? (Select ONE response.)

- A) Start a fresh session (or `/compact`) at natural task boundaries, such as between different sellers' batches, rather than accumulating unrelated context in one long session.
- B) Ask the model to "forget earlier listings" at the start of each new one.
- C) Increase the context window so more history fits without confusion.
- D) Reduce temperature to prevent cross-referencing.

---

## Scenario C: Cost/Latency Tuning for a Code-Review Assistant (Questions 31–45)

Ashgrove Systems runs an internal code-review assistant that comments on pull requests across dozens of repositories, processing thousands of diffs per day. Engineering leadership wants review comments fast and cheap for routine changes, while still catching subtle issues in the diffs that matter most.

---

**Question 31.** Most pull requests are small, routine changes (dependency bumps, formatting, minor refactors) where review is simple and extremely high-volume. Latency and cost per PR matter far more than catching rare, deeply subtle issues on every single diff.

Question: Which model tier best fits the default review path? (Select ONE response.)

- A) The highest-capability tier available, to guarantee nothing is ever missed.
- B) Whichever tier is cheapest per token, regardless of review quality on flagged diffs.
- C) The same tier used for the team's hardest architectural reviews, for consistency.
- D) A fast, low-latency tier suited to high-volume/low-complexity diffs, reserving a higher tier only for PRs flagged as higher-risk.

**Question 32.** A small fraction of PRs touch authentication, payment, or data-migration code, where the fast default model produces shallow, generic comments that miss real issues.

Question: What is the most targeted fix? (Select ONE response.)

- A) Route only the flagged high-risk PRs to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.
- B) Switch every PR to the highest-capability tier to be safe.
- C) Add many more few-shot examples to the fast model's prompt for every PR.
- D) Increase max_tokens for all PRs so comments can be longer.

**Question 33.** The assistant currently floats to "whatever model is latest" in production. After a routine model update, review comment tone and the issues it flags shifted noticeably with no code change on Ashgrove's side.

Question: What should the team do differently? (Select ONE response.)

- A) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- B) Disable all prompt caching to prevent drift.
- C) Roll back to the oldest available model version permanently.
- D) Accept the drift — behavior changes across releases require no process.

**Question 34.** Review comments need a consistent structure (issue, why it matters, suggested fix) but detailed prose instructions describing that structure haven't produced consistent output.

Question: What technique is most likely to help? (Select ONE response.)

- A) Ask the model to restate the structure before commenting.
- B) Write an even longer, more detailed prose description of the structure.
- C) Provide 2–3 few-shot examples demonstrating the exact desired comment structure.
- D) Lower the temperature to zero.

**Question 35.** A pull request has a very large diff (2,000+ changed lines). The team wants a maximally thorough review comment set and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) Long outputs are always truncated regardless of context window size.
- B) Output length has no measurable effect on latency.
- C) Input and output share the same context-window budget, so a very large diff leaves less room for a long comment set, and vice versa.
- D) None — input and output tokens are budgeted completely independently.

**Question 36.** The review prompt currently places the specific diff text before the general review instructions and desired comment format in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last always improves how carefully the model attends to them.
- B) Order has no effect on either consistency or caching.
- C) Reordering only affects cost, never comment consistency.
- D) Stable, role-defining instructions belong first, forming a consistent, cacheable prefix; diff-specific content should come after as the varying part.

**Question 37.** Finance wants to know exactly how much the review assistant costs per pull request, but the team currently estimates cost only from average diff size.

Question: What should be instrumented instead? (Select ONE response.)

- A) Number of files touched only, regardless of token count.
- B) Wall-clock review latency per PR, used as a cost proxy.
- C) A flat cost assumption based on lines-changed count.
- D) Actual token usage per request — input, output, and cache — attributed per PR, rather than an estimate from average diff size.

**Question 38.** An engineer writes an automated eval that asserts a review comment must exactly match a fixed reference string for a sample diff, and the eval fails intermittently even though the comments look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The eval needs a longer reference string to match against.
- B) Temperature should be increased to fix the intermittent failures.
- C) The model is broken and producing inconsistent answers.
- D) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.

**Question 39.** PR payloads include full raw CI-tool output (every linter warning, every dependency-audit line) that bloats the review prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix? (Select ONE response.)

- A) Switch to a model with a larger context window so the bloat matters less.
- B) Increase max_tokens to accommodate the extra data.
- C) Prune tool output to the relevant findings before they enter the prompt, rather than passing raw dumps.
- D) Summarize the CI output with a second Claude call before reviewing the diff.

**Question 40.** For very large diffs, the team notices review comments consistently miss issues in the middle files of the changeset while covering the first and last files well.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Add an instruction telling the model to "pay equal attention to every file."
- B) Alphabetize the changed files before reviewing.
- C) Put a brief overview of the changeset's structure at the start of the input and organize per-file content under clear headers, mitigating the tendency to attend most to the beginning and end of long inputs.
- D) Switch to a model with an even larger context window.

**Question 41.** A review comment confidently states that a function "already has a null check on this path," but on manual inspection the null check does not exist in the diff.

Question: What practice would most help catch this class of error before it reaches a developer? (Select ONE response.)

- A) Apply defensive parsing and skepticism toward confident claims — verify specific factual assertions (e.g., "already handled") against the actual diff rather than accepting fluency as correctness.
- B) Shorten review comments so there's less room for errors.
- C) Increase the model's temperature so comments sound less confident.
- D) Trust confident, fluent-sounding comments as evidence of correctness by default.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" for machine-readable findings still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach? (Select ONE response.)

- A) Repeat the JSON instruction more emphatically at the end of the prompt.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- C) Post-process every response to strip text before the first `{`.
- D) Increase max_tokens so there's room for both the preamble and the JSON.

**Question 43.** The team wants to add an exploratory step that scans a repository's broader codebase for context (related modules, prior patterns) before reviewing a diff, but worries the exploration will bloat the main review context with mostly-irrelevant detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Load the entire related codebase directly into the main review prompt every time.
- B) Skip broader-codebase context entirely to avoid the bloat risk.
- C) Have a subagent perform the codebase scan in an isolated context and return only a distilled, relevant summary to the main review step.
- D) Increase the context window so the full related codebase always fits.

**Question 44.** For the simplest, most common review type (formatting-only diffs), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- B) Multi-shot is always strictly better regardless of task simplicity.
- C) Zero-shot is required whenever latency matters at all.
- D) The choice has no effect on cost or latency.

**Question 45.** The review prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent drop in comment quality.

Question: What practice would have prevented this? (Select ONE response.)

- A) Only allowing one designated engineer to ever read the prompt.
- B) Rewriting the prompt from scratch every quarter.
- C) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- D) Locking the prompt so no one can ever change it again.

---

## Scenario D: MCP Servers for a Data-Engineering Team (Questions 46–60)

The data-engineering team at Cascade Logistics runs internal MCP servers exposing pipeline-status, data-catalog, and warehouse-query tools so that Claude Code sessions across the company can inspect ETL health and look up table schemas without engineers manually SSHing into anything.

---

**Question 46.** A new data analyst clones the team's dbt repository, but Claude Code doesn't apply the team's established SQL style conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) The conventions file exceeded a size limit and was silently truncated.
- B) CLAUDE.md requires an explicit `@import` from the repository root to take effect at all.
- C) The new analyst needs to run `/memory` to activate memory files.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.

**Question 47.** A nightly CI job invokes Claude Code to review dbt model changes and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The repository's CLAUDE.md is malformed.
- B) The CI runner lacks permission to call the Claude API.
- C) The dbt models are too large for Claude Code to process.
- D) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.

**Question 48.** A downstream dashboard parses Claude Code's pipeline-health summary with regex to populate a status page, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Run with `--output-format json` and a `--json-schema` defining the summary structure for machine-parseable output.
- B) Post the entire raw output as one block on the status page instead of parsing it.
- C) Harden the regex with more permissive fallback patterns.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** The team's `/audit-lineage` custom command prints thousands of lines of table-lineage data, and engineers report Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `argument-hint`, so engineers scope the lineage query more narrowly.
- B) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- C) Removing the command entirely.
- D) `allowed-tools`, restricting the command to read-only operations.

**Question 50.** An internal `/new-pipeline` skill is meant only to scaffold a new ETL job from a template, but an audit finds a session where it also ran shell commands that modified an unrelated production config file.

Question: What is the correct guardrail? (Select ONE response.)

- A) Require engineers to commit their work before running any skill.
- B) Add a warning in the skill's instructions telling Claude never to run shell commands.
- C) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 51.** An engineer needs to understand how a large, unfamiliar warehouse schema is structured before writing a new transformation, and worries that reading dozens of catalog entries will exhaust context before implementation begins.

Question: What is the best approach? (Select ONE response.)

- A) Skip exploration and infer the schema from table names alone.
- B) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- C) Split the work across two separate terminal windows.
- D) Read every catalog entry in one pass to be thorough.

**Question 52.** Mid-session, context is nearly full of verbose schema-discovery output, but the engineer still needs to write the transformation in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Delete the project CLAUDE.md temporarily to free context space.
- B) Continue working; Claude automatically discards irrelevant context.
- C) Start a brand-new session and rely on memory of what was learned.
- D) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.

**Question 53.** A multi-step Claude Code task that reads a pipeline config, calls the data-catalog MCP tool, and writes a remediation report produces a wrong final report. Trace logs show the config was read correctly and the catalog tool returned valid schema data.

Question: Where should debugging focus next? (Select ONE response.)

- A) The step between receiving the catalog tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- B) The network connection to the MCP server, since that's the most complex step.
- C) Re-read the pipeline config again, since that's the earliest step.
- D) Nothing — a wrong report with correct inputs means the task should simply be re-run.

**Question 54.** A warehouse-query tool integration fails, and the team can't tell whether the failure is in their integration code (bad credentials, wrong connection string) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Restart the CI runner and try again.
- B) Switch to a different model to see if the failure persists.
- C) Assume it's a model problem and rewrite the prompt.
- D) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.

**Question 55.** The pipeline-status information needs to be reachable from Claude Code sessions across the whole engineering org, not just the data team, and should be maintainable by the data-engineering team independently of any consuming application.

Question: What is the best approach? (Select ONE response.)

- A) Ask each engineer to curl the pipeline-status API manually when needed.
- B) Build an MCP server exposing pipeline-status operations as tools, shared across the org.
- C) Have each team paste warehouse credentials into their own CLAUDE.md.
- D) Hard-code pipeline-status logic into each team's custom skill separately.

**Question 56.** The data-catalog MCP server exposes both a `search_tables` tool and a way for agents to see what data domains exist without an exploratory search call.

Question: What is the second capability an example of? (Select ONE response.)

- A) A Claude Code Skill.
- B) A built-in tool provided by the platform automatically.
- C) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- D) An MCP tool, functionally identical to `search_tables`.

**Question 57.** The team is deciding whether the warehouse-query MCP server should run as a local stdio process on each engineer's machine or as a remote, centrally-hosted network service.

Question: What should drive the decision? (Select ONE response.)

- A) Remote servers cannot expose tools, only resources.
- B) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.
- C) MCP only supports one communication pattern, so there's no real decision to make.
- D) stdio servers are always faster regardless of deployment context.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a warehouse connection password hardcoded directly in the file.

Question: What is the correct fix? (Select ONE response.)

- A) Rotate the password weekly instead of removing it from the file.
- B) Move the password to environment-variable expansion (e.g., `${WAREHOUSE_PASSWORD}`) so the secret isn't committed to version control.
- C) Move `.mcp.json` to a private repository instead.
- D) Base64-encode the password before committing it.

**Question 59.** An audit finds that several MCP-connected warehouse tools grant broader access (e.g., full `DROP TABLE` rights) than any actual analytics workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- B) Add a confirmation prompt before any destructive statement.
- C) Add logging so misuse can be reviewed after the fact.
- D) Leave access as-is, since no misuse has been observed yet.

**Question 60.** The team is choosing how to expose a one-off, team-specific "weekly lineage report" workflow used by a single small team, versus a widely-reused "check pipeline SLA status" capability needed by every agent across the org.

Question: How should each be built? (Select ONE response.)

- A) Both as Skills, since Skills are always reusable.
- B) Both as MCP servers, since MCP is the correct choice for any shared capability.
- C) Both as built-in tools, since built-in tools require the least setup.
- D) The one-off lineage report as a Skill or custom tool scoped to that team; the widely-reused SLA-status capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.

---
# Answer Key

**Quick key:** 1-B, 2-C, 3-B, 4-C, 5-D, 6-B, 7-B, 8-A, 9-B, 10-D, 11-B, 12-A, 13-B, 14-D, 15-C, 16-C, 17-A, 18-C, 19-A, 20-D, 21-A, 22-A, 23-B, 24-B, 25-C, 26-D, 27-C, 28-A, 29-D, 30-A, 31-D, 32-A, 33-A, 34-C, 35-C, 36-D, 37-D, 38-D, 39-C, 40-C, 41-A, 42-B, 43-C, 44-A, 45-C, 46-D, 47-D, 48-A, 49-B, 50-C, 51-B, 52-D, 53-A, 54-D, 55-B, 56-C, 57-B, 58-B, 59-A, 60-D

---

**1. B** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"`, stop at `"end_turn"`. Text phrases (A) are unreliable, a fixed cap (C) is a backstop rather than the primary signal, and a non-empty payload (D) doesn't indicate the model is done reasoning.

**2. C** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate it. A and B keep the result out of the model's direct reasoning path; D misuses the system prompt for turn-level data.

**3. B** — A compliance-critical rule needs deterministic enforcement via a hook that blocks the call outright when the CRM flag is set. A, C, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed with normal tool choice. `tool_choice: "any"` (B) guarantees some tool call, but not which one; A and D are probabilistic.

**5. D** — Removing tools unrelated to the agent's core research role (or splitting them into a separate agent) directly reduces the candidate set the orchestrator must reason over. A adds prompt overhead without removing bloat; B and C don't address the underlying tool-selection problem.

**6. B** — Structured error metadata (category, retryable flag, description) lets the agent respond appropriately to each failure type. Blanket retry (A) wastes calls on non-retryable failures; asking the model to guess (C) is worse than the tool reporting it; D reduces frequency without fixing the missing information.

**7. B** — "No news found" is a valid empty result, not a failure — return success with an empty list. A patches symptoms while the underlying success/error conflation remains; C invents an unnecessary extra step; D hides real signal from the session.

**8. A** — High-ambiguity research where the right tools and order depend on intermediate findings is the core case for model-driven selection. B, C, and D are unsupported claims about the technology.

**9. B** — A narrowly-scoped subagent with only the outreach tool and explicit criteria minimizes accidental sends while the main agent reasons about unrelated tools. A, C, and D are unsupported or overgeneralized technical claims.

**10. D** — Delegating research gathering to a subagent that returns a distilled summary keeps the main agent's context focused on synthesis. A and B don't address the root accumulation problem; C removes needed capability.

**11. B** — A structured summary of what was checked, found, and any gaps lets the AE act with confidence. A omits how the brief was produced; C forces reconstruction from a raw transcript; D conveys a number without substance.

**12. A** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, C, and D are unsupported absolute claims.

**13. B** — Task predictability versus dependency on intermediate findings is the deciding factor between workflow and agent patterns, not tool count, language, or runtime speed.

**14. D** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. A, B, and C misdiagnose the cause.

**15. C** — A per-prospect send-count hook is the only option that deterministically guarantees the daily limit; A, B, and D remain probabilistic prompt-level guidance.

**16. C** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. A and D don't reduce per-token cost the same way; B risks degrading quality without addressing the actual cost lever.

**17. A** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request. B, C, and D misidentify the actual limitation.

**18. C** — Streaming supports incremental rendering, reducing perceived latency for a live "enriching" indicator. A and D don't address perceived latency; B is the wrong API for this use case.

**19. A** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. B, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. A discards the field's value entirely; B and C rely on probabilistic compliance.

**21. A** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. B, C, and D all discard information or guess.

**22. A** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. B and C are recovery layers for a problem that can be eliminated; D is a retry loop around a still-fragile format.

**23. B** — Schema validity guarantees syntax, not semantics; a separate validation step checking category/subcategory consistency is needed on top. A, C, and D misdiagnose or abandon a working mechanism.

**24. B** — Sending the image directly as a vision content block bypasses the sparse-text bottleneck entirely. A discards otherwise-processable listings; C and D don't address the actual data-quality gap.

**25. C** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. A, B, and D misstate how concurrency is actually achieved.

**26. D** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**27. C** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and D mishandle or misdescribe this.

**28. A** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-listing cost breakdown. B, C, and D all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. A** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. B is unreliable prompt-level mitigation; C doesn't address cross-contamination; D is an unrelated lever.

**31. D** — High-volume, low-complexity PRs fit a fast, low-latency tier, with a higher tier reserved for flagged higher-risk cases — matching capability to actual task difficulty. A and C overspend by default; B ignores review-quality fit entirely.

**32. A** — Targeted routing of only the flagged high-risk PRs to a higher tier addresses the actual gap without overspending on the high-volume routine path. B, C, and D apply broad, costly fixes to a narrow problem.

**33. A** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. B and C are unhelpful overcorrections unrelated to the actual fix; D accepts avoidable risk.

**34. C** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked. A and D don't reliably fix structural consistency; B repeats a failed approach.

**35. C** — Input and output share one context-window budget, so a large diff directly constrains available comment length and vice versa. A, B, and D misstate this relationship.

**36. D** — Stable instructions first (ideally cacheable) and variable diff content after both improves consistency (clear role separation) and caching. A, B, and C misstate the effect of ordering.

**37. D** — Actual per-request token usage (input/output/cache) attributed per PR gives an accurate cost picture; estimates from diff size or unrelated proxies (A, B, C) don't.

**38. D** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A, B, and C misdiagnose the cause.

**39. C** — Pruning to relevant findings before data enters the prompt removes the actual bloat at its source. A, B, and D work around or add cost around a problem solvable by simple filtering.

**40. C** — Placing a brief overview up front and organizing per-file detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A and B don't address the underlying attention pattern; D is costly and doesn't guarantee the effect disappears.

**41. A** — Verifying specific factual claims against the actual diff catches confident-but-wrong comments that fluency alone would let through. B, C, and D don't address correctness.

**42. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A, C, and D are workarounds for a problem that can be structurally eliminated.

**43. C** — An isolated subagent scan returning a distilled summary keeps codebase-scan bloat out of the main review context while still providing relevant findings. A and D reintroduce the bloat risk; B discards potentially useful context entirely.

**44. A** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. B and C are absolute claims that don't hold generally; D is false.

**45. C** — Versioning prompts like code enables attribution and rollback for quality regressions. A, B, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. D** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. D** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. A, B, and C would typically produce different, more specific failure signatures.

**48. A** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. B, C, and D are reactive or abandon the structured-output requirement.

**49. B** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A and D narrow scope or capability but don't isolate output destination; C removes useful functionality.

**50. C** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A mitigates damage rather than preventing it; B is probabilistic and the violation already happened despite instructions; D is a false claim about slash commands.

**51. B** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A guesses instead of investigating; C doesn't share context between windows meaningfully; D floods context directly.

**52. D** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A frees trivial space while losing standards; B describes behavior that doesn't exist; C discards findings.

**53. A** — Since the config and catalog data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. B and C re-check already-verified steps; D skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A, B, and C guess without diagnosis.

**55. B** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. A, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, B, and D mischaracterize this capability.

**57. B** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, C, and D are false or oversimplified claims about MCP's communication patterns.

**58. B** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A and D don't remove the exposed credential from history or ongoing risk; C doesn't remove the credential either.

**59. A** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. B and C are detective/compensating controls; D accepts unnecessary risk.

**60. D** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. A, B, and C force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 8.*
