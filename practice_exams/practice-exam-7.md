# CCAFC Practice Exam 7

**Claude Certified Architect – Foundations — Practice Exam**

Rebalanced edition of Practice Exam 2 — same knowledge points; options rewritten to remove test-taking tells (option-length cues, giveaway distractors), answer letters reshuffled, one near-duplicate question replaced.

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer, three distractors. Version 1.0 also includes multiple-response items. |
| Scenarios | 4 (Multi-Agent Research, Developer Productivity, Claude Code for CI/CD, Structured Data Extraction) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (matches the official weightings):

| Domain | Questions |
|---|---|
| D1: Agentic Architecture & Orchestration (27%) | 16 |
| D2: Tool Design & MCP Integration (18%) | 11 |
| D3: Claude Code Configuration & Workflows (20%) | 12 |
| D4: Prompt Engineering & Structured Output (20%) | 12 |
| D5: Context Management & Reliability (15%) | 9 |

Two scenarios also appear on Practice Exams 1/6 — that mirrors the real exam, which draws 4 scenarios from a bank of 6. All questions here are distinct. Answer key with explanations is at the end.

---

## Scenario A: Multi-Agent Research System (Questions 1–15)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 1.** To control costs, an engineer hard-capped the coordinator's agentic loop at 5 iterations. Complex topics now produce reports that end abruptly with sections like "Analysis pending." What is the correct control-flow design?

- A) Raise the hard cap to 15 iterations, since telemetry shows that covers roughly the 95th percentile of observed task lengths for this workload.
- B) Drive the loop from `stop_reason`: continue while it's `tool_use`, stop at `end_turn`, and keep the numeric cap only as a safety backstop.
- C) Have the coordinator estimate how many iterations a task will need up front and set a per-task cap before it starts working.
- D) Prompt the coordinator to plan its work so the whole task fits inside the existing 5-iteration cap before it begins.

**Question 2.** Your pipeline researches fast-moving topics using a fixed sequence: search three predetermined subtopics → analyze → synthesize. Reviews show reports keep missing important angles that only became apparent from the initial findings (e.g., a lawsuit that reframed an industry story). What should change?

- A) Increase the number of predetermined subtopics from three to eight, using a broader fixed checklist to widen initial coverage before search begins.
- B) Run the identical fixed pipeline twice on the same three subtopics and merge the two resulting reports into one.
- C) Move to a model with a larger context window so more raw search results can be packed into the analysis step at once.
- D) Have the coordinator dynamically generate new subtasks from what each prior step discovers along the way, replacing the fixed subtopic list entirely.

**Question 3.** Your coordinator frequently delegates document-analysis tasks to the web-search subagent. Reviewing the configuration, you find the subagents defined with descriptions like "Research helper 1" and "Research helper 2." What should you fix first?

- A) Add a routing table to the coordinator's system prompt that maps specific task keywords to "Research helper 1" and "Research helper 2" by number, updating it whenever behavior drifts.
- B) Reduce the number of subagents so there are fewer wrong choices for the coordinator to pick from.
- C) Rewrite each AgentDefinition's description so it states the subagent's specialization and the situations in which to choose it.
- D) Fine-tune the coordinator on a curated set of past transcripts showing correct delegation decisions between the two helpers.

**Question 4.** You want to continue a research project whose last session ran two weeks ago. Since then, several key sources have published updates, and the session's cached tool results reflect the old versions. What is the most reliable way to continue?

- A) Start a new session, inject an organized summary of the durable findings, and re-gather current data.
- B) Resume the session with `--resume`, since most of the prior context is still valid, and add a note telling the agent that some of the cached sources may have changed since it last ran.
- C) Resume the session and let the agent decide for itself which of the cached searches look stale enough to re-run.
- D) Use `fork_session` to branch the old session so the two-week-old stale results stay isolated in the parent while the fork continues.

**Question 5.** The analysis subagent passes its findings to the coordinator as flowing prose paragraphs. By the time the synthesis agent works with them, source URLs are garbled and page numbers have disappeared. How should inter-agent context passing change?

- A) Instruct the analysis agent to double-check URLs and page numbers before writing its prose summary.
- B) Have the coordinator re-look-up the original sources for any claim whose attribution got lost somewhere in the prose handoff.
- C) Shorten the analysis agent's output so there is less prose in which citation details can get lost during synthesis.
- D) Use a structured format that separates claim content from metadata: the claim text plus explicit fields for source URL, document name, and page number.

**Question 6.** A developer invokes the document-analysis subagent, then invokes it again with the prompt "Continue analyzing the paper from before." The agent responds that it has no paper to analyze. What explains this?

- A) The second invocation used a different model tier, and tier changes silently drop access to the first invocation's cached context window.
- B) Subagent invocations are independent — each one starts fresh, and all needed context must be passed explicitly every time.
- C) The subagent's context window overflowed silently between the two invocations, discarding the paper along with older turns.
- D) The Task tool requires a `session_id` parameter to link consecutive invocations of the same subagent, and it was omitted here.

**Question 7.** Your search subagent uses three search MCP servers. One nests results under an `items` key, timestamps differ in format across all three, and relevance scores are 0–1 in one server but 0–100 in the others. The agent visibly mis-ranks sources when comparing across providers. What is the cleanest fix?

- A) Add a system prompt table documenting each provider's field names, timestamp formats, and 0–1 vs 0–100 scoring so the agent converts scores itself when comparing across providers.
- B) Use only the provider with the best-structured format and drop the other two from the toolset entirely.
- C) Normalize all three providers' results into one common structure with a `PostToolUse` hook.
- D) Ask each search provider's maintainer to adopt a shared response schema across the industry.

**Question 8.** Reports on policy topics consistently lack opposing viewpoints. The pipeline makes a single pass, and the synthesis agent can only work with what was gathered. What is the most effective fix?

- A) Add a coordinator step that evaluates the synthesis output for coverage gaps and re-delegates targeted searches to close them before finalizing the report.
- B) Add "always include opposing viewpoints" as a fixed instruction to the synthesis agent's system prompt.
- C) Have the report-generation agent append a caveats section acknowledging that other viewpoints may exist.
- D) Double the search agent's result count per query so opposing sources are more likely to appear incidentally.

**Question 9.** One search MCP tool reports failures as ordinary text — a successful-looking response whose content reads "ERROR: rate limited." Your agent has been observed quoting this string in reports as if it were a research finding. What is the correct tool-side fix?

- A) Prompt the agent to scan every search result for text beginning with "ERROR:" and disregard anything that matches that pattern before using it.
- B) Have the tool silently return an empty result set via a response-filtering hook whenever the underlying search fails, so nothing malformed enters context.
- C) Retry rate-limited requests inside the tool automatically until they succeed, so the agent never sees an error message at all.
- D) Return failures using the MCP `isError` flag with explicit, machine-readable error content instead of ordinary text.

