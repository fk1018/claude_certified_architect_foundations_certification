# CCARP Practice Exam 3

**Claude Certified Architect – Professional — Practice Exam**

| | |
|---|---|
| Questions | 60 |
| Time limit | 120 minutes |
| Format | Single-answer practice set — every item has exactly one correct answer and three distractors. |
| Scenarios | 4 (Multi-Agent E-Discovery Platform, Pharmaceutical RAG and Model Tiering, HR Recruiting Assistant Evaluation & Optimization, Public-Sector FedRAMP Governance & Enablement) |
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

Harlow & Voss LLP, a 400-attorney litigation firm, is building a multi-agent e-discovery platform to review, classify, and produce documents for active matters. The platform must handle document intake/OCR, responsiveness classification, privilege review, redaction, and production formatting across matters governed by different protective orders. You are the architect responsible for the end-to-end design and for running discovery with litigation-support staff and partner stakeholders.

---

**Question 1.** Discovery reveals the firm's actual goal is reducing the per-matter cost of first-pass document review by using fewer contract attorneys, while maintaining the same review turnaround time — not adding entirely new review capabilities.

- A) Frame the architecture around transformation, since AI-assisted review is inherently transformative.
- B) Frame the architecture around performance SLAs exclusively, ignoring the cost objective discovery surfaced.
- C) Frame the architecture around new capability, since first-pass review didn't previously use AI at all.
- D) Frame the architecture around cost/efficiency, and build success metrics around cost-per-document and reviewer headcount rather than novel capability.

**Question 2.** Document intake, responsiveness classification, privilege review, and redaction each require different steps depending on document type, matter-specific protective order terms, and findings from prior steps (e.g., a privilege hit changes downstream handling).

- A) An agentic pattern, since the right steps vary by document and depend on intermediate findings.
- B) A fixed workflow, since document review is a standardized business process.
- C) An augmented LLM pattern, since a single enhanced call is sufficient for any matter.
- D) Whichever pattern ships fastest, since the patterns are functionally interchangeable.

**Question 3.** In the proposed coordinator/subagent design, the privilege-review subagent identifies a document as privileged and needs the redaction subagent to apply redactions before production.

- A) Route the privilege determination through the coordinator, which then dispatches to the redaction subagent — preserving observability and consistent handling of privilege calls across the matter.
- B) Let the privilege-review subagent call the redaction subagent directly to save a hop.
- C) Merge privilege review and redaction into a single subagent to avoid coordination entirely.
- D) Have every subagent broadcast its findings to all other subagents indiscriminately.

**Question 4.** Every subagent completes its assigned work correctly, but the responsiveness-classification and privilege-review subagents each independently re-run OCR on the same intake documents, since neither receives the intake subagent's OCR output.

- A) Add a fifth subagent dedicated solely to OCR deduplication.
- B) Give the intake subagent tool access to write directly into each downstream subagent's private context.
- C) Fix the coordinator's data flow so intake's OCR output is passed downstream to each subagent that needs it, rather than having subagents redundantly regenerate it.
- D) Increase the context window of the responsiveness-classification subagent so it can OCR faster.

**Question 5.** Discovery with partners surfaces that what actually worries them is defensibility of privilege calls in front of a judge, not raw review speed or cost.

- A) Ignore this since cost was the pillar named in the original engagement letter.
- B) Treat defensibility as identical to cost efficiency, since both are business concerns.
- C) Reframe the pillar toward auditability/defensibility — accuracy, explainability, and audit trails for privilege calls — since that is what discovery actually surfaced, and design metrics around it.
- D) Add defensibility as a documentation footnote without changing metrics or design.

**Question 6.** Discovery interviews reveal review attorneys are worried the AI will be used as the sole justification for withholding documents without attorney sign-off, exposing the firm to sanctions risk.

- A) Ignore the sentiment since it's a change-management issue, not architecture.
- B) Proceed with full automation of withholding decisions and address the sentiment only through a communications campaign.
- C) Treat this as a real constraint requiring a human-in-the-loop checkpoint before any document is withheld from production, and design the escalation path as part of the architecture.
- D) Recommend the firm abandon the AI review project based on the sentiment alone.

**Question 7.** A partner asks why the privilege-review subagent uses a higher-capability model tier than the intake/OCR subagent.

- A) Explain the tradeoff: privilege determination requires nuanced legal reasoning that justifies the added cost/latency, while OCR/intake is comparatively mechanical and suited to a faster, cheaper tier.
- B) Say the higher tier is used everywhere "to be safe," regardless of task.
- C) Avoid explaining the difference, since partners don't need technical detail.
- D) Say the tier choice was arbitrary and could be swapped without effect.

**Question 8.** The current design produces final privilege/responsiveness calls with no mechanism to capture reviewing-attorney overrides for future improvement.

- A) This is acceptable; the initial classifier already reflects current best practice.
- B) Feedback loops are a data-science concern unrelated to the architecture.
- C) Defer any feedback mechanism to an undefined future phase with no design hooks today.
- D) Add a feedback loop capturing attorney overrides and their reasons as a first-class architectural component, so the system can improve after deployment.

**Question 9.** A partner wants a single enhanced call — with retrieval over a matter's document set — to answer a quick question like "do we have any emails between X and Y," without multi-step autonomous orchestration.

- A) An augmented LLM pattern (a single call enhanced with retrieval) fits this simple augmentation need without the overhead of agentic orchestration.
- B) This requires the full multi-agent e-discovery pipeline regardless of the simplicity of the ask.
- C) This cannot be done with Claude, since it isn't a full agent.
- D) This requires a fixed workflow with at least five sequential steps.

