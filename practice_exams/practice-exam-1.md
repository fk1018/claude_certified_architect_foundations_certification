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

- A) Expand the phrase list to cover more terminal expressions and add fuzzy matching to catch paraphrases.
- B) Continue the loop while `stop_reason` is `"tool_use"`, executing requested tools and returning results; terminate when `stop_reason` is `"end_turn"`.
- C) Set a maximum of 10 iterations and terminate when the cap is reached, since most support cases complete in fewer turns.
- D) Terminate whenever the response contains no text content, since a tool-only response indicates the agent is still working.

**Question 2.** Your agent calls `process_refund` and your code executes the refund successfully. What must happen next so the agent can correctly continue the conversation?

- A) Append the tool result to the conversation history as a `tool_result` block (referencing the `tool_use` ID) in a user-role message, then send the updated conversation back to Claude.
- B) Store the refund confirmation in your application database and include a summary of all tool activity in the final response to the customer.
- C) Inject the refund confirmation into the system prompt so it persists across all subsequent turns of the conversation.
- D) Start a new conversation seeded with a summary of the prior turns plus the refund result, to keep context small.

**Question 3.** Your MCP tools come from different backend teams: `get_customer` returns ISO 8601 dates, `lookup_order` returns Unix timestamps, and order statuses are numeric codes in one tool but strings in another. The agent occasionally miscompares dates and misreads statuses when reasoning across tools. What is the most reliable fix?

- A) Add a system prompt section documenting each tool's formats and instructing the agent to convert values before comparing them.
- B) Ask each backend team to migrate their APIs to a common format standard before the agent ships.
- C) Add a validation step at the end of each conversation that checks the agent's final answer for date and status errors.
- D) Implement a `PostToolUse` hook that normalizes timestamps, dates, and status codes into consistent formats before the model processes the tool results.

**Question 4.** Company policy requires human approval for any refund over $500. Your system prompt states this rule prominently, but production logs show that about 2% of refunds above $500 are still processed autonomously. What should you do?

- A) Move the rule to the very top of the system prompt and repeat it before the tool definitions to increase its salience.
- B) Add few-shot examples showing the agent escalating refunds of $501, $750, and $1,200 to reinforce the boundary.
- C) Implement a hook that intercepts `process_refund` calls, blocks any call with an amount above $500, and redirects the agent to the human escalation workflow.
- D) Reduce the model temperature so the agent follows the system prompt instructions more deterministically.

**Question 5.** A customer writes one message reporting a damaged item, a duplicate charge on their card, and an address change for an upcoming shipment. The agent resolves the damaged item and ends the conversation without addressing the other two concerns. What is the best design change?

- A) Detect multi-issue messages with a classifier and ask the customer to submit each issue as a separate ticket.
- B) Instruct the agent to decompose multi-concern messages into distinct items, investigate each (in parallel where possible) using the shared conversation context, and synthesize a unified resolution covering all items.
- C) Route any message containing more than one concern directly to `escalate_to_human`, since multi-issue cases exceed single-agent capability.
- D) Handle the concerns sequentially in separate sessions, one new session per concern, so each gets a clean context window.

**Question 6.** When the agent escalates a billing dispute to a human agent, the human team works in a separate system with no access to the AI conversation transcript. Human agents report spending 10+ minutes reconstructing each case. What should the escalation include?

- A) The complete raw conversation transcript exported as text, so the human can read everything the agent saw.
- B) The customer ID and a link to open the customer's profile, keeping the handoff lightweight.
- C) A sentiment analysis of the conversation so the human knows how frustrated the customer is.
- D) A structured handoff summary containing the customer ID, root cause analysis, the disputed/refund amount, and a recommended action.

**Question 7.** You are deciding which agent behaviors need programmatic enforcement (hooks) versus system-prompt guidance. Which requirement is the strongest candidate for a hook rather than prompt instructions?

- A) The agent should maintain an empathetic, professional tone with frustrated customers.
- B) Refunds must only ever be issued to the verified original payment method on the order.
- C) The agent should keep responses concise and avoid unnecessary technical jargon.
- D) The agent should offer troubleshooting alternatives before proposing a refund.

**Question 8.** A product manager proposes replacing the agent's reasoning with a fixed sequence — always call `get_customer`, then `lookup_order`, then either resolve or refund — arguing it will make behavior predictable. Why is model-driven tool selection the better fit for this workload?

- A) Support requests are high-ambiguity, so the appropriate tools and their order vary per case; a fixed sequence wastes calls on some cases and cannot adapt when intermediate results change what is needed.
- B) Fixed sequences are not supported by the Claude Agent SDK, which requires the model to choose every tool call.
- C) Model-driven selection is always cheaper because the model skips the reasoning tokens needed to follow a script.
- D) Decision trees cannot invoke MCP tools, so the fixed sequence would only work with built-in tools.

**Question 9.** Every failure from `process_refund` currently returns the same response: `"Operation failed"`. Logs show the agent retrying policy-violation failures repeatedly (which will never succeed) and giving up immediately on transient gateway timeouts (which would succeed on retry). What is the best fix?

- A) Wrap all tool calls in an automatic retry-3-times policy at the application layer so the agent never has to reason about retries.
- B) Add a system prompt instruction telling the agent to judge from conversation context whether a failure is likely to be retryable.
- C) Return structured error responses that include an `errorCategory` (transient/validation/permission/business), an `isRetryable` boolean, and a human-readable description.
- D) Increase the payment gateway timeout so transient failures become rare enough to ignore.

**Question 10.** A customer requests a refund for an order purchased 47 days ago; policy allows refunds within 30 days. What should `process_refund` return so the agent handles this well?

- A) An error with the MCP `isError` pattern containing a business-rule category, `retriable: false`, a customer-friendly explanation ("outside the 30-day return window — purchase was 47 days ago"), and a suggested alternative such as store credit.
- B) A standard HTTP 400 status code with no body, letting the agent infer the cause from the request it sent.
- C) A success response with an empty body, so the agent doesn't alarm the customer with error language.
- D) An error containing the full server-side stack trace so the agent has maximum information to reason with.

**Question 11.** When a customer has no orders on file, `lookup_order` currently returns an error, and the agent responds by apologizing for "technical difficulties" and retrying the lookup. What should change?

