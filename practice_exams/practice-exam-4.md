# CCAFC Practice Exam 4

**Claude Certified Architect – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Customer Support Agent, Multi-Agent Research, Developer Productivity, Claude Code for CI/CD) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (matches the official weightings): D1 Agentic Architecture ×16, D2 Tool Design & MCP ×11, D3 Claude Code Configuration ×12, D4 Prompt Engineering & Structured Output ×12, D5 Context Management & Reliability ×9.

Answer key with explanations is at the end.

---

## Scenario A: Customer Support Resolution Agent (Questions 1–15)

You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues, with custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Your target is 80%+ first-contact resolution while knowing when to escalate.

---

**Question 1.** Your loop executes the agent's tool calls but the next API request fails with a 400 error complaining about `tool_use` blocks that have no corresponding `tool_result` blocks. What did the implementation skip?

- A) Setting `tool_choice: "auto"` on the follow-up request.
- B) Clearing the previous assistant message before sending the new request.
- C) Re-registering the tool definitions on every request.
- D) Appending each executed tool's result to the conversation as a `tool_result` block (matched to its `tool_use` ID) before sending the next request.

**Question 2.** Gift-card purchases are non-refundable by policy; the agent should route those customers to a goodwill-credit workflow instead. The rule lives in the system prompt today, and violations still occur monthly. What is the correct mechanism?

- A) Add gift-card examples to the few-shot section of the prompt.
- B) Intercept `process_refund` calls with a hook that blocks refunds on gift-card line items and redirects the agent to the goodwill-credit workflow.
- C) Add a second model that reviews each refund decision before execution.
- D) Move the gift-card rule into the `process_refund` tool description.

**Question 3.** Account email changes must be preceded by a completed identity verification in the same conversation. Reviewing incidents, you find the agent occasionally performs the change when a persuasive customer insists verification "already happened last week." What prevents this?

- A) A programmatic prerequisite gate: `update_email` is blocked unless an identity-verification step has actually completed in the current session, regardless of what the conversation claims.
- B) A system prompt instruction to never trust customer claims about prior verification.
- C) Few-shot examples of the agent politely refusing unverified email changes.
- D) A daily audit report of email changes for the fraud team.

**Question 4.** A billing dispute arrives with symptoms that don't match any known pattern — the charge exists in one system but not another. There is no established runbook. How should the agent approach the investigation?

- A) Follow the standard billing-dispute script; consistency matters more than fit.
- B) Escalate immediately, since no runbook exists.
- C) Use an adaptive investigation plan — form a hypothesis, run a lookup, and let each finding determine the next step, rather than executing a fixed sequence.
- D) Run every available lookup tool once, then decide.

**Question 5.** A support case is reopened the next morning through a new chat. Yesterday's session contains extensive tool results (order status, refund state) that may have changed overnight, plus the negotiated resolution details. How should the agent be initialized?

- A) Resume yesterday's session unchanged — continuity matters most.
- B) Resume yesterday's session and instruct the agent to distrust any tool results.
- C) Start fresh with no context and let the customer re-explain.
- D) Start a new session injecting a structured case summary (customer ID, agreed resolution, amounts, status as of yesterday), and re-run lookups for anything time-sensitive — a fresh session with a summary beats resuming atop stale tool results.

**Question 6.** You maintain four agent behavior requirements. Three are enforced with hooks. Which one is appropriately left to system-prompt guidance alone?

- A) Responses should acknowledge the customer's frustration before presenting solutions.
- B) Refunds above $500 must be approved by a human.
- C) Identity must be verified before account mutations.
- D) Refunds must go only to the original payment method.

**Question 7.** The agent calls `lookup_order` with the date "next Tuesday" in a field expecting `YYYY-MM-DD`. How should the tool respond so the agent can recover in one step?

- A) `isError` with a generic "invalid request" so the agent tries something else.
- B) A structured validation error naming the field, stating the expected format (`YYYY-MM-DD`), and marking the error as correctable — so the agent can fix the input and re-call.
- C) Silently interpret "next Tuesday" server-side using the current date.
- D) A transient-category error so the agent retries the same call.

**Question 8.** Customers asking for exchanges keep getting refunds — the agent calls `process_refund` because nothing tells it that exchanges are handled elsewhere. What is the highest-leverage change?

- A) Rename `process_refund` to `process_refund_not_exchange`.
- B) Block exchange-context refunds with a hook and let the error teach the agent.
- C) State the boundary in the `process_refund` description: what it is for, and explicitly that exchanges are out of scope — directing the agent to the `create_exchange` tool instead.
- D) Merge refunds and exchanges into one `resolve_return` tool.

**Question 9.** After a quarter of feature growth, the resolution agent now has 17 tools spanning refunds, subscriptions, loyalty, shipping, and marketing consent. Selection errors have risen steadily with each addition. What is the architectural correction?

- A) Scope tool access by role — split the surface into specialized agents (or route by concern), giving each only the 4–6 tools its role needs.
- B) Sort the tools array by usage frequency so common tools are found first.
- C) Add a mandatory reasoning step before every tool call.
- D) Shorten all tool descriptions so the full list fits in less context.

**Question 10.** Your team needs standard Zendesk operations (create ticket, add note, change status) available to the agent. An engineer has begun writing a custom MCP server for it. What guidance applies?

- A) Continue — support tooling is too business-critical for community code.
- B) Skip MCP and call Zendesk's REST API from a hook.
- C) Wrap Zendesk's API in your existing backend and expose one mega-tool.
- D) Use an existing community MCP server for a standard integration like Zendesk; reserve custom server effort for workflows unique to your team.

**Question 11.** A platform wrapper catches all tool exceptions and returns `{}` with a success status "to keep conversations smooth." Yesterday the agent told a customer their refund was complete when `process_refund` had actually thrown. What is the design lesson?