**Question 10.** The intake/OCR subagent's toolset has grown to include billing-code lookup and calendar-scheduling tools unrelated to document intake.

- A) This has no downside as long as the prompt is well-written.
- B) This capability bloat degrades tool-selection reliability; unrelated tools should be removed or relocated to a more appropriate subagent.
- C) More tools always increase flexibility and should be encouraged.
- D) The fix is to enlarge the subagent's context window.

**Question 11.** The coordinator currently runs responsiveness classification and privilege review sequentially for each document, though neither depends on the other's output once intake/OCR completes.

- A) Run responsiveness classification and privilege review as independent, parallel subagent calls once intake completes, rather than sequentially.
- B) Sequential processing is required for defensibility in litigation.
- C) Parallelization isn't possible in a coordinator/subagent architecture.
- D) Combine both into a single subagent to avoid the sequencing question.

**Question 12.** The firm's managing partners, unfamiliar with technical detail, ask how the e-discovery architecture should be described to the executive committee.

- A) Present only model names and token costs.
- B) Present the full technical architecture diagram with no simplification.
- C) Skip a high-level description and go straight to a live demo.
- D) Describe intake → classification → privilege review → production → feedback loop at a level the committee can evaluate against cost, risk, and turnaround outcomes, without requiring implementation detail.

**Question 13.** A competing vendor proposes one generalist agent holding every tool (OCR, classification, privilege review, redaction, production formatting) instead of a coordinator with specialized subagents.

- A) A single agent holding every tool and responsibility is more likely to suffer degraded tool-selection reliability than specialized subagents scoped to narrower roles.
- B) A single generalist agent scales better as tool count grows.
- C) Specialized subagents are strictly a cost-increasing choice with no reliability benefit.
- D) There's no meaningful architectural difference between the two approaches.

**Question 14.** The platform must eventually support foreign-language document review, a matter type planned for next year, but detailed requirements aren't finalized.

- A) Build full foreign-language support now, guessing at unspecified requirements.
- B) Ignore future foreign-language needs until requirements are formally scoped.
- C) Refuse to proceed with the current phase until future requirements are finalized.
- D) Design the current decomposition and subagent/tool boundaries with reasonable extensibility in mind, without over-building for speculative, undefined requirements.

**Question 15.** The steering committee wants documentation a new engineering team can use to extend the system next year without the original architect present.

- A) Document only final configuration values, since implementation is self-explanatory.
- B) Rely on the original architect remaining available indefinitely instead of documenting.
- C) Documentation is unnecessary if the code is well-organized.
- D) Document the architecture and the reasoning behind key decisions — pattern choices, decomposition boundaries, tier selections — not just the final "what."

---

## Scenario B: RAG and Model Tiering for a Pharmaceutical Literature-Review Platform (Questions 16–30)

Aventra Biosciences' medical affairs team needs Claude to answer scientist questions using both general reasoning and retrieval over a large, constantly-updated corpus of clinical trial protocols, published literature, and internal study reports. You are architecting model selection, prompting, and the integration layer.

---

**Question 16.** Most scientist questions are moderately complex; a small fraction require deep multi-step reasoning across many studies, and a small fraction are simple lookups (e.g., "what was the primary endpoint in Study 204").

- A) Always use the highest-capability tier to guarantee quality on every question.
- B) Always use the fastest tier to minimize cost, accepting quality loss on complex questions.
- C) Route by task difficulty — a fast tier for simple lookups, a balanced tier for typical questions, and a higher-capability tier (potentially with extended thinking) reserved for deep multi-step cases.
- D) Use one fixed model tier for all questions regardless of complexity.

**Question 17.** Every request sends the same long system prompt (scientific-writing persona, citation format, disclaimer language) followed by retrieved excerpts that vary per query.

- A) Order doesn't affect cost or latency for this use case.
- B) Put retrieved content first, since it's most relevant to the specific query.
- C) Place the stable system prompt first and enable prompt caching, with the varying retrieved content after it, to reduce latency and cost across high query volume.
- D) Alternate system instructions and retrieved content throughout the prompt.

**Question 18.** The corpus mixes long-form clinical study reports with short structured data (a table of adverse-event rates by treatment arm).

- A) One chunking/indexing strategy tuned for long-form documents can serve both content types equally well.
- B) Use the largest possible chunk size for everything to avoid needing multiple strategies.
- C) Chunking and indexing strategy should match each data shape — long-form reports need different chunking than short structured records, or retrieval quality degrades for whichever type doesn't match.
- D) Structured adverse-event data should be excluded from retrieval entirely.

**Question 19.** Scientist queries range from exact lookups ("primary endpoint for Study 204") to conceptual questions ("how has the safety narrative for Compound X evolved across trials").

- A) Use only embedding similarity search for every query type.
- B) Use only structured/metadata filtering for every query type.
- C) Match retrieval strategy to query pattern: structured/metadata filtering for exact lookups, embedding similarity search for conceptual questions, and hybrid retrieval where both are needed.
- D) Query pattern doesn't affect which retrieval approach is appropriate.

**Question 20.** Scientists need citations that reliably map each claim to a specific study and section, and generic prose responses often lose this mapping.

- A) Require structured output pairing each claim with its source (study, section, excerpt) so citation mapping survives synthesis rather than being reconstructed from memory.
- B) Ask the model, in prose, to "always cite sources" without further structure.
- C) Add citations after the fact by searching for a plausible source for each claim.
- D) Append a general bibliography of consulted documents at the end of each response.

**Question 21.** Two retrieved sources disagree on a trial's reported adverse-event rate by a small margin — likely different analysis populations (intent-to-treat vs. per-protocol).

