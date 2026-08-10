# CCDVF Practice Exam 9

**Claude Certified Developer – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
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

Meridian & Cole LLP, a mid-size legal services firm, has built an internal agent that reviews incoming vendor contracts before partners sign off. The agent has custom tools — `search_clause_library`, `flag_risk`, `request_partner_review`, and `redact_pii` — and its recommendations carry real legal and compliance weight, so tool-calling discipline and escalation behavior matter as much as the quality of its clause analysis.

---

**Question 1.** The agent's harness needs to know when to stop executing tools and hand a finished review back to the paralegal who queued it.

Question: What signal should the harness key off? (Select ONE response.)

- A) Whether `flag_risk` has been called at least once in the conversation.
- B) A hard limit of five tool calls per contract, regardless of context.
- C) Whether the most recent tool call succeeded without an error.
- D) The `stop_reason` field on the response: continue the loop while it is `"tool_use"`, and stop once it becomes `"end_turn"`.

**Question 2.** After `search_clause_library` returns matching precedent clauses, the harness needs the agent to keep reasoning about the contract with that information available.

Question: What must the harness do? (Select ONE response.)

- A) Append a `tool_result` block referencing the corresponding `tool_use` ID to the conversation and resend the full conversation to the model.
- B) Write the clause matches to a shared database and let the agent query it separately if needed.
- C) Paste the clause matches into the system prompt so they persist for future contracts too.
- D) Summarize the matches in a new user-authored message unrelated to the tool call.

**Question 3.** Firm policy requires a licensed partner to approve any recommendation to reject a vendor contract outright. The system prompt states this rule clearly, but an audit finds the agent occasionally recommended outright rejection without triggering `request_partner_review`.

Question: What is the most reliable fix? (Select ONE response.)

- A) Repeat the rule near the end of the system prompt as well as the beginning.
- B) Add several few-shot examples of the agent correctly escalating rejection recommendations.
- C) Lower the temperature so the agent follows written policy more consistently.
- D) Implement a hook that intercepts any final review output recommending rejection and blocks delivery unless `request_partner_review` was called first.

**Question 4.** The firm wants every review to begin with a mandatory `search_clause_library` call, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation? (Select ONE response.)

- A) Set `tool_choice: {"type": "tool", "name": "search_clause_library"}` on the first request, then allow normal tool choice afterward.
- B) State in the system prompt that clause-library lookup must always happen first.
- C) Set `tool_choice: "any"` on the first request so some tool call is guaranteed.
- D) Add several few-shot transcripts showing the clause lookup running first.

