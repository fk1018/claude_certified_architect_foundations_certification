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

- A) Compare the Claude Code CLI version on each machine and upgrade whichever is older.
- B) Delete the desktop's local clone and re-clone the repository fresh from the remote.
- C) Run `/memory` on both machines to compare which memory files each session actually loaded, since only one might be picking up a stray global file.
- D) Run `/compact` on the desktop session to clear accumulated context, then continue the same task.

**Question 2.** Your monorepo's `frontend/` packages need the React standards file and the accessibility standards file; `backend/` packages need the API standards and database standards files. All four files live in `standards/`. How do you wire this up without duplication?

- A) In each package's CLAUDE.md, use `@import` to pull in only the standards files that package needs.
- B) Concatenate all four standards files into the root CLAUDE.md so every package inherits the full set automatically.
- C) Copy the relevant standards files into each package directory and keep them updated in sync.
- D) Reference all four standards files from every package's CLAUDE.md and let Claude judge which apply.

**Question 3.** Your CLAUDE.md mixes testing standards, Git workflow, security rules, code style, and deployment steps in one 1,000-line file that three teams edit and constantly conflict over. What is the recommended reorganization?

- A) Freeze the file's structure, require an RFC with cross-team sign-off for every edit, and route all changes through a single release manager.
- B) Move the file to a wiki page and link to it from CLAUDE.md instead of keeping the content inline.
- C) Auto-generate the file nightly from each team's existing documentation sources.
- D) Split it into focused topic files under `.claude/rules/`, each owned by its team.

**Question 4.** Your database-seeding workflow — 300 lines of steps, fixtures, and cleanup logic — is used about once a week. Universal code conventions are used in every session. Where does each belong?

- A) Put both the conventions and the full seeding workflow into CLAUDE.md, since both matter to the team and dropping either risks someone missing it.
- B) Put the conventions in CLAUDE.md, since they're always loaded, and the seeding workflow in a skill under `.claude/skills/`.
- C) Put both the conventions and the seeding workflow into skills to minimize what gets loaded into context.
- D) Put the conventions into a skill and the 300-line seeding workflow into CLAUDE.md.

**Question 5.** Your `/explore-alternatives` skill generates several competing design sketches. After it runs, the main session's context carries all the rejected sketches, and Claude later resurrects abandoned ideas as if they were current. What frontmatter fixes this?

- A) `context: fork` — the exploration runs isolated in its own context, and only the chosen direction returns to resume the main session's work.
- B) `argument-hint`, so the skill prompts for a single design question and stays scoped to it.
- C) `allowed-tools`, restricting the skill so it can't write the sketches out to files.
- D) `paths`, restricting the skill so it only runs against design documents.

**Question 6.** Your `/update-changelog` skill needs only to read the git log and edit `CHANGELOG.md`. An incident review found a run where it also executed `git tag` and pushed the tag. What is the structural fix?

- A) Add a line to the skill's SKILL.md instructing it to never create or push tags.
- B) Add a hook that logs the skill's tool calls to a file for developers to review afterward.
- C) Protect the tag ref server-side, requiring a manual approval workflow before any push of a new tag is accepted by the remote.
- D) Set `allowed-tools` to the minimum the skill needs — Read, Edit, and Bash scoped to `git log` only.

**Question 7.** Your `/fix-issue` skill needs a ticket number to look up the issue before fixing it. Developers regularly invoke it bare and it fabricates an interpretation of "the issue." Which frontmatter option addresses the invocation problem?

- A) `context: fork`, so the fabricated interpretations stay isolated from the main session.
- B) A SKILL.md instruction telling the skill to refuse the run whenever no ticket number is given.
- C) `argument-hint`, prompting the developer for the required ticket number on bare invocation.
- D) `allowed-tools` restricted to read-only tools until a valid ticket number is supplied by the caller, so no fix can be written before the lookup succeeds.

**Question 8.** End-to-end test specs (`*.e2e.ts`) live next to the features they test, in dozens of directories. They must all follow your Playwright conventions. Which mechanism applies the conventions to exactly those files?

- A) Put a CLAUDE.md file in the `tests/` directory and hope engineers editing specs elsewhere still find and read it.
- B) A `.claude/rules/` file with frontmatter `paths: ["**/*.e2e.ts"]`.
- C) Add a section headed "For e2e files only" to the root CLAUDE.md that every session loads regardless.
- D) Add a skill that developers are expected to run manually before writing any e2e test.

**Question 9.** You're adding a caching layer. Three integration approaches are viable — sidecar, library, or gateway-level — each with different infrastructure requirements, and the choice constrains several services. How do you start?

- A) Start direct execution with whichever approach looks simplest, switching to another if it fails partway through.
- B) Implement all three approaches behind a feature flag in production and benchmark them against live traffic.
- C) Prototype whichever of the three is fastest to build, and let that spike decide the architecture.
- D) Enter plan mode: explore the affected services, weigh the three approaches against each other, and settle on one design before writing any code.

**Question 10.** A user reports that phone numbers with spaces fail validation. The regex lives in one function; the failing input and expected behavior are both known. How do you proceed?

- A) Direct execution — a single-function fix with a known reproduction and expected behavior needs no planning phase.
- B) Enter plan mode to consider the validation architecture holistically, mapping every field that might need the same treatment before touching the regex.
- C) Spawn an Explore subagent to find every other validation pattern in the codebase first.
- D) Use `fork_session` to develop and compare two candidate regexes before picking one.

**Question 11.** Claude's fixes to your date-parsing utility keep regressing other formats: each fix breaks a previously working case. What iteration structure stops the whack-a-mole?

- A) Ask Claude to enumerate every date format the utility should support before attempting each fix.
- B) Write a test suite first covering all known formats and edge cases, then iterate by sharing the failing tests.
- C) Freeze the existing utility in place, write a replacement one alongside it from scratch, and cut over once the new one passes every case anyone can recall.
- D) Fix formats in order of how frequently each one appears in production traffic.

**Question 12.** You're deep in a productive session; context is nearly full of file dumps from earlier exploration, and you have an hour of implementation left. You want to preserve key decisions but reclaim space. What do you do?

