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

- A) Continue looping while `stop_reason` comes back as `"tool_use"`, and stop once a response arrives with `stop_reason: "end_turn"`.
- B) Stop the loop the first time `find_contacts` returns any result, on the assumption that contact data is always the last thing a brief needs.
- C) Stop the loop once a fixed five-second timer elapses, regardless of whether any tool calls are still in flight.
- D) Stop the loop as soon as the response text contains a word like "brief," treating that specific phrasing as a reliable completion signal.

**Question 2.** After `pull_funding_data` runs, what must the integration code do so Claude can correctly reason about the result on the next turn?

- A) Insert the raw funding data directly into a new system prompt for the rest of the session so Claude treats it as a standing instruction.
- B) Append a `tool_result` block referencing the matching `tool_use` ID to the conversation, then resend the conversation so far to the model.
- C) Store the funding data only in the CRM database, trusting the model to reconstruct what it needs from context on the next pass.
- D) Start a new session and paste a short summary of the funding data in as the first user message of that fresh session.

**Question 3.** Meridian's policy requires that contacts from EU-based companies never be surfaced with personal emails unless a consent flag is set. The rule is stated clearly in the system prompt, but logs show occasional violations. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt so the model sees it twice per turn.
- B) Add a hook that intercepts `find_contacts` output and redacts personal emails for EU contacts lacking a consent flag.
- C) Add several few-shot examples of correctly redacting EU contacts before surfacing them to the rep.
- D) Lower the model's temperature so it follows the stated consent policy more consistently across calls.

**Question 4.** The team wants `classify_account_tier` to always run first, with no exceptions, before any other tool.

Question: What is the most reliable implementation?

- A) Set `tool_choice: {"type": "tool", "name": "classify_account_tier"}` on the first request, then use normal tool choice afterward.
- B) State in the system prompt that `classify_account_tier` must always run before any other tool, with no exceptions.
- C) Set `tool_choice: "any"` on the first request so that some tool call is guaranteed to happen up front.
- D) Add several few-shot examples showing a transcript where the classification tool is called before anything else.

**Question 5.** The research agent has grown to 14 tools, including several rarely-used ones (expense-report lookup, internal HR directory) unrelated to sales research. Tool selection has become unreliable.

Question: What is the best fix?

- A) Increase `max_tokens` so the agent has more room to reason through which of the 14 tools to pick each turn.
- B) Add a system prompt note listing which of the 14 tools are "primary," while leaving all of them available.
- C) Add more few-shot examples showing correct tool selection across the full set of 14 tools.
- D) Remove or scope out the tools that are unrelated to the agent's core sales-research role.

**Question 6.** `find_contacts` currently returns the string `"Error"` for every possible failure — invalid domain, permission denied, or directory-service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Wrap every call in an automatic retry policy that resends the same request up to three times.
- B) Add a system prompt instruction telling the agent to validate and infer the failure type itself from surrounding context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the directory service's timeout threshold so timeout-related failures happen less often.

**Question 7.** When `find_contacts` finds no matching contacts at a target account, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Have the agent call `lookup_company` first to check whether contacts should plausibly exist before searching.
- B) Add a hook that suppresses the error message and silently ends the conversation instead of surfacing anything.
- C) Return a successful response with an empty result set, reserving actual errors for genuine access failures.
- D) Add a system prompt note explaining to the model that this particular error usually just means no contacts matched.

**Question 8.** An engineer proposes replacing the agent's reasoning with a fixed sequence: always call `lookup_company`, then `pull_funding_data`, then `find_contacts`. They argue this makes behavior predictable.

Question: Why is model-driven tool selection the better fit for account research?

- A) Model-driven selection is always cheaper, since it skips the reasoning tokens a fixed sequence would otherwise spend.
- B) The Claude Agent SDK is technically incapable of executing a fixed, hardcoded tool sequence at all.
- C) Research needs vary by account and depend on intermediate findings, which a fixed sequence can't adapt to.
- D) A fixed sequence can only invoke Anthropic's built-in tools, not an organization's own custom tools.

**Question 9.** The team is deciding whether to give the main research agent a `send_outreach_email` tool directly or delegate it to a separate, narrowly-scoped subagent. Sending outreach has real cost (reaching a real prospect) and should only happen under specific approval criteria.

Question: What is the strongest argument for a separate, narrowly-scoped subagent?

- A) Subagents are required by the platform any time a tool has real-world side effects on external systems, such as sending email, issuing refunds, or modifying production records.
- B) Scope a separate subagent to only the email tool and approval criteria, so more research tools later don't increase the odds of an accidental send.
- C) The main agent's context window is technically too small to hold the email tool's schema alongside the others.
- D) Subagents execute measurably faster than the same tool called directly by the main agent.

**Question 10.** During research on a large enterprise account, the agent's context fills with raw funding-database dumps, leaving little room for reasoning about which contacts to prioritize.

Question: What is the best structural fix?

