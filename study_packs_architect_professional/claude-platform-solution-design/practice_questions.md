# Claude Platform & Solution Design Practice Questions

## Question 1

Scenario: A partner asks for a "claims triage assistant that reads a claim, decides priority under the partner's existing rule engine logic, looks up policy coverage, and emails the adjuster." An engineer proposes putting all four steps inside a single Claude prompt because "it's simpler that way."

Question: What is the strongest architectural objection to this proposal?

A. Claude cannot read free-text claims reliably, so the first step should also be removed.

B. Deciding priority and looking up coverage are knowledge-boundary and deterministic-rule problems that belong to the partner's existing systems, not Claude's language capability.

C. Emailing the adjuster should never involve Claude in any capacity.

D. The proposal is fine as long as Claude uses extended thinking on every step.

Correct answer: B

Explanation: Priority is a deterministic rule the partner's rule engine already maintains, and policy coverage is live/authoritative data — both are knowledge-boundary or deterministic-rule problems better handled by the systems that already own them, per the decomposition framework's "where do the four properties argue for Claude" test.

Distractors:
- A: Reading and interpreting the claim is squarely in Claude's capability zone (pattern-rich language work); the objection is not there.
- C: Claude can appropriately draft the notification even though sending and approval belong elsewhere — the objection is about priority/coverage, not blanket exclusion from the email step.
- D: Extended thinking doesn't fix a knowledge-boundary or deterministic-rule problem; it's a reasoning-effort lever, not a source-of-truth fix.

## Question 2

Scenario: A team replaced a deterministic SQL check ("claims over £5,000 require senior adjuster") with a Claude prompt to simplify their architecture. Three months into production, an audit found 41 of 14,000 claims misrouted, all cases where the dollar amount appeared in prose rather than as a clean number.

Question: What is the most accurate diagnosis of what went wrong?

A. Claude's context window was too small to hold the claim text.

B. A rule the business needed to be correct every time was handed to a system that is right most of the time, and no test suite or monitoring existed to catch the gap.

C. The team should have used a larger model tier from the start.

D. The rule engine was outdated and needed to be replaced by Claude entirely.

Correct answer: B

Explanation: This is the deterministic-drift failure mode: a deterministic business rule was folded into a probabilistic system, and because the team treated it as something Claude would "just handle," they built no test cases and no monitoring — the kind of logging that would catch a broken SQL check doesn't record in-request model choices.

Distractors:
- A: Context window size is unrelated; single claims are far under any context limit.
- C: A larger model tier doesn't fix a deterministic-rule-in-a-probabilistic-system problem; the fix is keeping the rule in the deterministic system.
- D: The rule engine wasn't the problem — replacing it with Claude is exactly the mistake that caused the misroutes.

## Question 3

Scenario: An architect is deciding between a workflow and an agent for a document-processing task. When traces of similar past work are mined, the actual paths through the system fall into exactly four shapes, all identifiable in advance.

Question: What should the architect conclude?

A. An agent is still the safer choice because it can adapt to any future path shape.

B. Since the paths are enumerable in advance, a workflow (e.g., a router with four chains) is the better-fit pattern, avoiding unnecessary autonomy cost and audit gaps.

C. The four shapes prove the task is too complex for a single pattern and should be split across five separate agents.

D. Multi-agent orchestration is required whenever more than one path shape exists.

Correct answer: B

Explanation: The module's core lesson on this exact scenario: agents should be reached for only when steps genuinely cannot be enumerated in advance. If traces show a small number of enumerable path shapes, a workflow (router + chains) delivers the same capability with better observability, auditability, and lower cost.

Distractors:
- A: Choosing an agent for hypothetical future flexibility when the current shape is known and bounded is exactly the mistake the module's "Flexibility vs Non-determinism" case describes.
- C: Four enumerable shapes is a workflow-routing problem, not evidence of excess complexity requiring multiple agents.
- D: Multi-agent orchestration is for work too large for one context, not merely for having multiple path shapes — routing within a single workflow handles this case.

## Question 4

