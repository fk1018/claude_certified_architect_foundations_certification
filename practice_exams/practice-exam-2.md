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

- A) Raise the cap to 15 iterations, which covers the 95th percentile of observed task lengths.
- B) Have the coordinator estimate the required iterations up front and set the cap per task.
- C) Drive the loop from `stop_reason` — continue while it returns `"tool_use"` and stop at `"end_turn"` — and use budget limits only as a safety backstop, not the primary stopping mechanism.
- D) Prompt the coordinator to plan its work to fit within 5 iterations before starting.

**Question 2.** Your pipeline researches fast-moving topics using a fixed sequence: search three predetermined subtopics → analyze → synthesize. Reviews show reports keep missing important angles that only became apparent from the initial findings (e.g., a lawsuit that reframed an industry story). What should change?

- A) Increase the number of predetermined subtopics from three to eight to widen initial coverage.
- B) Use dynamic task decomposition — have the coordinator generate new subtasks based on what is discovered at each step, rather than fixing the subtopics before research begins.
- C) Run the same fixed pipeline twice and merge the two reports.
- D) Move to a model with a larger context window so more search results fit into the analysis step.

**Question 3.** Your coordinator frequently delegates document-analysis tasks to the web-search subagent. Reviewing the configuration, you find the subagents defined with descriptions like "Research helper 1" and "Research helper 2." What should you fix first?

- A) Rewrite each AgentDefinition description to state the subagent's specialization, capabilities, and when it should be chosen — the coordinator selects subagents based on these descriptions.
- B) Add a routing table to the coordinator's system prompt mapping task keywords to subagent numbers.
- C) Reduce the number of subagents so there are fewer wrong choices available.
- D) Fine-tune the coordinator on transcripts of correct delegation decisions.

**Question 4.** You want to continue a research project whose last session ran two weeks ago. Since then, several key sources have published updates, and the session's cached tool results reflect the old versions. What is the most reliable way to continue?

- A) Resume the session with `--resume` and add a note telling the agent some sources may have changed.
- B) Resume the session and re-run only the searches the agent decides look stale.
- C) Use `fork_session` to branch the old session so the stale results stay isolated in the parent.
- D) Start a new session and inject a structured summary of the durable findings, re-gathering current data fresh — resuming with stale tool results is less reliable than a clean start with a summary.

**Question 5.** The analysis subagent passes its findings to the coordinator as flowing prose paragraphs. By the time the synthesis agent works with them, source URLs are garbled and page numbers have disappeared. How should inter-agent context passing change?

- A) Instruct the analysis agent to double-check URLs before writing its prose summary.
- B) Use a structured data format that separates content from metadata — each finding carries its claim text plus dedicated fields for source URL, document name, and page number.
- C) Have the coordinator re-look-up the sources for any claims whose attribution was lost.
- D) Shorten the analysis agent's output so there is less prose in which details can get lost.

**Question 6.** A developer invokes the document-analysis subagent, then invokes it again with the prompt "Continue analyzing the paper from before." The agent responds that it has no paper to analyze. What explains this?

- A) The second invocation used a different model tier that cannot access the first invocation's cache.
- B) The subagent's context window overflowed between the two invocations.
- C) Subagent invocations are independent — subagents do not share memory between invocations, so all needed context (including the paper or prior findings) must be passed explicitly each time.
- D) The Task tool requires a `session_id` parameter to link consecutive invocations, and it was omitted.

**Question 7.** Your search subagent uses three search MCP servers. One nests results under an `items` key, timestamps differ in format across all three, and relevance scores are 0–1 in one server but 0–100 in the others. The agent visibly mis-ranks sources when comparing across providers. What is the cleanest fix?

- A) Implement a `PostToolUse` hook that normalizes all three providers' results into a common structure (shape, timestamp format, score scale) before the model processes them.
- B) Add a system prompt table documenting each provider's format so the agent converts scores when comparing.
- C) Use only the provider with the best format and drop the other two.
- D) Ask each provider's maintainer to adopt a common response schema.

**Question 8.** Reports on policy topics consistently lack opposing viewpoints. The pipeline makes a single pass, and the synthesis agent can only work with what was gathered. What is the most effective fix?

- A) Add "always include opposing viewpoints" to the synthesis agent's system prompt.
- B) Have the report agent add a caveats section acknowledging other views may exist.
- C) Double the search agent's result count so opposing sources are more likely to appear incidentally.
- D) Add a coordinator evaluation step that checks synthesis output for gaps (like missing viewpoints), re-delegates targeted searches to fill them, and re-invokes synthesis until coverage is sufficient.

**Question 9.** One search MCP tool reports failures as ordinary text — a successful-looking response whose content reads "ERROR: rate limited." Your agent has been observed quoting this string in reports as if it were a research finding. What is the correct tool-side fix?

- A) Prompt the agent to check search results for text beginning with "ERROR:" and disregard it.
- B) Return failures using the MCP `isError` flag with structured error content, so the agent recognizes a failure instead of ingesting it as data.
- C) Have the tool return an empty result set on failure so nothing wrong enters the context.
- D) Retry rate-limited requests inside the tool until they succeed, so the agent never sees an error.

**Question 10.** Logs show the agent retried a paywalled source six times in a row, failing identically each time, before moving on. The tool returns only "Access failed." What should the error response include to prevent this waste?

- A) Structured metadata: `errorCategory: "permission"`, `isRetryable: false`, and a description ("source requires subscription access") so the agent immediately pivots to alternatives.
- B) A longer error message explaining paywalls in more detail so the agent understands the concept.
- C) An HTTP 402 status code, which models recognize as payment-related.
- D) A `retryAfter` value of 24 hours so retries are at least spaced out.

**Question 11.** Every transient search timeout currently propagates to the coordinator, which spends context reasoning about each one; coordinator contexts fill with error-handling on long tasks. How should error handling be distributed?

- A) Suppress transient errors entirely — drop the failed query and let the coordinator work with whatever succeeded.
- B) Route all errors to a dedicated error-handling subagent that decides retries for the whole system.
- C) Have subagents recover locally from transient failures (retry with backoff), and propagate to the coordinator only errors they cannot resolve — including what was attempted and any partial results.
- D) Increase the search timeout so transient failures become rare.

