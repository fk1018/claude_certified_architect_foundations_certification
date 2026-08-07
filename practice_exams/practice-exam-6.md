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

- A) Expand the phrase list and add fuzzy matching to catch paraphrased terminal expressions.
- B) Cap the loop at 10 iterations, since most support cases resolve in fewer turns.
- C) Continue the loop while `stop_reason` is `"tool_use"`, executing tools; terminate on `"end_turn"`.
- D) Terminate whenever a response arrives with no text content, treating tool-only turns as complete.

**Question 2.** Your agent calls `process_refund` and your code executes the refund successfully. What must happen next so the agent can correctly continue the conversation?

- A) Store the confirmation in your database and summarize all tool activity in the final customer response.
- B) Inject the refund confirmation into the system prompt so it persists across later turns.
- C) Start a new conversation seeded with a summary of prior turns plus the refund result.
- D) Append a `tool_result` block (with the `tool_use` ID) in a user message and resend the conversation.

**Question 3.** Your MCP tools come from different backend teams: `get_customer` returns ISO 8601 dates, `lookup_order` returns Unix timestamps, and order statuses are numeric codes in one tool but strings in another. The agent occasionally miscompares dates and misreads statuses when reasoning across tools. What is the most reliable fix?

- A) Document each tool's formats in the system prompt with conversion instructions.
- B) Normalize dates, timestamps, and status codes in a `PostToolUse` hook before the model sees them.
- C) Ask the backend teams to migrate their APIs to one shared format standard.
- D) Validate the agent's final answer for date and status errors at conversation end.

**Question 4.** Company policy requires human approval for any refund over $500. Your system prompt states this rule prominently, but production logs show that about 2% of refunds above $500 are still processed autonomously. What should you do?

- A) Intercept `process_refund` calls with a hook that blocks amounts over $500 and redirects to escalation.
- B) Move the rule to the top of the system prompt and repeat it before the tool definitions.
- C) Add few-shot examples of the agent escalating refunds of $501, $750, and $1,200.
- D) Lower the temperature so the agent follows system prompt instructions more consistently.

**Question 5.** A customer writes one message reporting a damaged item, a duplicate charge on their card, and an address change for an upcoming shipment. The agent resolves the damaged item and ends the conversation without addressing the other two concerns. What is the best design change?

- A) Detect multi-issue messages with a classifier and ask the customer to file separate tickets.
- B) Route messages containing more than one concern to `escalate_to_human` for manual handling.
- C) Handle each concern in its own fresh session so every issue gets a clean context window.
- D) Decompose the message into distinct items, investigate each with shared context, and synthesize one resolution.

**Question 6.** When the agent escalates a billing dispute to a human agent, the human team works in a separate system with no access to the AI conversation transcript. Human agents report spending 10+ minutes reconstructing each case. What should the escalation include?

- A) The complete raw conversation transcript exported as text for the human to read.
- B) A structured summary: customer ID, root cause, disputed amount, and recommended action.
- C) The customer ID plus a profile link, keeping the handoff lightweight for the queue.
- D) A sentiment analysis of the conversation showing the customer's frustration level.

**Question 7.** You are deciding which agent behaviors need programmatic enforcement (hooks) versus system-prompt guidance. Which requirement is the strongest candidate for a hook rather than prompt instructions?

- A) Maintaining an empathetic, professional tone with frustrated customers.
- B) Keeping responses concise and free of unnecessary technical jargon.
- C) Ensuring refunds are only issued to the verified original payment method.
- D) Offering troubleshooting alternatives before proposing any refund.

**Question 8.** A product manager proposes replacing the agent's reasoning with a fixed sequence — always call `get_customer`, then `lookup_order`, then either resolve or refund — arguing it will make behavior predictable. Why is model-driven tool selection the better fit for this workload?

- A) Model-driven selection is always cheaper, since the model skips the reasoning tokens needed to follow a script.
- B) Support requests vary too much for one sequence: the tools needed differ per case, and intermediate results change what should happen next.
- C) A fixed sequence would break session resumption, which requires model-chosen tool ordering.
- D) Decision trees cannot access conversation history, so a fixed sequence could not use context from earlier turns.

**Question 9.** Every failure from `process_refund` currently returns the same response: `"Operation failed"`. Logs show the agent retrying policy-violation failures repeatedly (which will never succeed) and giving up immediately on transient gateway timeouts (which would succeed on retry). What is the best fix?

- A) Wrap all tool calls in an automatic retry-three-times policy at the application layer.
- B) Tell the agent in the system prompt to judge retryability from conversation context.
- C) Increase the payment gateway timeout so transient failures become rare.
- D) Return structured errors with an `errorCategory`, an `isRetryable` boolean, and a description.

**Question 10.** A customer requests a refund for an order purchased 47 days ago; policy allows refunds within 30 days. What should `process_refund` return so the agent handles this well?

- A) A standard HTTP 400 status code with no body, letting the agent infer the cause from its own request.
- B) A success response with an empty body, so the agent avoids alarming the customer with error language.
- C) A business-category error with `retriable: false`, a customer-friendly explanation, and an alternative to offer.
- D) An error carrying the full server-side stack trace so the agent has maximum detail to reason with.

**Question 11.** When a customer has no orders on file, `lookup_order` currently returns an error, and the agent responds by apologizing for "technical difficulties" and retrying the lookup. What should change?

- A) Return a successful empty result set (with a note like "no orders found"), reserving errors for access failures.
- B) Add a system prompt note that this error usually means the customer has no orders.
- C) Suppress the error in a hook and instruct the agent to end the conversation gracefully.
- D) Have the agent call `get_customer` again first, in case the customer ID was wrong.

**Question 12.** Your tool descriptions are detailed and well-differentiated, yet the agent calls `lookup_order` even for general return-policy questions where no order is involved. You find this line in the system prompt: "Use lookup_order to help with any customer question about their purchases." What is the most likely fix?

