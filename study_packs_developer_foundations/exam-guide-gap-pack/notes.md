# Exam Guide Gap Pack — Developer: Foundations (CCDV-F)

- Source URL: `exam_guide_developer_foundations.txt` (official exam guide v1.0, effective July 2026)
- Study pack: `study_packs_developer_foundations/exam-guide-gap-pack/`
- Purpose: primary study pack for CCDV-F, built directly from the exam guide's content outline. Weighted toward Domain 2 (Applications and Integration, 33.1% — the single largest domain) and Domain 5 (Model Selection and Optimization, 16.8%), which together are half the exam.

## Exam Domain Mapping

| Domain | Weight | Covered Ideas |
|---|---|---|
| D1: Agents and Workflows | 14.7% | Workflow vs. agent decision, manager/supervisor hierarchies, Claude Agent SDK, custom agent loops, hooks, agentic frameworks |
| D2: Applications and Integration | 33.1% | Requirements/SDLC, Claude API mechanics (messages, tools, streaming, caching, batch), software engineering foundations, cross-interface app design, CLAUDE.md/settings.json config |
| D3: Claude Code | 3.1% | Rules, Skills, Commands, Agents, Agent Memory, session management, slash commands, headless/auto-mode |
| D4: Eval, Testing, and Debugging | 2.6% | Error type identification, recovery strategy, trace analysis, integration-layer vs. model-output isolation |
| D5: Model Selection and Optimization | 16.8% | Tokens/context/sampling, model tiers, thinking modes, cost/token/caching management |
| D6: Prompt and Context Engineering | 11.0% | Context window management, drift/bloat prevention, prompt engineering, output handling |
| D7: Security and Safety | 8.1% | Prompt injection, guardrails, hooks, identity/secrets/key management |
| D8: Tools and MCPs | 10.6% | Tool implementation, MCP server development, built-in vs. custom vs. Skills vs. MCP tradeoffs |

## Key Concepts

### D1 — Agent Architecture (4.5%)

