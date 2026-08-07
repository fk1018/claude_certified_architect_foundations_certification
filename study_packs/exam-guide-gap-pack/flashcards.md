# Exam Guide Gap Pack Flashcards

## Task Tool

Q: What is required in a coordinator's configuration before it can spawn any subagent?

A: Its `allowedTools` must include `"Task"` — the Task tool is the subagent-spawning mechanism.

## AgentDefinition

Q: What does an AgentDefinition configure, and which part most influences delegation quality?

A: Each subagent type's description, system prompt, and tool restrictions. The description drives the coordinator's delegation choices — vague descriptions cause misrouting.

## Subagent Context Isolation

Q: What context does a spawned subagent inherit from the coordinator?

A: None. No conversation history, no shared memory between invocations. Everything it needs must be placed explicitly in its prompt.

## Parallel Subagents

Q: How do you run multiple subagents in parallel?

A: Emit multiple Task tool calls in a single coordinator response. Calls spread across separate turns run sequentially.

## Inter-Agent Data Format

Q: How should findings be passed between agents to preserve attribution?

A: As structured data separating content from metadata — source URLs, document names, page numbers, dates — not as prose summaries.

## Hub-and-Spoke

Q: Why route all subagent communication through the coordinator?

A: Observability, consistent error handling, and controlled information flow. Direct subagent-to-subagent handoffs are the anti-pattern.

## Narrow Decomposition

Q: Every subagent succeeds, yet the final report misses whole subdomains of the topic. Root cause?

A: The coordinator's task decomposition was too narrow — subagents covered only what they were assigned. Fix decomposition breadth, not the subagents.

## Iterative Refinement Loop

Q: How does a coordinator fix coverage gaps found in synthesis output?

A: Evaluate the synthesis for gaps → re-delegate targeted queries to search/analysis subagents → re-invoke synthesis → repeat until coverage is sufficient.

## Coordinator Prompt Style

Q: Should a coordinator give subagents step-by-step procedures or goals?

A: Research goals and quality criteria. Procedural instructions kill subagent adaptability.

## Named Session Resume

Q: How do you continue a specific prior investigation across work sessions?

A: `--resume <session-name>`.

## fork_session

Q: When is `fork_session` the right choice?

A: To explore divergent approaches (e.g., two refactoring strategies) as independent branches from a shared analysis baseline, without re-analyzing.

## Resume vs Fresh

Q: Prior session's tool results are stale after a big refactor. Resume or restart?

A: Start a new session seeded with a structured summary — more reliable than resuming atop stale tool results. Resume only when prior context is mostly valid.

## Resuming After Edits

Q: You resume a session after modifying a few files. What should you do?

A: Tell the agent exactly which files changed so it re-analyzes only those, instead of re-exploring the codebase.

## Error Categories

Q: Name the four structured error categories for MCP tools.

A: Transient (retryable), validation (fix input), business (policy — never retry), permission.

## Structured Error Fields

Q: What should an MCP tool failure include so the agent can recover intelligently?

A: `errorCategory`, an `isRetryable` boolean, and a human-readable description; business errors add `retriable: false` plus a customer-friendly explanation and an alternative.

## Empty vs Error

Q: A query finds no matching records. What should the tool return?

A: Success with an empty result set and a note like "no orders found" — errors are reserved for actual access failures.

## Local Recovery

Q: Which errors should a subagent propagate to the coordinator?

A: Only those it cannot resolve locally (it retries transient failures itself), propagated with partial results and what was attempted.

## MCP Config Scopes

Q: Where do team-shared vs personal MCP servers get configured?

A: Team-shared in project `.mcp.json` (version-controlled); personal/experimental in `~/.claude.json`.

## MCP Credentials

Q: How do you configure an MCP server token without committing secrets?

A: Environment-variable expansion in `.mcp.json`, e.g. `${GITHUB_TOKEN}`.

## MCP Server Discovery

Q: When three MCP servers are configured, which one's tools are available?

A: All of them — tools from every configured server are discovered at connection time and available simultaneously. There is no "active server."

## MCP Resources

Q: What are MCP resources for?

A: Exposing content catalogs (issue summaries, doc hierarchies, schemas) so agents see available data without exploratory tool calls.

