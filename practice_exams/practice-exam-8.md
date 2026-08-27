# CCAFC Practice Exam 8

**Claude Certified Architect – Foundations — Practice Exam**

Rebalanced edition of Practice Exam 3 — same knowledge points; options rewritten to remove test-taking tells (option-length cues, giveaway distractors), answer letters reshuffled, one near-duplicate question replaced.

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

- A) Invert the check so that responses containing no text content at all are what the loop treats as the finished, ready-to-present turn.
- B) Prompt the model to never emit narration text alongside a pending tool call, so any text-bearing response can be treated as safely final.
- C) Require two consecutive text-only responses in a row before the loop is allowed to terminate the conversation.
- D) Text is not a completion signal — inspect `stop_reason` and continue the loop when it reads `"tool_use"`.

**Question 2.** Your agent updated a shipping address after matching only the customer's stated name, and the package went to the wrong person's account. The system prompt already says identity must be verified first. How do you make verification a hard guarantee?

- A) Add the verification rule to both the system prompt and the `update_address` tool description.
- B) Block `update_address` and every other account-mutation tool until `get_customer` has returned a verified customer ID.
- C) Add few-shot examples of the agent refusing address changes before identity has been verified.
- D) Require the customer to type a specific confirmation phrase before the agent is allowed to proceed with any change.

**Question 3.** Store policy prohibits refunds on final-sale items; the agent should instead explain the policy and offer store credit via escalation. Prompt instructions mostly work, but a compliance audit found four final-sale refunds last month. What closes the gap?

- A) Intercept `process_refund` with a hook that checks the final-sale flag and redirects to the store-credit workflow.
- B) Retrain support staff to catch final-sale refunds during the daily reconciliation report before it closes out.
- C) Add the final-sale rule to the top of the system prompt in bold capital letters for emphasis.
- D) Remove `process_refund` from the agent entirely and route every refund request to a human reviewer.

**Question 4.** `get_customer` returns the loyalty tier as an integer (1–4), but your system prompt and policies refer to tiers by name ("Silver," "Gold"). The agent sometimes applies the wrong tier's benefits. What is the cleanest fix?

- A) Add a tier-conversion lookup table to the system prompt for the agent to consult on every request.
- B) Ask the backend team to change the API so it returns tier names instead of numeric codes.
- C) Normalize the numeric tier into its name with a `PostToolUse` hook before the model reads it, keeping the system prompt free of manual conversion tables.
- D) Add few-shot examples in the prompt showing correct interpretation of each numeric tier value.

**Question 5.** Your warranty-claim flow is identical every time (verify purchase → check warranty status → issue RMA), while fraud investigations are open-ended and depend on what each lookup reveals. How should these two workflows be decomposed?

- A) Use dynamic decomposition for both flows, so the agent can still adapt if a warranty case turns out unusual.
- B) A fixed sequential chain for the warranty flow; dynamic decomposition for the open-ended fraud investigations.
- C) Fixed sequential chains for both, adding extra fraud-specific branches directly into the warranty script.
- D) Let the model choose its own approach for both, guided only by examples of past cases.

**Question 6.** To "speed up easy cases," an engineer added a regex-based intent matcher that pre-routes messages containing "refund" straight to the refund flow before the model sees them. Misrouting complaints have since increased ("I do NOT want a refund, I want a replacement" went to the refund flow). What went wrong?

- A) The regex needs negative-lookahead patterns added so it can handle simple negations correctly.
- B) Replace the regex intent matcher with a small trained classifier model that scores intent, instead of relying on brittle pattern matching.
- C) Have the refund flow double-check the customer's intent before proceeding with any action.
- D) Keyword pre-routing overrides the model's contextual judgment — remove it and let Claude reason about intent directly.

**Question 7.** Customers with three concerns in one message get correct resolutions, but handle time triples because the agent fully investigates each concern one after another. What does the recommended pattern look like?

- A) Decompose the message into distinct concerns, investigate each in parallel with shared context, then synthesize one resolution.
- B) Limit each conversation to one concern and queue the remaining concerns for separate follow-up messages later.
- C) Ask the customer which of their concerns matters most and address only that single item.
- D) Cache backend lookups aggressively so sequential investigations at least reuse previously fetched account and billing data across every concern.

**Question 8.** Your loop executes the `lookup_order` call the model requested and receives the order data. How must the result be returned so the conversation continues correctly?

- A) As an assistant-role message carrying a structured summary, so the model treats the data as something it already said.
- B) As a new section appended to the system prompt for the rest of the conversation.
- C) As a `tool_result` block referencing the `tool_use` ID, in a user-role message, with the conversation re-sent.
- D) As a fresh conversation seeded with the tool result and the customer's most recent question.

**Question 9.** The agent keeps passing customer email addresses to `get_customer`, which only accepts numeric customer IDs, producing a stream of avoidable errors. The tool's description is one line: "Retrieves customer information." What is the right first fix?

- A) Add an application-side translation layer that converts email addresses to customer IDs before the tool ever runs.
- B) Expand the tool description itself, rather than the system prompt, with the accepted input format, example calls, and what to do when only an email address is known.
- C) Loosen the tool's input schema and add a validation hook that accepts both emails and IDs directly, so the agent cannot get it wrong.
- D) Return friendlier, more descriptive error messages so the agent recovers faster after a failed call.

**Question 10.** During a refund, the payment gateway times out. What should `process_refund` return so the agent responds appropriately?

- A) Return `isError` with `retriable: false`, so the agent stops wasting calls on a gateway that is currently failing.
- B) Return a success response with a `pending: true` flag, since the refund will probably go through eventually.
- C) Return a generic failure message and let the agent decide what to do next from context alone.
- D) Return a structured error: `errorCategory: "transient"`, `isRetryable: true`, and a short human-readable description.

**Question 11.** Your tools include `lookup_order` ("Retrieves order details") and `get_order_history` ("Retrieves order information"), and agents interchange them constantly — one returns a single order by ID, the other returns a paginated list of all orders. What is the highest-leverage fix?

