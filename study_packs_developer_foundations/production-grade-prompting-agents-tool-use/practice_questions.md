# Production-Grade Prompting, Agents & Tool-use Practice Questions

## Question 1

Scenario: A developer's classification prompt has gone through five revision passes. Each pass added more explanatory text, but outputs are now over 2,000 characters per call, latency has increased, and accuracy on ambiguous tickets has not improved since pass four.

Question: What is the correct diagnosis and fix?

A. The prompt needs a sixth paragraph clarifying the ambiguous cases in more detail.

B. Replace the accumulated prose with an output constraint specifying the exact label set plus two few-shot examples.

C. Switch to a larger model tier so it can better follow the long instructions.

D. Enable extended thinking so Claude can reason through the ambiguous cases before answering.

Correct answer: B

Explanation: The six-pass pattern in this module shows that adding descriptive text without adding a structural technique (here, an output constraint and few-shot examples) makes prompts longer without fixing the failure. Replacing the accumulated prose with a tight output constraint and two examples resolves both the diagnostic failure (pass 4) and the engineering failure (pass 5, verbose output).

Distractors:

- A: More descriptive paragraphs is exactly what already failed across passes 3-5; it isn't a missing technique.
- C: A larger model does not fix a structural prompt defect and adds unnecessary cost.
- D: Extended thinking is for multi-step reasoning tasks, not for fixing an under-constrained output format; it would not stop label casing or format drift.

## Question 2

Scenario: An engineer sets `output_config.format` with `type: json_schema` on a data-extraction endpoint and assumes every response can now be parsed without a try/except block.

Question: What is the risk in this assumption?

A. Structured outputs are purely advisory and Claude may still return prose.

B. A response can still arrive with `stop_reason: refusal` or `stop_reason: max_tokens`, producing output that doesn't fully match the schema, so the code must still check `stop_reason`.

C. Structured outputs only work with the Batches API, not synchronous calls.

D. JSON schema constraints only apply to tool arguments, not to the final response text.

Correct answer: B

Explanation: The module is explicit that a guaranteed schema is not a guaranteed success — a safety refusal or a max_tokens truncation can still produce output that doesn't parse cleanly, so defensive `stop_reason` checks remain necessary even with structured outputs enabled.

Distractors:

- A: Structured outputs are enforced via constrained decoding at generation time, not merely advisory.
- C: Structured outputs apply to synchronous JSON responses (`output_config.format`) as taught in this module; the Batches API is a separate, unrelated mechanism.
- D: `output_config.format`/`json_schema` constrains the final response; `strict: true` on a tool definition constrains tool arguments — these are the two situations the module names, and the question is about the response case.

## Question 3

Scenario: A tool-use agent is mid-conversation and about to make a second tool call. The developer's code, to save context, strips out the `thinking` block from the previous assistant turn before sending the next request.

Question: What will happen, and why?

A. Nothing — thinking blocks are optional decoration and can be safely dropped.

B. The request will succeed, but reasoning quality on the next turn will silently degrade.

C. The API will reject the request because the thinking block's signature can no longer be verified once it has been altered or removed.

D. The API will automatically regenerate the missing thinking block from context.

Correct answer: C

Explanation: The module's carry-back rule states every thinking block, including redacted ones, must be returned to the API completely unchanged on the next tool-use turn. Each block carries a signature; removing or editing it causes a signature mismatch and the API rejects the request. The correct fix for context bloat is a context-engineering technique, not stripping thinking blocks.

Distractors:

- A: Thinking blocks are structurally required in a tool-use loop when they were returned by the API — this is not optional.
- B: The failure is a hard rejection at the API level, not a silent quality regression.
- D: The API does not regenerate dropped blocks; it validates and rejects.

## Question 4

Scenario: Two tools, `search_knowledge_base` and `get_cached_result`, both have descriptions that begin "Use this to find information for the user." Claude frequently calls `search_knowledge_base` even when the answer is already available in the current session context, and the input schemas for the two tools are already different.