- A) Wrappers should return `null` rather than `{}` so failures are detectable.
- B) The agent should verify refunds with a follow-up lookup after every attempt.
- C) Suppressing errors by disguising failures as successes is an anti-pattern — failures must surface as structured errors so the agent can respond truthfully and recover.
- D) The wrapper needs better logging so engineers catch these incidents sooner.

**Question 12.** A customer writes: "This is the THIRD time I'm contacting you people about this broken blender!!" The issue is a standard damage replacement with photo evidence — fully within the agent's capability. Sentiment analysis scores the message as highly negative. What should the agent do?

- A) Escalate to a human immediately — high negative sentiment indicates a case the bot shouldn't touch.
- B) Acknowledge the frustration and the repeated contact, then offer to resolve the replacement right now — escalating only if the customer asks for a human.
- C) Offer a discount code first to defuse the sentiment before addressing the issue.
- D) Process the replacement silently without addressing the tone.

**Question 13.** A customer requests a price match against a competitor's advertised price. Your published policy covers price adjustments for your own site's price drops but says nothing about competitor matching. The agent should:

- A) Apply the own-site adjustment policy by analogy, since it is the closest rule.
- B) Decline the request, since the policy does not authorize competitor matching.
- C) Ask the customer for a screenshot and decide based on the price difference.
- D) Escalate — the policy is silent on this request, and policy gaps are an escalation trigger rather than something to resolve by improvisation.

**Question 14.** `get_customer` returns three accounts for "Chris Martin" — different addresses, one shared phone number. The agent currently picks the account with the most recent order. What should it do instead?

- A) Ask the customer for an additional identifier (order number, email on the account, billing zip) and match on that — multiple matches require clarification, not heuristic selection.
- B) Pick the account matching the phone number the customer wrote in from.
- C) Merge the three accounts, since they likely belong to one person.
- D) Proceed with the most recent account but flag the conversation for review.

**Question 15.** In sessions where a customer raises several issues, the agent confuses details between them as the conversation grows — attributing order 8817's status to order 9902's refund. What is the recommended context structure?

- A) Limit customers to two issues per conversation.
- B) Repeat all issue details in every agent response so they stay in recent context.
- C) Extract and persist each issue's structured data (order ID, amount, status, next action) into a separate context layer maintained outside the conversational history, keyed by issue.
- D) Handle issues strictly one at a time, refusing to discuss an issue until the previous one closes.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Reports on "the impact of remote work" consistently cover only the technology industry; healthcare, education, and manufacturing never appear. The coordinator's decomposition logs show subtasks like "remote work in software companies" and "developer productivity at home." What is the fix?

- A) Instruct the search agent to broaden every query it receives with additional industries.
- B) Improve the coordinator's decomposition: have it first enumerate the topic's major domains/dimensions, then create subtasks against that enumeration, with coverage criteria to validate the decomposition before delegating.
- C) Add a fourth subagent dedicated to industries the others miss.
- D) Have the synthesis agent pad the report with general knowledge about other industries.

**Question 17.** Each subagent currently posts its findings directly into a shared results channel, and the report agent assembles whatever it finds there. Findings arrive out of order, some overwrite others, and nobody detects missing pieces. Which component should own result collection, and why?

- A) The report agent, since it consumes the results anyway.
- B) The shared channel, upgraded with ordering and dedup logic.
- C) Each subagent should verify its own delivery with a read-back check.
- D) The coordinator — aggregation is a coordinator responsibility in hub-and-spoke designs, giving one place for completeness checks, ordering, and error handling before anything reaches synthesis.

**Question 18.** After an expensive shared analysis of a 400-document corpus, you want to evaluate two competing report frameworks — thematic versus chronological — each developed independently from that same analysis. What mechanism does the Agent SDK provide?

- A) `fork_session` — create two independent branches from the shared analysis baseline and develop one framework in each.
- B) `--resume` the analysis session twice, once per framework.
- C) Run the analysis twice in two fresh sessions, one per framework.
- D) Develop both frameworks alternately within the single session.

**Question 19.** Your system produces (a) a weekly market digest with the same six sections every week, and (b) ad-hoc deep investigations of novel questions. How should the two pipelines be decomposed?

- A) Both dynamic — research is inherently unpredictable.
- B) Both fixed — consistency simplifies operations.
- C) The weekly digest as a fixed prompt chain (predictable, repeating stages); the ad-hoc investigations with dynamic decomposition that adapts to what each step uncovers.
- D) The digest dynamic and the investigations fixed, since digests have more room for creativity.

**Question 20.** Monday's run must gather updates from six independent news domains before synthesis. The coordinator currently delegates them one per turn. What single change most reduces wall-clock time?

- A) Cache Friday's results and only fetch weekend changes.
- B) Have the coordinator emit all six Task tool calls in one response so the subagents execute in parallel.
- C) Reduce each domain's search depth so sequential runs finish faster.
- D) Move synthesis earlier so it overlaps with the last two searches.

**Question 21.** A reviewer flags this coordinator code: `if "DONE" in assistant_text: break` — paired with a system prompt instructing the model to "say DONE when research is complete." What is the professional assessment?

- A) Acceptable — explicit completion markers are a common convention.
- B) The marker should be more unusual (e.g., "##COMPLETE##") to avoid false positives.
- C) The prompt and check should both use a JSON field rather than a bare string.
- D) Loop termination should key off `stop_reason` (`"end_turn"`), not a natural-language marker that can appear spuriously, be paraphrased away, or be echoed mid-task.

**Question 22.** Researching an extremely niche topic, the search subagent's query legitimately matches nothing. The tool returns an error, and the coordinator logs "search infrastructure degraded" and switches to a fallback provider — wasting a cycle. What is the correct contract?

- A) Zero matches is a successful query with an empty result set and should be returned as such; error responses are reserved for access failures — the two must be distinguishable.
- B) The tool should return the closest partial matches instead of nothing.
- C) The coordinator should ping a health-check endpoint before interpreting errors.
- D) Empty results and failures can share a response shape if the log message differs.

