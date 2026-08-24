# CCAFC Practice Exam 2

**Claude Certified Architect – Foundations — Practice Exam**

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

Two scenarios also appear on Practice Exam 1 — that mirrors the real exam, which draws 4 scenarios from a bank of 6. All questions here are new. Answer key with explanations is at the end.

---

## Scenario A: Multi-Agent Research System (Questions 1–15)

You are building a multi-agent research system using the Claude Agent SDK. A coordinator agent delegates to specialized subagents: one searches the web, one analyzes documents, one synthesizes findings, and one generates reports. The system researches topics and produces comprehensive, cited reports.

---

**Question 1.** To control costs, an engineer hard-capped the coordinator's agentic loop at 5 iterations. Complex topics now produce reports that end abruptly with sections like "Analysis pending." What is the correct control-flow design?

- A) Raise the iteration cap from 5 to 15, since profiling this exact workload shows that number covers the 95th percentile of observed task lengths.
- B) Have the coordinator estimate how many iterations a task will need up front and set a custom per-task cap before starting.
- C) Drive the loop from `stop_reason` — continue on `"tool_use"`, stop at `"end_turn"`, keeping iteration caps only as a safety backstop.
- D) Prompt the coordinator to plan its work so it always fits within the existing 5-iteration cap before starting.

**Question 2.** Your pipeline researches fast-moving topics using a fixed sequence: search three predetermined subtopics → analyze → synthesize. Reviews show reports keep missing important angles that only became apparent from the initial findings (e.g., a lawsuit that reframed an industry story). What should change?

- A) Increase the number of predetermined subtopics from three to eight, expanding coverage before research starts based on a stakeholder-supplied topic checklist.
- B) Use dynamic task decomposition — have the coordinator generate new subtasks from what each step actually discovers, rather than fixing the subtopics before research begins.
- C) Run the same fixed three-subtopic pipeline twice in parallel and merge the two resulting reports.
- D) Move to a model with a larger context window so more search results fit into the single analysis pass.

**Question 3.** Your coordinator frequently delegates document-analysis tasks to the web-search subagent. Reviewing the configuration, you find the subagents defined with descriptions like "Research helper 1" and "Research helper 2." What should you fix first?

- A) Rewrite each subagent's description to state its specialization and the situations where it should be chosen for a task.
- B) Add a routing table to the coordinator's prompt that maps keywords like "PDF," "cite," or "compare" to specific numbered research helpers.
- C) Reduce the subagent count to two, on the theory that fewer choices means fewer chances to delegate incorrectly.
- D) Fine-tune the coordinator model on a curated set of transcripts demonstrating correct delegation decisions.

**Question 4.** You want to continue a research project whose last session ran two weeks ago. Since then, several key sources have published updates, and the session's cached tool results reflect the old versions. What is the most reliable way to continue?

- A) Resume the session with `--resume` and add a note warning the agent that some sources may have changed since the last run.
- B) Resume the session and let the agent decide for itself which of the cached searches look stale enough to re-run.
- C) Use `fork_session` to branch the old session so the two-week-old cached results stay isolated in the parent branch.
- D) Start a new session and inject a structured summary of the durable findings, then re-gather current data fresh — resuming with two-week-old cached tool results is less reliable than a clean start built on a compact summary.

**Question 5.** The analysis subagent passes its findings to the coordinator as flowing prose paragraphs. By the time the synthesis agent works with them, source URLs are garbled and page numbers have disappeared. How should inter-agent context passing change?

- A) Instruct the analysis agent to double- and triple-check every URL, document name, and page number before it writes its prose summary, catching slips before they spread through the pipeline.
- B) Use a structured format that separates content from metadata — each finding carries its claim text plus dedicated fields for source URL, document name, and page number.
- C) Have the coordinator re-look-up the original sources for any claims whose attribution got garbled in transit.
- D) Shorten the analysis agent's output so there is less prose for details like URLs and page numbers to get lost in.

**Question 6.** A developer invokes the document-analysis subagent, then invokes it again with the prompt "Continue analyzing the paper from before." The agent responds that it has no paper to analyze. What explains this?

- A) The second invocation used a different model tier, and separate tiers don't share any structured cache context with each other.
- B) The subagent's context window silently overflowed between the two invocations, discarding the earlier paper entirely.
- C) Subagent invocations are independent — subagents do not share memory between invocations, so all needed context must be passed explicitly each time.
- D) The Task tool exposes a `session_id` parameter for linking consecutive invocations, and this invocation omitted it, so the two calls were treated as unrelated.

**Question 7.** Your search subagent uses three search MCP servers. One nests results under an `items` key, timestamps differ in format across all three, and relevance scores are 0–1 in one server but 0–100 in the others. The agent visibly mis-ranks sources when comparing across providers. What is the cleanest fix?

- A) Implement a `PostToolUse` hook that normalizes all three providers' results into one shape and score scale before the model sees them.
- B) Add a table to the prompt documenting each provider's exact format and scale so the agent manually converts scores whenever it compares results across the three sources.
- C) Use only the provider with the cleanest response format and drop the other two search sources entirely.
- D) Ask each search provider's maintainer to adopt a shared, normalized response schema across all three services.

**Question 8.** Reports on policy topics consistently lack opposing viewpoints. The pipeline makes a single pass, and the synthesis agent can only work with what was gathered. What is the most effective fix?

- A) Add a hard "always include opposing viewpoints on any policy topic, regardless of what was found" rule to the synthesis agent's prompt so balance is mandated directly.
- B) Have the report agent append a caveats section acknowledging that other viewpoints may exist beyond what was gathered.
- C) Double the search agent's result count per query so opposing sources are more likely to appear incidentally in the raw results.
- D) Add a coordinator evaluation step that checks synthesis output for gaps like missing viewpoints, re-delegates targeted searches to fill them, and re-invokes synthesis until coverage is sufficient.

**Question 9.** One search MCP tool reports failures as ordinary text — a successful-looking response whose content reads "ERROR: rate limited." Your agent has been observed quoting this string in reports as if it were a research finding. What is the correct tool-side fix?

- A) Prompt the agent to scan search results for text beginning with "ERROR:" and disregard any match it finds before using the content.
- B) Return failures using the MCP `isError` flag with structured error content, so the agent recognizes a failure instead of ingesting it as a finding.
- C) Have the tool return an empty result set whenever it fails, so nothing incorrect ever enters the agent's context.
- D) Retry rate-limited requests inside the tool automatically, with exponential backoff, until they eventually succeed, so the agent never has to observe an error at all.

**Question 10.** Logs show the agent retried a paywalled source six times in a row, failing identically each time, before moving on. The tool returns only "Access failed." What should the error response include to prevent this waste?

- A) Machine-readable error metadata: `errorCategory: "permission"`, `isRetryable: false`, and a short human-readable description, so the agent pivots immediately.
- B) A longer error message that explains what paywalls are and why they block automated access, in plain prose.
- C) An HTTP 402 status code, since models are trained to recognize 402 as a payment-related failure.
- D) A `retryAfter` value of 24 hours combined with a note that the source is temporarily unavailable, so future retries are spaced further apart and less wasteful.

**Question 11.** Every transient search timeout currently propagates to the coordinator, which spends context reasoning about each one; coordinator contexts fill with error-handling on long tasks. How should error handling be distributed?

