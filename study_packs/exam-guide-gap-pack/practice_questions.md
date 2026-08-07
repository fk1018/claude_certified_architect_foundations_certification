# Exam Guide Gap Pack Practice Questions

Supplemental drills targeting the task statements that had no coverage across the course study packs (see `fable_review_0.md`). These are not a full 60-question exam — pair them with `practice_exams/`. Options are deliberately length-balanced; reasoning lives in the explanations, not the options.

## Question 1

Scenario: Your multi-agent research coordinator has two subagents defined via AgentDefinition (web search, document analysis). In production the coordinator always answers directly and never delegates, even for queries that clearly need research.

Question: What is the most likely cause?

A. The coordinator's allowedTools does not include "Task".

B. The subagents are not registered in the project's .mcp.json.

C. The subagents' system prompts lack delegation instructions.

D. The coordinator's max_tokens is too low to emit Task calls.

Correct answer: A

Explanation: The Task tool is the mechanism for spawning subagents; if `"Task"` is missing from the coordinator's allowedTools, it cannot delegate no matter how good the AgentDefinitions are. Check configuration before prompts.

Distractors:

- B: Subagents are defined via AgentDefinition, not MCP server entries — plausible-sounding but not a real registration mechanism.
- C: Delegation is the coordinator's decision; subagent system prompts don't enable or disable it.
- D: max_tokens limits response length; it doesn't prevent tool calls from being emitted.

## Question 2

Scenario: Your coordinator runs web search and document analysis subagents successfully, then spawns a synthesis subagent. The synthesis output is coherent but generic — it contains none of the findings the other agents collected.

Question: What is the correct fix?

A. Re-run the synthesis subagent with a stronger system prompt about thoroughness.

B. Enable context inheritance on the Task call so the subagent sees the coordinator's history.

C. Include the search and analysis findings directly in the synthesis subagent's prompt.

D. Have the search subagents write their findings to shared conversation memory.

Correct answer: C

Explanation: Subagents run with isolated context — they do not inherit the coordinator's conversation history or share memory between invocations. Everything the synthesis agent needs must be passed explicitly in its prompt.

Distractors:

- A: The problem is missing inputs, not effort; no prompt strength recovers findings the agent never received.
- B: No such inheritance switch exists — isolation is how subagents work.
- D: There is no shared memory between subagent invocations.

## Question 3

Scenario: Your coordinator researches four independent subtopics one at a time, making total latency roughly four times a single investigation.

Question: How do you run the subtopics concurrently?

A. Submit the four subtopic requests through the Message Batches API.

B. Emit all four Task tool calls in a single coordinator response.

C. Set parallel: true on each Task call so the SDK fans them out.

D. Spawn one subagent per turn but shrink each subagent's tool set.

Correct answer: B

Explanation: Parallel subagent execution is achieved by emitting multiple Task tool calls in one coordinator response; calls spread across separate turns run sequentially.

Distractors:

- A: The Batches API is for latency-tolerant bulk requests and doesn't support the multi-turn tool loop subagents need.
- C: No such flag exists on the Task tool.
- D: Fewer tools doesn't change sequential turn-by-turn spawning.

## Question 4

Scenario: A report on "the impact of AI on healthcare" covers only diagnostic imaging. The coordinator's logs show it decomposed the topic into three imaging-related subtasks, and every subagent completed its assignment correctly.

Question: What change most directly prevents this failure?

A. Expand the web search subagent's queries to cover more of the healthcare sector.

B. Instruct the synthesis agent to flag missing subject areas in the final report.

C. Add more search subagents so each assigned subtask collects more sources.

D. Prompt the coordinator to enumerate the topic's major subdomains before assigning tasks.

Correct answer: D

Explanation: The root cause is the coordinator's overly narrow decomposition — subagents faithfully covered what they were given. Fixing decomposition breadth at the coordinator addresses the failure at its source.

Distractors:

- A: The search agent only searches what it's assigned; broader queries within a narrow assignment don't restore missing subdomains.
- B: A gap flag downstream is a detector, not a fix, and the synthesis agent only sees what upstream agents collected.
- C: More agents on the same narrow subtasks produce deeper coverage of the same slice.