- A) Start a brand-new session and reconstruct the key decisions from memory, cross-checking against whatever files were already changed.
- B) Ask Claude to respond more tersely for the rest of the session to slow context growth.
- C) Run `/compact` to summarize the conversation, preserving key information while reclaiming space.
- D) Export the transcript to a file and continue the remaining work in a text editor instead.

**Question 13.** Your main session must design a refactor, but first you need answers to three verbose research questions (where is X implemented, who calls Y, how is Z configured). How do you keep the main session's context clean?

- A) Answer all three research questions directly in the main session first, then run `/compact` before starting the design work.
- B) Design the refactor first from assumptions about the answers, verifying them only afterward.
- C) Investigate each question in the main session, running `/clear` between each one to reset.
- D) Spawn a subagent to investigate each question, returning only a distilled summary to the main session, so the raw exploration never touches its context.

**Question 14.** Your lint MCP tool returns the full AST dump (2,000+ lines) with every lint report; the agent only ever uses the rule violations list. Sessions using the linter heavily degrade fast. What is the fix?

- A) Trim the lint tool's output to just the violations list, the only part the agent ever actually reads, before it enters context at all.
- B) Lint entire directories in a single call instead of file-by-file, so the tool runs less often.
- C) Add a hook that logs each dump's line count for monitoring, without changing what enters context.
- D) Move linting to a subagent so the 2,000-line dumps accumulate in its context instead of the main one.

**Question 15.** Hour three of a security audit session: Claude begins asserting things about modules that contradict what it itself reported in hour one. The audit has hours to go. What practice should have been in place from the start (and is worth starting now)?

- A) Cap every audit session at one hour so contradictions don't have time to accumulate.
- B) Keep an audit scratchpad file where findings are recorded as confirmed and consulted for later questions.
- C) Run a second Claude instance auditing the same modules in parallel, reconciling any disagreement before either finding is written up.
- D) Re-read every module in the codebase before asking each new question during the audit.

---

## Scenario B: Multi-Agent Research System (Questions 16–30)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 16.** Analytics show that 30% of user queries are simple definitions or single facts, yet every query traverses search → analysis → synthesis → report. What should the coordinator do differently?

- A) Add a cache in front of the pipeline so repeated questions skip reprocessing.
- B) Shorten each stage's prompt so the full pipeline is cheaper to run per query.
- C) Assess each query's complexity and invoke only what it needs — a single search for a simple fact.
- D) Route simple queries to a smaller, cheaper model that still runs the same four-stage search-analysis-synthesis-report pipeline end to end.

**Question 17.** Reviewing the coordinator wrapper, you find: `for turn in range(8): response = send(...)` with no other exit condition, and users report reports that stop mid-topic. What is the correct redesign?

- A) Loop on `stop_reason` — continue on `"tool_use"`, exit on `"end_turn"` — with any turn cap kept only as a backstop.
- B) Raise the hardcoded range to 20 turns, since telemetry shows 95% of tasks finish comfortably within that window without truncation.
- C) Add a hook that flags the response as "looks complete" and stops the loop early.
- D) Let each user configure their own turn budget per query in a settings panel.

**Question 18.** The report agent produces beautiful reports with invented citations. Investigating, you find its prompt contains the synthesis text but not the claim-source mappings the synthesis agent produced. What is the fix?

- A) Instruct the report agent in its prompt to only cite a source when it's certain of the claim.
- B) Give the report agent its own web search tool so it can look up a plausible source for each claim as it writes.
- C) Add a post-processor that verifies and corrects citations after the report is generated.
- D) Pass the claim-source mappings the synthesis agent already produced explicitly into the report agent's own prompt, alongside the synthesis text.

**Question 19.** Five regional market analyses are needed before a global rollup; each is independent. The coordinator currently runs them one per turn, and latency is five times the single-region time. What fixes the latency?

- A) Merge all five regional analyses into a single subagent prompt covering every region at once.
- B) Emit five Task tool calls in a single coordinator response so the analyses run in parallel.
- C) Precompute all five regions on a nightly schedule so live requests hit a cache instead, accepting that the numbers may be up to a day stale.
- D) Shorten each regional analysis to a short summary so each one finishes faster.

**Question 20.** An engineer wired the search agent to hand results directly to the analysis agent and the analysis agent directly to synthesis, bypassing the coordinator "for speed." Since then, failures are impossible to localize and partial results vanish silently. What does the incident illustrate?

- A) Build out distributed tracing infrastructure so the direct handoffs become traceable after the fact, without changing who talks to whom.
- B) Direct handoffs are fine as an architecture; each agent just needs its own retry logic added.
- C) The speed gain proves the coordinator step was unnecessary overhead in the pipeline all along.
- D) Hub-and-spoke routing exists for exactly these properties: observability, error handling, controlled information flow.

**Question 21.** Competitor-analysis reports keep shipping without pricing data — the synthesis agent works with whatever arrives, and nothing checks completeness. What is the architectural fix?

- A) Add a synthesis prompt instruction telling it to "always include pricing" in every report it writes.
- B) Add a required `pricing` section to the report template, left blank whenever data is missing.
- C) Add a refinement loop: the coordinator checks synthesis output against required coverage and re-delegates targeted queries for any gaps found.
- D) Pull more search results per query so pricing data shows up more often by sheer volume.

**Question 22.** Policy: the document analysis agent may only load documents from your licensed research library. It has a `load_document` tool that accepts any URL, and prompt instructions restricting it. You need a guarantee. What is it?

- A) A hook intercepting `load_document` calls that blocks any URL outside the licensed domains.
- B) A nightly audit job reviewing which URLs were loaded against the licensed domain list, flagging any violation discovered after the fact.
- C) A stronger system prompt explicitly listing the approved licensed-library domains.
- D) Rename the tool `load_licensed_document` as a naming cue toward the intended domains.

**Question 23.** Your coordinator prompt dictates exact search strings for each subagent to run. Topics that don't match the anticipated phrasing return poor results, and subagents never adapt. What is the corrected delegation style?

- A) Add few-shot examples of well-formed search strings to the coordinator prompt, expanding the list as new topics fail.
- B) Delegate research goals and quality criteria through the subagent's system prompt, leaving search formulation to the specialist.
- C) Add a search-string-generation subagent that feeds phrasings to the search agent.
- D) Let subagents ignore the coordinator's instructions whenever the results look thin.

