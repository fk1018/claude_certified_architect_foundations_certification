# CCAFC Practice Exam 1

**Claude Certified Architect – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Customer Support Agent, Code Generation with Claude Code, Multi-Agent Research, Claude Code for CI/CD) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (matches the official weightings):

| Domain | Questions |
|---|---|
| D1: Agentic Architecture & Orchestration (27%) | 16 |
| D2: Tool Design & MCP Integration (18%) | 11 |
| D3: Claude Code Configuration & Workflows (20%) | 12 |
| D4: Prompt Engineering & Structured Output (20%) | 12 |
| D5: Context Management & Reliability (15%) | 9 |

Answer key with explanations is at the end of this file. Answer every question before checking — the real exam does not allow skipping.

---

## Scenario A: Customer Support Resolution Agent (Questions 1–15)

You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues. It has access to your backend systems through custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Your target is 80%+ first-contact resolution while knowing when to escalate.

---

**Question 1.** An engineer implements the agentic loop so that it exits whenever the assistant's text contains phrases like "your issue is resolved" or "is there anything else." In production, the loop sometimes exits while the agent still intends to call `process_refund`, and other times keeps looping after the conversation is clearly finished. What is the correct loop termination design?

- A) Expand the phrase list to cover more terminal expressions, add fuzzy matching for paraphrases, and re-tune the list every quarter as agents phrase closings in new ways the current list can't anticipate.
- B) Continue the loop while `stop_reason` is `"tool_use"`, executing the requested tools and returning their results; terminate only when `stop_reason` is `"end_turn"`.
- C) Cap the loop at 10 iterations and terminate once the cap is hit, since most support cases resolve in fewer turns than that and the cap acts as a safety net.
- D) Terminate whenever the response has no text content, on the assumption that a tool-only response always means the agent still has work left to do.

**Question 2.** Your agent calls `process_refund` and your code executes the refund successfully. What must happen next so the agent can correctly continue the conversation?

- A) Append the tool result as a `tool_result` block referencing the `tool_use` ID in a user-role message, then send the full updated conversation back to Claude so it can incorporate the result into its next reasoning step.
- B) Store the refund confirmation in your database and fold a summary into the final reply.
- C) Inject the refund confirmation into the prompt directive so it persists automatically across every later turn of the conversation without further bookkeeping.
- D) Start a fresh conversation seeded only with a summary of the prior turns plus the refund result, to keep the running context small going forward.

**Question 3.** Your MCP tools come from different backend teams: `get_customer` returns ISO 8601 dates, `lookup_order` returns Unix timestamps, and order statuses are numeric codes in one tool but strings in another. The agent occasionally miscompares dates and misreads statuses when reasoning across tools. What is the most reliable fix?

- A) Add a prompt section documenting each tool's formats and instructing the agent to normalize the values itself before comparing them, turn by turn, and re-apply the same manual conversions every time fresh tool data arrives.
- B) Ask each backend team to migrate their APIs to one shared format standard as part of the current release, before the agent ships to production.
- C) Add a validation pass at the end of each conversation that checks the agent's final answer for date and status mistakes before it's sent.
- D) Implement a `PostToolUse` hook that normalizes timestamps, dates, and status codes into one consistent format before the model reasons over the results.

**Question 4.** Company policy requires human approval for any refund over $500. Your system prompt states this rule prominently, but production logs show that about 2% of refunds above $500 are still processed autonomously. What should you do?

- A) Move the rule to the very top of the prompt and repeat it again just before the tool definitions, so the model can't miss it.
- B) Add few-shot examples showing the agent escalating refunds of $501, $750, and $1,200 in the conversation history, so the $500 boundary gets reinforced by direct demonstration rather than by description alone.
- C) Implement a hook that intercepts `process_refund` calls above $500 and redirects to escalation.
- D) Make the model's decisions more deterministic by lowering its sampling randomness, so it follows the prompted instructions more reliably.

**Question 5.** A customer writes one message reporting a damaged item, a duplicate charge on their card, and an address change for an upcoming shipment. The agent resolves the damaged item and ends the conversation without addressing the other two concerns. What is the best design change?

- A) Detect multi-issue messages with a classifier up front and ask the customer to resubmit each issue as its own separate ticket.
- B) Decompose multi-concern messages into distinct items, investigate each in parallel using shared context, and synthesize one resolution covering all of them.
- C) Route any message containing more than one concern straight to `escalate_to_human`, on the assumption that multi-issue cases structurally exceed what a single agent can resolve in one pass, even when each concern individually looks routine.
- D) Handle each concern in its own new session, one session per concern, so every issue gets a clean context window to work from.

**Question 6.** When the agent escalates a billing dispute to a human agent, the human team works in a separate system with no access to the AI conversation transcript. Human agents report spending 10+ minutes reconstructing each case. What should the escalation include?

- A) The complete raw conversation transcript, exported as plain text, so the human can read through everything.
- B) The customer ID plus a link to open the customer's profile in the CRM, keeping the handoff payload as lightweight as possible.
- C) A sentiment score summarizing the conversation, so the human agent knows roughly how frustrated the customer sounded going in.
- D) A structured handoff summary containing the customer ID, a root cause analysis, the disputed or refund amount, and a clearly stated recommended next action for the human agent to take immediately upon opening the case.

**Question 7.** You are deciding which agent behaviors need programmatic enforcement (hooks) versus system-prompt guidance. Which requirement is the strongest candidate for a hook rather than prompt instructions?

- A) The agent should maintain an empathetic, professional tone even with frustrated or upset customers throughout the exchange.
- B) Refunds must only go to the verified original payment method on the order, never to an alternate account the customer supplies mid-chat.
- C) The agent should keep its responses concise and steer away from unnecessary technical jargon when explaining a resolution.
- D) The agent should log the interaction and add a soft hook-style note reminding itself to offer troubleshooting alternatives before proposing a refund.

**Question 8.** A product manager proposes replacing the agent's reasoning with a fixed sequence — always call `get_customer`, then `lookup_order`, then either resolve or refund — arguing it will make behavior predictable. Why is model-driven tool selection the better fit for this workload?

- A) Support requests are high-ambiguity, so the right tools and their order vary per case; a fixed sequence can't adapt when intermediate results change what's needed.
- B) Fixed sequences aren't supported by the Claude Agent SDK at all, which requires the model to choose every single tool call it makes.
- C) Model-driven selection is always the cheaper option, since the model skips the reasoning tokens a scripted sequence would otherwise spend.
- D) Decision trees can't invoke MCP tools at all in this SDK, so a fixed sequence would only ever be able to work with the small set of built-in tools bundled with the runtime itself, never the custom backend integrations.

**Question 9.** Every failure from `process_refund` currently returns the same response: `"Operation failed"`. Logs show the agent retrying policy-violation failures repeatedly (which will never succeed) and giving up immediately on transient gateway timeouts (which would succeed on retry). What is the best fix?

- A) Wrap all tool calls in an automatic retry-3-times policy at the application layer, so the agent never has to reason about retries itself.
- B) Add a prompt instruction telling the agent to judge from conversation context whether a given failure is likely to be retryable or not.
- C) Return detailed error responses that include an `errorCategory` (transient/policy/permission/business), an `isRetryable` boolean, and a human-readable description.
- D) Raise the payment gateway's timeout threshold so transient failures become rare enough that the retry behavior stops mattering.