**Question 10.** Logs show the agent retried a paywalled source six times in a row, failing identically each time, before moving on. The tool returns only "Access failed." What should the error response include to prevent this waste?

- A) Return a longer, more structured-looking error message that explains, in plain language, what a paywall is and why a subscription would be required to access the source.
- B) Structured metadata: `errorCategory: "permission"`, `isRetryable: false`, plus a short human-readable description.
- C) An HTTP 402 status code in the tool response, since models are trained to recognize 402 as payment-related.
- D) A `retryAfter` value of 24 hours in the response so retries are at least spaced further apart.

**Question 11.** Every transient search timeout currently propagates to the coordinator, which spends context reasoning about each one; coordinator contexts fill with error-handling on long tasks. How should error handling be distributed?

- A) Have subagents retry transient failures locally with backoff, and propagate to the coordinator only errors that remain unresolved, along with whatever partial results were gathered.
- B) Suppress transient errors entirely — silently drop the failed query and let the coordinator work with whatever succeeded.
- C) Route every error, transient or not, to a dedicated error-handling subagent that decides on retries for the whole system.
- D) Increase the search timeout across the board so transient failures become rare enough to ignore.

**Question 12.** A teammate asks: "The research agent is connected to arxiv-mcp, news-mcp, and finance-mcp. Where do we build the router that switches the active server per task?" What is the correct answer?

- A) In a `PreToolUse` hook that inspects the incoming task description and enables only the MCP server relevant to that task before any tool call runs.
- B) In the coordinator's system prompt, with explicit rules describing when to activate arxiv-mcp, news-mcp, or finance-mcp.
- C) Nowhere — tools from all connected MCP servers are discovered at connection time and are simultaneously available.
- D) In `.mcp.json`, using an `activeServer` field that sets a default server and lets sessions override it.

**Question 13.** The report-generation agent occasionally calls `web_search` while writing, adding last-minute uncited claims that never went through analysis or synthesis. What is the best fix?

- A) Give the report agent a citation-generator tool so any last-minute additions it makes at least carry a source attached.
- B) Remove search tools from the report agent and have it flag genuine gaps back to the coordinator instead.
- C) Add a system prompt rule telling the report agent: "Do not perform new research while writing the report."
- D) Run a separate fact-checking pass over final reports specifically to catch unvetted last-minute additions before publishing.

**Question 14.** A report flags a "contradiction": one source says unemployment was 3.9%, another says 4.4%. Investigation shows the figures are from 2023 and 2025 — both correct for their time. How do you prevent this class of error?

- A) Instruct the synthesis agent to treat any numeric differences under one percentage point as agreement between sources.
- B) Have the search agent discard all sources more than a year old before they ever reach analysis.
- C) Present both numbers side by side and let readers decide, with no annotation explaining the discrepancy.
- D) Require publication or collection dates in every subagent's structured output, so differing figures read as a time series instead of a contradiction.

**Question 15.** During a research run, two topic areas couldn't be covered because key sources were unavailable. The final report presents all sections with equal apparent confidence. What should the synthesis output include?

- A) Nothing extra — the report should only contain what was found, and the absence of coverage in a section is implied by what's missing.
- B) A self-assessed confidence percentage attached to each section, computed by the model from its own internal sense of uncertainty.
- C) Coverage annotations distinguishing well-supported findings from topic areas with gaps.
- D) A general disclaimer paragraph stating that all research carries inherent limitations and gaps.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses the built-in tools (Read, Write, Bash, Grep, Glob) and integrates with MCP servers.

---

**Question 16.** You are implementing the agent's request loop. A response arrives with `stop_reason: "tool_use"` containing a request to run Grep. What must your code do?

- A) Execute the requested Grep call, append its output to the conversation as a tool result message, and send the updated conversation back to the model.
- B) Treat the turn as complete and display the assistant's text directly to the developer without running anything.
- C) Re-send the exact same request unchanged, since a `tool_use` stop reason means the model's previous attempt at answering wasn't accepted and it must try again from scratch.
- D) Pause and ask the developer to explicitly approve continuing, since the model appears to have stopped.

**Question 17.** An engineer is three days into investigating a legacy billing system, in a session she named. No relevant files have changed overnight. Each morning she wants to continue exactly where she left off. What should she do?

- A) Start a fresh session every morning and paste in a summary of her notes from the previous day's investigation.
- B) Use `--resume` with the session's name each morning, since no relevant files changed overnight and the prior three days of context is still valid.
- C) Use `fork_session` every morning so each day of the investigation gets its own independent branch.
- D) Keep one terminal session running continuously for the entire multi-day investigation instead of closing it.

**Question 18.** You resume yesterday's analysis session, but you refactored two files last night after it ended. The resumed agent confidently describes the old versions of those files. The rest of its analysis is still accurate. What is the best course?

- A) Abandon the resumed session entirely and re-run the full multi-hour analysis of the codebase from scratch.
- B) Keep working in the resumed session and correct the agent conversationally every time it misremembers one of the two files.
- C) Run `/compact` on the session so the resulting summarization refreshes the agent's view of the two refactored files.
- D) Tell the resumed session which two specific files changed overnight and ask it to re-analyze just those.

**Question 19.** After a thorough shared analysis of your codebase, you want to rigorously compare a Jest-to-Vitest migration against staying on Jest with upgraded tooling — explored independently so one exploration doesn't bias the other. What mechanism fits?

- A) Use `fork_session` to create two independent branches from the shared analysis baseline, one per migration approach.
- B) Explore the Vitest migration and the Jest-upgrade option sequentially inside the same session, then ask for a side-by-side comparison at the end.
- C) Start two brand-new sessions, one per approach, and repeat the full shared codebase analysis independently in each.
- D) Run both explorations in one session, separated by a `/clear` command that resets context between them.

**Question 20.** You ask the agent to "add comprehensive tests to this legacy codebase" — a large, open-ended task. Which decomposition approach fits best?

- A) Process every file alphabetically, writing tests for each one in turn before moving to the next file.
- B) Generate tests for the entire codebase in a single pass so the style stays consistent throughout.
- C) Map the codebase's structure, identify high-impact areas first, then build a prioritized test plan that adapts as new discoveries emerge.
- D) Only add tests to files that changed in the last 90 days, on the assumption that older code is already stable.

**Question 21.** You're automating API documentation generation: extract endpoint signatures → describe each endpoint → generate request/response examples → cross-check descriptions against the code. The stages are the same for every service. How should this be structured?

- A) A single mega-prompt that asks the model to extract signatures, describe endpoints, generate examples, and cross-check everything against the code all in one shot.
- B) A fixed sequential prompt chain: one focused pass per stage, with each stage's output feeding the next.
- C) Dynamic decomposition that lets the agent invent a different approach to documenting each service.
- D) Four parallel subagents, one per stage, all running simultaneously against the same service.

**Question 22.** The productivity agent uses Bash. Policy: it must never run destructive git commands (`push --force`, `reset --hard`) against shared branches. It is CLAUDE.md-instructed today, but an incident still occurred. What is the correct guardrail?

