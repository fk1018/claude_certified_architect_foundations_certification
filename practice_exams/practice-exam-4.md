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

- A) Setting `tool_choice: "auto"` on the follow-up request so the model is merely permitted, not required, to call another tool.
- B) Clearing the previous assistant turn from the conversation history before sending the retry request.
- C) Re-registering the tool definitions and their structured JSON schemas on every request, in case schema drift caused the rejection.
- D) Appending each executed tool's result to the conversation as a `tool_result` block, matched to its `tool_use` ID, before sending the next request.

**Question 2.** Gift-card purchases are non-refundable by policy; the agent should route those customers to a goodwill-credit workflow instead. The rule lives in the system prompt today, and violations still occur monthly. What is the correct mechanism?

- A) Add several gift-card refund examples to the few-shot section of the system prompt and hope the model generalizes.
- B) Intercept `process_refund` calls with a hook that blocks refunds on gift-card line items and redirects the agent to the goodwill-credit workflow.
- C) Add a second model that reviews every refund decision against the policy list before execution, adding a review step that itself can be persuaded like the first.
- D) Move the gift-card exclusion rule into the `process_refund` tool description and trust the agent to apply it.

**Question 3.** Account email changes must be preceded by a completed identity verification in the same conversation. Reviewing incidents, you find the agent occasionally performs the change when a persuasive customer insists verification "already happened last week." What prevents this?

- A) Block `update_email` behind a programmatic gate requiring a completed verification step in the current session, not what the conversation claims.
- B) Add a system prompt instruction telling the agent never to trust customer claims about prior verification, however persuasive.
- C) Add a structured set of few-shot examples showing the agent politely refusing to change an email without completed verification.
- D) Generate a daily audit report of all email changes for the fraud team to review after the fact, once any compromise has already occurred.

**Question 4.** A billing dispute arrives with symptoms that don't match any known pattern — the charge exists in one system but not another. There is no established runbook. How should the agent approach the investigation?

- A) Follow the standard billing-dispute script anyway, normalizing every case into the same steps regardless of fit.
- B) Escalate immediately, on the reasoning that no runbook existing means no path forward exists.
- C) Form a hypothesis from the mismatch, run a lookup, and let each finding determine the next step.
- D) Run every available lookup tool once up front, then decide on a course of action from whatever the results happen to turn up.

**Question 5.** A support case is reopened the next morning through a new chat. Yesterday's session contains extensive tool results (order status, refund state) that may have changed overnight, plus the negotiated resolution details. How should the agent be initialized?

- A) Resume yesterday's session unchanged, since continuity with the prior conversation matters most for the customer.
- B) Resume yesterday's session but instruct the agent to distrust any of its own prior tool results, without telling it which ones changed.
- C) Start fresh with no context at all and let the customer re-explain the whole situation.
- D) Start a new session with an injected structured case summary and re-run only the time-sensitive lookups.

**Question 6.** You maintain four agent behavior requirements. Three are enforced with hooks. Which one is appropriately left to system-prompt guidance alone?

- A) Responses should acknowledge the customer's frustration before presenting solutions — appropriate for system prompt guidance alone, since a rare miss here carries no compliance risk.
- B) Refunds above $500 must be approved by a human before the funds move.
- C) Identity must be verified before any account mutation is permitted — enforced with a hook rather than left to prompt wording, since a persuasive customer can talk past instructions.
- D) Refunds must be routed only to the original payment method, never a substitute.

**Question 7.** The agent calls `lookup_order` with the date "next Tuesday" in a field expecting `YYYY-MM-DD`. How should the tool respond so the agent can recover in one step?

- A) Return `isError` with a generic "invalid request" message, leaving the agent to guess what to try next without any hint about which field or format failed.
- B) Return a structured validation error naming the field, the expected `YYYY-MM-DD` format, and marking it correctable.
- C) Silently interpret "next Tuesday" server-side, normalizing it against the current date without telling the agent what happened.
- D) Return a transient-category error so the agent's retry logic re-sends the identical malformed call.

**Question 8.** Customers asking for exchanges keep getting refunds — the agent calls `process_refund` because nothing tells it that exchanges are handled elsewhere. What is the highest-leverage change?

- A) Rename `process_refund` to `process_refund_not_exchange` so the boundary is visible in the tool name itself.
- B) Add a hook that blocks exchange-context refund calls and lets the resulting error teach the agent the boundary.
- C) State the scope boundary in the `process_refund` description and point to `create_exchange` for exchange requests.
- D) Merge refunds and exchanges into a single `resolve_return` tool that handles both cases internally.

**Question 9.** After a quarter of feature growth, the resolution agent now has 17 tools spanning refunds, subscriptions, loyalty, shipping, and marketing consent. Selection errors have risen steadily with each addition. What is the architectural correction?

- A) Split the tool surface by role into specialized agents so each carries only the 4–6 tools its job needs.
- B) Sort the tools array by usage frequency so the model encounters common tools earlier in the list.
- C) Add a structured reasoning checklist before every tool call to slow the model down and reduce mistakes.
- D) Shorten every tool description so the full 17-tool catalog fits into a smaller context budget.

**Question 10.** Your team needs standard Zendesk operations (create ticket, add note, change status) available to the agent. An engineer has begun writing a custom MCP server for it. What guidance applies?

- A) Continue the custom build — support tooling is too business-critical for community code.
- B) Skip MCP entirely and call the Zendesk REST API directly from a hook instead.
- C) Wrap the Zendesk API in your existing backend and expose the whole thing as one mega-tool.
- D) Adopt an existing community MCP server for the standard integration; reserve custom server effort for workflows unique to your team, where no ready-made option exists.

**Question 11.** A platform wrapper catches all tool exceptions and returns `{}` with a success status "to keep conversations smooth." Yesterday the agent told a customer their refund was complete when `process_refund` had actually thrown. What is the design lesson?

- A) Have the wrapper return `null` instead of `{}`, even though the agent still can't tell what went wrong from either sentinel.
- B) Have the agent verify every refund with a separate follow-up lookup call after each attempt.
- C) Stop suppressing errors as fake successes — surface failures as structured errors so the agent can respond truthfully.
- D) Add better logging to the wrapper so engineers notice these incidents sooner after the fact.

