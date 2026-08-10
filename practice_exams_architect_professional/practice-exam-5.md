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

- A) Frame the architecture around efficiency, since most AI initiatives are efficiency plays regardless of what discovery found.
- B) Frame the architecture around transformation, since the actual driver is a new capability the current process entirely lacks, not a faster version of an existing one.
- C) Frame the architecture around cost reduction, since underwriting automation always reduces cost.
- D) Skip framing around a specific value pillar and let the build proceed without one.

**Question 2.** Underwriting risk assessment, pricing, and policy issuance each require different steps depending on the applicant's industry, prior loss history, and information uncovered mid-review.

- A) A fixed workflow, since underwriting is a mature, standardized business process.
- B) An augmented LLM pattern, since a single retrieval-enhanced call can underwrite any commercial policy.
- C) An agentic pattern, since the right sequence of steps varies by case and depends on intermediate findings uncovered during review.
- D) Whichever pattern requires the fewest engineering resources, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (risk scoring, pricing, compliance check, policy drafting).

- A) Let subagents communicate directly to skip a hop, minimizing latency.
- B) Route all inter-subagent communication through the coordinator, preserving observability and consistent error handling.
- C) Merge all four responsibilities into one subagent to avoid coordination overhead.
- D) Let subagents communicate directly, but log the traffic for later review.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition only routes single-state policies to the pipeline — multi-state package policies are never routed to any subagent and silently fall through.

- A) Add a fifth subagent specifically for edge cases.
- B) Add a prompt instruction telling subagents to flag policies they don't recognize.
- C) Fix the coordinator's decomposition so it explicitly covers all policy categories, including multi-state package policies, rather than tuning the existing subagents.
- D) Give the existing subagents broader tool access so they can handle any policy type.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian actually cares about, distinct from a generic "we added AI" narrative.

- A) Business value pillars are a sales concern, not an architectural one.
- B) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.
- C) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- D) Any AI system inherently demonstrates transformation, so no further framing is needed.

**Question 6.** Meridian's underwriters are skeptical of automation and worried about job security; discovery interviews surface this repeatedly.

- A) Ignore the sentiment since it's not a technical requirement.
- B) Proceed with the technical design and let change management handle it separately with no architectural input.
- C) Recommend against the project entirely based on the sentiment.
- D) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.

**Question 7.** A stakeholder asks why the risk-scoring subagent uses a higher-capability, higher-cost model tier than the document-drafting subagent.

- A) Use the same tier everywhere for simplicity, regardless of task difficulty.
- B) Explain the tradeoff explicitly: risk scoring needs deeper reasoning that justifies the added cost/latency, while document drafting is simpler and better served by a faster, cheaper tier.
- C) "Higher tier because it's more important" is a sufficient answer.
- D) Avoid explaining tier differences, since stakeholders don't need technical detail.

**Question 8.** The architecture's current design produces a final pricing recommendation with no mechanism to learn from underwriter overrides or outcomes over time.

- A) Add a feedback loop capturing underwriter overrides and outcomes as a first-class architectural component, so the system can improve post-deployment.
- B) This is acceptable since the initial design already reflects best practice.
- C) Feedback loops are a data science concern unrelated to the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** Meridian wants a single enhanced LLM call — with retrieval of policy wording — to answer straightforward certificate-of-insurance lookups, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- C) This cannot be built with Claude at all, since it doesn't involve an agent.
- D) This requires a fixed workflow with at least five sequential steps.

**Question 10.** The document-intake subagent's toolset has grown to include tools for tasks like billing lookup and customer notification that are unrelated to document intake.

- A) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or relocated to a more appropriate subagent.
- B) This has no architectural downside as long as the subagent's prompt is well-written.
- C) More tools always improve a subagent's flexibility and should be encouraged.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each application sequentially through document intake, risk scoring, compliance check, and pricing, even though risk scoring and compliance check have no dependency on each other's output.

