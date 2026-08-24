# CCAFC Practice Exam 14

**Claude Certified Architect – Foundations — Targeted Retake Exam: Integrated Judgment**

This remediation exam is the harder follow-up to Practice Exam 13. It revisits every objective that scored below 100% on the August 2, 2026 score report, but places the decisions inside denser scenarios where several answer choices are individually reasonable and only one best fits the stated constraint.

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — one correct answer and three plausible distractors per item |
| Scenarios | 4 (Customer Support Resolution Agent, Claude Code for CI/CD, Multi-Agent Research System, Structured Data Extraction) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**; for retake readiness on these weak areas, target at least 48 / 60. |

Focus distribution: Claude Code configuration selection ×6, MCP scope/integration ×6, adaptive decomposition ×8, extraction accuracy ×11, iterative refinement ×6, codebase exploration ×3, tool-description design ×5, session resumption ×4, human-review routing ×6, and MCP error handling ×5.

Answer key with explanations is at the end.

---

## Scenario A: Customer Support Resolution Agent (Questions 1–15)

Your support agent handles billing, fulfillment, account access, and policy questions through MCP tools. It must adapt to ambiguous cases while keeping deterministic controls and clear human-review paths.

**Question 1.** A customer says, “My replacement never arrived, and now the original card was charged again.” Identity is already verified, and the shipment and charge investigations are independent until the final response. What should the coordinator do?

- A) Classify the case by whichever concern the customer mentions first, run that fixed workflow to completion, and defer the other concern until it closes.
- B) Create separate shipment and billing subtasks, run them concurrently, then synthesize one coordinated case resolution for the customer.
- C) Escalate the entire case immediately, since any request naming more than one concern is treated as exceeding autonomous scope.
- D) Let the shipping and billing specialists each reply to the customer directly, without coordinator synthesis.

**Question 2.** Address changes always require verify identity → validate new address → update account. Account-takeover reports branch according to device, login, and payment evidence discovered during investigation. Which decomposition is best?

- A) Apply dynamic decomposition to both, reasoning that any process can eventually surface evidence worth investigating.
- B) Merge both procedures into one unrestricted prompt and let the model decide, turn by turn, what step to run next without any structure.
- C) Standardize on one fixed pipeline for both, since a single audited sequence is supposedly easier to review than two separate decomposition styles.
- D) Use a fixed verify-validate-update chain for address changes, and adaptive decomposition that branches on device, login, and payment evidence for takeover cases.

**Question 3.** A fraud investigation discovers that the disputed transaction belongs to a second customer profile sharing the same email domain. What should happen to the existing investigation plan?

- A) Add a targeted identity-linkage subtask, revise the dependent findings it touches, and leave unaffected work in place.
- B) Finish every subtask from the original plan first, then reopen the case for the new profile only once all of them close.
- C) Restart the investigation from an empty context, discarding evidence already verified, so the new profile gets a fresh review.
- D) Ignore the second profile since it fell outside the initial plan, and preserve the original timeline and subtask list for audit consistency.

**Question 4.** The agent must investigate “why refund completion times rose this month,” but the cause could be policy, provider latency, regional routing, or case mix. What is the strongest first step?

- A) Ask the payment specialist to start optimizing provider retry logic immediately, on the assumption that provider latency is the likely cause.
- B) Run the same fixed refund checklist used for individual customer cases, applying it wholesale at the aggregate level to the entire month's completions and averages.
- C) Map the refund process and pull the relevant metrics, then generate subtasks from whatever contributors the data shows.
- D) Assign one specialist to draft a final explanation before any evidence is gathered, then have the other specialists gather support for that conclusion.

**Question 5.** `lookup_order` receives an identifier with an invalid checksum. Retrying unchanged cannot succeed, but the customer can correct the value. What error should the tool return?

- A) A transient error with exponential backoff that keeps resending the identical, still-invalid identifier in the hope that a later retry happens to succeed.
- B) A successful empty result, so the coordinator treats the bad checksum the same as a customer with no matching order.
- C) A structured-looking permission error requiring supervisor access, even though the checksum problem has nothing to do with authorization.
- D) A structured validation error marked non-retryable until the input changes, including the specific checksum problem and the required identifier format.

**Question 6.** The shipping provider times out once, and the lookup is safe to repeat. Where should the first recovery attempt occur?

- A) In a human escalation queue, holding the case for a reviewer before any retry is attempted.
- B) Locally in the shipping specialist, propagating only the unresolved failure context to the coordinator if the retry does not recover.
- C) In the final customer-facing response, asking the customer to try again later while withholding any detail about which internal provider timed out or why.
- D) In every other specialist in turn, on the chance that a different one happens to reach the same provider.

**Question 7.** A refund specialist successfully verifies identity and policy eligibility but cannot reach the payment provider after safe retries. What should it return to the coordinator?

- A) Only the words "refund failed," with no indication of which steps already succeeded.
- B) A false success response, so the case can move forward as though the refund had actually completed.
- C) The verified partial results, the actions already attempted, a typed transient-failure category, retry status, and the next steps still available.
- D) The entire raw provider log verbatim, including request headers, internal customer identifiers, and every retry attempt, with no summary of what work is actually recoverable.

**Question 8.** The agent swaps `get_customer_profile` and `get_customer_authorizations` because both descriptions say “gets customer information.” What should be changed first?

- A) Rewrite each description with a distinct use case, its own identifiers and output fields, a worked example, and an explicit note about when to reach for the other tool instead.
- B) Force both `get_customer_profile` and `get_customer_authorizations` to run on every customer request, regardless of which one the task actually needs.
- C) Add several more customer-related tools to the server, on the theory that more choices will help Claude pick the right one.
- D) Route the call using a hard-coded list of trigger words like "customer," "profile," and "authorization," reviewing and expanding that list a little more by hand after each new misroute occurs.

**Question 9.** A generic `modify_account(action, value)` tool can change contact details, disable MFA, or close the account. The wrong mode has caused destructive calls. What redesign most directly improves reliability?

- A) Keep the single generic `modify_account` tool, but normalize and lengthen the action enum so every operation, including destructive ones, still shares the same call shape and permission level.
- B) Split the sensitive operations into purpose-specific tools, such as `update_contact_info`, `disable_mfa`, and `close_account`, each with its own contract and permission scope.
- C) Add a "be careful with destructive actions" reminder to the coordinator's system prompt, leaving the tool interface unchanged.
- D) Require the generic tool to run twice per call and compare its own two sets of arguments before executing either one.

**Question 10.** Most fields on a refund claim are clear, but the claimed amount is handwritten, low-confidence, and financially consequential. What review routing is best?

- A) Accept the whole claim, since its average field confidence is high, and treat that document-level average as proof that no individual field needs a closer look.
- B) Send one randomly chosen field, unrelated to the disputed amount, for human review, purely to preserve a representative review sample across claims.
- C) Route the claimed-amount field to a reviewer qualified to judge it, while unambiguous low-risk fields continue through the pipeline.
- D) Reject the entire claim automatically the moment any handwriting appears anywhere on the document, regardless of which field it touches or how confidently it was read.

