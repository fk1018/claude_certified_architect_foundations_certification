# Production-Grade Prompting, Agents & Tool-use Flashcards

## Diagnosing Prompt Failures

Q: A prompt returns correct content but in an inconsistent shape (sometimes a sentence, sometimes a label). Which technique is missing?

A: An output constraint. The prompt never specified the form, field names, or stopping point of the response.

Domain: D6

Example: A classifier returns "Billing", "billing", and "This looks like a billing issue" across different runs; adding "Return only the label, one of BILLING/TECHNICAL/ESCALATION, no other text" fixes the shape.

## Diagnosing Prompt Failures

Q: A prompt's output is correct on tested inputs but drifts in scope and tone deeper into a long conversation. Which technique is missing?

A: A system prompt, or a more specific one — the behavioral contract was too vague to hold across turns.

Domain: D6

Example: A support bot starts answering unrelated product questions by turn 10; a tighter system prompt re-anchors role and scope for every turn.

## Diagnosing Prompt Failures

Q: Claude understands the task correctly but invents a structure you never asked for. What's missing?

A: Few-shot examples — Claude cannot infer an exact structure from a description alone.

Domain: D6

Example: Asking for "a summary with key points" produces a different layout every run; one `<sample_input>`/`<ideal_output>` pair locks the exact structure.

## Diagnosing Prompt Failures

Q: What is the rule for fixing a failing prompt?

A: Name the specific failure, add the one technique that matches it, and re-run — do not reword or add unrelated text.

Domain: D6

Example: If three re-prompts in a row haven't fixed the output, stop adding words and diagnose which of the four techniques (system prompt, XML tags, few-shot, output constraint) is actually missing.

## Six-Pass Anti-Pattern

Q: In the module's six-pass classification example, what two distinct failures occurred across the revision passes?

A: A diagnostic failure (pass 4: added descriptive text instead of a constraint) and an engineering failure (pass 5: the verbose prompt induced verbose, slow output with no accuracy gain).

Domain: D6

Example: After pass 5, outputs ballooned past 2,000 characters per call and latency rose, even though the classification accuracy hadn't improved since pass 4.

## Structured Outputs

Q: How do structured outputs (`output_config.format` with `type: json_schema`) guarantee valid JSON, technically?

A: Constrained decoding — the API only allows tokens that keep the output valid against the schema as each token is generated, so a schema-violating response cannot be produced.

Domain: D6

Example: Even if Claude "wants" to add a preamble sentence before the JSON, the constrained decoder simply won't allow tokens that break the schema.

## Structured Outputs

Q: What does setting `strict: true` on a tool definition guarantee?

A: The arguments Claude sends to that tool are validated against the input schema before your application code runs.

Domain: D8

Example: In an agentic loop, `strict: true` on a `charge_card` tool prevents a malformed `amount` field from ever reaching the payment-processing function.

## Structured Outputs Costs

Q: Name two costs of enabling structured outputs in production.

A: The first request on a new schema is slower (grammar compilation, though compiled grammars are cached 24 hours from last use), and input token count rises because the API injects a system prompt describing the expected format.

Domain: D5

Example: A workload that changes its JSON schema on every call pays the compilation cost repeatedly instead of benefiting from the 24-hour cache.

## Structured Outputs Costs

Q: Does a schema-constrained response guarantee downstream success? Why or why not?

A: No — a refusal (`stop_reason: refusal`) or truncation (`stop_reason: max_tokens`) can still produce output that doesn't fully parse, so code must still check `stop_reason` rather than assuming every response parses.

Domain: D4

Example: A request hitting `max_tokens` mid-JSON-object still returns `stop_reason: max_tokens`, and naive code that assumes schema compliance will crash trying to parse the truncated fragment.

## Structured Outputs Limitation

Q: Can JSON outputs (schema-constrained responses) be combined with message prefilling?

A: No — JSON outputs and prefilling the assistant message are incompatible; pick whichever pattern fits the task.

Domain: D8

## Extended Thinking

Q: How is extended thinking effort controlled on current models, and what happened to the older `budget_tokens` parameter?

A: Effort is adaptive and tuned via an effort setting, not a fixed token budget; `budget_tokens` is deprecated and returns a 400 error on newest model generations.

Domain: D5

## Extended Thinking Carry-Back Rule

Q: What must happen to a thinking block (including a redacted one) before the next turn of a tool-use loop?

A: It must be sent back to the API completely unchanged — each block carries a signature, and editing, summarizing, or dropping it causes a signature mismatch that the API rejects.

