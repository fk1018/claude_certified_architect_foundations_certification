# Exam Guide Gap Pack Flashcards

## Task Tool

Q: What is required in a coordinator's configuration before it can spawn any subagent?

A: Its `allowedTools` must include `"Task"` — the Task tool is the subagent-spawning mechanism.

Domain: D3

Example: A coordinator whose config omits `"Task"` from `allowedTools` will fail when it tries to spawn a "research-subagent" to gather sources for a report.

## AgentDefinition

Q: What does an AgentDefinition configure, and which part most influences delegation quality?

A: Each subagent type's description, system prompt, and tool restrictions. The description drives the coordinator's delegation choices — vague descriptions cause misrouting.

Domain: D3

Example: A "code-reviewer" AgentDefinition described only as "helps with code" gets tasks meant for a "test-writer" agent routed to it by mistake; a description naming "reviews diffs for bugs and style issues" fixes the routing.

## Subagent Context Isolation

Q: What context does a spawned subagent inherit from the coordinator?

A: None. No conversation history, no shared memory between invocations. Everything it needs must be placed explicitly in its prompt.

Domain: D1

Example: A subagent spawned to "summarize the API docs discussed earlier" has no idea what "earlier" refers to unless the coordinator's prompt includes the actual doc excerpts or file paths.

## Parallel Subagents

Q: How do you run multiple subagents in parallel?

A: Emit multiple Task tool calls in a single coordinator response. Calls spread across separate turns run sequentially.

Domain: D1

Example: To research three competitors at once, the coordinator issues three Task calls for "research-subagent" (one per competitor) in the same response instead of waiting for each to finish before starting the next.

## Inter-Agent Data Format

Q: How should findings be passed between agents to preserve attribution?

A: As structured data separating content from metadata — source URLs, document names, page numbers, dates — not as prose summaries.

Domain: D1

Example: A subagent returns `{"claim": "revenue grew 12%", "source": "10-K filing", "url": "sec.gov/...", "date": "2025-03"}` instead of the vaguer sentence "revenue apparently grew about 12% per a filing."

## Hub-and-Spoke

Q: Why route all subagent communication through the coordinator?

A: Observability, consistent error handling, and controlled information flow. Direct subagent-to-subagent handoffs are the anti-pattern.

Domain: D1

Example: A "fetch-data" subagent finishes and hands its result to the coordinator, which then decides to invoke "analyze-data" — rather than "fetch-data" calling "analyze-data" directly and leaving the coordinator blind to that step.

## Narrow Decomposition

Q: Every subagent succeeds, yet the final report misses whole subdomains of the topic. Root cause?

A: The coordinator's task decomposition was too narrow — subagents covered only what they were assigned. Fix decomposition breadth, not the subagents.

Domain: D1

Example: A market report on "electric vehicles" only assigned subagents to research passenger cars, so the final report omits electric trucks and buses entirely — the fix is adding subtasks for those segments, not retraining the car subagent.

## Iterative Refinement Loop

Q: How does a coordinator fix coverage gaps found in synthesis output?

A: Evaluate the synthesis for gaps → re-delegate targeted queries to search/analysis subagents → re-invoke synthesis → repeat until coverage is sufficient.

Domain: D1

Example: After a first synthesis pass, the coordinator notices no pricing data was found, so it delegates a follow-up "find current pricing tiers" query, then re-runs synthesis with the new results merged in.

## Coordinator Prompt Style

Q: Should a coordinator give subagents step-by-step procedures or goals?

A: Research goals and quality criteria. Procedural instructions kill subagent adaptability.

Domain: D4

Example: Prompt the subagent with "find and cite at least three independent sources confirming the acquisition price" rather than "step 1: open Google, step 2: type the query, step 3: click the third result."

## Named Session Resume

Q: How do you continue a specific prior investigation across work sessions?

A: `--resume <session-name>`.

Domain: D3

Example: Running `claude --resume refactor-auth-module` picks up exactly where the named "refactor-auth-module" session left off, rather than starting a blank session.

## fork_session

Q: When is `fork_session` the right choice?

A: To explore divergent approaches (e.g., two refactoring strategies) as independent branches from a shared analysis baseline, without re-analyzing.

Domain: D3

Example: After a session finishes analyzing a slow database query, `fork_session` spins off two branches — one trying an index-based fix, another trying query restructuring — both reusing the same analysis instead of re-scanning the schema twice.

## Resume vs Fresh

Q: Prior session's tool results are stale after a big refactor. Resume or restart?

A: Start a new session seeded with a structured summary — more reliable than resuming atop stale tool results. Resume only when prior context is mostly valid.

Domain: D3

Example: After renaming half the modules in a large refactor, start a fresh session with a summary like "renamed `utils/` to `helpers/`, moved auth logic to `services/auth.ts`" rather than resuming a session whose cached file reads still point at the old paths.

## Resuming After Edits

Q: You resume a session after modifying a few files. What should you do?

A: Tell the agent exactly which files changed so it re-analyzes only those, instead of re-exploring the codebase.

Domain: D3

Example: "I edited `src/api/client.ts` and `src/api/types.ts` to add a `retries` option — re-check just those two files" instead of letting the agent re-scan the whole `src/api/` directory.

## Error Categories

Q: Name the four structured error categories for MCP tools.

A: Transient (retryable), validation (fix input), business (policy — never retry), permission.

Domain: D2

Example: A `create_refund` MCP tool call fails with `errorCategory: "business"` because the order is past the 30-day return window — retrying the same call won't help, since the fix is a policy exception, not a resend.

## Structured Error Fields

Q: What should an MCP tool failure include so the agent can recover intelligently?

A: `errorCategory`, an `isRetryable` boolean, and a human-readable description; business errors add `retriable: false` plus a customer-friendly explanation and an alternative.

Domain: D2

Example: A payment tool returns `{"errorCategory": "business", "isRetryable": false, "message": "Order already refunded", "alternative": "offer store credit instead"}` so the agent knows immediately not to retry and what to suggest instead.

## Empty vs Error

Q: A query finds no matching records. What should the tool return?

A: Success with an empty result set and a note like "no orders found" — errors are reserved for actual access failures.

Domain: D2

Example: `search_orders(customer_id: "C123")` returns `{"status": "success", "orders": [], "note": "no orders found for this customer"}` rather than throwing an error, since the lookup itself worked fine.

## Local Recovery

Q: Which errors should a subagent propagate to the coordinator?

A: Only those it cannot resolve locally (it retries transient failures itself), propagated with partial results and what was attempted.

Domain: D1

Example: A subagent hits a transient 503 from a search API, retries twice and succeeds on the third try without telling the coordinator; but if all retries fail, it reports back "search API unreachable after 3 attempts, returning partial results from cache."

## MCP Config Scopes

Q: Where do team-shared vs personal MCP servers get configured?

A: Team-shared in project `.mcp.json` (version-controlled); personal/experimental in `~/.claude.json`.

Domain: D2

Example: The team's shared Jira MCP server lives in the repo's `.mcp.json` so every teammate gets it on clone, while a developer's personal, still-experimental local-notes MCP server stays in their own `~/.claude.json`.

## MCP Credentials

Q: How do you configure an MCP server token without committing secrets?

A: Environment-variable expansion in `.mcp.json`, e.g. `${GITHUB_TOKEN}`.

Domain: D2

Example: `.mcp.json` sets `"env": {"TOKEN": "${GITHUB_TOKEN}"}`, so the actual token stays in each developer's shell environment or CI secret store rather than in the committed file.

## MCP Server Discovery

Q: When three MCP servers are configured, which one's tools are available?

A: All of them — tools from every configured server are discovered at connection time and available simultaneously. There is no "active server."

Domain: D2

Example: With GitHub, Jira, and Slack MCP servers configured, the agent can call `github.create_pr`, `jira.create_issue`, and `slack.post_message` all in the same session without switching between them.

## MCP Resources

Q: What are MCP resources for?

A: Exposing content catalogs (issue summaries, doc hierarchies, schemas) so agents see available data without exploratory tool calls.

Domain: D2