**Question 11.** Warranty photos require visual-damage expertise, while ambiguous policy exceptions require a policy specialist. How should reviewer assignment work?

- A) Route each case by the uncertain field's own characteristics and the expertise it actually requires, such as visual-damage judgment or policy interpretation, rather than by whichever reviewer happens to be free.
- B) Send both warranty photos and policy exceptions to whichever reviewer is randomly selected next, regardless of visual or policy background.
- C) Route every case using only the whole-document confidence score, ignoring which specific field or expertise is actually in question.
- D) Let the model pick a reviewer type from its own unvalidated self-confidence score, and accept whichever specialty it predicts without checking that score against outcomes.

**Question 12.** The model emits confidence 0.94 for extracted order numbers. Before using that value to skip human review, what is required?

- A) A prompt telling the model that 0.94 means "very certain," so it reports its own confidence more assertively next time.
- B) A higher acceptance threshold chosen by intuition, raised until the false-approval rate simply feels low enough to the team reviewing it.
- C) Agreement between two copies of the same response generated in the same context, taken as a stand-in for accuracy.
- D) Calibration against labeled outcomes for that specific field and the relevant document types.

**Question 13.** The support MCP server is required for every teammate, but its OAuth client secret differs by environment. Which setup is correct?

- A) Configure the server only in one operator's personal `~/.claude.json`, share screenshots of the working setup, and have every teammate manually reproduce the same configuration on their own workstation.
- B) Commit the OAuth client secret directly alongside the server command in the shared configuration file.
- C) Commit the server definition in the project's `.mcp.json`, and expand the OAuth secret from an environment variable at connection time.
- D) Describe the server's purpose and configuration in `CLAUDE.md`, without actually configuring an MCP server entry anywhere.

**Question 14.** You resume a week-old customer case. The agreed refund amount and customer authorization remain valid, but order status and payment-provider state may have changed. How should state be restored?

- A) Trust every prior tool result unchanged, on the assumption that naming the session guarantees the backend state it captured is still current.
- B) Preserve the durable case facts, such as the agreed refund amount and customer authorization, explicitly refresh the volatile order and provider state, and tell the resumed agent what changed since last week.
- C) Discard the existing customer authorization and make the customer repeat full identity verification, even though nothing about their identity has changed.
- D) Fork the session into a new branch, and assume that forking by itself refreshes provider state while still preserving every prior operational result untouched.

**Question 15.** A prior session mapped the support architecture, but the tool contracts and routing rules were substantially redesigned before work resumed. What is safest?

- A) Resume the old session and prohibit every tool call, on the theory that refusing to act keeps the stale schemas from ever causing a failure.
- B) Fork the old session into two structured-looking branches that still share the exact same stale tool contracts and routing rules, and merge whichever one fails less often in testing.
- C) Reuse the old tool outputs directly, since the underlying architectural intent behind the support system has not changed.
- D) Start a fresh session with a structured summary of the durable goals from before, and re-analyze the newly redesigned tool contracts and routing rules from scratch.

---

## Scenario B: Claude Code for CI/CD (Questions 16–30)

Your organization runs Claude Code in pull-request workflows and maintains shared conventions for a large monorepo. The configuration must load at the right time, and refinement must converge on observable criteria.

**Question 16.** All YAML workflow files scattered across the repository must follow a release-security convention, but ordinary code should not load it. What should you create?

- A) A `.claude/rules/` file scoped with `paths: ["**/.github/workflows/*.yml", "**/.github/workflows/*.yaml"]` so it loads specifically for workflow files and stays out of ordinary code sessions elsewhere in the repository.
- B) A user-level `CLAUDE.md` on the CI maintainer's own workstation, manually replicated by hand into every other workflow repository that needs the convention.
- C) A manually invoked skill covering the convention, which individual developers can simply forget to invoke before editing a workflow file.
- D) A root-level instruction file with no path scoping, so the release-security convention loads into context for every file in every session, whether or not the file is a workflow at all.

**Question 17.** Each package needs centrally maintained testing guidance plus its own language-specific conventions. Copying the shared text has caused drift. Which mechanism composes the relevant files without duplication?

- A) Copy the full text of every centrally maintained standard into every package's own `CLAUDE.md`, keeping each copy updated by hand.
- B) Turn the shared testing standards into MCP tools that every package must call before each of its test runs, instead of reading them as instructions.
- C) Use `@import` from each package's `CLAUDE.md` to pull in the shared testing guidance alongside that package's own language-specific conventions, without duplicating text.
- D) Store the shared standards only in one maintainer's personal memory, and paste them into each CI job's system prompt by hand for every run.

**Question 18.** A `/release-audit` workflow is shared by the team, runs only on demand, produces verbose exploration, and must not write files. How should it be configured?

- A) As always-loaded root memory, with a prose warning telling Claude not to write files during the audit.
- B) As a personal command that any one team member keeps on their own machine, granted unrestricted tool access including Write and Edit, since the audit is only exploratory in intent.
- C) As a path rule that fires for every source file in the repository, whether or not a release audit was actually requested.
- D) As a project skill using `context: fork` to isolate its verbose exploration, with read-only `allowed-tools` structurally preventing any file writes.

**Question 19.** CI must never read `.env.production`, whether through Read, Grep, or Bash. The forbidden paths are stable and do not require business-state evaluation. What is the strongest primary control?

- A) A sentence in `CLAUDE.md` asking Claude, in prose, not to inspect `.env.production` through Read, Grep, Bash, or any other available tool.
- B) Settings permission-deny rules that explicitly cover Read, Grep, and Bash against `.env.production` and any path matching it, enforced before a tool call can run.
- C) A PostToolUse hook that only reports the leak after the file has already been read, grepped, or catted by an earlier tool call.
- D) An inline reminder pasted into each pull request description, asking every reviewer to watch for secret access during review.

**Question 20.** A release command is allowed only when the version matches the signed manifest currently produced by the build. Which mechanism should make the decision at execution time?

- A) A path-scoped formatting rule that reformats the release command's arguments before it runs, without checking them against anything.
- B) A project slash command that runs the release with no validation step, trusting whatever version argument is passed to it.
- C) A `PreToolUse` hook that reads the command's version argument, compares it against the signed manifest the current build just produced, and blocks execution on any mismatch.
- D) A permanent reference to last week's signed manifest hard-coded directly in `CLAUDE.md`, which the release team is responsible for remembering to update by hand before every single build.

**Question 21.** Review standards, fixture conventions, and required test commands apply to every CI invocation of Claude Code. Where should that recurring context live?

