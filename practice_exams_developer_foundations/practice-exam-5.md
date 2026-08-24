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

- A) Whether the redline draft's text happens to contain the phrase "no further changes needed" anywhere in it.
- B) The `stop_reason` field: keep looping while it reads `tool_use`, stop once it reads `end_turn`.
- C) A fixed ceiling of five tool calls per contract, after which the loop halts no matter what work remains.
- D) Whether the most recent `flag_risk` call happened to return at least one flagged clause.

**Question 2.** After `flag_risk` executes and returns identified risk clauses, what must happen for the agent to correctly continue reasoning about the contract?

- A) Append a `tool_result` block referencing the original `tool_use` ID, then resend the full conversation so the model can incorporate the flags.
- B) Store the returned flags in a separate risk database only, without ever returning them to the model in the conversation.
- C) Insert the flags directly into the system prompt so they persist as instructions for the rest of the review.
- D) Start an entirely new session that briefly summarizes the flags found before continuing the review.

**Question 3.** Firm policy requires attorney approval before `redline_suggest` output can be sent to a client on any lease agreement above $1M in value. The system prompt states this clearly, but logs show occasional auto-sends bypassing approval. What is the most reliable fix?

- A) State the $1M approval rule at both the start and the end of the system prompt for emphasis.
- B) Add several few-shot examples in the system prompt showing the agent correctly escalating high-value leases above the $1M threshold before ever sending output.
- C) Add a hook that intercepts the send action and blocks it unless attorney approval is already recorded.
- D) Reduce the model's sampling randomness so it follows the stated approval policy more consistently.

**Question 4.** The team wants `classify_contract_type` to always run first, with no exceptions, before any other tool.

- A) State in the system prompt that `classify_contract_type` must always run before any other tool.
- B) Set `tool_choice: "any"` on the first request so some tool call is guaranteed to happen.
- C) Set `tool_choice` to force `classify_contract_type` on the first request, then allow normal tool choice afterward.
- D) Add several few-shot examples throughout the system prompt that show `classify_contract_type` being called before every other tool in past reviews.

**Question 5.** The agent currently has 14 tools, including several rarely-used ones (billing lookup, HR onboarding checks, marketing template access) unrelated to contract review. Tool selection has become unreliable. What is the single most direct fix?

- A) Add a system prompt note listing which of the fourteen tools count as "primary" for contract review.
- B) Remove or scope out the tools unrelated to the agent's core contract-review role.
- C) Raise the value of max_tokens so the agent has more room to reason through which of the fourteen tools to pick.
- D) Add several few-shot examples across all fourteen tools, including billing lookup and HR onboarding, demonstrating correct selection in each case.

**Question 6.** `search_clause_library` currently returns the string `"Error"` for every possible failure — bad query syntax, missing index, or service timeout. The agent responds inconsistently to each. What is the best fix?

- A) Return structured error metadata: an error category, a retryable flag, and a human-readable description of what failed.
- B) Wrap every call to the library in an automatic retry policy regardless of what actually failed.
- C) Add a system prompt instruction telling the agent to infer the failure type from unstructured context clues.
- D) Raise the clause library service's timeout setting instead of touching the response schema, so outright failures simply happen less often.

**Question 7.** When `search_clause_library` finds no matching precedent clauses, it currently returns an error. The agent responds by apologizing for "technical difficulties" and retrying the same query. What should change?

- A) Add a hook that silently suppresses the error and ends the review early.
- B) Return a successful response with an empty result set, reserving actual errors for genuine access failures.
- C) Have the agent call `flag_risk` first to check whether a clause should exist before searching.
- D) Add a system prompt note explaining that this particular error usually just means no clause matched the query.

**Question 8.** An attorney proposes replacing the agent's reasoning with a fixed sequence — always call `search_clause_library`, then `flag_risk`, then decide — arguing this makes behavior predictable.

Why is model-driven tool selection the better fit for contract review?

- A) Model-driven selection is always cheaper because it skips unnecessary reasoning tokens on every contract.
- B) Contract review is high-ambiguity; the right tools and order vary by contract type and depend on intermediate findings.
- C) The Claude Agent SDK is technically incapable of executing a fixed tool sequence at all.
- D) A fixed sequence of tool calls cannot invoke any custom tools the firm has defined for `flag_risk` or `redline_suggest`, only tools built directly into the underlying platform itself.

**Question 9.** The team is deciding whether to give the main review agent `request_attorney_review` directly, or to delegate escalation decisions to a separate, narrowly-scoped subagent. Escalating unnecessarily wastes attorney time.

What is the strongest argument for a separate, narrowly-scoped subagent?

