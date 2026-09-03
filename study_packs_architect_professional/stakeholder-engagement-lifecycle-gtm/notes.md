# Stakeholder Engagement, Lifecycle & GTM

- Source URL: https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional
- Completed: 2026-09-03
- Study pack: `study_packs_architect_professional/stakeholder-engagement-lifecycle-gtm/`

## Captured Sections

- Module Introduction: Orientation (five learning objectives; lifecycle framing: discovery → design → handoff → monitoring → iteration)
- Discovery: A discovery call is structured elicitation
- Watch Out: The discovery call that turned into a design session
- Checkpoint: Find the undocumented assumption
- Tradeoffs & GTM: Present a tradeoff so stakeholders can act
- Watch Out: The approval that was not an informed choice
- Checkpoint: Recommend the option and name the missing element
- Feedback Loops: The feedback loop decides which signals reach a stakeholder, and the SLA names what you owe when one breaks
- Watch Out: The observability stack that replaced the feedback loop
- Checkpoint: Triage the production signals
- Documentation: Documentation that survives your absence serves the handoff recipient, the auditor, and the returning Architect
- Watch Out: The design rationale that lived in the Architect's head
- Checkpoint: Place the documentation artifacts
- Entry Point & Outcomes: Entry point selection returns with the full production picture, and the outcome document turns the work into reusable IP
- Watch Out: The outcome document that measured the wrong thing
- Checkpoint: Pick the platform and the required outcome fields
- Module Cumulative: Architect a regulated multi-platform deployment end to end (7-decision healthcare case study)
- Recap: Five things that hold across everything here
- Glossary
- Module Complete (Module 4 of 5; M5 "Team Enablement and Operational Productivity" up next)

## Exam Domain Mapping

| Domain | Relevance | Covered Ideas |
|---|---|---|
| D1: Solution Design & Architecture | Low | Discovery's four-question framework (must do / must not do / must cost / must prove) feeds architectural requirements, and the entry-point-responsibility map touches multi-agent/multi-route decomposition, but the module does not teach architectural patterns, decomposition method, or business-value-pillar mapping directly. |
| D2: Claude Models, Prompting & Context Engineering | Low | The tradeoff Watch Out uses a context-window-vs-retrieval decision (full context vs. prompt caching) as its worked example, but only as a vehicle for tradeoff communication, not as prompting/context-engineering instruction. |
| D3: Integration | Medium | Entry point selection covers direct API vs. Bedrock vs. Vertex vs. Microsoft Foundry on latency/cost/compliance, model-identifier drift across routes, regional configuration for data residency, and the entry-point-responsibility map for multi-entry-point workflows. Does not teach RAG pipeline design, retrieval strategies, or tool/agent capability bloat. |
| D4: Evaluation, Testing & Optimization | Low | Feedback loops reference eval scores as one input signal (quality drift, SLA thresholds traced to eval results/acceptance criteria) and cost/latency monitoring, but do not teach eval dataset construction, A/B testing, or optimization technique. |
| D5: Governance, Safety & Risk Management | Medium | Regulated-deployment review checkpoints on a schedule, human-in-the-loop authorization gates (licensed clinician sign-off), health-privacy/data-residency obligations, control registers, and evidence artifacts for compliance reviewers are all covered substantively. Does not teach broader safety guardrail design, red-teaming, or general risk taxonomy beyond the stakeholder-lifecycle lens. |
| D6: Stakeholder Communication & Lifecycle Management | High | This is the module's core: structured discovery and the four-category translation framework, tradeoff presentation with reversal cost, feedback-loop/SLA governance tables, documentation for three readers (handoff recipient, compliance reviewer, returning architect), and lifecycle-phase gating from discovery through iteration. |
| D7: Developer Productivity & Operational Enablement | None | Not covered. This module explicitly hands off to Module 5 ("Team Enablement and Operational Productivity") for team tooling configuration, developer workflows, and operational support. |

## Key Concepts

