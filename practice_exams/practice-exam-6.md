# CCAFC Practice Exam 6

**Claude Certified Architect – Foundations — Practice Exam**

Rebalanced edition of Practice Exam 1 — same knowledge points; options rewritten to remove test-taking tells (option-length cues, giveaway distractors), answer letters reshuffled.

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

- A) Expand the terminal-phrase list and add fuzzy matching so paraphrases like "we're all set" or "that wraps it up" are also caught.
- B) Cap the loop at a fixed 10 iterations per conversation, since internal metrics show most cases resolve within that window, and escalate anything that runs longer.
- C) Continue the loop while `stop_reason` is `"tool_use"`, executing tools; terminate on `"end_turn"`.
- D) Terminate whenever a response arrives with no text content, treating any tool-only turn as a signal the case is closed.

**Question 2.** Your agent calls `process_refund` and your code executes the refund successfully. What must happen next so the agent can correctly continue the conversation?

- A) Store the confirmation in your database and have the agent summarize all tool activity once the ticket is marked closed.
- B) Inject the refund confirmation into the system prompt via a hook so it stays available across every later turn.
- C) Start a new conversation seeded with a structured summary of prior turns plus the refund result, discarding the original transcript.
- D) Append a `tool_result` block (with the `tool_use` ID) in a user message and resend the conversation.

**Question 3.** Your MCP tools come from different backend teams: `get_customer` returns ISO 8601 dates, `lookup_order` returns Unix timestamps, and order statuses are numeric codes in one tool but strings in another. The agent occasionally miscompares dates and misreads statuses when reasoning across tools. What is the most reliable fix?

- A) Document each tool's date and status formats in the system prompt, with explicit normalization instructions for the model to apply manually on every turn.
- B) Normalize dates, timestamps, and status codes in a `PostToolUse` hook before the model sees them.
- C) Ask the backend teams to migrate their APIs to one shared, validated format standard, closing the ticket once all three sign off.
- D) Validate the agent's final answer for date and status errors at the end of the conversation, before it reaches the customer.

**Question 4.** Company policy requires human approval for any refund over $500. Your system prompt states this rule prominently, but production logs show that about 2% of refunds above $500 are still processed autonomously. What should you do?

- A) Intercept `process_refund` calls with a hook that blocks amounts over $500 and redirects to escalation.
- B) Move the $500 rule to the very top of the system prompt and repeat it again immediately before the tool definitions.
- C) Add few-shot examples of the agent escalating specific refund amounts like $501, $750, and $1,200 so the pattern generalizes.
- D) Add a self-confirmation step where the agent asks itself whether the amount is under $500 before calling `process_refund`.

**Question 5.** A customer writes one message reporting a damaged item, a duplicate charge on their card, and an address change for an upcoming shipment. The agent resolves the damaged item and ends the conversation without addressing the other two concerns. What is the best design change?

- A) Detect multi-issue messages with a classifier and ask the customer to file a separate ticket for each additional concern.
- B) Route any message containing more than one concern to `escalate_to_human`, since multi-issue cases need a human's judgment.
- C) Handle each concern in its own fresh session, so every issue gets a clean context window free of the others.
- D) Decompose the message into distinct items, investigate each with shared context, and synthesize one resolution.

**Question 6.** When the agent escalates a billing dispute to a human agent, the human team works in a separate system with no access to the AI conversation transcript. Human agents report spending 10+ minutes reconstructing each case. What should the escalation include?

- A) The complete raw conversation transcript, exported as plain text, so the human has every detail if needed.
- B) A structured summary: customer ID, root cause, disputed amount, and recommended action.
- C) The customer ID plus a profile link, keeping the handoff lightweight so the queue doesn't back up.
- D) A sentiment analysis of the conversation, scoring the customer's frustration level from the transcript.

**Question 7.** You are deciding which agent behaviors need programmatic enforcement (hooks) versus system-prompt guidance. Which requirement is the strongest candidate for a hook rather than prompt instructions?

- A) Maintaining an empathetic, professional tone even with customers who are frustrated or upset.
- B) Keeping responses concise and free of unnecessary technical jargon in every reply.
- C) Ensuring refunds are only issued to the verified original payment method.
- D) Offering troubleshooting alternatives before proposing any refund, whenever the issue allows it.

**Question 8.** A product manager proposes replacing the agent's reasoning with a fixed sequence — always call `get_customer`, then `lookup_order`, then either resolve or refund — arguing it will make behavior predictable. Why is model-driven tool selection the better fit for this workload?

- A) Model-driven selection is always cheaper, since the model skips the reasoning tokens a fixed script would otherwise require.
- B) Support requests vary too much for one sequence: the tools needed differ per case, and intermediate results change what should happen next.
- C) A fixed sequence would break session resumption, which depends on the model choosing its own tool order each time.
- D) Decision trees cannot access conversation history, so a hard-coded sequence could never reference an earlier turn.

**Question 9.** Every failure from `process_refund` currently returns the same response: `"Operation failed"`. Logs show the agent retrying policy-violation failures repeatedly (which will never succeed) and giving up immediately on transient gateway timeouts (which would succeed on retry). What is the best fix?

- A) Wrap all tool calls in an automatic retry-three-times policy at the application layer, regardless of error type.
- B) Tell the agent in the system prompt to judge retryability from conversation context and its own experience with similar cases.
- C) Increase the payment gateway's timeout threshold so transient failures become rare enough to stop mattering.
- D) Return structured errors with an `errorCategory`, an `isRetryable` boolean, and a description.

**Question 10.** A customer requests a refund for an order purchased 47 days ago; policy allows refunds within 30 days. What should `process_refund` return so the agent handles this well?

- A) A standard HTTP 400 status code with no body, letting the agent infer the cause from its own original request.
- B) A success response with an empty body, so the agent avoids alarming the customer with error language.
- C) A business-category error with `retriable: false`, a customer-friendly explanation, and an alternative to offer.
- D) An error carrying the full server-side stack trace, so the agent has maximum technical detail to reason with.

**Question 11.** When a customer has no orders on file, `lookup_order` currently returns an error, and the agent responds by apologizing for "technical difficulties" and retrying the lookup. What should change?

- A) Return a successful empty result set (with a note like "no orders found"), reserving errors for access failures.
- B) Add a system prompt note explaining that this particular error usually just means the customer has no orders.
- C) Suppress the error in a `PostToolUse` hook and instruct the agent to end the conversation gracefully.
- D) Have the agent call `get_customer` again first to validate the original customer ID before giving up.