Scenario: A multi-agent system fans a 50-section contract review out to 50 subagents. Two subagents fail silently (one timeout, one unparseable page) and return nothing. The orchestrator's synthesis reports "48 sections reviewed, 3 flagged," and this summary is circulated as complete.

Question: What design change would have prevented this outcome?

A. Using a larger model tier for every subagent.

B. Adding a synthesis-time coverage check that asserts the number of results returned equals the number of units dispatched, flagging any discrepancy before the summary is shown.

C. Replacing the multi-agent architecture with a single augmented LLM call.

D. Increasing the per-subagent timeout to an unbounded duration.

Correct answer: B

Explanation: The root cause was that the orchestrator counted only the results it received with no rule requiring the count to match the number of dispatched units. A coverage check at synthesis is the specific, targeted fix the module identifies for this exact failure mode.

Distractors:
- A: A bigger model doesn't fix a missing coverage-reconciliation rule; the failures were a timeout and a parse error, not model quality.
- C: A single augmented LLM call couldn't handle a 50-section review in one bounded pass at all — that's not a viable substitute.
- D: An unbounded timeout could mask other problems (e.g., a hung subagent) and doesn't address the missing reconciliation logic, which is the actual defect.

## Question 5

Scenario: A customer asks an AI support assistant "Where's my order?" The assistant retrieves two chunks from a vector index — one saying the order shipped, one saying it's still processing — and confidently answers based on the higher-similarity chunk. The order had actually been returned to depot for a damaged label and was awaiting re-dispatch, a state that existed in neither chunk. A live order-status API existed but was never called.

Question: What is the correct architectural fix?

A. Use a more advanced embedding model to improve retrieval precision.

B. Shorten the index refresh interval so chunks stay more current.

C. Call the system that owns the live order state directly via a tool call, instead of retrieving cached text snapshots of it.

D. Add a third retrieval pass to average the two conflicting chunks into one answer.

Correct answer: C

Explanation: This is the textbook retrieval-vs-tool-call mistake: retrieval is for stable knowledge, tool use is for live state. No embedding or refresh-interval tuning fixes an index that structurally cannot represent "what is true right now" — only a direct tool call to the system of record does.

Distractors:
- A: A better embedding model still returns text snapshots from different points in time; it doesn't solve the live-state problem.
- B: A shorter refresh interval reduces but never eliminates staleness for genuinely live, frequently-changing state — and adds maintenance cost for a problem retrieval structurally can't solve.
- D: Averaging two stale, conflicting snapshots produces a plausible-sounding but still-wrong answer; the correct current state exists in neither chunk.

## Question 6

Scenario: A professional-services partner has 4,000 documents: section-numbered client contracts, long-form project write-ups, and a structured methodology handbook. Users ask concept-lookup questions ("what does our methodology say about X"), exact-target questions ("find the termination clause in the Acme contract"), and broad-synthesis questions ("summarize how we've handled engagements like this one").

Question: Which pipeline design best fits this corpus and query mix?

A. Fixed-size chunking for all documents and dense-only indexing, since it's the simplest to operate.

B. Hierarchical chunking for the contracts and handbook (preserving section context), semantic chunking for the write-ups (self-contained prose chunks), and hybrid indexing across the corpus to serve both concept and exact-target queries.

C. Semantic chunking for everything and sparse-only indexing, since most questions are about meaning, not keywords.

D. One chunking and indexing strategy chosen at random, since RAG design doesn't materially affect answer quality.

Correct answer: B

Explanation: Chunking should be chosen by document structure (hierarchical for structured, section-numbered material; semantic for prose needing self-contained chunks) and indexing by query pattern (hybrid to serve both the concept-lookup/paraphrase queries that favor dense retrieval and the exact-target queries like a named clause that favor sparse/keyword matching).

Distractors:
- A: Fixed-size chunking ignores the contracts' and handbook's structure, and dense-only indexing would likely miss the exact-target "find the termination clause" queries.
- C: Semantic chunking loses the exact section context contracts and the handbook need, and sparse-only indexing would miss paraphrased concept queries.
- D: RAG chunking/indexing choices directly determine retrieval quality; the module explicitly frames this as a defensible design decision, not an arbitrary one.

## Question 7

