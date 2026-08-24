# CCARP Practice Exam 5

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Underwriting Platform for a Commercial Insurer, RAG and Model Selection for a Manufacturing Predictive-Maintenance Platform, Evaluation and Optimization of a Fraud-Detection Triage System, Governance and Stakeholder Communication for a Banking GDPR Deployment) |
| Passing proxy | The real exam uses a scaled score of 100–1,000 with 720 to pass. As a rough proxy, aim for **≥ 45 / 60 (75%)**. |

Domain distribution (approximate, matches the official blueprint weightings):

| Domain | Questions |
|---|---|
| D1: Solution Design & Architecture (17%) | 10 |
| D2: Claude Models, Prompting & Context Engineering (13%) | 8 |
| D3: Integration (19%) | 11 |
| D4: Evaluation, Testing & Optimization (16%) | 10 |
| D5: Governance, Safety & Risk Management (14%) | 8 |
| D6: Stakeholder Communication & Lifecycle Management (14%) | 8 |
| D7: Developer Productivity & Operational Enablement (7%) | 5 |

Answer key with explanations is at the end of this file. Answer every question before checking — the real exam does not allow skipping.

---

## Scenario A: Multi-Agent Underwriting Platform for a Commercial Insurer (Questions 1–15)

Meridian Commercial Insurance is modernizing risk assessment, pricing, and policy issuance for its commercial lines business. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Meridian's underwriting and operations stakeholders.

---

**Question 1.** Discovery reveals that Meridian's actual driver for this initiative is entering a new specialty insurance line (cyber liability) that the current underwriting process has no capability to evaluate at all, not incremental efficiency gains on an existing line.

- A) Frame the architecture around efficiency, since most of Meridian's past AI initiatives have been efficiency plays on existing lines.
- B) Frame the architecture around transformation, since the driver is a capability the process entirely lacks.
- C) Frame the architecture around cost reduction, since automating underwriting steps typically lowers per-application handling cost.
- D) Skip framing around a single value pillar and let stakeholders infer the value narrative from whatever ships.

**Question 2.** Underwriting risk assessment, pricing, and policy issuance each require different steps depending on the applicant's industry, prior loss history, and information uncovered mid-review.

- A) Use a fixed workflow, since underwriting is a mature process most insurers have reduced to standard checklists.
- B) Use an augmented LLM pattern, since a single retrieval-enhanced call can underwrite any commercial policy.
- C) Use an agentic pattern, since the right sequence of steps varies by case and by mid-review findings.
- D) Use whichever pattern the engineering team can staff fastest, since the patterns are functionally interchangeable here.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (risk scoring, pricing, compliance check, policy drafting).

- A) Let subagents message each other directly to shave off a hop, accepting some loss of central visibility.
- B) Route all inter-subagent communication through the coordinator.
- C) Merge risk scoring, pricing, compliance, and drafting into one subagent to remove coordination overhead entirely.
- D) Let subagents communicate directly, but mirror the traffic to a log store for later review.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition only routes single-state policies to the pipeline — multi-state package policies are never routed to any subagent and silently fall through.

- A) Add a fifth subagent dedicated to multi-state package policies, layered on top of the existing routing.
- B) Add a prompt instruction telling each subagent to flag policies it doesn't recognize as its own.
- C) Fix the coordinator's decomposition so it explicitly routes every policy category, multi-state included.
- D) Give the existing subagents broader tool access so any of them can absorb an unrouted policy.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian actually cares about, distinct from a generic "we added AI" narrative.

- A) Treat business value pillars as a sales concern that shouldn't shape the technical architecture.
- B) Choose the pillar after the system ships, based on whichever benefit turns out easiest to measure.
- C) Efficiency, transformation, productivity, cost, and SLAs are pillars; the chosen one should drive architecture and metrics.
- D) Assume any AI system inherently demonstrates transformation, so no further framing is required.

**Question 6.** Meridian's underwriters are skeptical of automation and worried about job security; discovery interviews surface this repeatedly.

