# Exam Guide Gap Pack Flashcards — Developer: Foundations

## Workflow vs. Agent

Q: When should you choose a fixed workflow over an agent?

A: When the task is well-defined and repeatable with a predictable sequence of steps. Choose an agent when the right steps vary by case and depend on intermediate results.

## Manager/Supervisor Hierarchy

Q: Why delegate to specialized subagents instead of using one generalist agent?

A: Scoping each subagent's tools and context to its role improves reliability; a single agent holding every tool and every responsibility degrades tool-selection reliability and clarity of purpose.

## Claude Agent SDK

A: What does the Claude Agent SDK handle for you that a hand-rolled loop would require you to build yourself?

A: The tool-use loop mechanics — checking `stop_reason`, executing requested tools, returning results, and continuing until `end_turn` — without you re-implementing that control flow.

## Hooks vs. Prompts

Q: When must you use a hook instead of a system prompt instruction?

A: When a rule must be enforced deterministically, every time, regardless of what the model decides — e.g., blocking a destructive tool call above a dollar threshold.

## Messages API Statelessness

Q: Is the Claude Messages API stateful across turns?

A: No. Each request is independent; your application resends the full relevant message history each turn to maintain conversational continuity.

## Prompt Caching Order

Q: Why does content order matter for prompt caching?

A: Only a shared prefix can be cached. Stable content (system prompt, reference docs) must come first and dynamic content last so the stable prefix is reused across requests.

## Batch API Limitation

Q: Why can't an iterative "generate, run, fix, repeat" loop use the Message Batches API?

A: The Batch API does not support multi-turn tool calling within a request — it cannot pause mid-request to execute a tool and feed results back, which an iterative loop requires.

## Batch API Fit

Q: What kind of workload is the Batch API designed for?

A: High-volume, latency-tolerant, non-blocking work (e.g., an overnight report over 10,000 documents) — not anything the user is waiting on in real time.

## Schema Nullability

Q: Why make a structured-output field nullable instead of required, if the underlying data may be absent?

A: A required field pressures the model to fabricate a value when the real answer is "not present." Nullable fields let the model correctly report absence.

## Enum Escape Hatches

Q: What should you add to an enum field for real-world, ambiguous input?

A: An `"other"` value with a detail string, or an `"unclear"` value — otherwise the model is forced into an incorrect category for cases the enum didn't anticipate.

## CLAUDE.md Hierarchy

Q: Why won't a new teammate's Claude Code sessions follow your team's shared conventions if those conventions only live in `~/.claude/CLAUDE.md`?

A: `~/.claude/CLAUDE.md` is user-level and personal — it's never shared through version control. Team standards must live in a project-level CLAUDE.md committed to the repo.

## Headless Mode in CI

Q: Why does a Claude Code CI job hang indefinitely?

A: It's missing `-p`/`--print` (headless/non-interactive mode) — without it the process waits for interactive input that a CI runner never provides.

## Machine-Parseable CI Output

Q: What should a CI pipeline that programmatically consumes Claude Code's findings request?

A: `--output-format json` (with `--json-schema` where supported) for schema-conforming, machine-parseable output instead of parsing prose.

## Skills Frontmatter: context: fork

Q: What does `context: fork` in a Skill's frontmatter do, and why use it?

A: Runs the skill in an isolated sub-agent context so its verbose or exploratory output doesn't pollute the main conversation — only a summary returns.

## Skills Frontmatter: allowed-tools

Q: How do you prevent a skill meant only to create files from ever running shell commands?

A: Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, making Bash unavailable during that skill's execution.

## Tool Description Quality

Q: Two tools have near-identical names and descriptions, and the model misroutes between them ~30% of the time. What's the most effective first fix?

A: Rewrite each tool's description to state its distinct purpose, expected inputs/outputs, and when to use it versus the other — description quality is the primary routing signal, not a secondary detail.

## Structured Tool Errors

Q: Why does returning the same generic `"Operation failed"` message for every tool failure hurt an agent's ability to recover?

A: The agent can't distinguish retryable transient failures from permanent business-rule failures without structured metadata (`errorCategory`, `isRetryable`, description) — so it either retries forever or gives up on things that would have succeeded.

## MCP Server Reusability

Q: Why build an MCP server instead of hard-coding an internal API's logic into each application's system prompt?

A: An MCP server exposes reusable tools that multiple Claude applications can share and that can be maintained independently of any one app — hard-coded logic in a prompt is neither reusable nor independently maintainable.

## MCP Resources vs. Tools

Q: What's the difference between an MCP resource and an MCP tool?