- A) Merge both tools into one, with an optional `order_id` parameter that switches between the two behaviors.
- B) Remove `get_order_history` entirely, since `lookup_order` already covers the common single-order case.
- C) Rewrite both descriptions with each tool's distinct purpose, inputs, outputs, and guidance on when to use which.
- D) Add a system prompt rule instructing the agent to always try `lookup_order` first.

**Question 12.** The agent answers policy questions (return windows, warranty terms) by calling a `search_kb` tool 5–8 times per conversation, probing for the right policy document. How can you give it visibility into what policy content exists without the exploratory calls?

- A) Expose the policy document catalog as MCP resources the agent can see and fetch from precisely.
- B) Paste the full policy manual directly into the system prompt so nothing ever needs to be looked up.
- C) Fine-tune the model on the complete set of policy documents to internalize their content.
- D) Cache `search_kb` results across conversations so repeated probing at least avoids duplicate calls.

**Question 13.** The escalation-desk agent (a separate agent that manages handoffs) frequently needs just the current status of an order, but its only option is the full order-management suite (`lookup_order`, `modify_order`, `cancel_order`), and it has occasionally modified orders while "checking status." What is the right tool distribution?

- A) Keep the full order-management suite but add a hook that only logs modification attempts to an audit trail after they already happen.
- B) Remove all order tools from the escalation agent and have it ask the customer for status instead.
- C) Grant the full suite to both agents so their behavior is at least consistent.
- D) Give it a scoped, read-only `get_order_status` tool; route modification requests through the resolution agent instead.

**Question 14.** A single `manage_account` tool takes an `action` parameter (`"update_address"`, `"reset_password"`, `"close_account"`). The agent occasionally passes the wrong action — including one accidental account closure. What is the best redesign?

- A) Add a confirmation parameter that must be explicitly set to `true` before any destructive action can run.
- B) Split it into purpose-specific tools, each with its own contract, gating the destructive one separately.
- C) Document each `action` value more thoroughly in the tool's description text.
- D) Keep the single tool but block `close_account` actions specifically with a hook.

**Question 15.** A customer's first message is: "I've been through this twice with your bot already. Get me a human. Now." The agent's current behavior is to attempt a resolution first, escalating only if that fails. What should it do?

- A) Escalate immediately with a detailed case summary — an explicit human request is honored as stated.
- B) Acknowledge the frustration, briefly note that the agent can likely resolve it faster, and proceed with the fix.
- C) Ask the customer to describe the issue one more time, then decide how to proceed.
- D) Attempt one quick resolution pass first, escalating the moment that attempt doesn't succeed.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation, with custom slash commands, CLAUDE.md configurations, and both plan mode and direct execution.

---

**Question 16.** Your `/gen-migration` skill generates database migrations, but developers keep invoking it bare — `/gen-migration` — and get generic scaffolds because the skill never learns the target table. What frontmatter option addresses this?

- A) Set `context: fork`, so the skill runs in isolation and asks its own clarifying questions.
- B) Restrict `allowed-tools` so the skill physically cannot run until a table name is specified somewhere in context.
- C) Add a `paths` restriction limiting the skill to migration directories only.
- D) Add `argument-hint` frontmatter, prompting developers for the required table-name parameter on bare invocation.

**Question 17.** You want to experiment with an aggressive variant of the team's shared `/test-gen` skill — different coverage strategy, different output style — without changing anyone else's workflow. What is the recommended approach?

- A) Edit the shared project skill directly, but commit the change to a long-lived branch nobody else pulls from.
- B) Add an environment variable to the shared skill that switches to your experimental behavior when it's set.
- C) Create a personal variant under `~/.claude/skills/` with a different name from the shared one.
- D) Copy the skill into `.claude/skills/` under the same name so your version shadows the team's.

**Question 18.** You're migrating from Moment.js to date-fns across the codebase. You want to explore usage patterns and settle a conversion strategy before touching code, then apply the strategy efficiently. How should you use Claude Code's modes?

- A) Use direct execution throughout — a mechanical migration like this never benefits from planning first.
- B) Use plan mode for the investigation and strategy decision, then switch to direct execution to implement it.
- C) Stay in plan mode throughout, since a migration this large should never leave planning.
- D) Alternate modes file by file, planning each individual file immediately before you edit it.

**Question 19.** Your project's CLAUDE.md has grown to 1,200 lines mixing testing standards, API conventions, deployment procedures, and security rules. Finding and maintaining anything is painful. What is the recommended reorganization?

- A) Split it into focused, topic-specific files under `.claude/rules/` (e.g., `testing.md`, `api-conventions.md`).
- B) Sort the existing file alphabetically by topic, normalize the heading levels, and add a table of contents at the top.
- C) Move the whole file to the team wiki, replacing CLAUDE.md with a one-line link and a short structured summary of what's there.
- D) Compress it by removing the examples and explanations, keeping only the bare rules.

**Question 20.** All code under `packages/mobile/` — and only that code — must follow your mobile team's conventions (navigation patterns, platform-specific error handling). The rest of the repo has different standards. What is the simplest correct placement?

- A) Create a `.claude/rules/` file scoped with `paths: ["**/*"]` that contains both convention sets together.
- B) Put both convention sets in the root CLAUDE.md, with a note that one section applies only to mobile code.
- C) Create a skill that mobile developers must invoke manually at the start of each session.
- D) A CLAUDE.md inside `packages/mobile/`, since the conventions scope to one self-contained subtree.

**Question 21.** Claude's data-migration script works except it crashes on rows with null values in the `legacy_status` column. You've explained the problem twice in prose without a reliable fix. What feedback is most likely to produce the correct fix?

- A) Give a longer prose explanation covering nulls, empty strings, and undefined values in general terms.
- B) Send a link to the database schema documentation for the `legacy_status` column.
- C) Give a specific failing test case: an input row containing the null, plus the exact expected output.
- D) Ask Claude to re-read its own script and find the bug on its own.

**Question 22.** Claude's latest change has three problems: an incorrect log format, an off-by-one in pagination, and missing type hints — three unrelated parts of the code, no interaction between fixes. A teammate insists all three must be sent in one combined message "or the fixes will conflict." What is the right guidance?

