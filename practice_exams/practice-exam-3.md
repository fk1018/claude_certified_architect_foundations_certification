# CCAFC Practice Exam 3

**Claude Certified Architect – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Customer Support Agent, Code Generation with Claude Code, Developer Productivity, Structured Data Extraction) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (matches the official weightings): D1 Agentic Architecture ×16, D2 Tool Design & MCP ×11, D3 Claude Code Configuration ×12, D4 Prompt Engineering & Structured Output ×12, D5 Context Management & Reliability ×9.

Answer key with explanations is at the end.

---

## Scenario A: Customer Support Resolution Agent (Questions 1–15)

You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues. It has access to your backend systems through custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Your target is 80%+ first-contact resolution while knowing when to escalate.

---

**Question 1.** A teammate's loop implementation treats any response containing text content as the end of the conversation. In testing, the loop terminates on responses like "Let me look up that order for you" that also contain a pending `tool_use` block. What is the flaw?

- A) Presence of text is not a completion signal — responses can contain narration alongside tool calls; the loop must inspect `stop_reason` and continue whenever it is `"tool_use"`.
- B) The text check should be inverted: responses with no text content indicate completion.
- C) The model should be prompted to never emit text and tool calls together, making the check safe.
- D) The loop should wait for two consecutive text-bearing responses before terminating.

**Question 2.** Your agent updated a shipping address after matching only the customer's stated name, and the package went to the wrong person's account. The system prompt already says identity must be verified first. How do you make verification a hard guarantee?

- A) Add the verification rule to both the system prompt and the `update_address` tool description.
- B) Add few-shot examples of the agent refusing address changes before verification.
- C) Add a programmatic prerequisite that blocks `update_address` (and other account mutations) until `get_customer` has returned a verified customer ID in the session.
- D) Require the customer to type a confirmation phrase before the agent proceeds.

**Question 3.** Store policy prohibits refunds on final-sale items; the agent should instead explain the policy and offer store credit via escalation. Prompt instructions mostly work, but a compliance audit found four final-sale refunds last month. What closes the gap?

- A) Retrain support staff to catch final-sale refunds in the daily reconciliation report.
- B) Intercept `process_refund` calls with a hook that checks the item's final-sale flag, blocks the refund, and redirects the agent to the store-credit escalation workflow.
- C) Add the final-sale rule to the top of the system prompt in bold capital letters.
- D) Remove `process_refund` from the agent and route all refunds to humans.

**Question 4.** `get_customer` returns the loyalty tier as an integer (1–4), but your system prompt and policies refer to tiers by name ("Silver," "Gold"). The agent sometimes applies the wrong tier's benefits. What is the cleanest fix?

- A) Add a tier-conversion table to the system prompt for the agent to consult.
- B) Ask the backend team to change the API to return tier names.
- C) Add few-shot examples showing correct tier interpretation.
- D) Add a `PostToolUse` hook that maps the numeric tier to its name in the tool result before the model processes it.

**Question 5.** Your warranty-claim flow is identical every time (verify purchase → check warranty status → issue RMA), while fraud investigations are open-ended and depend on what each lookup reveals. How should these two workflows be decomposed?

- A) Use a fixed sequential chain for the predictable warranty flow, and dynamic decomposition — generating next steps from intermediate findings — for fraud investigations.
- B) Use dynamic decomposition for both, since flexibility never hurts.
- C) Use fixed sequential chains for both, adding fraud-specific branches to the script.
- D) Let the model choose freely for both, with no decomposition guidance.

**Question 6.** To "speed up easy cases," an engineer added a regex-based intent matcher that pre-routes messages containing "refund" straight to the refund flow before the model sees them. Misrouting complaints have since increased ("I do NOT want a refund, I want a replacement" went to the refund flow). What went wrong?

- A) The regex needs negative lookahead patterns to handle negations.
- B) The intent matcher should be a small classifier model instead of regex.
- C) A pre-configured keyword router overrides the model's contextual judgment — the point of a model-driven agent is that Claude reasons about intent from full context; remove the pre-routing.
- D) The refund flow should double-check intent with the customer before proceeding.

**Question 7.** Customers with three concerns in one message get correct resolutions, but handle time triples because the agent fully investigates each concern one after another. What does the recommended pattern look like?

- A) Limit conversations to one concern each and queue the rest for follow-up messages.
- B) Ask the customer which concern matters most and address only that one.
- C) Cache backend lookups so sequential investigations at least reuse data.
- D) Decompose the message into distinct items, investigate them in parallel using the shared conversation context, then synthesize a single unified resolution.

**Question 8.** In your loop implementation, a response arrives with `stop_reason: "tool_use"`, containing the text "Let me check that order" plus a `lookup_order` call. A junior developer's code displays the text to the customer and waits for the customer's reply. What should the code do instead?

- A) Suppress the text — responses with tool calls should never be shown to anyone.
- B) Execute `lookup_order`, append the result to the conversation, and send it back to the model; the text is narration accompanying an in-progress turn, not a completed reply.
- C) Show the text and simultaneously execute the tool, merging both paths on the next customer message.
- D) Return an error to the model, since text and tool calls must not be mixed.

**Question 9.** The agent keeps passing customer email addresses to `get_customer`, which only accepts numeric customer IDs, producing a stream of avoidable errors. The tool's description is one line: "Retrieves customer information." What is the right first fix?

- A) Add an application-side translation layer that converts emails to customer IDs before the tool runs.
- B) Have the tool accept both emails and IDs so the agent can't get it wrong.
- C) Return friendlier error messages so the agent recovers faster.
- D) Expand the tool description to document the accepted input format (numeric customer ID), give example calls, and state what to do when only an email is known.

**Question 10.** During a refund, the payment gateway times out. What should `process_refund` return so the agent responds appropriately?

