# CCARP Practice Exam 6

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
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

Meridian Freight Networks operates a multi-modal freight network spanning ocean, rail, and truck carriers. It wants to modernize procurement, carrier selection, routing, and exception handling (customs delays, weather disruptions, capacity shortfalls) with a Claude-powered orchestration platform. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Meridian's stakeholders.

---

**Question 1.** Discovery reveals the client's real goal is to reduce dwell time at distribution hubs by 30% using existing staff and equipment — not new capabilities the current process lacks.

- A) Frame the architecture around efficiency, and build success metrics around dwell-time reduction per existing resource rather than novel capability.
- B) Frame the architecture around transformation, since AI projects should aim to create new capability.
- C) Frame the architecture around cost reduction exclusively, regardless of what discovery surfaced.
- D) Skip framing around a specific value pillar, since the system either works or it doesn't.

**Question 2.** The customs-documentation validation step follows the same fixed sequence of checks for every shipment type, regardless of contents or destination, with no branching based on intermediate findings.

- A) An agentic pattern, since orchestration always benefits from autonomy.
- B) A single augmented LLM call, since document validation is inherently simple.
- C) A fixed workflow, since the steps are identical and predetermined regardless of case specifics.
- D) Whichever pattern requires the least tooling investment, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to four specialized subagents (procurement, carrier selection, routing optimization, exception handling).

- A) Let subagents communicate directly with whichever subagent needs the result next, minimizing hops.
- B) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- C) Merge all four responsibilities into a single subagent to avoid coordination overhead.
- D) Let subagents communicate directly, but log the traffic for later review.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition only routes domestic shipments to the pipeline — international shipments requiring customs handling are never routed to any subagent and silently fall through.

- A) Fix the coordinator's decomposition so it explicitly covers all shipment categories, including international/customs shipments, rather than tuning the existing subagents.
- B) Add a prompt instruction telling subagents to flag shipments they don't recognize.
- C) Give the existing subagents broader tool access so they can handle any shipment type.
- D) Add a fifth subagent specifically for edge cases, without changing the decomposition logic.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian actually cares about, distinct from a generic "we added AI" narrative.

- A) Business value pillars are a sales concern, not an architectural one.
- B) Efficiency, resilience, cost, and service-level pillars are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- C) Any AI system inherently demonstrates transformation, so no further framing is needed.
- D) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.

**Question 6.** Meridian's dispatch team is skeptical of automated routing decisions and worried about accountability if a shipment is misrouted; discovery interviews surface this repeatedly.

- A) Recommend against the project entirely based on the sentiment.
- B) Proceed with the technical design and let change management handle it separately with no architectural input.
- C) Ignore the sentiment since it's not a technical requirement.
- D) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape rollout sequencing and where human-in-the-loop checkpoints matter most.

**Question 7.** A stakeholder asks why the exception-handling subagent (weather, customs, disruptions) uses a higher-capability, higher-cost model tier than the load-consolidation subagent.

- A) Explain the tradeoff explicitly: exception handling needs deeper reasoning over ambiguous, high-stakes situations that justifies the added cost/latency, while load consolidation is simpler and better served by a faster, cheaper tier.
- B) Use the same tier everywhere for simplicity, regardless of task difficulty.
- C) "Higher tier because it's more important" is a sufficient answer.
- D) Avoid explaining tier differences, since stakeholders don't need technical detail.

**Question 8.** The architecture's current design produces a final routing recommendation with no mechanism to learn from dispatcher overrides or actual delivery outcomes over time.

- A) Add a feedback loop capturing dispatcher overrides and delivery outcomes as a first-class architectural component, so the system can improve post-deployment.
- B) This is acceptable since the initial design already reflects best practice.
- C) Feedback loops are a data science concern unrelated to the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** The client wants a single enhanced LLM call — with lookup of carrier contract terms — to answer straightforward rate-lookup questions from dispatchers, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) This requires a fixed workflow with at least five sequential steps.
- C) This cannot be built with Claude at all, since it doesn't involve an agent.
- D) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.

**Question 10.** The procurement subagent's toolset has grown to include tools for tasks like customer notifications and invoice generation that are unrelated to procurement.

- A) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- B) This has no architectural downside as long as the subagent's prompt is well-written.
- C) More tools always improve a subagent's flexibility and should be encouraged.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each shipment sequentially through procurement, carrier selection, routing, and exception-check, even though carrier selection and exception-check have no dependency on each other's output.