- A) In committed project `CLAUDE.md` guidance, loaded automatically and available to every CI invocation of Claude Code.
- B) In a one-time inline prompt, retyped and maintained separately inside each individual workflow run that needs it.
- C) In a developer's personal user-level command directory, which lives only on that individual's own workstation and never reaches the CI runner at all.
- D) In the review tool's own generated JSON output, produced after the review that the standards were supposed to shape.

**Question 22.** A generated migration maps blank strings incorrectly. Which prompt addition communicates the desired transformation most effectively?

- A) A single few-shot example, paired with the instruction to "handle blanks correctly in all circumstances," without showing the null or ordinary cases.
- B) Two or three concrete input/output examples that each show how a blank, a null, and an ordinary nonblank value should transform, side by side.
- C) A higher output token limit, on the assumption that the migration is simply running out of room to handle blanks correctly.
- D) A request to use a more sophisticated design pattern, and to normalize blank-value semantics by inferring them from the surrounding code style instead of stating them directly.

**Question 23.** A parser fix repeatedly repairs one fixture while breaking another. What workflow best drives convergence?

- A) Ask Claude to remember the previous correct behavior without ever writing a single test, and treat the recent conversation history itself as the permanent, authoritative regression archive.
- B) Fix whichever fixture failed most recently, and delete the older fixtures that keep getting broken again in the process.
- C) Increase the temperature between attempts, hoping a different sampling path avoids repeating the same regression.
- D) Establish a regression suite covering both fixtures first, then feed the specific failing test back into each iteration so the fix is checked against both cases at once.

**Question 24.** A new deployment queue requires decisions about retries, idempotency, ordering, and partial failure, but stakeholders have not specified them. What should happen before implementation?

- A) Use the interview pattern to walk through retries, idempotency, ordering, and partial failure with stakeholders and record the resulting decisions.
- B) Start coding whatever default behavior seems reasonable, and write down the retry and idempotency policy afterward once the code already reflects a choice.
- C) Ask Claude to infer every unresolved policy, including retry counts, idempotency keys, ordering guarantees, and partial-failure handling, purely from analogous code found elsewhere in the repository.
- D) Run the code formatter across the new queue module, on the assumption that formatting differences will reveal which requirements are still missing.

**Question 25.** Four review findings all stem from the same incorrect assumption about generated files; two unrelated typos are also present. How should feedback be sequenced?

- A) Put all six findings into six separate sessions so no context is ever shared between them, then manually reconcile whatever conflicting patches come back once every session has finished.
- B) Put all six findings into one single message, on the theory that issue relationships never actually matter to how a fix should be sequenced.
- C) Ignore the two typos entirely until the next release, since they are cosmetic compared to the shared assumption error.
- D) Batch the four findings that share the same incorrect assumption together with that shared context, and handle the two independent typos separately.

**Question 26.** A CI investigation first needs every file matching `**/*contract-test*.ts`, regardless of content. What tool should locate the candidates?

- A) Grep, searching inside file contents for matching text patterns rather than filenames.
- B) Glob, matching file paths against the `**/*contract-test*.ts` pattern to list candidate files by name alone.
- C) Read, opening one located file at a time to view its full contents in detail.
- D) Edit, replacing an exact string inside a file that has already been opened and read.

**Question 27.** After locating the contract tests, you need to find which ones call `seedRemoteAccount` and understand the surrounding setup. What is the efficient next move?

- A) Read every located contract test in full, before running any further search for the `seedRemoteAccount` symbol.
- B) Glob repeatedly, treating the function name `seedRemoteAccount` itself as a filename pattern, and keep adjusting the pattern until it seems to cover every place the helper is called.
- C) Grep the located candidates for the `seedRemoteAccount` symbol, then Read only the files that actually match and the helpers they call.
- D) Replace the `seedRemoteAccount` helper's implementation and observe which of the located tests then fail.

**Question 28.** A review bot flags harmless log statements because its only example shows a real credential leak. How should few-shot prompting reduce these false positives?

- A) Remove the existing example entirely and simply ask the model to report a leak only when it is highly confident.
- B) Add many more copies of the same one real credential-leak example, varying only their wording and ordering so the resulting set of examples merely looks more diverse than it actually is.
- C) Require every log statement in the codebase to be reported as a potential leak, regardless of whether it actually contains a sensitive value.
- D) Add a varied set of both positive examples of real secrets and near-miss negative examples, such as request IDs and other safe-looking identifiers that resemble them.

**Question 29.** Pull-request descriptions use dates, severity labels, and file paths in inconsistent formats, but the review schema expects normalized values. What should be added?

- A) Explicit normalization rules, stated for each field, plus two or three worked examples showing the accepted canonical date, severity, and file-path forms alongside their common inconsistent variants.
- B) More required schema fields describing dates, severities, and paths, added without any accompanying formatting guidance for what a valid value looks like.
- C) A random retry of the whole extraction whenever the produced formatting happens to differ from the last run.
- D) A prose-only output that downstream code has to normalize by guessing at the intended format, with repairs only made after review comments have already been posted.

**Question 30.** The review tool always emits schema-valid objects, but it sometimes labels test-only failures as production blockers. What additional control is needed?

- A) Remove the schema entirely so the model can explain its severity judgment in free-form prose instead.
- B) Force the same schema-valid tool call a second time, and keep whichever of the two results happens to look more severe.
- C) Semantic severity criteria plus validation logic that distinguishes a production blocker from a test-only failure using observable impact, not just schema shape.
- D) A larger context window, given to the exact same ambiguous tool with no new severity criteria and no additional examples of the production-versus-test distinction it keeps missing.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

Your coordinator produces technical due-diligence reports using web, document, data, and synthesis specialists connected to several MCP servers.

**Question 31.** A routine request asks for one documented API limit, while a strategic report needs market, security, cost, and implementation analysis. How should orchestration differ?

- A) Both requests should invoke every available specialist, on the theory that identical coverage makes the two reports more consistent with each other.
- B) Both requests should run through the same fixed one-agent workflow, regardless of how narrow or broad the underlying question actually is.
- C) The coordinator should pick the minimum suitable path for the single factual query, and assemble the broader specialists only for the strategic report.
- D) Escalate the single factual query to a human, and reserve multi-agent orchestration only for requests that already contain several explicit user questions before any tool selection begins.

**Question 32.** A global infrastructure study has repeatedly omitted smaller regions. What decomposition best protects coverage?

- A) Partition the study by complementary regions and evidence types, give each partition an explicit coverage goal, and check the combined result against the full region list for gaps before finalizing it.
- B) Ask every research agent to independently cover the entire world on its own, with no explicit partition of regions between them.
- C) Decompose the study only by the largest infrastructure vendors, since they happen to have the most available sources, and simply assume their coverage stands in for the smaller regions those same vendors don't actually serve.
- D) Make the final report longer with additional narrative detail, without changing which regions any agent was actually assigned to cover.

**Question 33.** A review of 80 modules requires the same security and performance checks on each, plus one architecture-wide dependency pass. Which pattern is most appropriate?