- A) A structured error with `errorCategory: "transient"`, `isRetryable: true`, and a description — so the agent knows a retry is reasonable before falling back.
- B) `isError` with `retriable: false` so the agent doesn't waste calls on a failing gateway.
- C) A success response with a `pending: true` flag, since the refund will probably go through eventually.
- D) A generic failure message, letting the agent decide what to do from context.

**Question 11.** Your tools include `lookup_order` ("Retrieves order details") and `get_order_history` ("Retrieves order information"), and agents interchange them constantly — one returns a single order by ID, the other returns a paginated list of all orders. What is the highest-leverage fix?

- A) Merge both into one tool with an optional `order_id` parameter.
- B) Rewrite both descriptions to state each tool's distinct purpose, inputs, and outputs — including when to use one versus the other (single known order vs browsing a customer's history).
- C) Remove `get_order_history` since `lookup_order` covers the common case.
- D) Add a system prompt rule to always try `lookup_order` first.

**Question 12.** The agent answers policy questions (return windows, warranty terms) by calling a `search_kb` tool 5–8 times per conversation, probing for the right policy document. How can you give it visibility into what policy content exists without the exploratory calls?

- A) Paste the full policy manual into the system prompt.
- B) Fine-tune the model on the policy documents.
- C) Expose the policy document catalog as MCP resources, so the agent can see what's available and fetch precisely what it needs.
- D) Cache `search_kb` results across conversations.

**Question 13.** The escalation-desk agent (a separate agent that manages handoffs) frequently needs just the current status of an order, but its only option is the full order-management suite (`lookup_order`, `modify_order`, `cancel_order`), and it has occasionally modified orders while "checking status." What is the right tool distribution?

- A) Give the escalation agent a scoped, read-only `get_order_status` tool for its high-frequency need, and route anything requiring modification through the resolution agent.
- B) Keep the full suite but add a system prompt rule against modifications.
- C) Remove all order tools from the escalation agent and have it ask the customer for status.
- D) Grant the full suite to both agents so behavior is at least consistent.

**Question 14.** A single `manage_account` tool takes an `action` parameter (`"update_address"`, `"reset_password"`, `"close_account"`). The agent occasionally passes the wrong action — including one accidental account closure. What is the best redesign?

- A) Add a confirmation parameter that must be set to `true` for destructive actions.
- B) Document each action value more thoroughly in the tool description.
- C) Keep the tool but block `close_account` actions with a hook.
- D) Split it into separate purpose-specific tools (`update_address`, `reset_password`, `close_account`), each with its own description and input contract — and gate the destructive one appropriately.

**Question 15.** A customer's first message is: "I've been through this twice with your bot already. Get me a human. Now." The agent's current behavior is to attempt a resolution first, escalating only if that fails. What should it do?

- A) Continue current behavior — first-contact resolution is the primary metric.
- B) Escalate immediately — an explicit customer request for a human is an escalation trigger that should be honored without first attempting investigation.
- C) Ask the customer to describe the issue once more, then decide.
- D) Offer a discount to encourage the customer to continue with the bot.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation, with custom slash commands, CLAUDE.md configurations, and both plan mode and direct execution.

---

**Question 16.** Your `/gen-migration` skill generates database migrations, but developers keep invoking it bare — `/gen-migration` — and get generic scaffolds because the skill never learns the target table. What frontmatter option addresses this?

- A) `context: fork`, so the skill runs isolated and asks its own questions.
- B) `allowed-tools`, restricting the skill until a table is specified.
- C) `argument-hint`, prompting developers for the required table-name parameter when they invoke the skill without arguments.
- D) `paths`, restricting the skill to migration directories.

**Question 17.** You want to experiment with an aggressive variant of the team's shared `/test-gen` skill — different coverage strategy, different output style — without changing anyone else's workflow. What is the recommended approach?

- A) Create a personal variant under `~/.claude/skills/` with a different name, leaving the team's project-scoped skill untouched.
- B) Edit the project skill directly but commit it to a long-lived branch nobody else uses.
- C) Add an environment variable to the shared skill that switches to your behavior when set.
- D) Copy the skill into `.claude/skills/` under the same name so your version shadows the team's.

**Question 18.** You're migrating from Moment.js to date-fns across the codebase. You want to explore usage patterns and settle a conversion strategy before touching code, then apply the strategy efficiently. How should you use Claude Code's modes?

- A) Direct execution throughout — migrations are mechanical once started.
- B) Plan mode throughout — large migrations should never leave planning.
- C) Alternate modes file by file, planning each file just before editing it.
- D) Plan mode for the investigation and strategy decision, then direct execution to implement the planned approach.

**Question 19.** Your project's CLAUDE.md has grown to 1,200 lines mixing testing standards, API conventions, deployment procedures, and security rules. Finding and maintaining anything is painful. What is the recommended reorganization?

- A) Sort the file alphabetically by topic and add a table of contents.
- B) Split it into focused, topic-specific files under `.claude/rules/` (e.g., `testing.md`, `api-conventions.md`, `deployment.md`).
- C) Move the whole file to the wiki and link to it from a one-line CLAUDE.md.
- D) Compress it by removing all examples and explanations, keeping only rules.

**Question 20.** All code under `packages/mobile/` — and only that code — must follow your mobile team's conventions (navigation patterns, platform-specific error handling). The rest of the repo has different standards. What is the simplest correct placement?

- A) A `.claude/rules/` file with `paths: ["**/*"]` containing both convention sets.
- B) The root CLAUDE.md with a note saying "the following applies only to mobile."
- C) A CLAUDE.md inside `packages/mobile/` — directory-level configuration fits conventions scoped to one self-contained subtree.
- D) A skill that mobile developers invoke at the start of each session.

**Question 21.** Claude's data-migration script works except it crashes on rows with null values in the `legacy_status` column. You've explained the problem twice in prose without a reliable fix. What feedback is most likely to produce the correct fix?

