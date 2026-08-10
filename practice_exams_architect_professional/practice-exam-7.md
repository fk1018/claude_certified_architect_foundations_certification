# CCARP Practice Exam 7

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform for a Legal Services Firm, RAG and Model Tiering for a Pharmaceutical Literature-Review Platform, Evaluation and Optimization of an HR Recruiting Assistant, Governance and Enablement for a Public-Sector FedRAMP Deployment) |
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

Meridian Discovery Partners, a litigation-support firm serving Am Law 100 clients, is building a Claude-powered e-discovery platform to review, tag, and produce documents for active litigation matters. The platform must classify documents for relevance, screen for attorney-client privilege, and route borderline calls to reviewing attorneys. You are the architect responsible for the multi-agent design and for running discovery with the firm's litigation-support leadership.

---

**Question 1.** Discovery with Meridian's litigation-support leadership reveals the actual goal: processing 5x the current document-review volume during peak discovery windows, using the same review team size and without increasing average per-document review time.

- A) Frame the architecture around transformation, since AI initiatives should introduce net-new capability.
- B) Frame the architecture around efficiency, and build success metrics around review throughput per reviewer rather than novel capability.
- C) Frame the architecture around risk reduction exclusively, regardless of what discovery actually surfaced.
- D) Skip framing around a specific value pillar, since a working system speaks for itself.

**Question 2.** Document-review steps vary by document type, by findings from earlier documents in the same custodian's collection, and by whether a privilege flag was already raised — the right next step isn't knowable in advance.

- A) A fixed workflow, since document review is a well-established process with known steps.
- B) An augmented LLM pattern, since a single enhanced call can resolve any document-review question.
- C) An agentic pattern, since the right steps vary by document and depend on findings discovered along the way.
- D) Whichever pattern the vendor's existing tooling already supports, since the patterns are functionally interchangeable.

**Question 3.** The proposed design uses a coordinator agent delegating to specialized subagents: document classification, privilege screening, relevance tagging, and production formatting.

- A) Let each subagent pass its output directly to whichever subagent needs it next, skipping the coordinator to save hops.
- B) Merge all four responsibilities into a single subagent to eliminate coordination overhead entirely.
- C) Route all inter-subagent communication through the coordinator, preserving observability, consistent error handling, and controlled information flow.
- D) Allow direct subagent-to-subagent communication, but require each subagent to log its own traffic separately.

**Question 4.** Every subagent performs its assigned task correctly, but the coordinator's decomposition routes only email and standard office documents through the pipeline — text messages and voicemail transcripts are never assigned to any subagent and silently skip review entirely.

- A) Add a fifth subagent purely to catch unrecognized document formats.
- B) Instruct the existing subagents, via prompt, to flag any document type they don't recognize.
- C) Fix the coordinator's decomposition so it explicitly covers all document formats in the collection, rather than tuning the subagents that are already working correctly.
- D) Expand each subagent's tool access so any subagent can process any document type.

**Question 5.** The design must align the technical architecture to a specific business value pillar the firm's leadership actually cares about, rather than a generic "we added AI to document review" narrative.

- A) Efficiency, risk reduction, cost, and defensibility (audit-trail quality) are examples of such pillars; the one chosen should drive both the architecture and its success metrics.
- B) Any AI-assisted review process inherently demonstrates transformation, so no additional framing is required.
- C) Business value pillars are a business-development concern, not an architectural one.
- D) The pillar should be selected after launch, based on whichever metric happens to look best.

**Question 6.** Discovery interviews with the firm's contract reviewers and paralegals repeatedly surface anxiety that the platform will eliminate their roles.

- A) Disregard the sentiment, since it isn't a stated technical requirement.
- B) Proceed with the technical design and let a separate change-management effort handle morale with no architectural input.
- C) Recommend cancelling the project based on the sentiment alone.
- D) Treat the sentiment as a real implicit constraint alongside the explicit requirements — it should shape rollout sequencing and where human-in-the-loop checkpoints matter most.

**Question 7.** A partner asks why the privilege-screening subagent runs on a higher-capability, higher-cost model tier than the document-classification subagent.