- A) Rewrite the `lookup_order` description to say it must not be used for policy questions.
- B) Reword or remove the keyword-sensitive prompt line that is overriding the tool descriptions.
- C) Add few-shot examples of policy questions being answered without any tool calls.
- D) Rename the tool `lookup_order_by_id` so the model understands an ID is required.

**Question 13.** The support team wants to expand the agent from its current 4 tools to 18 by adding loyalty-program, marketing-preferences, subscription, and gift-card tools — all attached to the single resolution agent. What is the primary risk?

- A) The MCP protocol limits each server to 10 tools, so the configuration will fail at connection time.
- B) The added tool schemas will exceed the context window before any conversation begins.
- C) The agent will slow down because it must call every available tool at least once per conversation.
- D) Tool selection reliability degrades as the tool count grows, increasing misrouting.

**Question 14.** Compliance requires that every conversation begin with a call to a `classify_request` tool before any other tool runs, with no exceptions. What is the most reliable implementation?

- A) Set `tool_choice: {"type": "tool", "name": "classify_request"}` on the first request, then normal tool choice afterward.
- B) State in the system prompt that `classify_request` is mandatory and must always come first.
- C) Set `tool_choice: "any"` on the first request so a tool call is guaranteed before any response.
- D) Add few-shot examples showing `classify_request` being called first in several conversation types.

**Question 15.** In long billing-dispute conversations, your context management summarizes older turns. After summarization, the agent starts misstating specifics — quoting "around $80" for a refund the customer was promised at exactly $83.47. What is the best fix?

- A) Increase the summary length limit so more detail from older turns survives.
- B) Re-run `lookup_order` and `get_customer` on every turn so fresh data is always in context.
- C) Extract transactional facts into a persistent "case facts" block included in every prompt.
- D) Ask the customer to re-confirm key amounts whenever the conversation exceeds 20 turns.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.

---

**Question 16.** You maintain your team's coding standards in `~/.claude/CLAUDE.md` on your machine. A new teammate clones the repository, but Claude Code ignores all of those standards for them. Why?

- A) The new teammate needs to run `/memory` once to activate memory files after cloning.
- B) User-level `~/.claude/CLAUDE.md` applies only to your account; team standards belong in a project-level CLAUDE.md.
- C) CLAUDE.md files require an explicit `@import` from the project root before they take effect.
- D) The standards file exceeds the size limit for automatic loading and is being silently truncated.

**Question 17.** Your monorepo has six packages with mostly shared standards but some package-specific conventions. The root CLAUDE.md has grown to 900 lines and every session loads all of it regardless of which package is being edited. Package maintainers know their own conventions best. What is the most maintainable structure?

- A) Duplicate the full standards document into each package directory so every package is self-contained.
- B) Keep the single root CLAUDE.md but add a table of contents so the model can navigate to sections.
- C) Move all standards into a wiki and instruct Claude to ask developers for conventions when unsure.
- D) Keep shared standards in focused files; each package's CLAUDE.md uses `@import` to pull in only what applies.

**Question 18.** Claude Code follows your API error-handling conventions in some sessions but not others, with no obvious pattern. What is the best first diagnostic step?

- A) Run `/memory` to verify which memory files are actually loaded in the affected sessions.
- B) Rewrite the conventions section of CLAUDE.md with stronger, more imperative language.
- C) Run `/compact` to clear stale context that may be overriding the conventions.
- D) Delete and recreate the project CLAUDE.md to rule out file corruption.

**Question 19.** Your team's `/analyze-deps` skill walks the dependency graph and prints thousands of lines of package data. Developers complain that after running it, Claude's answers about their actual coding task get noticeably worse. What change fixes this?

- A) Add `argument-hint` frontmatter so developers scope the analysis to one package at a time.
- B) Move the dependency analysis instructions into CLAUDE.md so no skill invocation is needed.
- C) Add `context: fork` so the skill runs in an isolated sub-agent context and returns a summary.
- D) Add `allowed-tools` frontmatter so the skill can only read files, reducing its output volume.

**Question 20.** Your `/scaffold-component` skill should only ever create new files from templates. During an audit you find a session where it also ran shell commands, including a `git checkout` that discarded a developer's uncommitted changes. What is the right guardrail?

- A) Add a warning to the skill's SKILL.md instructions telling Claude never to run shell commands.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations.
- C) Require developers to commit their work before running any skill.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 21.** Your team has two assets: (1) universal naming and error-handling conventions that apply to all code Claude writes, and (2) a release-notes generation workflow used once per sprint. How should each be configured?

- A) Put both in CLAUDE.md so nothing depends on developers remembering to invoke a skill.
- B) Put both in skills so the context cost is only paid when each is needed.
- C) Conventions in the project CLAUDE.md; the release-notes workflow in a skill under `.claude/skills/`.
- D) Conventions in a skill; the release-notes workflow in CLAUDE.md so it is always available.

**Question 22.** A production bug report includes a stack trace pointing to a single function with an obvious off-by-one error. The fix is one line in one file. How should you proceed in Claude Code?

- A) Use direct execution — the change is simple, well-scoped, and already located.
- B) Enter plan mode to explore the codebase before committing to an approach.
- C) Spawn an Explore subagent to investigate the surrounding module first.
- D) Use `fork_session` to try two candidate fixes in parallel branches.

**Question 23.** You are starting a multi-phase task: first understand how authentication works across a large unfamiliar codebase, then implement a change. The discovery phase will involve reading dozens of files, and you're worried the exploration output will exhaust context before implementation begins. What is the best approach?

- A) Read files in alphabetical order and run `/compact` after every ten files.
- B) Do the discovery in one session, then `--resume` it in a fresh terminal for the implementation phase.
- C) Front-load all the file reads into the first turn so summarization compresses them together.
- D) Use the Explore subagent for discovery so only a summary returns to the main conversation.

**Question 24.** You've described a data transformation to Claude in prose three separate times, and each implementation handles the edge cases differently. What is the most effective way to communicate the expected behavior?

