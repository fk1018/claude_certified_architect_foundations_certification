# CCARP Practice Exam 12

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
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

Meridian Mobile, a regional telecom retailer, wants to modernize how it handles customer escalations that arrive through three previously disconnected queues — billing disputes, device warranty claims, and network outage complaints — plus a fourth workflow for retention offers to at-risk subscribers. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with Meridian's stakeholders.

---

**Question 1.** Discovery reveals the client's actual goal is reducing average escalation resolution time by unifying the three disconnected queues, at the same staffing level — not adding new self-service capabilities customers currently lack.

- A) Frame the architecture around efficiency, building metrics around resolution time and handle volume rather than novel capability.
- B) Frame the architecture around transformation, since consolidating three queues is inherently transformative.
- C) Frame the architecture around cost reduction exclusively, regardless of what discovery revealed.
- D) Skip framing around a specific value pillar, since the system either works or it doesn't.

**Question 2.** Escalation handling requires different steps depending on the issue category, customer tier, and information uncovered mid-conversation (for example, discovering a device is under an active recall).

- A) A fixed workflow, since escalations follow a standard script regardless of variation.
- B) An agentic pattern, since the right steps vary by case and depend on intermediate findings uncovered during handling.
- C) An augmented LLM pattern, since one enhanced call is sufficient for any escalation.
- D) Whichever pattern is fastest to prototype, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (billing-dispute, device-warranty, network-outage-diagnostics, retention-offer).

- A) Let each subagent communicate directly to whichever subagent needs its output next, to minimize hops.
- B) Merge all four responsibilities into one subagent to avoid coordination overhead.
- C) Let subagents communicate directly, but log the traffic for later review.
- D) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition routes billing, device, and network escalations correctly while retention-eligible cases (customers actively threatening to cancel) are never routed to any subagent and silently fall through.

- A) Add a fifth generic subagent for edge cases.
- B) Give the existing subagents broader tool access so they can handle any escalation type.
- C) Fix the coordinator's decomposition so it explicitly covers retention-eligible cases, rather than tuning the existing subagents.
- D) Add a prompt instruction telling subagents to flag escalations they don't recognize.

**Question 5.** The design must align technical architecture to a specific business value pillar Meridian actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation, so no further framing is needed.
- B) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- C) Business value pillars are a sales concern, not an architectural one.
- D) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.

**Question 6.** Frontline escalation agents are skeptical of the new system and worried it will be used to justify headcount reductions; discovery interviews surface this repeatedly.

- A) Ignore the sentiment since it's not a technical requirement.
- B) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- C) Proceed with the technical design and let change management handle it separately with no architectural input.
- D) Recommend against the project entirely based on the sentiment.

**Question 7.** A stakeholder asks why the network-outage-diagnostics subagent uses a higher-capability, higher-cost model tier than the billing-dispute subagent.

- A) Use the same tier everywhere for simplicity, regardless of task difficulty.
- B) "Higher tier because it's more important" is a sufficient answer.
- C) Avoid explaining tier differences, since stakeholders don't need technical detail.
- D) Explain the tradeoff explicitly: outage diagnostics needs deeper reasoning over network telemetry that justifies the added cost/latency, while billing disputes are simpler and better served by a faster, cheaper tier.

**Question 8.** The architecture's current design produces a final retention-offer recommendation with no mechanism to learn from which offers customers actually accepted or rejected over time.

- A) This is acceptable since the initial design already reflects best practice.
- B) Feedback loops are a data science concern unrelated to the architecture.
- C) Add a feedback loop capturing offer acceptance/rejection outcomes as a first-class architectural component, so the system can improve post-deployment.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** The client wants a single enhanced LLM call — with retrieval of the customer's plan and billing history — to answer straightforward "why is my bill higher this month" questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) This cannot be built with Claude at all, since it doesn't involve an agent.
- C) This requires a fixed workflow with at least five sequential steps.
- D) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.

**Question 10.** The billing-dispute subagent's toolset has grown to include tools for tasks like device-shipping tracking and network-status lookups that are unrelated to billing disputes.

- A) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- B) This has no architectural downside as long as the subagent's prompt is well-written.
- C) More tools always improve a subagent's flexibility and should be encouraged.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each escalation sequentially through billing-dispute lookup, device-warranty lookup, and retention-offer scoring, even though device-warranty lookup and retention-offer scoring have no dependency on each other's output.