**Question 5.** The agent currently has eleven tools, including several rarely used ones (billing lookup, e-signature routing, calendar scheduling) that have nothing to do with clause review. Tool selection has become inconsistent, with the agent occasionally calling the wrong tool for a straightforward review.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` so the agent has more room to reason about tool choice.
- B) Add a system-prompt note ranking the eleven tools by importance.
- C) Remove or scope out the tools unrelated to contract review from this agent's tool set.
- D) Keep all eleven tools but rename them more descriptively.

**Question 6.** `redact_pii` currently returns the plain string `"failed"` whether the input document was missing, the redaction service timed out, or the user lacked permission to redact that document type. The agent responds inconsistently to each case.

Question: What is the best fix? (Select ONE response.)

- A) Add an automatic retry wrapper around every call.
- B) Add a system-prompt note asking the agent to infer the failure type from context.
- C) Return structured error metadata: an error category, a retryable flag, and a human-readable description.
- D) Increase the redaction service's timeout so failures occur less often.

**Question 7.** When `search_clause_library` finds no precedent matching an unusual clause, it currently returns an error. The agent responds by apologizing for a "system issue" and retrying the identical query.

Question: What should change? (Select ONE response.)

- A) Add a system-prompt note explaining that this particular error usually means no precedent exists.
- B) Have the agent call `flag_risk` automatically whenever this error occurs.
- C) Return a successful response with an empty result set, reserving errors for genuine access failures.
- D) Add a hook that silently ends the review whenever this error appears.

**Question 8.** An associate proposes replacing the agent's judgment with a fixed sequence — always run `search_clause_library`, then `flag_risk`, then decide — arguing this makes review behavior predictable across all contract types.

Question: Why is model-driven tool selection the better fit here? (Select ONE response.)

- A) Fixed sequences cannot invoke custom tools, only built-in ones.
- B) Model-driven selection is always cheaper because it uses fewer reasoning tokens.
- C) The harness technically cannot execute a fixed tool sequence.
- D) Contract review is high-ambiguity; which clauses matter and what to check next depends on what earlier tool calls reveal, which a fixed sequence can't adapt to.

**Question 9.** The firm wants to add `request_partner_review` but is deciding whether to give the main review agent that tool directly, or delegate escalation decisions to a separate, narrowly-scoped subagent. Escalating unnecessarily wastes a partner's billable time.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) A narrowly-scoped subagent can be given only the escalation tool and explicit escalation criteria, reducing the chance the main agent escalates unnecessarily while reasoning about unrelated clauses.
- B) Subagents execute noticeably faster than tools called directly by the main agent.
- C) The main agent's context window is too small to hold the escalation tool's schema.
- D) Subagents are required whenever a tool has a real-world consequence.

**Question 10.** During review of a lengthy master services agreement, the agent's context fills with verbose raw clause-library search results, leaving little room to reason about the contract's actual risk profile.

Question: What is the best structural fix? (Select ONE response.)

- A) Read only the first search result returned for every query.
- B) Disable clause-library search and rely on the agent's general knowledge instead.
- C) Increase `max_tokens` so responses can be longer.
- D) Delegate clause-library exploration to a subagent that returns a distilled summary of relevant precedent, keeping the main agent's context focused on risk analysis.

**Question 11.** The agent escalates a contract to a partner, but the partner has no visibility into what the agent checked beforehand — logs show fifteen minutes of tool calls with no accessible summary.

Question: What should the escalation include? (Select ONE response.)

- A) The full raw transcript of every tool call and result.
- B) A structured handoff summary: what clauses were checked, what was found, and a recommended next action.
- C) Just the final risk flag, since the partner can re-investigate independently.
- D) A tone analysis of how urgent the contract language seemed.

**Question 12.** The firm is deciding between running the agent through a hosted, Anthropic-managed execution environment versus self-hosting the harness on firm-owned infrastructure, given confidentiality obligations to clients.

Question: What is the core tradeoff to weigh? (Select ONE response.)

- A) Self-hosted agents cannot use custom tools like `redact_pii`.
- B) Managed agents are inherently less secure than self-hosted ones.
- C) Operational control (self-hosted) versus operational burden (managed) — there is no inherent difference in what tools the agent can call.
- D) Managed agents cannot access firm-internal infrastructure under any configuration.

**Question 13.** A partner asks whether the contract-intake process should be built as a fixed workflow or as an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the process needs to run in under a minute.
- B) Whether the firm's engineers prefer Python or TypeScript.
- C) Whether the task is well-defined and repeatable versus high-ambiguity, with the right next step depending on intermediate findings.
- D) Whether more than three tools are involved.

**Question 14.** A proposed "precedent-research subagent" has a vague `AgentDefinition` description: "Helps with clauses." The main agent rarely delegates to it even for contracts that clearly need deep precedent research.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The main agent's temperature is too low to consider delegating.
- B) The description drives delegation choices; rewriting it to state specifically what the subagent does and when to use it will most directly fix under-delegation.
- C) The subagent needs additional tools before delegation will occur.
- D) Subagents cannot be delegated to unless registered in a global configuration file.

**Question 15.** The firm wants a hard guarantee that `request_partner_review` is never triggered more than once per contract within a single review session, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system-prompt instruction stating the one-call limit clearly.
- B) A note in the tool's description mentioning the limit.
- C) Few-shot examples showing an agent stopping after one escalation.
- D) A hook that tracks the per-contract call count and blocks the tool call once the limit is reached.

---

## Scenario B: Real-Time Streaming Support Chat Integration (Questions 16–30)

Northbay Retail runs a customer support chat widget where Claude answers order and shipping questions live while a customer is typing and waiting. The team is integrating streaming responses, tool calls for order lookups, and multi-vendor deployment considerations into the widget's backend.

---

**Question 16.** Customers watch a live typing indicator while Claude composes its answer, and the team wants the first words to appear as quickly as possible rather than waiting for the full response.

Question: What technique best supports this? (Select ONE response.)

- A) Streaming, so the UI can render output incrementally as tokens arrive, reducing perceived latency.
- B) Increasing `max_tokens` so the full response finishes generating sooner.
- C) The Message Batches API, since it is designed for asynchronous chat delivery.
- D) Polling a status endpoint every 500 milliseconds until the response is ready.

**Question 17.** A nightly job re-summarizes the day's closed support chats for a quality dashboard. No customer is waiting on the result, and none of the summarization steps need a mid-request tool call.

Question: Which API best fits, and why? (Select ONE response.)

- A) The Message Batches API — latency-tolerant, non-blocking, high-volume work at reduced cost.
- B) The synchronous Messages API run across many parallel threads to finish quickly.
- C) The synchronous Messages API with `max_tokens` minimized.
- D) The synchronous Messages API paired with a smaller model to reduce cost.

**Question 18.** The team wants to add an "order-status lookup, verify against shipping carrier, retry if the carrier API times out" loop to the live chat flow, and considers running the whole loop through the Batch API to save cost.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API's context window is too small for chat transcripts.
- B) The 24-hour completion window makes retries structurally impossible.
- C) The Batch API cannot execute a tool call mid-request and feed the result back to the model within a single request — required for this loop, and incompatible with a live customer waiting anyway.
- D) The Batch API does not support system prompts.

**Question 19.** Every chat turn sends the same 4,500-token support policy and tone guidelines, followed by the specific customer message, which varies per turn.

Question: What optimization most directly reduces both latency and cost across many turns? (Select ONE response.)

- A) Move the policy guidelines into a few-shot example block instead.
- B) Switch to the smallest available model regardless of answer quality.
- C) Place the stable policy and tone guidelines first, enable prompt caching, and put the varying customer message last.
- D) Truncate the policy guidelines to reduce token count.

**Question 20.** The order-lookup tool's JSON output occasionally fails to parse — about 4% of chat turns produce malformed JSON that breaks the widget's rendering logic.

Question: What is the most reliable fix? (Select ONE response.)

- A) Ask for YAML output instead, since it tolerates formatting drift better.
- B) Define a `submit_order_lookup` tool whose input schema matches the needed structure, and read the data from the structured `tool_use` block instead of parsing free text.
- C) Wrap the parse in a try/catch and retry with "valid JSON only" appended to the prompt.
- D) Add a JSON-repair library to fix common syntax issues before parsing.

**Question 21.** Since switching to schema-constrained tool use for order lookups, output always parses successfully, but the widget occasionally displays a shipping estimate that contradicts the actual carrier status returned in the same tool call.

Question: What should the team conclude and do? (Select ONE response.)

- A) Schema compliance guarantees syntax, not semantics — add a validation step that checks the displayed estimate against the carrier status on top of schema compliance.
- B) `max_tokens` is too low, truncating output mid-generation.
- C) The schema needs stricter date types to fix this.
- D) Abandon tool use and return to free-text order lookups with manual review.

**Question 22.** Some customers attach a photo of a damaged product, and the pipeline currently sends only an OCR-extracted caption of the image to Claude. Answers about visible damage are poor when the caption is generic or missing detail.

Question: What is the most direct fix? (Select ONE response.)

- A) Switch to a larger model, since bigger models are always better at working from vague captions.
- B) Increase `max_tokens` so the model can reason harder about the caption.
- C) Send the photo itself as an image content block alongside the customer's message, using Claude's native vision input instead of relying solely on the caption.
- D) Reject photo attachments from the chat flow entirely.

**Question 23.** The widget needs to look up order status, shipping carrier data, and loyalty-point balance concurrently to keep the live chat responsive, rather than fetching each one sequentially.

Question: What must the integration layer support? (Select ONE response.)

- A) A single request with all three lookups concatenated, since Claude parallelizes internally.
- B) The Batch API, since it is the only way to issue more than one request at a time.
- C) Streaming, since only streaming supports concurrent operations.
- D) Async/concurrent request handling, so multiple API calls can be in flight without blocking on each other.

**Question 24.** Northbay plans to run the same chat integration through both the direct Anthropic API and a third-party cloud marketplace deployment for a separate regional entity.

Question: What should the team expect? (Select ONE response.)

- A) The Messages API contract stays conceptually the same across vendors, though auth/plumbing and feature-rollout timing can differ.
- B) The marketplace deployment requires a completely different prompting approach and schema design.
- C) Batch processing is unavailable on any third-party vendor integration.
- D) Response latency is guaranteed to be identical to the millisecond across vendors.

**Question 25.** The team enables extended thinking for a complex refund-eligibility chat flow that spans several tool-use turns.

Question: What must the integration layer handle correctly? (Select ONE response.)

- A) Convert thinking output into an additional tool call automatically.
- B) Treat the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- C) Discard thinking content whenever a tool is also involved in that turn.
- D) Ignore thinking content entirely, since it never affects downstream turns.

**Question 26.** Finance asks for an accurate per-conversation cost breakdown for the chat integration, but the current model only estimates cost from average message length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only output tokens, since input tokens are effectively free.
- B) Input tokens, output tokens, and cache read/write tokens, since each is priced differently.
- C) A flat per-conversation fee regardless of token usage.
- D) Only cache read tokens, since caching dominates the cost.

**Question 27.** A new engineer argues the team can skip code review on the chat backend's request-handling code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Only the prompt needs review; surrounding code is low-risk by definition.
- B) Code review is unnecessary once evals pass.
- C) Review should be skipped for any code that merely calls an external API.
- D) Standard SDLC practices — code review, testing, version control — still apply to the application code around Claude; integrating an LLM doesn't replace engineering discipline.

**Question 28.** A single long-running chat session stays open across an entire shift, handling unrelated conversations from different customers back-to-back, and agents notice Claude increasingly referencing details from unrelated earlier conversations.

Question: What is the best fix? (Select ONE response.)

- A) Start a fresh session (or `/compact`) at natural task boundaries, such as between different customers, rather than accumulating unrelated context in one long session.
- B) Ask the model to "ignore earlier customers" at the start of each new chat.
- C) Increase the context window so more history fits without confusion.
- D) Reduce temperature to prevent cross-referencing.

**Question 29.** The chat widget shows users a real-time "Claude is checking your order" indicator, but the current backend waits for the entire response — including tool results — before sending anything to the frontend, making the indicator feel frozen.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` so the response completes and arrives sooner overall.
- B) Switch the order lookup to the Batch API for faster completion.
- C) Reduce the number of tools available to shorten reasoning time.
- D) Stream the response and surface intermediate signals (e.g., tool-use events) to the frontend as they occur, rather than waiting for the full turn to complete.