- A) The teammate is right for multi-issue feedback — batching all three in one detailed message avoids the model re-litigating and second-guessing earlier fixes as it works through each one.
- B) These issues are independent, so sequential iteration works fine; batching matters only when fixes would interact.
- C) Neither approach works well here; regenerate the whole change as a structured diff from scratch instead.
- D) Send one issue per session, starting a brand-new session for each individual fix.

**Question 23.** You're about to have Claude implement a caching layer for your API — a domain where you know invalidation strategy, TTL policy, and stampede protection matter but you haven't thought them through. Which technique best surfaces these decisions before code gets written?

- A) Use the interview pattern: have Claude ask about invalidation, failure modes, and consistency requirements first.
- B) Have Claude generate three alternative implementations of the cache and pick whichever one looks best.
- C) Implement the cache quickly and let production load testing reveal whatever gaps show up.
- D) Hand Claude a list of caching libraries and let it choose one to build with.

**Question 24.** You've built a personal `/standup-notes` command that formats your daily notes — useful to you, irrelevant to teammates. Where does it belong?

- A) Put it in `.claude/commands/` in the repository, since that's the conventional place commands live.
- B) Add it to the project CLAUDE.md as an always-available instruction for the whole team.
- C) Add it as a gitignored file inside `.claude/commands/`, kept out of version control but still tracked locally in the project directory for convenience.
- D) Put it in `~/.claude/commands/` — user-scoped commands are the intended home for personal, individually-useful workflows.

**Question 25.** Twice this month you've had to revert half-completed refactors after discovering mid-way that the approach conflicted with how another module worked. Both refactors touched many files and had multiple viable designs. What practice prevents this?

- A) Make commits smaller, so reverting is cheaper on the occasions a conflict does appear.
- B) Add a rule limiting refactors to touching at most five files per session.
- C) Enter plan mode first to explore and validate the design before committing to any changes.
- D) Run the full test suite after each individual file edit during the refactor.

**Question 26.** Late in a long session, Claude contradicts architecture answers it gave correctly two hours ago. You have several hours of work left. What practice keeps the remaining work grounded?

- A) Correct each contradiction conversationally as it appears.
- B) Have Claude record key findings in a scratchpad file as it works and consult it for later answers.
- C) Ask Claude to summarize everything it has learned so far in its very next reply, then continue the rest of the session exactly as before, unaided.
- D) Restart the session and work from memory.

**Question 27.** Your build-and-test MCP tool returns ~300 lines of logs per run; you run it constantly, and only the pass/fail status and failing test names ever matter to the agent. Sessions degrade after a dozen runs. What is the right fix?

- A) Run builds less often, batching several changes together into each run.
- B) Switch to a model with a larger context window that can absorb the logs.
- C) Pipe the logs to a file and have the agent Read the file only when the details are actually needed.
- D) Trim the output to status, failing test names, and the first error before it enters context.

**Question 28.** You've finished a two-hour exploration phase and are about to start the implementation phase of the same large task. The session is at 70% context. What does the guide recommend before proceeding?

- A) Summarize the exploration phase's findings and start implementation with that summary injected as context.
- B) Push on into implementation without pausing — the fresh work will gradually displace the two hours of old exploration context anyway, given enough turns.
- C) Manually delete the exploration-phase messages from the conversation transcript before continuing.
- D) Ask Claude to be brief from now on, to conserve the remaining context budget.

**Question 29.** You ask Claude to analyze a 25-file diff pasted as one long message. The analysis is sharp for the first and last few files and superficial for the middle of the diff. Which restructuring most directly addresses the cause?

- A) Paste the diff in reverse order, so the files that were previously neglected come first instead.
- B) Lead with a priority summary, then organize the diff under explicit per-file section headers.
- C) Ask Claude to "grade every file in the diff with equal rigor" as a direct instruction.
- D) Raise `max_tokens` so the analysis is allowed to run longer overall.

**Question 30.** An internal code-assistant chat tool your team built on the Claude API forgets constraints developers stated four turns earlier. Inspecting the client, you find each API call sends only the newest user message. What is the fix?

- A) Add a system prompt instruction telling the model to remember all prior constraints.
- B) Increase `max_tokens` so that more context can fit into each response.
- C) Send the complete conversation history with each request to the API.
- D) Have users restate their constraints every few turns as a workaround for the client.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You're wiring the SDK response handler. Which `stop_reason` value tells your code the model has finished its work and the response text should be presented to the developer?

- A) `"end_turn"` — the model has completed its turn with no further tool calls pending.
- B) `"tool_use"` — the model has finished selecting which tools it wants to call.
- C) `"max_tokens"` — the model has said everything it possibly can before being cut off by truncation.
- D) `"stop_sequence"` — the model reached a configured stop string, its natural conclusion.

**Question 32.** Yesterday your agent built a thorough analysis of the repo in a named session. Overnight, a sweeping dependency upgrade changed imports in roughly 60% of files. You need analysis-informed help today. What is the most reliable continuation?

- A) Resume the named session and simply mention in a message that "some files changed."
- B) Start a new session seeded with a structured summary of yesterday's durable findings.
- C) Resume the session and have it re-Read every file it previously analyzed, one by one, to refresh its view.
- D) Fork the session so the stale analysis is preserved untouched in the parent branch.

**Question 33.** The agent generated a 20-file changeset. A single review pass over all 20 files produces uneven depth and missed an inter-file API mismatch. How should the review be structured?

- A) Run two full passes over all 20 files, keeping only the findings that show up identically in both passes.
- B) Run one pass over just the 10 riskiest files, ignoring the rest of the changeset.
- C) Run one pass with an added instruction to allocate equal attention to every file.
- D) Per-file passes for local issues, plus a separate integration pass for cross-file data flow.

**Question 34.** Your agent needs three independent investigations — git history of a module, its test coverage, and its dependency audit — before proposing a refactor. How should the coordinator spawn them for minimum wall-clock time?

