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

- A) Run a fixed shipping-only workflow because the first concern determines the case type, then open billing only after shipping closes.
- B) Create separate shipment and billing subtasks, run them concurrently, then synthesize one case resolution.
- C) Escalate immediately because any multi-concern request exceeds autonomous scope.
- D) Let two agents respond directly to the customer without coordinator synthesis.

**Question 2.** Address changes always require verify identity → validate new address → update account. Account-takeover reports branch according to device, login, and payment evidence discovered during investigation. Which decomposition is best?

- A) Use dynamic decomposition for both because customer state can always change and newly discovered evidence can always expand scope.
- B) Run both workflows as one unrestricted prompt.
- C) Use one fixed pipeline for both so auditing is simpler.
- D) Use a fixed chain for address changes and adaptive decomposition for takeover investigations.

**Question 3.** A fraud investigation discovers that the disputed transaction belongs to a second customer profile sharing the same email domain. What should happen to the existing investigation plan?

- A) Add a targeted identity-linkage subtask and revise dependent work while preserving unaffected findings.
- B) Complete every original subtask before considering the new profile.
- C) Restart the case from an empty context and discard verified evidence.
- D) Ignore the second profile because it was not in the initial plan and preserve the original timeline for audit consistency.

**Question 4.** The agent must investigate “why refund completion times rose this month,” but the cause could be policy, provider latency, regional routing, or case mix. What is the strongest first step?

- A) Ask the payment specialist to optimize retries immediately.
- B) Run the same fixed refund checklist used for individual customers.
- C) Map the process and relevant metrics, then generate prioritized subtasks from the observed contributors.
- D) Assign one specialist to write a final explanation before gathering evidence, then ask the other specialists to support that conclusion.

**Question 5.** `lookup_order` receives an identifier with an invalid checksum. Retrying unchanged cannot succeed, but the customer can correct the value. What error should the tool return?

- A) A transient error with exponential backoff that keeps resending the identical invalid identifier until a retry succeeds.
- B) A successful empty result.
- C) A permission error requiring supervisor access.
- D) A structured validation error marked non-retryable until input changes, including the required format.

**Question 6.** The shipping provider times out once, and the lookup is safe to repeat. Where should the first recovery attempt occur?

- A) In a human escalation queue before any retry.
- B) Locally in the specialist, with only unresolved failure context propagated to the coordinator.
- C) In the final response by asking the customer to try again later without exposing internal provider details.
- D) In every other specialist so one of them may reach the provider.

**Question 7.** A refund specialist successfully verifies identity and policy eligibility but cannot reach the payment provider after safe retries. What should it return to the coordinator?

- A) Only “refund failed.”
- B) A false success so the case can continue.
- C) The verified partial results, attempted actions, typed transient failure, retry status, and available next steps.
- D) The entire raw provider log, including headers and internal identifiers, with no summary of what remains recoverable.

**Question 8.** The agent swaps `get_customer_profile` and `get_customer_authorizations` because both descriptions say “gets customer information.” What should be changed first?

- A) Give each description distinct use cases, identifiers, output fields, examples, and explicit guidance about when to use the other tool.
- B) Force both calls for every customer request.
- C) Add more customer tools so Claude has additional choices.
- D) Route by a growing hard-coded list of words such as “customer,” “profile,” and “authorization,” then revise it after each misroute.

**Question 9.** A generic `modify_account(action, value)` tool can change contact details, disable MFA, or close the account. The wrong mode has caused destructive calls. What redesign most directly improves reliability?

- A) Keep the generic tool but make the action enum longer.
- B) Split sensitive operations into purpose-specific tools with separate contracts and permissions.
- C) Add “be careful” to the coordinator prompt.
- D) Require the generic tool to run twice and compare its own arguments.

**Question 10.** Most fields on a refund claim are clear, but the claimed amount is handwritten, low-confidence, and financially consequential. What review routing is best?

- A) Accept the whole claim because its average confidence is high and treat that average as proof no individual field needs attention.
- B) Send a random unrelated field for review to preserve sampling.
- C) Route the amount field to a qualified reviewer while allowing unambiguous low-risk fields to continue.
- D) Reject the whole claim automatically because handwriting appears anywhere.

**Question 11.** Warranty photos require visual-damage expertise, while ambiguous policy exceptions require a policy specialist. How should reviewer assignment work?

- A) Route by the uncertain field's characteristics and required expertise, not by reviewer availability alone.
- B) Send both types to the same randomly selected reviewer.
- C) Route only according to whole-document confidence.
- D) Let the model choose a reviewer from an unvalidated self-confidence score and accept whichever specialty it predicts.