**Question 23.** Your `search_corpus` tool truncates queries over 256 characters — silently. Agents regularly compose long, careful queries whose critical qualifiers get cut off, returning oddly irrelevant results no one can explain. Beyond fixing the truncation, what should the tool description have included?

- A) A version number so agents know the tool's behavior may change.
- B) Usage statistics showing typical query lengths.
- C) The input constraint and edge-case behavior — maximum query length and what happens beyond it — so the agent composes queries that fit (descriptions should document formats, limits, and edge cases).
- D) A warning that search quality varies by topic.

**Question 24.** The document analysis agent has access to a purpose-built `arxiv_search` MCP tool but keeps using the generic built-in WebSearch for academic queries, returning blog summaries instead of papers. `arxiv_search`'s description is "Searches arXiv." What is the recommended fix?

- A) Remove WebSearch from the agent so arxiv_search wins by default.
- B) Enhance the `arxiv_search` description — what it searches, what it returns (paper metadata, abstracts, full-text links), and when it should be preferred over general web search for academic material.
- C) Add a system prompt rule to always use arxiv_search for anything containing the word "paper."
- D) Lower WebSearch's priority via tool ordering.

**Question 25.** The document analysis agent abandons its entire assignment the first time a PDF-parsing call times out, reporting total failure to the coordinator even when 9 of 10 documents parsed fine. What error-handling design is missing?

- A) A longer parsing timeout so failures stop happening.
- B) A coordinator-side retry of the whole document analysis task.
- C) Parallel parsing so one timeout doesn't serialize the rest.
- D) Local recovery in the subagent: retry the transient parse failure with backoff, and if it still fails, continue with the other documents — propagating to the coordinator only what it couldn't resolve, alongside the partial results.

**Question 26.** While analyzing a corpus, the analysis agent finds two credible papers reporting incompatible efficacy figures. It currently discards the outlier and reports one clean number. What should it do instead?

- A) Report the average with a wide confidence interval.
- B) Hold both papers back from synthesis until a human adjudicates.
- C) Complete the analysis with both values included and explicitly annotated (source, methodology), letting the coordinator decide how to reconcile before synthesis — value selection is not the analysis agent's call.
- D) Re-run the analysis with instructions to prefer the more recent paper.

**Question 27.** The synthesis agent regularly misdates events and attributes findings to the wrong methodology. Upstream, the analysis agent's outputs are well-written prose summaries. What structural requirement fixes this?

- A) Require the analysis agent to emit structured outputs carrying metadata with every finding — publication dates, source locations, methodological context — that synthesis can rely on instead of inferring from prose.
- B) Give the synthesis agent web search access to verify dates itself.
- C) Have the synthesis agent flag any date it is unsure about.
- D) Use a stronger model for synthesis so it infers metadata more accurately.

**Question 28.** Your synthesis agent's context budget is small, and upstream agents currently send it full document excerpts plus their complete reasoning narratives. Synthesis truncates and quality collapses on large topics. What is the recommended change?

- A) Rotate synthesis across three agents, each taking a third of the material.
- B) Modify the upstream agents to return structured data — key facts, citations, relevance scores — rather than verbose content and reasoning chains, sized for the downstream consumer's budget.
- C) Raise the synthesis agent's budget and accept the cost.
- D) Have synthesis summarize its input first, then synthesize the summary.

**Question 29.** A source paper carefully describes its results as "preliminary findings from a small pilot (n=12)." The final report states the same results as established fact. Where should this be prevented?

- A) In report review — a final pass that re-checks every claim against sources.
- B) By excluding pilot studies from research entirely.
- C) By having the search agent rank small studies lower.
- D) In the structured findings passed downstream — subagents must preserve the source's own characterization and methodological context (preliminary, n=12) with the claim, and synthesis must carry these qualifiers through rather than flattening them.

**Question 30.** Your overnight research runs sometimes die partway (provider outages). Restarting from zero wastes hours of completed subagent work. What recovery design does the guide recommend?

- A) Each agent exports structured state (completed subtasks, findings) to a known location as it works; on resume, the coordinator loads a manifest of these exports and injects the prior state into agent prompts.
- B) Wrap the whole run in a retry loop with exponential backoff.
- C) Run two identical pipelines in parallel and keep whichever finishes.
- D) Schedule runs during the provider's historically most stable hours.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You resume yesterday's architecture-investigation session. Overnight, one teammate's PR merged, refactoring the two authentication modules the session had analyzed; nothing else changed. What is the efficient continuation?

- A) Start a new session — any change invalidates a session.
- B) Resume and let the agent notice the changes when it next reads those files.
- C) Resume the session and tell the agent specifically that the two auth modules changed in PR #412, asking it to re-analyze just those files — targeted re-analysis, not full re-exploration.
- D) Resume and re-run the entire investigation to be safe.

**Question 32.** Which loop skeleton is correct for an Agent SDK/API tool-use loop?

- A) `while response.content contains text: send(...)`
- B) `while response.stop_reason == "tool_use": execute tools; append results; send(...)` — exiting when `stop_reason` is `"end_turn"`.
- C) `for i in range(MAX_STEPS): send(...)` — with MAX_STEPS as the completion condition.
- D) `while not response.text.endswith("."): send(...)`

**Question 33.** Your agent uses three file-related MCP tools from different vendors: one returns absolute paths, one repo-relative paths, one `file://` URIs. The agent regularly treats the same file as three different files. What is the cleanest fix?

- A) Add a system prompt table explaining each vendor's path convention.
- B) Standardize on one vendor's tools and drop the others.
- C) Instruct the agent to canonicalize paths before comparing them.
- D) A `PostToolUse` hook that normalizes all paths to one canonical form before the model sees the results.

**Question 34.** Your doc-writer subagent's AgentDefinition grants the full toolset. Last week it ran `npm run build` "to verify the docs examples compile," consuming twenty minutes. Its actual job needs only Read, Grep, and Write. Where is the fix made?