- A) Run carrier selection and exception-check as independent, parallel subagent calls once procurement completes, rather than sequentially.
- B) Sequential processing is required for auditability.
- C) Parallelization is not possible with a coordinator/subagent architecture.
- D) Combine carrier selection and exception-check into a single subagent to avoid the sequencing question.

**Question 12.** The client asks how the end-to-end logistics architecture should be described for an executive steering committee unfamiliar with technical details.

- A) Present only the model names and token costs involved.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- C) Present the full technical architecture diagram with no simplification.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single generalist agent with all tools (procurement, carrier selection, routing, exception handling) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.
- C) There's no meaningful architectural difference between the two approaches.
- D) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.

**Question 14.** The logistics architecture must eventually support a new shipment mode (temperature-controlled pharma freight) planned for next year, but detailed requirements aren't available yet.

- A) Build full support for pharma freight now, guessing at requirements.
- B) Ignore future shipment modes until requirements exist.
- C) Refuse to proceed with the current phase until the future requirements are finalized.
- D) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Rely on the original architect remaining available indefinitely instead of documenting.
- C) Documentation is unnecessary if the code is well-organized.
- D) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."

---

## Scenario B: RAG Integration for a Legal Case-Law Research Platform (Questions 16–30)

Lex Meridian is a legal research platform used by attorneys to research case law, statutes, and internal firm briefs. It wants Claude to answer research questions using both general legal reasoning and retrieval over a large, constantly-updated corpus of opinions, statutes, and briefs. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most attorney queries are moderately complex; a small fraction require deep multi-step reasoning across many precedents, and a small fraction are simple citation lookups.

- A) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-step cases.
- D) Use one fixed model tier for all questions, regardless of complexity.

**Question 17.** Every request sends the same long system prompt (legal-analyst persona, citation format, formatting rules) followed by retrieved case excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Put retrieved content first, since it's most relevant to the specific query.
- C) Alternate system instructions and retrieved content throughout the prompt.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved case excerpts after it, to reduce both latency and cost across the high query volume.

**Question 18.** Lex Meridian's corpus mixes long-form case opinions and briefs with short structured records (statute citation tables with section numbers and effective dates).

- A) Chunking and indexing strategy should match each data shape — long-form opinions need different chunking than short structured statute records, or retrieval quality degrades for whichever type doesn't match.
- B) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- C) Structured statute records should be excluded from retrieval entirely.
- D) Use the largest possible chunk size for everything to avoid needing multiple strategies.

**Question 19.** Attorney queries range from exact lookups ("what is the statute of limitations under Section 12.4") to conceptual questions ("how has the doctrine of promissory estoppel evolved across circuits").

- A) Use only embedding similarity search for every query type.
- B) Query pattern doesn't affect which retrieval approach is appropriate.
- C) Use only structured/metadata filtering for every query type.
- D) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.

**Question 20.** Attorneys need citations that reliably map each legal claim to a specific case, page, and pin cite, and generic prose responses often lose this mapping.

- A) Require structured output pairing each claim with its source (case name, citation, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- B) Ask the model, in prose, to "always cite sources" without further structure.
- C) Add citations after the fact by searching for a plausible case for each claim.
- D) Append a general bibliography of consulted cases at the end of each response.

**Question 21.** Two retrieved cases disagree on whether a particular circuit still follows a specific precedent — one appears to have been implicitly overruled by a later, uncited opinion.

- A) Average or blend the two positions into a single stated rule.
- B) Present both positions explicitly, flagged as a discrepancy, with citations and the likely explanation (e.g., possible implicit overruling), rather than silently picking one.
- C) Always prefer whichever case was retrieved first.
- D) Omit the point of law entirely, since sources disagree.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- C) Post-process every response to strip leading text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary internal brief-bank system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Build an MCP server exposing the brief-bank operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the brief-bank integration into this platform's application code only.
- C) Paste the entire brief-bank corpus into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full case-law catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) There's no meaningful difference in context cost between the two approaches.
- C) The catalog should never be exposed to the agent in any form.
- D) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the corpus grows.

**Question 25.** An attorney asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved opinions before concluding on a multi-jurisdictional issue.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different attorney-facing features so changes propagate consistently.

- A) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- B) Duplicate the fragments into each feature's prompt independently.
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate the holding of a correctly retrieved case.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- C) Apply defensive validation — verify the stated holding against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether attorney-facing latency SLAs should factor into model tier selection for the research platform.