- A) Suppress transient errors entirely inside the subagent — drop the failed query silently and let the coordinator work only with whatever succeeded.
- B) Route every error, transient or permanent, through one dedicated error-handling subagent whose sole job is deciding on retries and escalation for the entire multi-agent research system end to end.
- C) Have subagents retry transient failures locally with backoff, and propagate only unresolved errors to the coordinator, including what was attempted and any partial results.
- D) Increase every search tool's timeout value substantially so transient timeout failures become rare in the first place.

**Question 12.** A teammate asks: "The research agent is connected to arxiv-mcp, news-mcp, and finance-mcp. Where do we build the router that switches the active server per task?" What is the correct answer?

- A) In a `PreToolUse` hook that inspects the upcoming task description and enables only the matching server for that call.
- B) In the coordinator's prompt, with explicit rules describing when to activate each of the three MCP servers.
- C) In `.mcp.json`, using an `activeServer` field to set a session default and override it per task.
- D) Nowhere — tools from all configured MCP servers are discovered at connection time and stay simultaneously available; the agent selects among them using tool descriptions, so no server-switching router exists or needs to be built.

**Question 13.** The report-generation agent occasionally calls `web_search` while writing, adding last-minute uncited claims that never went through analysis or synthesis. What is the best fix?

- A) Remove search tools from the report agent's toolset, since its role is to render vetted findings, not gather new ones.
- B) Give the report agent a dedicated citation-generator tool so any last-minute research it performs at least comes with sources attached and traceable.
- C) Add a `PostToolUse` hook that strips out any search results the report agent tries to use while drafting, instead of removing the tool itself.
- D) Run a fact-checking pass over finished reports afterward to catch any unvetted claims that slipped in.

**Question 14.** A report flags a "contradiction": one source says unemployment was 3.9%, another says 4.4%. Investigation shows the figures are from 2023 and 2025 — both correct for their time. How do you prevent this class of error?

- A) Instruct the synthesis agent to normalize any numeric difference smaller than a full percentage point into agreement, rather than flagging a contradiction to resolve.
- B) Have the search agent discard every source more than one year old before it ever reaches synthesis, regardless of topic.
- C) Require subagents to include publication or data-collection dates in their outputs so temporal differences read as time-series data, not contradictions.
- D) Present both numbers side by side in the report and let the reader decide which is current, with no annotation at all.

**Question 15.** During a research run, two topic areas couldn't be covered because key sources were unavailable. The final report presents all sections with equal apparent confidence. What should the synthesis output include?

- A) Nothing extra — the report should only contain what was actually found; the absence of coverage in a section is implied by what's missing.
- B) Coverage annotations distinguishing findings that are well-supported from topic areas that have gaps because key sources were unavailable.
- C) A single disclaimer paragraph at the end stating that all research has inherent limitations and gaps.
- D) Placeholder sections for the uncovered topics, filled in using the model's own general background knowledge so every section of the report reads as complete and equally confident.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses the built-in tools (Read, Write, Bash, Grep, Glob) and integrates with MCP servers.

---

**Question 16.** You are implementing the agent's request loop. A response arrives with `stop_reason: "tool_use"` containing a request to run Grep. What must your code do?

- A) Treat the turn as complete and display the assistant's message text to the developer right away.
- B) Re-send the exact same request unchanged, since `"tool_use"` means the model needs another attempt at the same call.
- C) Pause and ask the developer to approve continuing, since the model has stopped to wait for input.
- D) Execute the requested Grep call, append its result to the conversation as a tool result, and send the updated conversation back to Claude so it can continue the loop with that result in hand.

**Question 17.** An engineer is three days into investigating a legacy billing system, in a session she named. No relevant files have changed overnight. Each morning she wants to continue exactly where she left off. What should she do?

- A) Use `--resume` with the session's name to continue exactly that named session, since nothing relevant changed overnight and the prior context is still valid.
- B) Start a brand-new session each morning and manually paste in written notes summarizing yesterday's findings from memory, hoping nothing important got left out.
- C) Use `fork_session` each morning so every day of the investigation gets its own separate branch.
- D) Keep one terminal session open and running continuously for the entire multi-day investigation instead of closing it.

**Question 18.** You resume yesterday's analysis session, but you refactored two files last night after it ended. The resumed agent confidently describes the old versions of those files. The rest of its analysis is still accurate. What is the best course?

- A) Abandon the resumed session entirely, since reusing it after files changed invalidates everything it already worked out, and re-run the entire multi-hour codebase analysis again from a completely clean start.
- B) Keep working in the resumed session and correct the agent conversationally each time it misremembers a refactored file.
- C) Tell the resumed session which two files changed overnight and ask it to re-analyze just those, keeping the rest of the still-valid context.
- D) Run `/compact` on the session so summarization refreshes the agent's understanding of the two files.

**Question 19.** After a thorough shared analysis of your codebase, you want to rigorously compare a Jest-to-Vitest migration against staying on Jest with upgraded tooling — explored independently so one exploration doesn't bias the other. What mechanism fits?

- A) Explore both migration options sequentially within the same session, then ask the agent for a side-by-side comparison afterward.
- B) Use `fork_session` to branch two independent copies from the shared analysis baseline so each migration approach is explored separately, without either exploration's findings biasing the other.
- C) Start two brand-new sessions, one per approach, repeating the full codebase analysis independently in each before exploring.
- D) Ask the agent to write a comparative essay weighing the two approaches without doing any further exploration first.

**Question 20.** You ask the agent to "add comprehensive tests to this legacy codebase" — a large, open-ended task. Which decomposition approach fits best?

- A) First map the codebase's structure and risk areas, then build a prioritized test plan that adapts as dependencies and surprises are discovered.
- B) Process every file alphabetically, writing tests for each one before moving to the next, to guarantee complete coverage across the codebase.
- C) Generate tests for the entire codebase in a single pass so the testing style stays consistent throughout.
- D) Only add tests to files that were changed in the last 90 days, on the assumption that older, untouched code has already proven itself stable in production.

**Question 21.** You're automating API documentation generation: extract endpoint signatures → describe each endpoint → generate request/response examples → cross-check descriptions against the code. The stages are the same for every service. How should this be structured?

- A) A single mega-prompt asking for finished, polished documentation for the whole service in one shot.
- B) Dynamic decomposition that lets the agent invent a different approach to the four stages for each service.
- C) Four parallel subagents, one per stage, all running simultaneously against the same service, producing every artifact — signatures, descriptions, examples, and cross-checks — all at once.
- D) A fixed sequential prompt chain — one focused pass per stage feeding into the next — since the workflow is predictable across services.

**Question 22.** The productivity agent uses Bash. Policy: it must never run destructive git commands (`push --force`, `reset --hard`) against shared branches. It is CLAUDE.md-instructed today, but an incident still occurred. What is the correct guardrail?

- A) Strengthen the CLAUDE.md wording around destructive commands, add the identical rule to the agent's own system prompt as a redundant reminder, and ask developers to review transcripts weekly for any slip-ups.
- B) Remove Bash from the agent's toolset entirely and accept the loss of all shell capability across every task.
- C) Add a `PreToolUse` hook that intercepts every Bash tool call and blocks any command matching destructive git patterns like `push --force` or `reset --hard` against shared branches.
- D) Have the agent explain each git command it plans to run before executing it, so developers have a chance to object.