**Question 12.** A customer writes: "This is the THIRD time I'm contacting you people about this broken blender!!" The issue is a standard damage replacement with photo evidence — fully within the agent's capability. Sentiment analysis scores the message as highly negative. What should the agent do?

- A) Escalate to a human immediately, since high negative sentiment signals a case the bot shouldn't touch.
- B) Acknowledge the frustration and repeated contact, then resolve the replacement now, escalating only if asked.
- C) Offer a discount code first to defuse the sentiment before addressing the actual replacement issue.
- D) Process the replacement silently, treating the complaint as pure data to execute against without acknowledging the tone at all.

**Question 13.** A customer requests a price match against a competitor's advertised price. Your published policy covers price adjustments for your own site's price drops but says nothing about competitor matching. The agent should:

- A) Apply the own-site adjustment policy by analogy, since it is the closest existing rule available.
- B) Decline the request outright, since the published policy never authorizes competitor price matching, and the safest reading of an unwritten rule is no.
- C) Ask for a structured price-comparison form and decide based on the size of the gap.
- D) Escalate — the policy is silent on this request, and silence is a trigger, not something to resolve alone.

**Question 14.** `get_customer` returns three accounts for "Chris Martin" — different addresses, one shared phone number. The agent currently picks the account with the most recent order. What should it do instead?

- A) Ask for an additional identifier — order number, account email, billing zip — and match on that.
- B) Pick the account matching the phone number the customer wrote in from, since it's shared context.
- C) Merge the three accounts into one, since they likely belong to the same person anyway.
- D) Proceed with the most recent order's account, flagging the conversation for later review on the assumption someone will catch the mistake before it matters.

**Question 15.** In sessions where a customer raises several issues, the agent confuses details between them as the conversation grows — attributing order 8817's status to order 9902's refund. What is the recommended context structure?

- A) Limit customers to raising two issues per conversation so cross-issue confusion can't occur.
- B) Repeat every issue's full details in every agent response, even though this bloats every response and still leaves accuracy up to how well the model tracks repetition.
- C) Persist each issue's structured data — order ID, amount, status, next action — in a layer outside the conversation history.
- D) Handle issues strictly one at a time, refusing to discuss a new one until the current one closes.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Reports on "the impact of remote work" consistently cover only the technology industry; healthcare, education, and manufacturing never appear. The coordinator's decomposition logs show subtasks like "remote work in software companies" and "developer productivity at home." What is the fix?

- A) Instruct the search agent to broaden every query it receives against a fixed structured checklist of other industries.
- B) Fix the coordinator's decomposition: enumerate the topic's major domains first, then generate subtasks against that enumeration with coverage checks.
- C) Add a fourth subagent whose whole job is covering whatever industries the other three subagents happen to miss that week.
- D) Have the synthesis agent pad the final report with general, uncited knowledge about industries nobody actually researched, to create an appearance of coverage.

**Question 17.** Each subagent currently posts its findings directly into a shared results channel, and the report agent assembles whatever it finds there. Findings arrive out of order, some overwrite others, and nobody detects missing pieces. Which component should own result collection, and why?

- A) The report agent, since it consumes the collected results anyway and sees the whole picture last.
- B) The shared channel itself, upgraded with ordering and deduplication logic.
- C) Each subagent should verify its own delivery with a read-back check against the channel.
- D) The coordinator — aggregation is its job in hub-and-spoke designs, giving one place for completeness and ordering checks.

**Question 18.** After an expensive shared analysis of a 400-document corpus, you want to evaluate two competing report frameworks — thematic versus chronological — each developed independently from that same analysis. What mechanism does the Agent SDK provide?

- A) `fork_session` — branch the shared analysis baseline into two independent lines, one per framework.
- B) `--resume` the analysis session twice, once for each framework, from the same transcript.
- C) Run the expensive 400-document analysis twice from scratch, once in a fresh session per framework, paying the full analysis cost a second time.
- D) Develop both frameworks alternately within the single ongoing session, switching context as needed.

**Question 19.** Your system produces (a) a weekly market digest with the same six sections every week, and (b) ad-hoc deep investigations of novel questions. How should the two pipelines be decomposed?

- A) Both dynamic — research outcomes are inherently unpredictable regardless of how repetitive the task looks on paper, since novel facts can surface even in routine sections.
- B) Both fixed — a single structured pipeline shape simplifies operations across the board, even for questions nobody has asked before.
- C) The digest as a fixed chain of predictable stages; the investigations with decomposition that adapts to findings.
- D) The digest dynamic and the investigations fixed, since digests leave more room for creative structure.

**Question 20.** Monday's run must gather updates from six independent news domains before synthesis. The coordinator currently delegates them one per turn. What single change most reduces wall-clock time?

- A) Cache Friday's results and fetch only whatever changed since, to shrink the total workload.
- B) Have the coordinator emit all six Task calls in one response so subagents run in parallel.
- C) Reduce each domain's search depth so the six sequential runs finish faster overall.
- D) Move synthesis earlier so it overlaps with the last couple of searches still running, at the cost of synthesizing on incomplete input.

**Question 21.** A reviewer flags this coordinator code: `if "DONE" in assistant_text: break` — paired with a system prompt instructing the model to "say DONE when research is complete." What is the professional assessment?

- A) Acceptable — explicit completion markers in assistant text are a common, well-understood convention.
- B) The marker should just be more unusual, like "##COMPLETE##", to cut down on false positives.
- C) Both the prompt and the check should use a JSON field instead of a bare string.
- D) Termination should key off `stop_reason` (`"end_turn"`), not a marker that can appear spuriously or get paraphrased away.

**Question 22.** Researching an extremely niche topic, the search subagent's query legitimately matches nothing. The tool returns an error, and the coordinator logs "search infrastructure degraded" and switches to a fallback provider — wasting a cycle. What is the correct contract?

- A) Zero matches is a successful, empty-result query; errors are reserved for access failures, and the two must stay distinguishable.
- B) Return the closest partial matches instead of an empty set, without validating whether they're actually relevant to the query.
- C) Have the coordinator ping a health-check endpoint before it interprets any error as infrastructure trouble, adding a network round trip to every failed query just to guess at its cause.
- D) Let empty results and failures share one structured response shape, as long as the log message tells them apart.

