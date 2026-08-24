# CCAFC Practice Exam 5

**Claude Certified Architect – Foundations — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Code Generation with Claude Code, Multi-Agent Research, Developer Productivity, Structured Data Extraction) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (matches the official weightings): D1 Agentic Architecture ×16, D2 Tool Design & MCP ×11, D3 Claude Code Configuration ×12, D4 Prompt Engineering & Structured Output ×12, D5 Context Management & Reliability ×9.

Answer key with explanations is at the end.

---

## Scenario A: Code Generation with Claude Code (Questions 1–15)

You are using Claude Code to accelerate software development. Your team uses it for code generation, refactoring, debugging, and documentation, with custom slash commands, CLAUDE.md configurations, and both plan mode and direct execution.

---

**Question 1.** Claude follows your API conventions perfectly on your laptop but ignores them on your desktop, in the same repository. What is the right first diagnostic?

- A) Compare Claude Code versions on the two machines, since an older release missing a config feature would explain the gap, and upgrade whichever one is behind.
- B) Run `/memory` on both machines to see which memory files each session loaded.
- C) Re-clone the repository on the desktop in case the working copy has stray local edits.
- D) Run `/compact` on the desktop session to clear context that might be crowding out the conventions.

**Question 2.** Your monorepo's `frontend/` packages need the React standards file and the accessibility standards file; `backend/` packages need the API standards and database standards files. All four files live in `standards/`. How do you wire this up without duplication?

- A) Concatenate all four standards files into the root CLAUDE.md so every package loads one combined document regardless of stack.
- B) Copy the React, accessibility, API, and database files into every package directory that touches them, so each team keeps an editable local copy in sync by convention.
- C) Reference all four standards files from every package's CLAUDE.md and let Claude judge which ones apply to the code it's currently touching.
- D) In each package's CLAUDE.md, use `@import` to pull in only the standards files relevant to that package.

**Question 3.** Your CLAUDE.md mixes testing standards, Git workflow, security rules, code style, and deployment steps in one 1,000-line file that three teams edit and constantly conflict over. What is the recommended reorganization?

- A) Split it into focused topic files under `.claude/rules/`, each owned by the team that owns that topic.
- B) Freeze the file and require RFC approval for every future change, so conflicts get resolved through process instead of merges.
- C) Move it to a wiki and link from CLAUDE.md, keeping the canonical text outside version control.
- D) Auto-generate it nightly from each team's own documentation source, replacing manual edits with a build step.

**Question 4.** Your database-seeding workflow — 300 lines of steps, fixtures, and cleanup logic — is used about once a week. Universal code conventions are used in every session. Where does each belong?

- A) Both belong in CLAUDE.md, since both are things the team has agreed matter and Claude should always be aware they exist.
- B) Both belong in skills under `.claude/skills/`, so neither one adds to the context every session pays for by default.
- C) Conventions in CLAUDE.md, since they apply every session; the seeding workflow as a skill, loaded on demand only when it's invoked.
- D) Conventions belong in a skill invoked at the start of each session; the seeding workflow belongs in CLAUDE.md since it's the more complex of the two.

**Question 5.** Your `/explore-alternatives` skill generates several competing design sketches. After it runs, the main session's context carries all the rejected sketches, and Claude later resurrects abandoned ideas as if they were current. What frontmatter fixes this?

- A) `argument-hint`, so the skill is scoped to exactly one design question per invocation, rather than drifting across several different questions at once.
- B) `allowed-tools`, restricting the skill so it can't write the sketches out to files where they'd persist.
- C) `paths`, restricting the skill so it only triggers when a design document is already open.
- D) `context: fork` — the exploration runs isolated from the main conversation.

**Question 6.** Your `/update-changelog` skill needs only to read the git log and edit `CHANGELOG.md`. An incident review found a run where it also executed `git tag` and pushed the tag. What is the structural fix?

- A) Add a line to the skill's SKILL.md instructing it to never create or push tags under any circumstances, no matter the situation.
- B) Set `allowed-tools` to the minimal set — reads plus editing.
- C) Require a developer to review the structured diff of every changelog-skill run before it's complete.
- D) Protect the tag namespace server-side so pushes from the automation account are rejected.

**Question 7.** Your `/fix-issue` skill needs a ticket number to look up the issue before fixing it. Developers regularly invoke it bare and it fabricates an interpretation of "the issue." Which frontmatter option addresses the invocation problem?

- A) `argument-hint`, so invoking the skill bare prompts for the ticket number.
- B) `context: fork`, so at least the fabricated interpretation stays isolated in a sub-agent.
- C) A SKILL.md instruction telling the model to refuse politely when no ticket number was supplied.
- D) `allowed-tools` restricted to read-only tools until a valid ticket number appears somewhere earlier in the conversation.

**Question 8.** End-to-end test specs (`*.e2e.ts`) live next to the features they test, in dozens of directories. They must all follow your Playwright conventions. Which mechanism applies the conventions to exactly those files?

- A) A CLAUDE.md placed in the `tests/` directory, where some but not all specs happen to live.
- B) The root CLAUDE.md, with a section headed "For e2e files only" placed prominently near the top of the document.
- C) A `.claude/rules/` file with frontmatter `paths: ["**/*.e2e.ts"]`.
- D) A skill that developers are expected to run manually before writing any new e2e test.

**Question 9.** You're adding a caching layer. Three integration approaches are viable — sidecar, library, or gateway-level — each with different infrastructure requirements, and the choice constrains several services. How do you start?

- A) Enter plan mode: explore the affected services, weigh the three approaches, and commit to a design before writing code.
- B) Direct execution, starting with whichever approach looks simplest and switching to another if that one runs into trouble mid-implementation.
- C) Implement all three approaches behind a feature flag, deploy each to a slice of traffic, and benchmark them against each other in production.
- D) Ask Claude to pick whichever of the three approaches it thinks is best and implement that one immediately.

**Question 10.** A user reports that phone numbers with spaces fail validation. The regex lives in one function; the failing input and expected behavior are both known. How do you proceed?

- A) Enter plan mode first, so the fix accounts for validation architecture across the whole codebase rather than just this one function.
- B) Spawn an Explore subagent to find every validation pattern in the codebase before touching the regex.
- C) Use `fork_session` to try two candidate regexes in parallel and compare which one passes more of the existing test cases.
- D) Direct execution — a single-function fix with a clear reproduction and known expected behavior needs no planning phase.

**Question 11.** Claude's fixes to your date-parsing utility keep regressing other formats: each fix breaks a previously working case. What iteration structure stops the whack-a-mole?