- A) Leave the sentiment out of the architecture, since job-security worries aren't a technical requirement.
- B) Proceed with the technical design and leave the sentiment entirely to a separate change-management workstream.
- C) Recommend against the project entirely based on the sentiment surfaced in interviews.
- D) Treat it as a real constraint shaping rollout sequencing and where human-in-the-loop checkpoints matter most.

**Question 7.** A stakeholder asks why the risk-scoring subagent uses a higher-capability, higher-cost model tier than the document-drafting subagent.

- A) Use the same tier everywhere for simplicity, regardless of how much reasoning each task actually needs.
- B) Explain the tradeoff: risk scoring needs deeper reasoning that justifies the increased cost, drafting doesn't.
- C) Tell the stakeholder the higher tier was chosen "because it's more important" and leave it there.
- D) Avoid discussing tier differences, on the assumption stakeholders don't want the technical detail.

**Question 8.** The architecture's current design produces a final pricing recommendation with no mechanism to learn from underwriter overrides or outcomes over time.

- A) Add a feedback loop capturing underwriter overrides and outcomes as a first-class component.
- B) Treat the design as complete, since it already reflects current underwriting best practice.
- C) Treat feedback loops as a data-science concern with no architectural hooks required.
- D) Defer any feedback mechanism to a hypothetical future phase, with no hooks in the current build.

**Question 9.** Meridian wants a single enhanced LLM call — with retrieval of policy wording — to answer straightforward certificate-of-insurance lookups, without any multi-step autonomous orchestration.

- A) Build a full multi-agent architecture regardless of how simple the certificate lookup actually is.
- B) Use an augmented LLM pattern: a single retrieval-enhanced call fits this simpler need.
- C) Conclude this can't be built with Claude at all, since it doesn't involve autonomous agent behavior.
- D) Require a fixed workflow with at least five sequential steps before a lookup can return an answer.

**Question 10.** The document-intake subagent's toolset has grown to include tools for tasks like billing lookup and customer notification that are unrelated to document intake.

- A) Remove the unrelated tools and relocate them to a more appropriate subagent.
- B) Accept the added tools as long as the subagent's prompt gives structured guidance on which tool to use when.
- C) Treat more tools as always improving flexibility, and keep adding them as new needs arise.
- D) Address the growing toolset by increasing the subagent's context window rather than its scope.

**Question 11.** The coordinator currently processes each application sequentially through document intake, risk scoring, compliance check, and pricing, even though risk scoring and compliance check have no dependency on each other's output.

- A) Keep processing sequential, since compliance auditors require a single linear trace of steps.
- B) Conclude parallelization isn't possible once a coordinator/subagent architecture is in place.
- C) Run risk scoring and compliance check as independent, parallel subagent calls once intake completes.
- D) Combine risk scoring and compliance check into one subagent, accepting slower per-application throughput as a fair tradeoff for a simpler design to maintain.

**Question 12.** Meridian asks how the end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and per-call token costs involved in the pipeline.
- B) Present the full technical architecture diagram, including every subagent and tool call, unsimplified.
- C) Describe input → processing → output → feedback loop at a level tied to business outcomes.
- D) Skip a high-level description and move directly into a live implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, risk scoring, compliance checking, pricing) rather than a coordinator with specialized subagents.

- A) A single agent holding every tool is more exposed to degraded tool-selection reliability than scoped subagents.
- B) A single generalist agent scales better than specialized subagents as the tool count grows.
- C) Specialized subagents are strictly a cost-increasing choice, with no offsetting reliability benefit.
- D) There's no meaningful architectural difference between a single generalist agent and a coordinator with subagents.

**Question 14.** The underwriting architecture must eventually support a new line (parametric crop insurance) Meridian is planning to launch next year, but detailed requirements aren't available yet.

