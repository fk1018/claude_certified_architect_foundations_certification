# CCAFC Practice Exam 9

**Claude Certified Architect – Foundations — Practice Exam**

Rebalanced edition of Practice Exam 4 — same knowledge points; options rewritten to remove test-taking tells (option-length cues, giveaway distractors), answer letters fully reshuffled (the original followed a near-mechanical rotation), and the header's domain counts corrected to match the actual question mix.

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Customer Support Agent, Multi-Agent Research, Developer Productivity, Claude Code for CI/CD) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (actual): D1 Agentic Architecture ×16, D2 Tool Design & MCP ×10, D3 Claude Code Configuration ×12, D4 Prompt Engineering & Structured Output ×11, D5 Context Management & Reliability ×11. (Close to official weights; D5 runs ~2 high and D2/D4 one low — the original exam 4 header misstated its own mix.)

Answer key with explanations is at the end.

---

## Scenario A: Customer Support Resolution Agent (Questions 1–15)

You are building a customer support resolution agent using the Claude Agent SDK. The agent handles high-ambiguity requests like returns, billing disputes, and account issues, with custom MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`). Your target is 80%+ first-contact resolution while knowing when to escalate.

---

**Question 1.** Your loop executes the agent's tool calls but the next API request fails with a 400 error complaining about `tool_use` blocks that have no corresponding `tool_result` blocks. What did the implementation skip?

- A) Setting `tool_choice: "auto"` on the follow-up request so the model is free to choose whether to call another tool.
- B) Appending each tool's result as a `tool_result` block, matched to its originating `tool_use` ID, before the next request goes out.
- C) Clearing the prior assistant turn from history before sending the new request, along with its tool_use blocks.
- D) Re-registering the full tool definitions on every request in case the API expects them refreshed each round.

**Question 2.** Gift-card purchases are non-refundable by policy; the agent should route those customers to a goodwill-credit workflow instead. The rule lives in the system prompt today, and violations still occur monthly. What is the correct mechanism?

- A) Add several gift-card examples to the few-shot section of the system prompt so the model recognizes the pattern more reliably.
- B) Add a second reviewing model that applies a structured checklist to re-examine every refund decision before the tool executes, catching violations the first pass misses.
- C) Move the gift-card exception out of the system prompt and into the `process_refund` tool description instead.
- D) Intercept `process_refund` with a hook that blocks gift-card cases and reroutes to goodwill credit.

**Question 3.** Account email changes must be preceded by a completed identity verification in the same conversation. Reviewing incidents, you find the agent occasionally performs the change when a persuasive customer insists verification "already happened last week." What prevents this?

- A) A system prompt instruction telling the agent to always double-check with the customer's stated history before trusting a claim that verification already happened earlier.
- B) A library of few-shot examples showing the agent politely refusing to proceed with unverified email changes.
- C) A prerequisite gate: `update_email` stays blocked until an identity verification step has actually completed in the current session.
- D) A daily audit report reviewed by the fraud team, listing every email change made that day.

**Question 4.** A billing dispute arrives with symptoms that don't match any known pattern — the charge exists in one system but not another. There is no established runbook. How should the agent approach the investigation?

- A) Follow the standard billing-dispute script, which correctly handles the majority of disputes the team sees.
- B) Use an adaptive investigation plan: form a hypothesis, run a lookup, and let each finding determine the next step.
- C) Escalate immediately, since no runbook exists for this particular symptom pattern.
- D) Run every available lookup tool once, then decide from the combined set of results.

**Question 5.** A support case is reopened the next morning through a new chat. Yesterday's session contains extensive tool results (order status, refund state) that may have changed overnight, plus the negotiated resolution details. How should the agent be initialized?

- A) Start a new session injecting a written case summary covering the negotiated resolution, re-running lookups for time-sensitive data.
- B) Resume yesterday's session unchanged, since conversational continuity matters more than data freshness here.
- C) Resume yesterday's session but instruct the agent to distrust any tool result it reads from that history.
- D) Start completely fresh with no context carried over at all, and have the customer re-explain the situation, the prior negotiation, and the order details from scratch.

**Question 6.** You maintain four agent behavior requirements. Three are enforced with hooks. Which one is appropriately left to system-prompt guidance alone?

- A) Refunds above $500 must be approved by a human before the tool executes, since a financial threshold breach is exactly the kind of failure a hook exists to catch every time.
- B) Identity must be verified before any tool that mutates account data — email, address, payment method — is allowed to execute.
- C) Responses should acknowledge the customer's frustration before presenting a solution — tone guidance that belongs in the system prompt rather than as a hard-coded rule.
- D) Refunds must be issued only to the original payment method used for the purchase.

**Question 7.** The agent calls `lookup_order` with the date "next Tuesday" in a field expecting `YYYY-MM-DD`. How should the tool respond so the agent can recover in one step?

- A) Return `isError` with a generic "invalid request" message so the agent tries something else.
- B) Silently interpret "next Tuesday" server-side using the current date as a reference point.
- C) Return a transient-category error so the agent retries the exact same call again.
- D) A validation error naming the field, stating the expected format (`YYYY-MM-DD`), and marked correctable.

**Question 8.** Customers asking for exchanges keep getting refunds — the agent calls `process_refund` because nothing tells it that exchanges are handled elsewhere. What is the highest-leverage change?

- A) State the boundary in the description: what the tool is for, and that exchanges belong to `create_exchange`.
- B) Rename `process_refund` to `process_refund_not_exchange` so the scope is obvious from the name alone.
- C) Block exchange-context refunds with a hook that returns a structured error, relying on the agent to infer the exchange boundary from repeated failures over time.
- D) Merge refunds and exchanges into a single `resolve_return` tool that handles both cases internally.

**Question 9.** After a quarter of feature growth, the resolution agent now has 17 tools spanning refunds, subscriptions, loyalty, shipping, and marketing consent. Selection errors have risen steadily with each addition. What is the architectural correction?

- A) Sort the tools array by usage frequency, on the theory that surfacing the most commonly called tools first will reduce how often the model reaches for the wrong one.
- B) Add a mandatory reasoning step before every tool call to slow down selection.
- C) Scope tool access by role — split into specialized agents, each carrying only the tools its role needs.
- D) Shorten all tool descriptions so the full list fits into less context.

**Question 10.** Your team needs standard Zendesk operations (create ticket, add note, change status) available to the agent. An engineer has begun writing a custom MCP server for it. What guidance applies?

- A) Continue — support tooling is too business-critical for community-maintained code to be trusted here.
- B) Use an existing, well-maintained community MCP server for standard Zendesk operations; save custom development effort for workflows that are genuinely unique to your team.
- C) Skip MCP entirely and call Zendesk's REST API directly from inside a hook.
- D) Wrap Zendesk's API in your existing backend and expose the whole thing as one large mega-tool.

**Question 11.** A platform wrapper catches all tool exceptions and returns `{}` with a success status "to keep conversations smooth." Yesterday the agent told a customer their refund was complete when `process_refund` had actually thrown. What is the design lesson?

- A) Wrappers should return `null` rather than `{}` so downstream code can detect the failures.
- B) The agent should independently verify each refund's outcome with a follow-up lookup call after every attempt, regardless of what the tool wrapper reported back.
- C) The wrapper needs better logging so engineers catch these incidents sooner.
- D) Failures must surface to the agent as explicit errors, never disguised as a success response.

**Question 12.** A customer writes: "This is the THIRD time I'm contacting you people about this broken blender!!" The issue is a standard damage replacement with photo evidence — fully within the agent's capability. Sentiment analysis scores the message as highly negative. What should the agent do?

- A) Acknowledge the frustration and repeated contact, then offer to resolve the replacement right now.
- B) Escalate to a human immediately whenever sentiment analysis scores a message as highly negative, since strong emotion signals a case outside the bot's comfort zone.
- C) Escalate if sentiment remains negative after the agent's first empathetic response.
- D) Process the replacement silently without addressing the tone of the message at all.

**Question 13.** A customer requests a price match against a competitor's advertised price. Your published policy covers price adjustments for your own site's price drops but says nothing about competitor matching. The agent should:

- A) Apply the own-site adjustment policy by analogy, since it is the closest existing rule.
- B) Escalate the request to a human — the published policy is silent on competitor price matching entirely, and a genuine policy gap is itself an escalation trigger rather than something to resolve alone.
- C) Decline the request, since the policy does not explicitly authorize competitor matching.
- D) Ask the customer for a screenshot of the competitor's price and decide based on the difference.

**Question 14.** `get_customer` returns three accounts for "Chris Martin" — different addresses, one shared phone number. The agent currently picks the account with the most recent order. What should it do instead?

- A) Pick the account that matches the phone number the customer is currently writing in from, treating the shared number as sufficient confirmation of identity.
- B) Merge the three accounts together, since they likely all belong to the same person.
- C) Ask the customer for an additional identifier — order number, account email, or billing zip — and match on that.
- D) Proceed with the most recent account but flag the conversation for later review.

**Question 15.** In sessions where a customer raises several issues, the agent confuses details between them as the conversation grows — attributing order 8817's status to order 9902's refund. What is the recommended context structure?

- A) Limit customers to raising two issues per conversation so context stays manageable.
- B) Repeat every open issue's full details — order ID, amount, status, and history — back into the conversation at the start of each agent response so nothing drops out of recent context.
- C) Handle issues strictly one at a time, fully closing each before discussing the next.
- D) Persist each issue's own data — order ID, amount, status, next action — in a separate context layer, keyed by issue.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Reports on "the impact of an aging population" consistently cover only healthcare; labor markets, housing, and public pensions never appear. The coordinator's decomposition logs show subtasks like "hospital staffing shortages" and "elder-care costs." What is the fix?

- A) Improve the coordinator's decomposition: enumerate the topic's major domains first, then create subtasks against that list with coverage criteria.
- B) Instruct the search agent to broaden every query it receives with additional sectors.
- C) Add a fourth subagent dedicated to catching whatever domains the others miss.
- D) Have the synthesis agent note in the final report which domains received less attention.

**Question 17.** Each subagent currently posts its findings directly into a shared results channel, and the report agent assembles whatever it finds there. Findings arrive out of order, some overwrite others, and nobody detects missing pieces. Which component should own result collection, and why?

- A) The report agent, since it consumes the assembled results anyway without validating whether anything is missing.
- B) The shared channel itself, rebuilt with structured message ordering, deduplication, and a completeness check that flags any subagent whose expected findings never arrived.
- C) The coordinator — aggregation, completeness checks, and error handling belong at the hub.
- D) Each subagent, verifying its own delivery with a read-back confirmation check.

**Question 18.** After an expensive shared analysis of a 400-document corpus, you want to evaluate two competing report frameworks — thematic versus chronological — each developed independently from that same analysis. What mechanism does the Agent SDK provide?

- A) `--resume` the analysis session twice, once for each competing framework.
- B) `fork_session` — two independent branches from the shared analysis baseline, one framework developed in each.
- C) Run the corpus analysis twice from scratch in two entirely fresh sessions, one per competing framework, paying the full 400-document analysis cost each time.
- D) Develop both frameworks alternately within the single original session.

**Question 19.** Your system produces (a) a weekly market digest with the same six sections every week, and (b) ad-hoc deep investigations of novel questions. How should the two pipelines be decomposed?

- A) Treat both pipelines as dynamic — research output is inherently unpredictable either way.
- B) Treat both pipelines as fixed — consistency simplifies operations across the board.
- C) Make the digest dynamic and the investigations fixed, since digests have more room for creative framing.
- D) Run the weekly digest as a fixed prompt chain; give the ad-hoc investigations dynamic decomposition that adapts to findings.

**Question 20.** Monday's run must gather updates from six independent news domains before synthesis. The coordinator currently delegates them one per turn. What single change most reduces wall-clock time?

- A) Have the coordinator emit all six Task tool calls in a single response so they run in parallel.
- B) Cache Friday's results and only fetch whatever changed over the weekend.
- C) Reduce each domain's search depth so the sequential runs finish faster overall.
- D) Move synthesis earlier in the pipeline so it starts overlapping with the last two domain searches instead of waiting for all six to report back.

**Question 21.** A reviewer flags this coordinator code: `if "DONE" in assistant_text: break` — paired with a system prompt instructing the model to "say DONE when research is complete." What is the professional assessment?

- A) Acceptable — explicit completion markers like this are a common convention in agent frameworks.
- B) The marker should be structured, a JSON field, rather than a bare string embedded in prose.
- C) Termination should key off `stop_reason` (`"end_turn"`), not a natural-language marker the model might paraphrase or discuss without meaning it.
- D) The check is fine as written, but it should also require that no tool calls are pending in the same response, since a stray marker could otherwise appear mid-sequence before the work is actually done.

**Question 22.** Researching an extremely niche topic, the search subagent's query legitimately matches nothing. The tool returns an error, and the coordinator logs "search infrastructure degraded" and switches to a fallback provider — wasting a cycle. What is the correct contract?

- A) The tool should return the closest partial matches instead of returning nothing at all.
- B) The coordinator should ping a health-check endpoint before interpreting any tool error.
- C) Empty results and genuine failures can share one response shape as long as the log message differs.
- D) Zero matches is a successful query with an empty result set; errors are reserved for actual access failures like an unreachable index or malformed request.

**Question 23.** Your `search_corpus` tool truncates queries over 256 characters — silently. Agents regularly compose long, careful queries whose critical qualifiers get cut off, returning oddly irrelevant results no one can explain. Beyond fixing the truncation, what should the tool description have included?

- A) A version number in the description so agents know the tool's parsing and truncation behavior might silently change between releases.
- B) The input constraint and edge-case behavior: the maximum query length and what happens beyond it.
- C) Usage statistics showing what typical query lengths look like across other agents.
- D) A warning that overall search quality varies by topic.

**Question 24.** The document analysis agent has access to a purpose-built `arxiv_search` MCP tool but keeps using the generic built-in WebSearch for academic queries, returning blog summaries instead of papers. `arxiv_search`'s description is "Searches arXiv." What is the recommended fix?

- A) Enhance the description: what it searches, what it returns, and when to prefer it over general web search for academic queries.
- B) Remove WebSearch from the agent entirely so arxiv_search wins by default.
- C) Add a few-shot example showing arxiv_search used for a query containing the word "paper," and rely on that single pattern to generalize across every future academic query the agent sees.
- D) Lower WebSearch's priority through tool ordering in the agent definition.

**Question 25.** The document analysis agent abandons its entire assignment the first time a PDF-parsing call times out, reporting total failure to the coordinator even when 9 of 10 documents parsed fine. What error-handling design is missing?

- A) A longer parsing timeout so the failures stop happening in the first place.
- B) A coordinator-side retry that reruns the entire document analysis task from scratch.
- C) Local recovery: retry the failed parse, continue with the rest of the documents, and propagate only the unresolved failure alongside the partial results.
- D) Parallel parsing so a single timeout doesn't serialize the rest of the batch.

**Question 26.** While analyzing a corpus, the analysis agent finds two credible papers reporting incompatible efficacy figures. It currently discards the outlier and reports one clean number. What should it do instead?

- A) Report the average of the two figures, with a note describing the variance between them.
- B) Hold both papers back from synthesis entirely and pause the pipeline until a human reviewer is available to adjudicate which figure is correct.
- C) Re-run the analysis with instructions to prefer whichever paper is more recent.
- D) Include both values, annotated with source and methodology, and let the coordinator decide how to reconcile them.

**Question 27.** The synthesis agent regularly misdates events and attributes findings to the wrong methodology. Upstream, the analysis agent's outputs are well-written prose summaries. What structural requirement fixes this?

- A) Give the synthesis agent web search access so it can independently verify dates and methodology against outside sources itself, on every finding it receives.
- B) Require the analysis agent to attach metadata — dates, source locations, methodology — to every finding it passes downstream.
- C) Have the synthesis agent flag any date it feels unsure about in the final report.
- D) Use a stronger model for synthesis so it infers the missing metadata more accurately.

**Question 28.** Your synthesis agent's context budget is small, and upstream agents currently send it full document excerpts plus their complete reasoning narratives. Synthesis truncates and quality collapses on large topics. What is the recommended change?

- A) Rotate synthesis across three agents, each handling a third of the material independently.
- B) Raise the synthesis agent's context budget and accept the added cost.
- C) Have synthesis summarize its own input first, then synthesize that summary.
- D) Have upstream agents return structured key facts, citations, and relevance scores sized for what the synthesis agent can actually consume.

**Question 29.** A source paper carefully describes its results as "preliminary findings from a small pilot (n=12)." The final report states the same results as established fact. Where should this be prevented?

- A) In the structured findings passed downstream — qualifiers like "preliminary, n=12" stay attached to the claim all the way through synthesis.
- B) In report review — a final pass that re-checks every claim against its original source.
- C) By excluding pilot studies from the research process entirely.
- D) By having the search agent rank small pilot studies lower in its results, so they surface less often in the material passed downstream.

**Question 30.** Your overnight research runs sometimes die partway (provider outages). Restarting from zero wastes hours of completed subagent work. What recovery design is recommended?

- A) Wrap the whole overnight run in a retry loop with exponential backoff, restarting the entire pipeline from the beginning on every provider outage.
- B) Run two identical pipelines in parallel and keep whichever one finishes first.
- C) Agents export their state as they work; on resume the coordinator loads the manifest and injects the prior state.
- D) Schedule runs during the provider's historically most stable hours.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You resume yesterday's architecture-investigation session. Overnight, one teammate's PR merged, refactoring the two authentication modules the session had analyzed; nothing else changed. What is the efficient continuation?

- A) Start a new session — any change to the codebase invalidates a prior session.
- B) Resume the session and tell the agent that the two auth modules changed in PR #412, asking it to re-analyze just those.
- C) Resume the session and let the agent notice the changes on its own when it next reads those files.
- D) Resume the session and re-run the entire investigation from scratch to be safe.

**Question 32.** Which loop skeleton is correct for an Agent SDK/API tool-use loop?

- A) `while response.stop_reason == "tool_use": execute tools; append results; send(...)` — exiting the loop on `"end_turn"`.
- B) `while response.content contains text: send(...)`
- C) `for i in range(MAX_STEPS): send(...)` — treating an arbitrary iteration cap as the completion condition instead of anything the API actually returns.
- D) `while not response.text.endswith("."): send(...)`

**Question 33.** Your agent uses three file-related MCP tools from different vendors: one returns absolute paths, one repo-relative paths, one `file://` URIs. The agent regularly treats the same file as three different files. What is the cleanest fix?

