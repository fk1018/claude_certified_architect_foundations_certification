# CCAFC Practice Exam 13

**Claude Certified Architect – Foundations — Targeted Retake Exam: Mechanism Selection**

This remediation exam is weighted toward objectives that scored below 100% on the August 2, 2026 score report. It intentionally does not follow the official domain percentages: its purpose is to turn the reported weak areas into reliable scenario judgment.

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer and three plausible distractors per item |
| Scenarios | 4 (Code Generation with Claude Code, Developer Productivity, Multi-Agent Research System, Structured Data Extraction) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**; for retake readiness on these weak areas, target at least 48 / 60. |

Focus distribution: Claude Code configuration selection ×8, MCP scope/integration ×6, adaptive decomposition ×8, extraction accuracy ×8, iterative refinement ×6, codebase exploration ×6, tool-description design ×5, session resumption ×4, human-review routing ×4, and MCP error handling ×5.

Answer key with explanations is at the end.

---

## Scenario A: Code Generation with Claude Code (Questions 1–15)

Your platform team uses Claude Code across a monorepo. Teams want reusable context without bloating every session, deterministic enforcement for operational controls, and repeatable ways to refine code safely.

**Question 1.** Every contributor must follow the same repository-wide naming and error-handling conventions in every Claude Code session. The guidance changes with the repository and should be reviewed in pull requests. Where should it live?

- A) In each contributor's `~/.claude/CLAUDE.md`.
- B) In an on-demand project skill named `/standards`.
- C) In the repository's project-level `CLAUDE.md`.
- D) In an inline prompt copied into each new session.

**Question 2.** Security conventions apply to every file named `*Controller.ts`, which appears under many unrelated packages. The conventions should load only when Claude edits those files. Which mechanism fits?

- A) A `.claude/rules/` file with a `paths: ["**/*Controller.ts"]` glob.
- B) A `CLAUDE.md` in the first package containing a controller.
- C) A root `CLAUDE.md` section that asks Claude to infer when the rule matters.
- D) A slash command developers invoke before changing controllers.

**Question 3.** A team-wide dependency audit is run only before quarterly releases. It produces lengthy exploratory output that should not remain in the implementation conversation. How should it be packaged?

- A) As several hundred always-loaded lines in the root `CLAUDE.md`.
- B) As a user-level command installed separately by every contributor.
- C) As a path rule that activates whenever any dependency file is read.
- D) As a project skill configured with `context: fork`.

**Question 4.** A deployment tool may run only when its arguments contain both an approved change-ticket ID and the current maintenance-window identifier. Prompt reminders have already been bypassed. What should enforce the rule?

- A) A stronger warning in `CLAUDE.md`.
- B) A `PreToolUse` hook that validates the tool arguments and blocks invalid calls.
- C) A path-scoped rule for deployment manifests.
- D) A custom command that prints the policy and requires the operator to confirm both values before deployment.

**Question 5.** You created a personal `/rewrite-commit` command with an experimental style that should not affect teammates or be committed to the project. Where should it be stored?

- A) `.claude/commands/rewrite-commit.md` in the repository so every teammate receives the experiment.
- B) `~/.claude/commands/rewrite-commit.md` in your user configuration.
- C) The project `CLAUDE.md` under a personal heading.
- D) `.mcp.json` as a prompt definition.

**Question 6.** During one debugging task, Claude needs the exact contents of `docs/legacy-auth-flow.md`. The file is unlikely to matter again after the task. What is the most appropriate way to provide it?

- A) Add its full contents permanently to the root `CLAUDE.md`.
- B) Turn the document into an MCP server.
- C) Create a path rule that loads whenever any source file is edited.
- D) Reference it with `@docs/legacy-auth-flow.md` in the current prompt.

**Question 7.** Everything under `services/payments/` follows one cohesive set of conventions, while no other subtree uses them. The conventions should apply automatically throughout that subtree. What is the simplest placement?

- A) A `CLAUDE.md` inside `services/payments/`.
- B) A personal skill in `~/.claude/skills/`.
- C) A root slash command that developers must remember to invoke.
- D) An MCP resource containing the conventions.

**Question 8.** After every file edit, the team must run the formatter and immediately return any formatting failure to Claude, regardless of whether Claude remembered to run it. Which mechanism provides that behavior?

- A) A formatting paragraph in `CLAUDE.md` and an instruction that Claude invoke it after every edit.
- B) A `PreToolUse` hook on Read operations.
- C) A `PostToolUse` hook matched to file edits.
- D) An `@` reference to the formatter configuration.

**Question 9.** Claude's CSV converter mishandles quoted commas. Repeating “support all valid CSV” has not helped. Which feedback is most likely to produce a reliable correction?