**Question 23.** For "repetitive" boilerplate tasks, a teammate hardcoded the tool sequence Grep → Read → Write into the agent's loop. It works for the common case but fails when a task needs several related files read first, or none at all. What does this illustrate?

- A) The sequence is only missing a Glob step at the beginning; a four-step hardcoded script would be robust enough.
- B) Pre-configured sequences can't adapt to per-task variation — the model should decide which tools to call based on the actual task context each time, which is the whole point of model-driven agentic behavior.
- C) Grep should be swapped for an MCP code-search tool before the three-step sequence gets scripted.
- D) The Write step should be split into an Edit-then-Write pair for extra safety.

**Question 24.** You need to find every file that imports the deprecated `LegacyHttpClient` class across a large monorepo. Which built-in tool is right for the first step?

- A) Grep — search file contents across the monorepo for the literal import pattern naming `LegacyHttpClient`.
- B) Glob — match candidate files by name pattern first, then decide which ones to inspect further by hand.
- C) Read every file one by one across the monorepo, manually checking each file's import statements as you go.
- D) Bash `ls -R` to enumerate the entire monorepo tree first, then manually inspect whichever files look most likely to import the deprecated class.

**Question 25.** Your team needs Jira integration for the agent (create issues, query sprints — standard operations). An engineer proposes writing a custom MCP server for it. What is the better default guidance?

- A) Build the custom server in-house, since internally maintained integrations are always easier to keep perfectly aligned with your team's exact workflow than adopting someone else's code.
- B) Skip MCP entirely and have the agent call the Jira REST API directly through Bash and curl commands.
- C) Use an existing community MCP server for a standard integration like Jira, saving custom development for genuinely team-specific workflows.
- D) Wait until Atlassian ships native Claude integration rather than building anything now.

**Question 26.** The agent tries to Edit a config block that appears verbatim in four places in one file, and Edit fails because the anchor text is not unique. What is the reliable fallback?

- A) Retry the same Edit call with the identical anchor text, just with the `replace_all` option turned off this time.
- B) Use Bash `sed` to perform the replacement directly by line number instead of going through Edit.
- C) Delete the three duplicate config blocks first, leaving only the one that needs changing, so its anchor text becomes unique enough for the original Edit call to succeed.
- D) Read the full file, then Write it back with the intended modification applied at the correct location.

**Question 27.** An engineer asks the agent to explain how request authentication works in an unfamiliar 4,000-file service. Which exploration strategy should the agent use?

- A) Read every file under `src/` upfront so the eventual explanation is grounded in complete knowledge of the codebase.
- B) Start with Grep for entry points like middleware registration and auth imports, then Read the relevant files, following imports to trace the flow, building understanding incrementally rather than exhaustively.
- C) Rely on the repository's README and its directory names to infer how authentication is architected.
- D) Glob for filenames containing `*auth*` and read only the files that match.

**Question 28.** Your team built a semantic code-search MCP server that outperforms text search for conceptual queries, but the agent almost always uses built-in Grep instead. Its description reads: "Searches code." What should you do?

- A) Enhance the MCP tool's description to explain what it does — semantic matching — what it returns, and when it beats plain text search.
- B) Remove Grep from the agent's toolset entirely, on the theory that a smaller toolset with one search option left forces the model to default to the semantic MCP server every time.
- C) Add a prompt rule stating "always prefer MCP tools over built-in tools" for every search task.
- D) Lower the MCP server's response latency so the agent eventually learns it is the faster option to reach for.

**Question 29.** You want the whole team to get your GitHub MCP server automatically when they pull the repo, authenticating with each developer's own token, without committing any secrets. How?

- A) Commit `.mcp.json` with each developer's personal access token written directly into that developer's own per-user section of the same file.
- B) Have each developer manually configure the GitHub server in their own personal `~/.claude.json` file.
- C) Commit a project-scoped `.mcp.json` that references the token as `${GITHUB_TOKEN}`, expanded from each developer's environment at runtime.
- D) Store the token as a value inside CLAUDE.md, which is already shared through version control anyway.

**Question 30.** Your infrastructure conventions apply only to Terraform files, which live in `terraform/` directories scattered across a dozen service folders. You want the conventions loaded only when Claude edits those files, without paying their token cost in every session. What is the right mechanism?

- A) Add the Terraform conventions to the root CLAUDE.md under a dedicated, clearly labeled "Terraform" heading near the top.
- B) Create a separate CLAUDE.md file inside every one of the dozen scattered `terraform/` directories, keeping the text duplicated in each one.
- C) Create a `/terraform-rules` skill that developers have to remember to invoke manually before starting any infrastructure work.
- D) Create a `.claude/rules/` file with YAML frontmatter `paths: ["**/*.tf"]` so rules load automatically only when a matching file is edited.

---

## Scenario C: Claude Code for Continuous Integration (Questions 31–45)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 31.** You're writing the GitHub Actions step that runs the automated review. It must run without any interactive input and emit output your comment-posting script can parse. Which invocation is correct?

- A) `claude "Review this PR" --interactive=false --format=structured`
- B) `claude -p "Review this PR" --output-format json --json-schema review-schema.json`
- C) `CLAUDE_HEADLESS=true claude "Review this PR" --parse`
- D) `claude --batch "Review this PR" > findings.json`

**Question 32.** Your pipeline generates code with Claude Code, then resumes the same session for the review step "so the reviewer understands why the code was written." The reviews almost never find issues, but human reviewers do. What should change?

- A) Add "be maximally critical of every changed line, including ones you would normally trust without a second look" to the review step's prompt instructions.
- B) Enable extended thinking for the review step so it reasons more deeply before commenting.
- C) Keep the shared session but have it review each file in the diff twice for good measure.
- D) Run the review as an independent instance with no access to the generation session's context, since retained reasoning discourages self-critique.

**Question 33.** The nightly test-generation job keeps proposing test scenarios that already exist in your spec files. What is the most direct fix?

- A) Provide the existing test files as context during generation and instruct Claude to propose only scenarios that aren't already covered by them.
- B) Run a deduplication pass afterward that compares generated test names against the existing test file's test names.
- C) Have Claude generate twice as many candidate tests using one few-shot example as a template, on the theory that a larger batch of proposals will contain at least a few genuinely novel scenarios.
- D) Limit test generation to newly created source files only, since those files can't already have tests written for them.

**Question 34.** Your senior engineers each keep excellent review criteria in their personal `~/.claude/CLAUDE.md` files. The CI runner's automated reviews follow none of these criteria. Why, and what is the fix?

- A) The CI runner just needs a `--memory` flag added to its invocation to load user-level CLAUDE.md files.
- B) The criteria files are too large for non-interactive mode; anything over 10KB gets silently skipped in CI.
- C) User-level CLAUDE.md lives in each engineer's home directory and never reaches the CI environment at all — move the criteria into the project-level CLAUDE.md in the repository instead, since the CI checkout includes that file.
- D) CI-invoked Claude Code can't read any CLAUDE.md file; criteria have to be passed in as prompt flags instead.