- A) Add a system prompt note explaining that this particular error usually means the customer has no orders.
- B) Suppress the error in a hook and replace it with a message telling the agent to end the conversation.
- C) Have the agent call `get_customer` again first, since the error may indicate a bad customer ID.
- D) Return a successful response with an empty result set (and a note like "no orders found for this customer"), reserving errors for actual access failures.

**Question 12.** Your tool descriptions are detailed and well-differentiated, yet the agent calls `lookup_order` even for general return-policy questions where no order is involved. You find this line in the system prompt: "Use lookup_order to help with any customer question about their purchases." What is the most likely fix?

- A) Rewrite the `lookup_order` description to explicitly say it should not be used for policy questions.
- B) Add few-shot examples of policy questions being answered without tool calls.
- C) Reword or remove the keyword-sensitive system prompt instruction, which is creating an unintended tool association that overrides the well-written descriptions.
- D) Rename `lookup_order` to `lookup_order_by_id` so the model understands an ID is required.

**Question 13.** The support team wants to expand the agent from its current 4 tools to 18 by adding loyalty-program, marketing-preferences, subscription, and gift-card tools — all attached to the single resolution agent. What is the primary risk?

- A) The MCP protocol limits each server to 10 tools, so the configuration will fail at connection time.
- B) Tool selection reliability degrades as the number of available tools grows, increasing decision complexity and misrouting; tools should be scoped to the agent's role or split across specialized agents.
- C) The additional tool schemas will exceed the model's context window before any conversation begins.
- D) The agent will slow down because it must call every available tool at least once per conversation.

**Question 14.** Compliance requires that every conversation begin with a call to a `classify_request` tool before any other tool runs, with no exceptions. What is the most reliable implementation?

- A) State in the system prompt that `classify_request` is mandatory and must always come first.
- B) Set `tool_choice: "any"` on the first request so the model is guaranteed to call a tool before responding.
- C) Add few-shot examples showing `classify_request` being called first in several conversation types.
- D) Set `tool_choice: {"type": "tool", "name": "classify_request"}` on the first API request, then use normal tool choice on subsequent turns.

**Question 15.** In long billing-dispute conversations, your context management summarizes older turns. After summarization, the agent starts misstating specifics — quoting "around $80" for a refund the customer was promised at exactly $83.47. What is the best fix?

- A) Extract transactional facts (amounts, dates, order numbers, statuses) into a persistent "case facts" block that is included in every prompt outside the summarized history.
- B) Increase the summary length limit so the summarizer preserves more detail from older turns.
- C) Re-run `lookup_order` and `get_customer` on every turn so fresh data is always in context.
- D) Ask the customer to re-confirm key amounts whenever the conversation exceeds 20 turns.

---

## Scenario B: Code Generation with Claude Code (Questions 16–30)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation. You need to integrate it into your development workflow with custom slash commands, CLAUDE.md configurations, and understand when to use plan mode vs direct execution.

---

**Question 16.** You maintain your team's coding standards in `~/.claude/CLAUDE.md` on your machine. A new teammate clones the repository, but Claude Code ignores all of those standards for them. Why?

- A) The new teammate needs to run `/memory` once to activate memory files after cloning.
- B) CLAUDE.md files require an explicit `@import` from the project root before they take effect.
- C) `~/.claude/CLAUDE.md` is user-level configuration that applies only to your account and is not shared through version control; team standards belong in a project-level CLAUDE.md committed to the repository.
- D) The standards file exceeds the size limit for automatic loading and is being silently truncated.

**Question 17.** Your monorepo has six packages with mostly shared standards but some package-specific conventions. The root CLAUDE.md has grown to 900 lines and every session loads all of it regardless of which package is being edited. Package maintainers know their own conventions best. What is the most maintainable structure?

- A) Keep shared standards in focused files and have each package's CLAUDE.md use `@import` to include only the standards files relevant to that package, maintained by the package owners.
- B) Duplicate the full 900-line standards document into each package directory so every package is self-contained.
- C) Keep the single root CLAUDE.md but add a table of contents so the model can navigate to the relevant section.
- D) Move all standards into a wiki and add a CLAUDE.md instruction telling Claude to ask developers for conventions when unsure.

**Question 18.** Claude Code follows your API error-handling conventions in some sessions but not others, with no obvious pattern. What is the best first diagnostic step?

- A) Rewrite the conventions section of CLAUDE.md with stronger, more imperative language.
- B) Run `/memory` to verify which memory files are actually loaded in the affected sessions.
- C) Run `/compact` to clear stale context that may be overriding the conventions.
- D) Delete and recreate the project CLAUDE.md to rule out file corruption.

**Question 19.** Your team's `/analyze-deps` skill walks the dependency graph and prints thousands of lines of package data. Developers complain that after running it, Claude's answers about their actual coding task get noticeably worse. What change fixes this?

- A) Add `argument-hint` frontmatter so developers scope the analysis to one package at a time.
- B) Move the dependency analysis instructions into CLAUDE.md so they are always loaded and no skill invocation is needed.
- C) Add `allowed-tools` frontmatter so the skill can only read files, reducing the volume of output it produces.
- D) Add `context: fork` to the skill's frontmatter so it runs in an isolated sub-agent context and returns only a summary, keeping the verbose output out of the main conversation.

**Question 20.** Your `/scaffold-component` skill should only ever create new files from templates. During an audit you find a session where it also ran shell commands, including a `git checkout` that discarded a developer's uncommitted changes. What is the right guardrail?

- A) Add a warning to the skill's SKILL.md instructions telling Claude never to run shell commands.
- B) Require developers to commit their work before running any skill.
- C) Configure `allowed-tools` in the skill's frontmatter to permit only file-creation operations, so Bash is unavailable during skill execution.
- D) Convert the skill into a slash command, since commands cannot run tools.

**Question 21.** Your team has two assets: (1) universal naming and error-handling conventions that apply to all code Claude writes, and (2) a release-notes generation workflow used once per sprint. How should each be configured?

- A) Put the universal conventions in the project CLAUDE.md (always loaded) and the release-notes workflow in a skill under `.claude/skills/` (invoked on demand).
- B) Put both in CLAUDE.md so nothing depends on developers remembering to invoke a skill.
- C) Put both in skills so the context cost is only paid when each is needed.
- D) Put the conventions in a skill and the release-notes workflow in CLAUDE.md, since workflows need to be always available.

**Question 22.** A production bug report includes a stack trace pointing to a single function with an obvious off-by-one error. The fix is one line in one file. How should you proceed in Claude Code?

