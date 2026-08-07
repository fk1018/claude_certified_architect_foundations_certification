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

- A) Raise the cap to 15 iterations, which covers the 95th percentile of observed task lengths.
- B) Drive the loop from `stop_reason`: continue on `"tool_use"`, stop at `"end_turn"`, keeping caps as a safety backstop.
- C) Have the coordinator estimate the required iterations up front and set the cap per task.
- D) Prompt the coordinator to plan its work to fit within 5 iterations before starting.

**Question 2.** Your pipeline researches fast-moving topics using a fixed sequence: search three predetermined subtopics → analyze → synthesize. Reviews show reports keep missing important angles that only became apparent from the initial findings (e.g., a lawsuit that reframed an industry story). What should change?

- A) Increase the number of predetermined subtopics from three to eight to widen initial coverage.
- B) Run the same fixed pipeline twice and merge the two reports.
- C) Move to a model with a larger context window so more search results fit into the analysis step.
- D) Have the coordinator generate new subtasks from what each step discovers, instead of fixing subtopics up front.

**Question 3.** Your coordinator frequently delegates document-analysis tasks to the web-search subagent. Reviewing the configuration, you find the subagents defined with descriptions like "Research helper 1" and "Research helper 2." What should you fix first?

- A) Add a routing table to the coordinator's system prompt mapping task keywords to subagent numbers.
- B) Reduce the number of subagents so there are fewer wrong choices available.
- C) Rewrite each AgentDefinition description to state the subagent's specialization and when to choose it.
- D) Fine-tune the coordinator on transcripts of correct delegation decisions.

**Question 4.** You want to continue a research project whose last session ran two weeks ago. Since then, several key sources have published updates, and the session's cached tool results reflect the old versions. What is the most reliable way to continue?

- A) Start a new session, inject a structured summary of the durable findings, and re-gather current data fresh.
- B) Resume the session with `--resume` and add a note telling the agent some sources may have changed.
- C) Resume the session and re-run only the searches the agent decides look stale.
- D) Use `fork_session` to branch the old session so the stale results stay isolated in the parent.

**Question 5.** The analysis subagent passes its findings to the coordinator as flowing prose paragraphs. By the time the synthesis agent works with them, source URLs are garbled and page numbers have disappeared. How should inter-agent context passing change?

- A) Instruct the analysis agent to double-check URLs before writing its prose summary.
- B) Have the coordinator re-look-up the sources for any claims whose attribution was lost.
- C) Shorten the analysis agent's output so there is less prose in which details can get lost.
- D) Use a structured format separating content from metadata: claim text plus fields for source URL, document, and page.

**Question 6.** A developer invokes the document-analysis subagent, then invokes it again with the prompt "Continue analyzing the paper from before." The agent responds that it has no paper to analyze. What explains this?

- A) The second invocation used a different model tier that cannot access the first invocation's cache.
- B) Subagent invocations are independent — all needed context must be passed explicitly each time.
- C) The subagent's context window overflowed between the two invocations.
- D) The Task tool requires a `session_id` parameter to link consecutive invocations, and it was omitted.

**Question 7.** Your search subagent uses three search MCP servers. One nests results under an `items` key, timestamps differ in format across all three, and relevance scores are 0–1 in one server but 0–100 in the others. The agent visibly mis-ranks sources when comparing across providers. What is the cleanest fix?

- A) Add a system prompt table documenting each provider's format so the agent converts scores when comparing.
- B) Use only the provider with the best format and drop the other two.
- C) Normalize all three providers' results into a common structure with a `PostToolUse` hook.
- D) Ask each provider's maintainer to adopt a common response schema.

**Question 8.** Reports on policy topics consistently lack opposing viewpoints. The pipeline makes a single pass, and the synthesis agent can only work with what was gathered. What is the most effective fix?

- A) Add a coordinator step that checks synthesis output for gaps and re-delegates targeted searches to fill them.
- B) Add "always include opposing viewpoints" to the synthesis agent's system prompt.
- C) Have the report agent add a caveats section acknowledging other views may exist.
- D) Double the search agent's result count so opposing sources are more likely to appear incidentally.

**Question 9.** One search MCP tool reports failures as ordinary text — a successful-looking response whose content reads "ERROR: rate limited." Your agent has been observed quoting this string in reports as if it were a research finding. What is the correct tool-side fix?

- A) Prompt the agent to check search results for text beginning with "ERROR:" and disregard it.
- B) Have the tool return an empty result set on failure so nothing wrong enters the context.
- C) Retry rate-limited requests inside the tool until they succeed, so the agent never sees an error.
- D) Return failures using the MCP `isError` flag with structured error content.

**Question 10.** Logs show the agent retried a paywalled source six times in a row, failing identically each time, before moving on. The tool returns only "Access failed." What should the error response include to prevent this waste?

- A) A longer error message explaining paywalls in more detail so the agent understands the concept.
- B) Structured metadata: `errorCategory: "permission"`, `isRetryable: false`, and a short description.
- C) An HTTP 402 status code, which models recognize as payment-related.
- D) A `retryAfter` value of 24 hours so retries are at least spaced out.

**Question 11.** Every transient search timeout currently propagates to the coordinator, which spends context reasoning about each one; coordinator contexts fill with error-handling on long tasks. How should error handling be distributed?

- A) Have subagents retry transient failures locally and propagate only unresolved errors with partial results.
- B) Suppress transient errors entirely — drop the failed query and let the coordinator work with whatever succeeded.
- C) Route all errors to a dedicated error-handling subagent that decides retries for the whole system.
- D) Increase the search timeout so transient failures become rare.

