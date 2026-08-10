# CCARP Practice Exam 8

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Customer-Escalation Platform for a Telecom Retailer, Model Selection and Context Engineering for a Retail Merchandising Copilot, Evaluation and Monitoring of a Field-Service Dispatch Assistant, Governance and Team Enablement for an Insurance Claims Modernization) |
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

## Scenario A: Multi-Agent Customer-Escalation Platform for a Telecom Retailer (Questions 1–15)

Northfield Mobile, a regional telecom retailer, is building a Claude-powered platform to handle escalated customer contacts — billing disputes, service outages, and retention saves — that its front-line chat system can't resolve. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Northfield's operations stakeholders.

---

**Question 1.** Discovery reveals Northfield's actual goal is reducing average escalation handle time by 30% with the same headcount, not adding capabilities the current process lacks.

- A) Frame the architecture around transformation, since AI projects should aim to create new capability.
- B) Frame the architecture around cost reduction exclusively, regardless of what discovery surfaced.
- C) Skip framing around a specific value pillar, since the system either works or it doesn't.
- D) Frame the architecture around efficiency, and build success metrics around handle time per agent rather than novel capability.

**Question 2.** Escalation intake, categorization, and routing to the correct back-office queue follow a fixed, well-established sequence of steps that doesn't vary case to case, regardless of dispute type.

- A) An agentic pattern, since routing benefits from autonomy regardless of predictability.
- B) A fixed workflow, since the steps are well-defined and don't depend on intermediate findings.
- C) An augmented LLM pattern, since a single enhanced call is sufficient for any escalation workflow.
- D) Whichever pattern is fastest to implement, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (billing-dispute analysis, outage diagnostics, retention-offer calculation, resolution drafting).

- A) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- B) Let each subagent communicate results directly to whichever subagent needs them next, to minimize hops.
- C) Merge all four responsibilities into one subagent to avoid coordination overhead.
- D) Let subagents communicate directly, but log the traffic for later review.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition assigned only billing and outage cases to the pipeline — retention escalations and legal-threat complaints are never routed to any subagent and silently fall through.

- A) Add a fifth subagent specifically for edge cases.
- B) Add a prompt instruction telling subagents to flag cases they don't recognize.
- C) Give the existing subagents broader tool access so they can handle any case type.
- D) Fix the coordinator's decomposition so it explicitly covers all escalation categories, including retention and legal-threat cases, rather than tuning the existing subagents.

**Question 5.** The design must align technical architecture to a specific business value pillar Northfield actually cares about, distinct from a generic "we added AI" narrative.

- A) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- B) Any AI system inherently demonstrates transformation, so no further framing is needed.
- C) Business value pillars are a sales concern, not an architectural one.
- D) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.

**Question 6.** Northfield's frontline escalation agents fear the new system will be used to justify layoffs, and raise this repeatedly during discovery interviews.

- A) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- B) Ignore the sentiment since it's not a technical requirement.
- C) Proceed with the technical design and let change management handle it separately with no architectural input.
- D) Recommend against the project entirely based on the sentiment.

**Question 7.** A stakeholder asks why the retention-offer subagent uses a higher-capability, higher-cost model tier than the categorization subagent.

- A) "Higher tier because it's more important" is a sufficient answer.
- B) Avoid explaining tier differences, since stakeholders don't need technical detail.
- C) Explain the tradeoff explicitly: retention offers require deeper reasoning about financial exposure that justifies the added cost/latency, while categorization is simpler and better served by a faster, cheaper tier.
- D) Use the same tier everywhere for simplicity, regardless of task difficulty.

**Question 8.** The architecture's current design produces a final retention-offer recommendation with no mechanism to learn whether the customer accepted the offer or churned anyway.

- A) This is acceptable since the initial design already reflects best practice.
- B) Feedback loops are a data science concern unrelated to the architecture.
- C) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.
- D) Add a feedback loop capturing offer acceptance and churn outcomes as a first-class architectural component, so the system can improve post-deployment.

**Question 9.** Northfield wants a single enhanced LLM call — with retrieval of current plan details — to answer straightforward "what's my current plan" questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) This cannot be built with Claude at all, since it doesn't involve an agent.
- C) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- D) This requires a fixed workflow with at least five sequential steps.

**Question 10.** The billing-dispute subagent's toolset has grown to include tools for scheduling technician truck rolls and adjusting loyalty-tier status, unrelated to billing disputes.

