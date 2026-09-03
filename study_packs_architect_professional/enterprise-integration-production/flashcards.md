# Enterprise Integration & Production Flashcards

## Evals As Acceptance Criteria

Q: Why should the eval suite be written before production code, not after?

A: It forces you to state success in measurable terms, exposes design assumptions while they're still cheap to change, and gives you a gate to test whether any later change actually improved the system.

Domain: D4

Example: A team writes the eval for "extract claimant, policy number, loss amount, date of loss with 100% field accuracy" before building the claims summarizer, so every later prompt tweak has something objective to pass against.

## Eval Workflow Stages

Q: What are the five stages of the eval workflow, in order?

A: Define the task, build the golden dataset, run automated checks, score with a judge, interpret and act.

Domain: D4

Example: A team specifies "flag non-standard indemnification clauses" (define), assembles 200 real contracts including edge cases (golden dataset), runs schema checks (automated), has a judge model score clause-flagging quality (judge), then decides whether a prompt change is needed (interpret).

## Code-Based Eval

Q: When should you use a code-based eval instead of a model judge?

A: When the behavior is unambiguous and can be checked deterministically — schema validation, regex match, JSON parsing, length limits, or exact match against authoritative data.

Domain: D4

Example: Checking that every response is valid JSON matching a defined schema is a code-based eval; it either parses or it doesn't.

## Model-Based Eval

Q: When is a model-based (LLM-as-judge) eval the right tool, and what does it cost?

A: When the behavior requires interpretation, such as tone, reasoning quality, or edge-case appropriateness. It costs roughly one API call per item at the judge model's rate, which adds up at scale.

Domain: D4

Example: Scoring whether a customer-facing message's tone is "appropriately professional for the brand" needs a judge model, not a regex.

## Judge Calibration

Q: Why is an uncalibrated LLM judge worse than no automated grade at all?

A: It produces confident scores that may not track quality, which is more dangerous than an obvious gap because it looks trustworthy. Calibrate by running the judge against human-labeled outputs and confirming agreement is high enough to rely on.

Domain: D4

Example: A team trusts a judge's 9/10 safety scores for months until a human audit reveals the judge was systematically lenient on a failure category it was never calibrated against.

## The Grading Ladder

Q: What is the grading ladder, and why climb it in order?

A: Code-based grading first (cheapest, never drifts), LLM-as-judge second (for interpretation, with rubrics and calibration), human grading last (most expensive, least scalable). Climb only as far as the behavior demands.

Domain: D4

Example: A team checks output length and JSON validity in code, escalates reasoning-quality scoring to a calibrated judge, and reserves human review only for flagged safety-critical edge cases.

## Success Criteria Conversion

Q: What four steps turn a vague requirement like "summarize claims accurately" into a measurable eval criterion?

A: Identify the specific behavior, set numeric thresholds sourced from the business, identify failure modes as dataset categories, and include adversarial/edge-case inputs.

Domain: D4

Example: "Summarize accurately" becomes "extract filer name, claim number, incident date, claimed amount at 100% field accuracy, under 2% hallucination rate, 99.5% schema compliance" plus a dataset that includes handwritten and non-standard-layout claims.

## Evals As A Change Gate

Q: What happened when a team revised its summarization prompt but didn't update the eval suite to match?

A: The eval suite kept passing because it still measured the old prompt's expected behavior. Two days after the swap shipped, field reports showed multi-clause legal sentences being truncated — a regression the stale eval couldn't catch.

Domain: D4

Example: This is the canonical argument for re-running and updating the golden dataset every time the prompt, model, or retrieval strategy changes, not just when a bug is reported.

## Multi-Turn Evals

Q: Why do multi-turn evals need their own golden dataset instead of reusing single-turn eval data?

A: A single-turn eval set doesn't reveal how the system holds up across a conversation — whether it keeps prior context straight, avoids inventing details on follow-ups, and holds output quality as the conversation runs longer. That requires full conversation transcripts as the unit being scored.

Domain: D4

Example: A support-chat eval suite adds a separate dataset of ten-turn transcripts covering topic shifts, to catch a bot that forgets an earlier stated account number by turn seven.

## POC-To-Production Gap

Q: What four dimensions are invisible in a working demo but break in production?

A: Cost, latency, reliability, and failure modes.

Domain: D3

Example: A document-triage POC that costs pennies a day and never fails on a single request can still produce an unaffordable bill, blow an SLA under concurrent load, and go down entirely on the first transient API error once it hits real traffic.

