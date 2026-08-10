# CCARP Practice Exam 11

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform, RAG and Model Tiering for a Pharmaceutical Literature-Review Platform, Evaluation and Optimization of an HR Recruiting Assistant, Governance and Enablement for a Public-Sector FedRAMP Deployment) |
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

## Scenario A: Multi-Agent E-Discovery Platform for a Legal Services Firm (Questions 1–15)

Harrow & Vance LLP, a mid-size litigation firm, is building an internal e-discovery platform to handle document classification, privilege review, custodian communication analysis, and production packaging for large litigation matters. You are the architect responsible for the end-to-end design, including whether and how to use a multi-agent pattern, and for running discovery with the firm's stakeholders.

---

**Question 1.** Discovery reveals the firm's actual goal is processing 3x the current document volume per matter with the same review-team headcount, while preserving the same defensibility standard — not new capabilities the current process lacks.

- A) Frame the architecture around transformation, since AI projects should aim to create new capability.
- B) Frame the architecture around cost reduction exclusively, regardless of what discovery surfaced.
- C) Skip framing around a specific value pillar, since the system either works or it doesn't.
- D) Frame the architecture around efficiency, and build success metrics around review throughput per attorney-hour without sacrificing defensibility.

**Question 2.** Document classification, privilege review, and production each require different steps depending on document type, privilege signals surfaced along the way, and custodian context discovered mid-review.

- A) A fixed workflow, since e-discovery is a well-established legal process.
- B) An augmented LLM pattern, since a single enhanced call is sufficient for any e-discovery workflow.
- C) An agentic pattern, since the right steps vary by document and depend on intermediate findings.
- D) Whichever pattern is fastest to implement, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents (document classification, privilege detection, redaction, production formatting).

- A) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- B) Let subagents communicate directly, but log the traffic for later review.
- C) Merge all four responsibilities into one subagent to avoid coordination overhead.
- D) Let each subagent communicate directly with whichever subagent needs its results next, to minimize hops.

**Question 4.** Every subagent completes its assigned work correctly, but the coordinator's decomposition routes only email-format documents into the pipeline — scanned PDFs and chat-export logs are never routed to any subagent and silently fall through, missing production.

- A) Fix the coordinator's decomposition so it explicitly covers all document source types, including scanned PDFs and chat exports, rather than tuning the existing subagents.
- B) Add a prompt instruction telling subagents to flag document types they don't recognize.
- C) Give the existing subagents broader tool access so they can handle any document type.
- D) Add a fifth subagent specifically for edge-case document types.

**Question 5.** The design must align technical architecture to a specific business value pillar the firm actually cares about, distinct from a generic "we added AI" narrative.

- A) Any AI system inherently demonstrates transformation, so no further framing is needed.
- B) Business value pillars are a business-development concern, not an architectural one.
- C) Efficiency, risk-reduction/defensibility, cost-per-gigabyte-reviewed, and cycle-time-to-production are examples of such pillars; the chosen one should drive both the architecture and its success metrics.
- D) The pillar should be chosen after the matter closes, based on whatever benefit is easiest to measure.

**Question 6.** The firm's associates and paralegals are skeptical of automation and worried about reduced review hours; discovery interviews surface this repeatedly.

- A) Ignore the sentiment since it's not a technical requirement.
- B) Treat it as a real implicit constraint alongside the explicit technical requirements — it will shape adoption, rollout sequencing, and where human-in-the-loop checkpoints matter most.
- C) Proceed with the technical design and let change management handle it separately with no architectural input.
- D) Recommend against the project entirely based on the sentiment.

**Question 7.** A partner asks why the privilege-detection subagent uses a higher-capability, higher-cost model tier than the document-classification subagent.

- A) Use the same tier everywhere for simplicity, regardless of task difficulty.
- B) Explain the tradeoff explicitly: privilege determinations carry high legal risk and require deeper reasoning that justifies the added cost/latency, while classification is simpler and better served by a faster, cheaper tier.
- C) "Higher tier because it's more important" is a sufficient answer.
- D) Avoid explaining tier differences, since partners don't need technical detail.

**Question 8.** The architecture's current design produces a final production recommendation with no mechanism to learn from attorney overrides of privilege or relevance calls over time.

- A) Add a feedback loop capturing attorney overrides and outcomes as a first-class architectural component, so the system can improve post-deployment.
- B) This is acceptable since the initial design already reflects best practice.
- C) Feedback loops are a data science concern unrelated to the architecture.
- D) Defer any feedback mechanism to a hypothetical future phase with no current design hooks.