**Question 35.** Your CI review skill only needs to read code and report findings. A pipeline audit found one run where it executed `npm install` and modified `package-lock.json` in the workspace. What is the correct constraint?

- A) Run the entire CI job inside a container configured so that filesystem writes fail at the operating-system level, meaning nothing in the workspace can be modified by any process at all.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only read and reporting operations, so execution tools like Bash aren't available.
- C) Add "never install packages or modify any files" as an explicit instruction inside the skill's own prompt text.
- D) Add a `PostToolUse` hook that automatically reverts any workspace changes after the review step finishes running.

**Question 36.** Your 400-line review checklist currently lives in the root CLAUDE.md. Every interactive session pays its token cost, though it's only needed when reviews run. The checklist must stay identical for interactive `/review` use and CI. Where should it live?

- A) Split the 400-line checklist across ten smaller CLAUDE.md sections so no single block looks large.
- B) Keep the checklist in CLAUDE.md but add an instruction telling Claude to ignore its contents entirely outside of dedicated review sessions.
- C) Move the checklist to user-level CLAUDE.md so only the reviewers who set it up pay its token cost.
- D) Move the checklist into a review skill under `.claude/skills/`, loaded on demand, keeping it out of unrelated sessions.

**Question 37.** Your changelog-generation step turns merged-PR titles into release notes. The prose spec ("group by type, past tense, link each PR") is interpreted differently across runs — grouping and tense drift. What is the most effective fix?

- A) Add two or three concrete examples to the system prompt: sample commit lists paired with the exact changelog output expected for each.
- B) Rewrite the prose spec into a more structured, heavily bolded MUST-requirements format.
- C) Raise the sampling temperature so at least the resulting variation reads as more creative.
- D) Generate three separate drafts of the same changelog per run and have a second model read all three and pick whichever one complies best with the spec.

**Question 38.** You're using Claude to fix a data-transform module that intermittently fails in CI. You want an iteration loop that converges instead of whack-a-mole fixes. What is the best structure?

- A) Describe every known symptom of the intermittent failure in one message and ask for a single comprehensive fix.
- B) Ask Claude to review the entire module line by line, flag anything that looks even slightly suspicious, and fix all of it in one pass without a way to check whether the fix actually worked.
- C) Write a test suite first covering expected behavior, edge cases, and performance requirements, then iterate by sharing failing test output with Claude until the whole suite passes.
- D) Rewrite the module from scratch, on the theory that accumulated fixes are a sign of an unfixably bad design.

**Question 39.** You're about to build Claude Code into your deployment-approval flow — a domain with rollback semantics, partial-failure modes, and compliance constraints you haven't fully articulated. Which technique best surfaces the hidden requirements before implementation?

- A) Implement a minimal version first and let real production incidents reveal whatever requirements are missing.
- B) Use the interview pattern — have Claude ask you questions about failure modes and approval edge cases before you implement.
- C) Write the complete specification yourself, fully and in advance, covering every rollback and failure scenario, before involving Claude in the work at all.
- D) Copy a few-shot-engineered prompt template from a published blog post written by a team with a similar tech stack.

**Question 40.** Your review prompt has three problems that interact: the severity definitions conflict with the category definitions, which in turn contradict the output examples. Fixing them one at a time has caused regressions — each fix breaks under the next. How should you deliver the corrections?

- A) Fix the three problems in three sequential messages, verifying each fix works before moving to the next one.
- B) Rebuild the prompt from an empty file using a rigidly structured template, reintroducing every requirement one at a time.
- C) Open three parallel sessions, fix one of the three interacting problems in each, then manually merge whichever parts of each session's output look best.
- D) Address all three problems in one detailed message explaining how they interact, since interacting issues need fixing together.

**Question 41.** Before your CI can validate it, you must migrate the repo's test framework — 45+ files, several valid migration strategies, and infrastructure implications for the CI runners themselves. How should you begin in Claude Code?

- A) Enter plan mode to explore the codebase and settle on one migration approach before making any changes.
- B) Use direct execution and migrate the test framework file by file, since each individual file's change looks small in isolation.
- C) Ask Claude to generate one shell script that performs the entire migration mechanically in a single run.
- D) Fork 45 parallel sessions, one per file, to get through the migration as fast as possible.

**Question 42.** Generated tests cover happy paths well but consistently miss branch-level gaps — error paths, boundary conditions, early returns. Detailed instructions ("cover all branches, including error handling") haven't changed the behavior. What is the most effective next step?

- A) Raise the required coverage threshold in CI so pull requests with incomplete branch coverage fail automatically.
- B) Add one generic few-shot example of a happy-path test to the generation prompt, then ask for twice as many tests per function.
- C) Add few-shot examples showing how to spot a function's branch-level coverage gaps and write the tests that close them, demonstrating the analysis rather than just requesting it.
- D) Run a full mutation-testing pass across the suite, collect every mutant that survives, and feed the complete list of survivors back into the model for a dedicated follow-up generation pass.

**Question 43.** You're preparing your first Batch API run: overnight tech-debt analysis across 900 repositories with a prompt that has never been tested at scale. What should you do first?

- A) Submit all 900 repositories tonight and treat this untested first run as the real test, since batch pricing is already discounted 50% either way.
- B) Refine the prompt on a small sample using the synchronous API first, then submit the full batch once it performs well — this increases the odds of first-pass success.
- C) Split the run into two 450-repository halves so a bad prompt only wastes half of the overnight spend.
- D) Add an automatic retry wrapper that resubmits any repository whose analysis output looks wrong on inspection.

**Question 44.** Your overnight batch of 500 analysis requests completes with 38 failures, all caused by oversized diffs exceeding context limits. What is the correct recovery?

- A) Resubmit the entire 500-request batch with a larger context configuration applied to every request.
- B) Rerun just the 38 failed requests through the synchronous API completely unchanged, since it presumably handles oversized inputs better than batch.
- C) Drop the 38 failures — a 92% completion rate is within tolerance for an overnight job like this one.
- D) Identify the 38 failed requests by their `custom_id`, chunk the oversized diffs, and resubmit just those.

**Question 45.** You want the pipeline to auto-approve PRs the review bot deems clean, but only where that trust is justified. The bot can emit a confidence score per finding. What makes the confidence usable for routing?

- A) Calibrate it — collect a labeled set of past reviews with known outcomes and set thresholds from measured accuracy.
- B) Trust any score above 8 out of 10, since models are generally reliable at the extreme, most-confident ends of their scoring range.
- C) Ask the model to justify each confidence score in a structured paragraph, and trust the ones whose justification reads convincingly.
- D) Use PR size as the routing signal instead — small PRs are safe to auto-approve regardless of what the bot's confidence score says.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your extraction prompt asks Claude to "respond with a JSON object" in its text reply. About 7% of responses fail parsing — trailing commas, markdown code fences, explanatory text before the JSON. What is the most reliable fix?

- A) Add "Respond with ONLY raw JSON, no markdown, no commentary" as an explicit instruction in the prompt.
- B) Define an extraction tool whose input schema is your output structure and read the data from the `tool_use` block — this eliminates commas, fences, and preamble text as a failure class entirely, unlike merely lowering the temperature, which doesn't guarantee valid syntax.
- C) Strip code fences and trailing commas with a preprocessing regex before handing the text to the JSON parser.
- D) Switch the output format to XML instead, since it tolerates minor malformation better than JSON.

