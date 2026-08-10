# CCARP Practice Exam 4

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Customer-Escalation Platform, Model Selection and Context Engineering for Retail Merchandising, Evaluation and Monitoring of Field-Service Dispatch, Governance and Team Enablement for Insurance Claims Modernization) |
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

NorthWave Mobile, a regional telecom retailer, wants to modernize how frontline store and call-center escalations are triaged and resolved. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with NorthWave's stakeholders.

---

**Question 1.** Discovery reveals NorthWave's actual goal is reducing average escalation resolution time for the existing complaint volume, not adding new self-service capabilities the current process lacks.

- A) Frame the architecture around transformation, since AI initiatives should always introduce new capabilities.
- B) Frame the architecture around cost reduction exclusively, regardless of what discovery found.
- C) Skip framing around a specific value pillar, since success is self-evident once the system ships.
- D) Frame the architecture around efficiency, building success metrics around resolution-time reduction for the existing volume rather than novel capability.

**Question 2.** Escalation handling follows one of three well-defined steps — verify identity, check account status, apply the resolution script — always in the same order regardless of case specifics.

- A) An agentic pattern, since escalations always require autonomous, unpredictable step sequencing.
- B) A fixed workflow, since the three steps are well-defined and applied in the same order regardless of case specifics.
- C) An augmented LLM pattern, since a single enhanced call handles multi-step processes equally well.
- D) Whichever pattern is fastest to implement, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (sentiment analysis, account lookup, resolution drafting, compliance check).

- A) Let subagents communicate directly with whichever subagent needs their output next, to minimize hops.
- B) Merge all four responsibilities into one subagent to avoid coordination overhead.
- C) Let subagents communicate directly, but log the traffic for later review.
- D) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition only routes billing-dispute complaints — network-outage complaints are never routed to any subagent and silently fall through.

- A) Add a fifth subagent specifically for edge cases.
- B) Give the existing subagents broader tool access so they can handle any complaint type.
- C) Fix the coordinator's decomposition so it explicitly covers all complaint categories, including network-outage complaints, rather than tuning the existing subagents.
- D) Add a prompt instruction telling subagents to flag complaints they don't recognize.

**Question 5.** The design must align technical architecture to a specific business value pillar NorthWave actually cares about, distinct from a generic "we added AI" narrative.

- A) Business value pillars are a sales concern, not an architectural one.
- B) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- C) Any AI system inherently demonstrates transformation, so no further framing is needed.
- D) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.

**Question 6.** NorthWave's frontline store associates are worried automation will replace their role in handling escalations, and discovery interviews surface this repeatedly.

- A) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- B) Ignore the sentiment since it's not a technical requirement.
- C) Proceed with the technical design and let change management handle it separately with no architectural input.
- D) Recommend against the project entirely based on the sentiment.

**Question 7.** A stakeholder asks why the churn-risk assessment subagent uses a higher-capability, higher-cost model tier than the ticket-summarization subagent.

- A) "Higher tier because it's more important" is a sufficient answer.
- B) Explain the tradeoff explicitly: churn-risk assessment needs deeper reasoning that justifies the added cost/latency, while ticket summarization is simpler and better served by a faster, cheaper tier.
- C) Use the same tier everywhere for simplicity, regardless of task difficulty.
- D) Avoid explaining tier differences, since stakeholders don't need technical detail.

**Question 8.** The architecture's current design produces a final resolution recommendation with no mechanism to learn from agent overrides or customer outcomes over time.

- A) This is acceptable since the initial design already reflects best practice.
- B) Add a feedback loop capturing agent overrides and outcomes as a first-class architectural component, so the system can improve post-deployment.
- C) Feedback loops are a data-science concern unrelated to the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** NorthWave wants a single enhanced LLM call — with retrieval of plan and billing FAQ documents — to answer straightforward plan-question escalations, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) This cannot be built with Claude at all, since it doesn't involve an agent.
- C) This requires a fixed workflow with at least five sequential steps.
- D) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.

**Question 10.** The account-lookup subagent's toolset has grown to include tools for tasks like store-locator search and promotional-offer generation, unrelated to account lookup.

- A) This has no architectural downside as long as the subagent's prompt is well-written.
- B) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- C) More tools always improve a subagent's flexibility and should be encouraged.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each escalation sequentially through identity verification, account lookup, sentiment analysis, and resolution drafting, even though account lookup and sentiment analysis have no dependency on each other's output.