- A) Add a system prompt table explaining each vendor's path convention in detail, and rely on the model to normalize between absolute, relative, and URI forms itself, every time it compares two paths.
- B) Standardize on one vendor's tools and drop the other two entirely.
- C) Normalize all paths to one canonical form in a `PostToolUse` hook before the model ever sees the results.
- D) Instruct the agent to canonicalize paths itself before comparing any two of them.

**Question 34.** Your doc-writer subagent's AgentDefinition grants the full toolset. Last week it ran `npm run build` "to verify the docs examples compile," consuming twenty minutes. Its actual job needs only Read, Grep, and Write. Where is the fix made?

- A) In the doc-writer's system prompt: add an instruction saying "do not run builds," reinforced with a few-shot example of a compliant response.
- B) In the coordinator, using a hook that watches subagent tool calls and cancels any that run long.
- C) In CI, which should reject doc PRs that took an unusually long time to produce.
- D) In the subagent's AgentDefinition — restrict its tool list to Read, Grep, and Write so a build call is never possible.

**Question 35.** A stack trace shows the error string "connection pool exhausted" but the codebase is unfamiliar and you don't know which module raises it. What is the right first tool call?

- A) Glob for `**/pool*` and read whatever files match.
- B) Grep the codebase for the exact error message string.
- C) Read the database configuration files first, on the assumption that a connection-pool error must originate near the connection settings.
- D) Run `git log --grep "pool"` to find commits that might be related.