- A) Strengthen the CLAUDE.md wording with bold warnings and additionally duplicate the same instruction into the agent's system prompt for redundancy.
- B) Remove Bash entirely from the agent's toolset so no shell commands of any kind can run.
- C) Have the agent explain each git command in plain language before running it, so a developer can object in time.
- D) Add a `PreToolUse` hook that intercepts Bash calls and blocks destructive git patterns against shared branches.

**Question 23.** For "repetitive" boilerplate tasks, a teammate hardcoded the tool sequence Grep → Read → Write into the agent's loop. It works for the common case but fails when a task needs several related files read first, or none at all. What does this illustrate?

- A) The model should choose which tools to call based on the actual task context; a fixed sequence can't adapt to per-task variation in what's needed.
- B) The sequence is just missing a Glob step at the beginning; a four-step hardcoded script would be robust enough.
- C) Grep should be replaced with an MCP semantic code-search tool before scripting the same fixed sequence.
- D) The Write step should be split into a separate Edit-then-Write sequence for safety.

**Question 24.** You need to find every file that imports the deprecated `LegacyHttpClient` class across a large monorepo. Which built-in tool is right for the first step?

- A) Glob — match files by name pattern across the monorepo's directory structure.
- B) Read — open files one by one across the monorepo, checking each one's imports manually.
- C) Grep — search file contents for the `LegacyHttpClient` import pattern across the codebase.
- D) Bash `ls -R` — enumerate the entire directory tree first, then inspect the files that look likely to import it.

**Question 25.** Your team needs Jira integration for the agent (create issues, query sprints — standard operations). An engineer proposes writing a custom MCP server for it. What is the better default guidance?

- A) Build the full custom server in-house, on the reasoning that in-house code is inherently more maintainable than third-party code.
- B) Use an existing community MCP server for the standard operations, reserving custom development for team-specific workflows.
- C) Skip MCP entirely and have the agent call the Jira REST API directly through Bash and curl commands.
- D) Build a thin custom MCP server that wraps only the two Jira endpoints the team needs today, expanding it later as needed.

**Question 26.** The agent tries to Edit a config block that appears verbatim in four places in one file, and Edit fails because the anchor text is not unique. What is the reliable fallback?

- A) Read the entire file into context, then Write it back in full with the intended modification applied to the correct occurrence.
- B) Retry the same Edit call with the identical anchor text, just with the `replace_all` option turned off.
- C) Use Bash `sed` to perform the replacement directly by line number instead of going through Edit.
- D) Delete the duplicate config blocks first so the remaining one becomes a unique anchor for Edit.

**Question 27.** An engineer asks the agent to explain how request authentication works in an unfamiliar 4,000-file service. Which exploration strategy should the agent use?

- A) Read every file under `src/` upfront so the eventual explanation is grounded in complete knowledge of the service.
- B) Rely on the repository's README and its directory names to infer how authentication is architected.
- C) Glob for filenames containing `*auth*` and read only the files that pattern happens to match.
- D) Grep for authentication entry points, then Read the relevant files, following imports to trace the flow end to end.

**Question 28.** Your team built a semantic code-search MCP server that outperforms text search for conceptual queries, but the agent almost always uses built-in Grep instead. Its description reads: "Searches code." What should you do?

- A) Remove Grep from the agent's toolset entirely so the MCP semantic search server is the only search option left.
- B) Add a system prompt rule stating: "Always prefer MCP tools over built-in tools, regardless of the query."
- C) Rewrite the MCP tool's description to explain what its semantic matching does, what it returns, and when it beats text search.
- D) Lower the MCP server's response latency measurably via a caching hook, on the theory that the agent will statistically learn over many calls that it is the faster tool to reach for.

**Question 29.** You want the whole team to get your GitHub MCP server automatically when they pull the repo, authenticating with each developer's own token, without committing any secrets. How?

- A) Commit a project-scoped `.mcp.json` file that references the token as `${GITHUB_TOKEN}`, expanded from each developer's own local environment.
- B) Commit `.mcp.json` to the repo with each developer's actual personal token stored in a per-user section of the file.
- C) Have each developer manually configure the GitHub MCP server themselves in their personal `~/.claude.json`.
- D) Store the token as a value inside CLAUDE.md, which is already shared with the team through version control.

**Question 30.** Your infrastructure conventions apply only to Terraform files, which live in `terraform/` directories scattered across a dozen service folders. You want the conventions loaded only when Claude edits those files, without paying their token cost in every session. What is the right mechanism?

- A) Add the Terraform conventions to the root CLAUDE.md under a dedicated "Terraform" heading, alongside the rest of the project-wide standards.
- B) Create a `.claude/rules/` file with YAML frontmatter `paths: ["**/*.tf"]` so it activates only when matching files are edited.
- C) Create a separate CLAUDE.md inside every one of the dozen scattered `terraform/` directories across the services.
- D) Create a `/terraform-rules` skill that developers are expected to invoke manually before doing infrastructure work.

---

## Scenario C: Claude Code for Continuous Integration (Questions 31–45)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 31.** You're writing the GitHub Actions step that runs the automated review. It must run without any interactive input and emit output your comment-posting script can parse. Which invocation is correct?

- A) `claude "Review this PR" --interactive=false --format=structured --schema-file review-schema.json`
- B) `CLAUDE_HEADLESS=true claude "Review this PR" --parse`
- C) `claude --batch "Review this PR" > findings.json`
- D) `claude -p "Review this PR" --output-format json --json-schema review-schema.json`

**Question 32.** Your pipeline generates code with Claude Code, then resumes the same session for the review step "so the reviewer understands why the code was written." The reviews almost never find issues, but human reviewers do. What should change?

- A) Run the review as a completely independent Claude Code instance, with none of the generation session's context or reasoning carried over.
- B) Add the instruction "be maximally critical of the changes" to the review step's existing prompt.
- C) Enable extended thinking for the review step so it spends more reasoning tokens before responding.
- D) Keep the shared session as-is, but have it review each changed file twice instead of once.

**Question 33.** The nightly test-generation job keeps proposing test scenarios that already exist in your spec files. What is the most direct fix?

- A) Run a deduplication pass afterward that compares each generated test's name against a structured list of existing test names in the suite.
- B) Have Claude generate twice as many candidate test scenarios per run, on the assumption that at least some will turn out to be novel.
- C) Provide the existing spec files in context and instruct Claude to propose only scenarios they don't already cover.
- D) Limit test generation to source files created in the last week, since older files can't need brand-new tests.

**Question 34.** Your senior engineers each keep excellent review criteria in their personal `~/.claude/CLAUDE.md` files. The CI runner's automated reviews follow none of these criteria. Why, and what is the fix?

