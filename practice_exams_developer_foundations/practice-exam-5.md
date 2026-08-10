# CCDVF Practice Exam 5

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Contract-Review Agent for a Legal Services Firm, Real-Time Streaming Support Chat Integration, Optimizing a Multilingual Content-Moderation Service, Claude Code Skills and Commands for a QA Team) |
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

## Scenario A: Contract-Review Agent for a Legal Services Firm (Questions 1–15)

Meridian & Locke LLP, a mid-size legal services firm, is deploying a contract-review agent to help attorneys review vendor contracts, NDAs, and lease agreements. The agent has tools including `search_clause_library`, `flag_risk`, `redline_suggest`, and `request_attorney_review`. Because incorrect redlines or missed risk flags carry real legal and financial consequences, tool design and escalation policy matter as much as review quality.

---

**Question 1.** An engineer wants the contract-review agent's tool-use loop to keep executing tools and returning results until Claude has no more tool calls to make. What should the loop key off?

- A) Whether the redline text contains the phrase "no further changes."
- B) The `stop_reason` field on each response: continue looping while it is `"tool_use"`, stop when it is `"end_turn"`.
- C) A hard cap of five tool calls per contract.
- D) Whether `flag_risk` returned any flags.

**Question 2.** After `flag_risk` executes and returns identified risk clauses, what must happen for the agent to correctly continue reasoning about the contract?

- A) Append a `tool_result` block referencing the tool_use ID to the conversation, then send the full conversation back to the model.
- B) Store the flags in a separate risk database only, without returning them to the model.
- C) Insert the flags into the system prompt so they persist for the rest of the review.
- D) Start a new session summarizing the flags found so far.

**Question 3.** Firm policy requires attorney approval before `redline_suggest` output can be sent to a client on any lease agreement above $1M in value. The system prompt states this clearly, but logs show occasional auto-sends bypassing approval. What is the most reliable fix?

- A) Repeat the rule at both the start and end of the system prompt.
- B) Add few-shot examples of the agent correctly escalating high-value leases.
- C) Implement a hook that intercepts the send action for `redline_suggest` and blocks any output targeting a high-value lease without prior attorney approval recorded.
- D) Lower the model's temperature so it follows the stated policy more consistently.

**Question 4.** The team wants `classify_contract_type` to always run first, with no exceptions, before any other tool.

- A) State in the system prompt that `classify_contract_type` must always run first.
- B) Set `tool_choice: "any"` on the first request so a tool call is guaranteed.
- C) Set `tool_choice: {"type": "tool", "name": "classify_contract_type"}` on the first request, then use normal tool choice afterward.
- D) Add several few-shot examples showing `classify_contract_type` called first.

**Question 5.** The agent currently has 14 tools, including several rarely-used ones (billing lookup, HR onboarding checks, marketing template access) unrelated to contract review. Tool selection has become unreliable. What is the single most direct fix?

- A) Add a system prompt note listing which tools are "primary."
- B) Remove or scope out the tools unrelated to the agent's core contract-review role.
- C) Increase max_tokens so the agent has more room to reason about which tool to pick.
- D) Add several few-shot examples showing correct tool selection.

**Question 6.** `search_clause_library` currently returns the string `"Error"` for every possible failure — bad query syntax, missing index, or service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- B) Wrap every call in an automatic retry policy.
- C) Add a system prompt instruction telling the agent to infer the failure type from context.
- D) Increase the library service's timeout so failures become rarer.

**Question 7.** When `search_clause_library` finds no matching precedent clauses, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Add a hook that suppresses the error and ends the review.
- B) Return a successful response with an empty result set, reserving errors for actual access failures.
- C) Have the agent call `flag_risk` first to check whether a clause should exist.
- D) Add a system prompt note explaining that this error usually means no clause matched.

**Question 8.** An attorney proposes replacing the agent's reasoning with a fixed sequence — always call `search_clause_library`, then `flag_risk`, then decide — arguing this makes behavior predictable.

Why is model-driven tool selection the better fit for contract review?

- A) Model-driven selection is always cheaper since it skips unnecessary reasoning tokens.
- B) Contract review is high-ambiguity; the right tools and order vary by contract type and depend on intermediate findings, which a fixed sequence can't adapt to.
- C) The Claude Agent SDK technically cannot run fixed tool sequences.
- D) Fixed sequences cannot invoke custom tools, only built-in ones.