- A) One open-ended agent that reads all 80 modules in a single pass, relying entirely on a larger context window to keep its attention to security and performance checks equally distributed throughout.
- B) Fixed, focused security and performance passes applied identically to each of the 80 modules, followed by a separate architecture-wide dependency review that looks across module boundaries.
- C) Dynamic task generation for each module, with no stable security or performance checklist repeated between them.
- D) Independent local passes over each module, each producing findings with no final cross-module architecture synthesis at the end.

**Question 34.** Synthesis reveals that all cost estimates assume one deployment model, but a newly discovered regulatory rule requires a second model in two regions. What should the coordinator do?

- A) Preserve every original research task exactly as assigned, purely to keep the study reproducible, even though the new rule changes two regions' cost basis.
- B) Delete all completed research across every region and restart the entire due-diligence study from scratch.
- C) Ask the synthesis specialist to produce a structured provisional estimate for the second deployment model without commissioning any new source research at all, and label the resulting regional costs as provisional.
- D) Generate targeted subtasks covering the two affected regions and the second deployment model's costs, then update only the synthesis sections that depend on them while keeping the unaffected findings.

**Question 35.** The whole team needs a stable internal-document MCP server after cloning the repository. Where should it be defined?

- A) In each team member's personal `~/.claude.json`, with the server settings manually copied from one working example into every other person's file.
- B) In the committed project `.mcp.json`, so each teammate who clones the repository gets the same internal-document server configuration automatically, without any manual setup step.
- C) In the coordinator's natural-language prompt text, describing the internal-document server in prose instead of configuring an actual MCP connection.
- D) In a user-level slash command that only the person who created it can run, and only on their own machine, never shared with the rest of the team.

**Question 36.** The shared server requires a different token for each environment. How should authentication be represented in the committed definition?

- A) As a literal token string committed directly in `.mcp.json`, formatted to look encrypted or hashed even though it is really just the same plain secret checked into the shared repository.
- B) As a token pasted directly into `CLAUDE.md`, to be manually re-pasted by hand at the start of every new session on every machine.
- C) As a value that an otherwise-unrestricted MCP tool can return to any caller who asks for it, environment aside.
- D) As environment-variable expansion inside the committed definition, with the actual per-environment value resolved outside version control at connection time.

**Question 37.** The research application connects to document, statistics, and news MCP servers. What happens during connection?

- A) Tools from the document, statistics, and news servers are all discovered together at connection time and exposed to the agent, which can then call any of them as the research task actually requires.
- B) Only the tools from whichever configured server happens to sort first alphabetically by name are actually made available to the agent, regardless of the other two servers configured.
- C) Configuring the document and statistics servers at project scope silently disables every server the user has separately configured at user scope.
- D) The coordinator has to reconnect to each server every single time it switches which specialist is currently active, and that connection is only ever cached for the current specialist's one turn before it must reconnect all over again.

**Question 38.** Agents waste calls asking which datasets, reports, and schemas exist. What should the servers expose?

- A) A generic lookup tool that guesses at a likely dataset name from the agent's query, and returns whatever happens to match closest.
- B) Larger, more detailed error messages that list every available asset only after an agent's call has already failed to find one.
- C) MCP resources that catalog which datasets, reports, and schemas exist and describe their structure, so an agent can browse that catalog before making any exploratory call at all.
- D) A PostToolUse hook that automatically repeats every search the agent already ran, in case a different asset turns up the second time.

**Question 39.** `query_metrics` and `search_reports` both accept text, and the model uses them interchangeably. Which description change matters most?

- A) Rewrite both descriptions to focus on each tool's implementation language, hosting infrastructure, and deployment region, details that say nothing about which one to call for a given question.
- B) Shorten both descriptions so the model reads them faster, and rely on the tool names and which server they came from to imply the difference between them.
- C) Give `query_metrics` and `search_reports` the exact same set of examples, to emphasize that they behave consistently with each other.
- D) State each tool's distinct data source, expected query format, output shape, and boundaries, plus a worked example question for each.

**Question 40.** A source-selection prompt says, “Whenever the user says current, always use web search,” causing live database metrics to be ignored. What is the best diagnosis?

- A) The system prompt's unconditional rule ties the word "current" to web search regardless of context, and should be revised alongside the tool descriptions so live database metrics aren't excluded.
- B) The database tool's JSON schema needs longer property names and recency-ordered aliases, so the model happens to notice it before it notices the web-search tool.
- C) MCP discovery is structurally unable to expose a database tool and a web-search tool to the same agent during the same session at all.
- D) The model requires an explicitly random source-selection policy applied whenever a query could plausibly use either the database or web tool.

**Question 41.** A generic `process_source(mode=search|extract|verify)` tool frequently receives the wrong mode. What interface change gives the model clearer decisions?

- A) Add several more values to the `mode` enum, on the assumption that more granular modes will make the single correct one easier for the model to select each time.
- B) Hide the `mode` field from the model entirely, ask downstream code to infer search, extract, or verify from the prompt text, keeping one generic permission boundary.
- C) Split `process_source` into three purpose-specific tools, one each for search, extract, and verify, each with its own request schema and its own least-privilege permission scope, distinct from the others.
- D) Force the generic `process_source` tool to run on every single turn, regardless of which of the three underlying operations the task actually needs performed.

**Question 42.** A statistics provider returns HTTP 503. What metadata most directly tells the agent whether another attempt is sensible?

- A) The provider's full HTML error page returned as though it were structured data, requiring the agent to parse retry instructions out of untrusted markup that was never meant to be machine-read.
- B) A transient error category, an `isRetryable: true` flag, the attempted operation, and a suggested backoff interval.
- C) A successful response containing an empty dataset, as though the query had simply found no matching statistics.
- D) A non-retryable business-rule category, as though the 503 reflected a permanent policy decision rather than a temporary outage.

**Question 43.** A well-formed query legitimately finds no studies in the requested date range. How should that differ from access denial?

- A) Return a successful empty result when the query legitimately finds no studies; return a distinct typed permission error when access itself was denied.
- B) Return the exact same generic error string for both a legitimate no-match result and a denied-access failure, and ask the coordinator to work out which one actually happened purely from the surrounding conversational text.
- C) Mark both cases as retryable, on the reasoning that neither one returned any actual data back to the caller.
- D) Represent both a genuine no-match and a denied-access failure as ordinary successful prose messages describing what happened.

**Question 44.** A named session has an accurate source taxonomy, and only two ingestion adapters changed. You want to continue the investigation. What should you do?

- A) Start a blank session, discard the accurate source taxonomy that's already been carefully built, and rebuild the whole thing from public documentation before even looking at the two changed adapters.
- B) Resume the named session and continue the investigation without mentioning that the two ingestion adapters changed at all.
- C) Fork the named session solely to refresh filesystem state, on the assumption that forking by itself re-reads the two changed adapters.
- D) Resume the named session, since the accurate source taxonomy is still valid, explicitly identify which two ingestion adapters changed, and request a targeted re-analysis limited to just those two.