**Question 47.** Some invoices legitimately lack a PO number, but your schema marks `po_number` as required. Sampling reveals the model sometimes invents plausible-looking PO numbers for those invoices. What is the correct schema fix?

- A) Add a validation rule in the schema that rejects any PO number not matching your company's internal numbering format.
- B) Prompt the model to leave required fields as empty strings whenever the source data is actually missing.
- C) Cross-check every extracted PO number against the purchasing database afterward, and drop or flag any number that fails to match.
- D) Make `po_number` optional and nullable, and return null when it's absent, since required fields pressure fabrication.

**Question 48.** Your `document_type` enum is `["invoice", "receipt", "purchase_order"]`. New document types keep arriving (credit memos, delivery notes), and the model shoehorns them into the closest existing value. How should the schema evolve?

- A) Add an `"other"` enum value paired with a free-text detail field describing the actual document type.
- B) Remove the enum entirely and make `document_type` a free-text field so anything at all can be represented.
- C) Add every document type your entire industry could conceivably use to the enum, preemptively, before any of them ever actually arrive.
- D) Reject any document that doesn't match one of the three known types and queue it for a human to classify.

**Question 49.** You defined three extraction tools — `extract_invoice`, `extract_contract`, `extract_resume` — and documents arrive with unknown type. Sometimes the model responds with prose about the document instead of extracting. Which configuration guarantees structured output while letting the model pick the right schema?

- A) `tool_choice: {"type": "tool", "name": "extract_invoice"}` — force the single most common document type on every call.
- B) `tool_choice: "auto"` paired with a prompt instruction telling the model to always use a tool regardless.
- C) `tool_choice: "any"` — the model must call some tool on every turn, but it is free to select whichever extraction schema, invoice, contract, or resume, actually matches the document in front of it.
- D) Add a separate classification model upstream that routes each document to one forced single-tool call.

**Question 50.** Contract extractions repeatedly fail validation with `governing_law: null`. Sampling shows the governing-law clause typically lives in a master agreement referenced by, but not included with, the contracts you send. Will retry-with-error-feedback fix this?

- A) Yes — including the validation error in the retry will make the model look harder at the contract text it already has.
- B) Yes, but only with three or more retries and an escalating sampling temperature, on the theory that more attempts surface a clause the earlier passes simply missed.
- C) No — the governing-law field should just be dropped or normalized away from the schema, since it apparently can't be reliably extracted.
- D) No — retries can't recover information that was never present in the input; fix the pipeline to supply the master agreement, or accept null.

**Question 51.** Invoice line items sometimes don't sum to the stated total — occasionally an OCR artifact, occasionally a genuine source-document error. Downstream systems must not silently receive bad totals. What extraction design handles this?

- A) Have the model recompute the total from the line items itself and output that corrected value in place of the stated total.
- B) Extract `calculated_total`, the sum of the line items, alongside `stated_total`, and flag a conflict when they disagree.
- C) Reject any invoice where the line-item arithmetic doesn't add up and return it to the sender unprocessed.
- D) Trust `stated_total` in every single case, on the firm assumption that the original source document is always the authoritative record no matter what.

**Question 52.** Résumé extraction works well on standard corporate résumés but returns null for required-in-source fields on academic CVs and international formats, where the information exists but appears in unfamiliar sections. What is the most effective fix?

- A) Add few-shot examples demonstrating correct extraction from an academic CV and an international résumé format.
- B) Lengthen the schema's field descriptions so the model understands why each field matters more clearly.
- C) Run two separate extraction passes over the exact same document and merge whichever field values come back non-null across the two attempts.
- D) Preprocess every incoming document into one standardized layout before extraction ever begins.

**Question 53.** Source documents write dates as "3/4/25", "March 4th, 2025", and "04-03-2025" (ambiguous day/month order), while your schema requires ISO 8601. What should accompany the strict output schema?

- A) Add a post-processing date parser downstream of extraction that reinterprets and converts whatever raw, possibly ambiguous date string the model happened to output into ISO 8601.
- B) Loosen the schema to accept dates as free text instead, to be normalized later by a separate downstream step.
- C) Add format-normalization rules to the prompt: how to convert each source format to ISO 8601, how to resolve ambiguous day/month order from context, and when to mark a date unresolvable.
- D) Reject any document outright whose dates aren't already written in ISO 8601 format.

**Question 54.** Your extraction system reports 97% overall accuracy, and leadership wants to cut human review by 80%. What must you verify before agreeing?

- A) That the 97% figure was measured sometime recently, within the last full quarter, rather than considerably further back in time.
- B) That accuracy exceeds 97% specifically on the most recent week of processed documents.
- C) That reviewer headcount freed up by the cut can be reabsorbed into other teams.
- D) That accuracy holds up when segmented by document type and field, since a flat 97% can mask failure on one segment.

**Question 55.** You automated the pipeline for high-confidence extractions. Six months from now, how will you know whether new error patterns have crept into the extractions no human looks at?

- A) Implement stratified random sampling of high-confidence extractions for ongoing human review, measuring the error rate continuously and surfacing novel error patterns as they appear.
- B) Human review already covers the low-confidence extractions, so any new error pattern would naturally appear there first.
- C) Wait for downstream system failures or customer complaints to surface a problem before investigating it.
- D) Re-run the original validation benchmark once every quarter against the exact same fixed set of documents used when the pipeline first shipped, tracking the score over time.

**Question 56.** The model outputs a confidence score per extracted field, and you must choose the threshold above which fields skip human review. How should the threshold be set?

- A) Use 0.95 across the board — a conservative round number that leaves a comfortable safety margin.
- B) Let each reviewer team pick whatever threshold best matches its own current review workload.
- C) Calibrate against a labeled validation set — measure actual accuracy at each confidence level and choose thresholds where measured accuracy meets your requirement, set per field if performance varies field to field.
- D) Use the median confidence score across all fields, so roughly half of all extractions get routed to review.

**Question 57.** Your reviewers can inspect 500 documents daily out of 10,000 processed. Which routing strategy applies their capacity where the guide's reliability practices say it matters most?

- A) Review the 500 highest-dollar-value documents processed each day, on the reasoning that errors slipping through on high-value paperwork cost the business the most in the end.
- B) Route extractions with low model confidence, and those from ambiguous or contradictory source documents, to human review, prioritizing where errors are most likely to occur.
- C) Review a uniform random 5% of documents every day so every document type gets an equal audit probability.
- D) Review the newest documents first each day, since recently introduced formats are the least familiar to the model.

**Question 58.** Your extraction service supports a multi-turn correction chat: users point out extraction mistakes and the model revises. Users report the model "forgets" corrections from two turns earlier. The service sends each API request with only the latest user message. What is the fix?

- A) Add an instruction to the system prompt telling the model to remember every correction from every prior turn.
- B) Store each correction in a database and have the model retrieve past corrections through a lookup tool.
- C) Reduce each correction turn to touch only one field so there is less for the model to keep track of.
- D) Send the complete conversation history with every single API request — the API itself is stateless, so coherence across turns requires resending the full history each time, not just the latest message.

