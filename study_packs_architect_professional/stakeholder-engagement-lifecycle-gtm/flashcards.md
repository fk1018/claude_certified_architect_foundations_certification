# Stakeholder Engagement, Lifecycle & GTM Flashcards

## Discovery Fundamentals

Q: What are the three steps of the discovery-call filter?

A: Listen to the business goal in plain language, translate it into requirements/assumptions/unresolved constraints, and write those items down before the conversation moves on.

Domain: D6

Example: A stakeholder says "we want approvals to be fast." The architect listens for the underlying meaning, asks a follow-up to translate "fast" into a latency budget, and logs the resulting constraint in a translation table before the call ends.

## Translation Skill

Q: Why should an architect treat a stakeholder's experience word ("seamless," "easy," "fast," "simple," "intuitive") as a signal rather than a requirement?

A: Because design decisions are made against testable, bounded constraints, and an experience word alone is not testable — it signals that more discovery questions are needed to find the hidden constraint underneath it.

Domain: D6

Example: "We want this to feel seamless" gets translated, through follow-up questions, into a p95 latency target, a no-re-entry integration requirement, and a graceful internal-safe failure state.

## Four Discovery Categories

Q: What are the four categories a vague stakeholder statement should be forced into during discovery?

A: What the system must do, what the system must not do, what the system must cost, and what the system must prove.

Domain: D6

Example: For a healthcare dictation assistant, "must prove" surfaces the audit-trail and data-handling evidence required under a health-privacy regulation — a requirement that is far cheaper to catch in discovery than during a legal review weeks later.

## Must-Not-Do Constraints

Q: Why do "must not do" constraints require the architect to ask explicitly rather than wait for the stakeholder to volunteer them?

A: Stakeholders rarely volunteer boundaries, prohibited actions, and human-routing cases on their own; these have to be actively elicited.

Domain: D6

Example: A stakeholder describes what an assistant should do (draft an email) but never mentions, unprompted, that it must never auto-send anything above a certain dollar value — the architect has to ask.

## Translation Table Structure

Q: What four columns make up one row of a discovery translation table?

A: The stakeholder statement as said, the implied constraint, the required architectural decision, and the assumption being documented (if the constraint is not yet confirmed).

Domain: D6

Example: Row: "Clinicians will review the output anyway" → implied constraint: a licensed human must authorize output before it reaches the record → architectural decision: build a mandatory human-in-the-loop authorization gate → assumption: review is an architectural gate; confirm authority and timing.

## Watch Out: Discovery Becomes Design

Q: In the hospital-network discovery Watch Out, what turned "add a review step" from a minor detail into a mandatory architectural gate?

A: The stakeholder's "quick check" was actually a requirement that a licensed clinician authorize any model output before it reached the patient record — a required gate, not an optional add-on, that the architect never chased down because the call had already moved to sketching a solution.

Domain: D6

Example: An architect who hears "there's a review step, but it's just a quick check" should ask who performs the review, whether it's mandatory, and what happens if it's skipped — instead of nodding and starting the design.

## Watch Out: Discovery Consequences

Q: Besides the missing clinician-authorization gate, what two other constraints surfaced too late in the hospital-network Watch Out example?

A: Protected health information moving through the context window without proper handling, and the network spanning two states with different record-retention rules that the single-region design never accounted for.

Domain: D5

Example: Both issues trace to the "must not do" and "must prove" discovery categories that were never asked because the architect proposed a sketch after only two stakeholder statements.

## Checkpoint: Undocumented Assumption

Q: In the discovery checkpoint (email-drafting workflow), why is 60-day transcript retention for analytics the undocumented assumption, unlike the other three requirements?

A: The stakeholder statements only covered human sign-off on big items, drafting-with-human-send, and a "feel instant" latency expectation — nothing the stakeholder said supports a specific 60-day retention period for analytics, so it was added without being traced back to an elicited constraint.