**Question 9.** A litigation support team wants a single enhanced LLM call — with retrieval of privilege-rule guidance — to answer straightforward attorney questions about privilege categories, without any multi-step autonomous orchestration.

- A) This requires a fixed workflow with at least five sequential steps.
- B) This cannot be built with Claude at all, since it doesn't involve an agent.
- C) An augmented LLM pattern (a single call enhanced with retrieval/tools) fits this simpler augmentation need without the overhead of agentic orchestration.
- D) This calls for a full multi-agent architecture regardless of the simplicity of the task.

**Question 10.** The document-classification subagent's toolset has grown to include tools for billing entry and calendar scheduling that are unrelated to document classification.

- A) This has no architectural downside as long as the subagent's prompt is well-written.
- B) More tools always improve a subagent's flexibility and should be encouraged.
- C) The fix is to increase the subagent's context window.
- D) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or moved to a more appropriate subagent.

**Question 11.** The coordinator currently processes each document sequentially through classification, privilege detection, relevance scoring, and redaction, even though privilege detection and relevance scoring have no dependency on each other's output.

- A) Run privilege detection and relevance scoring as independent, parallel subagent calls once classification completes, rather than sequentially.
- B) Sequential processing is required for chain-of-custody defensibility.
- C) Parallelization is not possible with a coordinator/subagent architecture.
- D) Combine privilege detection and relevance scoring into a single subagent to avoid the sequencing question.

**Question 12.** General counsel asks how the end-to-end architecture should be described at a high level for a steering committee unfamiliar with the technical details.

- A) Present only the model names and token costs involved.
- B) Present the full technical architecture diagram with no simplification.
- C) Skip a high-level description and go directly into an implementation demo.
- D) Describe input → processing → output → feedback loop at a level the committee can evaluate against case-outcome and cost goals, without requiring them to understand implementation internals.

**Question 13.** A competing vendor proposes a single, generalist agent with all tools (document processing, privilege detection, redaction, production formatting) rather than a coordinator with specialized subagents.

- A) A single generalist agent scales better as tool count grows.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- C) There's no meaningful architectural difference between the two approaches.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The e-discovery architecture must eventually support a new matter type (regulatory investigations) the firm is planning to take on next year, but detailed requirements aren't available yet.

- A) Design the current decomposition and tool/subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- B) Ignore future matter types until requirements exist.
- C) Build full support for regulatory investigations now, guessing at requirements.
- D) Refuse to proceed with the current phase until the future requirements are finalized.

**Question 15.** The steering committee wants documentation they can hand to a new engineering team in a year, who will extend the system without the original architect present.

- A) Document the architecture and the reasoning ("why") behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."
- B) Document only the final configuration values, since implementation is self-explanatory.
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code is well-organized.

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Veritas Biopharma's medical affairs team needs Claude to answer scientific-literature questions using both general reasoning and retrieval over a large, constantly-updated corpus of clinical trial publications, regulatory filings, and internal study reports. You're architecting the model selection, prompting approach, and integration layer.

---

**Question 16.** Most medical-affairs questions are moderately complex; a small fraction require deep multi-step reasoning across many trial publications, and a small fraction are simple lookups.

- A) Always use the highest-capability tier to guarantee quality on every question.
- B) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for the deep multi-step cases.
- C) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.
- D) Use one fixed model tier for all questions, regardless of complexity.

**Question 17.** Every request sends the same long system prompt (medical-affairs persona, citation requirements, regulatory disclaimer language) followed by retrieved document excerpts that vary per query.

- A) Alternate system instructions and retrieved content throughout the prompt.
- B) Put retrieved content first since it's most relevant to the specific query.
- C) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce both latency and cost across the high query volume.
- D) Order doesn't affect cost or latency for this use case.

**Question 18.** The corpus mixes long-form publications (full-text articles) with short structured data (dosing and adverse-event tables).

- A) One chunking and indexing strategy tuned for long-form documents can serve both content types equally well.
- B) Chunking and indexing strategy should match each data shape — long-form articles need different chunking than structured tables, or retrieval quality degrades for whichever type doesn't match.
- C) Structured data should be excluded from retrieval entirely.
- D) Use the largest possible chunk size for everything to avoid needing multiple strategies.

**Question 19.** Reviewer queries range from exact lookups ("what was the primary endpoint p-value in Trial 4471") to conceptual questions ("how has the safety narrative for Compound K evolved across recent publications").