- A) Increase the reasoning budget without showing the failure.
- B) Ask for a completely different implementation with no constraints and compare it manually against a few successful CSV files.
- C) Add the issue permanently to user-level memory.
- D) Provide the failing input, the current output, the exact expected output, and the relevant regression test.

**Question 10.** You are designing an unfamiliar cache invalidation layer and have not decided how freshness, failure recovery, or multi-region writes should behave. Which refinement technique should come before implementation?

- A) Ask Claude to interview you about unresolved design constraints and failure modes.
- B) Generate the simplest cache, let production incidents reveal requirements, and document whatever behavior emerges as product policy.
- C) Put “use best practices” in `CLAUDE.md` and start direct execution.
- D) Ask multiple agents to implement alternatives before clarifying acceptance criteria.

**Question 11.** A refactor has two interacting API changes that share a compatibility constraint, plus an unrelated spelling error. How should you present the feedback during iteration?

- A) Send all three one at a time so each response can be reviewed and merged before the next issue is discussed.
- B) Send all three together because batching is always more efficient.
- C) Describe the interacting API changes together with their shared constraint, and handle the independent spelling fix separately.
- D) Add every issue to `CLAUDE.md` so later sessions can decide the order.

**Question 12.** You need to find every source file whose contents reference `LegacyTokenValidator`, regardless of filename. Which built-in tool is the best starting point?

- A) Glob.
- B) Grep.
- C) Write.
- D) Edit.

**Question 13.** An unfamiliar service has thousands of files. You need to understand how requests reach `authorizePayment` without flooding the context window. What is the strongest exploration strategy?

- A) Search for the symbol and likely entry points, Read only the matching files, then follow relevant imports incrementally.
- B) Read every file under the service before forming any hypothesis.
- C) Glob only for filenames containing `payment`, infer the call flow from names, and use import order as a proxy for runtime behavior.
- D) Run the entire test suite repeatedly and infer architecture from pass/fail output.

**Question 14.** Yesterday's named investigation session contains an accurate repository map, and no relevant files have changed. You want to continue the same work today. What should you do?

- A) Start a blank session and reconstruct everything from scratch.
- B) Fork the session even though no divergent approach is needed.
- C) Copy only the last assistant response into a new conversation.
- D) Resume the named session with `--resume <session-name>`.

**Question 15.** A named session contains useful architectural conclusions, but a major framework upgrade rewrote most analyzed files. What is the most reliable continuation?

- A) Resume unchanged because the conversation still contains the old tool results, and rely on the transcript to identify which files still matter.
- B) Fork the stale session and trust both branches equally.
- C) Start fresh with a structured summary of durable conclusions, identify changed areas, and re-read the affected files.
- D) Discard both the durable conclusions and all repository context.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are standardizing codebase-exploration tools and MCP integrations for a distributed engineering organization. Shared services must work after a clone, while experiments and credentials remain personal.

**Question 16.** Every engineer should receive the same internal issue-tracker MCP server definition from version control, but each engineer has a different access token. What configuration is correct?

- A) Put the server and literal shared token in the root `CLAUDE.md`, then tell every engineer to copy the token into a local file before starting Claude Code.
- B) Commit the server definition in project `.mcp.json` and reference an environment variable for the token.
- C) Ask every engineer to create an unrelated personal skill.
- D) Store the server only in one maintainer's `~/.claude.json`.

**Question 17.** One developer is evaluating an unstable local MCP server that nobody else should see yet. Where should the definition live?

- A) In project `.mcp.json`, commented as experimental.
- B) In the root `CLAUDE.md` so teammates can ignore it.
- C) In `.claude/rules/` with a path that matches only the developer's files.
- D) In that developer's user-scoped `~/.claude.json`.

**Question 18.** Claude Code connects to three configured MCP servers. A teammate proposes writing a router that activates exactly one server for each request. What should you explain?

- A) Tools from all connected servers are discovered at connection time and can be available simultaneously; selection is driven by their contracts and context.
- B) Project servers disable user-scoped servers whenever both are configured.
- C) Claude Code can discover only the first server listed in `.mcp.json` and requires manual reconnection whenever a tool from another server is needed.
- D) MCP resources, rather than tools, select which server becomes active.

**Question 19.** A committed `.mcp.json` currently contains a plaintext production token. What is the correct credential pattern?

- A) Base64-encode the token in the same file.
- B) Move the token into a comment so Claude does not read it.
- C) Replace it with environment-variable expansion such as `${INTERNAL_MCP_TOKEN}`.
- D) Put the token in a project slash command.

**Question 20.** The team needs a standard Jira integration, and a well-maintained community MCP server already meets the requirements. When is a custom server justified instead?