**Question 30.** An engineer proposes an automated eval that asserts the chat response must exactly match a fixed reference string for a sample "where's my order" question, and the eval fails intermittently even though responses look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) Temperature should be increased to fix the intermittent failures.
- B) The model is broken and producing wrong answers.
- C) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation rather than asserting exact text.
- D) The eval needs a longer reference string.

---

## Scenario C: Optimizing a Multilingual Content-Moderation Service (Questions 31–45)

Vantora Media runs a content-moderation service that screens user-submitted comments across a dozen languages for policy violations before publication, processing several million comments per day. The team is tuning model selection, prompting, and context handling to keep latency, cost, and moderation consistency within target.

---

**Question 31.** Most submitted comments are short and moderation is a simple binary classification. Latency and per-comment cost matter far more than handling rare, highly ambiguous edge cases perfectly.

Question: Which model tier best fits the default moderation path? (Select ONE response.)

- A) The highest-capability tier available, to guarantee accuracy on every comment.
- B) A fast, low-latency tier suited to high-volume/low-complexity classification, reserving a higher tier only for comments flagged as ambiguous.
- C) Whichever tier is cheapest per token, regardless of task fit.
- D) The same tier used for the company's hardest reasoning tasks, for consistency across teams.

**Question 32.** A small fraction of comments require nuanced judgment (satire versus genuine harassment, coded language, cultural context) where the fast default model produces shallow or inconsistent verdicts.