**Question 12.** A teammate asks: "The research agent is connected to arxiv-mcp, news-mcp, and finance-mcp. Where do we build the router that switches the active server per task?" What is the correct answer?

- A) In a `PreToolUse` hook that inspects the task and enables the right server.
- B) In the coordinator's system prompt, with rules for when to activate each server.
- C) In `.mcp.json`, using the `activeServer` field to set a default and override it per session.
- D) Nowhere — tools from all configured MCP servers are discovered at connection time and are available simultaneously; the agent selects among them based on tool descriptions, so no server switching exists or is needed.

**Question 13.** The report-generation agent occasionally calls `web_search` while writing, adding last-minute uncited claims that never went through analysis or synthesis. What is the best fix?

- A) Remove search tools from the report agent's toolset — its role is to render synthesized findings — and have it flag genuine gaps back to the coordinator for proper re-research.
- B) Give the report agent a citation-generator tool so its additions at least carry sources.
- C) Add a system prompt rule: "Do not perform new research while writing the report."
- D) Run a fact-checking pass over final reports to catch unvetted additions.

**Question 14.** A report flags a "contradiction": one source says unemployment was 3.9%, another says 4.4%. Investigation shows the figures are from 2023 and 2025 — both correct for their time. How do you prevent this class of error?

- A) Instruct the synthesis agent to treat numeric differences under 1 percentage point as agreement.
- B) Have the search agent discard all sources more than a year old.
- C) Require subagents to include publication/data-collection dates in their structured outputs so temporal differences are interpreted as time-series data rather than contradictions.
- D) Present both numbers and let readers decide, with no annotation.

**Question 15.** During a research run, two topic areas couldn't be covered because key sources were unavailable. The final report presents all sections with equal apparent confidence. What should the synthesis output include?

- A) Nothing extra — the report should only contain what was found; absence of coverage is implied.
- B) Coverage annotations distinguishing findings that are well-supported from topic areas with gaps due to unavailable sources.
- C) A disclaimer paragraph stating that research has inherent limitations.
- D) Placeholder sections for the uncovered topics filled with the model's background knowledge.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses the built-in tools (Read, Write, Bash, Grep, Glob) and integrates with MCP servers.

---

**Question 16.** You are implementing the agent's request loop. A response arrives with `stop_reason: "tool_use"` containing a request to run Grep. What must your code do?

- A) Treat the turn as complete and display the assistant's text to the developer.
- B) Re-send the same request, since `"tool_use"` indicates the model needs another attempt.
- C) Ask the developer to approve continuing, since the model has paused.
- D) Execute the Grep call, append the result to the conversation as a tool result, and send the updated conversation back to Claude for the next iteration.

**Question 17.** An engineer is three days into investigating a legacy billing system, in a session she named. No relevant files have changed overnight. Each morning she wants to continue exactly where she left off. What should she do?

- A) Use `--resume` with the session name to continue the named session, since the prior context is still valid.
- B) Start a fresh session each morning and paste in her notes from the previous day.
- C) Use `fork_session` each morning so every day gets its own branch.
- D) Keep one terminal session running continuously for the whole investigation.

**Question 18.** You resume yesterday's analysis session, but you refactored two files last night after it ended. The resumed agent confidently describes the old versions of those files. The rest of its analysis is still accurate. What is the best course?

- A) Abandon the session and re-run the full multi-hour analysis from scratch.
- B) Keep working and correct the agent conversationally whenever it misremembers.
- C) Inform the resumed session which specific files changed and ask it to re-analyze just those, keeping the still-valid context.
- D) Run `/compact` so the summarization refreshes the agent's view of the files.

**Question 19.** After a thorough shared analysis of your codebase, you want to rigorously compare a Jest-to-Vitest migration against staying on Jest with upgraded tooling — explored independently so one exploration doesn't bias the other. What mechanism fits?

- A) Explore both options sequentially in the same session, then ask for a comparison.
- B) Use `fork_session` to create two independent branches from the shared analysis baseline, exploring one approach in each.
- C) Start two brand-new sessions, one per approach, and repeat the codebase analysis in each.
- D) Ask the agent to write a comparative essay on the two approaches without further exploration.

**Question 20.** You ask the agent to "add comprehensive tests to this legacy codebase" — a large, open-ended task. Which decomposition approach fits best?

- A) First map the codebase structure, identify high-impact and high-risk areas, then build a prioritized test plan that adapts as dependencies and surprises are discovered.
- B) Process files alphabetically, writing tests for each file before moving to the next, to guarantee complete coverage.
- C) Generate tests for the entire codebase in a single pass to keep style consistent.
- D) Only add tests to files changed in the last 90 days, since older code is stable.

**Question 21.** You're automating API documentation generation: extract endpoint signatures → describe each endpoint → generate request/response examples → cross-check descriptions against the code. The stages are the same for every service. How should this be structured?

- A) A single mega-prompt asking for finished documentation in one shot.
- B) Dynamic decomposition, letting the agent invent its approach per service.
- C) Four parallel subagents, one per stage, all running simultaneously.
- D) A fixed sequential prompt chain — one focused pass per stage feeding the next — since the workflow is predictable and identical across services.

**Question 22.** The productivity agent uses Bash. Policy: it must never run destructive git commands (`push --force`, `reset --hard`) against shared branches. It is CLAUDE.md-instructed today, but an incident still occurred. What is the correct guardrail?

- A) Strengthen the CLAUDE.md wording and add the rule to the agent's system prompt as well.
- B) Remove Bash from the agent entirely and accept the loss of all shell capability.
- C) Add a hook that intercepts Bash tool calls and blocks commands matching destructive git patterns against shared branches.
- D) Have the agent explain each git command before running it so developers can object.

**Question 23.** For "repetitive" boilerplate tasks, a teammate hardcoded the tool sequence Grep → Read → Write into the agent's loop. It works for the common case but fails when a task needs several related files read first, or none at all. What does this illustrate?

- A) The sequence is missing a Glob step at the beginning; a four-step script would be robust.
- B) Pre-configured tool sequences can't adapt to per-task variation — the model should decide which tools to call based on context, which is the point of model-driven agentic behavior.
- C) Grep should be replaced with an MCP code-search tool before scripting the sequence.
- D) The Write step should be split into Edit-then-Write for safety.