Domain: D2

Example: A developer strips thinking blocks out of history to save context before the next tool call; the very next request fails signature validation.

## Extended Thinking Usage

Q: When should extended thinking be left off?

A: For mechanical/lookup tasks like classification, format conversion, or field extraction — a bare prompt with an output constraint is cheaper and equally accurate.

Domain: D5

Example: Classifying 50,000 support tickets into 3 labels overnight is a mechanical task; leaving thinking off is correct.

## Extended Thinking Usage

Q: When should extended thinking be enabled and budgeted for the planning step specifically?

A: For agentic loops with multi-tool planning or multi-step reasoning where each step depends on the previous one.

Domain: D1

Example: Planning a multi-step refactor where each step's approach depends on the outcome of the previous step calls for enabling thinking and budgeting effort for that planning step.

## Tool-Use Loop Mechanics

Q: Does Claude execute tools itself?

A: No — Claude emits a `tool_use` block naming the tool and arguments; your application code must execute it and return a `tool_result`; the loop is not automatic.

Domain: D8

## Message Block Types

Q: What must be preserved when an assistant turn contains both a `text` block and a `tool_use` block, and history is later appended?

A: The full content array, including the text block — dropping it while keeping only the tool_use block corrupts context.

Domain: D8

## Message Block Types

Q: Why are `tool_result` blocks always sent in the `user` role, even though your application (not the human user) generated them?

A: Role marks the sender in the conversation structure, not the content's author — tool results are conventionally attributed to the user turn.

Domain: D8

## Tool Pairing Invariant

Q: What happens if a `tool_use` block's ID doesn't exactly match the `tool_use_id` on the following `tool_result` block?

A: The API rejects the request with a validation error (e.g., "tool_result block references unknown tool_use_id") — every tool_use must be answered by a tool_result with the exact matching ID in the immediately following user turn.

Domain: D8

Example: A session shows `tool_use id="toolu_01"` in the assistant turn but `tool_result tool_use_id="toolu_02"` in the next user turn; the fix is correcting the ID, not adding a required field or changing a description.

## Tool Schema Anatomy

Q: What are the three parts of a tool schema, and what must the `description` part cover?

A: `name`, `description`, and `input_schema`. The description must state both when to use the tool AND when NOT to use it — vague descriptions like "use this to find information" cause wrong-tool selection.

Domain: D8

## Tool Schema Design

Q: Why should you avoid marking every plausible field as `required` in a tool's input schema?

A: Over-marking fields as required forces Claude to fabricate values it doesn't actually have; true-optional fields should be left out of the required array with defaults given in the function signature.

Domain: D8

## Tool Schema Design

Q: What is the recommended description length and content for a tool, and what happens at each extreme?

A: About 3-4 sentences covering what it does, when to reach for it, what it returns, and valid input examples; too short causes guessing, too long buries the actual trigger conditions.

Domain: D8

## Parallel vs Sequential Tool Calls

Q: When should tool calls run sequentially versus in parallel, and how do you force sequential execution?

A: Run sequentially when one call's output feeds the next call's input; models default to parallel tool_use blocks when calls are independent, and `disable_parallel_tool_use` forces exactly one call per turn.

Domain: D8

## The Wrong-Tool Failure Pattern

Q: Two tools both have descriptions that read like "use this to find information." What's the fix, and what's the fallback if that doesn't work?

A: Add an explicit exclusion condition to EACH tool's description (e.g., "do not call this if the answer is already in context" and its mirror). If descriptions still can't be cleanly separated, merge the tools into one with a `type` parameter.

Domain: D8

Example: A developer spends a morning debugging why Claude keeps calling `search_docs` when the answer is already in context, only to find both `search_docs` and `get_context_summary` had nearly identical descriptions.

## MCP Context Cost

Q: Does connecting an MCP server only add context cost when its tools are actually used?

A: No — every connected MCP server adds its tool definitions to the context window even when unused in the current turn, so servers should be connected deliberately.

Domain: D8

## MCP Connector Configuration

Q: What do the `defer_loading` and `enabled` fields do in an API MCP Connector's `mcp_toolset` configuration, and what beta header does the connector require?

A: `defer_loading` delays loading a tool's definition until the model actually needs it (reduces upfront context cost); `enabled` turns an individual tool on or off; the connector requires the `mcp-client-2025-11-20` beta header.

Domain: D8

## MCP Transports

Q: What transport do local MCP servers use, and what do remote MCP servers use, per this course?