**Question 12.** A teammate asks: "The research agent is connected to arxiv-mcp, news-mcp, and finance-mcp. Where do we build the router that switches the active server per task?" What is the correct answer?

- A) In a `PreToolUse` hook that inspects the task and enables the right server.
- B) In the coordinator's system prompt, with rules for when to activate each server.
- C) Nowhere — tools from all configured servers are discovered at connection time and available simultaneously.
- D) In `.mcp.json`, using the `activeServer` field to set a default and override it per session.

**Question 13.** The report-generation agent occasionally calls `web_search` while writing, adding last-minute uncited claims that never went through analysis or synthesis. What is the best fix?

- A) Give the report agent a citation-generator tool so its additions at least carry sources.
- B) Remove search tools from the report agent and have it flag genuine gaps back to the coordinator.
- C) Add a system prompt rule: "Do not perform new research while writing the report."
- D) Run a fact-checking pass over final reports to catch unvetted additions.

**Question 14.** A report flags a "contradiction": one source says unemployment was 3.9%, another says 4.4%. Investigation shows the figures are from 2023 and 2025 — both correct for their time. How do you prevent this class of error?

- A) Instruct the synthesis agent to treat numeric differences under 1 percentage point as agreement.
- B) Have the search agent discard all sources more than a year old.
- C) Present both numbers and let readers decide, with no annotation.
- D) Require publication dates in subagents' structured outputs so temporal differences read as time series.

**Question 15.** During a research run, two topic areas couldn't be covered because key sources were unavailable. The final report presents all sections with equal apparent confidence. What should the synthesis output include?

- A) Nothing extra — the report should only contain what was found; absence of coverage is implied.
- B) A self-assessed confidence percentage on each section, computed by the model from its own uncertainty.
- C) Coverage annotations distinguishing well-supported findings from topic areas with gaps.
- D) A disclaimer paragraph stating that research has inherent limitations.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses the built-in tools (Read, Write, Bash, Grep, Glob) and integrates with MCP servers.

---

**Question 16.** You are implementing the agent's request loop. A response arrives with `stop_reason: "tool_use"` containing a request to run Grep. What must your code do?

- A) Execute the Grep call, append the result to the conversation as a tool result, and send it back.
- B) Treat the turn as complete and display the assistant's text to the developer.
- C) Re-send the same request, since `"tool_use"` indicates the model needs another attempt.
- D) Ask the developer to approve continuing, since the model has paused.

**Question 17.** An engineer is three days into investigating a legacy billing system, in a session she named. No relevant files have changed overnight. Each morning she wants to continue exactly where she left off. What should she do?

- A) Start a fresh session each morning and paste in her notes from the previous day.
- B) Use `--resume` with the session name, since the prior context is still valid.
- C) Use `fork_session` each morning so every day gets its own branch.
- D) Keep one terminal session running continuously for the whole investigation.

**Question 18.** You resume yesterday's analysis session, but you refactored two files last night after it ended. The resumed agent confidently describes the old versions of those files. The rest of its analysis is still accurate. What is the best course?

- A) Abandon the session and re-run the full multi-hour analysis from scratch.
- B) Keep working and correct the agent conversationally whenever it misremembers.
- C) Run `/compact` so the summarization refreshes the agent's view of the files.
- D) Tell the resumed session which specific files changed and ask it to re-analyze just those.

**Question 19.** After a thorough shared analysis of your codebase, you want to rigorously compare a Jest-to-Vitest migration against staying on Jest with upgraded tooling — explored independently so one exploration doesn't bias the other. What mechanism fits?

- A) Use `fork_session` to create two independent branches from the shared analysis baseline.
- B) Explore both options sequentially in the same session, then ask for a comparison.
- C) Start two brand-new sessions, one per approach, and repeat the codebase analysis in each.
- D) Run both explorations in one session, separated by `/clear` to reset context between them.

**Question 20.** You ask the agent to "add comprehensive tests to this legacy codebase" — a large, open-ended task. Which decomposition approach fits best?

- A) Process files alphabetically, writing tests for each file before moving to the next.
- B) Generate tests for the entire codebase in a single pass to keep style consistent.
- C) Map the structure, identify high-impact areas, then build a prioritized plan that adapts as discoveries emerge.
- D) Only add tests to files changed in the last 90 days, since older code is stable.

**Question 21.** You're automating API documentation generation: extract endpoint signatures → describe each endpoint → generate request/response examples → cross-check descriptions against the code. The stages are the same for every service. How should this be structured?

- A) A single mega-prompt asking for finished documentation in one shot.
- B) A fixed sequential prompt chain — one focused pass per stage feeding the next.
- C) Dynamic decomposition, letting the agent invent its approach per service.
- D) Four parallel subagents, one per stage, all running simultaneously.

**Question 22.** The productivity agent uses Bash. Policy: it must never run destructive git commands (`push --force`, `reset --hard`) against shared branches. It is CLAUDE.md-instructed today, but an incident still occurred. What is the correct guardrail?

- A) Strengthen the CLAUDE.md wording and add the rule to the agent's system prompt as well.
- B) Remove Bash from the agent's toolset so no shell commands can run at all.
- C) Have the agent explain each git command before running it so developers can object.
- D) Add a hook that intercepts Bash calls and blocks destructive git patterns against shared branches.

**Question 23.** For "repetitive" boilerplate tasks, a teammate hardcoded the tool sequence Grep → Read → Write into the agent's loop. It works for the common case but fails when a task needs several related files read first, or none at all. What does this illustrate?

- A) The model should decide which tools to call from context; fixed sequences can't adapt to per-task variation.
- B) The sequence is missing a Glob step at the beginning; a four-step script would be robust.
- C) Grep should be replaced with an MCP code-search tool before scripting the sequence.
- D) The Write step should be split into Edit-then-Write for safety.