**Question 24.** `process_source` takes `mode: "summarize" | "extract" | "verify"` and agents keep calling it with the wrong mode for the situation. What is the recommended redesign?

- A) Document the three modes more thoroughly in the tool's description field.
- B) Give the tool a default mode so a call missing the mode argument still does something reasonable instead of erroring out.
- C) Add a wrapper that infers the intended mode from the other arguments passed in.
- D) Split it into three purpose-specific tools, each with a clear description and contract.

**Question 25.** Your toolset includes `search_news` ("Searches for news") and `search_web` ("Searches the web") — and agents use them interchangeably, though one hits a curated news API with date filtering and the other a general engine. What is the first fix?

- A) Drop `search_web` entirely, since news queries are the primary use case.
- B) Route by keyword: any query containing the word "news" goes to `search_news`.
- C) Rewrite both descriptions to state what each source is, which parameters matter, and when to prefer each.
- D) Merge them into one `search_all` tool with a source parameter to choose between them, keeping the same two underlying descriptions unchanged.

**Question 26.** A rate-limited search tool returns a normal successful response whose content is the string "quota exceeded, try later." Agents keep summarizing this string into research notes. What is the correct tool behavior?

- A) Signal the failure via the MCP `isError` flag with structured content describing the category and retryability.
- B) Change the returned string to something less sentence-like and more code-formatted, so it reads less like a plausible summary to quote.
- C) Return an empty result set instead of the quota message when the limit is hit.
- D) Add a hook that deletes the tool result whenever it contains the word "quota," regardless of context.

**Question 27.** Analysts curate 40 high-quality datasets your agents should prefer. Currently agents discover them by trial-and-error searching, often missing them entirely. How do you give agents standing visibility of the curated collection?

- A) List all 40 curated datasets directly in every subagent's system prompt.
- B) Boost the curated datasets' ranking inside the search tool's results.
- C) Add a `list_curated` tool that agents are instructed to call before searching.
- D) Expose the curated collection as MCP resources — a standing catalog agents can see without needing to make any exploratory call first.

**Question 28.** The analysis agent's generic `fetch_page` tool keeps pulling low-quality content mills into evidence. You maintain an allowlist of credible sources. What is the strongest fix?

- A) Add the allowlist of credible sources to the analysis agent's system prompt.
- B) Replace `fetch_page` with a constrained `load_source` tool that validates requests against the allowlist.
- C) Post-filter the evidence against the allowlist during synthesis, discarding anything sourced from an unlisted domain before the report is written.
- D) Penalize known content-mill domains in the search tool's ranking function.

**Question 29.** A report describes "conflicting GDP growth figures" — 2.1% versus 3.4% — but the sources measured different years. The subagent outputs contained the numbers without dates. What is the systemic fix?

- A) Have synthesis discard any growth figure whose date it can't infer from context.
- B) Prefer the higher of the two figures, since growth statistics are typically revised upward as more complete data comes in later.
- C) Require publication and data-collection dates in subagents' structured outputs.
- D) Report every numeric conflict to a human reviewer before the report is published.

**Question 30.** During research on a paywalled industry, several key sources were inaccessible. The coordinator knows which topic areas are affected. What should the final deliverable contain?

- A) Coverage annotations distinguishing well-supported findings from the specific gap areas caused by inaccessible, paywalled sources.
- B) Only the well-covered topic areas, with the paywalled gaps left out for a cleaner read.
- C) A general disclaimer stating that no research report is ever fully exhaustive.
- D) A methodology appendix listing every source that was actually consulted during research.

---

## Scenario C: Developer Productivity with Claude (Questions 31–45)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks, using built-in tools (Read, Write, Bash, Grep, Glob) and MCP servers.

---

**Question 31.** Your agent calls Grep, your harness executes it and appends the `tool_result` — and then nothing happens; the agent never produces its answer. The harness logs show no further API call was made. What is missing?

- A) Add a `tool_choice` setting to the follow-up request so the model is explicitly told which tool to call in response.
- B) Send the continuation request — after appending tool results, the conversation must go back to the model.
- C) The Grep result was too large and needs to be truncated before it's appended.
- D) A `continue: true` flag directly on the tool result content block.

**Question 32.** An engineer spent Friday building context in a named session about the notification service. Monday, with no code changes over the weekend, she wants to continue. What is the right move, and why?

- A) Start a fresh session, since sessions shouldn't be expected to span multiple days.
- B) Use `fork_session` so Friday's original session stays pristine and untouched, in case it's ever needed again as a reference copy.
- C) `--resume` the named session — the prior context is still valid since nothing changed.
- D) Start a fresh session but paste in Friday's final message for context.

**Question 33.** From one shared analysis of your build system, you want to develop two upgrade strategies — incremental adoption versus a clean cutover — without either exploration influencing the other. Which mechanism?

- A) `fork_session` — two independent branches from the shared analysis baseline, one strategy each.
- B) Explore both strategies in one session, alternating messages between them as you go.
- C) Start two fresh sessions, each re-analyzing the build system from scratch first, so neither has to trust the other's earlier conclusions.
- D) `--resume` the analysis session twice concurrently, one per strategy.

**Question 34.** "Make our CI builds faster" — an open-ended task with unknown bottlenecks. How should the agent decompose it?

- A) Apply the ten most common build-speed tricks, in order, regardless of what's slow.
- B) Parallelize every stage of the pipeline first, since parallelism usually dominates other gains.
- C) Ask the team which build step feels slowest, and optimize that one first.
- D) Measure where time actually goes, identify the biggest bottlenecks, and build a prioritized plan that keeps adapting as new findings come in.

**Question 35.** Generating a README for each of 40 services follows identical stages: read the service manifest → summarize endpoints → document env vars → assemble the file. What decomposition pattern fits?

- A) Use dynamic decomposition, letting the agent draft a new structured plan for each service individually based on whatever it notices along the way.
- B) A fixed prompt chain — the same focused stages, in sequence, applied to every service.
- C) Ask for all 40 READMEs in a single prompt covering every service at once.
- D) Interview each service's owner before generating anything for that service.