- A) Use only embedding similarity search for every query type.
- B) Query pattern doesn't affect which retrieval approach is appropriate.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- D) Use only structured/metadata filtering for every query type.

**Question 20.** Reviewers need citations that reliably map each claim to a specific source publication and page/section, and generic prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite sources" without further structure.
- B) Add citations after the fact by searching for a plausible source for each claim.
- C) Append a general bibliography of consulted publications at the end of each response.
- D) Require structured output pairing each claim with its source (publication, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.

**Question 21.** Two retrieved trial reports disagree on a reported adverse-event rate by a small margin — likely different reporting populations (intent-to-treat vs. per-protocol).

- A) Average the two figures and present the average.
- B) Always prefer whichever source was retrieved first.
- C) Omit the adverse-event figure entirely since sources disagree.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation (e.g., ITT vs. per-protocol), rather than silently picking one.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Post-process every response to strip leading text before the first `{`.
- C) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary internal clinical-study-reports repository, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond just this literature-review platform.

- A) Build an MCP server exposing the study-reports repository operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the repository integration into this platform's application code only.
- C) Paste the entire study-reports corpus into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full study-report catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the corpus grows.
- B) Loading the full catalog up front is always preferable for completeness.
- C) There's no meaningful difference in context cost between the two approaches.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** A reviewer asks a chain-of-thought-friendly question requiring the model to reason step by step across several trial publications before concluding on a possible safety signal.

- A) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- B) Zero-shot prompting with no reasoning guidance is always equally effective.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, regulatory disclaimer language, formatting rules) across several different literature-review features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Modular prompts are the same thing as prompt caching.
- C) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific statistic from the correctly retrieved source publication.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- C) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether reviewer-facing latency SLAs should factor into model tier selection for the literature-review platform.

- A) Latency should never factor into model or architecture decisions.
- B) Only cost should factor into tier selection, never latency.
- C) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.
- C) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- D) Never upgrade models once the initial version is chosen.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved document excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- B) Input and output token budgets are entirely independent of each other.
- C) This tradeoff only matters for very long documents, never for typical queries.
- D) Output length has no practical limit regardless of input size.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

TalentBridge Staffing built a Claude-powered assistant that screens resumes, drafts candidate outreach, and answers recruiter questions about pipeline status. It's been in production for four months, and you're responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only resume-screening throughput and hasn't defined targets for latency, cost, or safety/fairness.

- A) Throughput alone is sufficient since it's the system's primary purpose.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/fairness as first-class metrics — a system that screens quickly but is biased, too expensive, or unsafe still fails overall.
- C) Latency and cost are operations concerns unrelated to evaluation design.
- D) Fairness metrics are only relevant if a complaint is filed.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past resumes.

- A) A single automated method is sufficient for any production system.
- B) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for fairness-relevant paths — since no single method covers every failure mode.
- C) Replace the automated checks entirely with only human review.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new candidate-outreach prompt improves response rates before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Skip testing since prompt changes are low-risk by nature.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.

**Question 34.** A candidate outreach message states the wrong compensation band for a role. Investigation shows the underlying job-requisition data was correct and retrieved properly, and the model's message paraphrased it inaccurately.

- A) This is a retrieval problem; fix the indexing pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is best characterized as a prompt/generation issue (inaccurate paraphrasing of correctly retrieved content), which calls for prompt or output-validation fixes rather than retrieval changes.
- D) This is a model mismatch requiring a different model tier regardless of the specific failure.

**Question 35.** Immediately after a scheduled job-requisition data refresh, the system starts returning confident but incorrect compensation figures, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Suspect a temperature setting change, since confidence changed.
- C) Suspect the context window shrank.
- D) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.

**Question 36.** The team wants to reduce cost and latency of resume screening but is worried about hurting accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- C) Accuracy should always be maximized regardless of cost or latency implications.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average screening-accuracy score.

- A) Monitoring should surface drift and outliers — a per-role or per-candidate-segment breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence screening decisions by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone.
- B) Aggregate accuracy is definitionally representative of every segment.
- C) Segment accuracy by role and candidate type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new screening prompt improves throughput, but the team hasn't checked whether it also changed the false-negative rate on qualified candidates from underrepresented backgrounds.

- A) Throughput alone is a sufficient signal to ship the change.
- B) False-negative behavior on this dimension is not something evaluation can measure.
- C) Ship the change and monitor informally after the fact instead of testing beforehand.
- D) Check the fairness-related failure mode specifically before shipping — an isolated throughput improvement could be masking a disparate increase in false negatives for a specific group.

