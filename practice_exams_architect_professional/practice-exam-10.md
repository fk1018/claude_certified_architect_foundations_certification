# CCARP Practice Exam 10

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent Supply-Chain and Logistics Orchestration Platform, RAG Integration for a Legal Case-Law Research Platform, Evaluation and A/B Testing of a Sales-Forecasting Copilot, Lifecycle Management and Enablement for a Global Manufacturing Rollout) |
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

## Scenario A: Multi-Agent Supply-Chain and Logistics Orchestration Platform (Questions 1–15)

Meridian Freight Systems, a mid-market logistics provider, wants to modernize its order-to-delivery pipeline — carrier-capacity procurement, route/mode selection, in-transit exception handling, and customs/compliance checks — using a Claude-powered multi-agent architecture. You are the architect leading discovery and design.

---

**Question 1.** Discovery reveals the real business driver is reducing carrier detention and demurrage fees by 30%, not adding capabilities the current process lacks.

- A) Frame around transformation, since AI projects should always aim to add novel capability.
- B) Frame around throughput/efficiency exclusively, regardless of what discovery found.
- C) Skip pillar framing; a working system speaks for itself.
- D) Frame around cost reduction, anchoring both the architecture and success metrics on detention/demurrage fee reduction.

**Question 2.** Procurement, mode selection, and exception handling each require different steps depending on carrier responses, inventory position, and disruptions discovered mid-shipment.

- A) An agentic pattern, since the right steps vary by shipment and depend on intermediate findings.
- B) A fixed workflow, since freight logistics is a standardized process.
- C) An augmented LLM pattern, since one enhanced call suffices for any logistics task.
- D) Whichever pattern is quickest to prototype, since the patterns are interchangeable.

**Question 3.** The design has a coordinator delegating to subagents (procurement, routing, exception-handling, customs-compliance). Every subagent works correctly, but shipments requiring both a customs hold and a carrier substitution are never routed to any subagent — they fall through silently.

- A) Add a fifth subagent specifically for edge cases.
- B) Instruct subagents to flag unfamiliar shipments in their own prompts.
- C) Broaden existing subagents' tool access so any subagent can handle any case.
- D) Fix the coordinator's decomposition so it explicitly covers compound cases like simultaneous customs holds and carrier substitutions, rather than tuning subagents.

**Question 4.** Meridian's ops leadership wants the architecture aligned to a specific, named business value pillar rather than a generic "we added AI" narrative.

- A) Efficiency, cost, transformation, and performance-SLA pillars are examples; the chosen one should drive both the architecture and its success metrics.
- B) Any automated system inherently demonstrates transformation.
- C) Business value pillars belong to sales, not architecture.
- D) Choose the pillar after launch, based on whichever benefit is easiest to report.

**Question 5.** Dispatch coordinators are skeptical of the system and worried it will replace their jobs; this comes up repeatedly in discovery interviews.

- A) Ignore the sentiment; it isn't a technical requirement.
- B) Proceed with the design and let change management address it later, entirely outside the architecture.
- C) Recommend cancelling the project based on the sentiment alone.
- D) Treat the sentiment as a real implicit constraint that shapes rollout sequencing and where human-in-the-loop checkpoints matter most.

**Question 6.** A stakeholder asks why the exception-handling subagent uses a higher-capability, higher-cost model tier than the procurement subagent.

- A) "It's the more important subagent" is a sufficient answer on its own.
- B) Avoid explaining tier differences since stakeholders don't need technical detail.
- C) Explain the tradeoff explicitly: exception handling requires deeper reasoning over ambiguous, disruptive events, justifying the added cost/latency, while procurement is more routine and better served by a faster tier.
- D) Use the same tier everywhere for simplicity, regardless of task difficulty.

**Question 7.** The current design produces a route/mode recommendation with no mechanism to learn from dispatcher overrides or actual delivery outcomes.