**Question 10.** A customer requests a refund for an order purchased 47 days ago; policy allows refunds within 30 days. What should `process_refund` return so the agent handles this well?

- A) An error with the MCP `isError` pattern, a business-rule category, `retriable: false`, a customer-friendly explanation ("outside the 30-day window"), and a suggested alternative like store credit.
- B) A standard HTTP 400 status code with no response body at all, leaving the agent to guess at the cause purely from the shape of the request it originally sent, with nothing else to go on.
- C) A success response with an empty body, on the theory that this spares the customer from seeing alarming error language.
- D) An error containing the full server-side stack trace, so the agent has the maximum possible information to reason with.

**Question 11.** When a customer has no orders on file, `lookup_order` currently returns an error, and the agent responds by apologizing for "technical difficulties" and retrying the lookup. What should change?

- A) Add a prompt note explaining that, in practice, this particular error code usually just means the customer has no orders on file yet, and that the agent should treat it as informational rather than retrying the same lookup call again.
- B) Suppress the error with a hook and swap in a message telling the agent to end the conversation right there.
- C) Have the agent call `get_customer` again first, on the theory that the error may actually indicate a bad customer ID.
- D) Return a successful response with an empty result set, reserving errors for actual access failures.

**Question 12.** Your tool descriptions are detailed and well-differentiated, yet the agent calls `lookup_order` even for general return-policy questions where no order is involved. You find this line in the system prompt: "Use lookup_order to help with any customer question about their purchases." What is the most likely fix?

- A) Rewrite the `lookup_order` description to explicitly state that it should not be used for general policy questions.
- B) Add few-shot examples of policy questions being answered correctly without any tool call being made at all, covering several phrasings of the same kind of request.
- C) Reword or remove the keyword-sensitive prompt directive that's creating the unintended tool association.
- D) Rename `lookup_order` to `lookup_order_by_id` so the model understands that an order ID is a prerequisite.

**Question 13.** The support team wants to expand the agent from its current 4 tools to 18 by adding loyalty-program, marketing-preferences, subscription, and gift-card tools — all attached to the single resolution agent. What is the primary risk?

- A) The MCP protocol caps each server at 10 registered tools, so the expanded configuration will simply fail to connect once deployed.
- B) Tool selection reliability degrades as the number of available tools grows, increasing decision complexity and misrouting; tools should be scoped to the agent's role or split across specialized agents.
- C) The additional tool schemas, once structured into the model's context, will exceed the context window before any conversation even begins.
- D) The agent will run measurably slower because it is designed to call every available tool at least once per conversation, regardless of relevance.

**Question 14.** Compliance requires that every conversation begin with a call to a `classify_request` tool before any other tool runs, with no exceptions. What is the most reliable implementation?

- A) State in the prompt that `classify_request` is mandatory and must always be the very first tool call of the conversation.
- B) Set `tool_choice: "any"` on the first request so the model is guaranteed to call some tool before it responds with text.
- C) Add few-shot examples showing `classify_request` being called first across several different conversation types and openings, so the pattern is reinforced by demonstration rather than by instruction.
- D) Force `tool_choice` to `classify_request` on the first request, then use normal choice afterward.

**Question 15.** In long billing-dispute conversations, your context management summarizes older turns. After summarization, the agent starts misstating specifics — quoting "around $80" for a refund the customer was promised at exactly $83.47. What is the best fix?

- A) Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block included outside the summarized history.
- B) Raise the summary length limit so the summarizer has more room to normalize and preserve fine detail from the older turns.
- C) Re-run `lookup_order` and `get_customer` on every single turn so the freshest possible data is always sitting in context.
- D) Ask the customer to re-confirm every key dollar amount and date themselves whenever the running conversation crosses the 20-turn mark, adding a manual check-in step the agent relies on instead of preserving the numbers itself.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.

---

**Question 16.** You maintain your team's coding standards in `~/.claude/CLAUDE.md` on your machine. A new teammate clones the repository, but Claude Code ignores all of those standards for them. Why?

- A) The new teammate needs to run `/memory` once right after cloning the repository, in order to activate every memory file — both user-level and project-level — for their own local account before any session picks them up.
- B) CLAUDE.md files require an explicit `@import` from the project root before any of their contents take effect.
- C) `~/.claude/CLAUDE.md` is user-level configuration tied to your account only, not shared through version control; team standards belong in a project-level CLAUDE.md.
- D) The standards file exceeds the size limit for automatic loading and is being silently truncated on load.

**Question 17.** Your monorepo has six packages with mostly shared standards but some package-specific conventions. The root CLAUDE.md has grown to 900 lines and every session loads all of it regardless of which package is being edited. Package maintainers know their own conventions best. What is the most maintainable structure?

- A) Keep shared standards in focused files and have each package's CLAUDE.md use `@import` to include only the standards files relevant to that package, maintained by the package owners themselves.
- B) Duplicate the full 900-line standards document into each of the six package directories so every package is fully self-contained on its own.
- C) Keep the single root CLAUDE.md, but add a structured table of contents at the top so the model can navigate straight to the relevant section.
- D) Move all standards into a wiki and add one CLAUDE.md instruction telling Claude to ask developers for conventions whenever it's unsure.

**Question 18.** Claude Code follows your API error-handling conventions in some sessions but not others, with no obvious pattern. What is the best first diagnostic step?

- A) Rewrite the conventions section of CLAUDE.md with stronger, more imperative language throughout, and re-test across several fresh sessions.
- B) Run `/memory` to verify which memory files are actually loaded in the affected sessions before touching any content.
- C) Run `/compact` to clear out stale context that may be silently overriding the conventions in the misbehaving sessions.
- D) Delete and recreate the project CLAUDE.md from scratch, to rule out silent file corruption as the cause.

**Question 19.** Your team's `/analyze-deps` skill walks the dependency graph and prints thousands of lines of package data. Developers complain that after running it, Claude's answers about their actual coding task get noticeably worse. What change fixes this?

- A) Add `argument-hint` frontmatter so developers can scope the analysis down to one package at a time before running it.
- B) Move the dependency analysis instructions into CLAUDE.md so they are always loaded and no separate skill invocation is ever needed.
- C) Add a stricter `allowed-tools` schema restricting the skill to read-only operations, which trims the volume of output it can produce but still leaves that output landing in the main conversation.
- D) Add `context: fork` so the skill runs in an isolated sub-agent context and returns only a summary.

**Question 20.** Your `/scaffold-component` skill should only ever create new files from templates. During an audit you find a session where it also ran shell commands, including a `git checkout` that discarded a developer's uncommitted changes. What is the right guardrail?

- A) Add a prominent warning to the skill's SKILL.md instructions telling Claude never to run shell commands during scaffolding, and repeat that same warning again near the template-generation section for extra emphasis.
- B) Require developers to commit all of their work before they're allowed to run any skill, as a team policy.
- C) Configure `allowed-tools` in the frontmatter to permit only file-creation operations, so Bash is unavailable during execution.
- D) Convert the skill into a slash command instead, since slash commands are documented as being unable to run tools.