A: Resources expose content/catalogs an agent can read for visibility (e.g., what documents exist) without an action; tools perform actions (e.g., fetch, mutate, call an external system).

## Built-in vs. Custom vs. Skill vs. MCP

Q: You need reusable inventory-lookup capability shared across five different Claude applications, maintained by a separate team. Which approach fits best?

A: An MCP server — it's the option built for cross-application reuse and independent maintenance, unlike a custom tool (single-app) or a Skill (workflow-oriented, not typically a shared backend integration).

## Prompt Injection Definition

Q: What is prompt injection, in one sentence?

A: Untrusted content (a web page, a user upload) containing instructions that the model might follow as though they came from a trusted source.

## Prompt Injection Mitigation

Q: What's the most effective mitigation for prompt injection from retrieved web content?

A: Treat retrieved content as untrusted input, keep it separate from trusted instructions, and gate sensitive actions behind guardrails/hooks so injected instructions can't trigger them — not asking the model nicely to ignore injected text.

## Least Privilege for Agents

Q: A support agent has refund and account-deletion tools it never actually needs for its role. What's the least-privilege fix?

A: Remove those tools from the agent's configuration entirely, rather than just logging their use or adding a confirmation step — eliminate the unnecessary capability, don't just monitor it.

## Secrets in MCP Config

Q: How should credentials be referenced in an `.mcp.json` file shared via version control?

A: Via environment-variable expansion (e.g., `${API_TOKEN}`), never hardcoded directly in the committed file.

## Token Budget Tradeoff

Q: What's the practical consequence of the context window being shared between input and output?

A: A very long input leaves less room for a long output (and vice versa) — both draw from the same finite budget.

## Model Tier Selection

Q: What's the general tradeoff across Opus, Sonnet, and Haiku?

A: Roughly capability/cost/latency tiers — Opus for the hardest reasoning tasks, Haiku for high-volume/low-latency simple tasks, Sonnet as the balanced default for most production workloads.

## Model Version Pinning

Q: Why pin a specific model version in a production pipeline instead of always using "latest"?

A: Behavior can change across model releases even within the same capability tier; pinning gives you reproducibility and a deliberate, tested upgrade path instead of silent behavior drift.

## Few-Shot for Format Consistency

Q: Detailed prose instructions haven't fixed inconsistent output formatting. What technique is most likely to help?

A: Few-shot examples demonstrating the exact desired output format — concrete examples are more effective than additional prose at pinning down format and edge-case handling.

## Schema-Valid but Wrong

Q: A tool-use response always parses successfully against its schema, but some field values are semantically wrong (e.g., a line number pointing at the wrong line). What does this tell you?

A: Strict schemas eliminate syntax errors, not semantic errors — you need separate semantic validation layered on top of schema compliance.

## Defensive Parsing

Q: Why shouldn't a confident-sounding model response be treated as evidence of correctness?

A: Fluency and confidence are not correlated with accuracy — claims that matter should be verified against ground truth, not accepted because the phrasing sounds certain.

## Streaming Use Case

Q: When does streaming responses matter most?

A: In interactive UIs where perceived latency (time-to-first-token) affects user experience — non-interactive/batch workloads generally don't need it.

## Vision Input Handling

Q: How are images provided to Claude via the API?

A: As content blocks alongside text within the same message — there is no separate vision-specific endpoint.

## Async Programming Need

Q: Why does building production Claude applications typically require async programming?

A: To handle streaming responses and to run multiple tool calls or subagent tasks concurrently without blocking the main execution thread.

## Session Hygiene

Q: Why might you deliberately start a fresh session (or run `/compact`) rather than continuing one long-running session?

A: To avoid one session's context accumulating unrelated tasks and degrading focus/relevance for the current task — natural task boundaries are a good time to reset.

## Client-Side vs. Server-Side Tools

Q: What's the distinction between a client-side and a server-side tool?

A: Client-side tools execute in your application; server-side tools execute wherever the model itself runs. Approval patterns for sensitive actions apply to either, based on the action's risk, not its execution location.

## Trace Analysis for Debugging

Q: When a multi-step agent run produces a wrong final result, what's the recommended first debugging step?

A: Read the actual trace of tool calls, tool results, and model turns to localize exactly where the run diverged from the intended path, rather than guessing from the final output alone.

## Cost Modeling Components

Q: What three token categories should cost modeling account for separately?

A: Input tokens, output tokens, and cache read/write tokens — they are priced differently, so lumping them together produces an inaccurate cost model.

## AAA/CIA Framework

Q: What does the AAA/CIA framework help you reason about in application security?

A: Authentication, authorization, confidentiality, privacy, and integrity — the standard lenses for identifying what could go wrong and who should be permitted to do what.