- A) Only when team-specific behavior or interfaces are not provided by an appropriate existing server.
- B) Whenever an integration will be shared by more than one developer, so its definition remains consistent across machines and repositories.
- C) Whenever authentication uses an environment variable.
- D) Always, because community servers cannot be project-scoped.

**Question 21.** Agents repeatedly call `list_services` and `list_tables` just to discover what internal data exists before choosing a real operation. What MCP feature should expose those catalogs efficiently?

- A) A `PostToolUse` hook.
- B) A forced write tool.
- C) MCP resources describing the available services and schemas.
- D) A larger user-level `CLAUDE.md` containing copied live data.

**Question 22.** You need an inventory of files named `Dockerfile`, `Dockerfile.dev`, or `service.Dockerfile` across the repository. Which built-in tool should start the search?

- A) Read every service root.
- B) Grep for the text `FROM`.
- C) Edit the build configuration.
- D) Glob using filename patterns.

**Question 23.** Glob found four candidate configuration files. You now need the complete surrounding structure of one 120-line file before deciding where a setting is inherited. What should you use?

- A) Grep for a single key and ignore the rest of the file.
- B) Read the selected file.
- C) Write a replacement configuration.
- D) Bash-delete the other candidates.

**Question 24.** A production log contains the exact message `permission cache exhausted`, and you need to locate where that text is emitted. Which tool is most direct?

- A) Glob for files with `cache` in their names.
- B) Read the whole repository sequentially.
- C) Grep for the exact message.
- D) Edit likely logging files until the message changes.

**Question 25.** You must trace how a CLI command reaches a database adapter in an unfamiliar repository. Which sequence best manages context?

- A) Read every Python file, then search after the context is full and infer the database route from whichever file was read last.
- B) Locate command registration with Grep/Glob, Read the matches, and follow only the relevant imports and calls.
- C) Infer the route from directory names and skip file contents.
- D) Ask a generic coding question without repository evidence.

**Question 26.** Claude confuses `search_source_code` with `search_runbooks`. Both descriptions currently say “search company content.” What is the best first correction?

- A) Force `search_source_code` for every query containing the word “error.”
- B) Put both operations behind a third generic `search` tool.
- C) Give the agent more tools and allow it to call them all before choosing which result should drive the task.
- D) Rewrite each description with distinct use cases, accepted inputs, outputs, examples, boundaries, and when to prefer the other tool.

**Question 27.** `analyze_content` handles web snippets while `analyze_document` handles uploaded files, but their names and descriptions overlap. What redesign most directly improves selection?

- A) Rename the first to a web-specific operation and make both contracts explicitly source-specific.
- B) Keep the overlap, add “choose carefully” to the system prompt, and require Claude to explain its choice after the selected tool has already run.
- C) Randomize between the tools and compare outputs later.
- D) Force both tools on every item.

**Question 28.** Detailed tool descriptions look correct, yet a system prompt says “for any investigation, always begin with the archive tool.” Claude keeps ignoring a better live-search tool. What should you inspect?

- A) Whether the archive tool's JSON schema has alphabetized properties and whether its server connected before the live-search server.
- B) Keyword-sensitive prompt instructions that override or bias normal tool selection.
- C) Whether the tools appear in different MCP servers.
- D) Whether the response token limit is high enough.

**Question 29.** A source-control MCP tool times out. The agent must know whether to retry and what operation failed. What should the tool return?

- A) A successful empty list so the workflow continues.
- B) The text “something went wrong” without an error flag, plus a `CLAUDE.md` suggestion that Claude decide whether the string represents data or failure.
- C) `isError` plus a transient category, retryability, attempted operation, safe description, and suggested next action.
- D) Only the provider's raw stack trace.

**Question 30.** A code search completes successfully and finds no references. How should the tool represent this outcome?

- A) As a retryable transient error because the result is empty.
- B) As a permission error so the coordinator investigates access.
- C) As a business-rule failure requiring human escalation.
- D) As a successful empty result, distinct from any tool failure.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

Your research coordinator handles requests ranging from routine comparisons to open-ended investigations. It must choose decomposition strategies based on the work rather than blindly running a fixed pipeline.

**Question 31.** A compliance review always checks the same four known controls, while an incident investigation must branch based on each new log or dependency discovered. Which design is appropriate?

- A) Dynamic decomposition for both because all agent work should branch.
- B) One large prompt for both to avoid coordination overhead.
- C) A fixed chain for both so the step count is predictable and auditability takes priority over evidence discovered during the investigation.
- D) A fixed chain for the repeatable control review and dynamic decomposition for the investigation.

**Question 32.** The request is “add comprehensive tests to this unknown legacy service.” What should the coordinator do first?