- A) In the subagent's AgentDefinition — restrict its tools to those its role requires (Read, Grep, Write); tool restrictions per subagent type are part of the definition.
- B) In the doc-writer's system prompt: "do not run builds."
- C) In the coordinator, which should watch subagent tool calls and cancel long ones.
- D) In CI, which should reject doc PRs that took too long to produce.

**Question 35.** A stack trace shows the error string "connection pool exhausted" but the codebase is unfamiliar and you don't know which module raises it. What is the right first tool call?

- A) Glob for `**/pool*` and read what matches.
- B) Read the database configuration files first.
- C) Grep the codebase for the error message string — content search is how you locate where a string is raised.
- D) Bash `git log --grep "pool"` to find related commits.

**Question 36.** The agent must change one occurrence of a YAML block that appears, byte-identical, five times in a generated config file. Edit keeps failing on non-unique anchor text. What is the reliable approach?

- A) Widen the anchor to include surrounding lines until it's unique — and if no unique anchor exists, fall back further.
- B) Read the file, then Write it back with the single intended occurrence modified — the documented fallback when Edit cannot anchor uniquely.
- C) Edit with `replace_all`, then revert the four unwanted changes with four more Edits.
- D) Delete the file and regenerate it from the template with the change applied.

**Question 37.** You put your personal preferences — two-space indent debates, your favorite commit-message style — into the project's CLAUDE.md. Teammates are now complaining that Claude nags them about your preferences. Where do personal preferences belong?

- A) In a `.claude/rules/` file scoped to files you own.
- B) In the project CLAUDE.md, but prefixed with your name so others can ignore them.
- C) In a skill only you invoke.
- D) In your user-level `~/.claude/CLAUDE.md` — user scope applies only to you and never travels to teammates through the repo.

**Question 38.** Your `/analyze-arch` skill only ever needs to read code and produce a report, but during one run it executed `git push` from a leftover instruction in its prompt file. Beyond fixing the prompt, what structural control applies?

- A) Configure `allowed-tools` in the skill frontmatter to a read-only set — with no execution tools available, no prompt bug can run `git push`.
- B) Add a pre-run confirmation step where the developer approves the skill's plan.
- C) Have the skill run `git stash` first so pushes contain nothing.
- D) Move the skill to user scope so mistakes affect only one person.

**Question 39.** A new engineer clones the repo, opens Claude Code, and types `/deploy-check` — the team's pre-deployment verification command — and it works immediately with no setup. What makes this possible?

- A) The command was installed globally by the infrastructure team's laptop image.
- B) The command is defined in `.claude/commands/` in the repository — project-scoped commands travel through version control and are available on clone.
- C) Claude Code synced the command from the previous engineer's account.
- D) `/deploy-check` is a built-in Claude Code command.

**Question 40.** Your SQL conventions (naming, mandatory `WHERE` review for deletes, migration header format) should apply whenever Claude edits any `.sql` file — they sit in `db/`, `analytics/`, and various service folders. What is the correct configuration?

- A) A CLAUDE.md in `db/`, the largest SQL directory.
- B) The root CLAUDE.md with a "SQL rules" section.
- C) A `.claude/rules/` file with frontmatter `paths: ["**/*.sql"]` — glob-scoped rules load exactly when matching files are edited, wherever they live.
- D) A `/sql-mode` skill developers invoke before database work.

**Question 41.** The ask: add a validation check rejecting end dates earlier than start dates in one form handler — a well-understood, single-function change. Which workflow?

- A) Plan mode, then implementation — dates are subtle.
- B) An Explore subagent to survey date handling repo-wide first.
- C) `fork_session` to test two validation styles independently.
- D) Direct execution — simple, well-scoped changes with a clear location don't warrant planning overhead.

**Question 42.** You're replacing the ORM across a service — 45+ files, three plausible migration strategies with different transaction semantics, and rollback implications. Which workflow?

- A) Plan mode first: explore the codebase, compare the three strategies, and commit to a design before edits — architectural scope and multiple valid approaches are exactly its criteria.
- B) Direct execution, since each individual file's change is mechanical once begun.
- C) Direct execution with `--resume` checkpoints after every ten files.
- D) Delegating the whole migration to a single subagent to keep the main context clean.

**Question 43.** You're implementing a rate limiter but haven't decided on the algorithm, burst policy, or what happens to rejected requests — and you suspect there are failure modes you haven't considered. What gets you the best design conversation?

- A) Ask Claude for the industry-standard rate limiter and implement that.
- B) Write your best-guess spec and have Claude critique it.
- C) Use the interview pattern — have Claude ask you questions (traffic shape, burst tolerance, rejection semantics, distributed-state failure modes) to surface the decisions before implementation.
- D) Implement token-bucket first and iterate based on production behavior.

**Question 44.** Claude keeps misinterpreting your description of a log-line transformation ("extract the request ID and normalize the timestamp — you know, standard format"). Three attempts, three different behaviors. What input finally pins it down?

- A) A glossary defining "request ID," "normalize," and "standard format."
- B) Two or three concrete example pairs: actual input log lines and the exact output line expected for each — including one edge case.
- C) A longer description written with RFC-style MUST/SHOULD language.
- D) A link to the logging library's documentation.

**Question 45.** Security standards used by all six packages in your monorepo live in `standards/security.md`. Each package has its own CLAUDE.md. How do packages include the shared standards without copying them?

- A) Symlink `security.md` into each package directory.
- B) Paste the content into each package CLAUDE.md and update all six on changes.
- C) Mention in each CLAUDE.md that a security standards file "exists in the repo."
- D) Use `@import` in each package's CLAUDE.md to reference `standards/security.md` — one source of truth, included wherever it applies.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** A nightly cron job needs Claude Code to summarize the day's merged changes and write the summary to a file. Which flag makes the invocation suitable for cron?