- A) Ask Claude to enumerate every supported format out loud before attempting each fix.
- B) Freeze the existing utility in place and have Claude write a second, parallel utility instead.
- C) Write a test suite covering all formats first, then iterate against failing tests.
- D) Fix the formats in order of how frequently each one appears in production traffic logs from last quarter.

**Question 12.** You're deep in a productive session; context is nearly full of file dumps from earlier exploration, and you have an hour of implementation left. You want to preserve key decisions but reclaim space. What do you do?

- A) Start a brand-new session and reconstruct the important decisions from memory before continuing the implementation.
- B) Run `/compact` — it summarizes the conversation, reducing context usage while preserving key information, letting the session continue.
- C) Ask Claude to respond as tersely as possible for the remainder of the session to slow the context from filling further.
- D) Export the transcript to a text file and finish the remaining work by hand in an editor, referring back to it as needed.

**Question 13.** Your main session must design a refactor, but first you need answers to three verbose research questions (where is X implemented, who calls Y, how is Z configured). How do you keep the main session's context clean?

- A) Spawn subagents to investigate each question and return summaries, keeping the exploration out of the main context.
- B) Answer all three questions directly in the main session, then run `/compact` right before designing.
- C) Start designing the refactor from reasonable assumptions and verify them against the codebase afterward.
- D) Open three terminal tabs, investigate one question in each, and manually copy the conclusions over.

**Question 14.** Your lint MCP tool returns the full AST dump (2,000+ lines) with every lint report; the agent only ever uses the rule violations list. Sessions using the linter heavily degrade fast. What is the fix?

- A) Lint entire directories in a single call instead of file-by-file, so the tool is invoked less often.
- B) Add a hook that truncates each dump to its first 200 lines rather than to the fields actually used.
- C) Move linting into a subagent so the dumps accumulate there instead of the main context.
- D) Trim the tool's output to the violations list before it enters context, since the rest is never used.

**Question 15.** Hour three of a security audit session: Claude begins asserting things about modules that contradict what it itself reported in hour one. The audit has hours to go. What practice should have been in place from the start (and is worth starting now)?

- A) Cap security-audit sessions at one hour each, splitting the work across multiple shorter sessions instead.
- B) Run a second Claude instance auditing the same modules independently in parallel, then reconcile the two sets of findings by hand afterward.
- C) Keep an audit scratchpad file recording findings as they're confirmed, for reference when answering later questions.
- D) Re-read every relevant module from scratch immediately before answering each new question in the audit.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Analytics show that 30% of user queries are simple definitions or single facts, yet every query traverses search → analysis → synthesis → report. What should the coordinator do differently?

- A) Assess each query's complexity first, answering simple facts directly and reserving the pipeline for real research.
- B) Add a cache in front of the whole pipeline so repeated questions skip straight to a stored answer.
- C) Shorten each stage's prompt so running the full pipeline is cheaper per query, even for simple ones.
- D) Reject simple-looking queries outright with a message directing the user to a search engine instead.

**Question 17.** Reviewing the coordinator wrapper, you find: `for turn in range(8): response = send(...)` with no other exit condition, and users report reports that stop mid-topic. What is the correct redesign?

- A) Raise the range to 20, since telemetry shows most tasks finish comfortably within that many turns.
- B) Add a check after each response that breaks the loop early whenever the text "looks complete."
- C) Loop on `stop_reason` — continue on `"tool_use"`, exit on `"end_turn"` — with any turn cap as a backstop only.
- D) Let each user configure their own turn budget for the query, based on how thorough they expect it to be.

**Question 18.** The report agent produces beautiful reports with invented citations. Investigating, you find its prompt contains the synthesis text but not the claim-source mappings the synthesis agent produced. What is the fix?

- A) Instruct the report agent in its prompt to only cite a source when it is certain the citation is correct.
- B) Pass the claim-source mappings explicitly in the report agent's prompt, alongside the synthesis text.
- C) Give the report agent its own search tool so it can go find real citations to attach to each claim.
- D) Add a post-processing step that verifies each citation afterward and corrects the ones that don't check out.

**Question 19.** Five regional market analyses are needed before a global rollup; each is independent. The coordinator currently runs them one per turn, and latency is five times the single-region time. What fixes the latency?

- A) Merge the five regional analyses into a single subagent prompt covering all regions at once.
- B) Precompute all five regions on a nightly schedule so live requests hit a cache instead of running fresh.
- C) Normalize each regional analysis into a shorter summary so each one individually finishes faster.
- D) Emit five Task tool calls in a single coordinator response, so the subagents run concurrently.

**Question 20.** An engineer wired the search agent to hand results directly to the analysis agent and the analysis agent directly to synthesis, bypassing the coordinator "for speed." Since then, failures are impossible to localize and partial results vanish silently. What does the incident illustrate?

- A) Subagent chains generally need a dedicated distributed-tracing system bolted on to stay debuggable.
- B) Direct handoffs between subagents are fine architecturally as long as each one in the chain also gets its own dedicated retry logic.
- C) Hub-and-spoke routing through the coordinator is what gave observability, error handling, and controlled information flow.
- D) The speed gain from removing the coordinator proves its routing role was unnecessary overhead all along.

**Question 21.** Competitor-analysis reports keep shipping without pricing data — the synthesis agent works with whatever arrives, and nothing checks completeness. What is the architectural fix?

- A) The coordinator evaluates synthesis against required coverage, re-delegates for the gaps, and re-invokes synthesis.
- B) Add an instruction to the synthesis prompt telling it to always include a pricing section.
- C) Add a required `pricing` field to the report template, left blank whenever the data never arrived.
- D) Ask the search agent to fetch more results per query, on the theory pricing will surface more often at volume.

**Question 22.** Policy: the document analysis agent may only load documents from your licensed research library. It has a `load_document` tool that accepts any URL, and prompt instructions restricting it. You need a guarantee. What is it?

- A) Run a nightly job that audits which URLs were loaded the previous day, flagging anything found outside the licensed library.
- B) Intercept `load_document` calls with a hook that blocks URLs outside the licensed library's domains.
- C) Strengthen the prompt instructions by listing the approved domains explicitly near the tool's description.
- D) Rename the tool `load_licensed_document`, so its name itself reminds the model of the restriction.

**Question 23.** Your coordinator prompt dictates exact search strings for each subagent to run. Topics that don't match the anticipated phrasing return poor results, and subagents never adapt. What is the corrected delegation style?