**Question 36.** The agent must change one occurrence of a YAML block that appears, byte-identical, five times in a generated config file. Edit keeps failing on non-unique anchor text. What is the reliable approach?

- A) Keep retrying Edit with progressively larger anchor snippets, on the assumption that some surrounding context will eventually become unique in the file.
- B) Edit with `replace_all`, then manually revert the four unwanted changes with four more Edit calls.
- C) Read the file, then Write it back with only the single intended occurrence modified.
- D) Delete the file and regenerate it from the template with the change already applied.

**Question 37.** You put your personal preferences — two-space indent debates, your favorite commit-message style — into the project's CLAUDE.md. Teammates are now complaining that Claude nags them about your preferences. Where do personal preferences belong?

- A) In your user-level `~/.claude/CLAUDE.md`, which applies only to your own account and never touches the shared repo.
- B) In a `.claude/rules/` file scoped to files you personally own.
- C) In a skill only you invoke at the start of your own sessions.
- D) In a gitignored personal section appended to the project's CLAUDE.md.

**Question 38.** Your `/analyze-arch` skill only ever needs to read code and produce a report, but during one run it executed `git push` from a leftover instruction in its prompt file. Beyond fixing the prompt, what structural control applies?

- A) Add a pre-run confirmation step where the developer reviews and approves the skill's full plan before any command in it is allowed to execute.
- B) Have the skill run `git stash` first so any push it attempts contains nothing.
- C) Move the skill to user scope so a mistake only affects the one person who invoked it.
- D) Configure `allowed-tools` in the skill's frontmatter to a read-only set.