- A) The CI runner needs an additional `--memory` flag passed at invocation time to load each engineer's user-level CLAUDE.md files.
- B) User-level CLAUDE.md never reaches the CI environment; move the review criteria into the project-level CLAUDE.md instead.
- C) The criteria files are too large for non-interactive mode — CLAUDE.md content must stay under roughly 10KB in CI.
- D) CI-invoked Claude Code cannot read any CLAUDE.md file at all; the criteria must be passed as command-line prompt flags instead.

**Question 35.** Your CI review skill only needs to read code and report findings. A pipeline audit found one run where it executed `npm install` and modified `package-lock.json` in the workspace. What is the correct constraint?

- A) Run the CI job inside a container where any filesystem write simply fails at the OS level.
- B) Add the instruction "never install packages or modify files" to the skill's existing instructions.
- C) Have the pipeline automatically revert any workspace changes after the review step finishes running.
- D) Configure `allowed-tools` in the skill's frontmatter so only read-and-report operations are permitted during the review skill's execution.

**Question 36.** Your 400-line review checklist currently lives in the root CLAUDE.md. Every interactive session pays its token cost, though it's only needed when reviews run. The checklist must stay identical for interactive `/review` use and CI. Where should it live?

- A) In a review skill under `.claude/skills/`, loaded on demand only when invoked by developers or the CI job.
- B) Split the checklist across ten smaller CLAUDE.md sections so no single block reads as unreasonably large.
- C) Keep the full 400-line checklist in CLAUDE.md exactly as it is today, and add an instruction telling Claude to simply ignore it outside of actual review runs.
- D) Move it into user-level CLAUDE.md so only the individual reviewers who opt in pay its token cost.

**Question 37.** Your changelog-generation step turns merged-PR titles into release notes. The prose spec ("group by type, past tense, link each PR") is interpreted differently across runs — grouping and tense drift. What is the most effective fix?

- A) Rewrite the spec using stricter language and bolded MUST requirements throughout.
- B) Add 2–3 concrete examples to the system prompt: sample commit-title lists paired with the exact changelog output expected for each.
- C) Convert the prose spec into a numbered checklist that the model must work through step by step.
- D) Generate three candidate drafts per run using the same ambiguous spec plus a few-shot rubric, then have a second model score each one and select whichever draft looks most compliant.

**Question 38.** You're using Claude to fix a data-transform module that intermittently fails in CI. You want an iteration loop that converges instead of whack-a-mole fixes. What is the best structure?

- A) Describe every known symptom in one message and ask for a single comprehensive fix.
- B) Ask Claude to review the module line by line and fix anything that looks suspicious.
- C) Rewrite the module from scratch, on the theory that repeated fixes mean the design itself is unfixable.
- D) Write a test suite first that covers expected behavior, known edge cases, and performance; then iterate by sharing the failing output each round.

**Question 39.** You're about to build Claude Code into your deployment-approval flow — a domain with rollback semantics, partial-failure modes, and compliance constraints you haven't fully articulated. Which technique best surfaces the hidden requirements before implementation?

- A) Implement a minimal version first and let real production incidents reveal whichever requirements are actually missing.
- B) Write the complete specification yourself, covering rollback semantics, partial-failure modes, and compliance constraints, before involving Claude at all.
- C) Use the interview pattern: have Claude question you about failure modes and edge cases before any implementation begins.
- D) Copy the integration design from a published blog post written by a team running a similar stack.

**Question 40.** Your review prompt has three problems that interact: the severity definitions conflict with the category definitions, which in turn contradict the output examples. Fixing them one at a time has caused regressions — each fix breaks under the next. How should you deliver the corrections?

- A) Address all three problems in a single detailed message that explains each one and how they interact.
- B) Fix them in three sequential messages, verifying that each fix holds before moving to the next one.
- C) Rebuild the prompt from an empty file, reintroducing every requirement one at a time from scratch.
- D) Open three parallel sessions, fix one of the three problems in each, then manually merge the best parts together.

**Question 41.** Before your CI can validate it, you must migrate the repo's test framework — 45+ files, several valid migration strategies, and infrastructure implications for the CI runners themselves. How should you begin in Claude Code?

- A) Use direct execution and go file by file, since each individual file's change is small on its own.
- B) Ask Claude to generate a single shell script that performs the entire migration mechanically.
- C) Enter plan mode to explore the test framework's usage across the codebase and compare migration strategies before changing anything.
- D) Fork 45 parallel sessions, one per file, to complete the whole migration as fast as possible.

**Question 42.** Generated tests cover happy paths well but consistently miss branch-level gaps — error paths, boundary conditions, early returns. Detailed instructions ("cover all branches, including error handling") haven't changed the behavior. What is the most effective next step?

- A) Raise the coverage threshold enforced in CI so pull requests with incomplete branch coverage fail automatically.
- B) Add few-shot examples that demonstrate finding a function's branch-level gaps and writing the tests that close them.
- C) Switch the generation prompt to ask for twice as many tests per function, padded out with generic few-shot examples of trivial cases.
- D) Run a full mutation-testing pass across the module and feed every surviving mutant back into the model as the input for another, more targeted generation pass.

**Question 43.** You're preparing your first Batch API run: overnight tech-debt analysis across 900 repositories with a prompt that has never been tested at scale. What should you do first?

- A) Submit all 900 repositories in one batch and treat this first run as the test, since batch pricing is already discounted 50%.
- B) Split the 900 repositories into two 450-repo batches, so a bad prompt only wastes half the overnight spend.
- C) Add an automatic retry wrapper that resubmits any repo whose analysis output looks wrong on inspection.
- D) Refine the prompt on a small representative sample using the synchronous API first, then submit the full 900-repo batch.

**Question 44.** Your overnight batch of 500 analysis requests completes with 38 failures, all caused by oversized diffs exceeding context limits. What is the correct recovery?

- A) Identify the 38 failures by their `custom_id`, split their oversized diffs into smaller chunks, and resubmit only those 38 requests.
- B) Resubmit the entire 500-request batch, this time with a larger context window configured for every request.
- C) Rerun just the 38 failures through the synchronous API unchanged, since it handles oversized inputs better than batch.
- D) Drop the 38 failures entirely — a 92% completion rate is within tolerance for a nightly analysis job.

**Question 45.** You want the pipeline to auto-approve PRs the review bot deems clean, but only where that trust is justified. The bot can emit a confidence score per finding. What makes the confidence usable for routing?

- A) Trust confidence scores above 8 out of 10, since models tend to be most reliable at the extremes of their own scale.
- B) Ask the model to write a short justification for each confidence score it emits, and trust whichever scores come attached to a convincing-sounding justification.
- C) Calibrate the confidence score against a labeled validation set of past reviews and derive routing thresholds from that data.
- D) Route on PR size instead of confidence — small pull requests are safe to auto-approve regardless of what the bot reports.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your extraction prompt asks Claude to "respond with a JSON object" in its text reply. About 7% of responses fail parsing — trailing commas, markdown code fences, explanatory text before the JSON. What is the most reliable fix?