- A) Design current decomposition and subagent boundaries with reasonable extensibility, not for undefined future requirements.
- B) Ignore the future crop-insurance line entirely until detailed requirements eventually arrive.
- C) Build full support for parametric crop insurance now, guessing at underwriting rules, rate tables, and loss ratios that don't exist yet.
- D) Refuse to proceed with the current phase until next year's requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, on the assumption implementation is self-explanatory.
- B) Document the reasoning behind key decisions, not just the final "what."
- C) Rely on the original architect staying available indefinitely instead of writing anything down.
- D) Treat documentation as unnecessary as long as the codebase itself stays well-organized.

---

## Scenario B: RAG and Model Selection for a Manufacturing Predictive-Maintenance Platform (Questions 16–30)

Ferrotech Industrial wants Claude to answer plant engineers' questions using both general reasoning and retrieval over a large, constantly-updated corpus of maintenance manuals, sensor telemetry logs, and work-order history. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most engineer questions are moderately complex; a small fraction require deep multi-sensor diagnostic reasoning, and a small fraction are simple lookups (e.g., a threshold value).

- A) Use one fixed model tier for every question, regardless of how complex it turns out to be.
- B) Always use the highest-capability tier, to guarantee quality even on the simplest lookups.
- C) Always use the fastest tier to minimize cost, accepting quality loss on the hardest cases.
- D) Route by difficulty: a fast tier for lookups, a balanced tier for typical questions, a higher-capability tier for deep diagnostics.

**Question 17.** Every request sends the same long system prompt (engineer persona, safety-disclaimer language, formatting rules) followed by retrieved document excerpts that vary per query.

- A) Assume prompt order doesn't affect cost or latency for a retrieval-heavy, high-volume workload like this.
- B) Place the stable system prompt first with caching enabled, retrieved content after it.
- C) Put the retrieved document excerpts first, since they're most relevant to the specific query.
- D) Alternate system instructions and retrieved content throughout the prompt to keep both fresh.

**Question 18.** The corpus mixes long-form maintenance manuals with short structured data (sensor telemetry logs and vibration thresholds).

- A) Assume one chunking and indexing strategy tuned for long-form manuals serves both content types equally well.
- B) Exclude structured telemetry data from retrieval entirely, keeping the pipeline manual-only.
- C) Use the largest possible chunk size for everything, avoiding the need for multiple strategies.
- D) Match chunking and indexing strategy to each data shape, since manuals and telemetry need different handling.

**Question 19.** Engineer queries range from exact lookups ("current vibration threshold for pump model X") to conceptual questions ("why has bearing failure on line 3 increased over the last quarter").

- A) Use only embedding similarity search, for exact lookups and conceptual questions alike.
- B) Match retrieval strategy to query pattern: structured filtering, embeddings, or hybrid as needed.
- C) Use only structured metadata filtering, even for the open-ended conceptual questions.
- D) Assume query pattern doesn't meaningfully affect which retrieval approach fits best here.

**Question 20.** Engineers need citations that reliably map each maintenance recommendation to a specific manual and section, and generic prose responses often lose this mapping.

- A) Add a system prompt instruction to "always cite sources," with no further output structure.
- B) Define a citation schema in the documentation, then keep generating prose responses without enforcing it.
- C) Append a general bibliography of consulted manuals at the end of each response.
- D) Require structured output pairing each claim with its source, so the mapping survives synthesis.

**Question 21.** Two retrieved sources disagree on a sensor's rated failure threshold — likely because one reflects an older manual revision and the other a newer one.

- A) Average the two threshold values and present the blended number as the single answer, without noting the disagreement.
- B) Omit the threshold entirely from the response, since the two sources disagree.
- C) Present both values with attribution and the likely explanation, flagged as a discrepancy.
- D) Always prefer whichever source the retrieval system happened to return first.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Enforce schema-constrained output via tool use, and consider lowering temperature for added consistency.
- B) Repeat the "always output valid JSON" instruction more emphatically in the prompt text.
- C) Post-process every response to strip any leading text before the first `{`.
- D) Increase max_tokens, on the theory that extra room fixes both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary CMMS (computerized maintenance management system), exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this platform.