- A) `-p` (`--print`) — process the prompt, print the result, and exit without waiting for interactive input.
- B) `--cron`, which registers the command with the scheduler.
- C) `--quiet`, which suppresses the interactive UI.
- D) `--yes`, which auto-confirms all interactive prompts.

**Question 47.** Developers complain that after each push, the review bot re-posts its full findings list, burying the thread. The findings are usually the same unresolved items plus one or two new ones. What re-review design fixes the noise?

- A) Only run the bot once per PR, on first open.
- B) Have the bot delete its old comments before posting the new full list.
- C) Feed the prior findings into the re-review context with instructions to post only new findings and note which prior ones remain unaddressed — never re-posting duplicates.
- D) Post all findings into a single continuously-edited summary comment.

**Question 48.** Your pipeline must transform Claude's review findings into your internal defect-tracker format. The transformation code needs guaranteed field names and types from Claude's output. Which invocation provides that?

- A) `claude -p "..." | jq` with defensive null checks for missing fields.
- B) `claude -p "..." --output-format json --json-schema findings-schema.json` — schema-enforced structured output for machine parsing.
- C) `claude -p "..." --strict` to enable careful output mode.
- D) `claude -p "..."` with a prompt instruction to "output valid JSON matching our schema."

**Question 49.** Your comment-accuracy checker flags dozens of harmless doc comments per PR ("this comment could be more precise"). You want it to flag only real problems. Which criterion should replace the current "check that comments are accurate" instruction?

- A) "Only flag comments you are highly confident are wrong."
- B) "Flag at most three comments per pull request."
- C) "Prefer flagging comments on public APIs over internal helpers."
- D) "Flag a comment only when its claimed behavior contradicts what the code actually does" — a specific, categorical criterion rather than an open-ended accuracy judgment.

**Question 50.** Metrics show your security-review category is highly accurate, but the style category floods PRs with noise. A teammate argues style can wait since security "is what matters." Why does the guide say the style noise is urgent anyway?

- A) High false-positive categories erode developer trust in the whole tool — developers who learn to ignore style findings start ignoring the accurate security findings too.
- B) Style issues compound into security issues over time.
- C) Noise increases token costs, which dominate the tool's budget.
- D) The style category's noise statistically hides the security findings in long lists.

**Question 51.** Your CI bot has three response tools: `comment_inline`, `open_issue`, and `request_changes`. For clear-cut cases it chooses well, but for ambiguous ones (a real bug that's out of the PR's scope; a severe issue in unchanged code) it picks inconsistently. What most improves these decisions?

- A) A decision matrix in prose mapping issue attributes to tools.
- B) Removing `open_issue` so there are fewer choices.
- C) A few targeted few-shot examples of exactly these ambiguous cases, each showing the chosen tool *and the reasoning* why it beat the plausible alternatives.
- D) Making `request_changes` the default for any uncertainty.

**Question 52.** You want every PR summary the bot posts to follow the same five-column markdown table. Instructions describing the table produce close-but-drifting variants (merged columns, extra sections). What reliably locks the format?

- A) A markdown linter that rejects malformed summaries and triggers regeneration.
- B) Lowering temperature to reduce formatting creativity.
- C) A stricter prose description of the table with column widths specified.
- D) Few-shot examples showing complete, exact sample summaries in the required table format — demonstration beats description for format consistency.

**Question 53.** Which statement about `tool_choice` is correct?

- A) `"auto"` guarantees at least one tool call per response.
- B) With `"auto"` the model may respond with text and no tool call; `"any"` forces some tool call but leaves the choice of tool to the model; `{"type": "tool", "name": ...}` forces one specific tool.
- C) `"any"` lets the model call any number of tools, while `"auto"` limits it to one.
- D) Forced tool selection applies to every subsequent turn until reset.

**Question 54.** Developers dismiss many of the bot's test-generation suggestions, and you want to learn systematically which kinds of code constructs produce the unwanted suggestions. What enables that analysis?

- A) A `detected_pattern` field in each suggestion's structured output identifying the construct that triggered it — dismissals can then be aggregated by pattern.
- B) Exit interviews with developers who dismiss the most suggestions.
- C) A dashboard of dismissal counts by repository.
- D) Free-form "reason for dismissal" text boxes, reviewed monthly.

**Question 55.** The review bot's finding — "this implementation may not match the approved design" — fails validation because it cites a design document the bot was never given. Will retry-with-error-feedback resolve it?

- A) Yes — the validation error will make the bot reason more carefully about the design.
- B) Yes, if the retry also raises `max_tokens` for deeper analysis.
- C) No — the design document is absent from the input; retries can't recover information that was never provided. Supply the document in context, or scope the review to what's available.
- D) No — findings referencing external documents should be auto-deleted.

**Question 56.** Two jobs are proposed for the Message Batches API: (1) a nightly "explain every lint suppression in the repo" report read weekly; (2) the PR-blocking security gate developers wait on before merging. Evaluate.

- A) Both fit — the 50% savings applies to both equally.
- B) Neither fits — CI workloads need real-time APIs across the board.
- C) Job 2 fits better, since security scans are heavier and benefit more from discounts.
- D) Job 1 fits (latency-tolerant, non-blocking); job 2 does not — a blocking gate cannot depend on a service with an up-to-24-hour window and no latency SLA.

**Question 57.** Your overnight batch analyzes 300 open PRs. When results return, the poster must attach each analysis to the right PR. How is the mapping maintained?

- A) Results return in submission order, so index alignment suffices.
- B) Set each request's `custom_id` to its PR number at submission, and use the `custom_id` on each result to route it — the Batch API's correlation mechanism.
- C) Ask the model to embed the PR number in its own output text.
- D) Submit 300 separate single-request batches so each result is unambiguous.

**Question 58.** One pipeline job generates a bug fix and then, in the same session, reviews that fix before auto-merging. Post-incident analysis shows the reviews approve nearly everything, including a fix that broke production. What is the structural correction?