**Question 24.** You need to find every file that imports the deprecated `LegacyHttpClient` class across a large monorepo. Which built-in tool is right for the first step?

- A) Grep — search file contents for the import pattern across the codebase.
- B) Glob — match the files by name pattern.
- C) Read — read files one by one, checking imports.
- D) Bash `ls -R` — enumerate the tree, then inspect likely files.

**Question 25.** Your team needs Jira integration for the agent (create issues, query sprints — standard operations). An engineer proposes writing a custom MCP server for it. What is the better default guidance?

- A) Build the custom server — in-house servers are always more maintainable than third-party code.
- B) Skip MCP and have the agent call the Jira REST API directly through Bash and curl.
- C) Use an existing community MCP server for a standard integration like Jira, reserving custom server development for workflows specific to your team.
- D) Wait for Atlassian to embed Claude natively rather than integrating now.

**Question 26.** The agent tries to Edit a config block that appears verbatim in four places in one file, and Edit fails because the anchor text is not unique. What is the reliable fallback?

- A) Retry the Edit with the same anchor text but the `replace_all` option off.
- B) Use Bash `sed` to perform the replacement by line number.
- C) Delete the duplicate blocks first so the anchor becomes unique.
- D) Read the full file, then Write it back with the intended modification applied.

**Question 27.** An engineer asks the agent to explain how request authentication works in an unfamiliar 4,000-file service. Which exploration strategy should the agent use?

- A) Read every file under `src/` upfront so the explanation is grounded in complete knowledge.
- B) Start with Grep to find entry points (middleware registration, auth-related imports), then Read the relevant files, following imports to trace the flow incrementally.
- C) Rely on the repository README and directory names to infer the architecture.
- D) Glob for `*auth*` filenames and read only those files.

**Question 28.** Your team built a semantic code-search MCP server that outperforms text search for conceptual queries, but the agent almost always uses built-in Grep instead. Its description reads: "Searches code." What should you do?

- A) Enhance the MCP tool's description to explain in detail what it does (semantic/conceptual matching), what it returns, and when it beats plain text search — the agent is choosing tools based on descriptions, and Grep's purpose is better understood.
- B) Remove Grep from the agent's toolset so the MCP server is the only search option.
- C) Add a system prompt rule: "Always prefer MCP tools over built-in tools."
- D) Lower the MCP server's latency so the agent learns it is the faster option.

**Question 29.** You want the whole team to get your GitHub MCP server automatically when they pull the repo, authenticating with each developer's own token, without committing any secrets. How?

- A) Commit `.mcp.json` with each developer's token in a per-user section of the file.
- B) Have each developer configure the server in their personal `~/.claude.json`.
- C) Commit a project-scoped `.mcp.json` that references the token as `${GITHUB_TOKEN}`, expanded from each developer's environment at runtime.
- D) Store the token in CLAUDE.md, which is already shared through version control.

**Question 30.** Your infrastructure conventions apply only to Terraform files, which live in `terraform/` directories scattered across a dozen service folders. You want the conventions loaded only when Claude edits those files, without paying their token cost in every session. What is the right mechanism?

- A) Add the conventions to the root CLAUDE.md under a "Terraform" heading.
- B) Create a CLAUDE.md inside every one of the dozen `terraform/` directories.
- C) Create a `/terraform-rules` skill developers invoke before infrastructure work.
- D) Create a `.claude/rules/` file with YAML frontmatter `paths: ["**/*.tf"]` so the rules load only when matching files are edited.

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

- A) Add "be maximally critical of the changes" to the review step's prompt.
- B) Enable extended thinking for the review step so it reasons more deeply.
- C) Keep the shared session but review each file twice.
- D) Run the review as an independent instance without the generation session's context — a model that retains its own generation reasoning is unlikely to question its own decisions.

**Question 33.** The nightly test-generation job keeps proposing test scenarios that already exist in your spec files. What is the most direct fix?

- A) Provide the existing test files in the generation context and instruct Claude to propose only scenarios not already covered.
- B) Run a deduplication pass comparing generated test names against existing test names.
- C) Have Claude generate twice as many tests so at least some are novel.
- D) Limit generation to newly created source files, which cannot have tests yet.

**Question 34.** Your senior engineers each keep excellent review criteria in their personal `~/.claude/CLAUDE.md` files. The CI runner's automated reviews follow none of these criteria. Why, and what is the fix?

- A) The CI runner needs the `--memory` flag to load user-level CLAUDE.md files.
- B) The criteria files are too large for non-interactive mode; they need to be under 10KB.
- C) User-level CLAUDE.md lives in each engineer's home directory and never reaches the CI environment — move the criteria into the project-level CLAUDE.md in the repository, which the CI checkout includes.
- D) CI-invoked Claude Code cannot read CLAUDE.md at all; criteria must be passed as prompt flags.

**Question 35.** Your CI review skill only needs to read code and report findings. A pipeline audit found one run where it executed `npm install` and modified `package-lock.json` in the workspace. What is the correct constraint?

- A) Run the CI job in a container where writes fail at the filesystem level.
- B) Configure `allowed-tools` in the skill's frontmatter to permit only read and reporting operations, so execution tools aren't available at all.
- C) Add "never install packages or modify files" to the skill's instructions.
- D) Have the pipeline revert any workspace changes after the review step.

**Question 36.** Your 400-line review checklist currently lives in the root CLAUDE.md. Every interactive session pays its token cost, though it's only needed when reviews run. The checklist must stay identical for interactive `/review` use and CI. Where should it live?

- A) Split it across ten smaller CLAUDE.md sections so no single block is large.
- B) Keep it in CLAUDE.md but instruct Claude to ignore it outside reviews.
- C) Move it to user-level CLAUDE.md so only reviewers pay the cost.
- D) Move it into a review skill under `.claude/skills/` — loaded on demand when invoked by developers or CI, keeping it out of unrelated sessions.

**Question 37.** Your changelog-generation step turns merged-PR titles into release notes. The prose spec ("group by type, past tense, link each PR") is interpreted differently across runs — grouping and tense drift. What is the most effective fix?