**Question 36.** Your agent runs tests across many repos; some produce JUnit XML, others plaintext summaries, others JSON. The agent frequently misreads pass/fail status in formats it saw less often. What is the reliable fix?

- A) Add a prompt appendix describing each repo's specific test output format.
- B) Standardize every repo on a single test reporter before running the agent at all, migrating every legacy pipeline to match it first.
- C) Add a `PostToolUse` hook normalizing all test outputs into one canonical result structure.
- D) Have the agent re-run any test whose pass/fail status looks ambiguous, for a second opinion.

**Question 37.** You configure a new coordinator for the productivity pipeline with `allowedTools: ["Read", "Grep", "Bash"]` and three well-described subagents. In testing it never delegates — it attempts every investigation itself, slowly. What is wrong?

- A) The three subagent descriptions are too similar for the coordinator to tell them apart.
- B) `"Task"` is missing from the coordinator's `allowedTools` — the very tool that lets it spawn a subagent in the first place.
- C) The coordinator's system prompt must explicitly list the subagents by name before it can call them.
- D) Subagents must be registered via a startup hook before the coordinator can reach them at all.

**Question 38.** Your coordinator delegates test-writing to whichever subagent seems right, but its choices look random. The subagent definitions read: "Agent A — helps with code," "Agent B — helps with quality." What is the fix?

- A) Add few-shot delegation examples to the coordinator's prompt showing which agent handled which task before.
- B) Replace the coordinator's underlying model with a larger one.
- C) Hardcode a task-type-to-agent routing table outside the coordinator's own reasoning.
- D) Rewrite the AgentDefinition descriptions with each subagent's specialization and selection criteria.

**Question 39.** You need every `TODO` and `FIXME` comment across the codebase, with file locations. Which tool does this directly?

- A) Use Glob with the pattern `**/TODO*` to find matching files.
- B) Read every file individually and collect the matches by hand.
- C) Grep — pattern search across file contents is exactly its job.
- D) Use an MCP code-index server, since built-in tools can't reliably search inside comments spread across a large codebase.

**Question 40.** The agent must inventory every Dockerfile in the monorepo — `Dockerfile`, `Dockerfile.dev`, `api.Dockerfile` — wherever they live. Which tool call?

- A) Use Glob with patterns matching the naming variants: `**/Dockerfile*` and `**/*.Dockerfile`.
- B) Grep for `FROM ` across every file in the repository, normalize the resulting filenames, and collect them into a report.
- C) Read the docker-compose files and follow whatever Dockerfile references they contain.
- D) Run `docker images` in Bash to enumerate whatever images have already been built.

**Question 41.** Asked how payment processing works in an unfamiliar codebase, which exploration sequence reflects the recommended practice?

- A) Read every file in `src/payments/` end to end before answering the question.
- B) Answer directly from the architecture diagram in the team wiki, without validating it against the current code.
- C) Glob for `*payment*` and read only the files whose names are an exact match.
- D) Grep for entry points — route handlers, processor SDK calls — Read the matches, and follow imports to trace the actual flow through the system.

**Question 42.** `formatCurrency` is defined in `src/utils/money.ts` but consumed via two barrel files and one aliased re-export (`export { formatCurrency as fmtMoney }`). You need every real call site. Using Claude Code's built-in tools, what is the correct strategy?

- A) Grep for `utils/money` and read whichever files import from that path.
- B) First enumerate every name the function is exported under, including `fmtMoney`, then Grep for each name.
- C) Rely on IDE rename-refactor tooling to enumerate every reference automatically, trusting it to resolve the barrel files and the alias correctly.
- D) Grep for `formatCurrency` only, since aliased re-exports are rare enough to ignore.

**Question 43.** The team's internal-API MCP server needs a per-developer token. You want zero-setup onboarding via the repo without leaking credentials. Which configuration?

- A) Commit a project `.mcp.json` with the token referenced as `${INTERNAL_API_TOKEN}`.
- B) Embed the token directly in `.mcp.json`, relying on the repo being private as the safeguard.
- C) Have each developer maintain their own `~/.claude.json` entry from a wiki recipe.
- D) Ship a bootstrap script that writes `.mcp.json` locally on each developer's first run, prompting them to paste in their own token interactively.

**Question 44.** Your `schema-inspector` MCP tool answers database-structure questions precisely, but the agent keeps Grep-ing through migration files instead, producing stale answers. The tool's description: "Inspects schemas." What is the recommended fix?

- A) Remove the migrations directory from the agent's visible file tree entirely, so Grep-ing old migration history is no longer even an option during investigation.
- B) Add a system prompt rule instructing the agent never to Grep inside `migrations/`.
- C) Expand the tool's description: live table structures, columns, indexes, and relationships — preferred for current-database questions.
- D) Register the inspector tool as the default first tool the agent must try, via tool ordering.

**Question 45.** Before designing a plugin API, the agent should compare three candidate integration points, each requiring reading several large modules. The comparison itself is the input to your main design session. How do you structure this?

- A) Read all three candidates' modules directly in the design session and accept the context cost.
- B) Design the plugin API first, then check the three integration points afterward.
- C) Split the design work across three separate sessions, one per candidate integration point.
- D) Use an Explore subagent to do the comparison, receiving only a distilled summary of the three options back in the design session.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your invoice extractor prompts for "a JSON response" and parses the text. Failures cluster around markdown fences, apologetic preambles ("Here is the extracted data:"), and occasional mid-output drift where fields wander from the required structure. What eliminates the failure class?

- A) Pre-fill the assistant's turn with an opening `{` so the response is forced to start as JSON.
- B) Use tool use — an extraction tool defined with the invoice fields as its parameters, read from the `tool_use` block.
- C) Add a prompt rule enforcing a structured, prose-free response: "no prose, no markdown fences, JSON only, no preamble."
- D) Use a tolerant parser that strips fences and leading prose before parsing the rest.

**Question 47.** Receipts often genuinely lack a due date, but `due_date` is required in your schema — and audits found the model quietly inserting a date 30 days after the purchase date. What is the correct fix?