## Question 5

Scenario: In your research pipeline, the search subagent passes results directly to the analysis subagent, which passes directly to synthesis. Failures are hard to trace, and each handoff handles errors differently.

Question: What architectural change fixes this?

A. Route all subagent inputs and outputs through the coordinator.

B. Standardize one error format that subagents use with each other.

C. Add logging middleware between each pair of communicating agents.

D. Merge search and analysis into one subagent to remove a handoff.

Correct answer: A

Explanation: Hub-and-spoke — the coordinator mediating all inter-subagent communication — provides observability, consistent error handling, and controlled information flow. Direct subagent-to-subagent handoffs are the anti-pattern.

Distractors:

- B: A shared format helps but leaves routing, recovery, and visibility fragmented across hops.
- C: Logging observes the problem without giving any component authority to handle it consistently.
- D: Merging trades the handoff problem for an overloaded agent and doesn't scale past two agents.

## Question 6

Scenario: An agent has spent an hour building a thorough analysis of your codebase. The team now wants to evaluate two competing testing strategies — mock-heavy versus integration-first — each developed from that same analysis.

Question: What is the most efficient approach?

A. Explore both strategies sequentially in one session, running /compact in between.

B. Start two fresh sessions, each instructed to re-analyze the codebase first.

C. Use fork_session to branch two independent explorations from the shared analysis.

D. Resume the session in two terminals with --resume so each continues separately.

Correct answer: C

Explanation: fork_session creates independent branches from a shared baseline, letting each strategy develop in isolation without repeating the expensive analysis and without the two explorations contaminating each other.

Distractors:

- A: Sequential exploration in one session lets the first strategy's conclusions bias the second, and /compact doesn't isolate them.
- B: Re-analyzing twice discards an hour of shared work.
- D: Resuming the same session twice doesn't create independent branches.

## Question 7

Scenario: You have a named investigation session from last week. Since then, a large refactor changed most of the modules that session had analyzed.

Question: How should you continue the investigation?

A. Resume the named session and continue where the investigation stopped.

B. Start a new session seeded with a structured summary of the prior findings.

C. Resume the session and instruct the agent to distrust its earlier conclusions.

D. Fork the old session so the stale context stays isolated from the new work.

Correct answer: B

Explanation: When prior tool results are stale, a fresh session with an injected structured summary is more reliable than resuming — the old session's file reads and analysis no longer describe the codebase.

Distractors:

- A: Resuming keeps stale tool results in context, and the agent will reason from them.
- C: A distrust instruction is probabilistic; the stale data is still there competing with reality.
- D: Forking copies the same stale baseline into the new branch.

## Question 8

Scenario: Delivered research reports repeatedly turn out to have coverage gaps that readers discover after the fact.

Question: What process change catches the gaps before delivery?

A. Increase the number of parallel search subagents from three to eight.

B. Lower the relevance threshold so more sources reach the synthesis stage.

C. Instruct the synthesis agent to fill thin sections from model knowledge.

D. Have the coordinator evaluate the synthesis for gaps and re-delegate targeted queries.

Correct answer: D

Explanation: This is the iterative refinement loop: the coordinator inspects synthesis output for coverage gaps, re-delegates targeted queries to search/analysis subagents, and re-invokes synthesis until coverage is sufficient.

Distractors:

- A: More initial searchers widen the first pass but nothing verifies coverage afterward.
- B: A looser threshold adds noise without checking whether topic areas are missing.
- C: Padding from model knowledge fabricates unsourced content — the opposite of research quality.

## Question 9

Scenario: Every failure from process_refund returns the string "Operation failed". The agent retries policy-violation failures that can never succeed and gives up immediately on gateway timeouts that would succeed on retry.

Question: What should the tool return instead?

A. Nothing — add an application-layer policy that retries every failed call three times.

B. The failure modes documented in the system prompt so the agent can infer causes.

C. An errorCategory, an isRetryable flag, and a readable description with each failure.

D. A separate tool per failure type so each error maps to a distinct tool result.

Correct answer: C