**Question 39.** A new engineer clones the repo, opens Claude Code, and types `/deploy-check` — the team's pre-deployment verification command — and it works immediately with no setup. What makes this possible?

- A) The command was installed globally by the infrastructure team's laptop image.
- B) Claude Code synced the command from the previous engineer's account automatically the first time the new engineer signed in with the same organization.
- C) The command is defined in `.claude/commands/` in the repository, so it travels with version control.
- D) `/deploy-check` is a built-in Claude Code command available to everyone.

**Question 40.** Your SQL conventions (naming, mandatory `WHERE` review for deletes, migration header format) should apply whenever Claude edits any `.sql` file — they sit in `db/`, `analytics/`, and various service folders. What is the correct configuration?

- A) A CLAUDE.md placed in `db/`, the largest of the SQL directories.
- B) A `.claude/rules/` file with frontmatter `paths: ["**/*.sql"]`, so it loads automatically whenever a matching file is touched, no matter which folder it lives in.
- C) The root CLAUDE.md, with a dedicated "SQL rules" section added to it.
- D) A `/sql-mode` skill that developers invoke before starting database work.

**Question 41.** The ask: add a validation check rejecting end dates earlier than start dates in one form handler — a well-understood, single-function change. Which workflow?

- A) Direct execution — the change is simple, well-scoped, and its location in the codebase is already known.
- B) Plan mode, then implementation — date comparisons are subtler than they look, and even a single-function change deserves a design pass before touching code.
- C) An Explore subagent to survey date-handling logic across the whole repo first.
- D) `fork_session` to test two different validation styles independently.

**Question 42.** You're replacing the ORM across a service — 45+ files, three plausible migration strategies with different transaction semantics, and rollback implications. Which workflow?

- A) Direct execution, since each individual file's change becomes mechanical once you begin, and 45 mechanical edits are still just 45 edits regardless of the transaction semantics behind them.
- B) Direct execution with `--resume` checkpoints inserted after every ten files.
- C) Plan mode first: explore the codebase, compare the three strategies, and settle the design before making any edits.
- D) Delegate the whole migration to a single subagent to keep the main context window clean.

**Question 43.** You're implementing a rate limiter but haven't decided on the algorithm, burst policy, or what happens to rejected requests — and you suspect there are failure modes you haven't considered. What gets you the best design conversation?

- A) Ask Claude for the industry-standard rate limiter design and implement that directly.
- B) Write your own best-guess specification and have Claude critique it before you start.
- C) Implement a token-bucket limiter first and iterate based on staging-traffic behavior.
- D) Use the interview pattern: have Claude ask about traffic shape, burst tolerance, and failure modes before any implementation begins.

**Question 44.** Claude keeps misinterpreting your description of a log-line transformation ("extract the request ID and normalize the timestamp — you know, standard format"). Three attempts, three different behaviors. What input finally pins it down?

- A) Two or three concrete example pairs: real input log lines and the exact expected output, including one edge case.
- B) A glossary defining "request ID," "normalize," and "standard format" precisely.
- C) A longer description written with RFC-style MUST/SHOULD language throughout, spelling out every rule the transformation is supposed to follow in prose.
- D) A link to the logging library's own documentation for the format.

**Question 45.** Security standards used by all six packages in your monorepo live in `standards/security.md`. Each package has its own CLAUDE.md. How do packages include the shared standards without copying them?