**Question 24.** You need to find every file that imports the deprecated `LegacyHttpClient` class across a large monorepo. Which built-in tool is right for the first step?

- A) Glob — match the files by name pattern.
- B) Read — read files one by one, checking imports.
- C) Grep — search file contents for the import pattern across the codebase.
- D) Bash `ls -R` — enumerate the tree, then inspect likely files.

**Question 25.** Your team needs Jira integration for the agent (create issues, query sprints — standard operations). An engineer proposes writing a custom MCP server for it. What is the better default guidance?

- A) Build the full custom server — in-house servers are more maintainable than third-party code.
- B) Use an existing community MCP server, reserving custom development for team-specific workflows.
- C) Skip MCP and have the agent call the Jira REST API directly through Bash and curl.
- D) Build a thin custom MCP server wrapping only the two Jira endpoints you need today.

**Question 26.** The agent tries to Edit a config block that appears verbatim in four places in one file, and Edit fails because the anchor text is not unique. What is the reliable fallback?

- A) Read the full file, then Write it back with the intended modification applied.
- B) Retry the Edit with the same anchor text but the `replace_all` option off.
- C) Use Bash `sed` to perform the replacement by line number.
- D) Delete the duplicate blocks first so the anchor becomes unique.

**Question 27.** An engineer asks the agent to explain how request authentication works in an unfamiliar 4,000-file service. Which exploration strategy should the agent use?

- A) Read every file under `src/` upfront so the explanation is grounded in complete knowledge.
- B) Rely on the repository README and directory names to infer the architecture.
- C) Glob for `*auth*` filenames and read only those files.
- D) Grep for entry points, then Read the relevant files, following imports to trace the flow.

**Question 28.** Your team built a semantic code-search MCP server that outperforms text search for conceptual queries, but the agent almost always uses built-in Grep instead. Its description reads: "Searches code." What should you do?

- A) Remove Grep from the agent's toolset so the MCP server is the only search option.
- B) Add a system prompt rule: "Always prefer MCP tools over built-in tools."
- C) Rewrite the MCP tool's description: what semantic matching does, what it returns, and when it beats text search.
- D) Lower the MCP server's latency so the agent learns it is the faster option.

**Question 29.** You want the whole team to get your GitHub MCP server automatically when they pull the repo, authenticating with each developer's own token, without committing any secrets. How?

- A) Commit a project-scoped `.mcp.json` that references the token as `${GITHUB_TOKEN}` from each developer's environment.
- B) Commit `.mcp.json` with each developer's token in a per-user section of the file.
- C) Have each developer configure the server in their personal `~/.claude.json`.
- D) Store the token in CLAUDE.md, which is already shared through version control.

**Question 30.** Your infrastructure conventions apply only to Terraform files, which live in `terraform/` directories scattered across a dozen service folders. You want the conventions loaded only when Claude edits those files, without paying their token cost in every session. What is the right mechanism?

- A) Add the conventions to the root CLAUDE.md under a "Terraform" heading.
- B) Create a `.claude/rules/` file with YAML frontmatter `paths: ["**/*.tf"]`.
- C) Create a CLAUDE.md inside every one of the dozen `terraform/` directories.
- D) Create a `/terraform-rules` skill developers invoke before infrastructure work.

---

## Scenario C: Claude Code for Continuous Integration (Questions 31–45)

You are integrating Claude Code into your CI/CD pipeline. The system runs automated code reviews, generates test cases, and provides feedback on pull requests. You need to design prompts that provide actionable feedback and minimize false positives.

---

**Question 31.** You're writing the GitHub Actions step that runs the automated review. It must run without any interactive input and emit output your comment-posting script can parse. Which invocation is correct?

- A) `claude "Review this PR" --interactive=false --format=structured`
- B) `CLAUDE_HEADLESS=true claude "Review this PR" --parse`
- C) `claude --batch "Review this PR" > findings.json`
- D) `claude -p "Review this PR" --output-format json --json-schema review-schema.json`

**Question 32.** Your pipeline generates code with Claude Code, then resumes the same session for the review step "so the reviewer understands why the code was written." The reviews almost never find issues, but human reviewers do. What should change?

- A) Run the review as an independent instance without the generation session's context.
- B) Add "be maximally critical of the changes" to the review step's prompt.
- C) Enable extended thinking for the review step so it reasons more deeply.
- D) Keep the shared session but review each file twice.

**Question 33.** The nightly test-generation job keeps proposing test scenarios that already exist in your spec files. What is the most direct fix?

- A) Run a deduplication pass comparing generated test names against existing test names.
- B) Have Claude generate twice as many tests so at least some are novel.
- C) Provide the existing test files in context and instruct Claude to propose only uncovered scenarios.
- D) Limit generation to newly created source files, which cannot have tests yet.

**Question 34.** Your senior engineers each keep excellent review criteria in their personal `~/.claude/CLAUDE.md` files. The CI runner's automated reviews follow none of these criteria. Why, and what is the fix?

- A) The CI runner needs the `--memory` flag to load user-level CLAUDE.md files.
- B) User-level CLAUDE.md never reaches the CI environment — move the criteria into the project-level CLAUDE.md.
- C) The criteria files are too large for non-interactive mode; they need to be under 10KB.
- D) CI-invoked Claude Code cannot read CLAUDE.md at all; criteria must be passed as prompt flags.

**Question 35.** Your CI review skill only needs to read code and report findings. A pipeline audit found one run where it executed `npm install` and modified `package-lock.json` in the workspace. What is the correct constraint?