**Question 23.** Your `search_corpus` tool truncates queries over 256 characters — silently. Agents regularly compose long, careful queries whose critical qualifiers get cut off, returning oddly irrelevant results no one can explain. Beyond fixing the truncation, what should the tool description have included?

- A) A schema version field in the description so agents know the tool's behavior might change later.
- B) Usage statistics in the description showing what query lengths are typical in practice, without ever stating the hard limit that actually causes the failure.
- C) The 256-character limit and what happens beyond it, documented as part of the tool description.
- D) A general warning that search quality can vary depending on the topic searched.

**Question 24.** The document analysis agent has access to a purpose-built `arxiv_search` MCP tool but keeps using the generic built-in WebSearch for academic queries, returning blog summaries instead of papers. `arxiv_search`'s description is "Searches arXiv." What is the recommended fix?

- A) Remove WebSearch from the agent entirely so `arxiv_search` wins by default with no competition.
- B) Rewrite the `arxiv_search` description to state what it searches, what it returns, and when to prefer it over web search.
- C) Add a system prompt rule to always use `arxiv_search` whenever a query contains the word "paper."
- D) Lower WebSearch's priority through tool ordering in the agent's configuration, on the assumption that list position affects which tool the model picks.

**Question 25.** The document analysis agent abandons its entire assignment the first time a PDF-parsing call times out, reporting total failure to the coordinator even when 9 of 10 documents parsed fine. What error-handling design is missing?

- A) A longer parsing timeout, on the theory that a bigger number makes timeouts stop happening.
- B) A coordinator-side retry of the entire document-analysis task from the beginning, re-paying for the nine documents that already parsed successfully the first time.
- C) Parallel parsing of all ten documents so a single timeout can't serialize the rest.
- D) Local retry-with-backoff for the failed document, then continue with the rest and report only the unresolved one.

**Question 26.** While analyzing a corpus, the analysis agent finds two credible papers reporting incompatible efficacy figures. It currently discards the outlier and reports one clean number. What should it do instead?

- A) Report the average of the two figures inside a structured confidence-interval annotation, folding the disagreement into one number.
- B) Hold both papers back from synthesis entirely until a human adjudicates the discrepancy.
- C) Keep both values, annotated with source and methodology, and let the coordinator decide how to reconcile them.
- D) Re-run the analysis with instructions to prefer whichever paper is more recent, treating publication date as a stand-in for methodological quality.

**Question 27.** The synthesis agent regularly misdates events and attributes findings to the wrong methodology. Upstream, the analysis agent's outputs are well-written prose summaries. What structural requirement fixes this?

- A) Require the analysis agent to emit structured findings carrying dates, sources, and methodology as metadata, not prose.
- B) Give the synthesis agent web search access so it can verify dates itself, duplicating research the analysis agent already did once.
- C) Have the synthesis agent flag any date it is personally unsure about.
- D) Use a stronger model for synthesis so it infers metadata more accurately from prose.

**Question 28.** Your synthesis agent's context budget is small, and upstream agents currently send it full document excerpts plus their complete reasoning narratives. Synthesis truncates and quality collapses on large topics. What is the recommended change?

- A) Rotate synthesis across three agents, each handling a third of the source material, then stitch the three partial syntheses back together afterward.
- B) Have upstream agents return structured facts, citations, and relevance scores instead of full excerpts and reasoning chains.
- C) Raise the synthesis agent's context budget and simply accept the added cost.
- D) Have synthesis summarize its own input first, then synthesize that summary.

**Question 29.** A source paper carefully describes its results as "preliminary findings from a small pilot (n=12)." The final report states the same results as established fact. Where should this be prevented?

- A) In report review — a final pass that re-checks every claim in the report against its sources, catching mismatches only after the flattening has already happened upstream.
- B) By excluding small pilot studies (like n=12) from the research pipeline entirely.
- C) By having the search agent rank small-sample studies lower in its results.
- D) In the structured findings passed downstream — subagents preserve the source's own characterization and methodological context alongside each claim.

**Question 30.** Your overnight research runs sometimes die partway (provider outages). Restarting from zero wastes hours of completed subagent work. What recovery design does the guide recommend?

- A) Each agent exports structured progress to a known location; on resume the coordinator loads it and re-injects prior state.
- B) Wrap the entire run in a retry loop with exponential backoff between attempts.
- C) Run two identical pipelines in parallel and keep whichever one finishes first, paying twice for redundancy instead of resuming the one that already ran most of the way.
- D) Schedule overnight runs during the provider's historically most stable hours.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** You resume yesterday's architecture-investigation session. Overnight, one teammate's PR merged, refactoring the two authentication modules the session had analyzed; nothing else changed. What is the efficient continuation?

- A) Start a brand-new session, since any change to the codebase invalidates a prior investigation that's still accurate for everything the PR didn't touch.
- B) Resume and let the agent notice the refactor naturally whenever it next reads those files.
- C) Resume and tell the agent specifically that PR #412 refactored the two auth modules, asking for targeted re-analysis.
- D) Resume and re-run the entire investigation from scratch, just to be safe.

**Question 32.** Which loop skeleton is correct for an Agent SDK/API tool-use loop?

- A) `while response.content contains text: send(...)` — loop until no text remains in the reply.
- B) `while response.stop_reason == "tool_use": execute tools; append results; send(...)` — exit on `"end_turn"`.
- C) `for i in range(MAX_STEPS): send(...)` — treat the iteration cap itself as the completion signal.
- D) `while not response.text.endswith("."): send(...)` — which fails the moment a response ends in a code block or list.

**Question 33.** Your agent uses three file-related MCP tools from different vendors: one returns absolute paths, one repo-relative paths, one `file://` URIs. The agent regularly treats the same file as three different files. What is the cleanest fix?

- A) Add a system prompt table explaining each vendor's path convention for the model to apply by hand.
- B) Standardize on one vendor's file tools and drop the other two entirely.
- C) Instruct the agent to canonicalize paths itself before comparing any two of them.
- D) A `PostToolUse` hook that normalizes every path to one canonical form before the model ever sees it.

**Question 34.** Your doc-writer subagent's AgentDefinition grants the full toolset. Last week it ran `npm run build` "to verify the docs examples compile," consuming twenty minutes. Its actual job needs only Read, Grep, and Write. Where is the fix made?

