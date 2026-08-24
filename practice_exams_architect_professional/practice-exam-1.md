# CCARP Practice Exam 1

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer and multiple-response practice set — most items have one correct answer and three distractors; a few state how many responses to select. |
| Scenarios | 4 (Multi-Agent Claims Architecture, Financial Research Model/RAG Integration, Support-Deflection Evaluation & Optimization, Healthcare Governance & Team Enablement) |
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

## Scenario A: Multi-Agent Claims-Processing Architecture (Questions 1–15)

An insurance client wants to modernize claims intake, triage, and initial adjudication. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with the client's stakeholders.

---

**Question 1.** Discovery reveals the client's actual goal is processing 3x current claim volume with the same staffing, at the same average cycle time — not new capabilities the current process lacks.

- A) Frame the architecture around transformation, since AI projects should aim to create new capability.
- B) Frame the architecture around efficiency, and build success metrics around throughput per headcount rather than novel capability.
- C) Frame the architecture around cost reduction exclusively, regardless of what discovery surfaced.
- D) Skip framing around a specific value pillar, since the system either works or it doesn't.

**Question 2.** Claims intake, triage, and adjudication each require different steps depending on the claim type, prior findings, and missing information discovered along the way.

- A) An agentic pattern, since the right steps vary by case and depend on intermediate findings.
- B) A fixed workflow, since claims processing is a well-established business process.
- C) An augmented LLM pattern, since a single enhanced call is sufficient for any insurance workflow.
- D) Whichever pattern is fastest to implement, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (document intake, fraud-signal analysis, coverage lookup, adjudication recommendation).

- A) Let each subagent communicate results directly to whichever subagent needs them next, to minimize hops.
- B) Merge all four responsibilities into one subagent to avoid coordination overhead.
- C) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- D) Let subagents communicate directly, but log the traffic for later review.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition assigned only auto-claims to the pipeline — claims involving injury or third-party liability are never routed to any subagent and silently fall through.

- A) Add a fifth subagent specifically for edge cases.
- B) Add a prompt instruction telling subagents to flag claims they don't recognize.
- C) Give the existing subagents broader tool access so they can handle any claim type.
- D) Fix the coordinator's decomposition so it explicitly covers all claim categories, including injury and liability claims, rather than tuning the existing subagents.

**Question 5.** The design must align technical architecture to a specific business value pillar the client actually cares about, distinct from a generic "we added AI" narrative.

- A) Efficiency, transformation, productivity, cost, and performance SLAs are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- B) Any AI system inherently demonstrates transformation, so no further framing is needed.
- C) Business value pillars are a sales concern, not an architectural one.
- D) The pillar should be chosen after the system ships, based on whatever benefit is easiest to measure.

**Question 6.** The client's claims adjuster team is skeptical of automation and worried about job security; discovery interviews surface this repeatedly.

- A) Ignore the sentiment since it's not a technical requirement.
- B) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- C) Proceed with the technical design and let change management handle it separately with no architectural input.
- D) Recommend against the project entirely based on the sentiment.

**Question 7.** A stakeholder asks why the fraud-signal subagent uses a higher-capability, higher-cost model tier than the document-intake subagent.

- A) "Higher tier because it's more important" is a sufficient answer.
- B) Avoid explaining tier differences, since stakeholders don't need technical detail.
- C) Explain the tradeoff explicitly: fraud-signal analysis needs deeper reasoning that justifies the added cost/latency, while document intake is simpler and better served by a faster, cheaper tier.
- D) Use the same tier everywhere for simplicity, regardless of task difficulty.

**Question 8.** The architecture's current design produces a final adjudication recommendation with no mechanism to learn from adjuster overrides or outcomes over time.

- A) Add a feedback loop capturing adjuster overrides and outcomes as a first-class architectural component, so the system can improve post-deployment.
- B) This is acceptable since the initial design already reflects best practice.
- C) Feedback loops are a data science concern unrelated to the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** The client wants a single enhanced LLM call — with retrieval of policy documents — to answer straightforward coverage questions, without any multi-step autonomous orchestration.

- A) This calls for a full multi-agent architecture regardless of the simplicity of the task.
- B) This cannot be built with Claude at all, since it doesn't involve an agent.
- C) This requires a fixed workflow with at least five sequential steps.
- D) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.

