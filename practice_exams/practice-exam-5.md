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

- A) Compare Claude Code versions on the two machines and upgrade the older one.
- B) Run `/memory` on both machines to see which memory files each session actually loaded — the difference is almost certainly a configuration-loading difference (e.g., user-level files present on one machine only).
- C) Re-clone the repository on the desktop.
- D) Run `/compact` on the desktop session to clear interfering context.

**Question 2.** Your monorepo's `frontend/` packages need the React standards file and the accessibility standards file; `backend/` packages need the API standards and database standards files. All four files live in `standards/`. How do you wire this up without duplication?

- A) Concatenate all four files into the root CLAUDE.md.
- B) Copy the relevant files into each package directory.
- C) Reference all four from every package CLAUDE.md, letting Claude judge relevance.
- D) In each package's CLAUDE.md, use `@import` to pull in only the standards files relevant to that package.

**Question 3.** Your CLAUDE.md mixes testing standards, Git workflow, security rules, code style, and deployment steps in one 1,000-line file that three teams edit and constantly conflict over. What is the recommended reorganization?

- A) Split it into focused topic files under `.claude/rules/` (`testing.md`, `git-workflow.md`, `security.md`, …), each owned by the appropriate team.
- B) Freeze the file and require RFC approval for changes.
- C) Move it to a wiki and link from CLAUDE.md.
- D) Auto-generate it nightly from team documentation.

**Question 4.** Your database-seeding workflow — 300 lines of steps, fixtures, and cleanup logic — is used about once a week. Universal code conventions are used in every session. Where does each belong?

- A) Both in CLAUDE.md, since both matter.
- B) Both in skills, to minimize context cost.
- C) Conventions in CLAUDE.md (always loaded); the seeding workflow as a skill in `.claude/skills/` (loaded on demand when invoked).
- D) Conventions in a skill; the seeding workflow in CLAUDE.md.

**Question 5.** Your `/explore-alternatives` skill generates several competing design sketches. After it runs, the main session's context carries all the rejected sketches, and Claude later resurrects abandoned ideas as if they were current. What frontmatter fixes this?

- A) `argument-hint`, so the skill is scoped to one design question.
- B) `allowed-tools`, so the skill can't write the sketches to files.
- C) `paths`, restricting the skill to design documents.
- D) `context: fork` — the exploration runs in an isolated sub-agent context and only the selected direction returns to the main conversation.

**Question 6.** Your `/update-changelog` skill needs only to read the git log and edit `CHANGELOG.md`. An incident review found a run where it also executed `git tag` and pushed the tag. What is the structural fix?

- A) Add "never create or push tags" to the skill's SKILL.md.
- B) Set `allowed-tools` in the skill's frontmatter to the minimal set (read operations and file editing) so shell commands aren't available during the skill.
- C) Have developers review each skill run's transcript.
- D) Protect tags server-side so pushes fail.

**Question 7.** Your `/fix-issue` skill needs a ticket number to look up the issue before fixing it. Developers regularly invoke it bare and it fabricates an interpretation of "the issue." Which frontmatter option addresses the invocation problem?

- A) `argument-hint`, so invoking the skill without arguments prompts the developer for the required ticket number.
- B) `context: fork`, so the fabricated interpretations stay isolated.
- C) A SKILL.md instruction to refuse when no ticket is given.
- D) `allowed-tools` restricted to read-only until a ticket is provided.

**Question 8.** End-to-end test specs (`*.e2e.ts`) live next to the features they test, in dozens of directories. They must all follow your Playwright conventions. Which mechanism applies the conventions to exactly those files?

- A) A CLAUDE.md in the `tests/` directory, where some of the specs live.
- B) The root CLAUDE.md with a section headed "For e2e files only."
- C) A `.claude/rules/` file with frontmatter `paths: ["**/*.e2e.ts"]` — glob-scoped rules load whenever a matching file is edited, regardless of directory.
- D) A skill that developers run before writing e2e tests.

**Question 9.** You're adding a caching layer. Three integration approaches are viable — sidecar, library, or gateway-level — each with different infrastructure requirements, and the choice constrains several services. How do you start?

- A) Enter plan mode: explore the affected services, weigh the three approaches, and commit to a design before writing code.
- B) Direct execution starting with the simplest approach, switching if it fails.
- C) Implement all three behind a feature flag and benchmark.
- D) Ask Claude to vote for one approach and implement it immediately.

**Question 10.** A user reports that phone numbers with spaces fail validation. The regex lives in one function; the failing input and expected behavior are both known. How do you proceed?

- A) Plan mode, to consider validation architecture holistically.
- B) An Explore subagent to find all validation patterns first.
- C) A `fork_session` to compare two candidate regexes.
- D) Direct execution — a single-function fix with a clear reproduction needs no planning phase.

**Question 11.** Claude's fixes to your date-parsing utility keep regressing other formats: each fix breaks a previously working case. What iteration structure stops the whack-a-mole?

- A) Ask Claude to enumerate all formats before each fix.
- B) Freeze the utility and write a new one alongside it.
- C) Write a test suite first covering all supported formats and edge cases, then iterate by sharing failing tests — the suite pins previously working behavior while failures focus each round.
- D) Fix formats in order of usage frequency.

**Question 12.** You're deep in a productive session; context is nearly full of file dumps from earlier exploration, and you have an hour of implementation left. You want to preserve key decisions but reclaim space. What do you do?

- A) Start a new session and reconstruct decisions from memory.
- B) Run `/compact` — it summarizes the conversation, reducing context usage while preserving key information, letting the session continue.
- C) Ask Claude to respond more tersely for the remainder.
- D) Export the transcript and continue in a text editor.