- A) Add the instruction "Respond with ONLY raw JSON, no markdown, no commentary" to the extraction prompt.
- B) Strip and normalize markdown code fences, trailing commas, and any leading commentary with a structured preprocessing regex chain before ever handing the text to the JSON parser.
- C) Switch the output format from JSON to XML, on the theory that XML tolerates minor malformation better.
- D) Define an extraction tool whose input schema matches your target structure, and read the data straight from the `tool_use` block.

**Question 47.** Some invoices legitimately lack a PO number, but your schema marks `po_number` as required. Sampling reveals the model sometimes invents plausible-looking PO numbers for those invoices. What is the correct schema fix?

- A) Add a validation rule that rejects any PO number not matching your company's internal numbering format.
- B) Make `po_number` optional/nullable and instruct the model to return null when it's genuinely absent.
- C) Prompt the model to leave required fields as empty strings whenever the source data is missing.
- D) Cross-check every extracted PO number against the purchasing database's full record set and drop any invoice whose number doesn't match an existing entry.

**Question 48.** Your `document_type` enum is `["invoice", "receipt", "purchase_order"]`. New document types keep arriving (credit memos, delivery notes), and the model shoehorns them into the closest existing value. How should the schema evolve?

- A) Remove the enum entirely and make `document_type` a free-text field so any type at all can be represented.
- B) Add every document type used anywhere in your industry to the enum ahead of time, before they actually arrive.
- C) Add an `"other"` enum value paired with a free-text detail field describing what the document actually is.
- D) Reject any document that doesn't match one of the three known enum values outright, and route every rejected one into a manual queue for a human to classify by hand.

**Question 49.** You defined three extraction tools — `extract_invoice`, `extract_contract`, `extract_resume` — and documents arrive with unknown type. Sometimes the model responds with prose about the document instead of extracting. Which configuration guarantees structured output while letting the model pick the right schema?

- A) `tool_choice: "any"` — the model is required to call some tool, and it selects whichever extraction schema fits the document.
- B) `tool_choice: {"type": "tool", "name": "extract_invoice"}` — force the single most common document type's extraction tool on every incoming call, regardless of what actually arrives.
- C) `tool_choice: "auto"` combined with a prompt instruction telling the model to always use a tool regardless.
- D) Add a separate classification model upstream that first predicts the document type, then routes it to a forced single-tool call matching that prediction.

**Question 50.** Contract extractions repeatedly fail validation with `governing_law: null`. Sampling shows the governing-law clause typically lives in a master agreement referenced by, but not included with, the contracts you send. Will retry-with-error-feedback fix this?

- A) Yes — including the validation error in the retry prompt will make the model look harder at the contract text it already has.
- B) No — a retry can't recover information that was never in the input; either supply the master agreement alongside the contract or accept the null.
- C) Yes, but only with three or more retries and an escalating temperature setting to explore different readings of the text.
- D) No — the `governing_law` field should be dropped from the schema entirely, since it can never be extracted.

**Question 51.** Invoice line items sometimes don't sum to the stated total — occasionally an OCR artifact, occasionally a genuine source-document error. Downstream systems must not silently receive bad totals. What extraction design handles this?

- A) Have the model recompute the total from the line items and output that corrected value in place of whatever total the document actually stated.
- B) Reject any invoice where the line-item arithmetic doesn't check out and return it to the sender for correction.
- C) Trust `stated_total` unconditionally in every case — the source document is always the system of record.
- D) Extract a `calculated_total` field alongside `stated_total`, and raise a `conflict_detected` flag whenever the two disagree.

**Question 52.** Résumé extraction works well on standard corporate résumés but returns null for required-in-source fields on academic CVs and international formats, where the information exists but appears in unfamiliar sections. What is the most effective fix?

- A) Lengthen the field descriptions in the schema so the model better understands why each field matters.
- B) Run two separate extraction passes primed with generic few-shot examples of unrelated documents, and merge together whichever values came back non-null.
- C) Add few-shot examples showing correct extraction from an academic CV and from an international résumé format.
- D) Preprocess every incoming résumé — corporate, academic, and international alike — into one normalized, standardized layout with a universal template before it ever reaches extraction.

**Question 53.** Source documents write dates as "3/4/25", "March 4th, 2025", and "04-03-2025" (ambiguous day/month order), while your schema requires ISO 8601. What should accompany the strict output schema?

- A) Format normalization rules in the system prompt: how to map each source date format to ISO 8601, how to resolve ambiguous day/month orderings, and when to mark a date unresolvable.
- B) A post-processing date parser that converts whatever format the model happens to output into ISO 8601.
- C) A looser schema that accepts dates as free text, to be normalized by a downstream system later.
- D) Rejection of any document whose dates aren't already written in ISO 8601 in the source text.

**Question 54.** Your extraction system reports 97% overall accuracy, and leadership wants to cut human review by 80%. What must you verify before agreeing?

- A) That the 97% figure was measured within the last calendar quarter, not further back.
- B) That accuracy holds up when segmented by document type and by field — the basis needed before agreeing to any increase in the review cut.
- C) That accuracy exceeds 97% specifically on the most recent week of processed documents.
- D) That the reviewer headcount being freed up by an 80% cut can realistically be reabsorbed elsewhere in the organization once the change takes effect.

**Question 55.** You automated the pipeline for high-confidence extractions. Six months from now, how will you know whether new error patterns have crept into the extractions no human looks at?

- A) Human review already covers every low-confidence extraction, so on the assumption that confidence is well-calibrated, any new error pattern would necessarily surface there first.
- B) Track the distribution of confidence scores over time and investigate whenever the running average drifts.
- C) Re-run the original validation benchmark quarterly against the exact same set of benchmark documents.
- D) Keep a stratified random sample of high-confidence extractions under ongoing human review, even after automation ships.

**Question 56.** You calibrated the field-level confidence thresholds that decide which extractions skip human review against a labeled validation set six months ago. This week you substantially revised the extraction prompt to support several new document types. What should happen to the thresholds?

- A) Keep the existing thresholds unchanged — thresholds are properties of the output schema and downstream validation logic, neither of which changed this week.
- B) Recalibrate against fresh labeled data before trusting them; the confidence-accuracy mapping may have shifted.
- C) Raise every threshold by a fixed 10% margin until a full quarter of new production data has accumulated.
- D) Lower the thresholds temporarily, since the revised prompt should logically be more accurate than the old one.

**Question 57.** Your reviewers can inspect 500 documents daily out of 10,000 processed, and your goal is to catch as many extraction errors as possible with that fixed capacity. Which routing strategy best serves the goal?

- A) Review the 500 highest-dollar-value documents processed each day, on the reasoning that an error slipping through on a high-value document costs the most when it's eventually discovered.
- B) Review a uniform random 5% of documents daily, so every document type gets an equal audit probability.
- C) Route low-confidence extractions and those drawn from ambiguous or contradictory source documents to review.
- D) Review the newest documents first each day, since recently introduced formats are least familiar to the model.