- A) This is acceptable since the initial design reflects current best practice.
- B) Add a feedback loop capturing dispatcher overrides and delivery outcomes as a first-class architectural component, so the system can improve post-deployment.
- C) Feedback loops belong to a data science team, not the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 8.** Meridian's customer-service team wants a single enhanced LLM call — with retrieval over the carrier-rate/contract database — to answer straightforward "what's my current rate to lane X" questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of task simplicity.
- B) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- C) This requires a fixed workflow with at least five sequential steps.
- D) This cannot be built with Claude since it involves no autonomous agent.

**Question 9.** The procurement subagent's toolset has grown to include tools for tasks like driver payroll lookup and warehouse-staffing scheduling, unrelated to procurement.

- A) This has no architectural downside if the prompt is well-written.
- B) More tools always improve a subagent's flexibility and should be encouraged.
- C) The fix is to increase the subagent's context window.
- D) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.

**Question 10.** The coordinator currently processes each shipment sequentially through procurement, routing, exception-check, and customs-check, even though routing and customs-check have no dependency on each other's output.

- A) Sequential processing is required for auditability.
- B) Run routing and customs-check as independent, parallel subagent calls once procurement completes, rather than sequentially.
- C) Parallelization isn't possible in a coordinator/subagent architecture.
- D) Combine routing and customs-check into a single subagent to avoid the sequencing question.

**Question 11.** Meridian's executive steering committee, unfamiliar with technical detail, asks for a high-level description of the architecture.

- A) Present only model names and token costs involved.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- C) Present the full technical architecture diagram with no simplification.
- D) Skip a high-level description and go straight into an implementation demo.

**Question 12.** A competing vendor proposes a single generalist agent holding every tool (procurement, routing, exception handling, customs) instead of a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) There's no meaningful architectural difference between the two approaches.
- C) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.
- D) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.

**Question 13.** The architecture must eventually support a new mode of transport (intermodal rail) Meridian plans to add next year, but detailed requirements aren't yet available.

- A) Ignore future transport modes until requirements exist.
- B) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- C) Build full intermodal-rail support now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 14.** The steering committee wants documentation a new engineering team can use to extend the system in a year, without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code is well-organized.

**Question 15.** Discovery also surfaces that Meridian's warehouse-staffing team assumed this project would also automate staffing schedules, which was never in scope.

- A) Clarify and document scope explicitly with stakeholders now, rather than let the assumption persist into later delivery conflict.
- B) Quietly build staffing automation too, to avoid disappointing anyone.
- C) Ignore the misunderstanding since it wasn't in the original requirements document.
- D) Cancel the current project until every stakeholder's expectations are unified.

---

## Scenario B: RAG Integration for a Legal Case-Law Research Platform (Questions 16–30)

Caselight is a legal research platform that wants Claude to answer attorney questions using retrieval over case law, statutes, and secondary treatises, combined with general reasoning. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most attorney queries are moderately complex research questions; a small fraction require deep multi-step reasoning across many cases, and a small fraction are simple citation lookups.

- A) Route based on task difficulty — a fast tier for simple citation lookups, a balanced tier for typical research questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-case cases.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Use one fixed model tier for all questions, regardless of complexity.
- D) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.

**Question 17.** Every request sends the same long system prompt (jurisdiction rules, citation style, formatting requirements) followed by retrieved case excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Place the stable system prompt first and enable prompt caching, with the varying retrieved excerpts after it, to reduce both latency and cost across the high query volume.
- C) Put retrieved excerpts first since they're most relevant to the specific query.
- D) Alternate system instructions and retrieved content throughout the prompt.

**Question 18.** The corpus mixes long-form judicial opinions with short structured data (a table of statute citations and effective dates).

- A) One chunking and indexing strategy tuned for long-form opinions can serve both content types equally well.
- B) Chunking and indexing strategy should match each data shape — long-form opinions need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.
- C) Structured statute data should be excluded from retrieval entirely.
- D) Use the largest possible chunk size for everything to avoid needing multiple strategies.

**Question 19.** Attorney queries range from exact lookups ("cite for Smith v. Jones") to conceptual questions ("how has the reasonable-reliance standard evolved across circuits").

- A) Use only embedding similarity search for every query type.
- B) Use only structured/metadata filtering for every query type.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact citation lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Attorneys need citations that reliably map each legal claim to a specific case and pincite, and generic prose responses often lose this mapping.