- A) A separate subagent is legally required any time a tool call has real-world side effects on a client.
- B) The main agent's context window is too small to hold the escalation tool's full JSON schema definition.
- C) A narrowly-scoped subagent with only the escalation tool and explicit criteria is less likely to escalate unnecessarily than a generalist agent reasoning about unrelated tools.
- D) Subagents execute their tool calls measurably faster than tools called directly by the main review agent.

**Question 10.** During review of a 200-page master services agreement, the agent's context fills with verbose raw clause text, leaving little room to reason about actual risk.

What is the best structural fix?

- A) Raise the value of max_tokens substantially so the model's eventual responses about the agreement can run considerably longer without truncation.
- B) Read only the first 50 clauses of every document submitted for review and skip the remaining pages without exception.
- C) Disable clause search entirely so the context never fills with clause text again.
- D) Delegate clause exploration to a subagent that returns a distilled summary, keeping the main context focused on risk.

**Question 11.** The agent escalates a contract to an attorney, but the attorney has no visibility into what the agent checked before escalating — logs show many tool calls with no accessible summary.

What should the escalation to a human include?

- A) The full raw, unstructured transcript of every tool call and result made during the review.
- B) Just the final flagged clause, since the attorney can re-investigate everything else from there.
- C) A structured handoff summary: what was checked, what was found, and a recommended next action.
- D) A sentiment score estimating how urgent the review felt based on the language used.

**Question 12.** The firm is deciding between letting attorneys run the agent via a hosted, Anthropic-managed execution environment versus self-hosting the harness on firm infrastructure, given client-confidentiality concerns.

What is the core tradeoff?

- A) Operational control versus operational burden — the real tradeoff, since tool-calling capability doesn't differ between self-hosted and managed deployments.
- B) Self-hosted agents are structurally unable to register or call any custom tools the firm defines.
- C) Managed execution environments are always less secure than a self-hosted deployment, regardless of configuration.
- D) Managed agents cannot reach any private firm infrastructure under any circumstances.

**Question 13.** An attorney asks whether routine NDA review (a fixed checklist: check parties, term, governing law) and complex M&A contract review should both be built the same way — as either a fixed workflow or an agent.

What is the deciding factor?

- A) Whether the task is well-defined and repeatable versus high-ambiguity, with a path that depends on intermediate findings.
- B) Whether the task involves calling more than three tools during a single review.
- C) Whether the review team prefers writing the automation in Python, in TypeScript, or in another general-purpose scripting language.
- D) Whether the review needs to finish running in under 30 seconds.

**Question 14.** A "clause-research subagent" has a vague description: "Helps with clauses." The main agent rarely delegates to it even when clause research is clearly needed.

What is the most likely cause and fix?

- A) The description drives delegation choices; rewriting it to state specifically what it does fixes under-delegation.
- B) The subagent needs more tools, so add several more clause-related tools, such as citation lookup and precedent tagging, to its definition.
- C) Subagents cannot be delegated to unless they are explicitly registered in `.mcp.json`.
- D) The main agent's sampling settings are too conservative for it to consider delegating tasks.

**Question 15.** The firm wants a hard guarantee that `redline_suggest` is never applied more than twice to the same clause within one review session, regardless of what the model decides mid-conversation.

What is the correct enforcement mechanism?

- A) A system prompt instruction, stated clearly near the top of the prompt, explaining the two-edit-per-clause limit in plain language for the agent to follow.
- B) A note added to the tool's own description mentioning the two-edit limit.
- C) A hook that tracks per-clause call counts and blocks the call once the limit is reached.
- D) Few-shot examples showing an agent stopping itself after two edits to a clause.

---

## Scenario B: Real-Time Streaming Support Chat Integration (Questions 16–30)

Helios Connect, a SaaS company, is integrating Claude into its live customer-support chat widget, where Claude drafts responses to customers in real time alongside human agents, occasionally calling tools (`search_kb`, `create_ticket`, `check_order_status`).

---

**Question 16.** Customers see Claude's response appear incrementally, word by word, in the chat widget as it's generated. Which technique enables this, and why?

- A) Streaming, since it lets the UI render output incrementally, reducing perceived latency.
- B) The Batch API, since it was designed specifically for real-time, low-latency customer-facing feedback during live chat sessions.
- C) Raising max_tokens so the full response arrives to the customer more quickly overall.
- D) Polling a status endpoint once per second until the full response becomes available.

**Question 17.** A live chat reply needs `check_order_status` called mid-conversation and the result fed back before the reply finishes, with a customer actively waiting.

Which API fits, and why?