- A) Increase `max_tokens` so the final response has more room to summarize everything that came before it.
- B) Read only the first 50 rows of every funding-data result, discarding the rest before it reaches the model.
- C) Delegate the funding-data lookup to a subagent that returns a distilled summary of the relevant findings.
- D) Disable funding lookups entirely and rely on `find_contacts` output alone for prioritization.

**Question 11.** After a call brief is built, the account executive has no visibility into what the agent tried or found — logs show 15 minutes of tool calls with no accessible summary.

Question: What should the handoff to the rep include?

- A) The full raw transcript of every tool call and result, since it is already a structured, chronological record.
- B) Just the final error message from the session, on the assumption the rep can re-investigate from there.
- C) A sentiment analysis estimating how promising the account seemed based on tone of the findings.
- D) A structured handoff summary: what was researched, what was found, and a recommended talking point.

**Question 12.** The team is deciding between running the research agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on their own infrastructure.

Question: What is the core tradeoff?

- A) The tradeoff is operational control (self-hosted) versus operational burden (managed).
- B) Self-hosted agents are architecturally incapable of using any custom, organization-defined tools, since only a managed environment can register tool schemas at all.
- C) Managed agents are inherently less secure than self-hosted ones regardless of configuration, network isolation, or credential scoping.
- D) Managed agents are structurally unable to reach any private infrastructure at all, even through an outbound gateway or VPN peering.

**Question 13.** An engineer asks whether the account-research task should be built as a fixed workflow or an agent.

Question: What is the deciding factor?

- A) Whether the task involves calling more than three distinct tools in a single session, since workflows are defined by a fixed tool count.
- B) Whether the engineering team prefers writing the integration in Python or in TypeScript, since each language favors a different pattern.
- C) Whether the task's tool calls need to complete in under 30 seconds end to end, since agents are assumed to be inherently slower.
- D) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.

**Question 14.** The `AgentDefinition` for a proposed "contact-finder subagent" has a vague description: "Finds people." The main agent rarely delegates to it even when contact lookup is clearly needed.

Question: What is the most likely cause and fix?

- A) Rewrite the description to state specifically what the subagent does and when to use it.
- B) The subagent needs more capability; add several more directory-related tools to its `AgentDefinition` so it can handle a wider range of contact-lookup requests.
- C) Subagents cannot receive delegated work unless they are separately registered inside `.mcp.json` alongside every MCP server the team runs.
- D) The main agent's temperature setting is too low for it to consider delegating work at all, so raising it should restore normal delegation behavior.

**Question 15.** The team wants a hard guarantee that `send_outreach_email` is never called more than once per contact per day, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism?

- A) A hook that tracks per-contact call counts and timestamps, and blocks the tool call once the daily limit is reached.
- B) A system prompt instruction stating the once-per-contact-per-day limit clearly and unambiguously.
- C) A note appended to the tool's description mentioning the once-per-day limit for reference.
- D) Several few-shot examples showing a transcript where the agent stops after one email per contact.

---

## Scenario B: Product-Catalog Enrichment Pipeline for an Online Marketplace (Questions 16–30)

Fernhollow Marketplace runs a catalog enrichment pipeline that generates product descriptions, assigns categories, and extracts attributes (size, material, color) from seller-submitted text and images. It handles both interactive single-listing requests and nightly batch jobs covering hundreds of thousands of listings.

---

**Question 16.** The nightly job processes 200,000 listings with no user waiting on the result, and no step needs the model to call a tool mid-request.

Question: Which API best fits, and why?

- A) The synchronous Messages API paired with a smaller model chosen specifically to reduce per-listing cost.
- B) The synchronous Messages API run in parallel across many worker threads, to finish the run as fast as possible.
- C) The synchronous Messages API with `max_tokens` reduced to the smallest value that still fits a listing.
- D) The Message Batches API — latency-tolerant, non-blocking, high-volume work at a lower per-token cost.

**Question 17.** An engineer wants to add an "extract attributes, validate against taxonomy, retry failed attributes" loop to the batch pipeline, and proposes running the whole loop through the Batch API for its cost savings.

Question: Why won't this work as designed?

- A) The Batch API strips schema and tool definitions from every request, so structured validation calls can't be sent at all, even in a single turn.
- B) The Batch API can't run a validation call mid-request and feed the result back within one request.
- C) The Batch API's 24-hour completion window makes any kind of retry logic structurally impossible to implement, regardless of how the retries are scheduled.
- D) The Batch API's context window is too small to hold a single listing's description text alongside the taxonomy and style guide.

**Question 18.** The interactive single-listing flow shows sellers a real-time progress indicator while Claude enriches their upload.

Question: What technique best supports this user experience?

- A) The Batch API, since it was specifically designed to provide real-time progress feedback to end users.
- B) Increasing `max_tokens` so the complete, final response is generated and returned to the seller sooner.
- C) Polling the Batch API's status endpoint once per second until the enrichment job completes.
- D) Streaming, so the UI can render output incrementally as it's generated and reduce perceived latency.

**Question 19.** Every request sends the same 5,000-token attribute taxonomy and style guide, followed by the listing-specific text, which varies per request.

Question: What optimization most directly reduces both latency and cost across many requests?

