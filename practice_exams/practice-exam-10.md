# CCAFC Practice Exam 10

**Claude Certified Architect – Foundations — Practice Exam**

Rebalanced edition of Practice Exam 5 — same knowledge points; options rewritten to remove test-taking tells (option-length cues, giveaway distractors), answer letters reshuffled, one duplicate question replaced, and two internally inconsistent items corrected.

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
- B) Re-clone the repository on the desktop.
- C) Run `/memory` on both machines to see which memory files each session actually loaded.
- D) Run `/compact` on the desktop session to clear interfering context.

**Question 2.** Your monorepo's `frontend/` packages need the React standards file and the accessibility standards file; `backend/` packages need the API standards and database standards files. All four files live in `standards/`. How do you wire this up without duplication?

- A) In each package's CLAUDE.md, use `@import` to pull in only the standards files relevant to that package.
- B) Concatenate all four files into the root CLAUDE.md.
- C) Copy the relevant files into each package directory.
- D) Reference all four from every package CLAUDE.md, letting Claude judge relevance.

**Question 3.** Your CLAUDE.md mixes testing standards, Git workflow, security rules, code style, and deployment steps in one 1,000-line file that three teams edit and constantly conflict over. What is the recommended reorganization?

- A) Freeze the file and require RFC approval for changes.
- B) Move it to a wiki and link from CLAUDE.md.
- C) Auto-generate it nightly from team documentation.
- D) Split it into focused topic files under `.claude/rules/`, each owned by the appropriate team.

**Question 4.** Your database-seeding workflow — 300 lines of steps, fixtures, and cleanup logic — is used about once a week. Universal code conventions are used in every session. Where does each belong?

- A) Both in CLAUDE.md, since both matter.
- B) Conventions in CLAUDE.md (always loaded); the seeding workflow as a skill in `.claude/skills/`.
- C) Both in skills, to minimize context cost.
- D) Conventions in a skill; the seeding workflow in CLAUDE.md.

**Question 5.** Your `/explore-alternatives` skill generates several competing design sketches. After it runs, the main session's context carries all the rejected sketches, and Claude later resurrects abandoned ideas as if they were current. What frontmatter fixes this?

- A) `context: fork` — the exploration runs isolated and only the selected direction returns.
- B) `argument-hint`, so the skill is scoped to one design question.
- C) `allowed-tools`, so the skill can't write the sketches to files.
- D) `paths`, restricting the skill to design documents.

**Question 6.** Your `/update-changelog` skill needs only to read the git log and edit `CHANGELOG.md`. An incident review found a run where it also executed `git tag` and pushed the tag. What is the structural fix?

- A) Add "never create or push tags" to the skill's SKILL.md.
- B) Have developers review each skill run's transcript.
- C) Protect tags server-side so pushes fail.
- D) Set `allowed-tools` to the minimum the skill needs: Read, Edit, and Bash scoped to `git log` only.

**Question 7.** Your `/fix-issue` skill needs a ticket number to look up the issue before fixing it. Developers regularly invoke it bare and it fabricates an interpretation of "the issue." Which frontmatter option addresses the invocation problem?

- A) `context: fork`, so the fabricated interpretations stay isolated.
- B) A SKILL.md instruction to refuse when no ticket is given.
- C) `argument-hint`, prompting the developer for the required ticket number on bare invocation.
- D) `allowed-tools` restricted to read-only until a ticket is provided.

**Question 8.** End-to-end test specs (`*.e2e.ts`) live next to the features they test, in dozens of directories. They must all follow your Playwright conventions. Which mechanism applies the conventions to exactly those files?

- A) A CLAUDE.md in the `tests/` directory, where some of the specs live.
- B) A `.claude/rules/` file with frontmatter `paths: ["**/*.e2e.ts"]`.
- C) The root CLAUDE.md with a section headed "For e2e files only."
- D) A skill that developers run before writing e2e tests.

**Question 9.** You're adding a caching layer. Three integration approaches are viable — sidecar, library, or gateway-level — each with different infrastructure requirements, and the choice constrains several services. How do you start?

- A) Direct execution starting with the simplest approach, switching if it fails.
- B) Implement all three behind a feature flag and benchmark.
- C) Prototype whichever approach is fastest to build and decide from that spike.
- D) Enter plan mode: explore the affected services, weigh the three approaches, and settle the design first.

**Question 10.** A user reports that phone numbers with spaces fail validation. The regex lives in one function; the failing input and expected behavior are both known. How do you proceed?

- A) Direct execution — a single-function fix with a clear reproduction needs no planning phase.
- B) Plan mode, to consider validation architecture holistically.
- C) An Explore subagent to find all validation patterns first.
- D) A `fork_session` to compare two candidate regexes.

**Question 11.** Claude's fixes to your date-parsing utility keep regressing other formats: each fix breaks a previously working case. What iteration structure stops the whack-a-mole?

- A) Ask Claude to enumerate all formats before each fix.
- B) Write a test suite first covering all formats and edge cases, then iterate by sharing the failing tests.
- C) Freeze the utility and write a new one alongside it.
- D) Fix formats in order of usage frequency.

**Question 12.** You're deep in a productive session; context is nearly full of file dumps from earlier exploration, and you have an hour of implementation left. You want to preserve key decisions but reclaim space. What do you do?