**Question 9.** The team is deciding whether to give the main review agent `request_attorney_review` directly, or to delegate escalation decisions to a separate, narrowly-scoped subagent. Escalating unnecessarily wastes attorney time.

What is the strongest argument for a separate, narrowly-scoped subagent?

- A) Subagents are required any time a tool has real-world side effects.
- B) The main agent's context window is too small to hold the escalation tool's schema.
- C) A narrowly-scoped subagent given only the escalation tool and explicit criteria reduces the chance the main agent escalates unnecessarily while reasoning about unrelated tools.
- D) Subagents execute faster than tools called directly by the main agent.

**Question 10.** During review of a 200-page master services agreement, the agent's context fills with verbose raw clause text, leaving little room to reason about actual risk.

What is the best structural fix?

- A) Increase `max_tokens` so responses can be longer.
- B) Read only the first 50 clauses of every document.
- C) Disable clause search entirely.
- D) Delegate clause exploration to a subagent that returns a distilled summary of relevant findings, keeping the main agent's context focused on risk assessment.

**Question 11.** The agent escalates a contract to an attorney, but the attorney has no visibility into what the agent checked before escalating — logs show many tool calls with no accessible summary.

What should the escalation to a human include?

- A) The full raw transcript of every tool call and result.
- B) Just the final flagged clause, since the attorney can re-investigate from there.
- C) A structured handoff summary: what was checked, what was found, and a recommended next action.
- D) A sentiment analysis of how urgent the review seemed.

**Question 12.** The firm is deciding between letting attorneys run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on firm infrastructure, given client-confidentiality concerns.

What is the core tradeoff?

- A) Operational control (self-hosted) versus operational burden (managed) — there is no capability difference in what tools the agent can call.
- B) Self-hosted agents cannot use custom tools.
- C) Managed agents are always less secure than self-hosted ones.
- D) Managed agents cannot access private infrastructure at all.

**Question 13.** An attorney asks whether routine NDA review (a fixed checklist: check parties, term, governing law) and complex M&A contract review should both be built the same way — as either a fixed workflow or an agent.

What is the deciding factor?

- A) Whether the task is well-defined and repeatable versus high-ambiguity with a path that depends on intermediate findings.
- B) Whether the task involves more than three tools.
- C) Whether the team prefers Python or TypeScript.
- D) Whether the task needs to run in under 30 seconds.

**Question 14.** A "clause-research subagent" has a vague description: "Helps with clauses." The main agent rarely delegates to it even when clause research is clearly needed.

What is the most likely cause and fix?

- A) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.
- B) The subagent needs more tools; add several more clause-related tools to its definition.
- C) Subagents cannot be delegated to unless they are registered in `.mcp.json`.
- D) The main agent's temperature is too low to consider delegating.

**Question 15.** The firm wants a hard guarantee that `redline_suggest` is never applied more than twice to the same clause within one review session, regardless of what the model decides mid-conversation.

What is the correct enforcement mechanism?

- A) A system prompt instruction stating the two-edit limit clearly.
- B) A note in the tool's description mentioning the limit.
- C) A hook that tracks per-clause call counts and blocks the tool call once the limit is reached.
- D) Few-shot examples showing an agent stopping after two edits.

---

## Scenario B: Real-Time Streaming Support Chat Integration (Questions 16–30)

Helios Connect, a SaaS company, is integrating Claude into its live customer-support chat widget, where Claude drafts responses to customers in real time alongside human agents, occasionally calling tools (`search_kb`, `create_ticket`, `check_order_status`).

---

**Question 16.** Customers see Claude's response appear incrementally, word by word, in the chat widget as it's generated. Which technique enables this, and why?

- A) Streaming, so the UI can render output incrementally and reduce perceived latency.
- B) The Batch API, since it's designed for real-time feedback.
- C) Increasing max_tokens so the full response arrives faster.
- D) Polling a status endpoint every second.

**Question 17.** A live chat reply needs `check_order_status` called mid-conversation and the result fed back before the reply finishes, with a customer actively waiting.

Which API fits, and why?

- A) The Batch API, because it's cheaper per token.
- B) The Batch API, because it supports mid-request tool calls.
- C) The synchronous Messages API with streaming, since the customer is waiting live and the flow needs a tool call answered within the same request.
- D) The synchronous Messages API without streaming, since streaming and tool use are mutually exclusive.