- A) Add 2–3 concrete examples to the prompt: sample input commit lists with the exact changelog output expected for each.
- B) Rewrite the spec with stricter language and bolded MUST requirements.
- C) Raise the temperature so at least the variation is creative.
- D) Generate three drafts per run and have a second model choose the most compliant.

**Question 38.** You're using Claude to fix a data-transform module that intermittently fails in CI. You want an iteration loop that converges instead of whack-a-mole fixes. What is the best structure?

- A) Describe all known symptoms and ask for one comprehensive fix.
- B) Ask Claude to review the module line by line and fix everything suspicious.
- C) Write a test suite first covering expected behavior, edge cases, and performance requirements; then iterate by sharing failing test output with Claude until the suite passes.
- D) Rewrite the module from scratch, since accumulated fixes indicate unfixable design.

**Question 39.** You're about to build Claude Code into your deployment-approval flow — a domain with rollback semantics, partial-failure modes, and compliance constraints you haven't fully articulated. Which technique best surfaces the hidden requirements before implementation?

- A) Implement a minimal version first and let production incidents reveal the missing requirements.
- B) Use the interview pattern — have Claude ask you questions about the flow (failure modes, rollback triggers, approval edge cases) to surface considerations you haven't anticipated, then implement.
- C) Write the complete specification yourself before involving Claude at all.
- D) Copy the integration design from a published blog post by a team with a similar stack.

**Question 40.** Your review prompt has three problems that interact: the severity definitions conflict with the category definitions, which in turn contradict the output examples. Fixing them one at a time has caused regressions — each fix breaks under the next. How should you deliver the corrections?

- A) Fix them in three sequential messages, verifying each fix before the next.
- B) Rebuild the prompt from an empty file, reintroducing requirements one by one.
- C) Open three parallel sessions, fixing one problem in each, then merge the best parts.
- D) Address all three in a single detailed message explaining each problem and how they interact — interacting issues need to be fixed together, not sequentially.

**Question 41.** Before your CI can validate it, you must migrate the repo's test framework — 45+ files, several valid migration strategies, and infrastructure implications for the CI runners themselves. How should you begin in Claude Code?

- A) Enter plan mode to explore the codebase, compare migration strategies, and settle the approach before making any changes.
- B) Use direct execution file by file, since each individual file change is small.
- C) Ask Claude to generate a shell script that performs the whole migration mechanically.
- D) Fork 45 parallel sessions, one per file, to complete the migration fastest.

**Question 42.** Generated tests cover happy paths well but consistently miss branch-level gaps — error paths, boundary conditions, early returns. Detailed instructions ("cover all branches, including error handling") haven't changed the behavior. What is the most effective next step?

- A) Raise the coverage threshold in CI so incomplete test PRs fail automatically.
- B) Switch the generation prompt to ask for twice as many tests per function.
- C) Add few-shot examples that demonstrate identifying a function's branch-level coverage gaps and writing the specific tests that close them — showing the analysis, not just requesting it.
- D) Run mutation testing and feed surviving mutants back for another pass.

**Question 43.** You're preparing your first Batch API run: overnight tech-debt analysis across 900 repositories with a prompt that has never been tested at scale. What should you do first?

- A) Submit all 900 and treat the first run as the test — batch costs are already discounted 50%.
- B) Refine the prompt on a small representative sample using the synchronous API first, then submit the full batch — maximizing first-pass success avoids expensive iterative resubmission of 900-item batches.
- C) Split the batch into two 450-repo halves so a bad prompt only wastes half the spend.
- D) Add a retry wrapper that automatically resubmits any repo whose analysis looks wrong.

**Question 44.** Your overnight batch of 500 analysis requests completes with 38 failures, all caused by oversized diffs exceeding context limits. What is the correct recovery?

- A) Resubmit the full 500-request batch with a larger context configuration.
- B) Rerun the 38 through the synchronous API unchanged, since it handles large inputs better.
- C) Drop the 38 — a 92% completion rate is within tolerance for a nightly job.
- D) Identify the failed requests by `custom_id`, chunk their oversized diffs, and resubmit only those 38 as a follow-up batch.

**Question 45.** You want the pipeline to auto-approve PRs the review bot deems clean, but only where that trust is justified. The bot can emit a confidence score per finding. What makes the confidence usable for routing?

- A) Calibrate it: collect a labeled validation set of past reviews with known outcomes, measure how the model's self-reported confidence maps to actual accuracy, and set routing thresholds from that data.
- B) Trust scores above 8/10, since models are generally reliable at the extremes.
- C) Ask the model to justify each confidence score, and trust the ones with good justifications.
- D) Use PR size instead — small PRs are safe to auto-approve regardless of bot confidence.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your extraction prompt asks Claude to "respond with a JSON object" in its text reply. About 7% of responses fail parsing — trailing commas, markdown code fences, explanatory text before the JSON. What is the most reliable fix?

- A) Add "Respond with ONLY raw JSON, no markdown, no commentary" to the prompt.
- B) Define an extraction tool whose input schema is your output structure and read the data from the `tool_use` block — tool use with JSON schemas eliminates this class of syntax error.
- C) Strip code fences and trailing commas with a preprocessing regex before parsing.
- D) Switch the output format to XML, which tolerates minor malformation better.

**Question 47.** Some invoices legitimately lack a PO number, but your schema marks `po_number` as required. Sampling reveals the model sometimes invents plausible-looking PO numbers for those invoices. What is the correct schema fix?

- A) Add a validation rule that rejects PO numbers not matching your company's format.
- B) Prompt the model to leave required fields as empty strings when data is missing.
- C) Cross-check every extracted PO number against the purchasing database and drop mismatches.
- D) Make `po_number` optional/nullable and instruct the model to return null when the document doesn't contain one — required fields pressure the model to fabricate values.

**Question 48.** Your `document_type` enum is `["invoice", "receipt", "purchase_order"]`. New document types keep arriving (credit memos, delivery notes), and the model shoehorns them into the closest existing value. How should the schema evolve?