- A) Start a new session and reconstruct decisions from memory.
- B) Ask Claude to respond more tersely for the remainder.
- C) Run `/compact` to summarize the conversation, preserving key information while reclaiming space.
- D) Export the transcript and continue in a text editor.

**Question 13.** Your main session must design a refactor, but first you need answers to three verbose research questions (where is X implemented, who calls Y, how is Z configured). How do you keep the main session's context clean?

- A) Answer the three questions first, then `/compact` before designing.
- B) Design first from assumptions, verifying afterwards.
- C) Investigate each question in the main session, running `/clear` between questions.
- D) Spawn subagents to investigate each question, returning summaries to the main session.

**Question 14.** Your lint MCP tool returns the full AST dump (2,000+ lines) with every lint report; the agent only ever uses the rule violations list. Sessions using the linter heavily degrade fast. What is the fix?

- A) Trim the tool's output to the violations list before it enters context.
- B) Lint entire directories at once so the tool is called less.
- C) Have the agent skim only the top of each dump.
- D) Move linting to a subagent whose context absorbs the dumps.

**Question 15.** Hour three of a security audit session: Claude begins asserting things about modules that contradict what it itself reported in hour one. The audit has hours to go. What practice should have been in place from the start (and is worth starting now)?

- A) Shorter audits — cap sessions at one hour.
- B) An audit scratchpad file where findings are recorded as confirmed and consulted for later questions.
- C) A second Claude instance auditing in parallel for cross-checking.
- D) Re-reading every module before each new question.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Analytics show that 30% of user queries are simple definitions or single facts, yet every query traverses search → analysis → synthesis → report. What should the coordinator do differently?

- A) Add a cache in front of the pipeline for repeated questions.
- B) Shorten each stage's prompt so the pipeline is cheaper per query.
- C) Assess each query's complexity and invoke only what it needs — a single search for simple facts.
- D) Route simple queries to a smaller, cheaper model running the same full pipeline.

**Question 17.** Reviewing the coordinator wrapper, you find: `for turn in range(8): response = send(...)` with no other exit condition, and users report reports that stop mid-topic. What is the correct redesign?

- A) Loop on `stop_reason` — continue on `"tool_use"`, exit on `"end_turn"` — with any bound kept as a backstop.
- B) Raise the range to 20 — telemetry shows 95% of tasks finish by then.
- C) Add a check that breaks early when the response "looks complete."
- D) Let users configure the turn budget per query.

**Question 18.** The report agent produces beautiful reports with invented citations. Investigating, you find its prompt contains the synthesis text but not the claim-source mappings the synthesis agent produced. What is the fix?

- A) Instruct the report agent to only cite when certain.
- B) Give the report agent a search tool to find real citations.
- C) Have a post-processor verify and correct the citations.
- D) Pass the claim-source mappings explicitly in the report agent's prompt alongside the synthesis.

**Question 19.** Five regional market analyses are needed before a global rollup; each is independent. The coordinator currently runs them one per turn, and latency is five times the single-region time. What fixes the latency?

- A) Merge the five analyses into one subagent prompt.
- B) Emit five Task tool calls in a single coordinator response so the analyses run in parallel.
- C) Precompute regions on a nightly schedule so requests hit a cache.
- D) Shorten each regional analysis to a summary.

**Question 20.** An engineer wired the search agent to hand results directly to the analysis agent and the analysis agent directly to synthesis, bypassing the coordinator "for speed." Since then, failures are impossible to localize and partial results vanish silently. What does the incident illustrate?

- A) Subagent chains need distributed tracing infrastructure.
- B) Direct handoffs are fine, but each agent needs retry logic.
- C) The speed gain proves the coordinator was unnecessary overhead.
- D) Hub-and-spoke routing exists for these exact properties: observability, error handling, controlled information flow.

**Question 21.** Competitor-analysis reports keep shipping without pricing data — the synthesis agent works with whatever arrives, and nothing checks completeness. What is the architectural fix?

- A) A synthesis prompt instruction to "always include pricing."
- B) A required `pricing` section in the report template, left blank when data is missing.
- C) A refinement loop: the coordinator checks synthesis against required coverage and re-delegates for the gaps.
- D) More search results per query so pricing shows up more often.

**Question 22.** Policy: the document analysis agent may only load documents from your licensed research library. It has a `load_document` tool that accepts any URL, and prompt instructions restricting it. You need a guarantee. What is it?

- A) A hook intercepting `load_document` calls that blocks any URL outside the licensed domains.
- B) A nightly job auditing which URLs were loaded.
- C) A stronger system prompt listing approved domains.
- D) Renaming the tool `load_licensed_document` as a cue.

**Question 23.** Your coordinator prompt dictates exact search strings for each subagent to run. Topics that don't match the anticipated phrasing return poor results, and subagents never adapt. What is the corrected delegation style?

- A) Longer lists of predefined search strings covering more phrasings.
- B) Delegating research goals and quality criteria, leaving search formulation to the specialist.
- C) A search-string-generation subagent feeding the search agent.
- D) Letting subagents ignore instructions when results look thin.

**Question 24.** `process_source` takes `mode: "summarize" | "extract" | "verify"` and agents keep calling it with the wrong mode for the situation. What is the recommended redesign?

- A) Better documentation of the three modes in the description.
- B) A default mode so wrong calls do something reasonable.
- C) A wrapper that infers the mode from the arguments.
- D) Split it into three purpose-specific tools, each with a clear description and contract.