**Question 12.** Your tool descriptions are detailed and well-differentiated, yet the agent calls `lookup_order` even for general return-policy questions where no order is involved. You find this line in the system prompt: "Use lookup_order to help with any customer question about their purchases." What is the most likely fix?

- A) Rewrite the `lookup_order` description to explicitly say it must not be used for general policy questions.
- B) Reword or remove the keyword-sensitive system prompt line that is overriding the tool descriptions.
- C) Add a few-shot example showing a policy question being answered correctly with no tool call at all.
- D) Rename the tool `lookup_order_by_id` so the model understands that a specific order ID is required.

**Question 13.** The support team wants to expand the agent from its current 4 tools to 18 by adding loyalty-program, marketing-preferences, subscription, and gift-card tools — all attached to the single resolution agent. What is the primary risk?

- A) The MCP protocol enforces a hard limit of 10 tools per server, so the added configuration will fail to connect.
- B) The added tool schemas will exceed the model's context window before any conversation even begins.
- C) The agent will slow down because it must call every available tool at least once per conversation to check relevance.
- D) Tool selection reliability degrades as the tool count grows, increasing misrouting.

**Question 14.** Compliance requires that every conversation begin with a call to a `classify_request` tool before any other tool runs, with no exceptions. What is the most reliable implementation?

- A) Set `tool_choice: {"type": "tool", "name": "classify_request"}` on the first request, then normal tool choice afterward.
- B) State plainly in the system prompt that `classify_request` is mandatory and must always be called first, no exceptions.
- C) Set `tool_choice: "any"` on the first request, so a tool call is guaranteed before any customer-facing response.
- D) Add several few-shot examples showing `classify_request` being called first across a range of conversation types.

**Question 15.** In long billing-dispute conversations, your context management summarizes older turns. After summarization, the agent starts misstating specifics — quoting "around $80" for a refund the customer was promised at exactly $83.47. What is the best fix?

- A) Raise the summarization step's length limit and normalize numeric values so more detail from older turns is retained.
- B) Re-run `lookup_order` and `get_customer` on every turn and store the results in a structured cache, so the freshest data is always in context.
- C) Extract transactional facts into a persistent "case facts" block included in every prompt.
- D) Ask the customer to re-confirm key dollar amounts whenever a conversation exceeds 20 turns.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.

---

**Question 16.** You maintain your team's coding standards in `~/.claude/CLAUDE.md` on your machine. A new teammate clones the repository, but Claude Code ignores all of those standards for them. Why?

- A) The new teammate needs to run `/memory` once after cloning to activate the memory system for their account.
- B) User-level `~/.claude/CLAUDE.md` applies only to your account; team standards belong in a project-level CLAUDE.md.
- C) CLAUDE.md files require an explicit `@import` from the project root before any of their content takes effect.
- D) The standards file exceeds the size limit for automatic loading, so it is being silently truncated on load.

**Question 17.** Your monorepo has six packages with mostly shared standards but some package-specific conventions. The root CLAUDE.md has grown to 900 lines and every session loads all of it regardless of which package is being edited. Package maintainers know their own conventions best. What is the most maintainable structure?

- A) Duplicate the full standards document into each of the six package directories so every package is self-contained.
- B) Keep the single 900-line root CLAUDE.md, but add a table of contents so the model can jump straight to a package's section instead of reading every line each session.
- C) Move all standards into a structured team wiki and instruct Claude to ask developers for conventions whenever it is unsure.
- D) Keep shared standards in focused files; each package's CLAUDE.md uses `@import` to pull in only what applies.

**Question 18.** Claude Code follows your API error-handling conventions in some sessions but not others, with no obvious pattern. What is the best first diagnostic step?

- A) Run `/memory` to verify which memory files are actually loaded in the affected sessions.
- B) Rewrite the error-handling section of CLAUDE.md with stronger, more imperative language throughout.
- C) Run `/compact` to clear stale context that might be silently overriding the documented conventions.
- D) Delete and recreate the project CLAUDE.md from scratch to rule out file corruption.

**Question 19.** Your team's `/analyze-deps` skill walks the dependency graph and prints thousands of lines of package data. Developers complain that after running it, Claude's answers about their actual coding task get noticeably worse. What change fixes this?

- A) Add `argument-hint` frontmatter so developers can scope the dependency analysis to a single package, cutting the volume of graph data walked in one run.
- B) Move the dependency-analysis instructions directly into CLAUDE.md so no separate skill invocation is needed.
- C) Add `context: fork` so the skill runs in an isolated sub-agent context and returns a summary.
- D) Add `allowed-tools` frontmatter restricting the skill to read-only operations, reducing its output volume.

**Question 20.** Your `/scaffold-component` skill should only ever create new files from templates. During an audit you find a session where it also ran shell commands, including a `git checkout` that discarded a developer's uncommitted changes. What is the right guardrail?

- A) Add a warning to the skill's SKILL.md instructions telling Claude it must never run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations.
- C) Require developers to commit all of their work before running any project skill.
- D) Convert the skill into a slash command instead, since slash commands cannot execute tools.

**Question 21.** Your team has two assets: (1) universal naming and error-handling conventions that apply to all code Claude writes, and (2) a release-notes generation workflow used once per sprint. How should each be configured?

- A) Put both the conventions and the release-notes workflow in CLAUDE.md, so nothing depends on remembering to invoke a skill.
- B) Put both in skills under `.claude/skills/`, so the context cost is only paid on the sprint when each is actually needed.
- C) Conventions in the project CLAUDE.md; the release-notes workflow in a skill under `.claude/skills/`.
- D) Conventions in a skill; the release-notes workflow in CLAUDE.md so it stays always available.

**Question 22.** A production bug report includes a stack trace pointing to a single function with an obvious off-by-one error. The fix is one line in one file. How should you proceed in Claude Code?

- A) Use direct execution — the change is simple, well-scoped, and already located.
- B) Enter plan mode first to explore the surrounding codebase before committing to an approach.
- C) Spawn an Explore subagent to investigate the module around the flagged function first.
- D) Use `fork_session` to try two candidate one-line fixes in parallel branches.

**Question 23.** You are starting a multi-phase task: first understand how authentication works across a large unfamiliar codebase, then implement a change. The discovery phase will involve reading dozens of files, and you're worried the exploration output will exhaust context before implementation begins. What is the best approach?

- A) Read files in alphabetical order, keeping a structured running log, and run `/compact` after every ten files.
- B) Do the discovery in one session, then `--resume` that same session in a fresh terminal for implementation.
- C) Front-load every planned file read into the first turn so summarization compresses them together later.
- D) Use the Explore subagent for discovery so only a summary returns to the main conversation.