**Question 45.** Two teams want to compare incompatible synthesis architectures from the same accepted evidence map. Which session mechanism preserves the shared baseline and isolates later reasoning?

- A) Run both synthesis architectures sequentially inside the same conversation, one after the other, sharing all of the same context throughout.
- B) Fork the accepted-evidence session into two independent branches, one per synthesis architecture, so each team's reasoning develops separately from a shared starting point.
- C) Resume the exact same named session twice at once, from two separate terminals, and allow both teams to make concurrent, conflicting edits to what is really just one shared piece of underlying session state.
- D) Start two entirely blank sessions, one for each team, with no shared evidence map carried into either one.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

Your extraction platform handles procurement documents from many regions and vendors. It already uses tool schemas, but accuracy and reviewer efficiency vary across formats.

**Question 46.** Purchase-order numbers appear in page headers, table captions, and barcode-adjacent labels. The extractor handles only headers. What should you add first?

- A) A few-shot set demonstrating the same purchase-order-number field correctly extracted from a header, a table caption, and a barcode-adjacent label.
- B) A hard requirement that every purchase-order number appear in the page header, which rejects otherwise valid orders whose number only appears in a table caption or next to a barcode.
- C) A retry that resubmits the exact same unchanged extraction prompt, in case a different header-only pass happens to notice the other placements.
- D) A free-form text answer in place of the existing extraction schema, letting the model describe wherever it thinks the number appears.

**Question 47.** Some source documents genuinely omit shipping terms. The current required string causes plausible invented terms. Which schema behavior is appropriate?

- A) Silently normalize the missing shipping-terms field to that vendor's historically most common value, so the schema always sees something filled in.
- B) Reject every document that has no shipping-terms field at all, treating its total absence as equivalent to a data-quality failure, even when every other field extracted correctly.
- C) Keep the field required, ask the model in the prompt to be honest about missing values, and make runtime validation responsible for catching any invented term after the fact.
- D) Allow the shipping-terms field to be null or omitted entirely, and state explicitly, both in the schema description and the prompt, that missing source information must not be invented just to fill the field.

**Question 48.** A contract-type enum does not include a newly encountered but valid category, and some scans are too degraded to classify at all. How should both cases be represented?

- A) Map both the newly encountered valid category and the unreadable scans to whichever nearest known enum value happens to be the closest fit, even though the source clearly distinguishes a genuine novel category from evidence that simply can't be read at all.
- B) Remove the contract-type enum entirely and accept arbitrary prose instead, skipping schema validation for that field altogether.
- C) Use `other` plus a free-text detail field for the valid but unlisted category, and use `unclear` for the scans that are genuinely too degraded to classify.
- D) Reject both the newly categorized document and the degraded scan outright, without extracting any of their other fields.

**Question 49.** Validation says `subtotal + tax != total`. What should the self-correction request contain?

- A) Only the correct total value, computed independently and handed to the model, with no explanation of which extracted field was actually wrong.
- B) The original source text, the failed extraction, and the exact arithmetic validation error showing that subtotal plus tax doesn't equal the stated total.
- C) A new version of the schema with subtotal, tax, and total all made optional, so the mismatch simply can't trigger a validation failure anymore.
- D) A demand that the model return different numbers for subtotal, tax, or total without pointing back to any source evidence, and accept whichever new combination happens to satisfy the arithmetic check.

**Question 50.** A requested signature is absent because the scan ends before the signature page. Which response is correct?

- A) Keep retrying the extraction with varied temperature and reworded prompts until the model eventually supplies some signature-like value.
- B) Infer the missing signer's identity from the named contract owner listed elsewhere in the document, treating that role as an adequate substitute.
- C) Stop extraction retries regardless of prompt wording or temperature, since the page genuinely isn't in the scan, and route the document to rescanning, human review, or an explicitly documented missing value.
- D) Use a fabricated "signature present" default value, so downstream processing never sees a missing field anywhere in this contract or any similar one.

**Question 51.** Monetary values arrive as `$1,200.50`, `1.200,50 €`, and `1200.5 USD`. What should accompany the structured schema?

- A) Explicit currency and numeric normalization rules, with worked examples for comma, period, and symbol placement, plus guidance for genuinely ambiguous cases.
- B) A rule that discards the currency symbol or code entirely, keeping only the bare numeric value regardless of which currency it actually represents.
- C) A higher sampling temperature, on the theory that more creative formatting will help the model reconcile the three different input conventions.
- D) A random retry triggered after every non-US-style value, treating whichever US-style parse happened to appear first in the batch as the canonical baseline for every other format to match.

**Question 52.** Documents arrive with unknown type, and one of several extraction tools must be called so downstream processing never receives conversational prose. Which configuration is most reliable?

- A) `tool_choice: "auto"` alongside a structured-sounding request in the prompt asking Claude to prefer using a tool, without forcing one.
- B) Prefill an opening JSON brace in a plain-text response, and rely on downstream code to parse and repair whichever document-specific fields happen to follow.
- C) Force the invoice-extraction tool on every document, regardless of whether it's actually an invoice, a purchase order, or a shipping manifest.
- D) Use structured extraction tools for each document type together with `tool_choice: "any"`, so a tool call is guaranteed while Claude still selects whichever schema actually matches the document.

**Question 53.** The model flags every handwritten annotation as a fraud indicator, though most are harmless initials. Which few-shot set best sharpens the decision boundary?

- A) A few-shot set built from ten confirmed fraud annotations only, with no example of a harmless initial or reviewer note included anywhere in the set.
- B) A representative set of positive fraud examples plus near-miss negative examples, such as harmless initials and ordinary reviewer notes that look superficially similar.
- C) Use no examples at all, request conservative scoring in the prompt instead, and discard every single prediction that falls below a high but purely intuitive confidence threshold.
- D) One single example, with no explanation given for why it was labeled the way it was.

**Question 54.** Bank-account fields are high risk, while optional marketing codes are low risk. Both have confidence 0.82. What should routing do?

- A) Apply field-specific risk and ambiguity thresholds, so the high-consequence bank-account field at 0.82 confidence routes to human review while the low-risk marketing code follows a lighter, policy-defined path.
- B) Treat the equal 0.82 confidence score as equal operational risk, apply the exact same review threshold to both fields, and ignore field consequence, source ambiguity, or reviewer expertise entirely.
- C) Average the bank-account and marketing-code confidence scores into a single document-level confidence figure that ignores each field's distinct consequence.
- D) Randomly choose one of the two fields for human review, and let the other proceed automatically regardless of which one was picked or how consequential it is.

**Question 55.** Confidence thresholds were calibrated before adding new languages and a substantially revised prompt. What should happen before continued auto-acceptance?