Question: What is the most targeted fix? (Select ONE response.)

- A) Increase `max_tokens` for every comment to give more room to reason.
- B) Add more few-shot examples to the fast model's prompt for every comment.
- C) Switch every comment to the highest-capability tier to be safe.
- D) Route only the flagged ambiguous comments to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, moderation verdicts shifted noticeably in borderline cases with no code change.

Question: What should the team do differently? (Select ONE response.)

- A) Disable all prompt caching to prevent drift.
- B) Roll back permanently to the oldest available model version.
- C) Nothing — behavior drift across releases is expected and needs no process.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Moderation verdicts need a consistent structure (category, confidence, rationale) but detailed prose instructions describing that structure haven't produced consistent output across languages.

Question: What technique is most likely to help? (Select ONE response.)

- A) Provide 2–3 few-shot examples demonstrating the exact desired structure.
- B) Write an even longer, more detailed prose description of the structure.
- C) Ask the model to restate the structure before producing a verdict.
- D) Lower the temperature to zero.

**Question 35.** A flagged comment thread includes 40+ replies for context. The team wants a maximally detailed rationale for each verdict and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) Long outputs are always truncated regardless of context window size.
- B) None — input and output tokens are budgeted completely independently.
- C) Output length has no effect on latency.
- D) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.

**Question 36.** The moderation prompt currently places the specific comment text before the general moderation policy and category definitions in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last always improves model attention.
- B) Reordering only affects cost, never consistency.
- C) Order has no measurable effect on either consistency or caching.
- D) Stable, role-defining policy content belongs first so it forms a consistent, cacheable prefix; the varying comment text should come after.

**Question 37.** Finance wants an exact per-comment cost figure for the moderation service, but the team currently estimates cost only from average comment length.

Question: What should be instrumented instead? (Select ONE response.)

- A) A flat cost assumption based on comment character count.
- B) Actual token usage per request — input, output, and cache — attributed per comment, rather than an estimate from average length.
- C) Wall-clock latency per comment, used as a cost proxy.
- D) Number of API calls only, regardless of token count.

**Question 38.** Comments arrive with full raw platform metadata (device info, session IDs, every historical edit) that bloats the prompt with mostly-irrelevant data, slowing the pipeline.

Question: What is the best fix? (Select ONE response.)

- A) Switch to a model with a larger context window so the bloat matters less.
- B) Summarize the metadata with a second Claude call before moderation.
- C) Increase `max_tokens` to accommodate the extra data.
- D) Prune the metadata to the relevant fields before it enters the prompt, rather than passing raw dumps.

**Question 39.** For long comment threads, moderators notice verdicts consistently miss policy violations buried in the middle of the thread while catching violations in the opening and closing comments reliably.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Add an instruction telling the model to "pay equal attention to the whole thread."
- B) Switch to a model with an even larger context window.
- C) Alphabetize comments before moderation.
- D) Put a brief thread overview at the start of the input and organize the detailed comments under clear section markers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 40.** A verdict confidently states that a comment "contains a direct threat," but on manual review the comment contains no such language.

Question: What practice would most help catch this class of error before it reaches enforcement? (Select ONE response.)

- A) Shorten the rationale so there's less room for errors.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims against the source comment rather than accepting fluency as correctness.
- C) Increase the model's temperature so verdicts sound less confident.
- D) Trust confident, fluent-sounding output as evidence of correctness by default.

**Question 41.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON in a few languages.

Question: What is the more reliable approach? (Select ONE response.)