- A) Spawn them across three consecutive turns, carefully reviewing each investigation's full result and cross-referencing it before starting the next one.
- B) Combine all three into one subagent prompt for a single sequential investigation.
- C) Emit three Task tool calls within one coordinator response so the subagents run concurrently.
- D) Skip subagents entirely and run all three investigations inline in the coordinator.

**Question 35.** Policy: the productivity agent must never write to `config/production/`. It has broad Write access for scaffolding elsewhere, and CLAUDE.md states the rule, but a near-miss occurred last week. What is the correct enforcement?

- A) Add a hook that intercepts Write/Edit tool calls and blocks any targeting `config/production/` paths.
- B) Remove the Write tool from the agent everywhere, including the scaffolding work it legitimately needs elsewhere in the repo.
- C) Move the production configuration files outside the repository entirely.
- D) Strengthen the CLAUDE.md wording, call the rule deterministic, and add it again to every individual skill.

**Question 36.** A developer asks the agent to rename a variable in one file. Logs show the full multi-agent pipeline spun up — test-writer, doc-writer, and refactor subagents all invoked — for a 30-second task. What is the architectural fix?

- A) Cap the number of subagents the coordinator can invoke at two per request.
- B) Remove the coordinator entirely and let developers pick subagents manually themselves.
- C) Make the multi-agent pipeline run faster overall, so unnecessary invocation costs less time when it happens.
- D) Have the coordinator assess task complexity and invoke only the subagents each task actually requires.

**Question 37.** Early in a session the coordinator discovered the project's testing conventions. It then spawns a test-writer subagent, whose output ignores every one of those conventions. Why?

- A) The test-writer's underlying model tier is too weak to follow written conventions.
- B) The subagent's prompt didn't include the conventions — subagents don't inherit the coordinator's history.
- C) The test-writer's AgentDefinition is missing a `memory: shared` setting that would enable structured context inheritance.
- D) The Task tool strips formatting from prompts, garbling the conventions it was given.

**Question 38.** Asked to "improve error handling across our services," the coordinator decomposed the work into subtasks for just two of the seven services, and the final report claims completion. What is the root-cause fix?

- A) Instruct the subagents to volunteer for additional services on their own once they finish their originally assigned service ahead of schedule.
- B) Add more subagents to the pipeline so more services get covered by chance.
- C) Fix the coordinator's decomposition — enumerate the full scope before creating subtasks, with coverage criteria.
- D) Have the report generator flag which services it wasn't given any data for.

**Question 39.** Your utilities are re-exported through several `index.ts` barrel files, so importers reference the barrel, not the source file. You need every real usage of the functions defined in `src/util/dates.ts`. What is the right built-in tool strategy?

- A) Enumerate all names exported from `dates.ts` (directly and via barrels), then Grep for each name.
- B) Glob for every `**/index.ts` barrel file and read through each one manually.
- C) Grep for the exact string `src/util/dates` across the codebase and treat those importers as the full usage list.
- D) Read `dates.ts` and rely on the IDE's reference count from memory instead of a fresh search.

**Question 40.** The agent must locate every Storybook story file — they follow the `*.stories.tsx` naming convention and are scattered throughout `src/`. Which tool fits?

- A) Grep for the literal string "storiesOf" across every file's contents.
- B) Read the Storybook configuration file and infer the likely story file list from what it declares.
- C) Glob with the pattern `**/*.stories.tsx` to match the naming convention directly.
- D) Run a Bash `find` command piped through several chained greps.

**Question 41.** Two edits are queued: (a) completely regenerate a 15-line config file from a new template; (b) rename one function in a 2,000-line module. Which tool pairing is correct?

- A) Use Edit for the small config file and Write for the large module's targeted rename.
- B) Use Write for the config regeneration and Edit for the targeted rename in the large module.
- C) Use Edit for both changes, since Edit forces you to validate the surrounding anchor text before writing, unlike Write.
- D) Use Write for both changes — full-file writes are more predictable than targeted edits.

**Question 42.** You found a promising community MCP server for database introspection and want to trial it for a week before proposing it to the team. Where do you configure it?

- A) In the project's `.mcp.json`, marked with a comment saying "experimental."
- B) In the project's CLAUDE.md, so its usage is at least written down for anyone who looks.
- C) In `.claude/rules/`, committed for the team but with a path scope limiting its documented usage to only your own working files for now.
- D) Configure it in your user-scoped `~/.claude.json`, keeping the project configuration clean for the team.

**Question 43.** Your system prompt says: "Always use the ripgrep-mcp tool for searching." Now the agent uses it even to find files by name — where Glob is correct — and results have gotten worse. What is the underlying lesson?

- A) Keyword-mandate instructions override sensible per-task tool selection — describe when the tool applies instead.
- B) MCP search tools should never be configured alongside built-in search tools in the same project, since the two inevitably compete for the same queries.
- C) The instruction just needed the word "content" added somewhere — one extra word would fix everything.
- D) ripgrep-mcp's tool description is too weak to constrain an instruction phrased this way.

**Question 44.** Before choosing where to hook a new plugin system, the agent must survey twelve candidate modules. You want the survey's verbose output kept away from the main session, which will do the actual design work. What is the right mechanism?

- A) Read all twelve modules directly in the main session, then run `/compact` afterward to shrink it back down.
- B) Survey four modules per session, spread the work out across three separate sessions.
- C) Use the Explore subagent for the survey, keeping the verbose discovery isolated from the main context.
- D) Skip the survey and choose the hook point straight from the architecture diagram.

**Question 45.** Your `/brainstorm-designs` skill generates several speculative design alternatives with pros and cons. After running it, the main session keeps referencing rejected alternatives as if they were decisions. What fixes this?

- A) Run the skill inside a permanent dedicated session, saving each structured output for later reference, used only for brainstorming.
- B) Add `context: fork` to the skill so the exploratory content stays isolated, returning only the outcome.
- C) Add a closing line to the skill's output stating that the alternatives above are hypothetical, not decisions.
- D) End every brainstorm by asking Claude to forget the rejected options it just proposed.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your pipeline requires `extract_metadata` to run on every document before any enrichment tool may be called. The model usually complies with the prompt instruction but occasionally jumps straight to enrichment. What guarantees the ordering?