- A) Combine device-warranty lookup and retention-offer scoring into a single subagent to avoid the sequencing question.
- B) Run device-warranty lookup and retention-offer scoring as independent, parallel subagent calls once billing-dispute lookup completes, rather than sequentially.
- C) Sequential processing is required for auditability.
- D) Parallelization is not possible with a coordinator/subagent architecture.

**Question 12.** A regional VP unfamiliar with the technical details asks how the end-to-end escalation architecture should be described for a steering review.

- A) Present only the model names and token costs involved.
- B) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- C) Present the full technical architecture diagram with no simplification.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent holding every tool (billing, device, network, retention) rather than a coordinator with specialized subagents.

- A) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.
- B) A single generalist agent scales better as tool count grows.
- C) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- D) There's no meaningful architectural difference between the two approaches.

**Question 14.** The escalation architecture must eventually support a new escalation category (streaming-bundle disputes) planned for next year, but detailed requirements aren't available yet.

- A) Build full support for streaming-bundle disputes now, guessing at requirements.
- B) Ignore future escalation categories until requirements exist.
- C) Refuse to proceed with the current phase until the future requirements are finalized.
- D) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Rely on the original architect remaining available indefinitely instead of documenting.
- C) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: Model Selection and Context Engineering for a Retail Merchandising Copilot (Questions 16–30)

Harborview Retail Group, a multi-category apparel retailer, wants Claude to help category buyers answer questions using both general reasoning and retrieval over a large, constantly-updated corpus of vendor contracts, sell-through reports, and category strategy memos. You're architecting the model selection, prompting approach, and integration layer for the merchandising copilot.

---

**Question 16.** Most buyer questions to the copilot are moderately complex; a small fraction require deep multi-step reasoning across many SKUs and vendors, and a small fraction are simple lookups (for example, "current on-hand units for SKU 4471").

- A) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-step cases.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Use one fixed model tier for all questions, regardless of complexity.
- D) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.

**Question 17.** Every request to the copilot sends the same long system prompt (merchandiser persona, formatting rules, category taxonomy) followed by retrieved SKU and vendor data that varies per query.

- A) Put retrieved content first since it's most relevant to the specific query.
- B) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- C) Alternate system instructions and retrieved content throughout the prompt.
- D) Order doesn't affect cost or latency for this use case.

**Question 18.** The merchandising corpus mixes long-form vendor contracts and category strategy memos with short structured data (a table of weekly sell-through by SKU).

- A) Use the largest possible chunk size for everything to avoid needing multiple strategies.
- B) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- C) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.
- D) Structured sell-through data should be excluded from retrieval entirely.

**Question 19.** Buyer queries range from exact lookups ("current inventory for SKU 4471") to conceptual questions ("how has the athleisure category's margin story evolved this year").

- A) Use only embedding similarity search for every query type.
- B) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- C) Use only structured/metadata filtering for every query type.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Buyers need each margin or forecast claim reliably mapped to a specific source document and section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Add citations after the fact by searching for a plausible source for each claim.
- C) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- D) Append a general bibliography of consulted documents at the end of each response.

**Question 21.** Two retrieved sources disagree on a vendor's quoted unit cost by a small margin — likely because one reflects a pre-rebate price and the other a post-rebate net price.

- A) Average the two figures and present the average.
- B) Always prefer whichever source was retrieved first.
- C) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation (e.g., pre-rebate vs. post-rebate), rather than silently picking one.
- D) Omit the unit cost figure entirely since sources disagree.

**Question 22.** A prompt asking the model to "always output valid structured JSON with source fields" still occasionally produces a conversational preamble before the JSON.

- A) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- B) Repeat the instruction more emphatically in the prompt.
- C) Post-process every response to strip leading text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The copilot needs to connect to a proprietary internal vendor-catalog system, exposing search and lookup capabilities to multiple other internal Claude-powered tools beyond just the merchandising copilot.

- A) Hard-code the vendor-catalog integration into this copilot's application code only.
- B) Paste the entire vendor catalog into every prompt.
- C) Build an MCP server exposing the vendor-catalog operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full vendor catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) There's no meaningful difference in context cost between the two approaches.
- C) The catalog should never be exposed to the agent in any form.
- D) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the catalog grows.

**Question 25.** A buyer asks a chain-of-thought-friendly question requiring the model to reason step by step across several vendor contracts and sell-through reports before recommending a reorder quantity.