Explanation: Structured error metadata (transient/validation/permission/business category, isRetryable boolean, human-readable description) lets the agent retry what's retryable and stop on what isn't. Uniform errors force it to guess.

Distractors:

- A: Blanket retries hammer permanent failures and still mishandle the transient ones after three attempts.
- B: Prompt documentation can't tell the agent which category a specific runtime failure belongs to.
- D: Tool-per-error explodes the tool count and degrades tool selection without adding recovery information.

## Question 10

Scenario: Your team shares a Jira MCP server that requires an API token, and one developer wants to trial an experimental prototype server without affecting anyone else.

Question: How should these be configured?

A. Jira in project .mcp.json using ${JIRA_TOKEN} expansion; the prototype in that developer's ~/.claude.json.

B. Both in project .mcp.json, with the prototype entry commented out for other developers.

C. Both in each developer's ~/.claude.json so the API token never enters the repository.

D. Jira referenced from the project CLAUDE.md; the prototype installed via a custom slash command.

Correct answer: A

Explanation: Project-scoped .mcp.json is version-controlled team tooling, with environment-variable expansion keeping the token out of the repo; user-scoped ~/.claude.json is exactly for personal/experimental servers.

Distractors:

- B: Committing a commented-out experimental server pollutes shared config and invites accidental enablement.
- C: User-scoping the team server means every developer maintains their own copy and drift follows; ${ENV_VAR} already solves the secret problem.
- D: CLAUDE.md holds instructions, not server configuration, and slash commands don't install MCP servers.

## Question 11

Scenario: Your monorepo has SQL migration conventions, and migration files live in per-service directories scattered across the whole repository.

Question: What is the most maintainable way to apply the conventions automatically?

A. Place a CLAUDE.md in each service directory that contains migration files.

B. Create a .claude/rules/ file with paths: ["**/migrations/*.sql"] frontmatter.

C. Add a migrations section to the root CLAUDE.md and rely on Claude to infer scope.

D. Create a migrations skill that developers invoke before editing migration files.

Correct answer: B

Explanation: Path-scoped rules with glob frontmatter load exactly when a matching file is edited, regardless of directory — the right tool for conventions that span scattered locations.

Distractors:

- A: One CLAUDE.md per service duplicates content and has to be maintained in every new service.
- C: Root-file inference is unreliable and loads the content in every session whether relevant or not.
- D: Skills are on-demand; developers will forget to invoke them, so application isn't automatic.

## Question 12

Scenario: A dependency-audit skill outputs thousands of lines of package analysis. After developers run it, the rest of their session becomes noticeably degraded.

Question: What is the right fix?

A. Add argument-hint frontmatter so developers scope each audit to one package.

B. Tell users to run /compact immediately after each audit completes.

C. Move the audit checklist from the skill into the root CLAUDE.md file.

D. Add context: fork to the skill's frontmatter so it runs in an isolated context.

Correct answer: D

Explanation: context: fork runs the skill in an isolated sub-agent context, so its verbose output never enters the main conversation — the designed mechanism for exactly this problem.

Distractors:

- A: Scoping shrinks the output but still deposits it in the main context every run.
- B: /compact after the fact compresses the damage instead of preventing it, and relies on users remembering.
- C: CLAUDE.md placement makes the content always-loaded — strictly worse for context.

## Question 13

Scenario: A nightly pipeline runs Claude Code reviews and parses the output with regex to create tickets. Every few weeks phrasing shifts and the parser breaks.

Question: What is the robust approach?

A. Run claude -p with --output-format json and --json-schema for the findings format.

B. Add an output template to CLAUDE.md and tighten the regex to match that template.

C. Pipe the review output through a second claude call that reformats it as JSON.

D. Move the pipeline to the Message Batches API, which returns structured results.

Correct answer: A

Explanation: The documented CI pattern: -p for non-interactive mode, --output-format json plus --json-schema to enforce machine-parseable, schema-compliant output. No prose parsing, no drift.

Distractors:

- B: Prompted templates are probabilistic; the regex will break again.
- C: A reformatting hop adds cost and can itself vary; nothing enforces the schema.
- D: Batches changes the delivery model, not the output structure, and adds up-to-24h latency to a nightly job.

## Question 14