- A) Keep `due_date` required, and add a few-shot example of a filled-in date, hoping imitation curbs the fabrication.
- B) Post-validate that any extracted due date appears verbatim somewhere in the source text.
- C) Default the field server-side to 30 days after the purchase date, making the model's behavior official.
- D) Make `due_date` optional or nullable, and instruct the model to explicitly return null whenever the document genuinely has no due date stated anywhere.

**Question 48.** Your `payment_method` enum covers `["card", "cash", "bank_transfer"]`. Documents now mention regional wallets, crypto, and buy-now-pay-later services — all being forced into `"card"`. How should the schema evolve?

- A) Add `"other"` to the enum, with a companion free-text field capturing the actual payment method.
- B) Add the ten most common new payment methods to the enum every quarter, retiring the least-used existing categories to keep the list manageable.
- C) Make the field free text entirely, and classify it into categories downstream instead.
- D) Reject any document that mentions a payment method outside the current enum.

**Question 49.** A shared intake pipeline receives invoices, contracts, and HR forms mixed together, each with its own extraction tool defined. You need guaranteed structured output on every document without pre-classifying. Which setting?

- A) Force `tool_choice` to the invoice tool, since invoices are the most common document type.
- B) Use `tool_choice: "auto"` along with a prompt instruction to always extract structured data.
- C) Use `tool_choice: "any"` — a tool call is guaranteed, and the model picks whichever extraction tool matches the document.
- D) Run three separate pipeline lanes with a rules-based classifier routing documents up front, maintaining its keyword rules as new document variants appear.

**Question 50.** Contracts occasionally arrive with a stated term whose end date precedes its start date (drafting or OCR errors). Downstream date math silently produces negative durations. What extraction design surfaces the problem?

- A) Swap the two dates when the end precedes the start, since that's clearly the intended order.
- B) Extract both dates exactly as stated, and set a `conflict_detected` boolean when the ordering can't be true, so a human resolves which value is wrong.
- C) Reject any contract whose extracted dates are out of order before it reaches downstream systems.
- D) Extract only the start date, deriving the end date from the contract's stated term length instead.

**Question 51.** `signatory_date` keeps failing extraction on a batch of scanned agreements. Sampling shows the signature page simply wasn't scanned — the date isn't in the input. The retry system has been resubmitting these documents for days. What is the correct assessment?

- A) These retries cannot succeed — the date was never captured in the scan; stop retrying and route the batch for rescanning.
- B) Raise the retry count and vary the prompt wording until the model manages to find the missing dates.
- C) These retries would succeed with a larger context window feeding in more of the surrounding scanned pages, giving the model more material to search.
- D) The field should be dropped from the schema entirely, since this batch couldn't produce it.

**Question 52.** You added few-shot examples covering three vendors' invoice layouts. Extraction then also improved markedly on a fourth vendor whose layout none of the examples showed. What explains this?

- A) The fourth vendor's layout must simply happen to resemble one of the three example layouts closely.
- B) The longer prompt produced by adding examples happened to help on its own, since longer prompts generally score better on this kind of task regardless of their content.
- C) A model update shipped at the same time as the examples; the examples themselves were irrelevant.
- D) Few-shot examples teach the underlying judgment involved, which the model generalizes to novel layouts.

**Question 53.** Financial filings present the same facts sometimes in tables, sometimes in narrative paragraphs, sometimes in footnotes. Your extractor handles tables well and misses the rest. What is the recommended fix?

- A) Preprocess every filing to convert its narrative sections into tables before extraction.
- B) Run three separate extractors, one tuned to each presentation style, normalize their outputs to a common shape, and merge the results afterward.
- C) Add few-shot examples demonstrating extraction from tabular, narrative, and footnote presentations, so the model learns the pattern across all three.
- D) Restrict extraction to the tables, and flag narrative and footnote sections for human review.

**Question 54.** Two workloads: (1) re-extracting your ten-year document archive with an improved schema, results needed "sometime this quarter"; (2) extracting data from documents customers upload during a live onboarding flow. Assign the APIs.

- A) Use the synchronous API for both workloads, since operating a single API end to end is simpler than maintaining two separate integration paths.
- B) Batch API for the archive; synchronous API for the onboarding flow a customer is waiting on.
- C) Batch for the onboarding flow since volume is high; synchronous for the archive.
- D) Batch API for both workloads, since the pricing discount is too large to pass up.

**Question 55.** Your contract guarantees extraction results within 36 hours of document receipt. Batch processing takes up to 24 hours. Documents arrive continuously. Which accumulation window keeps the guarantee?

- A) Accumulate for 8 hours — worst case 8 + 24 = 32 hours, within the 36-hour guarantee.
- B) Accumulate for 24 hours — a single daily batch is the operationally cleanest schedule.
- C) Accumulate for 16 hours, since batches usually complete in far less than the stated 24-hour maximum processing window in practice.
- D) Accumulate for 48 hours, adding an expedite lane for documents that are already old.

**Question 56.** Legal has approved extracting 10,000 archived medical consent forms with a new prompt. The batch budget is fixed. What do you do before submitting the full batch?

- A) Submit the full batch immediately, since any failures can be resubmitted within the fixed budget.
- B) Submit the batch at half the usual temperature setting, to be safe with a sensitive dataset.
- C) Split the batch into two runs of 5,000 forms each, correcting the prompt between the two runs based on whatever errors the first half turns up.
- D) Refine and verify the prompt on a representative sample via the synchronous API first.

**Question 57.** Your extraction step ends with "double-check your extraction against the document" — and reports itself accurate. Auditors keep finding wrong values the self-check approved. What is the structural lesson?

- A) Give the self-check a few-shot example of a caught error, alongside a rubric listing common error types to watch for.
- B) Run the self-check twice in the same session, escalating to a human whenever the two passes happen to disagree with each other.
- C) Run verification as an independent instance, comparing output to source without the extractor's own context.
- D) Self-checks work fine as long as you also request a confidence score alongside them.

**Question 58.** Your dashboard proudly shows 96% extraction accuracy. An operations manager mentions that handwritten intake forms "seem to always be wrong." You segment the data: typed forms 99%, handwritten 61%. What is the lesson?