**Question 10.** The document-intake subagent's toolset has grown to include tools for tasks like customer notification and billing lookup that are unrelated to document intake.

- A) This has no architectural downside as long as the subagent's prompt is well-written.
- B) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.
- C) More tools always improve a subagent's flexibility and should be encouraged.
- D) The fix is to increase the subagent's context window.

**Question 11.** The coordinator currently processes each claim sequentially through document intake, fraud analysis, coverage lookup, and adjudication, even though fraud analysis and coverage lookup have no dependency on each other's output.

- A) Run fraud analysis and coverage lookup as independent, parallel subagent calls once document intake completes, rather than sequentially.
- B) Sequential processing is required for auditability.
- C) Parallelization is not possible with a coordinator/subagent architecture.
- D) Combine fraud analysis and coverage lookup into a single subagent to avoid the sequencing question.

**Question 12.** The client asks how end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and token costs involved.
- B) Present the full technical architecture diagram with no simplification.
- C) Describe input → processing → output → feedback loop at a level the committee can evaluate against business outcomes, without requiring them to understand implementation internals.
- D) Skip a high-level description and go directly into an implementation demo.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, fraud detection, coverage lookup, adjudication) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- C) There's no meaningful architectural difference between the two approaches.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The claims architecture must eventually support a new claim type (parametric weather claims) the client is planning to launch next year, but detailed requirements aren't available yet.

- A) Ignore future claim types until requirements exist.
- B) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- C) Build full support for parametric weather claims now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document only the final configuration values, since implementation is self-explanatory.
- B) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: Model, Prompting, and RAG Integration for a Financial Research Platform (Questions 16–30)

A financial research platform wants Claude to answer analyst questions using both general reasoning and retrieval over a large, constantly-updated corpus of filings, earnings transcripts, and internal research notes. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most analyst questions are moderately complex; a small fraction require deep multi-step reasoning across many documents, and a small fraction are simple lookups.

- A) Use one fixed model tier for all questions, regardless of complexity.
- B) Always use the highest-capability tier to guarantee quality on every question.
- C) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-step cases.
- D) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.

**Question 17.** Every request sends the same long system prompt (analyst persona, citation requirements, formatting rules) followed by retrieved document excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Alternate system instructions and retrieved content throughout the prompt.
- C) Put retrieved content first since it's most relevant to the specific query.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.

**Question 18.** The corpus mixes long-form filings (10-Ks, earnings call transcripts) with short structured data (a table of quarterly metrics).

- A) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- B) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.
- C) Structured data should be excluded from retrieval entirely.
- D) Use the largest possible chunk size for everything to avoid needing multiple strategies.

**Question 19.** Analyst queries range from exact lookups ("Q3 2026 revenue for Company X") to conceptual questions ("how has Company X's margin narrative evolved over the last four quarters").

- A) Use only embedding similarity search for every query type.
- B) Use only structured/metadata filtering for every query type.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Analysts need citations that reliably map each claim to a specific source document and page/section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- C) Add citations after the fact by searching for a plausible source for each claim.
- D) Append a general bibliography of consulted documents at the end of each response.

**Question 21.** Two retrieved sources disagree on a company's reported Q3 revenue by a small margin — likely different reporting bases (GAAP vs. non-GAAP).

- A) Average the two figures and present the average.
- B) Omit the revenue figure entirely since sources disagree.
- C) Always prefer whichever source was retrieved first.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation (e.g., GAAP vs. non-GAAP), rather than silently picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- C) Post-process every response to strip leading text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary internal research-notes system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this research platform.

- A) Hard-code the research-notes integration into this platform's application code only.
- B) Paste the entire research-notes corpus into every prompt.
- C) Build an MCP server exposing the research-notes operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full research-notes catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the corpus grows.
- B) Loading the full catalog up front is always preferable for completeness.
- C) There's no meaningful difference in context cost between the two approaches.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** An analyst asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved documents before concluding.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different analyst-facing features so changes propagate consistently.

- A) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- B) Duplicate the fragments into each feature's prompt independently.
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- C) Increase output length so there's more room to be correct.
- D) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.

**Question 28.** The team debates whether analyst-facing latency SLAs should factor into model tier selection for the research platform.