- A) The Batch API, because it charges a lower per-token rate than the synchronous API.
- B) The Batch API, because it supports a tool call being answered partway through a single request.
- C) The synchronous Messages API with streaming, since the customer is waiting live and the tool call must be answered within the same request.
- D) The synchronous Messages API without streaming, since streaming and tool use cannot be combined in one request.

**Question 18.** Every chat turn sends the same 4,000-token support policy and tone guidelines, followed by the evolving conversation history, which varies per turn.

What optimization most directly reduces both latency and cost across many turns?

- A) Move the 4,000-token policy into a few-shot example block instead of the system prompt.
- B) Switch to the smallest available model for every single turn regardless of the resulting quality tradeoff for customers.
- C) Place the stable policy and tone instructions first in the system prompt and enable prompt caching.
- D) Truncate the policy text down to save a few tokens on every request.

**Question 19.** The `create_ticket` schema requires a `resolution_summary` field on every ticket. Many tickets are still open with no resolution yet, and Claude has started inventing placeholder text like "resolved by agent" rather than reporting none.

What schema change fixes this?

- A) Remove the `resolution_summary` field from the schema entirely so it can't be misused.
- B) Add a prompt instruction telling the model never to invent placeholder values for the resolution field on open tickets.
- C) Make `resolution_summary` nullable so a genuine absence can be reported truthfully.
- D) Reduce the model's sampling randomness so it invents fewer placeholder values overall.

**Question 20.** Two calls to `check_order_status` for the same order return different estimated delivery dates, and there's no way to tell which is correct from context alone.

What should the integration do?

- A) Average the two conflicting delivery-date estimates and present the result as fact.
- B) Surface both candidate values to a human agent for review rather than silently picking one.
- C) Always trust whichever call to `check_order_status` returned its result first.
- D) Discard the order lookup result entirely and tell the customer no delivery information is currently available at all.

**Question 21.** The chatbot occasionally outputs a `create_ticket` payload as free text that fails to parse as JSON, crashing the ticket-creation step in about 2% of cases.

What is the most reliable fix?

- A) Wrap the JSON parse in a try/catch and retry the same request with "valid JSON only" appended to the prompt.
- B) Add a JSON-repair library that patches common syntax issues in the free-text output before parsing it.
- C) Ask the model for YAML output instead, since it tends to be more forgiving of formatting drift.
- D) Define `create_ticket` as a tool with a matching input schema, and read the payload from the structured `tool_use` block instead of free text.

**Question 22.** Since switching `create_ticket` to strict schema-constrained tool use, payloads always parse successfully, but some tickets are labeled `priority: low` despite the customer describing a full outage.

What should the team conclude and do?

- A) Schemas eliminate syntax errors, not semantic ones; add a validation step checking priority against the message.
- B) The schema needs stricter enum types on the priority field to fix this.
- C) max_tokens is set too low, truncating the ticket payload mid-generation before validation even has a chance to run against the customer's original outage description.
- D) Abandon tool use entirely and go back to unstructured free-text tickets with human review.

**Question 23.** Customers occasionally attach screenshots of error dialogs. The integration currently runs OCR on the screenshot and sends only the extracted text to Claude, and responses are poor whenever OCR mangles the error code.

What is the most direct fix?

- A) Send the screenshot image itself as a content block, using Claude's native vision input instead of relying on OCR text.
- B) Raise max_tokens substantially so the model can work harder at interpreting the degraded, OCR-mangled error text it receives.
- C) Switch to a larger model, since bigger models always read noisy or garbled text better.
- D) Reject screenshot attachments from customers entirely going forward.

**Question 24.** The support widget needs to serve many concurrent chat sessions from different customers at once, without one customer's request blocking another's.

What must the integration layer support to do this?

- A) Streaming, since only a streamed response can support more than one customer session at once.
- B) The Batch API, since it's the only mechanism that runs more than one request at a time.
- C) A single request that concatenates every active customer session together into one payload, since Claude parallelizes work internally across sessions.
- D) Async, concurrent request handling so multiple calls stay in flight without blocking each other.

**Question 25.** The company plans to run the same chat integration through both the direct Anthropic API and a cloud-hosted equivalent for different regional deployments.

What should the team expect?

- A) The Messages API contract stays conceptually the same across vendors, though auth, plumbing, and feature-rollout timing can differ.
- B) The cloud-hosted equivalent requires an entirely different prompting approach and a redesigned schema.
- C) Batch processing is unavailable across every third-party vendor integration without exception.
- D) Extraction accuracy and latency are guaranteed to be identical across every vendor.