- A) Generate one test file for every source file immediately.
- B) Map the service, identify high-impact behavior and dependencies, then create subtasks that adapt to what the map reveals.
- C) Apply the same fixed list of unit-test prompts used for every repository and rerun it unchanged whenever a test exposes a new dependency.
- D) Delegate only to a test-writer and prohibit further exploration.

**Question 33.** A simple factual query needs one authoritative source, but the coordinator always invokes search, document analysis, statistics, synthesis, and report agents. What is the best change?

- A) Keep the pipeline but shorten every agent's response so latency and cost remain predictable for every query.
- B) Cache every specialist's last answer.
- C) Let the coordinator select only the specialists justified by the query and intermediate findings.
- D) Replace all specialists with one unrestricted agent.

**Question 34.** A broad market study omits regional regulation because the coordinator decomposed it only by product feature. How should decomposition be improved?

- A) Partition the full scope across complementary dimensions or source types, then verify coverage before synthesis.
- B) Ask the synthesis agent to invent a regulatory section from general knowledge and label it as an informed architectural estimate.
- C) Make every existing subtask longer without changing scope.
- D) Remove the coverage requirement to match the available research.

**Question 35.** An open-ended performance investigation has not yet established which component is slow. What is the strongest initial subtask?

- A) Rewrite the database layer because it is commonly slow, even if later measurements implicate a different component.
- B) Ask every specialist to optimize its favorite component.
- C) Measure and map the request path first, then generate prioritized subtasks from the observed bottlenecks.
- D) Execute a fixed sequence of generic optimizations.

**Question 36.** Forty files need the same predictable local checklist, followed by one cross-file compatibility review. Which decomposition best preserves depth?

- A) Run focused per-file passes and then a separate integration pass.
- B) Use an open-ended dynamic investigation for every file even though the stages are known.
- C) Put all files in one prompt and ask Claude to divide attention evenly.
- D) Skip the integration pass because every local result passed.

**Question 37.** A dependency audit discovers midway that two services share a generated client, invalidating several planned subtasks. What should the coordinator do?

- A) Finish the original task list before acknowledging the dependency so the plan remains comparable with prior audit runs and reports.
- B) Revise the plan and generate replacement subtasks that account for the shared client.
- C) Restart the entire investigation without preserving valid findings.
- D) Hide the discovery from specialists so assignments remain stable.

**Question 38.** Which coordinator behavior most clearly distinguishes adaptive decomposition from a fixed workflow?

- A) It uses the same specialists in a different order each run while preserving the predefined task list and completion conditions.
- B) It runs all predefined steps in parallel.
- C) It asks for longer reports when evidence is thin.
- D) It creates or revises subtasks in response to intermediate discoveries and remaining coverage gaps.

**Question 39.** Initial synthesis is strong but lacks evidence for one geography. What should an iterative coordinator do?

- A) Identify the gap, delegate a targeted follow-up search, then resynthesize with the new evidence.
- B) Add a generic disclaimer and stop despite the recoverable gap.
- C) Restart every completed subtask from scratch.
- D) Ask the synthesis agent to fill the section without sources and cite the originally assigned material despite its missing geographic coverage.

**Question 40.** A specialist repeatedly maps “active users” to total registered accounts. Which feedback is most useful?

- A) Tell it to think harder about metrics.
- B) Raise the maximum output length.
- C) Replace the agent without describing the observed failure and ask the replacement to infer the intended definition from previous reports.
- D) Provide representative inputs, the incorrect mappings, the desired mappings, and a precise definition of “active.”

**Question 41.** Three findings arise from the same mistaken date-window assumption and will interact if fixed separately. How should the coordinator request refinement?

- A) Send each issue in isolation and withhold the shared assumption so every specialist can optimize its correction independently.
- B) Batch the related issues in one detailed request that explains their common dependency.
- C) Fix only the easiest finding and ignore the rest.
- D) Add the errors to permanent user memory.

**Question 42.** You resume a research session after editing three previously analyzed parsers. Most other context remains valid. What should you tell the agent?

- A) Nothing; resumption automatically detects every filesystem change.
- B) Re-read the entire repository because targeted recovery is impossible.
- C) Name the changed files and request targeted re-analysis while retaining unaffected findings.
- D) Trust the old parser outputs because named resumption snapshots the current filesystem before the next answer.

**Question 43.** You want two independent research strategies to begin from the same accepted source map without contaminating one another. What mechanism fits?

- A) Resume the same session in two terminals.
- B) Copy only the user prompt into two blank sessions.
- C) Run both strategies sequentially in one conversation.
- D) Use `fork_session` to branch from the shared baseline.

**Question 44.** A research agent has `search_news` and `search_academic`, but the latter is almost never chosen even for peer-reviewed-evidence requests. What should its description add?