- A) Move the taxonomy into a few-shot example block instead of its own dedicated section of the prompt.
- B) Place the stable taxonomy and style guide first, enable prompt caching, and put the varying listing text last.
- C) Truncate the taxonomy down to only its most commonly needed categories to save tokens.
- D) Switch to the smallest available model, accepting whatever drop in extraction quality results.

**Question 20.** The schema requires a `material` field on every listing. Many listings genuinely don't specify material, and the model has started inventing plausible-sounding materials rather than reporting unknown.

Question: What schema change fixes this?

- A) Remove the `material` field from the schema entirely so the model is never asked for a value it can't validate.
- B) Add a prompt instruction telling the model not to invent a value when the material isn't stated.
- C) Lower the temperature on extraction calls to reduce how often invented values appear.
- D) Make `material` nullable in the schema so its genuine absence can be reported truthfully instead of guessed.

**Question 21.** Two extraction passes on the same listing disagree on garment size — one reads "M" and another "Medium (US 8–10)" — and there's no way to tell which is more precise from context alone.

Question: What should the pipeline do?

- A) Automatically keep whichever value the first extraction pass happened to produce, since the earliest pass is assumed to be the most reliable source.
- B) Flag the field for human review with both candidate values and their source.
- C) Average the two values numerically to produce a single reconciled size figure that splits the difference between the two readings.
- D) Discard the entire listing from the catalog since its attribute data can no longer be trusted after a single disagreement.

**Question 22.** The extraction tool's JSON output occasionally fails to parse — about 4% of listings produce malformed JSON that crashes the catalog loader.

Question: What is the most reliable fix?

- A) Wrap the parse step in a try/catch and retry the same request with "valid JSON only" appended to the prompt, hoping the retry produces cleaner output the second time around.
- B) Add a JSON-repair library to the pipeline that patches common syntax issues, such as trailing commas or unescaped quotes, before the parser runs.
- C) Define a `submit_attributes` tool and read data from the structured `tool_use` block instead of parsing free text.
- D) Switch the requested output format to YAML instead, since it tends to tolerate formatting drift better than JSON does.

**Question 23.** Since switching to strict schema-constrained tool use, attribute output always parses successfully, but some listings have a `sale_price` value that is higher than the listed `price`, even though both fields pass schema validation.

Question: What should you conclude and do?

- A) Strict schemas eliminate semantic errors the same way they eliminate syntax errors, so no further action is needed here — both classes of error are covered by the same validation pass.
- B) Add a validation step checking logical constraints, such as `sale_price` ≤ `price`, on top of schema compliance.
- C) `max_tokens` is set too low for these listings, which is truncating the structured output mid-generation before the price fields are written.
- D) Abandon tool use for this field entirely and go back to free-text extraction with mandatory human review of every single listing.

**Question 24.** A subset of listing photos have overlaid seller text (size charts, care instructions) that a separate OCR pass on the image often garbles, and extraction quality is poor when only that OCR text is sent to Claude.

Question: What is the most direct fix?

- A) Reject listings with any overlay text from the pipeline entirely rather than risk a bad extraction, even though most of that listing's other attributes are otherwise fine.
- B) Send the listing image itself as a vision content block instead of relying solely on OCR text.
- C) Increase `max_tokens` so the model has more room to reason through the degraded, garbled OCR text before producing its final attribute output.
- D) Switch to a larger model on the assumption that bigger models are always better at reading noisy, garbled text regardless of the input format.

**Question 25.** The pipeline needs to enrich five attribute categories (color, size, material, style, care) of a multi-variant listing concurrently rather than one at a time, to keep latency reasonable.

Question: What must the integration layer support to do this?

- A) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.
- B) Streaming, since a streamed response is the only mechanism the API offers for handling more than one thing at once.
- C) The Batch API, since it's the only supported way to have more than one request outstanding at a time.
- D) A single request with all five categories concatenated together, relying on Claude to parallelize the work internally.

**Question 26.** The marketplace plans to run the enrichment pipeline through both the direct Anthropic API and a third-party cloud vendor's hosted version of the model, for regional compliance reasons.

Question: What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) The third-party vendor requires an entirely different prompting approach and a completely redesigned schema.
- C) Batch-style processing is structurally unavailable on every third-party vendor integration.
- D) Extraction accuracy and per-request latency are guaranteed to be identical to the millisecond across vendors.

**Question 27.** The team enables extended thinking on a complex multi-step categorization-and-validation task that uses tool calls across several turns.

Question: What must the integration layer do correctly?

- A) Ignore the thinking content block entirely, since it structurally never affects any downstream turn or subsequent tool call.
- B) Convert the thinking output into an additional tool call before continuing the rest of the conversation.
- C) Discard the thinking content, but only on turns where a tool call also happens to be present in the same response.
- D) Handle the thinking block as distinct from the final answer text, preserving it across the multi-turn conversation.

**Question 28.** Finance asks for an accurate per-listing cost breakdown for the enrichment pipeline, but the current cost model only estimates based on average prompt length.