- A) Hard-code the CMMS integration as a structured internal module used only by this platform's application code.
- B) Build an MCP server exposing CMMS operations as reusable tools/resources.
- C) Paste the entire work-order history into every prompt that might reference it.
- D) Have each consuming tool reimplement its own CMMS integration independently.

**Question 24.** The team is deciding between exposing the full equipment catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Load the full equipment catalog into every prompt up front, for the sake of completeness.
- B) Assume there's no meaningful context-cost difference between the two approaches as the fleet grows.
- C) Use progressive discovery: query a catalog resource only when the task actually needs it.
- D) Never expose the catalog to the agent in any form, blocking lookups entirely.

**Question 25.** An engineer asks a question requiring the model to reason step by step across several sensor readings and manual sections before concluding on a likely root cause.

- A) Use chain-of-thought prompting, allowing explicit intermediate reasoning across sources.
- B) Use zero-shot prompting with no reasoning guidance; it performs identically on this task.
- C) Assume chain-of-thought prompting only helps with coding tasks, not diagnostic ones.
- D) Assume the model can't reason across multiple sources regardless of how it's prompted.

**Question 26.** The platform wants to standardize prompt fragments (safety-disclaimer language, unit-formatting rules, citation format) across several different maintenance-facing features so changes propagate consistently.

- A) Duplicate the shared fragments into each feature's system prompt independently, updating each copy by hand whenever wording changes.
- B) Assume prompt caching alone makes multi-turn output deterministic across features, replacing the need for modular fragments.
- C) Assume standardization across features isn't achievable through prompt design.
- D) Use modular, versioned prompt fragments shared across features — distinct from caching or Skills.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific torque value from the correctly retrieved manual section.

- A) Verify extracted values against the actual source excerpt rather than trusting confident phrasing.
- B) Trust fluent, well-formatted output as evidence that the extracted value is correct.
- C) Treat this as a pure model limitation the architecture has no way to mitigate.
- D) Increase output length, on the theory that more room produces more accurate answers.

**Question 28.** The team debates whether latency SLAs for line-side technicians should factor into model tier selection for the maintenance platform.

- A) Yes — weigh accuracy needs against the latency/cost the SLA can tolerate, rather than defaulting to the top tier.
- B) No — latency should never factor into model or architecture decisions of any kind.
- C) Only cost should factor into tier selection; latency SLAs are irrelevant to the choice.
- D) SLAs are purely a stakeholder-communication concern with no bearing on technical architecture, model tier, or infrastructure choices.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Keep floating to "latest" automatically in production, since a newer model is always better.
- B) Never upgrade the model once an initial version has been chosen for the platform.
- C) Upgrade immediately without testing, since improved benchmark scores guarantee production gains.
- D) Pin the current version and evaluate the new one against the platform's own tests before upgrading.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output share one context-window budget, so retrieved content trades off against answer room.
- B) Assume this tradeoff only matters for unusually long documents, never for typical queries.
- C) Assume output length has no practical limit regardless of input size, since output tokens are billed and windowed separately.
- D) Treat input and output token budgets as entirely independent of each other.

---

## Scenario C: Evaluation and Optimization of a Fraud-Detection Triage System (Questions 31–45)

A Claude-powered system at Cascade Pay triages flagged transactions to decide which get auto-cleared, auto-blocked, or escalated to a human fraud analyst. It's been in production for several months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only fraud-catch rate and hasn't defined targets for latency, cost, or safety.

- A) Treat fraud-catch rate alone as sufficient, since it's the system's stated primary purpose.
- B) Define metrics spanning accuracy, latency, cost, and safety as first-class targets.
- C) Treat latency and cost as operations concerns with no bearing on evaluation design.
- D) Treat safety metrics as relevant only to more heavily regulated industries than payments.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past transactions.

