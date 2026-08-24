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

- A) In each contributor's personal `~/.claude/CLAUDE.md`, which loads regardless of repository.
- B) In an on-demand skill named `/standards` that a contributor must remember to invoke first.
- C) In the repository's project-level `CLAUDE.md`, committed alongside the code, reviewed in pull requests, and versioned like any other file in the tree.
- D) In an inline prompt block that gets pasted into the start of each new session before work begins.

**Question 2.** Security conventions apply to every file named `*Controller.ts`, which appears under many unrelated packages. The conventions should load only when Claude edits those files. Which mechanism fits?

- A) A `.claude/rules/` file scoped with a `paths` glob matching `*Controller.ts` everywhere.
- B) A `CLAUDE.md` placed in whichever package happens to contain the first controller file the team wrote.
- C) A root `CLAUDE.md` section that lists the convention once and asks Claude to infer when it applies from surrounding context.
- D) A slash command developers invoke before changing controllers, since no hook currently watches that path automatically.

**Question 3.** A team-wide dependency audit is run only before quarterly releases. It produces lengthy exploratory output that should not remain in the implementation conversation. How should it be packaged?

- A) As a large block appended to the root `CLAUDE.md` so every session always carries the audit checklist.
- B) As a user-level command each contributor must separately install and keep synchronized across their own `~/.claude` configuration.
- C) As a path rule that reloads its exploratory instructions whenever any dependency manifest file happens to be read.
- D) As a project skill configured with `context: fork`, invoked only before releases.

**Question 4.** A deployment tool may run only when its arguments contain both an approved change-ticket ID and the current maintenance-window identifier. Prompt reminders have already been bypassed. What should enforce the rule?

- A) A stronger warning added to `CLAUDE.md` asking Claude to double-check both IDs.
- B) A `PreToolUse` hook that inspects the tool's arguments before execution and blocks the call outright unless both the ticket ID and the window ID are present.
- C) A path-scoped rule that loads reminder text whenever a deployment manifest file is opened.
- D) A custom command that prints the policy and asks the operator to confirm both values before deployment begins.

**Question 5.** You created a personal `/rewrite-commit` command with an experimental style that should not affect teammates or be committed to the project. Where should it be stored?

- A) `.claude/commands/rewrite-commit.md` committed so every teammate receives it.
- B) `~/.claude/commands/rewrite-commit.md` in your personal user configuration, kept invisible to the rest of the team and never checked into the shared repository.
- C) A personal heading inside the shared project `CLAUDE.md` that only you are supposed to read.
- D) A prompt definition added to `.mcp.json` alongside the team's server configuration.

**Question 6.** During one debugging task, Claude needs the exact contents of `docs/legacy-auth-flow.md`. The file is unlikely to matter again after the task. What is the most appropriate way to provide it?

- A) Add its full contents permanently to the root `CLAUDE.md`, blurring the line between durable and one-off context.
- B) Turn the document into a dedicated MCP server just so this one file can be fetched on demand.
- C) Load it through a path rule that fires whenever any source file, not just this one, gets edited.
- D) Reference it with `@docs/legacy-auth-flow.md` directly in the current prompt for this task only.

**Question 7.** Everything under `services/payments/` follows one cohesive set of conventions, while no other subtree uses them. The conventions should apply automatically throughout that subtree. What is the simplest placement?

- A) A `CLAUDE.md` placed directly inside `services/payments/`, so it loads automatically for anyone working in that subtree.
- B) A personal skill kept in `~/.claude/skills/`, invoked manually by whoever remembers it.
- C) A root-level slash command developers must remember to run first.
- D) An MCP resource that stores the conventions as data a server happens to expose.

**Question 8.** After every file edit, the team must run the formatter and immediately return any formatting failure to Claude, regardless of whether Claude remembered to run it. Which mechanism provides that behavior?

- A) A formatting paragraph added to `CLAUDE.md`, trusting Claude to remember to invoke it after every edit.
- B) A `PreToolUse` hook attached to Read operations, checked before the file is even opened.
- C) A `PostToolUse` hook matched to file-edit events, run automatically after every edit completes.
- D) An `@` reference pointing at the formatter's configuration file for context only.

**Question 9.** Claude's CSV converter mishandles quoted commas. Repeating “support all valid CSV” has not helped. Which feedback is most likely to produce a reliable correction?

- A) Ask for more reasoning effort on the retry, without ever showing Claude the failing example.
- B) Ask for a completely different implementation with no constraints, then eyeball it against a few CSV files that already worked.
- C) Add the recurring issue permanently to user-level memory so future sessions inherit the note.
- D) Provide the failing input, the current output, the exact expected output, and the relevant regression test.

**Question 10.** You are designing an unfamiliar cache invalidation layer and have not decided how freshness, failure recovery, or multi-region writes should behave. Which refinement technique should come before implementation?

- A) Ask Claude to interview you about unresolved product decisions and failure-mode requirements before any code is written.
- B) Generate the simplest cache implementation, let production incidents reveal the real requirements, and record whatever behavior results as policy.
- C) Put a one-line "use best practices" note in `CLAUDE.md` and move straight to direct execution.
- D) Ask several agents to each implement a different alternative before the acceptance criteria have been clarified.

**Question 11.** A refactor has two interacting API changes that share a compatibility constraint, plus an unrelated spelling error. How should you present the feedback during iteration?