- A) Symlink `security.md` into each of the six package directories.
- B) Use `@import` in each package's CLAUDE.md to reference `standards/security.md`.
- C) Paste the full content into each of the six packages' CLAUDE.md files directly, and remember to manually update all six copies whenever the standard changes.
- D) Mention in each CLAUDE.md that a security standards file "exists somewhere in the repo."

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** A nightly cron job needs Claude Code to summarize the day's merged changes and write the summary to a file. Which flag makes the invocation suitable for cron?

- A) `--headless`, which disables the terminal UI for scripted runs.
- B) `--non-interactive`, which auto-answers any prompts with their defaults.
- C) `--quiet`, which suppresses interactive input requests entirely.
- D) `-p` (`--print`) — process the prompt non-interactively, print the result, and exit cleanly, which is exactly what a cron job needs.

**Question 47.** Developers complain that after each push, the review bot re-posts its full findings list, burying the thread. The findings are usually the same unresolved items plus one or two new ones. Reviewers want inline comments on the affected lines for new issues, with existing discussion threads preserved. What re-review design fixes the noise?

- A) Feed prior findings into the re-review context; post only new issues, noting which prior ones remain open.
- B) Only run the bot once per PR, on its first open.
- C) Have the bot's posting hook delete old comments before posting the new full list each time.
- D) Replace inline comments with a single continuously-edited summary comment at the top of the PR, so every push updates one comment instead of adding new ones each time.

**Question 48.** Your pipeline must transform Claude's review findings into your internal defect-tracker format. The transformation code needs guaranteed field names and types from Claude's output. Which invocation provides that?

- A) `claude -p "..." | jq` with defensive null checks, since plain text output carries no schema guarantee for field names or types.
- B) `claude -p "..." --strict` to enable a careful output mode.
- C) `claude -p "..." --output-format json --json-schema findings-schema.json`
- D) `claude -p "..."` with a prompt instruction to "output valid JSON matching our schema," trusting the model to follow the instruction consistently across every single run.

**Question 49.** Your comment-accuracy checker flags dozens of harmless doc comments per PR ("this comment could be more precise"). You want it to flag only real problems. Which criterion should replace the current "check that comments are accurate" instruction?

- A) "Only flag comments you are highly confident are wrong."
- B) "Flag a comment only when the behavior it claims directly contradicts what the code actually does, not merely when it could be phrased more precisely."
- C) "Flag at most three comments per pull request, regardless of how many are wrong."
- D) "Prefer flagging comments on public APIs over internal helper functions."

**Question 50.** Metrics show your security-review category is highly accurate, but the style category floods PRs with noise. A teammate argues style can wait since security "is what matters." Why is the style noise urgent anyway?

- A) Style issues compound into security issues over time if left unaddressed, since sloppy formatting habits gradually erode the discipline that also catches security mistakes.
- B) Noise adds token overhead, and token costs dominate the tool's overall budget.
- C) The style category's noise statistically hides the security findings inside long comment lists.
- D) High false-positive categories erode trust in the whole tool — the accurate security findings get ignored too.

**Question 51.** Your CI bot has three response tools: `comment_inline`, `open_issue`, and `request_changes`. For clear-cut cases it chooses well, but for ambiguous ones (a real bug that's out of the PR's scope; a severe issue in unchanged code) it picks inconsistently. What most improves these decisions?

- A) A few targeted few-shot examples of exactly these ambiguous cases, showing the chosen tool and the reasoning behind it.
- B) A decision matrix written out in prose, mapping every combination of issue attributes — scope, severity, location — to the tool that should handle it.
- C) Removing `open_issue` from the toolset so there are fewer choices to make.
- D) Making `request_changes` the default response for any case involving uncertainty.

**Question 52.** You want every PR summary the bot posts to follow the same five-column markdown table. Instructions describing the table produce close-but-drifting variants (merged columns, extra sections). What reliably locks the format?

- A) A markdown linter that checks the summary against a structured template and rejects malformed output, triggering regeneration.
- B) Few-shot examples showing several complete sample summaries, each already formatted in the exact five-column table the format requires.
- C) Lowering the temperature setting to reduce formatting creativity.
- D) A stricter prose description of the table, with column widths specified precisely.

**Question 53.** Which statement about `tool_choice` is correct?

- A) `"auto"` guarantees at least one tool call will appear in the response.
- B) `"any"` lets the model call any number of tools, while `"auto"` limits it to exactly one.
- C) `"auto"` may yield text only; `"any"` forces some tool call; `{"type": "tool", "name": ...}` forces one specific tool.
- D) Forced tool selection, once set with `tool_choice`, applies to every subsequent turn in the conversation and stays in effect until the developer explicitly resets it.

**Question 54.** Developers dismiss many of the bot's test-generation suggestions, and you want to learn systematically which kinds of code constructs produce the unwanted suggestions. What enables that analysis?

- A) Exit interviews with the developers who dismiss the most suggestions overall, asking them to recall which specific patterns felt wrong after the fact.
- B) A dashboard showing dismissal counts broken down by repository.
- C) Free-form "reason for dismissal" text boxes, reviewed manually once a month.
- D) A `detected_pattern` field in each suggestion identifying the code construct that triggered it.

**Question 55.** The review bot's finding — "this implementation may not match the approved design" — fails validation because it cites a design document the bot was never given. Will retry-with-error-feedback resolve it?

- A) No — the design document was never provided in context; supply it, or scope the review to only what the bot was actually given.
- B) Yes — the validation error will make the bot reason more carefully about the design.
- C) Yes, if the retry also raises `max_tokens` so the bot can analyze more deeply.
- D) No — findings that reference external documents should be auto-deleted on sight.

**Question 56.** Two jobs are proposed for the Message Batches API: (1) a nightly "explain every lint suppression in the repo" report read weekly; (2) the PR-blocking security gate developers wait on before merging. Evaluate.

- A) Both fit — the roughly 50% cost savings applies equally regardless of workload.
- B) Job 1 fits (latency-tolerant, non-blocking); job 2 cannot depend on a no-SLA, up-to-24-hour service.
- C) Neither fits — CI workloads need real-time APIs across the board, batch or not.
- D) Job 2 fits better, since security scans are the heavier of the two workloads and stand to benefit the most from the batch discount on token usage.

**Question 57.** Your overnight batch analyzes 300 open PRs. When results return, the poster must attach each analysis to the right PR. How is the mapping maintained?