- A) Present both figures explicitly annotated as a discrepancy, with source attribution and the likely methodological explanation (e.g., ITT vs. per-protocol), rather than silently picking one.
- B) Average the two figures and present the average.
- C) Omit the adverse-event rate entirely, since sources disagree.
- D) Always prefer whichever source was retrieved first.

**Question 22.** A prompt asking the model to "always output valid structured JSON with citation fields" still occasionally produces a conversational preamble before the JSON.

- A) Repeat the instruction more emphatically in the prompt.
- B) Use tool-use/schema-constrained output so the structure is enforced by the API mechanism rather than requested through prose alone.
- C) Post-process every response to strip leading text before the first `{`.
- D) Increase max_tokens to leave room for both the preamble and the JSON.

**Question 23.** The platform needs to connect to a proprietary internal study-repository system, exposing search and retrieval capabilities to multiple different internal Claude-powered tools beyond this literature-review platform.

- A) Build an MCP server exposing the study-repository operations as tools/resources, reusable across the multiple internal Claude-powered tools that need it.
- B) Hard-code the integration into this platform's application code only.
- C) Paste the entire study repository into every prompt.
- D) Require each consuming tool to reimplement its own integration independently.

**Question 24.** The team is deciding between exposing the full study catalog directly in every prompt versus letting the agent query a catalog resource only when needed.

- A) Loading the full catalog up front is always preferable for completeness.
- B) Progressive discovery (querying a catalog resource as needed) scales better than loading the entire catalog into context up front, especially as the corpus grows.
- C) There's no meaningful difference in context cost between the two approaches.
- D) The catalog should never be exposed to the agent in any form.

**Question 25.** A scientist asks a chain-of-thought-friendly question requiring the model to reason step by step across several retrieved studies before concluding.

- A) Zero-shot prompting with no reasoning guidance is always equally effective.
- B) Chain-of-thought prompting is only useful for coding tasks.
- C) The model cannot reason across multiple documents regardless of prompting approach.
- D) A chain-of-thought prompting approach, allowing explicit intermediate reasoning steps, is well suited to this kind of multi-study synthesis question.

**Question 26.** The platform wants to standardize prompt fragments (citation format, disclaimer language, formatting rules) across several different scientist-facing features so changes propagate consistently.

- A) Use modular, composable, versioned prompt fragments shared across features — a maintainability lever distinct from caching (a cost/latency lever) or Skills (a capability-packaging lever).
- B) Duplicate the fragments into each feature's prompt independently.
- C) Modular prompts are the same thing as prompt caching.
- D) Standardization across features isn't achievable with prompt design.

**Question 27.** The system occasionally returns confident, well-cited-looking answers that, on manual review, misstate a specific figure from the correctly retrieved source document.

- A) Trust the fluent, well-formatted output as evidence of correctness.
- B) This is not something an architecture can address; it's purely a model limitation with no mitigation.
- C) Apply defensive validation — verify extracted figures against the actual source excerpt rather than accepting confident, well-formatted phrasing as proof of accuracy.
- D) Increase output length so there's more room to be correct.

**Question 28.** The team debates whether scientist-facing latency SLAs should factor into model tier selection.

- A) Latency should never factor into model or architecture decisions.
- B) Only cost should factor into tier selection, never latency.
- C) Yes — model tier selection should weigh accuracy needs against the latency and cost the use case's SLA can tolerate, not default to the most capable tier regardless of SLA.
- D) SLAs are a stakeholder-communication concern with no bearing on technical architecture.

**Question 29.** A new model version is released with improved benchmark scores. The platform currently floats to "latest" automatically in production.

- A) Continue floating to latest automatically, since newer is always better.
- B) Pin the current version in production and evaluate the new version against the platform's own tests before deliberately upgrading, since behavior can shift across releases even at improved benchmark scores.
- C) Never upgrade models once the initial version is chosen.
- D) Upgrade immediately without testing, since benchmark improvements guarantee production improvements.

**Question 30.** The platform's context budget is a concern because both the system prompt/citation rules and the retrieved study excerpts must fit alongside room for a detailed answer.

- A) Input and output share the same context-window budget, so architects must balance retrieved-content volume against the room needed for a detailed, well-cited answer.
- B) Output length has no practical limit regardless of input size.
- C) This tradeoff only matters for very long documents, never for typical queries.
- D) Input and output token budgets are entirely independent of each other.

---

## Scenario C: Evaluation and Optimization of an HR Recruiting Assistant (Questions 31–45)

A Claude-powered recruiting assistant screens resumes, drafts candidate outreach messages, and answers candidate FAQs for a mid-size tech company's talent acquisition team. It has been in production for six months, and you are responsible for the evaluation strategy, diagnosing quality issues, and optimizing cost/latency/accuracy tradeoffs.

---

**Question 31.** The team currently measures only resume-screening throughput and hasn't defined targets for accuracy, latency, cost, or fairness.

- A) Define evaluation metrics spanning accuracy, latency, cost, and safety/fairness as first-class metrics — a system that screens quickly but is inaccurate, slow to correct itself, expensive, or unfair still fails overall.
- B) Throughput alone is sufficient, since it's the system's primary purpose.
- C) Latency and cost are operations concerns unrelated to evaluation design.
- D) Fairness metrics are only relevant if a complaint has already been filed.

**Question 32.** The evaluation dataset currently consists only of automated accuracy checks against a fixed labeled set of past resumes.

- A) A single automated method is sufficient for any production system.
- B) Use mixed methodologies — automated eval for scale, human review for nuanced judgment calls, and adversarial/edge-case testing for fairness-relevant paths — since no single method covers every failure mode.
- C) Replace the automated checks entirely with only human review.
- D) Expand the labeled set indefinitely as the sole improvement lever.