**Question 25.** Your toolset includes `search_news` ("Searches for news") and `search_web` ("Searches the web") — and agents use them interchangeably, though one hits a curated news API with date filtering and the other a general engine. What is the first fix?

- A) Drop `search_web` since news is the primary use case.
- B) Route by keyword: queries containing "news" go to `search_news`.
- C) Rewrite both descriptions: what each source is, which parameters matter, and when to prefer each.
- D) Merge them into `search_all` with a source parameter.

**Question 26.** A rate-limited search tool returns a normal successful response whose content is the string "quota exceeded, try later." Agents keep summarizing this string into research notes. What is the correct tool behavior?

- A) Signal the failure via the MCP `isError` flag with structured content (category, retryability).
- B) Change the string to something less sentence-like so it won't be quoted.
- C) Return an empty result set when the quota is hit.
- D) Have the agent's prompt list known error strings to ignore.

**Question 27.** Analysts curate 40 high-quality datasets your agents should prefer. Currently agents discover them by trial-and-error searching, often missing them entirely. How do you give agents standing visibility of the curated collection?

- A) List the datasets in every subagent's system prompt.
- B) Boost the datasets' ranking inside the search tool.
- C) Add a `list_curated` tool agents are instructed to call first.
- D) Expose the curated collection as MCP resources — a catalog visible without exploratory calls.

**Question 28.** The analysis agent's generic `fetch_page` tool keeps pulling low-quality content mills into evidence. You maintain an allowlist of credible sources. What is the strongest fix?

- A) Add the allowlist to the agent's system prompt.
- B) Replace `fetch_page` with a constrained `load_source` tool that validates requests against the allowlist.
- C) Post-filter evidence against the allowlist during synthesis.
- D) Penalize content-mill domains in the search ranking.

**Question 29.** A report describes "conflicting GDP growth figures" — 2.1% versus 3.4% — but the sources measured different years. The subagent outputs contained the numbers without dates. What is the systemic fix?

- A) Have synthesis discard any figure whose date it can't infer.
- B) Prefer the higher figure, since growth data gets revised upward.
- C) Require publication and data-collection dates in subagents' structured outputs.
- D) Report all numeric conflicts to a human before publishing.

**Question 30.** During research on a paywalled industry, several key sources were inaccessible. The coordinator knows which topic areas are affected. What should the final deliverable contain?

- A) Coverage annotations distinguishing well-supported findings from gap areas caused by inaccessible sources.
- B) Only the well-covered areas, with gaps omitted for a cleaner read.
- C) A general disclaimer that no research is exhaustive.
- D) A methodology appendix listing every source that was consulted.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** Your agent calls Grep, your harness executes it and appends the `tool_result` — and then nothing happens; the agent never produces its answer. The harness logs show no further API call was made. What is missing?

- A) A `tool_choice` setting on the follow-up request.
- B) The continuation request — after appending tool results, the conversation must be sent back to the model.
- C) The Grep result was too large and must be truncated.
- D) A `continue: true` flag on the tool result block.

**Question 32.** An engineer spent Friday building context in a named session about the notification service. Monday, with no code changes over the weekend, she wants to continue. What is the right move, and why?

- A) Start fresh — sessions should not span multiple days.
- B) `fork_session` so Friday's session stays pristine.
- C) `--resume` the named session — the prior context is still valid.
- D) Start fresh but paste in Friday's final message.

**Question 33.** From one shared analysis of your build system, you want to develop two upgrade strategies — incremental adoption versus a clean cutover — without either exploration influencing the other. Which mechanism?

- A) `fork_session` — two independent branches from the shared analysis baseline, one strategy each.
- B) One session exploring both strategies in alternating messages.
- C) Two fresh sessions, each re-analyzing the build system first.
- D) `--resume` the analysis session twice concurrently.

**Question 34.** "Make our CI builds faster" — an open-ended task with unknown bottlenecks. How should the agent decompose it?

- A) Apply the top ten generic build-speed tricks in order.
- B) Parallelize everything first, since parallelism usually dominates.
- C) Ask the team which step feels slowest and optimize that.
- D) Measure where time goes, identify the biggest bottlenecks, then build a prioritized plan that adapts as findings change.

**Question 35.** Generating a README for each of 40 services follows identical stages: read the service manifest → summarize endpoints → document env vars → assemble the file. What decomposition pattern fits?

- A) Dynamic decomposition per service, letting the agent restructure as it sees fit.
- B) A fixed prompt chain — the same focused stages in sequence for every service.
- C) A single prompt asking for all 40 READMEs at once.
- D) An interview with each service's owner before any generation.

**Question 36.** Your agent runs tests across many repos; some produce JUnit XML, others plaintext summaries, others JSON. The agent frequently misreads pass/fail status in formats it saw less often. What is the reliable fix?

- A) A prompt appendix describing each repo's output format.
- B) Standardizing every repo on one test reporter first.
- C) A `PostToolUse` hook normalizing all test outputs into one canonical result structure.
- D) Having the agent re-run ambiguous tests for a second opinion.

**Question 37.** You configure a new coordinator for the productivity pipeline with `allowedTools: ["Read", "Grep", "Bash"]` and three well-described subagents. In testing it never delegates — it attempts every investigation itself, slowly. What is wrong?