- A) Force it: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, then normal tool choice afterward.
- B) Set `tool_choice: "any"` so that some tool is always called first, whichever one the model prefers.
- C) List `extract_metadata` first in the tools array, since array order implies calling priority.
- D) Add few-shot examples in the prompt demonstrating metadata-first ordering of tool calls.

**Question 47.** You're designing the invoice schema and must decide which fields are `required`. Which principle is correct?

- A) Mark all business-critical fields required, so the schema signals to the model exactly how much each one matters.
- B) Mark everything optional to maximize flexibility across every document variant received.
- C) Require only fields that are genuinely present across the documents; make possibly-absent fields optional or nullable.
- D) Mark required whatever fields the downstream system needs, regardless of what the documents actually contain.

**Question 48.** You're extracting quantities from maintenance logs where technicians write informally: "topped off with about half a jug," "roughly two dozen bolts." The model keeps outputting precise-looking fabricated numbers. What is the most effective mitigation?

- A) Add a regex validator that rejects any suspiciously precise-looking numeric value outright.
- B) Instruct the model in the system prompt to normalize vague phrasing and never guess at a quantity.
- C) Route every log containing the word "about" straight to human review.
- D) Add few-shot examples mapping informal measurements to an estimate with a flag, or to null.

**Question 49.** Academic papers in your corpus vary structurally: some use inline citations, others end-of-paper bibliographies; some have a dedicated methodology section, others embed methods in results. Extraction quality varies wildly with the structure. What is the recommended fix?

- A) Preprocess every paper into one canonical structure before extraction ever begins.
- B) Add few-shot examples demonstrating correct extraction from each structural variant in the corpus.
- C) Build one separate extraction prompt per journal, routed automatically by source at intake.
- D) Extract only from papers that match the single most common structure in the corpus.

**Question 50.** Since adopting tool_use with a strict schema, outputs always validate — but spot checks find the vendor's name in the `customer_name` field and the invoice date in `due_date`. What does this demonstrate?

- A) Strict schemas eliminate syntax errors, not semantic ones — add cross-field checks and sampled audits.
- B) The schema's field names are too similar to each other and must be renamed to be more distinct.
- C) The source documents themselves are too noisy for automated extraction to ever be reliable here.
- D) `tool_choice: "any"` is needed to make field mapping more reliable going forward.

**Question 51.** An extraction fails Pydantic validation. You will retry. Which retry request gives the model the best chance of a correct second pass?

- A) Send the same request again — the model usually self-corrects on a second sample.
- B) Send just the validation error text, to keep the retry request cheap.
- C) Send the original document, the failed extraction, and the specific validation errors together.
- D) Send the failed extraction back with an instruction to "fix the errors."

**Question 52.** Documents arrive continuously and your contract guarantees results within 30 hours. Batch processing can take up to 24 hours. Which submission schedule guarantees the SLA while minimizing submission overhead?

- A) Submit one batch daily — 24-hour accumulation plus 24-hour processing stays under two days.
- B) Submit every 12 hours with a priority flag attached to the older documents.
- C) Submit every 8 hours — the tighter cadence usually leaves several hours of margin in practice, and matches typical document arrival patterns closely enough.
- D) Submit a batch every 4 hours, increasing frequency to keep the worst case comfortably inside the 30-hour SLA.

**Question 53.** Two extraction workloads: (1) a compliance archive of 80,000 historical contracts to process this quarter; (2) a customer-facing upload flow where the user watches a spinner until their document's data appears. How do you assign APIs?

- A) Use the Batch API for both workloads — the cost savings apply equally to each.
- B) Batch API for the archive; synchronous API for the upload flow a user is actively watching.
- C) Use the synchronous API for both — simpler architecture beats the cost savings here.
- D) Use synchronous for the archive to finish it faster; batch for uploads, with results emailed afterward.

**Question 54.** You've submitted a batch of 2,000 extraction requests. How does your pipeline obtain and correlate the results?

- A) Poll the batch's status until processing completes, then retrieve results and correlate them by `custom_id`.
- B) Results stream back over a webhook, arriving in the same order they were submitted.
- C) The submission call blocks until every one of the results is ready, then returns the complete set back to the caller in the original submission order.
- D) Results are emailed back as a signed archive once the whole batch finishes.

**Question 55.** Scanned approval forms have checkboxes that are sometimes too degraded to read. The schema's `decision` field is an enum: `["approved", "rejected"]`, and the model currently guesses. What is the correct schema change?

- A) Lower the scan-quality threshold so degraded forms are rejected at intake instead of processed.
- B) Add an `ocr_confidence` float field to the schema and validate that any guess scoring above 0.8 is accepted automatically.
- C) Make `decision` free text so the model can express its uncertainty in its own words.
- D) Add an `"unclear"` enum value for ambiguous cases and route those extractions to human review.

**Question 56.** Your extraction step also self-checks its output ("verify your extraction before finalizing") and reports near-zero errors — but human audits find real mistakes it never catches. What is the structural fix?

- A) Make the self-check mandatory by forcing it through `tool_choice` on every single extraction the pipeline runs, with no exceptions carved out.
- B) Strengthen the self-check prompt with a validated checklist of common error types.
- C) Run an independent verification pass in a fresh model instance, without the extractor's reasoning context.
- D) Ask for a confidence score alongside the self-check and audit only the low-scoring extractions.

**Question 57.** Next week you'll batch-process 50,000 archived contracts with a newly written extraction prompt. What should happen first?

- A) Split the archive into ten 5,000-document batches and fix the prompt between each one.
- B) Submit the full batch first — its results become the evaluation set used for prompt refinement afterward.
- C) Run the whole archive through a cheaper model first, as a smoke test of the approach.
- D) Refine the prompt on a representative sample using the synchronous API, then submit the full batch.

**Question 58.** Your OCR agent hands its output to a validation agent whose context budget is small. Currently it sends the full raw text plus its complete reasoning narrative, and the validation agent truncates. What is the right change?