**Question 21.** Your team has two assets: (1) universal naming and error-handling conventions that apply to all code Claude writes, and (2) a release-notes generation workflow used once per sprint. How should each be configured?

- A) Put the universal conventions in the project CLAUDE.md, so they load automatically every session, and put the release-notes workflow in a skill under `.claude/skills/`, invoked only when a release is actually being cut.
- B) Put both in CLAUDE.md, so nothing depends on a developer remembering to invoke a skill at the right moment.
- C) Put both in skills, so the context cost of each is only paid on the sessions where it's actually needed.
- D) Put the conventions in a skill and the release-notes workflow in CLAUDE.md, since sprint workflows need to stay always available.

**Question 22.** A production bug report includes a stack trace pointing to a single function with an obvious off-by-one error. The fix is one line in one file. How should you proceed in Claude Code?

- A) Enter plan mode first and run a fully structured exploration of the codebase, mapping out related call sites and edge cases, before committing to any approach for a change this small.
- B) Spawn an Explore subagent to investigate the surrounding module in detail before touching the function.
- C) Use `fork_session` to try two candidate one-line fixes in parallel branches and compare the results.
- D) Use direct execution — the fix is simple and well-scoped.

**Question 23.** You are starting a multi-phase task: first understand how authentication works across a large unfamiliar codebase, then implement a change. The discovery phase will involve reading dozens of files, and you're worried the exploration output will exhaust context before implementation begins. What is the best approach?

- A) Read the files in strict alphabetical order and run `/compact` after every ten files to keep context under control, repeating the cycle until every file in the authentication module has been covered.
- B) Use the Explore subagent for discovery, so exploration happens in an isolated context and only a summary returns.
- C) Ask Claude to skip exploration entirely and infer the authentication architecture from the directory names alone.
- D) Split the work across two terminal windows, one dedicated to reading and one dedicated to writing the change.

**Question 24.** You've described a data transformation to Claude in prose three separate times, and each implementation handles the edge cases differently. What is the most effective way to communicate the expected behavior?

- A) Write a longer, more precise prose specification that tries to cover every edge case you can think of, in as much detail as possible.
- B) Ask Claude to restate its understanding of the requirements before implementing, and correct any misunderstanding you spot.
- C) Provide 2–3 concrete input/output examples demonstrating the exact transformation you want, including how each edge case specifically should be handled in the output.
- D) Lower the temperature so that at least the three implementations come out consistent with each other, even if not fully correct.

**Question 25.** Two hours into a legacy-codebase exploration session, Claude starts describing "typical repository patterns" instead of the actual classes it read earlier, and gives inconsistent answers about code it correctly explained an hour ago. Which practice best counteracts this for ongoing long sessions?

- A) Have Claude maintain a scratchpad file recording key findings as it explores, in a consistent, well-organized format, and reference that file when answering later questions instead of relying on conversational memory.
- B) Ask Claude to "focus on the actual code, not typical patterns" every time you notice it drifting.
- C) Paste the important files back into the conversation again each time the drift reappears during the session.
- D) Switch to a model with a larger context window, so the same drift simply takes longer to show up.

**Question 26.** You're mapping a large legacy system. The main session's context is filling with raw file contents from exploration, leaving little room for the architectural reasoning you actually need. What is the best structural fix?

- A) Disable file reading altogether and work only from the directory tree structure that's already visible, inferring the system's architecture purely from file and folder names rather than their actual contents.
- B) Raise `max_tokens` so that the model's responses themselves are allowed to run longer.
- C) Read only the first 50 lines of each file, to cut down on the volume of content being pulled in.
- D) Spawn subagents to investigate specific questions while the main agent preserves context for high-level coordination.

**Question 27.** Mid-session, your context is nearly full of verbose discovery output, but you still need to implement the change in this session and want to keep the essential findings. What should you do?

- A) Start a brand-new session and rely on your own memory of what was learned during the earlier exploration phase, reconstructing the relevant findings from notes as you go along.
- B) Run `/compact` to summarize the conversation and reduce context usage.
- C) Delete the project CLAUDE.md temporarily to free up context space for the remaining work.
- D) Keep working as-is — Claude automatically drops old context the moment it becomes irrelevant to the task.

**Question 28.** You finished a week-long analysis phase for a large migration and are about to spawn implementation subagents for each module. How should the analysis inform the subagents?

- A) Rely on the subagents automatically inheriting the coordinator session's memory of the completed analysis.
- B) Have each subagent redo its own analysis of the relevant module completely from scratch, to guarantee freshness even though the coordinator already spent a week producing exactly this analysis.
- C) Summarize the key findings and inject the relevant summary into each subagent's initial context.
- D) Pass the full multi-day session transcript to every single subagent, so nothing from the analysis is lost.

**Question 29.** Your overnight multi-agent refactoring job occasionally crashes around hour three, and today's restart lost all progress. What design provides crash recovery?

- A) Have each agent export a structured record of its state (completed work, key findings) to a known location, and have the coordinator load a manifest of these exports on resume and inject them back into agent prompts.
- B) Extend the job's timeout window, so the crash-prone stretch is somewhat less likely to be hit on any given run.
- C) Run the full job twice in parallel, on the theory that at least one copy is likely to survive to completion.
- D) Shrink the job's scope so the whole thing tends to finish before the crash window is typically reached.

**Question 30.** You concatenated per-module analyses of 30 modules into a single prompt and asked for architecture recommendations. The recommendations consistently cite modules from the beginning and end of the input but ignore the middle third. What is the best mitigation?

- A) Normalize the module order alphabetically, on the theory that a neutral ordering removes any positional signal the model might otherwise pick up on when scanning through all thirty modules in sequence.
- B) Add an instruction: "Pay equal attention to every module, especially the ones sitting in the middle."
- C) Switch to a model with a larger context window, so all 30 modules fit in more comfortably at once.
- D) Place a key-findings summary up front and organize the module results under explicit headers.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 31.** Cost analysis shows that every query — including simple factual ones like "What is the current federal funds rate?" — runs the full search → analysis → synthesis → report pipeline, taking 4+ minutes. What should change?

- A) Cache pipeline outputs at every stage, so at least repeated queries can return their answer instantly on a second ask, even though a brand-new factual query still has to run the full four-stage pipeline regardless of caching.
- B) Design the coordinator to analyze each query and dynamically invoke only the subagents it actually needs.
- C) Reduce each subagent's token budget across the board, so the full four-stage pipeline simply completes faster end to end.
- D) Add a fifth "quick answer" subagent to the pipeline and route every query through it first before the rest run.

**Question 32.** The synthesis subagent produces generic, thin output that ignores specific data the search agent found. Logs show the synthesis agent's prompt contains only: "Synthesize the findings on renewable energy storage." What is the root cause?

- A) The synthesis agent's prompt directive lacks any instruction about the depth and specificity it's expected to produce, so it defaults to a generic, surface-level style regardless of what data was actually gathered upstream.
- B) The synthesis agent needs a larger context window in order to see the coordinator's own conversation history directly.
- C) Subagents do not inherit the coordinator's conversation history — the findings must be included directly in the synthesis prompt.
- D) The search agent is returning its results in a data format that the synthesis agent's tooling simply cannot parse.