**Question 26.** The team enables extended thinking for complex troubleshooting conversations that use tool calls across several turns.

What must the integration layer do correctly?

- A) Ignore thinking content entirely, since it never has any effect on later turns.
- B) Convert the thinking output into a separate tool call so the reasoning gets logged the same way every other tool result is logged.
- C) Discard thinking content, but only on turns where a tool was also called.
- D) Treat the thinking block as distinct from the final answer text across the multi-turn conversation.

**Question 27.** Finance asks for an accurate per-conversation cost breakdown for the chat integration, but the current cost model only estimates based on average message length.

What should the improved cost model account for separately?

- A) Only cache read tokens, since caching is assumed by finance to already be the single dominant cost driver across the pipeline.
- B) Only output tokens, since input tokens are treated as effectively free.
- C) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- D) A flat per-conversation fee that ignores how much was actually generated.

**Question 28.** A new engineer argues the team can skip code review on the chat widget's surrounding application code since "the AI part is the risky part."

What is the correct response?

- A) Review should be skipped for any code that simply calls an external API.
- B) Code review becomes unnecessary for that code once the evals are passing.
- C) Only the prompt itself needs review; the surrounding application code is low-risk by definition.
- D) Standard SDLC practices — review, testing, version control — still apply to the surrounding application code, not just the prompt.

**Question 29.** A single long-running agent session is reused across an entire shift to handle chats from many different, unrelated customers, and the team notices Claude referencing a previous customer's order details in a new customer's chat.

What is the best fix?

- A) Reduce the model's sampling randomness across every session to prevent it from cross-referencing details between different prior customers.
- B) Start a fresh session for each new customer conversation rather than reusing one long-running session.
- C) Ask the model to "ignore earlier customers" at the start of every new chat.
- D) Widen the context window so more history fits without the model getting confused.

**Question 30.** A troubleshooting conversation is very long, and the team wants Claude to produce a maximally detailed final resolution summary, considering a very long requested output.

What tradeoff must they account for?

- A) None — input and output tokens draw from two completely independent budgets.
- B) Input and output share the same context-window budget, so a long history leaves less room for a long output.
- C) The length of the output has no measurable effect on response latency.
- D) Long outputs are truncated automatically by the platform no matter how large the underlying context window happens to be.

---

## Scenario C: Optimizing a Multilingual Content-Moderation Service (Questions 31–45)

GlobalGuard operates a content-moderation service that classifies user-generated posts across 40 languages for policy violations, processing millions of posts per day. Cost, latency, and consistency across languages all matter, and the team is tuning model selection, prompting, and context handling to hit targets.

---

**Question 31.** Most posts are short and moderation is a simple binary classification (violates / doesn't violate) at extremely high volume. Latency and cost per post matter far more than handling rare, ambiguous edge cases well.

Which approach best fits the default path?

- A) The highest-capability tier available for every post, to guarantee quality regardless of cost.
- B) Whichever tier happens to be cheapest per token, regardless of how well it fits the task.
- C) The same tier the company uses for its hardest reasoning tasks across every product line, chosen for consistency of behavior rather than fit to this specific task.
- D) A fast, low-latency tier for high-volume, low-complexity classification, reserving a higher tier for flagged posts.

**Question 32.** A small fraction of posts require nuanced judgment (satire versus genuine hate speech, or context-dependent slang) where the fast default model produces inconsistent classifications.

What is the most targeted fix?

- A) Add more few-shot examples covering satire, slang, and context-dependent cases to the fast model's prompt for every single post it classifies.
- B) Route only the flagged ambiguous posts to a higher-capability tier, or one with extended thinking enabled.
- C) Switch every post in the pipeline to the highest-capability tier to be safe.
- D) Raise max_tokens across the board so the model has more room to reason.

**Question 33.** The service floats to "whatever model is latest" in production. After a routine model update, classification thresholds shifted noticeably for borderline posts, with no code change on the team's side.

What should the team do differently?

- A) Pin a specific model version in production and test any upgrade deliberately, rather than always floating to whatever is latest.
- B) Nothing — threshold drift across model releases is expected, and there's no need to make the pipeline more deterministic.
- C) Roll back permanently to the oldest model version the API still supports.
- D) Disable all prompt caching across the pipeline to prevent behavior from drifting.

**Question 34.** Moderation output needs a consistent label set (`hate_speech`, `harassment`, `spam`, `none`), but detailed prose instructions describing the categories haven't produced consistent output across languages.

What technique is most likely to help?