Question: What should the engineer change first?

A. Add a `required` field constraint to `search_knowledge_base`'s input schema to make it harder to call.

B. Add explicit exclusion conditions to each tool's description (e.g., "do not call this if the answer is already in context" / "only use this if X was already retrieved for the same query").

C. Rename `get_cached_result` to something more memorable.

D. Enable `strict: true` on both tools so the arguments are validated more tightly.

Correct answer: B

Explanation: Claude routes primarily on tool name and description; two tools with nearly identical descriptions are indistinguishable regardless of differing input schemas. The fix demonstrated in this module's Watch Out is adding an explicit exclusion condition to each tool's description so their appropriate contexts don't overlap.

Distractors:

- A: A required-field change affects argument validation, not tool selection, and does not address the root description ambiguity.
- C: A rename alone does not add the disambiguating "when to use / when not to use" information Claude routes on.
- D: `strict: true` validates arguments against a schema after a tool is already selected; it has no effect on which tool gets selected in the first place.

## Question 5

Scenario: A team connects three MCP servers to their agent "just in case," even though the agent's current tasks only use tools from one of them.

Question: What is the production cost of this decision, according to the module?

A. None — MCP servers only add cost when their tools are actually invoked.

B. Every connected MCP server adds its tool definitions to the context window even when unused in the current turn, so unused connections increase token cost on every request.

C. Extra MCP servers automatically trigger additional billing on Anthropic's side regardless of usage.

D. MCP servers must be re-authenticated on every request, adding latency but not token cost.

Correct answer: B

Explanation: The module explicitly warns that connected MCP servers add their tool definitions to the context window whether or not those tools are used in the current turn — the guidance is to register only actively-used servers, and to use `defer_loading`/`enabled` and allowlisting to control loading cost when broader connectivity is needed.

Distractors:

- A: This is the opposite of what the module teaches — unused tool definitions still occupy context.
- C: The module does not describe a separate per-server billing mechanism; the cost described is token/context cost.
- D: The module does not describe per-request re-authentication as the cost mechanism; the stated cost is context window consumption from tool definitions.

## Question 6

Scenario: A team's stream-handling code accumulates `content_block_delta` events into a buffer and appends the assembled assistant turn to conversation history as soon as the network read loop exits, without checking whether `message_stop` was received.

Question: What production failure mode does this create?

A. The agent will run slower because it re-parses every delta event twice.

B. A dropped connection mid-stream can leave a truncated tool_use block committed to history, which then causes a validation error on a LATER retry request rather than on the original stream.

C. The agent will silently retry the same tool call indefinitely.

D. Claude will refuse all subsequent requests in the session.

Correct answer: B

Explanation: This is the exact postmortem in the module's streaming Watch Out: gating history commits on the read loop ending (instead of on `message_stop`) let a network blip commit a corrupted, truncated tool_use block into history. The validation error only surfaced on the retry request, which is what made the team spend an afternoon debugging the wrong layer (the schema) before finding the real, upstream cause.

Distractors:

- A: The described bug is a correctness/data-integrity issue, not a performance issue from double-parsing.
- C: The module's postmortem describes a validation error on retry, not an infinite retry loop.
- D: There is no described mechanism for Claude to blanket-refuse a session because of a malformed prior turn; the API rejects the specific malformed request.

## Question 7

Scenario: A sales-receipt processing agent was built and tested with a 40,000-token context budget cap, using 20-receipt development fixtures averaging about 800 tokens per tool result. In production, receipts include supporting documents, and average tool output grows to about 3,200 tokens per call. Tool-selection quality appears to degrade after several turns.

Question: What is the most likely root cause and correct first diagnostic step?

A. The tool schemas are ambiguous and need better descriptions; rewrite them first.

B. The accumulated tool outputs are crowding out the system prompt and routing instructions well before the failure appears as wrong tool selections — check context window fill before touching the schema.

