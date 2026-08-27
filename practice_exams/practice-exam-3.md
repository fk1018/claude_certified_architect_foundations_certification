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

- A) Text is not a completion signal by itself, since narration can sit alongside a pending tool call — check `stop_reason` and loop again whenever it reads `"tool_use"`.
- B) Flip the check around: treat a response with zero text content as the one that signals the conversation is actually finished, and keep the rest of the logic as-is.
- C) Put a rule in the prompt instructions telling the model to never emit narration text in the same response as a tool call, so the existing text-based check stays safe to use.
- D) Require two consecutive text-bearing responses in a row, on the theory that a single one might just be mid-turn commentary rather than a real answer.

**Question 2.** Your agent updated a shipping address after matching only the customer's stated name, and the package went to the wrong person's account. The system prompt already says identity must be verified first. How do you make verification a hard guarantee?

- A) Restate the identity-verification rule in both the system prompt and the `update_address` tool description, in stronger and more explicit language than before.
- B) Add several few-shot transcripts of the agent politely refusing an address change until identity is confirmed, so the model has concrete examples to imitate.
- C) Add a programmatic prerequisite that blocks `update_address` and other account mutations until `get_customer` returns a verified customer ID in the session.
- D) Require the customer to type a one-time confirmation phrase read back by the agent before any address change proceeds, logging the phrase for the audit trail.

**Question 3.** Store policy prohibits refunds on final-sale items; the agent should instead explain the policy and offer store credit via escalation. Prompt instructions mostly work, but a compliance audit found four final-sale refunds last month. What closes the gap?

- A) Retrain support staff to catch final-sale refunds during the next daily reconciliation report, and add a line item for it in the weekly compliance summary that leadership reviews each Monday.
- B) Intercept `process_refund` with a hook that checks the item's final-sale flag, blocks the call, and redirects the agent into the store-credit escalation path.
- C) Move the final-sale rule to the very top of the system prompt, set in bold capital letters so the model cannot plausibly claim to have missed it.
- D) Remove `process_refund` from the agent entirely and route every refund request, final-sale or not, straight to a human agent.

**Question 4.** `get_customer` returns the loyalty tier as an integer (1–4), but your system prompt and policies refer to tiers by name ("Silver," "Gold"). The agent sometimes applies the wrong tier's benefits. What is the cleanest fix?

- A) Paste a structured tier-conversion table into the system prompt, listing each integer alongside its tier name so the model can look it up when needed.
- B) File a ticket asking the backend team to change the API so it returns tier names directly, and wait for that change before touching the agent.
- C) Add a batch of few-shot examples that walk through interpreting each numeric tier correctly, covering all four values in worked-out detail.
- D) Add a `PostToolUse` hook that maps the numeric tier to its name in the tool result before the model ever reasons over it.

**Question 5.** Your warranty-claim flow is identical every time (verify purchase → check warranty status → issue RMA), while fraud investigations are open-ended and depend on what each lookup reveals. How should these two workflows be decomposed?

- A) Use a fixed sequential chain for the predictable warranty flow, and dynamic decomposition for fraud, generating each next step from what the prior lookup found.
- B) Use dynamic decomposition for both, since giving the model more freedom to plan its own steps never really hurts even on flows that never change.
- C) Use fixed sequential chains for both, bolting a growing library of fraud-specific branches onto the same script so every possible path is pre-written in advance for reviewers.
- D) Let the model choose its own approach freely for both flows, with no scripting or decomposition guidance beyond the tool descriptions it already has.

**Question 6.** To "speed up easy cases," an engineer added a regex-based intent matcher that pre-routes messages containing "refund" straight to the refund flow before the model sees them. Misrouting complaints have since increased ("I do NOT want a refund, I want a replacement" went to the refund flow). What went wrong?

- A) The regex just needs negative-lookahead patterns added so it can detect common negation phrasing like "do not" before routing the message onward.
- B) Swap the regex for a small dedicated classifier model trained on labeled examples of refund versus non-refund messages, then route on its output.
- C) A keyword router pre-empts the model's contextual judgment; a model-driven agent should reason over full context, so the pre-routing layer should be removed.
- D) Have the refund flow itself double-check the customer's actual intent by asking a clarifying question before it takes any action on the account.

**Question 7.** Customers with three concerns in one message get correct resolutions, but handle time triples because the agent fully investigates each concern one after another. What does the recommended pattern look like?

- A) Limit each conversation to a single concern and ask the customer to send the other two as separate follow-up messages on a different day.
- B) Ask the customer which of the three concerns matters most to them, and only address that one, closing the ticket for the remaining two.
- C) Keep the sequential investigation as-is but cache backend lookups so at least repeated calls to the same order or customer record can be reused across the three concerns.
- D) Decompose the message into its distinct items, investigate them in parallel using the shared conversation context, then synthesize one unified reply.

**Question 8.** In your loop implementation, a response arrives with `stop_reason: "tool_use"`, containing the text "Let me check that order" plus a `lookup_order` call. A junior developer's code displays the text to the customer and waits for the customer's reply. What should the code do instead?

- A) Suppress the narration text entirely — a response paired with a tool call should never be surfaced to anyone on either side of the conversation.
- B) Execute `lookup_order`, append its result to the conversation, and send the whole thing back to the model; the text is narration on an in-progress turn.
- C) Show the narration text to the customer while simultaneously executing the tool in the background, merging the two paths on the customer's next reply.
- D) Return an error back to the model, since a single response combining narration text with a tool call is malformed and should never occur.

**Question 9.** The agent keeps passing customer email addresses to `get_customer`, which only accepts numeric customer IDs, producing a stream of avoidable errors. The tool's description is one line: "Retrieves customer information." What is the right first fix?

- A) Add an application-side hook that quietly rewrites any email-shaped argument into the matching numeric customer ID before the call ever reaches the tool.
- B) Loosen the tool so it accepts either an email or a numeric ID as input, resolving whichever one it receives internally so the agent can't get it wrong.
- C) Rewrite the tool's error messages to be friendlier and more specific, so the agent can recover on the very next attempt after a failed call.
- D) Expand the description to document the accepted format (numeric customer ID), give example calls, and state what to do when only an email is known.

**Question 10.** During a refund, the payment gateway times out. What should `process_refund` return so the agent responds appropriately?

- A) A structured error with `errorCategory: "transient"` and `isRetryable: true`, plus a short description, so the agent knows a retry is worth attempting.
- B) An `isError` result with `retriable: false`, on the reasoning that a gateway which just timed out is unlikely to succeed if the agent tries it again soon.
- C) A success response carrying a `pending: true` flag, since a payment-gateway timeout usually just means the refund is still quietly processing.
- D) A bare, generic failure message with no further detail, leaving the agent to infer from the surrounding conversation what probably went wrong.

**Question 11.** Your tools include `lookup_order` ("Retrieves order details") and `get_order_history` ("Retrieves order information"), and agents interchange them constantly — one returns a single order by ID, the other returns a paginated list of all orders. What is the highest-leverage fix?