- A) Results return in submission order, so simple index alignment is sufficient.
- B) Ask the model to embed the PR number directly inside its own output text.
- C) Submit 300 separate single-request batches so each result is unambiguous on its own, forgoing the throughput and cost benefits of grouping requests together.
- D) Set each request's `custom_id` to its PR number at submission time, and route each result by that ID when it comes back.

**Question 58.** One pipeline job generates a bug fix and then, in the same session, reviews that fix before auto-merging. Post-incident analysis shows the reviews approve nearly everything, including a fix that broke production. What is the structural correction?

- A) Add "assume the fix is wrong until proven otherwise" to the review prompt.
- B) Require two self-review passes by the same session before allowing the auto-merge.
- C) Split generation and review: an independent instance reviews the diff without any access to the generator's session context.
- D) Auto-merge only fixes under 20 lines, and route anything larger to manual review.

**Question 59.** A 16-file PR gets inconsistent review depth — thorough on early files, thin on later ones — and the bot approved a cross-file API change in one file while flagging its mirror image in another. How should the review be restructured?

- A) Reverse the file order on a second pass and merge the structured findings from both passes.
- B) Split the review into per-file passes for local issues, plus a dedicated cross-file integration pass.
- C) Cap PRs at 6 files via repository policy so review depth stays consistent.
- D) Increase the review job's `max_tokens` so later files in a long PR get as much generation budget as the earlier ones already received.

**Question 60.** You want findings the bot is demonstrably reliable about to post automatically, while shakier ones queue for human moderation. The bot emits a per-finding confidence score. What makes this routing sound?

- A) Validate first: measure accuracy per confidence level against labeled findings, then set the auto-post threshold where precision actually meets the bar.
- B) Trust findings at confidence ≥ 9/10 without further validation; models rarely overstate certainty at the very top of the scale, so the risk of a false positive there is negligible.
- C) Route by category instead — security findings go to humans, everything else auto-posts.
- D) Auto-post everything, but attach a "low confidence" label wherever the score is low.

---
# Answer Key — Practice Exam 9

**Quick key:** 1-B, 2-D, 3-C, 4-B, 5-A, 6-C, 7-D, 8-A, 9-C, 10-B, 11-D, 12-A, 13-B, 14-C, 15-D, 16-A, 17-C, 18-B, 19-D, 20-A, 21-C, 22-D, 23-B, 24-A, 25-C, 26-D, 27-B, 28-D, 29-A, 30-C, 31-B, 32-A, 33-C, 34-D, 35-B, 36-C, 37-A, 38-D, 39-C, 40-B, 41-A, 42-C, 43-D, 44-A, 45-B, 46-D, 47-A, 48-C, 49-B, 50-D, 51-A, 52-B, 53-C, 54-D, 55-A, 56-B, 57-D, 58-C, 59-B, 60-A

---

**1. B** — Every executed `tool_use` must be answered with a matching `tool_result` block, tied to the same ID, appended before the next request; the 400 error is the API telling you the loop skipped that step. A, C, and D are unrelated request mechanics — none satisfies the missing-result contract.

**2. D** — A monthly-violated financial policy needs interception: a hook that blocks gift-card refunds at the tool-call level and redirects to the goodwill workflow. A adds probabilistic reinforcement to an already-failing prompt approach. B doubles inference cost for a still-probabilistic check, structured checklist or not. C relocates prompt text; descriptions guide selection, they don't enforce.

**3. C** — The gate must check what actually happened in the session, not what the conversation claims: block `update_email` until a verification step has completed. Social engineering defeats prompt rules (A, B) precisely because the model weighs persuasive context. D detects fraud after the account is compromised.

**4. B** — No-runbook, unknown-cause investigations call for adaptive plans: hypothesize, look up, let findings drive the next step. A applies a script to a case that explicitly doesn't fit it — the script's coverage of ordinary disputes is what makes it tempting. C escalates work the agent can meaningfully progress. D burns calls without a hypothesis connecting them.

**5. A** — Overnight, tool results go stale while the negotiated resolution stays valid — exactly the split a written case summary preserves: start fresh, inject the durable facts, re-look-up the time-sensitive ones. B trusts stale state. C carries the stale context along while distrusting it — the worst of both. D throws away the resolution details and burns customer goodwill.

**6. C** — Tone and empathy are behavioral guidance where occasional imperfection is tolerable — the appropriate domain of system-prompt instructions rather than a hook. A, B, and D are compliance rules with financial or security consequences, which is why they're hooked: any violation is unacceptable, so enforcement must be deterministic.

**7. D** — A malformed input is a validation error: name the field, state the expected format, and mark it correctable so the agent fixes the argument and re-calls in one step. A gives no correction path. B silently guesses intent inside the tool — hidden behavior that will misfire. C triggers retries of an input that will fail identically every time.

**8. A** — Tool descriptions should state boundaries — what the tool is for and what it is not for, naming the alternative. The agent chooses refunds because nothing signals exchanges are out of scope. B abuses naming to carry documentation. C teaches by failure at customer expense, structured error or not. D merges two flows with different semantics, creating a new selection problem inside one tool.

**9. C** — Selection reliability degrades as the tool count grows; the correction is scoped tool access — split by role so each agent carries only the handful of tools its job needs. A and D are cosmetic reorderings of an oversized surface. B adds latency to every call without reducing the decision complexity causing the errors.

**10. B** — For standard integrations, prefer existing community MCP servers; custom development is reserved for team-specific workflows. Zendesk CRUD is as standard as it gets. A is not-invented-here. C bypasses the tool interface the agent needs, hook or not. D creates an undifferentiated mega-tool — a selection and description problem waiting to happen.

**11. D** — Returning failures as successes is the silent-suppression anti-pattern: the agent cannot respond truthfully or recover from an error it never sees. The fix is explicit errors that surface. A trades one sentinel for another — still not an error the agent can reason about. B adds a verification round-trip to compensate for lying infrastructure. C helps engineers, not the customer being told falsehoods.

**12. A** — Frustration over a resolvable issue calls for acknowledgment plus immediate resolution — escalate only if the customer asks for a human. Sentiment is an unreliable proxy for complexity (B), and gating on a second sentiment reading (C) still routes by mood rather than capability. D resolves the issue but ignores a customer who needs to be heard — hurting the interaction anyway.