**Question 58.** Your extraction service supports a multi-turn correction chat: users point out extraction mistakes and the model revises. Users report the model "forgets" corrections from two turns earlier. The service sends each API request with only the latest user message. What is the fix?

- A) Send the complete conversation history, including every prior correction, with each new API request.
- B) Add a system prompt instruction telling the model to remember all prior corrections on its own.
- C) Cache the model's last response client-side and re-send just that one turn with each new message.
- D) Store every correction the user makes in a database, and give the model a dedicated tool it can call to query that history back whenever it needs earlier context.

**Question 59.** Each extraction is enriched via a vendor-lookup MCP tool that returns 40+ fields per call, of which your workflow uses 5. Long enrichment sessions degrade noticeably and sometimes overflow context. What is the right fix?

- A) Call the vendor-lookup tool less often by batching several vendors into a single call.
- B) Move to a model with a larger context window so it can absorb the verbose 40-field results.
- C) Summarize the conversation with `/compact` after every ten enrichment calls.
- D) Trim the vendor-lookup tool's output down to the five relevant fields before the response ever accumulates in context.

**Question 60.** A nightly job must cross-reference 20 related documents in a single request (they reference each other, so they can't be processed separately). Fields sourced from documents in the middle of the concatenated input show markedly higher miss rates than those near the start and end. What is the best mitigation?

- A) Randomize the order of the 20 documents nightly, so no single document is always positioned in the middle.
- B) Duplicate the documents that fall in the middle of the concatenated input a second time near the end, so each one gets two separate chances to be read and extracted correctly.
- C) Add a key-facts summary at the beginning of the input and organize the documents under clearly labeled section headers.
- D) Add an explicit instruction telling the model: "Documents in the middle are equally important — do not skip them."

---
# Answer Key — Practice Exam 7

**Quick key:** 1-B, 2-D, 3-C, 4-A, 5-D, 6-B, 7-C, 8-A, 9-D, 10-B, 11-A, 12-C, 13-B, 14-D, 15-C, 16-A, 17-B, 18-D, 19-A, 20-C, 21-B, 22-D, 23-A, 24-C, 25-B, 26-A, 27-D, 28-C, 29-A, 30-B, 31-D, 32-A, 33-C, 34-B, 35-D, 36-A, 37-B, 38-D, 39-C, 40-A, 41-C, 42-B, 43-D, 44-A, 45-C, 46-D, 47-B, 48-C, 49-A, 50-B, 51-D, 52-C, 53-A, 54-B, 55-D, 56-B, 57-C, 58-A, 59-D, 60-C

---

**1. B** — Loop termination must be driven by `stop_reason`, not iteration counts: continue on `"tool_use"`, stop at `"end_turn"`. Caps are acceptable only as safety backstops. A and C just tune a cap that remains the primary stopping mechanism — some task will always exceed it. D asks the model to fit its work to an arbitrary limit rather than fixing the control flow.

**2. D** — Fast-moving, open-ended topics need dynamic decomposition: subtasks generated from what each step actually discovers. Fixed pipelines can't chase angles that only emerge mid-research. A widens the fixed net but still can't adapt. B repeats the same blindness twice. C — window size doesn't create searches that were never issued.

**3. C** — The coordinator chooses subagents based on their AgentDefinition descriptions; "Research helper 1" gives it nothing to select on. Clear specialization descriptions fix the root cause. A builds brittle keyword routing around a self-inflicted problem. B reduces options rather than clarifying them. D (fine-tuning) is out of scope and wildly disproportionate.

**4. A** — When prior tool results are stale, starting a new session with a structured summary of durable findings is more reliable than resuming — resumption is for when prior context is mostly valid. B and C resume atop stale data and depend on the agent correctly guessing what changed. D preserves the stale baseline in both branches; forking is for exploring divergent approaches, not freshness.

**5. D** — Context passed between agents should use structured formats that separate content from metadata (source URL, document name, page number) precisely so attribution survives handoffs. A still funnels metadata through prose. B tries to reconstruct provenance after it was destroyed. C reduces prose volume but not the structural fragility.

**6. B** — Subagents do not share memory between invocations; each invocation is independent and must receive all needed context explicitly in its prompt. A, C, and D invent mechanisms (tier-shared caches, cross-invocation windows, a session-linking parameter) that don't describe how the Task tool works.

**7. C** — A `PostToolUse` hook normalizing all providers into one shape/scale/format before the model sees the data removes the comparison errors deterministically. A relies on the model performing conversions correctly every time. B sacrifices coverage to avoid an integration problem with a standard solution. D is out of your control and doesn't ship this quarter.

**8. A** — Missing viewpoints are a coverage gap; only an iterative refinement loop — coordinator evaluates synthesis, re-delegates targeted searches, re-synthesizes until coverage is sufficient — can gather material that was never collected. B asks synthesis to include content it doesn't have. C papers over the gap with a disclaimer. D hopes volume incidentally includes balance.

**9. D** — The MCP `isError` flag is the mechanism for signaling tool failure; errors returned as ordinary content are indistinguishable from data, which is exactly why the agent quoted one. A is fragile string-matching over a protocol problem. B silently converts failure into "no results" behind a filtering step, misleading the agent differently. C hides genuine failures and can retry forever.

**10. B** — Structured error metadata — `errorCategory: "permission"`, `isRetryable: false`, a human-readable description — tells the agent immediately that retrying is pointless and why, so it pivots to alternatives. A adds words and a cosmetic claim of structure without anything machine-actionable. C leans on HTTP folklore instead of the MCP error contract. D still invites a retry that can never succeed.

**11. A** — The recommended distribution: subagents handle transient failures locally (retry/backoff) and propagate only unresolvable errors, with what was attempted and partial results. That keeps coordinator context for coordination. B silently suppresses errors — an anti-pattern that corrupts research completeness. C adds a communication hop for decisions best made where the failure happened. D reduces frequency without fixing the architecture.

**12. C** — There is no server switching: tools from all configured MCP servers are discovered at connection time and are simultaneously available; selection happens through tool descriptions like any other tools. A, B, and D all build (or invent — there is no `activeServer` field) machinery for a problem the protocol already solves.

**13. B** — The report agent's role is rendering synthesized, vetted findings; search tools are outside its specialization and their misuse (uncited last-minute claims) is the predictable result. Scope its tools to its role and route real gaps back through the coordinator. A legitimizes bypassing the pipeline. C is probabilistic — the behavior already occurs. D catches contamination after the fact.

**14. D** — Requiring publication/collection dates in structured outputs lets synthesis interpret differing figures as time-series data instead of contradictions. A is an arbitrary numeric heuristic that would also mask genuine conflicts. B throws away valid historical data. C presents the confusion to the reader instead of resolving its cause.

**15. C** — Synthesis output should carry coverage annotations: which findings are well-supported and which topic areas have gaps due to unavailable sources. A and D leave readers unable to distinguish thin coverage from strong coverage. B substitutes uncalibrated self-reported confidence for the factual annotation the system can actually make (these sources were unavailable).