- A) A specific failing test case: an example input row containing the null, plus the exact expected output for that row.
- B) A longer prose explanation covering nulls, empty strings, and undefined in general.
- C) A link to the database schema documentation.
- D) Asking Claude to re-read its own script and find the bug.

**Question 22.** Claude's latest change has three problems: an incorrect log format, an off-by-one in pagination, and missing type hints — three unrelated parts of the code, no interaction between fixes. A teammate insists all three must be sent in one combined message "or the fixes will conflict." What is the right guidance?

- A) The teammate is right — always batch feedback into a single message.
- B) Neither approach works; the change should be regenerated from scratch.
- C) Send one issue per session, starting a new session for each fix.
- D) These issues are independent, so sequential iteration works fine — the single-detailed-message approach matters when fixes interact, which these don't.

**Question 23.** You're about to have Claude implement a caching layer for your API — a domain where you know invalidation strategy, TTL policy, and stampede protection matter but you haven't thought them through. Which technique best surfaces these decisions before code gets written?

- A) Have Claude generate three alternative implementations and pick the best.
- B) Use the interview pattern: have Claude ask you questions about invalidation, failure modes, and consistency requirements before implementing.
- C) Implement quickly and let load testing reveal the gaps.
- D) Provide Claude a list of caching libraries and let it choose.

**Question 24.** You've built a personal `/standup-notes` command that formats your daily notes — useful to you, irrelevant to teammates. Where does it belong?

- A) `.claude/commands/` in the repository, since that's where commands live.
- B) The project CLAUDE.md as an always-available instruction.
- C) `~/.claude/commands/` — user-scoped commands are for personal workflows and don't travel with the repository.
- D) A gitignored file in `.claude/commands/` so it stays local.

**Question 25.** Twice this month you've had to revert half-completed refactors after discovering mid-way that the approach conflicted with how another module worked. Both refactors touched many files and had multiple viable designs. What practice prevents this?

- A) Smaller commits, so reverts are cheaper when conflicts appear.
- B) A rule that refactors may only touch five files per session.
- C) Running the test suite after every file edit.
- D) Entering plan mode first for this class of task — exploring the codebase and validating the design before committing to changes is what prevents costly rework.

**Question 26.** Late in a long session, Claude contradicts architecture answers it gave correctly two hours ago. You have several hours of work left. What practice keeps the remaining work grounded?

- A) Have Claude record key findings in a structured scratchpad file as it works, and consult that file when answering subsequent questions.
- B) Correct each contradiction conversationally as it appears.
- C) Ask Claude to summarize everything learned so far in its next reply, then continue as before.
- D) Restart the session and work from memory.

**Question 27.** Your build-and-test MCP tool returns ~300 lines of logs per run; you run it constantly, and only the pass/fail status and failing test names ever matter to the agent. Sessions degrade after a dozen runs. What is the right fix?

- A) Run builds less frequently, batching multiple changes per run.
- B) Trim the tool output to the relevant fields (status, failure names, first error) before it enters context — verbose results consume tokens disproportionately to their relevance.
- C) Switch to a larger-context model that absorbs the logs.
- D) Pipe the logs to a file and have the agent Read it when needed.

**Question 28.** You've finished a two-hour exploration phase and are about to start the implementation phase of the same large task. The session is at 70% context. What does the guide recommend before proceeding?

- A) Push on — implementation will naturally displace old exploration context.
- B) Delete the exploration messages manually from the transcript.
- C) Ask Claude to be brief from now on to conserve the remaining 30%.
- D) Summarize the key findings from the exploration phase, then start the next phase (or subagents) with that summary injected as initial context.

**Question 29.** You ask Claude to analyze a 25-file diff pasted as one long message. The analysis is sharp for the first and last few files and superficial for the middle of the diff. Which restructuring most directly addresses the cause?

- A) Paste the diff in reverse order so the neglected files come first.
- B) Ask Claude to "grade every file with equal rigor."
- C) Lead with a summary of the highest-priority files and organize the diff under explicit per-file section headers — countering the lost-in-the-middle position effect.
- D) Raise `max_tokens` so the analysis can be longer.

**Question 30.** Your desktop chat-style dev assistant (built on the API) forgets constraints the user stated four turns ago. Inspecting the client, you find each API call sends only the newest user message. What is the fix?

- A) Send the complete conversation history with every request — the API is stateless and coherence requires the full turn sequence each time.
- B) Add a system prompt instruction to remember all prior constraints.
- C) Increase `max_tokens` so more context fits.
- D) Have users restate constraints every few turns as a workaround.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You're wiring the SDK response handler. Which `stop_reason` value tells your code the model has finished its work and the response text should be presented to the developer?

- A) `"tool_use"` — the model has finished choosing tools.
- B) `"end_turn"` — the model has completed its turn with no further tool calls pending.
- C) `"max_tokens"` — the model has said everything it can.
- D) `"stop_sequence"` — the model reached its natural conclusion.

**Question 32.** Yesterday your agent built a thorough analysis of the repo in a named session. Overnight, a sweeping dependency upgrade changed imports in roughly 60% of files. You need analysis-informed help today. What is the most reliable continuation?

- A) Resume the named session and mention that "some files changed."
- B) Resume the session and have it re-Read every file it previously analyzed.
- C) Fork the session so the stale analysis is preserved in the parent branch.
- D) Start a new session seeded with a structured summary of the durable findings — with most prior tool results stale, resumption is less reliable than a fresh start plus summary.

**Question 33.** The agent generated a 20-file changeset. A single review pass over all 20 files produces uneven depth and missed an inter-file API mismatch. How should the review be structured?

- A) Two passes over all 20 files, keeping only findings that appear in both.
- B) One pass over the 10 riskiest files, ignoring the rest.
- C) Per-file passes for local issues, plus a separate integration pass focused on cross-file data flow and API consistency.
- D) One pass with an instruction to allocate equal attention to each file.