- A) In the subagent's AgentDefinition — restrict its tools to Read, Grep, and Write, matching what its role actually needs.
- B) In the doc-writer's system prompt, with an instruction not to run builds.
- C) In the coordinator, using a hook that watches subagent tool calls and cancels any that run long.
- D) In CI, which should reject documentation PRs that took unusually long to produce.

**Question 35.** A stack trace shows the error string "connection pool exhausted" but the codebase is unfamiliar and you don't know which module raises it. What is the right first tool call?

- A) Glob for `**/pool*` and read whatever files that pattern happens to match.
- B) Read the database configuration files first, since pooling usually lives near a structured config block, though the raising code could be anywhere.
- C) Grep the codebase for the literal error string to find where it's raised.
- D) Run `git log --grep "pool"` to look for commits that mention pooling.

**Question 36.** The agent must change one occurrence of a YAML block that appears, byte-identical, five times in a generated config file. Edit keeps failing on non-unique anchor text. What is the reliable approach?

- A) Widen the anchor to include more surrounding lines until it becomes unique, falling back further if needed, though in a generated file the five occurrences are often identical for lines around them too.
- B) Read the file, then write it back with only the one intended occurrence changed.
- C) Edit with `replace_all`, then revert the four unwanted changes with four separate follow-up edits.
- D) Delete the file and regenerate it from the template with the change already applied.

**Question 37.** You put your personal preferences — two-space indent debates, your favorite commit-message style — into the project's CLAUDE.md. Teammates are now complaining that Claude nags them about your preferences. Where do personal preferences belong?

- A) In a `.claude/rules/` file scoped only to the files you personally own in the repo.
- B) In the project CLAUDE.md, but with your name prefixed so teammates know to ignore it, even though it still loads and nags everyone by default.
- C) In a skill that only you ever invoke, kept out of everyone else's path.
- D) In your user-level `~/.claude/CLAUDE.md`, which applies only to you and never travels to teammates through the repo.

**Question 38.** Your `/analyze-arch` skill only ever needs to read code and produce a report, but during one run it executed `git push` from a leftover instruction in its prompt file. Beyond fixing the prompt, what structural control applies?

- A) Set `allowed-tools` in the skill frontmatter to a read-only set, so no execution tool is even available.
- B) Add a pre-run confirmation step where a developer approves the skill's plan before it executes.
- C) Have the skill run `git stash` first so any push it triggers contains nothing.
- D) Move the skill to user scope, shrinking the blast radius of a mistake without removing the capability that caused it.

**Question 39.** A new engineer clones the repo, opens Claude Code, and types `/deploy-check` — the team's pre-deployment verification command — and it works immediately with no setup. What makes this possible?

- A) The command was installed globally by the infrastructure team's standard laptop image, which every new hire's machine happens to receive on day one.
- B) It's defined in `.claude/commands/` in the repo, so project commands travel with version control.
- C) Claude Code synced the command over from the previous engineer's account automatically.
- D) `/deploy-check` is simply a built-in Claude Code command available to everyone.

**Question 40.** Your SQL conventions (naming, mandatory `WHERE` review for deletes, migration header format) should apply whenever Claude edits any `.sql` file — they sit in `db/`, `analytics/`, and various service folders. What is the correct configuration?

- A) A CLAUDE.md placed in `db/`, since it's the largest of the folders containing SQL.
- B) The root CLAUDE.md with a dedicated, structured "SQL rules" section, loaded into every session whether or not SQL is involved.
- C) A `.claude/rules/` file with `paths: ["**/*.sql"]`, loading whenever a matching file is edited anywhere.
- D) A `/sql-mode` skill that developers are expected to invoke before doing database work.

**Question 41.** The ask: add a validation check rejecting end dates earlier than start dates in one form handler — a well-understood, single-function change. Which workflow?

- A) Plan mode, then implementation — date logic is subtle enough to warrant the extra step.
- B) Send an Explore subagent to produce a structured report on date handling across the whole repo first.
- C) Use `fork_session` to try two different validation styles independently before choosing one.
- D) Direct execution — a well-scoped, single-function change with a clear location doesn't need planning overhead.

**Question 42.** You're replacing the ORM across a service — 45+ files, three plausible migration strategies with different transaction semantics, and rollback implications. Which workflow?

- A) Plan mode first — explore the codebase, compare the three strategies, and commit to a design before editing.
- B) Direct execution, since each individual file's edit becomes mechanical once the pattern is established, even though no pattern exists yet.
- C) Direct execution with `--resume` checkpoints inserted after every ten files are converted.
- D) Delegate the whole migration to a single subagent to keep the main context clean.

**Question 43.** You're implementing a rate limiter but haven't decided on the algorithm, burst policy, or what happens to rejected requests — and you suspect there are failure modes you haven't considered. What gets you the best design conversation?

- A) Ask Claude for the industry-standard rate limiter design and implement whatever it names, without ever stating your own traffic shape or burst tolerance requirements.
- B) Write a best-guess spec yourself and have Claude critique it afterward.
- C) Use the interview pattern — have Claude ask about traffic shape, burst tolerance, and failure modes before implementation.
- D) Implement token-bucket first and iterate later based on production behavior.

**Question 44.** Claude keeps misinterpreting your description of a log-line transformation ("extract the request ID and normalize the timestamp — you know, standard format"). Three attempts, three different behaviors. What input finally pins it down?

- A) A glossary defining "request ID," "normalize," and "standard format" in precise terms.
- B) Two or three concrete input/output line pairs, including one edge case, showing exactly what's expected.
- C) A longer description written in RFC-style MUST/SHOULD language, formalizing the same ambiguity in stricter-sounding words rather than removing it.
- D) A link to the logging library's own documentation for the format in question.

**Question 45.** Security standards used by all six packages in your monorepo live in `standards/security.md`. Each package has its own CLAUDE.md. How do packages include the shared standards without copying them?

- A) Symlink `security.md` into each of the six package directories in the monorepo.
- B) Paste the content into each package's CLAUDE.md and remember to update all six on every change.
- C) Mention in each CLAUDE.md that a security standards file "exists somewhere in the repo."
- D) Use `@import` in each package's CLAUDE.md to pull in `standards/security.md` from one source of truth.