- A) Zero-shot prompting with no reasoning guidance is always equally effective.
- B) The model cannot reason across multiple documents regardless of prompting approach.
- C) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- D) Chain-of-thought prompting is only useful for coding tasks.

**Question 26.** The copilot wants to standardize prompt fragments (citation format, category taxonomy, formatting rules) across several different buyer-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Modular prompts are the same thing as prompt caching.
- C) Standardization across features isn't achievable with prompt design.
- D) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).

**Question 27.** The copilot occasionally returns confident, well-cited-looking margin figures that, on manual review, misstate a specific number from the correctly retrieved source report.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) Increase output length so there's more room to be correct.
- C) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- D) This is not something an architecture can address; it's purely a model limitation with no mitigation.

**Question 28.** The team debates whether buyer-facing latency SLAs should factor into model tier selection for the merchandising copilot.

- A) Only cost should factor into tier selection, never latency.
- B) SLAs are a stakeholder-communication concern with no bearing on technical architecture.
- C) Latency should never factor into model or architecture decisions.
- D) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.

**Question 29.** A new model version is released with improved benchmark scores. The merchandising copilot currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Never upgrade models once the initial version is chosen.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.

**Question 30.** The copilot's context budget is a concern because both the system prompt/citation rules and the retrieved vendor/SKU data must fit alongside room for a detailed recommendation.

- A) Input and output token budgets are entirely independent of each other.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Output length has no practical limit regardless of input size.
- D) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.

---

## Scenario C: Evaluation and Monitoring of a Field-Service Dispatch Assistant (Questions 31–45)

Atlas Utilities operates a fleet of field-service technicians who service gas and electric meters. A Claude-powered dispatch assistant recommends likely fault causes, required parts, and whether an issue can be resolved remotely versus requiring an on-site visit. It's been in production for several months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only technician first-time-fix rate and hasn't defined targets for latency, cost, or safety.

- A) Latency and cost are operations concerns unrelated to evaluation design.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that improves first-time-fix rate but is too slow, too expensive, or unsafe still fails overall.
- C) First-time-fix rate alone is sufficient since it's the system's primary purpose.
- D) Safety metrics are only relevant for regulated industries.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past dispatch tickets.

- A) A single automated method is sufficient for any production system.
- B) Replace the automated checks entirely with only human review.
- C) Expand the labeled set indefinitely as the sole improvement lever.
- D) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new prompt version improves technician-recommendation quality before rolling it out to all dispatch traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Skip testing since prompt changes are low-risk by nature.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.

**Question 34.** A dispatch recommendation cites the wrong required part number. Investigation shows the underlying parts-catalog lookup returned correct, current data, and the model's response paraphrased it inaccurately.

- A) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.
- B) This is a retrieval problem; fix the indexing pipeline.
- C) This cannot be diagnosed without retraining the model.
- D) This is a model mismatch requiring a different model tier regardless of the specific failure.

**Question 35.** Immediately after a scheduled parts-catalog refresh, the dispatch assistant starts recommending obsolete part numbers, while model version and average latency are unchanged.

- A) Suspect a temperature setting change, since confidence changed.
- B) Suspect the model was silently updated by the provider.
- C) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency for dispatch recommendations but is worried about hurting first-time-fix accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring for the dispatch assistant currently reports only an overall weekly average accuracy score.

- A) A single aggregate average is sufficient for production monitoring.
- B) Monitoring should surface drift and outliers — a per-technician-specialty or per-issue-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- C) Weekly granularity is always sufficient regardless of system behavior.
- D) Monitoring should track only cost, since accuracy is captured by the eval suite alone.

**Question 38.** The team proposes cutting human review of flagged low-confidence dispatch recommendations by 80%, citing a 96% aggregate accuracy score.

- A) Segment accuracy by issue type and technician specialty before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- B) Proceed with the cut based on the 96% aggregate figure alone.
- C) Aggregate accuracy is definitionally representative of every segment.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new prompt version improves first-time-fix rate, but the team has not checked whether it also changed the rate of recommending an on-site visit for issues that should have been resolved remotely.

- A) First-time-fix rate alone is a sufficient signal to ship the change.
- B) Check the remote-resolution-eligible failure mode specifically before shipping — an isolated first-time-fix improvement could be masking an increase in unnecessary on-site dispatches.
- C) This failure mode is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** The team wants to diagnose why a subset of technically accurate dispatch recommendations are rated poorly by technicians in post-job surveys.