- A) Merge the two into a single tool with an optional `order_id` parameter, returning one order when it's supplied and the full history otherwise.
- B) Rewrite both descriptions to state each tool's distinct purpose, inputs, and outputs, including when to reach for one over the other.
- C) Remove `get_order_history` outright, on the theory that `lookup_order` already covers the common case of a customer asking about one order.
- D) Add a system prompt rule instructing the agent to always try `lookup_order` first and only fall back to `get_order_history` if that call fails.

**Question 12.** The agent answers policy questions (return windows, warranty terms) by calling a `search_kb` tool 5–8 times per conversation, probing for the right policy document. How can you give it visibility into what policy content exists without the exploratory calls?

- A) Paste the entire policy manual, cover to cover, into the base instructions so every conversation starts with full knowledge of every policy already loaded.
- B) Fine-tune the underlying model on the full set of policy documents so the correct terms are baked into its weights rather than looked up at runtime.
- C) Expose the policy document catalog as MCP resources, so the agent can see what's available and fetch precisely the document it actually needs.
- D) Cache `search_kb` results across conversations so that, at minimum, the second customer asking about the same policy gets a faster response.

**Question 13.** The escalation-desk agent (a separate agent that manages handoffs) frequently needs just the current status of an order, but its only option is the full order-management suite (`lookup_order`, `modify_order`, `cancel_order`), and it has occasionally modified orders while "checking status." What is the right tool distribution?

- A) Give the escalation agent a scoped, read-only `get_order_status` tool for its high-frequency need, and route anything requiring modification elsewhere.
- B) Keep the full suite in place but add a prompt-level rule instructing the escalation agent never to call the modification tools while it's only performing a routine status check.
- C) Remove every order-related tool from the escalation agent and have it ask the customer to read their own order status back to it verbally.
- D) Grant the full order-management suite to both agents equally, so at least the two agents' available capabilities stay consistent with each other.

**Question 14.** A single `manage_account` tool takes an `action` parameter (`"update_address"`, `"reset_password"`, `"close_account"`). The agent occasionally passes the wrong action — including one accidental account closure. What is the best redesign?

- A) Add a `confirm: true` parameter that must be explicitly set before any action the tool defines as destructive is allowed to actually run.
- B) Expand the tool description with a longer, more thorough write-up of what each of the three action values does and when to use it.
- C) Keep the single tool as-is, but add a validation hook that specifically double-checks and blocks any `close_account` call before it executes.
- D) Split it into separate purpose-specific tools (`update_address`, `reset_password`, `close_account`), each with its own contract, gating the destructive one.

**Question 15.** A customer's first message is: "I've been through this twice with your bot already. Get me a human. Now." The agent's current behavior is to attempt a resolution first, escalating only if that fails. What should it do?

- A) Continue with the current behavior, since first-contact resolution is the metric the whole agent program is being measured against this quarter.
- B) Escalate immediately — an explicit customer request for a human is a trigger to honor without first attempting another round of investigation.
- C) Ask the customer to describe the issue one more time in their own words, and use that answer to decide whether escalation is really warranted.
- D) Offer the customer a discount code in the hope that it encourages them to keep working the issue with the bot instead of a live person.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation, with custom slash commands, CLAUDE.md configurations, and both plan mode and direct execution.

---

**Question 16.** Your `/gen-migration` skill generates database migrations, but developers keep invoking it bare — `/gen-migration` — and get generic scaffolds because the skill never learns the target table. What frontmatter option addresses this?

- A) `context: fork`, so the skill runs in an isolated context and can ask its own follow-up questions without polluting the main conversation.
- B) `allowed-tools`, restricting which tools the skill may call until some table name has been specified somewhere earlier in the session.
- C) `argument-hint`, which prompts developers for the required table-name parameter when the skill is invoked without arguments supplied.
- D) `paths`, restricting where the skill is allowed to run so it only ever fires from inside a directory that already contains migration files.

**Question 17.** You want to experiment with an aggressive variant of the team's shared `/test-gen` skill — different coverage strategy, different output style — without changing anyone else's workflow. What is the recommended approach?

- A) Create a personal variant under `~/.claude/skills/` with a different name, leaving the team's project-scoped skill completely untouched.
- B) Edit the project skill directly, but do the work on a long-lived branch that nobody else on the team happens to be using right now.
- C) Add an environment variable to the shared skill that flips its behavior into your experimental mode whenever that variable happens to be set.
- D) Copy the skill into `.claude/skills/` under the exact same name, so that your local version quietly shadows the team's shared one.

**Question 18.** You're migrating from Moment.js to date-fns across the codebase. You want to explore usage patterns and settle a conversion strategy before touching code, then apply the strategy efficiently. How should you use Claude Code's modes?

- A) Direct execution the entire way through, on the reasoning that a migration like this becomes purely mechanical the moment it actually starts.
- B) Plan mode for the whole migration, on the reasoning that a change this large should never actually leave the planning phase at all.
- C) Alternate modes file by file, re-entering plan mode individually right before editing each file so every change gets its own tiny plan.
- D) Plan mode to explore usage and settle the conversion strategy, then direct execution to carry out the approach the plan already settled on.

**Question 19.** Your project's CLAUDE.md has grown to 1,200 lines mixing testing standards, API conventions, deployment procedures, and security rules. Finding and maintaining anything is painful. What is the recommended reorganization?

- A) Sort the single file alphabetically by topic and add a detailed, structured table of contents so the right section is at least easier to locate.
- B) Split it into focused, topic-specific files under `.claude/rules/`, such as `testing.md`, `api-conventions.md`, and `deployment.md`.
- C) Move the whole document to the team wiki instead, leaving a one-line pointer in CLAUDE.md so Claude knows where the real content now lives.
- D) Compress the file by stripping out every example and explanation, leaving only the bare rules themselves in as few lines as possible.

**Question 20.** All code under `packages/mobile/` — and only that code — must follow your mobile team's conventions (navigation patterns, platform-specific error handling). The rest of the repo has different standards. What is the simplest correct placement?

- A) A `.claude/rules/` file scoped with `paths: ["**/*"]` that contains both the mobile conventions and the rest of the repo's conventions together.
- B) The root CLAUDE.md, with a note near the mobile section saying the following rules apply only when working inside the mobile package.
- C) A CLAUDE.md placed inside `packages/mobile/` itself — directory-level configuration fits conventions scoped to one self-contained subtree.
- D) A skill that mobile developers are expected to invoke manually at the start of every session before they start editing mobile code.

**Question 21.** Claude's data-migration script works except it crashes on rows with null values in the `legacy_status` column. You've explained the problem twice in prose without a reliable fix. What feedback is most likely to produce the correct fix?

- A) A specific failing case: one example input row that actually contains the null, plus the exact expected output your pipeline wants for that row.
- B) A longer prose explanation this time, one that carefully covers the null case alongside empty strings and undefined values across the whole pipeline in general terms.
- C) A link to the database schema documentation, so Claude can read the column definitions and infer what a missing `legacy_status` should mean.
- D) Ask Claude to re-read its own script from the top and try again to spot the bug on its own, without giving it any additional information.