- A) Send all three items one at a time, waiting for each response to be reviewed and merged before raising the next.
- B) Send all three together in one message, since batching every kind of feedback is always the more efficient approach.
- C) Describe the two interacting API changes together with their shared constraint, and raise the unrelated spelling fix separately.
- D) Add all three issues as notes in `CLAUDE.md` and let whichever session picks it up next decide the order.

**Question 12.** You need to find every source file whose contents reference `LegacyTokenValidator`, regardless of filename. Which built-in tool is the best starting point?

- A) Glob, since it is built to enumerate paths rather than inspect file contents.
- B) Grep, since it searches file contents for the symbol regardless of filename.
- C) Write, which creates or overwrites a file rather than searching anything.
- D) Edit, which modifies an existing file's contents rather than searching for one.

**Question 13.** An unfamiliar service has thousands of files. You need to understand how requests reach `authorizePayment` without flooding the context window. What is the strongest exploration strategy?

- A) Search for the symbol and likely entry points, Read only the matching files, then follow relevant imports incrementally.
- B) Read every file under the service in full before forming any hypothesis about the call path.
- C) Glob only for filenames containing "payment," infer the flow from names, and treat import order as a proxy for runtime behavior.
- D) Run the entire test suite repeatedly and try to infer the architecture from pass/fail output alone.

**Question 14.** Yesterday's named investigation session contains an accurate repository map, and no relevant files have changed. You want to continue the same work today. What should you do?

- A) Start a completely blank session and reconstruct the repository map from scratch.
- B) Fork the session even though no divergent approach or comparison is actually needed here.
- C) Copy only yesterday's final assistant response into a brand-new conversation.
- D) Resume the named session directly with `--resume <session-name>`, since the repository map is still accurate.

**Question 15.** A named session contains useful architectural conclusions, but a major framework upgrade rewrote most analyzed files. What is the most reliable continuation?

- A) Resume unchanged, since the conversation still contains the old tool results and the transcript can identify which files still matter.
- B) Fork the stale session and treat both resulting branches as equally reliable going forward.
- C) Start fresh with a written summary of durable conclusions, identify changed areas, and re-read the affected files.
- D) Discard both the durable architectural conclusions and all prior repository context.

---

## Scenario B: Developer Productivity with Claude (Questions 16–30)

You are standardizing codebase-exploration tools and MCP integrations for a distributed engineering organization. Shared services must work after a clone, while experiments and credentials remain personal.

**Question 16.** Every engineer should receive the same internal issue-tracker MCP server definition from version control, but each engineer has a different access token. What configuration is correct?

- A) Put the server and the literal shared token directly in root `CLAUDE.md`, then ask each engineer to copy the token to a local file first.
- B) Commit the server definition in project `.mcp.json` and reference an environment variable for the token.
- C) Ask every engineer to create an unrelated personal skill that has nothing to do with the issue tracker.
- D) Store the server definition only in one maintainer's personal `~/.claude.json`.

**Question 17.** One developer is evaluating an unstable local MCP server that nobody else should see yet. Where should the definition live?

- A) In project `.mcp.json`, marked with a comment that calls it experimental.
- B) In the root `CLAUDE.md`, on the theory that teammates will simply ignore it.
- C) In `.claude/rules/` with a path scoped to that developer's files.
- D) In that developer's personal, user-scoped `~/.claude.json`, which is never committed or seen by anyone else on the team.

**Question 18.** Claude Code connects to three configured MCP servers. A teammate proposes writing a router that activates exactly one server for each request. What should you explain?

- A) Tools from every connected server are discovered together; selection follows their contracts and context, not a single active server.
- B) Project-scoped servers automatically disable any user-scoped server whenever both happen to be configured for the same session at once.
- C) Claude Code can only discover the first server listed in `.mcp.json` and needs a manual reconnect for any other tool.
- D) MCP resources, rather than tool contracts, are what determine which server becomes active for a request.

**Question 19.** A committed `.mcp.json` currently contains a plaintext production token. What is the correct credential pattern?

- A) Base64-encode the token and leave the encoded value in the same committed file.
- B) Move the token into a code comment on the theory that Claude will not read comments.
- C) Replace it with environment-variable expansion, such as `${INTERNAL_MCP_TOKEN}`, so the secret never gets committed to version control.
- D) Put the token inside a project slash command definition instead.

**Question 20.** The team needs a standard Jira integration, and a well-maintained community MCP server already meets the requirements. When is a custom server justified instead?

- A) Only when the team needs behavior or interfaces that no existing well-maintained server already provides.
- B) Whenever more than one developer will share an integration, so its definition stays identical across every machine and repository.
- C) Whenever the integration happens to authenticate using an environment variable.
- D) Always, since community servers can never be scoped to a single project.

**Question 21.** Agents repeatedly call `list_services` and `list_tables` just to discover what internal data exists before choosing a real operation. What MCP feature should expose those catalogs efficiently?

- A) A `PostToolUse` hook that fires after each discovery call completes.
- B) A forced write tool that records catalog lookups somewhere else.
- C) MCP resources describing the available services and their schemas.
- D) A larger user-level `CLAUDE.md` containing a copy of the live catalog data.