**Question 33.** The team wants to test whether a new screening-prompt version improves accuracy before rolling it out to all requisitions.

- A) Roll out the new prompt to all requisitions immediately and monitor for problems.
- B) Change the prompt and the model tier simultaneously to maximize potential improvement.
- C) Skip testing, since prompt changes are low-risk by nature.
- D) Run an A/B test changing only the prompt version against a stable baseline, so any observed difference can be attributed to that one change.

**Question 34.** A candidate is incorrectly screened out. Investigation shows the underlying resume was parsed and retrieved correctly, and the model's screening rationale misread a clearly-stated qualification.

- A) This is a retrieval/parsing problem; fix the ingestion pipeline.
- B) This cannot be diagnosed without retraining the model.
- C) This is a model mismatch requiring a different model tier regardless of the specific failure.
- D) This is best characterized as a generation/reasoning issue (misreading correctly retrieved content), which calls for prompt or output-validation fixes rather than ingestion changes.

**Question 35.** Immediately after a scheduled update to the job-requisition template library, the assistant starts screening out qualified candidates at a higher rate, while model version and average latency are unchanged.

- A) Suspect the model was silently updated by the provider.
- B) Investigate the requisition-template/retrieval layer first, since the regression is tied specifically to the template update event with model and latency unchanged.
- C) Suspect a temperature setting change, since screening behavior changed.
- D) Suspect the context window shrank.

**Question 36.** The team wants to reduce cost and latency in outreach-message drafting but is worried about hurting quality, with no current data on where the configuration sits on that tradeoff curve.

- A) Cost, latency, and quality should each be optimized independently, in isolation from one another.
- B) Optimize cost/latency/quality jointly against the system's actual SLA and budget — the cheapest, fastest configuration that fails the quality bar isn't a win, and neither is maximizing quality at unsustainable cost.
- C) Quality should always be maximized regardless of cost or latency implications.
- D) This tradeoff cannot be measured, only guessed at.

**Question 37.** Production monitoring currently reports only an overall weekly average screening-accuracy score.

- A) Monitoring should surface drift and outliers — a per-role or per-requisition-type breakdown — since an aggregate average can hide a specific failing segment even while looking healthy overall.
- B) A single aggregate average is sufficient for production monitoring.
- C) Monitoring should track only cost, since accuracy is captured by the eval suite alone.
- D) Weekly granularity is always sufficient regardless of system behavior.

**Question 38.** The team proposes cutting human review of flagged low-confidence screens by 80%, citing a 96% aggregate accuracy score.

- A) Proceed with the cut based on the 96% aggregate figure alone.
- B) Segment accuracy by role and requisition type before cutting review, since the aggregate figure can mask a specific segment performing far worse than the average.
- C) Aggregate accuracy is definitionally representative of every segment.
- D) Human review should never be reduced regardless of measured accuracy.

**Question 39.** An A/B test shows a new screening-prompt version improves throughput, but the team hasn't checked whether it also changed the false-negative rate on genuinely qualified candidates from underrepresented backgrounds.

- A) Throughput alone is a sufficient signal to ship the change.
- B) Check the fairness-related failure mode specifically before shipping — an isolated throughput improvement could be masking an increase in inappropriate screen-outs for a specific group.
- C) Fairness-related false-negative behavior is not something evaluation can measure.
- D) Ship the change and monitor informally after the fact instead of testing beforehand.

**Question 40.** The team wants to diagnose why a subset of outreach messages are factually accurate but rated poorly by candidates in post-interaction surveys.

- A) Assume the accuracy metric is broken and discard it.
- B) Increase the model's capability tier, assuming higher capability always improves candidate perception.
- C) Ignore candidate satisfaction scores in favor of the accuracy metric alone.
- D) Investigate a dimension beyond factual accuracy — e.g., tone, personalization, or warmth — since "accurate but poorly rated" points at a quality dimension the current eval doesn't measure.

**Question 41.** The team is optimizing token usage and notices the system sends the full candidate conversation history plus a large static company-policy/EEO-compliance document on every turn of multi-turn candidate chats.

- A) This has no optimization opportunity, since full history is always required.
- B) Switch to a smaller model as the only lever for reducing token cost.
- C) Remove the compliance document entirely to save tokens.
- D) Apply prompt caching to the static compliance document and consider trimming or summarizing older turns of conversation history to reduce redundant token cost across a multi-turn conversation.

**Question 42.** Logging captures every raw prompt and response for the production system, and the team treats this as their observability strategy, but no one can identify emerging failure patterns from the volume of raw logs.

- A) Raw logging at full volume is itself a sufficient observability strategy.
- B) Reduce logging to save storage cost, with no other change.
- C) Redesign observability toward structured, aggregable signals — sampling, tagged failure categories, quality metrics by segment — since raw logs at volume aren't reviewable or actionable on their own.
- D) Observability requires no structure as long as data is retained somewhere.

**Question 43.** The team wants to identify whether a recent quality regression was caused by a prompt change, a model version change, or an update to the resume-parsing library — all three shipped in the same week.

- A) Assume the most recent change is always the cause.
- B) Attribution is impossible once multiple changes have shipped in the same week.
- C) Revert all three changes without investigation, regardless of which (if any) caused the regression.
- D) This is why changes should be tested and rolled out one variable at a time — with three simultaneous changes, attribution requires isolating and re-testing each change independently rather than guessing.

**Question 44.** An automated eval asserts that an outreach-message draft must exactly match a fixed reference string, and the eval fails intermittently even on outputs a human reviewer would call correct.