- A) Write a longer, more precise prose specification covering every edge case you can think of.
- B) Provide 2–3 concrete input/output examples demonstrating the transformation and its edge cases.
- C) Ask Claude to restate the requirements before implementing, and correct any misunderstandings.
- D) Lower the temperature so the implementations are at least consistent with each other.

**Question 25.** Two hours into a legacy-codebase exploration session, Claude starts describing "typical repository patterns" instead of the actual classes it read earlier, and gives inconsistent answers about code it correctly explained an hour ago. Which practice best counteracts this for ongoing long sessions?

- A) Ask Claude to "focus on the actual code, not typical patterns" whenever it drifts.
- B) Paste the important files into the conversation again each time the drift appears.
- C) Switch to a model with a larger context window so drift takes longer to appear.
- D) Have Claude keep a scratchpad file of key findings and reference it for later questions.

**Question 26.** You're mapping a large legacy system. The main session's context is filling with raw file contents from exploration, leaving little room for the architectural reasoning you actually need. What is the best structural fix?

- A) Spawn subagents to investigate specific questions while the main agent coordinates high-level understanding.
- B) Summarize each file immediately after reading it and remove the original contents from the conversation.
- C) Read only public interfaces and type signatures, skipping the implementation bodies entirely.
- D) Increase `max_tokens` so responses can be longer during the mapping phase.

**Question 27.** Mid-session, your context is nearly full of verbose discovery output, but you still need to implement the change in this session and want to keep the essential findings. What should you do?

- A) Start a brand-new session and rely on memory of what you learned.
- B) Move the essential findings into the system prompt and clear the rest of the conversation.
- C) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- D) Run `/clear` to reset context, keeping CLAUDE.md as the only persistent state.

**Question 28.** You finished a week-long analysis phase for a large migration and are about to spawn implementation subagents for each module. How should the analysis inform the subagents?

- A) Rely on the subagents inheriting the coordinator session's memory of the analysis automatically.
- B) Summarize the key findings and inject the relevant summary into each subagent's initial context.
- C) Have each subagent redo its own analysis of the relevant module from scratch to guarantee freshness.
- D) Pass the full multi-day session transcript to every subagent so nothing is lost.

**Question 29.** Your overnight multi-agent refactoring job occasionally crashes around hour three, and today's restart lost all progress. What design provides crash recovery?

- A) Increase the job timeout so the crash-prone window is less likely to be hit.
- B) Commit code changes to git after each module so completed work survives a crash.
- C) Shrink the job scope so it finishes before the crash typically occurs.
- D) Have agents export structured state to a known location; the coordinator loads this manifest on resume.

**Question 30.** You concatenated per-module analyses of 30 modules into a single prompt and asked for architecture recommendations. The recommendations consistently cite modules from the beginning and end of the input but ignore the middle third. What is the best mitigation?

- A) Place a key-findings summary first and organize the detail under explicit section headers.
- B) Alphabetize the module sections so the ordering is neutral.
- C) Add an instruction: "Pay equal attention to every module, especially those in the middle."
- D) Switch to a model with a larger context window so all 30 modules fit more comfortably.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 31.** Cost analysis shows that every query — including simple factual ones like "What is the current federal funds rate?" — runs the full search → analysis → synthesis → report pipeline, taking 4+ minutes. What should change?

- A) Cache pipeline outputs so repeated queries return instantly.
- B) Reduce each subagent's token budget so the full pipeline completes faster.
- C) Have the coordinator analyze each query's requirements and invoke only the subagents it needs.
- D) Add a fifth "quick answer" subagent and route all queries through it first.

**Question 32.** The synthesis subagent produces generic, thin output that ignores specific data the search agent found. Logs show the synthesis agent's prompt contains only: "Synthesize the findings on renewable energy storage." What is the root cause?

- A) The synthesis agent's system prompt lacks instructions about depth and specificity.
- B) The synthesis agent needs a larger context window to see the coordinator's conversation.
- C) The search agent is returning results in a format the synthesis agent cannot parse.
- D) Subagents don't inherit the coordinator's history — the findings must be included in the synthesis prompt.

**Question 33.** A research task involves four independent subtopics. The coordinator currently delegates them one at a time, waiting for each subagent to finish before starting the next, quadrupling latency. How should the coordinator spawn the subagents to run them in parallel?

- A) Wrap the Agent SDK in an external async job queue that launches four coordinator processes.
- B) Emit multiple Task tool calls in a single coordinator response, one per subtopic.
- C) Combine all four subtopics into one prompt for a single subagent to handle together.
- D) Enable streaming on the coordinator so subagent calls overlap automatically.

**Question 34.** Your coordinator is configured with `allowedTools: ["WebSearch", "Read"]`. Instead of delegating, it attempts all research itself and never invokes any subagent. What is wrong?

- A) The coordinator's `allowedTools` must include `"Task"` — the tool that spawns subagents.
- B) The subagent definitions are missing `description` fields, so the coordinator cannot see them.
- C) The coordinator's model tier is too low to support delegation.
- D) Subagents must be registered in `.mcp.json` before they can be spawned.

**Question 35.** An engineer proposes letting the search agent pass results directly to the analysis agent, bypassing the coordinator to "cut a hop." What is the main argument against this?

- A) Direct subagent-to-subagent communication doubles token usage through double serialization.
- B) The analysis agent would need the search agent's tool permissions, violating scoping rules.
- C) It sacrifices the observability, error handling, and information control that coordinator routing provides.
- D) The Agent SDK blocks direct communication between subagents at the protocol level.

**Question 36.** Completed reports are coherent but often have coverage gaps — for instance, missing major recent developments the search agent never looked for. The pipeline currently makes a single pass. What is the most effective architectural improvement?

- A) Double the number of search results each query returns so more material is available in the first pass.
- B) Add a coordinator loop that checks the synthesis for gaps and re-delegates targeted queries.
- C) Add an instruction to the synthesis agent to write longer, more comprehensive reports.
- D) Switch the search agent to a more capable model so its first pass finds everything.

**Question 37.** You run two search subagents in parallel for broad topics, but their result sets overlap by roughly 60%, wasting tokens and analysis time. What is the best fix?