**Question 12.** The model emits confidence 0.94 for extracted order numbers. Before using that value to skip human review, what is required?

- A) A prompt saying 0.94 means “very certain.”
- B) A higher threshold chosen by intuition.
- C) Agreement between two copies of the same response in one context.
- D) Calibration against labeled outcomes for that field and relevant document types.

**Question 13.** The support MCP server is required for every teammate, but its OAuth client secret differs by environment. Which setup is correct?

- A) Put the server in one operator's `~/.claude.json`, share screenshots, and make each teammate reproduce it on every workstation.
- B) Commit the client secret alongside the server command.
- C) Commit the server definition in project `.mcp.json` and expand the secret from an environment variable.
- D) Describe the server in `CLAUDE.md` without configuring it.

**Question 14.** You resume a week-old customer case. The agreed refund amount and customer authorization remain valid, but order status and payment-provider state may have changed. How should state be restored?

- A) Trust every prior tool result because the session was named.
- B) Preserve durable case facts, refresh volatile backend state, and tell the resumed agent what changed.
- C) Discard the authorization and make the customer repeat identity verification without cause.
- D) Fork the session and assume branching refreshes provider state while preserving every prior operational result.

**Question 15.** A prior session mapped the support architecture, but the tool contracts and routing rules were substantially redesigned before work resumed. What is safest?

- A) Resume and prohibit all tool calls so stale schemas cannot fail.
- B) Fork the old session, compare two branches that share the same stale contracts, and merge whichever branch fails less often.
- C) Reuse old tool outputs because architectural intent is unchanged.
- D) Start a fresh session with a structured summary of durable goals and re-analyze the changed contracts and routes.

---

## Scenario B: Claude Code for CI/CD (Questions 16–30)

Your organization runs Claude Code in pull-request workflows and maintains shared conventions for a large monorepo. The configuration must load at the right time, and refinement must converge on observable criteria.

**Question 16.** All YAML workflow files scattered across the repository must follow a release-security convention, but ordinary code should not load it. What should you create?

- A) A `.claude/rules/` file with a `paths: ["**/.github/workflows/*.yml", "**/.github/workflows/*.yaml"]` scope.
- B) A user-level `CLAUDE.md` on the CI maintainer's workstation, manually replicated in every workflow repository.
- C) A manually invoked skill that developers may forget.
- D) A root instruction that loads the convention for every file.

**Question 17.** Each package needs centrally maintained testing guidance plus its own language-specific conventions. Copying the shared text has caused drift. Which mechanism composes the relevant files without duplication?

- A) Put every standard in every package's `CLAUDE.md`.
- B) Turn standards into MCP tools.
- C) Use `@import` from package `CLAUDE.md` files to include the appropriate shared guidance.
- D) Store the shared standards only in personal memory and ask every CI runner to copy the maintainer's setup.

**Question 18.** A `/release-audit` workflow is shared by the team, runs only on demand, produces verbose exploration, and must not write files. How should it be configured?

- A) As always-loaded root memory with a prose warning not to edit.
- B) As a personal command with unrestricted tools.
- C) As a path rule for every source file.
- D) As a project skill using `context: fork` and read-only `allowed-tools`.

**Question 19.** CI must never read `.env.production`, whether through Read, Grep, or Bash. The forbidden paths are stable and do not require business-state evaluation. What is the strongest primary control?

- A) A sentence in `CLAUDE.md` asking Claude not to inspect secrets.
- B) Settings permission-deny rules covering the relevant tools and paths.
- C) A PostToolUse hook that reports the leak after access.
- D) An inline reminder in each pull request.

**Question 20.** A release command is allowed only when the version matches the signed manifest currently produced by the build. Which mechanism should make the decision at execution time?

- A) A path-scoped formatting rule.
- B) A project slash command with no validation.
- C) A `PreToolUse` hook that compares the command arguments with the signed manifest and blocks mismatches.
- D) A permanent reference to last week's manifest in `CLAUDE.md` that the release team updates manually for every build.

**Question 21.** Review standards, fixture conventions, and required test commands apply to every CI invocation of Claude Code. Where should that recurring context live?

- A) In committed project `CLAUDE.md` guidance available to the CI session.
- B) In a one-time inline prompt maintained separately in each workflow run.
- C) In a developer's user-level command directory.
- D) In the generated review JSON output.

**Question 22.** A generated migration maps blank strings incorrectly. Which prompt addition communicates the desired transformation most effectively?