- A) Latency should never factor into model or architecture decisions.
- B) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- C) Only cost should factor into tier selection, never latency.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.
- B) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- C) Never upgrade models once the initial version is chosen.
- D) Continue floating to latest automatically, since newer is always better.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved case excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other.
- B) Output length has no practical limit regardless of input size.
- C) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- D) This tradeoff only matters for very long documents, never for typical queries.

---

## Scenario C: Evaluation and A/B Testing of a Sales-Forecasting Copilot (Questions 31–45)

Northwind Sales Intelligence built a Claude-powered copilot that helps sales reps and managers produce and explain pipeline forecasts. It's been in production for four months, and you're responsible for the evaluation strategy, diagnosing quality issues, and running controlled tests of proposed changes.

---

**Question 31.** The team currently measures only forecast-adoption rate (how often reps accept the copilot's suggested numbers) and hasn't defined targets for latency, cost, or safety.

- A) Latency and cost are operations concerns unrelated to evaluation design.
- B) Safety metrics are only relevant for regulated industries.
- C) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that gets adopted but is too slow, too expensive, or unsafe still fails overall.
- D) Adoption rate alone is sufficient, since it's the system's primary purpose.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past forecasts.

- A) A single automated method is sufficient for any production system.
- B) Replace the automated checks entirely with only human review.
- C) Expand the labeled set indefinitely as the sole improvement lever.
- D) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new prompt version improves forecast-accuracy explanations before rolling it out to all sales regions.

- A) Roll out the new prompt to all regions immediately and monitor for problems.
- B) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- C) Change the prompt and the model tier simultaneously to maximize potential improvement.
- D) Skip testing, since prompt changes are low-risk by nature.

**Question 34.** A forecast explanation is factually wrong about a deal's stage. Investigation shows the underlying CRM data was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved data), which calls for prompt or output-validation fixes rather than retrieval changes.
- C) This cannot be diagnosed without retraining the model.
- D) This is a model mismatch requiring a different model tier regardless of the specific failure.

**Question 35.** Immediately after a scheduled CRM data sync, the copilot starts producing confident but incorrect pipeline-stage summaries, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data-sync event with model and latency unchanged.
- C) Suspect a temperature setting change, since confidence changed.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting forecast accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) This tradeoff cannot be measured, only guessed at.
- D) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.

**Question 37.** Production monitoring currently reports only an overall monthly average forecast-accuracy score across all sales regions.

- A) A single aggregate average is sufficient for production monitoring.
- B) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- C) Monitoring should surface drift and outliers — a per-region or per-deal-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- D) Monthly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence forecasts by 80%, citing a 95% aggregate accuracy score.

- A) Proceed with the cut based on the 95% aggregate figure alone.
- B) Aggregate accuracy is definitionally representative of every segment.
- C) Human review should never be reduced regardless of measured accuracy.
- D) Segment accuracy by region and deal type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.

**Question 39.** An A/B test shows a new prompt version improves forecast-adoption rate, but the team has not checked whether it also changed the rate of overconfident forecasts on genuinely volatile, hard-to-predict deals.

- A) Adoption rate alone is a sufficient signal to ship the change.
- B) Overconfidence on volatile deals is not something evaluation can measure.
- C) Ship the change and monitor informally after the fact instead of testing beforehand.
- D) Check the overconfidence failure mode specifically before shipping — an isolated adoption-rate improvement could be masking increased overconfidence on the hardest-to-predict deals.

**Question 40.** The team wants to diagnose why a subset of forecasts are technically accurate but rated poorly by sales managers in feedback surveys.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves satisfaction.
- C) Investigate a dimension beyond factual accuracy — e.g., clarity, actionability, or explanation quality — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- D) Ignore manager satisfaction scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full deal history plus a large static forecasting-methodology document on every turn of multi-turn coaching conversations.

- A) This has no optimization opportunity, since full history is always required.
- B) Remove the methodology document entirely to save tokens.
- C) Apply prompt caching to the static methodology document and consider trimming or summarizing older turns of deal history to reduce redundant token cost across a multi-turn conversation.
- D) Switch to a smaller model as the only lever for reducing token cost.

**Question 42.** Logging captures every raw prompt and response for the production copilot, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a specific quality regression was caused by a recent prompt change, a recent model version change, or a CRM schema change — all three happened in the same week.