- A) Enter plan mode to explore the codebase before committing to an approach.
- B) Spawn an Explore subagent to investigate the surrounding module first.
- C) Use `fork_session` to try two candidate fixes in parallel branches.
- D) Use direct execution — the change is simple, well-scoped, and the location is already known, so planning overhead adds no value.

**Question 23.** You are starting a multi-phase task: first understand how authentication works across a large unfamiliar codebase, then implement a change. The discovery phase will involve reading dozens of files, and you're worried the exploration output will exhaust context before implementation begins. What is the best approach?

- A) Read files in alphabetical order and run `/compact` after every ten files.
- B) Use the Explore subagent for the discovery phase so the verbose exploration happens in an isolated context and only a summary returns to the main conversation.
- C) Ask Claude to skip exploration and infer the auth architecture from the directory names.
- D) Split the work across two terminal windows, one for reading and one for writing.

**Question 24.** You've described a data transformation to Claude in prose three separate times, and each implementation handles the edge cases differently. What is the most effective way to communicate the expected behavior?

- A) Write a longer, more precise prose specification covering every edge case you can think of.
- B) Ask Claude to restate the requirements before implementing, and correct any misunderstandings.
- C) Provide 2–3 concrete input/output examples demonstrating the transformation, including the edge cases.
- D) Lower the temperature so the implementations are at least consistent with each other.

**Question 25.** Two hours into a legacy-codebase exploration session, Claude starts describing "typical repository patterns" instead of the actual classes it read earlier, and gives inconsistent answers about code it correctly explained an hour ago. Which practice best counteracts this for ongoing long sessions?

- A) Have Claude maintain a scratchpad file recording key findings as it explores, and reference that file when answering subsequent questions.
- B) Ask Claude to "focus on the actual code, not typical patterns" whenever it drifts.
- C) Paste the important files into the conversation again each time the drift appears.
- D) Switch to a model with a larger context window so drift takes longer to appear.

**Question 26.** You're mapping a large legacy system. The main session's context is filling with raw file contents from exploration, leaving little room for the architectural reasoning you actually need. What is the best structural fix?

- A) Disable file reading and work only from the directory tree structure.
- B) Increase `max_tokens` so responses can be longer.
- C) Read only the first 50 lines of each file to reduce volume.
- D) Spawn subagents to investigate specific questions ("find all test files," "trace the refund flow dependencies") while the main agent preserves its context for high-level coordination.

**Question 27.** Mid-session, your context is nearly full of verbose discovery output, but you still need to implement the change in this session and want to keep the essential findings. What should you do?

- A) Start a brand-new session and rely on memory of what you learned.
- B) Run `/compact` to summarize the conversation and reduce context usage while preserving key information.
- C) Delete the project CLAUDE.md temporarily to free up context space.
- D) Keep working — Claude automatically ignores old context when it becomes irrelevant.

**Question 28.** You finished a week-long analysis phase for a large migration and are about to spawn implementation subagents for each module. How should the analysis inform the subagents?

- A) Rely on the subagents inheriting the coordinator session's memory of the analysis automatically.
- B) Have each subagent redo its own analysis of the relevant module from scratch to guarantee freshness.
- C) Summarize the key findings from the exploration phase and inject the relevant summary into each subagent's initial context.
- D) Pass the full multi-day session transcript to every subagent so nothing is lost.

**Question 29.** Your overnight multi-agent refactoring job occasionally crashes around hour three, and today's restart lost all progress. What design provides crash recovery?

- A) Have each agent export structured state (completed work, key findings) to a known location, and have the coordinator load a manifest of these exports on resume and inject them into agent prompts.
- B) Increase the job timeout so the crash-prone window is less likely to be hit.
- C) Run the full job twice in parallel so one copy is likely to survive.
- D) Shrink the job scope so it finishes before the crash typically occurs.

**Question 30.** You concatenated per-module analyses of 30 modules into a single prompt and asked for architecture recommendations. The recommendations consistently cite modules from the beginning and end of the input but ignore the middle third. What is the best mitigation?

- A) Alphabetize the module sections so the ordering is neutral.
- B) Add an instruction: "Pay equal attention to every module, especially those in the middle."
- C) Switch to a model with a larger context window so all 30 modules fit more comfortably.
- D) Place a key-findings summary at the beginning of the input and organize the detailed module results under explicit section headers to mitigate position effects.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 31.** Cost analysis shows that every query — including simple factual ones like "What is the current federal funds rate?" — runs the full search → analysis → synthesis → report pipeline, taking 4+ minutes. What should change?

- A) Cache pipeline outputs so repeated queries return instantly.
- B) Design the coordinator to analyze each query's requirements and dynamically invoke only the subagents the query actually needs, rather than always routing through the full pipeline.
- C) Reduce each subagent's token budget so the full pipeline completes faster.
- D) Add a fifth "quick answer" subagent and route all queries through it first.

**Question 32.** The synthesis subagent produces generic, thin output that ignores specific data the search agent found. Logs show the synthesis agent's prompt contains only: "Synthesize the findings on renewable energy storage." What is the root cause?

- A) The synthesis agent's system prompt lacks instructions about depth and specificity.
- B) The synthesis agent needs a larger context window to see the coordinator's conversation.
- C) Subagents do not inherit the coordinator's conversation history — the search results and analysis outputs must be included directly in the synthesis agent's prompt.
- D) The search agent is returning results in a format the synthesis agent cannot parse.

**Question 33.** A research task involves four independent subtopics. The coordinator currently delegates them one at a time, waiting for each subagent to finish before starting the next, quadrupling latency. How should the coordinator spawn the subagents to run them in parallel?

- A) Emit multiple Task tool calls in a single coordinator response, one per subtopic.
- B) Wrap the Agent SDK in an external async job queue that launches four coordinator processes.
- C) Combine all four subtopics into one prompt for a single subagent to handle together.
- D) Enable streaming on the coordinator so subagent calls overlap automatically.

**Question 34.** Your coordinator is configured with `allowedTools: ["WebSearch", "Read"]`. Instead of delegating, it attempts all research itself and never invokes any subagent. What is wrong?

- A) The subagent definitions are missing `description` fields, so the coordinator cannot see them.
- B) The coordinator's model tier is too low to support delegation.
- C) Subagents must be registered in `.mcp.json` before they can be spawned.
- D) The coordinator's `allowedTools` must include `"Task"` — the Task tool is the mechanism for spawning subagents.