- A) Require structured output pairing each claim with its source (case name, reporter citation, pincite, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- B) Ask the model, in prose, to "always cite sources" without further structure.
- C) Add citations after the fact by searching for a plausible case for each claim.
- D) Append a general bibliography of consulted cases at the end of each response.

**Question 21.** Two retrieved cases disagree on how a particular statute of limitations is tolled — likely because they're from different circuits with different precedent.

- A) Average the two positions and present a blended rule.
- B) Omit the tolling analysis entirely since sources disagree.
- C) Always prefer whichever case was retrieved first.
- D) Present both positions explicitly, attributed to their respective circuits, rather than silently picking one or blending them.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Increase max_tokens to leave room for both the preamble and the JSON.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- D) Post-process every response to strip leading text before the first `{`.

**Question 23.** The platform needs to connect to a proprietary internal brief bank, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Hard-code the brief-bank integration into this platform's application code only.
- B) Paste the entire brief bank into every prompt.
- C) Build an MCP server exposing the brief-bank operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team debates between exposing the full case-law catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) There's no meaningful difference in context cost between the two approaches.
- C) The catalog should never be exposed to the agent in any form.
- D) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the corpus grows.

**Question 25.** An attorney asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved opinions before concluding on a multi-factor test.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document, multi-factor synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, jurisdiction disclaimers, formatting rules) across several different attorney-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific holding from the correctly retrieved opinion.

- A) Apply defensive validation — verify extracted holdings against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- B) Trust the fluent, well-formatted output as evidence of correctness.
- C) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether attorney-facing latency SLAs should factor into model tier selection for the research platform.

- A) Latency should never factor into model or architecture decisions.
- B) Only cost should factor into tier selection, never latency.
- C) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- B) Continue floating to latest automatically, since newer is always better.
- C) Never upgrade models once the initial version is chosen.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved case excerpts must fit alongside room for a detailed analytical answer.

- A) Input and output token budgets are entirely independent of each other.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Output length has no practical limit regardless of input size.
- D) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.

---

## Scenario C: Evaluation and A/B Testing of a Sales-Forecasting Copilot (Questions 31–45)

A Claude-powered copilot at Northwind Analytics helps sales reps and managers forecast pipeline and deal close probability. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and running A/B tests on prompt/model changes.

---

**Question 31.** The team currently measures only forecast accuracy against actuals and hasn't defined targets for latency, cost, or safety/guardrail behavior.

- A) Forecast accuracy alone is sufficient since it's the system's primary purpose.
- B) Latency and cost are operations concerns unrelated to evaluation design.
- C) Safety metrics are only relevant for regulated industries.
- D) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that forecasts well but is too slow, too expensive, or unsafe still fails overall.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed set of past quarters' actual outcomes.

- A) A single automated method is sufficient for any production system.
- B) Replace the automated checks entirely with only human review.
- C) Use mixed methodologies — automated eval for scale, human review (sales-manager judgment) for nuanced calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new prompt version improves forecast-narrative quality before rolling it out to all sales reps.

- A) Roll out the new prompt to all reps immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Skip testing since prompt changes are low-risk by nature.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.

**Question 34.** A forecast narrative is factually wrong about a deal's stage. Investigation shows the CRM data was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled CRM data-sync refresh, the copilot starts producing confident but incorrect deal-stage references, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Suspect a temperature setting change, since confidence changed.
- C) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data-sync event with model and latency unchanged.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting forecast accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall monthly average forecast-accuracy score across all sales regions, hiding drift specific to one region.

- A) Monitoring should surface drift and outliers — a per-region or per-deal-size breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- D) Monthly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting manager review of flagged low-confidence forecasts by 80%, citing a 96% aggregate accuracy score.

- A) Segment accuracy by region and deal size before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- B) Proceed with the cut based on the 96% aggregate figure alone.
- C) Aggregate accuracy is definitionally representative of every segment.
- D) Manager review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new prompt version improves narrative-quality ratings, but the team has not checked whether it also changed the rate of overconfident forecasts on genuinely volatile deals that should be flagged as uncertain.