- A) “Handle blanks correctly in all circumstances.”
- B) Two or three concrete input/output examples covering blank, null, and nonblank values.
- C) A higher output token limit.
- D) A request to use a more sophisticated design pattern and infer blank-value semantics from the surrounding code style.

**Question 23.** A parser fix repeatedly repairs one fixture while breaking another. What workflow best drives convergence?

- A) Ask Claude to remember previous behavior without tests and treat recent conversation history as the permanent regression archive.
- B) Fix the newest failure and delete older fixtures.
- C) Increase temperature between attempts.
- D) Establish a regression suite first, then feed specific failing tests back during iteration.

**Question 24.** A new deployment queue requires decisions about retries, idempotency, ordering, and partial failure, but stakeholders have not specified them. What should happen before implementation?

- A) Use the interview pattern to surface and resolve those design choices.
- B) Start coding the default behavior and document it afterward.
- C) Ask Claude to infer every policy, including retries and idempotency, from analogous code elsewhere in the repository.
- D) Run the formatter to reveal the missing requirements.

**Question 25.** Four review findings all stem from the same incorrect assumption about generated files; two unrelated typos are also present. How should feedback be sequenced?

- A) Put all six in separate sessions so no context is shared, then resolve conflicting patches manually after every session completes.
- B) Put all six in one message because issue relationships never matter.
- C) Ignore the typos until the next release.
- D) Batch the four interacting findings with their shared context, and handle the independent typos separately.

**Question 26.** A CI investigation first needs every file matching `**/*contract-test*.ts`, regardless of content. What tool should locate the candidates?

- A) Grep.
- B) Glob.
- C) Read.
- D) Edit.

**Question 27.** After locating the contract tests, you need to find which ones call `seedRemoteAccount` and understand the surrounding setup. What is the efficient next move?

- A) Read every located test in full before searching.
- B) Glob repeatedly using the function name as a filename until path patterns appear to cover every helper call.
- C) Grep the candidates for the symbol, then Read only the matching files and relevant helpers.
- D) Replace the helper and see which tests fail.

**Question 28.** A review bot flags harmless log statements because its only example shows a real credential leak. How should few-shot prompting reduce these false positives?

- A) Remove examples and ask for high confidence.
- B) Add many copies of the same credential-leak example, varying their wording and order so the set appears diverse.
- C) Require every log statement to be reported.
- D) Add varied positive and negative boundary examples showing sensitive values versus safe identifiers.

**Question 29.** Pull-request descriptions use dates, severity labels, and file paths in inconsistent formats, but the review schema expects normalized values. What should be added?

- A) Explicit normalization rules and examples for the accepted canonical forms.
- B) More required fields without formatting guidance.
- C) A random retry whenever formatting differs.
- D) A prose-only output that downstream code normalizes by guessing and repairs after review comments have already been posted.

**Question 30.** The review tool always emits schema-valid objects, but it sometimes labels test-only failures as production blockers. What additional control is needed?

- A) Remove the schema so the model can explain itself.
- B) Force the same tool a second time.
- C) Semantic criteria and validation that distinguish severity using observable impact.
- D) A larger context window with no new examples or criteria.

---

## Scenario C: Multi-Agent Research System (Questions 31–45)

Your coordinator produces technical due-diligence reports using web, document, data, and synthesis specialists connected to several MCP servers.

**Question 31.** A routine request asks for one documented API limit, while a strategic report needs market, security, cost, and implementation analysis. How should orchestration differ?

- A) Both should invoke every specialist so reports are consistent.
- B) Both should use a fixed one-agent workflow.
- C) The coordinator should choose the minimum suitable path for the factual query and dynamically assemble broader specialists for the strategic report.
- D) Escalate the factual query and reserve multi-agent work for requests that contain several explicit user questions before tool selection begins.

**Question 32.** A global infrastructure study has repeatedly omitted smaller regions. What decomposition best protects coverage?

- A) Partition by complementary regions and evidence types, assign explicit coverage goals, and check the combined result for gaps.
- B) Ask every agent to research the entire world independently.
- C) Decompose only by the largest vendors because they have the most sources and assume their coverage represents smaller regions.
- D) Make the final report longer without changing assignments.

**Question 33.** A review of 80 modules requires the same security and performance checks on each, plus one architecture-wide dependency pass. Which pattern is most appropriate?

- A) One open-ended agent that reads all modules simultaneously while relying on a larger context window to preserve equal attention.
- B) Fixed focused module passes followed by a separate cross-module integration review.
- C) Dynamic task generation with no stable checklist.
- D) Independent local passes with no final synthesis.