- A) Explain the tradeoff explicitly: privilege determinations carry high error cost and require deeper reasoning that justifies the added cost and latency, while classification is simpler and better served by a faster, cheaper tier.
- B) Respond that the higher tier is used "because privilege is important," without further detail.
- C) Avoid the question, since partners don't need to understand technical tier decisions.
- D) Standardize on one tier for both subagents for simplicity, regardless of task difficulty.

**Question 8.** The current design produces a final privilege/relevance recommendation with no mechanism to capture attorney overrides or downstream case outcomes for future improvement.

- A) This is acceptable, since the initial classification logic already reflects current best practice.
- B) Add a feedback loop that captures attorney overrides and downstream outcomes as a first-class architectural component, so the system can improve after deployment.
- C) Feedback loops are a data-science concern with no architectural implication.
- D) Defer any feedback mechanism to a hypothetical future phase with no design hooks in the current build.

**Question 9.** For a narrower need, the firm wants a single enhanced call — with retrieval over the firm's internal case-law and precedent database — to answer straightforward "has this privilege argument been raised before in this matter" questions, without multi-step autonomous orchestration.

- A) This requires a full multi-agent architecture regardless of how narrow the task is.
- B) This can't be built with Claude, since it doesn't involve autonomous agent behavior.
- C) This requires a fixed workflow of at least four sequential steps.
- D) An augmented LLM pattern — a single call enhanced with retrieval — fits this simpler augmentation need without the overhead of agentic orchestration.

**Question 10.** The document-classification subagent's toolset has grown to include tools for tasks like billing-code lookup and client-invoice generation, unrelated to classification.

- A) This carries no architectural downside as long as the subagent's prompt is well-written.
- B) More tools always increase a subagent's flexibility and should be encouraged as the platform grows.
- C) This capability bloat degrades tool-selection reliability; the unrelated tools should be removed or relocated to a more appropriate subagent.
- D) The correct fix is to increase the subagent's context window rather than its toolset.

**Question 11.** The coordinator currently runs document classification, then privilege screening, then relevance tagging, then production formatting strictly in sequence, even though privilege screening and relevance tagging have no dependency on each other's output.

- A) Run privilege screening and relevance tagging as independent, parallel subagent calls once classification completes, rather than sequentially.
- B) Sequential processing is required to preserve an admissible audit trail.
- C) Parallelization isn't achievable within a coordinator/subagent architecture.
- D) Combine privilege screening and relevance tagging into one subagent to sidestep the sequencing question.

**Question 12.** Firm leadership asks how the end-to-end architecture should be described to a steering committee of partners unfamiliar with the technical implementation.

- A) Present only the model names and per-document token costs involved.
- B) Present the complete technical architecture diagram with no simplification.
- C) Describe input → processing → output → feedback loop at a level the committee can evaluate against defensibility and throughput goals, without requiring them to understand implementation internals.
- D) Skip a high-level description and move directly into a live system demo.

**Question 13.** A competing vendor proposes a single generalist agent holding every tool (classification, privilege logic, relevance tagging, production formatting) instead of a coordinator with specialized subagents.

- A) A single generalist agent scales better as the number of tools grows.
- B) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- C) There is no meaningful architectural difference between the two approaches.
- D) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.

**Question 14.** The platform must eventually support a new matter type (regulatory investigations with different privilege rules) the firm expects to take on next year, but detailed requirements aren't defined yet.

- A) Ignore future matter types entirely until requirements exist.
- B) Build full support for regulatory-investigation privilege rules now, guessing at undefined requirements.
- C) Design the current decomposition and subagent boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.
- D) Refuse to proceed with the current phase until next year's requirements are finalized.

**Question 15.** Firm leadership wants documentation they can hand to a new engineering vendor in a year, who will extend the platform without the original architect present.

- A) Document only the final configuration values, since the implementation is self-explanatory.
- B) Document the architecture and the reasoning behind key decisions — pattern choices, subagent boundaries, tier selections — not just the final "what."
- C) Rely on the original architect remaining available indefinitely instead of documenting.
- D) Documentation is unnecessary if the code and prompts are well-organized.

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Verdant Biosciences operates a literature-review platform that helps pharmacovigilance and regulatory-affairs teams synthesize findings across journal articles, clinical-trial registries, and internal safety reports. You are architecting model tiering, prompting, and the retrieval layer that connects the platform to a constantly growing corpus of publications and structured trial data.