**Question 22.** Claude's latest change has three problems: an incorrect log format, an off-by-one in pagination, and missing type hints — three unrelated parts of the code, no interaction between fixes. A teammate insists all three must be sent in one combined message "or the fixes will conflict." What is the right guidance?

- A) The teammate has this right — feedback should always be batched into a single detailed message no matter how unrelated the individual issues are.
- B) Neither approach is worth trying; a change with three separate problems in it should just be thrown out and regenerated completely from scratch.
- C) Send exactly one issue per session, starting a brand-new session from scratch for each of the three fixes so nothing can possibly cross-contaminate.
- D) These issues are independent, so sequential iteration works fine — the single-message approach mainly matters when fixes actually interact.

**Question 23.** You're about to have Claude implement a caching layer for your API — a domain where you know invalidation strategy, TTL policy, and stampede protection matter but you haven't thought them through. Which technique best surfaces these decisions before code gets written?

- A) Have Claude generate three alternative implementations using a slightly different sampling temperature for each, then pick whichever one reads best.
- B) Use the interview pattern: have Claude ask you questions about invalidation, failure modes, and consistency requirements before it implements anything.
- C) Implement the caching layer quickly as a first pass, and let production load testing surface whatever gaps show up once real traffic hits it.
- D) Hand Claude a short list of popular caching libraries and let it choose whichever one it judges to be the best fit for the API.

**Question 24.** You've built a personal `/standup-notes` command that formats your daily notes — useful to you, irrelevant to teammates. Where does it belong?

- A) `.claude/commands/` inside the repository, on the reasoning that this is simply the folder where every slash command is supposed to live.
- B) The project CLAUDE.md, added as an always-available instruction so the formatting behavior is documented for the whole team to see.
- C) `~/.claude/commands/` — user-scoped commands are for personal workflows and don't travel with the repository into anyone else's checkout.
- D) A gitignored file dropped into `.claude/commands/` inside the repo, so the command stays local without ever getting committed.

**Question 25.** Twice this month you've had to revert half-completed refactors after discovering mid-way that the approach conflicted with how another module worked. Both refactors touched many files and had multiple viable designs. What practice prevents this?

- A) Make commits smaller during the refactor, so that when a revert does become necessary, at least less accumulated work has to be thrown away.
- B) Adopt a rule that a refactor may only touch five files per working session, spreading a large change out across many smaller sessions instead.
- C) Run the full test suite after every single file edit during the refactor, so any conflict with another module is caught the moment it happens.
- D) Enter plan mode first for this class of task, exploring the codebase and settling the design before any file actually gets touched or changed.

**Question 26.** Late in a long session, Claude contradicts architecture answers it gave correctly two hours ago. You have several hours of work left. What practice keeps the remaining work grounded?

- A) Have Claude record key findings in a scratchpad file as it works, and consult that file whenever it answers a subsequent architecture question.
- B) Correct each contradiction conversationally the moment it shows up, without changing anything about how the session is otherwise being run.
- C) Ask Claude to summarize everything it has learned so far in its very next reply, and then just carry on with the session exactly as before.
- D) Restart the session from scratch and rebuild the architecture understanding purely from memory, without consulting anything written down.

**Question 27.** Your build-and-test MCP tool returns ~300 lines of logs per run; you run it constantly, and only the pass/fail status and failing test names ever matter to the agent. Sessions degrade after a dozen runs. What is the right fix?

- A) Run builds less frequently by batching several unrelated changes together before triggering the next build-and-test invocation.
- B) Trim the tool's output down to the fields that actually matter (status, failing names, first error) before it ever enters context.
- C) Move the whole team onto a larger-context model so the agent has enough headroom to absorb a dozen full 300-line log dumps.
- D) Pipe every run's logs to a file on disk and have the agent Read that file back only on the occasions it actually needs the full 300-line detail.

**Question 28.** You've finished a two-hour exploration phase and are about to start the implementation phase of the same large task. The session is at 70% context. What does the guide recommend before proceeding?

- A) Just push on into implementation — the new work will naturally displace the exploration context that's no longer needed anyway.
- B) Manually delete the exploration messages out of the transcript so the remaining 30% of context has more room to work with.
- C) Ask Claude to keep every future reply brief from this point forward, purely to stretch the remaining context a little further.
- D) Summarize the key findings from exploration, then start the next phase (or subagents) with that summary injected as initial context.

**Question 29.** You ask Claude to analyze a 25-file diff pasted as one long message. The analysis is sharp for the first and last few files and superficial for the middle of the diff. Which restructuring most directly addresses the cause?

- A) Paste the same diff again but in reverse file order, so the files that got neglected the first time end up at the very front this time.
- B) Simply ask Claude to "grade every file in the diff with equal rigor" as an instruction added to the top of the same long message.
- C) Lead with a short summary of the highest-priority files and add explicit per-file section headers throughout the diff.
- D) Raise `max_tokens` on the request so the resulting analysis has room to run considerably longer than it currently does.

**Question 30.** Your desktop chat-style dev assistant (built on the API) forgets constraints the user stated four turns ago. Inspecting the client, you find each API call sends only the newest user message. What is the fix?

- A) Send the complete conversation history with every request, since the API itself is stateless and has no memory of turns it wasn't sent.
- B) Add an instruction telling the assistant to remember all prior constraints even on turns where those constraints were never actually included.
- C) Increase `max_tokens` on each request so the model has more room in its own reply to restate whatever earlier constraints it can recall.
- D) Have the user restate their constraints every few turns as a manual workaround, and document this as an expected quirk of the assistant.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You're wiring the SDK response handler. Which `stop_reason` value tells your code the model has finished its work and the response text should be presented to the developer?

- A) `"tool_use"`, which the SDK sets once the model has settled on which tools it intends to call for the remainder of the turn.
- B) `"end_turn"`, which signals that the model has completed its turn with no further tool calls pending.
- C) `"max_tokens"`, which the SDK sets when the model has run out of room and said essentially everything it was able to fit.
- D) `"stop_sequence"`, which fires once the model reaches what it considers its own natural conclusion to the reply.

**Question 32.** Yesterday your agent built a thorough analysis of the repo in a named session. Overnight, a sweeping dependency upgrade changed imports in roughly 60% of files. You need analysis-informed help today. What is the most reliable continuation?

- A) Resume the named session and simply mention in your next message that some of the files it looked at yesterday have since changed.
- B) Resume the same session and have the agent re-Read every single file it previously analyzed before it's allowed to answer anything new.
- C) Fork the session first so the stale analysis stays intact on the parent branch while a child branch handles today's work separately.
- D) Start a new session seeded with a structured summary of the durable findings, since most of yesterday's tool results are now stale.