**Question 13.** Your main session must design a refactor, but first you need answers to three verbose research questions (where is X implemented, who calls Y, how is Z configured). How do you keep the main session's context clean?

- A) Spawn subagents to investigate each question, returning summaries — the verbose exploration happens in their contexts while the main session coordinates.
- B) Answer the three questions first, then `/compact` before designing.
- C) Design first from assumptions, verifying afterwards.
- D) Use three terminal tabs and copy conclusions between them.

**Question 14.** Your lint MCP tool returns the full AST dump (2,000+ lines) with every lint report; the agent only ever uses the rule violations list. Sessions using the linter heavily degrade fast. What is the fix?

- A) Lint entire directories at once so the tool is called less.
- B) Have the agent skim only the top of each dump.
- C) Move linting to a subagent whose context absorbs the dumps.
- D) Trim the tool's output to the violations list before it enters context — verbose fields that are never used should not accumulate.

**Question 15.** Hour three of a security audit session: Claude begins asserting things about modules that contradict what it itself reported in hour one. The audit has hours to go. What practice should have been in place from the start (and is worth starting now)?

- A) Shorter audits — cap sessions at one hour.
- B) A second Claude instance auditing in parallel for cross-checking.
- C) An audit scratchpad file where findings are recorded as they're confirmed, consulted when answering later questions — persistent findings that don't degrade with the context.
- D) Re-reading every module before each new question.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Analytics show that 30% of user queries are simple definitions or single facts, yet every query traverses search → analysis → synthesis → report. What should the coordinator do differently?

- A) Assess each query's complexity first and invoke only what it needs — answering simple factual queries with a single search (or directly), reserving the full pipeline for genuinely complex research.
- B) Add a cache in front of the pipeline for repeated questions.
- C) Shorten each stage's prompt so the pipeline is cheaper per query.
- D) Reject simple queries with a message directing users to a search engine.

**Question 17.** Reviewing the coordinator wrapper, you find: `for turn in range(8): response = send(...)` with no other exit condition, and users report reports that stop mid-topic. What is the correct redesign?

- A) Raise the range to 20 — telemetry shows 95% of tasks finish by then.
- B) Add a check that breaks early when the response "looks complete."
- C) Loop on `stop_reason` — continue while `"tool_use"`, exit on `"end_turn"` — keeping any iteration bound strictly as an emergency backstop.
- D) Let users configure the turn budget per query.

**Question 18.** The report agent produces beautiful reports with invented citations. Investigating, you find its prompt contains the synthesis text but not the claim-source mappings the synthesis agent produced. What is the fix?

- A) Instruct the report agent to only cite when certain.
- B) Pass the claim-source mappings explicitly in the report agent's prompt alongside the synthesis — subagents receive only what is put in their prompts, and citation data that never arrives cannot be used.
- C) Give the report agent a search tool to find real citations.
- D) Have a post-processor verify and correct the citations.

**Question 19.** Five regional market analyses are needed before a global rollup; each is independent. The coordinator currently runs them one per turn, and latency is five times the single-region time. What fixes the latency?

- A) Merge the five analyses into one subagent prompt.
- B) Precompute regions on a nightly schedule so requests hit a cache.
- C) Shorten each regional analysis to a summary.
- D) Emit five Task tool calls in a single coordinator response — parallel subagent execution for independent work.

**Question 20.** An engineer wired the search agent to hand results directly to the analysis agent and the analysis agent directly to synthesis, bypassing the coordinator "for speed." Since then, failures are impossible to localize and partial results vanish silently. What does the incident illustrate?

- A) Subagent chains need distributed tracing infrastructure.
- B) Direct handoffs are fine, but each agent needs retry logic.
- C) Hub-and-spoke exists for a reason: routing inter-agent communication through the coordinator provides observability, consistent error handling, and controlled information flow — the properties that vanished.
- D) The speed gain proves the coordinator was unnecessary overhead.

**Question 21.** Competitor-analysis reports keep shipping without pricing data — the synthesis agent works with whatever arrives, and nothing checks completeness. What is the architectural fix?

- A) An iterative refinement loop: the coordinator evaluates synthesis output against the required coverage (pricing, positioning, etc.), re-delegates targeted queries for the gaps, and re-invokes synthesis until coverage is sufficient.
- B) A synthesis prompt instruction to "always include pricing."
- C) A required `pricing` section in the report template, left blank when data is missing.
- D) More search results per query so pricing shows up more often.

**Question 22.** Policy: the document analysis agent may only load documents from your licensed research library. It has a `load_document` tool that accepts any URL, and prompt instructions restricting it. You need a guarantee. What is it?

- A) A nightly job auditing which URLs were loaded.
- B) A hook intercepting `load_document` calls that blocks any URL outside the licensed library's domains, redirecting the agent to the approved catalog.
- C) A stronger system prompt listing approved domains.
- D) Renaming the tool `load_licensed_document` as a cue.

**Question 23.** Your coordinator prompt dictates exact search strings for each subagent to run. Topics that don't match the anticipated phrasing return poor results, and subagents never adapt. What is the corrected delegation style?

- A) Longer lists of predefined search strings covering more phrasings.
- B) A search-string-generation subagent feeding the search agent.
- C) Letting subagents ignore instructions when results look thin.
- D) Delegating research goals and quality criteria — what the subagent must find out and how good the answer must be — leaving search formulation to the specialist, so it can adapt.

**Question 24.** `process_source` takes `mode: "summarize" | "extract" | "verify"` and agents keep calling it with the wrong mode for the situation. What is the recommended redesign?