- A) Add an `"other"` enum value paired with a free-text detail field describing the actual type, so novel categories are captured rather than misclassified.
- B) Remove the enum and make `document_type` free text so anything can be represented.
- C) Add every document type your industry uses to the enum preemptively.
- D) Reject any document that doesn't match the three known types and queue it for humans.

**Question 49.** You defined three extraction tools — `extract_invoice`, `extract_contract`, `extract_resume` — and documents arrive with unknown type. Sometimes the model responds with prose about the document instead of extracting. Which configuration guarantees structured output while letting the model pick the right schema?

- A) `tool_choice: {"type": "tool", "name": "extract_invoice"}` — force the most common type.
- B) `tool_choice: "auto"` with a prompt instruction to always use a tool.
- C) `tool_choice: "any"` — the model must call some tool, and it selects the appropriate extraction schema based on the document.
- D) A separate classification model that routes each document to a forced single-tool call.

**Question 50.** Contract extractions repeatedly fail validation with `governing_law: null`. Sampling shows the governing-law clause typically lives in a master agreement referenced by, but not included with, the contracts you send. Will retry-with-error-feedback fix this?

- A) Yes — include the validation error and the model will look harder at the contract text.
- B) Yes, but only with 3+ retries and escalating temperature to explore more readings.
- C) No — the field should be dropped from the schema since it cannot be extracted.
- D) No — retries cannot recover information absent from the provided input; fix the pipeline to supply the master agreement, or accept null and route these documents appropriately.

**Question 51.** Invoice line items sometimes don't sum to the stated total — occasionally an OCR artifact, occasionally a genuine source-document error. Downstream systems must not silently receive bad totals. What extraction design handles this?

- A) Have the model recompute the total from line items and output the corrected value in place of the stated one.
- B) Extract `calculated_total` (sum of line items) alongside `stated_total`, and set a `conflict_detected` flag when they disagree, so discrepancies are surfaced for review rather than silently passed through or silently corrected.
- C) Reject any invoice where the arithmetic fails and return it to the sender.
- D) Trust `stated_total` always — the document is the source of truth.

**Question 52.** Résumé extraction works well on standard corporate résumés but returns null for required-in-source fields on academic CVs and international formats, where the information exists but appears in unfamiliar sections. What is the most effective fix?

- A) Add few-shot examples demonstrating correct extraction from the varied formats — an academic CV, an international format — showing where the fields live in each structure.
- B) Lengthen the field descriptions in the schema so the model knows the fields matter.
- C) Run two extraction passes and merge the non-null values from each.
- D) Preprocess all documents into a standardized layout before extraction.

**Question 53.** Source documents write dates as "3/4/25", "March 4th, 2025", and "04-03-2025" (ambiguous day/month order), while your schema requires ISO 8601. What should accompany the strict output schema?

- A) A post-processing date parser that converts whatever the model outputs.
- B) A looser schema accepting dates as free text, normalized downstream.
- C) Format normalization rules in the prompt — how to convert each source format to ISO 8601, how to resolve ambiguous orderings (e.g., from document context), and when to mark a date as unresolvable.
- D) Rejection of documents whose dates aren't already ISO 8601.

**Question 54.** Your extraction system reports 97% overall accuracy, and leadership wants to cut human review by 80%. What must you verify before agreeing?

- A) That the 97% was measured within the last quarter.
- B) That accuracy exceeds 97% on the most recent week of documents specifically.
- C) That reviewer headcount can be reabsorbed elsewhere if the cut proceeds.
- D) That accuracy holds up when segmented by document type and by field — aggregate metrics can mask near-total failure on specific segments (e.g., one vendor's invoice layout) that a flat 97% hides.

**Question 55.** You automated the pipeline for high-confidence extractions. Six months from now, how will you know whether new error patterns have crept into the extractions no human looks at?

- A) Implement stratified random sampling of high-confidence extractions for ongoing human review — measuring the error rate continuously and surfacing novel error patterns.
- B) Human review already covers the low-confidence extractions; errors would appear there first.
- C) Wait for downstream system failures or customer complaints to flag problems.
- D) Re-run the original validation benchmark quarterly against the same benchmark documents.

**Question 56.** The model outputs a confidence score per extracted field, and you must choose the threshold above which fields skip human review. How should the threshold be set?

- A) Use 0.95 — a conservative round number leaves a safety margin.
- B) Let each reviewer team pick the threshold that matches their workload.
- C) Calibrate against a labeled validation set — measure actual accuracy at each confidence level and choose thresholds where measured accuracy meets your requirement, per field if performance varies.
- D) Use the median confidence across all fields so half of extractions get reviewed.

**Question 57.** Your reviewers can inspect 500 documents daily out of 10,000 processed. Which routing strategy applies their capacity where the guide's reliability practices say it matters most?

- A) Review the 500 highest-dollar-value documents, since errors there cost the most.
- B) Route extractions with low model confidence and those from ambiguous or contradictory source documents to review — prioritizing where errors are most likely.
- C) Review a uniform random 5% so every document type has equal audit probability.
- D) Review the newest documents first, since recent formats are least familiar to the model.

**Question 58.** Your extraction service supports a multi-turn correction chat: users point out extraction mistakes and the model revises. Users report the model "forgets" corrections from two turns earlier. The service sends each API request with only the latest user message. What is the fix?

- A) Add a system prompt instruction telling the model to remember all prior corrections.
- B) Store corrections in a database and have the model query them through a tool.
- C) Reduce each correction turn to one field so there is less to forget.
- D) Send the complete conversation history in every API request — the API is stateless, and coherence across turns requires the full history each time.

**Question 59.** Each extraction is enriched via a vendor-lookup MCP tool that returns 40+ fields per call, of which your workflow uses 5. Long enrichment sessions degrade noticeably and sometimes overflow context. What is the right fix?

- A) Trim the tool output to the relevant fields before it accumulates in context (tool-side, or via a PostToolUse transformation), since verbose tool results consume tokens disproportionately to their relevance.
- B) Call the vendor-lookup tool less often by batching several vendors per call.
- C) Move to a model with a larger context window to absorb the verbose results.
- D) Summarize the conversation with /compact after every ten enrichments.