**Question 22.** You need an inventory of files named `Dockerfile`, `Dockerfile.dev`, or `service.Dockerfile` across the repository. Which built-in tool should start the search?

- A) Read every service root directory looking for matching filenames by hand.
- B) Grep for the literal text `FROM`, since that line appears in most Dockerfiles.
- C) Edit the build configuration to see which file responds.
- D) Glob using filename patterns that match all three naming variants at once, across every directory in the repository.

**Question 23.** Glob found four candidate configuration files. You now need the complete surrounding structure of one 120-line file before deciding where a setting is inherited. What should you use?

- A) Grep for a single key inside the file and ignore everything else around it.
- B) Read the selected file in full to see how the setting sits within its surrounding structure.
- C) Write a brand-new replacement configuration before understanding the original.
- D) Bash-delete the other three candidate files to simplify the decision.

**Question 24.** A production log contains the exact message `permission cache exhausted`, and you need to locate where that text is emitted. Which tool is most direct?

- A) Glob for files whose names merely contain the word "cache."
- B) Read through the entire repository sequentially until the string turns up.
- C) Grep for the exact message text across the codebase.
- D) Edit likely logging files one at a time until the message changes.

**Question 25.** You must trace how a CLI command reaches a database adapter in an unfamiliar repository. Which sequence best manages context?

- A) Read every Python file first, then search only once context is nearly full, and infer the route from whichever file was read last.
- B) Locate command registration with Grep or Glob, Read the matches, and follow only the relevant imports and calls.
- C) Infer the route from directory names alone and skip reading file contents entirely.
- D) Ask a generic coding question about database adapters without citing any repository evidence.

**Question 26.** Claude confuses `search_source_code` with `search_runbooks`. Both descriptions currently say “search company content.” What is the best first correction?

- A) Force `search_source_code` to run for every query that merely contains the word "error."
- B) Put both operations behind one third, even more generic tool simply named `search`.
- C) Give the agent several more overlapping tools and let it call all of them before deciding, after the fact, which result actually answered the question.
- D) Rewrite each description with distinct use cases, inputs, outputs, examples, boundaries, and when to prefer the other tool.

**Question 27.** `analyze_content` handles web snippets while `analyze_document` handles uploaded files, but their names and descriptions overlap. What redesign most directly improves selection?

- A) Rename the first tool to a web-specific operation and make both contracts explicitly source-specific.
- B) Keep the overlap, add "choose carefully" to the system prompt, and have Claude explain its choice only after the tool already ran.
- C) Randomize which of the two tools runs and compare the outputs afterward.
- D) Force both tools to run on every single item regardless of its source.

**Question 28.** Detailed tool descriptions look correct, yet a system prompt says “for any investigation, always begin with the archive tool.” Claude keeps ignoring a better live-search tool. What should you inspect?

- A) Whether the archive tool's JSON schema lists its properties alphabetically and which server happened to connect first.
- B) Keyword-sensitive prompt instructions that override or bias the model's normal tool selection.
- C) Whether the two tools happen to live on different MCP servers entirely.
- D) Whether the response token limit is set high enough for the archive tool's output.

**Question 29.** A source-control MCP tool times out. The agent must know whether to retry and what operation failed. What should the tool return?

- A) A successful empty list, so the workflow just continues as if nothing happened.
- B) The text "something went wrong" with no error flag or validation marker, plus a `CLAUDE.md` note asking Claude to guess whether the string is data or failure.
- C) `isError` plus a transient category, retryability, the attempted operation, a safe description, and a suggested next action.
- D) Only the provider's raw, unfiltered stack trace.

**Question 30.** A code search completes successfully and finds no references. How should the tool represent this outcome?

- A) As a retryable transient error, purely because the result set happens to be empty.
- B) As a permission error, so the coordinator spends time investigating access.
- C) As a business-rule failure that requires human escalation before anything continues.
- D) As a successful empty result, clearly distinct from any tool failure, error, or timeout that the coordinator would otherwise need to retry.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

Your research coordinator handles requests ranging from routine comparisons to open-ended investigations. It must choose decomposition strategies based on the work rather than blindly running a fixed pipeline.

**Question 31.** A compliance review always checks the same four known controls, while an incident investigation must branch based on each new log or dependency discovered. Which design is appropriate?

- A) Dynamic decomposition for both, since every agent workflow should branch on new evidence.
- B) One large prompt for both, in order to avoid any coordination overhead between steps.
- C) A fixed chain for both, so the step count stays predictable and auditability outranks evidence discovered mid-investigation.
- D) A fixed chain for the repeatable control review, and dynamic decomposition for the investigation.

**Question 32.** The request is “add comprehensive tests to this unknown legacy service.” What should the coordinator do first?

- A) Generate one test file for every source file immediately, before looking at any of them.
- B) Map the service, identify high-impact behavior and dependencies, then create subtasks that adapt to what the map reveals.
- C) Apply the same fixed list of unit-test prompts used on every repository, and rerun it unchanged even after a test exposes a new dependency.
- D) Delegate the whole task to a single test-writer and prohibit any further exploration.

**Question 33.** A simple factual query needs one authoritative source, but the coordinator always invokes search, document analysis, statistics, synthesis, and report agents. What is the best change?