C. The model tier is too weak for this workload; upgrade from Sonnet to Opus.

D. Extended thinking should be enabled so Claude can reason more carefully about which tool to pick despite the added context.

Correct answer: B

Explanation: This mirrors the module's own worked example: at ~3,200 tokens/call, eight turns of tool output alone consumes about 25,600 tokens, and combined with the system prompt this crowds out routing instructions well before an obvious failure. The symptom looks like a tool-selection/schema problem but the root cause is context budget exhaustion — the module's explicit guidance is to check window fill first.

Distractors:

- A: The schema was correct in earlier turns of the same session; rewriting descriptions does not address token accumulation crowding out instructions.
- C: A stronger model tier does not fix a context-budget problem — the instructions themselves are being crowded out regardless of model capability.
- D: Enabling extended thinking adds more tokens to an already-crowded context and does not address the root cause.

## Question 8

Scenario: An engineering team needs to decide between building a workflow or an agent for a document-processing task. The steps required can be fully enumerated in code, inputs are well-constrained to a known set of document types, and every execution should follow the same sequence with clear guardrails at each step.

Question: Which pattern fits, and why?

A. An agent, because agents are always more capable regardless of task shape.

B. A workflow, because the exact steps can be enumerated, inputs are well-constrained, and step-level guardrails matter — the path doesn't need to be discovered at runtime.

C. A Claude Managed Agent, because it removes the need to design the control flow at all.

D. A subagent handoff pattern, because it isolates context automatically.

Correct answer: B

Explanation: The module's decision table is explicit: choose a workflow when you can enumerate the exact steps in code, error cost is real and step-level guardrails matter, inputs are well-constrained, and every execution follows the same sequence. An agent is for when only the goal and available tools can be specified, not the exact path.

Distractors:

- A: The module explicitly frames agents as carrying more coordination overhead and failure surface — not a default "more capable" choice regardless of task shape.
- C: Managed Agents is a wiring path for the agent pattern; it does not eliminate the workflow-vs-agent decision itself, and this task shape favors a workflow.
- D: Subagent handoffs are a context-engineering technique for isolating subtasks within an agent session, not a standalone answer to a workflow-vs-agent decision.

## Question 9

Scenario: A file-editing agent has `read_file`, `write_file`, and `validate_config` tools, and loops up to 10 times adjusting a config until `validate_config` passes. In a customer environment, it correctly flags an out-of-range parameter, writes a fix, `validate_config` passes on the first try, and the loop terminates after one iteration exactly as designed. Minutes later, the customer's application starts failing because the corrected parameter was a rate limit their app relied on at its old value.

Question: What was actually missing from this agent's design?

A. A larger iteration cap, since 10 iterations wasn't enough to catch the issue.

B. A HITL checkpoint between "proposed change validated" and "write committed to the customer environment," since `validate_config` only checked schema range, not downstream dependency impact.

C. A more detailed description on the `write_file` tool.

D. Extended thinking enabled during the validation step.

Correct answer: B

Explanation: The module's Watch Out on this exact scenario concludes that the missing piece was a checkpoint before an irreversible write executes — `validate_config` passing (a narrow schema-range check) is not the same as the change being safe for dependent production systems. The guiding question the module poses is "what is the worst outcome if this step runs without a human check," and the fix is a HITL checkpoint before the write, not more automation.

Distractors:

- A: The loop terminated in exactly one iteration as designed; the iteration cap was never the constraint that mattered here.
- C: A better `write_file` description would improve tool selection, not prevent a validated-but-unsafe write from being committed.
- D: Extended thinking affects reasoning depth before an answer, not whether an irreversible action gets a human checkpoint before executing.

## Question 10

Scenario: A support-escalation agent stores the full conversation history in-context and was tested with one long 10-15 turn development session, where it performed fine. In production, users have many shorter sessions, but state accumulates across sessions. By the fourth production session, over 40,000 tokens of injected history exist before a single tool call is made.

Question: What is the correct fix and lesson?