- A) Treat a single automated method against a fixed labeled set as sufficient for any production system.
- B) Replace the automated checks entirely with human review of every flagged transaction.
- C) Expand the labeled set indefinitely, treating dataset size as the sole improvement lever.
- D) Use mixed methods: automated eval for scale, human review for nuance, adversarial testing for safety paths.

**Question 33.** The team wants to test whether a new prompt version improves triage precision before rolling it out to all traffic.

- A) Roll the new prompt out to all traffic immediately and monitor informally for problems.
- B) Change the prompt and the model tier at the same time, to maximize potential improvement.
- C) Skip testing, on the assumption prompt changes are inherently low-risk.
- D) Run an A/B test changing only the prompt version against a stable baseline.

**Question 34.** A flagged transaction was wrongly cleared as legitimate. Investigation shows the underlying risk-signal data was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) Treat this as a generation issue and fix the prompt or add output validation to catch inaccurate paraphrasing.
- B) Treat this as a retrieval problem and rework the indexing pipeline.
- C) Conclude this can't be diagnosed without retraining the underlying model.
- D) Treat this as a model-tier mismatch requiring an upgrade to the next capability tier, regardless of what the investigation actually showed.

**Question 35.** Immediately after a scheduled risk-signal feed refresh, the system starts flagging legitimate transactions as fraud, while model version and average latency are unchanged.

- A) Suspect the model provider silently pushed an update to the underlying model.
- B) Suspect a temperature setting changed, assuming that would make flagging behavior perfectly deterministic again.
- C) Suspect the context window shrank, cutting off part of the risk signal.
- D) Investigate the retrieval/ingestion layer first, since the regression tracks the feed refresh.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting fraud-catch accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Optimize cost, latency, and accuracy independently, treating each as unrelated to the others.
- B) Maximize accuracy regardless of cost or latency, since fraud-catch is the system's core job.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget.
- D) Treat this tradeoff as unmeasurable, something that can only be guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average precision score.

- A) Treat a single aggregate weekly average as sufficient for production monitoring.
- B) Track only cost in monitoring, since the eval suite alone already covers accuracy.
- C) Surface drift via per-merchant-category or per-transaction-type breakdowns, not just an aggregate.
- D) Treat weekly granularity as always sufficient, regardless of how the system is behaving.

**Question 38.** The team proposes cutting manual review of flagged transactions by 80%, citing a 97% aggregate precision score.

- A) Proceed with the 80% review cut based on the 97% aggregate figure alone.
- B) Treat aggregate accuracy as definitionally representative of every merchant segment.
- C) Segment accuracy by merchant category and transaction type before cutting review.
- D) Refuse any reduction in human review, regardless of what the measured accuracy shows.

**Question 39.** An A/B test shows a new prompt version improves fraud-catch rate but the team hasn't checked whether it also increased the false-positive rate on legitimate high-value transactions.

- A) Check the false-positive rate on high-value legitimate transactions before shipping the change.
- B) Treat fraud-catch rate alone as a sufficient signal to ship the new prompt version.
- C) Treat false-positive behavior as something evaluation is structurally unable to measure, unlike fraud-catch rate itself.
- D) Ship the change and monitor informally afterward instead of testing it beforehand.

**Question 40.** The team wants to diagnose why a subset of correctly-flagged fraud alerts are rated as low quality by the fraud-ops team, who cite unclear reasoning in the alert write-up.

- A) Assume the accuracy metric's validation logic itself is broken and discard the metric entirely.
- B) Increase the model's capability tier, assuming higher capability always raises ops satisfaction.
- C) Investigate explanation clarity or actionability as a quality dimension the current eval doesn't measure.
- D) Ignore fraud-ops satisfaction scores and rely on the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full transaction history plus a large static risk-policy document on every turn of multi-turn triage-review conversations.