**Question 34.** Your agent needs three independent investigations — git history of a module, its test coverage, and its dependency audit — before proposing a refactor. How should the coordinator spawn them for minimum wall-clock time?

- A) Emit three Task tool calls in a single response so the subagents run in parallel.
- B) Spawn them in three consecutive turns, reviewing each result before the next.
- C) Combine all three into one subagent prompt for a single sequential investigation.
- D) Skip subagents and run the three investigations inline in the coordinator.

**Question 35.** Policy: the productivity agent must never write to `config/production/`. It has broad Write access for scaffolding elsewhere, and CLAUDE.md states the rule, but a near-miss occurred last week. What is the correct enforcement?

- A) Remove the Write tool from the agent everywhere.
- B) Move the production configs outside the repository.
- C) Strengthen the CLAUDE.md wording and add the rule to every skill.
- D) Add a hook that intercepts Write/Edit tool calls and blocks any targeting `config/production/` paths.

**Question 36.** A developer asks the agent to rename a variable in one file. Logs show the full multi-agent pipeline spun up — test-writer, doc-writer, and refactor subagents all invoked — for a 30-second task. What is the architectural fix?

- A) Cap the number of subagents at two per request.
- B) Have the coordinator assess each request's complexity and invoke only the subagents the task actually requires — trivial requests need no delegation at all.
- C) Remove the coordinator and let developers pick subagents manually.
- D) Make the pipeline faster so over-invocation costs less.

**Question 37.** Early in a session the coordinator discovered the project's testing conventions. It then spawns a test-writer subagent, whose output ignores every one of those conventions. Why?

- A) The test-writer's model tier is too low to follow conventions.
- B) The conventions need to be in CLAUDE.md to reach subagents.
- C) The subagent received a prompt that didn't include the discovered conventions — subagents don't inherit the coordinator's conversation history, so context must be passed explicitly.
- D) The Task tool strips formatting from prompts, garbling the conventions.

**Question 38.** Asked to "improve error handling across our services," the coordinator decomposed the work into subtasks for just two of the seven services, and the final report claims completion. What is the root-cause fix?

- A) Improve the coordinator's decomposition step — have it enumerate the full scope (all services) before creating subtasks, with coverage criteria to check against; the subagents did their assigned work correctly.
- B) Instruct the subagents to volunteer for additional services when they finish early.
- C) Add more subagents so more services get covered by chance.
- D) Have the report generator flag services it wasn't given data for.

**Question 39.** Your utilities are re-exported through several `index.ts` barrel files, so importers reference the barrel, not the source file. You need every real usage of the functions defined in `src/util/dates.ts`. What is the right built-in tool strategy?

- A) Glob for `**/index.ts` and read each barrel file.
- B) Grep for `src/util/dates` and treat those importers as the full usage list.
- C) Read `dates.ts` and rely on the IDE's reference count from memory.
- D) First identify all names exported from `dates.ts` (directly and via barrels), then Grep for each exported name across the codebase.

**Question 40.** The agent must locate every Storybook story file — they follow the `*.stories.tsx` naming convention and are scattered throughout `src/`. Which tool fits?

- A) Grep for the string "storiesOf" in file contents.
- B) Glob with the pattern `**/*.stories.tsx` — this is filename pattern matching, Glob's purpose.
- C) Read the Storybook config and infer the file list.
- D) Bash `find` piped through several greps.

**Question 41.** Two edits are queued: (a) completely regenerate a 15-line config file from a new template; (b) rename one function in a 2,000-line module. Which tool pairing is correct?

- A) Write for the config regeneration (full replacement of a small file); Edit for the targeted rename (unique-anchor modification in a large file).
- B) Edit for both — Edit is always safer than Write.
- C) Write for both — full-file writes are more predictable.
- D) Edit for the config file; Write for the module.

**Question 42.** You found a promising community MCP server for database introspection and want to trial it for a week before proposing it to the team. Where do you configure it?

- A) In the project's `.mcp.json`, marked with a comment saying "experimental."
- B) In the project's CLAUDE.md so its usage is documented.
- C) In your user-scoped `~/.claude.json` — personal and experimental servers belong at user level, keeping the project configuration clean for the team.
- D) In `.claude/rules/` with a path scope limiting it to your files.

**Question 43.** Your system prompt says: "Always use the ripgrep-mcp tool for searching." Now the agent uses it even to find files by name — where Glob is correct — and results have gotten worse. What is the underlying lesson?

- A) MCP search tools should never coexist with built-in search tools.
- B) The instruction needed the word "content": one word would fix everything.
- C) ripgrep-mcp's tool description is too weak to constrain the instruction.
- D) Keyword-sensitive system prompt instructions create unintended tool associations that override sensible per-task selection — describe when to use the tool instead of mandating it always.

**Question 44.** Before choosing where to hook a new plugin system, the agent must survey twelve candidate modules. You want the survey's verbose output kept away from the main session, which will do the actual design work. What is the right mechanism?

- A) Read all twelve modules in the main session, then `/compact`.
- B) Use the Explore subagent for the survey — its verbose discovery stays in an isolated context and only a summary returns.
- C) Survey four modules per session across three sessions.
- D) Skip the survey and choose the hook point from the architecture diagram.

**Question 45.** Your `/brainstorm-designs` skill generates several speculative design alternatives with pros and cons. After running it, the main session keeps referencing rejected alternatives as if they were decisions. What fixes this?

- A) Run the skill in a permanent dedicated session used only for brainstorming.
- B) Add a closing line to the skill output: "All of the above are hypothetical."
- C) End every brainstorm by asking Claude to forget the rejected options.
- D) Add `context: fork` to the skill so the exploratory content stays in an isolated context, returning only the chosen direction to the main session.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your pipeline requires `extract_metadata` to run on every document before any enrichment tool may be called. The model usually complies with the prompt instruction but occasionally jumps straight to enrichment. What guarantees the ordering?