Question: What should the improved cost model account for separately?

- A) Only cache read tokens, on the assumption that caching alone is the dominant driver of total cost.
- B) Only output tokens, on the assumption that input tokens are effectively free for this workload.
- C) A flat per-listing fee applied uniformly, regardless of how many tokens any individual listing actually used.
- D) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.

**Question 29.** A new engineer argues that once Claude is integrated, the team can skip code review on the enrichment pipeline's application code since "the AI part is the risky part."

Question: What is the correct response?

- A) Code review should be skipped for any code whose primary job is calling an external API, since the vendor is responsible for that code's correctness.
- B) Code review becomes unnecessary once the pipeline's evals are passing consistently, since eval coverage substitutes for a human reading the code.
- C) Only the prompt itself needs review; the surrounding application code is low-risk by definition once an LLM is in the loop.
- D) Standard SDLC practices — review, testing, version control — still apply to the code around Claude.

**Question 30.** A single long-running session is used across an entire day to enrich unrelated catalogs from different sellers, and the team notices Claude increasingly referencing details from an unrelated earlier seller's listings.

Question: What is the best fix?

- A) Reduce temperature on the enrichment calls specifically, on the theory that lower randomness stops the model from wandering back to earlier sellers.
- B) Increase the context window so more prior history fits, trusting that the already-structured conversation lets Claude filter out unrelated sellers on its own.
- C) Start a fresh session (or `/compact`) at natural task boundaries between sellers' catalogs.
- D) Add a hook that clears the conversation whenever the response text happens to mention a seller name for the second time in a row.

---

## Scenario C: Cost/Latency Tuning for a Code-Review Assistant (Questions 31–45)

Ridgeline DevTools runs a code-review assistant that fires on every pull request across dozens of internal repos, generating inline comments and a review summary. Given the CI volume, cost, latency, and consistency all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most PRs are small and the review task is straightforward; latency and cost per PR matter far more than handling rare, deeply architectural changes well.

Question: Which model tier best fits the default path?

- A) The highest-capability tier available for every PR, to guarantee quality regardless of complexity.
- B) A fast, low-latency tier suited to high-volume/low-complexity review, reserving a higher tier only for PRs flagged as complex.
- C) Whichever tier happens to be cheapest per token that billing cycle, independent of task fit.
- D) The same tier the company uses for its hardest reasoning tasks, applied here for consistency across teams.

**Question 32.** A small fraction of PRs require deep multi-file reasoning (a cross-service refactor) where the fast default model produces shallow comments.

Question: What is the most targeted fix?

- A) Add more few-shot examples covering cross-service refactors to the fast model's prompt, so it handles every PR, complex or not, more thoroughly without changing which model runs.
- B) Switch every PR in the pipeline permanently to the highest-capability tier, just to be safe against occasional edge cases like this one.
- C) Increase `max_tokens` across the board so every review, simple or complex, has more room to be written out in full.
- D) Route only the flagged complex PRs to a higher tier, keeping the fast path otherwise.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, review tone and comment structure shifted noticeably without any code change.

Question: What should the team do differently?

- A) Nothing — floating to the latest model is deterministic enough that behavior shouldn't shift release to release.
- B) Roll back permanently to the oldest model version the vendor still supports and never move forward again.
- C) Disable all prompt caching across the pipeline, since caching is the most likely cause of the tone shift.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Reviews need a consistent structure (summary, issues by severity, suggested fix) but detailed prose instructions describing the structure haven't produced consistent output.

Question: What technique is most likely to help?

- A) Write an even longer, more exhaustively detailed prose description of the exact structure wanted.
- B) Lower the temperature to zero across every review request, regardless of the structural drift's cause.
- C) Provide 2–3 few-shot examples demonstrating the exact desired structure, optionally at a lower temperature to further limit drift.
- D) Ask the model to restate the structure it plans to use before it starts writing the actual review.

**Question 35.** A PR diff is very large (2,000+ changed lines). The team wants a maximally detailed review and considers requesting a very long output to match.

Question: What tradeoff must they account for?

- A) Input and output tokens draw from the same context-window budget, so a long diff leaves less room for a long review.
- B) None — input tokens and output tokens are budgeted from two completely independent pools, so a 2,000-line diff and a 20-line diff leave exactly the same room for the review either way.
- C) Output length has no measurable effect on end-to-end request latency in practice, regardless of how many tokens the review ultimately generates.
- D) Long outputs are always truncated by the API regardless of how large the model's context window actually is.

**Question 36.** The review prompt currently places the PR diff before the general review instructions and desired format in every request.

Question: Why might reordering improve both consistency and cacheability?

- A) Option order has no measurable effect on either output consistency or cache behavior, since the model reads the entire prompt before generating anything.
- B) Placing instructions last always improves how much attention the model pays to them, regardless of what precedes them.
- C) Stable, role-defining instructions belong in the system prompt or first, forming a cacheable prefix; the diff goes after as the varying part.
- D) Reordering the prompt only ever affects token cost, never output consistency, since consistency is purely a function of the instructions' wording.