- A) The subagent descriptions are too similar for the coordinator to distinguish.
- B) `"Task"` is missing from the coordinator's allowedTools — the tool that spawns subagents.
- C) The coordinator's system prompt must list the subagents by name before it can call them.
- D) Subagents must be started as separate processes before the coordinator can reach them.

**Question 38.** Your coordinator delegates test-writing to whichever subagent seems right, but its choices look random. The subagent definitions read: "Agent A — helps with code," "Agent B — helps with quality." What is the fix?

- A) Add few-shot delegation examples to the coordinator prompt.
- B) Replace the coordinator's model with a larger one.
- C) Hardcode a task-type-to-agent routing table.
- D) Rewrite the AgentDefinition descriptions with each subagent's specialization, tools, and selection criteria.

**Question 39.** You need every `TODO` and `FIXME` comment across the codebase, with file locations. Which tool does this directly?

- A) Glob with the pattern `**/TODO*`.
- B) Read on each file, collecting matches manually.
- C) Grep — pattern search across file contents is exactly its job.
- D) An MCP code-index server, since built-ins can't search comments.

**Question 40.** The agent must inventory every Dockerfile in the monorepo — `Dockerfile`, `Dockerfile.dev`, `api.Dockerfile` — wherever they live. Which tool call?

- A) Glob with patterns matching the naming variants (`**/Dockerfile*`, `**/*.Dockerfile`).
- B) Grep for `FROM ` across all files and collect the filenames.
- C) Read the docker-compose files and follow references.
- D) Bash `docker images` to enumerate what's built.

**Question 41.** Asked how payment processing works in an unfamiliar codebase, which exploration sequence reflects the recommended practice?

- A) Read every file in `src/payments/` end to end, then answer.
- B) Answer from the architecture diagram in the wiki, verifying nothing.
- C) Glob for `*payment*` and read only exact-name matches.
- D) Grep for entry points (route handlers, processor SDK calls), Read the matches, and follow imports to trace the flow.

**Question 42.** `formatCurrency` is defined in `src/utils/money.ts` but consumed via two barrel files and one aliased re-export (`export { formatCurrency as fmtMoney }`). You need every real call site. Using Claude Code's built-in tools, what is the correct strategy?

- A) Grep for `utils/money` and read the matching importers.
- B) First enumerate all names the function is exported under (including `fmtMoney`), then Grep for each name.
- C) Rely on IDE rename-refactor tooling to enumerate the references.
- D) Grep for `formatCurrency` only — aliases are rare enough to ignore.

**Question 43.** The team's internal-API MCP server needs a per-developer token. You want zero-setup onboarding via the repo without leaking credentials. Which configuration?

- A) Project `.mcp.json` committed with the token referenced as `${INTERNAL_API_TOKEN}`.
- B) Token embedded in `.mcp.json`, with the repo private as the safeguard.
- C) Each developer maintains their own `~/.claude.json` entry from a wiki recipe.
- D) A bootstrap script that writes `.mcp.json` locally on first run.

**Question 44.** Your `schema-inspector` MCP tool answers database-structure questions precisely, but the agent keeps Grep-ing through migration files instead, producing stale answers. The tool's description: "Inspects schemas." What is the recommended fix?

- A) Delete the migrations directory from the agent's view.
- B) Add a system prompt rule: never Grep in `migrations/`.
- C) Expand the description: live table structures, columns, indexes, relationships — preferred over migration files for current-schema questions.
- D) Register the schema-inspector as the default first tool via tool ordering.

**Question 45.** Before designing a plugin API, the agent should compare three candidate integration points, each requiring reading several large modules. The comparison itself is the input to your main design session. How do you structure this?

- A) Read all the modules in the design session and accept the context cost.
- B) Design first, then check the integration points afterwards.
- C) Split the design across three sessions, one per candidate.
- D) Use the Explore subagent for the comparison, receiving only the summary in the design session.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your invoice extractor prompts for "a JSON response" and parses the text. Failures cluster around markdown fences, apologetic preambles ("Here is the extracted data:"), and occasional mid-output drift where fields wander from the required structure. What eliminates the failure class?

- A) A response prefix trick — pre-filling the assistant turn with `{`.
- B) Tool use — an extraction tool whose input schema is the invoice structure, read from the `tool_use` block.
- C) A prompt rule: "no prose, no fences, JSON only."
- D) A tolerant parser that strips fences and leading prose.

**Question 47.** Receipts often genuinely lack a due date, but `due_date` is required in your schema — and audits found the model quietly inserting a date 30 days after the purchase date. What is the correct fix?

- A) Keep it required but add "never invent dates" to the prompt.
- B) Post-validate that due dates appear verbatim in the source text.
- C) Default the field server-side to 30 days, making the model's behavior official.
- D) Make `due_date` optional/nullable and instruct the model to return null when the document has none.

**Question 48.** Your `payment_method` enum covers `["card", "cash", "bank_transfer"]`. Documents now mention regional wallets, crypto, and buy-now-pay-later services — all being forced into `"card"`. How should the schema evolve?

- A) Add `"other"` to the enum with a companion detail field capturing the actual method.
- B) Add the ten most common new methods to the enum each quarter.
- C) Make the field free text and classify downstream.
- D) Reject documents with unrecognized payment methods.

**Question 49.** A shared intake pipeline receives invoices, contracts, and HR forms mixed together, each with its own extraction tool defined. You need guaranteed structured output on every document without pre-classifying. Which setting?