- A) Keep the full pipeline running but shorten every agent's response so latency and cost stay predictable regardless of the query.
- B) Cache every specialist's most recent answer for reuse on the next request.
- C) Let the coordinator select only the specialists justified by the query and intermediate findings.
- D) Replace every specialist with one unrestricted general-purpose agent.

**Question 34.** A broad market study omits regional regulation because the coordinator decomposed it only by product feature. How should decomposition be improved?

- A) Partition the full scope across complementary dimensions or source types, then verify coverage before synthesis.
- B) Ask the synthesis agent to invent a regulatory section from general knowledge and label it an informed estimate.
- C) Make every existing subtask longer in length without changing what it actually covers.
- D) Remove the coverage requirement entirely so it matches whatever research was actually gathered.

**Question 35.** An open-ended performance investigation has not yet established which component is slow. What is the strongest initial subtask?

- A) Rewrite the database layer immediately, since it is commonly the slow component, even before any measurement confirms it.
- B) Ask every specialist to optimize whichever component it happens to favor.
- C) Measure and map the request path first, then generate prioritized subtasks from the observed bottlenecks.
- D) Execute a fixed sequence of generic optimizations regardless of where the actual bottleneck lies.

**Question 36.** Forty files need the same predictable local checklist, followed by one cross-file compatibility review. Which decomposition best preserves depth?

- A) Run focused per-file passes and then a separate integration pass across all forty files.
- B) Use an open-ended dynamic investigation for every single file even though every stage is already known in advance.
- C) Put all forty files into one prompt and ask Claude to divide its attention evenly across them.
- D) Skip the integration pass entirely, since every individual file already passed its local checklist.

**Question 37.** A dependency audit discovers midway that two services share a generated client, invalidating several planned subtasks. What should the coordinator do?

- A) Finish the original task list before acknowledging the dependency, so the plan stays comparable with prior audit runs.
- B) Revise the plan and generate replacement subtasks that account for the shared client.
- C) Restart the entire investigation from zero without preserving any valid findings already produced.
- D) Hide the discovery from the specialists so their assignments remain stable.

**Question 38.** Which coordinator behavior most clearly distinguishes adaptive decomposition from a fixed workflow?

- A) It uses the same specialists in a different order each run while keeping the predefined task list and completion conditions fixed.
- B) It runs every predefined step in parallel instead of one after another.
- C) It asks specialists for longer reports whenever the evidence gathered so far is thin.
- D) It creates or revises subtasks in response to intermediate discoveries and remaining coverage gaps.

**Question 39.** Initial synthesis is strong but lacks evidence for one geography. What should an iterative coordinator do?

- A) Identify the gap, delegate a targeted follow-up search, then resynthesize with the new evidence.
- B) Add a generic disclaimer to the report and stop despite the gap being recoverable.
- C) Restart every completed subtask from scratch rather than only the affected section.
- D) Ask the synthesis agent to fill the section without sources, citing material that never covered that geography.

**Question 40.** A specialist repeatedly maps “active users” to total registered accounts. Which feedback is most useful?

- A) Tell the specialist to simply think harder about what a metric means.
- B) Raise the specialist's maximum output length so its reports run longer.
- C) Replace the agent without describing the observed failure, and ask the replacement to guess the intended definition from old reports.
- D) Provide representative inputs, the incorrect mappings, the desired mappings, and a precise definition of "active."

**Question 41.** Three findings arise from the same mistaken date-window assumption and will interact if fixed separately. How should the coordinator request refinement?

- A) Send each issue in isolation and withhold the shared assumption so each specialist optimizes its own correction independently.
- B) Batch the related issues in one detailed request that explains their common dependency.
- C) Fix only the single easiest finding and leave the rest of the interacting issues untouched.
- D) Add the errors to permanent user memory instead of addressing them in this session.

**Question 42.** You resume a research session after editing three previously analyzed parsers. Most other context remains valid. What should you tell the agent?

- A) Say nothing, since resumption is assumed to automatically detect every filesystem change on its own.
- B) Re-read the entire repository from scratch, since targeted recovery is assumed to be impossible.
- C) Name the three changed parsers, request targeted re-analysis of just those files, and explicitly retain the unaffected earlier findings.
- D) Trust the old parser outputs, since named resumption is assumed to snapshot the filesystem before the next answer.

**Question 43.** You want two independent research strategies to begin from the same accepted source map without contaminating one another. What mechanism fits?

- A) Resume the same session concurrently in two separate terminals.
- B) Copy only the original user prompt into two brand-new blank sessions.
- C) Run both research strategies sequentially within one single conversation.
- D) Use `fork_session` to branch both strategies independently from the same shared, accepted baseline.

**Question 44.** A research agent has `search_news` and `search_academic`, but the latter is almost never chosen even for peer-reviewed-evidence requests. What should its description add?

- A) A promise that it always outperforms every other available tool, plus a blanket instruction to prefer it whenever the user requests credible or peer-reviewed evidence.
- B) Its indexed sources, accepted query and date inputs, output metadata, example academic requests, and explicit contrast with news search.
- C) Internal implementation details that have nothing to do with when to select it.
- D) A requirement that both search tools run together on every single query.

**Question 45.** A search specialist sees a transient timeout that succeeds on a safe local retry. What error-handling structure best protects coordinator context?