---

**Question 16.** Most literature-review questions on Verdant's platform are moderately complex; a small fraction require deep multi-step reasoning across many trial reports, and a small fraction are simple lookups (e.g., a single drug's approval date).

- A) Use one fixed model tier for every question, regardless of complexity.
- B) Route based on task difficulty — a fast tier for simple lookups, a balanced tier for typical synthesis questions, and a higher-capability tier (potentially with extended thinking) reserved for deep multi-document cases.
- C) Always use the fastest, cheapest tier to control cost, accepting quality loss on complex questions.
- D) Always use the highest-capability tier to guarantee quality regardless of question type.

**Question 17.** Every request sends the same long system prompt (regulatory-affairs persona, citation format, formatting rules) followed by retrieved excerpts that vary per query.

- A) Order has no effect on cost or latency for this workload.
- B) Interleave system instructions and retrieved content throughout the prompt.
- C) Put retrieved content first, since it's most specific to the query.
- D) Place the stable system prompt first and enable prompt caching, with the varying retrieved excerpts after it, to reduce latency and cost across high query volume.

**Question 18.** The corpus mixes long-form journal articles and trial reports with short structured records (a table of adverse-event counts by dose).

- A) Chunking and indexing strategy should match each data shape — long-form documents need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't fit.
- B) One chunking strategy tuned for long-form documents can serve both content types equally well.
- C) Structured adverse-event data should be excluded from retrieval entirely.
- D) Use the largest possible chunk size everywhere to avoid maintaining multiple strategies.

**Question 19.** Queries range from exact lookups ("what was the enrollment size of Trial NCT-1147") to conceptual questions ("how has the safety narrative for Drug X evolved across recent publications").

- A) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- B) Use only embedding similarity search for every query type.
- C) Use only structured/metadata filtering for every query type.
- D) Query pattern has no bearing on which retrieval approach is appropriate.

**Question 20.** Regulatory-affairs reviewers need citations that reliably map each claim to a specific source document and section, and prose responses often lose this mapping.

- A) Ask the model, in prose, to "always cite your sources" without further structure.
- B) Require structured output pairing each claim with its source (document, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- C) Add citations after the fact by searching for a plausible source for each claim.
- D) Append a general bibliography of consulted documents at the end of the response.

**Question 21.** Two retrieved sources report different adverse-event rates for the same trial arm — likely because one reports crude incidence and the other reports incidence adjusted for exposure time.

- A) Average the two figures and present the average as the answer.
- B) Omit the adverse-event rate entirely since the sources disagree.
- C) Always prefer whichever source was retrieved first.
- D) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation, rather than silently picking one.

**Question 22.** A prompt instructing the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Use tool-use/schema-constrained output so structure is enforced by the API mechanism rather than requested through prose alone.
- B) Repeat the instruction more emphatically in the prompt.
- C) Post-process every response to strip any text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to Verdant's proprietary internal safety-report system, exposing search and retrieval to several other internal Claude-powered tools beyond the literature-review platform.

- A) Build an MCP server exposing the safety-report operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the safety-report integration into this platform's application code only.
- C) Paste the entire safety-report corpus into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full trial-registry catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Progressive discovery — querying a catalog resource as needed — scales better than loading the entire catalog into context up front, especially as the registry grows.
- B) Loading the full catalog up front is always preferable for completeness.
- C) There's no meaningful difference in context cost between the two approaches.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** A researcher asks a question requiring the model to reason step by step across several trial reports and journal articles before concluding whether a safety signal is emerging.

- A) Zero-shot prompting with no reasoning guidance is always equally effective for this kind of question.
- B) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-document synthesis question.
- C) Chain-of-thought prompting is only useful for coding tasks.
- D) The model cannot reason across multiple documents regardless of prompting approach.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different researcher-facing features so changes propagate consistently.