- A) Post-process every response to strip text before the first `{`.
- B) Repeat the JSON instruction more emphatically for those languages.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Increase `max_tokens` so there's room for both the preamble and the JSON.

**Question 42.** The team wants to add an exploratory step that scans a user's full comment history for repeat-offense context before moderating the current comment, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main moderation step.
- B) Load the entire comment history directly into the main prompt every time.
- C) Skip historical context entirely to avoid the bloat risk.
- D) Increase the context window so the full history always fits.

**Question 43.** For the simplest, highest-volume comment category (obvious spam links), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) The choice has no effect on cost or latency.
- B) Zero-shot is required whenever latency matters at all.
- C) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- D) Multi-shot is always strictly better regardless of task simplicity.

**Question 44.** The moderation prompt has been informally edited by several engineers over time with no record of what changed or why, making it hard to diagnose a recent uptick in false positives.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt so no one can ever change it again.
- C) Only allowing one designated engineer to ever read the prompt.
- D) Rewriting the prompt from scratch every quarter.

**Question 45.** An automated eval suite for the moderation service checks only whether the verdict category matches a reference label, and passes even when the rationale field is nonsensical or references the wrong comment.

Question: What is the most useful improvement to the eval suite? (Select ONE response.)

- A) Extend the eval to also check rationale quality and grounding (e.g., does it reference content actually present in the comment), not just the final category label.
- B) Remove the rationale field entirely so there's nothing extra to check.
- C) Increase the number of reference labels used for category checks only.
- D) Run the category-only eval more frequently to catch regressions sooner.

---

## Scenario D: Claude Code Skills and Commands for a QA Team (Questions 46–60)

Cascade Software's QA team has adopted Claude Code for writing test plans, triaging flaky tests, and drafting bug reports, and has built a set of team-specific Skills and slash commands (`/triage-flaky`, `/draft-bug-report`, `/gen-test-plan`). You support this team's configuration, CI usage, and troubleshooting.

---

**Question 46.** A new QA hire clones the team's test-automation repository, but Claude Code doesn't apply the team's established bug-report conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) CLAUDE.md requires an explicit `@import` from the project root to take effect at all.
- B) The new hire needs to run `/memory` to activate memory files.
- C) The conventions file exceeded a size limit and was silently truncated.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that never travels through version control.

**Question 47.** A nightly CI job invokes Claude Code to triage newly flaky tests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The repository's CLAUDE.md is malformed.
- B) The flaky-test list is too large for Claude Code to process.
- C) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- D) The CI runner lacks permission to call the Claude API.

**Question 48.** A downstream dashboard parses `/triage-flaky` output with regex to file tickets automatically, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Add a stronger prompt instruction never to deviate from the format.
- B) Harden the regex with more permissive fallback patterns.
- C) Run with `--output-format json` and a defined schema for the triage findings, producing machine-parseable output.
- D) Post the entire raw output as a single ticket comment instead of parsing it.

**Question 49.** The `/gen-test-plan` command prints thousands of lines of exploratory code-reading output while building context on the feature under test, and QA engineers report Claude's answers about their actual follow-up questions get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `argument-hint`, so engineers scope the exploration more narrowly.
- B) `context: fork`, so the command's verbose exploration runs in an isolated sub-agent context and only a summary returns to the main conversation.
- C) Removing the command entirely.
- D) `allowed-tools`, restricting the command to read-only operations.

**Question 50.** An internal `/draft-bug-report` Skill is meant only to create a formatted markdown file from a template, but an audit finds a session where it also ran shell commands that modified unrelated test fixtures.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the Skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- B) Add a warning in the Skill's instructions telling Claude never to run shell commands.
- C) Require engineers to commit their work before running any Skill.
- D) Convert the Skill into a slash command, since commands cannot run tools.

**Question 51.** A QA engineer needs to understand how a flaky integration test's setup fixtures interact across a large, unfamiliar test suite before proposing a fix, and worries that reading dozens of files will exhaust context before the fix itself is written.

Question: What is the best approach? (Select ONE response.)

- A) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- B) Read every file in the test suite in one pass to be thorough.
- C) Skip exploration and infer fixture behavior from file names.
- D) Split the investigation across two separate terminal windows.

**Question 52.** Mid-session, context is nearly full of verbose fixture-exploration output, but the engineer still needs to implement the fix in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Continue working; Claude automatically discards irrelevant context.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md temporarily to free context space.
- D) Start a brand-new session and rely on memory of what was learned.

**Question 53.** A multi-step Claude Code task that reads a test-config file, calls `/triage-flaky`'s underlying analysis, and writes a bug report produces a wrong root-cause conclusion. Trace logs show the config was read correctly and the triage analysis returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Nothing — a wrong conclusion with correct inputs means the task should simply be re-run.
- B) The step between receiving the valid triage data and producing the final conclusion — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- C) The network connection used to read the test-config file, since that's the earliest step.
- D) Re-read the test-config file again, since that's the earliest step.