- A) Better documentation of the three modes in the description.
- B) A default mode so wrong calls do something reasonable.
- C) Split it into three purpose-specific tools — `summarize_source`, `extract_from_source`, `verify_against_source` — each with a clear description and contract.
- D) A wrapper that infers the mode from the arguments.

**Question 25.** Your toolset includes `search_news` ("Searches for news") and `search_web` ("Searches the web") — and agents use them interchangeably, though one hits a curated news API with date filtering and the other a general engine. What is the first fix?

- A) Rewrite both descriptions to state what each source actually is, what parameters matter (date filtering!), and when to prefer each — differentiation is what tool selection runs on.
- B) Drop `search_web` since news is the primary use case.
- C) Route by keyword: queries containing "news" go to `search_news`.
- D) Merge them into `search_all` with a source parameter.

**Question 26.** A rate-limited search tool returns a normal successful response whose content is the string "quota exceeded, try later." Agents keep summarizing this string into research notes. What is the correct tool behavior?

- A) Change the string to something less sentence-like so it won't be quoted.
- B) Return an empty result set when the quota is hit.
- C) Have the agent's prompt list known error strings to ignore.
- D) Signal the failure through the MCP `isError` flag with structured error content (category, retryability) — failures must be machine-distinguishable from data.

**Question 27.** Analysts curate 40 high-quality datasets your agents should prefer. Currently agents discover them by trial-and-error searching, often missing them entirely. How do you give agents standing visibility of the curated collection?

- A) List the datasets in every subagent's system prompt.
- B) Expose the curated collection as MCP resources — a catalog agents can see without exploratory tool calls.
- C) Boost the datasets' ranking inside the search tool.
- D) Add a `list_curated` tool agents are instructed to call first.

**Question 28.** The analysis agent's generic `fetch_page` tool keeps pulling low-quality content mills into evidence. You maintain an allowlist of credible sources. What is the strongest fix?

- A) Add the allowlist to the agent's system prompt.
- B) Post-filter evidence against the allowlist during synthesis.
- C) Replace `fetch_page` with a constrained `load_source` tool that validates requests against the allowlist — the boundary becomes structural, not behavioral.
- D) Penalize content-mill domains in the search ranking.

**Question 29.** A report describes "conflicting GDP growth figures" — 2.1% versus 3.4% — but the sources measured different years. The subagent outputs contained the numbers without dates. What is the systemic fix?

- A) Require publication and data-collection dates in subagents' structured outputs, so downstream agents can interpret differing figures temporally instead of flagging false conflicts.
- B) Have synthesis discard any figure whose date it can't infer.
- C) Prefer the higher figure, since growth data gets revised upward.
- D) Report all numeric conflicts to a human before publishing.

**Question 30.** During research on a paywalled industry, several key sources were inaccessible. The coordinator knows which topic areas are affected. What should the final deliverable contain?

- A) Only the well-covered areas, with gaps omitted for a cleaner read.
- B) Coverage annotations distinguishing well-supported findings from topic areas with gaps due to inaccessible sources — the reader must be able to see where the evidence is thin.
- C) A general disclaimer that no research is exhaustive.
- D) Model-generated estimates filling the gap areas, marked as estimates.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** Your agent calls Grep, your harness executes it and appends the `tool_result` — and then nothing happens; the agent never produces its answer. The harness logs show no further API call was made. What is missing?

- A) A `tool_choice` setting on the follow-up request.
- B) The Grep result was too large and must be truncated.
- C) A `continue: true` flag on the tool result block.
- D) The continuation request — after appending tool results, the harness must send the updated conversation back to the model; the loop is send → execute → append → send again.

**Question 32.** An engineer spent Friday building context in a named session about the notification service. Monday, with no code changes over the weekend, she wants to continue. What is the right move, and why?

- A) `--resume` the named session — prior context is still valid, and resumption is designed for continuing named investigations across work sessions.
- B) Start fresh — sessions should not span multiple days.
- C) `fork_session` so Friday's session stays pristine.
- D) Start fresh but paste in Friday's final message.

**Question 33.** From one shared analysis of your build system, you want to develop two upgrade strategies — incremental adoption versus a clean cutover — without either exploration influencing the other. Which mechanism?

- A) One session exploring both strategies in alternating messages.
- B) Two fresh sessions, each re-analyzing the build system first.
- C) `fork_session` — two independent branches from the shared analysis baseline, one strategy each.
- D) `--resume` the analysis session twice concurrently.

**Question 34.** "Make our CI builds faster" — an open-ended task with unknown bottlenecks. How should the agent decompose it?

- A) Apply the top ten generic build-speed tricks in order.
- B) First measure and map where time goes, identify the highest-impact bottlenecks, then form a prioritized plan that adapts as changes reveal new bottlenecks.
- C) Parallelize everything first, since parallelism usually dominates.
- D) Ask the team which step feels slowest and optimize that.

**Question 35.** Generating a README for each of 40 services follows identical stages: read the service manifest → summarize endpoints → document env vars → assemble the file. What decomposition pattern fits?

- A) Dynamic decomposition per service, letting the agent restructure as it sees fit.
- B) A single prompt asking for all 40 READMEs at once.
- C) An interview with each service's owner before any generation.
- D) A fixed prompt chain — the same focused stages in sequence for every service — since the workflow is predictable and repeating.

**Question 36.** Your agent runs tests across many repos; some produce JUnit XML, others plaintext summaries, others JSON. The agent frequently misreads pass/fail status in formats it saw less often. What is the reliable fix?