## Token Distribution Vs Average

Q: Why can a cost model based on average token usage significantly underestimate production cost?

A: Token distributions are often skewed — most requests are short, but a tail of long requests consumes a disproportionate share of total cost, sometimes 2-3x what an average-based estimate predicts.

Domain: D3

Example: A team models cost from typical 300-token inputs, then discovers in production that a small fraction of long documents was driving 80% of total token spend.

## P95 Latency As Design Target

Q: Why is p95 latency a better design target than median latency?

A: SLA breaches are usually caused by the slowest requests, not the typical ones. P95 is the latency value below which 95% of requests complete — median hides exactly the tail that breaches SLAs.

Domain: D3

Example: A chatbot's median response is 1.2s, but its p95 under concurrent load is 4s — well past a 3s SLA — even though "the demo felt fast."

## Prompt Caching Mechanics

Q: When does prompt caching deliver the most savings, and what is its key risk?

A: When the system prompt is long, stable, and reused across many requests faster than the cache TTL (default 5 minutes) — cached tokens are billed at a fraction of the standard input rate. The risk is consistency: if cached content needs to reflect live state, caching introduces a staleness window.

Domain: D3

Example: Caching a 5,000-token stable system prompt across 50,000 monthly requests cuts the dominant input-cost driver, but caching a prompt that embeds today's inventory levels risks serving stale stock counts.

## Reliability Control Placement

Q: Where in the call stack should retries, circuit breakers, and fallback chains each sit?

A: Exponential-backoff retries close to the API call, circuit breakers at the service boundary, and fallback chains in the orchestration layer.

Domain: D3

Example: A rate-limit (429) triggers a backoff retry at the call site; a downstream dependency with a high sustained error rate trips a circuit breaker at the service boundary; if the primary model is fully unavailable, the orchestration layer routes to a fallback model tier instead of surfacing an error to the user.

## Failure Modes By Architecture Type — Agent

Q: What breaks first in an agent architecture, and how do you mitigate it?

A: Unbounded tool use and growing context — cost and latency balloon invisibly until a single request blows the budget. Mitigate with per-turn token budgets, max tool-call counts, explicit stopping criteria, a minimal tool set, and evals on the stopping behavior itself, not just output quality.

Domain: D3

Example: An agent debugging a codebase without a turn limit keeps calling tools indefinitely on an ambiguous task, running up cost far beyond what any single request should cost.

## Failure Modes By Architecture Type — RAG

Q: What breaks first in a RAG architecture, and how do you mitigate it?

A: Retrieval quality drift — from unreindexed document changes, query/document representation misalignment, or staleness from scheduled refreshes on live-state queries. Mitigate by monitoring retrieval precision/recall as system metrics and separating live-state from static knowledge queries.

Domain: D3

Example: A RAG-backed FAQ bot keeps answering from documents that were deleted from the index six months ago because the index was never rebuilt after content changes.

## Model Version Pinning

Q: What operational discipline applies equally across every architecture type covered in this module?

A: Model version pinning — pin the model version in configuration, monitor the deprecation page, and maintain a version-update runbook.

Domain: D3

Example: A team pins `claude-sonnet-4-6` explicitly rather than tracking "latest," so a silent model update can't change production behavior without a deliberate, evaluated migration.

## Sizing A Use Case — Volume Source

Q: Where should call-volume estimates for a cost model come from?

A: The business requirement, from the business owner — not developer intuition and not a sample dataset.

Domain: D6

Example: An architect asks the business owner directly "how many conversations per day does support handle?" rather than extrapolating from the 40 test conversations used during development.

## Scoping Sequence

Q: What four-step sequence turns a business requirement into a scoped architecture ready for a statement of work?

A: Business requirement to capability list, capability list to architecture sketch, architecture sketch to boundary conditions, boundary conditions to SOW.

Domain: D6

Example: "Process insurance claims" becomes four separate capabilities (extract fields, look up coverage, route to adjuster, draft notification), each assigned an owner (Claude vs. existing system vs. human), with documented boundaries (works up to 20-page claims) that go straight into the SOW.

## Four AI Properties — Feasibility Lens

Q: What are the four AI properties used to assess technical feasibility, and what design pattern compensates for each?

A: Next-token prediction (probabilistic vs. precision-critical — compensate with generator-verifier loops, code-based evals, tool calls); Knowledge (rare/recent/domain info — compensate with RAG or live tool calls); Working memory (inputs exceeding the context window — compensate with chunking, progressive loading, summarization); Steerability (ambiguous instructions or precise computation — compensate with explicit schemas, structured outputs, code execution).

