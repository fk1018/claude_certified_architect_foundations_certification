# Stakeholder Engagement, Lifecycle & GTM Practice Questions

## Question 1

Scenario: An architect is on a discovery call for a customer-service assistant. The stakeholder says, "Escalations should feel effortless for the agent." The architect writes "effortless escalation" into the requirements document and moves on to the next topic.

Question: What is the correct next step according to the discovery framework taught in this module?

A. Accept "effortless escalation" as the requirement, since the stakeholder stated it directly.

B. Ask follow-up questions about what would make escalation feel non-effortless, to translate the preference into a testable, bounded constraint.

C. Skip ahead and propose a specific escalation UI design so the stakeholder can react to something concrete.

D. Move the topic to the "must cost" category, since effort usually implies a cost constraint.

Correct answer: B

Explanation: An experience word like "effortless" is a signal that more discovery is needed, not a requirement to record as-is. The architect must ask what would break that experience to surface the underlying testable constraint (e.g., no re-entry of case data, a maximum number of clicks, a defined handoff SLA).

Distractors:
- A: Recording the preference verbatim skips the translation step that turns a preference into something the design can actually be built against.
- C: Proposing a design before finishing discovery is the exact failure shown in the "discovery call that turned into a design session" Watch Out.
- D: "Must cost" is the wrong bucket — effort/experience constraints usually land in "must do" or "must not do," and forcing it into a bucket without asking follow-up questions skips translation entirely.

## Question 2

Scenario: During a discovery call, a stakeholder for a lending platform says, "Loan officers will double-check anything the model flags anyway." The architect notes this as a nice-to-have UI convenience and proceeds to design an automated approval path with no mandatory checkpoint.

Question: What is the most likely mistake in this response, based on the module's Watch Out example?

A. None — automated approval paths are always appropriate once a human "double-checks" is mentioned casually.

B. The architect should have treated "double-checks anything the model flags" as a possible mandatory authorization gate and asked whether review is required before action, not just possible.

C. The architect should have immediately escalated to legal before finishing the call.

D. The architect should have asked only about cost, since lending is primarily a budget-constrained domain.

Correct answer: B

Explanation: This mirrors the hospital discovery Watch Out, where "there's a review step, but it's just a quick check" turned out to be a mandatory clinician-authorization gate. A casually mentioned human check should always be chased down as a potential required architectural gate, not dismissed as a convenience feature.

Distractors:
- A: Treating a mentioned human check as automatically optional is precisely the failure pattern the module warns against.
- C: Escalating to legal mid-call is not the taught response; the taught response is to ask the direct clarifying question during discovery.
- D: Cost is one of four discovery categories, but "must not do" / "must prove" (human authorization, audit obligations) are the relevant categories here, not cost alone.

## Question 3

Scenario: An architect presents a tradeoff to a stakeholder: choosing a smaller, cheaper model tier for a support-ticket triage workflow. The presentation states the smaller model costs 60% less per call and slightly reduces triage accuracy. The stakeholder approves immediately.

Question: What is missing from this tradeoff presentation according to the module's three-element framework?

A. Nothing — cost and accuracy tradeoffs are the only two elements the framework requires.

B. A comparison against every other available model tier in the product line.

C. What it would cost to reverse the decision (e.g., re-tune prompts, re-run evals, and migrate dependent workflows) once the system is built around the smaller model.

D. A guarantee that accuracy will never degrade further after launch.

Correct answer: C

Explanation: The framework requires naming what the choice gains, what it gives up, and what reversal would cost once the system is built around it. This presentation only covers gain (lower cost) and give-up (accuracy), omitting reversal cost — the element the module identifies as most often missing and most likely to change the decision.

Distractors:
- A: The framework explicitly requires three elements, not two; reversal cost is missing.
- B: The framework does not require exhaustively comparing every alternative — it requires clearly presenting the chosen tradeoff's three elements.
- D: Guarantees about future accuracy are not part of the taught framework; the framework is about informed choice given known tradeoffs, not about eliminating uncertainty.

## Question 4

Scenario: A team's proof-of-concept for an internal-tools assistant costs roughly $200/month at pilot volume. The architect tells the stakeholder "this is cheap, don't worry about cost" and does not discuss production-scale volume before launch.

Question: What risk does this most directly create, based on the module's guidance on cost communication?

A. No risk — pilot costs are always representative of production costs.