- A) Let the specialist recover locally; propagate only unresolved failure context, attempts, and partial results.
- B) Propagate every first failure immediately, let the coordinator retry it, and preserve a full transcript of every attempt in the main context.
- C) Hide all failures from the coordinator, including permanent ones that will never resolve on their own.
- D) Terminate every subagent the moment any single tool call reports an error, without any recovery hook of its own.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

Your extraction service handles invoices, contracts, résumés, and scanned forms. A strict schema is already available, but accuracy varies across layouts and operational edge cases.

**Question 46.** Invoice extraction works on the layout used in the prompt but fails when totals appear in tables, footnotes, or sidebars. What is the strongest improvement?

- A) Make every field required so Claude searches harder for it.
- B) Retry the identical prompt repeatedly until one run happens to succeed.
- C) Add several worked examples across different layouts, with normalization guidance, while keeping the schema-based tool output.
- D) Replace tool use with free-form prose and require downstream code to parse whichever layout-specific explanation the model returns.

**Question 47.** Dates appear as `03/04/26`, `4 March 2026`, and `2026-03-04`, while downstream systems require ISO 8601. What should accompany the schema?

- A) Explicit normalization instructions, including how to represent genuinely ambiguous dates rather than silently guessing.
- B) Copy every date string unchanged, then have downstream systems infer the locale from the customer's account and the vendor's country instead of normalizing anything centrally.
- C) A higher confidence threshold applied to date fields, with no explicit format rule at all.
- D) A retry policy that simply omits the original date on the next attempt.

**Question 48.** Some contracts legitimately contain no renewal date. The current required string field causes invented dates. What is the best correction?

- A) Keep the field required, add "do not hallucinate" to the prompt, and rely on downstream validation to reject any fabricated date every single run.
- B) Make the field optional or nullable and instruct the model to use null when the source is silent.
- C) Reject every contract that lacks a renewal date outright.
- D) Derive a placeholder date from the contract's signing date instead.

**Question 49.** Résumé extraction works for conventional corporate résumés but misses existing education and publication fields on academic CVs. Which change is most likely to generalize?

- A) Add a rule for the exact CV that failed and a new exception for every additional university template.
- B) Force every missing field to an empty string rather than leaving it absent.
- C) Run the same prompt more times and manually pick whichever output looks the most complete.
- D) Add representative examples showing the same target fields across corporate, academic, and international layouts.

**Question 50.** A scanned form omitted the page containing the requested identifier. Validation fails on every retry. What should the system do?

- A) Recognize that the information is absent, stop retrying, and route the document to rescanning, null handling, or human review.
- B) Retry indefinitely using progressively stronger wording in the prompt.
- C) Ask Claude to infer the identifier from neighboring records and label it model-generated so downstream teams know it was not scanned.
- D) Mark the extraction successful and fill the field with a fabricated placeholder value.

**Question 51.** An extraction is schema-valid but fails a business check because line-item totals do not equal the stated subtotal. What should a corrective follow-up include?

- A) Only the phrase "try again," with no other context attached.
- B) Provide only the failed subtotal and a generic instruction to change whichever value looks least plausible.
- C) The original document, failed extraction, and specific validation discrepancy.
- D) A random alternative subtotal chosen because it happens to pass validation.

**Question 52.** Tool use guarantees that output conforms to the JSON schema, but customer names are occasionally placed in the vendor field. What does this demonstrate?

- A) Strict schemas eliminate both syntax errors and semantic extraction mistakes.
- B) Semantic validation and representative examples are still needed after structural compliance.
- C) The schema should be removed entirely, since it apparently caused the field swap.
- D) A larger output token limit will correct the field's meaning.

**Question 53.** Payment methods are represented by a fixed enum, but valid new methods appear regularly. How should the schema avoid forced misclassification?

- A) Include an `other` value with a detail field, and an `unclear` representation when the source is genuinely ambiguous.
- B) Map every unfamiliar method to the closest existing category and update a hard-coded list every quarter, folding new methods into old normalization rules.
- C) Reject every document containing a payment method the schema does not already list.
- D) Replace the entire schema-based response format with free-form prose instead.

**Question 54.** A document has clear header fields but an illegible handwritten approval box. Routing is currently based on one document-level confidence average. What is better?

- A) Randomly review ten percent of documents regardless of actual field quality.
- B) Review every document and require the reviewer to re-enter every header field as well as interpret the approval box.
- C) Accept every document whose average confidence score exceeds 0.9.
- D) Route based on field-level confidence, field risk, and the handwritten ambiguity while allowing clear fields to proceed.

**Question 55.** The team proposes auto-accepting fields above confidence 0.92 because the number “sounds safe.” How should the threshold be selected?

- A) Use 0.99 for every field without ever testing it against real outcomes.
- B) Average whatever confidence values the model produced last week.
- C) Calibrate scores against labeled outcomes by field and segment, then set thresholds that meet the accuracy target.
- D) Let each individual model response choose and report its own threshold without any calibration, and have downstream systems store and trust that self-reported number.

**Question 56.** High-confidence extractions now bypass normal human review. How can the team detect new error patterns that the confidence model does not recognize?

- A) Review only the outputs that already came back with low confidence.
- B) Continuously review a stratified random sample of auto-accepted outputs.
- C) Trust the original benchmark indefinitely without ever re-checking it.
- D) Retry a random sample without human labels and treat agreement between the two runs as proof the original was correct.

**Question 57.** Which review policy best uses document characteristics and ambiguity?