- A) A `PostToolUse` hook normalizing all test outputs into one canonical result structure (status, failed tests, durations) before the model processes them.
- B) A prompt appendix describing each repo's output format.
- C) Standardizing every repo on one test reporter first.
- D) Having the agent re-run ambiguous tests for a second opinion.

**Question 37.** The productivity agent automates release chores but must never run `npm publish` — releases go through CI only. It's in CLAUDE.md; an intern's session still published a package last week. What now?

- A) Revoke npm credentials from all developer machines.
- B) Add the rule to the agent's system prompt as well as CLAUDE.md.
- C) Intercept Bash tool calls with a hook that blocks `npm publish` (and equivalents), pointing the agent to the CI release flow.
- D) Have the agent ask permission before any npm command.

**Question 38.** Your coordinator delegates test-writing to whichever subagent seems right, but its choices look random. The subagent definitions read: "Agent A — helps with code," "Agent B — helps with quality." What is the fix?

- A) Add few-shot delegation examples to the coordinator prompt.
- B) Rewrite the AgentDefinition descriptions to state each subagent's actual specialization, tools, and when it should be selected — the coordinator's delegation runs on these descriptions.
- C) Replace the coordinator's model with a larger one.
- D) Hardcode a task-type-to-agent routing table.

**Question 39.** You need every `TODO` and `FIXME` comment across the codebase, with file locations. Which tool does this directly?

- A) Grep — pattern search across file contents is exactly its job.
- B) Glob with the pattern `**/TODO*`.
- C) Read on each file, collecting matches manually.
- D) An MCP code-index server, since built-ins can't search comments.

**Question 40.** The agent must inventory every Dockerfile in the monorepo — `Dockerfile`, `Dockerfile.dev`, `api.Dockerfile` — wherever they live. Which tool call?

- A) Grep for `FROM ` across all files and collect the filenames.
- B) Read the docker-compose files and follow references.
- C) Bash `docker images` to enumerate what's built.
- D) Glob with patterns matching the Dockerfile naming variants (e.g., `**/Dockerfile*`, `**/*.Dockerfile`) — filename matching is Glob's purpose.

**Question 41.** Asked how payment processing works in an unfamiliar codebase, which exploration sequence reflects the recommended practice?

- A) Read every file in `src/payments/` end to end, then answer.
- B) Grep for entry points (route handlers, "payment" imports, processor SDK calls), Read the files that match, and follow the imports to trace the flow — building understanding incrementally.
- C) Answer from the architecture diagram in the wiki, verifying nothing.
- D) Glob for `*payment*` and read only exact-name matches.

**Question 42.** `formatCurrency` is defined in `src/utils/money.ts` but consumed via two barrel files and one aliased re-export (`export { formatCurrency as fmtMoney }`). You need every real call site. What is the correct strategy?

- A) Grep for `utils/money` and read the matching importers.
- B) Rely on rename-refactor tooling to enumerate references.
- C) First enumerate all names the function is exported under (including `fmtMoney`), then Grep for each name across the codebase.
- D) Grep for `formatCurrency` only — aliases are rare enough to ignore.

**Question 43.** The team's internal-API MCP server needs a per-developer token. You want zero-setup onboarding via the repo without leaking credentials. Which configuration?

- A) Token embedded in `.mcp.json`, with the repo private as the safeguard.
- B) Each developer maintains their own `~/.claude.json` entry from a wiki recipe.
- C) A bootstrap script that writes `.mcp.json` locally on first run.
- D) Project `.mcp.json` committed with the token referenced as `${INTERNAL_API_TOKEN}` — environment-variable expansion resolves each developer's own credential at runtime.

**Question 44.** Your `schema-inspector` MCP tool answers database-structure questions precisely, but the agent keeps Grep-ing through migration files instead, producing stale answers. The tool's description: "Inspects schemas." What is the recommended fix?

- A) Expand the tool's description — it returns live table structures, columns, indexes, and relationships, and should be preferred over reading migration files for current-schema questions.
- B) Delete the migrations directory from the agent's view.
- C) Add a system prompt rule: never Grep in `migrations/`.
- D) Rename the tool `USE_THIS_FOR_SCHEMAS`.

**Question 45.** Before designing a plugin API, the agent should compare three candidate integration points, each requiring reading several large modules. The comparison itself is the input to your main design session. How do you structure this?

- A) Read all the modules in the design session and accept the context cost.
- B) Use the Explore subagent for the comparison — verbose module reading stays in its isolated context, and the design session receives the comparison summary.
- C) Design first, then check the integration points afterwards.
- D) Split the design across three sessions, one per candidate.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your invoice extractor prompts for "a JSON response" and parses the text. Failures cluster around markdown fences and apologetic preambles ("Here is the extracted data:"). What eliminates the failure class?

- A) A response prefix trick — pre-filling the assistant turn with `{`.
- B) A prompt rule: "no prose, no fences, JSON only."
- C) Tool use — define an extraction tool whose input schema is the invoice structure and read the guaranteed-shape data from the `tool_use` block.
- D) A tolerant parser that strips fences and leading prose.

**Question 47.** Receipts often genuinely lack a due date, but `due_date` is required in your schema — and audits found the model quietly inserting a date 30 days after the purchase date. What is the correct fix?

- A) Make `due_date` optional/nullable and instruct the model to return null when the document has none — a required field the source can't satisfy invites fabrication.
- B) Keep it required but add "never invent dates" to the prompt.
- C) Post-validate that due dates appear verbatim in the source text.
- D) Default the field server-side to 30 days, making the model's behavior official.