## Community vs Custom MCP

Q: Standard integration like Jira — build or reuse?

A: Use an existing community MCP server; reserve custom servers for team-specific workflows.

## CLAUDE.md Hierarchy

Q: Why doesn't a teammate get standards stored in your `~/.claude/CLAUDE.md`?

A: User-level config applies only to your account and isn't in version control. Team standards belong in a project-level CLAUDE.md in the repo.

## @import

Q: How do you keep a monorepo CLAUDE.md modular?

A: Each package's CLAUDE.md uses `@import` to include only the standards files relevant to that package.

## Path-Scoped Rules

Q: Conventions must apply to test files scattered across every directory. Mechanism?

A: A `.claude/rules/` file with YAML frontmatter `paths: ["**/*.test.tsx"]` — loads only when editing matching files. Directory CLAUDE.md can't follow scattered files.

## Rules vs Directory CLAUDE.md

Q: When is a directory-level CLAUDE.md better than a path-scoped rule?

A: When conventions apply to one self-contained subtree; use `paths:` globs when they span directories.

## context: fork

Q: What does `context: fork` in skill frontmatter do?

A: Runs the skill in an isolated sub-agent context so verbose or exploratory output doesn't pollute the main conversation.

## allowed-tools

Q: What does `allowed-tools` in skill frontmatter do?

A: Restricts which tools the skill may use during execution (least privilege, e.g., blocking destructive actions).

## argument-hint

Q: What does `argument-hint` in skill frontmatter do?

A: Prompts the developer for required parameters when the skill is invoked without arguments.

## Skills vs CLAUDE.md

Q: Where do universal always-applied standards go vs on-demand workflows?

A: Always-applied → CLAUDE.md (always loaded). On-demand task workflows → skills.

## Personal Skill Variant

Q: How do you customize a team skill without affecting teammates?

A: Create a personal variant in `~/.claude/skills/` under a different name.

## Explore Subagent

Q: What is the Explore subagent for?

A: Isolating verbose discovery output during codebase exploration, returning summaries to preserve main-conversation context.

## CI Non-Interactive

Q: A CI job running `claude "..."` hangs forever. Fix?

A: Add `-p` (`--print`) — non-interactive mode that prints the result and exits. (`CLAUDE_HEADLESS`, `--batch` are fake distractors.)

## CI Structured Output

Q: How do you get schema-enforced machine-parseable output from Claude Code in CI?

A: `--output-format json` together with `--json-schema`.

## CI Independent Review

Q: Why shouldn't the session that generated code also review it in CI?

A: It retains its own reasoning context and is less likely to question its decisions. Use a separate independent instance.

## CI Re-Review Dedup

Q: How do you stop duplicate PR comments when re-reviewing after new commits?

A: Include prior review findings in context and instruct Claude to report only new or still-unaddressed issues.

## Batches API Facts

Q: List the Message Batches API facts the exam tests.

A: 50% cost savings; up to 24-hour processing; no latency SLA; `custom_id` correlates request/response; no multi-turn tool calling within a request.

## Batch Fit

Q: Which workloads belong on the Batches API?

A: Non-blocking, latency-tolerant work (overnight reports, weekly audits, nightly test generation). Never blocking flows like pre-merge checks.

## Batch SLA Math

Q: Batches take up to 24h and your SLA is 30h from document arrival. Submission cadence?

A: Every 4 hours — worst case 4 + 24 = 28 ≤ 30. (Every 8 hours: 32 > 30, breach.)

## Batch Failures

Q: 40 of 900 batch items failed. What do you resubmit?

A: Only the failed items, identified by `custom_id`, modified as needed (e.g., chunk documents that exceeded context limits).

## Batch Prep

Q: Before batch-processing 10,000 documents, what should you do?

A: Refine the prompt on a small sample set first to maximize first-pass success and avoid costly resubmission cycles.

## Nullable Fields

Q: Why make schema fields optional/nullable when data may be absent?

A: Required fields pressure the model to fabricate values to satisfy the schema; nullable fields let it return null honestly.

## Enum Patterns

Q: How do you design enums for ambiguous and unforeseen categories?

A: Add `"unclear"` for ambiguous cases and `"other"` plus a detail string for extensible categories.