**13. B** — Policy gaps are an escalation trigger: the published policy is silent on competitor matching, so the agent has no authority to improvise (A), refuse definitively (C), or invent criteria (D). Escalating routes the exception to someone empowered to set precedent.

**14. C** — Multiple customer matches require clarification through additional identifiers, not heuristic selection. A is a heuristic (a phone number shared across the accounts makes it worse, not sufficient). B mutates customer data on a guess. D proceeds on the guess and merely documents it.

**15. D** — Multi-issue sessions need each issue's own data — order ID, amount, status, next action — persisted in a separate context layer rather than left to drift in conversational history. A and C constrain customers to fit the architecture. B bloats every response and still relies on the model keeping the issues straight.

**16. A** — The decomposition is the failure point: the coordinator collapsed a broad topic into one domain's subtasks. Fix decomposition — enumerate the topic's major domains first, then generate subtasks against that enumeration with coverage criteria. B patches queries downstream of bad assignments. C adds a guessing agent. D documents the gap instead of closing it.

**17. C** — In hub-and-spoke architecture, aggregation belongs to the coordinator: one place for completeness checks, ordering, and error handling before synthesis. A gives the consumer an orchestration job it isn't built to validate. B rebuilds coordinator responsibilities inside a message bus. D verifies delivery without anyone owning the whole picture.

**18. B** — `fork_session` creates independent branches from a shared analysis baseline — each framework develops in isolation without re-paying for the 400-document analysis and without cross-contamination. A resumes one lineage twice into the same history. C re-buys the corpus analysis in full, twice. D lets each framework bias the other.

**19. D** — Match decomposition to predictability: the six-section weekly digest is a fixed prompt chain; novel ad-hoc investigations need dynamic decomposition that adapts to findings. A adds adaptive overhead to clockwork. B scripts the unscriptable. C assigns each pipeline the wrong pattern.

**20. A** — Independent gathering tasks parallelize by emitting all six Task calls in a single coordinator response. B changes what is fetched, not the serialization. C makes each sequential step cheaper but keeps six round-trips. D starts synthesis before its inputs exist.

**21. C** — Natural-language completion markers are the classic termination anti-pattern: they fire spuriously (the model discusses "DONE"), get paraphrased away, and duplicate what `stop_reason` already provides reliably. A normalizes the anti-pattern. B structures the wrong mechanism — a JSON marker is still a string the model has to remember to emit. D patches one failure mode of a signal that shouldn't be the signal.

**22. D** — Zero matches from a valid query is a *successful* search; conflating it with failure caused a pointless failover. Tools must distinguish valid empty results from access failures. A substitutes wrong results for honest emptiness. B adds infrastructure to disambiguate what the response shape should state on its own. C keeps the ambiguity and hides the distinction in logs the agent never sees.

**23. B** — Descriptions should document input formats, limits, and edge-case behavior — a 256-character truncation is exactly the constraint an agent needs to compose valid queries. A and C are metadata that don't prevent the failure. D is a disclaimer, not a contract.

**24. A** — The agent prefers the tool it understands; "Searches arXiv" gives no case for selection. Enhance the description — what it searches, what it returns, when to prefer it over general web search. B removes a tool still needed for non-academic queries. C teaches one keyword pattern rather than the underlying preference. D — ordering isn't a documented selection mechanism; descriptions are.

**25. C** — Subagents should recover locally from transient failures (retry the parse) and, failing that, continue the assignment — propagating only the unresolvable failure with partial results. Nine parsed documents is a report, not a total failure. A pretends timeouts can be configured away. B re-runs everything including the nine successes. D addresses throughput, not the give-up-entirely logic.

**26. D** — Conflicting values from credible sources are completed analysis, not noise: include both, annotated with source and methodology, and let the coordinator decide reconciliation before synthesis. A invents a number no source reported, however carefully footnoted. B stalls the pipeline where annotation suffices. C encodes an arbitrary tiebreak (recency) as truth.

**27. B** — Synthesis can only be as accurate as its inputs; requiring the analysis agent to attach metadata — dates, source locations, methodological context — to every finding removes the inference that produces the misdating. A sends synthesis hunting for facts upstream already had. C flags the symptom. D asks a better model to guess better.

**28. D** — When the downstream consumer's budget is limited, change what upstream produces: structured key facts, citations, and relevance scores instead of excerpts plus reasoning narratives. A splits the material and loses cross-cutting synthesis. B scales cost to fit waste. C adds a lossy compression stage in the least-informed position.

**29. A** — Provenance must carry the source's own characterization: structured findings that keep "preliminary, n=12" attached to the claim, with synthesis required to preserve the qualifiers. B audits after the flattening. C and D exclude or demote evidence rather than representing it honestly.

**30. C** — The crash-recovery pattern: agents export their own state to a known location as they work; on resume the coordinator loads the manifest and injects prior state, resuming instead of restarting. A restarts from zero, just automatically. B doubles cost for a coin flip. D schedules around failure instead of recovering from it.