- A) Double the validation agent's context budget so the full raw text and narrative fit.
- B) Have the upstream agent return structured data — key facts, source locations, flags — sized for the consumer.
- C) Have the validation agent request additional pages from the source document on demand instead.
- D) Compress the OCR text with an extra summarization pass before sending it along.

**Question 59.** An extracted vendor name matches three different vendor records in your master file. The pipeline currently auto-selects the most recently active vendor. What should it do instead?

- A) Treat the multiple match as ambiguity: disambiguate using identifiers found in the document, and route to review only if that fails.
- B) Auto-select the vendor with the closest string match to the extracted name instead of recent activity.
- C) Create a brand-new vendor record so the pipeline avoids guessing among the three existing ones.
- D) Auto-select the vendor with the highest transaction volume, the statistically likeliest match.

**Question 60.** Your extraction summary report converts everything to prose paragraphs — including line-item tables and numeric comparisons — and reviewers say checking figures is painful. What is the recommended presentation?

- A) Convert everything to tables instead of prose, since reviewers generally prefer scanning tables.
- B) Provide raw JSON to reviewers, who can format it into whatever shape they need themselves.
- C) Render each content type appropriately — tables for financial data, prose for narrative, lists for findings.
- D) Add a "figures appendix" that repeats all the numbers again at the end of the prose section.

---
# Answer Key — Practice Exam 8

**Quick key:** 1-D, 2-B, 3-A, 4-C, 5-B, 6-D, 7-A, 8-C, 9-B, 10-D, 11-C, 12-A, 13-D, 14-B, 15-A, 16-D, 17-C, 18-B, 19-A, 20-D, 21-C, 22-B, 23-A, 24-D, 25-C, 26-B, 27-D, 28-A, 29-B, 30-C, 31-A, 32-B, 33-D, 34-C, 35-A, 36-D, 37-B, 38-C, 39-A, 40-C, 41-B, 42-D, 43-A, 44-C, 45-B, 46-A, 47-C, 48-D, 49-B, 50-A, 51-C, 52-D, 53-B, 54-A, 55-D, 56-C, 57-D, 58-B, 59-A, 60-C

---

**1. D** — Text content is not a completion signal: responses routinely carry narration alongside `tool_use` blocks. The loop must inspect `stop_reason` and continue on `"tool_use"`. A inverts a check that shouldn't exist. B tries to prompt around a control-flow bug instead of fixing the loop. C doubles down on the wrong signal by requiring more of it.

**2. B** — When identity verification must be guaranteed before account mutations, only a programmatic prerequisite (blocking mutation tools until `get_customer` returns a verified ID) is deterministic. A and C are prompt-layer measures with non-zero failure rates — the incident already proves the point. D adds customer friction without enforcement.

**3. A** — A compliance rule with audit findings needs hook-level interception: check the final-sale flag on `process_refund` calls, block, and redirect to the store-credit workflow. C is more prompt emphasis on an already-stated rule. D destroys the agent's core capability to fix one policy edge. B tightens human review after the fact but doesn't stop the refund at the moment it happens.

**4. C** — A `PostToolUse` hook mapping numeric tiers to names normalizes the data before the model reasons over it — deterministic, and it keeps the system prompt free of a conversion table the model has to consult. A and D rely on the model performing the conversion correctly every time. B may be right long-term but is out of your control and slow.

**5. B** — Match decomposition to the workflow: fixed sequential chains for predictable flows (warranty), dynamic decomposition driven by intermediate findings for open-ended investigations (fraud). A adds adaptive overhead and unpredictability to a flow that never varies. C scripts the unscriptable. D abandons the structure that makes the predictable flow reliable.

**6. D** — Pre-routing by keyword replaces the model's contextual judgment with a brittle pattern match — the exact failure the example shows ("do NOT want a refund"). Model-driven agents exist because intent requires context. A and B upgrade the router instead of removing an unnecessary layer. C patches the symptom downstream.

**7. A** — The pattern for multi-concern requests: decompose into distinct concerns, investigate in parallel using shared context, synthesize a unified resolution — correctness *and* speed. B and C degrade the customer experience to fit the architecture. D speeds up a sequential design instead of fixing it.

**8. C** — Tool results return as a `tool_result` block referencing the `tool_use` ID, inside a user-role message, with the updated conversation sent back — that's how the model incorporates the data into its next step. A corrupts the roles (the model didn't say it, no matter how the message is dressed up). B misuses the system prompt for turn-level data. D throws away the conversation state the resolution depends on.

**9. B** — Tool descriptions should document input formats, example queries, and boundary behavior; the agent is guessing because one line tells it nothing about accepted identifiers. A and C build infrastructure (a translation layer, a looser input schema) to tolerate a documentation gap. D makes failure cheaper rather than rarer.

**10. D** — A gateway timeout is a transient error: `errorCategory: "transient"`, `isRetryable: true`, plus a description lets the agent retry sensibly. A mislabels it non-retryable, abandoning refunds that would succeed. B reports success for an operation that didn't complete — dangerous. C returns the agent to guessing.

**11. C** — These tools have distinct purposes hidden behind near-identical descriptions; rewriting both to state purpose, inputs, outputs, and when to choose each fixes selection at the root. A merges two legitimately different access patterns. B removes needed functionality. D hardcodes a preference instead of enabling a choice.

**12. A** — MCP resources exist to expose content catalogs, giving the agent visibility into available policy documents without exploratory probing. B bloats every conversation with the full manual. C is out of scope and disproportionate. D makes repeated probing cheaper, not unnecessary.

**13. D** — Scoped cross-role tools serve high-frequency needs safely: a read-only `get_order_status` gives the escalation agent what it uses constantly, while modification stays with the role that owns it. A leaves the dangerous capability reachable and only logs the damage afterward — a hook here catches, not prevents. B removes a legitimate need. C doubles the exposure.

**14. B** — A mode-switched tool with a destructive branch is the case for splitting into purpose-specific tools with individual contracts — misselecting an enum value should never close an account. A and C leave one entry point where a parameter typo is catastrophic. D keeps the confusing design and bolts a gate onto one branch.