- A) Keep the existing thresholds unchanged, since the output schema itself didn't change, and assume field-level accuracy carries over identically to the new languages.
- B) Lower every threshold by the same fixed amount, regardless of which fields or languages actually saw their accuracy shift after the prompt revision.
- C) Recalibrate the thresholds against newly labeled data that specifically represents the added languages, the revised prompt, and the exact fields and document segments the changes actually affected.
- D) Ask the model directly whether its own reported confidence still feels accurate after the prompt revision, and trust whatever it reports back.

**Question 56.** What monitoring practice can reveal a new high-confidence error pattern after automation?

- A) Review only the cases that validation already rejected, since anything auto-accepted already passed its checks and needs no further look.
- B) Have humans review a stratified sample specifically drawn from the extractions that were auto-accepted, and track the types of error found in that sample over time so an emerging high-confidence failure pattern gets caught before it spreads.
- C) Compare confidence scores across batches over time, without ever examining the extractions against actual ground truth.
- D) Rerun the same successfully processed documents with the exact identical prompt every time, assume that getting the same answer again automatically means it was correct the first time, and use that repeated agreement as the ongoing monitoring metric.

**Question 57.** A single extraction change causes amount parsing, tax calculation, and currency labeling failures because all three share one normalization rule. How should refinement feedback be presented?

- A) Correct the amount, tax, and currency-labeling symptoms in three separate, isolated sessions, without mentioning the one shared normalization rule behind all three, then reconcile whatever inconsistent patches come out once all three changes are merged together.
- B) Fix only the amount-parsing failure first, and hope the tax and currency-labeling failures resolve on their own as a side effect.
- C) Add a permanent description of all three failures to `CLAUDE.md`, without changing the shared normalization rule that's actually causing them.
- D) Batch the three interacting failures together with the shared normalization rule that causes all of them, so one coherent fix can be evaluated against all three at once.

**Question 58.** The extractor mishandles a nested table only when a row contains both a null quantity and a discount. What feedback most directly guides correction?

- A) The one-line note "improve table support," with no reference to the specific null-quantity-plus-discount combination that actually fails.
- B) A substantially longer system prompt describing common nested-table shapes in general terms, while never actually including the specific failing input row or its expected corrected output.
- C) The exact source fragment for the failing row, the failed output, the expected output, and a regression case covering that specific null-quantity-plus-discount combination.
- D) A higher maximum output token count, applied to the same prompt that already omits the failing row entirely.

**Question 59.** A personal prototype extraction server and a shared production server are both needed on one developer's machine. What setup preserves the intended scopes?

- A) Keep the shared production server in project `.mcp.json` with environment-resolved credentials, and keep the personal prototype in the developer's own `~/.claude.json`; MCP discovery exposes both together.
- B) Put both the production server and the personal prototype in project `.mcp.json`, ask teammates to simply ignore the prototype entry, and require each person to locally edit the file before it will actually run.
- C) Put both the production and prototype servers in user scope, so that neither configuration is ever committed to the shared repository, even the production one every teammate needs to have configured.
- D) Describe the production server's purpose in `CLAUDE.md` instead of configuring an actual `.mcp.json` entry, leaving each teammate to set it up individually on their own machine.

**Question 60.** You need to determine which parsers handle `.xlsx` files and then understand only their normalization paths. What is the best context-conscious exploration sequence?

- A) Read every parser file and every one of its dependencies in full, before running any search for `.xlsx` handling at all.
- B) Glob for likely parser files, Grep those candidates for `.xlsx` handling, then Read only the matching code and its relevant imports.
- C) Grep only the generated output directory, since it's excluded from normal edits, and treat whatever recurring examples turn up there as a proxy for the current source implementation and its actual normalization path.
- D) Edit the first parser file whose filename happens to contain the word "excel," without confirming it actually handles `.xlsx`.

---

# Answer Key — Practice Exam 14

**Quick key:** 1-B, 2-D, 3-A, 4-C, 5-D, 6-B, 7-C, 8-A, 9-B, 10-C, 11-A, 12-D, 13-C, 14-B, 15-D, 16-A, 17-C, 18-D, 19-B, 20-C, 21-A, 22-B, 23-D, 24-A, 25-D, 26-B, 27-C, 28-D, 29-A, 30-C, 31-C, 32-A, 33-B, 34-D, 35-B, 36-D, 37-A, 38-C, 39-D, 40-A, 41-C, 42-B, 43-A, 44-D, 45-B, 46-A, 47-D, 48-C, 49-B, 50-C, 51-A, 52-D, 53-B, 54-A, 55-C, 56-B, 57-D, 58-C, 59-A, 60-B

**Focus key:** 1-DEC, 2-DEC, 3-DEC, 4-DEC, 5-ERR, 6-ERR, 7-ERR, 8-DESC, 9-DESC, 10-REV, 11-REV, 12-REV, 13-MCP, 14-RES, 15-RES, 16-CFG, 17-CFG, 18-CFG, 19-CFG, 20-CFG, 21-CFG, 22-REF, 23-REF, 24-REF, 25-REF, 26-EXP, 27-EXP, 28-EXT, 29-EXT, 30-EXT, 31-DEC, 32-DEC, 33-DEC, 34-DEC, 35-MCP, 36-MCP, 37-MCP, 38-MCP, 39-DESC, 40-DESC, 41-DESC, 42-ERR, 43-ERR, 44-RES, 45-RES, 46-EXT, 47-EXT, 48-EXT, 49-EXT, 50-EXT, 51-EXT, 52-EXT, 53-EXT, 54-REV, 55-REV, 56-REV, 57-REF, 58-REF, 59-MCP, 60-EXP

Focus codes: CFG = Claude Code configuration selection; MCP = MCP scope and integration; DEC = adaptive decomposition; EXT = extraction accuracy; REF = iterative refinement; EXP = codebase exploration; DESC = tool descriptions; RES = session resumption; REV = human-review routing; ERR = MCP error handling.

---

**1. B** — Independent concerns can be investigated in parallel once identity is confirmed, and coordinator synthesis produces one coherent resolution. Serializing by first-mentioned concern, blanket escalation, and unsynthesized replies each waste capability or fragment the case.

**2. D** — Predictable address changes suit a fixed prerequisite chain, whereas takeover investigations must branch on the device, login, and payment evidence as it's discovered. Applying one decomposition style to both, whether always-dynamic or one merged unrestricted prompt, ignores the difference between known stages and open-ended discovery.

**3. A** — Adaptive orchestration folds in the new identity evidence through one added subtask and updates only what depends on it. Waiting out the whole plan, wiping verified evidence, and freezing the plan against new evidence all ignore what the investigation just learned.

**4. C** — An unclear systemic cause needs process mapping and metrics before subtasks can target the contributors the data actually shows. Immediate optimization, an aggregate rerun of the individual-case checklist, and a conclusion drafted before evidence each assume the answer before gathering it.