**Question 34.** Synthesis reveals that all cost estimates assume one deployment model, but a newly discovered regulatory rule requires a second model in two regions. What should the coordinator do?

- A) Preserve the original tasks unchanged for reproducibility.
- B) Delete all completed research and restart globally.
- C) Ask synthesis to estimate the second model without source work and mark the resulting regional costs as provisional.
- D) Generate targeted regional and cost subtasks, then update affected synthesis while retaining unaffected findings.

**Question 35.** The whole team needs a stable internal-document MCP server after cloning the repository. Where should it be defined?

- A) In each person's `~/.claude.json` with manually copied settings.
- B) In committed project `.mcp.json`.
- C) In the coordinator's natural-language prompt.
- D) In a user-level slash command.

**Question 36.** The shared server requires a different token for each environment. How should authentication be represented in the committed definition?

- A) As an encrypted-looking literal token in `.mcp.json`.
- B) As a token pasted into `CLAUDE.md` at session start.
- C) As a value returned by an unrestricted MCP tool.
- D) As environment-variable expansion resolved outside version control.

**Question 37.** The research application connects to document, statistics, and news MCP servers. What happens during connection?

- A) Tools from all configured servers can be discovered and exposed together to the agent.
- B) Only tools from the alphabetically first server are available.
- C) Project scope disables every user-scoped server.
- D) The coordinator must reconnect each time it changes specialists and cache that connection only for the current specialist turn.

**Question 38.** Agents waste calls asking which datasets, reports, and schemas exist. What should the servers expose?

- A) A generic tool that guesses a dataset name.
- B) Larger error messages listing every asset after a failed call.
- C) MCP resources that catalog the available content and structures.
- D) A PostToolUse hook that repeats every search.

**Question 39.** `query_metrics` and `search_reports` both accept text, and the model uses them interchangeably. Which description change matters most?

- A) Describe their implementation languages and deployment regions.
- B) Shorten both descriptions so the model reads them faster and rely on names and server placement to imply the difference.
- C) Give both the same examples to emphasize consistency.
- D) State the distinct data sources, query formats, output shapes, boundaries, and example questions for each.

**Question 40.** A source-selection prompt says, “Whenever the user says current, always use web search,” causing live database metrics to be ignored. What is the best diagnosis?

- A) The system prompt creates an overly broad keyword association that should be revised alongside the tool contracts.
- B) The database tool needs longer JSON property names and aliases ordered by data recency so the model notices it first.
- C) MCP discovery cannot expose database and web tools together.
- D) The model requires a random selection policy.

**Question 41.** A generic `process_source(mode=search|extract|verify)` tool frequently receives the wrong mode. What interface change gives the model clearer decisions?

- A) Add more modes to cover edge cases.
- B) Hide the mode field, ask downstream code to infer it from the original prompt, and preserve one generic permission boundary.
- C) Split it into purpose-specific tools with separate schemas and permissions.
- D) Force the generic tool on every turn.

**Question 42.** A statistics provider returns HTTP 503. What metadata most directly tells the agent whether another attempt is sensible?

- A) The provider's full HTML error page, requiring the agent to parse retry instructions from untrusted markup.
- B) A transient error category, `isRetryable: true`, attempted operation, and suggested backoff.
- C) A successful empty dataset.
- D) A non-retryable business-rule category.

**Question 43.** A well-formed query legitimately finds no studies in the requested date range. How should that differ from access denial?

- A) Return a successful empty result for no matches; return a typed permission error for denied access.
- B) Return the same generic error for both and ask the coordinator to distinguish it from ordinary conversational text.
- C) Mark both as retryable because neither returned data.
- D) Represent both as successful prose messages.

**Question 44.** A named session has an accurate source taxonomy, and only two ingestion adapters changed. You want to continue the investigation. What should you do?

- A) Start blank, discard the source taxonomy, and rebuild it from public documentation before inspecting the changed adapters.
- B) Resume without mentioning the adapters.
- C) Fork solely to refresh filesystem state.
- D) Resume the named session, identify the changed adapters, and request targeted re-analysis.

**Question 45.** Two teams want to compare incompatible synthesis architectures from the same accepted evidence map. Which session mechanism preserves the shared baseline and isolates later reasoning?

- A) Run both architectures sequentially in the same conversation.
- B) Fork the session into independent branches.
- C) Resume the same named session twice and allow concurrent edits.
- D) Start two blank sessions with no evidence map.

---

## Scenario D: Structured Data Extraction (Questions 46–60)

Your extraction platform handles procurement documents from many regions and vendors. It already uses tool schemas, but accuracy and reviewer efficiency vary across formats.