- A) The model is malfunctioning and needs retraining.
- B) The reference string needs to be longer.
- C) Exact-string-match evals are the wrong tool for inherently non-deterministic LLM output; the eval should check for required content/structure rather than exact text.
- D) Temperature should be increased to fix the intermittent failures.

**Question 45.** Leadership wants a single number to represent "how good" the recruiting assistant is, to track over time.

- A) A single number is always achievable and sufficient for any system's evaluation needs.
- B) Use screening throughput alone as the single number, since it's the system's stated purpose.
- C) Refuse to provide any single summary metric under any circumstances.
- D) A single aggregate metric can be a useful top-line indicator, but should be presented alongside segment-level and multi-dimensional detail (accuracy, latency, cost, fairness) so a healthy top-line number doesn't mask a specific failing area.

---

## Scenario D: Governance and Enablement for a Public-Sector FedRAMP Deployment (Questions 46–60)

A state health-and-human-services agency is deploying a Claude-powered system that processes benefits-eligibility case files under a FedRAMP Moderate authorization, and assists a 25-person caseworker operations team using Claude Code internally. You are responsible for governance, compliance, and developer enablement for the launch.

---

**Question 46.** The architecture team is finalizing data flow, retention, and access-logging design in the final week before launch, after core application logic is already built.

- A) This sequencing carries no risk, since compliance can always be added right before launch.
- B) Compliance only affects legal documentation, not system architecture.
- C) HIPAA, not FedRAMP, is the relevant regime for a public-sector benefits system.
- D) FedRAMP-driven data residency, boundary, and access-logging requirements can force structural changes that are far more costly to retrofit than to design in from the start.

**Question 47.** A team proposes requiring caseworker approval on every single output the eligibility system produces, framing it as the safest governance posture.

- A) Maximal human review on every output is always the correct default for public-sector AI systems.
- B) Blanket human-in-the-loop on every output defeats much of the system's value; HITL should be targeted at high error-cost or genuinely judgment-requiring decisions (e.g., denial determinations) rather than applied universally.
- C) Human reviewers are categorically less accurate than the model, making review counterproductive.
- D) This approach is required by the Privacy Act regardless of other considerations.

**Question 48.** The system must identify and mitigate standard LLM risks — hallucination, prompt injection from applicant-submitted free text, and inconsistent output — as part of its design.

- A) These risks only need to be addressed if they're observed in production first.
- B) These risks are exclusive to private-sector use cases.
- C) Design mitigations for each known failure mode as part of the architecture up front — e.g., grounding/verification for hallucination, input isolation and guardrails for injection, output validation for consistency — rather than as a reactive afterthought.
- D) A single generic guardrail addresses all three risk types equally well.

**Question 49.** The agency's civil-rights office asks whether the system's eligibility recommendations could produce disparate outcomes across different applicant demographics.

- A) This is not an architectural concern; it belongs entirely to legal/compliance review after launch.
- B) Disparate impact is impossible in an LLM-based system by construction.
- C) Bias, fairness, and transparency are architecture concerns — evaluate whether training/eval data reflects the served population and measure for disparate impact rather than assuming it's absent.
- D) This concern only applies to systems making final, unreviewed determinations, not any assistive system.

**Question 50.** The 25-person caseworker operations team's Claude Code usage is inconsistent — some staff have team conventions applied automatically, others don't, and internal MCP server access varies by machine.

- A) Restrict Claude Code usage to a single designated engineer to reduce variance.
- B) Have each staff member individually troubleshoot their own local configuration.
- C) Standardize CLAUDE.md hierarchy and shared MCP server configuration at the team/project level so behavior doesn't depend on individual local setup.
- D) Accept the inconsistency as an unavoidable cost of AI tooling adoption.

**Question 51.** The team wants Claude Code-generated code changes in this FedRAMP context to go through the same review rigor as any other change to an authorized system.

- A) AI-assisted code should bypass standard review, since it was "written by AI."
- B) Only a spot-check of AI-generated code is necessary.
- C) Review requirements should be lower for AI-generated code than human-written code.
- D) Standard SDLC practices — code review, testing, version control, change control — still apply; Claude Code assisting with generation doesn't reduce the review rigor required for an authorized system.

**Question 52.** A production incident traces back to a Claude Code-generated data-handling change. The team can't immediately tell whether the bug is in the generated code logic or in how the surrounding system integrated it.

- A) Assume the bug is in the generated code without investigation.
- B) Triage the same way any incident is triaged — isolate whether the issue is in the integration layer or the code/model output — using traces/logs to localize the actual failure point.
- C) Disable Claude Code for the team entirely following any incident.
- D) Roll back all recent Claude Code-assisted changes regardless of relevance.

**Question 53.** The caseworker operations team wants a documented, repeatable workflow for a recurring task (generating a weekly eligibility-determination audit report) versus a one-off exploratory data-migration script.

- A) Build both as MCP servers regardless of reuse profile.
- B) Build both as ad hoc, undocumented prompts each time they're needed.
- C) Recurring workflows and one-off tasks should be built identically.
- D) Package the recurring, well-defined report workflow as a Skill for on-demand, consistent reuse; leave the one-off exploratory script as an unstructured session, since it doesn't need standing infrastructure.

**Question 54.** The compliance office wants documented evidence of who accessed what applicant-related data through the system and when.

- A) Access logging is optional if the system has role-based permissions.
- B) Design access-control and audit-logging as explicit architectural components satisfying identity validation, authorization, and monitoring requirements — not an implicit byproduct of normal operation.
- C) Only failed access attempts need to be logged.
- D) Audit logging can be added later without architectural impact.