- A) Write longer lists of predefined search strings that try to anticipate more possible phrasings in advance.
- B) Add a dedicated search-string-generation subagent whose only job is to feed queries to the search agent.
- C) Instruct subagents to ignore the coordinator's search strings whenever the results they get back look thin.
- D) Delegate research goals and quality criteria, leaving search formulation to the specialist so it can adapt.

**Question 24.** `process_source` takes `mode: "summarize" | "extract" | "verify"` and agents keep calling it with the wrong mode for the situation. What is the recommended redesign?

- A) Write clearer documentation of the three modes and their schema differences in the tool's description field.
- B) Give the tool a default mode so a call with the wrong or missing mode still does something reasonable.
- C) Split it into three purpose-specific tools, each with its own clear description and contract.
- D) Wrap the tool so it infers the intended mode automatically from the shape of the other arguments.

**Question 25.** Your toolset includes `search_news` ("Searches for news") and `search_web` ("Searches the web") — and agents use them interchangeably, though one hits a curated news API with date filtering and the other a general engine. What is the first fix?

- A) Rewrite both descriptions to state what each source is, what parameters matter, and when to prefer each.
- B) Drop `search_web` from the toolset entirely, since news queries appear to be the primary use case.
- C) Route calls by keyword: anything containing the word "news" goes to `search_news`, everything else to `search_web`.
- D) Merge the two tools into a single `search_all` tool that takes a source parameter the agent must choose.

**Question 26.** A rate-limited search tool returns a normal successful response whose content is the string "quota exceeded, try later." Agents keep summarizing this string into research notes. What is the correct tool behavior?

- A) Change the wording of the string so a naive structured-output parser won't quote it directly.
- B) Return an empty result set instead of the message whenever the quota has been hit.
- C) Have the agent's prompt list known error strings for it to recognize and ignore.
- D) Signal the failure through the MCP `isError` flag with structured content — category, retryability.

**Question 27.** Analysts curate 40 high-quality datasets your agents should prefer. Currently agents discover them by trial-and-error searching, often missing them entirely. How do you give agents standing visibility of the curated collection?

- A) List all 40 datasets directly in every subagent's prompt so none of them are ever missed.
- B) Expose the curated collection as MCP resources — a catalog agents can see directly.
- C) Adjust the search tool's ranking logic so the curated datasets are boosted above general results.
- D) Add a `list_curated` tool and instruct every subagent to always call it first, before any other kind of search.

**Question 28.** The analysis agent's generic `fetch_page` tool keeps pulling low-quality content mills into evidence. You maintain an allowlist of credible sources. What is the strongest fix?

- A) Add the allowlist to the agent's prompt instructions so it knows which domains are considered credible.
- B) Post-filter the evidence against the allowlist during synthesis, validating it only after analysis has already read it.
- C) Replace `fetch_page` with a constrained `load_source` tool that validates every request against the allowlist.
- D) Adjust the search ranking so content-mill domains score lower and appear further down the results.

**Question 29.** A report describes "conflicting GDP growth figures" — 2.1% versus 3.4% — but the sources measured different years. The subagent outputs contained the numbers without dates. What is the systemic fix?

- A) Require publication and collection dates in structured outputs, so figures can be read temporally.
- B) Have the synthesis agent discard any figure whenever it can't infer the date the figure applies to.
- C) Prefer whichever figure is higher, on the theory that growth data tends to get revised upward.
- D) Flag every numeric disagreement between sources to a human reviewer before the report can publish.

**Question 30.** During research on a paywalled industry, several key sources were inaccessible. The coordinator knows which topic areas are affected. What should the final deliverable contain?

- A) Only the well-covered areas, quietly omitting the gaps so the report reads more cleanly to the client.
- B) Coverage annotations distinguishing well-supported findings from areas thin due to inaccessible sources.
- C) A general boilerplate disclaimer that no research is ever fully exhaustive, placed at the end of the report.
- D) Model-generated estimates filling the gap areas, each one clearly marked as an estimate rather than sourced.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** Your agent calls Grep, your harness executes it and appends the `tool_result` — and then nothing happens; the agent never produces its answer. The harness logs show no further API call was made. What is missing?

- A) A `tool_choice` setting needs to be added to the follow-up request before the model will respond again.
- B) The Grep result was almost certainly too large and needs to be truncated before it can be sent back.
- C) Add a `PostToolUse` hook that re-sends the tool result automatically so the model keeps going.
- D) The continuation request — after appending tool results, the harness must send the conversation back.

**Question 32.** An engineer spent Friday building context in a named session about the notification service. Monday, with no code changes over the weekend, she wants to continue. What is the right move, and why?

- A) `--resume` the named session, since prior context from Friday is still valid and nothing changed.
- B) Start a fresh session, since sessions generally shouldn't be expected to span multiple calendar days.
- C) Use `fork_session` on Friday's session so the original stays untouched while Monday's work branches off.
- D) Start fresh but paste in the final message from Friday to carry over the essential context.

**Question 33.** From one shared analysis of your build system, you want to develop two upgrade strategies — incremental adoption versus a clean cutover — without either exploration influencing the other. Which mechanism?

- A) Continue in the one existing session, exploring both strategies in alternating messages so nothing gets lost.
- B) Start two fresh sessions, each re-running the build-system analysis from scratch before exploring its strategy.
- C) `fork_session` — two independent branches from the shared analysis baseline, one strategy explored in each.
- D) `--resume` the analysis session twice concurrently, one resumed copy per strategy.

**Question 34.** "Make our CI builds faster" — an open-ended task with unknown bottlenecks. How should the agent decompose it?

- A) Apply a standard top-ten list of generic build-speed tricks, in order, until the build feels fast enough.
- B) First measure where time goes, identify the highest-impact bottlenecks, then form a plan that adapts.
- C) Parallelize every stage of the pipeline first, on the theory parallelism usually dominates other gains.
- D) Ask the team which step of the pipeline feels slowest to them and optimize that step first.

**Question 35.** Generating a README for each of 40 services follows identical stages: read the service manifest → summarize endpoints → document env vars → assemble the file. What decomposition pattern fits?

- A) Dynamic decomposition per service, letting the agent restructure the stages differently each time.
- B) A single prompt asking the agent to produce all 40 READMEs at once in one long response.
- C) A short interview with each service's owner before generation begins, to confirm the scope.
- D) A fixed prompt chain — the same stages, same order, for every service — since the workflow repeats.

**Question 36.** Your agent runs tests across many repos; some produce JUnit XML, others plaintext summaries, others JSON. The agent frequently misreads pass/fail status in formats it saw less often. What is the reliable fix?

