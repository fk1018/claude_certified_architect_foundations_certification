# Responsible AI, Safety & Risk for Architects

- Source URL: https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional
- Completed: 2026-09-03
- Study pack: `study_packs_architect_professional/responsible-ai-safety-risk-for-architects/`

## Captured Sections

- Module Introduction: Orientation (the safety stack: who owns each layer, and what happens when one fails)
- Alignment: Model training vs your layer
- Alignment: Watch Out — trained refusals mistaken for a domain policy
- Alignment: Checkpoint — Sort the responsibility
- Guardrails: Risks, limitations, and failure modes of LLM systems
- Guardrails: Checkpoint — Assess the risks in a proposed architecture
- Guardrails: Placing screening and authorization so the system degrades safely
- Guardrails: Watch Out — when a single output filter looks like a finished design
- Guardrails: Checkpoint — Place the controls on the path
- Fairness: Where unequal outcomes enter, and what the system must explain
- Fairness: Watch Out — when fairness is treated as the model provider's problem
- Fairness: Checkpoint — Critique the decision-logging design
- Review routing: Routing decisions to people by stakes, not by volume
- Review routing: Watch Out — when routing everything to review makes review meaningless
- Review routing: Checkpoint — Build the review-routing rule
- Compliance: Turning each compliance obligation into a control with evidence
- Compliance: Watch Out — when passing entry point selection feels like finishing compliance
- Compliance: Checkpoint — Justify the control choice
- Wrap-up: Cumulative exercise — Assemble a responsible deployment (public-sector benefits assistant brief)
- Wrap-up: Glossary
- Wrap-up: Recap — five things that hold across everything in the module
- Module Complete (Module 3 of 5 in the Architect Professional path)

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| D1: Solution Design & Architecture | None | Module does not teach architectural patterns, multi-agent orchestration, or decomposition. It assumes architecture and model selection were already decided (M1/M2) and layers safety controls on top. |
| D2: Claude Models, Prompting & Context Engineering | None | System prompts appear only as one alignment layer ("system-prompt instruction") with the explicit caveat that instructions are not enforcement. No prompting technique, model selection, or context/token optimization content. |
| D3: Integration | Medium | Covers where guardrails sit on the request/tool-call path, RAG-specific indirect prompt injection via retrieved content, tool-call authorization before side-effecting actions, and skill supply-chain security (sandboxing, least privilege, trusted sources). Does not cover retrieval strategy design, connection protocols, or progressive discovery. |
| D4: Evaluation, Testing & Optimization | None | No eval metrics, test frameworks, A/B testing, or latency/cost optimization content beyond a brief cost/complexity/risk callout per section. |
| D5: Governance, Safety & Risk Management | High | This is the core of the module: the alignment boundary (trained behavior vs application layer), guardrail placement (input screening, output screening, tool-call authorization), fail-open vs fail-closed design, LLM risk categories (prompt injection direct/indirect, token-budget exhaustion, tool/action abuse, data exposure), fairness injection points, decision logging/explainability, human-in-the-loop review routing by stakes, and compliance obligation-to-control-to-evidence mapping (HIPAA, GDPR, FedRAMP, BAA, data residency). |
| D6: Stakeholder Communication & Lifecycle Management | Low | Only touched at the boundary: the module explicitly hands off to Module 4 ("Stakeholder Engagement, Lifecycle & Go-to-Market"), noting the control register and layered boundary become the documentation baseline for that handoff. No discovery, requirements-gathering, or SLA content here. |
| D7: Developer Productivity & Operational Enablement | None | Not covered; that is Module 5 ("Team Enablement and Operational Productivity") in this track. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| The four-layer safety stack | Trained behavior (Anthropic-owned, broad harm reduction) → system-prompt instruction (Architect-owned, steers but does not enforce) → runtime screening (Architect-owned, detects disallowed content) → authorization (Architect-owned, gates side-effecting actions). Each layer covers something the one below cannot, and each fails in a way the next layer must catch. |
| Anthropic's constitution | A written document (most recent published version January 2026) that shapes training via example generation and response ranking. Sets a holistic (not strictly sequential) priority order: be broadly safe, be ethical, comply with guidelines, be genuinely helpful. It reduces broad classes of harmful output but has no knowledge of any specific deployment's domain policy, data rules, or authorization model. |
| Training-time alignment vs inference-time control | Training-time alignment is general by design, set before any deployment exists, and lowers baseline risk. Inference-time control (system instructions + runtime guardrails: screening, authorization, review) enforces deployment-specific rules. System instructions alone are not enforcement — they must be paired with runtime controls. |
| The "silent failure" of assumed coverage | The single most dangerous failure mode: assuming Claude's training enforces a rule it was never given (e.g., a partner's cross-business-unit data isolation policy). Because the rule doesn't exist in any layer, nothing prevents the violation, and it surfaces as an in-domain request that looks harmless in general terms. |
| LLM system risk categories | Direct prompt injection (user input overrides system instructions). Indirect prompt injection (malicious instructions arrive via retrieved content or tool outputs the model treats as trusted — the dominant injection vector in enterprise RAG/tool-use deployments). Token-budget exhaustion (oversized/padded input consumes context or output budget, truncating work or inflating cost). Tool and action abuse (model induced to call a side-effecting tool outside policy). Data exposure (sensitive fields enter context window or logs independent of model behavior). |
| System vulnerability walk | Walk request and data paths together: user input, retrieved content, tool outputs, model output, and logs. At each entry point ask what an adversary could do and which control stands in the way; flag any point with no control. |
| Risk assessment as a deliverable | For each identified risk: record category, affected component, likelihood-and-impact judgment, and the mitigation control with an owner and an evidence artifact. This is what a security reviewer signs off on. |
| Three guardrail decision points | Input screening (before the model call — decides if the request reaches the model). Output screening (before the response reaches the user — decides if the model's output is safe to return). Tool-call authorization (before any side-effecting action — decides if this caller may perform this action in this context). Each sits at a different point and checks a different thing; a control at one point does nothing for the others. |
| Model-based vs deterministic checks | Model-based fits ambiguous intent (jailbreak/injection detection, toxicity/policy-compliance judging) — flexible but evadable by adversarial phrasing. Deterministic fits clear, definable rules (blocklist, regex, length/format check, allowlist) — fast and auditable but brittle/over-blocks. Tool-call authorization should almost always be deterministic because it must be provable and replayable. Because neither type catches everything, chain them in series so each one's blind spot is covered by a different control. |
| Refusal handling via the Messages API | `stop_reason: "refusal"` (available since Claude Opus 4.7) carries a `stop_details` object with a policy category and explanation; both are null when the refusal doesn't map to a named category. Known categories as of course publication: cyber, bio, frontier_llm, reasoning_extraction (verify current list at platform.claude.com — subject to change). Models without `stop_details` need a fallback path. Rule: reset the conversation context after a refusal (remove/rephrase the triggering turn or clear history) — resending on the same refused context returns further refusals. |
| Fail open vs fail closed | When an operator-built guardrail errors or is unreachable, it must explicitly fail open (pass traffic through unscreened) or fail closed (block until healthy). The default, if not chosen explicitly, is almost always fail open — the surrounding code decides for you. A guardrail that fails open silently is worse than no guardrail because it gives the appearance of protection with none of the function. This applies only to operator-built components — Anthropic's built-in model safety controls are not operator-configurable and do not fail open. |
| Indirect injection via retrieval/tools (second injection vector) | User-input screening only catches instructions the user sends directly. In RAG, a malicious instruction embedded in a retrieved document reaches the model after input screening already passed. In agentic systems, a tool response can carry instructions the model treats as authoritative. Requires a separate control: screen retrieved content and tool outputs before they're appended to context, using the same model-based classifier applied to user input. |
| The full guarded request path | User request → input screening (fail closed) → model call → output screening (fail closed) → tool-call authorization (deterministic allowlist + identity/scope) before any side-effecting action → response to user. Every blocked or failed gate is logged so an incident can be reconstructed. |
| Skill supply-chain security | Skills are reusable, distributable code + instructions — a supply-chain risk because an untrusted skill can carry a code-execution exploit that input/output filters can't see (the threat is baked into the bundle, not the conversation). Two-part defense: (1) audit before trust — read the bundle for anomalous calls (network, shell, filesystem, credentials) and out-of-scope operations against the skill's stated purpose; (2) runtime confinement — run with least privilege, sandboxed, limited file/network access, no standing credentials, because a clean audit can still miss code fetched at runtime. Also apply a trusted-source policy (vetted internal registry, verified publishers, signed releases) to shrink the audit surface. Never assume the platform screens skills for you — verify what vetting actually exists. Every audit ends in a recorded verdict: approve, reject, or remediate (fix, sandbox, pin version, re-audit). |
| Fairness as an architectural property | Fairness is not a single model attribute — it enters at four identifiable, inspectable injection points: (1) the retrieval corpus (over/under-representation skews what the model sees), (2) prompt framing (encoded assumptions push outcomes one direction), (3) few-shot examples (can carry the same skew as the corpus), (4) downstream routing (what happens to output after it's produced can route groups differently). |
| Three audiences for explainability | An affected user needs a clear explanation of why a decision was made, in actionable terms — requires capturing the inputs and reason in digestible form. A regulator needs evidence of consistent treatment and reconstructability on demand — requires a durable, queryable record of inputs/outputs/decision path. Your build team needs enough detail to diagnose a flagged decision — requires the full trace (prompt, retrieved context, model output, every routing step) tied to existing observability. |
| Decision logging | To replay/explain a single decision, capture the inputs, retrieved context, model output, and routing path — the same observability instrumentation used for system health, now applied to answering "why did this decision happen" rather than "is the system healthy." Retention and query path differ from health monitoring. |
| Fairness-and-transparency checklist | For each of the four injection points: is it instrumented? For an adverse decision: can you produce the inputs and an actionable reason? For a regulator: can you query the log to show comparable cases were treated comparably? For your team: can you pull the full trace for any flagged decision? A "no" anywhere is a design gap. |
| Discernment (AI Fluency competency) | One of four AI Fluency competencies: evaluating AI outputs and behaviors — judging whether an output is acceptable, needs revision, or needs override, rather than only confirming a value was produced. Applied to fairness, it's what lets a reviewer recognize a skewed/unjustified outcome instead of just rubber-stamping a result. |
| Decision logs are themselves compliance-in-scope | In HIPAA/GDPR contexts, logged inputs and retrieved context contain sensitive personal data. Apply minimization, retention limits, and access controls to the log itself, and register it as a named control. Logging for transparency and pinning data for compliance use the same log, governed differently — they are not in conflict. |
| Stakes = reversibility x cost of a wrong decision | Reversibility (how easily a wrong decision can be undone) and cost of a wrong decision (what the mistake causes if uncorrected) together set the stakes, independent of how the system reached the decision. |
| Confidence as a routing multiplier, not a stakes-setter | Confidence is the system's own (ideally calibrated) score about its output. It does not change the stakes of a decision — it estimates how likely this output is wrong, which tells you how much of that stakes-defined volume to route to a person. Rule: route to a person when low-confidence AND (irreversible OR high-cost); let confident + reversible + low-cost decisions through automatically. When cost/reversibility and confidence disagree, weight cost and reversibility more heavily, since they determine the consequences of a mistake. |
| Human placement tradeoff | Pre-action approval: nothing irreversible happens unreviewed, but adds latency to every routed decision and doesn't scale to high volume. Post-action audit: throughput stays high, but a wrong action has already taken effect — suits only reversible, lower-cost decisions. Sampled review: monitors quality without slowing the process, but a bad decision can slip through unsampled — monitors the system rather than guarding individual outcomes. |
| What the reviewer must see | Three things: the inputs that drove the decision, the model's output, and the reason it was flagged. Without the reason, a reviewer can't distinguish an edge case from routine traffic; without the inputs, they can't judge correctness. |
| Consent fatigue and checkpoint design | Anthropic's agent-autonomy research found requiring sign-off on every action adds friction without meaningful safety gain; a better pattern is monitoring with intervention at higher-value checkpoints (e.g., plan review or exception handling) rather than per-step approval — this is why Claude Code moved to plan-level review instead of per-step approval. Consent fatigue is when reviewers, faced with too many approval requests, start clicking through without reading, degrading review quality. |
| Diligence (AI Fluency competency) | One of four AI Fluency competencies: ensuring responsible AI collaboration — maintaining explicit human accountability checkpoints, recognizing when automation pressure erodes oversight, and auditing workflows for gaps where AI acts without review as automation scales. |
| Agent checkpoint pattern | For agent workflows, the routing rule becomes a gate that pauses execution for human review based on task risk and reversibility: place a gate before irreversible/high-stakes autonomous actions, and sample lower-stakes actions instead of gating each one. |
| Compliance obligation → control → owner → evidence | Regulatory frameworks (GDPR, HIPAA, FedRAMP) state outcomes, not implementations — they leave the technical control to you. Each surviving obligation (after using it as an entry-point/route pre-filter) must become three things you own: a specific technical control that achieves the outcome, a named accountable owner, and a living evidence artifact a reviewer can inspect (a signed agreement, a configuration screen, an authorization record, a returned log query). A design document naming a control with no owner and no evidence is not accepted as proof. |
| Training-use vs retention are distinct claims | Do not collapse them: data can be excluded from model training by default while still being retained or monitored for logging, abuse prevention, legal compliance, or configured audit purposes. |
| Compliant entry point is a prerequisite, not proof | Passing the constraint pre-filter (choosing a route/entry point that survives HIPAA/GDPR/FedRAMP) is visible and immediate at design time. Proving each obligation is actually met in production is invisible at design time — it requires a living, revalidated evidence artifact, because configurations drift (e.g., a logging change silently routes metadata to the wrong region) and nothing catches the gap until an audit asks for proof. |
| Glossary terms from the module | BAA (Business Associate Agreement), consent fatigue, constitution, control register, data residency, decision logging, evidence artifact, fail open vs fail closed, FedRAMP, GDPR, HIPAA, human-in-the-loop routing, injection point (fairness), input screening, judge model, output screening, tool-call authorization, training-time alignment vs inference-time control. |

## Decision Rules

- If a rule or policy is specific to your partner/domain (data handling, authorization model, approved script), assume it is NOT enforced by trained alignment — build it explicitly into system prompts, screening, or authorization.
- If you are placing a single guardrail, place it at only one of three points (input, output, or tool-call authorization) at your own risk — one filter covers only what it checks; use all three when the path includes retrieval or side-effecting tools.
- If a check's rule is clear, bounded, and definable (blocklist, regex, schema, allowlist), use a deterministic check. If intent is ambiguous or you're judging language quality (jailbreak detection, toxicity), use a model-based check. Chain both where risk warrants it, since neither catches everything alone.
- If a decision authorizes a side-effecting action, make the check deterministic — authorization must be provable and replayable, so avoid model-based judgment there.
- If a guardrail you built can error or go unreachable, explicitly choose fail closed for consequential checks; do not let the default (fail open) decide for you.
- If your system uses RAG or tool use, add a second injection-screening control for retrieved content and tool outputs before they enter context — user-input screening does not cover this vector.
- If you receive `stop_reason: "refusal"` from the API, read the `stop_details` category to route different refusal classes differently, and reset the conversation context (remove/rephrase the triggering turn or clear history) before continuing.
- If you are integrating a Skill, audit the bundle for anomalous or out-of-scope calls before trusting it, run it sandboxed with least privilege regardless of audit outcome, and prefer a trusted-source/signed-release policy to shrink what needs auditing.
- If you are asked whether fairness is covered, check the four injection points (retrieval corpus, prompt framing, few-shot examples, downstream routing) explicitly rather than assuming the model vendor's bias evaluations cover your deployment.
- If a decision is low-confidence and either irreversible or high-cost, route it to pre-action human review; if it is confident, reversible, and low-cost, let it proceed automatically.
- If cost/reversibility and confidence disagree on routing, weight cost and reversibility more heavily than confidence.
- If you route a decision to a human reviewer, always surface the inputs, the model's output, and the reason it was flagged — an approve button with no context is not a real review.
- If review volume is trending toward "everything," redesign the routing rule by stakes rather than accepting the volume — high review volume with no context is functionally equivalent to no review.
- If you name a compliance obligation and a technical control, also name an accountable owner and produce a living evidence artifact — a control with neither is indistinguishable from a non-operating control at audit time.
- If asked about training use vs data retention for a compliance claim, treat them as two separate claims and verify each independently.

## Anti-Patterns

- Assuming Claude's trained refusals cover a partner-specific data-handling, authorization, or domain policy rule (the "trained refusal mistaken for domain policy" failure).
- Treating a single output filter as a complete guarded path when the most consequential action (a side-effecting tool call) happens upstream of it, unauthorized.
- Letting an operator-built guardrail fail open by default because no explicit fail-open/fail-closed decision was made.
- Screening only direct user input and ignoring instructions embedded in retrieved documents or tool outputs (indirect prompt injection).
- Trusting a Skill because input/output filters didn't flag anything — the exploit can be baked into the bundle itself, invisible to conversation-level screening.
- Treating fairness as solved because "the model passed its bias evaluations" — ignoring that your retrieval corpus, prompt framing, examples, and routing can independently introduce skew.
- Logging only aggregate/dashboard metrics (e.g., overall accuracy) without per-decision, per-subgroup traceability.
- Routing every decision to human review "to be safe" — this floods the queue, collapses review into approval, and buries the genuinely high-stakes items.
- Giving a reviewer only the output and an approve button, with no inputs and no flag reason.
- Requiring sign-off on every agent step instead of gating high-stakes/irreversible actions and sampling the rest — inducing consent fatigue.
- Treating a compliant delivery-route/entry-point choice as proof of compliance, rather than as a prerequisite that still needs a named owner and living evidence per obligation.
- Collapsing "excluded from model training" and "not retained/logged" into a single compliance claim.
- Writing a compliance control into a design document once and never revalidating it as configurations drift.

## Scenario Traps

- Trap: "Claude already refuses harmful prompts in testing, so our partner's data-isolation rule must be covered too." Better: trained refusals cover broad harm categories, not deployment-specific policy — verify the specific rule is enforced in an application-layer control.
- Trap: "We added an output filter, so the path is guarded." Better: a side-effecting tool call that runs before output filtering has already happened by the time the filter looks at the text — you need input screening and tool-call authorization too, not just output screening.
- Trap: "The screening service errored, so we let the request through rather than block a real user." Better: unless you deliberately chose fail-open with the risk understood, a consequential guardrail should fail closed — appearing to work while doing nothing is worse than visibly failing.
- Trap: "Our input classifier passed the request, so nothing in the context is malicious." Better: in RAG/agentic systems, malicious instructions can arrive via retrieved content or tool outputs after input screening already ran — screen those separately.
- Trap: "The model passed Anthropic's bias evaluations, so our system is fair." Better: fairness is architectural — your retrieval corpus, prompt framing, examples, and routing can introduce skew the model provider never tested.
- Trap: "We route every low-confidence output to a human, so we're being careful." Better: confidence alone doesn't set stakes — a low-confidence but reversible, low-cost decision doesn't need pre-action human review, and flooding the queue degrades review quality for everything, including the truly high-stakes cases.
- Trap: "We chose a HIPAA-compliant delivery route, so we're HIPAA compliant." Better: a compliant route is a prerequisite; you still need a named control, an accountable owner, and a living evidence artifact per obligation to prove compliance at audit time.
- Trap: "Data isn't used for model training, so we don't retain or log it." Better: training-use exclusion and data retention are separate claims — verify each independently.
- Trap: "We audited the Skill bundle and it was clean, so it's safe to run with full privileges." Better: a clean audit doesn't guarantee runtime behavior (a skill can fetch code at runtime); always sandbox and run with least privilege regardless of audit outcome.

## Memorization Cues

- Four layers, four owners: Trained behavior (Anthropic) → System-prompt (Architect, steers not enforces) → Runtime screening (Architect, detects) → Authorization (Architect, gates action).
- Three gates, three questions: Input screening — should this reach the model? Output screening — is this safe to return? Tool-call authorization — is this action permitted for this caller now?
- Deterministic for authorization, always — it must be provable and replayable.
- Fail open = looks guarded, isn't. Fail closed = the safe default for consequential checks you build.
- Two injection vectors: direct (user input) and indirect (retrieved content / tool outputs) — screen both.
- Fairness enters at 4 points: corpus, framing, examples, routing.
- Three audiences for explanation: user (actionable reason), regulator (reconstructable/consistent), build team (full trace).
- Stakes = reversibility × cost. Confidence decides how much of that stakes-bucket gets automated, not the stakes itself.
- Reviewer needs 3 things: inputs, output, flag reason.
- Compliance triple: control + owner + evidence artifact. No owner + no evidence = invisible at audit.
- "Trained ≠ your rule" is the single most tested failure mode in this module.

## Source References

- Module Introduction / Orientation: the safety stack framing — four layers, five learning objectives, the module's central postmortem premise (a system that passes review and still fails in production).
- Alignment (Screens 2-4): trained behavior vs application layer, the constitution, training-time alignment vs inference-time control, the "trained refusals" Watch Out, and the Sort the Responsibility checkpoint.
- Guardrails (Screens 5-9): LLM risk categories, system vulnerability walk, risk assessment as a deliverable, guardrail placement (input/output/authorization), model-based vs deterministic decision table, refusal handling via `stop_reason`/`stop_details`, fail open vs fail closed, the full guarded request path, skill supply-chain security, the single-output-filter Watch Out, and the Place the Controls checkpoint.
- Fairness (Screens 10-12): four fairness injection points, three explainability audiences, decision logging, the fairness-as-vendor's-problem Watch Out, and the Critique the Decision-Logging Design checkpoint.
- Review routing (Screens 13-15): stakes (reversibility × cost) vs confidence, human placement tradeoffs (pre-action, post-action, sampled), what the reviewer needs to see, consent fatigue and Anthropic's agent-autonomy research, the Diligence competency, the routing-everything Watch Out, and the Build the Review-Routing Rule checkpoint.
- Compliance (Screens 16-18): obligation-to-control-owner-evidence mapping, training-use vs retention, the entry-point-selection Watch Out (data residency postmortem), and the Justify the Control Choice checkpoint.
- Wrap-up (Screens 19-22): the cumulative "Assemble a Responsible Deployment" exercise (public-sector benefits assistant under FedRAMP), the glossary, the five-point recap, and the module-complete screen positioning this as Module 3 of 5 in the Architect track (M1 Claude Platform & Solution Design, M2 Enterprise Integration & Production, M3 this module, M4 Stakeholder Engagement/Lifecycle/GTM, M5 Team Enablement and Operational Productivity).

## Gaps / Follow-Up

- This module assumes architecture, model selection, and integration design are already complete (from M1/M2) — study those modules separately for D1/D2/D3 architecture and prompting content.
- Cumulative exercise's full model answer (the assembled five-layer response to the benefits-assistant brief) was not captured verbatim in the source transcript — only the brief and the five decision prompts were; reconstruct or re-capture the model answer if the exam tests that exact scenario in depth.
- The exact current list of `stop_details` refusal categories (cyber, bio, frontier_llm, reasoning_extraction as of course publication) should be re-verified against platform.claude.com/docs before the exam, since the course explicitly flags this as subject to change.
- Anthropic's cited agent-autonomy research (anthropic.com/research/measuring-agent-autonomy and anthropic.com/research/trustworthy-agents) was referenced but not reproduced in detail — read the source papers directly for D5/D1 depth on agent checkpoint design.
- Module 4 (Stakeholder Engagement, Lifecycle & Go-to-Market) is the natural next study pack for D6, since this module explicitly hands off documentation/communication responsibility to it.
- Module 5 (Team Enablement and Operational Productivity) is the natural next study pack for D7, which this module does not touch at all.