**Question 60.** A nightly job must cross-reference 20 related documents in a single request (they reference each other, so they can't be processed separately). Fields sourced from documents in the middle of the concatenated input show markedly higher miss rates than those near the start and end. What is the best mitigation?

- A) Randomize document order nightly so no document is always in the middle.
- B) Duplicate the middle documents at the end of the input so they appear twice.
- C) Add a key-facts summary of all 20 documents at the beginning of the input and organize the full documents under explicit, labeled section headers — mitigating the lost-in-the-middle position effect.
- D) Instruct the model: "Documents in the middle are equally important; do not skip them."

---
# Answer Key — Practice Exam 2

**Quick key:** 1-C, 2-B, 3-A, 4-D, 5-B, 6-C, 7-A, 8-D, 9-B, 10-A, 11-C, 12-D, 13-A, 14-C, 15-B, 16-D, 17-A, 18-C, 19-B, 20-A, 21-D, 22-C, 23-B, 24-A, 25-C, 26-D, 27-B, 28-A, 29-C, 30-D, 31-B, 32-D, 33-A, 34-C, 35-B, 36-D, 37-A, 38-C, 39-B, 40-D, 41-A, 42-C, 43-B, 44-D, 45-A, 46-B, 47-D, 48-A, 49-C, 50-D, 51-B, 52-A, 53-C, 54-D, 55-A, 56-C, 57-B, 58-D, 59-A, 60-C

---

**1. C** — Loop termination must be driven by `stop_reason`, not iteration counts: continue on `"tool_use"`, stop at `"end_turn"`. Caps are acceptable only as safety backstops. A and B just tune a cap that remains the primary stopping mechanism — some task will always exceed it. D asks the model to fit its work to an arbitrary limit rather than fixing the control flow.

**2. B** — Fast-moving, open-ended topics need dynamic decomposition: subtasks generated from what each step actually discovers. Fixed pipelines can't chase angles that only emerge mid-research. A widens the fixed net but still can't adapt. C repeats the same blindness twice. D — window size doesn't create searches that were never issued.

**3. A** — The coordinator chooses subagents based on their AgentDefinition descriptions; "Research helper 1" gives it nothing to select on. Clear specialization descriptions fix the root cause. B builds brittle keyword routing around a self-inflicted problem. C reduces options rather than clarifying them. D (fine-tuning) is out of scope and wildly disproportionate.

**4. D** — When prior tool results are stale, starting a new session with a structured summary of durable findings is more reliable than resuming — resumption is for when prior context is mostly valid. A and B resume atop stale data and depend on the agent correctly guessing what changed. C preserves the stale baseline in both branches; forking is for exploring divergent approaches, not freshness.

**5. B** — Context passed between agents should use structured formats that separate content from metadata (source URL, document name, page number) precisely so attribution survives handoffs. A still funnels metadata through prose. C tries to reconstruct provenance after it was destroyed. D reduces prose volume but not the structural fragility.

**6. C** — Subagents do not share memory between invocations; each invocation is independent and must receive all needed context explicitly in its prompt. A, B, and D invent mechanisms (tier-shared caches, cross-invocation windows, a session-linking parameter) that don't describe how the Task tool works.

**7. A** — A `PostToolUse` hook normalizing all providers into one shape/scale/format before the model sees the data removes the comparison errors deterministically. B relies on the model performing conversions correctly every time. C sacrifices coverage to avoid an integration problem with a standard solution. D is out of your control and doesn't ship this quarter.

**8. D** — Missing viewpoints are a coverage gap; only an iterative refinement loop — coordinator evaluates synthesis, re-delegates targeted searches, re-synthesizes — can gather material that was never collected. A asks synthesis to include content it doesn't have. B papers over the gap with a disclaimer. C hopes volume incidentally includes balance.

**9. B** — The MCP `isError` flag is the mechanism for signaling tool failure; errors returned as ordinary content are indistinguishable from data, which is exactly why the agent quoted one. A is fragile string-matching over a protocol problem. C silently converts failure into "no results," misleading the agent differently. D hides genuine failures and can retry forever.

**10. A** — Structured error metadata — `errorCategory: "permission"`, `isRetryable: false`, a human-readable description — tells the agent immediately that retrying is pointless and why, so it pivots. B explains without machine-actionable structure. C leans on HTTP folklore instead of the MCP error contract. D still invites a retry that can never succeed.

**11. C** — The recommended distribution: subagents handle transient failures locally (retry/backoff) and propagate only unresolvable errors, with what was attempted and partial results. That keeps coordinator context for coordination. A silently suppresses errors — an anti-pattern that corrupts research completeness. B adds a communication hop for decisions best made where the failure happened. D reduces frequency without fixing the architecture.

**12. D** — There is no server switching: tools from all configured MCP servers are discovered at connection time and are simultaneously available; selection happens through tool descriptions like any other tools. A, B, and C all build (or invent — there is no `activeServer` field) machinery for a problem the protocol already solves.

**13. A** — The report agent's role is rendering synthesized, vetted findings; search tools are outside its specialization and their misuse (uncited last-minute claims) is the predictable result. Scope its tools to its role and route real gaps back through the coordinator. B legitimizes bypassing the pipeline. C is probabilistic — the behavior already occurs. D catches contamination after the fact.

**14. C** — Requiring publication/collection dates in structured outputs lets synthesis interpret differing figures as time-series data instead of contradictions. A is an arbitrary numeric heuristic that would also mask genuine conflicts. B throws away valid historical data. D presents the confusion to the reader instead of resolving its cause.

**15. B** — Synthesis output should carry coverage annotations: which findings are well-supported and which topic areas have gaps due to unavailable sources. A and C leave readers unable to distinguish thin coverage from strong coverage. D is worse than a gap — it fills the hole with unsourced model knowledge in a system that promises cited research.

**16. D** — `stop_reason: "tool_use"` means: execute the requested tool, append the result to the conversation as a tool result, and send it back for the next iteration. That's the agentic loop. A abandons the task mid-loop. B re-sends without providing the result the model asked for. C inserts a human where none is required.

**17. A** — Named session resumption (`--resume <session-name>`) is designed for exactly this: continuing a specific prior conversation whose context is still valid (no relevant files changed). B discards accumulated context that resumption preserves. C forks branches with no divergent approaches to explore. D conflates process uptime with session persistence.