- A) `tool_choice` forced to the invoice tool, the most common type.
- B) `tool_choice: "auto"` plus a prompt instruction to always extract.
- C) `tool_choice: "any"` — a tool call is guaranteed and the model picks the matching schema.
- D) Three pipeline lanes with a rules-based classifier in front.

**Question 50.** Contracts occasionally arrive with a stated term whose end date precedes its start date (drafting or OCR errors). Downstream date math silently produces negative durations. What extraction design surfaces the problem?

- A) Swap the dates when end precedes start, since that's obviously the intent.
- B) Extract both dates as stated and set a `conflict_detected` boolean when the ordering is impossible.
- C) Reject any contract whose dates are out of order.
- D) Extract only the start date, deriving the end from the stated term length.

**Question 51.** `signatory_date` keeps failing extraction on a batch of scanned agreements. Sampling shows the signature page simply wasn't scanned — the date isn't in the input. The retry system has been resubmitting these documents for days. What is the correct assessment?

- A) These retries can never succeed — the date is absent from the input; stop retrying and route to rescanning.
- B) Increase retries with prompt variations until the model finds the dates.
- C) The retries would work with a larger context window.
- D) The field should be removed from the schema.

**Question 52.** You added few-shot examples covering three vendors' invoice layouts. Extraction then also improved markedly on a fourth vendor whose layout none of the examples showed. What explains this?

- A) The fourth vendor's layout must coincidentally match one of the three.
- B) The examples increased the prompt length, which always improves accuracy.
- C) A model update shipped at the same time; the examples were irrelevant.
- D) Few-shot examples teach the underlying judgment, which the model generalizes to novel layouts.

**Question 53.** Financial filings present the same facts sometimes in tables, sometimes in narrative paragraphs, sometimes in footnotes. Your extractor handles tables well and misses the rest. What is the recommended fix?

- A) Preprocess filings to convert all narrative into tables.
- B) Run three extractors, one per presentation style, and merge.
- C) Add few-shot examples demonstrating extraction from tabular, narrative, and footnote presentations.
- D) Restrict extraction to the tables and flag the rest for humans.

**Question 54.** Two workloads: (1) re-extracting your ten-year document archive with an improved schema, results needed "sometime this quarter"; (2) extracting data from documents customers upload during a live onboarding flow. Assign the APIs.

- A) Synchronous for both — simpler to operate.
- B) Batch API for the archive; synchronous API for the onboarding flow a customer is waiting on.
- C) Batch for the onboarding flow since volume is high; synchronous for the archive.
- D) Batch for both — the discount is too large to pass up.

**Question 55.** Your contract guarantees extraction results within 36 hours of document receipt. Batch processing takes up to 24 hours. Documents arrive continuously. Which accumulation window keeps the guarantee?

- A) 8 hours — worst case 8 + 24 = 32 hours, within the guarantee.
- B) 24 hours — one daily batch is operationally cleanest.
- C) 16 hours, since batches usually complete in far less than 24.
- D) 48 hours with an expedite lane for old documents.

**Question 56.** Legal has approved extracting 10,000 archived medical consent forms with a new prompt. The batch budget is fixed. What do you do before submitting the full batch?

- A) Submit the full batch immediately; failures can be resubmitted within budget.
- B) Submit the batch at half temperature to be safe.
- C) Split into two 5,000-form batches and correct between them.
- D) Refine and verify the prompt on a representative sample via the synchronous API first.

**Question 57.** Your extraction step ends with "double-check your extraction against the document" — and reports itself accurate. Auditors keep finding wrong values the self-check approved. What is the structural lesson?

- A) The self-check needs a rubric listing common error types.
- B) The self-check should run twice, with disagreements escalated.
- C) Verification should run as an independent instance, comparing output to source without the extractor's context.
- D) Self-checks work if you also request a confidence score.

**Question 58.** Your dashboard proudly shows 96% extraction accuracy. An operations manager mentions that handwritten intake forms "seem to always be wrong." You segment the data: typed forms 99%, handwritten 61%. What is the lesson?

- A) Handwritten forms should be excluded from the accuracy metric.
- B) Aggregate metrics mask segment failures — validate accuracy by document type and field before it justifies decisions.
- C) The dashboard should show median accuracy instead of mean.
- D) 96% is accurate as an overall number, so no process change is needed.

**Question 59.** After automating high-confidence extractions, you need an ongoing mechanism to catch error patterns the confidence model doesn't know about yet. What is it?

- A) Quarterly re-validation against the original benchmark set.
- B) Alerting when confidence scores drift statistically.
- C) Stratified random sampling of high-confidence extractions for continuous human review.
- D) A user-facing "report an error" button on downstream systems.

**Question 60.** The model emits per-field confidence scores, and you plan to auto-accept above a threshold. A colleague proposes 0.9 "because it's high." What is the defensible way to choose?

- A) Calibrate against a labeled validation set: measure accuracy at each score level and set thresholds where it meets the requirement.
- B) Adopt 0.9 but review the first month's auto-accepts.
- C) Pick 0.95, splitting the difference between the proposal and maximum caution.
- D) Average the last quarter's scores and use that as the threshold.

---
# Answer Key — Practice Exam 10