- A) Sequential processing is required for auditability.
- B) Combine account lookup and sentiment analysis into a single subagent to avoid the sequencing question.
- C) Run account lookup and sentiment analysis as independent, parallel subagent calls once identity verification completes, rather than sequentially.
- D) Parallelization is not possible with a coordinator/subagent architecture.

**Question 12.** NorthWave asks how end-to-end architecture should be described at a high level for a retail-operations steering committee unfamiliar with the technical details.

- A) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- B) Present only the model names and token costs involved.
- C) Present the full technical architecture diagram with no simplification.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (identity verification, account lookup, sentiment analysis, resolution drafting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- C) There's no meaningful architectural difference between the two approaches.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The architecture must eventually support a new escalation category (satellite-internet outage complaints) NorthWave plans to launch next year, but detailed requirements aren't available yet.

- A) Ignore future escalation categories until requirements exist.
- B) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- C) Build full support for satellite-outage complaints now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

A national retail chain wants Claude to help category managers with pricing, assortment, and promotion questions, combining general reasoning with retrieval over product catalogs, sales data, and vendor contracts. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most merchandising questions are moderately complex; a small fraction require deep multi-step analysis across many SKUs, and a small fraction are simple lookups.

- A) Use one fixed model tier for all questions, regardless of complexity.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-step cases.
- D) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.

**Question 17.** Every request sends the same long system prompt (merchandiser persona, formatting rules, pricing-policy guardrails) followed by retrieved catalog and vendor excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Alternate system instructions and retrieved content throughout the prompt.
- C) Put retrieved content first since it's most relevant to the specific query.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.

**Question 18.** The corpus mixes long-form vendor contracts with short structured data (a table of SKU-level price points).

- A) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- B) Structured data should be excluded from retrieval entirely.
- C) Use the largest possible chunk size for everything to avoid needing multiple strategies.
- D) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.

**Question 19.** Category-manager queries range from exact lookups ("current price for SKU 48213") to conceptual questions ("how has the athleisure category's margin mix shifted over the last three seasons").

- A) Use only embedding similarity search for every query type.
- B) Use only structured/metadata filtering for every query type.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Category managers need pricing claims that reliably map to a specific source document and section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Append a general bibliography of consulted documents at the end of each response.
- C) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- D) Add citations after the fact by searching for a plausible source for each claim.

**Question 21.** Two retrieved sources disagree on a SKU's current wholesale cost by a small margin — likely due to different contract effective dates.

- A) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely explanation (e.g., differing effective dates), rather than silently picking one.
- B) Average the two figures and present the average.
- C) Omit the wholesale cost figure entirely since sources disagree.
- D) Always prefer whichever source was retrieved first.

**Question 22.** A prompt asking the model to "always output valid structured JSON with a source field" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Increase max_tokens to leave room for both the preamble and the JSON.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- D) Post-process every response to strip leading text before the first `{`.

**Question 23.** The platform needs to connect to a proprietary vendor-contract management system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this copilot.

- A) Build an MCP server exposing the vendor-contract operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the vendor-contract integration into this copilot's application code only.
- C) Paste the entire vendor-contract corpus into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full SKU catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) There's no meaningful difference in context cost between the two approaches.
- C) The catalog should never be exposed to the agent in any form.
- D) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the catalog grows.

**Question 25.** A category manager asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved sales reports before concluding on a recommendation.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (pricing-guardrail language, formatting rules, disclaimer text) across several merchandiser-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- B) Trust the fluent, well-formatted output as evidence of correctness.
- C) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether merchandiser-facing latency SLAs should factor into model tier selection for the copilot.

- A) Latency should never factor into model or architecture decisions.
- B) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- C) Only cost should factor into tier selection, never latency.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Never upgrade models once the initial version is chosen.
- C) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.
- D) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.

**Question 30.** The platform's context budget is a concern because both the system prompt/guardrail rules and the retrieved catalog/vendor excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- B) Input and output token budgets are entirely independent of each other.
- C) This tradeoff only matters for very long documents, never for typical queries.
- D) Output length has no practical limit regardless of input size.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

A Claude-powered assistant helps a utility company dispatch field technicians, recommending technician assignment, scheduling windows, and triage of urgent versus routine tickets. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only the correct-technician-assignment rate and hasn't defined targets for latency, cost, or safety.