**Question 54.** A test-runner integration fails intermittently, and the QA team can't tell whether the failure is in their integration code (bad flags, wrong exit-code parsing) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Assume it's a model problem and rewrite the prompt.
- B) Isolate whether the failure occurred at the integration layer (the actual command invocation and its output) versus in the model's output, by examining the trace of exactly what was run and returned.
- C) Switch to a different model to see if the failure persists.
- D) Restart the CI runner and try again.

**Question 55.** The QA team wants `/gen-test-plan` to be usable and maintainable across every team at Cascade Software, not just QA, and updated centrally without each team needing to copy files around.

Question: What is the best approach? (Select ONE response.)

- A) Package it as a plugin/shared Skill distributed centrally, rather than a per-repository command each team copies and maintains independently.
- B) Have each team paste the command's instructions into their own CLAUDE.md.
- C) Ask each engineer to manually re-type the plan format when needed.
- D) Hard-code the test-plan logic into each team's own custom script separately.

**Question 56.** The team's `.claude/settings.json`, committed to the repository, currently has a bug-tracker API token hardcoded directly in a hook script referenced by the config.

Question: What is the correct fix? (Select ONE response.)

- A) Base64-encode the token before committing it.
- B) Rotate the token weekly instead of removing it from the file.
- C) Move the token to environment-variable expansion so the secret isn't committed to version control.
- D) Move the settings file to a private repository instead.

**Question 57.** An audit finds that `/triage-flaky`'s `allowed-tools` configuration grants it broader shell access (including the ability to delete test artifacts) than the triage workflow actually requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Leave access as-is, since no misuse has been observed yet.
- B) Add a confirmation prompt before any deletion.
- C) Scope `allowed-tools` down to only the operations the triage workflow actually requires, removing unnecessary broad capabilities rather than just monitoring them.
- D) Add logging so misuse can be reviewed after the fact.

**Question 58.** The QA team is choosing how to expose a one-off, team-specific bug-report formatting workflow used only by QA, versus a widely-reused test-environment-health-check capability needed by every engineering team at Cascade.

Question: How should each be built? (Select ONE response.)

- A) The one-off bug-report workflow as a Skill or command scoped to the QA team; the widely-reused health-check capability as a centrally maintained plugin/shared tool available to every consuming team.
- B) Both as one-off Skills, since Skills are always team-specific.
- C) Both as centrally maintained plugins, since that is the correct choice for any capability.
- D) Both as ad hoc shell scripts, since that requires the least setup.

**Question 59.** The QA lead wants Claude Code sessions to automatically run the project's linter and block a commit if it fails, without relying on Claude choosing to run the linter on its own.

Question: What is the correct mechanism? (Select ONE response.)

- A) A hook bound to the relevant lifecycle event (e.g., before commit) that runs the linter deterministically and blocks the action on failure.
- B) A CLAUDE.md instruction telling Claude to always lint before committing.
- C) A few-shot example showing a session running the linter before committing.
- D) A Skill description mentioning that linting is recommended.

**Question 60.** A `/draft-bug-report` command frequently produces reports with an inconsistent severity field — sometimes "High," sometimes "P1," sometimes "critical" — because the command's prompt only says to "assign an appropriate severity."

Question: What is the most reliable fix? (Select ONE response.)

- A) Lower the temperature used for the command.
- B) Constrain the severity field with an explicit enumerated set of allowed values (e.g., via schema-constrained output or an explicit list in the instructions), rather than leaving it to free-text judgment.
- C) Ask engineers to manually correct the severity field after generation.
- D) Remove the severity field from bug reports entirely.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-A, 5-C, 6-C, 7-C, 8-D, 9-A, 10-D, 11-B, 12-C, 13-C, 14-B, 15-D, 16-A, 17-A, 18-C, 19-C, 20-B, 21-A, 22-C, 23-D, 24-A, 25-B, 26-B, 27-D, 28-A, 29-D, 30-C, 31-B, 32-D, 33-D, 34-A, 35-D, 36-D, 37-B, 38-D, 39-D, 40-B, 41-C, 42-A, 43-C, 44-A, 45-A, 46-D, 47-C, 48-C, 49-B, 50-A, 51-A, 52-B, 53-B, 54-B, 55-A, 56-C, 57-C, 58-A, 59-A, 60-B

---

**1. D** — The loop must key off `stop_reason`: continue while it is `"tool_use"`, stop at `"end_turn"`. Whether a specific tool was called (A), a fixed call cap (B), and error status (C) are all unreliable or secondary signals compared to the authoritative field.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent. Writing to a separate database (B) hides the result from the model; the system prompt (C) is the wrong place for turn-level data; a plain user message (D) breaks the expected tool-result linkage.

**3. D** — A compliance-critical rule needs deterministic enforcement via a hook that blocks delivery outright. Repeating the rule (A), few-shot examples (B), and lowering temperature (C) all remain probabilistic prompt compliance, which is exactly what's failing.

**4. A** — Forcing tool choice on a specific tool guarantees it runs first; later turns proceed normally. A system-prompt statement (B) and `tool_choice: "any"` (C) don't guarantee which tool runs; few-shot examples (D) remain probabilistic.