Domain: D6

Example: An architect reviewing a requirements doc should be able to trace every line back to a stakeholder statement or an explicitly flagged assumption; a retention period invented for convenience and left unflagged is exactly the failure mode discovery is meant to prevent.

## Tradeoff Presentation Elements

Q: What three elements must every architectural tradeoff presentation include?

A: What the choice gains, what it gives up, and what reversal would cost once the system is built around it.

Domain: D6

Example: Presenting a full-context design: gains simplicity, gives up per-call cost efficiency, and reversal costs a retrieval-layer rebuild plus re-testing once downstream systems assume full-context behavior.

## Reversal Cost

Q: Why is reversal cost usually the element most likely to change a stakeholder's decision?

A: It is the element most often left out of tradeoff presentations, and it answers the question stakeholders actually need to make an informed choice: what happens if this decision turns out to be wrong after the system depends on it.

Domain: D6

Example: A CTO approves a "simpler" full-context design after hearing only a per-call cost; naming the reversal cost (rebuilding a retrieval layer once other systems are built around full-context) might have changed the approval.

## Watch Out: Uninformed Approval

Q: In the "approval that was not an informed choice" Watch Out, what specifically did the CTO's approval fail to account for?

A: The CTO approved a per-call cost figure (about 4 cents) without hearing the projected monthly bill at production call volume, and without hearing the cost of unwinding the full-context design once the system was built around it.

Domain: D6

Example: Six weeks after launch, the CTO's production invoice showed a five-figure monthly line from a decision the CTO believed had been fully explained — an accurate answer to "what's the cost per call" was not the same as an informed decision about total cost and reversal risk.

## Checkpoint: Recommend the Option

Q: In the insurer tradeoff checkpoint, which option should be recommended, and why?

A: Option A — the workflow pattern with per-interaction logging built in — because it satisfies the stated audit-trail regulatory obligation with a full presentation (gains, gives up, and a named minor reversal cost); Option B drops audit detail the regulation requires, and Option C has neither logging nor a human gate.

Domain: D6

Example: A regulated insurer needing a defensible record of every automated interaction cannot accept Option C's "lowest build cost, no logging, no human gate" approach regardless of speed.

## Checkpoint: Missing Element

Q: In the same insurer checkpoint, what single element is missing from Option B's presentation?

A: Reversal cost — Option B names what it gains (speed) and gives up (audit detail) but never states what it costs to reverse that tradeoff later.

Domain: D6

Example: Even though Option B is technically accurate and appropriate in some contexts, its presentation is incomplete under the three-element framework taught in this module.

## Feedback Loop Definition

Q: What is a feedback loop, as distinct from an observability stack?

A: A feedback loop is the decision layer sitting above observability that maps each signal to a trigger, an owner, and a required action — observability only collects and displays raw signals like latency, error rates, and eval scores.

Domain: D6

Example: A dashboard showing eval scores drifting downward is observability; a governance-table row that says "3 consecutive weeks of eval decline triggers an Architect review" is the feedback loop.

## Feedback Loop Five Steps

Q: What are the five steps of the feedback loop?

A: Signals, Triage, Decide, Act, Review.

Domain: D6

Example: A latency spike (signal) gets triaged as noise vs. real, a decision is made on whether it needs a team fix or stakeholder review, an action (guardrail update or escalation) is taken, and later the loop reviews whether that response worked.

## SLA Three Required Elements

Q: What three things must an SLA make clear?

A: What is being measured, what counts as a breach, and what happens when a breach occurs.

Domain: D6

Example: "We measure p95 response latency; a breach is any week averaging above 2 seconds; a breach triggers an Architect review within 48 hours and a stakeholder notification."

## SLA Threshold Traceability

Q: Where should SLA thresholds for latency, availability, and quality each trace back to?

A: Latency should reflect the user-experience expectation identified in discovery; availability should reflect how critical the deployment is to the business; quality should reflect the eval results and acceptance criteria already established.