- A) Write an even longer, more detailed prose description of the four categories, translated carefully into all forty supported languages.
- B) Reduce the model's sampling randomness to zero so labels stop varying.
- C) Provide 2–3 few-shot examples in multiple languages demonstrating the exact desired labeling.
- D) Ask the model to restate the category definitions before it classifies each post.

**Question 35.** A post thread is very long (reply chains with 100+ comments), and the team wants a maximally detailed moderation report per comment, considering a very long requested output.

What tradeoff must they account for?

- A) Input and output share the same context-window budget, so a long thread leaves less room for output.
- B) Long outputs are truncated automatically by the platform regardless of how large the context window happens to be.
- C) The length of the output has no measurable effect on response latency.
- D) Input and output tokens draw from two completely independent budgets.

**Question 36.** The moderation prompt currently places the specific post text before the general policy instructions and desired label format in every request.

Why might reordering improve both consistency and cacheability?

- A) Order has no measurable effect on either output consistency or on caching.
- B) Placing instructions at the very end of the prompt always improves how the model attends to them.
- C) Stable policy instructions belong in the system prompt as a consistent, cacheable prefix, with post-specific content placed after.
- D) Reordering only affects cost, and has no bearing on labeling consistency.

**Question 37.** Finance wants to know exactly how much the moderation service costs per post, but the team currently estimates cost only from average prompt length.

What should be instrumented instead?

- A) Actual token usage per request — input, output, and cache — attributed per post.
- B) Wall-clock latency per post, used as a rough proxy for cost.
- C) The raw number of API calls made per day across the whole pipeline, regardless of how many tokens each one actually used.
- D) A flat cost assumption based only on the post's character count.

**Question 38.** An engineer writes an automated eval that asserts the moderation label must exactly match a fixed reference string for a sample post, and the eval fails intermittently even though the labels look correct on manual review.

What is the most likely issue with the eval design?

- A) The model itself is broken and is simply producing wrong answers on this sample.
- B) LLM output is non-deterministic; exact-string-match evals are the wrong tool for checking it.
- C) The eval needs a longer reference string to compare against.
- D) Raise the sampling randomness so the eval's supposedly deterministic comparison passes more consistently.

**Question 39.** Posts arrive with full raw platform metadata dumps (every field of the post object) that bloat the prompt with mostly-irrelevant data, slowing the pipeline and increasing cost.

What is the best fix?

- A) Raise max_tokens to make room for the extra metadata fields already defined in the platform's schema for every post object.
- B) Prune the metadata down to the relevant fields before it enters the prompt.
- C) Switch to a model with a larger context window so the bloat matters less.
- D) Summarize the metadata with a separate Claude call before the classification call.

**Question 40.** For very long comment threads, the team notices moderation misses violations in the middle of the thread while catching issues in the opening and closing comments well.

What is the most effective mitigation?

- A) Switch to a model with an even larger context window than the current one.
- B) Add an instruction telling the model to "pay equal attention to the whole thread, especially the middle comments" before classifying.
- C) Alphabetize the comments in the thread before sending them for classification.
- D) Put a brief key-facts summary at the start of the input and organize detail under clear section headers.

**Question 41.** A moderation report confidently states a post "contains a direct threat of violence," but on manual review the post was actually a quote from a news article being discussed critically.

What practice would most help catch this class of error before action is taken?

- A) Trust confident, fluent-sounding output as evidence of correctness by default.
- B) Raise the model's sampling randomness across the pipeline so its answers about threats sound noticeably less confident.
- C) Shorten the report so there is less surface area for errors to hide in.
- D) Apply defensive parsing and skepticism toward confident output — verify key claims against the source post.

**Question 42.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON.

What is the more reliable approach?

- A) Repeat the JSON-formatting instruction even more emphatically in the prompt.
- B) Post-process every response to strip any text before the first `{`, instead of adding a hook that enforces the JSON format up front.
- C) Raise max_tokens so there's room in the response for both the preamble and the JSON.
- D) Use tool-use or schema-constrained output so structure is enforced by the API rather than requested through prose.

**Question 43.** The team wants to add an exploratory step that scans a user's full posting history for repeat-offense context before moderating the current post, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

What is the best structural approach?

- A) Load the user's entire posting history directly into the main moderation prompt on every request.
- B) Skip historical context entirely to avoid the bloat risk from a long posting history.
- C) Widen the context window so the full posting history always fits regardless of length.
- D) Have a subagent perform the historical scan in an isolated context and return only a distilled summary.

**Question 44.** For the simplest, most common moderation case (obvious spam links), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

What consideration should drive the choice?