Example: An MCP resource lists all open Jira issues with titles and IDs up front, so the agent can pick "PROJ-142" directly instead of first calling a search tool to discover what issues exist.

## Community vs Custom MCP

Q: Standard integration like Jira — build or reuse?

A: Use an existing community MCP server; reserve custom servers for team-specific workflows.

Domain: D2

Example: For Jira, install the existing community Jira MCP server rather than writing a custom one from scratch; save custom server effort for something like your company's internal deployment-approval tool that has no off-the-shelf integration.

## CLAUDE.md Hierarchy

Q: Why doesn't a teammate get standards stored in your `~/.claude/CLAUDE.md`?

A: User-level config applies only to your account and isn't in version control. Team standards belong in a project-level CLAUDE.md in the repo.

Domain: D3

Example: You add "always use tabs, not spaces" to `~/.claude/CLAUDE.md` on your own machine; a teammate cloning the repo never sees that rule because it never made it into the repo's own `CLAUDE.md`.

## @import

Q: How do you keep a monorepo CLAUDE.md modular?

A: Each package's CLAUDE.md uses `@import` to include only the standards files relevant to that package.

Domain: D3

Example: `packages/api/CLAUDE.md` contains `@import ../../standards/backend.md`, pulling in only the backend conventions instead of duplicating the whole monorepo's shared standards doc inline.

## Path-Scoped Rules

Q: Conventions must apply to test files scattered across every directory. Mechanism?

A: A `.claude/rules/` file with YAML frontmatter `paths: ["**/*.test.tsx"]` — loads only when editing matching files. Directory CLAUDE.md can't follow scattered files.

Domain: D3

Example: `.claude/rules/testing.md` has frontmatter `paths: ["**/*.test.tsx"]` and body "always use `screen.getByRole` over `getByTestId`" — it loads automatically whenever any test file anywhere in the repo is opened.

## Rules vs Directory CLAUDE.md

Q: When is a directory-level CLAUDE.md better than a path-scoped rule?

A: When conventions apply to one self-contained subtree; use `paths:` globs when they span directories.

Domain: D3

Example: `packages/payments/CLAUDE.md` documenting payments-specific conventions is right for that one subtree, but a rule for "how we write tests" that applies across `packages/*` needs a `paths:` glob instead.

## context: fork

Q: What does `context: fork` in skill frontmatter do?

A: Runs the skill in an isolated sub-agent context so verbose or exploratory output doesn't pollute the main conversation.

Domain: D3

Example: A "codebase-audit" skill with `context: fork` runs its dozens of grep and file-read calls in a forked context, and the main conversation only sees the final summary report.

## allowed-tools

Q: What does `allowed-tools` in skill frontmatter do?

A: Restricts which tools the skill may use during execution (least privilege, e.g., blocking destructive actions).

Domain: D3

Example: A "generate-changelog" skill sets `allowed-tools: [Read, Grep]` so it can never accidentally call `Write` or `Bash` to delete files while summarizing commits.

## argument-hint

Q: What does `argument-hint` in skill frontmatter do?

A: Prompts the developer for required parameters when the skill is invoked without arguments.

Domain: D3

Example: A "deploy" skill sets `argument-hint: "<environment>"`, so running `/deploy` with no argument prompts the developer to specify "staging" or "production" instead of failing silently.

## Skills vs CLAUDE.md

Q: Where do universal always-applied standards go vs on-demand workflows?

A: Always-applied → CLAUDE.md (always loaded). On-demand task workflows → skills.

Domain: D3

Example: "This repo uses 2-space indentation" belongs in CLAUDE.md since it applies to every edit, while "how to cut a release branch" belongs in a `/release` skill invoked only when actually releasing.

## Personal Skill Variant

Q: How do you customize a team skill without affecting teammates?

A: Create a personal variant in `~/.claude/skills/` under a different name.

Domain: D3

Example: The team's shared `/deploy` skill in the repo doesn't run your local Docker setup, so you create `~/.claude/skills/deploy-local.md` with your own steps, leaving the team's `/deploy` untouched.

## Explore Subagent

Q: What is the Explore subagent for?

A: Isolating verbose discovery output during codebase exploration, returning summaries to preserve main-conversation context.

Domain: D3

Example: Asked "where is the retry logic defined," the Explore subagent greps and reads a dozen files internally but reports back only "src/http/client.ts, lines 40-65," keeping the noisy search out of the main conversation.

## CI Non-Interactive

Q: A CI job running `claude "..."` hangs forever. Fix?

A: Add `-p` (`--print`) — non-interactive mode that prints the result and exits. (`CLAUDE_HEADLESS`, `--batch` are fake distractors.)

Domain: D3

Example: A GitHub Actions step running `claude -p "lint and report issues"` prints the results and exits cleanly, whereas the same command without `-p` would sit waiting for interactive input and time out the job.

## CI Structured Output

Q: How do you get schema-enforced machine-parseable output from Claude Code in CI?

A: `--output-format json` together with `--json-schema`.

Domain: D3

Example: `claude -p "review this PR" --output-format json --json-schema review.schema.json` returns a JSON object matching the schema (e.g. `{"approved": false, "issues": [...]}`) that a CI script can parse directly instead of scraping free-form text.

## CI Independent Review

Q: Why shouldn't the session that generated code also review it in CI?

A: It retains its own reasoning context and is less likely to question its decisions. Use a separate independent instance.

Domain: D3

Example: The session that wrote a caching layer, if asked to review its own PR, tends to rubber-stamp its own design choices; a fresh CI-triggered session with no memory of writing the code catches an unhandled cache-invalidation edge case instead.

## CI Re-Review Dedup

Q: How do you stop duplicate PR comments when re-reviewing after new commits?

A: Include prior review findings in context and instruct Claude to report only new or still-unaddressed issues.

Domain: D3

Example: The CI prompt includes "previous review flagged: missing null check on line 42 (now fixed), unused import on line 10 (still present)" and instructs Claude to post a comment only about the unused import, not to re-flag the already-fixed null check.

## Batches API Facts

Q: List the Message Batches API facts the exam tests.

A: 50% cost savings; up to 24-hour processing; no latency SLA; `custom_id` correlates request/response; no multi-turn tool calling within a request.

Domain: D4

Example: Submitting 5,000 support-ticket summarization requests as a batch with `custom_id: "ticket-4821"` on each costs half the normal API price, but results may not come back for hours, so it's unsuitable for a live chat widget.

## Batch Fit

Q: Which workloads belong on the Batches API?

A: Non-blocking, latency-tolerant work (overnight reports, weekly audits, nightly test generation). Never blocking flows like pre-merge checks.

Domain: D4

Example: A nightly job that generates a summary of the day's 10,000 log entries is a good fit for Batches; a pre-merge PR check that developers wait on before merging is not.

## Batch SLA Math

Q: Batches take up to 24h and your SLA is 30h from document arrival. Submission cadence?

A: Every 4 hours — worst case 4 + 24 = 28 ≤ 30. (Every 8 hours: 32 > 30, breach.)

Domain: D4

Example: A document arriving at 2:00pm waits at most until the 4:00pm submission window (4h wait) plus up to 24h processing, landing by 4:00pm the next day — well inside the 30h SLA.

## Batch Failures

Q: 40 of 900 batch items failed. What do you resubmit?

A: Only the failed items, identified by `custom_id`, modified as needed (e.g., chunk documents that exceeded context limits).

Domain: D4

Example: Item `custom_id: "doc-317"` failed because the document exceeded the context window, so it's split into two smaller chunks and resubmitted as `doc-317a` and `doc-317b`, while the 860 successful items are left alone.

## Batch Prep

Q: Before batch-processing 10,000 documents, what should you do?

A: Refine the prompt on a small sample set first to maximize first-pass success and avoid costly resubmission cycles.

Domain: D4

Example: Test the extraction prompt on 50 representative invoices, tune it until accuracy looks solid, and only then submit the full 10,000-invoice batch — rather than discovering a systemic prompt flaw after paying for all 10,000.

## Nullable Fields

Q: Why make schema fields optional/nullable when data may be absent?

A: Required fields pressure the model to fabricate values to satisfy the schema; nullable fields let it return null honestly.