Domain: D6

Example: A quality SLA threshold set at "eval score must stay within 5% of the acceptance-criteria baseline" is defensible because it traces to an established source, unlike a number picked because it "sounded reasonable."

## Cost Drift at Scale

Q: Why does cost break most often right after launch, and what should an architect do to pre-empt it?

A: Production volume routinely runs one to two orders of magnitude above pilot volume, so a trivial-looking per-call pilot cost becomes a large recurring line at scale; pre-empt it by forecasting consumption at expected production volume, naming the spend-control posture (caching, model tiering, budget alerts), and framing the model-tiering narrative before the first invoice arrives.

Domain: D6

Example: A pilot costing a few hundred dollars a month can become a five-figure monthly cost once real production volume hits, if nobody forecast that scaling before launch.

## Regulated Schedule-Based Checkpoints

Q: How do regulated deployments' review requirements differ from typical threshold-based feedback-loop triggers?

A: Some regulated reviews must fire on a defined schedule regardless of whether any metric has breached — e.g., a periodic output audit for a documentation obligation, or a scheduled data-residency confirmation — and these must be built in at design time, not added later.

Domain: D5

Example: A healthcare workflow with a documentation obligation runs a quarterly output audit on the calendar even in a quarter where every dashboard metric looked fine.

## Watch Out: Observability Without a Loop

Q: In the 90-day alert-log Watch Out, why did a visible quality drift from weeks 4-7 go unaddressed until week 12?

A: The eval score was drifting down week over week and was visible in the data, but the error rate stayed flat so no hard alert fired, and no governance rule mapped a slow quality drift to a review trigger — the signal existed but nothing decided it mattered.

Domain: D6

Example: The gap was only caught when the stakeholder complained the output was "less useful lately" at the week-12 quarterly review, seven weeks after the loop should have escalated it.

## Governance Table Purpose

Q: What should a production-signal governance table map, and when should it exist?

A: It should map each signal to its trigger, the architect's required response/action, and any regulatory checkpoint, and it should exist before launch.

Domain: D6

Example: Before a healthcare assistant goes live, the governance table already has a row specifying that a scheduled quarterly output audit is due regardless of metrics, with a named owner.

## Checkpoint: Signal Triage Buckets

Q: In the nine-signal triage checkpoint, which bucket does "eval score down three weeks running, trend is clear" belong to, and why?

A: Architect Review (or escalating toward Stakeholder Review) — a sustained multi-week eval decline is exactly the kind of slow drift the feedback-loop Watch Out shows gets missed when no trigger maps it to a review, so it needs deliberate escalation rather than being treated as noise.

Domain: D6

Example: Contrast with "one malformed request from a known bad client," which is Noise/Internal Monitoring — a single known-cause anomaly, not a trend.

## Checkpoint: Scheduled Compliance Signals

Q: Why do "scheduled data-residency confirmation is due" and "quarterly output audit against the documentation standard is due" belong in Stakeholder Review rather than Internal Monitoring, even with no metric breach?

A: Both are regulated, schedule-based obligations that must produce evidence and visibility to stakeholders/compliance regardless of whether any threshold was crossed — they are design-time governance rows, not reactive alerts.

Domain: D5

Example: These fire on the calendar the same way a scheduled audit fires whether or not the system's dashboards show any problem that quarter.

## Documentation Three Readers

Q: Who are the three readers architecture documentation must serve, and what does each need?

A: The handoff recipient (inheriting engineer) needs decisions made, alternatives rejected, and why; the compliance reviewer/auditor needs each obligation mapped to a control, an owner, and an evidence artifact; the returning architect needs dated decisions, explicitly labeled assumptions, and open items with owners and resolution criteria.

Domain: D6

Example: A document that only has a clean architecture diagram (serving neither the rejected-alternatives need nor the evidence need) is incomplete even though it looks professional.