**Quick key:** 1-C, 2-A, 3-D, 4-B, 5-A, 6-D, 7-C, 8-B, 9-D, 10-A, 11-B, 12-C, 13-D, 14-A, 15-B, 16-C, 17-A, 18-D, 19-B, 20-D, 21-C, 22-A, 23-B, 24-D, 25-C, 26-A, 27-D, 28-B, 29-C, 30-A, 31-B, 32-C, 33-A, 34-D, 35-B, 36-C, 37-B, 38-D, 39-C, 40-A, 41-D, 42-B, 43-A, 44-C, 45-D, 46-B, 47-D, 48-A, 49-C, 50-B, 51-A, 52-D, 53-C, 54-B, 55-A, 56-D, 57-C, 58-B, 59-C, 60-A

---

**1. C** — Same repo, different behavior across machines points at configuration loading, and `/memory` shows exactly which memory files each session loaded — diagnose before changing anything. The likely culprit is user-level configuration present on one machine only. A, B, and D change things before establishing what differs.

**2. A** — `@import` lets each package's CLAUDE.md include only the standards files relevant to it — one copy of each standard, selectively composed. B loads everything everywhere. C duplicates and drifts. D loads all four and hopes the model scopes them correctly.

**3. D** — The recommended structure for a contested monolith: topic-specific files under `.claude/rules/`, each owned by the team that owns the topic — smaller diffs, fewer conflicts, clearer ownership. A freezes the pain in place. B removes the content from Claude's view. C generates a monolith instead of splitting it.

**4. B** — The dividing line: universal always-applicable content in CLAUDE.md; occasional task-specific workflows as skills loaded on invocation. A pays 300 lines of seeding logic in every session. C makes universal conventions opt-in. D is backwards on both.

**5. A** — Exploratory content that shouldn't persist is what `context: fork` isolates: the sketches live in the fork, and only the chosen direction returns. B narrows scope without isolating the residue. C affects file writes, not conversation context. D isn't the mechanism for this.

**6. D** — `allowed-tools` scoped to the skill's actual needs — Read, Edit, and Bash limited to `git log` — keeps the changelog function working while making `git tag` and pushes structurally unavailable. A is the advisory approach that already failed. B reviews after the fact. C catches only the push, not the local mutation, and depends on server configuration.

**7. C** — `argument-hint` prompts for the required parameter when the skill is invoked bare — fixing the invocation gap that causes the fabrication. A isolates the bad output instead of preventing it. B handles the failure politely rather than collecting the input. D misuses tool permissions as input validation.

**8. B** — Files identified by naming convention and spread across directories are the glob-rule case: `paths: ["**/*.e2e.ts"]` loads the conventions exactly when those files are edited. A covers only one location of many. C loads always and scopes never. D depends on someone remembering.

**9. D** — Multiple viable architectures with cross-service constraints is plan mode's core criterion: explore, compare, and commit to a design before code. A ships the first idea and discovers constraints by failure. B triples the work to avoid a decision. C optimizes for build speed, not fit — the fastest prototype says little about the approach that constrains several services best.

**10. A** — Single function, known reproduction, clear expected behavior: direct execution. Planning (B), repo-wide exploration (C), and session forking (D) add process where there is no design uncertainty.

**11. B** — Regressions on previously working cases mean nothing is pinning existing behavior: write the test suite first (all formats, edge cases), then iterate on failing tests. The suite converts whack-a-mole into convergence. A relies on enumeration without enforcement. C abandons instead of stabilizing. D orders the moles without stopping the whacking.

**12. C** — `/compact` is the mid-session relief valve: summarize the conversation, reduce usage, preserve key information, keep working. A discards the decisions unless you can reconstruct them perfectly. B conserves output, not context. D takes the work out of the tool entirely.

**13. D** — Delegate the verbose questions to subagents and let summaries return — exploration happens in their contexts while the main session keeps its budget for design. A spends the main context first and compresses after. B designs on assumptions. C — `/clear` between questions destroys the accumulated understanding the design needs.

**14. A** — Output fields the agent never uses should be trimmed before entering context; a 2,000-line AST dump attached to every lint call is the textbook disproportionate tool result. B batches the bloat. C — the agent can't "skim" what's already in context. D relocates the waste.

**15. B** — Long-session context degradation is countered by a scratchpad: findings recorded as confirmed, consulted for later answers — ground truth that doesn't decay. A caps the work to fit the failure mode. C doubles cost to detect the problem rather than prevent it. D re-spends context constantly, accelerating the degradation.

**16. C** — Coordinators should match invocation to query complexity: simple factual queries get a single search or a direct answer; the full pipeline is for real research. A helps only repeats. B makes every unnecessary stage cheaper instead of skipping it. D changes who runs the unnecessary pipeline, not whether it runs.

**17. A** — A bare `range(8)` makes an arbitrary cap the only termination — hence mid-topic truncation. Loop on `stop_reason`, with any bound kept strictly as an emergency backstop. B tunes the wrong mechanism. C adds a "looks complete" heuristic — a second anti-pattern. D makes users configure a bug.

**18. D** — Subagents use only what their prompts contain: the mappings existed upstream but never reached the report agent, so it improvised. Pass the claim-source mappings explicitly with the synthesis. A asks for restraint while withholding the data. B invites fresh, unvetted sourcing. C corrects fabrications after generation instead of preventing them.

**19. B** — Independent analyses parallelize via multiple Task calls in one coordinator response — five subagents at once, latency near single-region time. A serializes inside one context. C changes freshness semantics to dodge an orchestration fix. D trades quality for speed unnecessarily.