- A) Route every hundredth document to whichever reviewer is next in a random queue.
- B) Review every field in low-confidence documents with one generalist, even when only a single field is actually ambiguous.
- C) Assign reviewers strictly by arrival order to keep the routing logic simple.
- D) Route uncertain or high-risk fields to reviewers with relevant expertise, using confidence and source characteristics as signals.

**Question 58.** The model confuses `extract_invoice` and `extract_purchase_order` when both documents contain totals and vendor names. What is the best tool-interface improvement?

- A) Give each tool explicit document cues, unique outputs, boundary examples, and guidance for distinguishing the two formats.
- B) Force invoice extraction to run for every financial document regardless of its actual type.
- C) Rename both tools to shorter, more generic names than they already have.
- D) Ask downstream code to infer the document type after the fact from whichever fields happen to be populated most often during extraction and apply ad hoc normalization there, rather than fixing the tool contracts themselves.

**Question 59.** A refund extraction requests an amount prohibited by policy. Retrying cannot change the policy result. What should the tool surface?

- A) A transient retryable error with unlimited attempts, skipping validation of whether the failure is actually temporary, and treating temporary glitches and permanent policy outcomes as one recovery path.
- B) A successful empty response with no indication that anything was declined.
- C) A non-retryable business error with a customer-safe explanation, a reason code, and the permitted next action.
- D) Only an internal policy stack trace exposed straight to the caller.

**Question 60.** An extraction tool cannot open a restricted document collection. Which response gives the agent the clearest recovery path?

- A) A generic "operation failed" message with no further detail.
- B) A permission error, typed as non-retryable until access changes, with a suggestion to request access or escalate.
- C) A valid, empty extraction object returned as if the call succeeded.
- D) A transient category that keeps retrying, coordinated through a retry hook, until the same restricted collection has failed a fixed number of times before escalation.

---

# Answer Key — Practice Exam 13

**Quick key:** 1-C, 2-A, 3-D, 4-B, 5-B, 6-D, 7-A, 8-C, 9-D, 10-A, 11-C, 12-B, 13-A, 14-D, 15-C, 16-B, 17-D, 18-A, 19-C, 20-A, 21-C, 22-D, 23-B, 24-C, 25-B, 26-D, 27-A, 28-B, 29-C, 30-D, 31-D, 32-B, 33-C, 34-A, 35-C, 36-A, 37-B, 38-D, 39-A, 40-D, 41-B, 42-C, 43-D, 44-B, 45-A, 46-C, 47-A, 48-B, 49-D, 50-A, 51-C, 52-B, 53-A, 54-D, 55-C, 56-B, 57-D, 58-A, 59-C, 60-B

**Focus key:** 1-CFG, 2-CFG, 3-CFG, 4-CFG, 5-CFG, 6-CFG, 7-CFG, 8-CFG, 9-REF, 10-REF, 11-REF, 12-EXP, 13-EXP, 14-RES, 15-RES, 16-MCP, 17-MCP, 18-MCP, 19-MCP, 20-MCP, 21-MCP, 22-EXP, 23-EXP, 24-EXP, 25-EXP, 26-DESC, 27-DESC, 28-DESC, 29-ERR, 30-ERR, 31-DEC, 32-DEC, 33-DEC, 34-DEC, 35-DEC, 36-DEC, 37-DEC, 38-DEC, 39-REF, 40-REF, 41-REF, 42-RES, 43-RES, 44-DESC, 45-ERR, 46-EXT, 47-EXT, 48-EXT, 49-EXT, 50-EXT, 51-EXT, 52-EXT, 53-EXT, 54-REV, 55-REV, 56-REV, 57-REV, 58-DESC, 59-ERR, 60-ERR

Focus codes: CFG = Claude Code configuration selection; MCP = MCP scope and integration; DEC = adaptive decomposition; EXT = extraction accuracy; REF = iterative refinement; EXP = codebase exploration; DESC = tool descriptions; RES = session resumption; REV = human-review routing; ERR = MCP error handling.

---

**1. C** — Shared, durable, repository-wide guidance belongs in the committed project `CLAUDE.md`, where it is versioned and reviewed like code. Personal memory loads regardless of which project is open, an on-demand skill can be skipped, and a re-pasted prompt drifts and gets forgotten.

**2. A** — A path-scoped rule with a glob follows matching files across unrelated directories and loads only for them. A single-package memory file misses scattered locations, a root-level note relies on inference instead of automatic scoping, and a manual command is easy to forget even without a competing hook.

**3. D** — An occasional, verbose workflow fits a skill, and `context: fork` isolates its exploration so it never bloats the main conversation. Always-loaded memory wastes context every session, a per-contributor command fragments and drifts, and a rule tied to manifest reads fires far more often than the intended quarterly cadence.

**4. B** — Enforcement that depends on live tool arguments must be deterministic and run before the tool executes, which is what a `PreToolUse` hook provides. Warnings and printed policy text remain advisory, and a path-scoped rule cannot inspect the arguments a running tool receives.

**5. B** — User-scoped commands are personal and are not distributed through the repository. A project command would affect teammates, while `CLAUDE.md` and MCP configuration are different mechanisms entirely.

**6. D** — An `@` reference supplies a known relevant file to the current task without permanently consuming future context. The other choices make one-time context durable or introduce unrelated infrastructure that fires on unrelated edits.