Scenario: Client contracts guarantee extraction results within 30 hours of document receipt. You accumulate incoming documents and submit them to the Message Batches API, which takes up to 24 hours per batch.

Question: Which submission schedule meets the SLA?

A. Every 12 hours

B. Every 4 hours

C. Every 8 hours

D. Once per day

Correct answer: B

Explanation: Worst case = submission interval + 24h processing. A document arriving just after a submission waits the full interval, then up to 24h: 4 + 24 = 28 ≤ 30 meets the SLA; 8 + 24 = 32, 12 + 24 = 36, and 24 + 24 = 48 all breach it.

Distractors:

- A: 36-hour worst case breaches by 6 hours.
- C: 32-hour worst case breaches by 2 hours.
- D: 48-hour worst case breaches by 18 hours.

## Question 15

Scenario: You run two Claude workloads: a customer-facing chat assistant that needs sub-minute responses, and a weekly compliance audit of 5,000 contracts whose results are reviewed the next morning. Your manager proposes moving both to the Message Batches API for the 50% savings.

Question: How should you respond?

A. Move both to batches, polling frequently so chat responses come back quickly.

B. Keep both synchronous; correlating batch results by custom_id adds complexity.

C. Batch the weekly audit; keep the chat assistant on the synchronous API.

D. Batch both, with a synchronous fallback whenever a batch runs past an hour.

Correct answer: C

Explanation: Batch processing fits latency-tolerant, non-blocking work (the overnight audit) and is wrong for anything a user waits on — there is no latency SLA, and batches can take up to 24 hours. Match each workload to its latency requirement.

Distractors:

- A: Polling doesn't make a no-SLA API fast; chat users can't wait hours.
- B: custom_id correlation is trivial and forfeits a legitimate 50% saving on the audit.
- D: A fallback re-runs work at full price and still delays users up to the timeout.

## Question 16

Scenario: Your extraction pipeline retries failed validations with the error messages appended. The policy_effective_date field still fails after four retries. Investigation shows the date appears only in a separate rider document that is never sent to the model.

Question: What should you do?

A. Increase the retry limit to eight and vary temperature across attempts.

B. Make policy_effective_date required so the model prioritizes finding it.

C. Rewrite the validation error text to point at where dates usually appear.

D. Include the rider document in the request instead of retrying further.

Correct answer: D