**Question 48.** Your `payment_method` enum covers `["card", "cash", "bank_transfer"]`. Documents now mention regional wallets, crypto, and buy-now-pay-later services — all being forced into `"card"`. How should the schema evolve?

- A) Add the ten most common new methods to the enum each quarter.
- B) Make the field free text and classify downstream.
- C) Reject documents with unrecognized payment methods.
- D) Add `"other"` to the enum with a companion detail field capturing the actual method — the extensible-category pattern.

**Question 49.** A shared intake pipeline receives invoices, contracts, and HR forms mixed together, each with its own extraction tool defined. You need guaranteed structured output on every document without pre-classifying. Which setting?

- A) `tool_choice` forced to the invoice tool, the most common type.
- B) `tool_choice: "any"` — the model must call one of the tools and picks the schema matching the document.
- C) `tool_choice: "auto"` plus a prompt instruction to always extract.
- D) Three pipeline lanes with a rules-based classifier in front.

**Question 50.** Contracts occasionally arrive with a stated term whose end date precedes its start date (drafting or OCR errors). Downstream date math silently produces negative durations. What extraction design surfaces the problem?

- A) Swap the dates when end precedes start, since that's obviously the intent.
- B) Reject any contract whose dates are out of order.
- C) Extract both dates as stated and set a `conflict_detected` boolean when the ordering is impossible — inconsistent source data gets flagged for review, neither silently passed nor silently "fixed."
- D) Extract only the start date, deriving the end from the stated term length.

**Question 51.** `signatory_date` keeps failing extraction on a batch of scanned agreements. Sampling shows the signature page simply wasn't scanned — the date isn't in the input. The retry system has been resubmitting these documents for days. What is the correct assessment?

- A) Increase retries with prompt variations until the model finds the dates.
- B) The retries would work with a larger context window.
- C) The field should be removed from the schema.
- D) These retries can never succeed — the information is absent from the input. Detect this case, stop retrying, and route to the rescanning workflow (or accept null with a documented reason).

**Question 52.** You added few-shot examples covering three vendors' invoice layouts. Extraction then also improved markedly on a fourth vendor whose layout none of the examples showed. What explains this?

- A) Few-shot examples teach the underlying judgment — how to locate and map fields across layout variation — which the model generalizes to novel structures, rather than memorizing the specific layouts shown.
- B) The fourth vendor's layout must coincidentally match one of the three.
- C) The examples increased the prompt length, which always improves accuracy.
- D) A model update shipped at the same time; the examples were irrelevant.

**Question 53.** Financial filings present the same facts sometimes in tables, sometimes in narrative paragraphs, sometimes in footnotes. Your extractor handles tables well and misses the rest. What is the recommended fix?

- A) Preprocess filings to convert all narrative into tables.
- B) Add few-shot examples demonstrating correct extraction from each presentation — tabular, narrative, and footnote — so the model handles the structural variety.
- C) Run three extractors, one per presentation style, and merge.
- D) Restrict extraction to the tables and flag the rest for humans.

**Question 54.** Two workloads: (1) re-extracting your ten-year document archive with an improved schema, results needed "sometime this quarter"; (2) extracting data from documents customers upload during a live onboarding flow. Assign the APIs.

- A) Synchronous for both — simpler to operate.
- B) Batch for both — the discount is too large to pass up.
- C) Batch for the onboarding flow since volume is high; synchronous for the archive.
- D) Batch API for the archive (massive, latency-tolerant, 50% cheaper); synchronous API for onboarding (a customer is waiting on the result).

**Question 55.** Your contract guarantees extraction results within 36 hours of document receipt. Batch processing takes up to 24 hours. Documents arrive continuously. Which accumulation window keeps the guarantee?

- A) 24 hours — one daily batch is operationally cleanest.
- B) 16 hours, since batches usually complete in far less than 24.
- C) 8 hours — worst case 8 + 24 = 32 hours, within the guarantee with margin.
- D) 48 hours with an expedite lane for old documents.

**Question 56.** Legal has approved extracting 10,000 archived medical consent forms with a new prompt. The batch budget is fixed. What do you do before submitting the full batch?

- A) Refine and verify the prompt on a representative sample via the synchronous API first — maximizing first-pass success so the fixed budget isn't spent on a flawed full run.
- B) Submit the full batch immediately; failures can be resubmitted within budget.
- C) Submit the batch at half temperature to be safe.
- D) Split into two 5,000-form batches and correct between them.

**Question 57.** Your extraction step ends with "double-check your extraction against the document" — and reports itself accurate. Auditors keep finding wrong values the self-check approved. What does the guide say about this design?

- A) The self-check needs a rubric listing common error types.
- B) A model checking its own extraction retains the reasoning that produced the errors; verification should run as an independent instance comparing output to source without the extractor's context.
- C) The self-check should run twice, with disagreements escalated.
- D) Self-checks work if you also request a confidence score.

**Question 58.** Your dashboard proudly shows 96% extraction accuracy. A operations manager mentions that handwritten intake forms "seem to always be wrong." You segment the data: typed forms 99%, handwritten 61%. What is the lesson?

- A) Handwritten forms should be excluded from the accuracy metric.
- B) The dashboard should show median accuracy instead of mean.
- C) 96% was still accurate as an overall number, so no process change is needed.
- D) Aggregate metrics mask segment failures — accuracy must be validated by document type (and field) before it can justify decisions like reducing review, and segments like handwritten forms need their own remediation.

**Question 59.** After automating high-confidence extractions, you need an ongoing mechanism to catch error patterns the confidence model doesn't know about yet. What is it?