- A) Treat this as unoptimizable, since full transaction history is always required on every turn.
- B) Switch to a smaller model as the only lever considered for reducing token cost.
- C) Cache the static risk-policy document and trim or summarize older review-conversation turns.
- D) Remove the risk-policy document entirely from the prompt to save tokens.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Treat raw logging at full volume, already structured by timestamp and request ID, as sufficient observability on its own.
- B) Reduce logging volume to save storage cost, with no other change to the approach.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged categories, segment metrics.
- D) Treat observability as needing no structure as long as the data is retained somewhere.

**Question 43.** The team wants to identify whether a specific quality regression was caused by a recent prompt change, a recent model version change, or a risk-data change — all three happened in the same week.

- A) Assume the most recently shipped change is always the cause of a regression.
- B) Treat attribution as impossible once multiple changes have shipped in the same week.
- C) Revert all three changes without investigating which one, if any, actually caused the regression, to be safe.
- D) Isolate and re-test each of the three changes independently to attribute the regression correctly.

**Question 44.** An automated eval asserts that a fraud-explanation output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) Conclude the model is malfunctioning and needs retraining.
- B) Loosen the schema slightly and make the reference string longer, on the theory that either change fixes the failures.
- C) Replace exact-string-match with a check for required content/structure, since output isn't fully deterministic.
- D) Increase the temperature setting to fix the intermittent eval failures.

**Question 45.** Leadership wants a single number to represent "how good" the fraud-triage system is, to track over time.

- A) Treat a single number as always achievable and sufficient for any system's evaluation needs.
- B) Use a top-line number, but pair it with segment-level and multi-dimensional detail underneath.
- C) Use fraud-catch rate alone as the single number, since it's the system's stated purpose.
- D) Refuse to provide any single summary metric to leadership, under any circumstances.

---

## Scenario D: Governance and Stakeholder Communication for a Banking GDPR Deployment (Questions 46–60)

Alderbrook Bank, a European retail bank, is deploying a Claude-powered system that processes customer service requests containing personal data and assists a 40-person compliance-operations team using Claude Code internally. You are responsible for governance, GDPR compliance, and stakeholder communication for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) Treat this sequencing as low-risk, since compliance requirements can always be layered on right before launch with minor patches.
- B) Recognize that GDPR-driven requirements can force costly structural retrofits this late in a build.
- C) Treat compliance as affecting only legal documentation, not system architecture.
- D) Treat HIPAA, not GDPR, as the relevant regime for a European retail bank.

**Question 47.** A team proposes requiring human approval on every single output the customer-service system produces, framing it as the safest governance posture.

- A) Target human-in-the-loop at high error-cost or genuinely judgment-requiring decisions, not every output.
- B) Require maximal human review on every output, as the correct default for banking AI systems.
- C) Treat human reviewers as categorically less accurate than the model across every decision type, making review counterproductive.
- D) Treat blanket review on every output as required by GDPR, regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from customer-submitted free text, and inconsistent output — as part of its design.

- A) Address these risks only once they're actually observed happening in production.
- B) Design a mitigation for each failure mode up front — grounding, input isolation, consistency checks.
- C) Treat these risks as exclusive to non-banking use cases.
- D) Rely on a single generic guardrail to address hallucination, injection, and inconsistency equally well.

**Question 49.** Stakeholders ask whether the system's lending-related outputs could produce disparate outcomes across different customer demographics.

- A) Treat this as a legal/compliance matter entirely, with no architectural concern before launch.
- B) Evaluate whether training/eval data reflects the served population and measure for disparate impact.
- C) Treat disparate impact as impossible in an LLM-based system by construction.
- D) Treat this concern as relevant only to systems making the final lending decision outright.

**Question 50.** The 40-person compliance-operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each of the 40 staff individually troubleshoot their own local configuration.
- B) Restrict Claude Code usage to a single designated engineer to reduce variance across the team.
- C) Accept the inconsistency as an unavoidable cost of rolling AI tooling out to a large team.
- D) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team level.