- A) A `PostToolUse` hook normalizing test outputs into one canonical result structure before the model sees them.
- B) A prompt appendix describing each repo's output format in enough detail for the model to parse it.
- C) Standardize every repo on a single test reporter first, retiring the JUnit and plaintext formats.
- D) Have the agent re-run any test whose outcome looks ambiguous, to get a confirming second reading.

**Question 37.** The productivity agent automates release chores but must never run `npm publish` — releases go through CI only. It's in CLAUDE.md; an intern's session still published a package last week. What now?

- A) Revoke npm publish credentials from every developer machine so no local session can publish at all.
- B) Add the same rule to the agent's prompt in addition to CLAUDE.md, stating it in two places.
- C) Intercept Bash calls with a hook that blocks `npm publish`, pointing the agent to the CI flow instead.
- D) Add a hook that pauses for confirmation before every npm command at all, regardless of which one it is.

**Question 38.** Your coordinator delegates test-writing to whichever subagent seems right, but its choices look random. The subagent definitions read: "Agent A — helps with code," "Agent B — helps with quality." What is the fix?

- A) Add a handful of few-shot delegation examples to the coordinator's prompt, showing past assignments.
- B) Rewrite the AgentDefinition descriptions to state each subagent's specialization, tools, and selection criteria.
- C) Swap the coordinator to a larger model, on the theory it will infer the right subagent regardless.
- D) Hardcode a fixed task-type-to-agent routing table that bypasses the coordinator's own judgment.

**Question 39.** You need every `TODO` and `FIXME` comment across the codebase, with file locations. Which tool does this directly?

- A) Grep — pattern search across file contents, with locations returned per match.
- B) Glob with the pattern `**/TODO*`, since it will find every file whose name matches.
- C) Read every file individually and scan each one's contents by eye for the two comment markers.
- D) An MCP code-index server, since the built-in tools aren't able to search inside comments.

**Question 40.** The agent must inventory every Dockerfile in the monorepo — `Dockerfile`, `Dockerfile.dev`, `api.Dockerfile` — wherever they live. Which tool call?

- A) Grep for the string `FROM ` across all files in the repository and collect the filenames that match.
- B) Read every `docker-compose` file and follow whatever build-context references they contain.
- C) Run Bash `docker images` to enumerate whatever images have already been built locally.
- D) Glob with patterns matching the naming variants (`**/Dockerfile*`, `**/*.Dockerfile`) directly.

**Question 41.** Asked how payment processing works in an unfamiliar codebase, which exploration sequence reflects the recommended practice?

- A) Read every file in `src/payments/` end to end before attempting to answer the question at all.
- B) Grep for entry points, Read the files that match, and follow the imports to trace the flow.
- C) Answer directly from the architecture diagram already in the wiki, without checking it against the code.
- D) Glob for `*payment*` and read only the files whose names match that pattern exactly.

**Question 42.** `formatCurrency` is defined in `src/utils/money.ts` but consumed via two barrel files and one aliased re-export (`export { formatCurrency as fmtMoney }`). You need every real call site. What is the correct strategy?

- A) Grep for `utils/money` across the codebase and read whichever files come back as importers.
- B) Rely on the editor's rename-refactor tooling to enumerate every reference automatically.
- C) First enumerate all the exported names, including `fmtMoney`, then Grep for each one.
- D) Grep for `formatCurrency` only, since aliased re-exports like this one are rare enough in this codebase to ignore.

**Question 43.** The team's internal-API MCP server needs a per-developer token. You want zero-setup onboarding via the repo without leaking credentials. Which configuration?

- A) Commit the token directly inside `.mcp.json`, relying on the repository being private as the safeguard.
- B) Have each developer maintain their own `~/.claude.json` entry, following a recipe on the wiki.
- C) Ship a bootstrap script developers run once to write a local, untracked `.mcp.json` on first use.
- D) Commit `.mcp.json` with the token as `${INTERNAL_API_TOKEN}`, resolved from each developer's own environment.

**Question 44.** Your `schema-inspector` MCP tool answers database-structure questions precisely, but the agent keeps Grep-ing through migration files instead, producing stale answers. The tool's description: "Inspects schemas." What is the recommended fix?

- A) Expand the description to state it returns live schema structures directly.
- B) Delete the migrations directory from the paths the agent is allowed to browse or search at all.
- C) Add a prompt rule saying never to Grep inside the `migrations/` directory.
- D) Rename the tool to something more emphatic, like `USE_THIS_FOR_SCHEMAS`.

**Question 45.** Before designing a plugin API, the agent should compare three candidate integration points, each requiring reading several large modules. The comparison itself is the input to your main design session. How do you structure this?

- A) Read all the relevant modules directly inside the design session and accept the context cost.
- B) Use the Explore subagent for the comparison, so verbose reading stays isolated from the design session.
- C) Do the design work first, from assumptions, and check those assumptions against the modules afterward.
- D) Split the design conversation across three separate sessions, one per candidate integration point.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your invoice extractor prompts for "a JSON response" and parses the text. Failures cluster around markdown fences and apologetic preambles ("Here is the extracted data:"). What eliminates the failure class?

- A) A response-prefill trick — starting the assistant turn with a literal `{` to nudge it toward JSON.
- B) A firmer prompt rule stating plainly: "no prose, no fences, JSON only," repeated near the end.
- C) Tool use — define an extraction tool whose input schema is the invoice structure, and read the `tool_use` block.
- D) A hook that strips markdown fences and leading prose from the raw response before parsing it.

**Question 47.** Receipts often genuinely lack a due date, but `due_date` is required in your schema — and audits found the model quietly inserting a date 30 days after the purchase date. What is the correct fix?

- A) Make `due_date` optional and nullable, instructing the model to return null when the document has none.
- B) Keep the field required but add a prompt instruction telling the model never to invent dates.
- C) Post-validate that the date already in the structured output appears verbatim in the source text.
- D) Default the field to purchase date plus 30 days server-side, turning the guess into official policy.

**Question 48.** Your `payment_method` enum covers `["card", "cash", "bank_transfer"]`. Documents now mention regional wallets, crypto, and buy-now-pay-later services — all being forced into `"card"`. How should the schema evolve?

- A) Add the ten most commonly seen new payment methods to the enum on a recurring quarterly cycle.
- B) Make the field a free-text string and hand classification off to a downstream process instead.
- C) Reject any document whose payment method falls outside what the current schema's enum recognizes.
- D) Add `"other"` to the enum with a companion detail field capturing the actual method described.

**Question 49.** A shared intake pipeline receives invoices, contracts, and HR forms mixed together, each with its own extraction tool defined. You need guaranteed structured output on every document without pre-classifying. Which setting?