---

## Scenario D: Claude Code for Continuous Integration (Questions 46–60)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 46.** A nightly cron job needs Claude Code to summarize the day's merged changes and write the summary to a file. Which flag makes the invocation suitable for cron?

- A) `-p` (`--print`) — process the prompt, print the result, and exit without any interactive input.
- B) `--cron`, a flag that registers the command directly with the system scheduler.
- C) `--quiet`, which suppresses the interactive UI but still returns a structured session waiting on stdin.
- D) `--yes`, which auto-confirms any interactive prompts that would otherwise appear.

**Question 47.** Developers complain that after each push, the review bot re-posts its full findings list, burying the thread. The findings are usually the same unresolved items plus one or two new ones. What re-review design fixes the noise?

- A) Run the bot only once, on first PR open, and never again after that.
- B) Have the bot delete its old comments before posting the fresh full list each time.
- C) Feed prior findings into the re-review context and post only what's new, noting what's still unaddressed.
- D) Post all findings into a single comment that gets continuously edited in place, so nothing ever appears as a fresh notification developers would actually see.

**Question 48.** Your pipeline must transform Claude's review findings into your internal defect-tracker format. The transformation code needs guaranteed field names and types from Claude's output. Which invocation provides that?

- A) `claude -p "..." | jq` with defensive null checks scattered around every field, hoping the shape stays close enough to keep working.
- B) `claude -p "..." --output-format json --json-schema findings-schema.json` for schema-enforced output.
- C) `claude -p "..." --strict` to switch the model into a more careful output mode.
- D) `claude -p "..."` with a prompt instruction telling the model to "output valid JSON."

**Question 49.** Your comment-accuracy checker flags dozens of harmless doc comments per PR ("this comment could be more precise"). You want it to flag only real problems. Which criterion should replace the current "check that comments are accurate" instruction?

- A) "Only flag comments you are highly confident are wrong," relying on the model's own certainty.
- B) "Flag at most three comments per pull request," capping volume rather than defining quality, so genuine problems still slip through once the cap is hit.
- C) "Prefer flagging comments on public APIs over internal helpers," a rule about location, not accuracy.
- D) "Flag a comment only when its claimed behavior contradicts what the code actually does" — a specific, categorical rule rather than an open-ended judgment.

**Question 50.** Metrics show your security-review category is highly accurate, but the style category floods PRs with noise. A teammate argues style can wait since security "is what matters." Why does the guide say the style noise is urgent anyway?

- A) High false-positive categories erode trust in the whole tool — developers start ignoring accurate findings along with noisy ones.
- B) Style issues compound into security issues if they're left unaddressed for long enough.
- C) Noise adds token costs that show up in the structured cost-monitoring dashboard, and token costs dominate the tool's overall operating budget more than any accuracy concern the team has raised.
- D) The style category's volume statistically buries the security findings inside long comment lists.

**Question 51.** Your CI bot has three response tools: `comment_inline`, `open_issue`, and `request_changes`. For clear-cut cases it chooses well, but for ambiguous ones (a real bug that's out of the PR's scope; a severe issue in unchanged code) it picks inconsistently. What most improves these decisions?

- A) A decision matrix written in prose that maps issue attributes to the three tools, listed once in the system prompt for every case at once.
- B) Remove `open_issue` from the toolset so there are simply fewer choices to make.
- C) A few targeted few-shot examples of exactly these ambiguous cases, each showing the reasoning behind the chosen tool.
- D) Make `request_changes` the default response whenever the bot is uncertain which tool fits.

**Question 52.** You want every PR summary the bot posts to follow the same five-column markdown table. Instructions describing the table produce close-but-drifting variants (merged columns, extra sections). What reliably locks the format?

- A) A markdown linter that rejects malformed summaries and forces a regeneration attempt, retrying blind until one happens to pass the linter.
- B) Lowering the sampling temperature to cut down on formatting creativity.
- C) A stricter prose description of the table, with exact column widths specified.
- D) Complete, exact sample summaries in the required table format — this fixes structure the way lowering temperature alone cannot, since demonstration beats description for consistency.

**Question 53.** Which statement about `tool_choice` is correct?

- A) `"auto"` guarantees at least one tool call will appear in the response.
- B) With `"auto"` the model may respond with text and no tool call; `"any"` forces some tool call but leaves the choice of tool to the model; naming one specific tool forces exactly that tool.
- C) `"any"` lets the model call any number of tools at once, misreading a name that actually means "some tool, model's pick" as a count instead of a choice.
- D) A forced tool choice, once set, applies to every subsequent turn until explicitly reset.

**Question 54.** Developers dismiss many of the bot's test-generation suggestions, and you want to learn systematically which kinds of code constructs produce the unwanted suggestions. What enables that analysis?

- A) A `detected_pattern` field in the structured suggestion output naming the construct that triggered it, so dismissals aggregate by pattern.
- B) Exit interviews with the developers who dismiss the most suggestions overall.
- C) A dashboard tracking dismissal counts broken down by repository.
- D) A free-form "reason for dismissal" text box, reviewed manually once a month, producing anecdotes rather than anything that aggregates into a pattern the team could act on systematically.

**Question 55.** The review bot's finding — "this implementation may not match the approved design" — fails validation because it cites a design document the bot was never given. Will retry-with-error-feedback resolve it?

- A) Yes — the validation error will push the bot to reason more carefully about the design, as though careful reasoning could substitute for a document it never read.
- B) Yes, if the retry also raises `max_tokens` so the model can think through it more deeply.
- C) No — the design document was never provided; retries can't recover information the bot was never given.
- D) No — any finding referencing an external document should be auto-deleted from the report.

**Question 56.** Two jobs are proposed for the Message Batches API: (1) a nightly "explain every lint suppression in the repo" report read weekly; (2) the PR-blocking security gate developers wait on before merging. Evaluate.

- A) Both jobs fit — the roughly 50% cost savings applies equally regardless of latency needs.
- B) Neither fits — CI workloads should always use real-time APIs across the board.
- C) Job 2 fits better, since security scans are heavier and benefit more from a bulk discount, even though developers are waiting on the result the whole time.
- D) Job 1 fits (latency-tolerant); job 2 doesn't — a blocking gate can't depend on an up-to-24-hour window.