**7. A** — A directory-level `CLAUDE.md` is the natural automatic scope for one cohesive subtree. Skills require manual invocation, and commands or MCP resources do not provide inherited directory guidance.

**8. C** — `PostToolUse` runs after the edit and can invoke the formatter and return failures to Claude every time. A prose instruction is probabilistic, attaching the hook to Read fires at the wrong event, and an `@` reference does not execute checks.

**9. D** — A concrete failing input, observed output, expected output, and regression test give Claude an exact correction target and preserve the fix. Asking for more effort without evidence, a from-scratch rewrite compared only by eye, and permanent memory notes do not pin down the transformation.

**10. A** — The interview pattern surfaces missing product and failure-mode decisions before code hardens accidental assumptions. Implementing first and letting incidents define policy, or multiplying implementations before criteria exist, cannot resolve requirements that have not been decided.

**11. C** — Interacting issues should be presented together with their shared constraints, while an independent issue can be handled separately. Universal "always batch" or "always sequence" rules ignore dependency structure.

**12. B** — Grep searches file contents for symbol references regardless of filename. Glob searches paths, while Write and Edit mutate files rather than discover usages.

**13. A** — Targeted search followed by selective Read and import tracing builds understanding incrementally without filling context. Reading everything wastes the window, and filenames or test output alone do not establish the real call path.

**14. D** — Named resumption is appropriate when prior context and tool results remain valid and the goal is unchanged. Forking is for divergence, and starting over or copying a single response discards reliable work.

**15. C** — Major file changes make old tool results stale, so a fresh session seeded with durable conclusions and targeted re-reading is safer than resuming or forking stale evidence. Discarding the durable architectural conclusions along with the stale evidence is unnecessary.

**16. B** — Project `.mcp.json` distributes shared tooling, while environment expansion supplies per-user credentials without committing secrets. User scope is not shared, and an unrelated skill does not configure the server at all.

**17. D** — Personal or experimental servers belong in user-scoped `~/.claude.json`. Committing an unstable server exposes it to the team even if a comment or a narrow path rule tries to limit its visibility.

**18. A** — Tools from every connected MCP server are discovered together and made available to the agent; clear contracts and context guide selection. There is no required one-active-server toggle, and MCP resources do not gate which server runs.

**19. C** — Environment-variable expansion keeps the secret outside version control while leaving the server definition shareable. Encoding, comments, and slash commands do not secure a committed credential.

**20. A** — Existing maintained servers are preferred for standard integrations; custom work is warranted for team-specific contracts or behavior not otherwise available. Sharing across developers or using an environment variable does not by itself require a custom server.

**21. C** — MCP resources expose catalogs and schema structures without repeated exploratory tool calls. A hook only reacts after a call already happened, and copying live catalogs into memory creates stale, bloated context.

**22. D** — Glob is designed for matching file paths and naming variants. Grep searches contents, reading every root is slower, and Edit is for changing files, not discovering them.

**23. B** — Once candidates are narrowed, Read supplies the selected file's full local context. A single Grep match can hide inheritance structure, and writing or deleting files is premature before the original is understood.

**24. C** — An exact log string is a content-search problem, so Grep is direct. A filename guess and an exhaustive sequential read are both weaker, and Edit should follow diagnosis, not replace it.

**25. B** — Incremental discovery narrows candidates before reading and follows only evidence-bearing relationships. Reading everything exhausts context, while inferring the route from names or asking without repository evidence is unreliable.

**26. D** — Tool descriptions are the model's primary selection signal and should differentiate purpose, formats, outputs, examples, edges, and neighboring tools. Forced keyword routing, generic consolidation, and giving the agent even more overlapping tools all preserve the ambiguity.

**27. A** — Source-specific names and contracts move the distinction into the interface the model selects from. A system-prompt warning that is checked only after the tool already ran, randomness, and always calling both tools do not remove the overlapping semantics.

**28. B** — System-prompt wording can create keyword associations that override good descriptions. Schema property ordering, which server a tool lives on, and response length do not explain the mandated archive preference.

**29. C** — A structured error type, retryability, the attempted action, and next steps let the agent choose a recovery path. Empty success hides failure, text with no error flag or validation marker is not actionable, and a raw trace is unsafe and incomplete.

**30. D** — No matches is a valid successful query result and must remain distinct from access or operational failures. Mislabeling it prompts wasteful retries or unnecessary escalation.

**31. D** — Known repeatable stages suit a fixed chain, while evidence-driven incident work needs adaptive decomposition. One decomposition style is not optimal for both predictable and open-ended work, and a single unstructured prompt loses the benefit of either approach.

**32. B** — An unknown legacy system must first be mapped so high-impact behavior and dependencies can drive the testing plan. Immediate file-by-file generation, or a fixed prompt list that never updates even after new dependencies surface, is a guess that can miss integration risk.

**33. C** — The coordinator should scale delegation to query complexity and what is discovered along the way. Shortening every agent's output or caching stale answers does not remove an unnecessary full pipeline.

**34. A** — Broad work needs complementary scope partitioning and a coverage check so no major dimension vanishes. Longer subtasks cannot recover an unassigned region, and synthesis must not fabricate one from general knowledge.