- A) `tool_choice` forced permanently to the invoice tool's schema, since invoices are the most common type.
- B) `tool_choice: "any"` — the model must call one of the tools and picks the schema that fits the document.
- C) `tool_choice: "auto"` combined with a prompt instruction reminding the model to always extract.
- D) Three separate pipeline lanes, each fed by a rules-based classifier deciding which lane a document enters.

**Question 50.** Contracts occasionally arrive with a stated term whose end date precedes its start date (drafting or OCR errors). Downstream date math silently produces negative durations. What extraction design surfaces the problem?

- A) Swap the two dates automatically whenever the end date precedes the start date, since that seems intentional.
- B) Reject any contract outright whose two dates come back out of order.
- C) Extract both dates as stated and set a `conflict_detected` boolean whenever the ordering is impossible.
- D) Extract only the start date and derive the end date from the term length stated elsewhere.

**Question 51.** `signatory_date` keeps failing extraction on a batch of scanned agreements. Sampling shows the signature page simply wasn't scanned — the date isn't in the input. The retry system has been resubmitting these documents for days. What is the correct assessment?

- A) Add more retries with varied prompt phrasing, in case a different phrasing surfaces the date after all.
- B) The retries would likely succeed if the context window used for extraction were made larger.
- C) The field should simply be removed from the schema, since it's clearly unreliable to extract.
- D) Detect that no retry can succeed here, stop retrying, and route to the rescanning workflow instead.

**Question 52.** You added few-shot examples covering three vendors' invoice layouts. Extraction then also improved markedly on a fourth vendor whose layout none of the examples showed. What explains this?

- A) Few-shot examples teach transferable judgment about locating and mapping fields, which generalizes.
- B) The fourth vendor's invoice layout must simply coincide closely with one of the three example layouts.
- C) Adding the few-shot examples simply increased the prompt's length, and a longer prompt reliably improves accuracy.
- D) A model update happened to ship around the same time, and the new examples were actually incidental.

**Question 53.** Financial filings present the same facts sometimes in tables, sometimes in narrative paragraphs, sometimes in footnotes. Your extractor handles tables well and misses the rest. What is the recommended fix?

- A) Preprocess every filing to mechanically convert its narrative sections into normalized tables before extraction ever runs.
- B) Add few-shot examples demonstrating extraction from each presentation style directly.
- C) Run three extractors, each given its own few-shot examples for one presentation style, and merge the outputs.
- D) Restrict extraction to the tabular sections and route narrative and footnote sections to reviewers.

**Question 54.** Two workloads: (1) re-extracting your ten-year document archive with an improved schema, results needed "sometime this quarter"; (2) extracting data from documents customers upload during a live onboarding flow. Assign the APIs.

- A) Use the synchronous API for both workloads, since it keeps the operational story simpler for the team.
- B) Use the batch API for both workloads, since the pricing discount is too large to leave on the table.
- C) Use the batch API for the onboarding flow since its overall volume is higher than the archive's, and the synchronous API for the archive.
- D) Batch API for the archive since it's latency-tolerant; synchronous API for onboarding, where a customer waits.

**Question 55.** Your contract guarantees extraction results within 36 hours of document receipt. Batch processing takes up to 24 hours. Documents arrive continuously. Which accumulation window keeps the guarantee?

- A) Accumulate for 24 hours before batching, since one daily batch is the operationally cleanest schedule to run.
- B) Accumulate for 16 hours, since batches in practice tend to complete in well under the full 24-hour ceiling.
- C) Accumulate for 8 hours — worst case 8 + 24 = 32 hours, staying within the 36-hour guarantee with margin to spare.
- D) Accumulate for 48 hours and add a separate expedite lane for documents that are already getting old.

**Question 56.** Legal has approved extracting 10,000 archived medical consent forms with a new prompt. The batch budget is fixed. What do you do before submitting the full batch?

- A) Refine and verify the prompt on a representative sample via the synchronous API before the full run.
- B) Submit the full 10,000-form batch immediately, since failures can simply be resubmitted within budget.
- C) Submit the full batch but at a lower sampling randomness setting, on the theory it's more consistent.
- D) Split the run into two 5,000-form batches and correct the prompt in between the two.

**Question 57.** Your extraction step ends with "double-check your extraction against the document" — and reports itself accurate. Auditors keep finding wrong values the self-check approved. What does the guide say about this design?

- A) The self-check step needs a detailed rubric listing the common error types to look for, rather than a vague, open-ended instruction.
- B) Verification should run as an independent instance, comparing output to source directly.
- C) The self-check should simply be run twice in a row, escalating to a human whenever the two disagree.
- D) Self-checks become reliable once the model also reports a numeric confidence score alongside them.

**Question 58.** Your dashboard proudly shows 96% extraction accuracy. A operations manager mentions that handwritten intake forms "seem to always be wrong." You segment the data: typed forms 99%, handwritten 61%. What is the lesson?

- A) Handwritten forms should simply be excluded from the accuracy metric, since they clearly skew it.
- B) The dashboard should report median accuracy instead of the mean, which is more sensitive to outliers.
- C) 96% was still a perfectly accurate overall number, so no change to the review process is needed.
- D) Validate accuracy by document type before it justifies a decision, and remediate the failing segment.

**Question 59.** After automating high-confidence extractions, you need an ongoing mechanism to catch error patterns the confidence model doesn't know about yet. What is it?

- A) Schedule a quarterly re-validation of the system against the original benchmark set used to build it.
- B) A hook that alerts automatically whenever the confidence-score distribution drifts in a detectable way.
- C) Stratified random sampling of high-confidence extractions for continuous human review.
- D) Add a user-facing "report an error" button to every downstream system that consumes the extracted data.

**Question 60.** The model emits per-field confidence scores, and you plan to auto-accept above a threshold. A colleague proposes 0.9 "because it's high." What is the defensible way to choose?

- A) Calibrate against a labeled validation set, setting thresholds where measured accuracy meets the requirement.
- B) Adopt the proposed 0.9 threshold for now, but schedule a review of the first month's auto-accepts.
- C) Use 0.99 instead of 0.9, on the reasoning that a stricter cutoff is always the safer choice.
- D) Average the confidence scores from the last quarter's extractions and use that as the new threshold.

---
# Answer Key — Practice Exam 5