- A) Duplicate the fragments into each feature's prompt independently.
- B) Modular prompts are the same mechanism as prompt caching.
- C) Standardization across features isn't achievable through prompt design.
- D) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- C) Increase output length so there's more room to be correct.
- D) This is a pure model limitation with no architectural mitigation available.

**Question 28.** The team debates whether researcher-facing latency SLAs should factor into model tier selection for the platform.

- A) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, rather than defaulting to the most capable tier regardless of SLA.
- B) Latency should never factor into model or architecture decisions.
- C) Only cost should factor into tier selection, never latency.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer benchmark scores always mean better production behavior.
- B) Never upgrade models once the initial version is chosen.
- C) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.
- D) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.

**Question 30.** The platform's context budget is a concern because the system prompt/citation rules and the retrieved excerpts must fit alongside room for a detailed, well-cited answer.

- A) Input and output token budgets are entirely independent of each other.
- B) This tradeoff only matters for very long documents, never for typical queries.
- C) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- D) Output length has no practical limit regardless of input size.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

A Claude-powered recruiting assistant screens resumes, drafts outreach messages, and answers candidate questions for TalentBridge, a mid-market staffing firm. It has been in production for four months, and you are responsible for the evaluation strategy, diagnosing quality regressions, and optimizing the cost/latency/accuracy tradeoff as volume grows.

---

**Question 31.** TalentBridge's team currently measures only resume-screening throughput and hasn't defined targets for latency, cost, or fairness.

- A) Throughput alone is sufficient since it's the assistant's primary purpose.
- B) Define evaluation metrics spanning accuracy, latency, cost, and safety/fairness as first-class metrics — an assistant that screens quickly but is slow elsewhere, too expensive, or biased still fails overall.
- C) Latency and cost are operations concerns unrelated to evaluation design.
- D) Fairness metrics are only relevant if a complaint is filed.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past candidate resumes.

- A) A single automated method is sufficient for any production system.
- B) Replace the automated checks entirely with only human review.
- C) Expand the labeled set indefinitely as the sole improvement lever.
- D) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for bias-relevant paths — since no single method covers every failure mode.

**Question 33.** The team wants to test whether a new outreach-message prompt improves candidate response rate before rolling it out to all traffic.

- A) Roll out the new prompt to all traffic immediately and monitor for problems.
- B) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.
- C) Change the prompt and the model tier simultaneously to maximize potential improvement.
- D) Skip testing since outreach-message changes are low-risk by nature.

**Question 34.** A candidate's screening summary misstates their years of relevant experience. Investigation shows the resume was parsed and retrieved correctly, and the model's response paraphrased the experience section inaccurately.

- A) This is a retrieval problem; fix the resume-parsing pipeline.
- B) This is best characterized as a prompt/generation issue — inaccurate paraphrasing of correctly retrieved content — which calls for prompt or output-validation fixes rather than retrieval changes.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This cannot be diagnosed without retraining the model.

**Question 35.** Immediately after a scheduled refresh of the job-requisition database, the assistant starts recommending mismatched candidates, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Suspect a temperature setting change, since the mismatches look erratic.
- C) Investigate the retrieval/indexing layer first, since the regression is tied specifically to the data refresh event with model and latency unchanged.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency in the screening pipeline but is worried about hurting candidate-match accuracy, and currently has no data on where the current configuration sits on that tradeoff curve.

- A) Cost, latency, and accuracy should each be optimized independently, in isolation from one another.
- B) Optimize cost/latency/accuracy jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the accuracy bar isn't a win, and neither is maximizing accuracy at unsustainable cost.
- C) Accuracy should always be maximized regardless of cost or latency implications.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average match-quality score.

- A) Monitoring should surface drift and outliers — a per-role or per-source breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since match quality is captured by the eval suite alone.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence screening decisions by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone.
- B) Aggregate accuracy is definitionally representative of every role and candidate segment.
- C) Human review should never be reduced regardless of measured accuracy.
- D) Segment accuracy by role and candidate source before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.

**Question 39.** An A/B test shows a new screening prompt improves throughput, but the team hasn't checked whether it also changed the false-negative rate for genuinely qualified candidates who should have advanced.