**Question 55.** The steering committee for this deployment includes caseworker operations, legal/compliance, and engineering stakeholders with different priorities and vocabularies.

- A) Communicate only with the engineering stakeholders, since they'll relay information to the others.
- B) Tailor architectural communication to each audience — tradeoffs framed in terms caseworker and compliance stakeholders can evaluate against their own priorities, not just engineering metrics.
- C) Use identical technical documentation for all three audiences to save effort.
- D) Skip stakeholder communication until the system is fully built.

**Question 56.** Midway through the project, eligibility-determination requirements shift meaningfully based on new state legislation.

- A) Treat this as a normal part of lifecycle management — re-engage discovery for the affected scope, communicate the tradeoff of the change to stakeholders, and adjust the design and timeline accordingly.
- B) Refuse to incorporate the change, since requirements were already agreed upon.
- C) Incorporate the change silently without informing stakeholders of the impact.
- D) Restart the entire project from scratch regardless of the change's actual scope.

**Question 57.** After launch, the architect's involvement is discussed as ending at handoff to the operations team.

- A) This is the correct lifecycle model; monitoring and iteration are entirely the operations team's responsibility.
- B) Lifecycle management includes monitoring and iteration based on production signal as part of the architect's ongoing responsibility, not just discovery through handoff.
- C) Lifecycle responsibility ends once the authorization to operate (ATO) is granted.
- D) Monitoring is only necessary if a major incident occurs.

**Question 58.** Documentation for this system currently lists final configuration values (model tier, retry settings, thresholds) with no explanation of why each was chosen.

- A) This level of documentation is sufficient, since the "what" is all a future team needs.
- B) Documenting reasoning is unnecessary overhead in a regulated environment.
- C) Documentation should also capture the "why" behind key decisions — compliance drivers, tradeoff reasoning — so a future team can safely extend or modify the system without re-deriving that context.
- D) Only the original architect should ever be allowed to modify the system, making documentation moot.

**Question 59.** The caseworker operations team wants Claude Code to help with routine tasks (drafting documentation, exploring an unfamiliar module) but is unsure where it actually saves meaningful time versus adding review overhead.

- A) Evaluate specific task categories for genuine friction reduction (e.g., repetitive documentation drafting, codebase exploration) versus cases where review overhead may exceed time saved, rather than assuming a blanket benefit.
- B) Ban Claude Code for all documentation tasks without evaluation.
- C) Mandate Claude Code usage for all tasks regardless of measured benefit.
- D) Assume AI-assisted tooling always saves time on every task category by default.

**Question 60.** A recurring operational issue is that different engineers debug similar Claude Code integration failures independently, each re-deriving the same integration-layer-versus-model-output triage process.

- A) This is an acceptable ongoing inefficiency with no architectural fix.
- B) Document the triage process (how to distinguish integration-layer failures from model-output failures for this system) as shared operational knowledge, reducing redundant re-derivation across the team.
- C) Restrict debugging to a single designated engineer.
- D) The issue can only be resolved by switching to a different tool entirely.

---
# Answer Key — Practice Exam 3

**Quick key:** 1-D, 2-A, 3-A, 4-C, 5-C, 6-C, 7-A, 8-D, 9-A, 10-B, 11-A, 12-D, 13-A, 14-D, 15-D, 16-C, 17-C, 18-C, 19-C, 20-A, 21-A, 22-B, 23-A, 24-B, 25-D, 26-A, 27-C, 28-C, 29-B, 30-A, 31-A, 32-B, 33-D, 34-D, 35-B, 36-B, 37-A, 38-B, 39-B, 40-D, 41-D, 42-C, 43-D, 44-C, 45-D, 46-D, 47-B, 48-C, 49-C, 50-C, 51-D, 52-B, 53-D, 54-B, 55-B, 56-A, 57-B, 58-C, 59-A, 60-B

---

**1. D** — The stated goal (fewer contract attorneys, same turnaround) is a cost/efficiency problem; naming that pillar correctly shapes both the architecture and its success metrics. A and C misname the pillar as transformation/new capability, and B drops the cost objective discovery actually surfaced.

**2. A** — Steps that vary by document type, protective-order terms, and intermediate findings (a privilege hit changing downstream handling) are the defining case for an agentic pattern. B assumes a predictability the scenario lacks; C undersells the orchestration needed; D ignores real, non-interchangeable tradeoffs.

**3. A** — Routing the privilege determination through the coordinator preserves observability and consistent handling of privilege calls across the matter. B and D sacrifice this for a shortcut or noise; C discards the specialization that motivated separate subagents.

**4. C** — Every subagent succeeding while redundantly re-deriving the same OCR output is a coordinator data-flow problem, not a subagent capability gap. A, B, and D all patch around the issue instead of fixing the missing hand-off.

**5. C** — Discovery surfacing defensibility as the actual driving concern means the pillar and its metrics should shift toward auditability/explainability, not stay anchored to the originally named pillar. A and D ignore what discovery revealed; B conflates two distinct concerns.

**6. C** — Adoption/liability sentiment about unsupervised withholding decisions is a real implicit constraint that should shape a specific HITL checkpoint in the architecture. A and B treat it as out of scope; D overreacts to sentiment alone without weighing the technical case.

**7. A** — Explaining the specific tradeoff (deeper legal reasoning need vs. added cost/latency) is the standard for stakeholder communication about architectural decisions. B and D remove or hide a deliberate, justified difference; C withholds reasoning partners need.

**8. D** — Adding a feedback loop that captures attorney overrides and reasoning as a first-class architectural component is what lets the system improve post-deployment. A, B, and C all treat this component as optional or someone else's problem.