**Question 33.** The agent generated a 20-file changeset. A single review pass over all 20 files produces uneven depth and missed an inter-file API mismatch. How should the review be structured?

- A) Run two full passes over all 20 files back to back, and keep only the findings that both passes happen to agree on independently.
- B) Run one pass over just the 10 riskiest files by line count, and skip reviewing the other 10 files in this changeset entirely.
- C) Run per-file passes for local issues, plus a separate integration pass focused specifically on cross-file data flow and API consistency.
- D) Run a single pass over all 20 files with an added instruction telling Claude to allocate exactly equal attention and depth to every single one of them.

**Question 34.** Your agent needs three independent investigations — git history of a module, its test coverage, and its dependency audit — before proposing a refactor. How should the coordinator spawn them for minimum wall-clock time?

- A) Emit three separate Task tool calls within a single coordinator response so all three subagents run their investigations in parallel.
- B) Spawn the three subagents across three consecutive turns instead, reviewing each one's findings in full before the next one is started.
- C) Combine all three investigations into one long prompt for a single subagent to work through sequentially inside one context window.
- D) Skip subagents altogether and run all three investigations directly inline inside the coordinator's own single conversation.

**Question 35.** Policy: the productivity agent must never write to `config/production/`. It has broad Write access for scaffolding elsewhere, and CLAUDE.md states the rule, but a near-miss occurred last week. What is the correct enforcement?

- A) Remove the Write tool from the agent across the board, even though it's needed for the routine scaffolding work the agent does elsewhere.
- B) Move the production configuration files out of the repository entirely, into a separate location the agent has no reason to ever browse.
- C) Strengthen the CLAUDE.md wording around this rule and copy the same warning into the frontmatter of every skill the agent might invoke.
- D) Add a hook that intercepts every Write and Edit call and blocks any of them from targeting a path under `config/production/`.

**Question 36.** A developer asks the agent to rename a variable in one file. Logs show the full multi-agent pipeline spun up — test-writer, doc-writer, and refactor subagents all invoked — for a 30-second task. What is the architectural fix?

- A) Cap the number of subagents the coordinator is allowed to invoke at two per incoming request, regardless of what that request asks for.
- B) Have the coordinator assess each request's complexity and invoke only the subagents the task actually requires — trivial tasks need none.
- C) Remove the coordinator layer entirely and let individual developers pick which subagents to invoke manually for each request themselves.
- D) Optimize the pipeline so it runs faster end to end, which lowers the cost of spinning up subagents even when they weren't needed at all.

**Question 37.** Early in a session the coordinator discovered the project's testing conventions. It then spawns a test-writer subagent, whose output ignores every one of those conventions. Why?

- A) The specific model tier assigned to the test-writer subagent is too small to reliably follow a set of detailed testing conventions.
- B) The conventions were never written down in CLAUDE.md, and only content that lives in CLAUDE.md is able to reach a subagent at all.
- C) The subagent's prompt omitted the discovered conventions — subagents don't inherit the coordinator's history.
- D) The Task tool silently strips certain kinds of markdown formatting out of prompts it forwards to subagents, which garbled the conventions somewhere in transit.

**Question 38.** Asked to "improve error handling across our services," the coordinator decomposed the work into subtasks for just two of the seven services, and the final report claims completion. What is the root-cause fix?

- A) Improve the coordinator's decomposition step so it enumerates the full scope up front and checks its subtasks against coverage criteria.
- B) Instruct each subagent to volunteer for additional services on its own initiative whenever it happens to finish its assigned work early.
- C) Add more subagents to the pipeline overall, on the theory that more parallel workers naturally end up covering more of the seven services.
- D) Have the report-generation step flag any service it wasn't handed data for, so at least the gap is visible somewhere in the output.

**Question 39.** Your utilities are re-exported through several `index.ts` barrel files, so importers reference the barrel, not the source file. You need every real usage of the functions defined in `src/util/dates.ts`. What is the right built-in tool strategy?

- A) Glob for every file matching `**/index.ts` across the repository and manually read through each barrel file that Glob returns.
- B) Grep for the literal string `src/util/dates` and treat whatever importers turn up in that search as the complete usage list.
- C) Read `dates.ts` once and rely on the surrounding IDE's cached reference count from a previous session to estimate real usage.
- D) First identify every name exported from `dates.ts`, directly and via barrels, then Grep for each exported name across the codebase.

**Question 40.** The agent must locate every Storybook story file — they follow the `*.stories.tsx` naming convention and are scattered throughout `src/`. Which tool fits?

- A) Grep for the literal string "storiesOf" across every file's contents, on the theory that every story file will contain that call.
- B) Glob with the pattern `**/*.stories.tsx` — this is filename pattern matching, which is exactly what Glob exists to do.
- C) Read through the Storybook configuration file and try to infer the likely list of story files from whatever it references.
- D) Run a Bash `find` command piped through a chain of several `grep` invocations to filter down to the matching filenames.

**Question 41.** Two edits are queued: (a) completely regenerate a 15-line config file from a new template; (b) rename one function in a 2,000-line module. Which tool pairing is correct?

- A) Write for the config regeneration, since it's a full replacement of a small file; Edit for the targeted rename in the large module.
- B) Edit for both changes, on the reasoning that Edit is categorically safer to use than Write no matter what the underlying change is.
- C) Write for both changes, on the reasoning that a full-file write is always more predictable to review than a small targeted patch would ever be.
- D) Edit for the small config file and Write for the entire 2,000-line module, rewriting the whole file just to rename one function.

**Question 42.** You found a promising community MCP server for database introspection and want to trial it for a week before proposing it to the team. Where do you configure it?

- A) In the project's `.mcp.json`, with a comment next to the entry marking it as experimental so the rest of the team knows not to rely on it yet.
- B) In the project's CLAUDE.md, where its usage and current experimental status can be documented for anyone reading the file.
- C) In your user-scoped `~/.claude.json` — personal and experimental servers belong at user level, keeping the project configuration clean.
- D) In `.claude/rules/`, with a `paths` scope that limits the server's availability to only the files you personally work on.

**Question 43.** Your system prompt says: "Always use the ripgrep-mcp tool for searching." Now the agent uses it even to find files by name — where Glob is correct — and results have gotten worse. What is the underlying lesson?

- A) MCP-provided search tools should never be allowed to coexist in the same agent alongside any of the built-in search tools.
- B) The instruction only needed the single word "content" added to it, and doing so would have fixed the whole problem outright.
- C) The ripgrep-mcp tool's own description is too weak to constrain a blanket instruction like this one written by hand.
- D) A blanket "always use this tool" instruction in the system prompt creates an unintended association that overrides sensible per-task tool selection; describe when to use it instead.

**Question 44.** Before choosing where to hook a new plugin system, the agent must survey twelve candidate modules. You want the survey's verbose output kept away from the main session, which will do the actual design work. What is the right mechanism?