- A) Sequential processing is required for auditability.
- B) Parallelization is not possible with a coordinator/subagent architecture.
- C) Run risk scoring and compliance check as independent, parallel subagent calls once document intake completes, rather than sequentially.
- D) Combine risk scoring and compliance check into a single subagent to avoid the sequencing question.

**Question 12.** Meridian asks how the end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and token costs involved.
- B) Present the full technical architecture diagram with no simplification.
- C) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, risk scoring, compliance checking, pricing) rather than a coordinator with specialized subagents.

- A) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.
- B) A single generalist agent scales better as tool count grows.
- C) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- D) There's no meaningful architectural difference between the two approaches.

**Question 14.** The underwriting architecture must eventually support a new line (parametric crop insurance) Meridian is planning to launch next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- B) Ignore future lines of business until requirements exist.
- C) Build full support for parametric crop insurance now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: RAG and Model Selection for a Manufacturing Predictive-Maintenance Platform (Questions 16–30)

Ferrotech Industrial wants Claude to answer plant engineers' questions using both general reasoning and retrieval over a large, constantly-updated corpus of maintenance manuals, sensor telemetry logs, and work-order history. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most engineer questions are moderately complex; a small fraction require deep multi-sensor diagnostic reasoning, and a small fraction are simple lookups (e.g., a threshold value).

- A) Use one fixed model tier for all questions, regardless of complexity.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.
- D) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-sensor diagnostic cases.

**Question 17.** Every request sends the same long system prompt (engineer persona, safety-disclaimer language, formatting rules) followed by retrieved document excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- C) Put retrieved content first since it's most relevant to the specific query.
- D) Alternate system instructions and retrieved content throughout the prompt.

**Question 18.** The corpus mixes long-form maintenance manuals with short structured data (sensor telemetry logs and vibration thresholds).

- A) One chunking and indexing strategy tuned for long-form manuals can serve both content types equally well.
- B) Structured telemetry data should be excluded from retrieval entirely.
- C) Use the largest possible chunk size for everything to avoid needing multiple strategies.
- D) Chunking and indexing strategy should match each data shape — long-form manuals need different chunking than structured telemetry records, or retrieval quality degrades for whichever type doesn't match.

**Question 19.** Engineer queries range from exact lookups ("current vibration threshold for pump model X") to conceptual questions ("why has bearing failure on line 3 increased over the last quarter").

- A) Use only embedding similarity search for every query type.
- B) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- C) Use only structured/metadata filtering for every query type.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Engineers need citations that reliably map each maintenance recommendation to a specific manual and section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Add citations after the fact by searching for a plausible source for each recommendation.
- C) Append a general bibliography of consulted manuals at the end of each response.
- D) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.

**Question 21.** Two retrieved sources disagree on a sensor's rated failure threshold — likely because one reflects an older manual revision and the other a newer one.

- A) Average the two values and present the average.
- B) Omit the threshold entirely since sources disagree.
- C) Present both values explicitly annotated as a discrepancy, with source attribution and the likely explanation (e.g., manual revision), rather than silently picking one.
- D) Always prefer whichever source was retrieved first.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- B) Repeat the instruction more emphatically in the prompt.
- C) Post-process every response to strip leading text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary CMMS (computerized maintenance management system), exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this platform.

- A) Hard-code the CMMS integration into this platform's application code only.
- B) Build an MCP server exposing the CMMS operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- C) Paste the entire work-order history into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full equipment catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) There's no meaningful difference in context cost between the two approaches.
- C) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the equipment fleet grows.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** An engineer asks a question requiring the model to reason step by step across several sensor readings and manual sections before concluding on a likely root cause.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-source diagnostic synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple sources regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (safety-disclaimer language, unit-formatting rules, citation format) across several different maintenance-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Modular prompts are the same thing as prompt caching.
- C) Standardization across features isn't achievable with prompt design.
- D) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific torque value from the correctly retrieved manual section.