Domain: D1

Example: A feasibility review flags a real-time trading assistant on the Knowledge property — current market prices aren't in training data, so a live tool call is required, not model recall.

## Feasibility Verdicts

Q: What are the three possible feasibility verdicts, and what must accompany each?

A: Feasible as scoped (document the assumptions, since they can flip the verdict), feasible with constraints (document each constraint and its failure mode), not feasible (state which constraint is disqualifying and, if applicable, what scope reduction would change the verdict).

Domain: D6

Example: A delay-predictor use case is ruled "feasible with constraints" because extraction accuracy on a transactional write requires a code-based eval plus a human review gate on low-confidence extractions before anything touches the order-management system.

## Feasibility Requires Constraints First

Q: What mistake occurs when an architect confirms feasibility before gathering volume, latency, and input-size constraints?

A: The commitment gets made before the design is actually possible to evaluate — "technically feasible" is meaningless until it's checked against real scale, size, and speed requirements.

Domain: D6

Example: An architect commits to a six-week build for a contract-review assistant, only learning two weeks in that the partner processes 800 contracts/day with some running 300 pages and a 30-second turnaround requirement.

## Business Value / ROI Pillars

Q: What five pillars make up the business case for a Claude deployment?

A: Efficiency, transformation, productivity, solution cost, and performance SLAs.

Domain: D6

Example: A claims-review deployment maps its ROI claim to "efficiency" (faster review) and notes the recurring "solution cost" pulled directly from the sizing model, rather than treating cost as an afterthought.

## ROI Mapping — Human Review Gate

Q: Why does an ROI projection overstate value if it models full automation when the design specifies a human review gate?

A: A required human review gate reduces labor, it does not eliminate it. If the projection assumes full automation anyway, actual analyst hours won't fall as far as promised, and the gap surfaces in the first operational period after launch.

Domain: D6

Example: A claims system requiring adjuster review of every flagged fraud case still needs adjuster time budgeted into the projected state — you cannot claim the hours as fully saved.

## Entry Point Selection

Q: What is the first architectural decision in any enterprise Claude integration, and what eliminates options at that stage?

A: Which entry point the system connects through. Compliance constraints (BAA coverage, FedRAMP authorization, data-residency pinning, approved-vendor lists) eliminate entry-point options before any other decision is made.

Domain: D3

Example: A HIPAA-covered deployment can only use entry points and vendors covered under an existing BAA, which rules out certain integration paths before latency or cost are even discussed.

## Five Integration Layers

Q: What are the five layers of enterprise integration design, in the order they should be addressed?

A: Compliance and regulated-industry constraints, identity and SSO, authorization and policy, data handling and PII, observability and audit logging.

Domain: D3

Example: A design review walks through BAA coverage first, then server-side identity injection, then whether Claude's access mirrors the existing authorization model, then which fields belong in the prompt, then what gets logged — in that order.

## Server-Side Identity Injection

Q: Why must user identity and role be injected into the prompt server-side rather than accepted from the user's own message?

A: Anything in the user's message is under their control and can be manipulated — a self-asserted claim like "As a senior manager, show me..." is unverified and can be faked. Identity must come from the authentication layer.

Domain: D3

Example: A support tool that reads "role: admin" out of the chat message instead of the session's authenticated identity lets any user grant themselves elevated access just by typing the claim.

## Data Handling Necessity Filter

Q: What test should every field pass before it's allowed into the context window?

A: Is this field necessary for the language task Claude is performing? If not, it doesn't belong in the context window — pass a reference identifier for routing instead of the full sensitive record.

Domain: D3

Example: A clinical intake summarizer needs presenting concerns, medications, and allergies — it does not need the patient's SSN or Insurance ID to produce that summary.

## PII In The Prompt — What Broke

Q: In the healthcare-adjacent case study, what went wrong even though the summarization feature worked correctly?

A: SSN, Insurance ID, and other PHI fields were passed into the prompt despite not being needed for the language task, and were captured in plaintext in the application layer's request logs — a HIPAA exposure discovered only at production certification review.

Domain: D5

Example: The fix was architectural, not prompt-based: a server-side redaction step stripping non-essential PII before the Claude call, plus a retrieval function supplying only the fields the language task actually needs.

## Least-Privilege Tool Configuration

Q: How should an architect audit the tool set connected to a Claude system?