- A) Exclude handwritten forms from the accuracy metric entirely, since they drag down the average.
- B) Aggregate metrics mask segment failures — validate accuracy by document type and field before it justifies any downstream decision.
- C) Have the dashboard show median accuracy instead of the mean across all documents.
- D) 96% is an accurate overall number, so no change to the process is required here.

**Question 59.** After automating high-confidence extractions, you need an ongoing mechanism to catch error patterns the confidence model doesn't know about yet. What is it?

- A) Run a quarterly re-validation of the model against the original benchmark set.
- B) Alert whenever confidence scores drift statistically from their historical baseline.
- C) Stratified random sampling of high-confidence extractions for continuous human review.
- D) Add a user-facing "report an error" button on the downstream systems that consume the data, relying on customers to surface anything the model got wrong.

**Question 60.** The model emits per-field confidence scores, and you plan to auto-accept above a threshold. A colleague proposes 0.9 "because it's high." What is the defensible way to choose?

- A) Calibrate against a labeled validation set: measure accuracy at each score level and set the threshold where it actually meets the requirement.
- B) Adopt 0.9 as proposed, but review the first month of auto-accepted extractions by hand.
- C) Pick 0.95 instead, splitting the difference between the proposal and maximum caution.
- D) Average the last quarter's confidence scores and use that average as the threshold.

---
# Answer Key — Practice Exam 10

**Quick key:** 1-C, 2-A, 3-D, 4-B, 5-A, 6-D, 7-C, 8-B, 9-D, 10-A, 11-B, 12-C, 13-D, 14-A, 15-B, 16-C, 17-A, 18-D, 19-B, 20-D, 21-C, 22-A, 23-B, 24-D, 25-C, 26-A, 27-D, 28-B, 29-C, 30-A, 31-B, 32-C, 33-A, 34-D, 35-B, 36-C, 37-B, 38-D, 39-C, 40-A, 41-D, 42-B, 43-A, 44-C, 45-D, 46-B, 47-D, 48-A, 49-C, 50-B, 51-A, 52-D, 53-C, 54-B, 55-A, 56-D, 57-C, 58-B, 59-C, 60-A

---

**1. C** — Same repo, different behavior across machines points at configuration loading, and `/memory` shows exactly which memory files each session loaded — diagnose before changing anything. The likely culprit is user-level configuration present on one machine only. B rebuilds the environment without learning why it differs. A and D change something before establishing what's different.

**2. A** — `@import` lets each package's CLAUDE.md include only the standards relevant to it — one copy of each file, composed selectively per package. B loads everything into every package regardless of relevance. C duplicates content that will drift out of sync. D loads all four everywhere and hopes Claude scopes them correctly.

**3. D** — The recommended structure for a contested monolith: topic-specific files under `.claude/rules/`, each owned by the team that owns the topic — smaller diffs, fewer conflicts, clearer ownership. A adds process overhead without addressing why teams collide. B removes the content from Claude's direct view. C generates a monolith instead of splitting one.

**4. B** — The dividing line: universal, always-applicable content in CLAUDE.md; occasional task-specific workflows as skills loaded on invocation. A pays the 300-line seeding cost in every session regardless of need. C makes universal conventions opt-in when they should always load. D has both backwards.

**5. A** — Exploratory content that shouldn't persist is what `context: fork` isolates: the sketches live in the fork, and only the chosen direction returns to the main session. B narrows what triggers the skill without isolating leftover context. C affects file writes, not what stays in the conversation. D scopes which files the skill touches, not what it leaves behind.

**6. D** — `allowed-tools` scoped to the skill's actual needs — Read, Edit, and Bash limited to `git log` — makes `git tag` and pushes structurally unavailable, not just discouraged. A is advisory and already failed once. B only logs after the fact instead of preventing anything. C blocks only the push half and depends on remote configuration the skill author doesn't control.

**7. C** — `argument-hint` prompts for the required ticket number the moment the skill is invoked bare, closing the gap that produces fabrication. A isolates the bad output instead of preventing it. B handles the missing input politely rather than collecting it. D repurposes tool permissions as a substitute for input validation.

**8. B** — Files identified by naming convention and spread across directories are the glob-rule case: `paths: ["**/*.e2e.ts"]` loads the conventions exactly when those files are edited, wherever they live. A only covers files that happen to sit in one folder. C loads always, for every session, whether or not e2e files are involved. D depends on someone remembering to run it.

**9. D** — Multiple viable architectures with cross-service constraints is plan mode's core criterion: explore, compare, and commit to a design before code. A commits to the first idea and discovers the constraints by failure. B triples the build cost in production to avoid deciding up front. C optimizes for build speed, which says little about which approach fits several dependent services best.

**10. A** — Single function, known reproduction, clear expected behavior: direct execution. Planning (B), repo-wide exploration (C), and session forking (D) add process where there is no design uncertainty.

**11. B** — Regressions on previously working cases mean nothing is pinning existing behavior: write the test suite first (all formats, edge cases), then iterate on failing tests. The suite converts whack-a-mole into convergence. A relies on enumeration without enforcement. C abandons the utility instead of stabilizing it. D orders the moles without stopping the whacking.

**12. C** — `/compact` is the mid-session relief valve: summarize the conversation, reduce usage, preserve key information, keep working. A discards the decisions unless you can reconstruct them perfectly. B conserves output, not context. D takes the work out of the tool entirely.

**13. D** — Delegate the verbose questions to subagents and let summaries return — exploration happens in their contexts while the main session keeps its budget for design. A spends the main context first and compresses after the damage is done. B designs on assumptions. C — `/clear` between questions destroys the accumulated understanding the design needs.

**14. A** — Output fields the agent never uses should be trimmed before entering context; a 2,000-line AST dump attached to every lint call is the textbook disproportionate tool result. B batches the same bloat into fewer, bigger calls. C only logs the dump's size without changing what the agent actually receives. D relocates the waste rather than removing it.

**15. B** — Long-session context degradation is countered by a scratchpad: findings recorded as confirmed, consulted for later answers — ground truth that doesn't decay. A caps the work to fit the failure mode. C doubles cost to detect the problem rather than prevent it. D re-spends context constantly, accelerating the degradation.