**5. C** — Removing tools unrelated to the agent's core role directly reduces the candidate set the model must reason over. More reasoning tokens (A), a ranking note (B), and renaming (D) don't remove the actual capability bloat causing misselection.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent respond appropriately to each distinct failure. Blanket retry (A) wastes calls on non-retryable failures; asking the model to guess (B) is worse than the tool reporting it; a longer timeout (D) reduces frequency without fixing missing information.

**7. C** — "No precedent found" is a valid empty result, not a failure — return success with an empty set. A prompt note (A) papers over the underlying conflation; auto-flagging (B) invents an unwarranted extra step; silently ending review (D) hides real signal.

**8. D** — High-ambiguity review where the next step depends on earlier findings is the core case for model-driven tool selection. The other options make unsupported technical claims about fixed sequences or cost.

**9. A** — A narrowly-scoped subagent with only the escalation tool and explicit criteria minimizes unnecessary escalations while the main agent reasons about unrelated clauses. B, C, and D are unsupported or overgeneralized claims.

**10. D** — Delegating clause exploration to a subagent that returns a distilled summary keeps the main agent's context focused on risk analysis. Reading only one result (A) loses information; disabling search (B) removes needed capability; more `max_tokens` (C) doesn't address context accumulation.

**11. B** — A structured handoff (what was checked, what was found, recommended action) lets a partner act immediately. A raw transcript (A) forces reconstruction; the flag alone (C) omits context; a tone analysis (D) conveys mood, not facts.

**12. C** — The tradeoff is operational control versus operational burden; tool-calling capability doesn't differ between deployment models. A, B, and D are unsupported absolute claims.

**13. C** — Task predictability versus dependency on intermediate findings is the deciding factor between workflow and agent, not runtime, language, or tool count.

**14. B** — Subagent descriptions drive delegation choices; a vague description causes under-delegation regardless of the subagent's actual capability. A, C, and D misdiagnose the cause.

**15. D** — A per-contract call-count hook is the only option that deterministically guarantees the limit; A, B, and C remain probabilistic prompt-level guidance.

**16. A** — Streaming renders output incrementally as tokens arrive, directly reducing perceived latency for a live typing indicator. B, C, and D don't address perceived latency the same way, and Batch/polling are the wrong tools for live chat.

**17. A** — Latency-tolerant, non-blocking, high-volume work with no mid-request tool calls is exactly the Batch API's fit, at reduced cost. B doesn't reduce per-token cost; C and D risk quality or don't address the real cost lever.

**18. C** — A retry/verify loop requires mid-request tool use, which the Batch API can't do — and it's the wrong fit for a live customer waiting regardless. A, B, and D misidentify the actual limitation.

**19. C** — Placing stable content first with caching enabled and variable content last maximizes cache hits, cutting both latency and cost. A, B, and D either break the cacheable prefix or degrade quality without addressing caching.

**20. B** — Tool-use with a matching input schema guarantees structurally valid output, eliminating the parsing failure class outright. A, C, and D are workarounds for a problem that can be structurally eliminated.

**21. A** — Schema validity guarantees syntax, not semantics; a separate validation step is needed to catch cross-field contradictions. B, C, and D misdiagnose or abandon a working mechanism.

**22. C** — Sending the photo directly as a vision content block bypasses a lossy, generic caption entirely. A and B don't address the actual data bottleneck; D discards otherwise-useful attachments.

**23. D** — Concurrent lookups require async/non-blocking request handling in the integration layer. A, B, and C misstate how concurrency is actually achieved.

**24. A** — The Messages API contract stays conceptually consistent across vendors, though plumbing and rollout timing can differ — the realistic expectation, not identical latency or a wholly different prompting approach.

**25. B** — Thinking content is a distinct block type that must be handled (and typically preserved) separately from final answer text across multi-turn tool-use conversations. A, C, and D mishandle or misdescribe this.

**26. B** — Input, output, and cache tokens are priced differently and must be modeled separately for an accurate cost breakdown. A, C, and D all oversimplify in ways that produce an inaccurate model.

**27. D** — Standard SDLC discipline still applies to the application code around an LLM integration; the model doesn't replace engineering rigor for the surrounding system.

**28. A** — Resetting at natural task boundaries (e.g., between customers) prevents unrelated context from bleeding into new conversations. B is unreliable prompt-level mitigation; C and D don't address cross-contamination.

**29. D** — Streaming and surfacing intermediate tool-use signals as they occur keeps the live indicator responsive instead of frozen until the full turn completes. A, B, and C don't address the actual latency-perception problem.

**30. C** — LLM output is inherently non-deterministic; exact-string-match evals are the wrong tool and will fail intermittently even on correct output. A, B, and D misdiagnose the cause.

**31. B** — High-volume, low-complexity classification fits a fast, low-latency tier, with a higher tier reserved for flagged ambiguous cases. A and D overspend by default; C ignores task fit.