- A) This has no architectural downside as long as the subagent's prompt is well-written.
- B) More tools always improve a subagent's flexibility and should be encouraged.
- C) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each escalation sequentially through categorization, outage diagnostics, retention-offer calculation, and resolution drafting, even though outage diagnostics and retention-offer calculation have no dependency on each other's output.

- A) Sequential processing is required for auditability.
- B) Run outage diagnostics and retention-offer calculation as independent, parallel subagent calls once categorization completes, rather than sequentially.
- C) Parallelization is not possible with a coordinator/subagent architecture.
- D) Combine outage diagnostics and retention-offer calculation into a single subagent to avoid the sequencing question.

**Question 12.** Northfield's steering committee, unfamiliar with technical details, asks how the end-to-end architecture should be described at a high level.

- A) Present only the model names and token costs involved.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- C) Present the full technical architecture diagram with no simplification.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (billing, outage diagnostics, retention, drafting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- C) There's no meaningful architectural difference between the two approaches.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The escalation platform must eventually support a new category (5G home-internet escalations) Northfield plans to launch next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- B) Ignore future categories until requirements exist.
- C) Build full support for 5G home-internet escalations now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Rely on the original architect remaining available indefinitely instead of documenting.
- C) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

Meridian Home Goods wants Claude to help merchandising planners answer questions ranging from simple SKU price lookups to complex, multi-region assortment tradeoff analysis, using retrieval over vendor contracts, sales reports, and inventory data. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Planner questions range from simple SKU lookups to complex multi-region assortment tradeoff analysis requiring deep reasoning.

- A) Always use the highest-capability tier for every query regardless of complexity.
- B) Route based on task difficulty — a fast tier for simple SKU lookups, a balanced tier for typical planning questions, and a higher-capability tier reserved for complex multi-region tradeoff analysis.
- C) Use one fixed mid-tier model for all queries regardless of complexity.
- D) Always use the fastest/cheapest tier to minimize cost, accepting quality loss on complex analysis.

**Question 17.** Every request sends the same long system prompt (merchandising rules, tone, formatting) followed by retrieved sales-data excerpts that vary per query.

- A) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- B) Alternate system instructions and retrieved content throughout the prompt.
- C) Put retrieved content first since it's most relevant to the specific query.
- D) Order doesn't affect cost or latency for this use case.

**Question 18.** The corpus mixes long-form vendor contracts with short structured SKU/price tables.

- A) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- B) Structured data should be excluded from retrieval entirely.
- C) Use the largest possible chunk size for everything to avoid needing multiple strategies.
- D) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.

**Question 19.** Planner queries range from exact lookups ("current price for SKU 48213") to conceptual questions ("how has our outdoor-furniture assortment mix shifted over two years").

- A) Use only embedding similarity search for every query type.
- B) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- C) Use only structured/metadata filtering for every query type.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Planners need each pricing recommendation reliably mapped to its specific source (vendor contract clause, sales report section), and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Add citations after the fact by searching for a plausible source for each claim.
- C) Append a general bibliography of consulted documents at the end of each response.
- D) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.

**Question 21.** Two systems disagree on the current on-hand inventory count for a SKU by a meaningful margin — likely due to a stale nightly sync in one of them.

- A) Average the two figures and present the average.
- B) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely explanation (e.g., a stale sync), rather than silently picking one.
- C) Always prefer whichever source was retrieved first.
- D) Omit the inventory figure entirely since sources disagree.

**Question 22.** A prompt asking the model to "always output valid structured JSON with source fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Increase max_tokens to leave room for both the preamble and the JSON.
- C) Post-process every response to strip leading text before the first `{`.
- D) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.

**Question 23.** The platform needs to connect to a proprietary vendor-catalog system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just the merchandising copilot.

- A) Build an MCP server exposing the vendor-catalog operations as tools/resources, reusable across the multiple internal tools that need it.
- B) Hard-code the vendor-catalog integration into this copilot's application code only.
- C) Paste the entire vendor catalog into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full vendor catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the catalog grows.
- B) Loading the full catalog up front is always preferable for completeness.
- C) There's no meaningful difference in context cost between the two approaches.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** A planner asks a question requiring the model to reason step by step across several sales reports before concluding on an assortment recommendation.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (formatting rules, disclaimer language, tone) across several different planner-facing features so changes propagate consistently.