**Question 59.** Each extraction is enriched via a vendor-lookup MCP tool that returns 40+ fields per call, of which your workflow uses 5. Long enrichment sessions degrade noticeably and sometimes overflow context. What is the right fix?

- A) Trim the vendor-lookup tool's output to only the relevant fields before it accumulates in context.
- B) Add a `PreToolUse` hook that batches several vendors into a single call instead of calling the tool once per vendor.
- C) Move to a model with a much larger context window so it can absorb the verbose 40-field results without ever running into trouble.
- D) Add one few-shot example of a trimmed-down enrichment result, then summarize the conversation with `/compact` automatically after every ten calls.

**Question 60.** A nightly job must cross-reference 20 related documents in a single request (they reference each other, so they can't be processed separately). Fields sourced from documents in the middle of the concatenated input show markedly higher miss rates than those near the start and end. What is the best mitigation?

- A) Randomize the order the 20 documents are concatenated in each night, so no single document always lands in the middle.
- B) Duplicate every middle-positioned document a second time at the very end of the concatenated input, so each one that would otherwise sit buried in the middle also appears again near the end.
- C) Add a key-facts summary of all 20 documents at the beginning of the input, and organize the full documents underneath explicit, labeled section headers — mitigating the lost-in-the-middle position effect.
- D) Add an instruction telling the model that documents in the middle are equally important and should not be skipped.

---
# Answer Key — Practice Exam 2

**Quick key:** 1-C, 2-B, 3-A, 4-D, 5-B, 6-C, 7-A, 8-D, 9-B, 10-A, 11-C, 12-D, 13-A, 14-C, 15-B, 16-D, 17-A, 18-C, 19-B, 20-A, 21-D, 22-C, 23-B, 24-A, 25-C, 26-D, 27-B, 28-A, 29-C, 30-D, 31-B, 32-D, 33-A, 34-C, 35-B, 36-D, 37-A, 38-C, 39-B, 40-D, 41-A, 42-C, 43-B, 44-D, 45-A, 46-B, 47-D, 48-A, 49-C, 50-D, 51-B, 52-A, 53-C, 54-D, 55-A, 56-C, 57-B, 58-D, 59-A, 60-C

---

**1. C** — Loop termination should be driven by `stop_reason`: continue on `"tool_use"`, stop at `"end_turn"`, with iteration caps kept only as a backstop. A and D just tune or lean on a cap that stays the primary stopping mechanism — some task will exceed whatever number you pick. B has the coordinator guess a per-task number under the same flawed assumption that iteration count, not `stop_reason`, should drive the loop.

**2. B** — Fast-moving, open-ended topics need dynamic decomposition: subtasks generated from what each step actually discovers. Fixed pipelines can't chase angles that only emerge mid-research. A widens the fixed net with a bigger checklist but still can't adapt once research starts. C repeats the same blind pipeline twice. D — a bigger context window doesn't create searches that were never issued.

**3. A** — The coordinator chooses subagents based on their descriptions; "Research helper 1" gives it nothing to select on. Naming each subagent's specialization and trigger conditions fixes the root cause. B builds a brittle keyword table around a self-inflicted labeling problem instead of fixing the labels. C shrinks the option set rather than clarifying it. D (fine-tuning) is disproportionate for a description problem.

**4. D** — When prior tool results are stale, starting a new session with a structured summary of durable findings is more reliable than resuming — resumption is for when prior context is still mostly valid. A and B resume atop stale cached data and depend on the agent correctly guessing what changed. C preserves the stale baseline in both branches; forking is for exploring divergent approaches, not for restoring freshness.

**5. B** — Context passed between agents should use a structured format that separates content from metadata (source URL, document name, page number) precisely so attribution survives handoffs. A adds more manual checking but still funnels metadata through prose that can garble it later. C tries to reconstruct provenance after it was already destroyed. D reduces prose volume but not the structural fragility that caused the loss.

**6. C** — Subagents do not share memory between invocations; each invocation is independent and must receive all needed context explicitly in its prompt. A, B, and D invent mechanisms (tier-shared caches, cross-invocation context windows, a session-linking parameter) that don't describe how the Task tool actually works.

**7. A** — A `PostToolUse` hook that normalizes all providers into one shape, timestamp format, and score scale before the model sees the data removes the comparison errors deterministically. B relies on the model performing every conversion correctly, every time, from a documentation table. C sacrifices coverage to dodge an integration problem with a standard solution. D depends on external maintainers and won't ship this quarter.

**8. D** — Missing viewpoints are a coverage gap; only an iterative refinement loop — coordinator evaluates synthesis, re-delegates targeted searches, re-synthesizes — can gather material that was never collected in the first place. A mandates content the synthesis agent still doesn't have the material to produce. B papers over the gap with a caveat instead of closing it. C hopes higher volume incidentally includes balance.

**9. B** — The MCP `isError` flag is the mechanism for signaling tool failure; errors returned as ordinary content are indistinguishable from data, which is exactly why the agent quoted one as a finding. A is fragile string-matching layered on top of a protocol-level problem. C silently converts failure into "no results," which misleads the agent differently. D hides genuine failures behind invisible retries that can loop forever.

**10. A** — Machine-readable error metadata — `errorCategory: "permission"`, `isRetryable: false`, a human-readable description — tells the agent immediately that retrying is pointless and why, so it pivots right away. B explains the concept without giving the agent anything machine-actionable. C leans on HTTP status folklore instead of the MCP error contract the agent actually reads. D still invites a retry that can never succeed, just less often.

**11. C** — The recommended distribution: subagents handle transient failures locally (retry with backoff) and propagate only unresolvable errors, along with what was attempted and any partial results. That keeps coordinator context focused on coordination. A silently drops failed queries, corrupting research completeness. B routes every decision through an extra hop for choices best made locally where the failure happened. D reduces frequency without fixing the underlying distribution of responsibility.

**12. D** — There is no server switching to build: tools from all configured MCP servers are discovered at connection time and are simultaneously available, and selection happens through tool descriptions like any other tools. A, B, and C all build — or invent, since there is no `activeServer` field — machinery for a problem the protocol already solves on its own.

**13. A** — The report agent's role is rendering synthesized, vetted findings; search tools sit outside that role, and their misuse (uncited last-minute claims) is the predictable result. Scoping its tools to its role and routing real gaps back through the coordinator addresses the cause. B legitimizes bypassing the pipeline instead of closing it off. C reaches for a hook to clean up after the fact instead of removing the agent's ability to search in the first place. D catches contamination only after it has already shipped.

**14. C** — Requiring publication or collection dates in subagent outputs lets synthesis interpret differing figures as time-series data instead of contradictions. A is an arbitrary numeric heuristic that would also mask genuine conflicts above the threshold. B throws away valid historical data outright. D presents the confusion to the reader instead of resolving its actual cause.

**15. B** — Synthesis output should carry coverage annotations: which findings are well-supported and which topic areas have gaps because sources were unavailable. A and C leave readers unable to distinguish thin coverage from strong coverage. D is worse than a visible gap — it fills the hole with unsourced model knowledge inside a report that promises cited research.