**Question 24.** You've described a data transformation to Claude in prose three separate times, and each implementation handles the edge cases differently. What is the most effective way to communicate the expected behavior?

- A) Write a longer, more precise prose specification that tries to cover every edge case you can think of.
- B) Provide 2–3 concrete input/output examples demonstrating the transformation and its edge cases.
- C) Ask Claude to restate the requirements before implementing, and correct any misunderstanding you hear.
- D) Ask Claude to write out pseudocode first and implement strictly from that pseudocode every time.

**Question 25.** Two hours into a legacy-codebase exploration session, Claude starts describing "typical repository patterns" instead of the actual classes it read earlier, and gives inconsistent answers about code it correctly explained an hour ago. Which practice best counteracts this for ongoing long sessions?

- A) Ask Claude to "focus on the actual code, not typical patterns" each time you notice the drift.
- B) Paste the important files back into the conversation again every time the drift reappears.
- C) Switch to a model with a larger context window, so the same drift simply takes longer to appear.
- D) Have Claude keep a scratchpad file of key findings and reference it for later questions.

**Question 26.** You're mapping a large legacy system. The main session's context is filling with raw file contents from exploration, leaving little room for the architectural reasoning you actually need. What is the best structural fix?

- A) Spawn subagents to investigate specific questions while the main agent coordinates high-level understanding.
- B) Summarize each file immediately after reading it, then delete the original contents from the conversation.
- C) Read only public interfaces and type signatures across the codebase, skipping every implementation body.
- D) Allow longer responses via `max_tokens` and switch to a model with a larger context window during the mapping phase.

**Question 27.** Mid-session, your context is nearly full of verbose discovery output, but you still need to implement the change in this session and want to keep the essential findings. What should you do?

- A) Start a brand-new session and rely on your own memory of what was learned in the old one.
- B) Move the essential findings into the system prompt by hand, then clear the rest of the conversation.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- D) Run `/clear` to reset the context entirely, keeping only CLAUDE.md as persistent state.

**Question 28.** You finished a week-long analysis phase for a large migration and are about to spawn implementation subagents for each module. How should the analysis inform the subagents?

- A) Rely on the subagents automatically inheriting the coordinator session's memory of the completed analysis.
- B) Summarize the key findings and inject the relevant summary into each subagent's initial context.
- C) Have each subagent redo its own analysis of the relevant module from scratch, to guarantee freshness.
- D) Pass the full multi-day session transcript to every subagent so no detail is ever lost.

**Question 29.** Your overnight multi-agent refactoring job occasionally crashes around hour three, and today's restart lost all progress. What design provides crash recovery?

- A) Raise the job's timeout ceiling so the crash-prone three-hour window is less likely to be hit.
- B) Commit code changes to git after each completed module, so finished work survives a crash.
- C) Shrink the job's scope so the whole run finishes before the crash typically occurs.
- D) Have agents export structured state to a known location; the coordinator loads this manifest on resume.

**Question 30.** You concatenated per-module analyses of 30 modules into a single prompt and asked for architecture recommendations. The recommendations consistently cite modules from the beginning and end of the input but ignore the middle third. What is the best mitigation?

- A) Place a key-findings summary first and organize the detail under explicit section headers.
- B) Alphabetize the 30 module sections so the ordering carries no inherent bias.
- C) Add an instruction: "Pay equal attention to every module, especially those in the middle."
- D) Switch to a model with a larger context window so all 30 modules fit more comfortably at once.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 31.** Cost analysis shows that every query — including simple factual ones like "What is the current federal funds rate?" — runs the full search → analysis → synthesis → report pipeline, taking 4+ minutes. What should change?

- A) Cache pipeline outputs so that repeated identical queries return instantly on subsequent requests.
- B) Reduce each subagent's token budget across the board so the full four-stage pipeline completes faster.
- C) Have the coordinator analyze each query's requirements and invoke only the subagents it needs.
- D) Add a fifth "quick answer" subagent and route every incoming query through it first, before the rest.

**Question 32.** The synthesis subagent produces generic, thin output that ignores specific data the search agent found. Logs show the synthesis agent's prompt contains only: "Synthesize the findings on renewable energy storage." What is the root cause?

- A) The synthesis agent's system prompt lacks sufficiently detailed instructions about depth and specificity.
- B) The synthesis agent needs a larger context window in order to see the coordinator's full conversation.
- C) The search agent is returning results in a structured format the synthesis agent cannot parse correctly.
- D) Subagents don't inherit the coordinator's history — the findings must be included in the synthesis prompt.

**Question 33.** A research task involves four independent subtopics. The coordinator currently delegates them one at a time, waiting for each subagent to finish before starting the next, quadrupling latency. How should the coordinator spawn the subagents to run them in parallel?

- A) Wrap the Agent SDK in an external async job queue that launches four separate coordinator processes.
- B) Emit multiple Task tool calls in a single coordinator response, one per subtopic.
- C) Combine all four subtopics into one prompt and hand the whole thing to a single subagent.
- D) Enable streaming on the coordinator's responses so the four subagent calls overlap automatically.

**Question 34.** Your coordinator is configured with `allowedTools: ["WebSearch", "Read"]`. Instead of delegating, it attempts all research itself and never invokes any subagent. What is wrong?

- A) The coordinator's `allowedTools` must include `"Task"` — the tool that spawns subagents.
- B) The subagent definitions are missing `description` fields, so the coordinator cannot see they exist.
- C) The coordinator is running on a model tier too small to support any delegation behavior.
- D) Subagents must first be registered in `.mcp.json` before the coordinator can spawn any of them.

**Question 35.** An engineer proposes letting the search agent pass results directly to the analysis agent, bypassing the coordinator to "cut a hop." What is the main argument against this?

- A) Direct subagent-to-subagent communication doubles token usage through redundant double serialization.
- B) The analysis agent would need the search agent's own tool permissions, violating scoping rules.
- C) It sacrifices the observability, error handling, and information control that coordinator routing provides.
- D) The Agent SDK blocks any direct communication between subagents at the protocol level.

**Question 36.** Completed reports are coherent but often have coverage gaps — for instance, missing major recent developments the search agent never looked for. The pipeline currently makes a single pass. What is the most effective architectural improvement?

- A) Double the number of search results returned per query so more raw material is available up front.
- B) Add a coordinator loop that checks the synthesis for gaps and re-delegates targeted queries.
- C) Add an instruction telling the synthesis agent to write longer, more comprehensive reports overall.
- D) Switch the search agent to a more capable model so its single pass finds everything on the first try.

