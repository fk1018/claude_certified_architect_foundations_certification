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

- A) Whether `flag_risk` has been called at least once in the conversation, since escalation implies the review already reached a structured conclusion.
- B) A hard cap of five tool calls per contract, so the harness force-stops the loop once the limit is hit regardless of context.
- C) Whether the most recent tool call's result validated successfully against its expected schema, treating a clean result as a stop signal.
- D) The `stop_reason` field on the response: continue the loop while it is `"tool_use"`, and stop once it becomes `"end_turn"`.

**Question 2.** After `search_clause_library` returns matching precedent clauses, the harness needs the agent to keep reasoning about the contract with that information available.

Question: What must the harness do? (Select ONE response.)

- A) Append a `tool_result` block referencing the corresponding `tool_use` ID to the conversation and resend the full updated conversation to the model.
- B) Write the clause matches to a shared database with a normalized schema, letting the agent query it separately whenever it needs the data again.
- C) Paste the clause matches into the system prompt so they persist as reusable context for every future contract review, not just this one.
- D) Summarize the matches in a new, structured user-authored message that stands apart from the original tool call.

**Question 3.** Firm policy requires a licensed partner to approve any recommendation to reject a vendor contract outright. The system prompt states this rule clearly, but an audit finds the agent occasionally recommended outright rejection without triggering `request_partner_review`.

Question: What is the most reliable fix? (Select ONE response.)

- A) Repeat the compliance rule near the end of the system prompt as well as the beginning, relying on repeated prompt text rather than a hook to enforce it.
- B) Add several few-shot examples demonstrating the agent correctly escalating rejection recommendations, placed right before the section describing tool schemas.
- C) Lower the temperature so the deterministic parts of policy compliance are followed more consistently across contracts.
- D) Implement a hook that intercepts any final review recommending rejection and blocks delivery unless `request_partner_review` was already called.

**Question 4.** The firm wants every review to begin with a mandatory `search_clause_library` call, with no exceptions, before any other tool runs.

Question: What is the most reliable implementation? (Select ONE response.)

- A) Set `tool_choice: {"type": "tool", "name": "search_clause_library"}` on the first request only, then allow normal tool selection guided by the system prompt afterward.
- B) State plainly in the system prompt, repeated near the top and bottom, that clause-library lookup must always run before any other tool call.
- C) Set `tool_choice: "any"` on the first request so the model is guaranteed to call some tool before responding.
- D) Add several few-shot transcripts that consistently show the clause lookup tool running first, before any other tool call.