**Question 57.** Your overnight batch analyzes 300 open PRs. When results return, the poster must attach each analysis to the right PR. How is the mapping maintained?

- A) Results come back in submission order, so lining results up by index is enough, an assumption the batch API never actually documents or guarantees.
- B) Set each request's `custom_id` to the PR number at submission, then route results by reading that field back.
- C) Have the model embed the PR number directly inside its own output text.
- D) Submit 300 separate single-request batches so each result is unambiguous on its own.

**Question 58.** One pipeline job generates a bug fix and then, in the same session, reviews that fix before auto-merging. Post-incident analysis shows the reviews approve nearly everything, including a fix that broke production. What is the structural correction?

- A) Split generation and review into separate jobs; review runs as an independent instance seeing only the diff, not the generator's session.
- B) Add "assume the fix is wrong until proven otherwise" to the same review prompt, hoping a stronger instruction offsets a reviewer that still shares the generator's context and reasoning.
- C) Require two structured self-review passes in the same session before allowing the auto-merge.
- D) Auto-merge only fixes under 20 lines, routing anything larger to manual review.

**Question 59.** An 18-file PR gets inconsistent review depth — thorough on early files, thin on later ones — and the bot approved a cross-file API change in one file while flagging its mirror image in another. How should the review be restructured?

- A) Reverse the file order on a second pass and merge the findings from both passes, doubling the cost without fixing the underlying dilution across eighteen files.
- B) Cap pull requests at 6 files through repository policy going forward.
- C) Split review into per-file passes for local issues plus a dedicated cross-file pass for API consistency.
- D) Increase the review job's `max_tokens` so later files get a larger share of budget.

**Question 60.** You want findings the bot is demonstrably reliable about to post automatically, while shakier ones queue for human moderation. The bot emits a per-finding confidence score. What makes this routing sound?

- A) Trust findings at confidence ≥ 9/10; models rarely overstate certainty at the top of the scale, and a lower sampling temperature only reduces variety, not error.
- B) Route by category instead — security findings go to humans, everything else auto-posts.
- C) Auto-post everything but attach a "low confidence" label wherever the score is low.
- D) Measure accuracy against a labeled set of past findings at each confidence level, then set the threshold where precision meets the bar.

---
# Answer Key — Practice Exam 4

**Quick key:** 1-D, 2-B, 3-A, 4-C, 5-D, 6-A, 7-B, 8-C, 9-A, 10-D, 11-C, 12-B, 13-D, 14-A, 15-C, 16-B, 17-D, 18-A, 19-C, 20-B, 21-D, 22-A, 23-C, 24-B, 25-D, 26-C, 27-A, 28-B, 29-D, 30-A, 31-C, 32-B, 33-D, 34-A, 35-C, 36-B, 37-D, 38-A, 39-B, 40-C, 41-D, 42-A, 43-C, 44-B, 45-D, 46-A, 47-C, 48-B, 49-D, 50-A, 51-C, 52-D, 53-B, 54-A, 55-C, 56-D, 57-B, 58-A, 59-C, 60-D

---

**1. D** — Every executed `tool_use` block must be answered with a matching `tool_result` block, keyed to its ID, before the next request goes out; the 400 error is the API reporting that the loop skipped this step. A only changes whether a tool call is optional, B discards unrelated history, and C's schema-drift theory doesn't match a missing-block error.

**2. B** — A monthly-violated financial policy needs interception: a hook that blocks gift-card refunds at the tool-call level and redirects to the goodwill workflow. A adds more few-shot reinforcement to an approach already failing. C doubles inference cost for a still-probabilistic check that can be talked past the same way the first model was. D relocates prompt text into a description; neither enforces.

**3. A** — The gate must check what actually happened in the session, not what the conversation claims: block `update_email` until a verification step has completed. Social engineering defeats prompt rules (B, C) precisely because the model weighs persuasive context. D detects fraud after the account is already compromised.

**4. C** — No-runbook, unknown-cause investigations call for adaptive plans: hypothesize, look up, let findings drive the next step. A forces a mismatched case through a script built for a different pattern. B escalates work the agent can meaningfully progress. D burns calls without a hypothesis connecting them.

**5. D** — Overnight, tool results go stale while the negotiated resolution stays valid — exactly the split a structured case summary preserves: start fresh, inject the durable facts, re-look-up the time-sensitive ones. A trusts stale state. B carries the stale context along while distrusting it — the worst of both. C throws away the resolution details and burns customer goodwill.

**6. A** — Tone and empathy are behavioral guidance where occasional imperfection is tolerable — the appropriate domain of prompt instructions. B, C, and D are compliance rules with financial or security consequences, which is why they're hooked: any violation is unacceptable, so enforcement must be programmatic.

**7. B** — A malformed input is a validation error: name the field, state the expected format, and mark it correctable so the agent fixes the argument and re-calls in one step. A gives no correction path. C silently guesses intent inside the tool — hidden behavior that will misfire. D triggers retries of an input that will fail identically every time.

**8. C** — Tool descriptions should state boundaries — what the tool is for and what it is not for, naming the alternative. The agent chooses refunds because nothing signals exchanges are out of scope. A abuses naming to carry documentation. B teaches by failure at customer expense. D merges two flows with different semantics, creating a new selection problem inside one tool.

**9. A** — Selection reliability degrades as the tool count grows; the correction is scoped tool access — split by role so each agent carries only the handful of tools its job needs. B and D are cosmetic reorderings of an oversized surface. C adds latency to every call without reducing the decision complexity causing the errors.

**10. D** — For standard integrations, prefer existing community MCP servers; custom development is reserved for team-specific workflows. Zendesk CRUD is as standard as it gets. A is not-invented-here. B bypasses the tool interface the agent needs. C creates an undifferentiated mega-tool — a selection and description problem waiting to happen.

**11. C** — Returning failures as successes is the silent-suppression anti-pattern: the agent cannot respond truthfully or recover from an error it never sees. The fix is structured errors that surface. A trades one uninformative sentinel for another. B adds a verification round-trip to compensate for lying infrastructure. D helps engineers, not the customer being told falsehoods.