**18. C** — When resuming after code modifications, inform the session which specific files changed for targeted re-analysis; the rest of the context is still valid. A re-spends hours to refresh two files. B leaves stale beliefs in context to resurface later. D — `/compact` summarizes conversation history; it doesn't re-read changed files.

**19. B** — `fork_session` exists for exploring divergent approaches from a shared analysis baseline: two independent branches, each unbiased by the other's exploration, both grounded in the same understanding. A lets the first exploration contaminate the second. C pays for the codebase analysis twice. D produces opinion without the exploration you asked for.

**20. A** — Open-ended tasks decompose best by mapping structure, identifying high-impact areas, and building a prioritized plan that adapts as dependencies are discovered. B spends effort by filename rather than by risk. C is one unfocused pass over a large codebase — attention dilution. D uses recency as a proxy for importance; critical old code stays untested.

**21. D** — Predictable, identical multi-stage workflows are the home ground of prompt chaining: focused sequential passes, each feeding the next. A crams four concerns into one pass and loses focus. B adds adaptive machinery where nothing varies. C ignores the data dependency — stage 2 needs stage 1's output.

**22. C** — A must-never-happen rule needs programmatic enforcement: a hook intercepting Bash calls and blocking destructive git patterns gives a deterministic guarantee. A doubles down on prompt-based compliance, which already failed. B trades away all shell capability to avoid two commands. D relies on developers reading every command in time.

**23. B** — Pre-configured sequences fail on per-task variation; the case for model-driven behavior is that the model chooses tools based on the actual task context. A and D just lengthen or reshuffle the script — some task will break any fixed sequence. C swaps one tool inside a script whose problem is being a script.

**24. A** — Finding files by their *contents* (an import statement) is Grep's job: search the codebase for the pattern. B (Glob) matches file *names*, which tell you nothing about imports. C reads blindly at monorepo scale. D enumerates names, same limitation as Glob with more steps.

**25. C** — For standard integrations like Jira, existing community MCP servers are the default; custom server development is reserved for team-specific workflows. A spends engineering time re-solving a solved problem. B abandons MCP's typed tool interface for shell-and-curl fragility. D isn't an integration strategy.

**26. D** — When Edit can't find a unique anchor, the documented fallback is Read the full file, then Write it back with the modification applied. A retries the exact failure. B bypasses the harness's file tools for `sed` line-number surgery — easy to get subtly wrong. C makes semantic changes to the file just to enable a mechanical edit.

**27. B** — Build understanding incrementally: Grep for entry points, Read the relevant files, follow imports to trace the flow. That answers the question with minimal context spend. A exhausts context on mostly-irrelevant files. C infers instead of verifying. D assumes auth code is named "auth" — middleware, guards, and interceptors say otherwise.

**28. A** — The agent prefers Grep because it understands what Grep does; a three-word MCP description gives the semantic tool no case for selection. Enhancing the description — capabilities, outputs, when it beats text search — is the documented fix. B removes a tool that's still right for exact-string searches. C is a blanket rule that misroutes exact-match queries. D — the agent isn't choosing on latency.

**29. C** — Project-scoped `.mcp.json` is shared via version control, and `${GITHUB_TOKEN}` environment-variable expansion supplies each developer's own credential at runtime without committing secrets. A commits secrets. B isn't shared — every developer configures by hand. D puts a credential in a context file; CLAUDE.md is instructions, not secret storage.

**30. D** — A `.claude/rules/` file with `paths: ["**/*.tf"]` frontmatter loads the conventions only when matching files are edited — glob-based activation that works no matter which directories the files sit in. A pays the token cost in every session. B means a dozen files to keep synchronized. C loads only when a human remembers to invoke it.

**31. B** — `-p` runs Claude Code non-interactively (print result and exit), and `--output-format json` with `--json-schema` yields machine-parseable, schema-conforming output. A, C, and D are built from flags and environment variables that don't exist (`--interactive`, `CLAUDE_HEADLESS`, `--batch`).

**32. D** — A session that generated the code retains the reasoning that produced it and is unlikely to question its own decisions; independent review instances catch what self-review misses. The "understands why" intuition is precisely the bias. A and B intensify a structurally biased review. C repeats it.

**33. A** — Provide the existing test files in context and instruct generation to avoid scenarios already covered — the model can't avoid duplicating tests it has never seen. B catches only name collisions, not semantic duplicates. C generates more duplicates alongside the novelty. D abandons coverage improvement for existing code, which was the point.

**34. C** — User-level CLAUDE.md lives in each engineer's home directory; the CI runner has no such files. Project-level CLAUDE.md is in the repository, so the CI checkout carries it. The fix is moving the criteria there (which also shares them with the whole team). A, B, and D describe flags and limits that don't exist.

**35. B** — `allowed-tools` in the skill frontmatter removes execution tools from availability during the skill — a structural guarantee that read-and-report is all it can do. A contains damage at the infrastructure layer but lets the harness misbehave inside it. C is instruction-based and already failed once. D cleans up afterward instead of preventing.

**36. D** — On-demand, task-specific content belongs in a skill: invoked identically by developers and CI, absent from unrelated sessions. That's the skills-vs-CLAUDE.md dividing line (always-loaded universal standards vs. on-demand workflows). A still loads everything, just in pieces. B pays full cost and adds an ignore instruction. C hides team-shared material in personal config.

**37. A** — When prose specs are interpreted inconsistently, concrete input/output examples are the most effective correction — they show the exact grouping, tense, and linking expected. B is stronger prose with the same ambiguity. C increases variation deliberately. D spends three generations plus a judgment call to avoid writing two examples.

**38. C** — Test-driven iteration: write the suite covering expected behavior, edge cases, and performance first, then iterate by sharing failures. The tests define "done" and each round has an objective target. A and B are single-shot or unfocused passes with no convergence criterion. D throws away working behavior on a hunch.

**39. B** — The interview pattern is designed for unfamiliar domains with unarticulated constraints: Claude asks the questions that surface failure modes and edge cases you didn't think to specify. A discovers requirements via incidents. C assumes you can enumerate considerations you haven't anticipated — the exact gap. D imports another team's constraints, not yours.