A. Increase `max_tokens` so the agent can generate longer responses despite the crowded context.

B. Move the accumulated state to external storage, injecting only the relevant subset at session start, because in-context memory does not survive session boundaries efficiently when state must persist across many short sessions.

C. Enable extended thinking so Claude can better prioritize which parts of the long history matter.

D. Switch the agent to Claude Managed Agents so Anthropic manages session state.

Correct answer: B

Explanation: This is the module's memory Watch Out: in-context memory was chosen without measuring how state would accumulate across many short production sessions (versus the one long dev session used in testing). The fix was moving state to external storage and injecting only the relevant subset — matching memory scope to session shape at design time, not defaulting to the easiest-to-write option.

Distractors:

- A: `max_tokens` controls output length per response; it does not address an already-crowded input context from accumulated history.
- C: Extended thinking does not solve a memory-architecture mismatch; it adds more token cost on top of an already bloated context.
- D: Managed Agents changes who runs the loop and sandbox, but its sessions are still server-side and don't automatically solve an application's own memory-scope design choice, and switching wiring paths does not itself fix the underlying scope decision (in-context vs. external) that caused the failure.

## Question 11

Scenario: A team needs to classify 5,000 customer feedback responses overnight, with no real-time latency requirement. A developer proposes looping over the synchronous Messages API, splitting the list into smaller chunks of 50 to "avoid rate limits."

Question: Will this approach solve the rate-limit problem, and what should be done instead?

A. Yes — chunking into smaller groups reduces the concurrent request count enough to stay under rate limits.

B. No — chunking still produces the same number of individual synchronous API calls and hits the same rate limits; the Message Batches API should be used instead, since it is a different asynchronous submission model, not a smaller batch size.

C. No — the fix is to enable prompt caching on the classification prompt instead of changing the submission method.

D. Yes, as long as each chunk is submitted with the Files API instead of inline text.

Correct answer: B

Explanation: The module's batching Watch Out makes this exact point: looping the synchronous API, even in smaller chunks, is still one request per item and hits the same rate limits as before — chunking is not batching. The Message Batches API accepts up to 100,000 requests or 256 MB per batch as a single asynchronous submission and is the correct tool for high-volume, offline workloads like this.

Distractors:

- A: Chunking reduces batch size but not total request count over time; the same number of individual API calls still occur.
- C: Prompt caching reduces cost on a repeated stable prefix but does not change the request-count/rate-limit dynamics of looping the synchronous API.
- D: The Files API addresses payload size for reused assets like images; it is unrelated to the rate-limit problem caused by per-item synchronous calls.

## Question 12

Scenario: A pipeline sends a 4000x3000px product photo to Claude in every request of a high-volume nightly batch job, encoding it as inline base64 each time even though the same photo is reused across all 5,000 requests in the batch.

Question: What is the main inefficiency in this design, and what should change?

A. Nothing needs to change — inline base64 is required for all batch workloads.

B. The image should be uploaded once via the Files API and referenced by `file_id`, since inline base64 repeats the full encoded payload on every request, multiplying cost for a reused asset.

C. The image should be converted to a PDF `document` block to reduce its token cost.

D. The image should be sent via a URL reference instead, since URL references never count against token budgets.

Correct answer: B

Explanation: The module is explicit that inline base64 is best for one-off images and that costs multiply when the same image is sent repeatedly; the Files API is designed exactly for this case — upload once, reference by `file_id`, with near-zero payload overhead on every subsequent request.

Distractors:

- A: Inline base64 is one of several sending methods and is specifically discouraged for a reused asset due to repeated payload cost.
- C: Switching block type from `image` to `document` does not change the underlying visual-token cost formula, which is based on pixel dimensions regardless of block type.
- D: URL references avoid payload transfer but still incur visual-token cost when Claude processes the fetched image, and they add a reachability/stability dependency the module warns about — they are not automatically cost-free or the best fit here versus the Files API for a reused asset.