**Question 33.** A research task involves four independent subtopics. The coordinator currently delegates them one at a time, waiting for each subagent to finish before starting the next, quadrupling latency. How should the coordinator spawn the subagents to run them in parallel?

- A) Emit multiple Task tool calls in a single coordinator response, one call per subtopic, so all four subagents start together.
- B) Wrap the Agent SDK in an external async job queue that separately launches four full coordinator processes at once.
- C) Combine all four subtopics into one larger prompt and hand the whole thing to a single subagent to work through together.
- D) Enable streaming on the coordinator's own responses, on the assumption that subagent calls will then overlap automatically.

**Question 34.** Your coordinator is configured with `allowedTools: ["WebSearch", "Read"]`. Instead of delegating, it attempts all research itself and never invokes any subagent. What is wrong?

- A) The subagent definitions are missing their `description` fields, so the coordinator has no visibility into them at all.
- B) The coordinator's underlying model tier is simply too low to support any form of delegation to other agents.
- C) Subagents must first be registered in `.mcp.json` before the coordinator is able to spawn any of them.
- D) The coordinator's `allowedTools` must include `"Task"` — the Task tool is the mechanism for spawning subagents.

**Question 35.** An engineer proposes letting the search agent pass results directly to the analysis agent, bypassing the coordinator to "cut a hop." What is the main argument against this?

- A) Direct subagent-to-subagent communication roughly doubles token usage, since the same results end up serialized twice over, once for the direct hand-off and again whenever the coordinator eventually needs visibility into what happened.
- B) Routing communication through the coordinator preserves observability, consistent error handling, and controlled information flow.
- C) The Agent SDK blocks direct communication between subagents at the protocol level, so the proposal simply can't be built as described.
- D) The analysis agent would need to inherit the search agent's tool permissions, which would violate the system's tool-scoping rules.

**Question 36.** Completed reports are coherent but often have coverage gaps — for instance, missing major recent developments the search agent never looked for. The pipeline currently makes a single pass. What is the most effective architectural improvement?

- A) Add an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient.
- B) Double the number of search results returned per query, so noticeably more raw material is available on the first pass.
- C) Add an instruction to the synthesis agent telling it to write longer, more comprehensive-sounding reports each time.
- D) Switch the search agent to a more capable model, on the assumption that a single stronger first pass will simply find every relevant recent development on its own, without any second look at the topic ever being needed.

**Question 37.** You run two search subagents in parallel for broad topics, but their result sets overlap by roughly 60%, wasting tokens and analysis time. What is the best fix?

- A) Merge the two search agents back into a single agent, so overlapping coverage becomes structurally impossible.
- B) Add a deduplication step in the coordinator that discards repeated sources only after both agents have already finished.
- C) Partition the research scope when delegating — assign each search agent distinct subtopics or source types so their coverage is complementary rather than overlapping.
- D) Have the second agent wait for the first agent's full results and manually steer clear of its already-covered sources.

**Question 38.** Your coordinator prompt gives each subagent a rigid 12-step procedure to follow. Subagents perform well on topics that fit the procedure but fail badly on topics that don't. How should the coordinator's delegation prompts change?

- A) Expand the procedure to 20 steps covering more topic types, and add few-shot examples of each step being followed correctly across a wider range of research subjects than the original twelve steps ever addressed.
- B) Add branching logic to the procedure: "if the topic is technical, do steps 4a–4c instead of the normal sequence."
- C) Remove all instructions entirely and let each subagent improvise its approach from its system prompt alone.
- D) Specify the research goals and quality criteria for each delegation, rather than step-by-step procedures.

**Question 39.** Your system has two tools: `analyze_content` ("Analyzes content and returns insights") and `analyze_document` ("Analyzes documents and returns findings"). Agents misroute between them about 30% of the time. What is the most effective first fix?

- A) Rename the tools to reflect their distinct purposes and rewrite each description to state its purpose, inputs, outputs, and when to use it versus the other.
- B) Add a prompt rule: "When in doubt about which analysis tool to use, prefer analyze_document by default, since it has historically been the safer, more general-purpose choice of the two in most past conversations."
- C) Remove one of the two tools entirely and route all analysis calls through whichever one remains.
- D) Have the coordinator intercept and silently correct misrouted calls with a `PostToolUse` hook after the fact.

**Question 40.** `analyze_document` accepts a `mode` parameter that switches between extraction, summarization, and claim verification. Agents frequently pass the wrong mode and get output they didn't expect. What is the best redesign?

- A) Wrap `mode` in a stricter schema with clearer documentation for each of its three accepted values, and add a validation step that rejects any request naming a mode outside that fixed set before the call ever reaches the tool.
- B) Split the tool into three purpose-specific tools, each with a defined input/output contract.
- C) Default `mode` to summarization, since it's the most common case, so that a wrong mode matters less often.
- D) Have the tool normalize its input and infer the intended mode from the shape of the incoming request instead.

**Question 41.** The synthesis agent's toolset was copy-pasted from the search agent's config and includes `web_search`. You discover it performing new searches mid-synthesis and weaving unvetted, uncited claims into reports. What is the right fix?

- A) Add a prompt rule telling the synthesis agent to only run a search itself when it's strictly necessary to do so.
- B) Reduce the synthesis agent's sampling randomness, on the theory that it will then stick more closely to the findings it was given.
- C) Add a post-hoc citation checker that flags any uncited claims it finds in the final report before it ships.
- D) Restrict each subagent's toolset to its role — remove search tools from the synthesis agent so it works only from the findings it is given.

**Question 42.** The document analysis agent begins every task with 8–10 exploratory `list_documents` and `search_library` calls just to learn what's in the research library. How can you eliminate this overhead?

- A) Cache the exploratory call results for 24 hours, so at least repeated runs on the same day are cheap.
- B) Paste the full library listing into the agent's prompt directive, and remember to update it by hand every single time a document is added, removed, or renamed in the library, however often that happens to be.
- C) Expose the document catalog as an MCP resource for direct visibility into what's available.
- D) Expand the agent's tool-call budget, so the exploratory calls at least complete faster within the run.

**Question 43.** The document analysis agent has a generic `fetch_url` tool and occasionally pulls arbitrary blog pages instead of documents from your vetted research library. What is the best fix?

- A) Replace `fetch_url` with a constrained `load_document` tool that checks URLs against the library.
- B) Add a prompt instruction listing which domains are acceptable for the agent to fetch from during a task.
- C) Log every fetched URL and have someone review the list weekly for policy violations after the fact.
- D) Reduce the agent's sampling randomness, on the theory that a less random model will naturally gravitate toward the same small set of trusted, previously-fetched domains instead of wandering off to arbitrary blog pages on the open web.

**Question 44.** Final reports contain claims with no traceable source. Investigation shows the analysis agent summarizes findings into prose, and by the time synthesis runs, the source associations are gone. What is the fix?

- A) Have the report agent add citations at the very end, by searching after the fact for a plausible-looking source to attach to each claim that survived into the final draft, even though nothing links that source back to where the claim actually originated.
- B) Require subagents to output claim-source mappings as defined fields (claim, source, excerpt), and require synthesis to preserve and merge them rather than compressing findings into prose.
- C) Append a bibliography listing every consulted source to the end of each finished report.
- D) Instruct the synthesis agent to only include claims it can still remember a source for by the time it runs.