| Concept | Study Notes |
|---|---|
| Discovery as structured elicitation | A discovery call is a three-step filter: listen (business goal in plain language), translate (requirements, assumptions, unresolved constraints), write down (record before the conversation moves on). Skipping the filter means the design inherits the architect's assumptions instead of the stakeholder's actual constraints. |
| Translation (the core discovery skill) | Stakeholders speak in preferences ("seamless," "easy," "fast," "simple," "intuitive"); design decisions require constraints. An experience word is a signal that more discovery is needed, not a requirement to record as-is. Ask what would break the experience, what the user must never notice, what must happen behind the scenes, and what must still hold when something goes wrong. |
| Four discovery question categories | (1) What the system must do — business-outcome capabilities and what Claude owns vs. what stays with a human/existing system. (2) What the system must not do — boundaries, prohibited actions, human-routing cases (rarely volunteered, must be asked). (3) What the system must cost — latency target, per-interaction cost ceiling, volume forecast. (4) What the system must prove — evidence/audit obligations, especially in regulated workflows; cheaper to surface in discovery than in a later legal review. |
| Translation table | The output artifact of discovery: one row per item with four columns — stakeholder statement (verbatim), implied constraint, required architectural decision, and assumption-of-document (assumptions not yet confirmed, explicitly flagged). Keeps reasoning intact as work moves from discovery into design. |
| Watch Out: discovery → design session | Sketching a solution mid-call feels productive and the stakeholder approves because it sounds competent — but that plausibility ends the question-asking. A "quick check" or "it's just a review" is exactly the kind of statement that hides a required architectural gate (e.g., mandatory clinician authorization), a PHI-handling requirement, or a multi-jurisdiction data-retention conflict. Fix: finish all four question categories before proposing anything. |
| Tradeoff presentation — three required elements | Every tradeoff presentation must name: (1) what the choice gains, (2) what it gives up, (3) what reversal costs once the system is built around it. The third element (reversal cost) is most often missing and is usually the one that changes the stakeholder's decision. |
| Watch Out: approval without informed choice | A stakeholder can approve a technically accurate presentation and still not have made an informed choice if the reversal cost was never named. Example: CTO approved "~4 cents per call" for a large-context design without hearing the monthly bill at production volume or the cost of unwinding a full-context-dependent system later — got a five-figure surprise invoice. |
| Cost surprises after launch | Production volume typically runs 1-2 orders of magnitude above pilot volume, so a per-call cost that looked trivial in POC becomes a large recurring line at scale. Pre-empt this: give a consumption forecast at expected production volume, name the spend-control posture (caching, model tiering, budget alerts), and frame model-tiering narrative before the first invoice, not after. |
| Feedback loop as decision layer | Observability (latency, error rates, eval scores, usage patterns) supplies raw signals; a feedback loop is the governance layer on top that decides which signals matter and what to do. Five-step loop: Signals → Triage → Decide → Act → Review. A dashboard without a feedback loop just displays data; it does not decide anything. |
| Watch Out: observability replacing the feedback loop | A rigorous observability stack can create false confidence that stakeholder feedback is "covered." In the case study, eval score drifted for weeks (weeks 4-7) without crossing a hard error-rate threshold, so no alert fired and no review triggered — the decline surfaced only at a routine quarterly review in week 12, seven weeks late. Signals existed; no rule mapped them to a trigger. |
| SLA — three required elements | An SLA must state: (1) what is being measured, (2) what counts as a breach, (3) what happens when a breach occurs. Thresholds must trace to something tangible: latency → the user-experience expectation from discovery; availability → business criticality; quality → the eval results/acceptance criteria already established. An untraceable threshold is an arbitrary target, not a defensible SLA. |
| Regulated review checkpoints on a schedule | In regulated deployments, some governance reviews must fire on a calendar regardless of whether any metric breaches (e.g., periodic output audits for a documentation obligation, scheduled data-residency confirmation). These are design-time obligations, not later add-ons — retrofitting them after the fact is far more expensive and may leave a violation running undetected until an external reviewer asks for records. |
| Production-signal governance table | Maps each signal to a trigger, an owner (Architect vs. stakeholder vs. internal monitoring), and a required action. Built and populated before launch. This table is what turns policy into an operating routine — the mechanism the "observability stack" Watch Out shows was missing. |
| Documentation serves three distinct readers | One documentation set must serve: (1) the handoff recipient (inheriting engineer) — needs decisions made, alternatives rejected, and why; (2) the compliance reviewer/auditor — needs each obligation mapped to a control, an owner, and an evidence artifact (not just an assertion); (3) the returning architect — needs dated decisions, explicitly labeled assumptions, and open items with owners/resolution criteria. A document built for only one reader is incomplete even if detailed. |
| Documentation completeness test | Can a competent architect who was not in the room make a safe change to the system after reading the document alone? If no, the documentation is incomplete regardless of how thorough the diagrams are. A diagram shows *what* the system is; only recorded rationale shows *why*, and only the "why" tells a successor which choices are load-bearing vs. mere preference. |
| Watch Out: rationale lived in the architect's head | Original architect designed a context strategy specifically to keep regulated data in-region; left the engagement 12 weeks post-launch with no design-session record. Replacement, facing a performance issue, switched context strategies to fix it — reintroducing a data-handling pattern that violated the data-residency rule. The diagram never carried the rejected alternative or the rationale, so the replacement reversed a load-bearing compliance decision for an understandable but wrong reason. |
| Control register / evidence artifact | For a compliance reviewer, an asserted control ("we have a control for X") is a claim, not proof. An evidence artifact is concrete proof the control is operating: a signed agreement, a configuration screen, an authorization record, a returned log query. The control register carries obligation → control → owner → evidence artifact forward into the living document that governs the deployment's production life. |
| Entry point selection returns with production context | Earlier-module entry-point selection (direct API, Bedrock, Vertex, Microsoft Foundry) was a compliance pre-filter. Post-launch, the same decision is re-evaluated on live latency, cost, and compliance performance across a multi-platform deployment. Model identifier strings differ across routes; feature availability can lag on cloud-provider-mediated routes vs. direct API; regional availability on Bedrock/Vertex requires explicit configuration — defaulting to a global endpoint is the common way data-residency requirements get silently broken. |
| Entry-point-responsibility map | Required before writing the first line of integration code for any workflow spanning multiple entry points (e.g., direct API for back-end inference + Claude Code for an engineering sub-task + Bedrock for a regulated data path). Documents which entry point owns which task and why. Prevents the common failure of an entry point chosen for one task silently absorbing another because routing logic was never documented. |
| Customer outcome document — six required fields | (1) the use case and its scope boundary, (2) the metric before deployment, (3) the metric after deployment, (4) the control that makes the result auditable, (5) the owner responsible for ongoing measurement, (6) the potential to reuse the pattern for other customers/engagements (partner-track relevant). Technical metrics alone (volume, latency, error rate) do not constitute this document — the before/after business metric and reuse notes are what make it a reusable asset. |
| Watch Out: outcome document measured the wrong thing | An architect wrote an outcome document from the easiest-to-export metrics: request volume, average latency, error rate under 0.5%. The sponsor's CFO asked what the deployment saved/produced in business terms (e.g., claims-processing time before vs. after) — the document had no answer. Technical metrics tell a reader the system runs; only a before/after business metric backed by an auditable control tells a CFO what expansion is worth. |
| Project/deployment lifecycle phases | Discovery → design → handoff → monitoring → iteration. Discovery and tradeoff framing are the discovery-and-design work; the feedback loop is monitoring-and-iteration; documentation is the handoff phase; entry-point selection plus the outcome document closes the loop. Each topic in the module extends the one before it: discovery's constraints are what the tradeoff presentation defends; the feedback loop keeps the control register current; documentation rationale keeps decisions from being silently reversed; the outcome document draws on every layer above it. |
| Lifecycle-phase gating | Identifying which lifecycle phase a decision belongs to is what lets an architect judge whether that phase is ready to move to the next (an explicit skill tested in Decision 7 of the cumulative case study — naming the artifact that gates the next phase transition and judging whether it is satisfied). |
| Partner-track content (not exam-tested) | Objective 4 (leading Architect's role in partner GTM: discovery, scenario-based demo, technical objection handling, joint scoping with Anthropic Applied AI team) is explicitly flagged "Partner-Track Relevant, not tested by the Architect exam." The "reuse potential" field of the outcome document and the scenario-specific demo material are similarly partner-track flavor on top of an otherwise on-blueprint document. |

## Decision Rules

- If a stakeholder uses an experience word ("seamless," "easy," "fast," "simple," "intuitive"), do not record it as the requirement — ask what would break that experience and translate the answer into a testable, bounded constraint before proceeding to design.
- If a stakeholder says "it's just a quick check" or "it's just a review," treat that phrase as a probable required architectural gate (e.g., mandatory human authorization) and chase down the constraint explicitly rather than accepting it as a minor add-on.
- If you are about to sketch or propose a solution mid-discovery-call, stop and finish all four question categories (must do / must not do / must cost / must prove) first — a plausible sketch ends the questions a discovery call exists to ask.
- If presenting a tradeoff for stakeholder approval, always name what it gains, what it gives up, and what reversal costs once the system is built around it — omitting reversal cost means the stakeholder has not made an informed choice even if they said yes.
- If a workflow is high-volume, forecast cost at production volume (not pilot volume) and name the spend-control posture (caching, model tiering, budget alerts) before launch, since production volume routinely runs 1-2 orders of magnitude above pilot.
- If a metric is drifting slowly but has not crossed a hard alert threshold, it still needs a governance-table row mapping it to a trigger, owner, and action — a dashboard collecting a signal is not the same as a feedback loop deciding the signal matters.
- If setting an SLA threshold, trace it to a tangible source (user-experience expectation for latency, business criticality for availability, eval/acceptance criteria for quality) — an untraceable number is not defensible.
- If a deployment is regulated, wire scheduled review checkpoints (periodic audits, residency confirmations) into the governance table at design time, independent of any metric threshold, because these obligations fire on a calendar, not on a breach.
- If documenting a decision, always record the rejected alternatives and the tradeoff each resolved, not just the final choice — the "why" is what tells a successor which choices are load-bearing.
- If a design choice satisfies a compliance/regulatory constraint (e.g., a context strategy chosen for data residency), flag that decision explicitly as load-bearing in the documentation so a successor does not reverse it while "fixing" an unrelated issue like performance.
- If a workflow spans more than one Claude entry point (API, Bedrock, Vertex, Foundry, Claude Code), produce an entry-point-responsibility map before writing integration code, naming which entry point owns which task and why.
- If configuring a cloud-mediated route (Bedrock/Vertex) for a data-residency-bound workload, explicitly configure regional availability — do not default to a global endpoint.
- If writing a customer outcome document, always capture the before-deployment metric, the after-deployment metric, and the auditable control connecting them — technical metrics (volume, latency, error rate) alone cannot justify expansion to a CFO.
- If judging whether a lifecycle phase is ready to move to the next, name the specific artifact that gates that transition and verify it is actually satisfied, rather than assuming forward progress by default.

## Anti-Patterns

- Sketching or proposing an architecture mid-discovery-call before the four question categories are exhausted, because a confident, plausible sketch stops the stakeholder from raising further constraints.
- Recording a stakeholder's experience word ("seamless") verbatim as a requirement instead of translating it into a bounded, testable constraint.
- Treating "it's just a review" or "it's just a quick check" as a minor implementation detail rather than as a probable mandatory human-in-the-loop gate.
- Presenting a tradeoff with only "what it gains" and "what it costs per unit," and omitting reversal cost — this produces an approval that is not actually an informed choice.
- Sizing cost estimates only at pilot/POC volume and never forecasting production-scale spend before launch.
- Treating an observability/monitoring stack as equivalent to a feedback loop; a dashboard displays signals, a feedback loop decides which signals trigger action and assigns an owner.
- Leaving regulated review checkpoints undefined until a metric breaches, when some checkpoints are calendar-based obligations that must exist independent of any threshold.
- Producing architecture diagrams without a decision log that records rejected alternatives and rationale — this leaves "why" undocumented and load-bearing decisions vulnerable to accidental reversal.
- Asserting that a compliance control exists without attaching an evidence artifact (a reviewer treats an assertion as a claim, not proof).
- Defaulting a Bedrock or Vertex deployment to a global endpoint on a data-residency-bound workload.
- Building a multi-entry-point integration without a documented entry-point-responsibility map, letting an entry point chosen for one task silently absorb another.
- Writing a customer outcome document using only easy-to-export technical metrics (volume, latency, error rate) without a before/after business metric, an auditable control, and a reuse note.
- Assuming a lifecycle phase is complete without naming and checking the specific artifact that gates transition to the next phase.

## Scenario Traps

- Trap: "The stakeholder approved the sketch, so discovery is done." Better: approval of a plausible-sounding sketch is exactly when critical constraints (mandatory human gates, PHI handling, multi-jurisdiction rules) go unasked and surface later during compliance review.
- Trap: "The stakeholder said yes to the tradeoff, so it was an informed decision." Better: check whether reversal cost was actually named — an accurate presentation can still leave out the one element (reversal cost, or monthly cost at production volume) that would have changed the answer.
- Trap: "We have dashboards and alerts, so stakeholder feedback is covered." Better: a dashboard only displays signals; without a governance table mapping signals to triggers, owners, and actions, a slow quality drift can run for weeks with no alert firing.
- Trap: "The architecture diagram is thorough, so documentation is complete." Better: a diagram shows what the system is, not why — without a decision log naming rejected alternatives and rationale, a successor cannot tell which choices are load-bearing.
- Trap: "We collected volume, latency, and error-rate metrics, so the outcome document proves the deployment's value." Better: those are technical metrics that show the system runs; a CFO needs a before/after business metric backed by an auditable control to justify expansion spend.
- Trap: "Regulated checkpoints will show up once something breaks." Better: some regulated reviews are calendar-based obligations independent of any metric breach and must be wired in at design time.
- Trap: "A per-call cost that looked trivial in the pilot will scale fine." Better: production volume typically runs 1-2 orders of magnitude above pilot, turning a trivial per-call number into a large recurring cost line.
- Trap: "Multi-platform deployment is just picking the compliant route once, up front." Better: once live, the same route decision must be revisited against actual latency, cost, and compliance performance, and a responsibility map is needed for every entry-point boundary.

## Memorization Cues

- Discovery filter: Listen → Translate → Write down.
- Four discovery categories: Must Do, Must Not Do, Must Cost, Must Prove.
- Tradeoff's three elements: Gain, Give up, Reversal cost (reversal cost is the one most often missing).
- Feedback loop's five steps: Signals → Triage → Decide → Act → Review.
- SLA's three parts: What's measured, what's a breach, what happens on breach — thresholds trace to UX expectation (latency), business criticality (availability), or eval/acceptance criteria (quality).
- Documentation's three readers: Handoff recipient (why), Compliance reviewer (evidence), Returning architect (navigable without a briefing).
- Documentation completeness test: could someone who wasn't in the room make a safe change after reading it alone?
- Outcome document's six fields: use case + scope, before metric, after metric, auditable control, owner, reuse potential.
- Lifecycle: Discovery → Design → Handoff → Monitoring → Iteration.
- "A diagram carries what the system is; without rationale it cannot say what is load-bearing."

## Source References

- Module Introduction / Orientation: five learning objectives, lifecycle framing (discovery → design → handoff → monitoring → iteration), and how the five topics build on each other.
- Discovery: three-step filter (listen/translate/write down), the "seamless" translation walkthrough, four discovery question categories, and the translation table format.
- Watch Out (Discovery): reconstructed hospital-network discovery call that jumped to a design sketch, missing the mandatory clinician-authorization gate, PHI handling, and multi-state retention rules.
- Checkpoint (Discovery): find the undocumented assumption in a requirements document built from a discovery-call summary (customer-email drafting scenario).
- Tradeoffs & GTM: three required tradeoff elements (gain, give up, reversal cost), and why reversal cost is the element that changes the meeting.
- Watch Out (Tradeoffs): reconstructed pre-production review where a CTO approved a per-call cost figure without hearing the production-volume monthly cost or the reversal cost of a full-context design.
- Checkpoint (Tradeoffs): recommend an option among three adjuster-response workflow presentations for a regulated insurer, and name the missing element in the second.
- Feedback Loops: feedback loop as decision layer above observability, the five-step loop (Signals/Triage/Decide/Act/Review), SLA's three required elements and threshold traceability, cost drift at production volume, and regulated schedule-based checkpoints.
- Watch Out (Feedback Loops): 90-day alert-log-vs-review-calendar trace showing a quality drift (weeks 4-7) that never fired a hard alert and was only caught at a routine quarterly review in week 12.
- Checkpoint (Feedback Loops): triage nine production signals into Internal Monitoring / Architect Review / Stakeholder Review / Noise.
- Documentation: documentation's three readers (handoff recipient, compliance reviewer, returning architect) and the completeness test.
- Watch Out (Documentation): financial-services handoff postmortem where an undocumented context-strategy rationale (chosen for data residency) was reversed by a successor fixing a performance issue, reintroducing a residency violation.
- Checkpoint (Documentation): place six documentation artifacts (architecture diagram, decision log, control register, runbook, test-result summary, assumption register) on a handoff/compliance x intention/evidence plane.
- Entry Point & Outcomes: entry-point selection revisited with production context, cross-platform integration risks (model-identifier drift, feature-availability lag, regional-config defaults), entry-point-responsibility map, and the six-field outcome document template.
- Watch Out (Entry Point & Outcomes): outcome document built from easy-to-export technical metrics that could not survive a CFO's first question about business value.
- Checkpoint (Entry Point & Outcomes): pick a primary/secondary platform and required outcome-document fields given cloud platform, regulatory obligation level, and performance constraint.
- Module Cumulative: seven-decision regulated multi-platform healthcare case study spanning discovery, tradeoff framing, feedback loop, documentation, entry-point selection, outcome document, and phase-transition gating.
- Recap: five takeaways restating discovery, tradeoff/GTM, feedback loops/SLA, documentation, and entry-point/outcomes; partner-track GTM material flagged as not exam-tested.
- Glossary: control register, decision log, deployment lifecycle, discovery, documentation completeness, entry-point-responsibility map, evidence artifact, feedback loop, governance table, joint scoping, limit placement, outcome document, requirement vs. assumption, reversal cost, scenario-specific demo, SLA, tradeoff framing, translation, translation table.
- Sources cited by the module: Building with the Claude API (Skilljar), Claude 101 (Skilljar), AI Capabilities and Limitations (Skilljar), platform.claude.com/docs, anthropic.com partner program documentation, Anthropic Applied AI team documentation.

## Gaps / Follow-Up

- The raw capture records the checkpoint and cumulative-case-study *questions* and setups but not the platform's revealed model-answer text (interactive "Reveal model answer" / "Check answer" content was not captured as static text) — flashcards and practice questions in this pack apply the module's stated frameworks to construct consistent answers, but verify against the live course if exact wording matters.
- Study the full deployment-entry-point decision matrix and customer outcome documentation template referenced by name in Screen 13 — the capture names these artifacts but the underlying matrix/template tables were not rendered as text.
- Study the partner-track GTM material (scenario-based demo design, technical objection handling, joint scoping with Anthropic Applied AI) in a partner-specific resource, since it is explicitly excluded from the Architect exam.
- Study Module 5 ("Team Enablement and Operational Productivity") separately for team tooling configuration, developer workflows, and operational support — this module explicitly does not cover that material.
- Cross-check current entry-point capabilities (model identifiers, regional availability, feature parity across API/Bedrock/Vertex/Foundry) against platform.claude.com/docs at build/study time, since the module flags this content as subject to change.