**40. D** — Interacting problems must be fixed together: one detailed message addressing all three and how they interrelate. Sequential fixes (A) are what's already regressing — each fix optimizes against soon-to-change context. B discards the working parts along with the broken ones. C produces three prompts that each still contain two of the conflicts.

**41. A** — Multi-file scope (45+), multiple valid strategies, and infrastructure implications are the plan-mode trifecta: explore, compare approaches, and commit to a design before changing anything. B starts changing files before the strategy exists. C mechanizes a decision that hasn't been made. D parallelizes without an agreed approach — 45 sessions, several strategies.

**42. C** — When instructions fail to change behavior, few-shot examples demonstrating the analysis — here, spotting branch-level gaps and writing the closing tests — teach the judgment so the model generalizes it. A fails PRs without improving them. B multiplies happy-path tests. D is real but heavyweight infrastructure to reach for before trying examples.

**43. B** — Refine the prompt on a representative sample before batch-processing large volumes: first-pass success is what controls cost when a batch is 900 items and results arrive up to 24 hours later. A risks 900 bad analyses and a full resubmission cycle. C halves the waste instead of preventing it. D automates resubmission of a prompt that was never validated.

**44. D** — Batch failure handling: identify failed requests by `custom_id`, fix the cause (chunk the oversized diffs), and resubmit only those. A re-pays for 462 successful analyses (and "larger context configuration" isn't a batch setting). B re-sends the same oversized inputs to the same context limits. C silently drops the repos most likely to harbor debt — the biggest diffs.

**45. A** — Self-reported confidence is only usable after calibration: measure it against a labeled validation set with known outcomes and derive thresholds from measured accuracy. B trusts raw self-report — known to be poorly calibrated. C swaps numeric self-report for verbal self-report. D substitutes a proxy (size) for the measurement you need.

**46. B** — Tool use with a JSON schema is the reliable mechanism for structured output: the extraction "tool" input conforms to your schema, eliminating trailing commas, fences, and preambles as a failure class. A reduces frequency but keeps the class. C is an arms race with formatting drift. D changes the syntax without adding any guarantee.

**47. D** — Required fields pressure the model to fabricate; fields that may legitimately be absent should be optional/nullable with instructions to return null. That removes the incentive to invent. A rejects fabrications after inviting them. B misuses empty strings as a null substitute while keeping the pressure. C is a downstream audit for an upstream schema problem.

**48. A** — The extensible-category pattern: an `"other"` enum value plus a detail string. Novel types are captured faithfully instead of forced into the nearest wrong bucket. B loses the machine-readable categories downstream systems rely on. C guesses the future and still misses something. D turns every novel type into manual work.

**49. C** — `tool_choice: "any"` guarantees a tool call while leaving the choice of tool to the model — exactly right when multiple extraction schemas exist and the document type is unknown. A forces the invoice schema onto contracts and résumés. B ("auto") is what permits the prose responses today. D adds a model and a routing layer to replicate what "any" already does.

**50. D** — Retries correct format and structural errors; they cannot recover information that is absent from the provided input. The governing law lives in a document the model never sees. Fix the input pipeline or handle the null explicitly. A and B retry harder at reading text that isn't there. C deletes a business-required field because the pipeline starves it.

**51. B** — Extracting `calculated_total` alongside `stated_total` with a `conflict_detected` flag is the self-correction/validation design: discrepancies are surfaced, not silently passed through (D) or silently overwritten (A — which hides genuine source-document errors that may matter legally). C treats every OCR artifact as a sender problem and stalls the pipeline.

**52. A** — Few-shot examples demonstrating extraction from varied document structures are the established fix for structure-driven misses — they show where the information lives in each format, and the model generalizes to further variants. B re-describes fields the model already understands. C reruns the same blindness twice. D presumes a reliable universal normalizer, which is the original problem restated.

**53. C** — Strict output schemas should be paired with format normalization rules in the prompt: how to map each source format to ISO 8601, how to disambiguate day/month order, and when to mark a value unresolvable. A pushes ambiguity downstream to a parser with even less context than the model had. B just relocates the problem. D rejects most real-world documents.

**54. D** — Aggregate accuracy can mask severe failures on specific segments; before reducing review, verify accuracy by document type and field. A flat 97% is consistent with 0% on one vendor's layout. A and B re-slice by time, not by segment. C is a staffing question, not a validation of the automation's safety.

**55. A** — Stratified random sampling of high-confidence extractions provides ongoing error-rate measurement and catches novel error patterns in exactly the population no one otherwise inspects. B assumes new errors will conveniently arrive with low confidence — miscalibration means they won't. C makes customers your QA. D can't detect novel patterns absent from the original benchmark.

**56. C** — Review thresholds are set by calibrating confidence against a labeled validation set: measure real accuracy at each confidence level, per field where performance differs, and set the cutoff where accuracy meets requirements. A and D are arbitrary numbers dressed as prudence. B sets thresholds by workload rather than by measured risk.

**57. B** — The reliability guidance: route low-confidence extractions and those from ambiguous or contradictory source documents to human review — spending scarce reviewer capacity where errors are most probable. A is a defensible business overlay but doesn't target error likelihood. C spreads capacity evenly over mostly-fine documents. D uses recency as a weak proxy for difficulty.

**58. D** — The API is stateless: conversational coherence requires passing the complete conversation history in every request. Sending only the latest message *is* the bug. A instructs the model to remember context it was never sent. B rebuilds conversation memory as external infrastructure. C shrinks the turns without restoring the missing history.

**59. A** — Verbose tool outputs consume context disproportionately to their relevance; trimming to the relevant fields before results accumulate (tool-side or via a PostToolUse transformation) fixes the accumulation at the source. B changes call frequency, not per-call bloat. C delays the overflow and doesn't address degradation. D summarizes after the tokens are already spent, repeatedly.

**60. C** — This is the lost-in-the-middle effect. Since splitting the request isn't possible, apply the position mitigations: a key-facts summary at the beginning and explicit, labeled section headers organizing the detail. A rotates which fields get missed. B doubles input size and still buries other documents. D — position effects are not fixed by exhortation.

---

*End of Practice Exam 2.*