**Question 45.** Two credible sources report the market size for the same year as $4.2B and $6.8B. The synthesis agent currently picks one value, seemingly at random. What should it do instead?

- A) Average the two values, report $5.5B, and add a footnote noting that the number is a blend of two sources.
- B) Always prefer whichever source was published more recently, and simply discard the other value outright.
- C) Present both values, explicitly annotated as a conflict, with source attribution and any methodological context explaining the difference.
- D) Omit the statistic entirely from the report, on the theory that conflicting data can't be trusted either way.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** Your review job asks Claude Code for findings and then regex-parses its prose output to post inline PR comments. The parser breaks almost weekly when the output format drifts. What is the robust fix?

- A) Harden the regex with more permissive patterns and add fallbacks for each known format variant as it turns up.
- B) Add a prompt instruction: "Always use the exact output format shown below, and never deviate from it under any circumstances."
- C) Post Claude's entire raw output as a single PR comment instead, so that no parsing step is needed at all.
- D) Run Claude Code with `--output-format json` and a `--json-schema` defining the findings structure, producing machine-parseable output the comment poster can consume directly, without any regex layer between the model and the poster.

**Question 47.** After a developer pushes new commits to a PR, your pipeline re-runs the review, and the bot posts duplicate comments for issues it already flagged and that remain unfixed. How should re-reviews be designed?

- A) Include the prior review's findings in context and instruct Claude to report only new or still-unaddressed issues, without re-posting duplicates.
- B) Review only the files touched by the newest commits, to keep each re-review's scope as minimal as possible, on the assumption that an issue in an untouched file can't have changed and therefore never needs re-checking.
- C) Delete every previous bot comment before each re-review runs, and post the fresh full set from scratch.
- D) Skip re-reviews altogether; treat the single review at PR-open time as sufficient for the whole PR lifecycle.

**Question 48.** Your nightly test-generation job produces mostly low-value tests — trivial getter checks and tests of framework behavior — and never uses the fixture factories your team built. What is the most effective fix?

- A) Generate three times as many tests as before, and have a second automated job filter out whichever ones look low-value after the fact, on the theory that more raw volume up front makes the eventual filtered set better.
- B) Document your testing standards, valuable-test criteria, and fixture factories in CLAUDE.md.
- C) Post-process the generated tests to inject fixture factory imports into them automatically after generation.
- D) Restrict generation to files under 50% coverage, on the theory that any test added there adds value by default.

**Question 49.** Your review bot flags too many trivial style nitpicks. You added "Be conservative — only report issues you are highly confident about" to the prompt, but the false positive rate barely moved. What should you do instead?

- A) Strengthen the wording further, to "Only report issues you are 100% certain about, with no exceptions."
- B) Add a second reviewer model to the pipeline, and only post the findings both models happen to agree on.
- C) Replace confidence-based filtering with explicit categorical criteria defining which issue types to report (bugs, security vulnerabilities) and which to skip (minor style, local naming patterns).
- D) Have the bot self-assign a numeric confidence score to each finding and filter out anything below a threshold.

**Question 50.** False-positive analysis shows the "performance" review category is 70% false positives while all other categories are under 10%. Developers have started ignoring all bot findings, including accurate security ones. What is the best immediate action?

- A) Temporarily disable the performance category to restore trust in the remaining categories, while its prompts are reworked.
- B) Keep all categories enabled as-is, but add a disclaimer noting that performance findings are still experimental.
- C) Lower the displayed severity of performance findings across the board, so they read as less alarming to developers, while still leaving the same 70% false-positive rate quietly buried inside every PR review that gets posted.
- D) Batch performance findings into a weekly digest email instead of posting them as PR comments in real time.

**Question 51.** The same type of issue gets labeled "critical" in one PR and "minor" in another. Severity drives your merge-blocking logic, so inconsistency is breaking the pipeline's usefulness. What is the most effective fix?

- A) Remove severity from findings entirely, and simply block any merge that has any finding at all, of any kind.
- B) Ask the model to re-validate each severity label itself, against no defined standard, before finalizing the output.
- C) Map severity purely from the finding's category (all security findings become critical, all style findings become minor).
- D) Define explicit severity criteria in the prompt with concrete code examples illustrating each severity level.

**Question 52.** Despite detailed formatting instructions, review findings arrive in inconsistent shapes — sometimes missing the file location, sometimes merging several issues into one paragraph. What is the most effective technique to get consistent, actionable findings?

- A) Repeat the same formatting instructions at both the very start and the very end of the prompt for emphasis, on the theory that saying the same rule twice will succeed where saying it once has already failed to produce consistent shapes.
- B) Add few-shot examples demonstrating the exact desired output shape — location, issue, severity, and fix — for several finding types.
- C) Raise `max_tokens` so the model always has enough room left to complete every field of every finding.
- D) Post-process the output with a second Claude call whose only job is to reformat whatever came out of the first.

**Question 53.** Your codebase intentionally uses patterns that the reviewer keeps flagging — like empty catch blocks (with explanatory comments) inside retry helpers. You can't enumerate every acceptable pattern in the prompt. What approach reduces these false positives while still catching genuine issues?

- A) Suppress all findings that involve a catch block anywhere in the codebase, full stop, regardless of context.
- B) Add inline "claude-ignore" comments at every single intentional-pattern site across the codebase.
- C) Add a handful of few-shot examples contrasting acceptable intentional patterns with genuine issues, so the model learns the underlying judgment and generalizes it to novel cases it hasn't seen labeled before.
- D) Maintain an exhaustive allowlist file of every acceptable pattern and check each new finding against it before posting, updating the file by hand any time the codebase adds a new intentional pattern.

**Question 54.** You're building the review bot on the Agent SDK, and it returns findings as JSON inside its text response. About 5% of runs produce malformed JSON that crashes the comment poster. What is the most reliable fix?

- A) Define a `report_findings` tool whose input contract is your findings structure, and read from the `tool_use` block instead of parsing text.
- B) Wrap the JSON parse in a try/catch and automatically re-request the output on failure with "valid JSON only," retrying up to three times before finally giving up and surfacing the run as a failure to the pipeline.
- C) Ask for YAML output instead of JSON, since YAML is generally more forgiving of small formatting drift.
- D) Add a JSON-repair library that fixes trailing commas and unquoted keys before the parse step runs.

**Question 55.** Your review bot has two tools — `report_findings` and `approve_pr` — but sometimes it replies with conversational text like "The code looks good to me!" and calls neither. Downstream automation requires a tool call every time. What is the fix?

- A) Force `tool_choice: {"type": "tool", "name": "report_findings"}` so that a tool is always called on every run.
- B) Add a prompt instruction telling the bot to always call one of the two tools before it finishes responding.
- C) Parse any conversational responses that slip through and infer an approval from the general sentiment of the text.
- D) Set `tool_choice: "any"` so the model must call a tool but can still choose the appropriate one itself.