**Question 18.** Every chat turn sends the same 4,000-token support policy and tone guidelines, followed by the evolving conversation history, which varies per turn.

What optimization most directly reduces both latency and cost across many turns?

- A) Move the policy into a few-shot example block instead.
- B) Switch to the smallest available model regardless of quality.
- C) Place the stable policy/tone instructions first, enable prompt caching, and put the varying conversation history after it.
- D) Truncate the policy text to save tokens.

**Question 19.** The `create_ticket` schema requires a `resolution_summary` field on every ticket. Many tickets are still open with no resolution yet, and Claude has started inventing placeholder text like "resolved by agent" rather than reporting none.

What schema change fixes this?

- A) Remove the field from the schema entirely.
- B) Add a prompt instruction telling the model not to invent values.
- C) Make `resolution_summary` nullable so its absence can be reported truthfully.
- D) Lower the temperature to reduce invented values.

**Question 20.** Two calls to `check_order_status` for the same order return different estimated delivery dates, and there's no way to tell which is correct from context alone.

What should the integration do?

- A) Average the two dates.
- B) Surface both candidate values to a human agent for review rather than silently picking one and telling the customer.
- C) Always trust the first call's result.
- D) Discard the order lookup entirely.

**Question 21.** The chatbot occasionally outputs a `create_ticket` payload as free text that fails to parse as JSON, crashing the ticket-creation step in about 2% of cases.

What is the most reliable fix?

- A) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library to fix common syntax issues before parsing.
- C) Ask for YAML output instead, since it's more forgiving of formatting drift.
- D) Define `create_ticket` as a tool with an input schema matching the ticket structure, and read the data from the structured `tool_use` block instead of parsing free text.

**Question 22.** Since switching `create_ticket` to strict schema-constrained tool use, payloads always parse successfully, but some tickets are labeled `priority: low` despite the customer describing a full outage.

What should the team conclude and do?

- A) Strict schemas eliminate syntax errors, not semantic errors — add a validation step that checks priority classification against message content on top of schema compliance.
- B) The schema needs stricter enum types to fix this.
- C) max_tokens is too low, truncating output mid-generation.
- D) Abandon tool use and return to free-text tickets with human review.

**Question 23.** Customers occasionally attach screenshots of error dialogs. The integration currently runs OCR on the screenshot and sends only the extracted text to Claude, and responses are poor whenever OCR mangles the error code.

What is the most direct fix?

- A) Send the screenshot image itself as a content block alongside the customer's message, using Claude's native vision input instead of relying solely on OCR text.
- B) Increase max_tokens so the model works harder on the degraded OCR text.
- C) Switch to a larger model, since bigger models are always better at reading noisy text.
- D) Reject screenshot attachments entirely.

**Question 24.** The support widget needs to serve many concurrent chat sessions from different customers at once, without one customer's request blocking another's.

What must the integration layer support to do this?

- A) Streaming, since only streaming supports concurrency.
- B) The Batch API, since it's the only way to run more than one request at a time.
- C) A single request handling all sessions concatenated together, since Claude parallelizes internally.
- D) Async/concurrent request handling, so multiple API calls can be in flight at once without blocking on each other.

**Question 25.** The company plans to run the same chat integration through both the direct Anthropic API and a cloud-hosted equivalent for different regional deployments.

What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) The cloud-hosted equivalent requires a completely different prompting approach and schema design.
- C) Batch processing is unavailable on all third-party vendor integrations.
- D) Extraction accuracy and latency are guaranteed identical across vendors.

**Question 26.** The team enables extended thinking for complex troubleshooting conversations that use tool calls across several turns.

What must the integration layer do correctly?

- A) Ignore thinking content entirely, since it never affects downstream turns.
- B) Convert thinking output into a separate tool call.
- C) Discard thinking content only when tools are involved.
- D) Handle the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.

**Question 27.** Finance asks for an accurate per-conversation cost breakdown for the chat integration, but the current cost model only estimates based on average message length.

What should the improved cost model account for separately?

- A) Only cache read tokens, since caching is the dominant cost driver.
- B) Only output tokens, since input is effectively free.
- C) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- D) A flat per-conversation fee regardless of token usage.

**Question 28.** A new engineer argues the team can skip code review on the chat widget's surrounding application code since "the AI part is the risky part."