**16. A** — `stop_reason: "tool_use"` means: execute the requested tool, append the result to the conversation as a tool result, and send it back for the next iteration. That's the agentic loop. B abandons the task mid-loop. C re-sends without providing the result the model asked for, on a mistaken reading of what the stop reason means. D inserts a human where none is required.

**17. B** — Named session resumption (`--resume <session-name>`) is designed for exactly this: continuing a specific prior conversation whose context is still valid (no relevant files changed). A discards accumulated context that resumption preserves. C forks branches with no divergent approaches to explore. D conflates process uptime with session persistence.

**18. D** — When resuming after code modifications, inform the session which specific files changed for targeted re-analysis; the rest of the context is still valid. A re-spends hours to refresh two files. B leaves stale beliefs in context to resurface later. C — `/compact` summarizes conversation history; it doesn't re-read changed files.

**19. A** — `fork_session` exists for exploring divergent approaches from a shared analysis baseline: two independent branches, each unbiased by the other's exploration, both grounded in the same understanding. B lets the first exploration contaminate the second. C pays for the codebase analysis twice. D — `/clear` discards the shared analysis the comparison depends on.

**20. C** — Open-ended tasks decompose best by mapping structure, identifying high-impact areas, and building a prioritized plan that adapts as dependencies are discovered. A spends effort by filename rather than by risk. B is one unfocused pass over a large codebase — attention dilution. D uses recency as a proxy for importance; critical old code stays untested.

**21. B** — Predictable, identical multi-stage workflows are the home ground of prompt chaining: focused sequential passes, each feeding the next. A crams four concerns into one pass and loses focus. C adds adaptive machinery where nothing varies. D ignores the data dependency — stage 2 needs stage 1's output.

**22. D** — A must-never-happen rule needs programmatic enforcement: a hook intercepting Bash calls and blocking destructive git patterns gives a deterministic guarantee. A doubles down on prompt-based compliance, which already failed, just in two places instead of one. B is a structural guarantee but massively over-broad — it removes all shell capability to block two command patterns. C relies on developers reading every command in time.

**23. A** — Pre-configured sequences fail on per-task variation; the case for model-driven behavior is that the model chooses tools based on the actual task context. B and D just lengthen or reshuffle the script — some task will break any fixed sequence. C swaps one tool inside a script whose problem is being a script.

**24. C** — Finding files by their *contents* (an import statement) is Grep's job: search the codebase for the pattern. A (Glob) matches file *names*, which tell you nothing about imports. B reads blindly at monorepo scale. D enumerates names, same limitation as Glob with more steps.

**25. B** — For standard integrations like Jira, existing community MCP servers are the default; custom server development is reserved for team-specific workflows. A and D both spend engineering time re-solving a solved problem — the thin wrapper still needs auth, error handling, and maintenance the community server already has. C abandons MCP's typed tool interface for shell-and-curl fragility.

**26. A** — When Edit can't find a unique anchor, the documented fallback is Read the full file, then Write it back with the modification applied. B retries the exact failure. C bypasses the harness's file tools for `sed` line-number surgery — easy to get subtly wrong. D makes semantic changes to the file just to enable a mechanical edit.

**27. D** — Build understanding incrementally: Grep for entry points, Read the relevant files, follow imports to trace the flow. That answers the question with minimal context spend. A exhausts context on mostly-irrelevant files. B infers instead of verifying. C assumes auth code is named "auth" — middleware, guards, and interceptors say otherwise.

**28. C** — The agent prefers Grep because it understands what Grep does; a two-word MCP description gives the semantic tool no case for selection. Enhancing the description — capabilities, outputs, when it beats text search — is the documented fix. A removes a tool that's still right for exact-string searches. B is a blanket rule that misroutes exact-match queries. D — the agent isn't choosing on latency, and there's no mechanism by which it would "learn" to prefer a faster tool over many independent calls.

**29. A** — Project-scoped `.mcp.json` is shared via version control, and `${GITHUB_TOKEN}` environment-variable expansion supplies each developer's own credential at runtime without committing secrets. B commits secrets. C isn't shared — every developer configures by hand. D puts a credential in a context file; CLAUDE.md is instructions, not secret storage.

**30. B** — A `.claude/rules/` file with `paths: ["**/*.tf"]` frontmatter loads the conventions only when matching files are edited — glob-based activation that works no matter which directories the files sit in. A pays the token cost in every session. C means a dozen files to keep synchronized. D loads only when a human remembers to invoke it.

**31. D** — `-p` runs Claude Code non-interactively (print result and exit), and `--output-format json` with `--json-schema` yields machine-parseable, schema-conforming output. A, B, and C are built from flags and environment variables that don't exist (`--interactive`, `--schema-file`, `CLAUDE_HEADLESS`, `--batch`).

**32. A** — A session that generated the code retains the reasoning that produced it and is unlikely to question its own decisions; independent review instances catch what self-review misses. The "understands why" intuition is precisely the bias. B and C intensify a structurally biased review. D repeats it.

**33. C** — Provide the existing test files in context and instruct generation to avoid scenarios already covered — the model can't avoid duplicating tests it has never seen. A catches only name collisions, not semantic duplicates, and only after the fact. B generates more duplicates alongside the novelty. D abandons coverage improvement for existing code, which was the point.

**34. B** — User-level CLAUDE.md lives in each engineer's home directory; the CI runner has no such files. Project-level CLAUDE.md is in the repository, so the CI checkout carries it. The fix is moving the criteria there (which also shares them with the whole team). A, C, and D describe flags and limits that don't exist.

**35. D** — `allowed-tools` in the skill frontmatter removes execution tools from availability during the skill — a structural guarantee that read-and-report is all it can do. A contains damage at the infrastructure layer but lets the harness misbehave inside it. B is instruction-based and already failed once. C cleans up afterward instead of preventing.

**36. A** — On-demand, task-specific content belongs in a skill: invoked identically by developers and CI, absent from unrelated sessions. That's the skills-vs-CLAUDE.md dividing line (always-loaded universal standards vs. on-demand workflows). B still loads everything, just in pieces. C pays full cost and adds an ignore instruction the model may not reliably follow. D hides team-shared material in personal config.

**37. B** — When prose specs are interpreted inconsistently, concrete input/output examples are the most effective correction — they show the exact grouping, tense, and linking expected. A is stronger prose with the same ambiguity. C is still prose instructions, restructured — the interpretation variance remains. D spends three generations plus a judgment call to avoid writing two examples.

**38. D** — Test-driven iteration: write the suite covering expected behavior, edge cases, and performance first, then iterate by sharing failures. The tests define "done" and each round has an objective target. A and B are single-shot or unfocused passes with no convergence criterion. C throws away working behavior on a hunch.