**15. A** — An explicit customer request for a human is a defined escalation trigger to honor immediately — investigation attempts after "get me a human, now" erode trust. B applies the acknowledge-and-resolve pattern that belongs to frustrated customers who *haven't* explicitly demanded a human. C and D both do what the customer asked you not to do.

**16. D** — `argument-hint` frontmatter prompts developers for required parameters when the skill is invoked without arguments — precisely the failure here. A changes execution isolation, not input collection. B misuses a tool-permission control to gate on a value it can't inspect. C isn't skill frontmatter for this purpose.

**17. C** — Personal skill customization: create a variant under `~/.claude/skills/` with a different name, so teammates' workflow is untouched. A ships team-visible changes to a shared artifact. B adds a hidden mode to a shared skill. D shadows the team's skill under the same name — exactly the collision to avoid.

**18. B** — Combine the modes: plan mode for exploring usage patterns and settling the conversion strategy, direct execution to apply the planned approach. A skips the design decision that determines the migration's quality. C never ships. D fragments a strategy decision that should be made once.

**19. A** — The recommended structure for an overgrown CLAUDE.md is topic-specific files in `.claude/rules/` (`testing.md`, `api-conventions.md`, …). B reorganizes without reducing the monolith. C makes the content invisible to Claude, which doesn't browse the wiki. D strips the examples that make conventions followable.

**20. D** — Conventions scoped to one self-contained subtree are the fit for a directory-level CLAUDE.md inside `packages/mobile/`. A loads both convention sets everywhere via a root-scoped rules file. B loads mobile rules in every session and relies on the model to scope them from a note. C applies conventions only when someone remembers to invoke it.

**21. C** — For edge-case fixes, provide a specific test case: example input containing the null and the exact expected output. That's unambiguous in a way prose has already failed to be. A is more prose. B provides background, not the expected behavior. D re-asks the model to find what it's already missed twice.

**22. B** — Independent problems can be fixed sequentially; the single-detailed-message guidance applies when fixes interact and would invalidate each other. A applies the interacting-issues rule to issues that don't interact. C is disproportionate — regenerating structured output from scratch throws away working code over three unrelated nits. D adds session churn with no benefit.

**23. A** — The interview pattern targets unfamiliar domains with unarticulated constraints: Claude asks about invalidation, failure modes, and consistency before implementing — surfacing exactly the considerations you know you haven't thought through. B generates three versions of the same blind spots. C discovers requirements in production. D picks a library, not a design.

**24. D** — Personal, team-irrelevant commands belong in `~/.claude/commands/` (user-scoped); `.claude/commands/` is for team-shared, version-controlled commands, so A places it in the wrong scope even though the path looks conventional. B misplaces a command as an instruction. C pollutes the project directory to simulate what user scope already provides.

**25. C** — Multi-file changes with multiple viable designs are plan mode's core case: explore and validate the approach before changing code, preventing exactly this costly rework. A cheapens the failure instead of preventing it. B is an arbitrary constraint unrelated to the cause. D catches breakage, not design conflicts.

**26. B** — This is context degradation in an extended session; the countermeasure is a scratchpad file of key findings, recorded as discovered and consulted for later answers — persistent ground truth outside the degrading context. A fixes symptoms one at a time, forever. C puts the summary into the same degrading context. D loses the accumulated understanding entirely.

**27. D** — Verbose tool outputs consume context disproportionately to their relevance; trim to the fields that matter (status, failing tests, first error) before results accumulate. A slows the feedback loop that makes the agent useful. B postpones the problem to a future budget crunch. C still spends the context whenever the file is actually read, and adds an extra step.

**28. A** — The phase-transition practice: summarize key findings from the completed exploration phase and inject the summary as initial context for the next phase or subagents. B lets implementation compete with exploration residue at 70% full. C isn't a reliable operation to do by hand mid-session. D conserves output tokens, not context already spent.

**29. B** — Uneven middle coverage of a long uniform input is lost-in-the-middle; the mitigation is a priority summary at the start plus explicit per-file section headers. A moves the blind spot rather than removing it. C — exhortation doesn't change position effects. D lengthens the answer, not the attention.

**30. C** — The API is stateless: each request must carry the complete conversation history, or earlier constraints simply don't exist for the model. A instructs it to remember what it was never sent. B is unrelated to missing input. D makes users compensate for a client bug.

**31. A** — `"end_turn"` signals the model has completed its turn with no pending tool work — time to present the response. `"tool_use"` (B) means work remains. `"max_tokens"` (C) means truncation, not completion. D — stop sequences are a different, configured mechanism.

**32. B** — With ~60% of analyzed files changed, the session's tool results are mostly stale; starting fresh with a structured summary of durable findings is more reliable than resuming. A resumes atop stale data with a vague warning. C re-does the analysis inside a context already full of the old one. D preserves staleness in two places.

**33. D** — Uneven depth plus a missed cross-file issue is attention dilution: split into per-file passes for local issues and a dedicated integration pass for cross-file data flow. A double-spends on the same diluted view and suppresses intermittent catches. B trades coverage for depth by guesswork. C — instructions don't reallocate attention.

**34. C** — Independent investigations parallelize by emitting multiple Task tool calls in a single coordinator response. A serializes them across turns. B serializes them inside one context. D floods the coordinator's context with three investigations' worth of raw output.

**35. A** — A must-never rule with a near-miss on record needs interception: a hook blocking Write/Edit calls targeting `config/production/` paths. B removes a capability the agent legitimately needs elsewhere. C reorganizes the repo around a missing guardrail. D adds prompt emphasis and a label where prompts already failed — calling a rule "deterministic" in the text doesn't make it enforced.

**36. D** — Coordinators should assess query complexity and invoke only the subagents a task needs — a one-line rename needs none. A caps waste at two subagents instead of zero. B removes orchestration rather than fixing its judgment. C optimizes the cost of doing the wrong thing.

**37. B** — Subagents don't inherit the coordinator's conversation history; the conventions discovered this session had to be included in the test-writer's prompt explicitly. A and D invent failure mechanisms. C references a `memory: shared` setting that doesn't exist — there is no inheritance to switch on.