**Question 56.** Since switching to tool_use with a strict JSON schema, review outputs always parse — but some findings reference line numbers pointing at the wrong lines, and severity labels occasionally contradict the description text. What should you conclude?

- A) The schema needs stricter typing; changing line numbers to a bounded integer range tied to the diff's own line count will fix the misalignment on its own, without requiring any separate validation pass afterward.
- B) Strict tool-use contracts eliminate syntax errors but not semantic errors — you need semantic validation layered on top, such as checking line references against the diff and cross-checking severity against criteria.
- C) The model is being cut off mid-generation; raising `max_tokens` will resolve both problems at once.
- D) Tool use is fundamentally unsuitable for code review output; revert to prose findings with full human triage instead.

**Question 57.** Your semantic validator rejects a finding because it references a file that isn't part of the PR diff. What is the most effective retry design?

- A) Retry with an identical prompt, on the assumption that a validation failure like this is usually just transient.
- B) Silently drop the invalid finding and move on, continuing with whichever findings did pass validation.
- C) Send a follow-up request that includes the original context, the failed output, and the specific validation error ("finding 3 references src/util.ts, which is not in this diff"), asking the model to correct it.
- D) Regenerate the entire review from scratch with a different sampling seed and hope the new run avoids the issue.

**Question 58.** Developers dismiss about 40% of the bot's findings, but you have no systematic way to learn which kinds of code constructs trigger the bad findings. What schema change enables this analysis?

- A) Add a free-text `notes` field with a loosely structured explanation of the model's own reasoning behind each finding, written out at whatever length the model happens to choose for that particular run.
- B) Add a `reviewer_id` field, so you can compare dismissal rates across different model versions over time.
- C) Add a `confidence` field and simply assume that whichever findings get dismissed were low-confidence ones.
- D) Add a `detected_pattern` field capturing which construct triggered each finding, so dismissals can be aggregated by pattern.

**Question 59.** An engineer proposes moving your agentic "generate tests, run them, fix failures, repeat" workflow to the Message Batches API for the 50% cost savings. Why won't this work?

- A) The Batch API doesn't support multi-turn tool calling within a request — it can't execute your test-runner tool mid-request and return results to the model, which this iterative generate-run-fix loop fundamentally requires.
- B) The Batch API's 24-hour completion window is simply too slow for an overnight job of this size to finish in time.
- C) Batch requests can't include a prompt directive at all, which this entire workflow structurally depends on to run.
- D) The Batch API caps individual requests at a context size too small to hold the project's test files.

**Question 60.** Your pipeline has the same Claude Code session generate a feature and then immediately review its own changes. The self-reviews rarely find problems, yet human reviewers regularly catch real bugs in the same code. What is the most effective fix?

- A) Add "review your work with fresh eyes and maximum skepticism" to the self-review prompt directive, and repeat the same instruction a second time immediately before the review step actually runs, for emphasis.
- B) Have a second, independent Claude instance perform the review, without the generator's own reasoning context.
- C) Enable extended thinking during the self-review step, so the model reasons more deeply before responding.
- D) Have the same session review the exact same code three times in a row and merge the three sets of findings.

---
# Answer Key — Practice Exam 1

**Quick key:** 1-B, 2-A, 3-D, 4-C, 5-B, 6-D, 7-B, 8-A, 9-C, 10-A, 11-D, 12-C, 13-B, 14-D, 15-A, 16-C, 17-A, 18-B, 19-D, 20-C, 21-A, 22-D, 23-B, 24-C, 25-A, 26-D, 27-B, 28-C, 29-A, 30-D, 31-B, 32-C, 33-A, 34-D, 35-B, 36-A, 37-C, 38-D, 39-A, 40-B, 41-D, 42-C, 43-A, 44-B, 45-C, 46-D, 47-A, 48-B, 49-C, 50-A, 51-D, 52-B, 53-C, 54-A, 55-D, 56-B, 57-C, 58-D, 59-A, 60-B

---