- A) Set `tool_choice: "any"` so a tool is always called first.
- B) List `extract_metadata` first in the tools array, since order implies priority.
- C) Force it: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, then handle enrichment in subsequent turns with normal tool choice.
- D) Add few-shot examples demonstrating metadata-first ordering.

**Question 47.** You're designing the invoice schema and must decide which fields are `required`. Which principle is correct?

- A) Mark all business-critical fields required so the model knows they matter.
- B) Mark everything optional to maximize extraction flexibility.
- C) Mark required whatever downstream systems need, regardless of the documents.
- D) Mark required only fields genuinely present in every document; fields that may legitimately be absent should be optional/nullable — required-but-absent fields pressure the model to fabricate values.

**Question 48.** You're extracting quantities from maintenance logs where technicians write informally: "topped off with about half a jug," "roughly two dozen bolts." The model keeps outputting precise-looking fabricated numbers. What is the most effective mitigation?

- A) Add a regex validator rejecting suspiciously precise values.
- B) Add few-shot examples demonstrating correct handling of informal measurements — mapping them to approximate values with an `is_estimate` flag, or to null when unquantifiable — so the model generalizes instead of inventing precision.
- C) Instruct the model to "never guess" in the system prompt.
- D) Route all logs containing the word "about" to human review.

**Question 49.** Academic papers in your corpus vary structurally: some use inline citations, others end-of-paper bibliographies; some have a dedicated methodology section, others embed methods in results. Extraction quality varies wildly with the structure. What is the recommended fix?

- A) Add few-shot examples demonstrating correct extraction from each structural variant — inline vs bibliography citations, dedicated vs embedded methodology — so the model handles the variety.
- B) Preprocess every paper into a single canonical structure before extraction.
- C) Build one extraction prompt per journal, routed by source.
- D) Extract only from papers matching the most common structure.

**Question 50.** Since adopting tool_use with a strict schema, outputs always validate — but spot checks find the vendor's name in the `customer_name` field and the invoice date in `due_date`. What does this demonstrate?

- A) The schema's field names are too similar and must be renamed.
- B) The documents are too noisy for automated extraction.
- C) Strict schemas eliminate syntax errors, not semantic errors — values in the wrong fields validate fine; you need semantic validation (cross-field checks, spot sampling) on top.
- D) `tool_choice: "any"` is needed to make field mapping reliable.

**Question 51.** An extraction fails Pydantic validation. You will retry. Which retry request gives the model the best chance of a correct second pass?

- A) The same request again — the model usually self-corrects on a second sample.
- B) Just the validation error, to keep the retry cheap.
- C) The failed extraction with an instruction to "fix the errors."
- D) The original document, the failed extraction, and the specific validation errors together — full context for targeted self-correction.

**Question 52.** Documents arrive continuously and your contract guarantees results within 30 hours. Batch processing can take up to 24 hours. Which submission schedule guarantees the SLA while minimizing submission overhead?

- A) One batch daily — 24-hour accumulation plus 24-hour processing stays under two days.
- B) Submit a batch every 4 hours — worst case 4h accumulation + 24h processing = 28 hours, inside the SLA with margin.
- C) Every 8 hours — 8 + 24 = 32 hours is close enough given batches usually finish early.
- D) Every 12 hours with a priority flag on older documents.

**Question 53.** Two extraction workloads: (1) a compliance archive of 80,000 historical contracts to process this quarter; (2) a customer-facing upload flow where the user watches a spinner until their document's data appears. How do you assign APIs?

- A) Batch API for the archive (latency-tolerant, 50% cheaper); synchronous API for the upload flow (a user is blocked waiting).
- B) Batch API for both — the savings apply equally.
- C) Synchronous API for both — simpler architecture beats cost savings.
- D) Synchronous for the archive to finish it faster; batch for uploads since users can be emailed later.

**Question 54.** You've submitted a batch of 2,000 extraction requests. How does your pipeline obtain and correlate the results?

- A) Results stream back over a webhook in submission order as each completes.
- B) The submission call blocks until all results are ready, returning them in order.
- C) Results are emailed as a signed archive when the batch finishes.
- D) Poll the batch's status until processing ends, then retrieve results and match each to its request using the `custom_id` you assigned at submission.

**Question 55.** Scanned approval forms have checkboxes that are sometimes too degraded to read. The schema's `decision` field is an enum: `["approved", "rejected"]`, and the model currently guesses. What is the correct schema change?

- A) Lower the scan-quality threshold so degraded forms are rejected at intake.
- B) Add an `ocr_confidence` float and accept guesses above 0.8.
- C) Add an `"unclear"` enum value for ambiguous cases, and route those extractions to human review rather than forcing a binary guess.
- D) Make `decision` free text so the model can express uncertainty.

**Question 56.** Your extraction step also self-checks its output ("verify your extraction before finalizing") and reports near-zero errors — but human audits find real mistakes it never catches. What is the structural fix?

- A) Make the self-check mandatory via tool_choice.
- B) Run a second, independent verification pass in a fresh instance that compares the extraction against the source without the extractor's reasoning context.
- C) Strengthen the self-check prompt with a checklist of error types.
- D) Ask for a confidence score with the self-check and audit only low scores.

**Question 57.** Next week you'll batch-process 50,000 archived contracts with a newly written extraction prompt. What should happen first?

- A) Refine the prompt on a representative sample using the synchronous API, iterating until quality is verified — first-pass success is what controls cost at 50,000-document scale.
- B) Submit the full batch — the 50% discount makes failed passes affordable.
- C) Split the archive into ten 5,000-document batches and fix the prompt between each.
- D) Run the whole archive through a cheaper model first as a smoke test.