**Question 37.** You run two search subagents in parallel for broad topics, but their result sets overlap by roughly 60%, wasting tokens and analysis time. What is the best fix?

- A) Partition the research scope at delegation time — assign each agent distinct subtopics or source types.
- B) Merge the two search agents into a single agent that runs one broader query pass, so overlapping results become structurally impossible by design.
- C) Add a deduplication step in the coordinator that discards repeated sources once both agents finish.
- D) Have the second agent wait for the first agent's results and manually avoid its already-used sources.

**Question 38.** Your coordinator prompt gives each subagent a rigid 12-step procedure to follow. Subagents perform well on topics that fit the procedure but fail badly on topics that don't. How should the coordinator's delegation prompts change?

- A) Expand the rigid procedure from 12 steps to 20, covering a wider range of topic types.
- B) Add branching logic to the procedure: "if the topic is technical, do steps 4a–4c instead."
- C) Specify research goals and quality criteria per delegation instead of step-by-step procedures.
- D) Remove all instructions and let each subagent improvise entirely from its own system prompt.

**Question 39.** Your system has two tools: `analyze_content` ("Analyzes content and returns insights") and `analyze_document` ("Analyzes documents and returns findings"). Agents misroute between them about 30% of the time. What is the most effective first fix?

- A) Add a system prompt rule: "When in doubt between the two, prefer analyze_document."
- B) Remove one of the two tools entirely and route all analysis through the one that remains.
- C) Intercept and silently correct misrouted calls with a `PostToolUse` hook in the coordinator.
- D) Rename the tools for their distinct purposes and rewrite each description with inputs, outputs, and when to use it.

**Question 40.** `analyze_document` accepts a `mode` parameter that switches between extraction, summarization, and claim verification. Agents frequently pass the wrong mode and get output they didn't expect. What is the best long-term redesign to eliminate this failure class?

- A) Split it into three purpose-specific tools, each with its own defined input/output contract.
- B) Make `mode` a strict enum type documented in the tool's schema, with inline examples for each of the three values, so misuse is easy to spot in code review.
- C) Default `mode` to summarization, the most common case, so a wrong mode matters less often.
- D) Have the tool infer the intended mode itself from the shape of the input it receives.

**Question 41.** The synthesis agent's toolset was copy-pasted from the search agent's config and includes `web_search`. You discover it performing new searches mid-synthesis and weaving unvetted, uncited claims into reports. What is the right fix?

- A) Add a system prompt rule telling the synthesis agent to only search when strictly necessary.
- B) Remove search tools from the synthesis agent so it works only from the findings it is given.
- C) Add a stricter word-count limit on synthesis output so there's less room for the model to wander into unsupported claims.
- D) Add a post-hoc citation checker that flags any uncited claims in the finished report.

**Question 42.** The document analysis agent begins every task with 8–10 exploratory `list_documents` and `search_library` calls just to learn what's in the research library. How can you eliminate this overhead?

- A) Cache the exploratory `list_documents` and `search_library` results for 24 hours so repeats are cheap.
- B) Paste the full library listing into the agent's system prompt and update it whenever documents change.
- C) Raise the agent's tool-call budget so the exploratory calls complete faster overall.
- D) Expose the document catalog as an MCP resource the agent can see without exploratory calls.

**Question 43.** The document analysis agent has a generic `fetch_url` tool and occasionally pulls arbitrary blog pages instead of documents from your vetted research library. What is the best fix?

- A) Add a system prompt instruction listing which domains are acceptable for the agent to fetch from.
- B) Log every fetched URL and have someone review the log weekly for policy violations.
- C) Replace `fetch_url` with a `load_document` tool that validates URLs against the vetted library.
- D) Reduce the agent's temperature so it makes more conservative choices about what to fetch.

**Question 44.** Final reports contain claims with no traceable source. Investigation shows the analysis agent summarizes findings into prose, and by the time synthesis runs, the source associations are gone. What is the fix?

- A) Require subagents to output structured claim-source mappings that synthesis must preserve and merge.
- B) Have the report agent add citations at the end by running a fresh search for a plausible, topically-matching source to back each claim already in the draft.
- C) Append a bibliography listing every consulted source to the end of each generated report.
- D) Instruct the synthesis agent to only include claims it can still remember a source for.

**Question 45.** Two credible sources report the market size for the same year as $4.2B and $6.8B. The synthesis agent currently picks one value, seemingly at random. What should it do instead?

- A) Prefer whichever source was published more recently, and simply discard the other value.
- B) Present both values, annotated as a conflict, with source attribution and methodological context.
- C) Report the midpoint of the two values, with a footnote noting where each number came from.
- D) Request a third source from the coordinator and keep only the two values that happen to agree.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** Your review job asks Claude Code for findings and then regex-parses its prose output to post inline PR comments. The parser breaks almost weekly when the output format drifts. What is the robust fix?

- A) Harden the regex with more permissive patterns and fallback rules for known format variants.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure.
- C) Add a system prompt instruction: "Always use the exact output format below, never deviate from it."
- D) Post Claude's entire raw output as a single PR comment, so no parsing is needed at all.

**Question 47.** After a developer pushes new commits to a PR, your pipeline re-runs the review, and the bot posts duplicate comments for issues it already flagged and that remain unfixed. How should re-reviews be designed?

- A) Review only the files changed in the newest commits, to keep each re-review scope minimal.
- B) Delete all previous bot comments before every re-review and post a fresh, structured full set again.
- C) Skip re-reviews entirely — treat one review per pull request as sufficient going forward.
- D) Include prior findings in context and instruct Claude to post only new or still-unaddressed issues.

**Question 48.** Your nightly test-generation job produces mostly low-value tests — trivial getter checks and tests of framework behavior — and never uses the fixture factories your team built. What is the most effective fix?

- A) Document testing standards, valuable-test criteria, and available fixture factories in CLAUDE.md.
- B) Generate three times as many tests as needed and have a second job filter the low-value ones.
- C) Post-process the generated tests to inject fixture-factory imports into them automatically.
- D) Restrict generation to files under 50% coverage, on the reasoning that any test there adds value.

**Question 49.** Your review bot flags too many trivial style nitpicks. You added "Be conservative — only report issues you are highly confident about" to the prompt, but the false positive rate barely moved. What should you do instead?

- A) Strengthen the wording further, to "Only report issues you are 100% certain about."
- B) Define categorical criteria in the system prompt: report bugs and security issues; skip minor style and local naming patterns.
- C) Add a second reviewer model and only post findings that both models agree on.
- D) Have the bot self-assign a confidence score per finding and filter anything below a threshold.