**Question 46.** Purchase-order numbers appear in page headers, table captions, and barcode-adjacent labels. The extractor handles only headers. What should you add first?

- A) Few-shot examples demonstrating the same field correctly extracted from each representative placement.
- B) A requirement that every order number appear in the header, rejecting valid orders that use another source layout.
- C) A retry that repeats the unchanged prompt.
- D) A free-form answer instead of the existing schema.

**Question 47.** Some source documents genuinely omit shipping terms. The current required string causes plausible invented terms. Which schema behavior is appropriate?

- A) Substitute the most common term for that vendor.
- B) Reject every document with no term.
- C) Keep the field required, ask the model to be honest, and make runtime validation responsible for detecting invention.
- D) Allow null or omission and state that missing source information must not be invented.

**Question 48.** A contract-type enum does not include a newly encountered but valid category, and some scans are too degraded to classify at all. How should both cases be represented?

- A) Map both to the nearest known enum value even when the source distinguishes a novel category from unreadable evidence.
- B) Remove the enum and accept arbitrary prose.
- C) Use `other` plus a detail for the valid novel category, and `unclear` for genuinely ambiguous evidence.
- D) Reject both documents.

**Question 49.** Validation says `subtotal + tax != total`. What should the self-correction request contain?

- A) Only the desired total value.
- B) The source, failed extraction, and exact arithmetic validation error.
- C) A new schema with all fields optional.
- D) A demand to return different numbers without evidence and accept any values that happen to satisfy the schema.

**Question 50.** A requested signature is absent because the scan ends before the signature page. Which response is correct?

- A) Keep retrying with varied temperature and wording until the model supplies a signature-like value.
- B) Infer the signer from the contract owner.
- C) Stop extraction retries and route to rescanning, review, or a documented missing value.
- D) Use a fabricated “signature present” default.

**Question 51.** Monetary values arrive as `$1,200.50`, `1.200,50 €`, and `1200.5 USD`. What should accompany the structured schema?

- A) Explicit currency and numeric normalization rules with examples and ambiguity handling.
- B) A rule to discard currency information.
- C) Higher temperature to encourage format creativity.
- D) A random retry after every non-US format, treating the first US-style parse as the canonical baseline.

**Question 52.** Documents arrive with unknown type, and one of several extraction tools must be called so downstream processing never receives conversational prose. Which configuration is most reliable?

- A) `tool_choice: "auto"` and a request to prefer tools.
- B) Prefill an opening JSON brace in a text response, then parse and repair whichever document-specific fields follow in downstream code.
- C) Force the invoice tool regardless of document type.
- D) Use structured extraction tools and `tool_choice: "any"` so a tool call is guaranteed while Claude selects the matching schema.

**Question 53.** The model flags every handwritten annotation as a fraud indicator, though most are harmless initials. Which few-shot set best sharpens the decision boundary?

- A) Ten examples of confirmed fraud annotations only.
- B) Representative positive examples plus near-miss negative examples such as harmless initials and reviewer notes.
- C) Use no examples, request conservative scoring, and discard every prediction that falls below a high intuitive confidence threshold.
- D) One example with no explanation of the label.

**Question 54.** Bank-account fields are high risk, while optional marketing codes are low risk. Both have confidence 0.82. What should routing do?

- A) Apply field-specific risk and ambiguity thresholds, sending the bank field to review while allowing policy-defined handling for the low-risk code.
- B) Treat equal confidence as equal operational risk, apply the same review threshold, and ignore field consequence, source ambiguity, or reviewer expertise during downstream decisions.
- C) Average both fields into one document confidence.
- D) Randomly choose one field for review.

**Question 55.** Confidence thresholds were calibrated before adding new languages and a substantially revised prompt. What should happen before continued auto-acceptance?

- A) Keep the thresholds because the output schema did not change and assume field-level accuracy remains stable across languages.
- B) Lower every threshold by the same amount.
- C) Recalibrate on labeled data representing the new languages, prompt, fields, and document segments.
- D) Ask the model whether its confidence remains accurate.

**Question 56.** What monitoring practice can reveal a new high-confidence error pattern after automation?

- A) Review only cases already rejected by validation.
- B) Human-review a stratified sample of auto-accepted extractions and track error types over time.
- C) Compare confidence scores without examining ground truth.
- D) Rerun successful documents with the identical prompt, assume agreement means correctness, and use repeated agreement as the monitoring metric.

**Question 57.** A single extraction change causes amount parsing, tax calculation, and currency labeling failures because all three share one normalization rule. How should refinement feedback be presented?