- A) Split generation and review into separate jobs, with the review running as an independent instance that receives the diff but none of the generator's session context.
- B) Add "assume the fix is wrong until proven otherwise" to the review prompt.
- C) Require two self-review passes before the auto-merge.
- D) Auto-merge only fixes under 20 lines, reviewing larger ones manually.

**Question 59.** An 18-file PR gets inconsistent review depth — thorough on early files, thin on later ones — and the bot approved a cross-file API change in one file while flagging its mirror image in another. How should the review be restructured?

- A) Reverse file order on a second pass and merge both passes' findings.
- B) Cap PRs at 6 files via repository policy.
- C) Split the review into per-file passes for local issues plus a dedicated cross-file integration pass for API consistency and data flow — eliminating the attention dilution causing both symptoms.
- D) Increase the review job's `max_tokens` so later files get more budget.

**Question 60.** You want findings the bot is demonstrably reliable about to post automatically, while shakier ones queue for human moderation. The bot emits a per-finding confidence score. What makes this routing sound?

- A) Trust findings at confidence ≥ 9/10; models rarely overstate certainty at the top of the scale.
- B) Route by category instead — security findings to humans, everything else auto-posts.
- C) Auto-post everything but add a "low confidence" label where the score is low.
- D) Validate the scores first: measure accuracy against a labeled set of past findings at each confidence level, and set the auto-post threshold where measured precision meets your bar — self-reported confidence is only usable once calibrated.

---
# Answer Key — Practice Exam 4

**Quick key:** 1-D, 2-B, 3-A, 4-C, 5-D, 6-A, 7-B, 8-C, 9-A, 10-D, 11-C, 12-B, 13-D, 14-A, 15-C, 16-B, 17-D, 18-A, 19-C, 20-B, 21-D, 22-A, 23-C, 24-B, 25-D, 26-C, 27-A, 28-B, 29-D, 30-A, 31-C, 32-B, 33-D, 34-A, 35-C, 36-B, 37-D, 38-A, 39-B, 40-C, 41-D, 42-A, 43-C, 44-B, 45-D, 46-A, 47-C, 48-B, 49-D, 50-A, 51-C, 52-D, 53-B, 54-A, 55-C, 56-D, 57-B, 58-A, 59-C, 60-D

---

**1. D** — Every executed `tool_use` must be answered with a matching `tool_result` block appended to the conversation before the next request; the 400 error is the API telling you the loop skipped that step. A, B, and C are unrelated request mechanics — none satisfies the missing-result contract.

**2. B** — A monthly-violated financial policy needs interception: a hook that blocks gift-card refunds at the tool-call level and redirects to the goodwill workflow. A adds probabilistic reinforcement to an already-failing prompt approach. C doubles inference cost for a still-probabilistic check. D relocates prompt text; descriptions guide selection, they don't enforce.

**3. A** — The gate must check what actually happened in the session, not what the conversation claims: block `update_email` until a verification step has completed. Social engineering defeats prompt rules (B, C) precisely because the model weighs persuasive context. D detects fraud after the account is compromised.

**4. C** — No-runbook, unknown-cause investigations call for adaptive plans: hypothesize, look up, let findings drive the next step. A applies a script to a case that doesn't fit it. B escalates work the agent can meaningfully progress. D burns calls without a hypothesis connecting them.

**5. D** — Overnight, tool results go stale while the negotiated resolution stays valid — exactly the split a structured case summary preserves: start fresh, inject the durable facts, re-look-up the time-sensitive ones. A trusts stale state. B carries the stale context along while distrusting it — the worst of both. C throws away the resolution details and burns customer goodwill.

**6. A** — Tone and empathy are behavioral guidance where occasional imperfection is tolerable — the appropriate domain of prompt instructions. B, C, and D are compliance rules with financial or security consequences, which is why they're hooked: any violation is unacceptable, so enforcement must be deterministic.

**7. B** — A malformed input is a validation error: name the field, state the expected format, and mark it correctable so the agent fixes the argument and re-calls in one step. A gives no correction path. C silently guesses intent inside the tool — hidden behavior that will misfire. D triggers retries of an input that will fail identically every time.

**8. C** — Tool descriptions should state boundaries — what the tool is for and what it is not for, naming the alternative. The agent chooses refunds because nothing signals exchanges are out of scope. A abuses naming to carry documentation. B teaches by failure at customer expense. D merges two flows with different semantics, creating a new selection problem inside one tool.

**9. A** — Selection reliability degrades as the tool count grows; the correction is scoped tool access — split by role so each agent carries only the handful of tools its job needs. B and D are cosmetic reorderings of an oversized surface. C adds latency to every call without reducing the decision complexity causing the errors.

**10. D** — For standard integrations, prefer existing community MCP servers; custom development is reserved for team-specific workflows. Zendesk CRUD is as standard as it gets. A is not-invented-here. B bypasses the tool interface the agent needs. C creates an undifferentiated mega-tool — a selection and description problem waiting to happen.

**11. C** — Returning failures as successes is the silent-suppression anti-pattern: the agent cannot respond truthfully or recover from an error it never sees. The fix is structured errors that surface. A trades one sentinel for another. B adds a verification round-trip to compensate for lying infrastructure. D helps engineers, not the customer being told falsehoods.

**12. B** — Frustration over a resolvable issue calls for acknowledgment plus immediate resolution — escalate only if the customer asks for a human. Sentiment is an unreliable proxy for complexity (A); this case is squarely within capability. C addresses mood while deferring the actual fix. D resolves the issue but ignores a customer who needs to be heard — hurting the interaction anyway.

**13. D** — Policy gaps are an escalation trigger: the published policy is silent on competitor matching, so the agent has no authority to improvise (A), refuse definitively (B), or invent criteria (C). Escalating routes the exception to someone empowered to set precedent.