**Question 37.** Finance wants to know exactly how much the review service costs per PR, but the team currently estimates cost only from average diff size.

Question: What should be instrumented instead?

- A) Wall-clock latency per PR, used as a stand-in proxy for actual token-based cost, on the theory that slower requests always cost more per token.
- B) The raw number of API calls made per PR, regardless of how many tokens any individual call actually consumed.
- C) Actual token usage per request — input, output, and cache, any of which can increase independently — attributed per PR.
- D) A flat cost assumption derived from the number of lines changed in each PR, independent of what the model actually read or wrote.

**Question 38.** An engineer writes an automated eval that asserts the review output must exactly match a fixed reference string for a sample PR, and the eval fails intermittently even though the reviews look correct on manual review.

Question: What is the most likely issue with the eval design?

- A) The model itself is broken and is intermittently producing genuinely wrong answers, which manual review is simply failing to catch each time.
- B) Exact-string-match evals are the wrong tool for non-deterministic output; check for required content/structure instead.
- C) The reference string needs to be normalized to a longer form that validates every acceptable phrasing up front.
- D) Temperature should be increased on the eval calls specifically, on the theory that more randomness will make the eval's pass rate more stable over time.

**Question 39.** PR metadata dumps (every CI check, every commit timestamp, every file mode change) bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

Question: What is the best fix?

- A) Increase `max_tokens` so the model has enough room to work through the extra metadata.
- B) Switch to a model with a larger context window so the metadata bloat matters less per request.
- C) Prune tool/data output to the relevant fields before they enter the prompt, rather than passing raw dumps.
- D) Summarize the metadata with a separate Claude call before the actual review call runs.

**Question 40.** For very large diffs, the team notices reviews consistently miss issues in files in the middle of the diff while covering the first and last files well.

Question: What is the most effective mitigation?

- A) Switch to a model with an even larger context window, on the assumption that raw window size alone resolves an attention pattern rather than a capacity limit.
- B) Add a plain instruction telling the model to "pay equal attention to the whole diff" every single time, regardless of diff length.
- C) Alphabetize the file list before sending the diff so the ordering is at least deterministic and consistent across runs.
- D) Put a key-facts summary at the start and organize detail under clear section headers.

**Question 41.** A review confidently states that a function "already has null checks" that, on manual inspection, don't actually exist in the diff.

Question: What practice would most help catch this class of error before it reaches the PR?

- A) Validate confident-sounding claims against the source diff rather than accepting fluency as correctness.
- B) Trust confident, fluent-sounding output as sufficient evidence of correctness by default, since a model that writes clearly is also generally reasoning correctly.
- C) Increase the model's temperature so its answers read as less confident and overstated, on the theory that hedged language is less likely to be wrong.
- D) Shorten the review output so there is simply less room for a claim like this to appear anywhere in it.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

Question: What is the more reliable approach?

- A) Use tool-use/schema-constrained output, enforced by the API mechanism rather than requested through prose or nudged along with temperature.
- B) Repeat the same JSON instruction even more emphatically at both the start and end of the prompt.
- C) Post-process every response to strip out any text that appears before the first `{` character.
- D) Increase `max_tokens` so there's guaranteed room for both the preamble and the full JSON body.

**Question 43.** The team wants to add an exploratory step that scans a repo's full commit history for related past bugs before reviewing the current PR, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach?

- A) Load the entire commit history directly into the main review prompt on every single run, regardless of how far back the relevant bug history actually goes.
- B) Skip historical context entirely, accepting the loss of a potentially useful signal in order to avoid the bloat risk altogether.
- C) Move to a model with a large enough context window that the full history always fits without any pruning at all.
- D) Have a subagent scan history in isolation and return a distilled summary to the main review step.

**Question 44.** For the simplest, most common review type (formatting-only lint fixes), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice?

- A) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper.
- B) Multi-shot prompting is strictly better than zero-shot in every case, regardless of the task's actual simplicity, because more examples always improve output quality on any task.
- C) Zero-shot is mandatory whenever latency matters at all, no matter how inconsistent the resulting lint-fix output turns out to be across runs.
- D) The choice between zero-shot and multi-shot has no measurable effect on either cost or latency, since both approaches send roughly the same number of tokens.

**Question 45.** The review prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent quality regression.

Question: What practice would have prevented this?

- A) Treat the review prompt and system prompt as versioned artifacts, similar to code, so changes are tracked and attributable.
- B) Locking the prompt file so that no engineer, including its original author, can ever change it again.
- C) Restricting prompt edits to a single designated engineer who is the only person allowed to read it.
- D) Rewriting the entire prompt from scratch every quarter regardless of whether anything is actually wrong with it.

---

## Scenario D: MCP Servers for a Data-Engineering Team (Questions 46–60)

Cascade Analytics has a 40-engineer data-engineering team that uses Claude Code alongside internal MCP servers for warehouse queries, pipeline status, and a data catalog. You lead team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new engineer clones the team's dbt repository, but Claude Code doesn't apply the team's established SQL style conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause?