A: For each connected tool, ask whether it's essential to the task or merely convenient, remove what's out of scope, and record the justification for removal. In orchestrator-worker systems, scope each subagent's tool access to only what its specific task requires.

Domain: D3

Example: A customer-service agent that can send emails, issue refunds, and browse the web is trimmed to just the refund tool once the team confirms the other two aren't part of the actual task.

## What Observability Should Log

Q: What four categories should every production Claude request log?

A: The request (model version, input token count, prompt identifier), the response (output token count, latency, stop reason), the context (user role, session ID, whether caching applied), and the outcome (whether the downstream system accepted the output, rejection signals).

Domain: D4

Example: A trace that includes stop reason and downstream acceptance lets a team distinguish "the model refused" from "the model answered but the CRM rejected the format" — two very different problems.

## Why LLM Systems Are Hard To Debug

Q: Why does standard error/timeout logging fail to catch most LLM production problems?

A: An LLM-based system doesn't crash when something goes wrong — it produces a subtly wrong response. Standard logging catches errors and timeouts but misses quietly incorrect outputs with real business consequences.

Domain: D4

Example: A claims summarizer that silently drops a policy exclusion clause returns a 200 OK with no error — only per-request outcome tracking and evals would catch it.

## Observability As Precondition For Agent Autonomy

Q: Why do security organizations increasingly treat observability as a precondition for approving any agentic action?

A: Without a trustworthy audit trail, an autonomous system cannot be approved to act — an action taken but not logged is, to a security reviewer, an action that cannot be allowed.

Domain: D5

Example: Before approving an agent to auto-file support tickets, a security review requires that every ticket-creation call be logged with full context, or the capability is disabled.

## Shared API Key Risk

Q: What breaks in a multi-tenant deployment that uses a single shared API key across all tenants?

A: There's no way to attribute a rate-limit breach to the tenant that caused it — when the org-level limit trips at peak load, every tenant absorbs the impact even though only one caused it. Separate API keys per tenant are required for attribution and isolation.

Domain: D3

Example: One tenant's traffic spike trips the shared rate limit and every other tenant's requests start failing too, with no way to trace the cause back to the offending tenant.

## Integration Diagram Critique

Q: In the multi-tenant SaaS customer-service diagram exercise, which components were flagged as integration problems?

A: A shared API key across all tenants, a capability check based on a user-asserted "I am a premium customer" claim, account number and email appearing in request logs, and a Claude response passed to the downstream CRM with no logging at the integration layer.

Domain: D3

Example: The same exercise flagged server-side authentication and per-tenant storage isolation as sound components — the problems were specifically the shared key, the self-asserted claim, the exposed PII in logs, and the missing integration-layer log before the CRM handoff.

## Structured A/B Test Hypothesis

Q: What makes "the new prompt is better" an unusable A/B test hypothesis, and what does a usable one look like?

A: It names no treatment, no metric, and no threshold. A usable hypothesis names the treatment, the metric, the expected direction/threshold, and any constraints — e.g., "replacing the summarize instruction with an extract-action-items instruction will increase task success rate by at least 5% without degrading p95 latency."

Domain: D4

Example: This specificity is what lets a team later say definitively whether the experiment succeeded, rather than arguing after the fact about what counts as a win.

## Pre-Specifying The Primary Metric

Q: Why must the primary metric be chosen before an A/B test runs, not after seeing results?

A: Choosing the metric after seeing results is outcome-shopping — you can always find some metric that moved in the right direction if you look at enough of them after the fact, which turns an experiment into a retrospective correlation rather than evidence.

Domain: D4

Example: A team that watches five metrics and reports "task success rate improved" only after checking all five, ignoring that latency and cost both got worse, has cherry-picked a story rather than run a test.

## Statistical Vs Practical Significance

Q: What two separate questions should you ask before declaring an A/B test winner?

A: Is the effect large enough to justify the operational overhead of maintaining the new version? And did any secondary metric degrade? A statistically significant result can still be too small to matter, or can come with an unacceptable tradeoff.

Domain: D4

Example: A prompt change that improves task success rate 2% while increasing cost 30% may not be a net win depending on budget constraints, even if the 2% is statistically real.

## Shadow Testing

Q: What is shadow testing, and when should you use it instead of a live A/B test?

A: Running the new version in parallel on a copy of live traffic, logging its output but serving every user the current version's response, then scoring the new version's outputs offline. Use it when a single bad output carries too much risk, or traffic is too low to reach significance with a live split — often the only acceptable validation method for regulated deployments.