- A) Multi-shot prompting is always strictly better than zero-shot for every moderation task, regardless of how simple or high-volume it is.
- B) Zero-shot is required whenever latency matters at all, no matter the task.
- C) The choice between zero-shot and multi-shot has no effect on cost or latency.
- D) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper than multi-shot.

**Question 45.** The moderation prompt has been modified informally by several engineers over time with no record of what changed or why, making it hard to diagnose a recent uptick in false positives.

What practice would have prevented this?

- A) Lock the prompt so that no one is ever able to change it again.
- B) Treat prompts as versioned artifacts, similar to code, so changes are tracked and attributable.
- C) Allow only one designated engineer to ever read the moderation prompt.
- D) Rewrite the moderation prompt completely from scratch every quarter regardless of whether the current one is working well.

---

## Scenario D: Claude Code Skills and Commands for a QA Team (Questions 46–60)

You support a 30-person QA team's use of Claude Code, custom skills, slash commands, and internal MCP servers (test-case management, defect tracking, test-environment provisioning). You're responsible for team-wide configuration, CI integration, and troubleshooting.

---

**Question 46.** A new QA engineer clones the team's test-automation repo, but Claude Code doesn't apply the team's established test-naming and assertion conventions, even though a teammate's machine applies them correctly.

What is the most likely cause?

- A) The new engineer needs to run a memory-refresh command to activate the team's memory files.
- B) A project CLAUDE.md requires an explicit import statement from the project root before it takes effect at all.
- C) The conventions live only in the teammate's personal, user-level configuration, which never travels through version control.
- D) The conventions file exceeded a size limit and was silently truncated on checkout.

**Question 47.** A nightly CI job invokes Claude Code to triage failing test runs and consistently hangs until timeout, with no visible error in the logs.

What is the most likely cause?

- A) The job is missing headless/print mode, so it waits for interactive input the CI runner never provides.
- B) The nightly test runs are simply too large in volume for the triage tool to process within a single invocation at all.
- C) The CI runner lacks permission to call the underlying model API.
- D) The repository's CLAUDE.md file is malformed and failing to parse.

**Question 48.** A downstream dashboard parses Claude Code's test-triage output with regex to auto-file defect tickets, and the parser breaks whenever output formatting drifts slightly between runs.

What is the robust fix?

- A) Harden the parsing regex with more permissive fallback patterns instead of adopting a formal output schema.
- B) Run with a JSON output format and a schema for the triage-findings structure, so output is machine-parseable by construction.
- C) Post the entire raw, unstructured output as a single comment on the ticket instead of parsing it at all.
- D) Add a stronger prompt instruction telling the model never to deviate from the format, without adding any real validation of what comes back.

**Question 49.** The team's `/scan-flaky-tests` custom command prints thousands of lines of historical test-run data, and testers report that Claude's answers about their actual task get noticeably worse right after running it.

What frontmatter change fixes this?

- A) An argument hint, so testers scope the flaky-test analysis more narrowly before running it.
- B) A forked-context setting, so the command's verbose output runs in an isolated sub-agent context.
- C) An allowed-tools restriction, limiting the command to read-only operations only.
- D) Remove the `/scan-flaky-tests` command entirely rather than adding any kind of hook or scoping to gate its verbose output.

**Question 50.** An internal `/generate-test-fixtures` skill is meant only to create new fixture files from a template, but an audit finds a session where it also ran shell commands that modified unrelated config files.

What is the correct guardrail?

- A) Add a warning inside the skill's own instructions telling Claude never to run shell commands.
- B) Require testers to commit their work before running any skill, as a safety net.
- C) Convert the skill into a slash command instead, since commands supposedly cannot run tools.
- D) Configure the skill's allowed-tools setting to permit only file-creation operations, making Bash unavailable during execution.

**Question 51.** A QA engineer needs to understand how a large, unfamiliar test-automation framework's fixture system works before writing new tests, and worries that reading dozens of files will exhaust context before implementation begins.

What is the best approach?

- A) Read every file in the framework in one long pass to be maximally thorough.
- B) Skip exploration entirely and infer the architecture from directory names alone.
- C) Split the exploration work across two separate terminal windows running the same session in parallel to save time.
- D) Use the Explore subagent for the discovery phase so verbose exploration stays in an isolated context.

**Question 52.** Mid-session, context is nearly full of verbose discovery output, but the engineer still needs to implement the new tests in the same session and wants to preserve key findings.

What should they do?

- A) Start a brand-new session and rely on memory of what was already learned.
- B) Run the compact command to summarize the conversation and reduce context usage.
- C) Temporarily delete the project's CLAUDE.md file to free up context space.
- D) Keep working as-is; irrelevant context from the fixture-system exploration is discarded automatically without any action needed.