What is the correct response?

- A) Review should be skipped for any code that calls an external API.
- B) Code review is unnecessary once evals pass.
- C) Only the prompt needs review; the surrounding code is low-risk by definition.
- D) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.

**Question 29.** A single long-running agent session is reused across an entire shift to handle chats from many different, unrelated customers, and the team notices Claude referencing a previous customer's order details in a new customer's chat.

What is the best fix?

- A) Reduce temperature to prevent cross-referencing.
- B) Start a fresh session for each new customer conversation rather than accumulating unrelated context in one long-running session.
- C) Ask the model to "ignore earlier customers" at the start of each new chat.
- D) Increase the context window so more history fits without confusion.

**Question 30.** A troubleshooting conversation is very long, and the team wants Claude to produce a maximally detailed final resolution summary, considering a very long requested output.

What tradeoff must they account for?

- A) None — input and output tokens are budgeted completely independently.
- B) Input and output share the same context-window budget, so a very long conversation history leaves less room for a long output, and vice versa.
- C) Output length has no effect on latency.
- D) Long outputs are always truncated regardless of context window size.

---

## Scenario C: Optimizing a Multilingual Content-Moderation Service (Questions 31–45)

GlobalGuard operates a content-moderation service that classifies user-generated posts across 40 languages for policy violations, processing millions of posts per day. Cost, latency, and consistency across languages all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most posts are short and moderation is a simple binary classification (violates / doesn't violate) at extremely high volume. Latency and cost per post matter far more than handling rare, ambiguous edge cases well.

Which approach best fits the default path?

- A) The highest-capability tier available, to guarantee quality on every post.
- B) Whichever tier is cheapest per token regardless of task fit.
- C) The same tier used for the company's hardest reasoning tasks, for consistency.
- D) A fast, low-latency tier suited to high-volume/low-complexity classification, reserving a higher tier only for posts flagged as ambiguous.

**Question 32.** A small fraction of posts require nuanced judgment (satire versus genuine hate speech, or context-dependent slang) where the fast default model produces inconsistent classifications.

What is the most targeted fix?

- A) Add more few-shot examples to the fast model's prompt for every post.
- B) Route only the flagged ambiguous posts to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.
- C) Switch every post to the highest-capability tier to be safe.
- D) Increase max_tokens for all posts.

**Question 33.** The service floats to "whatever model is latest" in production. After a routine model update, classification thresholds shifted noticeably for borderline posts, with no code change on the team's side.

What should the team do differently?

- A) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.
- B) Nothing — behavior drift across releases is expected and requires no process.
- C) Roll back to the oldest available model version permanently.
- D) Disable all prompt caching to prevent drift.

**Question 34.** Moderation output needs a consistent label set (`hate_speech`, `harassment`, `spam`, `none`), but detailed prose instructions describing the categories haven't produced consistent output across languages.

What technique is most likely to help?

- A) Write an even longer, more detailed prose description of the categories.
- B) Lower the temperature to zero.
- C) Provide 2–3 few-shot examples in multiple languages demonstrating the exact desired labeling.
- D) Ask the model to restate the categories before classifying.

**Question 35.** A post thread is very long (reply chains with 100+ comments), and the team wants a maximally detailed moderation report per comment, considering a very long requested output.

What tradeoff must they account for?

- A) Input and output share the same context-window budget, so a long input thread leaves less room for a long output, and vice versa.
- B) Long outputs are always truncated regardless of context window size.
- C) Output length has no effect on latency.
- D) Input and output tokens are budgeted completely independently.

**Question 36.** The moderation prompt currently places the specific post text before the general policy instructions and desired label format in every request.

Why might reordering improve both consistency and cacheability?

- A) Order has no effect on either consistency or caching.
- B) Placing instructions last always improves model attention.
- C) Stable, role-defining policy instructions belong first (system prompt or first block) so they form a consistent, cacheable prefix; post-specific content should come after as the varying part.
- D) Reordering only affects cost, never consistency.

**Question 37.** Finance wants to know exactly how much the moderation service costs per post, but the team currently estimates cost only from average prompt length.

What should be instrumented instead?

- A) Actual token usage per request — input, output, and cache — attributed per post, rather than an estimate from average length.
- B) Wall-clock latency per post, used as a cost proxy.
- C) Number of API calls only, regardless of token count.
- D) A flat cost assumption based on post character count.