- Workflow vs. agent: choose a **workflow** (fixed, predetermined sequence of LLM calls and tools) when the task is well-defined and repeatable; choose an **agent** (model decides its own steps) when the path varies by case and intermediate results change what's needed next.
- Manager/supervisor hierarchies: a coordinator agent delegates to specialized subagents rather than one agent trying to do everything — improves reliability by scoping each agent's tools and context to its role.
- Subagents improve task execution by isolating verbose or exploratory work (so it doesn't pollute the main context) and by allowing specialization (a narrow, well-scoped agent outperforms one generalist agent with every tool).

### D1 — Agent Construction with Claude (5.3%)

- Claude Agent SDK: the supported path for building production agent loops — handles the tool-use loop (send message → check `stop_reason` → execute tools → return results → repeat until `end_turn`) without hand-rolling it.
- Custom agent loops/harnesses: hand-rolled alternatives to the SDK; valid when you need control the SDK doesn't expose, but you own the loop's correctness (stop conditions, retry logic, tool dispatch).
- Managed deployment models: self-hosted (you run the harness and infrastructure) vs. Anthropic-hosted managed agents (Anthropic runs the sandboxed execution environment) — the tradeoff is operational control vs. operational burden.
- Hooks: deterministic, code-level interception points (e.g., `PreToolUse`, `PostToolUse`) for actions that must happen every time, not just when the model remembers to follow a prompt instruction.

### D1 — Agent Patterns and Frameworks (4.9%)

- Tool-use loop: the core agentic pattern — the model requests a tool, your code executes it, you return the result, the model continues.
- Memory patterns: scratchpad files or structured state exports let an agent (or a resumed session) recover context across long tasks or crashes without replaying the entire history.
- Context-window management in agents: prune or summarize tool outputs before they accumulate; isolate exploratory work in subagents so only a summary returns to the main context.
- Agentic frameworks (Strands, LangGraph, PydanticAI): third-party abstractions over the tool-use loop, graph-based orchestration, or structured-output validation — know what problem each class of framework solves, not implementation trivia.

### D2 — Claude API Mechanics (6.8%)

- Messages API: the core request/response primitive — `messages`, `system`, `tools`, `max_tokens`. Multi-turn conversations are stateless from the API's perspective; your application resends the full message history each turn.
- Streaming: use for interactive UIs where perceived latency (time-to-first-token) matters; adds complexity (partial JSON, incremental tool-use blocks) that non-interactive/batch workloads don't need.
- Vision: image inputs are content blocks alongside text in the same message; no separate vision endpoint.
- Extended thinking: a distinct content block type that must be handled (and typically preserved) separately from the final answer text in multi-turn tool-use conversations.
- Prompt caching: mark stable, repeated prefixes (system prompt, long reference documents) as cacheable to cut both cost and latency on repeated requests — order matters: static content first, dynamic content last, since only the shared prefix is cacheable.
- Batch API: asynchronous, high-volume, latency-tolerant (up to 24h window) processing at reduced cost. Cannot execute multi-turn tool calling within a single request — no mid-request pause to run a tool and feed results back. Wrong fit for any interactive or iterative agent loop.
- Third-party vendor access (Bedrock, Vertex): same model capabilities, different auth/plumbing and sometimes different feature rollout timing — know that the Messages API contract stays conceptually the same across vendors.

### D2 — Software Engineering Foundations (7.4%)

- REST/JSON fundamentals apply directly to designing Claude tool schemas and API wrappers.
- Async programming: needed for streaming responses and for running multiple tool calls or subagent tasks concurrently without blocking.
- SDLC integration: where Claude-powered features fit in your existing build/test/review/deploy pipeline, not a separate parallel process.
- Code review and refactoring at both small scale (single function) and large scale (cross-file, architectural) — Claude Code assists at both, but the review discipline (tests, diff review) doesn't change.

### D2 — Claude Application Design (8.6%)

- Claude behaves differently depending on interface: claude.ai/Desktop chat, Claude Code (repo-aware, tool-using), API/SDK (you control every input). Design decisions (what context to provide, what tools to expose) must match the interface's actual capabilities.
- Content boundaries: keep untrusted content (retrieved documents, user-submitted text) clearly separated from trusted instructions so the model doesn't treat injected text as a command.
- Schema design for structured output: nullable/optional fields for data that may legitimately be absent (required fields pressure the model to fabricate); enums with an escape hatch (`"other"` + detail, or `"unclear"`) for ambiguous real-world input.
- Session hygiene: don't let one long-running session accumulate unrelated tasks' context; start fresh sessions (or `/compact`) at natural task boundaries.
- Plugin management: plugins bundle skills/commands/MCP connections for distribution — a packaging and versioning concern, not a new capability class.

### D2 — Configuration Management (4.1%)

- CLAUDE.md hierarchy: user-level (`~/.claude/CLAUDE.md`, personal, never version-controlled) vs. project-level (committed, shared team standards) vs. directory-level (subtree-specific).
- settings.json: project/user configuration for permissions, tool allowlists, and other CLI behavior — distinct from CLAUDE.md's role as instructional content.
- Model version pinning: pin a specific model version for reproducibility in production pipelines rather than always floating to "latest," since behavior can shift across releases.
- Prompt versioning: treat prompts as versioned artifacts (like code) so you can roll back a regression and A/B test changes.
- Plugin dependencies: plugins can depend on specific tool or MCP availability — a missing dependency should fail predictably, not degrade silently.

### D3 — Claude Code Operation (3.1%)

- Core components: **Rules** (path-scoped conventions via `.claude/rules/` with `paths:` globs), **Skills** (on-demand task-specific workflows in `.claude/skills/`, with frontmatter like `context: fork`, `allowed-tools`, `argument-hint`), **Commands** (custom slash commands), **Agents** (subagent definitions), **Agent Memory** (persisted findings/scratchpad across a session or resumption).
- Session management: `--resume` to continue a named session; sessions carry their own context and history.
- Headless mode (`-p`/`--print`): required for any non-interactive/CI invocation — without it, the process waits for interactive input and a CI job hangs.
- Streaming mode and auto-mode: streaming for incremental output consumption; auto-mode for reduced confirmation prompts in trusted, scripted contexts.
- CLAUDE.md hierarchy and repository initialization mirror the D2 configuration concepts, applied specifically inside the Claude Code product.

### D4 — Debugging and Error Handling (2.6%)

- Error type identification: distinguish integration-layer errors (your code's API calls, auth, network) from model-output errors (the model produced something wrong or unparseable) before choosing a fix.
- Recovery strategy selection: transient failures get retried; validation/business-rule failures get surfaced with structured detail, not blindly retried.
- Trace analysis: read the actual sequence of tool calls, tool results, and model turns to localize where a multi-step agent run diverged from the intended path, rather than guessing from the final output alone.

### D5 — LLM Fundamentals (5.2%)

- Tokens: the unit of both context-window accounting and billing; a rough proxy for cost and latency.
- Context window: finite; both input and output share the same budget, so long inputs reduce room for output (and vice versa).
- Sampling and non-determinism: the same prompt can produce different outputs across calls; design evals and tests that tolerate this rather than asserting exact string matches.
- Model options: fast mode for latency-sensitive/simple tasks; extended thinking / adaptive thinking / effort levels for harder reasoning tasks where you're willing to trade latency and cost for quality.
- Fundamental prompting techniques: zero-shot (no examples), single-shot (one example), multi-shot/few-shot (several examples) — few-shot generally improves consistency on tasks with a specific desired format or edge-case handling.

### D5 — Model Selection and Tradeoffs (2.7%)

- Opus vs. Sonnet vs. Haiku: roughly capability/cost/latency tiers — Opus for the hardest reasoning, Haiku for high-volume/low-latency simple tasks, Sonnet as the balanced default for most production workloads.
- Adaptive thinking support varies by model/tier — check before assuming a thinking mode is available for a given deployment.
- Breaking changes across model releases: pin versions in production and test against a new version before floating to it; don't assume identical behavior across releases even at the "same" capability tier.

### D5 — Cost and Token Management (2.8%)

- Token usage tracking: instrument actual token consumption per request/feature to attribute cost, not just estimate from prompt length.
- Cost modeling: account for input tokens, output tokens, and cache read/write pricing separately — they are not priced the same.
- Prompt caching / cache checkpointing: reduces cost and latency for repeated stable prefixes; requires deliberately structuring prompts (stable content first) to get cache hits.

### D6 — Context Engineering (3.8%)

- Context window management: actively curate what stays in context rather than letting it grow unbounded.
- Preventing context drift/bloat: prune or summarize verbose tool outputs before they accumulate; keep only the fields actually needed downstream.
- Context isolation via subagents/multi-step workflows: route exploratory or verbose sub-tasks to isolated contexts (subagents) so only a distilled result re-enters the main conversation.

### D6 — Prompt Engineering (4.6%)

- Instruction clarity and system vs. user placement: stable, role-defining instructions belong in the system prompt; per-request variable content belongs in user messages.
- Few-shot examples: the most reliable lever for consistent output format/edge-case handling when prose instructions alone produce drift.
- Output constraints: explicit format constraints (schemas, enumerated options) reduce variance more reliably than prose asking nicely for a format.
- Iterative refinement: treat prompts as something you test and version, not something you get right on the first attempt.
- Input sanitization: treat any user- or retrieval-sourced text inserted into a prompt as potentially adversarial.

### D6 — Output Handling (2.6%)

- Structured output patterns: prefer tool-use/schema-constrained output over parsing free-form text when downstream code needs to consume the result programmatically.
- Response validation: schema compliance (syntax) does not guarantee semantic correctness — validate business logic (do line items sum correctly, is a referenced ID actually valid) separately.
- Defensive parsing and skepticism toward confident output: a fluent, confident-sounding response is not evidence of correctness — verify claims against ground truth where it matters.

### D7 — AI Application Security (3.2%)

- Prompt injection: text from an untrusted source (a web page, a user upload) that contains instructions the model might follow as if they came from you. Mitigate by isolating untrusted content from trusted instructions and gating sensitive actions behind guardrails/hooks rather than trusting the model to "notice" the injection.
- Jailbreak defense: layered defenses (system prompt design, guardrails, monitoring) rather than a single prompt-level fix.
- Untrusted input handling / data leakage prevention / PII handling: minimize what sensitive data enters the prompt at all; redact or tokenize where possible.
- AAA/CIA: authentication, authorization, confidentiality, privacy, integrity — the standard framework for reasoning about what could go wrong and who should be able to do what.

### D7 — Guardrails and Safe Deployment (2.3%)

- Content policy and guardrail layering: no single guardrail catches everything; combine prompt-level guidance, programmatic gates, and monitoring.
- Secure-by-design / least privilege: grant an agent only the tools and data access its task actually requires, not the broadest convenient set.

### D7 — Claude Hooks (1.0%)

- Hooks as guardrails: use hooks (not prompt instructions) when a safety rule must be enforced every time, deterministically — e.g., blocking a destructive tool call above a threshold, regardless of what the model "decides."

### D7 — Identity, Secrets, and Key Management (1.6%)

- Never hardcode API keys/credentials in prompts, code committed to version control, or MCP config files — use environment-variable expansion or a secrets manager.
- Identity validation and authorization checks belong in your application/tool layer, not as something the model is trusted to enforce on its own.
- Monitor authorized access after the fact (audit logs) as a second layer, not a substitute for access controls.

### D8 — Tool Implementation (4.4%)

- Tool descriptions are the primary mechanism the model uses to select the right tool — vague or overlapping descriptions cause misrouting even with good tool names.
- Error handling in tools: return structured error metadata (category, retryable flag, human-readable message) rather than opaque failures, so the calling agent can make a sensible recovery decision.
- Tool usage patterns: client-side tools execute in your application; server-side tools execute where the model runs. Approval patterns (human-in-the-loop confirmation) apply to sensitive actions regardless of where the tool executes.
- Tool set construction: fewer, well-scoped tools per agent outperform a large generic toolbox — tool-selection reliability degrades as the candidate set grows.

### D8 — MCP Server Development (2.1%)

- MCP servers expose reusable tools/resources/prompts that multiple Claude applications can share and that can be maintained independently of any single app.
- MCP resources expose content catalogs (so an agent has visibility into available data without exploratory tool calls) distinct from MCP tools (which perform actions).
- Communication patterns: stdio (local process) vs. sockets/network (remote server) — pick based on where the server needs to run relative to the client.

### D8 — Agentic Customization (4.1%)

- Built-in tools: lowest effort, fixed capability set provided by the platform/product.
- Custom tools: purpose-built for your specific backend/business logic, defined per application.
- Skills: on-demand, reusable task workflows (prompt + optional scripts) invoked when needed rather than always loaded.
- MCPs: reusable, cross-application tool/resource servers maintained independently of any single consuming app.
- Choosing among them is a reusability/maintenance-boundary decision: one-off and app-specific favors custom tools; shared across many apps/teams favors MCP; occasional structured workflow favors Skills.

## Decision Rules

- If the right sequence of steps varies by case and depends on intermediate results, use an agent, not a fixed workflow.
- If a rule must hold every single time regardless of what the model decides, enforce it with a hook or programmatic gate — not a prompt instruction.
- If a subagent needs prior findings, put them explicitly in its prompt; there is no context inheritance from the coordinator.
- If a task is latency-tolerant, high-volume, and does not need mid-task tool calls, consider the Batch API; if it needs any mid-request tool execution, it cannot use Batch.
- If output must be consumed programmatically, use tool-use/schema-constrained output, not free-text parsing.
- If a schema field may legitimately be absent, make it nullable — don't force a value and invite fabrication.
- If two tools have overlapping descriptions and the model misroutes between them, rewrite the descriptions (purpose, inputs, outputs, when to use each) before adding more prompt instructions.
- If a CI job hangs, check for missing `-p`/headless mode first.
- If downstream automation parses CLI output, require `--output-format json` (and `--json-schema` where supported).
- If credentials would otherwise appear in a config file or prompt, use environment-variable expansion or a secrets manager instead.
- If an agent's tool set is growing past what its role strictly needs, scope it down or split into specialized agents — larger toolsets degrade selection reliability.

## Anti-Patterns

- Relying on prompt wording alone to enforce a hard business rule with real consequences.
- Treating retrieved/untrusted content as trustworthy instructions.
- Required schema fields for data that may not exist in the source.
- Uniform, unstructured error messages that give the calling agent nothing to act on.
- Floating to "latest model" in production without re-testing against version-specific behavior changes.
- Hardcoding secrets in prompts, code, or MCP configuration files.
- Growing a single agent's toolset indefinitely instead of scoping or splitting responsibilities.
- Assuming schema-valid output is semantically correct.

## Memorization Cues

- **Workflow = fixed path. Agent = model decides the path.**
- **Hooks for guarantees, prompts for guidance.**
- **Batch API: cheaper, slower, no mid-request tools.**
- **Nullable beats fabricated.**
- **Tool descriptions drive routing — fix the description before adding prompt patches.**
- **`-p` for CI, `--output-format json` for machine parsing.**
- **Env vars/secrets managers, never hardcoded keys.**
- **Fewer, well-scoped tools beat one large toolbox.**

## Source References

- Exam guide Domain 1–8 content outline and detailed objectives (`exam_guide_developer_foundations.txt`)
- Exam guide Section 8 sample questions (Batch API, prompt injection, MCP server reusability)

## Gaps / Follow-Up

- This pack is built from the exam guide's task statements, not hands-on repetition. Pair it with actual API/SDK usage — build one small end-to-end agent exercising tool use, streaming, and at least one guardrail — per the guide's "How to Prepare" recommendation.
- Claude Code specifics (Rules/Skills frontmatter mechanics, `/compact`, Explore subagent) are covered in more depth in the Architect: Foundations workspace's `claude-code-in-action` pack — worth a skim even though Claude Code is only 3.1% of this exam.