**31. B** — Resumption fits when prior context is mostly valid; the practice is informing the resumed session of the specific changes (the two auth modules, PR #412) for targeted re-analysis. A discards a mostly-valid session over one localized refactor. C leaves stale beliefs live until the agent happens to re-read. D re-pays for the 95% that didn't change.

**32. A** — The canonical loop: continue while `stop_reason` is `"tool_use"` (execute, append results, send), exit on `"end_turn"`. B keys on text presence — meaningless. C makes an iteration cap the completion condition instead of anything the API reports. D parses punctuation.

**33. C** — Heterogeneous formats from multiple MCP servers are normalized deterministically in a `PostToolUse` hook — one canonical path form before the model reasons. A and D make the model do conversions probabilistically on every comparison. B sacrifices capability to dodge an integration with a standard solution.

**34. D** — Tool restrictions belong in the subagent's AgentDefinition: a doc-writer defined with Read, Grep, and Write cannot run builds. A is advisory, examples or not. B has the coordinator babysitting instead of configuring. C punishes output latency after the fact.

**35. B** — Locating where a string originates is content search: Grep for the error message. A guesses the filename encodes the concept. C assumes the answer's location before searching. D searches history for what the working tree can answer directly.

**36. C** — With byte-identical repeated blocks, unique anchoring is unreliable: in a generated file the surroundings are often identical too, so progressively widening the anchor (A) can never terminate. The documented fallback is Read the file, then Write it back with the single intended change. B makes five changes to achieve one. D is disproportionate and assumes a regeneration path exists.

**37. A** — Personal preferences belong in user-level `~/.claude/CLAUDE.md`: applied for you, invisible to teammates, never in the repo. B ties preferences to file ownership, which changes. C makes your own defaults opt-in for you. D — CLAUDE.md is a single committed file; a "gitignored section" of a tracked file isn't a mechanism that exists.

**38. D** — `allowed-tools` is the structural control: a read-only toolset means no prompt defect can execute `git push` — the capability isn't there. A relies on developers reading plans carefully every time. B mitigates one command's damage. C shrinks the blast radius instead of removing the blast.

**39. C** — Project-scoped commands in `.claude/commands/` are version-controlled and available to anyone who clones — zero setup. A, B, and D describe distribution mechanisms Claude Code doesn't have (image installs, account sync, this built-in).

**40. B** — Conventions tied to a file type spread across many directories are the glob-rule case: `.claude/rules/` with `paths: ["**/*.sql"]` loads them exactly when matching files are edited. A covers one directory of many. C loads SQL rules in every session forever. D loads them only when invoked.

**41. A** — A well-understood, single-function change with a clear location is direct execution. Plan mode (B), exploration subagents (C), and session forking (D) each add process to a task with no design uncertainty to resolve.

**42. C** — Architectural scope (45+ files), multiple valid strategies, and rollback implications are plan mode's explicit criteria: explore, compare, commit to a design before edits. A begins mechanically before the strategy exists — the per-file mechanics aren't the risk, the transaction semantics are. B checkpoints a process that lacks a design. D delegates the decision along with the labor.

**43. D** — Undecided design dimensions plus suspected unknown-unknowns is the interview pattern's home case: Claude asks about traffic shape, burst tolerance, rejection semantics, and failure modes before implementation. A picks a "standard" without your requirements. B critiques a spec limited by the same blind spots. C discovers requirements in staging incidents — later and more expensively than an interview.

**44. A** — When prose descriptions produce inconsistent interpretations, concrete input/output example pairs — including an edge case — pin down the transformation. B defines words instead of behavior. C formalizes ambiguity in stronger prose without resolving it. D documents the library, not your expected output.

**45. B** — `@import` exists for exactly this: each package's CLAUDE.md references the single `standards/security.md`, one source of truth included where relevant. A works by filesystem trickery and breaks portability. C guarantees drift across six copies. D mentions the file without loading it.

**46. D** — `-p` / `--print` is non-interactive mode: process, print, exit — cron-safe. A, B, and C are invented flags; none exists in Claude Code.

**47. A** — The re-review pattern: prior findings go into context, and the bot reports only new issues plus a note on which prior ones remain unaddressed — no duplicates, threads preserved. B leaves post-push changes unreviewed. C destroys the discussion threads reviewers asked to keep, hook or no hook. D abandons the inline-comment requirement entirely.

**48. C** — Guaranteed field names and types come from `--output-format json` with `--json-schema`: schema-enforced structure for machine parsing. A and D parse unguaranteed output defensively or hopefully — plain text carries no schema guarantee at all. B is an invented flag.

**49. B** — Effective criteria are specific and categorical: flag only when the comment's claimed behavior contradicts the code. A is confidence-based filtering, which demonstrably fails to move precision. C caps volume without defining quality. D changes where noise lands, not whether it's noise.

**50. D** — False-positive-heavy categories destroy trust in the whole tool: developers who learn to skim past style noise skim past the accurate security findings too. That contagion is why the noisy category is urgent. A, B, and C invent indirect costs; the documented mechanism is trust erosion.

**51. A** — Ambiguous cases are the targeted-few-shot case: examples of exactly these situations, showing the chosen tool *and the reasoning* over plausible alternatives, teach judgment the model generalizes. B describes the mapping in prose — already too coarse for edge cases. C removes a legitimate output. D hardcodes one answer to varied situations.

**52. B** — Format consistency comes from demonstration: complete sample summaries already in the exact required table. Description (D), even stricter, keeps producing drift; that's the observed failure. A regenerates against a template until lucky rather than teaching the format up front. C reduces variance around a format the model hasn't internalized.

**53. C** — The correct trio: `"auto"` permits text-only responses; `"any"` mandates some tool call, model's choice; forced selection mandates one named tool. A describes "any." B invents count semantics. D — forcing applies per-request, not until reset.

**54. D** — A structured `detected_pattern` field ties every suggestion to the construct that triggered it, so dismissals aggregate into pattern-level insight — the systematic feedback loop. A and C produce anecdote at low volume. B counts dismissals without capturing what caused them.

**55. A** — The design document was never in the input; no retry recovers information that isn't there. Provide the document, or scope the review to available material. B and C retry harder at reading an absent file. D deletes a category wholesale when the fix is supplying context.

**56. B** — Batch fits latency-tolerant, non-blocking work: the nightly report is ideal; a merge-blocking gate cannot ride a no-SLA, up-to-24-hour service. A ignores the blocking constraint. C overcorrects — the report genuinely fits. D prices workloads instead of matching latency requirements.

**57. D** — `custom_id` is the Batch API's request/response correlation mechanism: set it to the PR number at submission, read it on each result. A relies on ordering the API doesn't promise. B trusts model output for plumbing. C abandons batching's economics to avoid using the feature built for this.

**58. C** — Generation and review must be separated: an independent review instance receives the diff without the generator's session context, avoiding the self-approval bias that shipped the bad fix. A and B prompt or repeat a structurally biased review. D limits exposure without fixing the reviewer.

**59. B** — Declining depth across files plus contradictory verdicts on mirrored code are attention dilution; the restructure is per-file passes for local issues and a separate integration pass for cross-file consistency. A averages two diluted passes instead of restructuring the review. C constrains developers to fit the tool. D — token budget doesn't reallocate attention across a long input.

**60. A** — Confidence becomes routable only after calibration: measure accuracy at each score level against labeled outcomes and place the threshold where precision meets the bar. B trusts raw self-report at the extreme — where miscalibration concentrates. C discards per-finding signal for category stereotype. D posts everything anyway, labeling the risk instead of routing it.

---

*End of Practice Exam 9.*