A: Local servers use stdio (subprocess); remote servers use Streamable HTTP (POST client-to-server, with optional GET-based SSE for server-initiated messages) — the older SSE-only transport is deprecated.

Domain: D8

## MCP vs Manual Tools

Q: When should you write a tool manually instead of connecting an MCP server?

A: When no existing server covers the use case, or when you need precise control over description quality — MCP tool descriptions from a third-party server may not meet your routing-precision needs.

Domain: D8

## Streaming Event Sequence

Q: List the six streaming event types in order, and state what each one signals.

A: `message_start` (new message begins, empty content), `content_block_start` (a new block opens at an index), `content_block_delta` (an incremental fragment), `content_block_stop` (the block at that index is complete), `message_delta` (top-level stop_reason and final usage), `message_stop` (the stream is complete).

Domain: D2

## Streaming Discipline

Q: Why can't you parse a tool_use block's input as JSON right after a `content_block_delta` event?

A: The input JSON string is incomplete until the block closes — it is only parseable once `content_block_stop` fires for that block.

Domain: D2

## Streaming Discipline

Q: At what point should a streamed assistant turn be appended to conversation history?

A: Only after `message_stop`, with every block in the turn fully assembled and closed — never based on the stream's read loop simply ending.

Domain: D2

## Stream Interruption Handling

Q: What should your code do if a stream is interrupted (dropped connection, timeout) before `message_stop` arrives?

A: Discard the partial assistant turn entirely — do not save it to history — and retry from the last complete turn.

Domain: D4

Example: In the module's Watch Out postmortem, a handler appended an assistant turn whenever its read loop ended (not gated on `message_stop`); a mid-stream network blip left a truncated tool_use block in history, which only produced a validation error on the NEXT (retry) request, misleading the team into debugging the schema instead of the stream handler.

## Model Tiers

Q: Name the four model tiers referenced in this course and their general fit.

A: Haiku (speed/cost efficiency within its capability envelope), Sonnet (balanced default for most production workloads), Opus (demanding work above Sonnet's envelope), Fable (Anthropic's most capable model, for complex reasoning/advanced coding/research synthesis/sophisticated agentic workflows).

Domain: D5

## Model Tier Selection

Q: What should trigger moving from Sonnet up to Opus or Fable, or down to Haiku?

A: Eval results, not assumption — move up only when an eval set shows the current tier misses the quality bar, move down only when an eval shows the regression is acceptable.

Domain: D5

## Context Window Mechanics

Q: What happens if a request already exceeds the context window versus if it fits but hits the ceiling mid-generation?

A: A request that already exceeds the window is rejected before generation; a request that fits but hits the ceiling mid-generation returns the output generated so far with `stop_reason: model_context_window_exceeded`. Neither path silently truncates old content.

Domain: D5

## Dev-vs-Prod Context Gap

Q: Why can a session that stays comfortably within budget in testing hit the context ceiling much earlier in production?

A: Production tool outputs commonly run 3-5x longer than development fixtures, and production sessions run more turns, so the window fills much earlier (e.g., turn 8 instead of turn 50).

Domain: D5

Example: A sales-receipt agent built under a 40,000-token budget cap worked fine on 20-receipt dev fixtures (~800 tokens/tool result) but hit the cap at turn 8 in production once tool outputs grew to ~3,200 tokens/call with supporting documents attached.

## Context Budget Strategies

Q: What are the four strategies for staying within a context budget, and what does each one lose?

A: Pruning (jump back and drop everything after a point — loses work done after the rewind), Compaction (summarize history — loses details not captured in the summary), Clearing (start fresh — loses all session context), Subagent Handoffs (isolate a subtask and keep only its summary — loses visibility into how the subagent reached its conclusion).

Domain: D1

## Compaction Summarizer Quality

Q: Why does an under-specified compaction summarizer prompt ("summarize the conversation so far") cause failures in later turns?

A: It drops task-critical state (files modified, decisions at branch points, errors and their resolutions) that the agent needs going forward — one of the most common sources of multi-session agent failures.

Domain: D1

Example: "Summarize the conversation so far" loses which files were edited, while "summarize, preserving all file paths modified, all decisions made, and any errors encountered and their resolutions" produces a usable summary.

## Prompt Caching

Q: How do you mark a cache breakpoint, and how many are allowed per request?

A: Set a `cache_control` field of type `ephemeral` on the last block you want cached; up to 4 cache breakpoints are allowed per request.

Domain: D5

## Prompt Caching

Q: What are the best candidates for prompt caching?