- A) Throughput alone is a sufficient signal to ship the change.
- B) Ship the change and monitor informally after the fact instead of testing beforehand.
- C) Check the qualified-candidate false-negative rate specifically before shipping — an isolated throughput improvement could be masking an increase in inappropriately filtered strong candidates.
- D) False-negative behavior on qualified candidates is not something evaluation can measure.

**Question 40.** The team wants to diagnose why a subset of screening summaries are factually accurate but rated poorly by hiring managers.

- A) Assume the accuracy metric is broken and discard it.
- B) Investigate a dimension beyond factual accuracy — e.g., tone, completeness, or actionability — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.
- C) Increase the model's capability tier, assuming higher capability always improves hiring-manager satisfaction.
- D) Ignore hiring-manager ratings in favor of the accuracy metric alone.

**Question 41.** The team is optimizing token usage and notices the system sends the full conversation history plus a large static compliance-policy document on every turn of multi-turn candidate conversations.

- A) Apply prompt caching to the static compliance-policy document and consider trimming or summarizing older turns of conversation history to reduce redundant token cost across a multi-turn conversation.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Remove the compliance-policy document entirely to save tokens.
- D) This has no optimization opportunity since full history is always required.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or a job-requisition data change — all three happened in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) Revert all three changes without investigation, regardless of which (if any) caused the regression.
- D) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.

**Question 44.** An automated eval asserts that an outreach-message draft must exactly match a fixed reference string, and the eval fails intermittently even on drafts a human reviewer would call correct.

- A) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- B) The model is malfunctioning and needs retraining.
- C) The reference string needs to be longer.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use throughput alone as the single number, since it's the assistant's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, fairness) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

The Department of Civic Records Modernization (DCRM), a state-level public-sector agency pursuing a FedRAMP Moderate authorization, is deploying a Claude-powered system that helps citizens navigate benefits applications, alongside a 25-person internal engineering team using Claude Code to build and maintain it. You are responsible for governance, ATO-relevant compliance, and developer enablement for the launch.

---

**Question 46.** DCRM's architecture team is finalizing data-boundary, retention, and access-logging design in the final weeks before the ATO assessment, after core application logic is already built.

- A) This sequencing carries no risk since compliance controls can always be added right before an ATO review.
- B) Compliance only affects documentation submitted for the ATO package, not system architecture.
- C) HIPAA, not FedRAMP, is the relevant regime for a state benefits agency.
- D) FedRAMP-driven data-boundary, retention, and access-control requirements can force structural changes that are far more costly to retrofit than to design in from the start.

**Question 47.** A team proposes requiring human approval on every single response the citizen-facing benefits assistant produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for public-sector AI systems.
- B) Human reviewers are categorically less accurate than the model, making review counterproductive.
- C) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions rather than applied universally.
- D) This approach is required by FedRAMP regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from citizen-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) These risks are exclusive to non-government use cases.
- C) A single generic guardrail addresses all three risk types equally well.
- D) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.

**Question 49.** Program staff ask whether the assistant's eligibility-guidance responses could produce disparate outcomes across different applicant demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Disparate impact is impossible in an LLM-based system by construction.
- C) This concern only applies to systems making final eligibility determinations, not any assistive system.
- D) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.

**Question 50.** The 25-person engineering team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Have each staff member individually troubleshoot their own local configuration.
- B) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- C) Restrict Claude Code usage to a single designated engineer to reduce variance.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) AI-assisted code should bypass standard review since it was "written by AI."
- B) Only a spot-check of AI-generated code is necessary.
- C) Standard SDLC practices — code review, testing, version control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for an authorized system.
- D) Review requirements should be lower for AI-generated code than human-written code.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- B) Disable Claude Code for the team entirely following any incident.
- C) Roll back all recent Claude Code-assisted changes regardless of relevance.
- D) Assume the bug is in the generated code without investigation.

**Question 53.** The engineering team wants a documented, repeatable workflow for a recurring task (generating a weekly ATO-evidence summary) versus a one-off exploratory coding task.

- A) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory task as an unstructured session, since it doesn't need standing infrastructure.
- B) Build both as ad hoc, undocumented prompts each time they're needed.
- C) Build both as MCP servers regardless of reuse profile.
- D) Recurring workflows and one-off tasks should be built identically.