**Question 35.** An engineer proposes letting the search agent pass results directly to the analysis agent, bypassing the coordinator to "cut a hop." What is the main argument against this?

- A) Direct subagent-to-subagent communication doubles token usage because results are serialized twice.
- B) Routing all communication through the coordinator preserves observability, consistent error handling, and controlled information flow — direct channels sacrifice all three.
- C) The Agent SDK blocks direct communication between subagents at the protocol level, so the proposal cannot be built.
- D) The analysis agent would need the search agent's tool permissions, violating scoping rules.

**Question 36.** Completed reports are coherent but often have coverage gaps — for instance, missing major recent developments the search agent never looked for. The pipeline currently makes a single pass. What is the most effective architectural improvement?

- A) Add an iterative refinement loop: the coordinator evaluates the synthesis output for gaps, re-delegates targeted queries to the search and analysis subagents, and re-invokes synthesis until coverage is sufficient.
- B) Double the number of search results each query returns so more material is available in the first pass.
- C) Add an instruction to the synthesis agent to write longer, more comprehensive reports.
- D) Switch the search agent to a more capable model so its first pass finds everything.

**Question 37.** You run two search subagents in parallel for broad topics, but their result sets overlap by roughly 60%, wasting tokens and analysis time. What is the best fix?

- A) Merge the two search agents into one so overlap is impossible.
- B) Add a deduplication step in the coordinator that discards repeated sources after both agents finish.
- C) Partition the research scope when delegating — assign each search agent distinct subtopics or source types so their coverage is complementary.
- D) Have the second agent wait for the first agent's results and manually avoid its sources.

**Question 38.** Your coordinator prompt gives each subagent a rigid 12-step procedure to follow. Subagents perform well on topics that fit the procedure but fail badly on topics that don't. How should the coordinator's delegation prompts change?

- A) Expand the procedure to 20 steps covering more topic types.
- B) Add branching logic to the procedure: "if the topic is technical, do steps 4a–4c instead."
- C) Remove all instructions and let each subagent improvise from its system prompt alone.
- D) Specify the research goals and quality criteria for each delegation, rather than step-by-step procedural instructions, so subagents can adapt their approach to the topic.

**Question 39.** Your system has two tools: `analyze_content` ("Analyzes content and returns insights") and `analyze_document` ("Analyzes documents and returns findings"). Agents misroute between them about 30% of the time. What is the most effective first fix?

- A) Rename the tools to reflect their actual distinct purposes (e.g., `extract_web_results` for the web one) and rewrite each description to state its purpose, expected inputs, outputs, and when to use it versus the other.
- B) Add a system prompt rule: "When in doubt, prefer analyze_document."
- C) Remove one of the tools and route all analysis through the remaining one.
- D) Have the coordinator intercept and correct misrouted calls with a `PostToolUse` hook.

**Question 40.** `analyze_document` accepts a `mode` parameter that switches between extraction, summarization, and claim verification. Agents frequently pass the wrong mode and get output they didn't expect. What is the best redesign?

- A) Make `mode` an enum with better documentation for each value.
- B) Split the tool into three purpose-specific tools — `extract_data_points`, `summarize_content`, and `verify_claim_against_source` — each with a defined input/output contract.
- C) Default `mode` to summarization, the most common case, so wrong modes matter less.
- D) Have the tool infer the intended mode from the shape of the input.

**Question 41.** The synthesis agent's toolset was copy-pasted from the search agent's config and includes `web_search`. You discover it performing new searches mid-synthesis and weaving unvetted, uncited claims into reports. What is the right fix?

- A) Add a system prompt rule telling the synthesis agent to only search when strictly necessary.
- B) Lower the synthesis agent's temperature so it sticks to the provided findings.
- C) Add a post-hoc citation checker that flags uncited claims in the final report.
- D) Restrict each subagent's toolset to its role — remove search tools from the synthesis agent so it works only from the findings it is given.

**Question 42.** The document analysis agent begins every task with 8–10 exploratory `list_documents` and `search_library` calls just to learn what's in the research library. How can you eliminate this overhead?

- A) Cache the exploratory call results for 24 hours so repeats are cheap.
- B) Paste the full library listing into the agent's system prompt and update the prompt whenever documents change.
- C) Expose the document catalog as an MCP resource so the agent has visibility into available documents without exploratory tool calls.
- D) Increase the agent's tool-call budget so the exploration completes faster.

**Question 43.** The document analysis agent has a generic `fetch_url` tool and occasionally pulls arbitrary blog pages instead of documents from your vetted research library. What is the best fix?

- A) Replace `fetch_url` with a constrained `load_document` tool that validates requested URLs against the vetted document library.
- B) Add a system prompt instruction listing which domains are acceptable to fetch.
- C) Log all fetched URLs and review them weekly for policy violations.
- D) Reduce the agent's temperature so it makes more conservative fetching choices.

**Question 44.** Final reports contain claims with no traceable source. Investigation shows the analysis agent summarizes findings into prose, and by the time synthesis runs, the source associations are gone. What is the fix?

- A) Have the report agent add citations at the end by searching for a plausible source for each claim.
- B) Require subagents to output structured claim-source mappings (claim, source URL or document name, relevant excerpt), and require the synthesis agent to preserve and merge these mappings rather than compressing findings into prose.
- C) Append a bibliography of all consulted sources to the end of each report.
- D) Instruct the synthesis agent to only include claims it can remember the source for.

**Question 45.** Two credible sources report the market size for the same year as $4.2B and $6.8B. The synthesis agent currently picks one value, seemingly at random. What should it do instead?

- A) Average the two values and report $5.5B with a footnote.
- B) Always prefer the more recently published source and discard the other value.
- C) Present both values, explicitly annotated as a conflict, with source attribution and any methodological context explaining the difference.
- D) Omit the statistic entirely, since conflicting data cannot be trusted.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** Your review job asks Claude Code for findings and then regex-parses its prose output to post inline PR comments. The parser breaks almost weekly when the output format drifts. What is the robust fix?

- A) Harden the regex with more permissive patterns and fallbacks for known format variants.
- B) Add a system prompt instruction: "Always use the exact output format below, never deviate."
- C) Post Claude's entire output as a single PR comment so no parsing is needed.
- D) Run Claude Code with `--output-format json` and a `--json-schema` defining the findings structure, producing machine-parseable output for the comment poster.