**14. A** — Multiple customer matches require clarification through additional identifiers, not heuristic selection. B is a heuristic (shared phone number across the accounts makes it worse). C mutates customer data on a guess. D proceeds on the guess and merely documents it.

**15. C** — Multi-issue sessions need structured issue data — order ID, amount, status, next action per issue — persisted in a separate context layer rather than left to drift in conversational history. A and D constrain customers to fit the architecture. B bloats every response and still relies on the model keeping the issues straight.

**16. B** — The decomposition is the failure point: the coordinator collapsed a broad topic into one industry's subtasks. Fix decomposition — enumerate the topic's domains first, then generate subtasks against that enumeration with coverage criteria. A patches queries downstream of bad assignments. C adds a guessing agent. D fills gaps with uncited background knowledge.

**17. D** — In hub-and-spoke architecture, aggregation belongs to the coordinator: one place for completeness checks, ordering, and error handling before synthesis. A gives the consumer an orchestration job. B rebuilds coordinator responsibilities inside a message bus. C verifies delivery without anyone owning the whole picture.

**18. A** — `fork_session` creates independent branches from a shared analysis baseline — each framework develops in isolation without re-paying for the 400-document analysis and without cross-contamination. B resumes one lineage twice into the same history. C re-buys the corpus analysis. D lets each framework bias the other.

**19. C** — Match decomposition to predictability: the six-section weekly digest is a fixed prompt chain; novel ad-hoc investigations need dynamic decomposition that adapts to findings. A adds adaptive overhead to clockwork. B scripts the unscriptable. D assigns each pipeline the wrong pattern.

**20. B** — Independent gathering tasks parallelize by emitting all six Task calls in a single coordinator response. A changes what is fetched, not the serialization. C makes each sequential step cheaper but keeps six round-trips. D starts synthesis before its inputs exist.

**21. D** — Natural-language completion markers are the classic termination anti-pattern: they fire spuriously (the model discusses "DONE"), get paraphrased away, and duplicate what `stop_reason` already provides reliably. A, B, and C progressively decorate the wrong mechanism.

**22. A** — Zero matches from a valid query is a *successful* search; conflating it with failure caused a pointless failover. Tools must distinguish valid empty results from access failures. B substitutes wrong results for honest emptiness. C adds infrastructure to disambiguate what the response shape should state. D keeps the ambiguity and hides the distinction in logs the agent never sees.

**23. C** — Descriptions should document input formats, limits, and edge-case behavior — a 256-character truncation is exactly the constraint an agent needs to compose valid queries. A and B are metadata that don't prevent the failure. D is a disclaimer, not a contract.

**24. B** — The agent prefers the tool it understands; "Searches arXiv" gives no case for selection. Enhance the description — what it searches, what it returns, when to prefer it over general web search. A removes a tool still needed for non-academic queries. C is keyword-matching brittleness. D — ordering isn't a documented selection mechanism; descriptions are.

**25. D** — Subagents should recover locally from transient failures (retry the parse) and, failing that, continue the assignment — propagating only the unresolvable failure with partial results. Nine parsed documents is a report, not a total failure. A pretends timeouts can be configured away. B re-runs everything including the nine successes. C addresses throughput, not the give-up-entirely logic.

**26. C** — Conflicting values from credible sources are completed analysis, not noise: include both, annotated with source and methodology, and let the coordinator decide reconciliation before synthesis. A invents a number. B stalls the pipeline where annotation suffices. D encodes an arbitrary tiebreak (recency) as truth.

**27. A** — Synthesis can only be as accurate as its inputs; requiring structured outputs with metadata — dates, source locations, methodological context — on every finding removes the inference that produces the misdating. B sends synthesis hunting for facts upstream already had. C flags the symptom. D asks a better model to guess better.

**28. B** — When the downstream consumer's budget is limited, change what upstream produces: structured key facts, citations, and relevance scores instead of excerpts plus reasoning narratives. A splits the material and loses cross-cutting synthesis. C scales cost to fit waste. D adds a lossy compression stage in the least-informed position.

**29. D** — Provenance must carry the source's own characterization: structured findings that keep "preliminary, n=12" attached to the claim, with synthesis required to preserve the qualifiers. A audits after the flattening. B and C exclude or demote evidence rather than representing it honestly.

**30. A** — The crash-recovery pattern: agents export structured state to a known location as they work; on resume the coordinator loads the manifest and injects prior state, resuming instead of restarting. B restarts from zero, just automatically. C doubles cost for a coin flip. D schedules around failure instead of recovering from it.