**Question 53.** A multi-step Claude Code task that reads a test-config file, calls an internal MCP tool to fetch environment status, and writes a defect-triage report produces a wrong final report. Trace logs show the config was read correctly and the MCP tool returned valid data.

Where should debugging focus next?

- A) Re-read the config file again, since that was the earliest step in the pipeline.
- B) Inspect the network connection to the MCP server, since that's the most complex step.
- C) The step between receiving the MCP tool's valid data and producing the final report, since the inputs were already confirmed correct.
- D) Nothing further — a wrong final report produced from correct config data and correct MCP tool output means the whole task should simply be re-run from scratch.

**Question 54.** A test-environment provisioning tool integration fails, and the team can't tell whether the failure is in their integration code (bad auth, wrong endpoint) or in something the model did.

What is the correct first diagnostic step?

- A) Assume the failure is a model problem and immediately start rewriting the prompt.
- B) Switch to a different underlying model to see whether the failure persists.
- C) Restart the CI runner and try the provisioning step again without changes.
- D) Isolate whether the failure is in the integration layer's API call and response, or in the model's output.

**Question 55.** The internal defect-tracking system needs to be reachable from Claude Code sessions across the whole QA org, not just one team, and should be maintainable by the platform team independently of any consuming application.

What is the best approach?

- A) Build an MCP server exposing defect-tracking operations as tools, shared across the org.
- B) Have each team paste defect-tracker API credentials directly into its own CLAUDE.md file.
- C) Hard-code defect-tracking logic separately inside each team's own custom skill.
- D) Ask each engineer to curl the defect-tracker API manually whenever it's needed.

**Question 56.** An MCP server for the test-case management system exposes both a `search_test_cases` tool and a way for agents to see what test suites exist without an exploratory search call.

What is the second capability an example of?

- A) An MCP tool, functionally identical to `search_test_cases`, just returning the same unstructured text.
- B) An MCP resource — content or catalog visibility distinct from a tool, which performs an action.
- C) A built-in tool that the platform provides automatically to every agent.
- D) A Claude Code Skill packaged specifically for the test-case system.

**Question 57.** The team is deciding whether an internal MCP server for test-environment provisioning should run as a local stdio process per QA engineer's machine or as a remote, centrally-hosted network service.

What should drive the decision?

- A) Local stdio servers are always faster than remote servers regardless of deployment context.
- B) MCP only supports one communication pattern, so there is no real decision to make here.
- C) Remote servers are structurally unable to expose tools, only resources.
- D) Where the server must run and who needs access — local for per-machine use, remote for centrally shared services.

**Question 58.** The team's `.mcp.json`, committed to the repository, currently has a defect-tracker API token hardcoded directly in the file.

What is the correct fix?

- A) Base64-encode the token before committing the file to the repository.
- B) Rotate the token weekly on a fixed schedule instead of ever removing it from the committed configuration file.
- C) Move the token to environment-variable expansion so the secret is never committed to version control.
- D) Move the entire `.mcp.json` file into a private repository instead.

**Question 59.** An audit finds that several MCP-connected tools grant broader access (e.g., full test-suite deletion rights) than any actual QA workflow requires.

What is the correct remediation, consistent with least-privilege principles?

- A) Add logging around the broad access so misuse can be reviewed after the fact.
- B) Leave access as-is for now, since no misuse has actually been observed yet.
- C) Scope the exposed tools down to only the operations actual workflows require, removing unnecessary broad capabilities.
- D) Add a confirmation prompt before any deletion operation is allowed to run.

**Question 60.** The platform team is choosing how to expose a one-off, team-specific test-report-formatting workflow used by a single small QA squad, versus a widely-reused environment-health-check capability needed by every agent across the org.

How should each be built?

- A) The one-off workflow as a team-scoped Skill; the widely-reused capability as a centrally maintained MCP server or built-in tool.
- B) Build both as MCP servers, since MCP is claimed to be the correct choice for any shared capability.
- C) Build both as Skills, since Skills are assumed to always be reusable.
- D) Build both as built-in tools, since built-in tools supposedly require the least setup.

---
# Answer Key — Practice Exam 5

**Quick key:** 1-B, 2-A, 3-C, 4-C, 5-B, 6-A, 7-B, 8-B, 9-C, 10-D, 11-C, 12-A, 13-A, 14-A, 15-C, 16-A, 17-C, 18-C, 19-C, 20-B, 21-D, 22-A, 23-A, 24-D, 25-A, 26-D, 27-C, 28-D, 29-B, 30-B, 31-D, 32-B, 33-A, 34-C, 35-A, 36-C, 37-A, 38-B, 39-B, 40-D, 41-D, 42-D, 43-D, 44-D, 45-B, 46-C, 47-A, 48-B, 49-B, 50-D, 51-D, 52-B, 53-C, 54-D, 55-A, 56-B, 57-D, 58-C, 59-C, 60-A