- A) Apply defensive validation — verify extracted values against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- B) Trust the fluent, well-formatted output as evidence of correctness.
- C) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether latency SLAs for line-side technicians should factor into model tier selection for the maintenance platform.

- A) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- B) Latency should never factor into model or architecture decisions.
- C) Only cost should factor into tier selection, never latency.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Never upgrade models once the initial version is chosen.
- C) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.
- D) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Output length has no practical limit regardless of input size.
- D) Input and output token budgets are entirely independent of each other.

---

## Scenario C: Evaluation and Optimization of a Fraud-Detection Triage System (Questions 31–45)

A Claude-powered system at Cascade Pay triages flagged transactions to decide which get auto-cleared, auto-blocked, or escalated to a human fraud analyst. It's been in production for several months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only fraud-catch rate and hasn't defined targets for latency, cost, or safety.

- A) Fraud-catch rate alone is sufficient since it's the system's primary purpose.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that catches fraud but is too slow, too expensive, or unsafe still fails overall.
- C) Latency and cost are operations concerns unrelated to evaluation design.
- D) Safety metrics are only relevant for regulated industries.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past transactions.

- A) A single automated method is sufficient for any production system.
- B) Replace the automated checks entirely with only human review.
- C) Expand the labeled set indefinitely as the sole improvement lever.
- D) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new prompt version improves triage precision before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Skip testing since prompt changes are low-risk by nature.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.

**Question 34.** A flagged transaction was wrongly cleared as legitimate. Investigation shows the underlying risk-signal data was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) This is best characterized as a prompt/generation issue (inaccurate summarization of correctly retrieved signals), which calls for prompt or output-validation fixes rather than retrieval changes.
- B) This is a retrieval problem; fix the indexing pipeline.
- C) This cannot be diagnosed without retraining the model.
- D) This is a model mismatch requiring a different model tier regardless of the specific failure.

**Question 35.** Immediately after a scheduled risk-signal feed refresh, the system starts flagging legitimate transactions as fraud, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Suspect a temperature setting change, since flagging behavior changed.
- C) Suspect the context window shrank.
- D) Investigate the retrieval/data-ingestion layer first, since the regression is tied specifically to the feed-refresh event with model and latency unchanged.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting fraud-catch accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average precision score.

- A) A single aggregate average is sufficient for production monitoring.
- B) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- C) Monitoring should surface drift and outliers — a per-merchant-category or per-transaction-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting manual review of flagged transactions by 80%, citing a 97% aggregate precision score.

- A) Proceed with the cut based on the 97% aggregate figure alone.
- B) Aggregate accuracy is definitionally representative of every segment.
- C) Segment accuracy by merchant category and transaction type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new prompt version improves fraud-catch rate but the team hasn't checked whether it also increased the false-positive rate on legitimate high-value transactions.

- A) Check the false-positive rate on legitimate high-value transactions specifically before shipping — an isolated fraud-catch improvement could be masking an increase in inappropriate blocks.
- B) Fraud-catch rate alone is a sufficient signal to ship the change.
- C) False-positive behavior is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** The team wants to diagnose why a subset of correctly-flagged fraud alerts are rated as low quality by the fraud-ops team, who cite unclear reasoning in the alert write-up.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves ops satisfaction.
- C) Investigate a dimension beyond factual accuracy — e.g., explanation clarity or actionability — since "correct but poorly rated" points at a quality dimension the current eval doesn't measure.
- D) Ignore fraud-ops satisfaction scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full transaction history plus a large static risk-policy document on every turn of multi-turn triage-review conversations.

- A) This has no optimization opportunity since full history is always required.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Apply prompt caching to the static risk-policy document and consider trimming or summarizing older turns of the review conversation to reduce redundant token cost.
- D) Remove the risk-policy document entirely to save tokens.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a specific quality regression was caused by a recent prompt change, a recent model version change, or a risk-data change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) Revert all three changes without investigation, regardless of which (if any) caused the regression.
- D) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.