**Question 47.** After a developer pushes new commits to a PR, your pipeline re-runs the review, and the bot posts duplicate comments for issues it already flagged and that remain unfixed. How should re-reviews be designed?

- A) Include the prior review's findings in context and instruct Claude to report only new issues or previously-flagged issues that remain unaddressed, without re-posting duplicates.
- B) Review only the files changed in the newest commits to keep the review scope minimal.
- C) Delete all previous bot comments before each re-review and post the fresh full set.
- D) Skip re-reviews entirely; one review per PR is sufficient.

**Question 48.** Your nightly test-generation job produces mostly low-value tests — trivial getter checks and tests of framework behavior — and never uses the fixture factories your team built. What is the most effective fix?

- A) Generate three times as many tests and have a second job filter out the low-value ones.
- B) Document your testing standards, criteria for valuable tests, and available fixture factories in CLAUDE.md so the CI-invoked Claude Code has that project context.
- C) Post-process the generated tests to inject fixture factory imports automatically.
- D) Restrict generation to files with less than 50% coverage, where any test adds value.

**Question 49.** Your review bot flags too many trivial style nitpicks. You added "Be conservative — only report issues you are highly confident about" to the prompt, but the false positive rate barely moved. What should you do instead?

- A) Strengthen the wording to "Only report issues you are 100% certain about."
- B) Add a second reviewer model and only post findings both agree on.
- C) Replace confidence-based filtering with explicit categorical criteria that define which issue types to report (bugs, security vulnerabilities) and which to skip (minor style, local naming patterns).
- D) Have the bot self-assign a confidence score per finding and filter below a threshold.

**Question 50.** False-positive analysis shows the "performance" review category is 70% false positives while all other categories are under 10%. Developers have started ignoring all bot findings, including accurate security ones. What is the best immediate action?

- A) Temporarily disable the performance category to restore trust in the remaining categories, while improving the performance prompts separately.
- B) Keep all categories enabled but add a disclaimer that performance findings are experimental.
- C) Lower the displayed severity of performance findings so they look less alarming.
- D) Batch performance findings into a weekly digest instead of PR comments.

**Question 51.** The same type of issue gets labeled "critical" in one PR and "minor" in another. Severity drives your merge-blocking logic, so inconsistency is breaking the pipeline's usefulness. What is the most effective fix?

- A) Remove severity from findings and block merges on any finding at all.
- B) Ask the model to double-check each severity label before finalizing output.
- C) Map severity from the finding category (all security = critical, all style = minor).
- D) Define explicit severity criteria in the prompt with concrete code examples illustrating each severity level.

**Question 52.** Despite detailed formatting instructions, review findings arrive in inconsistent shapes — sometimes missing the file location, sometimes merging several issues into one paragraph. What is the most effective technique to get consistent, actionable findings?

- A) Repeat the formatting instructions at both the start and end of the prompt.
- B) Add few-shot examples to the prompt demonstrating the exact desired output format — location, issue description, severity, and suggested fix — for several finding types.
- C) Increase `max_tokens` so the model has room to complete every field.
- D) Post-process the output with a second Claude call that reformats it.

**Question 53.** Your codebase intentionally uses patterns that the reviewer keeps flagging — like empty catch blocks (with explanatory comments) inside retry helpers. You can't enumerate every acceptable pattern in the prompt. What approach reduces these false positives while still catching genuine issues?

- A) Suppress all findings that involve catch blocks anywhere in the codebase.
- B) Add inline "claude-ignore" comments at every intentional pattern site.
- C) Add few-shot examples contrasting acceptable intentional patterns with genuine issues, so the model learns the judgment and generalizes it to novel cases.
- D) Maintain an exhaustive allowlist file of acceptable patterns and check findings against it.

**Question 54.** You're building the review bot on the Agent SDK, and it returns findings as JSON inside its text response. About 5% of runs produce malformed JSON that crashes the comment poster. What is the most reliable fix?

- A) Define a `report_findings` tool whose input schema is your findings structure, and read the findings from the structured `tool_use` block instead of parsing text.
- B) Wrap the JSON parse in a try/catch and re-request on failure with "valid JSON only."
- C) Ask for YAML instead of JSON, since it is more forgiving of formatting drift.
- D) Add a JSON-repair library to fix trailing commas and unquoted keys before parsing.

**Question 55.** Your review bot has two tools — `report_findings` and `approve_pr` — but sometimes it replies with conversational text like "The code looks good to me!" and calls neither. Downstream automation requires a tool call every time. What is the fix?

- A) Force `tool_choice: {"type": "tool", "name": "report_findings"}` so a tool is always called.
- B) Add a system prompt instruction to always call one of the two tools.
- C) Parse conversational responses and infer approval from positive sentiment.
- D) Set `tool_choice: "any"` so the model must call a tool but can still choose the appropriate one.

**Question 56.** Since switching to tool_use with a strict JSON schema, review outputs always parse — but some findings reference line numbers pointing at the wrong lines, and severity labels occasionally contradict the description text. What should you conclude?

- A) The schema needs stricter types; changing line numbers to a bounded integer range will fix the misalignment.
- B) Strict schemas eliminate syntax errors but not semantic errors — you need semantic validation (e.g., verifying line references against the diff, cross-checking severity against criteria) on top of schema compliance.
- C) The model is being truncated mid-generation; increasing `max_tokens` will fix both problems.
- D) Tool use is unsuitable for code review output; revert to prose findings with human triage.

**Question 57.** Your semantic validator rejects a finding because it references a file that isn't part of the PR diff. What is the most effective retry design?

- A) Retry with an identical prompt — validation failures are usually transient.
- B) Silently drop the invalid finding and continue with the valid ones only.
- C) Send a follow-up request that includes the original context, the failed output, and the specific validation error ("finding 3 references src/util.ts, which is not in this diff"), asking the model to correct it.
- D) Regenerate the entire review from scratch with a different seed.

**Question 58.** Developers dismiss about 40% of the bot's findings, but you have no systematic way to learn which kinds of code constructs trigger the bad findings. What schema change enables this analysis?

- A) Add a free-text `notes` field where the model can explain its reasoning at length.
- B) Add a `reviewer_id` field so you can compare dismissal rates across model versions.
- C) Add a `confidence` field and assume dismissed findings were low-confidence.
- D) Add a `detected_pattern` field capturing which code construct triggered each finding, so dismissals can be aggregated and analyzed by pattern.

