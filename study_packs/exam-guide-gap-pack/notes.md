# Exam Guide Gap Pack (Zero-Coverage Topics)

- Source URL: `exam_guide_pdf_v0.2.txt` (archived official exam guide draft, v0.2, 2026-06-30) — not a Skilljar course
- Completed: 2026-07-06
- Study pack: `study_packs/exam-guide-gap-pack/`
- Purpose: closes the topics a cross-pack audit (`fable_review_0.md`) found had zero or weak coverage across all seven course packs. Built directly from the exam guide's task statements, so terminology here is exam terminology.

## Captured Sections

- Domain 1 task statements 1.2, 1.3, 1.7 (coordinator/subagent orchestration, Task tool, sessions)
- Domain 2 task statements 2.2, 2.4 (structured MCP errors, `.mcp.json` mechanics)
- Domain 3 task statements 3.1 (@import), 3.2 (skills frontmatter), 3.3 (path rules), 3.6 (CI flags)
- Domain 4 task statements 4.3 (schema design specifics), 4.4 (retry limits), 4.5 (Message Batches API), 4.6 (multi-instance review)
- Domain 5 task statements 5.1–5.6 (context, escalation, error propagation, calibration, provenance)

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| Domain 1: Agentic Architecture & Orchestration | High | Task tool, AgentDefinition, allowedTools, parallel spawning, hub-and-spoke, decomposition breadth, iterative refinement, `--resume`, `fork_session` |
| Domain 2: Tool Design & MCP Integration | High | errorCategory/isRetryable metadata, empty-vs-error, local recovery, `.mcp.json` vs `~/.claude.json`, `${ENV_VAR}` expansion, MCP resources |
| Domain 3: Claude Code Configuration & Workflows | High | `.claude/rules/` path globs, `@import`, skills frontmatter (`context: fork`, `allowed-tools`, `argument-hint`), Explore subagent, `-p`, `--output-format json`, `--json-schema` |
| Domain 4: Prompt Engineering & Structured Output | High | Message Batches API, nullable/enum schema patterns, retry-with-error-feedback limits, `detected_pattern`, independent review instances, per-file + integration passes |
| Domain 5: Context Management & Reliability | High | Case-facts blocks, lost-in-the-middle, escalation triggers, structured error propagation, scratchpads/manifests, confidence calibration, stratified sampling, claim-source provenance |

## Key Concepts

### D1 — Subagent spawning and context (TS 1.3)

- Task tool: the mechanism a coordinator uses to spawn subagents. The coordinator's `allowedTools` **must include `"Task"`** or it cannot delegate at all.
- AgentDefinition: configures each subagent type — description, system prompt, tool restrictions. The *description* is what drives delegation choices, so vague descriptions cause misrouting.
- Context isolation: subagents do **not** inherit the coordinator's conversation history and do not share memory between invocations. Anything a subagent needs (prior findings, search results, constraints) must be placed **explicitly in its prompt**.
- Parallel spawning: emit **multiple Task tool calls in a single coordinator response**. Spawning across separate turns runs them sequentially.
- Pass structured data between agents: separate content from metadata (source URLs, document names, page numbers) so attribution survives handoffs.
- Coordinator prompts should state **research goals and quality criteria**, not step-by-step procedures — procedures kill subagent adaptability.

### D1 — Coordinator patterns (TS 1.2)

- Hub-and-spoke: the coordinator mediates **all** inter-subagent communication. Benefits: observability, consistent error handling, controlled information flow. Direct subagent-to-subagent handoffs are the anti-pattern.
- Coordinator responsibilities: task decomposition, delegation, result aggregation, and deciding **which** subagents to invoke per query (dynamic selection — not always the full pipeline).
- Narrow-decomposition risk: if the coordinator splits "creative industries" into only visual-arts subtasks, downstream agents execute perfectly and the report still misses music/writing/film. The fix targets the **coordinator's decomposition**, not the subagents.
- Iterative refinement loop: coordinator evaluates synthesis output for gaps → re-delegates targeted queries to search/analysis subagents → re-invokes synthesis → repeat until coverage is sufficient.
- Partition research scope across subagents (distinct subtopics or source types) to minimize duplication.

### D1 — Sessions, resumption, forking (TS 1.7)

- `--resume <session-name>`: continue a specific named prior conversation across work sessions.
- `fork_session`: create independent branches from a **shared analysis baseline** to explore divergent approaches (e.g., compare two refactoring strategies without re-analyzing the codebase twice).
- Resume vs fresh: resume when prior context is mostly still valid. When prior tool results are **stale** (code changed significantly), starting a **new session seeded with a structured summary** is more reliable than resuming.
- If you do resume after modifying files, **tell the agent which files changed** so it re-analyzes only those instead of re-exploring everything.