- A) The new engineer needs to run `/memory` once to activate the memory files that ship with the repository.
- B) CLAUDE.md requires an explicit `@import` statement from the project root before it will take effect at all.
- C) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- D) The conventions file exceeded an internal size limit and was silently truncated on checkout.

**Question 47.** A nightly CI job invokes Claude Code to review dbt model changes and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause?

- A) The pull requests being reviewed are simply too large for Claude Code to process in CI, so the process stalls trying to read the full diff.
- B) The CI runner's service account lacks permission to call the Claude API at all, which would normally surface as an authentication error rather than a silent hang.
- C) The job is missing `-p`/`--print` (headless mode), so it waits on interactive input the runner never provides.
- D) The repository's CLAUDE.md file is malformed and fails to parse during startup, blocking the session before any review work begins.

**Question 48.** A downstream service parses Claude Code's pipeline-review output with regex to post inline comments on dbt pull requests, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix?

- A) Harden the existing regex with additional, more permissive fallback patterns for common drift cases.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure for machine-parseable output.
- C) Post the entire raw, unstructured output as a single PR comment instead of attempting to parse it at all.
- D) Add a stronger prompt instruction telling the model never to deviate from the expected format.

**Question 49.** The team's `/audit-lineage` custom command prints thousands of lines of table-lineage graph data, and engineers report that Claude's answers about their actual task get noticeably worse right after running it.

Question: What frontmatter change fixes this?

- A) `allowed-tools`, restricting the command so it can only perform read-only operations against the lineage graph and never write anything back.
- B) `argument-hint`, so engineers are nudged to scope the lineage analysis more narrowly up front before running the command at all.
- C) `context: fork`, so the verbose output stays isolated and only a summary returns.
- D) Removing the `/audit-lineage` command from the repository entirely, even though other engineers rely on it regularly.

**Question 50.** An internal `/scaffold-pipeline` skill is meant only to create new files from a template, but an audit finds a session where it also ran shell commands that modified unrelated files.

Question: What is the correct guardrail?

- A) Add a warning inside the skill's own instructions telling Claude never to run shell commands, and trust it to follow that instruction every time.
- B) Configure `allowed-tools` to permit only file-creation, making Bash unavailable during execution.
- C) Require engineers to commit all of their work before running any skill, so unrelated file changes can at least be diffed and reverted afterward.
- D) Convert the skill into a slash command instead, since slash commands are structurally unable to run tools of any kind.

**Question 51.** An engineer needs to understand how a complex data-lineage flow crosses an unfamiliar warehouse schema before making a change, and worries that reading dozens of model files will exhaust context before implementation begins.

Question: What is the best approach?

- A) Use the Explore subagent for discovery, so exploration stays isolated and only a summary returns.
- B) Read every file in the schema in a single continuous pass to be as thorough as possible before writing any implementation code at all.
- C) Skip exploration entirely and infer the schema's shape from the model files' table names alone, without opening any of the files themselves.
- D) Split the discovery and implementation work across two separate terminal windows running independently, with no shared context between them.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the pipeline change in the same session and wants to preserve key findings.

Question: What should they do?

- A) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- B) Start a brand-new session and rely on personal memory of what was learned during discovery.
- C) Delete the project's CLAUDE.md file temporarily to free up additional context space.
- D) Continue working as-is, since Claude automatically discards context it judges to be irrelevant.

**Question 53.** A multi-step Claude Code task that reads a pipeline config, calls the warehouse-query MCP tool, and writes a report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Question: Where should debugging focus next?

- A) Re-read the pipeline config file a second time, since that was the earliest step in the task and the most likely place for a stale read to have occurred.
- B) The step between receiving the MCP tool's valid data and producing the final report, since both prior inputs were already confirmed correct.
- C) The network connection between Claude Code and the MCP server, since that's the most technically complex step in the whole pipeline.
- D) Nothing further — a wrong final report with confirmed-correct inputs means the task should simply be re-run and hope for a better outcome.

**Question 54.** A pipeline-status tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

Question: What is the correct first diagnostic step?

- A) Assume the failure is a model problem up front and start rewriting the prompt immediately, without first checking what the integration code actually sent.
- B) Examine the trace of what was actually sent and received to isolate the integration layer from the model's output.
- C) Switch to a different model entirely and see whether the same tool-integration failure still occurs under the new model.
- D) Add a hook that automatically restarts the CI runner whenever the pipeline-status call fails, without further investigation.

**Question 55.** The internal warehouse-query capability needs to be reachable from Claude Code sessions across the whole data org, not just one team, and should be maintainable by the platform team independently of any consuming application.

Question: What is the best approach?

- A) Have each individual team paste their own copy of warehouse credentials into their team's CLAUDE.md, so every team manages its own access independently.
- B) Hard-code the same query logic separately into each team's own custom skill, duplicating the implementation across the org.
- C) Build a single MCP server exposing warehouse-query operations as shared tools, maintained centrally by the platform team.
- D) Ask each engineer to run the warehouse CLI by hand whenever a query is needed, rather than integrating it into Claude Code sessions at all.