**Question 59.** An engineer proposes moving your agentic "generate tests, run them, fix failures, repeat" workflow to the Message Batches API for the 50% cost savings. Why won't this work?

- A) The Batch API does not support multi-turn tool calling within a request — it cannot execute your test-runner tool mid-request and return results to the model, which the iterative loop requires.
- B) The Batch API's 24-hour window is too slow for overnight jobs of this size.
- C) Batch requests cannot include system prompts, which the workflow depends on.
- D) The Batch API caps requests at a context size too small for test files.

**Question 60.** Your pipeline has the same Claude Code session generate a feature and then immediately review its own changes. The self-reviews rarely find problems, yet human reviewers regularly catch real bugs in the same code. What is the most effective fix?

- A) Add "review your work with fresh eyes and maximum skepticism" to the self-review prompt.
- B) Have a second, independent Claude instance — without the generator's reasoning context — perform the review.
- C) Enable extended thinking during the self-review step so the model reasons more deeply.
- D) Have the same session review the code three times and merge the findings.

---
# Answer Key — Practice Exam 1

**Quick key:** 1-B, 2-A, 3-D, 4-C, 5-B, 6-D, 7-B, 8-A, 9-C, 10-A, 11-D, 12-C, 13-B, 14-D, 15-A, 16-C, 17-A, 18-B, 19-D, 20-C, 21-A, 22-D, 23-B, 24-C, 25-A, 26-D, 27-B, 28-C, 29-A, 30-D, 31-B, 32-C, 33-A, 34-D, 35-B, 36-A, 37-C, 38-D, 39-A, 40-B, 41-D, 42-C, 43-A, 44-B, 45-C, 46-D, 47-A, 48-B, 49-C, 50-A, 51-D, 52-B, 53-C, 54-A, 55-D, 56-B, 57-C, 58-D, 59-A, 60-B

---

**1. B** — The agentic loop must key off `stop_reason`: continue while it is `"tool_use"` (execute tools, return results), stop at `"end_turn"`. Parsing natural-language signals (A) is exactly the anti-pattern producing the observed failures — text can look terminal while a tool call is pending. Iteration caps (C) are a safety backstop, not a primary stopping mechanism, and truncate legitimate long cases. D inverts the semantics: absence of text says nothing definitive about completion.

**2. A** — Tool results must be appended to the conversation history as a `tool_result` block referencing the `tool_use` ID, then the whole conversation is sent back so the model can incorporate the result into its next reasoning step. B keeps the result away from the model entirely — it can't confirm the refund. C misuses the system prompt for turn-level data. D destroys conversational state mid-task and is unnecessary here.

**3. D** — A `PostToolUse` hook deterministically normalizes heterogeneous formats before the model ever sees them, removing the error class entirely. Prompt instructions (A) rely on probabilistic per-turn conversions and will still fail occasionally. B is organizationally impractical and out of your control. C detects errors after they've influenced the conversation instead of preventing them.

**4. C** — A business rule with financial consequences needs deterministic enforcement: intercept the tool call, block amounts over $500, and redirect to escalation. Prompt salience (A), few-shot examples (B), and temperature (D) all still rely on probabilistic compliance — the observed 2% failure rate is precisely why prompt-only enforcement is insufficient here.

**5. B** — The recommended pattern is decomposing multi-concern requests into distinct items, investigating each in parallel with shared context, then synthesizing one unified resolution. A pushes work onto the customer. C escalates cases the agent could resolve, hurting first-contact resolution. D discards the shared context (customer identity, verification) that the concerns have in common.

**6. D** — Humans without transcript access need a structured handoff: customer ID, root cause analysis, amount, recommended action — everything needed to act immediately. A raw transcript (A) forces the human to reconstruct the case anyway, just from more text. B omits the case analysis entirely. C conveys mood, not the facts needed to resolve the dispute.

**7. B** — "Refunds only to the verified original payment method" is a hard compliance rule where any violation has financial/fraud consequences — the case for programmatic enforcement (a hook gating `process_refund`). Tone (A), conciseness (C), and offering alternatives first (D) are behavioral guidance where occasional imperfection is acceptable, so prompt instructions are appropriate.

**8. A** — This workload is explicitly high-ambiguity: the right tools and their order genuinely vary per case, and intermediate results (e.g., what `lookup_order` reveals) change what should happen next — the core argument for model-driven decision-making. B is false; you can hardcode sequences around the SDK. C is false in general (and irrelevant). D is false — decision trees can call any tool; that's not the issue.

**9. C** — Structured error metadata (`errorCategory`, `isRetryable`, description) gives the agent what it needs to retry transient failures and stop retrying non-retryable ones. Blanket retry (A) wastes calls on business errors and hides retry decisions from the agent. B asks the model to guess what the tool already knows. D reduces one error type's frequency without fixing the decision-making problem.

**10. A** — Business-rule violations should come back as structured errors with `retriable: false` and a customer-friendly explanation so the agent can communicate accurately and pivot to alternatives (store credit). B gives the agent nothing to reason with. C silently misrepresents a failure as success — the agent may tell the customer the refund happened. D leaks internals and buries the relevant fact (policy window) in noise.

**11. D** — "No orders" is a valid empty result of a successful query, not a failure; conflating the two causes exactly the observed misbehavior (apologizing, retrying). Errors should be reserved for access failures. A patches the symptom with prompt text while the contract stays broken. B hides real signal behind a hook. C invents a spurious recovery path for a non-error.

**12. C** — Keyword-sensitive system prompt instructions can create unintended tool associations that override even good tool descriptions — "any customer question about their purchases" is sweeping policy questions into `lookup_order`. A and D modify the tool when the tool isn't the problem. B adds token overhead to counteract an instruction you can simply fix at the source.

**13. B** — Growing from 4 to 18 tools on one agent increases decision complexity and degrades tool selection reliability. The fix is scoped tool access per role (or splitting into specialized agents). A and C describe nonexistent limits. D misdescribes how tool use works — agents don't call every available tool.

**14. D** — Forced tool selection (`tool_choice: {"type": "tool", "name": "classify_request"}`) on the first request is the only option that *guarantees* that specific tool runs first; later turns then proceed normally. A and C are probabilistic. B (`"any"`) guarantees *some* tool call, but not which one — the agent could call `get_customer` first.

**15. A** — Extracting transactional facts (amounts, dates, order numbers, statuses) into a persistent case-facts block that rides outside the summarized history is the recommended defense against progressive summarization degrading precise values into vague ones ("around $80"). B only delays the loss. C works but adds cost and latency on every turn for data that isn't changing. D pushes the system's memory problem onto the customer.