- A) Run the CI job in a container where writes fail at the filesystem level.
- B) Add "never install packages or modify files" to the skill's instructions.
- C) Have the pipeline revert any workspace changes after the review step.
- D) Configure `allowed-tools` in the skill's frontmatter to permit only read and reporting operations.

**Question 36.** Your 400-line review checklist currently lives in the root CLAUDE.md. Every interactive session pays its token cost, though it's only needed when reviews run. The checklist must stay identical for interactive `/review` use and CI. Where should it live?

- A) In a review skill under `.claude/skills/`, loaded on demand when invoked by developers or CI.
- B) Split across ten smaller CLAUDE.md sections so no single block is large.
- C) In CLAUDE.md still, with an instruction telling Claude to ignore it outside reviews.
- D) In user-level CLAUDE.md so only reviewers pay the cost.

**Question 37.** Your changelog-generation step turns merged-PR titles into release notes. The prose spec ("group by type, past tense, link each PR") is interpreted differently across runs — grouping and tense drift. What is the most effective fix?

- A) Rewrite the spec with stricter language and bolded MUST requirements.
- B) Add 2–3 concrete examples to the prompt: sample input commit lists with the exact changelog output expected.
- C) Convert the spec into a numbered checklist the model must follow step by step.
- D) Generate three drafts per run and have a second model choose the most compliant.

**Question 38.** You're using Claude to fix a data-transform module that intermittently fails in CI. You want an iteration loop that converges instead of whack-a-mole fixes. What is the best structure?

- A) Describe all known symptoms and ask for one comprehensive fix.
- B) Ask Claude to review the module line by line and fix everything suspicious.
- C) Rewrite the module from scratch, since accumulated fixes indicate unfixable design.
- D) Write a test suite first covering behavior, edge cases, and performance; iterate by sharing failing output.

**Question 39.** You're about to build Claude Code into your deployment-approval flow — a domain with rollback semantics, partial-failure modes, and compliance constraints you haven't fully articulated. Which technique best surfaces the hidden requirements before implementation?

- A) Implement a minimal version first and let production incidents reveal the missing requirements.
- B) Write the complete specification yourself before involving Claude at all.
- C) Use the interview pattern — have Claude question you about failure modes and edge cases before implementing.
- D) Copy the integration design from a published blog post by a team with a similar stack.

**Question 40.** Your review prompt has three problems that interact: the severity definitions conflict with the category definitions, which in turn contradict the output examples. Fixing them one at a time has caused regressions — each fix breaks under the next. How should you deliver the corrections?

- A) Address all three in a single detailed message explaining each problem and how they interact.
- B) Fix them in three sequential messages, verifying each fix before the next.
- C) Rebuild the prompt from an empty file, reintroducing requirements one by one.
- D) Open three parallel sessions, fixing one problem in each, then merge the best parts.

**Question 41.** Before your CI can validate it, you must migrate the repo's test framework — 45+ files, several valid migration strategies, and infrastructure implications for the CI runners themselves. How should you begin in Claude Code?

- A) Use direct execution file by file, since each individual file change is small.
- B) Ask Claude to generate a shell script that performs the whole migration mechanically.
- C) Enter plan mode to explore the codebase and compare migration strategies before changing anything.
- D) Fork 45 parallel sessions, one per file, to complete the migration fastest.

**Question 42.** Generated tests cover happy paths well but consistently miss branch-level gaps — error paths, boundary conditions, early returns. Detailed instructions ("cover all branches, including error handling") haven't changed the behavior. What is the most effective next step?

- A) Raise the coverage threshold in CI so incomplete test PRs fail automatically.
- B) Add few-shot examples that demonstrate finding a function's branch-level gaps and writing the closing tests.
- C) Switch the generation prompt to ask for twice as many tests per function.
- D) Run mutation testing and feed surviving mutants back for another pass.

**Question 43.** You're preparing your first Batch API run: overnight tech-debt analysis across 900 repositories with a prompt that has never been tested at scale. What should you do first?

- A) Submit all 900 and treat the first run as the test — batch costs are already discounted 50%.
- B) Split the batch into two 450-repo halves so a bad prompt only wastes half the spend.
- C) Add a retry wrapper that automatically resubmits any repo whose analysis looks wrong.
- D) Refine the prompt on a small representative sample with the synchronous API, then submit the full batch.

**Question 44.** Your overnight batch of 500 analysis requests completes with 38 failures, all caused by oversized diffs exceeding context limits. What is the correct recovery?

- A) Identify the failures by `custom_id`, chunk their oversized diffs, and resubmit only those 38.
- B) Resubmit the full 500-request batch with a larger context configuration.
- C) Rerun the 38 through the synchronous API unchanged, since it handles large inputs better.
- D) Drop the 38 — a 92% completion rate is within tolerance for a nightly job.

**Question 45.** You want the pipeline to auto-approve PRs the review bot deems clean, but only where that trust is justified. The bot can emit a confidence score per finding. What makes the confidence usable for routing?

- A) Trust scores above 8/10, since models are generally reliable at the extremes.
- B) Ask the model to justify each confidence score, and trust the ones with good justifications.
- C) Calibrate it against a labeled validation set of past reviews and set routing thresholds from that data.
- D) Use PR size instead — small PRs are safe to auto-approve regardless of bot confidence.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

You are building a structured data extraction system using Claude. The system extracts information from unstructured documents, validates the output using JSON schemas, and maintains high accuracy. It must handle edge cases gracefully and integrate with downstream systems.

---

**Question 46.** Your extraction prompt asks Claude to "respond with a JSON object" in its text reply. About 7% of responses fail parsing — trailing commas, markdown code fences, explanatory text before the JSON. What is the most reliable fix?