**Question 56.** An MCP server for the data catalog exposes both a `search_tables` tool and a way for agents to see what tables and schemas exist without an exploratory search call.

Question: What is the second capability an example of?

- A) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- B) An MCP tool that is functionally identical in every respect to `search_tables`.
- C) A built-in tool that the platform provides automatically to every MCP server.
- D) A Claude Code Skill packaged and shipped alongside the MCP server.

**Question 57.** The team is deciding whether the pipeline-status MCP server should run as a local stdio process per engineer's machine or as a remote, centrally-hosted network service.

Question: What should drive the decision?

- A) stdio servers are always faster than remote servers, regardless of what the deployment actually needs or how many clients must reach it.
- B) MCP only supports one communication pattern in practice, so there's no real decision to make here at all.
- C) Where the server runs relative to the client, and who needs access: local stdio per machine, remote hosting for shared services.
- D) Remote MCP servers are structurally unable to expose tools, only resources, so any tool-based capability must run locally instead.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a warehouse API token hardcoded directly in the file.

Question: What is the correct fix?

- A) Base64-encode the token in place before committing the file, so it isn't stored as obviously readable plain text.
- B) Move `.mcp.json` into a separate, private repository instead of the main one, while leaving the token itself unchanged inside the file.
- C) Rotate the token on a weekly schedule instead of removing it from the file, so any leaked copy has a shorter useful lifetime.
- D) Move the token to environment-variable expansion (e.g., `${WAREHOUSE_TOKEN}`) so it isn't committed at all.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full table-drop rights) than any actual data-engineering workflow requires.

Question: What is the correct remediation, consistent with least-privilege principles?

- A) Add logging around the broad tools so any misuse of the existing drop rights can be reviewed after the fact.
- B) Add a confirmation prompt before any drop operation runs, while leaving the underlying tool permissions exactly as broad as they are today.
- C) Leave the access as-is for now, since no actual misuse of the drop rights has been observed yet in the audit.
- D) Scope the exposed tools down to only the operations actual workflows require.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific data-quality reporting workflow used by a single small team, versus a widely-reused schema-validation capability needed by every pipeline agent across the org.

Question: How should each be built?

- A) Both as MCP servers, since MCP is structurally the correct choice for any capability, whether it's used by one team or every team in the org.
- B) Scope the one-off workflow to a team Skill; build the widely-reused capability as a centrally maintained MCP server.
- C) Both as Skills, since Skills are inherently reusable across teams regardless of how narrow or specific their original scope was.
- D) Both as built-in tools, since built-in tools require the least setup effort of any option and cost nothing to maintain going forward.

---
# Answer Key

**Quick key:** 1-A, 2-B, 3-B, 4-A, 5-D, 6-C, 7-C, 8-C, 9-B, 10-C, 11-D, 12-A, 13-D, 14-A, 15-A, 16-D, 17-B, 18-D, 19-B, 20-D, 21-B, 22-C, 23-B, 24-B, 25-A, 26-A, 27-D, 28-D, 29-D, 30-C, 31-B, 32-D, 33-D, 34-C, 35-A, 36-C, 37-C, 38-B, 39-C, 40-D, 41-A, 42-A, 43-D, 44-A, 45-A, 46-C, 47-C, 48-B, 49-C, 50-B, 51-A, 52-A, 53-B, 54-B, 55-C, 56-A, 57-C, 58-D, 59-D, 60-B

---

**1. A** — The tool-use loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. B stops after one arbitrary tool call regardless of what's left to do; C and D key off a timer or specific wording that don't reflect whether Claude actually still has tool calls pending.

**2. B** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. C keeps the result from the model entirely, hoping it can infer what it never saw. A misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. B** — A compliance-critical rule needs deterministic enforcement via a hook that redacts the data outright. A, C, and D all remain probabilistic prompt compliance — repetition, examples, or temperature tuning — which is exactly what's failing at the observed rate.

**4. A** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (C) guarantees some tool call, but not which one. B and D are still probabilistic prompt-level requests.

**5. D** — Removing tools unrelated to the agent's core role directly reduces the candidate set the agent must reason over, improving selection reliability. B adds prompt overhead without removing the actual capability bloat, and A and C don't touch the root cause at all.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (A) wastes calls on non-retryable failures. Asking the model to infer and validate the category itself (B) is strictly worse than the tool reporting it directly. D reduces frequency without fixing the missing information.

**7. C** — "No matching contacts" is a valid empty result, not a failure — return success with an empty set. B hides real signal from the caller entirely. A invents an unnecessary extra step to work around the mislabeling. D patches symptoms while the underlying success/error conflation remains.

**8. C** — High-ambiguity research where the right tools/order depend on intermediate findings is the core case for model-driven selection. A, B, and D are false or unsupported claims about cost, SDK capability, and tool compatibility.

**9. B** — A subagent scoped to only the outreach tool and explicit approval criteria minimizes accidental sends while the main agent reasons about unrelated tools. A overgeneralizes into a platform requirement that doesn't exist; C and D are unsupported technical claims.