**Quick key:** 1-B, 2-D, 3-A, 4-C, 5-D, 6-B, 7-A, 8-C, 9-A, 10-D, 11-C, 12-B, 13-A, 14-D, 15-C, 16-A, 17-C, 18-B, 19-D, 20-C, 21-A, 22-B, 23-D, 24-C, 25-A, 26-D, 27-B, 28-C, 29-A, 30-B, 31-D, 32-A, 33-C, 34-B, 35-D, 36-A, 37-C, 38-B, 39-A, 40-D, 41-B, 42-C, 43-D, 44-A, 45-B, 46-C, 47-A, 48-D, 49-B, 50-C, 51-D, 52-A, 53-B, 54-D, 55-C, 56-A, 57-B, 58-D, 59-C, 60-A

---

**1. B** — Same repo, different behavior across machines points at configuration loading, and `/memory` shows exactly which memory files each session loaded — diagnose before changing anything. The likely culprit is user-level configuration present on one machine only. A guesses at a plausible cause without checking; C and D change things before establishing what actually differs.

**2. D** — `@import` lets each package's CLAUDE.md include only the standards files relevant to it — one copy of each standard, selectively composed. A loads everything everywhere regardless of stack. B duplicates the files and lets copies drift out of sync. C loads all four into every package and hopes the model scopes them correctly on its own.

**3. A** — The recommended structure for a contested monolith: topic-specific files under `.claude/rules/`, each owned by the team that owns the topic — smaller diffs, fewer conflicts, clearer ownership. B freezes the conflict in place behind process. C removes the content from Claude's direct view. D replaces one monolith-maintenance problem with another, generated one.

**4. C** — The dividing line: universal, always-applicable content in CLAUDE.md; occasional task-specific workflows as skills loaded on invocation. A pays the 300-line seeding cost in every session regardless of need. B makes universal conventions opt-in, so a session can miss them entirely. D has the split exactly backwards.

**5. D** — Exploratory content that shouldn't persist is what `context: fork` isolates: the sketches live in the fork, and only the chosen direction returns to the parent. A narrows the scope of a single invocation without isolating what it leaves behind. B affects whether sketches get written to files, not whether they stay in conversation context. C isn't the mechanism that controls what returns to the main session.

**6. B** — `allowed-tools` restricted to reads plus file editing means the skill physically cannot run `git tag` or push it — a structural guarantee, not an advisory one. A is the advisory instruction that already failed to prevent the incident. C reviews after the fact rather than preventing the action. D catches only the push and depends on server-side configuration the skill itself doesn't control.

**7. A** — `argument-hint` prompts for the required parameter when the skill is invoked bare, closing the invocation gap that leads to fabrication. B isolates the bad output rather than preventing it from being generated. C handles the missing input politely instead of actually collecting it. D repurposes a tool-permission setting as if it were input validation, which it isn't.

**8. C** — Files identified by naming convention and spread across many directories are the glob-scoped-rule case: `paths: ["**/*.e2e.ts"]` loads the conventions whenever a matching file is edited, wherever it lives. A covers only the one directory where some specs happen to sit. B loads the section for every file, not just e2e ones. D depends on a developer remembering to run it.

**9. A** — Multiple viable architectures with cross-service constraints is plan mode's core criterion: explore the impact, compare the approaches, and commit to a design before writing code. B starts implementing before the cross-service constraints are understood. C triples the build effort to avoid making an upfront decision. D accepts a recommendation without the exploration needed to justify it.

**10. D** — Single function, known reproduction, clear expected behavior: direct execution is appropriate. Planning (A), a codebase-wide subagent (B), and forking sessions to compare regexes (C) all add process where there's no real design uncertainty to resolve.

**11. C** — Regressions on previously working cases mean nothing is pinning existing behavior in place: write the test suite first, covering all formats and edge cases, then iterate against failing tests. The suite converts whack-a-mole into steady convergence. A relies on verbal enumeration with no enforcement behind it. B abandons the utility instead of stabilizing it. D orders the fixes without doing anything to stop them from breaking each other.

**12. B** — `/compact` is the mid-session relief valve: it summarizes the conversation, reduces context usage, and preserves key information so work can continue. A discards the decisions unless they can be perfectly reconstructed from memory. C conserves output length, not context usage. D removes the work from the tool that was doing it entirely.

**13. A** — Delegate the verbose research questions to subagents and let only their summaries return — the exploration happens in their contexts while the main session's budget stays available for design. B spends the main context on the research first and compresses only afterward. C designs from assumptions instead of grounding the design in answers. D is the same idea done manually, with copy-paste standing in for the return channel.

**14. D** — Output fields the agent never actually uses should be trimmed before they enter context; a 2,000-line AST dump attached to every lint call is a textbook disproportionate tool result. A reduces call frequency but not the size of each payload. B truncates by an arbitrary line count rather than by which fields are actually used, so it's as likely to cut something needed as something irrelevant. C relocates the waste into a different context rather than removing it.

**15. C** — Long-session context degradation is countered by a scratchpad: findings recorded as they're confirmed, then consulted for later answers instead of being re-derived from a degrading context. A caps the work to avoid the failure mode rather than addressing it. B doubles the cost to detect the contradiction rather than prevent it. D re-reads constantly, which itself consumes the context budget that's already under pressure.

**16. A** — Coordinators should match invocation to query complexity: simple factual queries get a single search or a direct answer; the full pipeline is reserved for real research. B only helps on repeated queries. C makes every stage of an unnecessary pipeline cheaper instead of skipping the pipeline altogether. D turns an efficiency fix into a product regression that fails simple queries outright.

**17. C** — A bare `range(8)` makes an arbitrary turn count the only termination condition — hence the mid-topic truncation. Loop on `stop_reason` instead, with any numeric bound kept strictly as an emergency backstop. A tunes the wrong mechanism to a bigger arbitrary number. B introduces a second, unreliable heuristic for "done." D pushes an implementation bug onto the user as a configuration choice.

**18. B** — Subagents work only from what their own prompts contain: the claim-source mappings existed upstream but never reached the report agent, so it improvised citations. Pass the mappings explicitly alongside the synthesis text. A asks for restraint while still withholding the data needed to comply. C invites fresh, unvetted sourcing instead of using the sourcing that already exists. D corrects fabrications after they're generated instead of preventing them.

**19. D** — Independent analyses parallelize by emitting multiple Task calls in one coordinator response — five subagents run concurrently, and latency approaches the single-region time. A serializes all five inside one context instead. B changes freshness semantics to dodge an orchestration fix rather than fixing the orchestration. C trades away quality to chase speed unnecessarily.

**20. C** — The properties that vanished — failure localization, partial results not disappearing — are exactly what hub-and-spoke routing through the coordinator provides: observability, consistent error handling, controlled information flow. A tries to rebuild those properties as separate infrastructure instead of restoring the topology that already provided them. B patches one symptom while leaving the routing problem in place. D mistakes the cause of the speedup for proof the coordinator was pure overhead.