- A) Investigate a dimension beyond factual accuracy — e.g., clarity, completeness of instructions, or practicality in the field — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- B) Assume the accuracy metric is broken and discard it.
- C) Increase the model's capability tier, assuming higher capability always improves ratings.
- D) Ignore technician satisfaction scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends the full ticket history plus a large static equipment-manual excerpt on every turn of multi-turn dispatch conversations.

- A) This has no optimization opportunity since full history is always required.
- B) Remove the equipment-manual excerpt entirely to save tokens.
- C) Switch to a smaller model as the only lever for reducing token cost.
- D) Apply prompt caching to the static equipment-manual excerpt and consider trimming or summarizing older turns of ticket history to reduce redundant token cost across a multi-turn conversation.

**Question 42.** Logging captures every raw prompt and response for the dispatch assistant, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Observability requires no structure as long as data is retained somewhere.
- D) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or an equipment-manual content update — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) Revert all three changes without investigation, regardless of which (if any) caused the regression.
- C) Attribution is impossible once multiple changes have shipped in the same week.
- D) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.

**Question 44.** An automated eval asserts that a dispatch-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The reference string needs to be longer.
- B) The model is malfunctioning and needs retraining.
- C) Temperature should be increased to fix the intermittent failures.
- D) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.

**Question 45.** Leadership wants a single number to represent "how good" the dispatch assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use first-time-fix rate alone as the single number, since it's the system's stated purpose.
- C) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.
- D) Refuse to provide any single summary metric under any circumstances.

---

## Scenario D: Governance and Team Enablement for an Insurance Claims Modernization (Questions 46–60)

Cascade Mutual Insurance is modernizing its claims-intake and reserve-estimation systems with a Claude-powered assistant, and its 25-person claims engineering team uses Claude Code internally for day-to-day development. You are responsible for governance, regulatory alignment, and developer enablement for the program.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic for the claims system is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) Compliance only affects legal documentation, not system architecture.
- C) State insurance data-privacy and retention requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- D) FedRAMP, not state insurance regulation, is the relevant regime for this client.

**Question 47.** A team proposes requiring human approval on every single output the claims-intake system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for insurance AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- D) This approach is required by GDPR regardless of other considerations.

**Question 48.** The claims system must identify and mitigate standard LLM risks — hallucination, prompt injection from claimant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- C) These risks are exclusive to non-insurance use cases.
- D) A single generic guardrail addresses all three risk types equally well.

**Question 49.** The claims operations team asks whether the system's payout recommendations could produce disparate outcomes across different policyholder demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final payout decisions, not any assistive system.

**Question 50.** The claims engineering team's Claude Code usage is inconsistent — some engineers have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- B) Have each engineer individually troubleshoot their own local configuration.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this regulated claims context to go through the same review rigor as any other change.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- C) Only a spot-check of AI-generated code is necessary.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated claims-calculation change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- C) Disable Claude Code for the team entirely following any incident.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The claims operations team wants a documented, repeatable workflow for a recurring task (generating a weekly reserve-adequacy summary) versus a one-off exploratory coding task.

- A) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- B) Build both as ad hoc, undocumented prompts each time they're needed.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what claimant-related data through the system and when.

- A) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- B) Access logging is optional if the system has role-based permissions.
- C) Audit logging can be added later without architectural impact.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this claims modernization includes claims-operations, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Skip stakeholder communication until the system is fully built.
- C) Tailor architectural communication to each audience — tradeoffs framed in terms claims-operations and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- D) Use identical technical documentation for all three audiences to save effort.

**Question 56.** Midway through the project, the claims team's requirements shift meaningfully based on a new state regulatory bulletin.

- A) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- B) Refuse to incorporate the change since requirements were already agreed upon.
- C) Incorporate the change silently without informing stakeholders of the impact.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the claims operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle responsibility ends once the contract is signed.
- C) Monitoring is only necessary if a major incident occurs.
- D) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.

**Question 58.** Documentation for this claims system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- C) Documenting reasoning is unnecessary overhead in a regulated environment.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The claims operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- B) Assume AI-assisted tooling always saves time on every task category by default.
- C) Ban Claude Code for all documentation tasks without evaluation.
- D) Mandate Claude Code usage for all tasks regardless of measured benefit.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging to a single designated engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key — Practice Exam 12