- A) Correct each symptom in isolated sessions without mentioning the shared rule, then reconcile inconsistent patches after all changes merge.
- B) Fix only the first failing field and hope the others follow.
- C) Add every failure permanently to `CLAUDE.md`.
- D) Batch the interacting failures with the shared normalization context so one coherent fix can be evaluated.

**Question 58.** The extractor mishandles a nested table only when a row contains both a null quantity and a discount. What feedback most directly guides correction?

- A) “Improve table support.”
- B) A longer system prompt describing common table shapes generally while omitting the actual failing input and expected output.
- C) The exact source fragment, failed output, expected output, and a regression case for that edge condition.
- D) A higher maximum token count.

**Question 59.** A personal prototype extraction server and a shared production server are both needed on one developer's machine. What setup preserves the intended scopes?

- A) Keep production in project `.mcp.json` with environment-based credentials and the prototype in user `~/.claude.json`; both can be discovered together.
- B) Put both in project `.mcp.json`, ask teammates to ignore the prototype, and require each person to edit the file locally before use.
- C) Put both in user scope so no configuration is committed.
- D) Describe one server in `CLAUDE.md` instead of configuring it.

**Question 60.** You need to determine which parsers handle `.xlsx` files and then understand only their normalization paths. What is the best context-conscious exploration sequence?

- A) Read every parser and dependency before searching.
- B) Glob for likely parser files, Grep for `.xlsx` handlers, then Read the matching code and relevant imports.
- C) Grep generated output only and use recurring examples as a proxy for the current source implementation and normalization path.
- D) Edit the first parser whose filename contains `excel`.

---

# Answer Key — Practice Exam 14

**Quick key:** 1-B, 2-D, 3-A, 4-C, 5-D, 6-B, 7-C, 8-A, 9-B, 10-C, 11-A, 12-D, 13-C, 14-B, 15-D, 16-A, 17-C, 18-D, 19-B, 20-C, 21-A, 22-B, 23-D, 24-A, 25-D, 26-B, 27-C, 28-D, 29-A, 30-C, 31-C, 32-A, 33-B, 34-D, 35-B, 36-D, 37-A, 38-C, 39-D, 40-A, 41-C, 42-B, 43-A, 44-D, 45-B, 46-A, 47-D, 48-C, 49-B, 50-C, 51-A, 52-D, 53-B, 54-A, 55-C, 56-B, 57-D, 58-C, 59-A, 60-B

**Focus key:** 1-DEC, 2-DEC, 3-DEC, 4-DEC, 5-ERR, 6-ERR, 7-ERR, 8-DESC, 9-DESC, 10-REV, 11-REV, 12-REV, 13-MCP, 14-RES, 15-RES, 16-CFG, 17-CFG, 18-CFG, 19-CFG, 20-CFG, 21-CFG, 22-REF, 23-REF, 24-REF, 25-REF, 26-EXP, 27-EXP, 28-EXT, 29-EXT, 30-EXT, 31-DEC, 32-DEC, 33-DEC, 34-DEC, 35-MCP, 36-MCP, 37-MCP, 38-MCP, 39-DESC, 40-DESC, 41-DESC, 42-ERR, 43-ERR, 44-RES, 45-RES, 46-EXT, 47-EXT, 48-EXT, 49-EXT, 50-EXT, 51-EXT, 52-EXT, 53-EXT, 54-REV, 55-REV, 56-REV, 57-REF, 58-REF, 59-MCP, 60-EXP

Focus codes: CFG = Claude Code configuration selection; MCP = MCP scope and integration; DEC = adaptive decomposition; EXT = extraction accuracy; REF = iterative refinement; EXP = codebase exploration; DESC = tool descriptions; RES = session resumption; REV = human-review routing; ERR = MCP error handling.

---

**1. B** — Independent concerns can be investigated in parallel after their shared prerequisite, while coordinator synthesis preserves one coherent customer resolution. Serializing or escalating by default wastes capability; direct specialist replies fragment the case.

**2. D** — Predictable address changes suit a fixed prerequisite chain, whereas takeover investigations must branch as evidence changes. Using one decomposition style for both ignores the difference between known stages and open-ended discovery.

**3. A** — Adaptive orchestration incorporates the new identity evidence by adding focused work and updating only dependent tasks. Blindly completing the original plan or discarding verified evidence is not responsive decomposition.

**4. C** — An unknown systemic cause requires mapping and measurement before subtasks can target observed contributors. Immediate optimization and individual-case checklists assume the answer before gathering evidence.