**Question 50.** False-positive analysis shows the "performance" review category is 70% false positives while all other categories are under 10%. Developers have started ignoring all bot findings, including accurate security ones. What is the best immediate action?

- A) Keep all categories enabled, but add a disclaimer that performance findings are still experimental.
- B) Lower the displayed severity of performance findings so they read as less alarming to reviewers.
- C) Temporarily disable the performance category while improving its prompts separately.
- D) Batch performance findings into a weekly digest instead of posting them directly on PRs.

**Question 51.** The same type of issue gets labeled "critical" in one PR and "minor" in another. Severity drives your merge-blocking logic, so inconsistency is breaking the pipeline's usefulness. What is the most effective fix?

- A) Define explicit severity criteria in the system prompt with a concrete code example at each level.
- B) Remove severity from findings entirely and block merges on the presence of any finding at all.
- C) Ask the model to double-check its own severity label before finalizing each finding.
- D) Map severity directly from the finding category — all security findings critical, all style findings minor, all performance findings automatically medium.

**Question 52.** Despite detailed formatting instructions, review findings arrive in inconsistent shapes — sometimes missing the file location, sometimes merging several issues into one paragraph. What is the most effective technique to get consistent, actionable findings?

- A) Repeat the same formatting instructions at both the start and the end of the prompt.
- B) Allow more `max_tokens` so the model has room to complete every required field.
- C) Post-process the output with a second Claude call that reformats it against the same schema.
- D) Add few-shot examples demonstrating the exact desired format for several finding types.

**Question 53.** Your codebase intentionally uses patterns that the reviewer keeps flagging — like empty catch blocks (with explanatory comments) inside retry helpers. You can't enumerate every acceptable pattern in the prompt. What approach reduces these false positives while still catching genuine issues?

- A) Add few-shot examples contrasting acceptable intentional patterns with genuine issues.
- B) Suppress every finding that involves a catch block anywhere in the codebase, without exception.
- C) Add inline "claude-ignore" comments at every site where the pattern is intentional.
- D) Maintain an exhaustive, structured allowlist file of acceptable patterns and check each finding against it.

**Question 54.** You're building the review bot on the Agent SDK, and it returns findings as JSON inside its text response. About 5% of runs produce malformed JSON that crashes the comment poster. What is the most reliable fix?

- A) Wrap the JSON parse in a try/catch and automatically re-request with "valid JSON only" on failure.
- B) Ask for YAML output instead of JSON, since YAML tolerates formatting drift more gracefully.
- C) Define a `report_findings` tool with your findings schema and read from the `tool_use` block.
- D) Add a JSON-repair library that fixes trailing commas and unquoted keys before parsing.

**Question 55.** Your review bot has two tools — `report_findings` and `approve_pr` — but sometimes it replies with conversational text like "The code looks good to me!" and calls neither. Downstream automation requires a tool call every time. What is the fix?

- A) Force `tool_choice: {"type": "tool", "name": "report_findings"}` so a tool call always happens.
- B) Set `tool_choice: "any"` so the model must call a tool but can choose the appropriate one.
- C) Add a system prompt instruction telling the bot to always call one of the two tools.
- D) Parse conversational replies and infer an approval decision from positive sentiment in the wording.

**Question 56.** Since switching to tool_use with a strict JSON schema, review outputs always parse — but some findings reference line numbers pointing at the wrong lines, and severity labels occasionally contradict the description text. What should you conclude?

- A) The schema needs stricter types; a bounded integer range on line numbers will fix the misalignment.
- B) The model is being truncated mid-generation; increasing `max_tokens` will fix both problems at once.
- C) Tool use is unsuitable for code review output; revert to prose findings with human triage instead.
- D) Schemas eliminate syntax errors, not semantic ones; add semantic validation on top.

**Question 57.** Your semantic validator rejects a finding because it references a file that isn't part of the PR diff. What is the most effective retry design?

- A) Send a follow-up with the original context, the failed output, and the specific validation error.
- B) Retry with an identical prompt, since validation failures like this are usually just transient.
- C) Silently drop the invalid finding and continue posting only the ones that pass validation.
- D) Regenerate the entire review from scratch, this time with a different sampling seed.

**Question 58.** Developers dismiss about 40% of the bot's findings, but you have no systematic way to learn which kinds of code constructs trigger the bad findings. What schema change enables this analysis?

- A) Add a free-text `notes` field to the schema where the model can explain its reasoning about each finding at length.
- B) Add a `reviewer_id` field so you can compare dismissal rates across different model versions.
- C) Add a `detected_pattern` field capturing which code construct triggered each finding.
- D) Add a `confidence` field and simply assume dismissed findings were the ones with low confidence.

**Question 59.** An engineer proposes moving your agentic "generate tests, run them, fix failures, repeat" workflow to the Message Batches API for the 50% cost savings. Why won't this work?

- A) Batch requests cannot include a system prompt at all, which this workflow depends on.
- B) The Batch API can't execute tools mid-request — the generate-run-fix loop needs multi-turn tool calling.
- C) The Batch API's 24-hour completion window is too slow for an overnight job of this size.
- D) The Batch API caps each request at a context size too small to hold the generated test files.

**Question 60.** Your pipeline has the same Claude Code session generate a feature and then immediately review its own changes. The self-reviews rarely find problems, yet human reviewers regularly catch real bugs in the same code. What is the most effective fix?

- A) Add "review your own work with fresh eyes and maximum skepticism" to the self-review prompt.
- B) Enable extended thinking during the self-review step so the model reasons more deeply about its own code.
- C) Have the same session review the code three separate times and merge the resulting findings.
- D) Have a second, independent Claude instance — without the generator's context — perform the review.

---
# Answer Key — Practice Exam 6

**Quick key:** 1-C, 2-D, 3-B, 4-A, 5-D, 6-B, 7-C, 8-B, 9-D, 10-C, 11-A, 12-B, 13-D, 14-A, 15-C, 16-B, 17-D, 18-A, 19-C, 20-B, 21-C, 22-A, 23-D, 24-B, 25-D, 26-A, 27-C, 28-B, 29-D, 30-A, 31-C, 32-D, 33-B, 34-A, 35-C, 36-B, 37-A, 38-C, 39-D, 40-A, 41-B, 42-D, 43-C, 44-A, 45-B, 46-B, 47-D, 48-A, 49-B, 50-C, 51-A, 52-D, 53-A, 54-C, 55-B, 56-D, 57-A, 58-C, 59-B, 60-D

---