**Question 51.** The team wants Claude Code-generated code changes in this banking context to go through the same review rigor as any other change to a regulated system.

- A) Let AI-assisted code bypass the standard review process entirely, since it was "written by AI" rather than by a human engineer.
- B) Apply only a spot-check to AI-generated code, rather than the standard review process.
- C) Apply a lower review bar to AI-generated code than to human-written code in this system.
- D) Keep standard SDLC review, testing, and version-control practices unchanged, regardless of who generated the diff.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigating the integration layer at all.
- B) Disable Claude Code for the team entirely, since generated code can never be adequately validated.
- C) Triage it like any incident: use traces/logs to localize whether the failure is in integration or in the generated logic.
- D) Roll back every recent Claude Code-assisted change across the whole platform, regardless of whether it's related to this specific incident.

**Question 53.** The compliance-operations team wants a documented, repeatable workflow for a recurring task (generating a weekly GDPR data-subject-request summary report) versus a one-off exploratory coding task.

- A) Build both the recurring report and the one-off task as ad hoc, undocumented prompts each time.
- B) Package the recurring report as a Skill for reuse; leave the one-off task as an ad hoc session.
- C) Build both the recurring report and the one-off exploratory task as dedicated MCP servers.
- D) Build the recurring workflow and the one-off task using identical tooling and structure.

**Question 54.** The compliance team wants documented evidence of who accessed what customer data through the system and when, to satisfy GDPR accountability obligations.

- A) Design access control and audit logging as explicit architectural components, not an implicit byproduct.
- B) Treat access logging as optional, as long as the system already has role-based permissions and single sign-on configured.
- C) Treat audit logging as something that can be added later without any architectural impact.
- D) Log only failed access attempts, since those are the ones accountability reviews typically ask about.

**Question 55.** The steering committee for this deployment includes retail-banking, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor communication to each audience — tradeoffs framed in terms retail-banking and legal can evaluate.
- B) Communicate only with engineering stakeholders, trusting them to relay information to the others.
- C) Skip stakeholder communication with retail-banking and legal until the system is fully built.
- D) Use identical technical documentation for all three audiences, to save preparation effort.

**Question 56.** Midway through the project, the compliance team's requirements shift meaningfully based on new EDPB regulatory guidance.

- A) Refuse to incorporate the EDPB-driven change, since requirements were already agreed upon.
- B) Incorporate the change silently, without informing stakeholders of its downstream impact.
- C) Restart the entire project from scratch, regardless of how narrow the change's actual scope is.
- D) Re-engage discovery for the affected scope and communicate the tradeoff to stakeholders.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to Alderbrook's operations team.

- A) Extend lifecycle responsibility through monitoring and iteration, treating production signal as an architectural hook back into the design rather than stopping at handoff.
- B) Treat lifecycle responsibility as ending once the contract with Alderbrook is signed.
- C) Treat monitoring as necessary only if a major incident eventually occurs.
- D) Treat handoff as correct: monitoring and iteration become entirely the operations team's responsibility.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) Treat listing final configuration values as sufficient, since the "what" is all a future team needs.
- B) Treat documenting reasoning as unnecessary overhead, especially in a regulated environment.
- C) Restrict modification rights to the original architect, making further documentation moot.
- D) Capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — alongside the "what."

**Question 59.** The compliance-operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling saves time on every task category by default, without measuring it.
- B) Ban Claude Code for all documentation tasks without evaluating where it actually helps.
- C) Mandate Claude Code usage for all tasks, regardless of measured benefit.
- D) Evaluate specific task categories for genuine friction reduction versus added review overhead.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) Accept the redundant re-derivation across the team as an ongoing inefficiency with no realistic architectural fix available.
- B) Document the triage process for distinguishing integration-layer failures from model-output failures.
- C) Restrict debugging on this system to a single designated engineer.
- D) Conclude the issue can only be resolved by switching to a different tool entirely.

---
# Answer Key — Practice Exam 5