**35. C** — Measurement and mapping identify actual bottlenecks, after which subtasks can adapt to evidence. Rewriting a commonly-slow component pre-emptively, or running generic optimizations, starts from unsupported assumptions.

**36. A** — Predictable local checks benefit from focused per-file passes, and a separate integration pass catches cross-file behavior. One shared mega-prompt dilutes attention, and treating open-ended investigation as necessary for known stages, or skipping integration, both waste the structure that already exists.

**37. B** — Adaptive plans change when a newly discovered dependency invalidates prior assumptions, preserving still-valid findings while replacing affected work. Finishing the stale plan for comparability, restarting from zero, and hiding the discovery are all wasteful or dishonest.

**38. D** — Creating and revising subtasks from intermediate findings is the defining adaptive behavior. Reordering, parallelizing, or lengthening a still-fixed task list does not change what work actually gets generated.

**39. A** — Iterative orchestration evaluates synthesis, identifies a specific gap, commissions targeted evidence, and resynthesizes. Disclaiming the gap, restarting unaffected subtasks, or inventing uncited content all skip a recoverable refinement step.

**40. D** — Examples of the failure and desired mapping plus an exact definition teach the disputed boundary. Generic effort, a longer output limit, or a silent agent swap supplies no corrective evidence.

**41. B** — Related failures caused by one shared assumption should be evaluated together so the fix is coherent. Isolating them hides the interaction, fixing only one leaves the rest broken, and permanent memory is not an issue tracker.

**42. C** — A resumed agent must be told what changed so it can refresh affected evidence without repeating valid exploration. Session history does not automatically know about filesystem changes, and assuming otherwise in either direction wastes work or trusts stale output.

**43. D** — `fork_session` preserves the accepted baseline while isolating divergent reasoning. Concurrent resume in two terminals shares the same branch, a blank session loses the baseline, and sequential work in one conversation contaminates the comparison.

**44. B** — Selection improves when the academic tool says what it indexes, how to query it, what it returns, and when it wins over news search. Boasts and a blanket preference instruction, irrelevant implementation trivia, and mandatory dual calls are not useful boundaries.

**45. A** — Specialists should recover locally from safe transient failures and spare coordinator context; unresolved errors should include attempts and usable partial results. Immediate propagation of every first failure, and total suppression of even permanent errors, are both brittle.

**46. C** — Diverse positive examples teach field-location patterns across layouts, while normalization guidance and schema-based output preserve consistency. Repeating an identical prompt and making every field required do not teach layout variation.

**47. A** — The prompt must state the canonical format and define what to do when source notation is ambiguous. Leaving locale inference to downstream systems, a confidence threshold with no format rule, and a retry that drops the original date all fail to normalize centrally.

**48. B** — Optional or nullable fields faithfully represent genuine absence and remove pressure to fabricate. Rejection or deriving a placeholder date invents a business rule the source does not support.

**49. D** — Representative layout diversity teaches transferable extraction behavior across document families. A one-off rule overfits, forced empty strings hide the gap rather than close it, and re-running the same prompt and picking by eye does not fix the underlying pattern.

**50. A** — Retries cannot recover content missing from the source, so the system must stop and choose an operational path such as rescanning, null, or review. Guessing from neighboring records and indefinite retries both manufacture confidence without evidence.

**51. C** — Corrective retries need the evidence, failed candidate, and exact validation error so the model can repair the semantic defect. A vague instruction or a value chosen only because it happens to validate cannot ground the correction.

**52. B** — A schema guarantees shape, not that evidence was mapped to the correct field. Semantic validation and representative examples still define meaning and catch swaps; removing the schema or raising the token limit addresses neither problem.

**53. A** — `other` plus detail preserves novel valid values, while `unclear` represents ambiguity without guessing. Nearest-category mapping into a hand-maintained list, outright rejection, and dropping the schema for prose all lose source truth.

**54. D** — Field-level routing isolates the ambiguous, risky approval box while preserving clear header extraction. A document average can hide critical field uncertainty, and blanket or random review wastes effort re-checking fields that were already clear.

**55. C** — Confidence scores become actionable only after calibration against labeled outcomes at the relevant field and segment. An intuitive fixed number, a rolling average, and a self-reported per-response threshold all have no demonstrated relationship to accuracy.

**56. B** — Stratified sampling of auto-accepted output detects blind spots and distribution drift that confidence alone misses. Reviewing only known low-confidence failures, trusting an old benchmark, or comparing unlabeled reruns cannot reveal unknown high-confidence errors.

**57. D** — Effective routing combines ambiguity, field risk, source characteristics, and reviewer expertise. Random, arrival-order, or aggregate-only routing ignores where the uncertainty actually resides.

**58. A** — Similar document tools need explicit discriminators, examples, and distinct output contracts. Forcing one tool as the default, shortening both names, and having downstream code guess the type after the fact all leave the selection ambiguity intact.

**59. C** — A policy violation is a non-retryable business outcome and should include a safe explanation, a reason code, and an allowed alternative. Treating it as transient wastes calls, empty success conceals the reason, and a raw stack trace is unsafe.

**60. B** — A permission error typed as non-retryable tells the agent that retries will not help until access changes and gives a concrete escalation path. A generic message, a silent empty success, and a retry loop dressed up with a "retry hook" all drive the wrong behavior.

*End of Practice Exam 13.*