**20. D** — The lost properties — failure localization, non-vanishing partial results — are exactly what hub-and-spoke routing through the coordinator provides: observability, consistent error handling, controlled information flow. A rebuilds those properties as infrastructure around a broken topology. B patches one symptom. C mistakes the cause of the speedup for proof the coordinator was waste.

**21. C** — Completeness requires an evaluation loop: the coordinator checks synthesis against required coverage, re-delegates targeted queries for gaps, and re-invokes synthesis. A instructs synthesis to include data it may not have. B formats the gap nicely. D hopes volume delivers pricing incidentally.

**22. A** — A guarantee means interception: a hook validating every `load_document` URL against the licensed domains, blocking and redirecting anything else. B detects violations after the licensing breach. C remains probabilistic. D is a naming hint, not a control.

**23. B** — Delegation should specify goals and quality criteria, leaving method to the specialist — dictated search strings are procedural micromanagement that breaks on unanticipated topics. A writes more of the brittle thing. C adds an agent to generate the brittle thing. D makes adaptation an act of disobedience.

**24. D** — Mode-switched generic tools invite wrong-mode calls; split into three purpose-specific tools with clear contracts so selection happens at the tool level, where descriptions can differentiate. A documents the confusion. B substitutes silent wrong behavior. C hides the decision in inference.

**25. C** — The tools differ meaningfully (curated news API, date filtering) but their descriptions don't say so — and descriptions are what selection runs on. Rewrite both to state source, parameters, and when to prefer each. A removes real capability. B is keyword routing. D relocates the choice into a parameter with the same documentation problem.

**26. A** — Failures must be signaled through the MCP `isError` flag with structured content, or they're indistinguishable from data — hence quota messages becoming "findings." B makes the string less quotable, not machine-distinguishable. C disguises failure as a valid empty result. D hardcodes error strings into prompts.

**27. D** — Standing visibility of curated content is what MCP resources provide: a catalog agents see without exploratory calls. A duplicates the catalog into every prompt and drifts. B secretly reweights search instead of exposing the collection. C reinvents resources as a tool call plus an instruction.

**28. B** — Replace the generic tool with a constrained alternative: `load_source` validates against the allowlist, making credibility a structural boundary. A is behavioral. C filters evidence after it has shaped analysis. D lowers rankings but the tool still fetches anything.

**29. C** — False conflicts between figures from different periods are prevented by requiring publication/collection dates in structured outputs — temporal interpretation needs temporal metadata. A discards data for missing what upstream should provide. B is an invented heuristic. D escalates a class of error you can eliminate systematically.

**30. A** — Deliverables must distinguish well-supported findings from gap areas caused by inaccessible sources — coverage annotations. B hides the thinness. C disclaims generally what should be marked specifically. D lists what was read without revealing what couldn't be — the reader still can't see where evidence is thin.

**31. B** — The loop is send → execute → append → **send again**: after appending tool results, the updated conversation must go back to the model. Nothing happens because the continuation request was never made. A, C, and D decorate a request that isn't being sent.

**32. C** — Unchanged code and valid prior context is exactly what `--resume` with a named session is for: continuing a named investigation across work sessions. A discards a day of context on principle. B forks with no divergence to explore. D recovers one message out of a day's understanding.

**33. A** — Independent development of two strategies from one shared baseline is `fork_session`'s purpose: two branches, no cross-contamination, no re-analysis. B lets each exploration bias the other. C re-pays for the analysis. D — resuming twice concurrently isn't the branching mechanism; forking is.

**34. D** — Open-ended optimization decomposes as: measure and map, identify highest-impact bottlenecks, build a prioritized plan that adapts as findings change. A applies generic fixes to an unmeasured system. B guesses the dominant factor. C substitutes anecdote for measurement.

**35. B** — Forty services through identical, predictable stages: a fixed prompt chain, the same focused passes per service. A adds adaptive machinery where nothing varies. C is one unfocused mega-task — attention dilution across 40 services. D gates mechanical work on interviews it doesn't need.

**36. C** — Heterogeneous formats from many sources are normalized deterministically in a `PostToolUse` hook — one canonical result structure before the model reasons. A asks the model to be the parser, probabilistically, every time. B is a multi-team migration to avoid a hook. D re-runs tests to compensate for misreading their output.

**37. B** — The Task tool is the spawning mechanism; a coordinator whose `allowedTools` lacks `"Task"` cannot delegate no matter how good the subagent definitions are, so it does everything itself. A contradicts the stem (the descriptions are good). C and D invent requirements — subagents are spawned via Task, not pre-registered in prompts or run as separate processes.

**38. D** — Delegation runs on AgentDefinition descriptions, and "helps with code/quality" gives the coordinator nothing to distinguish. Rewrite the descriptions with specialization, tools, and selection criteria. A trains around missing information. B throws capability at an information gap. C hardcodes what descriptions express naturally.

**39. C** — Finding strings in file contents across a codebase is Grep. A matches filenames, not comments. B is Grep by hand at scale. D — built-ins search content fine; that's the point of Grep.

**40. A** — Inventorying files by naming variants is Glob: `**/Dockerfile*` and `**/*.Dockerfile`. B finds `FROM` in any file, including docs and vendored code. C finds only referenced Dockerfiles. D lists built images, not files in the repo.