- A) Assignment-rate alone is sufficient since it's the system's primary purpose.
- B) Latency and cost are operations concerns unrelated to evaluation design.
- C) Safety metrics are only relevant for regulated industries.
- D) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that assigns well but is too slow, too expensive, or unsafe still fails overall.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch tickets.

- A) A single automated method is sufficient for any production system.
- B) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- C) Replace the automated checks entirely with only human review.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new triage-prompt version improves urgent-versus-routine classification before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip testing since prompt changes are low-risk by nature.

**Question 34.** A technician assignment is wrong. Investigation shows the underlying technician-skill database was correct and retrieved properly, and the model's reasoning misapplied the skill-match logic.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This is best characterized as a prompt/generation issue (misapplied logic over correctly retrieved data), which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled technician-skills database refresh, the system starts recommending mismatched technicians, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.
- C) Suspect a temperature setting change, since confidence changed.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting assignment accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average accuracy score.

- A) Monitoring should surface drift and outliers — a per-region or per-ticket-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence assignments by 80%, citing a 97% aggregate accuracy score.

- A) Segment accuracy by region and ticket type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- B) Proceed with the cut based on the 97% aggregate figure alone.
- C) Aggregate accuracy is definitionally representative of every segment.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new prompt version improves assignment speed, but the team has not checked whether it also changed the rate of urgent tickets misclassified as routine.

- A) Assignment-speed improvement alone is a sufficient signal to ship the change.
- B) This failure mode is not something evaluation can measure.
- C) Ship the change and monitor informally after the fact instead of testing beforehand.
- D) Check the urgent-misclassification failure mode specifically before shipping — an isolated speed improvement could be masking an increase in urgent tickets wrongly treated as routine.

**Question 40.** The team wants to diagnose why a subset of dispatch recommendations are technically correct (right technician, right time window) but rated poorly by dispatchers in feedback surveys.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves satisfaction.
- C) Ignore dispatcher satisfaction scores in favor of the accuracy metric alone.
- D) Investigate a dimension beyond correctness — e.g., clarity of reasoning, communication tone, or practicality of the suggested window — since "correct but poorly rated" points at a quality dimension the current eval doesn't measure.

**Question 41.** The team is optimizing token usage and notices the system sends full ticket history plus a large static service-policy document on every turn of multi-turn dispatch conversations.

- A) Apply prompt caching to the static policy document and consider trimming or summarizing older turns of ticket history to reduce redundant token cost across a multi-turn conversation.
- B) This has no optimization opportunity since full history is always required.
- C) Switch to a smaller model as the only lever for reducing token cost.
- D) Remove the policy document entirely to save tokens.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a quality regression was caused by a recent prompt change, a recent model version change, or a skills-database content change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- C) Attribution is impossible once multiple changes have shipped in the same week.
- D) Revert all three changes without investigation, regardless of which (if any) caused the regression.

**Question 44.** An automated eval asserts that a scheduling-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Temperature should be increased to fix the intermittent failures.
- D) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.
- B) A single number is always achievable and sufficient for any system's evaluation needs.
- C) Use assignment accuracy alone as the single number, since it's the system's stated purpose.
- D) Refuse to provide any single summary metric under any circumstances.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

An insurance carrier is deploying a Claude-powered system that processes claims intake information and assists a 25-person claims-operations team using Claude Code internally. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) Regulatory data-residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- C) Compliance only affects legal documentation, not system architecture.
- D) HIPAA, not state insurance regulation, is the relevant regime for an insurance claims client.

**Question 47.** A team proposes requiring human approval on every single output the claims-intake system produces, framing it as the safest governance posture.

- A) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- B) Maximal human review on every output is always the correct default for insurance AI systems.
- C) Human reviewers are categorically less accurate than the model, making review counterproductive.
- D) This approach is required by GDPR regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- B) These risks only need to be addressed if they're observed in production first.
- C) A single generic guardrail addresses all three risk types equally well.
- D) These risks are exclusive to non-insurance use cases.

**Question 49.** The claims-operations team asks whether the system's decisions could produce disparate outcomes across different claimant demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Disparate impact is impossible in an LLM-based system by construction.
- C) This concern only applies to systems making final claim-payout decisions, not any assistive system.
- D) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.