**12. B** — Frustration over a resolvable issue calls for acknowledgment plus immediate resolution — escalate only if the customer asks for a human. Sentiment is an unreliable proxy for complexity (A); this case is squarely within capability. C addresses mood while deferring the actual fix. D resolves the issue but ignores a customer who needs to be heard — hurting the interaction anyway.

**13. D** — Policy gaps are an escalation trigger: the published policy is silent on competitor matching, so the agent has no authority to improvise (A), refuse definitively (B), or invent criteria (C). Escalating routes the exception to someone empowered to set precedent.

**14. A** — Multiple customer matches require clarification through additional identifiers, not heuristic selection. B is a heuristic (a shared phone number across the accounts makes it a worse one). C mutates customer data on a guess. D proceeds on the guess and merely documents it.

**15. C** — Multi-issue sessions need structured issue data — order ID, amount, status, next action per issue — persisted in a separate context layer rather than left to drift in conversational history. A and D constrain customers to fit the architecture. B bloats every response and still relies on the model keeping the issues straight.

**16. B** — The decomposition is the failure point: the coordinator collapsed a broad topic into one industry's subtasks. Fix decomposition — enumerate the topic's domains first, then generate subtasks against that enumeration with coverage criteria. A patches queries downstream of bad assignments. C adds a guessing agent with no enumeration of its own. D fills gaps with uncited background knowledge.

**17. D** — In hub-and-spoke architecture, aggregation belongs to the coordinator: one place for completeness checks, ordering, and error handling before synthesis. A gives the consumer an orchestration job. B rebuilds coordinator responsibilities inside a message bus. C verifies delivery without anyone owning the whole picture.

**18. A** — `fork_session` creates independent branches from a shared analysis baseline — each framework develops in isolation without re-paying for the 400-document analysis and without cross-contamination. B resumes one lineage twice into the same history. C re-buys the corpus analysis. D lets each framework bias the other.

**19. C** — Match decomposition to predictability: the six-section weekly digest is a fixed prompt chain; novel ad-hoc investigations need dynamic decomposition that adapts to findings. A adds adaptive overhead to clockwork. B scripts the unscriptable. D assigns each pipeline the wrong pattern.

**20. B** — Independent gathering tasks parallelize by emitting all six Task calls in a single coordinator response. A changes what is fetched, not the serialization. C makes each sequential step cheaper but keeps six round-trips. D starts synthesis before its inputs exist.

**21. D** — Natural-language completion markers are the classic termination anti-pattern: they fire spuriously (the model discusses "DONE"), get paraphrased away, and duplicate what `stop_reason` already provides reliably. A, B, and C progressively decorate the wrong mechanism instead of replacing it.

**22. A** — Zero matches from a valid query is a *successful* search; conflating it with failure caused a pointless failover. Tools must distinguish valid empty results from access failures. B substitutes unvetted results for honest emptiness. C adds infrastructure to disambiguate what the response shape should state on its own. D keeps the ambiguity and hides the distinction in a log the agent never sees.

**23. C** — Descriptions should document input formats, limits, and edge-case behavior — a 256-character truncation is exactly the constraint an agent needs to compose valid queries. A and B are metadata that don't prevent the failure. D is a disclaimer, not a contract.

**24. B** — The agent prefers the tool it understands; "Searches arXiv" gives no case for selection. Enhance the description — what it searches, what it returns, when to prefer it over general web search. A removes a tool still needed for non-academic queries. C is keyword-matching brittleness. D — list ordering isn't a documented selection mechanism; descriptions are.

**25. D** — Subagents should recover locally from transient failures (retry the parse) and, failing that, continue the assignment — propagating only the unresolvable failure with partial results. Nine parsed documents is a report, not a total failure. A pretends timeouts can be configured away. B re-runs everything including the nine successes. C addresses throughput, not the give-up-entirely logic.

**26. C** — Conflicting values from credible sources are completed analysis, not noise: include both, annotated with source and methodology, and let the coordinator decide reconciliation before synthesis. A collapses the disagreement into a single invented figure. B stalls the pipeline where annotation suffices. D encodes an arbitrary tiebreak (recency) as truth.

**27. A** — Synthesis can only be as accurate as its inputs; requiring structured outputs with metadata — dates, source locations, methodological context — on every finding removes the inference that produces the misdating. B sends synthesis hunting for facts upstream already had. C flags the symptom. D asks a better model to guess better.

**28. B** — When the downstream consumer's budget is limited, change what upstream produces: structured key facts, citations, and relevance scores instead of excerpts plus reasoning narratives. A splits the material and loses cross-cutting synthesis. C scales cost to fit waste. D adds a lossy compression stage in the least-informed position.

**29. D** — Provenance must carry the source's own characterization: structured findings that keep "preliminary, n=12" attached to the claim, with synthesis required to preserve the qualifiers. A audits after the flattening has already reached the report. B and C exclude or demote evidence rather than representing it honestly.

**30. A** — The crash-recovery pattern: agents export structured state to a known location as they work; on resume the coordinator loads the manifest and injects prior state, resuming instead of restarting. B restarts from zero, just automatically. C doubles cost for a coin flip. D schedules around failure instead of recovering from it.