---

**1. B** — The loop must key off `stop_reason`: continue while it's `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Text-based signals (A) are unreliable; a fixed cap (C) is a backstop, not a primary mechanism; whether flags were found (D) doesn't indicate loop completion.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent so the model can incorporate the result. B keeps the result from the model entirely. C misuses the system prompt for turn-level data. D discards conversational state unnecessarily.

**3. C** — A financially/legally significant rule needs deterministic enforcement via a hook that blocks the send outright. A, B, and D all remain probabilistic prompt compliance, which is exactly what's failing at the observed rate.

**4. C** — Forcing tool choice onto a specific tool guarantees that tool runs first; later turns proceed normally. `tool_choice: "any"` (B) guarantees some tool call, but not which one. A and D are probabilistic.

**5. B** — Removing tools unrelated to the agent's core role directly shrinks the candidate set the agent must reason over, improving selection reliability. A adds prompt overhead without removing capability bloat; C and D don't address tool-selection reliability at all.

**6. A** — Structured error metadata (category, retryable flag, description) lets the agent decide how to respond appropriately. Blanket retry (B) wastes calls on non-retryable failures. Asking the model to guess from context (C) is strictly worse than the tool reporting it. D reduces failure frequency without fixing the missing information, and leaves the same undifferentiated response format in place.

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

**18. C** — Only a shared prefix is cacheable; placing stable content first in the system prompt and variable content last maximizes cache hits, reducing both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without addressing caching.

**19. C** — Making the field nullable lets the model truthfully report a genuine absence instead of inventing a value to satisfy a required field. B and D rely on probabilistic compliance; A removes the field's value entirely.

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

**36. C** — Stable instructions first (ideally in the system prompt, cacheable) and variable content after both improves consistency (clear role separation) and caching. A, B, and D misstate the effect of ordering.

**37. A** — Actual per-request token usage (input/output/cache) attributed per post gives an accurate cost picture; estimates from average length or unrelated proxies (B, C, D) don't.

**38. B** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A and D misdiagnose the cause; C doesn't address the underlying non-determinism.

**39. B** — Pruning to relevant fields before data enters the prompt removes the actual bloat at its source. A and C work around the symptom without reducing waste; D adds cost and complexity for a problem solvable by simple filtering.

**40. D** — Placing a key-facts summary up front and organizing detail under clear headers directly counteracts the tendency to under-attend to the middle of long inputs. A is costly and doesn't guarantee the effect disappears; B and C don't address the underlying attention pattern.

**41. D** — Verifying key claims against the source post catches confident-but-wrong output that fluency alone would let through. A is the failure mode itself; B and C don't address correctness.

**42. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and B are workarounds for a problem that can be structurally eliminated; C doesn't address the preamble issue.

**43. D** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant findings. A and C reintroduce the bloat risk; B discards potentially useful context entirely.

**44. D** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format/edge-case consistency, which a simple high-volume task may not need. A and B are absolute claims that don't hold generally; C is false.

**45. B** — Versioning prompts like code enables attribution and rollback for quality regressions. A, C, and D are impractical overcorrections that don't provide the actual missing capability (change tracking).

**46. C** — User-level configuration never travels through version control, so a new engineer cloning the repo won't see it; team conventions must live in a committed project-level file instead. A, B, and D misdescribe how that configuration actually loads.

**47. A** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang rather than a clean error. B, C, and D would typically produce different, more specific failure signatures.

**48. B** — Schema-constrained JSON output is machine-parseable by construction, removing the fragile dependency on prose format stability. A, C, and D are reactive or abandon the structured-parsing requirement.

**49. B** — Forking the command's context isolates verbose output in a sub-agent context so only a summary returns, directly fixing the described context pollution. A narrows scope but doesn't isolate output; C restricts capability, not output destination; D removes useful functionality.

**50. D** — Restricting the skill's allowed tools is the enforcement mechanism that makes Bash structurally unavailable during the skill's execution. A is probabilistic and the violation already happened despite instructions; B mitigates damage rather than preventing it; C is a false claim about slash commands.

**51. D** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for implementation. A floods context directly; B guesses instead of investigating; C doesn't share context between windows meaningfully.

**52. B** — The compact command summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A discards findings; C frees trivial space while losing standards; D describes behavior that doesn't exist.

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