- A) Quarterly re-validation against the original benchmark set.
- B) Alerting when confidence scores drift statistically.
- C) Stratified random sampling of high-confidence extractions for continuous human review — measuring the true error rate and surfacing novel error patterns in the automated stream.
- D) A user-facing "report an error" button on downstream systems.

**Question 60.** The model emits per-field confidence scores, and you plan to auto-accept above a threshold. A colleague proposes 0.9 "because it's high." What is the defensible way to choose?

- A) Calibrate against a labeled validation set: measure actual field accuracy at each score level and set thresholds (per field type if needed) where measured accuracy meets the requirement.
- B) Adopt 0.9 but review the first month's auto-accepts.
- C) Use 0.99 — stricter is safer, whatever the data says.
- D) Average the last quarter's scores and use that as the threshold.

---
# Answer Key — Practice Exam 5

**Quick key:** 1-B, 2-D, 3-A, 4-C, 5-D, 6-B, 7-A, 8-C, 9-A, 10-D, 11-C, 12-B, 13-A, 14-D, 15-C, 16-A, 17-C, 18-B, 19-D, 20-C, 21-A, 22-B, 23-D, 24-C, 25-A, 26-D, 27-B, 28-C, 29-A, 30-B, 31-D, 32-A, 33-C, 34-B, 35-D, 36-A, 37-C, 38-B, 39-A, 40-D, 41-B, 42-C, 43-D, 44-A, 45-B, 46-C, 47-A, 48-D, 49-B, 50-C, 51-D, 52-A, 53-B, 54-D, 55-C, 56-A, 57-B, 58-D, 59-C, 60-A

---

**1. B** — Same repo, different behavior across machines points at configuration loading, and `/memory` shows exactly which memory files each session loaded — diagnose before changing anything. The likely culprit is user-level configuration present on one machine only. A, C, and D change things before establishing what differs.

**2. D** — `@import` lets each package's CLAUDE.md include only the standards files relevant to it — one copy of each standard, selectively composed. A loads everything everywhere. B duplicates and drifts. C loads all four and hopes the model scopes them correctly.

**3. A** — The recommended structure for a contested monolith: topic-specific files under `.claude/rules/`, each owned by the team that owns the topic — smaller diffs, fewer conflicts, clearer ownership. B freezes the pain in place. C removes the content from Claude's view. D generates a monolith instead of splitting it.

**4. C** — The dividing line: universal always-applicable content in CLAUDE.md; occasional task-specific workflows as skills loaded on invocation. A pays 300 lines of seeding logic in every session. B makes universal conventions opt-in. D is backwards on both.

**5. D** — Exploratory content that shouldn't persist is what `context: fork` isolates: the sketches live in the fork, and only the chosen direction returns. A narrows scope without isolating the residue. B affects file writes, not conversation context. C isn't the mechanism for this.

**6. B** — `allowed-tools` restricted to reads plus file editing means the skill physically cannot run `git tag` or push — structural, not advisory. A is the advisory approach that already failed. C reviews after the fact. D catches only the push, not the local mutation, and depends on server config.

**7. A** — `argument-hint` prompts for the required parameter when the skill is invoked bare — fixing the invocation gap that causes the fabrication. B isolates the bad output instead of preventing it. C handles the failure politely rather than collecting the input. D misuses tool permissions as input validation.

**8. C** — Files identified by naming convention and spread across directories are the glob-rule case: `paths: ["**/*.e2e.ts"]` loads the conventions exactly when those files are edited. A covers only one location of many. B loads always and scopes never. D depends on someone remembering.

**9. A** — Multiple viable architectures with cross-service constraints is plan mode's core criterion: explore, compare, and commit to a design before code. B ships the first idea and discovers constraints by failure. C triples the work to avoid a decision. D takes the recommendation without the exploration that justifies it.

**10. D** — Single function, known reproduction, clear expected behavior: direct execution. Planning (A), repo-wide exploration (B), and session forking (C) add process where there is no design uncertainty.

**11. C** — Regressions on previously working cases mean nothing is pinning existing behavior: write the test suite first (all formats, edge cases), then iterate on failing tests. The suite converts whack-a-mole into convergence. A relies on enumeration without enforcement. B abandons instead of stabilizing. D orders the moles without stopping the whacking.

**12. B** — `/compact` is the mid-session relief valve: summarize the conversation, reduce usage, preserve key information, keep working. A discards the decisions unless you can reconstruct them perfectly. C conserves output, not context. D takes the work out of the tool entirely.

**13. A** — Delegate the verbose questions to subagents and let summaries return — exploration happens in their contexts while the main session keeps its budget for design. B spends the main context first and compresses after. C designs on assumptions. D is manual subagents with copy-paste as the protocol.

**14. D** — Output fields the agent never uses should be trimmed before entering context; a 2,000-line AST dump attached to every lint call is the textbook disproportionate tool result. A batches the bloat. B — the agent can't "skim" what's already in context. C relocates the waste.

**15. C** — Long-session context degradation is countered by a scratchpad: findings recorded as confirmed, consulted for later answers — ground truth that doesn't decay. A caps the work to fit the failure mode. B doubles cost to detect the problem rather than prevent it. D re-spends context constantly, accelerating the degradation.

**16. A** — Coordinators should match invocation to query complexity: simple factual queries get a single search or a direct answer; the full pipeline is for real research. B helps only repeats. C makes every unnecessary stage cheaper instead of skipping it. D turns an efficiency fix into a product regression.