- A) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- B) Duplicate the fragments into each feature's prompt independently.
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-formatted answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- C) Increase output length so there's more room to be correct.
- D) This is not something an architecture can address; it's purely a model limitation with no mitigation.

**Question 28.** The team debates whether planner-facing latency SLAs should factor into model tier selection for the copilot.

- A) Latency should never factor into model or architecture decisions.
- B) Only cost should factor into tier selection, never latency.
- C) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Never upgrade models once the initial version is chosen.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.

**Question 30.** The copilot's context budget is a concern because both the system prompt/formatting rules and the retrieved excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- D) Output length has no practical limit regardless of input size.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

Cascade Utilities uses a Claude-powered assistant to triage and assign field technicians to service jobs based on urgency, required skills, and location. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only technician-assignment accuracy and hasn't defined targets for latency, cost, or safety.

- A) Accuracy alone is sufficient since it's the system's primary purpose.
- B) Latency and cost are operations concerns unrelated to evaluation design.
- C) Safety metrics are only relevant for regulated industries.
- D) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that assigns technicians well but is too slow, too expensive, or unsafe still fails overall.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch decisions.

- A) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- B) A single automated method is sufficient for any production system.
- C) Replace the automated checks entirely with only human review.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new prioritization-scoring prompt improves dispatch quality before rolling it out to all technicians.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip testing since prompt changes are low-risk by nature.

**Question 34.** A dispatch recommendation assigns the wrong-skilled technician. Investigation shows the skill-matrix lookup was correct and retrieved properly, and the model's job-summary paraphrase mischaracterized the required skill.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled technician-roster and skill-matrix refresh, the assistant starts making poor assignments, while model version and average latency are unchanged.

- A) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.
- B) Suspect the model was silently updated by the provider.
- C) Suspect a temperature setting change, since confidence changed.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average assignment-accuracy score.

- A) Monitoring should surface drift and outliers — a per-region or per-job-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence dispatch decisions by 75%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone.
- B) Aggregate accuracy is definitionally representative of every segment.
- C) Human review should never be reduced regardless of measured accuracy.
- D) Segment accuracy by region and job type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.

**Question 39.** An A/B test shows a new prioritization prompt improves on-time-arrival rate, but the team hasn't checked whether it increased mis-escalations of complex, safety-critical jobs that should route to senior technicians.

- A) On-time-arrival rate alone is a sufficient signal to ship the change.
- B) Check the escalation-related failure mode specifically before shipping — an isolated on-time improvement could be masking an increase in inappropriate routing of complex, safety-critical jobs.
- C) False-positive escalation behavior is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** A subset of dispatch assignments are technically correct (right skill match) but rated poorly by technicians in satisfaction surveys, often citing unreasonable travel distance.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves satisfaction.
- C) Investigate a dimension beyond skill-match correctness — e.g., travel burden or workload balance — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- D) Ignore technician satisfaction scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full technician-roster history plus a large static skill-matrix reference document on every dispatch decision.

- A) Apply prompt caching to the static skill-matrix document and consider trimming or summarizing older roster history to reduce redundant token cost.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Remove the skill-matrix document entirely to save tokens.
- D) This has no optimization opportunity since full history is always required.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Observability requires no structure as long as data is retained somewhere.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.

**Question 43.** The team wants to identify whether a quality regression was caused by a recent prompt change, a recent model version change, or a roster-data schema change — all three shipped in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- D) Revert all three changes without investigation, regardless of which (if any) caused the regression.

**Question 44.** An automated eval asserts that a dispatch-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use on-time-arrival rate alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

Harborline Insurance is deploying a Claude-powered system that assists claims adjusters with intake, coverage lookup, and payout recommendations, alongside a 25-person claims-engineering team using Claude Code internally to build and maintain it. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) State insurance-regulation requirements around data residency, retention, and access control can force structural changes that are far more costly to retrofit than to design in from the start.
- B) This sequencing carries no risk since compliance can always be added right before launch.
- C) Compliance only affects legal documentation, not system architecture.
- D) HIPAA, not state insurance regulation, is the relevant regime for this claims system.

**Question 47.** A team proposes requiring human approval on every single claims-adjudication output, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for regulated AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) This approach is required by GDPR regardless of other considerations.
- D) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) These risks are exclusive to non-insurance use cases.
- C) A single generic guardrail addresses all three risk types equally well.
- D) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.

**Question 49.** The claims team asks whether the system's payout recommendations could produce disparate outcomes across different policyholder demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final payout decisions, not any assistive system.