- A) Read all twelve modules directly inside the main session, working through them one at a time, and then run `/compact` once the survey is done.
- B) Use the Explore subagent for the survey — its verbose discovery stays in an isolated context and only a summary returns to the main session.
- C) Split the survey into four modules per session, spread across three separate sessions run back to back over the course of the day.
- D) Skip the module survey altogether and pick the hook point directly from whatever the existing architecture diagram happens to show.

**Question 45.** Your `/brainstorm-designs` skill generates several speculative design alternatives with pros and cons. After running it, the main session keeps referencing rejected alternatives as if they were decisions. What fixes this?

- A) Run the skill only inside a single permanent dedicated session that exists purely for brainstorming and is never used for anything else.
- B) Add a closing line to the skill's output stating plainly that everything printed above it was purely hypothetical, not a decision.
- C) End every brainstorming run by explicitly asking Claude to forget the rejected options it just spent the whole run generating.
- D) Add `context: fork` to the skill so exploratory content stays isolated, returning only the chosen direction to the main session.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your pipeline requires `extract_metadata` to run on every document before any enrichment tool may be called. The model usually complies with the prompt instruction but occasionally jumps straight to enrichment. What guarantees the ordering?

- A) Set `tool_choice: "any"` on the first request, which guarantees the model must call some tool before it's allowed to reply with plain text.
- B) Add a hook that automatically re-runs `extract_metadata` retroactively after the fact, any time an enrichment tool call is detected in the transcript.
- C) Force it: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, then use normal tool choice for later turns.
- D) Add a batch of few-shot examples in the prompt demonstrating the correct metadata-first ordering across a handful of worked scenarios.

**Question 47.** You're designing the invoice schema and must decide which fields are `required`. Which principle is correct?

- A) Mark every business-critical field required, on the reasoning that doing so signals to the model just how much each of those fields matters.
- B) Mark essentially everything optional across the board, in order to maximize how much extraction flexibility the schema leaves available.
- C) Mark required whatever fields the downstream systems happen to need, independent of whether those fields are actually present in the documents.
- D) Mark required only fields genuinely present in every document; fields that may legitimately be absent should stay optional or nullable.

**Question 48.** You're extracting quantities from maintenance logs where technicians write informally: "topped off with about half a jug," "roughly two dozen bolts." The model keeps outputting precise-looking fabricated numbers. What is the most effective mitigation?

- A) Add a regex-based validator downstream that rejects any extracted value that looks suspiciously too precise for language this informal.
- B) Add few-shot examples showing correct handling of informal measurements — mapped to approximate values with an `is_estimate` flag, or to null.
- C) Add a line to the system prompt instructing the model to "never guess" whenever it encounters a quantity phrased in vague, informal language.
- D) Route every maintenance log containing the word "about" straight to human review instead of letting the model extract it automatically.

**Question 49.** Academic papers in your corpus vary structurally: some use inline citations, others end-of-paper bibliographies; some have a dedicated methodology section, others embed methods in results. Extraction quality varies wildly with the structure. What is the recommended fix?

- A) Add few-shot examples demonstrating correct extraction from each structural variant — inline citations vs bibliographies, dedicated vs embedded methods.
- B) Preprocess every incoming paper into one single canonical structure, normalizing citation style and section layout before extraction ever runs.
- C) Build one separate extraction prompt per academic journal, routed automatically by whichever source the incoming paper happens to come from.
- D) Extract only from the papers that already match the single most common structure across the whole corpus, and route every other paper straight to manual review.

**Question 50.** Since adopting tool_use with a strict schema, outputs always validate — but spot checks find the vendor's name in the `customer_name` field and the invoice date in `due_date`. What does this demonstrate?

- A) The schema's field names are simply too similar to one another, and the whole schema needs a careful renaming pass across every field.
- B) The source documents are too noisy overall for any automated extraction pipeline to realistically be trusted on them going forward.
- C) Strict schemas eliminate syntax errors, not semantic ones — values can land in the wrong field and still validate; add cross-field checks and spot sampling.
- D) Switching `tool_choice` to `"any"` for these calls is what's needed to make the model's field-to-field mapping reliable going forward.

**Question 51.** An extraction fails Pydantic validation. You will retry. Which retry request gives the model the best chance of a correct second pass?

- A) Send the exact same request a second time unchanged, on the reasoning that the model usually self-corrects on a second independent sample.
- B) Send back just the bare validation error text on its own, in order to keep the retry request itself as cheap and short as possible.
- C) Send back only the failed extraction along with a short instruction telling the model to "fix the errors" it apparently contains.
- D) Send the original document, the failed extraction, and the specific validation errors together — full context for targeted self-correction.

**Question 52.** Documents arrive continuously and your contract guarantees results within 30 hours. Batch processing can take up to 24 hours. Which submission schedule guarantees the SLA while minimizing submission overhead?

- A) Submit one batch daily, on the reasoning that 24 hours of accumulation plus 24 hours of processing still comes in comfortably under two full days.
- B) Submit a batch every 4 hours — worst case 4h accumulation plus 24h processing lands at 28 hours, inside the SLA with margin to spare.
- C) Submit every 8 hours instead, since 8 plus 24 comes out close enough to the limit given that batches in practice usually finish somewhat early.
- D) Submit every 12 hours with a priority flag attached to whichever documents in the batch happen to be the oldest ones waiting.

**Question 53.** Two extraction workloads: (1) a compliance archive of 80,000 historical contracts to process this quarter; (2) a customer-facing upload flow where the user watches a spinner until their document's data appears. How do you assign APIs?

- A) Batch API for the archive, since it's latency-tolerant and cheaper; synchronous API for the upload flow, since a user is sitting there waiting.
- B) Batch API for both workloads, on the reasoning that the same cost savings apply equally regardless of how latency-sensitive either one is.
- C) Synchronous API for both workloads, on the reasoning that one single simpler architecture is worth more overall than whatever the batch discount would save on the archive.
- D) Synchronous processing for the archive to finish it faster, and batch processing for the uploads since those users can just be emailed later.

**Question 54.** You've submitted a batch of 2,000 extraction requests. How does your pipeline obtain and correlate the results?

- A) Results stream back over a webhook in the same order the 2,000 requests were originally submitted, arriving individually as each one finishes.
- B) The original submission call itself blocks until every one of the 2,000 results is ready, then returns the full set back in submission order.
- C) Results are emailed to the account owner as a single signed archive file once the entire 2,000-request batch has finished processing.
- D) Poll the batch's status until processing ends, then retrieve results and match each to its request using the `custom_id` assigned at submission.

**Question 55.** Scanned approval forms have checkboxes that are sometimes too degraded to read. The schema's `decision` field is an enum: `["approved", "rejected"]`, and the model currently guesses. What is the correct schema change?

- A) Lower the scan-quality threshold applied at intake so that any form degraded enough to cause trouble gets rejected before it reaches extraction.
- B) Add an `ocr_confidence` float alongside the existing field, and simply accept whatever the model guesses whenever that score is above 0.8.
- C) Add an `"unclear"` enum value for ambiguous cases, and route those extractions to human review rather than forcing a binary guess.
- D) Make the `decision` field free text instead of an enum, so the model has room to write out its uncertainty in its own words.