**31. C** — Resumption fits when prior context is mostly valid; the practice is informing the resumed session of the specific changes (the two auth modules, PR #412) for targeted re-analysis. A over-rotates on a small delta. B leaves stale beliefs live until the agent happens to re-read. D re-pays for the 95% that didn't change.

**32. B** — The canonical loop: continue while `stop_reason` is `"tool_use"` (execute, append results, send), exit on `"end_turn"`. A keys on text presence — meaningless. C makes an iteration cap the completion condition. D parses punctuation, which breaks on ordinary formatting.

**33. D** — Heterogeneous formats from multiple MCP servers are normalized deterministically in a `PostToolUse` hook — one canonical path form before the model reasons. A and C make the model do conversions probabilistically on every comparison. B sacrifices capability to dodge an integration with a standard solution.

**34. A** — Tool restrictions belong in the subagent's AgentDefinition: a doc-writer defined with Read, Grep, and Write cannot run builds. B is advisory. C has the coordinator babysitting instead of configuring. D punishes output latency after the fact.

**35. C** — Locating where a string originates is content search: Grep for the error message. A guesses the filename encodes the concept. B assumes the answer's location before searching. D searches history for what the working tree can answer directly.

**36. B** — With byte-identical repeated blocks, unique anchoring is unreliable even widened; the documented fallback is Read the file, then Write it back with the single intended change. A gambles that surroundings differ — in a generated file they often don't. C makes five changes to achieve one. D is disproportionate and assumes a regeneration path exists.

**37. D** — Personal preferences belong in user-level `~/.claude/CLAUDE.md`: applied for you, invisible to teammates, never in the repo. A ties preferences to file ownership, which changes. B ships them to everyone with a courtesy label that doesn't stop the nagging. C makes your own defaults opt-in for you.

**38. A** — `allowed-tools` is the structural control: a read-only toolset means no prompt defect can execute `git push` — the capability isn't there. B relies on developers reading plans carefully every time. C mitigates one command's damage after the fact. D shrinks the blast radius instead of removing it.

**39. B** — Project-scoped commands in `.claude/commands/` are version-controlled and available to anyone who clones — zero setup. A, C, and D describe distribution mechanisms Claude Code doesn't have (image installs, account sync, this built-in).

**40. C** — Conventions tied to a file type spread across many directories are the glob-rule case: `.claude/rules/` with `paths: ["**/*.sql"]` loads them exactly when matching files are edited. A covers one directory of many. B loads SQL rules in every session forever, SQL or not. D loads them only when invoked.

**41. D** — A well-understood, single-function change with a clear location is direct execution. Plan mode (A), exploration subagents (B), and session forking (C) each add process to a task with no design uncertainty to resolve.

**42. A** — Architectural scope (45+ files), multiple valid strategies, and rollback implications are plan mode's explicit criteria: explore, compare, commit to a design before edits. B begins mechanically before the strategy exists. C checkpoints a process that lacks a design. D delegates the decision along with the labor.

**43. C** — Undecided design dimensions plus suspected unknown-unknowns is the interview pattern's home case: Claude asks about traffic shape, burst tolerance, rejection semantics, and failure modes before implementation. A picks a "standard" without your requirements. B critiques a spec limited by the same blind spots. D discovers requirements in production.

**44. B** — When prose descriptions produce inconsistent interpretations, concrete input/output example pairs — including an edge case — pin down the transformation. A defines words instead of behavior. C formalizes ambiguity in stricter language without resolving it. D documents the library, not your expected output.

**45. D** — `@import` exists for exactly this: each package's CLAUDE.md references the single `standards/security.md`, one source of truth included where relevant. A works by filesystem trickery and breaks portability. B guarantees drift across six copies. C mentions the file without loading it.

**46. A** — `-p` / `--print` is non-interactive mode: process, print, exit — cron-safe. B, C, and D are invented flags; none exists in Claude Code.

**47. C** — The re-review pattern: prior findings go into context, and the bot reports only new issues plus a note on which prior ones remain unaddressed — no duplicates. A leaves post-push changes unreviewed. B destroys comment threads and discussion. D still requires the dedup logic C provides, while burying findings in an edit history instead of a notification.

**48. B** — Guaranteed field names and types come from `--output-format json` with `--json-schema`: schema-enforced structure for machine parsing. A and D parse unguaranteed output defensively or hopefully. C is an invented flag.

**49. D** — Effective criteria are specific and categorical: flag only when the comment's claimed behavior contradicts the code — the guide's own example. A is confidence-based filtering, which demonstrably fails to move precision. B caps volume without defining quality. C changes where noise lands, not whether it's noise.

**50. A** — False-positive-heavy categories destroy trust in the whole tool: developers who learn to skim past style noise skim past the accurate security findings too. That contagion is why the noisy category is urgent. B, C, and D invent indirect costs; the documented mechanism is trust erosion.

**51. C** — Ambiguous cases are the targeted-few-shot case: examples of exactly these situations, showing the chosen tool *and the reasoning* over plausible alternatives, teach judgment the model generalizes. A describes the mapping in prose — already too coarse for edge cases. B removes a legitimate output. D hardcodes one answer to varied situations.

**52. D** — Format consistency comes from demonstration: complete sample summaries in the exact required table. Description (C), even stricter, keeps producing drift; that's the observed failure. A regenerates until lucky. B reduces variance around a format the model hasn't internalized rather than fixing the format itself.

**53. B** — The correct trio: `"auto"` permits text-only responses; `"any"` mandates some tool call, model's choice; forced selection mandates one named tool. A describes "any." C invents count semantics for a name that describes choice, not quantity. D — forcing applies per-request, not until reset.

**54. A** — A structured `detected_pattern` field ties every suggestion to the construct that triggered it, so dismissals aggregate into pattern-level insight — the systematic feedback loop. B and D produce anecdote at low volume. C counts dismissals without capturing what caused them.

**55. C** — The design document was never in the input; no retry recovers information that isn't there. Provide the document, or scope the review to available material. A and B retry harder at reading an absent file. D deletes a category wholesale when the fix is supplying context.

**56. D** — Batch fits latency-tolerant, non-blocking work: the nightly report is ideal; a merge-blocking gate cannot ride a no-SLA, up-to-24-hour service. A ignores the blocking constraint. B overcorrects — the report genuinely fits. C prices workloads instead of matching latency requirements.

**57. B** — `custom_id` is the Batch API's request/response correlation mechanism: set it to the PR number at submission, read it on each result. A relies on ordering the API doesn't promise. C trusts model output for plumbing. D abandons batching's economics to avoid using the feature built for this.

**58. A** — Generation and review must be separated: an independent review instance receives the diff without the generator's session context, avoiding the self-approval bias that shipped the bad fix. B and C prompt or repeat a structurally biased review. D limits exposure without fixing the reviewer.

**59. C** — Declining depth across files plus contradictory verdicts on mirrored code are attention dilution; the restructure is per-file passes for local issues and a separate integration pass for cross-file consistency. A averages two diluted passes. B constrains developers to fit the tool. D — token budget doesn't reallocate attention across a long input.

**60. D** — Confidence becomes routable only after calibration: measure accuracy at each score level against labeled outcomes and place the threshold where precision meets the bar. A trusts raw self-report at the extreme — where miscalibration concentrates. B discards per-finding signal for category stereotype. C posts everything anyway, labeling the risk instead of routing it.

---

*End of Practice Exam 4.*