Domain: D4

Example: A medical-intake summarizer change is validated via shadow testing against real incoming intake traffic, with zero patients ever seeing the unvalidated version's output.

## The 50-Session Winner That Wasn't

Q: What three compounding problems invalidated the "6-point win" in the 50-session A/B comparison case study?

A: The sample size was too small to distinguish the 6-point difference from noise; the input distribution wasn't controlled between the two groups; and the primary metric was chosen only because it happened to move in the right direction.

Domain: D4

Example: Two weeks after deployment, the new version's task success rate settled at 61% — below the old version's 62% baseline — because the apparent 6-point gain was noise dressed up as signal.

## Observability At Scale — Four Layers

Q: What are the four layers of observability instrumentation at scale, and what question does each answer?

A: Request-level tracing (what is the system doing — raw data), metric aggregation (how well is it performing — cost, latency p50/p95, success rate, error rate), anomaly detection (when did it change — threshold alerts and distribution comparison), change attribution (why did it change — model drift vs. data drift vs. model-update effects).

Domain: D4

Example: A cost spike triggers an anomaly alert (layer 3); change attribution (layer 4) then determines whether it's because the input mix shifted (data drift) or the model version was silently updated (model-update effect) — each needs a different fix.

## Per-Request Decomposition

Q: Why is per-request decomposition important even when aggregate metrics look healthy?

A: Aggregate metrics can look fine while a small fraction of requests consumes most of the budget and produces wrong outputs. Aggregates protect against obvious failures; per-request decomposition protects against the non-obvious ones.

Domain: D4

Example: A dashboard shows average cost per request within budget, while a hidden 3% of requests (long documents hitting an edge case) are burning 60% of total monthly spend.

## Failure Taxonomy

Q: What are the four failure classes in the production failure taxonomy, and what's the fix for each?

A: Prompt failure (ambiguous instruction — fix the prompt), hallucination (confident but ungrounded content — fix with grounding via retrieval/tool use/verification, not a stronger instruction), model mismatch (wrong tier for the task or swapped without re-eval — fix via model selection gated by an eval), orchestrator-workers failure (recoverable subagent vs. unrecoverable orchestrator failure — needs a trace spanning both).

Domain: D4

Example: A team that keeps rewriting the system prompt to fix a hallucinating extraction step is misdiagnosing a hallucination as a prompt failure — the actual fix is grounding via retrieval or a verification tool call.

## Discernment

Q: What is Discernment, and how does it apply to a production monitoring practice?

A: One of the four AI Fluency competencies — the discipline of judging the quality of model output rather than accepting it at face value. In production, it's the habit of classifying each output as acceptable, needs revision, or needs override, and feeding that judgment back into evals and monitoring.

Domain: D4

Example: A team without Discernment watches its success-rate metric hold steady for months without ever re-checking whether the outputs behind that metric are still actually good.

## Business-To-Technical Metric Translation

Q: Why should the translation layer between technical metrics and business KPIs be built when the system is designed, not after the first business review?

A: The people funding the deployment read a business KPI dashboard (e.g., handle time, first-contact resolution), not the request trace. If the mapping isn't built at design time, the first business review that asks "what's driving the change in handle time" requires a retrospective reconstruction instead of a live query.

Domain: D6

Example: A customer-service deployment maps task success rate to first-contact resolution and latency to average handle time from day one, so a business reviewer can query the dashboard directly instead of waiting on an ad hoc analysis.

## Experiment-Design Plane

Q: What two axes determine the required experimental posture and minimum sample size for a change?

A: Expected effect size and the confidence requirement. A high-stakes domain (e.g., a medical intake summarizer where an error could delay treatment) needs high confidence regardless of effect size, while a minor low-stakes wording tweak can tolerate a lighter test.

Domain: D4

Example: A prompt architecture change for a medical intake summarizer sits in the high-confidence zone even if the expected effect looks large, because the cost of being wrong is too high to accept moderate confidence.

## Batch API Cost Lever

Q: When should an architect model the Batch API as a cost alternative, and what must be checked first for regulated workloads?

A: When the SLA permits asynchronous processing — batch processing can offer a substantial price reduction relative to standard API pricing. For regulated workloads, verify batch processing is covered under the partner's BAA and compliance configuration before routing governed data through it.

Domain: D3

Example: An overnight document-classification job with no real-time SLA requirement is a strong Batch API candidate, but a healthcare deployment must confirm BAA coverage for batch processing before routing PHI through it.