- A) Check the uncertainty-flagging failure mode specifically before shipping — an isolated narrative-quality improvement could be masking an increase in inappropriate overconfidence on volatile deals.
- B) Narrative-quality rating alone is a sufficient signal to ship the change.
- C) Overconfidence behavior is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** The team wants to diagnose why a subset of forecasts are numerically accurate but rated as unhelpful by sales managers in feedback surveys.

- A) Investigate a dimension beyond numerical accuracy — e.g., actionability, explanation quality, or relevance to the manager's specific pipeline — since "accurate but unhelpful" points at a quality dimension the current eval doesn't measure.
- B) Assume the accuracy metric is broken and discard it.
- C) Increase the model's capability tier, assuming higher capability always improves helpfulness.
- D) Ignore manager feedback scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends the full deal history plus a large static sales-methodology reference on every turn of multi-turn conversations with reps.

- A) This has no optimization opportunity since full history is always required.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Remove the sales-methodology reference entirely to save tokens.
- D) Apply prompt caching to the static methodology reference and consider trimming or summarizing older turns of conversation history to reduce redundant token cost across a multi-turn conversation.

**Question 42.** Logging captures every raw prompt and response for the production copilot, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Observability requires no structure as long as data is retained somewhere.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.

**Question 43.** The team wants to identify whether a specific forecast-quality regression was caused by a recent prompt change, a recent model version change, or a CRM schema change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- C) Attribution is impossible once multiple changes have shipped in the same week.
- D) Revert all three changes without investigation, regardless of which (if any) caused the regression.

**Question 44.** An automated eval asserts that a forecast-narrative output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the sales-forecasting copilot is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use forecast accuracy alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Lifecycle Management and Enablement for a Global Manufacturing Rollout (Questions 46–60)

Ferrotech Industries, a global manufacturer, is rolling out a Claude-powered production-line quality-inspection assistant across plants in multiple countries, alongside internal Claude Code enablement for its distributed engineering teams. You are responsible for governance, phased global rollout, lifecycle management, and developer enablement.

---

**Question 46.** The architecture team is finalizing data residency, retention, and access-logging design for plant-floor quality data in the final weeks before the first regional rollout, after core application logic is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) Compliance only affects legal documentation, not system architecture.
- C) Cross-border data residency, retention, and access-control requirements (e.g., EU vs. APAC plants) can force structural changes that are far more costly to retrofit than to design in from the start.
- D) A single global data-handling policy is guaranteed to satisfy every plant's local regulatory regime.

**Question 47.** A team proposes requiring human approval on every single output the quality-inspection system produces across all plants, framing it as the safest governance posture for a global rollout.

- A) Maximal human review on every output is always the correct default for manufacturing AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions (e.g., borderline defect calls) rather than applied universally.
- D) This approach is required by every relevant regulatory regime regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from free-text inspector notes, and inconsistent output — as part of its design across every plant.

- A) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- B) These risks only need to be addressed if they're observed in production first.
- C) A single generic guardrail addresses all three risk types equally well.
- D) These risks are exclusive to consumer-facing use cases, not internal manufacturing tools.

**Question 49.** The plant-safety team asks whether the system's defect-flagging decisions could produce inconsistent outcomes across different plants with different equipment vintages and lighting conditions.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Disparate outcomes across plants are impossible in an LLM-based system by construction.
- C) Consistency and fairness across deployment contexts are architecture concerns — evaluate whether eval data reflects the range of plant conditions and measure for disparate performance rather than assuming it's absent.
- D) This concern only applies to systems making final shutdown decisions, not any assistive system.

**Question 50.** Engineering teams across Ferrotech's plants have inconsistent Claude Code usage — some plants have team conventions applied automatically, others don't, and internal MCP server access to plant systems varies by machine.

- A) Restrict Claude Code usage to a single designated global engineer to reduce variance.
- B) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the organization/project level so behavior doesn't depend on individual local setup.
- C) Have each plant's engineers individually troubleshoot their own local configuration.
- D) Accept the inconsistency as an unavoidable cost of a global rollout.