Domain: D4

Example: A `middle_name` field marked required on an invoice-extraction schema causes the model to invent a middle name when the document has none; marking it nullable lets it return `null` instead.

## Enum Patterns

Q: How do you design enums for ambiguous and unforeseen categories?

A: Add `"unclear"` for ambiguous cases and `"other"` plus a detail string for extensible categories.

Domain: D4

Example: A `document_type` enum includes `"invoice"`, `"receipt"`, `"unclear"` (for a smudged scan that can't be classified), and `"other"` with a `detail: "shipping manifest"` field for a category the schema author didn't anticipate.

## Syntax vs Semantic

Q: What do strict JSON schemas via tool use eliminate — and not eliminate?

A: They eliminate syntax errors; they do not prevent semantic errors (values that don't sum, data in wrong fields). Validate semantics separately (e.g., `calculated_total` vs `stated_total`, `conflict_detected`).

Domain: D4

Example: A tool-use schema guarantees the model returns valid JSON with a numeric `total` field, but it can't stop the model from putting $120 in `total` when the line items actually sum to $150 — a separate check comparing `calculated_total` to `stated_total` catches that.

## Retry Limits

Q: When is retry-with-error-feedback useless?

A: When the required information is absent from the source document. Retries fix format/structural errors only.

Domain: D4

Example: Retrying extraction of a `contract_end_date` field ten times in a row won't help if the uploaded contract simply never states an end date — no amount of error-feedback prompting invents information that isn't in the document.

## detected_pattern

Q: What is a `detected_pattern` field on review findings for?

A: Tracking which code constructs trigger findings so dismissed findings can be analyzed for false-positive patterns.

Domain: D5

Example: A finding tagged `detected_pattern: "unused-variable-in-destructure"` gets dismissed by reviewers 40 times in a row, revealing that this specific pattern is a chronic false positive worth suppressing.

## Multi-Pass Review

Q: A 14-file PR review is inconsistent and contradictory. Restructure how?

A: Per-file passes for local issues plus a separate cross-file integration pass — fixes attention dilution.

Domain: D5

Example: Instead of one pass reviewing all 14 changed files at once (where it misses that `api/routes.ts` calls a function renamed in `api/handlers.ts`), run one pass per file for local style/logic issues, then a dedicated pass that checks cross-file consistency like renamed function calls.

## Case Facts Block

Q: After summarization the agent quotes "around $80" instead of $83.47. Fix?

A: Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block included in every prompt outside summarized history.

Domain: D5

Example: A case-facts block reading `refund_amount: $83.47, order_id: ORD-9921, status: pending` is appended to every prompt verbatim, so summarization of the surrounding conversation can't blur the exact dollar figure into "around $80."

## Lost in the Middle

Q: How do you mitigate position effects in long aggregated inputs?

A: Put a key-findings summary at the beginning and organize detail under explicit section headers; models attend best to the start and end.

Domain: D5

Example: A 40-page aggregated research report opens with a "Key Findings" bullet list, then organizes the rest under headers like "## Market Size," "## Competitors," rather than dumping all the raw source text in one undifferentiated block.

## Tool Output Trimming

Q: Order lookups return 40+ fields but 5 matter. What do you do?

A: Trim tool outputs to relevant fields before they accumulate in context.

Domain: D5

Example: Instead of feeding the full 40-field `get_order` response into context, the agent extracts just `{status, total, ship_date, tracking_number, item_count}` before continuing the conversation.

## Escalation Triggers

Q: Name the three valid escalation triggers.

A: Explicit customer request for a human (honor immediately), policy gap/exception (policy silent or ambiguous), and inability to make meaningful progress.

Domain: D1

Example: A customer asks for a refund on a product category the return policy doesn't mention at all — that's a policy gap, so the agent escalates rather than guessing an answer.

## Explicit Human Request

Q: Customer demands a human for a case the agent could easily solve. What happens?

A: Escalate immediately with a structured handoff — do not investigate first. (If merely frustrated but not demanding a human: acknowledge, offer to resolve, escalate if they reiterate.)

Domain: D1

Example: A customer says "just get me a human, I don't want to explain this again" about a simple password reset — the agent hands off immediately with a summary of the account and issue, rather than resetting the password itself first.

## Bad Escalation Proxies

Q: Why not escalate based on sentiment or the agent's self-reported confidence?

A: Neither correlates with actual case complexity; self-reported confidence is poorly calibrated.

Domain: D1

Example: An angry-sounding but simple "where's my package" question shouldn't auto-escalate on sentiment alone, and an agent saying "I'm 95% confident" on a case it's actually getting wrong shouldn't be trusted to skip escalation.

## Multiple Matches

Q: `get_customer` returns three matching customers. What should the agent do?

A: Ask the customer for additional identifiers. Never select heuristically.

Domain: D1

Example: `get_customer(name: "John Smith")` returns three different John Smiths, so the agent asks "can you confirm your email or the last 4 digits of your account number?" instead of picking the first result in the list.

## Error Propagation

Q: What should a failing subagent return so the coordinator can recover?

A: Structured context: failure type, attempted query, partial results, and potential alternative approaches.

Domain: D1

Example: `{"failure": "rate_limited", "query": "search competitors pricing", "partial_results": ["Company A: $29/mo"], "alternative": "retry after 60s or query a cached snapshot"}` gives the coordinator enough to decide how to proceed.

## Propagation Anti-Patterns

Q: Name three error-propagation anti-patterns.

A: Generic statuses ("search unavailable"), silent suppression (failure returned as empty success), and terminating the whole workflow on a single failure.

Domain: D1

Example: A search subagent that hit a timeout returns `{"status": "success", "results": []}` instead of reporting the timeout — the coordinator wrongly concludes there's simply nothing to find, and worse, some coordinators would abort the entire research task over that one failed subagent.

## Scratchpads & Manifests

Q: How do agents survive context degradation and crashes in long explorations?

A: Scratchpad files recording key findings (referenced for later questions); structured state exports/manifests the coordinator loads on resume; phase summaries injected into the next phase.

Domain: D5

Example: During a multi-hour codebase migration, the agent writes `progress-manifest.json` after each phase listing files converted so far; if the session crashes, resuming reloads the manifest and continues from the last completed phase instead of starting over.

## Confidence Calibration

Q: How are confidence scores made trustworthy for routing review?

A: Have the model output field-level confidence, then calibrate thresholds against labeled validation sets.

Domain: D5

Example: The model tags `invoice_total: {value: 483.20, confidence: 0.92}`; a threshold of 0.85 for auto-approval is chosen only after checking on 500 hand-labeled invoices that 0.85+ scores are actually correct over 99% of the time.

## Stratified Sampling

Q: Why keep sampling high-confidence extractions after automating them?

A: Stratified random sampling measures the residual error rate and detects novel error patterns that confidence scores miss.

Domain: D5

Example: Even after auto-approving all extractions scored above 0.9 confidence, a weekly sample of 100 of those "high-confidence" extractions is manually checked and turns up a new failure mode — the model confidently mis-extracting dates from a newly introduced invoice template.

## Accuracy Segmentation

Q: Aggregate extraction accuracy is 97%. Why can't you cut human review yet?

A: Aggregates can mask poor performance on specific document types or fields — validate accuracy per segment first.

Domain: D5

Example: Overall accuracy is 97%, but broken down by document type, handwritten receipts score only 78% while typed invoices score 99% — cutting human review across the board would let most handwritten-receipt errors slip through unnoticed.

## Claim-Source Mappings

Q: How does source attribution survive multi-agent synthesis?

A: Subagents output structured claim-source mappings (URL, document, excerpt, date) that downstream agents must preserve and merge.

Domain: D5

Example: The synthesis agent merges research from three subagents but keeps each claim tagged with its origin, so the final report can still say "per TechCrunch (2025-11-02): valuation reached $2B" instead of a bare, unattributed sentence.

## Conflicting Statistics

Q: Two credible sources report different figures. What does synthesis do?

A: Includes both values annotated with their sources (and dates); never averages, drops, or arbitrarily picks one. Reports separate well-established from contested findings.

Domain: D5

Example: Reuters (2025-08) reports 12,000 employees while the company's own site (2025-10) reports 11,200 — the synthesis states both figures with their sources and dates rather than averaging them to 11,600.

## Temporal Data

Q: Why require publication/collection dates in subagent outputs?

A: So temporal differences aren't misread as contradictions.

Domain: D5

Example: A source dated January says the company has 200 employees and one dated June says 350 — with dates attached, this reads as normal growth over time rather than a contradiction between two disagreeing sources.

## Coverage Annotations

Q: Some sources were unreachable during research. How does the report handle it?

A: Structure the synthesis with coverage annotations — which findings are well-supported and which topic areas have gaps due to unavailable sources.

Domain: D5

Example: The report notes "financials: well-supported by three sources" alongside "leadership team: coverage gap — the company's About page was unreachable during research" instead of silently omitting the leadership section as if it were never relevant.

## Content-Type Rendering

Q: How should synthesis render mixed content types?

A: Appropriately per type — financial data as tables, news as prose, technical findings as structured lists — not one uniform format.

Domain: D4

Example: A synthesis report renders quarterly revenue figures as a markdown table, summarizes a product-launch news story as a short paragraph, and lists API rate-limit specs as bullet points rather than forcing all three into the same paragraph style.

## Orchestrator-Worker Pattern

Q: A support-ticket system needs one component to decide which specialist (billing, technical, refunds) handles each ticket and to assemble the final reply. Which orchestration pattern fits, and what is the key architectural constraint?

A: Orchestrator-worker: a central orchestrator dispatches tasks to specialized worker agents and synthesizes their results. The constraint is that workers should not need to communicate with each other directly — all coordination and state flow through the orchestrator.

Domain: D1

Example: The orchestrator classifies a ticket as "refund," invokes the refund-policy worker, receives its answer, and composes the customer-facing reply itself rather than having the refund worker draft the reply.

## Evaluator-Optimizer Pattern

Q: A code-generation agent produces a function, then a second agent critiques it against a spec, and the first agent revises until the critique passes or a retry cap is hit. What pattern is this, and when is it worth the extra cost?

A: This is the evaluator-optimizer pattern: one agent generates, another evaluates against explicit criteria, and the loop repeats until acceptance. It is worth the cost when quality has clear, checkable criteria and the task tolerates extra latency and tokens for higher reliability.

Domain: D1

Example: A "generator" agent writes SQL, an "evaluator" agent runs EXPLAIN and checks it against forbidden-operation rules, and rejected queries are sent back with the evaluator's feedback for another pass.

## Planner-Executor Split

Q: Why separate a "planner" agent that produces a step list from an "executor" agent that carries out each step, rather than letting one agent both plan and act?

A: Splitting planning from execution lets the plan be inspected, validated, or approved before any side-effecting action runs, and lets the executor use a smaller, cheaper model since it only needs to follow instructions rather than reason about strategy.

Domain: D1

Example: The planner outputs "1) look up account, 2) verify balance, 3) issue refund," a human or policy check approves the plan, and only then does the executor call the refund tool.

## Supervisor/Manager Pattern

Q: How does a supervisor pattern differ from a plain orchestrator-worker pattern when a worker's output looks wrong?

A: A supervisor actively monitors worker output quality and can intervene mid-run — reassigning work, requesting a redo, or escalating — rather than just dispatching tasks and passing results through unchecked.

Domain: D1

Example: A supervisor agent notices the "summarize" worker returned an empty string, and instead of forwarding that to the next stage, it retries the worker with a clarified prompt.

## Blackboard Pattern

Q: Several loosely related agents (a pricing agent, an inventory agent, a shipping agent) each need to read and contribute partial findings without waiting on each other in a fixed order. What coordination pattern fits, and what's its main risk?

A: The blackboard pattern: agents read and write to a shared data store ("blackboard") opportunistically, and a controller decides when enough has accumulated to proceed. The main risk is write conflicts and unclear provenance — without discipline it's hard to tell which agent asserted what, or to resolve contradictory writes.

Domain: D1

Example: The pricing and inventory agents both write to a shared "quote" object; the shipping agent only fires once both fields are populated, without any agent calling another directly.

## Agent Handoff

Q: In a customer-service system, a triage agent determines a request needs legal review and transfers the conversation to a legal-specialist agent. What must the handoff include to avoid the specialist re-deriving context from scratch?

A: The handoff must carry forward the relevant conversation history, the reason for the transfer, and any state already gathered — not just a bare pointer to "continue this conversation," or the specialist will burn tokens and turns rebuilding context or ask the user to repeat themselves.

Domain: D1

Example: The triage agent hands off with a structured summary — "user disputes a charge, refund already denied once, escalation requested" — instead of just forwarding the raw chat log for the specialist to re-read and reinterpret.

## Agent-to-Agent Communication Format

Q: When two agents in a pipeline exchange results, why prefer a structured schema (e.g., JSON with defined fields) over passing free-text natural language between them?

A: Structured formats are machine-parseable and validate reliably, letting the receiving agent programmatically check for missing or malformed fields; free text forces the receiver to re-interpret prose, which is fragile and can silently drop or misread information.

Domain: D1

Example: A "research" agent returns `{"claim": "...", "source_url": "...", "confidence": 0.8}` instead of a paragraph the next agent has to parse for the same facts.

## Fan-Out/Fan-In Decomposition

Q: A document-review task needs to check ten independent sections against ten independent style rules. How should this be decomposed for orchestration, and what does the "fan-in" step require?

A: Fan out one subagent per section (or per section-rule pair) to run in parallel, then fan in by aggregating all results in the orchestrator. Fan-in requires the orchestrator to wait for all branches (or apply a timeout/partial-result policy) and reconcile results that may arrive out of order or with different formats.

Domain: D1

Example: Ten section-review subagents run concurrently; the orchestrator collects all ten JSON verdicts, and if two of them time out, it decides whether to retry, mark them "unreviewed," or fail the whole batch.

## Task Decomposition Granularity

Q: An architect is deciding whether to split a "generate a project status report" task into one large subagent or a dozen fine-grained subagents (one per data source). What tradeoff governs this choice?

A: Coarse-grained subagents cut coordination overhead and context-passing cost but reduce parallelism and make failures harder to isolate; fine-grained subagents parallelize well and isolate failures but multiply orchestration overhead, prompt/token cost, and the number of handoff points that can go wrong.

Domain: D1

Example: One subagent per data source lets a failed "finance API" fetch be retried alone without redoing the whole report, at the cost of ten separate agent invocations instead of one.

## Orchestration Framework vs Hand-Rolled Loop

Q: A team is building a multi-agent workflow and is deciding between adopting an orchestration framework versus writing their own control loop around the model API. What should drive that decision?

A: Choose a framework when the system needs common infrastructure the framework already solves well — retries, state persistence, tracing, parallel dispatch — and the team's workflow fits its abstractions; hand-roll a loop when requirements are simple enough that the framework's abstractions add more indirection and lock-in than they save.

Domain: D1

Example: A two-step "fetch then summarize" pipeline is simpler as a hand-rolled loop, while a system needing durable long-running multi-agent state across restarts benefits from a framework that already persists that state.

## Streaming Orchestration Output

Q: In a multi-agent pipeline where a user is waiting on the final answer, why might an architect stream intermediate subagent output to the UI rather than only streaming the final synthesis step?

A: Streaming intermediate progress (e.g., "searching," "found 3 sources," "drafting") gives the user feedback during long multi-step runs and surfaces partial results if a later step fails, at the cost of exposing in-progress reasoning that may later be revised or discarded.

Domain: D1

Example: A research pipeline streams each subagent's "now checking source X" status line to the UI while the final synthesis subagent is still running.

## Agent Memory Architecture: Short-Term vs Long-Term

Q: An architect is designing memory for a multi-turn agent that runs many sessions with the same user over weeks. How should short-term and long-term memory differ in scope and storage?

A: Short-term memory is the in-context conversation/task state for the current run and disappears when the session ends; long-term memory is durable, persisted outside the context window (a database, vector store, or file) and is selectively retrieved back into context in future sessions.

Domain: D1

Example: The current conversation's tool outputs live in context as short-term memory, while a summarized "user prefers metric units" fact is written to a persistent store so it can be recalled in next week's session.

## Context-Window Budgeting Across Subagents

Q: An orchestrator dispatches five subagents, each of which could return a large amount of output. Why is context-window budgeting a distinct architectural concern from simply giving each subagent enough tokens to do its job?

A: Every subagent's raw output that gets passed back into the orchestrator's context, or forwarded into a downstream agent's context, consumes that recipient's window too — so budgeting must account for the cumulative cost of aggregation, not just each subagent's individual task size, or the orchestrator can blow its own context limit synthesizing results.

Domain: D1

Example: Each of five subagents is capped at returning a 200-token summary rather than its full 5,000-token working output, so the orchestrator's synthesis step stays within budget.

## Trust Boundaries Between Agents

Q: A workflow includes an internally-trusted "planner" agent and a "web-research" agent that ingests untrusted third-party content. How should the architecture treat output crossing from the research agent into the planner?

A: Treat the research agent's output as untrusted input at a trust boundary — sanitize or clearly delimit it, and never let content it retrieved be interpreted as instructions to the planner, since it may contain injected prompts from the pages it fetched.

Domain: D1

Example: The research agent's fetched page content is wrapped in clearly labeled data tags before being passed to the planner, so an embedded "ignore previous instructions" string in the page is treated as data, not a command.

## Retry/Backoff at the Orchestrator Level

Q: A worker subagent call fails with a transient tool error. Should the retry logic live inside the worker subagent's own prompt/loop, or at the orchestrator level?

A: Generally at the orchestrator level, with exponential backoff — the orchestrator can decide whether to retry the same worker, reroute to a fallback, or fail the whole task, and it can apply a consistent policy across all workers rather than duplicating retry logic in every subagent.

Domain: D1

Example: The orchestrator catches a rate-limit error from a worker's tool call, waits with exponential backoff, and retries the worker invocation up to three times before marking that branch failed.

## Circuit Breakers in Agentic Systems

Q: A tool an agent depends on starts failing repeatedly mid-run. What architectural mechanism prevents the agent from continuing to hammer that tool on every subsequent turn, and why is it needed beyond simple retries?

A: A circuit breaker: after a failure threshold, the orchestrator stops calling that tool/agent for a cooldown period and either fails fast or routes to a fallback. It's needed beyond retries because retries alone keep re-attempting a persistently broken dependency, wasting turns, tokens, and latency instead of failing fast.

Domain: D1

Example: After three consecutive failures calling the inventory API, the orchestrator "opens the circuit" and returns a cached fallback response for the next two minutes instead of calling the API again.

## Idempotent Agent Actions

Q: An orchestrator retries a subagent step after a timeout, but the step had actually already completed and issued a payment before the timeout was reported. What design principle prevents this from double-charging?

A: Actions with side effects should be idempotent — designed so repeating the same action with the same identifier produces the same result rather than a duplicate effect, typically via an idempotency key or a check-before-act pattern.

Domain: D1

Example: The "charge customer" tool call includes an idempotency key tied to the order ID, so a retried call with the same key is recognized as a duplicate and not billed twice.

## Agent Versioning and Rollback

Q: A production multi-agent system updates one subagent's prompt and it starts producing worse results. What architectural practice limits the blast radius and allows fast recovery?

A: Version subagent prompts/configs independently (not as one monolithic bundle), deploy changes incrementally with the ability to route traffic back to the previous version, and monitor per-version metrics so a regression can be rolled back for just the affected subagent.

Domain: D1

Example: The "summarizer" subagent's prompt is versioned separately from the orchestrator; when v3's summaries regress in quality, traffic is rolled back to v2 for that subagent without touching the rest of the pipeline.

## Observability and Tracing Across a Multi-Agent Run

Q: A multi-agent pipeline produces a wrong final answer, and the team cannot tell which of six subagent calls introduced the error. What should have been in place?

A: End-to-end tracing that assigns a correlation/trace ID to the whole run and logs each subagent's inputs, outputs, tool calls, and latency as spans under that ID, so any run can be replayed and inspected step by step after the fact.

Domain: D1

Example: A trace viewer shows the full run as a tree: orchestrator span, five worker spans each with their tool calls, and one worker's span reveals it received a malformed input from the fan-out step.

## Cyclic vs Acyclic Agent Graphs

Q: An architect is choosing between modeling a workflow as a directed acyclic graph (DAG) of agents versus a graph that allows cycles (e.g., an evaluator sending work back to a generator). What does allowing cycles buy, and what does it cost?

A: Cycles enable iterative refinement loops (generate-critique-revise) that a DAG cannot express, but they remove the guarantee of termination — the architecture must add explicit loop limits or exit conditions, since the graph structure itself no longer bounds the number of steps.

Domain: D1

Example: A DAG pipeline (fetch → transform → report) always finishes in a fixed number of steps, while a generator-evaluator cycle needs an explicit "max 3 revision passes" cap to avoid looping indefinitely.

## Choosing Orchestration Granularity

Q: A team is deciding whether to give the orchestrator fine-grained control (approving every individual tool call a worker makes) or coarse-grained control (dispatching a worker and only reviewing its final output). What should drive that choice?

A: Drive it by the risk and reversibility of the actions involved: high-stakes or irreversible actions (payments, deletions, external communications) warrant fine-grained orchestrator oversight of individual steps, while low-risk, easily-reversible or read-only work can run coarse-grained with only final-output review to save latency and cost.

Domain: D1

Example: A worker reading internal documentation runs autonomously end to end, while a worker capable of sending customer emails has each send call routed through the orchestrator for approval first.

## Statelessness vs Statefulness of Orchestrator State

Q: A long-running multi-agent workflow needs to survive a process restart partway through. Should the orchestrator keep its in-progress state only in memory, or externalize it?

A: Externalize orchestrator state (task progress, which subagents have completed, intermediate results) to durable storage so a restart can resume from the last checkpoint; keeping state only in process memory means any crash or redeploy loses the entire in-progress run.

Domain: D1

Example: After completing worker 3 of 5, the orchestrator persists "steps 1-3 done, results attached" to a database; if the process restarts, it resumes at worker 4 instead of restarting the whole workflow.

## Agent Handoff Failure Mode

Q: A triage agent hands off to a specialist agent, but the specialist's response contradicts a decision the triage agent already made and communicated to the user. What architectural safeguard prevents this from reaching the user as a visible inconsistency?

A: The orchestrator (or a supervisor step) should reconcile handoff outputs against prior decisions before they reach the user — either by giving downstream agents visibility into prior commitments, or by validating specialist output against the conversation history before sending it onward.

Domain: D1

Example: The specialist agent recommends a refund the triage agent already told the customer was denied; a reconciliation check catches the contradiction and routes it to a human rather than sending the conflicting reply.

## Agentic-Loop Termination Conditions

Q: When architecting an autonomous agent loop, what termination conditions should be defined besides "task complete"?

A: The loop must terminate on max iteration count, max wall-clock time, max token/cost budget, and repeated-failure detection (e.g., the same error N times in a row), not only on a success signal. Relying solely on the model deciding it is "done" risks the loop never exiting on ambiguous or unsolvable tasks.

Domain: D1

Example: A code-fixing agent stops after 15 tool calls even if tests still fail, surfacing a partial result instead of looping indefinitely.

## Runaway-Loop Prevention

Q: An agent keeps calling the same tool with slightly different arguments after each failed attempt, burning budget with no progress. What architectural control prevents this?

A: A loop-detection guard that tracks recent tool calls (or their hashes) and halts or escalates when the same call, or a near-identical one, repeats beyond a threshold without state change. This is distinct from a raw step limit because it catches wasteful cycling before the budget is exhausted.

Domain: D1

Example: The orchestrator flags the run for human review after the same API call fails three times with only cosmetic argument changes.

## Step and Budget Limits

Q: Why should step limits and cost/token budgets be enforced at the orchestration layer rather than left to the model's own judgment?

A: The model cannot reliably self-limit because it lacks a ground-truth view of cumulative cost or elapsed steps across the run; the orchestrator holds that state and can hard-stop deterministically when a cap is hit. This turns an unbounded cost risk into a bounded, predictable one.

Domain: D1

Example: The harness tracks total tokens spent across all subagent calls and aborts the workflow once it crosses a configured ceiling, regardless of what the model reports.

## Human-in-the-Loop Checkpoint Placement

Q: Where in an agentic workflow should human-in-the-loop checkpoints be placed for best cost/safety tradeoff?

A: Checkpoints belong at points of irreversibility or high blast radius (before an action that is hard to undo, before crossing a trust boundary, or before committing to a plan that will drive many downstream steps) rather than after every individual tool call, which creates review fatigue and slows the system without adding proportional safety.

Domain: D1

Example: A deployment agent asks for approval before running `terraform apply` but not before read-only `terraform plan` calls.

## Approval Gates for High-Risk Actions

Q: How should an architecture distinguish actions that require synchronous human approval from actions an agent can take autonomously?

A: Classify tools/actions by risk tier (e.g., reversible+low-impact, reversible+high-impact, irreversible) at design time, and route only the irreversible or high-impact tier through a blocking approval gate; lower tiers proceed autonomously but remain logged. Hardcoding the gate into the tool layer (not just prompting the model to "ask first") ensures it cannot be bypassed by a persuaded or jailbroken model.

Domain: D1

Example: A `delete_production_table` tool is wired so the call itself pauses and waits on an external approval webhook, independent of what the model's reasoning concluded.

## Sandboxing Agent Tool Execution

Q: Why should agent-executed code or shell commands run inside a sandbox rather than directly on the host system?

A: Sandboxing (containers, VMs, or restricted execution environments) contains the blast radius of a mistaken or adversarially-induced action, limiting filesystem, network, and process access so a bad tool call can't compromise the broader system. It is a containment control, complementary to prompting the model to "be careful."

Domain: D1

Example: A coding agent's shell tool runs inside an ephemeral container with no access to the host's credentials store or production network.

## Least-Privilege Tool Scoping

Q: At the architecture level, how should tool access be scoped for an agent versus scoping access for the human who deployed it?

A: Each agent (or subagent role) should be granted only the specific tools, API scopes, and data access it needs for its narrow task, issued per-session or per-role rather than inheriting the deploying user's full permission set. This limits damage from both model error and prompt injection, since a compromised agent can only do what its own scoped credentials allow.

Domain: D1

Example: A read-only research subagent gets a search-tool credential with no write access, even though the orchestrating user has full admin rights.

## Rollback and Compensating Actions

Q: What is a compensating action, and why does an agentic architecture need it even when actions aren't technically transactional?

A: A compensating action is an explicit inverse or corrective step (e.g., a refund, a delete, a revert commit) that the architecture can invoke when a multi-step agent run fails partway through, since agent workflows typically can't rely on database-style atomic rollback across external side effects. Designing compensating actions alongside each risky tool means partial failures leave the system in a recoverable state instead of a corrupted one.

Domain: D1

Example: If step 3 of a 5-step order-processing agent fails, a `cancel_reservation` compensating action undoes the reservation made in step 1.

## Agent Self-Correction vs. External Verification

Q: Why is an agent re-checking its own work not a substitute for external verification?

A: Self-correction reuses the same model, context, and blind spots that produced the original error, so it catches only errors the model is capable of noticing about itself; external verification (a separate check, a test suite, a different model, a human) has independent failure modes and catches classes of error self-review structurally cannot. Robust architectures use both, treating self-correction as cheap first-pass filtering, not the safety boundary.

Domain: D1

Example: An agent's own "let me double check this SQL" pass misses a subtle logic bug that a separate automated test suite catches immediately.

## Confidence Thresholds for Autonomous Action

Q: How can an agentic system use confidence signals to decide when to act autonomously versus escalate?

A: Define an explicit threshold (derived from model-reported certainty, retrieval match quality, or task classification) below which the action routes to human review or a safer fallback instead of executing directly. The threshold must be calibrated against real outcome data, since a model's stated confidence is not inherently well-calibrated to actual correctness.

Domain: D1

Example: A support agent auto-resolves tickets only when its intent-classification confidence exceeds 90%; anything lower routes to a human agent.

## Audit-Logging Requirements for Agentic Systems

Q: What must an audit log capture for an agentic system to support incident investigation, beyond just the final output?

A: Every tool call with its full arguments and result, the reasoning/plan that led to it, timestamps, the identity/credentials used, and any human approvals or overrides in the chain — enough to reconstruct exactly what the agent did and why, not just what it produced. This is what lets an architect distinguish a model reasoning failure from a tool failure from a human override after the fact.

Domain: D1

Example: When a customer disputes an automated refund, the audit log shows the exact tool call, its inputs, and the approval step that authorized it.

## Deterministic Guardrails vs. Prompted Guardrails

Q: What's the architectural difference between a "deterministic" guardrail and a "prompted" guardrail, and why does it matter for high-stakes actions?

A: A prompted guardrail is an instruction in the system prompt ("never delete without confirmation") that the model can still fail to follow under adversarial input or reasoning drift; a deterministic guardrail is enforced in code outside the model's control (a permission check, a schema validator, a hard-coded approval gate) that cannot be talked around. High-stakes actions should be protected by deterministic guardrails, with prompted guardrails as a defense-in-depth layer, not the only layer.

Domain: D1

Example: Instead of just telling the model "don't exceed a $500 spend," the payment tool itself rejects any transaction request above $500 regardless of what the model sends.

## Rate-Limiting Agent Actions

Q: Why should an agent's outbound tool calls be rate-limited independently of any per-run step budget?

A: Rate limiting caps the velocity of actions over time (e.g., API calls per minute), protecting downstream systems from being overwhelmed and containing the damage rate of a misbehaving loop, whereas a step budget only caps total count over the whole run and doesn't prevent a burst. The two controls address different failure modes and are typically both needed.

Domain: D1

Example: An agent's email-sending tool is capped at 5 sends per minute even though its overall run budget allows 200 tool calls.

## Idempotency Keys for Agent Actions

Q: Why do side-effecting tool calls in an agentic architecture need idempotency keys?

A: Agent loops routinely retry failed or timed-out calls (due to network errors, ambiguous results, or the model itself re-issuing a call), so without an idempotency key a retried "create order" or "send payment" call can execute the side effect twice. An idempotency key lets the downstream system recognize and safely no-op a duplicate request.

Domain: D1

Example: A `charge_card` tool call includes a unique idempotency key per logical transaction so a retried call after a timeout doesn't double-charge the customer.

## Failure Isolation Between Subagents

Q: In a multi-agent architecture, how should a failure in one subagent be prevented from taking down the whole workflow?

A: Each subagent should run in its own isolated execution context (separate process/context window, own error boundary) with failures reported as structured results to the orchestrator rather than propagating as an uncaught exception through shared state. The orchestrator then decides whether to retry, degrade, or abort based on which subagent failed and how critical it was.

Domain: D1

Example: A research subagent that crashes fetching one source returns a partial-failure status; the orchestrator continues with the other three subagents' results instead of aborting the whole report.

## Graceful-Degradation Strategies

Q: What does graceful degradation look like for an agentic system when a required tool or dependency becomes unavailable mid-run?

A: The system falls back to a reduced-capability mode — cached data, a simpler heuristic, or a partial answer flagged as incomplete — rather than failing the entire task outright, and it makes the degradation visible to the user or downstream consumer instead of silently returning lower-quality output as if it were complete.

Domain: D1

Example: When a live pricing API is down, a shopping agent returns results with a "prices may be stale, last updated 2 hours ago" notice instead of erroring out entirely.

## Timeout Design for Long-Running Agent Tasks

Q: Why is a single global timeout usually insufficient for a long-running agentic task, and what should replace it?

A: A single global timeout either kills legitimate long-running work too early or lets a stuck sub-step run far too long before the global limit finally fires; better designs layer per-step timeouts (catching a hung tool call quickly) with an overall budget (catching runaway total duration), plus progress checks that detect "no forward progress" distinct from "still working."

Domain: D1

Example: An agent's web-scraping tool call times out after 30 seconds per request, while the overall research task has a separate 20-minute ceiling.

## Agent State Persistence Across Restarts

Q: Why must an agentic architecture persist run state externally rather than keeping it only in the running process's memory?

A: If the orchestrating process crashes, gets redeployed, or is killed mid-run, in-memory-only state is lost and the task must restart from scratch, wasting the work already done and potentially leaving external side effects (like a partially completed multi-step transaction) in an unknown state. Persisting plan, progress, and intermediate results to durable storage lets the run be inspected and resumed.

Domain: D1

Example: A long-running document-generation agent checkpoints its outline and completed sections to a database after each step, so a server restart doesn't lose an hour of work.

## Resuming Interrupted Agent Runs

Q: What must an architecture verify before resuming an agent run from a persisted checkpoint, rather than just replaying from the saved state?

A: It must re-validate that the world hasn't changed in ways that invalidate the saved plan or partial results (stale data, a resource that was deleted, a since-expired approval) and re-check any external side effects for whether they actually completed, since a checkpoint saved "about to call X" doesn't guarantee X didn't already fire before the crash.

Domain: D1

Example: On resume, the agent re-queries whether the payment it was mid-way through actually posted before deciding whether to retry the charge.

## Concurrency Control for Shared Resources

Q: When multiple agents or subagents can act on the same shared resource concurrently, what architectural mechanism prevents conflicting writes?

A: A concurrency control mechanism such as optimistic locking (version checks that reject a stale write) or pessimistic locking (an explicit lock acquired before mutation) at the resource layer, so simultaneous agent actions can't silently overwrite each other's changes. This must live in the resource/data layer, not in agent instructions, since the model has no visibility into other agents' concurrent activity.

Domain: D1

Example: Two subagents updating the same customer record use optimistic concurrency (a version field) so the second writer's update is rejected and retried against fresh data instead of clobbering the first.

## Race-Condition Prevention in Parallel Subagents

Q: Two subagents running in parallel both read a shared counter, increment it, and write it back. What race condition results, and how should the architecture prevent it?

A: Both subagents may read the same initial value before either writes, so one increment is lost (a classic read-modify-write race), producing a counter that's too low. The fix is to make the increment atomic at the resource layer (a database atomic increment or a transaction) rather than having each agent do a separate read-then-write, which cannot be made safe purely by sequencing agent instructions.

Domain: D1

Example: Instead of each subagent reading, adding one, and writing a shared inventory count, they each call an atomic `DECREMENT stock WHERE id=X AND stock>0` operation.

## Kill-Switch Design

Q: What properties must a kill switch for an autonomous agent system have to be trustworthy in an incident?

A: It must operate outside the agent's own control path (the agent cannot disable or ignore it), take effect immediately without depending on the agent reaching a natural checkpoint, and be reachable by an operator through a path independent of the primary system in case that system itself is the thing misbehaving. A kill switch implemented as "tell the agent to stop" via the same channel it's misusing is not a real kill switch.

Domain: D1

Example: An ops team can revoke an agent's API credentials at the gateway level, halting all its tool calls immediately, without needing the agent process itself to cooperate.

## Agent Identity and Authentication in Multi-Agent Systems

Q: In a multi-agent architecture, why does each agent need its own distinct identity and credentials rather than all agents sharing one service account?

A: Distinct per-agent identity enables scoped least-privilege access, attributable audit logs (knowing which specific agent took which action), and the ability to revoke or rate-limit one agent's access without affecting the others. A shared service account collapses all of this: any compromised or misbehaving agent has the full combined blast radius, and logs can't distinguish which agent did what.

Domain: D1

Example: A code-review subagent and a deployment subagent authenticate with separate API tokens scoped to read-only-repo and deploy-only-staging respectively, so revoking one doesn't disable the other.


## Single-Agent Vs Multi-Agent Tradeoff

Q: A team wants to build a customer-support assistant that answers billing questions from one internal knowledge base. They propose a multi-agent architecture with a router, a retrieval agent, and a drafting agent. What should an architect push back on?

A: A single agent with a retrieval tool likely performs as well with far less latency, cost, and failure surface; multi-agent decomposition earns its overhead only when subtasks need different context windows, tools, or independent scaling, none of which apply here.

Domain: D1

Example: Splitting a one-KB-lookup Q&A flow into three agents adds two extra LLM round trips and two more places for context to be dropped, for no accuracy gain.

## Orchestration Overhead Threshold

Q: How should an architect decide whether the coordination cost of a multi-agent system is worth paying?

A: Compare the marginal accuracy or capability gain from decomposition against the added latency, token cost, and failure modes of inter-agent handoffs; if a single agent with more tools or a longer prompt achieves comparable results, orchestration overhead outweighs its benefit.

Domain: D1

Example: A document-review pipeline that gains 2% accuracy from a 4-agent pipeline but triples p95 latency is a case where the overhead isn't justified for a latency-sensitive product.

## Latency Budget Across Agent Hops

Q: A product has a 5-second end-to-end latency SLA and its design routes a request through a planner agent, two tool-calling agents, and a summarizer agent. How should an architect allocate the budget?

A: Assign each hop an explicit latency budget (including model inference, tool calls, and network overhead) that sums under the SLA with margin, and treat any hop exceeding its budget as a design defect to fix, not something to absorb elsewhere.

Domain: D1

Example: Budgeting 1s for planning, 1.5s per tool-agent, and 1s for summarization leaves 0s margin — a warning sign that one slow tool call will blow the SLA.

## Token-Cost Modeling For Agentic Systems

Q: Why is estimating cost for a multi-agent system based on a single "average request" token count usually wrong?

A: Cost in agentic systems scales with tokens per call multiplied by number of hops, and hops vary with tool-loop iterations, retries, and conversation history growth, so cost should be modeled as a distribution over hop counts, not a fixed multiplier.

Domain: D1

Example: A research agent that loops 3-8 times before finishing has an 8-hop worst case costing nearly 3x the 3-hop median, which a flat "average tokens x agents" estimate would miss.

## Synchronous Vs Asynchronous Agent Execution

Q: When should an agentic workflow be built to run asynchronously rather than block on a synchronous request-response call?

A: Use asynchronous execution when tasks can take minutes to hours, involve long-running tool calls, or don't need an immediate answer; synchronous execution suits interactive, user-facing turns where the caller is waiting live.

Domain: D1

Example: A chat assistant answering in-session uses synchronous calls, while a nightly report-generation agent that crawls dozens of documents should run async and notify on completion.

## Event-Driven Vs Polling Agent Architecture

Q: An agent needs to react when a new support ticket is created. What are the tradeoffs between an event-driven trigger and a polling loop?

A: Event-driven triggers (webhooks, queues) minimize latency and idle cost by invoking the agent only when work exists, while polling is simpler to implement but wastes compute and adds average latency equal to half the poll interval.

Domain: D1

Example: Polling a ticket queue every 60 seconds adds up to 60s of avoidable delay per ticket versus a queue subscription that invokes the agent within milliseconds of ticket creation.

## Observability Designed In From The Start

Q: Why should tracing and logging be part of the initial architecture of an agentic system rather than added after launch?

A: Agent behavior is non-deterministic and multi-step, so without structured traces of each prompt, tool call, and decision from day one, debugging a bad output after the fact is nearly impossible; retrofitting observability requires re-running failures that already happened.

Domain: D1

Example: Logging only the final answer means a wrong output caused by a tool call three steps earlier can't be diagnosed without reproducing the exact failure.

## Testing Strategies For Agentic Architectures

Q: How should an architect approach testing an agent that makes autonomous tool-use decisions, given that traditional unit tests can't cover open-ended reasoning?

A: Combine deterministic unit tests for individual tools and guardrails with scenario-based evaluations (a fixed set of representative tasks graded against rubrics or golden transcripts) and ongoing production sampling to catch drift.

Domain: D1

Example: Testing a coding agent means unit-testing its file-edit tool in isolation, plus running it against a suite of benchmark tasks and checking pass rates over time.

## Versioned Prompts And Tools In Production

Q: A production agent's system prompt and tool schema are edited directly in the deployment config without version control. What risk does this create?

A: Without versioning, there's no way to correlate a behavior change or regression with a specific prompt or tool-schema edit, no rollback path, and no way to run A/B comparisons between prompt versions.

Domain: D1

Example: A silent prompt edit that removes a safety instruction can't be traced back or reverted quickly if it isn't tagged with a version and deploy timestamp.

## Deployment Patterns For Agentic Services

Q: What deployment pattern reduces risk when rolling out a new version of an agent's prompt or tool set to production traffic?

A: Canary or shadow deployment — routing a small percentage of traffic (or a shadow copy of traffic with no user-facing effect) to the new version and comparing quality and error metrics before full rollout.

Domain: D1

Example: Shadowing 5% of support tickets to a new agent version and comparing resolution rates before promoting it avoids a blanket regression across all users.

## Scaling Agent Fleets

Q: What's the primary bottleneck to consider when scaling an agentic system from tens to thousands of concurrent agent sessions?

A: Downstream dependencies (model API rate limits, tool/API quotas, and shared state stores) typically become the bottleneck before compute does, so scaling requires rate-limit-aware queuing and backpressure, not just adding more workers.

Domain: D1

Example: Adding more agent worker instances doesn't help if they all compete for the same third-party API's 100-requests-per-minute limit.

## Multi-Tenant Agent Architecture Considerations

Q: What must an architect isolate when the same agentic service handles multiple customers (tenants)?

A: Tenant data must be isolated in retrieval, memory/session state, and tool access (so one tenant's documents or credentials can never leak into another's context), and usage/cost must be attributable per tenant.

Domain: D1

Example: A shared vector store queried without a tenant-ID filter can return Tenant A's confidential documents into Tenant B's agent context.

## Migration Path: Workflow To Agent

Q: A team has a reliable deterministic workflow (fixed steps, explicit branching) and wants to make it "agentic." What migration approach limits risk?

A: Migrate incrementally by replacing one well-scoped step at a time with agent-driven reasoning while keeping the surrounding steps deterministic, validating each swapped step against the original before proceeding, rather than rewriting the whole pipeline as an open-ended agent at once.

Domain: D1

Example: Replacing only the "classify document type" step with an LLM call while keeping upstream ingestion and downstream routing as fixed code limits blast radius if the classifier misbehaves.

## Migration Path: Agent To Workflow

Q: An agent-based system has stabilized into a fixed sequence of tool calls that never varies in production. What should an architect consider?

A: Convert the stable portion into an explicit deterministic workflow, since a fixed sequence no longer benefits from the agent's flexible reasoning but still pays its latency and cost overhead; reserve the agent for the genuinely variable decision points.

Domain: D1

Example: If an agent always calls "lookup customer" then "check balance" then "draft reply" in that order, hardcoding that sequence and using the agent only to draft the reply text cuts cost without losing capability.

## Agentic Architecture Anti-Pattern: Chatty Hops

Q: A multi-agent pipeline has each agent summarizing and re-passing the entire conversation history to the next agent at every hop. What anti-pattern is this and why does it matter?

A: This is context re-inflation, an anti-pattern where token cost and latency grow multiplicatively with hop count because each agent re-processes accumulated history; the fix is passing only the minimal structured data each downstream agent actually needs.

Domain: D1

Example: A 5-hop pipeline that forwards the full transcript at each step can see input token counts triple by the final hop compared to passing a condensed summary.

## Agentic Architecture Anti-Pattern: God Agent

Q: A team gives one agent dozens of tools spanning unrelated domains (billing, scheduling, code execution, email) and a single sprawling system prompt. What risk does this create?

A: This "god agent" anti-pattern degrades tool-selection accuracy as tool count grows, makes the system prompt hard to reason about or test, and couples unrelated failure domains together; splitting into narrower agents or tool subsets per domain, coordinated by a router, is more reliable.

Domain: D1

Example: An agent with 40 tools may pick the wrong one for an ambiguous request more often than a domain-scoped agent with 8 relevant tools would.

## Designing Fallback Paths For Agent Failure

Q: What should an architecture include for the case where an autonomous agent fails to complete a task or times out?

A: A defined fallback path — such as escalating to a human, returning a partial result with a clear failure state, or retrying with a simpler deterministic strategy — rather than surfacing a raw error or silently returning nothing.

Domain: D1

Example: If a research agent exceeds its tool-call budget without finishing, the system should return the best partial answer gathered so far plus a flag, not a blank response.

## Architecture Review Checklist For Agentic Systems

Q: Name three items an architecture review of a new agentic system should specifically check beyond standard service review items.

A: Whether latency/cost budgets per hop are defined, whether observability (tracing per step) is built in, and whether a fallback/escalation path exists for agent failure or low-confidence output.

Domain: D1

Example: A review that only checks API contracts and infra sizing but skips "what happens when the agent gets stuck in a tool loop" misses an agent-specific failure mode.

## Integrating Agents With Existing Microservices

Q: How should an agent that needs to call existing internal microservices be integrated, to avoid becoming a special-cased dependency?

A: Wrap existing service APIs as tool definitions with the same contracts, auth, and rate limits used by other callers, rather than granting the agent direct database or infra access; this keeps the agent a normal client of the service boundary.

Domain: D1

Example: An agent that needs order data should call the existing Orders API as a tool, not query the orders database directly, preserving the service's existing access controls and versioning.

## Agent Architecture And Compliance Touchpoints

Q: What compliance-relevant properties does an agentic architecture need to support that a simple stateless API often doesn't?

A: Auditable logs of what data the agent accessed and what actions it took (for regulations requiring explainability or data-access trails), and enforceable data-retention/deletion for any conversation or tool-call history the agent stores.

Domain: D1

Example: A financial-services agent that queries account data needs a retained, queryable log of which records it read and why, to satisfy audit requirements.

## Single Powerful Agent Vs Many Narrow Agents

Q: Under what conditions does a single agent with a broad toolset outperform decomposing into many narrow specialized agents?

A: When tasks are highly interdependent and benefit from shared context in one reasoning pass, a single agent avoids the information loss and latency of handoffs; narrow agents win when subtasks are independent, need different tool access scopes, or must scale separately.

Domain: D1

Example: A single agent drafting and then critiquing its own email in one context often beats a separate "writer agent" and "critic agent" needing to hand off the draft, since nothing is lost in the handoff.

## Adding A Coordinator Layer

Q: A system has three specialized agents that occasionally need to collaborate on tasks spanning their domains. When is it justified to add a coordinator (orchestrator) agent rather than having the agents call each other directly?

A: A coordinator is justified when task routing logic itself is non-trivial (requires judgment about which specialist(s) to invoke and in what order) or when specialists must not have direct dependencies on each other; if routing is a fixed rule, a simple deterministic router is cheaper than an LLM-based coordinator.

Domain: D1

Example: If which specialist handles a request depends on ambiguous natural-language intent, an LLM coordinator adds value; if it's just "route by ticket category field," a switch statement suffices.

## Session And Thread Boundaries In Multi-User Products

Q: What must an architect define explicitly for a multi-user agentic product regarding conversation state?

A: Clear session/thread boundaries determining what context persists across turns, when a session resets, and how concurrent sessions for the same user are isolated from each other, since unbounded context growth or cross-session bleed both cause failures.

Domain: D1

Example: A support-chat agent that never resets session context can eventually exceed the context window mid-conversation, or worse, leak details from an earlier unrelated ticket if sessions aren't properly scoped.

## Cold-Start Vs Warm-Start Agent Infrastructure

Q: What's the tradeoff between cold-starting agent worker processes on demand versus keeping a warm pool running?

A: Cold-start minimizes idle infrastructure cost but adds startup latency (loading tools, establishing connections, initial context) to the first request; a warm pool eliminates that latency at the cost of paying for idle capacity continuously.

Domain: D1

Example: A low-traffic internal agent tolerates cold starts fine, but a customer-facing chat agent with a strict first-response SLA needs a warm pool to avoid a multi-second delay on every new session.