**Question 40.** The team wants to diagnose why a subset of screening summaries are technically accurate but rated poorly by recruiters in usability feedback.

- A) Assume the accuracy metric is broken and discard it.
- B) Investigate a dimension beyond factual accuracy — e.g., clarity, completeness, or actionability of the summary — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- C) Increase the model's capability tier, assuming higher capability always improves recruiter satisfaction.
- D) Ignore recruiter feedback scores in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends full candidate-conversation history plus a large static company hiring-policy document on every turn of multi-turn recruiter chats.

- A) This has no optimization opportunity since full history is always required.
- B) Apply prompt caching to the static hiring-policy document and consider trimming or summarizing older turns of conversation history to reduce redundant token cost across a multi-turn conversation.
- C) Remove the hiring-policy document entirely to save tokens.
- D) Switch to a smaller model as the only lever for reducing token cost.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- B) Raw logging at full volume is itself a sufficient observability strategy.
- C) Reduce logging to save storage cost, with no other change.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a recent screening-quality regression was caused by a recent prompt change, a recent model version change, or a job-requisition data change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) Revert all three changes without investigation, regardless of which (if any) caused the regression.
- D) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.

**Question 44.** An automated eval asserts that a candidate-summary output must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Temperature should be increased to fix the intermittent failures.
- D) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, fairness) so a healthy top-line number doesn't mask a specific failing area.
- B) A single number is always achievable and sufficient for any system's evaluation needs.
- C) Use screening throughput alone as the single number, since it's the system's stated purpose.
- D) Refuse to provide any single summary metric under any circumstances.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

The Department of Civic Services, a state benefits agency, is deploying a Claude-powered system that processes constituent benefits applications and assists a 25-person case-management team using Claude Code internally, operating within a FedRAMP Moderate authorization boundary. You are responsible for governance, compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk since compliance can always be added right before launch.
- B) Compliance only affects legal documentation, not system architecture.
- C) HIPAA, not FedRAMP, is the relevant regime for a public-sector benefits system.
- D) FedRAMP-driven data boundary, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.

**Question 47.** A team proposes requiring human approval on every single output the benefits-eligibility system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for public-sector AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) This approach is required by FedRAMP regardless of other considerations.
- D) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from applicant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) A single generic guardrail addresses all three risk types equally well.
- C) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- D) These risks are exclusive to non-government use cases.

**Question 49.** The case-management team asks whether the system's eligibility recommendations could produce disparate outcomes across different applicant demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- C) Disparate impact is impossible in an LLM-based system by construction.
- D) This concern only applies to systems making final eligibility decisions, not any assistive system.

**Question 50.** The 25-person case-management team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- B) Have each staff member individually troubleshoot their own local configuration.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for a FedRAMP-authorized system.
- B) AI-assisted code should bypass standard review since it was "written by AI."
- C) Only a spot-check of AI-generated code is necessary.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- C) Disable Claude Code for the team entirely following any incident.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The case-management team wants a documented, repeatable workflow for a recurring task (generating a weekly caseload-compliance report) versus a one-off exploratory coding task.

- A) Build both as ad hoc, undocumented prompts each time they're needed.
- B) Build both as MCP servers regardless of reuse profile.
- C) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance team wants documented evidence of who accessed what applicant-related data through the system and when.

- A) Access logging is optional if the system has role-based permissions.
- B) Audit logging can be added later without architectural impact.
- C) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- D) Only failed access attempts need to be logged.

**Question 55.** The steering committee for this deployment includes program-office, legal, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms program-office and legal stakeholders can evaluate against their own priorities, not just engineering metrics.
- C) Skip stakeholder communication until the system is fully built.
- D) Use identical technical documentation for all three audiences to save effort.

**Question 56.** Midway through the project, the case-management team's requirements shift meaningfully based on a new state regulatory guidance document.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Incorporate the change silently without informing stakeholders of the impact.
- C) Restart the entire project from scratch regardless of the change's actual scope.
- D) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- C) Lifecycle responsibility ends once the contract is signed.
- D) Monitoring is only necessary if a major incident occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Only the original architect should ever be allowed to modify the system, making documentation moot.
- D) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.

**Question 59.** The case-management team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- C) Ban Claude Code for all documentation tasks without evaluation.
- D) Mandate Claude Code usage for all tasks regardless of measured benefit.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Restrict debugging to a single designated engineer.
- C) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key — Practice Exam 11