## Documentation Completeness Test

Q: What is the practical test for whether architecture documentation is complete?

A: Whether a competent architect who was not present at the design sessions could read the document and make a safe change to the system.

Domain: D6

Example: If a document doesn't explain that a particular context strategy was chosen specifically to satisfy a data-residency rule, a successor could safely-looking "fix" a performance issue by changing it and unknowingly reintroduce a compliance violation.

## Rejected Alternatives

Q: Why do rejected alternatives matter as much as the decisions actually made in handoff documentation?

A: Without the rejected alternatives and the reason each was rejected, a successor cannot tell which tradeoff the final design was resolving, so they may reverse the right decision for the wrong reason or defend the wrong decision entirely.

Domain: D6

Example: Recording "we rejected the lower-latency context strategy because it broke the data-residency rule" tells a successor exactly why the current, slower design cannot be swapped out casually.

## Watch Out: Undocumented Rationale

Q: In the financial-services handoff postmortem, what specific failure occurred, and what was the root cause?

A: A replacement architect switched context strategies to fix a performance issue, unknowingly reintroducing a data-handling pattern that violated the deployment's data-residency constraint; the root cause was that the original architect's rationale for the original context strategy (chosen specifically to keep regulated data in-region) was never written down before leaving the engagement.

Domain: D6

Example: The architecture diagram told the replacement what the system was, but not why it was that way, so a reasonable, competent fix broke a compliance rule nobody knew was load-bearing.

## Evidence Artifact vs. Assertion

Q: What is an evidence artifact, and why does a compliance reviewer require one instead of accepting an assertion?

A: An evidence artifact is concrete proof a control is operating — a signed agreement, a configuration screen, an authorization record, or a returned log query; a reviewer treats a bare statement that a control exists as a claim, not proof.

Domain: D5

Example: "We log every interaction" is an assertion; a sample query returning actual logged records with timestamps is the evidence artifact that proves it.

## Control Register

Q: What does a control register carry forward, and where does it live after design?

A: For each regulatory obligation, it carries the technical control that satisfies it, the owner of that control, and the evidence artifact demonstrating the control is operating — carried forward into the living document that governs the deployment's production life.

Domain: D5

Example: A health-privacy audit-trail obligation maps to a specific logging control, an owner responsible for that logging pipeline, and a sample query as the evidence artifact — all tracked in the control register.

## Checkpoint: Documentation Artifact Placement

Q: On the documentation checkpoint's two-axis plane (handoff↔compliance, intention↔evidence), where does a "control register with evidence links" sit, and where does an "architecture diagram" sit?

A: The control register with evidence links sits toward compliance/evidence (it exists to prove controls are operating for an auditor); the architecture diagram sits toward handoff/intention (it shows the inheriting engineer what was built, but on its own carries no rationale or evidence).

Domain: D6

Example: A "decision log with rationale" sits toward handoff/intention (explains why choices were made for a successor), while a "test-result summary" leans toward evidence for either reader depending on what it's cited to support.

## Entry Point Re-Evaluation

Q: How does the entry-point decision change once a deployment is live across more than one platform, compared to the earlier pre-filter decision?

A: The earlier decision filtered routes on a compliance pre-filter; the live-deployment decision re-evaluates the same routes on which performs best across latency, cost, and compliance dimensions of the actual production system.

Domain: D3

Example: A route that passed the initial compliance pre-filter might still turn out to be the wrong choice once real production latency and cost data are in hand, prompting a re-selection.

## Cross-Platform Integration Risks

Q: Name three problems that a multi-entry-point deployment exposes that a single-entry-point system does not.

A: Model identifier strings differ across routes; feature availability can lag on a cloud-provider-mediated route relative to the direct API; regional availability on Bedrock/Vertex requires explicit configuration, and defaulting to a global endpoint is a common way data-residency requirements get broken.

Domain: D3