**Question 51.** The team wants Claude Code-generated code changes to plant-control-adjacent software to go through the same review rigor as any other change to a safety-relevant system.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a safety-relevant system.
- C) Only a spot-check of AI-generated code is necessary.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident at one plant traces back to a Claude Code-generated change to the inspection-data pipeline. The team can't immediately tell whether the bug is in the generated code logic or in how the plant's surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code globally across all plants following any single incident.
- C) Roll back all recent Claude Code-assisted changes at every plant regardless of relevance.
- D) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.

**Question 53.** A plant's engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly quality-defect summary report) versus a one-off exploratory investigation into a new sensor integration.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory investigation as an unstructured session, since it doesn't need standing infrastructure.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** Ferrotech's compliance team wants documented evidence of who accessed what plant-floor quality data through the system and when, across every regional deployment.

- A) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- B) Access logging is optional if the system has role-based permissions.
- C) Audit logging can be added later without architectural impact.
- D) Only failed access attempts need to be logged.

**Question 55.** The global rollout's steering committee includes plant operations, legal/compliance, and engineering stakeholders across regions, each with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Skip stakeholder communication until the system is fully rolled out to every plant.
- C) Tailor architectural communication to each audience — tradeoffs framed in terms plant operations and legal/compliance stakeholders can evaluate against their own priorities, not just engineering metrics.
- D) Use identical technical documentation for all audiences to save effort.

**Question 56.** Midway through the global rollout, requirements shift meaningfully after a new regional safety regulation is issued in one of the countries where Ferrotech operates.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Treat this as a normal part of lifecycle management — re-engage discovery for the affected region's scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- C) Incorporate the change silently without informing stakeholders of the impact.
- D) Restart the entire global rollout from scratch regardless of the change's actual scope.

**Question 57.** After the final plant's rollout, the architect's involvement is discussed as ending at handoff to each plant's local operations team.

- A) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- B) This is the correct lifecycle model; monitoring and iteration are entirely each plant's local operations responsibility.
- C) Lifecycle responsibility ends once the rollout contract is signed.
- D) Monitoring is only necessary if a major incident occurs at a specific plant.

**Question 58.** Documentation for the global rollout currently lists final configuration values (model tier, retry settings, thresholds per region) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a multi-region rollout.
- C) Documentation should also capture the "why" behind key decisions — regional compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system at any plant without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** Plant engineering teams want Claude Code to help with routine tasks (drafting maintenance documentation, exploring an unfamiliar legacy control module) but are unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Ban Claude Code for all documentation tasks without evaluation.
- C) Mandate Claude Code usage for all tasks regardless of measured benefit.
- D) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, legacy-module exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.

**Question 60.** A recurring operational issue is that different plant engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across plants.
- C) Restrict debugging to a single designated global engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key

**Quick key:** 1-D, 2-A, 3-D, 4-A, 5-D, 6-C, 7-B, 8-B, 9-D, 10-B, 11-B, 12-C, 13-B, 14-B, 15-A, 16-A, 17-B, 18-B, 19-C, 20-A, 21-D, 22-C, 23-C, 24-D, 25-A, 26-B, 27-A, 28-C, 29-A, 30-D, 31-D, 32-C, 33-D, 34-D, 35-C, 36-C, 37-A, 38-A, 39-A, 40-A, 41-D, 42-D, 43-B, 44-C, 45-D, 46-C, 47-C, 48-A, 49-C, 50-B, 51-B, 52-D, 53-B, 54-A, 55-C, 56-B, 57-A, 58-C, 59-D, 60-B

---

**1. D** — Discovery pointed to a cost driver (detention/demurrage fees), so the architecture and metrics should be anchored on cost reduction. A and B misname the pillar the discovery actually surfaced; C skips framing that keeps the project aligned to real value.

**2. A** — Steps that vary by shipment and depend on intermediate findings (carrier responses, disruptions) are the defining case for an agentic pattern. B assumes a predictability the scenario lacks; C undersells the orchestration needed; D ignores real tradeoffs between patterns.

**3. D** — Whole compound case categories never being routed at all is a coordinator decomposition gap, not a subagent performance issue. A, B, and C all patch downstream instead of fixing the actual scope gap in the coordinator's routing logic.