- A) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- B) Assume the most recent change is always the cause.
- C) Attribution is impossible once multiple changes have shipped in the same week.
- D) Revert all three changes without investigation, regardless of which (if any) caused the regression.

**Question 44.** An automated eval asserts that a forecast-explanation output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the sales-forecasting copilot is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use forecast-adoption rate alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Lifecycle Management and Enablement for a Global Manufacturing Rollout (Questions 46–60)

Atlas Industrial Group is rolling out a Claude-powered quality-flagging system on production lines and Claude Code for a 40-person plant-engineering team, across multiple countries. You are responsible for governance, compliance, and developer enablement across the rollout's lifecycle.

---

**Question 46.** The architecture team is finalizing data residency, retention, and access-logging design in the final weeks before a multi-country rollout, after core application logic is already built.

- A) This sequencing carries no risk, since compliance can always be added right before launch.
- B) Cross-border data-residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- C) Compliance only affects legal documentation, not system architecture.
- D) A single global data-residency policy is sufficient regardless of which countries are involved.

**Question 47.** A team proposes requiring human approval on every single quality-flag output the production-line system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for manufacturing safety systems.
- B) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- C) Human reviewers are categorically less accurate than the model, making review counterproductive.
- D) This approach is required by ISO certification regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from operator-submitted free-text notes, and inconsistent output — as part of its design.

- A) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- B) These risks only need to be addressed if they're observed in production first.
- C) A single generic guardrail addresses all three risk types equally well.
- D) These risks are exclusive to non-manufacturing use cases.

**Question 49.** Plant management asks whether the quality-flagging system's decisions could produce disparate outcomes across different production lines or shifts with different staffing demographics.

- A) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population of lines/shifts and measure for disparate impact rather than assuming it's absent.
- B) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final personnel decisions, not any assistive system.

**Question 50.** The 40-person plant-engineering team's Claude Code usage is inconsistent across country sites — some engineers have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Restrict Claude Code usage to a single designated engineer to reduce variance.
- B) Have each engineer individually troubleshoot their own local configuration.
- C) Accept the inconsistency as an unavoidable cost of AI tooling adoption across sites.
- D) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.

**Question 51.** The team wants Claude Code-generated code changes to production-line control tooling to go through the same review rigor as any other change to a safety-relevant system.

- A) AI-assisted code should bypass standard review, since it was "written by AI."
- B) Only a spot-check of AI-generated code is necessary.
- C) Review requirements should be lower for AI-generated code than human-written code.
- D) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a safety-relevant system.

**Question 52.** A production incident traces back to a Claude Code-generated change to a data-logging module at one plant. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code for the team entirely following any incident.
- C) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- D) Roll back all recent Claude Code-assisted changes across every plant regardless of relevance.

**Question 53.** The plant-engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly cross-plant quality-metrics rollup) versus a one-off exploratory debugging task at a single site.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Build both as MCP servers regardless of reuse profile.
- C) Package the recurring, well-defined rollup workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what production and quality data through the system, and when, across all rollout sites.

- A) Access logging is optional if the system has role-based permissions.
- B) Audit logging can be added later without architectural impact.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this rollout includes plant operations, legal/compliance, and engineering stakeholders across multiple countries with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Use identical technical documentation for all three audiences to save effort.
- C) Tailor architectural communication to each audience — tradeoffs framed in terms operations and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- D) Skip stakeholder communication until the system is fully built.

**Question 56.** Midway through the rollout, requirements shift meaningfully at several plants based on a new regional safety-certification standard.

- A) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- B) Refuse to incorporate the change, since requirements were already agreed upon.
- C) Incorporate the change silently without informing stakeholders of the impact.
- D) Restart the entire rollout from scratch regardless of the change's actual scope.

**Question 57.** After the initial rollout, the architect's involvement is discussed as ending at handoff to each plant's local operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the local operations teams' responsibility.
- B) Lifecycle responsibility ends once the contract is signed.
- C) Monitoring is only necessary if a major incident occurs.
- D) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the "what" is all a future team needs.
- B) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- C) Documenting reasoning is unnecessary overhead across a multi-site rollout.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The plant-engineering team wants Claude Code to help with routine tasks (drafting maintenance documentation, exploring an unfamiliar control-system module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Mandate Claude Code usage for all tasks regardless of measured benefit.
- C) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- D) Ban Claude Code for all documentation tasks without evaluation.

**Question 60.** A recurring operational issue is that different engineers across plants debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across plants.
- C) Restrict debugging to a single designated engineer across all plants.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key