**9. A** — A single call enhanced with retrieval, without multi-step autonomous orchestration, is exactly what an augmented LLM pattern is for. B and D over-engineer a simple augmentation need; C is factually wrong.

**10. B** — Tools unrelated to a subagent's core role degrade tool-selection reliability as the candidate set grows; the fix is removing or relocating them. A and C ignore this real degradation; D doesn't address selection reliability at all.

**11. A** — Independent subagent calls with no data dependency between them can run in parallel once their shared prerequisite (intake) completes, reducing latency without sacrificing correctness. B and C misstate real constraints; D avoids the sequencing question rather than answering it.

**12. D** — A steering-level audience needs the architecture communicated at the level of business-outcome evaluation, not implementation internals. A and B are the wrong level of detail; C skips the communication need entirely.

**13. A** — A single generalist agent holding every tool and responsibility is more exposed to degraded tool-selection reliability than agents scoped to narrower roles — the core argument for specialization. B, C, and D understate or deny this real architectural tradeoff.

**14. D** — Reasonable extensibility without over-building for undefined future requirements balances current delivery against future flexibility. A wastes effort guessing at undefined requirements; B ignores a known future need entirely; C blocks current delivery unnecessarily.

**15. D** — Documenting the reasoning behind key decisions, not just final values, is what lets a future team safely extend the system without the original architect present. A, B, and C all leave the actual knowledge-transfer gap unaddressed.

**16. C** — Routing by task difficulty matches the fast/balanced/high-capability tiers to the actual mix of simple, typical, and complex questions. A and D ignore fit-to-task; B sacrifices quality on the cases that need capability most.

**17. C** — Placing stable content first with caching enabled, and variable content after, maximizes the cacheable prefix across high query volume, reducing latency and cost. A, B, and D all misstate or break the caching opportunity.

**18. C** — Chunking and indexing strategy must match each data shape; a single strategy tuned for one content type degrades retrieval for the mismatched type. A and B ignore this mismatch; D discards useful structured data.

**19. C** — Matching retrieval mechanism to query pattern — structured filtering for exact lookups, embeddings for conceptual questions, hybrid where needed — is the correct architecture. A and B force one mechanism onto queries it doesn't fit; D denies a real, consequential distinction.

**20. A** — Structured claim-source pairing preserves citation mapping through synthesis; prose citation requests and after-the-fact citation search are exactly the patterns that lose or fabricate mappings. B, C, and D all reintroduce the failure mode the fix is meant to prevent.

**21. A** — Presenting both figures with attribution and the likely methodological explanation preserves the actual information for the scientist rather than resolving a real discrepancy arbitrarily. B, C, and D all discard or obscure a genuine data conflict.

**22. B** — Schema-constrained tool-use output is enforced by the API mechanism, unlike prose requests that can still drift. A and C are workarounds for a structurally solvable problem; D doesn't address the preamble at all.

**23. A** — An MCP server matches the described need: reusable access across multiple different internal Claude-powered tools, maintained independently. B, C, and D all fail the reuse or maintainability requirement.

**24. B** — Progressive discovery via a queryable catalog resource scales with corpus growth better than loading the entire catalog into every prompt. A and C ignore the real context cost of the monolithic approach; D removes needed capability entirely.

**25. D** — Chain-of-thought prompting, allowing explicit intermediate reasoning, fits multi-study synthesis requiring step-by-step reasoning. A, B, and C all misstate the fit or capability of prompting techniques for this task.

**26. A** — Modular, versioned prompt fragments are a maintainability lever distinct from caching (cost/latency) and Skills (capability packaging) — the right tool for consistent propagation of shared fragments across features. B reintroduces duplication; C conflates two distinct mechanisms; D denies a real, common architecture pattern.

**27. C** — Verifying extracted figures against source excerpts catches confident-but-wrong output that fluent formatting alone would let through. A is the failure mode itself; D doesn't address correctness; B incorrectly claims no architectural mitigation exists.

**28. C** — Weighing accuracy needs against latency/cost relative to the SLA is standard model-tier decision-making; defaulting to maximum capability regardless of SLA ignores a real, decidable tradeoff. A, B, and D each drop a relevant factor from the decision.

**29. B** — Pinning and deliberately testing against the platform's own evaluation before upgrading avoids unattributed behavior drift, even when benchmark scores improve. A and D assume benchmark gains transfer automatically; C over-corrects into permanent stagnation.

**30. A** — Input and output share one context-window budget, directly constraining how much retrieved content and answer detail can coexist. B, C, and D all misstate this real, architecture-relevant constraint.

**31. A** — Accuracy, latency, cost, and safety/fairness should all be defined as first-class metrics, since a system failing on any of them fails overall even if it screens quickly. B, C, and D each drop a dimension that materially affects whether the system is actually working well.

**32. B** — Mixed methodologies (automated, human, adversarial) are needed because no single method covers every failure mode, especially fairness-relevant edge cases. A, C, and D each over-rely on or discard one method without addressing the actual coverage gap.

**33. D** — Changing only the prompt version against a stable baseline is what allows the observed difference to be attributed correctly to that one change. A skips testing entirely; B confounds two variables; C dismisses a real risk without evidence.

**34. D** — Correct parsing plus a misread qualification is a generation-side issue, calling for prompt or output-validation fixes rather than ingestion or model-tier changes. A and C misdiagnose the layer at fault; B avoids diagnosis entirely.

**35. B** — A regression tied specifically to a template-update event, with model and latency unchanged, points first at the requisition-template/retrieval layer. A, C, and D would not specifically correlate with that update.