### D2 — Structured MCP error responses (TS 2.2)

- Error taxonomy: **transient** (timeout, service unavailable — retryable), **validation** (bad input — fix and retry), **business** (policy violation — never retryable), **permission** (not allowed).
- Return structured metadata: `errorCategory`, `isRetryable` boolean, human-readable description. Uniform "Operation failed" prevents the agent from choosing a sensible recovery.
- Business errors: include `retriable: false` plus a customer-friendly explanation (and ideally an alternative, e.g., store credit) so the agent communicates instead of retrying forever.
- **Access failure ≠ empty result.** A successful query with no matches should return success with an empty result set ("no orders found"), reserving errors for actual failures. Otherwise the agent apologizes for "technical difficulties" that aren't happening.
- Local recovery: subagents retry transient failures themselves; they propagate to the coordinator only errors they cannot resolve — together with partial results and what was attempted.

### D2 — MCP server configuration (TS 2.4)

- Project scope: `.mcp.json` in the repo — version-controlled, shared team tooling.
- User scope: `~/.claude.json` — personal/experimental servers, not shared.
- Credentials: environment-variable expansion in `.mcp.json` (e.g., `${GITHUB_TOKEN}`) keeps secrets out of the repo.
- Tools from **all configured servers are discovered at connection time and available simultaneously** — there is no "active server" switching.
- MCP resources expose content catalogs (issue summaries, doc hierarchies, schemas) so agents see what's available without exploratory tool calls.
- Prefer community MCP servers for standard integrations (Jira, GitHub); build custom only for team-specific workflows.

### D3 — Configuration mechanics (TS 3.1, 3.2, 3.3)

- Hierarchy: user `~/.claude/CLAUDE.md` (personal, never shared via git) → project CLAUDE.md (team, version-controlled) → directory-level CLAUDE.md (subtree-specific).
- `@import` syntax keeps CLAUDE.md modular: each package's CLAUDE.md imports only the standards files relevant to it.
- `.claude/rules/` files with YAML frontmatter `paths: ["glob"]` load **only when editing matching files**. Choose them over directory CLAUDE.md when a convention spans directories (e.g., `**/*.test.tsx` scattered through the repo). Choose directory CLAUDE.md for a self-contained subtree.
- Skills frontmatter (in `SKILL.md`):
  - `context: fork` — run the skill in an isolated sub-agent context so verbose or exploratory output doesn't pollute the main conversation.
  - `allowed-tools` — restrict tool access during skill execution (least privilege).
  - `argument-hint` — prompt the developer for required parameters when invoked without arguments.
- Skills = on-demand, task-specific workflows. CLAUDE.md = always-loaded universal standards. Personal skill variants go in `~/.claude/skills/` under a **different name** so teammates aren't affected.
- Explore subagent: isolates verbose discovery output and returns summaries — use for large read-only surveys during multi-phase work.
- `/memory` verifies which memory files loaded — first diagnostic for inconsistent conventions.

### D3 — CI/CD integration (TS 3.6)

- `-p` / `--print`: non-interactive mode. Without it, CI jobs hang waiting for input. (Fake alternatives like `CLAUDE_HEADLESS=true` or `--batch` are classic distractors.)
- `--output-format json` + `--json-schema`: machine-parseable, schema-enforced findings for automated posting (e.g., inline PR comments).
- Independent review: the session that generated code is worse at reviewing it (it retains its own reasoning). Use a separate instance for CI review.
- Re-reviews after new commits: include prior findings in context and instruct Claude to report only new or still-unaddressed issues (no duplicate comments).
- Provide existing test files in context so test generation doesn't duplicate covered scenarios; put testing standards/fixtures in CLAUDE.md.

### D4 — Message Batches API (TS 4.5)

- Facts to memorize: **50% cost savings, up to 24-hour processing window, no latency SLA, `custom_id` correlates request/response pairs, no multi-turn tool calling within a request.**
- Fit: non-blocking, latency-tolerant work (overnight reports, weekly audits, nightly test generation). Never for blocking flows (pre-merge checks) — "usually faster than 24h" is not a guarantee.
- SLA math: worst case = submission interval + 24h. To guarantee a 30-hour SLA, submit every 4 hours (4 + 24 = 28 ≤ 30); every 8 hours breaches (32 > 30).
- Failure handling: resubmit **only failed items** (identified by `custom_id`), modified as needed (e.g., chunk documents that blew the context limit).
- Refine the prompt on a small sample **before** batch-processing the full volume — resubmission cycles are slow and costly.

### D4 — Schema design, retry limits, review architecture (TS 4.3, 4.4, 4.6)