- A) Partition the research scope at delegation time — assign each agent distinct subtopics or source types.
- B) Merge the two search agents into one so overlap is impossible.
- C) Add a deduplication step in the coordinator that discards repeated sources after both finish.
- D) Have the second agent wait for the first agent's results and manually avoid its sources.

**Question 38.** Your coordinator prompt gives each subagent a rigid 12-step procedure to follow. Subagents perform well on topics that fit the procedure but fail badly on topics that don't. How should the coordinator's delegation prompts change?

- A) Expand the procedure to 20 steps covering more topic types.
- B) Add branching logic to the procedure: "if the topic is technical, do steps 4a–4c instead."
- C) Specify research goals and quality criteria per delegation instead of step-by-step procedures.
- D) Remove all instructions and let each subagent improvise from its system prompt alone.

**Question 39.** Your system has two tools: `analyze_content` ("Analyzes content and returns insights") and `analyze_document` ("Analyzes documents and returns findings"). Agents misroute between them about 30% of the time. What is the most effective first fix?

- A) Add a system prompt rule: "When in doubt, prefer analyze_document."
- B) Remove one of the tools and route all analysis through the remaining one.
- C) Intercept and correct misrouted calls with a `PostToolUse` hook in the coordinator.
- D) Rename the tools for their distinct purposes and rewrite each description with inputs, outputs, and when to use it.

**Question 40.** `analyze_document` accepts a `mode` parameter that switches between extraction, summarization, and claim verification. Agents frequently pass the wrong mode and get output they didn't expect. What is the best long-term redesign to eliminate this failure class?

- A) Split it into three purpose-specific tools, each with a defined input/output contract.
- B) Make `mode` an enum with detailed documentation for each of the three values.
- C) Default `mode` to summarization, the most common case, so wrong modes matter less.
- D) Have the tool infer the intended mode from the shape of the input it receives.

**Question 41.** The synthesis agent's toolset was copy-pasted from the search agent's config and includes `web_search`. You discover it performing new searches mid-synthesis and weaving unvetted, uncited claims into reports. What is the right fix?

- A) Add a system prompt rule telling the synthesis agent to only search when strictly necessary.
- B) Remove search tools from the synthesis agent so it works only from the findings it is given.
- C) Lower the synthesis agent's temperature so it sticks to the provided findings.
- D) Add a post-hoc citation checker that flags uncited claims in the final report.

**Question 42.** The document analysis agent begins every task with 8–10 exploratory `list_documents` and `search_library` calls just to learn what's in the research library. How can you eliminate this overhead?

- A) Cache the exploratory call results for 24 hours so repeats are cheap.
- B) Paste the full library listing into the agent's system prompt and update it when documents change.
- C) Increase the agent's tool-call budget so the exploration completes faster.
- D) Expose the document catalog as an MCP resource the agent can see without exploratory calls.

**Question 43.** The document analysis agent has a generic `fetch_url` tool and occasionally pulls arbitrary blog pages instead of documents from your vetted research library. What is the best fix?

- A) Add a system prompt instruction listing which domains are acceptable to fetch.
- B) Log all fetched URLs and review them weekly for policy violations.
- C) Replace `fetch_url` with a `load_document` tool that validates URLs against the vetted library.
- D) Reduce the agent's temperature so it makes more conservative fetching choices.

**Question 44.** Final reports contain claims with no traceable source. Investigation shows the analysis agent summarizes findings into prose, and by the time synthesis runs, the source associations are gone. What is the fix?

- A) Require subagents to output structured claim-source mappings that synthesis must preserve and merge.
- B) Have the report agent add citations at the end by searching for a plausible source for each claim.
- C) Append a bibliography of all consulted sources to the end of each report.
- D) Instruct the synthesis agent to only include claims it can remember the source for.

**Question 45.** Two credible sources report the market size for the same year as $4.2B and $6.8B. The synthesis agent currently picks one value, seemingly at random. What should it do instead?

- A) Prefer the more recently published source and discard the other value.
- B) Present both values, annotated as a conflict, with source attribution and methodological context.
- C) Report the midpoint with a footnote noting the two source values.
- D) Request a third source from the coordinator and keep the two values that agree.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** Your review job asks Claude Code for findings and then regex-parses its prose output to post inline PR comments. The parser breaks almost weekly when the output format drifts. What is the robust fix?

- A) Harden the regex with more permissive patterns and fallbacks for known format variants.
- B) Run with `--output-format json` and a `--json-schema` defining the findings structure.
- C) Add a system prompt instruction: "Always use the exact output format below, never deviate."
- D) Post Claude's entire output as a single PR comment so no parsing is needed.

**Question 47.** After a developer pushes new commits to a PR, your pipeline re-runs the review, and the bot posts duplicate comments for issues it already flagged and that remain unfixed. How should re-reviews be designed?

- A) Review only the files changed in the newest commits to keep the review scope minimal.
- B) Delete all previous bot comments before each re-review and post the fresh full set.
- C) Skip re-reviews entirely; one review per PR is sufficient.
- D) Include prior findings in context and instruct Claude to post only new or still-unaddressed issues.

**Question 48.** Your nightly test-generation job produces mostly low-value tests — trivial getter checks and tests of framework behavior — and never uses the fixture factories your team built. What is the most effective fix?

- A) Document testing standards, valuable-test criteria, and available fixture factories in CLAUDE.md.
- B) Generate three times as many tests and have a second job filter out the low-value ones.
- C) Post-process the generated tests to inject fixture factory imports automatically.
- D) Restrict generation to files with less than 50% coverage, where any test adds value.

**Question 49.** Your review bot flags too many trivial style nitpicks. You added "Be conservative — only report issues you are highly confident about" to the prompt, but the false positive rate barely moved. What should you do instead?

- A) Strengthen the wording to "Only report issues you are 100% certain about."
- B) Define categorical criteria: report bugs and security issues; skip minor style and local naming patterns.
- C) Add a second reviewer model and only post findings both agree on.
- D) Have the bot self-assign a confidence score per finding and filter below a threshold.