- A) Add "Respond with ONLY raw JSON, no markdown, no commentary" to the prompt.
- B) Strip code fences and trailing commas with a preprocessing regex before parsing.
- C) Switch the output format to XML, which tolerates minor malformation better.
- D) Define an extraction tool whose input schema is your structure and read the data from the `tool_use` block.

**Question 47.** Some invoices legitimately lack a PO number, but your schema marks `po_number` as required. Sampling reveals the model sometimes invents plausible-looking PO numbers for those invoices. What is the correct schema fix?

- A) Add a validation rule that rejects PO numbers not matching your company's format.
- B) Make `po_number` optional/nullable and instruct the model to return null when the document has none.
- C) Prompt the model to leave required fields as empty strings when data is missing.
- D) Cross-check every extracted PO number against the purchasing database and drop mismatches.

**Question 48.** Your `document_type` enum is `["invoice", "receipt", "purchase_order"]`. New document types keep arriving (credit memos, delivery notes), and the model shoehorns them into the closest existing value. How should the schema evolve?

- A) Remove the enum and make `document_type` free text so anything can be represented.
- B) Add every document type your industry uses to the enum preemptively.
- C) Add an `"other"` enum value paired with a free-text detail field describing the actual type.
- D) Reject any document that doesn't match the three known types and queue it for humans.

**Question 49.** You defined three extraction tools — `extract_invoice`, `extract_contract`, `extract_resume` — and documents arrive with unknown type. Sometimes the model responds with prose about the document instead of extracting. Which configuration guarantees structured output while letting the model pick the right schema?

- A) `tool_choice: "any"` — the model must call some tool and selects the appropriate extraction schema.
- B) `tool_choice: {"type": "tool", "name": "extract_invoice"}` — force the most common type.
- C) `tool_choice: "auto"` with a prompt instruction to always use a tool.
- D) A separate classification model that routes each document to a forced single-tool call.

**Question 50.** Contract extractions repeatedly fail validation with `governing_law: null`. Sampling shows the governing-law clause typically lives in a master agreement referenced by, but not included with, the contracts you send. Will retry-with-error-feedback fix this?

- A) Yes — include the validation error and the model will look harder at the contract text.
- B) No — retries can't recover information absent from the input; supply the master agreement or accept the null.
- C) Yes, but only with 3+ retries and escalating temperature to explore more readings.
- D) No — the field should be dropped from the schema since it cannot be extracted.

**Question 51.** Invoice line items sometimes don't sum to the stated total — occasionally an OCR artifact, occasionally a genuine source-document error. Downstream systems must not silently receive bad totals. What extraction design handles this?

- A) Have the model recompute the total from line items and output the corrected value in place of the stated one.
- B) Reject any invoice where the arithmetic fails and return it to the sender.
- C) Trust `stated_total` always — the document is the source of truth.
- D) Extract `calculated_total` alongside `stated_total`, with a `conflict_detected` flag when they disagree.

**Question 52.** Résumé extraction works well on standard corporate résumés but returns null for required-in-source fields on academic CVs and international formats, where the information exists but appears in unfamiliar sections. What is the most effective fix?

- A) Lengthen the field descriptions in the schema so the model knows the fields matter.
- B) Run two extraction passes and merge the non-null values from each.
- C) Add few-shot examples showing correct extraction from an academic CV and an international format.
- D) Preprocess all documents into a standardized layout before extraction.

**Question 53.** Source documents write dates as "3/4/25", "March 4th, 2025", and "04-03-2025" (ambiguous day/month order), while your schema requires ISO 8601. What should accompany the strict output schema?

- A) Format normalization rules in the prompt: how to map each source format to ISO 8601, how to resolve ambiguous orderings, and when to mark a date unresolvable.
- B) A post-processing date parser that converts whatever the model outputs.
- C) A looser schema accepting dates as free text, normalized downstream.
- D) Rejection of documents whose dates aren't already ISO 8601.

**Question 54.** Your extraction system reports 97% overall accuracy, and leadership wants to cut human review by 80%. What must you verify before agreeing?

- A) That the 97% was measured within the last quarter.
- B) That accuracy holds up when segmented by document type and by field.
- C) That accuracy exceeds 97% on the most recent week of documents specifically.
- D) That reviewer headcount can be reabsorbed elsewhere if the cut proceeds.

**Question 55.** You automated the pipeline for high-confidence extractions. Six months from now, how will you know whether new error patterns have crept into the extractions no human looks at?

- A) Human review already covers the low-confidence extractions; errors would appear there first.
- B) Track the distribution of confidence scores over time and investigate when the average drifts.
- C) Re-run the original validation benchmark quarterly against the same benchmark documents.
- D) Keep stratified random sampling of high-confidence extractions under ongoing human review.

**Question 56.** You calibrated the field-level confidence thresholds that decide which extractions skip human review against a labeled validation set six months ago. This week you substantially revised the extraction prompt to support several new document types. What should happen to the thresholds?

- A) Keep them — thresholds attach to the output schema, which did not change.
- B) Recalibrate against labeled data before trusting them; the confidence-accuracy mapping may have shifted.
- C) Raise them by a fixed 10% margin until a quarter of new production data accumulates.
- D) Lower them temporarily, since the revised prompt should be more accurate than the old one.

**Question 57.** Your reviewers can inspect 500 documents daily out of 10,000 processed, and your goal is to catch as many extraction errors as possible with that fixed capacity. Which routing strategy best serves the goal?