- A) A promise that it is always better than every other tool and an instruction to prefer it whenever the user requests credible evidence.
- B) Its indexed sources, accepted query/date inputs, output metadata, example academic requests, and explicit contrast with news search.
- C) Internal implementation details unrelated to selection.
- D) A requirement that both tools run for every query.

**Question 45.** A search specialist sees a transient timeout that succeeds on a safe local retry. What error-handling structure best protects coordinator context?

- A) Let the specialist recover locally; propagate only unresolved failure context, attempts, and partial results.
- B) Propagate every first failure immediately, let the coordinator retry it, and preserve a full transcript of every attempt in the main context.
- C) Hide all failures, including permanent ones, from the coordinator.
- D) Terminate every subagent when any tool reports an error.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

Your extraction service handles invoices, contracts, résumés, and scanned forms. A strict schema is already available, but accuracy varies across layouts and operational edge cases.

**Question 46.** Invoice extraction works on the layout used in the prompt but fails when totals appear in tables, footnotes, or sidebars. What is the strongest improvement?

- A) Make every field required so Claude searches harder.
- B) Retry the same prompt until one run succeeds.
- C) Add varied few-shot examples with correct outputs and explicit normalization guidance while retaining the structured schema.
- D) Replace tool use with free-form prose and require downstream code to parse whichever layout-specific explanation the model returns.

**Question 47.** Dates appear as `03/04/26`, `4 March 2026`, and `2026-03-04`, while downstream systems require ISO 8601. What should accompany the schema?

- A) Explicit normalization instructions, including how to represent genuinely ambiguous dates rather than guessing.
- B) Copy all date strings unchanged, then require downstream systems to infer locale from the customer account and vendor country.
- C) A higher confidence threshold with no format rule.
- D) A retry policy that omits the original date.

**Question 48.** Some contracts legitimately contain no renewal date. The current required string field causes invented dates. What is the best correction?

- A) Keep the field required, add “do not hallucinate,” and reject any fabricated date through downstream validation in every run.
- B) Make the field optional or nullable and instruct the model to use null when the source is silent.
- C) Reject every contract without a renewal date.
- D) Derive a date from the contract's signing date.

**Question 49.** Résumé extraction works for conventional corporate résumés but misses existing education and publication fields on academic CVs. Which change is most likely to generalize?

- A) Add a rule for the exact CV that failed and a growing exception for every new university template.
- B) Force missing fields to empty strings.
- C) Increase temperature so the model explores more sections.
- D) Add representative examples showing the same target fields across corporate, academic, and international layouts.

**Question 50.** A scanned form omitted the page containing the requested identifier. Validation fails on every retry. What should the system do?

- A) Recognize that the information is absent, stop model retries, and route to rescanning, null handling, or review.
- B) Retry indefinitely with stronger wording.
- C) Ask Claude to infer the identifier from neighboring records and label it model-generated so downstream teams know it was not scanned.
- D) Mark the extraction successful with a fabricated placeholder.

**Question 51.** An extraction is schema-valid but fails a business check because line-item totals do not equal the stated subtotal. What should a corrective follow-up include?

- A) Only the phrase “try again.”
- B) Provide only the failed subtotal and a generic instruction to change whichever value appears least plausible.
- C) The original document, failed extraction, and specific validation discrepancy.
- D) A random alternative subtotal that passes validation.

**Question 52.** Tool use guarantees that output conforms to the JSON schema, but customer names are occasionally placed in the vendor field. What does this demonstrate?

- A) Strict schemas eliminate both syntax and semantic extraction errors.
- B) Semantic validation and representative examples are still needed after structural compliance.
- C) The schema should be removed because it caused the field swap.
- D) A larger output token limit will correct field meaning.

**Question 53.** Payment methods are represented by a fixed enum, but valid new methods appear regularly. How should the schema avoid forced misclassification?

- A) Include an `other` value with a detail field, and an `unclear` representation when the source is ambiguous.
- B) Map every unfamiliar method to the closest existing category and update a hard-coded category list every quarter.
- C) Reject every document containing an unfamiliar value.
- D) Replace the entire structured response with prose.

**Question 54.** A document has clear header fields but an illegible handwritten approval box. Routing is currently based on one document-level confidence average. What is better?

- A) Randomly review ten percent of documents regardless of field quality.
- B) Review every document and require the reviewer to re-enter all header fields as well as interpret the approval box.
- C) Accept every document whose average confidence exceeds 0.9.
- D) Route based on field-level confidence, field risk, and the handwritten ambiguity while allowing clear fields to proceed.

**Question 55.** The team proposes auto-accepting fields above confidence 0.92 because the number “sounds safe.” How should the threshold be selected?