**Quick key:** 1-A, 2-B, 3-D, 4-C, 5-B, 6-B, 7-D, 8-C, 9-D, 10-A, 11-B, 12-B, 13-A, 14-D, 15-C, 16-A, 17-B, 18-C, 19-B, 20-C, 21-C, 22-A, 23-C, 24-D, 25-C, 26-D, 27-C, 28-D, 29-C, 30-D, 31-B, 32-D, 33-D, 34-A, 35-C, 36-A, 37-B, 38-A, 39-B, 40-A, 41-D, 42-D, 43-D, 44-D, 45-C, 46-C, 47-C, 48-B, 49-B, 50-A, 51-B, 52-B, 53-A, 54-A, 55-C, 56-A, 57-D, 58-B, 59-A, 60-B

---

**1. A** — A goal of more volume/consistency within the same staffing and cycle time is a throughput/efficiency problem; naming that pillar correctly shapes both architecture and success metrics. B, C, and D either misname the pillar or skip the framing discovery actually surfaced.

**2. B** — Steps that vary by case and depend on intermediate findings are the defining case for an agentic pattern. A assumes a predictability the scenario lacks; C undersells the orchestration needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. D** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and C sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents.

**4. C** — Every subagent succeeding while an entire escalation category is never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap.

**5. B** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. A, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. D** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; C removes a deliberate, justified difference for false simplicity.

**8. C** — Adding a feedback loop that captures offer outcomes as a first-class architectural component is what lets the system improve after deployment. A, B, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. A** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not writing around it. B and C ignore this real degradation; D doesn't address selection reliability at all.

**11. B** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite completes, reducing latency without sacrificing correctness. A and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. B** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; C is too much of the wrong kind of detail; D skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D all understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at undefined requirements; B ignores a known future need entirely; C blocks current delivery unnecessarily.

**15. C** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and D all leave the actual knowledge transfer gap unaddressed.

**16. A** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. B and D sacrifice fit-to-task or quality; C ignores complexity variation entirely.

**17. B** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and D all misstate or break the caching opportunity.

**18. C** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and B ignore this mismatch; D discards useful structured data.

**19. B** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. C** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and D all reintroduce the failure mode the fix is meant to prevent.

**21. C** — Presenting both figures with attribution and a likely methodological explanation preserves the actual information for the buyer rather than resolving a real discrepancy arbitrarily. A, B, and D all discard or obscure a genuine data conflict.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. D** — Progressive discovery via a queryable catalog resource scales with catalog growth better than loading the entire catalog into every prompt. A and B ignore the real context cost of the monolithic approach; C removes needed capability entirely.

**25. C** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. A, B, and D all misstate the fit or capability of prompting techniques for this task.

**26. D** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; C denies a real, common architecture pattern.

**27. C** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; B doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. D** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and C each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and C all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if first-time-fix rate improves. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. A** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. B and D misdiagnose the layer at fault; C avoids diagnosis entirely.

**35. C** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a parts-catalog refresh.

**36. A** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. B and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. B** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and C accept a monitoring blind spot; D drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by issue type and technician specialty before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated first-time-fix improvement could mask a worsened dispatch-necessity failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. A** — "Accurate but poorly rated" points at an unmeasured quality dimension (clarity, completeness, practicality) rather than a broken accuracy metric. B and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. D** — Caching the static equipment-manual excerpt and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; B removes needed content; C is a blunt, quality-risking lever when a more targeted fix is available.

**42. D** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and C accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and B guess without evidence; C gives up on a solvable (if effortful) diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and C misdiagnose model behavior as broken; A doesn't address the actual mismatch between eval design and output variability.

**45. C** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. C** — State insurance data-privacy and retention requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; D misattributes this to GDPR, which isn't the relevant regime described.

**48. B** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; C is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. B** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and D skip diagnosis; C is a disproportionate reaction that doesn't investigate the actual cause.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. A** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. B, C, and D each understate what compliance-grade audit evidence actually requires.

**55. C** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by claims-operations, legal, and engineering audiences alike. A, B, and D each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. D** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, B, and C all end architectural responsibility earlier than the lifecycle model calls for.

**58. B** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, C, and D all leave that reasoning undocumented and effectively lost.

**59. A** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. B and D over-assume benefit; C forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 12.*