**16. D** — `stop_reason: "tool_use"` means: execute the requested tool, append the result to the conversation as a tool result, and send the updated conversation back for the next iteration. That's the agentic loop. A abandons the task mid-loop. B re-sends the request without ever providing the result the model needs. C inserts a human approval step where none is required by the protocol.

**17. A** — Named session resumption is designed for exactly this: continuing a specific prior conversation whose context is still valid because nothing relevant changed. B discards the accumulated context that resumption exists to preserve. C forks branches for exploring divergent approaches, and there's nothing divergent to explore here. D conflates process uptime with the session persistence `--resume` already provides.

**18. C** — When resuming after code changed, tell the session which specific files changed so it can re-analyze just those; the rest of its context is still valid. A discards hours of still-valid work over two files. B leaves stale beliefs sitting in context to resurface unpredictably later. D — `/compact` summarizes conversation history; it doesn't re-read the two changed files from disk.

**19. B** — `fork_session` exists for exploring divergent approaches from a shared analysis baseline: two independent branches, each unbiased by the other's exploration, both grounded in the same prior understanding. A lets the first exploration's framing contaminate the second. C pays for the codebase analysis a second time. D produces an opinion without the independent exploration you actually asked for.

**20. A** — Open-ended tasks decompose best by mapping structure and risk, then building a plan that adapts as dependencies and surprises are discovered. B spends effort by filename rather than by risk, wasting time on low-value files. C is one unfocused pass over a large codebase, diluting attention everywhere. D uses recency as a proxy for importance, so critical old code stays untested.

**21. D** — Predictable, identical multi-stage workflows are the home ground of prompt chaining: a focused sequential pass per stage, each feeding the next. A crams four distinct concerns into a single pass and loses focus on each. B adds adaptive machinery to a workflow where nothing actually varies between services. C ignores the real data dependency — stage two needs stage one's output to describe anything.

**22. C** — A must-never-happen rule needs programmatic enforcement: a hook intercepting Bash calls and blocking destructive git patterns gives a deterministic guarantee regardless of prompt wording. A doubles down on prompt-based compliance, which already failed once. B trades away all shell capability to prevent two specific commands. D relies on developers reading and objecting to every command in real time.

**23. B** — Pre-configured sequences can't adapt to per-task variation; the case for model-driven behavior is that the model chooses tools from the actual task context each time. A and D just lengthen or reorder the script — some task will still break any fixed sequence. C swaps one tool inside a script whose real problem is being a script at all.

**24. A** — Finding files by their *contents* (an import statement) is Grep's job: search the codebase for the literal pattern. B (Glob) matches file *names*, which say nothing about what a file imports. C reads blindly at monorepo scale with no targeting. D enumerates filenames first, the same limitation as Glob with extra steps.

**25. C** — For standard integrations like Jira, an existing, maintained community MCP server is the default choice; custom server development is reserved for genuinely team-specific workflows. A spends engineering time re-solving an already-solved problem. B abandons MCP's typed tool interface for shell-and-curl fragility. D isn't an integration strategy at all, just a delay.

**26. D** — When Edit can't find a unique anchor, the documented fallback is to Read the full file, then Write it back with the modification applied at the right spot. A retries the exact same failure condition. B bypasses the harness's file tools for `sed` line-number surgery, which is easy to get subtly wrong. C makes an unrelated structural change to the file just to force a mechanical edit to succeed.

**27. B** — Build understanding incrementally: Grep for entry points, Read the relevant files, follow imports to trace the flow. That answers the question with a fraction of the context an exhaustive read would cost. A burns context on mostly-irrelevant files across 4,000 of them. C infers architecture instead of verifying it against the code. D assumes auth code is literally named "auth" — middleware, guards, and interceptors often say otherwise.

**28. A** — The agent keeps choosing Grep because it understands what Grep does; a three-word MCP description gives the semantic tool nothing to be selected on. Enhancing the description — capabilities, outputs, when it beats text search — is the documented fix for tool selection. B removes a tool that's still correct for exact-string searches. C is a blanket override that misroutes exact-match queries to the wrong tool. D — the agent isn't choosing based on latency at all.

**29. C** — A project-scoped `.mcp.json` is shared through version control, and `${GITHUB_TOKEN}` environment-variable expansion supplies each developer's own credential at runtime without ever committing a secret. A commits secrets directly into the repository. B isn't shared automatically — every developer has to configure it by hand. D puts a credential inside a context file; CLAUDE.md is instructions for the model, not secret storage.

**30. D** — A `.claude/rules/` file with `paths: ["**/*.tf"]` frontmatter loads the conventions only when a matching file is being edited — activation that works no matter which of the dozen directories the file sits in. A pays the token cost in every session regardless of relevance. B means a dozen copies of the same text to keep synchronized by hand. C loads only when a human remembers to invoke it first.

**31. B** — `-p` runs Claude Code non-interactively (print the result and exit), and `--output-format json` with `--json-schema` yields machine-parseable output conforming to your schema. A, C, and D are built from flags and environment variables that don't exist (`--interactive`, `CLAUDE_HEADLESS`, `--batch`).

**32. D** — A session that generated the code retains the reasoning that produced it and is unlikely to meaningfully question its own recent decisions; an independent review instance catches what self-review misses. The "understands why" intuition is precisely the source of the bias. A and B intensify a structurally biased review rather than removing the bias. C repeats the same biased pass twice.

**33. A** — Providing the existing test files in context and instructing generation to avoid already-covered scenarios addresses the cause directly — the model can't avoid duplicating tests it has never seen. B only catches literal name collisions, not scenarios that are semantically the same. C generates more duplicates alongside whatever novelty appears. D abandons improving coverage on existing code, which was the actual goal.

**34. C** — User-level CLAUDE.md lives in each engineer's home directory; the CI runner has no such files checked out. Project-level CLAUDE.md lives in the repository, so the CI checkout carries it. Moving the criteria there (which also shares them with the whole team) is the fix. A, B, and D describe flags and limits that don't exist in Claude Code.

**35. B** — `allowed-tools` in the skill's frontmatter removes execution tools from availability during the skill entirely — a structural guarantee that read-and-report is all it can do. A contains damage at the infrastructure layer but lets the harness attempt the misbehavior inside it. C is instruction-based and already failed once in this exact scenario. D reaches for a hook that cleans up after the fact instead of preventing the action from ever being available.

**36. D** — On-demand, task-specific content belongs in a skill: invoked identically by developers and by CI, and absent from every unrelated session. That's the dividing line between skills and CLAUDE.md (always-loaded universal standards versus on-demand workflows). A still loads the full checklist every session, just in smaller pieces. B pays the full cost and adds an instruction to ignore it. C hides team-shared review criteria inside one person's personal config.

**37. A** — When a prose spec is interpreted inconsistently, concrete input/output examples are the most effective correction — they show the exact grouping, tense, and linking expected instead of describing them abstractly. B is stronger wording around the same ambiguity. C deliberately increases the variation you're trying to remove. D spends three generations plus a judgment call to avoid writing two examples up front.

**38. C** — Test-driven iteration: write the suite covering expected behavior, edge cases, and performance first, then iterate by sharing failures. The tests define "done" and give each round an objective target to converge toward. A and B are single-shot or unfocused passes with no way to verify convergence. D discards working behavior on a hunch instead of using tests to isolate the actual defect.