**Quick key:** 1-B, 2-C, 3-B, 4-C, 5-C, 6-D, 7-B, 8-A, 9-B, 10-A, 11-C, 12-C, 13-A, 14-A, 15-B, 16-D, 17-B, 18-D, 19-B, 20-D, 21-C, 22-A, 23-B, 24-C, 25-A, 26-D, 27-A, 28-A, 29-D, 30-A, 31-B, 32-D, 33-D, 34-A, 35-D, 36-C, 37-C, 38-C, 39-A, 40-C, 41-C, 42-C, 43-D, 44-C, 45-B, 46-B, 47-A, 48-B, 49-B, 50-D, 51-D, 52-C, 53-B, 54-A, 55-A, 56-D, 57-A, 58-D, 59-D, 60-B

---

**1. B** — The actual driver is a capability the current process entirely lacks (a new specialty line), which is a transformation story, not an efficiency one. A and C misname the pillar discovery actually surfaced; D skips framing entirely.

**2. C** — Steps that vary by applicant industry, loss history, and mid-review findings are the defining case for an agentic pattern. A assumes a predictability underwriting doesn't have here; B undersells the orchestration needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. B** — Hub-and-spoke routing through the coordinator preserves observability and consistent error handling. A and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. C** — Every subagent succeeding while whole policy categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap.

**5. C** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, B, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. D** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and B treat it as out of scope; C overreacts to sentiment alone without weighing it against the technical case.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. C and D withhold the reasoning stakeholders need; A removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures underwriter overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. B** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; C is factually wrong.

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not writing around it or growing the context window. B and C ignore this real degradation; D targets the wrong lever entirely.

**11. C** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (document intake) completes, reducing latency without sacrificing correctness. A and B misstate real constraints; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; D skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. D** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex diagnostic questions. A and B ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. D** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and C ignore this mismatch; B discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; a bare system-prompt request and an unenforced schema are exactly the patterns that lose or fail to guarantee that mapping. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. C** — Presenting both figures with attribution and likely explanation preserves the actual information for the engineer rather than resolving a real discrepancy arbitrarily. A, B, and D all discard or obscure a genuine data conflict.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift; lowering temperature is a reasonable secondary lever for consistency once structure is enforced. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. B** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, C, and D all fail the reuse or maintainability requirement.

**24. C** — Progressive discovery via a queryable catalog resource scales with fleet growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-source diagnostic synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. D** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; C denies a real, common architecture pattern.

**27. A** — Verifying extracted values against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. A** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. B, C, and D each drop a relevant factor from the decision.

**29. D** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it catches fraud. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. A** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. B and D misdiagnose the layer at fault; C avoids diagnosis entirely.

**35. D** — A regression tied specifically to a data-refresh event, with model and latency unchanged, points first at retrieval/ingestion. A, B, and C would not specifically correlate with a feed refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. C** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and D accept a monitoring blind spot; B drops accuracy monitoring from observability entirely.

**38. C** — Segmenting accuracy by merchant category and transaction type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. A** — An isolated fraud-catch improvement could mask a worsened false-positive rate on legitimate transactions; checking specifically for that before shipping is the correct diagnostic step. B and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. C** — "Correct but poorly rated" points at an unmeasured quality dimension (explanation clarity, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. C** — Caching the static risk-policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn review conversations. A denies an obvious lever; D removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable, however consistently they're timestamped. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. B** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and C oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. B** — GDPR-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. A** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. B and C overstate the universal safety case for maximal review; D misattributes this requirement to GDPR, which doesn't mandate it.

**48. B** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, consistency checks for output drift) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; C is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. D** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and C leave the systemic cause unaddressed; B sacrifices the tool's benefit for the rest of the team.

**51. D** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, B, and C all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. A** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct, especially under GDPR accountability obligations. B, C, and D each understate what compliance-grade audit evidence actually requires.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by retail-banking, legal, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. D** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; C disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. D** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and C all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 5.*