**16. C** — Coordinators should match invocation to query complexity: simple factual queries get a single search or a direct answer; the full pipeline is for real research. A helps only repeats. B makes every unnecessary stage cheaper instead of skipping it. D changes which model runs the unnecessary pipeline, not whether it runs at all.

**17. A** — A bare `range(8)` makes an arbitrary cap the only termination — hence mid-topic truncation. Loop on `stop_reason`, with any bound kept strictly as an emergency backstop. B tunes the arbitrary number instead of removing it as the mechanism. C adds a second heuristic exit condition on top of the first. D makes users configure a bug.

**18. D** — Subagents use only what their prompts contain: the mappings existed upstream but never reached the report agent, so it improvised. Pass the claim-source mappings explicitly alongside the synthesis. A asks for restraint while withholding the data needed to comply. B invites fresh, unvetted sourcing. C corrects fabrications after generation instead of preventing them.

**19. B** — Independent analyses parallelize via multiple Task calls in one coordinator response — five subagents at once, latency near single-region time. A serializes inside one context. C changes freshness semantics to dodge an orchestration fix. D trades quality for speed unnecessarily.

**20. D** — The lost properties — failure localization, non-vanishing partial results — are exactly what hub-and-spoke routing through the coordinator provides: observability, consistent error handling, controlled information flow. A rebuilds those properties as infrastructure around a broken topology. B patches one symptom. C mistakes the cause of the speedup for proof the coordinator was waste.

**21. C** — Completeness requires an evaluation loop: the coordinator checks synthesis against required coverage, re-delegates targeted queries for gaps, and re-invokes synthesis. A instructs synthesis to include data it may not have. B formats the gap nicely without closing it. D hopes volume delivers pricing incidentally.

**22. A** — A guarantee means interception: a hook validating every `load_document` URL against the licensed domains, blocking and redirecting anything else. B detects violations after the licensing breach. C remains probabilistic. D is a naming hint, not a control.

**23. B** — Delegation should specify goals and quality criteria, leaving method to the specialist — dictated search strings are procedural micromanagement that breaks on unanticipated topics. A adds examples of the same brittle thing rather than removing the brittleness. C adds an agent to generate the brittle thing. D makes adaptation an act of disobedience.

**24. D** — Mode-switched generic tools invite wrong-mode calls; split into three purpose-specific tools with clear contracts so selection happens at the tool level, where descriptions can differentiate. A documents the confusion. B substitutes silent wrong behavior for an obvious error. C hides the decision in inference.

**25. C** — The tools differ meaningfully (curated news API, date filtering) but their descriptions don't say so — and descriptions are what selection runs on. Rewrite both to state source, parameters, and when to prefer each. A removes real capability. B is keyword routing bolted outside the tool layer. D relocates the same undocumented choice into a parameter.

**26. A** — Failures must be signaled through the MCP `isError` flag with structured content, or they're indistinguishable from data — hence quota messages becoming "findings." B makes the string less quotable, not machine-distinguishable. C disguises failure as a valid empty result. D deletes tool output based on brittle string matching instead of a real failure signal.

**27. D** — Standing visibility of curated content is what MCP resources provide: a catalog agents see without exploratory calls. A duplicates the catalog into every prompt and drifts. B secretly reweights search instead of exposing the collection. C reinvents resources as a tool call plus an instruction.

**28. B** — Replace the generic tool with a constrained alternative: `load_source` validates against the allowlist, making credibility a structural boundary. A is behavioral. C filters evidence after it has already shaped analysis. D lowers rankings but the tool still fetches anything.

**29. C** — False conflicts between figures from different periods are prevented by requiring publication/collection dates in structured outputs — temporal interpretation needs temporal metadata. A discards data for missing what upstream should provide. B is an invented heuristic that doesn't generally hold. D escalates a class of error you can eliminate systematically.

**30. A** — Deliverables must distinguish well-supported findings from gap areas caused by inaccessible sources — coverage annotations. B hides the thinness. C disclaims generally what should be marked specifically. D lists what was read without revealing what couldn't be — the reader still can't see where evidence is thin.

**31. B** — The loop is send → execute → append → **send again**: after appending tool results, the updated conversation must go back to the model. Nothing happens because the continuation request was never made. A, C, and D decorate a request that isn't being sent.

**32. C** — Unchanged code and valid prior context is exactly what `--resume` with a named session is for: continuing a named investigation across work sessions. A discards a day of context on principle. B forks with no divergence to explore, keeping a copy that's never needed. D recovers one message out of a day's understanding.

**33. A** — Independent development of two strategies from one shared baseline is `fork_session`'s purpose: two branches, no cross-contamination, no re-analysis. B lets each exploration bias the other. C re-pays for the analysis that's already been done once. D — resuming twice concurrently isn't the branching mechanism; forking is.

**34. D** — Open-ended optimization decomposes as: measure and map, identify highest-impact bottlenecks, build a prioritized plan that adapts as findings change. A applies generic fixes to an unmeasured system. B guesses the dominant factor. C substitutes anecdote for measurement.

**35. B** — Forty services through identical, predictable stages: a fixed prompt chain, the same focused passes per service. A adds adaptive machinery where nothing actually varies. C is one unfocused mega-task — attention dilution across 40 services. D gates mechanical work on interviews it doesn't need.

**36. C** — Heterogeneous formats from many sources are normalized deterministically in a `PostToolUse` hook — one canonical result structure before the model reasons. A asks the model to be the parser, probabilistically, every time. B is a multi-team migration to avoid a hook. D re-runs tests to compensate for misreading their output.

**37. B** — The Task tool is the spawning mechanism; a coordinator whose `allowedTools` lacks `"Task"` cannot delegate no matter how good the subagent definitions are, so it does everything itself. A contradicts the stem (the descriptions are good). C and D invent requirements — subagents are spawned via Task, not pre-registered in prompts or reached through a startup hook.

**38. D** — Delegation runs on AgentDefinition descriptions, and "helps with code/quality" gives the coordinator nothing to distinguish. Rewrite the descriptions with specialization and selection criteria. A trains around missing information instead of supplying it. B throws capability at an information gap. C hardcodes what descriptions express naturally.