- Nullable/optional fields for information that may be absent — required fields pressure the model to **fabricate** values.
- Enum patterns: add `"unclear"` for ambiguous cases; `"other"` + a detail string for extensible categories.
- Strict schemas via tool use eliminate **syntax** errors only — semantic errors (line items not summing, values in wrong fields) still need validation. Self-check patterns: extract `calculated_total` alongside `stated_total`; add `conflict_detected` booleans.
- Retry-with-error-feedback: resend document + failed extraction + the specific validation errors. Works for format/structure mistakes; **useless when the information simply isn't in the source** — detect that case and stop retrying.
- `detected_pattern` field on findings lets you analyze which constructs trigger false positives when developers dismiss them.
- Multi-pass review: per-file passes for local issues + a separate cross-file integration pass — fixes attention dilution and contradictory findings on large PRs.

### D5 — Context, escalation, propagation, calibration, provenance

- Case-facts block (TS 5.1): extract transactional facts (exact amounts, dates, order numbers, statuses) into a persistent block included in every prompt **outside** summarized history — summarization turns $83.47 into "around $80".
- Trim verbose tool outputs to relevant fields before they accumulate (40-field order lookups when 5 fields matter).
- Lost-in-the-middle (TS 5.1): models attend to the start and end of long inputs. Put a key-findings summary first and organize detail under explicit section headers.
- Escalation triggers (TS 5.2): (1) customer explicitly asks for a human — honor **immediately**, no investigation first; (2) policy is ambiguous or silent on the request (e.g., competitor price matching when policy only covers own-site); (3) no meaningful progress. Frustrated-but-simple cases: acknowledge, offer to resolve, escalate only if the customer reiterates.
- Unreliable escalation proxies: sentiment analysis and self-reported confidence scores do not track case complexity.
- Multiple customer matches → ask for additional identifiers; never pick heuristically.
- Error propagation (TS 5.3): return failure type + attempted query + partial results + possible alternatives. Anti-patterns: generic status ("search unavailable"), silent suppression (empty result marked success), terminating the whole workflow on one failure.
- Long-exploration hygiene (TS 5.4): scratchpad files for key findings; phase summaries injected into the next phase's subagents; crash recovery via structured state exports/manifests the coordinator loads on resume; `/compact` when discovery output fills context.
- Confidence calibration (TS 5.5): field-level confidence scores calibrated against **labeled validation sets**; stratified random sampling of high-confidence extractions to measure residual error and catch novel patterns; segment accuracy by document type and field before cutting human review — aggregate 97% can hide a failing segment.
- Provenance (TS 5.6): subagents output structured claim-source mappings (URL, document, excerpt, publication/collection date) that synthesis must preserve and merge. Conflicting credible statistics → include both, annotated with sources (and dates — temporal differences aren't contradictions). Annotate coverage gaps from unavailable sources. Render by content type: financial data as tables, news as prose, technical findings as lists.

## Decision Rules

- If a coordinator never delegates, check `allowedTools` for `"Task"` before touching prompts.
- If a subagent ignores prior findings, put those findings in its prompt — there is no inheritance to enable.
- If subtasks are independent, spawn them as multiple Task calls in one response; sequential turns are the slow path.
- If a report misses whole subdomains while every subagent succeeded, fix the coordinator's decomposition breadth.
- If comparing divergent approaches from one analysis baseline, `fork_session`; if prior tool results are stale, fresh session + structured summary.
- If a tool failure could be retried, the *tool response* must say so (`errorCategory` + `isRetryable`) — don't make the model guess.
- If a query legitimately finds nothing, return success + empty set, not an error.
- If team-shared MCP tooling, `.mcp.json` + `${ENV_VAR}`; if personal/experimental, `~/.claude.json`.
- If a convention spans scattered files, `.claude/rules/` with `paths:` globs; if it's one subtree, a directory CLAUDE.md.
- If a skill produces verbose/exploratory output, `context: fork`; if it must not touch dangerous tools, `allowed-tools`; if it needs parameters, `argument-hint`.
- If CI, always `-p`; if downstream code parses the output, `--output-format json` + `--json-schema`.
- If work is latency-tolerant and non-blocking, Message Batches API (50% cheaper); if anything blocks on it, synchronous API.
- If extraction keeps failing on a field, first ask whether the information exists in the source — retries only fix format/structure errors.
- If a customer asks for a human, escalate now; if policy has no answer, escalate; if merely frustrated, acknowledge and offer to resolve.
- If cutting human review, first segment accuracy by document type and field, then calibrate thresholds on a labeled set, then keep stratified sampling running.
- If two credible sources disagree, keep both values with attribution and dates; never average, drop, or arbitrarily pick.

## Anti-Patterns

- Prompt-only enforcement of hard business rules (probabilistic compliance; use hooks/gates for guarantees).
- Subagent-to-subagent direct handoffs (no observability, inconsistent error handling).
- Step-by-step procedural coordinator prompts (kills adaptability; give goals and quality criteria).
- Resuming a session on top of stale tool results instead of fresh-with-summary.
- Uniform "Operation failed" errors; errors for valid empty results; silently marking failures as success.
- Committing tokens in `.mcp.json` instead of `${ENV_VAR}` expansion.
- Monolithic 900-line CLAUDE.md instead of `@import`/`.claude/rules/` modularity.
- Batch API for blocking workflows; polling and "it's usually faster" as an SLA strategy.
- Required schema fields for possibly-absent data (fabrication pressure).
- Retrying extraction when the source lacks the information.
- Self-review in the generating session as the primary quality gate.
- Sentiment-based escalation; self-reported confidence thresholds without calibration.
- Trusting aggregate accuracy; cutting review without per-segment validation.
- Summarizing away source attribution, dates, or exact figures.

## Scenario Traps

- "Add it to the system prompt" for a must-never-happen rule: plausible, but the exam wants programmatic enforcement (hooks/prerequisite gates) when compliance must be deterministic.
- "Give the struggling subagent more tools": the exam prefers scoped access — a narrow cross-role tool for the high-frequency case (e.g., `verify_fact` for synthesis), with complex cases still routed through the coordinator.
- "Retry with exponential backoff, then return a generic status": hides context; the coordinator needs structured failure detail to decide recovery.
- "Switch to a bigger context window" for attention/consistency problems: the fix is decomposition (per-file passes, trimming, summaries at the front), not more window.
- "Batch both workflows for the 50% savings": only the latency-tolerant one; blocking checks stay synchronous.
- "The agent seems unsure, so route by its confidence score": self-reported confidence is uncalibrated; calibrate on labeled data first, and route ambiguous/contradictory sources to humans.
- "Average the conflicting numbers" / "use the newer one": preserve both with attribution and dates.
- Fake-feature distractors: `CLAUDE_HEADLESS`, `--batch`, `parallel: true` on Task, "active MCP server" switching, MCP per-server tool limits, `session_id` params — if you've never seen it in the guide's appendix, suspect it.

## Memorization Cues

- **Batch API = 50 / 24 / custom_id / no-tools**: 50% cheaper, ≤24h, correlate by custom_id, no multi-turn tool calling.
- **SLA math**: worst case = submission interval + 24. (30h SLA → submit every 4h.)
- **Error categories: T-V-B-P** — transient, validation, business, permission; only transient/validation are retry candidates.
- **Escalate on: ASK, GAP, STUCK** — explicit request, policy gap, no progress.
- **Task-in-allowedTools** — no `"Task"`, no subagents.
- **Fork to compare, fresh when stale, resume when valid.**
- **Project `.mcp.json` / personal `~/.claude.json`** — "team file lives in the repo."
- **fork / allowed-tools / argument-hint** — isolate, restrict, prompt-for-args.
- **`-p` prints, JSON needs a schema** — `-p` + `--output-format json` + `--json-schema` for CI.
- **Nullable beats fabricated; "other"+detail beats a frozen enum; "unclear" beats a guess.**
- **Calibrate, stratify, segment** — labeled sets, random sampling of high-confidence, per-type/per-field accuracy.
- **Both values, both sources, both dates** — conflict handling in synthesis.

## Source References

- Exam guide Domain 1 task statements 1.2, 1.3, 1.7 (coordinator patterns, Task tool/AgentDefinition, sessions/forking)
- Exam guide Domain 2 task statements 2.2, 2.4 (structured errors, MCP config scoping)
- Exam guide Domain 3 task statements 3.1–3.3, 3.6 (hierarchy/@import, skills frontmatter, path rules, CI flags)
- Exam guide Domain 4 task statements 4.3–4.6 (schemas, retry, batches, multi-pass review)
- Exam guide Domain 5 task statements 5.1–5.6 (context, escalation, propagation, exploration hygiene, calibration, provenance)
- Exam guide Appendix: "Technologies and Concepts", "In-Scope Topics", "Out-of-Scope Topics"
- Exam guide sample questions 1–12 (answer-rationale style these notes mirror)

## Gaps / Follow-Up

- This pack is doctrine from the guide, not hands-on experience. Do the guide's Preparation Exercises — especially Exercise 4 (multi-agent research pipeline: Task spawning, parallel delegation, error propagation, provenance) and Exercise 3 (extraction pipeline: schemas, validation-retry, batches) — to convert recall into judgment.
- Hook mechanics (PreToolUse/PostToolUse details) are covered in `study_packs/claude-code-in-action/`; `tool_choice` and `stop_reason` are covered in `study_packs/claude-in-amazon-bedrock/`. Review those alongside this pack.
- Least-privilege tool distribution across specialized subagents (TS 2.3) is only touched here via scenario traps; drill it with practice exam questions.