**4. A** — Naming a specific pillar (efficiency, cost, transformation, SLA) gives both architecture and metrics a clear anchor. B, C, and D each skip or defer that framing in ways that risk building toward the wrong measure of success.

**5. D** — Adoption sentiment from dispatchers is a real implicit constraint shaping rollout sequencing and HITL placement, not noise to dismiss. A and B treat it as out of scope; C overreacts to sentiment alone without weighing the technical case.

**6. C** — Explaining the specific tradeoff (deeper reasoning need vs. cost/latency) is the standard for communicating tier decisions to stakeholders. A and B withhold reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**7. B** — A first-class feedback loop capturing dispatcher overrides and outcomes is what lets the system improve post-deployment. A, C, and D each treat this component as optional or someone else's responsibility.

**8. B** — A single call enhanced with retrieval, without multi-step orchestration, is exactly what an augmented LLM pattern serves. A and C over-engineer a simple augmentation need; D is factually wrong.

**9. D** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows. A and B ignore this real degradation; C doesn't address selection reliability at all.

**10. B** — Independent subagent calls with no shared dependency can run in parallel once their prerequisite (procurement) completes, cutting latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**11. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail, C is too much of the wrong kind, and D skips the communication need entirely.

**12. C** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles. A, B, and D understate or deny this real architectural tradeoff.

**13. B** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need; C wastes effort guessing; D blocks current delivery unnecessarily.

**14. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge-transfer gap unaddressed.

**15. A** — Clarifying and documenting scope now prevents an unspoken assumption from becoming a delivery conflict later. B expands scope without agreement; C ignores a real stakeholder misunderstanding; D is a disproportionate reaction to a clarifiable gap.

**16. A** — Routing by task difficulty matches fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex research questions. B and D ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both positions with attribution preserves the actual information for the attorney rather than resolving a genuine jurisdictional conflict arbitrarily. A, B, and C all discard or obscure a real disagreement.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and D are workarounds for a structurally solvable problem; B doesn't address the preamble at all.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning across a multi-factor test. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. B** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. A** — Verifying extracted holdings against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. B is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. A** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. B and D assume benchmark gains transfer automatically; C over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. D** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it forecasts well. A, B, and C each drop a dimension that materially affects whether the system is actually working.

**32. C** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. C** — A regression tied specifically to a data-sync event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a CRM data-sync refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate monthly average can hide, such as region-specific drift. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by region and deal size before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. A** — An isolated narrative-quality improvement could mask a worsened overconfidence failure mode; checking specifically for that before shipping is the correct diagnostic step. B and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. A** — "Accurate but unhelpful" points at an unmeasured quality dimension (actionability, explanation quality) rather than a broken accuracy metric. B and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. D** — Caching the static methodology reference and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. B** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. C** — Cross-border data residency, retention, and access-control requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; D wrongly assumes one policy fits every regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically, like borderline defect calls. A and B overstate the universal safety case for maximal review; D makes an unsupported blanket regulatory claim.

**48. A** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. B defers to a reactive posture; C assumes one guardrail covers distinct risk types; D is factually wrong.

**49. C** — Consistency and fairness across deployment contexts are architecture concerns requiring active measurement (data representativeness across plant conditions, disparate-performance checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and D make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the organization level directly fixes the described inconsistency, which stems from relying on individual local setup. C and D leave the systemic cause unaddressed; A sacrifices the tool's benefit for the rest of the organization.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially for safety-relevant systems. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for this context.

**52. D** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory investigation unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. A** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. B, C, and D each understate what compliance-grade audit evidence actually requires.

**55. C** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by plant operations, legal/compliance, and engineering alike. A, B, and D each fail to serve at least one audience's real information need.

**56. B** — Re-engaging discovery for the affected region's scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and C mishandle a real change; D disproportionately discards unaffected work.

**57. A** — Lifecycle management extends through monitoring and iteration based on production signal, not just through discovery and handoff. B, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (regional compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend or modify the system at any plant. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 10.*