**36. B** — Joint optimization against the actual SLA and budget avoids both an unsustainably expensive "quality at all costs" outcome and a cheap configuration that fails the quality bar. A and C optimize dimensions in isolation; D claims the tradeoff is unmeasurable when it is not.

**37. A** — Segment/outlier-aware monitoring surfaces problems an aggregate weekly average can hide. B and D accept a monitoring blind spot; C drops accuracy monitoring from observability entirely.

**38. B** — Segmenting accuracy by role/requisition type before cutting review protects against a failing segment hiding behind a healthy aggregate. A and C trust the aggregate uncritically; D over-corrects by refusing any reduction regardless of evidence.

**39. B** — An isolated throughput improvement could mask a worsened fairness-related failure mode; checking specifically for that before shipping is the correct diagnostic step. A and D ship without adequate testing; C incorrectly claims the failure mode is unmeasurable.

**40. D** — "Accurate but poorly rated" points at an unmeasured quality dimension (tone, personalization, warmth) rather than a broken accuracy metric. A and C discard a working, differently-scoped metric; B assumes a fix without diagnosis.

**41. D** — Caching the static compliance document and trimming/summarizing older turns directly reduces redundant token cost in multi-turn conversations. A denies an obvious lever; C removes needed content; B is a blunt, quality-risking lever when a more targeted fix is available.

**42. C** — Structured, sampled, and tagged signals are what make observability actionable at volume; raw logs alone aren't reviewable. A and D accept the described dysfunction; B addresses cost, not the actual observability gap.

**43. D** — With three simultaneous changes, correct attribution requires isolating and re-testing each independently — exactly the discipline one-variable-at-a-time testing is meant to preserve. A and C guess without evidence; B gives up on a solvable (if effortful) diagnostic problem.

**44. C** — Non-deterministic output makes exact-string-match evals structurally unsuited to this task; content/structure-based checks are the correct fix. A and D misdiagnose model behavior as broken; B doesn't address the actual mismatch between eval design and output variability.

**45. D** — A top-line number can be useful communication but should be paired with segment- and dimension-level detail so it doesn't mask a specific failing area. A and B oversimplify to a single lossy number; C refuses a reasonable, common stakeholder request.

**46. D** — FedRAMP-driven boundary, residency, and logging requirements can force structural changes that are far costlier to retrofit after core logic is built than to design in from the start. A and B understate real architectural impact; C misidentifies the applicable regulatory regime.

**47. B** — Blanket human review on every output defeats much of the system's value; HITL should target high error-cost or judgment-requiring decisions specifically. A and C overstate the universal safety case for maximal review; D misattributes this to a statute that isn't the relevant driver described.

**48. C** — Designing mitigations for each known failure mode (grounding for hallucination, isolation/guardrails for injection, validation for consistency) up front is the architecture-first approach the domain calls for. A defers to a reactive posture; D assumes one guardrail covers distinct risk types; B is factually wrong.

**49. C** — Bias, fairness, and transparency are architecture concerns requiring active measurement (data representativeness, disparate-impact checks), not an assumption of absence. A defers a design concern entirely to a later stage; B and D make unsupported blanket claims.

**50. C** — Standardizing CLAUDE.md and shared MCP configuration at the team level directly fixes the described inconsistency, which stems from relying on individual local setup. B and D leave the systemic cause unaddressed; A sacrifices the tool's benefit for the rest of the team.

**51. D** — Standard SDLC review rigor still applies regardless of whether Claude Code assisted with generation, especially for an authorized system. A, B, and C all propose reducing rigor specifically because AI was involved, which is the wrong direction in this context.

**52. B** — Standard incident triage — isolating integration-layer versus model/code-output failure via traces/logs — applies here just as it would to any other incident. A and C skip diagnosis; D is a disproportionate reaction that doesn't investigate the actual cause.

**53. D** — Packaging the recurring, well-defined report as a Skill matches its reuse profile; leaving the one-off exploratory script unstructured avoids unnecessary standing infrastructure. A over-engineers the one-off task; B under-serves the recurring task; C ignores that reuse profile should drive the choice.

**54. B** — Access control and audit logging need to be explicit architectural components satisfying identity, authorization, and monitoring requirements — not an incidental byproduct. A, C, and D each understate what compliance-grade audit evidence actually requires.

**55. B** — Tailoring communication to each stakeholder group's priorities and vocabulary is what makes architectural tradeoffs actually evaluable by caseworker, compliance, and engineering audiences alike. A, C, and D each fail to serve at least one audience's real information need.

**56. A** — Re-engaging discovery for the affected scope and communicating the tradeoff of the change is standard lifecycle management for a legitimate, externally-driven requirements shift. B and C mishandle a real change; D disproportionately discards unaffected work.

**57. B** — Lifecycle management extends through monitoring and iteration based on production signal, not just through handoff. A, C, and D all end architectural responsibility earlier than the lifecycle model calls for.

**58. C** — Capturing the "why" (compliance drivers, tradeoff reasoning) alongside the "what" is what lets a future team safely extend the system, especially in a regulated context. A, B, and D all leave that reasoning undocumented and effectively lost.

**59. A** — Evaluating specific task categories for genuine friction reduction versus added review overhead gives an evidence-based answer instead of assuming a blanket benefit either way. C and D over-assume benefit; B forecloses potential benefit without evaluation.

**60. B** — Documenting the shared triage process turns individually re-derived knowledge into reusable operational knowledge, directly addressing the redundant-effort problem described. A accepts avoidable inefficiency; C and D propose disproportionate structural changes instead of the straightforward documentation fix.

---

*End of Practice Exam 3.*