**1. B** — The agentic loop must key off `stop_reason`: continue while it is `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Expanding the phrase list and adding fuzzy matching (A) still parses natural language for a structural signal and will keep missing new phrasings no matter how often it's retuned. Iteration caps (C) are a safety backstop, not a primary stopping mechanism, and truncate legitimate long cases. D inverts the semantics: absence of text says nothing definitive about completion.

**2. A** — Tool results must be appended to the conversation history as a `tool_result` block referencing the `tool_use` ID, then the whole conversation is sent back so the model can incorporate the result into its next reasoning step. B keeps the result out of the model's own context entirely — it never gets to confirm the refund happened. C misuses the prompt directive for turn-level data that should live in the conversation, not the instructions. D destroys conversational state mid-task and is unnecessary here.

**3. D** — A `PostToolUse` hook deterministically normalizes heterogeneous formats before the model ever sees them, removing the error class entirely. Prompt instructions asking the agent to normalize the values itself (A) rely on probabilistic per-turn conversions and will still fail occasionally. B is organizationally impractical and out of your control on this release. C detects errors after they've already influenced the conversation instead of preventing them.

**4. C** — A business rule with financial consequences needs deterministic enforcement: intercept the tool call, block amounts over $500, and redirect to escalation. Prompt placement (A), few-shot examples (B), and lowering sampling randomness (D) all still rely on probabilistic compliance — the observed 2% failure rate is precisely why prompt-only enforcement is insufficient here.

**5. B** — The recommended pattern is decomposing multi-concern requests into distinct items, investigating each in parallel with shared context, then synthesizing one unified resolution. A pushes the decomposition work onto the customer. C escalates cases the agent could resolve, hurting first-contact resolution. D discards the shared context (customer identity, verification) that the concerns have in common.

**6. D** — Humans without transcript access need a structured handoff: customer ID, root cause analysis, amount, recommended action — everything needed to act immediately. A raw transcript (A) forces the human to reconstruct the case anyway, just from more text. B omits the case analysis entirely. C conveys mood, not the facts needed to resolve the dispute.

**7. B** — "Refunds only to the verified original payment method" is a hard compliance rule where any violation has financial/fraud consequences — the case for programmatic enforcement (a hook gating `process_refund`). Tone (A), conciseness (C), and a soft self-reminder to offer alternatives first (D) are behavioral guidance where occasional imperfection is acceptable, so prompt instructions are appropriate.

**8. A** — This workload is explicitly high-ambiguity: the right tools and their order genuinely vary per case, and intermediate results (e.g., what `lookup_order` reveals) change what should happen next — the core argument for model-driven decision-making. B is false; you can hardcode sequences around the SDK. C is false in general (and irrelevant here). D is false — decision trees can call any tool; that's not the issue.

**9. C** — Detailed error metadata (`errorCategory`, `isRetryable`, description) gives the agent what it needs to retry transient failures and stop retrying non-retryable ones. Blanket retry (A) wastes calls on business errors and hides the retry decision from the agent entirely. B asks the model to guess what the tool already knows. D reduces one error type's frequency without fixing the decision-making problem.

**10. A** — Business-rule violations should come back as structured errors with `retriable: false` and a customer-friendly explanation so the agent can communicate accurately and pivot to alternatives (store credit). B gives the agent nothing to reason with. C silently misrepresents a failure as success — the agent may tell the customer the refund happened. D leaks internals and buries the relevant fact (policy window) in noise.

**11. D** — "No orders" is a valid empty result of a successful query, not a failure; conflating the two causes exactly the observed misbehavior (apologizing, retrying). Errors should be reserved for access failures. A patches the symptom with prompt text while the underlying contract stays broken. B hides real signal behind a hook. C invents a spurious recovery path for a non-error.

**12. C** — Keyword-sensitive prompt directives can create unintended tool associations that override even good tool descriptions — "any customer question about their purchases" is sweeping policy questions into `lookup_order`. A and D modify the tool when the tool isn't the actual problem. B adds token overhead to counteract an instruction you can simply fix at the source.

**13. B** — Growing from 4 to 18 tools on one agent increases decision complexity and degrades tool selection reliability. The fix is scoped tool access per role (or splitting into specialized agents). A and C describe limits that don't exist. D misdescribes how tool use works — agents don't call every available tool.

**14. D** — Forced tool selection (`tool_choice: {"type": "tool", "name": "classify_request"}`) on the first request is the only option that *guarantees* that specific tool runs first; later turns then proceed normally. A and C are probabilistic. B (`"any"`) guarantees *some* tool call, but not which one — the agent could call `get_customer` first instead.

**15. A** — Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block that rides outside the summarized history is the recommended defense against progressive summarization degrading precise values into vague ones ("around $80"). B only delays the loss. C works but adds cost and latency on every turn for data that isn't changing. D pushes the system's memory problem onto the customer.

**16. C** — `~/.claude/CLAUDE.md` is user-level configuration: it applies to your account only and never travels through version control. Team-wide standards belong in a project-level CLAUDE.md committed to the repo. A misstates what `/memory` does (it inspects loaded memory; it doesn't "activate" anything). B — project CLAUDE.md loads without imports. D invents a failure mode that doesn't exist.

**17. A** — `@import` keeps CLAUDE.md modular: each package's CLAUDE.md pulls in only the relevant shared standards files, and package maintainers with domain knowledge own the selection. B creates six diverging copies. C still loads all 900 lines every session — a table of contents doesn't reduce what's loaded. D makes standards invisible to Claude by default.

**18. B** — Inconsistent behavior across sessions is the classic symptom of different memory files being loaded in different sessions; `/memory` shows exactly which files are in effect, so diagnose before rewriting anything. A and D change content before you know whether content is even the problem. C addresses context pressure, not configuration loading.

**19. D** — `context: fork` runs the skill in an isolated sub-agent context so its verbose output never enters (pollutes) the main conversation — only the useful summary returns. A reduces volume but the output still lands in the main context. B makes it worse: always-loaded verbosity. C restricts capability, not where the output ends up.

**20. C** — `allowed-tools` in the skill frontmatter is the enforcement mechanism: restrict the skill to file-creation operations and Bash simply isn't available during execution. A is prompt-based and probabilistic — the failure already happened despite the skill's own instructions. B mitigates damage rather than preventing it. D is false — slash commands don't disable tools.

**21. A** — Universal, always-applicable standards belong in CLAUDE.md (loaded every session); task-specific workflows used occasionally belong in skills (loaded on demand). B pays the release-notes workflow's context cost in every session, whether or not a release is happening. C means conventions only apply when someone remembers to invoke them. D is backwards on both counts.

**22. D** — A single-file, single-line fix with a stack trace pointing at the location is the textbook case for direct execution; plan mode (A), exploration subagents (B), and session forking (C) all add overhead with no decision-making or architectural payoff for a change this well-scoped.

**23. B** — The Explore subagent is designed for exactly this: verbose discovery runs in an isolated context and returns a summary, preserving the main conversation's context for the implementation phase. A still floods the main context between compactions. C trades context for guessing. D describes two unrelated sessions, not a shared-context workflow.

**24. C** — Concrete input/output examples are the most effective way to communicate expected transformations when prose is being interpreted inconsistently — they pin down the edge cases directly. A produces more prose subject to the same interpretation problem. B surfaces misunderstandings but doesn't pin down edge-case behavior the way examples do. D makes outputs consistent with each other, not correct.

**25. A** — Context degradation in extended sessions (drifting to "typical patterns" instead of discovered specifics) is counteracted by persisting key findings to a scratchpad file in a consistent format and referencing it for subsequent questions — the findings survive outside degrading conversational context. B asks the model to fix a context problem with willpower. C repeatedly re-spends context and accelerates the problem. D delays symptoms without adding persistence.

**26. D** — Delegating specific investigation questions to subagents isolates the verbose file-dump output in their contexts, while the main agent keeps its own context for high-level coordination. A and C sacrifice the understanding you actually need. B is unrelated — `max_tokens` governs response length, not context accumulation.

**27. B** — `/compact` summarizes the conversation to reduce context usage while preserving key information — the right mid-session relief valve when you need to keep working. A discards the findings (Claude has no cross-session memory of them). C frees trivial space and drops your standards along with it. D describes behavior that doesn't exist.

**28. C** — The reliable pattern is summarizing key findings from the completed phase and injecting the relevant summary into each subagent's initial context. A fails because subagents do not inherit parent context automatically. B re-spends a week of analysis per module. D floods each subagent's context with mostly-irrelevant transcript, inviting lost-in-the-middle problems.

**29. A** — Structured state export is the crash-recovery pattern: each agent exports completed work and key findings to a known location; on resume the coordinator loads the manifest and injects that state into agent prompts, resuming rather than restarting. B and D reduce crash odds but don't recover from one when it happens. C doubles cost for a coin-flip.

**30. D** — This is the lost-in-the-middle effect: models reliably process the beginning and end of long inputs but may omit middle sections. The mitigation is a key-findings summary up front plus explicit section headers organizing the detail. A changes ordering without addressing position effects. B — instructions don't fix attention position biases. C — the effect persists in larger windows too.

**31. B** — The coordinator should analyze query requirements and dynamically select which subagents to invoke; simple factual queries shouldn't traverse the full pipeline. A only helps repeated queries. C makes every stage worse instead of skipping unneeded stages. D adds a fifth stage to a pipeline whose actual problem is mandatory stages.

**32. C** — Subagents operate with isolated context: they do not inherit the coordinator's conversation history. The synthesis prompt must include the actual search results and analysis outputs directly. A would deepen prose style but can't conjure data the agent never received. B misunderstands isolation — window size is irrelevant if the content is never passed at all. D is contradicted by the logs: nothing was passed at all.

**33. A** — Parallel subagents are spawned by emitting multiple Task tool calls in a single coordinator response, rather than one per turn. B bolts external infrastructure onto a problem the SDK pattern already solves. C serializes the work inside one context and loses the parallelism entirely. D — streaming affects token delivery, not tool-call concurrency.

**34. D** — The Task tool is the mechanism for spawning subagents; if `"Task"` isn't in the coordinator's `allowedTools`, it cannot delegate and will attempt the work itself. A affects selection quality among subagents, not the total inability to spawn any. B and C describe requirements that don't exist.

**35. B** — Hub-and-spoke routing through the coordinator is what provides observability, consistent error handling, and controlled information flow; a direct side channel sacrifices all three. A invents a token penalty that doesn't follow from the design. C is false — you could build it, it's just a bad idea. D is a side detail, not the main architectural argument.

**36. A** — Coverage gaps are addressed with an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient. B adds volume, not targeted coverage. C asks for length — the missing material was never gathered in the first place. D still makes a single pass with no gap-checking mechanism at all.

**37. C** — Partitioning research scope — assigning each agent distinct subtopics or source types — prevents duplication at the source. B deduplicates after the tokens and analysis time are already spent. A gives up the parallelism that motivated using two agents in the first place. D serializes the agents, also defeating parallelism.

**38. D** — Coordinator prompts should specify research goals and quality criteria rather than step-by-step procedures, enabling subagents to adapt their approach to each topic. A and B double down on rigid proceduralism — there will always be topics outside the script. C removes direction entirely; goals and quality bars are still needed.

**39. A** — Tool descriptions are the primary mechanism for tool selection; near-identical names and descriptions cause misrouting. Renaming to purpose-specific names and rewriting descriptions (purpose, inputs, outputs, when-to-use-vs-the-other) fixes the root cause. B papers over ambiguity with a default. C may discard needed functionality. D corrects symptoms downstream and needs its own routing logic — the very thing that's broken.

**40. B** — A generic tool with mode switches invites wrong-mode calls; splitting into purpose-specific tools (`extract_data_points`, `summarize_content`, `verify_claim_against_source`) with clear contracts makes selection explicit. A keeps the confusing single entry point. C substitutes a silent wrong behavior for an error. D makes behavior unpredictable and hard to debug.

**41. D** — Agents with tools outside their specialization tend to misuse them; the synthesis agent's job is to work from provided findings, so search tools should be removed from its set (scoped tool access). A is probabilistic and the misuse is already happening. B doesn't remove the capability at all. C flags damage after publication instead of preventing it.

**42. C** — MCP resources exist to expose content catalogs — giving agents visibility into available data without exploratory tool calls. A makes the waste cheaper, not gone. B is a manual, drift-prone copy of what resources provide natively. D speeds up the overhead instead of eliminating it.

**43. A** — Replacing the generic `fetch_url` with a constrained `load_document` that checks URLs against the vetted library makes the boundary structural rather than behavioral. B relies on prompt compliance alone. C detects violations after they've already contaminated the research. D doesn't address capability at all.

**44. B** — Attribution survives only if subagents emit claim-source mappings as defined fields (claim, source, excerpt) and the synthesis agent is required to preserve and merge them; prose summarization is where provenance dies. A fabricates citations after the fact — worse than none at all. C lists sources without linking claims to them. D relies on memory of information that was already compressed away.

**45. C** — Conflicting statistics from credible sources should be presented with explicit conflict annotation, source attribution, and methodological context — not resolved arbitrarily. A invents a number no source reported. B assumes recency explains the difference (it may be methodology or scope instead). D throws away material information the reader needs.

**46. D** — `--output-format json` with `--json-schema` produces machine-parseable, schema-conforming output — the supported mechanism for structured findings in CI. A and B keep betting on format stability that prose output doesn't guarantee. C abandons the inline-comment requirement rather than meeting it.

**47. A** — The documented pattern for re-reviews: include prior findings in context and instruct Claude to report only new or still-unaddressed issues, avoiding duplicate comments. B misses issues that new commits introduce in interaction with unchanged files. C recreates comment noise and destroys discussion threads. D leaves post-push changes unreviewed entirely.

**48. B** — CLAUDE.md is the mechanism for giving CI-invoked Claude Code project context: testing standards, what makes a test valuable, and which fixtures exist. Without it the generator can't know your conventions. A generates waste then filters it. C injects imports into tests that still don't use the factories meaningfully. D narrows scope without improving quality within it.

**49. C** — General instructions like "be conservative" or "high-confidence only" demonstrably fail to improve precision; explicit categorical criteria — report these types, skip those types — are what work. A is more of the same failed approach. D relies on self-reported confidence, which is poorly calibrated. B doubles cost and still lacks defined criteria for either reviewer.

**50. A** — One high-false-positive category undermines trust in all categories. Temporarily disabling the 70%-FP performance category restores signal quality immediately while you improve its prompts offline. B, C, and D all keep the noise flowing in some form, and trust keeps eroding.

**51. D** — Consistent classification comes from explicit severity criteria with concrete code examples for each level. A makes every nitpick merge-blocking. B is self-review with no standard to check against. C is too coarse — not all security findings are critical, and category isn't the same thing as impact.

**52. B** — When detailed instructions alone produce inconsistent output, few-shot examples demonstrating the exact desired format (location, issue, severity, suggested fix) are the most effective technique for consistency. A repeats what already isn't working. C addresses truncation, which isn't the symptom described. D adds cost and a second chance for drift.

**53. C** — Few-shot examples contrasting acceptable intentional patterns with genuine issues let the model generalize the judgment to novel cases — exactly what an enumerated allowlist (D) can't do. A suppresses real bugs involving catch blocks. B requires annotating the whole codebase and doesn't help with new code written later.

**54. A** — Tool use with a JSON schema is the most reliable path to structured output: the `report_findings` tool's input contract guarantees well-formed structure, eliminating the JSON-in-text syntax errors outright. B and D are recovery layers for a problem you can eliminate outright instead. C trades one fragile text format for another.

**55. D** — `tool_choice: "any"` guarantees the model calls *a* tool while leaving it free to pick the appropriate one (`report_findings` vs `approve_pr`). A forces every response through `report_findings`, breaking approvals. B is probabilistic — the failure already occurs despite instructions telling it otherwise. C is sentiment-parsing fragility replacing a structural guarantee.

**56. B** — Strict schemas via tool use eliminate *syntax* errors but not *semantic* errors — wrong line numbers and contradictory severities are semantically wrong, schema-valid outputs. The fix is semantic validation layered on top of the schema. A — a bounded range can't know which line is actually correct. C misdiagnoses; truncated output would fail schema validation outright. D throws away the syntax guarantee to fix nothing.

**57. C** — Retry-with-error-feedback: include the original context, the failed output, and the specific validation error so the model can self-correct. An identical retry (A) has no new information and will likely fail identically. B silently loses a possibly-real finding that just referenced the wrong file. D discards all the valid findings along with the one invalid one.

**58. D** — A `detected_pattern` field records which code construct triggered each finding, enabling systematic aggregation of dismissals by pattern — the feedback loop you're missing. A gives unstructured text you can't aggregate. B varies the wrong dimension entirely. C assumes the very correlation you're trying to measure.

**59. A** — The Batch API does not support multi-turn tool calling within a request: it cannot pause mid-request, execute your test-runner tool, and feed results back to the model. An iterative generate-run-fix loop is inherently multi-turn tool use, which batching's independent-request model doesn't accommodate. B is backwards — overnight jobs are the Batch API's sweet spot. C and D describe restrictions that don't exist.

**60. B** — A model reviewing its own generation retains the reasoning context that produced the code, making it unlikely to question its own decisions. An independent instance without that context is more effective at catching subtle issues. A and C try to prompt or think around a structural bias instead of removing it. D repeats the same biased review three times.

---

*End of Practice Exam 1.*