**Question 50.** False-positive analysis shows the "performance" review category is 70% false positives while all other categories are under 10%. Developers have started ignoring all bot findings, including accurate security ones. What is the best immediate action?

- A) Keep all categories enabled but add a disclaimer that performance findings are experimental.
- B) Lower the displayed severity of performance findings so they look less alarming.
- C) Temporarily disable the performance category while improving its prompts separately.
- D) Batch performance findings into a weekly digest instead of PR comments.

**Question 51.** The same type of issue gets labeled "critical" in one PR and "minor" in another. Severity drives your merge-blocking logic, so inconsistency is breaking the pipeline's usefulness. What is the most effective fix?

- A) Define explicit severity criteria in the prompt with concrete code examples for each level.
- B) Remove severity from findings and block merges on any finding at all.
- C) Ask the model to double-check each severity label before finalizing output.
- D) Map severity from the finding category (all security = critical, all style = minor).

**Question 52.** Despite detailed formatting instructions, review findings arrive in inconsistent shapes — sometimes missing the file location, sometimes merging several issues into one paragraph. What is the most effective technique to get consistent, actionable findings?

- A) Repeat the formatting instructions at both the start and end of the prompt.
- B) Increase `max_tokens` so the model has room to complete every field.
- C) Post-process the output with a second Claude call that reformats it.
- D) Add few-shot examples demonstrating the exact desired format for several finding types.

**Question 53.** Your codebase intentionally uses patterns that the reviewer keeps flagging — like empty catch blocks (with explanatory comments) inside retry helpers. You can't enumerate every acceptable pattern in the prompt. What approach reduces these false positives while still catching genuine issues?

- A) Add few-shot examples contrasting acceptable intentional patterns with genuine issues.
- B) Suppress all findings that involve catch blocks anywhere in the codebase.
- C) Add inline "claude-ignore" comments at every intentional pattern site.
- D) Maintain an exhaustive allowlist file of acceptable patterns and check findings against it.

**Question 54.** You're building the review bot on the Agent SDK, and it returns findings as JSON inside its text response. About 5% of runs produce malformed JSON that crashes the comment poster. What is the most reliable fix?

- A) Wrap the JSON parse in a try/catch and re-request on failure with "valid JSON only."
- B) Ask for YAML instead of JSON, since it is more forgiving of formatting drift.
- C) Define a `report_findings` tool with your findings schema and read from the `tool_use` block.
- D) Add a JSON-repair library to fix trailing commas and unquoted keys before parsing.

**Question 55.** Your review bot has two tools — `report_findings` and `approve_pr` — but sometimes it replies with conversational text like "The code looks good to me!" and calls neither. Downstream automation requires a tool call every time. What is the fix?

- A) Force `tool_choice: {"type": "tool", "name": "report_findings"}` so a tool is always called.
- B) Set `tool_choice: "any"` so the model must call a tool but can choose the appropriate one.
- C) Add a system prompt instruction to always call one of the two tools.
- D) Parse conversational responses and infer approval from positive sentiment.

**Question 56.** Since switching to tool_use with a strict JSON schema, review outputs always parse — but some findings reference line numbers pointing at the wrong lines, and severity labels occasionally contradict the description text. What should you conclude?

- A) The schema needs stricter types; a bounded integer range for line numbers will fix the misalignment.
- B) The model is being truncated mid-generation; increasing `max_tokens` will fix both problems.
- C) Tool use is unsuitable for code review output; revert to prose findings with human triage.
- D) Schemas eliminate syntax errors, not semantic ones; add semantic validation on top.

**Question 57.** Your semantic validator rejects a finding because it references a file that isn't part of the PR diff. What is the most effective retry design?

- A) Send a follow-up with the original context, the failed output, and the specific validation error.
- B) Retry with an identical prompt — validation failures are usually transient.
- C) Silently drop the invalid finding and continue with the valid ones only.
- D) Regenerate the entire review from scratch with a different seed.

**Question 58.** Developers dismiss about 40% of the bot's findings, but you have no systematic way to learn which kinds of code constructs trigger the bad findings. What schema change enables this analysis?

- A) Add a free-text `notes` field where the model can explain its reasoning at length.
- B) Add a `reviewer_id` field so you can compare dismissal rates across model versions.
- C) Add a `detected_pattern` field capturing which code construct triggered each finding.
- D) Add a `confidence` field and assume dismissed findings were low-confidence.

**Question 59.** An engineer proposes moving your agentic "generate tests, run them, fix failures, repeat" workflow to the Message Batches API for the 50% cost savings. Why won't this work?

- A) Batch requests cannot include system prompts, which the workflow depends on.
- B) The Batch API can't execute tools mid-request — the generate-run-fix loop needs multi-turn tool calling.
- C) The Batch API's 24-hour window is too slow for overnight jobs of this size.
- D) The Batch API caps requests at a context size too small for test files.

**Question 60.** Your pipeline has the same Claude Code session generate a feature and then immediately review its own changes. The self-reviews rarely find problems, yet human reviewers regularly catch real bugs in the same code. What is the most effective fix?

- A) Add "review your work with fresh eyes and maximum skepticism" to the self-review prompt.
- B) Enable extended thinking during the self-review step so the model reasons more deeply.
- C) Have the same session review the code three times and merge the findings.
- D) Have a second, independent Claude instance — without the generator's context — perform the review.

---
# Answer Key — Practice Exam 6

**Quick key:** 1-C, 2-D, 3-B, 4-A, 5-D, 6-B, 7-C, 8-B, 9-D, 10-C, 11-A, 12-B, 13-D, 14-A, 15-C, 16-B, 17-D, 18-A, 19-C, 20-B, 21-C, 22-A, 23-D, 24-B, 25-D, 26-A, 27-C, 28-B, 29-D, 30-A, 31-C, 32-D, 33-B, 34-A, 35-C, 36-B, 37-A, 38-C, 39-D, 40-A, 41-B, 42-D, 43-C, 44-A, 45-B, 46-B, 47-D, 48-A, 49-B, 50-C, 51-A, 52-D, 53-A, 54-C, 55-B, 56-D, 57-A, 58-C, 59-B, 60-D