B. A likely surprise cost increase at production scale, since production volume routinely runs one to two orders of magnitude above pilot volume, turning a trivial pilot cost into a large recurring line.

C. A risk that the model will be deprecated before production launch.

D. A compliance risk, since cost estimates must always be reviewed by legal before launch.

Correct answer: B

Explanation: The module explicitly warns that cost is the expectation that breaks most often after launch because production volume is typically 1-2 orders of magnitude above pilot volume. Architects should pre-empt this with a production-volume consumption forecast and a named spend-control posture before the first invoice.

Distractors:
- A: This is the opposite of the module's guidance — pilot-scale cost is explicitly called out as misleading for production planning.
- C: Model deprecation is not the risk described or discussed in this context.
- D: Legal review of cost estimates is not part of the taught framework; the risk here is a communication/forecasting gap, not a legal one.

## Question 5

Scenario: A deployment's dashboards show latency, error rate, and eval scores updating in real time, with alerts configured for hard thresholds. Three months after launch, a stakeholder complains that output quality has "felt worse for weeks," but no alert had fired and no review had been scheduled during that period.

Question: What is the most likely root cause, according to the module's framing of feedback loops versus observability?

A. The observability stack was not collecting enough data.

B. No governance rule mapped the slow, threshold-missing eval-score drift to a review trigger, so the stack collected the right signal but nothing decided it mattered.

C. The stakeholder's complaint is unreliable and should be dismissed until a hard alert fires.

D. The dashboards should be replaced with a different monitoring vendor.

Correct answer: B

Explanation: This mirrors the "observability stack that replaced the feedback loop" Watch Out: a dashboard collects and displays signals, but a feedback loop is the governance layer that maps a signal (including a slow drift below hard-alert thresholds) to a trigger, owner, and action. Without that governance table row, a real decline can run for weeks undetected.

Distractors:
- A: The data was already being collected (eval score, latency, error rate) — the gap was decision-layer governance, not data collection.
- C: Dismissing stakeholder-reported quality complaints contradicts the module's point that this is exactly the kind of signal a feedback loop should have caught earlier.
- D: The tooling itself was working; the missing piece was a governance rule, not different tooling.

## Question 6

Scenario: A regulated healthcare deployment has been running for two quarters with all technical metrics nominal (no errors, latency in budget, eval scores stable). No stakeholder review or output audit has occurred in that time because "nothing triggered an alert."

Question: What does the module's guidance on regulated deployments say about this situation?

A. This is acceptable, since no metric has crossed a threshold.

B. Some regulated reviews (e.g., periodic output audits, scheduled data-residency confirmations) must fire on a defined schedule independent of any metric breach, and these should have been built into the governance table at design time.

C. Stakeholder reviews are only required after a compliance incident has already occurred.

D. Regulated review requirements only apply to deployments using a third-party cloud entry point.

Correct answer: B

Explanation: The module explicitly distinguishes threshold-triggered reviews from schedule-based regulated obligations. A healthcare workflow with a documentation obligation, for example, may require periodic output audits regardless of whether metrics look fine — these are design-time obligations, and skipping them risks a violation running undetected until an external reviewer asks for records.

Distractors:
- A: This confuses metric-triggered review logic with calendar-based regulatory obligations, which the module explicitly separates.
- C: Waiting for an incident before reviewing is the opposite of what a proactive, schedule-based governance row is meant to prevent.
- D: The module does not limit schedule-based regulatory obligations to any particular entry point; they follow from the regulatory context of the workflow, not the hosting route.

## Question 7

Scenario: An architect is leaving an engagement after 10 weeks. They hand off a clean, detailed architecture diagram showing the final system design. Two months later, a new architect encounters a performance issue, changes a core data-handling pattern to fix it, and inadvertently violates a data-residency requirement that the original design had specifically been built to satisfy.

Question: What does the module identify as the root cause of this kind of failure?

A. The new architect was not sufficiently senior to make production changes.

B. The architecture diagram documented what the system was but not why it was built that way, so the rationale and rejected alternatives that made the original decision load-bearing were never recorded and left with the departing architect.

C. The performance issue should never have been raised as a concern.

D. The data-residency requirement was not a real constraint and should have been ignored.

Correct answer: B