**17. C** — A bare `range(8)` makes an arbitrary cap the only termination — hence mid-topic truncation. Loop on `stop_reason`, with any bound kept strictly as an emergency backstop. A tunes the wrong mechanism. B adds a "looks complete" heuristic — a second anti-pattern. D makes users configure a bug.

**18. B** — Subagents use only what their prompts contain: the mappings existed upstream but never reached the report agent, so it improvised. Pass the claim-source mappings explicitly with the synthesis. A asks for restraint while withholding the data. C invites fresh, unvetted sourcing. D corrects fabrications after generation instead of preventing them.

**19. D** — Independent analyses parallelize via multiple Task calls in one coordinator response — five subagents at once, latency near single-region time. A serializes inside one context. B changes freshness semantics to dodge an orchestration fix. C trades quality for speed unnecessarily.

**20. C** — The lost properties — failure localization, non-vanishing partial results — are exactly what hub-and-spoke routing through the coordinator provides: observability, consistent error handling, controlled information flow. A rebuilds those properties as infrastructure around a broken topology. B patches one symptom. D mistakes the cause of the speedup for proof the coordinator was waste.

**21. A** — Completeness requires an evaluation loop: the coordinator checks synthesis against required coverage, re-delegates targeted queries for gaps, and re-invokes synthesis. B instructs synthesis to include data it may not have. C formats the gap nicely. D hopes volume delivers pricing incidentally.

**22. B** — A guarantee means interception: a hook validating every `load_document` URL against the licensed domains, blocking and redirecting anything else. A detects violations after the licensing breach. C remains probabilistic. D is a naming hint, not a control.

**23. D** — Delegation should specify goals and quality criteria, leaving method to the specialist — dictated search strings are procedural micromanagement that breaks on unanticipated topics. A writes more of the brittle thing. B adds an agent to generate the brittle thing. C makes adaptation an act of disobedience.

**24. C** — Mode-switched generic tools invite wrong-mode calls; split into three purpose-specific tools with clear contracts so selection happens at the tool level, where descriptions can differentiate. A documents the confusion. B substitutes silent wrong behavior. D hides the decision in inference.

**25. A** — The tools differ meaningfully (curated news API, date filtering) but their descriptions don't say so — and descriptions are what selection runs on. Rewrite both to state source, parameters, and when to prefer each. B removes real capability. C is keyword routing. D relocates the choice into a parameter with the same documentation problem.

**26. D** — Failures must be signaled through the MCP `isError` flag with structured content, or they're indistinguishable from data — hence quota messages becoming "findings." A makes the string less quotable, not machine-distinguishable. B disguises failure as a valid empty result. C hardcodes error strings into prompts.

**27. B** — Standing visibility of curated content is what MCP resources provide: a catalog agents see without exploratory calls. A duplicates the catalog into every prompt and drifts. C secretly reweights search instead of exposing the collection. D reinvents resources as a tool call plus an instruction.

**28. C** — Replace the generic tool with a constrained alternative: `load_source` validates against the allowlist, making credibility a structural boundary. A is behavioral. B filters evidence after it has shaped analysis. D lowers rankings but the tool still fetches anything.

**29. A** — False conflicts between figures from different periods are prevented by requiring publication/collection dates in structured outputs — temporal interpretation needs temporal metadata. B discards data for missing what upstream should provide. C is an invented heuristic. D escalates a class of error you can eliminate systematically.

**30. B** — Deliverables must distinguish well-supported findings from gap areas caused by inaccessible sources — coverage annotations. A hides the thinness. C disclaims generally what should be marked specifically. D fills evidence gaps with model guesses, the opposite of a research system's contract.

**31. D** — The loop is send → execute → append → **send again**: after appending tool results, the updated conversation must go back to the model. Nothing happens because the continuation request was never made. A, B, and C decorate a request that isn't being sent.

**32. A** — Unchanged code and valid prior context is exactly what `--resume` with a named session is for: continuing a named investigation across work sessions. B discards a day of context on principle. C forks with no divergence to explore. D recovers one message out of a day's understanding.

**33. C** — Independent development of two strategies from one shared baseline is `fork_session`'s purpose: two branches, no cross-contamination, no re-analysis. A lets each exploration bias the other. B re-pays for the analysis. D — resuming twice concurrently isn't the branching mechanism; forking is.

**34. B** — Open-ended optimization decomposes as: measure and map, identify highest-impact bottlenecks, build a prioritized plan that adapts as findings change. A applies generic fixes to an unmeasured system. C guesses the dominant factor. D substitutes anecdote for measurement.

**35. D** — Forty services through identical, predictable stages: a fixed prompt chain, the same focused passes per service. A adds adaptive machinery where nothing varies. B is one unfocused mega-task — attention dilution across 40 services. C gates mechanical work on interviews it doesn't need.

**36. A** — Heterogeneous formats from many sources are normalized deterministically in a `PostToolUse` hook — one canonical result structure before the model reasons. B asks the model to be the parser, probabilistically, every time. C is a multi-team migration to avoid a hook. D re-runs tests to compensate for misreading their output.

**37. C** — A hard rule with an incident on record needs tool-call interception: block `npm publish` in Bash calls and point to the CI flow. A breaks legitimate npm use beyond the agent. B adds a second advisory layer. D reintroduces the human error the rule exists to prevent.

**38. B** — Delegation runs on AgentDefinition descriptions, and "helps with code/quality" gives the coordinator nothing to distinguish. Rewrite the descriptions with specialization, tools, and selection criteria. A trains around missing information. C throws capability at an information gap. D hardcodes what descriptions express naturally.

**39. A** — Finding strings in file contents across a codebase is Grep. B matches filenames, not comments. C is Grep by hand at scale. D — built-ins search content fine; that's the point of Grep.