**32. D** — Targeted routing of only the flagged ambiguous cases to a higher tier addresses the actual gap without overspending on the high-volume simple path. A, B, and C apply broad, costly fixes to a narrow problem.

**33. D** — Pinning and deliberately testing before upgrading avoids unattributed behavior drift in production. A, B, and C are unhelpful overcorrections unrelated to the actual fix.

**34. A** — Concrete few-shot examples are the most effective lever for consistent structure across languages when prose alone hasn't worked. B, C, and D don't reliably fix structural consistency.

**35. D** — Input and output share one context-window budget, so long input directly constrains available output length and vice versa. A, B, and C misstate this relationship.

**36. D** — Stable policy content first (ideally cacheable) with variable content after both improves consistency and caching. A, B, and C misstate the effect of ordering.

**37. B** — Actual per-request token usage (input/output/cache) attributed per comment gives an accurate cost picture; estimates or unrelated proxies (A, C, D) don't.

**38. D** — Pruning to relevant fields before data enters the prompt removes the bloat at its source. A, B, and C work around the symptom without reducing waste at its origin.

**39. D** — A key-facts overview up front plus clear section markers directly counteracts the tendency to under-attend to the middle of long inputs. A, B, and C don't address the underlying attention pattern.

**40. B** — Verifying key claims against the source comment catches confident-but-wrong verdicts that fluency alone would let through. A, C, and D don't address correctness.

**41. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift in some languages. A, B, and D are workarounds for a problem that can be structurally eliminated.

**42. A** — An isolated subagent scan returning a distilled summary keeps historical bloat out of the main context while still providing relevant repeat-offense context. B and D reintroduce the bloat risk; C discards potentially useful context entirely.

**43. C** — Task simplicity and volume should drive the zero-shot-vs-multi-shot tradeoff; multi-shot earns its cost on tasks needing format or edge-case consistency, which obvious spam may not need. A, B, and D are absolute or false claims.

**44. A** — Versioning prompts like code enables attribution and rollback for quality regressions. B, C, and D are impractical overcorrections that don't provide the actual missing capability.

**45. A** — Extending the eval to check rationale grounding, not just the category label, closes the actual gap the team observed. B, C, and D don't address the missing rationale check.

**46. D** — User-level CLAUDE.md never travels through version control, so a new hire cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

**47. C** — Missing headless/non-interactive mode causes the process to wait for input a CI runner never provides, producing a hang. A, B, and D would typically produce different, more specific failure signatures.

**48. C** — Schema-constrained JSON output is machine-parseable by construction, removing the fragile dependency on prose format stability. A, B, and D are reactive or abandon the structured-parsing requirement.

**49. B** — `context: fork` isolates the command's verbose exploration in a sub-agent context so only a summary returns, directly fixing the described context pollution. A and D scope or restrict differently but don't isolate output; C removes useful functionality.

**50. A** — `allowed-tools` is the enforcement mechanism that makes Bash structurally unavailable during the Skill's execution. B is probabilistic and the violation already happened despite instructions; C mitigates damage rather than preventing it; D is a false claim about commands.

**51. A** — The Explore subagent isolates verbose discovery in a separate context, preserving the main conversation's budget for the fix itself. B floods context directly; C guesses instead of investigating; D doesn't meaningfully share context between windows.

**52. B** — `/compact` summarizes the conversation to free context while preserving key information, the correct mid-session relief valve. A describes behavior that doesn't exist; C frees trivial space while losing standards; D discards findings.

**53. B** — Since the config and triage data were both confirmed correct, the divergence is most likely in how that verified-correct data was subsequently reasoned about — that's where the trace should focus next. A, C, and D re-check already-verified steps or skip diagnosis.

**54. B** — Isolating integration-layer versus model-output failure requires examining the actual trace of what was run and returned, before assuming which side is at fault. A, C, and D guess without diagnosis.

**55. A** — A centrally distributed plugin/shared Skill matches the cross-team reuse and central-maintenance requirement. B, C, and D all fail to provide reusable, centrally maintained access.

**56. C** — Environment-variable expansion keeps the secret out of the version-controlled file while the file itself remains shareable. A is easily reversible obfuscation, not real protection; B and D don't remove the exposed credential from history or ongoing risk.

**57. C** — Least privilege means removing unnecessary capability, not just observing or slowing its misuse. A, B, and D are detective/compensating controls or accept unnecessary risk.

**58. A** — Matching each capability's actual reuse scope — a scoped Skill/command for the one-off QA workflow, a centrally maintained plugin for the widely shared health-check — is the correct architecture. B, C, and D force every capability into one category regardless of its actual reuse profile.

**59. A** — A hook bound to the relevant lifecycle event runs the linter deterministically and can block the action on failure, independent of the model's choices. B and D remain probabilistic prompt-level guidance; C doesn't guarantee anything either.

**60. B** — Constraining the severity field to an explicit enumerated set (ideally via schema-constrained output) removes the ambiguity causing inconsistent labels. A, C, and D don't address the root cause of the inconsistency.

---

*End of Practice Exam 9.*