---

**1. C** — The agentic loop must key off `stop_reason`: continue while it is `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Parsing natural-language signals (A) is exactly the anti-pattern producing the observed failures — text can look terminal while a tool call is pending. Iteration caps (B) are a safety backstop, not a primary stopping mechanism, and truncate legitimate long cases. D inverts the semantics: absence of text says nothing definitive about completion.

**2. D** — Tool results must be appended to the conversation history as a `tool_result` block referencing the `tool_use` ID, then the whole conversation is sent back so the model can incorporate the result into its next reasoning step. A keeps the result away from the model entirely — it can't confirm the refund. B misuses the system prompt for turn-level data. C destroys conversational state mid-task and is unnecessary here.

**3. B** — A `PostToolUse` hook deterministically normalizes heterogeneous formats before the model ever sees them, removing the error class entirely. Prompt instructions (A) rely on probabilistic per-turn conversions and will still fail occasionally. C is organizationally impractical and out of your control. D detects errors after they've influenced the conversation instead of preventing them.

**4. A** — A business rule with financial consequences needs deterministic enforcement: intercept the tool call, block amounts over $500, and redirect to escalation. Prompt salience (B), few-shot examples (C), and temperature (D) all still rely on probabilistic compliance — the observed 2% failure rate is precisely why prompt-only enforcement is insufficient here.

**5. D** — The recommended pattern is decomposing multi-concern requests into distinct items, investigating each in parallel with shared context, then synthesizing one unified resolution. A pushes work onto the customer. B escalates cases the agent could resolve, hurting first-contact resolution. C discards the shared context (customer identity, verification) that the concerns have in common.

**6. B** — Humans without transcript access need a structured handoff: customer ID, root cause analysis, amount, recommended action — everything needed to act immediately. A raw transcript (A) forces the human to reconstruct the case anyway, just from more text. C omits the case analysis entirely. D conveys mood, not the facts needed to resolve the dispute.

**7. C** — "Refunds only to the verified original payment method" is a hard compliance rule where any violation has financial/fraud consequences — the case for programmatic enforcement (a hook gating `process_refund`). Tone (A), conciseness (B), and offering alternatives first (D) are behavioral guidance where occasional imperfection is acceptable, so prompt instructions are appropriate.

**8. B** — This workload is explicitly high-ambiguity: the right tools and their order genuinely vary per case, and intermediate results (e.g., what `lookup_order` reveals) change what should happen next — the core argument for model-driven decision-making, and a fixed script also wastes calls on cases that don't need them. A's "always cheaper" is false — model-driven selection spends reasoning tokens. C invents a connection: session resumption doesn't depend on tool ordering. D is false — a scripted sequence can be given any context you choose.

**9. D** — Structured error metadata (`errorCategory`, `isRetryable`, description) gives the agent what it needs to retry transient failures and stop retrying non-retryable ones. Blanket retry (A) wastes calls on business errors and hides retry decisions from the agent. B asks the model to guess what the tool already knows. C reduces one error type's frequency without fixing the decision-making problem.

**10. C** — Business-rule violations should come back as structured errors with `retriable: false` and a customer-friendly explanation so the agent can communicate accurately and pivot to alternatives (store credit). A gives the agent nothing to reason with. B silently misrepresents a failure as success — the agent may tell the customer the refund happened. D leaks internals and buries the relevant fact (policy window) in noise.

**11. A** — "No orders" is a valid empty result of a successful query, not a failure; conflating the two causes exactly the observed misbehavior (apologizing, retrying). Errors should be reserved for access failures. B patches the symptom with prompt text while the contract stays broken. C hides real signal behind a hook. D invents a spurious recovery path for a non-error.

**12. B** — Keyword-sensitive system prompt instructions can create unintended tool associations that override even good tool descriptions — "any customer question about their purchases" is sweeping policy questions into `lookup_order`. A and D modify the tool when the tool isn't the problem. C adds token overhead to counteract an instruction you can simply fix at the source.

**13. D** — Growing from 4 to 18 tools on one agent increases decision complexity and degrades tool selection reliability; the fix is scoped tool access per role, or splitting into specialized agents. A and B describe nonexistent limits. C misdescribes how tool use works — agents don't call every available tool.

**14. A** — Forced tool selection (`tool_choice: {"type": "tool", "name": "classify_request"}`) on the first request is the only option that *guarantees* that specific tool runs first; later turns then proceed normally. B and D are probabilistic. C (`"any"`) guarantees *some* tool call, but not which one — the agent could call `get_customer` first.

**15. C** — Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block that rides outside the summarized history is the recommended defense against progressive summarization degrading precise values into vague ones ("around $80"). A only delays the loss. B works but adds cost and latency on every turn for data that isn't changing. D pushes the system's memory problem onto the customer.

**16. B** — `~/.claude/CLAUDE.md` is user-level configuration: it applies to your account only and never travels through version control. Team-wide standards belong in a project-level CLAUDE.md committed to the repo. A misstates what `/memory` does (it inspects loaded memory; it doesn't "activate" anything). C — project CLAUDE.md loads without imports. D invents a failure mode.

**17. D** — `@import` keeps CLAUDE.md modular: each package's CLAUDE.md pulls in only the relevant shared standards files, and package maintainers with domain knowledge own the selection. A creates six diverging copies. B still loads all 900 lines every session — a table of contents doesn't reduce context. C makes standards invisible to Claude by default.

**18. A** — Inconsistent behavior across sessions is the classic symptom of different memory files being loaded in different sessions; `/memory` shows exactly which files are in effect, so diagnose before rewriting anything. B and D change content before you know whether content is the problem. C addresses context pressure, not configuration loading.

**19. C** — `context: fork` runs the skill in an isolated sub-agent context so its verbose output never enters (pollutes) the main conversation — only the useful summary returns. A reduces volume but the output still lands in the main context. B makes it worse: always-loaded verbosity. D restricts capability, not output destination.

**20. B** — `allowed-tools` in the skill frontmatter is the enforcement mechanism: restrict the skill to file-creation operations and Bash simply isn't available during execution. A is prompt-based and probabilistic — the failure already happened despite the skill's instructions. C mitigates damage rather than preventing it. D is false — slash commands don't disable tools.

**21. C** — Universal, always-applicable standards belong in CLAUDE.md (loaded every session); task-specific workflows used occasionally belong in skills (loaded on demand). A pays the release-notes workflow's context cost in every session. B means conventions only apply when someone remembers to invoke them. D is backwards on both counts.

**22. A** — A single-file, single-line fix with a stack trace pointing at the location is the textbook case for direct execution; plan mode (B), exploration subagents (C), and session forking (D) all add overhead with no decision-making or architectural payoff for a change this well-scoped.

**23. D** — The Explore subagent is designed for exactly this: verbose discovery runs in an isolated context and returns a summary, preserving the main conversation's context for the implementation phase. A still floods the main context between compactions. B — resuming carries the full exploration context into the implementation phase; nothing is isolated. C changes when the flooding happens, not whether it happens.

**24. B** — Concrete input/output examples are the most effective way to communicate expected transformations when prose is being interpreted inconsistently — they pin down the edge cases directly. A produces more prose subject to the same interpretation problem. C surfaces misunderstandings but doesn't pin down edge-case behavior the way examples do. D makes outputs consistent, not correct.

**25. D** — Context degradation in extended sessions (drifting to "typical patterns" instead of discovered specifics) is counteracted by persisting key findings to a scratchpad file and referencing it for subsequent questions — the findings survive outside degrading conversational context. A asks the model to fix a context problem with willpower. B repeatedly re-spends context and accelerates the problem. C delays symptoms without adding persistence.

**26. A** — Delegating specific investigation questions to subagents isolates the verbose file-dump output in their contexts, while the main agent keeps its context for high-level coordination. B — the raw contents have already consumed context by the time they're summarized, and prior turns can't be selectively removed mid-session. C sacrifices the implementation-level understanding a legacy mapping needs. D is unrelated — `max_tokens` governs response length, not context accumulation.

**27. C** — `/compact` summarizes the conversation to reduce context usage while preserving key information — the right mid-session relief valve when you need to keep working. A discards the findings (Claude has no cross-session memory of them). B isn't an available mid-session operation — the system prompt isn't an editable store for conversation findings. D (`/clear`) resets the conversation and loses the findings entirely.

**28. B** — The reliable pattern is summarizing key findings from the completed phase and injecting the relevant summary into each subagent's initial context. A fails because subagents do not inherit parent context automatically. C re-spends a week of analysis. D floods each subagent's context with mostly-irrelevant transcript, inviting lost-in-the-middle problems.

**29. D** — Structured state persistence is the crash-recovery pattern: each agent exports completed work and key findings to a known location; on resume the coordinator loads the manifest and injects state into agent prompts, resuming rather than restarting. A and C reduce crash odds but don't recover from one. B preserves code edits but loses the agents' analysis state, task assignments, and findings — the coordinator still can't resume intelligently.

**30. A** — This is the lost-in-the-middle effect: models reliably process the beginning and end of long inputs but may omit middle sections. The mitigation is a key-findings summary up front plus explicit section headers organizing the detail. B changes ordering without addressing position effects. C — instructions don't fix attention position biases. D — the effect persists in larger windows.

**31. C** — The coordinator should analyze query requirements and dynamically select which subagents to invoke; simple factual queries shouldn't traverse the full pipeline. A only helps repeated queries. B makes every stage worse instead of skipping unneeded stages. D adds a fifth stage to a pipeline whose problem is mandatory stages.

**32. D** — Subagents operate with isolated context: they do not inherit the coordinator's conversation history. The synthesis prompt must include the actual search results and analysis outputs. A would deepen prose style but can't conjure data the agent never received. B misunderstands isolation — window size is irrelevant if the content is never passed. C is contradicted by the logs: nothing was passed at all.

**33. B** — Parallel subagents are spawned by emitting multiple Task tool calls in a single coordinator response, rather than one per turn. A bolts external infrastructure onto a problem the SDK pattern already solves. C serializes the work inside one context and loses parallelism. D — streaming affects token delivery, not tool-call concurrency.

**34. A** — The Task tool is the mechanism for spawning subagents; if `"Task"` isn't in the coordinator's `allowedTools`, it cannot delegate and will attempt the work itself. B affects selection quality among subagents, not the total inability to spawn. C and D describe requirements that don't exist.

**35. C** — Hub-and-spoke routing through the coordinator is what provides observability, consistent error handling, and controlled information flow; a direct side channel sacrifices all three. A invents a token penalty. B is a side detail, not the main architectural argument. D is false — you could build it, it's just a bad idea.

**36. B** — Coverage gaps are addressed with an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient. A adds volume, not targeted coverage. C asks for length — the missing material was never gathered. D still makes a single pass with no gap-checking.

**37. A** — Partitioning research scope — assigning each agent distinct subtopics or source types — prevents duplication at the source. C deduplicates after the tokens and analysis time are already spent. B gives up the parallelism that motivated two agents. D serializes the agents, also defeating parallelism.

**38. C** — Coordinator prompts should specify research goals and quality criteria rather than step-by-step procedures, enabling subagents to adapt their approach to each topic. A and B double down on rigid proceduralism — there will always be topics outside the script. D removes direction entirely; goals and quality bars are still needed.

**39. D** — Tool descriptions are the primary mechanism for tool selection; near-identical names and descriptions cause misrouting. Renaming to purpose-specific names and rewriting descriptions (purpose, inputs, outputs, when-to-use-vs-the-other) fixes the root cause. A papers over ambiguity with a default. B may discard needed functionality. C corrects symptoms downstream and needs its own routing logic — the very thing that's broken.

**40. A** — A generic tool with mode switches invites wrong-mode calls; splitting into purpose-specific tools (`extract_data_points`, `summarize_content`, `verify_claim_against_source`) with clear contracts makes selection explicit and eliminates the failure class. B documents the confusion but keeps the single overloaded entry point. C substitutes a silent wrong behavior for an error. D makes behavior unpredictable and undebuggable.

**41. B** — Agents with tools outside their specialization tend to misuse them; the synthesis agent's job is to work from provided findings, so search tools should be removed from its set (scoped tool access). A is probabilistic and the misuse is already happening. C doesn't remove the capability. D flags damage after publication instead of preventing it.

**42. D** — MCP resources exist to expose content catalogs — giving agents visibility into available data without exploratory tool calls. A makes the waste cheaper, not gone. B is a manual, drift-prone copy of what resources provide natively. C speeds up the overhead instead of eliminating it.

**43. C** — Replacing the generic `fetch_url` with a constrained `load_document` that validates URLs against the vetted library makes the boundary structural rather than behavioral. A relies on prompt compliance. B detects violations after they've contaminated research. D doesn't address capability at all.

**44. A** — Attribution survives only if subagents emit structured claim-source mappings (claim, source, excerpt) and the synthesis agent is required to preserve and merge them; prose summarization is where provenance dies. B fabricates citations after the fact — worse than none. C lists sources without linking claims to them. D relies on memory of information that was already compressed away.

**45. B** — Conflicting statistics from credible sources should be presented with explicit conflict annotation, source attribution, and methodological context — not resolved arbitrarily. A assumes recency explains the difference (it may be methodology or scope). C invents a number no source reported. D outsources the judgment to a majority vote that may simply share a methodology — and discards a credible value either way.

**46. B** — `--output-format json` with `--json-schema` produces machine-parseable, schema-conforming output — the supported mechanism for structured findings in CI. A and C keep betting on format stability that prose output doesn't guarantee. D abandons the inline-comment requirement rather than meeting it.

**47. D** — The documented pattern for re-reviews: include prior findings in context and instruct Claude to report only new or still-unaddressed issues, avoiding duplicate comments. A misses issues that new commits introduce in interaction with unchanged files. B recreates comment noise and destroys discussion threads. C leaves post-push changes unreviewed.

**48. A** — CLAUDE.md is the mechanism for giving CI-invoked Claude Code project context: testing standards, what makes a test valuable, and which fixtures exist. Without it the generator can't know your conventions. B generates waste then filters it. C injects imports into tests that still don't use the factories meaningfully. D narrows scope without improving quality within it.

**49. B** — General instructions like "be conservative" or "high-confidence only" demonstrably fail to improve precision; explicit categorical criteria — report these types, skip those types — are what work. A is more of the same failed approach. D relies on self-reported confidence, which is poorly calibrated. C doubles cost and still lacks defined criteria for either reviewer.

**50. C** — One high-false-positive category undermines trust in all categories. Temporarily disabling the 70%-FP performance category restores signal quality immediately while you improve its prompts offline. A, B, and D all keep the noise flowing in some form, and trust continues eroding.

**51. A** — Consistent classification comes from explicit severity criteria with concrete code examples for each level. B makes every nitpick merge-blocking. C is self-review with no standard to check against. D is too coarse — not all security findings are critical, and category ≠ impact.

**52. D** — When detailed instructions alone produce inconsistent output, few-shot examples demonstrating the exact desired format (location, issue, severity, suggested fix) are the most effective technique for consistency. A repeats what already isn't working. B addresses truncation, which isn't the symptom. C adds cost and a second chance for drift.

**53. A** — Few-shot examples contrasting acceptable intentional patterns with genuine issues let the model generalize the judgment to novel cases — exactly what an enumerated list (D) can't do. B suppresses real bugs involving catch blocks. C requires annotating the whole codebase and doesn't help with new code.

**54. C** — Tool use with a JSON schema is the most reliable path to structured output: the `report_findings` tool's input schema guarantees well-formed structure, eliminating the JSON-in-text syntax errors. A and D are recovery layers for a problem you can eliminate outright. B trades one fragile text format for another.

**55. B** — `tool_choice: "any"` guarantees the model calls *a* tool while leaving it free to pick the appropriate one (`report_findings` vs `approve_pr`). A forces every response through `report_findings`, breaking approvals. C is probabilistic — the failure already occurs despite instructions. D is sentiment-parsing fragility replacing a structural guarantee.

**56. D** — Strict schemas via tool use eliminate *syntax* errors but not *semantic* errors — wrong line numbers and contradictory severities are semantically wrong, schema-valid outputs. The fix is semantic validation layered on top (e.g., verifying line references against the diff, cross-checking severity against criteria). A — a bounded range can't know which line is correct. B misdiagnoses; truncated output would fail schema validation. C throws away the syntax guarantee to fix nothing.

**57. A** — Retry-with-error-feedback: include the original context, the failed output, and the specific validation error ("finding 3 references src/util.ts, which is not in this diff") so the model can self-correct. An identical retry (B) has no new information and will likely fail identically. C silently loses a possibly-real finding that referenced the wrong file. D discards all the valid findings along with the invalid one.

**58. C** — A `detected_pattern` field records which code construct triggered each finding, enabling systematic aggregation of dismissals by pattern — the feedback loop you're missing. A gives unstructured text you can't aggregate. B varies the wrong dimension. D assumes the correlation you're trying to measure.

**59. B** — The Batch API does not support multi-turn tool calling within a request: it cannot pause mid-request, execute your test-runner tool, and feed results back to the model. An iterative generate-run-fix loop is inherently multi-turn tool use. C is backwards — overnight jobs are the Batch API's sweet spot. A and D describe restrictions that don't exist.

**60. D** — A model reviewing its own generation retains the reasoning context that produced the code, making it unlikely to question its own decisions. An independent instance without that context is more effective at catching subtle issues. A and B try to prompt or think around a structural bias. C repeats the biased review three times.

---

*End of Practice Exam 6.*