**38. C** — The subagents completed their assignments; the coverage failure happened at decomposition. Fix the coordinator: enumerate the full scope before creating subtasks and check decomposition against coverage criteria. A asks workers to fix planning. B adds capacity without direction. D reports the gap instead of closing it.

**39. A** — Barrel re-exports mean importers reference the barrel, so tracing requires two steps: enumerate the exported names, then Grep for each name across the codebase. B finds the barrels, not the users. C finds only direct-path importers — the minority. D isn't grounded in the current code.

**40. C** — Finding files by naming convention is Glob's exact purpose: `**/*.stories.tsx`. A searches contents for an API string many stories won't contain. B infers instead of matching. D reimplements Glob with more failure modes.

**41. B** — Write is for full-file creation/replacement (the regenerated config); Edit is for targeted modifications via unique anchor text (the rename in a large file). C forces anchor-matching on a total rewrite — Edit's anchor requirement isn't a validation feature for a from-scratch file, it's overhead. D rewrites 2,000 lines to change one name — slow and risky. A is backwards on both.

**42. D** — Personal and experimental MCP servers belong in user-scoped `~/.claude.json`; project `.mcp.json` is for shared team tooling. A ships your experiment to everyone. B documents without configuring. C misuses a rules mechanism for server configuration.

**43. A** — The system prompt's "always use X" phrasing is a keyword-sensitive instruction that creates an unintended blanket association, overriding sensible per-task tool selection. The fix is describing when the tool applies, not mandating it unconditionally. B and D misplace the blame. C patches this instance of a pattern worth learning generally.

**44. C** — The Explore subagent isolates verbose discovery and returns a summary — the main session keeps its context for design. A spends the main context first and summarizes after the damage. B splits the survey but loses cross-module comparison. D skips the evidence the decision needs.

**45. B** — Exploratory, speculative content is what `context: fork` is for: the brainstorm runs isolated, and only the outcome returns — rejected alternatives never enter the main conversation to be misremembered as decisions. A quarantines by convention, not mechanism. C and D ask the model to disregard context it has already absorbed.

**46. A** — Guaranteeing that a specific tool runs first requires forced tool selection: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, with enrichment handled in follow-up turns. B guarantees *a* tool, not *that* tool. C — array order carries no such semantics. D remains probabilistic.

**47. C** — Required should mean "genuinely present across the documents." Fields that may legitimately be absent must be optional/nullable, or the model is pressured to fabricate values to satisfy the schema. A confuses importance with presence. B loses real invariants. D encodes downstream wishes the documents can't honor.

**48. D** — Few-shot examples demonstrating informal-measurement handling (approximate value + estimate flag, or null when unquantifiable) teach a judgment the model generalizes — few-shot is the cited technique for reducing extraction hallucination. A catches some fabrications after the fact. B is a vague instruction where examples are the effective tool. C outsources a solvable pattern.

**49. B** — Structural variety is the textbook few-shot case: examples demonstrating correct extraction from each variant (inline vs bibliography, dedicated vs embedded methodology) let the model handle the spread. A presumes a reliable universal normalizer. C multiplies prompts to dodge generalization. D silently shrinks coverage.

**50. A** — Schema-valid output with values in the wrong fields is a semantic error — the class strict schemas cannot prevent. Add semantic validation: cross-field consistency checks and sampled audits. B might help marginally but misses the general lesson. C gives up on a solvable problem. D governs *whether* a tool is called, not field accuracy.

**51. C** — Effective retries carry the original document, the failed extraction, and the specific validation errors — everything needed for targeted self-correction. A relies on luck. B and D omit the source document, so the model can't re-ground the corrected values.

**52. D** — Worst case must fit the SLA: a document arriving just after a submission waits the full interval plus processing. A 4-hour cadence: 4 + 24 = 28 ≤ 30, with margin. A's worst case is 48 hours; B's is 36; C's is 32 — over the line, and "usually leaves margin" isn't a guarantee.

**53. B** — Match API to latency tolerance: the archive is the Batch API's ideal case (huge, non-blocking, 50% cheaper); the upload flow has a human watching a spinner — synchronous. A leaves users staring at spinners for potentially hours. C forfeits large savings for no benefit. D is backwards on both workloads.

**54. A** — Batch results are obtained by polling for completion, then retrieving the result set and correlating each entry back to its request via the `custom_id` set at submission. B, C, and D describe delivery mechanisms the Batch API doesn't have (ordered streaming webhooks, blocking submission, email delivery).

**55. D** — Ambiguous source data needs an explicit `"unclear"` enum value plus routing to human review — the schema should let the model tell the truth instead of forcing a binary guess. A throws away processable documents. B dresses the guess in a score. C destroys the machine-readable contract downstream systems depend on.

**56. C** — Self-checks inherit the extractor's reasoning and blind spots; an independent verification pass — fresh instance, source document, no prior reasoning or conclusions carried over — catches what self-review structurally cannot. A makes the biased check mandatory. B gives the biased check a checklist. D calibrates a signal produced by the same blind process.

**57. D** — Refine on a representative sample before batch-processing large volumes: first-pass success determines cost when each full pass is 50,000 documents with up-to-24-hour turnaround. B spends an entire full-archive pass to learn what a small sample would teach. A discovers problems 5,000 documents at a time. C tests a different model's behavior, not your prompt's quality on the real one.

**58. B** — When the downstream agent has a limited context budget, modify the upstream agent to emit structured data — key facts, source locations, flags — instead of verbose content and reasoning chains. A scales the budget to fit the waste. C adds round-trips to consume the same verbosity. D compresses prose that shouldn't be prose at all.

**59. A** — Multiple matches are an ambiguity to resolve with additional identifiers (address, tax ID from the document), not a heuristic pick; when identifiers don't resolve it, route to human review. B and D swap one heuristic for another — statistically likely is still a guess with someone's money. C corrupts the master file.

**60. C** — Content types should render in the form that fits them: financial data as tables, narrative as prose, findings as structured lists — uniform formatting is the anti-pattern in both directions. A repeats the mistake with a different uniform. B exports the formatting work to reviewers. D duplicates numbers instead of presenting them properly once.

---

*End of Practice Exam 8.*