**Quick key:** 1-A, 2-C, 3-B, 4-A, 5-B, 6-D, 7-A, 8-A, 9-D, 10-A, 11-A, 12-B, 13-B, 14-D, 15-D, 16-C, 17-D, 18-A, 19-D, 20-A, 21-B, 22-B, 23-A, 24-D, 25-A, 26-A, 27-C, 28-B, 29-B, 30-C, 31-C, 32-D, 33-B, 34-B, 35-B, 36-D, 37-C, 38-D, 39-D, 40-C, 41-C, 42-C, 43-A, 44-C, 45-D, 46-B, 47-B, 48-A, 49-A, 50-D, 51-D, 52-C, 53-C, 54-C, 55-C, 56-A, 57-D, 58-B, 59-C, 60-B

---

**1. A** — The stated goal (dwell-time reduction with existing staff/equipment) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. B, C, and D either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. C** — Steps that are identical and predetermined regardless of case specifics are the defining case for a fixed workflow. A overstates the autonomy needed; B undersells the sequencing actually required; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. B** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. A** — Every subagent succeeding while whole shipment categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. B, C, and D all patch downstream instead of fixing the actual scope gap.

**5. B** — Business value pillars (efficiency, resilience, cost, service-level) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. D** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; B overreacts to sentiment alone without weighing it against the technical case.

**7. A** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. C and D withhold the reasoning stakeholders need; B removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures dispatcher overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and B over-engineer a simple augmentation need; C is factually wrong.

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. B and C ignore this real degradation; D doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (procurement) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. B** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, C, and D understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at undefined requirements; B ignores a known future need entirely; C blocks current delivery unnecessarily.

**15. D** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and C all leave the actual knowledge transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break the caching opportunity.

**18. A** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. B and D ignore this mismatch; C discards useful structured data.

**19. D** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; B denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. B** — Presenting both positions with attribution and likely explanation preserves the actual information for the attorney rather than resolving a real discrepancy arbitrarily. A, C, and D all discard or obscure a genuine legal conflict.

**22. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. C** — Verifying the stated holding against the source excerpt catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; D doesn't address correctness; B incorrectly claims no architectural mitigation exists.

**28. B** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, C, and D each drop a relevant factor from the decision.

**29. B** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; C over-corrects into permanent stagnation.

**30. C** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and D all misstate this real, architecture-relevant constraint.

**31. C** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it gets adopted. A, B, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. B** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; C confounds two variables; D dismisses a real risk without evidence.

**34. B** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and D misdiagnose the layer at fault; C avoids diagnosis entirely.

**35. B** — A regression tied specifically to a data-sync event, with model and latency unchanged, points first at retrieval/indexing. A, C, and D would not specifically correlate with a CRM data sync.

**36. D** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; C claims the tradeoff is unmeasurable when it is not.

**37. C** — Segment/outlier-aware monitoring surfaces problems an aggregate monthly average can hide. A and D accept a monitoring blind spot; B drops accuracy monitoring from observability entirely.

**38. D** — Segmenting accuracy by region and deal type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; C over-corrects by refusing any reduction regardless of evidence.

**39. D** — An isolated adoption-rate improvement could mask a worsened overconfidence failure mode; checking specifically for that before shipping is the correct diagnostic step. A and C ship without adequate testing; B incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (clarity, actionability, explanation quality) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. C** — Caching the static methodology document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; B removes needed content; D is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. A** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. B and D guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. B** — Cross-border data-residency, retention, and access-control requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D wrongly assumes a single policy suffices across jurisdictions.

**47. B** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and C overstate the universal safety case for maximal review; D misattributes this to a certification regime not established by the scenario.

**48. A** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. B defers to a reactive posture; C assumes one guardrail covers distinct risk types; D is factually wrong.

**49. A** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. B defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. D** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and C leave the systemic cause unaddressed; A sacrifices the tool's benefit for the rest of the team.

**51. D** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a safety-relevant system. A, B, and C all propose reducing rigor specifically because AI was involved, which is the wrong direction for this context.

**52. C** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. C** — Packaging the recurring, well-defined rollup as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. C** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by operations, legal, and engineering audiences alike. A, B, and D each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. D** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, B, and C all end architectural responsibility earlier than the lifecycle model calls for.

**58. B** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially across a multi-site rollout. A, C, and D all leave that reasoning undocumented and effectively lost.

**59. C** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and B over-assume benefit; D forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 6.*