**21. A** — Completeness requires an evaluation loop: the coordinator checks synthesis output against required coverage, re-delegates targeted queries for the gaps, and re-invokes synthesis. B instructs synthesis to include data that may simply not have arrived yet. C formats the gap nicely without closing it. D hopes pricing shows up incidentally at higher search volume rather than ensuring it does.

**22. B** — A guarantee means interception: a hook validating every `load_document` URL against the licensed domains, blocking and redirecting anything outside them. A detects a licensing breach only after it has already happened. C remains an instruction the model can still fail to follow. D is a naming cue, not an enforcement mechanism.

**23. D** — Delegation should specify goals and quality criteria, leaving method to the specialist — dictating exact search strings is procedural micromanagement that breaks the moment a topic doesn't match the anticipated phrasing. A writes more of the same brittle thing at greater length. B adds a whole extra agent to keep generating that brittle thing. C makes adapting to results conditional on disobeying instructions.

**24. C** — Mode-switched generic tools invite wrong-mode calls; splitting into three purpose-specific tools puts the distinction at the tool level, where descriptions can actually differentiate the choices. A documents the confusion without resolving it. B substitutes a plausible-looking default for a correct one. D hides the mode decision inside inference logic instead of making the call explicit.

**25. A** — The tools differ meaningfully (curated news API, date filtering) but their descriptions don't say so — and descriptions are exactly what tool selection runs on. Rewrite both to state source, parameters, and when to prefer each. B removes real capability from the toolset. C is keyword routing standing in for genuine differentiation. D relocates the same undocumented choice into a parameter instead of resolving it.

**26. D** — Failures must be signaled through the MCP `isError` flag with structured content, or they remain indistinguishable from ordinary data — which is exactly how a quota message became a "finding." A only makes the string awkward to quote, not machine-detectable. B disguises a failure as a valid, if empty, result. C hardcodes brittle string-matching into every prompt instead of using the protocol's own error channel.

**27. B** — Standing visibility of curated content is what MCP resources are for: a catalog agents can see directly, without needing exploratory calls to stumble onto it. A duplicates the catalog into every prompt, where it will drift out of date. C secretly reweights search instead of actually exposing the collection. D reinvents a resource as a tool call plus an instruction to remember to use it.

**28. C** — Replace the generic tool with a constrained alternative: `load_source` validates every request against the allowlist, making credibility a structural boundary instead of a remembered rule. A is behavioral and depends on the agent following it. B filters evidence only after it has already shaped the analysis. D lowers rankings, but the tool itself will still fetch anything asked of it.

**29. A** — False conflicts between figures from different periods are prevented by requiring publication and collection dates in structured outputs — temporal interpretation needs temporal metadata to work with. B discards data for missing metadata that upstream agents should simply be providing. C substitutes an invented heuristic for actual verification. D escalates every instance of a class of error that can instead be eliminated systematically.

**30. B** — Deliverables must distinguish well-supported findings from gap areas caused by inaccessible sources — coverage annotations do exactly that. A hides the thinness of the coverage from the reader. C disclaims generally what should instead be marked specifically, area by area. D fills genuine evidence gaps with model guesses, which runs against a research system's whole purpose.

**31. D** — The loop is send → execute → append → **send again**: after appending tool results, the updated conversation must go back to the model for a response. Nothing happens because that continuation request was never made. A and B decorate a request that isn't actually being sent. C invents a hook-based workaround for what is really just a missing API call — no hook governs whether the harness sends the next request.

**32. A** — Unchanged code and still-valid prior context is exactly what `--resume` with a named session exists for: continuing a named investigation across separate work sessions. B discards a full day of built-up context on principle alone. C forks a session when there's no divergent path to explore yet. D recovers a single message out of an entire day's accumulated understanding.

**33. C** — Independent development of two strategies from one shared baseline is exactly `fork_session`'s purpose: two branches, no cross-contamination, no wasted re-analysis. A lets each exploration bias the other by sharing one context. B pays for the build-system analysis a second time. D — resuming the same session twice concurrently isn't a branching mechanism; forking is.

**34. B** — Open-ended optimization decomposes as: measure and map where time goes, identify the highest-impact bottlenecks, then build a prioritized plan that adapts as findings change. A applies generic fixes to a system nobody has actually measured yet. C guesses which factor dominates before checking. D substitutes anecdote for measurement as the basis for prioritization.

**35. D** — Forty services moving through identical, predictable stages call for a fixed prompt chain — the same focused passes, in the same order, for each one. A adds adaptive machinery to a workflow that doesn't vary. B is one unfocused mega-task, diluting attention across forty services at once. C gates purely mechanical work behind interviews it doesn't actually need.

**36. A** — Heterogeneous formats from many different test runners get normalized deterministically in a `PostToolUse` hook — one canonical result structure before the model ever has to reason about the raw output. B asks the model to be the parser, probabilistically, every single time. C is a multi-repo migration undertaken just to avoid writing one hook. D re-runs tests to compensate for having misread their output the first time.

**37. C** — A hard rule with an incident already on record needs tool-call interception: block `npm publish` in Bash calls and point the agent to the CI flow instead. A breaks legitimate npm use well beyond the scope of the agent. B adds a second advisory layer identical in kind to the one that just failed. D reintroduces the exact human judgment call the rule exists to remove.

**38. B** — Delegation runs on AgentDefinition descriptions, and "helps with code" / "helps with quality" gives the coordinator nothing to actually distinguish between the two. Rewrite the descriptions with specialization, tools, and selection criteria spelled out. A trains around a gap in information the coordinator still won't have at runtime. C throws more capability at a description problem. D hardcodes what a good description would express naturally and keep adaptable.

**39. A** — Finding strings inside file contents across a whole codebase, with locations, is Grep's job by design. B matches only filenames, not the comments inside files. C is Grep performed by hand, at scale, with no automation. D — the built-in tools already search file contents fine; that's the point of Grep.

**40. D** — Inventorying files by naming variant is Glob's purpose: `**/Dockerfile*` and `**/*.Dockerfile` cover the naming conventions directly. A finds the string `FROM` in any file at all, including unrelated documentation. B finds only Dockerfiles that some compose file happens to reference. C lists images already built locally, not files that exist in the repository.

**41. B** — The recommended exploration is incremental: Grep for entry points, Read the files that match, then follow the imports to trace the flow as understanding builds. A reads an entire directory just to answer one question. C accepts a diagram without checking it against the current code. D assumes the filenames encode the concept, when payment logic often lives outside any file literally named "payment."