**Question 56.** Your extraction step also self-checks its output ("verify your extraction before finalizing") and reports near-zero errors — but human audits find real mistakes it never catches. What is the structural fix?

- A) Make the self-check step mandatory by forcing it through `tool_choice`, so the model is never able to skip it on any single extraction.
- B) Run a second, independent verification pass in a fresh instance that compares the extraction against the source without the extractor's own reasoning.
- C) Strengthen the self-check prompt with a detailed validation checklist enumerating every category of error the model ought to be looking for.
- D) Ask the self-check step to also report a confidence score, and route only the extractions with the very lowest scores to human audit.

**Question 57.** Next week you'll batch-process 50,000 archived contracts with a newly written extraction prompt. What should happen first?

- A) Refine the prompt on a representative sample using the synchronous API first, since first-pass success is what controls cost at 50,000-document scale.
- B) Submit the full batch straightaway, on the reasoning that the roughly 50% batch discount makes even a handful of failed passes across the archive affordable to absorb.
- C) Split the archive into ten batches of 5,000 documents each, and adjust the prompt in between each of the ten runs as issues surface.
- D) Run the entire archive through a smaller, cheaper model first as a smoke test before committing to the prompt on the full-size model.

**Question 58.** Your OCR agent hands its output to a validation agent whose context budget is small. Currently it sends the full raw text plus its complete reasoning narrative, and the validation agent truncates. What is the right change?

- A) Simply double the validation agent's context budget so it has enough room to hold the full raw text and reasoning narrative without truncating.
- B) Have the validation agent request additional pages of the raw OCR text on demand, one page at a time, instead of receiving everything up front.
- C) Add a summarization pass over the OCR agent's text before it ever reaches the validation agent, shrinking the reasoning narrative down.
- D) Modify the upstream agent to return organized key facts, source locations, and flags — sized for the downstream consumer — instead of raw narrative.

**Question 59.** An extracted vendor name matches three different vendor records in your master file. The pipeline currently auto-selects the most recently active vendor. What should it do instead?

- A) Auto-select whichever of the three vendor records has the closest string match to the extracted name, instead of the most recently active one on file.
- B) Create a brand-new vendor record altogether, on the reasoning that doing so avoids having to guess among the three existing candidates.
- C) Treat multiple matches as an ambiguity — use identifiers from the document like address or tax ID to disambiguate, and route to review otherwise.
- D) Pick one of the three vendor records essentially at random, but log which one was chosen so the decision can be reviewed in an audit later.

**Question 60.** Your extraction summary report converts everything to prose paragraphs — including line-item tables and numeric comparisons — and reviewers say checking figures is painful. What does the guide recommend?

- A) Convert everything in the report to more structured tables instead of prose, on the reasoning that reviewers have already said tables are what they prefer.
- B) Render each content type in the form that fits it — financial and line-item data as tables, narrative as prose, findings as lists — not one uniform format.
- C) Hand reviewers the raw underlying JSON directly and let each of them format the figures however works best for their own review process.
- D) Add a "figures appendix" at the end of the prose report that simply repeats every number already mentioned earlier in the document.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-A, 2-C, 3-B, 4-D, 5-A, 6-C, 7-D, 8-B, 9-D, 10-A, 11-B, 12-C, 13-A, 14-D, 15-B, 16-C, 17-A, 18-D, 19-B, 20-C, 21-A, 22-D, 23-B, 24-C, 25-D, 26-A, 27-B, 28-D, 29-C, 30-A, 31-B, 32-D, 33-C, 34-A, 35-D, 36-B, 37-C, 38-A, 39-D, 40-B, 41-A, 42-C, 43-D, 44-B, 45-D, 46-C, 47-D, 48-B, 49-A, 50-C, 51-D, 52-B, 53-A, 54-D, 55-C, 56-B, 57-A, 58-D, 59-C, 60-B

---

**1. A** — Text content is not a completion signal: responses routinely carry narration alongside `tool_use` blocks. The loop must inspect `stop_reason` and continue on `"tool_use"`. B inverts a check that shouldn't exist. C prompts around a control-flow bug instead of fixing the loop. D just delays the same wrong signal by one more response.

**2. C** — When identity verification must be guaranteed before account mutations, only a programmatic prerequisite (blocking mutation tools until `get_customer` returns a verified ID) is deterministic. A and B are prompt-layer measures with non-zero failure rates — the incident already proves the point. D adds customer friction the agent itself doesn't enforce.

**3. B** — A compliance rule with audit findings needs hook-level interception: check the final-sale flag on `process_refund` calls, block, and redirect to the store-credit workflow. C is more prompt emphasis on an already-stated rule. D destroys the agent's core capability to fix one policy edge. A only detects violations after the money has already moved.

**4. D** — A `PostToolUse` hook mapping numeric tiers to names normalizes the data before the model reasons over it — deterministic and invisible to the prompt. A and C rely on the model performing the conversion correctly every single time. B may be right long-term but is out of your control and slow to land.

**5. A** — Match decomposition to the workflow: fixed sequential chains for predictable flows (warranty), dynamic decomposition driven by intermediate findings for open-ended investigations (fraud). B adds adaptive overhead where nothing actually varies. C tries to pre-script the unscriptable. D abandons the structure that makes the predictable flow reliable in the first place.

**6. C** — Pre-routing by keyword replaces the model's contextual judgment with a brittle pattern match — the exact failure the example shows ("do NOT want a refund"). Model-driven agents exist because intent requires context. A and B upgrade the router instead of removing an unnecessary layer. D patches the symptom downstream of the actual bug.

**7. D** — The pattern for multi-concern requests: decompose into distinct items, investigate in parallel using shared context, synthesize a unified resolution — correctness *and* speed together. A and B degrade the customer experience to fit the existing architecture. C speeds up a sequential design instead of actually restructuring it.

**8. B** — `stop_reason: "tool_use"` means the turn is in progress: execute the tool, append the result, send it back. Accompanying text is narration, not a completed reply awaiting customer input. A discards useful narration unnecessarily. C forks the conversation state into two inconsistent paths. D treats a normal, expected combination as an error.

**9. D** — Tool descriptions should document input formats, example queries, and boundary behavior; the agent is guessing because one line tells it nothing about accepted identifiers. A and B build extra infrastructure to tolerate a documentation gap instead of closing it. C makes each failure cheaper rather than making failures rarer.

**10. A** — A gateway timeout is a transient error: `errorCategory: "transient"`, `isRetryable: true`, plus a description lets the agent retry sensibly. B mislabels it non-retryable, abandoning refunds that would likely succeed. C reports success for an operation that didn't actually complete — dangerous. D returns the agent to guessing with even less information than before.

**11. B** — These tools have distinct purposes hidden behind near-identical descriptions; rewriting both to state purpose, inputs, outputs, and when to choose each fixes selection at the root. A merges two legitimately different access patterns into one. C removes needed functionality outright. D hardcodes a preference instead of enabling an informed choice.