**Question 50.** The 25-person claims-operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each staff member individually troubleshoot their own local configuration.
- B) Restrict Claude Code usage to a single designated engineer to reduce variance.
- C) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this insurance context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a spot-check of AI-generated code is necessary.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code for the team entirely following any incident.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The claims-operations team wants a documented, repeatable workflow for a recurring task (generating a weekly claims-aging summary report) versus a one-off exploratory coding task.

- A) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- B) Build both as ad hoc, undocumented prompts each time they're needed.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant-related data through the system and when.

- A) Access logging is optional if the system has role-based permissions.
- B) Audit logging can be added later without architectural impact.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this deployment includes claims, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor architectural communication to each audience — tradeoffs framed in terms claims and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- B) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- C) Skip stakeholder communication until the system is fully built.
- D) Use identical technical documentation for all three audiences to save effort.

**Question 56.** Midway through the project, the claims team's requirements shift meaningfully based on new state insurance regulatory guidance.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Incorporate the change silently without informing stakeholders of the impact.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims-operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle responsibility ends once the contract is signed.
- C) Monitoring is only necessary if a major incident occurs.
- D) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The claims-operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

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

**Quick key:** 1-D, 2-B, 3-D, 4-C, 5-B, 6-A, 7-B, 8-B, 9-D, 10-B, 11-C, 12-A, 13-D, 14-B, 15-B, 16-C, 17-D, 18-D, 19-C, 20-C, 21-A, 22-C, 23-A, 24-D, 25-A, 26-B, 27-A, 28-B, 29-D, 30-A, 31-D, 32-B, 33-C, 34-D, 35-B, 36-C, 37-A, 38-A, 39-D, 40-D, 41-A, 42-C, 43-B, 44-D, 45-A, 46-B, 47-A, 48-A, 49-D, 50-C, 51-B, 52-C, 53-A, 54-C, 55-A, 56-C, 57-D, 58-C, 59-C, 60-B

---

**1. D** — The stated goal (faster resolution for existing volume) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. B** — Steps that are well-defined and always applied in the same order are the defining case for a fixed workflow. A overstates the unpredictability actually present; C undersells the multi-step process needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. D** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and C sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents in the first place.

**4. C** — Every subagent succeeding while whole complaint categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap.

**5. B** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. A** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. B and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and D withhold the reasoning stakeholders need; C removes a deliberate, justified difference for false simplicity.

**8. B** — Adding a feedback loop that captures agent overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. A, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and C ignore this real degradation; D doesn't address selection reliability at all.

**11. C** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (identity verification) completes, reducing latency without sacrificing correctness. A and D misstate real constraints; B avoids the sequencing question rather than answering it.

**12. A** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. B is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. B** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break the caching opportunity.

**18. D** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and C ignore this mismatch; B discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. C** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation appending are exactly the patterns that lose or fabricate mappings. A, B, and D all reintroduce the failure mode the fix is meant to prevent.

**21. A** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the category manager rather than resolving a real discrepancy arbitrarily. B, C, and D all discard or obscure a genuine data conflict.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and D are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. B** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. A** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. B** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, C, and D each drop a relevant factor from the decision.

**29. D** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it assigns technicians well. A, B, and C each drop a dimension that materially affects whether the system is actually working well.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. D** — Correctly retrieved data plus misapplied reasoning logic is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. B** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, C, and D would not specifically correlate with a skills-database refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by region and ticket type before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. D** — An isolated speed improvement could mask a worsened urgent-misclassification failure mode; checking specifically for that before shipping is the correct diagnostic step. A and C ship without adequate testing; B incorrectly claims the failure mode is unmeasurable.

**40. D** — "Correct but poorly rated" points at an unmeasured quality dimension (clarity, tone, practicality) rather than a broken accuracy metric. A and C discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. A** — Caching the static policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. B denies an obvious lever; D removes needed content; C is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. B** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and C misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. A** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. B and C oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. B** — Regulatory data-residency, retention, and access-control requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D misidentifies the applicable regulatory regime for an insurance claims client.

**47. A** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. B and C overstate the universal safety case for maximal review; D misattributes this to GDPR, which isn't the relevant regime described.

**48. A** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. B defers to a reactive posture; C assumes one guardrail covers distinct risk types; D is factually wrong.

**49. D** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and C make unsupported blanket claims.

**50. C** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; B sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims, legal, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. D** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, B, and C all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. C** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 4.*