**42. C** — Aliased re-exports (`fmtMoney`) mean the function gets called under other names entirely: enumerate all the exported names first, then Grep for each one. A finds only the direct-path importers and misses the barrel and alias paths. B assumes tooling this codebase may not even have available. D explicitly ignores the very alias the question describes.

**43. D** — A project `.mcp.json` with `${INTERNAL_API_TOKEN}` gives zero-setup, version-controlled configuration while resolving each developer's own credential from their environment — no secret ever lands in the repo. A commits a live secret into version control. B abandons zero-setup in favor of manual, per-developer configuration. C builds a bootstrap script to do what expansion already does natively.

**44. A** — The agent reaches for the tool it already understands; "Inspects schemas" gives it no reason to prefer that tool over the migration files it's used to reading. Expand the description: live structures, columns, indexes, relationships, and when to prefer it over migration files. B and C try to block or ban the fallback instead of making the better tool legible enough to choose on its own. D substitutes a shouted name for actual documentation.

**45. B** — Verbose comparative reading that feeds a downstream design decision is the Explore subagent's use case: the module reading stays isolated there, and only the comparison summary lands in the design session. A spends the design session's own context on raw module contents. C makes the design decision before the input that should inform it exists. D fragments one comparison across three separate sessions instead of keeping it whole.

**46. C** — Tool use eliminates the entire failure class: the extraction tool's input schema guarantees structure, so there's no fence and no preamble to strip in the first place. A narrows the failure without guaranteeing it away — drift can still reappear mid-output with nothing there to enforce the format. B is an instruction of exactly the kind that was already being ignored. D is an ongoing arms race against however creatively the model decides to wrap its output next.

**47. A** — A required field the source may not contain pressures the model toward fabrication; making `due_date` nullable and instructing null-when-absent removes that pressure at the source. B keeps the pressure in place and simply asks nicely against it. C catches some fabrications after the fact but misses reformatted or paraphrased dates. D turns the fabricated 30-day guess into official, unquestioned policy.

**48. D** — The extensible-category pattern: `"other"` plus a companion detail field capturing what was actually described — novel categories get represented faithfully and the enum stays machine-readable. A chases new payment methods on a quarterly cadence and permanently trails reality. B defers the real classification problem downstream, unsolved. C rejects legitimate business documents purely for using a payment method the enum hasn't caught up with yet.

**49. B** — Multiple extraction schemas, an unknown document type, and a requirement for guaranteed structured output all point to `tool_choice: "any"` — a tool call is forced, and the model picks whichever schema actually fits. A forces the wrong schema onto two of the three document types. C still permits a prose response instead of a tool call. D builds an entire classifier to replicate what `"any"` already provides directly.

**50. C** — Impossible source data should be neither passed through silently nor silently corrected: extract both dates exactly as stated and flag the pair with `conflict_detected` for review. A "fixes" data it has no way to actually verify — the drafting error could be in either date. B stalls otherwise-legitimate documents over a condition that's better flagged than blocked. D derives a value from data that's already shown itself to be unreliable.

**51. D** — The date simply isn't present in the input, so no amount of retrying can extract it — days of resubmission have bought nothing. Detect information-absent failures, stop retrying, and route to rescanning or accept a documented null instead. A and B keep retrying harder at reading a page that was never scanned. C removes a legitimate business field from the schema over one badly scanned batch.

**52. A** — Few-shot examples teach transferable judgment — how to locate and map fields across layout variation — which generalizes to structures the examples never showed; that's why they outperform trying to enumerate every layout by hand. B is possible in principle but doesn't explain a "marked" improvement across the board. C treats prompt length itself as a quality lever, which it isn't. D is a coincidence story offered with nothing to actually support it.

**53. B** — Structural variety across tables, narrative, and footnotes is the textbook few-shot case: demonstrate correct extraction from each presentation style and the model learns to handle the spread directly. A presumes a reliable narrative-to-table converter already exists, which is really the original problem restated. C triples the pipeline to avoid teaching one model the variety. D shrinks the system's coverage down to just the easy subset of cases.

**54. D** — The archive is the batch API's ideal customer: enormous, latency-tolerant, and roughly half the price. Onboarding has an actual customer waiting on the result, which calls for the synchronous API. A forfeits a major, appropriate discount for no operational benefit. B parks live customers behind a queue with no latency guarantee. C assigns both workloads to the wrong API.

**55. C** — The guarantee has to hold in the worst case: an 8-hour accumulation window plus a 24-hour batch ceiling is 32 hours, comfortably inside the 36-hour promise. A's 24 + 24 = 48 already breaches it in the worst case. B's 16 + 24 = 40 also breaches it, and "usually faster" isn't a guarantee. D starts beyond the SLA and tries to patch the shortfall with a separate expedite lane.

**56. A** — With a fixed batch budget, first-pass success on the full run is everything: refine and verify the prompt on a representative sample synchronously before spending the budget at scale. B risks discovering a flawed prompt only after the entire budget has been spent. C adjusts an unrelated sampling parameter instead of validating the prompt itself. D still burns roughly half the fixed budget before the prompt has been properly checked.

**57. B** — A model checking its own extraction retains the same reasoning that produced any errors in the first place, so it tends to approve its own mistakes. Verification should run as an independent instance comparing the output to the source, without the extractor's own context or reasoning attached. A hands the same biased checker a checklist instead of independence. C repeats the same biased check a second time. D adds a score without changing what's actually doing the checking.

**58. D** — A 96% aggregate coexisting with 61% on handwritten forms is exactly how aggregate metrics mask segment failures: accuracy has to be validated by document type (and field) before it can justify a decision, and failing segments need their own remediation. A hides the failing segment from the metric entirely. B changes which statistic is reported without addressing the underlying blindness. C accepts a segment that is wrong four times in ten.

**59. C** — Novel error patterns in an automated stream are caught by stratified random sampling of high-confidence extractions paired with ongoing human review — it measures the true error rate in exactly the place no one is otherwise looking. A can't catch a pattern that didn't exist when the benchmark set was built. B watches the scores the model reports, not the ground truth underneath them. D turns customers into the system's only QA layer.

**60. A** — Thresholds should come from calibration: measure actual accuracy at each confidence level against labeled data, then set the cutoff — per field type, if performance differs enough to warrant it — where measured accuracy meets the requirement. B and C are round numbers chosen by feel rather than by measurement. D averages past scores into a number with no established connection to actual accuracy.

---

*End of Practice Exam 5.*