**Question 5.** The agent currently has eleven tools, including several rarely used ones (billing lookup, e-signature routing, calendar scheduling) that have nothing to do with clause review. Tool selection has become inconsistent, with the agent occasionally calling the wrong tool for a straightforward review.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` substantially so the agent has more reasoning room before deciding which tool to call.
- B) Add a system-prompt note explicitly ranking all eleven tools by importance and typical use frequency.
- C) Remove or scope out the tools unrelated to contract review from this agent's available tool set.
- D) Keep all eleven tools in place but rename each one with a clearer, more descriptive label.

**Question 6.** `redact_pii` currently returns the plain string `"failed"` whether the input document was missing, the redaction service timed out, or the user lacked permission to redact that document type. The agent responds inconsistently to each case.

Question: What is the best fix? (Select ONE response.)

- A) Add an automatic retry wrapper around every `redact_pii` call, so any failure is retried a fixed number of times before being surfaced to the agent.
- B) Add a system-prompt note asking the agent to infer which failure type occurred from tone and context, distinguishing a missing document from a timeout by inference alone.
- C) Return structured error metadata: a distinct error category, a retryable flag, and a human-readable description, letting the agent validate which errors are worth retrying.
- D) Increase the redaction service's timeout substantially so timeout-driven failures occur less often, even though missing-document and permission failures would remain unaffected.

**Question 7.** When `search_clause_library` finds no precedent matching an unusual clause, it currently returns an error. The agent responds by apologizing for a "system issue" and retrying the identical query.

Question: What should change? (Select ONE response.)

- A) Add a system-prompt note explaining that this particular error usually means no precedent exists yet.
- B) Have the agent automatically call `flag_risk` every time this specific error is returned by the tool.
- C) Return a successful response with an empty result set, reserving errors for genuine access failures.
- D) Add a hook that silently and immediately ends the review whenever this particular error message appears.

**Question 8.** An associate proposes replacing the agent's judgment with a fixed sequence — always run `search_clause_library`, then `flag_risk`, then decide — arguing this makes review behavior predictable across all contract types.

Question: Why is model-driven tool selection the better fit here? (Select ONE response.)

- A) Fixed sequences technically cannot invoke custom tools like `flag_risk`, only built-in Anthropic tools, making firm-specific tooling unusable in a hardcoded pipeline.
- B) Model-driven selection is always cheaper, since it structurally uses fewer reasoning tokens per contract than a fixed sequence that runs every tool needlessly on every contract regardless of content.
- C) The harness technically lacks the capability to execute any fixed, hardcoded tool sequence at all, since it was built only to dispatch whichever call the model itself decides to make.
- D) Contract review is high-ambiguity — which clauses matter and what to check next depends on what earlier tool calls reveal, which a fixed sequence can't adapt to.

**Question 9.** The firm wants to add `request_partner_review` but is deciding whether to give the main review agent that tool directly, or delegate escalation decisions to a separate, narrowly-scoped subagent. Escalating unnecessarily wastes a partner's billable time.

Question: What is the strongest argument for a separate, narrowly-scoped subagent? (Select ONE response.)

- A) A narrowly-scoped subagent given only the escalation tool and explicit criteria reduces unnecessary escalations while the main agent reasons about unrelated clauses.
- B) Subagents execute noticeably faster than tools called directly by the main agent, which meaningfully cuts total per-contract review latency across a busy day of intake.
- C) The main agent's context window is too small to hold the escalation tool's schema alongside everything else, particularly once clause-library results are already occupying most of the space.
- D) Subagents are required by policy whenever a tool call carries a real-world legal or financial consequence, regardless of how narrowly scoped the tool itself is or how rarely it fires.

**Question 10.** During review of a lengthy master services agreement, the agent's context fills with verbose raw clause-library search results, leaving little room to reason about the contract's actual risk profile.

Question: What is the best structural fix? (Select ONE response.)

- A) Read only the first search result returned for every clause-library query, discarding the rest even when the strongest precedent match appears further down the list.
- B) Disable clause-library search entirely and rely on the agent's general legal knowledge instead, since that knowledge already covers most standard vendor clauses.
- C) Increase `max_tokens` substantially so the verbose raw search results have more room to complete without truncation, on the theory that a larger budget resolves the crowding.
- D) Delegate clause-library exploration to a subagent that returns a distilled summary of relevant precedent, keeping the main agent's context focused on risk analysis.

**Question 11.** The agent escalates a contract to a partner, but the partner has no visibility into what the agent checked beforehand — logs show fifteen minutes of tool calls with no accessible summary.

Question: What should the escalation include? (Select ONE response.)

- A) The full raw transcript of every tool call and result from the entire fifteen-minute review session, unedited and in chronological order.
- B) A structured handoff summary covering what clauses were checked, what was found, and a recommended next action for the partner to take.
- C) Just the final risk flag alone, since the partner can re-investigate the contract independently from scratch if the flag seems worth pursuing.
- D) A tone analysis describing how urgent or anxious the contract's language seemed to the agent while it worked through the document.

**Question 12.** The firm is deciding between running the agent through a hosted, Anthropic-managed execution environment versus self-hosting the harness on firm-owned infrastructure, given confidentiality obligations to clients.

Question: What is the core tradeoff to weigh? (Select ONE response.)

- A) Self-hosted agents structurally cannot use custom tools like `redact_pii` without a separate vendor approval process and additional infrastructure sign-off.
- B) Managed agents are inherently less secure than self-hosted ones, regardless of configuration, because the firm no longer controls the underlying hardware.
- C) Operational control (self-hosted) versus operational burden (managed) — tool-calling capability doesn't inherently differ between the two.
- D) Managed agents cannot ever access firm-internal infrastructure under any configuration whatsoever, no matter what networking is arranged.

**Question 13.** A partner asks whether the contract-intake process should be built as a fixed workflow or as an agent.

Question: What is the deciding factor? (Select ONE response.)

- A) Whether the process needs to run in under one minute of wall-clock time per contract, regardless of how many steps it takes.
- B) Whether the firm's engineers happen to prefer Python or TypeScript for the implementation, since either language can call the same underlying API and tools.
- C) Whether the task is well-defined and repeatable versus high-ambiguity, with the right next step depending on intermediate findings.
- D) Whether more than three distinct tools are involved in executing the process, since tool count alone determines the right architecture.

**Question 14.** A proposed "precedent-research subagent" has a vague `AgentDefinition` description: "Helps with clauses." The main agent rarely delegates to it even for contracts that clearly need deep precedent research.

Question: What is the most likely cause and fix? (Select ONE response.)

- A) The main agent's temperature is set too low to ever consider delegating work to a subagent instead of handling it directly.
- B) The description drives delegation choices; rewriting it to state what the subagent does and when to use it will fix the under-delegation.
- C) The subagent needs several additional tools added to its definition before delegation to it will reliably occur.
- D) Subagents cannot be delegated to at all unless they are first registered in a global, firm-wide configuration file shared across every team's agent deployments.

**Question 15.** The firm wants a hard guarantee that `request_partner_review` is never triggered more than once per contract within a single review session, regardless of what the model decides mid-conversation.

Question: What is the correct enforcement mechanism? (Select ONE response.)

- A) A system-prompt instruction stating the one-call limit clearly, relying on the model to remember and honor it rather than wiring an actual hook to enforce it.
- B) A note added to the tool's own description mentioning that the limit exists, in the hope the model reads and respects it on every contract.
- C) Few-shot examples showing an agent correctly stopping after one escalation, included alongside the other tool-usage examples in the system prompt.
- D) A hook that tracks the per-contract call count across the session and blocks any further call to the tool once that limit has already been reached, independent of temperature or other sampling settings.

---

## Scenario B: Real-Time Streaming Support Chat Integration (Questions 16–30)

Northbay Retail runs a customer support chat widget where Claude answers order and shipping questions live while a customer is typing and waiting. The team is integrating streaming responses, tool calls for order lookups, and multi-vendor deployment considerations into the widget's backend.

---

**Question 16.** Customers watch a live typing indicator while Claude composes its answer, and the team wants the first words to appear as quickly as possible rather than waiting for the full response.

Question: What technique best supports this? (Select ONE response.)

- A) Streaming, so the UI can render output incrementally as tokens arrive.
- B) Increasing `max_tokens` substantially, so the full response has more room to finish generating without truncation, which should make it arrive sooner overall.
- C) The Message Batches API, since it is purpose-built for asynchronous chat delivery scenarios like this one.
- D) Polling a status endpoint every 500 milliseconds until the full response becomes ready.

**Question 17.** A nightly job re-summarizes the day's closed support chats for a quality dashboard. No customer is waiting on the result, and none of the summarization steps need a mid-request tool call.

Question: Which API best fits, and why? (Select ONE response.)

- A) The Message Batches API — latency-tolerant, non-blocking, high-volume work processed at meaningfully reduced cost compared to synchronous calls.
- B) The synchronous Messages API, run across many parallel threads so the whole batch of nightly summaries finishes quickly regardless of cost.
- C) The synchronous Messages API with `max_tokens` minimized to cut cost, accepting shorter summaries as the tradeoff.
- D) The synchronous Messages API paired with a smaller model to reduce cost, accepting some quality loss on the summaries.

**Question 18.** The team wants to add an "order-status lookup, verify against shipping carrier, retry if the carrier API times out" loop to the live chat flow, and considers running the whole loop through the Batch API to save cost.

Question: Why won't this work as designed? (Select ONE response.)

- A) The Batch API's context window is too small to hold a full chat transcript alongside the carrier-status data the retry loop would need to inspect.
- B) The Batch API's 24-hour completion window makes any retry logic structurally impossible to implement, since retries would have to wait for the whole batch to resolve first.
- C) The Batch API cannot execute a tool call mid-request and feed the result back to the model within a single request — required for this loop, and incompatible with a live customer waiting anyway.
- D) The Batch API does not support system prompts at all, so all policy guidance, tone rules, and escalation criteria would be silently lost entirely for this loop.

**Question 19.** Every chat turn sends the same 4,500-token support policy and tone guidelines, followed by the specific customer message, which varies per turn.

Question: What optimization most directly reduces both latency and cost across many turns? (Select ONE response.)

- A) Move the 4,500-token policy guidelines into a few-shot example block instead of a plain instruction, on the theory that examples cache identically to plain instructions.
- B) Switch to the smallest available model regardless of the resulting drop in answer quality.
- C) Place the stable policy and tone guidelines first, enable prompt caching, and put the varying customer message last, with no need to increase `max_tokens` for this to work.
- D) Truncate the policy guidelines substantially to reduce the total token count sent on every turn.

**Question 20.** The order-lookup tool's JSON output occasionally fails to parse — about 4% of chat turns produce malformed JSON that breaks the widget's rendering logic.

Question: What is the most reliable fix? (Select ONE response.)

- A) Ask for YAML output instead of JSON in the prompt's formatting instructions, on the assumption that YAML tolerates minor formatting drift better than JSON does.
- B) Define a `submit_order_lookup` tool whose input schema matches the needed structure, and read the data from the structured `tool_use` block instead of parsing free text.
- C) Wrap the parse in a try/catch block and retry the request with "valid JSON only" appended to the prompt whenever the first attempt fails to parse.
- D) Add a JSON-repair library to the rendering pipeline to fix common syntax issues in the free-text output before parsing it.

**Question 21.** Since switching to schema-constrained tool use for order lookups, output always parses successfully, but the widget occasionally displays a shipping estimate that contradicts the actual carrier status returned in the same tool call.

Question: What should the team conclude and do? (Select ONE response.)

- A) Schema compliance guarantees syntax, not semantics — add a validation step that checks the displayed estimate against the carrier status on top of schema compliance.
- B) `max_tokens` is set too low, silently truncating the tool output mid-generation before the estimate resolves correctly against the carrier data.
- C) The schema needs stricter date types applied to the shipping fields, since tightening the types would catch the mismatch between estimate and carrier status.
- D) Abandon schema-constrained tool use entirely and return to free-text order lookups with manual human review of every single response before it reaches a customer.

**Question 22.** Some customers attach a photo of a damaged product, and the pipeline currently sends only an OCR-extracted caption of the image to Claude. Answers about visible damage are poor when the caption is generic or missing detail.

Question: What is the most direct fix? (Select ONE response.)

- A) Switch to a larger, higher-capability model, since bigger models are always meaningfully better at working from vague or generic captions regardless of the underlying data quality.
- B) Increase `max_tokens` so the model has more room to reason harder about the existing caption.
- C) Send the photo itself as an image content block alongside the customer's message, using Claude's native vision input.
- D) Reject photo attachments from the chat flow entirely and ask customers to describe the damage in text instead.

**Question 23.** The widget needs to look up order status, shipping carrier data, and loyalty-point balance concurrently to keep the live chat responsive, rather than fetching each one sequentially.

Question: What must the integration layer support? (Select ONE response.)

- A) A single request with all three lookups concatenated into one prompt, since Claude parallelizes tool calls internally on its own.
- B) The Batch API, since it is the only mechanism that allows issuing more than one request at a time.
- C) Streaming, since only a streamed response supports concurrent backend operations.
- D) Async/concurrent request handling, so multiple API calls can be in flight without blocking on each other.

**Question 24.** Northbay plans to run the same chat integration through both the direct Anthropic API and a third-party cloud marketplace deployment for a separate regional entity.

Question: What should the team expect? (Select ONE response.)

- A) The Messages API contract stays conceptually the same across both the direct API and the marketplace deployment, though authentication, plumbing, and feature-rollout timing can differ.
- B) The marketplace deployment requires a completely different prompting approach and a wholly separate schema design from the direct API, since the two platforms process requests fundamentally differently underneath.
- C) Batch processing is unavailable on any third-party vendor integration whatsoever, so the nightly summarization job would have to move to the direct API entirely.
- D) Response latency is guaranteed to be identical to the millisecond across every vendor, regardless of the underlying infrastructure each one runs on.

**Question 25.** The team enables extended thinking for a complex refund-eligibility chat flow that spans several tool-use turns.

Question: What must the integration layer handle correctly? (Select ONE response.)

- A) Convert thinking output into an additional tool call automatically, so it always feeds back through the same tool-result mechanism as ordinary tool calls.
- B) Treat the thinking content block as distinct from the final answer text, typically preserving it appropriately across the multi-turn tool-use conversation.
- C) Discard thinking content whenever a tool is also invoked during that same turn, since the schema-validated tool result already captures everything relevant.
- D) Ignore thinking content entirely, since it never affects any downstream turn in the conversation and can be discarded without consequence.

**Question 26.** Finance asks for an accurate per-conversation cost breakdown for the chat integration, but the current model only estimates cost from average message length.

Question: What should the improved cost model account for separately? (Select ONE response.)

- A) Only output tokens, since input tokens are effectively free once prompt caching is enabled across every turn of the conversation.
- B) Input tokens, output tokens, and cache read/write tokens, since each is priced differently and each can increase independently as conversations grow.
- C) A flat per-conversation fee applied regardless of actual token usage in that conversation.
- D) Only cache read tokens, since caching dominates the total cost of the integration.

**Question 27.** A new engineer argues the team can skip code review on the chat backend's request-handling code since "the AI part is the risky part."

Question: What is the correct response? (Select ONE response.)

- A) Only the prompt itself needs review; the surrounding request-handling code is low-risk by definition since it merely moves data around.
- B) Code review becomes unnecessary once the evals for the prompt are passing consistently, since passing evals already prove the whole system works.
- C) Review should be skipped for any code that merely calls an external, well-tested API like Claude's, since the vendor's own schema validation already covers correctness end to end.
- D) Standard SDLC practices — code review, testing, version control — still apply to the code around Claude; using an LLM doesn't replace engineering discipline.

**Question 28.** A single long-running chat session stays open across an entire shift, handling unrelated conversations from different customers back-to-back, and agents notice Claude increasingly referencing details from unrelated earlier conversations.

Question: What is the best fix? (Select ONE response.)

- A) Start a fresh session (or `/compact`) at natural task boundaries, such as between different customers, rather than accumulating unrelated context in one long session.
- B) Ask the model to "ignore earlier customers" at the start of each new chat turn, trusting that instruction to override whatever is already sitting in context.
- C) Increase the context window so more history fits without confusion, on the assumption that a bigger window resolves cross-customer bleed on its own.
- D) Reduce the sampling temperature to prevent cross-referencing between unrelated customers, since lower temperature should keep the model focused on the current turn.

**Question 29.** The chat widget shows users a real-time "Claude is checking your order" indicator, but the current backend waits for the entire response — including tool results — before sending anything to the frontend, making the indicator feel frozen.

Question: What is the most direct fix? (Select ONE response.)

- A) Increase `max_tokens` substantially so the full response, including tool results, completes and arrives at the frontend sooner overall.
- B) Switch the order lookup to the Batch API, since batch requests complete faster than synchronous ones and would let the typing indicator resolve immediately once queued.
- C) Reduce the number of tools available to the order-lookup flow, on the theory that fewer tools shortens the model's reasoning time before it responds.
- D) Stream the response and surface intermediate signals (e.g., tool-use events) to the frontend as they occur, rather than waiting for the full turn to complete.

**Question 30.** An engineer proposes an automated eval that asserts the chat response must exactly match a fixed reference string for a sample "where's my order" question, and the eval fails intermittently even though responses look correct on manual review.

Question: What is the most likely issue with the eval design? (Select ONE response.)

- A) The sampling temperature should be increased, since that would give the eval more varied phrasing to potentially land on an exact match.
- B) The model is broken and consistently producing wrong answers to this simple question, and needs to be retrained before the eval can pass reliably.
- C) LLM output is non-deterministic across calls; exact-string-match evals are the wrong tool — evals should tolerate reasonable variation rather than asserting exact text.
- D) The eval needs a longer, more detailed reference string to compare against, since short strings under twenty words statistically produce more false failures in automated comparison pipelines.

---

## Scenario C: Optimizing a Multilingual Content-Moderation Service (Questions 31–45)

Vantora Media runs a content-moderation service that screens user-submitted comments across a dozen languages for policy violations before publication, processing several million comments per day. The team is tuning model selection, prompting, and context handling to keep latency, cost, and moderation consistency within target.

---

**Question 31.** Most submitted comments are short and moderation is a simple binary classification. Latency and per-comment cost matter far more than handling rare, highly ambiguous edge cases perfectly.

Question: Which model tier best fits the default moderation path? (Select ONE response.)

- A) The highest-capability tier available for every comment, to guarantee maximum accuracy even though most submissions are short and simple to classify — deliberately overspending on latency and cost since accuracy matters more than either.
- B) A fast, low-latency tier suited to high-volume/low-complexity classification, reserving a higher tier only for comments flagged as ambiguous.
- C) Whichever tier happens to be cheapest per token at the moment, regardless of task fit.
- D) The same tier used for the company's hardest reasoning tasks, for consistency across every team.

**Question 32.** A small fraction of comments require nuanced judgment (satire versus genuine harassment, coded language, cultural context) where the fast default model produces shallow or inconsistent verdicts.

Question: What is the most targeted fix? (Select ONE response.)

- A) Increase `max_tokens` for every comment across the board, to give the fast model more room to reason regardless of complexity or comment length.
- B) Add more few-shot examples to the fast model's prompt, applied uniformly to every comment regardless of whether that comment is actually ambiguous.
- C) Switch every comment to the highest-capability tier to be safe, abandoning the fast default path entirely even for the bulk of simple, unambiguous comments.
- D) Route only the flagged ambiguous comments to a higher-capability tier or one with extended/adaptive thinking enabled, keeping the fast path for everything else.

**Question 33.** The service currently floats to "whatever model is latest" in production. After a routine model update, moderation verdicts shifted noticeably in borderline cases with no code change.

Question: What should the team do differently? (Select ONE response.)

- A) Disable all prompt caching across the pipeline to prevent behavioral drift between releases.
- B) Roll back permanently to the oldest available model version and never upgrade again.
- C) Do nothing further — behavior drift across model releases is an expected, unavoidable cost of using a hosted model and needs no dedicated evaluation process.
- D) Pin a specific model version in production and deliberately test before upgrading, rather than always floating to latest.

**Question 34.** Moderation verdicts need a consistent structure (category, confidence, rationale) but detailed prose instructions describing that structure haven't produced consistent output across languages.

Question: What technique is most likely to help? (Select ONE response.)

- A) Provide 2–3 few-shot examples demonstrating the exact desired output structure, since temperature alone won't fix structural drift across languages.
- B) Write an even longer, more detailed prose description of the required structure and its fields.
- C) Ask the model to restate the structure back before producing its actual verdict.
- D) Lower the temperature to zero across every moderation request in the pipeline, on the theory that deterministic sampling alone yields a deterministic, schema-consistent output structure.

**Question 35.** A flagged comment thread includes 40+ replies for context. The team wants a maximally detailed rationale for each verdict and considers requesting a very long output to match.

Question: What tradeoff must they account for? (Select ONE response.)

- A) Long outputs are always truncated regardless of the model's stated context-window size, so requesting maximal detail is pointless either way.
- B) None — input and output tokens are budgeted completely independently of each other, so the 40+ replies leave the output allowance untouched.
- C) Output length has no measurable effect on response latency at all, so requesting a maximally detailed rationale costs nothing extra in wait time.
- D) Input and output share the same context-window budget, so a very long input leaves less room for a long output, and vice versa.

**Question 36.** The moderation prompt currently places the specific comment text before the general moderation policy and category definitions in every request.

Question: Why might reordering improve both consistency and cacheability? (Select ONE response.)

- A) Placing instructions last in the prompt always improves the model's attention to them.
- B) Reordering the prompt only affects cost, and never affects output consistency.
- C) Prompt order has no measurable effect on either output consistency or cache-hit rate, since the model reads the entire structured prompt as one undifferentiated block regardless of arrangement.
- D) Stable, role-defining policy content belongs first so it forms a consistent, cacheable prefix; the varying comment text should come after.

**Question 37.** Finance wants an exact per-comment cost figure for the moderation service, but the team currently estimates cost only from average comment length.

Question: What should be instrumented instead? (Select ONE response.)

- A) A flat cost assumption based on average comment character count alone, validated once against a small sample and then reused indefinitely without further checking.
- B) Actual token usage per request — input, output, and cache — attributed per comment, so cost tracking scales correctly as usage increases, rather than an estimate from average length.
- C) Wall-clock latency per comment, used as a rough proxy for actual cost since slower requests are assumed to cost more.
- D) The number of API calls made only, regardless of the token count consumed within each individual call.

**Question 38.** Comments arrive with full raw platform metadata (device info, session IDs, every historical edit) that bloats the prompt with mostly-irrelevant data, slowing the pipeline.

Question: What is the best fix? (Select ONE response.)

- A) Switch to a model with a larger context window so the metadata bloat matters proportionally less.
- B) Summarize the raw metadata with a second Claude call before it enters the moderation prompt, adding a normalization step that reshapes the dump into a consistent schema first.
- C) Increase `max_tokens` substantially to accommodate the extra metadata volume in each request.
- D) Prune the metadata to the relevant fields before it enters the prompt, essentially normalizing the input rather than passing raw dumps.

**Question 39.** For long comment threads, moderators notice verdicts consistently miss policy violations buried in the middle of the thread while catching violations in the opening and closing comments reliably.

Question: What is the most effective mitigation? (Select ONE response.)

- A) Add an instruction telling the model to "pay equal attention to the whole thread," trusting that phrasing alone corrects the attention pattern.
- B) Switch to a model with an even larger context window to fit more of the thread, on the assumption that a bigger window alone corrects where attention concentrates.
- C) Alphabetize the comments before sending the thread to the model for moderation, so ordering no longer reflects the original conversation flow.
- D) Put a brief thread overview at the start of the input and organize the detailed comments under clear section markers, mitigating the tendency to attend most to the beginning and end of long inputs.

**Question 40.** A verdict confidently states that a comment "contains a direct threat," but on manual review the comment contains no such language.

Question: What practice would most help catch this class of error before it reaches enforcement? (Select ONE response.)

- A) Shorten the verdict's rationale so there's less room for factual errors to appear in the explanation text.
- B) Apply defensive parsing and skepticism toward confident output — verify key claims against the source comment rather than accepting fluency as correctness.
- C) Increase the model's sampling temperature so verdicts sound noticeably less confident and assertive overall.
- D) Trust confident, fluent-sounding output as sufficient evidence of correctness by default, since a verdict that cites a specific policy category has already been implicitly validated by that citation.

**Question 41.** Detailed prose asking the model to "always output valid structured JSON with these exact fields" still produces occasional free-text preambles before the JSON in a few languages.

Question: What is the more reliable approach? (Select ONE response.)

- A) Post-process every response to strip any free text appearing before the first `{` character, treating the stripped prefix as noise regardless of what it actually said.
- B) Repeat the JSON-formatting instruction more emphatically specifically for the affected languages.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose.
- D) Increase `max_tokens` so there's enough room for both the preamble and the JSON body.

**Question 42.** The team wants to add an exploratory step that scans a user's full comment history for repeat-offense context before moderating the current comment, but worries the exploration will bloat the main context with mostly-irrelevant historical detail.

Question: What is the best structural approach? (Select ONE response.)

- A) Have a subagent perform the historical scan in an isolated context and return only a distilled, relevant summary to the main moderation step.
- B) Load the user's entire comment history directly into the main prompt every single time a comment is moderated, treating the full raw history as necessary structured context for every verdict.
- C) Skip historical context entirely to avoid any risk of context bloat from the scan, forgoing repeat-offense signal altogether.
- D) Increase the context window so the full comment history always fits without trimming, no matter how long a user's history has grown.

**Question 43.** For the simplest, highest-volume comment category (obvious spam links), the team is deciding between a zero-shot prompt and a multi-shot prompt with several examples.

Question: What consideration should drive the choice? (Select ONE response.)

- A) The choice has no effect on either cost or latency for this task, since token count is dominated by the comment text rather than the prompt template.
- B) Zero-shot is required whenever latency matters at all, regardless of task complexity, since any added examples necessarily slow the response down.
- C) For a simple, well-understood, high-volume task, zero-shot may be sufficient and cheaper; multi-shot earns its extra token cost on tasks needing specific formatting or edge-case consistency.
- D) Multi-shot is always strictly better than zero-shot, regardless of task simplicity, because more examples can only ever improve consistency.

**Question 44.** The moderation prompt has been informally edited by several engineers over time with no record of what changed or why, making it hard to diagnose a recent uptick in false positives.

Question: What practice would have prevented this? (Select ONE response.)

- A) Treating prompts as versioned artifacts, similar to code, so changes are tracked and regressions can be attributed and rolled back.
- B) Locking the prompt entirely so that no one is ever allowed to change it again, without wiring any hook or other enforcement layer to actually verify compliance.
- C) Only allowing one single designated engineer to ever read or touch the prompt, funneling every change through that one person.
- D) Rewriting the prompt completely from scratch on a fixed quarterly schedule, regardless of whether anything has actually gone wrong.

**Question 45.** An automated eval suite for the moderation service checks only whether the verdict category matches a reference label, and passes even when the rationale field is nonsensical or references the wrong comment.

Question: What is the most useful improvement to the eval suite? (Select ONE response.)

- A) Extend the eval to also check rationale quality and grounding (e.g., does it reference content actually present in the comment) as coverage increases, not just the final category label.
- B) Remove the rationale field from verdicts entirely so there's nothing extra left for the eval suite to check or the moderators to read.
- C) Increase the number of reference labels used, but only for the existing category-match check, leaving the rationale field unchecked as before.
- D) Run the existing category-only eval more frequently, on a shorter schedule, to catch category-label regressions sooner, on the assumption that frequency alone compensates for what the eval doesn't check.

---

## Scenario D: Claude Code Skills and Commands for a QA Team (Questions 46–60)

Cascade Software's QA team has adopted Claude Code for writing test plans, triaging flaky tests, and drafting bug reports, and has built a set of team-specific Skills and slash commands (`/triage-flaky`, `/draft-bug-report`, `/gen-test-plan`). You support this team's configuration, CI usage, and troubleshooting.

---

**Question 46.** A new QA hire clones the team's test-automation repository, but Claude Code doesn't apply the team's established bug-report conventions for them, even though a teammate's machine applies them correctly.

Question: What is the most likely cause? (Select ONE response.)

- A) CLAUDE.md requires an explicit `@import` from the project root in order to take effect at all, otherwise its structured conventions are silently ignored by the session.
- B) The new hire needs to run `/memory` first in order to activate any memory files before conventions take effect.
- C) The conventions file exceeded an internal size limit and was silently truncated on load without any warning in the session.
- D) The conventions live only in `~/.claude/CLAUDE.md` on the teammate's machine — user-level config that isn't tracked by version control.

**Question 47.** A nightly CI job invokes Claude Code to triage newly flaky tests and consistently hangs until timeout, with no visible error in the logs.

Question: What is the most likely cause? (Select ONE response.)

- A) The repository's CLAUDE.md file is malformed in a way that stalls the session before it can produce any output at all.
- B) The nightly flaky-test list is simply too large for Claude Code to process in one pass, causing it to hang while scanning the full list.
- C) The job is missing `-p`/`--print` (headless mode), so the process is waiting for interactive input the CI runner never provides.
- D) The CI runner lacks sufficient permission to call the Claude API from its network, so every request silently fails without a visible error.

**Question 48.** A downstream dashboard parses `/triage-flaky` output with regex to file tickets automatically, and the parser breaks whenever output formatting drifts slightly between runs.

Question: What is the robust fix? (Select ONE response.)

- A) Add a stronger prompt instruction telling the model never to deviate from the format.
- B) Harden the parsing regex with more permissive fallback patterns for near-miss formats, validating each captured field against expected types before filing the ticket.
- C) Run with `--output-format json` and a defined schema for the triage findings, producing machine-parseable, easily validated output.
- D) Post the entire raw output as a single ticket comment instead of parsing it.

**Question 49.** The `/gen-test-plan` command prints thousands of lines of exploratory code-reading output while building context on the feature under test, and QA engineers report Claude's answers about their actual follow-up questions get noticeably worse right after running it.

Question: What frontmatter change fixes this? (Select ONE response.)

- A) `argument-hint`, so engineers see guidance up front about scoping the exploration more narrowly themselves before the command runs its structured code-reading pass.
- B) `context: fork`, so the command's verbose exploration runs in an isolated sub-agent context and only a summary returns to the main conversation.
- C) Removing the command from the team's shared command set entirely, since no other fix would keep exploratory output out of the main conversation.
- D) `allowed-tools`, restricting the command to strictly read-only operations, without changing where the exploration output lands in context.

**Question 50.** An internal `/draft-bug-report` Skill is meant only to create a formatted markdown file from a template, but an audit finds a session where it also ran shell commands that modified unrelated test fixtures.

Question: What is the correct guardrail? (Select ONE response.)

- A) Configure `allowed-tools` in the Skill's frontmatter to permit only file-creation operations, making Bash unavailable during execution.
- B) Add a warning in the Skill's instructions telling Claude never to run shell commands, instead of configuring a hook to block that behavior outright.
- C) Require engineers to commit their work before running any Skill, as a safety net against unwanted changes the Skill might make.
- D) Convert the Skill into a slash command, since commands structurally cannot run tools the way Skills can.

**Question 51.** A QA engineer needs to understand how a flaky integration test's setup fixtures interact across a large, unfamiliar test suite before proposing a fix, and worries that reading dozens of files will exhaust context before the fix itself is written.

Question: What is the best approach? (Select ONE response.)

- A) Use the Explore subagent for the discovery phase so verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- B) Read every file in the test suite in one single pass to be maximally thorough, since a complete, validated picture of every fixture is worth the context it consumes.
- C) Skip exploration entirely and infer fixture behavior from file names alone, without opening the files to confirm anything.
- D) Split the investigation across two separate terminal windows running in parallel, each reading a different half of the test suite.

**Question 52.** Mid-session, context is nearly full of verbose fixture-exploration output, but the engineer still needs to implement the fix in the same session and wants to preserve key findings.

Question: What should they do? (Select ONE response.)

- A) Continue working as normal; Claude automatically discards irrelevant context on its own.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md file temporarily to free up context space.
- D) Start a brand-new session and rely on memory of what was learned earlier, since the earlier findings were already validated and don't need to persist in context verbatim.

**Question 53.** A multi-step Claude Code task that reads a test-config file, calls `/triage-flaky`'s underlying analysis, and writes a bug report produces a wrong root-cause conclusion. Trace logs show the config was read correctly and the triage analysis returned valid data.

Question: Where should debugging focus next? (Select ONE response.)

- A) Nothing — a wrong conclusion reached from correct inputs means the task should simply be re-run as-is, on the assumption the same error is unlikely to repeat.
- B) The step between receiving the valid triage data and producing the final conclusion — since inputs were confirmed correct, the divergence is most likely in how the model reasoned about or transformed that data afterward.
- C) The network connection used to read the test-config file, since that's the earliest step in the pipeline and network issues are historically the least visible, hardest-to-validate failure class.
- D) Re-read the test-config file again from disk, since that's the earliest step in the pipeline and re-checking the earliest step first is generally good practice.

**Question 54.** A test-runner integration fails intermittently, and the QA team can't tell whether the failure is in their integration code (bad flags, wrong exit-code parsing) or in something the model did.

Question: What is the correct first diagnostic step? (Select ONE response.)

- A) Assume it's a model problem from the outset and rewrite the prompt accordingly, since intermittent failures usually point at the language model rather than the surrounding glue code.
- B) Isolate whether the failure occurred at the integration layer (the actual command invocation and its output) versus in the model's output, by examining the trace of exactly what was run and returned.
- C) Switch to a different model entirely to see whether the failure persists, treating a change in symptoms as proof of where the fault lies.
- D) Restart the CI runner and simply try the same job again, without capturing what actually ran or what the model actually returned this time.

**Question 55.** The QA team wants `/gen-test-plan` to be usable and maintainable across every team at Cascade Software, not just QA, and updated centrally without each team needing to copy files around.

Question: What is the best approach? (Select ONE response.)

- A) Package it as a plugin/shared Skill distributed centrally, rather than a per-repository command each team copies and maintains independently.
- B) Have each team paste the command's full instructions into their own local CLAUDE.md file, then keep that structured copy synchronized manually whenever the format changes.
- C) Ask each engineer to manually re-type the plan format from memory whenever it's needed, since the format is simple enough to remember.
- D) Hard-code the test-plan logic separately into each team's own custom internal script, maintained independently by whoever wrote it.

**Question 56.** The team's `.claude/settings.json`, committed to the repository, currently has a bug-tracker API token hardcoded directly in a hook script referenced by the config.

Question: What is the correct fix? (Select ONE response.)

- A) Base64-encode the hardcoded token before committing the hook script to the repository.
- B) Rotate the token weekly on a fixed, automated schedule instead of ever removing it from the file, treating rotation as an equivalent, validated substitute for actually eliminating the exposure.
- C) Move the token to environment-variable expansion so the secret isn't committed to version control.
- D) Move the entire settings file to a private repository instead of the shared one.

**Question 57.** An audit finds that `/triage-flaky`'s `allowed-tools` configuration grants it broader shell access (including the ability to delete test artifacts) than the triage workflow actually requires.

Question: What is the correct remediation, consistent with least-privilege principles? (Select ONE response.)

- A) Leave access as-is for now, since no actual misuse has been observed yet and the broad grant hasn't caused a visible incident.
- B) Add a confirmation prompt before any deletion the tool would otherwise perform silently, while leaving the rest of the broad grant untouched.
- C) Scope `allowed-tools` down to only the operations the triage workflow actually requires, removing unnecessary broad capabilities rather than just monitoring them.
- D) Add structured logging around the broad access so any misuse can be reviewed and validated after the fact, without changing what the workflow is actually permitted to do.

**Question 58.** The QA team is choosing how to expose a one-off, team-specific bug-report formatting workflow used only by QA, versus a widely-reused test-environment-health-check capability needed by every engineering team at Cascade.

Question: How should each be built? (Select ONE response.)

- A) The one-off bug-report workflow as a Skill or command scoped to the QA team; the widely-reused health-check capability as a centrally maintained plugin/shared tool available to every consuming team.
- B) Both as one-off Skills, since Skills are structurally always team-specific by design and can never be shared centrally.
- C) Both as centrally maintained plugins, since that is the correct choice for any capability regardless of how narrowly one team actually uses it.
- D) Both as ad hoc shell scripts, since that approach requires the least initial setup effort even for a capability every team depends on.

**Question 59.** The QA lead wants Claude Code sessions to automatically run the project's linter and block a commit if it fails, without relying on Claude choosing to run the linter on its own.

Question: What is the correct mechanism? (Select ONE response.)

- A) A hook bound to the relevant lifecycle event (e.g., before commit) that runs the linter deterministically and blocks the action on failure, unaffected by temperature or other sampling settings.
- B) A CLAUDE.md instruction telling Claude to always lint before committing any change, treating that written policy as an effectively deterministic gate on its own.
- C) A few-shot example showing a past session running the linter before committing, included among the other examples in the system prompt.
- D) A Skill description that mentions linting is recommended before finalizing a commit, left up to the model's judgment on any given run.

**Question 60.** A `/draft-bug-report` command frequently produces reports with an inconsistent severity field — sometimes "High," sometimes "P1," sometimes "critical" — because the command's prompt only says to "assign an appropriate severity."

Question: What is the most reliable fix? (Select ONE response.)

- A) Lower the temperature used for the `/draft-bug-report` command across every run, on the theory that a more deterministic sampling process alone will produce a consistent, schema-like severity label.
- B) Constrain the severity field with an explicit enumerated set of allowed values (e.g., via schema-constrained output or an explicit list in the instructions), rather than leaving it to free-text judgment that's hard to validate.
- C) Ask engineers to manually correct the severity field after every generation, treating the correction step as an acceptable permanent fix.
- D) Remove the severity field from bug reports entirely going forward, since a missing field can't display an inconsistent value.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-A, 5-C, 6-C, 7-C, 8-D, 9-A, 10-D, 11-B, 12-C, 13-C, 14-B, 15-D, 16-A, 17-A, 18-C, 19-C, 20-B, 21-A, 22-C, 23-D, 24-A, 25-B, 26-B, 27-D, 28-A, 29-D, 30-C, 31-B, 32-D, 33-D, 34-A, 35-D, 36-D, 37-B, 38-D, 39-D, 40-B, 41-C, 42-A, 43-C, 44-A, 45-A, 46-D, 47-C, 48-C, 49-B, 50-A, 51-A, 52-B, 53-B, 54-B, 55-A, 56-C, 57-C, 58-A, 59-A, 60-B

---

**1. D** — The loop must key off `stop_reason`: continue while it is `"tool_use"`, stop at `"end_turn"`. Whether a specific tool was called (A), a fixed call cap (B), and treating a clean result as a stop signal (C) are all unreliable or secondary signals compared to the authoritative field.

**2. A** — Tool results must be appended as a `tool_result` block referencing the `tool_use` ID, then the full conversation resent. Writing to a separate database (B) hides the result from the model; the system prompt (C) is the wrong place for turn-level data; a plain user message (D) breaks the expected tool-result linkage.

**3. D** — A compliance-critical rule needs deterministic enforcement via a hook that blocks delivery outright. Repeating the rule (A), few-shot examples (B), and lowering temperature (C) all remain probabilistic prompt compliance, which is exactly what's failing.

**4. A** — Forcing tool choice on a specific tool guarantees it runs first; later turns proceed normally. A system-prompt statement (B) and `tool_choice: "any"` (C) don't guarantee which tool runs; few-shot examples (D) remain probabilistic.

**5. C** — Removing tools unrelated to the agent's core role directly reduces the candidate set the model must reason over. More reasoning tokens (A), a ranking note (B), and renaming (D) don't remove the actual capability bloat causing misselection.

**6. C** — Structured error metadata (category, retryable flag, description) lets the agent respond appropriately to each distinct failure. Blanket retry (A) wastes calls on non-retryable failures; asking the model to guess (B) is worse than the tool reporting it; a longer timeout (D) reduces frequency without fixing missing information.

**7. C** — "No precedent found" is a valid empty result, not a failure — return success with an empty set. A prompt note (A) papers over the underlying conflation; auto-flagging (B) invents an unwarranted extra step; silently ending review (D) hides real signal.

**8. D** — High-ambiguity review where the next step depends on earlier findings is the core case for model-driven tool selection. The other options make unsupported technical or cost claims about fixed sequences.

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

**46. D** — User-level CLAUDE.md isn't tracked by version control, so a new hire cloning the repo won't see it; team conventions must live in a committed project-level file. A, B, and C misdescribe how CLAUDE.md loading actually works.

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