**Question 54.** The compliance office wants documented evidence of who accessed what citizen data through the system and when, as part of the ATO evidence package.

- A) Access logging is optional if the system has role-based permissions.
- B) Audit logging can be added later without architectural impact.
- C) Only failed access attempts need to be logged.
- D) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.

**Question 55.** The steering group for this deployment includes program office, ATO assessors, and engineering stakeholders with different priorities and vocabularies.

- A) Tailor architectural communication to each audience — tradeoffs framed in terms program-office and ATO-assessor stakeholders can evaluate against their own priorities, not just engineering metrics.
- B) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- C) Skip stakeholder communication until the system is fully built.
- D) Use identical technical documentation for all three audiences to save effort.

**Question 56.** Midway through the project, eligibility requirements shift meaningfully based on new state regulatory guidance.

- A) Refuse to incorporate the change since requirements were already agreed upon.
- B) Incorporate the change silently without informing stakeholders of the impact.
- C) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending once the system passes its ATO assessment.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle responsibility ends once the ATO is granted.
- C) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through authorization.
- D) Monitoring is only necessary if a major incident occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The engineering team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Assume AI-assisted tooling always saves time on every task category by default.
- B) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- C) Mandate Claude Code usage for all tasks regardless of measured benefit.
- D) Ban Claude Code for all documentation tasks without evaluation.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging to a single designated engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key

**Quick key:** 1-B, 2-C, 3-C, 4-C, 5-A, 6-D, 7-A, 8-B, 9-D, 10-C, 11-A, 12-C, 13-D, 14-C, 15-B, 16-B, 17-D, 18-A, 19-A, 20-B, 21-D, 22-A, 23-A, 24-A, 25-B, 26-D, 27-B, 28-A, 29-D, 30-C, 31-B, 32-D, 33-B, 34-B, 35-C, 36-B, 37-A, 38-D, 39-C, 40-B, 41-A, 42-C, 43-D, 44-A, 45-D, 46-D, 47-C, 48-D, 49-D, 50-B, 51-C, 52-A, 53-A, 54-D, 55-A, 56-C, 57-C, 58-C, 59-B, 60-B

---

**1. B** — The stated goal (more volume, same headcount, same cycle time) is an efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A, C, and D either misname the pillar or skip the framing discovery actually surfaced.

**2. C** — Steps that vary by document and depend on findings discovered along the way are the defining case for an agentic pattern. A assumes a predictability the scenario lacks; B undersells the orchestration needed; D ignores real, non-interchangeable tradeoffs between the patterns.

**3. C** — Hub-and-spoke routing through the coordinator preserves observability, consistent error handling, and controlled information flow. A and D sacrifice these properties for a shortcut; B discards the specialization that motivated separate subagents.

**4. C** — Every subagent succeeding while whole document formats are never routed at all is a decomposition problem at the coordinator level, not a subagent performance problem. A, B, and D all patch downstream instead of fixing the actual scope gap.

**5. A** — Business value pillars (efficiency, risk reduction, cost, defensibility) give both the architecture and its metrics a clear anchor. B, C, and D all skip or defer this framing in ways that risk building toward the wrong measure of success.

**6. D** — Adoption sentiment is a real implicit constraint that should shape rollout sequencing and where human-in-the-loop checkpoints matter — it's discovery input, not noise to ignore. A and B treat it as out of scope; C overreacts to sentiment alone without weighing it against the technical case.