**Question 38.** An engineer writes an automated eval that asserts the moderation label must exactly match a fixed reference string for a sample post, and the eval fails intermittently even though the labels look correct on manual review.

What is the most likely issue with the eval design?

- A) The model is broken and producing wrong answers.
- B) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation (e.g., checking for required content/structure) rather than asserting exact text.
- C) The eval needs a larger reference string.
- D) Temperature should be increased to fix the intermittent failures.

**Question 39.** Posts arrive with full raw platform metadata dumps (every field of the post object) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

What is the best fix?

- A) Increase max_tokens to accommodate the extra data.
- B) Prune the metadata to the relevant fields before it enters the prompt, rather than passing raw dumps.
- C) Switch to a model with a larger context window so the bloat matters less.
- D) Summarize the metadata with a second Claude call before classifying.

**Question 40.** For very long comment threads, the team notices moderation misses violations in the middle of the thread while catching issues in the opening and closing comments well.

What is the most effective mitigation?

- A) Switch to a model with an even larger context window.
- B) Add an instruction telling the model to "pay equal attention to the whole thread."
- C) Alphabetize the comments before classifying.
- D) Put a brief overview or key-facts summary at the start of the input and organize the detailed content under clear section headers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 41.** A moderation report confidently states a post "contains a direct threat of violence," but on manual review the post was actually a quote from a news article being discussed critically.

What practice would most help catch this class of error before action is taken?

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Increase the model's temperature so answers sound less confident.
- C) Shorten the report so there's less room for errors.
- D) Apply defensive parsing and skepticism toward confident output — verify key claims against the source post rather than accepting fluency as correctness.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

What is the more reliable approach?

- A) Repeat the JSON instruction more emphatically.
- B) Post-process every response to strip text before the first `{`.
- C) Increase max_tokens so there's room for both the preamble and the JSON.
- D) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.

**Question 43.** The team wants to add an exploratory step that scans a user's full posting history for repeat-offense context before moderating the current post, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

What is the best structural approach?

- A) Load the entire posting history directly into the main prompt every time.
- B) Skip historical context entirely to avoid the bloat risk.
- C) Increase the context window so the full history always fits.
- D) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main moderation step.

**Question 44.** For the simplest, most common moderation case (obvious spam links), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

What consideration should drive the choice?

- A) Multi-shot is always strictly better regardless of task simplicity.
- B) Zero-shot is required whenever latency matters at all.
- C) The choice has no effect on cost or latency.
- D) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.

**Question 45.** The moderation prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent uptick in false positives.

What practice would have prevented this?

- A) Locking the prompt so no one can ever change it again.
- B) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- C) Only allowing one designated engineer to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

---

## Scenario D: Claude Code Skills and Commands for a QA Team (Questions 46–60)

You support a 30-person QA team's use of Claude Code, custom skills, slash commands, and internal MCP servers (test-case management, defect tracking, test-environment provisioning). You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new QA engineer clones the team's test-automation repo, but Claude Code doesn't apply the team's established test-naming and assertion conventions, even though a teammate's machine applies them correctly.

What is the most likely cause?

- A) The new engineer needs to run `/memory` to activate memory files.
- B) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- C) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.
- D) The conventions file exceeded a size limit and was silently truncated.

**Question 47.** A nightly CI job invokes Claude Code to triage failing test runs and consistently hangs until timeout, with no visible error in the logs.

What is the most likely cause?

- A) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- B) The test runs are too large for Claude Code to process.
- C) The CI runner lacks permission to call the Claude API.
- D) The repository's CLAUDE.md is malformed.

**Question 48.** A downstream dashboard parses Claude Code's test-triage output with regex to auto-file defect tickets, and the parser breaks whenever output formatting drifts slightly between runs.

What is the robust fix?

- A) Harden the regex with more permissive fallback patterns.
- B) Run with `--output-format json` and a `--json-schema` defining the triage-findings structure for machine-parseable output.
- C) Post the entire raw output as a single ticket comment instead of parsing it.
- D) Add a stronger prompt instruction never to deviate from the format.

**Question 49.** The team's `/scan-flaky-tests` custom command prints thousands of lines of historical test-run data, and testers report that Claude's answers about their actual task get noticeably worse right after running it.

What frontmatter change fixes this?