**39. C** — Finding strings in file contents across a codebase is Grep. A matches filenames, not comments. B is Grep by hand at scale. D — built-ins search content fine; that's the point of Grep.

**40. A** — Inventorying files by naming variants is Glob: `**/Dockerfile*` and `**/*.Dockerfile`. B finds `FROM` in any file, including docs and vendored code, and normalizing filenames doesn't fix that scope problem. C finds only referenced Dockerfiles. D lists built images, not files in the repo.

**41. D** — Recommended exploration is incremental: Grep for entry points, Read the matches, follow imports to trace the flow. A reads everything for one question. B doesn't check the diagram against the actual code. C assumes filenames encode the concept — payment logic often lives elsewhere.

**42. B** — Aliased re-exports (`fmtMoney`) mean the function is called by other names: enumerate all exported names first, then Grep for each. A finds direct-path importers only. C reaches outside the built-in toolset the task specifies, and resolving barrels and aliases automatically isn't guaranteed. D explicitly ignores the alias that exists.

**43. A** — Project `.mcp.json` with `${INTERNAL_API_TOKEN}` gives zero-setup, version-controlled configuration with per-developer credentials resolved from the environment — no secret in the repo. B commits a secret. C abandons zero-setup. D generates what expansion provides natively, and still asks each developer to paste a secret in by hand.

**44. C** — The agent picks the tool it understands; "Inspects schemas" gives no case against Grep-ing familiar migration files. Enhance the description: live structures, columns, indexes, relationships, preferred for current-database questions. A and B block or ban the fallback rather than making the better tool legible. D — tool ordering isn't a selection mechanism; descriptions are.

**45. D** — Verbose comparative reading that feeds a design decision is the Explore subagent's case: module reading stays isolated, the summary lands in the design session. A spends the design context on raw input. B designs before the comparison exists. C fragments one comparison across three contexts.

**46. B** — Tool use eliminates the failure class: the extraction tool's parameters guarantee structure — no fences, no preambles, and no mid-output drift, because the API enforces the shape rather than a request the model can drift away from. A (prefill) suppresses preambles and the opening fence but guarantees nothing about the rest of the output — the drift failures survive. C is an instruction, already being violated. D is an arms race with formatting variety.

**47. D** — A required field the source may not contain pressures the model to fabricate; make `due_date` nullable and instruct null when absent. A keeps the pressure and merely models the desired format via example. B catches some fabrications after the fact (and fails on reformatted dates). C institutionalizes the fabrication.

**48. A** — The extensible-category pattern: `"other"` plus a detail field capturing the actual method — novel categories are represented faithfully, and the enum stays machine-readable. B chases reality quarterly and always trails it, while also discarding categories still in use. C pushes classification downstream, unsolved. D rejects valid business documents.

**49. C** — Multiple extraction schemas, unknown document type, structured output required: `tool_choice: "any"` — a tool call is guaranteed, and the model selects the schema fitting the document. A forces the wrong schema onto two of three types. B permits prose despite the instruction. D builds a router to replicate what "any" does automatically.

**50. B** — Impossible source data is neither passed through silently nor silently corrected: extract as stated and flag with `conflict_detected` for review. A "fixes" data it cannot verify — the error might be in either field. C stalls legitimate documents over a flag-able condition. D derives from data already suspect.

**51. A** — The date isn't in the input, so no retry can extract it — days of resubmission bought nothing. Detect information-absent failures, stop retrying, and route to rescanning or accept a documented null. B and C retry harder at reading a page that was never scanned. D deletes a real business field because one batch was scanned badly.

**52. D** — Few-shot examples teach transferable judgment — how to locate and map fields across layout variation — which generalizes to unseen structures; that's why they beat exhaustive per-layout rules. A is possible but explains nothing generalizable and contradicts "markedly improved." B treats prompt length as the mechanism, which it isn't. C is an unfalsifiable coincidence that doesn't fit the pattern described.

**53. C** — Structural variety (tables, narrative, footnotes) is the few-shot case: demonstrate correct extraction from each presentation and the model handles the spread. A presumes a reliable narrative-to-table converter — the original problem restated. B triples the pipeline to route around a single model's limitation. D shrinks automation to the easy subset.

**54. B** — The archive is the Batch API's ideal customer: enormous, latency-tolerant, half price. Onboarding has a customer waiting — synchronous. A forfeits major savings for no operational reason. C parks live customers behind a no-SLA queue. D is backwards on one of the two.

**55. A** — The guarantee must hold in the worst case: 8-hour accumulation + 24-hour processing = 32 ≤ 36 with margin. B gives 48 worst case. C's 16 + 24 = 40 breaches the SLA, and "usually faster" isn't a guarantee. D starts beyond the SLA and patches with an expedite lane.

**56. D** — With a fixed budget, first-pass success is everything: refine the prompt on a representative sample synchronously, verify, then submit the batch. A spends the budget discovering flaws at full scale. B tweaks an unrelated generation parameter instead of validating correctness. C still burns half the budget on the unvalidated version.

**57. C** — A model verifying its own extraction retains the reasoning that produced the errors — self-checks approve their own mistakes. Verification must be an independent instance comparing output to source without the extractor's context. A hands the same biased checker a rubric and an example. B repeats the biased check twice. D scores it without changing what's doing the checking.

**58. B** — 96% aggregate coexisting with 61% on handwritten forms is exactly how aggregate metrics mask segment failures: validate by document type and field before the number justifies anything, and remediate the failing segment. A hides the problem from the metric instead of fixing it. C changes the statistic, not the blindness. D accepts a segment that's wrong 4 times in 10.

**59. C** — Novel error patterns in the automated stream are caught by stratified random sampling of high-confidence extractions with ongoing human review — measuring true error rates where no one otherwise looks. A can't contain patterns that didn't exist at benchmark time. B watches the scores, not the truth. D makes customers the QA layer.

**60. A** — Thresholds come from calibration: measure actual accuracy at each confidence level against labeled data, and set the cutoff (per field type if performance differs) where accuracy meets requirements. B and C are round numbers with different amounts of caution — neither is a measurement. D averages scores into a threshold with no connection to accuracy.

---

*End of Practice Exam 10.*