**Question 58.** Your OCR agent hands its output to a validation agent whose context budget is small. Currently it sends the full raw text plus its complete reasoning narrative, and the validation agent truncates. What is the right change?

- A) Double the validation agent's context budget.
- B) Have the validation agent request pages on demand.
- C) Compress the OCR text with a summarization pass.
- D) Modify the upstream agent to return structured data — key extracted facts, locations in the source, flags — instead of verbose content and reasoning chains, sized for the downstream consumer.

**Question 59.** An extracted vendor name matches three different vendor records in your master file. The pipeline currently auto-selects the most recently active vendor. What should it do instead?

- A) Auto-select the vendor with the closest string match instead of recent activity.
- B) Create a new vendor record to avoid guessing among the three.
- C) Treat multiple matches as an ambiguity requiring more information — use additional identifiers from the document (address, tax ID) to disambiguate, and route to human review when they don't resolve it.
- D) Pick randomly but log the decision for audit.

**Question 60.** Your extraction summary report converts everything to prose paragraphs — including line-item tables and numeric comparisons — and reviewers say checking figures is painful. What does the guide recommend?

- A) Convert everything to tables instead, since reviewers prefer them.
- B) Render each content type appropriately — financial and line-item data as tables, narrative context as prose, itemized findings as structured lists — rather than forcing a uniform format.
- C) Provide raw JSON to reviewers, who can format it as needed.
- D) Add a "figures appendix" repeating all numbers at the end of the prose.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-A, 2-C, 3-B, 4-D, 5-A, 6-C, 7-D, 8-B, 9-D, 10-A, 11-B, 12-C, 13-A, 14-D, 15-B, 16-C, 17-A, 18-D, 19-B, 20-C, 21-A, 22-D, 23-B, 24-C, 25-D, 26-A, 27-B, 28-D, 29-C, 30-A, 31-B, 32-D, 33-C, 34-A, 35-D, 36-B, 37-C, 38-A, 39-D, 40-B, 41-A, 42-C, 43-D, 44-B, 45-D, 46-C, 47-D, 48-B, 49-A, 50-C, 51-D, 52-B, 53-A, 54-D, 55-C, 56-B, 57-A, 58-D, 59-C, 60-B

---

**1. A** — Text content is not a completion signal: responses routinely carry narration alongside `tool_use` blocks. The loop must inspect `stop_reason` and continue on `"tool_use"`. B inverts a check that shouldn't exist. C prompts around a control-flow bug. D doubles down on the wrong signal.

**2. C** — When identity verification must be guaranteed before account mutations, only a programmatic prerequisite (blocking mutation tools until `get_customer` returns a verified ID) is deterministic. A and B are prompt-layer measures with non-zero failure rates — the incident already proves the point. D adds customer friction without enforcement.

**3. B** — A compliance rule with audit findings needs hook-level interception: check the final-sale flag on `process_refund` calls, block, and redirect to the store-credit workflow. C is more prompt emphasis on an already-stated rule. D destroys the agent's core capability to fix one policy edge. A detects violations after the money moves.

**4. D** — A `PostToolUse` hook mapping numeric tiers to names normalizes the data before the model reasons over it — deterministic and invisible to the prompt. A and C rely on the model performing the conversion correctly every time. B may be right long-term but is out of your control and slow.

**5. A** — Match decomposition to the workflow: fixed sequential chains for predictable flows (warranty), dynamic decomposition driven by intermediate findings for open-ended investigations (fraud). B adds adaptive overhead where nothing varies. C scripts the unscriptable. D abandons the structure that makes the predictable flow reliable.

**6. C** — Pre-routing by keyword replaces the model's contextual judgment with a brittle pattern match — the exact failure the example shows ("do NOT want a refund"). Model-driven agents exist because intent requires context. A and B upgrade the router instead of removing an unnecessary layer. D patches the symptom downstream.

**7. D** — The pattern for multi-concern requests: decompose into distinct items, investigate in parallel using shared context, synthesize a unified resolution — correctness *and* speed. A and B degrade the customer experience to fit the architecture. C speeds up a sequential design instead of fixing it.

**8. B** — `stop_reason: "tool_use"` means the turn is in progress: execute the tool, append the result, send it back. Accompanying text is narration, not a completed reply awaiting customer input. A discards useful narration unnecessarily (it can be shown as status). C forks the conversation state. D — mixed text and tool calls are normal.

**9. D** — Tool descriptions should document input formats, example queries, and boundary behavior; the agent is guessing because one line tells it nothing about accepted identifiers. A and B build infrastructure to tolerate a documentation gap. C makes failure cheaper rather than rarer.

**10. A** — A gateway timeout is a transient error: `errorCategory: "transient"`, `isRetryable: true`, plus a description lets the agent retry sensibly. B mislabels it non-retryable, abandoning refunds that would succeed. C reports success for an operation that didn't complete — dangerous. D returns the agent to guessing.

**11. B** — These tools have distinct purposes hidden behind near-identical descriptions; rewriting both to state purpose, inputs, outputs, and when to choose each fixes selection at the root. A merges two legitimately different access patterns. C removes needed functionality. D hardcodes a preference instead of enabling a choice.

**12. C** — MCP resources exist to expose content catalogs, giving the agent visibility into available policy documents without exploratory probing. A bloats every conversation with the full manual. B is out of scope and disproportionate. D makes repeated probing cheaper, not unnecessary.

**13. A** — Scoped cross-role tools serve high-frequency needs safely: a read-only `get_order_status` gives the escalation agent what it uses constantly, while modification stays with the role that owns it. B leaves the dangerous capability reachable behind a prompt. C removes a legitimate need. D doubles the exposure.

**14. D** — A mode-switched tool with a destructive branch is the case for splitting into purpose-specific tools with individual contracts — misselecting an enum value should never close an account. A and B leave one entry point where a parameter typo is catastrophic. C keeps the confusing design and bolts a gate onto one branch.