- A) `argument-hint`, so testers scope the analysis more narrowly.
- B) `context: fork`, so the command's verbose output runs in an isolated sub-agent context and only a summary returns to the main conversation.
- C) `allowed-tools`, restricting the command to read-only operations.
- D) Removing the command entirely.

**Question 50.** An internal `/generate-test-fixtures` skill is meant only to create new fixture files from a template, but an audit finds a session where it also ran shell commands that modified unrelated config files.

What is the correct guardrail?

- A) Add a warning in the skill's instructions telling Claude never to run shell commands.
- B) Require testers to commit their work before running any skill.
- C) Convert the skill into a slash command, since commands cannot run tools.
- D) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.

**Question 51.** A QA engineer needs to understand how a large, unfamiliar test-automation framework's fixture system works before writing new tests, and worries that reading dozens of files will exhaust context before implementation begins.

What is the best approach?

- A) Read every file in the framework in one pass to be thorough.
- B) Skip exploration and infer the architecture from directory names.
- C) Split the work across two separate terminal windows.
- D) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the new tests in the same session and wants to preserve key findings.

What should they do?

- A) Start a brand-new session and rely on memory of what was learned.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md temporarily to free context space.
- D) Continue working; Claude automatically discards irrelevant context.

**Question 53.** A multi-step Claude Code task that reads a test-config file, calls an internal MCP tool to fetch environment status, and writes a defect-triage report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Where should debugging focus next?

- A) Re-read the config file again, since that's the earliest step.
- B) The network connection to the MCP server, since that's the most complex step.
- C) The step between receiving the MCP tool's valid data and producing the final report — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- D) Nothing — a wrong final report with correct inputs means the task should simply be re-run.

**Question 54.** A test-environment provisioning tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

What is the correct first diagnostic step?

- A) Assume it's a model problem and rewrite the prompt.
- B) Switch to a different model to see if the failure persists.
- C) Restart the CI runner and try again.
- D) Isolate whether the failure occurred at the integration layer (the actual API/tool call and its response) versus in the model's output, by examining the trace of exactly what was sent and received.

**Question 55.** The internal defect-tracking system needs to be reachable from Claude Code sessions across the whole QA org, not just one team, and should be maintainable by the platform team independently of any consuming application.

What is the best approach?

- A) Build an MCP server exposing defect-tracking operations as tools, shared across the org.
- B) Have each team paste defect-tracker API credentials into their own CLAUDE.md.
- C) Hard-code defect-tracking logic into each team's custom skill separately.
- D) Ask each engineer to curl the defect-tracker API manually when needed.

**Question 56.** An MCP server for the test-case management system exposes both a `search_test_cases` tool and a way for agents to see what test suites exist without an exploratory search call.

What is the second capability an example of?

- A) An MCP tool, functionally identical to `search_test_cases`.
- B) An MCP resource — content/catalog visibility distinct from a tool, which performs an action.
- C) A built-in tool provided by the platform automatically.
- D) A Claude Code Skill.

**Question 57.** The team is deciding whether an internal MCP server for test-environment provisioning should run as a local stdio process per QA engineer's machine or as a remote, centrally-hosted network service.

What should drive the decision?

- A) stdio servers are always faster regardless of deployment context.
- B) MCP only supports one communication pattern, so there's no real decision to make.
- C) Remote servers cannot expose tools, only resources.
- D) Where the server needs to run relative to the client and who needs access — local stdio for per-machine/local resources, remote/network hosting for centrally shared services accessed by many clients.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a defect-tracker API token hardcoded directly in the file.

What is the correct fix?

- A) Base64-encode the token before committing it.
- B) Rotate the token weekly instead of removing it from the file.
- C) Move the token to environment-variable expansion (e.g., `${DEFECT_TRACKER_TOKEN}`) so the secret isn't committed to version control.
- D) Move `.mcp.json` to a private repository instead.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full test-suite deletion rights) than any actual QA workflow requires.

What is the correct remediation, consistent with least-privilege principles?

- A) Add logging so misuse can be reviewed after the fact.
- B) Leave access as-is, since no misuse has been observed yet.
- C) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities rather than just monitoring them.
- D) Add a confirmation prompt before any deletion.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific test-report-formatting workflow used by a single small QA squad, versus a widely-reused environment-health-check capability needed by every agent across the org.