- A) Use 0.99 for every field without testing.
- B) Average the confidence values produced last week.
- C) Calibrate scores against labeled outcomes by field and document segment, then choose thresholds that meet the required accuracy.
- D) Let each model response choose its own threshold without calibration and store that number for downstream systems to trust.

**Question 56.** High-confidence extractions now bypass normal human review. How can the team detect new error patterns that the confidence model does not recognize?

- A) Review only low-confidence failures.
- B) Continuously review a stratified random sample of auto-accepted outputs.
- C) Trust the original benchmark indefinitely.
- D) Retry a random sample without human labels and treat agreement between the two runs as proof that the original was correct.

**Question 57.** Which review policy best uses document characteristics and ambiguity?

- A) Route every hundredth document to a random reviewer.
- B) Review every field in low-confidence documents with one generalist, even when only a single field is ambiguous.
- C) Assign reviewers by arrival order to keep routing simple.
- D) Route uncertain or high-risk fields to reviewers with relevant expertise, using confidence and source characteristics as signals.

**Question 58.** The model confuses `extract_invoice` and `extract_purchase_order` when both documents contain totals and vendor names. What is the best tool-interface improvement?

- A) Give each tool explicit document cues, unique outputs, boundary examples, and guidance for distinguishing the two formats.
- B) Force invoice extraction for every financial document.
- C) Rename both tools to shorter generic names.
- D) Ask downstream code to infer document type from whichever fields happen to be populated most often during every extraction.

**Question 59.** A refund extraction requests an amount prohibited by policy. Retrying cannot change the policy result. What should the tool surface?

- A) A transient retryable error with unlimited attempts so temporary and permanent policy outcomes share one recovery path.
- B) A successful empty response.
- C) A structured non-retryable business error with a customer-safe explanation and permitted next action.
- D) Only an internal policy stack trace.

**Question 60.** An extraction tool cannot open a restricted document collection. Which response gives the agent the clearest recovery path?

- A) A generic “operation failed” message.
- B) A structured permission error marked non-retryable without changed access, with a suggestion to request access or escalate.
- C) A valid empty extraction object.
- D) A transient category that retries until the same restricted collection has failed a fixed number of times before escalation.

---

# Answer Key — Practice Exam 13

**Quick key:** 1-C, 2-A, 3-D, 4-B, 5-B, 6-D, 7-A, 8-C, 9-D, 10-A, 11-C, 12-B, 13-A, 14-D, 15-C, 16-B, 17-D, 18-A, 19-C, 20-A, 21-C, 22-D, 23-B, 24-C, 25-B, 26-D, 27-A, 28-B, 29-C, 30-D, 31-D, 32-B, 33-C, 34-A, 35-C, 36-A, 37-B, 38-D, 39-A, 40-D, 41-B, 42-C, 43-D, 44-B, 45-A, 46-C, 47-A, 48-B, 49-D, 50-A, 51-C, 52-B, 53-A, 54-D, 55-C, 56-B, 57-D, 58-A, 59-C, 60-B

**Focus key:** 1-CFG, 2-CFG, 3-CFG, 4-CFG, 5-CFG, 6-CFG, 7-CFG, 8-CFG, 9-REF, 10-REF, 11-REF, 12-EXP, 13-EXP, 14-RES, 15-RES, 16-MCP, 17-MCP, 18-MCP, 19-MCP, 20-MCP, 21-MCP, 22-EXP, 23-EXP, 24-EXP, 25-EXP, 26-DESC, 27-DESC, 28-DESC, 29-ERR, 30-ERR, 31-DEC, 32-DEC, 33-DEC, 34-DEC, 35-DEC, 36-DEC, 37-DEC, 38-DEC, 39-REF, 40-REF, 41-REF, 42-RES, 43-RES, 44-DESC, 45-ERR, 46-EXT, 47-EXT, 48-EXT, 49-EXT, 50-EXT, 51-EXT, 52-EXT, 53-EXT, 54-REV, 55-REV, 56-REV, 57-REV, 58-DESC, 59-ERR, 60-ERR

Focus codes: CFG = Claude Code configuration selection; MCP = MCP scope and integration; DEC = adaptive decomposition; EXT = extraction accuracy; REF = iterative refinement; EXP = codebase exploration; DESC = tool descriptions; RES = session resumption; REV = human-review routing; ERR = MCP error handling.

---

**1. C** — Shared, durable, always-applied repository guidance belongs in the committed project `CLAUDE.md`. User memory is personal, a skill is on demand, and repeated inline prompts are not reliably shared.

**2. A** — A path-scoped rule follows matching controller files across unrelated directories and loads only for those files. Directory memory misses scattered locations, root memory loads too broadly, and a command is not automatic.

**3. D** — An occasional reusable workflow belongs in a skill, and `context: fork` keeps its verbose exploration out of the main conversation. The other placements either load it constantly, make it personal, or activate it for unrelated file work.