A: A long system prompt, a large tool definition set, or a repeatedly-queried reference document — anything that forms a stable prefix reused across requests.

Domain: D5

## Token Counting

Q: What does the `count_tokens` endpoint do, and how should it be used in production?

A: It accepts the same request body as a Messages call and returns a token count without running inference — use it to gate requests before they would error, based on real tool-output sizes rather than assumptions.

Domain: D5

## RAG Failure Points

Q: Name the three failure points of a RAG pipeline described in this course.

A: Chunking (too small loses context, too large dilutes the match), Embedding match (semantic similarity can outrank an exact-term match), and Assembly (retrieved chunks must land in the prompt in the expected structure or the model answers from memory instead).

Domain: D6

## Fetch-Once Index vs Agentic Search

Q: When is a pre-built retrieval index preferable to iterative agentic search, and vice versa?

A: An index is preferable for a stable corpus with simple lookups (inspectable, testable, but costs infrastructure to build/store/sync/secure); iterative agentic search is preferable for a changing corpus or multi-step questions (no staleness/infra cost, but more tokens/time per query).

Domain: D1

## Workflow vs Agent

Q: What is the core decision criterion for choosing a workflow over an agent?

A: Choose a workflow when you can enumerate the exact steps in code and every execution follows the same sequence with well-constrained inputs; choose an agent when you can specify the goal and available tools but not the exact path, and inputs vary unpredictably.

Domain: D1

## Agent Wiring Paths

Q: Compare the three agent wiring paths on who runs the loop and what you own.

A: Raw Messages API loop — your code runs and owns everything (execution, retries, exit conditions). Agent SDK — the SDK runs the loop in your process; you still execute the tools. Claude Managed Agents — Anthropic runs the loop and the sandbox; your app sends events and consumes a stream.

Domain: D1

## Managed Agents Compliance Constraint

Q: Why can't Claude Managed Agents be used for HIPAA/PHI or Zero Data Retention workloads?

A: Managed Agents sessions are stateful and stored server-side by Anthropic, which currently makes them ineligible for Zero Data Retention or a HIPAA Business Associate Agreement — those workloads need the Agent SDK or a raw loop on a covered configuration instead.

Domain: D7

## Agent Loop Wiring Steps

Q: What are the four steps to wire an agent loop, regardless of which wiring path you choose?

A: Register tools, set a task-scoped system prompt, handle the tool-use loop (execute every call, return every result before the next assistant turn), and define explicit exit conditions.

Domain: D1

## HITL Insertion Points

Q: Name the three types of HITL insertion points and their relative risk.