How should each be built?

- A) The one-off report-formatting workflow as a Skill or custom tool scoped to that team; the widely-reused environment-health-check capability as an MCP server or built-in tool maintained centrally and shared across all consuming agents.
- B) Both as MCP servers, since MCP is the correct choice for any shared capability.
- C) Both as Skills, since Skills are always reusable.
- D) Both as built-in tools, since built-in tools require the least setup.

---
# Answer Key — Practice Exam 5

**Quick key:** 1-B, 2-A, 3-C, 4-C, 5-B, 6-A, 7-B, 8-B, 9-C, 10-D, 11-C, 12-A, 13-A, 14-A, 15-C, 16-A, 17-C, 18-C, 19-C, 20-B, 21-D, 22-A, 23-A, 24-D, 25-A, 26-D, 27-C, 28-D, 29-B, 30-B, 31-D, 32-B, 33-A, 34-C, 35-A, 36-C, 37-A, 38-B, 39-B, 40-D, 41-D, 42-D, 43-D, 44-D, 45-B, 46-C, 47-A, 48-B, 49-B, 50-D, 51-D, 52-B, 53-C, 54-D, 55-A, 56-B, 57-D, 58-C, 59-C, 60-A

---

**1. B** — The loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (C) is a backstop, not a primary mechanism; whether flags were found (D) doesn't indicate loop completion.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. C** — A financially/legally significant rule needs deterministic enforcement via a hook that blocks the send outright. A, B, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forced tool choice on a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and D are probabilistic.

**5. B** — Removing tools unrelated to the agent's core role directly shrinks the candidate set the agent must reason over, improving selection reliability. A adds prompt overhead without removing capability bloat; C and D don't address tool-selection reliability at all.

**6. A** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (B) wastes calls on non-retryable failures. Asking the model to guess (C) is strictly worse than the tool reporting it. D reduces frequency without fixing the missing information.

**7. B** — "No matching clause" is a valid empty result, not a failure — return success with an empty set. A hides real signal. C invents an unnecessary extra step. D patches symptoms while the underlying success/error conflation remains.

**8. B** — High-ambiguity tasks where tools/order depend on intermediate findings are the core case for model-driven selection. A, C, and D are false or unsupported claims about the technology.

**9. C** — A narrowly-scoped subagent with only the escalation tool and explicit criteria minimizes unnecessary escalations while the main agent reasons about unrelated tools. A overgeneralizes; B and D are unsupported technical claims.

**10. D** — Delegating exploration to a subagent that returns a distilled summary keeps the main agent's context focused on risk assessment. A and B don't address the root accumulation problem; C removes needed capability.

**11. C** — A structured handoff (what was checked, what was found, recommended action) lets an attorney act immediately. A forces reconstruction from a raw transcript. B omits diagnostic context. D conveys mood, not facts.

**12. A** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between the two deployment models. B, C, and D are unsupported absolute claims.

**13. A** — Task predictability versus dependency on intermediate results is the deciding factor between workflow and agent patterns, not tool count, language, or runtime.

**14. A** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of how many tools the subagent has. B, C, and D misdiagnose the cause.

**15. C** — A per-clause call-count hook is the only option that deterministically guarantees the limit; A, B, and D remain probabilistic prompt-level guidance.

**16. A** — Streaming supports incremental rendering, reducing perceived latency for real-time chat UIs. B is the wrong API for this use case; C and D don't address perceived latency.

**17. C** — A customer waiting live for a reply that requires a mid-request tool call needs the synchronous Messages API (with streaming for responsiveness); the Batch API cannot answer a tool call within a single request the way this flow needs. A and B misdescribe the Batch API; D is a false claim — streaming and tool use are not mutually exclusive.

**18. C** — Only a shared prefix is cacheable; placing stable content first and variable content last maximizes cache hits, reducing both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without addressing caching.

**19. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance or lose data; A removes the field's value entirely.

**20. B** — Conflicting values with no way to resolve them from context should be surfaced for human review with both candidates, not resolved arbitrarily. A, C, and D all discard information or guess.

**21. D** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the JSON-in-text parsing failure class outright. A and B are recovery layers for a problem that can be eliminated; C swaps one fragile text format for another.

**22. A** — Schema validity guarantees syntax, not semantics; a separate validation step (checking priority against message content) is needed on top. B, C, and D misdiagnose or abandon a working mechanism.