Example: A team assumes the same model name works identically on Bedrock and the direct API, only to discover the Bedrock route lags a newly released capability the direct API already supports.

## Entry-Point-Responsibility Map

Q: What is an entry-point-responsibility map, and what failure does it prevent?

A: A documented map of which entry point handles which task in a multi-entry-point workflow, and why; it prevents an entry point chosen for one task from gradually taking on another task because the routing logic was never made explicit.

Domain: D3

Example: A workflow uses the direct API for back-end inference, Claude Code for an engineering sub-task, and a Bedrock endpoint for a regulated data path — each boundary documented with its own auth, logging, and failure-mode profile.

## Outcome Document Six Fields

Q: What six fields make up a well-structured customer outcome document?

A: The use case and its scope boundary, the metric before deployment, the metric after deployment, the control that makes the result auditable, the owner responsible for ongoing measurement, and the potential to reuse the pattern for other customers/engagements.

Domain: D6

Example: For a claims-processing assistant: scope = claims intake; before = 6 days average processing time; after = 1.5 days; control = a logged approval audit trail; owner = the claims-ops lead; reuse = applicable to the network's other regional claims centers.

## Watch Out: Wrong Outcome Metrics

Q: In the CFO Watch Out, what did the outcome document capture, and what could it not answer?

A: It captured request volume (40,000/month), average latency (sub-2-second), and error rate (under 0.5%) — technical metrics that show the system runs — but it could not answer the CFO's question of what the deployment saved or produced in business terms, because the before-and-after claims-processing-time metric and its auditable control were never captured.

Domain: D6

Example: The sponsor could say "it runs reliably" but not "it cut processing time by X," which is the number that actually justifies expanding the deployment's budget.

## Technical Metrics vs. Business Outcomes

Q: Why are volume, latency, and error rate insufficient to justify deployment expansion to a CFO?

A: They demonstrate that the system works, not what it changed; only a before-and-after comparison on the business metric the use case targeted, backed by an auditable control, tells a sponsor what the deployment is worth.

Domain: D6

Example: "Sub-two-second average latency" answers "does it run fast," not "did it save us money or time," which is the question that actually unlocks further budget.

## Deployment Lifecycle Phases

Q: What are the five phases of the deployment lifecycle referenced across this module, and which topics map to which phases?

A: Discovery → Design → Handoff → Monitoring → Iteration. Discovery and tradeoff framing cover discovery-and-design; the feedback loop covers monitoring-and-iteration; documentation covers handoff; entry-point selection and the outcome document close the loop.

Domain: D6

Example: Recognizing that a stakeholder's question ("should we switch context strategies now?") is a monitoring-and-iteration-phase decision, not a discovery-phase one, tells the architect which governance table and which evidence to consult.

## Lifecycle-Phase Gating

Q: What does it mean to judge whether a lifecycle phase is "ready" to move to the next?

A: Identifying the specific artifact that gates the transition to the next phase and verifying that artifact is actually satisfied, rather than assuming a phase is complete by default.

Domain: D6

Example: Handoff to production monitoring isn't complete just because code shipped — it requires the decision log, control register, and governance table to actually exist and be populated first.

## Case Study: Must-Prove Constraint

Q: In the cumulative healthcare case study, what is the must-prove constraint that most shapes the architecture, and what does it force?

A: The health-privacy obligation with its audit-trail requirement is the must-prove constraint; it forces a requirement row establishing that every clinical note draft and its human authorization must be logged in an auditable, evidence-producing way before the note reaches the patient record.

Domain: D5

Example: This is a direct application of the discovery translation framework's "what must the system prove" category to a regulated healthcare workflow.

## Case Study: Latency vs. Audit Tradeoff

Q: In the cumulative case study's tradeoff decision, how should the architect frame trimming logging for latency against keeping the audit trail?