**41. D** — Recommended exploration is incremental: Grep for entry points, Read the matches, follow imports to trace the flow. A reads everything for one question. B verifies nothing. C assumes filenames encode the concept — payment logic often lives elsewhere.

**42. B** — Aliased re-exports (`fmtMoney`) mean the function is called by other names: enumerate all exported names first, then Grep for each. A finds direct-path importers only. C reaches outside the built-in toolset the task specifies — and LSP coverage of dynamic references varies. D explicitly ignores the alias that exists.

**43. A** — Project `.mcp.json` with `${INTERNAL_API_TOKEN}` gives zero-setup, version-controlled configuration with per-developer credentials resolved from the environment — no secret in the repo. B commits a secret. C abandons zero-setup. D generates what expansion provides natively.

**44. C** — The agent picks the tool it understands; "Inspects schemas" gives no case against Grep-ing familiar migration files. Enhance the description: live structures, columns, indexes, relationships, preferred for current-schema questions. A and B block or ban the fallback rather than making the better tool legible. D — tool ordering isn't a selection mechanism; descriptions are.

**45. D** — Verbose comparative reading that feeds a design decision is the Explore subagent's case: module reading stays isolated, the summary lands in the design session. A spends the design context on raw input. B designs before the input exists. C fragments one comparison across three contexts.

**46. B** — Tool use eliminates the failure class: the extraction tool's input schema guarantees structure — no fences, no preambles, and no mid-output drift, because the schema is enforced. A (prefill) suppresses preambles and opening fences but guarantees nothing about the rest of the output — the drift failures survive. C is an instruction, already being violated. D is an arms race with formatting variety.

**47. D** — A required field the source may not contain pressures the model to fabricate; make `due_date` nullable and instruct null when absent. A keeps the pressure and adds a plea. B catches some fabrications after the fact (and fails on reformatted dates). C institutionalizes the fabrication.

**48. A** — The extensible-category pattern: `"other"` plus a detail field capturing the actual method — novel categories are represented faithfully, and the enum stays machine-readable. B chases reality quarterly and always trails it. C pushes classification downstream, unsolved. D rejects valid business documents.

**49. C** — Multiple extraction schemas, unknown document type, structured output required: `tool_choice: "any"` — a tool call is guaranteed, and the model selects the schema fitting the document. A forces the wrong schema onto two of three types. B permits prose. D builds a router to replicate what "any" does.

**50. B** — Impossible source data is neither passed through silently nor silently corrected: extract as stated and flag with `conflict_detected` for review. A "fixes" data it cannot verify — the error might be in either field. C stalls legitimate documents over a flag-able condition. D derives from data already suspect.

**51. A** — The date isn't in the input, so no retry can extract it — days of resubmission bought nothing. Detect information-absent failures, stop retrying, and route to rescanning or accept a documented null. B and C retry harder at reading an unscanned page. D deletes a real business field because one batch was scanned badly.

**52. D** — Few-shot examples teach transferable judgment — how to locate and map fields across layout variation — which generalizes to unseen structures; that's why they beat exhaustive per-layout rules. A is possible but explains nothing generalizable and contradicts "markedly improved." B — prompt length isn't a quality mechanism. C is an unfalsifiable dodge.

**53. C** — Structural variety (tables, narrative, footnotes) is the few-shot case: demonstrate correct extraction from each presentation and the model handles the spread. A presumes a reliable narrative-to-table converter — the original problem restated. B triples the pipeline. D shrinks automation to the easy subset.

**54. B** — The archive is the Batch API's ideal customer: enormous, latency-tolerant, half price. Onboarding has a customer waiting — synchronous. A forfeits major savings. C parks live customers behind a no-SLA queue. D is backwards on one of the two.

**55. A** — The guarantee must hold in the worst case: 8-hour accumulation + 24-hour processing = 32 ≤ 36 with margin. B gives 48 worst case. C's 16 + 24 = 40 breaches the SLA, and "usually faster" isn't a guarantee. D starts beyond the SLA and patches with an expedite lane.

**56. D** — With a fixed budget, first-pass success is everything: refine the prompt on a representative sample synchronously, verify, then submit the batch. A spends the budget discovering flaws at full scale. B tweaks a parameter instead of validating the prompt. C still burns half the budget on the unvalidated version.

**57. C** — A model verifying its own extraction retains the reasoning that produced the errors — self-checks approve their own mistakes. Verification must be an independent instance comparing output to source without the extractor's context. A gives the biased checker a rubric. B repeats the biased check. D scores it.

**58. B** — 96% aggregate coexisting with 61% on handwritten forms is exactly how aggregate metrics mask segment failures: validate by document type and field before the number justifies anything, and remediate the failing segment. A hides the problem from the metric. C changes the statistic, not the blindness. D accepts a segment that's wrong 4 times in 10.

**59. C** — Novel error patterns in the automated stream are caught by stratified random sampling of high-confidence extractions with ongoing human review — measuring true error rates where no one otherwise looks. A can't contain patterns that didn't exist at benchmark time. B watches the scores, not the truth. D makes customers the QA layer.

**60. A** — Thresholds come from calibration: measure actual accuracy at each confidence level against labeled data, and set the cutoff (per field type if performance differs) where accuracy meets requirements. B and C are round numbers with different amounts of caution — neither is a measurement. D averages scores into a threshold with no connection to accuracy.

---

*End of Practice Exam 10.*