**5. D** — The identifier is invalid input, so the tool should return a validation category naming the checksum problem and the accepted format, with no retry until the value changes. A resent identical retry, empty success, and a mislabeled permission error all point the caller toward the wrong recovery path.

**6. B** — A safe, one-time transient retry belongs close to the failure, inside the specialist that hit it, so only genuinely unresolved failures reach the coordinator. Queuing for a human before trying, deferring to the final response, and fanning the retry out to unrelated specialists all delay or misplace the recovery.

**7. C** — Structured partial results, attempted actions, and a typed transient-failure category let the coordinator preserve completed checks and choose between retry, escalation, or an alternative. A bare failure notice, a false success, and an unfiltered raw log each destroy or bury that operational detail.

**8. A** — Distinct purposes, identifiers, outputs, examples, and explicit cross-references give the model the selection evidence the two descriptions currently lack. Forcing both calls, adding more tools, and keyword routing all leave the underlying ambiguity in place.

**9. B** — Purpose-specific tools make destructive intent explicit up front and let each operation carry its own contract and least-privilege permission. Normalizing the enum, adding a prompt reminder, and doubling the same ambiguous call all preserve the interface that caused the wrong-mode failures.

**10. C** — Review should track field-level uncertainty and consequence, so the risky amount reaches a qualified reviewer without stalling the fields that are already clear. A high document-wide average, an unrelated random sample, and a blanket rejection each misjudge where the actual risk sits.

**11. A** — Assignment should follow the specific expertise a field's uncertainty calls for, whether visual-damage judgment or policy interpretation, rather than defaulting to whoever is available. A shared random reviewer, a document-wide score, and an unvalidated self-prediction all miss that distinction.

**12. D** — A confidence number only becomes meaningful once it is checked against labeled outcomes for that field and document type. Prompted wording, an intuition-based threshold, and same-context self-agreement don't establish accuracy.

**13. C** — Shared tooling belongs in the committed project `.mcp.json`, while resolving the secret from an environment variable keeps the per-environment value out of version control. Per-operator personal configuration, a literal committed secret, and prose-only documentation each fail to give the whole team a working, secure setup.

**14. B** — Agreements that don't depend on live systems can carry over, but order status and provider state must be re-checked and any changes surfaced to the resumed agent explicitly. Trusting a name, dropping a valid authorization, and assuming a fork refreshes external systems on its own are each unsafe shortcuts.

**15. D** — Redesigned contracts and routes make old operational context unsafe to reuse, so a fresh session seeded with durable goals plus targeted re-analysis of the new interface is the safer path. Refusing every tool call, comparing branches that still share the stale contracts, and reusing old outputs all carry the outdated interface forward.

**16. A** — Glob-scoped rules apply automatically to workflow files wherever they live without taxing ordinary code sessions. Personal memory that must be replicated by hand, an optional skill someone can forget, and an unscoped root instruction each either under- or over-apply the convention.

**17. C** — `@import` composes the centrally maintained guidance into each package's own file without copying its text, so drift stops at the source. Duplicating the standard everywhere, wrapping it as a tool, and keeping it only in personal memory pasted into prompts each reintroduce drift or leave some runners without it.

**18. D** — A team-shared, on-demand workflow is a project skill; `context: fork` keeps its verbose exploration out of the main conversation, and read-only `allowed-tools` structurally rules out writes. Always-loaded memory, a personal command with full tool access, and an unconditional path rule each miss one of the on-demand, shared, or read-only requirements.

**19. B** — Settings permission-deny rules block the prohibited tools and paths before execution, which is what a stable, business-state-independent prohibition needs. A prose request, a hook that only reacts afterward, and a per-PR reminder are all advisory rather than enforced.

**20. C** — This decision depends on the live signed manifest and the exact arguments about to run, which is exactly what a `PreToolUse` hook can check and block on. A cosmetic formatting rule, an unvalidated command, and a manually updated stale reference cannot verify the current build.

**21. A** — Recurring shared CI context belongs in committed project memory, so every invocation of Claude Code in the pipeline sees the same review standards, fixtures, and test commands. A per-run inline prompt, a personal command directory scoped to one developer, and generated output all fail to reach every CI session.

**22. B** — Concrete paired examples show exactly how blank, null, and ordinary values must each transform, resolving the ambiguity no prose fully specifies. A single example paired with vague wording, more output tokens, and an instruction to normalize semantics by inferring them from style all leave the actual transformation undefined.

**23. D** — A regression suite anchors both fixtures as executable checks, and feeding back the specific failing test drives each iteration toward a fix that satisfies both. Relying on conversation memory, discarding the older fixture, and varying temperature all abandon the case that keeps breaking.

**24. A** — The interview pattern surfaces the unresolved retry, idempotency, ordering, and partial-failure decisions and records stakeholder answers before code commits to any of them. Coding a default first, inferring policy from unrelated analogous code, and formatting cannot substitute for those decisions.

**25. D** — Findings that share one root cause converge fastest when batched with that shared context, while independent issues like typos don't need to ride along. Isolating every finding into its own session, dumping all six together, and deferring the typos indefinitely each mis-sequence the work.

**26. B** — Glob matches file paths by pattern, which is exactly what's needed to locate candidates by name alone, before any content is inspected. Grep searches inside contents, Read opens one file at a time, and Edit modifies a file already open — none of them locate candidates by filename.

**27. C** — Grep narrows the candidates down to files that actually reference the symbol, and a targeted Read then supplies only the matching setup and helpers. Reading everything first, treating a function name as a filename pattern, and replacing the helper to see what breaks each waste context or risk an unreviewed change.

**28. D** — Positive examples plus near-miss negatives teach the boundary between an actual secret and a harmless identifier that merely looks similar. Removing examples, repeating one positive case, and reporting every log line regardless of content each fail to sharpen that boundary.

**29. A** — Schemas define shape, but explicit normalization rules and worked examples define which canonical form is expected across otherwise inconsistent source formats. More required fields, unguided retries, and downstream guessing after the fact each leave the canonical form undefined.

**30. C** — Schema validity only checks shape; observable-impact criteria and validation logic are what can tell a test-only failure from a real production blocker. Dropping the schema, repeating the same ambiguous call, and adding context without new criteria all leave the severity judgment unchanged.

**31. C** — Delegation should scale with what the task actually needs: a single documented fact doesn't need a research organization, while the strategic report's breadth does. Uniform full-team invocation, one fixed workflow for both, and escalating a routine factual lookup each mismatch effort to task complexity.

**32. A** — Complementary partitioning with explicit coverage goals, plus a gap check against the full region list, is what actually protects smaller regions from being dropped. Independent whole-world assignments overlap without covering everything, assuming vendor coverage stands in for smaller regions repeats the same omission, and a longer report doesn't fix unassigned scope.

**33. B** — The same repeated security and performance checks fit a fixed, focused pass per module, with a separate integration pass catching what only shows up across modules. One huge open-ended read dilutes attention across 80 modules, an unstable checklist loses consistency, and skipping synthesis misses cross-module issues entirely.