A: Gains: faster response time by trimming the logging step. Gives up: per-interaction audit-trail detail required by the health-privacy obligation. Reversal cost: rebuilding the audit-logging layer and revalidating compliance evidence after the fact, likely under time pressure from a reviewer, once the system and its downstream record-keeping have been built around the trimmed-logging design.

Domain: D6

Example: This mirrors the insurer checkpoint's Option A vs. B framing, but here the audit trail is not optional — it is required by the health-privacy obligation, making the reversal cost especially severe.

## Case Study: Scheduled Governance Row

Q: In the cumulative case study's feedback-loop decision, what does a governance-table row for the required output audit look like?

A: Signal: none (schedule-based, not metric-triggered). Trigger: the recurring output-audit due date under the documentation obligation. Owner: the architect or designated compliance lead. Action: conduct the periodic output audit and produce the evidence artifact, regardless of whether any other metric has breached that period.

Domain: D5

Example: This applies the module's core lesson that some regulated reviews fire on a schedule independent of any threshold — exactly the gap shown in the "observability stack" Watch Out.

## Case Study: Load-Bearing Decision Log Row

Q: In the cumulative case study's documentation decision, what decision-log row is critical to prevent a compliance-load-bearing reversal, and what must it carry?

A: The row documenting the choice of context/data-handling strategy made to satisfy the data-residency rule; it must carry the rejected alternative (e.g., a lower-latency or cross-region approach) and the explicit reason it was rejected (it would have violated data residency).

Domain: D6

Example: This directly parallels the financial-services Watch Out, where an undocumented residency-driven decision was reversed by a successor "fixing" performance and reintroduced a violation.

## Case Study: Entry Point Selection

Q: In the cumulative case study, given AWS standardization, a strict regulatory obligation, and a data-residency rule, what entry points should be selected and what configuration step matters most?

A: AWS Bedrock as the primary entry point for the regulated clinical-note workflow (matching partner standardization and compliance posture), with the direct API retained as secondary for non-regulated back-end work; the critical configuration step is explicitly setting regional availability on Bedrock rather than defaulting to a global endpoint, which is the common way data-residency requirements get silently broken.

Domain: D3

Example: This directly applies the module's warning that Bedrock/Vertex regional availability requires explicit configuration and that defaulting to global is the most common multi-platform residency failure.

## Case Study: Outcome Document Fields

Q: In the cumulative case study, what before-and-after business metric and control should the outcome document capture for the CFO's expansion case?

A: The before-and-after clinical-documentation metric the use case targeted (e.g., nurse time spent per note, or note turnaround time) compared pre- and post-deployment, backed by the auditable clinician-authorization/logging control that makes the after-number defensible.

Domain: D6

Example: This mirrors the claims-processing-time example from the outcome-document Watch Out — a CFO needs a business-metric before/after, not just volume/latency/error-rate figures.

## Case Study: Phase Transition Gate

Q: In the cumulative case study's final decision, what determines whether the deployment is ready to move to its next lifecycle phase?

A: The gating artifact is whatever the phase transition specifically requires being complete and evidenced — e.g., moving from handoff to steady-state monitoring requires the decision log, control register, and governance table to exist and be populated, not merely that the system is technically live; the architect must name that artifact and judge whether it is actually satisfied, not assume it by default.

Domain: D6

Example: Four weeks into the deployment with the original architect rotating off, the case study specifically tests whether the handoff documentation (decision log + control register) is complete enough to gate a safe transition away from that architect's direct involvement.

## Partner-Track Exclusion

Q: Which learning objective and which outcome-document field are explicitly flagged as partner-track content not tested on the Architect exam?

A: The objective to lead the Architect's role in partner go-to-market (discovery, scenario-based demo, technical objection handling, joint scoping with the Anthropic Applied AI team), and the "reuse potential for other customers/engagements" field of the outcome document.

Domain: General

Example: An exam-focused reader can safely deprioritize demo-design and joint-scoping mechanics while still learning the underlying outcome-document structure, since five of its six fields are on-blueprint.