**5. D** — The identifier is invalid input, so the tool should state a validation category, explain the accepted format, and avoid retry until the input changes. Empty success and unrelated error categories lead to incorrect recovery.

**6. B** — A safe transient retry belongs near the failure in the specialist, protecting coordinator context from routine recovery. Escalation and cross-specialist retries add cost without improving the first recovery path.

**7. C** — Structured partial results and failure metadata let the coordinator preserve completed checks and decide between retry, escalation, or an alternative. Generic text, false success, and raw logs remove operational meaning.

**8. A** — Distinct purposes, identifiers, outputs, examples, and boundaries give the model the selection evidence it lacks. Forced dual calls, extra tools, and keyword routing do not clarify the interface.

**9. B** — Purpose-specific tools make destructive intent explicit and allow separate permissions and contracts. More modes retain the ambiguous high-risk interface, while prompt warnings remain probabilistic.

**10. C** — Review should follow field-level uncertainty and consequence, so the ambiguous amount receives human attention without discarding clear data. Averages and random sampling are not sufficient for a known high-risk ambiguity.

**11. A** — Document and field characteristics determine the expertise needed for efficient, accurate review. Random or aggregate-only routing ignores the type of judgment required.

**12. D** — A confidence value has no operational meaning until labeled outcomes establish its calibration for the relevant field and sources. Wording, intuition, and same-context agreement do not measure accuracy.

**13. C** — Shared tooling belongs in project `.mcp.json`, while environment expansion keeps environment-specific secrets out of version control. User scope and documentation alone do not distribute a usable server.

**14. B** — Durable agreements can remain in the resumed context, but volatile order and provider state must be refreshed, with changes made explicit. Naming or forking a session does not update external systems.

**15. D** — Redesigned contracts make old operational context unsafe; a fresh session seeded with durable goals and targeted re-analysis avoids stale tool assumptions. Resuming or forking preserves the stale interface evidence.

**16. A** — Glob-scoped rules apply automatically to workflow files wherever they live without taxing ordinary code sessions. User memory is not shared, skills are opt-in, and root guidance loads too broadly.

**17. C** — `@import` composes maintained standards into the packages that need them without copying. MCP tools and user memory do not replace repository instruction composition.

**18. D** — A team-shared, on-demand workflow is a project skill; `context: fork` isolates verbose output, and `allowed-tools` structurally enforces read-only access. Always-loaded or personal mechanisms miss one or more requirements.

**19. B** — Stable access prohibitions belong in settings permissions that cover every relevant tool and path. A PostToolUse hook reacts too late, and prompt reminders are not deterministic controls.

**20. C** — This decision depends on current tool arguments and a live signed artifact, making `PreToolUse` the correct dynamic enforcement point. Static guidance or last week's state cannot prove the current version.

**21. A** — Recurring shared CI context belongs in committed project memory available to every invocation. Inline duplication drifts, user commands are personal, and output cannot configure the request that produced it.

**22. B** — Concrete examples show exactly how blank, null, and ordinary inputs must transform. Vague wording and more tokens do not define the disputed boundary.

**23. D** — A regression suite preserves working cases, while specific failures drive each correction toward convergence. Deleting fixtures or varying temperature hides regressions rather than resolving them.

**24. A** — The interview pattern surfaces unresolved product and reliability decisions before implementation. Code and formatting cannot decide stakeholder policy implicitly.

**25. D** — Interacting findings should be evaluated together with their common assumption, while independent typos can be handled separately. Universal batching or universal isolation ignores dependency structure.

**26. B** — Glob finds candidate paths from filename patterns. Grep searches content, while Read and Edit are later operations.

**27. C** — Grep narrows the candidates by symbol usage, and targeted Read supplies only the relevant setup and helpers. Exhaustive reading consumes context before the discriminating search.

**28. D** — Positive and near-miss negative examples teach the review boundary between real secret exposure and harmless identifiers. Repetition of one positive case cannot reduce the observed false-positive class.

**29. A** — Schemas define shape, while normalization rules and examples define canonical values across inconsistent source formats. More required fields and unguided retries do not establish formatting semantics.

**30. C** — Structural validity does not decide severity; observable semantic criteria and validation must map impact to the correct label. Repeating the same tool or expanding context without criteria preserves the error.

**31. C** — Delegation should scale with task complexity and evidence needs: a direct authoritative lookup does not need a full research organization, while strategy work does. Always invoking all agents wastes cost and context.

**32. A** — Complementary partitioning plus explicit coverage checks prevents small regions from disappearing. Duplicated whole-world assignments increase overlap, and longer synthesis cannot recover unassigned scope.