- A) Review the 500 highest-dollar-value documents, since errors there cost the most.
- B) Review a uniform random 5% so every document type has equal audit probability.
- C) Route low-confidence extractions and those from ambiguous or contradictory sources to review.
- D) Review the newest documents first, since recent formats are least familiar to the model.

**Question 58.** Your extraction service supports a multi-turn correction chat: users point out extraction mistakes and the model revises. Users report the model "forgets" corrections from two turns earlier. The service sends each API request with only the latest user message. What is the fix?

- A) Send the complete conversation history in every API request.
- B) Add a system prompt instruction telling the model to remember all prior corrections.
- C) Cache the model's last response client-side and re-send it with each new message.
- D) Store corrections in a database and have the model query them through a tool.

**Question 59.** Each extraction is enriched via a vendor-lookup MCP tool that returns 40+ fields per call, of which your workflow uses 5. Long enrichment sessions degrade noticeably and sometimes overflow context. What is the right fix?

- A) Call the vendor-lookup tool less often by batching several vendors per call.
- B) Move to a model with a larger context window to absorb the verbose results.
- C) Summarize the conversation with /compact after every ten enrichments.
- D) Trim the tool output to the relevant fields before it accumulates in context.

**Question 60.** A nightly job must cross-reference 20 related documents in a single request (they reference each other, so they can't be processed separately). Fields sourced from documents in the middle of the concatenated input show markedly higher miss rates than those near the start and end. What is the best mitigation?

- A) Randomize document order nightly so no document is always in the middle.
- B) Duplicate the middle documents at the end of the input so they appear twice.
- C) Add a key-facts summary at the beginning and organize the documents under labeled section headers.
- D) Instruct the model: "Documents in the middle are equally important; do not skip them."

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

**9. D** — The MCP `isError` flag is the mechanism for signaling tool failure; errors returned as ordinary content are indistinguishable from data, which is exactly why the agent quoted one. A is fragile string-matching over a protocol problem. B silently converts failure into "no results," misleading the agent differently. C hides genuine failures and can retry forever.

**10. B** — Structured error metadata — `errorCategory: "permission"`, `isRetryable: false`, a human-readable description — tells the agent immediately that retrying is pointless and why, so it pivots to alternatives. A explains without machine-actionable structure. C leans on HTTP folklore instead of the MCP error contract. D still invites a retry that can never succeed.

**11. A** — The recommended distribution: subagents handle transient failures locally (retry/backoff) and propagate only unresolvable errors, with what was attempted and partial results. That keeps coordinator context for coordination. B silently suppresses errors — an anti-pattern that corrupts research completeness. C adds a communication hop for decisions best made where the failure happened. D reduces frequency without fixing the architecture.

**12. C** — There is no server switching: tools from all configured MCP servers are discovered at connection time and are simultaneously available; selection happens through tool descriptions like any other tools. A, B, and D all build (or invent — there is no `activeServer` field) machinery for a problem the protocol already solves.

**13. B** — The report agent's role is rendering synthesized, vetted findings; search tools are outside its specialization and their misuse (uncited last-minute claims) is the predictable result. Scope its tools to its role and route real gaps back through the coordinator. A legitimizes bypassing the pipeline. C is probabilistic — the behavior already occurs. D catches contamination after the fact.

**14. D** — Requiring publication/collection dates in structured outputs lets synthesis interpret differing figures as time-series data instead of contradictions. A is an arbitrary numeric heuristic that would also mask genuine conflicts. B throws away valid historical data. C presents the confusion to the reader instead of resolving its cause.

**15. C** — Synthesis output should carry coverage annotations: which findings are well-supported and which topic areas have gaps due to unavailable sources. A and D leave readers unable to distinguish thin coverage from strong coverage. B substitutes uncalibrated self-reported confidence for the factual annotation the system can actually make (these sources were unavailable).

**16. A** — `stop_reason: "tool_use"` means: execute the requested tool, append the result to the conversation as a tool result, and send it back for the next iteration. That's the agentic loop. B abandons the task mid-loop. C re-sends without providing the result the model asked for. D inserts a human where none is required.

**17. B** — Named session resumption (`--resume <session-name>`) is designed for exactly this: continuing a specific prior conversation whose context is still valid (no relevant files changed). A discards accumulated context that resumption preserves. C forks branches with no divergent approaches to explore. D conflates process uptime with session persistence.

**18. D** — When resuming after code modifications, inform the session which specific files changed for targeted re-analysis; the rest of the context is still valid. A re-spends hours to refresh two files. B leaves stale beliefs in context to resurface later. C — `/compact` summarizes conversation history; it doesn't re-read changed files.

**19. A** — `fork_session` exists for exploring divergent approaches from a shared analysis baseline: two independent branches, each unbiased by the other's exploration, both grounded in the same understanding. B lets the first exploration contaminate the second. C pays for the codebase analysis twice. D — `/clear` discards the shared analysis the comparison depends on.

**20. C** — Open-ended tasks decompose best by mapping structure, identifying high-impact areas, and building a prioritized plan that adapts as dependencies are discovered. A spends effort by filename rather than by risk. B is one unfocused pass over a large codebase — attention dilution. D uses recency as a proxy for importance; critical old code stays untested.

**21. B** — Predictable, identical multi-stage workflows are the home ground of prompt chaining: focused sequential passes, each feeding the next. A crams four concerns into one pass and loses focus. C adds adaptive machinery where nothing varies. D ignores the data dependency — stage 2 needs stage 1's output.

**22. D** — A must-never-happen rule needs programmatic enforcement: a hook intercepting Bash calls and blocking destructive git patterns gives a deterministic guarantee. A doubles down on prompt-based compliance, which already failed. B is a structural guarantee but massively over-broad — it removes all shell capability to block two command patterns. C relies on developers reading every command in time.