**12. C** — MCP resources exist to expose content catalogs, giving the agent visibility into available policy documents without exploratory probing. A bloats every conversation with the full manual whether it's needed or not. B is disproportionate and out of scope for this problem. D makes repeated probing cheaper, not unnecessary in the first place.

**13. A** — Scoped cross-role tools serve high-frequency needs safely: a read-only `get_order_status` gives the escalation agent what it uses constantly, while modification stays with the role that owns it. B leaves the dangerous capability reachable behind a prompt rule. C removes a legitimate, frequent need. D doubles the exposure instead of narrowing it.

**14. D** — A mode-switched tool with a destructive branch is the case for splitting into purpose-specific tools with individual contracts — misselecting an enum value should never be able to close an account. A and B leave one entry point where a parameter typo is still catastrophic. C keeps the confusing design and only bolts a gate onto one branch of it.

**15. B** — An explicit customer request for a human is a defined escalation trigger to honor immediately — investigation attempts after "get me a human, now" erode trust. A and C do exactly what the customer asked the agent not to do. D is a retention tactic dressed up as a resolution step, not an escalation policy.

**16. C** — `argument-hint` frontmatter prompts developers for required parameters when the skill is invoked without arguments — precisely the failure here. A changes execution isolation, not input collection. B misuses a tool-permission control for a parameter problem. D isn't the right frontmatter for collecting a missing argument.

**17. A** — Personal skill customization: create a variant under `~/.claude/skills/` with a different name, so teammates' workflow is left untouched. B ships team-visible changes to a shared artifact regardless of the branch it lives on. C adds a hidden mode to a shared skill everyone else still relies on. D shadows the team's skill under the same name — exactly the collision to avoid.

**18. D** — Combine the modes: plan mode for exploring usage patterns and settling the conversion strategy, direct execution to apply the planned approach. A skips the design decision that determines the migration's quality. B never actually ships the migration. C fragments a strategy decision that should be made once, up front.

**19. B** — The recommended structure for an overgrown CLAUDE.md is topic-specific files in `.claude/rules/` (`testing.md`, `api-conventions.md`, …). A reorganizes the same monolith without actually splitting it. C makes the content invisible to Claude entirely. D strips the very examples that make conventions followable in practice.

**20. C** — Conventions scoped to one self-contained subtree are the fit for a directory-level CLAUDE.md inside `packages/mobile/`. A loads both convention sets everywhere in the repo at once. B loads mobile rules into every session and relies on the model to scope them correctly. D applies conventions only when someone remembers to invoke a skill.

**21. A** — For edge-case fixes, provide a specific test case: example input containing the null and the exact expected output. That's unambiguous in a way prose has already failed to be twice. B is still more prose. C provides background, not the expected behavior for the null row. D re-asks the model to find what it's already missed twice on its own.

**22. D** — Independent problems can be fixed sequentially; the single-detailed-message guidance applies when fixes interact and would invalidate each other. A overgeneralizes a rule meant for interacting issues. B is a disproportionate response to three small, unrelated bugs. C adds session churn for no real benefit here.

**23. B** — The interview pattern targets unfamiliar domains with unarticulated constraints: Claude asks about invalidation, failure modes, and consistency before implementing — surfacing exactly the considerations you know you haven't thought through. A generates three versions of the same blind spots. C discovers requirements in production instead of before writing code. D picks a library, not a design.

**24. C** — Personal, team-irrelevant commands belong in `~/.claude/commands/` (user-scoped); `.claude/commands/` in the repo is for team-shared, version-controlled commands. B misplaces a command as a standing instruction for everyone. D pollutes the project directory to simulate what user scope already provides for free.

**25. D** — Multi-file changes with multiple viable designs are plan mode's core case: explore and validate the approach before changing code, preventing exactly this costly rework. A cheapens the failure instead of preventing it. B is an arbitrary constraint unrelated to the actual cause. C catches breakage after the fact, not design conflicts before it.

**26. A** — This is context degradation in an extended session; the countermeasure is a scratchpad file of key findings, recorded as discovered and consulted for later answers — persistent ground truth outside the degrading context. B fixes symptoms one at a time, forever. C puts the summary right back into the same degrading context. D loses the accumulated understanding entirely.

**27. B** — Verbose tool outputs consume context disproportionately to their relevance; trim to the fields that matter (status, failing tests, first error) before results accumulate. A slows down the feedback loop that makes the agent useful in the first place. C postpones the problem to a bigger model. D still spends the context once the file is read back in, plus adds a step.

**28. D** — The guide's phase-transition practice: summarize key findings from the completed exploration phase and inject the summary as initial context for the next phase or subagents. A lets implementation compete with exploration residue at 70% full. B isn't a supported or reliable operation. C conserves output tokens, not the context that's actually the problem.

**29. C** — Uneven middle coverage of a long uniform input is lost-in-the-middle; the mitigation is a priority summary at the start plus explicit per-file section headers. A just moves the blind spot to a different set of files. B — exhortation alone doesn't change position effects. D lengthens the answer without changing what gets attended to.

**30. A** — The API is stateless: each request must carry the complete conversation history, or earlier constraints simply don't exist for the model on that call. B instructs it to remember what it was never actually sent. C is unrelated to the missing-input problem entirely. D makes users compensate for what is really a client-side bug.

**31. B** — `"end_turn"` signals the model has completed its turn with no pending tool work — time to present the response. `"tool_use"` (A) means work still remains. `"max_tokens"` (C) means truncation, not a clean completion. D — stop sequences are a separate, explicitly configured mechanism.

**32. D** — With ~60% of analyzed files changed, the session's tool results are mostly stale; starting fresh with a structured summary of durable findings is more reliable than resuming. A resumes on top of stale data with only a vague warning attached. B re-does the analysis inside a context that's already full of the old one. C preserves the staleness in two places instead of one.

**33. C** — Uneven depth plus a missed cross-file issue is attention dilution: split into per-file passes for local issues and a dedicated integration pass for cross-file data flow. A double-spends on the same diluted view and can still miss intermittent issues. B trades coverage for depth by pure guesswork. D — instructions alone don't reallocate attention.

**34. A** — Independent investigations parallelize by emitting multiple Task tool calls in a single coordinator response. B serializes them across turns for no benefit. C serializes them again, just inside one context instead of three turns. D floods the coordinator's own context with three investigations' worth of raw output.

**35. D** — A must-never rule with a near-miss on record needs interception: a hook blocking Write/Edit calls targeting `config/production/` paths. A removes a capability the agent legitimately needs elsewhere in the repo. B reorganizes the repo around a guardrail that's still missing. C adds more prompt emphasis where prompts have already failed once.

**36. B** — Coordinators should assess query complexity and invoke only the subagents a task needs — a one-line rename needs none of them. A caps waste at two subagents instead of at zero. C removes orchestration rather than fixing its judgment. D optimizes the cost of doing the wrong thing instead of not doing it.