**23. A** — Sending the image directly as a vision content block bypasses lossy OCR entirely for damaged screenshots. B and C don't address the actual data-quality bottleneck; D discards otherwise-useful attachments.

**24. D** — Concurrent tool/API calls require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**25. A** — The Messages API contract is conceptually consistent across vendors, though plumbing and rollout timing can differ — this is the realistic expectation, not identical latency or unavailable features.

**26. D** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, B, and C mishandle or misdescribe this.

**27. C** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate per-conversation cost breakdown. A, B, and D all oversimplify in ways that produce an inaccurate model.

**28. D** — Standard SDLC discipline (review, testing, version control) still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**29. B** — Starting a fresh session per customer prevents unrelated context from bleeding into a new conversation. A is an unrelated lever; C is unreliable prompt-level mitigation; D doesn't address cross-contamination.

**30. B** — Input and output share one context-window budget, so long conversation history directly constrains available output length and vice versa. A, C, and D misstate this relationship.

**31. D** — High-volume, low-complexity classification fits a fast, low-latency tier, with a higher tier reserved for flagged ambiguous cases — matching capability to actual task difficulty. A and B overspend or ignore fit by default; C ignores task fit.

**32. B** — Targeted routing of only the flagged ambiguous cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, C, and D apply broad, costly fixes to a narrow problem.

**33. A** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. B accepts avoidable risk; C and D are unhelpful overcorrections unrelated to the actual fix.

**34. C** — Concrete, multilingual few-shot examples are the most effective lever for consistent labeling when prose alone hasn't worked across languages. A repeats a failed approach; B and D don't reliably fix structural/labeling consistency.

**35. A** — Input and output share one context-window budget, so a long input thread directly constrains available output length and vice versa. B, C, and D misstate this relationship.

**36. C** — Stable instructions first (ideally cacheable) and variable content after both improves consistency (clear role separation) and caching. A, B, and D misstate the effect of ordering.

**37. A** — Actual per-request token usage (input/output/cache) attributed per post gives an accurate cost picture; estimates from average length or unrelated proxies (B, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. B** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and C work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and C don't address the underlying attention pattern.

**41. D** — Verifying key claims against the source post catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; B and C don't address correctness.

**42. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and B are workarounds for a problem that can be structurally eliminated; C doesn't address the preamble issue.

**43. D** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; B discards potentially useful context entirely.

**44. D** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and B are absolute claims that don't hold generally; C is false.

**45. B** — Versioning prompts like code enables attribution and rollback for quality regressions. A, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. C** — User-level CLAUDE.md never travels through version control, so a new engineer cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and D misdescribe how CLAUDE.md loading actually works.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. B** — Schema-constrained JSON output via `--output-format json`/`--json-schema` is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive or abandon the structured-parsing requirement.

**49. B** — `context: fork` isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A narrows scope but doesn't isolate output; C restricts capability, not output destination; D removes useful functionality.

**50. D** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; B mitigates damage rather than preventing it; C is a false claim about slash commands.

**51. D** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; C doesn't share context between windows meaningfully.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; D describes behavior that doesn't exist.

**53. C** — Since the config and MCP data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about or transformed — that's where the trace should focus next. A and B re-check already-verified steps; D skips diagnosis entirely.

**54. D** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was sent and received, before assuming which side is at fault. A and B guess without diagnosis; C doesn't investigate the cause at all.

**55. A** — An MCP server exposing shared tools org-wide, maintained centrally, matches the cross-application reuse and independent-maintenance requirement. B, C, and D all fail to provide reusable, centrally maintained access.

**56. B** — Visibility into available content without an action call is the defining trait of an MCP resource, distinct from a tool that performs an action. A, C, and D mischaracterize this capability.

**57. D** — The choice should follow where the server needs to run and who needs access — local stdio for per-machine resources, remote hosting for centrally shared services. A, B, and C are false or oversimplified claims about MCP's communication patterns.

**58. C** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and D don't remove the exposed credential from history or ongoing risk.

**59. C** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A and D are detective/compensating controls; B accepts unnecessary risk.

**60. A** — Matching each capability's actual reuse scope — Skill/custom tool for the one-off, team-specific workflow; MCP or built-in tool for the widely shared, centrally maintained capability — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

---

*End of Practice Exam 5.*