## Syntax vs Semantic

Q: What do strict JSON schemas via tool use eliminate — and not eliminate?

A: They eliminate syntax errors; they do not prevent semantic errors (values that don't sum, data in wrong fields). Validate semantics separately (e.g., `calculated_total` vs `stated_total`, `conflict_detected`).

## Retry Limits

Q: When is retry-with-error-feedback useless?

A: When the required information is absent from the source document. Retries fix format/structural errors only.

## detected_pattern

Q: What is a `detected_pattern` field on review findings for?

A: Tracking which code constructs trigger findings so dismissed findings can be analyzed for false-positive patterns.

## Multi-Pass Review

Q: A 14-file PR review is inconsistent and contradictory. Restructure how?

A: Per-file passes for local issues plus a separate cross-file integration pass — fixes attention dilution.

## Case Facts Block

Q: After summarization the agent quotes "around $80" instead of $83.47. Fix?

A: Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block included in every prompt outside summarized history.

## Lost in the Middle

Q: How do you mitigate position effects in long aggregated inputs?

A: Put a key-findings summary at the beginning and organize detail under explicit section headers; models attend best to the start and end.

## Tool Output Trimming

Q: Order lookups return 40+ fields but 5 matter. What do you do?

A: Trim tool outputs to relevant fields before they accumulate in context.

## Escalation Triggers

Q: Name the three valid escalation triggers.

A: Explicit customer request for a human (honor immediately), policy gap/exception (policy silent or ambiguous), and inability to make meaningful progress.

## Explicit Human Request

Q: Customer demands a human for a case the agent could easily solve. What happens?

A: Escalate immediately with a structured handoff — do not investigate first. (If merely frustrated but not demanding a human: acknowledge, offer to resolve, escalate if they reiterate.)

## Bad Escalation Proxies

Q: Why not escalate based on sentiment or the agent's self-reported confidence?

A: Neither correlates with actual case complexity; self-reported confidence is poorly calibrated.

## Multiple Matches

Q: `get_customer` returns three matching customers. What should the agent do?

A: Ask the customer for additional identifiers. Never select heuristically.

## Error Propagation

Q: What should a failing subagent return so the coordinator can recover?

A: Structured context: failure type, attempted query, partial results, and potential alternative approaches.

## Propagation Anti-Patterns

Q: Name three error-propagation anti-patterns.

A: Generic statuses ("search unavailable"), silent suppression (failure returned as empty success), and terminating the whole workflow on a single failure.

## Scratchpads & Manifests

Q: How do agents survive context degradation and crashes in long explorations?

A: Scratchpad files recording key findings (referenced for later questions); structured state exports/manifests the coordinator loads on resume; phase summaries injected into the next phase.

## Confidence Calibration

Q: How are confidence scores made trustworthy for routing review?

A: Have the model output field-level confidence, then calibrate thresholds against labeled validation sets.

## Stratified Sampling

Q: Why keep sampling high-confidence extractions after automating them?

A: Stratified random sampling measures the residual error rate and detects novel error patterns that confidence scores miss.

## Accuracy Segmentation

Q: Aggregate extraction accuracy is 97%. Why can't you cut human review yet?

A: Aggregates can mask poor performance on specific document types or fields — validate accuracy per segment first.

## Claim-Source Mappings

Q: How does source attribution survive multi-agent synthesis?

A: Subagents output structured claim-source mappings (URL, document, excerpt, date) that downstream agents must preserve and merge.

## Conflicting Statistics

Q: Two credible sources report different figures. What does synthesis do?

A: Includes both values annotated with their sources (and dates); never averages, drops, or arbitrarily picks one. Reports separate well-established from contested findings.

## Temporal Data

Q: Why require publication/collection dates in subagent outputs?

A: So temporal differences aren't misread as contradictions.

## Coverage Annotations

Q: Some sources were unreachable during research. How does the report handle it?

A: Structure the synthesis with coverage annotations — which findings are well-supported and which topic areas have gaps due to unavailable sources.

## Content-Type Rendering

Q: How should synthesis render mixed content types?

A: Appropriately per type — financial data as tables, news as prose, technical findings as structured lists — not one uniform format.