**39. C** — The interview pattern is designed for unfamiliar domains with unarticulated constraints: Claude asks the questions that surface failure modes and edge cases you didn't think to specify. A discovers requirements via incidents. B assumes you can enumerate considerations you haven't anticipated — the exact gap, just written by you alone instead of by an agent that already failed to help you here. D imports another team's constraints, not yours.

**40. A** — Interacting problems must be fixed together: one detailed message addressing all three and how they interrelate. Sequential fixes (B) are what's already regressing — each fix optimizes against soon-to-change context. C discards the working parts along with the broken ones. D produces three prompts that each still contain two of the conflicts.

**41. C** — Multi-file scope (45+), multiple valid strategies, and infrastructure implications are the plan-mode trifecta: explore, compare approaches, and commit to a design before changing anything. A starts changing files before the strategy exists. B mechanizes a decision that hasn't been made. D parallelizes without an agreed approach — 45 sessions, several strategies.

**42. B** — When instructions fail to change behavior, few-shot examples demonstrating the analysis — here, spotting branch-level gaps and writing the closing tests — teach the judgment so the model generalizes it. A fails PRs without improving them. C multiplies happy-path tests. D is real but heavyweight infrastructure to reach for before trying examples.

**43. D** — Refine the prompt on a representative sample before batch-processing large volumes: first-pass success is what controls cost when a batch is 900 items and results arrive up to 24 hours later. A risks 900 bad analyses and a full resubmission cycle. B halves the waste instead of preventing it. C automates resubmission of a prompt that was never validated.

**44. A** — Batch failure handling: identify failed requests by `custom_id`, fix the cause (chunk the oversized diffs), and resubmit only those. B re-pays for 462 successful analyses (and "larger context configuration" isn't a batch setting). C re-sends the same oversized inputs to the same context limits. D silently drops the repos most likely to harbor debt — the biggest diffs.

**45. C** — Self-reported confidence is only usable after calibration: measure it against a labeled validation set with known outcomes and derive thresholds from measured accuracy. A trusts raw self-report at its extremes — known to be poorly calibrated regardless of where on the scale it sits. B swaps numeric self-report for a persuasive-sounding narrative self-report, which is no more grounded. D substitutes a proxy (size) for the measurement you need.

**46. D** — Tool use with a JSON schema is the reliable mechanism for structured output: the extraction "tool" input conforms to your schema, eliminating trailing commas, fences, and preambles as a failure class. A reduces frequency but keeps the class. B is an arms race with formatting drift — every new failure mode needs a new regex. C changes the syntax without adding any guarantee.

**47. B** — Required fields pressure the model to fabricate; fields that may legitimately be absent should be optional/nullable with instructions to return null. That removes the incentive to invent. A rejects fabrications after inviting them. C misuses empty strings as a null substitute while keeping the pressure. D is a downstream audit for an upstream schema problem.

**48. C** — The extensible-category pattern: an `"other"` enum value plus a detail string. Novel types are captured faithfully instead of forced into the nearest wrong bucket. A loses the machine-readable categories downstream systems rely on. B guesses the future and still misses something. D turns every novel type into manual work and discards the document instead of extracting what it safely can.

**49. A** — `tool_choice: "any"` guarantees a tool call while leaving the choice of tool to the model — exactly right when multiple extraction schemas exist and the document type is unknown. B forces the invoice schema onto contracts and résumés regardless of which arrives. C ("auto") is what permits the prose responses today. D adds a whole extra model and routing layer to replicate what "any" already does directly.

**50. B** — Retries correct format and structural errors; they cannot recover information that is absent from the provided input. The governing law lives in a document the model never sees. Fix the input pipeline or handle the null explicitly. A and C retry harder, and hotter, at reading text that isn't there. D deletes a business-required field because the pipeline starves it.

**51. D** — Extracting `calculated_total` alongside `stated_total` with a `conflict_detected` flag is the self-correction/validation design: discrepancies are surfaced, not silently passed through (C) or silently overwritten (A — which hides genuine source-document errors that may matter legally). B treats every OCR artifact as a sender problem and stalls the pipeline.

**52. C** — Few-shot examples demonstrating extraction from varied document structures are the established fix for structure-driven misses — they show where the information lives in each format, and the model generalizes to further variants. A re-describes fields the model already understands. B reruns the same blindness twice. D presumes a reliable universal normalizer covering every résumé variant, which is the original problem restated as its own solution.

**53. A** — Strict output schemas should be paired with format normalization rules in the prompt: how to map each source format to ISO 8601, how to disambiguate day/month order (e.g., from document context), and when to mark a value unresolvable. B pushes ambiguity downstream to a parser with even less context than the model had. C just relocates the problem. D rejects most real-world documents.

**54. B** — Aggregate accuracy can mask severe failures on specific segments; before reducing review, verify accuracy by document type and field. A flat 97% is consistent with near-total failure on one vendor's layout. A and C re-slice by time, not by segment. D is a staffing question, not a validation of the automation's safety.

**55. D** — Stratified random sampling of high-confidence extractions provides ongoing error-rate measurement and catches novel error patterns in exactly the population no one otherwise inspects. A assumes new errors will conveniently arrive with low confidence — miscalibration means they won't, so that population is never actually checked. B monitors the model's opinion of itself, not actual accuracy; confidently-wrong errors never move the average. C can't detect novel patterns absent from the original benchmark.

**56. B** — Calibration maps confidence to measured accuracy *for a specific system*; substantially changing the prompt changes that mapping, so thresholds must be re-validated against labeled data before extractions skip review on their strength. A ties calibration to the wrong artifact — the schema didn't drive the mapping, the model+prompt did. C and D adjust blindly in opposite directions; neither is a measurement.

**57. C** — To catch the most errors with fixed capacity, route review to where errors are most likely: low model confidence and ambiguous or contradictory source documents. A targets cost-of-error, not likelihood-of-error — high-value documents are mostly extracted correctly. B spreads capacity evenly over mostly-fine documents. D uses recency as a weak proxy for difficulty.

**58. A** — The API is stateless: conversational coherence requires passing the complete conversation history in every request. Sending only the latest message *is* the bug. B instructs the model to remember context it was never sent. C restores one turn of history — corrections from two turns back stay lost. D rebuilds conversation memory as external infrastructure the model has to remember to query on its own.

**59. D** — Verbose tool outputs consume context disproportionately to their relevance; trimming to the relevant fields before results accumulate (tool-side or via a PostToolUse transformation) fixes the accumulation at the source. A changes call frequency, not per-call bloat. B delays the overflow and doesn't address degradation. C summarizes after the tokens are already spent, repeatedly.

**60. C** — This is the lost-in-the-middle effect. Since splitting the request isn't possible, apply the position mitigations: a key-facts summary at the beginning and explicit, labeled section headers organizing the detail. A rotates which fields get missed rather than fixing the underlying position effect. B doubles input size and still buries other documents behind the same weak middle positions. D — position effects are not fixed by exhortation.

---

*End of Practice Exam 7.*