**16. C** — `~/.claude/CLAUDE.md` is user-level configuration: it applies to your account only and never travels through version control. Team-wide standards belong in a project-level CLAUDE.md committed to the repo. A misstates what `/memory` does (it inspects loaded memory; it doesn't "activate" anything). B — project CLAUDE.md loads without imports. D invents a failure mode.

**17. A** — `@import` keeps CLAUDE.md modular: each package's CLAUDE.md pulls in only the relevant shared standards files, and package maintainers with domain knowledge own the selection. B creates six diverging copies. C still loads all 900 lines every session — a table of contents doesn't reduce context. D makes standards invisible to Claude by default.

**18. B** — Inconsistent behavior across sessions is the classic symptom of different memory files being loaded in different sessions; `/memory` shows exactly which files are in effect, so diagnose before rewriting anything. A and D change content before you know whether content is the problem. C addresses context pressure, not configuration loading.

**19. D** — `context: fork` runs the skill in an isolated sub-agent context so its verbose output never enters (pollutes) the main conversation — only the useful summary returns. A reduces volume but the output still lands in the main context. B makes it worse: always-loaded verbosity. C restricts capability, not output destination.

**20. C** — `allowed-tools` in the skill frontmatter is the enforcement mechanism: restrict the skill to file-creation operations and Bash simply isn't available during execution. A is prompt-based and probabilistic — the failure already happened despite the skill's instructions. B mitigates damage rather than preventing it. D is false — slash commands don't disable tools.

**21. A** — Universal, always-applicable standards belong in CLAUDE.md (loaded every session); task-specific workflows used occasionally belong in skills (loaded on demand). B pays the release-notes workflow's context cost in every session. C means conventions only apply when someone remembers to invoke them. D is backwards on both counts.

**22. D** — A single-file, single-line fix with a stack trace pointing at the location is the textbook case for direct execution; plan mode (A), exploration subagents (B), and session forking (C) all add overhead with no decision-making or architectural payoff for a change this well-scoped.

**23. B** — The Explore subagent is designed for exactly this: verbose discovery runs in an isolated context and returns a summary, preserving the main conversation's context for the implementation phase. A still floods the main context between compactions. C trades context for guessing. D describes two unrelated sessions, not a shared-context workflow.

**24. C** — Concrete input/output examples are the most effective way to communicate expected transformations when prose is being interpreted inconsistently — they pin down the edge cases directly. A produces more prose subject to the same interpretation problem. B surfaces misunderstandings but doesn't pin down edge-case behavior the way examples do. D makes outputs consistent, not correct.

**25. A** — Context degradation in extended sessions (drifting to "typical patterns" instead of discovered specifics) is counteracted by persisting key findings to a scratchpad file and referencing it for subsequent questions — the findings survive outside degrading conversational context. B asks the model to fix a context problem with willpower. C repeatedly re-spends context and accelerates the problem. D delays symptoms without adding persistence.

**26. D** — Delegating specific investigation questions to subagents isolates the verbose file-dump output in their contexts, while the main agent keeps its context for high-level coordination. A and C sacrifice the understanding you actually need. B is unrelated — `max_tokens` governs response length, not context accumulation.

**27. B** — `/compact` summarizes the conversation to reduce context usage while preserving key information — the right mid-session relief valve when you need to keep working. A discards the findings (Claude has no cross-session memory of them). C frees trivial space and drops your standards. D describes behavior that doesn't exist.

**28. C** — The reliable pattern is summarizing key findings from the completed phase and injecting the relevant summary into each subagent's initial context. A fails because subagents do not inherit parent context automatically. B re-spends a week of analysis. D floods each subagent's context with mostly-irrelevant transcript, inviting lost-in-the-middle problems.

**29. A** — Structured state persistence is the crash-recovery pattern: each agent exports completed work and key findings to a known location; on resume the coordinator loads the manifest and injects state into agent prompts, resuming rather than restarting. B and D reduce crash odds but don't recover from one. C doubles cost for a coin-flip.

**30. D** — This is the lost-in-the-middle effect: models reliably process the beginning and end of long inputs but may omit middle sections. The mitigation is a key-findings summary up front plus explicit section headers organizing the detail. A changes ordering without addressing position effects. B — instructions don't fix attention position biases. C — the effect persists in larger windows.

**31. B** — The coordinator should analyze query requirements and dynamically select which subagents to invoke; simple factual queries shouldn't traverse the full pipeline. A only helps repeated queries. C makes every stage worse instead of skipping unneeded stages. D adds a fifth stage to a pipeline whose problem is mandatory stages.

**32. C** — Subagents operate with isolated context: they do not inherit the coordinator's conversation history. The synthesis prompt must include the actual search results and analysis outputs. A would deepen prose style but can't conjure data the agent never received. B misunderstands isolation — window size is irrelevant if the content is never passed. D is contradicted by the logs: nothing was passed at all.

**33. A** — Parallel subagents are spawned by emitting multiple Task tool calls in a single coordinator response, rather than one per turn. B bolts external infrastructure onto a problem the SDK pattern already solves. C serializes the work inside one context and loses parallelism. D — streaming affects token delivery, not tool-call concurrency.

**34. D** — The Task tool is the mechanism for spawning subagents; if `"Task"` isn't in the coordinator's `allowedTools`, it cannot delegate and will attempt the work itself. A affects selection quality among subagents, not the total inability to spawn. B and C describe requirements that don't exist.

**35. B** — Hub-and-spoke routing through the coordinator is what provides observability, consistent error handling, and controlled information flow; a direct side channel sacrifices all three. A invents a token penalty. C is false — you could build it, it's just a bad idea. D is a side detail, not the main architectural argument.

**36. A** — Coverage gaps are addressed with an iterative refinement loop: the coordinator evaluates synthesis output for gaps, re-delegates targeted queries, and re-invokes synthesis until coverage is sufficient. B adds volume, not targeted coverage. C asks for length — the missing material was never gathered. D still makes a single pass with no gap-checking.

**37. C** — Partitioning research scope — assigning each agent distinct subtopics or source types — prevents duplication at the source. B deduplicates after the tokens and analysis time are already spent. A gives up the parallelism that motivated two agents. D serializes the agents, also defeating parallelism.

**38. D** — Coordinator prompts should specify research goals and quality criteria rather than step-by-step procedures, enabling subagents to adapt their approach to each topic. A and B double down on rigid proceduralism — there will always be topics outside the script. C removes direction entirely; goals and quality bars are still needed.

**39. A** — Tool descriptions are the primary mechanism for tool selection; near-identical names and descriptions cause misrouting. Renaming to purpose-specific names and rewriting descriptions (purpose, inputs, outputs, when-to-use-vs-the-other) fixes the root cause. B papers over ambiguity with a default. C may discard needed functionality. D corrects symptoms downstream and needs its own routing logic — the very thing that's broken.

**40. B** — A generic tool with mode switches invites wrong-mode calls; splitting into purpose-specific tools (`extract_data_points`, `summarize_content`, `verify_claim_against_source`) with clear contracts makes selection explicit. A keeps the confusing single entry point. C substitutes a silent wrong behavior for an error. D makes behavior unpredictable and undebuggable.

**41. D** — Agents with tools outside their specialization tend to misuse them; the synthesis agent's job is to work from provided findings, so search tools should be removed from its set (scoped tool access). A is probabilistic and the misuse is already happening. B doesn't remove the capability. C flags damage after publication instead of preventing it.

**42. C** — MCP resources exist to expose content catalogs — giving agents visibility into available data without exploratory tool calls. A makes the waste cheaper, not gone. B is a manual, drift-prone copy of what resources provide natively. D speeds up the overhead instead of eliminating it.

**43. A** — Replacing the generic `fetch_url` with a constrained `load_document` that validates URLs against the vetted library makes the boundary structural rather than behavioral. B relies on prompt compliance. C detects violations after they've contaminated research. D doesn't address capability at all.

**44. B** — Attribution survives only if subagents emit structured claim-source mappings (claim, source, excerpt) and the synthesis agent is required to preserve and merge them; prose summarization is where provenance dies. A fabricates citations after the fact — worse than none. C lists sources without linking claims to them. D relies on memory of information that was already compressed away.

**45. C** — Conflicting statistics from credible sources should be presented with explicit conflict annotation, source attribution, and methodological context — not resolved arbitrarily. A invents a number no source reported. B assumes recency explains the difference (it may be methodology or scope). D throws away material information the reader needs.

**46. D** — `--output-format json` with `--json-schema` produces machine-parseable, schema-conforming output — the supported mechanism for structured findings in CI. A and B keep betting on format stability that prose output doesn't guarantee. C abandons the inline-comment requirement rather than meeting it.

**47. A** — The documented pattern for re-reviews: include prior findings in context and instruct Claude to report only new or still-unaddressed issues, avoiding duplicate comments. B misses issues that new commits introduce in interaction with unchanged files. C recreates comment noise and destroys discussion threads. D leaves post-push changes unreviewed.

**48. B** — CLAUDE.md is the mechanism for giving CI-invoked Claude Code project context: testing standards, what makes a test valuable, and which fixtures exist. Without it the generator can't know your conventions. A generates waste then filters it. C injects imports into tests that still don't use the factories meaningfully. D narrows scope without improving quality within it.

**49. C** — General instructions like "be conservative" or "high-confidence only" demonstrably fail to improve precision; explicit categorical criteria — report these types, skip those types — are what work. A is more of the same failed approach. D relies on self-reported confidence, which is poorly calibrated. B doubles cost and still lacks defined criteria for either reviewer.

**50. A** — One high-false-positive category undermines trust in all categories. Temporarily disabling the 70%-FP performance category restores signal quality immediately while you improve its prompts offline. B, C, and D all keep the noise flowing in some form, and trust continues eroding.

**51. D** — Consistent classification comes from explicit severity criteria with concrete code examples for each level. A makes every nitpick merge-blocking. B is self-review with no standard to check against. C is too coarse — not all security findings are critical, and category ≠ impact.

**52. B** — When detailed instructions alone produce inconsistent output, few-shot examples demonstrating the exact desired format (location, issue, severity, suggested fix) are the most effective technique for consistency. A repeats what already isn't working. C addresses truncation, which isn't the symptom. D adds cost and a second chance for drift.

**53. C** — Few-shot examples contrasting acceptable intentional patterns with genuine issues let the model generalize the judgment to novel cases — exactly what an enumerated list (D) can't do. A suppresses real bugs involving catch blocks. B requires annotating the whole codebase and doesn't help with new code.

**54. A** — Tool use with a JSON schema is the most reliable path to structured output: the `report_findings` tool's input schema guarantees well-formed structure, eliminating the JSON-in-text syntax errors. B and D are recovery layers for a problem you can eliminate outright. C trades one fragile text format for another.

**55. D** — `tool_choice: "any"` guarantees the model calls *a* tool while leaving it free to pick the appropriate one (`report_findings` vs `approve_pr`). A forces every response through `report_findings`, breaking approvals. B is probabilistic — the failure already occurs despite instructions. C is sentiment-parsing fragility replacing a structural guarantee.

**56. B** — Strict schemas via tool use eliminate *syntax* errors but not *semantic* errors — wrong line numbers and contradictory severities are semantically wrong, schema-valid outputs. The fix is semantic validation layered on top. A — a bounded range can't know which line is correct. C misdiagnoses; truncated output would fail schema validation. D throws away the syntax guarantee to fix nothing.

**57. C** — Retry-with-error-feedback: include the original context, the failed output, and the specific validation error so the model can self-correct. An identical retry (A) has no new information and will likely fail identically. B silently loses a possibly-real finding that referenced the wrong file. D discards all the valid findings along with the invalid one.

**58. D** — A `detected_pattern` field records which code construct triggered each finding, enabling systematic aggregation of dismissals by pattern — the feedback loop you're missing. A gives unstructured text you can't aggregate. B varies the wrong dimension. C assumes the correlation you're trying to measure.

**59. A** — The Batch API does not support multi-turn tool calling within a request: it cannot pause mid-request, execute your test-runner tool, and feed results back to the model. An iterative generate-run-fix loop is inherently multi-turn tool use. B is backwards — overnight jobs are the Batch API's sweet spot. C and D describe restrictions that don't exist.

**60. B** — A model reviewing its own generation retains the reasoning context that produced the code, making it unlikely to question its own decisions. An independent instance without that context is more effective at catching subtle issues. A and C try to prompt or think around a structural bias. D repeats the biased review three times.

---

*End of Practice Exam 1.*