Explanation: This is the module's financial-services handoff Watch Out. The completeness test for documentation is whether a competent architect who wasn't in the room can make a safe change after reading it. A diagram alone shows what the system is; without a decision log naming the rejected alternative and its rationale, a successor cannot tell that a given decision is compliance-load-bearing.

Distractors:
- A: The module frames this as a documentation completeness failure, not a competence or seniority issue — the replacement acted reasonably given the information available.
- C: Raising and investigating performance issues is a legitimate part of ongoing operation; the failure is in how the resulting change was made without rationale to guide it.
- D: The scenario explicitly states the requirement was real and that the original design was deliberately built to satisfy it — the failure was undocumented rationale, not an invalid constraint.

## Question 8

Scenario: A compliance auditor reviewing a deployment's control register finds a row stating "Audit logging control: implemented and operating" with no further detail, and no attached artifact.

Question: What is the correct critique of this control register row, based on the module's guidance?

A. The row is sufficient, since it clearly states the control is implemented.

B. The row is incomplete because it is an assertion, not evidence — the reviewer needs a concrete evidence artifact (e.g., a configuration screen, an authorization record, or a returned log query) demonstrating the control is actually operating.

C. The row should be removed entirely, since audit logging is not normally something an auditor reviews.

D. The row is fine as long as the owner named in a separate document confirms it verbally during the audit.

Correct answer: B

Explanation: The module is explicit that a compliance reviewer does not accept mere assertions — a statement that a control exists is a claim, not proof. An evidence artifact is required: a signed agreement, a configuration screen, an authorization record, or a returned log query.

Distractors:
- A: A bare assertion with no supporting artifact is exactly what the module says a reviewer will not accept.
- C: Audit logging obligations tied to a regulatory requirement are a normal, expected part of a control register, not something to omit.
- D: Verbal confirmation is not an evidence artifact; the module requires concrete, reviewable proof, not a spoken assurance.

## Question 9

Scenario: A multi-platform deployment uses AWS Bedrock for a regulated data path and the direct Anthropic API for an unregulated back-end summarization task. The team configures the Bedrock endpoint using its default settings and does not set a specific region.

Question: What risk does this most likely create, according to the module's entry-point guidance?

A. No risk — Bedrock's default endpoint is always region-appropriate for regulated workloads.

B. A likely data-residency violation, since defaulting a Bedrock or Vertex endpoint to a global configuration instead of explicitly setting the region is the common way multi-platform deployments break residency requirements.

C. A guaranteed increase in latency regardless of region settings.

D. A licensing violation specific to the direct API portion of the workflow.

Correct answer: B

Explanation: The module explicitly warns that regional availability on Bedrock and Vertex requires explicit configuration, and that defaulting to a global endpoint is the common pattern that breaks a data-residency requirement — especially relevant here since this is the regulated data path.

Distractors:
- A: The module states the opposite — explicit regional configuration is required, and defaults are the common failure mode.
- C: Latency impact is not the stated risk of a default/global endpoint configuration in this context; residency is.
- D: Licensing is not the concern raised by the module for this scenario; the direct API portion is unregulated and unaffected by the Bedrock region setting.

## Question 10

Scenario: At the close of an engagement, an architect delivers a customer outcome document reporting: "45,000 requests/month, 1.8-second average latency, 0.3% error rate." The customer's sponsor brings this to their CFO to request budget for expanding the deployment. The CFO asks what the deployment has saved or improved in business terms, and the sponsor has no answer.

Question: What is missing from this outcome document, based on the module's guidance?

A. Nothing is missing — technical metrics are the correct basis for an expansion budget request.

B. A before-and-after comparison on the business metric the use case targeted, backed by the auditable control that makes that comparison defensible, plus the document's other required fields (scope, owner, reuse note).

C. A more detailed breakdown of the error types by hour of day.

D. A comparison of this deployment's latency against a competitor's product.

Correct answer: B

Explanation: This is the module's CFO Watch Out. Volume, latency, and error rate show that the system runs, but they are not a business outcome. The document needed the before-deployment and after-deployment measurement of the actual business metric the use case targeted, plus the control that makes that comparison auditable — the elements that actually justify expansion spend.

Distractors:
- A: This is precisely the mistake illustrated in the Watch Out — technical metrics alone could not survive the CFO's first question.
- C: Hourly error-type breakdowns are additional technical detail, not the business-outcome comparison the CFO needed.
- D: Competitive latency benchmarking is not part of the outcome document template and does not address the CFO's business-value question.