**15. B** — An explicit customer request for a human is a defined escalation trigger to honor immediately — investigation attempts after "get me a human, now" erode trust. A and C do exactly what the customer asked you not to do. D is a retention tactic, not an escalation policy.

**16. C** — `argument-hint` frontmatter prompts developers for required parameters when the skill is invoked without arguments — precisely the failure here. A changes execution isolation, not input collection. B misuses a tool-permission control. D isn't skill frontmatter for this purpose.

**17. A** — Personal skill customization: create a variant under `~/.claude/skills/` with a different name, so teammates' workflow is untouched. B ships team-visible changes to a shared artifact. C adds a hidden mode to a shared skill. D shadows the team's skill under the same name — exactly the collision to avoid.

**18. D** — Combine the modes: plan mode for exploring usage patterns and settling the conversion strategy, direct execution to apply the planned approach. A skips the design decision that determines the migration's quality. B never ships. C fragments a strategy decision that should be made once.

**19. B** — The recommended structure for an overgrown CLAUDE.md is topic-specific files in `.claude/rules/` (`testing.md`, `api-conventions.md`, …). A reorganizes without reducing the monolith. C makes the content invisible to Claude. D strips the examples that make conventions followable.

**20. C** — Conventions scoped to one self-contained subtree are the fit for a directory-level CLAUDE.md inside `packages/mobile/`. A loads both convention sets everywhere. B loads mobile rules in every session and relies on the model to scope them. D applies conventions only when someone remembers to invoke it.

**21. A** — For edge-case fixes, provide a specific test case: example input containing the null and the exact expected output. That's unambiguous in a way prose has already failed to be. B is more prose. C provides background, not the expected behavior. D re-asks the model to find what it's already missed twice.

**22. D** — Independent problems can be fixed sequentially; the single-detailed-message guidance applies when fixes interact and would invalidate each other. A overgeneralizes the interacting-issues rule. B is disproportionate. C adds session churn with no benefit.

**23. B** — The interview pattern targets unfamiliar domains with unarticulated constraints: Claude asks about invalidation, failure modes, and consistency before implementing — surfacing exactly the considerations you know you haven't thought through. A generates three versions of the same blind spots. C discovers requirements in production. D picks a library, not a design.

**24. C** — Personal, team-irrelevant commands belong in `~/.claude/commands/` (user-scoped); `.claude/commands/` is for team-shared, version-controlled commands. B misplaces a command as an instruction. D pollutes the project directory to simulate what user scope already provides.

**25. D** — Multi-file changes with multiple viable designs are plan mode's core case: explore and validate the approach before changing code, preventing exactly this costly rework. A cheapens the failure instead of preventing it. B is an arbitrary constraint unrelated to the cause. C catches breakage, not design conflicts.

**26. A** — This is context degradation in an extended session; the countermeasure is a scratchpad file of key findings, recorded as discovered and consulted for later answers — persistent ground truth outside the degrading context. B fixes symptoms one at a time, forever. C puts the summary into the same degrading context. D loses the accumulated understanding entirely.

**27. B** — Verbose tool outputs consume context disproportionately to their relevance; trim to the fields that matter (status, failing tests, first error) before results accumulate. A slows the feedback loop that makes the agent useful. C postpones the problem. D still spends the context when the file is read, and adds a step.

**28. D** — The guide's phase-transition practice: summarize key findings from the completed exploration phase and inject the summary as initial context for the next phase or subagents. A lets implementation compete with exploration residue at 70% full. B isn't a supported operation. C conserves output tokens, not context.

**29. C** — Uneven middle coverage of a long uniform input is lost-in-the-middle; the mitigation is a priority summary at the start plus explicit per-file section headers. A moves the blind spot rather than removing it. B — exhortation doesn't change position effects. D lengthens the answer, not the attention.

**30. A** — The API is stateless: each request must carry the complete conversation history, or earlier constraints simply don't exist for the model. B instructs it to remember what it was never sent. C is unrelated to missing input. D makes users compensate for a client bug.

**31. B** — `"end_turn"` signals the model has completed its turn with no pending tool work — time to present the response. `"tool_use"` (A) means work remains. `"max_tokens"` (C) means truncation, not completion. D — stop sequences are a different, configured mechanism.

**32. D** — With ~60% of analyzed files changed, the session's tool results are mostly stale; starting fresh with a structured summary of durable findings is more reliable than resuming. A resumes atop stale data with a vague warning. B re-does the analysis inside a context already full of the old one. C preserves staleness in two places.

**33. C** — Uneven depth plus a missed cross-file issue is attention dilution: split into per-file passes for local issues and a dedicated integration pass for cross-file data flow. A double-spends on the same diluted view and suppresses intermittent catches. B trades coverage for depth by guesswork. D — instructions don't reallocate attention.

**34. A** — Independent investigations parallelize by emitting multiple Task tool calls in a single coordinator response. B serializes them across turns. C serializes them inside one context. D floods the coordinator's context with three investigations' worth of raw output.

**35. D** — A must-never rule with a near-miss on record needs interception: a hook blocking Write/Edit calls targeting `config/production/` paths. A removes a capability the agent legitimately needs elsewhere. B reorganizes the repo around a missing guardrail. C adds prompt emphasis where prompts already failed.

**36. B** — Coordinators should assess query complexity and invoke only the subagents a task needs — a one-line rename needs none. A caps waste at two subagents instead of zero. C removes orchestration rather than fixing its judgment. D optimizes the cost of doing the wrong thing.

**37. C** — Subagents don't inherit the coordinator's history; the discovered conventions had to be included in the test-writer's prompt. A and D invent mechanisms. B would work for static conventions but doesn't address the actual mechanism — and these conventions were discovered dynamically this session.