**7. A** — Explaining the specific tradeoff (deeper reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. B and C withhold the reasoning stakeholders need; D removes a deliberate, justified difference for false simplicity.

**8. B** — Adding a feedback loop that captures attorney overrides and outcomes as a first-class architectural component is what lets the system improve after deployment. A, C, and D all treat a first-class architectural component as optional or someone else's problem.

**9. D** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. A and C over-engineer a simple augmentation need; B is factually wrong.

**10. C** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows — the fix is removing or relocating them, not just writing around it. A and B ignore this real degradation; D doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (classification) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. C** — A steering committee needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A is insufficient detail; B is too much of the wrong kind of detail; D skips the communication need entirely.

**13. D** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. A, B, and C understate or deny this real architectural tradeoff.

**14. C** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A ignores a known future need entirely; B wastes effort guessing at undefined requirements; D blocks current delivery unnecessarily.

**15. B** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, C, and D all leave the actual knowledge-transfer gap unaddressed.

**16. B** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and C ignore fit-to-task; D sacrifices quality on the cases that need capability most.

**17. D** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and C all misstate or break the caching opportunity.

**18. A** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. B and D ignore this mismatch; C discards useful structured data.

**19. A** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. B and C force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. B** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. A, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. D** — Presenting both figures with attribution and likely methodological explanation preserves the actual information for the reviewer rather than resolving a real discrepancy arbitrarily. A, B, and C all discard or obscure a genuine data conflict.

**22. A** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. B and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. A** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. B and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. B** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-document synthesis requiring step-by-step reasoning. A, C, and D all misstate the fit or capability of prompting techniques for this task.

**26. D** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. A reintroduces duplication; B conflates two distinct mechanisms; C denies a real, common architecture pattern.

**27. B** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; C doesn't address correctness; D incorrectly claims no architectural mitigation exists.

**28. A** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. B, C, and D each drop a relevant factor from the decision.

**29. D** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and C assume benchmark gains transfer automatically; B over-corrects into permanent stagnation.

**30. C** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. A, B, and D all misstate this real, architecture-relevant constraint.

**31. B** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. A, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. D** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially bias-relevant edge cases. A, B, and C each over-rely on or discard one method without addressing the actual coverage gap.

**33. B** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; C confounds two variables; D dismisses a real risk without evidence.

**34. B** — Correct retrieval plus inaccurate paraphrasing is a generation-side issue, calling for prompt/output-validation fixes rather than retrieval or model-tier changes. A and C misdiagnose the layer at fault; D avoids diagnosis entirely.

**35. C** — A regression tied specifically to a data-refresh event, with model and latency unchanged, points first at retrieval/indexing. A, B, and D would not specifically correlate with a requisition-database refresh.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "accuracy at all costs" outcome and a cheap configuration that fails the accuracy bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. D** — Segmenting accuracy by role and candidate source before cutting review protects against a failing segment hiding behind a healthy aggregate. A and B trust the aggregate uncritically; C over-corrects by refusing any reduction regardless of evidence.

**39. C** — An isolated throughput improvement could mask a worsened false-negative rate on qualified candidates; checking specifically for that before shipping is the correct diagnostic step. A and B ship without adequate testing; D incorrectly claims the failure mode is unmeasurable.

**40. B** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, completeness, actionability) rather than a broken accuracy metric. A and D discard a working, differently-scoped metric; C assumes a fix without diagnosis.

**41. A** — Caching the static compliance-policy document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. D denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. A** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. B and D misdiagnose model behavior as broken; C doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. D** — FedRAMP-driven requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. C** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and B overstate the universal safety case for maximal review; D misattributes this requirement to FedRAMP, which isn't what the regime mandates.

**48. D** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; C assumes one guardrail covers distinct risk types; B is factually wrong.

**49. D** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and C make unsupported blanket claims.

**50. B** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. A and D leave the systemic cause unaddressed; C sacrifices the tool's benefit for the rest of the team.

**51. C** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially in an authorized system. A, B, and D all propose reducing rigor specifically because AI was involved, which is the wrong direction for a regulated context.

**52. A** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. C and D skip diagnosis; B is a disproportionate reaction that doesn't investigate the actual cause.

**53. A** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory task unstructured avoids unnecessary standing infrastructure. B under-serves the recurring task; C over-engineers the one-off task; D ignores that reuse profile should drive the choice.

**54. D** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, B, and C each understate what ATO-grade audit evidence actually requires.

**55. A** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by program-office, assessor, and engineering audiences alike. B, C, and D each fail to serve at least one audience's real information need.

**56. C** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally driven requirements shift. A and B mishandle a real change; D disproportionately discards unaffected work.

**57. C** — Lifecycle management extends through monitoring and iteration based on production signal, not just through discovery and authorization. A, B, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. B** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. A and C over-assume benefit; D forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 7.*