**34. D** — The new rule only changes cost assumptions for two regions, so targeted subtasks can refresh that research and update the dependent synthesis while everything else stands. Freezing the original tasks, restarting the whole study, and having synthesis invent a structured-looking number without new research each mishandle a partial, localized change.

**35. B** — A server the whole team needs after cloning belongs in committed project `.mcp.json`, so it's available automatically rather than through per-person manual setup. Personal configuration files, prose in a prompt, and a personal slash command each fail to reach every teammate the same way.

**36. D** — Environment-variable expansion lets the committed file resolve a different real token per environment without ever storing a secret in version control. A committed literal, however it's formatted, a manually re-pasted token, and an unrestricted credential-returning tool all expose the actual secret.

**37. A** — MCP clients discover every configured server's tools at connection time and can expose them to the agent together, regardless of server order or which specialist is active. An alphabetical-only rule, project scope disabling user scope, and per-turn reconnection caching don't describe how discovery actually works.

**38. C** — MCP resources give agents a stable catalog of what exists and its structure to consult up front, instead of discovering assets through trial-and-error calls. A guessing tool, bigger post-failure error messages, and a hook that blindly repeats searches all still rely on wasted exploratory calls.

**39. D** — The model needs source, format, output-shape, and boundary distinctions plus concrete examples to choose reliably between two text-accepting tools. Implementation trivia, shorter descriptions that lean on naming alone, and identical examples all leave the actual difference undescribed.

**40. A** — An unconditional keyword rule in the system prompt is overriding a legitimate distinction the tool contracts should otherwise support, so both need revision together. Longer property names, a claim about MCP's discovery limits, and a random policy each misdiagnose a prompt-level overgeneralization as something else.

**41. C** — Purpose-specific tools remove the mode-selection guess entirely and let each operation carry its own schema and least-privilege permission. Adding modes, hiding the field for downstream code to infer, and forcing one generic call every turn all keep the same ambiguous interface.

**42. B** — An explicit transient category, a retryability flag, the attempted operation, and a backoff suggestion give the agent exactly what it needs to decide whether to try again. Untrusted HTML to parse, a false empty success, and a non-retryable label for what is really a temporary outage each obscure that decision.

**43. A** — A legitimate empty result is valid success, while denied access is a distinct operational error with its own recovery path, so the two need different, typed representations. Collapsing them into one generic error the coordinator has to guess at, marking both retryable, and treating both as prose successes each blur that distinction.

**44. D** — Most of the session's context, including the source taxonomy, remains valid, so naming it back and requesting targeted re-analysis of just the two changed adapters is the efficient path. Discarding valid context, resuming silently, and forking to refresh files each waste or skip the work still needed.

**45. B** — Forking gives each team an independent branch that starts from the same accepted evidence map, so their later reasoning can diverge without contaminating each other. Running both sequentially in one conversation, resuming the same session concurrently from two places, and starting from blank sessions each lose the shared or isolated properties the comparison needs.

**46. A** — Representative few-shot examples teach the extractor to recognize the same field across header, caption, and barcode-adjacent placements, rather than just the one layout it already handles. Requiring a single placement, repeating the unchanged prompt, and dropping the schema for free text don't add the missing evidence.

**47. D** — A nullable or omittable field accurately reflects genuine absence and removes the pressure that a required string creates to invent a plausible value. Silently normalizing to a common default, rejecting the whole document, and relying only on downstream validation each still let the required field push toward fabrication or an unnecessary rejection.

**48. C** — `other` with a detail preserves a genuinely novel category instead of mislabeling it, and `unclear` keeps unreadable evidence honestly distinct from a known classification. Forcing both into the nearest existing enum value, dropping the enum and its validation for free text, and rejecting both documents outright each lose or misrepresent that distinction.

**49. B** — Semantic self-correction needs the source text, the failed candidate, and the exact arithmetic discrepancy so the model can fix the actual error instead of guessing. Handing over only the answer, loosening the schema so the check can't fire, and demanding new numbers with no evidence each invite an unsupported but schema-valid fix.

**50. C** — No amount of retrying or rewording can extract content the scan never captured, so the pipeline should stop and route to rescanning, review, or a documented absence. Continued retries, inferring a signer from the contract owner, and a fabricated default each manufacture evidence that was never in the source.

**51. A** — Explicit normalization rules with worked examples define how each locale's format maps to one canonical value, including how to handle genuine ambiguity. Discarding currency entirely, raising temperature, and anchoring on whichever US-style value parsed first are not defined rules at all.

**52. D** — `tool_choice: "any"` guarantees some structured tool call happens while still letting Claude select the schema that matches the document, so prose never reaches downstream code. Auto still permits a plain-text reply, prefilled JSON still needs ad hoc repair, and forcing one document type's tool can select the wrong schema.

**53. B** — Positive examples paired with near-miss negatives, like harmless initials, teach the boundary the extractor is currently missing between real fraud markers and ordinary annotations. A one-sided fraud-only set, no examples with an intuitive cutoff, and a single unexplained example each fail to show that boundary.

**54. A** — The same confidence number carries very different operational risk depending on the field's consequence, so routing should apply field-specific thresholds rather than a single rule. Treating equal confidence as equal risk, averaging into one document score, and choosing randomly all erase the distinction that actually matters here.

**55. C** — A revised prompt and new languages can shift the relationship between a confidence score and actual accuracy, so thresholds need recalibration against labeled data reflecting those changes. Assuming schema stability implies accuracy stability, an across-the-board threshold cut, and simply asking the model each skip the labeled recalibration that's actually needed.

**56. B** — Stratified human review of auto-accepted output, tracked over time, is what surfaces a new high-confidence error pattern that validation and confidence scores alone never see. Reviewing only what validation already rejected, comparing scores without ground truth, and treating repeated agreement as correctness each skip the actual ground-truth check needed.

**57. D** — One shared normalization defect causing three symptoms calls for one batched fix evaluated against all three together. Isolating each symptom into its own session, fixing only the first field, and just documenting the failures each leave the shared cause unaddressed or invite conflicting patches.

**58. C** — The exact failing fragment, the wrong output, the expected output, and a regression case for that specific combination give a concrete, testable target. A vague instruction, a longer general system prompt without the actual failing case, and more output tokens each fail to point at the specific edge condition.

**59. A** — Committed project scope with environment-resolved credentials keeps production shared and secure, while user scope keeps the personal prototype out of the shared file; MCP discovery still exposes both to that developer. Committing the prototype for everyone to ignore, keeping production out of the shared file entirely, and describing a server without configuring it each break the intended scope.

**60. B** — Path matching narrows down likely parsers, targeted content search confirms which ones actually handle `.xlsx`, and a final Read covers only the matching code and its imports. Reading everything up front, treating generated output as a stand-in for source, and editing by filename guess each skip or misplace the discriminating search.

*End of Practice Exam 14.*