**1. C** — The agentic loop must key off `stop_reason`: continue while it is `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Parsing natural-language signals (A) is exactly the anti-pattern producing the observed failures — text can look terminal while a tool call is pending, and no amount of fuzzy matching fixes that. Iteration caps (B) are a safety backstop, not a primary stopping mechanism, and truncate legitimate long cases. D inverts the semantics: absence of text says nothing definitive about completion.

**2. D** — Tool results must be appended to the conversation history as a `tool_result` block referencing the `tool_use` ID, then the whole conversation is sent back so the model can incorporate the result into its next reasoning step. A defers confirmation to ticket closure, leaving the agent unaware the refund happened during the live conversation. B misuses the system prompt for turn-level data via a hook that has no such role. C destroys conversational state mid-task and is unnecessary here.

**3. B** — A `PostToolUse` hook deterministically normalizes heterogeneous formats before the model ever sees them, removing the error class entirely. Prompt instructions (A) rely on probabilistic per-turn conversions and will still fail occasionally. C bundles a real fix behind an organizationally impractical, out-of-your-control migration. D validates the agent's final answer after the bad data has already influenced its reasoning, rather than preventing the miscomparison.

**4. A** — A business rule with financial consequences needs deterministic enforcement: intercept the tool call, block amounts over $500, and redirect to escalation. Prompt salience (B), few-shot examples (C), and a self-confirmation instruction (D) all still rely on the model choosing to comply — the observed 2% failure rate is precisely why prompt-only enforcement is insufficient here.

**5. D** — The recommended pattern is decomposing multi-concern requests into distinct items, investigating each in parallel with shared context, then synthesizing one unified resolution. A pushes the multi-issue problem onto the customer instead of solving it. B escalates cases the agent could resolve, hurting first-contact resolution. C discards the shared context (customer identity, verification) that the concerns have in common.

**6. B** — Humans without transcript access need a structured handoff: customer ID, root cause, amount, recommended action — everything needed to act immediately. A raw transcript (A) forces the human to reconstruct the case anyway, just from more text. C is even thinner than the transcript, omitting the case analysis entirely. D conveys mood, not the facts needed to resolve the dispute.

**7. C** — "Refunds only to the verified original payment method" is a hard compliance rule where any violation has financial/fraud consequences — the case for programmatic enforcement (a hook gating `process_refund`). Tone (A), conciseness (B), and offering alternatives first (D) are behavioral guidance where occasional imperfection is acceptable, so prompt instructions are appropriate.

**8. B** — This workload is explicitly high-ambiguity: the right tools and their order genuinely vary per case, and intermediate results (e.g., what `lookup_order` reveals) change what should happen next — the core argument for model-driven decision-making, and a fixed script also wastes calls on cases that don't need them. A's "always cheaper" claim is false — model-driven selection spends reasoning tokens a script would skip. C invents a connection: session resumption doesn't depend on tool ordering. D is false — a scripted sequence can be given any context you choose to feed it.

**9. D** — Structured error metadata (`errorCategory`, `isRetryable`, description) gives the agent what it needs to retry transient failures and stop retrying non-retryable ones. Blanket retry (A) wastes calls on business errors and hides the retry decision from the agent entirely. B asks the model to guess what the tool already knows about itself. C reduces one error type's frequency without fixing the underlying decision-making problem.

**10. C** — Business-rule violations should come back as structured errors with `retriable: false` and a customer-friendly explanation so the agent can communicate accurately and pivot to alternatives (store credit). A gives the agent nothing to reason with beyond a bare status code. B silently misrepresents a failure as success — the agent may tell the customer the refund happened. D leaks internals and buries the relevant fact (the policy window) in noise.

**11. A** — "No orders" is a valid empty result of a successful query, not a failure; conflating the two causes exactly the observed misbehavior (apologizing, retrying). Errors should be reserved for access failures. B patches the symptom with prompt text while the underlying contract stays broken. C hides real signal behind a hook instead of fixing what the tool returns. D invents a spurious recovery path for what isn't actually an error.

**12. B** — Keyword-sensitive system prompt instructions can create unintended tool associations that override even good tool descriptions — "any customer question about their purchases" is sweeping policy questions into `lookup_order`. A and D modify the tool when the tool description isn't the problem. C adds token overhead to counteract an instruction you can simply fix at the source.

**13. D** — Growing from 4 to 18 tools on one agent increases decision complexity and degrades tool selection reliability; the fix is scoped tool access per role, or splitting into specialized agents. A and B describe limits that don't exist in the MCP protocol or typical context budgets. C misdescribes how tool use works — agents don't call every available tool per conversation.

**14. A** — Forced tool selection (`tool_choice: {"type": "tool", "name": "classify_request"}`) on the first request is the only option that *guarantees* that specific tool runs first; later turns then proceed normally. B and D are probabilistic prompt-level nudges. C (`"any"`) guarantees *some* tool call, but not which one — the agent could call `get_customer` first and still satisfy it.

**15. C** — Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block that rides outside the summarized history is the recommended defense against progressive summarization degrading precise values into vague ones ("around $80"). A only delays the loss and doesn't address why numeric precision degrades under summarization. B works but adds cost and latency on every turn for data that isn't changing. D pushes the system's memory problem onto the customer.

**16. B** — `~/.claude/CLAUDE.md` is user-level configuration: it applies to your account only and never travels through version control. Team-wide standards belong in a project-level CLAUDE.md committed to the repo. A misstates what `/memory` does (it inspects loaded memory; it doesn't "activate" anything). C — project CLAUDE.md loads without imports. D invents a failure mode.

**17. D** — `@import` keeps CLAUDE.md modular: each package's CLAUDE.md pulls in only the relevant shared standards files, and package maintainers with domain knowledge own the package-specific additions. A creates six diverging copies that will drift apart. B still loads all 900 lines every session — a table of contents doesn't reduce what's loaded. C makes standards invisible to Claude by default, relying on developers to supply them ad hoc.

**18. A** — Inconsistent behavior across sessions is the classic symptom of different memory files being loaded in different sessions; `/memory` shows exactly which files are in effect, so diagnose before rewriting anything. B and D change content before you know whether content is the problem. C addresses context pressure, not configuration loading.

**19. C** — `context: fork` runs the skill in an isolated sub-agent context so its verbose output never enters (pollutes) the main conversation — only the useful summary returns. A reduces volume but the output still lands in the main context. B makes it worse: always-loaded verbosity on every session. D restricts capability, not where the output ends up.

**20. B** — `allowed-tools` in the skill frontmatter is the enforcement mechanism: restrict the skill to file-creation operations and Bash simply isn't available during execution. A is prompt-based and probabilistic — the failure already happened despite the skill's instructions. C mitigates damage rather than preventing it. D is false — slash commands don't disable tool execution.

**21. C** — Universal, always-applicable standards belong in CLAUDE.md (loaded every session); task-specific workflows used occasionally belong in skills (loaded on demand). A pays the release-notes workflow's context cost in every session even on the 51 weeks it isn't needed. B means conventions only apply when someone remembers to invoke a skill for them. D is backwards on both counts.

**22. A** — A single-file, single-line fix with a stack trace pointing at the location is the textbook case for direct execution; plan mode (B), exploration subagents (C), and session forking (D) all add overhead with no decision-making or architectural payoff for a change this well-scoped.

**23. D** — The Explore subagent is designed for exactly this: verbose discovery runs in an isolated context and returns a summary, preserving the main conversation's context for the implementation phase. A still floods the main context between compactions. B — resuming the same session carries its full exploration context into the implementation phase; nothing is isolated. C changes when the flooding happens, not whether it happens.

**24. B** — Concrete input/output examples are the most effective way to communicate expected transformations when prose is being interpreted inconsistently — they pin down the edge cases directly. A produces more prose subject to the same interpretation problem. C surfaces misunderstandings but doesn't pin down edge-case behavior the way examples do. D pins down a process (write pseudocode, then implement it) but the pseudocode itself is still prose Claude has to interpret, so the edge cases it silently resolves can still vary between the pseudocode and the final code.

**25. D** — Context degradation in extended sessions (drifting to "typical patterns" instead of discovered specifics) is counteracted by persisting key findings to a scratchpad file and referencing it for subsequent questions — the findings survive outside degrading conversational context. A asks the model to fix a context problem with an instruction, repeated every time it recurs. B repeatedly re-spends context and accelerates the problem. C delays symptoms without adding any persistence.

**26. A** — Delegating specific investigation questions to subagents isolates the verbose file-dump output in their contexts, while the main agent keeps its context for high-level coordination. B — the raw contents have already consumed context by the time they're summarized, and prior turns can't be selectively removed mid-session. C sacrifices the implementation-level understanding a legacy mapping needs. D targets the wrong lever twice over: `max_tokens` governs response length, not context accumulated from reading files, and a larger context window only postpones the same pressure rather than relieving it structurally.

**27. C** — `/compact` summarizes the conversation to reduce context usage while preserving key information — the right mid-session relief valve when you need to keep working. A discards the findings (Claude has no cross-session memory of them). B isn't an available mid-session operation — the system prompt isn't an editable store for conversation findings. D (`/clear`) resets the conversation and loses the findings entirely.

**28. B** — The reliable pattern is summarizing key findings from the completed phase and injecting the relevant summary into each subagent's initial context. A fails because subagents do not inherit parent context automatically. C re-spends a week of analysis per module. D floods each subagent's context with a mostly-irrelevant transcript, inviting lost-in-the-middle problems.

**29. D** — Structured state persistence is the crash-recovery pattern: each agent exports completed work and key findings to a known location; on resume the coordinator loads the manifest and injects state into agent prompts, resuming rather than restarting. A and C reduce crash odds but don't recover from one when it happens anyway. B preserves code edits but loses the agents' analysis state, task assignments, and findings — the coordinator still can't resume intelligently.

**30. A** — This is the lost-in-the-middle effect: models reliably process the beginning and end of long inputs but may omit middle sections. The mitigation is a key-findings summary up front plus explicit section headers organizing the detail. B changes ordering without addressing the underlying position effect. C — instructions alone don't fix attention position biases. D — the effect persists even in larger windows, just at larger scale.

**31. C** — The coordinator should analyze query requirements and dynamically select which subagents to invoke; simple factual queries shouldn't traverse the full pipeline. A only helps on repeated queries, not the first (or unique) instance of a simple one. B makes every stage worse instead of skipping stages that aren't needed. D adds a fifth mandatory stage to a pipeline whose problem is mandatory stages.

**32. D** — Subagents operate with isolated context: they do not inherit the coordinator's conversation history. The synthesis prompt must include the actual search results and analysis outputs. A would deepen prose style but can't conjure data the agent never received. B misunderstands isolation — window size is irrelevant if the content is never passed in the first place. C is contradicted by the logs: nothing was passed at all, structured or otherwise.

**33. B** — Parallel subagents are spawned by emitting multiple Task tool calls in a single coordinator response, rather than one per turn. A bolts external infrastructure onto a problem the SDK pattern already solves natively. C serializes the work inside one context and loses the parallelism entirely. D — streaming affects token delivery, not tool-call concurrency.

**34. A** — The Task tool is the mechanism for spawning subagents; if `"Task"` isn't in the coordinator's `allowedTools`, it cannot delegate and will attempt the work itself. B affects selection quality among subagents, not the total inability to spawn any. C and D describe requirements that don't exist in the SDK.

**35. C** — Hub-and-spoke routing through the coordinator is what provides observability, consistent error handling, and controlled information flow; a direct side channel sacrifices all three at once. A invents a token penalty that doesn't generally hold. B is a side detail, not the main architectural argument against the proposal. D is false — you could build it, it's just a bad idea architecturally.

**36. B** — Coverage gaps are addressed with an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient. A adds volume to the same single pass, not targeted coverage of what was missed. C asks for length — the missing material was never gathered in the first place. D still makes a single pass with no gap-checking step at all.

**37. A** — Partitioning research scope — assigning each agent distinct subtopics or source types — prevents duplication at the source, so neither agent spends tokens rediscovering what the other already found. C deduplicates only after the tokens and analysis time are already spent. B gives up the parallelism that motivated running two agents in the first place. D serializes the agents, also defeating the original parallelism.

**38. C** — Coordinator prompts should specify research goals and quality criteria rather than step-by-step procedures, enabling subagents to adapt their approach to each topic. A and B double down on rigid proceduralism — there will always be topics outside whatever script you write. D removes direction entirely; goals and quality bars are still needed even without fixed steps.

**39. D** — Tool descriptions are the primary mechanism for tool selection; near-identical names and descriptions cause misrouting. Renaming to purpose-specific names and rewriting descriptions (purpose, inputs, outputs, when-to-use-vs-the-other) fixes the root cause. A papers over ambiguity with a default that will be wrong some of the time. B may discard functionality the team actually needs. C corrects symptoms downstream with a hook and needs its own routing logic — the very thing that's broken.

**40. A** — A generic tool with mode switches invites wrong-mode calls; splitting into purpose-specific tools with clear contracts makes selection explicit and eliminates the failure class entirely. B documents the confusion but keeps the single overloaded entry point in place. C substitutes a silent wrong behavior for a visible error. D makes behavior unpredictable and undebuggable by hiding the decision inside the tool.

**41. B** — Agents with tools outside their specialization tend to misuse them; the synthesis agent's job is to work from provided findings, so search tools should be removed from its set (scoped tool access). A is probabilistic and the misuse is already happening despite similar instincts being assumed by default. C constrains output length, not the ability to call `web_search` mid-synthesis — the agent can still weave in an unvetted claim within a shorter word count. D flags damage after publication instead of preventing it from entering the report.

**42. D** — MCP resources exist to expose content catalogs — giving agents visibility into available data without exploratory tool calls. A makes the waste cheaper on repeat runs, not gone on the first one. B is a manual, drift-prone copy of what resources provide natively and automatically. C speeds up the overhead instead of eliminating the extra calls.

**43. C** — Replacing the generic `fetch_url` with a constrained `load_document` that validates URLs against the vetted library makes the boundary structural rather than behavioral. A relies on prompt compliance the agent has already shown it can ignore. B detects violations only after they've contaminated the research. D doesn't address capability at all, only sampling behavior.

**44. A** — Attribution survives only if subagents emit structured claim-source mappings (claim, source, excerpt) and the synthesis agent is required to preserve and merge them; prose summarization is where provenance dies. B fabricates citations after the fact — worse than none at all. C lists sources without linking any specific claim to them. D relies on memory of information that was already compressed away during summarization.

**45. B** — Conflicting statistics from credible sources should be presented with explicit conflict annotation, source attribution, and methodological context — not resolved arbitrarily. A assumes recency explains the difference, when it may be methodology or scope instead. C invents a number no source actually reported. D outsources the judgment to a majority vote that may simply share a flawed methodology, and discards a credible value either way.

**46. B** — `--output-format json` with `--json-schema` produces machine-parseable, schema-conforming output — the supported mechanism for structured findings in CI. A and C keep betting on the same format stability that prose output has already failed to provide. D abandons the inline-comment requirement rather than meeting it.

**47. D** — The documented pattern for re-reviews: include prior findings in context and instruct Claude to report only new or still-unaddressed issues, avoiding duplicate comments. A misses issues that new commits introduce in interaction with unchanged files elsewhere in the diff. B recreates comment noise on every push and destroys any existing discussion threads. C leaves everything after the first push unreviewed.

**48. A** — CLAUDE.md is the mechanism for giving CI-invoked Claude Code project context: testing standards, what makes a test valuable, and which fixtures exist. Without it the generator can't know your conventions no matter how it's invoked. B generates waste and then filters it, paying the generation cost twice. C injects imports into tests that still don't use the factories meaningfully. D narrows the scope of generation without improving the quality of what's generated within it.

**49. B** — General instructions like "be conservative" or "high-confidence only" demonstrably fail to improve precision; explicit categorical criteria — report these types, skip those types — are what work. A is more of the same failed approach, just with stronger wording. D relies on self-reported confidence, which is poorly calibrated for this kind of judgment. C doubles cost and still lacks defined criteria for either reviewer to apply.

**50. C** — One high-false-positive category undermines trust in all categories. Temporarily disabling the 70%-FP performance category restores signal quality immediately while you improve its prompts offline. A, B, and D all keep the same noise flowing in some form, and trust continues eroding in the meantime.

**51. A** — Consistent classification comes from explicit severity criteria anchored with concrete code examples at each level. B makes every nitpick merge-blocking regardless of severity. C is self-review with no external standard to check against. D is too coarse — not all security findings carry critical impact, and category isn't the same thing as severity.

**52. D** — When detailed instructions alone produce inconsistent output, few-shot examples demonstrating the exact desired format (location, issue, severity, suggested fix) are the most effective technique for consistency. A repeats what already isn't working, just in two places instead of one. B addresses truncation, which isn't the symptom being described. C adds cost and a second chance for drift in the reformatting call itself.

**53. A** — Few-shot examples contrasting acceptable intentional patterns with genuine issues let the model generalize the judgment to novel cases — exactly what an enumerated allowlist (D) can't do for patterns nobody has written down yet. B suppresses real bugs involving catch blocks along with the intentional ones. C requires annotating the whole codebase and doesn't help with new code going forward.

**54. C** — Tool use with a JSON schema is the most reliable path to structured output: the `report_findings` tool's input schema guarantees well-formed structure, eliminating the JSON-in-text syntax errors at the source. A and D are recovery layers for a problem you can eliminate outright. B trades one fragile text format for another that is only somewhat more forgiving.

**55. B** — `tool_choice: "any"` guarantees the model calls *a* tool while leaving it free to pick the appropriate one (`report_findings` vs `approve_pr`). A forces every response through `report_findings`, breaking legitimate approvals. C is probabilistic — the failure already occurs despite instructions along these lines. D is sentiment-parsing fragility replacing a structural guarantee.

**56. D** — Strict schemas via tool use eliminate *syntax* errors but not *semantic* errors — wrong line numbers and contradictory severities are semantically wrong, schema-valid outputs. The fix is semantic validation layered on top (e.g., verifying line references against the diff, cross-checking severity against criteria). A — a bounded integer range can't know which specific line is correct, only that it's in range. B misdiagnoses the cause; truncated output would fail schema validation outright rather than parse cleanly. C throws away the syntax guarantee the schema already earned you, without fixing the semantic gap.

**57. A** — Retry-with-error-feedback: include the original context, the failed output, and the specific validation error ("finding 3 references src/util.ts, which is not in this diff") so the model can self-correct. An identical retry (B) has no new information and will likely fail identically. C silently loses a possibly-real finding that referenced the wrong file by mistake. D discards all the valid findings along with the one invalid one.

**58. C** — A `detected_pattern` field records which code construct triggered each finding, enabling systematic aggregation of dismissals by pattern — the feedback loop you're missing. A gives unstructured text you can't aggregate at scale. B varies the wrong dimension for this question. D assumes the very correlation you're trying to measure instead of measuring it.

**59. B** — The Batch API does not support multi-turn tool calling within a request: it cannot pause mid-request, execute your test-runner tool, and feed results back to the model. An iterative generate-run-fix loop is inherently multi-turn tool use. C is backwards — overnight jobs are exactly the Batch API's sweet spot. A and D describe restrictions that don't actually exist on the API.

**60. D** — A model reviewing its own generation retains the reasoning context that produced the code, making it unlikely to question its own decisions. An independent instance without that context is more effective at catching subtle issues the generator talked itself past. A and B try to prompt or think around a structural bias instead of removing it. C repeats the same biased review three times instead of introducing a genuinely independent check.

---

*End of Practice Exam 6.*