**4. B** — The rule depends on live tool arguments and must be deterministic, so a `PreToolUse` hook should validate and block before execution. Documentation and commands remain advisory; a file-path rule cannot inspect the required operational state.

**5. B** — User-scoped commands are personal and are not distributed through the repository. A project command would affect teammates, while `CLAUDE.md` and MCP configuration are different mechanisms.

**6. D** — An `@` reference supplies a known relevant file to the current task without permanently consuming future context. The other choices make one-time context durable or introduce unrelated infrastructure.

**7. A** — A directory-level `CLAUDE.md` is the natural automatic scope for one cohesive subtree. Skills require invocation, and commands or MCP resources do not provide inherited directory guidance.

**8. C** — `PostToolUse` runs after the edit and can invoke the formatter and return failures to Claude every time. A prose instruction is probabilistic, PreToolUse is the wrong event, and an `@` reference does not execute checks.

**9. D** — A concrete failing input, observed output, expected output, and regression test give Claude an exact correction target and preserve the fix. More effort without evidence and permanent memory do not clarify the transformation.

**10. A** — The interview pattern surfaces missing product and failure-mode decisions before code hardens accidental assumptions. Implementing first or multiplying implementations cannot resolve requirements that have not been decided.

**11. C** — Interacting issues should be presented together with their shared constraints, while independent issues can be iterated separately. Universal “always batch” or “always sequence” rules ignore dependency structure.

**12. B** — Grep searches file contents for symbol references. Glob searches paths, while Write and Edit mutate files rather than discover usages.

**13. A** — Targeted search followed by selective Read and import tracing builds understanding incrementally without filling context. Reading everything wastes the window, and names or test output alone do not establish the call path.

**14. D** — Named resumption is appropriate when prior context and tool results remain valid and the goal is unchanged. Forking is for divergence, and starting over discards reliable work.

**15. C** — Major file changes make old tool results stale, so a fresh session seeded with durable conclusions and targeted re-reading is safer than resuming or forking stale evidence. Discarding durable architecture facts is unnecessary.

**16. B** — Project `.mcp.json` distributes shared tooling, while environment expansion supplies per-user credentials without committing secrets. User scope is not shared, and neither skills nor `CLAUDE.md` configure the server.

**17. D** — Personal or experimental servers belong in user-scoped `~/.claude.json`. Committing an unstable server exposes it to the team even if comments or path rules try to limit it.

**18. A** — Tools from connected MCP servers are discovered together and made available to the agent; clear contracts and context guide selection. There is no required one-active-server router or first-server-only rule.

**19. C** — Environment-variable expansion keeps the secret outside version control while leaving the server definition shareable. Encoding, comments, and commands do not secure a committed credential.

**20. A** — Existing maintained servers are preferred for standard integrations; custom work is warranted for team-specific contracts or behavior not otherwise available. Scope and authentication do not by themselves require a custom server.

**21. C** — MCP resources expose catalogs and reference structures without repeated exploratory tool calls. Hooks intercept events, and copying live catalogs into memory creates stale, bloated context.

**22. D** — Glob is designed for matching file paths and naming variants. Grep searches contents; reading every root is slower and less precise.

**23. B** — Once candidates are narrowed, Read supplies the selected file's full local context. A single Grep match can hide inheritance structure, and mutation is premature.

**24. C** — An exact log string is a content-search problem, so Grep is direct. Filename guesses and exhaustive reads are weaker; Edit should follow diagnosis, not replace it.

**25. B** — Incremental discovery narrows candidates before reading and follows only evidence-bearing relationships. Reading everything exhausts context, while inference without file evidence is unreliable.

**26. D** — Tool descriptions are the model's primary selection signal and should differentiate purpose, formats, outputs, examples, edges, and neighboring tools. Forced keyword routing, generic consolidation, and more tools preserve the ambiguity.

**27. A** — Source-specific names and contracts move the distinction into the interface the model selects. Warnings, randomness, and always calling both do not remove overlapping semantics.

**28. B** — System-prompt wording can create keyword associations that overpower good descriptions. Property ordering, server placement, and response length do not explain the mandated archive preference.

**29. C** — Structured error type, retryability, attempted action, and next steps let the agent choose a recovery path. Empty success hides failure, generic text is not actionable, and raw traces are unsafe and incomplete.

**30. D** — No matches is a valid successful query result and must remain distinct from access or operational failures. Mislabeling it prompts wasteful retries or unnecessary escalation.

**31. D** — Known repeatable stages suit a fixed chain, while evidence-driven incident work needs adaptive decomposition. One decomposition style is not optimal for both predictable and open-ended work.