- A) Latency should never factor into model or architecture decisions.
- B) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- C) Only cost should factor into tier selection, never latency.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Never upgrade models once the initial version is chosen.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output token budgets are entirely independent of each other.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Output length has no practical limit regardless of input size.
- D) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
---

## Scenario C: Evaluation and Optimization of a Production Support-Deflection System (Questions 31–45)

A Claude-powered system answers customer questions directly to deflect support tickets. It's been in production for six months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only ticket-deflection rate and hasn't defined targets for latency, cost, or safety.

- A) Deflection rate alone is sufficient since it's the system's primary purpose.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/security as first-class metrics — a system that deflects tickets but is too slow, too expensive, or unsafe still fails overall.
- C) Latency and cost are operations concerns unrelated to evaluation design.
- D) Safety metrics are only relevant for regulated industries.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past questions.

- A) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for safety-relevant paths — since no single method covers every failure mode.
- B) A single automated method is sufficient for any production system.
- C) Replace the automated checks entirely with only human review.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new prompt version improves deflection quality before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- D) Skip testing since prompt changes are low-risk by nature.

**Question 34.** A support answer is factually wrong. Investigation shows the underlying knowledge-base article was correct and retrieved properly, and the model's response paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.

**Question 35.** Immediately after a scheduled knowledge-base refresh, the system starts returning confident but incorrect answers, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.
- C) Suspect a temperature setting change, since confidence changed.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Accuracy should always be maximized regardless of cost or latency implications.
- C) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average accuracy score.

- A) A single aggregate average is sufficient for production monitoring.
- B) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- C) Weekly granularity is always sufficient regardless of system behavior.
- D) Monitoring should surface drift and outliers — a per-topic or per-query-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.

**Question 38.** The team proposes cutting human review of flagged low-confidence answers by 80%, citing a 97% aggregate accuracy score.

- A) Proceed with the cut based on the 97% aggregate figure alone.
- B) Segment accuracy by topic and query type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- C) Aggregate accuracy is definitionally representative of every segment.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new prompt version improves deflection rate but the team has not checked whether it also changed the false-positive rate on genuinely complex questions that should escalate to a human.

- A) Deflection rate alone is a sufficient signal to ship the change.
- B) Check the escalation-related failure mode specifically before shipping — an isolated deflection-rate improvement could be masking an increase in inappropriate deflections of complex cases.
- C) False-positive escalation behavior is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** The team wants to diagnose why a subset of answers are technically accurate but rated poorly by customers in satisfaction surveys.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves satisfaction.
- C) Investigate a dimension beyond factual accuracy — e.g., tone, completeness, or actionability — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- D) Ignore customer satisfaction scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full conversation history plus a large static policy document on every turn of multi-turn conversations.

- A) This has no optimization opportunity since full history is always required.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Remove the policy document entirely to save tokens.
- D) Apply prompt caching to the static policy document and consider trimming or summarizing older turns of conversation history to reduce redundant token cost across a multi-turn conversation.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- C) Reduce logging to save storage cost, with no other change.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a specific quality regression was caused by a recent prompt change, a recent model version change, or a knowledge-base content change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.
- D) Revert all three changes without investigation, regardless of which (if any) caused the regression.

**Question 44.** An automated eval asserts that a summarization output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- C) The reference string needs to be longer.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the support-deflection system is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use deflection rate alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, safety) so a healthy top-line number doesn't mask a specific failing area.
---

## Scenario D: Governance, Compliance, and Team Enablement for a Healthcare Deployment (Questions 46–60)

A healthcare client is deploying a Claude-powered system that processes patient intake information and assists a 30-person clinical operations team using Claude Code internally. You are responsible for governance, regulatory compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) HIPAA-driven data residency, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.
- C) Compliance only affects legal documentation, not system architecture.
- D) FedRAMP, not HIPAA, is the relevant regime for a healthcare client.

**Question 47.** A team proposes requiring human approval on every single output the patient-intake system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for healthcare AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- D) This approach is required by GDPR regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from patient-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) These risks are exclusive to non-healthcare use cases.
- C) A single generic guardrail addresses all three risk types equally well.
- D) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.

**Question 49.** The clinical operations team asks whether the system's decisions could produce disparate outcomes across different patient demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final clinical decisions, not any assistive system.