**31. C** — Resumption fits when prior context is mostly valid; the practice is informing the resumed session of the specific changes (the two auth modules, PR #412) for targeted re-analysis. A over-rotates on a small delta. B leaves stale beliefs live until the agent happens to re-read. D re-pays for the 95% that didn't change.

**32. B** — The canonical loop: continue while `stop_reason` is `"tool_use"` (execute, append results, send), exit on `"end_turn"`. A keys on text presence — meaningless. C makes an iteration cap the completion condition. D parses punctuation.

**33. D** — Heterogeneous formats from multiple MCP servers are normalized deterministically in a `PostToolUse` hook — one canonical path form before the model reasons. A and C make the model do conversions probabilistically on every comparison. B sacrifices capability to dodge an integration with a standard solution.

**34. A** — Tool restrictions belong in the subagent's AgentDefinition: a doc-writer defined with Read, Grep, and Write cannot run builds. B is advisory. C has the coordinator babysitting instead of configuring. D punishes output latency after the fact.

**35. C** — Locating where a string originates is content search: Grep for the error message. A guesses the filename encodes the concept. B assumes the answer's location before searching. D searches history for what the working tree can answer directly.

**36. B** — With byte-identical repeated blocks, unique anchoring is unreliable even widened; the documented fallback is Read the file, then Write it back with the single intended change. A gambles that surroundings differ — in a generated file they often don't. C makes five changes to achieve one. D is disproportionate and assumes a regeneration path exists.

**37. D** — Personal preferences belong in user-level `~/.claude/CLAUDE.md`: applied for you, invisible to teammates, never in the repo. A ties preferences to file ownership, which changes. B ships them to everyone with a courtesy label. C makes your own defaults opt-in for you.

**38. A** — `allowed-tools` is the structural control: a read-only toolset means no prompt defect can execute `git push` — the capability isn't there. B relies on developers reading plans carefully every time. C mitigates one command's damage. D shrinks the blast radius instead of removing the blast.

**39. B** — Project-scoped commands in `.claude/commands/` are version-controlled and available to anyone who clones — zero setup. A, C, and D describe distribution mechanisms Claude Code doesn't have (image installs, account sync, this built-in).

**40. C** — Conventions tied to a file type spread across many directories are the glob-rule case: `.claude/rules/` with `paths: ["**/*.sql"]` loads them exactly when matching files are edited. A covers one directory of many. B loads SQL rules in every session forever. D loads them only when invoked.

**41. D** — A well-understood, single-function change with a clear location is direct execution. Plan mode (A), exploration subagents (B), and session forking (C) each add process to a task with no design uncertainty to resolve.

**42. A** — Architectural scope (45+ files), multiple valid strategies, and rollback implications are plan mode's explicit criteria: explore, compare, commit to a design before edits. B begins mechanically before the strategy exists. C checkpoints a process that lacks a design. D delegates the decision along with the labor.

**43. C** — Undecided design dimensions plus suspected unknown-unknowns is the interview pattern's home case: Claude asks about traffic shape, burst tolerance, rejection semantics, and failure modes before implementation. A picks a "standard" without your requirements. B critiques a spec limited by the same blind spots. D discovers requirements in production.

**44. B** — When prose descriptions produce inconsistent interpretations, concrete input/output example pairs — including an edge case — pin down the transformation. A defines words instead of behavior. C formalizes ambiguity. D documents the library, not your expected output.

**45. D** — `@import` exists for exactly this: each package's CLAUDE.md references the single `standards/security.md`, one source of truth included where relevant. A works by filesystem trickery and breaks portability. B guarantees drift across six copies. C mentions the file without loading it.

**46. A** — `-p` / `--print` is non-interactive mode: process, print, exit — cron-safe. B, C, and D are invented flags; none exists in Claude Code.

**47. C** — The re-review pattern: prior findings go into context, and the bot reports only new issues plus a note on which prior ones remain unaddressed — no duplicates. A leaves post-push changes unreviewed. B destroys comment threads and discussion. D still requires the dedup logic C provides, while hiding findings from inline context.

**48. B** — Guaranteed field names and types come from `--output-format json` with `--json-schema`: schema-enforced structure for machine parsing. A and D parse unguaranteed output defensively or hopefully. C is an invented flag.

**49. D** — Effective criteria are specific and categorical: flag only when the comment's claimed behavior contradicts the code — the guide's own example. A is confidence-based filtering, which demonstrably fails to move precision. B caps volume without defining quality. C changes where noise lands, not whether it's noise.

**50. A** — False-positive-heavy categories destroy trust in the whole tool: developers who learn to skim past style noise skim past the accurate security findings too. That contagion is why the noisy category is urgent. B, C, and D invent indirect costs; the documented mechanism is trust erosion.

**51. C** — Ambiguous cases are the targeted-few-shot case: examples of exactly these situations, showing the chosen tool *and the reasoning* over plausible alternatives, teach judgment the model generalizes. A describes the mapping in prose — already too coarse for edge cases. B removes a legitimate output. D hardcodes one answer to varied situations.

**52. D** — Format consistency comes from demonstration: complete sample summaries in the exact required table. Description (C), even stricter, keeps producing drift; that's the observed failure. A regenerates until lucky. B reduces variance around a format the model hasn't internalized.

**53. B** — The correct trio: `"auto"` permits text-only responses; `"any"` mandates some tool call, model's choice; forced selection mandates one named tool. A describes "any." C invents count semantics. D — forcing applies per-request, not until reset.

**54. A** — A structured `detected_pattern` field ties every suggestion to the construct that triggered it, so dismissals aggregate into pattern-level insight — the systematic feedback loop. B and D produce anecdote at low volume. C counts dismissals without capturing what caused them.

**55. C** — The design document was never in the input; no retry recovers information that isn't there. Provide the document, or scope the review to available material. A and B retry harder at reading an absent file. D deletes a category wholesale when the fix is supplying context.

**56. D** — Batch fits latency-tolerant, non-blocking work: the nightly report is ideal; a merge-blocking gate cannot ride a no-SLA, up-to-24-hour service. A ignores the blocking constraint. B overcorrects — the report genuinely fits. C prices workloads instead of matching latency requirements.

**57. B** — `custom_id` is the Batch API's request/response correlation mechanism: set it to the PR number at submission, read it on each result. A relies on ordering the API doesn't promise. C trusts model output for plumbing. D abandons batching's economics to avoid using the feature built for this.

**58. A** — Generation and review must be separated: an independent review instance receives the diff without the generator's session context, avoiding the self-approval bias that shipped the bad fix. B and C prompt or repeat a structurally biased review. D limits exposure without fixing the reviewer.

**59. C** — Declining depth across files plus contradictory verdicts on mirrored code are attention dilution; the restructure is per-file passes for local issues and a separate integration pass for cross-file consistency. A averages two diluted passes. B constrains developers to fit the tool. D — token budget doesn't reallocate attention across a long input.

**60. D** — Confidence becomes routable only after calibration: measure accuracy at each score level against labeled outcomes and place the threshold where precision meets the bar. A trusts raw self-report at the extreme — where miscalibration concentrates. B discards per-finding signal for category stereotype. C posts everything anyway, labeling the risk instead of routing it.

---

*End of Practice Exam 4.*
