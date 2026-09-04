# Enterprise Integration & Production

- Source URL: https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional
- Completed: 2026-09-03
- Study pack: `study_packs_architect_professional/enterprise-integration-production/`

## Captured Sections

- Module Introduction: Orientation
- Evals: Evals as acceptance criteria
- Watch Out: The eval suite that measured the wrong thing
- Checkpoint: Sort the eval types (code-based vs. model-based)
- POC to Prod: From POC to production (cost, latency, reliability, failure modes)
- Watch Out: The demo cost profile that became the production bill
- Checkpoint: Cost & reliability calculator
- Sizing: Use-case sizing and feasibility
- Watch Out: The scoping call that skipped the constraints
- Checkpoint: Justify the feasibility call (three scenarios)
- Integration: Enterprise integration patterns (identity, auth, data, observability)
- Watch Out: The PII field that went straight into the prompt
- Checkpoint: Critique the integration diagram
- A/B & Obs: A/B testing and observability at scale
- Watch Out: The 50-session winner that wasn't
- Checkpoint: Place on the experiment-design plane
- Exercise: Define the evaluation framework (insurance claims case study; model answer not captured in this transcript)
- Wrap-up: Glossary
- Wrap-up: Recap (five takeaways)
- Module Complete / Certification progress screen

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| D1: Solution Design & Architecture | Low | Touches architecture only indirectly, through failure-mode-by-architecture-type (agent, RAG, document pipeline, orchestrator-workers) and the capability-list-to-architecture-sketch scoping step. Does not teach the core patterns themselves (workflow vs. agentic vs. augmented LLM) or multi-agent orchestration design; assumes Module 1 covered that. |
| D2: Claude Models, Prompting & Context Engineering | Low | Covers prompt caching mechanics (cache_control, 5-minute default TTL, cache write vs. read cost) and model tier selection as a cost/latency lever. Does not cover system prompt authoring technique, prompting patterns, or Skills as prompt reuse; caching here is framed as a cost lever, not a context-engineering technique. |
| D3: Integration | High | This is the core of the module. Covers entry-point selection under compliance constraints, the five integration layers (compliance, identity/SSO, authorization, data handling/PII, observability), least-privilege tool configuration, server-side identity injection, accuracy-latency tradeoffs (model tier, caching, max_tokens), observability instrumentation (request/response/context/outcome logging, anomaly detection, change attribution), and failure modes by architecture type (agent, RAG, document pipeline, orchestrator-workers). RAG is discussed at the failure-mode level (retrieval quality drift, precision/recall monitoring), not chunking/indexing design. MCP/API/CLI protocol selection is named ("Place the right integration point (API, SDK, MCP, Claude Code)") but not built out in depth in this capture. |
| D4: Evaluation, Testing & Optimization | High | Covers the full eval workflow (task definition, golden dataset, automated checks, judge scoring, interpret/act), code-based vs. model-based vs. human-review evals, the grading ladder, judge calibration, evals as a change-gating mechanism, multi-turn eval sets, structured A/B testing (hypothesis, treatment/control, primary metric, sample size), shadow testing, observability metrics (p50/p95 latency, cost per request, error rate), and a four-part failure taxonomy (prompt failure, hallucination, model mismatch, orchestrator-workers failure). |
| D5: Governance, Safety & Risk Management | Medium | Covers PII/PHI data-handling discipline (necessity filter, server-side redaction, HIPAA example), the compliance-first entry-point elimination logic (BAA, FedRAMP, data residency, attorney-client privilege), and audit-log-as-precondition-for-agent-autonomy. Does not cover broader guardrail design, ethical AI frameworks, or human-in-the-loop validation as a general pattern beyond the specific low-confidence-routing examples. |
| D6: Stakeholder Communication & Lifecycle Management | Medium | Covers the discovery-to-SOW sequence (business requirement to capability list to architecture sketch to boundary conditions to SOW), feasibility verdicts (feasible as scoped / feasible with constraints / not feasible) as a communication artifact, and ROI/business-value mapping (five pillars, baseline vs. projected state, payback period with sensitivity). Does not cover general stakeholder communication technique, SLA negotiation, or documentation practice beyond the sizing/scoping context. |
| D7: Developer Productivity & Operational Enablement | None | Not addressed. This module is about production architecture and integration, not team tooling, developer workflow configuration, or debugging/operational support for engineers. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Evals-before-code | Write the eval suite before production code. Forces you to state success measurably, expose design assumptions early, and gives a gate to test whether any change (model swap, prompt revision, retrieval change) actually improved the system. |
| Eval workflow stages | 1) Define the task (measurable behavior + test prompt), 2) Build the golden dataset (representative inputs incl. edge cases), 3) Run automated checks, 4) Score with a judge, 5) Interpret and act. Each stage's output feeds the next. |
| Code-based eval | Deterministic function check (schema validation, regex, JSON parse, length, exact match against authoritative data). Milliseconds, near-zero cost, cannot judge interpretation. Use for unambiguous behaviors. |
| Model-based eval (LLM-as-judge) | A judge model scores output against a rubric and returns reasoning. Medium/high cost (one API call per item). Use for behaviors requiring interpretation: tone, reasoning quality, safety, ambiguous-input handling. Must be calibrated against human-labeled examples; ideally judged by a different model than the one being evaluated (avoid self-preference). |
| Human-review eval | Human evaluator scores against a rubric. Slowest, most expensive, least scalable. Reserve for high-stakes/novel behaviors neither code nor a calibrated judge can trust, and for calibrating the judge itself. |
| The grading ladder | Reach for the cheapest reliable method first: code-based, then LLM-as-judge (with rubrics, constrained verdicts, calibration, cross-model judging), then human grading as last resort. Favor volume over perfection — many cheap gradable cases beat a few painstaking manual ones. |
| Judge calibration | An uncalibrated LLM judge produces confident scores that may not track quality — worse than no automated grade because it looks trustworthy. Calibrate by running the judge against human-labeled outputs and confirming agreement is high enough to trust. |
| Success-criteria conversion | Turn a vague business requirement ("summarize accurately") into a measurable spec: identify the behavior specifically, set numeric thresholds sourced from the business (not from what the prototype already achieves), identify failure modes as dataset categories, and include adversarial/edge-case inputs. |
| Evals as change gate | Every production change (model swap, prompt revision, context strategy, retrieval config) should run the eval suite before shipping. Multi-turn evals are a separate category (own golden dataset of full transcripts) — they check context retention, no invented details on follow-ups, and quality holding over a longer conversation. Stale eval sets that don't track prompt changes give false confidence — the highest-risk moment is when evals exist but are out of date. |
| POC-to-production gap | Four dimensions invisible in a demo: cost (low-volume POC bill != production bill), latency (single-request demo latency != p95 under concurrent load), reliability (no retry/fallback/circuit breaker in a POC), and failure modes (demo only sees expected inputs). A POC also gives an early read on business-metric impact — capture that on the POC sample, separately from cost modeling. |
| Cost/latency modeling inputs | Call volume + token budget per request (input + output, modeled as a distribution not an average — long-tail requests can be 2-3x the average-based estimate) + model tier. p95 latency is the design target, not the median, since SLA breaches come from the slow tail. |
| Prompt caching | Most effective lever when the system prompt is long and stable. Requires explicit `cache_control` markers. Cache reads are billed far below standard input rate (e.g., ~10% in the course's illustrative figure — verify current rate on the pricing page); cache writes cost more than standard input. Default cache TTL is 5 minutes — workloads with request frequency below the TTL won't realize consistent savings. Risk: a stale cache creates a consistency window if the cached content needs to reflect live state. |
| Batch API | Can offer a large price reduction (illustrative ~50% in the course) relative to standard API pricing for workloads where the SLA permits asynchronous processing, with limits on requests per batch (illustrative up to 100,000 — verify current limits). For regulated workloads, verify batch processing is covered under the BAA/compliance configuration before routing governed data through it. |
| Reliability controls and their layer | Exponential backoff for transient errors (429/timeout/5xx) sits close to the API call. Circuit breakers (trip on error-rate threshold, fail fast rather than time out) sit at the service boundary. Fallback chains (route to alternate model/cached response, never raise a raw error to the user) sit in the orchestration layer. Wrong layer = wrong part of the system protected. |
| Failure modes by architecture type | Agent: unbounded tool use/growing context — mitigate with per-turn token budgets, max tool-call counts, stopping criteria, minimal tool set, eval the stopping behavior. RAG: retrieval quality drift from unindexed changes or staleness — monitor precision/recall as system metrics, separate live-state from static queries. Document pipeline (evaluator-optimizer): no exception path for low-confidence extraction — add confidence scoring and route low-confidence cases to human review. Orchestrator-workers: blurred failure boundaries and fragmented traces — define recoverable (subagent) vs. unrecoverable (orchestrator) failures, use a shared trace ID, reconcile coverage at synthesis. |
| Model version pinning | An operational discipline that applies across every architecture type: pin model versions in config, monitor the deprecation page, maintain a version-update runbook. |
| Sizing a use case | Four inputs: call volume (from the business owner, not intuition or a sample dataset), token budget per request (model the distribution), model tier, sensitivity parameters. Project monthly cost by multiplying volume x tokens x rate for input and output separately (they're priced differently), applying the cache read rate to cached tokens, and comparing to the cost ceiling before writing code. Run sensitivity analysis on volume and token-distribution assumptions. |
| Scoping sequence | Business requirement to capability list (name each capability separately and its owner) to architecture sketch (which capabilities does Claude own vs. existing systems vs. human-in-the-loop) to boundary conditions (state where the architecture works and where it doesn't) to SOW (boundary conditions become the documented scope). |
| Four AI properties (feasibility lens) | Next-token prediction: probabilistic tasks (classification, summarization, drafting) vs. tasks needing precision on specific values (extraction of authoritative values) — compensate with generator-verifier loops, code-based evals, tool calls. Knowledge: rare/contested/recent/domain-specific info not in training data — compensate with RAG for stable knowledge, tool calls for live-state data, uncertainty flagging. Working memory: inputs that exceed the context window in aggregate — compensate with chunking, progressive loading, cross-turn summarization, pipeline architecture. Steerability: abstract/ambiguous instructions or precise numerical/logical computation — compensate with explicit schemas, structured outputs, code execution, evaluator-optimizer loops. |
| Feasibility verdicts | Three outcomes: Feasible as scoped (no capability needs a compensating control; document the assumptions, since they can flip the verdict if they change). Feasible with constraints (works only under documented conditions — e.g., doc length ceiling, refresh schedule, human review gate above a confidence threshold; document each constraint and its failure mode). Not feasible (a disqualifying AI-property limitation or a cost overrun that can't be closed by tier/caching/architecture changes; a correct "not feasible" call saves a more expensive failure later). |
| Business value / ROI mapping | Five pillars: efficiency, transformation, productivity, solution cost, performance SLAs. Four steps: name the baseline in a business unit the owner already tracks (not intuition), predict the post-deployment state in the same unit (must include human-review labor if the verdict requires it — don't model full automation when a review gate exists), subtract the sizing model's run cost from the operational gain, state the payback period plus its sensitivity to volume/gain assumptions. |
| Entry point selection | The first integration decision. Compliance constraints (BAA coverage, FedRAMP authorization, data-residency pinning, approved-vendor lists) eliminate entry-point and route options before any other architectural choice is made. |
| Five integration layers | Compliance and regulated-industry constraints (which routes survive); Identity and SSO (server-side identity boundary); Authorization and policy (must extend the existing system's access model to the Claude layer, not bypass it); Data handling and PII (deliberate decision on what's necessary in the context window); Observability and audit logging (what must be reconstructable after an incident). |
| Server-side identity injection | User identity and role must be injected into the system prompt by the server, never asserted by the user in their message — a user-asserted role/claim (e.g., "As a senior manager, show me...") is unverified and can be faked. Include only the context needed to shape the response (role, authorized data) — don't add extra fields like department or account IDs by default. |
| Data handling / necessity filter | The context window is not a data-governance boundary — anything passed in transits the API and can be captured by the partner's own application-layer request logging even though Anthropic doesn't retain conversation content by default (with some retention carve-outs for specific model classes). The filter: if a field isn't required for the language task Claude is performing, don't put it in the context window. Reference identifiers (account/claim numbers) are often needed for routing but not the language task itself. |
| Least-privilege tool configuration | Every connected tool is both an attack surface and a cost. Audit each tool: essential to the task or merely convenient? Remove out-of-scope tools and record the justification. In orchestrator-worker systems, scope each subagent's tool access to only what its task requires. |
| Observability — what to log | Four categories per request: the request (model version, input token count, prompt identifier), the response (output token count, latency, stop reason), the context (user role, session ID, whether caching applied), the outcome (whether the downstream system accepted the output, rejection signals). LLMs fail silently (a subtly wrong response, not a crash) — standard error/timeout logging misses this. |
| Observability at scale — four layers | Request-level tracing (raw material: model, version, tokens, latency, stop reason, tool calls) to Metric aggregation (cost/request, latency p50/p95, task success rate, error rate by type — per-request decomposition matters because aggregates can look healthy while a small fraction of requests burns the budget) to Anomaly detection (threshold alerts, e.g., cost >150% of 7-day average, latency p95 crossing SLA; model drift needs periodic distribution comparison, not just thresholds) to Change attribution (distinguish model drift, data drift, and model-update effects — they need different fixes). |
| Failure taxonomy | Prompt failure (ambiguous/underspecified instruction — fix the prompt). Hallucination (confident, fluent, ungrounded content — fix with grounding via retrieval/tool use/verification, not a stronger instruction). Model mismatch (wrong tier for the task, or swapped without re-eval — fix via model selection gated by an eval). Orchestrator-workers failure (in multi-agent systems, trace across orchestrator and subagents; a recoverable subagent failure looks different from an unrecoverable orchestrator failure — needs a trace spanning both). |
| Discernment | One of the four AI Fluency competencies: the discipline of judging output quality rather than accepting it at face value. In production, it means classifying each output as acceptable / needs revision / needs override and feeding that judgment back into evals and monitoring. |
| Business-to-technical metric translation | The people funding the deployment read a business KPI dashboard (e.g., handle time, first-contact resolution, CSAT), not the request trace. Build the translation layer mapping technical metrics (latency, task success rate, error rate) to those business metrics at design time — reconstructing it retroactively at the first business review is much harder. |
| Structured A/B testing | Needs a specific, falsifiable hypothesis (names the treatment, metric, and threshold — "the new prompt is better" fails); random, session-consistent treatment/control assignment; a single primary metric chosen before the experiment runs (choosing after seeing results is outcome-shopping); and a sample size sized to the minimum detectable effect and baseline variance (LLM output variance is higher than deterministic systems, so required samples are larger). |
| Reading A/B results without overclaiming | Statistical significance (unlikely due to chance) is a separate question from practical significance (large enough to justify the operational cost of maintaining a new version). Also check whether any secondary metric degraded, and whether the treatment might interact with input types not well represented in the test window (a change that helps typical inputs can hurt rare-but-important edge cases like seasonal spikes). |
| Live A/B test vs. shadow testing | Live A/B test: send real users to the new version — use when the deployment can absorb a small bounded exposure and traffic is high enough to reach significance in a reasonable window; captures downstream signals like whether the user accepted the answer. Shadow testing: run the new version in parallel on a copy of live traffic, log its output, serve everyone the current version, score offline — use when a single bad output is too risky or traffic is too low for a live split; loses downstream user-behavior signal, relies on an offline rubric/golden answers. Often the only acceptable validation method for regulated deployments where exposing users to an unvalidated change isn't permissible. |
| Underpowered / uncontrolled experiments | A small sample (e.g., 50 vs. 50 sessions) cannot distinguish signal from noise on a moderate effect size; uncontrolled input-distribution assignment across groups can make an apparent win an artifact of which inputs landed where; and choosing the primary metric after seeing results turns a test into confirmation-seeking rather than evidence. |
| Experiment-design plane | Two axes — expected effect size and required confidence — determine experimental posture and minimum sample size. Low-stakes/small-effect changes can tolerate a lighter test; high-stakes domains (e.g., medical) or large-effect claims need high confidence and a properly powered test regardless of how "obvious" the win looks. |

## Decision Rules

- If a behavior can be checked deterministically (schema, regex, exact match, length), use a code-based eval — never spend a judge-model call on it.
- If a behavior requires interpretation (tone, reasoning quality, edge-case appropriateness), use a calibrated LLM judge with a rubric and constrained verdicts, ideally graded by a different model than the one under test.
- If a behavior is high-stakes or novel and neither code nor a calibrated judge can be trusted, use human review — and use it to calibrate the judge for future runs.
- If you change the prompt, retrieval strategy, or model, re-run and, if the underlying behavior changed, update the golden dataset before trusting the eval result.
- If you are estimating production cost, model the token distribution (not the average) and use p95 latency (not the median) as the design target.
- If the system prompt is long and stable and reused frequently (faster than the cache TTL), turn on prompt caching; if content must reflect live state, treat caching as a consistency risk.
- If reliability controls are needed, place retries at the API call, circuit breakers at the service boundary, and fallback chains in the orchestration layer — never in the wrong layer.
- If sizing a use case, get call volume from the business owner, not from a sample dataset or developer intuition.
- If a business owner asks for a feasibility verdict, gather volume, latency, and input-size constraints before answering — capability alone is not a verdict.
- If identity or role must be reflected in the prompt, inject it server-side from the auth layer — never trust a role the user asserts in their own message.
- If a data field is not required for the language task Claude is performing, keep it out of the context window — pass a reference identifier instead of the full sensitive record when routing is all that's needed.
- If a system is multi-tenant, issue separate API keys per tenant for cost attribution and rate-limit isolation — never share one key across tenants.
- If you are about to connect a tool, ask whether it's essential or merely convenient; remove what isn't essential and record why.
- If you are running an A/B test, pre-specify the hypothesis, the single primary metric, and the required sample size before looking at any data.
- If a single bad output carries high risk or traffic is too low for a live split, use shadow testing instead of a live A/B test.
- If a metric moves, classify the failure type (prompt failure, hallucination, model mismatch, or orchestrator/subagent failure) before choosing a fix — the four types have different remedies.
- If a production Claude system is agentic, treat observability as a precondition for approving autonomous action, not an add-on — an unlogged agentic action is, to a security reviewer, one that cannot be allowed.

## Anti-Patterns

- Testing manually against a handful of familiar examples and declaring the system "production ready" without a representative golden dataset.
- Leaving an eval suite in place after a prompt or behavior change without updating the golden dataset — it keeps "passing" while measuring a system that no longer exists.
- Sizing production cost and latency from POC-level traffic and clean inputs instead of modeling production volume and the real token distribution.
- Shipping an architecture with no retry logic, fallback chain, or circuit breaker because "the demo never failed."
- Issuing a feasibility verdict before gathering call volume, latency requirement, and input size from the business owner.
- Passing PII/PHI fields into the prompt because they were convenient to include, rather than filtering to only what the language task requires.
- Letting a user assert their own role or permissions inside their message and trusting it instead of injecting identity server-side.
- Using a shared API key across all tenants in a multi-tenant deployment.
- Adding observability instrumentation only after the first production incident instead of designing it in from the start.
- Reporting a 50-session (or similarly small) comparison as a decisive A/B test win, especially when the primary metric was chosen after seeing which one moved.
- Modeling ROI as if a human-review gate weren't there, overstating labor savings versus what the design actually specifies.
- Treating aggregate observability metrics as sufficient — a small fraction of requests can consume most of the budget or produce wrong outputs while the aggregate dashboard looks healthy.
- Skipping the business-to-technical metric translation layer until the first business review forces a retrospective reconstruction.

## Scenario Traps

- Trap: "The demo works, so the system is production-ready." Better: a POC establishes capability, not cost, reliability, or failure-mode coverage at production volume — all three require separate design work.
- Trap: "The eval suite passed, so the change is safe." Better: check whether the golden dataset was updated for the new behavior — a stale eval suite gives false confidence and is the highest-risk moment for a regression.
- Trap: "This is a capability question, so I can confirm feasibility right away." Better: gather volume, latency, and input-size constraints first; "technically feasible" without constraints applied at scale is meaningless.
- Trap: "The connected data source means Claude can see everything in it." Better: Claude only accesses what the authenticated user's identity and the connector's granted scope allow — and that identity must be injected server-side, never trusted from the user's message.
- Trap: "We need this field for context, so pass the whole record into the prompt." Better: apply the necessity filter — pass only what the language task requires; use a reference identifier for routing instead of the full sensitive record.
- Trap: "A 6-point lift over 50 sessions each is a clear winner." Better: with high output variance, a difference that size at that sample size is well within the noise floor; check sample size, input-distribution balance, and whether the metric was pre-specified.
- Trap: "The most capable model tier is always the safest choice." Better: model tier should be chosen against the cost ceiling and latency target for the specific task — Opus is not automatically the right lever for meeting a cost/latency ceiling (per the calculator exercise, caching the stable system prompt did the real work).
- Trap: "A statistically significant result means we should ship it." Better: statistical significance and practical significance (worth the operational cost, no secondary-metric regression) are separate questions.
- Trap: "We can't test this change live because it's risky, so we just won't test it." Better: use shadow testing to validate against real traffic without exposing users to the new version.
- Trap: "The ROI case should assume full automation once Claude is deployed." Better: if the design specifies a human-review gate, the ROI projection must include that remaining labor cost, not model it as eliminated.

## Memorization Cues

- Eval grading ladder: code first, judge second (calibrated, rubric-based, cross-model), human last.
- Eval workflow: Define, Build (golden dataset), Check, Judge, Interpret.
- POC-to-prod gap has four invisible dimensions: cost, latency, reliability, failure modes.
- Sizing inputs: volume, token budget (as a distribution), model tier, sensitivity.
- Reliability control placement: retries at the call, circuit breakers at the boundary, fallbacks in orchestration.
- Feasibility verdicts: feasible as scoped / feasible with constraints / not feasible — always name the load-bearing constraint.
- Five integration layers: compliance, identity, authorization, data handling, observability — in that order.
- Necessity filter for PII: if the language task doesn't need it, it doesn't go in the context window.
- Observability logs four things: request, response, context, outcome.
- Failure taxonomy: prompt failure, hallucination, model mismatch, orchestrator-workers failure — each has a different fix.
- A/B test must-haves: hypothesis, random consistent assignment, one pre-specified primary metric, adequate sample size.
- Live A/B vs. shadow: live tests real user exposure at volume; shadow tests real traffic with zero user exposure, scored offline.
- p95, not the median, is the latency design target.

## Source References

- Module Introduction / Orientation: module scope — evals, POC-to-prod, sizing/feasibility, integration patterns, A/B testing/observability.
- Evals as acceptance criteria: eval definition, workflow stages, code-based vs. model-based vs. human-review evals, the grading ladder, judge calibration, success-criteria conversion, evals as a change gate, multi-turn evals.
- Watch Out — The eval suite that measured the wrong thing: composite postmortem on a non-representative, stale golden dataset in a contract review assistant.
- Checkpoint — Sort the eval types: eight example behaviors sorted into code-based vs. model-based evals.
- From POC to production: cost, latency, reliability, and failure modes across architecture types (agent, RAG, document pipeline, orchestrator-workers); prompt caching mechanics; reliability control placement; model version pinning.
- Watch Out — The demo cost profile that became the production bill: composite post-launch review on unscaled POC cost estimates, skewed token distribution, and untested failure handling.
- Checkpoint — Cost & reliability calculator: interactive scenario (50,000 req/month customer service agent) exploring model tier, caching, max_tokens, and volume against a cost ceiling and latency target.
- Use-case sizing and feasibility: sizing steps (volume, token budget, cost projection, sensitivity analysis), scoping sequence (capability list to architecture sketch to boundary conditions to SOW), the four AI properties as a feasibility lens, the three feasibility verdicts, business value/ROI mapping (five pillars, four-step mapping, common ROI errors).
- Watch Out — The scoping call that skipped the constraints: dialogue-style example of a feasibility verdict issued before volume/size/latency constraints were gathered.
- Checkpoint — Justify the feasibility call: three scenarios (research assistant, delay predictor, real-time trading recommendations) each requiring a verdict plus its load-bearing constraint.
- Enterprise integration patterns: entry point selection, compliance-first elimination logic, the five integration layers, least-privilege tool configuration, server-side identity injection, data handling/necessity filter, what to log for observability.
- Watch Out — The PII field that went straight into the prompt: composite trace from a healthcare-adjacent deployment where SSN and Insurance ID landed in application-layer request logs.
- Checkpoint — Critique the integration diagram: multi-tenant SaaS customer-service deployment diagram; identify which components are integration problems (shared API key, message-asserted premium status, account number/email in logs, no logging before the downstream CRM) versus sound components (server-side auth, per-tenant storage isolation).
- A/B testing and observability at scale: structured A/B test components, reading results without overclaiming, shadow testing, the four-layer observability model, the failure taxonomy, Discernment, business-to-technical metric translation.
- Watch Out — The 50-session winner that wasn't: composite example of an underpowered, uncontrolled, post-hoc-metric-selected comparison that reversed after full deployment.
- Checkpoint — Place on the experiment-design plane: five scenarios placed by expected effect size and required confidence.
- Exercise — Define the evaluation framework: insurance-claims case study (accuracy, latency, safety, security, cost dimensions); the reveal-model-answer content was not captured in this transcript.
- Glossary: term list only (5xx errors, BAA, caching, circuit breaker, data-residency pinning, DPA, eval, exponential backoff, GDPR, generator-verifier loop, hallucination rate, live state, median latency, p95, PHI, RAG, rate limit, regex, schema, SSO, structured fields, timeout, tool use, transient error) — definitions were not expanded in the capture.
- Recap — Five takeaways: evals as acceptance criteria, POC to production, use-case sizing and feasibility, enterprise integration patterns, A/B testing and observability — condensed as one-line action items each.
- Module Complete screen: confirms this is Module 2 of 5 in the Architect Professional path (M1: Claude Platform & Solution Design [completed]; M2: this module; M3: Responsible AI, Safety & Risk [up next]; M4: Stakeholder Engagement, Lifecycle & Go-to-Market; M5: Team Enablement and Operational Productivity).

## Gaps / Follow-Up

- The Exercise (screen 17, "Define the evaluation framework") model answer was not present in this capture — no "Screen 18" content exists in the transcript. Follow up by revisiting the course directly to capture the graded model answer for the insurance-claims eval framework.
- The Glossary (screen 19) captured only term names, not their expanded definitions (5xx errors, BAA, DPA, generator-verifier loop, live state, transient error, etc.) — the click-to-expand definitions were not present in the scrape.
- The "Entry points" table (which of the five entry points applies when, and their flexibility/maintenance tradeoffs) and the "Constraint-to-integration matrix" (which integration pattern satisfies which regulatory constraint) were referenced by the course but their table contents were not captured in this transcript — only the surrounding narrative survived.
- RAG chunking and indexing strategy design, and retrieval-strategy selection by data shape/query pattern (D3 topics per the exam blueprint), are not covered here beyond "retrieval quality drift" as a failure mode — likely covered in a different module or the underlying Claude API course.
- MCP-specific integration design (tool schemas, structured errors, progressive discovery vs. monolithic context) is named as an entry-point option but not built out in this module — study separately.
- Broader guardrail design, ethical AI frameworks, and human-in-the-loop validation as a general governance pattern (beyond the specific low-confidence-routing and compliance-elimination examples here) are flagged by the course itself as Module 3 content (Responsible AI, Safety & Risk).
- Stakeholder communication technique and lifecycle management beyond the sizing/scoping/ROI artifacts here are flagged as Module 4 content.
- Team tooling and operational enablement content is flagged as Module 5 content and is entirely absent from this module.