**38. A** — The subagents completed their assignments; the coverage failure happened at decomposition. Fix the coordinator: enumerate the full scope before creating subtasks and check decomposition against coverage criteria. B asks workers to fix planning. C adds capacity without direction. D reports the gap instead of closing it.

**39. D** — Barrel re-exports mean importers reference the barrel, so tracing requires two steps: enumerate the exported names, then Grep for each name across the codebase. A finds the barrels, not the users. B finds only direct-path importers — the minority. C isn't grounded in the current code.

**40. B** — Finding files by naming convention is Glob's exact purpose: `**/*.stories.tsx`. A searches contents for an API string many stories won't contain. C infers instead of matching. D reimplements Glob with more failure modes.

**41. A** — Write is for full-file creation/replacement (the regenerated config); Edit is for targeted modifications via unique anchor text (the rename in a large file). B forces anchor-matching on a total rewrite. C rewrites 2,000 lines to change one name — slow and risky. D is backwards on both.

**42. C** — Personal and experimental MCP servers belong in user-scoped `~/.claude.json`; project `.mcp.json` is for shared team tooling. A ships your experiment to everyone. B documents without configuring. D misuses a rules mechanism for server configuration.

**43. D** — "Always use X" is a keyword-sensitive instruction that creates an unintended blanket association, overriding sensible per-task tool selection. The fix is describing when the tool applies. A and C misplace the blame. B patches this instance of a pattern worth learning generally.

**44. B** — The Explore subagent isolates verbose discovery and returns a summary — the main session keeps its context for design. A spends the main context first and summarizes after the damage. C splits the survey but loses cross-module comparison. D skips the evidence the decision needs.

**45. D** — Exploratory, speculative content is what `context: fork` is for: the brainstorm runs isolated, and only the outcome returns — rejected alternatives never enter the main conversation to be misremembered as decisions. A quarantines by convention, not mechanism. B and C ask the model to disregard context it has already absorbed.

**46. C** — Guaranteeing that a specific tool runs first requires forced tool selection: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, with enrichment handled in follow-up turns. A guarantees *a* tool, not *that* tool. B — array order carries no such semantics. D remains probabilistic.

**47. D** — Required should mean "genuinely always present." Fields that may legitimately be absent must be optional/nullable, or the model is pressured to fabricate values to satisfy the schema. A confuses importance with presence. B loses real invariants. C encodes downstream wishes the documents can't honor.

**48. B** — Few-shot examples demonstrating informal-measurement handling (approximate value + estimate flag, or null when unquantifiable) teach a judgment the model generalizes — the guide's cited use of few-shot for reducing extraction hallucination. A catches some fabrications after the fact. C is a vague instruction where examples are the effective tool. D outsources a solvable pattern.

**49. A** — Structural variety is the textbook few-shot case: examples demonstrating correct extraction from each variant (inline vs bibliography, dedicated vs embedded methodology) let the model handle the spread. B presumes a reliable universal normalizer. C multiplies prompts to dodge generalization. D silently shrinks coverage.

**50. C** — Schema-valid output with values in the wrong fields is a semantic error — the class strict schemas cannot prevent. Add semantic validation: cross-field consistency checks and sampled audits. A might help marginally but misses the general lesson. B gives up on a solvable problem. D governs *whether* a tool is called, not field accuracy.

**51. D** — Effective retries carry the original document, the failed extraction, and the specific validation errors — everything needed for targeted self-correction. A relies on luck. B and C omit the source document, so the model can't re-ground the corrected values.

**52. B** — Worst case must fit the SLA: 4-hour accumulation + 24-hour processing = 28 hours ≤ 30, with margin. A's worst case is 48 hours. C's is 32 — over the line, and "usually finishes early" isn't a guarantee. D's is 36, and priority flags don't change batch processing time.

**53. A** — Match API to latency tolerance: the archive is the Batch API's ideal case (huge, non-blocking, 50% cheaper); the upload flow has a human watching a spinner — synchronous. B leaves users staring at spinners for potentially hours. C forfeits large savings for no benefit. D is backwards on both workloads.

**54. D** — Batch results are obtained by polling for completion, then retrieving and correlating via the `custom_id` set at submission. A, B, and C describe delivery mechanisms the Batch API doesn't have (streaming webhooks in order, blocking submission, email delivery).

**55. C** — Ambiguous source data needs an explicit `"unclear"` enum value plus routing to human review — the schema should let the model tell the truth instead of forcing a binary guess. A throws away processable documents. B dresses the guess in a score. D destroys the machine-readable contract downstream systems depend on.

**56. B** — Self-checks inherit the extractor's reasoning and blind spots; an independent verification pass — fresh instance, source document, no prior context — catches what self-review structurally cannot. A makes the biased check mandatory. C gives the biased check a checklist. D calibrates a signal produced by the same blind process.

**57. A** — Refine on a representative sample before batch-processing large volumes: first-pass success determines cost when each full pass is 50,000 documents with up-to-24-hour turnaround. B risks the whole archive on an untested prompt. C discovers problems 5,000 documents at a time. D tests a different model's behavior, not your prompt's quality on the real one.

**58. D** — When the downstream agent has a limited context budget, modify the upstream agent to emit structured data — key facts, source locations, flags — instead of verbose content and reasoning chains. A scales the budget to fit the waste. B adds round-trips to consume the same verbosity. C compresses prose that shouldn't be prose at all.

**59. C** — Multiple matches are an ambiguity to resolve with additional identifiers (address, tax ID from the document), not a heuristic pick; when identifiers don't resolve it, route to human review. A swaps one heuristic for another. B corrupts the master file. D is a heuristic with a paper trail.

**60. B** — Content types should render in the form that fits them: financial data as tables, narrative as prose, findings as structured lists — uniform formatting is the anti-pattern in both directions. A repeats the mistake with a different uniform. C exports the formatting work to reviewers. D duplicates numbers instead of presenting them properly once.

---

*End of Practice Exam 3.*