**32. B** — An unknown legacy system must first be mapped so high-impact behavior and dependencies can drive the testing plan. Immediate file-by-file generation is a fixed guess and can miss integration risk.

**33. C** — The coordinator should scale delegation to query complexity and what is discovered. Making an unnecessary full pipeline cheaper or caching irrelevant work does not remove it.

**34. A** — Broad work needs complementary scope partitioning and a coverage check so no major dimension vanishes. Longer reports cannot recover an unassigned region, and synthesis must not fabricate it.

**35. C** — Measurement and mapping identify actual bottlenecks, after which subtasks can adapt to evidence. Generic or preference-based optimization starts with unsupported assumptions.

**36. A** — Predictable local checks benefit from focused per-file passes, and a separate integration pass catches cross-file behavior. One mega-prompt dilutes attention, while skipping integration leaves an explicit gap.

**37. B** — Adaptive plans change when a newly discovered dependency invalidates prior assumptions, preserving still-valid findings while replacing affected work. Blind completion and wholesale restart are both wasteful.

**38. D** — Creating and revising subtasks from intermediate findings is the defining adaptive behavior. Reordering or parallelizing a fixed list does not change what work is generated.

**39. A** — Iterative orchestration evaluates synthesis, identifies a specific gap, commissions targeted evidence, and resynthesizes. Disclaiming or inventing content skips a recoverable refinement step.

**40. D** — Examples of the failure and desired mapping plus an exact definition teach the disputed boundary. Generic effort, length, or agent replacement supplies no corrective evidence.

**41. B** — Related failures caused by one assumption should be evaluated together so the fix is coherent. Isolating them hides the interaction; permanent memory is not an issue tracker.

**42. C** — A resumed agent must be told what changed so it can refresh affected evidence without repeating valid exploration. Session history does not automatically know filesystem changes.

**43. D** — `fork_session` preserves the accepted baseline while isolating divergent reasoning. Concurrent resume shares the same branch, blank sessions lose context, and sequential work contaminates the comparison.

**44. B** — Selection improves when the academic tool says what it indexes, how to query it, what it returns, and when it wins over news search. Boasts, implementation trivia, and mandatory dual calls are not useful boundaries.

**45. A** — Specialists should recover locally from safe transient failures and spare coordinator context; unresolved errors should include attempts and usable partial results. Immediate propagation and total suppression are both brittle.

**46. C** — Diverse positive examples teach field-location patterns across layouts, while normalization guidance and schema enforcement preserve consistency. Repeated identical prompts and required fields do not teach layout variation.

**47. A** — The prompt must state the canonical format and define what to do when source notation is ambiguous. Confidence alone cannot decide day/month order, and silent guessing corrupts data.

**48. B** — Optional or nullable fields faithfully represent genuine absence and remove pressure to fabricate. Rejection or derivation invents a business rule the source does not support.

**49. D** — Representative layout diversity teaches transferable extraction behavior across document families. A one-off rule overfits, and temperature or forced empty strings do not locate existing information.

**50. A** — Retries cannot recover content missing from the source, so the system must stop and choose an operational path such as rescanning, null, or review. Guessing and indefinite retries manufacture confidence without evidence.

**51. C** — Corrective retries need the evidence, failed candidate, and exact validation error so the model can repair the semantic defect. A vague retry or invented value cannot ground the correction.

**52. B** — A schema guarantees shape, not that evidence was mapped to the correct field. Semantic validators and examples still define meaning and catch swaps.

**53. A** — `other` plus detail preserves novel valid values, while `unclear` represents ambiguity without guessing. Nearest-category mapping and rejection both lose source truth.

**54. D** — Field-level routing isolates the ambiguous, risky approval box while preserving clear header extraction. A document average can hide critical field uncertainty, and blanket or random review wastes effort.

**55. C** — Confidence scores become actionable only after calibration against labeled outcomes at the relevant field and segment. An intuitive number has no demonstrated relationship to accuracy.

**56. B** — Stratified sampling of auto-accepted output detects blind spots and distribution drift that confidence alone misses. Reviewing only known failures cannot reveal unknown high-confidence errors.

**57. D** — Effective routing combines ambiguity, field risk, source characteristics, and reviewer expertise. Random or aggregate-only routing ignores where uncertainty actually resides.

**58. A** — Similar document tools need explicit discriminators, examples, and distinct output contracts. Forced defaults, generic names, and downstream guessing leave the selection ambiguity intact.

**59. C** — A policy violation is a non-retryable business outcome and should include a safe explanation and allowed alternative. Treating it as transient wastes calls; empty success conceals the reason.

**60. B** — A typed permission error tells the agent that retries will not help until access changes and provides a concrete escalation path. Generic, empty, or transient responses drive the wrong behavior.

*End of Practice Exam 13.*