Scenario: A team defaulted every call in their pipeline to Opus during build so they wouldn't have to defend a model choice or build an eval set. Ninety days after launch, monthly cost is running 7x the original estimate and median latency is 2.3 seconds against an 800ms target agreed at launch.

Question: What is the most accurate diagnosis?

A. Opus itself is defective and should never be used in production pipelines.

B. Not making a deliberate per-step model-tier decision was itself an implicit decision that defaulted the system to its most expensive configuration, compounded by a routing classifier left on extended thinking that never needed reasoning.

C. The partner's monthly cost review cadence was the root cause and switching to weekly review alone would have fixed the overrun.

D. The fix requires abandoning Claude and evaluating a different model provider entirely.

Correct answer: B

Explanation: The module's "Opus Everywhere" case: the absence of a deliberate model-tier decision is not neutral — it defaults to the most expensive option — and a second compounding factor (unnecessary extended thinking on a classifier) added further unjustified cost and latency. An eval set built retroactively let the team route steps to cheaper tiers with no quality regression.

Distractors:
- A: Opus is appropriate on the one step where the eval showed it earned its place (final response composition); the failure was applying it everywhere without an eval.
- C: Review cadence contributed to detection lag, but it did not cause the underlying architecture problem — no per-step model-tier decision existed at all.
- D: Nothing in the case suggests a provider-level defect; it's a design/discipline failure (no eval-gated tiering), fully addressable within the same platform.

## Question 8

Scenario: A team enables a Sonnet-to-Haiku model swap in production without building an eval set first, reasoning that "Haiku is cheaper and probably good enough."

Question: What is missing from this decision process, per the module's guidance on model swaps?

A. Nothing — cost savings alone justify a swap between model tiers.

B. A curated eval set with known-good outputs, a grading function, and a delta/rollback threshold set in advance, since any model change is a behavior change that should be treated like a release.

C. A sign-off from the Anthropic account team on every model-tier change.

D. A commitment to use extended thinking on all Haiku calls to compensate for the smaller model.

Correct answer: B

Explanation: The module treats a model swap as a code deployment requiring, at minimum, a curated test set covering the real distribution of work, a grading function, and a rollback threshold set before the eval runs — exactly as shown in the Sonnet-to-Haiku downgrade case, where a stratified eval surfaced a partial-migration option a single overall score would have hidden.

Distractors:
- A: Cost savings without a quality check is exactly the gap the module warns against — "cheaper" isn't "validated."
- C: The module does not require Anthropic sign-off for internal model-tier decisions; the required gate is an internal eval set and rollback threshold.
- D: Extended thinking is a separate cost/latency lever gated by its own measured accuracy gap, not a blanket compensation strategy for a smaller model.

## Question 9

Scenario: A team put their reusable analysis prompt into production with the per-request document content placed at the top of the prompt, ahead of the large fixed instruction block. They observe no cost savings from prompt caching at all.

Question: What is the correct fix?

A. Increase the cache TTL to give the cache more time to build up hits.

B. Reorder the prompt so the fixed, stable instruction content comes first and the per-request dynamic content comes last, since the cache matches on a stable prefix.

C. Switch to a smaller model tier, since caching savings scale with model size.

D. Disable caching entirely, since it clearly does not work for this use case.

Correct answer: B

Explanation: The module's caching-mechanics case is exactly this scenario: because the cache matches on a stable prefix, putting dynamic content first means the prefix changes on every request and the cache never hits. Reordering fixed content first, dynamic content last, is the specific fix.

Distractors:
- A: A longer TTL doesn't help if the prefix itself changes on every single request — there's nothing stable to retain.
- C: Caching savings are about prefix stability and reuse, not model tier; changing models doesn't address the ordering defect.
- D: The mechanism works fine once the ordering is corrected — abandoning caching discards a legitimate cost-saving lever over a fixable configuration mistake.

## Question 10

Scenario: A regional bank proposes an "operations assistant" for branch staff: Claude Code running on branch laptops with a per-branch CLAUDE.md, MCP servers exposing the customer database, appointment system, and policy corpus, and subagents running compliance checks on every interaction.