A: Before a destructive tool call (high risk, irreversible), after a planning step (medium risk — a wrong plan can still produce a wrong outcome even with correct execution), and on unexpected output like an error flag or out-of-bounds value (variable risk — catches failures retry logic won't resolve).

Domain: D7

## HITL Design Question

Q: What question should you ask about every tool capable of an irreversible action?

A: "What is the worst possible outcome if this step runs without a human check?"

Domain: D7

Example: In the module's Watch Out, a file-editing agent's `validate_config` tool checked only schema range, not whether a downstream system depended on the old value — it corrected a "misconfigured" rate limit that the customer's app actually relied on, and no checkpoint existed between "validation passed" and "write committed to the customer environment."

## Over-Tooling vs Under-Tooling

Q: Which is the more common production problem — too many tools or too few — and why?

A: Over-tooling is more common — teams register "just in case" tools, and selection quality degrades as the overlapping-description surface grows. Start minimal and add only when a specific gap is confirmed.

Domain: D8

## Regulated Data Delivery Routes

Q: Why doesn't a HIPAA Business Associate Agreement automatically cover every Anthropic surface?

A: A BAA covers only a specific configuration (e.g., a dedicated HIPAA-enabled org via direct API, or Bedrock/Vertex on a covered account) — it does not cover Console, Workbench, beta features, or consumer plans.

Domain: D7

## Regulated Data Delivery Routes

Q: What are the three authorized routes for FedRAMP/government work mentioned in this course?

A: Claude for Government (FedRAMP High via Palantir Federal Cloud Service), Claude via Amazon Bedrock GovCloud (FedRAMP High, DoD IL4/5), and Claude via Vertex AI Assured Workloads (FedRAMP authorized) — Claude Enterprise on AWS Marketplace is explicitly NOT FedRAMP authorized.

Domain: D7

## Agent Memory Scopes

Q: Compare in-context memory and external storage on cost and persistence.

A: In-context memory has zero retrieval overhead but inflates every API call's token cost as the conversation grows and vanishes when the session clears. External storage adds retrieval latency and read/write engineering but survives across sessions, users, and agent instances.

Domain: D1

## Agent Memory Scopes

Q: When is a stateless (no persistent memory) agent the right choice?

A: For task-execution agents that finish and close, or fully independent pipelines where each job doesn't need to know about any other job.

Domain: D1

Example: A document formatter that receives a file, transforms it, returns output, and terminates — each job is fully independent, so it needs no persistent memory.

## Memory Scope as a Design Decision

Q: Why does the module insist memory scope should be decided at design time rather than fixed later?

A: The default trap — storing full history in the messages array — works at first, then token cost scales with every turn until the agent hits a hard limit; refactoring to external storage later is mechanically simple but happens under production pressure with a deadline already in motion.

Domain: D1

Example: A support-escalation agent's in-context history exceeded 40,000 tokens before a single tool call by session four, because state accumulated across many short production sessions instead of the one long continuous session used in testing.

## Skills vs CLAUDE.md vs In-Context

Q: How does a Skill's loading behavior differ from CLAUDE.md's and from plain in-context instructions?

A: A Skill (SKILL.md) loads only when its name/description matches the current task — low context cost. CLAUDE.md loads into every session unconditionally in Claude Code CLI (or per `settingSources` in the Agent SDK) — fixed overhead. In-context instructions persist only within the current session and grow with it.

Domain: D3

## Subagent Inheritance

Q: Do subagents automatically inherit Skills and permission context from their parent session?

A: They inherit permission context (permission scope is not reset at delegation) but do NOT automatically inherit Skills or conversation history — a needed Skill must be explicitly listed in the subagent's configuration.

Domain: D1

## `settingSources` Configuration

Q: What does the Agent SDK's `settingSources` configuration control, and what's the guidance for setting it?

A: Whether filesystem-based features like CLAUDE.md and skills load in the Agent SDK; never rely on a default — set it explicitly (e.g., `["user", "project", "local"]` to match Claude Code CLI behavior, or `[]` to run fully isolated).

Domain: D2

## Image Token Cost

Q: What is the formula for an image's visual token cost, and roughly how many tokens does a 1000x1000px image cost?

A: ceil(width/28) x ceil(height/28) visual tokens (one token per 28x28-pixel patch); a 1000x1000px image costs roughly 1,296 visual tokens.

Domain: D5

## Sending Images and PDFs

Q: What block type is used for sending a PDF (as opposed to an image), and what fields does it require?

A: The block type is `document` (not `image`); the source structure mirrors images (base64/URL/Files API `file_id`), with no required `name` field and only optional `title` and `context` fields.

Domain: D2

## Sending Images

Q: When is the Files API the right choice for sending an image, versus inline base64?

A: The Files API is best when the same asset appears across multiple requests or turns (upload once, reference by `file_id`, near-zero payload thereafter); inline base64 is best for a genuine one-off image where an upload step adds complexity without payoff.

Domain: D2

## Message Batches API

Q: What are the size/count limits and the latency tradeoff of the Message Batches API?

A: Up to 100,000 requests or 256 MB per batch, whichever comes first; per-token cost is lower than synchronous, but latency is non-deterministic and can take up to 24 hours (often much faster).

Domain: D5

## Message Batches API

Q: How do you match batch results back to their original inputs?

A: Use the `custom_id` field set on each request — results return in arbitrary order, not submission order.

Domain: D2

## Batching Anti-Pattern

Q: Why doesn't looping over the synchronous API in smaller chunks count as "batching"?

A: The API still sees one request per item back-to-back, hitting the same rate limits as the unchunked version — the Message Batches API is a different submission model, not a smaller batch size.

Domain: D5

Example: A developer's nightly classification job kept hitting rate limits after 3 nights despite "splitting into smaller chunks," because each chunk was still individual synchronous calls in a loop.

## Multimodal Prompting Craft

Q: Why does a bare "describe this image" prompt underperform, and what should you add?

A: Images carry ambiguity text doesn't (overlapping objects, depth/spatial relationships, partial occlusion), so the prompt should explicitly instruct how to handle each ambiguity type, e.g. "if objects overlap, describe each separately and note the overlap."

Domain: D6

## Exam Trap

Q: Why can't tool-selection degradation after a fixed number of turns be assumed to be a schema problem?

A: Accumulated tool outputs can crowd out the system prompt and routing instructions in the context window well before an obvious error appears — check context window fill first, since the symptom (wrong tool selections) looks identical to a schema defect.

Domain: D4