**23. A** — Pre-configured sequences fail on per-task variation; the case for model-driven behavior is that the model chooses tools based on the actual task context. B and D just lengthen or reshuffle the script — some task will break any fixed sequence. C swaps one tool inside a script whose problem is being a script.

**24. C** — Finding files by their *contents* (an import statement) is Grep's job: search the codebase for the pattern. A (Glob) matches file *names*, which tell you nothing about imports. B reads blindly at monorepo scale. D enumerates names, same limitation as Glob with more steps.

**25. B** — For standard integrations like Jira, existing community MCP servers are the default; custom server development is reserved for team-specific workflows. A and D both spend engineering time re-solving a solved problem — the thin wrapper still needs auth, error handling, and maintenance the community server already has. C abandons MCP's typed tool interface for shell-and-curl fragility.

**26. A** — When Edit can't find a unique anchor, the documented fallback is Read the full file, then Write it back with the modification applied. B retries the exact failure. C bypasses the harness's file tools for `sed` line-number surgery — easy to get subtly wrong. D makes semantic changes to the file just to enable a mechanical edit.

**27. D** — Build understanding incrementally: Grep for entry points, Read the relevant files, follow imports to trace the flow. That answers the question with minimal context spend. A exhausts context on mostly-irrelevant files. B infers instead of verifying. C assumes auth code is named "auth" — middleware, guards, and interceptors say otherwise.

**28. C** — The agent prefers Grep because it understands what Grep does; a two-word MCP description gives the semantic tool no case for selection. Enhancing the description — capabilities, outputs, when it beats text search — is the documented fix. A removes a tool that's still right for exact-string searches. B is a blanket rule that misroutes exact-match queries. D — the agent isn't choosing on latency.

**29. A** — Project-scoped `.mcp.json` is shared via version control, and `${GITHUB_TOKEN}` environment-variable expansion supplies each developer's own credential at runtime without committing secrets. B commits secrets. C isn't shared — every developer configures by hand. D puts a credential in a context file; CLAUDE.md is instructions, not secret storage.

**30. B** — A `.claude/rules/` file with `paths: ["**/*.tf"]` frontmatter loads the conventions only when matching files are edited — glob-based activation that works no matter which directories the files sit in. A pays the token cost in every session. C means a dozen files to keep synchronized. D loads only when a human remembers to invoke it.

**31. D** — `-p` runs Claude Code non-interactively (print result and exit), and `--output-format json` with `--json-schema` yields machine-parseable, schema-conforming output. A, B, and C are built from flags and environment variables that don't exist (`--interactive`, `CLAUDE_HEADLESS`, `--batch`).

**32. A** — A session that generated the code retains the reasoning that produced it and is unlikely to question its own decisions; independent review instances catch what self-review misses. The "understands why" intuition is precisely the bias. B and C intensify a structurally biased review. D repeats it.

**33. C** — Provide the existing test files in context and instruct generation to avoid scenarios already covered — the model can't avoid duplicating tests it has never seen. A catches only name collisions, not semantic duplicates. B generates more duplicates alongside the novelty. D abandons coverage improvement for existing code, which was the point.

**34. B** — User-level CLAUDE.md lives in each engineer's home directory; the CI runner has no such files. Project-level CLAUDE.md is in the repository, so the CI checkout carries it. The fix is moving the criteria there (which also shares them with the whole team). A, C, and D describe flags and limits that don't exist.

**35. D** — `allowed-tools` in the skill frontmatter removes execution tools from availability during the skill — a structural guarantee that read-and-report is all it can do. A contains damage at the infrastructure layer but lets the harness misbehave inside it. B is instruction-based and already failed once. C cleans up afterward instead of preventing.

**36. A** — On-demand, task-specific content belongs in a skill: invoked identically by developers and CI, absent from unrelated sessions. That's the skills-vs-CLAUDE.md dividing line (always-loaded universal standards vs. on-demand workflows). B still loads everything, just in pieces. C pays full cost and adds an ignore instruction. D hides team-shared material in personal config.

**37. B** — When prose specs are interpreted inconsistently, concrete input/output examples are the most effective correction — they show the exact grouping, tense, and linking expected. A is stronger prose with the same ambiguity. C is still prose instructions, restructured — the interpretation variance remains. D spends three generations plus a judgment call to avoid writing two examples.

**38. D** — Test-driven iteration: write the suite covering expected behavior, edge cases, and performance first, then iterate by sharing failures. The tests define "done" and each round has an objective target. A and B are single-shot or unfocused passes with no convergence criterion. C throws away working behavior on a hunch.

**39. C** — The interview pattern is designed for unfamiliar domains with unarticulated constraints: Claude asks the questions that surface failure modes and edge cases you didn't think to specify. A discovers requirements via incidents. B assumes you can enumerate considerations you haven't anticipated — the exact gap. D imports another team's constraints, not yours.

**40. A** — Interacting problems must be fixed together: one detailed message addressing all three and how they interrelate. Sequential fixes (B) are what's already regressing — each fix optimizes against soon-to-change context. C discards the working parts along with the broken ones. D produces three prompts that each still contain two of the conflicts.

**41. C** — Multi-file scope (45+), multiple valid strategies, and infrastructure implications are the plan-mode trifecta: explore, compare approaches, and commit to a design before changing anything. A starts changing files before the strategy exists. B mechanizes a decision that hasn't been made. D parallelizes without an agreed approach — 45 sessions, several strategies.