**33. B** — Known repeated checks suit focused fixed passes, with a separate architecture review for interactions. One huge prompt dilutes attention, while local-only review misses cross-module behavior.

**34. D** — The new rule changes only part of the research, so targeted adaptive subtasks should refresh affected regions and estimates while preserving valid work. Blind completion, invention, and global restart are weaker.

**35. B** — A required team server belongs in committed project `.mcp.json`. User configuration is personal, and prompts or commands do not establish MCP connections.

**36. D** — Environment expansion lets one committed definition resolve credentials securely per environment. Literals, memory, and unrestricted credential-returning tools expose secrets.

**37. A** — MCP clients discover configured servers' tools at connection time and can expose them simultaneously. No alphabetical, scope-exclusive, or per-specialist reconnection rule applies.

**38. C** — Resources provide stable catalogs and schemas without exploratory action calls. Guessing tools and failure messages make discovery indirect and wasteful.

**39. D** — The model needs source, query, output, and boundary distinctions plus examples to select reliably. Implementation trivia, shorter ambiguity, and identical examples do not differentiate the tools.

**40. A** — The prompt's unconditional “current” keyword rule is overriding a valid tool distinction and should be narrowed. Server discovery and property naming do not explain the systematic bias.

**41. C** — Purpose-specific names and schemas remove mode ambiguity and permit least-privilege permissions. Adding or hiding modes keeps the core selection risk.

**42. B** — A 503 is normally transient; explicit category, retryability, operation, and backoff tell the agent how to recover. Empty success and business-error labeling misrepresent the failure.

**43. A** — Successful absence is valid data, while access denial is an operational permission error with a different recovery path. Treating them identically causes false conclusions or wasted retries.

**44. D** — Most context remains valid, so named resumption plus explicit changed-adapter re-analysis preserves work without trusting stale files. Forking is not a refresh mechanism.

**45. B** — Forking creates independent branches from one accepted baseline, exactly matching the comparison need. Sequential work cross-contaminates reasoning, and blank sessions lose evidence.

**46. A** — Representative examples teach the same field across multiple visual locations and generalize beyond one header layout. Requiring a nonexistent convention or repeating the same prompt does not add evidence.

**47. D** — Nullable or optional representation accurately preserves genuine absence and removes pressure to fabricate. Defaults, rejection, and prose warnings retain or worsen the required-field problem.

**48. C** — `other` with detail preserves a valid unforeseen category, while `unclear` preserves ambiguity. Conflating either with the nearest known class fabricates certainty.

**49. B** — Semantic correction requires the source, failed candidate, and exact arithmetic discrepancy. Supplying an answer without evidence encourages a schema-valid but unsupported value.

**50. C** — Missing source content cannot be recovered by model retry; the pipeline must choose rescanning, review, or an explicit missing value. Inference and defaults fabricate evidence.

**51. A** — Canonical numeric and currency rules plus examples define how each source form maps downstream and what to do when ambiguous. Temperature and retries do not define locale semantics.

**52. D** — Tool schemas enforce structure, and `tool_choice: "any"` guarantees some extraction tool while leaving schema selection to Claude. Auto permits prose, while forcing one document type can select the wrong schema.

**53. B** — Positive and close negative examples sharpen the classification boundary that the extractor currently lacks. Positive-only repetition explains fraud but not why harmless initials are different.

**54. A** — Equal model confidence does not imply equal operational risk; field-specific consequence and ambiguity should determine routing. Whole-document averages and random choice hide the dangerous field.

**55. C** — Prompt and language changes alter the score-to-accuracy relationship, so thresholds require new labeled calibration across the changed distribution. Schema stability does not preserve calibration.

**56. B** — Stratified human sampling of auto-accepted data supplies ground truth for unknown high-confidence failures and drift. Confidence agreement without labels cannot prove correctness.

**57. D** — One shared normalization defect requires one consolidated evaluation of its interacting symptoms. Isolated fixes can conflict or repeatedly patch the same cause.

**58. C** — The exact failing evidence, observed output, expected output, and regression case give a testable correction target. General wording and more tokens do not identify the compound edge condition.

**59. A** — Production remains shared through project scope and environment credentials, while the prototype remains personal; MCP discovery can expose both on that developer's machine. Putting either in the wrong scope violates the intended audience.

**60. B** — Path matching narrows likely parsers, content search identifies actual `.xlsx` handling, and targeted Read follows only relevant normalization code. Exhaustive reading and filename guessing waste context or risk premature edits.

*End of Practice Exam 14.*