**40. D** — Inventorying files by naming variants is Glob: `**/Dockerfile*` and `**/*.Dockerfile`. A finds `FROM` in any file, including docs and vendored code. B finds only referenced Dockerfiles. C lists built images, not files in the repo.

**41. B** — Recommended exploration is incremental: Grep for entry points, Read the matches, follow imports to trace the flow. A reads everything for one question. C verifies nothing. D assumes filenames encode the concept — payment logic often lives elsewhere.

**42. C** — Aliased re-exports (`fmtMoney`) mean the function is called by other names: enumerate all exported names first, then Grep for each. A finds direct-path importers only. B assumes tooling this codebase may not have — and the question asks for the built-in tool strategy. D explicitly ignores the alias that exists.

**43. D** — Project `.mcp.json` with `${INTERNAL_API_TOKEN}` gives zero-setup, version-controlled configuration with per-developer credentials resolved from the environment — no secret in the repo. A commits a secret. B abandons zero-setup. C generates what expansion provides natively.

**44. A** — The agent picks the tool it understands; "Inspects schemas" gives no case against Grep-ing familiar migration files. Enhance the description: live structures, columns, indexes, relationships, preferred for current-schema questions. B and C block or ban the fallback rather than making the better tool legible. D abuses naming as documentation.

**45. B** — Verbose comparative reading that feeds a design decision is the Explore subagent's case: module reading stays isolated, the summary lands in the design session. A spends the design context on raw input. C designs before the input exists. D fragments one comparison across three contexts.

**46. C** — Tool use eliminates the failure class: the extraction tool's input schema guarantees structure — no fences, no preambles, no prose. A (prefill) narrows the failure without a guarantee — drift can still appear mid-output and nothing enforces the schema. B is an instruction, already being violated. D is an arms race with formatting variety.

**47. A** — A required field the source may not contain pressures the model to fabricate; make `due_date` nullable and instruct null when absent. B keeps the pressure and adds a plea. C catches some fabrications after the fact (and fails on reformatted dates). D institutionalizes the fabrication.

**48. D** — The extensible-category pattern: `"other"` plus a detail field capturing the actual method — novel categories are represented faithfully, and the enum stays machine-readable. A chases reality quarterly and always trails it. B pushes classification downstream, unsolved. C rejects valid business documents.

**49. B** — Multiple extraction schemas, unknown document type, structured output required: `tool_choice: "any"` — a tool call is guaranteed, and the model selects the schema fitting the document. A forces the wrong schema onto two of three types. C permits prose. D builds a router to replicate what "any" does.

**50. C** — Impossible source data is neither passed through silently nor silently corrected: extract as stated and flag with `conflict_detected` for review. A "fixes" data it cannot verify — the drafting error might be in either field. B stalls legitimate documents over a flag-able condition. D derives from data already suspect.

**51. D** — The date isn't in the input, so no retry can extract it — days of resubmission bought nothing. Detect information-absent failures, stop retrying, and route to rescanning or accept a documented null. A and B retry harder at reading an unscanned page. C deletes a real business field because one batch was scanned badly.

**52. A** — Few-shot examples teach transferable judgment — how to locate and map fields across layout variation — which generalizes to unseen structures; that's why they beat exhaustive per-layout rules. B is possible but explains nothing generalizable and contradicts "markedly improved." C — prompt length isn't a quality mechanism. D is an unfalsifiable dodge.

**53. B** — Structural variety (tables, narrative, footnotes) is the few-shot case: demonstrate correct extraction from each presentation and the model handles the spread. A presumes a reliable narrative-to-table converter — the original problem restated. C triples the pipeline. D shrinks automation to the easy subset.

**54. D** — The archive is the Batch API's ideal customer: enormous, latency-tolerant, half price. Onboarding has a customer waiting — synchronous. A forfeits major savings. B parks live customers behind a no-SLA queue. C is backwards on both.

**55. C** — The guarantee must hold in the worst case: 8-hour accumulation + 24-hour processing = 32 ≤ 36 with margin. A gives 48 worst case. B's 16 + 24 = 40 breaches the SLA, and "usually faster" isn't a guarantee. D starts beyond the SLA and patches with an expedite lane.

**56. A** — With a fixed budget, first-pass success is everything: refine the prompt on a representative sample synchronously, verify, then submit the batch. B spends the budget discovering flaws at full scale. C tweaks a parameter instead of validating the prompt. D still burns half the budget on the unvalidated version.

**57. B** — A model verifying its own extraction retains the reasoning that produced the errors — self-checks approve their own mistakes. Verification must be an independent instance comparing output to source without the extractor's context. A gives the biased checker a rubric. C repeats the biased check. D scores it.

**58. D** — 96% aggregate coexisting with 61% on handwritten forms is exactly how aggregate metrics mask segment failures: validate by document type and field before the number justifies anything, and remediate the failing segment. A hides the problem from the metric. B changes the statistic, not the blindness. C accepts a segment that's wrong 4 times in 10.

**59. C** — Novel error patterns in the automated stream are caught by stratified random sampling of high-confidence extractions with ongoing human review — measuring true error rates where no one otherwise looks. A can't contain patterns that didn't exist at benchmark time. B watches the scores, not the truth. D makes customers the QA layer.

**60. A** — Thresholds come from calibration: measure actual accuracy at each confidence level against labeled data, and set the cutoff (per field type if performance differs) where accuracy meets requirements. B and C are round numbers with different vibes. D averages scores into a threshold with no connection to accuracy.

---

*End of Practice Exam 5.*