**42. B** — When instructions fail to change behavior, few-shot examples demonstrating the analysis — here, spotting branch-level gaps and writing the closing tests — teach the judgment so the model generalizes it. A fails PRs without improving them. C multiplies happy-path tests. D is real but heavyweight infrastructure to reach for before trying examples.

**43. D** — Refine the prompt on a representative sample before batch-processing large volumes: first-pass success is what controls cost when a batch is 900 items and results arrive up to 24 hours later. A risks 900 bad analyses and a full resubmission cycle. B halves the waste instead of preventing it. C automates resubmission of a prompt that was never validated.

**44. A** — Batch failure handling: identify failed requests by `custom_id`, fix the cause (chunk the oversized diffs), and resubmit only those. B re-pays for 462 successful analyses (and "larger context configuration" isn't a batch setting). C re-sends the same oversized inputs to the same context limits. D silently drops the repos most likely to harbor debt — the biggest diffs.

**45. C** — Self-reported confidence is only usable after calibration: measure it against a labeled validation set with known outcomes and derive thresholds from measured accuracy. A trusts raw self-report — known to be poorly calibrated. B swaps numeric self-report for verbal self-report. D substitutes a proxy (size) for the measurement you need.

**46. D** — Tool use with a JSON schema is the reliable mechanism for structured output: the extraction "tool" input conforms to your schema, eliminating trailing commas, fences, and preambles as a failure class. A reduces frequency but keeps the class. B is an arms race with formatting drift. C changes the syntax without adding any guarantee.

**47. B** — Required fields pressure the model to fabricate; fields that may legitimately be absent should be optional/nullable with instructions to return null. That removes the incentive to invent. A rejects fabrications after inviting them. C misuses empty strings as a null substitute while keeping the pressure. D is a downstream audit for an upstream schema problem.

**48. C** — The extensible-category pattern: an `"other"` enum value plus a detail string. Novel types are captured faithfully instead of forced into the nearest wrong bucket. A loses the machine-readable categories downstream systems rely on. B guesses the future and still misses something. D turns every novel type into manual work.

**49. A** — `tool_choice: "any"` guarantees a tool call while leaving the choice of tool to the model — exactly right when multiple extraction schemas exist and the document type is unknown. B forces the invoice schema onto contracts and résumés. C ("auto") is what permits the prose responses today. D adds a model and a routing layer to replicate what "any" already does.

**50. B** — Retries correct format and structural errors; they cannot recover information that is absent from the provided input. The governing law lives in a document the model never sees. Fix the input pipeline or handle the null explicitly. A and C retry harder at reading text that isn't there. D deletes a business-required field because the pipeline starves it.

**51. D** — Extracting `calculated_total` alongside `stated_total` with a `conflict_detected` flag is the self-correction/validation design: discrepancies are surfaced, not silently passed through (C) or silently overwritten (A — which hides genuine source-document errors that may matter legally). B treats every OCR artifact as a sender problem and stalls the pipeline.

**52. C** — Few-shot examples demonstrating extraction from varied document structures are the established fix for structure-driven misses — they show where the information lives in each format, and the model generalizes to further variants. A re-describes fields the model already understands. B reruns the same blindness twice. D presumes a reliable universal normalizer, which is the original problem restated.

**53. A** — Strict output schemas should be paired with format normalization rules in the prompt: how to map each source format to ISO 8601, how to disambiguate day/month order (e.g., from document context), and when to mark a value unresolvable. B pushes ambiguity downstream to a parser with even less context than the model had. C just relocates the problem. D rejects most real-world documents.

**54. B** — Aggregate accuracy can mask severe failures on specific segments; before reducing review, verify accuracy by document type and field. A flat 97% is consistent with near-total failure on one vendor's layout. A and C re-slice by time, not by segment. D is a staffing question, not a validation of the automation's safety.

**55. D** — Stratified random sampling of high-confidence extractions provides ongoing error-rate measurement and catches novel error patterns in exactly the population no one otherwise inspects. A assumes new errors will conveniently arrive with low confidence — miscalibration means they won't. B monitors the model's opinion of itself, not actual accuracy; confidently-wrong errors never move the average. C can't detect novel patterns absent from the original benchmark.

**56. B** — Calibration maps confidence to measured accuracy *for a specific system*; substantially changing the prompt changes that mapping, so thresholds must be re-validated against labeled data before extractions skip review on their strength. A ties calibration to the wrong artifact — the schema didn't drive the mapping, the model+prompt did. C and D adjust blindly in opposite directions; neither is a measurement.

**57. C** — To catch the most errors with fixed capacity, route review to where errors are most likely: low model confidence and ambiguous or contradictory source documents. A targets cost-of-error, not likelihood-of-error — high-value documents are mostly extracted correctly. B spreads capacity evenly over mostly-fine documents. D uses recency as a weak proxy for difficulty.

**58. A** — The API is stateless: conversational coherence requires passing the complete conversation history in every request. Sending only the latest message *is* the bug. B instructs the model to remember context it was never sent. C restores one turn of history — corrections from two turns back stay lost. D rebuilds conversation memory as external infrastructure.

**59. D** — Verbose tool outputs consume context disproportionately to their relevance; trimming to the relevant fields before results accumulate (tool-side or via a PostToolUse transformation) fixes the accumulation at the source. A changes call frequency, not per-call bloat. B delays the overflow and doesn't address degradation. C summarizes after the tokens are already spent, repeatedly.

**60. C** — This is the lost-in-the-middle effect. Since splitting the request isn't possible, apply the position mitigations: a key-facts summary at the beginning and explicit, labeled section headers organizing the detail. A rotates which fields get missed. B doubles input size and still buries other documents. D — position effects are not fixed by exhortation.

---

*End of Practice Exam 7.*