**Quick key:** 1-D, 2-C, 3-A, 4-A, 5-C, 6-B, 7-B, 8-A, 9-C, 10-D, 11-A, 12-D, 13-D, 14-A, 15-A, 16-B, 17-C, 18-B, 19-C, 20-D, 21-D, 22-C, 23-A, 24-A, 25-A, 26-C, 27-B, 28-C, 29-C, 30-A, 31-B, 32-B, 33-D, 34-C, 35-D, 36-B, 37-A, 38-C, 39-D, 40-B, 41-B, 42-A, 43-D, 44-D, 45-A, 46-D, 47-D, 48-C, 49-B, 50-A, 51-A, 52-B, 53-C, 54-C, 55-B, 56-D, 57-B, 58-D, 59-B, 60-C

---

**1. D** — The stated goal (3x volume, same headcount, same defensibility standard) is a throughput/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, B, and C either misname the pillar or skip the framing that keeps the project aligned to what discovery actually found.

**2. C** — Steps that vary by document and depend on intermediate findings are the defining case for an agentic pattern. A assumes a predictability the scenario explicitly lacks; B undersells the orchestration actually needed; D ignores that the patterns have real, non-interchangeable tradeoffs.

**3. A** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. B and D sacrifice these properties for a shortcut; C discards the specialization that motivated separate subagents in the first place.

**4. A** — Every subagent succeeding while whole document-source categories are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. B, C, and D all patch downstream instead of fixing the actual scope gap.

**5. C** — Business value pillars (efficiency, defensibility, cost-per-gigabyte, cycle time) give both the architecture and its metrics a clear anchor. A, B, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. B** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and C treat it as out of scope; D overreacts to sentiment alone without weighing it against the technical case.

**7. B** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. A and C withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. A** — Adding a feedback loop that captures attorney overrides and outcomes as a first-class architectural component is what lets the system improve after deployment, per the input→processing→output→feedback loop framing. B, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. C** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and D over-engineer a simple augmentation need; B is factually wrong.

**10. D** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and B ignore this real degradation; C doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (classification) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. D** — A steering committee needs the architecture communicated at the level of case-outcome and cost evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; C skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. A** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. B ignores a known future need entirely; C wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. A** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. B, C, and D all leave the actual knowledge transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and D ignore fit-to-task; C sacrifices quality on the cases that need capability most.

**17. C** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and D all misstate or break the caching opportunity.

**18. B** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and D ignore this mismatch; C discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and D force one mechanism onto queries it doesn't fit; B denies a real, consequential distinction.

**20. D** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, B, and C all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the reviewer rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict.

**22. C** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and B are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. A** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. B, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. C** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; D doesn't address correctness; C incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. C** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and B assume benchmark gains transfer automatically; D over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially fairness-relevant edge cases. A, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. C** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and D misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. D** — A regression tied specifically to a data refresh event, with model and latency unchanged, points first at retrieval/indexing. A, B, and C would not specifically correlate with a job-requisition data refresh.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. C** — Segmenting accuracy by role/candidate type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. D** — An isolated throughput improvement could mask a worsened fairness-related failure mode; checking specifically for that before shipping is the correct diagnostic step. A and C ship without adequate testing; B incorrectly claims the failure mode is unmeasurable.

**40. B** — "Accurate but poorly rated" points at an unmeasured quality dimension (clarity, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. B** — Caching the static hiring-policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; D is a blunt, quality-risking lever when a more targeted fix is available.

**42. A** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. B and D accept the described dysfunction; C addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. D** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and C misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. A** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. B and C oversimplify to a single lossy number; D refuses a reasonable, common stakeholder request.

**46. D** — FedRAMP-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. D** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; C misattributes this to FedRAMP, which doesn't mandate universal review.

**48. C** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; B assumes one guardrail covers distinct risk types; D is factually wrong.

**49. B** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; C and D make unsupported blanket claims.

**50. A** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. A** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in a FedRAMP-authorized system. B, C, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; D is a disproportionate reaction that doesn't investigate the actual cause.

**53. C** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. A under-serves the recurring task; B over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. C** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by program-office, legal, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. D** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. A and B mishandle a real change; C disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. D** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and C all leave that reasoning undocumented and effectively lost.

**59. B** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and D over-assume benefit; C forecloses potential benefit without evaluation.

**60. C** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; B and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 11.*