**10. C** — Delegating the funding lookup to a subagent that returns a distilled summary keeps the main agent's context focused on prioritization. A and B don't address the root accumulation problem — one just makes room at the end, the other truncates data arbitrarily — and D removes needed capability.

**11. D** — A structured handoff (what was researched, what was found, recommended talking point) lets the rep act immediately. A forces reconstruction from a raw transcript despite calling that transcript "already structured." B omits diagnostic context. C conveys a guess, not facts.

**12. A** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, C, and D are unsupported absolute claims about capability, security, and reachability.

**13. D** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or a latency threshold.

**14. A** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. B, C, and D misdiagnose the cause as capability, registration, or an unrelated sampling parameter.

**15. A** — A per-contact call-count/timestamp hook is the only option that deterministically guarantees the limit; B, C, and D remain probabilistic prompt-level guidance that the earlier scenario already showed can be violated.

**16. D** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost versus synchronous calls. B doesn't reduce per-token cost at all, and A and C risk quality or truncate output without addressing the actual cost lever.

**17. B** — An iterative validate-and-retry loop is inherently multi-turn tool use, which the Batch API cannot support mid-request — each Batch item is a single independent request/response. A, C, and D misidentify the actual limitation.

**18. D** — Streaming supports incremental rendering, reducing perceived latency for real-time progress UIs. A is the wrong API for this use case entirely; B and C don't address perceived latency and add unnecessary overhead.

**19. B** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, C, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. D** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and C rely on probabilistic compliance that hasn't worked so far; A removes the field's value entirely instead of fixing the reporting problem.

**21. B** — Conflicting extractions with no way to resolve them from context should be surfaced for human review with both candidates and sources, not resolved arbitrarily. A, C, and D all discard information or guess at a resolution.

**22. C** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated at the source; D swaps one fragile text format for another.

**23. B** — Schema validity guarantees syntax, not semantics; a separate validation step (checking logical constraints between fields) is needed on top. A wrongly extends schema guarantees to semantics; C and D misdiagnose or abandon a working mechanism.

**24. B** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged overlay text. C and D don't address the actual data-quality bottleneck; A discards otherwise-processable listings rather than fixing the extraction path.

**25. A** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. B, C, and D misstate how concurrency is actually achieved and what each mechanism is actually for.

**26. A** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not an identical-latency guarantee or a wholesale prompt redesign.

**27. D** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and C mishandle or misdescribe this behavior.

**28. D** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-listing cost breakdown. A, B, and C all oversimplify in ways that produce an inaccurate model.

**29. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**30. C** — Resetting at natural task boundaries prevents unrelated context from bleeding into new work. A and B are unrelated levers (a sampling parameter, raw window size) that don't address cross-contamination, and D is a hook wired to an unreliable, text-based trigger rather than an actual session boundary.

**31. B** — High-volume, low-complexity tasks fit a fast, low-latency tier, with a higher tier reserved for flagged complex cases — matching capability to actual task difficulty. A and D overspend by default; C ignores task fit entirely.

**32. D** — Targeted routing of only the flagged complex PRs to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and C apply broad, costly fixes to a narrow problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. A wrongly calls floating-to-latest "deterministic" when the scenario shows the opposite; B and C are unhelpful overcorrections unrelated to the actual fix.

**34. C** — Concrete few-shot examples are the most effective lever for consistent structure when prose alone hasn't worked; pairing them with a lower temperature is a reasonable secondary support, not a replacement. A repeats a failed approach; B and D don't reliably fix structural consistency on their own.

**35. A** — Input and output share one context-window budget, so a long diff directly constrains available review length and vice versa — the usable budget for one side doesn't increase to cover the other. B, C, and D misstate this relationship.

**36. C** — Stable instructions first (ideally cacheable, in the system prompt) and variable content after both improve consistency (clear role separation) and caching. A, B, and D misstate the effect of ordering.

**37. C** — Actual per-request token usage (input/output/cache) attributed per PR gives an accurate cost picture; estimates from latency, call count, or lines-changed (A, B, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism either.

**39. C** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and B work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the pattern disappears; B and C don't address the underlying attention pattern at all.

**41. A** — Validating key claims against the source diff catches confident-but-wrong output that fluency alone would let through. B is the failure mode itself; C and D don't address correctness.

**42. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. B and C are workarounds for a problem that can be structurally eliminated; D doesn't address the preamble issue at all.

**43. D** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; B discards potentially useful context entirely.

**44. A** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. B and C are absolute claims that don't hold generally; D is false.

**45. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. C** — User-level CLAUDE.md never travels through version control, so a new teammate cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and D misdescribe how CLAUDE.md loading actually works.

**47. C** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. A, B, and D would typically produce different, more specific failure signatures instead of a silent hang.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive patches or abandon the structured-comment requirement.

**49. C** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A restricts capability, not output destination; B narrows scope but doesn't isolate output; D removes useful functionality outright.

**50. B** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about slash commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. B floods context directly; C guesses instead of investigating; D doesn't meaningfully share context between windows.

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