**37. C** — Subagents don't inherit the coordinator's history; the discovered conventions had to be included directly in the test-writer's prompt. A and D invent mechanisms that aren't actually at play here. B would work only for conventions already written into CLAUDE.md ahead of time — these were discovered dynamically this session.

**38. A** — The subagents completed their assignments; the coverage failure happened at decomposition. Fix the coordinator: enumerate the full scope before creating subtasks and check decomposition against coverage criteria. B asks the workers to fix a planning problem. C adds capacity without adding direction. D reports the gap instead of closing it.

**39. D** — Barrel re-exports mean importers reference the barrel, so tracing requires two steps: enumerate the exported names, then Grep for each name across the codebase. A finds the barrels themselves, not their users. B finds only direct-path importers — the minority of real usages. C isn't grounded in the current state of the code at all.

**40. B** — Finding files by naming convention is Glob's exact purpose: `**/*.stories.tsx`. A searches file contents for an API string many story files won't even contain. C infers a file list instead of matching one directly. D reimplements Glob with more moving parts and more failure modes.

**41. A** — Write is for full-file creation/replacement (the regenerated config); Edit is for targeted modifications via unique anchor text (the rename in a large file). B forces anchor-matching onto a total rewrite. C rewrites 2,000 lines just to change one name — slow and needlessly risky. D is backwards on both halves of the pairing.

**42. C** — Personal and experimental MCP servers belong in user-scoped `~/.claude.json`; project `.mcp.json` is for shared team tooling everyone relies on. A ships your untested experiment to the whole team. B documents a server without actually configuring it anywhere. D misuses a rules mechanism for what is really server configuration.

**43. D** — "Always use X" is a keyword-sensitive instruction that creates an unintended blanket association, overriding sensible per-task tool selection. The fix is describing when the tool applies instead of mandating it unconditionally. A and C misplace the blame. B patches this one instance of a pattern worth fixing generally.

**44. B** — The Explore subagent isolates verbose discovery and returns a summary — the main session keeps its context free for design. A spends the main context first and only compacts after the damage is done. C splits the survey but loses any cross-module comparison. D skips the evidence the eventual decision actually needs.

**45. D** — Exploratory, speculative content is what `context: fork` is for: the brainstorm runs isolated, and only the outcome returns — rejected alternatives never enter the main conversation to be misremembered as decisions. A quarantines by convention, not by mechanism. B and C ask the model to disregard context it has already fully absorbed.

**46. C** — Guaranteeing that a specific tool runs first requires forced tool selection: `tool_choice: {"type": "tool", "name": "extract_metadata"}` on the first request, with enrichment handled in follow-up turns. A guarantees *a* tool, not *that specific* tool. B reacts after the fact instead of preventing the skip. D remains probabilistic no matter how many examples are added.

**47. D** — Required should mean "genuinely always present." Fields that may legitimately be absent must be optional/nullable, or the model is pressured to fabricate values to satisfy the schema. A confuses importance with presence. B loses real invariants the schema should be enforcing. C encodes downstream wishes the documents themselves can't honor.

**48. B** — Few-shot examples demonstrating informal-measurement handling (approximate value plus an estimate flag, or null when unquantifiable) teach a judgment the model generalizes from. A catches some fabrications only after the fact. C is a vague instruction where concrete examples are the more effective tool. D outsources a pattern the model can actually be taught to handle.

**49. A** — Structural variety is the textbook few-shot case: examples demonstrating correct extraction from each variant (inline vs bibliography, dedicated vs embedded methodology) let the model handle the spread. B presumes a reliable universal normalizer that doesn't really exist. C multiplies prompts to dodge generalization instead of building it. D silently shrinks coverage of the corpus.

**50. C** — Schema-valid output with values in the wrong fields is a semantic error — the class strict schemas cannot prevent by construction. Add semantic validation: cross-field consistency checks and sampled audits. A might help marginally but misses the general lesson. B gives up on a solvable problem entirely. D governs *whether* a tool is called, not field-level accuracy.

**51. D** — Effective retries carry the original document, the failed extraction, and the specific validation errors — everything needed for targeted self-correction. A relies on luck alone. B and C both omit the source document, so the model can't re-ground the corrected values against anything.

**52. B** — Worst case must fit the SLA: 4-hour accumulation + 24-hour processing = 28 hours ≤ 30, with margin. A's worst case is 48 hours. C's is 32 — over the line, and "usually finishes early" isn't a guarantee. D's is 36, and a priority flag doesn't change how long batch processing itself takes.

**53. A** — Match API to latency tolerance: the archive is the Batch API's ideal case (huge, non-blocking, roughly half the cost); the upload flow has a human watching a spinner — synchronous fits there instead. B leaves users staring at spinners for potentially hours. C forfeits large savings for no real benefit on the archive side. D is backwards on both workloads at once.

**54. D** — Batch results are obtained by polling for completion, then retrieving and correlating via the `custom_id` set at submission. A, B, and C describe delivery mechanisms the Batch API doesn't actually have (streaming webhooks in order, a blocking submission call, or email delivery).

**55. C** — Ambiguous source data needs an explicit `"unclear"` enum value plus routing to human review — the schema should let the model tell the truth instead of forcing a binary guess. A throws away documents that are still perfectly processable. B just dresses the same guess up with a confidence score. D destroys the machine-readable contract downstream systems depend on.

**56. B** — Self-checks inherit the extractor's own reasoning and blind spots; an independent verification pass — fresh instance, source document, no prior context — catches what self-review structurally cannot. A makes the biased check mandatory rather than fixing its bias. C gives the same biased check a longer checklist. D calibrates a signal produced by that same blind process.

**57. A** — Refine on a representative sample before batch-processing large volumes: first-pass success determines cost when each full pass is 50,000 documents with up to a 24-hour turnaround. B risks the whole archive on an untested prompt. C discovers problems 5,000 documents at a time instead of before running any of them. D tests a different model's behavior, not the actual prompt's quality on the model you'll really use.

**58. D** — When the downstream agent has a limited context budget, modify the upstream agent to emit organized key facts, source locations, and flags instead of verbose content and reasoning chains. A scales the budget to fit the waste rather than reducing it. B adds round-trips that still move the same volume of text. C compresses prose that shouldn't have been prose in the first place.

**59. C** — Multiple matches are an ambiguity to resolve with additional identifiers (address, tax ID from the document), not a heuristic pick; when identifiers don't resolve it, route to human review. A swaps one heuristic for a different one. B corrupts the master file with a needless duplicate. D is a heuristic with a paper trail attached, but still a guess.

**60. B** — Content types should render in the form that fits them: financial data as tables, narrative as prose, findings as structured lists — uniform formatting is the anti-pattern in both directions. A repeats the same mistake with a different uniform format. C exports the formatting work onto the reviewers instead of doing it once. D duplicates numbers instead of presenting them properly a single time.

---

*End of Practice Exam 3.*