**39. B** — The interview pattern is designed for unfamiliar domains with unarticulated constraints: Claude asks the questions that surface failure modes and edge cases you didn't think to specify yourself. A discovers requirements only after an incident in production. C assumes you can enumerate considerations you haven't anticipated — the exact gap the interview pattern closes. D imports another team's constraints instead of surfacing yours.

**40. D** — Interacting problems must be fixed together: one detailed message addressing all three and how they interrelate. Sequential fixes (A) are exactly what's already regressing — each fix optimizes against a context that's about to change again. B discards the working parts of the prompt along with the broken ones. C produces three separate prompts that each still contain two of the three unresolved conflicts.

**41. A** — Multi-file scope (45+), multiple valid strategies, and infrastructure implications are the plan-mode trifecta: explore, compare approaches, and commit to a design before changing anything. B starts changing files before any strategy has been chosen. C mechanizes a decision that was never actually made. D parallelizes execution without an agreed approach across 45 sessions and several competing strategies.

**42. C** — When detailed instructions fail to change behavior, few-shot examples demonstrating the analysis — here, spotting branch-level gaps and writing the tests that close them — teach the judgment so the model generalizes it. A fails PRs without ever improving the tests that fail them. B multiplies happy-path tests without addressing the actual gap. D is a real technique but heavier infrastructure than trying examples first.

**43. B** — Refining the prompt on a representative sample before committing to a large batch is what controls cost when a batch is 900 items and results can take hours to return. A risks 900 bad analyses and a full, expensive resubmission cycle. C halves the potential waste instead of preventing it. D automates resubmission of a prompt that was never validated in the first place.

**44. D** — Batch failure handling: identify failed requests by `custom_id`, fix the actual cause (chunk the oversized diffs), and resubmit only those. A re-pays for 462 already-successful analyses, and "larger context configuration" isn't a real batch setting. B re-sends the same oversized inputs into the same context limits. C silently drops the repositories most likely to carry the largest, most consequential diffs.

**45. A** — Self-reported confidence is only usable after calibration: measuring it against a labeled validation set with known outcomes and deriving thresholds from measured accuracy. B trusts raw self-report at face value, which is known to be poorly calibrated at the extremes too. C swaps a numeric self-report for a verbal one with the same reliability problem. D substitutes a weak proxy (size) for the measurement the question actually needs.

**46. B** — Tool use with a JSON schema is the reliable mechanism for structured output: the extraction "tool" call's input conforms to your schema, eliminating trailing commas, fences, and preambles as a failure class rather than reducing their frequency. A only reduces how often the failure occurs. C is an arms race against future formatting drift. D changes the syntax without adding any structural guarantee.

**47. D** — Required fields pressure the model to fabricate; fields that may legitimately be absent should be optional and nullable, with instructions to return null. That removes the incentive to invent a value at all. A rejects fabrications after the schema already invited them. B misuses empty strings as an informal null while keeping the same pressure in place. C is a downstream audit patching an upstream schema design problem.

**48. A** — The extensible-category pattern: an `"other"` enum value plus a free-text detail field. Novel document types are captured faithfully instead of being forced into the nearest wrong bucket. B loses the machine-readable categories downstream systems rely on for routing. C guesses at a future list and will still miss something. D turns every novel type into manual triage work.

**49. C** — `tool_choice: "any"` guarantees a tool call on every turn while leaving the choice of which tool to the model — exactly right when several extraction schemas exist and the document type isn't known in advance. A forces the invoice schema onto contracts and résumés alike. B ("auto") is what already permits the prose responses today. D adds a whole extra model and routing layer to replicate what "any" already does natively.

**50. D** — Retries correct format and structural errors; they cannot recover information that is simply absent from the provided input. The governing-law clause lives in a document the model never receives. Fixing the input pipeline, or handling the null explicitly, is the actual solution. A and B just retry harder at reading text that was never there. C deletes a business-required field because the pipeline is starving it of its source.

**51. B** — Extracting `calculated_total` alongside `stated_total` with a conflict flag is the self-correction design: discrepancies are surfaced for review, not silently passed through (as in D, which treats the source as infallible) or silently overwritten (as in A, which can hide a genuine source-document error that may matter legally). C treats every mismatch as a sender problem and halts the pipeline over what is sometimes just an OCR artifact.

**52. A** — Few-shot examples demonstrating extraction from varied document structures are the established fix for structure-driven misses — they show where the information lives in each unfamiliar format, and the model generalizes the pattern to further variants. B re-describes fields the model already understands the meaning of. C reruns the identical blind extraction twice and merges the same gaps. D presumes a reliable universal layout normalizer, which is really the original problem restated.

**53. C** — Strict output schemas should be paired with format-normalization rules in the prompt: how to map each source format to ISO 8601, how to disambiguate day/month order using context, and when to mark a value unresolvable. A pushes the ambiguity downstream to a parser with even less surrounding context than the model had. B just relocates the same unresolved problem. D rejects a large share of real-world documents outright.

**54. D** — Aggregate accuracy can mask severe failure on specific segments; before cutting review, verify accuracy by document type and by field. A flat 97% is entirely consistent with near-zero accuracy on one vendor's layout. A and B re-slice the same aggregate by time rather than by segment. C is a staffing question, not a validation of whether the automation is actually safe to trust more.

**55. A** — Stratified random sampling of high-confidence extractions gives ongoing error-rate measurement and catches novel error patterns in exactly the population no one otherwise inspects. B assumes new errors will conveniently arrive with low confidence attached — miscalibration means they often won't. C makes customers the QA process. D can't detect a pattern that didn't exist in the original benchmark set.

**56. C** — Review thresholds are set by calibrating confidence against a labeled validation set: measure real accuracy at each confidence level, per field where performance differs, and set the cutoff where accuracy meets your requirement. A and D are arbitrary numbers dressed up as caution. B sets thresholds by workload rather than by measured risk.

**57. B** — The reliability guidance: route low-confidence extractions and those from ambiguous or contradictory source documents to human review, spending scarce reviewer capacity where errors are most likely. A is a defensible business overlay but doesn't target where errors are most probable. C spreads capacity evenly over mostly-fine documents. D uses recency as a weak proxy for actual difficulty.

**58. D** — The API is stateless: conversational coherence requires sending the complete conversation history with every request. Sending only the latest message is precisely the bug. A instructs the model to remember context it was literally never sent. B rebuilds conversation memory as external infrastructure the API doesn't need. C shrinks each turn without restoring the missing history from prior turns.

**59. A** — Verbose tool outputs consume context disproportionately to how much of them the workflow actually uses; trimming to the relevant fields before results accumulate (tool-side or via a `PostToolUse` transformation) fixes the accumulation at its source. B changes call frequency, not the bloat per call. C delays the eventual overflow without addressing the degradation. D summarizes after the tokens are already spent, repeatedly.

**60. C** — This is the lost-in-the-middle effect. Since the 20 documents can't be split across separate requests, apply the position mitigations instead: a key-facts summary at the beginning and explicit, labeled section headers organizing the detail. A rotates which fields get missed rather than fixing the effect. B doubles the input size and still buries other documents in the middle. D — position effects aren't fixed by telling the model to try harder.

---

*End of Practice Exam 2.*