**Question 50.** The 25-person claims-engineering team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each staff member individually troubleshoot their own local configuration.
- B) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this regulated claims system to go through the same review rigor as any other change.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a spot-check of AI-generated code is necessary.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated claims-data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code for the team entirely following any incident.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The claims-ops team wants a documented, repeatable workflow for a recurring task (generating a weekly reserve-adequacy summary report) versus a one-off exploratory investigation task.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Build both as MCP servers regardless of reuse profile.
- C) Recurring workflows and one-off tasks should be built identically.
- D) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant data through the system and when.

- A) Access logging is optional if the system has role-based permissions.
- B) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- C) Audit logging can be added later without architectural impact.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this deployment includes claims-ops, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms claims-ops and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- C) Use identical technical documentation for all three audiences to save effort.
- D) Skip stakeholder communication until the system is fully built.

**Question 56.** Midway through the project, claims-handling requirements shift meaningfully based on new state insurance-regulation guidance.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Incorporate the change silently without informing stakeholders of the impact.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims-operations team.

- A) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- B) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- C) Lifecycle responsibility ends once the contract is signed.
- D) Monitoring is only necessary if a major incident occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- C) Documenting reasoning is unnecessary overhead in a regulated environment.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The claims-ops team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Ban Claude Code for all documentation tasks without evaluation.
- C) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- D) Mandate Claude Code usage for all tasks regardless of measured benefit.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging to a single designated engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key

**Quick key:** 1-D, 2-B, 3-A, 4-D, 5-A, 6-A, 7-C, 8-D, 9-C, 10-C, 11-B, 12-B, 13-D, 14-A, 15-C, 16-B, 17-A, 18-D, 19-B, 20-D, 21-B, 22-D, 23-A, 24-A, 25-A, 26-A, 27-B, 28-C, 29-C, 30-C, 31-D, 32-A, 33-C, 34-D, 35-A, 36-C, 37-A, 38-D, 39-B, 40-C, 41-A, 42-D, 43-C, 44-C, 45-D, 46-A, 47-D, 48-D, 49-B, 50-B, 51-B, 52-C, 53-D, 54-B, 55-B, 56-C, 57-A, 58-B, 59-C, 60-B

---

**1. D** — The stated goal (less handle time, same headcount) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. B** — Steps that are well-defined and don't vary case to case are the defining case for a fixed workflow, not autonomous orchestration. A overstates the need for agentic autonomy; C undersells what a genuinely multi-step, standardized process needs; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. A** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. B and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. D** — Every subagent succeeding while whole escalation categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and C all patch downstream instead of fixing the actual scope gap.

**5. A** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. B, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. A** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. B and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. C** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. D** — Adding a feedback loop that captures offer acceptance and churn outcomes as a first-class architectural component is what lets the system improve after deployment. A, B, and C all treat a first-class architectural component as optional or someone else's problem.

**9. C** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; B is factually wrong.

**10. C** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and B ignore this real degradation; D doesn't address selection reliability at all.

**11. B** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (categorization) completes, reducing latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. C** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and D all leave the actual knowledge transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and D ignore or sacrifice fit-to-task; C forces one tier onto queries with very different needs.

**17. A** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. B, C, and D all misstate or break the caching opportunity.

**18. D** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and C ignore this mismatch; B discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. B** — Presenting both figures with attribution and a likely explanation preserves the actual information for the planner rather than resolving a real discrepancy arbitrarily. A, C, and D all discard or obscure a genuine data conflict.

**22. D** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. C** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and D all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it assigns technicians well. A, B, and C each drop a dimension that materially affects whether the system is actually working well.

**32. A** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. B, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. A** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. B, C, and D would not specifically correlate with a roster/skill-matrix refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. D** — Segmenting accuracy by region and job type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; C over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated on-time-arrival improvement could mask a worsened escalation failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (travel burden, workload balance) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. A** — Caching the static skill-matrix document and trimming/summarizing older roster history directly reduces redundant token cost. D denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. C** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. A** — State insurance-regulation requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. B and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. D** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; C misattributes this to GDPR, which isn't the relevant regime described.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. D** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B over-engineers the one-off task; C ignores that reuse profile should drive the choice.

**54. B** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, C, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims-ops, legal, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. B** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, C, and D all leave that reasoning undocumented and effectively lost.

**59. C** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 8.*