Question: What is the most serious architectural defect in this proposal?

A. Claude Code cannot run on laptops, only in cloud environments.

B. The entry point (Claude Code, a terminal-based developer tool) is mismatched with non-technical branch staff, MCP is used without a genuine cross-client reuse need, and compliance — the highest-consequence path — runs on subagents, the weakest deterministic guarantee available.

C. MCP servers are inherently insecure and should never be used for customer data.

D. The proposal is sound; the only issue is that Sonnet should be used instead of Opus.

Correct answer: B

Explanation: This is the module's "Claude Code Misused" case, with three compounding failures: entry point chosen before the user was named (branch staff don't run terminals), MCP carried forward without a reuse justification (no other Claude clients existed in the bank), and compliance assigned to the entry point with the weakest deterministic guarantees instead of deterministic server-side code.

Distractors:
- A: Claude Code can technically run locally; the defect is audience/entry-point fit, not a technical impossibility.
- C: MCP itself isn't inherently insecure; the issue is applying it without a reuse justification, adding integration cost for a capability the partner didn't need.
- D: Model tier is not the issue raised in this case at all; the defects are entry-point, integration-layer, and compliance-placement mistakes.

## Question 11

Scenario: A healthcare network needs a clinical documentation assistant. The network already holds a Business Associate Agreement (BAA) with AWS, and has confirmed AWS Bedrock is covered under that existing agreement. A competing proposal suggests using the direct Anthropic API with a separately negotiated BAA instead.

Question: What is the correct choice and reasoning?

A. AWS Bedrock, because the deciding tradeoff is governance/control: the network's existing BAA already covers this configuration, eliminating the compliance risk before any other tradeoff applies.

B. Direct Anthropic API with a new BAA, because the direct API always gives more control over how PHI flows through the system.

C. AWS Bedrock, because Bedrock pins data to a US region, which alone satisfies HIPAA regardless of any BAA.

D. Either option is equally valid since the underlying model behaves identically on both routes.

Correct answer: A

Explanation: When a partner already has a compliance-covering agreement in place for a given route, that eliminates the compliance risk before cost, latency, or ergonomics tradeoffs are even considered — negotiating a brand-new BAA for the direct API when an existing, already-confirmed agreement covers Bedrock is unnecessary risk and delay.

Distractors:
- B: This treats "more control" as an absolute good, ignoring that it requires negotiating and validating a brand-new BAA when a covering agreement already exists — the module's governance framing is about what's already committed, not abstract control.
- C: Regional data pinning alone doesn't satisfy HIPAA; the BAA is the governing instrument, and the existing agreement already covering the configuration is the actual deciding factor.
- D: While the model behaves identically across routes, the delivery-route decision is precisely about which cloud commitment and compliance agreement the partner has already made — it's not indifferent here.

## Question 12

Scenario: A financial services firm on GCP needs a high-frequency trade-commentary system that must generate a natural-language summary within 400 milliseconds of each trade.

Question: Which delivery route and reasoning best fits?

A. AWS Bedrock, because Bedrock's managed infrastructure is generically optimized for low-latency inference regardless of the firm's cloud environment.

B. Direct Anthropic API, because it always ships new features first and therefore has the lowest overhead.

C. Google Vertex AI, because the 400ms requirement demands the lowest-latency path, and staying inside the firm's existing GCP environment minimizes network round-trip.

D. Any route works equally well since the model's inference speed is identical everywhere.

Correct answer: C

Explanation: The deciding tradeoff here is latency, and the delivery-route decision should keep the request path inside the firm's existing cloud environment (GCP) to minimize network round-trip — this is the entry-point/route selection principle of matching the route to what the partner has already committed to, applied to a latency-critical case.

Distractors:
- A: Bedrock is not the firm's cloud environment (GCP), so routing there would add cross-cloud network latency rather than reduce it — "generically optimized" doesn't override that geography.
- B: Feature-release speed is irrelevant to raw request latency, and picking a route outside the firm's own cloud does not minimize round-trip time.
- D: The model's inference itself is the same across routes, but network path and regional proximity differ meaningfully — which is exactly why route selection matters for a 400ms budget.