Explanation: Retry-with-error-feedback fixes format and structural errors; it cannot recover information absent from the source. Supply the missing document (or make the field nullable if it's legitimately unavailable).

Distractors:

- A: No number of retries surfaces data the model was never given; varied temperature invites fabrication.
- B: Required fields pressure the model to fabricate a date to satisfy the schema.
- C: Better hints can't help when the date isn't in the provided text at all.

## Question 17

Scenario: The same Claude session that generates your migration scripts is then asked to "review your work carefully before finalizing." Reviewers keep catching bugs the self-review missed.

Question: Why, and what fixes it?

A. The review step needs extended thinking enabled in the generating session.

B. The generator retains its reasoning context; use a separate instance to review.

C. The session should list its assumptions before performing the self-review.

D. The session should self-report a confidence score for each change it made.

Correct answer: B

Explanation: A model reviewing its own output in-session carries the reasoning that produced the bugs, making it unlikely to question its own decisions. An independent instance without that context reviews the code cold and catches more.

Distractors:

- A: More thinking inside the same biased context doesn't remove the bias.
- C: Stated assumptions come from the same reasoning that made the errors.
- D: Self-reported confidence is poorly calibrated and doesn't find the bugs.

## Question 18

Scenario: A customer's first message reads: "I want to talk to a real person about my late delivery." Late-delivery credits are squarely within your agent's capability.

Question: What should the agent do?

A. Escalate to a human immediately, attaching a structured summary of the case.

B. Resolve the late-delivery credit first, then offer a human follow-up if desired.

C. Explain that it can issue the credit instantly and proceed with the resolution.

D. Ask a clarifying question to gauge whether the issue truly requires a human.

Correct answer: A

Explanation: An explicit customer request for a human is honored immediately — no investigation or persuasion first. (The acknowledge-and-offer-to-resolve pattern applies to frustrated customers who have not explicitly asked for a human.)

Distractors:

- B: Resolving first ignores an explicit request and damages trust even when the fix is correct.
- C: Persuading the customer to stay with the bot overrides their stated preference.
- D: The customer already stated the requirement; probing it reads as deflection.

## Question 19

Scenario: Your invoice extraction system shows 97% aggregate accuracy. Leadership wants to eliminate human review for high-confidence extractions to cut costs.

Question: What must happen before automating?

A. Drop review for extractions above 0.95 confidence and monitor complaint volume.

B. Keep full review in place until aggregate accuracy reaches 99% or better.

C. Validate accuracy by document type and field segment before reducing review.

D. Sample 1% of all extractions weekly and widen review whenever errors appear.

Correct answer: C

Explanation: Aggregate accuracy can mask a failing segment — 97% overall may hide, say, 70% on handwritten forms or a specific field. Verify per-segment performance first, then calibrate confidence thresholds on labeled data, and keep stratified sampling of high-confidence extractions running afterward.

Distractors:

- A: Uncalibrated confidence thresholds plus complaints-as-QA means customers find your errors first.
- B: A higher aggregate bar still hides segment failures — same flaw, higher number.
- D: A flat 1% sample is unstratified and reactive; it doesn't establish segment safety before automating.

## Question 20

Scenario: During synthesis, two credible sources report different market sizes: an $8.1B figure from a 2024 industry report and an $11.4B figure from a 2026 trade article.

Question: How should the final report handle this?

A. Use the more recent figure and move the older one to a footnote.

B. Average the figures and cite both sources for transparency.

C. Omit the statistic until a third source resolves the disagreement.

D. Include both figures, annotated with their sources and publication dates.

Correct answer: D

Explanation: Conflicting values from credible sources are preserved with attribution, and dates matter — a 2024 vs 2026 difference may be growth, not contradiction. Arbitrating, averaging, or omitting all destroy information the reader needs.

Distractors:

- A: Recency alone doesn't invalidate the earlier figure, and demoting it hides a possibly-real temporal trend.
- B: An averaged number exists in no source — it's fabricated data with citations attached.
- C: Omission withholds well-sourced information the reader needs.

## Question 21

Scenario: In long billing-dispute conversations your context manager summarizes older turns. Afterward, the agent quotes "around $80" for a refund the customer was promised at exactly $83.47, and order numbers start to drift.

Question: What is the reliable fix?

A. Keep a persistent case-facts block of exact amounts, dates, and order numbers in every prompt.

B. Raise the summarizer's length limit so more of the older turns survive.

C. Re-run the order-lookup tools on every turn so exact values stay fresh.

D. Instruct the summarizer never to round numbers when compressing history.

Correct answer: A

Explanation: Transactional facts belong in a persistent structured block that lives outside summarized history and rides along in every prompt. Summarization inherently compresses specifics; the fix is to exempt the facts from it.

Distractors:

- B: Longer summaries lose precision more slowly but still lose it.
- C: Re-running tools every turn burns tokens and latency, and doesn't preserve promises made in conversation (like the quoted $83.47).
- D: A no-rounding instruction is probabilistic and doesn't protect order numbers, dates, or commitments.

## Question 22

Scenario: Mid-run, your document-analysis subagent discovers that several key sources are paywalled and cannot be read. The coordinator needs to decide what happens next.

Question: What should the subagent return?

A. "Analysis unavailable" once its internal retries are exhausted.

B. The failure type, what was attempted, partial results, and possible alternatives.

C. The completed portion marked successful so synthesis can proceed cleanly.

D. Nothing — it should halt the run and surface the paywall error to the user.

Correct answer: B

Explanation: Structured error context lets the coordinator make an intelligent recovery decision — substitute open sources, proceed with partial results plus coverage annotations, or re-scope. Generic statuses, silent suppression, and full-workflow termination are the three propagation anti-patterns.

Distractors:

- A: A generic status hides which sources failed and what partial work exists.
- C: Marking failure as success poisons the synthesis with an undisclosed gap.
- D: One recoverable failure shouldn't kill the run; the coordinator has options.