**Question 44.** An automated eval asserts that a fraud-explanation output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the fraud-triage system is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.
- C) Use fraud-catch rate alone as the single number, since it's the system's stated purpose.
- D) Refuse to provide any single summary metric under any circumstances.

---

## Scenario D: Governance and Stakeholder Communication for a Banking GDPR Deployment (Questions 46–60)

Alderbrook Bank, a European retail bank, is deploying a Claude-powered system that processes customer service requests containing personal data and assists a 40-person compliance-operations team using Claude Code internally. You are responsible for governance, GDPR compliance, and stakeholder communication for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) GDPR-driven data residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- C) Compliance only affects legal documentation, not system architecture.
- D) HIPAA, not GDPR, is the relevant regime for a European bank.

**Question 47.** A team proposes requiring human approval on every single output the customer-service system produces, framing it as the safest governance posture.

- A) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- B) Maximal human review on every output is always the correct default for banking AI systems.
- C) Human reviewers are categorically less accurate than the model, making review counterproductive.
- D) This approach is required by GDPR regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from customer-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- C) These risks are exclusive to non-banking use cases.
- D) A single generic guardrail addresses all three risk types equally well.

**Question 49.** Stakeholders ask whether the system's lending-related outputs could produce disparate outcomes across different customer demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final lending decisions, not any assistive system.

**Question 50.** The 40-person compliance-operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each staff member individually troubleshoot their own local configuration.
- B) Restrict Claude Code usage to a single designated engineer to reduce variance.
- C) Accept the inconsistency as an unavoidable cost of AI tooling adoption.
- D) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.

**Question 51.** The team wants Claude Code-generated code changes in this banking context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Only a spot-check of AI-generated code is necessary.
- C) Review requirements should be lower for AI-generated code than human-written code.
- D) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code for the team entirely following any incident.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The compliance-operations team wants a documented, repeatable workflow for a recurring task (generating a weekly GDPR data-subject-request summary report) versus a one-off exploratory coding task.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what customer data through the system and when, to satisfy GDPR accountability obligations.

- A) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- B) Access logging is optional if the system has role-based permissions.
- C) Audit logging can be added later without architectural impact.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this deployment includes retail-banking, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor architectural communication to each audience — tradeoffs framed in terms retail-banking and legal/compliance stakeholders can evaluate against their own priorities, not just engineering metrics.
- B) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- C) Skip stakeholder communication until the system is fully built.
- D) Use identical technical documentation for all three audiences to save effort.

**Question 56.** Midway through the project, the compliance team's requirements shift meaningfully based on new EDPB regulatory guidance.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Incorporate the change silently without informing stakeholders of the impact.
- C) Restart the entire project from scratch regardless of the change's actual scope.
- D) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to Alderbrook's operations team.

- A) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- B) Lifecycle responsibility ends once the contract is signed.
- C) Monitoring is only necessary if a major incident occurs.
- D) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Only the original architect should ever be allowed to modify the system, making documentation moot.
- D) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.

**Question 59.** The compliance-operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Ban Claude Code for all documentation tasks without evaluation.
- C) Mandate Claude Code usage for all tasks regardless of measured benefit.
- D) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging to a single designated engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

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

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. B and C ignore this real degradation; D doesn't address selection reliability at all.

**11. C** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (document intake) completes, reducing latency without sacrificing correctness. A and B misstate real constraints; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; D skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. D** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex diagnostic questions. A and B ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. D** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and C ignore this mismatch; B discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. C** — Presenting both figures with attribution and likely explanation preserves the actual information for the engineer rather than resolving a real discrepancy arbitrarily. A, B, and D all discard or obscure a genuine data conflict.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

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

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. B** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and C oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. B** — GDPR-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. A** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. B and C overstate the universal safety case for maximal review; D misattributes this requirement to GDPR, which doesn't mandate it.

**48. B** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; C is factually wrong.

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