**Question 50.** The 30-person clinical operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- B) Have each staff member individually troubleshoot their own local configuration.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this healthcare context to go through the same review rigor as any other change to a regulated system.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Only a spot-check of AI-generated code is necessary.
- C) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a regulated system.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Disable Claude Code for the team entirely following any incident.
- C) Roll back all recent Claude Code-assisted changes regardless of relevance.
- D) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.

**Question 53.** The clinical operations team wants a documented, repeatable workflow for a recurring task (generating a weekly compliance summary report) versus a one-off exploratory coding task.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what patient-related data through the system and when.

- A) Access logging is optional if the system has role-based permissions.
- B) Audit logging can be added later without architectural impact.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this deployment includes clinical, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Skip stakeholder communication until the system is fully built.
- C) Use identical technical documentation for all three audiences to save effort.
- D) Tailor architectural communication to each audience — tradeoffs framed in terms clinical and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- 
**Question 56.** Midway through the project, the clinical team's requirements shift meaningfully based on a new regulatory guidance document.

- A) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- B) Refuse to incorporate the change since requirements were already agreed upon.
- C) Incorporate the change silently without informing stakeholders of the impact.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- C) Lifecycle responsibility ends once the contract is signed.
- D) Monitoring is only necessary if a major incident occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The clinical operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

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
# Answer Key — Practice Exam 1

**Quick key:** 1-B, 2-A, 3-C, 4-D, 5-A, 6-B, 7-C, 8-A, 9-D, 10-B, 11-A, 12-C, 13-D, 14-A, 15-B, 16-C, 17-D, 18-B, 19-C, 20-A, 21-D, 22-B, 23-C, 24-A, 25-A, 26-A, 27-D, 28-B, 29-C, 30-D, 31-B, 32-A, 33-C, 34-D, 35-B, 36-C, 37-D, 38-A, 39-B, 40-C, 41-D, 42-B, 43-C, 44-A, 45-D, 46-B, 47-C, 48-D, 49-B, 50-A, 51-C, 52-D, 53-B, 54-C, 55-D, 56-A, 57-B, 58-C, 59-D, 60-B

---

**1. B** — The stated goal (more volume, same headcount, same cycle time) is a throughput/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, C, and D either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. A** — Steps that vary by case and depend on intermediate findings are the defining case for an agentic pattern. B assumes a predictability the scenario explicitly lacks; C undersells the orchestration actually needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. C** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and D sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents in the first place.

**4. D** — Every subagent succeeding while whole claim categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, C, and B all patch downstream instead of fixing the actual scope gap.

**5. A** — Business value pillars (efficiency, transformation, productivity, cost, performance SLAs) give both the architecture and its metrics a clear anchor. B, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. C** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and B withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures adjuster overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and C ignore this real degradation; D doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (document intake) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, C, and B understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and B ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, C, and B all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the analyst rather than resolving a real discrepancy arbitrarily. A, C, and B all discard or obscure a genuine data conflict.

**22. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. C** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. A, B, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. D** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; B incorrectly claims no architectural mitigation exists.

**28. B** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, C, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. D** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, C, and B all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/security should all be defined as first-class metrics, since a system failing on any of them fails overall even if it deflects tickets. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. A** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially safety-relevant edge cases. B, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. C** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; D dismisses a real risk without evidence.

**34. D** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. B** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, C, and D would not specifically correlate with a knowledge-base refresh.

**36. C** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and B optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. D** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. A and C accept a monitoring blind spot; B drops accuracy monitoring from observability entirely.

**38. A** — Segmenting accuracy by topic/query type before cutting review protects against a failing segment hiding behind a healthy aggregate. B and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated deflection-rate improvement could mask a worsened escalation failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. C** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. D** — Caching the static policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. B** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; C addresses cost, not the actual observability gap.

**43. C** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and D guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. A** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and D misdiagnose model behavior as broken; C doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. B** — HIPAA-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and C understate real architectural impact; D misidentifies the applicable regulatory regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; D misattributes this to GDPR, which isn't the relevant regime described.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. C** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a regulated system. A, B, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. D** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. B** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. D** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by clinical, legal, and engineering audiences alike. A, C, and B each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. D** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 1.*
